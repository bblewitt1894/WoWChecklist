import json
import os
from configs.config import PROGRESS_FILE


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return { }


def save_progress(progress):
    try:
        sorted_items = sorted(progress.items(), key=lambda item: int(item[0]))
    except (ValueError, TypeError):
        items = [(str(k), v) for k, v in progress.items()]
        sorted_items = sorted(items, key=lambda item: int(item[0]) if item[0].isdigit() else item[0])

    sorted_progress = { str(k): v for k, v in sorted_items }
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)

    with open(PROGRESS_FILE, "w") as f:
        json.dump(sorted_progress, f, indent=2)