+++
title = "第32章 Next.js全栈开发"
weight = 320
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-32 - Next.js 全栈开发

## 32.1 Next.js 概述

### 32.1.1 Next.js App Router vs Pages Router

| 对比项 | Pages Router | App Router |
|--------|------------|------------|
| **路由** | 基于文件系统 | 基于文件系统 |
| **组件** | 客户端组件 | 服务端组件优先 |
| **数据获取** | getServerSideProps | async Server Components |
| **推荐场景** | 现有项目 | 新项目 |

### 32.1.2 App Router 的新特性

- **服务端组件默认**：组件默认是服务端的
- **React 19 支持**：App Router 是 React 19 特性的完整支持
- **嵌套布局**：layout.tsx 实现嵌套布局

### 32.1.3 迁移策略

从 Pages Router 迁移到 App Router：
1. **创建 `app/` 目录**：这是整个迁移的起点，App Router 所有文件都在 `app/` 下
2. **迁移 `_app.tsx` → `app/layout.tsx`**：原 `_app.tsx` 负责全局布局和 Providers，现在由 `layout.tsx` 替代。注意：`layout.tsx` 是根布局，会包裹所有页面，是迁移的核心
3. **`_document.tsx` 的职责已被 `app/layout.tsx` 内置的 `<html>` / `<body>` 标签替代**：以前用来控制 `<head>` 标签的地方，现在直接写在 `layout.tsx` 里，不需要单独文件了
4. **逐步迁移页面（优先迁移静态页面和数据获取逻辑）**：建议从最简单、交互最少的页面开始试水，把复杂的带交互页面留到最后，避免一次性迁移踩坑导致回滚困难

---

## 32.2 服务端组件

### 32.2.1 默认是服务端组件

App Router 中，组件默认是**服务端组件**——代码在服务器上运行，产物直接发送给浏览器。

```jsx
// app/page.tsx
// 这是服务端组件，可以直接访问数据库、文件系统
async function HomePage() {
  const posts = await db.posts.findMany()  // 直接数据库查询！
  return <PostList posts={posts} />
}
```

### 32.2.2 "use client" 指令：客户端组件

需要客户端交互的组件用 `"use client"` 声明：

```jsx
'use client'

import { useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

### 32.2.3 服务端组件 vs 客户端组件的选择

| 场景 | 推荐 |
|------|------|
| 数据获取 | 服务端组件 |
| 访问后端资源 | 服务端组件 |
| 用户交互、事件处理 | 客户端组件 |
| useState / useEffect | 客户端组件 |

---

## 32.3 数据获取

### 32.3.1 async / await 直接获取数据

```jsx
// app/users/page.tsx
async function UsersPage() {
  const users = await fetch('https://api.example.com/users').then(r => r.json())

  return (
    <ul>
      {users.map(u => <li key={u.id}>{u.name}</li>)}
    </ul>
  )
}
```

### 32.3.2 fetch 的 cache / revalidate 选项

```jsx
// 默认缓存
fetch('https://api.example.com/data')

// 不缓存（SSR）
fetch('https://api.example.com/data', { cache: 'no-store' })

// 重新验证（ISR）
fetch('https://api.example.com/data', { next: { revalidate: 3600 } })
```

### 32.3.3 静态生成（SSG）与增量静态再生成（ISR）

**SSG（Static Site Generation，静态站点生成）** 和 **ISR（Incremental Static Regeneration，增量静态再生成）** 是两种静态页面策略：

- **SSG**：构建时生成，部署后内容固定不变，直到下次构建。常用于文档、博客等几乎不改动的页面。优点是性能极高（纯静态文件），缺点是内容更新需要重新部署
- **ISR**：SSG 的"进化版"——页面仍然是静态的，但在部署后可以按需重新生成。比如设置 `revalidate: 3600`，页面在首次访问后 1 小时内有更新请求就会触发后台重新生成。用户下次访问就能看到新内容，而无需整个站点重新部署。适合内容频繁更新但又不至于实时变化的场景（如电商商品页、新闻文章）

---

## 32.4 API 层

### 32.4.1 Route Handlers：创建 API 端点

```jsx
// app/api/users/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const users = await db.users.findMany()
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const body = await request.json()
  const user = await db.users.create({ data: body })
  return NextResponse.json(user)
}
```

### 32.4.2 请求与响应处理

```jsx
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')

  if (!id) {
    return NextResponse.json({ error: '缺少 id' }, { status: 400 })
  }

  return NextResponse.json({ id, name: '用户' })
}
```

---

## 32.5 SEO 优化

### 32.5.1 metadata API

```jsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: '我的网站',
  description: '这是我的网站描述'
}
```

### 32.5.2 generateMetadata 的使用

```jsx
// ⚠️ 注意：Next.js 15+ 中 params 是 Promise，需先 await
type Props = { params: Promise<{ id: string }> }

export async function generateMetadata({ params }: Props) {
  const { id } = await params  // 先解析 params
  const product = await getProduct(id)

  return {
    title: product.name,
    description: product.description
  }
}
```

### 32.5.3 结构化数据（Schema.org）

**结构化数据**是一种让搜索引擎"读懂"页面内容的标准化格式（Google 称其为 Schema）。在页面中嵌入 JSON-LD 脚本后，搜索引擎可以在搜索结果中显示商品评分、价格等丰富摘要，大幅提升点击率。`next-seo` 库提供了 `JsonLd` 组件，方便在 Next.js 中注入结构化数据。

```jsx
import { JsonLd } from 'next-seo'

export default function ProductPage({ product }) {
  return (
    <>
      <JsonLd
        item={{
          '@context': 'https://schema.org',
          '@type': 'Product',
          name: product.name,
          image: product.image,
          description: product.description
        }}
      />
      {/* 页面内容 */}
    </>
  )
}
```

---

## 本章小结

本章我们对 Next.js 全栈开发进行了全面学习：

- **App Router vs Pages Router**：App Router 是新一代路由，推荐新项目使用
- **服务端组件**：组件默认在服务端运行，可直接访问数据库
- **数据获取**：async/await 直接获取数据，fetch 的 cache/revalidate 选项
- **Route Handlers**：创建 API 端点，处理 GET/POST 请求
- **SEO 优化**：metadata API、结构化数据

Next.js 是 React 生态中最强大的全栈框架！下一章我们将学习 **React 生态精选库**！🛠️