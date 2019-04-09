# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw
import time

# 字体颜色
color = "#000000"

"""
生成分享图片的方法
"""
def createShareImg(avatarImg, qrcodeImg, goodsImg, nickname, countWord,imgWidth,headImgSize,headImgPosition,qrcodeImgSize,qrcodeImgPosition,goodsImgSize,goodsImgPosition,nameSize,nameCoordinate,goodsSize,goodsCoordinate,backgroundImg):
    startTime = time.time()
    # 加载背景图片
    background = Image.open(backgroundImg)
    # 加载头像图片
    avatar = Image.open(avatarImg, "r")
    # 加载二维码图片
    qrcode_img = Image.open(qrcodeImg, "r")
    # 加载商品图片
    info_img = Image.open(goodsImg, "r")

    #改变背景图颜色
    # background = Image.new('RGB', background.size, (178,  34, 34))


    back_img = drawCircleAvatar(avatar, background,headImgSize,headImgPosition)
    region = qrcode_img
    region = region.resize(qrcodeImgSize)
    back_img.paste(region, qrcodeImgPosition)
    info_img=info_img.resize(goodsImgSize)
    back_img.paste(info_img, goodsImgPosition)
    nameStart=int(int(len(nickname)) * nameSize / 2)
    fonts("simsun.ttc",imgWidth,nameStart,nickname,nameSize,back_img,nameCoordinate,1)
    fonts("simsun.ttc",imgWidth,goodsCoordinate[0],countWord,goodsSize,back_img,goodsCoordinate,2)
    back_img.save('out1.jpg')  
    endTime = time.time()

    print("在当前目录生成图片out1.jpg一共用时：")
    print(str(endTime - startTime) + "秒")


"""
将头像变成圆形绘制在背景图片上，然后将合成的图片对象返回
"""
def drawCircleAvatar(im, background,headImgSize,headImgPosition):
    im = im.resize(headImgSize)
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)
    background.paste(im, headImgPosition, im)
    return background


def fonts(font,maxWidth,startWidth,string,size,back_img,coordinate,type):
    lineWidth=int(maxWidth) - int(startWidth)
    newLine=int(lineWidth /size)
    new_str=''
    data=[]
    for strs in range(0,len(list(string))):
        if int(int(strs) + 1) % newLine == 0:
            data.append([new_str])
            new_str=''
        else:
            new_str+=string[strs]
    data.append([new_str])

    font = ImageFont.truetype(str(font), size)
    drawImage = ImageDraw.Draw(back_img)

    for da in range(len(data)):
        content=str(data[da]).replace("['",'').replace("']",'')
        if da > 0:
            new_height=(size+10) * da
            if int(type) == 1:
                drawImage.text((coordinate[0]-startWidth,coordinate[1]+new_height), u'%s' % content, color, font)
            else:
                drawImage.text((coordinate[0],coordinate[1]+new_height), u'%s' % content, color, font)
        else:
            if int(type) == 1:
                drawImage.text((coordinate[0]-startWidth, coordinate[1]), u'%s' % content, color, font)
            else:
                drawImage.text(coordinate, u'%s' % content, color, font)
'''
模板
'''
def template(id):
    #模板参数请看下方
    array=[[1080,(154,154),(463, 67),(280, 295),(400, 1337),(926, 460),(77, 480),32,(540,250),60,(100, 980),'./image/ooo.jpg'],[]]
    return array[id]



if __name__ == '__main__':
    try:
        # 头像图片
        avatarImg = "./image/rr.jpg"
        # 二维码图片
        qrcodeImg = "./image/iii.png"
        # 商品图片
        goodsImg = "./image/uuu.jpg"
        # 用户昵称
        nickname = '梦想家'
        # 商品信息
        countWord = "如果标题超出了图片宽度会不会自动换行呢?我想应该不会的!"
        # 模板id
        templateId = 0

        # 加载模板参数
        arrat = template(templateId)

        # 背景图片实际大小的宽度
        imgWidth = arrat[0]

        # 用户头像缩放到符合模板中展示头像的大小像素
        headImgSize = arrat[1]
        # 用户头像移动到展示模板中的位置   通过坐标左上角2元组的方式将头像图片放置在背景图像的（235，155）两个位置其结果如下图所示：
        headImgPosition = arrat[2]

        # 二维码缩放到符合模板中展示二维码的大小像素
        qrcodeImgSize = arrat[3]
        # 二维码移动到模板中展示二维码的位置   通过坐标左上角2元组的方式将头像图片放置在背景图像的（235，155）两个位置其结果如下图所示：
        qrcodeImgPosition = arrat[4]

        # 商品图片缩放到符合模板中展示商品的大小像素
        goodsImgSize = arrat[5]
        # 商品移动到模板中展示商品的位置   通过坐标左上角2元组的方式将头像图片放置在背景图像的（235，155）两个位置其结果如下图所示：
        goodsImgPosition = arrat[6]

        # 昵称字体大小
        nameSize = arrat[7]
        # 昵称字体坐标位置
        nameCoordinate = arrat[8]

        # 商品字体大小
        goodsSize = arrat[9]
        # 商品字体坐标位置
        goodsCoordinate = arrat[10]

        # 加载背景图片
        backgroundImg = arrat[11]

        createShareImg(avatarImg, qrcodeImg, goodsImg, nickname, countWord, imgWidth, headImgSize,
                       headImgPosition, qrcodeImgSize, qrcodeImgPosition, goodsImgSize,
                       goodsImgPosition,
                       nameSize, nameCoordinate, goodsSize, goodsCoordinate, backgroundImg)
        print('执行成功')
    except:
        print('服务器错误,请联系管理员')


