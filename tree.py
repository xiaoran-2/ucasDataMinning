# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 21:53:21 2016

@author: XIAORAN
"""
import xlrd

from sklearn import tree
X = [[0, 0], [1, 1]]
Y = [0, 1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)


def readFileDataPuls():
    data = []
    
    bk = xlrd.open_workbook("outt.xls")
    sh = bk.sheet_by_name("Sheet1")
    nrows = sh.nrows #行数
    for i in range(0,nrows):
        lineValues = sh.row_values(i)
        data.append(lineValues)
        
    return data

d1 = set(['D3','F3'])
d2 = set(['D3','F3','H4'])
k1 = 0
k2 = 0
data = readFileDataPuls()
for d in data:
    if d1.issubset(set(d)):
        k1 += 1    
    if d2.issubset(set(d)):
        k2 += 1
        
r1 = k1/len(data)
r2 = k2/len(data)

print(r2/r1)


