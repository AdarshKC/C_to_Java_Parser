import sys
from antlr4 import *
from gen.CLexer import CLexer
from gen.CParser import CParser
from gen.CVisitor import CVisitor
import itertools

result = open('result.c', 'w')
contextList = []


class MyCVisitor(CVisitor):
    def __init__(self):
        pass

    def visitTranslationUnit(self, ctx):
        contextList.append(ctx)
        pass


def main(argv):
    inputFile = FileStream(argv[1])
    lexer = CLexer(inputFile)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()

    v = MyCVisitor()
    v.visit(tree)

    print("package demo;\n\npublic class DemoTranslation {\n", file=result, end="")
    tab = 0
    beginFlag = 1
    argFlag = 0
    ignore = 0
    funFlag = 0

    while len(contextList) > 0:

        t = 0
        firstChild = contextList[0]

        if str(type(firstChild)) == "<class 'gen.CParser.CParser.FunctionDefinitionContext'>":
            funFlag = 1

        # "<class 'gen.CParser.CParser.TypeSpecifierContext'>"

        contextList.pop(0)
        if firstChild.getChildCount() > 0:
            for x in range(0, firstChild.getChildCount()):
                contextList.insert(t, firstChild.children[x])
                t = t + 1
        elif firstChild.getChildCount() == 0:
            if beginFlag == 1:
                for x in range(tab):
                    print("\t", file=result, end="")
                if (firstChild.getText() != "}") and beginFlag == 1:
                    print("\t", file=result, end="")
            if firstChild.getText() in [";"]:
                print(firstChild.getText(), file=result, end="\n")
                beginFlag = 1
            elif firstChild.getText() in ["{"]:
                print(firstChild.getText(), file=result, end="\n")
                tab += 1
                beginFlag = 1
            elif firstChild.getText() in ["int", "void"] and funFlag == 1:
                print("public static void", file=result, end=" ")
                beginFlag = 0
                funFlag = 0
            elif firstChild.getText() in ["main"]:
                print(str(type(firstChild)))
                print(firstChild.getText(), file=result, end=" ")
                argFlag = 1
            elif firstChild.getText() in ["}"]:
                print(firstChild.getText(), file=result, end="\n")
                tab -= 1
                beginFlag = 1
            elif firstChild.getText() in ["("] and argFlag == 1:
                print(firstChild.getText(), file=result, end="")
                ignore = 1
            elif firstChild.getText() in [")"] and argFlag == 1:
                print("String[] args", file=result, end="")
                print(firstChild.getText(), file=result, end=" ")
                ignore = 0
                argFlag = 0
            else:
                if ignore == 0:
                    print(firstChild.getText(), file=result, end=" ")
                    beginFlag = 0

    print("}", file=result, end="")


if __name__ == '__main__':
    main(sys.argv)
