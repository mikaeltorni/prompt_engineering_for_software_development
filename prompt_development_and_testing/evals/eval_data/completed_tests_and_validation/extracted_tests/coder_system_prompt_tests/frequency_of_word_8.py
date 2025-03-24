"""
word_frequency_counter.py

Reads a text file and displays the top 10 most frequent words.

Functions:
    read_file(file_path: str) -> str
    process_text(text: str) -> dict
    display_results(word_counts: dict, top_n: int = 10)
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

def process_text(text: str) -> dict:
    """
    Processes text and counts word frequencies.

    Parameters:
        text (str): Input text to process

    Returns:
        dict: Dictionary of word frequencies
    """
    logger.debug(f"Processing text of length: {len(text)}")
    
    if not isinstance(text, str):
        logger.error("Input must be a string")
        raise TypeError("Input must be a string")
    
    # Convert to lowercase and remove special characters
    cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
    
    # Split into words and remove empty strings
    words = [word for word in cleaned_text.split() if word]
    
    # Count word frequencies
    word_counts = Counter(words)
    
    logger.debug(f"Found {len(word_counts)} unique words")
    return dict(word_counts)

def display_results(word_counts: dict, top_n: int = 10) -> None:
    """
    Displays the top N most frequent words.

    Parameters:
        word_counts (dict): Dictionary of word frequencies
        top_n (int): Number of top words to display, default 10

    Returns:
        None
    """
    logger.debug(f"Displaying top {top_n} results")
    
    if not word_counts:
        print("No words to display.")
        return
    
    # Sort words by frequency
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Display results
    print("\nTop {} most frequent words:".format(top_n))
    print("-" * 30)
    print("Rank  Word          Frequency")
    print("-" * 30)
    
    for rank, (word, count) in enumerate(sorted_words[:top_n], 1):
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
    parser.add_argument('--file', help='Path to the text file (optional)')
    args = parser.parse_args()

    while True:
        try:
            # Get file path from command line or user input
            file_path = args.file if args.file else input("\nEnter the path to your text file (or 'quit' to exit): ")
            
            if file_path.lower() == 'quit':
                logger.info("Program terminated by user")
                break
            
            # Process the file
            text = read_file(file_path)
            word_counts = process_text(text)
            display_results(word_counts)
            
            # If file was provided via command line, exit after processing
            if args.file:
                break
                
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            logger.error(f"Unexpected error: {e}")
        
        if args.file:
            break

if __name__ == "__main__":
    main()