import time
import os
import sys
import logging
import subprocess
from pathlib import Path
from typing import Optional, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Configuration
WATCH_DIR = Path.home() / "WatchZone"
LOG_FILE = "watch_home.log"

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class PathWatcher(FileSystemEventHandler):
    """
    A custom FileSystemEventHandler that watches for new files and folders in the watch directory,
    prompts the user for a destination, and handles file moves with optional email notifications.
    
    Attributes:
        observer (Observer): The watchdog Observer instance for managing the file system watch
    """
    observer = None

    def __init__(self):
        """
        Initialize the PathWatcher instance and ensure the watch directory exists.
        """
        super().__init__()
        self.ensure_watch_dir()

    def ensure_watch_dir(self):
        """
        Ensure the watch directory exists, creating it if necessary.
        """
        if not WATCH_DIR.exists():
            WATCH_DIR.mkdir(parents=True, exist_ok=True)
            logging.info(f"✅ Created watch directory: {WATCH_DIR}")

    def on_created(self, event):
        """
        Handle file creation events by processing the new path.
        
        Args:
            event (FileSystemEvent): The watchdog event object containing the created path
        """
        self.handle_new_path(Path(event.src_path))

    def on_moved(self, event):
        """
        Handle file move events by processing the destination path.
        
        Args:
            event (FileSystemEvent): The watchdog event object containing the moved path
        """
        self.handle_new_path(Path(event.dest_path))

    def handle_new_path(self, path: Path):
        """
        Handle a new file or folder by prompting the user for a destination and moving it.
        
        Args:
            path (Path): The path to the newly created or moved file/folder
        """
        logging.info(f"📁 New {'folder' if path.is_dir() else 'file'} detected: {path}")
        EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        while True:
            dest_input = input(
                f"\n🟡 Where would you like to move '{path.name}' inside your home directory?\n"
                f"➡️  Example: github/{path.name}\n"
                f"➡️  Type Exit to quit the watcher, Enter to skip, or enter a subpath: "
            )

            if dest_input.lower() == "exit":
                logging.info("👋 Exiting watcher.")
                os._exit(0)

            elif dest_input.lower() in ["enter", ""]:
                logging.info(f"⏭️ User skipped: {path}")
                print(f"👀 Watching: {WATCH_DIR.resolve()}")
                return

            # Construct destination path
            dest_path = Path.home() / dest_input
            dest = (
                dest_path / path.name if dest_path.is_dir() or not dest_path.exists()
                else dest_path.parent / path.name
            )

            # Ask for email
            email = input("📧 Enter an email address to notify (or press Enter to skip): ").strip()
            if email and not re.match(EMAIL_REGEX, email):
                print("❌ Invalid email format. Please try again.")
                continue

            args = [
            "python3", "file_mover.py",
            str(path), str(dest),
            "--verbose"
            ]
            if email:
               args += ["--email", email]

            logging.info(f"✅ Attempting to move to {dest}")
            logging.info(f"Running command: {' '.join(args)}")

            try:
                result = subprocess.run(args, capture_output=True, text=True, check=True)
                logging.info(f"✅ Move succeeded: {result.stdout.strip()}")
                print(f"👀 Watching: {WATCH_DIR.resolve()}")
                return

            except subprocess.CalledProcessError as e:
                logging.error(f"❌ Move failed with return code {e.returncode}")

def main():
    """
    Main entry point for the file watcher application.
    
    Sets up the file system observer and begins watching for changes in the watch directory.
    """
    print(f"👀 Watching: {WATCH_DIR.resolve()}")

    observer = Observer()
    path_watcher = PathWatcher() 
    observer.schedule(path_watcher, path=str(WATCH_DIR), recursive=True)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Exiting watcher.")
        os._exit(0)

if __name__ == "__main__":
    main()