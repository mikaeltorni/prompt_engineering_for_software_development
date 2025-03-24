"""
Agent Tools

This module provides tools for file operations and code execution in a multi-agent programming system.

Functions:
    read_file_content(file_name: str) -> str:
        Reads content from a file relative to the project source directory.
        Handles file not found and permission errors.

    write_file_content(file_name: str, content: str) -> str:
        Writes content to a file relative to the project source directory.
        Returns success/error message.

    update_project_plan(content: str) -> str:
        Special function to update the project plan XML file.
        Avoids delegation issues between Project Manager and Coder.

    execute_python_code(code: str) -> str:
        Executes Python code in an isolated namespace with timeout.
        Captures and returns execution output or errors.

    test_file(file_name: str) -> str:
        Combines file reading and code execution.
        Returns both file content and execution results.
"""

import os
import io
import sys
import threading
import traceback
import logging
from typing import Dict, Any

from scripts.file_tools import read_file, write_file
from data.project_config import PROJECT_NAME, SRC_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s'
)
logger = logging.getLogger(__name__)

def read_file_content(file_name: str) -> str:
    """
    Read the content of a file given its path relative to the project source.

    Parameters:
        file_name (str): The path to the file, relative to the project source.

    Returns:
        str: The content of the file as a string or an error message.
    """
    logger.debug(f"Reading file: {file_name}")
    
    try:
        full_path = os.path.join(SRC_DIR, PROJECT_NAME, file_name)
        content = read_file(full_path)
        logger.info(f"Successfully read file: {full_path}")
        return content
    except FileNotFoundError:
        error_msg = f"Error: File '{full_path}' not found."
        logger.error(error_msg)
        return error_msg
    except PermissionError:
        error_msg = f"Error: Permission denied when trying to read '{full_path}'."
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error: An unexpected error occurred while reading '{full_path}': {str(e)}"
        logger.error(error_msg)
        return error_msg

def write_file_content(file_name: str, content: str) -> str:
    """
    Write content to a file given its path relative to the project source.

    Parameters:
        file_name (str): The path to the file, relative to the project source.
        content (str): The content to write to the file.

    Returns:
        str: A success message if the write operation is successful, or an error message if it fails.
    """
    logger.debug(f"Writing to file: {file_name}")
    
    try:
        full_path = os.path.join(SRC_DIR, PROJECT_NAME, file_name)
        write_file(full_path, content)
        logger.info(f"Successfully wrote content to file: {full_path}")
        return f"Successfully wrote content to '{full_path}'."
    except FileNotFoundError:
        error_msg = f"Error: Directory for file '{full_path}' not found."
        logger.error(error_msg)
        return error_msg
    except PermissionError:
        error_msg = f"Error: Permission denied when trying to write to '{full_path}'."
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error: An unexpected error occurred while writing to '{full_path}': {str(e)}"
        logger.error(error_msg)
        return error_msg

def update_project_plan(content: str) -> str:
    """
    Write content to the project plan XML file.
    
    This is a separate function to avoid delegation issues where the Project Manager
    might delegate the task to the Coder, which creates the project_plan.xml.

    Parameters:
        content (str): The XML content to write to the project plan file.

    Returns:
        str: A success message if the write operation is successful, or an error message if it fails.
    """
    logger.debug(f"Updating project plan with content length: {len(content)}")
    
    try:
        full_path = os.path.join(SRC_DIR, PROJECT_NAME, "project_plan.xml")
        write_file(full_path, content)
        logger.info(f"Successfully updated project plan at: {full_path}")
        return f"Successfully wrote content to '{full_path}'."
    except FileNotFoundError:
        error_msg = f"Error: Directory for file '{full_path}' not found."
        logger.error(error_msg)
        return error_msg
    except PermissionError:
        error_msg = f"Error: Permission denied when trying to write to '{full_path}'."
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error: An unexpected error occurred while writing to '{full_path}': {str(e)}"
        logger.error(error_msg)
        return error_msg

def execute_python_code(code: str) -> str:
    """
    Executes the given Python code and returns the output.

    Parameters:
        code (str): The Python code to execute.

    Returns:
        str: The output of the executed code, or an error message if execution fails.
    """
    logger.debug(f"Executing Python code of length: {len(code)}")
    logger.debug(f"First 100 chars of code: {code[:100]}")
    
    original_stdout = sys.stdout
    output_buffer = None
    
    try:
        # Set up output capture
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        def execute() -> None:
            """
            Inner function to execute the code in a separate thread.
            
            Parameters:
                None
                
            Returns:
                None
            """
            try:
                print("=== Code Execution ===")
                print("Code to execute:")
                print("```python")
                print(code)
                print("```")
                print("\n=== Code Execution Output ===")
                
                # Create a new namespace for execution
                namespace: Dict[str, Any] = {}
                exec(code, namespace, namespace)
                
                print("\n=== Namespace Contents ===")
                for key, value in namespace.items():
                    if not key.startswith('__'):
                        print(f"  {key}: {type(value).__name__}")
                
                # Call run_tests() if it exists in the namespace
                if 'run_tests' in namespace:
                    print("\n=== Running Tests ===")
                    namespace['run_tests']()
                    print("=== Tests Completed ===")
                
                print("=== End Code Execution ===")
                
            except Exception as e:
                print("\n=== Code Execution Error ===")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {str(e)}")
                print(traceback.format_exc())
                print("=== End Code Execution Error ===")
        
        # Run code execution in separate thread with timeout
        thread = threading.Thread(target=execute)
        thread.daemon = True
        thread.start()
        thread.join(timeout=10)  # 10 second timeout
        
        # Restore stdout before checking thread status
        sys.stdout = original_stdout
        output = output_buffer.getvalue()
        
        if thread.is_alive():
            logger.warning("Code execution timed out after 10 seconds")
            return "Error: Code execution timed out after 10 seconds\n\nPartial output:\n" + output
        
        logger.info("Code execution completed successfully")
        
        if not output.strip():
            return "Code executed successfully with no output."
        return output
        
    except Exception as e:
        if sys.stdout is not output_buffer:
            sys.stdout = original_stdout
        
        error_msg = f"Error executing code: {str(e)}\n{traceback.format_exc()}"
        logger.error(f"Error during code execution: {str(e)}")
        return error_msg
    finally:
        # Ensure stdout is restored even if an exception occurs
        if sys.stdout is not original_stdout:
            sys.stdout = original_stdout

def test_file(file_name: str) -> str:
    """
    Reads the content of a file, executes it as Python code, and returns both the file content and execution result.

    Parameters:
        file_name (str): The name of the file to test.

    Returns:
        str: A string containing the file content and the execution result.
    """
    logger.debug(f"Testing file: {file_name}")
    
    file_content = read_file_content(file_name)
    logger.debug(f"Read file content of length: {len(file_content)}")
    
    if file_content.startswith("Error:"):
        logger.error(f"Error reading file: {file_content}")
        return f"Error reading file:\n{file_content}"
    
    execution_result = execute_python_code(file_content)
    logger.debug(f"Execution result length: {len(execution_result)}")
    
    result = f"File content:\n{file_content}\n\nExecution result:\n{execution_result}"
    logger.info(f"Test completed for file: {file_name}")
    
    return result
