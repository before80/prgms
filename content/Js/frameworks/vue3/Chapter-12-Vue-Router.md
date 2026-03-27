+++
title = "第12章 Vue Router 4"
weight = 120
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十二章 Vue Router 4

> Vue Router 是 Vue 官方出品的路由管理器，它是构建单页应用（SPA）的核心基础设施。当用户在页面上点击链接或改变 URL 时，Vue Router 负责找出匹配的路由规则，并渲染对应的组件。本章会详细介绍 Vue Router 4 的所有核心功能——从基础的路由配置到高级的导航守卫、懒加载和滚动行为控制。

## 12.1 SPA 与路由原理

### 12.1.1 单页面应用概念

传统的多页面应用（MPA）每次切换页面，浏览器都要向服务器请求一个新的 HTML 文件，页面会闪烁、重新加载整个页面。

**单页面应用（SPA）** 只需要一个 HTML 文件，通过 JavaScript 动态地**替换页面内容**来实现"页面切换"——页面永远不刷新，体验流畅，但页面 URL 会变化，给用户"在多个页面之间跳转"的感觉。

```mermaid
flowchart LR
    A["浏览器地址栏<br/>URL 变化"] --> B["Vue Router<br/>监听 URL 变化"]
    B --> C["匹配路由规则<br/>找到对应组件"]
    C --> D["组件切换<br/>页面内容更新"]
    D --> E["URL 历史栈<br/>浏览器后退/前进"]
    
    style A fill:#42b883,color:#fff
    style D fill:#f4a261,color:#fff
```

Vue Router 就是这个"根据 URL 变化渲染对应组件"的机制。它维护了一个 URL 到组件的映射表，当 URL 变化时，Vue Router 找到匹配的组件，渲染到 `<router-view>` 标签的位置。

### 12.1.2 history vs hash 模式

Vue Router 支持两种路由模式：**history 模式**和 **hash 模式**。

**hash 模式**：URL 里带 `#`，比如 `example.com/#/user/123`。`#` 后面的内容叫**哈希（hash）**，浏览器不会把哈希部分发送给服务器——所以即使服务器没有配置任何路由，只要返回 index.html，Vue Router 都能正常工作。

```bash
# hash 模式的 URL
https://example.com/#/user/123
https://example.com/#/products/5
https://example.com/#/about
```

**history 模式**：URL 里没有 `#`，看起来像普通的多页面 URL：

```bash
# history 模式的 URL
https://example.com/user/123
https://example.com/products/5
https://example.com/about
```

history 模式需要服务器配合——因为当用户直接访问 `example.com/user/123` 时，浏览器会向服务器请求 `/user/123` 这个路径的 HTML 文件，服务器如果没有配置，会返回 404。需要在服务器上配置把所有路由都回退到 `index.html`。

### 12.1.3 三种模式对比（hash / history / abstract）

| 模式 | URL 样子 | 是否需要服务器配置 | 微信/内网兼容性 | 推荐场景 |
|------|----------|------------------|--------------|---------|
| hash | `/#/user` | ❌ 不需要 | ✅ 好（内网穿透简单） | 内部工具、简单后台 |
| history | `/user` | ✅ 需要 | ❌ 需要额外配置 | 正式上线项目、对外网站 |
| abstract | 无 URL | N/A | N/A | 非浏览器环境（如 Node.js 测试） |

## 12.2 快速上手

### 12.2.1 安装与引入

```bash
pnpm add vue-router
```

### 12.2.2 基础配置

```typescript
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

// 路由配置数组：每一条记录对应一个 URL → 组件的映射
const routes = [
  {
    path: '/',                        // URL 路径（必填）
    name: 'Home',                     // 路由名称（可选，但推荐写，方便用 name 而非 path 做跳转）
    component: () => import('../views/Home.vue')  // 懒加载：访问 / 时才加载这个组件
    // component: Home                  // 非懒加载写法：直接 import 进来（首屏就会加载）
    // redirect: '/home'               // 重定向：访问 / 时自动跳转到 /home
    // props: true                     // 把 route.params 当作 props 传给组件
    // meta: { requiresAuth: true }    // 自定义数据：权限、标题等（详见路由守卫章节）
    // children: []                    // 子路由：嵌套路由（详见嵌套路由章节）
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  // 动态路由：/:id 匹配任意路径，id 会成为 route.params.id
  {
    path: '/user/:id',              // :id 是动态段，匹配 /user/123、/user/abc 等
    name: 'UserProfile',
    component: () => import('../views/UserProfile.vue')
    // 组件里通过 const route = useRoute(); route.params.id 获取 id 值
  },
  // 通配符：匹配所有未定义的路径（通常用于 404 页面）
  {
    path: '/:pathMatch(.*)*',      // 正则：匹配任意路径
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

// 创建路由实例
const router = createRouter({
  // history：路由模式
  // createWebHistory('/') → History 模式（URL 更美观，适合有服务器配置的项目）
  // createWebHashHistory('/') → Hash 模式（URL 带 #，无需服务器配置，适合静态托管）
  history: createWebHistory(import.meta.env.BASE_URL),
  routes  // routes：路由配置数组，上面的 routes 常量
})

export default router
```

```typescript
// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router)  // 注册路由插件

app.mount('#app')
```

### 12.2.3 router-link 与 router-view

**`<router-link>`**：用于在页面上生成链接，点击时不刷新页面，而是触发路由切换。

```vue
<!-- App.vue -->
<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <nav>
    <!-- router-link 会自动给当前匹配的链接加 .router-link-active class -->
    <RouterLink to="/">首页</RouterLink>
    <RouterLink to="/about">关于</RouterLink>
    <RouterLink to="/user/123">用户</RouterLink>
  </nav>

  <!-- router-view 是路由视图——匹配的组件会渲染在这里 -->
  <RouterView />
</template>
```

**`<RouterLink>` 的属性：**

```vue
<RouterLink
  to="/about"
  replace               <!-- 用 replaceState 而不是 pushState，不留历史记录 -->
  active-class="active" <!-- 自定义激活 class 名（默认是 router-link-active） -->
  exact-active-class="exact-active"  <!-- 精确匹配时的 class -->
>
  关于
</RouterLink>
```

### 12.2.4 useRouter / useRoute 组合式 API

Vue Router 4 提供了两个组合式 API：

```typescript
import { useRoute, useRouter } from 'vue-router'

// useRouter：路由实例，可以编程式导航
const router = useRouter()

// useRoute：当前路由信息（URL 参数、匹配规则等）
const route = useRoute()

// 编程式导航
router.push('/user/123')    // 跳转（会留下历史记录）
router.replace('/about')    // 替换（不留下历史记录）
router.go(-1)              // 后退
router.forward()           // 前进
```

## 12.3 路由定义与参数

### 12.3.1 静态路由

```typescript
const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/contact', component: Contact }
]
```

### 12.3.2 动态路由（params 路径参数）

用冒号 `:` 来定义**动态路径参数**：

```typescript
const routes = [
  // /user/123 匹配这个路由
  { path: '/user/:id', component: UserDetail },

  // 支持多个参数
  { path: '/user/:userId/post/:postId', component: PostDetail },

  // 参数可选
  { path: '/user/:id?', component: UserProfile },

  // 参数有正则约束
  { path: '/user/:id(\\d+)', component: UserByNumber }
]
```

### 12.3.3 query 参数（URL 查询参数）

query 参数是 URL 中 `?` 后面的部分，比如 `/search?keyword=vue&page=1`。

```vue
<!-- 跳转时带 query 参数 -->
<RouterLink to="/search?keyword=vue&page=1">搜索</RouterLink>

<!-- 编程式跳转 -->
router.push({ path: '/search', query: { keyword: 'vue', page: 1 } })
```

### 12.3.4 嵌套路由

用 `children` 属性定义嵌套路由：

```typescript
const routes = [
  {
    path: '/user',
    component: UserLayout,
    children: [
      { path: '', redirect: '/user/profile' },  // 默认子路由
      { path: 'profile', component: UserProfile },  // /user/profile
      { path: 'settings', component: UserSettings }  // /user/settings
    ]
  }
]
```

### 12.3.5 多级嵌套

```typescript
{
  path: '/dashboard',
  component: DashboardLayout,
  children: [
    {
      path: 'analytics',
      component: Analytics,
      children: [
        { path: 'realtime', component: RealtimeAnalytics },
        { path: 'historical', component: HistoricalAnalytics }
      ]
    }
  ]
}
```

### 12.3.6 命名路由

给路由起个名字，编程式跳转时用名字而不是路径：

```typescript
const routes = [
  { path: '/user/:id', name: 'UserDetail', component: UserDetail }
]

// 用名字跳转
router.push({ name: 'UserDetail', params: { id: '123' } })
// URL 变成 /user/123

// 比直接写路径更可靠，路径变了名字不用改
```

## 12.4 路由参数获取

### 12.4.1 useRoute 获取参数（params / query）

```typescript
import { useRoute } from 'vue-router'

const route = useRoute()

// 获取 params 参数
console.log(route.params.id)  // '123'

// 获取 query 参数
console.log(route.query.keyword)  // 'vue'

// 获取路由名
console.log(route.name)  // 'UserDetail'
```

### 12.4.2 路由参数变化检测

当 URL 的 params 参数变化时（如从 `/user/1` 切换到 `/user/2`），组件不会重新创建（因为是同一个路由规则），需要用 `watch` 来监听：

```typescript
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 监听 params 变化
watch(
  () => route.params.id,
  (newId) => {
    console.log('用户 ID 从变了：', newId)
    fetchUser(newId)
  }
)
```

### 12.4.3 路由 Props 传递

可以用 `props` 把路由参数作为组件的 props 传递：

```typescript
// 路由配置：启用 props
{ path: '/user/:id', component: UserDetail, props: true }

// 组件里直接用 props.id，而不是 route.params.id
defineProps<{ id: string }>()
```

### 12.4.4 $route 对象结构解析

```typescript
interface RouteLocationNormalized {
  path: string        // '/user/123'
  name: string | null // 'UserDetail'
  params: Record<string, string | string[]>
  query: Record<string, string | string[]>
  hash: string         // '#section'
  fullPath: string     // '/user/123?page=1#section'
  meta: RouteMeta      // 路由元信息
  redirectedFrom: string | null
}
```

## 12.5 编程式导航

### 12.5.1 router.push / replace / go

```typescript
const router = useRouter()

// push：跳转到指定路径（会留下历史记录）
router.push('/user/123')
router.push({ path: '/user/123' })
router.push({ name: 'UserDetail', params: { id: '123' }, query: { tab: 'info' } })

// replace：替换当前历史记录（不会留下历史记录）
router.replace('/about')

// go：在历史记录中前进或后退
router.go(-1)    // 后退一页
router.go(1)    // 前进一页
router.go(-2)   // 后退两页
```

### 12.5.2 命名视图（多个 router-view）

如果一个页面有多个独立区域需要渲染不同的组件，可以用**命名视图**：

```vue
<!-- App.vue -->
<template>
  <RouterView name="header" />   <!-- 命名视图：header -->
  <main>
    <RouterView />                <!-- 默认视图 -->
  </main>
  <RouterView name="footer" />    <!-- 命名视图：footer -->
</template>
```

```typescript
// 路由配置：给每个视图分配不同的组件
{
  path: '/',
  components: {
    default: () => import('./views/Main.vue'),
    header: () => import('./views/Header.vue'),
    footer: () => import('./views/Footer.vue')
  }
}
```

### 12.5.3 别名与重定向

```typescript
const routes = [
  // redirect：访问 /home 时自动跳转到 /
  { path: '/home', redirect: '/' },

  // redirect 到命名路由
  { path: '/old-user/:id', redirect: (to) => `/user/${to.params.id}` },

  // alias：两个 URL 都能访问同一个组件
  { path: '/about', component: About, alias: '/关于' }
]
```

## 12.6 路由守卫

### 12.6.1 全局前置守卫（beforeEach）

最常用的守卫，在每次路由切换前触发：

```typescript
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [...]
})

// 全局前置守卫：每次路由跳转之前都会执行
// 适合做：登录验证、权限检查、页面标题设置等
router.beforeEach((to, from) => {
  // to：目标路由对象（包含 path、params、query、meta 等）
  //     例如：to.path = '/admin'，to.meta.requiresAuth = true
  // from：来源路由对象（上一页是什么）

  // beforeEach 必须返回一个值来决定是否放行：
  // return true  → 允许跳转，继续执行后续流程
  // return false → 阻止跳转，停留在当前页面
  // return '/login' 或 return { name: 'Login' } → 跳转到指定路径
  // return new Error('xxx') → 取消跳转并抛出错误

  // 示例：检查目标页面是否需要登录
  if (to.meta.requiresAuth) {
    // to.meta.requiresAuth 是我们在路由配置里自定义的数据（meta 字段）
    // meta 可以存放任意自定义数据：requiresAuth、roles、title 等
    const token = localStorage.getItem('token')
    if (!token) {
      // 没有 token，跳转到登录页，并把用户想访问的页面作为 redirect 参数带过去
      return { name: 'Login', query: { redirect: to.fullPath } }
    }
  }

  // 动态设置页面标题（每个路由的 meta 里设置 title 即可）
  if (to.meta.title) {
    document.title = `${to.meta.title} - 我的网站`
  }

  return true  // 放行
})
```

### 12.6.2 全局解析守卫（beforeResolve）

在所有组件内守卫和异步路由组件解析之后、导航确认之前触发：

```typescript
router.beforeResolve((to, from) => {
  // 适合在这里做数据预获取
  console.log('路由解析完成，即将跳转')
  return true
})
```

### 12.6.3 全局后置钩子（afterEach）

导航完成后触发，适合做页面埋点：

```typescript
router.afterEach((to, from) => {
  // 没有返回值，用于"事后处理"
  console.log('跳转完成，从', from.path, '到', to.path)

  // 发送 PV 统计
  fetch('/api/analytics', {
    method: 'POST',
    body: JSON.stringify({ path: to.path, referrer: from.path })
  })
})
```

### 12.6.4 路由独享守卫（beforeEnter）

写在路由配置里，只在进入这个路由时触发：

```typescript
{
  path: '/admin',
  component: AdminPanel,
  beforeEnter: (to, from) => {
    // 只有访问 /admin 时才检查权限
    if (!isAdmin()) {
      return '/login'
    }
    return true
  }
}
```

### 12.6.5 组件内守卫（beforeRouteEnter / Update / Leave）

```typescript
export default {
  beforeRouteEnter(to, from) {
    // 在渲染该组件的路由确认前调用
    // 不能访问 this（组件实例还没创建）
    // 可以用 next(vm => { vm.xxx }) 访问组件实例
    next(vm => {
      console.log('组件已挂载，vm 是组件实例', vm)
    })
  },

  beforeRouteUpdate(to, from) {
    // 路由参数变化时调用（如 /user/1 -> /user/2）
    // 可以访问 this
    console.log('路由参数变化了', to.params.id)
  },

  beforeRouteLeave(to, from) {
    // 离开该路由时调用
    const answer = window.confirm('有未保存的内容，确定离开吗？')
    if (!answer) return false
  }
}
```

### 12.6.6 setup 组件中的路由守卫（onBeforeRouteEnter / onBeforeRouteUpdate / onBeforeRouteLeave，Vue 3.5+）

Vue 3.5 引入了组合式 API 版本的路由守卫：

```typescript
import { onBeforeRouteEnter, onBeforeRouteUpdate, onBeforeRouteLeave } from 'vue-router'

onBeforeRouteEnter((to, from) => {
  console.log('进入路由')
})

onBeforeRouteUpdate((to, from) => {
  console.log('路由更新了', to.params.id)
})

onBeforeRouteLeave((to, from) => {
  if (hasUnsavedChanges.value) {
    return '有未保存的更改，确定离开？'
  }
})
```

### 12.6.7 守卫执行顺序

```
1. 路由切换触发
     ↓
2. 全局 beforeEach（按注册顺序，每个都执行完）
     ↓
3. 路由独享 beforeEnter（按配置顺序）
     ↓
4. 组件 beforeRouteEnter
     ↓
5. 全局 beforeResolve
     ↓
6. 导航确认，DOM 更新
     ↓
7. 全局 afterEach（后置钩子，无权阻止）
```

## 12.7 路由元信息（meta）

路由的 `meta` 字段可以存储任意自定义信息，用来实现路由级别的权限、标题、缓存策略等：

```typescript
{
  path: '/admin',
  component: AdminPanel,
  meta: {
    requiresAuth: true,     // 需要登录才能访问
    roles: ['admin'],       // 需要 admin 角色
    title: '管理后台',       // 页面标题（配合全局守卫设置 document.title）
    keepAlive: true        // 是否需要 KeepAlive 缓存
  }
}
```

**常见 meta 字段及用途：**

| meta 字段 | 类型 | 用途 |
|-----------|------|------|
| `requiresAuth` | `boolean` | 是否需要登录 |
| `roles` | `string[]` | 允许访问的角色列表 |
| `title` | `string` | 页面标题 |
| `keepAlive` | `boolean` | 是否缓存组件 |
| `breadcrumb` | `BreadcrumbItem[]` | 面包屑导航数据 |
| `affix` | `boolean` | 是否固定在标签栏（KeepAlive 场景） |

```typescript
// 在全局守卫里读取 meta
router.beforeEach((to, from) => {
  // to.meta 是 RouteMeta 类型（详见下节），访问方式和普通对象一样
  if (to.meta.requiresAuth) {
    // 检查登录状态
  }

  if (to.meta.roles) {
    // 检查用户角色是否匹配
    const userRole = getUserRole()
    if (!to.meta.roles.includes(userRole)) {
      return '/403'  // 无权限，跳转到 403 页面
    }
  }

  // 动态设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 我的网站`
  }
})
```

**RouteMeta 类型定义（TypeScript 推荐）：**

用 TypeScript 时，建议给 `meta` 定义一个接口，这样 IDE 会有类型提示：

```typescript
// src/types/router.d.ts
import 'vue-router'

// 扩展 RouteMeta 接口，给 meta 字段添加类型
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean    // 是否需要登录
    roles?: string[]          // 允许的角色
    title?: string            // 页面标题
    keepAlive?: boolean       // 是否 KeepAlive
  }
}
```

这样 `to.meta.requiresAuth` 就有了正确的类型，IDE 也能提供自动补全。

## 12.8 高级用法

### 12.8.1 滚动行为控制

路由切换后，页面会保持在切换前的滚动位置。你可以通过 `scrollBehavior` 自定义这个行为——比如让页面每次切换都滚到顶部，或者记住用户在某个页面的滚动位置。

**常见场景**：
- 点击"回到顶部"链接后，切换路由时自动滚到顶部
- 用户在列表页滚动到一半，点击进入详情页，再点返回，能回到列表页的原来位置（`savedPosition`）
- 点击锚点链接（如 `#comments`），跳转到页面特定位置

```typescript
const router = createRouter({
  history: createWebHistory(),
  routes: [...],

  // scrollBehavior：控制路由切换后的页面滚动位置
  // to：目标路由，from：来源路由，savedPosition：浏览器前进/后退时的位置
  scrollBehavior(to, from, savedPosition) {
    // 场景一：用户点击浏览器的前进/后退按钮，恢复到之前的滚动位置
    // 这是最符合直觉的行为——返回上一页时，滚动位置应该和离开时一样
    if (savedPosition) {
      return savedPosition
    }

    // 场景二：目标路由 URL 里有 hash（如 /article#comments），滚动到对应锚点
    // el: to.hash → 找到 id 为 hash 的元素，behavior: 'smooth' → 平滑滚动
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }

    // 场景三：默认行为——每次路由切换都滚动到页面顶部
    // top: 0 → 距离页面顶部 0px（即最顶部）
    return { top: 0, behavior: 'smooth' }
  }
})
```

### 12.8.2 路由懒加载（动态 import）

把每个路由组件拆分成独立的 JS 文件，用户访问时才加载：

```typescript
// 不用懒加载：所有组件一次性加载（首屏慢）
import Home from '../views/Home.vue'

// 懒加载：路由匹配时才加载（首屏快）
const Home = () => import('../views/Home.vue')

// 带名字的懒加载（webpack）
const Home = () => import(/* webpackChunkName: "home" */ '../views/Home.vue')

const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/about', component: () => import('../views/About.vue') }
]
```

### 12.8.3 路由过渡动画

```vue
<template>
  <RouterView v-slot="{ Component }">
    <Transition name="fade" mode="out-in">
      <component :is="Component" :key="route.path" />
    </Transition>
  </RouterView>
</template>

<style>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
```

### 12.8.4 导航故障处理（NavigationFailureType）

Vue Router 4 引入了更精确的导航故障处理：

```typescript
import { createRouter, NavigationFailureType } from 'vue-router'

router.push('/user/123').catch((err) => {
  if (err.type === NavigationFailureType.redirected) {
    console.log('导航被重定向了')
  }
  if (err.type === NavigationFailureType.aborted) {
    console.log('导航被 beforeEach 阻止了')
  }
  if (err.type === NavigationFailureType.cancelled) {
    console.log('导航被新的导航取消了')
  }
  if (err.type === NavigationFailureType.duplicated) {
    console.log('导航到当前页面（重复导航）')
  }
})
```

### 12.8.5 history 模式服务器配置（nginx）

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

`try_files` 的意思是：先找对应的文件，找不到就找目录，都找不到就返回 `index.html`——这样 SPA 的路由就能正常工作了。

### 12.8.6 通配符与 404

```typescript
// 放在路由配置的最后
{ path: '/:pathMatch(.*)*', component: NotFound }  // 匹配所有未定义的路由
{ path: '/:pathMatch(.*)', component: NotFound }    // 不带 * 的版本只能匹配单层
```

## 12.9 路由进阶

### 12.9.1 路由分组与批量导入

```typescript
// src/router/modules/home.ts
export default [
  { path: '/', name: 'Home', component: () => import('@/views/home/index.vue') },
  { path: '/about', name: 'About', component: () => import('@/views/home/About.vue') }
]

// src/router/modules/user.ts
export default [
  { path: '/user/:id', name: 'UserDetail', component: () => import('@/views/user/Detail.vue') },
  { path: '/user/settings', name: 'UserSettings', component: () => import('@/views/user/Settings.vue') }
]

// router/index.ts 合并
import homeRoutes from './modules/home'
import userRoutes from './modules/user'

const routes = [
  ...homeRoutes,
  ...userRoutes,
  { path: '/:pathMatch(.*)*', component: () => import('@/views/NotFound.vue') }
]
```

### 12.9.2 动态路由注册

```typescript
// 模拟：从服务器获取权限路由配置
const permissionRoutes = await fetch('/api/routes').then(r => r.json())

// 动态添加路由
permissionRoutes.forEach((route: RouteRecordRaw) => {
  router.addRoute(route)
})
```

---

## 本章小结

本章我们系统学习了 Vue Router 4 的核心知识：

- **SPA 路由原理**：history vs hash 两种模式，URL 变化通过 JavaScript 切换组件而不是刷新页面。
- **快速上手**：创建路由实例，router-link 和 router-view 的基本用法。
- **路由参数**：params 动态路径参数、query 查询参数、嵌套路由、多级路由。
- **编程式导航**：`router.push`、`router.replace`、`router.go`，命名视图和重定向。
- **路由守卫**：全局前置/解析/后置守卫、路由独享守卫、组件内守卫、组合式 API 守卫（Vue 3.5+），完整的守卫执行顺序。
- **路由 meta 元信息**：存储任意自定义数据，导航守卫中读取。
- **高级用法**：滚动行为、路由懒加载、过渡动画、导航故障处理、history 模式服务器配置、动态路由注册。

下一章我们会学习 **Pinia 状态管理**——Vue 官方推荐的全新状态管理方案，它比 Vuex 更简洁、更 TypeScript 友好，是 Vue 3 项目的首选状态管理工具！

