"""
word_frequency_counter.py

Reads a text file and displays the top 10 most frequently occurring words.

Functions:
    clean_text(text: str) -> str: Cleans the input text
    count_words(text: str) -> Counter: Counts word frequencies
    display_top_words(word_counts: Counter, n: int) -> None: Displays top n frequent words
    process_file(file_path: str, top_n: int) -> None: Main processing function

Command Line Usage Examples:
    python word_frequency_counter.py <file_path> [--top N]
    python word_frequency_counter.py sample.txt
    python word_frequency_counter.py sample.txt --top 15
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

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing special characters and converting to lowercase.

    Parameters:
        text (str): Input text to clean

    Returns:
        str: Cleaned text
    """
    logger.debug(f"Input text length: {len(text)}")
    
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    # Convert to lowercase and remove special characters
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    
    logger.debug(f"Cleaned text length: {len(cleaned_text)}")
    return cleaned_text

def count_words(text: str) -> Counter:
    """
    Counts the frequency of each word in the text.

    Parameters:
        text (str): Input text to process

    Returns:
        Counter: Counter object containing word frequencies
    """
    logger.debug("Starting word counting")
    
    if not text.strip():
        raise ValueError("Input text cannot be empty")
    
    # Split text into words and count frequencies
    words = text.split()
    word_counts = Counter(words)
    
    logger.debug(f"Found {len(word_counts)} unique words")
    return word_counts

def display_top_words(word_counts: Counter, n: int) -> None:
    """
    Displays the top n most frequent words.

    Parameters:
        word_counts (Counter): Counter object containing word frequencies
        n (int): Number of top words to display

    Returns:
        None
    """
    logger.debug(f"Displaying top {n} words")
    
    if n < 1:
        raise ValueError("Number of words to display must be positive")
    
    print(f"\nTop {n} most common words:")
    print("-" * 30)
    print("Word".ljust(20) + "Frequency")
    print("-" * 30)
    
    for word, count in word_counts.most_common(n):
        print(f"{word.ljust(20)}{count}")

def process_file(file_path: str, top_n: int) -> None:
    """
    Processes the input file and displays word frequencies.

    Parameters:
        file_path (str): Path to the input file
        top_n (int): Number of top words to display

    Returns:
        None
    """
    logger.info(f"Processing file: {file_path}")
    
    try:
        # Convert string path to Path object
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read and process the file
        with path.open('r', encoding='utf-8') as file:
            text = file.read()
            
        # Clean and process text
        cleaned_text = clean_text(text)
        word_counts = count_words(cleaned_text)
        
        # Display results
        display_top_words(word_counts, top_n)
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise

def main():
    """
    Main function to handle command line arguments and program flow.

    Parameters:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(
        description="Count and display the most frequent words in a text file."
    )
    parser.add_argument("file_path", help="Path to the text file to process")
    parser.add_argument("--top", type=int, default=10,
                       help="Number of top words to display (default: 10)")
    
    args = parser.parse_args()
    
    try:
        while True:
            process_file(args.file_path, args.top)
            
            # Ask if user wants to process another file
            response = input("\nWould you like to process another file? (y/n): ").lower()
            if response != 'y':
                break
            
            # Get new file path
            new_file = input("Enter the path to the new file: ")
            args.file_path = new_file
            
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()