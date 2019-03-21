#!/usr/bin/env python3
# pip3 install pymupdf
import fitz
import sys
import re
import os



def pdf2pic(pdf_path, output_path):
    # 使用正则表达式来查找图片
    checkXO = r"/Type(?= */XObject)" 
    checkIM = r"/Subtype(?= */Image)" 
    
    # 打开pdf
    doc = fitz.open(pdf_path)
    # 图片计数
    imgcount = 0
    lenXREF = doc._getXrefLength()
 
    # 打印PDF的信息
    print("文件名:{}, 页数: {}, 对象: {}".format(pdf_path, len(doc), lenXREF - 1))
    
    # 遍历每一个对象
    for i in range(1, lenXREF):
        # 定义对象字符串
        text = doc._getXrefString(i)
        
        isXObject = re.search(checkXO, text)
        # 使用正则表达式查看是否是图片
        isImage = re.search(checkIM, text)
        # 如果不是对象也不是图片，则continue
        if not isXObject:
            continue
        if not isImage:
            continue
        imgcount += 1
        # 根据索引生成图像
        pix = fitz.Pixmap(doc, i)
        # 根据pdf的路径生成图片的名称
        
        new_name = "%02d.png" %imgcount

        # 如果pix.n<5,可以直接存为PNG
        if pix.n < 5:
            pix.writePNG(os.path.join(output_path, new_name))
        # 否则先转换CMYK
        else:
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG(os.path.join(output_path, new_name))
            pix0 = None
        # 释放资源
        pix = None
        print("提取了{}张图片".format(imgcount))

def pdf2txt(pdf_path,output_path):
    '''
    从PDF中获取文本
    '''
    doc = fitz.open(pdf_path)
    output_file = output_path + os.sep + 'output.txt'
    print(output_file)
    out = open(output_file,'w')
    for d in doc:
        out.write(d.getText("text")) # 可选 html / xml /json  等
    out.close()

if __name__=='__main__':
    # pdf路径
    if len(sys.argv) == 1:
        exit(-1)
    pdf_path = sys.argv[1]
    output_path = os.getcwd() + os.sep + os.path.basename(pdf_path)[:-4]
    # 不存在则创建
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    pdf2txt(pdf_path,output_path)
    pdf2pic(pdf_path,output_path)