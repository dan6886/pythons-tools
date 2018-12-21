import jpype
import numpy


def encode(str_code):
    return decrypt(str_code, mode='encode', str=str_code)


def decode(str_code):
    return decrypt(str_code, mode='decode', str=str_code)


def decrypt(str_code, **p):
    ext_classpath = './test1_main.jar'
    jvmArg = '-Djava.class.path=' + ext_classpath
    jvmPath = jpype.getDefaultJVMPath()  # 获得系统的jvm路径
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)  # 启动虚拟机

    TA = jpype.JClass("EncrypDES")  # 这种用法可以简化后面的书写
    result = ''
    if p['mode'] == 'encode':
        result = TA.encode(p['str'])

    if p['mode'] == 'decode':
        result = TA.decode(p['str'])
        # print("sddddd")
    # jpype.shutdownJVM()  # 关闭jvm
    return result
