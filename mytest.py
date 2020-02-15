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

    while len(contextList) > 0:

        t = 0
        firstChild = contextList[0]


        contextList.pop(0)
        if firstChild.getChildCount() > 0:
            for x in range(0, firstChild.getChildCount()):
                contextList.insert(t, firstChild.children[x])
                t = t + 1
        elif firstChild.getChildCount() == 0:
            if beginFlag == 1:
               # print("Tab-"+str(tab), file=result, end="")
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
            elif firstChild.getText() in ["}"]:
                print(firstChild.getText(), file=result, end="\n")
                tab -= 1
                beginFlag = 1
            else:
                print(firstChild.getText(), file=result, end=" ")
                beginFlag = 0

    print("}", file=result, end="")


if __name__ == '__main__':
    main(sys.argv)
