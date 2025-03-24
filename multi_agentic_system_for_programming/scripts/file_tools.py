"""
File Tools

This module provides file system utilities for managing files and directories.

Functions:
    read_file(file_name: str) -> str:
        Reads and returns the content of a file relative to the project root.
        Handles path normalization and UTF-8 encoding.

    write_file(file_name: str, content: str) -> None:
        Writes content to a file relative to the project root.
        Creates parent directories if they don't exist.

    create_directory(directory_path: str) -> None:
        Creates a directory at the specified path if it doesn't already exist.
        Creates parent directories as needed.

    delete_non_hidden_file(file_path: str) -> bool:
        Deletes a file if it exists and is not hidden (doesn't start with '.').
        Skips hidden files for safety. Returns True if file was deleted.

    delete_non_hidden_directory(dir_path: str) -> bool:
        Recursively deletes a directory if it exists and is not hidden.
        Skips hidden directories for safety. Returns True if directory was deleted.
"""

import os
import shutil
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s'
)
logger = logging.getLogger(__name__)

def read_file(file_name: str) -> str:
    """
    Read the content of a file.
    
    Parameters:
        file_name (str): Path to the file to read, relative to project root
        
    Returns:
        str: Content of the file
        
    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there is an error reading the file
    """
    logger.debug(f"file_name: {file_name}")
    
    # Check if it's an absolute path
    if os.path.isabs(file_name):
        full_path = file_name
    else:
        # Check if file exists as is (might be an absolute path already)
        if os.path.exists(file_name):
            full_path = file_name
        else:
            # Get project root directory (up two levels from scripts)
            project_root = os.path.dirname(os.path.dirname(__file__))
            
            # Check if the file exists relative to multi_agentic_system_for_programming
            normalized_path = os.path.normpath(file_name)
            full_path = os.path.normpath(os.path.join(project_root, normalized_path))
            
            # If not found, try looking in the workspace root 
            if not os.path.exists(full_path):
                workspace_root = os.path.dirname(project_root)
                full_path = os.path.normpath(os.path.join(workspace_root, normalized_path))
    
    logger.debug(f"Resolved path: {full_path}")
    
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        logger.debug(f"Read {len(content)} characters from file")
        return content
    except FileNotFoundError:
        logger.error(f"File not found: {full_path}")
        raise
    except IOError as e:
        logger.error(f"Error reading file {full_path}: {e}")
        raise

def write_file(file_name: str, content: str) -> None:
    """
    Write content to a file.
    
    Parameters:
        file_name (str): Path to the file to write, relative to project root
        content (str): Content to write to the file
        
    Returns:
        None
        
    Raises:
        IOError: If there is an error writing to the file
    """
    logger.debug(f"file_name: {file_name} | content length: {len(content)}")
    
    # Check if it's an absolute path
    if os.path.isabs(file_name):
        full_path = file_name
    else:
        # Get project root directory (up two levels from scripts)
        project_root = os.path.dirname(os.path.dirname(__file__))
        normalized_path = os.path.normpath(file_name)
        full_path = os.path.normpath(os.path.join(project_root, normalized_path))
    
    try:
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write content to file
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(content)
            
        logger.info(f"Successfully wrote to file: {full_path}")
    except IOError as e:
        logger.error(f"Error writing to file {full_path}: {e}")
        raise

def create_directory(directory_path: str) -> None:
    """
    Create a directory if it doesn't exist.
    
    Parameters:
        directory_path (str): Path to the directory to create
        
    Returns:
        None
    """
    logger.debug(f"directory_path: {directory_path}")
    
    try:
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)
            logger.info(f"Created directory: {directory_path}")
        else:
            logger.debug(f"Directory already exists: {directory_path}")
    except OSError as e:
        logger.error(f"Error creating directory {directory_path}: {e}")
        raise

def delete_non_hidden_file(file_path: str) -> bool:
    """
    Delete a non-hidden file.
    
    Parameters:
        file_path (str): Path to the file to delete
        
    Returns:
        bool: True if the file was deleted, False otherwise
    """
    logger.debug(f"file_path: {file_path}")
    
    try:
        # Check if path is a file and not hidden
        if os.path.isfile(file_path) and not os.path.basename(file_path).startswith('.'):
            os.unlink(file_path)
            logger.info(f"Deleted file: {file_path}")
            return True
        else:
            logger.debug(f"File not deleted (hidden or non-existent): {file_path}")
            return False
    except OSError as e:
        logger.error(f"Error deleting file {file_path}: {e}")
        return False

def delete_non_hidden_directory(dir_path: str) -> bool:
    """
    Delete a non-hidden directory.
    
    Parameters:
        dir_path (str): Path to the directory to delete
        
    Returns:
        bool: True if the directory was deleted, False otherwise
    """
    logger.debug(f"dir_path: {dir_path}")
    
    try:
        # Check if path is a directory and not hidden
        if os.path.isdir(dir_path) and not os.path.basename(dir_path).startswith('.'):
            shutil.rmtree(dir_path)
            logger.info(f"Deleted directory: {dir_path}")
            return True
        else:
            logger.debug(f"Directory not deleted (hidden or non-existent): {dir_path}")
            return False
    except OSError as e:
        logger.error(f"Error deleting directory {dir_path}: {e}")
        return False