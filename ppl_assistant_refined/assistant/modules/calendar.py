from __future__ import annotations

import json
from pathlib import Path

from assistant.config import CALENDAR_FILE, RESPONSE_FILE
from assistant.models import Command
from assistant.modules.base import Module


class CalendarModule(Module):
    def __init__(self, command: Command, *, calendar_file: Path = CALENDAR_FILE, response_file: Path = RESPONSE_FILE):
        super().__init__(command)
        self.calendar_file = calendar_file
        self.response_file = response_file

    def respond(self) -> str:
        responses = json.loads(self.response_file.read_text(encoding='utf-8'))

        if self.command.location:
            return responses['wrong_input']['missing_object']

        if self.command.object_name == 'calendar':
            return self._show_all_on_date(responses)

        if self.command.object_name in {'meeting', 'event'}:
            if self.command.verb == 'show':
                return self._show_by_type(responses)
            if self.command.verb == 'set':
                return self._validate_before_add(responses)

        return responses['wrong_input']['missing_object']

    def add_activity(self, pending: dict, title: str) -> str:
        data = json.loads(self.calendar_file.read_text(encoding='utf-8'))
        for day in data['schedule']:
            if day['date'] == pending['date']:
                day['activities'].append(
                    {
                        'type': pending['objects'],
                        'description': title,
                        'start_time': pending['start_time'],
                        'end_time': pending.get('end_time'),
                    }
                )
                break
        else:
            data['schedule'].append(
                {
                    'date': pending['date'],
                    'activities': [
                        {
                            'type': pending['objects'],
                            'description': title,
                            'start_time': pending['start_time'],
                            'end_time': pending.get('end_time'),
                        }
                    ],
                }
            )

        self.calendar_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        responses = json.loads(self.response_file.read_text(encoding='utf-8'))
        return responses['calendar']['finish_set'].format(objects=pending['objects'], title=title, date=pending['date'])

    def _show_all_on_date(self, responses: dict) -> str:
        if self.command.verb != 'show':
            return responses['wrong_input']['missing_object']
        if not self.command.date:
            return responses['wrong_input']['missing_date']
        activities = self._activities_for_date(self.command.date)
        if activities is None:
            return responses['calendar']['date_out_of_bound']
        if not activities:
            return responses['calendar']['no_activity'].format(objects='activity', date=self.command.date)
        return '\n'.join(self._format_activity(activity) for activity in activities)

    def _show_by_type(self, responses: dict) -> str:
        if not self.command.date:
            return responses['wrong_input']['missing_date']
        activities = self._activities_for_date(self.command.date)
        if activities is None:
            return responses['calendar']['date_out_of_bound']
        filtered = [a for a in activities if a['type'] == self.command.object_name]
        if not filtered:
            return responses['calendar']['no_activity'].format(objects=self.command.object_name, date=self.command.date)
        return '\n'.join(self._format_activity(activity) for activity in filtered)

    def _validate_before_add(self, responses: dict) -> str:
        if not self.command.date:
            return responses['wrong_input']['missing_date']
        if not self.command.start_time:
            return responses['wrong_input']['wrong_time']
        if self.command.object_name == 'meeting' and not self.command.end_time:
            return responses['wrong_input']['wrong_time']
        if 'invalid_input' in {self.command.start_time, self.command.end_time}:
            return responses['wrong_input']['wrong_time']
        if self.command.end_time and self.command.start_time > self.command.end_time:
            return responses['wrong_input']['wrong_time']
        return responses['calendar']['add_title']

    def _activities_for_date(self, date: str):
        data = json.loads(self.calendar_file.read_text(encoding='utf-8'))
        for day in data['schedule']:
            if day['date'] == date:
                return day['activities']
        return None

    @staticmethod
    def _format_activity(activity: dict) -> str:
        end_time = activity.get('end_time') or 'N/A'
        return f"You have {activity['type']}: \"{activity['description']}\", start at {activity.get('start_time', 'N/A')} and end at {end_time}."
