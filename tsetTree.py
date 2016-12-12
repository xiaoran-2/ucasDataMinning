#coding=utf-8
import decisionTree
import xlrd
import Tree

def readFileDataPuls():
    data = []
    
    bk = xlrd.open_workbook("C:\\Users\\Administrator\\Desktop\\4 fill all blanks.xls")
    sh = bk.sheet_by_name("Sheet1")
    nrows = sh.nrows #行数
    for i in range(1,nrows):
        lineValues = sh.row_values(i)
        data.append(lineValues)
        
    return data
# myDat,lable = ad.createDataSet1()
# ad.printData(myDat)
# myTree=ad.createTree(myDat,lable)
# Tree.createPlot(myTree)
dataSet=readFileDataPuls()[150:200]
labels=[u'肝气郁结证型系数',
        u'热毒蕴结证型系数',
        u'冲任失调证型系数',
        u'气血两虚证型系数',
        u'脾胃虚弱证型系数',
        u'肝肾阴虚证型系数']
# data=xlrd.open_workbook("C:\\Users\\Administrator\\Desktop\\4 fill all blanks.xls")
# table=data.sheet_by_index(0)
# row=table.nrows
# col=table.ncols
# for i in range(row):
#     if i==0:
#         continue
#     L=[]
#     for j in range(col):
#         L.append(table.cell(i,j).value)
#     dataSet.append(L)
decisionTree.printData(dataSet)
myTree=decisionTree.createTree(dataSet, labels)
print myTree
Tree.createPlot(myTree)