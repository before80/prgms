+++
title = "第19章 HTTP请求与数据获取"
weight = 190
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-19 - HTTP 请求与数据获取

## 19.1 fetch API

### 19.1.1 fetch 的基本用法

`fetch` 是浏览器原生的网络请求 API，不需要安装任何库。

```javascript
// 基本语法
fetch(url, options)
  .then(response => {
    // 处理响应
    return response.json()  // 解析 JSON
  })
  .then(data => {
    console.log(data)
  })
  .catch(error => {
    console.error('请求失败:', error)
  })
```

### 19.1.2 GET 请求与查询参数拼接

```javascript
// 简单的 GET 请求
fetch('https://api.example.com/users')
  .then(res => res.json())
  .then(data => console.log(data))

// 带查询参数
const params = new URLSearchParams({
  page: 1,
  limit: 10,
  category: 'tech'
})

fetch(`https://api.example.com/articles?${params}`)
  .then(res => res.json())
  .then(data => console.log(data))

// 或者手动拼接
fetch('https://api.example.com/users?page=1&limit=10')
  .then(res => res.json())
```

### 19.1.3 POST 请求与请求体（JSON / FormData）

```javascript
// POST JSON
fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token123'
  },
  body: JSON.stringify({
    name: '小明',
    email: 'xiaoming@example.com',
    age: 25
  })
})
  .then(res => {
    if (!res.ok) {
      throw new Error(`HTTP 错误！状态码：${res.status}`)
    }
    return res.json()
  })
  .then(data => console.log('创建成功:', data))
  .catch(err => console.error('请求失败:', err))

// POST FormData（文件上传等）
const formData = new FormData()
formData.append('name', '小明')
formData.append('avatar', fileInput.files[0])

fetch('https://api.example.com/upload', {
  method: 'POST',
  body: formData
  // 注意：FormData 不需要手动设置 Content-Type
})
  .then(res => res.json())
```

### 19.1.4 fetch 的错误处理：response.ok 与 try-catch

```javascript
async function fetchUser(id) {
  try {
    const res = await fetch(`https://api.example.com/users/${id}`)

    // 检查 HTTP 状态码
    if (!res.ok) {
      if (res.status === 404) {
        throw new Error('用户不存在')
      }
      if (res.status === 401) {
        throw new Error('未授权，请重新登录')
      }
      throw new Error(`请求失败：${res.status} ${res.statusText}`)
    }

    const data = await res.json()
    return data

  } catch (error) {
    // 捕获网络错误（如断网）
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error('网络连接失败，请检查网络')
    }
    throw error  // 其他错误重新抛出
  }
}
```

### 19.1.5 fetch 的超时处理：AbortController

fetch 默认没有超时机制，需要用 AbortController 实现：

```javascript
async function fetchWithTimeout(url, options = {}, timeout = 5000) {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)

  try {
    const res = await fetch(url, {
      ...options,
      signal: controller.signal
    })
    clearTimeout(timeoutId)
    return res
  } catch (error) {
    clearTimeout(timeoutId)
    if (error.name === 'AbortError') {
      throw new Error('请求超时')
    }
    throw error
  }
}

// 使用
try {
  const res = await fetchWithTimeout('https://api.example.com/data', {}, 3000)
  const data = await res.json()
  console.log(data)
} catch (err) {
  console.error(err.message)
}
```

---

## 19.2 axios 详解

### 19.2.1 axios vs fetch 的优势

| 对比项 | fetch | axios |
|--------|-------|-------|
| **安装** | 无需安装（浏览器原生） | 需要 npm install |
| **超时处理** | 需要 AbortController | 原生支持 timeout |
| **错误处理** | HTTP 错误不会自动抛出 | 4xx/5xx 都会 reject |
| **请求/响应拦截器** | 不支持 | 原生支持 |
| **JSON 自动转换** | 需要手动 res.json() | 自动 |
| **文件上传进度** | 需要特殊处理 | 原生支持 |
| **取消请求** | AbortController | CancelToken（已废弃，推荐 AbortController）|

简单来说：**fetch 够用但功能简陋，axios 功能齐全但需要安装**。实际项目中 axios 更常用，特别是拦截器和自动错误处理能省很多代码。

### 19.2.2 GET/POST/PUT/DELETE 的写法

```javascript
import axios from 'axios'

// GET 请求
axios.get('/api/users')
  .then(res => console.log(res.data))
  .catch(err => console.error(err))

// GET 带参数
axios.get('/api/users', {
  params: { page: 1, limit: 10 }
})

// POST 请求
axios.post('/api/users', {
  name: '小明',
  email: 'xiaoming@example.com'
})

// PUT 请求（全量更新）
axios.put('/api/users/123', {
  name: '新名字',
  email: 'new@example.com'
})

// PATCH 请求（部分更新）
axios.patch('/api/users/123', {
  name: '只改名字'
})

// DELETE 请求
axios.delete('/api/users/123')
```

### 19.2.3 请求拦截器与响应拦截器

拦截器是 axios 最强大的功能之一——在请求发送前和响应返回后统一处理：

```javascript
import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：在请求发送之前处理
api.interceptors.request.use(
  config => {
    // 添加 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 添加时间戳防止缓存
    config.params = {
      ...config.params,
      _t: Date.now()
    }

    console.log('发送请求:', config.method?.toUpperCase(), config.url)
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器：在响应返回之后处理
api.interceptors.response.use(
  response => {
    console.log('收到响应:', response.status, response.config.url)
    // 可以统一处理响应数据
    return response.data  // 直接返回 data 而非整个 response
  },
  error => {
    // 统一处理错误
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // token 过期，跳转登录页
          window.location.href = '/login'
          break
        case 403:
          console.error('没有权限')
          break
        case 404:
          console.error('资源不存在')
          break
        case 500:
        case 502:
        case 503:
          console.error('服务器错误')
          break
      }
    } else if (error.request) {
      console.error('网络错误')
    }
    return Promise.reject(error)
  }
)

export default api
```

### 19.2.4 统一错误处理

```javascript
// 定义错误类型
class ApiError extends Error {
  constructor(message, code, status) {
    super(message)
    this.code = code
    this.status = status
  }
}

// 响应拦截器中的统一错误处理
api.interceptors.response.use(
  response => response.data,
  error => {
    let apiError

    if (error.response) {
      const { status, data } = error.response
      apiError = new ApiError(
        data.message || '请求失败',
        data.code,
        status
      )
    } else if (error.request) {
      apiError = new ApiError('网络连接失败', 'NETWORK_ERROR', 0)
    } else {
      apiError = new ApiError(error.message, 'UNKNOWN', -1)
    }

    return Promise.reject(apiError)
  }
)
```

### 19.2.5 封装一个 axios 实例

```javascript
// api/request.js
import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,  // API 基础路径，所有请求都会自动拼接此前缀
                                                  // 例如 baseURL = '/api'，请求 '/users' 实际发往 '/api/users'
  timeout: 15000,                                // 请求超时时间（毫秒），超过此时间未收到响应则中断请求
  headers: {
    'Content-Type': 'application/json'          // 默认请求头，告诉后端发送的是 JSON 数据
                                                  // 注意：上传 FormData 时需要删除此行（axios 会自动设置正确的 multipart/form-data）
  }
})

request.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.message || error.message
    console.error('API 错误:', message)
    return Promise.reject(error)
  }
)

export default request
```

```javascript
// api/users.js
import request from './request'

export const userApi = {
  // 获取用户列表
  getUsers(params) {
    return request.get('/users', { params })
  },

  // 获取单个用户
  getUserById(id) {
    return request.get(`/users/${id}`)
  },

  // 创建用户
  createUser(data) {
    return request.post('/users', data)
  },

  // 更新用户
  updateUser(id, data) {
    return request.put(`/users/${id}`, data)
  },

  // 删除用户
  deleteUser(id) {
    return request.delete(`/users/${id}`)
  }
}
```

---

## 19.3 请求实战：loading、error、success 三状态

### 19.3.1 三状态的设计模式

数据请求有三种典型状态：**加载中（Loading）**、**错误（Error）**、**成功（Success）**。

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  async function loadUser() {
    setLoading(true)
    setError(null)
    try {
      const data = await userApi.getUserById(userId)
      setUser(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadUser()
  }, [userId])

  if (loading) return <div className="loading">加载中...</div>
  if (error) return <div className="error">❌ {error}</div>
  if (!user) return null

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

### 19.3.2 自定义 Hook 封装：useAsync

把三状态模式封装成自定义 Hook，实现复用：

```javascript
import { useState, useEffect, useCallback } from 'react'

function useAsync(asyncFunction, dependencies = []) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const execute = useCallback(async (...args) => {
    setLoading(true)
    setError(null)
    try {
      const result = await asyncFunction(...args)
      setData(result)
      return result
    } catch (err) {
      setError(err.message || '请求失败')
      throw err
    } finally {
      setLoading(false)
    }
  }, dependencies)

  useEffect(() => {
    execute()
  }, [execute])

  return { data, loading, error, execute, setData }
}

// 使用
function UserProfile({ userId }) {
  const { data: user, loading, error, execute } = useAsync(
    () => userApi.getUserById(userId),
    [userId]
  )

  if (loading) return <div>加载中...</div>
  if (error) return <div>❌ {error}</div>

  return (
    <div>
      <h1>{user?.name}</h1>
      <button onClick={() => execute()}>刷新</button>
    </div>
  )
}
```

### 19.3.3 错误处理与重试机制

```javascript
async function fetchWithRetry(url, options = {}, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url, options)
      if (!res.ok && i < retries - 1) {
        console.log(`请求失败，${retries - i - 1}次重试中...`)
        await new Promise(r => setTimeout(r, 1000 * (i + 1)))  // 线性退避（1s, 2s, 3s...）
        continue
      }
      return res
    } catch (error) {
      if (i === retries - 1) throw error
      console.log(`网络错误，${retries - i - 1}次重试中...`)
      await new Promise(r => setTimeout(() => {}, 1000 * (i + 1)))  // 线性退避
    }
  }
}
```

### 19.3.4 骨架屏（Skeleton）提升用户体验

骨架屏是在数据加载完成前显示的"占位"UI，让用户知道页面正在加载：

```jsx
function UserProfileSkeleton() {
  return (
    <div className="profile">
      <div className="skeleton avatar-skeleton"></div>
      <div className="skeleton title-skeleton"></div>
      <div className="skeleton text-skeleton"></div>
      <div className="skeleton text-skeleton short"></div>
    </div>
  )
}

// CSS
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## 19.4 TanStack Query（React Query）

### 19.4.1 TanStack Query 的核心概念：缓存即是状态

在 React 应用中，数据有两类：

1. **本地状态**：比如表单输入、弹窗开关，这类数据存在组件的 `useState` 里
2. **服务器状态**：从后端获取的用户信息、商品列表，这类数据本来不属于你的应用，是"借来的"

传统做法是：把服务器数据也放进 `useState`，等 API 返回后再 `setState`。但这会产生一堆问题：
- 每次路由切换都要重新请求（没有缓存）
- 多个组件要用同一份数据怎么办？（层层 prop drilling）
- 用户切换页面再回来，数据过期了怎么办？（手动刷新）

**TanStack Query**（原名 React Query）是目前最强大的 React 数据获取和缓存管理库。它的核心思想是：**服务器状态是缓存，而不是本地状态**。

打个比方：TanStack Query 就像给后端数据建了一个"图书馆"——你不用每次都跑去后端"借书"（请求），图书馆会帮你缓存、管理、更新这些书。你只需要说"我要第3章"，图书馆自动决定是给你缓存还是去后端拿新的。

```jsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// 安装
// npm install @tanstack/react-query

function App() {
  return (
    <QueryClientProvider client={new QueryClient()}>
      <UserList />
    </QueryClientProvider>
  )
}

function UserList() {
  // useQuery：获取数据
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['users'],          // 缓存的唯一标识
    queryFn: () => fetch('/api/users').then(r => r.json()),
    staleTime: 5 * 60 * 1000,   // 5分钟内数据被认为是"新鲜"的
    cacheTime: 10 * 60 * 1000,   // 10分钟后从缓存中移除
  })

  if (isLoading) return <div>加载中...</div>
  if (error) return <div>错误：{error.message}</div>

  return (
    <div>
      {data.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
      <button onClick={() => refetch()}>刷新</button>
    </div>
  )
}
```

### 19.4.2 useQuery / useMutation 的基本用法

```javascript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

function ProductList() {
  // 查询
  const { data: products, isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: () => api.getProducts(),
  })

  // 缓存管理器
  const queryClient = useQueryClient()

  // 变更操作
  const addProduct = useMutation({
    mutationFn: (newProduct) => api.createProduct(newProduct),
    onSuccess: () => {
      // 成功后使缓存失效，重新获取
      queryClient.invalidateQueries({ queryKey: ['products'] })
    }
  })

  if (isLoading) return <div>加载中...</div>

  return (
    <div>
      <button
        onClick={() => addProduct.mutate({ name: '新产品', price: 99 })}
        disabled={addProduct.isLoading}
      >
        {addProduct.isLoading ? '添加中...' : '添加产品'}
      </button>

      {products?.map(p => (
        <div key={p.id}>{p.name} - ¥{p.price}</div>
      ))}
    </div>
  )
}
```

### 19.4.3 缓存、预取、乐观更新

```javascript
// 缓存策略
useQuery({
  queryKey: ['user', userId],
  queryFn: () => api.getUser(userId),
  staleTime: 5 * 60 * 1000,  // 5分钟内不重新请求
  gcTime: 30 * 60 * 1000,    // 30分钟后清理缓存
})

// 预取：当用户悬停在某个项目上时预取数据
function ProductCard({ product }) {
  const queryClient = useQueryClient()

  function handleHover() {
    queryClient.prefetchQuery({
      queryKey: ['product', product.id],
      queryFn: () => api.getProduct(product.id),
    })
  }

  return (
    <div onMouseEnter={handleHover}>
      <span>{product.name}</span>
    </div>
  )
}

// 乐观更新：先更新 UI，后请求服务器
const updateTodo = useMutation({
  mutationFn: (updatedTodo) => api.updateTodo(updatedTodo),
  onMutate: async (newTodo) => {
    // 取消正在进行的请求
    await queryClient.cancelQueries({ queryKey: ['todos'] })

    // 保存当前数据
    const previousTodos = queryClient.getQueryData(['todos'])

    // 乐观更新
    queryClient.setQueryData(['todos'], old =>
      old.map(t => t.id === newTodo.id ? newTodo : t)
    )

    return { previousTodos }
  },
  onError: (err, newTodo, context) => {
    // 失败后回滚
    queryClient.setQueryData(['todos'], context.previousTodos)
  },
  onSettled: () => {
    // 最终同步服务器数据
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  }
})
```

### 19.4.4 离线支持与 background refetch

```javascript
// 离线支持：网络恢复时自动重新请求
useQuery({
  queryKey: ['data'],
  queryFn: () => api.getData(),
  networkMode: 'offlineFirst',  // 离线优先
  refetchOnWindowFocus: true,   // 窗口获得焦点时重新请求
  refetchOnReconnect: true,     // 网络恢复时重新请求
})

// 后台静默刷新
useQuery({
  queryKey: ['data'],
  queryFn: () => api.getData(),
  refetchInterval: 30 * 1000,  // 每30秒自动刷新（后台）
  refetchIntervalInBackground: false,  // 标签页不可见时不刷新
})
```

### 19.4.5 TanStack Query vs SWR vs fetch：选型建议

| 特性 | TanStack Query | SWR | fetch/useEffect |
|------|---------------|-----|----------------|
| **缓存管理** | 强大 | 一般 | 无 |
| **DevTools** | 官方支持 | 官方支持 | 无 |
| **乐观更新** | 原生支持 | 需手动实现 | 无 |
| **离线支持** | 优秀 | 一般 | 无 |
| **学习曲线** | 中等 | 低 | 低 |
| **包体积** | 较大 | 小 | 无（原生） |
| **适用场景** | 中大型应用 | 中小型应用 | 简单场景 |

---

## 本章小结

本章我们对 React 中的 HTTP 请求与数据获取进行了全面学习：

- **fetch API**：浏览器原生 API，无需安装，支持 GET/POST/PUT/DELETE，用 AbortController 处理超时
- **axios**：功能更强大的 HTTP 库，支持请求/响应拦截器、自动 JSON 转换、请求/响应取消，封装成实例更方便
- **三状态模式**：loading / error / success 覆盖数据请求的完整生命周期，自定义 Hook 封装实现复用
- **TanStack Query**：最强大的数据获取库，缓存管理、预取、乐观更新、离线支持、background refetch，是中大型应用的必备工具

数据获取是前端最核心的能力之一，选择合适的方案能让代码更优雅、性能更优！下一章我们将学习 **Redux Toolkit**——全局状态管理的完整方案！📦