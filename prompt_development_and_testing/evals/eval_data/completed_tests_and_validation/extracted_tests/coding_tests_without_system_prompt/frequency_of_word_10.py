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

def get_word_frequencies(words, min_word_length=3, exclude_words=None):
    if exclude_words is None:
        exclude_words = set()
    
    # Filter words based on length and exclude list
    filtered_words = [word for word in words 
                     if len(word) >= min_word_length 
                     and word not in exclude_words]
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    
    return word_counts

def display_top_words(word_counts, num_words=10):
    print("\nTop", num_words, "most common words:")
    print("-" * 30)
    print("Rank  Word          Frequency")
    print("-" * 30)
    
    # Get the top words
    for rank, (word, count) in enumerate(word_counts.most_common(num_words), 1):
        print(f"{rank:4d}  {word:<12} {count:8d}")

def main():
    # Common words to exclude (stopwords)
    stopwords = {'the', 'and', 'to', 'of', 'in', 'a', 'is', 'that', 'for', 'it', 
                'on', 'was', 'with', 'as', 'are', 'this', 'be', 'by', 'an', 'at'}

    while True:
        # Get file path from user
        file_path = input("\nEnter the path to your text file (or 'q' to quit): ")
        
        if file_path.lower() == 'q':
            break

        # Read and process the file
        words = read_and_count_words(file_path)
        
        if words:
            # Get word frequencies
            word_counts = get_word_frequencies(
                words,
                min_word_length=3,
                exclude_words=stopwords
            )

            # Display results
            total_words = len(words)
            unique_words = len(word_counts)
            
            print(f"\nTotal words: {total_words}")
            print(f"Unique words: {unique_words}")
            
            display_top_words(word_counts)

            # Ask if user wants to see more words
            while True:
                more = input("\nWould you like to see more words? (y/n): ")
                if more.lower() == 'y':
                    try:
                        num = int(input("How many more words would you like to see? "))
                        display_top_words(word_counts, num)
                    except ValueError:
                        print("Please enter a valid number.")
                elif more.lower() == 'n':
                    break

if __name__ == "__main__":
    print("Word Frequency Counter")
    print("=====================")
    main()
    print("\nThank you for using Word Frequency Counter!")