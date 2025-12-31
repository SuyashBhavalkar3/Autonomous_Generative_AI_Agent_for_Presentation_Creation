# agents/registry.py

from .executor.research_agent import research_agent
from .executor.content_agent import content_agent
from .executor.image_agent import image_agent
from .executor.slide_agent import slide_agent
from .executor.ppt_executor_agent import executor_agent

ALLOWED_AGENTS = {
    "research_agent",
    "content_agent",
    "image_agent",
    "slide_agent",
    "executor_agent",
    "code_agent"
}

AGENT_REGISTRY = {
    "research_agent": research_agent,
    "content_agent": content_agent,
    "image_agent": image_agent,
    "slide_agent": slide_agent,
    "executor_agent": executor_agent,
    # "code_agent": code_agent  # add when implemented
}