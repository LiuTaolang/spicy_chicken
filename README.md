## 0. 立项缘由
读到公众号“ETF拯救世界”的一篇文章[不死品种的极限跌幅](https://mp.weixin.qq.com/s/-wD8L9xjdBb_9wcRE76gNQ)，因此想监测所有的指数基金涨跌幅。天天基金网或者晨星基金网的筛选工具，一是不能根据跌幅排名，二是QDII里的基金难以批量筛选指数型基金。如果能够自动抓取历史数据并保存到本地，判断历史最高点至当前跌幅，那么当跌到70%、80%就能及时获取到信息。

## 1. 功能设计
spicy chicken是个独立的软件，点开以后图形界面展示菜单栏和实时净值表。

### 1.1 菜单栏
菜单栏功能按钮：
* 刷新：即更新所有指数基金数据，跌幅前十将展示在“实际净值表”中。
* 关于spicy chicken：对这个软件做一些介绍，放上项目地址和作者，反馈联系邮箱，版本（点击则检查更新）。

### 1.2 实时净值表
列表形式展示跌幅前十的指数基金。展示的字段：基金代码（链接天天基金网页）、基金名称、当前净值、对比上一交易日涨跌幅、对比历史最高点跌幅、与历史最高点天数差。

## 2. 开发设计
以下是项目开发的结构说明，辅助一些参考资料

### 2.1 网页爬取

#### 2.1.1 网页爬取模块分解

##### 2.1.1.1 爬虫功能
* 所有境内基金的代码获取
* 指数基金的判别
* 基金历史净值的获取

##### 2.1.1.2 与数据库管理模块的交互
* 根据数据库管理模块的读写接口，获取本地数据或者写入爬取、清洗后的数据。
* 根据数据库记录，判断要全量获取还是增量获取，全量获取为初始化时使用。增量获取则根据数据库中最后一次的数据日期与当前日期的差值，获取增量部分。

##### 2.1.1.3 与 GUI 模块的信息交互
* 用户在 GUI 界面点击刷新，则触发爬虫本模块运行。

#### 2.1.2 网页爬取相关的书|教程
* Chapter 12 web Scraping of [Automate The Boring Stuff With Python](https://book.douban.com/subject/26284938/)
* [阿里云学习中心-Python爬虫实战](https://developer.aliyun.com/learning/course/555?spm=a2c6h.13148508.0.0.15bb4f0e1EVMAK)
* [哔哩哔哩-Python数据分析教程：天天基金整站数据分析，教你如何理财！](https://www.bilibili.com/video/BV1Ty4y1n7Ak?from=search&seid=8952173057990536557&spm_id_from=333.337.0.0)

### 2.2 数据库管理

#### 2.2.1 数据存储
* 数据库选型？用 sqlite 还是 MySQL，或者其它？
* 数据库表设计。

#### 2.2.2 与网页爬取模块的交互
* 网页爬取模块如何传输数据过来？json？Excel？CSV？要结合基金净值数据定下传输格式。
* 注意数据写入效率

#### 2.2.3 与GUI模块的交互
* GUI模块要展示的字段，得先计算出来保存在数据库中。用户打开时，数据库模块直接把相应数据传给 GUI，减少用户等待时间。
* 跌幅计算
* 跌幅排序

#### 2.2.4 数据库管理相关的教程
* 哔哩哔哩搜“Python 数据库"，“Python sqlite”，“Python MySQL”
* 排序会用到算法，参考[算法图解](https://weread.qq.com/web/reader/fbf32b80715c0184fbff41f)

### 2.3 GUI界面
这款软件的颜值担当

#### 2.3.1 界面上的菜单
这个在功能设计模块有说明，暂时就这些。

#### 2.3.2 与网页爬取模块的交互
依网页爬取模块需要的参数来设计调用。

#### 2.3.3 与数据库管理模块的交互
目前的 GUI 界面只有列表式展示。绘图式展示还没设想，暂时在基金代码上放链接，要能够呼出默认浏览器跳转打开天天基金的详情页。

#### 2.3.4 GUI相关的教程
哔哩哔哩搜“Python 图形开发”

## 3. 协作

### 3.1 git 版本控制
利用 github 远程仓库协作，每个模块的每个细分功能都可以单独构思逻辑并测试，最后根据数据格式调整实现。git 版本控制教程参考[阿里云学习中心-Git基础入门到实战详解](https://developer.aliyun.com/learning/course/714?spm=a2c6h.13148508.0.0.46524f0er4kg72)。

### 3.2 项目地址
学完此 git 教程后，可以把 ssh 公钥文件发给 jayer.ltl@outlook.com，邮件标题注明“spicy_chicken：你的名字的公钥”。克隆项目地址，ssh方式：git@github.com:LiuTaolang/spicy_chicken.git

### 3.3 模块名称
不同的模块使用不同的分支名称，最终合并到主分支（main）。开发相应模块的功能时，应将分支选中为对应的分支名称，以免错乱。
* 网页爬取模块：scratch_web
* 数据库管理模块：db_management
* 图形界面：gui

先切换 checkout 到对应的分支，再 push 到远程仓库。首次 push 到对应的模块，命令执行如下：
```
git push --set-upstream origin scratch_web #提交到网页爬取模块分支
git push --set-upstream origin db_management #提交到数据管理模块分支
git push --set-upstream origin gui #提交到图形界面模块分支
```



## 附录
### git 指令

```
git config --global user.name 'name' //配置用户名
git config --global user.email 'email@address' //配置邮箱
ssh-keygen -t rsa -C 'emial@address' //生成ssh密钥文件
git status //查看状态
git add . //将工作区变更压入暂存区
git commit -m 'comment' //将暂存区内容提交至仓库
git log --pretty=oneline //单行显示日志
git reset --hard 'commit id' //回退到某个版本
git reflog //为了从过去版本切回最新版本，需要使用此命令查看历史的commit id
git clone 网址 //从线上克隆项目到本地
git push //将本地的变更提交至线上
git pull //将线上的变更拉取到本地
git branch //查看分支
git branch 分支名 //创建分支
git branch -d 分支名 //删除分支
git checkout 分支名 //切换分支
git checkout -b 分支名 //创建一个新的分支并切换过去
git merge 被合并的分支名 //合并分支
touch .gitignore //创建忽略文件，文件里编写要忽略的规则。
```

### git忽略规则

```
#在 .gitignore中按以下规则编写

/directory/ #过滤整个目录及子目录

*.zip #过滤所有 .zip 文件

/directory/file.py #过滤某个具体文件

!index.php #不过滤某个具体文件
```