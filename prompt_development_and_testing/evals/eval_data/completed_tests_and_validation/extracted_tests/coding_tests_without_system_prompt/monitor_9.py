import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import logging

class FileMonitor(FileSystemEventHandler):
    def __init__(self, log_file):
        """Initialize the file monitor with a log file."""
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

    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            file_path = event.src_path
            creation_time = self.get_file_creation_time(file_path)
            file_size = self.get_file_size(file_path)
            
            log_message = (
                f"New file detected!\n"
                f"File: {os.path.basename(file_path)}\n"
                f"Path: {file_path}\n"
                f"Creation Time: {creation_time}\n"
                f"Size: {self.format_size(file_size)}\n"
                f"{'-'*50}"
            )
            
            self.logger.info(log_message)

    def get_file_creation_time(self, file_path):
        """Get the creation time of a file."""
        timestamp = os.path.getctime(file_path)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def get_file_size(self, file_path):
        """Get the size of a file in bytes."""
        return os.path.getsize(file_path)

    def format_size(self, size):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

def start_monitoring(directory_path, log_file):
    """Start monitoring the specified directory."""
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")

        # Create an observer and file monitor
        event_handler = FileMonitor(log_file)
        observer = Observer()
        observer.schedule(event_handler, directory_path, recursive=False)
        
        print(f"Starting to monitor directory: {directory_path}")
        print(f"Logs will be written to: {log_file}")
        
        # Start the observer
        observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\nMonitoring stopped by user")
        
        observer.join()

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Configuration
    MONITOR_DIR = "./monitored_directory"  # Directory to monitor
    LOG_FILE = "file_monitor.log"          # Log file path
    
    start_monitoring(MONITOR_DIR, LOG_FILE)