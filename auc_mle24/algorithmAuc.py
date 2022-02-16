import dataset__
import calculate__
import math
import numpy as np

'''
输入参数 ：
    node     : 编号    /数组
    unoccupy : 空闲率  /数组
    delay    : 总时延  /数组
输出数据：
    DicCompetion: 1->1 的 映射关系（用字典的键值队来表示）
计算公式：
    调用函数计算->选中节点的 空闲率和总时延的 权重（e1， e2） e1+e2=1
    e1 /(unoccupy+1) + e2 / (delay+1)
'''
#  1.偏好度的计算(竞争力)
def mapCompete(node, unoccupy, delay):
    
    # 1.1 对总时延 映射到1,2 的区间
    max = np.max(delay)
    min = np.min(delay)
    delay = ((delay - min) / max)

    # 1.2 计算对整体选中的协作节点的 在空闲率 和 总时延 方面的权重
    E1, E2 = calculate__.calculate_weight(len(node), unoccupy.tolist(), delay.tolist())    # 传入的是list副本
    #print(E1,E2)
    #  1.3 计算每个节点的竞争力并且保存到字典
    dicCompete = dict()    #  字典保存保存偏好度
    node = node.astype(int).tolist()    # node  变为整型的列表
    for j in node:    # j是节点编号, 比数组里面对应下标大一位
        dicCompete[j] = E1 /(unoccupy[j-1]+1) + E2 / (delay[j-1]+1)
        
    return dicCompete
# 这必不可能出错啊

'''
输入参数：
    dType: 数据类型有关的系数(1,2)  / float
    dSize: 协作节点j所购买的资源项大小 (这里即这项资源的大小) / float
    data/node
    node : 节点的编号  / 列表                               
    delaT: 资源项的数据传输到协作节点j的时延  / 数组                
    delaS: 资源项的数据写入到节点j的时延      / 数组                
    unit1: 是存储一单位大小资源项所需的存储空间 (默认为1) / 数组
输出数据：
    DicService:1->1 的 映射关系（用字典的键值队来表示）
计算公式：
    sij = dType(i)·log2( (dSize(i)/unit1(j)) - delaT - delaS ) 
    
'''
# 3. 满意度计算（服务质量）
def mapService(dType, dSize, node, delaT, delaS, unit1):
    
    #  3.1 对每个节点分别 计算他们存储数据项 i 的服务效能
    DIC_nodeService = dict()
    # node = node.astype(int).tolist()    # 复制一份协作节点编号的列表
    dicService = dict()
    for j in node:
        # 计算服务效能,存入字典构成映射
        antilog = (dSize/unit1[j-1]) - delaT[j-1] - delaS[j-1]
        if antilog < 0:
            dicService[j] = -9E6
        else:
            dicService[j] = dType*math.log2( antilog )

    return dicService
# 比不可能出错啊

'''
输入参数：
    beita:  期望系数           / float
    compN:  (偏好度)竞争力     / dic
    value:  数据项的单位价值   /  int
    node : 节点的编号          /   list
    bid  : 这些节点对资源项目i的报价  /array 一行
输出结果：

计算过程：
    standValue = beita * compN * value
    (standValue - bid) / standValue
    
'''
# 6. 计算期望获利比（对方让利比率）
def mapYieldRate(beita, value, node, compN, bid):
    # 计算标准定价 和 利润比
    dicYieldRate = dict()

    for j in node:
        standValue = beita * compN[j] * value
        dicYieldRate[j] = (standValue  - bid[j-1]) / standValue
    return dicYieldRate


'''
输入参数：
    m: 数据项的个数
    n: 协作节点的个数
    infoData, infoNode, infoBids
输出结果:
    映射: 数据项->(节点,成交价格)
    ...


'''
# 拍卖算法流程
def algorithmAUC(Data, Node, Bids, rate=0.5):
    
    dicDataToNode = dict()   
    delay = Node[:,2]+Node[:,3]
    
    #   循环对资源项开始拍卖.
    for i in Data[0:,0]:    #  i 即为数据项的编号(1->m)
        
        #  1.1 一个字典保存 发起节点 对协作节点的 偏好度
        #   调用mapCompete 计算偏好（参数：节点编号，空闲率， 总时延）
        dictCompetiom = mapCompete(Node[:,0],Node[:,5],delay)
        
        # 2. 对出价不符合发起节点预期的 协作节点作排除
        Ja = Node[:,0].astype(int).tolist()    #  拷贝一份所有节点编号的集合
        
        for j in Ja:    # 编号j比下标大1 编号i比下标同样大1
            if Bids[j-1][i-1] < Data[i-1][3] or Node[j-1,1]*Node[j-1,5] < Data[i-1,2]:
                Ja.remove(j)    #  对出价不符合要求的节点,从这个集合中删除
        
        
        if len(Ja) == 0:
            dicDataToNode[i] = (-1,-1)
            continue
        
        # 3. 对 Ja 中的节点计算满意度(服务效能)
        dicService = mapService(dType=Data[i-1,1], dSize=Data[i-1,2],node=Ja, 
                                delaT=Node[:,2], delaS=Node[:,3], unit1=Node[:,4])
                                                    
        
        # 4. 按照满意度（服务效能排序）
        sortService = sorted(dicService.items(), key=lambda items:items[1], reverse=True)    # 排序后的元组列表
        
        # 5.记录下排名前 rate=0.5 的节点
        Jb = []
        for j in range(math.ceil(len(sortService)*rate)):
            Jb.append(sortService[j][0])
            
            
        
        # 6. 得到期望系数 β
        beita = 1/max(dictCompetiom.values())
        
        # 7. 得到期望利率（对方的让利比）
        dicYieldRate = mapYieldRate(beita=beita, value=Data[i-1,3], node=Jb, compN=dictCompetiom, bid=Bids[:,i-1])
        
        # 8.排序期望利润
        sortYieldRate = sorted(dicYieldRate.items(), key=lambda items:items[1], reverse=True)
        
        # 9.记录下投标价和节点编号
        if (len(sortYieldRate) == 1):
            winner1 = sortYieldRate[0][0]
            endPrice = Bids[winner1-1,i-1]
            dicDataToNode[i] = (winner1, endPrice)
        else:
            winner1 = sortYieldRate[0][0]
            winner2 = sortYieldRate[1][0]
            endPrice = max(Bids[winner1-1,i-1], Bids[winner2-1,i-1])
            dicDataToNode[i] = (winner1, endPrice)
            
        #10.更新节点资源空闲率 和竞争力
        #10.1 资源空闲 = 现在空闲 / 总大小
        Node[winner1-1,5] = (Node[winner1-1,1] *  Node[winner1-1,5] - Data[i-1,2]) / Node[winner1-1,1] 
        #print(beita)
        
    #print(dicDataToNode)  
    return dicDataToNode

