import os
from PIL import Image
import numpy as np
import shutil

# imageA = np.array(Image.open("./sample/1.jpg"))
# imageB = np.array(Image.open("./sample/3.jpg"))

## OSError: image file is truncated (97 bytes not processed)
# 注意该报错
## 另外，注意需要使用四舍五入（补充：个屁），否则会因为浮点误差出现图片尺寸不一致的情况
## python的int float自动转换真让人摸不着头脑，总是得debug
def centerCrop(image, re_width, re_height):
    width, height = image.size
    # size = 200
    left = round((width - re_width) / 2)
    top = round((height - re_height) / 2)
    
    ## 因此使用以下方法
    # right = round((width + re_width) / 2)
    # bottom = round((height + re_height) / 2)
    ## 教训， 网上的代码不能随便抄
    
    right = left + re_width
    bottom = top + re_height
    return image.crop((left, top, right, bottom))

def eucliDist(A,B):
    return np.sqrt(sum(np.power((A - B), 2)))

def cosDist(A,B):
    return np.dot(A,B)/(np.linalg.norm(A)*np.linalg.norm(B))

def hist_similar(lh, rh):
    hist = sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)
    return hist

def computSimilarity(image):
    width, height = image.size
    widthS, heightS = imageSample.size
    
    re_width = min(width, widthS)
    re_height = min(height, heightS)
    # if(width < 200 or height < 200):
    #     return True
    
    imageN = centerCrop(image, re_width, re_height)
    imageNp = np.array(imageN)
    imageSampleN = centerCrop(imageSample, re_width, re_height)
    imageSampleNp = np.array(imageSampleN)
    
    if(imageSampleNp.shape == imageNp.shape and imageSampleN.mode == imageN.mode):
        ed = np.sum(eucliDist(imageNp,imageSampleNp)/(imageNp.shape[0]*imageNp.shape[1])) + hist_similar(imageN.histogram(), imageSampleN.histogram())/10
        if ed < 0.3:
            return True
        else:
            return False
    return False
    


imageSample = Image.open("./sample/1.jpg")

if __name__ == "__main__":
    testA = np.array(Image.open("./sample/2.jpg"))
    testB = np.array(Image.open("./sample/4.jpg"))
    testC = np.array(Image.open("./sample/eb6eb503jw1efax69mn90j20k00e3di8.jpg"))
    
    print(computSimilarity(Image.open("./sample/3.jpg")))
    
    
    pic_path = "./pic"
    
    
    for file in os.listdir(pic_path):
        if computSimilarity(Image.open(os.path.join(pic_path, file))):
            print(file)
            try:
                shutil.move(os.path.join(pic_path, file), "./sample/")
            except:
                os.remove(os.path.join(pic_path, file))