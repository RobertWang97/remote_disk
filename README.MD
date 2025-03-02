# uucopy安装操作手册
## 第一部分 Python环境的安装和依赖包安装
### 1. 解压，将包中python-3.10.11-amd64.exe安装到主机 - 已经完成
### 2. 使用管理员权限打开powershell黑窗口, 输入python, 确认python环境是否安装成功 - 已经完成
### 3. 在2窗口中导航到程序文件夹目录D:\uucopy, 运行命令=>
```shell
pip3 install -r requirements.txt
```
## 第二部分 程序和目录环境搭建
### 1. 在工作机上共享u盘所在盘符，并且赋予相应权限
### 2. 在服务器上映射驱动器到#1的共享驱动，比如 I:\
### 3. 在服务器上设置一个用于拷贝数据的目标文件夹比如 D:\u_disk_files
### 4. 将运行程序文件夹拷贝的服务器，比如目录为D:\uucopy
### 5. 打开并修改config.ini文件, 样例=>
```shell
[production]
source=I:\
target=D:\u_disk_files
program=D:\uucopy
seconds=30
```
## 第三部分 创建windows服务UUCopy
### 1. 管理员权限的黑窗口D:\uucopy运行下面代码
```shell
python 1.new_service_uucopy.py
```
### 2. 确认uucopy服务已经建立之后，修改注册表(regedit),HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UUCopy
> 1. UUCopy下面创建String Value=Description, 值为Copy files from remote u disk.
> 2. UUCopy下面创建key=Parameters
> 3. 在Parameters下面创建String Value=Application， 在Application里边添加值为D:\uucopy\main.bat
### 3. 找到系统服务UUCopy, 修改登陆者属性为 honey\administrator并验证

## 第四部分 利用python执行程序修改bat文件
### 1. 管理员权限的黑窗口D:\uucopy运行下面代码
```shell
python 2.update_main_bat.py
```
### 2. 检查确认main.bat已经按照config.ini文件正确修改，类似=>
```shell
start python D:\uucopy\main.py -seconds 30 -s I:\ -t D:\u_disk_files -dir %~dp0
```
## 第五部分 运行服务，查看结果
### 1. 执行启动服务, 重启电脑
### 2. 查看disk_copy.log和D:\u_disk_files运行结果