"""
XML Parsing Tools

This module provides utilities for parsing XML project plan files in a multi-agent programming system.

The module handles parsing of project_plan.xml files that define tasks and their delegation to different agents.
It extracts structured task information including descriptions, assigned agents, and subtasks.

Functions:
    parse_project_plan(project_dir: str) -> list:
        Parses a project_plan.xml file from the given directory.
        Returns a list of parsed task dictionaries.
        
    parse_task(task_element: ElementTree.Element) -> dict:
        Parses a single task XML element into a task dictionary.
        Returns task with description and assigned agent.
        
    parse_root_as_task(root_element: ElementTree.Element) -> dict:
        Parses the root project plan element as a high-level task.
        Returns task with name, description, delegated agents and subtasks.
"""

import os
import logging
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_project_plan(project_dir: str) -> List[Dict[str, Any]]:
    """
    Parse project_plan.xml and return task details.
    
    Parameters:
        project_dir (str): Directory containing the project_plan.xml file
        
    Returns:
        List[Dict[str, Any]]: List of parsed task dictionaries
    """
    logger.debug(f"project_dir: {project_dir}")
    
    project_plan_path = os.path.join(project_dir, "project_plan.xml")
    
    if not os.path.exists(project_plan_path):
        logger.error(f"Project plan file not found: {project_plan_path}")
        return []
    
    try:
        tree = ET.parse(project_plan_path)
        root = tree.getroot()
        
        if root.tag != 'project_plan':
            logger.error("Root element must be 'project_plan'")
            return []
        
        # Create a single task from the project plan root
        task = parse_root_as_task(root)
        tasks = [task] if task else []
            
        logger.debug(f"Parsed {len(tasks)} tasks")
        return tasks
    except ET.ParseError as e:
        logger.error(f"XML parsing error: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error parsing project plan: {e}")
        return []

def parse_task(task_element: ET.Element) -> Optional[Dict[str, str]]:
    """
    Parse a single task from XML.
    
    Parameters:
        task_element (ET.Element): XML element representing a task
        
    Returns:
        Optional[Dict[str, str]]: Dictionary with task description and agent, or None if parsing fails
    """
    logger.debug(f"Parsing task element: {task_element.tag}")
    
    if task_element is None:
        logger.error("Task element is None")
        return None
    
    name = task_element.find('name')
    delegated_to = task_element.find('delegatedTo')
    
    if name is None or name.text is None or delegated_to is None or delegated_to.text is None:
        logger.error("Missing or empty required fields (name or delegatedTo)")
        return None
    
    task = {
        'description': name.text,
        'agent': delegated_to.text
    }
    logger.debug(f"Parsed task: description='{task['description']}', agent='{task['agent']}'")
    return task

def parse_root_as_task(root_element: ET.Element) -> Optional[Dict[str, Any]]:
    """
    Parse the project plan root element as a task.
    
    Parameters:
        root_element (ET.Element): Root XML element of the project plan
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary with task details, or None if parsing fails
    """
    logger.debug(f"Parsing root element: {root_element.tag}")
    
    if root_element is None:
        logger.error("Root element is None")
        return None
    
    # Required fields
    name = root_element.find('name')
    description = root_element.find('description')
    
    if name is None or name.text is None or description is None or description.text is None:
        logger.error("Missing or empty required fields (name or description)")
        return None
        
    task = {
        'name': name.text,
        'description': description.text,
        'delegatedTo': [],
        'tasks': []
    }
    
    # Parse delegated agents
    delegated_to = root_element.find('delegatedTo')
    if delegated_to is not None:
        for agent in delegated_to.findall('agent'):
            if agent.text:
                task['delegatedTo'].append(agent.text)
    
    # Parse tasks
    tasks_element = root_element.find('tasks')
    if tasks_element is not None:
        for task_elem in tasks_element.findall('task'):
            parsed_task = parse_task(task_elem)
            if parsed_task:
                task['tasks'].append(parsed_task)
    
    logger.debug(f"Parsed project task: name='{task['name']}', {len(task['tasks'])} subtasks, {len(task['delegatedTo'])} agents")
    return task
