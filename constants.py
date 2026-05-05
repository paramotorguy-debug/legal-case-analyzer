# ============================================================================
# Case classification: practice areas + case types
# ============================================================================

# Practice areas group case types in the dropdown. Each case_type belongs to
# exactly one practice area. Lawyers can list multiple practice areas in their
# profile and accept multiple case types within each.
PRACTICE_AREAS = [
    ("personal_injury_group", "Personal Injury"),
    ("tenant_law", "Landlord–Tenant"),
    ("family_law", "Family Law"),
    ("employment", "Employment"),
    ("civil_rights", "Civil Rights & Abuse"),
    ("criminal_defense", "Criminal Defense"),
    ("real_estate", "Real Estate & Property"),
    ("estate_probate", "Estate & Probate"),
    ("immigration", "Immigration"),
    ("other_practice", "Other"),
]
PRACTICE_AREA_LABELS = dict(PRACTICE_AREAS)

CASE_TYPES_BY_PRACTICE = {
    "personal_injury_group": [
        ("personal_injury", "Personal Injury (general)"),
        ("auto_accident", "Auto Accident"),
        ("premises_liability", "Premises Liability"),
        ("medical_malpractice", "Medical Malpractice"),
        ("workers_comp", "Workers' Compensation"),
        ("product_liability", "Product Liability"),
        ("wrongful_death", "Wrongful Death"),
        ("dog_bite", "Dog Bite / Animal Attack"),
    ],
    "tenant_law": [
        ("habitability", "Habitability / Repairs"),
        ("toxic_exposure", "Mold / Lead / Toxic Exposure"),
        ("illegal_lockout", "Illegal Lockout"),
        ("landlord_harassment", "Landlord Harassment"),
        ("eviction_defense", "Eviction Defense"),
        ("security_deposit", "Security Deposit Dispute"),
        ("wrongful_eviction", "Wrongful Eviction"),
        ("rent_control", "Rent Control / Rent Increase Dispute"),
    ],
    "family_law": [
        ("divorce", "Divorce"),
        ("child_custody", "Child Custody"),
        ("child_support", "Child Support"),
        ("domestic_violence_civil", "Domestic Violence / Restraining Order"),
        ("adoption", "Adoption"),
        ("prenup", "Prenup / Postnup"),
    ],
    "employment": [
        ("wrongful_termination", "Wrongful Termination"),
        ("discrimination", "Discrimination"),
        ("sexual_harassment", "Sexual Harassment"),
        ("wage_and_hour", "Wage & Hour"),
        ("retaliation", "Retaliation / Whistleblower"),
    ],
    "civil_rights": [
        ("sexual_abuse", "Sexual Abuse / Assault"),
        ("police_misconduct", "Police Misconduct"),
        ("institutional_abuse", "Institutional Abuse"),
    ],
    "criminal_defense": [
        ("dui", "DUI / DWI"),
        ("drug_charges", "Drug Charges"),
        ("assault_battery", "Assault / Battery"),
        ("white_collar", "White Collar"),
        ("theft_burglary", "Theft / Burglary"),
        ("juvenile", "Juvenile"),
    ],
    "real_estate": [
        ("boundary_dispute", "Boundary Dispute"),
        ("title_issues", "Title Issues"),
        ("construction_defect", "Construction Defect"),
        ("foreclosure_defense", "Foreclosure Defense"),
        ("hoa_dispute", "HOA Dispute"),
    ],
    "estate_probate": [
        ("will_contest", "Will Contest"),
        ("probate_administration", "Probate Administration"),
        ("trust_dispute", "Trust Dispute"),
        ("guardianship", "Guardianship"),
    ],
    "immigration": [
        ("deportation_defense", "Deportation Defense"),
        ("asylum", "Asylum"),
        ("visa_greencard", "Visa / Green Card"),
        ("naturalization", "Naturalization"),
    ],
    "other_practice": [
        ("other", "Other"),
    ],
}

# Flat list of all case types (for backward compat and label lookup)
CASE_TYPES = []
for _practice_code, _items in CASE_TYPES_BY_PRACTICE.items():
    CASE_TYPES.extend(_items)
CASE_TYPE_LABELS = dict(CASE_TYPES)

# Reverse lookup: case_type → practice_area
CASE_TYPE_TO_PRACTICE = {}
for _practice_code, _items in CASE_TYPES_BY_PRACTICE.items():
    for _code, _label in _items:
        CASE_TYPE_TO_PRACTICE[_code] = _practice_code

# ============================================================================
# Value tiers (specialty-neutral; lawyer interprets within their domain)
# ============================================================================

VALUE_TIERS = [
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
    ("major", "Major"),
]
VALUE_TIER_LABELS = dict(VALUE_TIERS)

# ============================================================================
# Pipeline statuses
# ============================================================================

STATUSES = [
    ("needs_review", "Needs Review"),
    ("ready_to_refer", "Ready to Refer"),
    ("referred", "Referred"),
    ("accepted", "Accepted"),
    ("declined", "Declined"),
    ("closed", "Closed"),
]
STATUS_LABELS = dict(STATUSES)
STATUS_STYLES = {
    "needs_review": "bg-amber-100 text-amber-800",
    "ready_to_refer": "bg-sky-100 text-sky-800",
    "referred": "bg-emerald-100 text-emerald-800",
    "accepted": "bg-emerald-200 text-emerald-900",
    "declined": "bg-rose-100 text-rose-800",
    "closed": "bg-slate-200 text-slate-700",
}

# ============================================================================
# Geography
# ============================================================================

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

# ============================================================================
# Intake assessment: case strength
# ============================================================================

INTAKE_STRENGTH = [
    ("strong", "Strong", "Clear merit, real damages, defensible"),
    ("moderate", "Moderate", "Workable; some issues"),
    ("weak", "Weak", "Significant problems on merits or damages"),
    ("insufficient_info", "Need more info", "Follow up before referring"),
]
INTAKE_STRENGTH_LABELS = {c: l for c, l, _ in INTAKE_STRENGTH}
INTAKE_STRENGTH_STYLES = {
    "strong": "bg-emerald-100 text-emerald-800",
    "moderate": "bg-sky-100 text-sky-800",
    "weak": "bg-amber-100 text-amber-800",
    "insufficient_info": "bg-slate-100 text-slate-700",
}

# ============================================================================
# Intake signals — per case-type taxonomies
# ============================================================================
#
# Architecture:
#   - INTAKE_SIGNAL_GROUPS_BY_TYPE: dict keyed by case_type, value is a list
#     of (group_name, [(code, label), ...]) tuples — these are the case-type-
#     specific signal categories (e.g., "Severity" for PI, "Living conditions"
#     for tenant law).
#   - UNIVERSAL_INTAKE_GROUPS: appended to every case type. Things every case
#     has: documentation status, timing, vulnerability, prior counsel, etc.
#
# When the new-case form renders, JavaScript shows the groups for the
# selected case_type plus the universal groups. All signal codes live in a
# single flat label dictionary so display elsewhere just works.
# ============================================================================

UNIVERSAL_INTAKE_GROUPS = [
    ("Documentation", [
        ("records_complete", "Records complete"),
        ("records_partial", "Records partial"),
        ("witnesses", "Witnesses available"),
        ("photos_video", "Photos / video"),
        ("written_communications", "Written communications"),
    ]),
    ("Timing & context", [
        ("sol_urgent", "Statute of limitations approaching"),
        ("court_date_set", "Court date set"),
        ("prior_counsel", "Had prior counsel"),
        ("repeat_client", "Repeat client"),
    ]),
    ("Client vulnerability", [
        ("non_english", "Non-English speaker"),
        ("elderly_or_disabled", "Elderly or disabled"),
        ("minor_involved", "Minor involved"),
        ("financial_hardship", "Financial hardship"),
        ("immigration_status_concern", "Immigration status concern"),
    ]),
]

# ---- Personal Injury family ----

_PI_SEVERITY = ("Severity", [
    ("hospitalized", "Hospitalized"),
    ("surgery_likely", "Surgery likely / completed"),
    ("ongoing_treatment", "Ongoing treatment"),
    ("catastrophic", "Catastrophic injury"),
    ("minor_injury", "Minor injury"),
    ("soft_tissue_only", "Soft tissue only"),
])
_PI_LIABILITY = ("Liability & damages", [
    ("clear_liability", "Clear liability"),
    ("liability_disputed", "Liability disputed"),
    ("documented_losses", "Documented losses"),
    ("comparative_fault", "Comparative fault concern"),
])
_PI_DEFENDANT = ("Defendant", [
    ("corporate_defendant", "Corporate defendant"),
    ("individual_defendant", "Individual defendant"),
    ("govt_entity", "Government entity"),
    ("insurance_dispute", "Insurance dispute"),
    ("uninsured_motorist", "Uninsured motorist"),
])

# ---- Tenant Law family ----

_TENANT_CONDITIONS = ("Living conditions", [
    ("no_heat_or_water", "No heat or water"),
    ("no_electricity", "No electricity"),
    ("vermin_infestation", "Vermin / pest infestation"),
    ("mold_visible", "Visible mold"),
    ("lead_paint_suspected", "Lead paint suspected"),
    ("asbestos_concern", "Asbestos concern"),
    ("structural_damage", "Structural damage"),
    ("plumbing_failure", "Plumbing failure / sewage backup"),
    ("displaced_unsafe", "Tenant displaced / uninhabitable"),
])
_TENANT_DOCS = ("Tenant-law documentation", [
    ("code_violations_issued", "Code violations issued"),
    ("government_citation_35_days", "Citation persisting 35+ days"),
    ("repair_requests_written", "Repair requests in writing"),
    ("repair_requests_verbal_only", "Repair requests verbal only"),
    ("written_lease", "Written lease"),
    ("oral_lease", "Oral lease only"),
    ("security_deposit_paid", "Security deposit paid"),
])
_TENANT_LANDLORD = ("Landlord behavior", [
    ("refused_repairs", "Refused repairs outright"),
    ("partial_repairs", "Partial / inadequate repairs"),
    ("retaliation_after_complaint", "Retaliation after complaint"),
    ("illegal_entry", "Illegal entry into unit"),
    ("verbal_threats", "Verbal threats / harassment"),
    ("utility_shutoff", "Utility shutoff"),
])
_TENANT_HEALTH = ("Health & household impact", [
    ("hospitalized", "Tenant hospitalized"),
    ("ongoing_treatment", "Ongoing medical treatment"),
    ("child_in_unit", "Child in the unit"),
    ("pregnant_tenant", "Pregnant tenant"),
])
_LOCKOUT = ("Lockout details", [
    ("locks_changed", "Locks changed"),
    ("belongings_inside", "Belongings still inside"),
    ("belongings_removed", "Belongings removed by landlord"),
    ("utilities_shut_off", "Utilities shut off"),
    ("no_court_order", "No court order"),
    ("still_locked_out", "Still locked out"),
    ("police_called", "Police called"),
])
_EVICTION = ("Eviction posture", [
    ("notice_served", "Notice served"),
    ("notice_defective", "Notice appears defective"),
    ("summons_received", "Summons received"),
    ("default_judgment_entered", "Default judgment already entered"),
    ("nonpayment_alleged", "Nonpayment alleged"),
    ("breach_of_lease_alleged", "Breach of lease alleged"),
    ("retaliation_suspected", "Retaliation suspected"),
    ("habitability_defense", "Habitability defense available"),
    ("court_date_within_7_days", "Court date within 7 days"),
])
_DEPOSIT = ("Security deposit specifics", [
    ("full_amount_withheld", "Full amount withheld"),
    ("partial_withheld", "Partial amount withheld"),
    ("no_itemization", "No itemization provided"),
    ("more_than_30_days_past", "More than 30 days past return deadline"),
    ("alleges_damage", "Landlord alleges damage"),
    ("dispute_pre_existing", "Dispute over pre-existing condition"),
])
_TOXIC = ("Toxic exposure", [
    ("confirmed_mold_test", "Confirmed mold test"),
    ("confirmed_lead_test", "Confirmed lead test"),
    ("asbestos_confirmed", "Asbestos confirmed"),
    ("lead_blood_test_elevated_child", "Elevated child blood-lead level"),
    ("respiratory_issues", "Respiratory symptoms"),
    ("neurological_symptoms", "Neurological symptoms"),
    ("ongoing_exposure", "Ongoing exposure"),
    ("prior_complaints_to_landlord", "Landlord had prior notice"),
])

# ---- Family Law family ----

_DIVORCE = ("Marriage & assets", [
    ("short_marriage_under_5", "Short marriage (<5 yrs)"),
    ("long_marriage_over_20", "Long marriage (>20 yrs)"),
    ("high_net_worth", "High net worth (>$500k)"),
    ("business_owned", "Business interest involved"),
    ("retirement_only", "Primarily retirement assets"),
    ("hidden_assets_suspected", "Hidden assets suspected"),
    ("debt_heavy", "Debt-heavy estate"),
])
_FAMILY_CHILDREN = ("Children & custody", [
    ("minor_children", "Minor children"),
    ("special_needs_child", "Special needs child"),
    ("custody_disputed", "Custody disputed"),
    ("custody_agreed", "Custody agreed"),
    ("relocation_planned", "Relocation planned"),
])
_FAMILY_CONFLICT = ("Conflict & safety", [
    ("high_conflict", "High conflict"),
    ("dv_present", "Domestic violence present"),
    ("substance_abuse_concern", "Substance abuse concern"),
    ("mental_health_concern", "Mental health concern"),
    ("uncontested", "Uncontested"),
])
_DV = ("Incident & threat", [
    ("physical_assault", "Physical assault"),
    ("threats_with_weapon", "Threats with weapon"),
    ("hospitalization_required", "Hospitalization required"),
    ("strangulation", "Choking / strangulation"),
    ("sexual_assault", "Sexual assault"),
    ("escalating_pattern", "Escalating pattern"),
    ("incident_within_7_days", "Incident within 7 days"),
    ("ongoing_threat", "Ongoing threat"),
    ("prior_order_violated", "Prior order violated"),
    ("children_witnessed", "Children witnessed"),
])

# ---- Employment family ----

_EMPLOYMENT_THEORY = ("Theory of the case", [
    ("discrimination_alleged", "Discrimination alleged"),
    ("retaliation_alleged", "Retaliation alleged"),
    ("public_policy_violation", "Public policy violation"),
    ("breach_of_contract", "Breach of contract"),
    ("whistleblower_protected", "Whistleblower-protected activity"),
    ("constructive_discharge", "Constructive discharge"),
])
_EMPLOYMENT_PROTECTED_CLASS = ("Protected class", [
    ("pc_race", "Race"),
    ("pc_sex_gender", "Sex / gender"),
    ("pc_age_40_plus", "Age (40+)"),
    ("pc_disability", "Disability"),
    ("pc_religion", "Religion"),
    ("pc_national_origin", "National origin"),
    ("pc_pregnancy", "Pregnancy"),
    ("pc_sexual_orientation", "Sexual orientation"),
])
_EMPLOYMENT_DOCS = ("Employment-law specifics", [
    ("eeoc_filed", "EEOC charge filed"),
    ("hr_complaint_filed", "Internal HR complaint filed"),
    ("performance_reviews_positive", "Positive performance reviews"),
    ("severance_offered", "Severance offered"),
    ("nda_signed", "NDA / arbitration agreement signed"),
    ("eeoc_deadline_approaching", "EEOC deadline approaching"),
])
_HARASSMENT = ("Harassment specifics", [
    ("physical_contact", "Physical / sexual contact"),
    ("quid_pro_quo", "Quid pro quo"),
    ("hostile_environment", "Hostile environment"),
    ("ongoing_pattern", "Ongoing pattern"),
    ("hr_aware", "HR aware / notified"),
    ("hr_response_inadequate", "HR response inadequate"),
    ("retaliation_after_report", "Retaliation after reporting"),
])
_WAGE_HOUR = ("Wage-and-hour violation", [
    ("unpaid_overtime", "Unpaid overtime"),
    ("misclassified_exempt", "Misclassified exempt"),
    ("misclassified_independent_contractor", "Misclassified as 1099"),
    ("off_clock_work", "Off-the-clock work"),
    ("denied_meal_breaks", "Denied meal breaks"),
    ("minimum_wage_violation", "Minimum wage violation"),
    ("tip_theft", "Tip theft / pooling violation"),
    ("class_potential", "Multiple employees affected"),
])

# ---- Civil Rights / Abuse family ----

_ABUSE = ("Abuse details", [
    ("minor_at_time", "Minor at time of abuse"),
    ("institutional_negligence", "Institutional negligence"),
    ("clergy_abuse", "Clergy / religious institution"),
    ("school_abuse", "School / education setting"),
    ("sports_abuse", "Sports / coaching setting"),
    ("medical_provider", "Medical provider"),
    ("multiple_victims_known", "Multiple victims known"),
    ("prior_complaints_ignored", "Prior complaints ignored"),
    ("sol_revival_window", "SOL revival window applies"),
    ("incident_over_10_years", "Incident over 10 years ago"),
])
_POLICE = ("Police misconduct details", [
    ("excessive_force", "Excessive force"),
    ("wrongful_arrest", "Wrongful arrest"),
    ("illegal_search", "Illegal search"),
    ("deadly_force", "Deadly force"),
    ("racial_profiling_alleged", "Racial profiling alleged"),
    ("video_available", "Video available"),
    ("body_cam_requested", "Body cam footage requested"),
    ("hospitalization_required", "Hospitalization required"),
    ("fatality", "Fatality"),
    ("criminal_charges_dropped", "Criminal charges dropped"),
])

# ---- Real Estate family ----

_REAL_ESTATE = ("Property dispute", [
    ("survey_done", "Survey completed"),
    ("title_insurance_in_place", "Title insurance in place"),
    ("encroachment_documented", "Encroachment documented"),
    ("hoa_involved", "HOA involved"),
    ("recorded_easement", "Recorded easement at issue"),
    ("foreclosure_filed", "Foreclosure filed"),
    ("loan_modification_attempted", "Loan modification attempted"),
])

# ---- Estate / Probate family ----

_ESTATE = ("Estate specifics", [
    ("contested_will", "Will contested"),
    ("undue_influence_alleged", "Undue influence alleged"),
    ("capacity_question", "Decedent capacity in question"),
    ("missing_will", "Missing or revoked will"),
    ("multiple_heirs_disputing", "Multiple heirs disputing"),
    ("trust_funded", "Trust funded"),
    ("trust_unfunded", "Trust drafted but unfunded"),
])

# ---- Immigration family ----

_IMMIGRATION = ("Immigration posture", [
    ("in_removal_proceedings", "In removal proceedings"),
    ("court_date_set", "Immigration court date set"),
    ("asylum_one_year_deadline", "1-year asylum deadline"),
    ("prior_denial", "Prior denial on file"),
    ("criminal_history", "Criminal history involved"),
    ("us_citizen_family", "US citizen family member"),
    ("dv_or_trafficking_victim", "DV or trafficking victim"),
])

# ---- Criminal Defense family ----

_CRIMINAL = ("Criminal posture", [
    ("arraignment_pending", "Arraignment pending"),
    ("custody_in", "In custody"),
    ("custody_out_on_bail", "Out on bail"),
    ("felony_charges", "Felony charges"),
    ("misdemeanor_charges", "Misdemeanor charges"),
    ("prior_convictions", "Prior convictions"),
    ("first_offense", "First offense"),
    ("plea_offered", "Plea offered"),
    ("evidence_motion_viable", "Suppression motion viable"),
])

# ============================================================================
# The big map: case_type → list of signal groups
# ============================================================================

INTAKE_SIGNAL_GROUPS_BY_TYPE = {
    # Personal Injury — share the PI signal groups
    "personal_injury":   [_PI_SEVERITY, _PI_LIABILITY, _PI_DEFENDANT],
    "auto_accident":     [_PI_SEVERITY, _PI_LIABILITY, _PI_DEFENDANT],
    "premises_liability":[_PI_SEVERITY, _PI_LIABILITY, _PI_DEFENDANT],
    "medical_malpractice":[_PI_SEVERITY, _PI_LIABILITY, _PI_DEFENDANT],
    "workers_comp":      [_PI_SEVERITY, _PI_LIABILITY, _PI_DEFENDANT],
    "product_liability": [_PI_SEVERITY, _PI_LIABILITY, _PI_DEFENDANT],
    "wrongful_death":    [_PI_SEVERITY, _PI_LIABILITY, _PI_DEFENDANT],
    "dog_bite":          [_PI_SEVERITY, _PI_LIABILITY, _PI_DEFENDANT],

    # Tenant Law
    "habitability":         [_TENANT_CONDITIONS, _TENANT_DOCS, _TENANT_LANDLORD, _TENANT_HEALTH],
    "toxic_exposure":       [_TOXIC, _TENANT_DOCS, _TENANT_LANDLORD, _TENANT_HEALTH],
    "illegal_lockout":      [_LOCKOUT, _TENANT_LANDLORD],
    "landlord_harassment":  [_TENANT_LANDLORD, _TENANT_DOCS],
    "eviction_defense":     [_EVICTION, _TENANT_DOCS, _TENANT_LANDLORD],
    "security_deposit":     [_DEPOSIT, _TENANT_DOCS],
    "wrongful_eviction":    [_LOCKOUT, _EVICTION, _TENANT_LANDLORD],
    "rent_control":         [_TENANT_DOCS, _TENANT_LANDLORD],

    # Family Law
    "divorce":               [_DIVORCE, _FAMILY_CHILDREN, _FAMILY_CONFLICT],
    "child_custody":         [_FAMILY_CHILDREN, _FAMILY_CONFLICT],
    "child_support":         [_FAMILY_CHILDREN],
    "domestic_violence_civil": [_DV, _FAMILY_CHILDREN],
    "adoption":              [_FAMILY_CHILDREN],
    "prenup":                [_DIVORCE],

    # Employment
    "wrongful_termination": [_EMPLOYMENT_THEORY, _EMPLOYMENT_PROTECTED_CLASS, _EMPLOYMENT_DOCS],
    "discrimination":       [_EMPLOYMENT_THEORY, _EMPLOYMENT_PROTECTED_CLASS, _EMPLOYMENT_DOCS],
    "sexual_harassment":    [_HARASSMENT, _EMPLOYMENT_DOCS],
    "wage_and_hour":        [_WAGE_HOUR, _EMPLOYMENT_DOCS],
    "retaliation":          [_EMPLOYMENT_THEORY, _EMPLOYMENT_DOCS],

    # Civil Rights / Abuse
    "sexual_abuse":         [_ABUSE],
    "police_misconduct":    [_POLICE],
    "institutional_abuse":  [_ABUSE],

    # Criminal Defense
    "dui":              [_CRIMINAL],
    "drug_charges":     [_CRIMINAL],
    "assault_battery":  [_CRIMINAL],
    "white_collar":     [_CRIMINAL],
    "theft_burglary":   [_CRIMINAL],
    "juvenile":         [_CRIMINAL],

    # Real Estate
    "boundary_dispute":     [_REAL_ESTATE],
    "title_issues":         [_REAL_ESTATE],
    "construction_defect":  [_REAL_ESTATE],
    "foreclosure_defense":  [_REAL_ESTATE],
    "hoa_dispute":          [_REAL_ESTATE],

    # Estate / Probate
    "will_contest":           [_ESTATE],
    "probate_administration": [_ESTATE],
    "trust_dispute":          [_ESTATE],
    "guardianship":           [_ESTATE],

    # Immigration
    "deportation_defense": [_IMMIGRATION],
    "asylum":              [_IMMIGRATION],
    "visa_greencard":      [_IMMIGRATION],
    "naturalization":      [_IMMIGRATION],

    # Other (universal only)
    "other": [],
}


def signal_groups_for(case_type):
    """Return the list of (group_name, [(code, label), ...]) for a case type,
    including the universal groups every case has."""
    specific = INTAKE_SIGNAL_GROUPS_BY_TYPE.get(case_type, [])
    return list(specific) + list(UNIVERSAL_INTAKE_GROUPS)


# Flat dict: every signal code → label (for display in detail/list views)
INTAKE_SIGNAL_LABELS = {}
for _groups in INTAKE_SIGNAL_GROUPS_BY_TYPE.values():
    for _group_name, _items in _groups:
        for _code, _label in _items:
            INTAKE_SIGNAL_LABELS[_code] = _label
for _group_name, _items in UNIVERSAL_INTAKE_GROUPS:
    for _code, _label in _items:
        INTAKE_SIGNAL_LABELS[_code] = _label

# Backward-compat: existing templates iterate over INTAKE_SIGNAL_GROUPS in
# places that aren't yet case-type-aware. Provide a fallback view: union of
# all PI groups (the original taxonomy) so legacy renders still work.
INTAKE_SIGNAL_GROUPS = [_PI_SEVERITY, _PI_LIABILITY, _PI_DEFENDANT] + UNIVERSAL_INTAKE_GROUPS

# ============================================================================
# Decision capture: referral reasons
# ============================================================================

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
    ("statute_expertise", "Knows the statute well"),
    ("trial_ready", "Trial-ready posture"),
]
REFERRAL_REASON_LABELS = dict(REFERRAL_REASONS)

# ============================================================================
# Decline reasons
# ============================================================================

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
    ("court_date_too_soon", "Court date too soon to prep"),
    ("other", "Other"),
]
DECLINE_REASON_LABELS = dict(DECLINE_REASONS)

# ============================================================================
# Outcomes
# ============================================================================

OUTCOMES = [
    ("settled", "Settled"),
    ("won_trial", "Won at trial"),
    ("lost_trial", "Lost at trial"),
    ("dropped", "Client dropped"),
    ("withdrawn", "Withdrawn"),
    ("no_recovery", "No recovery"),
    ("favorable_judgment", "Favorable judgment / order"),
]
OUTCOME_LABELS = dict(OUTCOMES)
OUTCOME_STYLES = {
    "settled": "bg-emerald-100 text-emerald-800",
    "won_trial": "bg-emerald-200 text-emerald-900",
    "favorable_judgment": "bg-emerald-100 text-emerald-800",
    "lost_trial": "bg-rose-100 text-rose-800",
    "dropped": "bg-slate-100 text-slate-700",
    "withdrawn": "bg-slate-100 text-slate-700",
    "no_recovery": "bg-rose-50 text-rose-700",
}
OUTCOMES_WITH_RECOVERY = {"settled", "won_trial", "favorable_judgment"}
