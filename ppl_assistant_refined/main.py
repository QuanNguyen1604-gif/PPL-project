from __future__ import annotations

import argparse

from assistant.response_engine import ResponseEngine
from assistant.ui import ChatApplicationUI
from assistant.web_ui import app


def run_chat() -> None:
    engine = ResponseEngine()
    print('PPL Assistant chat mode. Type quit to stop.')
    while True:
        try:
            text = input('> ').strip()
        except EOFError:
            print()
            break
        if not text:
            continue
        if text.lower() in {'quit', 'exit'}:
            break
        print(engine.get_response(text))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='PPL assistant based on CFG + ANTLR.')
    parser.add_argument('--chat', action='store_true', help='Run interactive CLI chat mode.')
    parser.add_argument('--gui', action='store_true', help='Run the Tkinter GUI.')
    parser.add_argument('--web', action='store_true', help='Run the web-based GUI.')
    parser.add_argument('--command', type=str, help='Run a single command and print the response.')
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.gui:
        ChatApplicationUI().run()
        return
    if args.web:
        app.run(debug=True)
        return
    if args.command:
        engine = ResponseEngine()
        print(engine.get_response(args.command))
        return
    run_chat() if args.chat or not (args.chat or args.gui or args.web or args.command) else None


if __name__ == '__main__':
    main()
