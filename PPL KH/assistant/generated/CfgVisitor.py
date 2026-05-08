# Generated from Cfg.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CfgParser import CfgParser
else:
    from .CfgParser import CfgParser

# This class defines a complete generic visitor for a parse tree produced by CfgParser.

class CfgVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CfgParser#program.
    def visitProgram(self, ctx:CfgParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#expression.
    def visitExpression(self, ctx:CfgParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#time.
    def visitTime(self, ctx:CfgParser.TimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#date.
    def visitDate(self, ctx:CfgParser.DateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#today.
    def visitToday(self, ctx:CfgParser.TodayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#query.
    def visitQuery(self, ctx:CfgParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#start_time.
    def visitStart_time(self, ctx:CfgParser.Start_timeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#end_time.
    def visitEnd_time(self, ctx:CfgParser.End_timeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#duration.
    def visitDuration(self, ctx:CfgParser.DurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#objects.
    def visitObjects(self, ctx:CfgParser.ObjectsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#verbs.
    def visitVerbs(self, ctx:CfgParser.VerbsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CfgParser#location.
    def visitLocation(self, ctx:CfgParser.LocationContext):
        return self.visitChildren(ctx)



del CfgParser