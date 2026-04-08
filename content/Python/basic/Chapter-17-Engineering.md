+++
title = "第17章 工程化"
weight = 170
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 17 章 工程化：让代码从小打小闹升级为正规军

> 你是否有过这样的经历：写了一个 Python 脚本，运行得好好的，然后换了一台电脑，弹出 `ModuleNotFoundError`；或者代码写完了，过了一个月自己都看不懂了；或者改了一个小 bug，结果上线后发现引出了一堆新 bug。这些问题的根源在于——你缺了点工程化思维。

这一章，我们来聊聊 Python 项目从"野生代码"到"正规项目"的进化之路。项目结构怎么搭、依赖怎么管、测试怎么写、日志怎么配、配置怎么管、CI/CD 怎么搭、文档怎么维护——一条龙服务，包教包会。学完以后，你的代码就不是"个人作品"了，而是能拿得出手、招得来投资、经得起维护的正经项目了。

---

## 17.1 项目结构规范

你有没有见过这种项目结构？

```
我的项目/
├── 脚本1.py
├── 脚本2.py
├── 脚本3.py（最终版）.py
├── 脚本3.py（最终版）改.py
├── 新建文件夹/
│   ├── 111.py
│   └── 222.py
└── 乱七八糟的东西.txt
```

如果你的项目长这样，那这一节就是为你准备的。好的项目结构就像好的厨房——每样东西都有它该放的地方，找起来方便，收拾起来也轻松。

### 17.1.1 单文件脚本结构

**适用场景**：小型工具、一次性脚本、一次性数据分析、课程作业。

单个 `.py` 文件闯天下，简单粗暴有时候就是最优解。但即便是单文件，也有优雅的写法。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
My Cool Tool - 一个超厉害的工具
功能：blablabla
作者：xxx
日期：2026-04-08
"""

# ============ 导入区 ============
import sys
import os
import json
from pathlib import Path
from typing import Optional

# ============ 配置区 ============
# 这里放各种配置常量
DEFAULT_CONFIG = {
    "debug": False,
    "max_retries": 3,
    "timeout": 30,
}

# ============ 工具函数 ============
def validate_input(data: dict) -> bool:
    """验证输入数据是否合法"""
    return isinstance(data, dict) and "name" in data

def load_config(config_path: str) -> dict:
    """从文件加载配置"""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ============ 主逻辑 ============
class DataProcessor:
    """数据处理器"""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or DEFAULT_CONFIG
    
    def process(self, data: dict) -> dict:
        """处理数据"""
        if not validate_input(data):
            raise ValueError("无效的输入数据")
        return {"result": f"处理完成: {data['name']}"}

def main():
    """入口函数"""
    print("工具启动中...")
    processor = DataProcessor()
    result = processor.process({"name": "测试数据"})
    print(f"结果: {result}")

if __name__ == "__main__":
    main()
```

> **单文件脚本的最佳实践**：
> - 按`导入区 → 配置区 → 工具函数 → 主逻辑 → 入口`的顺序组织代码
> - 文件顶部写 docstring 说明脚本功能
> - 使用 `if __name__ == "__main__":` 保护入口
> - 类型注解写上，别嫌麻烦，三个月后你会感谢现在的自己

### 17.1.2 多模块包结构

**适用场景**：中型项目、功能较多、需要多人协作。

当你决定把代码分成多个文件时，你实际上是在创建一个**包（package）**。Python 中一个包含 `__init__.py` 文件的文件夹就是一个包。

假设我们做一个命令行翻译工具：

```
translator/
├── __init__.py          # 包初始化文件（可以很简洁）
├── main.py              # 入口文件
├── config.py            # 配置文件
├── translator/          # 核心功能子包
│   ├── __init__.py
│   ├── api.py           # 翻译 API 调用
│   ├── cache.py         # 缓存管理
│   └── parser.py        # 结果解析
└── utils/               # 工具函数子包
    ├── __init__.py
    ├── logger.py        # 日志工具
    └── file_helpers.py   # 文件处理
```

核心文件示例：

```python
# translator/__init__.py
"""Translator - 一个简洁的翻译工具包"""
__version__ = "1.0.0"

from .api import Translator
from .cache import CacheManager

__all__ = ["Translator", "CacheManager"]
```

```python
# translator/api.py
"""翻译 API 相关功能"""
from typing import Optional

class Translator:
    """翻译器类"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.request_count = 0
    
    def translate(self, text: str, target_lang: str = "en") -> str:
        """翻译文本"""
        self.request_count += 1
        # 这里是模拟，实际会调用翻译API
        return f"[{target_lang}] {text}"
    
    def batch_translate(self, texts: list, target_lang: str = "en") -> list:
        """批量翻译"""
        return [self.translate(t, target_lang) for t in texts]
```

```python
# main.py
"""命令行入口"""
from translator import Translator

def main():
    translator = Translator(api_key="your-api-key")
    result = translator.translate("你好世界", target_lang="en")
    print(result)  # 输出: [en] 你好世界

if __name__ == "__main__":
    main()
```

> **包结构的黄金法则**：
> - `__init__.py` 不要写太多东西，简单的导入导出即可
> - 每个模块只做一件事（单一职责原则）
> - 包内模块之间通过相对导入（如 `from . import api`）
> - 避免循环导入（circular import），那是让人头秃的经典问题

### 17.1.3 标准项目布局（src layout）

**适用场景**：需要发布到 PyPI 的正式开源项目、工业级项目。

这是目前 Python 社区推荐的标准布局，尤其适合需要打包发布的项目。核心思想是把**源代码**和**非代码文件**严格分开。

```
my_awesome_project/           # 项目根目录（也叫 repo root）
├── .github/                  # GitHub 相关配置
│   └── workflows/            # GitHub Actions 工作流
│       └── ci.yml
├── docs/                     # 文档
│   ├── index.md
│   └── getting-started.md
├── tests/                    # 测试文件（和 src 平级）
│   ├── __init__.py
│   ├── test_api.py
│   └── test_parser.py
├── src/                      # 源代码目录（重要！）
│   └── my_awesome_project/   # 项目包（和目录名一致）
│       ├── __init__.py
│       ├── api.py
│       ├── parser.py
│       └── utils.py
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml            # 现代项目配置（取代 setup.py）
└── uv.lock                   # 依赖锁定文件
```

> **为什么用 src 布局？**
> - 避免 import 时遇到本地包名和第三方包名冲突
> - 测试可以直接用 `pytest tests/`
> - 发布时只打包 `src/` 下的内容，不会把测试、文档一股脑发到 PyPI
> - 这是当前 PyPA（Python Packaging Authority）推荐的方式

来看一个完整的 `pyproject.toml`：

```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]      # 构建后端
build-backend = "hatchling.build"

[project]
name = "my-awesome-project"
version = "1.0.0"
description = "一个超厉害的项目"
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.10"
authors = [
    { name = "你的名字", email = "you@example.com" }
]
dependencies = [
    "requests>=2.28.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]
```

### 17.1.4 Flask / Django 项目布局

**适用场景**：Web 开发。

Web 框架有自己的项目布局约定，遵循这些约定可以让其他开发者一眼就找到他们想要的东西。

#### Flask 项目布局

Flask 是一个**微框架（micro-framework）**，它本身只提供核心功能，扩展需要自行添加。Flask 的项目布局比较灵活，但有一个比较公认的推荐结构：

```
flask_project/
├── app/                      # 应用主包
│   ├── __init__.py           # Flask 应用工厂
│   ├── routes/               # 路由（蓝图）
│   │   ├── __init__.py
│   │   ├── auth.py           # 认证相关路由
│   │   └── api.py            # API路由
│   ├── models/               # 数据库模型
│   │   ├── __init__.py
│   │   └── user.py
│   ├── templates/            # Jinja2 模板
│   │   ├── base.html
│   │   └── index.html
│   ├── static/               # 静态文件
│   │   ├── css/
│   │   └── js/
│   ├── extensions.py         # Flask 扩展初始化
│   └── config.py             # 配置
├── tests/                    # 测试
├── .env                      # 环境变量（不上传git）
├── requirements.txt
└── run.py                    # 应用入口
```

Flask 的应用工厂模式（Application Factory Pattern）是推荐写法：

```python
# app/__init__.py
"""Flask 应用工厂"""
from flask import Flask
from app.extensions import init_extensions

def create_app(config_name: str = "default") -> Flask:
    """创建并配置 Flask 应用"""
    app = Flask(__name__)
    
    # 加载配置
    from app.config import configs
    app.config.from_object(configs[config_name])
    
    # 初始化扩展
    init_extensions(app)
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app
```

```python
# run.py
"""应用入口"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

#### Django 项目布局

Django 是一个**全栈框架（full-stack framework）**，自带后台管理、ORM、认证系统等。Django 有一个标准的管理命令 `django-admin startproject`，会生成如下结构：

```
django_project/
├── manage.py                 # Django 管理脚本（必须）
├── django_project/           # 项目配置包（名字可改）
│   ├── __init__.py
│   ├── settings.py          # 所有配置
│   ├── urls.py              # 根 URL 配置
│   ├── wsgi.py              # WSGI 入口（部署用）
│   └── asgi.py              # ASGI 入口（异步用）
├── myapp/                    # 你的应用（用 manage.py startapp 创建）
│   ├── __init__.py
│   ├── admin.py             # 后台管理配置
│   ├── apps.py
│   ├── models.py            # 数据模型
│   ├── views.py             # 视图函数
│   ├── urls.py              # 应用内 URL 配置
│   ├── serializers.py       # DRF 序列化器（如果有 API）
│   └── tests.py             # 测试
└── templates/                # 全局模板目录
```

> **Flask vs Django 怎么选？**
> - Flask：轻量、灵活，你需要自己做很多选择。适合 API 项目、微服务、小到中型 Web 应用
> - Django：自带电池（batteries-included），适合需要快速开发完整功能的中大型项目
> - 打个比方：Flask 是乐高积木，Django 是高达模型。Flask 给你的都是散件，Django 给你的已经拼好了一大半

### 17.1.5 配置文件分离

**核心原则**：代码与配置分离，敏感信息不上传到代码仓库。

```python
# config.py - 基础配置
import os
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-me"
    DATABASE_URL = os.environ.get("DATABASE_URL") or f"sqlite:///{BASE_DIR}/app.db"
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    LOG_LEVEL = "WARNING"

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"  # 内存数据库，测试专用

# 配置字典，通过环境变量选择
configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
```

```python
# .env - 环境变量文件（不上传git！）
SECRET_KEY=your-super-secret-production-key
DATABASE_URL=postgresql://user:pass@localhost/mydb
DEBUG=False
LOG_LEVEL=INFO
API_KEY=your-api-key-here
```

```python
# .gitignore - 忽略这些文件
.env
__pycache__/
*.pyc
*.db
*.log
.venv/
venv/
env/
.pytest_cache/
.coverage
dist/
build/
*.egg-info/
```

> **配置分离的三个层次**：
> 1. **代码层面的默认配置**（`config.py`）
> 2. **环境变量**（`.env` 或系统环境变量）
> 3. **配置优先级**：环境变量 > `.env` 文件 > 代码默认值

---

## 17.2 依赖管理

> 有一句话怎么说来着？"在我电脑上是能跑的"——这句话不知道引发了程序员之间多少血案。依赖管理的本质就是：**保证所有人的"依赖世界"一致**。

### 17.2.1 requirements.txt 详解

`requirements.txt` 是 Python 项目最常见的依赖管理文件。它的格式非常简单，就是每行一个包，格式为 `包名==版本号`（或 `包名>=版本号` 等）。

```txt
# requirements.txt
flask==3.0.0
requests==2.31.0
click==8.1.7
python-dotenv==1.0.0
pydantic==2.5.0
```

```bash
# 安装 requirements.txt 中的所有依赖
pip install -r requirements.txt

# 导出当前环境的所有依赖
pip freeze > requirements.txt

# 导出时排除某些包
pip freeze | grep -v "pkg-resources" > requirements.txt
```

> **但 `pip freeze` 有个坑**：它会把所有包的版本都锁死，包括传递依赖。这在某些情况下是好的（保证一致性），但在开发时可能过于严格。

```txt
# 更灵活的开发用 requirements
# 使用 >= 而不是 ==，允许小幅升级
flask>=3.0.0
requests>=2.31.0

# 分环境依赖
-r requirements-dev.txt   # 引用另一个文件
```

### 17.2.2 pip-tools（pip-compile）

`pip-tools` 解决的是这样一个问题：开发时想用灵活版本（`flask>=3.0`），但部署时需要锁定具体版本（`flask==3.0.3`）。

`pip-tools` 有两个核心命令：

- `pip-compile`：从你的"源依赖"文件生成"锁定版本"文件
- `pip-sync`：根据锁定文件安装/卸载包，保持环境同步

```bash
# 安装 pip-tools
pip install pip-tools
```

```txt
# requirements.in - 你的源依赖文件（开发时维护这个）
# 使用灵活的版本说明
flask>=3.0.0
requests>=2.31.0
pytest>=7.0.0
black>=23.0.0
```

```bash
# 运行 pip-compile 生成锁定的依赖
pip-compile requirements.in

# 这会生成 requirements.txt，自动解析所有传递依赖并锁定版本
```

生成的 `requirements.txt` 看起来像这样：

```txt
# requirements.txt - 自动生成，请勿手动编辑
#
#   pip-compile requirements.in
#
attrs==23.2.0
    # via jsonschema
black==24.1.1
    # via -r requirements.in (line 2)
click==8.1.7
    # via flask
flask==3.0.3
    # via -r requirements.in (line 1)
itsdangerous==2.1.2
    # via flask
jinja2==3.1.3
    # via flask
markupsafe==2.1.5
    # via jinja2
pytest==8.0.0
    # via -r requirements.in (line 3)
requests==2.31.0
    # via -r requirements.in (line 2)
```

```bash
# 安装锁定的依赖
pip-sync requirements.txt

# pip-sync 会自动卸载不在 requirements.txt 中的包
# 并安装所有在 requirements.txt 中的包
```

### 17.2.3 Poetry（现代依赖管理 + 打包）

**Poetry** 是一个现代化的 Python 依赖管理和打包工具。它用 `pyproject.toml` 作为配置文件，但做了更丰富的扩展。

```bash
# 安装 Poetry
pip install poetry

# 初始化项目
poetry new my-awesome-project

# 或在现有项目中初始化
poetry init
```

`poetry.lock` 是 Poetry 的锁定文件，功能类似 `pip-tools` 生成的锁定文件，但内置于 Poetry 中。

```toml
# pyproject.toml - Poetry 配置示例
[tool.poetry]
name = "my-awesome-project"
version = "1.0.0"
description = "一个使用 Poetry 管理的项目"
authors = ["你的名字 <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
flask = "^3.0"
requests = "^2.31"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"
black = "^23.0"
mypy = "^1.0"

[tool.poetry.scripts]
my-script = "my_awesome_project.main:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

```bash
# 核心命令
poetry install          # 安装依赖（自动创建虚拟环境）
poetry add requests     # 添加依赖
poetry add --dev pytest # 添加开发依赖
poetry remove requests  # 移除依赖
poetry update          # 更新锁定文件
poetry lock            # 只更新锁定文件（不安装）
poetry run python xxx.py  # 在虚拟环境中运行命令
poetry shell           # 进入虚拟环境的 shell

# 打包发布
poetry build            # 构建包
poetry publish          # 发布到 PyPI
```

```python
# 使用 Poetry 管理的项目结构示例
from my_awesome_project import __version__

def main():
    print(f"项目版本: {__version__}")  # 输出: 项目版本: 1.0.0

if __name__ == "__main__":
    main()
```

> **Poetry 的优势**：
> - 一个工具搞定依赖管理 + 打包 + 发布
> - 内置虚拟环境管理，不需要再装 `virtualenv`
> - `pyproject.toml` 是 PEP 517/518 标准
> - 自动处理传递依赖，生成 `poetry.lock`
> - 语义化版本控制（`^`, `~`, `>=` 等）

### 17.2.4 PDM（PEP 582 支持）

**PDM**（Python Development Master）是一个支持 **PEP 582** 的包管理器。PEP 582 是 Python 官方提出的一种"本地 `__pypackages__` 目录"方案，类似于 Node.js 的 `node_modules`，不需要虚拟环境。

```bash
# 安装 PDM
pip install pdm

# 初始化项目
pdm init

# 基本命令
pdm add requests         # 添加依赖
pdm add -dG dev pytest   # 添加开发组依赖
pdm install              # 安装依赖
pdm run pytest           # 运行测试
pdm build                # 构建包
```

```toml
# pyproject.toml - PDM 配置
[project]
name = "my-project"
version = "1.0.0"
requires-python = ">=3.10"
dependencies = ["requests>=2.31"]

[tool.pdm.dev-dependencies]
dev = ["pytest>=7.0", "black>=23.0"]
test = ["pytest-cov>=4.0"]
```

```bash
# PDM 的 PEP 582 项目结构（不需要 .venv）
my-project/
├── __pypackages__/      # PEP 582 包目录（类 node_modules）
│   └── 3.10/
│       ├── lib/
│       └── include/
├── src/
│   └── my_project/
├── pyproject.toml
└── pdm.lock
```

> **PDM vs Poetry**：
> - PDM 支持 PEP 582（实验性），Poetry 不支持
> - PDM 对 PEP 621 原生支持
> - 两者功能相似，选择哪个更多是个人偏好
> - PDM 在国内的使用率正在上升

### 17.2.5 uv（极速新一代包管理）

**uv** 是由 Astral 公司（Rust / Ruff 的作者）开发的极速 Python 包管理器。它用 Rust 编写，速度比 pip 快 10-100 倍。如果你用过 `pnpm`（Node.js）或 `cargo`（Rust），uv 就是 Python 世界里的那个极速选手。

```bash
# 安装 uv（单个脚本搞定）
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# 核心命令 - 速度感人
uv pip install requests              # 安装包
uv pip install -r requirements.txt   # 从文件安装
uv pip compile requirements.in -o requirements.txt  # 编译依赖（类似 pip-tools）
uv sync                              # 同步依赖
uv add requests                      # 添加依赖
uv add --dev pytest                  # 添加开发依赖
uv run python script.py              # 运行脚本（自动在临时环境）
uv run pytest                        # 运行测试

# 项目管理
uv init my-project                   # 初始化新项目
uv add httpx                         # 添加依赖（自动创建 pyproject.toml）
```

```bash
# uv 的速度有多快？做个对比
time pip install flask requests sqlalchemy  # pip: 慢...
time uv pip install flask requests sqlalchemy # uv: 毫秒级
```

> **uv 的核心优势**：
> - **极快**：用 Rust 编写，10-100 倍于 pip 的速度
> - **统一工具链**：可替代 pip、pip-tools、poetry、virtualenv、tox 等
> - **内置项目支持**：从初始化到发布一条龙
> - **锁定文件**：`uv.lock`，语义化锁定
> - **跨平台**：Linux、macOS、Windows 全支持
> - **Python 版本管理**：可以自动下载和管理不同版本的 Python

```bash
# uv 的推荐工作流
uv init my-awesome-project   # 创建项目
cd my-awesome-project
uv add flask requests         # 添加依赖
uv add --dev pytest pytest-cov black mypy  # 添加开发依赖
uv run pytest                # 运行测试
uv build                     # 构建发布包
```

uv 在 2024-2025 年迅速走红，很多新项目都推荐使用 uv 作为包管理工具。如果你追求速度，uv 绝对是首选。

### 依赖管理工具对比

```
┌─────────────┬────────────┬────────┬──────────┬──────────────┬─────────────┐
│   工具      │   速度     │ PEP 582│  锁定文件 │   打包发布   │   学习曲线  │
├─────────────┼────────────┼────────┼──────────┼──────────────┼─────────────┤
│ pip + reqs  │    慢      │   ❌   │   手动    │     ❌       │     低      │
│ pip-tools   │    慢      │   ❌   │   ✅     │     ❌       │     低      │
│ Poetry      │    中      │   ❌   │   ✅     │     ✅       │     中      │
│ PDM         │    中      │   ✅   │   ✅     │     ✅       │     中      │
│ uv          │   极快     │   ✅   │   ✅     │     ✅       │     低      │
└─────────────┴────────────┴────────┴──────────┴──────────────┴─────────────┘
```

---

## 17.3 测试

> 写代码的时候信心满满，上线之后心凉凉——这是没有测试的程序的宿命。测试是你代码的"保险单"，让你改代码的时候不用担心把原来好好的功能搞坏了。

### 17.3.1 unittest（标准库单元测试）

`unittest` 是 Python 标准库自带的测试框架，源自 Java 的 JUnit（unit test → unittest，命名逻辑很直白）。

```python
# test_calculator.py
import unittest
from calculator import Calculator, divide_by_zero_error

class TestCalculator(unittest.TestCase):
    """计算器类的单元测试"""
    
    def setUp(self):
        """每个测试方法前都会调用"""
        self.calc = Calculator()
    
    def test_add(self):
        """测试加法"""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
    
    def test_divide(self):
        """测试除法"""
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5)
        self.assertAlmostEqual(self.calc.divide(10, 3), 3.333333, places=5)
    
    def test_divide_by_zero(self):
        """测试除以零的情况"""
        with self.assertRaises(divide_by_zero_error):
            self.calc.divide(10, 0)
    
    def tearDown(self):
        """每个测试方法后都会调用（清理资源）"""
        pass
```

```bash
# 运行测试
python -m unittest test_calculator.py
python -m unittest discover                    # 自动发现所有测试
python -m unittest test_module.TestClass.test  # 运行特定测试
```

```bash
# 运行结果
# ....F.....
# ======================================================================
# FAIL: test_add (test_calculator.TestCalculator.test_add)
# ----------------------------------------------------------------------
# Traceback (most recent call last):
#   File "test_calculator.py", line 15, in test_add
#     self.assertEqual(result, 5)
# AssertionError: 6 != 5
```

> **unittest 的核心概念**：
> - `TestCase`：测试用例类，继承它来写测试
> - `setUp()`：每个测试前执行，用于初始化
> - `tearDown()`：每个测试后执行，用于清理
> - `assertEqual(a, b)`：断言 a == b
> - `assertTrue(x)`：断言 x 为 True
> - `assertRaises(Exception)`：断言抛出指定异常
> - `assertAlmostEqual(a, b, places=7)`：断言浮点数近似相等

### 17.3.2 pytest（最流行的测试框架）

**pytest** 是目前 Python 生态最流行的测试框架。它兼容 `unittest`，但写法更简洁、功能更强大。没有理由不选 pytest。

```bash
# 安装
pip install pytest

# 或者用 uv
uv add --dev pytest
```

pytest 的核心哲学是：**你不需要继承什么类，直接写函数就行**。

```python
# test_calculator.py - pytest 版本
from calculator import Calculator, divide_by_zero_error

def test_add():
    """测试加法 - 函数名以 test_ 开头即可"""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0

def test_divide():
    """测试除法"""
    calc = Calculator()
    assert calc.divide(10, 2) == 5
    assert calc.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

def test_divide_by_zero():
    """测试除以零抛出异常"""
    calc = Calculator()
    with pytest.raises(divide_by_zero_error):
        calc.divide(10, 0)

def test_add_with_negative():
    calc = Calculator()
    assert calc.add(-5, -3) == -8
    assert calc.add(100, -50) == 50
```

```bash
# 运行 pytest
pytest                        # 当前目录所有测试
pytest test_file.py          # 指定文件
pytest tests/                # 指定目录
pytest -v                    # 详细输出（verbose，每个测试单独一行）
pytest --tb=short            # 简短的错误回溯
pytest -x                    # 遇到第一个失败就停止
pytest -k "add"              # 只运行名字包含 "add" 的测试
pytest --collect-only        # 只收集测试，不运行（看看有哪些测试）
```

```bash
# 输出示例
# ========================= test session starts =========================
# collected 4 items
#
# test_calculator.py::test_add PASSED                                  [ 25%]
# test_calculator.py::test_divide PASSED                              [ 50%]
# test_calculator.py::test_divide_by_zero PASSED                      [ 75%]
# test_calculator.py::test_add_with_negative PASSED                    [100%]
#
# ========================= 4 passed in 0.12s ===========================
```

### 17.3.3 pytest 高级用法（fixtures / parametrize / markers）

pytest 有三大法宝：fixtures（夹具）、parametrize（参数化）、markers（标记）。

#### Fixtures（夹具）

Fixtures 用来**提供测试数据、创建测试资源、自动清理**。比 `setUp/tearDown` 更灵活、更强大。

```python
import pytest
from app import create_app
from database import reset_db, seed_data

@pytest.fixture
def app():
    """创建测试用的 Flask 应用"""
    app = create_app("testing")
    yield app  # yield 相当于 setUp + tearDown

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def auth_headers():
    """认证头"""
    return {"Authorization": "Bearer test-token-123"}

@pytest.fixture
def sample_user():
    """创建测试用户数据"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
    }

def test_login(client, sample_user):
    """测试登录"""
    response = client.post("/api/login", json=sample_user)
    assert response.status_code == 200
    assert "token" in response.json

def test_get_profile(client, auth_headers):
    """测试获取个人资料"""
    response = client.get("/api/profile", headers=auth_headers)
    assert response.status_code == 200
```

```python
# 更高级的 fixture - 带参数和依赖
@pytest.fixture(scope="module")  # session/module/function，默认 function
def db_connection():
    """数据库连接 fixture"""
    conn = create_db_connection()
    yield conn
    conn.close()

@pytest.fixture
def clean_db(db_connection):
    """带依赖的 fixture"""
    db_connection.execute("DELETE FROM users")
    yield
    db_connection.execute("DELETE FROM users")
```

> **scope 参数说明**：
> - `function`：每个测试函数调用一次（默认，最常用）
> - `class`：每个测试类调用一次
> - `module`：每个模块（文件）调用一次
> - `session`：整个测试会话调用一次（所有文件共享）

#### parametrize（参数化）

参数化让你用**一套测试代码 + 多组测试数据**，避免写一堆重复的测试函数。

```python
import pytest

@pytest.mark.parametrize("input_data,expected", [
    ([2, 3], 5),
    ([0, 0], 0),
    ([-1, 1], 0),
    ([100, -50], 50),
    ([0.1, 0.2], pytest.approx(0.3)),
])
def test_add_parametrized(input_data, expected):
    """参数化测试加法"""
    calc = Calculator()
    a, b = input_data
    assert calc.add(a, b) == expected

@pytest.mark.parametrize("username,password,expected_status", [
    ("user1", "pass1", 200),
    ("user1", "wrongpass", 401),
    ("", "pass", 400),
    ("user1", "", 400),
])
def test_login_cases(client, username, password, expected_status):
    """参数化测试登录的各种情况"""
    response = client.post("/api/login", json={
        "username": username,
        "password": password,
    })
    assert response.status_code == expected_status
```

运行结果：

```bash
$ pytest -v test_parametrize.py

# test_parametrize.py::test_add_parametrized[2,3-5] PASSED         [ 20%]
# test_parametrize.py::test_add_parametrized[0,0-0] PASSED          [ 40%]
# test_parametrize.py::test_add_parametrized[-1,1-0] PASSED         [ 60%]
# test_parametrize.py::test_add_parametrized[100,-50-50] PASSED    [ 80%]
# test_parametrize.py::test_add_parametrized[0.1,0.2-0.3] PASSED   [100%]
```

#### Markers（标记）

Markers 用来给测试打标签，可以实现**选择性运行**。

```python
import pytest

@pytest.mark.slow          # 标记为慢测试
def test_full_integration():
    """完整的集成测试，很慢"""
    # 模拟运行 30 秒的测试
    pass

@pytest.mark.integration    # 标记为集成测试
def test_api_integration():
    """API 集成测试"""
    pass

@pytest.mark.unit           # 单元测试
def test_unit():
    """单元测试"""
    pass

@pytest.mark.skip(reason="这个功能还没实现")
def test_future_feature():
    """跳过的测试"""
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="需要 Python 3.10+")
def test_new_feature():
    """条件跳过"""
    pass

@pytest.mark.xfail(reason="已知问题，等待修复")
def test_known_issue():
    """预期失败的测试"""
    assert False
```

```bash
# 只运行带有特定标记的测试
pytest -m "slow"
pytest -m "not slow"           # 排除慢测试
pytest -m "unit and not slow"  # 组合条件

# 标记注册（在 pytest.ini 或 pyproject.toml 中）
```

```toml
# pyproject.toml 中配置 pytest markers
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

### 17.3.4 pytest-cov（覆盖率报告）

**pytest-cov** 是 pytest 的覆盖率插件，能生成详细的代码覆盖率报告，告诉你哪些代码被执行了、哪些没有。

```bash
# 安装
pip install pytest-cov

# 运行并生成覆盖率报告
pytest --cov=my_app              # 覆盖率针对 my_app 包
pytest --cov=my_app tests/       # 指定测试目录
pytest --cov=.                    # 当前目录所有包
pytest --cov=my_app --cov-report=html  # 生成 HTML 报告
```

```bash
# 输出示例
# ---------- coverage: platform darwin, Python 3.10.12 ----------
# Name                    Stmts   Miss  Cover   Missing
# -----------------------------------------------------------
# my_app/__init__             5      0   100%
# my_app/api                 45      3    93%   67,89
# my_app/models              60     12    80%   45-52,78
# my_app/utils               30      0   100%
# -----------------------------------------------------------
# TOTAL                     140     15    89%
```

```bash
# 更多用法
pytest --cov=my_app --cov-report=term-missing  # 终端显示未覆盖行号
pytest --cov=my_app --cov-report=html --cov-report=term  # 多格式报告
pytest --cov=my_app -p no:cov  # 禁用覆盖率（某些 CI 配置）

# 最低覆盖率门禁
pytest --cov=my_app --cov-fail-under=80  # 低于 80% 则测试失败
```

> **覆盖率不是万能的**：
> - 100% 覆盖率不等于 100% 没有 bug
> - 它只能告诉你"哪些代码被执行了"，不能告诉你"执行得对不对"
> - 覆盖率是**最低标准**，不是**最高目标**
> - 一般项目 80%-90% 覆盖率是合理的

### 17.3.5 Mock（unittest.mock）

**Mock** 用来**模拟（mock）**那些你不想真正调用的东西——比如外部 API、数据库、文件系统等。测试应该测试你的代码，而不是依赖外部系统。

```python
from unittest.mock import Mock, patch, MagicMock
import pytest

def test_mock_basic():
    """最基本的 Mock 用法"""
    mock_obj = Mock()
    mock_obj.some_method.return_value = "mocked!"
    
    result = mock_obj.some_method(42, name="test")
    
    # 验证方法被调用了
    mock_obj.some_method.assert_called_once_with(42, name="test")
    assert result == "mocked!"

def test_mock_external_api():
    """模拟外部 API 调用"""
    with patch("requests.get") as mock_get:
        # 设置模拟返回值
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"user": "张三", "age": 25}
        mock_get.return_value = mock_response
        
        # 测试使用 requests 的函数
        from user_service import get_user_info
        result = get_user_info("user123")
        
        assert result["user"] == "张三"
        mock_get.assert_called_once_with("https://api.example.com/user/user123")

def test_mock_class():
    """Mock 整个类"""
    mock_db = MagicMock(spec=Database)  # spec 限制只能调用真实存在的方法
    mock_db.query.return_value = [{"id": 1, "name": "测试"}]
    
    service = UserService(mock_db)
    users = service.list_users()
    
    assert len(users) == 1
    assert users[0]["name"] == "测试"

def test_patch_decorator():
    """用装饰器 patch"""
    @patch("datetime.datetime.now")
    def test_with_mocked_time(mock_now):
        mock_now.return_value = Mock(hour=10)
        
        result = get_greeting()  # 根据时间返回问候语
        assert result == "早上好！"
```

```python
# 模拟文件操作
from unittest.mock import mock_open, patch

def test_read_config():
    """模拟读取配置文件"""
    fake_config = """
DATABASE_URL=postgresql://localhost/testdb
SECRET_KEY=abc123
DEBUG=true
"""
    with patch("builtins.open", mock_open(read_data=fake_config)):
        from config import load_config
        config = load_config("config.ini")
        
        assert config["DATABASE_URL"] == "postgresql://localhost/testdb"
        assert config["DEBUG"] == "true"
```

> **Mock vs Fake vs Stub**：
> - **Mock**：验证调用行为（调用了没？参数对不对？调用了几次？）
> - **Stub**：提供预设响应（返回一个固定值）
> - **Fake**：有实际实现的简化版本（内存数据库代替真实数据库）
> - 简单理解：Mock 是会"说话"的 Stub，Fake 是"简单版"的真实对象

### 17.3.6 TDD 开发流程

**TDD**（Test-Driven Development，测试驱动开发）是一种开发方法论，核心理念是：**先写测试，再写实现**。三个步骤：红（Red）→ 绿（Green）→ 重构（Refactor）。

```
┌─────────────────────────────────────────────────────────┐
│                    TDD 循环                             │
│                                                         │
│   1. 写一个会失败的测试  ──→  RED（红灯）              │
│          ↓                                            │
│   2. 写最简代码让它通过  ──→  GREEN（绿灯）            │
│          ↓                                            │
│   3. 重构代码              ──→  REFACTOR               │
│          ↓                                            │
│   4. 下一个测试                                          │
└─────────────────────────────────────────────────────────┘
```

```python
# TDD 示例：实现一个栈（Stack）数据结构

# ========== 步骤 1：先写测试（RED）==========
# test_stack.py

def test_stack_is_empty():
    """新创建的栈应该是空的"""
    stack = Stack()
    assert stack.is_empty() is True

def test_stack_push():
    """push 后栈不为空"""
    stack = Stack()
    stack.push(1)
    assert stack.is_empty() is False

def test_stack_pop():
    """pop 应该返回最后 push 的元素"""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2

def test_stack_pop_order():
    """栈是 LIFO（后进先出）"""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1

def test_pop_empty_stack():
    """空栈 pop 应该抛出异常"""
    stack = Stack()
    with pytest.raises(StackUnderflowError):
        stack.pop()
```

```bash
# 运行测试 - 当然是失败的，因为 Stack 还没实现
$ pytest test_stack.py -v
# E   NameError: name 'Stack' is not defined
```

```python
# ========== 步骤 2：写最简实现让测试通过（GREEN）==========

class StackUnderflowError(Exception):
    """栈下溢异常"""
    pass

class Stack:
    """栈数据结构 - LIFO"""
    
    def __init__(self):
        self._items = []
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise StackUnderflowError("Cannot pop from empty stack")
        return self._items.pop()
```

```bash
# 再运行测试 - 全部通过
$ pytest test_stack.py -v
# ===== 5 passed in 0.03s =====
```

```bash
# ========== 步骤 3：重构 - 让代码更优雅 ==========
# 现在的实现已经很简单了，但如果我们想优化...
# 可以考虑用列表替代 `_items`，或者添加更多功能
# 运行测试确保重构没有破坏功能
$ pytest test_stack.py -v
# ===== 5 passed in 0.03s =====
```

> **TDD 的好处**：
> - 测试覆盖率天然就高
> - 代码设计由测试驱动，更容易解耦
> - 每次改动都能立即知道是否破坏了已有功能
> - 减少调试时间
>
> **TDD 的挑战**：
> - 初期速度慢，需要适应这种"先写测试"的思维方式
> - 不是所有项目都适合 TDD（探索性原型就不适合）
> - 测试本身也需要维护

---

## 17.4 日志

> `print()` 是程序员最原始的调试方式，但用它来记录生产环境的运行状态，就像用喷灯来点蚊香——不是不行，但显得很不专业。`logging` 模块是你 Python 生涯中迟早要掌握的工具。

### 17.4.1 logging 模块详解

`logging` 是 Python 标准库的日志模块，设计得很完善：**级别分明、输出可控、格式可定**。

```
DEBUG    <-- 最详细，调试时用
INFO     <-- 一般信息，确认正常工作
WARNING  <-- 警告，可能有问题但不影响运行
ERROR    <-- 错误，功能受到影响
CRITICAL <-- 严重错误，系统可能无法继续运行
```

```python
import logging

# 创建 logger
logger = logging.getLogger(__name__)

# 设置级别（只会记录 >= 此级别的日志）
logger.setLevel(logging.DEBUG)

# 使用
logger.debug("这是一条调试信息")
logger.info("这是一般信息")
logger.warning("这是一条警告")
logger.error("这是一条错误信息")
logger.critical("这是严重错误信息")
```

```bash
# 输出
# WARNING:__name__:这是一条警告
# ERROR:__name__:这是一条错误信息
# CRITICAL:__name__:这是严重错误信息
```

### 17.4.2 Logger / Handler / Formatter / Filter

`logging` 的四大天王：**Logger（日志器）**、**Handler（处理器）**、**Formatter（格式器）**、**Filter（过滤器）**。

```
Logger（日志器）
    │
    ├── Filter（过滤器，可选）← 决定这条日志要不要记录
    │
    └── Handler（处理器）× N ← 决定日志输出到哪里
            │
            └── Formatter（格式器）← 决定日志长什么样
```

```python
import logging

# 1. 创建 logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

# 2. 创建 Formatter（决定日志格式）
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)
console_formatter = logging.Formatter(
    "%(levelname)s - %(message)s"
)

# 3. 创建 Handler（决定输出到哪里）
# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)      # 控制台只显示 INFO 及以上
console_handler.setFormatter(console_formatter)

# 文件处理器
file_handler = logging.FileHandler(
    "app.log",
    encoding="utf-8",
    mode="a"                                  # append 模式
)
file_handler.setLevel(logging.DEBUG)          # 文件记录 DEBUG 及以上
file_handler.setFormatter(file_formatter)

# 4. 把 Handler 加到 Logger 上
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 5. 使用
logger.debug("这条只在文件里")
logger.info("这条文件和控制台都有")
logger.warning("这条文件和控制台都有（警告）")
```

> **层级关系**：
> - Logger 设置了 `level`，Handler 也可以各自设置 `level`
> - Handler 的 `level` 是最后一道关卡
> - Logger 负责"生成"日志，Handler 负责"分发"日志
> - 一个 Logger 可以加多个 Handler（同时输出到控制台和文件）

### 17.4.3 logging.basicConfig() 快速配置

如果你只是想要一个快速配置，`basicConfig()` 是最简单的方式——一行代码搞定。

```python
import logging

# 最简单的配置（输出到控制台，级别为 WARNING 及以上）
logging.basicConfig(level=logging.WARNING)

logging.debug("调试信息")  # 不显示
logging.info("一般信息")   # 不显示
logging.warning("警告信息")  # 显示
```

```python
# 稍微完整一点的配置
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),            # 控制台
        logging.FileHandler("app.log", encoding="utf-8"),  # 文件
    ],
)

logger = logging.getLogger(__name__)
logger.info("应用启动")
```

> **basicConfig 的坑**：
> - 只能调用一次，多次调用只有第一次生效
> - 默认是 `root logger`，所以 `logging.info()` 这种无前缀的方式也能用
> - 生产环境建议还是用完整配置，更可控

### 17.4.4 loguru（更简单的日志方案）

**loguru** 是一个第三方日志库，设计理念是"让日志记录变得极其简单"。它不需要 Handler、Formatter 那些概念，开箱即用。

```bash
pip install loguru
```

```python
from loguru import logger

# 开箱即用，不需要任何配置！
logger.info("你好，日志！")
logger.success("成功了！")
logger.warning("警告！")
logger.error("出错了！")
logger.debug("调试信息")
```

```bash
# 输出
# 2026-04-08 10:20:01 | INFO    | root: 你好，日志！
# 2026-04-08 10:20:01 | SUCCESS | root: 成功了！
# 2026-04-08 10:20:01 | WARNING | root: 警告！
# 2026-04-08 10:20:01 | ERROR   | root: 出错了！
# 2026-04-08 10:20:01 | DEBUG   | root: 调试信息
```

```python
# 移除默认处理器，添加自定义文件输出
from loguru import logger
import sys

# 移除默认的 stderr 处理器
logger.remove()

# 添加自定义文件处理器
logger.add(
    "app_{time}.log",                       # 文件名（带时间）
    rotation="500 MB",                      # 文件超过 500MB 则轮转
    retention="10 days",                    # 保留 10 天
    compression="zip",                      # 压缩旧日志
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
)

# 添加控制台输出
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>",
)

# 使用
logger.info("请求来了: {}", request_id)  # {} 格式化，性能更好
logger.info("用户 {user} 登录了", user="张三")
```

```python
# 异常捕获 - loguru 的杀手级功能
from loguru import logger

def dangerous_function():
    return 1 / 0

# 方法1：装饰器
@logger.catch
def main():
    dangerous_function()

# 方法2：上下文管理器
with logger.catch():
    dangerous_function()

# 方法3：手动记录
try:
    dangerous_function()
except ZeroDivisionError:
    logger.exception("出错了，但没关系我们记录了上下文")
```

```python
# 完整示例
from loguru import logger
import sys

# 配置
logger.remove()  # 移除默认处理器

# 控制台：只显示 WARNING 及以上，彩色输出
logger.add(
    sys.stderr,
    level="WARNING",
    format="<red>{time:HH:mm:ss}</red> | <level>{level}</level> | {message}",
)

# 文件：记录所有级别
logger.add(
    "app.log",
    level="DEBUG",
    rotation="00:00",        # 每天午夜轮转
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level:8} | {name}:{line} - {message}",
)

logger.info("应用启动")
logger.warning("这是一个警告")
logger.error("这是一个错误")
```

> **loguru vs 标准 logging**：
> - loguru：更简单、更漂亮，适合中小型项目
> - 标准 logging：更灵活、更可控，适合需要精细配置的大型项目
> - 如果项目简单，直接 loguru；如果项目复杂，还是老老实实用 logging

---

## 17.5 配置管理

> 程序最怕什么？最怕硬编码！`config.py` 里写满了 `password = "123456"`，然后不小心上传到 GitHub——这种事每年都在发生。配置管理的核心就是：**代码和配置分离，环境之间隔离**。

### 17.5.1 环境变量（os.environ）

环境变量是配置管理最基础的方式，操作系统级别、容器化部署、无服务器函数都靠它。

```python
import os

# 读取环境变量
db_url = os.environ.get("DATABASE_URL")
api_key = os.environ.get("API_KEY", "default-key")  # 提供默认值

# 设置环境变量（仅当前进程）
os.environ["DEBUG"] = "true"

# 读取并转换类型
timeout = int(os.environ.get("TIMEOUT", "30"))  # 默认 30 秒
debug = os.environ.get("DEBUG", "false").lower() == "true"
```

```python
# 类型安全的配置读取
from typing import Optional

class Config:
    """从环境变量读取配置"""
    
    @property
    def database_url(self) -> str:
        return os.environ["DATABASE_URL"]
    
    @property
    def debug(self) -> bool:
        return os.environ.get("DEBUG", "false").lower() in ("true", "1", "yes")
    
    @property
    def max_connections(self) -> int:
        value = os.environ.get("MAX_CONNECTIONS", "10")
        return int(value)
    
    @property
    def secret_key(self) -> Optional[str]:
        return os.environ.get("SECRET_KEY")
    
    def validate(self):
        """验证必需的配置"""
        required = ["DATABASE_URL", "SECRET_KEY"]
        missing = [k for k in required if k not in os.environ]
        if missing:
            raise ValueError(f"缺少必需的环境变量: {', '.join(missing)}")

config = Config()
config.validate()
```

### 17.5.2 .env 文件（python-dotenv）

`.env` 文件让你在开发时把环境变量写在文件里，而不是每次开终端都手动设置。`python-dotenv` 帮你读取这个文件。

```bash
pip install python-dotenv
```

```bash
# .env 文件（不要上传到 Git！）
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/mydb
DEBUG=true
LOG_LEVEL=DEBUG
API_KEY=your-api-key
REDIS_URL=redis://localhost:6379
MAX_WORKERS=4
```

```python
# settings.py - 配置管理
import os
from pathlib import Path
from dotenv import load_dotenv

# 找到 .env 文件（在项目根目录）
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / ".env"

# 加载 .env 文件
load_dotenv(env_path)
# 也可以不传路径，默认在当前目录和父目录找
# load_dotenv()  # 简单写法

# 读取配置（现在 os.environ 里就有 .env 中的值了）
SECRET_KEY = os.environ["SECRET_KEY"]
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///app.db")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
```

```python
# 自动加载 .env 到 shell 环境（用于本地开发）
# 在项目根目录运行：
# dotenv run python your_script.py

# 或者用命令行
# dotenv set DEBUG true
# dotenv list
```

> **.gitignore 要忽略 .env**：
> ```
> .env
> .env.local
> .env.*.local
> ```
> `.env` 文件里通常包含密钥、密码等敏感信息，绝对不能提交到代码仓库！

### 17.5.3 pydantic-settings（类型安全配置）

**pydantic-settings** 是 pydantic 团队出的配置管理库，完美结合了 pydantic 的类型验证和环境变量加载功能。

```bash
pip install pydantic-settings
```

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """应用配置 - pydantic-settings 版本"""
    
    # 只需要声明字段和类型，自动从环境变量读取
    database_url: str
    secret_key: str
    debug: bool = False  # 带默认值
    log_level: str = "INFO"
    max_connections: int = 10
    api_key: Optional[str] = None
    
    # 配置
    model_config = SettingsConfigDict(
        env_file=".env",           # 从 .env 文件读取
        env_file_encoding="utf-8",
        case_sensitive=False,       # 环境变量大小写不敏感
        extra="ignore",             # 忽略额外字段
    )

# 使用
settings = Settings()
print(settings.database_url)
print(f"调试模式: {settings.debug}")
```

```python
# 嵌套配置（使用 pydantic BaseModel）
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class DatabaseSettings(BaseModel):
    """数据库配置"""
    host: str = "localhost"
    port: int = 5432
    name: str = "mydb"
    user: str
    password: str

class Settings(BaseSettings):
    """主配置类"""
    database: DatabaseSettings
    
    model_config = SettingsConfigDict(env_file=".env")

# .env 中可以这样写：
# DATABASE__HOST=db.example.com
# DATABASE__PORT=5432
# DATABASE__NAME=production_db
# DATABASE__USER=admin
# DATABASE__PASSWORD=secret
```

> **pydantic-settings 的优势**：
> - **类型自动验证**：字符串 "123" 自动转成 int 123
> - **环境变量自动绑定**：字段名自动对应环境变量
> - **默认值支持**：没设置环境变量时有保底值
> - **敏感信息脱敏**：调试时不会打印密码
> - **IDE 友好**：有类型提示，敲代码时自动补全

### 17.5.4 configparser（INI 文件）

`configparser` 是 Python 标准库，用来解析 **INI 格式**的配置文件。这种格式结构清晰，适合项目配置文件。

```ini
; config.ini - INI 配置文件示例
[database]
host = localhost
port = 5432
name = mydb
user = admin
password = secret123

[server]
host = 0.0.0.0
port = 8000
debug = true

[logging]
level = INFO
file = app.log

[cache]
enabled = true
ttl = 3600
```

```python
import configparser

# 读取配置
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

# 访问配置
db_host = config["database"]["host"]
db_port = config.getint("database", "port")  # 自动转 int
db_debug = config.getboolean("server", "debug")  # 自动转 bool

# 遍历配置
for section in config.sections():
    print(f"[{section}]")
    for key, value in config[section].items():
        print(f"  {key} = {value}")
```

```python
# 写入配置
config = configparser.ConfigParser()
config["database"] = {
    "host": "localhost",
    "port": "5432",
    "name": "mydb",
}
config["server"] = {
    "debug": "true",
}

with open("config_new.ini", "w", encoding="utf-8") as f:
    config.write(f)
```

> **INI 格式适合什么场景？**
> - Windows 配置（经典的 `.ini` 文件）
> - 需要手动编辑的配置文件
> - 配置项不太多、结构不太复杂的情况
> - 如果配置有深层嵌套，INI 就不太适合了

### 17.5.5 TOML 文件解析

**TOML**（Tom's Obvious, Minimal Language）是一种配置文件格式，Python 3.11+ 内置了 `tomllib`，Python 3.11 之前可用第三方库 `tomli`。

```toml
# pyproject.toml 是最常见的 TOML 文件
[project]
name = "my-awesome-project"
version = "1.0.0"
description = "一个超厉害的项目"

[project.dependencies]
flask = "^3.0"
requests = "^2.31"

[tool.pytest]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.black]
line-length = 88
target-version = ['py310']

[tool.mypy]
python_version = "3.10"
warn_return_any = true
```

```python
# Python 3.11+ 内置 tomllib
import tomllib

with open("config.toml", "rb") as f:  # tomllib 需要二进制模式
    config = tomllib.load(f)

print(config["project"]["name"])
print(config["database"]["host"])

# 访问嵌套配置
db_config = config["database"]
print(f"连接: {db_config['host']}:{db_config['port']}")
```

```python
# Python 3.10 及之前用 tomli
try:
    import tomllib
except ImportError:
    import tomli as tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
```

```python
# 写入 TOML（用 tomli_w / tomlkit）
import tomli_w

config = {
    "project": {
        "name": "my-project",
        "version": "1.0.0",
    },
    "database": {
        "host": "localhost",
        "port": 5432,
    }
}

with open("config.toml", "wb") as f:
    tomli_w.dump(config, f)
```

> **TOML vs INI vs YAML**：
> - **INI**：简单，但不支持嵌套
> - **YAML**：支持嵌套，但缩进敏感，容易出错
> - **TOML**：支持嵌套，语法简洁，Python 官方推荐用于配置文件
> - 现代 Python 项目越来越多用 TOML，`pyproject.toml` 就是最佳证明

---

## 17.6 CI/CD

> CI/CD 全称 **Continuous Integration（持续集成）** 和 **Continuous Deployment（持续部署）**。简单说就是：代码提交后，自动运行测试、自动构建、自动部署——你只需要写代码，剩下的全部自动化。

### 17.6.1 GitHub Actions 自动化

**GitHub Actions** 是 GitHub 自带的 CI/CD 工具，免费额度很慷慨（2000 分钟/月），是开源项目和小团队的首选。

```
┌─────────────────────────────────────────────────────┐
│              GitHub Actions 工作流                   │
│                                                     │
│  代码 push/PR  ──→  触发 workflow  ──→  运行 job    │
│       │                                      │      │
│       │                               ┌──────┴──────┐│
│       │                               │  运行步骤   ││
│       │                               │  1. checkout││
│       │                               │  2. setup  ││
│       │                               │  3. lint   ││
│       │                               │  4. test   ││
│       │                               │  5. cover  ││
│       │                               └─────────────┘│
│       │                                      │        │
│       └──────────────  结果通知 ◄────────────┘        │
└─────────────────────────────────────────────────────┘
```

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
      
      - name: 设置 Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"  # 缓存依赖，加快速度
      
      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: 运行测试
        run: pytest --cov=my_app --cov-fail-under=80 -v
      
      - name: 上传覆盖率报告
        uses: codecov/codecov-action@v4
        if: matrix.python-version == '3.11'  # 只在一个版本上传报告
```

```yaml
# 更完整的 workflow，包含 lint 和构建
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.11"

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: 安装 lint 工具
        run: pip install black mypy ruff
      
      - name: 检查代码格式 (Black)
        run: black --check .
      
      - name: 运行静态检查 (mypy)
        run: mypy src/
      
      - name: 运行 lint (ruff)
        run: ruff check .

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: "pip"
      
      - name: 安装依赖
        run: pip install -r requirements-dev.txt
      
      - name: 运行测试
        run: pytest -v --cov=src --cov-fail-under=80
      
      - name: 上传测试覆盖率
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/

  build-and-release:
    runs-on: ubuntu-latest
    needs: [lint, test]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: 构建包
        run: |
          pip install build
          python -m build
      
      - name: 发布到 PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_TOKEN }}
```

> **secrets** 是 GitHub 存储敏感信息的地方。在仓库 Settings → Secrets and variables → Actions 中添加。你的 PyPI token、数据库密码等敏感信息都存在这里。

### 17.6.2 测试自动化（lint + test + coverage）

一套完整的测试自动化流水线：

```bash
# 本地模拟 CI 流程

# 1. 代码格式检查
black --check src/ tests/

# 2. Lint 检查
ruff check src/ tests/

# 3. 类型检查
mypy src/

# 4. 运行测试
pytest tests/ -v

# 5. 覆盖率检查
pytest tests/ --cov=src --cov-fail-under=80 --cov-report=term-missing
```

```makefile
# Makefile - 把常用命令做成快捷方式
.PHONY: install test lint format clean

install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=src --cov-fail-under=80

lint:
	black --check src/ tests/
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/
```

### 17.6.3 自动打包与发布

#### 打包到 PyPI

```bash
# 安装构建工具
pip install build

# 构建源码包和 wheel
python -m build

# 发布到 Test PyPI（测试用）
pip install twine
twine upload --repository testpypi dist/*

# 发布到正式 PyPI
twine upload dist/*
```

#### 自动发布 workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  release:
    types: [published]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: 构建发布包
        run: |
          pip install build
          python -m build
      
      - name: 发布到 PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_TOKEN }}
```

---

## 17.7 文档

> 代码写完了，文档在哪里？"文档？等我写完再补！"——这句话永远不会有实现的那一天。文档应该和代码同步进行，而不是事后补交。

### 17.7.1 Markdown 文档编写

Markdown 是最流行的轻量级标记语言，GitHub、GitLab、Notion 都原生支持。Python 项目的 README、CHANGELOG、贡献指南等都用 Markdown 写。

```markdown
# 项目名称

[![CI](https://github.com/you/project/actions/workflows/ci.yml/badge.svg)](https://github.com/you/project/actions)
[![PyPI version](https://badge.fury.io/py/project.svg)](https://pypi.org/project/)
[![Python versions](https://img.shields.io/pypi/pyversions/project.svg)](https://pypi.org/project/)

一行简短的项目描述。

## 安装

```bash
pip install project
```

## 快速开始

```python
from project import Client

client = Client(api_key="your-key")
result = client.do_something()
print(result)
```

## 功能特点

- ✅ 功能一：描述
- ✅ 功能二：描述
- ✅ 功能三：描述

## 配置

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| api_key | str | 必填 | API 密钥 |
| timeout | int | 30 | 超时时间（秒）|

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
```

> **README 的黄金法则**：
> - 前三行决定别人会不会继续看
> - 必须包含：是什么、能做什么、怎么安装、怎么用
> - 代码示例必须能直接运行
> - CI 状态徽章是标配

### 17.7.2 MkDocs（文档站点生成）

**MkDocs** 是一个用 Markdown 生成静态文档站点的工具，简单、好看、易用。

```bash
pip install mkdocs mkdocs-material  # material 是主题

# 初始化
mkdocs new my-docs
cd my-docs
```

```yaml
# mkdocs.yml - MkDocs 配置文件
site_name: 我的项目文档
site_description: 项目的详细文档
site_author: 你的名字

# 主题（material 是最流行的）
theme:
  name: material
  palette:
    primary: indigo
    accent: blue
  features:
    - navigation.instant   # 即时导航
    - navigation.tracking  # URL 跟随
    - content.code.copy    # 代码复制按钮
    - content.code.annotate  # 代码注释

# 插件
plugins:
  - search                # 搜索功能
  - gen-files:
      scripts:
        - docs/gen_api_ref.py  # 自动生成 API 文档

# 导航结构
nav:
  - Home: index.md
  - Getting Started:
      - 安装: getting-started/installation.md
      - 快速开始: getting-started/quickstart.md
  - Guide:
      - 基本用法: guides/basic-usage.md
      - 高级用法: guides/advanced.md
  - API Reference: api/index.md
  - Changelog: changelog.md
  - Contributing: contributing.md

# Markdown 扩展
markdown_extensions:
  - pymdownx.highlight:    # 代码高亮
      anchor_linenums: true
  - pymdownx.superfences  # 超级代码块
  - admonition           # 提示块（tip、warning 等）
  - toc:
      permalink: true
```

```bash
# 常用命令
mkdocs serve       # 本地预览（热重载）
mkdocs build       # 构建静态网站
mkdocs gh-deploy   # 部署到 GitHub Pages
mkdocs --help
```

```markdown
<!-- docs/index.md - 首页 -->
# 欢迎使用

这是一个功能强大、文档完善的 Python 项目。

## 安装

```bash
pip install my-project
```

> 💡 **提示**：建议在虚拟环境中安装

## 快速开始

5 分钟上手：

1. 获取 API Key
2. 安装包
3. 写代码

## 示例代码

```python
from my_project import Client

client = Client()
result = client.query("你好")
print(result)
```
```

### 17.7.3 Sphinx + Read the Docs

**Sphinx** 是 Python 官方文档工具，Python 自身的文档就是用 Sphinx 写的。它可以从 Python 代码的 docstring（文档字符串）自动生成 API 文档。配合 **Read the Docs** 可以实现自动托管文档网站。

```bash
# 安装 Sphinx
pip install sphinx sphinx-rtd-theme  # sphinx-rtd-theme 是 Read the Docs 主题

# 初始化文档项目
sphinx-quickstart docs
# 交互式问答后生成文档结构
```

```
docs/
├── _build/              # 构建输出（不用管）
├── _static/             # 静态文件
├── _templates/          # 模板
├── conf.py              # Sphinx 配置
├── index.rst            # 文档首页（reStructuredText 格式）
└── usage.rst            # 其他文档
```

```python
# docs/conf.py - Sphinx 配置
project = "My Project"
copyright = "2026, Your Name"
author = "Your Name"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",      # 自动从 docstring 生成文档
    "sphinx.ext.viewcode",     # 在文档中显示源代码
    "sphinx.ext.napoleon",     # 支持 Google/NumPy 风格的 docstring
    "sphinx.ext.intersphinx",  # 跨文档链接
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# autodoc 配置
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
```

```rst
<!-- docs/index.rst -->
Welcome to My Project's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

```bash
# 构建 HTML 文档
cd docs
make html

# 本地预览
# 打开 _build/html/index.html
```

#### Read the Docs 集成

1. 在 [readthedocs.org](https://readthedocs.org) 注册账号
2. 导入你的 GitHub 仓库
3. 配置触发构建（push 时自动构建）
4. 访问 `https://your-project.readthedocs.io/`

```yaml
# .readthedocs.yaml - Read the Docs 配置文件
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: docs/conf.py

python:
  install:
    - requirements: docs/requirements.txt
    - method: pip
      path: .
```

### 17.7.4 docstring 自动生成 API 文档

docstring（文档字符串）是写在函数/类/模块开头的字符串，用于说明代码功能。配合 Sphinx 的 autodoc 扩展，可以自动生成 API 文档。

```python
# my_module.py

def process_data(
    data: list[dict],
    filter_key: str = "status",
    filter_value: str = "active",
    batch_size: int = 100,
) -> list[dict]:
    """处理数据列表，按条件过滤并返回结果。

    这是 Google 风格的 docstring，也是目前最流行的风格。

    Args:
        data: 输入数据列表，每个元素是一个字典
        filter_key: 用于过滤的字典键名
        filter_value: 要保留的过滤值
        batch_size: 批处理大小，用于控制内存使用

    Returns:
        过滤后的数据列表

    Raises:
        ValueError: 当 data 为空或 filter_key 不存在时抛出

    Examples:
        >>> result = process_data(users, filter_key="role", filter_value="admin")
        >>> len(result)
        3

    Note:
        这个函数会修改原始数据的副本，不会修改原数据。
    """
    if not data:
        raise ValueError("data 不能为空")
    
    if filter_key not in data[0]:
        raise ValueError(f"filter_key '{filter_key}' 不存在于数据中")
    
    return [
        item for item in data
        if item.get(filter_key) == filter_value
    ][:batch_size]
```

```python
# 使用 NumPy 风格（也很流行）
class DataProcessor:
    """数据处理器类。

    Parameters
    ----------
    config : dict
        配置字典，包含处理参数。
    max_workers : int, optional
        最大并发数，默认为 4。

    Attributes
    ----------
    processor_name : str
        处理器名称。

    Examples
    --------
    >>> processor = DataProcessor({"timeout": 30})
    >>> processor.process([{"id": 1}])
    [{'id': 1, 'processed': True}]
    """
    
    def __init__(self, config: dict, max_workers: int = 4):
        self.config = config
        self.max_workers = max_workers
        self.processor_name = "DataProcessor"
    
    def process(self, data: list) -> list:
        """处理数据。

        Parameters
        ----------
        data : list
            要处理的数据列表。

        Returns
        -------
        list
            处理后的数据列表。
        """
        return [{"processed": True, "item": item} for item in data]
```

```python
# Sphinx autodoc - 在 docs/api.rst 中引用
# docs/api.rst

API 参考文档
=============

.. automodule:: my_module
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: DataProcessor
   :members:
   :undoc-members:
   :special-members: __init__
```

```bash
# 运行 autodoc 自动生成文档
# 1. 先生成 .rst 文件
sphinx-apidoc -f -o docs/ my_module.py

# 2. 构建文档
cd docs && make html
```

> **docstring 风格选择**：
> - **Google 风格**：简洁易读，`pip install numpydoc` 支持
> - **NumPy 风格**：结构化程度高，适合大型 API 文档
> - **Epytext 风格**：经典但较老，现在用得较少
> - 推荐用 **Google** 或 **NumPy** 风格

---

## 本章小结

这一章我们聊了 Python 工程化的方方面面，核心目标是让代码从"能跑就行"进化到"专业可靠"。以下是各节的核心要点：

### 项目结构规范
- 单文件脚本适合小工具，按"导入→配置→函数→主逻辑→入口"顺序组织
- 多模块包结构适合中型项目，通过 `__init__.py` 形成包
- **src 布局**（`src/your_package/`）是 PyPA 推荐的最佳实践，适合需要发布到 PyPI 的项目
- Flask 用应用工厂模式 + 蓝图，Django 用固定的项目结构
- 敏感配置（密码、密钥）绝对不能硬编码，更不能上传到 Git

### 依赖管理
- `requirements.txt` 是最基础的依赖文件，但不够灵活
- `pip-tools`（`pip-compile`）解决"开发时用灵活版本，部署时锁定版本"的问题
- **Poetry** 是现代 Python 项目的首选工具，一个工具搞定依赖+打包+发布
- **PDM** 支持 PEP 582，适合想尝鲜的开发者
- **uv** 是速度最快的包管理器（Rust 编写），2024-2025 年迅速走红，推荐尝试

### 测试
- `unittest` 是标准库自带的测试框架，源自 JUnit 的类继承写法
- **pytest** 是最流行的测试框架，函数式写法更简洁
- **Fixtures** 是 pytest 的核心功能，通过 `yield` 实现 setUp/tearDown
- **parametrize** 用一套代码测试多组数据，避免重复
- **markers** 给测试打标签，实现选择性运行
- **pytest-cov** 生成覆盖率报告，通常 80%-90% 是合理的覆盖率目标
- **Mock** 模拟外部依赖，让测试更稳定、更快
- **TDD**（测试驱动开发）是一种开发方法论："红→绿→重构"的循环

### 日志
- `logging` 模块有 5 个级别：DEBUG < INFO < WARNING < ERROR < CRITICAL
- Logger/Handler/Formatter/Filter 四层结构，Logger 产生日志，Handler 决定输出到哪里
- `logging.basicConfig()` 是快速配置方式，适合简单场景
- **loguru** 是更简单的日志库，开箱即用，异常捕获是其杀手级功能

### 配置管理
- 环境变量（`os.environ`）是最基础的配置方式，容器化部署必备
- `.env` 文件配合 `python-dotenv` 让本地开发更方便，记得加入 `.gitignore`
- **pydantic-settings** 提供类型安全的配置管理，自动验证类型、自动绑定环境变量
- `configparser` 解析 INI 格式配置文件，Windows 风格配置
- **TOML** 是现代 Python 项目的推荐配置文件格式，`pyproject.toml` 是最佳实践

### CI/CD
- **GitHub Actions** 是最方便的 CI/CD 工具，免费额度够用
- 典型 CI 流水线：checkout → setup python → install → lint → test → coverage
- `needs` 关键字让 job 之间有依赖关系
- `secrets` 用于存储敏感信息（API token、密码等）
- 本地用 `Makefile` 可以模拟 CI 的本地检查流程

### 文档
- Markdown 是基础中的基础，每个 Python 项目都应该有 README.md
- **MkDocs** + material 主题是生成漂亮文档站点的最简方案
- **Sphinx** 是 Python 官方文档工具，autodoc 扩展可以从 docstring 自动生成 API 文档
- **Read the Docs** 配合 GitHub 实现文档自动部署
- Google/NumPy 风格的 docstring 是目前的主流选择

> 工程化不是大项目的专利，小项目同样需要工程化思维。一个有工程化意识的程序员，写出来的代码结构清晰、测试完整、配置分离、文档齐全——这样的代码，无论是一个人维护还是团队协作，都是让人省心的代码。从今天起，让你的 Python 项目也"正规"起来吧！
