# -*- coding:utf-8 -*-
"""
__project_ = 'mqttclient'
__file_name__ = 'MqttClient_dev'
__author__ = 'xbxia'
__time__ = '2020/12/23 9:24'
__product_name = PyCharm
# code is far away from bugs with the god animal protecting

"""
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

client_id = "X1XXXQ2007060012|productid=a1s2d3|"  # walle平台
mqttc = mqtt.Client(client_id)
mqttc.username_pw_set("hd", "hdcloud890!")
# mqttc.username_pw_set("iotwedora", "cloud")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log


# 连接broker，心跳时间为60s
# mqttc.connect("172.16.22.170", 41564, 60)      #walle平台
#mqttc.connect("mapall.cn", 6811, 60)  # walle平台
#mqttc.connect("192.168.80.21", 50210, 60)
#mqttc.connect("mdtu.com", 50210, 60)
mqttc.connect("172.16.22.155", 51553, 60)   #ops开发测试环境
print('***2连接建立**')

num = 0  # 初始上报量
decimal = 3  # 默认两位小数点


def count1():
    global num, decimal
    num += 1.0
    # num = round(num, decimal)
    nu = format(num, '.{}f'.format(decimal))
    return nu


count = 0

def count2():
    global count, decimal
    count += random.uniform(0, 5)
    #count = round(count, decimal)
    co = format(count, '.{}f'.format(decimal))
    return co


# 定时发布主题
def fun_timer():
    global decimal
    now_time = dt.datetime.now().strftime('%F %T')
    print(now_time)

    # 发布消息
    content_dic1 = {
        "data": {
            "device": "202104101017",
            "timestamp": dt.datetime.now().strftime('%F %T'),
            #  "energy": random.randrange(10, 1000, 2)
            "energy": count1()
            #   "VD8": random.randint(0, 1),
            #  "VD7": random.uniform(30, 40)
        }
    }
    content1 = json.dumps(content_dic1)

    # 下位机2
    temp = format(random.uniform(20, 40), '.{}f'.format(decimal))
    humidity = format(random.uniform(40, 80), '.{}f'.format(decimal))

    content_dic2 = {
        "data": {
            "device": "202103260959",
            "timestamp": dt.datetime.now().strftime('%F %T'),
            # "temp": random.randrange(1000, 10000, 2),
            "temp": temp,
            "humidity": humidity
        }
    }
    content2 = json.dumps(content_dic2)

    # 发布消息
    content_dic3 = {
        "data": {
            "device": "202104101016",
            "timestamp": dt.datetime.now().strftime('%F %T'),
            #  "energy": random.randrange(10, 1000, 2)
            "energy": count2()
            #   "VD8": random.randint(0, 1),
            #  "VD7": random.uniform(30, 40)
        }
    }
    content3 = json.dumps(content_dic3)

    # 空调
    content_dic4 = {
        "data": {
            "device": "202106250906",
            "timestamp": dt.datetime.now().strftime('%F %T'),
            #  "energy": random.randrange(10, 1000, 2)
            "onff": random.randint(0, 1),
            "wind": random.randrange(1, 5, 1),
           # "temp": 28,
            "temp": format(random.uniform(26, 32), '.{}f'.format(decimal))
        }
    }
    content4 = json.dumps(content_dic4)

    #mqttc.publish("/UL/X1XXXQ2007060012/DPU/data", payload=content1, qos=0)

    #mqttc.publish("/UL/X1XXXQ2007060012/DPU/data", payload=content2, qos=0)

    #mqttc.publish("/UL/X1XXXQ2007060012/DPU/data", payload=content3, qos=0)

    mqttc.publish("/UL/X1XXXQ2007060012/DPU/data", payload=content4, qos=0)
    global timer
    timer = threading.Timer(60, fun_timer)
    timer.start()
    print('&&&&&&&&&')

mqttc.subscribe("/UL/X1XXXQ2007060012/DPU/data", 0)

timer = threading.Timer(1, fun_timer)
timer.start()
#mqttc.loop_start()
mqttc.loop_forever()