from dataclasses import dataclass, fields
from typing import Literal, Optional
from pathlib import Path
import tomllib

class PyprojectTomlConfig:
    name: str

    @classmethod
    def load_config(cls) -> Optional[dict]:

        current_dir = Path.cwd()
        config_file = None

        for path in [current_dir] + list(current_dir.parents):
            potential_file = path / "pyproject.toml"
            if potential_file.exists():
                config_file = potential_file
                break

        if config_file:
            try:
                with open(config_file, 'rb') as f:
                    data = tomllib.load(f)
                tool_config = data.get('tool', {}).get(cls.name, {})

                return tool_config
            except (FileNotFoundError, tomllib.TOMLDecodeError, KeyError):
                pass


        return None


@dataclass
class GitPrompterConfig(PyprojectTomlConfig):
    def __init__(self):
        data = self.load_config()

        if data:
            for field in fields(self):
                if field.name in data:
                    setattr(self, field.name, data[field.name])

    name = 'gitprompter'

    style: Literal["feature", "conventional", "compact"] = "conventional"
    to_file: bool = False
    language: str = "ru"
    default_branch: str = "main"
    analysis: bool = False

