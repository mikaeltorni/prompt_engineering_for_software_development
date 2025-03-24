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
            return None

def get_numeric_columns(df):
    """
    Returns a list of numerical columns from the DataFrame.
    """
    return df.select_dtypes(include=['int64', 'float64']).columns.tolist()

def select_columns(numeric_columns):
    """
    Allows user to select columns for analysis from available numeric columns.
    """
    while True:
        print("\nAvailable numerical columns:")
        for i, col in enumerate(numeric_columns, 1):
            print(f"{i}. {col}")
        
        selection = input("\nEnter column numbers to analyze (comma-separated) or 'all': ").strip()
        
        if selection.lower() == 'all':
            return numeric_columns
            
        try:
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
        column_stats = {
            'mean': df[column].mean(),
            'median': df[column].median(),
            'mode': multimode(df[column].tolist())  # handles multiple modes
        }
        stats[column] = column_stats
    
    return stats

def display_statistics(stats):
    """
    Displays calculated statistics in a formatted manner.
    """
    print("\n=== Statistical Analysis Results ===")
    
    for column, measures in stats.items():
        print(f"\nColumn: {column}")
        print("-" * (len(column) + 8))
        print(f"Mean: {measures['mean']:.2f}")
        print(f"Median: {measures['median']:.2f}")
        
        # Handle multiple modes
        if len(measures['mode']) == 1:
            print(f"Mode: {measures['mode'][0]:.2f}")
        else:
            modes_str = ", ".join(f"{x:.2f}" for x in measures['mode'])
            print(f"Modes: {modes_str}")

def main():
    print("=== CSV Data Analysis Tool ===")
    
    # Load CSV file
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
    
    # Calculate statistics
    stats = calculate_statistics(df, selected_columns)
    
    # Display results
    display_statistics(stats)
    
    # Additional information
    print("\nDataset Information:")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Numerical columns: {len(numeric_columns)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")