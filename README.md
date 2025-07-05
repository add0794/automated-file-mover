# 🗂 Automated File & Folder Manager (Python)

A safer, smarter alternative to using the shell for basic file and folder operations. This Python tool handles file creation, renaming, moving, deleting, zipping, and more — with built-in logging, error handling, and optional email notifications.

---

## ✅ A Need for Error-Free File & Folder Operations

The shell is powerful — but also error-prone. One typo or wrong working directory and you've:
- Deleted the wrong file
- Overwritten important data
- Broken a path without knowing it

This tool wraps core shell actions in a Python class (`FileManager`) that provides:
- 📦 Clear APIs for file/folder operations
- ✅ Safe error handling with helpful exceptions
- 🔐 Optional email notifications to file/folder events
- 📜 Logging to file and console
- 📡 Watchdog support for automatic reactions to file/folder events
- 📁 Modular CLI interface for power users

---

## 🛠 Features

### Core Commands
- Create empty files or files with text
- Remove characters from files
- Create folders
- Move or rename files/folders
- Delete files/folders
- View file content
- Zip folders
- Copy files/folders
- Email file/folder (as attachment or notification)

### Bonus Features
- 🕵️‍♀️ File/folder monitoring with `watchdog`
- 🧪 Unit-testable architecture
- 📨 Optional email alerts per command
- 🧩 CLI modularity with `argparse subcommands`

---

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/add0794/automated-file-mover.git
cd automated-file-mover
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create the WatchZone directory:
```bash
mkdir -p ~/WatchZone
```

---

## 🚀 Example Usage (CLI)

```bash
# Create a new file with text
python cli.py create-file notes.txt --text "Hello there!"

# Create a file and remove characters
python cli.py create-file notes.txt --text "Hello there!" --remove "there"

# Create a new folder
python cli.py create-folder Archive

# Move a file with email notification
python cli.py move notes.txt Archive/ --email --sender you@example.com --recipient you@example.com

# Rename a file
python cli.py rename oldname.txt newname.txt

# Delete a file
python cli.py delete Archive/notes.txt

# View file contents
python cli.py view Archive/notes.txt
```

## 📁 File Watcher

The file watcher monitors the `~/WatchZone` directory for new files and folders. When a new item is detected, it will:
1. Display the detected item
2. Present a menu of actions:
   - Move
   - Rename
   - Zip
   - Delete
   - View
   - Copy
   - Email
   - Skip
3. Execute the chosen action
4. Continue watching for new items

## 📝 Logging

All operations are logged with:
- Timestamps
- Operation type
- File paths
- Success/failure status
- Error details (if any)

Logs are written to both console and file for easy debugging and audit trails.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

---

## 📋 Project Structure

```
automated-file-mover/
├── cli.py              # Main CLI interface
├── manager.py          # Core FileManager class
├── watcher.py          # Watchdog implementation
└── .gitignore          # Git ignore rules
```

---

## 📢 Note

This project is actively maintained. Please check the latest version for any updates or improvements. PRs welcome! This is built to grow.