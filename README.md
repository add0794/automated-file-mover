# Automated File Mover

A Python-based file organization system that watches a designated directory and automatically moves files to specified locations.

## Features

- Watches a specified directory for new files/folders
- Interactive prompt for moving files to desired locations
- Retry mechanism for failed moves
- Comprehensive logging
- Handles both files and directories
- Skips system folders and hidden files
- Python-based implementation with modern libraries

## Installation

1. Clone the repository:
```bash
git clone https://github.com/add0794/automated-file-mover.git
cd automated-file-mover
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Create the watch directory (if it doesn't exist):
```bash
mkdir -p ~/WatchZone
```

2. Run the watcher:
```bash
python watch_home_and_prompt.py
```

The script will start watching the `~/WatchZone` directory. When new files or folders appear:
1. You'll be prompted to specify a destination path inside your home directory
2. The script will attempt to move the file/folder
3. If the move fails, you'll be asked if you want to try again with a different destination

## Configuration

The script watches the `~/WatchZone` directory by default. This can be changed by modifying the `WATCH_DIR` variable in `watch_home_and_prompt.py`.

## Logging

The script logs all operations to `watch_home.log` in the project directory. The log includes:
- Timestamps
- Operation status (success/failure)
- Retry attempts
- User interactions

## Requirements

- Python 3.8+
- Required packages (listed in requirements.txt):
  - watchdog
  - python-dotenv

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