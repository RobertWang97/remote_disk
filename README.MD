# 安装操作手册
### 1. 解压，将包中python-3.10.11-amd64.exe安装到主机
### 2. 随便打开cmd黑窗口, 输入python, 确认python环境是否安装成功
### 3. 在2黑窗口中导航到程序文件夹目录, 运行命令pip3 install -r requirements.txt安装必要包
### 4. 在工作机上共享u盘所在盘符，并且赋予相应权限
### 5. 在服务器上映射驱动器到4的共享驱动，比如 I:/
### 6. 在服务器上设置一个用于拷贝数据的目标文件夹比如 D:/u_disk_files
### 7. 尝试在3的黑窗口中，运行命令python main.py -seconds 30 -s I:/ -t D:/u_disk_files，其中参数seconds是轮询时间，单位为秒
### 8. 查看disk_copy.log和D:/u_disk_files运行结果