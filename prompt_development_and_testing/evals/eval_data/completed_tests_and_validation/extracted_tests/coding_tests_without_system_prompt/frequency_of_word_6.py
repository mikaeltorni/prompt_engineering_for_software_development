import re
from collections import Counter
import string

def read_and_count_words(file_path):
    try:
        # Initialize word counter
        word_counter = Counter()
        
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()  # Convert to lowercase
            
            # Remove punctuation
            text = text.translate(str.maketrans('', '', string.punctuation))
            
            # Split into words and count
            words = text.split()
            word_counter.update(words)
            
        return word_counter
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def display_top_words(word_counter, n=10):
    if word_counter is None:
        return
    
    print(f"\nTop {n} most common words:")
    print("-" * 30)
    print("Word".ljust(20) + "Frequency")
    print("-" * 30)
    
    # Get the n most common words
    for word, count in word_counter.most_common(n):
        print(f"{word.ljust(20)} {count}")

def filter_stop_words(word_counter):
    # Common English stop words
    stop_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
                  'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at'}
    
    # Remove stop words from the counter
    for word in stop_words:
        if word in word_counter:
            del word_counter[word]
    
    return word_counter

def main():
    while True:
        # Get file path from user
        file_path = input("\nEnter the path to your text file (or 'q' to quit): ")
        
        if file_path.lower() == 'q':
            print("Goodbye!")
            break
        
        # Read and count words
        word_counter = read_and_count_words(file_path)
        
        if word_counter:
            # Ask user if they want to filter stop words
            filter_choice = input("Would you like to filter out common stop words? (y/n): ")
            
            if filter_choice.lower() == 'y':
                word_counter = filter_stop_words(word_counter)
            
            # Display statistics
            total_words = sum(word_counter.values())
            unique_words = len(word_counter)
            
            print(f"\nTotal words: {total_words}")
            print(f"Unique words: {unique_words}")
            
            # Display top words
            display_top_words(word_counter)

if __name__ == "__main__":
    main()