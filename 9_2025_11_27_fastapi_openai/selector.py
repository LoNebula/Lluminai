from enum import Enum

class TaskType(str, Enum):
    CHAT = "chat"
    SUMMARIZE = "summarize"
    CLASSIFY = "classify"
    REASONING = "reasoning"

class ModelSelector:
    def choose(self, task: TaskType):
        if task == TaskType.CLASSIFY:
            return "gpt-4o-mini"

        if task == TaskType.SUMMARIZE:
            return "gpt-4o-mini"

        if task == TaskType.CHAT:
            return "gpt-4o"

        if task == TaskType.REASONING:
            return "o1"

        return "gpt-4o"

