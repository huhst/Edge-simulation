# from numpy.random import seed
# import dataset__
# import algorithmAuc
# dn = 157
# nn = 15
#
# data, node, bid = dataset__.dataset(seed=96,Dn=dn, Nn=nn)
# ans = algorithmAuc.algorithmAUC(data,node,bid)
#
# print(ans)

import pandas as pd
a = input("请输入网络类型：")
network = {"Wifi4": 200, "Wifi5": 1500, "Wifi6": 2400, "4G": 150, "5G": 2200}
for i in network.keys():
    if a == i:
        print(network[i])
service = pd.read_csv("service.csv", header=None)
print(service)