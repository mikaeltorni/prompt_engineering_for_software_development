"""
word_frequency_counter.py

Analyzes text files to count and display word frequencies.

Functions:
    clean_text(text: str) -> str: Cleans and normalizes text
    count_words(text: str, min_length: int) -> Counter: Counts word frequencies
    display_top_words(word_counts: Counter, n: int) -> None: Displays top n frequent words
    process_file(file_path: str, min_length: int) -> Counter: Processes a file and returns word counts

Command Line Usage Examples:
    python word_frequency_counter.py
    python word_frequency_counter.py --min-length 4
"""

from pathlib import Path
from collections import Counter
import re
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Cleans and normalizes text by removing special characters and converting to lowercase.
    
    Parameters:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    logger.debug(f"Input text length: {len(text)}")
    
    # Convert to lowercase and remove special characters
    cleaned_text = re.sub(r'[^\w\s]', ' ', text.lower())
    
    logger.debug(f"Cleaned text length: {len(cleaned_text)}")
    return cleaned_text

def count_words(text: str, min_length: int) -> Counter:
    """
    Counts word frequencies in the given text.
    
    Parameters:
        text (str): Text to analyze
        min_length (int): Minimum word length to consider
        
    Returns:
        Counter: Dictionary-like object containing word frequencies
    """
    logger.debug(f"Counting words with minimum length: {min_length}")
    
    # Split text into words and filter by length
    words = [word for word in text.split() if len(word) >= min_length]
    
    # Count frequencies
    word_counts = Counter(words)
    
    logger.debug(f"Total unique words found: {len(word_counts)}")
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
    
    print(f"\nTop {n} most common words:")
    print("-" * 30)
    print("Word".ljust(20) + "Frequency")
    print("-" * 30)
    
    for word, count in word_counts.most_common(n):
        print(f"{word.ljust(20)}{count}")

def process_file(file_path: str, min_length: int) -> Counter:
    """
    Processes a text file and returns word frequencies.
    
    Parameters:
        file_path (str): Path to the text file
        min_length (int): Minimum word length to consider
        
    Returns:
        Counter: Dictionary-like object containing word frequencies
    """
    logger.debug(f"Processing file: {file_path} | min_length: {min_length}")
    
    path = Path(file_path)
    
    try:
        # Validate file existence
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Read and process file
        with path.open('r', encoding='utf-8') as file:
            text = file.read()
            
        # Clean and count words
        cleaned_text = clean_text(text)
        word_counts = count_words(cleaned_text, min_length)
        
        return word_counts
        
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise

def main():
    """
    Main program loop.
    
    Parameters:
        None
        
    Returns:
        None
    """
    while True:
        try:
            # Get file path from user
            file_path = input("\nEnter the path to your text file (or 'quit' to exit): ")
            
            if file_path.lower() == 'quit':
                print("Goodbye!")
                break
                
            # Get minimum word length
            while True:
                min_length = input("Enter minimum word length (default is 3): ").strip()
                if min_length == "":
                    min_length = 3
                    break
                try:
                    min_length = int(min_length)
                    if min_length > 0:
                        break
                    print("Please enter a positive number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Process file and display results
            word_counts = process_file(file_path, min_length)
            display_top_words(word_counts, 10)
            
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()