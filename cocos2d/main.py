import cocos
from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer
from cocos.layer import *
from cocos.actions import *

import pyglet


class HelloWorld(cocos.layer.Layer):
    def __init__(self):
        super(HelloWorld, self).__init__()

        label = cocos.text.Label('Hello, World!',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')

        label.position = 320, 240
        self.add(label)
        # 只支持ogg格式
        audio = Sound("bounce.ogg")
        # audio.play(-1)
        scroll_layer = ScrollableLayer()
        map1 = cocos.tiles.load("110.tmx")['1']
        scroll_layer.add(map1)
        # colorLayer = ColorLayer(64, 200, 64, 255)
        # colorLayer.scale = 0.2
        # self.add(colorLayer)
        # colorLayer.do(Rotate(360, 3))
        # print(colorLayer.anchor)
        self.add(scroll_layer)


# cocos.director.director.init()
# mixer.init()
# helloLayer = HelloWorld()
# main_scene = cocos.scene.Scene(helloLayer)
# cocos.director.director.run(main_scene)


def main():
    global keyboard, scroller
    from cocos.director import director
    director.init(width=600, height=300, autoscale=False, resizable=True)
    # 一定要用这个对象加载
    scroller = cocos.layer.ScrollingManager()
    map_root = cocos.tiles.load('110.tmx')
    scroller.add(map_root['1'])
    # 读取对象层的属性
    for o in map_root['obj'].objects:
        print(o.properties)
    main_scene = cocos.scene.Scene(scroller)

    director.run(main_scene)


if __name__ == '__main__':
    main()
