import json
import requests
from requests.cookies import RequestsCookieJar
import requests.utils
from urllib import parse
import os
import re
from lxml import etree
from typing import List,Union
import time
import base64
from colorama import Fore,Style
from wenkuthread import wenkupool as WenkuPool
import database
from book import Wenkubook1 as wenkubook
from book import get_book,insert
import sqlalchemy


def display_message(message, color, style=Style.NORMAL):
    formatted_message = f"{style}{color}{message}{Style.RESET_ALL}"
    print(formatted_message)

class wenku():
    __cookies = RequestsCookieJar()
    __headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    __filename = './book/'
    def __init__(self,uid=None,pwd=None) -> None:
        self.uid = uid
        self.pwd = pwd
        self.__file_init()
        self.Pool = None
        database.init()
    
    def __file_init(self):
        if not os.path.exists(self.__filename):
            os.makedirs(self.__filename)
        if not os.path.exists('./cookies.txt'):
            with open('./cookies.txt','w',encoding='utf-8') as f:
                f.close()

    def login(self,uid:str='',pwd:str='',mode=86400):#mode 和上次一样 0浏览器进程 86400一天 当然还有其他的 这里我们默认一天
        if uid:
            self.uid = uid
        if pwd:
            self.pwd = pwd
        if not self.uid or not self.pwd:
            print("你是不是有鬼 登录不给账号密码 等着报错吧")
            return False
        params = {
            'do':'submit'
        }
        data = {
            'username':uid,
            'password':pwd,
            'usecookie':mode,
            'action':'login',
            'submit':'&#160;登&#160;&#160;录&#160;'#gbk的话%26%23160%3B%B5%C7%26%23160%3B%26%23160%3B%C2%BC%26%23160%3B
        }
        login_url = 'https://www.wenku8.cc/login.php'
        r = requests.get(login_url,headers=self.__headers)
        self.__cookies.update(r.cookies) #更新cookies
        self.__lookcookie(r.cookies)
        headers = self.__headers
        headers['origin'] = 'https://www.wenku8.net'
        headers['referer'] = 'https://www.wenku8.net/login.php'
        login_r = requests.post(login_url,headers=headers,data=data,params=params,cookies=self.__cookies)
        if login_r.status_code == 200:
            self.__cookies.update(login_r.cookies)
            self.__lookcookie(login_r.cookies)
            self.__cookies_save(login_r.cookies)
            return True
        else:
            display_message("登录失败",Fore.RED, Style.BRIGHT)
            return False

    def __cookies_read(self,a:str='cookies.txt'):#a 是指文件名
        #读cookie用的 避免一直登录
        cookies_dict = {}
        with open(a,'r',encoding='utf-8') as f:
            cookies = f.read()
            if cookies:
                cookies_dict = json.loads(cookies)
        cookies = requests.utils.cookiejar_from_dict(cookies_dict)#将字典转为CookieJar：
        return cookies
    
    def __cookies_save(self,s):#s 是指cookie
        #人工储存cookie
        cookies_dict = requests.utils.dict_from_cookiejar(s)
        cookies_str = json.dumps(cookies_dict)
        with open ('cookies.txt','w+') as f:
            f.write(cookies_str)

    def __lookcookie(self,s:RequestsCookieJar):
        #方便我查看cookie s是cookie
        cookies_dict = requests.utils.dict_from_cookiejar(s)
        cookies_str = json.dumps(cookies_dict)#多重字典应该用dumps 不然会报错

    def __cerficate(self):
        #验证之前的cookie是否有效
        self.__cookies.update(self.__cookies_read('cookies.txt'))#首先读取之前的cookie
        a = self.bookcase()
        pattern = re.compile(r'https://www.wenku8.cc/login.php')
        matchobj = pattern.match(a) 
        if matchobj:
            return False
        return True

    def bookcase(self):
        #没什么用就是看看我的书架
        headers = self.__headers
        headers['referer'] = 'https://www.wenku8.cc/index.php'
        bookcase_url = 'https://www.wenku8.cc/modules/article/bookcase.php'
        r = requests.get(bookcase_url,headers=headers,cookies=self.__cookies)
        if r.status_code == 200:
            r.encoding="gbk"
        return r.url
    
    
    def is_login(self):
        if self.__cerficate():
            return True
        else:
            uid= input("请输入用户名:")
            pwd = input("请输入密码:")
            if self.login(uid,pwd):
                return True
        return False
    def __datatoparse(self,data:dict) ->str:
        query_string = parse.urlencode(data,encoding='gbk')
        return query_string
    
    def __getbookid(self,s:str)->int:
        patten = re.compile(r'/(([0-9]+)).htm$')
        selectobj = patten.search(s.strip()).group(1)
        return selectobj
    #downtype = 1时则自动文字下载到sqlite里面 做一下尝试
    def searchbook(self,selecttype='articlename',searchkey:str=None,downtype:int= 0):#参数有articlename author
        if self.is_login():
          res = self.__selectbook(selecttype=selecttype,searchkey=searchkey,pagenum=1)
          #0 maxpage def
          if len(res[1])  == 0:#没有找到
              display_message("没有找到",color=Fore.GREEN)
          if len(res[1]) == 1:#找到了 但是直接302跳转到了小说页面
              display_message("正在下载",color=Fore.GREEN)
              self.__downbook(bookid=self.__getbookid(res[1][0][1]),bookname=res[1][0][0],downtype=downtype)
              return 
          booklist = []
          while res[0] != res[2]:
              display_message("稍等 page:"+str(res[2]+1),color=Fore.GREEN)
              time.sleep(6)# 他说要等5s 
              res = self.__selectbook(selecttype=selecttype,searchkey=searchkey,pagenum=res[2]+1)
              for i in res[1]: #i->[[name,url],[name2,url]]
                  i:list
                  booklist.append(i[0])
          display_message("看看你找的是哪一本书:",color=Fore.GREEN)
          display_message(booklist,color=Fore.YELLOW)
        else:
            display_message("没有登录",color=Fore.RED)


    def __selectbook(self,selecttype='articlename',searchkey:str=None,pagenum:int = 1) ->list:
        url = 'https://www.wenku8.cc/modules/article/search.php'
        data = {
            'searchtype':selecttype,
            'searchkey':searchkey,
            'action':'login',
            'submit':'&#160;搜&#160;&#160;索&#160;',
            'page':pagenum,
        }
        data = self.__datatoparse(data)
        headers = self.__headers
        headers['origin'] = 'https://www.wenku8.cc'
        headers['referer'] = 'https://www.wenku8.cc/modules/article/search.php?'
        headers['content-type'] = 'application/x-www-form-urlencoded'
        r = requests.post(url=url,headers=headers,data=data,cookies=self.__cookies,timeout=(5, 20))
        if r.status_code == 200:
            r.encoding = "gbk"
            if 'search' in r.url:#如果有多个结果或者压根没搜到
                element:etree._Element = etree.HTML(r.text,etree.HTMLParser())
                rst1:List[etree._Element] = element.xpath("/html/body/div[@class='main'][2]/div[@id='centerm']/div[@id='content']/table[@class='grid']/tr/td/div")
                max_page = element.xpath("/html/body/div[@class='main'][2]/div[@id='centerm']/div[@id='content']/div[@class='pages']/div[@id='pagelink']/a[@class='last']/text()")[0]
                alist = []
                for i in rst1:
                    rst2_title = i.xpath("./div[2]/b/a/text()")[0]
                    rst2_url = i.xpath("./div[2]/b/a/@href")[0]
                    alist.append([rst2_title,rst2_url])
                return [int(max_page),alist,pagenum]
            else:
                element:etree._Element = etree.HTML(r.text,etree.HTMLParser())
                rst1_title = element.xpath("/html/body/div[@class='main'][2]/div[@id='centerl']/div[@id='content']/div[1]/table[1]/tr[1]/td/table/tr/td[1]/span/b/text()")[0]
                return [1,[[rst1_title,r.url]],pagenum]
        else:
            display_message(r.status_code,color=Fore.RED)
        return [1,[[]],1]
    
    def __downbook(self,bookid:int=3670,bookname='不和双胞胎一起『谈恋爱』吗？',downtype:int=0) -> bool:
        #如果选择模式1
        a = {'aid':bookid,'lang':0}
        bookchapt = WenkuAndoridAPi.getNovelIndex(details=a)
        chaptidlist = bookchapt.keys()
        if downtype:
            #好消息 起码书名不用和谐了 原汁原味 发现和之前要的数据结构 冲突的不行 人麻了
            for i in chaptidlist:
                chaptname:str = bookchapt[i]['title']#小说卷名 i chapt_id
                detailed:dict = bookchapt[i]['data']
                for j in detailed.keys():# j 小节名 detailed[j] 这才是chapter_id
                    self.__getcontent(bookid=bookid,bookname=bookname,chapterid=int(detailed[j]),chaptername=j)
            return
        #理想模式里提供两种方式 分卷 或者 整本下载 先做分卷吧 不过我就做简体 繁体 欸我直接不写
        urllist = ['https://dl1.wenku8.com/packtxt.php?','https://dl2.wenku8.com/packtxt.php?','https://dl3.wenku8.com/packtxt.php?']
        bookname = re.sub(r'[\\/:*?"<>|]','_',bookname)
        if not os.path.exists(self.__filename+bookname+'/'):
            os.mkdir(self.__filename+bookname+'/')
        self.Pool = WenkuPool(bookname)
        for i in chaptidlist:#小说卷 名字
            chaptname:str = bookchapt[i]['title']
            chaptname = re.sub(r'[\\/:*?"<>|]','_',chaptname)
            if not os.path.exists(self.__filename+bookname+'/'+chaptname):
                os.mkdir(self.__filename+bookname+'/'+chaptname)#./book/Re_/第一卷
            for index in range(3):
                url = urllist[index]+'aid={}&vid={}&charset=utf-8'.format(bookid,i)
                try:
                    res = requests.get(url=url,headers=self.__headers)
                    if res.status_code == 200:
                        with open(self.__filename+bookname+'/'+chaptname+'/'+chaptname+'.txt','wb') as f:#他们表面说utf-8 实际早早用上utf-16 奇怪表情太多了
                            f.write(res.content)
                    else:
                        display_message(res.status_code,color=Fore.RED)
                except Exception as e:
                    print(e)
                else:
                    print(Fore.GREEN+chaptname,Fore.BLUE+i)
                    break
            detailed:dict = bookchapt[i]['data']
            if '插图' in detailed.keys():
                self.__downimg(bookid=bookid,imgurl=int(detailed['插图']),chaptname=chaptname)
            

    def __downimg(self,bookid:int=1861,imgurl:int=65640,chaptname:str='第一卷'):
        #想起了这小说网站 有些小节后面也会跟图片 这个效果只能说很差
        a = {'aid':bookid,'cid':imgurl,'lang':0}
        imglist = WenkuAndoridAPi.getNovelContent(details=a,texttype=1)
        self.Pool.done(chaptname,imglist)
        display_message(chaptname+' 下载完成',Fore.GREEN)
        return True

    def __getcontent(self,bookid:int=0,bookname:str='',chapterid:int=0,chaptername:str=''):
        a = {'aid':bookid,'cid':chapterid,'lang':0}
        content =  WenkuAndoridAPi.getNovelContent(details=a,texttype=0)
        insert(bookid=bookid,bookname=bookname,chapterid=chapterid,chaptername=chaptername,chaptertext=content)
        display_message(chaptername+' 下载完成',Fore.GREEN)
        return True

# @dataclasses.dataclass
class WenkuAndoridAPi():
    __header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; unknown Build/NZH54D)',
    }
    def __encode(self,s:str):
        s = bytes(s,encoding="utf-8")
        a = base64.b64encode(s)#btoa(str) base64 to ASCII
        a = a.decode("utf-8")
        return '&appver=1.13&request=' + str(a) + '&timetoken=' + str(int(time.time() * 1000))#1718874662575
    
    def __apirequest(self,details):
        data = self.__encode(details)
        r = requests.post(url='http://app.wenku8.com/android.php',headers=self.__header,data=data,timeout=(5, 20))
        if r.status_code == 200:
            return r.text
        
    @classmethod 
    def getNovelIndex(cls,details:dict[str:str]) ->dict:
        '''
        在想返回数据类型的时候 算了内部用用dict 就好 转换来转换去的干什么
        {
            id1:{
                title:'title1',
                data:{
                    subtitle1:id1,subtitle2:id2
                }
            },
            id2:{
                title:'title2'
            }
        }
        '''
        aid = details['aid']    
        lang = details['lang']
        url = 'action=book&do=list&aid=' + str(aid) + '&t=' + str(lang)
        r = cls().__apirequest(url)
        ru_8 = bytes(r,encoding='utf-8')#lxml 不支持解析带有encoding 声明的字符串 所以要先转换从byte
        tree:etree._Element = etree.XML(ru_8,etree.XMLParser())
        root = tree.xpath("/package/volume")
        adict = {}
        for i in root:
            i:etree._Element
            # print(i.xpath("./@vid")[0],i.text.replace('\n', '').replace('\r', ''))#这一步拿到 每一卷的id 和 卷名
            juanid = str(i.xpath("./@vid")[0])
            adict[juanid] = {'title':i.text.replace('\n', '').replace('\r', ''),'data':{}}
            temp = i.xpath("./chapter")
            for j in temp:
                j:etree._Element
                # print(j.xpath("./@cid")[0],j.text)
                jieid = str(j.xpath("./@cid")[0])
                adict[juanid]['data'][j.text] = jieid
        return adict

    @classmethod
    def getNovelContent(cls,details:dict[str:str],texttype=0) ->list:
        aid = details['aid']    
        cid = details['cid']
        lang = details['lang']
        url = 'action=book&do=text&aid=' + str(aid) + '&cid=' + str(cid) + '&t=' + str(lang)
        r = cls().__apirequest(url)
        if texttype:
            pattern = re.compile(r"<!--image-->(https?:[^<>]+)<!--image-->")
            findobj = pattern.findall(r)
        else:
            # findobj = r.splitlines()#文字版本
            findobj = r#原谅我直接返回str
        return findobj




        
if __name__ == "__main__":
    W = wenku()
    # 输入关键词就可以搜索了 如果要你登录 就登录 这cookie维持时间只能说超乎想象
    # 如果精准匹配到了 就会自动下载 没有匹配到 就自己选选
    W.searchbook(searchkey='反派富二代',downtype=1)

    # b= {'aid':3686,'cid':154166,'lang':0 }
    # b = {'aid':3686,'lang':0}
    # print(WenkuAndoridAPi.getNovelIndex(b))
    # d = WenkuAndoridAPi.getNovelContent(b)
    # W.insert_book(3687,'反派富二代充满误会的圣者生活～第二次人生明明只想随心所欲度过～',154166,d)
