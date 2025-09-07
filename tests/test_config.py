from gitprompter.config import GitPrompterConfig


def test():
    config = GitPrompterConfig()
    print(config.load_config())
