# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 23:21:55 2016

@author: XIAORAN
"""
import pandas as pd
from sklearn.cluster import KMeans

datafile = 'data.xls' #待聚类的数据
processedfile = 'data_processed.xls' #数据处里后的文件
tryfile = 'data_tryfile.xls' #数据处里后的文件

typelabel = {u'肝气郁结证型系数':'A', u'热毒蕴结证型系数':'B', u'冲任失调证型系数':'C',             
             u'气血两虚证型系数':'D', u'脾胃虚弱证型系数':'E', u'肝肾阴虚证型系数':'F'}

k = 4 #聚类的类别数

#读取数据并进行聚类分析
data = pd.read_excel(datafile) #读取数据
keys = list(typelabel.keys())
result = pd.DataFrame()

if __name__ == '__main__': #判断是否是主窗口运行
    
    for i in range(len(keys)):
        print(u'正在进行 “%s” 的聚类...' % keys[i])
        kmodel = KMeans(n_clusters = k)
        lists = [[i] for i in data[keys[i]]]
        kmodel.fit(lists) #训练模型
        
        r1 = pd.DataFrame(kmodel.cluster_centers_, columns = [typelabel[keys[i]]])
        r2 = pd.Series(kmodel.labels_).value_counts() #分类统计
        r2 = pd.DataFrame(r2, columns = [typelabel[keys[i]]+'n'])
        
        r = pd.concat([r1, r2], axis = 1).sort(typelabel[keys[i]])
        r.index = [1,2,3,4]
        r[typelabel[keys[i]]] = pd.rolling_mean(r[typelabel[keys[i]]], 2)
        r[typelabel[keys[i]]][1] = 0.0

        result = result.append(r.T)
    result = result.sort()
    result.to_excel(processedfile)
    
dataCopy = data.copy()
for i in range(len(keys)):
    print(u'正在进行 “%s” 的聚类...' % keys[i])
    kmodel = KMeans(n_clusters = k)
    lists = [[i] for i in dataCopy[keys[i]]]
    kmodel.fit(lists) #训练模型
    for j in range(len(dataCopy[keys[i]])):
        dataCopy[keys[i]][j] = typelabel[keys[i]] + str(kmodel.predict([dataCopy[keys[i]][j]])[0]+1)
        
dataCopy.to_excel(tryfile)



        
    
    










    