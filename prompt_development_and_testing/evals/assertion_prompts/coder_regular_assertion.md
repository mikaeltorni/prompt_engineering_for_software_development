# Expected Behavior
Your evaluation process should individually cover each of the points below.

## Documentation
Every function and file must have proper docstrings. Files should have a docstring at the top that includes:
```python
"""
    File name

    Description

    Functions

    Command Line Usage Example(s), if applicable, including with arguments
    """
```

Functions should have docstrings with descriptions, parameters, and return values:
```python     
def process_file(file_path: str) -> dict:
    """
    Process a file and return the results.
    
    Parameters:
        file_path (str): Path to the file to process
        
    Returns:
        dict: Results of processing containing word counts and statistics
    """
```
If the docstring or any part of it is missing (e.g., parameters or returns), **the test should fail**.

## Debugging
Contains proper logging setup and appropriate logger calls at function inputs and outputs:

```python
"""
logger_example.py

Demonstrates proper logging techniques.

Functions:
    None

Command Line Usage Example:
    python logger_example.py
"""
# Setup at module level
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Within functions
logger.debug(f"input: {input_data}")
logger.debug(f"output: {output_data}")
```

For multiple variables, use the `|` separator:
```python
logger.debug(f"variable1: {variable1} | variable2: {variable2}")
```

## Error Handling
Implements proper exception handling and input validation, for example:
```python
"""
error_handler.py

Demonstrates proper error handling techniques.

Functions:
    perform_critical_operation(): Performs a critical operation with error handling.

Command Line Usage Example:
    python error_handler.py
"""
import sys
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Critical operation
    result = perform_critical_operation()
except Exception as e:
    logger.error(f"Critical error: {e}")
    sys.exit(1)
```

## File Handling
Uses proper file handling techniques without hardcoded file paths:
```python
"""
word_processor.py

Processes text files to analyze word statistics.

Functions:
    process_file(file_path: str) -> dict: Process a file and return word statistics.

Command Line Usage Examples:
    python word_processor.py <file_path>
    python word_processor.py sample.txt
    python word_processor.py data/books/sample_book.txt
"""
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(funcName)s: %(message)s'
)
logger = logging.getLogger(__name__)

def process_file(file_path: str) -> dict:
    """
    Process a file and return the results.
    
    Parameters:
        file_path (str): Path to the file to process
        
    Returns:
        dict: Results of processing containing word counts and statistics
    """
    logger.info(f"Processing file: {file_path}")
    
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
        
    processed_results = {
        'word_counts': {},
        'total_words': 0,
        'unique_words': 0,
        'avg_word_length': 0
    }
    
    try:
        logger.debug("Opening and reading file")
        with path.open('r', encoding='utf-8') as file:
            text = file.read().lower()
            # Remove special characters and split into words
            words = ''.join(c if c.isalnum() else ' ' for c in text).split()
            
            logger.debug("Calculating word statistics")
            # Calculate word statistics
            processed_results['total_words'] = len(words)
            word_lengths = 0
            
            # Count word frequencies
            logger.debug("Counting word frequencies")
            for word in words:
                processed_results['word_counts'][word] = processed_results['word_counts'].get(word, 0) + 1
                word_lengths += len(word)
            
            processed_results['unique_words'] = len(processed_results['word_counts'])
            processed_results['avg_word_length'] = word_lengths / len(words) if words else 0
            
            logger.info(f"Processing complete. Total words: {processed_results['total_words']}, Unique words: {processed_results['unique_words']}")
            
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise RuntimeError(f"Error processing file: {e}")
        
    return processed_results
```

## Requirements
If the code includes external packages that require installation (such as pandas, numpy, requests, beautifulsoup4, matplotlib, scikit-learn, flask, django, pillow, pytest), a `requirements.txt` file should be included with the necessary dependencies. For example:
```
requests==2.28.1
pandas>=1.3.0
numpy~=1.21.0
```
This is not needed for native Python packages that do not require separate installation, such as `os`, `sys`, `math`, `random`, `datetime`, `json`, `re`, `collections`, `logging`, and `unittest`.

## Readability
Code follows clean coding practices and is easy to understand, while being split into logical functions.

## Functionality
Code performs the requested task correctly.

## Looping
Command-line applications continue execution until the user decides to stop.
