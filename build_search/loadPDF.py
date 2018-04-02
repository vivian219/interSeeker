import json
import hashlib
import redis_manager
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser, PDFDocument
import re
import time
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
def spider_bot(pdfList,redis_obj):
    for pdf in pdfList:
        md5ConTex=pdf['title']
        conTex=pdf['conTex']
        report_md5=pdf['report_md5']
        if conTex=="":
            continue
        md5 = hashlib.md5(md5ConTex.encode('utf-8')).hexdigest()
        redis_obj.public(json.dumps({"md5":md5,"conTex":conTex,"report_md5":report_md5,"url":""}))
def readAllPdf(filePath,txt_obj):
    import os
    path = filePath  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file in files:  # 遍历文件夹
        m = re.match('.+pdf$', file)
        if m is None:
            print('continue',file)
            continue
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            content=getPdfContent("pdfFile/"+file)
            pdf={}
            pdf['title']=file
            pdf['conTex']=content
            report_md5 = hashlib.md5(file.encode('utf-8')).hexdigest()
            pdf['report_md5']=report_md5
            s.append(pdf)  # 每个文件的文本存到list中
            _time=time.strftime('%Y-%m-%d', time.localtime(time.time()))#在循环体中加上time
            txt_obj.public(json.dumps({"md5":report_md5,"title":file.split('.pdf')[0],"tag":"","abstract":"","time":str(_time),"urlList":"","vendor":"","source":"pdf"}))
            time.sleep(3)
    logging.warning(s)  # 打印结果
    return s
def getPdfContent(filepath):
    #fileDir="pdfFile/"
    fp = open(filepath, 'rb')  # 以二进制读模式打开
    # 用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)
    content = ""
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        content = ""
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages():  # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    content += results
    content = " ".join(content.replace("\n", "").strip().split())
    return content
def loadLocalFile():
    spider_pub=redis_manager.SpiderRedis()
    txt_pub=redis_manager.TxtRedis()
    pdfList=readAllPdf("pdfFile",txt_pub)
    print(pdfList)
    spider_bot(pdfList,spider_pub)
def uploadFile(filepath,filename,report):
    txt_pub=redis_manager.TxtRedis()
    content=getPdfContent(filepath)
    pdf={}
    pdf['title']=filename
    pdf['conTex']=content
    report_md5 = hashlib.md5(filename.encode('utf-8')).hexdigest()
    pdf['report_md5']=report_md5
    pdfList=[]
    pdfList.append(pdf)
    logging.info("txt extend info",report)
    txt_pub.public(json.dumps({"md5":report_md5,"title":filename.split('.pdf')[0],"tag":report["labels"],"abstract":report["abstract"],"time":report["date"],"urlList":"","vendor":report["from"],"source":"pdf"}))
    spider_pub=redis_manager.SpiderRedis()
    spider_bot(pdfList,spider_pub)
