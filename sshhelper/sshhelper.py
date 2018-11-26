import datetime
import os
import sys

import paramiko

# hostname = '192.168.11.123'
hostname = '10.10.27.52'
username = 'cruiser'
password = 'aa'
port = 22
local_dir = 'logs'
remote_dir = 'logs'
file_counts = 0
downloaded_counts = 1


def func(i, j):
    cureentmb = round(i / (1024 * 1024), 0)
    totalmb = round(j / (1024 * 1024), 0)
    msg = '[{current}MB/{total}MB]'.format(current=cureentmb, total=totalmb)
    show_process(int((i / j) * 100), msg=msg)


def DownLoadFile(sftp, LocalFile, RemoteFile):  # 下载当个文件
    global downloaded_counts
    global file_counts
    file_handler = open(LocalFile, 'wb')
    msg = '{filename}[{current}/{totals}]'.format(filename=file_handler.name,
                                                  current=downloaded_counts,
                                                  totals=file_counts)
    print(msg)
    sftp.get(RemoteFile, LocalFile, callback=func)  # 下载目录中文件
    file_handler.close()
    return True


def download_file_tree(sftp, LocalDir, RemoteDir):  # 下载整个目录下的文件
    if not os.path.exists(LocalDir):
        os.makedirs(LocalDir)
    for file in sftp.listdir(RemoteDir):
        Local = os.path.join(LocalDir, file).replace('\\', '/')
        Remote = os.path.join(RemoteDir, file).replace('\\', '/')
        if file.find(".") == -1:  # 判断是否是文件
            if not os.path.exists(Local):
                os.makedirs(Local)
                print("转变下载文件目录：" + file)
            download_file_tree(sftp, Local, Remote)
        else:  # 文件
            if DownLoadFile(sftp, Local, Remote):
                global downloaded_counts
                downloaded_counts += 1

    return "complete"


def check_files_numbers(sftp1, remote_dir1):
    counts = 0
    for file in sftp1.listdir(remote_dir1):
        remote = os.path.join(remote_dir1, file).replace('\\', '/')
        if file.find(".") == -1:  # 判断是否是文件
            counts = counts + check_files_numbers(sftp1, remote)
        else:  # 文件
            print(file)
            counts = counts + 1
    return counts


def show_process(percent=None, msg=None):
    if percent >= 100:
        percent = 100

    hashes = '*' * int(percent / 100.0 * 50)
    spaces = ' ' * (50 - len(hashes))
    sys.stdout.write("\rrun: [%s] %d%%%s" % (hashes + spaces, percent, msg))
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
            # hostname = '10.10.27.52'

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
        file_counts = check_files_numbers(sftp, remote_dir)
        print(file_counts)
        download_file_tree(sftp, local_dir, remote_dir)
        t.close()
        input_str = input("请按回车键退出，拜拜！！！")
        print(input_str)
    except Exception as err:
        print(err)
        input_str = input("异常请按回车键退出，拜拜！！！")
        print(input_str)
