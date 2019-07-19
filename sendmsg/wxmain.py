import os
import re
import time

from wxpy import *

from sendmsg.loop_timer import LoopTimer
from wxpy import WeChatLoggingHandler

bot = Bot(cache_path=True)
mp = bot.enable_puid(path='wxpy_puid.pkl')

SourceSavePath = './RecieveFile/'
messages = ()
all_messages = {}
nick_name_csh = 'a～💗小屁民陈哒哒'
remark_name_csh = '天使座'
special_user = [nick_name_csh, remark_name_csh, '魔鬼座', '罗沛鹏']

debug = True


def clear_old():
    # 循环遍历300秒的消息删除不保存
    for key in list(all_messages.keys()):
        message_old = all_messages[key]
        if get_delta_time(str(message_old.create_time)) > 300:
            del all_messages[key]
            print("delete over time:" + str(message_old.create_time), message_old)
    print_debug("there is left messages:" + str(len(all_messages)))
    delete_expired_file()


def print_debug(msg):
    if debug:
        print('{time}|{msg}'.format(time=get_current_time(), msg=msg))


def add_pre_time(msg):
    return '{time}|{msg}'.format(time=get_current_time(), msg=msg)


def prn_obj(obj):
    print_debug('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


def check_special(msg):
    if not isinstance(msg.chat, Friend):
        return None
    pre_sentence = None
    if msg.sender.name in special_user or msg.sender.nick_name in special_user:
        create_time = str(msg.create_time)

        pre_sentence = '报告猪立力，纠结的她{delay}秒后又撤回了一则消息，这里发给你了，我们假装不知道。\n发送时间:{create_time}\n内容如下:'.format(
            delay=get_delta_time(create_time), create_time=create_time)
    return pre_sentence


# 根据不同的联系人，生成不同的回复方式
def build_name(msg):
    pre_sentence = ''
    name = ""
    from_chat = ""
    if isinstance(msg.chat, Group):
        name = msg.member.name
        from_chat = msg.chat.name
    elif isinstance(msg.chat, Friend):
        name = msg.sender.name
        from_chat = msg.sender.name
    special = check_special(msg=msg)

    if special is not None:
        pre_sentence = special
    else:
        pre_sentence = '{name}|{nick_name}--->测回一条消息:'.format(name=name, nick_name=from_chat)
    return pre_sentence


def get_delta_time(last_time):
    """
    传入时间和当前时间的差值，单位 秒
    :param last_time: 2019-07-02 20:35:02.600
    :return:
    """
    timeArray = time.strptime(last_time.split('.')[0], "%Y-%m-%d %H:%M:%S")
    last_time_stamp = time.mktime(timeArray)
    return int(time.time() - last_time_stamp)


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@bot.register()
def print_others(msg):
    print(add_pre_time(msg))
    print_debug(msg.type)
    print_debug(msg.sender)
    print_debug(msg.chat)
    prn_obj(msg)
    msg_id = msg.raw['MsgId']
    msg_status = msg.raw['Status']
    msg_type = msg.raw['MsgType']
    # 消息存入字典里面
    all_messages.update({msg_id: msg})
    user_name = msg.sender.name
    # 4代表撤Note 10002代表测回消息了,10000代表邀请入群
    if msg_status == 4 and msg_type == 10002:
        # 获取到测回消息的id
        msg_ids_find = re.search("\<msgid\>(.*?)\<\/msgid\>", msg.raw['Content'])
        if msg_ids_find is None:
            bot.file_helper.send(
                '你自己撤回了一条消息(为保证隐私我就不来这里显示了)\n时间:{time}'.format(time=get_current_time()))
            print('此条消息处理完毕！！！')
            return
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg.raw['Content']).group(1)
        # 获取到被撤回的消息对象
        cancelled_message = all_messages.get(old_msg_id)
        # 只是根据不同的联系人生成不同的回复话语，tips可以写死
        tips = build_name(cancelled_message)
        # 如果是文本
        if cancelled_message.type == TEXT:
            prefix = '{tips}\n{time}\n{text}'.format(tips=tips,
                                                     time=get_time_tips(cancelled_message),
                                                     text=cancelled_message.text)
            resend_message(cancelled_message.type, old_msg_id, prefix=prefix)
            pass
        # 如果是图片和视频
        elif cancelled_message.type == PICTURE or cancelled_message.type == VIDEO:
            prefix = '{tips}\n{time}'.format(tips=tips,
                                             time=get_time_tips(cancelled_message))
            resend_message(cancelled_message.type, old_msg_id, prefix=prefix)
            pass
        else:
            pass

        print(old_msg_id)
        print(cancelled_message.raw['Text'])
        pass
    else:
        # 正常消息
        if msg.type == PICTURE or msg.type == VIDEO:
            final_path = '{id}-{user_name}-{file_name}'.format(id=msg_id, user_name=user_name,
                                                               file_name=msg.file_name)
            save_path = SourceSavePath + final_path
            msg.get_file(save_path=save_path)

    print('此条消息处理完毕！！！')


def get_time_tips(msg):
    return '接收时间:{r}|撤回时间:{rc}'.format(r=msg.create_time, rc=get_current_time())


def delete_expired_file():
    format_date = get_format_date()
    g = os.walk(SourceSavePath)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            # 去除后缀
            pre_name = os.path.splitext(file_name)[0]
            # 分隔出 -
            file_names = pre_name.split('-')
            # 获取时间
            file_date = file_names[-2] + file_names[-1]
            # 只删除时间超过5分钟的
            if int(format_date) - int(file_date) > 60 * 5:
                os.remove(os.path.join(path, file_name))
                print("delete expired file" + file_name)


def get_format_date():
    date = time.strftime("%Y%m%d%H%M%S", time.localtime())[2:]
    return date


def find_cached_file(msg_id):
    g = os.walk(SourceSavePath)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            if msg_id in file_name:
                return os.path.join(path, file_name)
    return None


def resend_message(msg_type, msg_id, prefix):
    local_file_path = find_cached_file(msg_id=msg_id)
    if local_file_path is None and msg_type != TEXT:
        print("没有找到对应的缓存文件")
        return
    bot.file_helper.send(prefix)
    if msg_type == PICTURE:
        bot.file_helper.send_image(local_file_path)
        pass
    elif msg_type == VIDEO:
        bot.file_helper.send_video(local_file_path)
        pass
    elif msg_type == TEXT:
        # bot.file_helper.send(prefix)
        pass
    else:
        pass


def find_target():
    path = "user.txt"
    users = []
    if os.path.exists(path=path):
        f = open("user.txt", "r", encoding='UTF-8')
        users = f.readlines()
        f.close()
    for user in users:
        user = user.strip("\n")
        special_user.append(user)


def create_cached_dir():
    path = SourceSavePath
    if os.path.exists(path=path):
        print("缓存文件夹存在")
    else:
        os.mkdir(path=path)
        print("缓存文件夹不存在,创建一个缓存文件夹")


if __name__ == "__main__":
    print("有人撤回我会在微信的文件助手告诉你的")
    print("已经成功启动...")
    create_cached_dir()
    # print("同级目录下面创建user.txt文件里面逐行写上昵称")
    find_target()
    timer = LoopTimer(400, clear_old)
    timer.start()

embed()
