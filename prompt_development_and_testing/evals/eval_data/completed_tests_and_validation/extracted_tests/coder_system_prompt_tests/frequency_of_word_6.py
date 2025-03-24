"""
word_frequency_counter.py

Reads a text file and displays the top 10 most frequent words.

Functions:
    read_file(file_path: str) -> str
    process_text(text: str) -> Counter
    display_results(word_counts: Counter, top_n: int = 10) -> None
    main() -> None

Command Line Usage Examples:
    python word_frequency_counter.py
    python word_frequency_counter.py --file sample.txt
"""

import logging
from pathlib import Path
from collections import Counter
import re
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
    logger.debug(f"Attempting to read file: {file_path}")
    
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        logger.error(f"Path is not a file: {file_path}")
        raise ValueError(f"Path is not a file: {file_path}")
    
    try:
        with path.open('r', encoding='utf-8') as file:
            content = file.read()
            logger.debug(f"Successfully read file, content length: {len(content)}")
            return content
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise RuntimeError(f"Error reading file: {e}")

def process_text(text: str) -> Counter:
    """
    Processes text and counts word frequencies.

    Parameters:
        text (str): Input text to process

    Returns:
        Counter: Word frequency counter object
    """
    logger.debug(f"Processing text of length: {len(text)}")
    
    if not isinstance(text, str):
        logger.error("Input must be a string")
        raise TypeError("Input must be a string")
    
    # Convert to lowercase and remove special characters
    cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
    
    # Split into words and filter out empty strings
    words = [word for word in cleaned_text.split() if word]
    
    # Count word frequencies
    word_counts = Counter(words)
    logger.debug(f"Found {len(word_counts)} unique words")
    
    return word_counts

def display_results(word_counts: Counter, top_n: int = 10) -> None:
    """
    Displays the top N most frequent words.

    Parameters:
        word_counts (Counter): Counter object with word frequencies
        top_n (int): Number of top words to display, default 10

    Returns:
        None
    """
    logger.debug(f"Displaying top {top_n} words")
    
    if not word_counts:
        logger.warning("No words to display")
        print("No words found in the text.")
        return
    
    print(f"\nTop {top_n} most frequent words:")
    print("-" * 30)
    print("Rank  Word           Frequency")
    print("-" * 30)
    
    for rank, (word, count) in enumerate(word_counts.most_common(top_n), 1):
        print(f"{rank:4d}  {word:<14} {count:8d}")

def main() -> None:
    """
    Main function to run the word frequency counter program.

    Parameters:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Count word frequencies in a text file.")
    parser.add_argument('--file', help='Path to the text file (optional)')
    args = parser.parse_args()

    while True:
        try:
            # If file path wasn't provided as command line argument, ask for it
            file_path = args.file or input("\nEnter the path to your text file (or 'quit' to exit): ")
            
            if file_path.lower() == 'quit':
                logger.info("User requested to quit")
                break
            
            # Process the file
            text = read_file(file_path)
            word_counts = process_text(text)
            display_results(word_counts)
            
            # If file was provided as command line argument, exit after processing
            if args.file:
                break
                
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            print(f"Error: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()