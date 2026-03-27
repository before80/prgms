+++
title = "第21章 Zustand轻量级状态管理"
weight = 210
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-21 - Zustand——轻量级状态管理

## 21.1 Zustand 基础

### 21.1.1 安装与 store 创建

**Zustand** 是一个超轻量的状态管理库，比 Redux 简洁得多，但功能同样强大。

什么场景需要它？想象一下：你的应用有"主题切换"功能，用户在设置页改了深色模式，头部组件、侧边栏组件、底部组件...十几个组件都要响应这个变化。用 Context 要层层嵌套，用 Redux 又太重。**Zustand 就是来解决这种"中等规模"状态共享问题的**——比 Context 强大（细粒度订阅），比 Redux 简单（不用写模板代码）。

```bash
npm install zustand
```

```javascript
import { create } from 'zustand'

// 创建一个 store
const useStore = create((set) => ({
  // 状态
  count: 0,
  user: null,

  // 方法（更新状态）
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  setUser: (user) => set({ user }),
  reset: () => set({ count: 0, user: null })
}))
```

### 21.1.2 读取、写入状态

```javascript
// 在组件中读取和写入
function Counter() {
  // 选择器：只订阅需要的部分
  const count = useStore(state => state.count)
  const increment = useStore(state => state.increment)

  return (
    <div>
      <p>计数：{count}</p>
      <button onClick={increment}>+1</button>
    </div>
  )
}

// 选择多个状态
function UserPanel() {
  const { user, setUser, reset } = useStore(state => ({
    user: state.user,
    setUser: state.setUser,
    reset: state.reset
  }))

  return (
    <div>
      {user ? <p>用户：{user.name}</p> : <p>未登录</p>}
      <button onClick={() => setUser({ name: '小明' })}>登录</button>
      <button onClick={reset}>重置</button>
    </div>
  )
}
```

### 21.1.3 实战：计数器 store

```javascript
// store/counterStore.js
import { create } from 'zustand'

export const useCounterStore = create((set, get) => ({
  count: 0,

  increment: () => set(state => ({ count: state.count + 1 })),
  decrement: () => set(state => ({ count: state.count - 1 })),
  incrementBy: (amount) => set(state => ({ count: state.count + amount })),
  reset: () => set({ count: 0 }),

  // 访问其他状态
  double: () => set(state => ({ count: state.count * 2 })),

  // get() 可以获取当前状态
  incrementIfOdd: () => {
    const { count, increment } = get()
    if (count % 2 !== 0) {
      increment()
    }
  }
}))
```

---

## 21.2 持久化与中间件

### 21.2.1 persist 中间件：localStorage 持久化

```javascript
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

const useStore = create(
  persist(
    (set) => ({
      user: null,
      theme: 'light',
      setUser: (user) => set({ user }),
      setTheme: (theme) => set({ theme })
    }),
    {
      name: 'my-app-storage',  // localStorage 的 key，保存到 localStorage 时的键名
      // 推荐使用 createJSONStorage 包装 storage，它会自动处理 JSON 序列化/反序列化
      storage: createJSONStorage(() => localStorage),

      // partialize：选择性持久化——只保存 state 中的部分字段
      // 如果不写 partialize，默认保存整个 state
      // 场景：user 等敏感信息不想存本地，只存 theme 设置
      partialize: (state) => ({
        theme: state.theme  // 只持久化 theme 字段，user 字段不会被保存
      })
    }
  )
)
```

> 💡 如果想用 sessionStorage，只需要把 `localStorage` 换成 `sessionStorage` 即可：`createJSONStorage(() => sessionStorage)`。

### 21.2.2 devtools 中间件：Zustand DevTools 集成

Zustand 提供了自己的 DevTools 集成，可以可视化每次状态变化的前因后果，体验和 Redux DevTools 类似！只需要加一个中间件：

```javascript
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

const useStore = create(
  devtools(
    (set) => ({
      count: 0,
      increment: () => set(state => ({ count: state.count + 1 }))
    }),
    {
      name: 'my-store',                            // DevTools 中显示的 store 名称
      enabled: process.env.NODE_ENV === 'development'  // 仅开发环境开启
    }
  )
)
```

### 21.2.3 自定义中间件

```javascript
import { create } from 'zustand'

// 自定义日志中间件
const loggerMiddleware = (config) => (set, get, api) =>
  config(
    (...args) => {
      console.log('应用状态前:', get())
      set(...args)
      console.log('应用状态后:', get())
    },
    get,
    api
  )

const useStore = create(
  loggerMiddleware((set) => ({
    count: 0,
    increment: () => set(state => ({ count: state.count + 1 }))
  }))
)
```

---

## 21.3 Zustand vs Redux vs Context

### 21.3.1 复杂度对比

| 维度 | Context | Redux Toolkit | Zustand |
|------|--------|--------------|---------|
| **学习曲线** | 低 | 中高 | 低 |
| **代码量** | 少 | 多 | 少 |
| **配置量** | 无 | 需要配置 store、provider | 无 |
| **DevTools** | 无 | 官方支持 | 官方支持 |

### 21.3.2 开发体验对比

```javascript
// Zustand：极其简洁
const useStore = create((set) => ({
  count: 0,
  increment: () => set(state => ({ count: state.count + 1 }))
}))

// Redux Toolkit：稍多一些模板代码
const counterSlice = createSlice({
  name: 'counter',
  initialState: { count: 0 },
  reducers: {
    increment: (state) => { state.count += 1 }
  }
})

// Context：每次都要定义 Provider
const CounterContext = createContext(null)
function CounterProvider({ children }) {
  const [count, setCount] = useState(0)
  return (
    <CounterContext.Provider value={{ count, setCount }}>
      {children}
    </CounterContext.Provider>
  )
}
```

### 21.3.3 性能对比

| 场景 | Context | Redux Toolkit | Zustand |
|------|---------|--------------|---------|
| **选择器性能** | 需要手动优化 | 有优化工具 | 原生支持细粒度订阅 |
| **组件重渲染** | 任意 value 变化都重渲染 | 可优化 | 只重渲染订阅的组件 |
| **中间件** | 无 | 完整中间件体系 | 有但不完整 |

### 21.3.4 选型建议：何时用哪个

- **简单场景**（2-3 个组件共享状态）：Context 足够
- **中型项目**（需要 DevTools、中间件、异步 thunk）：Redux Toolkit
- **轻量需求**（需要比 Context 更细的粒度控制）：Zustand
- **大型项目**（需要完整的工程化能力）：Redux Toolkit

---

## 本章小结

本章我们学习了 **Zustand**——轻量级状态管理的利器：

- **store 创建**：`create((set, get) => ({ state, actions }))` 简洁明了
- **读取写入**：用选择器 `state => state.xxx` 只订阅需要的状态
- **持久化**：`persist` 中间件让状态自动保存到 localStorage
- **中间件**：devtools、persist、自定义中间件
- **对比**：Zustand 比 Redux 更简洁，比 Context 更强大，适合中型项目

Zustand 是 React 状态管理库中的"瑞士军刀"——小巧、强大、用起来爽！下一章我们将学习 **TypeScript 与 React**——让代码更安全的秘密武器！🔒