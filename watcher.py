""" 
watcher.py - Interactive file watcher for WatchZone.

📌 Description:
This script monitors the ~/WatchZone directory for new files or folders.
When a new item is detected, it prompts the user with a menu of actions
like move, copy, zip, rename, delete, or email — and automates those using `cli.py`.

Please note: This script only acts on files or folders created in the WatchZone directory and those that have just been created. It does not act on files or folders that have already already in the WatchZone directory.

✅ How to run:
$ python3 watcher.py

Make sure `cli.py` and all related commands are implemented and available in the same directory.
"""

import os
import time
import subprocess
from pathlib import Path
from logger import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directory to monitor
WATCH_DIR = Path.home() / "WatchZone"
WATCH_DIR.mkdir(exist_ok=True)

class InteractiveWatcher(FileSystemEventHandler):
    """
    A Watchdog event handler that prompts the user to act on newly created files/folders.
    """

    def on_created(self, event):
        """
        Triggered when a new file or directory is created in the watch directory.
        """
        path = Path(event.src_path)
        if not path.exists():
            return

        logger.info(f"Created file: {path}")

        if path.is_file():
            print(f"\n📄 File detected: {path.name}")
        elif path.is_dir():
            print(f"\n📁 Folder detected: {path.name}")

        self.prompt_user_action(path)

    def prompt_user_action(self, path: Path):
        """
        Present a menu to the user for actions to take on the new file/folder.
        Retries if an error occurs.
        """
        actions = [
            "1. Move",
            "2. Rename",
            "3. Zip",
            "4. Delete",
            "5. View",
            "6. Copy",
            "7. Email",
            "8. Skip"
        ]

        while True:
            print("What would you like to do?")
            for action in actions:
                print(action)

            choice = input("\nEnter choice [1-8]: ").strip()

            try:
                if choice == "1":  # Move
                    dest = input("Move to (absolute or ~ path): ").strip()
                    subprocess.run([
                        "python3", "cli.py", "move", str(path), str(Path(dest).expanduser())
                    ], check=True)
                    logger.info(f"Watching: {self.WATCH_DIR.resolve()}")
                    print(f"👀 Watching: {self.WATCH_DIR.resolve()}")

                elif choice == "2":  # Rename
                    new_name = input("Rename to: ").strip()
                    subprocess.run([
                        "python3", "cli.py", "rename", str(path), new_name
                    ], check=True)
                    logger.info(f"Watching: {self.WATCH_DIR.resolve()}")
                    print(f"👀 Watching: {self.WATCH_DIR.resolve()}")

                elif choice == "3":  # Zip
                    subprocess.run([
                        "python3", "cli.py", "zip", str(path)
                    ], check=True)

                elif choice == "4":  # Delete
                    subprocess.run([
                        "python3", "cli.py", "delete", str(path)
                    ], check=True)
                    logger.info(f"Watching: {self.WATCH_DIR.resolve()}")
                    print(f"👀 Watching: {self.WATCH_DIR.resolve()}")

                elif choice == "5":  # View
                    subprocess.run([
                        "python3", "cli.py", "view", str(path)
                    ], check=True)
                    logger.info(f"Watching: {self.WATCH_DIR.resolve()}")
                    print(f"👀 Watching: {self.WATCH_DIR.resolve()}")

                elif choice == "6":  # Copy
                    dest = input("Copy to (absolute or ~ path): ").strip()
                    subprocess.run([
                        "python3", "cli.py", "copy", str(path), str(Path(dest).expanduser())
                    ], check=True)
                    logger.info(f"Watching: {self.WATCH_DIR.resolve()}")
                    print(f"👀 Watching: {self.WATCH_DIR.resolve()}")

                elif choice == "7":  # Email
                    sender = input("Sender email: ").strip()
                    recipient = input("Recipient email: ").strip()
                    subprocess.run([
                        "python3", "cli.py", "email",
                        str(path), "--sender", sender, "--recipient", recipient
                    ], check=True)
                    logger.info(f"Watching: {self.WATCH_DIR.resolve()}")
                    print(f"👀 Watching: {self.WATCH_DIR.resolve()}")

                elif choice == "8":  # Skip
                    logger.info("Skipped")
                    print("⏭️ Skipped.\n")
                    logger.info(f"Watching: {self.WATCH_DIR.resolve()}")
                    print(f"👀 Watching: {self.WATCH_DIR.resolve()}")

                else:
                    logger.error("Invalid choice. Please enter a number from 1 to 8.")
                    print("❌ Invalid choice. Please enter a number from 1 to 8.")
                    continue 
                
                break               

            except KeyboardInterrupt:
                print("\n🛑 Stopping watcher.")
                os._exit(0)

def start_watching():
    """
    Start the file watcher and keep listening for new files/folders.
    """

    logger.info(f"Watching: {WATCH_DIR.resolve()}")
    print(f"👀 Watching: {WATCH_DIR.resolve()}")
    observer = Observer()
    event_handler = InteractiveWatcher()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Watcher stopped by user")
        print("\n🛑 Stopping watcher.")
        os._exit(0)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print("❌ Error occurred. Let's try again.")

if __name__ == "__main__":
    start_watching()