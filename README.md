🗂# Automated File Watcher

A Python script that watches a directory (~/WatchZone) for new files or folders, prompts the user for a destination path, and moves the items with optional email notifications.

## Features

- 🔄 Real-time file and folder monitoring
- 📦 Interactive destination path selection
- 📧 Optional email notifications
- 🛡️ Robust error handling via subprocess
- 📄 Works for both files and directories
- 📝 Comprehensive logging to file and console
- 💡 Unicode emoji support for clear feedback
- 🧹 Clean exit on Ctrl+C or user input
- 🔐 Uses .env for secure credentials

## Installation

```bash
git clone https://github.com/add0794/automated-file-watcher.git
cd automated-file-watcher
```

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Ensure the watch directory exists:

```bash
mkdir -p ~/WatchZone
```

2. Start the watcher:

```bash
python watch_home_and_prompt.py
```

## How It Works

1. The script monitors ~/WatchZone for new files/folders
2. When something appears:
   - You'll be prompted to choose a destination in your home directory
   - Options:
     - Type a relative path (e.g., Documents/notes)
     - Press Enter to skip
     - Type 'exit' to quit
   - You'll be asked if you'd like to receive an email notification
   - The file will be moved using file_mover.py
   - Success/failure will be logged and shown in the terminal

## Configuration

Create a `.env` file in the project root with:

```ini
EMAIL_SENDER=your-email@example.com
EMAIL_PASSWORD=your-app-specific-password
```

These credentials are used to send email notifications via SMTP (e.g., Gmail with app passwords).

## Logging

All events are logged to both:
- `watch_home.log` file
- Console output

Log details include:
- Timestamps
- File/folder detection
- Destination paths
- Move status (success/failure)
- Error details (if any)

## Error Handling

- Invalid emails are rejected
- File move failures are logged with detailed output
- Subprocess errors are safely handled
- Unicode emoji are used for clarity
- Signal interruptions (Ctrl+C) are caught and safely terminated

## Exit Options

You can stop the watcher by:
- Typing 'exit' when prompted
- Pressing Ctrl+C in the terminal

## Requirements

- Python 3.8+
- Required packages (listed in requirements.txt):
  - watchdog
  - python-dotenv

## Optional: Using fswatch Directly

If you prefer to monitor file changes outside Python:

```bash
# Watch recursively
fswatch -r ~/WatchZone

# Exclude .git directory
fswatch -r -e "\.git" ~/WatchZone

# Watch only .txt files
fswatch -r -i "\.txt$" ~/WatchZone
```

For more options, see: https://github.com/emcrisostomo/fswatch/wiki

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For support, please open an issue in the GitHub repository.