
# coding=gbk

from encryp.UI import GUI
from encryp.encrypdes import decode
from encryp.encrypdes import encode


def decode_fun(str_code):
    result = decode(str_code)
    print(result)
    return result


def encode_fun(str_code):
    result = encode(str_code)
    print(result)
    return result


def decrypt_java(str_code, **p):
    pass


if __name__ == '__main__':
    ui = GUI(encode_fun, decode_fun)
    ui.set_init_window()
    ui.start()

