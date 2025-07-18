from pathlib import Path

import pyperclip
from loguru import logger


def copy_to_buffer(text: str):
    # Копируем текст в буфер обмена
    try:
        pyperclip.copy(text)
        logger.success(f"Промт успешно скопирован в буфер обмена!")
    except Exception as e:
        logger.error(f"Не удалось скопировать текст в буфер обмена: {e}")
        
def write_to_txt(text: str):
    # Создаем путь к файлу (кросс-платформенный способ)
    output_path = Path(__file__).resolve().parent / 'output'
    path = Path(output_path, "prompt.txt")
    # Записываем вывод в файл с явным указанием кодировки
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

    logger.success(f"Вывод git diff сохранён в {path}")
    
def log_text_info(text: str, request: str):
    line_count = len(text.splitlines())  # Подсчет количества строк
    msg = f'Длина запроса "{request}": {len(text)} символов ({line_count} строк)' # посчитай кол-во строк
    
    if len(text) == 0:
        logger.warning(msg)
    else:
        logger.info(msg)

def clean_git_diff(diff_text: str) -> str:
    """
    Очищает вывод git diff, оставляя только значимые изменения (+ и - строки),
    игнорируя служебные заголовки и метаданные.
    """
    clean_lines = []
    for line in diff_text.splitlines():
        # Оставляем изменения в содержании: удалённые и добавленные строки.
        if line.startswith('+'):
            clean_lines.append(line)
        elif line.startswith('-'):
            clean_lines.append(line)
        # также включать контекст:
        elif line.startswith('@'):
            clean_lines.append(line)
        elif line.startswith(' '):
            clean_lines.append(line)
        # Всё остальное (служебная инфа) пропускаем.
    return '\n'.join(clean_lines)
