from __future__ import annotations

from datetime import datetime

from assistant.generated.CfgParser import CfgParser
from assistant.generated.CfgVisitor import CfgVisitor


VALID_OBJECTS = {'calendar', 'meeting', 'event', 'weather', 'pomodoro'}


class ExtractorVisitor(CfgVisitor):
    def __init__(self) -> None:
        self.result: dict[str, str] = {}

    def visitExpression(self, ctx: CfgParser.ExpressionContext):  # noqa: N802
        if ctx.verbs():
            self.result['verbs'] = ctx.verbs().getText()

        if ctx.objects():
            obj = ctx.objects().getText().lower()
            self.result['objects'] = obj if obj in VALID_OBJECTS else 'invalid_input'

        if ctx.time():
            self.visit(ctx.time())

        if ctx.location():
            self.result['location'] = self.visit(ctx.location())

        if ctx.query():
            self.result['query'] = self.visit(ctx.query())

        if ctx.TITLE_STRING():
            title = ctx.TITLE_STRING().getText()
            self.result['title'] = title.replace('"', '').strip()
            # title is used only in the follow-up state; object will be injected by the engine

        return self.result

    def visitTime(self, ctx: CfgParser.TimeContext):  # noqa: N802
        if ctx.start_time():
            self.result['start_time'] = self.visit(ctx.start_time())
        if ctx.end_time():
            self.result['end_time'] = self.visit(ctx.end_time())
        if ctx.today():
            self.result['date'] = datetime.today().strftime('%d/%m/%Y')
        if ctx.date():
            self.result['date'] = ctx.date().getText()
        if ctx.duration():
            self.result['duration'] = self.visit(ctx.duration())
        return self.result

    def visitStart_time(self, ctx: CfgParser.Start_timeContext):  # noqa: N802
        return self._format_time(int(ctx.INT(0).getText()), int(ctx.INT(1).getText()))

    def visitEnd_time(self, ctx: CfgParser.End_timeContext):  # noqa: N802
        return self._format_time(int(ctx.INT(0).getText()), int(ctx.INT(1).getText()))

    def visitLocation(self, ctx: CfgParser.LocationContext):  # noqa: N802
        try:
            parts = [token.getText() for token in ctx.STRING()]
        except TypeError:
            parts = [ctx.getText()]
        return ' '.join(parts).strip().lower()

    def visitQuery(self, ctx: CfgParser.QueryContext):  # noqa: N802
        return ctx.getText().lower()

    def visitDuration(self, ctx: CfgParser.DurationContext):  # noqa: N802
        return ctx.INT().getText()

    @staticmethod
    def _format_time(hour: int, minute: int) -> str:
        if minute >= 60 or hour >= 24:
            return 'invalid_input'
        return f'{hour:02d}:{minute:02d}'
