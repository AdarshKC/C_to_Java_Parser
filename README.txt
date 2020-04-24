Group number: 4

Team members:
    Adarsh Chaudhary (1701CS01)
    Ankit Kumar (1701CS05)

Status: Completed

Files:
    1. C.g4: Grammar file for C
    2. mytest.py: The main file
    3. result.java: The output file
    4. README.txt: Meta information file
    5. Sample.c: Test case provided
    6. Sample.java; Output of Sample.c as per our code

Instruction for execution:
    1. Before executing make sure that your system has python3 and pycharm.
    2. Run the command: "python3 -m pip install antlr4-python3-runtime" in the terminal of Pycharm.
    3. Open the C.g4 file and generate ATLR recognizers by right clicking on Translation unit.
    4. This will create gen folder containing different Lexer, parser, Visitor files.
    5. Run the command: "python mytest.py input.c" in the pycharm terminal.
    6. This will generate result.java file which is the translation of input.c file to corresponding java file.

Some corner cases covered in of our Project: (Apart from basic translation)
    1. While converting proper indentations is maintained in the result.java file.
    2. Since java is a class based language so while converting, all the functions are translated accordingly as class functions.
    3. Nothing like "unsigned" exists in java so a list called ignoreList has been created which contains the keywords which is not there in the Java but present in C and during translation it ignores these keywords.
    4. In C we can define functions at one place and implement them later. Java doesn't support this feature so while converting, the code binds function definition and implementation together.
    5. Class function for header files has been created which can be further implemented while scaling the project.
    6. Proper comments in the main file for the better understanding of the code.

    