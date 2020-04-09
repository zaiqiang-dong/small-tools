import sys
import clang.cindex
from clang.cindex import Index
from clang.cindex import Config
from clang.cindex import CursorKind
from clang.cindex import TypeKind
from graphviz import Digraph
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
    def toString(self):
        # if len(self.ttype) + len(self.text) > 20:
        #     return "<f" + str(self.idx) + "> "+ self.ttype + r'\n' + self.text
        return "<f" + str(self.idx) + "> "+ self.ttype + "  " + self.text

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
g = Digraph('structs', filename='structs_revisited.gv',
        node_attr={'shape': 'record', 'height':'.8'},engine='fdp', format='svg')

tab = 0
def preorder_travers_AST(cursor):
    global tab

    for cur in cursor.get_children():
        t = cur.type
        print(" " * tab * 4 + t.spelling + " " + cur.spelling +  " - > "+ str(cur.lexical_parent.spelling))
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


print("*"*100)
for p in lpnode:
    print(p.ttype + p.text)
    sname=p.ttype +r"\n"+ p.text
    sinfo='{ '
    c = len(p.childs)
    for s in p.childs:
        c -= 1
        if c > 0:
            sinfo += s.toString() + " | "
        else:
            sinfo += s.toString()

    sinfo +=' }'
    print(sinfo)
    g.node(sname, "<" + sname + "> " + sname + " | " + sinfo)


def get_index(lst, item):
    c = 0
    for i in lst:
        if i.ttype == item:
            return c
        else:
            c += 1
    return -1

print("*"*100)
for p in lpnode:
    print(p.text)
    sname=p.ttype +r"\n"+ p.text
    for s in p.childs:
        i = get_index(lpnode,s.ttype)
        if i != -1:
            tname = lpnode[i].ttype+r"\n"+lpnode[i].text
            g.edge(sname + ":<f" + str(s.idx) + ">", tname+":f<"+tname+">", len="9.00")

g.view()
