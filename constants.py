CASE_TYPES = [
    ("personal_injury", "Personal Injury"),
    ("auto_accident", "Auto Accident"),
    ("premises_liability", "Premises Liability"),
    ("medical_malpractice", "Medical Malpractice"),
    ("workers_comp", "Workers' Compensation"),
    ("product_liability", "Product Liability"),
    ("property_damage", "Property Damage"),
    ("wrongful_death", "Wrongful Death"),
    ("other", "Other"),
]

VALUE_TIERS = [
    ("low", "Low (< $25k)"),
    ("medium", "Medium ($25k–$250k)"),
    ("high", "High ($250k–$1M)"),
    ("major", "Major (> $1M)"),
]

STATUSES = [
    ("needs_review", "Needs Review"),
    ("ready_to_refer", "Ready to Refer"),
    ("referred", "Referred"),
    ("accepted", "Accepted"),
    ("declined", "Declined"),
    ("closed", "Closed"),
]

CASE_TYPE_LABELS = dict(CASE_TYPES)
VALUE_TIER_LABELS = dict(VALUE_TIERS)
STATUS_LABELS = dict(STATUSES)

STATUS_STYLES = {
    "needs_review": "bg-amber-100 text-amber-800",
    "ready_to_refer": "bg-sky-100 text-sky-800",
    "referred": "bg-emerald-100 text-emerald-800",
    "accepted": "bg-emerald-200 text-emerald-900",
    "declined": "bg-rose-100 text-rose-800",
    "closed": "bg-slate-200 text-slate-700",
}

# ---------- Geography ----------

US_STATES = [
    ("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"),
    ("CA", "California"), ("CO", "Colorado"), ("CT", "Connecticut"), ("DE", "Delaware"),
    ("DC", "District of Columbia"), ("FL", "Florida"), ("GA", "Georgia"), ("HI", "Hawaii"),
    ("ID", "Idaho"), ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"),
    ("KS", "Kansas"), ("KY", "Kentucky"), ("LA", "Louisiana"), ("ME", "Maine"),
    ("MD", "Maryland"), ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"),
    ("MS", "Mississippi"), ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"),
    ("NV", "Nevada"), ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"),
    ("NY", "New York"), ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"),
    ("OK", "Oklahoma"), ("OR", "Oregon"), ("PA", "Pennsylvania"), ("RI", "Rhode Island"),
    ("SC", "South Carolina"), ("SD", "South Dakota"), ("TN", "Tennessee"), ("TX", "Texas"),
    ("UT", "Utah"), ("VT", "Vermont"), ("VA", "Virginia"), ("WA", "Washington"),
    ("WV", "West Virginia"), ("WI", "Wisconsin"), ("WY", "Wyoming"),
]
US_STATE_LABELS = dict(US_STATES)
US_STATE_CODES = [c for c, _ in US_STATES]

# Curated city list for the datalist autocomplete. Users can type any city;
# this is just suggestions. Format: "City, ST".
US_CITIES = [
    "Birmingham, AL", "Mobile, AL", "Anchorage, AK", "Phoenix, AZ", "Tucson, AZ", "Mesa, AZ",
    "Little Rock, AR", "Los Angeles, CA", "San Diego, CA", "San Jose, CA", "San Francisco, CA",
    "Fresno, CA", "Sacramento, CA", "Long Beach, CA", "Oakland, CA", "Bakersfield, CA",
    "Anaheim, CA", "Santa Ana, CA", "Riverside, CA", "Stockton, CA", "Irvine, CA",
    "Livermore, CA", "Pleasanton, CA", "Fremont, CA",
    "Denver, CO", "Colorado Springs, CO", "Aurora, CO", "Boulder, CO",
    "Bridgeport, CT", "New Haven, CT", "Hartford, CT",
    "Wilmington, DE", "Washington, DC",
    "Jacksonville, FL", "Miami, FL", "Tampa, FL", "Orlando, FL", "St. Petersburg, FL",
    "Hialeah, FL", "Fort Lauderdale, FL", "Tallahassee, FL",
    "Atlanta, GA", "Augusta, GA", "Columbus, GA", "Savannah, GA",
    "Honolulu, HI", "Boise, ID", "Chicago, IL", "Aurora, IL", "Naperville, IL", "Springfield, IL",
    "Indianapolis, IN", "Fort Wayne, IN", "Evansville, IN",
    "Des Moines, IA", "Cedar Rapids, IA",
    "Wichita, KS", "Overland Park, KS", "Kansas City, KS",
    "Louisville, KY", "Lexington, KY",
    "New Orleans, LA", "Baton Rouge, LA", "Shreveport, LA",
    "Portland, ME", "Baltimore, MD", "Annapolis, MD",
    "Boston, MA", "Worcester, MA", "Cambridge, MA",
    "Detroit, MI", "Grand Rapids, MI", "Ann Arbor, MI",
    "Minneapolis, MN", "St. Paul, MN", "Rochester, MN",
    "Jackson, MS",
    "Kansas City, MO", "St. Louis, MO", "Springfield, MO",
    "Billings, MT", "Omaha, NE", "Lincoln, NE",
    "Las Vegas, NV", "Henderson, NV", "Reno, NV",
    "Manchester, NH", "Newark, NJ", "Jersey City, NJ", "Paterson, NJ",
    "Albuquerque, NM", "Santa Fe, NM",
    "New York, NY", "Buffalo, NY", "Rochester, NY", "Yonkers, NY", "Albany, NY",
    "Charlotte, NC", "Raleigh, NC", "Greensboro, NC", "Durham, NC",
    "Fargo, ND",
    "Columbus, OH", "Cleveland, OH", "Cincinnati, OH", "Toledo, OH", "Akron, OH",
    "Oklahoma City, OK", "Tulsa, OK",
    "Portland, OR", "Eugene, OR", "Salem, OR",
    "Philadelphia, PA", "Pittsburgh, PA", "Allentown, PA",
    "Providence, RI",
    "Charleston, SC", "Columbia, SC",
    "Sioux Falls, SD",
    "Nashville, TN", "Memphis, TN", "Knoxville, TN", "Chattanooga, TN",
    "Houston, TX", "San Antonio, TX", "Dallas, TX", "Austin, TX", "Fort Worth, TX",
    "El Paso, TX", "Arlington, TX", "Corpus Christi, TX", "Plano, TX", "Lubbock, TX",
    "Galveston, TX", "Sugar Land, TX", "The Woodlands, TX",
    "Salt Lake City, UT", "Provo, UT",
    "Burlington, VT",
    "Virginia Beach, VA", "Norfolk, VA", "Richmond, VA", "Arlington, VA",
    "Seattle, WA", "Spokane, WA", "Tacoma, WA", "Bellevue, WA",
    "Charleston, WV", "Milwaukee, WI", "Madison, WI", "Green Bay, WI",
    "Cheyenne, WY",
]

# ---------- Decision capture: intake signals ----------

INTAKE_STRENGTH = [
    ("strong", "Strong", "Clear liability, real damages"),
    ("moderate", "Moderate", "Workable; some issues"),
    ("weak", "Weak", "Soft tissue / minor / liability problems"),
    ("insufficient_info", "Need more info", "Follow up before referring"),
]
INTAKE_STRENGTH_LABELS = {c: l for c, l, _ in INTAKE_STRENGTH}
INTAKE_STRENGTH_STYLES = {
    "strong": "bg-emerald-100 text-emerald-800",
    "moderate": "bg-sky-100 text-sky-800",
    "weak": "bg-amber-100 text-amber-800",
    "insufficient_info": "bg-slate-100 text-slate-700",
}

INTAKE_SIGNAL_GROUPS = [
    ("Severity", [
        ("hospitalized", "Hospitalized"),
        ("surgery_likely", "Surgery likely"),
        ("ongoing_treatment", "Ongoing treatment"),
        ("minor_injury", "Minor injury"),
    ]),
    ("Liability & damages", [
        ("clear_liability", "Clear liability"),
        ("liability_disputed", "Liability disputed"),
        ("documented_losses", "Documented losses"),
        ("catastrophic", "Catastrophic"),
        ("soft_tissue_only", "Soft tissue only"),
    ]),
    ("Defendant", [
        ("corporate_defendant", "Corporate defendant"),
        ("individual_defendant", "Individual defendant"),
        ("govt_entity", "Government entity"),
        ("insurance_dispute", "Insurance dispute"),
    ]),
    ("Documentation", [
        ("records_complete", "Records complete"),
        ("records_partial", "Records partial"),
        ("witnesses", "Witnesses available"),
        ("police_report", "Police report"),
    ]),
    ("Context", [
        ("sol_urgent", "SOL approaching"),
        ("prior_counsel", "Had prior counsel"),
        ("non_english", "Non-English speaker"),
        ("repeat_client", "Repeat client"),
    ]),
]
INTAKE_SIGNAL_LABELS = {
    code: label
    for _, items in INTAKE_SIGNAL_GROUPS for code, label in items
}

# ---------- Decision capture: referral reasons ----------

REFERRAL_REASONS = [
    ("specialty_match", "Specialty match"),
    ("jurisdiction_match", "Jurisdiction match"),
    ("value_tier_match", "Value tier fit"),
    ("capacity_available", "Has capacity"),
    ("prior_success", "Past wins on similar"),
    ("relationship", "Strong relationship"),
    ("records_ready", "Records meet their bar"),
    ("fee_structure", "Fee structure works"),
    ("volume_practice", "Volume practice fit"),
    ("last_resort", "Last resort / others passed"),
    ("corporate_litigator", "Strong vs corporate"),
    ("specific_expertise", "Specific expertise"),
]
REFERRAL_REASON_LABELS = dict(REFERRAL_REASONS)

# ---------- Decline reasons (lawyer rejected the referral) ----------

DECLINE_REASONS = [
    ("case_too_weak", "Case too weak"),
    ("below_value_threshold", "Below their value threshold"),
    ("outside_jurisdiction", "Outside jurisdiction"),
    ("outside_specialty", "Outside their specialty"),
    ("at_capacity", "At capacity"),
    ("conflict_of_interest", "Conflict of interest"),
    ("client_already_repped", "Client already represented"),
    ("missing_records", "Records insufficient"),
    ("sol_expired", "Statute of limitations issue"),
    ("client_unresponsive", "Client unresponsive to lawyer"),
    ("fee_dispute", "Fee structure didn't work"),
    ("no_response", "No response (treated as decline)"),
    ("other", "Other"),
]
DECLINE_REASON_LABELS = dict(DECLINE_REASONS)

# ---------- Outcomes (after acceptance) ----------

OUTCOMES = [
    ("settled", "Settled"),
    ("won_trial", "Won at trial"),
    ("lost_trial", "Lost at trial"),
    ("dropped", "Client dropped"),
    ("withdrawn", "Withdrawn"),
    ("no_recovery", "No recovery"),
]
OUTCOME_LABELS = dict(OUTCOMES)
OUTCOME_STYLES = {
    "settled": "bg-emerald-100 text-emerald-800",
    "won_trial": "bg-emerald-200 text-emerald-900",
    "lost_trial": "bg-rose-100 text-rose-800",
    "dropped": "bg-slate-100 text-slate-700",
    "withdrawn": "bg-slate-100 text-slate-700",
    "no_recovery": "bg-rose-50 text-rose-700",
}
OUTCOMES_WITH_RECOVERY = {"settled", "won_trial"}
