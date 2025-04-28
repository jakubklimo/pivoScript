import sys
from antlr4 import *
from PivoScriptLexer import PivoScriptLexer
from PivoScriptParser import PivoScriptParser
from PivoScriptVisitor import PivoScriptVisitor

class Evaluator(PivoScriptVisitor):
    def __init__(self):
        self.symbol_table = {}

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    def visitVarDecl(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        value = self.visit(ctx.expr())
        self.symbol_table[var_name] = value
        #print(f"Uložena proměnná {var_name} = {value}")
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
        if ctx.getChildCount() == 2:  # nenekamo něco
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
                print(f"Chyba: Nelze použít operaci '{op}' s řetězcem")
                return None

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

            # Chyba při dělení nebo násobení mezi řetězcem a číslem
            if isinstance(result, str) or isinstance(right, str):
                print(f"Chyba: Nelze použít operaci '{op}' s řetězcem")
                return None

            # Kontrola dělení nulou
            if op == '/' and right == 0:
                print("Chyba: Dělení nulou!")
                return float('inf')

            if op == '*':
                result *= right
            elif op == '/':
                result /= right
        return result

    def visitIntExpr(self, ctx):
        return int(ctx.INT().getText())
    
    def visitBinaryExpr(self, ctx):
        # Odstraníme prefix '0b' a převedeme binární číslo na desítkovou hodnotu
        bin_value = ctx.BINARY().getText()[2:]  # odstraníme '0b' prefix
        return int(bin_value, 2)  # převod binárního čísla na desítkové
    
    def visitHexExpr(self, ctx):
        # Odstraníme prefix '0x' a převedeme hexadecimální číslo na desítkovou hodnotu
        hex_value = ctx.HEX().getText()[2:]  # odstraníme '0x' prefix
        return int(hex_value, 16)  # převod hexadecimálního čísla na desítkové

    def visitStringExpr(self, ctx):
        return ctx.STRING().getText()[1:-1]

    def visitIdExpr(self, ctx):
        var_name = ctx.IDENTIFIER().getText()
        return self.symbol_table.get(var_name, 0)

    def visitParensExpr(self, ctx):
        return self.visit(ctx.expr())
    
    def visitNegExpr(self, ctx):
        value = self.visit(ctx.factor())
        return -value


def main():
    input_stream = FileStream(sys.argv[1], encoding='utf-8')

    lexer = PivoScriptLexer(input_stream)
    stream = CommonTokenStream(lexer)

    parser = PivoScriptParser(stream)
    tree = parser.program()

    print(tree.toStringTree(recog=parser))  # Debug: ukáže parsed strom

    evaluator = Evaluator()
    evaluator.visit(tree)

    # Volitelně - můžeš si vypsat symbol_table na konci
    #print(evaluator.symbol_table)

if __name__ == '__main__':
    main()
