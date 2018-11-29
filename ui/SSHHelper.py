import datetime
import os
import sys
import threading
import paramiko
import time
import glob

# hostname = '192.168.11.123'
hostname = '10.10.27.52'
username = 'cruiser'
password = 'aa'
port = 22
local_dir = 'logs'
remote_dir = 'logs'
file_counts = 0
downloaded_counts = 1


class SSHHelper:
    def __init__(self):
        self.gui = None
        self.file_counts = 0
        self.downloaded_counts = 1

    def func(self, i, j):
        cureentmb = round(i / (1024 * 1024), 0)
        totalmb = round(j / (1024 * 1024), 0)
        msg = '[{current}MB/{total}MB]'.format(current=cureentmb, total=totalmb)
        self.show_process(int((i / j) * 100), msg=msg)

    def DownLoadFile(self, sftp, LocalFile, RemoteFile):  # 下载当个文件
        file_handler = open(LocalFile, 'wb')

        msg = '[{current}/{totals}]'.format(current=self.downloaded_counts, totals=self.file_counts)
        msg2 = '{filename}{percent}'.format(filename=file_handler.name, percent=msg)
        print(msg2)
        # self.outputlog(msg2)
        self.gui.update_progress_bar2(
            int(float(self.downloaded_counts) / float(self.file_counts) * 100),
            msg)
        sftp.get(RemoteFile, LocalFile, callback=self.func)  # 下载目录中文件
        file_handler.close()
        return True

    def download_file_tree(self, sftp, LocalDir, RemoteDir):  # 下载整个目录下的文件
        if not os.path.exists(LocalDir):
            os.makedirs(LocalDir)

        list_dir = sftp.listdir_attr(RemoteDir)
        list_dir.sort(key=lambda e: e.st_mtime, reverse=True)
        for fileAttr in list_dir:
            file = fileAttr.filename
            mtime = fileAttr.st_mtime
            Local = os.path.join(LocalDir, file).replace('\\', '/')
            Remote = os.path.join(RemoteDir, file).replace('\\', '/')
            if file.find(".") == -1:  # 判断是否是文件
                if not os.path.exists(Local):
                    os.makedirs(Local)
                    print("转变下载文件目录：" + file)
                self.gui.update_log(
                    '当前下载目录{file}[{time}]'.format(file=file,
                                                  time=time.strftime("%Y-%m-%d %H:%M:%S",
                                                                     time.localtime(mtime))))
                self.download_file_tree(sftp, Local, Remote)
            else:  # 文件
                if self.DownLoadFile(sftp, Local, Remote):
                    self.downloaded_counts += 1

        return "complete"

    def check_files_numbers(self, sftp1, remote_dir1):
        counts = 0
        for file in sftp1.listdir(remote_dir1):
            remote = os.path.join(remote_dir1, file).replace('\\', '/')
            if file.find(".") == -1:  # 判断是否是文件
                counts = counts + self.check_files_numbers(sftp1, remote)
            else:  # 文件
                # print(file)
                counts = counts + 1
        return counts

    def show_process(self, percent=None, msg=None):
        self.gui.update_progress_bar(percent, msg)
        if percent >= 100:
            percent = 100

        hashes = '*' * int(percent / 100.0 * 50)
        spaces = ' ' * (50 - len(hashes))
        sys.stdout.write("\rrun: [%s] %d%%%s" % (hashes + spaces, percent, msg))
        sys.stdout.flush()

        if percent == 100:
            print("")

    def start(self):
        self.downloaded_counts = 1
        try:
            rosip = self.gui.ros_ip.get()
            file_name = self.gui.file_name.get()
            username = self.gui.user_name.get()
            password = self.gui.pass_word.get()
            if username == '':
                username = "cruiser"
            if password == '':
                password = "aa"

            print('rosip:{rosip},file_name:{file_name},username:{username},password:{password}'.
                  format(rosip=rosip, file_name=file_name, username=username, password=password))
            print("如果没有很快开始，请检查网络和ip")
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  # 现在
            local_dir = nowTime + '-' + file_name + '/logs'
            self.t = paramiko.Transport((rosip, port))
            self.t.banner_timeout = 30
            self.t.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(self.t)
            # stdin,stdout,stderr = sftp.exec_command('ls')
            # print(stdout.read())
            self.file_counts = self.check_files_numbers(sftp, remote_dir)
            print(self.file_counts)
            self.download_file_tree(sftp, local_dir, remote_dir)
            self.t.close()
            self.outputlog("♌♌♌❤❤❤正常结束了的❤❤❤♌♌♌")
        except Exception as err:
            print(err)
            self.outputlog("☂☂☂"+str(err)+"☂☂☂")
        self.gui.finish()

    def outputlog(self, log):
        self.gui.update_log(log)

    def set_gui(self, gui):
        self.gui = gui

    def stop(self):
        self.t.close()

