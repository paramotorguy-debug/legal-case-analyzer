import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def _path(name):
    return DATA_DIR / f"{name}.json"


def _load(name):
    p = _path(name)
    if not p.exists():
        return []
    return json.loads(p.read_text() or "[]")


def _save(name, data):
    _path(name).write_text(json.dumps(data, indent=2))


def now():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def new_id(prefix):
    return f"{prefix}_{uuid4().hex[:8]}"


def get_cases():
    return _load("cases")


def save_cases(cases):
    _save("cases", cases)


def get_case(case_id):
    return next((c for c in get_cases() if c["id"] == case_id), None)


def upsert_case(case):
    cases = get_cases()
    for i, c in enumerate(cases):
        if c["id"] == case["id"]:
            cases[i] = case
            save_cases(cases)
            return case
    cases.append(case)
    save_cases(cases)
    return case


def delete_case(case_id):
    save_cases([c for c in get_cases() if c["id"] != case_id])


def get_lawyers():
    return _load("lawyers")


def save_lawyers(lawyers):
    _save("lawyers", lawyers)


def get_lawyer(lawyer_id):
    return next((l for l in get_lawyers() if l["id"] == lawyer_id), None)


def upsert_lawyer(lawyer):
    lawyers = get_lawyers()
    for i, l in enumerate(lawyers):
        if l["id"] == lawyer["id"]:
            lawyers[i] = lawyer
            save_lawyers(lawyers)
            return lawyer
    lawyers.append(lawyer)
    save_lawyers(lawyers)
    return lawyer


def delete_lawyer(lawyer_id):
    save_lawyers([l for l in get_lawyers() if l["id"] != lawyer_id])
