# *_*coding:utf-8 *_*
__author__ = "Test Lu"
import os,codecs
import configparser
prodir = os.path.dirname(os.path.abspath(__file__))
conf_prodir = os.path.join(prodir,'conf.ini')
class Read_conf():
     def __init__(self):
         with open(conf_prodir) as fd:
             data = fd.read()

             if data[:3] ==codecs.BOM_UTF8:
                 data = data[3:]
                 file = codecs.open(conf_prodir, 'w')
                 file.write(data)
                 file.close()
         self.cf = configparser.ConfigParser()
         self.cf.read(conf_prodir)
     def  get_mqtt(self,name):
         value = self.cf.get("MQTTClinet", name)
         return value

     def get_data(self,name):
         return self.cf.get("ProtocolData", name)

#
# if __name__=='__main__':
#     w = Read_conf()
#     print(w.get_http('baseurl'))
