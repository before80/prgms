+++
title = "第24章 数据爬取"
weight = 240
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十四章：数据爬取——让程序替你"逛街"

想象一下：你想获取某个网站上成千上万的商品信息、价格变化、新闻更新……用手一行行复制粘贴？先不说你的手指会不会"罢工"，光是时间成本就让人想躺平。数据爬取，就是让程序替你完成这种"重复劳动"，速度可以是人类的千百倍，而且程序不会抱怨、不会请假、不会偷偷刷短视频摸鱼。

这一章，我们会玩转三个"爬虫神器"：

- **Scrapy**：爬虫界的"全能冠军"，工业级框架，适合大型项目
- **Selenium**：浏览器自动化工具，专门对付那些"JavaScript渲染"的懒癌网站
- **Playwright**：微软出品的现代化浏览器自动化工具，比Selenium更年轻更帅气

> 💡 **爬虫是什么？** 爬虫（Spider/Crawler）是一种自动浏览网页、抓取数据的程序。类比一下：它就像一只勤快的小蜘蛛，沿着网页的蛛丝（链接）四处爬动，把路过地方的"猎物"（数据）一网打尽。

---

## 24.1 Scrapy（全功能爬虫框架）

Scrapy 是 Python 爬虫领域的"老大哥"，功能全面、性能强劲、被业界广泛使用。它不仅仅是"发请求+拿网页"那么简单，还自带请求调度、数据管道、中间件扩展……一套完整的爬虫"生态系统"。

### 24.1.1 项目结构与 Spider 编写

Scrapy 的项目结构清晰明了，每个文件各司其职，就像一个分工明确的工厂流水线。

```bash
# 安装 Scrapy
pip install scrapy

# 创建一个新项目
scrapy startproject myproject
```

项目创建完成后，你会得到这样的目录结构：

```mermaid
graph LR
    A[scrapy.cfg<br/>配置文件] --> B[myproject/]
    B --> C[__init__.py]
    B --> D[items.py<br/>定义数据结构]
    B --> E[middlewares.py<br/>中间件]
    B --> F[pipelines.py<br/>数据管道]
    B --> G[spiders/]
    G --> H[__init__.py]
    G --> I[quote_spider.py<br/>爬虫主体]
```

> 📁 **spiders/** 文件夹是你的"蜘蛛"们住的地方。每个 spider（爬虫）就是一个 Python 类，负责定义"去哪儿爬"和"怎么爬"。

来看一个最简单的 Scrapy Spider：

```python
# -*- coding: utf-8 -*-
# 文件：myproject/myproject/spiders/quote_spider.py

import scrapy


class QuoteSpider(scrapy.Spider):
    # 爬虫的唯一标识名称，启动时用
    name = "quotes"
    
    # 允许爬取的域名范围，防止爬出界（像个有礼貌的蜘蛛）
    allowed_domains = ["quotes.toscrape.com"]
    
    # 起始URL列表，蜘蛛从这里出发
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):
        """
        解析函数：response 是请求返回的网页内容
        Scrapy 会自动把 HTML 解析好传给你
        """
        # 提取所有名言的容器
        for quote in response.css("div.quote"):
            yield {
                # css 选择器：取出文本内容，strip() 去掉首尾空格
                "text": quote.css("span.text::text").get().strip(),
                "author": quote.css("span small::text").get().strip(),
                # 获取标签列表，用逗号连接
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        # 翻页：找到"下一页"的链接，继续爬！
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            # 构造完整的绝对URL，然后扔给 Scrapy 调度器
            yield response.follow(next_page, callback=self.parse)
```

启动这只蜘蛛：

```bash
# 在项目根目录运行
cd myproject
scrapy crawl quotes
```

你将看到控制台疯狂滚动输出抓取到的名言数据，格式大概是：

```python
{'text': '"The world as we have created it...", 'author': 'Albert Einstein', 'tags': ['change', 'deep-thoughts']}
{'text': '"It is our choices...', 'author': 'J.K. Rowling', 'tags': ['abilities', 'choices']}
```

> 🕷️ **为什么叫 `yield` 而不是 `return`？** yield 是"生成器"语法，它像流水线上的传送带，一边抓一边吐，不会把所有数据堆在内存里才放行。适合处理海量数据，内存友好。

### 24.1.2 Item 与 Item Pipeline

**Item** 是 Scrapy 中用来定义"数据结构"的类，就像数据库的表结构一样——你告诉 Scrapy："我要爬的每一条数据，长这样。"

```python
# -*- coding: utf-8 -*-
# 文件：myproject/myproject/items.py

import scrapy


class BookItem(scrapy.Item):
    # 定义字段，有点像字典但更规范，有提示功能
    title = scrapy.Field()        # 书名
    price = scrapy.Field()        # 价格
    author = scrapy.Field()      # 作者
    rating = scrapy.Field()       # 评分（1-5星）
    availability = scrapy.Field() # 库存状态
```

在 Spider 中使用：

```python
from myproject.items import BookItem

class BookSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            item = BookItem()
            item["title"] = book.css("h3 a::attr(title)").get()
            item["price"] = book.css("p.price_color::text").get()
            # 星级评分通过 class 名来获取，比如 "star-rating Three"
            item["rating"] = book.css("p.star-rating::attr(class)").re_first(r"star-rating (\w+)")
            item["availability"] = book.css("p.instock::text").getall()[-1].strip()
            yield item
```

---

**Pipeline（管道）** 是数据处理流水线。当你 `yield` 出一个 Item，它会流经一系列 Pipeline 进行清洗、验证、存储。

> 🔗 **Pipeline 是什么？** 想象工厂流水线上的质检员、包装工、发货员——Pipeline 就是每个"处理步骤"。Scrapy 默认不给配任何 Pipeline，你需要自己写。

一个典型的 Pipeline 示例：

```python
# -*- coding: utf-8 -*-
# 文件：myproject/myproject/pipelines.py

import json
import re

from scrapy.exceptions import DropItem


class PriceValidationPipeline:
    """清理价格数据，移除货币符号，保留数字"""

    def process_item(self, item, spider):
        if "price" in item and item["price"]:
            # 把 "£51.77" 变成 51.77
            item["price"] = float(re.sub(r"[^\d.]", "", item["price"]))
        return item


class DuplicatesPipeline:
    """去重Pipeline：记录已爬过的URL"""

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        # 用 title 作为去重依据
        if item.get("title") in self.urls_seen:
            spider.logger.warning(f"重复数据丢弃: {item['title']}")
            # drop_item() 会直接丢弃这个 item
            raise DropItem(f"重复: {item['title']}")
        self.urls_seen.add(item.get("title"))
        return item


class JsonExportPipeline:
    """把数据写入 JSON 文件"""

    def __init__(self):
        self.file = open("books.jl", "w", encoding="utf-8")

    def close_spider(self, spider):
        # 爬虫结束时自动调用，关闭文件
        self.file.close()

    def process_item(self, item, spider):
        # 写成 JSON Lines 格式（每行一个JSON，方便流式处理）
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
```

别忘了在 `settings.py` 中启用 Pipeline：

```python
# 启用 Pipeline，数字越小优先级越高
ITEM_PIPELINES = {
    "myproject.pipelines.PriceValidationPipeline": 100,
    "myproject.pipelines.DuplicatesPipeline": 200,
    "myproject.pipelines.JsonExportPipeline": 300,
}
```

> 💡 **为什么 Pipeline 有顺序？** 就像做菜：先洗菜(100)，再切菜(200)，最后炒菜(300)。数字小的先执行。如果顺序搞反了（比如先炒菜再洗菜）……祝你好运。

### 24.1.3 请求与响应

Scrapy 的请求/响应机制是整个框架的核心。它使用了 Twisted 异步网络库，可以并发发出大量请求，效率极高。

**发送请求的方式：**

```python
# -*- coding: utf-8 -*-

import scrapy


class DetailSpider(scrapy.Spider):
    name = "detail"

    def start_requests(self):
        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3",
        ]
        for url in urls:
            # 手动构造请求，可以指定爬取方式(GET/POST)、headers、cookies等
            yield scrapy.Request(
                url=url,
                callback=self.parse_detail,
                headers={"User-Agent": "Mozilla/5.0"},  # 假装自己是浏览器
                cookies={"session_id": "abc123"},        # 带上Cookie
                meta={"dont_merge_cookies": True},       # True: 本次请求的Cookie不与之前响应中的Cookie合并
            )

    def parse_detail(self, response):
        # response 是 Scrapy 为你封装好的响应对象
        print(f"状态码: {response.status}")           # 200
        print(f"当前URL: {response.url}")             # 可能因为重定向变了
        print(f"原始URL: {response.request.url}")     # 请求时的URL（与当前URL可能不同）

        # CSS 选择器（最常用，上手快）
        title = response.css("h1.title::text").get()

        # XPath（更灵活，适合复杂场景）
        description = response.xpath('//div[@id="desc"]/p/text()').get()

        # re 方法：正则提取
        price = response.css("span.price::text").re_first(r"[\d.]+")

        yield {
            "title": title,
            "description": description,
            "price": price,
        }
```

**POST 请求：**

```python
# 模拟表单提交
yield scrapy.FormRequest(
    url="https://example.com/login",
    formdata={"username": "admin", "password": "123456"},
    callback=self.after_login,
)

def after_login(self, response):
    # 登录后检查是否成功
    if "登录成功" in response.text:
        self.log("登录成功！")
```

**response 常用方法速查：**

| 方法 | 作用 |
|------|------|
| `response.css("selector")` | CSS选择器，返回 SelectorList |
| `response.xpath("xpath")` | XPath选择器，返回 SelectorList |
| `response.get()` / `response.getall()` | 获取第一个 / 所有结果 |
| `response.follow()` / `response.follow_all()` | 自动补全相对链接为绝对链接 |
| `response.json()` | 把响应体当作 JSON 解析 |

> 🎯 **CSS vs XPath 怎么选？** 新手建议先用 CSS selector，简单直观。如果遇到嵌套很深的结构，或者需要"选择父节点"、"选择第N个"这种操作，再祭出 XPath。两者可以混用，Scrapy 都支持。

### 24.1.4 中间件

Scrapy 的中间件（Middleware）分为两种：**下载器中间件（Downloader Middleware）** 和 **爬虫中间件（Spider Middleware）**。它们像两层"安检关卡"，可以拦截进出的请求和响应，进行修改、增强或拦截。

```mermaid
graph LR
    A[Spider 生成请求] --> B[Spider Middleware<br/>进]
    B --> C[Scheduler<br/>请求队列]
    C --> D[Downloader Middleware<br/>进]
    D --> E[互联网]
    E --> D2[Downloader Middleware<br/>出]
    D2 --> C2[Scheduler]
    C2 --> B2[Spider Middleware<br/>出]
    B2 --> F[Spider parse()]
```

**下载器中间件实战：随机User-Agent**

```python
# -*- coding: utf-8 -*-
# 文件：myproject/myproject/middlewares.py

import random


class RandomUserAgentMiddleware:
    """每次请求随机换User-Agent，让网站以为是不同浏览器"""

    def __init__(self):
        # 一堆浏览器的身份列表
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Firefox/121.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) Mobile/15E148",
        ]

    def process_request(self, request, spider):
        """在请求发出去之前，修改请求头"""
        request.headers["User-Agent"] = random.choice(self.user_agents)


class ProxyMiddleware:
    """代理IP中间件，保护真实IP"""

    def process_request(self, request, spider):
        # 代理地址（示例，需要真实的代理服务）
        proxy = "http://user:password@proxy.example.com:8080"
        request.meta["proxy"] = proxy


class RetryMiddleware:
    """自动重试中间件，网络波动不慌张"""

    def __init__(self):
        self.max_retry_times = 3

    def process_response(self, request, response, spider):
        """如果返回的状态码不对劲，就重试"""
        if response.status in [500, 502, 503, 504, 408]:
            # 增加重试次数标记
            retry_times = request.meta.get("retry_times", 0) + 1
            if retry_times <= self.max_retry_times:
                spider.logger.info(f"重试 {retry_times}/{self.max_retry_times}: {request.url}")
                # 重新扔回调度器
                return request
        return response
```

启用中间件（在 `settings.py` 中）：

```python
DOWNLOADER_MIDDLEWARES = {
    "myproject.middlewares.RandomUserAgentMiddleware": 400,
    "myproject.middlewares.ProxyMiddleware": 410,
    "myproject.middlewares.RetryMiddleware": 420,
}
```

> ⚙️ **数字越小越先执行？** 不完全是！中间件的执行顺序是：根据优先级数字，**先从小到大执行 Downloader 的 process_request**，然后**从大到小执行 Downloader 的 process_response**。所以 process_request 的顺序和 process_response 的顺序是**相反**的，很像"先进后出"的栈。

### 24.1.5 分布式爬虫（Scrapy-Redis）

单机爬虫的瓶颈在哪里？—— **带宽和IP**。当你要爬取千万级数据时，一台机器无论如何优化，请求速度都会碰到天花板。而且很多网站会封IP，单机作战分分钟被拉黑。

Scrapy-Redis 就是来解决这个问题的：它把 Scrapy 的调度器换成了 **Redis**，让你可以**多台机器同时爬、共同维护一个请求队列**，实现分布式！

> 🔑 **Redis 是什么？** Redis 是一个内存数据库，读写速度极快，常用于缓存、消息队列、排行榜等场景。这里用它来充当"任务协调中心"。

```bash
# 安装
pip install scrapy-redis
```

```mermaid
graph TB
    subgraph "机器A (Master)"
        A1[Scrapy Engine]
        A2[Scrapy-Redis<br/>Scheduler]
    end
    subgraph "机器B (Slave 1)"
        B1[Scrapy Engine]
        B2[Scrapy-Redis<br/>Scheduler]
    end
    subgraph "机器C (Slave 2)"
        C1[Scrapy Engine]
        C2[Scrapy-Redis<br/>Scheduler]
    end
    subgraph "Redis 服务器"
        R[(Redis<br/>请求队列)]
    end
    A2 --> R
    B2 --> R
    C2 --> R
```

**settings.py 配置（以 Redis 所在服务器 192.168.1.100 为例）：**

```python
# 使用 Redis 调度器替代默认的
SCHEDULER = "scrapy_redis.schedulers.Scheduler"

# 启用请求去重（不同机器爬同一URL不会重复）
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Redis 连接信息
REDIS_HOST = "192.168.1.100"
REDIS_PORT = 6379
REDIS_PASSWORD = "redis_password_here"

# 是否持久化请求队列（断电恢复）
SCHEDULER_PERSIST = True

# 每次请求之间的延迟（秒），避免请求过快被封
DOWNLOAD_DELAY = 0.5
```

**Spider 改造（机器B和C上运行的代码完全一样！）：**

```python
# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider


class DistributedImageSpider(RedisSpider):
    """分布式爬虫，从 Redis 队列里取任务"""
    name = "distributed_images"
    # allowed_domains 和 start_urls 可以不写
    # 因为任务是从 Redis 动态推送给各节点的

    def parse(self, response):
        for image_url in response.css("img::attr(src)").getall():
            yield {"image_url": image_url}
```

**Master 节点手动推送起始URL：**

```python
# 在 Redis 中执行命令，推送起始URL
# redis-cli
# redis> RPUSH myproject:start_urls https://example.com/gallery
```

或者写个脚本：

```python
import redis

r = redis.Redis(host="192.168.1.100", port=6379, password="redis_password_here")
r.rpush("myproject:start_urls", "https://example.com/page1")
r.rpush("myproject:start_urls", "https://example.com/page2")
r.rpush("myproject:start_urls", "https://example.com/page3")
```

> 🚀 **分布式爬虫的威力：** 假设你有 10 台机器，每台机器每秒爬 10 个页面，那每秒就是 100 个页面。一小时就是 36 万个页面！这速度，单机做梦都别想达到。

### 24.1.6 反爬与反反爬策略

爬虫和反爬虫就像猫鼠游戏，互相斗智斗勇。网站会想各种办法识别"程序"，我们也要想办法伪装。

**常见反爬手段：**

| 反爬手段 | 说明 | 反反爬策略 |
|---------|------|-----------|
| User-Agent 检测 | 识别非浏览器UA | 随机轮换真实UA |
| IP 频率限制 | 同一IP访问太快就封 | 代理IP池 + 降低请求频率 |
| Cookie/Session 追踪 | 检测是否浏览器行为 | 带上正常Cookie，定期更新 |
| 验证码（CAPTCHA） | 人机识别，比如图片选字 | 接入打码平台（花钱）或 OCR |
| JavaScript 渲染 | 数据靠JS动态生成 | Selenium/Playwright 渲染 |
| 加密参数 | 请求中带有签名/加密串 | 逆向JS代码破解加密逻辑 |
| 行为分析 | 检测访问模式（鼠标轨迹等） | 随机化请求间隔，模拟人类行为 |

> 🤖 **为什么网站要反爬？** 主要原因：防止数据被竞争对手抢走、减轻服务器压力、防止被恶意大量请求打挂网站、有些数据涉及版权或隐私。所以"能爬"不代表"应该爬"，请遵守 robots.txt 和相关法律法规。

**常用反反爬技巧：**

```python
# 1. 随机延时，假装人类在思考
import random
import time

def human_delay():
    time.sleep(random.uniform(1.0, 3.5))  # 1到3.5秒之间随机等

# 2. 伪造 Referer（防盗链检测）
yield scrapy.Request(
    url=image_url,
    headers={"Referer": "https://target-site.com/"},
)

# 3. 使用代理IP池（示例，需要真实代理服务）
class ProxyMiddleware:
    PROXY_LIST = [
        "http://1.2.3.4:8080",
        "http://5.6.7.8:8080",
        # ... 几十上百个代理
    ]

    def process_request(self, request, spider):
        proxy = random.choice(self.PROXY_LIST)
        request.meta["proxy"] = proxy
```

> ⚠️ **法律红线：** 违反网站 robots.txt 协议爬取数据可能违法；爬取个人信息、版权内容用于商业用途可能构成犯罪；攻击网站防护措施（如破解验证码）可能触犯《网络安全法》。爬虫有风险，使用需谨慎。

---

## 24.2 Selenium（浏览器自动化）

Scrapy 擅长"静态网页"——那些服务器直接返回完整HTML的网站。但现在越来越多的网站是"SPA"（单页应用）或用 JavaScript 动态渲染数据，你用 Scrapy 发请求拿到的可能是一片空白。

Selenium 就是来解决这个问题的：它**真正打开一个浏览器窗口**，像真人一样加载网页、执行JS、等待元素出现，然后你就可以"指点江山"了。

> 🌐 **Selenium 是什么？** 原本是用于 Web 应用自动化测试的工具，可以模拟用户在浏览器中的操作。后来被爬虫工程师们发现"嘿，这玩意可以用来执行JS啊"，于是就成了爬虫神器。

### 24.2.1 WebDriver 配置

Selenium 的核心是 WebDriver，它是一个浏览器驱动，用来控制浏览器行为。

```bash
# 安装 Selenium
pip install selenium

# 还需要下载对应浏览器的驱动程序
# Chrome:  chromedriver   (注意版本要和 Chrome 浏览器版本匹配！)
# Firefox: geckodriver
# Edge:    msedgedriver
```

```python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ------------------- 方式1：普通浏览器模式 -------------------
driver = webdriver.Chrome()

# 打开网页
driver.get("https://www.baidu.com")

# 获取页面标题
print(driver.title)  # 百度一下，你就知道

# 关闭浏览器
driver.quit()


# ------------------- 方式2：无头模式（推荐生产环境使用） -------------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # 不显示浏览器窗口
chrome_options.add_argument("--no-sandbox")  # Linux/Mac 需要加这个
chrome_options.add_argument("--disable-dev-shm-usage")  # 防止容器环境崩溃
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

# 也可以指定已安装的 Chrome 路径
chrome_options.binary_location = "/usr/bin/google-chrome"

service = Service("/path/to/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://example.com")
```

> 🖥️ **无头模式（Headless）** 就是不打开可见的浏览器窗口，后台静默运行。服务器上爬数据常用，省资源，速度也快。如果你想"看"到浏览器在干什么，用普通模式就好了。

**Firefox 配置示例：**

```python
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service

firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
firefox_options.set_preference("browser.download.folderList", 2)  # 下载到指定目录
firefox_options.set_preference("browser.download.dir", "/tmp/downloads")

service = Service("/path/to/geckodriver")
driver = webdriver.Firefox(service=service, options=firefox_options)
```

### 24.2.2 元素定位（ID / XPath / CSS Selector）

Selenium 提供了八种定位方式，按照"精准度"和"速度"来选：

```python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")

# 1. ID 定位（最快，因为 ID 唯一）
search_box = driver.find_element(By.ID, "kw")

# 2. Name 定位（次快，表单元素常用）
search_box = driver.find_element(By.NAME, "wd")

# 3. Class Name 定位（可能有多个同名 class）
button = driver.find_element(By.CLASS_NAME, "s_btn")

# 4. Tag Name 定位（不推荐，太宽泛）
first_div = driver.find_element(By.TAG_NAME, "div")

# 5. CSS Selector（灵活，语法类似前端开发）
logo = driver.find_element(By.CSS_SELECTOR, "#lg img")

# 6. XPath（最强大，适用所有场景，但写起来复杂一点）
link = driver.find_element(By.XPATH, '//a[@href="/about"]')
# 相对路径：从当前元素开始找
# link.find_element(By.XPATH, './span')

# 7. Link Text（专找链接，精确匹配）
news_link = driver.find_element(By.LINK_TEXT, "新闻")

# 8. Partial Link Text（链接文本包含某段文字）
news_link = driver.find_element(By.PARTIAL_LINK_TEXT, "新")

# 如果有多个匹配，返回列表（复数形式 find_elements）
all_links = driver.find_elements(By.TAG_NAME, "a")
for link in all_links:
    print(link.get_attribute("href"))
```

**XPath 高级用法：**

```python
# 文本内容定位（找"登录"按钮）
login_btn = driver.find_element(By.XPATH, '//button[text()="登录"]')

# 模糊匹配属性（class 包含 "primary"）
primary_btn = driver.find_element(By.XPATH, '//button[contains(@class, "primary")]')

# 组合定位：form 里找 name 为 "email" 的 input
email_input = driver.find_element(By.XPATH, '//form[@id="login"]//input[@name="email"]')

# 按索引取第3个 div
third_div = driver.find_element(By.XPATH, '//div[@class="container"]/div[3]')

# 父节点（用到 `..`）
parent = element.find_element(By.XPATH, "..")

# 轴定位：找包含 "密码" 文本的 td 的前一个同辈节点
prev = driver.find_element(By.XPATH, '//td[text()="密码"]/preceding-sibling::td')
```

> 🎯 **定位速度排序：** ID > Name > CSS Selector > XPath > Class Name > Tag Name。如果网页没有 ID 和 Name，别慌，CSS Selector 和 XPath 几乎能定位任何元素。

### 24.2.3 等待策略（显式等待 / 隐式等待）

这是 Selenium 里**最容易踩坑**的地方！很多人写的爬虫"找不到元素"，十有八九是等待策略没搞对。

> ⏱️ **为什么需要等待？** 网页是"异步加载"的——你点了一个按钮，服务器可能要等 2 秒才返回数据。如果代码不等，直接去拿，当然拿不到。就像点外卖，你不能还没等骑手接单就去门口等开饭。

**隐式等待（Implicit Wait）：** 全局设置，告诉浏览器"你去DOM里找，找不到就多等一会儿"。

```python
# 隐式等待：最多等 10 秒，每 0.5 秒查一次
driver.implicitly_wait(10)
```

> ⚠️ **隐式等待的坑：** 它对所有 `find_element` 调用都生效，但如果元素**根本不存在**（比如页面结构就错了），它等 10 秒后会抛异常。而且如果设置得太长，会拖慢整体速度。建议用隐式等待处理"加载延迟"，显式等待处理"特定元素"。

**显式等待（Explicit Wait）：** 精确等待某个条件满足再继续，更灵活，是生产环境的**首选**。

```python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://example.com")

# 显式等待：最多等 20 秒，每 0.5 秒检查一次
# 直到出现"提交"按钮就停止等待
wait = WebDriverWait(driver, timeout=20, poll_frequency=0.5)

submit_btn = wait.until(
    EC.presence_of_element_located((By.XPATH, '//button[@id="submit"]'))
)

print("按钮出现了！")
submit_btn.click()  # 点击它
```

**常用等待条件（expected_conditions）：**

| 条件 | 说明 |
|------|------|
| `EC.presence_of_element_located((By.ID, "id"))` | 元素出现在 DOM 中（可能不可见） |
| `EC.visibility_of_element_located((By.ID, "id"))` | 元素可见且有大小 |
| `EC.element_to_be_clickable((By.ID, "id"))` | 元素可见且可点击 |
| `EC.text_to_be_present_in_element((By.ID, "id"), "内容")` | 元素包含指定文本 |
| `EC.title_contains("标题")` | 页面标题包含某文字 |
| `EC.invisibility_of_element_located((By.ID, "id"))` | 元素消失 |
| `EC.frame_to_be_available_and_switch_to_it((By.ID, "frameId"))` | iframe 可用并切换 |
| `EC.alert_is_present()` | 出现弹窗/alert |

**自定义等待条件（更高级）：**

```python
# 等到某个元素包含"加载完成"文本
def wait_for_loading_complete(driver):
    element = driver.find_element(By.ID, "status")
    return "加载完成" in element.text

element = wait.until(wait_for_loading_complete)
```

> 🔥 **最佳实践：** 隐式等待设一个合理的全局值（5-10秒），然后在关键时刻用显式等待精确控制。不要混用太多，也不要到处滥用隐式等待。

### 24.2.4 无头浏览器模式

无头模式我们已经提过，这里再深入一点，看看有哪些实用的配置选项：

```python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_options = Options()

# ==================== 核心无头配置 ====================
chrome_options.add_argument("--headless")              # 无头模式
chrome_options.add_argument("--disable-gpu")           # 禁用GPU加速
chrome_options.add_argument("--window-size=1920,1080") # 虚拟窗口尺寸

# ==================== 实用参数 ====================
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 隐藏自动化特征
chrome_options.add_argument("--disable-infobars")      # 禁用"Chrome正受自动测试软件控制"提示
chrome_options.add_argument("--no-sandbox")            # 沙盒模式关闭
chrome_options.add_argument("--disable-dev-shm-usage")  # 避免内存溢出
chrome_options.add_argument("--disable-extensions")     # 禁用扩展
chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误

# ==================== 反检测配置 ====================
# 伪造真实的窗口对象（后面还有JS方案）
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# ==================== 用户数据目录（保持登录状态） ====================
# chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")

# ==================== 启动 ====================
service = Service("/path/to/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# 执行JS代码隐藏 webdriver 属性
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    """
})

driver.get("https://example.com")
```

### 24.2.5 反检测（stealth）

即使是无头浏览器，很多网站也能通过检测 `navigator.webdriver`、`Chrome runtime`、`automation` 等特征来识别 Selenium。stealth 就是专门干这事的库，让你的自动化脚本更像一个真实用户。

```bash
# 安装
pip install selenium-stealth
```

```python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

# Chrome 配置
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service("/path/to/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# 使用 stealth 伪装
stealth(
    driver,
    languages=["zh-CN", "zh", "en"],       # 浏览器语言
    vendor="Google Inc.",                   # 显卡供应商
    platform="Win32",                       # 操作系统
    webgl_vendor="Intel Inc.",               # WebGL 厂商
    renderer="Intel Iris OpenGL Engine",     # 渲染器
    fix_hairline=True,                      # 修复hairline边框问题
)

driver.get("https://example.com")
print("当前 URL:", driver.current_url)
print("页面标题:", driver.title)

driver.quit()
```

> 🎭 **stealth 原理是什么？** 它通过 CDP（Chrome DevTools Protocol）注入 JavaScript 代码，修改浏览器暴露给网页的各种属性。比如把 `navigator.webdriver` 改成 `undefined`，把真实的 GPU 信息塞进去，让你看起来就像一台真电脑在浏览网页。

**手动反检测（不依赖 stealth 库）：**

```python
# 执行一系列 CDP 命令，抹掉自动化痕迹
driver.execute_cdp_cmd("Network.setUserAgentOverride", {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
})

driver.execute_script("""
    // Object.defineProperty 篡改原生属性
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    
    // 删除 Chrome 属性
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
""")

# 伪造 Canvas 指纹（网站可能通过 Canvas 识别爬虫）
# 这个比较复杂，通常 stealth 已经帮你做了
```

---

## 24.3 Playwright（现代化浏览器自动化）

Playwright 是微软出品的新一代浏览器自动化框架（2020年发布），主打 **"一次编写，多浏览器运行"**、**内置等待机制**、**网络拦截**、**移动端模拟**等特性。相比 Selenium，Playwright 更年轻、更现代、更快更稳，社区活跃度近几年已经超过了 Selenium。

> 🏎️ **Playwright vs Selenium 怎么选？** Selenium 历史久，资料多；Playwright 速度更快、API 更优雅、内置等待更智能。如果是从头开始新项目，建议优先考虑 Playwright。如果要维护老项目，那还是 Selenium 吧。

### 24.3.1 安装与配置

```bash
# 安装 Playwright
pip install playwright

# 安装浏览器驱动（Playwright 会帮你下载 Chromium、Firefox、WebKit）
playwright install

# 如果遇到问题，也可以单独装
playwright install chromium
playwright install firefox
playwright install webkit
```

> 🌐 **Playwright 支持哪些浏览器？** Chromium（Chrome的开源兄弟）、Firefox、WebKit（Safari内核）。一次代码，可以跑在三个主流引擎上，这叫"跨浏览器测试"。

```python
# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

# ==================== 基本用法 ====================
with sync_playwright() as p:
    # 启动 Chromium（可以指定 headless=True 静默运行）
    browser = p.chromium.launch(headless=True)
    
    # 创建一个"上下文"（类似浏览器的一个独立会话）
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},  # 视口尺寸
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        locale="zh-CN",                              # 语言
        timezone_id="Asia/Shanghai",                # 时区
        geolocation={"latitude": 31.2304, "longitude": 121.4737},  # 地理位置
        permissions=["geolocation"],               # 授权地理位置
    )
    
    # 在上下文里打开一个页面（标签页）
    page = context.new_page()
    
    # 导航到网页
    page.goto("https://www.baidu.com")
    
    # 获取标题
    print(page.title())
    
    # 截图保存
    page.screenshot(path="baidu.png")
    
    # 关闭
    browser.close()


# ==================== 异步版本（配合 asyncio 使用） ====================
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        content = await page.content()
        print(content[:200])
        await browser.close()

asyncio.run(main())
```

### 24.3.2 元素定位与交互

Playwright 的定位 API 比 Selenium 更优雅，而且内置智能等待，不用你操心元素加载问题。

```python
# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # ==================== 定位元素 ====================
    # ID 定位（推荐，速度最快）
    search_box = page.locator("#kw")
    
    # 文本定位（非常直观）
    login_btn = page.get_by_text("登录")
    
    # 占位符文本定位（input 的 placeholder）
    email_input = page.get_by_placeholder("请输入邮箱")
    
    # 按标签和文本组合
    submit_btn = page.get_by_role("button", name="提交")
    
    # CSS Selector
    logo = page.locator("div.header img.logo")
    
    # XPath
    link = page.locator("xpath=//a[@href='/about']")
    
    # ==================== 交互操作 ====================
    page.goto("https://www.baidu.com")
    
    # 点击
    page.locator("#kw").fill("Python教程")  # 也可以直接填充文本
    page.locator("#su").click()             # 点击搜索按钮
    
    # 等待搜索结果加载（Playwright 会自动等元素出现）
    page.wait_for_selector("h3.t a", timeout=10000)
    
    # 获取搜索结果列表
    results = page.locator("h3.t a").all()
    for result in results:
        print(result.text_content())
    
    # ==================== 键盘和鼠标 ====================
    page.keyboard.press("Enter")           # 按回车
    page.keyboard.type("Hello World")      # 打字
    page.keyboard.press("Control+a")      # 全选
    
    page.mouse.click(100, 200)             # 鼠标点击坐标
    page.mouse.wheel(0, 300)               # 滚轮滚动
    
    # ==================== 下拉框 / Select ====================
    page.select_option("select#country", "China")  # 通过值选择
    page.select_option("select#country", label="中国")  # 通过文本选择
    
    # ==================== 文件上传 ====================
    page.set_input_files('input[type="file"]', "path/to/file.pdf")
    
    # ==================== 获取元素属性和文本 ====================
    link = page.locator("a.primary").first
    print(link.get_attribute("href"))     # 获取 href 属性
    print(link.text_content())             # 获取文本
    print(link.inner_html())               # 获取内部 HTML
    print(link.is_visible())               # 是否可见
    print(link.is_enabled())               # 是否可交互
    print(link.is_disabled())              # 是否禁用
```

**智能等待 vs 强制等待：**

Playwright 的"智能等待"是其最大亮点——它会**自动等待元素变为可操作状态**，不像 Selenium 那样需要你手动写一堆 `WebDriverWait`。

```python
# Playwright 自动等待，不需要额外写 wait
page.locator("#dynamic-content").click()  # 元素一出现就点

# 如果你想等某个条件
page.wait_for_url("**/success")           # 等 URL 变化
page.wait_for_load_state("networkidle")  # 等网络空闲（所有请求完成）
page.wait_for_function("() => window.innerWidth > 768")  # 等 JS 条件成立
```

> ⚡ **为什么 Playwright 不需要那么多 wait？** 因为它的底层架构更智能。Selenium 是"轮询 DOM"的方式等元素，而 Playwright 内部有动作验证机制（Actionability Checks），只有当元素真的"可交互"了才会执行下一步。

### 24.3.3 录制与回放

Playwright 有一个非常酷的功能：**codegen（代码生成器）**。你可以用 `playwright open` 命令打开浏览器，模拟操作，它会自动生成 Python 代码！

```bash
# 打开浏览器，进入录制模式
playwright codegen https://www.baidu.com

# 常用参数
# --target python  指定输出语言
# -o output.py    指定输出文件
playwright codegen --target python -o my_script.py https://www.baidu.com
```

```mermaid
graph LR
    A[打开浏览器<br/>浏览器窗口] --> B[你进行点击<br/>输入等操作]
    B --> C[Playwright 实时<br/>生成代码]
    C --> D[操作结束<br/>保存代码文件]
    D --> E[运行生成<br/>的脚本]
```

**回放（Replay）** 就是运行录制的脚本：

```bash
# 直接运行录制的脚本
python my_script.py

# 或者用 Playwright 的回放工具（主要用途是调试）
playwright show-trace trace.zip
```

> 🎬 **这个功能有什么用？** 对于不熟悉 Playwright API 的新手来说，先"录"一段，找到想要的元素和操作，然后把代码粘贴到自己的项目中修改。这比翻文档找 API 快多了。

### 24.3.4 移动端模拟

Playwright 原生支持移动端模拟，可以在电脑上模拟 iPhone、Android 手机的浏览器行为，包括**触摸手势**、**设备像素比（device pixel ratio）**、**UA**等。

```python
# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # ==================== iPhone 模拟 ====================
    # Playwright 内置了很多设备配置（iPhone、Galaxy 等）
    iphone = p.devices["iPhone 13 Pro"]
    
    context = p.chromium.launch(headless=True).new_context(
        **iphone,  # 自动设置 viewport、user_agent、device_scale_factor 等
    )
    page = context.new_page()
    
    page.goto("https://www.baidu.com")
    
    # 在手机上测试触摸手势
    page.touchscreen.tap(200, 300)  # 点击屏幕某处
    page.evaluate("window.scrollBy(0, 500)")  # 模拟滑动
    
    print(f"当前 UA: {page.evaluate('navigator.userAgent')}")
    print(f"视口: {page.viewport_size}")
    
    context.close()
```

**自定义移动端配置（不用预设设备）：**

```python
with p.chromium.launch(headless=True) as browser:
    context = browser.new_context(
        viewport={"width": 375, "height": 812},    # iPhone X 尺寸
        device_scale_factor=3,                       # 视网膜屏（3倍像素）
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        is_mobile=True,                             # 开启移动端模式
        has_touch=True,                             # 开启触摸支持
    )
    page = context.new_page()
    page.goto("https://www.baidu.com")
    
    # 移动端特有的手势
    page.touchscreen.tap(100, 200)  # 轻触
    
    # 模拟双指捏合缩放（通过两次点击无法真正实现，此处演示双击代替）
    page.mouse.click(200, 200)
    page.mouse.click(400, 400)

    context.close()
```

**同时测试多设备（响应式布局测试）：**

```python
with sync_playwright() as p:
    devices = ["iPhone 13", "Galaxy S21", "iPad Mini"]
    
    for device_name in devices:
        device = p.devices[device_name]
        context = p.chromium.launch().new_context(**device)
        page = context.new_page()
        
        page.goto("https://example.com/responsive")
        page.screenshot(path=f"screenshot_{device_name}.png")
        
        print(f"{device_name}: 视口 {device['viewport']}")
        context.close()
```

---

## 本章小结

这一章我们系统学习了 Python 数据爬取的三驾马车：

### Scrapy（全功能爬虫框架）
- **项目结构**：通过 `scrapy startproject` 创建工程，核心文件包括 `items.py`（数据结构）、`pipelines.py`（数据处理流水线）、`middlewares.py`（中间件）和 `spiders/` 目录下的爬虫文件
- **Spider 编写**：核心是 `parse()` 方法，使用 CSS Selector 或 XPath 提取数据，用 `yield` 逐条输出，支持自动翻页（`response.follow`）
- **Item 与 Pipeline**：Item 定义数据结构模板，Pipeline 负责数据清洗、验证、去重、持久化，支持多个 Pipeline 按优先级顺序串联
- **请求与响应**：`scrapy.Request` 支持 GET/POST、headers、cookies、meta；响应对象内置 `css()`、`xpath()`、`re()` 等解析方法
- **中间件**：下载器中间件和爬虫中间件组成双层关卡，可以实现 UA 轮换、代理IP、自动重试等功能
- **Scrapy-Redis**：通过 Redis 共享请求队列，实现多机分布式爬取，大幅提升爬取速度
- **反爬策略**：常见手段有 UA 检测、IP 限速、验证码、JS 渲染、行为分析等，对应策略包括随机UA、代理池、延时、OCR 识别、Selenium 辅助等

### Selenium（浏览器自动化）
- **WebDriver**：控制真实浏览器，需下载对应浏览器的驱动（chromedriver/geckodriver），支持普通模式和无头（headless）模式
- **元素定位**：八种定位方式（ID/Name/Class/Tag/CSS/XPath/Link Text/Partial Link Text），其中 ID 和 CSS Selector 最常用，XPath 最灵活
- **等待策略**：隐式等待（全局）配合显式等待（精确控制）是最佳实践；`WebDriverWait` + `expected_conditions` 是 Selenium 最标准的等待写法
- **无头模式**：通过 `--headless` 参数后台运行，配合 `--disable-gpu`、`--no-sandbox` 等参数优化
- **反检测**：网站会检测 `navigator.webdriver` 等自动化特征，使用 `selenium-stealth` 库或手动执行 CDP 命令可以有效伪装

### Playwright（现代化浏览器自动化）
- **安装配置**：`pip install playwright` + `playwright install` 自动安装三浏览器引擎；支持同步和异步两种 API
- **元素定位与交互**：API 更现代化，`.locator()` 是核心方法，支持文本定位、按角色定位等高级方式；内置智能等待，无需手动处理加载延迟
- **录制与回放**：`playwright codegen` 可以可视化录制操作并生成代码，大幅降低学习成本
- **移动端模拟**：内置 iPhone、Android 等设备配置，可模拟触摸手势、视口缩放、视网膜屏像素比等移动端特性

> 🧠 **工具选择建议**：小型爬虫、快速脚本 → Scrapy；需要 JS 渲染或复杂交互 → Playwright（优先）或 Selenium；分布式大规模爬取 → Scrapy + Scrapy-Redis；老项目维护 → Selenium。

**记住：爬虫是把双刃剑，用得不当会惹上官司。用好它，它就是数据分析、竞品监控、市场研究最强大的武器。** 🕷️
