import re
from collections import Counter
import string

def read_and_count_words(file_path):
    try:
        # Initialize word counter
        word_counts = Counter()
        
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().lower()  # Convert to lowercase
            
            # Remove punctuation
            text = text.translate(str.maketrans('', '', string.punctuation))
            
            # Split into words and count
            words = text.split()
            word_counts.update(words)
            
        return word_counts
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
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
    top_words = word_counts.most_common(n)
    
    for word, count in top_words:
        print(f"{word.ljust(20)}{count}")

def filter_common_words(word_counts, min_length=3):
    """Filter out very short words and common English articles/prepositions"""
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    return Counter({word: count for word, count in word_counts.items() 
                   if len(word) >= min_length and word not in common_words})

def main():
    while True:
        # Get file path from user
        file_path = input("\nEnter the path to your text file (or 'q' to quit): ")
        
        if file_path.lower() == 'q':
            print("Goodbye!")
            break
        
        # Read and count words
        word_counts = read_and_count_words(file_path)
        
        if word_counts:
            # Ask user if they want to filter common words
            filter_choice = input("\nDo you want to filter out common words? (y/n): ").lower()
            
            if filter_choice == 'y':
                word_counts = filter_common_words(word_counts)
            
            # Display results
            display_top_words(word_counts)
            
            # Display total unique words
            print(f"\nTotal unique words: {len(word_counts)}")
            
            # Ask if user wants to save results
            save_choice = input("\nDo you want to save the results to a file? (y/n): ").lower()
            
            if save_choice == 'y':
                output_file = file_path.rsplit('.', 1)[0] + '_word_counts.txt'
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write("Word Frequency Count\n")
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