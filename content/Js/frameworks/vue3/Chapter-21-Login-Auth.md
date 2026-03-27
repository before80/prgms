+++
title = "第21章 登录与权限控制"
weight = 210
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十一章 登录与权限控制

> 用户登录和权限控制，可能是全栈开发中最让人又爱又恨的部分。爱的是它太重要了，几乎每个应用都需要；恨的是，这里面的门门道道多到能写一本书。JWT、Token、OAuth2、SSO、动态路由、按钮权限……本章用一整章的篇幅，把这些"拦路虎"一个个给你讲明白，让你从此不再谈"权"色变。

## 21.1 常见的登录认证方案

### 21.1.1 账号密码登录（最传统、最经典）

账号密码登录是最古老的认证方式，也是最容易理解的。用户输入用户名和密码，后端校验通过后返回认证凭证。流程如下：

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端
    participant B as 后端服务器
    participant DB as 数据库

    U->>F: 输入用户名/密码，点击登录
    F->>B: POST /api/login { username, password }
    B->>DB: 查询用户信息
    DB-->>B: 返回用户记录
    B->>B: 校验密码（bcrypt比较）
    B-->>F: 返回 Token / Session
    F->>F: 存储 Token，跳转到首页
    F-->>U: 登录成功！
```

密码在传输和存储时都有讲究：**传输层**必须用 HTTPS 加密，否则密码在网络上就是裸奔；**存储层**必须加盐哈希（比如用 bcrypt），绝对不能存明文密码。想象一下，如果数据库被拖库，而你存的是明文密码，那用户的支付宝、微信密码可能都跟这个一样——后果不堪设想。

前端在登录成功后，通常会把 Token 存在 `localStorage` 或 `sessionStorage` 里：

```typescript
// 登录成功后保存 token
localStorage.setItem('token', response.data.token)

// 请求时携带 token（通过 Axios 拦截器）
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 登出时清除 token
localStorage.removeItem('token')
```

`localStorage` 和 `sessionStorage` 的区别在于：前者是持久存储，关闭浏览器再打开还在；后者是会话级存储，关闭浏览器标签就没了。从安全角度，敏感 Token 存 `sessionStorage` 更安全——别人趁你不在翻开你浏览器时，至少拿不到 Token。

### 21.1.2 短信验证码登录（OTP）

OTP（One-Time Password，一次性密码）登录在移动互联网时代非常常见。用户输入手机号，后端生成一个验证码（通常6位数字，有效期5-10分钟），短信服务商（如阿里云、腾讯云）负责把验证码发到用户手机，用户输入验证码完成登录。

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端
    participant B as 后端服务器
    participant SMS as 短信服务商

    U->>F: 输入手机号，点击获取验证码
    F->>B: POST /api/send-sms { phone: '13800138000' }
    B->>B: 生成6位随机验证码，存入 Redis（设置5分钟过期）
    B->>SMS: 调用短信 API 发送验证码
    SMS-->>U: 收到短信："您的验证码是 384921"
    U->>F: 输入验证码 384921，点击登录
    F->>B: POST /api/login-by-sms { phone, code: '384921' }
    B->>B: 从 Redis 取出验证码比对
    alt 验证码正确
        B-->>F: 返回 Token，登录成功
    else 验证码错误或过期
        B-->>F: 返回错误：验证码错误/已过期
    end
```

前端需要处理的几个细节：

```typescript
// CountDown.vue - 倒计时按钮组件
import { ref } from 'vue'

export default {
  setup() {
    const countDown = ref(0)  // 倒计时秒数
    const isCounting = ref(false)
    let timer: number | null = null

    const sendCode = async () => {
      if (isCounting.value) return

      // 调用发送验证码接口
      await api.sendSms(phone.value)

      // 开始倒计时
      isCounting.value = true
      countDown.value = 60

      timer = window.setInterval(() => {
        countDown.value--
        if (countDown.value <= 0) {
          isCounting.value = false
          if (timer) clearInterval(timer)
        }
      }, 1000)
    }

    return { countDown, isCounting, sendCode }
  }
}
```

短信验证码登录有个**安全陷阱**需要注意：有些系统设计成"验证码正确就自动注册"，也就是说，如果用户输入一个从未注册过的手机号，收到了验证码，那说明这个手机号归你控制，系统就默认你是这个手机号的主人了。这在逻辑上是合理的，但有被滥用风险——攻击者可以批量发送短信给陌生号码，然后尝试自己输入正确的验证码来"认领"这些号码。所以生产环境中，发送验证码前最好加图形验证码或行为验证码，防止接口被刷。

### 21.1.3 第三方登录（OAuth 2.0）

OAuth 2.0 是一个**授权框架**，不是认证协议，但实践中它被广泛用于"第三方登录"。简单说，OAuth 2.0 让你可以在不获取用户密码的情况下，授权另一个应用访问你的某些资源。

以"微信登录"为例，用流程图展示：

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端（你的应用）
    participant WX as 微信授权服务器
    participant B as 后端（你的服务器）

    U->>F: 点击"微信登录"
    F->>WX: 跳转微信授权页面（redirect_uri, scope, state）
    Note over U,WY: 用户在微信页面确认授权
    WX-->>F: 携带 code 跳转回 redirect_uri
    F->>B: 把 code 传给后端（不要在前端直接处理！）
    B->>WX: 用 code 换 access_token（后端对后端，安全）
    WX-->>B: 返回 access_token + openid
    B->>WX: 用 access_token 获取用户信息
    WX-->>B: 返回微信用户信息（昵称、头像等）
    B->>B: 在自己数据库查找或创建用户，生成自己的 Token
    B-->>F: 返回自己系统的 Token
    F-->>U: 登录成功，跳转首页
```

**安全要点**：整个过程中，最核心的原则是——**code 换 token 必须在后端进行**。因为把 `client_secret` 放在前端代码里，就等于把家门钥匙放在门垫下面。攻击者只要扒拉一下你的代码，就能用你的 secret 去换用户的 token，后果非常严重。

OAuth 2.0 有几种授权模式（grant type），最常用的是**授权码模式（Authorization Code）**，就是上面展示的流程。其他模式如**隐式模式（Implicit）**（已经deprecated，不推荐用）、**密码模式（Password）**（只用于自家客户端）等，了解一下即可。

### 21.1.4 SSO 单点登录（企业级）

SSO（Single Sign-On，单点登录）是企业级场景的标配。员工在公司的任意一个系统（如 OA、邮箱、报销系统）登录后，访问其他系统无需再次输入用户名密码。大型互联网公司内部也大量使用 SSO。

SSO 的核心原理是**共享登录状态**。当用户访问子系统 A 时，如果没登录，A 会把用户跳转到一个**统一的登录中心（SSO Server）**；用户在登录中心登录后，登录中心会在自己的域下写入 Cookie（或者通过 Token 机制），然后跳转回子系统 A；后续用户访问子系统 B 时，B 发现没登录，再跳转到登录中心，但这次登录中心发现用户已经登录了，就会直接跳转回 B，省去输入密码的环节。

```mermaid
flowchart TB
    subgraph SSO["SSO 单点登录架构"]
        direction TB
        SSO_Server["登录中心<br/>sso.company.com"]
        Sub_A["子系统 A<br/>app1.company.com"]
        Sub_B["子系统 B<br/>app2.company.com"]
        Sub_C["子系统 C<br/>app3.company.com"]
        
        SSO_Server --> Sub_A
        SSO_Server --> Sub_B
        SSO_Server --> Sub_C
    end

    U["用户浏览器"] --> Sub_A
    U --> Sub_B
    U --> Sub_C
    U -.->|共享 Cookie| SSO_Server
```

SSO 的实现可以用**共享 Cookie**（同父域下）、**JSONP 跨域**、**Token 传递**（比如 CAS 协议）等方式。在 Vue 前端项目中，接入 SSO 通常是：在路由守卫里检查是否已登录，未登录就跳转 SSO 登录页，登录成功后 SSO Server 会带一个 Ticket 回来，前端用 Ticket 换自己的 Token。

## 21.2 JWT 与 Token 机制

### 21.2.1 JWT 是什么？

JWT（JSON Web Token）是一种开放标准（RFC 7519），它定义了一种紧凑、URL 安全的方式来表示在各方之间传输的声明（claims）。翻译成人话：JWT 就是一个**字符串**，里面包含了用户信息，而且这个字符串是**防篡改**的——因为它的签名机制保证了，如果有人偷偷改了里面的内容，签名就对不上了。

JWT 由三部分组成，用点号（`.`）分隔：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

| 部分 | 名称 | 作用 |
|------|------|------|
| Header（第一段） | 头部 | 声明类型和签名算法（如 HS256） |
| Payload（第二段） | 载荷 | 存放实际要传输的数据（用户ID、角色等） |
| Signature（第三段） | 签名 | 用 secret 加密前两段，防止数据被篡改 |

**JWT 的优点**：
- **无状态**：服务端不需要存 Token，Token 本身包含所有需要的信息。集群部署时不需要共享 Session。
- **可验证**：通过签名可以验证 Token 的真伪和完整性。
- **跨域**：适合微服务架构，不同服务之间通过 Token 传递用户信息。

**JWT 的缺点**：
- **无法主动失效**：Token 一旦签发，在过期之前无法撤销。所以一般 Token 有效期设得比较短（如15分钟），配合 Refresh Token 使用。
- **Payload 是明文的**（只是 Base64 编码，不是加密！），不要存敏感信息。

### 21.2.2 Token 的存储与刷新

前端的 Token 存储策略是个老生常谈的问题，常见方案有以下几种：

**方案一：只存 Access Token**

最简单的方式，只用一个 Token。每次请求带上它，后端校验有效性。缺点是有效期不能设太长，否则安全性差；设短了用户体验差——用户操作到一半突然要重新登录。

**方案二：Access Token + Refresh Token（推荐）**

```mermaid
flowchart LR
    A["Access Token<br/>有效期15分钟"] --> B["用于接口请求"]
    C["Refresh Token<br/>有效期7天"] --> D["用于刷新 Access Token"]
    
    style A fill:#e63946,color:#fff
    style C fill:#457b9d,color:#fff
```

Access Token 有效期短，即使泄露也能把损失控制在15分钟内；Refresh Token 有效期长，专门用来换新的 Access Token，这样即使 Access Token 过期，用户也能"静默"续期，用户完全感知不到。

```typescript
// token 管理模块 - token.ts
import axios from 'axios'

// 保存 token
export const saveTokens = (accessToken: string, refreshToken: string) => {
  localStorage.setItem('access_token', accessToken)
  localStorage.setItem('refresh_token', refreshToken)
}

// 获取 access token
export const getAccessToken = () => localStorage.getItem('access_token')

// 刷新 token
export const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token')
  if (!refreshToken) {
    throw new Error('没有 refresh token，需要重新登录')
  }

  const response = await axios.post('/api/auth/refresh', { refreshToken })
  const { accessToken, refreshToken: newRefreshToken } = response.data

  // 保存新 token（通常 refresh token 也会更新）
  saveTokens(accessToken, newRefreshToken)

  return accessToken
}

// Axios 拦截器 - 自动处理 token 刷新
let isRefreshing = false  // 防止多个请求同时触发刷新
let requestQueue: Array<(token: string) => void> = []  // 等待 token 的请求队列

axios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // 如果是 401（未授权）且不是刷新 token 的请求
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // 如果正在刷新，把请求加入队列，等刷新完成后再执行
        return new Promise(resolve => {
          requestQueue.push((token: string) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(axios(originalRequest))
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const newToken = await refreshToken()

        // 刷新成功后，依次处理队列中的请求
        requestQueue.forEach(callback => callback(newToken))
        requestQueue = []

        // 重试当前请求
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return axios(originalRequest)
      } catch (refreshError) {
        // 刷新失败，跳转到登录页
        window.location.href = '/login'
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)
```

这个方案有个细节值得注意：当 Access Token 过期时，可能有多个请求同时触发 401，如果没有特殊处理，这些请求会各自调用一次刷新 Token 接口，导致刷新多次。上面代码用 `isRefreshing` 标志和请求队列巧妙地解决了这个问题——只有第一个请求去刷新，其他请求排队等刷新完成后再用新 Token 重试。

### 21.2.3 Token 的过期处理与安全考虑

**Token 过期后怎么办？** 如果 Refresh Token 也过期了，那就只能跳转登录页让用户重新登录。但在跳转前，最好给用户一个友好的提示，而不是直接一脚踢出去。可以这样处理：

```typescript
// 在路由守卫或 Axios 拦截器中
if (error.response?.status === 401) {
  // 清除本地 token
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')

  // 跳转到登录页，带上当前路径，登录成功后可以跳回来
  const currentPath = window.location.pathname
  window.location.href = `/login?redirect=${encodeURIComponent(currentPath)}`
}
```

**安全建议**：
1. 生产环境必须用 HTTPS，否则 Token 在网络上明文传输，等于把家门钥匙寄给陌生人。
2. 敏感操作（如修改密码、删除数据）可以要求用户重新输入密码，验证后才放行。
3. 后端可以对 Token 做**主动失效**处理（把已签发但未过期的 Token 加入黑名单），比如用户修改密码后，旧 Token 应该立即失效。
4. 前端不要把 Token 存在 URL 参数里（`?token=xxx`），因为 URL 会被浏览器历史、服务器日志、Referer 头泄露。

## 21.3 路由级别的权限控制（动态路由）

### 21.3.1 动态路由的原理

路由权限控制的核心思路是：**路由表不是写死的，而是根据用户登录后返回的权限数据动态生成的**。

```mermaid
flowchart TB
    A["用户登录"] --> B["后端返回用户信息和权限列表"]
    B --> C["前端根据权限列表<br/>过滤路由表"]
    C --> D["生成最终路由表<br/>动态添加到 router"]
    D --> E["用户只能访问有权限的页面"]
    
    style A fill:#42b883,color:#fff
    style E fill:#e63946,color:#fff
```

具体实现分为两步：

**第一步：定义路由时标记权限**

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

// 路由配置元信息 - 用来标记哪些路由需要权限
const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }  // 不需要登录
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/users',
    name: 'UserList',
    component: () => import('@/views/users/List.vue'),
    meta: {
      requiresAuth: true,
      permission: 'user:list'  // 需要 user:list 权限
    }
  },
  {
    path: '/users/create',
    name: 'UserCreate',
    component: () => import('@/views/users/Create.vue'),
    meta: {
      requiresAuth: true,
      permission: 'user:create'  // 需要 user:create 权限
    }
  },
  {
    path: '/roles',
    name: 'RoleList',
    component: () => import('@/views/roles/List.vue'),
    meta: {
      requiresAuth: true,
      permission: 'role:list'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: {
      requiresAuth: true,
      permission: 'system:settings'
    }
  },
  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

**第二步：在路由守卫中动态处理**

```typescript
// router/permission.ts
import router from './index'
import { getAccessToken } from '@/utils/token'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

// 权限白名单 - 不需要登录就能访问的页面
const whiteList = ['/login', '/register', '/forgot-password']

// 动态生成可访问路由（根据用户权限过滤）
const generateAccessibleRoutes = (userPermissions: string[]) => {
  const allRoutes = getAllRoutes()  // 这里从路由配置里取出所有带 permission 的路由

  return allRoutes.filter(route => {
    // 如果路由没有 permission 字段，说明不需要特殊权限，只要有登录就行
    if (!route.meta?.permission) return true

    // 检查用户权限列表中是否包含该路由需要的权限
    return userPermissions.includes(route.meta.permission)
  })
}

// 获取所有需要权限的路由（实际项目中可以从路由配置文件里提取）
const getAllRoutes = () => {
  const mainRoutes = router.getRoutes()
  return mainRoutes.filter(r => r.meta?.requiresAuth)
}

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const hasToken = getAccessToken()
  const userStore = useUserStore()

  if (hasToken) {
    // 已登录
    if (to.path === '/login') {
      // 已登录还访问登录页，跳转到首页
      next({ path: '/' })
    } else {
      // 检查是否有用户信息
      const hasUserInfo = userStore.userInfo && Object.keys(userStore.userInfo).length > 0

      if (hasUserInfo) {
        // 有用户信息，检查权限
        if (to.meta?.permission) {
          // 该页面需要特定权限
          const hasPermission = userStore.permissions.includes(to.meta.permission)
          if (hasPermission) {
            next()
          } else {
            // 没有权限，跳转到 403 页面
            next({ path: '/403', replace: true })
          }
        } else {
          // 不需要特定权限，直接放行
          next()
        }
      } else {
        // 没有用户信息，说明刷新后状态丢了，需要重新获取
        try {
          await userStore.getUserInfo()
          // 重新触发路由守卫，让守卫重新判断（hack 方式）
          next({ ...to, replace: true })
        } catch (error) {
          // 获取用户信息失败，Token 可能过期
          console.error('获取用户信息失败:', error)
          // 清除 Token，跳转登录
          userStore.logout()
          next(`/login?redirect=${to.path}`)
        }
      }
    }
  } else {
    // 未登录
    if (whiteList.includes(to.path)) {
      next()
    } else {
      // 跳转登录页
      next(`/login?redirect=${to.path}`)
    }
  }
})

export default router
```

### 21.3.2 刷新页面后权限丢失的应对

SPA 应用有个经典问题：用户刷新页面后，JavaScript 重新执行，Pinia/Vuex 里的状态丢失了，但动态生成的路由表也丢了——因为路由表是在用户登录后根据权限动态生成的，刷新后需要重新生成。

解决方案是：用户信息存在 `localStorage` 或 `sessionStorage` 里作为备份，页面加载时先检查有没有 Token，有的话从存储里恢复用户信息，再重新生成路由。

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { getAccessToken, removeTokens } from '@/utils/token'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null as any,
    permissions: [] as string[]
  }),

  actions: {
    // 从本地存储恢复用户信息（页面刷新后调用）
    restoreFromStorage() {
      const storedUserInfo = localStorage.getItem('user_info')
      const storedPermissions = localStorage.getItem('user_permissions')

      if (storedUserInfo) {
        this.userInfo = JSON.parse(storedUserInfo)
      }
      if (storedPermissions) {
        this.permissions = JSON.parse(storedPermissions)
      }
    },

    async getUserInfo() {
      const response = await axios.get('/api/user/info')
      this.userInfo = response.data.userInfo
      this.permissions = response.data.permissions

      // 存入本地存储，作为状态丢失后的备份
      localStorage.setItem('user_info', JSON.stringify(this.userInfo))
      localStorage.setItem('user_permissions', JSON.stringify(this.permissions))
    },

    logout() {
      this.userInfo = null
      this.permissions = []
      removeTokens()
      localStorage.removeItem('user_info')
      localStorage.removeItem('user_permissions')
    }
  }
})
```

```typescript
// main.ts - 应用入口
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import { useUserStore } from './stores/user'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 恢复用户状态（放在 router 安装之后，app.mount 之前）
const userStore = useUserStore()
if (getAccessToken()) {
  userStore.restoreFromStorage()
}

app.mount('#app')
```

## 21.4 按钮级别的权限控制（自定义指令）

### 21.4.1 v-permission 自定义指令

路由级别的权限控制住了页面访问，但页面内部的按钮——比如"新增用户"、"删除订单"——还需要单独控制。一个没有"删除"权限的用户，如果能看到"删除"按钮并点击，可能看到报错，这体验也不好。更好的做法是：**没有权限的按钮，直接不显示**。

Vue 3 的自定义指令（directive）非常适合做这件事：

```typescript
// directives/permission.ts
import type { Directive, DirectiveBinding } from 'vue'
import { useUserStore } from '@/stores/user'

// 按钮权限指令 v-permission="'user:delete'"
const permissionDirective: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const userStore = useUserStore()
    const requiredPermission = binding.value  // 比如 'user:delete'

    // 如果没有传入权限要求，或者用户有该权限，则不处理
    if (!requiredPermission) return

    // 检查用户权限列表
    if (!userStore.permissions.includes(requiredPermission)) {
      // 没有权限，移除这个按钮
      el.parentNode?.removeChild(el)
    }
  }
}

// 批量注册指令
export const registerDirectives = (app: any) => {
  app.directive('permission', permissionDirective)
}

// 或者单独导出
export { permissionDirective as vPermission }
```

### 21.4.2 在组件中使用权限指令

```vue
<template>
  <div class="user-list">
    <!-- 有 user:create 权限才显示新增按钮 -->
    <el-button v-permission="'user:create'" type="primary" @click="handleCreate">
      新增用户
    </el-button>

    <!-- 有 user:delete 权限才显示删除按钮 -->
    <el-table :data="tableData">
      <el-table-column prop="name" label="姓名" />
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button
            v-permission="'user:edit'"
            size="small"
            @click="handleEdit(row)"
          >
            编辑
          </el-button>
          <el-button
            v-permission="'user:delete'"
            size="small"
            type="danger"
            @click="handleDelete(row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { vPermission } from '@/directives/permission'

// 指令注册（如果没在 main.ts 里全局注册的话）
// 局部注册的方式
// const vPermission = computed(() => { ... })  // 这个不行，需要 directive
</script>
```

不过有个问题：上面的 `v-permission` 指令是基于当前用户的权限列表来判断的，这个权限列表是从后端获取并存到 Pinia store 里的。如果组件需要在 store 初始化之前就渲染（虽然这种情况很少），指令可能会失效。保证 store 先初始化再用是前提。

### 21.4.3 权限指令的增强：支持多个权限（OR/AND）

有时候，一个按钮可能需要多种权限之一就能访问（OR），或者必须同时拥有多个权限（AND）：

```typescript
// directives/permission.ts
interface PermissionValue {
  type: 'or' | 'and'
  value: string[]
}

// v-permission-or="['user:create', 'system:admin']"  -- 拥有任意一个即可
// v-permission-and="['user:read', 'user:write']"      -- 必须同时拥有

const permissionDirective: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const userStore = useUserStore()

    // 支持两种写法：字符串 'user:delete' 或对象 { type: 'or', value: ['user:create', 'admin'] }
    let requiredPermissions: string[] = []
    let logicType: 'or' | 'and' = 'or'

    if (typeof binding.value === 'string') {
      requiredPermissions = [binding.value]
    } else if (binding.value && typeof binding.value === 'object') {
      requiredPermissions = binding.value.value
      logicType = binding.value.type || 'or'
    }

    if (requiredPermissions.length === 0) return

    let hasPermission = false
    if (logicType === 'or') {
      // OR: 有任意一个权限就行
      hasPermission = requiredPermissions.some(p => userStore.permissions.includes(p))
    } else {
      // AND: 必须拥有所有权限
      hasPermission = requiredPermissions.every(p => userStore.permissions.includes(p))
    }

    if (!hasPermission) {
      el.parentNode?.removeChild(el)
    }
  }
}
```

## 21.5 角色与权限管理

### 21.5.1 RBAC 模型介绍

RBAC（Role-Based Access Control，基于角色的访问控制）是最常见的权限管理模型。它的核心概念很简单：

- **用户（User）**：系统实际操作者
- **角色（Role）**：一组权限的集合，比如"管理员"、"运营"、"普通用户"
- **权限（Permission）**：对某个资源的某种操作，`resource:action`，比如 `user:create`、`order:read`

用户和角色是多对多关系（一个用户可以有多个角色，一个角色可以包含多个用户），角色和权限也是多对多关系。

```mermaid
erDiagram
    USER ||--o{ USER_ROLE : "拥有"
    ROLE ||--o{ USER_ROLE : "被分配给"
    ROLE ||--o{ ROLE_PERMISSION : "拥有"
    PERMISSION ||--o{ ROLE_PERMISSION : "被赋予给"

    USER {
        int id PK
        string username
        string password_hash
        string phone
        datetime created_at
    }

    ROLE {
        int id PK
        string name
        string code
        string description
    }

    PERMISSION {
        int id PK
        string name
        string code "user:create"
        string resource "user"
        string action "create"
    }

    USER_ROLE {
        int user_id FK
        int role_id FK
    }

    ROLE_PERMISSION {
        int role_id FK
        int permission_id FK
    }
```

### 21.5.2 前端的角色数据设计

前端通常不需要维护完整的 RBAC 逻辑（那是后端的事），但前端需要：

1. **获取当前用户的角色和权限**：登录后从后端拿到
2. **根据角色/权限显示不同内容**：比如管理员能看到某个菜单，普通用户看不到

```typescript
// stores/user.ts
export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null as any,
    roles: [] as string[],       // 角色标识列表，如 ['admin', 'editor']
    permissions: [] as string[]  // 权限标识列表，如 ['user:create', 'user:delete']
  }),

  getters: {
    // 判断是否有某个角色
    hasRole: (state) => (role: string) => state.roles.includes(role),

    // 判断是否有某个权限
    hasPermission: (state) => (permission: string) => state.permissions.includes(permission),

    // 是否是超级管理员
    isAdmin: (state) => state.roles.includes('admin'),

    // 是否是普通用户
    isNormalUser: (state) => !state.roles.some(r => ['admin', 'editor'].includes(r))
  },

  actions: {
    // 获取用户信息（包含角色和权限）
    async getUserInfo() {
      const response = await axios.get('/api/user/info')
      this.userInfo = response.data.userInfo
      this.roles = response.data.roles.map((r: any) => r.code)
      this.permissions = response.data.permissions.map((p: any) => p.code)

      localStorage.setItem('user_info', JSON.stringify(this.userInfo))
      localStorage.setItem('user_roles', JSON.stringify(this.roles))
      localStorage.setItem('user_permissions', JSON.stringify(this.permissions))
    }
  }
})
```

### 21.5.3 页面内基于角色的内容展示

```vue
<template>
  <div class="dashboard">
    <h1>控制台</h1>

    <!-- 管理员专属内容 -->
    <div v-if="userStore.isAdmin" class="admin-panel">
      <h2>管理员面板</h2>
      <p>欢迎，管理员大人！这里可以看到系统全貌。</p>
    </div>

    <!-- 编辑者专属内容 -->
    <div v-if="userStore.hasRole('editor')" class="editor-panel">
      <h2>内容管理</h2>
      <p>你可以编辑文章和管理草稿。</p>
    </div>

    <!-- 所有登录用户可见 -->
    <div class="common-panel">
      <h2>我的工作台</h2>
      <p>这是你的个人工作区。</p>
    </div>

    <!-- 权限按钮 -->
    <el-button
      v-if="userStore.hasPermission('system:config')"
      @click="showConfigDialog = true"
    >
      系统配置
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const { userInfo, roles, permissions } = storeToRefs(userStore)
</script>
```

## 21.6 本章小结

本章我们从登录认证的几种常见方案出发，介绍了账号密码、短信验证码、OAuth2 第三方登录和 SSO 单点登录的原理和流程。重点讲解了 JWT/Token 的存储、刷新和过期处理机制——这是前端权限体系的核心基础设施。

动态路由是保护页面级权限的核心手段：通过在路由元信息中标记权限需求，在路由守卫中根据用户实际权限动态放行或拦截。按钮级权限则通过 Vue 3 的自定义指令 `v-permission` 实现，将无权限的按钮从 DOM 中移除，比显示后禁用（disable）体验更好。

最后介绍了 RBAC 角色权限模型，以及前端如何存储和使用角色/权限数据。一个完善的权限体系需要前后端紧密配合——后端负责权限的精确控制（所有接口都需要二次校验），前端负责用户体验层面的权限过滤，两者缺一不可。

**核心要点回顾**：
- Token 建议使用 Access + Refresh 双 Token 方案
- 动态路由在路由守卫中根据 `meta.permission` 判断
- 按钮权限用 `v-permission` 自定义指令实现
- 用户信息和权限列表需要做持久化（localStorage）以应对页面刷新
- 权限控制要前后端双重校验，前端防君子，后端防小人
