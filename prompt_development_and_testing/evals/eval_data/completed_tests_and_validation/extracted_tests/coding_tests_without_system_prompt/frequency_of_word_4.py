import re
from collections import Counter
import string

def read_and_count_words(file_path):
    try:
        # Initialize word counter
        word_counter = Counter()
        
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Convert to lowercase and remove punctuation
                line = line.lower()
                line = line.translate(str.maketrans('', '', string.punctuation))
                
                # Split line into words and count
                words = line.split()
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
    print("Word          | Frequency")
    print("-" * 30)
    
    # Get the n most common words
    for word, count in word_counter.most_common(n):
        # Format the output with proper spacing
        print(f"{word:<14}| {count}")

def filter_stop_words(word_counter):
    # Common English stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
                  'for', 'of', 'with', 'by'}
    
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
            
            # Display results
            display_top_words(word_counter)
            
            # Display total word count
            total_words = sum(word_counter.values())
            unique_words = len(word_counter)
            print(f"\nTotal words: {total_words}")
            print(f"Unique words: {unique_words}")

if __name__ == "__main__":
    main()