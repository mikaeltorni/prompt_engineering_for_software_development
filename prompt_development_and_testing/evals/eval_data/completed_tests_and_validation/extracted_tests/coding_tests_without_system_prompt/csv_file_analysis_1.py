import pandas as pd
from statistics import mode, multimode
import os

def load_csv_file():
    """
    Prompts user for CSV file path and loads the file.
    Returns DataFrame if successful, None if failed.
    """
    while True:
        file_path = input("\nEnter the path to your CSV file: ").strip()
        
        if not os.path.exists(file_path):
            print("Error: File does not exist!")
            continue
            
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            print(f"Error loading file: {e}")
            continue

def get_numeric_columns(df):
    """
    Returns a list of numerical columns from the DataFrame.
    """
    return df.select_dtypes(include=['int64', 'float64']).columns.tolist()

def select_columns(numeric_columns):
    """
    Allows user to select which columns to analyze.
    """
    print("\nAvailable numerical columns:")
    for i, col in enumerate(numeric_columns, 1):
        print(f"{i}. {col}")
    
    while True:
        try:
            selection = input("\nEnter column numbers to analyze (comma-separated) or 'all': ").strip()
            
            if selection.lower() == 'all':
                return numeric_columns
            
            selected_indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_columns = [numeric_columns[i] for i in selected_indices]
            return selected_columns
            
        except (ValueError, IndexError):
            print("Invalid selection! Please try again.")

def calculate_statistics(df, columns):
    """
    Calculates mean, median, and mode for selected columns.
    """
    stats = {}
    
    for column in columns:
        stats[column] = {
            'mean': df[column].mean(),
            'median': df[column].median(),
            'mode': multimode(df[column].tolist())  # handles multiple modes
        }
    
    return stats

def display_statistics(stats):
    """
    Displays the calculated statistics in a formatted way.
    """
    print("\nStatistical Analysis Results:")
    print("-" * 50)
    
    for column, measures in stats.items():
        print(f"\nColumn: {column}")
        print(f"Mean: {measures['mean']:.2f}")
        print(f"Median: {measures['median']:.2f}")
        print(f"Mode: {', '.join(map(str, measures['mode']))}")
        print("-" * 50)

def main():
    print("CSV Data Analysis Program")
    print("=" * 30)
    
    # Load the CSV file
    df = load_csv_file()
    if df is None:
        return
    
    # Get numerical columns
    numeric_columns = get_numeric_columns(df)
    if not numeric_columns:
        print("No numerical columns found in the CSV file!")
        return
    
    # Let user select columns
    selected_columns = select_columns(numeric_columns)
    if not selected_columns:
        print("No columns selected!")
        return
    
    # Calculate and display statistics
    stats = calculate_statistics(df, selected_columns)
    display_statistics(stats)
    
    # Additional information
    print("\nAdditional Information:")
    print(f"Total rows in dataset: {len(df)}")
    print(f"Total columns analyzed: {len(selected_columns)}")

def run_program():
    while True:
        main()
        
        if input("\nWould you like to analyze another file? (y/n): ").lower() != 'y':
            print("\nThank you for using the CSV Data Analysis Program!")
            break

if __name__ == "__main__":
    run_program()