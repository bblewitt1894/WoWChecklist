# WoWChecklist

**WoWChecklist** is a World of Warcraft quest tracking tool designed for completionists, speed-levelers, and anyone who wants a clear, organized view of their remaining quests.  
It connects to a WoW 1.12.1 (Vanilla) database and displays available quests filtered by **Zone**, **Class**, and **Faction**.

---

## ✨ Features

- **Full Quest List** – Pulls quests directly from the WoW database.
- **Smart Filtering** – Narrow down quests by:
    - Zone
    - Class (Warrior, Mage, etc.)
    - Faction (Alliance / Horde / All)
- **Progress Tracking** – Mark quests as completed and save progress locally.
- **Persistent Save** – Completed quests are stored in `configs/quest_progress.json` and automatically loaded on startup.
- **Editable Progress** – Unchecking a quest removes it from the save file.
- **Sorted Output** – Saved quest IDs are stored in ascending numerical order for easy reading.
- **Lightweight GUI** – Simple, scrollable interface built with Tkinter.
- **Currently Supports** – World of Warcraft **1.12.1 (Vanilla)** databases.
- **Import Characters** - Sync the program with the character to pull the quest list in to the quest progression file

---

## 📦 Requirements

- Python **3.8+**
- A WoW 1.12.1 database (MySQL / MariaDB)
- The following Python packages:
    - `mysql-connector-python`
    - `tkinter` (usually included with Python, may require OS-level package like `python3-tk` on Linux)

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bblewitt1894/WoWChecklist.git
   cd WoWChecklist
   ```

2. **Install dependencies**

   Make sure you have Python **3.8+** installed, then run:
   ```bash
   pip install mysql-connector-python
   pip install tk
   ```

3. Configure database connection

   Edit your database connection details in .env file.

   Make sure you have access to the WoW quest database tables.

4. Run the application
   ```bash
   python "WoW Vanilla Checklist.py"
   ```

---

## 🖥 Usage

On launch, select your Class, Faction, and optionally filter by Zone.

Scroll through the quest list and check off quests you’ve completed.

Click Save to store your progress.

Next time you open the program, your progress will be restored.

---

## 🚀 Planned Features

Support for additional WoW expansions (TBC and WotLK)

Additions to Vanilla when reaching to a point that something else is needed.

---

## 🤝 Contributing

Contributions are welcome!
If you'd like to help add features, fix bugs, or expand database compatibility:

Fork the repo

Create a new branch (feature/my-feature)

Commit changes

Open a pull request

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE)

---

## 💡 Notes

This tool is not a WoW addon — it’s a standalone Python application.

You’ll need access to a WoW 1.12.1 database for it to work.

Quest data accuracy depends on your database’s completeness.

---

Enjoy questing, and may your bags always be empty and your hearthstone off cooldown!