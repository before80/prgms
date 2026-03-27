+++
title = "第10章 响应式 API 进阶"
weight = 100
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十章 响应式 API 进阶

> ref 和 reactive 只是 Vue 响应式系统的"入门 API"。这一章我们来探索更深层的东西——shallowRef、shallowReactive、markRaw、toRaw、readonly、customRef……以及 watch 的各种高级用法、nextTick 的原理。读完这一章，你对 Vue 响应式系统的理解会从"会用"升级到"理解原理"。

## 10.1 响应式 API 全解

### 10.1.1 ref 与 reactive 深度对比

前面已经讲过 `ref` 和 `reactive`，这里做一下深度对比，帮你彻底理解两者的异同：

| | ref | reactive |
|---|---|---|
| 适用类型 | 基本类型 + 对象/数组 | 仅对象/数组 |
| 访问方式 | `.value`（script）/ 自动解包（template） | 直接属性访问 |
| 可以整体替换 | ✅ `ref.value = newValue` | ❌ 需要 `Object.assign` |
| 解构后响应式 | ❌（除非用 toRefs） | ❌（除非用 toRefs） |
| 类型标注 | 泛型参数：`ref<T>()` | 泛型参数：`reactive<T>()` |
| 内部实现 | 对象包装 + getter/setter | Proxy |

```typescript
import { ref, reactive } from 'vue'

// ref 适合基本类型
const count = ref(0)
const name = ref('小明')

// ref 也适合对象（会自动用 reactive 包装）
const user = ref({ name: '小明', age: 25 })
// 访问时：user.value.name
// 模板里：user.name（自动解包）

// reactive 只适合对象/数组
const state = reactive({
  count: 0,
  user: { name: '小明' }
})
// 访问时：state.count, state.user.name

// 整体替换：ref 可以，reactive 不行
count.value = 10  // ✅ OK
// reactive 不支持：state = reactive({ new: 'state' }) —— 会丢失响应式

// 如果真的要替换 reactive 的整体，用 Object.assign
Object.assign(state, { count: 10 })  // ✅ OK
```

### 10.1.2 shallowRef 与 triggerRef

`ref` 会递归地把所有嵌套属性都变成响应式的——如果你的数据嵌套很深（比如一个巨大的对象），`ref` 可能会带来性能问题。

`shallowRef` 是"浅层响应式"的 ref——它只把**第一层**变成响应式的，深层属性的变化**不会**触发视图更新，除非你手动**强制触发**。

```typescript
import { shallowRef, triggerRef } from 'vue'

// shallowRef：只追踪 .value 的变化，不追踪内部属性的变化
const state = shallowRef({
  count: 0,
  nested: {
    value: 100
  }
})

state.value.count++         // ⚠️ 不会触发视图更新！因为只追踪 .value
state.value = { count: 1, nested: { value: 100 } }  // ✅ 整体替换会触发

// 如果只想更新深层属性，需要手动调用 triggerRef
state.value.nested.value = 200
triggerRef(state)  // 强制触发更新 —— 但这基本等于放弃了响应式的自动追踪
```

**什么时候用 `shallowRef`？**

- 数据结构非常庞大，深层变化频繁，但视图不需要每次都更新（比如大数据量的表格、游戏引擎数据）
- 性能优化场景：如果你明确知道只在特定时机更新视图，可以用 shallowRef 减少不必要的追踪

```typescript
import { shallowRef } from 'vue'

// 场景：大数据量列表，只在翻页时更新
const largeDataTable = shallowRef({
  rows: [],       // 第一次填充
  page: 1,
  totalPages: 100
})

// 翻页时整体替换数据
async function loadPage(page: number) {
  const data = await fetchPageData(page)
  largeDataTable.value = { rows: data.rows, page, totalPages: data.totalPages }
  // shallowRef 只追踪 .value 的变化，所以整体替换才会触发更新
}
```

### 10.1.3 shallowReactive 与 readonly

**`shallowReactive`**：和 `shallowRef` 类似，`shallowReactive` 只让对象的第一层属性响应式，深层不会。

```typescript
import { shallowReactive, readonly } from 'vue'

// shallowReactive：只有第一层是响应式的
const state = shallowReactive({
  count: 0,
  nested: {
    value: 100
  }
})

state.count++      // ✅ 响应式更新
state.nested.value = 200  // ⚠️ 不会触发更新！
```

**`readonly`**：把一个响应式对象变成"只读"——任何修改操作都会报警告。常用于只读的常量或配置数据。

```typescript
import { readonly, reactive } from 'vue'

// readonly：只读副本
const original = reactive({
  apiBase: 'https://api.example.com',
  maxRetries: 3,
  config: { timeout: 5000 }
})

const config = readonly(original)

// 读取没问题
console.log(config.apiBase)  // https://api.example.com

// 修改会报警告
config.apiBase = 'http://localhost'  // ⚠️ Vue 会报警告：Vue received a Received-a-reactive-proxy-of...
config.maxRetries = 10              // ⚠️ 同样报警告

// 修改 original 也会影响 config（因为是同一份数据）
original.apiBase = 'http://changed.com'
console.log(config.apiBase)  // http://changed.com —— readonly 不创造副本，只是禁止修改
```

**`readable`**：`readonly` 是"只读"版本，如果你的数据一开始就是普通数据（非响应式），想变成只读但不转 Proxy，可以用 `readable`。

```typescript
import { readonly, ref } from 'vue'

const count = ref(0)

// readonly 创建只读代理
const readOnlyCount = readonly(count)

// 读取 OK
console.log(readOnlyCount.value)  // 0

// 写入会报错
count.value++  // ⚠️ 报错（如果直接赋值给 readonly 的响应式数据）
```

### 10.1.4 markRaw（绕过响应式）

`markRaw` 告诉 Vue："这个对象不需要响应式处理"，可以提升性能。常用于不渲染在模板里、只是当作配置或工具函数使用的对象。

```typescript
import { reactive, markRaw } from 'vue'

// 如果一个对象不需要响应式，用 markRaw 可以避免不必要的 Proxy 包装开销
const utils = markRaw({
  formatDate: (date: Date) => date.toISOString(),
  deepClone: <T>(obj: T): T => JSON.parse(JSON.stringify(obj)),
  someLargeLib: new LargeLibrary()  // 大型库实例，不需要响应式追踪
})

const state = reactive({
  data: { message: 'hello' },
  utils  // utils 里的内容不会被 Proxy 包装
})
```

**常见的使用场景：**

- 第三方库的实例（如 axios、lodash）
- 不需要在模板中渲染的工具对象
- 组件实例的引用（如 `new Chart()`）

### 10.1.5 toRaw（获取原始对象）

`toRaw` 可以从 Proxy 响应式对象中提取出"原始对象"——也就是被 Vue 包装之前的那个原始对象。

```typescript
import { reactive, toRaw } from 'vue'

const state = reactive({
  count: 0,
  name: '小明'
})

const raw = toRaw(state)
console.log(raw === state)  // false —— 是两个不同的引用
console.log(raw.count)     // 0 —— 可以正常访问

// 修改 raw 不会触发响应式更新（绕过了 Proxy）
raw.count = 999
console.log(state.count)  // 0 —— 响应式对象没有变
```

`toRaw` 的使用场景不多，但在某些需要**绕过响应式直接操作对象**的场景下会用到（比如你需要直接修改某个属性但不触发更新，或者需要把对象传给不支持 Proxy 的第三方库）。

## 10.2 Template Refs（获取 DOM）

### 10.2.1 传统 ref 绑定 DOM

`ref` 除了创建响应式数据，还能用来**获取 DOM 元素或子组件实例**——这就是 Template Ref。

```vue
<script setup>
import { ref, onMounted } from 'vue'

// 声明一个 ref，类型是 HTMLDivElement
const containerRef = ref<HTMLDivElement | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)

onMounted(() => {
  // DOM 元素在 onMounted 之后才能访问
  console.log(containerRef.value)  // <div> 元素
  console.log(inputRef.value)     // <input> 元素

  // 获取焦点
  inputRef.value?.focus()
  // 获取尺寸
  const rect = containerRef.value?.getBoundingClientRect()
  console.log('container 宽度：', rect?.width)
})
</script>

<template>
  <div ref="containerRef" class="container">
    <input ref="inputRef" type="text" placeholder="自动聚焦" />
  </div>
</template>
```

### 10.2.2 useTemplateRef（Vue 3.5+ 新 API）

Vue 3.5 引入了 `useTemplateRef`，简化了模板 ref 的获取——不需要在 `<script setup>` 里声明 ref 变量，只需要指定 ref 名称即可。

```vue
<script setup>
import { useTemplateRef, onMounted } from 'vue'

// 不需要 ref()！直接用 useTemplateRef
// 'myDiv' 是 ref 的名字，要和模板里 ref 属性绑定的变量名一致
const myDiv = useTemplateRef<HTMLDivElement>('myDiv')

onMounted(() => {
  console.log(myDiv.value)  // DOM 元素
})
</script>

<template>
  <!-- ref="myDiv" 对应 useTemplateRef('myDiv') -->
  <!-- 注意：在模板里用 camelCase 命名（如 myDiv），Vue 会自动处理 -->
  <div ref="myDiv">Hello</div>
</template>
```

**`useTemplateRef` vs 传统 `ref()` 的区别：**

| | 传统 `ref()` | `useTemplateRef()` |
|---|---|---|
| 需要先声明变量 | `const el = ref(null)` | 无需声明 |
| ref 名和变量名的对应 | 容易拼写不一致 | 声明和使用在一起，不易出错 |
| 适用场景 | 所有场景 | Vue 3.5+ 推荐 |

`useTemplateRef` 的优势是**不需要提前声明 ref 变量**——传统写法容易出现"模板里写了 `ref="xxx"` 但 JS 里变量名拼错了"的 bug，`useTemplateRef` 把声明和使用绑定在一起，减少了出错的可能。

### 10.2.3 绑定组件实例

模板 ref 还可以用来获取**子组件实例**，访问子组件暴露的属性和方法。

```vue
<!-- 子组件：Counter.vue -->
<script setup>
import { ref } from 'vue'

const count = ref(0)

function reset() {
  count.value = 0
}

// 通过 defineExpose 暴露给父组件
defineExpose({ count, reset })
</script>
```

```vue
<!-- 父组件 -->
<script setup>
import { ref } from 'vue'
import Counter from './Counter.vue'

const counterRef = ref<InstanceType<typeof Counter> | null>(null)

function handleReset() {
  counterRef.value?.reset()  // 调用子组件的方法
  console.log(counterRef.value?.count)  // 访问子组件的 count
}
</script>

<template>
  <Counter ref="counterRef" />
  <button @click="handleReset">重置</button>
</template>
```

`InstanceType<typeof Counter>` 是 TypeScript 的语法，用来获取 `Counter` 组件实例的类型。这样 `counterRef.value` 就有正确的类型提示，可以访问 `reset()` 方法和 `count` 属性。

### 10.2.4 常见错误与注意事项

**错误一：在 setup 里访问 ref**

```typescript
setup() {
  const el = ref<HTMLDivElement | null>(null)
  console.log(el.value)  // null —— setup 执行时 DOM 还不存在！

  // 正确做法：在 onMounted 里访问
  onMounted(() => {
    console.log(el.value)  // DOM 元素
  })

  return { el }
}
```

**错误二：ref 名称拼写错误**

```vue
<!-- 模板里：ref="inputRef" -->
<!-- script 里：const inputReff = ref(...) -->  <!-- 拼写不一致！ -->
```

`useTemplateRef`（Vue 3.5+）可以避免这个问题，因为它把名称绑定在一起，拼写错误在编译时就能发现。

## 10.3 reactive 解构与 Vue 3.5 改进

### 10.3.1 reactive 直接解构（Vue 3.5 支持，保持响应式）

在 Vue 3.5 之前，从 reactive 对象解构出来的属性会**丢失响应式**。从 Vue 3.5 开始，`defineProps` 返回的对象解构后保持响应式（前面讲过），但普通 reactive 对象的解构仍然有问题。

```typescript
import { reactive } from 'vue'

const state = reactive({
  count: 0,
  name: '小明'
})

// ❌ Vue 3.5 之前：解构会丢失响应式
// const { count, name } = state
// count++ 不会影响 state.count

// ✅ 正确做法：保持对原始对象的引用
function increment() {
  state.count++  // 直接修改原对象
}

// 或者用 toRefs 转换成多个 ref
import { toRefs } from 'vue'
const { count, name } = toRefs(state)
count.value++  // ✅ 响应式更新
```

### 10.3.2 toRef / toRefs 的使用场景变化

`toRefs` 的核心价值是把 reactive 对象的所有属性变成 ref，从而支持解构后仍然保持响应式：

```typescript
import { reactive, toRefs } from 'vue'

const state = reactive({
  count: 0,
  name: '小明'
})

// toRefs：解构后每个属性都是 ref，和原始对象保持响应式连接
const { count, name } = toRefs(state)

// count.value++ 会更新 state.count
// state.count++ 也会更新 count.value
```

### 10.3.3 Props 解构与 withDefaults 配合（重点）

Props 的解构是 Vue 3.5 的重点改进之一。从 Vue 3.5 开始，`defineProps` 返回的对象可以被安全地解构，且解构后的值保持响应式。

```typescript
// Vue 3.5+：解构 props 保持响应式
const { title, count, items } = defineProps<{
  title: string
  count?: number
  items?: string[]
}>()

// title, count, items 都是响应式的
// 在模板里可以直接用，不需要 props.title
```

**配合 withDefaults 设置默认值：**

```typescript
const { title, count = 0, items = [] } = withDefaults(defineProps<{
  title: string
  count?: number
  items?: string[]
}>(), {
  count: 0,
  items: () => []  // 引用类型必须用函数返回
})

// 在模板里直接用 title, count, items
```

## 10.4 watch 进阶

### 10.4.1 flush 选项（pre / post / sync）

`watch` 默认在组件更新前触发（`flush: 'pre'`）。你可以通过 `flush` 选项调整触发时机：

| flush 值 | 触发时机 | 适用场景 |
|----------|----------|----------|
| `'pre'`（默认） | 组件更新前触发，组件更新多个时只触发一次 | 常规场景 |
| `'post'` | DOM 更新后触发 | 需要访问更新后的 DOM |
| `'sync'` | 数据变化时同步触发（不推荐日常使用） | 需要即时响应 |

```typescript
import { ref, watch } from 'vue'

const inputValue = ref('')

// 默认（pre）：输入时不会立即触发，等输入稳定后才触发
watch(inputValue, (newVal) => {
  console.log('输入值变了：', newVal)
})

// post：DOM 更新后触发，可以访问最新 DOM
const domRef = ref<HTMLDivElement | null>(null)
watch(inputValue, () => {
  // DOM 已经更新完成
  console.log('DOM 内容：', domRef.value?.innerText)
}, { flush: 'post' })
```

### 10.4.2 once 修饰符（Vue 3.5+）

Vue 3.5 引入了 `watch` 的 `.once` 修饰符，让监听器只触发一次后自动停止：

```typescript
import { ref, watch } from 'vue'

const userId = ref(1)

watch(userId, (newId) => {
  console.log('用户 ID 变了：', newId)
  // fetchUser(newId)
}, { once: true })  // 只触发一次，之后自动停止（相当于手动调用了 stop()）
```

### 10.4.3 watch 参数详解（source / callback / options）

`watch` 的完整签名：

```typescript
watch<T>(
  source: () => T,          // getter 函数或 ref/reactive
  callback: (newValue: T, oldValue: T) => void,  // 回调函数
  options?: {                // 可选配置
    immediate?: boolean,     // 是否立即执行
    deep?: boolean,         // 是否深度监听
    flush?: 'pre' | 'post' | 'sync',
    once?: boolean          // Vue 3.5+，只触发一次
  }
)
```

**监听 getter 函数：**

```typescript
// 监听计算属性（getter）
const user = reactive({ name: '小明', age: 25 })

watch(
  () => user.name,  // getter 函数，只监听 user.name 的变化
  (newName, oldName) => {
    console.log(`名字从 ${oldName} 变成了 ${newName}`)
  }
)
```

### 10.4.4 监听多个数据源

`watch` 支持同时监听多个数据源：

```typescript
import { ref, watch } from 'vue'

const firstName = ref('')
const lastName = ref('')

// 监听多个 ref
watch([firstName, lastName], ([newFirst, newLast], [oldFirst, oldLast]) => {
  console.log(`姓名从 ${oldFirst} ${oldLast} 变成了 ${newFirst} ${newLast}`)
})
```

### 10.4.5 Vue 3.5 onWatcherCleanup 清理（重点）

Vue 3.5 的 `onWatcherCleanup` API 让 watch 回调里的清理逻辑更清晰：

```typescript
import { ref, watch, onWatcherCleanup } from 'vue'

const searchQuery = ref('')

watch(searchQuery, async (query) => {
  // 创建取消控制器
  const controller = new AbortController()

  // 注册清理函数 —— watch 重新触发或停止时调用
  onWatcherCleanup(() => {
    controller.abort()  // 取消还在进行的请求
  })

  try {
    const data = await fetch(`/api/search?q=${query}`, {
      signal: controller.signal
    }).then(r => r.json())

    console.log('搜索结果：', data)
  } catch (err) {
    if ((err as Error).name !== 'AbortError') {
      console.error('请求失败：', err)
    }
  }
})
```

## 10.5 nextTick 与 DOM 更新

### 10.5.1 DOM 异步更新机制

Vue 的 DOM 更新是**异步**的——当响应式数据变化时，Vue 不会立即更新 DOM，而是把更新操作放到一个**队列**里，然后在下一个微任务（microtask）中批量执行。

```typescript
import { ref } from 'vue'

const count = ref(0)

// 连续修改数据
count.value++
count.value++
count.value++
// 此时 DOM 还没有更新！

// 访问 DOM 的最新值，需要等 nextTick
console.log(document.querySelector('p')?.textContent)  // 旧值

// 正确做法：等 nextTick
import { nextTick } from 'vue'
count.value++
count.value++
count.value++

nextTick(() => {
  console.log(document.querySelector('p')?.textContent)  // 最新值
})
```

### 10.5.2 nextTick 原理（微任务队列）

`nextTick` 的实现依赖于 JavaScript 的微任务队列。它把回调函数包装成一个 Promise（或者用 `queueMicrotask`），在当前宏任务结束后、下一个宏任务开始前执行。

```typescript
// nextTick 的等价实现
function nextTick(callback?: () => void) {
  return Promise.resolve().then(callback)
}

// 或者更精确的实现（Vue 实际用的是 MessageChannel / queueMicrotask）
queueMicrotask(callback)
```

这就是为什么 `nextTick` 总是在 DOM 更新后执行——因为 Vue 把 DOM 更新操作也放到了微任务队列里，而 `nextTick` 的回调会在所有 DOM 更新任务之后执行。

### 10.5.3 实际场景（聚焦、滚动、获取最新 DOM）

`nextTick` 最常用的三个场景：

```typescript
import { ref, nextTick } from 'vue'

// 场景一：表单验证后聚焦到第一个错误字段
async function validateForm() {
  errors.value = await runValidation()
  if (errors.value.length > 0) {
    await nextTick()
    // DOM 已经更新，可以聚焦
    const firstErrorInput = document.querySelector('.input-error')
    ;(firstErrorInput as HTMLInputElement)?.focus()
  }
}

// 场景二：数据更新后滚动到列表底部
async function loadMoreComments() {
  comments.value.push(...newComments)
  await nextTick()
  // DOM 更新后，滚动到底部
  scrollContainer.value?.scrollTo({
    top: scrollContainer.value.scrollHeight,
    behavior: 'smooth'
  })
}

// 场景三：获取动态生成的元素的尺寸
async function measureElement() {
  show.value = true  // 显示一个之前隐藏的元素
  await nextTick()
  const height = containerRef.value?.offsetHeight
  console.log('元素高度：', height)
}
```

## 10.6 辅助 API

### 10.6.1 isRef / unref / isProxy / isReactive / isReadonly

Vue 提供了一系列**类型判断**工具函数，帮助你检查一个值是什么类型：

```typescript
import { ref, reactive, readonly, isRef, isProxy, isReactive, isReadonly, unref } from 'vue'

const count = ref(0)
const state = reactive({ name: '小明' })
const ro = readonly(state)

isRef(count)      // true —— count 是 ref
isRef(state)      // false —— state 是 reactive，不是 ref
isProxy(state)     // true —— state 是 Proxy（reactive 返回的就是 Proxy）
isReactive(state) // true —— 是 reactive 的 Proxy
isReadonly(ro)    // true —— 是 readonly 的 Proxy

// unref：如果值是 ref，返回 .value；否则直接返回值
const a = ref(10)
const b = 20
console.log(unref(a))  // 10
console.log(unref(b))  // 20
```

### 10.6.2 toRef / toRefs / toRaw

```typescript
import { reactive, toRef, toRefs, toRaw } from 'vue'

const state = reactive({ count: 0, name: '小明' })

// toRef：从 reactive 对象取单个属性变成 ref
const countRef = toRef(state, 'count')
countRef.value++  // state.count 变成 1

// toRefs：把整个对象变成多个 ref
const { count, name } = toRefs(state)
count.value++  // state.count 变成 2

// toRaw：获取原始对象（绕过 Proxy）
const raw = toRaw(state)
raw.count = 999  // 不会触发响应式更新
```

### 10.6.3 customRef（自定义响应式）

`customRef` 允许你**自定义**响应式的追踪和触发逻辑——这在实现一些特殊的响应式行为时非常有用，比如防抖 ref。

```typescript
import { customRef } from 'vue'

// 创建一个防抖的 ref：只在停止输入 500ms 后才触发更新
function useDebouncedRef<T>(initialValue: T, delay = 500) {
  let timeout: ReturnType<typeof setTimeout>

  return customRef((track, trigger) => {
    return {
      get() {
        track()  // 告诉 Vue：这个值需要被追踪
        return initialValue
      },
      set(value: T) {
        clearTimeout(timeout)
        timeout = setTimeout(() => {
          initialValue = value
          trigger()  // 告诉 Vue：触发更新
        }, delay)
      }
    }
  })
}

// 使用这个自定义 ref
const searchQuery = useDebouncedRef('', 300)
```

`track()` 必须在 `get` 里调用，告诉 Vue "这个值在 `get` 里被读取了，需要追踪它的变化"。`trigger()` 在 `set` 里调用，告诉 Vue "值变了，需要重新渲染"。

## 10.7 应用级 API（createApp）

### 10.7.1 app.use（插件注册）

`app.use()` 用来注册 Vue **插件**。插件是一个包含 `install` 方法的对象（或者是一个返回 Promise 的函数），它可以在应用实例上注册全局功能。

```typescript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

const app = createApp(App)

// 注册路由插件
app.use(router)

// 注册 Pinia 状态管理插件
app.use(createPinia())

// 注册自定义插件
app.use({
  install(app) {
    // 全局组件注册
    app.component('MyGlobalButton', MyButton)
    // 全局指令注册
    app.directive('focus', FocusDirective)
    // 全局 mixin（不推荐）
    app.mixin({ /* ... */ })
    // 应用级别的配置
    app.config.globalProperties.$myUtils = { /* ... */ }
  }
})

app.mount('#app')
```

### 10.7.2 app.component / app.directive（全局组件/指令注册）

```typescript
import { createApp } from 'vue'
import App from './App.vue'
import MyButton from './components/MyButton.vue'
import myFocus from './directives/myFocus'

const app = createApp(App)

// 全局注册组件（不需要 import 就能在模板里用）
app.component('MyButton', MyButton)

// 全局注册自定义指令
app.directive('focus', myFocus)
app.directive('click-outside', ClickOutsideDirective)

// 一次性注册多个
app
  .component('HeaderNav', HeaderNav)
  .component('FooterNav', FooterNav)
  .component('SideBar', SideBar)
  .directive('resize', ResizeDirective)

app.mount('#app')
```

### 10.7.3 app.mount / app.unmount（挂载与卸载）

```typescript
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

// 挂载到 #app
app.mount('#app')

// 卸载（从 DOM 中移除应用实例）
// app.unmount()
```

### 10.7.4 app.config（全局配置）

```typescript
const app = createApp(App)

// 全局错误处理器
app.config.errorHandler = (err, instance, info) => {
  console.error('全局错误：', err)
  console.error('组件实例：', instance)
  console.error('错误信息：', info)
}

// 警告处理器（开发环境）
app.config.warnHandler = (msg, instance, trace) => {
  // 可以压制某些警告
  if (msg.includes('Avoided redundant Vue')) return
  console.warn(msg)
}

// 是否启用性能分析
app.config.performance = true  // 需要 Vue 3.2+ 并开启 devtools

// 全局属性（类似 Vue 2 的 Vue.prototype）
app.config.globalProperties.$myUtils = {
  formatDate: (date: Date) => date.toLocaleDateString()
}

// 是否允许开发者工具
app.config.devtools = true

app.mount('#app')
```

### 10.7.5 app.provide / app.version

```typescript
import { createApp, inject } from 'vue'
import App from './App.vue'

const app = createApp(App)

// 在应用级别 provide 数据（所有后代组件都能 inject）
app.provide('user', reactive({ name: '小明', role: 'admin' }))
app.provide('appVersion', '1.0.0')

// 访问 Vue 版本号
console.log(app.version)  // 3.4.x

app.mount('#app')

// 在组件里使用
// const user = inject('user')
```

---

## 本章小结

本章我们深入了 Vue 3 响应式系统的"高级 API"：

- **shallowRef / shallowReactive**：浅层响应式，只追踪第一层变化，用于优化大数据量场景。
- **readonly / markRaw**：只读和绕过响应式，用于不可变数据和第三方库实例。
- **toRaw**：获取 Proxy 背后的原始对象，绕过响应式直接操作。
- **模板 ref**：用 ref 获取 DOM 元素和子组件实例，`useTemplateRef`（Vue 3.5+）简化了这个过程。
- **watch 进阶**：`flush` 控制触发时机，`once` 只触发一次，`onWatcherCleanup` 处理清理逻辑。
- **nextTick**：等待 DOM 异步更新完成后执行回调，原理是基于微任务队列。
- **辅助 API**：isRef / isProxy / isReactive / isReadonly / toRaw / toRef / toRefs / customRef。
- **应用级 API**：createApp 的插件注册、全局组件/指令注册、全局配置、app.provide。

下一章我们会学习 **Composables（组合式函数）**——这是 Vue 3 最核心的代码复用模式，也是 Vue 社区最活跃的领域之一！

