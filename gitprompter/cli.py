import click
from .core import create_diff_prompt, create_branch_diff_prompt

@click.group()  # Делаем основную группу команд
def cli():
    """Генератор промтов для Git-изменений."""
    pass

@cli.command()
def diff():
    """Генерирует промт для нейросети на основе git diff."""
    create_diff_prompt()


@cli.command()
@click.option("--branch", default="master", help='Просмотр изменений с момента ответвления от указанной ветки')
def branch_diff(branch: str):
    """Генерирует промт для нейросети на основе git diff для всей ветки начиная от --branch (master по умолчанию)."""
    create_branch_diff_prompt(branch)




if __name__ == "__main__":
    cli()