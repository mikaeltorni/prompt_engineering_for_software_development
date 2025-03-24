"""
Project Tools

This module provides utilities for managing project directories and files in a multi-agent programming system.

Functions:
    check_empty_project(project_dir: str) -> None:
        Checks if a project directory is empty (excluding hidden files) and prints a warning if so.
        
    reset_project_files(project_dir: str) -> None:
        Removes all non-hidden files and directories from the project directory to reset it.
        
    setup_project_directory(root_dir: str, src_dir: str, project_name: str) -> tuple:
        Creates the main project directory structure including source and database directories.
        Returns tuple of (project_dir, db_dir).
        
    initialize_project_plan(project_dir: str) -> bool:
        Creates an empty project_plan.xml file if it doesn't exist.
        Returns True if file already existed, False if newly created.
        
    prompt_combiner(prompt1_path: str, prompt2_path: str) -> str:
        Combines content from two prompt files into a single string with a newline separator.
        Returns the combined content.
"""

import os
import logging
from typing import Tuple, List

from scripts.file_tools import delete_non_hidden_file, delete_non_hidden_directory, create_directory, read_file

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s')
logger = logging.getLogger(__name__)

def check_empty_project(project_dir: str) -> List[str]:
    """
    Check and warn if project directory is empty.
    
    Parameters:
        project_dir (str): Path to the project directory to check
        
    Returns:
        List[str]: List of non-hidden files in the project directory
    """
    logger.debug(f"project_dir: {project_dir}")
    
    project_files = [f for f in os.listdir() if not f.startswith('.')]
    
    if not project_files:
        logger.warning(f"The directory '{project_dir}' is empty (excluding hidden files).")
    
    logger.debug(f"Found {len(project_files)} non-hidden files")
    return project_files

def reset_project_files(project_dir: str) -> None:
    """
    Reset the project directory by removing non-hidden files.
    
    Parameters:
        project_dir (str): Path to the project directory to reset
        
    Returns:
        None
    """
    logger.debug(f"project_dir: {project_dir}")
    
    removed_count = 0
    for item in os.listdir(project_dir):
        item_path = os.path.join(project_dir, item)
        if delete_non_hidden_file(item_path) or delete_non_hidden_directory(item_path):
            removed_count += 1
    
    logger.info(f"Deleted {removed_count} non-hidden files/directories in {project_dir}")

def setup_project_directory(root_dir: str, src_dir: str, project_name: str) -> Tuple[str, str]:
    """
    Set up the project directory structure.
    
    Parameters:
        root_dir (str): Root directory of the application
        src_dir (str): Source directory name
        project_name (str): Name of the project
        
    Returns:
        Tuple[str, str]: Tuple containing (project_dir, db_dir)
    """
    logger.debug(f"root_dir: {root_dir} | src_dir: {src_dir} | project_name: {project_name}")
    
    project_dir = os.path.join(root_dir, src_dir, project_name)
    db_dir = os.path.join(project_dir, ".db")
    
    create_directory(project_dir)
    logger.info(f"Created or verified project directory: {project_dir}")
    
    create_directory(db_dir)
    logger.info(f"Created or verified database directory: {db_dir}")
    
    return project_dir, db_dir

def initialize_project_plan(project_dir: str) -> bool:
    """
    Create empty project_plan.xml if it doesn't exist.
    
    Parameters:
        project_dir (str): Path to the project directory
        
    Returns:
        bool: True if file already existed, False if newly created
    """
    logger.debug(f"project_dir: {project_dir}")
    
    project_plan_path = os.path.join(project_dir, "project_plan.xml")
    
    if not os.path.exists(project_plan_path):
        try:
            with open(project_plan_path, "w") as f:
                f.write("")
            logger.info(f"Created new project_plan.xml at {project_plan_path}")
            return False
        except Exception as e:
            logger.error(f"Failed to create project_plan.xml: {e}")
            raise
    
    logger.info(f"Project plan already exists at {project_plan_path}")
    return True

def prompt_combiner(prompt1_path: str, prompt2_path: str) -> str:
    """
    Combines two prompt files into a single string with a newline between them.
    
    Parameters:
        prompt1_path (str): Path to the first prompt file
        prompt2_path (str): Path to the second prompt file
    
    Returns:
        str: Combined prompt content with a newline between them
    """
    logger.debug(f"prompt1_path: {prompt1_path} | prompt2_path: {prompt2_path}")
    
    # Get the absolute path to the project workspace root
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    # Resolve paths relative to workspace root
    prompt1_abs_path = os.path.join(workspace_root, prompt1_path)
    prompt2_abs_path = os.path.join(workspace_root, prompt2_path)
    
    logger.debug(f"Resolved prompt1_abs_path: {prompt1_abs_path}")
    logger.debug(f"Resolved prompt2_abs_path: {prompt2_abs_path}")
    
    if not os.path.exists(prompt1_abs_path):
        logger.error(f"First prompt file not found: {prompt1_abs_path}")
        raise FileNotFoundError(f"File not found: {prompt1_path}")
        
    if not os.path.exists(prompt2_abs_path):
        logger.error(f"Second prompt file not found: {prompt2_abs_path}")
        raise FileNotFoundError(f"File not found: {prompt2_path}")
    
    prompt1_content = read_file(prompt1_abs_path)
    prompt2_content = read_file(prompt2_abs_path)
    
    combined_content = f"{prompt1_content}\n\n{prompt2_content}"
    logger.debug(f"Combined content length: {len(combined_content)}")
    
    return combined_content