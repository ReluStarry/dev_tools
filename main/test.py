
import os,sys,json
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )    #获取当前文件的绝对路径
sys.path.append(BASE_DIR)      #添加到系统环境变量中

# 测试读取配置文件
from env import readconf

conf = readconf.Read_conf()    #实例化类

# 获取mqttclient相关配置
host = conf.get_mqtt('host')    #传参
port = int(conf.get_mqtt('port'))
username = conf.get_mqtt('username')
password = conf.get_mqtt('password')
sn = conf.get_mqtt('sn')
productcode = conf.get_mqtt('productcode')

# 获取protocoldata相关配置
topic_pub = conf.get_data('topic_pub')
topic_name = conf.get_data('topic_name')
topic = topic_pub + sn + topic_name
Timer = conf.get_data('Timer')
content = conf.get_data('content')
content = json.loads(content)        # 把str转换成json字典
#print(type(content))
#device = content['data']['device']

count = int(conf.get_data('count'))      # 网关数量
lp_count = int(conf.get_data('lp_count'))    # 下位机数量

# 下位机

# 替换device
#content['data']['device'] = lp_device

# 网关数量
def devCount(count, lp_count):
    global sn
    list, lp_list = [], []
    for i in range(count):
       # sn = sn + ("%08d" % i)
        list.append(sn + ("%08d" % i))
       # print('------')
        l= list[-1]
       # print(list)
        for j in range(lp_count):
           # print('获取最后一位元素')
            #print(list[-1])
            lp_list.append(l + "_" + ("%d" % j))
            #print(lp_list)
           # print('*********')
           # print(list[-1])
           # print(lp_list)

    print(list)
    print('---')
    print(lp_list)

    return (list,lp_list)




num = 0  # 初始上报量
decimal = 3  # 默认两位小数点
import random

def counter():
    global num, decimal
    num += 1.0
     #num += random(0,1)
    nu = format(num, '.{}f'.format(decimal))
    return nu




if __name__=='__main__':

    list, lp_list = devCount(count, lp_count)

    # for i in range(count):
    #     print(list[i])
    #     for j in range(lp_count):
    #         j = j + i*lp_count
    #         print(lp_list[j])
    for i in range(15):
        print(random.uniform(0, 0.01))



    # 下位机设备
  #  print(lp_device)
    #print(content['data']['device'])
