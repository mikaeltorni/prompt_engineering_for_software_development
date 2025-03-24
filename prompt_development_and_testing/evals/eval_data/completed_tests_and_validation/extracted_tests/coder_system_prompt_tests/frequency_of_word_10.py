"""
word_frequency_counter.py

Reads a text file and displays the top 10 most frequent words.

Functions:
    clean_text(text: str) -> list
    process_file(file_path: str) -> dict
    display_results(word_counts: dict) -> None
    main() -> None

Command Line Usage Examples:
    python word_frequency_counter.py
    python word_frequency_counter.py --file sample.txt
"""

from pathlib import Path
from collections import Counter
import string
import logging
import sys

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
    
    try:
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        
        # Split into words and remove empty strings
        words = [word.strip() for word in text.split()]
        words = [word for word in words if word]
        
        logger.debug(f"Number of words after cleaning: {len(words)}")
        return words
    
    except Exception as e:
        logger.error(f"Error in clean_text: {e}")
        raise

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
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not path.is_file():
            logger.error(f"Not a file: {file_path}")
            raise ValueError(f"Not a file: {file_path}")
            
        with path.open('r', encoding='utf-8') as file:
            text = file.read()
            
        words = clean_text(text)
        word_counts = Counter(words)
        
        logger.debug(f"Total unique words found: {len(word_counts)}")
        return word_counts
    
    except Exception as e:
        logger.error(f"Error in process_file: {e}")
        raise

def display_results(word_counts: dict) -> None:
    """
    Display the top 10 most frequent words.

    Parameters:
        word_counts (dict): Dictionary of word frequencies

    Returns:
        None
    """
    logger.debug("Displaying results")
    
    try:
        print("\nTop 10 most frequent words:")
        print("-" * 30)
        print("Rank  Word          Frequency")
        print("-" * 30)
        
        for rank, (word, count) in enumerate(word_counts.most_common(10), 1):
            print(f"{rank:4d}  {word:<12} {count:8d}")
            
        logger.debug("Results displayed successfully")
    
    except Exception as e:
        logger.error(f"Error in display_results: {e}")
        raise

def main() -> None:
    """
    Main function to run the word frequency counter program.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Starting program")
    
    while True:
        try:
            print("\nWord Frequency Counter")
            print("=" * 20)
            
            # Get file path from user
            file_path = input("\nEnter the path to your text file (or 'quit' to exit): ").strip()
            
            if file_path.lower() == 'quit':
                logger.info("User requested to quit")
                print("\nGoodbye!")
                break
                
            # Process file and display results
            word_counts = process_file(file_path)
            display_results(word_counts)
            
        except FileNotFoundError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            logger.error(f"Unexpected error: {e}")
        
        print("\nPress Enter to continue...")
        input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
        print("\nProgram terminated by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
        print(f"\nCritical error: {e}")
        sys.exit(1)