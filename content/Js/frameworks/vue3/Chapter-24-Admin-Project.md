+++
title = "第24章 实战：后台管理系统项目"
weight = 240
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十四章 实战：后台管理系统项目

> 前二十三章我们学了大量知识点，本章终于要"真刀真枪"地做一个完整的项目了。后台管理系统是 Vue 3 最典型的应用场景——登录认证、侧边菜单、表格列表、表单增删改查、分页、搜索、权限控制……这些"标准动作"本章全部覆盖。学完这一章，你将拥有一个可以写进简历的完整后台管理项目。

## 24.1 项目初始化（Vite + Vue 3 + TS + Pinia）

### 24.1.1 项目脚手架

使用 Vite 创建项目，选择 Vue 3 + TypeScript 模板：

```bash
# 创建项目
npm create vite@latest vue3-admin -- --template vue-ts

# 进入目录
cd vue3-admin

# 安装依赖
npm install

# 安装项目所需的库
npm install vue-router@4 pinia element-plus @element-plus/icons-vue axios
npm install -D unplugin-vue-components unplugin-auto-import
```

### 24.1.2 目录结构规划

一个规范的后台管理项目，目录结构应该清晰合理：

```
vue3-admin/
├── public/
│   └── favicon.ico
├── src/
│   ├── api/                    # API 接口层
│   │   ├── request.ts          # Axios 实例配置
│   │   ├── user.ts             # 用户相关接口
│   │   ├── article.ts          # 文章相关接口
│   │   └── index.ts            # API 统一导出
│   │
│   ├── assets/                  # 静态资源
│   │   ├── images/
│   │   └── styles/
│   │       ├── variables.scss   # SCSS 变量
│   │       └── global.scss      # 全局样式
│   │
│   ├── components/              # 通用组件
│   │   ├── ProTable/           # 通用表格组件
│   │   ├── ProModal/           # 通用弹窗组件
│   │   └── ProSearch/          # 通用搜索组件
│   │
│   ├── composables/             # 组合式函数
│   │   ├── useTable.ts
│   │   └── useDialog.ts
│   │
│   ├── directive/               # 全局指令
│   │   ├── permission.ts       # 权限指令
│   │   └── loading.ts           # 加载指令
│   │
│   ├── hooks/                   # 业务 hooks
│   │   └── usePage.ts          # 分页逻辑
│   │
│   ├── layout/                  # 布局组件
│   │   ├── index.vue           # 主布局入口
│   │   ├── components/
│   │   │   ├── Sidebar.vue     # 侧边栏
│   │   │   ├── Navbar.vue      # 顶部导航
│   │   │   └── TagsView.vue    # 标签页
│   │   └── styles/
│   │       └── layout.scss
│   │
│   ├── router/                  # 路由配置
│   │   ├── index.ts            # 路由主文件
│   │   ├── routes/
│   │   │   ├── static.ts       # 静态路由（登录页、404 等）
│   │   │   └── dynamic.ts      # 动态路由（需要权限的路由）
│   │   └── guards.ts           # 路由守卫
│   │
│   ├── stores/                  # Pinia 状态管理
│   │   ├── user.ts             # 用户状态
│   │   ├── app.ts              # 应用状态（侧边栏折叠等）
│   │   └── permission.ts       # 权限状态（路由、菜单）
│   │
│   ├── types/                   # TypeScript 类型定义
│   │   ├── api.d.ts            # API 响应类型
│   │   ├── user.d.ts           # 用户相关类型
│   │   └── router.d.ts         # 路由相关类型
│   │
│   ├── utils/                   # 工具函数
│   │   ├── storage.ts          # 存储封装
│   │   ├── token.ts            # Token 管理
│   │   └── format.ts           # 格式化工具
│   │
│   ├── views/                   # 页面组件
│   │   ├── login/
│   │   ├── dashboard/
│   │   ├── user/
│   │   │   ├── index.vue       # 用户列表
│   │   │   └── detail.vue      # 用户详情
│   │   ├── article/
│   │   └── error/
│   │       ├── 403.vue
│   │       └── 404.vue
│   │
│   ├── App.vue
│   ├── main.ts
│   └── env.d.ts
│
├── .env.production              # 生产环境变量
├── .env.development             # 开发环境变量
├── vite.config.ts
└── tsconfig.json
```

### 24.1.3 Vite 配置与全局导入

这个项目的核心配置是 **自动导入**：Vue/Pinia 的 API（如 `ref`、`computed`、`defineStore`）不需要手动 import，插件会自动在编译时添加。

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'  // 自动导入 API（ref、computed 等）
import Components from 'unplugin-vue-components/vite'  // 自动导入组件（无需 import MyButton）
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'  // Element Plus 的自动导入
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [
    vue(),
    // AutoImport：自动导入 Vue/Pinia 的 API，无需手动写 import 语句
    AutoImport({
      // imports：指定哪些库的 API 要自动导入
      // 'vue' → ref、reactive、computed、watch 等
      // 'vue-router' → useRoute、useRouter 等
      // 'pinia' → defineStore、storeToRefs 等
      imports: ['vue', 'vue-router', 'pinia'],

      // resolvers：组件库的自动导入解析器
      // ElementPlusResolver() 会自动导入用到的 Element Plus 组件
      // 例如模板里用了 <el-button>，会自动添加 import { ElButton } from 'element-plus'
      resolvers: [ElementPlusResolver()],

      // dts：自动生成 TypeScript 类型声明文件
      // src/auto-imports.d.ts 会被自动生成和更新
      // IDE 根据这个文件提供类型提示
      dts: 'src/auto-imports.d.ts'
    }),
    // Components：自动导入组件（.vue 文件），无需 import 直接用
    Components({
      resolvers: [ElementPlusResolver()],  // 同上，Element Plus 组件自动导入
      dts: 'src/components.d.ts'          // 组件类型声明文件
    })
      resolvers: [ElementPlusResolver()],
      dts: 'src/components.d.ts'
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  }
})
```

## 24.2 登录与权限体系

### 24.2.1 登录页面

```vue
<!-- src/views/login/index.vue -->
<template>
  <div class="login-page">
    <div class="login-box">
      <h1 class="title">Vue3 Admin</h1>
      <p class="subtitle">后台管理系统</p>

      <el-form
        ref="formRef"
        :model="loginForm"
        :rules="rules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="loginForm.remember">
            记住密码
          </el-checkbox>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登 录' }}
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { usePermissionStore } from '@/stores/permission'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const permissionStore = usePermissionStore()

const formRef = ref()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid: boolean) => {
    if (!valid) return

    loading.value = true
    try {
      // 调用登录接口
      await userStore.login(loginForm.username, loginForm.password)

      // 获取用户权限，构建动态路由
      await permissionStore.buildRoutes()

      // 跳转到首页或重定向地址
      const redirect = (route.query.redirect as string) || '/'
      router.replace(redirect)
    } catch (error) {
      ElMessage.error('用户名或密码错误')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.title {
  text-align: center;
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  text-align: center;
  font-size: 14px;
  color: #999;
  margin-bottom: 32px;
}

.login-form {
  .login-button {
    width: 100%;
  }
}
</style>
```

### 24.2.2 动态路由与菜单

```typescript
// src/stores/permission.ts
import { defineStore } from 'pinia'
import { RouteRecordRaw } from 'vue-router'

export const usePermissionStore = defineStore('permission', {
  state: () => ({
    // 完整的动态路由列表
    routes: [] as RouteRecordRaw[],
    // 生成侧边栏菜单用的路由（去掉 hidden: true 的路由）
    menuRoutes: [] as RouteRecordRaw[],
    // 按钮权限列表
    permissions: [] as string[],
    // 是否已构建路由
    isRoutesBuilt: false
  }),

  actions: {
    // 构建动态路由
    async buildRoutes() {
      try {
        // 从后端获取路由配置
        const remoteRoutes = await fetchRoutesFromServer()

        // 将后端返回的路由配置转成 Vue Router 格式
        const dynamicRoutes = generateRoutes(remoteRoutes)

        // 存储完整路由（用于 addRoute）
        this.routes = dynamicRoutes

        // 过滤出菜单路由（hidden 不等于 true 的）
        this.menuRoutes = dynamicRoutes.filter(route => !route.meta?.hidden)

        this.isRoutesBuilt = true

        return dynamicRoutes
      } catch (error) {
        console.error('构建路由失败:', error)
        throw error
      }
    },

    // 重置路由状态（退出登录时调用）
    resetRoutes() {
      this.routes = []
      this.menuRoutes = []
      this.permissions = []
      this.isRoutesBuilt = false
    }
  }
})

// 模拟从后端获取路由配置
async function fetchRoutesFromServer(): Promise<any[]> {
  // 实际项目中这里会调用 /api/routes 接口
  return [
    {
      path: '/user',
      name: 'User',
      meta: { title: '用户管理', icon: 'User' },
      children: [
        {
          path: '/user/list',
          name: 'UserList',
          meta: { title: '用户列表', permission: 'user:list' }
        },
        {
          path: '/user/create',
          name: 'UserCreate',
          meta: { title: '新增用户', permission: 'user:create' }
        }
      ]
    },
    {
      path: '/article',
      name: 'Article',
      meta: { title: '文章管理', icon: 'Document' },
      children: [
        {
          path: '/article/list',
          name: 'ArticleList',
          meta: { title: '文章列表', permission: 'article:list' }
        },
        {
          path: '/article/create',
          name: 'ArticleCreate',
          meta: { title: '发布文章', permission: 'article:create' }
        }
      ]
    }
  ]
}

// 将后端路由配置转成 Vue Router 格式
function generateRoutes(remoteRoutes: any[]): RouteRecordRaw[] {
  return remoteRoutes.map(route => {
    const vueRoute: RouteRecordRaw = {
      path: route.path,
      name: route.name,
      meta: {
        title: route.meta?.title,
        icon: route.meta?.icon,
        permission: route.meta?.permission,
        hidden: route.meta?.hidden
      },
      component: () => import('@/layout/index.vue'),  // 父路由用 layout 包裹
      children: route.children ? generateRoutes(route.children) : []
    }
    return vueRoute
  })
}
```

### 24.2.3 路由守卫

```typescript
// src/router/guards.ts
import type { Router } from 'vue-router'
import { getAccessToken } from '@/utils/token'
import { useUserStore } from '@/stores/user'
import { usePermissionStore } from '@/stores/permission'

export const setupRouterGuards = (router: Router) => {
  router.beforeEach(async (to, from, next) => {
    const hasToken = getAccessToken()
    const userStore = useUserStore()
    const permissionStore = usePermissionStore()

    // 有 Token，说明已登录
    if (hasToken) {
      if (to.path === '/login') {
        // 已登录还访问登录页，跳转到首页
        next({ path: '/' })
      } else {
        // 检查是否有用户信息
        const hasUserInfo = !!userStore.userInfo

        if (hasUserInfo) {
          // 有用户信息，检查是否已构建过路由
          if (!permissionStore.isRoutesBuilt) {
            // 还没构建路由，先构建
            try {
              await permissionStore.buildRoutes()

              // 把构建好的路由动态添加进去
              permissionStore.routes.forEach(route => {
                router.addRoute(route as RouteRecordRaw)
              })

              // 重新触发当前导航，让它匹配到新添加的路由
              next({ ...to, replace: true })
            } catch (error) {
              // 获取路由失败，可能是 Token 过期
              userStore.logout()
              next(`/login?redirect=${to.path}`)
            }
          } else {
            // 路由已构建，检查权限
            const requiredPermission = to.meta?.permission as string | undefined
            if (requiredPermission && !userStore.hasPermission(requiredPermission)) {
              // 没有权限，跳转到 403
              next({ path: '/403', replace: true })
            } else {
              next()
            }
          }
        } else {
          // 没有用户信息，先获取
          try {
            await userStore.getUserInfo()
            await permissionStore.buildRoutes()

            // 动态添加路由
            permissionStore.routes.forEach(route => {
              router.addRoute(route as RouteRecordRaw)
            })

            next({ ...to, replace: true })
          } catch (error) {
            userStore.logout()
            next(`/login?redirect=${to.path}`)
          }
        }
      }
    } else {
      // 没有 Token
      if (to.path === '/login') {
        next()
      } else {
        // 跳转到登录页
        next(`/login?redirect=${to.path}`)
      }
    }
  })

  // 路由出错时的处理（比如动态添加的路由重复）
  router.onError(error => {
    console.error('路由错误:', error)
    const path = window.location.pathname
    window.location.href = path
  })
}
```

## 24.3 布局与菜单

### 24.3.1 主布局组件

```vue
<!-- src/layout/index.vue -->
<template>
  <div class="app-wrapper">
    <!-- 侧边栏 -->
    <Sidebar
      :is-collapse="appStore.isSidebarCollapsed"
      :menu-routes="permissionStore.menuRoutes"
    />

    <!-- 主内容区 -->
    <div class="main-container" :class="{ 'is-collapse': appStore.isSidebarCollapsed }">
      <!-- 顶部导航 -->
      <Navbar @toggle-sidebar="appStore.toggleSidebar" />

      <!-- 标签页 -->
      <TagsView />

      <!-- 页面内容 -->
      <main class="app-main">
        <router-view v-slot="{ Component }">
          <keep-alive :include="keepAliveIncludes">
            <component :is="Component" :key="$route.path" />
          </keep-alive>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import { usePermissionStore } from '@/stores/permission'
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'
import TagsView from './components/TagsView.vue'

const appStore = useAppStore()
const permissionStore = usePermissionStore()

// 需要缓存的页面（name 字段）
const keepAliveIncludes = computed(() => {
  return permissionStore.menuRoutes
    .filter(route => route.meta?.keepAlive)
    .map(route => route.name as string)
})
</script>

<style scoped lang="scss">
.app-wrapper {
  display: flex;
  height: 100vh;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin-left: 200px;
  transition: margin-left 0.3s;

  &.is-collapse {
    margin-left: 64px;
  }
}

.app-main {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background: #f0f2f5;
}
</style>
```

### 24.3.2 侧边栏菜单

```vue
<!-- src/layout/components/Sidebar.vue -->
<template>
  <div class="sidebar" :class="{ 'is-collapse': isCollapse }">
    <!-- Logo 区域 -->
    <div class="logo-container">
      <img v-if="!isCollapse" src="@/assets/logo.svg" class="logo" alt="logo" />
      <span v-if="!isCollapse" class="title">Vue3 Admin</span>
      <div v-else class="logo-mini">V</div>
    </div>

    <!-- 菜单 -->
    <el-menu
      :default-active="activeMenu"
      :collapse="isCollapse"
      :unique-opened="true"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      router
    >
      <template v-for="route in menuRoutes" :key="route.path">
        <!-- 一级菜单（没有子菜单） -->
        <el-menu-item
          v-if="!route.children || route.children.length === 0"
          :index="route.path"
        >
          <el-icon v-if="route.meta?.icon">
            <component :is="route.meta.icon" />
          </el-icon>
          <template #title>
            <span>{{ route.meta?.title }}</span>
          </template>
        </el-menu-item>

        <!-- 一级菜单（有子菜单） -->
        <el-sub-menu
          v-else
          :index="route.path"
        >
          <template #title>
            <el-icon v-if="route.meta?.icon">
              <component :is="route.meta.icon" />
            </el-icon>
            <span>{{ route.meta?.title }}</span>
          </template>

          <!-- 二级菜单 -->
          <template v-for="child in route.children" :key="child.path">
            <el-menu-item
              :index="child.path"
              :route="child"
            >
              {{ child.meta?.title }}
            </el-menu-item>
          </template>
        </el-sub-menu>
      </template>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

interface Props {
  isCollapse: boolean
  menuRoutes: RouteRecordRaw[]
}

const props = defineProps<Props>()
const route = useRoute()

// 当前激活的菜单
const activeMenu = computed(() => {
  const { path } = route
  return path
})
</script>

<style scoped lang="scss">
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px;
  height: 100vh;
  background: #304156;
  overflow-x: hidden;
  transition: width 0.3s;
  z-index: 100;

  &.is-collapse {
    width: 64px;
  }
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  background: #2b3a4a;

  .logo {
    width: 32px;
    height: 32px;
    margin-right: 8px;
  }

  .title {
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    white-space: nowrap;
  }

  .logo-mini {
    width: 32px;
    height: 32px;
    background: #409EFF;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: bold;
    font-size: 18px;
    margin: 0 auto;
  }
}

.el-menu {
  border-right: none;
  height: calc(100vh - 60px);
  overflow-y: auto;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
  }
}

.el-menu--collapse {
  width: 64px;
}
</style>
```

### 24.3.3 标签页组件

标签页（TagsView）让用户可以快速切换已访问过的页面：

```vue
<!-- src/layout/components/TagsView.vue -->
<template>
  <div class="tags-view">
    <div class="tags-view-container">
      <router-link
        v-for="tag in visitedRoutes"
        :key="tag.path"
        :to="{ path: tag.path, query: tag.query }"
        class="tags-view-item"
        :class="{ 'is-active': isActive(tag) }"
        @contextmenu.prevent="openContextMenu($event, tag)"
      >
        {{ tag.meta?.title }}
        <el-icon
          v-if="!isAffix(tag)"
          class="close-icon"
          @click.prevent.stop="closeTag(tag)"
        >
          <Close />
        </el-icon>
      </router-link>
    </div>

    <!-- 右键菜单 -->
    <ul
      v-if="contextMenuVisible"
      class="context-menu"
      :style="{ left: contextMenuLeft + 'px', top: contextMenuTop + 'px' }"
    >
      <li @click="refreshSelectedTag">刷新</li>
      <li @click="closeSelectedTag">关闭</li>
      <li @click="closeOthersTags">关闭其他</li>
      <li @click="closeAllTags">关闭所有</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 访问过的路由
const visitedRoutes = ref<RouteRecordRaw[]>([])

// 右键菜单
const contextMenuVisible = ref(false)
const contextMenuLeft = ref(0)
const contextMenuTop = ref(0)
const selectedTag = ref<RouteRecordRaw>()

// 初始化时添加当前路由
watch(
  () => route.path,
  () => {
    if (!visitedRoutes.value.find(v => v.path === route.path)) {
      visitedRoutes.value.push(route as unknown as RouteRecordRaw)
    }
  },
  { immediate: true }
)

const isActive = (tag: RouteRecordRaw) => tag.path === route.path

// 固定标签（不能关闭的）
const isAffix = (tag: RouteRecordRaw) => tag.meta?.affix

const closeTag = (tag: RouteRecordRaw) => {
  const index = visitedRoutes.value.findIndex(v => v.path === tag.path)
  visitedRoutes.value.splice(index, 1)
  // 如果关闭的是当前路由，跳转到最后一个
  if (isActive(tag) && visitedRoutes.value.length > 0) {
    router.push(visitedRoutes.value[visitedRoutes.value.length - 1].path)
  }
}

const refreshSelectedTag = () => {
  router.replace(selectedTag.value!.path)
  contextMenuVisible.value = false
}

const closeSelectedTag = () => {
  closeTag(selectedTag.value!)
  contextMenuVisible.value = false
}

const closeOthersTags = () => {
  visitedRoutes.value = visitedRoutes.value.filter(
    v => v.path === selectedTag.value!.path || isAffix(v)
  )
  contextMenuVisible.value = false
}

const closeAllTags = () => {
  visitedRoutes.value = visitedRoutes.value.filter(v => isAffix(v))
  router.push(visitedRoutes.value[0]?.path || '/')
  contextMenuVisible.value = false
}

const openContextMenu = (event: MouseEvent, tag: RouteRecordRaw) => {
  contextMenuVisible.value = true
  contextMenuLeft.value = event.clientX
  contextMenuTop.value = event.clientY
  selectedTag.value = tag
}

// 点击其他区域关闭右键菜单
document.addEventListener('click', () => {
  contextMenuVisible.value = false
})
</script>

<style scoped lang="scss">
.tags-view {
  height: 34px;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.12);

  .tags-view-container {
    display: flex;
    align-items: center;
    height: 100%;
    overflow-x: auto;
    padding: 0 8px;

    &::-webkit-scrollbar {
      height: 4px;
    }
  }

  .tags-view-item {
    display: inline-flex;
    align-items: center;
    padding: 0 12px;
    height: 26px;
    margin: 4px 4px;
    font-size: 12px;
    color: #495060;
    background: #fff;
    border: 1px solid #d8dce5;
    border-radius: 4px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      color: #409EFF;
      border-color: #409EFF;
    }

    &.is-active {
      color: #fff;
      background: #409EFF;
      border-color: #409EFF;

      .close-icon {
        color: #fff;
      }
    }

    .close-icon {
      margin-left: 4px;
      font-size: 10px;

      &:hover {
        background: rgba(0, 0, 0, 0.1);
        border-radius: 50%;
      }
    }
  }

  .context-menu {
    position: fixed;
    background: #fff;
    border: 1px solid #d8dce5;
    border-radius: 4px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    padding: 4px 0;
    margin: 0;
    list-style: none;
    z-index: 9999;

    li {
      padding: 8px 16px;
      font-size: 12px;
      cursor: pointer;

      &:hover {
        background: #f0f2f5;
        color: #409EFF;
      }
    }
  }
}
</style>
```

## 24.4 CRUD 模板（用户列表页）

### 24.4.1 列表页面

```vue
<!-- src/views/user/List.vue -->
<template>
  <div class="user-list-page">
    <!-- 搜索区域 -->
    <ProSearch @search="handleSearch" @reset="handleReset">
      <el-form-item label="用户名">
        <el-input v-model="queryParams.username" placeholder="请输入用户名" clearable />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="queryParams.status" placeholder="请选择状态" clearable>
          <el-option label="启用" value="1" />
          <el-option label="禁用" value="0" />
        </el-select>
      </el-form-item>
    </ProSearch>

    <!-- 工具栏 -->
    <div class="toolbar">
      <el-button type="primary" v-permission="'user:create'" @click="handleCreate">
        新增用户
      </el-button>
      <el-button type="danger" :disabled="!selectedRows.length" @click="handleBatchDelete">
        批量删除
      </el-button>
      <el-button @click="handleExport">导出 Excel</el-button>
    </div>

    <!-- 表格 -->
    <ProTable
      ref="tableRef"
      :table-data="tableData"
      :loading="loading"
      :total="total"
      :current-page="queryParams.page"
      :page-size="queryParams.pageSize"
      @query="fetchData"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column type="index" label="序号" width="60" />
      <el-table-column prop="username" label="用户名" min-width="120" />
      <el-table-column prop="nickname" label="昵称" min-width="120" />
      <el-table-column prop="email" label="邮箱" min-width="160" />
      <el-table-column prop="phone" label="手机号" min-width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'danger'">
            {{ row.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="roles" label="角色" min-width="150">
        <template #default="{ row }">
          <el-tag
            v-for="role in row.roles"
            :key="role.id"
            size="small"
            style="margin-right: 4px;"
          >
            {{ role.name }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createdAt" label="创建时间" min-width="180">
        <template #default="{ row }">
          {{ formatDate(row.createdAt) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link size="small" v-permission="'user:edit'" @click="handleEdit(row)">
            编辑
          </el-button>
          <el-button type="primary" link size="small" v-permission="'user:assign'" @click="handleAssignRole(row)">
            分配角色
          </el-button>
          <el-button type="danger" link size="small" v-permission="'user:delete'" @click="handleDelete(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </ProTable>

    <!-- 新增/编辑弹窗 -->
    <ProModal
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @confirm="handleSubmit"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="formData.nickname" placeholder="请输入昵称" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item v-if="!formData.id" label="密码" prop="password">
          <el-input v-model="formData.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
    </ProModal>

    <!-- 分配角色弹窗 -->
    <ProModal
      v-model="roleDialogVisible"
      title="分配角色"
      width="500px"
      @confirm="handleAssignRoleSubmit"
    >
      <el-checkbox-group v-model="formData.roleIds">
        <el-checkbox
          v-for="role in allRoles"
          :key="role.id"
          :label="role.id"
          style="display: block; margin-bottom: 8px;"
        >
          {{ role.name }}（{{ role.code }}）
        </el-checkbox>
      </el-checkbox-group>
    </ProModal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatDate } from '@/utils/format'
import { getAccessToken } from '@/utils/token'

// API
import { getUserList, createUser, updateUser, deleteUser, assignRole } from '@/api/user'
import { getAllRoles } from '@/api/role'

// 类型
interface User {
  id: number
  username: string
  nickname: string
  email: string
  phone: string
  status: number
  roles: Array<{ id: number; name: string }>
  createdAt: string
}

interface QueryParams {
  page: number
  pageSize: number
  username?: string
  status?: string
}

// 表格数据
const loading = ref(false)
const tableData = ref<User[]>([])
const total = ref(0)
const selectedRows = ref<User[]>([])

// 搜索参数
const queryParams = reactive<QueryParams>({
  page: 1,
  pageSize: 10,
  username: '',
  status: ''
})

// 弹窗相关
const dialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const formRef = ref()
const formData = reactive({
  id: null as number | null,
  username: '',
  nickname: '',
  email: '',
  phone: '',
  password: '',
  status: 1,
  roleIds: [] as number[]
})

const formRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ]
}

// 角色分配弹窗
const roleDialogVisible = ref(false)
const allRoles = ref<Array<{ id: number; name: string; code: string }>>([])

// 获取表格数据
const fetchData = async () => {
  loading.value = true
  try {
    const res: any = await getUserList(queryParams)
    tableData.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    console.error('获取用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  queryParams.page = 1
  fetchData()
}

// 重置
const handleReset = () => {
  queryParams.username = ''
  queryParams.status = ''
  queryParams.page = 1
  fetchData()
}

// 新增
const handleCreate = () => {
  dialogTitle.value = '新增用户'
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: User) => {
  dialogTitle.value = '编辑用户'
  // 填充表单数据
  Object.assign(formData, {
    id: row.id,
    username: row.username,
    nickname: row.nickname,
    email: row.email,
    phone: row.phone,
    password: '',
    status: row.status
  })
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      if (formData.id) {
        // 编辑
        await updateUser({
          id: formData.id,
          username: formData.username,
          nickname: formData.nickname,
          email: formData.email,
          phone: formData.phone,
          status: formData.status
        })
        ElMessage.success('编辑成功')
      } else {
        // 新增
        await createUser({
          username: formData.username,
          nickname: formData.nickname,
          email: formData.email,
          phone: formData.phone,
          password: formData.password,
          status: formData.status
        })
        ElMessage.success('新增成功')
      }

      dialogVisible.value = false
      fetchData()
    } catch (error) {
      ElMessage.error('操作失败')
    }
  })
}

// 关闭弹窗
const handleDialogClose = () => {
  formRef.value?.resetFields()
  Object.assign(formData, {
    id: null,
    username: '',
    nickname: '',
    email: '',
    phone: '',
    password: '',
    status: 1,
    roleIds: []
  })
}

// 删除
const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm(`确定要删除用户"${row.username}"吗？`, '提示', {
      type: 'warning'
    })
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedRows.value.length} 个用户吗？`,
      '提示',
      { type: 'warning' }
    )
    const ids = selectedRows.value.map(r => r.id)
    await deleteUser(ids)
    ElMessage.success('批量删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

// 导出
const handleExport = () => {
  window.open(`/api/user/export?token=${getAccessToken()}`, '_blank')
}

// 选中行变化
const handleSelectionChange = (rows: User[]) => {
  selectedRows.value = rows
}

// 分配角色
const handleAssignRole = async (row: User) => {
  // 获取所有角色列表
  const rolesRes: any = await getAllRoles()
  allRoles.value = rolesRes.data

  // 回显当前用户已有的角色
  formData.id = row.id
  formData.roleIds = row.roles.map(r => r.id)
  roleDialogVisible.value = true
}

// 提交角色分配
const handleAssignRoleSubmit = async () => {
  try {
    await assignRole({ userId: formData.id!, roleIds: formData.roleIds })
    ElMessage.success('分配成功')
    roleDialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('分配失败')
  }
}

// 初始化
fetchData()
</script>
```

## 24.5 分页与搜索

### 24.5.1 分页逻辑封装

每个列表页都需要分页和搜索，把这个逻辑封装成 composable 可以减少大量重复代码：

```typescript
// src/composables/usePage.ts
import { ref, reactive, computed } from 'vue'

interface PageParams {
  page: number
  pageSize: number
  [key: string]: any  // 其他查询参数
}

interface UsePageOptions<T> {
  // 获取数据的函数
  fetchData: (params: PageParams) => Promise<{ list: T[]; total: number }>
  // 初始每页条数
  defaultPageSize?: number
}

export function usePage<T>(options: UsePageOptions<T>) {
  const { fetchData, defaultPageSize = 10 } = options

  // 分页参数
  const queryParams = reactive<PageParams>({
    page: 1,
    pageSize: defaultPageSize
  })

  // 表格数据
  const tableData = ref<T[]>([])
  const total = ref(0)
  const loading = ref(false)

  // 计算属性：是否有数据
  const hasData = computed(() => tableData.value.length > 0)

  // 加载数据
  const loadData = async () => {
    loading.value = true
    try {
      const res = await fetchData({ ...queryParams })
      tableData.value = res.list
      total.value = res.total
    } catch (error) {
      console.error('加载数据失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 搜索（重置到第一页）
  const search = () => {
    queryParams.page = 1
    loadData()
  }

  // 重置搜索参数
  const reset = (keys?: string[]) => {
    if (keys) {
      // 只重置指定字段
      keys.forEach(key => {
        if (key in queryParams) {
          (queryParams as any)[key] = ''
        }
      })
    } else {
      // 重置所有搜索参数（保留 page 和 pageSize）
      Object.keys(queryParams).forEach(key => {
        if (key !== 'page' && key !== 'pageSize') {
          (queryParams as any)[key] = ''
        }
      })
    }
    queryParams.page = 1
    loadData()
  }

  // 页码变化
  const handlePageChange = (page: number) => {
    queryParams.page = page
    loadData()
  }

  // 每页条数变化
  const handleSizeChange = (size: number) => {
    queryParams.pageSize = size
    queryParams.page = 1
    loadData()
  }

  // 刷新当前页
  const refresh = () => {
    loadData()
  }

  return {
    queryParams,
    tableData,
    total,
    loading,
    hasData,
    loadData,
    search,
    reset,
    handlePageChange,
    handleSizeChange,
    refresh
  }
}
```

## 24.6 KeepAlive 与页面缓存

### 24.6.1 缓存指定页面

Vue 的 `<KeepAlive>` 组件可以缓存组件实例，避免重复创建和销毁。当用户切换标签页时，被缓存的页面状态会保留。

```vue
<!-- src/layout/index.vue -->
<template>
  <router-view v-slot="{ Component, route }">
    <keep-alive :include="keepAliveIncludes">
      <component :is="Component" :key="route.path" />
    </keep-alive>
  </router-view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePermissionStore } from '@/stores/permission'

const permissionStore = usePermissionStore()

// 只有标记了 keepAlive: true 的页面才缓存
const keepAliveIncludes = computed(() => {
  const allRoutes = [...permissionStore.routes]
  return allRoutes
    .filter(route => route.meta?.keepAlive)
    .map(route => route.name as string)
})
</script>
```

### 24.6.2 动态路由中标记缓存

```typescript
// 后端返回的路由配置中，可以通过 meta.keepAlive 标记哪些页面需要缓存
const dynamicRoutes = [
  {
    path: '/article/list',
    name: 'ArticleList',
    meta: {
      title: '文章列表',
      keepAlive: true  // 开启缓存
    }
  },
  {
    path: '/user/list',
    name: 'UserList',
    meta: {
      title: '用户列表',
      keepAlive: true  // 开启缓存
    }
  }
]
```

### 24.6.3 手动操作缓存（onActivated / onDeactivated）

当页面被缓存后，`onMounted` 不会再触发，取而代之的是 `onActivated`（页面被激活）和 `onDeactivated`（页面被缓存）：

```vue
<script setup lang="ts">
import { onMounted, onActivated, onDeactivated } from 'vue'

onMounted(() => {
  console.log('组件首次挂载')
})

onActivated(() => {
  console.log('页面从缓存中恢复，重新激活')
  // 适合在这里刷新数据（如果需要）
})

onDeactivated(() => {
  console.log('页面被缓存起来，即将消失')
  // 适合在这里保存一些状态
})
</script>
```

## 24.7 国际化（i18n）

### 24.7.1 Vue I18n 安装与配置

```bash
npm install vue-i18n
```

```typescript
// src/i18n/index.ts
import { createI18n } from 'vue-i18n'
import messages from './messages'

const i18n = createI18n({
  legacy: false,  // 使用 Composition API 模式
  locale: localStorage.getItem('locale') || 'zh-CN',
  fallbackLocale: 'en-US',
  messages
})

export default i18n
```

```typescript
// src/i18n/messages/index.ts
import zhCN from './locales/zh-CN'
import enUS from './locales/en-US'

const messages = {
  'zh-CN': zhCN,
  'en-US': enUS
}

export default messages
```

```typescript
// src/i18n/locales/zh-CN.ts
export default {
  common: {
    confirm: '确定',
    cancel: '取消',
    save: '保存',
    delete: '删除',
    edit: '编辑',
    add: '新增',
    search: '搜索',
    reset: '重置',
    export: '导出',
    import: '导入',
    loading: '加载中...',
    noData: '暂无数据'
  },
  menu: {
    home: '首页',
    user: '用户管理',
    userList: '用户列表',
    userCreate: '新增用户',
    article: '文章管理',
    articleList: '文章列表'
  },
  user: {
    username: '用户名',
    nickname: '昵称',
    email: '邮箱',
    phone: '手机号',
    status: '状态',
    role: '角色',
    createdAt: '创建时间',
    enabled: '启用',
    disabled: '禁用'
  }
}
```

### 24.7.2 在组件中使用

```vue
<template>
  <div>
    <!-- 在模板中使用 $t -->
    <h1>{{ $t('menu.userList') }}</h1>
    <el-button>{{ $t('common.add') }}</el-button>
    <el-table-column :label="$t('user.username')" />
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()

// 在 script 中使用
console.log(t('common.confirm'))

// 切换语言
const switchLanguage = (lang: string) => {
  locale.value = lang
  localStorage.setItem('locale', lang)
}
</script>
```

## 24.8 部署（Nginx / Docker）

### 24.8.1 打包构建

```bash
# 开发环境构建
npm run build:dev

# 生产环境构建
npm run build:prod
```

构建产物在 `dist/` 目录下，包含 `index.html` 和打包后的静态资源。

### 24.8.2 Nginx 配置

```nginx
# /etc/nginx/conf.d/vue-admin.conf

server {
    listen 80;
    server_name admin.example.com;

    # 前端静态资源
    root /var/www/vue-admin/dist;
    index index.html;

    # SPA 的关键配置：将所有请求都回退到 index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源缓存
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API 代理
    location /api/ {
        proxy_pass http://backend:8080/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 开启 gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    gzip_min_length 1k;
}
```

### 24.8.3 Docker 部署

```dockerfile
# Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# 生产镜像
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```nginx
# nginx.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8080/api/;
        proxy_set_header Host $host;
    }
}
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: .
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    image: my-backend:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=mysql://db:3306/app
    depends_on:
      - db

  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: app
```

## 24.9 本章小结

本章从零构建了一个完整的后台管理系统项目，涵盖了前端工程化的方方面面：
- 项目结构规划、依赖安装、Vite 配置
- 登录认证、动态路由、路由守卫、按钮权限
- 侧边栏菜单、顶部导航、标签页
- 用户管理的完整 CRUD（列表、搜索、新增、编辑、删除、角色分配）
- 分页与搜索逻辑的 composable 封装
- KeepAlive 页面缓存
- Vue I18n 国际化
- Nginx 和 Docker 部署

一个完整的后台管理项目需要掌握的技术栈非常多，本章覆盖的只是最核心的部分。实际项目中还会有更多高级功能，比如表格拖拽排序、树形结构数据、ECharts 可视化、Excel 导入导出等。建议在本章基础上逐步扩展，打造属于你自己的项目模板。

**核心要点回顾**：
- 规范的项目目录结构是团队协作的基础
- 动态路由由后端返回权限列表，前端根据权限过滤并动态添加
- 路由守卫是权限控制的核心，需要处理 Token 校验、用户信息获取、路由构建等逻辑
- CRUD 页面遵循"搜索 -> 工具栏 -> 表格 -> 分页 -> 弹窗"的统一布局
- KeepAlive 可以缓存页面状态，但要注意内存占用
- Vue I18n 是 Vue 3 国际化的标准方案
- SPA 部署需要配置 Nginx 的 `try_files` 将所有请求回退到 index.html
