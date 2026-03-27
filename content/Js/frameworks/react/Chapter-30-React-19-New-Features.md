+++
title = "第30章 React 19新特性"
weight = 300
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-30 - React 19 新特性

## 30.1 use() Hook：React 19 最重大的 API

### 30.1.1 use() 的基本用法

`use()` 是 React 19 引入的最重要新 API，它允许在组件内部读取 Promise 和 Context。

```jsx
import { use } from 'react'

// use() 读取 Promise
function UserProfile({ userPromise }) {
  const user = use(userPromise)
  return <h1>{user.name}</h1>
}
```

### 30.1.2 use() 在 render 中读取 Promise / Context

`use()` 可以在渲染阶段读取 Promise，并在 Promise resolve 后自动重新渲染。

> ⚠️ **重要**：`use()` 读取 Promise 时，组件会进入"挂起（Suspended）"状态，因此**必须在 `use()` 外层包裹 `Suspense`** 边界来展示加载中 UI，否则会报错。

```jsx
function Comments({ commentsPromise }) {
  // use() 会等待 Promise resolve（组件此时会挂起）
  // 如果不用 Suspense 包裹，Promise pending 时会抛出错误
  const comments = use(commentsPromise)

  return (
    <ul>
      {comments.map(c => (
        <li key={c.id}>{c.text}</li>
      ))}
    </ul>
  )
}

// 使用时必须包裹 Suspense：
// <Suspense fallback={<div>加载中...</div>}>
//   <Comments commentsPromise={fetchComments(postId)} />
// </Suspense>
```

### 30.1.3 use() vs useContext 的区别

| 对比 | useContext | use() |
|------|-----------|--------|
| 用法 | `useContext(Context)` | `use(Context)` |
| 条件调用 | 不允许 | 允许（可以在 if 里用） |

```jsx
// use() 可以在条件语句中使用
function MyComponent({ showTheme }) {
  let theme = null  // ✅ 允许条件调用，但变量需在外部声明
  if (showTheme) {
    theme = use(ThemeContext)
  }
  return <div style={{ background: theme?.color }}>Hello</div>
}
```

### 30.1.4 use() 的 Suspense 集成

`use()` 与 Suspense 深度集成——当 Promise 处于 pending 状态时，组件会挂起，Suspense 的 fallback 就派上用场了：

```jsx
// use() 搭配 Suspense 使用：加载中显示 fallback，成功后显示内容
<Suspense fallback={<div>加载中...</div>}>
  <UserProfile userPromise={fetchUser(id)} />
</Suspense>
```

### 30.1.5 use() 的错误处理

`use()` 读取的 Promise 如果 reject，会触发 **Error Boundary**（错误边界）——这是 React 提供的组件级错误处理机制：

```jsx
// Promise 被 reject 时，Error Boundary 会捕获错误并显示降级 UI
<ErrorBoundary fallback={<div>加载用户信息失败</div>}>
  <Suspense fallback={<div>加载中...</div>}>
    <UserProfile userPromise={fetchUser(id)} />
  </Suspense>
</ErrorBoundary>
```

所以 `use()` + Promise 的完整"兜底"组合是：**Suspense**（处理加载中）+ **Error Boundary**（处理加载失败），两者缺一不可。

---

## 30.2 useOptimistic：乐观更新

### 30.2.1 useOptimistic 的基本用法

`useOptimistic` 让你在请求还在进行时就更新 UI，提供即时的用户反馈。

```jsx
import { useOptimistic } from 'react'

function LikeButton({ likes, onLike }) {
  // useOptimistic：返回 [乐观值, 添加乐观更新的函数]
  // 第一个参数是当前"真实"值（服务端返回的 likes）
  // 第二个参数是"乐观更新函数"：
  //   state = 当前乐观值（初始为 likes），newLike = 传给 addOptimisticLike 的参数
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (state, newLike) => state + newLike  // 旧状态 + 新增量 = 新状态
  )

  async function handleLike() {
    addOptimisticLike(1)  // 立即将 UI 显示为 likes + 1（不等服务端）
    await onLike()        // 实际请求在后台进行
  }

  return (
    <button onClick={handleLike}>
      👍 {optimisticLikes}
    </button>
  )
}
```

### 30.2.2 典型场景：即时反馈 + 后台确认

`useOptimistic` 的核心价值是**消除等待感**。典型应用：

- **点赞**：点完就变红，后台默默发请求，失败了再回退
- **发帖/评论**：发完立即显示在列表里，后台慢慢存
- **表单提交**：提交按钮瞬间变"处理中..."，实际请求在后台跑

想象你在餐厅点完菜，服务员说"您的菜已经在做了"，然后先去忙别的——虽然菜还没端上来，但你已经不焦虑了，因为你知道"已经在处理中"。`useOptimistic` 就是给用户的这种安心。

原理很简单：
1. 用户操作 → **立即**更新 UI（显示乐观结果）
2. 实际请求在后台进行
3. 成功：啥都不用做（UI 本来就是对的）
4. 失败：回退到真实状态 + 提示用户

---

## 30.3 Actions 与 Server Actions

### 30.3.1 Actions 的概念：可自动执行的可序列化函数引用

Actions 是 React 19 引入的核心概念，全称是"可自动执行的可序列化函数引用"。听起来很玄乎，但拆开来看就很好理解：

- **可序列化**：函数引用可以在客户端和服务端之间传递（通过 `'use server'` 标记）
- **可自动执行**：Actions 配合 `<form action={...}>` 使用时，React 会自动处理提交、loading 状态、错误处理，甚至乐观更新

**用传统写法对比一下，你就知道 Actions 香在哪里：**

```jsx
// 🚢 传统写法：表单提交需要一大坨代码
function OldForm() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()  // 阻止默认行为
    setLoading(true)
    setError(null)
    
    try {
      const formData = new FormData(e.target)
      await fetch('/api/createPost', {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(formData))
      })
      // 成功后还要清空表单、跳转页面...
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      {/* loading 和 error 的 UI 都要自己写 */}
      {loading && <Spinner />}
      {error && <ErrorMessage error={error} />}
      <input name="title" />
      <button disabled={loading}>提交</button>
    </form>
  )
}
```

```jsx
// ✨ Actions 写法：简洁到哭
async function createPost(formData) {
  'use server'  // 这行代码运行在服务端！
  await db.posts.create({ title: formData.get('title') })
}

function NewForm() {
  return (
    <form action={createPost}>
      {/* loading？自动处理！ */}
      {/* error？自动处理！ */}
      {/* 成功？自动处理！ */}
      <input name="title" />
      <button type="submit">提交</button>
    </form>
  )
}
```

Actions 让"表单提交"这件事变得异常简洁——不需要手动写 `e.preventDefault()`，不需要手动管理 loading 状态，不需要手动处理错误。React 帮你一条龙搞定。

这在以前需要一堆 `useState` + `handleSubmit` + `try/catch` 才能实现的场景，现在几行代码就搞定了。

### 30.3.2 HTML form 的 actions 属性

```jsx
// 注意：'use server' 必须写在文件最顶部（所有 import 之前！）
// 'use server'

// 以下为 actions.ts（服务端文件）的写法示例：
// 'use server'  // ← 必须位于文件第一行！
//
// async function createPost(formData: FormData) {
//   const title = formData.get('title')
//   await db.posts.create({ title })
// }

// 前端组件中使用时，直接把 Server Action 作为 action 传递：
function Form() {
  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">提交</button>
    </form>
  )
}
```

> ⚠️ **常见误区**：`'use server'` 并不是写在组件函数内部或 `<form>` 内部，而是写在**独立的文件顶部**，相当于把这个文件声明为"服务端文件"。组件里直接 import 这个 action 函数并传给 `action={...}` 即可。

### 30.3.3 Server Actions：服务端操作的前端调用

Server Actions 是 Actions 的"服务端版本"——用 `'use server'` 标记的函数实际上运行在服务端（或者通过 RPC 调用服务端），但前端可以像调用普通函数一样调用它，React 自动处理序列化、网络传输、反序列化。

```jsx
// actions.ts（服务端文件）
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  // 这里可以直接访问数据库，无需 API 接口
  await db.posts.create({ title })
}
```

Server Actions 的优势是**省略了传统 API 接口层**——不需要写 `POST /api/posts` 路由，不需要处理 HTTP 状态码，不需要处理请求体序列化。表单提交直接对应一个数据库操作，开发体验大幅提升。

### 30.3.4 useTransition 在 Actions 中的作用

Actions 虽然已经自动处理了 loading 状态，但 `useTransition` 可以让你**更精细地控制过渡效果**——比如在 Action 执行期间让整个页面保持可交互（部分区域显示 loading，部分区域正常工作）。

```jsx
function PostForm() {
  const [isPending, startTransition] = useTransition()

  async function handleSubmit(formData) {
    startTransition(async () => {
      await createPost(formData)  // Action 在 transition 内执行
    })
  }

  return (
    <form action={handleSubmit}>
      <input name="title" />
      <button type="submit" disabled={isPending}>
        {isPending ? '发布中...' : '发布'}
      </button>
    </form>
  )
}
```

实际上，如果 Action 是表单提交的最简单场景，你可能根本不需要 `useTransition`——Action 本身就处理了 pending 状态。只有当你需要在 Action 执行期间保持其他 UI 可交互时，才需要显式用 `useTransition`。

---

## 30.4 ref 作为 prop 直接传递

### 30.4.1 ref 作为普通 prop 传递（无需 forwardRef）

React 19 之前需要用 `forwardRef` 才能接收 ref。React 19 中，函数组件可以直接接收 ref 作为 prop。

```jsx
// React 19：不需要 forwardRef
function Button({ children, ref }) {
  return <button ref={ref}>{children}</button>
}
```

### 30.4.2 React 19 也依然支持 forwardRef（向后兼容）

```jsx
// React 19 仍然支持 forwardRef
const Button = forwardRef(({ children }, ref) => {
  return <button ref={ref}>{children}</button>
})
```

---

## 30.5 错误处理改进

### 30.5.1 错误堆栈的改进

React 19 大幅改进了开发时的错误提示体验。以前如果组件报错，你看到的错误堆栈可能只有一行模糊的 "Error: An error occurred"，根本不知道是哪行代码出的问题。React 19 会显示更完整的组件堆栈，甚至能告诉你是哪个父组件导致的问题。

```jsx
// React 18 的错误（可能是这样的）
Error: Minified React Error #418

// React 19 的错误（更详细的组件堆栈）
Error: Cannot read property 'map' of undefined

  at CommentList (comments.jsx:12)
  at PostDetail (post.jsx:5)
  at App (app.jsx:10)
```

这对于线上排查问题特别有用——不用再对着压缩后的代码干瞪眼了。

### 30.5.2 Error Boundary 与新 Root API

Error Boundary（错误边界）是 React 提供的组件级错误处理机制——如果子组件在渲染时出错，Error Boundary 可以"接住"这个错误，显示一个降级 UI，而不是整个应用白屏。

```jsx
import { Component } from 'react'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error) {
    // 更新 state 使下一次渲染能够显示降级 UI
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    // 记录错误日志
    console.error('React Error:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong.</div>
    }
    return this.props.children
  }
}

// 使用
<ErrorBoundary>
  <BuggyComponent />
</ErrorBoundary>
```

React 19 引入了 **new Root API**（`createRoot`），这是现在创建 React 应用的唯一方式。旧的 `ReactDOM.render` 已经废弃了。

```jsx
// React 18+ 唯一正确的用法
import { createRoot } from 'react-dom/client'

const root = createRoot(document.getElementById('root'))
root.render(<App />)

// ReactDOM.render（React 18 之前的方式）已废弃
// ReactDOM.render(<App />, rootElement)  // ❌ 别用了
```

`createRoot` 的优势是支持并发特性（Concurrent Mode），并且错误处理更加健壮。如果你在用 React 18+，确保所有地方都迁移到了 `createRoot`。

---

## 30.6 React 19 清理机制改进

### 30.6.1 cleanup 函数在 ref 中的支持

React 19 支持在 ref callback 中返回清理函数。

```jsx
function Input() {
  return (
    <input
      ref={node => {
        console.log('mounted', node)
        return () => console.log('unmounted')  // ✅ cleanup 函数
      }}
    />
  )
}
```

---

## 30.7 React 19 迁移指南

### 30.7.1 从 React 18 升级到 19 的步骤

1. 升级依赖：`npm install react@19 react-dom@19`
2. 升级相关库（如 react-router-dom 需要 v7）
3. 运行 TypeScript 检查：`tsc --noEmit`
4. 修复废弃 API 的警告

### 30.7.2 废弃的 API 与替代方案

| 废弃 | 替代 |
|------|------|
| `forwardRef`（简化版 ref 传递已内置） | 直接将 `ref` 作为 prop 接收 |
| Legacy Root API `ReactDOM.render` | `createRoot` |
| string ref | callback ref / 对象 ref |

### 30.7.3 React 19 对第三方库的影响

React 19 本身是向后兼容的，大多数应用可以相对平滑地升级。但**第三方库**需要针对 React 19 做适配，尤其是涉及 Hooks 内部实现或 Ref 相关的库。

好消息是，主流生态已经基本完成适配：
- **React Router v7**：完整支持 React 19
- **Redux Toolkit**：v2.0+ 支持
- **Zustand**：v4.5+ 支持
- **SWR / TanStack Query**：最新版支持 Suspense for Data Fetching

如果你用的库较老，升级前建议先查一下 Changelog 或在 GitHub 上确认是否已有 React 19 兼容版本。另外，升级后用 `npm audit` 跑一遍安全检查，`npm run lint` 跑一遍代码检查，确保没有遗漏的废弃警告。

---

## 本章小结

本章我们全面学习了 React 19 的新特性：

- **use() Hook**：可在渲染中读取 Promise/Context，支持条件调用，是 React 19 最重要的 API
- **useOptimistic**：乐观更新，即时 UI 反馈
- **Actions 与 Server Actions**：简化表单提交流程
- **ref 作为 prop**：无需 forwardRef
- **清理机制改进**：ref callback 支持返回清理函数

React 19 让 React 开发体验更上一层楼！最让人眼前一亮的是 `use()` 终于打破了 Hook 不能条件调用的铁律，而 `useOptimistic` 让"先让 UI 爽起来"变成了官方认可的最佳实践。下一章我们将学习 **React 并发模式**——让你在用户输入和后台加载之间优雅地"摸鱼"！⚡