"""
XML Task Parser and Analyzer

This module provides functionality to parse and analyze XML files containing project task definitions.
It processes XML files in a specified directory, validates their structure, and generates a detailed
analysis report.

The XML files should follow a specific schema with a root 'project_plan' element containing:
- name: Task/project name
- description: Task/project description  
- delegatedTo: List of agents assigned to the task
- tasks: List of subtasks with name and delegatedTo fields

Functions:
    format_subtask(task: Dict) -> str:
        Formats a single subtask into a readable string representation.
        
    format_project_plan(task: Dict) -> str:
        Formats the complete project plan including all subtasks into a readable string.
        
    parse_xml_file(file_path: str) -> Tuple[List[Dict], str]:
        Parses a single XML file and returns the extracted tasks and any error messages.
        
    process_directory(directory_path: str, output_file: str) -> None:
        Processes all XML files in a directory and writes analysis results to an output file.
        
    run_interactive_mode() -> None:
        Runs the program in interactive mode, allowing the user to process multiple directories.
        
    main() -> None:
        Command-line interface to run the XML parsing and analysis.

Command-line arguments:
    --dir, -d: Directory containing XML files to process (default: current directory)
    --output, -o: Output file path for analysis report (default: task_analysis_<timestamp>.txt)
    --interactive, -i: Run in interactive mode, allowing the user to process multiple directories.

Example usage:
    # Process XML files in the current directory with default output file
    python parse_xml_files_to_the_task_format.py
    
    # Process XML files in a specific directory
    python parse_xml_files_to_the_task_format.py --dir /path/to/xml/files
    
    # Process XML files and save report to a specific file
    python parse_xml_files_to_the_task_format.py -d /path/to/xml/files -o /path/to/output.txt
    
    # Run in interactive mode
    python parse_xml_files_to_the_task_format.py --interactive
"""

import sys
import logging
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Any
import argparse
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s')
logger = logging.getLogger(__name__)

def format_subtask(task: Dict[str, str]) -> str:
    """
    Formats a single task into a readable string representation.
    
    Parameters:
        task (Dict[str, str]): Dictionary containing task description and agent info
        
    Returns:
        str: Formatted string representation of the subtask
    """
    logger.debug(f"task: {task}")
    
    if not isinstance(task, dict):
        logger.error("Task must be a dictionary")
        raise TypeError("Task must be a dictionary")
    
    if 'description' not in task or 'agent' not in task:
        logger.error("Task dictionary must contain 'description' and 'agent' keys")
        raise ValueError("Task dictionary must contain 'description' and 'agent' keys")
    
    result = f"  - {task['description']} (Delegated to: {task['agent']})"
    
    logger.debug(f"result: {result}")
    return result

def format_project_plan(task: Dict[str, Any]) -> str:
    """
    Formats the complete project plan including all subtasks into a readable string.
    
    Parameters:
        task (Dict[str, Any]): Dictionary containing task details including name, description, 
                              delegatedTo list, and subtasks
        
    Returns:
        str: Formatted string representation of the complete project plan
    """
    logger.debug(f"task name: {task.get('name')} | subtasks count: {len(task.get('tasks', []))}")
    
    if not isinstance(task, dict):
        logger.error("Task must be a dictionary")
        raise TypeError("Task must be a dictionary")
    
    required_keys = ['name', 'description', 'delegatedTo', 'tasks']
    for key in required_keys:
        if key not in task:
            logger.error(f"Task dictionary must contain '{key}' key")
            raise ValueError(f"Task dictionary must contain '{key}' key")
    
    lines = []
    lines.append(f"Task: {task['name']}")
    lines.append(f"Delegated to: {', '.join(task['delegatedTo'])}")
    lines.append(f"Description: {task['description']}")
    lines.append("Tasks:")
    
    for subtask in task['tasks']:
        try:
            lines.append(format_subtask(subtask))
        except (TypeError, ValueError) as e:
            logger.error(f"Error formatting subtask: {e}")
            lines.append(f"  - Error formatting subtask: {e}")
    
    result = '\n'.join(lines)
    
    logger.debug(f"result length: {len(result)}")
    return result

def parse_xml_file(file_path: str) -> Tuple[List[Dict[str, Any]], str]:
    """
    Parses a single XML file and returns the extracted tasks and any error messages.
    
    Parameters:
        file_path (str): Path to the XML file to be parsed
        
    Returns:
        Tuple[List[Dict[str, Any]], str]: Tuple containing a list of parsed task dictionaries 
                                         and an error message (empty if successful)
    """
    logger.debug(f"file_path: {file_path}")
    
    if not isinstance(file_path, str):
        error_msg = "File path must be a string"
        logger.error(error_msg)
        return [], error_msg
    
    file = Path(file_path)
    if not file.exists():
        error_msg = f"File not found: {file_path}"
        logger.error(error_msg)
        return [], error_msg
    
    if not file.is_file():
        error_msg = f"Not a file: {file_path}"
        logger.error(error_msg)
        return [], error_msg
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        if root.tag != 'project_plan':
            error_msg = "Root element must be 'project_plan'"
            logger.error(error_msg)
            return [], error_msg
        
        # Required fields
        name = root.find('name')
        description = root.find('description')
        
        if name is None or description is None:
            error_msg = f"Missing required fields (name or description) in {file.name}"
            logger.error(error_msg)
            return [], error_msg
        
        task_dict = {
            'name': name.text if name.text is not None else "",
            'description': description.text if description.text is not None else "",
            'delegatedTo': [],
            'tasks': []
        }
        
        # Parse delegated agents
        delegated_to = root.find('delegatedTo')
        if delegated_to is not None:
            for agent in delegated_to.findall('agent'):
                if agent.text:
                    task_dict['delegatedTo'].append(agent.text)
        
        # Parse tasks
        tasks_element = root.find('tasks')
        if tasks_element is not None:
            for task in tasks_element.findall('task'):
                task_name = task.find('name')
                task_agent = task.find('delegatedTo')
                
                if task_name is None or task_agent is None:
                    error_msg = f"Missing required fields in task (name or delegatedTo) in {file.name}"
                    logger.error(error_msg)
                    return [], error_msg
                
                if task_name.text is None or task_agent.text is None:
                    error_msg = f"Empty name or delegatedTo field in task in {file.name}"
                    logger.error(error_msg)
                    return [], error_msg
                
                task_dict['tasks'].append({
                    'description': task_name.text,
                    'agent': task_agent.text
                })
        
        logger.debug(f"output: {len(task_dict['tasks'])} tasks parsed successfully")
        return [task_dict], ""
        
    except ET.ParseError as e:
        error_msg = f"XML parsing error in {file.name}: {str(e)}"
        logger.error(error_msg)
        return [], error_msg
    except Exception as e:
        error_msg = f"Unexpected error in {file.name}: {str(e)}"
        logger.error(error_msg)
        return [], error_msg

def process_directory(directory_path: str, output_file: str) -> None:
    """
    Process all XML files in the specified directory and write results to output file.
    
    Parameters:
        directory_path (str): Path to the directory containing XML files
        output_file (str): Path where the output analysis report will be written
        
    Returns:
        None
    """
    logger.debug(f"directory_path: {directory_path} | output_file: {output_file}")
    
    if not isinstance(directory_path, str) or not isinstance(output_file, str):
        logger.error("Both directory_path and output_file must be strings")
        return
    
    dir_path = Path(directory_path)
    if not dir_path.exists():
        logger.error(f"Directory '{directory_path}' does not exist.")
        return
    
    if not dir_path.is_dir():
        logger.error(f"'{directory_path}' is not a directory.")
        return
    
    # Find all XML files in the directory
    xml_files = list(dir_path.glob('*.xml'))
    
    if not xml_files:
        logger.info(f"No XML files found in directory: {directory_path}")
        return
    
    successful_files = []
    failed_files = {}
    
    # Create output file directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create or open the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"XML Task Analysis Report\nGenerated: {timestamp}\nDirectory: {directory_path}\n\n"
            f.write(header)
            logger.info(header.strip())

            for xml_file in xml_files:
                separator = f"\n===[{xml_file.name}]===\n"
                f.write(separator)
                logger.info(separator.strip())
                
                try:
                    tasks, error_msg = parse_xml_file(str(xml_file))
                    if error_msg:
                        failed_files[xml_file.name] = error_msg
                        error_output = f"Error processing {xml_file.name}: {error_msg}\n"
                        f.write(error_output)
                        logger.error(error_output.strip())
                    else:
                        successful_files.append(xml_file.name)
                        for task in tasks:
                            formatted_task = format_project_plan(task)
                            f.write("\n" + formatted_task + "\n\n")
                            logger.info(f"Successfully processed {xml_file.name}")
                except Exception as e:
                    failed_files[xml_file.name] = str(e)
                    error_output = f"Error processing {xml_file.name}: {str(e)}\n"
                    f.write(error_output)
                    logger.error(error_output.strip())
                
                end_separator = "=" * (len(xml_file.name) + 8)  # Match the header length
                f.write(end_separator + "\n")
                logger.info(end_separator)
            
            # Write detailed summary
            total_files = len(xml_files)
            success_count = len(successful_files)
            failed_count = len(failed_files)
            
            success_percentage = (success_count/total_files)*100 if total_files > 0 else 0
            
            summary = f"\nAnalysis Summary:"
            summary += f"\n- Total XML files processed: {total_files}"
            summary += f"\n- Successfully parsed: {success_count}/{total_files} ({success_percentage:.1f}%)"
            
            if failed_files:
                summary += "\n\nFailed files and reasons:"
                for file, reason in failed_files.items():
                    summary += f"\n- {file}: {reason}"
            
            f.write(summary)
            logger.info(summary)
            
    except IOError as e:
        logger.error(f"Error writing to output file: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    logger.debug(f"Completed processing {len(xml_files)} files | Successful: {len(successful_files)} | Failed: {len(failed_files)}")

def run_interactive_mode() -> None:
    """
    Run the program in interactive mode, allowing the user to provide input and process multiple directories.
    
    Parameters:
        None
        
    Returns:
        None
    """
    logger.debug("Starting interactive mode")
    
    while True:
        print("\nXML Task Parser and Analyzer - Interactive Mode")
        print("1. Process XML files in a directory")
        print("2. Exit")
        
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == '2':
            logger.info("Exiting program")
            break
        
        if choice == '1':
            directory_path = input("Enter the directory path containing XML files: ").strip()
            output_file = input("Enter the output file path (press Enter for default): ").strip()
            
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"task_analysis_{timestamp}.txt"
            
            logger.info(f"Processing directory: {directory_path}")
            process_directory(directory_path, output_file)
        else:
            logger.warning("Invalid choice. Please enter 1 or 2.")
    
def main() -> None:
    """
    Main function to process XML files in the specified or current directory.
    
    Parameters:
        None
        
    Returns:
        None
    """
    logger.debug("Starting XML Task Parser and Analyzer")
    
    parser = argparse.ArgumentParser(description="Parse XML files in a directory and format their task contents.")
    parser.add_argument("--dir", "-d", 
                       help="Path to the directory containing XML files. If not provided, uses current directory.",
                       default=None)
    parser.add_argument("--output", "-o",
                       help="Output file path. If not provided, uses 'task_analysis_<timestamp>.txt' in current directory.",
                       default=None)
    parser.add_argument("--interactive", "-i", 
                       help="Run in interactive mode",
                       action="store_true")
    
    args = parser.parse_args()
    
    if args.interactive:
        run_interactive_mode()
        return
    
    # If not interactive and no directory specified, use current directory
    directory_path = args.dir if args.dir else str(Path.cwd())
    directory_path = str(Path(directory_path).resolve())
    
    # Generate default output filename if not provided
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = str(Path.cwd() / f"task_analysis_{timestamp}.txt")
    else:
        output_file = str(Path(args.output).resolve())
    
    logger.info(f"Processing XML files in directory: {directory_path}")
    logger.info(f"Output will be saved to: {output_file}")
    
    process_directory(directory_path, output_file)
    logger.info("XML Task Parser and Analyzer completed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
