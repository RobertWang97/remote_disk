# uucopy安装操作手册
### 1. 解压，将包中python-3.10.11-amd64.exe安装到主机 - 已经完成
### 2. 使用管理员权限打开powershell黑窗口, 输入python, 确认python环境是否安装成功 - 已经完成
### 3. 在2窗口中导航到程序文件夹目录, 运行命令pip3 install -r requirements.txt安装必要包 - 已经完成
### 4. 在工作机上共享u盘所在盘符，并且赋予相应权限 - 已经完成
### 5. 在服务器上映射驱动器到4的共享驱动，比如 I:/ - 已经完成
### 6. 在服务器上设置一个用于拷贝数据的目标文件夹比如 D:/u_disk_files - 已经完成
### 7. 将运行程序文件夹拷贝的服务器，比如目录为D:/uucopy
### 8. 黑窗口尝试运行 D:\uucopy\Instsrv.exe UUCopy D:\uucopy\Srvany.exe 
### ~~7. 尝试在3的黑窗口中，运行命令python main.py -seconds 30 -s I:/ -t D:/u_disk_files，其中参数seconds是轮询时间，单位为秒~~
### 7. 编辑修改main.bat文件，python D:/uucopy/main.py -seconds 30 -s I:/ -t D:/u_disk_files，其中参数seconds是轮询时间，单位为秒
### ~~8. sc.exe create UUCopy binpath= C:\self-learning\remote_disk\main.bat displayname= 自动拷贝远程U盘中的文件~~
### ~~8. 编辑修改system_service.py文件，找到os.system(xxxxxxxxx)一行，修改为os.system('D:/uucopy/main.bat')~~
### ~~9. 执行安装服务，在2黑窗口中运行python D:/uucopy/system_service.py install~~
### 8. 修改注册表(regedit),HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UUCopy
###         下面创建key=Parameters, 在Parameters下面创建String Value=Application
###         在Application里边添加值为D:\uucopy\main.bat
### 9. 修改main.py中一行log_file = 'C:/uucopy/disk_copy.log'
### 10. 找到系统服务UUCopy, 修改登陆属性为  honey\administrator并验证
### 11. 执行启动服务
### 12. 查看disk_copy.log和D:/u_disk_files运行结果