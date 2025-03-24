"""
directory_monitor.py

Monitors a specified directory for new files and logs their creation details.

Functions:
    setup_logging(): Sets up logging configuration
    validate_directory(dir_path: str) -> Path: Validates directory path
    monitor_directory(directory: Path): Monitors directory for changes
    handle_new_file(file_path: Path): Handles new file detection

Command Line Usage Examples:
    python directory_monitor.py /path/to/monitor
    python directory_monitor.py C:\\Users\\Documents\\monitor
    python directory_monitor.py /home/user/downloads --log-file custom.log
"""

import logging
import time
from pathlib import Path
import argparse
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class FileEventHandler(FileSystemEventHandler):
    """Custom file event handler for monitoring directory changes."""
    
    def on_created(self, event):
        """
        Handles file creation events.

        Parameters:
            event: The file system event that occurred

        Returns:
            None
        """
        if not event.is_directory:
            file_path = Path(event.src_path)
            handle_new_file(file_path)

def setup_logging(log_file: str = "directory_monitor.log") -> None:
    """
    Sets up logging configuration.

    Parameters:
        log_file (str): Path to the log file

    Returns:
        None
    """
    try:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        )
        logger.addHandler(file_handler)
        logger.debug(f"Logging setup complete. Log file: {log_file}")
    except Exception as e:
        logger.error(f"Failed to setup logging: {e}")
        raise

def validate_directory(dir_path: str) -> Path:
    """
    Validates if the provided directory path exists and is accessible.

    Parameters:
        dir_path (str): Path to the directory to monitor

    Returns:
        Path: Validated Path object for the directory
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
        logger.error(f"Directory validation failed: {e}")
        raise

def handle_new_file(file_path: Path) -> None:
    """
    Handles the detection of a new file.

    Parameters:
        file_path (Path): Path to the new file

    Returns:
        None
    """
    try:
        creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
        file_size = file_path.stat().st_size
        
        logger.info(
            f"New file detected: {file_path.name} | "
            f"Created: {creation_time} | "
            f"Size: {file_size} bytes"
        )
    except Exception as e:
        logger.error(f"Error handling new file {file_path}: {e}")

def monitor_directory(directory: Path) -> None:
    """
    Sets up and starts directory monitoring.

    Parameters:
        directory (Path): Path to the directory to monitor

    Returns:
        None
    """
    logger.info(f"Starting directory monitoring: {directory}")
    
    try:
        event_handler = FileEventHandler()
        observer = Observer()
        observer.schedule(event_handler, str(directory), recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
            observer.stop()
            
        observer.join()
    except Exception as e:
        logger.error(f"Error during directory monitoring: {e}")
        raise

def main():
    """
    Main function to set up argument parsing and start monitoring.

    Parameters:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Monitor a directory for new files"
    )
    parser.add_argument(
        "directory",
        help="Directory path to monitor"
    )
    parser.add_argument(
        "--log-file",
        default="directory_monitor.log",
        help="Path to log file (default: directory_monitor.log)"
    )
    
    args = parser.parse_args()
    
    try:
        setup_logging(args.log_file)
        directory = validate_directory(args.directory)
        monitor_directory(directory)
    except Exception as e:
        logger.error(f"Application error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())