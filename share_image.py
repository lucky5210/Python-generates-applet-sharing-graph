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

    # 将背景图片和圆形头像合成之后当成新的背景图片
    back_img = drawCircleAvatar(avatar, background,headImgSize,headImgPosition)

    # 将二维码图片粘贴在背景图片上
    region = qrcode_img
    #将二维码图片缩小到180*180像素
    region = region.resize(qrcodeImgSize)
    #通过坐标左上角2元组的方式将二维码图片放置在背景图像的（230，860）两个位置其结果如下图所示：
    back_img.paste(region, qrcodeImgPosition)

    #将商品图片黏贴在背景图片上
    #将商品图片缩小到926*337像素
    info_img=info_img.resize(goodsImgSize)
    #通过坐标左上角2元组的方式将二维码图片放置在背景图像的（77，430）两个位置其结果如下图所示：
    back_img.paste(info_img, goodsImgPosition)


    # 绘制用户昵称
    #计算出字体总长度 求出字体居中开始的位置
    nameStart=int(int(len(nickname)) * nameSize / 2)
    fonts("simsun.ttc",imgWidth,nameStart,nickname,nameSize,back_img,nameCoordinate,1)

    # 绘制内容
    fonts("simsun.ttc",imgWidth,goodsCoordinate[0],countWord,goodsSize,back_img,goodsCoordinate,2)
    # 保存图片到文件
    back_img.save('out1.jpg')  # 保存图片
    endTime = time.time()

    print("在当前目录生成图片out1.jpg一共用时：")
    print(str(endTime - startTime) + "秒")


"""
将头像变成圆形绘制在背景图片上，然后将合成的图片对象返回
"""
def drawCircleAvatar(im, background,headImgSize,headImgPosition):
    #头像缩放到154*154像素
    im = im.resize(headImgSize)
    #创建一个新的透明图片
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    # 遮罩对象
    mask = Image.new('L', bigsize, 0)
    #创建一个可以在给定图像上绘图的对象。
    draw = ImageDraw.Draw(mask)
    # 画椭圆的方法  在给定的区域绘制一个椭圆形。
    draw.ellipse((0, 0) + bigsize, fill=255)
    #图像缩放到和头像图片一致
    mask = mask.resize(im.size, Image.ANTIALIAS)
    #图像 im 必须是 "RGBA"或者"RGB"，alpha 必须是 "L" 或 "1".
    #将一张与原图尺寸相同的图片写入到原图片的透明通道之中，但不会影响原图片的正常显示. 可用于信息隐藏. 在做信息隐藏时，需要原图具有透明通道.
    im.putalpha(mask)
    #通过坐标左上角2元组或4元组的方式将头像图片放置在背景图像的（235，155）两个位置其结果如下图所示：
    background.paste(im, headImgPosition, im)
    return background


#内容字体计算 一行显示多少字 自动换行  最后不足一行的居中展示
def fonts(font,maxWidth,startWidth,string,size,back_img,coordinate,type):
    #计算出行最大宽度
    lineWidth=int(maxWidth) - int(startWidth)
    #计算出到第几个字符该换行了
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

    # 设置字体格式  字体大小
    font = ImageFont.truetype(str(font), size)
    #加载背景图片
    drawImage = ImageDraw.Draw(back_img)

    for da in range(len(data)):
        content=str(data[da]).replace("['",'').replace("']",'')
        #da大于0 说明字体内容一行装不下需要换行 换行需要增加高度 否则字体会重叠在一起
        if da > 0:
            new_height=(size+10) * da
            #等于1是居中显示 其他是根据设置的坐标显示
            if int(type) == 1:
                drawImage.text((coordinate[0]-startWidth,coordinate[1]+new_height), u'%s' % content, color, font)
            else:
                drawImage.text((coordinate[0],coordinate[1]+new_height), u'%s' % content, color, font)
        else:
            #等于1是居中显示 其他是根据设置的坐标显示
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
        print('执行成功.')
    except:
        print('服务器错误,请联系管理员')


