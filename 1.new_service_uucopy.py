import os
import configparser
import codecs
conf = configparser.ConfigParser()
conf.read_file(codecs.open('config.ini', "r", "utf-8-sig"))

program = conf.get('production', 'program')
# 执行命令
return_code = os.system(f'{program}\Instsrv.exe UUCopy {program}\Srvany.exe')

# print("返回码:", return_code)