#coding=gbk
import matplotlib.pyplot as plt
#�����ı���ͼ�ͷ��ʽ  
decisionNode = dict(boxstyle="sawtooth", fc="0.8") #�����жϽڵ���̬  
leafNode = dict(boxstyle="round4", fc="0.8") #����Ҷ�ڵ���̬  
arrow_args = dict(arrowstyle="<-") #�����ͷ  
  
#���ƴ���ͷ��ע��  
#nodeTxt���ڵ�����ֱ�ע, centerPt���ڵ�����λ��,  
#parentPt����ͷ���λ�ã���һ�ڵ�λ�ã�, nodeType���ڵ�����  
def plotNode(nodeTxt, centerPt, parentPt, nodeType):  
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',  
             xytext=centerPt, textcoords='axes fraction',  
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args )  
#����Ҷ�ڵ���  
def getNumLeafs(myTree):  
    numLeafs = 0  
    firstStr = myTree.keys()[0]   
    secondDict = myTree[firstStr]   
    for key in secondDict.keys():  
        if type(secondDict[key]).__name__=='dict':#�Ƿ����ֵ�  
            numLeafs += getNumLeafs(secondDict[key]) #�ݹ����getNumLeafs  
        else:   numLeafs +=1 #�����Ҷ�ڵ㣬��Ҷ�ڵ�+1  
    return numLeafs  
  
#�������Ĳ���  
def getTreeDepth(myTree):  
    maxDepth = 0  
    firstStr = myTree.keys()[0]  
    secondDict = myTree[firstStr]  
    for key in secondDict.keys():  
        if type(secondDict[key]).__name__=='dict':#�Ƿ����ֵ�  
            thisDepth = 1 + getTreeDepth(secondDict[key]) #������ֵ䣬�������1���ٵݹ����getTreeDepth  
        else:   thisDepth = 1  
        #�õ�������  
        if thisDepth > maxDepth:  
            maxDepth = thisDepth  
    return maxDepth  
#�ڸ��ӽڵ������ı���Ϣ  
#cntrPt:�ӽڵ�λ��, parentPt�����ڵ�λ��, txtString����ע����  
def plotMidText(cntrPt, parentPt, txtString):  
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]  
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]  
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30) 
#��������ͼ  
#myTree�������ֵ�, parentPt:���ڵ�, nodeTxt���ڵ�����ֱ�ע  
def plotTree(myTree, parentPt, nodeTxt):  
    numLeafs = getNumLeafs(myTree)  #��Ҷ�ڵ���  
    depth = getTreeDepth(myTree)    #���Ĳ���  
    firstStr = myTree.keys()[0]     #�ڵ��ǩ  
    #���㵱ǰ�ڵ��λ��  
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)  
    plotMidText(cntrPt, parentPt, nodeTxt) #�ڸ��ӽڵ������ı���Ϣ  
    plotNode(firstStr, cntrPt, parentPt, decisionNode) #���ƴ���ͷ��ע��  
    secondDict = myTree[firstStr]  
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD  
    for key in secondDict.keys():  
        if type(secondDict[key]).__name__=='dict':#�ж��ǲ����ֵ䣬  
            plotTree(secondDict[key],cntrPt,str(key))        #�ݹ��������ͼ  
        else:   #�����Ҷ�ڵ�  
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW  
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)  
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))  
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD  
  
#������ͼ��  
def createPlot(inTree):  
    fig = plt.figure(1, facecolor='white')  
    fig.clf()  
    axprops = dict(xticks=[], yticks=[])  
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)      
    plotTree.totalW = float(getNumLeafs(inTree)) #���Ŀ��  
    plotTree.totalD = float(getTreeDepth(inTree)) #�������  
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;  
    plotTree(inTree, (0.5,1.0), '')  
    plt.show() 