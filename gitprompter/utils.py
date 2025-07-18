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
    
def log_diff_text_info(text: str, request: str):
    msg = f'Длина запроса "{request}": {len(text)} символов'
    
    if len(text) == 0:
        logger.warning(msg)
    else:
        logger.info(msg)
    