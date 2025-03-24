"""
Agent Chat Tools

This module provides tools for managing agent conversations and task execution in a multi-agent system.

Functions:
    execute_agent_tasks(task: dict) -> tuple:
        Orchestrates the execution of tasks by configuring and initializing the appropriate agents.
        Sets up the agent order including a debug loop pattern of Tester -> Debugger -> Coder.
        
    setup_group_chat(agents: list, message: str = None, max_rounds: int = 3, agent_order: list = None) -> tuple:
        Creates and configures either a single-agent or multi-agent group chat based on the number of agents.
        Handles initialization of the chat with an optional starting message.
        
    setup_single_agent_chat(agent: object, user_proxy: object, message: str, max_rounds: int) -> tuple:
        Configures a chat environment for communication with a single agent.
        Useful for focused interactions with individual agents.
        
    setup_multi_agent_chat(agents: list, user_proxy: object, message: str, max_rounds: int, agent_order: list = None) -> tuple:
        Sets up a chat environment for multiple agents to communicate.
        Implements custom speaker selection logic to control the order of agent interactions.
"""

import logging
from typing import List, Dict, Any, Tuple, Optional, Callable, Set, Union

from autogen import GroupChat, GroupChatManager
from data.agents import project_manager, coder, tester, debugger, user_proxy

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration for debugging loops
num_debug_loops = 3

def execute_agent_tasks(task: Dict[str, Any]) -> Tuple[List[Any], Any]:
    """
    Execute all tasks for the agent team.
    
    Parameters:
        task (Dict[str, Any]): Task containing tasks and descriptions
        
    Returns:
        Tuple[List[Any], Any]: Tuple containing list of agents and chat manager
    """
    logger.debug(f"Processing task: {task['name']}")
    logger.debug(f"Task has {len(task['tasks'])} subtasks")
    
    tasks = task['tasks']
    
    # Create task list for the initial message
    tasks_list = "\n".join([f"- [{task['agent']}] {task['description']}" for task in tasks])
    
    initial_message = f"Task Description: {task['description']}\n\n"
    initial_message += f"Your Tasks:\n{tasks_list}"
    logger.debug(f"Created initial message with length: {len(initial_message)}")
    
    # Collect and order agents based on task requirements
    seen_agents: Set[str] = set()
    ordered_agents = []
    agent_order = []
    
    for subtask in tasks:
        agent_name = subtask['agent'].lower()
        agent_order.append(agent_name)
        
        if agent_name not in seen_agents:
            seen_agents.add(agent_name)
            logger.info(f"Adding agent: {agent_name}")
            
            agent_instances = {
                'coder': coder,
                'project_manager': project_manager,
                'tester': tester,
                'debugger': debugger
            }
            
            if agent_name in agent_instances:
                ordered_agents.append(agent_instances[agent_name])
    
    # Add debugger to the agent order if not already included
    if 'debugger' not in seen_agents:
        seen_agents.add('debugger')
        ordered_agents.append(debugger)
        agent_order.append('debugger')
        logger.info("Adding debugger agent")
    
    # Add debug loop pattern
    debug_loop = ['tester', 'debugger', 'coder'] * num_debug_loops
    logger.info(f"Adding debug loop pattern: Tester -> Debugger -> Coder ({num_debug_loops} iterations)")
    agent_order.extend(debug_loop)
    
    logger.info(f"Configured {len(ordered_agents)} unique agents")
    logger.debug(f"Agent order: {agent_order}")
    
    # Set up the group chat with the configured agents and order
    agents, manager = setup_group_chat(
        agents=ordered_agents,
        message=initial_message,
        max_rounds=99,
        agent_order=agent_order
    )
    
    logger.info(f"Group chat initialized with {len(agents)} agents")
    return agents, manager

def setup_group_chat(
    agents: List[Any], 
    message: Optional[str] = None, 
    max_rounds: int = 3, 
    agent_order: Optional[List[str]] = None
) -> Tuple[List[Any], Any]:
    """
    Initialize and return the group chat and its manager.
    
    Parameters:
        agents (List[Any]): List of agent instances
        message (Optional[str]): Initial message to start chat
        max_rounds (int): Maximum chat rounds
        agent_order (Optional[List[str]]): Order of agent turns
        
    Returns:
        Tuple[List[Any], Any]: Tuple containing list of agents and chat manager
    """
    logger.debug(f"Setting up group chat with {len(agents)} agents")
    logger.debug(f"Max rounds: {max_rounds}")
    
    if agent_order:
        logger.debug(f"Using custom agent order with {len(agent_order)} turns")
    
    # Determine if we need a single or multi-agent chat
    if len(agents) == 1:
        logger.info("Setting up single agent chat")
        return setup_single_agent_chat(agents[0], user_proxy, message, max_rounds)
    else:
        logger.info(f"Setting up multi-agent chat with {len(agents)} agents")
        return setup_multi_agent_chat(agents, user_proxy, message, max_rounds, agent_order)

def setup_single_agent_chat(
    agent: Any, 
    user_proxy: Any, 
    message: Optional[str], 
    max_rounds: int
) -> Tuple[List[Any], Any]:
    """
    Set up chat for single agent communication.
    
    Parameters:
        agent (Any): Agent instance
        user_proxy (Any): User proxy agent
        message (Optional[str]): Initial message
        max_rounds (int): Maximum chat rounds
        
    Returns:
        Tuple[List[Any], Any]: Tuple containing list with single agent and chat manager
    """
    logger.debug(f"Configuring single agent chat with {agent.name}")
    
    # Create agent list with user proxy and the single agent
    temp_agents = [user_proxy, agent]
    
    # Configure the group chat
    groupchat = GroupChat(
        agents=temp_agents,
        messages=[],
        max_round=max_rounds,
        speaker_selection_method="auto",
        allow_repeat_speaker=True
    )
    
    # Create the chat manager
    manager = GroupChatManager(groupchat=groupchat)
    logger.info("Created GroupChat and GroupChatManager for single agent")
    
    # Initiate the chat if a message was provided
    if message:
        logger.info("Initiating chat with provided message")
        user_proxy.initiate_chat(manager, message=message)
    
    # Log token usage
    agent.print_usage_summary()
    user_proxy.print_usage_summary()
    
    return [agent], manager

def setup_multi_agent_chat(
    agents: List[Any], 
    user_proxy: Any, 
    message: Optional[str], 
    max_rounds: int, 
    agent_order: Optional[List[str]] = None
) -> Tuple[List[Any], Any]:
    """
    Set up chat for multiple agent communication.
    
    Parameters:
        agents (List[Any]): List of agent instances
        user_proxy (Any): User proxy agent
        message (Optional[str]): Initial message
        max_rounds (int): Maximum chat rounds
        agent_order (Optional[List[str]]): Order of agent turns
        
    Returns:
        Tuple[List[Any], Any]: Tuple containing list of agents and chat manager
    """
    logger.debug(f"Configuring multi-agent chat with {len(agents)} agents")
    
    # Combine user proxy with agents
    all_agents = [user_proxy] + agents
    
    def custom_speaker_selection_func(last_speaker: Any, groupchat: GroupChat) -> Any:
        """
        Define a customized speaker selection function.
        
        Parameters:
            last_speaker (Any): The agent who spoke last
            groupchat (GroupChat): The group chat instance
            
        Returns:
            Any: The next agent to speak
        """
        messages = groupchat.messages
        logger.debug(f"Selecting next speaker after {last_speaker.name}, message count: {len(messages)}")
        
        # For the first message, select the first agent
        if not messages:
            logger.debug(f"First message - selecting first agent: {agents[0].name}")
            return agents[0]
        
        # Use agent_order if provided
        if agent_order:
            message_index = len(messages) // 3
            agent_index = message_index % len(agent_order)
            agent_name = agent_order[agent_index].lower()
            
            # Find the agent with the matching name
            selected_agent = next(
                (agent for agent in agents if agent.name.lower() == agent_name),
                agents[0]
            )
            
            logger.debug(f"Selected agent by order: {selected_agent.name}")
            return selected_agent
        
        # Default rotation if no agent_order provided
        selected_agent = agents[(len(messages) // 3) % len(agents)]
        logger.debug(f"Selected agent by default rotation: {selected_agent.name}")
        return selected_agent
    
    # Configure the group chat with custom speaker selection
    groupchat = GroupChat(
        agents=all_agents,
        messages=[],
        max_round=max_rounds,
        speaker_selection_method=custom_speaker_selection_func,
        allow_repeat_speaker=True
    )
    
    # Create the chat manager
    manager = GroupChatManager(groupchat=groupchat)
    logger.info("Created GroupChat and GroupChatManager for multi-agent chat")
    
    # Initiate the chat if a message was provided
    if message:
        logger.info("Initiating chat with provided message")
        user_proxy.initiate_chat(manager, message=message)
    
    # Log token usage for all agents
    for agent in agents:
        agent.print_usage_summary()
    user_proxy.print_usage_summary()
    
    return agents, manager