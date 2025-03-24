import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class FileMonitor(FileSystemEventHandler):
    def __init__(self, log_file):
        """Initialize the FileMonitor with a log file."""
        super().__init__()
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # Also print to console
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Keep track of processed files
        self.processed_files = set()

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        try:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            
            # Check if we've already processed this file
            if file_path in self.processed_files:
                return
                
            # Get file creation time
            creation_time = os.path.getctime(file_path)
            creation_datetime = datetime.fromtimestamp(creation_time)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Log file details
            self.logger.info(
                f"New file detected:\n"
                f"  Name: {file_name}\n"
                f"  Path: {file_path}\n"
                f"  Creation Time: {creation_datetime}\n"
                f"  Size: {self.format_size(file_size)}"
            )
            
            # Add to processed files
            self.processed_files.add(file_path)
            
        except Exception as e:
            self.logger.error(f"Error processing file {event.src_path}: {str(e)}")

    def format_size(self, size):
        """Convert size in bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

def monitor_directory(directory_path, log_file):
    """
    Monitor a directory for new files.
    
    Args:
        directory_path (str): Path to the directory to monitor
        log_file (str): Path to the log file
    """
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")

        # Initialize the file monitor
        event_handler = FileMonitor(log_file)
        observer = Observer()
        observer.schedule(event_handler, directory_path, recursive=False)
        observer.start()

        print(f"Started monitoring directory: {directory_path}")
        print(f"Logging to: {log_file}")
        print("Press Ctrl+C to stop monitoring...")

        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\nMonitoring stopped.")

        observer.join()

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Configuration
    DIRECTORY_TO_MONITOR = "monitored_directory"  # Change this to your desired directory
    LOG_FILE = "file_monitor.log"  # Change this to your desired log file path
    
    # Start monitoring
    monitor_directory(DIRECTORY_TO_MONITOR, LOG_FILE)