import argparse
import shutil
from pathlib import Path
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

def send_email_notification(source, destination):
    time_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    subject = f"Moved '{source.name}' to '{destination}'"
    body = (
        f"The file or folder '{source.name}' was moved to:\n\n"
        f"{destination}\n\n"
        f"Time: {time_str}\n"
        f"Host: {os.uname().nodename}"
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

def parse_args():
    parser = argparse.ArgumentParser(description="Move files or directories and optionally notify via email")
    parser.add_argument("source", help="Source file or directory")
    parser.add_argument("destination", help="Destination path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite if destination exists")
    parser.add_argument("--email", action="store_true", help="Send email notification after moving")
    return parser.parse_args()

def move_path(source: Path, destination: Path, force: bool, verbose: bool):
    if not source.exists():
        raise FileNotFoundError(f"Source path '{source}' does not exist.")

    if destination.exists() and not force:
        raise FileExistsError(f"Destination path '{destination}' already exists. Use -f to overwrite.")

    if verbose:
        print(f"Moving '{source}' to '{destination}'")

    shutil.move(str(source), str(destination))

    if verbose:
        print("Move completed successfully")

def main():
    args = parse_args()
    source = Path(args.source)
    destination = Path(args.destination)

    try:
        move_path(source, destination, args.force, args.verbose)

        if args.email:
            send_email_notification(source, destination)

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())