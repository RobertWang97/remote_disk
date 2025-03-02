import time
from datetime import datetime
import subprocess
import ctypes
import os
import configparser
import codecs
import glob
import re
import logging
from logging.handlers import TimedRotatingFileHandler
from schedule import every, repeat, run_pending
import shutil
import hashlib
import argparse

# 配置日志文件的路径和每天的大小限制
# 在这个例子中，日志文件application.log会在每天结束或文件大小达到10MB时自动分割，
# 并保留最近的3个备份。每个备份文件都会以日期和分钟命名，例如disk_copy_2023-01-01_00.log。
# 这样的设置可以有效管理日志文件的大小，避免单个文件过大。
parser = argparse.ArgumentParser()
parser.add_argument("-seconds", type=int, nargs="?", default=5, help="每次轮询需要多少秒?")
parser.add_argument("-s", default='D://', help="源文件夹路径，也就是映射u盘路径")
parser.add_argument("-t", default='C:/self-learning/tmp', help="目标文件夹主路径，也就是拷贝到的路径")
parser.add_argument("-dir", default='C:/self-learning/tmp', help="程序路径")
args = parser.parse_args()

# print("当前文件夹: " + args.dir)
# print("开始执行")
conf = configparser.ConfigParser()
conf.read_file(codecs.open(f'{args.dir}config.ini', "r", "utf-8-sig"))

program = conf.get('production', 'program')
log_file = f'{program}\\disk_copy.log'
max_bytes = 1024 * 1024 * 10  # 10MB
backup_count = 3

# 创建一个日志器并设置级别
logger = logging.getLogger('my_app')
logger.setLevel(logging.INFO)

# 创建TimedRotatingFileHandler
handler = TimedRotatingFileHandler(
    log_file, when='midnight', backupCount=backup_count, encoding='utf-8')
handler.setLevel(logging.DEBUG)

# 设置日志文件的最大大小
handler.suffix = '%Y-%m-%d_%M.log'
handler.rotation_size = max_bytes

# 创建日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 将handler添加到日志器
logger.addHandler(handler)


# 使用完毕后关闭日志器
# logger.removeHandler(handler)
# handler.close()
# logger.setLevel(logging.NOTSET)

def copy_folder(src, dst):
    '''
    拷贝文件夹数据
    :param src:
    :param dst:
    :return:
    '''
    shutil.copytree(src, dst)
    # for item in os.listdir(src):
    #     src_item = os.path.join(src, item)
    #     dst_item = os.path.join(dst, item)
    #     if os.path.isdir(src_item):
    #         copy_folder(src_item, dst_item)
    #     else:
    #         shutil.copy2(src_item, dst_item)


def dir_hash(directory):
    # 初始化MD5对象
    md5 = hashlib.md5()
    # 将文件夹中的文件名和文件内容都加入到MD5计算中
    for root, dirs, files in os.walk(directory):
        for file_name in sorted(files) + sorted(dirs):
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    md5.update(file.read())
            else:
                md5.update(file_name.encode())
    # 返回16进制的哈希值
    return md5.hexdigest()


def folder_found(main_path, md5):
    # 定义正则表达式
    regex_pattern = r"^.*" + md5 + "-done$"  # 匹配所有.txt文件

    # 使用glob获取所有文件，然后用正则表达式过滤
    files = glob.glob(os.path.join(main_path, "*"))
    matching_files = [f for f in files if re.match(regex_pattern, os.path.basename(f))]
    now = datetime.now().strftime("%Y.%m.%d.%H.%M.%S.%f")
    folder = now + "-" + md5
    fullpath = main_path + "/" + folder
    fullpath = os.path.normpath(fullpath)
    # 检查是否有匹配的文件
    if matching_files:
        return True, folder, fullpath
    else:
        # 如果目标文件夹存在，则删除它
        if os.path.exists(fullpath):
            shutil.rmtree(fullpath)
        return False, folder, fullpath


def done_folder(main_path, folder):
    new_filename = folder + '-done'
    for filename in os.listdir(main_path):
        if filename == folder:
            os.rename(os.path.join(main_path, filename), os.path.join(main_path, new_filename))
            return True, new_filename
    return False, new_filename


if __name__ == '__main__':
    @repeat(every(args.seconds).seconds)
    def job():
        service_name = "UUCopy"
        # 使用sc命令查询服务状态，并查找包含"RUNNING"的行来判断服务是否正在运行
        command = f'sc query "{service_name}" | findstr /i "RUNNING"'
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                logger.info(f"{service_name}服务未启动, 关闭进程")
                ctypes.windll.kernel32.ExitProcess(0)  # 这将结束当前Python进程。
                return
        except subprocess.CalledProcessError as e:
            logger.info(f"检测服务启动状态时出错: {e}")
            ctypes.windll.kernel32.ExitProcess(0)  # 这将结束当前Python进程。
            return

        try:
            source_path = args.s
            target_main_path = args.t
            if not os.path.exists(source_path): return  # 不存在就退出
            logger.info("发现u盘插入。")
            # print("发现u盘插入。")
            # copy_folder(source_path, 'destination_folder')
            folder_hash = dir_hash(source_path)
            logger.info("计算得当前u盘MD5码为" + folder_hash)
            # print("计算得当前u盘MD5码为" + folder_hash)
            flag, folder, target_path = folder_found(target_main_path, folder_hash)
            if flag:
                logger.info("找到已完成的拷贝，无需重新拷贝此u盘:" + target_path)
                # print("找到已完成的拷贝，无需重新拷贝此u盘:" + target_path)
                return
            # logger.info("创建新文件夹成功: " + target_path)
            logger.info("开始拷贝数据: " + target_path)
            # print("开始拷贝数据: " + target_path)
            shutil.copytree(source_path, target_path)
            logger.info("结束拷贝数据: " + target_path)
            # print("结束拷贝数据: " + target_path)
            flag2, new_path = done_folder(target_main_path, folder)
            if flag2:
                logger.info("结束后修改路径为: " + new_path)
                # print("结束后修改路径为: " + new_path)
            else:
                logger.error("结束后修改路径失败: " + new_path)
                # print("结束后修改路径失败: " + new_path)
        # logger.info("计算得当前u盘MD5码为" + folder_hash)

        except FileNotFoundError as e:
            logger.error(str(e) + " 文件没找到")
            # print(str(e) + " 文件没找到")
        except IOError as e1:
            # 没插u盘无需报错
            if e1.winerror != 21:
                logger.error(str(e1) + " 文件读取错误")
                # print(str(e1) + " 文件读取错误")
                ctypes.windll.kernel32.ExitProcess(0)  # 这将结束当前Python进程。
                return
        except PermissionError as e2:
            logger.error(str(e2) + " 权限错误")
            # print(str(e2) + " 权限错误")
            ctypes.windll.kernel32.ExitProcess(0)  # 这将结束当前Python进程。
            return
        except Exception as e3:
            logger.error(str(e3) + " 其他错误")
            # print(str(e3) + " 其他错误")
            ctypes.windll.kernel32.ExitProcess(0)  # 这将结束当前Python进程。
            return
        finally:
            pass

    while True:
        run_pending()
        # time.sleep(5)