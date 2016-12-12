# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 19:46:19 2016
Apriori算法来发现频繁集
@author: XIAORAN
"""
import xlrd  
import time
import xlwt

begin = time.clock()

def readFileData():
    k = 0
    data = []
    
    bk = xlrd.open_workbook("outt.xls")
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

def readFileDataPuls():
    data = []
    
    bk = xlrd.open_workbook("fianData.xls")
    sh = bk.sheet_by_name("Sheet1")
    nrows = sh.nrows #行数
    for i in range(1,nrows):
        lineValues = sh.row_values(i)
        data.append(lineValues)
        
    return data

def loadDataSet():
    '''
    加载数据集，或者修改原始数据集为列表格式
    '''
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]


def createC1(dataSet):
    '''
    构建集合C1，是大小为1的所有候选项的集合，然后产生频繁集L1
    '''
    C1 = []
    for transaction in dataSet:#遍历数据集的所有事务
        for item in transaction:
            if not [item] in C1:#[item]集合不在,就加入
                C1.append([item])
    #C1.sort()#排序    
    
    return [frozenset(i) for i in C1]#对C1中每个项构建一个不变集合

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if frozenset(can).issubset(frozenset(tid)):
                if ssCnt.get(frozenset(can)) == None : ssCnt[frozenset(can)] = 1
                else: ssCnt[frozenset(can)] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData

def aprioriGen(Lk,k): #creats CK
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    
    return retList

def apriori(dataSet, minSupport = 0.06):
    C1 = createC1(dataSet)
    #print("dataSet的数据类型1111",type(dataSet))    
    D = list(map(set, dataSet)) 
    
    #print("dataSet的数据类型2222",D)
    L1, supportData = scanD(D,C1,minSupport)
    #print(L1,supportData)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2],k)
        Lk, supK = scanD(dataSet, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
        
    return L,supportData

ruleList = [] #记录所有的规则列表进行后处理数据，元素格式[set,set,confence]
deleteSet = frozenset(['S1','S2','S3','S4','H1','H2','H3','H4','R0',
                       'R1','R2','R3','R4','R5','J0','J1','J2','J3'])

def postRuleList(ruleList,deleteSet):#后处理结果数据
    postruleList = []
    for d in ruleList:
        if len(d[0] & deleteSet) == 0:
            postruleList.append(d)
    
    return postruleList

def postRuleList1(ruleList,deleteSet):#后处理结果数据
    postruleList = []
    for d in ruleList:
        s = set(d[0])
        if len(s - (d[0] & deleteSet))!=0:        
            postruleList.append([s - (d[0] & deleteSet),set(d[1]),d[2]])    
    return postruleList
    
        
        
def generateRulesPlus(L,supportData, minConf=0.75):
    bigRuleList = []
    for H1 in L[1]:
        
        for h1 in H1:
            h1 = frozenset([h1])
            conf = supportData[H1] / supportData[h1]
            if conf >= minConf:
                bigRuleList.append(((h1,supportData[h1]),(H1-h1,supportData[H1-h1]),conf,(h1,'-->',H1-h1)))
    for H1 in L[2]:
        for h1 in H1:
            h1 = frozenset([h1])
            conf = supportData[H1] / supportData[h1]
            if conf >= minConf:
                bigRuleList.append(((h1,supportData[h1]),(H1-h1,supportData[H1-h1]),conf,(h1,'-->',H1-h1)))
            conf = supportData[H1] / supportData[H1-h1]
            if conf >= minConf:
                bigRuleList.append(((H1-h1,supportData[H1-h1]),(h1,supportData[h1]),conf,(H1-h1,'-->',h1)))
                
    return bigRuleList
        

def generateRules(L,supportData, minConf=0.75):
    bigRuleList = []
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if(i > 1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else: calcConf(freqSet,H1,supportData,bigRuleList,minConf)

    return bigRuleList

def calcConf(freqSet,H,supportData,br1,minConf=0.75):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print(freqSet-conseq, '--->', conseq, 'conf:', conf)
            ruleList.append([freqSet-conseq, conseq, conf])
            br1.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)            
    return prunedH



def rulesFromConseq(freqSet,H,supportData,br1,minConf=0.75):
    m = len(H[0])
    if(len(freqSet) > m + 1):
        Hmp1 = aprioriGen(H,m + 1)
        Hmp1 = calcConf(freqSet,Hmp1,supportData,br1,minConf)
        if(len(Hmp1) > 1):
            rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf)
    

#运行代码
data = readFileDataPuls()
L,supportData = apriori(data, minSupport = 0.06)

bigRuleList = generateRulesPlus(L,supportData, minConf=0.75)

end = time.clock()

print('运行时间：%.2lf秒' % (end-begin))

