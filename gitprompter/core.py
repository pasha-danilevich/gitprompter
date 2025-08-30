import subprocess
import sys
from typing import Optional

import click

from gitprompter import utils, GitPrompterConfig
from gitprompter.prompts import Prompt


class GitDiffProcessor:
    """
    Класс для обработки git diff и создания промптов на основе изменений.

    Обеспечивает унифицированный интерфейс для работы с git diff, git diff --cached,
    и сравнения между ветками с обработкой ошибок и логированием.

    """

    BASE_PARAMS = {
        'capture_output': True,
        'text': True,
        'encoding': 'utf-8',
        'errors': 'replace',  # Обработка проблем с кодировкой
        'shell': sys.platform == 'win32',  # Используем shell=True только на Windows
    }

    def __init__(self, config: GitPrompterConfig, prompt: Prompt):
        self.config = config
        self.prompt = prompt

    def _run_git_command(self, commands: list[str]) -> Optional[str]:
        """
        Выполняет git команду и обрабатывает ошибки.

        Args:
            commands: Список аргументов команды git

        Returns:
            Стандартный вывод команды или None в случае ошибки
        """
        result = subprocess.run(commands, **self.BASE_PARAMS)

        if result.returncode != 0:
            command_text = ' '.join(commands)
            click.secho(f"Ошибка при выполнении '{command_text}':", fg="red")
            click.secho(result.stderr, fg="red")
            return None

        return result.stdout

    def _process_prompt(self, diff_text: str, command: str) -> None:
        """
        Создает промпт на основе diff текста и копирует в буфер.

        Args:
            diff_text: Текст diff для обработки
            command: Описание для логирования
        """
        cleaned_text = utils.clean_git_diff(diff_text)
        utils.log_text_info(cleaned_text, command)
        utils.copy_to_buffer(self.prompt.make(command, cleaned_text))

    def create_diff_prompt(self) -> None:
        """
        Создает промпт на основе git diff и git diff --cached.

        Объединяет изменения в рабочей директории и индексированные изменения
        в единый промпт для коммита.
        """
        diff = self._run_git_command(['git', 'diff'])
        diff_cached = self._run_git_command(['git', 'diff', '--cached'])

        if diff is None or diff_cached is None:
            return

        self._process_prompt(diff + diff_cached, 'git diff + git diff --cached')

    def create_branch_diff_prompt(self, since: str) -> None:
        """
        Создает промпт на основе diff между текущей веткой и указанной точкой.

        Args:
            since: Имя ветки/тега/коммита для сравнения
        """
        param = f'{since}...'
        diff = self._run_git_command(['git', 'diff', param])

        if diff is not None:
            self._process_prompt(diff, f'git diff {param}')

    def create_branch_comments_prompt(self, since: str) -> None:
        """
        Создает промпт на основе истории коммитов между ветками.

        Args:
            since: Имя ветки/тега/коммита для сравнения истории
        """
        current_branch = self._run_git_command(
            ['git', 'symbolic-ref', '--short', 'HEAD']
        )

        if current_branch is None:
            return

        current_branch_name = current_branch.strip()
        commit_range = f"{since}..{current_branch_name}"

        log = self._run_git_command(
            ['git', 'log', commit_range],
        )

        if log is not None:
            self._process_prompt(
                log,
                f'git log {commit_range}'

            )