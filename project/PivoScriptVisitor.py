# Generated from PivoScript.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .PivoScriptParser import PivoScriptParser
else:
    from PivoScriptParser import PivoScriptParser

# This class defines a complete generic visitor for a parse tree produced by PivoScriptParser.

class PivoScriptVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PivoScriptParser#program.
    def visitProgram(self, ctx:PivoScriptParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#statement.
    def visitStatement(self, ctx:PivoScriptParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#varDecl.
    def visitVarDecl(self, ctx:PivoScriptParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#output.
    def visitOutput(self, ctx:PivoScriptParser.OutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#addSubExpr.
    def visitAddSubExpr(self, ctx:PivoScriptParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#mulDivExpr.
    def visitMulDivExpr(self, ctx:PivoScriptParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#negExpr.
    def visitNegExpr(self, ctx:PivoScriptParser.NegExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#intExpr.
    def visitIntExpr(self, ctx:PivoScriptParser.IntExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#binaryExpr.
    def visitBinaryExpr(self, ctx:PivoScriptParser.BinaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#hexExpr.
    def visitHexExpr(self, ctx:PivoScriptParser.HexExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#stringExpr.
    def visitStringExpr(self, ctx:PivoScriptParser.StringExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#idExpr.
    def visitIdExpr(self, ctx:PivoScriptParser.IdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PivoScriptParser#parensExpr.
    def visitParensExpr(self, ctx:PivoScriptParser.ParensExprContext):
        return self.visitChildren(ctx)



del PivoScriptParser