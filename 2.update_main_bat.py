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

lines = ["@echo off\n",
         "wmic process where \"name='python.exe'\" get name | find \"python.exe\" >nul\n",
         "if errorlevel 1 (\n",
         f"    start python {program}\\main.py -seconds {seconds} -s {source} -t {target} -dir %~dp0\n",
         ") else (\n",
         "    echo python is already running.\n",
         ")"]
# 修改内容
# content = f'python {program}\\main.py -seconds {seconds} -s {source} -t {target}'

# 写回文件
with open(file_path, 'w') as file:
    file.writelines(lines)

print('done')