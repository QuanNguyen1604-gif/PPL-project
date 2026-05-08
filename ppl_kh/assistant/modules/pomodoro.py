from __future__ import annotations

import json
from pathlib import Path

from assistant.config import POMODORO_FILE, RESPONSE_FILE
from assistant.models import Command
from assistant.modules.base import Module


class PomodoroModule(Module):
    def __init__(self, command: Command, *, pomodoro_file: Path = POMODORO_FILE, response_file: Path = RESPONSE_FILE):
        super().__init__(command)
        self.pomodoro_file = pomodoro_file
        self.response_file = response_file

    def respond(self) -> str:
        data = json.loads(self.pomodoro_file.read_text(encoding='utf-8'))
        responses = json.loads(self.response_file.read_text(encoding='utf-8'))
        pomodoro = data['pomodoro']

        if self.command.verb == 'start':
            current_session = pomodoro['session']
            if current_session == 3:
                pomodoro['round'] += 1
            pomodoro['session'] = current_session + 1 if current_session < 4 else 1
            self._save(data)
            return responses['pomodoro']['start'].format(
                duration=pomodoro['duration'],
                session=pomodoro['session'],
                round=pomodoro['round'],
            )

        if self.command.verb == 'reset':
            pomodoro['session'] = 0
            pomodoro['round'] = 0
            self._save(data)
            return responses['pomodoro']['reset']

        if self.command.verb == 'set' and self.command.duration:
            duration = int(self.command.duration)
            if duration < 1 or duration > 60:
                return responses['error_handler']['duration_out_of_bound']
            pomodoro['duration'] = duration
            self._save(data)
            return responses['pomodoro']['set'].format(duration=duration)

        return responses['wrong_input']['missing_object']

    def _save(self, data: dict) -> None:
        self.pomodoro_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
