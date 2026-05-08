from __future__ import annotations

import json
from pathlib import Path

from assistant.models import Command
from assistant.modules.pomodoro import PomodoroModule
from assistant.response_engine import ResponseEngine


def copy_data_tree(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for file in src.glob('*.json'):
        dst.joinpath(file.name).write_text(file.read_text(encoding='utf-8'), encoding='utf-8')


def make_engine(data_dir: Path) -> ResponseEngine:
    return ResponseEngine(
        response_file=data_dir / 'Data_Response.json',
        temp_file=data_dir / 'Data_temp.json',
        calendar_file=data_dir / 'Data_Calendar.json',
        pomodoro_file=data_dir / 'Data_Pomodoro.json',
        weather_file=data_dir / 'Mock_weather_data.json',
    )


def test_weather_show_contains_city(tmp_path: Path):
    data_dir = tmp_path / 'data'
    project_data = Path(__file__).resolve().parents[1] / 'data'
    copy_data_tree(project_data, data_dir)
    engine = make_engine(data_dir)
    text = engine.get_response('show weather vung tau 16/12/2024')
    assert 'Vung Tau' in text


def test_pomodoro_set_updates_duration(tmp_path: Path):
    data_dir = tmp_path / 'data'
    project_data = Path(__file__).resolve().parents[1] / 'data'
    copy_data_tree(project_data, data_dir)

    cmd = Command(verb='set', object_name='pomodoro', duration='25')
    response = PomodoroModule(cmd, pomodoro_file=data_dir / 'Data_Pomodoro.json', response_file=data_dir / 'Data_Response.json').respond()
    saved = json.loads((data_dir / 'Data_Pomodoro.json').read_text(encoding='utf-8'))
    assert saved['pomodoro']['duration'] == 25
    assert '25 minutes' in response


def test_calendar_add_followup(tmp_path: Path):
    data_dir = tmp_path / 'data'
    project_data = Path(__file__).resolve().parents[1] / 'data'
    copy_data_tree(project_data, data_dir)
    engine = make_engine(data_dir)

    prompt = engine.get_response('set event 13:30 04/01/2025')
    assert 'Please provide the title' in prompt
    final = engine.get_response('"Demo Presentation"')
    assert 'Demo Presentation' in final

    saved = json.loads((data_dir / 'Data_Calendar.json').read_text(encoding='utf-8'))
    day = next(item for item in saved['schedule'] if item['date'] == '04/01/2025')
    assert any(activity['description'] == 'Demo Presentation' for activity in day['activities'])
