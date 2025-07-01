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

def send_email_notification(source, destination, recipient):
    """
    Send an email notification about a file/folder move operation.

    Args:
        source (Path): The source path that was moved
        destination (Path): The destination path where the item was moved to
        recipient (str): Email address of the recipient

    Raises:
        smtplib.SMTPException: If there's an error sending the email
    """
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
    msg["To"] = recipient
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

def parse_args():
    """
    Parse command line arguments for the file mover.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Move files or directories with optional email notifications")
    parser.add_argument("source", help="Source file or directory to move")
    parser.add_argument("destination", help="Destination path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-f", "--force", action="store_true", help="Force overwrite if destination exists")
    parser.add_argument("--email", nargs="?", const=True, help="Send email notification (optionally specify recipient)")
    return parser.parse_args()

def move_path(source: Path, destination: Path, force: bool, verbose: bool):
    """
    Move a file or directory from source to destination.

    Args:
        source (Path): Source path to move
        destination (Path): Destination path
        force (bool): If True, overwrite destination if it exists
        verbose (bool): If True, print detailed output

    Raises:
        FileNotFoundError: If source path does not exist
        FileExistsError: If destination exists and force is False
    """
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
    """
    Main entry point for the file mover.

    Parses arguments and performs the file/directory move operation.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    args = parse_args()
    source = Path(args.source)
    destination = Path(args.destination)

    try:
        move_path(source, destination, args.force, args.verbose)

        if args.email:
            recipient = args.email if isinstance(args.email, str) else input("📧 Enter recipient email address: ").strip()
            if not recipient:
                raise ValueError("Recipient email address is required when using --email")
            send_email_notification(source, destination, recipient)

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())