import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

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
        
        # Keep track of processed files
        self.processed_files = set()

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        try:
            file_path = event.src_path
            file_name = os.path.basename(file_path)
            
            # Avoid processing the same file multiple times
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
                f"Name: {file_name}\n"
                f"Path: {file_path}\n"
                f"Creation Time: {creation_datetime}\n"
                f"Size: {self.format_size(file_size)}\n"
                f"{'-'*50}"
            )
            
            # Add to processed files
            self.processed_files.add(file_path)
            
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")

    @staticmethod
    def format_size(size):
        """Convert size in bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

def start_monitoring(directory_path, log_file):
    """Start monitoring the specified directory."""
    try:
        # Create an observer and file monitor
        event_handler = FileMonitor(log_file)
        observer = Observer()
        observer.schedule(event_handler, directory_path, recursive=False)
        
        # Start the observer
        print(f"Starting to monitor directory: {directory_path}")
        print(f"Logs will be written to: {log_file}")
        observer.start()
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\nMonitoring stopped by user")
        
        observer.join()
        
    except Exception as e:
        print(f"Error setting up directory monitoring: {str(e)}")

def main():
    # Configuration
    DIRECTORY_TO_MONITOR = "path/to/your/directory"  # Change this to your directory
    LOG_FILE = "file_monitor.log"  # Change this to your desired log file path
    
    # Validate directory
    if not os.path.exists(DIRECTORY_TO_MONITOR):
        print(f"Error: Directory '{DIRECTORY_TO_MONITOR}' does not exist!")
        return
    
    # Start monitoring
    start_monitoring(DIRECTORY_TO_MONITOR, LOG_FILE)

if __name__ == "__main__":
    main()