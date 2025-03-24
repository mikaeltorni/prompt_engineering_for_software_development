import pandas as pd
from statistics import mode, multimode
import os

def load_csv_file():
    while True:
        file_path = input("Enter the path to your CSV file: ").strip()
        if os.path.exists(file_path) and file_path.endswith('.csv'):
            try:
                df = pd.read_csv(file_path)
                return df
            except Exception as e:
                print(f"Error reading the file: {e}")
        else:
            print("Invalid file path or not a CSV file. Please try again.")

def get_numeric_columns(df):
    return df.select_dtypes(include=['int64', 'float64']).columns.tolist()

def calculate_statistics(df, column):
    """Calculate mean, median, and mode for a given column"""
    try:
        mean = df[column].mean()
        median = df[column].median()
        
        # Handle multiple modes
        try:
            mode_result = mode(df[column])
        except:
            mode_result = multimode(df[column])
            
        return {
            'mean': mean,
            'median': median,
            'mode': mode_result
        }
    except Exception as e:
        return f"Error calculating statistics: {e}"

def display_column_info(df):
    """Display information about available columns"""
    print("\nAvailable columns in the dataset:")
    for idx, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        print(f"{idx}. {col} (Type: {dtype})")

def main():
    print("CSV Data Analysis Program")
    print("========================")
    
    # Load the CSV file
    try:
        df = load_csv_file()
    except Exception as e:
        print(f"Error: {e}")
        return

    while True:
        print("\nOptions:")
        print("1. View dataset information")
        print("2. Analyze specific columns")
        print("3. Analyze all numeric columns")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            print("\nDataset Information:")
            print("-------------------")
            print(f"Number of rows: {len(df)}")
            print(f"Number of columns: {len(df.columns)}")
            display_column_info(df)
            
        elif choice == '2':
            display_column_info(df)
            numeric_columns = get_numeric_columns(df)
            
            column_name = input("\nEnter the column name to analyze: ").strip()
            
            if column_name in numeric_columns:
                stats = calculate_statistics(df, column_name)
                print(f"\nStatistics for {column_name}:")
                print(f"Mean: {stats['mean']:.2f}")
                print(f"Median: {stats['median']:.2f}")
                print(f"Mode: {stats['mode']}")
            else:
                print("Invalid column name or non-numeric column selected.")
                
        elif choice == '3':
            numeric_columns = get_numeric_columns(df)
            
            if not numeric_columns:
                print("No numeric columns found in the dataset.")
                continue
                
            print("\nAnalyzing all numeric columns:")
            print("-----------------------------")
            
            for column in numeric_columns:
                stats = calculate_statistics(df, column)
                print(f"\nStatistics for {column}:")
                print(f"Mean: {stats['mean']:.2f}")
                print(f"Median: {stats['median']:.2f}")
                print(f"Mode: {stats['mode']}")
                
        elif choice == '4':
            print("Thank you for using the CSV Data Analysis Program!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()