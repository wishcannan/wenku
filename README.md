# wenku
实现了登录 也就是cookie交换
图片，文本写入


#2021.12.27 
今天要实现一下 搜索功能 并尝试 线程下载 和 错误存储 以及 修复一下 有人喜欢在文章里面放图片 这种缺心眼的事

#2021.12.29
前面说的那么好 实际实现起来 有点难
1，这个网站 使用什么排序呀 搜索功能必须登录(有点抠门) 这就使我不得不先解决cookie问题 经过一番实验 确定了使用的cookie 使用RequestsCookieJar模块 来便于调用
也写了存储cookie的方式 不过在程序中默认保存一天有点不适用我做实验(其实就是脑死 没有想到如何验证cookie是否生效 写这个的时候已经想到了 就是直接访问私人页面
不禁止重定向 这样失效的话 会跳转的登录页面 然后验证请求的网址就是了)
2,实现图片下载 在文章中这件事其实也算是实现了 不过不能控制空文章写入 应该给他添个get_text是否为空试一试的 避免出问题(顺便优化了之前额外访问网址次数，以及会跳过有内容章节的bug)
3，线程下载没做 因为这次下载部分代码是从上次里面扣下来的 简单来说就是没写 
4，我发现站长还是做出了一些改动 只能说别改了 如果这个被站长看到了 维护起来真的很难 我一年也看不了几本 也不想全部爬下来用来盈利什么的就是私人看看
5，这gbk网站参数真的阴间
6，搜索没做完 也没有做榜单功能 下次一定(搜索现在只支持精准匹配小说名，匹配作者也没有做)
7，如果发现cookie问题报错 起码自己登录一下哦 这个下次一定

#2022.1.5
今天修复不能下载多个搜索结果的问题 还有翻页问题没有解决
图片章 依旧没有添加检索为空的方法
写了一个可以检测cookie是否有效的方法 适用后发现cookie不过期 

#2022.1.6
今天修复会有空章的情况 也就是插图集 运用了isspace()虽然是常见方法 出奇意料的是没有什么特殊符号
今天还有修复以前不知道顺序问题 在每一章 的每一小节前面添加了 顺序
准备后面实现一些对排行表的查询以及 实现查询的翻页
