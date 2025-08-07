import os
import json
from configs.config import SETTINGS_FILE


def save_settings(zone, class_name, faction):
    settings = { "zone": zone, "class": class_name, "faction": faction }
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return { "zone": "All", "class": "Warrior", "faction": "All" }
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)