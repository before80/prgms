+++
title = "第27章 项目二——社交类应用"
weight = 270
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-27 - 项目二——社交类应用

## 27.1 项目架构设计

### 27.1.1 页面划分：Feed / 详情 / 个人页 / 消息

社交应用的核心页面设计，某种程度上决定了整个应用的用户体验基线。

**Feed（动态信息流）** 是用户打开 App 后第一个看到的页面，相当于社交应用的脸面。信息流的质量直接决定用户留存——帖子怎么排列（时间序？热度序？）、图片怎么展示（全部加载还是懒加载）、下拉刷新和无限滚动的体验，都是这里要解决的难题。

**详情页**包括帖子详情和用户详情。当用户点击某条动态或某个头像时，需要有一个"深入"的页面展示完整内容。它与 Feed 的关系是"从总览到细节"，要注意详情页的加载状态（骨架屏是标配）和返回后 Feed 状态的保持。

**个人页**是用户的"名片"，除了展示基本信息，还要能看到该用户发布的所有帖子列表。这里通常还需要一个"编辑资料"的功能入口（对自己可见，对他人隐藏或变成"关注/发消息"按钮）。

**消息模块**一般分两块：通知（谁点赞/评论/关注了你的内容）和私信（一对一的对话）。私信需要有实时能力，可以用 WebSocket 或轮询实现。

### 27.1.2 数据流设计：状态管理方案

```
用户操作 → Action → Reducer/Store → UI 更新
```

---

## 27.2 路由规划

### 27.2.1 React Router v7 路由配置

```jsx
function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/explore" element={<Explore />} />
      <Route path="/notifications" element={<Notifications />} />
      <Route path="/messages" element={<Messages />} />
      <Route path="/profile/:username" element={<Profile />} />
      <Route path="/post/:id" element={<PostDetail />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  )
}
```

### 27.2.2 路由守卫：登录拦截

```jsx
import { Navigate } from 'react-router-dom'

function ProtectedRoute({ children, isAuthenticated }) {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return children
}
```

---

## 27.3 全局状态

### 27.3.1 Zustand 管理用户状态

```jsx
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) => set({ user, token, isAuthenticated: true }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
      updateToken: (token) => set({ token })
    }),
    { name: 'auth-storage' }
  )
)
```

### 27.3.2 API 层封装（axios 实例 + 拦截器）

```jsx
import axios from 'axios'

// 创建 axios 实例，配置公共基础路径
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL  // .env 文件中定义，如 http://localhost:3000
})

// --------------------------------------------------
// 请求拦截器：每次发请求前自动执行
// --------------------------------------------------
api.interceptors.request.use(config => {
  // 从 zustand store 同步获取当前 token（不用 useStore 是因为这是请求拦截器，非组件内）
  const token = useAuthStore.getState().token
  if (token) {
    // 注入 Bearer Token，用于身份验证
    config.headers.Authorization = `Bearer ${token}`
  }
  return config  // 必须返回，否则请求会卡住
})

// --------------------------------------------------
// 响应拦截器：每次收到响应后自动执行
// --------------------------------------------------
api.interceptors.response.use(
  // 成功时：直接返回 data，省去每个调用处手动 .data
  response => response.data,
  // 失败时：统一处理 401 未授权
  error => {
    if (error.response?.status === 401) {
      // Token 过期或无效：登出并跳转登录页
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    // 其他错误：继续抛出，让调用方处理
    return Promise.reject(error)
  }
)
```

---

## 27.4 登录注册

### 27.4.1 React Hook Form + Zod 表单验证

```jsx
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'

const schema = z.object({
  email: z.string().email('邮箱格式不正确'),
  password: z.string().min(6, '密码至少6位')
})

function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  })

  async function onSubmit(data) {
    const { email, password } = data
    await loginApi({ email, password })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <p>{errors.email.message}</p>}
      <input type="password" {...register('password')} />
      {errors.password && <p>{errors.password.message}</p>}
      <button type="submit">登录</button>
    </form>
  )
}
```

### 27.4.2 JWT token 管理与刷新

```jsx
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.config && error.response?.status === 401) {
      try {
        // Token 过期，尝试用 refreshToken 获取新 token
        const newToken = await refreshToken()
        // 更新 store 中的 token（不改变登录状态）
        useAuthStore.getState().updateToken(newToken)
        // 用新 token 重新执行失败的那个请求
        error.config.headers.Authorization = `Bearer ${newToken}`
        return api.request(error.config)
      } catch {
        // refreshToken 也失败了（如 refreshToken 也过期），强制登出
        useAuthStore.getState().logout()
      }
    }
    return Promise.reject(error)
  }
)
```

### 27.4.3 登录状态持久化

```jsx
const useAuthStore = create(
  persist(
    (set) => ({ /* ... */ }),
    {
      name: 'auth-storage',  // localStorage 的 key 名
      // partialize：指定哪些 state 字段要持久化
      // 这里只存 user、token、isAuthenticated，不存其他临时状态
      // 好处：避免把不相关的数据（如 UI 状态、loading 等）也存进 localStorage
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated
      })
    }
  )
)
```

---

## 27.5 响应式设计

### 27.5.1 移动优先设计

```css
/* 移动优先 */
.layout { padding: 16px; }

@media (min-width: 768px) {
  .layout { padding: 24px; max-width: 960px; margin: 0 auto; }
}

@media (min-width: 1200px) {
  .layout { max-width: 1200px; }
}
```

### 27.5.2 触摸交互优化

```css
/* 触摸友好的按钮大小 */
button { min-height: 44px; min-width: 44px; }

/* 触摸时的高亮反馈 */
button:active { opacity: 0.8; transform: scale(0.98); }
```

### 27.5.3 图片懒加载

图片懒加载是社交类应用必备的优化手段——一个 Feed 可能有几十张图，如果一次性全加载，用户等半天看不到任何东西，还可能把浏览器搞崩。

实现思路：图片初始用占位图（或者透明图），等真实图片加载完成后再显示。常见做法有两种：

**方案一：CSS 占位 + onLoad 切换（推荐）**

```jsx
import { useState } from 'react'

function LazyImage({ src, alt }) {
  const [isLoaded, setIsLoaded] = useState(false)

  return (
    <div className="relative w-full h-full">
      {/* 占位层：图片加载完之前显示 */}
      {!isLoaded && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse" />
      )}
      <img
        src={src}
        alt={alt}
        loading="lazy"  {/* 浏览器原生懒加载 */}
        onLoad={() => setIsLoaded(true)}
        className={`w-full h-full object-cover transition-opacity duration-300 ${
          isLoaded ? 'opacity-100' : 'opacity-0'
        }`}
      />
    </div>
  )
}
```

**方案二：Intersection Observer（更精细的控制）**

如果需要"滚动到视口才加载"，可以用 Intersection Observer API，在图片进入可视区之前连请求都不发。

```jsx
import { useState, useEffect, useRef } from 'react'

function LazyImage({ src, alt }) {
  const [isVisible, setIsVisible] = useState(false)
  const [isLoaded, setIsLoaded] = useState(false)
  const imgRef = useRef(null)

  useEffect(() => {
    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        setIsVisible(true)  // 进入视口，加载图片
        observer.disconnect()
      }
    })
    observer.observe(imgRef.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div ref={imgRef} className="relative">
      {!isLoaded && <div className="absolute inset-0 bg-gray-200 animate-pulse" />}
      {isVisible && (
        <img
          src={src}
          alt={alt}
          onLoad={() => setIsLoaded(true)}
          className={`transition-opacity ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
        />
      )}
    </div>
  )
}
```

方案一简单够用，方案二更省流量。社交 Feed 场景下方案一就足够了，除非你的列表特别长、图特别多。

---

## 本章小结

本章我们完成了社交类应用的架构设计：

- **路由规划**：React Router v7 路由守卫实现登录拦截
- **全局状态**：Zustand 管理用户状态，持久化到 localStorage
- **API 层封装**：axios 实例 + 拦截器统一处理 token
- **登录注册**：React Hook Form + Zod 表单验证
- **响应式设计**：移动优先、触摸交互优化、图片懒加载

下一个项目我们将实现一个 **电商后台管理系统**！📊