import paramiko
import datetime
import os
import sys
import time

# hostname = '192.168.11.123'
hostname = '10.10.27.52'
username = 'cruiser'
password = 'aa'
port = 22
local_dir = 'logs'
remote_dir = 'logs'


def func(i, j):
    cureentmb = round(i / (1024 * 1024), 2)
    totalmb = round(j / (1024 * 1024), 2)
    # print('{current}MB/{total}MB'.format(current=cureentmb, total=totalmb))
    # print(int((i / j) * 100))
    show_process(int((i / j) * 100))


def DownLoadFile(sftp, LocalFile, RemoteFile):  # 下载当个文件
    file_handler = open(LocalFile, 'wb')
    print(file_handler)
    sftp.get(RemoteFile, LocalFile, callback=func)  # 下载目录中文件
    file_handler.close()
    return True


def DownLoadFileTree(sftp, LocalDir, RemoteDir):  # 下载整个目录下的文件
    if not os.path.exists(LocalDir):
        os.makedirs(LocalDir)
    for file in sftp.listdir(RemoteDir):
        Local = os.path.join(LocalDir, file).replace('\\', '/')
        Remote = os.path.join(RemoteDir, file).replace('\\', '/')
        if file.find(".") == -1:  # 判断是否是文件
            if not os.path.exists(Local):
                os.makedirs(Local)
                print("转变下载文件目录：" + file)
            DownLoadFileTree(sftp, Local, Remote)
        else:  # 文件
            DownLoadFile(sftp, Local, Remote)
    return "complete"


def show_process(percent=None):
    width = 60
    if percent >= 100:
        percent = 100

    # show_str = ('[%%-%ds]' % width) % (int(width * percent / 100) * "*")  # 字符串拼接的嵌套使用
    # # print('\r%s %d%%' % (show_str, percent), end='')
    # sys.stdout.write("\r%s %d%%" % (show_str, percent))
    # sys.stdout.flush()

    hashes = '*' * int(percent/100.0 * 50)
    spaces = ' ' * (50 - len(hashes))
    sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, percent))
    sys.stdout.flush()

    if percent == 100:
        print("")


if __name__ == '__main__':
    try:
        print("wywbnjysxx")
        print("===========四叶草系列工具三==============")
        m = input("局域网模式/M|网线模式/L:")
        if m == 'm' or m == 'M':
            hostname = input("RosIp:")
        elif m == 'l' or m == 'L':
            hostname = '192.168.11.123'
            # hostname = '10.10.27.144'

        userStr = input("用户名，默认直接回车:")
        if userStr != "":
            username = userStr

        passStr = input("密码，默认直接回车:")
        if passStr != "":
            password = passStr
        message = input("操作备注 默认直接回车:")
        print("如果没有很快开始，请检查网络和ip")
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  # 现在
        local_dir = nowTime + '-' + message + '/logs'
        t = paramiko.Transport((hostname, port))
        t.banner_timeout = 30
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)

        # sftp.get(os.path.join(remote_dir, f), os.path.join(local_dir, f))
        DownLoadFileTree(sftp, local_dir, remote_dir)
        t.close()
        input("请按回车键退出，拜拜！！！")
    except Exception as err:
        print(err)
        input("异常请按回车键退出，拜拜！！！")
