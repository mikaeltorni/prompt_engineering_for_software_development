"""
directory_monitor.py

Monitors a specified directory for new files and logs their creation.

Functions:
    setup_logging(): Sets up logging configuration
    validate_directory(dir_path: str) -> Path: Validates the input directory path
    monitor_directory(dir_path: Path) -> None: Monitors directory for new files
    get_initial_files(dir_path: Path) -> set: Gets initial set of files in directory

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
    Validates the input directory path.

    Parameters:
        dir_path (str): Path to the directory to monitor

    Returns:
        Path: Validated Path object for the directory
    """
    logger.debug(f"Validating directory path: {dir_path}")
    
    try:
        path = Path(dir_path)
        if not path.exists():
            raise FileNotFoundError(f"Directory does not exist: {dir_path}")
        if not path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {dir_path}")
        if not path.is_absolute():
            path = path.absolute()
        
        logger.debug(f"Directory validated: {path}")
        return path
    
    except Exception as e:
        logger.error(f"Directory validation failed: {e}")
        raise

def get_initial_files(dir_path: Path) -> set:
    """
    Gets the initial set of files in the directory.

    Parameters:
        dir_path (Path): Path to the directory to monitor

    Returns:
        set: Set of initial files in the directory
    """
    logger.debug(f"Getting initial files from: {dir_path}")
    
    try:
        initial_files = {f.name for f in dir_path.glob('*') if f.is_file()}
        logger.debug(f"Found {len(initial_files)} initial files")
        return initial_files
    
    except Exception as e:
        logger.error(f"Failed to get initial files: {e}")
        raise

def monitor_directory(dir_path: Path) -> None:
    """
    Monitors directory for new files.

    Parameters:
        dir_path (Path): Path to the directory to monitor

    Returns:
        None
    """
    logger.info(f"Starting directory monitoring for: {dir_path}")
    
    try:
        # Get initial state
        known_files = get_initial_files(dir_path)
        
        while True:
            # Get current files
            current_files = {f.name for f in dir_path.glob('*') if f.is_file()}
            
            # Check for new files
            new_files = current_files - known_files
            
            # Log new files
            for file_name in new_files:
                file_path = dir_path / file_name
                creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                logger.info(f"New file detected: {file_name} | Created: {creation_time}")
            
            # Update known files
            known_files = current_files
            
            # Sleep before next check
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Monitoring error: {e}")
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
        
        # Get directory path from user
        while True:
            dir_path = input("Enter directory path to monitor (or 'quit' to exit): ").strip()
            
            if dir_path.lower() == 'quit':
                logger.info("Program terminated by user")
                break
            
            try:
                # Validate directory
                validated_path = validate_directory(dir_path)
                
                # Start monitoring
                monitor_directory(validated_path)
                
            except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
                logger.error(f"Invalid directory: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                continue
            
    except Exception as e:
        logger.error(f"Program error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()