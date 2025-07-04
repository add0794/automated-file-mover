import argparse
import shutil
from pathlib import Path
from datetime import datetime
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv
from typing import Optional

# Load .env values
load_dotenv()

EMAIL_SENDER: Optional[str] = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD: Optional[str] = os.getenv("EMAIL_PASSWORD")
WATCHZONE = Path.home() / "WatchZone"
WATCHZONE.mkdir(exist_ok=True)

def remove_and_save(text: str, char: Optional[str] = None, filename: Optional[str] = None, just_save: bool = False) -> Path:
    """Optionally clean text and save it to WatchZone."""
    if just_save:
        cleaned = text  # Save as-is
    else:
        if not char:
            raise ValueError("You must provide --char unless using --just-save")
        cleaned = text.replace(char, "")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_name = filename or f"cleaned_text_{timestamp}.txt"
    output_path = WATCHZONE / output_name
    output_path.write_text(cleaned)
    print(f"✅ File written to: {output_path}")
    return output_path

def move_path(source: Path, destination: Path, force: bool = False, verbose: bool = False) -> None:
    """Move file or folder with optional overwrite and logging."""
    if not source.exists():
        raise FileNotFoundError(f"Source path '{source}' does not exist.")
    if destination.exists() and not force:
        raise FileExistsError(f"Destination '{destination}' exists. Use --force to overwrite.")

    if verbose:
        print(f"📦 Moving '{source}' → '{destination}'")

    shutil.move(str(source), str(destination))

    if verbose:
        print("✅ Move completed successfully.")

def send_email_notification(source: Path, destination: Path, recipient: str) -> None:
    """Send an email notification after moving."""
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        raise ValueError("Missing EMAIL_SENDER or EMAIL_PASSWORD in .env")

    time_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    msg = EmailMessage()
    msg["Subject"] = f"Moved '{source.name}' to '{destination}'"
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient
    msg.set_content(
        f"The file '{source.name}' was moved to:\n{destination}\n\nTime: {time_str}\nHost: {os.uname().nodename}"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

def parse_args():
    parser = argparse.ArgumentParser(description="Clean and move text files with optional email.")
    parser.add_argument("--text", help="Text to clean")
    parser.add_argument("--src", help="Name of file in ~/WatchZone to clean")
    parser.add_argument("--just-save", action="store_true", help="Only save the file without removing characters")
    parser.add_argument("--make-folder", help="Create a new folder in WatchZone (name required)")
    parser.add_argument("--char", required=True, help="Character to remove")
    parser.add_argument("--dst", required=True, help="Destination directory")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("--email", nargs="?", const=True, help="Send email notification (optional recipient)")
    return parser.parse_args()

def main():
    args = parse_args()
    destination = Path(args.dst).expanduser()
    destination.mkdir(parents=True, exist_ok=True)

    # If making a folder, handle it separately
    if args.make_folder:
        folder_name = args.make_folder.strip().replace(" ", "_")
        folder_path = WATCHZONE / folder_name

        if folder_path.exists():
            print(f"❌ Folder '{folder_name}' already exists in WatchZone.")
            return 1

        folder_path.mkdir(parents=True)
        print(f"📁 Created folder: {folder_path}")

        try:
            move_path(folder_path, destination / folder_name, force=args.force, verbose=args.verbose)

            if args.email:
                recipient = args.email if isinstance(args.email, str) else input("📧 Enter recipient email: ").strip()
                if not recipient:
                    raise ValueError("Recipient email required when using --email")
                send_email_notification(folder_path, destination, recipient)

        except Exception as e:
            print(f"❌ Error moving folder: {e}")
            return 1

        return 0  # Exit after folder creation and move

    # Otherwise, handle file-based logic
    if args.text:
        source_path = remove_and_save(args.text, args.char, just_save=args.just_save)
    elif args.src:
        src_path = WATCHZONE / args.src
        if not src_path.exists():
            print(f"❌ File not found: {src_path}")
            return 1
        raw_text = src_path.read_text()
        source_path = remove_and_save(raw_text, args.char, filename=src_path.name, just_save=args.just_save)
    else:
        if args.just_save:
            # Save empty file
            source_path = remove_and_save("", filename=None, just_save=True)
        else:
            print("❌ Must provide --text or --src (or use --just-save to create empty file)")
            return 1

    try:
        move_path(source_path, destination / source_path.name, force=args.force, verbose=args.verbose)

        if args.email:
            recipient = args.email if isinstance(args.email, str) else input("📧 Enter recipient email: ").strip()
            if not recipient:
                raise ValueError("Recipient email required when using --email")
            send_email_notification(source_path, destination, recipient)

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
