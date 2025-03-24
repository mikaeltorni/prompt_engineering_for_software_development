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
        print(f"{word.ljust(20)}{count}")

def main():
    while True:
        # Get file path from user
        file_path = input("\nEnter the path to your text file (or 'q' to quit): ")
        
        if file_path.lower() == 'q':
            print("Goodbye!")
            break

        # Process the file and display results
        word_counts = read_and_count_words(file_path)
        if word_counts:
            # Get total word count
            total_words = sum(word_counts.values())
            unique_words = len(word_counts)

            # Display statistics
            print(f"\nTotal words: {total_words}")
            print(f"Unique words: {unique_words}")

            # Display top words
            display_top_words(word_counts)

            # Option to save results
            save_option = input("\nWould you like to save the results to a file? (y/n): ")
            if save_option.lower() == 'y':
                output_file = f"{os.path.splitext(file_path)[0]}_word_counts.txt"
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"Total words: {total_words}\n")
                        f.write(f"Unique words: {unique_words}\n\n")
                        f.write("Word Frequencies:\n")
                        f.write("-" * 30 + "\n")
                        f.write("Word".ljust(20) + "Frequency\n")
                        f.write("-" * 30 + "\n")
                        for word, count in word_counts.most_common():
                            f.write(f"{word.ljust(20)}{count}\n")
                    print(f"Results saved to {output_file}")
                except Exception as e:
                    print(f"Error saving results: {str(e)}")

if __name__ == "__main__":
    print("Word Frequency Counter")
    print("=" * 20)
    main()