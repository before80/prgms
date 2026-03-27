+++
title = "第18章 表单处理与数据验证"
weight = 180
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-18 - 表单处理与数据验证

## 18.1 受控组件

### 18.1.1 受控组件的概念：表单数据由 React 控制

**受控组件（Controlled Component）** 是指表单元素的值完全由 React 的 state 来控制的组件。用户的输入会触发 onChange 事件，更新 state，state 更新导致组件重新渲染，渲染出新的值。

```jsx
function ControlledInput() {
  const [value, setValue] = useState('')

  function handleChange(e) {
    setValue(e.target.value)  // 用 state 存储输入值
  }

  return (
    <input
      value={value}          // value 由 state 控制
      onChange={handleChange}  // onChange 更新 state
    />
  )
}
```

### 18.1.2 input / textarea / select 的受控组件实现

```jsx
function FormDemo() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    gender: 'male',
    bio: '',
    agree: false
  })

  function handleChange(e) {
    const { name, value, type, checked } = e.target
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  return (
    <form>
      {/* input */}
      <input
        name="name"
        value={form.name}
        onChange={handleChange}
        placeholder="姓名"
      />

      {/* email */}
      <input
        name="email"
        type="email"
        value={form.email}
        onChange={handleChange}
        placeholder="邮箱"
      />

      {/* select */}
      <select name="gender" value={form.gender} onChange={handleChange}>
        <option value="male">男</option>
        <option value="female">女</option>
        <option value="other">其他</option>
      </select>

      {/* textarea */}
      <textarea
        name="bio"
        value={form.bio}
        onChange={handleChange}
        placeholder="个人简介"
      />

      {/* checkbox */}
      <input
        name="agree"
        type="checkbox"
        checked={form.agree}
        onChange={handleChange}
      />

      <button type="submit">提交</button>
    </form>
  )
}
```

### 18.1.3 处理多个输入：给每个 input 加 name

```jsx
function MultiInputForm() {
  const [form, setForm] = useState({
    username: '',
    password: '',
    remember: false
  })

  function handleChange(e) {
    const { name, value, type, checked } = e.target
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  function handleSubmit(e) {
    e.preventDefault()
    console.log('表单数据:', form)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="username"
        value={form.username}
        onChange={handleChange}
        placeholder="用户名"
      />
      <input
        name="password"
        type="password"
        value={form.password}
        onChange={handleChange}
        placeholder="密码"
      />
      <input
        name="remember"
        type="checkbox"
        checked={form.remember}
        onChange={handleChange}
      />
      <button type="submit">登录</button>
    </form>
  )
}
```

### 18.1.4 onChange 的性能问题与优化

每次按键都触发 onChange → 更新 state → 重新渲染，对于大型表单可能会有性能问题。但大多数场景下，这不是问题。只有在极端大表单（几百个字段）时才需要优化。

---

## 18.2 非受控组件

### 18.2.1 非受控组件的概念：表单数据由 DOM 自己管理

**非受控组件（Uncontrolled Component）** 是指表单数据由 DOM 自身管理，React 不控制它的值。访问表单数据的方式是使用 **ref**。

```jsx
function UncontrolledInput() {
  const inputRef = useRef(null)

  function handleSubmit(e) {
    e.preventDefault()
    console.log('输入的值:', inputRef.current.value)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input ref={inputRef} type="text" defaultValue="默认值" />
      {/* defaultValue 是非受控组件的唯一初始化方式 */}
      <button type="submit">提交</button>
    </form>
  )
}
```

### 18.2.2 useRef 获取 DOM 元素的值

对于多个非受控输入字段，可以分别用不同的 ref 指向它们，在提交时统一读取：

```jsx
function UncontrolledForm() {
  const nameRef = useRef(null)
  const emailRef = useRef(null)

  function handleSubmit(e) {
    e.preventDefault()
    console.log('name:', nameRef.current.value)
    console.log('email:', emailRef.current.value)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input ref={nameRef} type="text" placeholder="姓名" />
      <input ref={emailRef} type="email" placeholder="邮箱" />
      <button type="submit">提交</button>
    </form>
  )
}
```

### 18.2.3 非受控组件的 defaultValue / defaultChecked

非受控组件的值在 HTML 自身（DOM）中，用 `defaultValue`（text/radio）和 `defaultChecked`（checkbox）来设置初始值。注意：这些只是初始值，之后修改不会同步到 React。

```jsx
<input
  ref={inputRef}
  defaultValue="初始值"       // text input
  defaultChecked={true}      // checkbox / radio
/>
```

### 18.2.4 受控 vs 非受控：何时用哪种

| 场景 | 受控组件 | 非受控组件 |
|------|---------|-----------|
| 需要实时验证/格式化 | ✅ | ❌ |
| 需要根据某个值禁用/控制 | ✅ | ❌ |
| 文件上传 | ❌ | ✅ |
| 简单表单、快速实现 | ❌ | ✅ |
| 表单数据最终要提交 | ✅ | ✅ |

---

## 18.3 React Hook Form

### 18.3.1 安装与核心概念

你有没有发现：受控组件每次输入都要 `onChange` → `setState` → 重渲染。对于一个有很多字段的表单，这会产生大量的重渲染——用户每打一个字，整个表单都要重新渲染一次！

**React Hook Form** 就是来解决这个性能问题的。它用了"非受控组件"的技术——表单字段自己管理自己的值，React 只有在提交时才去读取。这样输入时就不会触发重渲染，性能飙升！

React Hook Form 是目前最流行的 React 表单库，它的特点是：**高性能（不触发不必要的重渲染）、易用、轻量**。

```bash
npm install react-hook-form
```

核心概念：
- `register`：注册表单字段（告诉 Hook Form "这个输入框归我管了"）
- `handleSubmit`：处理表单提交
- `watch`：监听字段值变化
- `errors`：获取错误信息

### 18.3.2 register：注册表单字段

```jsx
import { useForm } from 'react-hook-form'

function RegisterForm() {
  const { register, handleSubmit } = useForm()

  function onSubmit(data) {
    console.log('表单数据:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* register 注册字段 */}
      <input {...register('name')} placeholder="姓名" />
      <input {...register('email')} placeholder="邮箱" />
      <input {...register('password')} type="password" placeholder="密码" />
      <button type="submit">注册</button>
    </form>
  )
}
```

### 18.3.3 handleSubmit：表单提交处理

```jsx
function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm()

  function onSubmit(data) {
    console.log('表单数据:', data)
    // { name: '小明', email: 'xiaoming@example.com', password: '123456' }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email', { required: true })} placeholder="邮箱" />
      {errors.email && <span>邮箱是必填项</span>}

      <input {...register('password', { required: true, minLength: 6 })} type="password" />
      {errors.password && <span>密码至少6位</span>}

      <button type="submit">登录</button>
    </form>
  )
}
```

### 18.3.4 watch：实时监控字段值

```jsx
function SearchForm() {
  const { register, watch } = useForm()

  const searchValue = watch('search')
  const category = watch('category')

  return (
    <form>
      <input {...register('search')} placeholder="搜索..." />
      <p>当前搜索词：{searchValue}</p>
      <p>当前分类：{category}</p>
    </form>
  )
}
```

### 18.3.5 errors：获取错误信息

```jsx
function ValidationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    mode: 'onBlur'  // 验证时机：onBlur（失去焦点时）/ onChange（变化时）/ onSubmit（提交时）
  })

  function onSubmit(data) {
    console.log('表单数据:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('name', {
          required: '姓名不能为空',
          minLength: { value: 2, message: '姓名至少2个字符' }
        })}
      />
      {errors.name && <p className="error">{errors.name.message}</p>}

      <input
        {...register('email', {
          required: '邮箱不能为空',
          pattern: {
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: '邮箱格式不正确'
          }
        })}
      />
      {errors.email && <p className="error">{errors.email.message}</p>}

      <input
        {...register('age', {
          valueAsNumber: true,
          validate: value => value >= 18 || '必须年满18周岁'
        })}
        type="number"
      />
      {errors.age && <p className="error">{errors.age.message}</p>}

      <button type="submit">提交</button>
    </form>
  )
}
```

### 18.3.6 Controller：配合第三方 UI 组件使用

当使用第三方 UI 组件（如 Ant Design、Material UI）时，直接用 register 可能不生效，需要用 Controller 包装：

```jsx
import { useForm, Controller } from 'react-hook-form'
import { Select, DatePicker } from 'antd'

function AdvancedForm() {
  const { control, handleSubmit } = useForm()

  function onSubmit(data) {
    console.log('表单数据:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* 使用 Controller 包装第三方 Select */}
      <Controller
        name="category"
        control={control}
        rules={{ required: '请选择分类' }}
        render={({ field }) => (
          <Select
            {...field}
            placeholder="请选择分类"
            options={[
              { value: 'tech', label: '科技' },
              { value: 'art', label: '艺术' },
              { value: 'music', label: '音乐' }
            ]}
          />
        )}
      />

      {/* 使用 Controller 包装第三方 DatePicker */}
      <Controller
        name="birthday"
        control={control}
        render={({ field }) => (
          <DatePicker onChange={date => field.onChange(date)} />
        )}
      />

      <button type="submit">提交</button>
    </form>
  )
}
```

### 18.3.7 useFormContext：深层表单共享

当表单状态需要在深层嵌套的组件中访问时，用 `useFormContext`：

```jsx
import { useForm, FormProvider, useFormContext } from 'react-hook-form'

// 父组件
function App() {
  const methods = useForm()
  return (
    <FormProvider {...methods}>
      <form>
        <Step1 />
        <Step2 />
        <Step3 />
      </form>
    </FormProvider>
  )
}

// 子组件 - 使用 useFormContext 获取表单上下文
function Step2() {
  const { register, formState: { errors } } = useFormContext()

  return (
    <div>
      <input {...register('address')} placeholder="地址" />
      <input {...register('phone')} placeholder="电话" />
    </div>
  )
}
```

---

## 18.4 Zod schema 验证

### 18.4.1 Zod 的安装与基本用法

在用 React Hook Form 时，我们可以在 `register` 中写验证规则：

```jsx
<input {...register('email', { required: true, minLength: 6 })} />
```

这看起来挺简单，但如果表单字段很多呢？10个字段、20个字段，每个都要写一堆规则，整个表单组件会变得又长又乱。更要命的是，这些验证规则散落在 UI 代码里，不方便复用和测试。

**Zod 就是来解决这个问题的**——它让你把验证规则集中在一起，像写"数据宪法"一样定义"我的表单应该长什么样"。验证规则和 UI 代码分离，两边都清爽！

**Zod** 是一个 TypeScript 优先的模式声明和验证库，与 React Hook Form 配合使用非常方便。

```bash
npm install zod
npm install @hookform/resolvers
```

```jsx
import { z } from 'zod'

// 定义验证 schema
const userSchema = z.object({
  name: z.string().min(2, '姓名至少2个字符'),
  email: z.string().email('邮箱格式不正确'),
  age: z.number().min(18, '必须年满18周岁'),
  password: z.string().min(6, '密码至少6位'),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: '两次密码不一致',
  path: ['confirmPassword']
})
```

### 18.4.2 schema 定义验证规则

```jsx
const schema = z.object({
  // 字符串验证
  name: z.string()
    .min(2, '姓名至少2个字符')
    .max(50, '姓名最多50个字符'),

  // 邮箱验证
  email: z.string()
    .email('邮箱格式不正确'),

  // URL 验证
  website: z.string().url('必须是有效的 URL'),

  // 数字验证
  age: z.number()
    .min(0, '年龄不能为负数')
    .max(150, '年龄不能超过150'),

  // 正则验证
  phone: z.string()
    .regex(/^1[3-9]\d{9}$/, '手机号格式不正确'),

  // 枚举验证
  role: z.enum(['admin', 'user', 'guest']),

  // 布尔验证
  agree: z.boolean()
    .refine(val => val === true, '必须同意条款'),

  // 数组验证
  tags: z.array(z.string()).min(1, '至少选择一个标签'),

  // 对象验证
  address: z.object({
    city: z.string(),
    street: z.string()
  })
})
```

### 18.4.3 与 React Hook Form 集成

```jsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(2, '姓名至少2个字符'),
  email: z.string().email('邮箱格式不正确'),
  age: z.number().min(18, '必须年满18周岁').or(z.string().transform(v => Number(v)))
})

function ZodForm() {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    resolver: zodResolver(schema)  // 用 Zod resolver 替换默认验证
  })

  function onSubmit(data) {
    console.log('表单数据:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} />
      {errors.name && <p>{errors.name.message}</p>}

      <input {...register('email')} />
      {errors.email && <p>{errors.email.message}</p>}

      <input type="number" {...register('age', { valueAsNumber: true })} />
      {errors.age && <p>{errors.age.message}</p>}

      <button type="submit">提交</button>
    </form>
  )
}
```

### 18.4.4 常用验证规则：string、number、object、array、enum

```jsx
const schema = z.object({
  // 字符串
  username: z.string().min(3).max(20),
  bio: z.string().optional(),           // 可选
  nickname: z.string().nullable(),     // 可以是 null

  // 数字
  price: z.number().positive(),         // 正数
  discount: z.number().min(0).max(1), // 0-1 之间

  // 枚举
  status: z.enum(['pending', 'approved', 'rejected']),

  // 数组
  emails: z.array(z.string().email()).min(1),

  // 对象
  config: z.object({
    theme: z.string(),
    language: z.string()
  }),

  // 联合类型
  type: z.union([z.string(), z.number()]),

  // 深度可选
  nested: z.object({
    deep: z.object({
      value: z.string()
    }).optional()
  })
})
```

### 18.4.5 自定义错误消息与验证函数

```jsx
const schema = z.object({
  username: z.string()
    .min(2, '太短了，至少2个字符')
    .max(20, '太长了，最多20个字符')
    .refine(val => /^[a-zA-Z]/.test(val), {
      message: '必须以字母开头'
    }),

  // 自定义验证函数
  customField: z.string()
    .refine(val => {
      // 自定义逻辑，返回 true 表示通过
      return checkSomething(val)
    }, {
      message: '自定义验证失败'
    })
})
```

---

## 18.5 文件上传

### 18.5.1 文件上传的基本表单结构

文件上传用受控组件的方式来实现——用 `useState` 保存选中的文件对象：

```jsx
function FileUpload() {
  const [file, setFile] = useState(null)

  function handleFileChange(e) {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)
  }

  return (
    <form>
      <input type="file" onChange={handleFileChange} />
      {file && <p>已选择: {file.name} ({(file.size / 1024).toFixed(2)} KB)</p>}
    </form>
  )
}
```

### 18.5.2 使用 ref 获取文件

```jsx
function FileUploadWithRef() {
  const fileInputRef = useRef(null)

  function handleSubmit(e) {
    e.preventDefault()
    const file = fileInputRef.current.files[0]
    console.log('上传文件:', file)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input ref={fileInputRef} type="file" accept=".jpg,.png,.pdf" />
      <button type="submit">上传</button>
    </form>
  )
}
```

### 18.5.3 FormData 处理文件上传

准备好文件后，用 `FormData` 对象包装并通过 `fetch` 或 `axios` 发送到服务器。`FormData` 会自动设置正确的 `Content-Type: multipart/form-data`，无需手动指定：

```jsx
async function uploadFile(file) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('filename', file.name)

  const response = await fetch('/api/upload', {
    method: 'POST',
    body: formData
  })

  return response.json()
}
```

### 18.5.4 文件预览与多文件上传

```jsx
function MultiFileUpload() {
  const [previews, setPreviews] = useState([])

  function handleFileChange(e) {
    const files = Array.from(e.target.files)

    // 生成预览 URL
    const newPreviews = files.map(file => ({
      file,
      preview: URL.createObjectURL(file)
    }))

    setPreviews(newPreviews)
  }

  return (
    <div>
      <input type="file" multiple onChange={handleFileChange} />

      <div style={{ display: 'flex', gap: '8px' }}>
        {previews.map((item, index) => (
          <div key={index}>
            {item.file.type.startsWith('image/') ? (
              <img
                src={item.preview}
                alt="预览"
                style={{ width: 100, height: 100, objectFit: 'cover' }}
              />
            ) : (
              <div>{item.file.name}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## 18.6 React 19 <Form> 组件（新方式）

### 18.6.1 `<Form>` vs 受控组件 vs React Hook Form：三种方式对比

React 19 引入了内置的 `<Form>` 组件（由 React Router v7 提供更完整的实现），它结合了受控组件的声明式写法与 React Hook Form 的高性能，同时原生支持服务端 Action。下面从几个关键维度对比三种方案：

| 对比项 | 受控组件 | React Hook Form | React 19 `<Form>` |
|-------|---------|----------------|----------------|
| **性能** | 每次输入都重渲染 | 几乎无重渲染 | 无重渲染 |
| **验证** | 手动或第三方库 | 内置 + Zod | 内置（actions） |
| **学习曲线** | 低 | 中 | 低 |
| **与后端集成** | 需要 JS 处理 | 需要 JS 处理 | 原生支持 action |
| **SSR 支持** | 手动处理 | 需要额外配置 | 原生支持 |

### 18.6.2 `<Form>` 的渐进增强：JavaScript 禁用时仍可工作

```jsx
import { Form } from 'react-router-dom'

// React 19 的 <Form> 组件
function ContactForm() {
  return (
    // action 是服务端点，method 是 HTTP 方法
    // 当 JS 禁用时，表单会像普通 HTML 表单一样提交
    // 当 JS 启用时，React 会拦截提交并用 fetch 发送（无刷新）
    <Form action="/api/contact" method="post">
      <input name="name" placeholder="姓名" />
      <input name="email" type="email" placeholder="邮箱" />
      <textarea name="message" placeholder="留言" />
      <button type="submit">发送</button>
    </Form>
  )
}
```

### 18.6.3 `<Form>` 与 Actions 的结合使用

```jsx
// 在 React Router v7 中使用 action 处理表单提交
import { Form, useActionData, useNavigation } from 'react-router-dom'

async function contactAction({ request }) {
  const formData = await request.formData()
  const name = formData.get('name')
  const email = formData.get('email')
  const message = formData.get('message')

  // 验证
  if (!name || !email) {
    return { error: '姓名和邮箱必填' }
  }

  // 发送到后端
  await sendEmail({ name, email, message })

  return { success: true }
}

function ContactPage() {
  const actionData = useActionData()
  const navigation = useNavigation()
  const isSubmitting = navigation.state === 'submitting'

  return (
    <Form method="post">
      <input name="name" placeholder="姓名" />
      <input name="email" type="email" placeholder="邮箱" />
      <textarea name="message" placeholder="留言" />

      {actionData?.error && <p className="error">{actionData.error}</p>}
      {actionData?.success && <p className="success">发送成功！</p>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '发送中...' : '发送'}
      </button>
    </Form>
  )
}
```

### 18.6.4 `<Form>` 的状态管理：loading / success / error

```jsx
import { Form, useNavigation, useActionData } from 'react-router-dom'

function SubscribeForm() {
  const navigation = useNavigation()
  const actionData = useActionData()

  // 状态
  const isLoading = navigation.state === 'loading'
  const isSubmitting = navigation.state === 'submitting'

  return (
    <Form method="post" action="/api/subscribe">
      <input name="email" type="email" placeholder="订阅邮箱" />

      {actionData?.success && (
        <p style={{ color: 'green' }}>订阅成功！</p>
      )}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '订阅中...' : '订阅'}
      </button>
    </Form>
  )
}
```

---

## 本章小结

本章我们系统学习了 React 表单处理的方方面面：

- **受控组件**：表单值由 React state 控制，onChange 更新 state，适合需要实时验证/格式化的场景
- **非受控组件**：表单值由 DOM 管理，用 ref 获取，适合文件上传等简单场景
- **React Hook Form**：高性能表单库，`register` 注册字段、`handleSubmit` 处理提交、`errors` 获取错误、Controller 包装第三方组件
- **Zod 验证**：TypeScript 优先的 schema 验证库，配合 `@hookform/resolvers` 与 React Hook Form 完美集成
- **文件上传**：使用 ref 或受控方式获取文件，FormData 处理上传，URL.createObjectURL 生成预览
- **React 19 `<Form>`**：新一代表单方案，内置渐进增强，与 Actions 深度集成，loading/success/error 状态原生支持

表单是前端最复杂的交互场景之一，选择合适的方案能大幅提升开发效率和用户体验！下一章我们将学习 **HTTP 请求与数据获取**——让 React 与后端"对话"！🌐