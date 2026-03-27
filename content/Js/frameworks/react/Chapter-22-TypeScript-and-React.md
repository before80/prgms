+++
title = "第22章 TypeScript与React"
weight = 220
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-22 - TypeScript 与 React

## 22.1 为什么用 TypeScript？

### 22.1.1 类型安全带来的开发体验提升

TypeScript 是 JavaScript 的超集，它在 JavaScript 的基础上添加了**静态类型检查**。在开发阶段就能发现错误，而不是等到运行时才崩溃。

```typescript
// JavaScript：运行时报错
function add(a, b) {
  return a + b
}
add(1, '2')  // 运行结果: "12" （字符串拼接！）

// TypeScript：编译时报错
function add(a: number, b: number): number {
  return a + b
}
add(1, '2')  // ❌ 编译错误：Argument of type 'string' is not assignable to parameter of type 'number'
```

### 22.1.2 编译时发现 bug，减少运行时错误

TypeScript 的类型系统能在编译阶段就捕获：
- 拼写错误的变量名
- 类型不匹配
- 调用不存在的属性/方法
- 传入错误数量的参数

### 22.1.3 代码即文档：类型定义是最好的注释

TypeScript 的类型定义本身就是最好的文档：

```typescript
interface User {
  id: number
  name: string
  email: string
  role: 'admin' | 'user' | 'guest'  // 枚举型字符串
  createdAt: Date
  avatar?: string  // 可选属性
}

// 这个函数的参数和返回值类型一目了然
function getUser(id: number): Promise<User> {
  // ...
}
```

---

## 22.2 TypeScript 基础类型

### 22.2.1 基础类型：string、number、boolean、array、object

```typescript
// 基础类型
const name: string = '小明'
const age: number = 25
const isActive: boolean = true

// 数组
const numbers: number[] = [1, 2, 3]
const names: Array<string> = ['小明', '小红']

// 对象
const user: { name: string; age: number } = {
  name: '小明',
  age: 25
}

// any：任意类型（尽量少用）
let anything: any = '可以是任何类型'
```

### 22.2.2 接口 vs 类型别名（type）

```typescript
// 接口
interface User {
  id: number
  name: string
  email: string
}

// 类型别名
type User = {
  id: number
  name: string
  email: string
}

// 两者几乎等价，但接口可以声明合并（同名接口会自动合并）
interface Config {
  theme: string
}
interface Config {
  language: string  // Config 现在有 theme 和 language 两个属性
}
```

### 22.2.3 可选属性、只读属性

```typescript
interface User {
  readonly id: number        // 只读，创建后不能修改
  name: string
  email?: string              // 可选，可以不存在
  age?: number
}

// 尝试修改只读属性会报错
const user: User = { id: 1, name: '小明' }
user.id = 2  // ❌ 错误：Cannot assign to 'id' because it is a read-only property
```

### 22.2.4 联合类型与交叉类型

```typescript
// 联合类型：可以是其中之一
type Status = 'pending' | 'approved' | 'rejected'
const status: Status = 'pending'

// 交叉类型：同时满足两者
type A = { a: string }
type B = { b: number }
type C = A & B  // { a: string; b: number }
```

---

## 22.3 React + TypeScript

### 22.3.1 函数组件 + Props 类型定义

```tsx
// 方式一：interface（推荐，声明更清晰）
interface ButtonProps {
  label: string
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
  onClick?: () => void
}

function Button({
  label,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  )
}

// 方式二：type
type UserCardProps = {
  name: string
  age: number
  avatar?: string
  onClick?: () => void
}

function UserCard({ name, age, avatar, onClick }: UserCardProps) {
  return (
    <div onClick={onClick}>
      {avatar && <img src={avatar} alt={name} />}
      <p>{name}</p>
      <p>{age}岁</p>
    </div>
  )
}
```

### 22.3.2 Props 类型推荐写法：interface vs type

| 场景 | 推荐 | 原因 |
|------|------|------|
| 组件 Props | `interface` | 语义更清晰，可声明合并 |
| 复杂联合类型 | `type` | 更灵活 |
| 需要继承/扩展 | `interface` | 支持 extends |

```tsx
// 推荐用 interface 定义组件 Props
interface CardProps {
  title: string
  children?: React.ReactNode
}

// 组件可以继承接口
interface InteractiveCardProps extends CardProps {
  onClick: () => void
}
```

### 22.3.3 children 的类型定义：ReactNode / JSX.Element

```tsx
// ReactNode：最宽松，几乎任何东西都可以
interface ContainerProps {
  children: React.ReactNode
}

// JSX.Element：只能是 JSX
interface TitleProps {
  children: JSX.Element
}

// React.ReactElement：更严格，不包括字符串等
interface LabelProps {
  children: React.ReactElement
}
```

### 22.3.4 事件处理函数的类型

```tsx
// HTML 元素事件类型
function EventHandlers() {
  function handleClick(e: React.MouseEvent<HTMLButtonElement>) {
    console.log('点击:', e.currentTarget)
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    console.log('输入值:', e.target.value)
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    console.log('表单提交')
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter') {
      console.log('按下了回车')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input onChange={handleChange} onKeyDown={handleKeyDown} />
      <button onClick={handleClick}>提交</button>
    </form>
  )
}
```

### 22.3.5 defaultProps 的 TypeScript 写法

在 TypeScript + React 中，不再需要 `defaultProps`，直接使用函数参数的默认值即可。这样类型推断更准确，代码更简洁。

```tsx
interface ButtonProps {
  label: string
  variant?: 'primary' | 'secondary'
  disabled?: boolean
}

// 使用默认参数（现代写法，推荐）
function Button({ label, variant = 'primary', disabled = false }: ButtonProps) {
  return <button className={`btn btn-${variant}`} disabled={disabled}>{label}</button>
}
```

---

## 22.4 泛型与高级类型

### 22.4.1 泛型基础：类型参数化

```typescript
// 泛型函数：类型像参数一样传入
function identity<T>(arg: T): T {
  return arg
}

const num = identity<number>(42)    // num 是 number 类型
const str = identity<string>('hello') // str 是 string 类型
const bool = identity(true)          // 自动推断为 boolean
```

### 22.4.2 泛型组件：类型参数化的列表/表单组件

```tsx
interface ListProps<T> {
  items: T[]
  renderItem: (item: T, index: number) => React.ReactNode
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>{renderItem(item, index)}</li>
      ))}
    </ul>
  )
}

// 使用
<List
  items={['苹果', '香蕉', '橙子']}
  renderItem={(item) => <span>{item}</span>}
/>

<List
  items={[{ name: '小明', age: 25 }, { name: '小红', age: 23 }]}
  renderItem={(user) => <span>{user.name} - {user.age}岁</span>}
/>
```

### 22.4.3 泛型 Hook

```tsx
// 泛型 Hook：自定义 Hook 也可以使用泛型
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch {
      return initialValue
    }
  })

  const setValue = (value: T | ((prev: T) => T)) => {
    const valueToStore = value instanceof Function ? value(storedValue) : value
    setStoredValue(valueToStore)
    localStorage.setItem(key, JSON.stringify(valueToStore))
  }

  return [storedValue, setValue] as const
}

// 使用
const [name, setName] = useLocalStorage('name', '')
const [count, setCount] = useLocalStorage('count', 0)
```

### 22.4.4 Exclude / Extract / NonNullable 等工具类型

TypeScript 内置了一些"类型操作工具"，可以让你对已有类型进行"剪切"、"拼接"、"筛选"。这就像 JavaScript 有 `Array.map`、`Array.filter` 一样，TypeScript 也有一套类型版的"数组操作"。

```typescript
// 假设你有一个状态联合类型
type Status = 'pending' | 'approved' | 'rejected' | 'cancelled'

// Exclude：排除某些类型 —— 就像数组的 filter
// 场景：后端返回的取消订单不算"活跃状态"，我们需要排除它
type ActiveStatus = Exclude<Status, 'cancelled'>
// ActiveStatus = 'pending' | 'approved' | 'rejected'

// Extract：提取某些类型 —— 就像数组的 filter（反向操作）
// 场景：只想要"成功相关"的状态
type SuccessStatus = Extract<Status, 'approved'>
// SuccessStatus = 'approved'

// NonNullable：去掉 null 和 undefined —— 就像 filter(v => v != null)
// 场景：处理可能为空的用户数据后，确保类型不再包含 null/undefined
type MaybeUser = User | null | undefined
type DefiniteUser = NonNullable<MaybeUser>
// DefiniteUser = User

// ReturnType：获取函数返回值的类型 —— 场景：你想定义一个和某个函数返回值相同类型的变量
function getUser() { return { name: '小明', age: 25 } }
type UserType = ReturnType<typeof getUser>
// UserType = { name: string; age: number }

// Partial / Required / Readonly / Pick —— 对类型进行" transformations"
// 场景：编辑表单需要所有字段可选，创建表单需要所有字段必填
interface User {
  id: number
  name: string
  email: string
}

type PartialUser = Partial<User>       // 所有属性变可选（Partial = 部分的）
type RequiredUser = Required<User>    // 所有属性变必选（Required = 必需的）
type ReadonlyUser = Readonly<User>    // 所有属性变只读（Readonly = 只读的）
type UserNameOnly = Pick<User, 'name'> // 只保留指定属性（Pick = 挑选）
```

### 22.4.5 类型守卫与类型断言

```typescript
// 类型守卫
function isString(value: unknown): value is string {
  return typeof value === 'string'
}

function process(value: unknown) {
  if (isString(value)) {
    console.log(value.toUpperCase())  // TypeScript 知道 value 是 string
  }
}

// 类型断言
function getLength(value: string | number): number {
  if (typeof value === 'string') {
    return value.length  // TypeScript 知道是 string
  } else {
    return value.toString().length  // TypeScript 知道是 number
  }
}

// 非空断言
const user = { name: '小明', age: 25 } as const
// 或者
function getName(name?: string) {
  return name!.toUpperCase()  // 断言 name 一定存在
}
```

---

## 22.5 Hooks 的类型定义

### 22.5.1 useState 的类型推断与泛型

```tsx
// 自动推断
const [name, setName] = useState('小明')  // name: string

// 显式指定泛型
const [user, setUser] = useState<User | null>(null)

// 联合类型
type Status = 'idle' | 'loading' | 'success' | 'error'
const [status, setStatus] = useState<Status>('idle')
```

### 22.5.2 useRef 的类型定义

```tsx
// DOM 元素 ref
const inputRef = useRef<HTMLInputElement>(null)
// inputRef.current 是 HTMLInputElement | null

// 可变值 ref
const timerRef = useRef<number | null>(null)
// timerRef.current 是 number | null

function Timer() {
  const timerRef = useRef<number | undefined>(undefined)

  useEffect(() => {
    timerRef.current = window.setInterval(() => {
      console.log('tick')
    }, 1000)

    return () => {
      if (timerRef.current) {
        window.clearInterval(timerRef.current)
      }
    }
  }, [])

  return <div>Timer</div>
}
```

### 22.5.3 useEffect / useCallback / useMemo 的类型

```tsx
// useEffect 的类型由回调函数的返回类型决定
useEffect(() => {
  const timer = setTimeout(() => {}, 1000)
  return () => clearTimeout(timer)
}, [])

// useCallback 自动推断
const handleClick = useCallback(() => {
  console.log('clicked')
}, [])  // handleClick: () => void

// 带泛型的 useCallback（注意：.tsx 文件中需要用 <T,> 避免与 JSX 语法冲突）
const setValue = useCallback(<T,>(value: T) => {
  console.log(value)
}, [])
```

---

## 22.6 tsconfig.json 配置

### 22.6.1 关键配置项解析

```json
{
  "compilerOptions": {
    "target": "ES2020",           // 编译到哪个 ECMAScript 版本
    "module": "ESNext",                      // 模块系统（ESNext = 最新 ES 特性，如 import/export）
    "lib": ["ES2020", "DOM"],                  // 编译时包含的类型定义库
                                                  // ES2020：语法特性（如 Promise.allSettled）
                                                  // DOM：浏览器 DOM API 类型（如 Window, Document）
    "jsx": "react-jsx",                        // JSX 编译方式
                                                  // react-jsx：React 17+ 新编译器（无需手动导入 React）
                                                  // 可选值："react"（经典）、"react-jsx"（新版）、"react-jsxdev"（开发）
    "moduleResolution": "bundler",             // 模块解析策略
                                                  // bundler：Vite/Webpack 等打包工具的解析方式，支持 path mapping
                                                  // 可选值："node"（Node 风格）、"bundler"（推荐）、"node16"、"nodenext"
    "strict": true,                            // 严格模式，开启后启用所有严格类型检查
    "esModuleInterop": true,                   // 允许 ES 模块与 CommonJS 互操作（如 `import React from 'react'` 即使 React 用 default export）
    "skipLibCheck": true,                      // 跳过第三方库（node_modules）的类型检查，加速编译
    "forceConsistentCasingInFileNames": true   // 强制文件名大小写一致，防止跨平台大小写不一致问题（Windows 不区分，Linux 区分）
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### 22.6.2 strict 模式的作用

`strict: true` 开启后相当于同时启用：
- `strictNullChecks`：null/undefined 必须显式处理
- `strictFunctionTypes`：函数参数类型必须匹配
- `strictPropertyInitialization`：类属性必须初始化

### 22.6.3 paths 路径别名配置

通过 `paths` 可以配置路径别名（如 `@/` 指向 `src/`），配合 Vite 的 alias 使用，告别长串的相对路径导入：

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@hooks/*": ["src/hooks/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

```tsx
// 现在可以这样导入
import Button from '@/components/Button'
import { useLocalStorage } from '@/hooks/useLocalStorage'
```

---

## 本章小结

本章我们学习了 **TypeScript 与 React** 的完美结合：

- **为什么用 TypeScript**：编译时发现 bug、类型安全、代码即文档
- **基础类型**：string/number/boolean/array/object、interface vs type、可选/只读属性、联合/交叉类型
- **React + TypeScript**：函数组件 Props 类型定义、children 类型、事件处理函数类型
- **泛型**：泛型函数、泛型组件、泛型 Hook，以及 Exclude/Extract/NonNullable 等工具类型
- **Hooks 类型**：useState/useRef/useEffect/useCallback/useMemo 的 TypeScript 类型

TypeScript 让 React 代码更安全、更可维护，是现代 React 开发的标配！下一章我们将学习 **Vite 深入配置**——让你的构建工具发挥最大威力！🔧