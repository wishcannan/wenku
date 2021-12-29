'''
    这次要更好 的使用 更棒的体验 对网站要有更透彻的分析

'''
import json
import requests
from requests.cookies import RequestsCookieJar
import requests.utils
import codecs
from bs4 import BeautifulSoup
import os
import re



class wenku():
    def __init__(self,uid=None,pwd=None) -> None:
        self.cookies = RequestsCookieJar()
        self.headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.uid = uid
        self.pwd = pwd
        proxy='127.0.0.1:1091' 
        self.proxies={
            'http':'http://'+proxy,
            'https':'https://'+proxy
        }
        self.filename = './book/'
        if not os.path.exists(self.filename):
            os.mkdir(self.filename)
        pass
    def response_text(self,url):
            """请求函数"""
            response = requests.get(url,headers=self.headers,cookies=self.cookies) # 发送请求带入cookies
            if response.status_code==200:
                response.encoding="gbk"
            result = response.text
            self.cookies.update(response.cookies) #更新cookies
            return result



    def login(self,uid=None,pwd=None,mode=86400):#mode 和上次一样 0浏览器进程 86400一天 当然还有其他的 这里我们默认一天
        #距离上次写这个登录怎么说呢 他们居然更新了 加了一个gbk的参数 万万没想到
        if not uid and not pwd:
            uid = self.uid
            pwd = self.pwd
            if not uid and pwd:
                print("你是不是有鬼 登录不给账号密码 等着报错吧")
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
        # self.cookies.update(self.cookies_read())#首先读取之前的cookie 
        #第一步 访问 这个登录页面 获取两个cookie
        login_url = 'https://www.wenku8.net/login.php'
        r = requests.get(login_url,headers=self.headers)
        self.cookies.update(r.cookies) #更新cookies
        # self.lookcookie(r.cookies)
        headers = self.headers
        headers['origin'] = 'https://www.wenku8.net'
        headers['referer'] = 'https://www.wenku8.net/login.php'
        login_r = requests.post(login_url,headers=headers,data=data,params=params,cookies=self.cookies)
        if login_r.status_code == 200:
            self.cookies.update(login_r.cookies)
            self.lookcookie(login_r.cookies)
            self.cookies_save(login_r.cookies)
        else:
            print('登录失败',login_r.status_code)

    def lookcookie(self,s):
        #方便我查看cookie s是cookie
        cookies_dict = requests.utils.dict_from_cookiejar(s)
        cookies_str = json.dumps(cookies_dict)#多重字典应该用dumps 不然会报错
        print("这次的cookie为:",cookies_str,'\n')
    
    def cookies_read(self,a):#a 是指文件名
        #读cookie用的 避免一直登录
        cookies_txt = open(a, 'r')
        cookies_dict = json.loads(cookies_txt.read())
        # print(cookies_dict)
        cookies = requests.utils.cookiejar_from_dict(cookies_dict)
        # print(cookies)
        return cookies
    
    def cookies_save(self,s):#s 是指cookie
        #人工储存cookie
        cookies_dict = requests.utils.dict_from_cookiejar(s)
        cookies_str = json.dumps(cookies_dict)
        with open ('cookies.txt','w+') as f:
            f.write(cookies_str)

    def cookies_stitching(self):
        #没什么主要实现一下 cookie的拼接
        wenku_cookie = json.loads(open("cookies2.txt",'r').read())
        login_cookie = json.loads(open("cookies.txt",'r').read())
        adict = dict(wenku_cookie,**login_cookie)
        adict = json.dumps(adict)
        with open('cookies.txt','w+') as f:
            f.write(adict)

    def bookcase(self):
        #没什么用就是看看我的书架
        headers = self.headers
        headers['referer'] = 'https://www.wenku8.net/index.php'
        bookcase_url = 'https://www.wenku8.net/modules/article/bookcase.php'
        r = requests.get(bookcase_url,headers=headers,cookies=self.cookies)
        if r.status_code == 200:
                r.encoding="gbk"
        result = r.text
        print(result)

    def searchbook(self,type='articlename',searchkey:str=None):#参数有articlename author
        #使用搜索功能一定要登录 不登陆就不行
        self.cookies.update(self.cookies_read('cookies.txt'))#首先读取之前的cookie 
        # data = {
        #     'searchtype':type,
        #     'searchkey':searchkey,
        #     'charset':'gbk',

        #     # 'action':'login',
        #     'submit':'&#160;搜&#160;&#160;索&#160;'#gbk的话%26%23160%3B%CB%D1%26%23160%3B%26%23160%3B%CB%F7%26%23160%3B
        # }
        headers = self.headers
        headers['origin'] = 'https://www.wenku8.net'
        headers['referer'] = 'https://www.wenku8.net/modules/article/search.php?searchtype=articlename&searchkey='
        #经过多次测试 正常传参 容易受到问题 没有细致研究 所以决定直接 编译网址
        '''
            这里还涉及到一个翻页问题 我试了试超过page页 都会自动到最后一页 所以呢
        '''
        searchkey = searchkey.encode("gbk")
        searchkey = str(searchkey).replace("\\x","%")
        searchkey = searchkey[2:-1]
        # print(searchkey)
        url = 'https://www.wenku8.net/modules/article/search.php?searchtype={}&searchkey={}'.format(type,searchkey)
        # print(url)

        # r = requests.post(search_url2,data=data,headers=headers,cookies=self.cookies,allow_redirects=True)
        r = requests.get(url,headers=headers,cookies=self.cookies)
        if r.status_code == 200:
            print(r.headers)
            r.encoding="gbk"
            print(r.text)
            # print(r.url)
            '''
                这里有问题 就是如果只有一个符合选项的 就会直接跳转到书页面 虽然方便爬取
                但是如果有多个匹配项 一则要翻页 二则要对网址正则匹配

            '''
            if r.url == 'https://www.wenku8.net/modules/article/search.php':
                #说明有多匹配项
                pass
            else:
                #直接执行下载
                self.getbook(r.url)
                pass
            #这里有些 要提到的搜作者 就很正常 原地址加载数据 如果搜小说名 就会看返回头 然后重定向 
        else:
            print('你还未登录')
            print(r.status_code)
            print(r.headers)

    def article(self):
        article_url = 'https://www.wenku8.net/modules/article/toplist.php'
        params = {
            'sotr':'anime'
        }
        r = requests.get(article_url,params=params)

    def getbook(self,bookurl):
        bookid = self.getbookid(bookurl)
        a = int(bookid // 1000)
        booknovel = "https://www.wenku8.net/novel/{}/{}/index.htm".format(a,bookid)
        print(booknovel+"这次要看的书")
        bookrespronse = requests.get(booknovel,headers=self.headers,cookies=self.cookies)
        bookrespronse.encoding = "gbk"
        soup = BeautifulSoup(bookrespronse.text,'html.parser')
        bookname = soup.find('div',id="title").string#获取标题
        print(bookname)
        if not os.path.exists(self.filename+bookname):
            os.mkdir(self.filename+bookname)
        #获取章节
        all_chapter = soup.find('table')
        # print('all_chapter',all_chapter)
        self.getchapter(all_chapter,bookname,bookid)



    def getbookid(self,s):
        return int(re.split('\W+',s)[-2])
    def getchapter(self,all_chapter,bookname,bookid):
        a = int(bookid // 1000)
        filename = self.filename + bookname + '/'
        filename1 = ''
        tr_list = all_chapter.find_all('tr')
        for i in tr_list:
            td_list = i.find_all('td')
            print('td_list',td_list)
            for j in td_list:
                # print(j['class'])
                if j['class'][0] == 'vcss':
                    # print(j.text)
                    filename1 = filename+j.string
                    if not os.path.exists(filename1):
                        os.mkdir(filename1)
                    continue
                else:
                    if j.a != None:
                        s = j.a['href'][:-4]
                        self.gettxt('https://www.wenku8.net/novel/{}/{}/{}.htm'.format(a,bookid,s),filename1)
        return

    def gettxt(self,url,filename):#获取章节内容并写入 
        a = self.response_text(url)
        soup = BeautifulSoup(a,'html.parser')
        chapter_title = soup.find('div',id='title').string
        soup1 = soup.find("div",id='content')
        for biv in soup1.find_all('div'):
            # print(str(biv))
            self.getimage(str(biv),filename)
            biv.decompose()
        for ul in soup1.find_all('ul'):
            ul.decompose()
        filename = filename + '/{}'.format(chapter_title)+'.txt'
        with open(filename,'w+',encoding="utf-8") as f:
            f.write(chapter_title)
            f.write(soup1.get_text())
        f.close()
        return chapter_title+'ok'
    
    def getimage(self,p_img,filename):
        pattern = r'href="(.*?)"'
        img_href = re.findall(pattern,p_img)[0]
        # print(img_href)
        # print(img_href)x
        # print(i.a.img['src'])
        self.saveimage(img_href,filename)
        return 'ok'


    def saveimage(self,url,filename):
        # os.chdir(filename)
        r = requests.get(url,headers=self.headers,cookies=self.cookies,timeout=100)
        p = re.split('\W+',url)
        file_path = filename + '/' + p[-2] + '.' + p[-1]
        with open(file_path,"wb") as f:
            f.write(r.content)
        f.close

W = wenku('cannan','memochou')
# W.login()
# W.cookies_stitching()
W.searchbook(searchkey='魔法使之夜')
# W.bookcase()
# W.gettxt('https://www.wenku8.net/novel/1/1973/74161.htm','./book')


