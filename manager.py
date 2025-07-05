"""
FileManager: A class-based Python utility for handling file and folder operations
similar to basic shell commands — with added support for email notifications,
zip compression, and built-in error handling.

Supports:
- File and folder creation
- Move, rename, delete, copy
- View contents of file or directory
- Zip folders
- Send files via email
- Notify about file/folder status

Example usage:
    fm = FileManager()
    fm.create_file("notes.txt", content="hello")
    fm.move("notes.txt", "archive/")
"""

import shutil
import smtplib
from pathlib import Path
from email.message import EmailMessage
from typing import Optional
from datetime import datetime
import os

class FileManager:
    def __init__(self, base_dir: Path = Path.home()):
        """
        Initialize FileManager with a base directory (defaults to user's home).
        """
        self.base_dir = base_dir

    # ────────────────────────────────
    # 🔧 Creation Methods
    # ────────────────────────────────

    def create_folder(self, name: str) -> Path:
        """
        Create a new folder inside the base directory.

        Raises:
            FileExistsError: if the folder already exists.
        """
        folder_path = self.base_dir / name
        if folder_path.exists():
            raise FileExistsError(f"Folder '{folder_path}' already exists.")
        folder_path.mkdir(parents=True)
        return folder_path

    def create_file(self, name: str, content: Optional[str] = None, remove_chars: Optional[str] = None) -> Path:
        """
        Create a file with optional content and optional characters to remove from that content.

        Raises:
            FileExistsError: if the file already exists.
        """
        file_path = self.base_dir / name
        if file_path.exists():
            raise FileExistsError(f"File '{file_path}' already exists.")
        content = content or ""
        if remove_chars:
            for char in remove_chars:
                content = content.replace(char, "")
        file_path.write_text(content)
        return file_path

    # ────────────────────────────────
    # 🚚 Move / Rename / Copy
    # ────────────────────────────────

    def move(self, source: str, destination: str) -> Path:
        """
        Move a file or folder from source to destination.
        """
        src = self.base_dir / source
        dst = self.base_dir / destination
        if not src.exists():
            raise FileNotFoundError(f"Source '{src}' not found.")
        if dst.is_dir():
            dst = dst / src.name
        shutil.move(str(src), str(dst))
        return dst

    def rename(self, old: str, new: str) -> Path:
        """
        Rename a file or folder.
        """
        src = self.base_dir / old
        dst = self.base_dir / new
        if not src.exists():
            raise FileNotFoundError(f"Source '{src}' not found.")
        src.rename(dst)
        return dst

    def copy(self, source: str, destination: str) -> Path:
        """
        Copy a file or folder.
        """
        src = self.base_dir / source
        dst = self.base_dir / destination
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        return dst

    # ────────────────────────────────
    # 📦 Zip
    # ────────────────────────────────

    def zip_folder(self, folder_name: str) -> Path:
        """
        Zip the contents of a folder.

        Returns:
            Path to the .zip file.
        """
        folder_path = self.base_dir / folder_name
        if not folder_path.is_dir():
            raise NotADirectoryError(f"'{folder_path}' is not a folder.")
        zip_path = folder_path.with_suffix('.zip')
        shutil.make_archive(str(zip_path.with_suffix('')), 'zip', str(folder_path))
        return zip_path

    # ────────────────────────────────
    # 🗑 Delete / View / Inspect
    # ────────────────────────────────

    def delete(self, name: str) -> None:
        """
        Delete a file or folder (recursively if folder).
        """
        path = self.base_dir / name
        if not path.exists():
            raise FileNotFoundError(f"'{path}' does not exist.")
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

    def view(self, name: str) -> str:
        """
        Return contents of a file, or list contents of a folder.
        """
        path = self.base_dir / name
        if not path.exists():
            raise FileNotFoundError(f"'{path}' does not exist.")
        if path.is_file():
            return path.read_text()
        elif path.is_dir():
            return "\n".join([p.name for p in path.iterdir()])
        else:
            return f"{name} exists but is not a regular file or directory."

    # ────────────────────────────────
    # 📬 Email Support
    # ────────────────────────────────

    def email_file_or_folder(self, name: str, recipient: str, sender: str, password: str) -> None:
        """
        Email a file or zipped folder to a recipient.
        """
        path = self.base_dir / name
        if not path.exists():
            raise FileNotFoundError(f"'{path}' does not exist.")
        if path.is_dir():
            path = self.zip_folder(name)

        msg = EmailMessage()
        msg['Subject'] = f"File/Folder: {name}"
        msg['From'] = sender
        msg['To'] = recipient
        msg.set_content(f"Attached is '{name}' from {self.base_dir}.")

        with path.open('rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename=path.name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)

    def email_notification(self, name: str, recipient: str, sender: str, password: str) -> None:
        """
        Send an email notification about the presence or status of a file or folder.
        """
        path = self.base_dir / name
        if not path.exists():
            raise FileNotFoundError(f"'{path}' does not exist.")

        msg = EmailMessage()
        msg['Subject'] = f"Notification: {name}"
        msg['From'] = sender
        msg['To'] = recipient
        msg.set_content(
            f"The file or folder '{name}' is located at:\n\n{path.resolve()}\n\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Host: {os.uname().nodename}"
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
