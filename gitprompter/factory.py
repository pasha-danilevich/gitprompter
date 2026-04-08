from typing import Literal

from gitprompter.config import GitPrompterConfig
from gitprompter.core import GitDiffProcessor
from gitprompter.prompts import Prompt


def build_processor(style: Literal["feature", "conventional", "compact"], analysis: bool) -> GitDiffProcessor:
    config = GitPrompterConfig()

    if style:
        config.style = style

    config.analysis = analysis

    return GitDiffProcessor(
        config=config,
        prompt=Prompt(config)
    )
