import subprocess
import ctypes
import time
service_name = "UUCopy"
# 使用sc命令查询服务状态，并查找包含"RUNNING"的行来判断服务是否正在运行
command = f'sc query "{service_name}" | findstr /i "RUNNING"'
try:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{service_name}服务已启动, 尝试关闭")
        time.sleep(10)
        ctypes.windll.kernel32.ExitProcess(0)  # 这将结束当前Python进程。
    else:

        print(f"{service_name}服务未启动")
except subprocess.CalledProcessError as e:
    print(f"检测服务启动状态时出错: {e}")