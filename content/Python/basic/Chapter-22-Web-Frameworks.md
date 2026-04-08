+++
title = "第22章 Web框架"
weight = 220
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十二章：Web 框架三巨头 —— Flask、Django、FastAPI

> 💡 **章前趣闻**：想象一下，你开了一家餐厅。Flask 像是只给你一个厨房和灶台，让你自由发挥；Django 则是一条龙的中央厨房，连食材都帮你切好了；FastAPI 呢？它是个带异步魔法的高科技厨房，能同时做好几十道菜而且速度飞快。Web 框架就是程序员的"厨房"，决定你"做菜"的效率和质量！

## 22.1 Flask（轻量级 Web 框架）

Flask 是一位**极简主义建筑师**，它的核心理念是"保持核心功能精炼，允许自由扩展"。如果说 Django 是瑞士军刀（什么都带），那 Flask 就是一把锋利的小刀——轻巧、灵活、你想装什么配件自己决定。

### 22.1.1 安装与第一个应用

**安装 Flask**，简单到怀疑人生：

```bash
pip install flask
```

> 💬 **小知识**：Flask 由 Armin Ronacher 于 2010 年创建，最初只是一个愚人节玩笑（开个玩笑）。实际上它确实诞生于一个叫 Pocoo 的团队，最初是为了满足一个简单需求——做一个够用的 Web 微框架。

**第一个 Flask 应用**，仅需 7 行代码就能跑起来：

```python
from flask import Flask

# 创建 Flask 应用实例
# 这里的 __name__ 参数告诉 Flask 你的模块位置
# 这样它才能找到模板和静态文件
app = Flask(__name__)

# 定义路由：访问根路径时返回 "Hello, World!"
@app.route('/')
def hello():
    return 'Hello, World!'

# 程序入口
if __name__ == '__main__':
    # debug=True 开启调试模式，修改代码后自动重载
    app.run(debug=True, host='0.0.0.0', port=5000)
    # 现在打开浏览器访问 http://127.0.0.1:5000 就能看到效果了
```

运行效果（浏览器访问 `http://127.0.0.1:5000`）：

```
Hello, World!
```

> 🎭 **Flask 运行原理**：Flask 内部使用 Werkzeug（一个 WSGI 工具集）来处理 HTTP 请求。当你访问一个 URL 时，Werkzeug 把请求"翻译"成 Python 能理解的形式，Flask 根据路由找到对应的视图函数，返回响应，Werkzeug 再把响应"翻译"成 HTTP 格式发回给浏览器。Werkzeug 是 Flask 的"首席翻译官"！

### 22.1.2 路由系统

Flask 的路由系统就像**餐厅的菜单系统**，告诉服务器"如果客人点这道菜，就做这个"。路由决定哪个 URL 调用哪个函数。

#### 基础路由：`@app.route`

```python
from flask import Flask

app = Flask(__name__)

# 最简单的路由：根路径
@app.route('/')
def index():
    return '这是首页'

# 访问 /about 就看到这个函数
@app.route('/about')
def about():
    return '这是关于页面'
```

#### 路径参数：动态 URL

路径参数就像是 URL 里的**变量插槽**，让同一个路由模板处理无数个具体 URL。

```python
from flask import Flask

app = Flask(__name__)

# <变量名> 定义路径参数，类型默认是字符串
@app.route('/user/<username>')
def show_user_profile(username):
    # username 会自动传递给函数参数
    return f'用户资料：{username}'

# <int:参数名> 限制参数必须是整数
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # post_id 会是整数类型，而不是字符串
    return f'文章ID：{post_id}，类型是 {type(post_id).__name__}'

# <float:参数名> 限制参数必须是浮点数
@app.route('/price/<float:price>')
def show_price(price):
    return f'价格：{price} 元'

# <path:参数名> 匹配包含斜杠的路径（用于嵌套路径）
@app.route('/files/<path:filepath>')
def show_file(filepath):
    return f'文件路径：{filepath}'
```

运行效果：

```
访问 http://127.0.0.1:5000/user/张三
→ 用户资料：张三

访问 http://127.0.0.1:5000/post/42
→ 文章ID：42，类型是 int

访问 http://127.0.0.1:5000/price/19.99
→ 价格：19.99 元
```

> 📝 **路径参数类型转换器**：
> - `string`（默认）：不包含斜杠的字符串
> - `int`：整数
> - `float`：浮点数
> - `path`：路径，可以包含斜杠
> - `uuid`：UUID 格式的字符串

#### HTTP 方法：GET、POST 等

HTTP 方法就像是**点餐方式**——你是堂食（GET）还是外卖（POST）？

```python
from flask import Flask, request

app = Flask(__name__)

# methods 参数指定允许的 HTTP 方法
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        password = request.form.get('password')
        return f'登录成功：用户名={username}'
    else:
        return '请通过 POST 方法提交登录表单'

# 只接受 GET 请求（默认就是 GET）
@app.route('/search', methods=['GET'])
def search():
    # 获取 URL 查询参数（?key=value）
    query = request.args.get('q', '')
    return f'搜索关键词：{query}'

# RESTful 风格示例
@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book_detail(book_id):
    if request.method == 'GET':
        return f'获取书籍 {book_id} 的详情'
    elif request.method == 'PUT':
        return f'更新书籍 {book_id}'
    elif request.method == 'DELETE':
        return f'删除书籍 {book_id}'
```

运行效果：

```bash
# GET 请求（浏览器直接访问）
curl http://127.0.0.1:5000/search?q=Python
→ 搜索关键词：Python

# POST 请求
curl -X POST http://127.0.0.1:5000/login \
  -d "username=admin&password=123456"
→ 登录成功：用户名=admin
```

> 🎯 **常见 HTTP 方法速查**：
> - `GET`：获取资源（浏览网页、API 查询）—— **只读操作**
> - `POST`：创建新资源（注册、发帖）—— **新增操作**
> - `PUT`：更新资源（完整更新）—— **替换操作**
> - `PATCH`：部分更新资源 —— **修改操作**
> - `DELETE`：删除资源 —— **删除操作**

### 22.1.3 请求与响应对象

Flask 的请求和响应对象就像是**餐厅服务员手中的订单和菜品**——请求对象承载着客人的需求，响应对象是你给客人的"成品"。

#### 请求对象 `request`

`request` 是 Flask 提供的全局对象，包含所有 HTTP 请求信息：

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/demo', methods=['POST'])
def demo_request():
    # 1. 获取查询参数（URL 中 ? 后面的部分）
    # 例如：/demo?page=1&limit=10
    page = request.args.get('page', 1)        # type: ignore
    limit = request.args.get('limit', 10)

    # 2. 获取表单数据（POST 表单提交）
    username = request.form.get('username')
    password = request.form.get('password')

    # 3. 获取 JSON 数据（API 请求常用）
    # Content-Type: application/json
    json_data = request.get_json()
    email = json_data.get('email') if json_data else None

    # 4. 获取请求头信息
    user_agent = request.headers.get('User-Agent')
    auth_token = request.headers.get('Authorization')

    # 5. 获取 URL 路径和完整 URL
    path = request.path          # 例如：/demo
    full_url = request.url       # 例如：http://127.0.0.1:5000/demo?page=1

    # 6. 获取上传的文件
    # <form method="post" enctype="multipart/form-data">
    #   <input type="file" name="myfile">
    # </form>
    uploaded_file = request.files.get('myfile')
    if uploaded_file:
        filename = uploaded_file.filename
        uploaded_file.save(f'/uploads/{filename}')

    # 7. 获取请求方法
    method = request.method  # 'POST'

    return {
        'page': page,
        'limit': limit,
        'username': username,
        'user_agent': user_agent,
        'method': method
    }
```

#### 响应对象 `make_response`

默认 return 的字符串会被包装成响应对象，但有时你需要自定义响应：

```python
from flask import Flask, make_response, jsonify

app = Flask(__name__)

@app.route('/text')
def text_response():
    # 1. 直接返回字符串（自动包装为 HTML 响应）
    return '<h1>这是 HTML</h1>'

@app.route('/json')
def json_response():
    # 2. 返回 JSON（API 开发最常用）
    # jsonify 会自动设置 Content-Type: application/json
    return jsonify({
        'name': '张三',
        'age': 25,
        'skills': ['Python', 'JavaScript']
    })

@app.route('/custom')
def custom_response():
    # 3. 自定义响应（用于设置 Cookie、状态码等）
    response = make_response('操作成功')
    response.status_code = 200
    response.headers['X-Custom-Header'] = 'CustomValue'
    response.set_cookie('session_id', 'abc123')
    return response

@app.route('/redirect')
def redirect_demo():
    # 4. 重定向
    from flask import redirect, url_for
    # url_for 根据函数名生成 URL
    return redirect(url_for('json_response'))

@app.route('/error')
def error_response():
    # 5. 错误响应
    from flask import abort
    abort(404)  # 抛出 404 错误，会被 errorhandler 捕获
    # 或者直接返回错误响应
    return '页面不存在', 404
```

> 💡 **JSON 响应技巧**：`jsonify()` 和直接返回字典的区别是什么？`jsonify()` 会正确设置 `Content-Type` 为 `application/json`，并确保 JSON 格式正确。没有它，浏览器可能把响应当作普通文本处理。

### 22.1.4 模板引擎 Jinja2

Flask 默认使用 **Jinja2** 作为模板引擎。模板引擎就是让你在 HTML 里写 Python 代码的神器——就像是在 HTML 中插入"魔法变量"，自动变成动态内容。

#### 基础模板渲染

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # render_template 会在 templates/ 文件夹下查找模板文件
    # 默认路径：./templates/index.html
    return render_template(
        'index.html',
        title='首页',
        message='欢迎来到 Flask 世界！',
        username='小明',
        items=['苹果', '香蕉', '橙子'],
        is_logged_in=True,
        user={'name': '张三', 'level': 'VIP'},
        price=19.99
    )
```

#### 模板文件 `templates/index.html`

首先创建目录结构：

```
project/
├── app.py
└── templates/
    └── index.html
```

然后编写模板：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <!-- 1. 变量插值：{{ 变量名 }} -->
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    <p>当前用户：{{ username }}</p>

    <!-- 2. 条件判断 -->
    {% if is_logged_in %}
        <p>欢迎回来，会员用户！</p>
    {% else %}
        <p>请 <a href="/login">登录</a></p>
    {% endif %}

    <!-- 3. 循环遍历 -->
    <h2>商品列表</h2>
    <ul>
    {% for item in items %}
        <li>{{ loop.index }}: {{ item }}</li>
    {% endfor %}
    </ul>

    <!-- 4. 访问对象属性 -->
    <p>用户名称：{{ user.name }}</p>
    <p>会员等级：{{ user.level }}</p>

    <!-- 5. 过滤器（管道操作） -->
    <p>价格：{{ price }} 元</p>
    <p>价格（保留2位小数）：{{ price | round(2) }}</p>
    <p>用户名（转大写）：{{ username | upper }}</p>
    <p>用户名（转小写）：{{ username | lower }}</p>
    <p>用户名（首字母大写）：{{ username | capitalize }}</p>
    <p>用户名（未定义时默认）：{{ undefined_var | default("匿名用户") }}</p>

    <!-- 6. 模板继承：子模板可覆盖 content 块 -->
</body>
</html>
```

> 🎭 **Jinja2 过滤器**（类似 Linux 管道 `|`）：
> - `upper` / `lower` / `capitalize`：字符串大小写
> - `trim`：去除首尾空格
> - `length`：获取长度
> - `round(n)`：四舍五入保留 n 位小数
> - `default(value)`：默认值
> - `safe`：标记为安全 HTML（不转义）
> - `join(separator)`：列表拼接
> - `date(format)`：日期格式化

#### 模板继承：告别重复代码

模板继承就像**装修房子的天花板**——定义一次，子模板自动继承！

**基础模板 `templates/base.html`**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}默认标题{% endblock %}</title>
    <!-- 引入 CSS -->
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        nav { background: #333; padding: 10px; }
        nav a { color: white; margin: 0 10px; text-decoration: none; }
        footer { background: #f5f5f5; padding: 20px; text-align: center; margin-top: 50px; }
        .content { padding: 20px; }
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav>
        <a href="/">首页</a>
        <a href="/about">关于</a>
        <a href="/contact">联系</a>
    </nav>

    <!-- 内容区域：子模板可以覆盖这个 block -->
    <div class="content">
        {% block content %}
        <p>默认内容</p>
        {% endblock %}
    </div>

    <!-- 页脚 -->
    <footer>
        <p>&copy; 2026 我的 Flask 网站</p>
    </footer>
</body>
</html>
```

**子模板 `templates/home.html`**：

```html
<!-- 继承基础模板 -->
{% extends "base.html" %}

<!-- 覆盖 title block -->
{% block title %}首页 - 我的网站{% endblock %}

<!-- 覆盖 content block -->
{% block content %}
    <h1>欢迎来到首页！</h1>
    <p>这是一个使用 Flask 和 Jinja2 构建的动态网站。</p>

    <!-- 演示 Jinja2 的内置变量（在 for 循环中可用）-->
    {% for item in items %}
    <p>当前循环索引：{{ loop.index }}</p>
    <p>是否为第一次循环：{{ loop.first }}</p>
    <p>是否为最后一次循环：{{ loop.last }}</p>
    {% endfor %}

{% endblock %}
```

**另一个子模板 `templates/about.html`**：

```html
{% extends "base.html" %}

{% block title %}关于我们{% endblock %}

{% block content %}
    <h1>关于我们</h1>
    <p>我们是一个热爱技术的团队。</p>
    <p>成立于 2020年</p>
{% endblock %}
```

> 💡 **模板继承的核心概念**：
> - `{% extends "base.html" %}`：声明继承哪个模板
> - `{% block block_name %}...{% endblock %}`：定义可覆盖的内容块
> - 子模板只需定义 `block`，其他内容自动继承自父模板

### 22.1.5 会话与 Cookie

**Cookie** 是浏览器存储在用户本地的小文本文件，**会话（Session）**是服务器存储的会话数据。两者配合实现"记住用户状态"的功能。

Cookie 就像是**餐厅会员卡**——你拿着卡（Cookie），服务员知道你是谁、你喜欢什么位置、你上次点了什么菜。会话就是餐厅系统里关于你的那一条记录。

#### Flask 的 Session

Flask 内置的 Session 基于 Cookie，把数据加密后存在客户端：

```python
from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)

# ⚠️ 重要：设置一个强密钥，用于加密 Session 数据
# 在生产环境中，这个密钥要保密且随机生成
app.secret_key = '这是一个超级-secret-key-不要告诉别人！'

@app.route('/')
def index():
    # 检查 session 中是否有用户名
    if 'username' in session:
        return f'已登录：{session["username"]} <a href="/logout">退出</a>'
    return '未登录 <a href="/login">登录</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 简单验证（实际项目要用数据库验证）
        if username == 'admin' and password == '123456':
            # 将用户名存入 session
            session['username'] = username
            session['is_vip'] = True
            return redirect(url_for('index'))
        else:
            return '用户名或密码错误 <a href="/login">重新登录</a>'
    else:
        # 返回登录表单页面
        return '''
        <form method="post">
            用户名：<input type="text" name="username"><br>
            密码：<input type="password" name="password"><br>
            <button type="submit">登录</button>
        </form>
        '''

@app.route('/logout')
def logout():
    # 清除 session
    session.pop('username', None)
    session.pop('is_vip', None)
    return '已退出登录 <a href="/">返回首页</a>'

# Session 配置
@app.route('/set_session')
def set_session():
    session['theme'] = 'dark'
    session['language'] = 'zh-CN'
    return 'Session 已设置'

@app.route('/get_session')
def get_session():
    theme = session.get('theme', 'light')
    return f'当前主题：{theme}'
```

运行效果：

```
访问 http://127.0.0.1:5000/login
→ 显示登录表单

输入 admin / 123456 并提交
→ 重定向到首页，显示 "已登录：admin"

访问 http://127.0.0.1:5000/
→ 显示 "已登录：admin"

访问 http://127.0.0.1:5000/logout
→ "已退出登录"
```

> ⚠️ **Session 安全须知**：
> 1. `secret_key` 必须足够长且随机（至少 32 字节）
> 2. 生产环境使用环境变量设置：`app.secret_key = os.environ.get('SECRET_KEY')`
> 3. Flask Session 存在客户端（Cookie），用户可以查看但无法篡改（因为有签名）

#### 直接操作 Cookie

有时候你需要更精细地控制 Cookie：

```python
from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/set_cookie')
def set_cookie():
    response = make_response('Cookie 已设置')
    # set_cookie(名称, 值, 过期时间秒)
    response.set_cookie('username', '张三', max_age=3600)  # 1小时后过期
    response.set_cookie('is_vip', 'true', max_age=3600*24)  # 1天后过期
    return response

@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username', '游客')
    is_vip = request.cookies.get('is_vip', 'false')
    return f'用户名：{username}，VIP：{is_vip}'

@app.route('/delete_cookie')
def delete_cookie():
    response = make_response('Cookie 已删除')
    response.delete_cookie('username')
    return response
```

### 22.1.6 蓝图（Blueprint）

**蓝图（Blueprint）**是 Flask 用来组织大型应用的结构化方案。就像城市规划——你可以把不同的功能模块划分为不同的"区"，每个区有自己的路由、模板、静态文件。

为什么需要蓝图？想象一个社交网站：
- 用户模块：注册、登录、个人资料
- 帖子模块：发微博、评论、点赞
- 消息模块：私信、通知

不用蓝图 = 所有代码挤在一个文件里，灾难！
用蓝图 = 每个模块独立，代码整洁，可维护性爆表！

#### 基础蓝图使用

创建项目结构：

```
myapp/
├── app.py              # 主应用入口
├── auth.py             # 用户认证蓝图
├── blog.py             # 博客蓝图
└── templates/          # 全局模板
    ├── auth/
    │   └── login.html
    └── blog/
        └── index.html
```

**`auth.py` - 用户认证蓝图**：

```python
from flask import Blueprint, render_template, request, redirect, url_for

# 创建蓝图：第一个参数是蓝图名称，第二个是蓝图所在的模块
# __name__ 帮助 Flask 定位模板和静态文件
auth_bp = Blueprint('auth', __name__, 
                    template_folder='templates')

# 使用 auth_bp.route() 定义路由
@auth_bp.route('/login')
def login():
    return render_template('auth/login.html', title='用户登录')

@auth_bp.route('/register')
def register():
    return '注册页面'

@auth_bp.route('/logout')
def logout():
    return '退出登录'
```

**`blog.py` - 博客蓝图**：

```python
from flask import Blueprint, render_template

blog_bp = Blueprint('blog', __name__,
                    template_folder='templates',
                    url_prefix='/blog')  # 所有路由自动加上 /blog 前缀

@blog_bp.route('/')
def index():
    return render_template('blog/index.html', title='博客首页')

@blog_bp.route('/<int:post_id>')
def detail(post_id):
    return f'文章详情：{post_id}'

@blog_bp.route('/create')
def create():
    return '创建文章'
```

**`app.py` - 主应用**：

```python
from flask import Flask
from auth import auth_bp      # 导入蓝图
from blog import blog_bp

app = Flask(__name__)

# 注册蓝图
# url_prefix 参数会在所有路由前添加前缀
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(blog_bp, url_prefix='/blog')

@app.route('/')
def home():
    return '<h1>首页</h1><ul>' \
           '<li><a href="/auth/login">登录</a></li>' \
           '<li><a href="/blog">博客</a></li>' \
           '</ul>'

if __name__ == '__main__':
    app.run(debug=True)
```

运行效果：

```
http://127.0.0.1:5000/auth/login   → 用户登录页
http://127.0.0.1:5000/auth/register → 注册页面
http://127.0.0.1:5000/blog/        → 博客首页
http://127.0.0.1:5000/blog/42      → 文章详情：42
```

> 💡 **蓝图 URL 反向生成**：使用 `url_for('蓝图名.函数名')` 生成 URL。例如：
> - `url_for('auth.login')` → `/auth/login`
> - `url_for('blog.detail', post_id=5)` → `/blog/5`

#### 蓝图静态文件和 URL 构建

```python
# 创建蓝图时指定静态文件目录
admin_bp = Blueprint('admin', __name__,
                     static_folder='static',      # 静态文件目录
                     static_url_path='/admin_static')  # 访问路径

# 在模板中使用蓝图名生成 URL
# <link rel="stylesheet" href="{{ url_for('admin.static', filename='admin.css') }}">
```

### 22.1.7 Flask-RESTful（RESTful API）

**RESTful API** 是一种设计风格，让 API 遵循"名词而非动词"的约定。Flask-RESTful 是 Flask 官方推荐的 REST API 扩展。

#### 安装与基础使用

```bash
pip install flask-restful
```

```python
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
# 包装 Flask 应用
api = Api(app)

# 定义资源（Resource）是 RESTful 的核心概念
# 每个 Resource 对应一个 URL 端点，自动处理 GET/POST/PUT/DELETE

class HelloWorld(Resource):
    def get(self):
        '''GET 请求返回欢迎信息'''
        return {
            'message': 'Hello, World!',
            'status': 'success'
        }

    def post(self):
        '''POST 请求处理客户端提交的数据'''
        # 从请求体中获取参数
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='姓名不能为空')
        parser.add_argument('age', type=int, default=18)
        args = parser.parse_args()

        return {
            'message': f'欢迎 {args["name"]}！',
            'age': args['age'],
            'status': 'created'
        }, 201  # 201 = Created

# 注册资源到路由
api.add_resource(HelloWorld, '/', '/hello')

if __name__ == '__main__':
    app.run(debug=True)
```

运行效果：

```bash
# GET 请求
curl http://127.0.0.1:5000/
# 返回：
# {
#     "message": "Hello, World!",
#     "status": "success"
# }

# POST 请求
curl -X POST http://127.0.0.1:5000/hello \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "age": 25}'
# 返回（状态码 201）：
# {
#     "message": "欢迎 张三！",
#     "age": 25,
#     "status": "created"
# }
```

#### RESTful 完整示例：Todo API

```python
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

# 模拟数据库
todos = {
    1: {'title': '学 Flask', 'done': False},
    2: {'title': '学 Django', 'done': False},
}

# 请求参数解析器
parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='标题不能为空')
parser.add_argument('done', type=bool, default=False)

def abort_if_todo_not_found(todo_id):
    '''检查 todo 是否存在，不存在则返回 404'''
    if todo_id not in todos:
        abort(404, message=f'Todo {todo_id} 不存在')

class TodoList(Resource):
    '''Todo 列表资源'''

    def get(self):
        '''获取所有 todos'''
        return todos

    def post(self):
        '''创建新 todo'''
        args = parser.parse_args()
        new_id = max(todos.keys(), default=0) + 1
        todos[new_id] = {'title': args['title'], 'done': args['done']}
        return todos[new_id], 201

class Todo(Resource):
    '''单个 Todo 资源'''

    def get(self, todo_id):
        '''获取指定 todo'''
        abort_if_todo_not_found(todo_id)
        return todos[todo_id]

    def put(self, todo_id):
        '''更新指定 todo'''
        abort_if_todo_not_found(todo_id)
        args = parser.parse_args()
        todos[todo_id]['title'] = args['title']
        todos[todo_id]['done'] = args['done']
        return todos[todo_id]

    def delete(self, todo_id):
        '''删除指定 todo'''
        abort_if_todo_not_found(todo_id)
        del todos[todo_id]
        return '', 204  # 204 = No Content

# 注册路由
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
```

运行效果：

```bash
# 获取所有 todos
curl http://127.0.0.1:5000/todos
# [{"title": "学 Flask", "done": false}, {"title": "学 Django", "done": false}]
# 注意：字典的 key 变成了字符串，因为 JSON 格式

# 获取单个 todo
curl http://127.0.0.1:5000/todos/1
# {"title": "学 Flask", "done": false}

# 创建新 todo
curl -X POST http://127.0.0.1:5000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "学 FastAPI", "done": false}'
# 状态码 201

# 更新 todo
curl -X PUT http://127.0.0.1:5000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "学 Flask（已学完）", "done": true}'

# 删除 todo
curl -X DELETE http://127.0.0.1:5000/todos/2

# 访问不存在的 todo
curl http://127.0.0.1:5000/todos/999
# {"message": "Todo 999 不存在"}
# 状态码：404
```

### 22.1.8 Flask 扩展生态

Flask 的强大之处在于它的扩展生态——就像乐高积木，需要什么功能就插什么扩展。

#### Flask-SQLAlchemy（ORM）

**ORM（Object-Relational Mapping）**是对象-关系映射，简单说就是"用 Python 面向对象的方式操作数据库"，不用写 SQL！

```bash
pip install flask-sqlalchemy
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库
# SQLite 格式：sqlite:///数据库名（三个斜杠是相对路径）
# 绝对路径：sqlite:////绝对路径/数据库名
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁止追踪修改，省内存

# 创建数据库实例
db = SQLAlchemy(app)

# 定义模型（类 → 表）
class User(db.Model):
    '''用户表'''
    __tablename__ = 'users'  # 表名，不写默认用类名的小写

    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(80), unique=True, nullable=False)  # 唯一、不能为空
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())  # 创建时间

    # 关系：一对多
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    '''文章表'''
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # ForeignKey 外键关联 users 表的 id

    def __repr__(self):
        return f'<Post {self.title}>'

# 创建表（开发环境用，生产用迁移）
with app.app_context():
    db.create_all()

# CRUD 操作
@app.route('/init')
def init_db():
    # 创建数据
    admin = User(username='admin', email='admin@example.com')
    post1 = Post(title='第一篇文章', content='内容...', author=admin)

    db.session.add(admin)  # 添加到会话
    db.session.add(post1)
    db.session.commit()  # 提交事务

    return '数据库初始化成功！'

@app.route('/users')
def list_users():
    # 查询所有用户
    users = User.query.all()
    return '<br>'.join([f'{u.id}: {u.username} - {u.email}' for u in users])

@app.route('/user/<int:user_id>')
def get_user(user_id):
    # 根据主键查询
    user = User.query.get_or_404(user_id, description='用户不存在')
    return f'{user.username} - {user.email}'

@app.route('/user/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return f'用户 {user.username} 已删除'
    return '用户不存在'

@app.route('/posts')
def list_posts():
    # 过滤查询
    posts = Post.query.filter_by(user_id=1).all()
    return '<br>'.join([f'{p.title} (作者: {p.author.username})' for p in posts])
```

> 🎭 **为什么用 ORM 而不是直接写 SQL？**
> 想象你要查"所有文章及其作者"：
> - **原生 SQL**：`SELECT posts.title, users.username FROM posts JOIN users ON posts.user_id = users.id`
> - **ORM**：`Post.query.join(User).all()` 简直优雅到哭！

#### Flask-Migrate（数据库迁移）

当模型结构变化时，不能直接改表，要用迁移工具：

```bash
pip install flask-migrate
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # 初始化迁移

# 定义模型...
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)  # 新增字段

# 迁移命令（终端执行）：
# flask db init         # 初始化迁移目录
# flask db migrate -m "添加 age 字段"  # 创建迁移脚本
# flask db upgrade      # 执行迁移
# flask db downgrade    # 回滚迁移
```

#### Flask-Login（用户认证）

```bash
pip install flask-login
```

```python
from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # 未登录时重定向到登录页

# 用户模型需要继承 UserMixin
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    '''根据用户 ID 加载用户（必须实现）'''
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return f'''
    <h1>首页</h1>
    <p>当前用户：{current_user.username if current_user.is_authenticated else "未登录"}</p>
    <a href="/login">登录</a> |
    <a href="/logout">退出</a> |
    <a href="/profile">个人资料（需登录）</a>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)  # 登录用户
            next_page = request.args.get('next')  # 登录后跳转
            return redirect(next_page or url_for('index'))
        return '用户名或密码错误'
    return '''
    <form method="post">
        用户名：<input name="username"><br>
        密码：<input name="password" type="password"><br>
        <button>登录</button>
    </form>
    '''

@app.route('/logout')
@login_required  # 必须登录才能访问
def logout():
    logout_user()  # 退出登录
    return '已退出 <a href="/">返回</a>'

@app.route('/profile')
@login_required  # 保护路由
def profile():
    return f'<h1>个人资料</h1><p>欢迎，{current_user.username}！</p>'

# 初始化数据库
with app.app_context():
    db.create_all()
    # 创建测试用户
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', password='123456'))
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
```

### 22.1.9 部署（Gunicorn + Nginx）

开发用 `flask run` 很方便，但生产环境需要更强大的服务器。**Gunicorn** 是一个 Python WSGI HTTP 服务器，**Nginx** 是反向代理服务器。

```mermaid
flowchart LR
    A["用户请求<br/>:443"] --> B["Nginx<br/>反向代理"]
    B --> C["Gunicorn<br/>:8000"]
    C --> D["Flask App"]
    D --> C
    C --> B
    B --> A
```

#### 安装依赖

```bash
# 服务器端安装
pip install gunicorn flask

# Nginx 安装（Linux）
# sudo apt install nginx   # Ubuntu/Debian
# sudo yum install nginx    # CentOS/RHEL
```

#### Gunicorn 配置

```ini
# gunicorn_config.py
import multiprocessing

# 绑定地址和端口
bind = '127.0.0.1:8000'

# 工作进程数（一般设为 CPU 核心数的 2-4 倍）
workers = multiprocessing.cpu_count() * 2

# 工作模式
worker_class = 'sync'  # 同步模式（简单应用）
# worker_class = 'gevent'  # 异步模式（高并发）
# worker_class = 'uvicorn.workers.UvicornWorker'  # 如果用 FastAPI

# 每个 worker 的线程数
threads = 2

# 超时时间（秒）
timeout = 30

# 预加载应用（共享内存，省内存）
preload_app = True

# 日志
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'

# 进程名称
proc_name = 'myflaskapp'

# 协程数（异步 worker 用）
worker_connections = 1000
```

启动 Gunicorn：

```bash
# 基本启动
gunicorn -w 4 -b 127.0.0.1:8000 app:app

# 使用配置文件
gunicorn -c gunicorn_config.py app:app

# 停止旧进程并重启
# kill -HUP $(cat /tmp/gunicorn.pid)  # 平滑重启（重载代码）
# kill -9 $(cat /tmp/gunicorn.pid)    # 强制停止
```

#### Nginx 配置

```nginx
# /etc/nginx/sites-available/myflaskapp
upstream flask_backend {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    server_name example.com www.example.com;

    # 重定向到 HTTPS（如果配置了 SSL）
    # return 301 https://$server_name$request_uri;

    # 访问日志
    access_log /var/log/nginx/myflaskapp_access.log;
    error_log /var/log/nginx/myflaskapp_error.log;

    # 最大上传文件大小
    client_max_body_size 10M;

    location / {
        # 代理到 Gunicorn
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://flask_backend;

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
    }

    # 静态文件（让 Nginx 直接处理，不经过 Flask）
    location /static/ {
        alias /var/www/myflaskapp/static/;
        expires 30d;  # 缓存 30 天
    }

    # 上传文件目录
    location /media/ {
        alias /var/www/myflaskapp/media/;
    }
}
```

启用站点：

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/myflaskapp /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx

# 或者完全重载
sudo systemctl restart nginx
```

> 📝 **生产环境检查清单**：
> 1. ✅ 使用 `gunicorn -D` 或 systemd 后台运行
> 2. ✅ 设置 `SECRET_KEY` 为随机值
> 3. ✅ 生产数据库用 PostgreSQL/MySQL，不要用 SQLite
> 4. ✅ 开启 HTTPS（Let's Encrypt 免费证书）
> 5. ✅ 配置防火墙，只开放 80/443 端口
> 6. ✅ 设置定时任务备份数据库

---

## 22.2 Django（全功能 Web 框架）

Django 是 Python 生态中最"全能"的 Web 框架，被誉为"The Web framework for perfectionists with deadlines"（完美主义者的截止日期救星）。它就像一座**全功能精装房**——厨房、卫生间、卧室全给你装修好了，拎包入住。

Django 的设计哲学是**"不要重复自己"（DRY - Don't Repeat Yourself）**和**"显式优于隐式"**。它内置了 ORM、Admin 后台、表单处理、用户认证、缓存系统、RSS/Atom 订阅、站点地图等功能，基本上市面上网站需要的功能 Django 都帮你做好了。

### 22.2.1 MTV 架构

Django 采用 **MTV 架构**，和传统 MVC 有些区别：

```mermaid
flowchart TB
    subgraph D["Django MTV 架构"]
        direction TB
        M["M - Model<br/>模型层"]
        T["T - Template<br/>模板层"]
        V["V - View<br/>视图层"]
    end

    U["用户请求"] --> W["URL 配置<br/>urls.py"]
    W --> V
    V --> M
    M --> DBase["数据库"]
    V --> T
    T --> H["HTML 响应"]
    H --> U

    style M fill:#FF6B6B,color:#fff
    style T fill:#4ECDC4,color:#fff
    style V fill:#45B7D1,color:#fff
```

| MTV 组件 | 职责 | 类比 |
|---------|------|-----|
| **M - Model** | 数据模型、数据库操作 | 建筑师（设计房屋结构） |
| **T - Template** | 前端模板（HTML） | 室内设计师（装修风格） |
| **V - View** | 业务逻辑 | 大脑（处理请求、返回响应） |

> 💡 **MTV vs MVC**：MTV 的 View 对应 MVC 的 Controller，MTV 的 Template 对应 MVC 的 View。本质上是一样的，只是名字不同。

#### 创建 Django 项目

```bash
# 安装 Django
pip install django

# 创建项目（类似于脚手架）
django-admin startproject mysite

# 创建应用
cd mysite
python manage.py startapp blog

# 目录结构
mysite/
├── manage.py              # 管理脚本
├── mysite/
│   ├── __init__.py
│   ├── settings.py         # 项目配置
│   ├── urls.py             # URL 根配置
│   ├── wsgi.py             # WSGI 入口
│   └── asgi.py             # ASGI 入口（异步）
└── blog/
    ├── __init__.py
    ├── models.py           # 模型定义
    ├── views.py            # 视图函数
    ├── urls.py             # 应用 URL 配置（需创建）
    ├── admin.py            # Admin 配置
    └── ...
```

#### 第一个 Django 应用

**`blog/models.py` - 定义模型**：

```python
from django.db import models

class Article(models.Model):
    '''文章模型'''
    title = models.CharField(max_length=200)      # 标题，最大200字符
    content = models.TextField()                  # 内容，文本
    author = models.CharField(max_length=100)     # 作者
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)      # 更新时间
    is_published = models.BooleanField(default=False)     # 是否发布

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # 默认按创建时间倒序
```

**`blog/views.py` - 定义视图**：

```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article

def index(request):
    '''首页：显示所有已发布的文章'''
    articles = Article.objects.filter(is_published=True)
    return render(request, 'blog/index.html', {'articles': articles})

def detail(request, article_id):
    '''文章详情页'''
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'blog/detail.html', {'article': article})

def about(request):
    '''关于页面'''
    return HttpResponse('这是关于页面')
```

**`blog/urls.py` - 创建 URL 配置**：

```python
from django.urls import path
from . import views

app_name = 'blog'  # 命名空间，用于 url 反查

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('about/', views.about, name='about'),
]
```

**`mysite/urls.py` - 根 URL 配置**：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),        # Admin 后台
    path('blog/', include('blog.urls')),     # 引入 blog 应用的 URL
]
```

**`blog/templates/blog/index.html` - 模板**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>我的博客</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        .article { border-bottom: 1px solid #ddd; padding: 10px 0; }
        h1 { color: #333; }
        .meta { color: #888; font-size: 0.9em; }
    </style>
</head>
<body>
    <h1>📚 我的博客</h1>
    <a href="/admin">管理后台</a>
    <hr>

    {% for article in articles %}
    <div class="article">
        <h2><a href="{% url 'blog:detail' article.id %}">{{ article.title }}</a></h2>
        <p class="meta">作者：{{ article.author }} | 发布时间：{{ article.created_at|date:"Y-m-d H:i" }}</p>
        <p>{{ article.content|truncatewords:30 }}</p>
    </div>
    {% empty %}
    <p>暂无文章</p>
    {% endfor %}
</body>
</html>
```

**运行开发服务器**：

```bash
python manage.py runserver
# Watching for file changes with StatReloader
# Starting development server at http://127.0.0.1:8000/

# 创建数据表
python manage.py makemigrations  # 生成迁移文件
python manage.py migrate          # 执行迁移
```

> 🎭 **Django 命令速记**：`makemigrations` = 写 SQL 语句（还没执行），`migrate` = 真正执行 SQL 创建表。

### 22.2.2 ORM 深度教程

Django ORM 是 Python Web 框架中最强大的数据库抽象层，让你用 Python 代码操作数据库，完全不用写 SQL！

#### 字段类型详解

```python
from django.db import models

class Author(models.Model):
    '''作者模型'''
    name = models.CharField(max_length=100)  # 字符串，最大100字符
    email = models.EmailField()              # 邮箱格式验证
    bio = models.TextField()                 # 长文本
    birth_date = models.DateField()          # 日期
    phone = models.CharField(max_length=20, blank=True, null=True)  # 可选
    website = models.URLField(blank=True)    # URL 格式验证

class Book(models.Model):
    '''书籍模型'''
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 精确小数
    pages = models.IntegerField(default=0)    # 整数
    rating = models.FloatField(default=0.0)   # 浮点数
    is_available = models.BooleanField(default=True)
    published_date = models.DateField()

    # ForeignKey：一对多关系（一个作者 → 多本书）
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    # ManyToManyField：多对多关系（一本书 → 多个标签，一个标签 → 多本书）
    tags = models.ManyToManyField('Tag', related_name='books')

    def __str__(self):
        return self.title

class Tag(models.Model):
    '''标签模型'''
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    '''出版社模型'''
    name = models.CharField(max_length=100)
    # OneToOneField：一对一关系（用户表扩展信息）
    user = models.OneToOneField('User', on_delete=models.CASCADE)
```

> 📝 **字段参数说明**：
> - `max_length`：最大字符数
> - `blank=True`：表单验证时允许空字符串（可选）
> - `null=True`：数据库允许 NULL 值
> - `default`：默认值
> - `unique`：唯一约束
> - `choices`：选项列表（类似枚举）
> - `auto_now_add`：创建时自动设置时间
> - `auto_now`：每次保存时自动更新时间

#### ForeignKey（外键）详解

```python
class Comment(models.Model):
    '''评论模型 - 展示自引用外键'''
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 自引用外键：评论可以回复评论
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)

    # related_name='comments' 允许反向查询：
    # article.comments.all() 获取某文章的所有评论
```

#### 查询操作

Django ORM 的查询接口非常丰富：

```python
from blog.models import Article, Author, Book

# ===== 基本查询 =====

# 获取所有记录
all_articles = Article.objects.all()

# 获取第一条/最后一条
first = Article.objects.first()
last = Article.objects.last()

# 获取单个记录（不存在抛异常）
article = Article.objects.get(pk=1)

# 获取数量
count = Article.objects.count()

# ===== 过滤查询（filter）=====

# 精确匹配
published_articles = Article.objects.filter(is_published=True)

# 模糊匹配（包含）
python_articles = Article.objects.filter(title__contains='Python')

# 不区分大小写
python_articles = Article.objects.filter(title__icontains='python')

# 开头/结尾匹配
starts_with = Article.objects.filter(title__startswith='Django')
ends_with = Article.objects.filter(title__endswith='入门')

# 范围查询
from datetime import datetime
recent = Article.objects.filter(created_at__gte=datetime(2026, 1, 1))
price_range = Book.objects.filter(price__gte=20, price__lte=50)

# in 查询
authors = Author.objects.filter(id__in=[1, 2, 3])

# ===== 排除查询（exclude）=====

# 排除已发布的
drafts = Article.objects.exclude(is_published=True)

# ===== 排序 =====
ascending = Article.objects.order_by('created_at')      # 升序
descending = Article.objects.order_by('-created_at')     # 降序（减号）
multi = Book.objects.order_by('author__name', '-price') # 多字段排序

# ===== 聚合查询 =====
from django.db.models import Count, Sum, Avg, Max, Min

# 统计每个作者的书量
author_books = Author.objects.annotate(book_count=Count('books'))

# 统计总收入
total_revenue = Book.objects.aggregate(total=Sum('price'))

# 平均价格
avg_price = Book.objects.aggregate(avg=Avg('price'))

# ===== 分组查询 =====
from django.db.models import Count

# 每个作者的书量统计
authors_with_books = Author.objects.annotate(book_count=Count('books')).filter(book_count__gt=0)

# ===== 链式查询 =====
# Django ORM 支持无限链式调用
result = Article.objects \
    .filter(is_published=True) \
    .exclude(author='匿名') \
    .order_by('-created_at') \
    [:10]  # 取前10条

# ===== F 表达式（字段间比较）=====
from django.db.models import F

# 查找价格大于库存的书籍（奇怪的业务逻辑）
weird_books = Book.objects.filter(price__gt=F('stock'))

# 打折：所有书籍价格打 9 折
Book.objects.update(price=F('price') * 0.9)

# ===== Q 对象（复杂查询）=====
from django.db.models import Q

# OR 查询：标题包含 "Python" 或 "Django" 的文章
articles = Article.objects.filter(
    Q(title__contains='Python') | Q(title__contains='Django')
)

# AND 查询：已发布且作者是 "张三"
articles = Article.objects.filter(
    Q(is_published=True) & Q(author='张三')
)

# NOT 查询：不是 "张三" 写的文章
articles = Article.objects.filter(~Q(author='张三'))

# ===== 关联查询（跨表查询）=====
# 正向查询：通过外键访问
book = Book.objects.get(pk=1)
author_name = book.author.name  # 通过外键获取作者名

# 反向查询：通过 related_name
author = Author.objects.get(pk=1)
books = author.books.all()  # 获取该作者的所有书籍

# 使用双下划线跨表查询（JOIN）
# 查找作者是 "张三" 的所有书籍
books = Book.objects.filter(author__name='张三')

# 查找包含 "Python" 标签的所有书籍
books = Book.objects.filter(tags__name='Python')

# 查找作者居住在城市是 "北京" 的书籍
books = Book.objects.filter(author__city='北京')

# 去重
unique_books = Book.objects.filter(tags__name__in=['Python', 'Django']).distinct()
```

> 💡 **QuerySet 特性**：
> 1. **惰性执行**：QuerySet 创建时不执行数据库查询，直到真正需要数据时才执行
> 2. **可复用**：可以无限链式调用
> 3. **可缓存**：同一个 QuerySet 执行两次只查一次数据库

#### 增删改操作

```python
# ===== 创建记录 =====

# 方法1：save() 方法
article = Article()
article.title = 'Django 入门'
article.content = 'Django 是一个全能框架...'
article.author = '张三'
article.is_published = True
article.save()

# 方法2：create() 方法（一步到位）
article = Article.objects.create(
    title='FastAPI 入门',
    content='FastAPI 是现代高性能框架...',
    author='李四',
    is_published=True
)

# 方法3：get_or_create()（存在则获取，不存在则创建）
article, created = Article.objects.get_or_create(
    title='Django 入门',
    defaults={'content': '默认内容', 'author': '张三'}
)
# created 为 True 表示新建，False 表示已存在

# ===== 更新记录 =====

# 方法1：修改后 save()
article = Article.objects.get(pk=1)
article.title = '新标题'
article.save()  # 更新所有字段

# 方法2：update() 批量更新（只更新指定字段，不调用 save()）
Article.objects.filter(pk=1).update(title='批量更新标题', is_published=False)
Article.objects.all().update(is_published=True)  # 全部更新

# ===== 删除记录 =====

# 删除单条
article = Article.objects.get(pk=1)
article.delete()  # 返回被删除的数量

# 批量删除
Article.objects.filter(is_published=False).delete()

# ===== 事务操作 =====
from django.db import transaction

with transaction.atomic():
    # 创建一个作者
    author = Author.objects.create(name='王五', email='wang@example.com')
    # 创建两本书
    Book.objects.create(title='书1', author=author, price=30)
    Book.objects.create(title='书2', author=author, price=40)
    # 如果中间出错，整个事务回滚
```

### 22.2.3 Admin 后台

Django Admin 是 Django 自带的**神器级后台管理界面**，让你不用写代码就能管理数据。

#### 基本配置

**`blog/admin.py`**：

```python
from django.contrib import admin
from .models import Article, Author, Book

# 注册模型到 Admin
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    '''文章 Admin 配置'''
    list_display = ['title', 'author', 'is_published', 'created_at']  # 列表页显示的字段
    list_filter = ['is_published', 'author', 'created_at']             # 过滤侧边栏
    search_fields = ['title', 'content']                                # 搜索框
    ordering = ['-created_at']                                          # 默认排序
    date_hierarchy = 'created_at'                                        # 日期层级导航
    list_per_page = 20                                                  # 每页数量

    # 字段分组（编辑页）
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'author')
        }),
        ('内容', {
            'fields': ('content',)
        }),
        ('状态', {
            'fields': ('is_published',)
        }),
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'get_book_count']
    search_fields = ['name', 'email']

    def get_book_count(self, obj):
        return obj.books.count()
    get_book_count.short_description = '书籍数量'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'is_available']
    list_filter = ['is_available', 'author']
    search_fields = ['title']
    date_hierarchy = 'published_date'
```

运行服务器，访问 `http://127.0.0.1:8000/admin/`：

```bash
python manage.py createsuperuser
# 输入用户名、邮箱、密码
# 访问管理后台
```

#### Admin 进阶配置

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 操作按钮
    actions = ['publish_articles', 'unpublish_articles']

    @admin.action(description='发布选中文章')
    def publish_articles(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} 篇文章已发布')

    @admin.action(description='取消发布选中文章')
    def unpublish_articles(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} 篇文章已取消发布')

    # 只读字段
    readonly_fields = ['created_at', 'updated_at']

    # 字段布局
    save_on_top = True  # 顶部也显示保存按钮
```

### 22.2.4 表单（Forms）

Django Forms 就像**自动化的表单处理流水线**——验证、清洗、渲染、错误提示，全自动！

#### 表单基础

**`forms.py`**：

```python
from django import forms

class ContactForm(forms.Form):
    '''联系表单'''
    name = forms.CharField(max_length=100, label='姓名')
    email = forms.EmailField(label='邮箱')
    subject = forms.CharField(max_length=200, label='主题')
    message = forms.CharField(widget=forms.Textarea, label='留言内容')

    # 自定义验证
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError('留言内容至少10个字符')
        return message

class ArticleForm(forms.ModelForm):
    '''基于模型的表单（自动对应模型字段）'''

    class Meta:
        model = Article  # 对应的模型
        fields = ['title', 'content', 'author', 'is_published']  # 包含的字段
        # 或者排除：exclude = ['created_at', 'updated_at']

    # 添加额外字段
    cc_myself = forms.BooleanField(required=False, label='抄送自己')

    # 自定义验证
    def clean_title(self):
        title = self.cleaned_data['title']
        if 'Django' in title and '烂' in title:
            raise forms.ValidationError('不能贬低 Django！')
        return title
```

**`views.py`**：

```python
from django.shortcuts import render
from .forms import ContactForm, ArticleForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.cleaned_data 包含验证后的数据
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            # ... 处理数据，发送邮件等
            return render(request, 'contact_success.html', {'name': name})
    else:
        form = ContactForm()  # 空表单

    return render(request, 'contact.html', {'form': form})
```

**`templates/contact.html`**：

```html
<!DOCTYPE html>
<html>
<head>
    <title>联系我们</title>
    <style>
        .errorlist { color: red; list-style: none; padding: 0; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>联系我们</h1>
    <form method="post">
        {% csrf_token %}
        <!-- form.as_p 以段落形式渲染 -->
        {{ form.as_p }}
        <button type="submit">提交</button>
    </form>
</body>
</html>
```

> 💡 **Django 表单的自动功能**：
> 1. 自动验证输入（类型、长度、格式）
> 2. 自动转义 XSS 攻击
> 3. 自动显示错误信息
> 4. 自动 CSRF 保护（`{% csrf_token %}`）

#### 表单渲染方式

```html
<!-- 方式1：as_p 每个字段一个段落 -->
{{ form.as_p }}

<!-- 方式2：as_table 渲染成表格 -->
<table>
{{ form.as_table }}
</table>

<!-- 方式3：as_ul 渲染成列表 -->
<ul>
{{ form.as_ul }}
</ul>

<!-- 方式4：手动渲染每个字段 -->
<div class="form-group">
    <label for="{{ form.name.id_for_label }}">{{ form.name.label }}</label>
    {{ form.name }}
    {% if form.name.errors %}
        <ul class="errorlist">
        {% for error in form.name.errors %}
            <li>{{ error }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</div>
```

### 22.2.5 中间件（Middleware）

**中间件**是 Django 请求/响应处理流水线上的"质检员"——每个请求和响应都会经过中间件，可以对它们进行检查、修改、拦截。

```mermaid
flowchart TB
    subgraph MIDDLEWARE["Django 请求处理流水线"]
        direction TB
        R["请求 Request"]
        M1["中间件1<br/>（如 SessionMiddleware）"]
        M2["中间件2<br/>（如 AuthenticationMiddleware）"]
        M3["中间件3<br/>（如 CommonMiddleware）"]
        V["View 视图"]
        M3R["中间件3（响应）"]
        M2R["中间件2（响应）"]
        M1R["中间件1（响应）"]
        RESP["响应 Response"]
    end

    R --> M1 --> M2 --> M3 --> V
    V --> M3R --> M2R --> M1R --> RESP

    style M1 fill:#FF6B6B,color:#fff
    style M2 fill:#4ECDC4,color:#fff
    style M3 fill:#45B7D1,color:#fff
    style V fill:#FFE66D
```

#### 内置中间件

**`mysite/settings.py`**：

```python
MIDDLEWARE = [
    # 1. 安全中间件
    'django.middleware.security.SecurityMiddleware',  # HTTPS 重定向等

    # 2. Session 中间件
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 开启后 request.session 可用

    # 3. 通用中间件
    'django.middleware.common.CommonMiddleware',
    # 处理 URL、禁止访问等

    # 4. CSRF 保护
    'django.middleware.csrf.CsrfViewMiddleware',
    # POST 请求验证 csrf_token

    # 5. 认证中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 开启后 request.user 可用

    # 6. 消息框架
    'django.contrib.messages.middleware.MessageMiddleware',

    # 7. 点击劫持保护
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

#### 自定义中间件

```python
# mysite/middleware.py

class MyMiddleware:
    '''自定义中间件类'''

    def __init__(self, get_response):
        '''服务器启动时调用一次'''
        self.get_response = get_response

    def __call__(self, request):
        '''每个请求都会调用'''
        # 请求处理前的代码（从左到右）
        print(f'请求路径: {request.path}')

        response = self.get_response(request)

        # 响应处理前的代码（从右到左）
        response['X-Custom-Header'] = 'Hello from Middleware'

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        '''在调用视图之前调用'''
        # 可以在这里做权限检查
        # 返回 None 继续处理，返回 HttpResponse 短路
        pass

    def process_exception(self, request, exception):
        '''视图抛出异常时调用'''
        # 可以在这里记录日志、发送告警
        print(f'异常: {exception}')
        return None  # 返回 None 交给其他处理器

class AdminAccessMiddleware:
    '''限制后台访问来源'''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 只允许特定 IP 访问 admin
        if request.path.startswith('/admin/'):
            allowed_ips = ['127.0.0.1', '192.168.1.100']
            client_ip = request.META.get('REMOTE_ADDR')
            if client_ip not in allowed_ips:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden('禁止访问')

        return self.get_response(request)
```

在 `settings.py` 中注册：

```python
MIDDLEWARE = [
    # ...
    'mysite.middleware.MyMiddleware',
    'mysite.middleware.AdminAccessMiddleware',
]
```

### 22.2.6 用户认证与权限

Django 内置了完整的用户认证系统，开箱即用！

#### 内置 User 模型

```python
from django.contrib.auth.models import User

# User 常用字段：
# username, email, password, first_name, last_name
# is_active, is_staff, is_superuser, date_joined
# last_login

# 创建用户（明文密码会自动哈希）
user = User.objects.create_user('zhangsan', 'zhang@example.com', 'password123')

# 创建超级用户
python manage.py createsuperuser

# 设置密码
user.set_password('newpassword')
user.save()

# 验证密码
from django.contrib.auth import authenticate
user = authenticate(username='zhangsan', password='password123')
if user:
    print('验证成功')
else:
    print('密码错误')
```

#### 登录/登出/权限装饰器

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def user_login(request):
    '''登录视图'''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  # 登录（写入 session）
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html')

def user_logout(request):
    '''登出视图'''
    logout(request)
    return redirect('home')

@login_required(login_url='/login/')  # 未登录重定向到登录页
def profile(request):
    '''个人资料（必须登录）'''
    return render(request, 'profile.html', {'user': request.user})

@permission_required('auth.change_user', raise_exception=True)  # 需要特定权限
def manage_users(request):
    '''用户管理（需要 change_user 权限）'''
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})
```

#### 自定义用户模型

有时内置 User 模型不够用（比如需要手机号登录）：

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    '''扩展用户模型'''
    phone = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(verbose_name='个人简介')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

# settings.py
AUTH_USER_MODEL = 'accounts.AppUser'  # 替换内置 User 模型

# 其他模型中引用用户
class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

> ⚠️ **警告**：必须在 `startapp` 后、`makemigrations` 前设置 `AUTH_USER_MODEL`，否则需要数据迁移。

### 22.2.7 DRF（Django REST Framework）

**Django REST Framework（DRF）** 是 Django 的 RESTful API 框架，让构建 API 变得优雅而强大。

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

#### Serializer（序列化器）

```python
# blog/serializers.py
from rest_framework import serializers
from .models import Article, Author

class AuthorSerializer(serializers.ModelSerializer):
    '''作者序列化器'''
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio']
        # fields = '__all__'  # 包含所有字段

class ArticleSerializer(serializers.ModelSerializer):
    '''文章序列化器'''
    # 显示作者名称（而不是 ID）
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'author_name',
                  'is_published', 'created_at']
        read_only_fields = ['created_at']

class ArticleSerializerDeep(serializers.ModelSerializer):
    '''嵌套作者信息的文章序列化器'''
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'author_id',
                  'is_published', 'created_at']
```

#### ViewSet 和路由

```python
# blog/views.py
from rest_framework import viewsets, permissions
from .models import Article, Author
from .serializers import ArticleSerializer, AuthorSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    '''
    自动提供 CRUD 全部操作：
    - GET /articles/          列表
    - POST /articles/          创建
    - GET /articles/{id}/      详情
    - PUT /articles/{id}/      更新
    - PATCH /articles/{id}/    部分更新
    - DELETE /articles/{id}/   删除
    '''
    queryset = Article.objects.filter(is_published=True)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # 自动设置作者为当前登录用户
        serializer.save(author=self.request.user)

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    '''只读视图集（只能查看，不能修改）'''
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
```

#### URL 配置

```python
# blog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'authors', views.AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

现在你就有了一个完整的 RESTful API！

```bash
GET    /api/articles/           # 列表
POST   /api/articles/           # 创建
GET    /api/articles/1/         # 详情
PUT    /api/articles/1/          # 更新
DELETE /api/articles/1/         # 删除
```

### 22.2.8 信号（Signals）机制

Django 信号就像是**事件监听器**——当某个动作发生时，自动触发你注册的回调函数。

```mermaid
flowchart LR
    A["Django 信号"] --> B["model.post_save<br/>模型保存后"]
    A --> C["model.pre_delete<br/>模型删除前"]
    A --> D["user.login<br/>用户登录后"]
    A --> E["request_started<br/>请求开始"]

    B --> H["发送欢迎邮件"]
    C --> I["删除相关缓存"]
    D --> J["记录登录日志"]
    E --> K["记录请求日志"]
```

#### 内置信号示例

```python
# blog/signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Article, Comment

@receiver(post_save, sender=Article)
def article_saved(sender, instance, created, **kwargs):
    '''文章保存后触发'''
    if created:
        print(f'新文章创建: {instance.title}')
        # 发送邮件通知
        # send_mail(
        #     '新文章发布',
        #     f'{instance.title} 已发布！',
        #     'admin@example.com',
        #     ['subscribers@example.com']
        # )
    else:
        print(f'文章更新: {instance.title}')

@receiver(pre_delete, sender=Article)
def article_deleted(sender, instance, **kwargs):
    '''文章删除前触发'''
    print(f'文章将被删除: {instance.title}')
    # 清理相关资源：删除图片、清理缓存等

@receiver(post_save, sender=Comment)
def comment_added(sender, instance, created, **kwargs):
    '''有新评论时通知作者'''
    if created:
        article = instance.article
        print(f'用户 {instance.author_name} 评论了文章: {article.title}')
        # 发送通知邮件给文章作者
```

#### 注册信号

在 `apps.py` 中注册信号：

```python
# blog/apps.py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        # 导入信号模块，触发装饰器注册
        import blog.signals
```

#### 自定义信号

```python
from django.dispatch import Signal, receiver

# 定义自定义信号
order_completed = Signal()

@receiver(order_completed)
def send_order_notification(sender, order, **kwargs):
    '''订单完成后发送通知'''
    print(f'订单 {order.id} 已完成，准备发送通知...')
    # 发送短信、邮件等

# 触发信号
order_completed.send(sender=None, order=my_order)
```

### 22.2.9 部署（uWSGI + Nginx + Docker）

生产环境部署 Django 推荐组合：**uWSGI + Nginx + Docker**。

#### uWSGI 配置

```ini
# uwsgi.ini
[uwsgi]
# 基础配置
socket = 127.0.0.1:8000
master = true
processes = 4
threads = 2

# Python 配置
module = mysite.wsgi:application
home = /var/www/mysite/venv
pythonpath = /var/www/mysite

# 虚拟环境
virtualenv = /var/www/mysite/venv

# 日志
daemonize = /var/log/uwsgi/mysite.log
log-maxsize = 10000000

# 进程管理
max-requests = 1000
vacuum = true
die-on-term = true

# 缓存优化
lazy-apps = true
```

#### Nginx 配置

```nginx
upstream django_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name example.com;
    charset utf-8;

    client_max_body_size 50M;

    location /static/ {
        alias /var/www/mysite/static/;
        expires 7d;
        access_log off;
    }

    location /media/ {
        alias /var/www/mysite/media/;
    }

    location / {
        uwsgi_pass django_app;
        include /etc/nginx/uwsgi_params;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Docker 部署

**`Dockerfile`**：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 运行方式
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "mysite.wsgi:application"]
```

**`docker-compose.yml`**：

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=0
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine

volumes:
  postgres_data:
```

启动：

```bash
docker-compose up -d
docker-compose logs -f web
```

> 📝 **生产环境检查清单**：
> 1. ✅ `DEBUG = False`（关闭调试模式）
> 2. ✅ `ALLOWED_HOSTS` 设置正确
> 3. ✅ 使用 PostgreSQL/MySQL
> 4. ✅ 配置 Redis 缓存
> 5. ✅ 使用 HTTPS（Let's Encrypt）
> 6. ✅ 设置定时任务备份
> 7. ✅ 日志收集和监控

---

## 22.3 FastAPI（现代高性能 API 框架）

**FastAPI** 是 2018 年诞生的"新生儿"，但它已经席卷了 Python API 开发界。它就像是**高铁和飞机的结合体**——既有 Python 的简洁，又有异步的高性能，还有自动生成的 API 文档。

FastAPI 的设计哲学是：**开发者体验第一，性能第二，类型安全贯穿始终**。

### 22.3.1 异步框架基础

在了解 FastAPI 之前，必须理解**异步编程**。想象你是餐厅服务员：

- **同步模式**：你端着菜走到 1 号桌，放下菜，等客人吃完，收回盘子，再去 2 号桌... 一个一个来
- **异步模式**：你把菜放到 1 号桌，告诉厨房继续做着，然后去 2 号桌点单，1 号桌吃完了你再回来收钱... 不用干等

异步让一个服务员（线程）能同时服务多个桌子（请求），效率飙升！

#### 同步 vs 异步代码

```python
# 同步函数（普通函数）
def sync_function():
    return "同步结果"

# 异步函数（async/await）
import asyncio

async def async_function():
    return "异步结果"

# 运行异步函数
async def main():
    result = await async_function()  # await 等待异步函数完成
    print(result)

# asyncio.run(main())
```

#### FastAPI 异步基础

```bash
pip install fastapi uvicorn
```

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

# 同步路径操作
@app.get("/sync")
def sync_endpoint():
    """同步函数，直接返回"""
    return {"type": "sync", "data": [1, 2, 3]}

# 异步路径操作
@app.get("/async")
async def async_endpoint():
    """异步函数，可以用 await"""
    # 模拟异步操作（如数据库查询）
    await asyncio.sleep(1)  # 模拟耗时操作
    return {"type": "async", "data": [4, 5, 6]}

# 混合使用
@app.get("/mixed/{item_id}")
async def mixed_endpoint(item_id: int):
    # 同步操作直接用
    result = sync_function()

    # 异步操作用 await
    await asyncio.sleep(0.5)

    return {"item_id": item_id, "result": result}
```

运行：

```bash
uvicorn main:app --reload
# INFO: Uvicorn running on http://127.0.0.1:8000
# 访问 http://127.0.0.1:8000/docs 查看自动生成的 API 文档
```

> 💡 **什么时候用 async**：
> - I/O 密集型：数据库查询、文件读写、网络请求 → 用 `async def` + `await`
> - CPU 密集型：复杂计算、图片处理 → 用普通 `def`（同步函数会被自动在线程池中运行）

### 22.3.2 路由与路径参数

FastAPI 的路由系统和 Flask 类似，但更强大——自动参数类型转换和验证。

```python
from fastapi import FastAPI

app = FastAPI()

# ===== 基础路由 =====
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

@app.post("/items/")
async def create_item(name: str, price: float):
    return {"name": name, "price": price}

# ===== 路径参数 =====
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """路径参数，自动类型转换（字符串 "123" → int 123）"""
    return {"item_id": item_id, "type": type(item_id).__name__}

@app.get("/users/{user_id}/posts/{post_id}")
async def get_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}

# ===== 查询参数 =====
@app.get("/search")
async def search(q: str, limit: int = 10, offset: int = 0):
    """查询参数，带默认值"""
    return {
        "query": q,
        "limit": limit,
        "offset": offset,
        "results": [f"结果{i}" for i in range(offset, min(offset + limit, 20))]
    }

@app.get("/products")
async def list_products(category: str = None, on_sale: bool = False):
    """可选查询参数"""
    return {"category": category, "on_sale": on_sale}

# ===== 组合：路径参数 + 查询参数 =====
@app.get("/stores/{store_id}/items")
async def get_store_items(store_id: int, min_price: float = None):
    return {"store_id": store_id, "min_price": min_price}
```

运行效果：

```bash
curl http://127.0.0.1:8000/items/42
# {"item_id":42,"type":"int"}

curl "http://127.0.0.1:8000/search?q=Python&limit=5"
# {"query":"Python","limit":5,"offset":0,"results":["结果0","结果1","结果2","结果3","结果4"]}
```

#### 请求体（Request Body）

```python
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

# 定义数据模型（Pydantic）
class Item(BaseModel):
    """商品模型"""
    name: str                    # 必需字段
    description: str = None      # 可选字段，默认 None
    price: float                 # 必需
    quantity: int = 0            # 可选，默认 0
    tags: list[str] = []         # 列表，默认空列表
    is_active: bool = True

class User(BaseModel):
    """用户模型"""
    username: str
    email: str
    age: int = None

# 使用 Request Body
@app.post("/items/")
async def create_item(item: Item):
    """Request Body 是 Item 类型"""
    # Pydantic 自动验证数据
    return {"item": item, "status": "created"}

@app.post("/users/")
async def create_user(user: User):
    """创建用户"""
    return {"user": user, "status": "created"}

# 多个 Request Body
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    """路径参数 + 两个 Request Body"""
    return {
        "item_id": item_id,
        "item": item,
        "updated_by": user.username
    }
```

### 22.3.3 Pydantic 数据验证

**Pydantic** 是 Python 最强大的数据验证库，FastAPI 用它来做请求验证。简单说就是"把你的数据定义成模型，Pydantic 自动帮你验证"。

```python
from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ===== 基础验证 =====
class Product(BaseModel):
    name: str                                    # 必需字符串
    price: float = Field(..., gt=0)             # 必须大于 0
    stock: int = Field(default=0, ge=0)         # 大于等于 0
    description: Optional[str] = None          # 可选字符串
    sku: str = Field(min_length=3, max_length=20)  # 长度限制

# ===== 枚举类型 =====
class Size(str, Enum):
    """尺码枚举"""
    SMALL = "s"
    MEDIUM = "m"
    LARGE = "l"
    EXTRA_LARGE = "xl"

class ClothingItem(BaseModel):
    name: str
    size: Size  # 只能是枚举值

# ===== 嵌套模型 =====
class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class Customer(BaseModel):
    name: str
    email: EmailStr  # 自动验证邮箱格式
    phone: Optional[str] = None
    addresses: List[Address] = []  # 嵌套列表

# ===== 自定义验证器 =====
class UserRegistration(BaseModel):
    username: str
    password: str
    password_confirm: str
    age: int = Field(ge=13, le=120)  # 年龄限制

    @validator('password_confirm')
    def passwords_match(cls, v, values):
        if v != values.get('password'):
            raise ValueError('两次密码不一致')
        return v

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v.lower()

# ===== 实际使用 =====
@app.post("/products/")
async def create_product(product: Product):
    return {"product": product.model_dump()}

@app.post("/register/")
async def register(user: UserRegistration):
    return {"message": "注册成功", "user": user.username}

@app.post("/customers/")
async def create_customer(customer: Customer):
    return customer.model_dump()
```

运行效果：

```bash
# 正常请求
curl -X POST http://127.0.0.1:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "T-shirt", "price": 29.99, "stock": 100}'
# 返回：验证通过

# 错误请求（price <= 0）
curl -X POST http://127.0.0.1:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "T-shirt", "price": -10, "stock": 100}'
# 返回 422 Unprocessable Entity：
# {
#   "detail": [
#     {
#       "loc": ["body", "price"],
#       "msg": "ensure this value is greater than 0",
#       "type": "value_error"
#     }
#   ]
# }
```

> 💡 **Pydantic Field 参数**：
> - `...`（省略号）：必需字段
> - `default`：默认值
> - `gt` / `ge`：大于 / 大于等于
> - `lt` / `le`：小于 / 小于等于
> - `min_length` / `max_length`：字符串/列表长度限制
> - `regex`：正则表达式验证
> - `alias`：字段别名

### 22.3.4 依赖注入系统

FastAPI 的**依赖注入（Dependency Injection）**系统非常强大——想象它是"自动供应链"，你需要什么，FastAPI 自动给你送上门。

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# ===== 简单依赖函数 =====
def get_query_param(name: str = "Guest"):
    """简单依赖：返回用户名"""
    return name

@app.get("/greet")
async def greet(name: str = Depends(get_query_param)):
    return {"greeting": f"你好, {name}!"}

# ===== 带逻辑的依赖 =====
def verify_api_key(x_api_key: str = Header(...)):
    """验证 API Key"""
    if x_api_key != "secret-key-123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的 API Key"
        )
    return {"api_key": x_api_key}

@app.get("/protected")
async def protected(api_key: dict = Depends(verify_api_key)):
    return {"message": "已授权访问", "key": api_key}

# ===== 数据库依赖 =====
class Database:
    """模拟数据库"""
    def __init__(self):
        self.users = {
            1: {"id": 1, "name": "张三", "role": "admin"},
            2: {"id": 2, "name": "李四", "role": "user"},
        }

    def get_user(self, user_id: int):
        return self.users.get(user_id)

db = Database()

def get_current_user(user_id: int):
    """获取当前用户"""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.get("/users/{user_id}")
async def get_user(user: dict = Depends(get_current_user)):
    return user

# ===== 认证依赖 ======
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_active_user(token: str = Depends(oauth2_scheme)):
    """模拟认证"""
    if token != "valid-token":
        raise HTTPException(status_code=401, detail="未认证")
    return {"username": "current_user", "token": token}

@app.get("/me")
async def read_me(user: dict = Depends(get_current_active_user)):
    return user

# ===== 类作为依赖 =====
class PaginationParams:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def list_items(params: PaginationParams = Depends()):
    return {"skip": params.skip, "limit": params.limit}
```

> 💡 **依赖注入的好处**：
> 1. **代码复用**：认证、数据库连接等逻辑写一次，到处用
> 2. **易于测试**：可以 mock 依赖
> 3. **解耦合**：视图函数不关心具体实现，只关心"我需要什么"

### 22.3.5 异步数据库（SQLAlchemy async）

FastAPI 支持异步数据库操作，让高并发成为可能。

```bash
pip install sqlalchemy[asyncio] asyncpg aiosqlite
```

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, select
from typing import Optional

# 数据库 URL（异步驱动）
DATABASE_URL = "sqlite+aiosqlite:///./shop.db"  # 开发用 SQLite
# 生产用 PostgreSQL: "postgresql+asyncpg://user:pass@host/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# 定义模型
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer, default=0)

# 创建表
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 依赖：获取数据库会话
async def get_db():
    async with async_session() as session:
        yield session

# Pydantic 模型
class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int

    model_config = {"from_attributes": True}

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

# CRUD 操作（异步）
@app.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=list[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product).offset(skip).limit(limit)
    )
    products = result.scalars().all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")

    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    await db.commit()
    await db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")

    await db.delete(db_product)
    await db.commit()
    return {"message": "删除成功"}
```

### 22.3.6 WebSocket

**WebSocket** 是一种双向实时通信协议，和 HTTP 的"请求-响应"不同，WebSocket 可以让服务器主动给客户端发消息。

想象成**对讲机**vs**手机**：
- HTTP = 手机：你拨出去，对方才能回话
- WebSocket = 对讲机：连接上，双方随时可以说话

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json

app = FastAPI()

# 连接管理器
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """向所有连接广播消息"""
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    """聊天 WebSocket"""
    await manager.connect(websocket)
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()

            # 解析消息
            message = json.loads(data)
            username = message.get("username", "匿名")
            content = message.get("content", "")

            # 广播给所有人
            broadcast_msg = json.dumps({
                "type": "message",
                "username": username,
                "content": content
            })
            await manager.broadcast(broadcast_msg)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # 通知其他人用户离开
        await manager.broadcast(json.dumps({
            "type": "system",
            "content": f"用户离开了聊天室"
        }))

@app.websocket("/ws/echo")
async def echo_websocket(websocket: WebSocket):
    """回声 WebSocket（服务器原样返回）"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass

# 前端连接示例（JavaScript）
# const ws = new WebSocket("ws://127.0.0.1:8000/ws/echo");
# ws.onmessage = (event) => console.log(event.data);
# ws.send("Hello!");
```

### 22.3.7 OAuth2 + JWT 认证

**JWT（JSON Web Token）** 是一种安全的身份验证方式。想象它是**演唱会门票**——你买票时（登录）拿到一张票（JWT），之后入场（访问受保护资源）只需出示票，验票员（服务器）验真假就行，不用每次都查你的身份证（重新登录）。

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

app = FastAPI()

# ===== 配置 =====
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密码哈希工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ===== 数据模型 =====
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: bool = True

class UserInDB(User):
    hashed_password: str

# 模拟用户数据库
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "john@example.com",
        "hashed_password": pwd_context.hash("secret123"),
        "is_active": True
    }
}

# ===== 密码工具函数 =====
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# ===== JWT 工具函数 =====
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ===== 认证依赖 =====
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return current_user

# ===== 路由 =====
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """登录获取 Token"""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息（需要认证）"""
    return current_user

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    """需要认证的 API"""
    return [{"item": "1", "name": "商品1"}, {"item": "2", "name": "商品2"}]
```

运行效果：

```bash
# 登录获取 token
curl -X POST http://127.0.0.1:8000/token \
  -d "username=johndoe&password=secret123"
# 返回：
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIs...",
#   "token_type": "bearer"
# }

# 使用 token 访问受保护资源
curl http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
# 返回：
# {
#   "username": "johndoe",
#   "email": "john@example.com",
#   "is_active": true
# }
```

### 22.3.8 自动 OpenAPI 文档

FastAPI 最酷的功能之一——**自动生成 API 文档**！

- **Swagger UI**：`http://127.0.0.1:8000/docs`
- **ReDoc**：`http://127.0.0.1:8000/redoc`

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="我的 FastAPI 应用",
    description="这是一个展示 FastAPI 自动文档功能的示例",
    version="1.0.0",
    docs_url="/docs",       # Swagger 文档路径
    redoc_url="/redoc",     # ReDoc 文档路径
)

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    quantity: int = 0

@app.post("/items/",
    summary="创建商品",
    description="创建一个新的商品到库存中",
    response_description="创建的商品信息"
)
async def create_item(item: Item):
    return {"item": item, "status": "created"}
```

访问 `http://127.0.0.1:8000/docs`：

```
┌─────────────────────────────────────────────┐
│ FastAPI                                     │
│ Swagger UI                                  │
├─────────────────────────────────────────────┤
│ /items/                          POST  创建  │
│ /items/{item_id}                GET   读取  │
│ /items/{item_id}                PUT   更新  │
│ /items/{item_id}                DELETE 删除│
└─────────────────────────────────────────────┘
```

你可以直接在 Swagger UI 中：
1. **Try it out** → **Execute** → 实时测试 API
2. 查看请求/响应格式
3. 下载 OpenAPI 规范（JSON/YAML）

---

## 本章小结

本章我们详细探索了 Python 生态中三大主流 Web 框架：**Flask**、**Django** 和 **FastAPI**。以下是核心要点总结：

### 🎯 三大框架定位对比

| 维度 | Flask | Django | FastAPI |
|------|-------|--------|---------|
| **设计哲学** | 微框架，灵活可扩展 | 全功能，"电池包含" | 现代高性能，异步优先 |
| **学习曲线** | 平缓 | 较陡 | 平缓 |
| **适用场景** | 微服务、API、小型应用 | 大型全栈应用 | 高性能 API、微服务 |
| **数据库 ORM** | 需扩展（Flask-SQLAlchemy） | 内置强大 ORM | 需扩展（SQLAlchemy） |
| **Admin 后台** | 需扩展 | 内置神器 | 需自行开发 |
| **异步支持** | 可选（需扩展） | 有限（3.0+ 改进） | 原生异步，性能优异 |
| **API 文档** | 需扩展（flask-restful） | 可扩展（DRF） | 自动生成 Swagger/ReDoc |

### 📌 Flask 核心要点

1. **路由系统**：`@app.route()` 装饰器定义路由，支持路径参数（`<type:name>`）和 HTTP 方法（`methods=['GET', 'POST']`）
2. **请求/响应**：`request` 对象处理所有请求信息，`jsonify()` 返回 JSON 响应
3. **Jinja2 模板**：支持模板继承、变量插值、过滤器、循环判断
4. **会话与 Cookie**：`session` 基于加密 Cookie，蓝图 `Blueprint` 组织大型应用
5. **扩展生态**：Flask-SQLAlchemy（ORM）、Flask-Migrate（迁移）、Flask-Login（认证）
6. **生产部署**：Gunicorn（WSGI 服务器）+ Nginx（反向代理）

### 📌 Django 核心要点

1. **MTV 架构**：Model（模型层）- Template（模板层）- View（视图层）
2. **ORM 深度**：支持 ForeignKey、ManyToMany、OneToOne 关系；链式查询、`F` 表达式、`Q` 对象
3. **Admin 后台**：`admin.site.register()` 注册模型，自动生成 CRUD 后台管理
4. **表单系统**：`Form` 处理表单验证，`ModelForm` 与模型绑定
5. **中间件**：请求/响应流水线上可插拔的"质检员"
6. **用户认证**：内置 User 模型，`login_required`、`permission_required` 装饰器
7. **DRF**：强大的 RESTful API 框架，`ModelViewSet` 自动 CRUD
8. **信号机制**：`@receiver` 监听模型保存/删除等事件
9. **生产部署**：uWSGI + Nginx + Docker

### 📌 FastAPI 核心要点

1. **异步框架**：使用 `async def` + `await`，适合 I/O 密集型高并发场景
2. **类型安全**：Pydantic 模型自动验证请求数据，类型提示贯穿全程
3. **依赖注入**：`Depends()` 实现依赖复用、解耦、轻松测试
4. **路由**：路径参数、查询参数、Request Body 自动类型转换
5. **WebSocket**：`websocket_endpoint` 实现双向实时通信
6. **JWT 认证**：`OAuth2PasswordBearer` + `python-jose` 实现无状态认证
7. **自动文档**：访问 `/docs`（Swagger）或 `/redoc` 查看交互式 API 文档

### 🚀 选择建议

- **小型项目、简单 API** → Flask（轻量灵活）
- **大型全栈应用、内容管理系统** → Django（功能完善）
- **高性能微服务、实时应用** → FastAPI（异步高性能）
- **需要快速验证想法** → FastAPI（开发速度快）
- **需要完整后台管理** → Django（Admin 太香了）

> 🎭 **终极感悟**：框架只是工具，没有最好的框架，只有最适合的框架。理解核心概念后，框架之间的切换就像换一辆车——方向盘位置可能不同，但踩油门前进的道理是一样的！

---

*本章完* 📖
