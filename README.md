## 功能描述
读到公众号“ETF拯救世界”的一篇文章[不死品种的极限跌幅](https://mp.weixin.qq.com/s/-wD8L9xjdBb_9wcRE76gNQ)，因此想监测所有的指数基金涨跌幅。天天基金网或者晨星基金网的筛选工具，一是不能根据跌幅排名，二是QDII里的基金难以批量筛选指数型基金。如果能够自动抓取历史数据并保存到本地，判断历史最高点至当前跌幅，那么当跌到70%、80%就能及时获取到信息。

## 使用方法
### 创建 venv 虚拟环境并激活
```bash
$ mkdir spicy_chicken
$ cd spicy_chicken  # 创建、进入新文件夹
$ python3 -m venv sc_env    # 在新文件夹下创建虚拟环境
$ source sc_env/bin/activate # MacOS/Linux 下激活
$ ./sc_env/Scripts/activate # Windows 下激活
```
### 安装 akshare
```bash
$ pip3 install akshare
```

### 运行 example 脚本
```bash
$ python3 example.py
```

### 查阅 csv 文件
输出的 csv 文件（spicy_chicken.csv）按“当前价/历史最高价"的比值升序排列，最上面的就是跌得最狠的。

### 数据说明
基金代码包含在 A 股上市的 ETF、LOF、指数类公募基金、非指数类公募基金、场内交易基金（ETF 和 LOF 类没取全的基金代码）。ETF 和 LOF 类采用复权后数据，其他采用累计净值。