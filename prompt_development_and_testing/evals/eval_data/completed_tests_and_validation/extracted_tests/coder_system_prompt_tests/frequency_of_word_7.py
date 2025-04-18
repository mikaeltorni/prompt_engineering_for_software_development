"""
word_frequency_counter.py

Reads a text file and displays the top 10 most frequent words.

Functions:
    clean_text(text: str) -> list
    process_file(file_path: str) -> dict
    display_results(word_counts: dict, top_n: int = 10) -> None
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

def clean_text(text: str) -> list:
    """
    Clean and tokenize the input text.

    Parameters:
        text (str): Raw text to be processed

    Returns:
        list: List of cleaned words
    """
    logger.debug(f"Input text length: {len(text)}")
    
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Split into words and remove empty strings
    words = [word.strip() for word in text.split() if word.strip()]
    
    logger.debug(f"Number of words after cleaning: {len(words)}")
    return words

def process_file(file_path: str) -> dict:
    """
    Read and process a text file to count word frequencies.

    Parameters:
        file_path (str): Path to the text file

    Returns:
        dict: Dictionary containing word frequencies
    """
    logger.debug(f"Processing file: {file_path}")
    
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with path.open('r', encoding='utf-8') as file:
            text = file.read()
            
        words = clean_text(text)
        word_counts = Counter(words)
        
        logger.info(f"Successfully processed file. Found {len(word_counts)} unique words")
        return dict(word_counts)
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise

def display_results(word_counts: dict, top_n: int = 10) -> None:
    """
    Display the top N most frequent words.

    Parameters:
        word_counts (dict): Dictionary of word frequencies
        top_n (int): Number of top words to display, default 10

    Returns:
        None
    """
    logger.debug(f"Displaying top {top_n} words")
    
    if not word_counts:
        logger.warning("No words to display")
        print("No words found in the text.")
        return
        
    # Sort words by frequency
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nTop {top_n} most frequent words:")
    print("-" * 30)
    print("Word".ljust(20) + "Frequency")
    print("-" * 30)
    
    for word, count in sorted_words[:top_n]:
        print(f"{word.ljust(20)} {count}")

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
            # If file path wasn't provided as command line argument, ask for it
            file_path = args.file if args.file else input("\nEnter the path to your text file (or 'quit' to exit): ")
            
            if file_path.lower() == 'quit':
                logger.info("Program terminated by user")
                break
                
            word_counts = process_file(file_path)
            display_results(word_counts)
            
            # If file was provided as command line argument, exit after processing
            if args.file:
                break
                
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            print(f"Error: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print(f"Error: An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    main()