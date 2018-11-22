import os
import subprocess
import sys
import re


class Installer(object):
    i = 0  # 当前的处理进度
    max_steps = 50  # 总共需要处理的次数
    max_arrow = 50  # 进度条的长度
    infoDone = 'done'
    fail_count = 0

    def __init__(self, path):
        self.path = path
        self.apk_list = list()
        self.i = 0
        pass

    def start(self):
        self.printTips()
        self.find_in_dir(self.path)
        self.handle_list()
        pass

    def printTips(self):
        print("四叶草向您问好，很高兴为你服务")
        print("四叶草提示您:文件路径不要包含中文字符(〃'▽'〃)")
        print("四叶草提示您:请保证设备已经连接(╯﹏╰)b")
        print("四叶草提示您:早睡早起身体棒！！！［(－－)］zzz")
        print("四叶草提示您:晚上喝咖啡睡不着！！！［(－－)］zzz")

    def is_apk_file(self, path):
        path_tuple = os.path.splitext(path)
        if "apk" in path_tuple[1].lower():
            return True
        return False

    def find_in_dir(self, path):
        # print("当前处理Path:" + path)
        dir_list = os.listdir(path)
        for n in dir_list:
            # print("当前文件:" + n)
            join_path = os.path.join(path, n)
            abs_path = os.path.abspath(join_path)
            isfile = os.path.isfile(abs_path)
            # print(isfile)
            if (isfile):
                # 文件
                is_apk = self.is_apk_file(abs_path)
                if (is_apk):
                    self.apk_list.append(abs_path)
                    pass
                # 是apk加入列表
                else:
                    pass
                    # 其他文件，不管
            else:
                # 文件夹
                # print("查找文件夹:" + n)
                self.find_in_dir(abs_path)
                pass
        pass

    def do_install(self, path, msg):
        # tmp = os.popen('adb install -r ' + path).readlines()
        is_success = False
        p = subprocess.Popen('adb install -r ' + path, stdout=subprocess.PIPE)
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                # print('Subprogram output: [{}]'.format(line))
                # str = line[line.index('['):line.index(']')]
                pattern = re.compile(r"[0-9]*%")
                matches = re.search(pattern, str(line))
                if matches:
                    progress = matches.group()[:-1]
                    # print(progress)
                    self.show_process(int(progress))
                else:
                    print(line)
                    if "Failure" in str(line):
                        self.fail_count += 1
                        is_success = False
                        pass
                    else:
                        is_success = True
        if p.returncode == 0 and is_success:
            print('恭喜你' + msg + "安装执行完毕")
        else:
            print('安装失败了！！！')
        pass

    def show_process(self, percent=None):
        width = 60
        if percent >= 100:
            percent = 100

        show_str = ('[%%-%ds]' % width) % (int(width * percent / 100) * "*")  # 字符串拼接的嵌套使用
        print('\r%s %d%%' % (show_str, percent), end='')
        if percent == 100:
            print("")

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0

    def handle_list(self):
        if len(self.apk_list) == 0:
            print("当前目录没有可用文件，你简直棒极了！！！")
            return

        count = 0
        for p in self.apk_list:
            count += 1
            msg = "第{}/{}个文件".format(count, len(self.apk_list))
            print("正在执行安装" + msg + "  " + p)
            self.do_install(p, msg)
        if (self.fail_count == 0):
            print("所有文件安装成功，你简直棒极了！！！")
        else:
            print("貌似有apk 安装失败了哦，请检查一下哦。数量：" + str(self.fail_count))

    # installer = Installer("C:/Users/ubt/PycharmProjects/untitled/build")


installer = Installer(".")
installer.start()
input("请按回车键退出，拜拜！！！")
