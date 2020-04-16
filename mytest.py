import sys
from antlr4 import *
from gen.CLexer import CLexer
from gen.CParser import CParser
from gen.CVisitor import CVisitor
import itertools

result = open('result.java', 'w')
contextList = []
dataList = ["d", "c", "f", "s"]         # popular data types in c like %d, %c, %f, %s
ignoreList = ["unsigned"]

class MyCVisitor(CVisitor):
    def __init__(self):
        pass

    def visitTranslationUnit(self, ctx):            # store root of the traversal tree...
        contextList.append(ctx)
        pass


class coverCases():
    def printWithoutNewLine(self,var):              # print the word without newline
        print(var, file=result, end=" ")

    def printWithNewLine(self, var):                # print the word with newline
        print(var, file=result, end="\n")

    def spaceGeneration(self,tab):                  # for proper indentations...
        for x in range(tab):
            print("\t", file=result, end="")

    def checkIgnore(self,var):
        if var in ignoreList:                       # write nothing if found this...
            return 1
        return 0

def main(argv):

    inputFile = FileStream(argv[1])
    lexer = CLexer(inputFile)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.compilationUnit()

    v = MyCVisitor()
    v.visit(tree)

    print("package demo;\n\npublic class DemoTranslation {\n", file=result, end="")  # default format of java program

    tab = 0                                 # for handling indentation...
    beginFlag = 1                           # to check for line beginning...
    argFlag = 0                             # for command line input...
    ignore = 0                              # java translation for command line input...
    funFlag = 0                             # for return type of functions...
    printFlag = 0                           # to handle print statements...
    forFlag = 0                             # to handle for loop...
    c = 0                                   # index of variable list...
    declarationFlag = 0                     # to handle newline in declaration of arrays etc...
    stringLiteral = ""                      # message part in print statements...
    variableList = []                       # variables part in print statements...

    solve = coverCases()                    #instance of class to access class functions...

    while len(contextList) > 0:             # runs till we found node in the traversal tree...

        t = 0
        firstChild = contextList[0]
        contextList.pop(0)

        if str(type(firstChild)) == "<class 'gen.CParser.CParser.FunctionDefinitionContext'>":
            funFlag = 1
        if str(type(firstChild)) == "<class 'gen.CParser.CParser.DeclarationContext'>":
            declarationFlag += 1
        if firstChild.getText() in ["for"]:
            forFlag += 2

        if firstChild.getChildCount() > 0:
            for x in range(0, firstChild.getChildCount()):
                contextList.insert(t, firstChild.children[x])
                t = t + 1
        elif firstChild.getChildCount() == 0:   # enters when leaf is found...
            word = firstChild.getText()
            if beginFlag == 1:
                solve.spaceGeneration(tab)
                if (word != "}") and beginFlag == 1:
                    print("\t", file=result, end="")
            if solve.checkIgnore(word) :
                continue
            elif word in [";"]:               # new line begins after this...
                if forFlag == 0:
                    solve.printWithNewLine(word)
                    beginFlag = 1
                else:
                    forFlag -= 1
                    solve.printWithoutNewLine(word)
                declarationFlag = 0
            elif word in ["{"]:             # new line begins after this...
                if declarationFlag == 0:
                    solve.printWithNewLine(word)
                    tab += 1
                    beginFlag = 1
                else:
                    solve.printWithoutNewLine(word)
            elif word in ["printf"]:        # translate print statement...
                print("System.out.print", file=result, end="")
                printFlag = 1
                beginFlag = 0
            elif word in ["int", "void"] and funFlag == 1:  # handle return type of functions...
                print("public static " + word, file=result, end=" ")
                beginFlag = 0
                funFlag = 0
            elif word in ["main"]:
                solve.printWithoutNewLine(word)
                argFlag = 1
            elif word in ["}"]:             # new line begins after this...
                if declarationFlag == 0:
                    solve.printWithNewLine(word)
                    tab -= 1
                    beginFlag = 1
                else:
                    print(word, file=result, end=" ")
            elif word in ["("] and argFlag == 1:
                solve.printWithoutNewLine(word)
                ignore = 1
            elif word in ["("]:
                solve.printWithoutNewLine(word)
                c = -1
                if printFlag == 1:
                    printFlag = 2
            elif word in [")"] and argFlag == 1:
                print("String[] args )", file=result, end=" ")
                ignore = 0
                argFlag = 0
            else:                                       # translation of print arguments and messages(differently)...
                if printFlag == 2:                      # store message of print statement...
                    stringLiteral = word
                    printFlag = 3
                elif printFlag == 3:                    # variable part of print statement...
                    temp1 = 0
                    if word in [")"]:
                        for var in stringLiteral:       # look for data type in message part...
                            if temp1 == 1:
                                if var in dataList:     # if data type is found
                                    print("\");\n", file=result, end="")
                                    solve.spaceGeneration(tab+1) # for proper indentations...
                                    print("System.out.print(", file=result, end=" ")
                                    if variableList[0] in ["argc"]:     # command line input translation...
                                        print("args.length+1 ) ;\n", file=result, end="")
                                    else:
                                        print(variableList[0] + " );\n", file=result, end="")
                                    solve.spaceGeneration(tab+1) # for proper indentations...
                                    print("System.out.print( \"", file=result, end="")
                                    variableList.pop(0)
                                else:
                                    print("%"+var, file=result, end="")  # if % is not used as data type(like %d)...
                                temp1 = 0
                            elif var == "%":
                                temp1 = 1
                            else:
                                print(var, file=result, end="")
                        variableList = [""]                                           # reset variable list...
                        c = -1
                        printFlag = 0
                        print(")", file=result, end="")
                    if word not in [",", ")"]:
                        variableList.insert(c, variableList[c]+word)  # handle expression in print...
                    else:
                        variableList.append("")
                        c += 1
                else:
                    if ignore == 0:
                        solve.printWithoutNewLine(word)
                        beginFlag = 0

    print("}", file=result, end="")


if __name__ == '__main__':
    main(sys.argv)
