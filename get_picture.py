# 'https://wx4.sinaimg.cn/orj360/007dTstegy1hb5ejgii67j30to0xlgp1.jpg'
# -i https://pypi.tuna.tsinghua.edu.cn/simple 

import sys
import requests as req
import os
from PIL import Image
from io import BytesIO

from picture_similarity import computSimilarity


## 常用的图片后缀
# IMG_EXTS = [
#     ".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".jp2", ".j2k", ".jpf",
#     ".jpx", ".jpm", ".mj2", ".jxr", ".hdp", ".wdp", ".gif", ".raw", ".webp",
#     ".png", ".apng", ".mng", ".tiff", ".tif", ".svg", ".svgz", ".pdf", ".xbm",
#     ".bmp", ".dib", ".ico", ".3dm", ".max"
# ]
IMG_EXTS = [
    ".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".jp2", ".j2k", ".jpf",
    ".jpx", ".jpm", ".mj2", ".jxr", ".hdp", ".wdp", ".raw", ".webp",
    ".png", ".apng", ".mng", ".tiff", ".tif", ".svg", ".svgz", ".pdf", ".xbm",
    ".bmp", ".dib", ".ico", ".3dm", ".max"
]


def isNotDeleted(img):
    return True


def save_pic(url):
    ## sample_url = "//ww2.sinaimg.cn/orj360/a864f8c4jw1ecashyx78nj20c708r75a.jpg"
    ## 对以上url形式做切分，获取ww2.sinaimg.cn，a864f8c4jw1ecashyx78nj20c708r75a.jpg两个必要组成部分
    ## 注意，根据测试，有的url组成形式为"//u1.sinaimg.cn/upload/2013/07/03/33338.png"
    ## 而该形式的url，占少数。在fake_realease中只占20项，同时新浪微博禁止获取，因此抛弃该形式
    try:
        _,_,basic_part,_,name_part=url.split('/') 
    except:
        return 0, "NOT SUPPORTED URL TYPE"
    ## 第一步对图片进行判定，如果不符合，直接返回0，不再进行后续操作
    ext = os.path.splitext(name_part)[1]
    if(ext not in IMG_EXTS):
        return 0, "NOT SUPPORTED IMAGE TYPE"
    # 状态保存
    sta = 0
    
    ## 可能的图片尺寸
    img_type = ["square", "thumb150", "orj360", "orj480", "mw690", "mw1024", "mw2048", "small", "bmiddle", "large"]
    
    ## headers REDERER修改为weibo.com，欺骗微博官网
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Connection': 'close',
            # 标记了请求从什么设备，什么浏览器上发出
        }
    headers['Referer']= "https://weibo.com"
    req.adapters.DEFAULT_RETRIES = 5
    
    img_valueble = 0
    ## 构建一个1*1的图片，用于比较图片分辨率
    img_max = Image.new('RGB', (1, 1))
    content_max = None
    
    m = 0
    for img in img_type:
        m = m + 1
        
        out = "%d/%d"%(m, len(img_type))
        sys.stdout.write("%s"%out.rjust(6, " "))
        sys.stdout.write("\b"*6)
        sys.stdout.flush()
        ## 拼接url
        concat_url = "https://" + basic_part + "/" + img + "/" + name_part
        
        ## 如果pic有该图片，跳过
        pic_path = './pic'
        
        if(os.path.exists(os.path.join(pic_path, name_part))):
            img_valueble = 1
            return img_valueble, name_part
        
        ## 发送请求，如果无法连接到，则抛弃
        try:
            response = req.get(concat_url, headers=headers, timeout=30)
        except:
            continue
        
        if(response.status_code != 200):
            continue
        
        ## 读取图片，判定分辨率，保存分辨率最大的图片
        image = Image.open(BytesIO(response.content))
        
        ## 判断图片是否被删除
        if computSimilarity(image):
            if(img_valueble == 0):
                img_valueble = -1
            continue
        
        max_pre = img_max.size[0] * img_max.size[1]
        max_now = image.size[0] * image.size[1]
        # print(max_now)
        if(max_now > max_pre):
            img_max = image
            content_max = response.content
        
        ## 图片计数
        img_valueble = 1
    
     # ## 输出图片名称
    # print(os.path.splitext(name_part))
    if(img_valueble == 0):
        return img_valueble, "NO IMAGE"  ## 无图片
    elif(img_valueble == -1):
        return img_valueble, "IMAGE DELETED"
    
    ## 保存图片
    save_path = "./pic/" + name_part
    with open(save_path, 'wb') as f:  # 以二进制写入文件保存
        f.write(response.content)
        
   
    return img_valueble, name_part

if __name__ == "__main__":
    print("test for save_pic")
    sample_url = "//ww2.sinaimg.cn/orj360/a864f8c4jw1ecashyx78nj20c708r75a.jpg"
    _,_,basic_part,_,name_part=sample_url.split('/') 
    
    ## 可能的图片尺寸
    img_type = ["square", "thumb150", "orj360", "orj480", "mw690", "mw1024", "mw2048", "small", "bmiddle", "large"]
    
    ## headers REDERER修改为weibo.com，欺骗微博官网
    headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            # 标记了请求从什么设备，什么浏览器上发出
        }
    headers['Referer']= "https://weibo.com"
    
    img_valueble = 0
    ## 构建一个1*1的图片，用于比较图片分辨率
    img_max = Image.new('RGB', (1, 1))
    content_max = None
    
    for img in img_type:
        ## 拼接url
        concat_url = "https://" + basic_part + "/" + img + "/" + name_part
        
        ## 发送请求
        response = req.get(concat_url, headers=headers)
        if(response.status_code != 200):
            continue
        
        ## 读取图片，判定分辨率，保存分辨率最大的图片
        image = Image.open(BytesIO(response.content))
        max_pre = img_max.size[0] * img_max.size[1]
        max_now = image.size[0] * image.size[1]
        print(max_now)
        if(max_now > max_pre):
            img_max = image
            content_max = response.content
        
        ## 图片计数
        img_valueble = img_valueble + 1
    
    ## 保存图片
    save_path = "./pic/" + name_part
    with open(save_path, 'wb') as f:  # 以二进制写入文件保存
        f.write(response.content)
        
    # ## 输出图片名称·
    # print(os.path.splitext(name_part))
    