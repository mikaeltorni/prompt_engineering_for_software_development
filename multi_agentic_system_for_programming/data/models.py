"""
Language Model Configurations

This module defines the configuration settings for the language models used in the multi-agent system.

The module provides two model configurations:
1. gpt4omini_deterministic - OpenAI GPT-4o mini model configuration
2. claude_35_sonnet_new_deterministic - Anthropic Claude 3.5 Sonnet model configuration

Note: API keys for both OpenAI and Anthropic must be set in the environment variables
to use these models.

Variables:
    gpt4omini_deterministic: Configuration dictionary for GPT-4o mini model
    claude_35_sonnet_new_deterministic: Configuration dictionary for Claude 3.5 Sonnet model
"""

import os
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(funcName)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check for API keys in environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    logger.warning("OPENAI_API_KEY not found in environment variables")

anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY") 
if not anthropic_api_key:
    logger.warning("ANTHROPIC_API_KEY not found in environment variables")

# Model configurations
gpt4omini_deterministic: Dict[str, Any] = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": openai_api_key,
            "api_type": "openai",
        }
    ],
    "temperature": 0,
    "max_tokens": 16384,
}

claude_35_sonnet_new_deterministic: Dict[str, Any] = {
    "config_list": [
        {
            "model": "claude-3-5-sonnet-20240620",
            "api_key": anthropic_api_key,
            "api_type": "anthropic",
        }
    ],
    "temperature": 0,
    "max_tokens": 8192,
}