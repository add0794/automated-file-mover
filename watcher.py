from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time
import logging

class FileWatcher(FileSystemEventHandler):
    def __init__(self, watch_dir: Path, file_manager: FileManager):
        self.watch_dir = watch_dir
        self.file_manager = file_manager
        self.observer = Observer()

    def start(self):
        logging.info(f"👀 Watching directory: {self.watch_dir}")
        self.observer.schedule(self, str(self.watch_dir), recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            logging.info("🛑 Stopped watcher.")
        self.observer.join()

    def on_created(self, event):
        path = Path(event.src_path)
        if path.is_file():
            logging.info(f"📄 File created: {path.name}")
            # Optional: read or move the file
        elif path.is_dir():
            logging.info(f"📁 Folder created: {path.name}")

    def on_moved(self, event):
        src = Path(event.src_path)
        dst = Path(event.dest_path)
        logging.info(f"🚚 Moved: {src.name} → {dst.name}")

    def on_deleted(self, event):
        path = Path(event.src_path)
        logging.info(f"❌ Deleted: {path.name}")
