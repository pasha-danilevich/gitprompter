import click
from gitprompter import build_processor


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
@click.option(
    "--analysis", "-a",
    default=False,
    is_flag=True,
    help="Сказать LLM, чтобы проанализировала код и подсветила ошибки"
)
def diff(style: str | None, analysis: bool) -> None:
    """Промт на основе git diff текущих изменений."""
    processor = build_processor(style, analysis)
    processor.create_diff_prompt()


@cli.command()
@click.option(
    "--since",
    default="main",
    help="Просмотр изменений с момента ответвления от указанной ветки"
)
@click.option(
    "--style", "-s",
    type=click.Choice(["feature", "conventional", "compact"]),
    help="Стиль commit-сообщения"
)
def branch_comments(since: str, style: str | None):
    """Промт из всех комментариев коммитов ветки."""
    processor = build_processor(style, False)
    processor.create_branch_comments_prompt(since)


if __name__ == "__main__":
    cli()