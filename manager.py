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
from logger import logger

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
        try:
            if folder_path.exists():
                logger.error(f"Failed to create folder: {folder_path}", extra={"operation": "create_folder"})
                raise FileExistsError(f"Folder '{folder_path}' already exists.")
            folder_path.mkdir()
            logger.info(f"Created folder: {folder_path}", extra={"operation": "create_folder"})
            return folder_path
        except Exception as e:
            logger.error(f"Error creating folder: {str(e)}", extra={"operation": "create_folder"})
            raise

    def create_file(self, name: str, content: Optional[str] = None, remove_chars: Optional[str] = None) -> Path:
        """
        Create a file with optional content and optional characters to remove from that content.

        Raises:
            FileExistsError: if the file already exists.
        """
        file_path = self.base_dir / name
        try:
            if file_path.exists():
                logger.error(f"Failed to create file: {file_path}", extra={"operation": "create_file"})
                raise FileExistsError(f"File '{file_path}' already exists.")
            
            if content and remove_chars:
                content = content.replace(remove_chars, "")
            
            file_path.write_text(content or "")
            logger.info(f"Created file: {file_path}", extra={"operation": "create_file"})
            return file_path
        except Exception as e:
            logger.error(f"Error creating file: {str(e)}", extra={"operation": "create_file"})
            raise

    # ────────────────────────────────
    # 🚚 Move / Rename / Copy
    # ────────────────────────────────

    def move(self, source: str, destination: str) -> Path:
        """
        Move a file or folder from source to destination.
        """
        src = self.base_dir / source
        dst = self.base_dir / destination
        try:
            if not src.exists():
                logger.error(f"Source not found: {src}", extra={"operation": "move"})
                raise FileNotFoundError(f"Source '{src}' does not exist.")
            if dst.exists():
                logger.error(f"Destination exists: {dst}", extra={"operation": "move"})
                raise FileExistsError(f"Destination '{dst}' already exists.")
            
            if src.is_dir():
                shutil.move(str(src), str(dst))
            else:
                src.rename(dst)
            logger.info(f"Moved {src} to {dst}", extra={"operation": "move"})
            return dst
        except Exception as e:
            logger.error(f"Error moving {src} to {dst}: {str(e)}", extra={"operation": "move"})
            raise

    def rename(self, old: str, new: str) -> Path:
        """
        Rename a file or folder.
        """
        src = self.base_dir / old
        dst = self.base_dir / new
        try:
            if not src.exists():
                logger.error(f"Source not found: {src}", extra={"operation": "rename"})
                raise FileNotFoundError(f"Source '{src}' does not exist.")
            if dst.exists():
                logger.error(f"Destination exists: {dst}", extra={"operation": "rename"})
                raise FileExistsError(f"Destination '{dst}' already exists.")
            
            src.rename(dst)
            logger.info(f"Renamed {src} to {dst}", extra={"operation": "rename"})
            return dst
        except Exception as e:
            logger.error(f"Error renaming {src} to {dst}: {str(e)}", extra={"operation": "rename"})
            raise

    def copy(self, source: str, destination: str) -> Path:
        """
        Copy a file or folder.
        """
        src = self.base_dir / source
        dst = self.base_dir / destination
        try:
            if not src.exists():
                logger.error(f"Source not found: {src}", extra={"operation": "copy"})
                raise FileNotFoundError(f"Source '{src}' does not exist.")
            if dst.exists():
                logger.error(f"Destination exists: {dst}", extra={"operation": "copy"})
                raise FileExistsError(f"Destination '{dst}' already exists.")
            
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            logger.info(f"Copied {src} to {dst}", extra={"operation": "copy"})
            return dst
        except Exception as e:
            logger.error(f"Error copying {src} to {dst}: {str(e)}", extra={"operation": "copy"})
            raise

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
        try:
            if not folder_path.is_dir():
                logger.error(f"Not a directory: {folder_path}", extra={"operation": "zip_folder"})
                raise NotADirectoryError(f"'{folder_path}' is not a folder.")
            
            zip_path = folder_path.with_suffix('.zip')
            shutil.make_archive(str(zip_path.with_suffix('')), 'zip', str(folder_path))
            logger.info(f"Zipped folder {folder_path} to {zip_path}", extra={"operation": "zip_folder"})
            return zip_path
        except Exception as e:
            logger.error(f"Error zipping folder {folder_path}: {str(e)}", extra={"operation": "zip_folder"})
            raise

    # ────────────────────────────────
    # 🗑 Delete / View / Inspect
    # ────────────────────────────────

    def delete(self, name: str) -> None:
        """
        Delete a file or folder (recursively if folder).
        """
        path = self.base_dir / name
        try:
            if not path.exists():
                logger.error(f"File/folder not found: {path}", extra={"operation": "delete"})
                raise FileNotFoundError(f"'{path}' does not exist.")
            
            if path.is_dir():
                shutil.rmtree(str(path))
            else:
                path.unlink()
            logger.info(f"Deleted {path}", extra={"operation": "delete"})
        except Exception as e:
            logger.error(f"Error deleting {path}: {str(e)}", extra={"operation": "delete"})
            raise

    def view(self, name: str) -> str:
        """
        Return contents of a file, or list contents of a folder.
        """
        path = self.base_dir / name
        try:
            if not path.exists():
                logger.error(f"File/folder not found: {path}", extra={"operation": "view"})
                raise FileNotFoundError(f"'{path}' does not exist.")
            
            if path.is_file():
                content = path.read_text()
                logger.info(f"Viewed file contents: {path}", extra={"operation": "view"})
                return content
            elif path.is_dir():
                contents = "\n".join([p.name for p in path.iterdir()])
                logger.info(f"Listed directory contents: {path}", extra={"operation": "view"})
                return contents
            else:
                logger.error(f"Path is neither file nor directory: {path}", extra={"operation": "view"})
                return f"{name} exists but is not a regular file or directory."
        except Exception as e:
            logger.error(f"Error viewing {path}: {str(e)}", extra={"operation": "view"})
            raise

    # ────────────────────────────────
    # 📬 Email Support
    # ────────────────────────────────

    def email_file_or_folder(self, name: str, recipient: str, sender: str, password: str) -> None:
        """
        Email a file or zipped folder to a recipient.
        """
        path = self.base_dir / name
        try:
            if not path.exists():
                logger.error(f"File/folder not found: {path}", extra={"operation": "email"})
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
                logger.info(f"Emailed {path} to {recipient}", extra={"operation": "email"})

        except Exception as e:
            logger.error(f"Error emailing {path}: {str(e)}", extra={"operation": "email"})
            raise

    def email_notification(self, name: str, recipient: str, sender: str, password: str) -> None:
        """
        Send an email notification about the presence or status of a file or folder.
        """
        path = self.base_dir / name
        try:
            if not path.exists():
                logger.error(f"File/folder not found: {path}", extra={"operation": "email_notification"})
                raise FileNotFoundError(f"'{path}' does not exist.")
            
            msg = EmailMessage()
            msg['Subject'] = f"Status Update: {name}"
            msg['From'] = sender
            msg['To'] = recipient
            
            if path.is_file():
                size = path.stat().st_size
                msg.set_content(f"File '{name}' exists. Size: {size} bytes.")
            else:
                num_items = len(list(path.iterdir()))
                msg.set_content(f"Folder '{name}' exists. Contains {num_items} items.")
            
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.login(sender, password)
                smtp.send_message(msg)
                logger.info(f"Sent notification about {path} to {recipient}", extra={"operation": "email_notification"})

        except Exception as e:
            logger.error(f"Error sending notification about {path}: {str(e)}", extra={"operation": "email_notification"})
            raise
