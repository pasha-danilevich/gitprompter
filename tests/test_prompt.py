from gitprompter import GitPrompterConfig
from gitprompter.prompts import Prompt


def test():
    prompt = Prompt(GitPrompterConfig())
    command = 'test'
    result = 'test_result'
    print(prompt.make(command, result))