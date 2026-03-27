+++
title = "第9章 setup 与 script setup"
weight = 90
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第九章 setup 与 script setup

> Composition API 是 Vue 3 的核心编程范式，而 setup 函数和 script setup 则是 Composition API 的主战场。这一章我们会深入理解 setup 的执行时机、this 的行为、返回值的作用，以及 script setup 这个编译器语法糖带来的便利。掌握这一章，你才算真正"会用" Vue 3。

## 9.1 setup() 函数

### 9.1.1 执行时机（在 created 之前，data/props 已初始化）

`setup` 是 Vue 3 Composition API 的入口函数，它在组件实例创建后、`beforeCreate` 钩子之前执行。此时，组件的 `props` 已经初始化完成，可以访问 `props`，但 `data`、`computed`、`methods` 等还没有初始化。

```mermaid
flowchart LR
    A["new Vue()<br/>实例创建"] --> B["setup()<br/>Composition API 入口"]
    B --> C["beforeCreate()"]
    C --> D["created()"]
    D --> E["template 编译<br/>render 函数"]
    E --> F["挂载到 DOM"]
    
    style B fill:#42b883,color:#fff
```

这意味着：**在 setup 里，不能访问 `this.data`**（因为 data 还没初始化），也不能调用 `this.xxx` 方法。但可以访问 `props`（作为 `setup` 的第一个参数）。

```typescript
import { ref } from 'vue'

export default {
  props: ['userId'],

  setup(props) {
    // props 已经可以用了
    console.log(props.userId)  // 父组件传过来的 userId

    // 不能访问 data 里定义的数据（data 还没初始化）
    // console.log(this.username)  // undefined 或报错

    // 不能调用 methods 里定义的方法
    // this.handleSubmit()  // 不能用

    const username = ref('小明')  // 可以用 ref
    return { username }
  },

  data() {
    return {
      // 这里的 username 和 setup 里的 username 不是同一个！
      username: '张三'
    }
  },

  mounted() {
    // mounted 里可以访问 both
    console.log('setup 里的 username:', this.username)  // undefined（setup 里的 username 不在 this 上）
    console.log('data 里的 username:', this.username)    // 张三
  }
}
```

### 9.1.2 setup 中的 this（undefined）

在 `setup` 函数里，`this` 是 **`undefined`**——它不指向组件实例。这和 Vue 2 的 Options API（`this` 指向组件实例）完全不同。

为什么这样设计？因为 Composition API 鼓励你用**组合式**的思维写代码——你不需要 `this`，因为数据和方法都直接定义在 `setup` 的作用域里。

```typescript
export default {
  setup() {
    console.log(this)  // undefined —— 不要再用 this 了！
    
    // 响应式数据直接定义
    const count = ref(0)

    // 方法直接定义
    function increment() {
      count.value++
    }

    // 计算属性直接定义
    import { computed } from 'vue'
    const doubled = computed(() => count.value * 2)

    // 生命周期钩子直接调用
    import { onMounted } from 'vue'
    onMounted(() => {
      console.log('mounted 了，count 是', count.value)
    })

    return { count, increment, doubled }
  }
}
```

### 9.1.3 setup 的返回值

`setup` 函数要么不返回值，要么返回一个**对象**。返回的对象上的属性会在模板里直接可用。

```typescript
setup(props) {
  const count = ref(0)
  const message = 'Hello'

  function handleClick() {
    count.value++
  }

  // setup 返回的对象，模板里可以直接用
  return {
    count,         // count 可以在模板里用 {{ count }}
    message,       // message 可以在模板里用 {{ message }}
    handleClick    // handleClick 可以在模板里用 @click="handleClick"
  }
}
```

**setup 不返回值时，模板里无法访问 setup 里定义的变量。**

```typescript
// 常见错误：忘记 return
setup() {
  const secret = ref('我的秘密')  // 模板里用不了这个！
  // forgot to return secret
}

// 正确做法：
setup() {
  const secret = ref('我的秘密')
  return { secret }  // 必须在 return 里暴露，模板才能用
}
```

**setup 返回函数 vs 返回对象：**

setup 可以返回一个**渲染函数**，用于完全控制组件的渲染方式（类似 React 的 render 函数）：

```typescript
import { h } from 'vue'

export default {
  setup() {
    const count = ref(0)

    // 返回渲染函数时，模板里的内容会被忽略
    return () => h('div', { class: 'counter' }, [
      h('span', {}, count.value),
      h('button', { onClick: () => count.value++ }, '+1')
    ])
  }
}
```

实际开发中，99% 的情况下我们用返回对象的方式，不需要返回渲染函数。

## 9.2 script setup 语法

### 9.2.1 为什么推荐 script setup

`<script setup>` 是 Vue 3.2 引入的一个**编译器语法糖**——它让 `setup` 函数的写法变得更简洁。

**普通 `<script>` + `setup` 写法：**

```vue
<script>
import { ref } from 'vue'

export default {
  setup() {
    const count = ref(0)
    function increment() {
      count.value++
    }
    return { count, increment }
  }
}
</script>
```

**`<script setup>` 写法（更简洁）：**

```vue
<script setup>
import { ref } from 'vue'

const count = ref(0)

function increment() {
  count.value++
}

// 不需要 return！模板里可以直接用 count 和 increment
</script>
```

**`<script setup>` 的优势：**

1. **更少样板代码**：不需要写 `export default {}`，不需要 `return`
2. **编译器宏自动可用**：`defineProps`、`defineEmits`、`defineExpose` 等宏不需要 import
3. **性能更好**：编译器会对 `<script setup>` 做更多优化，减少运行时开销
4. **IDE 支持更好**：VS Code + Volar 插件对 `<script setup>` 的类型推断更准确

### 9.2.2 编译器宏（defineProps / defineEmits / defineExpose / defineOptions / defineSlots）

Vue 3.2+ 在 `<script setup>` 里内置了五个编译器宏，它们不需要 import，会在编译时自动转换。

**`defineProps`**：声明组件接收的 props。

```vue
<script setup>
// 编译器宏，不需要 import
const props = defineProps<{
  title: string
  count?: number
}>()

// props 是一个响应式对象
console.log(props.title)
</script>
```

**`defineEmits`**：声明组件会触发的事件。

```vue
<script setup>
const emit = defineEmits<{
  (e: 'update', value: string): void
  (e: 'delete', id: number): void
}>()

emit('update', 'new value')
</script>
```

**`defineExpose`**：暴露组件实例给父组件（通过 ref）。

默认情况下，父组件通过 `ref` 获取子组件时，只能访问子组件暴露的内容。`<script setup>` 的组件是**默认不暴露任何内容**的，需要用 `defineExpose` 来暴露。

```vue
<!-- 子组件：ChildComponent.vue -->
<script setup>
import { ref } from 'vue'

const count = ref(0)
const message = ref('Hello')

// 暴露 count 和 message 给父组件
defineExpose({ count, message })
</script>
```

```vue
<!-- 父组件 -->
<script setup>
import { ref } from 'vue'
import ChildComponent from './ChildComponent.vue'

const childRef = ref(null)

function showChildData() {
  // childRef.value 是子组件暴露的内容
  console.log(childRef.value?.count)    // 0
  console.log(childRef.value?.message)  // Hello
}
</script>

<template>
  <ChildComponent ref="childRef" />
  <button @click="showChildData">查看子组件数据</button>
</template>
```

**`defineOptions`**：在 `<script setup>` 里设置组件选项（name、inheritAttrs、props、emits 等）。

```vue
<script setup>
import { ref } from 'vue'

// 给组件起名字（如果不写，Vue 会自动从文件名推断）
defineOptions({
  name: 'MyCounter',
  inheritAttrs: false
})

const count = ref(0)
</script>
```

**`defineSlots`**：在 `<script setup>` 里声明插槽类型（用于 TypeScript）。

```vue
<script setup lang="ts">
// 声明组件接受的插槽
defineSlots<{
  default: { message: string }
  header: { title: string }
}>()
</script>

<template>
  <slot name="header" :title="'标题'" />
  <slot :message="'内容'" />
</template>
```

### 9.2.3 使用顶层 await

在 `<script setup>` 里，可以用**顶层 await**（不需要包装在 async 函数里）：

```vue
<script setup>
import { ref } from 'vue'

const user = ref(null)

// 顶层 await：组件 setup 会等待这个 Promise 完成后再完成初始化
// 这在需要服务端预取数据的 SSR 场景下特别有用
const data = await fetch('/api/user').then(res => res.json())
user.value = data
</script>
```

**注意**：使用了顶层 await 的 `<script setup>` 组件会自动变成异步组件，需要配合 `<Suspense>` 或者在父组件里用 `v-if` 来处理加载状态。

### 9.2.4 defineExpose 暴露组件实例

`defineExpose` 在 9.2.2 节已经讲过，这里补充一个实际场景的例子：

```vue
<!-- 子组件：VideoPlayer.vue -->
<script setup>
import { ref } from 'vue'

const videoRef = ref<HTMLVideoElement | null>(null)
const isPlaying = ref(false)

function play() {
  videoRef.value?.play()
  isPlaying.value = true
}

function pause() {
  videoRef.value?.pause()
  isPlaying.value = false
}

function seek(time: number) {
  if (videoRef.value) {
    videoRef.value.currentTime = time
  }
}

// 暴露方法给父组件调用
defineExpose({ play, pause, seek, isPlaying })
</script>

<template>
  <video ref="videoRef" src="..." />
</template>
```

```vue
<!-- 父组件：通过 ref 调用子组件的方法 -->
<script setup>
import { ref } from 'vue'
import VideoPlayer from './VideoPlayer.vue'

const player = ref(null)

function handlePlay() {
  player.value?.play()   // 播放
}

function handlePause() {
  player.value?.pause()  // 暂停
}

function handleSeek() {
  player.value?.seek(30)  // 跳到 30 秒
}
</script>

<template>
  <VideoPlayer ref="player" />
  <button @click="handlePlay">播放</button>
  <button @click="handlePause">暂停</button>
  <button @click="handleSeek">跳到 30 秒</button>
</template>
```

这种"父组件调用子组件方法"的模式常用于：视频播放器、地图组件、富文本编辑器等需要从外部控制的组件。

## 9.3 两种写法的选择

Vue 3 支持两种组件写法：**Options API**（Vue 2 的写法）和 **Composition API**（setup / script setup）。

**`<script setup>`（推荐）：**

- 代码更简洁，样板代码更少
- 逻辑相关性强，方便抽取 Composables
- 性能更好，编译器优化更多
- TypeScript 支持更完善
- 适合：绝大多数场景

**普通 `<script>` + `setup()`：**

- 需要手动 return
- 适合：需要在同一个组件里混用 Options API 和 Composition API（比如迁移老项目）

**纯 Options API（`<script>` 不含 setup）：**

- Vue 2 遗留写法
- 适合：不想学 Composition API 的团队快速迁移
- 不推荐新项目使用

```vue
<!-- 三种写法对比 -->
<!-- 写法一：<script setup>（推荐） -->
<script setup>
import { ref, computed } from 'vue'
const count = ref(0)
const doubled = computed(() => count.value * 2)
</script>

<!-- 写法二：普通 script + setup -->
<script>
import { ref, computed } from 'vue'
export default {
  setup() {
    const count = ref(0)
    const doubled = computed(() => count.value * 2)
    return { count, doubled }
  }
}
</script>

<!-- 写法三：纯 Options API（Vue 2 风格，不推荐新项目用） -->
<script>
export default {
  data() {
    return { count: 0 }
  },
  computed: {
    doubled() {
      return this.count * 2
    }
  }
}
</script>
```

**选择建议：** 新项目无脑选 `<script setup>`。它已经是 Vue 3 的主流写法，社区里的教程、组件库、Composables 几乎都基于 `<script setup>`。掌握它，你就能轻松读懂和复用社区的代码。

---

## 本章小结

本章我们深入理解了 Vue 3 Composition API 的核心入口：

- **`setup()` 函数的执行时机**：在组件实例创建后、beforeCreate 之前，props 已初始化，但 data/methods 还没有。
- **`setup()` 里的 `this` 是 undefined**：Composition API 不需要 `this`，数据和逻辑直接定义在 setup 作用域里。
- **`setup()` 的返回值**：返回的对象属性在模板里直接可用；也可以返回渲染函数来完全控制渲染。
- **`<script setup>` 语法糖**：`defineProps`、`defineEmits`、`defineExpose`、`defineOptions`、`defineSlots` 等编译器宏让代码更简洁，性能更好。
- **顶层 await**：`<script setup>` 支持顶层 await，方便处理异步数据。
- **两种写法的选择**：新项目推荐 `<script setup>`，性能和开发体验都更好。

下一章我们会深入 **响应式 API 进阶**——shallowRef、shallowReactive、markRaw、toRaw、watch 进阶、nextTick 原理等，这些是 Vue 3 响应式系统的"高级用法"！

