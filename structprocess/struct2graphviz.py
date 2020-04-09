#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import pdb
import sys
from graphviz import Digraph


def getLayout(level):
    ret= '\t\t\t'
    while level > 0:
        level -=1
        ret +='\t'
    return ret

class Node:
    'Node'
    comment=''
    macrodef=''
    text=''
    level=0

    def __init__(self, comment, macrodef, text, level):
        self.comment = comment
        self.macrodef = macrodef
        self.text = text
        self.level = level


    def toString(self):
        return ''


class OpmlNode(Node):
    'opml least node'
    def __init__(self, text, level, comment, macrodef):
        Node.__init__(self,comment,macrodef,text,level)

    def toString(self):
        return self.text

class TopicNode(Node):
    'includ opml node topic'
    listSubNode = []
    def __init__(self, text, level, comment='',macrodef=''):
        Node.__init__(self,comment,macrodef,text,level)
        self.listSubNode = []

    def addSubNode(self, node):
        self.listSubNode.append(node)

    def toString(self):
        ret = "{"
        for i in self.listSubNode:
            ret += i.toString() + " | "
        ret += "}"
        return ret



listTopic = []
source = open(sys.argv[1])

def getLine():
    line = source.readline()
    return line


listMacro = []

def processOneLine(line, level):
    comment=''
    macrodef=''
    text=''
    haveGetReal = 0
    while haveGetReal == 0:
        line = line.strip()
        sr = line.split(';', 1)
        for i in sr:
            if i == '' or i == '\n':
                continue
            searchResult = re.search( '(.*)struct(.*?){', i, re.S)
            if searchResult:
                return  processStrucTopic('struct ' + searchResult.group(2), level+1)
            searchResult = re.search( '(.*)enum(.*){', i, re.S)
            if searchResult:
                return  processEnumTopic(level+1,searchResult.group(2))
            searchResult = re.search( '(.*)union(.*){', i, re.S)
            if searchResult:
                return processUnionTopic(level+1)
            searchObj = re.search( '(.*)#define(.*)', i, re.S)
            if searchObj:
                continue
            searchObj = re.search( '(.*)#endif(.*)', i, re.S)
            if searchObj:
                if len(listMacro) > 1:
                    listMacro.pop();
                continue
            searchObj = re.search( '(.*)#if(.*)', i, re.S)
            if searchObj:
                listMacro.append(i)
                continue

            searchObj = re.search( '(.*)#else(.*)', i, re.S)
            if searchObj:
                if len(listMacro) > 1:
                    listMacro.pop();
                continue
            searchObj = re.search( '(.*)\/\*(.*)', i, re.S)
            if searchObj:
                comment = comment + searchObj.group()
                searchObj = re.search( '(.*)\*\/(.*)', i, re.S)
                if searchObj:
                    continue
                else:
                    while 1:
                        line = getLine()
                        comment = comment + line
                        searchObj = re.search( '(.*)\*\/(.*)', line, re.S)
                        if searchObj:
                            break
                    continue
            splitR = i.rsplit(' ', 1)
            if len(splitR) > 1:
                text = splitR[0] + '  :  ' + splitR[1]
            else:
                text = i
            haveGetReal = 1
        if haveGetReal == 0:
            line = getLine()
            #print (line)
            searchObj = re.search( '(.*)}(.*?);', line, re.S)
            if searchObj:
                return None

    for m in listMacro:
        macrodef += m

    return OpmlNode(text, level, comment, macrodef)






def processEnumTopic(level, t=' '):
    listNode = []
    while 1:
        line = getLine()
        end = re.search( '(.*)}(.*?);', line, re.S)
        if end:
            if t==' ':
                t = end.group(2)
            e = TopicNode('enum :' + t, level)
            for j in listNode:
                e.addSubNode(j)
            if level ==0:
                listTopic.append(e)
                return None
            else:
                return e
        o = processOneLine(line, level+1)
        if o != None:
            listNode.append(o)
        else:
            if level ==0:
                listTopic.append(e)
                return None
            else:
                return e


def processUnionTopic(level):
    t = TopicNode('union :', level)
    while 1:
        line  = getLine()
        searchResult = re.search( '(.*)}(.*?);', line, re.S)
        if searchResult:
            print ('End for a Struct process.' + t.text)
            if level == 0:
                listTopic.append(t)
                return None
            else:
                return t
        searchResult = re.search( '(.*)struct(.*?){', line, re.S)
        if searchResult:
            nt = processStrucTopic('struct '+searchResult.group(2), level+1)
            t.addSubNode(nt)
            continue
        searchResult = re.search( '(.*)enum(.*){', line, re.S)
        if searchResult:
            e = processEnumTopic(level+1,searchResult.group(2))
            t.addSubNode(e)
            continue
        searchResult = re.search( '(.*)union(.*){', line, re.S)
        if searchResult:
            e = processUnionTopic(level+1)
            t.addSubNode(e)
            continue
        end = re.search( '(.*)}(.*?);', line, re.S)
        if end:
            if level ==0:
                listTopic.append(t)
                return None
            else:
                return t
        o = processOneLine(line, level+1)
        if o != None:
            t.addSubNode(o)
        else:
            if level ==0:
                listTopic.append(t)
                return None
            else:
                return t




def processStrucTopic(topic, level):
    t = TopicNode(topic, level)
    leftinclude = 1
    while 1:
        line = getLine()
        # r = line.find("vtime_snap")
        # if r > 0:
            # pdb.set_trace()
        searchResult = re.search( '(.*)}(.*?);', line, re.S)
        if searchResult:
            print ('End for a Struct process.' + t.text)
            if level == 0:
                listTopic.append(t)
                return None
            else:
                return t
        searchResult = re.search( '(.*)struct(.*?){', line, re.S)
        if searchResult:
            nt = processStrucTopic('struct '+searchResult.group(2), level+1)
            t.addSubNode(nt)
            continue
        searchResult = re.search( '(.*)enum(.*){', line, re.S)
        if searchResult:
            e = processEnumTopic(level+1,searchResult.group(2))
            t.addSubNode(e)
            continue

        searchResult = re.search( '(.*)union(.*){', line, re.S)
        if searchResult:
            e = processUnionTopic(level+1)
            t.addSubNode(e)
            continue
        o = processOneLine(line, level+1)
        if o != None:
            t.addSubNode(o)
        else:
            if level == 0:
                listTopic.append(t)
                return None
            else:
                return t


while 1:
    line = getLine()
    #pdb.set_trace()
    if not line:
        break;
    searchResult = re.search( '(.*)struct (.*?) {', line, re.S)
    if searchResult:
        processStrucTopic(searchResult.group(2),0)
    searchResult = re.search( '(.*)enum(.*?){', line, re.S)
    if searchResult:
        processEnumTopic(0)



s = Digraph('structs', filename='structs_revisited.gv',
            node_attr={'shape': 'record'}, format='svg')

for t in listTopic:
    s.node(t.text, t.text + " | "+ t.toString())

s.view()
