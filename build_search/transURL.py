# -*- coding: utf-8 -*-
'''
获得目前已经爬取的URL列表
通过白名单对URL进行筛选，得到新的URL
利用爬虫爬取页面内容并匹配IP,Domain等信息
导入buildIndex
利用buildIndex中的相关函数将新匹配到的信息录入ES
'''
import re
from enum import Enum

from bs4 import BeautifulSoup
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser, PDFDocument

import buildIndex
import mongoengine_test

class ExtractMode(Enum):
    PDFMode = 1
    HTMLMode = 2

def getURLlist():
    f=open(r'F:\实验室\安管中心-暑期项目\urlfile.txt',"r",encoding='utf-8')
    urlList=[]
    for line in f.readlines():
        urlList.append(line.split("\n")[0])
    return urlList


def filtURL(filename, urlList):
    f=open(filename)
    urlfile=open(r'F:\实验室\安管中心-暑期项目\urlfile.txt',r'a',encoding='utf-8')
    filePat=re.compile(r'https?://.*')
    newURL=[]
    for line in f.readlines():
        # 找出URL并存储在文件中
        match=filePat.match(line)
        if match and line not in urlList:
            urlfile.write(line)
        else:
            continue
        newURL.append(line)
    return newURL

"""
从url爬取内容并返回，当无法爬取或超时，返回为空
"""
def spider(url):
    import requests
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}
    try:
        r=requests.get(url,headers=headers).content.decode('utf-8','ignore')
    except Exception:
        r=""
    return r


"""
从给定的路径读取白名单,返回白名单
"""
def genWhiteList():
    f=open(r'F:\实验室\安管中心-暑期项目\白名单\top-1m.csv')
    whiteList=[]
    for line in f.readlines():
        whiteList.append(line.split(",")[1])
    return whiteList


"""
白名单判断函数,判断 url 是否在白名单列表内
"""
def whiteJudge(whiteList,url):
    if url in whiteList:
        return "whiteURL : "+url
    else:
        return url

def parse_html(url):
    """
    从 url 对应的网页中抽取内容
    :param url: 要爬取的网页链接
    :return: 抽取到的文本内容
    """
    content = spider(url)
    if content == "":
        return content
    soup = BeautifulSoup(content)
    conTex = soup.get_text()
    return conTex


def parse_pdf(url):
    """
    从pdf中抽取内容
    :param filename: 要抽取的 pdf路径
    :return: 抽取到的pdf的内容
    """
    get_pdf(url)
    fp = open('1.pdf', 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
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
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
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



def parser(urlList, mode):
    """
    爬取URL,使用域名后缀进行筛选,并提取其中的结构化信息
    :param urlList: 需要爬取的URL链接
    :return: 根据URL页面内容得到的结构化信息
    """
    topHostPostfix = [    '.com','.la','.io','.co','.info','.net','.org','.me','.mobi',
    '.us','.biz','.xxx','.ca','.co.jp','.com.cn','.net.cn',
    '.org.cn','.mx','.tv','.ws','.ag','.com.ag','.net.ag',
    '.org.ag','.am','.asia','.at','.be','.com.br','.net.br',
    '.bz','.com.bz','.net.bz','.cc','.com.co','.net.co',
    '.nom.co','.de','.es','.com.es','.nom.es','.org.es',
    '.eu','.fm','.fr','.gs','.in','.co.in','.firm.in','.gen.in',
    '.ind.in','.net.in','.org.in','.it','.jobs','.jp','.ms',
    '.com.mx','.nl','.nu','.co.nz','.net.nz','.org.nz',
    '.se','.tc','.tk','.tw','.com.tw','.idv.tw','.org.tw',
    '.hk','.co.uk','.me.uk','.org.uk','.vg', ".com.hk"]
    '''保存结果'''
    res_file=open(r"F:\实验室\安管中心-暑期项目\res.csv","a",encoding='utf-8')
    res_list=[]
    whiteList=genWhiteList()
    for url in urlList:
        res=""
        pat_pdf=re.compile('.pdf$')
        m=re.match(url,'.pdf$')
        if m is None:
            conTex=parse_html(url)
        else:
            conTex=parse_pdf(url)
        # if mode == ExtractMode.HTMLMode:
        #     conTex = parse_html(url)
        # elif mode == ExtractMode.PDFMode:
        #     conTex = parse_pdf(url)
        # 如果为空, 则进入下一轮抽取
        if conTex == "":
            continue
        mongoengine_test.contentToFile(url,conTex)
        continue
        pat_ip=re.compile('\d{1,3}(\.\d{1,3}){3}')
        pat_dom=re.compile('([a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?)')
        pat_hash=re.compile('[a-z|0-9|A-Z]{32,64}')
        
        res_ip_list = list(pat_ip.finditer(conTex))
        res_dom_list = list(pat_dom.finditer(conTex))
        res_hash_list=pat_hash.findall(conTex)
        
        res_file.write(str(url)+",")
        res+=(str(url)+",")
        for i in res_ip_list:
            if len(i.group(0))<15:
                res+=(i.group(0)+"|")
                res_file.write(i.group(0)+"|")
        if len(res_ip_list) <1:
            res+=("none")
            res_file.write("none")
        res+=(",")
        res_file.write(",")
        empty=1
        for i in res_dom_list:
            wordlist=i.group(0).split('.')
            l=len(wordlist)
            if '.'+wordlist[l-1] in topHostPostfix:
                judURL=whiteJudge(whiteList,str(i.group(0)))
                res+=(judURL+"|")
                res_file.write((i.group(0)+"|"))
                empty=0
        if empty==1:
            res+=("none")
            res_file.write("none")
        res+=(",")
        res_file.write(",")
        for hash_value in res_hash_list:
            if len(hash_value)==32 or len(hash_value)==40 or len(hash_value)==64:
                res+=(hash_value+"|")
                res_file.write(hash_value+"|")
        if len(res_hash_list)<1:
            res+=("none")
            res_file.write("none")
        res_file.write("\n")
        res_list.append(res)
    return res_list



def buildDoc(resList):
    """
    :param resList:以','分隔的结构化信息
    :return:
    """
    for res in resList:
        resDict= buildIndex.prepare_dict(res)
        if not buildIndex.document_exist(resDict["url"]):
            buildIndex.post_document(buildIndex.index_name, resDict)
        else:
            print("{0} already exist!".format(resDict["url"]))


""" HTML 爬取部分 """
def addNewHTMLDoc(filename):
    """
    从filename中读取 url,并进行爬取
    :param filename: url 存储文件
    """
    # 获取URL
    urlList = getURLlist()
    # 从filename中获取新的URL，更新到 url list文件中，并整合成新的URL
    newURL = filtURL(filename, urlList)
    # 从URL中抽取结构化的信息
    res_list = parser(newURL, ExtractMode.HTMLMode)
    # 为文档建立索引
    buildDoc(res_list)


""" PDF 爬取部分 """
def addNewPDFDoc(filename):
    """
    从filename中读取 pdf文件的路径,并遍历进行爬取
    :param filename: url 存储文件
    """
    # 获取PDF文件路径
    with open(filename, 'r') as fp:
        fileList = fp.readlines()
    res_list = parser(fileList, ExtractMode.PDFMode)
    print(res_list)
    # 为文档建立索引
    buildDoc(res_list)
def get_pdf(url):
    # soup=BeautifulSoup(r)
    # print(soup.contents)
    # f=open('test_pdf.txt','w')
    # f.write(r)
    import requests

    # url = 'https://www2.trustwave.com/rs/815-RFM-693/images/2017%20Trustwave%20Global%20Security%20Report-FINAL-6-20-2017.pdf'
    r = requests.get(url)
    with open('1.pdf', 'wb') as f:
        f.write(r.content)

if __name__ == "__main__":
    addNewHTMLDoc(r"F:\实验室\安管中心-暑期项目\APT Feeds_v0.txt")
    #addNewPDFDoc("pdflist.txt")
    # r=spider('https://www2.trustwave.com/rs/815-RFM-693/images/2017%20Trustwave%20Global%20Security%20Report-FINAL-6-20-2017.pdf')
    # print(r)
