"""
Centralized logging module for the file manager system.

This module provides a centralized logging solution that:
- Logs to both file and console
- Supports different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Includes timestamps in log messages
- Rotates log files to prevent excessive growth
- Provides structured logging with operation context
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

# Constants
LOG_FILE = "file_manager.log"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Create logs directory if it doesn't exist
logs_dir = Path(__file__).parent / "logs"
logs_dir.mkdir(exist_ok=True)

class AppLogger:
    """
    Centralized logger for file manager operations.
    
    Usage:
    ```python
    logger = FileManagerLogger()
    logger.info("Operation completed successfully")
    logger.error("Failed to perform operation", extra={"operation": "create_file"})
    ```
    """
    
    def __init__(self, name: str = "file_manager"):
        """
        Initialize the logger with both file and console handlers.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            logs_dir / LOG_FILE,
            maxBytes=MAX_LOG_SIZE,
            backupCount=LOG_BACKUP_COUNT
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter with timestamp and operation context
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(operation)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def debug(self, message: str, extra: dict = None):
        """Log a debug message."""
        self._log(logging.DEBUG, message, extra)
        
    def info(self, message: str, extra: dict = None):
        """Log an info message."""
        self._log(logging.INFO, message, extra)
        
    def warning(self, message: str, extra: dict = None):
        """Log a warning message."""
        self._log(logging.WARNING, message, extra)
        
    def error(self, message: str, extra: dict = None):
        """Log an error message."""
        self._log(logging.ERROR, message, extra)
        
    def critical(self, message: str, extra: dict = None):
        """Log a critical message."""
        self._log(logging.CRITICAL, message, extra)
        
    def _log(self, level: int, message: str, extra: dict = None):
        """Helper method to log messages with operation context."""
        if extra is None:
            extra = {}
        
        # Add default operation context if not provided
        if 'operation' not in extra:
            extra['operation'] = 'unknown'
        
        self.logger.log(level, message, extra=extra)

# Create a global instance for easy access
logger = AppLogger()

# Example usage:
if __name__ == "__main__":
    logger.info("Logger initialized successfully")
    logger.warning("This is a warning message", extra={"operation": "test"})
    logger.error("This is an error message", extra={"operation": "test"})
    logger.critical("This is a critical message", extra={"operation": "test"})
