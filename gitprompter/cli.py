import click
from gitprompter import processor, config


@click.group()  # Делаем основную группу команд
def cli():
    """Генератор промтов для Git-изменений."""
    pass

@cli.command()
@click.option(
    "--style", "-s",
    type=click.Choice(["feature", "conventional", "compact"]),
    help="Стиль commit-сообщения"
)
def diff(style: str | None):
    """Промт на основе git diff текущих изменений."""
    if style:
        config.style = style
    processor.create_diff_prompt()


@cli.command()
@click.option(
    "--since",
    default=config.default_branch,
    help="Просмотр изменений с момента ответвления от указанной ветки"
)
@click.option(
    "--style", "-s",
    type=click.Choice(["feature", "conventional", "compact"]),
    help="Стиль commit-сообщения"
)
def branch_comments(since: str, style: str | None):
    """Промт из всех комментариев коммитов ветки."""
    if style:
        config.style = style
    processor.create_branch_comments_prompt(since)


if __name__ == "__main__":
    cli()