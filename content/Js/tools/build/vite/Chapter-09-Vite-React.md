

+++
title = "第9章 Vite + React 实战"
weight = 90
date = "2026-03-27T17:13:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter-09-Vite-React

# 第9章：Vite + React 实战

> React 和 Vue 是前端框架界的"两大巨头"。如果说 Vue 3 是尤雨溪的精心之作，那 React 就是 Facebook（Meta）出品的"老牌劲旅"。
>
> Vite 对 React 的支持同样出色——极速冷启动、毫秒级 HMR，让 React 开发者也能体验到"丝般顺滑"的开发体验。
>
> 这一章，我们来一场 React + Vite 的"深度游"：从项目创建开始，到 React 18 新特性，再到 React Router、Zustand 状态管理，最后到开发最佳实践。准备好了吗？Let's React! ⚛️

---

## 9.1 React 项目创建

### 9.1.1 使用 Vite React 模板

创建 React 项目的最快方式是使用 Vite 官方模板：

```bash
# 创建项目
pnpm create vite@latest my-react-app -- --template react

# 进入项目目录
cd my-react-app

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

**使用 TypeScript 模板**（推荐）：

```bash
pnpm create vite@latest my-react-app -- --template react-ts
```

### 9.1.2 项目结构解析

一个典型的 React + Vite 项目结构：

```
my-react-app/
├── public/
│   └── vite.svg              # 网站图标
│
├── src/
│   ├── assets/               # 资源目录
│   │   └── react.svg        # React logo
│   │
│   ├── components/           # 组件目录
│   │   ├── Button.jsx
│   │   ├── Header.jsx
│   │   └── Footer.jsx
│   │
│   ├── pages/               # 页面目录
│   │   ├── Home.jsx
│   │   ├── About.jsx
│   │   └── NotFound.jsx
│   │
│   ├── hooks/              # 自定义 Hooks
│   │   ├── useLocalStorage.js
│   │   └── useWindowSize.js
│   │
│   ├── App.jsx             # 根组件
│   ├── App.css             # 根组件样式
│   ├── main.jsx            # 入口文件
│   └── index.css           # 全局样式
│
├── index.html              # 入口 HTML
├── vite.config.js         # Vite 配置
├── package.json           # 项目配置
└── tsconfig.json          # TypeScript 配置（如果用 TS）
```

### 9.1.3 JSX 语法支持

Vite 原生支持 JSX，不需要额外的配置。但理解 JSX 的工作原理很重要：

```jsx
// src/components/HelloWorld.jsx

// JSX = JavaScript XML，是一种语法糖
// 让我们可以在 JavaScript 中写类似 HTML 的代码
// JSX 会被 Babel/Vite 编译成 React.createElement() 调用

// 普通函数组件
function HelloWorld() {
  return (
    <div className="hello-world">
      <h1>Hello, React!</h1>
      <p>欢迎来到 React 的世界</p>
    </div>
  )
}

// 使用箭头函数 + 默认导出
const Greeting = ({ name = 'World' }) => {
  return (
    <div className="greeting">
      <h2>你好，{name}！</h2>
      <p>今天天气不错</p>
    </div>
  )
}

// 导出
export default HelloWorld
export { Greeting }
```

**JSX 规则**：
- 必须有**一个根元素**（或使用 Fragment `<>...</>`）
- 类名用 `className` 而不是 `class`
- 使用 `htmlFor` 而不是 `for`
- 表达式用 `{}` 包裹

---

## 9.2 React 开发配置

### 9.2.1 Fast Refresh 配置

Vite 的 React 插件提供了**Fast Refresh**（快速刷新）功能，让你在修改组件时，组件状态可以保持不变。

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react({
      // 启用 Fast Refresh（默认 true）
      fastRefresh: true,
    }),
  ],
})
```

**Fast Refresh 的工作原理**：
- 修改组件代码 → 只重新渲染该组件
- 组件的 state 保持不变（大多数情况下）
- Hooks 的状态会重新初始化

**注意事项**：
- 如果修改了 Hooks 的签名（比如添加/删除依赖），状态可能会重置
- 组件顶层的 `console.log` 每次都会执行，这是正常的

### 9.2.2 JSX Transform 模式

React 17 引入了新的 JSX Transform，不需要在每个文件里 `import React from 'react'`。

**旧模式（经典模式）**：

```jsx
// 经典模式：每个文件都要 import React
import React from 'react'

function Button() {
  return <button className="btn">点击我</button>
}
```

**新模式（自动模式）**：

```jsx
// 自动模式：不需要 import React
// Vite 会自动注入 JSX 运行时
function Button() {
  return <button className="btn">点击我</button>
}
```

Vite 默认使用**自动模式**，你不需要在每个文件中导入 React：

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react({
      // 使用新的 JSX Transform（自动模式）
      // 替代了旧的 classic 模式
      jsxRuntime: 'automatic',
    }),
  ],
})
```

### 9.2.3 经典 vs 自动 JSX 转换

| 模式 | 需要的 import | JSX 编译结果 | React 版本要求 |
|------|--------------|--------------|----------------|
| classic（已废弃） | `import React from 'react'` | `React.createElement(...)` | 任意版本 |
| automatic（推荐） | 不需要 | 自动导入 JSX 运行时 | React 17+ |

**为什么推荐自动模式**：
- 不需要每个文件都 `import React`
- 代码更简洁
- Tree Shaking 效果更好（不会意外保留未使用的 React）

### 9.2.4 CSS 方案选择

React 项目有多种 CSS 方案可选：

**方案一：普通 CSS + CSS Modules**：

```jsx
// Button.jsx
import './Button.css'

function Button({ children, variant = 'primary' }) {
  return (
    <button className={`btn btn-${variant}`}>
      {children}
    </button>
  )
}
```

```css
/* Button.css */
.btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-secondary {
  background-color: #e5e7eb;
  color: #374151;
}
```

**方案二：CSS-in-JS（Styled Components / Emotion）**：

```jsx
// Button.jsx
import styled from 'styled-components'

const StyledButton = styled.button`
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  background-color: ${props => props.$variant === 'primary' ? '#3b82f6' : '#e5e7eb'};
  color: ${props => props.$variant === 'primary' ? 'white' : '#374151'};
`

function Button({ children, variant = 'primary', ...props }) {
  return (
    <StyledButton $variant={variant} {...props}>
      {children}
    </StyledButton>
  )
}
```

**方案三：Tailwind CSS（原子化 CSS）**：

```jsx
// Button.jsx
function Button({ children, variant = 'primary' }) {
  const baseClasses = 'px-4 py-2 rounded font-semibold transition-all'
  const variantClasses = variant === 'primary' 
    ? 'bg-blue-500 text-white hover:bg-blue-600'
    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
  
  return (
    <button className={`${baseClasses} ${variantClasses}`}>
      {children}
    </button>
  )
}
```

---

## 9.3 React 生态集成

### 9.3.1 React Router 配置（v6/v7）

React Router 是 React 官方推荐的路由库。

**安装**：

```bash
pnpm add react-router-dom
```

**路由配置**：

```jsx
// src/App.jsx
import { BrowserRouter, Routes, Route, Link, useParams, useNavigate, Navigate } from 'react-router-dom'

// 懒加载组件
import { lazy, Suspense } from 'react'

// 懒加载的页面组件（使用 Page 后缀避免与函数组件重名）
const HomePage = lazy(() => import('./pages/Home'))
const AboutPage = lazy(() => import('./pages/About'))
const UserProfilePage = lazy(() => import('./pages/UserProfile'))
const NotFoundPage = lazy(() => import('./pages/NotFound'))

// 加载中组件
function Loading() {
  return <div>加载中...</div>
}

// 首页组件
function Home() {
  return (
    <div>
      <h1>首页</h1>
      <p>欢迎来到首页</p>
    </div>
  )
}

// 关于页组件
function About() {
  return (
    <div>
      <h1>关于</h1>
      <p>这是关于页面</p>
    </div>
  )
}

// 用户详情组件
function UserProfile() {
  const { id } = useParams()  // 获取 URL 参数
  const navigate = useNavigate()  // 编程式导航
  
  return (
    <div>
      <h1>用户 ID：{id}</h1>
      <button onClick={() => navigate('/')}>返回首页</button>
    </div>
  )
}

// 404 组件
function NotFound() {
  return (
    <div>
      <h1>404 - 页面不存在</h1>
      <Link to="/">返回首页</Link>
    </div>
  )
}

// 路由配置
function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: '20px' }}>
        <Link to="/" style={{ marginRight: '15px' }}>首页</Link>
        <Link to="/about" style={{ marginRight: '15px' }}>关于</Link>
        <Link to="/user/1">用户1</Link>
      </nav>
      
      {/* Suspense 用于包裹懒加载组件 */}
      <Suspense fallback={<Loading />}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/user/:id" element={<UserProfilePage />} />
          
          {/* 重定向 */}
          <Route path="/home" element={<Navigate to="/" replace />} />
          
          {/* 404 */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default App
```

**嵌套路由**：

```jsx
// 嵌套路由配置
import { Outlet } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="users" element={<Users />}>
            <Route index element={<UserList />} />
            <Route path=":id" element={<UserDetail />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

// Layout 组件（父路由）
function Layout() {
  return (
    <div>
      <nav>导航</nav>
      {/* Outlet 是子路由的出口 */}
      <Outlet />
      <footer>页脚</footer>
    </div>
  )
}
```

### 9.3.2 Zustand 状态管理

Zustand 是一个轻量级的状态管理库，比 Redux 简单得多。

**安装**：

```bash
pnpm add zustand
```

**创建 Store**：

```javascript
// src/stores/useStore.js
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

// 使用 persist 中间件，数据会保存到 localStorage
const useStore = create(
  persist(
    (set, get) => ({
      // ===== 状态 =====
      bears: 0,
      name: '小明',
      todos: [
        { id: 1, text: '学习 React', done: false },
        { id: 2, text: '学习 Vite', done: false },
      ],
      
      // ===== Actions =====
      increaseBears: () => set((state) => ({ bears: state.bears + 1 })),
      decreaseBears: () => set((state) => ({ bears: state.bears - 1 })),
      resetBears: () => set({ bears: 0 }),
      
      setName: (name) => set({ name }),
      
      addTodo: (text) =>
        set((state) => ({
          todos: [
            ...state.todos,
            { id: Date.now(), text, done: false },
          ],
        })),
      
      toggleTodo: (id) =>
        set((state) => ({
          todos: state.todos.map((todo) =>
            todo.id === id ? { ...todo, done: !todo.done } : todo
          ),
        })),
      
      removeTodo: (id) =>
        set((state) => ({
          todos: state.todos.filter((todo) => todo.id !== id),
        })),
    }),
    {
      name: 'my-app-storage',  // localStorage 的 key
      partialize: (state) => ({ todos: state.todos }),  // 只持久化 todos
    }
  )
)

export default useStore
```

**在组件中使用**：

```jsx
// src/components/TodoApp.jsx
import useStore from '../stores/useStore'

function TodoApp() {
  const { 
    bears, 
    name, 
    todos, 
    increaseBears, 
    decreaseBears,
    addTodo,
    toggleTodo,
    removeTodo,
  } = useStore()
  
  const [inputText, setInputText] = useState('')
  
  const handleAddTodo = () => {
    if (inputText.trim()) {
      addTodo(inputText.trim())
      setInputText('')
    }
  }
  
  return (
    <div className="todo-app">
      <h1>Zustand Todo App</h1>
      
      <div className="bears">
        <p>熊的数量：{bears}</p>
        <button onClick={increaseBears}>增加</button>
        <button onClick={decreaseBears}>减少</button>
      </div>
      
      <div className="todos">
        <h2>待办事项</h2>
        
        <div className="add-todo">
          <input
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAddTodo()}
            placeholder="添加新待办..."
          />
          <button onClick={handleAddTodo}>添加</button>
        </div>
        
        <ul>
          {todos.map((todo) => (
            <li key={todo.id} className={todo.done ? 'done' : ''}>
              <input
                type="checkbox"
                checked={todo.done}
                onChange={() => toggleTodo(todo.id)}
              />
              <span>{todo.text}</span>
              <button onClick={() => removeTodo(todo.id)}>删除</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
```

### 9.3.3 Redux Toolkit

Redux Toolkit（RTK）是 Redux 的官方推荐方式，比传统 Redux 简洁得多。

**安装**：

```bash
pnpm add @reduxjs/toolkit react-redux
```

**配置 Store**：

```javascript
// src/store/index.js
import { configureStore } from '@reduxjs/toolkit'
import counterReducer from './counterSlice'
import todosReducer from './todosSlice'

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    todos: todosReducer,
  },
})
```

**创建 Slice**：

```javascript
// src/store/counterSlice.js
import { createSlice } from '@reduxjs/toolkit'

const counterSlice = createSlice({
  name: 'counter',
  initialState: {
    value: 0,
    step: 1,
  },
  reducers: {
    increment: (state) => {
      state.value += state.step
    },
    decrement: (state) => {
      state.value -= state.step
    },
    setStep: (state, action) => {
      state.step = action.payload
    },
    reset: (state) => {
      state.value = 0
    },
  },
})

export const { increment, decrement, setStep, reset } = counterSlice.actions
export default counterSlice.reducer
```

**在组件中使用**：

```jsx
// src/components/Counter.jsx
import { useSelector, useDispatch } from 'react-redux'
import { increment, decrement, reset, setStep } from '../store/counterSlice'

function Counter() {
  const { value, step } = useSelector((state) => state.counter)
  const dispatch = useDispatch()
  
  return (
    <div className="counter">
      <h2>计数器：{value}</h2>
      <p>步长：{step}</p>
      
      <div className="controls">
        <button onClick={() => dispatch(decrement())}>-</button>
        <button onClick={() => dispatch(increment())}>+</button>
        <button onClick={() => dispatch(reset())}>重置</button>
      </div>
      
      <div className="step-control">
        <label>步长：</label>
        <input
          type="number"
          value={step}
          onChange={(e) => dispatch(setStep(Number(e.target.value)))}
        />
      </div>
    </div>
  )
}
```

### 9.3.4 React Context 与状态管理

React 内置的 Context API 可以用于简单的全局状态共享：

```jsx
// src/context/ThemeContext.jsx
import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext()

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light')
  
  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))
  }
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

```jsx
// src/App.jsx
import { ThemeProvider, useTheme } from './context/ThemeContext'

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()
  
  return (
    <div>
      <p>当前主题：{theme}</p>
      <button onClick={toggleTheme}>切换主题</button>
    </div>
  )
}

function App() {
  return (
    <ThemeProvider>
      <ThemeToggle />
    </ThemeProvider>
  )
}
```

### 9.3.5 React Query / TanStack Query

React Query 是用于管理服务端状态（异步数据）的库。

**安装**：

```bash
pnpm add @tanstack/react-query
```

**配置**：

```jsx
// src/main.jsx
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,  // 5分钟内不重新获取
      gcTime: 1000 * 60 * 10,    // 10分钟内缓存
      retry: 1,                   // 失败重试1次
    },
  },
})

createRoot(document.getElementById('root')).render(
  <QueryClientProvider client={queryClient}>
    <App />
    <ReactQueryDevtools initialIsOpen={false} />
  </QueryClientProvider>
)
```

**使用**：

```jsx
// src/components/TodoList.jsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// 获取数据的函数
async function fetchTodos() {
  const response = await fetch('https://jsonplaceholder.typicode.com/todos?_limit=10')
  if (!response.ok) throw new Error('获取数据失败')
  return response.json()
}

// 添加数据的函数
async function addTodo(todo) {
  const response = await fetch('https://jsonplaceholder.typicode.com/todos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(todo),
  })
  return response.json()
}

function TodoList() {
  const queryClient = useQueryClient()
  
  // 查询数据
  const { data: todos, isPending, isError, error } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })
  
  // 变更数据
  const mutation = useMutation({
    mutationFn: addTodo,
    onSuccess: () => {
      // 成功后刷新数据
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })
  
  const handleAddTodo = () => {
    mutation.mutate({ title: '新待办', completed: false })
  }
  
  if (isPending) return <div>加载中...</div>
  if (isError) return <div>错误：{error.message}</div>
  
  return (
    <div>
      <h1>Todo 列表</h1>
      <button onClick={handleAddTodo} disabled={mutation.isPending}>
        {mutation.isPending ? '添加中...' : '添加待办'}
      </button>
      
      <ul>
        {todos?.map((todo) => (
          <li key={todo.id} className={todo.completed ? 'done' : ''}>
            <input type="checkbox" checked={todo.completed} readOnly />
            <span>{todo.title}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
```

### 9.3.6 SWR（Stale-While-Revalidate）

SWR 是 Vercel 开发的另一个数据获取库，理念和 React Query 类似。

**安装**：

```bash
pnpm add swr
```

**使用**：

```jsx
// src/components/UserProfile.jsx
import useSWR from 'swr'

const fetcher = (url) => fetch(url).then((res) => res.json())

function UserProfile({ userId }) {
  const { data, error, isLoading, mutate } = useSWR(
    `https://jsonplaceholder.typicode.com/users/${userId}`,
    fetcher,
    {
      revalidateOnFocus: false,  // 失焦后不重新验证
      dedupingInterval: 5000,     // 5秒内不重复请求
    }
  )
  
  if (isLoading) return <div>加载中...</div>
  if (error) return <div>加载失败</div>
  
  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.email}</p>
      <button onClick={() => mutate()}>刷新</button>
    </div>
  )
}
```

### 9.3.7 React I18next 国际化

**安装**：

```bash
pnpm add react-i18next i18next
```

**配置**：

```javascript
// src/i18n/index.js
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './locales/en.json'
import zh from './locales/zh.json'

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    zh: { translation: zh },
  },
  lng: 'zh',  // 默认语言
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,  // React 已经处理了 XSS
  },
})

export default i18n
```

```json
// src/i18n/locales/en.json
{
  "hello": "Hello World",
  "welcome": "Welcome to React i18n",
  "count": "You clicked {{count}} times"
}
```

```json
// src/i18n/locales/zh.json
{
  "hello": "你好世界",
  "welcome": "欢迎使用 React i18n",
  "count": "你点击了 {{count}} 次"
}
```

**使用**：

```jsx
// src/components/LanguageSwitcher.jsx
import { useTranslation } from 'react-i18next'

function LanguageSwitcher() {
  const { t, i18n } = useTranslation()
  
  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang)
  }
  
  return (
    <div>
      <h1>{t('hello')}</h1>
      <p>{t('welcome')}</p>
      
      <button onClick={() => changeLanguage('en')}>English</button>
      <button onClick={() => changeLanguage('zh')}>中文</button>
    </div>
  )
}
```

---

## 9.4 React 开发最佳实践

### 9.4.1 Hooks 使用规范

**自定义 Hooks 规范**：

```jsx
// src/hooks/useLocalStorage.js
import { useState, useEffect } from 'react'

// 自定义 Hook：封装 localStorage
function useLocalStorage(key, initialValue) {
  // 从 localStorage 获取初始值
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error('Error reading localStorage:', error)
      return initialValue
    }
  })
  
  // 当值变化时，同步到 localStorage
  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue))
    } catch (error) {
      console.error('Error writing to localStorage:', error)
    }
  }, [key, storedValue])
  
  return [storedValue, setStoredValue]
}

export default useLocalStorage
```

```jsx
// src/hooks/useWindowSize.js
import { useState, useEffect } from 'react'

function useWindowSize() {
  const [windowSize, setWindowSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  })
  
  useEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      })
    }
    
    window.addEventListener('resize', handleResize)
    
    // 清理函数
    return () => window.removeEventListener('resize', handleResize)
  }, [])
  
  return windowSize
}

export default useWindowSize
```

### 9.4.2 组件懒加载

React 18 支持 `lazy` + `Suspense` 实现组件懒加载：

```jsx
// src/App.jsx
import { lazy, Suspense } from 'react'

// 懒加载页面组件
const Home = lazy(() => import('./pages/Home'))
const About = lazy(() => import('./pages/About'))
const Dashboard = lazy(() => import('./pages/Dashboard'))

// 加载中组件
function Loading() {
  return (
    <div className="loading">
      <div className="spinner"></div>
      <p>加载中...</p>
    </div>
  )
}

function App() {
  return (
    <div>
      <Suspense fallback={<Loading />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </Suspense>
    </div>
  )
}
```

### 9.4.3 错误边界处理

错误边界是 React 组件，用于捕获子组件的 JavaScript 错误：

```jsx
// src/components/ErrorBoundary.jsx
import { Component } from 'react'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }
  
  // 捕获错误
  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }
  
  // 记录错误
  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h1>出错了！</h1>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            刷新页面
          </button>
        </div>
      )
    }
    
    return this.props.children
  }
}

export default ErrorBoundary
```

```jsx
// src/App.jsx
function App() {
  return (
    <ErrorBoundary>
      <MyComponent />
    </ErrorBoundary>
  )
}
```

### 9.4.4 TypeScript + React 最佳实践

**组件 Props 类型定义**：

```tsx
// src/components/Button.tsx
import { ButtonHTMLAttributes, ReactNode } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  children: ReactNode
  isLoading?: boolean
}

function Button({
  variant = 'primary',
  size = 'md',
  children,
  isLoading = false,
  disabled,
  className = '',
  ...props
}: ButtonProps) {
  const baseClasses = 'btn'
  const variantClasses = `btn-${variant}`
  const sizeClasses = `btn-${size}`
  
  return (
    <button
      className={`${baseClasses} ${variantClasses} ${sizeClasses} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? '加载中...' : children}
    </button>
  )
}

export default Button
```

**useState 类型推断**：

```tsx
// 自动推断类型
const [count, setCount] = useState(0)  // number
const [name, setName] = useState('')  // string
const [items, setItems] = useState<string[]>([])  // string[]
const [user, setUser] = useState<User | null>(null)  // User | null
const [loading, setLoading] = useState<boolean>(false)  // boolean
```

### 9.4.5 HMR 不生效问题排查

如果 React Fast Refresh 不生效：

1. **确保组件是导出的**：
   ```jsx
   // ✅ 正确
   export default function MyComponent() { }
   
   // ❌ 可能有问题
   function MyComponent() { }
   export default MyComponent
   ```

2. **避免在组件顶层使用 console.log**：
   ```jsx
   // 每次更新都会打印
   console.log('render')
   function MyComponent() {
     return <div>内容</div>
   }
   ```

3. **检查是否有语法错误**：

4. **重启开发服务器**：`pnpm dev --force`

### 9.4.6 React Server Components 了解

React Server Components（RSC）是 React 18+ 的新特性，允许组件在服务器端渲染。

**服务端组件 vs 客户端组件**：

```jsx
// ServerComponent.jsx（服务端组件）
// 默认，所有组件都是服务端组件
// 可以直接访问数据库、文件系统等
async function ServerComponent() {
  // 可以直接使用 async/await
  const data = await fetchData()
  
  return <div>{data}</div>
}
```

```jsx
// ClientComponent.jsx（客户端组件）
'use client'

// 需要 'use client' 指令才能使用 useState、useEffect 等
import { useState } from 'react'

function ClientComponent() {
  const [count, setCount] = useState(0)
  
  return (
    <button onClick={() => setCount(count + 1)}>
      点击了 {count} 次
    </button>
  )
}
```

---

## 9.5 本章小结

### 🎉 本章总结

这一章我们完成了 React + Vite 的深度实战：

1. **React 项目创建**：Vite React 模板、项目结构、JSX 语法

2. **React 开发配置**：Fast Refresh、新 JSX Transform、自动 vs 经典模式、CSS 方案选择

3. **React 生态集成**：React Router v6/v7（动态路由、嵌套路由、懒加载）、Zustand（轻量状态管理）、Redux Toolkit（传统 Redux 升级版）、React Context、React Query/TanStack Query（服务端状态）、SWR（数据获取）、React I18next（国际化）

4. **开发最佳实践**：自定义 Hooks 规范、组件懒加载、错误边界、TypeScript + React 最佳实践、HMR 排查

5. **实战项目**：Todo 应用，涵盖状态管理、CRUD 操作

### 📝 本章练习

1. **创建项目**：用 `pnpm create vite@latest my-react-app -- --template react-ts` 创建一个 TypeScript React 项目

2. **Todo 应用**：实现一个完整的 Todo 应用，包含增删改查功能

3. **路由嵌套**：实现一个用户管理页面，包含用户列表和用户详情

4. **Zustand Store**：把 Todo 应用的状态管理迁移到 Zustand

5. **React Query 实战**：使用 React Query 获取和展示数据

---

> 📌 **预告**：下一章（最后一章）我们将学习 **Vite + TypeScript**，包括 TypeScript 基础、Vite 中的 TypeScript 配置、类型安全开发、高级类型技巧。敬请期待！
