"""
directory_monitor.py

Monitors a specified directory for new files and logs their creation.

Functions:
    setup_logger(): Sets up the logging configuration
    get_existing_files(directory): Gets current files in directory
    monitor_directory(directory, interval): Monitors directory for new files
    main(): Main function to run the directory monitor

Command Line Usage Examples:
    python directory_monitor.py /path/to/directory
    python directory_monitor.py /path/to/directory --interval 5
"""

import os
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime

def setup_logger() -> logging.Logger:
    """
    Sets up the logging configuration.

    Parameters:
        None

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)

    # Configure logging
    log_file = logs_dir / f"directory_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def get_existing_files(directory: Path) -> set:
    """
    Gets the current files in the specified directory.

    Parameters:
        directory (Path): Path to the directory to monitor

    Returns:
        set: Set of existing files in the directory
    """
    logger = logging.getLogger(__name__)
    try:
        existing_files = {file.name for file in directory.iterdir() if file.is_file()}
        logger.debug(f"Found {len(existing_files)} existing files")
        return existing_files
    except PermissionError:
        logger.error(f"Permission denied accessing directory: {directory}")
        raise
    except Exception as e:
        logger.error(f"Error accessing directory {directory}: {e}")
        raise

def monitor_directory(directory: Path, interval: int = 1) -> None:
    """
    Monitors the specified directory for new files.

    Parameters:
        directory (Path): Path to the directory to monitor
        interval (int): Monitoring interval in seconds, defaults to 1

    Returns:
        None
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Starting directory monitoring of: {directory}")
    logger.debug(f"Monitoring interval: {interval} seconds")

    try:
        existing_files = get_existing_files(directory)
        
        while True:
            try:
                # Get current files
                current_files = {file.name for file in directory.iterdir() if file.is_file()}
                
                # Find new files
                new_files = current_files - existing_files
                
                # Log new files
                for file_name in new_files:
                    file_path = directory / file_name
                    creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                    logger.info(f"New file detected: {file_name} | Created: {creation_time}")
                
                # Update existing files
                existing_files = current_files
                
                # Wait for next check
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error during monitoring: {e}")
                time.sleep(interval)  # Wait before retrying
                
    except Exception as e:
        logger.error(f"Fatal error in monitoring: {e}")
        raise

def main():
    """
    Main function to run the directory monitor.

    Parameters:
        None

    Returns:
        None
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Monitor a directory for new files.')
    parser.add_argument('directory', help='Directory to monitor')
    parser.add_argument('--interval', type=int, default=1, help='Monitoring interval in seconds')
    
    args = parser.parse_args()
    
    # Setup logger
    logger = setup_logger()
    
    try:
        # Convert directory to Path object and verify it exists
        directory = Path(args.directory)
        if not directory.exists():
            logger.error(f"Directory does not exist: {directory}")
            return
        if not directory.is_dir():
            logger.error(f"Path is not a directory: {directory}")
            return
            
        # Start monitoring
        monitor_directory(directory, args.interval)
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    main()