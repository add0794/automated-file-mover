import time
import os
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === CONFIG ===
WATCH_DIR = Path.home() / "WatchZone"
LOG_FILE = "watch_home.log"

# === LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# === HANDLER CLASS ===
class PathWatcher(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.ensure_watch_dir()

    def ensure_watch_dir(self):
        if not WATCH_DIR.exists():
            WATCH_DIR.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created watch directory: {WATCH_DIR}")
        elif not WATCH_DIR.is_dir():
            raise ValueError(f"Path exists but is not a directory: {WATCH_DIR}")

    def on_any_event(self, event):
        logging.debug(f"⚡ EVENT: {event.event_type} on {event.src_path}")

    def on_created(self, event):
        path = Path(event.src_path)
        if path.exists():
            self.handle_new_path(path)

    def on_moved(self, event):
        path = Path(event.dest_path)
        if path.exists():
            self.handle_new_path(path)

    def handle_new_path(self, path: Path, max_retries=3):
        """
        Handle moving a new path with retry mechanism.
        
        Args:
            path: The path to move
            max_retries: Maximum number of retry attempts
        """
        try:
            if not path.exists():
                logging.info(f"❌ Skipped: path no longer exists - {path}")
                return

            if path.name.startswith('.') or path.name in {
                'Library', 'Applications', 'Desktop', 'Documents', 'Downloads'}:
                logging.info(f"❌ Skipped system folder: {path}")
                return

            logging.info(f"📁 New {'folder' if path.is_dir() else 'file'} detected: {path}")

            # Get destination path from user
            dest_input = self.get_destination_input(path)
            if not dest_input:
                return

            dest_path = Path.home() / dest_input
            
            # Try to move the path
            success = self.move_path(path, dest_path, max_retries)
            if not success:
                # Ask if user wants to try a different destination
                if self.ask_for_retry(path):
                    self.handle_new_path(path)  # Try again with new destination

        except Exception as e:
            logging.error(f"⚠️ Error handling path: {e}")

    def get_destination_input(self, path: Path) -> str:
        """Get destination input from user."""
        while True:
            dest_input = input(
                f"\n🟡 Where would you like to move '{path.name}' inside your home directory?\n"
                f"➡️  Example: github/{path.name}\n"
                f"➡️  Enter subpath or press Enter to skip: "
            ).strip()

            if not dest_input:
                logging.info("User skipped moving the path.")
                return None

            return dest_input

    def move_path(self, source: Path, dest: Path, max_retries: int) -> bool:
        """
        Move a path with retry mechanism.
        
        Args:
            source: Source path
            dest: Destination path
            max_retries: Maximum number of retry attempts
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        attempt = 0
        while attempt < max_retries:
            attempt += 1
            
            try:
                if not dest.parent.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)

                logging.info(f"✅ Attempt {attempt}/{max_retries}: Moving to {dest}")
                result = subprocess.run([
                    "python3", "file_mover.py",
                    str(source),
                    str(dest),
                    "--verbose"
                ], capture_output=True, text=True)

                if result.returncode == 0:
                    logging.info(f"✅ Move succeeded: {result.stdout.strip()}")
                    return True
                else:
                    logging.error(f"❌ Move failed (attempt {attempt}/{max_retries}): {result.stderr.strip()}")
                    
            except Exception as e:
                logging.error(f"⚠️ Error on attempt {attempt}/{max_retries}: {e}")

        return False

    def ask_for_retry(self, path: Path) -> bool:
        """Ask user if they want to try moving the path again."""
        while True:
            response = input(
                f"\n⚠️ Move failed for '{path.name}'. Try again with a different destination? (y/n): "
            ).strip().lower()
            
            if response in ['y', 'n']:
                return response == 'y'
            print("Please enter 'y' or 'n'")

# === MAIN ===
def main():
    print(f"👀 Watching: {WATCH_DIR.resolve()}")
    observer = Observer()
    handler = PathWatcher()
    observer.schedule(handler, path=str(WATCH_DIR), recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Watcher stopped.")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
