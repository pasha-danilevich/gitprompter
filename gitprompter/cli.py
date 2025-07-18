import click
from .core import create_diff_prompt, create_branch_diff_prompt, create_branch_commit_message

@click.group()  # Делаем основную группу команд
def cli():
    """Генератор промтов для Git-изменений."""
    pass

@cli.command()
def diff():
    """Промт на основе git diff."""
    create_diff_prompt()


@cli.command()
@click.option("--branch", default="master", help='Просмотр изменений с момента ответвления от указанной ветки')
def branch_diff(branch: str):
    """Промт для всей ветки."""
    create_branch_diff_prompt(branch)

@cli.command()
@click.option("--branch", default="master", help='Просмотр изменений с момента ответвления от указанной ветки')
def branch_comments(branch: str):
    """Промт из всех коммитов ветки."""
    create_branch_commit_message(branch)


if __name__ == "__main__":
    cli()