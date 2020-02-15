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

    tab = 0

    while len(contextList) > 0:
        t = 0
        firstChild = contextList[0]

        contextList.pop(0)
        if firstChild.getChildCount() > 0:
            for x in range(0, firstChild.getChildCount()):
                contextList.insert(t, firstChild.children[x])
                t = t + 1
        elif firstChild.getChildCount() == 0:
            if firstChild.getText() in [";", "{", "}"]:
                print(firstChild.getText(), file=result, end="\n")

            else:
                print(firstChild.getText(), file=result, end=" ")


if __name__ == '__main__':
    main(sys.argv)