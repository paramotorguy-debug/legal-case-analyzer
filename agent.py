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
    CASE_TYPES,
    CASE_TYPES_BY_PRACTICE,
    PRACTICE_AREAS,
    CASE_TYPE_LABELS,
    VALUE_TIERS,
    VALUE_TIER_LABELS,
    INTAKE_STRENGTH,
    INTAKE_STRENGTH_LABELS,
    INTAKE_SIGNAL_LABELS,
    INTAKE_SIGNAL_GROUPS_BY_TYPE,
    UNIVERSAL_INTAKE_GROUPS,
    REFERRAL_REASON_LABELS,
    DECLINE_REASON_LABELS,
    OUTCOME_LABELS,
    US_STATE_CODES,
    US_STATE_LABELS,
    signal_groups_for,
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


# ============================================================================
# Email parser — turns a forwarded intake email into a populated case form.
# ============================================================================

PARSE_PROMPT = """You are an intake assistant for Litics, a legal case-routing platform. You receive raw forwarded emails (often messy — quoted threads, forwarded headers, signatures) and extract structured case fields for the firm's intake system.

You will be given:
1. The case-type taxonomy (codes + labels, organized by practice area)
2. The intake-signal taxonomy (signals organized by case_type — only select signals that belong to the case_type you classify)
3. The raw email content

Output ONLY a JSON object matching this schema:

{
  "name": str | null,
  "email": str | null,
  "phone": str | null,
  "property_address": str | null,
  "city": str | null,
  "state": str | null,                // 2-letter US code
  "case_type": str | null,            // one of the listed codes
  "value_tier": str | null,           // "low" | "medium" | "high" | "major"
  "intake_strength": str | null,      // "strong" | "moderate" | "weak" | "insufficient_info"
  "intake_signals": [str],            // codes only, must be valid for chosen case_type
  "comments": str,                    // 2-4 sentence summary IN YOUR OWN WORDS
  "extraction_notes": str             // one line: what you inferred vs stated; flags for review
}

Rules:
- If a field can't be confidently extracted, use null. Do not guess.
- intake_signals: ONLY select signals applicable to your chosen case_type from the taxonomy. If unsure, leave the array empty. Universal signals (Documentation, Timing, Vulnerability) apply to every case.
- comments: write a clean 2-4 sentence summary in your own words. Do NOT paste the raw email or signature.
- value_tier: estimate based on case severity, dollar amounts mentioned, or injury severity. Be conservative.
- intake_strength: "strong" if liability and damages both look clear; "moderate" if workable with issues; "weak" if proof problems are obvious; "insufficient_info" if you can't tell.
- Output ONLY the JSON object — no prose before or after, no markdown fences."""


def _build_taxonomy_block():
    """Format the case-type and signal taxonomies as a single string for the parse prompt."""
    out = ["CASE TYPES (code: label):"]
    for practice_code, practice_label in PRACTICE_AREAS:
        items = CASE_TYPES_BY_PRACTICE.get(practice_code, [])
        if not items:
            continue
        out.append(f"\n  [{practice_label}]")
        for code, label in items:
            out.append(f"    {code}: {label}")

    out.append("\n\nSIGNALS BY CASE TYPE (only select from the chosen case_type's list, plus universal signals):")
    out.append("\n  [universal — apply to every case]")
    for group_name, group_items in UNIVERSAL_INTAKE_GROUPS:
        for code, label in group_items:
            out.append(f"    {code}: {label}")
    for ct_code, ct_label in CASE_TYPES:
        groups = INTAKE_SIGNAL_GROUPS_BY_TYPE.get(ct_code, [])
        if not groups:
            continue
        out.append(f"\n  [{ct_code} — {ct_label}]")
        for group_name, group_items in groups:
            for code, label in group_items:
                out.append(f"    {code}: {label}")
    return "\n".join(out)


def parse_email(email_text):
    """Extract structured case fields from a raw forwarded email.
    Returns dict with the schema in PARSE_PROMPT, or {error: ...} on failure."""
    if not is_configured():
        return None

    email_text = (email_text or "").strip()
    if not email_text:
        return {"error": "Empty email."}
    # Cap input size to keep the call sane
    if len(email_text) > 16000:
        email_text = email_text[:16000] + "\n\n[...truncated]"

    user_msg = (
        f"{_build_taxonomy_block()}\n\n"
        "EMAIL CONTENT:\n"
        "---\n"
        f"{email_text}\n"
        "---\n\n"
        "Extract the structured case fields per the schema."
    )

    try:
        resp = _client().messages.create(
            model=MODEL,
            max_tokens=1500,
            system=[
                {"type": "text", "text": PARSE_PROMPT, "cache_control": {"type": "ephemeral"}},
            ],
            messages=[{"role": "user", "content": user_msg}],
        )
    except Exception as e:
        return {"error": str(e)}

    text = "".join(b.text for b in resp.content if hasattr(b, "text"))
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return {"error": "Parser did not return JSON.", "raw": text[:400]}
    try:
        parsed = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return {"error": "Could not parse JSON.", "raw": text[:400]}

    # Validate / clean the output
    valid_case_types = {c for c, _ in CASE_TYPES}
    valid_value_tiers = {c for c, _ in VALUE_TIERS}
    valid_strengths = {c for c, _, _ in INTAKE_STRENGTH}

    if parsed.get("case_type") and parsed["case_type"] not in valid_case_types:
        parsed["case_type"] = None
    if parsed.get("value_tier") and parsed["value_tier"] not in valid_value_tiers:
        parsed["value_tier"] = None
    if parsed.get("intake_strength") and parsed["intake_strength"] not in valid_strengths:
        parsed["intake_strength"] = None
    if parsed.get("state") and parsed["state"].upper() not in US_STATE_CODES:
        parsed["state"] = None
    elif parsed.get("state"):
        parsed["state"] = parsed["state"].upper()

    # Filter signals to only those valid for the chosen case_type
    if parsed.get("intake_signals"):
        chosen_ct = parsed.get("case_type")
        if chosen_ct:
            allowed = set()
            for _, items in signal_groups_for(chosen_ct):
                for code, _ in items:
                    allowed.add(code)
            parsed["intake_signals"] = [s for s in parsed["intake_signals"] if s in allowed]
        else:
            # Without a case_type, only allow universal signals
            allowed = set()
            for _, items in UNIVERSAL_INTAKE_GROUPS:
                for code, _ in items:
                    allowed.add(code)
            parsed["intake_signals"] = [s for s in parsed["intake_signals"] if s in allowed]
    else:
        parsed["intake_signals"] = []

    if hasattr(resp, "usage"):
        parsed["_usage"] = {
            "input_tokens": getattr(resp.usage, "input_tokens", None),
            "output_tokens": getattr(resp.usage, "output_tokens", None),
        }
    return parsed
