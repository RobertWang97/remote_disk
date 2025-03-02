import os
import configparser
import codecs

conf = configparser.ConfigParser()
conf.read_file(codecs.open('config.ini', "r", "utf-8-sig"))

source = conf.get('production', 'source')
target = conf.get('production', 'target')
program = conf.get('production', 'program')
seconds = conf.get('production', 'seconds')

file_path = f'{program}\\main.bat'  # 文件路径

# 修改内容
content = f'python {program}\\main.py -seconds {seconds} -s {source} -t {target}'

# 写回文件
with open(file_path, 'w') as file:
    file.write(content)

print('done')