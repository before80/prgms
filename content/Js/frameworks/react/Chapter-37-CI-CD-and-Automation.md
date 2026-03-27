+++
title = "第37章 CI/CD与自动化"
weight = 370
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-37 - CI/CD 与自动化

## 37.1 GitHub Actions

### 37.1.1 CI/CD 的概念

在没有 CI/CD 的年代，开发者手动打包、上传服务器、盯着日志——听起来像远古 rituals，实际上也没好到哪里去。

**CI（Continuous Integration，持续集成）**：你的代码每次 push 到仓库，自动化流水线立即启动——安装依赖、运行测试、构建产物。任何一个人提交的代码有问题，都会第一时间暴露，而不是等到上线前夜才发现一团乱麻。

**CD（Continuous Deployment，持续部署）**：CI 跑通之后，CD 负责把通过测试的产物自动部署到服务器（测试环境、预发布环境，甚至生产环境）。从"代码写完"到"上线跑起来"，中间不再需要人工介入。

两者结合的效果：**你只需要 commit + push，剩下的全部交给机器**。这不只是偷懒的艺术，更是团队协作和代码质量的守护神。

### 37.1.2 编写第一个 workflow

```yaml
# .github/workflows/ci.yml
# workflow 名称，会显示在 GitHub Actions 页面标签上
name: CI

# 触发条件：
# push 时触发（可指定分支，这里监听 main）
# pull_request 时触发（有人提 PR 合并到 main 时自动运行）
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest  # 使用 GitHub 提供的 ubuntu 最新版虚拟机
    steps:
      # 检出代码：将仓库代码拉到虚拟机上
      - uses: actions/checkout@v4
      # 设置 Node.js 环境，指定版本为 20（LTS）
      # actions/setup-node@v4 是官方 Node.js 环境配置 action
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      # 安装依赖（npm ci 比 npm install 更适合 CI：基于 package-lock.json 精确安装，速度更快）
      - run: npm ci
      # 运行单元测试
      - run: npm test
      # 运行代码检查（ESLint 等）
      - run: npm run lint

  build:
    runs-on: ubuntu-latest
    # 依赖 test job：只有当 test 全部通过后，build 才会开始
    # 这是一种常见的流水线设计——测试不过就不构建，省资源也避免无效构建
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      # 构建生产产物（如 Vite build），生成 dist/ 目录供后续步骤使用
      - run: npm run build
```

### 37.1.3 自动测试、自动构建、自动部署

```yaml
deploy:
  runs-on: ubuntu-latest
  needs: build  # 依赖 build job，确保构建产物准备好后再部署
  steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npm run build
    # 使用 peaceiris/actions-gh-pages@v3 将构建产物发布到 GitHub Pages
    # github_token：GitHub 自动注入的访问令牌，无需手动配置，secrets.GITHUB_TOKEN 是内置 secret
    # publish_dir：发布哪个目录（这里是 Vite/Nest.js 的构建产物目录）
    # 注意：使用此 action 需要在仓库 Settings → Pages → Source 勾选 "GitHub Actions"
    - uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./dist
```

---

## 37.2 Docker 容器化

### 37.2.1 Dockerfile 编写

```dockerfile
# 多阶段构建：第一阶段（builder）在 Node.js 环境完成构建
# 第二阶段（production）只复制构建产物，用轻量的 nginx 镜像运行
# 这样最终镜像只包含运行产物，不包含 node_modules、构建工具等，体积大幅缩小
FROM node:20-alpine AS builder  # alpine 为精简版 Linux 发行版，体积更小
WORKDIR /app                       # WORKDIR 设置容器内的工作目录
COPY package*.json ./              # 先复制依赖文件（package.json + package-lock.json）
RUN npm ci                         # 安装依赖（CI 环境推荐用 npm ci 精确安装）
COPY . .                           # 再复制其余源代码
RUN npm run build                  # 执行构建命令，生成 dist/ 产物

# 第二阶段：生产镜像，只用到 nginx
FROM nginx:alpine  # nginx:alpine 镜像本身只有约 40MB（比 ubuntu/node 镜像小得多）
# --from=builder 引用第一阶段（builder）的产物，将 dist 目录复制到 nginx 的网站根目录
COPY --from=builder /app/dist /usr/share/nginx/html
# 将自定义 nginx 配置文件复制到 nginx 配置目录，覆盖默认配置
COPY nginx.conf /etc/nginx/conf.d/default.conf  # 自定义站点配置，覆盖默认的 default.conf
EXPOSE 80  # 声明容器对外暴露的端口（仅文档作用，实际运行需用 -p 映射）
# CMD：容器启动时执行的命令，-g "daemon off;" 让 nginx 以前台进程运行（避免容器立即退出）
CMD ["nginx", "-g", "daemon off;"]
```

### 37.2.2 多阶段构建优化体积

多阶段构建可以大幅减小镜像体积。

```nginx
# nginx.conf
server {
    listen 80;                        # 监听 80 端口（HTTP 默认端口）
    server_name localhost;             # 匹配的域名（localhost 表示仅本机访问）
    root /usr/share/nginx/html;        # 网站根目录，即 React 构建产物的所在路径
    index index.html;                  # 默认索引文件

    # SPA 路由支持（所有路径回退到 index.html）
    # try_files：首先尝试匹配文件/目录，若都不存在则回退到 index.html
    # 这对 React Router 等客户端路由至关重要，否则刷新会返回 404
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源长期缓存
    # /assets/ 路径下的文件（JS/CSS/图片等）设置 1 年缓存期
    # public：允许浏览器和 CDN 等中间节点缓存
    # immutable：告知浏览器该文件永不变更，直接使用缓存无需再验证
    # 注意：只有文件名带 hash 的构建产物（如 main.a1b2c3.js）才适合用 immutable
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**注意：** 如果不使用 Docker 多阶段构建，直接把 React 产物放在 nginx 的 `html/` 目录也是可以的——只是多阶段构建能让你最终镜像里不包含构建工具，体积更小。

---

## 37.3 自动化部署

### 37.3.1 Vercel / Netlify 自动部署

连接 GitHub 仓库，设置构建命令，push 代码自动触发部署。

**Vercel 部署 Next.js 示例：**
1. 在 [vercel.com](https://vercel.com) 用 GitHub 登录
2. 点击 "Import Project"，选择 GitHub 仓库
3. Vercel 会自动检测 Next.js 并填入构建命令（`next build`）
4. 点击 Deploy，之后每次 push 到 main 分支都会自动部署

**Netlify 部署 Vite React 项目：**
```toml
# netlify.toml
[build]
  command = "npm run build"   # 构建命令，Netlify 会执行此命令生成产物
  publish = "dist"            # 产物目录，Netlify 会将此目录下内容作为网站根目录部署

# 重定向规则（SPA 路由支持）
# 所有路径（/*）都重定向到 /index.html，返回 200 状态码（不是 301/302 浏览器感知不到的跳转）
# 效果等同于 nginx 的 try_files，让 React Router 等客户端路由正常工作
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

> 💡 **小技巧**：Vercel 和 Netlify 都有预览部署（Preview Deployments）功能——每个 PR 都会自动生成一个独立的预览链接，方便 Code Review！

### 37.3.2 GitHub Pages 部署

```yaml
- uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./dist
```

---

## 本章小结

本章我们学习了 CI/CD 与自动化：

- **GitHub Actions**：自动化测试、构建、部署
- **Docker**：容器化，构建多阶段镜像
- **自动化部署**：Vercel、Netlify、GitHub Pages

最后一章我们将展望 **React 的未来**！🔭