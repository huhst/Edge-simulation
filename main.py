# 导入库
import random

import pandas as pd
import numpy as np
import os
from file_generate import genSizeFile, dirsize  # 文件生成
from file_split import file_split      # 文件拆分
from env import Environment, Service, MEC, EdgeData   # 环境配置

# 服务与节点的保存位置
service_file_path = "service.csv"
mec_file_path = "mec.csv"

# 要拆分的文件大小

# 发起节点的单位成本
unit_cost = 50
# 边缘节点的单位成本
mec_unit_cost = []
# 数据大小(GB)
data_size = []
# 上传功率(m/s)
upload = []
# 带宽(m/s)
band_width = []
# 存储大小(GB)
mem_size = []
# 距离(km)
distance = []
# IOPS(写入速度)(m/s)
in_speed = []
# 已用存储(GB)
apply_size = []
# 数据类型
data_type = []

def sum(service_file_path,mec_file_path):
    """# 统计申请服务与边缘节点的个数"""
    service_num = 0
    for index, line in enumerate(open(service_file_path, 'r')):
        service_num += 1
    mec_num = 0
    for index, line in enumerate(open(mec_file_path, 'r')):
        mec_num += 1
    return service_num, mec_num

def get_index(service_file_path, mec_file_path, service_num, mec_num):
    """# 得到服务与节点的索引"""
    service = pd.read_csv(service_file_path, header=None, index_col=False)
    service_index = []
    for i in range(service_num):
        service_index.append(service.iloc[i, 0])
    mec = pd.read_csv(mec_file_path, header=None, index_col=False)
    mec_index = []
    for i in range(mec_num):
        mec_index.append(mec.iloc[i, 0])
    print(service_index, mec_index)
    return service_index, mec_index

def random_num(num):
    """随机生成节点的信息"""
    # 数据大小(GB)
    # 得到文件的大小
    dir = ["Data/bdd100k/test", "Data/bdd100k/train", "Data/bdd100k/val"]
    data_size = []
    for i in range(len(dir)):
        data_size.append(random.uniform(20, 40)*1024*1024*100)
        # data_size.append(dirsize(dir[i]))
    # 上传功率(m/s)
    upload = [np.random.randint(400, 900)]
    # 带宽(m/s)
    band_width = [np.random.randint(1, 155)for i in range(num)]
    # 存储大小(GB)
    mem_size = [np.random.randint(200, 400)for i in range(num)]
    # 距离(km)
    distance = [np.random.randint(1, 200)for i in range(num)]
    # IOPS(写入速度)(m/s)
    in_speed = [np.random.randint(400, 500)for i in range(num)]
    # 已用存储(GB)
    apply_size = [np.random.randint(10, 200)for i in range(num)]
    # 节点数据类型
    data_type = [np.random.randint(1, 3)for i in range(3)]
    # 节点的单位成本*
    mec_unit_cost = [np.random.uniform(42.5, 57.5)for i in range(num)]
    return data_size, upload, band_width, mem_size, distance, in_speed, apply_size, data_type, mec_unit_cost

def calculation(service_num, mec_num, service_index, mec_index, num):
    """计算时延和资源利用率"""
    # 保存los
    los = []
    # 保存传输时延
    pro_delay = []
    # 保存存储时延
    sto_delay = []
    # 保存时延
    all_delay = []
    # 保存资源闲置率
    res_idle_rate = []
    # 保存资源利用率
    res_utilization = []

    for i in range(num):
        # 得到los
        los.append(Environment(service_num, mec_num).Los(mec_index[i]))
        # 传输时延
        pro_delay.append(Environment(service_num, mec_num).getdelay(service_index[0], mec_index[i], los[i], delay_type=1))
        # 存储时延
        sto_delay.append(Environment(service_num, mec_num).getdelay(service_index[0], mec_index[i], los[i], delay_type=2))
        # 得到总时延
        all_delay.append(Environment(service_num, mec_num).getdelay(service_index[0], mec_index[i], los[i], delay_type=0))
        # 得到资源闲置率
        res_idle_rate.append(Environment(service_num, mec_num).Res(mec_index[i]))
        # 得到资源利用率
        res_utilization.append((1 - res_idle_rate[i]) * 100)
    # print(all_delay)
    # print(res_idle_rate)
    # print(res_utilization)
    return pro_delay, sto_delay, all_delay, res_utilization


def main():
    """主函数"""
    print("是否有配置文件，有请输入1，无请输入2")
    flag = eval(input())
    if flag == 1:
        ser_data, ser_data_line, ser_data_row = EdgeData().get_ser_file()
        print(ser_data)
        mec_data, mec_data_line, mec_data_row = EdgeData().get_mec_file()
        print(mec_data)

        # 服务文件的清空
        if os.path.isfile(service_file_path):
            os.remove(service_file_path)
        # 服务配置的导入
        for i in range(ser_data_line):
            print("这是第{}行".format(i))
            print(Service(ser_data.loc[i, 0], ser_data.loc[i, 1], ser_data.loc[i, 2], ser_data.loc[i, 3],
                          ser_data.loc[i, 4],ser_data.loc[i, 5], ser_data.loc[i, 6], ser_data.loc[i, 7],
                          ser_data.loc[i, 8], ser_data.loc[i, 9]))

            Service(ser_data.loc[i, 0], ser_data.loc[i, 1], ser_data.loc[i, 2], ser_data.loc[i, 3],
                    ser_data.loc[i, 4],ser_data.loc[i, 5], ser_data.loc[i, 6], ser_data.loc[i, 7],
                    ser_data.loc[i, 8], ser_data.loc[i, 9]).build()

        # 节点文件的清空
        if os.path.isfile(mec_file_path):
            os.remove(mec_file_path)

        #边缘节点配置的导入
        for i in range(mec_data_line):
            MEC(mec_data.loc[i, 0], mec_data.loc[i, 1], mec_data.loc[i, 2], mec_data.loc[i, 3],
                mec_data.loc[i, 4], mec_data.loc[i, 5], mec_data.loc[i, 6]).build()

        # 得到节点的索引值
        service_num, mec_num = ser_data_line, mec_data_line
        service_index = []
        mec_index= []
        for i in range(ser_data_line):
            service_index.append(i)
        for i in range(mec_data_line):
            mec_index.append(i)
        # print(service_index, mec_index)

        # 得到时延和资源利用率
        Pro_delay, sto_delay, all_delay, res_utilization = calculation(service_num, mec_num, service_index,
                                                                           mec_index, mec_data_line)
        print(all_delay)
        print(res_utilization)



    else:
        print("由于您没有配置文件，我们将为您随机生成")
        num = eval(input("请输入边缘节点的个数："))
        # 数据的生成
        data_size, upload, band_width, mem_size,distance, in_speed, apply_size, data_type, mec_unit_cost = random_num(num)

        # 服务文件的清空
        if os.path.isfile(service_file_path):
            os.remove(service_file_path)

        # 服务的创建
        for i in range(3):
            print(Service(0, i, data_size[i] / 1024 / 1024/100, upload[0], band_width[0]+10,
                    mem_size[0]+10, 0, in_speed[0]+10, apply_size[0], data_type[i]))
            Service(0, i, data_size[i] / 1024 / 1024/100, upload[0], band_width[0],
                    mem_size[0], 0, in_speed[0], apply_size[0], data_type[i]).build()
        # 节点文件的清空
        if os.path.isfile(mec_file_path):
            os.remove(mec_file_path)
        # 节点的创建
        for i in range(num):
            MEC(i, band_width[i], mem_size[i], distance[i], in_speed[i], apply_size[i], mec_unit_cost[i]).build()
        #得到节点的索引值
        service_num, mec_num = sum(service_file_path, mec_file_path)
        service_index, mec_index = get_index(service_file_path, mec_file_path, service_num, mec_num)
        # print(service_index, mec_index)

        # 得到时延和资源利用率
        Pro_delay, sto_delay, all_delay, res_utilization = calculation(service_num, mec_num, service_index, mec_index, num)
        print(all_delay)
        print(res_utilization)


