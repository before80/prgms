+++
title = "第11章 useContext与跨组件传值"
weight = 110
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-11 - useContext 与跨层级数据传递

## 11.1 Context 基础

### 11.1.1 Props 层层传递的痛苦：Props Drilling

在第六章我们学过，数据通过 props 从父组件传给子组件。但如果组件嵌套得很深（层级很多），数据就需要一层一层地往下传——这叫 **Props Drilling**（props 层层向下钻）。

Props Drilling 有多痛苦？看看这个例子：

```jsx
// 假设 App 是根组件，DeepChild 是深度为 5 层的组件
// App 有用户信息，想传给 DeepChild

function App() {
  const user = { name: '小明', avatar: '/avatar.jpg', role: 'admin' }
  return <Level1 user={user} />
}

function Level1({ user }) {
  return <Level2 user={user} />
}

function Level2({ user }) {
  return <Level3 user={user} />
}

function Level3({ user }) {
  return <Level4 user={user} />
}

function Level4({ user }) {
  return <Level5 user={user} />
}

function Level5({ user }) {
  // DeepChild 终于拿到了 user，但中间 4 层组件根本不需要 user！
  // 它们只是"中转站"，被迫接收并传递 user
  return <div>{user.name}</div>
}
```

中间那些组件（Level1~Level4）根本不需要 `user`，但因为数据要往下传，它们被迫当"搬运工"。这不仅代码冗余，还会让组件之间的关系变得混乱。

### 11.1.2 Context 的解决思路：跨层级直接传递

**Context（上下文）** 就是用来解决这个问题的！它允许数据从父组件直接传递到任意深度的子组件，**不需要经过中间每一层**。

```jsx
// Context 的思路：
// 数据像"喷泉"一样，从父组件直接往下"浇灌"
// 中间的组件不需要知道这些数据的存在
```

```mermaid
flowchart TD
    A["App（数据源头）\n提供 Theme / User"] --> B["Level1（路过）"]
    B --> C["Level2（路过）"]
    C --> D["Level3（路过）"]
    D --> E["DeepChild（直接拿到数据）"]

    subgraph "Props Drilling 模式"
        A -.->|"props.user| user"| B
        B -.->|"props.user| user"| C
        C -.->|"props.user| user"| D
        D -.->|"props.user| user"| E
    end

    subgraph "Context 模式"
        A --"ThemeContext.Provider\nUserContext.Provider"--> B
        B --"直接路过，不需要传"| C
        C --"直接路过，不需要传"| D
        D --"直接路过，不需要传"| E
    end
```

**使用 Context 的三步走：**
1. 用 `createContext()` 创建一个"数据发射站"
2. 用 `Provider` 在父组件中包裹子树，把数据"发射"出去
3. 在需要数据的子组件里，用 `useContext()` "接收"数据

对比一下：Props Drilling 就像老式电话，需要一级一级转接；而 Context 就是对讲机，父组件直接喊话，任意深度的子组件都能听到！📻


---

## 11.2 createContext 与 useContext

### 11.2.1 createContext 创建上下文

在数据共享之前，需要先用 `createContext` 创建一个"数据管道"。可以把它想象成**一根自来水管**——`createContext` 是买水管，`Provider` 是打开水龙头，`useContext` 是把水接到自己家。三步缺一不可。

`createContext` 的参数是**默认值**——当没有任何 Provider 包裹组件时，就会使用这个默认值。

```jsx
import { createContext } from 'react'

// createContext() 创建一个 Context 对象
// 参数是默认值：当没有 <Provider> 包裹时，组件会使用这个默认值
const ThemeContext = createContext({
  theme: 'light',
  toggleTheme: () => {}
})

// 创建用户上下文
const UserContext = createContext(null)

// 导出供其他组件使用
export { ThemeContext, UserContext }
```

### 11.2.2 Provider 包裹：传递数据

**Provider（提供者）** 是 Context 的"发射塔"——用它包裹子组件，子组件就能收到 Context 提供的数据。

```jsx
import { useState } from 'react'
import { ThemeContext, UserContext } from './contexts'

function App() {
  const [theme, setTheme] = useState('light')
  const user = { name: '小明', avatar: '/avatar.jpg' }

  function toggleTheme() {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  return (
    // 用 Provider 包裹子树
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <UserContext.Provider value={user}>
        {/* 所有的子组件都能访问 ThemeContext 和 UserContext */}
        <div className={`app ${theme}`}>
          <Header />
          <Content />
          <Footer />
        </div>
      </UserContext.Provider>
    </ThemeContext.Provider>
  )
}
```

### 11.2.3 useContext 读取数据

子组件用 `useContext` 读取 Context 提供的数据：

```jsx
import { useContext } from 'react'
import { ThemeContext, UserContext } from './contexts'

// 读取主题
function Header() {
  const { theme, toggleTheme } = useContext(ThemeContext)
  // 读取用户
  const user = useContext(UserContext)

  return (
    <header className={`header ${theme}`}>
      <img src={user.avatar} alt={user.name} />
      <button onClick={toggleTheme}>
        切换到{theme === 'light' ? '深色' : '浅色'}模式
      </button>
    </header>
  )
}

// 即使是深层嵌套的组件，也能直接拿到数据
function DeepButton() {
  const { theme, toggleTheme } = useContext(ThemeContext)

  return <button className={`btn ${theme}`}>{theme}</button>
}
```

---

## 11.3 Context 实战应用场景

### 11.3.1 主题切换：dark/light mode

主题切换是 Context 最经典的应用场景：

```jsx
// theme/ThemeContext.js
import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext()

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light')

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  const value = {
    theme,
    isDark: theme === 'dark',
    toggleTheme
  }

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  )
}

// 自定义 Hook：方便子组件读取
function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme 必须在 ThemeProvider 内使用')
  }
  return context
}

export { ThemeContext, ThemeProvider, useTheme }
```

```jsx
// App.jsx
import { ThemeProvider } from './theme/ThemeContext'
import Header from './components/Header'
import Content from './components/Content'

function App() {
  return (
    <ThemeProvider>
      <div className="app">
        <Header />
        <Content />
      </div>
    </ThemeProvider>
  )
}

// Header.jsx
import { useTheme } from '../theme/ThemeContext'

function Header() {
  const { theme, isDark, toggleTheme } = useTheme()

  return (
    <header className={`header ${theme}`}>
      <h1>我的应用</h1>
      <button onClick={toggleTheme}>
        {isDark ? '🌙 深色' : '☀️ 浅色'}
      </button>
    </header>
  )
}
```

### 11.3.2 用户信息全局状态

```jsx
// auth/AuthContext.js
import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)

  const login = (userData, authToken) => {
    setUser(userData)
    setToken(authToken)
    localStorage.setItem('token', authToken)
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
  }

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth 必须在 AuthProvider 内使用')
  }
  return context
}

export { AuthContext, AuthProvider, useAuth }
```

```jsx
// 任意组件都可以直接获取用户信息
function ProfileMenu() {
  const { user, isAuthenticated, logout } = useAuth()

  if (!isAuthenticated) {
    return <a href="/login">登录</a>
  }

  return (
    <div>
      <img src={user.avatar} alt={user.name} />
      <span>{user.name}</span>
      <button onClick={logout}>退出</button>
    </div>
  )
}
```

### 11.3.3 国际化语言切换

```jsx
// i18n/I18nContext.js
import { createContext, useContext, useState } from 'react'

const translations = {
  zh: {
    greeting: '你好',
    welcome: '欢迎来到我的应用',
    logout: '退出'
  },
  en: {
    greeting: 'Hello',
    welcome: 'Welcome to my app',
    logout: 'Logout'
  }
}

const I18nContext = createContext()

function I18nProvider({ children }) {
  const [locale, setLocale] = useState('zh')

  const t = (key) => {
    return translations[locale][key] || key
  }

  return (
    <I18nContext.Provider value={{ locale, setLocale, t }}>
      {children}
    </I18nContext.Provider>
  )
}

function useI18n() {
  return useContext(I18nContext)
}

export { I18nProvider, useI18n }
```

### 11.3.4 全局配置参数

```jsx
// config/ConfigContext.js
import { createContext, useContext, useState } from 'react'

const ConfigContext = createContext()

function ConfigProvider({ children }) {
  const [config, setConfig] = useState({
    apiBaseUrl: 'https://api.example.com',
    uploadMaxSize: 10 * 1024 * 1024,  // 10MB
    enableAnalytics: true,
    maintenanceMode: false
  })

  const updateConfig = (updates) => {
    setConfig(prev => ({ ...prev, ...updates }))
  }

  return (
    <ConfigContext.Provider value={{ config, updateConfig }}>
      {children}
    </ConfigContext.Provider>
  )
}

function useConfig() {
  return useContext(ConfigContext)
}

export { ConfigProvider, useConfig }
```

---

## 11.4 Context 性能优化

> **先别急着优化！** Context 的性能问题只有在特定场景下才会成为真正的瓶颈。在学习优化技巧之前，先问问自己：真的需要优化吗？用 React DevTools Profiler 确认问题再动手。

### 11.4.1 Context 每次更新导致所有消费者重渲染

Context 的一个重要性能问题是：**当 Provider 的 value 变化时，所有消费这个 Context 的组件都会重新渲染**。

```jsx
function App() {
  const [theme, setTheme] = useState('light')
  const [user, setUser] = useState({ name: '小明' })

  // ❌ 问题：每次 App 重新渲染，这个对象都是新引用！
  // 导致所有消费 ThemeContext 的组件都重新渲染
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <UserContext.Provider value={{ user, setUser }}>
        <div>{/* 内容 */}</div>
      </UserContext.Provider>
    </ThemeContext.Provider>
  )
}
```

### 11.4.2 拆分 Context：按更新频率分离

**解决方案一：把 Context 按更新频率拆分成多个**。因为 Context 的 value 每次更新，所有消费者都会重新渲染，所以最好把**频繁变化的值**和**不频繁变化的值**放在不同的 Context 里。

```jsx
// ❌ 一个 Context 包含所有值，一个变化全都重渲染
const AppContext = createContext({
  theme: 'light',
  user: null,
  notifications: [],
  cartItems: []
})

// ✅ 拆成多个 Context，变化时只影响需要的组件
const ThemeContext = createContext()
const UserContext = createContext()
const NotificationContext = createContext()
const CartContext = createContext()
```

### 11.4.3 useMemo 优化 Context 值

用 `useMemo` 缓存 Context 的 value，避免不必要的引用变化：

```jsx
import { useMemo } from 'react'

function App() {
  const [theme, setTheme] = useState('light')
  const [user, setUser] = useState({ name: '小明' })

  // 用 useMemo 缓存 value，只有当 theme 或 setTheme 变化时才重新创建
  const themeValue = useMemo(() => ({
    theme,
    setTheme
  }), [theme, setTheme])

  // user 没变化时，这个 value 不会重新创建
  const userValue = useMemo(() => ({
    user,
    setUser
  }), [user, setUser])

  return (
    <ThemeContext.Provider value={themeValue}>
      <UserContext.Provider value={userValue}>
        <div>{/* 内容 */}</div>
      </UserContext.Provider>
    </ThemeContext.Provider>
  )
}
```

### 11.4.4 memo + useCallback + Context 组合优化

```jsx
import { memo, useCallback, useMemo, useState, useContext } from 'react'

// 子组件用 memo 包裹，只有 props 真正变化时才重新渲染
// 注意：这个子组件通过 props 接收回调，而不是直接从 Context 读
const ThemeToggle = memo(function ThemeToggle({ theme, onToggle }) {
  console.log('ThemeToggle 渲染了')  // 方便观察是否重渲染
  return <button onClick={onToggle}>{theme}</button>
})

// 父组件：用 useCallback 稳定回调函数
function Parent() {
  const [count, setCount] = useState(0)
  const [theme, setTheme] = useState('light')

  // 用 useCallback 保证函数引用稳定
  const handleToggle = useCallback(() => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }, [])

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      {/* 即使 count 变化导致 Parent 重渲染，ThemeToggle 也不会重渲染 */}
      {/* 因为 theme 没变，handleToggle 引用也没变 */}
      <ThemeToggle theme={theme} onToggle={handleToggle} />
    </div>
  )
}
```

> ⚠️ **这个例子的教训**：如果子组件从 Context 读取数据（比如 `useContext(ThemeContext)`），那你用不用 `memo` + `useCallback` 都无所谓——Context value 变化了，子组件照样重渲染。上面例子的 `ThemeToggle` 是**通过 props 接收** `theme` 和 `onToggle`，这样 `memo` 才能真正发挥作用：只有当这两个 prop 真正变化时才重渲染。

---

## 本章小结

本章我们学习了 React 的"跨组件数据传递神器"——Context：

- **Props Drilling 问题**：深层嵌套的组件需要数据时，数据要经过每一层中间组件，造成代码冗余和维护困难
- **Context 的解决方案**：数据从 Provider 直接传递到消费者，无需经过中间层级
- **createContext + useContext**：createContext 创建上下文，Provider 包裹子树并传递数据，子组件用 useContext 读取
- **实战场景**：主题切换（dark/light mode）、用户信息全局状态、国际化语言、全局配置参数
- **性能优化**：Context value 变化时所有消费者都会重新渲染，解决方法包括拆分 Context、useMemo 缓存 value、memo + useCallback 配合使用

Context 是 React 状态管理的重要工具，适合"真正需要全局共享"的数据。对于复杂应用的状态管理，还需要结合 useReducer、Zustand、Redux 等方案。下一章我们将学习 **useReducer**——复杂状态逻辑的克星！🧠