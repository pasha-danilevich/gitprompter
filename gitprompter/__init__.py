"""gitprompter"""
from gitprompter.config import GitPrompterConfig
config = GitPrompterConfig()

from gitprompter.core import GitDiffProcessor
from gitprompter.prompts import Prompt


processor = GitDiffProcessor(
    config=config,
    prompt=Prompt(config)
)