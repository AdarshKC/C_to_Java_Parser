import sys
from antlr4 import *
from gen.CLexer import CLexer
from gen.CParser import CParser
from gen.CVisitor import CVisitor
import itertools

result = open('result.java', 'w')
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
    printFlag = 0
    c = 0
    stringLiteral = ""
    variableList = []
    dataList = ["d", "c", "f"]

    while len(contextList) > 0:

        t = 0
        firstChild = contextList[0]

        # if printFlag == 2:
        #     printFlag = 0

        if str(type(firstChild)) == "<class 'gen.CParser.CParser.FunctionDefinitionContext'>":
            funFlag = 1

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
            elif firstChild.getText() in ["printf"]:
                print("System.out.print", file=result, end="")
                printFlag = 1
                beginFlag = 0
            elif firstChild.getText() in ["int", "void"] and funFlag == 1:
                print("public static void", file=result, end=" ")
                beginFlag = 0
                funFlag = 0
            elif firstChild.getText() in ["main"]:
                print(firstChild.getText(), file=result, end=" ")
                argFlag = 1
            elif firstChild.getText() in ["}"]:
                print(firstChild.getText(), file=result, end="\n")
                tab -= 1
                beginFlag = 1
            elif firstChild.getText() in ["("] and argFlag == 1:
                print(firstChild.getText(), file=result, end=" ")
                ignore = 1
            elif firstChild.getText() in ["("]:
                print(firstChild.getText(), file=result, end=" ")
                c = -1
                if printFlag == 1:
                    printFlag = 2
            # elif firstChild.getText() in [")"]:
            #     printFlag = 0
            elif firstChild.getText() in [")"] and argFlag == 1:
                print("String[] args )", file=result, end=" ")
                ignore = 0
                argFlag = 0
            else:
                if printFlag == 2:
                    stringLiteral = firstChild.getText()
                    printFlag = 3
                elif printFlag == 3:
                    temp1 = 0
                    if firstChild.getText() in [")"]:
                        for var in stringLiteral:
                            if temp1 == 1:
                                if var == "d" or var == "f":
                                    print("\");\n", file=result, end="")
                                    for x in range(tab+1):
                                        print("\t", file=result, end="")
                                    print("System.out.print(", file=result, end=" ")
                                    if variableList[0] in ["argc"] :
                                        print("args.length+1 ) ;\n", file=result, end="")
                                    else:
                                        print(variableList[0] + " );\n", file=result, end="")
                                    for x in range(tab+1):
                                        print("\t", file=result, end="")
                                    print("System.out.print( \"", file=result, end="")
                                    variableList.pop(0)
                                else:
                                    print("%"+var, file=result, end="")
                                temp1 = 0
                            elif var == "%":
                                temp1 = 1
                            else:
                                print(var, file=result, end="")
                        variableList = [""]
                        c = -1
                        printFlag = 0
                        print(")", file=result, end="")
                    if firstChild.getText() not in [",", ")"]:
                        variableList.insert(c, variableList[c]+firstChild.getText())
                    else:
                        variableList.append("")
                        c += 1
                else:
                    if ignore == 0:
                        print(firstChild.getText(), file=result, end=" ")
                        beginFlag = 0

    print("}", file=result, end="")


if __name__ == '__main__':
    main(sys.argv)
