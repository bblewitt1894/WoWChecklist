import json
import os
from configs.config import PROGRESS_FILE


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return { }


def save_progress(progress):
    sorted_progress = {str(k): v for k, v in sorted(progress.items(), key=lambda item: int(item[0]))}

    with open(PROGRESS_FILE, 'w') as f:
        json.dump(sorted_progress, f, indent=2)
