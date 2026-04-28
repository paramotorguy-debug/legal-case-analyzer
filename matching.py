from constants import CASE_TYPE_LABELS, US_STATE_LABELS


def score_lawyer(case, lawyer):
    """Rule-based scoring. Returns (score, reasons[]).

    Phase 1 placeholder. Phase 2 swaps for an LLM that learns from the
    structured intake_signals + referral_reasons + override history.
    """
    score = 0
    reasons = []

    if case.get("case_type") and case["case_type"] in lawyer.get("practice_areas", []):
        score += 50
        reasons.append(f"Handles {CASE_TYPE_LABELS.get(case['case_type'], case['case_type'])} cases")
    else:
        reasons.append("Not a listed practice area")

    case_state = (case.get("state") or "").upper().strip()
    lawyer_states = [s.upper().strip() for s in lawyer.get("states", [])]
    if case_state and case_state in lawyer_states:
        score += 30
        reasons.append(f"Licensed in {US_STATE_LABELS.get(case_state, case_state)}")
    elif case_state:
        reasons.append(f"Not licensed in {US_STATE_LABELS.get(case_state, case_state)}")

    if case.get("value_tier") and case["value_tier"] in lawyer.get("value_tiers", []):
        score += 15
        reasons.append(f"Takes {case['value_tier']}-tier cases")

    cap = lawyer.get("capacity") or {}
    cur, mx = cap.get("current", 0), cap.get("max", 0) or 1
    pct = cur / mx
    if pct < 0.8:
        score += 5
        reasons.append(f"Has capacity ({cur}/{mx} active)")
    else:
        reasons.append(f"Near capacity ({cur}/{mx} active)")

    return score, reasons


def rank_lawyers(case, lawyers, top_n=None):
    scored = []
    for l in lawyers:
        s, r = score_lawyer(case, l)
        scored.append({"lawyer": l, "score": s, "reasons": r})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored if top_n is None else scored[:top_n]
