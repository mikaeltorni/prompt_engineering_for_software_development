"""
Agent Definitions

This module defines the core agents used in the multi-agent programming system.

The agents work together to plan, implement, test and debug code:

Variables:
    user_proxy: A dummy agent used to initiate conversations
    project_manager: Creates and manages detailed project plans, delegating tasks to other agents
    coder: Implements code based on project requirements and specifications
    tester: Validates code functionality through testing
    debugger: Helps identify and fix issues in the code

Each agent is configured with specific capabilities, LLM models, and function mappings
to enable their specialized roles in the development process.
"""

import autogen

from scripts.agent_tools import update_project_plan, write_file_content, test_file
from data.models import gpt4omini_deterministic, claude_35_sonnet_new_deterministic
from scripts.file_tools import read_file
from scripts.project_tools import prompt_combiner
from langchain_core.prompts import PromptTemplate

user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "output", "use_docker": False},
    system_message="Dummy to start the chat",
)

project_manager = autogen.AssistantAgent(
    name="Project_Manager",
    system_message=PromptTemplate.from_template(read_file("data/prompts/system/project_manager_prompt.md")).template,
    llm_config=gpt4omini_deterministic,
    code_execution_config=False,
    human_input_mode="NEVER",
    function_map={
        "update_project_plan": update_project_plan,
    },
)

project_manager.register_for_llm(name="update_project_plan", description="Updates the project plan with the given information.")(update_project_plan)

coder = autogen.AssistantAgent(
    name="Coder",
    system_message=PromptTemplate.from_template(
        # Combining the coder instructions and the coder agentic part
        prompt_combiner(
            "prompt_development_and_testing/prompts/system/coder_instructions.xml",
            "multi_agentic_system_for_programming/data/prompts/system/coder_agentic_part.xml"
        )
    ).template,
    llm_config=claude_35_sonnet_new_deterministic,
    code_execution_config=False,
    human_input_mode="NEVER",
    function_map={
        "write_file_content": write_file_content,
    },
    is_termination_msg=lambda msg: msg.get("content") and "TERMINATE" in msg["content"],
)

coder.register_for_llm(name="write_file_content", description="Writes content to a file given its name.")(write_file_content)

tester = autogen.AssistantAgent(
    name="Tester",
    system_message=PromptTemplate.from_template(read_file("data/prompts/system/tester_prompt.md")).template,
    llm_config=gpt4omini_deterministic,
    human_input_mode="NEVER",
    function_map={
        "test_file": test_file,
    },
    is_termination_msg=lambda msg: msg.get("content") and "TERMINATE" in msg["content"],
)

tester.register_for_llm(name="test_file", description="Tests a Python file by reading its content and executing it.")(test_file)

debugger = autogen.AssistantAgent(
    name="Debugger",
    system_message=PromptTemplate.from_template(read_file("data/prompts/system/debugger_prompt.xml")).template,
    llm_config=claude_35_sonnet_new_deterministic,
    code_execution_config=False,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: msg.get("content") and "TERMINATE" in msg["content"],
)