# -*- coding:utf-8 -*-
"""
__project_ = 'mqttclient'
__file_name__ = 'MqttClient_dev'
__author__ = 'xbxia'
__time__ = '2020/12/23 9:24'
__product_name = PyCharm
# code is far away from bugs with the god animal protecting

"""

import os,sys,json,time
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )    #获取当前文件的绝对路径
sys.path.append(BASE_DIR)      #添加到系统环境变量中

# 测试读取配置文件
from env import readconf

conf = readconf.Read_conf()    #实例化类

# 获取mqttclient相关配置
host = conf.get_mqtt('host')
port = int(conf.get_mqtt('port'))
username = conf.get_mqtt('username')
password = conf.get_mqtt('password')
sn = conf.get_mqtt('sn')
productcode = conf.get_mqtt('productcode')

# 获取protocoldata相关配置
topic_pub = conf.get_data('topic_pub')
topic_name = conf.get_data('topic_name')
#topic = topic_pub + sn + topic_name          #拼接主题
Timer = int(conf.get_data('Timer'))
content = conf.get_data('content')
content = json.loads(content)     # 把发包内容转换成json格式，方便后面修改键值
#device = content['data']['device']
count = int(conf.get_data('count'))
# 每个网关的下位机
lp_count = int(conf.get_data('lp_count'))    # 下位机数量


# 使用定时器
import threading
import datetime as dt
import binascii  # ascii编码
from queue import Queue

# 生成随机数
import random

# mqtt客户端
import paho.mqtt.client as mqtt


def save(content):
    with open(r'result.txt', 'w+', encoding='utf-8') as fs:      #文本读写模式： r,r+; w, w+; a,a+
        fs.writelines(content + '\n')

# 一旦连接成功，回调此方法
def on_connect(mqttc, userdata, flags, rc):
    print("rc: " + str(rc))


# 一旦订阅到消息，回调此方法
def on_message(mqttc, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    # save(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# 一旦订阅成功，回调此方法
def on_subscribe(mqttc, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# 一旦有log，回调此方法
def on_log(mqttc, userdata, level, string):
    print(string)


#  累增计数器
num = 19  # 初始上报量
decimal = 0  # 默认两位小数点


def counter():
    global num, decimal
    #num += 1.0
    nu = format(num, '.{}f'.format(decimal))
    num += random.randrange(-1, 2, 1)
    return nu


# 生成设备sn,下位机device
def devCount(count, lp_count):
    global sn
    list, lp_list = [], []
    for i in range(count):
        list.append(sn + ("%08d" % i))
        print(list[i])
        for j in range(lp_count):
            lp_list.append(list[-1] + "_" + ("%d" % j))
            print(lp_list[j])
            i += 1    # 获取下一个设备sn
    #print(list, lp_list)   # 打印 设备列表，下位机列表
    return (list, lp_list)


class mqClient(object):
    def __init__(self, i):
        self.i = i
        self.client_id = list[i] + "|" + "productid=" + productcode + "|"  # 设备客户端连接
        self.mqttc = mqtt.Client(self.client_id)
        self.mqttc.username_pw_set(username, password)
        self.mqttc.on_message = on_message
        self.mqttc.on_connect = on_connect       # 设备连接
        self.mqttc.on_subscribe = on_subscribe
        self.mqttc.on_log = on_log
        print('***客户端连接**')
        # 连接broker，心跳时间为60s
        self.mqttc.connect(host, port, 60)  # ops开发测试环境
        print('***连接服务器**')
        self.topic = topic_pub + list[i] + topic_name


    def fun_timer(self):
        now_time = dt.datetime.now().strftime('%F %T')
        print(now_time)

        # 替换发包内容，如 下位机device
        for j in range(lp_count):
            print('发布第%d 个下位机数据包：' % j)
            j = j + self.i * lp_count
            content['data']['device'] = lp_list[j]
            content['data']['onoff'] = random.randint(0, 1)
            content['data']['wind'] = random.randrange(1, 5, 1)
            content['data']['temp'] = format(random.uniform(26, 32), '.{}f'.format(decimal))
            content['data']['setTemp'] = counter()
            # 发布消息
           # print('发布第%d 个下位机数据包：' % j)
            self.mqttc.publish(self.topic, payload=json.dumps(content), qos=0)

        threading.Timer(Timer, self.fun_timer).start()

    def run(self):
        self.mqttc.subscribe(self.topic, 0)
        #print('****订阅主题****')
        self.fun_timer()
        print('-------设备连接完成准备定时发包------')
        self.mqttc.loop_forever()



if __name__ == '__main__':
    list, lp_list = devCount(count, lp_count)
    usetimeSum = 0
    for i in range(count):
        s_t1 = time.time()
        mqttClient = mqClient(i)  # 类实例化
        #content1 = '第 %d 个设备连接： , clientid= %s ' % (i, mqttClient.client_id)
        #print(content1)
        print('第 %d 个设备连接： , clientid= %s ' % (i, mqttClient.client_id))
        #save(content1)
        e_t1 = time.time()    # 每个设备连接耗时
        usetimeSum += e_t1 - s_t1     #设备连接耗时
        #content2 = "设备连接总数：%s , 总耗时: %s 分钟" % (i, usetimeSum/60)
        #print(content2)
        print("设备连接总数：%s , 总耗时: %s 秒" % (i, usetimeSum))
       # save(content2)

        threading.Thread(target=mqttClient.run).start()



