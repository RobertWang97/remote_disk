import os
import configparser
import codecs
import chardet

with open('config.ini', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(encoding)
# conf = configparser.ConfigParser()
# conf.read_file(codecs.open('config.ini', "r", "utf-8-sig"))

# program = conf.get('production', 'program')
# service_name = conf.get('production', 'service_name')
# # 执行命令
# return_code = os.system(f'{program}\Instsrv.exe {service_name} {program}\Srvany.exe')

# print("返回码:", return_code)
