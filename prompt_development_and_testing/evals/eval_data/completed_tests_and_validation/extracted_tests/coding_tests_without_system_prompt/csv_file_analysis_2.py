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
                print("Please try again.")
        else:
            print("Invalid file path or not a CSV file. Please try again.")

def get_numeric_columns(df):
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    return numeric_columns

def select_columns(numeric_columns):
    while True:
        print("\nAvailable numeric columns:")
        for i, col in enumerate(numeric_columns, 1):
            print(f"{i}. {col}")
        
        selection = input("\nEnter column numbers to analyze (comma-separated) or 'all' for all columns: ").strip()
        
        if selection.lower() == 'all':
            return numeric_columns
        
        try:
            selected_indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_columns = [numeric_columns[i] for i in selected_indices]
            return selected_columns
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")

def calculate_statistics(df, columns):
    stats = {}
    for column in columns:
        column_data = df[column].dropna()
        
        try:
            mean_val = column_data.mean()
            median_val = column_data.median()
            # Handle potential multiple modes
            mode_val = multimode(column_data.tolist())
            
            stats[column] = {
                'mean': mean_val,
                'median': median_val,
                'mode': mode_val,
                'count': len(column_data),
                'missing': df[column].isna().sum()
            }
        except Exception as e:
            print(f"Error calculating statistics for {column}: {e}")
            
    return stats

def display_statistics(stats):
    print("\nStatistical Analysis Results:")
    print("=" * 50)
    
    for column, values in stats.items():
        print(f"\nColumn: {column}")
        print("-" * 30)
        print(f"Count: {values['count']}")
        print(f"Missing Values: {values['missing']}")
        print(f"Mean: {values['mean']:.2f}")
        print(f"Median: {values['median']:.2f}")
        
        if len(values['mode']) == 1:
            print(f"Mode: {values['mode'][0]:.2f}")
        else:
            mode_str = ", ".join(f"{x:.2f}" for x in values['mode'])
            print(f"Modes: {mode_str}")

def main():
    print("CSV Data Analysis Program")
    print("=" * 30)
    
    try:
        # Load the CSV file
        df = load_csv_file()
        
        # Get numeric columns
        numeric_columns = get_numeric_columns(df)
        
        if not numeric_columns:
            print("No numeric columns found in the CSV file.")
            return
        
        # Let user select columns
        selected_columns = select_columns(numeric_columns)
        
        if not selected_columns:
            print("No columns selected for analysis.")
            return
        
        # Calculate statistics
        stats = calculate_statistics(df, selected_columns)
        
        # Display results
        display_statistics(stats)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("\nAnalysis complete.")

if __name__ == "__main__":
    main()