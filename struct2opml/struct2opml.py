#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import pdb
import sys


xmlInfo = '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
opmleInfoS = '<opml version="2.0">\n'
opmlHeadS = '\t<head>\n'
opmlBodyS = '\t<body>\n'
opmlLinuxS = '\t\t<outline text="linux">\n'
opmlLinuxE = '\t\t</outline>\n'
opmlHeadE = '\t</head>\n'
opmlBodyE = '\t</body>\n'
opmleInfoE = '</opml>\n'

class OpmlNode:
    'opml least node'
    comment=''
    macrodef=''
    text=''

    def __init__(self, comment, macrodef, text):
        self.comment = comment
        self.macrodef = macrodef
        self.text = text

    def toOpmlString(self):
        return '<outline text="'+self.text+'" />'

class Topic:
    'includ opml node topic'
    text = ''
    listOpmlNode = []

    def __init__(self, text):
        self.text = text
        self.listOpmlNode = []

    def addAOpmlNode(self, node):
        self.listOpmlNode.append(node)

    def toTopicString(self):
        ret='\t\t\t<outline text="'+self.text+'">\n'
        for i in self.listOpmlNode:
            ret += "\t\t\t\t"+i.toOpmlString()+"\n"
        ret+="\t\t\t</outline>\n"
        return ret


# open the out file and add begin info
outFile = open(sys.argv[2], "wb")
outFile.write(bytes(xmlInfo, encoding = "utf8"))
outFile.write(bytes(opmleInfoS, encoding = "utf8"))
outFile.write(bytes(opmlHeadS, encoding = "utf8"))
outFile.write(bytes(opmlHeadE, encoding = "utf8"))
outFile.write(bytes(opmlBodyS, encoding = "utf8"))
outFile.write(bytes(opmlLinuxS, encoding = "utf8"))
# end

# a = OpmlNode('zhushi 1', '#ifdef ABCDED-A', 'this node a')
# b = OpmlNode('zhushi 2', '#ifdef ABCDED-B', 'this node b')
# c = OpmlNode('zhushi 3', '#ifdef ABCDED-C', 'this node c')

# t = Topic("test")

# t.addAOpmlNode(a)
# t.addAOpmlNode(b)
# t.addAOpmlNode(c)

listTopic = []
source = open(sys.argv[1])


listMacro = []

def processOneLine(line):
    comment=''
    macrodef=''
    text=''
    haveGetReal = 0
    while haveGetReal == 0:
        line = line.strip()
        # r = line.find('stack')
        # if r > 0:
            # pdb.set_trace()
        sr = line.split(';', 1)
        for i in sr:
            if i == '' or i == '\n':
                continue
            searchObj = re.search( '(.*)#endif(.*)', i, re.S)
            if searchObj:
                listMacro.pop();
                continue
            searchObj = re.search( '(.*)#if(.*)', i, re.S)
            if searchObj:
                listMacro.append(i)
                continue

            # searchObj = re.search( '(.*)#ifdef(.*)', i, re.S)
            # if searchObj:
                # listMacro.append(i)
                # continue
            # searchObj = re.search( '(.*)#ifndef(.*)', i, re.S)
            # if searchObj:
                # listMacro.append(i)
                # continue
            # searchObj = re.search( '(.*)#if defined(.*)', i, re.S)
            # if searchObj:
                # listMacro.append(i)
                # continue
            # searchObj = re.search( '(.*)#if !defined(.*)', i, re.S)
            # if searchObj:
                # listMacro.append(i)
                continue
            searchObj = re.search( '(.*)\/\*(.*)', i, re.S)
            if searchObj:
                comment = comment + searchObj.group()
                searchObj = re.search( '(.*)\*\/(.*)', i, re.S)
                if searchObj:
                    continue
                else:
                    while 1:
                        line = source.readline()
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
            line = source.readline()
            searchObj = re.search( '(.*)}(.*?);', line, re.S)
            if searchObj:
                return None

    for m in listMacro:
        macrodef += m

    return OpmlNode(comment, macrodef, text)






def processEnumTopic():
    #pdb.set_trace()
    listNode = []
    while 1:
        line = source.readline()
        sr = line.split(';', 1)
        for i in sr:
            if i == '' or i == '\n':
                continue
            end = re.search( '(.*)}(.*?);', line, re.S)
            if end:
                e = Topic(end.group(2))
                for j in listNode:
                    e.addAOpmlNode(j)
                listTopic.append(e)
                print ('End for a Enum process. -->' + e.text)
                #outFile.write(bytes( t.toTopicString() , encoding = "utf8"))
                return;
            o = processOneLine(line)
            if o != None:
                listNode.append(o)
            else:
                print ('Get the end of Enum topic.')
                listTopic.append(e)
                return



def processStrucTopic(topic):
    t = Topic(topic)
    leftinclude = 1
    while 1:
        line = source.readline()
        #print (line)
        # r = line.find("vtime_snap")
        # if r > 0:
            # pdb.set_trace()
        searchResult = re.search( '(.*)}(.*?);', line, re.S)
        if searchResult:
            print ('End for a Struct process.' + t.text)
            #outFile.write(bytes( t.toTopicString() , encoding = "utf8"))
            listTopic.append(t)
            return
        sr = line.split(';', 1)
        for i in sr:
            if i == '' or i == '\n':
                continue
            searchResult = re.search( '(.*)struct (.*?) {', i, re.S)
            if searchResult:
                processStrucTopic(searchResult.group(2))
                continue
            searchResult = re.search( '(.*)enum(.*){', i, re.S)
            if searchResult:
                processEnumTopic()
                continue
            o = processOneLine(i)
            if o != None:
                t.addAOpmlNode(o)
            else:
                print ('Get the end of Struct topic.')
                listTopic.append(t)
                return




while 1:
    line = source.readline()
    #pdb.set_trace()
    if not line:
        break;
    searchResult = re.search( '(.*)struct (.*?) {', line, re.S)
    if searchResult:
        processStrucTopic(searchResult.group(2))
    searchResult = re.search( '(.*)enum(.*?){', line, re.S)
    if searchResult:
        processEnumTopic()




for t in listTopic:
    outFile.write(bytes( t.toTopicString() , encoding = "utf8"))

# add end info
outFile.write(bytes(opmlLinuxE, encoding = "utf8"))
outFile.write(bytes(opmlBodyE, encoding = "utf8"))
outFile.write(bytes(opmleInfoE, encoding = "utf8"))
# end
