+++
title = "附录 A VS Code 插件推荐"
weight = 1000
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 附录 A VS Code 插件推荐

> VS Code 是 Vue 3 开发的首选编辑器，而插件是 VS Code 的灵魂。这一章我们整理了 Vue 3 开发中必备的、实用的、锦上添花的各类插件，让你的开发效率更上一层楼。

## A.1 Volar（Vue 官方插件）

**插件名称**：Vue - Official（Volar）
**插件 ID**：`Vue.volar`
**安装地址**：VS Code 扩展商店搜索 "Volar"

**这是 Vue 3 开发者最重要的插件，没有之一。** 它是 Vue 官方出品的 VS Code 扩展，提供了对 Vue 3 单文件组件（`.vue`）的完整支持：

- **语法高亮**：对 `<template>`、`<script>`、`<style>` 三部分分别高亮，互不干扰
- **智能提示**：输入 Vue 3 API 时提供自动补全，包括 `ref(`、`reactive(`、`computed(` 等
- **类型检查**：结合 TypeScript，在编写时就能发现类型错误
- **模板验证**：检查模板中的 HTML 语法错误、错误的指令用法
- **跳转到定义**：`F12` 可以跳转到组件、props、方法的定义处
- **组件引用查找**：右键点击组件名，可以查找所有引用位置

**安装后注意**：如果你之前安装了给 Vue 2 用的 **Vetur**，必须先禁用它——两个插件同时启用会产生冲突。

## A.2 TypeScript Vue Plugin

**插件名称**：TypeScript Vue Plugin
**插件 ID**：`Vue.vscode-typescript-vue-plugin`

这是 Volar 的"辅助插件"，作用是让 TypeScript 语言服务能够正确识别 `.vue` 文件的模块引用。在编写 TypeScript 代码时，如果 import 了一个 `.vue` 文件，TypeScript 需要这个插件才能知道 `.vue` 文件的类型。

**安装后无需配置**，Volar 会自动检测并协同工作。

## A.3 ESLint / Prettier

**ESLint**：`ESLint`（插件 ID：`dbaeumer.vscode-eslint`）
**Prettier**：`Prettier - Code formatter`（插件 ID：`esbenp.prettier-vscode`）

这两个插件在第一章已经详细介绍过，它们分别是代码质量检查工具和代码格式化工具。安装后建议在 `settings.json` 中配置保存时自动格式化：

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[vue]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## A.4 Auto Close Tag

**插件名称**：Auto Close Tag
**插件 ID**：`formulahendry.auto-close-tag`

这个插件会自动补全 HTML/XML 标签的闭合标签。

- 输入 `<div>`，自动生成 `</div>`
- 输入 `</`，自动选择要闭合的标签
- 修改开始标签时，自动更新结束标签

对于 Vue 的模板部分也非常有用，特别是当模板里有很多嵌套标签时。

## A.5 GitLens

**插件名称**：GitLens — Git supercharged
**插件 ID**：`eamodio.gitlens`

GitLens 是 Git 的超级增强器，它的核心功能是**在代码里直接显示每一行的最后提交信息和作者**。

安装了 GitLens 之后，你不需要打开 Git 面板，不需要运行 `git blame`，在代码编辑器里就能看到：

```text
const count = ref(0)  // ← 这行代码是谁改的？什么时候改的？commit message 是什么？
```

这对于团队协作和代码审查来说非常方便，可以快速追溯某个功能的实现来源。

**核心功能**：

- 行级别 blame 注释
- 提交历史可视化
- 文件历史对比
- 团队成员贡献统计

## A.6 REST Client

**插件名称**：REST Client
**插件 ID**：`humao.rest-client`

如果你的项目中需要调试 API 接口，这个插件可以让你在 VS Code 里直接发送 HTTP 请求，不需要切换到 Postman 或 Insomnia。

```http
### 获取用户列表
GET https://api.example.com/users
Authorization: Bearer {{token}}
Content-Type: application/json

### 创建用户
POST https://api.example.com/users
Content-Type: application/json

{
  "name": "小明",
  "email": "xiaoming@example.com"
}
```

安装后新建一个 `.http` 文件，把上面的内容粘贴进去，点击 "Send Request" 即可直接在 VS Code 里看到响应结果。

---

## 附录小结

本章推荐了 Vue 3 开发中最重要的 VS Code 插件：

- **Volar + TypeScript Vue Plugin**：Vue 3 开发的必备组合
- **ESLint + Prettier**：代码质量和格式的守护神
- **Auto Close Tag**：减少无谓的标签闭合操作
- **GitLens**：代码历史的透明化工具
- **REST Client**：API 调试神器

另外还有一些锦上添花的插件值得一试：

| 插件 | 用途 |
|------|------|
| **Bracket Pair Colorizer 2** | 彩虹括号配对，找匹配更直观 |
| **Error Lens** | 把 ESLint/TS 错误直接显示在代码行上 |
| **Import Cost** | 显示 import 语句的包体积大小 |
| **Excel Viewer** | 在 VS Code 里查看 CSV/Excel 数据 |
| **Markdown Preview Enhanced** | 增强型 Markdown 预览 |

