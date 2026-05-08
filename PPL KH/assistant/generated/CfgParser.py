# Generated from Cfg.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\26")
        buf.write("_\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2\3\2")
        buf.write("\3\2\3\3\3\3\3\3\5\3!\n\3\3\3\5\3$\n\3\3\3\5\3\'\n\3\3")
        buf.write("\3\3\3\3\3\5\3,\n\3\3\3\3\3\5\3\60\n\3\3\3\5\3\63\n\3")
        buf.write("\3\4\3\4\5\4\67\n\4\3\4\3\4\5\4;\n\4\3\4\3\4\3\4\5\4@")
        buf.write("\n\4\3\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3")
        buf.write("\b\3\b\3\t\3\t\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\r\6")
        buf.write("\r[\n\r\r\r\16\r\\\3\r\2\2\16\2\4\6\b\n\f\16\20\22\24")
        buf.write("\26\30\2\4\3\2\5\13\3\2\r\22\2_\2\32\3\2\2\2\4\62\3\2")
        buf.write("\2\2\6?\3\2\2\2\bA\3\2\2\2\nG\3\2\2\2\fI\3\2\2\2\16K\3")
        buf.write("\2\2\2\20O\3\2\2\2\22S\3\2\2\2\24U\3\2\2\2\26W\3\2\2\2")
        buf.write("\30Z\3\2\2\2\32\33\5\4\3\2\33\34\7\2\2\3\34\3\3\2\2\2")
        buf.write("\35\36\5\26\f\2\36 \5\24\13\2\37!\5\30\r\2 \37\3\2\2\2")
        buf.write(" !\3\2\2\2!#\3\2\2\2\"$\5\6\4\2#\"\3\2\2\2#$\3\2\2\2$")
        buf.write("&\3\2\2\2%\'\5\f\7\2&%\3\2\2\2&\'\3\2\2\2\'\63\3\2\2\2")
        buf.write("()\5\26\f\2)+\5\24\13\2*,\5\30\r\2+*\3\2\2\2+,\3\2\2\2")
        buf.write(",-\3\2\2\2-/\5\f\7\2.\60\5\6\4\2/.\3\2\2\2/\60\3\2\2\2")
        buf.write("\60\63\3\2\2\2\61\63\7\23\2\2\62\35\3\2\2\2\62(\3\2\2")
        buf.write("\2\62\61\3\2\2\2\63\5\3\2\2\2\64\66\5\16\b\2\65\67\5\20")
        buf.write("\t\2\66\65\3\2\2\2\66\67\3\2\2\2\67:\3\2\2\28;\5\n\6\2")
        buf.write("9;\5\b\5\2:8\3\2\2\2:9\3\2\2\2;@\3\2\2\2<@\5\n\6\2=@\5")
        buf.write("\b\5\2>@\5\22\n\2?\64\3\2\2\2?<\3\2\2\2?=\3\2\2\2?>\3")
        buf.write("\2\2\2@\7\3\2\2\2AB\7\25\2\2BC\7\3\2\2CD\7\25\2\2DE\7")
        buf.write("\3\2\2EF\7\25\2\2F\t\3\2\2\2GH\7\4\2\2H\13\3\2\2\2IJ\t")
        buf.write("\2\2\2J\r\3\2\2\2KL\7\25\2\2LM\7\f\2\2MN\7\25\2\2N\17")
        buf.write("\3\2\2\2OP\7\25\2\2PQ\7\f\2\2QR\7\25\2\2R\21\3\2\2\2S")
        buf.write("T\7\25\2\2T\23\3\2\2\2UV\7\24\2\2V\25\3\2\2\2WX\t\3\2")
        buf.write("\2X\27\3\2\2\2Y[\7\24\2\2ZY\3\2\2\2[\\\3\2\2\2\\Z\3\2")
        buf.write("\2\2\\]\3\2\2\2]\31\3\2\2\2\f #&+/\62\66:?\\")
        return buf.getvalue()


class CfgParser ( Parser ):

    grammarFileName = "Cfg.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'/'", "'today'", "'sunny'", "'cloudy'", 
                     "'rainy'", "'windy'", "'snowy'", "'clear'", "'foggy'", 
                     "':'", "'set'", "'show'", "'check'", "'tell'", "'start'", 
                     "'reset'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "TITLE_STRING", "STRING", "INT", "WS" ]

    RULE_program = 0
    RULE_expression = 1
    RULE_time = 2
    RULE_date = 3
    RULE_today = 4
    RULE_query = 5
    RULE_start_time = 6
    RULE_end_time = 7
    RULE_duration = 8
    RULE_objects = 9
    RULE_verbs = 10
    RULE_location = 11

    ruleNames =  [ "program", "expression", "time", "date", "today", "query", 
                   "start_time", "end_time", "duration", "objects", "verbs", 
                   "location" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    TITLE_STRING=17
    STRING=18
    INT=19
    WS=20

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self):
            return self.getTypedRuleContext(CfgParser.ExpressionContext,0)


        def EOF(self):
            return self.getToken(CfgParser.EOF, 0)

        def getRuleIndex(self):
            return CfgParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = CfgParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            self.expression()
            self.state = 25
            self.match(CfgParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def verbs(self):
            return self.getTypedRuleContext(CfgParser.VerbsContext,0)


        def objects(self):
            return self.getTypedRuleContext(CfgParser.ObjectsContext,0)


        def location(self):
            return self.getTypedRuleContext(CfgParser.LocationContext,0)


        def time(self):
            return self.getTypedRuleContext(CfgParser.TimeContext,0)


        def query(self):
            return self.getTypedRuleContext(CfgParser.QueryContext,0)


        def TITLE_STRING(self):
            return self.getToken(CfgParser.TITLE_STRING, 0)

        def getRuleIndex(self):
            return CfgParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = CfgParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expression)
        self._la = 0 # Token type
        try:
            self.state = 48
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 27
                self.verbs()
                self.state = 28
                self.objects()
                self.state = 30
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CfgParser.STRING:
                    self.state = 29
                    self.location()


                self.state = 33
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CfgParser.T__1 or _la==CfgParser.INT:
                    self.state = 32
                    self.time()


                self.state = 36
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CfgParser.T__2) | (1 << CfgParser.T__3) | (1 << CfgParser.T__4) | (1 << CfgParser.T__5) | (1 << CfgParser.T__6) | (1 << CfgParser.T__7) | (1 << CfgParser.T__8))) != 0):
                    self.state = 35
                    self.query()


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 38
                self.verbs()
                self.state = 39
                self.objects()
                self.state = 41
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CfgParser.STRING:
                    self.state = 40
                    self.location()


                self.state = 43
                self.query()
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CfgParser.T__1 or _la==CfgParser.INT:
                    self.state = 44
                    self.time()


                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 47
                self.match(CfgParser.TITLE_STRING)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def start_time(self):
            return self.getTypedRuleContext(CfgParser.Start_timeContext,0)


        def today(self):
            return self.getTypedRuleContext(CfgParser.TodayContext,0)


        def date(self):
            return self.getTypedRuleContext(CfgParser.DateContext,0)


        def end_time(self):
            return self.getTypedRuleContext(CfgParser.End_timeContext,0)


        def duration(self):
            return self.getTypedRuleContext(CfgParser.DurationContext,0)


        def getRuleIndex(self):
            return CfgParser.RULE_time

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTime" ):
                listener.enterTime(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTime" ):
                listener.exitTime(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTime" ):
                return visitor.visitTime(self)
            else:
                return visitor.visitChildren(self)




    def time(self):

        localctx = CfgParser.TimeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_time)
        try:
            self.state = 61
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 50
                self.start_time()
                self.state = 52
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
                if la_ == 1:
                    self.state = 51
                    self.end_time()


                self.state = 56
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [CfgParser.T__1]:
                    self.state = 54
                    self.today()
                    pass
                elif token in [CfgParser.INT]:
                    self.state = 55
                    self.date()
                    pass
                else:
                    raise NoViableAltException(self)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 58
                self.today()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 59
                self.date()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 60
                self.duration()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(CfgParser.INT)
            else:
                return self.getToken(CfgParser.INT, i)

        def getRuleIndex(self):
            return CfgParser.RULE_date

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDate" ):
                listener.enterDate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDate" ):
                listener.exitDate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDate" ):
                return visitor.visitDate(self)
            else:
                return visitor.visitChildren(self)




    def date(self):

        localctx = CfgParser.DateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_date)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(CfgParser.INT)
            self.state = 64
            self.match(CfgParser.T__0)
            self.state = 65
            self.match(CfgParser.INT)
            self.state = 66
            self.match(CfgParser.T__0)
            self.state = 67
            self.match(CfgParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TodayContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CfgParser.RULE_today

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterToday" ):
                listener.enterToday(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitToday" ):
                listener.exitToday(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitToday" ):
                return visitor.visitToday(self)
            else:
                return visitor.visitChildren(self)




    def today(self):

        localctx = CfgParser.TodayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_today)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(CfgParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QueryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CfgParser.RULE_query

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery" ):
                listener.enterQuery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery" ):
                listener.exitQuery(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuery" ):
                return visitor.visitQuery(self)
            else:
                return visitor.visitChildren(self)




    def query(self):

        localctx = CfgParser.QueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_query)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CfgParser.T__2) | (1 << CfgParser.T__3) | (1 << CfgParser.T__4) | (1 << CfgParser.T__5) | (1 << CfgParser.T__6) | (1 << CfgParser.T__7) | (1 << CfgParser.T__8))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Start_timeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(CfgParser.INT)
            else:
                return self.getToken(CfgParser.INT, i)

        def getRuleIndex(self):
            return CfgParser.RULE_start_time

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart_time" ):
                listener.enterStart_time(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart_time" ):
                listener.exitStart_time(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart_time" ):
                return visitor.visitStart_time(self)
            else:
                return visitor.visitChildren(self)




    def start_time(self):

        localctx = CfgParser.Start_timeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_start_time)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(CfgParser.INT)
            self.state = 74
            self.match(CfgParser.T__9)
            self.state = 75
            self.match(CfgParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class End_timeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(CfgParser.INT)
            else:
                return self.getToken(CfgParser.INT, i)

        def getRuleIndex(self):
            return CfgParser.RULE_end_time

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnd_time" ):
                listener.enterEnd_time(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnd_time" ):
                listener.exitEnd_time(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEnd_time" ):
                return visitor.visitEnd_time(self)
            else:
                return visitor.visitChildren(self)




    def end_time(self):

        localctx = CfgParser.End_timeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_end_time)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(CfgParser.INT)
            self.state = 78
            self.match(CfgParser.T__9)
            self.state = 79
            self.match(CfgParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DurationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(CfgParser.INT, 0)

        def getRuleIndex(self):
            return CfgParser.RULE_duration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDuration" ):
                listener.enterDuration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDuration" ):
                listener.exitDuration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDuration" ):
                return visitor.visitDuration(self)
            else:
                return visitor.visitChildren(self)




    def duration(self):

        localctx = CfgParser.DurationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_duration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(CfgParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjectsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(CfgParser.STRING, 0)

        def getRuleIndex(self):
            return CfgParser.RULE_objects

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObjects" ):
                listener.enterObjects(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObjects" ):
                listener.exitObjects(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObjects" ):
                return visitor.visitObjects(self)
            else:
                return visitor.visitChildren(self)




    def objects(self):

        localctx = CfgParser.ObjectsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_objects)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self.match(CfgParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VerbsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CfgParser.RULE_verbs

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVerbs" ):
                listener.enterVerbs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVerbs" ):
                listener.exitVerbs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVerbs" ):
                return visitor.visitVerbs(self)
            else:
                return visitor.visitChildren(self)




    def verbs(self):

        localctx = CfgParser.VerbsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_verbs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << CfgParser.T__10) | (1 << CfgParser.T__11) | (1 << CfgParser.T__12) | (1 << CfgParser.T__13) | (1 << CfgParser.T__14) | (1 << CfgParser.T__15))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LocationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self, i:int=None):
            if i is None:
                return self.getTokens(CfgParser.STRING)
            else:
                return self.getToken(CfgParser.STRING, i)

        def getRuleIndex(self):
            return CfgParser.RULE_location

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLocation" ):
                listener.enterLocation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLocation" ):
                listener.exitLocation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLocation" ):
                return visitor.visitLocation(self)
            else:
                return visitor.visitChildren(self)




    def location(self):

        localctx = CfgParser.LocationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_location)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 87
                self.match(CfgParser.STRING)
                self.state = 90 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==CfgParser.STRING):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





