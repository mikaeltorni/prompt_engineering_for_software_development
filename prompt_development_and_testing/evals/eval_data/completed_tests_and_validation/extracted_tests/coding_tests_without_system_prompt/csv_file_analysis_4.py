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

def display_column_names(columns):
    """
    Displays available numerical columns with their indices.
    """
    print("\nAvailable numerical columns:")
    for idx, col in enumerate(columns, 1):
        print(f"{idx}. {col}")

def get_user_column_selection(numeric_columns):
    """
    Gets user's column selection and returns selected columns.
    """
    while True:
        try:
            print("\nEnter the numbers of the columns you want to analyze")
            print("(separated by commas, or 'all' for all columns):")
            selection = input().strip().lower()
            
            if selection == 'all':
                return numeric_columns
            
            selected_indices = [int(x.strip()) for x in selection.split(',')]
            selected_columns = []
            
            for idx in selected_indices:
                if 1 <= idx <= len(numeric_columns):
                    selected_columns.append(numeric_columns[idx-1])
                else:
                    print(f"Invalid column number: {idx}")
                    return get_user_column_selection(numeric_columns)
                    
            return selected_columns
            
        except ValueError:
            print("Invalid input! Please enter numbers separated by commas or 'all'")

def calculate_statistics(df, columns):
    """
    Calculates and returns statistical measures for selected columns.
    """
    stats = {}
    for col in columns:
        stats[col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'mode': multimode(df[col].tolist()),  # handles multiple modes
            'min': df[col].min(),
            'max': df[col].max(),
            'std': df[col].std()
        }
    return stats

def display_statistics(stats):
    """
    Displays calculated statistics in a formatted way.
    """
    print("\n=== Statistical Analysis Results ===")
    for column, measures in stats.items():
        print(f"\nColumn: {column}")
        print("-" * 40)
        print(f"Mean: {measures['mean']:.2f}")
        print(f"Median: {measures['median']:.2f}")
        print(f"Mode: {', '.join(map(str, measures['mode']))}")
        print(f"Minimum: {measures['min']:.2f}")
        print(f"Maximum: {measures['max']:.2f}")
        print(f"Standard Deviation: {measures['std']:.2f}")

def main():
    print("=== CSV Data Analysis Tool ===")
    
    # Load the CSV file
    df = load_csv_file()
    if df is None:
        return
    
    # Get numerical columns
    numeric_columns = get_numeric_columns(df)
    if not numeric_columns:
        print("No numerical columns found in the CSV file!")
        return
    
    # Display available columns and get user selection
    display_column_names(numeric_columns)
    selected_columns = get_user_column_selection(numeric_columns)
    
    # Calculate and display statistics
    stats = calculate_statistics(df, selected_columns)
    display_statistics(stats)
    
    # Display additional information
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