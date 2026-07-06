
import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HISTORY_FILE = os.path.join(
    BASE_DIR,
    "Outputs",
    "risk_history.json"
)


def save_snapshot(total_exposure):

    history = []

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.append({
        "timestamp": datetime.now().isoformat(),
        "total_exposure": total_exposure
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
    print("Snapshot saved:", HISTORY_FILE)
    

def get_exposure_delta():

    if not os.path.exists(HISTORY_FILE):
        return None

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    if len(history) < 2:
        return None

    previous = history[-2]["total_exposure"]
    current = history[-1]["total_exposure"]

    change = current - previous

    pct_change = 0

    if previous > 0:
        pct_change = (change / previous) * 100

    return {
        "previous": previous,
        "current": current,
        "change": change,
        "pct_change": pct_change
    }