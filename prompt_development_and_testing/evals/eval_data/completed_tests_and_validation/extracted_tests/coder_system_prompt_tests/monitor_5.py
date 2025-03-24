"""
directory_monitor.py

Monitors a specified directory for new files and logs their creation.

Functions:
    setup_logging(): Sets up logging configuration
    validate_directory(directory_path: str) -> Path: Validates the directory path
    get_existing_files(directory_path: Path) -> set: Gets existing files in directory
    monitor_directory(directory_path: Path, interval: int): Monitors directory for new files

Command Line Usage Examples:
    python directory_monitor.py
    python directory_monitor.py --interval 5
"""

import logging
from pathlib import Path
import time
from datetime import datetime
import sys

def setup_logging() -> None:
    """
    Sets up logging configuration.

    Parameters:
        None

    Returns:
        None
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s:%(funcName)s: %(message)s',
        handlers=[
            logging.FileHandler('directory_monitor.log'),
            logging.StreamHandler()
        ]
    )

def validate_directory(directory_path: str) -> Path:
    """
    Validates if the provided directory path exists and is accessible.

    Parameters:
        directory_path (str): Path to the directory to monitor

    Returns:
        Path: Validated Path object for the directory
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Validating directory: {directory_path}")

    try:
        path = Path(directory_path)
        if not path.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory_path}")
        if not path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {directory_path}")
        if not os.access(path, os.R_OK):
            raise PermissionError(f"No read permission for directory: {directory_path}")
        
        logger.debug(f"Directory validated successfully: {path}")
        return path

    except Exception as e:
        logger.error(f"Directory validation failed: {str(e)}")
        raise

def get_existing_files(directory_path: Path) -> set:
    """
    Gets the set of existing files in the directory.

    Parameters:
        directory_path (Path): Path to the directory

    Returns:
        set: Set of existing file paths
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Getting existing files from: {directory_path}")

    try:
        files = {str(f) for f in directory_path.glob('*') if f.is_file()}
        logger.debug(f"Found {len(files)} existing files")
        return files

    except Exception as e:
        logger.error(f"Error getting existing files: {str(e)}")
        raise

def monitor_directory(directory_path: Path, interval: int) -> None:
    """
    Monitors the directory for new files.

    Parameters:
        directory_path (Path): Path to monitor
        interval (int): Monitoring interval in seconds

    Returns:
        None
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Starting directory monitoring of: {directory_path}")
    logger.info(f"Monitoring interval: {interval} seconds")

    try:
        # Get initial set of files
        existing_files = get_existing_files(directory_path)

        while True:
            # Get current set of files
            current_files = get_existing_files(directory_path)
            
            # Find new files
            new_files = current_files - existing_files
            
            # Log new files
            for file_path in new_files:
                file = Path(file_path)
                creation_time = datetime.fromtimestamp(file.stat().st_ctime)
                logger.info(f"New file detected: {file.name} | Created: {creation_time}")
            
            # Update existing files
            existing_files = current_files
            
            # Wait for next check
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Error during monitoring: {str(e)}")
        raise

def main():
    """
    Main function to run the directory monitor.

    Parameters:
        None

    Returns:
        None
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Get directory path from user
        while True:
            directory_path = input("Enter directory path to monitor (or 'quit' to exit): ")
            
            if directory_path.lower() == 'quit':
                logger.info("Program terminated by user")
                sys.exit(0)

            try:
                # Get and validate monitoring interval
                interval = input("Enter monitoring interval in seconds (default: 5): ").strip()
                interval = int(interval) if interval else 5

                if interval < 1:
                    logger.warning("Invalid interval. Using default of 5 seconds")
                    interval = 5

                # Validate directory and start monitoring
                valid_path = validate_directory(directory_path)
                monitor_directory(valid_path, interval)

            except ValueError:
                logger.error("Invalid interval value. Please enter a valid number")
            except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
                logger.error(str(e))
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")

    except KeyboardInterrupt:
        logger.info("Program terminated by user")
        sys.exit(0)

if __name__ == "__main__":
    main()