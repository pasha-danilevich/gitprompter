import subprocess
import sys

from loguru import logger

from gitprompter import utils

BASE_PARAMS = {
    'capture_output': True,
    'text': True,
    'encoding': 'utf-8',
    'errors': 'replace',  # Обработка проблем с кодировкой
    'shell': sys.platform == 'win32',  # Используем shell=True только на Windows
}

COMMIT_PROMPT = (
    "Задача:\n"
    "Напиши комментарий к моему commit используя следующую структуру:\n"
    "{краткое название commit`а, описывающее всю суть}\n"
    "{символ каретки для отступа (enter)}\n"
    "{пункты изменений (начинаются с дефиса)}\n"
    "СВОЙ ОТВЕТ НАПИШИ В code формате на русском языке\n\n"
)

BRANCH_COMMIT_MESSAGE_PROMPT = (
    "Задача:\n"
    "Напиши комментарий к моему Pull Request используя следующую структуру:\n"
    "{краткое название Pull Request, описывающее всю суть}\n"
    "{символ каретки для отступа (enter)}\n"
    "{пункты изменений (начинаются с дефиса)}\n"
    "СВОЙ ОТВЕТ НАПИШИ В code формате на русском языке\n"
    "Комментарии всех фиксаций в текущей ветке:\n\n"
)


def create_diff_prompt():
    # Получаем вывод git diff (универсальный способ для всех ОС)
    diff = subprocess.run(['git', 'diff'], **BASE_PARAMS)
    diff_cached = subprocess.run(['git', 'diff', '--cached'], **BASE_PARAMS)
    
    if diff.returncode != 0 or diff_cached.returncode != 0:
        logger.error("Ошибка при выполнении git diff или git diff --cached:")
        logger.error(diff.stderr)
        return
    
    diff_text = utils.clean_git_diff(diff.stdout)
    diff_cached_text = utils.clean_git_diff(diff_cached.stdout)
    
    utils.log_text_info(diff_text, 'git diff')
    utils.log_text_info(diff_cached_text, 'git diff --cached')
    
    full_text = (
            COMMIT_PROMPT + f'git diff --cached: {diff_cached_text}' + f'git diff: {diff_text}'
    )
    utils.copy_to_buffer(full_text)

BRANCH_PROMPT = (
    "Задача:\n"
)

def create_branch_diff_prompt(branch: str):
    param = f'{branch}...'
    diff = subprocess.run(['git', 'diff', param], **BASE_PARAMS)
    if diff.returncode != 0 :
        logger.debug(f'Пытаюсь выполнить git log {param}')
        logger.error(diff.stderr)
        return
    diff_text = diff.stdout
    
    utils.log_text_info(diff_text, f'git diff {param}')
    
    full_text = COMMIT_PROMPT + f'git diff {param}: {diff_text}'
    utils.copy_to_buffer(full_text)
    

def create_branch_commit_message(branch: str):
    current_branch = subprocess.run(['git', 'symbolic-ref', '--short', 'HEAD'], **BASE_PARAMS)
    current_branch_name = current_branch.stdout.strip()
    commit_range = f"{branch}..{current_branch_name}"
    result = subprocess.run(['git', 'log', commit_range], **BASE_PARAMS)
    if result.returncode != 0 :
        logger.debug(f'Пытаюсь выполнить git log {commit_range}')
        logger.error(result.stderr)
        return
    
    utils.log_text_info(result.stdout, f'git log {commit_range}')
    
    full_text = BRANCH_COMMIT_MESSAGE_PROMPT + f'git log {commit_range}: {result.stdout}'
    utils.copy_to_buffer(full_text)
