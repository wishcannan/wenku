
---

# 前言
直接面对[轻小说文库](https://wenku8.com)的爬虫 多线程还没有写 所以如果爬很长的小说 会因为下载图片 等待好久

---

# 如何使用
## 1.引入库
代码如下（示例）：

```c
pip3 install -r requirements.txt
```

## 2.开始下载
代码如下（示例）：
wenku.py
```c
if __name__ == "__main__":
    W = wenku()
    # 输入关键词就可以搜索了 如果要你登录 就登录 这cookie维持时间只能说超乎想象
    # 如果精准匹配到了 就会自动下载 没有匹配到 就自己选选
    W.searchbook(searchkey='从零开始的异世界生活')
```


---

# 总结
坏了 写到这里才发现 想写的都没写 比如根据小节cid 配合aid 下载 不过其实已经实现了(看WenkuAndoridAPi里面就知道) 多线程也没写好遗憾 原本准备搭配pyttsx3读文的 写了但是有点丑陋 想好了怎么使用再安排上吧 这一次比上一次 成功的地方在于使用了他们android端api 获取到了被隐藏的小说内容 也能正确获取到page实现翻页功能 还是比较好的

24.6.30多线程上线了 图片果真是最需要多线程的地方 这样就快多了 想安排database 来存取了 以前是这么做过的 不过这次在本地试一试

24.7.4就结论而言 数据库结构 如果只想使用一张表的情况下 还是太难 想法能让每次运行就能自动检查是否有中途插入新的章节 并自动录入 还保持顺序 难道真的要用到三表 联查 