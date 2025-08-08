import tkinter as tk
from db.database import fetch_quests
from utils.progress import load_progress, save_progress
from ui.questList import quest_list
from ui.build import build
from utils.settings import save_settings, load_settings


class QuestTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WoW Quest Tracker")
        self.geometry("400x600")
        self.search_entry = None
        self.canvas = None
        self.scrollbar = None
        self.scroll_frame = None
        self.zone_filter_dropdown = None

        saved_settings = load_settings()
        saved_class = saved_settings.get("class", "Warrior")
        saved_faction = saved_settings.get("faction", "All")
        saved_zone = saved_settings.get("zone", "All")

        self.progress = load_progress()
        self.checkbox_vars = { }
        self.class_var = tk.StringVar(value=saved_class)
        self.faction_var = tk.StringVar(value=saved_faction)
        self.zone_filter_var = tk.StringVar(value=saved_zone)
        self.quests = fetch_quests(faction_filter=self.faction_var.get())
        self.build_ui()

    def build_ui(self):
        build(self)

    def update_quest_list(self):
        quest_list(self)
        save_settings(self.zone_filter_var.get(), self.class_var.get(), self.faction_var.get())

    def save(self):
        progress = load_progress()

        for qid, var in self.checkbox_vars.items():
            if var.get():
                progress[qid] = True
            else:
                progress.pop(qid, None)

        sorted_progress = { str(k): v for k, v in sorted(progress.items(), key=lambda item: int(item[0])) }
        save_progress(sorted_progress)