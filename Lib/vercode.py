#encoding:utf-8
from random import choice, randint, randrange
import string
from PIL import Image, ImageDraw, ImageFont
import io
# 验证码图片文字的字符集
characters = string.ascii_letters + string.digits

def selectedCharacters(length):

    result = ''.join(choice(characters) for _ in range(length))
    return result


def getColor():

    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)

def main(size=(200, 100), characterNumber=6, bgcolor=(255, 255, 255)):
    # 创建空白图像和绘图对象
    imageTemp = Image.new('RGB', size, bgcolor)
    draw01 = ImageDraw.Draw(imageTemp)     

    # 生成并计算随机字符串的宽度和高度
    text = selectedCharacters(characterNumber)
    try:
        font = ImageFont.truetype('comic.ttf', 42)
    except:
        font= ImageFont.truetype('./Lib/comic.ttf',42);
    width, height = draw01.textsize(text, font)
    if width + 2 * characterNumber > size[0] or height > size[1]:
        print('尺寸不合法')
        return

    # 绘制随机字符串中的字符
    startX = 0
    widthEachCharater = width // characterNumber
    for i in range(characterNumber):
        startX += widthEachCharater + 1
        position = (startX, (size[1] - height) // 2 + randint(-10, 10))
        draw01.text(xy=position, text=text[i], font=font, fill=getColor())

    # 对像素位置进行微调，实现扭曲的效果
    imageFinal = Image.new('RGB', size, bgcolor)
    pixelsFinal = imageFinal.load()
    pixelsTemp = imageTemp.load()
    for y in range(size[1]):
        offset = randint(-1, 0)
        for x in range(size[0]):
            newx = x + offset
            if newx >= size[0]:
                newx = size[0] - 1
            elif newx < 0:
                newx = 0
            pixelsFinal[newx, y] = pixelsTemp[x, y]

    # 绘制随机颜色随机位置的干扰像素
    draw02 = ImageDraw.Draw(imageFinal)
    for i in range(int(size[0] * size[1] * 0.07)):
        draw02.point((randrange(0, size[0]), randrange(0, size[1])), fill=getColor())

    # 绘制8条随机干扰直线
    for i in range(8):
        start = (0, randrange(size[1]))
        end = (size[0], randrange(size[1]))
        draw02.line(start + end, fill = getColor(), width=1)

    # 绘制8条随机弧线
    for i in range(8):
        start = (-50, -50)
        end = (size[0] + 10, randint(0, size[1] + 10))
        draw02.arc(start + end, 0, 360, fill=getColor())

    # 保存并显示图片
    #imageFinal.save("result.jpg")
    #imageFinal.show()
    #img = Image.open(img_path, mode='r')
    imgByteArr = io.BytesIO()
    imageFinal.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr.getvalue()
    return (text,imgByteArr);

def make_vercode():
    return main((200, 100), 6, (255, 255, 255))

