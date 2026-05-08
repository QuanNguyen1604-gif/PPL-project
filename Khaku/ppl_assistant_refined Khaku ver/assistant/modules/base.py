from __future__ import annotations

from assistant.models import Command


class Module:
    def __init__(self, command: Command):
        self.command = command

    def respond(self) -> str:
        raise NotImplementedError
