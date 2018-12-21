可以这样
–icon=图标路径
-F 打包成一个exe文件
-w 使用窗口，无控制台
-c 使用控制台，无窗口
-D 创建一个目录，里面包含exe以及其他一些依赖性文件

pyinstaller -F main.py -i icon/favicon.ico

pyinstaller -F rename/rename.py -i icon/favicon-red.ico

pyinstaller -F sshhelper/sshhelper.py -i icon/blue.ico

pyinstaller -F ui/start.py -i icon/favicon-red.ico

pyinstaller -F encryp/start.py -w

如果遇到图标打包显示不正确，请修改exe文件名则会刷新正确