import re
from collections import Counter
import os

def read_and_count_words(file_path):
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()  # Convert to lowercase

        # Clean the text and split into words
        # Remove punctuation and split by whitespace
        words = re.findall(r'\b\w+\b', text)

        # Count word frequencies using Counter
        word_counts = Counter(words)

        return word_counts

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def display_top_words(word_counts, n=10):
    if word_counts is None:
        return

    print(f"\nTop {n} most common words:")
    print("-" * 30)
    print("Word".ljust(20) + "Frequency")
    print("-" * 30)

    # Get the n most common words
    for word, count in word_counts.most_common(n):
        print(f"{word.ljust(20)} {count}")

def main():
    while True:
        # Get file path from user
        file_path = input("\nEnter the path to your text file (or 'q' to quit): ")
        
        if file_path.lower() == 'q':
            print("Goodbye!")
            break

        # Count words and display results
        word_counts = read_and_count_words(file_path)
        if word_counts:
            # Get total word count
            total_words = sum(word_counts.values())
            unique_words = len(word_counts)

            print(f"\nTotal words: {total_words}")
            print(f"Unique words: {unique_words}")

            # Display top 10 words
            display_top_words(word_counts)

            # Option to see more words
            while True:
                more = input("\nWould you like to see more words? (y/n): ").lower()
                if more == 'y':
                    try:
                        n = int(input("How many words would you like to see? "))
                        display_top_words(word_counts, n)
                    except ValueError:
                        print("Please enter a valid number.")
                elif more == 'n':
                    break
                else:
                    print("Please enter 'y' or 'n'")

if __name__ == "__main__":
    print("Word Frequency Counter")
    print("=" * 20)
    main()