import tkinter as tk
from tkinter import ttk
from configs.config import CLASS_FLAGS


def build(self):
    search_frame = ttk.Frame(self)
    search_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(search_frame, text="Filter by Zone:").pack(side="left")
    available_zones = set()
    zone_quests = { }

    for quest in self.quests:
        zone = quest.get("zone_name") or "Unknown Zone"
        zone_quests.setdefault(zone, []).append(quest)

    for zone, quests in zone_quests.items():
        if not all(self.progress.get(str(q["id"]), False) for q in quests):
            available_zones.add(zone)

    available_zones = sorted(available_zones)
    available_zones.insert(0, "All")

    if self.zone_filter_var.get() not in available_zones:
        self.zone_filter_var.set("All")

    self.zone_filter_dropdown = ttk.Combobox(search_frame, textvariable=self.zone_filter_var, values=available_zones, state="readonly")
    self.zone_filter_dropdown.pack(side="left", fill="x", expand=True, padx=5)
    self.zone_filter_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_quest_list())

    class_frame = ttk.LabelFrame(self, text="Filter by Class")
    class_frame.pack(fill="x", padx=10, pady=5)
    for i, cls in enumerate(CLASS_FLAGS):
        ttk.Radiobutton(class_frame, text=cls, variable=self.class_var, value=cls, command=self.update_quest_list).grid(row=i // 5, column=i % 5, sticky="w", padx=5)

    faction_frame = ttk.LabelFrame(self, text="Faction Filter")
    faction_frame.pack(fill="x", padx=10, pady=5)

    factions = [("All", "All"), ("Alliance", "Alliance"), ("Horde", "Horde")]
    for text, value in factions:
        ttk.Radiobutton(faction_frame, text=text, variable=self.faction_var, value=value, command=self.update_quest_list).pack(side="left", padx=5)

    self.canvas = tk.Canvas(self)
    self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
    self.scroll_frame = ttk.Frame(self.canvas)
    self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    self.canvas.pack(side="left", fill="both", expand=True)
    self.scrollbar.pack(side="right", fill="y")
    self.update_quest_list()