from antlr4 import *
from gen.XMLLexer import XMLLexer
from gen.XMLParser import XMLParser
from gen.XMLParserListener import XMLParserListener
import ast as tree
import os

# ------------ phase 1 --------------
class XMLParserListener(ParseTreeListener):
    def __init__(self):
        self.comboBox = []

    def enterElement(self, ctx: XMLParser.ElementContext):
        if ctx.children[1].getText() == "combobox":
            self.comboBox.append(ctx.children)


def find_combobox(file_path):
    stream = FileStream(file_path)
    lexer = XMLLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = XMLParser(token_stream)
    parse_tree = parser.document()
    myClass = XMLParserListener()
    walker = ParseTreeWalker()
    walker.walk(myClass, parse_tree)
    return myClass.comboBox

# ----------------phase 2 ------------------
class AST(XMLParserListener):
    def __init__(self):
        self.Tree = []
        self.root = ""

    def enterElement(self, ctx: XMLParser.ElementContext):
        self.root = str(ctx.Name()[0])

    def enterAttribute(self, ctx: XMLParser.AttributeContext):
        temp = {}
        temp["Method"] = str(ctx.Name())
        temp["Value"] = str(ctx.STRING())
        self.Tree.append(temp)

    def PrintAST(self):
        print(self.root)
        print("|")
        for i in range(len(self.Tree)):
            print("|___________________",
            self.Tree[i]["Method"], "-->", self.Tree[i]["Value"])
            if i != len(self.Tree)-1:
                print("|")
    # ----- phase 3 -----
    def generate_python_code(self):
        code = self.root + " = {"
        for i in range(len(self.Tree)):
            method = self.Tree[i]["Method"]
            value = self.Tree[i]["Value"]
            code += f"\n    {method}: {value},"
        code += "\n}"
        return code


if __name__ == '__main__':
    # phase 1
    address = "compilerProject.xml"
    answer = find_combobox(address)

    # phase 2
    comboBox = []
    for i in answer:
        combo = ""
        for j in i:
            if "id" in j.getText() or "name" in j.getText() or "value" in j.getText():
                combo = combo + " " + j.getText()
            elif "item" in j.getText():
                continue
            else:
                combo += j.getText()
        comboBox.append(combo)

    all_asts = []
    for tree in comboBox:
        input_stream = InputStream(tree)
        lexer = XMLLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = XMLParser(token_stream)
        parse_tree = parser.document()
        walker = ParseTreeWalker()
        myAST = AST()
        walker.walk(t=parse_tree, listener=myAST)
        all_asts.append(myAST)

    for ast in all_asts:
        ast.PrintAST()
        print("\n")
    print("---------------------------------------------------")
    # -------------- phase 3 PYQT5 mode---------------
    res = []
    for ast in all_asts:
        python_code = ast.generate_python_code()
        res.append(python_code)
        print(python_code)
        print("")
    print("------------------------")

def convertAst(inp):
    string = inp
    closing_tag_index = string.find('</combobox>')
    updated_string = string[:closing_tag_index]
    converted_string = '"' + updated_string + '"'
    return updated_string
    #print(converted_string)


def convertString(inp):
    conv = convertAst(inp)
    conv = conv.replace("<","")
    conv = conv.replace(">","")
    conv = conv.replace("combobox","")
    conv = conv.replace('" ','",')
    conv = "{" + conv + "}"
    conv = conv.replace("{ i","{i")
    return conv


def convertDict(conv):
    string = conv.strip("{}")
    pairs = string.split(",")
    dictionary = {}
    for pair in pairs:
        key, value = pair.split("=")
        value = value.strip('"')
        dictionary[key] = value
    return dictionary

lis = []
for i in comboBox:
    conv = convertString(i)
    final = convertDict(conv)
    lis.append(final)
# print(type(final)
# print(len(comboBox))
# print(res)
ls = []
for i in lis:
    ls.append(i['value'])
ls2 = []
for i in lis:
    ls.append(i['name'])
ls3 = []
for i in lis:
    ls.append(i['id'])


#
def generate_python_code(input_file_path, output_file):
    with open(input_file_path) as input_file:
        lines = input_file.readlines()

    for line in lines:
        output_file.write(line)

#
def writeString(string,outputFile):
    outputFile.write(string)

# finalFile = "genereatedcode.py"
# if os.path.exists(finalFile):
#     os.remove(finalFile)
#
# file = open(r"" + finalFile, "a")
# generate_python_code("libraries.txt",file)
# file.write("\n")
# generate_python_code("header.txt",file)
# file.write("\n")
# writeString(f"\t\tlist = {ls}",file)
# file.write("\n")
# generate_python_code("restFunction.txt",file)
# file.write("\n")
# generate_python_code("footer.txt",file)
# file.write("\n")


# ------------------- Phase 3 Normal python code mode -------------------


finalFile = "genereatedcode2.py"
file = open(r"" + finalFile, "a")


generate_python_code("libraries.txt",file)
file.write("\n")
writeString(f"comboBoxes = {lis}",file)
file.write("\n")
loop = "for i in comboBoxes:\n"
prnt = "\tprint(i)\n"
writeString(loop,file)
writeString(prnt,file)
writeString("print(len(comboBoxes))",file)
