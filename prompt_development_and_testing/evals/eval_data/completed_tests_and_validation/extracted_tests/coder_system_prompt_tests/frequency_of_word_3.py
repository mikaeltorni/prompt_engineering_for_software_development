"""
word_frequency_counter.py

Reads a text file and displays the top 10 most frequent words.

Functions:
    read_file(file_path: str) -> str: Reads and validates text file
    process_text(text: str, min_word_length: int = 3) -> Counter: Processes text and counts word frequencies
    display_results(word_counts: Counter, top_n: int = 10) -> None: Displays top N most common words
    main() -> None: Main program loop

Command Line Usage Examples:
    python word_frequency_counter.py
    python word_frequency_counter.py --min-length 4
"""

from pathlib import Path
from collections import Counter
import re
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def read_file(file_path: str) -> str:
    """
    Reads and validates a text file.
    
    Parameters:
        file_path (str): Path to the text file
        
    Returns:
        str: Contents of the file
    """
    logger.debug(f"Reading file: {file_path}")
    
    path = Path(file_path)
    
    # Validate file path
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if path.suffix.lower() != '.txt':
        logger.error(f"Invalid file type: {path.suffix}")
        raise ValueError("File must be a .txt file")
        
    try:
        with path.open('r', encoding='utf-8') as file:
            text = file.read()
            
        if not text.strip():
            logger.error("File is empty")
            raise ValueError("File is empty")
            
        logger.debug(f"Successfully read file, length: {len(text)}")
        return text
        
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise

def process_text(text: str, min_word_length: int = 3) -> Counter:
    """
    Processes text and counts word frequencies.
    
    Parameters:
        text (str): Text to process
        min_word_length (int): Minimum word length to include
        
    Returns:
        Counter: Word frequency counts
    """
    logger.debug(f"Processing text | min_word_length: {min_word_length}")
    
    # Clean text: convert to lowercase and replace special characters with spaces
    cleaned_text = re.sub(r'[^a-zA-Z\s]', ' ', text.lower())
    
    # Split into words and filter by length
    words = [word for word in cleaned_text.split() if len(word) >= min_word_length]
    
    # Count frequencies
    word_counts = Counter(words)
    
    logger.debug(f"Found {len(word_counts)} unique words")
    return word_counts

def display_results(word_counts: Counter, top_n: int = 10) -> None:
    """
    Displays the top N most common words.
    
    Parameters:
        word_counts (Counter): Word frequency counts
        top_n (int): Number of top words to display
        
    Returns:
        None
    """
    logger.debug(f"Displaying top {top_n} results")
    
    print(f"\nTop {top_n} most common words:")
    print("-" * 30)
    print("Rank  Word          Frequency")
    print("-" * 30)
    
    for rank, (word, count) in enumerate(word_counts.most_common(top_n), 1):
        print(f"{rank:4d}  {word:<12} {count:8d}")

def main() -> None:
    """
    Main program loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Count word frequencies in a text file.')
    parser.add_argument('--min-length', type=int, default=3,
                      help='Minimum word length to consider (default: 3)')
    args = parser.parse_args()
    
    while True:
        try:
            file_path = input("\nEnter the path to your text file (or 'quit' to exit): ")
            
            if file_path.lower() == 'quit':
                logger.info("Program terminated by user")
                break
                
            text = read_file(file_path)
            word_counts = process_text(text, args.min_length)
            display_results(word_counts)
            
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()