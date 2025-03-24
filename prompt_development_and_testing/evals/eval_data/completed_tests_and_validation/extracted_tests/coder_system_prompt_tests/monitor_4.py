"""
directory_monitor.py

Monitors a specified directory for new files and logs their creation.

Functions:
    setup_logging(): Sets up logging configuration
    validate_directory(dir_path: str) -> Path: Validates directory path
    monitor_directory(dir_path: str): Monitors directory for changes
    handle_directory_events(event): Handles directory events

Command Line Usage Examples:
    python directory_monitor.py /path/to/directory
    python directory_monitor.py C:/Users/Documents
"""

import logging
import sys
import time
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(funcName)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('directory_monitor.log')
    ]
)

logger = logging.getLogger(__name__)

class FileEventHandler(FileSystemEventHandler):
    """Custom file event handler."""
    
    def on_created(self, event: FileSystemEvent) -> None:
        """
        Handles file creation events.

        Parameters:
            event (FileSystemEvent): The file system event that occurred

        Returns:
            None
        """
        if not event.is_directory:
            file_path = Path(event.src_path)
            creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
            logger.info(f"New file detected | Name: {file_path.name} | Created: {creation_time}")

def validate_directory(dir_path: str) -> Path:
    """
    Validates if the provided directory path exists and is accessible.

    Parameters:
        dir_path (str): Path to the directory to monitor

    Returns:
        Path: Validated Path object for the directory

    Raises:
        ValueError: If directory path is invalid or inaccessible
    """
    logger.debug(f"Validating directory: {dir_path}")
    
    try:
        path = Path(dir_path)
        if not path.exists():
            raise ValueError(f"Directory does not exist: {dir_path}")
        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {dir_path}")
        if not path.is_absolute():
            path = path.absolute()
            
        logger.debug(f"Directory validated: {path}")
        return path
    
    except Exception as e:
        logger.error(f"Error validating directory: {e}")
        raise ValueError(f"Invalid directory path: {e}")

def monitor_directory(dir_path: str) -> None:
    """
    Monitors a directory for new files.

    Parameters:
        dir_path (str): Path to the directory to monitor

    Returns:
        None
    """
    try:
        # Validate directory
        validated_path = validate_directory(dir_path)
        logger.info(f"Starting directory monitoring for: {validated_path}")

        # Set up the observer
        event_handler = FileEventHandler()
        observer = Observer()
        observer.schedule(event_handler, str(validated_path), recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
            observer.stop()
            observer.join()
            
    except Exception as e:
        logger.error(f"Error monitoring directory: {e}")
        sys.exit(1)

def main():
    """
    Main function to run the directory monitor.

    Parameters:
        None

    Returns:
        None
    """
    try:
        if len(sys.argv) != 2:
            logger.error("Please provide the directory path as an argument")
            print("Usage: python directory_monitor.py <directory_path>")
            sys.exit(1)

        directory_path = sys.argv[1]
        monitor_directory(directory_path)

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()