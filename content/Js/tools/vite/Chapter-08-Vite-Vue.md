

+++
title = "第8章 Vite + Vue 实战"
weight = 80
date = "2026-03-27T17:13:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter-08-Vite-Vue

# 第8章：Vite + Vue 实战

> 如果说 Vue 3 是尤雨溪的得意之作，那 Vite 就是让 Vue 开发者"爽到飞起"的利器。两者的结合，堪称"天作之合"。
>
> 这一章，我们来一场 Vue 3 + Vite 的"深度游"：从项目创建开始，到 Vue Router 路由配置，再到 Pinia 状态管理，最后到开发最佳实践... 每一个环节都不放过。
>
> 准备好了吗？让我们一起打造一个真正的 Vue 3 应用！💪

---

## 8.1 Vue 项目创建

### 8.1.1 使用 create-vue 脚手架

`create-vue` 是 Vue 官方推荐的脚手架工具，专门用于创建 Vue 3 项目。它比 `npm create vite@latest -- --template vue` 更 Vue 专属，提供了一些额外的选项：

**创建项目**：

```bash
# 使用 pnpm（推荐）
pnpm create vue@latest my-vue-app

# 使用 npm
npm create vue@latest my-vue-app

# 使用 yarn
yarn create vue my-vue-app
```

**创建过程中的选项**：

```
Vue.js - 欢迎使用 create-vue向导

? 项目名称：my-vue-app
? 添加 TypeScript？ 否 / 是
? 添加 JSX 支持？ 否 / 是
? 添加 Vue Router？ 否 / 是
? 添加 Pinia？ 否 / 是
? 添加 Vitest？ 否 / 是
? 添加 ESLint？ 否 / 是
? 添加 Prettier？ 否 / 是
```

> 💡 **推荐配置**：对于学习目的，选择"否"（不添加），后续可以自己添加。对于实际项目，建议添加 TypeScript + Vue Router + Pinia。

**交互式创建的完整流程**：

```bash
pnpm create vue@latest my-vue-app

# 回答问题
✔ 项目名称：my-vue-app
✔ 添加 TypeScript：是
✔ 添加 JSX 支持：否
✔ 添加 Vue Router：是
✔ 添加 Pinia：是
✔ 添加 Vitest（单元测试）：否
✔ 添加 ESLint + Prettier：否

# 创建完成后
cd my-vue-app
pnpm install
pnpm dev
```

### 8.1.2 使用 Vite 官方模板

如果不需要 create-vue 的额外选项，可以直接用 Vite 的 Vue 模板：

```bash
# 创建项目
pnpm create vite@latest my-vite-vue -- --template vue

# 安装依赖
cd my-vite-vue
pnpm install

# 启动开发服务器
pnpm dev
```

### 8.1.3 项目结构解析

一个典型的 Vue 3 + Vite 项目结构：

```
my-vue-app/
├── public/                    # 静态资源目录
│   └── favicon.ico            # 网站图标
│
├── src/
│   ├── assets/               # 资源目录
│   │   └── logo.svg          # Vue logo
│   │
│   ├── components/           # 公共组件
│   │   ├── TheWelcome.vue
│   │   ├── WelcomeItem.vue
│   │   └── icons/
│   │       └── IconCommunity.vue
│   │
│   ├── views/                # 页面组件
│   │   ├── HomeView.vue
│   │   └── AboutView.vue
│   │
│   ├── router/               # 路由配置
│   │   └── index.js
│   │
│   ├── stores/               # Pinia 状态管理
│   │   └── counter.js
│   │
│   ├── App.vue              # 根组件
│   ├── main.js              # 入口文件
│   └── main.css             # 全局样式
│
├── index.html               # 入口 HTML
├── vite.config.js           # Vite 配置
├── package.json             # 项目配置
└── tsconfig.json            # TypeScript 配置（如果使用 TS）
```

---

## 8.2 Vue 单文件组件（SFC）

### 8.2.1 .vue 文件结构

Vue 单文件组件（`.vue` 文件）是 Vue 3 的核心，它把模板、逻辑和样式封装在一个文件里：

```vue
<!-- 1. 模板（Template）：HTML 结构 -->
<template>
  <div class="container">
    <h1>{{ title }}</h1>
    <button @click="handleClick">点击我</button>
  </div>
</template>

<!-- 2. 逻辑（Script）：JavaScript/TypeScript 代码 -->
<script setup>
// 使用 setup 语法糖，代码更简洁
import { ref, computed, onMounted } from 'vue'

// 定义响应式数据
const title = ref('Hello Vue 3!')
const count = ref(0)

// 计算属性
const doubled = computed(() => count.value * 2)

// 方法
function handleClick() {
  count.value++
  console.log(`点击了！count = ${count.value}`)  // 点击了！count = 1
}

// 生命周期钩子
onMounted(() => {
  console.log('组件已挂载')  // 组件已挂载
})
</script>

<!-- 3. 样式（Style）：CSS/SCSS -->
<style scoped>
/* scoped 表示样式只在当前组件生效 */
.container {
  text-align: center;
  padding: 20px;
}

h1 {
  color: #42b983;
  font-size: 2rem;
}

button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #3aa876;
}
</style>
```

### 8.2.2 模板语法与响应式

Vue 3 的模板语法简洁而强大：

```vue
<template>
  <div class="app">
    <!-- 文本插值 -->
    <p>你好，{{ name }}！</p>
    
    <!-- HTML 渲染（需要谨慎使用，防止 XSS） -->
    <div v-html="rawHtml"></div>
    
    <!-- 属性绑定 -->
    <img :src="imageUrl" :alt="imageAlt" class="avatar">
    
    <!-- 动态属性名 -->
    <button :[attrName]="attrValue">动态属性按钮</button>
    
    <!-- 事件绑定 -->
    <button @click="handleClick">点击</button>
    <form @submit.prevent="handleSubmit">
      <input @keyup.enter="handleEnter">
    </form>
    
    <!-- 条件渲染 -->
    <p v-if="showMessage">消息显示</p>
    <p v-else>消息隐藏</p>
    
    <!-- v-show（display 控制 vs v-if（DOM 控制） -->
    <p v-show="isVisible">v-show 示例</p>
    
    <!-- 列表渲染 -->
    <ul>
      <li v-for="(item, index) in items" :key="item.id">
        {{ index + 1 }}. {{ item.name }}
      </li>
    </ul>
    
    <!-- 双向绑定 -->
    <input v-model="inputValue" type="text">
    <p>输入的内容：{{ inputValue }}</p>
    
    <!-- 计算属性 -->
    <p>计算后的值：{{ computedValue }}</p>
    
    <!-- 监听器 -->
    <p>原始值：{{ message }}</p>
    <p>反转值：{{ reversedMessage }}</p>
    
    <!-- 条件组 -->
    <template v-if="isLoggedIn">
      <span>欢迎回来！</span>
      <button @click="logout">退出</button>
    </template>
    <template v-else>
      <button @click="login">登录</button>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// 数据
const name = '小明'
const rawHtml = '<strong>粗体文本</strong>'
const imageUrl = 'https://via.placeholder.com/150'
const imageAlt = '占位图'
const attrName = 'data-id'
const attrValue = '123'

// 响应式数据
const showMessage = ref(true)
const isVisible = ref(true)
const items = ref([
  { id: 1, name: '苹果' },
  { id: 2, name: '香蕉' },
  { id: 3, name: '橙子' },
])
const inputValue = ref('')
const message = ref('Hello')

// 计算属性
const computedValue = computed(() => {
  return inputValue.value.length * 2
})

// 监听器
const reversedMessage = ref('')
watch(message, (newVal) => {
  reversedMessage.value = newVal.split('').reverse().join('')
}, { immediate: true })

// 方法
function handleClick() {
  console.log('按钮点击')
}

function handleSubmit() {
  console.log('表单提交')
}

function handleEnter() {
  console.log('按下了回车键')
}

// 条件渲染
const isLoggedIn = ref(false)
function login() { isLoggedIn.value = true }
function logout() { isLoggedIn.value = false }
</script>

<style scoped>
.app {
  padding: 20px;
  font-family: -apple-system, sans-serif;
}
.avatar {
  width: 150px;
  height: 150px;
  border-radius: 8px;
}
</style>
```

### 8.2.3 组合式 API（Composition API）

组合式 API 是 Vue 3 最重要的特性之一，它比 Options API 更灵活、更易复用：

```vue
<template>
  <div class="user-profile">
    <h2>{{ user.name }}</h2>
    <p>年龄：{{ user.age }}</p>
    <p>城市：{{ user.city }}</p>
    
    <button @click="updateUser">更新用户</button>
    <button @click="resetUser">重置</button>
    
    <div class="posts">
      <h3>文章列表</h3>
      <div v-for="post in posts" :key="post.id" class="post">
        <h4>{{ post.title }}</h4>
        <p>{{ post.content }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// 1. 导入需要的函数
import { ref, reactive, computed, watch, onMounted, onUpdated, onUnmounted } from 'vue'

// 2. 定义响应式数据
// ref：用于基本类型（String、Number、Boolean）
const name = ref('张三')
const age = ref(25)

// reactive：用于对象类型
const user = reactive({
  name: '张三',
  age: 25,
  city: '北京',
})

// ref 用于对象也可以（需要 .value 访问）
const userRef = ref({
  name: '李四',
  age: 30,
})

// 3. 计算属性
const isAdult = computed(() => {
  return user.age >= 18
})

const userSummary = computed(() => {
  return `${user.name}，${user.age}岁，住在${user.city}`
})

// 4. 方法
function updateUser() {
  user.name = '王五'
  user.age = 35
  user.city = '上海'
}

function resetUser() {
  user.name = '张三'
  user.age = 25
  user.city = '北京'
}

// 5. 监听器
// 监听基本类型
watch(age, (newVal, oldVal) => {
  console.log(`年龄从 ${oldVal} 变成了 ${newVal}`)
})

// 监听对象（深度监听）
watch(user, (newVal) => {
  console.log('用户信息变化了：', newVal)
}, { deep: true })

// 监听计算属性
watch(isAdult, (newVal) => {
  console.log(`成年状态变化：${newVal}`)
})

// 6. 生命周期钩子
onMounted(() => {
  console.log('组件挂载完成')
  document.title = `用户：${user.name}`
})

onUpdated(() => {
  console.log('组件更新了')
})

onUnmounted(() => {
  console.log('组件卸载了')
})

// 7. 提供给模板使用的"导出"
/*
 * 所有在 <script setup> 中定义的变量和方法
 * 都会自动暴露给模板
 */
</script>

<style scoped>
.user-profile {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.post {
  border: 1px solid #ddd;
  padding: 15px;
  margin: 10px 0;
  border-radius: 8px;
}

button {
  margin-right: 10px;
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #3aa876;
}
</style>
```

### 8.2.4 `<script setup>` 语法糖

`<script setup>` 是 Vue 3.2+ 引入的语法糖，让组合式 API 的使用更加简洁：

```vue
<!-- 普通写法 vs script setup 写法 -->

<!-- 普通写法 -->
<script>
import { ref } from 'vue'

export default {
  setup() {
    const count = ref(0)
    function increment() {
      count.value++
    }
    // 需要 return 才能在模板中使用
    return {
      count,
      increment,
    }
  }
}
</script>

<!-- script setup 写法（更简洁） -->
<script setup>
import { ref } from 'vue'

const count = ref(0)
function increment() {
  count.value++
}
// 不需要 return！所有定义的变量和方法自动暴露给模板
</script>
```

**`<script setup>` 的优势**：

```vue
<script setup>
// 1. 更少的样板代码
import { ref, computed, watch } from 'vue'

// 2. 自动暴露给模板（不需要 return）
const name = ref('小明')
const items = ref([1, 2, 3])

// 3. 可以使用 defineProps 和 defineEmits（编译器宏，不需要导入）
const props = defineProps({
  title: String,
  count: {
    type: Number,
    default: 0,
  },
})

const emit = defineEmits(['update', 'delete'])

// 4. 可以定义异步函数
async function fetchData() {
  const response = await fetch('/api/data')
  const data = await response.json()
  return data
}

// 5. 可以使用顶层 await（Vue 3.2+）
const data = await fetchData()

// 6. Ref 在模板中自动解包，不需要 .value
// 模板中可以直接用 {{ name }}，不需要 {{ name.value }}
</script>
```

**defineProps 和 defineEmits**：

```vue
<script setup>
// 运行时声明
const props = defineProps({
  // 基础类型
  title: String,
  
  // 多种类型
  count: [Number, String],
  
  // 带默认值
  name: {
    type: String,
    default: '匿名',
  },
  
  // 必填
  id: {
    type: Number,
    required: true,
  },
  
  // 对象默认值
  user: {
    type: Object,
    default() {
      return { name: '默认用户', age: 0 }
    },
  },
})

// 运行时声明
const emit = defineEmits(['update', 'delete'])

// 带参数验证的 emit
const emitWithValidation = defineEmits({
  update(id: Number) {
    return id > 0
  },
  delete(id: Number) {
    return id > 0
  },
})
</script>
```

**使用 TypeScript 声明**：

```vue
<script setup lang="ts">
// TypeScript 声明（更推荐）
interface User {
  name: string
  age: number
  email?: string
}

const props = defineProps<{
  title: string
  count?: number
  user: User
}>()

const emit = defineEmits<{
  (e: 'update', id: number): void
  (e: 'delete', id: number): void
}>()

// 使用
emit('update', 1)
</script>
```

---

## 8.3 Vue 生态集成

### 8.3.1 Vue Router 配置

Vue Router 是 Vue 官方的路由管理器，用于构建单页面应用（SPA）。

**安装**：

```bash
pnpm add vue-router
```

**创建路由配置**：

```javascript
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// 路由懒加载（推荐）
const Home = () => import('../views/HomeView.vue')
const About = () => import('../views/AboutView.vue')
const UserProfile = () => import('../views/UserProfile.vue')
const UserPosts = () => import('../views/UserPosts.vue')
const NotFound = () => import('../views/NotFound.vue')

const routes = [
  // 首页
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { title: '首页' },
  },
  
  // 关于页
  {
    path: '/about',
    name: 'about',
    component: About,
    meta: { title: '关于' },
  },
  
  // 嵌套路由
  {
    path: '/user/:id',  // 动态路由参数
    name: 'user-profile',
    component: UserProfile,
    props: true,  // 把路由参数作为 props 传递给组件
    meta: { title: '用户资料' },
    children: [
      {
        path: 'posts',  // /user/:id/posts
        name: 'user-posts',
        component: UserPosts,
      },
    ],
  },
  
  // 重定向
  {
    path: '/home',
    redirect: '/',
  },
  
  // 404 页面（必须放在最后）
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: { title: '页面不存在' },
  },
]

const router = createRouter({
  // history 模式：使用 URL 路径（需要服务器配置支持）
  history: createWebHistory(import.meta.env.BASE_URL),
  
  // hash 模式：使用 URL hash（不需要服务器配置）
  // history: createWebHashHistory(),
  
  routes,
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 我的网站` : '我的网站'
  
  // 权限检查（示例）
  // const isLoggedIn = localStorage.getItem('token')
  // if (to.meta.requiresAuth && !isLoggedIn) {
  //   next('/login')
  // } else {
  //   next()
  // }
  
  next()
})

export default router
```

**在 main.js 中注册**：

```javascript
// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)

app.mount('#app')
```

**在 App.vue 中使用**：

```vue
<template>
  <div id="app">
    <!-- 导航链接 -->
    <nav>
      <router-link to="/">首页</router-link>
      <router-link to="/about">关于</router-link>
      <router-link :to="{ name: 'user-profile', params: { id: 1 }}">
        用户资料
      </router-link>
    </nav>
    
    <!-- 路由出口 -->
    <router-view v-slot="{ Component, route }">
      <!-- 缓存组件，提高性能 -->
      <keep-alive :include="['Home']">
        <component :is="Component" :key="route.path" />
      </keep-alive>
    </router-view>
  </div>
</template>

<script setup>
</script>

<style>
#app {
  font-family: -apple-system, sans-serif;
}

nav {
  padding: 20px;
}

nav a {
  margin-right: 15px;
  text-decoration: none;
  color: #42b983;
}

nav a.router-link-active {
  font-weight: bold;
}
</style>
```

### 8.3.2 Pinia 状态管理

Pinia 是 Vue 官方推荐的新一代状态管理库，比 Vuex 更简单、更 TypeScript 友好。

**安装**：

```bash
pnpm add pinia
```

**创建 Store**：

```javascript
// src/stores/counter.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  // ===== 状态 =====
  const count = ref(0)
  const userName = ref('小明')
  const todos = ref([
    { id: 1, text: '学习 Vue 3', done: true },
    { id: 2, text: '学习 Vite', done: false },
    { id: 3, text: '学习 Pinia', done: false },
  ])

  // ===== 计算属性 =====
  const doubleCount = computed(() => count.value * 2)
  const completedTodos = computed(() => todos.value.filter(t => t.done))
  const pendingTodos = computed(() => todos.value.filter(t => !t.done))
  const totalTodos = computed(() => todos.value.length)

  // ===== 方法 =====
  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function reset() {
    count.value = 0
  }

  function addTodo(text) {
    todos.value.push({
      id: Date.now(),
      text,
      done: false,
    })
  }

  function toggleTodo(id) {
    const todo = todos.value.find(t => t.id === id)
    if (todo) {
      todo.done = !todo.done
    }
  }

  function removeTodo(id) {
    const index = todos.value.findIndex(t => t.id === id)
    if (index > -1) {
      todos.value.splice(index, 1)
    }
  }

  // ===== 返回 =====
  return {
    // 状态
    count,
    userName,
    todos,
    // 计算属性
    doubleCount,
    completedTodos,
    pendingTodos,
    totalTodos,
    // 方法
    increment,
    decrement,
    reset,
    addTodo,
    toggleTodo,
    removeTodo,
  }
})
```

**在组件中使用**：

```vue
<template>
  <div class="counter-app">
    <h1>计数器应用</h1>
    
    <!-- 状态 -->
    <p>用户名：{{ counterStore.userName }}</p>
    <p>计数：{{ counterStore.count }}</p>
    <p>双倍计数：{{ counterStore.doubleCount }}</p>
    
    <!-- 操作按钮 -->
    <div class="buttons">
      <button @click="counterStore.decrement">-</button>
      <button @click="counterStore.increment">+</button>
      <button @click="counterStore.reset">重置</button>
    </div>
    
    <!-- Todo 列表 -->
    <div class="todos">
      <h2>待办事项 ({{ counterStore.pendingTodos.length }})</h2>
      
      <div class="add-todo">
        <input 
          v-model="newTodoText" 
          @keyup.enter="handleAddTodo"
          placeholder="添加新待办..."
        >
        <button @click="handleAddTodo">添加</button>
      </div>
      
      <ul>
        <li 
          v-for="todo in counterStore.todos" 
          :key="todo.id"
          :class="{ done: todo.done }"
        >
          <input 
            type="checkbox" 
            :checked="todo.done"
            @change="counterStore.toggleTodo(todo.id)"
          >
          <span>{{ todo.text }}</span>
          <button @click="counterStore.removeTodo(todo.id)">删除</button>
        </li>
      </ul>
      
      <p v-if="counterStore.completedTodos.length > 0">
        已完成：{{ counterStore.completedTodos.length }} / {{ counterStore.totalTodos }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

// 创建 store 实例
const counterStore = useCounterStore()

// 新待办输入
const newTodoText = ref('')

function handleAddTodo() {
  if (newTodoText.value.trim()) {
    counterStore.addTodo(newTodoText.value.trim())
    newTodoText.value = ''
  }
}
</script>

<style scoped>
.counter-app {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.buttons button {
  margin: 0 5px;
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.todos ul {
  list-style: none;
  padding: 0;
}

.todos li {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.todos li.done span {
  text-decoration: line-through;
  color: #999;
}

.todos li span {
  flex: 1;
  margin-left: 10px;
}

.todos li button {
  padding: 4px 8px;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
```

### 8.3.3 Vuex 状态管理（遗留项目）

Vuex 是 Vue 2 时代的官方状态管理库，Vue 3 + Pinia 的组合已经取代了 Vuex + Vue 2 的组合。如果你是在维护一个 Vue 2 项目，可以使用 Vuex 3；如果是 Vue 3 项目，**强烈建议使用 Pinia**。

### 8.3.4 VueUse 工具库

VueUse 是一个实用的 Vue Composition API 工具集，提供了大量好用的组合式函数。

**安装**：

```bash
pnpm add @vueuse/core
```

**使用示例**：

```vue
<template>
  <div class="vueuse-demo">
    <!-- useLocalStorage -->
    <p>存储的值：{{ storedValue }}</p>
    <button @click="updateValue">更新值</button>
    
    <!-- useMouse -->
    <p>鼠标位置：x={{ x }}, y={{ y }}</p>
    
    <!-- useDark -->
    <p>当前主题：{{ isDark ? '深色' : '浅色' }}</p>
    <button @click="toggleDark">切换主题</button>
    
    <!-- useFetch -->
    <div v-if="pending">加载中...</div>
    <div v-else-if="error">错误：{{ error.message }}</div>
    <div v-else>
      <p>数据：{{ data }}</p>
    </div>
    
    <!-- useIntersectionObserver -->
    <div ref="target" class="observe-target">
      观察我
    </div>
    <p v-if="isVisible">元素可见！</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  useLocalStorage, 
  useMouse, 
  useDark, 
  useToggle,
  useFetch,
  useIntersectionObserver,
} from '@vueuse/core'

// useLocalStorage - 本地存储
const storedValue = useLocalStorage('my-key', '默认值')

function updateValue() {
  storedValue.value = `新值 ${Date.now()}`
}

// useMouse - 鼠标位置
const { x, y } = useMouse()

// useDark - 暗色模式
const isDark = useDark()
const toggleDark = useToggle(isDark)

// useFetch - 数据请求
const { data, pending, error } = useFetch('https://jsonplaceholder.typicode.com/todos/1')

// useIntersectionObserver - 元素可见性
const target = ref(null)
const isVisible = ref(false)

useIntersectionObserver(target, ([{ isIntersecting }]) => {
  isVisible.value = isIntersecting
}, { threshold: 0.5 })
</script>

<style scoped>
.observe-target {
  padding: 50px;
  background-color: #eee;
  text-align: center;
  margin: 20px 0;
}
</style>
```

**常用 VueUse 函数速查**：

| 函数 | 说明 |
|------|------|
| `useLocalStorage` | 本地存储响应式封装 |
| `useSessionStorage` | 会话存储响应式封装 |
| `useMouse` | 鼠标位置 |
| `useDark` / `useToggle` | 暗色模式切换 |
| `useFetch` | 数据请求 |
| `useIntersectionObserver` | 元素可见性 |
| `useDebounceFn` | 防抖函数 |
| `useThrottleFn` | 节流函数 |
| `useClipboard` | 剪贴板操作 |
| `useGeolocation` | 地理位置 |
| `useFullscreen` | 全屏模式 |
| `useEventListener` | 事件监听（自动清理） |
| `onClickOutside` | 点击元素外部 |
| `useStorage` | 通用存储 |
| `createGlobalState` | 跨组件共享状态 |

### 8.3.5 Vue I18n 国际化

**安装**：

```bash
pnpm add vue-i18n
```

**配置**：

```javascript
// src/i18n/index.js
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zh from './locales/zh.json'

const i18n = createI18n({
  legacy: false,  // 使用组合式 API
  locale: 'zh',   // 默认语言
  fallbackLocale: 'en',
  messages: {
    en,
    zh,
  },
})

export default i18n
```

```json
// src/i18n/locales/en.json
{
  "hello": "Hello World",
  "welcome": "Welcome to Vue i18n",
  "count": "You clicked {count} times"
}
```

```json
// src/i18n/locales/zh.json
{
  "hello": "你好世界",
  "welcome": "欢迎使用 Vue i18n",
  "count": "你点击了 {count} 次"
}
```

**在组件中使用**：

```vue
<template>
  <div class="i18n-demo">
    <h1>{{ $t('hello') }}</h1>
    <p>{{ $t('welcome') }}</p>
    
    <p>{{ $t('count', { count: clickCount }) }}</p>
    <button @click="clickCount++">点击</button>
    
    <div class="lang-switch">
      <button @click="switchLang('en')">English</button>
      <button @click="switchLang('zh')">中文</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()
const clickCount = ref(0)

function switchLang(lang) {
  locale.value = lang
}
</script>
```

### 8.3.6 Vue Query（TanStack Query Vue）

Vue Query 是用于管理服务端状态（异步数据）的库。

**安装**：

```bash
pnpm add @tanstack/vue-query
```

**配置**：

```javascript
// main.js
import { createApp } from 'vue'
import { VueQueryPlugin } from '@tanstack/vue-query'
import App from './App.vue'

const app = createApp(App)

app.use(VueQueryPlugin)

app.mount('#app')
```

**使用**：

```vue
<template>
  <div class="vue-query-demo">
    <h1>Vue Query 示例</h1>
    
    <div v-if="isPending">加载中...</div>
    <div v-else-if="isError">错误：{{ error.message }}</div>
    <div v-else>
      <div v-for="todo in data" :key="todo.id" class="todo">
        <span :class="{ done: todo.completed }">{{ todo.title }}</span>
      </div>
    </div>
    
    <button @click="refetch">刷新</button>
  </div>
</template>

<script setup>
import { useQuery } from '@tanstack/vue-query'

// 获取数据的函数
async function fetchTodos() {
  const response = await fetch('https://jsonplaceholder.typicode.com/todos?_limit=10')
  if (!response.ok) throw new Error('获取数据失败')
  return response.json()
}

// 使用 useQuery
const { data, isPending, isError, error, refetch, isFetching } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  staleTime: 1000 * 60 * 5,  // 5分钟内不重新获取
})
</script>
```

### 8.3.7 VueMacros（宏扩展）

VueMacros 是 Vue 3 的宏扩展库，提供了更多语法糖。

**安装**：

```bash
pnpm add -D vue-macros
```

---

## 8.4 Vue 开发最佳实践

### 8.4.1 组件组织方式

一个良好的组件组织方式可以提高代码可维护性：

```
src/
├── components/          # 公共组件
│   ├── ui/             # UI 基础组件（Button、Input、Modal）
│   │   ├── BaseButton.vue
│   │   ├── BaseInput.vue
│   │   └── BaseModal.vue
│   ├── layout/         # 布局组件
│   │   ├── AppHeader.vue
│   │   ├── AppSidebar.vue
│   │   └── AppFooter.vue
│   └── common/         # 通用业务组件
│       ├── UserAvatar.vue
│       └── TodoItem.vue
│
├── views/              # 页面组件
│   ├── Home.vue
│   ├── About.vue
│   └── users/
│       ├── UserList.vue
│       └── UserDetail.vue
```

### 8.4.2 自动导入配置

使用 `unplugin-auto-import` 和 `unplugin-vue-components` 自动导入 API 和组件：

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { VueUseAliases } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      imports: ['vue', 'vue-router', 'pinia', '@vueuse/core'],
      dts: 'src/auto-imports.d.ts',
    }),
    Components({
      dirs: ['src/components'],
      dts: 'src/components.d.ts',
      resolvers: [
        VueUseAliases(),
      ],
    }),
  ],
})
```

### 8.4.3 TypeScript 支持

Vue 3 对 TypeScript 的支持非常出色。使用 `<script setup lang="ts">` 可以获得完整的类型安全：

```vue
<script setup lang="ts">
// 定义 Props 类型
interface Props {
  title: string
  count?: number
  items?: string[]
}

// withDefaults 是编译器宏，不需要导入
const props = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => [],
})

// 定义 Emit 类型
const emit = defineEmits<{
  (e: 'update', value: number): void
  (e: 'delete', id: string): void
}>()

// 定义复杂类型
interface User {
  id: number
  name: string
  email?: string
}

const user = ref<User | null>(null)

// 使用 async/await
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
}
</script>
```

### 8.4.4 样式管理方案

**CSS 变量 + Scoped CSS**：

```vue
<script setup>
const theme = {
  primary: '#42b983',
  secondary: '#34495e',
  danger: '#e74c3c',
}
</script>

<style scoped>
/* 使用 CSS 变量 */
.button {
  background-color: v-bind('theme.primary');
  color: white;
}
</style>
```

**CSS Modules**（见第6章）。

### 8.4.5 HMR 不生效问题排查

如果 HMR 不生效，尝试以下步骤：

1. **检查是否支持 HMR**：确保使用的是 Vue 3 + Vite
2. **清除缓存**：删除 `node_modules/.vite` 目录
3. **重启开发服务器**：完全停止 `pnpm dev`，然后重新启动
4. **检查是否有语法错误**：控制台是否有红色报错
5. **检查热更新配置**：

```javascript
// vite.config.js
export default defineConfig({
  server: {
    hmr: {
      overlay: true,  // 显示错误浮层
    },
  },
})
```

### 8.4.6 Vue 3.4+ 新特性

**Vue 3.4 引入的新特性**：

```vue
<script setup>
// 1. defineModel（简化双向绑定）
const modelValue = defineModel()
// 相当于：
// const props = defineProps(['modelValue'])
// const emit = defineEmits(['update:modelValue'])

// defineModel 的第一个参数是 v-model 的名称，第二个参数是 props 选项
// default 需要放在 props 定义中
const title = defineModel({ type: String, default: '默认标题' })

// 2. 更精准的响应式追踪
// Vue 3.4 优化了 ref/reactive 的实现，性能更好

// 3. style scoped 中的 v-bind()
</script>

<template>
  <!-- defineModel 用法 -->
  <input v-model="title">
  <p>标题：{{ title }}</p>
</template>

<style scoped>
/* Vue 3.4 支持在 style 中使用 v-bind */
h1 {
  /* 使用组件中的响应式数据作为 CSS 值 */
  color: v-bind('title');  /* 会根据 title 变量实时更新 */
}
</style>
```

---

## 8.5 本章小结

### 🎉 本章总结

这一章我们完成了 Vue 3 + Vite 的深度实战：

1. **项目创建**：create-vue 脚手架、官方模板、项目结构解析

2. **Vue SFC**：.vue 文件结构、模板语法、响应式基础、组合式 API、`<script setup>` 语法糖

3. **Vue 生态**：Vue Router（动态路由、嵌套路由、路由守卫）、Pinia（状态管理）、VueUse（工具库）、Vue I18n（国际化）、Vue Query（服务端状态）

4. **开发最佳实践**：组件组织、自动导入、TypeScript 支持、样式管理、HMR 排查、Vue 3.4+ 新特性

5. **实战项目**：构建了一个 Todo 应用，涵盖计数器、待办列表、本地存储

### 📝 本章练习

1. **创建项目**：用 `pnpm create vue@latest` 创建一个完整的 Vue 3 项目

2. **Todo 应用**：动手实现一个完整的 Todo 应用，包含增删改查功能

3. **路由嵌套**：实现一个用户管理页面，包含用户列表和用户详情

4. **Pinia Store**：把 Todo 应用的状态管理迁移到 Pinia

5. **VueUse 实战**：在项目中使用 VueUse 的几个常用函数

---

> 📌 **预告**：下一章我们将学习 **Vite + React 实战**，包括 React 项目创建、React 18 新特性、React Router、Zustand 状态管理等。敬请期待！
