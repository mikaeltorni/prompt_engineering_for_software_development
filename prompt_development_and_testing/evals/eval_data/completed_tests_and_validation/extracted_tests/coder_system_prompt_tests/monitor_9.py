"""
directory_monitor.py

Monitors a specified directory for new files and logs their creation.

Functions:
    setup_logging(): Sets up logging configuration
    validate_directory(dir_path: str) -> Path: Validates directory path
    get_existing_files(dir_path: Path) -> set: Gets existing files in directory
    monitor_directory(dir_path: str): Main monitoring function

Command Line Usage Examples:
    python directory_monitor.py
    python directory_monitor.py /path/to/monitor
"""

import logging
from pathlib import Path
import time
from datetime import datetime
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(funcName)s: %(message)s',
    handlers=[
        logging.FileHandler('directory_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def setup_logging() -> None:
    """
    Sets up logging configuration.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Setting up logging configuration")
    try:
        # Ensure log directory exists
        log_file = Path('directory_monitor.log')
        log_file.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to setup logging: {e}")
        sys.exit(1)

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
            raise FileNotFoundError(f"Directory does not exist: {dir_path}")
        if not path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {dir_path}")
        if not path.is_absolute():
            path = path.absolute()
        return path
    except Exception as e:
        logger.error(f"Directory validation failed: {e}")
        raise

def get_existing_files(dir_path: Path) -> set:
    """
    Gets the set of existing files in the directory.

    Parameters:
        dir_path (Path): Path object of the directory to scan

    Returns:
        set: Set of existing file paths
    """
    logger.debug(f"Getting existing files in: {dir_path}")
    
    try:
        return {f.name for f in dir_path.glob('*') if f.is_file()}
    except Exception as e:
        logger.error(f"Failed to get existing files: {e}")
        raise

def monitor_directory(dir_path: str) -> None:
    """
    Monitors the specified directory for new files.

    Parameters:
        dir_path (str): Path to the directory to monitor

    Returns:
        None
    """
    logger.info(f"Starting directory monitoring for: {dir_path}")
    
    try:
        # Validate directory
        path = validate_directory(dir_path)
        
        # Get initial state
        existing_files = get_existing_files(path)
        logger.info(f"Initial file count: {len(existing_files)}")
        
        print("\nMonitoring directory for new files... Press Ctrl+C to stop.")
        
        while True:
            # Get current files
            current_files = get_existing_files(path)
            
            # Check for new files
            new_files = current_files - existing_files
            if new_files:
                for file_name in new_files:
                    file_path = path / file_name
                    creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                    logger.info(f"New file detected: {file_name} | Created: {creation_time}")
                
                # Update existing files
                existing_files = current_files
            
            # Sleep before next check
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
        print("\nMonitoring stopped.")
    except Exception as e:
        logger.error(f"Monitoring failed: {e}")
        raise

def main():
    """
    Main function to run the directory monitor.

    Parameters:
        None

    Returns:
        None
    """
    try:
        # Setup logging
        setup_logging()
        
        while True:
            # Get directory path from user
            print("\nDirectory Monitor")
            print("================")
            dir_path = input("Enter directory path to monitor (or 'quit' to exit): ").strip()
            
            if dir_path.lower() == 'quit':
                logger.info("Program terminated by user")
                break
            
            # Start monitoring
            monitor_directory(dir_path)
            
    except Exception as e:
        logger.error(f"Program failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()