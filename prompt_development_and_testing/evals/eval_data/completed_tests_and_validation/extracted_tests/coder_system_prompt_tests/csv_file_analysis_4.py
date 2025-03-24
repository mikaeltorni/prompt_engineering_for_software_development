"""
csv_analyzer.py

Performs basic statistical analysis on numerical columns in CSV files.

Functions:
    read_csv_file(file_path: str) -> pd.DataFrame: Reads and validates CSV file
    get_numeric_columns(df: pd.DataFrame) -> list: Returns list of numerical columns
    calculate_statistics(df: pd.DataFrame, column: str) -> dict: Calculates statistics for a column
    display_results(stats_dict: dict, column: str) -> None: Displays statistical results
    main() -> None: Main program loop

Command Line Usage Example:
    python csv_analyzer.py
"""

import logging
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

def read_csv_file(file_path: str) -> pd.DataFrame:
    """
    Reads and validates a CSV file.

    Parameters:
        file_path (str): Path to the CSV file

    Returns:
        pd.DataFrame: DataFrame containing the CSV data
    """
    logger.debug(f"Attempting to read file: {file_path}")
    
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            logger.error("CSV file is empty")
            raise ValueError("CSV file is empty")
        logger.debug(f"Successfully read CSV with shape: {df.shape}")
        return df
    except pd.errors.EmptyDataError:
        logger.error("CSV file is empty")
        raise ValueError("CSV file is empty")
    except pd.errors.ParserError:
        logger.error("Invalid CSV format")
        raise ValueError("Invalid CSV format")

def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """
    Returns a list of numerical columns from the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame

    Returns:
        List[str]: List of column names with numerical data
    """
    logger.debug("Identifying numeric columns")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    logger.debug(f"Found numeric columns: {numeric_columns}")
    return numeric_columns

def calculate_statistics(df: pd.DataFrame, column: str) -> Dict:
    """
    Calculates basic statistics for a given column.

    Parameters:
        df (pd.DataFrame): Input DataFrame
        column (str): Column name to analyze

    Returns:
        Dict: Dictionary containing calculated statistics
    """
    logger.debug(f"Calculating statistics for column: {column}")
    
    try:
        stats = {
            'mean': df[column].mean(),
            'median': df[column].median(),
            'mode': df[column].mode().iloc[0],
            'std': df[column].std(),
            'min': df[column].min(),
            'max': df[column].max()
        }
        logger.debug(f"Statistics calculated: {stats}")
        return stats
    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        raise ValueError(f"Error calculating statistics: {e}")

def display_results(stats_dict: Dict, column: str) -> None:
    """
    Displays statistical results in a formatted manner.

    Parameters:
        stats_dict (Dict): Dictionary containing statistical results
        column (str): Name of the column being displayed

    Returns:
        None
    """
    logger.debug(f"Displaying results for column: {column}")
    print(f"\nStatistics for column: {column}")
    print("-" * 40)
    for stat, value in stats_dict.items():
        print(f"{stat.capitalize():10}: {value:,.2f}")

def main() -> None:
    """
    Main program loop.

    Parameters:
        None

    Returns:
        None
    """
    while True:
        try:
            print("\nCSV File Analyzer")
            print("=" * 20)
            
            # Get file path
            file_path = input("\nEnter the path to your CSV file (or 'quit' to exit): ")
            if file_path.lower() == 'quit':
                logger.info("User requested to quit")
                break

            # Read and validate CSV
            df = read_csv_file(file_path)
            numeric_cols = get_numeric_columns(df)

            if not numeric_cols:
                logger.warning("No numeric columns found in CSV")
                print("No numeric columns found in the CSV file!")
                continue

            # Display available columns
            print("\nAvailable numeric columns:")
            for i, col in enumerate(numeric_cols, 1):
                print(f"{i}. {col}")

            # Get column selection
            while True:
                try:
                    selection = int(input("\nEnter the number of the column to analyze (0 to go back): "))
                    if selection == 0:
                        break
                    if 1 <= selection <= len(numeric_cols):
                        selected_column = numeric_cols[selection - 1]
                        stats = calculate_statistics(df, selected_column)
                        display_results(stats, selected_column)
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")

        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"An error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()