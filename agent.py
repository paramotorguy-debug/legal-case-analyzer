"""LLM agent for case-to-lawyer matching.

Reads accumulated referral history (decisions, declines, outcomes) and recommends
a lawyer for a new case with a rationale. Falls back gracefully if ANTHROPIC_API_KEY
is not set — the rule-based engine in matching.py keeps working.

Phase 3 of the project: this is the "real LLM behind the decision-capture loop"
the rest of the app has been collecting training data for.
"""
import os
import json

from constants import (
    CASE_TYPE_LABELS,
    VALUE_TIER_LABELS,
    INTAKE_STRENGTH_LABELS,
    INTAKE_SIGNAL_LABELS,
    REFERRAL_REASON_LABELS,
    DECLINE_REASON_LABELS,
    OUTCOME_LABELS,
    US_STATE_LABELS,
)

MODEL = "claude-sonnet-4-6"


def is_configured():
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def _client():
    from anthropic import Anthropic
    return Anthropic()


SYSTEM_PROMPT = """You are an AI agent embedded in a legal case-referral platform. Your job is to recommend which lawyer in the user's network should receive a new case, based on:

1. The case's structured features (type, value tier, jurisdiction, intake strength, signals).
2. The lawyer's profile (practice areas, jurisdictions, value tiers, capacity, preferences).
3. The user's past referral patterns — specifically: which lawyer they chose for similar cases, the structured reasons they gave, when they overrode the rule-based suggestion, when lawyers DECLINED and why, and when accepted referrals settled / paid out.

Decline reasons and outcomes are the most valuable signals — they tell you which referrals would have been wrong even when they looked right on paper.

You must:
- Recommend exactly one lawyer (by their id) from the available list.
- Never recommend a lawyer who has already declined this case (listed under "Previously declined by").
- Reference the user's past patterns in your rationale when you can.
- Be honest about confidence. If history is thin or the case doesn't clearly match a past pattern, say "low" or "medium" confidence.
- Output ONLY a JSON object — no prose before or after — matching the requested schema."""


def _format_lawyers(lawyers):
    lines = []
    for l in lawyers:
        cap = l.get("capacity") or {}
        lines.append(
            f"- id={l['id']} | {l['name']} ({l.get('firm', '')}) | "
            f"practices: {', '.join(l.get('practice_areas') or []) or '—'} | "
            f"states: {', '.join(l.get('states') or []) or '—'} | "
            f"value tiers: {', '.join(l.get('value_tiers') or []) or '—'} | "
            f"capacity: {cap.get('current', 0)}/{cap.get('max', 0)} | "
            f"fee: {l.get('referral_fee') or '—'} | "
            f"prefs: {l.get('preferences') or '—'}"
        )
    return "\n".join(lines) if lines else "(no lawyers in network)"


def _format_history(cases, lawyers):
    by_id = {l["id"]: l for l in lawyers}
    refs = [c for c in cases if c.get("assigned_lawyer_id")]
    if not refs and not any(c.get("previously_referred_to") for c in cases):
        return "(no past referrals yet)"

    lines = []
    for c in refs:
        lw = by_id.get(c["assigned_lawyer_id"])
        ln = (
            f"- Case ({CASE_TYPE_LABELS.get(c.get('case_type'), c.get('case_type'))}, "
            f"{VALUE_TIER_LABELS.get(c.get('value_tier'), c.get('value_tier'))}, "
            f"{c.get('city') or ''} {c.get('state') or ''}): "
            f"chose {lw['name'] if lw else c['assigned_lawyer_id']} (id={c['assigned_lawyer_id']})"
        )
        if c.get("referral_reasons"):
            ln += f" — reasons: {', '.join(REFERRAL_REASON_LABELS.get(r, r) for r in c['referral_reasons'])}"
        if c.get("referral_was_override"):
            ln += " [override of rule-based top suggestion]"
        if c.get("intake_strength"):
            ln += f" | strength: {INTAKE_STRENGTH_LABELS.get(c['intake_strength'], c['intake_strength'])}"
        if c.get("intake_signals"):
            ln += f" | signals: {', '.join(INTAKE_SIGNAL_LABELS.get(s, s) for s in c['intake_signals'])}"
        if c.get("lawyer_response") == "accepted":
            ln += " | ACCEPTED"
        elif c.get("lawyer_response") == "declined":
            ln += f" | DECLINED: {', '.join(DECLINE_REASON_LABELS.get(r, r) for r in c.get('decline_reason_codes', []))}"
        if c.get("outcome"):
            ln += f" → outcome: {OUTCOME_LABELS.get(c['outcome'], c['outcome'])}"
            if c.get("outcome_amount"):
                ln += f" (${c['outcome_amount']:,.0f})"
        lines.append(ln)

    for c in cases:
        for prev in c.get("previously_referred_to") or []:
            lw = by_id.get(prev.get("lawyer_id"))
            lines.append(
                f"- Past decline: {lw['name'] if lw else prev.get('lawyer_id')} "
                f"(id={prev.get('lawyer_id')}) declined a "
                f"{CASE_TYPE_LABELS.get(c.get('case_type'), c.get('case_type'))} / "
                f"{VALUE_TIER_LABELS.get(c.get('value_tier'), c.get('value_tier'))} case "
                f"— reasons: {', '.join(DECLINE_REASON_LABELS.get(r, r) for r in prev.get('decline_reasons') or [])}"
            )
    return "\n".join(lines)


def _format_case(case):
    juris_bits = [b for b in [case.get("city"), US_STATE_LABELS.get(case.get("state"), case.get("state"))] if b]
    juris = ", ".join(juris_bits) or "(unspecified)"

    declined_by = [p.get("lawyer_id") for p in (case.get("previously_referred_to") or [])]

    parts = [
        f"Case type: {CASE_TYPE_LABELS.get(case.get('case_type'), case.get('case_type'))}",
        f"Value tier: {VALUE_TIER_LABELS.get(case.get('value_tier'), case.get('value_tier'))}",
        f"Location: {juris}",
    ]
    if case.get("intake_strength"):
        parts.append(f"Intake strength: {INTAKE_STRENGTH_LABELS.get(case['intake_strength'], case['intake_strength'])}")
    if case.get("intake_signals"):
        parts.append(f"Intake signals: {', '.join(INTAKE_SIGNAL_LABELS.get(s, s) for s in case['intake_signals'])}")
    if case.get("comments"):
        parts.append(f"Client comments: {case['comments']}")
    if declined_by:
        parts.append(f"Previously declined by lawyer ids: {', '.join(declined_by)} (do NOT recommend these)")
    return "\n".join(parts)


def suggest(case, lawyers, history_cases):
    """Returns dict with recommended_lawyer_id, rationale, key_factors, confidence,
    alternatives — or None if not configured / call failed."""
    if not is_configured() or not lawyers:
        return None

    user_msg = (
        "Available lawyers in the network:\n"
        f"{_format_lawyers(lawyers)}\n\n"
        "Past referral history (the user's revealed preferences):\n"
        f"{_format_history(history_cases, lawyers)}\n\n"
        "New case to evaluate:\n"
        f"{_format_case(case)}\n\n"
        "Output JSON only, this exact shape:\n"
        '{\n'
        '  "recommended_lawyer_id": "<one id from the list above>",\n'
        '  "rationale": "<1-2 sentences citing case features and past patterns>",\n'
        '  "key_factors": ["<short factor>", "<short factor>", ...],\n'
        '  "confidence": "high" | "medium" | "low",\n'
        '  "alternatives": [{"lawyer_id": "<id>", "reason": "<short reason>"}]\n'
        '}'
    )

    try:
        resp = _client().messages.create(
            model=MODEL,
            max_tokens=600,
            system=[
                {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}},
            ],
            messages=[{"role": "user", "content": user_msg}],
        )
    except Exception as e:
        return {"error": str(e)}

    text = "".join(b.text for b in resp.content if hasattr(b, "text"))
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return {"error": "Agent did not return JSON.", "raw": text[:400]}
    try:
        parsed = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return {"error": "Could not parse agent JSON.", "raw": text[:400]}

    valid_ids = {l["id"] for l in lawyers}
    declined_ids = {p.get("lawyer_id") for p in (case.get("previously_referred_to") or [])}
    if parsed.get("recommended_lawyer_id") not in valid_ids:
        return {"error": "Agent recommended an unknown lawyer.", "raw": parsed}
    if parsed.get("recommended_lawyer_id") in declined_ids:
        return {"error": "Agent recommended a lawyer who already declined this case.", "raw": parsed}

    parsed["alternatives"] = [
        a for a in (parsed.get("alternatives") or [])
        if a.get("lawyer_id") in valid_ids and a.get("lawyer_id") not in declined_ids
    ][:3]

    if hasattr(resp, "usage"):
        parsed["_usage"] = {
            "input_tokens": getattr(resp.usage, "input_tokens", None),
            "output_tokens": getattr(resp.usage, "output_tokens", None),
        }
    return parsed
