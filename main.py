### 图片尺寸可供选择:square、thumb150、orj360、orj480、mw690、mw1024、mw2048、small、bmiddle、large 
### 根据之前经验，能做好统计就做好统计，不然再来一遍过于麻烦
## pip freeze > requirements

#-*-coding:utf-8-*-
# import sys;
# total=100000
# for i in range(0,total):
#   percent=float(i)*100/float(total)
#   sys.stdout.write("%.4f"%percent);
#   sys.stdout.write("%\r");
#   sys.stdout.flush();
# sys.stdout.write("100%!finish!\r");
# sys.stdout.flush();


import os
import json
import sys
import math

from get_picture import save_pic

run_path = os.getcwd()
# os.path.pardir() 获取上级路径
weibo21Path = os.path.abspath(os.path.join(run_path, os.path.pardir))


## 读取json文件，存储图片，对于符合需要的json进行相应的id存储，使用的当然是json方法
## 格式基本为，id：xxxx, piclists:[url1,url2,url3]
def json_read(abspath):
    f = open(abspath,'r',encoding='utf-8')
    
    ## fd_json用于存储符合要求的微博
    save_name = os.path.splitext(os.path.split(abspath)[1])[0]
    fd_json = open(r'./select_' + save_name + '.json','w+', encoding='utf-8')  
    
    count = 0
    may_exist = 0
    useful = 0
    num404 = 0
    numNoExist = 0
    
    lines = f.readlines()
    all_num = len(lines)
    
    print("\tid\t\tprogress\tImgprogress\tImgSizeSeletProgress")
    for line in lines:
        count = count + 1
        
        line_message = json.loads(line)
        
        img_id = line_message["id"]
        img_content = line_message["content"]
        img_urls = line_message["piclists"]
        img_label = line_message["label"]
        img_category = line_message["category"]
        
        out = "%d/%d"%(count, all_num)
        img_id2 = img_id.ljust(20)
        out2 = "%s"%out.rjust(10)
        sys.stdout.write("\t%s%s"%(img_id2, out2))
        
        pic_list = []
        img_count = 0
        num404sub = 0
        numNoExistsub = 0
        ### 注意！！！！注意！！！！！
        # 在json文件的3394行，开始"piclists": NaN，而非"piclists": []，导致程序出错，哪个傻逼写的json文件
        # 因此需要判断是否是nan，判断nan的方法如下
        ## 记录可能图片数量，到时候通过判断useful和may_exist的比例来判断是否存在爬取限制
        if not(isinstance(img_urls,float)):
            if len(img_urls) != 0:
                may_exist = may_exist + 1
            
            m = 0
            for img_url in img_urls:
                m = m + 1
                out = "%d/%d"%(m, len(img_urls))
                
                sys.stdout.write("%s"%out.rjust(15))
                
                status, message = save_pic(img_url)
                if status != 1:
                    if(status == -1):
                        numNoExistsub = numNoExistsub + 1
                    else:
                        num404sub = num404sub + 1
                    sys.stdout.write("\b"*15)
                    sys.stdout.flush()
                    continue
                pic_list.append(message)
                img_count = img_count + 1
                
                sys.stdout.write("\b"*15)
                sys.stdout.flush()
            
        if img_count == 0:
            if(num404sub > numNoExistsub):
                num404 = num404 + 1
            else:
                numNoExist = numNoExist + 1  
            sys.stdout.write("\r")
            sys.stdout.flush()
            continue
        useful = useful + 1
        
        result_json = json.dumps({'id': img_id,
                                  'content': img_content,
                                  'piclists': pic_list,
                                  'label': img_label,
                                  'category': img_category}, ensure_ascii=False)
        
        fd_json.write(result_json)
        fd_json.write('\n')
        
        sys.stdout.write("\r")
        sys.stdout.flush()
    
    f.close()
    fd_json.close()
    
    message = "total: %d, may_exist: %d, useful: %d, num404: %d, numNoExist %d\n"%(count, may_exist, useful, num404, numNoExist)
    
    fd_txt = open(r'./select_' + save_name + '.txt','w+', encoding='utf-8')
    fd_txt.write(message)
    fd_txt.close()
    
    return 0


if __name__ == '__main__':
    print("Reading.....")
    for file in os.listdir(weibo21Path):
        # os.path.splitext(file)[0]
        absPath = os.path.abspath(os.path.join(weibo21Path, file))
        if not os.path.isfile(absPath):
            continue
        ## print formate输出见https://blog.csdn.net/eagle2728/article/details/102934466
        print("current file: %s"%(file))
        print("\texceeding")
        json_read(absPath)
        print("current file: %s precess complete!\n"%(file))
    print("ALL Work Done!")
    