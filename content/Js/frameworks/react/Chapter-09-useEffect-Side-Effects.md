+++
title = "第9章 useEffect与副作用"
weight = 90
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-09 - useEffect——副作用的正确打开方式

## 9.1 useEffect 基础

> 如果把 React 组件比作一个"加工厂"，那 **useEffect** 就是这个加工厂的"生产许可证"——它告诉 React："除了正常生产产品（渲染 UI）之外，我还需要做一些别的事情，比如：采购原材料（请求数据）、处理废水废气（清理订阅）、和外面的世界打交道（操作 DOM、播放音乐、记录日志）。" useEffect 让函数组件拥有了"和外界互动"的能力。

### 9.1.1 useEffect 的基本概念：副作用的容器

**副作用（Side Effect）**是什么？简单说就是：**除了返回值之外，对外部环境产生的影响**。

纯函数：`y = f(x)` — 相同的输入，永远得到相同的输出，不产生任何副作用。

有副作用的函数：修改全局变量、发送网络请求、操作 DOM、设置定时器、订阅事件、打印日志……

```jsx
import { useEffect } from 'react'

function UserProfile({ userId }) {
  // useEffect：处理副作用
  // 第一个参数：副作用要执行的函数
  // 第二个参数：依赖数组
  useEffect(() => {
    // 这个函数里可以做任何"有副作用"的事情
    console.log('开始请求用户数据，userId =', userId)
    document.title = `加载中...`  // 修改页面标题（副作用）

    // 例如发送网络请求
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        console.log('用户数据获取成功：', data)
      })

  }, [userId])  // 依赖数组：userId 变化时重新执行

  return <div>用户资料页面</div>
}
```

> 📝 useEffect 就是在告诉 React："我有一段代码，它不只是用来计算 UI 的，它还会做一些其他事情。这段代码在什么时候运行，由依赖数组决定。"

### 9.1.2 没有依赖数组：每次渲染都执行

如果不写依赖数组，`useEffect` 的函数会在**每次渲染后**都执行一次。

```jsx
import { useState, useEffect } from 'react'

function LoggingComponent() {
  const [count, setCount] = useState(0)

  // ⚠️ 注意：没有依赖数组，每次渲染都会执行（包括首次渲染和更新渲染）
  useEffect(() => {
    console.log('组件渲染了，当前 count =', count)
    // 每次 count 变化，都会触发这条日志
  })

  return (
    <button onClick={() => setCount(count + 1)}>
      点我 {count}
    </button>
  )
}

// 打印顺序：
// 初始渲染：组件渲染了，当前 count = 0
// 点击一次：组件渲染了，当前 count = 1
// 点击两次：组件渲染了，当前 count = 2
```

### 9.1.3 空依赖数组：`[]` 只在首次渲染后执行一次

空数组 `[]` 意味着"这个 effect 不依赖任何状态，初始化一次就够了"。

```jsx
function Analytics() {
  useEffect(() => {
    // ✅ 只在组件首次挂载时执行一次（类似 componentDidMount）
    console.log('页面访问了！')
    // 通常在这里：发送访问统计、设置页面标题等一次性的初始化工作
    document.title = '欢迎来到我的网站'

    // 如果 useEffect 返回一个函数，那就是"清理函数"
    return () => {
      console.log('组件卸载了，清理工作')
    }
  }, [])  // 空数组：只在首次渲染后执行

  return <div>页面内容</div>
}
```

### 9.1.4 指定依赖：`[dep1, dep2]` 在依赖变化时执行

当依赖数组里有值时，useEffect 会在**初始渲染执行一次**，之后每当依赖值变化时**重新执行**。

```jsx
function SearchResults({ query }) {
  useEffect(() => {
    console.log('搜索词变了，执行搜索：', query)
    // 当 query 变化时，重新发起搜索请求

    // 模拟搜索请求
    const timer = setTimeout(() => {
      console.log(`搜索"${query}"的结果已加载`)
    }, 500)

    // 返回清理函数：清除上一个定时器，避免请求重叠
    return () => clearTimeout(timer)
  }, [query])  // query 变化时重新执行

  return <div>搜索结果页面</div>
}

// 使用
function App() {
  const [query, setQuery] = useState('')

  return (
    <div>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <SearchResults query={query} />
    </div>
  )
}
```

---

## 9.2 依赖数组的正确使用

### 9.2.1 依赖数组的三大规则

**规则一：依赖数组里的值，必须是"在 useEffect 里用到的所有外部值"**

```jsx
function Search({ keyword, category }) {
  useEffect(() => {
    // 在这里用了 keyword 和 category
    fetchResults(keyword, category)
  }, [keyword, category])  // ✅ 两个都加进去

  // ❌ 错误：漏了 category
  // useEffect(() => { fetchResults(keyword, category) }, [keyword])
}
```

**规则二：依赖数组里的值，必须是稳定的（不应该在渲染中创建新引用）**

```jsx
function BadExample() {
  const [items, setItems] = useState([])

  // ❌ 错误：没有依赖数组（或依赖不对），在 effect 里调用 setState
  // 效果：每次渲染后执行 effect → 调用 setItems → 触发新渲染 → 无限循环！
  useEffect(() => {
    setItems([...items, { id: 1, name: '新物品' }])  // setState 在 effect 里！
  })  // 没有依赖数组，每次渲染都执行 → 无限循环！

  return <button onClick={() => setItems(items => [...items, { id: 1, name: '新物品' }])}>添加</button>
}

// ✅ 正确：用空数组，只在首次渲染执行一次
function GoodExample() {
  const [items, setItems] = useState([])

  useEffect(() => {
    // 初始化逻辑，只执行一次
    console.log('初始化完成')
  }, [])  // ✅ 空数组：真的不依赖任何东西

  return <button onClick={() => setItems(items => [...items, { id: 1, name: '新物品' }])}>添加</button>
}
```

**规则三：如果 effect 确实不依赖任何东西，用空数组**

### 9.2.2 ESLint exhaustive-deps 规则的作用

ESLint 的 `react-hooks/exhaustive-deps` 规则会**强制检查你的 useEffect 依赖是否完整**。它能帮你发现：

```jsx
function Component({ userId }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(false)

  // ❌ ESLint 会警告：缺少依赖 'userId'
  useEffect(() => {
    setLoading(true)
    fetchUser(userId).then(data => {
      setUser(data)
      setLoading(false)
    })
  }, [])  // ❌ 警告：userId 在 effect 中使用，但没有在依赖数组中！

  // ✅ 修复：加上 userId
  useEffect(() => {
    setLoading(true)
    fetchUser(userId).then(data => {
      setUser(data)
      setLoading(false)
    })
  }, [userId])
}
```

### 9.2.3 常见错误：忘记添加依赖导致 bug

**场景一：闭包陷阱——定时器里的旧数据**

定时器回调函数是一个闭包，它"记住"的是首次渲染时的 `count` 值。如果依赖数组为空，effect 永不更新，闭包里的 `count` 就永远是初始值。

```jsx
function Counter() {
  const [count, setCount] = useState(0)

  // ❌ 错误：setInterval 的回调里 count 永远是 0
  useEffect(() => {
    const timer = setInterval(() => {
      // 这里的 count 是首次渲染时的值，永远是 0
      setCount(count + 1)  // count 永远是 0，所以每次都是 setCount(1)
    }, 1000)
  }, [])  // 空数组，effect 永不更新

  // ✅ 正确：用函数式更新，或者把 count 加到依赖数组
  useEffect(() => {
    const timer = setInterval(() => {
      setCount(prev => prev + 1)  // 用函数式更新，不依赖外部变量
    }, 1000)
    return () => clearInterval(timer)
  }, [])
}
```

**场景二：忘记清理订阅——内存泄漏的元凶**

如果 effect 创建了某种"连接"（订阅、定时器、WebSocket等），组件卸载时没有断开这个连接，就会导致内存泄漏。举个例子：

```jsx
function ChatRoom({ roomId }) {
  useEffect(() => {
    // ❌ 错误：没有清理订阅
    const connection = createConnection(roomId)
    connection.connect()  // 建立连接

    // 如果 roomId 变了，这个连接没断开，新的又建立了
    // 造成连接泄漏！
  }, [roomId])

  // ✅ 正确：返回清理函数
  useEffect(() => {
    const connection = createConnection(roomId)
    connection.connect()

    return () => {
      connection.disconnect()  // 清理：断开旧连接
    }
  }, [roomId])
}
```

### 9.2.4 依赖数组常见误解：空数组不代表"只执行一次"

空数组 `[]` 确实只在首次渲染后执行一次，但要注意：
- **组件卸载时**会执行清理函数
- **组件重新挂载时**会再次执行

```jsx
function Example() {
  useEffect(() => {
    console.log('Effect 执行')
    return () => console.log('清理函数执行')
  }, [])

  return <div>示例</div>
}

// 初始渲染：Effect 执行
// 卸载（路由切换等）：清理函数执行
// 重新挂载：Effect 再次执行
```

---

## 9.3 清理副作用

### 9.3.1 为什么需要清理？取消订阅、清除定时器

很多副作用在完成后需要**清理**，否则会造成资源泄漏：

- **定时器**：`setInterval` / `setTimeout` → 用 `clearInterval` / `clearTimeout` 清理
- **事件监听**：`addEventListener` → 用 `removeEventListener` 清理
- **WebSocket 连接**：`connection.connect()` → 用 `connection.disconnect()` 清理
- **订阅**：`subscribe(callback)` → 用 `unsubscribe()` 清理

### 9.3.2 清理函数的执行时机：下次 effect 执行前 + 卸载时

useEffect 的清理函数在两个时机执行：

1. **下次 effect 执行之前**（在同一个 effect 重新运行之前）
2. **组件卸载时**

```jsx
function Timer() {
  useEffect(() => {
    console.log('设置定时器')
    const timer = setInterval(() => {
      console.log('定时器 tick')
    }, 1000)

    // 清理函数
    return () => {
      console.log('清理定时器')
      clearInterval(timer)
    }
  }, [])

  return <div>计时器组件</div>
}

// 时机分析：
// 1. 初始挂载：打印 "设置定时器"
// 2. 每秒打印一次："定时器 tick"
// 3. 卸载时：打印 "清理定时器"，定时器停止
```

### 9.3.3 常见的清理场景：定时器、事件监听、WebSocket、AbortController

**定时器清理：**

```jsx
function AutoSave() {
  useEffect(() => {
    const timer = setInterval(() => {
      saveData()
    }, 5000)

    // 清理：组件卸载时清除定时器
    return () => clearInterval(timer)
  }, [])

  return <div>自动保存组件</div>
}
```

**事件监听清理：**

```jsx
function WindowSize() {
  const [width, setWidth] = useState(window.innerWidth)

  useEffect(() => {
    function handleResize() {
      setWidth(window.innerWidth)
    }

    window.addEventListener('resize', handleResize)

    // 清理：移除事件监听
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return <div>窗口宽度：{width}px</div>
}
```

**AbortController 清理（网络请求）：**

```jsx
import { useState, useEffect } from 'react'

function UserProfile({ userId }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    // AbortController 可以取消正在进行的请求
    const controller = new AbortController()

    async function fetchUser() {
      try {
        const res = await fetch(`/api/users/${userId}`, {
          signal: controller.signal  // 把 signal 传给 fetch
        })
        const data = await res.json()
        setUser(data)
      } catch (err) {
        if (err.name === 'AbortError') {
          console.log('请求被取消了')
        } else {
          console.error('请求失败', err)
        }
      }
    }

    fetchUser()

    // 清理：取消请求
    return () => controller.abort()
  }, [userId])

  return <div>{user ? user.name : '加载中...'}</div>
}
```

### 9.3.4 React 19 中的 ref 清理改进

React 19 改进了 ref 的清理机制——现在可以把清理函数作为 ref callback 的返回值：

```jsx
// React 18 及之前：ref callback 不能返回清理函数
<input
  ref={node => {
    console.log('挂载了')
    // 不能返回清理函数！
  }}
/>

// React 19：ref callback 可以返回清理函数
<input
  ref={node => {
    console.log('挂载了')
    // 返回清理函数
    return () => console.log('卸载了')
  }}
/>
```

---

## 9.4 防止无限循环

### 9.4.1 useEffect 内部 setState 导致无限循环

这是最常见的 useEffect 错误之一：

```jsx
import { useState, useEffect } from 'react'

function BadComponent({ userId }) {
  const [user, setUser] = useState(null)

  // ❌ 错误：在 effect 里调用 setState，但没有加依赖
  // 导致 effect 每次执行都调用 setState，触发重新渲染，重新渲染又触发 effect……无限循环！
  useEffect(() => {
    fetchUser(userId).then(setUser)  // setUser 触发重新渲染
  })  // 没有依赖数组，或者依赖不对 → 无限循环！

  // ✅ 正确：加上正确的依赖
  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId])  // userId 变化才重新执行
}
```

### 9.4.2 网络请求放在 useEffect 中的正确姿势

```jsx
function UserList({ search }) {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false  // 防止请求完成后组件已卸载的情况

    async function load() {
      setLoading(true)
      setError(null)

      try {
        const data = await searchUsers(search)
        // 只有组件还在挂载时才更新 state
        if (!cancelled) {
          setUsers(data)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message)
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    load()

    // 清理函数：组件卸载或 search 变化时执行
    return () => {
      cancelled = true  // 标记"请求作废"
    }
  }, [search])

  if (loading) return <div>加载中...</div>
  if (error) return <div>错误：{error}</div>

  return (
    <ul>
      {users.map(u => <li key={u.id}>{u.name}</li>)}
    </ul>
  )
}
```

### 9.4.3 依赖数组的正确设置方法

**判断依赖的法则**：在 useEffect 内部使用的所有变量，都应该出现在依赖数组里。

```jsx
function Example({ userId, enabled }) {
  const [data, setData] = useState(null)

  useEffect(() => {
    if (!enabled) return  // enabled 为 false 时不执行

    async function fetchData() {
      const result = await api.getData(userId)
      setData(result)
    }

    fetchData()
  }, [userId, enabled])  // ✅ userId 和 enabled 都用了，都加进来
}
```

### 9.4.4 useEffect 中的 async/await：常见陷阱与解决方案

**陷阱一：useEffect 不能直接是 async 函数**

```jsx
// ❌ 错误：useEffect 不能是 async 函数
useEffect(async () => {
  const data = await fetchData()
  setData(data)
}, [])

// ✅ 正确：在 useEffect 内部定义 async 函数
useEffect(() => {
  async function load() {
    const data = await fetchData()
    setData(data)
  }
  load()
}, [])
```

**陷阱二：async 函数返回的是 Promise，不能当清理函数**

```jsx
// ❌ 错误：清理函数不能是 async
useEffect(() => {
  async function load() {
    const data = await fetchData()
    setData(data)
  }
  load()

  return async () => {
    // ❌ 这不是正确的清理函数！async 函数返回 Promise
    await cancelRequest()
  }
}, [])

// ✅ 正确：清理函数应该是同步的
useEffect(() => {
  let cancelled = false

  async function load() {
    const data = await fetchData()
    if (!cancelled) setData(data)
  }
  load()

  return () => {
    cancelled = true  // ✅ 同步的清理
  }
}, [])
```

---

## 9.5 useEffect 实战：数据获取三状态

### 9.5.1 三个状态的设计：isLoading / error / data

数据请求有三种典型状态：**加载中（Loading）**、**错误（Error）**、**成功（Data）**。合理管理这三种状态，能让你的应用体验流畅。

```jsx
// 三状态模型
const [data, setData] = useState(null)        // 数据
const [loading, setLoading] = useState(false)  // 加载中
const [error, setError] = useState(null)       // 错误
```

### 9.5.2 初始状态与加载状态的处理

```jsx
function DataFetcher({ url }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false

    async function fetchData() {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch(url)
        if (!response.ok) {
          throw new Error(`HTTP 错误！状态码：${response.status}`)
        }
        const result = await response.json()

        if (!cancelled) {
          setData(result)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message)
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    fetchData()

    return () => {
      cancelled = true
    }
  }, [url])

  // 渲染分支
  if (loading) {
    return <div className="loading">加载中...</div>
  }

  if (error) {
    return <div className="error">请求失败：{error}</div>
  }

  if (!data) {
    return null  // 没有数据且没有错误，显示空白
  }

  return (
    <div className="data">
      {/* 渲染数据 */}
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
```

### 9.5.3 错误处理：try-catch 与 error 状态

```jsx
// 常见错误类型和对应的处理
async function fetchData() {
  try {
    const res = await fetch(url)

    // 网络错误（fetch 本身抛出的）
    if (!res.ok) {
      // HTTP 错误（如 404、500）
      throw new Error(`请求失败：${res.status} ${res.statusText}`)
    }

    const data = await res.json()
    setData(data)

  } catch (err) {
    if (err.name === 'AbortError') {
      // 请求被取消了，不显示错误（组件已卸载）
      console.log('请求被取消')
    } else {
      // 网络错误或解析错误
      setError(err.message)
    }
  }
}
```

### 9.5.4 完整示例：从 API 获取数据并展示

```jsx
import { useState, useEffect } from 'react'

function UserProfile({ userId }) {
  const [user, setUser] = useState(null)
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const controller = new AbortController()

    async function loadUserData() {
      setLoading(true)
      setError(null)

      try {
        // 同时获取用户信息和文章列表（Promise.all）
        const [userRes, postsRes] = await Promise.all([
          fetch(`/api/users/${userId}`, { signal: controller.signal }),
          fetch(`/api/users/${userId}/posts`, { signal: controller.signal })
        ])

        if (!userRes.ok || !postsRes.ok) {
          throw new Error('获取数据失败')
        }

        const userData = await userRes.json()
        const postsData = await postsRes.json()

        setUser(userData)
        setPosts(postsData)
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message)
        }
      } finally {
        setLoading(false)
      }
    }

    loadUserData()

    return () => controller.abort()
  }, [userId])

  if (loading) return <div className="skeleton-loader">加载中...</div>
  if (error) return <div className="error-banner">❌ {error}</div>
  if (!user) return <div>用户不存在</div>

  return (
    <div className="user-profile">
      <div className="profile-header">
        <img src={user.avatar} alt={user.name} />
        <div>
          <h1>{user.name}</h1>
          <p>{user.bio}</p>
        </div>
      </div>

      <div className="posts-section">
        <h2>文章列表（{posts.length} 篇）</h2>
        {posts.map(post => (
          <div key={post.id} className="post-card">
            <h3>{post.title}</h3>
            <p>{post.excerpt}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## 本章小结

本章我们深入学习了 React 中处理"副作用"的 Hook——useEffect：

- **useEffect 基础**：useEffect 是副作用的容器，依赖数组决定执行时机；无依赖每次渲染都执行，空数组只在首次执行，指定依赖则在变化时执行
- **依赖数组规则**：依赖数组里的值必须是在 effect 中用到的所有外部值；ESLint exhaustive-deps 规则帮你检查依赖是否完整
- **清理副作用**：清理函数在下次 effect 执行前和组件卸载时执行；常见的清理场景有定时器、事件监听、WebSocket、AbortController
- **防止无限循环**：在 effect 里调用 setState 但不加依赖或依赖错误，是导致无限循环的主要原因
- **async/await 陷阱**：useEffect 不能是 async，但可以在内部定义 async 函数；清理函数不能是 async，要用同步标记位
- **数据获取三状态**：loading / error / data 三个状态覆盖了数据请求的完整生命周期

useEffect 是 React 中最复杂也最强大的 Hook。掌握好它，就掌握了 React 与外部世界交互的能力！下一章我们将学习更多 React Hooks——**useState 深入**和**自定义 Hook**！🪝