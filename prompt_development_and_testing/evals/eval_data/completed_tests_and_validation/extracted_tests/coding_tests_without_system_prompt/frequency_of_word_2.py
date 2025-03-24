import re
from collections import Counter
import os

def read_and_count_words(file_path):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError("The specified file does not exist.")

        # Read the file and process words
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read all text and convert to lowercase
            text = file.read().lower()
            
            # Remove punctuation and split into words
            # This regex splits on any non-word character
            words = re.findall(r'\b\w+\b', text)
            
            return words

    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def get_word_frequency(words, min_length=3):
    """
    Count word frequency and return the top 10 most common words
    Excludes words shorter than min_length
    """
    if not words:
        return None

    # Filter words by minimum length and count frequencies
    word_counts = Counter(word for word in words if len(word) >= min_length)
    return word_counts

def display_top_words(word_counts, num_words=10):
    """
    Display the top words and their frequencies
    """
    if not word_counts:
        print("No words to display.")
        return

    print(f"\nTop {num_words} most common words:")
    print("-" * 30)
    print("Rank  |  Word  |  Frequency")
    print("-" * 30)

    # Get the top words
    for rank, (word, count) in enumerate(word_counts.most_common(num_words), 1):
        print(f"{rank:4d}  |  {word:8s}  |  {count:5d}")

def main():
    while True:
        # Get file path from user
        file_path = input("\nEnter the path to your text file (or 'q' to quit): ")
        
        if file_path.lower() == 'q':
            break

        # Read and process the file
        words = read_and_count_words(file_path)
        
        if words:
            # Get word frequencies
            word_counts = get_word_frequency(words)
            
            if word_counts:
                # Display statistics
                total_words = len(words)
                unique_words = len(word_counts)
                
                print(f"\nTotal words: {total_words}")
                print(f"Unique words: {unique_words}")
                
                # Display top words
                display_top_words(word_counts)
            
        # Ask if user wants to analyze another file
        choice = input("\nWould you like to analyze another file? (y/n): ")
        if choice.lower() != 'y':
            break

    print("\nThank you for using the word frequency counter!")

if __name__ == "__main__":
    print("Welcome to Word Frequency Counter!")
    print("This program will analyze a text file and show the most common words.")
    main()