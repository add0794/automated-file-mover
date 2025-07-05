"""
cli.py - Command-line interface for FileManager operations.

This script allows you to interact with the FileManager class using subcommands like:
create-file, create-folder, move, rename, delete, and view.

Each command optionally supports email notifications using --email, --sender, --recipient, and --password.

Example usage:
    python cli.py create-file notes.txt --text "Hello" --remove e
    python cli.py create-folder Archive
    python cli.py move notes.txt Archive/
    python cli.py rename oldname.txt newname.txt
    python cli.py delete Archive/notes.txt
    python cli.py view Archive/notes.txt

    With email:
    python cli.py move notes.txt Archive/ --email --sender me@example.com --recipient you@example.com
"""

import argparse
from manager import FileManager
import getpass
from logger import logger


def add_common_args(subparser):
    """
    Adds shared email notification arguments to each subparser.
    """
    subparser.add_argument(
        "--email",
        nargs="?",
        const=True,
        help="Send email update to self or another user"
    )
    subparser.add_argument("--sender", help="Sender email address")
    subparser.add_argument("--recipient", help="Recipient email address")

def main():
    parser = argparse.ArgumentParser(description="FileManager CLI utility")
    subparsers = parser.add_subparsers(dest="command")

    # Create file
    create_file = subparsers.add_parser("create-file", help="Create a new file")
    create_file.add_argument("name", help="File name")
    create_file.add_argument("--text", help="Optional file content")
    create_file.add_argument("--remove", help="Characters to remove from content")
    add_common_args(create_file)

    # Create folder
    create_folder = subparsers.add_parser("create-folder", help="Create a new folder")
    create_folder.add_argument("name", help="Folder name")
    add_common_args(create_folder)

    # Move
    move = subparsers.add_parser("move", help="Move a file or folder")
    move.add_argument("source", help="Source path")
    move.add_argument("destination", help="Destination path")
    add_common_args(move)

    # Rename
    rename = subparsers.add_parser("rename", help="Rename a file or folder")
    rename.add_argument("old", help="Old path")
    rename.add_argument("new", help="New path")
    add_common_args(rename)

    # Delete
    delete = subparsers.add_parser("delete", help="Delete a file or folder")
    delete.add_argument("name", help="File or folder to delete")
    add_common_args(delete)

    # View
    view = subparsers.add_parser("view", help="View contents of a file or folder")
    view.add_argument("name", help="File or folder to view")
    add_common_args(view)

    args = parser.parse_args()
    fm = FileManager()

    try:
        if args.command == "create-file":
            result = fm.create_file(args.name, content=args.text, remove_chars=args.remove)
            logger.info(f"Created file: {result}", extra={"operation": "cli_create_file"})
            print(f"✅ Created file: {result}")
        elif args.command == "create-folder":
            result = fm.create_folder(args.name)
            logger.info(f"Created folder: {result}", extra={"operation": "cli_create_folder"})
            print(f"📁 Created folder: {result}")
        elif args.command == "move":
            result = fm.move(args.source, args.destination)
            logger.info(f"Moved {args.source} to {result}", extra={"operation": "cli_move"})
            print(f"🚚 Moved to: {result}")
        elif args.command == "rename":
            result = fm.rename(args.old, args.new)
            logger.info(f"Renamed {args.old} to {result}", extra={"operation": "cli_rename"})
            print(f"✏️ Renamed to: {result}")
        elif args.command == "delete":
            fm.delete(args.name)
            logger.info(f"Deleted: {args.name}", extra={"operation": "cli_delete"})
            print(f"🗑 Deleted: {args.name}")
        elif args.command == "view":
            content = fm.view(args.name)
            logger.info(f"Viewed: {args.name}", extra={"operation": "cli_view"})
            print(content)
        else:
            parser.print_help()
            return

        # Optional email notification
        if args.email:
            sender = args.sender or input("📤 Enter sender email: ").strip()
            recipient = args.recipient or input("📥 Enter recipient email: ").strip()
            password = getpass.getpass("🔑 Enter sender email password (input hidden): ")

            fm.email_notification(
                result if "result" in locals() else args.name,
                sender,
                recipient,
                password
            )

    except Exception as e:
        logger.error(f"CLI Error: {str(e)}", extra={"operation": "cli_error"})
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
