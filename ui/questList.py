import tkinter as tk
from tkinter import ttk
from configs.config import CLASS_FLAGS


def quest_list(app):
    for widget in app.scroll_frame.winfo_children():
        widget.destroy()

    selected_zone = app.zone_filter_var.get()
    selected_class = app.class_var.get()
    selected_faction = app.faction_var.get()
    class_mask = CLASS_FLAGS.get(selected_class, 0)
    zones = { }

    for quest in app.quests:
        zone = quest.get("zone_name") or "Unknown Zone"
        required_classes = quest.get("RequiredClasses", 0)
        side = quest.get("side", "Neutral")

        if selected_zone != "All" and zone != selected_zone:
            continue

        if required_classes and not (required_classes & class_mask):
            continue

        if selected_faction == "Alliance" and side not in ("Alliance", "Neutral"):
            continue
        elif selected_faction == "Horde" and side not in ("Horde", "Neutral"):
            continue

        zones.setdefault(zone, []).append(quest)

    displayed_any = False

    for zone, quests in sorted(zones.items()):
        if all(app.progress.get(str(q["id"]), False) for q in quests):
            if selected_zone != "All":
                ttk.Label(app.scroll_frame, text="This zone was already completed.", font=("Helvetica", 12, "italic")).pack(anchor="center", pady=20)
                return
            continue

        ttk.Label(app.scroll_frame, text=f"Area: {zone}", font=("Helvetica", 14, "bold")).pack(anchor="w", pady=(10, 0))

        for quest in sorted(quests, key=lambda q: (q["QuestLevel"], q["id"])):
            quest_id = str(quest["id"])

            if app.progress.get(quest_id, False):
                continue

            var = app.checkbox_vars.get(quest_id)
            if var is None:
                var = tk.BooleanVar(value=False)
                app.checkbox_vars[quest_id] = var

            display = f"{quest_id}: [{quest['QuestLevel']}] {quest['name']}"
            cb = ttk.Checkbutton(app.scroll_frame, text=display, variable=var, command=app.save)
            cb.pack(anchor="w", padx=20)

            displayed_any = True

    if not displayed_any:
        ttk.Label(app.scroll_frame, text="No quests found matching current filters.", font=("Helvetica", 12, "italic")).pack(anchor="center", pady=20)