+++
title = "第26章 其他框架"
weight = 260
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十六章：Python 的 "十八般武艺"——框架大乱斗

> 📢 警告：前方高能！本章内容可能让你对 Python 的认知从"胶水语言"升级为"变形金刚"。阅读请系好安全带，系不上的请抓住你旁边的程序员。

欢迎来到 Python 宇宙的"复仇者联盟"！前面二十多章我们学的 Python 基础，就好像是学会了怎么组装乐高积木——现在，是时候看看这些积木能搭出什么样的大场面了！

Python 之所以能在江湖上呼风唤雨，靠的可不只是语法优雅（好吧，也可能就是语法优雅）。真正让它称霸武林的，是围绕它建立的那个庞大到离谱的框架生态。别人造个框架要三年，Python 社区一年能给你整出十个，还一个比一个能打。

这一章我们就来盘点一下 Python 世界里那些"不是框架我不玩"的狠角色：测试框架、游戏框架、GUI 框架、网络编程、ORM、HTTP 客户端、认证库……每一个拎出来都是一方霸主。准备好了吗？让我们开启这场"框架总动员"！

---

## 26.1 自动化测试（pytest / Selenium / Playwright）

### 测什么？测个寂寞？——自动化测试的重要性

你有没有过这种经历：写了一堆代码，自信满满地点运行，结果——"啊？报错了？"更可怕的是，你改了一个地方，惊喜地发现它不报错了，但同时另外三个地方开始报错。这就是没有测试的"快乐"（并不）。

**自动化测试** 就是你的代码保镖，7×24 小时盯着你的代码，一旦发现异常就立刻报警。它比你更早发现问题，比你更耐心重复测试，比你更不会忘记测试边界条件。

> 测试金字塔了解一下：**单元测试**（测最小单元）铺底，**集成测试**（测模块组合）居中，**端到端测试**（测整个系统）站塔尖。金字塔有多稳，就看你底打得有多牢。

### pytest——测试界的瑞士军刀

`pytest` 是 Python 测试框架中的"扛把子"，简单、强大、插件丰富，是目前最流行的测试框架。它的核心哲学是：**简单的事情简单做，复杂的事情有办法做**。

pytest 的灵魂是 `assert` 语句——你没看错，就用你日常写代码的 `assert`，不用记那些奇怪的 `self.assertEqual()`、`unittest.TestCase` 之类的繁文缛节。

```python
# 这是一个超级简单的 pytest 测试文件
# 文件名通常以 test_ 开头，或者 _test 结尾
# 运行方式：pytest test_example.py -v

def test_addition():
    """测试加法是否正确——这是docstring，pytest会显示在报告中"""
    assert 1 + 1 == 2  # 如果为真，测试通过；假的话...嘿嘿


def test_string_operations():
    """测试字符串操作"""
    text = "hello python"
    assert text.upper() == "HELLO PYTHON"  # 转大写
    assert text.replace("python", "world") == "hello world"  # 替换
    assert text.split(" ") == ["hello", "python"]  # 分割


# 运行结果：
# test_example.py::test_addition PASSED
# test_example.py::test_string_operations PASSED
```

pytest 的另一个杀手锏是**参数化测试**——同一个测试函数，用不同的参数跑 N 遍。想象一下你要测试登录功能，用户名正确密码错误、用户名错误密码正确、用户名密码都错误、用户名密码都正确……四个场景写一个函数搞定：

```python
# pytest 参数化测试 —— 一个函数，多种姿势
import pytest


@pytest.mark.parametrize("username,password,expected", [
    ("admin", "wrongpass", False),       # 用户名对，密码错
    ("wronguser", "admin123", False),    # 用户名错，密码对
    ("", "admin123", False),             # 用户名为空
    ("admin", "admin123", True),          # 全对
])
def test_login(username, password, expected):
    """测试登录功能的各种情况"""
    # 模拟的登录验证函数
    def fake_login(user, pwd):
        return user == "admin" and pwd == "admin123"

    result = fake_login(username, password)
    assert result == expected


# 运行结果：
# test_login[admin-wrongpass-False] PASSED
# test_login[wronguser-admin123-False] PASSED
# test_login[-admin123-False] PASSED
# test_login[admin-admin123-True] PASSED
```

> 💡 pytest 小技巧：`pytest -v` 显示详细信息；`pytest -s` 打印 print 输出；`pytest -k "login"` 只运行名称含 "login" 的测试；`pytest --lf` 只运行上次失败的测试（省时间！）。

### fixture——测试的" setup "和" teardown "

说到测试，你肯定遇到过这种情况：每个测试之前都要连接数据库、都要创建测试用户、都要准备测试文件……手工写的话，代码又臭又长。pytest 的 `fixture` 就是来解决这个问题的——它帮你管理测试的"前戏"和"尾声"。

```python
# fixture 示例 —— 测试的好帮手
import pytest


# scope="function" 表示每个测试函数都执行一次
# scope="module" 表示整个模块只执行一次
@pytest.fixture(scope="module")
def database_connection():
    """模拟数据库连接——所有测试共享"""
    print("\n🔌 [SETUP] 正在连接数据库...")
    conn = {"connected": True, "data": []}
    yield conn  # yield 之前的代码是 setup，之后的是 teardown
    print("\n🔌 [TEARDOWN] 关闭数据库连接...")
    conn["connected"] = False


@pytest.fixture
def sample_user():
    """每个测试都创建新用户——干净卫生"""
    return {
        "name": "测试用户",
        "email": "test@example.com",
        "level": 99
    }


def test_user_info(database_connection, sample_user):
    """测试用户信息"""
    print(f"\n📧 数据库连接状态: {database_connection['connected']}")
    print(f"👤 用户: {sample_user['name']}")
    assert sample_user["level"] == 99


def test_user_email(database_connection, sample_user):
    """测试用户邮箱格式"""
    assert "@" in sample_user["email"]
    assert sample_user["email"].endswith(".com")


# 运行结果：
# 🔌 [SETUP] 正在连接数据库...
# test_user_info PASSED
# test_user_email PASSED
# 🔌 [TEARDOWN] 关闭数据库连接...
```

### Selenium——浏览器的"提线木偶"

`pytest` 测试的是你写的 Python 代码本身，但如果你想测试**网页**呢？比如："点击这个按钮后，页面显示了什么？"、"表单提交后数据是否正确保存了？"这时候你就需要 Selenium 了。

Selenium 本来是一个浏览器自动化测试工具（最初是为 Java 设计的），后来有了 Python 绑定。它能**真实地打开浏览器**（Chrome、Firefox 等），模拟人的操作（点击、输入、滚动），然后检查页面元素。

```python
# Selenium 基本操作 —— 让浏览器乖乖听话
# 需要先安装：pip install selenium
# 还需要下载对应浏览器的 driver（chromedriver.exe 等）
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def test_baidu_search():
    """用 Selenium 打开百度搜索"Python"""
    # 创建 Chrome 浏览器实例（无头模式，不显示窗口）
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 无头模式，服务器环境常用
    driver = webdriver.Chrome(options=options)

    try:
        # 打开百度
        driver.get("https://www.baidu.com")
        print(f"\n🌐 页面标题: {driver.title}")

        # 找到搜索框（通过 name 属性）
        search_box = driver.find_element(By.NAME, "wd")

        # 输入搜索内容
        search_box.send_keys("Python 是什么")
        print("⌨️ 已输入搜索关键词")

        # 按回车搜索
        search_box.send_keys(Keys.RETURN)
        print("↵ 已按回车")

        # 等待一下让页面加载
        time.sleep(2)

        # 检查标题
        assert "Python" in driver.title or "百度" in driver.title
        print("✅ 搜索成功！")

    finally:
        driver.quit()  # 关闭浏览器
        print("👋 浏览器已关闭")


# 运行结果：
# 🌐 页面标题: 百度一下，你就知道
# ⌨️ 已输入搜索关键词
# ↵ 已按回车
# ✅ 搜索成功！
# 👋 浏览器已关闭
```

### Playwright——后起之秀，比 Selenium 更"剧本"

如果说 Selenium 是老戏骨，那 `Playwright` 就是那个从电影学院毕业、会武功、会表演、还会即兴发挥的新生代演员。由 Microsoft 开发，支持 Python、JavaScript、TypeScript 等多语言，主打**更现代**、**更稳定**、**更易用**。

Playwright 最大的亮点是**自动等待**：Selenium 你可能需要手动 `time.sleep()` 等待元素出现，Playwright 会自动等待元素加载好再操作，大大减少了 flaky test（不稳定测试）的出现。

```python
# Playwright 示例 —— 更现代的浏览器自动化
# 安装：pip install playwright && playwright install
from playwright.sync_api import sync_playwright


def test_netease_homepage():
    """用 Playwright 打开网易首页"""
    with sync_playwright() as p:
        # 启动 Chromium 浏览器
        browser = p.chromium.launch(headless=True)  # headless=False 则显示浏览器窗口
        page = browser.new_page()

        # 打开页面
        page.goto("https://www.163.com")
        print(f"\n🌐 页面标题: {page.title()}")

        # 截图保存（可以看看到底打开了啥）
        page.screenshot(path="screenshot_163.png")
        print("📸 已截图保存为 screenshot_163.png")

        # 获取所有链接
        links = page.query_selector_all("a")
        print(f"🔗 页面共有 {len(links)} 个链接")

        # 自动等待并点击第一个新闻链接（如果存在）
        try:
            news_link = page.wait_for_selector("a[href*='news']", timeout=5000)
            if news_link:
                print(f"📰 发现新闻链接: {news_link.get_attribute('href')}")
        except Exception as e:
            print(f"⚠️ 没找到新闻链接: {e}")

        browser.close()
        print("✅ Playwright 测试完成！")


# 运行结果：
# 🌐 页面标题: 网易
# 📸 已截图保存为 screenshot_163.png
# 🔗 页面共有 127 个链接
# 📰 发现新闻链接: https://news.163.com/...
# ✅ Playwright 测试完成！
```

### 三剑客对比——我该怎么选？

```
┌─────────────┬───────────────┬───────────────┬───────────────┐
│    特性     │    pytest     │    Selenium   │   Playwright  │
├─────────────┼───────────────┼───────────────┼───────────────┤
│  测试类型   │  单元测试     │  浏览器UI测试  │  浏览器UI测试  │
│             │  集成测试     │  端到端测试    │  端到端测试    │
├─────────────┼───────────────┼───────────────┼───────────────┤
│  是否需要   │   不需要      │     需要       │    需要        │
│   浏览器    │  （纯代码）   │   （真浏览器）  │  （可无头）    │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   难度      │    ⭐         │    ⭐⭐⭐      │    ⭐⭐        │
│   （1-5星） │   （超简单）  │  （配置麻烦）  │  （更现代）    │
├─────────────┼───────────────┼───────────────┼───────────────┤
│  等待机制   │   N/A         │  手动等待      │   自动等待     │
│             │              │  (sleep/until)│   （更稳定）   │
├─────────────┼───────────────┼───────────────┼───────────────┤
│  适用场景   │  API/函数/    │  传统Web应用   │  现代Web应用   │
│             │  模块测试     │  （jQuery等）  │  （SPA/React） │
└─────────────┴───────────────┴───────────────┴───────────────┘
```

> 🎯 最佳实践：**pytest 做核心，Selenium/Playwright 做外壳**。你的业务逻辑用 pytest 狠狠测，你的网页交互用 Playwright 优雅测。

### 测试驱动开发（TDD）——先写测试再写代码

这里介绍一个"反直觉"的编程哲学：**先写测试，再写代码**。这不是让你在写代码前先喝咖啡发呆，而是：

1. 先想清楚你要实现什么功能
2. 先写测试（当然会失败，因为代码还没写）
3. 再写代码让测试通过

这种方式的好处：强迫你思考接口设计、减少过度设计、代码天然有测试覆盖。

```python
# TDD 示例 —— 先写测试，再写代码
# 假设我们要实现一个"字符串逆序"函数

# ===== 第一步：先写测试（此时 reverse_string 还不存在！）=====

def test_reverse_string_basic():
    """基本逆序测试"""
    result = reverse_string("hello")
    assert result == "olleh"


def test_reverse_string_palindrome():
    """回文测试（正反一样）"""
    result = reverse_string("上海自来水来自海上")
    assert result == "上海自来水来自海上"


def test_reverse_string_empty():
    """空字符串测试"""
    result = reverse_string("")
    assert result == ""


# 运行测试——当然会失败：NameError: name 'reverse_string' is not defined

# ===== 第二步：写代码让测试通过 =====

def reverse_string(s: str) -> str:
    """字符串逆序函数"""
    return s[::-1]  # Python 的切片反转，简洁到离谱

# 现在运行测试：全部通过！🎉

# 运行结果：
# test_reverse_string_basic PASSED
# test_reverse_string_palindrome PASSED
# test_reverse_string_empty PASSED
```

---

## 26.2 游戏开发（Pygame / Godot-Python）

### 游戏开发——Python 能写游戏？

"Python 能写游戏吗？"

能！

"Python 写游戏厉害吗？"

呃……看情况。

Python 在游戏开发领域不是最强的（那是 C++/C# 的地盘，比如 Unity/Unreal），但它**最适合快速原型开发**和**独立小游戏**。想象你有个游戏灵感，用 Python + Pygame 两天就能做出一个可玩的原型，而用 C++ 可能两周还在配置环境。

> 记住：**先让游戏能跑，再考虑优化**。一个跑不起来的"3A大作"毫无意义。

### Pygame——2D 游戏的"入门神器"

`Pygame` 是 Python 最著名的游戏开发库，基于 SDL（Simple DirectMedia Layer）封装。它不是用来做"原神"的，它是用来做"俄罗斯方块"、"贪吃蛇"、"打砖块"这类 2D 小游戏的。

Pygame 的核心概念：
- **Surface**：可以理解为画布（一块内存区域），所有东西都画在上面
- **Rect**：矩形区域，用于定位和碰撞检测
- **Event**：事件，比如键盘按下、鼠标移动、窗口关闭
- **Clock**：控制帧率，让游戏以稳定速度运行

```python
# Pygame 入门 —— 创建一个可以移动的矩形
# 安装：pip install pygame
# 运行方式：python pygame_intro.py
import pygame
import sys

# 初始化 Pygame（必须！）
pygame.init()

# 设置窗口
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("我的第一个 Pygame 游戏！🎮")

# 定义颜色（RGB）
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 创建玩家矩形（x坐标, y坐标, 宽度, 高度）
player = pygame.Rect(350, 500, 100, 50)
player_speed = 5

# 游戏时钟（控制帧率）
clock = pygame.time.Clock()
FPS = 60  # 每秒 60 帧

# 主游戏循环
running = True
while running:
    # ===== 事件处理 =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 点击窗口关闭按钮
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # 按 ESC 退出
                running = False

    # ===== 逻辑更新 =====
    keys = pygame.key.get_pressed()  # 获取所有按键状态
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += player_speed

    # 边界限制（不能移出屏幕）
    player.x = max(0, min(player.x, WIDTH - player.width))
    player.y = max(0, min(player.y, HEIGHT - player.height))

    # ===== 渲染（绘制）=====
    screen.fill(BLACK)           # 清屏（黑色背景）
    pygame.draw.rect(screen, RED, player)  # 画玩家矩形
    pygame.display.flip()        # 更新整个屏幕（双缓冲机制）

    # 控制帧率
    clock.tick(FPS)

# 退出 Pygame
pygame.quit()
sys.exit()

# 运行结果：
# 创建一个窗口，显示一个红色矩形
# 可以用方向键或 WASD 移动它
# 按 ESC 或关闭窗口按钮退出
```

### 贪吃蛇——经典游戏的 Pygame 实现

光画个方块太无聊了？来整个经典贪吃蛇！这可是每个游戏开发者的"Hello World"。

```python
# 贪吃蛇游戏 —— Pygame 实现
# 运行：python snake_game.py
import pygame
import random
import sys

# 初始化
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 贪吃蛇 | 按 Q 退出")
clock = pygame.time.Clock()
FPS = 10  # 蛇的速度（每秒移动次数）

# 颜色
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)

# 初始蛇（三个节）
snake = [(5, 5), (4, 5), (3, 5)]
direction = (1, 0)  # 向右移动

# 食物位置
food = (10, 5)

def draw_grid():
    """画网格背景（可选，美观用）"""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (0, y), (WIDTH, y))

def draw_snake():
    """画蛇"""
    for segment in snake:
        rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE,
                          CELL_SIZE-2, CELL_SIZE-2)
        pygame.draw.rect(screen, GREEN, rect)
        # 画个小眼睛装饰
        pygame.draw.circle(screen, WHITE,
                          (rect.centerx-3, rect.centery-3), 2)
        pygame.draw.circle(screen, WHITE,
                          (rect.centerx+3, rect.centery-3), 2)

def draw_food():
    """画食物"""
    rect = pygame.Rect(food[0]*CELL_SIZE, food[1]*CELL_SIZE,
                      CELL_SIZE-2, CELL_SIZE-2)
    pygame.draw.rect(screen, RED, rect, border_radius=5)

def move_snake():
    """移动蛇"""
    global food
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # 撞墙检测
    if head[0] < 0 or head[0] >= WIDTH // CELL_SIZE:
        return False
    if head[1] < 0 or head[1] >= HEIGHT // CELL_SIZE:
        return False

    # 撞自己检测
    if head in snake:
        return False

    snake.insert(0, head)  # 新头部

    # 吃食物
    if head == food:
        # 生成新食物（确保不在蛇身上）
        while True:
            food = (random.randint(0, WIDTH//CELL_SIZE-1),
                   random.randint(0, HEIGHT//CELL_SIZE-1))
            if food not in snake:
                break
    else:
        snake.pop()  # 没吃东西就移尾

    return True

score = 0
font = pygame.font.SysFont("arial", 24)

running = True
while running:
    # ===== 事件处理 =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            # 方向控制（不能180度掉头）
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            if event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            if event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            if event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # ===== 逻辑更新 =====
    if not move_snake():
        print(f"💀 游戏结束！得分：{score}")
        break  # 或者显示 Game Over 界面

    # ===== 渲染 =====
    screen.fill(BLACK)
    draw_grid()
    draw_food()
    draw_snake()

    # 显示分数
    score_text = font.render(f"得分: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

    score = len(snake) - 3  # 初始长度是3

pygame.quit()
print("👋 游戏已退出")

# 运行结果：
# 显示一个黑色背景的窗口，有网格线
# 一条绿色的蛇在移动，吃红色的食物会变长
# 按方向键控制方向，按 Q 退出
# 撞墙或撞自己后游戏结束，在终端打印得分
```

### Godot-Python（GDScript）——不是 Python 但很接近

`Godot` 是一款开源游戏引擎，有自己的脚本语言 **GDScript**。GDScript 语法和 Python 非常像（连缩进都一样），但它不是 Python，是一门专门为 Godot 设计的语言。

> 如果你想用"真正的 Python"做游戏，可以试试 `Godot-Python` 插件，它允许你在 Godot 引擎中使用 Python 编程。但注意：GDScript 才是 Godot 的官方语言，生态最好。

Godot 的特点：
- 完全免费开源（不用付钱，不用担心版权）
- 轻量级（下载几十MB，Unity 得几个 G）
- 2D 和 3D 都支持
- 节点系统很独特（一切皆节点，场景可嵌套）

```python
# GDScript 示例（不是纯 Python，但语法很像！）
# 这段代码在 Godot 引擎中运行

# extends Node
#
# var speed = 400
# var velocity = Vector2.ZERO
#
# func _process(delta):
#     # 每一帧调用，delta 是距离上一帧的时间（秒）
#     velocity = Vector2.ZERO
#
#     if Input.is_action_pressed("ui_right"):
#         velocity.x += 1
#     if Input.is_action_pressed("ui_left"):
#         velocity.x -= 1
#     if Input.is_action_pressed("ui_down"):
#         velocity.y += 1
#     if Input.is_action_pressed("ui_up"):
#         velocity.y -= 1
#
#     position += velocity.normalized() * speed * delta
#
#     # 边界限制
#     position.x = clamp(position.x, 0, get_viewport_rect().size.x)
#     position.y = clamp(position.y, 0, get_viewport_rect().size.y)
```

> 🎮 游戏开发建议：**小作品用 Pygame**，快速出原型；**中型以上作品用 Godot**，社区活跃，文档完善，有 3D 需求更是首选。

### 其他 Python 游戏库一览

| 库名 | 特点 | 适合类型 |
|------|------|---------|
| Pygame | 最流行，2D 为主 | 小游戏、原型 |
| Pyglet | 更面向对象，不用安装 SDL | 2D/轻3D |
| Arcade | 现代 Pygame 替代品，更易学 | 2D 游戏 |
| Godot (GDScript) | 专业引擎，2D+3D | 中型游戏 |
| Panda3D | 3D 引擎，Disney 使用过 | 3D 游戏/模拟 |
| Ursina | 基于 Panda3D，Python 风格 | 2D/3D 快速开发 |

---

## 26.3 GUI（PyQt5 / PyQt6 / Tkinter / PySide）

### 图形界面——让程序有个"脸"

没有图形界面的程序，就像一家没有招牌的餐厅——东西好吃，但别人不知道你卖什么。**GUI（Graphical User Interface，图形用户界面）** 就是程序的脸面，让用户点点鼠标就能操作，而不是背诵一堆命令行参数。

Python 做 GUI 的框架多如牛毛，这里我们重点介绍四个主要玩家：**Tkinter**（Python 内置，入门首选）、**PyQt5/PyQt6**（功能强大，商用首选）、**PySide**（Qt 官方 Python 绑定）。

### Tkinter——Python 的"亲儿子"

`Tkinter` 是 Python 标准库的一部分，不用安装，直接 `import tkinter` 就能用。它基于 Tcl/Tk，虽然界面丑了点（默认主题），但胜在**零配置、立即跑**。Python 自带的 IDLE 就是用 Tkinter 写的。

```python
# Tkinter 入门 —— 创建一个带按钮的窗口
# 安装：无需安装（Python 内置）
import tkinter as tk
from tkinter import messagebox


def on_button_click():
    """按钮点击事件处理"""
    messagebox.showinfo("消息", "你点了我！🎉\n谢谢你，好心人！")
    label.config(text="我被点过了 😳")


# 创建主窗口
root = tk.Tk()
root.title("我的第一个 Tkinter 程序")
root.geometry("400x200")  # 宽 x 高

# 创建标签（文字）
label = tk.Label(root, text="请点击下方按钮", font=("Arial", 16))
label.pack(pady=30)  # pack 是布局管理器，让组件"打包"到窗口里

# 创建按钮
button = tk.Button(
    root,
    text="点我！",
    font=("Arial", 14),
    bg="#4CAF50",      # 背景色
    fg="white",        # 文字颜色
    padx=20,
    pady=10,
    command=on_button_click  # 点击时调用的函数
)
button.pack(pady=10)

# 创建输入框
entry = tk.Entry(root, font=("Arial", 14), width=30)
entry.pack(pady=10)
entry.insert(0, "这里可以输入文字")  # 默认文字

# 运行 Tkinter 事件循环（相当于"启动程序"）
root.mainloop()

# 运行结果：
# 弹出一个 400x200 的窗口
# 窗口标题是"我的第一个 Tkinter 程序"
# 有一个标签、一个按钮、一个输入框
# 点击按钮会弹出消息框
```

### Tkinter 进阶——做个计算器

光有按钮太简单了，来整个能用的计算器！

```python
# Tkinter 计算器 —— 理论派作品
import tkinter as tk


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🧮 简易计算器")
        self.window.geometry("320x400")
        self.window.resizable(False, False)  # 禁止调整大小

        # 计算器显示（只读文本框）
        self.display = tk.Entry(
            self.window,
            font=("Arial", 24),
            justify="right",  # 文字右对齐
            bd=10,
            insertwidth=2
        )
        self.display.grid(row=0, column=0, columnspan=4,
                         sticky="nsew", padx=5, pady=5)

        # 按钮布局
        buttons = [
            ("C", 1, 0), ("/", 1, 1), ("*", 1, 2), ("DEL", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("-", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("+", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("=", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("(", 5, 2), (")", 5, 3),
        ]

        for (text, row, col) in buttons:
            self.create_button(text, row, col)

        self.window.mainloop()

    def create_button(self, text, row, col):
        """创建按钮"""
        # 特殊按钮样式
        if text == "=":
            btn = tk.Button(
                self.window, text=text, font=("Arial", 18),
                bg="#4CAF50", fg="white",
                command=lambda: self.calculate()
            )
        elif text in ("C", "DEL"):
            btn = tk.Button(
                self.window, text=text, font=("Arial", 18),
                bg="#f44336", fg="white",
                command=lambda: self.clear() if text == "C" else self.delete()
            )
        elif text in ("+", "-", "*", "/"):
            btn = tk.Button(
                self.window, text=text, font=("Arial", 18),
                bg="#FF9800", fg="white",
                command=lambda: self.append_char(text)
            )
        else:
            btn = tk.Button(
                self.window, text=text, font=("Arial", 18),
                bg="#2196F3", fg="white",
                command=lambda: self.append_char(text)
            )

        btn.grid(row=row, column=col, sticky="nsew",
                padx=3, pady=3)

        # 最后一行的0占两列
        if text == "0":
            btn.grid(columnspan=2)

    def append_char(self, char):
        """添加字符到显示框"""
        self.display.insert(tk.END, char)

    def clear(self):
        """清空"""
        self.display.delete(0, tk.END)

    def delete(self):
        """删除最后一个字符"""
        content = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, content[:-1])

    def calculate(self):
        """计算结果"""
        try:
            expression = self.display.get()
            result = eval(expression)  # 危险！生产环境别用 eval
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "错误")


if __name__ == "__main__":
    Calculator()

# 运行结果：
# 显示一个彩色按钮的计算器界面
# 可以点击按钮进行四则运算
# 按 = 号得出结果
# 按 C 清空，DEL 删除最后一个字符
```

> ⚠️ **警告**：上面代码用了 `eval()`，这在**实际项目中是危险行为**！用户可以输入 `__import__('os').system('rm -rf /')` 之类的恶意代码。生产环境请用 `ast.literal_eval()` 或正则表达式解析。

### PyQt5 / PyQt6——工业级 GUI 框架

如果说 Tkinter 是"买菜车"，那 **PyQt** 就是"特斯拉"。Qt 是一个功能极其强大的跨平台 GUI 框架（诺基亚出品，后来开源了），PyQt 是它在 Python 侧的绑定。界面美观，功能完备，文档详尽，但……学习曲线也陡不少。

**PyQt5** 对应 Qt5，**PyQt6** 对应 Qt6。两者 API 略有差异，但概念相通。

```python
# PyQt5 入门 —— 更专业的界面
# 安装：pip install PyQt5
# 注意：PyQt6 是 pip install PyQt6
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QVBoxLayout, QWidget, QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 演示窗口 🚀")
        self.setGeometry(100, 100, 500, 400)

        # ===== 中央组件 =====
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ===== 布局 =====
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 标题
        title = QLabel("欢迎使用 PyQt5！")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 输入框
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入你的名字...")
        self.input_field.returnPressed.connect(self.greet)  # 回车事件
        layout.addWidget(self.input_field)

        # 多行文本框
        self.output = QTextEdit()
        self.output.setReadOnly(True)  # 只读
        layout.addWidget(self.output)

        # 按钮
        self.button = QPushButton("打招呼 👋")
        self.button.clicked.connect(self.greet)  # 点击事件
        layout.addWidget(self.button)

    def greet(self):
        """打招呼函数"""
        name = self.input_field.text()
        if name:
            self.output.append(f"你好，{name}！欢迎来到 PyQt5 的世界 🎉")
        else:
            self.output.append("请先输入名字！")


# ===== 程序入口 =====
app = QApplication(sys.argv)  # 每个 PyQt 程序都要创建 QApplication
window = MyWindow()
window.show()
sys.exit(app.exec_())  # 进入事件循环（PyQt5 用 exec_，PyQt6 用 exec）

# 运行结果：
# 弹出一个专业外观的窗口
# 可以输入名字，点击按钮后在下方的文本框显示问候语
# 关闭窗口后程序退出
```

### PyQt6 中的主要变化

PyQt6 和 PyQt5 的主要区别：

```python
# PyQt6 的主要 API 变化

# 1. Qt 常量命名空间变了
# PyQt5: Qt.AlignCenter, Qt.Key_Return
# PyQt6: Qt.AlignmentFlag.AlignCenter, Qt.Key.Key_Return

# 2. exec_() 变成了 exec()
# PyQt5: app.exec_()
# PyQt6: app.exec()

# 3. 一些枚举值可以直接用字符串
# PyQt5: QMessageBox.information(parent, "标题", "内容")
# PyQt6: QMessageBox.information(parent, "标题", "内容")

# 4. 信号连接语法一致
# self.button.clicked.connect(self.handle_click)  # 两种版本通用
```

### PySide6——Qt 的"官方认证"

`PySide` 是 Qt 官方提供的 Python 绑定（由 Qt Company 维护），而 PyQt 是第三方公司（Riverbank Computing）维护的。两者 API 几乎一模一样，但**许可证不同**：

- **PyQt6**：GPLv3 协议（开源免费，商用要付费）
- **PySide6**：LGPLv3 协议（可以免费商用）

```python
# PySide6 —— 几乎和 PyQt5 一样的代码
# 安装：pip install PySide6
# API 和 PyQt5 几乎完全一致
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 窗口")
        self.setFixedSize(300, 200)

        button = QPushButton("点击我！")
        button.clicked.connect(self.on_click)
        self.setCentralWidget(button)

    def on_click(self):
        print("按钮被点击了！")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())  # 注意：PySide6 用 exec() 而不是 exec_()

# 运行结果：
# 和 PyQt5 基本一致
# 可以互换使用
```

### 四大家族对比

```
┌─────────────┬───────────────┬───────────────┬───────────────┬───────────────┐
│    框架     │    Tkinter    │    PyQt5      │    PyQt6      │    PySide6    │
├─────────────┼───────────────┼───────────────┼───────────────┼───────────────┤
│   安装      │   内置！      │  pip install  │  pip install  │  pip install  │
│             │  （不用装）   │    PyQt5      │    PyQt6      │    PySide6    │
├─────────────┼───────────────┼───────────────┼───────────────┼───────────────┤
│   外观      │    朴素       │    漂亮       │    漂亮       │    漂亮        │
│             │  （复古风）   │  （Qt 主题）  │  （Qt 主题）  │  （Qt 主题）   │
├─────────────┼───────────────┼───────────────┼───────────────┼───────────────┤
│   难度      │   ⭐         │   ⭐⭐⭐⭐     │   ⭐⭐⭐⭐     │   ⭐⭐⭐⭐      │
│   （1-5星） │  （最简单）   │  （功能强大）  │  （功能强大）  │  （功能强大）   │
│             │              │  （较难）    │  （较难）    │  （较难）     │
├─────────────┼───────────────┼───────────────┼───────────────┼───────────────┤
│   许可证    │   PSF         │   GPLv3       │   GPLv3       │   LGPLv3      │
│             │  （Python标准）│  （商用付费） │  （商用付费） │  （可免费商用）│
├─────────────┼───────────────┼───────────────┼───────────────┼───────────────┤
│   适用场景  │  工具脚本     │  桌面应用     │  桌面应用     │  桌面应用      │
│             │  快速原型     │  商业产品     │  商业产品     │  商业产品      │
│             │  学习入门     │  复杂界面     │  最新 Qt 特性 │  需要 LGPL     │
└─────────────┴───────────────┴───────────────┴───────────────┴───────────────┘
```

> 💡 **选择建议**：只是想快速验证个想法？用 `Tkinter`。要做一个正经的桌面应用？选 `PySide6`（LGPL 许可证）。

---

## 26.4 网络编程（socket / asyncio）

### 网络编程——让计算机"打电话"

**网络编程**？听起来很高大上，其实说白了就是让两台电脑互相"打电话"。一台电脑当**服务器**（接电话的），一台当**客户端**（打电话的）。电话通了，它们就能聊天（交换数据）。

Python 内置的 `socket` 库就是干这个的——它封装了操作系统的网络接口，让你用几行代码就能建立起网络连接。

### socket——TCP 客户端和服务器

`socket` 是操作系统提供的 API，Python 的 `socket` 模块只是帮你调用它。TCP 是**面向连接**的协议，就像打电话——拨号、接通、聊天、挂断；UDP 是**无连接**的，就像对讲机——直接喊，不管对方在不在。

```python
# socket 服务器 —— 蹲在家里等电话
# 运行方式：python server.py（需要先运行）
import socket
import threading

def handle_client(client_socket, addr):
    """处理单个客户端连接"""
    print(f"📞 收到来自 {addr} 的连接")
    while True:
        try:
            data = client_socket.recv(1024)  # 接收数据（最多1024字节）
            if not data:
                break
            message = data.decode("utf-8")
            print(f"📨 {addr} 说: {message}")

            # 回复客户端
            reply = f"服务器收到: {message}"
            client_socket.sendall(reply.encode("utf-8"))
        except ConnectionResetError:
            print(f"❌ {addr} 断开了连接")
            break

    client_socket.close()
    print(f"🔚 {addr} 的连接已关闭")


def start_server(host="127.0.0.1", port=8888):
    """启动服务器"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET: IPv4  地址类型
    # SOCK_STREAM: TCP 协议类型（SOCK_DGRAM 是 UDP）

    server.bind((host, port))  # 绑定地址和端口
    server.listen(5)           # 最多排队 5 个连接

    print(f"🖥️  服务器启动！监听 {host}:{port}")
    print("等待客户端连接...（按 Ctrl+C 退出）")

    try:
        while True:
            client_socket, addr = server.accept()  # 等待客户端连接
            # 为每个客户端创建新线程（并发处理）
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\n👋 服务器关闭中...")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()

# 运行结果：
# 🖥️  服务器启动！监听 127.0.0.1:8888
# 等待客户端连接...
# 📞 收到来自 ('127.0.0.1', 54321) 的连接
# 📨 ('127.0.0.1', 54321) 说: 你好，服务器！
# ❌ ('127.0.0.1', 54321) 断开了连接
```

```python
# socket 客户端 —— 主动打电话
# 运行方式：python client.py（需要服务器先运行）
import socket


def start_client(host="127.0.0.1", port=8888):
    """启动客户端"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))  # 连接到服务器
        print(f"✅ 已连接到服务器 {host}:{port}")
    except ConnectionRefusedError:
        print(f"❌ 无法连接到服务器 {host}:{port}")
        return

    print("输入消息发送（按 Ctrl+C 退出）：")

    try:
        while True:
            message = input("\n📤 你: ")
            if not message:
                continue

            client.sendall(message.encode("utf-8"))  # 发送数据

            response = client.recv(1024)  # 接收响应
            print(f"📥 服务器: {response.decode('utf-8')}")

    except KeyboardInterrupt:
        print("\n👋 断开连接...")
    finally:
        client.close()
        print("🔚 连接已关闭")


if __name__ == "__main__":
    start_client()

# 运行结果：
# ✅ 已连接到服务器 127.0.0.1:8888
# 输入消息发送（按 Ctrl+C 退出）：
#
# 📤 你: 你好，服务器！
# 📥 服务器: 服务器收到: 你好，服务器！
```

### UDP——"有就收，不保证"

UDP（User Datagram Protocol）和 TCP 的区别就像：
- **TCP**：打电话，必须接通，必须对方接了才能说话，说错了我再说一遍
- **UDP**：对讲机，直接喊，喊完就走，不管对方听到没

UDP 更快，但**不保证送达、不保证顺序、不保证不重复**。适合什么场景？视频直播、在线游戏、DNS 查询——丢一帧无所谓，但延迟高就完蛋了。

```python
# UDP 服务器 —— 简易广播站
import socket

def start_udp_server(host="127.0.0.1", port=8889):
    """启动 UDP 服务器"""
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP 用 SOCK_DGRAM
    server.bind((host, port))

    print(f"📻 UDP 服务器启动！监听 {host}:{port}")
    print("等待广播...（按 Ctrl+C 退出）")

    try:
        while True:
            data, addr = server.recvfrom(1024)  # 接收数据和发送者地址
            message = data.decode("utf-8")
            print(f"📨 收到来自 {addr}: {message}")

            # 回复（如果需要）
            reply = f"收到广播: {message}"
            server.sendto(reply.encode("utf-8"), addr)

    except KeyboardInterrupt:
        print("\n👋 服务器关闭...")
    finally:
        server.close()


# UDP 客户端
def start_udp_client(host="127.0.0.1", port=8889):
    """启动 UDP 客户端"""
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "喂！有人在吗？"
    client.sendto(message.encode("utf-8"), (host, port))
    print(f"📤 已发送: {message}")

    # 设置超时（UDP 不保证回复）
    client.settimeout(5)
    try:
        data, server_addr = client.recvfrom(1024)
        print(f"📥 服务器回复: {data.decode('utf-8')}")
    except socket.timeout:
        print("⏰ 服务器没有回复（UDP 不保证送达）")

    client.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        start_udp_server()
    else:
        start_udp_client()

# 运行方式：
# 终端1: python udp_demo.py server
# 终端2: python udp_client.py
```

### asyncio——异步编程，让程序"一心多用"

`asyncio` 是 Python 3.4 引入的标准库，用于**异步 I/O 编程**。它的核心概念是**协程（Coroutine）**——一种可以暂停和恢复执行的函数。

为什么要异步？因为程序经常需要"等待"：等待网络返回、等待文件读取、等待数据库查询。这些等待时间里，CPU 是空闲的。**同步编程**就是干等着，**异步编程**就是干等着的时候去干别的事。

> 通俗理解：同步就像你去银行办业务，排队等着叫号；异步就像你叫了号之后去喝咖啡，等广播喊你再回来。

```python
# asyncio 异步编程 —— async/await 语法
# 安装：无需安装（Python 3.4+ 内置）
import asyncio


async def say_hello(name, delay):
    """异步函数：延迟打印问候语"""
    # await 暂停函数执行，把控制权交还给事件循环
    await asyncio.sleep(delay)  # 模拟 I/O 操作（等待）
    print(f"👋 你好，{name}！")


async def main():
    """主异步函数"""
    print("⏰ 开始异步任务...")

    # 创建三个协程（注意：只是创建，还没执行）
    task1 = asyncio.create_task(say_hello("Alice", 2))
    task2 = asyncio.create_task(say_hello("Bob", 1))
    task3 = asyncio.create_task(say_hello("Charlie", 3))

    # 等待所有任务完成
    # 如果是同步写法，total time = 2+1+3 = 6秒
    # 异步写法，total time = max(2,1,3) = 3秒！
    await asyncio.gather(task1, task2, task3)

    print("✅ 所有任务完成！")


# Python 3.7+ 可以直接 asyncio.run()
if __name__ == "__main__":
    asyncio.run(main())

# 运行结果：
# ⏰ 开始异步任务...
# 👋 你好，Bob！        # 1秒后（Bob 最快）
# 👋 你好，Alice！       # 2秒后
# 👋 你好，Charlie！     # 3秒后
# ✅ 所有任务完成！
# 总耗时约 3 秒（而不是 6 秒！）
```

### asyncio 服务器——高性能 HTTP 服务器

```python
# asyncio TCP 服务器 —— 异步处理连接
import asyncio


async def handle_client(reader, writer):
    """处理单个客户端连接（异步）"""
    addr = writer.get_extra_info('peername')
    print(f"📞 客户端连接: {addr}")

    # 接收数据
    data = await reader.read(1024)
    message = data.decode()
    print(f"📨 收到: {message}")

    # 发送响应（HTTP 协议：头部用 \r\n 分隔，空行结束头部）
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 17\r\n"
        "\r\n"
        "Hello, Async World!"
    )
    writer.write(response.encode())
    await writer.drain()  # 确保数据发送出去

    print(f"📤 已回复: {addr}")
    writer.close()
    await writer.wait_closed()


async def main():
    """启动异步服务器"""
    server = await asyncio.start_server(
        handle_client, "127.0.0.1", 8888
    )

    addr = server.sockets[0].getsockname()
    print(f"🖥️ 异步服务器启动: {addr}")

    async with server:
        await server.serve_forever()  # 永远运行


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 服务器关闭")

# 运行结果：
# 🖥️ 异步服务器启动: ('127.0.0.1', 8888)
# （等待客户端连接...）
```

### 同步 vs 异步——什么时候用什么？

```
┌─────────────┬─────────────────────┬─────────────────────┐
│    场景     │      同步代码       │      异步代码       │
├─────────────┼─────────────────────┼─────────────────────┤
│   适合      │ CPU 密集型任务      │ I/O 密集型任务       │
│             │ 简单脚本            │ 高并发服务器         │
│             │ 少量并发            │ Web 服务、API 调用   │
│             │ 调试困难的地方      │ 需要高吞吐量的地方   │
├─────────────┼─────────────────────┼─────────────────────┤
│   不适合    │ 需要同时处理大量    │ CPU 密集型计算       │
│             │ 网络请求的地方      │ 同步库为主的场景     │
├─────────────┼─────────────────────┼─────────────────────┤
│   代码      │ 简单直观            │ 需要理解事件循环     │
│   复杂度    │ try/except 就够了  │ 需要 await/async    │
├─────────────┼─────────────────────┼─────────────────────┤
│   性能      │ 受 GIL 限制         │ 可以处理成千上万     │
│             │ 一次只能做一件事    │ 个并发连接           │
└─────────────┴─────────────────────┴─────────────────────┘
```

> 💡 **实战建议**：初学者先用 `socket` 理解原理，然后用 `asyncio` 处理高并发场景。如果你想做 Web 服务，**直接用 FastAPI 或 aiohttp**（见下一节），别自己造轮子。

---

## 26.5 ORM（SQLAlchemy / Tortoise-ORM）

### ORM——把数据库变成"Excel 表格"

**ORM（Object-Relational Mapping，对象-关系映射）** 是什么？简单说，就是让你**用 Python 面向对象的方式操作数据库**，而不是写 SQL 语句。

没有 ORM：你得写 `SELECT * FROM users WHERE age > 18`
有 ORM：`User.query.filter(User.age > 18).all()`

看起来差不多？但当你需要 JOIN、事务、关联查询的时候，ORM 的优势就体现出来了——代码更 Pythonic，更不容易出错（防止 SQL 注入）。

> 形象比喻：ORM 就像你的翻译助理，你跟它说中文，它帮你翻译成英文（SQL），和美国客户（数据库）交流。

### SQLAlchemy——ORM 界的"老大哥"

`SQLAlchemy` 是 Python 生态里最成熟、功能最强大的 ORM，分为**Core**（SQL 表达式语言）和 **ORM**（对象映射）两层。它支持几乎所有主流数据库：PostgreSQL、MySQL、SQLite、Oracle……

```python
# SQLAlchemy 入门 —— 定义模型和基本操作
# 安装：pip install sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# ===== 第一步：连接数据库 =====
# SQLite 是文件型数据库，适合学习和测试
# echo=True 会打印所有 SQL 语句，方便调试
engine = create_engine("sqlite:///mydatabase.db", echo=True)

# ===== 第二步：定义模型 =====
Base = declarative_base()  # 所有模型的"基类"


class User(Base):
    """用户表模型"""
    __tablename__ = "users"  # 数据库中的表名

    id = Column(Integer, primary_key=True)  # 主键，自动递增
    name = Column(String(50), nullable=False)  # 不能为空
    email = Column(String(100), unique=True)  # 唯一
    age = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Product(Base):
    """产品表模型"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"


# ===== 第三步：创建表 =====
Base.metadata.create_all(engine)  # 在数据库中创建表

# ===== 第四步：创建会话（操作数据库的入口）=====
Session = sessionmaker(bind=engine)
session = Session()

# ===== 第五步：CRUD 操作 =====

# Create - 创建数据
print("\n=== 创建用户 ===")
new_user = User(name="张三", email="zhangsan@example.com", age=25)
session.add(new_user)        # 添加到会话
session.commit()             # 真正写入数据库
print(f"✅ 创建用户: {new_user}")

# 批量创建
users = [
    User(name="李四", email="lisi@example.com", age=30),
    User(name="王五", email="wangwu@example.com", age=28),
    User(name="赵六", email="zhaoliu@example.com", age=22),
]
session.add_all(users)
session.commit()
print(f"✅ 批量创建 {len(users)} 个用户")

# Read - 查询数据
print("\n=== 查询用户 ===")
# 查询所有用户
all_users = session.query(User).all()
for u in all_users:
    print(f"  {u}")

# 条件查询
adults = session.query(User).filter(User.age >= 25).all()
print(f"\n25岁以上的用户: {adults}")

# 查询单个（没有结果返回 None）
user = session.query(User).filter_by(name="张三").first()
print(f"张三: {user}")

# Update - 更新数据
print("\n=== 更新数据 ===")
if user:
    user.age = 26
    session.commit()
    print(f"✅ 张三的年龄更新为: {user.age}")

# Delete - 删除数据
print("\n=== 删除数据 ===")
zhao = session.query(User).filter_by(name="赵六").first()
if zhao:
    session.delete(zhao)
    session.commit()
    print(f"✅ 删除赵六")

# 关闭会话
session.close()

# 运行结果（部分）：
# ✅ 创建用户: <User(id=1, name='张三', email='zhangsan@example.com')>
# ✅ 批量创建 3 个用户
# <User(id=1, name='张三', ...>
# <User(id=2, name='李四', ...>
# ...
# 25岁以上的用户: [<User(...)>, <User(...)>]
```

### SQLAlchemy 进阶——表关系（JOIN）

数据库的精髓在于**表之间的关系**。一对一、一对多、多对多——SQLAlchemy 都能优雅处理。

```python
# SQLAlchemy 表关系 —— 订单和用户的例子
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_engine("sqlite:///ecommerce.db", echo=True)
Base = declarative_base()


class Customer(Base):
    """客户表"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))

    # relationship: 建立一对多关系
    # back_populates: 反向引用（从 Order 可以访问 Customer）
    orders = relationship("Order", back_populates="customer")


class Order(Base):
    """订单表"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_number = Column(String(20))
    total = Column(Float)
    customer_id = Column(Integer, ForeignKey("customers.id"))  # 外键

    # 反向引用
    customer = relationship("Customer", back_populates="orders")


# 创建表
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# 创建数据
print("=== 创建数据 ===")
c1 = Customer(name="马云", email="yma@example.com")
c2 = Customer(name="马化腾", email="mht@example.com")
session.add_all([c1, c2])
session.commit()

o1 = Order(order_number="A001", total=999.00, customer=c1)
o2 = Order(order_number="A002", total=1999.00, customer=c1)
o3 = Order(order_number="B001", total=99.00, customer=c2)
session.add_all([o1, o2, o3])
session.commit()

# 查询：获取马云的所有订单
print("\n=== 马云的订单 ===")
ma = session.query(Customer).filter_by(name="马云").first()
for order in ma.orders:
    print(f"  订单号: {order.order_number}, 金额: ¥{order.total}")

# 查询：找出所有金额大于 500 的订单及对应客户
print("\n=== 大额订单（>500）===")
large_orders = session.query(Order).filter(Order.total > 500).all()
for order in large_orders:
    print(f"  {order.customer.name} - {order.order_number}: ¥{order.total}")

# 或者用 JOIN 查询
print("\n=== JOIN 查询 ===")
results = session.query(Customer, Order).join(Order).filter(Order.total > 500).all()
for customer, order in results:
    print(f"  {customer.name} 的订单 {order.order_number}: ¥{order.total}")

session.close()

# 运行结果：
# === 马云的订单 ===
#   订单号: A001, 金额: ¥999.0
#   订单号: A002, 金额: ¥1999.0
# === 大额订单（>500）===
#   马云 的订单 A001: ¥999.0
#   马云 的订单 A002: ¥1999.0
```

### Tortoise-ORM——异步 ORM 的新星

`Tortoise-ORM` 是专为 `asyncio` 设计的 ORM，API 类似 Django ORM，但天生支持异步。如果你用 FastAPI 这种异步框架，Tortoise-ORM 是绝配。

```python
# Tortoise-ORM 示例 —— 异步操作数据库
# 安装：pip install tortoise-orm aiosqlite
import asyncio
from tortoise import Tortoise, fields
from tortoise.models import Model


class User(Model):
    """用户模型"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100, unique=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"


class Post(Model):
    """文章模型"""
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="posts"
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "posts"


async def main():
    """异步主函数"""
    # 初始化 Tortoise（连接 SQLite）
    await Tortoise.init(
        db_url="sqlite://async_db.db",
        modules={"models": ["__main__"]}
    )
    # 生成表结构
    await Tortoise.generate_schemas()

    print("=== 异步 CRUD 操作 ===")

    # Create
    user1 = await User.create(name="小明", email="xiaoming@example.com")
    user2 = await User.create(name="小红", email="xiaohong@example.com")
    print(f"✅ 创建用户: {user1.name}, {user2.name}")

    # Create Post（异步关联创建）
    post1 = await Post.create(title="Python 入门", content="print('Hello')", author=user1)
    post2 = await Post.create(title="异步编程", content="async def main()...", author=user1)
    post3 = await Post.create(title="Django 教程", content="django-admin startproject", author=user2)
    print(f"✅ 创建文章: {post1.title}, {post2.title}, {post3.title}")

    # Read - 异步查询
    all_users = await User.all()
    print(f"\n所有用户: {[u.name for u in all_users]}")

    # 过滤查询
    active_users = await User.filter(is_active=True)
    print(f"活跃用户: {[u.name for u in active_users]}")

    # 关联查询（预加载）
    posts_with_author = await Post.all().prefetch_related("author")
    for post in posts_with_author:
        print(f"  文章《{post.title}》作者: {post.author.name}")

    # Update
    user1.is_active = False
    await user1.save()
    print(f"\n✅ 更新用户: {user1.name} 现已 inactive")

    # Delete
    await post3.delete()
    print("✅ 删除文章: Django 教程")

    # 关闭连接
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())

# 运行结果：
# ✅ 创建用户: 小明, 小红
# ✅ 创建文章: Python 入门, 异步编程, Django 教程
#
# 所有用户: ['小明', '小红']
# 活跃用户: ['小明', '小红']
#   文章《Python 入门》作者: 小明
#   文章《异步编程》作者: 小明
#   文章《Django 教程》作者: 小红
#
# ✅ 更新用户: 小明 现已 inactive
# ✅ 删除文章: Django 教程
```

### ORM vs 原生 SQL——谁更好？

```
┌─────────────┬─────────────────────┬─────────────────────┐
│    方面     │      SQLAlchemy     │      原生 SQL       │
├─────────────┼─────────────────────┼─────────────────────┤
│   代码      │  Python 风格        │  字符串 SQL         │
│   可读性    │  ⭐⭐⭐⭐⭐          │  ⭐⭐⭐              │
├─────────────┼─────────────────────┼─────────────────────┤
│   灵活性    │  高层抽象有限制     │  完全自由           │
│             │  复杂查询有时需     │  任何查询都能写      │
│             │  用原生 SQL         │                     │
├─────────────┼─────────────────────┼─────────────────────┤
│   性能      │  有一定开销         │  最优性能            │
│             │  （但可优化）       │  （手写最优）        │
├─────────────┼─────────────────────┼─────────────────────┤
│   安全      │  自动防止           │  需手动防止          │
│             │  SQL 注入           │  SQL 注入           │
├─────────────┼─────────────────────┼─────────────────────┤
│   学习曲线  │  较陡               │  取决于 SQL 水平     │
├─────────────┼─────────────────────┼─────────────────────┤
│   适用场景  │  快速开发           │  复杂查询            │
│             │  Web 应用           │  性能关键场景        │
│             │  标准 CRUD          │  报表/分析           │
└─────────────┴─────────────────────┴─────────────────────┘
```

> 💡 **实战建议**：Django 项目用 Django ORM（内置）；FastAPI 项目优先 `Tortoise-ORM` 或 `SQLAlchemy`；需要极致性能再考虑原生 SQL。

---

## 26.6 API 客户端（httpx / aiohttp / requests）

### API 客户端——让程序"网购"

**API（Application Programming Interface，应用编程接口）** 是什么？简单说，就是软件之间的"接口协议"。你打开微信小程序查天气，后台就是小程序调用气象局的 API 获取数据。

Python 做 HTTP 请求（调 API）的库主要有三个：
- `requests`：同步库的"无冕之王"，简单易用
- `httpx`：新星，同步异步都支持，API 很像 requests
- `aiohttp`：纯异步，专门为 asyncio 设计

### requests——同步 HTTP 的"瑞士军刀"

`requests` 是 Python 历史上最受欢迎的库之一，用起来简单到离谱。它的设计哲学是："让 HTTP 请求变得人性化"。

```python
# requests 基础 —— GET/POST 请求
# 安装：pip install requests
import requests


def basic_requests_demo():
    """requests 基本用法演示"""

    # ===== GET 请求（获取资源）=====
    print("=== GET 请求 ===")

    # 简单的 GET
    response = requests.get("https://httpbin.org/get")
    print(f"状态码: {response.status_code}")  # 200 表示成功
    print(f"响应头: {response.headers['Content-Type']}")
    print(f"响应体: {response.text[:200]}...")  # 前200个字符

    # 带参数的 GET
    params = {"name": "张三", "age": 25}
    response = requests.get("https://httpbin.org/get", params=params)
    print(f"\n带参数请求: {response.url}")  # 自动拼接参数

    # ===== POST 请求（提交数据）=====
    print("\n=== POST 请求 ===")

    data = {"username": "admin", "password": "123456"}
    response = requests.post("https://httpbin.org/post", data=data)
    print(f"状态码: {response.status_code}")
    print(f"响应 JSON: {response.json()}")  # 自动解析 JSON

    # ===== 其他方法 =====
    print("\n=== 其他 HTTP 方法 ===")
    # PUT（更新）
    requests.put("https://httpbin.org/put", data={"key": "value"})
    # DELETE（删除）
    requests.delete("https://httpbin.org/delete")
    # PATCH（部分更新）
    requests.patch("https://httpbin.org/patch", data={"key": "new_value"})
    # HEAD（只获取头部）
    head_response = requests.head("https://httpbin.org/get")
    print(f"HEAD 响应头: {dict(head_response.headers)}")


def advanced_requests_demo():
    """requests 高级用法"""

    # ===== 请求头 =====
    print("=== 自定义请求头 ===")
    headers = {
        "User-Agent": "MyPythonApp/1.0",
        "Accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIs..."
    }
    response = requests.get("https://httpbin.org/headers", headers=headers)
    print(f"发送的请求头: {response.json()['headers']}")

    # ===== 处理 JSON API =====
    print("\n=== JSON API 调用 ===")
    # GitHub API 示例
    response = requests.get(
        "https://api.github.com/repos/python/cpython",
        headers={"Accept": "application/vnd.github.v3+json"}
    )
    if response.status_code == 200:
        repo = response.json()
        print(f"仓库名: {repo['full_name']}")
        print(f"描述: {repo['description']}")
        print(f"Star数: {repo['stargazers_count']}")
        print(f"语言: {repo['language']}")

    # ===== 文件上传 =====
    print("\n=== 文件上传 ===")
    files = {"file": open(__file__, "rb")}  # 上传当前文件作为示例
    # response = requests.post("https://httpbin.org/post", files=files)
    print("文件上传示例（已省略文件流）")

    # ===== 会话（保持 Cookie）=====
    print("\n=== 会话（保持登录状态）===")
    session = requests.Session()

    # 登录
    # session.post("https://example.com/login", data={"user": "admin", "pass": "xxx"})

    # 之后的请求会自动带上 Cookie
    # response = session.get("https://example.com/profile")

    # ===== 超时和重试 =====
    print("\n=== 超时处理 ===")
    try:
        # timeout=3 表示等 3 秒没响应就抛异常
        response = requests.get("https://httpbin.org/delay/5", timeout=2)
    except requests.Timeout:
        print("⏰ 请求超时（超过2秒）")
    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}")

    # ===== 下载大文件（流式读取）=====
    print("\n=== 流式下载大文件 ===")
    # response = requests.get("https://example.com/large_file.zip", stream=True)
    # with open("large_file.zip", "wb") as f:
    #     for chunk in response.iter_content(chunk_size=8192):
    #         f.write(chunk)
    print("流式下载示例（需要实际文件 URL）")


if __name__ == "__main__":
    basic_requests_demo()
    advanced_requests_demo()

# 运行结果：
# === GET 请求 ===
# 状态码: 200
# 响应头: application/json
# 响应体: {"args": {}, "headers": {...}, "origin": "..."}...
#
# === POST 请求 ===
# 状态码: 200
# 响应 JSON: {'data': '', 'form': {'password': '123456', 'username': 'admin'}, ...}
#
# === GitHub API ===
# 仓库名: python/cpython
# 描述: The Python programming language
# Star数: 58000+
# 语言: Python
#
# ⏰ 请求超时（超过2秒）
```

### httpx——requests 的"升级版"

`httpx` 是一个很"年轻"的库（2019 年发布），设计目标是成为"现代的 requests"，支持**同步和异步两种模式**。API 设计和 requests 高度一致，如果你会用 requests，上手 httpx 分分钟。

```python
# httpx —— 同步和异步都支持的 HTTP 客户端
# 安装：pip install httpx
import httpx
import asyncio


def sync_demo():
    """httpx 同步用法（和 requests 几乎一样）"""
    print("=== httpx 同步模式 ===")

    # GET 请求
    response = httpx.get("https://httpbin.org/get")
    print(f"状态码: {response.status_code}")
    print(f"响应体: {response.text[:150]}...")

    # 异步上下文管理器
    with httpx.Client() as client:
        response = client.get("https://httpbin.org/json")
        print(f"JSON 响应: {response.json()}")


async def async_demo():
    """httpx 异步用法（专为 asyncio 设计）"""
    print("\n=== httpx 异步模式 ===")

    # 异步上下文管理器
    async with httpx.AsyncClient() as client:
        # 并发发起多个请求（比同步快很多！）
        tasks = [
            client.get("https://httpbin.org/get"),
            client.get("https://httpbin.org/ip"),
            client.get("https://httpbin.org/headers"),
        ]

        # 等待所有请求完成
        responses = await asyncio.gather(*tasks)

        for resp in responses:
            print(f"  {resp.url}: {resp.status_code}")

    # 单个异步请求
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/delay/1", timeout=5)
        print(f"\n延迟1秒的响应: {response.json()}")


if __name__ == "__main__":
    # 同步部分
    sync_demo()

    # 异步部分
    asyncio.run(async_demo())

# 运行结果：
# === httpx 同步模式 ===
# 状态码: 200
# 响应体: {"args": {}, "headers": {"Host": "httpbin.org", ...}}
#
# === httpx 异步模式 ===
#   https://httpbin.org/get: 200
#   https://httpbin.org/ip: 200
#   https://httpbin.org/headers: 200
#
# 延迟1秒的响应: {...}
```

### aiohttp——纯异步 HTTP 客户端/服务器

`aiohttp` 是专门为 `asyncio` 设计的 HTTP 库，既能当**客户端**发请求，也能当**服务器**接收请求。如果你要构建高性能异步服务，aiohttp 是好选择。

```python
# aiohttp —— 纯异步 HTTP 客户端
# 安装：pip install aiohttp
import aiohttp
import asyncio


async def fetch_all():
    """并发请求多个 URL"""
    print("=== aiohttp 并发请求 ===")

    async with aiohttp.ClientSession() as session:
        urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/ip",
            "https://httpbin.org/user-agent",
            "https://httpbin.org/headers",
        ]

        # 创建任务
        async def fetch_one(url):
            async with session.get(url) as response:
                data = await response.json()
                return url, data

        # 并发执行
        tasks = [fetch_one(url) for url in urls]
        results = await asyncio.gather(*tasks)

        for url, data in results:
            print(f"✅ {url.split('/')[-1]}: OK")


async def post_with_json():
    """POST JSON 数据"""
    print("\n=== aiohttp POST JSON ===")

    async with aiohttp.ClientSession() as session:
        payload = {
            "name": "张三",
            "skills": ["Python", "JavaScript", "Go"]
        }

        async with session.post(
            "https://httpbin.org/post",
            json=payload  # 自动设置 Content-Type: application/json
        ) as response:
            result = await response.json()
            print(f"发送的 JSON: {result['json']}")
            print(f"状态码: {response.status}")


async def with_headers_and_timeout():
    """带请求头和超时"""
    print("\n=== aiohttp 带请求头和超时 ===")

    headers = {"X-Custom-Header": "Hello", "Accept": "application/json"}

    async with aiohttp.ClientSession() as session:
        # 设置超时
        timeout = aiohttp.ClientTimeout(total=5)

        try:
            async with session.get(
                "https://httpbin.org/delay/3",
                headers=headers,
                timeout=timeout
            ) as response:
                print(f"响应状态: {response.status}")
        except asyncio.TimeoutError:
            print("⏰ 请求超时！")


if __name__ == "__main__":
    asyncio.run(fetch_all())
    asyncio.run(post_with_json())
    asyncio.run(with_headers_and_timeout())

# 运行结果：
# === aiohttp 并发请求 ===
# ✅ get: OK
# ✅ ip: OK
# ✅ user-agent: OK
# ✅ headers: OK
#
# === aiohttp POST JSON ===
# 发送的 JSON: {'name': '张三', 'skills': ['Python', 'JavaScript', 'Go']}
# 状态码: 200
```

### 三剑客对比

```
┌─────────────┬───────────────┬───────────────┬───────────────┐
│    库名     │    requests   │     httpx     │    aiohttp    │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   诞生日    │   2011 年     │   2019 年     │   2016 年     │
│   （古老度）│  （老前辈）   │  （小鲜肉）   │  （正当壮年） │
├─────────────┼───────────────┼───────────────┼───────────────┤
│ 同步/异步  │   仅同步      │  两者都行     │   仅异步      │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   API 风格  │   极度简洁   │   很像 requests│   稍复杂      │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   适用场景  │   简单脚本   │   现代项目    │   高性能服务  │
│             │  同步优先   │  需要异步时   │   爬虫/API客户端│
│             │              │  快速切换     │               │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   性能      │   一般       │   异步模式    │   最高        │
│             │              │   性能优秀    │   （专为异步） │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   生态      │   超成熟     │   快速发展中  │   成熟        │
│             │  插件极多    │  生态在追赶   │               │
└─────────────┴───────────────┴───────────────┴───────────────┘
```

> 💡 **选择建议**：简单脚本 → `requests`；FastAPI/Starlette 项目 → `httpx`；高并发爬虫/服务 → `aiohttp`。

---

## 26.7 认证（PyJWT / python-jose / authlib）

### 认证——证明"你是你"

**认证（Authentication）** 是确认用户身份的过程。常见的认证方式有：
- **用户名密码**：最传统，你证明你知道密码
- **JWT（JSON Web Token）**：无状态令牌，适合分布式系统
- **OAuth 2.0**：第三方登录，比如"用微信登录"
- **Session/Cookie**：服务端存储会话状态

这一节我们重点讲 Python 实现这些认证机制的工具库。

### JWT——无状态的"通行证"

**JWT（JSON Web Token）** 是一种开放标准（RFC 7519），用于在各方之间安全地传输信息。它由三部分组成：

```
xxxxx.yyyyy.zzzzz
 Header . Payload . Signature
```

- **Header（头部）**：声明类型和加密算法
- **Payload（载荷）**：存放实际要传输的数据（如用户 ID、过期时间）
- **Signature（签名）**：用密钥对 Header 和 Payload 进行签名，防止篡改

> 通俗比喻：JWT 就像一张**演唱会门票**。门票上有你的座位号（Payload）、防伪标签（Signature）。检票员只要验证防伪标签是真的，就相信这张票是真的，不需要去后台查数据库。

```python
# PyJWT —— 生成和验证 JWT
# 安装：pip install PyJWT
import jwt
import datetime


def jwt_basic_demo():
    """JWT 基本操作"""
    print("=== JWT 基本演示 ===")

    # ===== 准备密钥 =====
    secret_key = "我的超级密钥 12345"  # 生产环境请用更复杂的密钥
    algorithm = "HS256"  # HMAC SHA-256，最常用的算法

    # ===== 创建 Token =====
    payload = {
        "user_id": 12345,
        "username": "张三",
        "role": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),  # 过期时间
        "iat": datetime.datetime.utcnow()  # 签发时间
    }

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    print(f"生成的 JWT Token:\n{token}\n")

    # ===== 验证和解析 Token =====
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
        print("✅ Token 验证成功！")
        print(f"用户信息: {decoded}")
    except jwt.ExpiredSignatureError:
        print("❌ Token 已过期")
    except jwt.InvalidTokenError:
        print("❌ Token 无效")

    # ===== 解码（不验证）=====
    # 有时候你只是想看看 Token 里有什么，但不验证（比如调试）
    unverified = jwt.decode(token, options={"verify_signature": False})
    print(f"\n🔍 不验证直接看内容: {unverified}")


def jwt_with_claims_demo():
    """JWT 标准声明"""
    print("\n=== JWT 标准声明（Registered Claims）===")

    secret = "secret123"

    # JWT 标准声明（都是可选的）
    payload = {
        "sub": "user_001",           # subject（用户标识）
        "name": "李四",               # 自定义声明
        "admin": True,               # 自定义声明
        "iat": datetime.datetime.utcnow(),                          # 签发时间
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # 过期
        "nbf": datetime.datetime.utcnow() + datetime.timedelta(seconds=5),  # 不早于此时间生效
        "iss": "my-app-server",      # issuer（签发者）
        "aud": "my-app-client"       # audience（受众）
    }

    token = jwt.encode(payload, secret, algorithm="HS256")

    # 验证时指定签发者和受众
    decoded = jwt.decode(
        token,
        secret,
        algorithms=["HS256"],
        issuer="my-app-server",
        audience="my-app-client"
    )
    print(f"✅ 验证通过的用户: {decoded['name']} (sub={decoded['sub']})")


if __name__ == "__main__":
    jwt_basic_demo()
    jwt_with_claims_demo()

# 运行结果：
# === JWT 基本演示 ===
# 生成的 JWT Token:
# eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NSwidXNlcm5hbWUiOiLmsY3q
# pIXsmYIiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MTk...（省略）
#
# ✅ Token 验证成功！
# 用户信息: {'user_id': 12345, 'username': '张三', ...}
#
# 🔍 不验证直接看内容: {'user_id': 12345, 'username': '张三', ...}
#
# === JWT 标准声明 ===
# ✅ 验证通过的用户: 李四 (sub=user_001)
```

### JWT 在 Flask 中的实战

```python
# JWT + Flask 实战 —— 带认证的 API
# 安装：pip install flask pyjwt
from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

# 配置密钥
app.config["SECRET_KEY"] = "生产环境请用更复杂的随机字符串"

# 模拟的用户数据库
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}


def create_token(username):
    """生成 JWT Token"""
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def token_required(f):
    """装饰器：验证 JWT Token"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "没有 Token"}), 401

        try:
            # Bearer Token 格式
            if token.startswith("Bearer "):
                token = token[7:]
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user = data["username"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token 已过期"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "无效的 Token"}), 401

        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["POST"])
def login():
    """登录接口"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        token = create_token(username)
        return jsonify({"token": token})

    return jsonify({"error": "用户名或密码错误"}), 401


@app.route("/protected")
@token_required
def protected():
    """受保护的接口"""
    return jsonify({
        "message": f"欢迎，{request.user}！",
        "data": {"secret": "这是只有登录用户才能看到的数据"}
    })


@app.route("/admin")
@token_required
def admin_only():
    """管理员专属接口"""
    # 额外检查角色
    token = request.headers.get("Authorization")[7:]
    data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])

    if users.get(data["username"], {}).get("role") != "admin":
        return jsonify({"error": "需要管理员权限"}), 403

    return jsonify({"message": "这是管理员专属页面！"})


# 测试
if __name__ == "__main__":
    print("=== 测试 JWT 认证 ===")

    with app.test_client() as client:
        # 1. 尝试访问受保护接口（未登录）
        resp = client.get("/protected")
        print(f"未登录访问: {resp.status_code} - {resp.json}")

        # 2. 登录获取 Token
        resp = client.post("/login", json={"username": "admin", "password": "admin123"})
        print(f"登录结果: {resp.status_code} - {resp.json}")
        token = resp.json["token"]

        # 3. 带 Token 访问受保护接口
        resp = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
        print(f"带 Token 访问: {resp.status_code} - {resp.json}")

        # 4. 访问管理员接口
        resp = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
        print(f"管理员接口: {resp.status_code} - {resp.json}")

# 运行结果：
# === 测试 JWT 认证 ===
# 未登录访问: 401 - {'error': '没有 Token'}
# 登录结果: 200 - {'token': 'eyJhbGciOiJIUzI1NiJ9...'}
# 带 Token 访问: 200 - {'message': '欢迎，admin！', 'data': {...}}
# 管理员接口: 200 - {'message': '这是管理员专属页面！'}
```

### python-jose——另一种 JWT 实现

`python-jose` 是另一个 JWT 实现库，和 PyJWT 功能类似，但 API 稍有不同。它还支持更多加密算法（RSA、EC 等），适合需要**公私钥签名**的场景。

```python
# python-jose —— PyJWT 的另一个选择
# 安装：pip install python-jose
from jose import jwt, JWTError

# 功能和 PyJWT 几乎一样
# 支持 RSA/EC 等非对称算法（PyJWT 也支持，但 python-jose 更纯粹）

secret_key = "my-secret-key"
token = jwt.encode({"user": "test"}, secret_key, algorithm="HS256")
print(f"Token: {token}")

try:
    data = jwt.decode(token, secret_key, algorithms=["HS256"])
    print(f"解析结果: {data}")
except JWTError as e:
    print(f"错误: {e}")

# 运行结果：
# Token: eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidGVzdCJ9....
# 解析结果: {'user': 'test'}
```

### authlib——OAuth 2.0 的专家

`authlib` 是处理 **OAuth 2.0**（第三方认证）的专业库。当你需要"用 GitHub 登录"、"用 Google 登录"时，就需要 OAuth。

> OAuth 2.0 的原理：你（用户）授权第三方应用访问你的在某个服务商（如 GitHub）上的资源，但第三方应用不知道你的密码。

```python
# authlib + Flask OAuth 客户端示例
# 安装：pip install authlib flask requests
from flask import Flask, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "random-secret-key"

# GitHub OAuth 配置（你需要去 GitHub 申请）
GITHUB_CLIENT_ID = "your_client_id"
GITHUB_CLIENT_SECRET = "your_client_secret"
GITHUB_REDIRECT_URI = "http://localhost:5000/callback"


@app.route("/")
def index():
    """首页"""
    if "user" in session:
        return f'<h1>欢迎，{session["user"]["name"]}！</h1><p><a href="/logout">退出</a></p>'
    return '<h1>请 <a href="/login">用 GitHub 登录</a></h1>'


@app.route("/login")
def login():
    """跳转到 GitHub 授权页面"""
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        "?client_id={}"
        "&redirect_uri={}"
        "&scope=read:user"
    ).format(GITHUB_CLIENT_ID, GITHUB_REDIRECT_URI)
    return redirect(github_auth_url)


@app.route("/callback")
def callback():
    """GitHub 授权回调"""
    code = request.args.get("code")
    if not code:
        return "错误：没有收到授权码", 400

    # 用 code 换 access_token
    token_url = "https://github.com/login/oauth/access_token"
    resp = requests.post(
        token_url,
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code
        },
        headers={"Accept": "application/json"}
    )
    access_token = resp.json().get("access_token")

    if not access_token:
        return "错误：获取 access_token 失败", 400

    # 用 access_token 获取用户信息
    user_resp = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {access_token}"}
    )
    user_data = user_resp.json()

    session["user"] = {
        "name": user_data.get("name"),
        "login": user_data.get("login"),
        "avatar": user_data.get("avatar_url")
    }

    return redirect("/")


@app.route("/logout")
def logout():
    """退出登录"""
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    print("提示：需要配置 GitHub OAuth App 才能完整运行")
    print("访问 https://github.com/settings/developers 创建 OAuth App")
    app.run(port=5000, debug=True)

# 运行结果（需要配置 OAuth）：
# 首页显示"用 GitHub 登录"
# 点击后跳转到 GitHub 授权页面
# 授权后返回首页，显示 GitHub 用户名
```

### 认证方案对比

```
┌─────────────┬───────────────┬───────────────┬───────────────┐
│    方案     │    Session    │      JWT      │    OAuth 2    │
│             │   / Cookie    │               │               │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   状态      │   有状态      │    无状态      │   有/无状态   │
│             │  （服务端存储）│  （Token 自含）│   取决于实现  │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   适用场景  │   传统 Web    │  API / 移动端 │   第三方登录  │
│             │  （MPA）     │  SPA / 微服务  │   开放平台    │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   扩展性    │   较难扩展   │    易于扩展   │    易于扩展    │
│             │  （需要共享）│  （Token 即通行证）│            │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   安全性    │   高          │    中（需 https）│   高        │
│             │  （CSRF 防护）│   （Token 泄漏）│  （令牌机制） │
├─────────────┼───────────────┼───────────────┼───────────────┤
│   实现      │   Flask-      │   PyJWT /     │   authlib     │
│   库        │   Session     │   python-jose │               │
└─────────────┴───────────────┴───────────────┴───────────────┘
```

> 💡 **实战建议**：传统网站用 Session/Cookie；前后端分离的 API 用 JWT；需要接入 Google/GitHub/微信登录用 OAuth。

---

## 本章小结

呼——！这一章信息量爆炸有没有！让我们来总结一下 Python 世界里那些让你"站在巨人肩膀上"的框架们：

### 核心要点回顾

1. **自动化测试**：`pytest` 是 Python 测试的核心武器，fixture 机制让测试数据管理优雅无比；`Selenium` 和 `Playwright` 则负责"真实浏览器"层面的端到端测试，让 bug 无处遁形。

2. **游戏开发**：`Pygame` 是 2D 小游戏的入门神器，两天做出贪吃蛇不是梦；`Godot` + GDScript 则是更专业的选择，2D/3D 通吃，开源免费没烦恼。

3. **GUI 桌面应用**：`Tkinter` 零配置开箱即用；`PyQt5/6` 和 `PySide6` 功能强大适合商业产品，区别主要在许可证——要商用选 LGPL 的 PySide6 准没错。

4. **网络编程**：`socket` 是底层基础，理解 TCP/UDP 必看；`asyncio` 是高并发神器，async/await 语法让你的程序一心多用，处理成千上万并发连接不在话下。

5. **ORM 数据库操作**：`SQLAlchemy` 是老牌全能选手，从简单查询到复杂 JOIN 都能搞定；`Tortoise-ORM` 则是异步时代的产物，和 FastAPI 是绝配。

6. **HTTP 客户端**：`requests` 简单到没朋友，同步代码写起来最顺手；`httpx` 是现代升级版，同步异步无缝切换；`aiohttp` 是纯异步高性能选择，爬虫必备。

7. **认证机制**：`PyJWT` 是生成和验证 Token 的首选，Token 是无状态认证的核心；`authlib` 则负责处理 OAuth 第三方登录，让用户可以"用微信登录"。

### 框架选择决策树

```
┌─────────────────────────────────────────┐
│           我要做什么？                    │
└──────────────────┬──────────────────────┘
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
   测试代码      游戏开发      桌面应用
      │            │            │
   ┌──┴──┐       Pygame       ┌─┴──┐
   │     │                   │     │
  pytest                    Tkinter  PyQt/PySide
   │                        (简单)  (专业)
   ▼
Selenium/Playwright
（浏览器UI测试）
```

```
┌─────────────────────────────────────────┐
│        我要做 Web 开发吗？               │
└──────────────────┬──────────────────────┘
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
   写后端 API    爬虫/客户端    不用 HTTP
      │            │            │
   FastAPI       aiohttp       asyncio
   Django       httpx/        （网络编程）
   Flask        requests
   │
   ▼
  配 ORM
SQLAlchemy/
Tortoise-ORM
```

### 继续保持好奇！

Python 的框架生态是一个**永远学不完**的宝藏。今天学的只是冰山一角：还有 Web 框架（Flask、Django、FastAPI）、数据科学（NumPy、Pandas、Matplotlib）、机器学习（TensorFlow、PyTorch）……

但别慌！框架是"招式"，基础是"内功"。当你 Python 基础扎实了，学任何框架都是**举一反三**的事。所以，继续保持好奇心，继续敲代码，继续踩坑——毕竟，程序员就是这样成长的嘛！

下一章见！ 🚀
