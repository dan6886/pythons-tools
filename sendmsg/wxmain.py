from wxpy import *
import re
import time
import threading

from sendmsg.loop_timer import LoopTimer

bot = Bot()
bot.enable_puid()
myfriends = bot.friends().search('天使座')[0]
# myfriends.send("你好啊")
SourceSavePath = './RecieveFile/'
messages = ()
all_messages = {}
nick_name_csh = 'a～💗小屁民陈哒哒'
remark_name_csh = '天使座'
special_user = (nick_name_csh, remark_name_csh, '魔鬼座', '赵文强', '罗沛鹏')


def clear_old():
    # 循环遍历300秒的消息删除不保存
    for key in list(all_messages.keys()):
        message_old = all_messages[key]
        if get_delta_time(str(message_old.create_time)) > 300:
            del all_messages[key]
            print("delete over time:" + str(message_old.create_time), message_old)
    print("there is left messages:" + str(len(all_messages)))


def prn_obj(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


# 根据不同的联系人，生成不同的回复方式
def build_name(msg):
    preSentence = ''
    if msg.sender.name in special_user or msg.sender.nick_name in special_user:
        create_time = str(msg.create_time)

        preSentence = '报告猪立力，纠结的她{delay}秒后又撤回了一则消息，这里发给你了，我们假装不知道。\n发送时间:{create_time}\n内容如下:'.format(
            delay=get_delta_time(create_time), create_time=create_time)
        pass
    else:
        preSentence = '{name}|{nick_name}--->测回一条消息:'.format(name=msg.sender.name,
                                                             nick_name=msg.sender.nick_name)
    return preSentence


def get_delta_time(last_time):
    """
    传入时间和当前时间的差值，单位 秒
    :param last_time: 2019-07-02 20:35:02.600
    :return:
    """
    print(time.time())
    timeArray = time.strptime(last_time.split('.')[0], "%Y-%m-%d %H:%M:%S")
    last_time_stamp = time.mktime(timeArray)
    return int(time.time() - last_time_stamp)


@bot.register()
def print_others(msg):
    print(msg)
    # print(msg.type)
    # print(msg.sender)
    # print(msg.chat)
    # prn_obj(msg)
    msg_id = msg.raw['MsgId']
    msg_status = msg.raw['Status']
    # 消息存入字典里面
    all_messages.update({msg_id: msg})
    user_name = msg.sender.name
    # 4代表撤回消息了
    if msg_status == 4:
        # 获取到测回消息的id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg.raw['Content']).group(1)
        # 获取到被撤回的消息对象
        cancelled_message = all_messages.get(old_msg_id)
        # 只是根据不同的联系人生成不同的回复话语，tips可以写死
        tips = build_name(cancelled_message)
        # 如果是文本则直接转发
        if cancelled_message.type == TEXT:
            cancelled_message.forward(bot.file_helper, prefix=tips,
                                      raise_for_unsupported=True)
            pass
        # 如果是图片和视频，则直接转发
        elif cancelled_message.type == PICTURE or cancelled_message.type == VIDEO:
            cancelled_message.forward(bot.file_helper, prefix=tips,
                                      raise_for_unsupported=True)
            final_path = '{id}(+){user_name}(+){file_name}'.format(id=msg_id,
                                                                   user_name=user_name,
                                                                   file_name=cancelled_message.file_name)

            save_path = SourceSavePath + final_path
            cancelled_message.get_file(save_path=save_path)
            pass
        else:
            pass

        print(old_msg_id)
        print(cancelled_message.raw['Text'])
        pass

    print('处理完毕！！！')


if __name__ == "__main__":
    print("开始了")
    timer = LoopTimer(300, clear_old)
    timer.start()

embed()
