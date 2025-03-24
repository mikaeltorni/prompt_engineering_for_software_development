"""
word_frequency_counter.py

Reads a text file and displays the top 10 most frequent words.

Functions:
    read_file(file_path: str) -> str
    process_text(text: str) -> list
    count_words(words: list) -> dict
    display_results(word_counts: dict, limit: int = 10) -> None
    main() -> None

Command Line Usage Examples:
    python word_frequency_counter.py
    python word_frequency_counter.py --file path/to/file.txt
"""

import logging
from pathlib import Path
from collections import Counter
import re
import argparse
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def read_file(file_path: str) -> str:
    """
    Reads content from a text file.

    Parameters:
        file_path (str): Path to the text file

    Returns:
        str: Content of the file
    """
    logger.debug(f"Reading file: {file_path}")
    
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        with path.open('r', encoding='utf-8') as file:
            content = file.read()
            logger.debug(f"Successfully read {len(content)} characters")
            return content
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise RuntimeError(f"Error reading file: {e}")

def process_text(text: str) -> list:
    """
    Processes text by removing special characters and splitting into words.

    Parameters:
        text (str): Input text to process

    Returns:
        list: List of processed words
    """
    logger.debug(f"Processing text of length: {len(text)}")
    
    # Convert to lowercase and remove special characters
    cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
    
    # Split into words and filter out empty strings
    words = [word for word in cleaned_text.split() if word]
    
    logger.debug(f"Processed {len(words)} words")
    return words

def count_words(words: list) -> dict:
    """
    Counts frequency of each word in the list.

    Parameters:
        words (list): List of words to count

    Returns:
        dict: Dictionary with word counts
    """
    logger.debug(f"Counting frequency of {len(words)} words")
    
    word_counts = Counter(words)
    logger.debug(f"Found {len(word_counts)} unique words")
    
    return dict(word_counts)

def display_results(word_counts: dict, limit: int = 10) -> None:
    """
    Displays the top words and their frequencies.

    Parameters:
        word_counts (dict): Dictionary of word counts
        limit (int): Number of top words to display

    Returns:
        None
    """
    logger.debug(f"Displaying top {limit} words")
    
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("\nTop 10 most common words:")
    print("-" * 30)
    print("Rank  Word          Frequency")
    print("-" * 30)
    
    for rank, (word, count) in enumerate(sorted_words[:limit], 1):
        print(f"{rank:4d}  {word:<12} {count:8d}")

def main() -> None:
    """
    Main function to run the word frequency counter.

    Parameters:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Count word frequencies in a text file.')
    parser.add_argument('--file', help='Path to the text file')
    args = parser.parse_args()

    while True:
        try:
            # Get file path from command line or user input
            file_path = args.file if args.file else input("\nEnter the path to your text file (or 'quit' to exit): ")
            
            if file_path.lower() == 'quit':
                logger.info("Program terminated by user")
                break
                
            # Process the file
            content = read_file(file_path)
            words = process_text(content)
            word_counts = count_words(words)
            display_results(word_counts)
            
            # If file was provided via command line, exit after processing
            if args.file:
                break
                
        except FileNotFoundError as e:
            logger.error(f"File error: {e}")
            print(f"Error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"An unexpected error occurred: {e}")
            
        if args.file:  # If file was provided via command line, exit on error
            sys.exit(1)

if __name__ == "__main__":
    main()