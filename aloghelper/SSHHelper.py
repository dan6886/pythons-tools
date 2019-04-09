# -*- coding:utf-8 -*-
import subprocess
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
        self.p = None
        self.isStop = False;

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
        self.isStop = False
        try:

            android_ip = self.gui.android_ip.get()
            file_name = self.gui.file_name.get()
            mode = self.gui.mode.get()
            pull_mode = self.gui.pull_mode.get()
            log_time = self.gui.log_time.get()
            dir_child = self.gui.dir_child.get()
            # dir_child = dir_child.encode('utf-8')
            if mode == 2:
                self.connect_ip(android_ip)
            else:
                pass

            if dir_child != '':
                self.mkdir(dir_child)
                dir_child = dir_child + "/"
            # else:
            #     dir_child = None
            print(
                'android_ip:{android_ip},file_name:{file_name},log_time:{log_time},dir_child:{dir_child},pull_mode:{pull_mode}'.
                    format(android_ip=android_ip, file_name=file_name, log_time=log_time,
                           dir_child=dir_child,
                           pull_mode=pull_mode))

            origin_file_name = self.assemble_log(log_time)
            self.pull_file(dir_child, origin_file_name, file_name, pull_mode)
            print("如果没有很快开始，请检查网络和ip")
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')  # 现在
            local_dir = nowTime + '-' + file_name + '/logs'

            self.outputlog("♌♌♌❤❤❤正常结束了的❤❤❤♌♌♌")
        except Exception as err:
            print(err)
            self.outputlog("☂☂☂" + str(err) + "☂☂☂")
        self.gui.finish()

    def outputlog(self, log):
        self.gui.update_log(log)

    def set_gui(self, gui):
        self.gui = gui

    def stop(self):
        self.isStop = True
        print("调用了停止")
        self.p.kill()

    def open(self):
        self.isStop = True
        print("调用了停止")
        cmd = 'start .'
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, universal_newlines=True,
                                  shell=True)
        result_lines = self.p.communicate()
        self.outputlog("打开完成")
        print("打开完成:")

    def clearAll(self):
        print("调用了清除")
        cmd = 'adb shell rm -rf /sdcard/log/*'
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, universal_newlines=True,
                                  shell=True)
        result_lines = self.p.communicate()
        # result_lines = self.p.stdout.readlines()
        self.outputlog("清除完成")
        print("清除完成:")

    def connect_ip(self, ip):
        cmd = 'adb connect {ip}'.format(ip=ip)
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, universal_newlines=True,
                                  shell=True)
        result_lines = self.p.communicate()
        # result_lines = self.p.stdout.readlines()
        self.outputlog("".join(result_lines))
        print("连接完成:")

    def assemble_log(self, log_time):
        cmd = 'adb shell todo getlog {time}'.format(time=log_time)
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True, shell=True)
        p.wait()
        result_lines = p.stdout.readlines()
        print("生成日志完成:" + "".join(result_lines))
        file_name = ''
        for i, val in enumerate(result_lines):
            if val.startswith('/sdcard/log/Alog'):
                file_name = val.split("/")[-1].strip("\n")
                print(file_name)
                self.outputlog('生成成功--->' + file_name)
                return file_name
        self.outputlog('异常')
        return None

    def pull_file(self, dir_child, old_name, append_name, pull_mode):
        if pull_mode == 2:
            self.outputlog('先准备拉取全部日志')
            cmd_all = 'adb pull /sdcard/log/ ./{dir_child}'.format(
                old_name=old_name,
                dir_child=dir_child,
                append_name=append_name)
            self.p = subprocess.Popen(cmd_all, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, universal_newlines=True,
                                      shell=True)
            self.p.communicate()
            print("拉取日志完成")
            self.outputlog('拉取全部日志完成')

        self.outputlog(
            '准备拉取本次生成的日志--->{old_name}并且改为新名称--->{append_name}{old_name}'.format(old_name=old_name,
                                                                                 append_name=append_name))
        cmd = 'adb pull /sdcard/log/{old_name} ./{dir_child}{append_name}{old_name}'.format(
            old_name=old_name,
            dir_child=dir_child,
            append_name=append_name)
        self.p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  universal_newlines=True, shell=True)
        result_lines = self.p.communicate()
        print("拉取单个日志完成")

    def mkdir(self, path):
        # 引入模块
        import os

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            os.makedirs(path)
            print(path + ' 创建成功')
            self.outputlog(path + '---->创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            self.outputlog(path + '---->目录已存在')
            return False
