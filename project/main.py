import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from PivoScriptLexer import PivoScriptLexer
from PivoScriptParser import PivoScriptParser
from PivoScriptVisitor import PivoScriptVisitor

class LexerErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, symbol, line, column, msg, e):
        raise RuntimeError(f"Lexikální chyba v řádku {line}, sloupec {column}: {msg}")

class StopErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, symbol, line, column, msg, e):
        raise RuntimeError(f"Chyba v řádku {line}, sloupec {column}: {msg}")


class Evaluator(PivoScriptVisitor):
    def __init__(self):
        self.symbol_table = {}

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    def visitVarDecl(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        if ctx.expr():
            value = self.visit(ctx.expr())
        else:
            value = 0 
        self.symbol_table[var_name] = value
        return value

    def visitOutput(self, ctx):
        value = self.visit(ctx.expr())
        print(value)
        return value
    
    def visitIfStatement(self, ctx):
        condition = self.visit(ctx.condition())
        if condition:
            self.visit(ctx.block(0))
        elif ctx.block(1):
            self.visit(ctx.block(1))
        return None
    
    def visitForStatement(self, ctx):
        self.visit(ctx.varDecl())

        while self.visit(ctx.condition()):
            self.visit(ctx.block())
            self.visit(ctx.assignment())
        return None
    
    def visitAssignment(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        if var_name not in self.symbol_table:
            raise RuntimeError(f"Chyba: proměnná '{var_name}' nebyla deklarována.")
        value = self.visit(ctx.expr())
        self.symbol_table[var_name] = value
        return value

    def visitBlock(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)
        return None

    def visitCondition(self, ctx):
        return self.visit(ctx.logicalOr())

    def visitLogicalOr(self, ctx):
        result = self.visit(ctx.logicalAnd(0))
        for i in range(1, len(ctx.logicalAnd())):
            result = result or self.visit(ctx.logicalAnd(i))
        return result

    def visitLogicalAnd(self, ctx):
        result = self.visit(ctx.logicalNot(0))
        for i in range(1, len(ctx.logicalNot())):
            result = result and self.visit(ctx.logicalNot(i))
        return result

    def visitLogicalNot(self, ctx):
        if ctx.getChildCount() == 2:
            return not self.visit(ctx.logicalNot())
        else:
            return self.visit(ctx.comparison())

    def visitComparison(self, ctx):
        if ctx.expr():
            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            op = ctx.getChild(1).getText()
            if op == '==':
                return left == right
            elif op == '<':
                return left < right
            elif op == '>':
                return left > right
        else: 
            return self.visit(ctx.condition())

    def visitAddSubExpr(self, ctx):
        result = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.term(i))

            if (isinstance(result, str) or isinstance(right, str)) and op == '-':
                raise RuntimeError(f"Chyba: Nelze použít operaci '{op}' s řetězcem")

            if isinstance(result, str) and isinstance(right, str) and op == '+':
                result += right
            elif isinstance(result, str) and op == '+':
                result = result + str(right)
            elif isinstance(right, str) and op == '+':
                result = str(result) + right
            elif op == '+':
                result += right
            elif op == '-':
                result -= right
        return result

    def visitMulDivExpr(self, ctx):
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.factor(i))

            if isinstance(result, str) or isinstance(right, str):
                raise RuntimeError(f"Chyba: Nelze použít operaci '{op}' s řetězcem")

            if op == '/' and right == 0:
                raise RuntimeError("Chyba: Dělení nulou!")

            if op == '*':
                result *= right
            elif op == '/':
                result /= right
        return result

    def visitIntExpr(self, ctx):
        return int(ctx.INT().getText())
    
    def visitBinaryExpr(self, ctx):
        bin_value = ctx.BINARY().getText()[2:]
        return int(bin_value, 2)
    
    def visitHexExpr(self, ctx):
        hex_value = ctx.HEX().getText()[2:]
        return int(hex_value, 16)

    def visitStringExpr(self, ctx):
        return ctx.STRING().getText()[1:-1]

    def visitIdExpr(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        if var_name not in self.symbol_table:
            raise RuntimeError(f"Chyba: proměnná '{var_name}' nebyla deklarována.")
        return self.symbol_table[var_name]

    def visitParensExpr(self, ctx):
        return self.visit(ctx.expr())
    
    def visitNegExpr(self, ctx):
        value = self.visit(ctx.factor())
        return -value


def main():
    input_stream = FileStream(sys.argv[1], encoding='utf-8')

    lexer = PivoScriptLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(LexerErrorListener())

    stream = CommonTokenStream(lexer)

    parser = PivoScriptParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(StopErrorListener())

    try:
        print("Začínám parsovat...")
        tree = parser.program()
        print("Parsování dokončeno.")
        print(tree.toStringTree(recog=parser))

        evaluator = Evaluator()
        evaluator.visit(tree)

    except RuntimeError as e:
        print(e)
        sys.exit(1)  # Zastaví program, pokud je chyba při analýze
    except Exception as e:
        print(f"Chyba při analýze: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
