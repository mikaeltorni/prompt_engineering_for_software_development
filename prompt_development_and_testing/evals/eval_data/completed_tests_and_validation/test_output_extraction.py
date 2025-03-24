"""
Test Output Block Extractor

This script extracts output blocks from JSON files and saves them as separate files.
It searches for text fields in JSON data and extracts output blocks of the specified
programming language using regular expressions.

Functions:
    - get_output_block_regex(language: str = "python") -> re.Pattern:
        Returns a compiled regex pattern for extracting output blocks of the specified language.
    - find_text_fields(data: Union[Dict, List]) -> Generator[str, None, None]:
        Recursively search a data structure for any values whose key is 'text'.
    - extract_output_blocks(text: str, language: str = "python") -> List[str]:
        Given a text string, extract the first output block of the specified language.
    - save_output_blocks(output_blocks: List[str], output_dir: str, categories: List[str], tests_per_category: int, file_extension: str) -> None:
        Save each output block to a new file with appropriate naming.
    - process_json_file(json_path: str, output_dir: str, categories: List[str], tests_per_category: int, language: str = "python") -> int:
        Load a JSON file, search for text fields, extract output blocks, and save them to separate files.
    - get_file_extension_for_language(language: str) -> str:
        Returns the file extension for a given programming language.
    - parse_arguments() -> argparse.Namespace:
        Parses command-line arguments for the script.
    - main() -> None:
        Main function to run the output block extraction process.
    - run_interactive_mode() -> None:
        Run the script in interactive mode, allowing the user to process multiple JSON files.

Command Line Usage:
    python test_output_extraction.py <json_file> [options]

Examples:
    # Extract the Python test output blocks from input.json and save to the default directory
    python test_output_extraction.py input.json

    # Extract output blocks for a different language (e.g., XML) and save to a custom directory
    python test_output_extraction.py input.json --output-dir my_tests --language xml

    # Extract output blocks with custom categories and verbose logging
    python test_output_extraction.py input.json --categories calculator contact_book --verbose

    # Extract output blocks with a specified number of tests per category
    python test_output_extraction.py input.json --tests-per-category 1
"""

import re
import json
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Generator, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default categories
DEFAULT_CATEGORIES = [
    "calculator",
    "contact_book",
    "csv_file_analysis",
    "monitor",
    "frequency_of_word",
    "quiz_game",
    "password_generator",
    "temperature_converter",
    "room_game",
    "weather_app"
]

# Default number of tests per category
DEFAULT_TESTS_PER_CATEGORY = 10


def get_output_block_regex(language: str = "python") -> re.Pattern:
    """
    Returns a compiled regex pattern for extracting output blocks of the specified language.

    Parameters:
        language (str): The programming language to extract output blocks for

    Returns:
        re.Pattern: Compiled regular expression pattern
    """
    logger.debug(f"language: {language}")
    
    if not isinstance(language, str) or not language:
        logger.error("Language must be a non-empty string")
        raise ValueError("Language must be a non-empty string")
    
    pattern = re.compile(fr"```{language}\s*(.*?)\s*```", re.DOTALL)
    
    logger.debug(f"output: {pattern}")
    return pattern


def find_text_fields(data: Union[Dict, List]) -> Generator[str, None, None]:
    """
    Recursively search a data structure (dict or list) for any values whose key is 'text'.
    Yields each found text value.

    Parameters:
        data (Union[Dict, List]): The data structure to search

    Returns:
        Generator[str, None, None]: Generator yielding text values
    """
    logger.debug(f"data type: {type(data)}")
    
    if not isinstance(data, (dict, list)):
        logger.warning(f"Expected dict or list, got {type(data)}")
        return
        
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "text" and isinstance(value, str):
                logger.debug(f"Found text field with {len(value)} characters")
                yield value
            else:
                yield from find_text_fields(value)
    elif isinstance(data, list):
        for item in data:
            yield from find_text_fields(item)
            
    logger.debug(f"finished searching {type(data)}")


def extract_output_blocks(text: str, language: str = "python") -> List[str]:
    """
    Given a text string, extract the first output block of the specified language.
    Subsequent blocks are ignored.

    Parameters:
        text (str): The text to extract output blocks from
        language (str): The programming language to extract output blocks for

    Returns:
        List[str]: List containing the first extracted output block or empty list if none found
    """
    logger.debug(f"text length: {len(text)} | language: {language}")
    
    if not isinstance(text, str):
        logger.error("Text must be a string")
        raise TypeError("Text must be a string")
        
    output_block_regex = get_output_block_regex(language)
    # Use search() instead of findall() to get only the first match
    match = output_block_regex.search(text)
    
    if match:
        # Return a list with just the first match
        output_blocks = [match.group(1)]
        logger.debug(f"output: found first output block ({len(output_blocks[0])} chars)")
    else:
        output_blocks = []
        logger.debug(f"output: no output blocks found")
    
    return output_blocks


def save_output_blocks(output_blocks: List[str], output_dir: str, categories: List[str], tests_per_category: int, file_extension: str) -> None:
    """
    Save each output block to a new file with appropriate naming.
    
    File names are generated by cycling through categories with a fixed number of files per category.
    If more output blocks are found than expected, extra ones are named with a 'test' prefix.

    Parameters:
        output_blocks (List[str]): List of output blocks to save
        output_dir (str): Directory to save the files to
        categories (List[str]): List of category names for organizing output blocks
        tests_per_category (int): Number of tests per category
        file_extension (str): File extension to use for the saved files

    Returns:
        None
    """
    logger.debug(f"output_blocks count: {len(output_blocks)} | output_dir: {output_dir}")
    
    if not output_blocks:
        logger.warning("No output blocks to save")
        return
        
    if not isinstance(output_dir, str):
        logger.error("Output directory must be a string")
        raise TypeError("Output directory must be a string")
        
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created or verified output directory: {output_dir}")
    except Exception as e:
        logger.error(f"Failed to create output directory: {e}")
        raise RuntimeError(f"Failed to create output directory: {e}")

    # Save output blocks
    saved_count = 0
    for i, output in enumerate(output_blocks):
        try:
            # Determine which category to use based on the index
            cat_index = i // tests_per_category
            test_number = (i % tests_per_category) + 1

            if cat_index < len(categories):
                category = categories[cat_index]
                filename = f"{category}_{test_number}{file_extension}"
            else:
                # If there are more output blocks than categories * tests_per_category, use a fallback name
                filename = f"test_{i+1}{file_extension}"

            filepath = output_path / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(output)
            
            logger.info(f"Saved output block #{i+1} to {filepath}")
            saved_count += 1
            
        except Exception as e:
            logger.error(f"Error saving output block #{i+1}: {e}")
            
    logger.debug(f"output: saved {saved_count} output blocks to {output_dir}")


def process_json_file(json_path: str, output_dir: str, categories: List[str], tests_per_category: int, language: str = "python") -> int:
    """
    Load a JSON file, search for text fields, extract output blocks, and save them to separate files.

    Parameters:
        json_path (str): Path to the JSON file to process
        output_dir (str): Directory to save the extracted output blocks to
        categories (List[str]): List of category names for organizing output blocks
        tests_per_category (int): Number of tests per category
        language (str): Programming language to extract output blocks for

    Returns:
        int: Number of output blocks extracted and saved
    """
    logger.debug(f"json_path: {json_path} | output_dir: {output_dir} | language: {language}")
    
    # Validate input parameters
    if not json_path or not isinstance(json_path, str):
        logger.error("JSON path must be a non-empty string")
        raise ValueError("JSON path must be a non-empty string")
        
    if not output_dir or not isinstance(output_dir, str):
        logger.error("Output directory must be a non-empty string")
        raise ValueError("Output directory must be a non-empty string")
        
    # Get file extension for the language
    file_extension = get_file_extension_for_language(language)
    
    # Check if the JSON file exists
    json_file_path = Path(json_path)
    if not json_file_path.exists():
        error_msg = f"JSON file not found: {json_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
        
    # Load and parse the JSON file
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Successfully loaded JSON file: {json_path}")
    except json.JSONDecodeError as e:
        error_msg = f"Error decoding JSON: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"Error reading file: {e}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    # Gather all output blocks from every "text" field found
    all_output_blocks = []
    try:
        for text in find_text_fields(data):
            output_blocks = extract_output_blocks(text, language)
            if output_blocks:
                logger.info(f"Found {len(output_blocks)} output block(s) in a text field")
            all_output_blocks.extend(output_blocks)
    except Exception as e:
        logger.error(f"Error extracting output blocks: {e}")
        raise RuntimeError(f"Error extracting output blocks: {e}")

    # Save the output blocks if any were found
    if not all_output_blocks:
        logger.warning(f"No output blocks found in {json_path}")
    else:
        logger.info(f"Total output blocks found: {len(all_output_blocks)}")
        try:
            save_output_blocks(all_output_blocks, output_dir, categories, tests_per_category, file_extension)
        except Exception as e:
            logger.error(f"Error saving output blocks: {e}")
            raise RuntimeError(f"Error saving output blocks: {e}")
    
    logger.debug(f"output: extracted {len(all_output_blocks)} output blocks")
    return len(all_output_blocks)


def get_file_extension_for_language(language: str) -> str:
    """
    Get the appropriate file extension for a programming language.

    Parameters:
        language (str): Programming language name

    Returns:
        str: File extension for the language
    """
    logger.debug(f"language: {language}")
    
    if not isinstance(language, str) or not language:
        logger.error("Language must be a non-empty string")
        raise ValueError("Language must be a non-empty string")
    
    # Mapping of language to file extension
    extension_map = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "java": ".java",
        "c": ".c",
        "cpp": ".cpp",
        "csharp": ".cs",
        "go": ".go",
        "ruby": ".rb",
        "php": ".php",
        "swift": ".swift",
        "kotlin": ".kt",
        "rust": ".rs",
        "scala": ".scala",
        "html": ".html",
        "css": ".css",
        "shell": ".sh",
        "bash": ".sh",
        "sql": ".sql",
        "r": ".r",
        "xml": ".xml"
    }
    
    extension = extension_map.get(language.lower(), f".{language.lower()}")
    
    logger.debug(f"output: {extension}")
    return extension


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the script.

    Parameters:
        None

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    logger.debug("Parsing command line arguments")
    
    parser = argparse.ArgumentParser(
        description="Parse JSON file(s) for 'text' fields and extract output blocks into separate files."
    )
    parser.add_argument(
        "json_file",
        nargs="?",
        help="Path to the JSON file to process."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="extracted_tests",
        help="Directory to save the extracted files (default: extracted_tests)"
    )
    parser.add_argument(
        "-l", "--language",
        default="python",
        help="Programming language to extract output blocks for (default: python)"
    )
    parser.add_argument(
        "-c", "--categories",
        nargs="+",
        help="Categories to use for naming files (space-separated list)"
    )
    parser.add_argument(
        "-t", "--tests-per-category",
        type=int,
        default=DEFAULT_TESTS_PER_CATEGORY,
        help="Number of tests per category (default: 10)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        
    logger.debug(f"output: {args}")
    return args


def main() -> None:
    """
    Main function to run the output block extraction process.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Starting output block extraction")
    
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Set up logging level based on verbose flag
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        
        # Check if json_file is provided
        if args.json_file is None:
            logger.info("No JSON file specified. Running in interactive mode.")
            run_interactive_mode()
            return
            
        # Process the JSON file and extract output blocks
        blocks_count = process_json_file(
            args.json_file,
            args.output_dir,
            args.categories or DEFAULT_CATEGORIES,
            args.tests_per_category,
            args.language
        )
        
        if blocks_count > 0:
            logger.info(f"Successfully extracted {blocks_count} output blocks to {args.output_dir}")
        else:
            logger.warning("No output blocks were extracted")
            
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Value error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
        
    logger.debug("Output block extraction completed")


def run_interactive_mode() -> None:
    """
    Run the script in interactive mode, allowing the user to process multiple JSON files.

    Parameters:
        None

    Returns:
        None
    """
    logger.debug("Starting interactive mode")
    
    print("\n===== Output Block Extractor - Interactive Mode =====")
    print("This program extracts output blocks from JSON files and saves them to separate files.")
    
    while True:
        try:
            # Get JSON file path
            json_path = input("\nEnter the path to the JSON file (or 'q' to quit): ").strip()
            if json_path.lower() in ('q', 'quit', 'exit'):
                logger.info("Exiting program")
                print("Exiting program. Goodbye!")
                break
                
            if not json_path:
                logger.warning("Empty file path entered")
                print("Error: Please enter a valid file path.")
                continue
                
            # Check if file exists
            if not Path(json_path).exists():
                logger.error(f"File not found: {json_path}")
                print(f"Error: File not found: {json_path}")
                continue
                
            # Get output directory
            output_dir = input("Enter output directory (or press Enter for 'extracted_tests'): ").strip()
            if not output_dir:
                output_dir = "extracted_tests"
                
            # Get language
            language = input("Enter programming language (or press Enter for 'python'): ").strip()
            if not language:
                language = "python"
                
            # Process the file
            try:
                blocks_count = process_json_file(
                    json_path,
                    output_dir,
                    DEFAULT_CATEGORIES,
                    DEFAULT_TESTS_PER_CATEGORY,
                    language
                )
                
                if blocks_count > 0:
                    logger.info(f"Extracted {blocks_count} output blocks to {output_dir}")
                    print(f"\nSuccess! Extracted {blocks_count} output blocks to {output_dir}")
                else:
                    logger.warning(f"No output blocks found in {json_path}")
                    print(f"\nNo output blocks were found in {json_path}")
            except Exception as e:
                logger.error(f"Error processing file: {e}")
                print(f"Error: {e}")
                
        except Exception as e:
            logger.error(f"Error in interactive mode: {e}")
            print(f"Error: {e}")
            
    logger.debug("Interactive mode completed")


if __name__ == "__main__":
    try:
        # Check if any command-line arguments are provided
        if len(sys.argv) > 1:
            main()
        else:
            # If no arguments provided, run in interactive mode
            run_interactive_mode()
    except KeyboardInterrupt:
        logger.info("Program terminated by user.")
        print("\nProgram terminated by user.")
        sys.exit(0)
