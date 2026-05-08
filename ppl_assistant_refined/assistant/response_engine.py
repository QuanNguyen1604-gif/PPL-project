from __future__ import annotations

import json
from pathlib import Path

from assistant.config import CALENDAR_FILE, POMODORO_FILE, RESPONSE_FILE, TEMP_FILE, WEATHER_FILE
from assistant.models import Command
from assistant.modules.calendar import CalendarModule
from assistant.modules.pomodoro import PomodoroModule
from assistant.modules.weather import WeatherModule
from assistant.parser_service import CommandParser


class ResponseEngine:
    def __init__(
        self,
        *,
        response_file: Path = RESPONSE_FILE,
        temp_file: Path = TEMP_FILE,
        calendar_file: Path = CALENDAR_FILE,
        pomodoro_file: Path = POMODORO_FILE,
        weather_file: Path = WEATHER_FILE,
    ):
        self.parser = CommandParser()
        self.response_file = response_file
        self.temp_file = temp_file
        self.calendar_file = calendar_file
        self.pomodoro_file = pomodoro_file
        self.weather_file = weather_file
        self.awaiting_title = False
        self.pending_calendar_command: dict | None = None
        self.responses = json.loads(self.response_file.read_text(encoding='utf-8'))

    def parse_only(self, text: str) -> Command:
        result = self.parser.parse(text, preprocess=not self.awaiting_title)
        command = Command.from_dict(result.data, raw=text)
        command.errors.extend(result.syntax_errors)
        return command

    def get_response(self, text: str) -> str:
        parse_result = self.parser.parse(text, preprocess=not self.awaiting_title)
        if parse_result.syntax_errors:
            self.awaiting_title = False
            self.pending_calendar_command = None
            return self.responses['wrong_input']['missing_object']

        command = Command.from_dict(parse_result.data, raw=text)
        if self.awaiting_title:
            return self._handle_title_followup(command)
        return self._dispatch(command)

    def _dispatch(self, command: Command) -> str:
        if command.object_name in {'meeting', 'event', 'calendar'}:
            module = CalendarModule(command, calendar_file=self.calendar_file, response_file=self.response_file)
            message = module.respond()
            if command.verb == 'set' and command.object_name in {'meeting', 'event'} and message == self.responses['calendar']['add_title']:
                self.awaiting_title = True
                self.pending_calendar_command = command.to_dict()
                self.temp_file.write_text(json.dumps(self.pending_calendar_command, indent=2, ensure_ascii=False), encoding='utf-8')
            return message

        if command.object_name == 'weather':
            return WeatherModule(command, weather_file=self.weather_file, response_file=self.response_file).respond()

        if command.object_name == 'pomodoro':
            return PomodoroModule(command, pomodoro_file=self.pomodoro_file, response_file=self.response_file).respond()

        return self.responses['wrong_input']['missing_object']

    def _handle_title_followup(self, command: Command) -> str:
        if command.title and self.pending_calendar_command:
            module = CalendarModule(Command(), calendar_file=self.calendar_file, response_file=self.response_file)
            message = module.add_activity(self.pending_calendar_command, command.title)
            self.awaiting_title = False
            self.pending_calendar_command = None
            return message

        self.awaiting_title = False
        self.pending_calendar_command = None
        return self.responses['wrong_input']['retry_process']
