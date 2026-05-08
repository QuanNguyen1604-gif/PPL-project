from __future__ import annotations

from dataclasses import dataclass

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from assistant.generated.CfgLexer import CfgLexer
from assistant.generated.CfgParser import CfgParser
from assistant.extractor_visitor import ExtractorVisitor
from assistant.preprocessing import preprocess_text


class SyntaxErrorListener(ErrorListener):
    def __init__(self) -> None:
        super().__init__()
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):  # noqa: N802
        self.errors.append(f"line {line}:{column} {msg}")


@dataclass
class ParseResult:
    data: dict
    syntax_errors: list[str]
    normalized_text: str


class CommandParser:
    def parse(self, text: str, *, preprocess: bool = True) -> ParseResult:
        normalized = preprocess_text(text) if preprocess else text.strip()
        input_stream = InputStream(normalized)
        lexer = CfgLexer(input_stream)
        parser = CfgParser(CommonTokenStream(lexer))

        error_listener = SyntaxErrorListener()
        lexer.removeErrorListeners()
        parser.removeErrorListeners()
        lexer.addErrorListener(error_listener)
        parser.addErrorListener(error_listener)

        tree = parser.program()
        if error_listener.errors:
            return ParseResult(data={}, syntax_errors=error_listener.errors, normalized_text=normalized)

        visitor = ExtractorVisitor()
        visitor.visit(tree)
        return ParseResult(data=visitor.result or {}, syntax_errors=[], normalized_text=normalized)
