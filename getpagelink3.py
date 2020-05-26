#! python3
# -*- coding: UTF-8 -*-
#coding: UTF-8
#获取帖子网页中的每个帖子的链接,存入字典link_dict，格式{链接全地址:link标题}，如{"https://www.aisex.com/bt/htm_data/xxx/xxxxx.html":"xxx来了"}

from bs4 import BeautifulSoup
import requests
import re
from pStr3 import refineString,removeSstr
pattern = re.compile("[.*M]")
pattern2 = re.compile("[.*G]")
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

def getlink_list(my_page='https://www.aisex.com/bt/thread.php?fid=16&page=1',page_host = u'www.aisex.com',enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "获取网页中帖子链接的列表"

    page_prefix = "https://www.aisex.com/bt/"
    #page_no = "1"
    #full_page_address = page_prefix + "thread.php?fid=16&page=" + page_no
    try:
        r1 = requests.get(my_page,headers = headers,timeout = 15)
    except Exception as e:
        print('error',e)

    content1 = r1.content.decode("gbk","ignore")

    soup = BeautifulSoup(content1,'html.parser')
    mytags_a = soup.find_all('a')
    #print 'A tags-----------'
    link_list = []
    link_dict = {}
    linksList = []
    n = 0
    for mytag_a in mytags_a:
        mytag_href = str(mytag_a.get('href'))
        mytag_title = mytag_a.get('title')
        mytag_string = mytag_a.string
        #mytag_string = mytag_string.decode('gbk') #将GBK编码转换为unicode，如果要把unicode转为gbk则用encode('gbk')
        #也可用unicode(str,'gbk'),与str.decode('gbk')一样

        if mytag_href.find('htm_data') != -1:
            if mytag_title == None:
                if mytag_string.find(u'发帖者') == -1 & mytag_string.find(u'版规') == -1:
                    #print 'the tag A is: %s' %unicode(mytag_a)
                    #print 'the href is: %s' %unicode(mytag_href)
                    myfull_link = page_prefix + mytag_href #内容页全地址full_Url
                    link_list.append(myfull_link)
                    mytorrent_filename = removeSstr(mytag_string)
                    mytorrent_filename = refineString(mytorrent_filename)
                    linksList.append({'title':mytorrent_filename,'link':myfull_link})
                    n = n+1
                    print('    ',n,'Refined Title: ',mytorrent_filename)

                    link_dict[myfull_link] = mytorrent_filename #以赋值的方式生成字典{myfull_link:mytorrent_filename}
    print('total %s links in this page: %s\n' %(n,my_page))
    return linksList,link_dict

def getLinksLists(indexPageS = 1,indexPageC = 2):
    prePage = 'https://bt.aisex.com/bt/thread.php?fid=16&page='
    linksList = [] #内容 {'title':torrenttitle,'link':btpagefull_link}
    for pageN in range(indexPageS,indexPageS+indexPageC):
        curPage = prePage + str(pageN)
        linksList_1,linkDict = getlink_list(my_page=curPage)
        linksList = linksList + linksList_1
    return linksList

if __name__ == '__main__':
    print('not run in module mode ',__name__)
    n = 0
##    a,b = getlink_list(enable_proxy = False)
##    for item in a:
##        n = n + 1
##        print(n,item)
##    n = 0
##    print(b)
##    for item in b:
##        n = n + 1
##        print(n,item)
    c = getLinksLists(1,2)
    for item in c:
        n = n+1
        print(n,item)
