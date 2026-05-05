import os
from datetime import datetime, timedelta, timezone
from collections import Counter

from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from authlib.integrations.flask_client import OAuth

import store
import matching
import agent
from auth import login_required, current_user, google_configured
from constants import (
    CASE_TYPES,
    CASE_TYPES_BY_PRACTICE,
    PRACTICE_AREAS,
    PRACTICE_AREA_LABELS,
    CASE_TYPE_TO_PRACTICE,
    VALUE_TIERS,
    STATUSES,
    CASE_TYPE_LABELS,
    VALUE_TIER_LABELS,
    STATUS_LABELS,
    STATUS_STYLES,
    US_STATES,
    US_STATE_LABELS,
    US_STATE_CODES,
    US_CITIES,
    INTAKE_STRENGTH,
    INTAKE_STRENGTH_LABELS,
    INTAKE_STRENGTH_STYLES,
    INTAKE_SIGNAL_GROUPS,
    INTAKE_SIGNAL_GROUPS_BY_TYPE,
    INTAKE_SIGNAL_LABELS,
    UNIVERSAL_INTAKE_GROUPS,
    signal_groups_for,
    REFERRAL_REASONS,
    REFERRAL_REASON_LABELS,
    DECLINE_REASONS,
    DECLINE_REASON_LABELS,
    OUTCOMES,
    OUTCOME_LABELS,
    OUTCOME_STYLES,
    OUTCOMES_WITH_RECOVERY,
)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-not-for-prod")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.context_processor
def inject_user():
    return {
        "current_user": current_user(),
        "google_configured": google_configured(),
        "agent_configured": agent.is_configured(),
        "branding": store.get_branding(),
    }


@app.context_processor
def inject_globals():
    return {
        "CASE_TYPES": CASE_TYPES,
        "CASE_TYPES_BY_PRACTICE": CASE_TYPES_BY_PRACTICE,
        "PRACTICE_AREAS": PRACTICE_AREAS,
        "PRACTICE_AREA_LABELS": PRACTICE_AREA_LABELS,
        "CASE_TYPE_TO_PRACTICE": CASE_TYPE_TO_PRACTICE,
        "VALUE_TIERS": VALUE_TIERS,
        "STATUSES": STATUSES,
        "CASE_TYPE_LABELS": CASE_TYPE_LABELS,
        "VALUE_TIER_LABELS": VALUE_TIER_LABELS,
        "STATUS_LABELS": STATUS_LABELS,
        "STATUS_STYLES": STATUS_STYLES,
        "US_STATES": US_STATES,
        "US_STATE_LABELS": US_STATE_LABELS,
        "US_CITIES": US_CITIES,
        "INTAKE_STRENGTH": INTAKE_STRENGTH,
        "INTAKE_STRENGTH_LABELS": INTAKE_STRENGTH_LABELS,
        "INTAKE_STRENGTH_STYLES": INTAKE_STRENGTH_STYLES,
        "INTAKE_SIGNAL_GROUPS": INTAKE_SIGNAL_GROUPS,
        "INTAKE_SIGNAL_GROUPS_BY_TYPE": INTAKE_SIGNAL_GROUPS_BY_TYPE,
        "UNIVERSAL_INTAKE_GROUPS": UNIVERSAL_INTAKE_GROUPS,
        "INTAKE_SIGNAL_LABELS": INTAKE_SIGNAL_LABELS,
        "signal_groups_for": signal_groups_for,
        "REFERRAL_REASONS": REFERRAL_REASONS,
        "REFERRAL_REASON_LABELS": REFERRAL_REASON_LABELS,
        "DECLINE_REASONS": DECLINE_REASONS,
        "DECLINE_REASON_LABELS": DECLINE_REASON_LABELS,
        "OUTCOMES": OUTCOMES,
        "OUTCOME_LABELS": OUTCOME_LABELS,
        "OUTCOME_STYLES": OUTCOME_STYLES,
        "OUTCOMES_WITH_RECOVERY": OUTCOMES_WITH_RECOVERY,
    }


def jurisdiction_str(case):
    parts = [p for p in [case.get("city"), case.get("state")] if p]
    return ", ".join(parts) if parts else ""


# ---------- Auth ----------

@app.route("/login")
def login_page():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return render_template("login.html", next_url=request.args.get("next") or url_for("dashboard"))


@app.route("/auth/google")
def auth_google():
    if not google_configured():
        flash("Google OAuth isn't configured yet. Use the demo login.", "error")
        return redirect(url_for("login_page"))
    redirect_uri = url_for("auth_google_callback", _external=True)
    session["next_url"] = request.args.get("next") or url_for("dashboard")
    return oauth.google.authorize_redirect(redirect_uri)


@app.route("/auth/google/callback")
def auth_google_callback():
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        flash(f"Google sign-in failed: {e}", "error")
        return redirect(url_for("login_page"))
    info = token.get("userinfo") or {}
    session["user"] = {
        "id": info.get("sub"),
        "name": info.get("name") or info.get("email", "Signed-in user"),
        "email": info.get("email"),
        "picture": info.get("picture"),
        "source": "google",
    }
    flash(f"Signed in as {session['user']['name']}.", "success")
    return redirect(session.pop("next_url", url_for("dashboard")))


@app.route("/auth/demo", methods=["POST"])
def auth_demo():
    session["user"] = {
        "id": "demo_001",
        "name": "Travis Demo",
        "email": "demo@example.com",
        "picture": None,
        "source": "demo",
    }
    flash("Signed in to the demo workspace.", "success")
    return redirect(request.form.get("next") or url_for("dashboard"))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# ---------- Dashboard ----------

@app.route("/")
@login_required
def dashboard():
    cases = store.get_cases()
    lawyers = store.get_lawyers()

    needs_review = [c for c in cases if c["status"] in ("needs_review", "ready_to_refer")]
    referred = [c for c in cases if c["status"] in ("referred", "accepted")]

    pipeline_order = ["needs_review", "ready_to_refer", "referred", "accepted", "declined", "closed"]
    pipeline_counts = Counter(c["status"] for c in cases)
    pipeline = [
        {"key": k, "label": STATUS_LABELS.get(k, k), "count": pipeline_counts.get(k, 0)}
        for k in pipeline_order
    ]

    today = datetime.now(timezone.utc).date()
    spark_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    by_day_created = Counter()
    by_day_referred = Counter()
    for c in cases:
        try:
            d = datetime.fromisoformat(c["created_at"].rstrip("Z")).date()
            by_day_created[d] += 1
        except Exception:
            pass
        if c.get("status") in ("referred", "accepted"):
            try:
                d = datetime.fromisoformat(c["updated_at"].rstrip("Z")).date()
                by_day_referred[d] += 1
            except Exception:
                pass
    spark_cases = [by_day_created.get(d, 0) for d in spark_days]
    spark_referred = [by_day_referred.get(d, 0) for d in spark_days]

    attention = sorted(
        [c for c in cases if c["status"] in ("needs_review", "ready_to_refer")],
        key=lambda c: c["created_at"],
    )[:5]

    network = []
    for l in lawyers:
        cap = l.get("capacity") or {"current": 0, "max": 0}
        cur, mx = cap.get("current", 0), cap.get("max", 0) or 1
        pct = round(min(100, (cur / mx) * 100))
        network.append({"lawyer": l, "current": cur, "max": mx, "pct": pct})
    network.sort(key=lambda x: x["pct"], reverse=True)

    activity = sorted(
        [c for c in cases if c.get("assigned_lawyer_id") or c.get("previously_referred_to")],
        key=lambda c: c["updated_at"],
        reverse=True,
    )[:6]
    lawyers_by_id = {l["id"]: l for l in lawyers}

    closed_cases = [c for c in cases if c["status"] == "closed"]
    total_recovery = sum((c.get("outcome_amount") or 0) for c in closed_cases)
    total_fees = sum((c.get("referral_fee_collected") or 0) for c in closed_cases)
    active_count = sum(1 for c in cases if c["status"] == "accepted")
    awaiting_count = sum(1 for c in cases if c["status"] == "referred")

    hour = datetime.now().hour
    greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 18 else "Good evening")

    return render_template(
        "dashboard.html",
        total_cases=len(cases),
        needs_review_count=len(needs_review),
        referred_count=len(referred),
        lawyers_count=len(lawyers),
        pipeline=pipeline,
        spark_cases=spark_cases,
        spark_referred=spark_referred,
        attention=attention,
        network=network,
        activity=activity,
        lawyers_by_id=lawyers_by_id,
        greeting=greeting,
        today_str=datetime.now().strftime("%A, %B %-d"),
        jurisdiction_str=jurisdiction_str,
        total_recovery=total_recovery,
        total_fees=total_fees,
        active_count=active_count,
        awaiting_count=awaiting_count,
        closed_count=len(closed_cases),
    )


# ---------- Cases ----------

@app.route("/cases")
@login_required
def cases_list():
    cases = sorted(store.get_cases(), key=lambda c: c["created_at"], reverse=True)
    lawyers_by_id = {l["id"]: l for l in store.get_lawyers()}
    return render_template(
        "cases/list.html",
        cases=cases,
        lawyers_by_id=lawyers_by_id,
        jurisdiction_str=jurisdiction_str,
    )


@app.route("/cases/new", methods=["GET", "POST"])
@login_required
def cases_new():
    if request.method == "POST":
        state = (request.form.get("state") or "").upper().strip()
        if state and state not in US_STATE_CODES:
            flash("Pick a valid US state.", "error")
            return render_template("cases/new.html", form=request.form), 400

        case = {
            "id": store.new_id("c"),
            "name": request.form.get("name", "").strip(),
            "property_address": request.form.get("property_address", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "comments": request.form.get("comments", "").strip(),
            "case_type": request.form.get("case_type") or "other",
            "value_tier": request.form.get("value_tier") or "medium",
            "city": request.form.get("city", "").strip(),
            "state": state,
            "intake_strength": request.form.get("intake_strength") or None,
            "intake_signals": request.form.getlist("intake_signals"),
            "status": "needs_review",
            "assigned_lawyer_id": None,
            "referral_reasons": [],
            "referral_notes": None,
            "referral_was_override": None,
            "referral_suggested_lawyer_id": None,
            "created_at": store.now(),
            "updated_at": store.now(),
        }
        if not case["name"]:
            flash("Name is required.", "error")
            return render_template("cases/new.html", form=request.form), 400
        store.upsert_case(case)
        flash("Case created.", "success")
        return redirect(url_for("cases_detail", case_id=case["id"]))
    return render_template("cases/new.html", form={})


@app.route("/cases/<case_id>")
@login_required
def cases_detail(case_id):
    case = store.get_case(case_id)
    if not case:
        abort(404)
    lawyers = store.get_lawyers()
    ranked = matching.rank_lawyers(case, lawyers)
    assigned = store.get_lawyer(case["assigned_lawyer_id"]) if case.get("assigned_lawyer_id") else None
    return render_template(
        "cases/detail.html",
        case=case,
        ranked=ranked,
        lawyers=lawyers,
        assigned=assigned,
        jurisdiction_str=jurisdiction_str,
    )


@app.route("/cases/<case_id>/assign", methods=["POST"])
@login_required
def cases_assign(case_id):
    case = store.get_case(case_id)
    if not case:
        abort(404)
    lawyer_id = request.form.get("lawyer_id")
    notes = request.form.get("notes", "").strip()
    reasons = request.form.getlist("referral_reasons")

    if not lawyer_id:
        flash("Pick a lawyer.", "error")
        return redirect(url_for("cases_detail", case_id=case_id))
    if not reasons:
        flash("Pick at least one reason — this is the training signal.", "error")
        return redirect(url_for("cases_detail", case_id=case_id))

    lawyer = store.get_lawyer(lawyer_id)
    if not lawyer:
        abort(404)

    ranked = matching.rank_lawyers(case, store.get_lawyers(), top_n=1)
    suggested_id = ranked[0]["lawyer"]["id"] if ranked else None
    was_override = bool(suggested_id and suggested_id != lawyer_id)

    case["assigned_lawyer_id"] = lawyer_id
    case["referral_reasons"] = reasons
    case["referral_notes"] = notes or None
    case["referral_was_override"] = was_override
    case["referral_suggested_lawyer_id"] = suggested_id
    case["referral_fee_at_referral"] = lawyer.get("referral_fee") or ""
    case["referred_at"] = store.now()
    case["lawyer_response"] = None
    case["status"] = "referred"
    case["updated_at"] = store.now()
    store.upsert_case(case)

    cap = lawyer.get("capacity") or {"current": 0, "max": 50}
    cap["current"] = cap.get("current", 0) + 1
    lawyer["capacity"] = cap
    stats = lawyer.get("stats") or {"referred": 0, "accepted": 0, "declined": 0}
    stats["referred"] = stats.get("referred", 0) + 1
    lawyer["stats"] = stats
    store.upsert_lawyer(lawyer)

    flash(f"Referred to {lawyer['name']}.", "success")
    return redirect(url_for("cases_detail", case_id=case_id))


@app.route("/cases/<case_id>/respond", methods=["POST"])
@login_required
def cases_respond(case_id):
    """The lawyer (in real life via email/portal) accepted or declined.
    The referrer marks the response here, capturing decline reasons as training data."""
    case = store.get_case(case_id)
    if not case:
        abort(404)
    if case["status"] != "referred" or not case.get("assigned_lawyer_id"):
        flash("This case isn't awaiting a response.", "error")
        return redirect(url_for("cases_detail", case_id=case_id))

    response = request.form.get("response")
    if response not in ("accepted", "declined"):
        abort(400)

    lawyer = store.get_lawyer(case["assigned_lawyer_id"])
    if not lawyer:
        abort(404)
    cap = lawyer.get("capacity") or {"current": 0, "max": 50}
    stats = lawyer.get("stats") or {"referred": 0, "accepted": 0, "declined": 0}

    if response == "accepted":
        case["lawyer_response"] = "accepted"
        case["lawyer_responded_at"] = store.now()
        case["status"] = "accepted"
        stats["accepted"] = stats.get("accepted", 0) + 1
    else:
        decline_codes = request.form.getlist("decline_reason_codes")
        decline_notes = request.form.get("decline_notes", "").strip()
        if not decline_codes:
            flash("Pick at least one decline reason — that's the training signal.", "error")
            return redirect(url_for("cases_detail", case_id=case_id))

        history = case.get("previously_referred_to") or []
        history.append({
            "lawyer_id": lawyer["id"],
            "lawyer_name": lawyer["name"],
            "decline_reasons": decline_codes,
            "decline_notes": decline_notes or None,
            "referral_reasons": case.get("referral_reasons") or [],
            "referral_notes": case.get("referral_notes"),
            "referred_at": case.get("referred_at"),
            "declined_at": store.now(),
        })

        case["previously_referred_to"] = history
        case["lawyer_response"] = "declined"
        case["lawyer_responded_at"] = store.now()
        case["assigned_lawyer_id"] = None
        case["referral_reasons"] = []
        case["referral_notes"] = None
        case["referral_was_override"] = None
        case["referral_suggested_lawyer_id"] = None
        case["referred_at"] = None
        case["status"] = "needs_review"

        cap["current"] = max(0, cap.get("current", 0) - 1)
        stats["declined"] = stats.get("declined", 0) + 1

    case["updated_at"] = store.now()
    store.upsert_case(case)
    lawyer["capacity"] = cap
    lawyer["stats"] = stats
    store.upsert_lawyer(lawyer)

    flash("Marked accepted." if response == "accepted" else f"{lawyer['name']} declined — back in the pipeline.", "success")
    return redirect(url_for("cases_detail", case_id=case_id))


@app.route("/cases/<case_id>/outcome", methods=["POST"])
@login_required
def cases_outcome(case_id):
    """Record the eventual outcome of an accepted case. Closes the case and
    calculates the referral fee owed to the user."""
    case = store.get_case(case_id)
    if not case:
        abort(404)
    if case["status"] not in ("accepted", "closed"):
        flash("Outcome can only be set on accepted cases.", "error")
        return redirect(url_for("cases_detail", case_id=case_id))

    outcome = request.form.get("outcome")
    if outcome not in dict(OUTCOMES):
        abort(400)
    amount_raw = request.form.get("outcome_amount", "").replace(",", "").replace("$", "").strip()
    try:
        amount = float(amount_raw) if amount_raw else 0.0
    except ValueError:
        amount = 0.0
    notes = request.form.get("outcome_notes", "").strip()

    fee_pct_str = (case.get("referral_fee_at_referral") or "").replace("%", "").strip()
    try:
        fee_pct = float(fee_pct_str)
    except ValueError:
        fee_pct = 0.0
    fee_collected = round(amount * fee_pct / 100, 2) if outcome in OUTCOMES_WITH_RECOVERY else 0.0

    case["outcome"] = outcome
    case["outcome_amount"] = amount
    case["outcome_notes"] = notes or None
    case["outcome_at"] = store.now()
    case["referral_fee_collected"] = fee_collected
    case["status"] = "closed"
    case["updated_at"] = store.now()
    store.upsert_case(case)

    if case.get("assigned_lawyer_id"):
        lawyer = store.get_lawyer(case["assigned_lawyer_id"])
        if lawyer:
            cap = lawyer.get("capacity") or {"current": 0, "max": 50}
            cap["current"] = max(0, cap.get("current", 0) - 1)
            lawyer["capacity"] = cap
            store.upsert_lawyer(lawyer)

    flash(f"Outcome recorded: {OUTCOME_LABELS.get(outcome, outcome)}.", "success")
    return redirect(url_for("cases_detail", case_id=case_id))


@app.route("/cases/<case_id>/agent", methods=["GET"])
@login_required
def cases_agent_suggestion(case_id):
    """Async endpoint: returns the LLM agent's recommendation as JSON.
    The case detail page fetches this after initial render so the page isn't
    blocked on a 2-5 second LLM call."""
    case = store.get_case(case_id)
    if not case:
        abort(404)
    if not agent.is_configured():
        return jsonify({"configured": False})
    suggestion = agent.suggest(case, store.get_lawyers(), store.get_cases())
    if suggestion is None:
        return jsonify({"configured": False})
    suggestion["configured"] = True
    lawyers_by_id = {l["id"]: l for l in store.get_lawyers()}
    rec = lawyers_by_id.get(suggestion.get("recommended_lawyer_id"))
    if rec:
        suggestion["recommended_lawyer"] = {"id": rec["id"], "name": rec["name"], "firm": rec.get("firm", "")}
    for alt in suggestion.get("alternatives") or []:
        lw = lawyers_by_id.get(alt.get("lawyer_id"))
        if lw:
            alt["lawyer_name"] = lw["name"]
            alt["firm"] = lw.get("firm", "")
    return jsonify(suggestion)


@app.route("/cases/<case_id>/delete", methods=["POST"])
@login_required
def cases_delete(case_id):
    store.delete_case(case_id)
    flash("Case deleted.", "success")
    return redirect(url_for("cases_list"))


# ---------- Lawyers ----------

@app.route("/lawyers")
@login_required
def lawyers_list():
    lawyers = store.get_lawyers()
    return render_template("lawyers/list.html", lawyers=lawyers)


@app.route("/lawyers/new", methods=["GET", "POST"])
@login_required
def lawyers_new():
    if request.method == "POST":
        states = [s.strip().upper() for s in request.form.get("states", "").split(",") if s.strip()]
        states = [s for s in states if s in US_STATE_CODES]
        lawyer = {
            "id": store.new_id("l"),
            "name": request.form.get("name", "").strip(),
            "firm": request.form.get("firm", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "practice_areas": request.form.getlist("practice_areas"),
            "states": states,
            "value_tiers": request.form.getlist("value_tiers"),
            "referral_fee": request.form.get("referral_fee", "").strip(),
            "capacity": {
                "current": int(request.form.get("capacity_current") or 0),
                "max": int(request.form.get("capacity_max") or 50),
            },
            "preferences": request.form.get("preferences", "").strip(),
            "stats": {"referred": 0, "accepted": 0, "declined": 0},
            "created_at": store.now(),
        }
        if not lawyer["name"]:
            flash("Name is required.", "error")
            return render_template("lawyers/new.html", form=request.form), 400
        store.upsert_lawyer(lawyer)
        flash("Lawyer added.", "success")
        return redirect(url_for("lawyers_detail", lawyer_id=lawyer["id"]))
    return render_template("lawyers/new.html", form={})


@app.route("/lawyers/<lawyer_id>")
@login_required
def lawyers_detail(lawyer_id):
    lawyer = store.get_lawyer(lawyer_id)
    if not lawyer:
        abort(404)
    all_cases = store.get_cases()
    referred_cases = [c for c in all_cases if c.get("assigned_lawyer_id") == lawyer_id]

    past_declines = []
    for c in all_cases:
        for prev in c.get("previously_referred_to") or []:
            if prev.get("lawyer_id") == lawyer_id:
                past_declines.append({
                    "case_id": c["id"],
                    "case_name": c["name"],
                    "case_type": c.get("case_type"),
                    "value_tier": c.get("value_tier"),
                    "decline_reasons": prev.get("decline_reasons") or [],
                    "decline_notes": prev.get("decline_notes"),
                    "declined_at": prev.get("declined_at"),
                })
    past_declines.sort(key=lambda d: d.get("declined_at") or "", reverse=True)

    return render_template(
        "lawyers/detail.html",
        lawyer=lawyer,
        referred_cases=referred_cases,
        past_declines=past_declines,
        jurisdiction_str=jurisdiction_str,
    )


@app.route("/lawyers/<lawyer_id>/delete", methods=["POST"])
@login_required
def lawyers_delete(lawyer_id):
    store.delete_lawyer(lawyer_id)
    flash("Lawyer removed.", "success")
    return redirect(url_for("lawyers_list"))


# ---------- Settings (firm info + logo, white-label) ----------

import base64

ALLOWED_LOGO_MIMETYPES = {"image/png", "image/jpeg", "image/svg+xml", "image/webp"}
MAX_LOGO_BYTES = 2 * 1024 * 1024  # 2 MB


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        action = request.form.get("action", "save_firm")

        if action == "save_firm":
            store.save_branding({
                "firm_name": request.form.get("firm_name", "").strip(),
                "tagline": request.form.get("tagline", "").strip(),
                "address": request.form.get("address", "").strip(),
                "phone": request.form.get("phone", "").strip(),
                "email": request.form.get("email", "").strip(),
                "website": request.form.get("website", "").strip(),
            })
            flash("Firm info saved.", "success")
            return redirect(url_for("settings"))

        if action == "save_logo":
            f = request.files.get("logo")
            if not f or not f.filename:
                flash("Pick a logo file to upload.", "error")
                return redirect(url_for("settings"))
            if f.mimetype not in ALLOWED_LOGO_MIMETYPES:
                flash("Logo must be PNG, JPG, SVG, or WEBP.", "error")
                return redirect(url_for("settings"))
            data = f.read()
            if len(data) > MAX_LOGO_BYTES:
                flash("Logo file is too large (max 2 MB).", "error")
                return redirect(url_for("settings"))
            b64 = base64.b64encode(data).decode("ascii")
            data_url = f"data:{f.mimetype};base64,{b64}"
            store.save_branding({"logo_data_url": data_url})
            flash("Logo uploaded.", "success")
            return redirect(url_for("settings"))

        if action == "remove_logo":
            store.save_branding({"logo_data_url": ""})
            flash("Logo removed.", "success")
            return redirect(url_for("settings"))

        flash("Unknown action.", "error")
        return redirect(url_for("settings"))

    return render_template("settings.html", branding=store.get_branding())


if __name__ == "__main__":
    app.run(debug=True, port=5050)
