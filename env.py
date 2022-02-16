import csv
import numpy as np
import math
import pandas as pd


# 参数的定义
Pro_rate = 2*10**7    # 电磁波在铜线电缆中的传播速率(m/s)
# 默认理想信道带宽
bandwidth = 20        # 单位MHz
# 高斯噪声功率
Gaussian_noise = np.random.randint(1, 10)    # 单位W

class EdgeData:
    """
    与用户交互
    """

    def __init__(self):
        """
        获取文件的路径
        """
        # print("请输入配置信息")
        # ser_configuration = str(input("服务节点配置文件位置："))
        # self.ser_configuration = ser_configuration
        # mec_configuration = str(input("边缘节点配置文件位置："))
        # self.mec_configuration = mec_configuration

    def get_ser_file(self):
        # 服务节点的配置信息
        # print(self.ser_configuration)
        ser_configuration = str(input("服务节点配置文件位置："))
        ser_data = pd.read_csv(ser_configuration, header=None)
        return ser_data, ser_data.shape[0], ser_data.shape[1]

    def get_mec_file(self):
        # 边缘节点的配置信息
        mec_configuration = str(input("边缘节点配置文件位置："))
        # print(self.mec_configuration)
        mec_data = pd.read_csv(mec_configuration, header=None)
        return mec_data, mec_data.shape[0], mec_data.shape[1]


class Service:
    """
    服务
    """
    def __init__(self, index, task_index, data_size, upload, band_width, mem_size, distance, in_speed, apply_size, data_type):
        """
        初始化服务
        index: 编号
        data_size: 数据大小
        upload: 上传功率
        data_type :数据类型
        """
        self.index = index
        self.task_index = task_index
        # 数据大小
        self.data_size = data_size
        # 上传速度
        self.upload = upload
        # 带宽
        self.band_witch = band_width
        # 存储空间大小
        self.mem_size = mem_size
        # 距离
        self.distance = distance
        # 写入速度
        self.in_speed = in_speed
        # 已用空间
        self.apply_size = apply_size
        # 数据类型
        self.data_type = data_type

    def __str__(self):
        """
        返回字符串
        :return: 返回字符串
        """
        print(self.data_size)
        return "申请服务器编号:{},任务编号:{} 数据大小:{}(GB),上传功率:{}M/s,数据类型{}"\
            .format(self.index, self.task_index, int(self.data_size), self.upload, self.data_type)

    def build(self, name='service.csv', cnt=1):
        """
        生成csv数据集文件
        name: 文件名称
        cnt: 循环次数
        """
        with open(name, 'a', newline="") as f:
            writer = csv.writer(f)
            for i in range(cnt):
                ls = [self.index, self.task_index, int(self.data_size), self.upload, self.band_witch, self.mem_size,
                      self.distance, self.in_speed, self.apply_size, self.data_type]
                writer.writerow(ls)
            f.close()

    @staticmethod
    def read(count=1, name='service.csv'):
        """
        从文件中读取申请服务的节点信息
        name: 文件名
        return: 返回申请服务的节点信息
        """
        ans = []
        c = 0
        with open(name) as f:
            reader = csv.reader(f)
            for i, rows in enumerate(reader):
                if c < count:
                    ls = rows
                    ans.append(Service(ls[0], int(ls[1]), int(ls[2]), int(ls[3]), int(ls[4]),
                                       int(ls[5]), int(ls[6]), int(ls[7]), int(ls[8]), int(ls[9])))
                    c = c + 1
                else:
                    return ans
            return ans


class MEC:
    """
    边缘服务器
    """
    def __init__(self, index, band_width, mem_size, distance, in_speed, apply_size, unit_cost):
        # 索引
        self.index = index
        # 带宽
        self.band_width = band_width
        # 存储大小
        self.mem_size = mem_size
        # 距离
        self.distance = distance
        # IOPS(写入速度)
        self.in_speed = in_speed
        # 已用存储
        self.apply_size = apply_size
        # 单位成本
        self.unit_cost = unit_cost

    def __str__(self):
        """
        转换为字符串
        :return: 返回字符串
        """
        return "MEC编号:{},信道带宽:{}(m/s),存储大小:{}(GB),与申请节点的距离:{}KM,写入速度:{}m/s,已用存储:{}GB"\
            .format(self.index, self.band_width, self.mem_size, self.distance, self.in_speed, self.apply_size)

    # @staticmethod
    def build(self, name='mec.csv', cnt=1):
        """
        生成csv数据集文件
        name: 文件名称
        cnt: 循环次数
        """
        with open(name, 'a', newline="") as f:
            writer = csv.writer(f)
            for i in range(cnt):
                ls = [self.index, self.band_width, self.mem_size, self.distance, self.in_speed, self.apply_size,
                      self.unit_cost]
                writer.writerow(ls)
            f.close()

    @staticmethod
    def read(name='mec.csv', count=1):
        """
        从文件中读取边缘节点的基本信息
        name: 文件名
        return: 返回边缘节点的基本信息
        """
        ans = []
        with open(name) as f:
            reader = csv.reader(f)
            for i, rows in enumerate(reader):
                if i < count:
                    ls = rows
                    index = ls[0]
                    band_width = int(ls[1])
                    mem_size = int(ls[2])
                    distance = int(ls[3])
                    in_speed = int(ls[4])
                    apply_size = int(ls[5])
                    unit_cost = ls[6]
                    ans.append(MEC(index=index, band_width=band_width, mem_size=mem_size, distance=distance,
                                   in_speed=in_speed, apply_size=apply_size, unit_cost=unit_cost))
        return ans


class Environment:
    """
    环境
    """

    def __init__(self, service_num, mec_num):
        """
        创建环境
        service_num: 服务的数量
        mec_num: mec的数量
        """
        self.service_num = service_num
        self.mec_num = mec_num
        # 服务集
        self.services = Service.read(count=self.service_num)
        # mec集
        self.mecs = MEC.read(count=self.mec_num)

    def Los(self, mec_index):
        """
        计算los
        """
        a = -4
        distance = self.mecs[mec_index].distance
        los = distance**a
        return los

    def getdelay(self, service_index, mec_index, los, delay_type):
        """
        计算时延
        处理时延与排队时延忽略不计
        type = 0 返回总时延
        type = 1 返回传输时延
        type = 2 返回存储时延
        """
        # 数据大小
        data_size = self.services[service_index].data_size
        # 存储速率
        in_speed = self.mecs[mec_index].in_speed
        # print(in_speed)
        # 求信噪比
        los = los
        up_load = self.services[service_index].upload
        Signal_noise_ratio = (los*up_load)/Gaussian_noise

        # 分母
        den = bandwidth * math.log2(1 + Signal_noise_ratio)

        # 传输时延 = 信道长度(m)/电磁波在信道上的传播速率(m/s)

        Pro_delay = data_size/den

        # 存储时延
        sto_delay = data_size / in_speed

        # 总时延
        all_delay = Pro_delay + sto_delay
        if delay_type == 0:
            return all_delay
        if delay_type == 1:
            return Pro_delay
        if delay_type == 2:
            return sto_delay

    def Res(self, mec_index):
        """
        计算资源闲置率
        """
        mem_size = self.mecs[mec_index].mem_size
        apply_size = self.mecs[mec_index].apply_size
        res_idle_rate = (mem_size - apply_size)/mem_size
        return res_idle_rate

    def service_inf(self, service_index, los):
        """
        得到服务本身的时延和资源利用率
        """
        data_size = self.services[service_index].data_size
        # 存储速率
        in_speed = self.services[service_index].in_speed
        # print(in_speed)
        # 求信噪比
        los = los
        up_load = self.services[service_index].upload
        Signal_noise_ratio = (los * up_load) / Gaussian_noise
        # 分母
        den = bandwidth * math.log2(1 + Signal_noise_ratio)
        # 传输时延 = 信道长度(m)/电磁波在信道上的传播速率(m/s)
        # distance = self.mecs[mec_index].distance
        Pro_delay = data_size / den
        # 存储时延
        sto_delay = data_size / in_speed
        # 总时延
        all_delay = Pro_delay + sto_delay
        # 资源利用率
        mem_size = self.services[service_index].mem_size
        apply_size = self.services[service_index].apply_size
        res_idle_rate = (mem_size - apply_size) / mem_size
        return all_delay, res_idle_rate


class NetworkProtocol:
    """
    获取物联网设备的网络配置
    """
    def __init__(self, service_num, mec_num):
        """
        service_num: 服务的数量
        mec_num: mec的数量
        """
        self.service_num = service_num
        self.mec_num = mec_num
        # 服务集
        self.services = Service.read(count=self.service_num)
        # mec集
        self.mecs = MEC.read(count=self.mec_num)

    def services_decide(self, service_index):
        """
        判断网络类型与返回带宽
        """
        network = {"Wifi4": 200, "Wifi5": 1500, "Wifi6": 2400, "4G": 150, "5G": 2200}
        network_type = self.services[service_index].network_type
        for i in network.keys():
            if network_type == i:
                return network[i]

    def mec_decide(self, mec_index):
        """
        判断网络类型与返回带宽
        """
        network = {"Wifi4": 200, "Wifi5": 1500, "Wifi6": 2400, "4G": 150, "5G": 2200}
        network_type = self.mecs[mec_index].network_type
        for i in network.keys():
            if network_type == i:
                return network[i]


class File:
    """
    文件大小判断与协作请求
    """
    def __init__(self, service_num):
        """
        比较文件的大小
        """
        self.service_num = service_num
        self.services = Service.read(count=self.service_num)

    def compare(self, service_index):
        """
        通过索引获取文件大小
        """
        data_size = self.services[service_index].data_size
        mem_size = self.services[service_index].mem_size
        apply_size = self.services[service_index].apply_size
        # 剩余存储容量
        mem_space = mem_size - apply_size
        # 当申请服务的数据大于剩余存储容量时返回Ture
        if data_size > mem_space and data_size > 1:
            return True
        else:
            return False







