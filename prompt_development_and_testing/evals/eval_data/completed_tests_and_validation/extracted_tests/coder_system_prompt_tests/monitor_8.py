"""
directory_monitor.py

Monitors a specified directory for new files and logs their creation.

Functions:
    setup_logging(): Sets up logging configuration
    get_existing_files(directory): Gets current files in directory
    monitor_directory(directory, interval): Monitors directory for new files
    validate_directory(directory): Validates if directory exists and is accessible

Command Line Usage Examples:
    python directory_monitor.py
    python directory_monitor.py --directory /path/to/monitor --interval 5
"""

import os
import time
from pathlib import Path
import logging
from datetime import datetime
import argparse
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
            logging.StreamHandler(sys.stdout)
        ]
    )

def validate_directory(directory: str) -> Path:
    """
    Validates if the specified directory exists and is accessible.

    Parameters:
        directory (str): Path to the directory to validate

    Returns:
        Path: Path object of validated directory
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Validating directory: {directory}")

    try:
        path = Path(directory)
        if not path.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory}")
        if not path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {directory}")
        if not os.access(path, os.R_OK):
            raise PermissionError(f"No read permission for directory: {directory}")
        
        logger.debug("Directory validation successful")
        return path
    
    except Exception as e:
        logger.error(f"Directory validation failed: {str(e)}")
        raise

def get_existing_files(directory: Path) -> set:
    """
    Gets the set of existing files in the specified directory.

    Parameters:
        directory (Path): Path object of directory to scan

    Returns:
        set: Set of filenames in the directory
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Scanning directory: {directory}")

    try:
        files = {file.name for file in directory.iterdir() if file.is_file()}
        logger.debug(f"Found {len(files)} existing files")
        return files
    
    except Exception as e:
        logger.error(f"Error scanning directory: {str(e)}")
        raise

def monitor_directory(directory: str, interval: int = 1) -> None:
    """
    Monitors a directory for new files and logs when they are detected.

    Parameters:
        directory (str): Path to the directory to monitor
        interval (int): Monitoring interval in seconds, default 1

    Returns:
        None
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Starting directory monitoring of: {directory}")
    logger.info(f"Monitoring interval: {interval} seconds")

    try:
        # Validate directory and get Path object
        dir_path = validate_directory(directory)
        
        # Get initial set of files
        existing_files = get_existing_files(dir_path)
        
        while True:
            try:
                # Get current set of files
                current_files = get_existing_files(dir_path)
                
                # Find new files
                new_files = current_files - existing_files
                
                # Log any new files
                for file in new_files:
                    file_path = dir_path / file
                    creation_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                    logger.info(f"New file detected: {file} | Created: {creation_time}")
                
                # Update existing files
                existing_files = current_files
                
                # Wait for next check
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error during monitoring: {str(e)}")
                time.sleep(interval)  # Wait before retrying
                
    except Exception as e:
        logger.error(f"Fatal error in monitoring: {str(e)}")
        raise

def main():
    """
    Main function to set up argument parsing and start monitoring.

    Parameters:
        None

    Returns:
        None
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Monitor directory for new files.')
    parser.add_argument('--directory', '-d', type=str, default='.',
                      help='Directory to monitor (default: current directory)')
    parser.add_argument('--interval', '-i', type=int, default=1,
                      help='Monitoring interval in seconds (default: 1)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    try:
        # Start monitoring
        monitor_directory(args.directory, args.interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()