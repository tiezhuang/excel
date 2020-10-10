# !/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil
import wmi
import socket

c = wmi.WMI()


# CPU处理器
def printCPU():
    global cpu
    cpu = {}
    cpu["CPU核数"] = 0
    for i in c.Win32_Processor():
        cpu["处理器ID"] = i.ProcessorId.strip()
        cpu["CPU类型"] = i.Name
        cpu['系统名称'] = i.SystemName
        try:
            cpu["CPU核数"] = i.NumberOfCores
        except:
            cpu["CPU核数"] += 1
        cpu["CPU时钟频率"] = i.MaxClockSpeed
        cpu['CPU数据宽度（位数）'] = i.DataWidth
    print(cpu)
    return cpu


# 主板
def printMain_board():
    global boards
    boards = []
    # print len(c.Win32_BaseBoard()):
    for board_id in c.Win32_BaseBoard():
        tmpmsg = {}
        tmpmsg['主板UUID'] = board_id.qualifiers['UUID'][1:-1]  # 主板UUID,有的主板这部分信息取到为空值，ffffff-ffffff这样的
        tmpmsg['主板序列号'] = board_id.SerialNumber  # 主板序列号
        tmpmsg['主板生产厂家'] = board_id.Manufacturer  # 主板生产品牌厂家
        tmpmsg['主板型号'] = board_id.Product  # 主板型号
        boards.append(tmpmsg)
    print(boards)
    return boards


# BIOS
def printBIOS():
    global bioss
    bioss = []
    for bios_id in c.Win32_BIOS():
        tmpmsg = {}
        tmpmsg['BIOS特征码'] = bios_id.BiosCharacteristics  # BIOS特征码
        tmpmsg['BIOS版本'] = bios_id.Version  # BIOS版本
        tmpmsg['BIOS固件生产厂家'] = bios_id.Manufacturer.strip()  # BIOS固件生产厂家
        tmpmsg['BIOS释放日期'] = bios_id.ReleaseDate  # BIOS释放日期
        tmpmsg['系统管理规范版本'] = bios_id.SMBIOSBIOSVersion  # 系统管理规范版本
        bioss.append(tmpmsg)
    print(bioss)
    return bioss


# 硬盘
def printDisk():
    global disks
    disks = []
    for disk in c.Win32_DiskDrive():
        # print disk.__dict__
        tmpmsg = {}
        tmpmsg['硬盘序列号'] = disk.SerialNumber.strip()
        tmpmsg['硬盘ID'] = disk.DeviceID
        tmpmsg['描述'] = disk.Caption
        tmpmsg['磁盘大小'] = disk.Size
        disks.append(tmpmsg)
    for d in disks:
        print(d)
    return disks


# 内存
def printPhysicalMemory():
    global memorys
    memorys = []
    for mem in c.Win32_PhysicalMemory():
        tmpmsg = {}
        tmpmsg['BankLabel'] = mem.BankLabel
        tmpmsg['内存条序列号'] = mem.SerialNumber.strip()
        tmpmsg['内存条配置时钟速度'] = mem.ConfiguredClockSpeed
        tmpmsg['内存容量'] = mem.Capacity
        tmpmsg['内存条配置电压'] = mem.ConfiguredVoltage
        memorys.append(tmpmsg)
    for m in memorys:
        print(m)
    return memorys


# # 电池信息，只有笔记本才会有电池选项
# def printBattery():
#     isBatterys = False
#     for b in c.Win32_Battery():
#         isBatterys = True
#     return isBatterys


# 网卡mac地址：
def printMacAddress():
    global macs
    macs = []
    for n in c.Win32_NetworkAdapter():
        mactmp = n.MACAddress
        if mactmp and len(mactmp.strip()) > 5:
            tmpmsg = {}
            tmpmsg['MAC地址'] = n.MACAddress
            tmpmsg['网卡名称'] = n.Name
            tmpmsg['设备ID'] = n.DeviceID
            tmpmsg['适配类型'] = n.AdapterType
            tmpmsg['速度'] = n.Speed

            macs.append(str(tmpmsg))
    print(macs)
    return macs


# Ip地址
def printIPandHostName():
    try:
        global ip,host_name
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        a = "IP地址为：" + ip
        host_name = socket.gethostname()
        mm = "主机名为：" + host_name
        print(a)
        print(mm)

    finally:
        s.close()
    return ip,host_name


def process():
    global process
    process=[]
    for pnum in psutil.pids():
        a={}
        p = psutil.Process(pnum)
        a['进程名']=p.name()
        a['内存利用率']=p.memory_percent()
        a['进程状态']=p.status()
        a['创建时间']=p.create_time()
        process.append(str(a))
        # a = str(u"进程名 %-20s  内存利用率 %-18s 进程状态 %-10s 创建时间 %-10s " \
        #         % (p.name(), p.memory_percent(), p.status(), p.create_time()))
    print(process)
    return process



import MySQLdb
def dbBasicInfo():
    database = MySQLdb.connect(host="192.168.168.6", user="root", passwd="123456", db="testip", charset="utf8")
    # database = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="testip", charset="utf8")
# 获得游标对象, 用于逐行遍历数据库数据
    cursor = database.cursor()
    printCPU()
    printMain_board()
    printBIOS()
    printDisk()
    printPhysicalMemory()
    printMacAddress()
    # printBattery()
    printIPandHostName()
    process()

    text1 =str(cpu)
    text2 = str(boards)
    text3 = str(bioss)
    text4 = str(disks)
    text5 = str(memorys)
    text6 = str(macs)[13:30]#mac地址
    text7 = str(macs)[32:]#网卡信息
    text8 = str(ip)
    text9 = str(host_name)
    text10 = str(process)





    cursor.execute("insert into test123(cpu,zhuban,bios,disk,memorys,mac,ip,network_adapter,host_name) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",[text1,text2,text3,text4,text5,text6,text8,text7,text9])
    cursor.execute("insert into process(test123_ip,process) values(%s,%s)",[text8,text10])

# 提交
    database.commit()

# 关闭数据库连接

    cursor.close()
    database.close()




if __name__ == '__main__':
    dbBasicInfo()