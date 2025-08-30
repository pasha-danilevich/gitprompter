import click
from gitprompter import processor

@click.group()  # Делаем основную группу команд
def cli():
    """Генератор промтов для Git-изменений."""
    pass

@cli.command()
def diff():
    """Промт на основе git diff текущих изменений."""
    processor.create_diff_prompt()


@cli.command()
@click.option("--since", default="master", help='Просмотр изменений с момента ответвления от указанной ветки')
def branch_diff(since: str):
    """Промт на основе git diff всей ветки."""
    processor.create_branch_diff_prompt(since)

@cli.command()
@click.option("--since", default="master", help='Просмотр изменений с момента ответвления от указанной ветки')
def branch_comments(since: str):
    """Промт из всех комментариев коммитов ветки."""
    processor.create_branch_comments_prompt(since)


if __name__ == "__main__":
    cli()