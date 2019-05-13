import os, shutil
import os.path


def mycopyfile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstfile))


rootdir = "D:/立白11"  # 指明被遍历的文件夹

list = os.listdir(rootdir)
# print(list)
for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    # for dirname in dirnames:  # 输出文件夹信息
    #     print("parent is:" + parent)
    #     print("dirname is" + dirname)
    current_name = ""
    current_image_index = 0
    current_image_offset = 1

    for filename in filenames:  # 输出文件信息
        # print("parent is:" + parent)
        file_name_part = filename[:6]
        if current_name != file_name_part:
            current_name = file_name_part
            current_image_index = current_image_index + 1
            current_image_offset = 1
        new_name = 'NO{current_image_index}#{current_image_offset}.jpg'.format(
            current_image_index=current_image_index,
            current_image_offset=current_image_offset)
        current_image_offset = current_image_offset + 1
        print("new_name is:" + new_name)
        print("filename is:" + filename)
        mycopyfile(os.path.join(parent, filename), os.path.join(parent, "hello/", new_name))
        print("the full name of the file is:" + os.path.join(parent, filename))  # 输出文件路径信息
