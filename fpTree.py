# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 18:22:22 2016
@author: XIAORAN
"""

import numpy as np
import xlrd

def readFileData():
    data = []
    
    bk = xlrd.open_workbook("filename.xls")
    sh = bk.sheet_by_name("Sheet1")
    nrows = sh.nrows #行数
    for i in range(1,nrows):
        lineValues = sh.row_values(i)
        if(len(lineValues[8]) > 2):#讲多个症状单一分开
            for i in range(len(lineValues[8]),2):
                tmp = [t for t in lineValues[:8]]
                tmp.append(lineValues[8][i:i+2])
                tmp.append(lineValues[9])
                data.append(tmp) 
        else : data.append(lineValues)
        
    return data

def loadSimpDat():#测试数据
    simpDat = [['r','z','h','j','p'],
               ['z','y','x','w','v','u','t','s'],
               ['z'],
               ['r','x','n','o','s'],
               ['y','r','x','z','q','t','p'],
               ['y','z','x','e','q','s','t','m']]
    return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        if retDict.get(frozenset(trans)) == None :retDict[frozenset(trans)] = 0
        retDict[frozenset(trans)] += 1
    return retDict


class treeNode:
    def __init__(self,nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    def inc(self, numOccur):
        self.count += numOccur
    
    def disp(self, ind=1):
        print(ind, self.name, self.count)
        for child in self.children.values():
            child.disp(ind+1)
            

def createTree(dataSet, minSup=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item,0) + dataSet[trans]
            #print(headerTable.get(item,0),dataSet[trans])            
            
    #for k in headerTable.keys():
    #    if headerTable[k] < minSup: del headerTable[k]
            
    #print(headerTable)
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0: return None, None
    
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    
    retTree = treeNode('null Set', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
            
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(),key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems,retTree,headerTable,count)
                
    return retTree,headerTable    
    
    
def updateTree(items,inTree,headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else: 
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
    if len(items) > 1: 
        updateTree(items[1::], inTree.children[items[0]],headerTable,count)

def updateHeader(nodeToTest, targetNode):
    while(nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    
    nodeToTest.nodeLink = targetNode
    
def ascendTree(leafNode, prefixPath):
    if leafNode.parent !=None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
    

def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode !=None:
        prefixpath = []
        ascendTree(treeNode,prefixpath)
        if len(prefixpath) > 1:
            condPats[frozenset(prefixpath[1:])] = treeNode.count
        
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable,minSup,preFix,freqIntemList):
    bigL = [v[0] for v in headerTable.items()]
    #print(bigL)
    for basepat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basepat)
        freqIntemList.append(newFreqSet)
        condPatBases = findPrefixPath(basepat,headerTable[basepat][1])
        myCondTree, myHead = createTree(condPatBases,minSup)
    
    if myHead !=None:
        mineTree(myCondTree,myHead,minSup,newFreqSet,freqIntemList)








