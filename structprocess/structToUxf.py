import sys
import clang.cindex
from clang.cindex import Index
from clang.cindex import Config
from clang.cindex import CursorKind
from clang.cindex import TypeKind
import pdb

class SNode:
    'SNode'
    ttype=''
    text=''
    level=0
    idx=0

    def __init__(self, ttype, text, level, idx):
        self.text = text
        self.level = level
        self.idx = idx
        self.ttype = ttype
    def toString(self,maxl):
        # if len(self.ttype) + len(self.text) > 20:
        #     return "<f" + str(self.idx) + "> "+ self.ttype + r'\n' + self.text
        sty = self.ttype + " "*(maxl - len(self.ttype) + 1)
        return sty + self.text

class PNode:
    'PNode'
    ttype=''
    text=''
    childs=[]
    def __init__(self, ttype, text):
        self.childs = []
        self.text = text
        self.ttype = ttype

libclangPath = r'/usr/lib/llvm-8/lib/libclang.so.1'
Config.set_library_file(libclangPath)

file_path = sys.argv[1]
index = Index.create()

tu = index.parse(file_path)
AST_root_node= tu.cursor

lpnode = []

tab = 0
def preorder_travers_AST(cursor):
    global tab

    for cur in cursor.get_children():
        t = cur.type
        #print(" " * tab * 4 + t.spelling + " " + cur.spelling +  " - > "+ str(cur.lexical_parent.spelling))
        if tab == 0:
            lpnode.append(PNode(t.spelling ,cur.spelling))
        else:
            p = lpnode[len(lpnode) - 1]
            p.childs.append(SNode(t.spelling, cur.spelling, tab, len(p.childs)))
        tab += 1
        if tab <= 1:
            preorder_travers_AST(cur)
        tab -= 1

preorder_travers_AST(AST_root_node)

outlines=[]

outlines.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
outlines.append('<diagram program="umlet" version="14.3.0">')
outlines.append('<zoom_level>10</zoom_level>')
loc=0
for p in lpnode:
    high=100
    outlines.append("<element>")
    outlines.append("<id>UMLClass</id>")
    outlines.append("<coordinates>")
    outlines.append("<x>"+str(loc)+"</x>")
    loc += 600
    outlines.append("<y>460</y>")
    outlines.append("<w>400</w>")
    high += len(p.childs) * 15
    if high > 1000:
        high = 1000
    outlines.append("<h>"+str(high)+"</h>")
    outlines.append("</coordinates>")
    outlines.append("<panel_attributes>")
    outlines.append("*"+p.ttype + " " + p.text+"*" + "\n--\n")

    maxl = 0
    for s in p.childs:
        if len(s.ttype) > maxl:
            maxl = len(s.ttype)

    sinfo=''
    for s in p.childs:
        sinfo += s.toString(maxl) + '\n'

    outlines.append(sinfo)

    outlines.append("</panel_attributes>")
    outlines.append("<additional_attributes/>")
    outlines.append("</element>")


outlines.append("</diagram>")

outFD = open("umlet.uxf", "w")
for line in outlines:
    outFD.write(line + '\n')

