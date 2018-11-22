import os
from pypinyin import pinyin, lazy_pinyin
import pypinyin


class RenameHelper:

    def __init__(self):
        pass

    def start(self, path):
        self.show_tips()
        self.do_walk(path)
        pass

    def do_walk(self, path):
        for (root, dirs, files) in os.walk(path, topdown=True):
            for name in files:
                if ".apk" in name.lower():
                    names = os.path.splitext(name)
                    new_name = name.replace(names[0], "".join(lazy_pinyin(names[0])))
                    self.rename(os.path.join(root, name), os.path.join(root, new_name))
        print("已经改完所有的中文名字了，你真棒！！！")
        pass

    def rename(self, old, new):
        print("正在改名{}---->{}".format(old, new))
        os.rename(old, new)
        pass

    def show_tips(self):
        print("生气的红色四叶草提醒你:早点休息，别熬夜！！！")
        print("生气的红色四叶草提醒你:早点休息，别熬夜！！！")
        print("生气的红色四叶草提醒你:早点休息，别熬夜！！！")
        print("生气的红色四叶草提醒你:早点休息，别熬夜！！！")


helper = RenameHelper()
helper.start(".")
input("请按回车键退出，拜拜！！！")
