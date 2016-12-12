# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 20:23:10 2016

@author: XIAORAN
"""
import random
import math
import numpy as np
import pandas as pd

def distManHaDu(vecA,vecB): #曼哈顿距离 
    return math.fabs(vecA - vecB)

def randCenter(dataSet,k): #随机构建k个质心
    n = np.shape(dataSet)[1]
    m = np.shape(dataSet)[0]
    centroids = np.mat(np.zeros([k,n]))
    j = 0
    vis = {}
    while j <k:
        index = int(m * random.random())        
        if index not in vis.keys(): 
            centroids[j,:] = dataSet[index,:]; j += 1; vis[index] = 1
    
    return centroids

def kMeans(dataSet,k,dist=distManHaDu,createCent=randCenter):
    m = np.shape(dataSet)[0]
    clusterAssment = np.mat(np.zeros((m,2)))    
    centroids = createCent(dataSet,k)
    clusterChange = True
    while clusterChange:
        clusterChange = False
        for i in range(m):
            minDist = np.inf; minIndex = -1
            for j in range(k):
                distJ = dist(centroids[j,:],dataSet[i,:])
                if distJ < minDist:
                    minDist = distJ; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChange = True
            clusterAssment[i,:] = minIndex,minDist ** 2
        #print(centroids)
        for cent in range(k):
            ptsInclust = dataSet[np.nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:] = np.mean(ptsInclust,axis=0)        
    return centroids,clusterAssment

def getAllCenter(data,s = ['A','B','C','D','E','F']):
    
    center = []
    cluster = []
    for i in range(len(s)):
        dataSet = loadData(data,s[i])
        cen,clu = kMeans(dataSet,4)
        #print(11111111111111111111)
        center.append(cen)
        cluster.append(clu)
    return center,cluster

def writeFile(center,data,s=['A','B','C','D','E','F']):#center[A..F],S=[A..F],data[A..F]    
    finalfile='fianlfile.xls'
    for i in range(len(center)):    
        for j in range(len(data[s[i]])):
            d = np.array([data[s[i]][j]])
            print(d)
            dt = np.abs(center[i] - d)
            #print(data[d,:],dt)
            tmp = np.min(dt) == dt 
            k = [v for v in range(len(tmp)) if tmp[v] == True][0]
            data[s[i]][j] = s[i]+str(k+1)
            #print(s[i]+str(k+1))
            
    data.to_excel(finalfile)



def readFile():  #从文件中读入所有数据
    datafile = 'data.xls' #待聚类的数据
    processedfile = 'processedData.xls' #离散数据处里后的文件
    tryfile = 'dataZuifile.xls' #最后数据处里后的文件

    typelabel = {u'肝气郁结证型系数':'A', u'热毒蕴结证型系数':'B', u'冲任失调证型系数':'C',             
             u'气血两虚证型系数':'D', u'脾胃虚弱证型系数':'E', u'肝肾阴虚证型系数':'F'}
    
    data = pd.read_excel(datafile,names = ['A','B','C','D','E','F']) #读取数据
    return data

def loadData(data,s):#得到数据的第 A 列的数据，进行聚类, s = ['A','B','C','D','E','F']   
    k = 4 #聚类的类别数

    #读取数据并进行聚类分析
    data1 = [[data.get_value(i,s)] for i in range(len(data))]
    dataSet = np.array(data1)
    
    return dataSet






    


    

    
    
    
    
    
    
    
    
    
    