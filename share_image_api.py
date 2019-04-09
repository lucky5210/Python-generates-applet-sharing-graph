# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request
from urllib import request as req
import time,json,uuid,os

app = Flask(__name__)

#存放下载的图片
dir='./image/'

# 头像的命名空间
class HEAD_NAMESPACE:
    bytes = b'1'

# 商品的命名空间
class GOODS_NAMESPACE:
    bytes = b'2'

# 二维码的命名空间
class QRCODE_NAMESPACE:
    bytes = b'3'


# 字体颜色
color = "#000000"

"""
生成分享图片的方法
"""
def createShareImg(avatarImg, qrcodeImg, goodsImg, nickname, countWord,imgWidth,headImgSize,headImgPosition,qrcodeImgSize,qrcodeImgPosition,goodsImgSize,goodsImgPosition,nameSize,nameCoordinate,goodsSize,goodsCoordinate,backgroundImg):
    startTime = time.time()
    background = Image.open(backgroundImg)
    avatar = Image.open(avatarImg, "r")
    qrcode_img = Image.open(qrcodeImg, "r")
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

    # 绘制内容
    fonts("simsun.ttc",imgWidth,goodsCoordinate[0],countWord,goodsSize,back_img,goodsCoordinate,2)
    # 保存图片到文件
    back_img.save('out1.jpg')  # 保存图片
    endTime = time.time()
    print("本次生成图片一共用时：")
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

"""
内容字体计算 一行显示多少字 自动换行  最后不足一行的居中展示
"""
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
            #等于1是居中显示 其他是根据设置的坐标显示
            if int(type) == 1:
                drawImage.text((coordinate[0]-startWidth, coordinate[1]), u'%s' % content, color, font)
            else:
                drawImage.text(coordinate, u'%s' % content, color, font)

"""
下载图片
"""
def downloadImg(jpg_link,imgName):
    try:
        #设置请求下载链接时添加header中的User-Agent
        opener = req.build_opener()
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        req.install_opener(opener)
        req.urlretrieve(jpg_link, imgName)
        return True
    except:
        return False



"""
如果用户头像 商品图片 二维码图片可以再本地获取会很明显的提升运行速度
"""
@app.route('/share/', methods = ['GET','POST'])
def sharImg():
    if request.method == 'POST':
        try:
            if not os.path.isdir(dir):
                os.makedirs(dir)

            times = str(int(time.time()))
            head_ = uuid.uuid3(HEAD_NAMESPACE, times)
            goods_ = uuid.uuid3(GOODS_NAMESPACE, times)
            qrcode_ = uuid.uuid3(QRCODE_NAMESPACE, times)

            head_path=str(dir)+str(head_)+'.png'
            goods_path=str(dir)+str(goods_)+'.png'
            qrcode_path=str(dir)+str(qrcode_)+'.png'
            startTime = time.time()

            head = downloadImg(request.form['head_url'], head_path)
            goods = downloadImg(request.form['goods_url'], goods_path)
            qrcode = downloadImg(request.form['qrcode_url'], qrcode_path)
            endTime = time.time()
            print('下载图片一共用时:')
            print(str(endTime-startTime)+'秒')
            if head:
                if goods:
                    if qrcode:
                        # 头像图片
                        avatarImg = head_path
                        # 商品图片
                        goodsImg = goods_path
                        # 二维码图片
                        qrcodeImg = qrcode_path
                        # 用户昵称
                        nickname = request.form['name']
                        # 商品信息
                        countWord = request.form['content']
                        # 模板id
                        templateId = int(request.form['templateid'])

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
                        return json.dumps({'status': True, 'mag': 'ok'})
                    else:
                        return json.dumps({'status': False, 'mag': '获取二维码图片失败导致无法生成分享图'})
                else:
                    return json.dumps({'status': False, 'mag': '获取商品图片失败导致无法生成分享图'})
            else:
                return json.dumps({'status': False, 'mag': '获取头像图片失败导致无法生成分享图'})
        except:
            return json.dumps({'status': False, 'mag': '服务器错误,请联系管理员'})
    else:
        return json.dumps({'status': False, 'mag': '请使用POST方式'})

"""
模板参数
"""
def template(id):
    #元素注释 请看上方
    array=[[1080,(154,154),(463, 67),(280, 295),(400, 1337),(926, 460),(77, 480),32,(540,250),60,(100, 980),'./image/ooo.jpg'],[]]
    return array[id]

if __name__ == '__main__':
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", port=8000, debug=True)

