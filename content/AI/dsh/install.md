+++
title = "安装deepseek harness"
date = 2026-09-18T15:06:57+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++



## Macbook Pro

```bash
# corepack enable 是 Node.js 生态中的包管理器管理命令。
# 因为 DeepSeek Harness 的 dsh plugin 需要调用 pnpm
# 开启后，在遇到需要使用pnpm的时候会提示你类似如下的内容：
# ! Corepack is about to download https://registry.npmjs.org/pnpm/-/pnpm-12.4.2.tgz
# ? Do you want to continue? [Y/n] 这里你需要输入 y
# Downloading the pnpm 12.4.2 binary for darwin-arm64...
sudo corepack enable

# 建议安装 dshmarket 插件
# 之后就可以通过该插件，在web页面方便安装其他插件了
npx @deepseek-ai/dsh plugin --profile web add dshmarket

# 其他建议安装的插件还有：
# dsh-web-all            DSH Web UI 全家桶聚合插件：一键安装家族的全部功能插件
#                       （任务看板 / Git 图谱 / 宠物 / 移动端远程 / SSH / 模型能力 / 会话归档 
#                         / 皮肤 / 设置区 / 社区插件）
# dsh-find-plugin       让 AI 自己找插件
# dsh-better-sidebar    侧边栏,注意： 可能会和原生web界面冲突，先放一边
# dsh-token-usage-stats Token使用情况统计,但安装了dsh-web-all后，也可以放一边
# dsh-at-file           使用@符号可以引用目录下的文件,但安装了dsh-web-all后，也可以放一边
# ModLens               外挂视觉插件，为 DeepSeek、GLM 等纯文本模型外挂视觉能力，
#                       粘贴图片即得结构化 JSON 证据（OCR、版面、语义）
#                       但，目前 Deepseek-v4-flash-vision-EXP 等原生多模态模型已经可以看图，
#                       故也可以放一边
# browser-skill-dsh-plugin  BrowserSkill 的 DeepSeek Harness 浏览器自动化桥接插件，
# 通过原生浏览器工具控制可见的 Chrome 和 Edge Agent Window，
# 支持可访问性与 VOM 页面观察、截图、隔离的多会话控制和 Web UI 实时观察浮层。

# 安装 dsh web,即 deepseek harness
npx @deepseek-ai/dsh web


# 端口被占用时先找出是哪个进程占用
# 会列出类似如下的信息：
# COMMAND   PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
# node    26956   lx   15u  IPv4 0xc6a28494d62936b9      0t0  TCP 127.0.0.1:3080 (LISTEN)
lsof -nP -iTCP:3080 -sTCP:LISTEN

# 此时只需执行
# 这里的PID是上面PID对应的数字
kill PID
# 若不能退出则执行
# kill -9 PID 
# 来强制退出


```

