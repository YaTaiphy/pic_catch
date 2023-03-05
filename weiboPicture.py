from asyncio.windows_events import NULL
import shutil
import requests
from PIL import Image
from io import BytesIO
import os
import json

url='http://dasfdfasfasfasfdasfasf.com/'
try:
    response = requests.get(url, timeout=10)  # 超时设置为10秒
except:
    for i in range(4):  # 循环去请求网站
        response = requests.get(url,  timeout=20)
        if response.status_code == 200:
            break

    