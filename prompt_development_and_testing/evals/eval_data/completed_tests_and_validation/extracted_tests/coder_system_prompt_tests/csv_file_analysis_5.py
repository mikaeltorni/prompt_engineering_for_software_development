"""
csv_analyzer.py

Performs basic statistical analysis on numerical columns in CSV files.

Functions:
    validate_file(file_path: str) -> bool
    load_csv_data(file_path: str) -> pd.DataFrame
    get_numeric_columns(df: pd.DataFrame) -> list
    calculate_statistics(data: pd.Series) -> dict
    display_results(stats: dict, column: str) -> None
    process_file(file_path: str) -> None

Command Line Usage Examples:
    python csv_analyzer.py
    python csv_analyzer.py --file data.csv
"""

import logging
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from statistics import mode, multimode

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)

def validate_file(file_path: str) -> bool:
    """
    Validates if the file exists and has a .csv extension.

    Parameters:
        file_path (str): Path to the CSV file

    Returns:
        bool: True if file is valid, False otherwise
    """
    logger.debug(f"Validating file: {file_path}")
    
    path = Path(file_path)
    if not path.exists():
        logger.error("File does not exist")
        return False
    if path.suffix.lower() != '.csv':
        logger.error("File is not a CSV")
        return False
    
    return True

def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    Loads CSV file into a pandas DataFrame.

    Parameters:
        file_path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Loaded CSV data
    """
    logger.debug(f"Loading CSV file: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        logger.debug(f"Successfully loaded CSV with shape: {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        raise

def get_numeric_columns(df: pd.DataFrame) -> list:
    """
    Identifies numerical columns in the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame

    Returns:
        list: List of numerical column names
    """
    logger.debug("Identifying numeric columns")
    
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    logger.debug(f"Found numeric columns: {numeric_columns}")
    return numeric_columns

def calculate_statistics(data: pd.Series) -> dict:
    """
    Calculates basic statistics for a numeric series.

    Parameters:
        data (pd.Series): Numeric data series

    Returns:
        dict: Dictionary containing calculated statistics
    """
    logger.debug(f"Calculating statistics for series with length: {len(data)}")
    
    stats = {
        'mean': None,
        'median': None,
        'mode': None,
        'std': None,
        'min': None,
        'max': None
    }
    
    try:
        stats['mean'] = data.mean()
        stats['median'] = data.median()
        stats['mode'] = multimode(data)
        stats['std'] = data.std()
        stats['min'] = data.min()
        stats['max'] = data.max()
        
        logger.debug(f"Statistics calculated: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        raise

def display_results(stats: dict, column: str) -> None:
    """
    Displays calculated statistics in a formatted manner.

    Parameters:
        stats (dict): Dictionary of calculated statistics
        column (str): Column name

    Returns:
        None
    """
    logger.debug(f"Displaying results for column: {column}")
    
    print(f"\nStatistics for column: {column}")
    print("-" * 40)
    print(f"Mean: {stats['mean']:.2f}")
    print(f"Median: {stats['median']:.2f}")
    print(f"Mode: {', '.join(map(str, stats['mode']))}")
    print(f"Standard Deviation: {stats['std']:.2f}")
    print(f"Minimum: {stats['min']:.2f}")
    print(f"Maximum: {stats['max']:.2f}")

def process_file(file_path: str) -> None:
    """
    Main function to process the CSV file and calculate statistics.

    Parameters:
        file_path (str): Path to the CSV file

    Returns:
        None
    """
    logger.debug(f"Processing file: {file_path}")
    
    if not validate_file(file_path):
        return

    try:
        # Load the data
        df = load_csv_data(file_path)
        
        # Get numeric columns
        numeric_columns = get_numeric_columns(df)
        
        if not numeric_columns:
            logger.error("No numeric columns found in the CSV file")
            return

        # Display available columns
        print("\nAvailable numeric columns:")
        for i, col in enumerate(numeric_columns, 1):
            print(f"{i}. {col}")

        # Get user selection
        while True:
            try:
                selection = input("\nEnter the number of the column to analyze (or 'q' to quit): ")
                
                if selection.lower() == 'q':
                    break
                
                col_index = int(selection) - 1
                if 0 <= col_index < len(numeric_columns):
                    selected_column = numeric_columns[col_index]
                    stats = calculate_statistics(df[selected_column])
                    display_results(stats, selected_column)
                else:
                    logger.warning("Invalid column number")
                    print("Please enter a valid column number")
            except ValueError:
                logger.warning("Invalid input")
                print("Please enter a valid number")
            except Exception as e:
                logger.error(f"Error processing selection: {e}")
                print("An error occurred. Please try again.")

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        print(f"An error occurred while processing the file: {e}")

def main():
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    print("CSV File Analyzer")
    print("================")

    while True:
        file_path = input("\nEnter the path to your CSV file (or 'q' to quit): ")
        
        if file_path.lower() == 'q':
            break
            
        process_file(file_path)

if __name__ == "__main__":
    main()