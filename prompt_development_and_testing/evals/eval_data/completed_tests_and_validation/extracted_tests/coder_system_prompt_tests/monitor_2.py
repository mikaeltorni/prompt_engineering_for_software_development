"""
directory_monitor.py

Monitors a specified directory for new files and logs their creation.

Functions:
    setup_logging(): Sets up logging configuration
    validate_directory(dir_path: str) -> Path: Validates directory path
    get_initial_files(dir_path: Path) -> set: Gets initial set of files
    monitor_directory(dir_path: Path, interval: int): Monitors directory for changes

Command Line Usage Examples:
    python directory_monitor.py /path/to/directory
    python directory_monitor.py /path/to/directory --interval 5
    python directory_monitor.py /path/to/directory --interval 10 --log-file custom.log
"""

import logging
from pathlib import Path
import time
import argparse
from datetime import datetime
import sys

def setup_logging(log_file: str = "directory_monitor.log") -> None:
    """
    Sets up logging configuration.

    Parameters:
        log_file (str): Path to the log file, defaults to 'directory_monitor.log'

    Returns:
        None
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.debug(f"Logging setup complete. Writing to {log_file}")

def validate_directory(dir_path: str) -> Path:
    """
    Validates if the provided directory path exists and is accessible.

    Parameters:
        dir_path (str): Path to the directory to monitor

    Returns:
        Path: Validated Path object for the directory

    Raises:
        ValueError: If directory doesn't exist or isn't accessible
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Validating directory: {dir_path}")

    path = Path(dir_path)
    if not path.exists():
        logger.error(f"Directory does not exist: {dir_path}")
        raise ValueError(f"Directory does not exist: {dir_path}")
    if not path.is_dir():
        logger.error(f"Path is not a directory: {dir_path}")
        raise ValueError(f"Path is not a directory: {dir_path}")
    if not path.is_absolute():
        path = path.absolute()

    logger.debug(f"Directory validated: {path}")
    return path

def get_initial_files(dir_path: Path) -> set:
    """
    Gets the initial set of files in the directory.

    Parameters:
        dir_path (Path): Path to the directory to monitor

    Returns:
        set: Set of file paths in the directory
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Getting initial files from: {dir_path}")
    
    files = set(path for path in dir_path.glob('*') if path.is_file())
    logger.debug(f"Found {len(files)} files initially")
    return files

def monitor_directory(dir_path: Path, interval: int) -> None:
    """
    Monitors the directory for new files.

    Parameters:
        dir_path (Path): Path to the directory to monitor
        interval (int): Monitoring interval in seconds

    Returns:
        None
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Starting directory monitoring of: {dir_path}")
    logger.info(f"Monitoring interval: {interval} seconds")

    try:
        known_files = get_initial_files(dir_path)
        
        while True:
            current_files = set(path for path in dir_path.glob('*') if path.is_file())
            new_files = current_files - known_files

            for new_file in new_files:
                creation_time = datetime.fromtimestamp(new_file.stat().st_ctime)
                logger.info(f"New file detected: {new_file.name} | Created: {creation_time}")

            known_files = current_files
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"An error occurred during monitoring: {e}")
        raise

def main():
    """
    Main function to set up argument parsing and start monitoring.

    Parameters:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Monitor a directory for new files.")
    parser.add_argument("directory", help="Directory path to monitor")
    parser.add_argument("--interval", type=int, default=1,
                      help="Monitoring interval in seconds (default: 1)")
    parser.add_argument("--log-file", default="directory_monitor.log",
                      help="Log file path (default: directory_monitor.log)")

    args = parser.parse_args()

    try:
        setup_logging(args.log_file)
        logger = logging.getLogger(__name__)
        logger.info("Starting directory monitor")
        
        dir_path = validate_directory(args.directory)
        monitor_directory(dir_path, args.interval)

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()