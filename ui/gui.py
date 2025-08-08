import tkinter as tk
import threading
from db.database import fetch_quests, fetch_character_quests_by_name
from utils.progress import load_progress, save_progress
from ui.questList import quest_list
from ui.build import build
from utils.settings import save_settings, load_settings
from tkinter import messagebox


class QuestTracker(tk.Tk):
    AUTO_REFRESH_MS = 5 * 60 * 1000

    def __init__(self):
        super().__init__()
        self.title("WoW Quest Tracker")
        self.geometry("700x600")
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
        self.sync_char_name_var = tk.StringVar(value="")
        self.build_ui()
        self.after(self.AUTO_REFRESH_MS, self.auto_refresh_check) # type: ignore[arg-type]

    def build_ui(self):
        build(self)

        sync_frame = tk.Frame(self)
        sync_frame.pack(fill=tk.X, padx=6, pady=6) # type: ignore[arg-type]

        tk.Label(sync_frame, text="Character name:").pack(side=tk.LEFT) # type: ignore[arg-type]
        char_entry = tk.Entry(sync_frame, textvariable=self.sync_char_name_var)
        char_entry.pack(side=tk.LEFT, padx=(6, 6)) # type: ignore[arg-type]
        sync_btn = tk.Button(sync_frame, text="Sync", command=self.on_sync_button)
        sync_btn.pack(side=tk.LEFT) # type: ignore[arg-type]

    def on_sync_button(self):
        name = self.sync_char_name_var.get().strip()
        if not name:
            messagebox.showinfo("Info", "Please enter a character name to sync.")
            return
        threading.Thread(target=self.sync_character_and_reload, args=(name,), daemon=True).start()

    def sync_character_and_reload(self, character_name):
        try:
            quest_ids = fetch_character_quests_by_name(character_name)
        except Exception as e:
            print("Error fetching character quests:", e)
            quest_ids = set()

        if not quest_ids:
            self.after(0, lambda: messagebox.showinfo("No quests", f"No quests found for {character_name}")) # type: ignore[arg-type]
            return

        progress = load_progress()

        for qid in quest_ids:
            progress[str(qid)] = True

        save_progress(progress)

        self.after(0, self.reload_after_sync) # type: ignore[arg-type]

    def reload_after_sync(self):
        self.progress = load_progress()
        self.update_quest_list()
        messagebox.showinfo("Synced", "Quests synced and UI refreshed.")

    def auto_refresh_check(self):
        name = self.sync_char_name_var.get().strip()
        if name:
            threading.Thread(target=self._auto_sync_background, args=(name,), daemon=True).start()

        self.after(self.AUTO_REFRESH_MS, self.auto_refresh_check) # type: ignore[arg-type]

    def _auto_sync_background(self, name):
        try:
            quest_ids = fetch_character_quests_by_name(name)
        except Exception as e:
            print("Auto-refresh DB error:", e)
            return

        if not quest_ids:
            return

        progress = load_progress()
        for qid in quest_ids:
            progress[str(qid)] = True
        save_progress(progress)

        self.after(0, lambda: (setattr(self, "progress", load_progress()), self.update_quest_list())) # type: ignore[arg-type]

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