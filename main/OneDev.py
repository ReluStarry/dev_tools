# -*- coding:utf-8 -*-
"""
__project_ = 'mqttclient'
__file_name__ = 'MqttClient_dev'
__author__ = 'xbxia'
__time__ = '2020/12/23 9:24'
__product_name = PyCharm
# code is far away from bugs with the god animal protecting

"""

import os,sys
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
topic = conf.get_data('topic')
time = int(conf.get_data('time'))
content = conf.get_data('content')

# 使用定时器
import threading
import datetime as dt
import binascii  # ascii编码

# 生成随机数
import random

# mqtt客户端
import paho.mqtt.client as mqtt
import json


def save(content):
    with open(r'topic.txt', 'a+', encoding='utf-8') as fs:
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


# 创建mqtt客户端,带有鉴权

client_id = sn + "|" + "productid=" + productcode + "|"         # 设备客户端连接
mqttc = mqtt.Client(client_id)
mqttc.username_pw_set(username, password)
# mqttc.username_pw_set("iotwedora", "cloud")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log


# 连接broker，心跳时间为60s
mqttc.connect(host, port, 60)   #ops开发测试环境
print('***2连接建立**')

# 定时发布主题
def fun_timer():
    global decimal
    now_time = dt.datetime.now().strftime('%F %T')
    print(now_time)

    # 发布消息
   # data = json.dumps(content)
    mqttc.publish(topic, payload=content, qos=0)
    global timer
    timer = threading.Timer(time, fun_timer)
    timer.start()
    print('&&&&&&&&&')

mqttc.subscribe(topic, 0)

timer = threading.Timer(1, fun_timer)
timer.start()
#mqttc.loop_start()
mqttc.loop_forever()