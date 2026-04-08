# GitPrompter

**GitPrompter** — это CLI-инструмент, который превращает `git diff` и историю коммитов в готовые промпты для генерации commit-сообщений через LLM.

Он помогает автоматизировать написание осмысленных commit message в заданном стиле (например, *Conventional Commits*).

---

## 🚀 Возможности

* Генерация промпта из:

  * текущих изменений (`git diff`)
  * staged изменений (`git diff --cached`)
  * истории коммитов ветки (`git log`)
* Поддержка разных стилей:

  * `conventional` (по умолчанию)
  * `feature`
  * `compact`
* Автозагрузка конфигурации из `pyproject.toml`
* Копирование результата:

  * в буфер обмена
  * или в файл `prompt.txt`

---

## 📦 Установка

```bash
pip install gitprompter
```

или локально:

```bash
pip install -e .
```

---

## ⚙️ Конфигурация

Настройки задаются в `pyproject.toml`:

```toml
[tool.gitprompter]
style = "conventional"
to_file = false
language = "ru"
default_branch = "main"
```

### Параметры

| Параметр         | Описание                                                      |
| ---------------- |---------------------------------------------------------------|
| `style`          | Стиль commit-сообщения (`conventional`, `feature`, `compact`) |
| `to_file`        | Сохранять в файл вместо буфера                                |
| `language`       | Язык ответа LLM                                               |
| `default_branch` | Базовая ветка для сравнения                                   |

---

## 🧠 Как это работает

1. Инструмент получает изменения из Git
2. Очищает diff (убирает служебную информацию)
3. Формирует промпт
4. Копирует его в буфер или сохраняет в файл

---

## 🖥 CLI Использование

### 1. Генерация промпта из текущих изменений

```bash
gitprompter diff
```

Что делает:

* берет `git diff`
* берет `git diff --cached`
* объединяет
* генерирует промпт

---
### 1.1 Выбор стиля ответа

```bash
gitprompter diff -s compact
```

Возможные стили:

* feature 
* conventional
* compact

Как выглядят эти стили, вы можете посмотреть в gitprompter/prompts.py

---

### 2. Генерация промпта из истории ветки

```bash
gitprompter branch-comments
```

или:

```bash
gitprompter branch-comments --since develop
```

Что делает:

* сравнивает текущую ветку с указанной (`since`)
* берет `git log`
* генерирует промпт

⚠️ Не отталкивается от `git diff`, в промт попадают только commit massege всей ветки

---

## 📝 Пример результата

```text
Task:
Write a comment following this structure:

<type>[optional scope]: <short summary>

[optional detailed description]

[optional footer(s)]

...

Please write your ANSWER in either "code" or "plaintext" format, using the "ru" language.

Result of the "git diff + git diff --cached" command:
+ added new feature
- removed old logic
```

---

## 🧩 Архитектура

### Основные компоненты

* **GitDiffProcessor**

  * Работа с git
  * Обработка diff/log
  * Генерация финального промпта

* **Prompt**

  * Формирует текст запроса для LLM
  * Поддерживает разные стили

* **GitPrompterConfig**

  * Загружает конфигурацию из `pyproject.toml`

* **utils**

  * Очистка diff
  * Логирование
  * Копирование / запись

---

## 🔧 Программное использование

```python
from gitprompter import processor

processor.create_diff_prompt()
```

или:

```python
processor.create_branch_comments_prompt("develop")
```

---

## ⚠️ Особенности

* Работает только внутри git-репозитория
* Использует системный `git`
* На Windows команды выполняются через `shell=True`
* Требует установленный `pyperclip` для буфера обмена (подтянется автоматически)

---

## 💡 Когда это реально полезно

* Когда ты ленишься писать commit message (и правильно делаешь 😄, лучше пусть рутину делает нейро-сеть, чем писать commit в стиле: "fix", "add some", "qwerty")
* Когда нужен единый стиль коммитов в команде
* Когда используешь AI в workflow разработки
