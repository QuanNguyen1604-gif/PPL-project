# Generated from Cfg.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CfgParser import CfgParser
else:
    from .CfgParser import CfgParser

# This class defines a complete listener for a parse tree produced by CfgParser.
class CfgListener(ParseTreeListener):

    # Enter a parse tree produced by CfgParser#program.
    def enterProgram(self, ctx:CfgParser.ProgramContext):
        pass

    # Exit a parse tree produced by CfgParser#program.
    def exitProgram(self, ctx:CfgParser.ProgramContext):
        pass


    # Enter a parse tree produced by CfgParser#expression.
    def enterExpression(self, ctx:CfgParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CfgParser#expression.
    def exitExpression(self, ctx:CfgParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CfgParser#time.
    def enterTime(self, ctx:CfgParser.TimeContext):
        pass

    # Exit a parse tree produced by CfgParser#time.
    def exitTime(self, ctx:CfgParser.TimeContext):
        pass


    # Enter a parse tree produced by CfgParser#date.
    def enterDate(self, ctx:CfgParser.DateContext):
        pass

    # Exit a parse tree produced by CfgParser#date.
    def exitDate(self, ctx:CfgParser.DateContext):
        pass


    # Enter a parse tree produced by CfgParser#today.
    def enterToday(self, ctx:CfgParser.TodayContext):
        pass

    # Exit a parse tree produced by CfgParser#today.
    def exitToday(self, ctx:CfgParser.TodayContext):
        pass


    # Enter a parse tree produced by CfgParser#query.
    def enterQuery(self, ctx:CfgParser.QueryContext):
        pass

    # Exit a parse tree produced by CfgParser#query.
    def exitQuery(self, ctx:CfgParser.QueryContext):
        pass


    # Enter a parse tree produced by CfgParser#start_time.
    def enterStart_time(self, ctx:CfgParser.Start_timeContext):
        pass

    # Exit a parse tree produced by CfgParser#start_time.
    def exitStart_time(self, ctx:CfgParser.Start_timeContext):
        pass


    # Enter a parse tree produced by CfgParser#end_time.
    def enterEnd_time(self, ctx:CfgParser.End_timeContext):
        pass

    # Exit a parse tree produced by CfgParser#end_time.
    def exitEnd_time(self, ctx:CfgParser.End_timeContext):
        pass


    # Enter a parse tree produced by CfgParser#duration.
    def enterDuration(self, ctx:CfgParser.DurationContext):
        pass

    # Exit a parse tree produced by CfgParser#duration.
    def exitDuration(self, ctx:CfgParser.DurationContext):
        pass


    # Enter a parse tree produced by CfgParser#objects.
    def enterObjects(self, ctx:CfgParser.ObjectsContext):
        pass

    # Exit a parse tree produced by CfgParser#objects.
    def exitObjects(self, ctx:CfgParser.ObjectsContext):
        pass


    # Enter a parse tree produced by CfgParser#verbs.
    def enterVerbs(self, ctx:CfgParser.VerbsContext):
        pass

    # Exit a parse tree produced by CfgParser#verbs.
    def exitVerbs(self, ctx:CfgParser.VerbsContext):
        pass


    # Enter a parse tree produced by CfgParser#location.
    def enterLocation(self, ctx:CfgParser.LocationContext):
        pass

    # Exit a parse tree produced by CfgParser#location.
    def exitLocation(self, ctx:CfgParser.LocationContext):
        pass



del CfgParser