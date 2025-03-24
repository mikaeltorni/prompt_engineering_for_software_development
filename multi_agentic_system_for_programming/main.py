"""
Main entry point for the multi-agent programming system.

This module orchestrates the overall execution flow of the multi-agent programming system.
It handles project initialization, task delegation, and agent communication to generate code
based on user prompts.

Functions:
    main(project_name: str, src_dir: str, reset_db: bool, prompt: str = None) -> list:
        Initializes and runs the main program flow. Sets up project directories,
        initializes agents, parses tasks, and executes them through the agent system.
        Returns the list of completed tasks.

The module uses a combination of project management tools, agent communication systems,
and file handling utilities to:
1. Set up project directory structure
2. Initialize or reset project state
3. Process user requirements via prompts
4. Delegate tasks to appropriate agents
5. Execute the multi-agent programming workflow

Command-line arguments:
    --project: Name of the project to work on (default: from project_config)
    --src: Source directory to work in (default: from project_config)
    --reset: Flag to reset database and delete non-hidden project files
    --prompt: Optional custom prompt or path to prompt file
"""

import os
import argparse
import logging
from typing import List, Dict, Any, Optional

from scripts.agent_chat_tools import setup_group_chat, execute_agent_tasks
from scripts.file_tools import read_file
from scripts.project_tools import setup_project_directory, reset_project_files, check_empty_project, initialize_project_plan
from scripts.xml_parsing_tools import parse_project_plan
from data.project_config import PROJECT_NAME, SRC_DIR
from data.agents import project_manager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s')
logger = logging.getLogger(__name__)

def main(project_name: str, src_dir: str, reset_db: bool, prompt: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Initializes and runs the main program flow.

    Parameters:
        project_name (str): Name of the project to work on
        src_dir (str): Source directory to work in
        reset_db (bool): Flag to reset database and delete non-hidden project files
        prompt (Optional[str]): Custom prompt or path to prompt file

    Returns:
        List[Dict[str, Any]]: List of completed tasks
    """
    logger.debug(f"project_name: {project_name} | src_dir: {src_dir} | reset_db: {reset_db} | prompt: {prompt}")
    
    if not src_dir:
        src_dir = "src"
        logger.info(f"Using default source directory: {src_dir}")
    
    # Set up project directories
    root_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir, db_dir = setup_project_directory(root_dir, src_dir, project_name)
    logger.info(f"Project directory: {project_dir} | Database directory: {db_dir}")
    
    # Reset project files if requested
    if reset_db:
        reset_project_files(project_dir)
        logger.info(f"Reset completed for project directory: {project_dir}")
    
    # Change to project directory and verify
    os.chdir(project_dir)
    check_empty_project(project_dir)
    logger.debug(f"Changed to and verified project directory: {project_dir}")
    
    # Initialize project plan
    initialize_project_plan(project_dir)
    logger.info(f"Initialized project plan in: {project_dir}")

    # Load default prompt if none provided
    if prompt is None:
        # User prompt is in the prompt_development_and_testing directory
        workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        user_prompt_path = os.path.join(workspace_root, "prompt_development_and_testing", "prompts", "user", "calculator_no_gui_prompt.txt")
        prompt = read_file(user_prompt_path)
        logger.info(f"Using default prompt from: {user_prompt_path}")
    elif os.path.exists(prompt) and not prompt.startswith('"') and not prompt.endswith('"'):
        prompt = read_file(prompt)
        logger.info(f"Loaded prompt from file: {prompt}")

    # Start group chat with project manager
    chat_result = setup_group_chat(
        agents=[project_manager],
        message=prompt,
        max_rounds=3
    )
    logger.info(f"Group chat completed with result: {chat_result}")

    # Parse and execute tasks
    tasks = parse_project_plan(project_dir)
    logger.info(f"Parsed {len(tasks)} tasks from project plan")
    
    for task in tasks:
        logger.info(f"Executing task: {task['name']}")
        result = execute_agent_tasks(task)
        logger.info(f"Task '{task['name']}' completed with result: {result}")
    
    return tasks

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the Codering Assistant with a specific project name and source directory.")
    parser.add_argument("--project", help="The name of the project to work on", default=PROJECT_NAME)
    parser.add_argument("--src", help="The source directory to work in", default=SRC_DIR)
    parser.add_argument("--reset", action="store_true", help="Reset the database and delete all non-hidden files in the project directory")
    parser.add_argument("--prompt", help="Override the default prompt with a custom one or path to prompt file", default=None)
    
    args = parser.parse_args()
    logger.debug(f"Command-line arguments: project={args.project}, src={args.src}, reset={args.reset}, prompt={args.prompt}")

    # Run main program
    main(args.project, args.src, args.reset, args.prompt)
