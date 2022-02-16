import random
import numpy as np
from numpy.ma.core import left_shift
from numpy.random import rand
random.seed(42)

'''
数据集合随机生成

目标输出:
    infoData: (dataNumber, dataType, dataSize, dataValue)  长度为m
               (数据项编号 , 数据类型 , 数据大小,  数据价值 )  不同的数据类型系数表示不同的数据类型.
               
    infoNode: (nodeNumber , storageSize, delayTransfer, delayStore, unitSize, unoccupy)  长度为n
               (协作节点编号, 存储空间大小, 传输数据的延迟, 存储的延迟 , unitSize,, 空闲率)  unitSize 单位大小资源项所需的存储空间
               
    infoBids: (b11, b12, b13 ... ... ... b1m)   n*m 关于投标价格的矩阵.
               (b21, b22, b23 ... ... ... b2m)
                .                           .
                .                           .
               (bn1, bn2, bn3 ... ... ... bnm)
输入参数：
    m: 数据项的个数
    n: 协作节点的个数



'''

def dataset(seed=42,Dn=300, Dtype=2, Dsize=(300, 0.25, 1.75), Dvalue=(200, 0.75, 1.25), 
            Nn=30, storage=(150000, 0.75, 1.25), delayTra=(50, 0.45, 1.45), delaySto=(50, 0.55, 1.45),
            unitSize=1, unoccupy=(0.15, 0.68)):
    random.seed(seed)
    #  构建测试数据项集合
    #  infoData: (dataNumber, dataType, dataSize, dataValue)
    dataInfo = []

    for i in range(Dn):
        list = []
        list.append(i+1)    #  dataNumber
        list.append(random.randint(1, Dtype))    #  dataType
        list.append(int(random.uniform(Dsize[1], Dsize[2])*Dsize[0]))    #  dataSize
        if list[1] == 1:    #  dataSize
            list.append(int(random.uniform(Dvalue[1], Dvalue[2])*Dvalue[0] * 1.014))
        else:    #  dataValue
            list.append(int(random.uniform(Dvalue[1], Dvalue[2])*Dvalue[0] * 1.235))
        dataInfo.append(list)

    dataInfo = np.array(dataInfo)

    #  构建测试协作节点的集合
    #  infoNode:(nodeNumber , storageSize, delayTransfer, delayStore, unitSize, unoccupy)
    nodeInfo = []
    for j in range(Nn):
        list = []
        list.append(j+1)
        list.append((random.uniform(storage[1], storage[2]) * storage[0]))
        list.append((random.uniform(delayTra[1], delayTra[2]) * delayTra[0]))
        list.append((random.uniform(delaySto[1], delaySto[2]) * delaySto[0]))
        list.append(unitSize)
        list.append(random.uniform(unoccupy[0], unoccupy[1]))
        nodeInfo.append(list)
    
    nodeInfo = np.array(nodeInfo)

    #  构建测试数据的 投标价集合  随机范围在 dataValue(0.62,1.15)
    bidsInfo = []
    for j in range(Nn):
        list = []
        for i in range(Dn):
            list.append(int(dataInfo[i,3]*random.uniform(0.62,1.15)))
        bidsInfo.append(list)

    bidsInfo = np.array(bidsInfo)

    return dataInfo, nodeInfo, bidsInfo










