+++
title = "附录 D 术语表"
weight = 1030
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 附录 D 术语表

> Vue 3 的文档、教程和社区讨论里充满了各种专业术语。对于新手来说，这些术语就像一座座小山，爬过一座还有一座。这一章把 Vue 3 相关的核心术语整理成中英对照表，配上简洁的解释，让你从此不再迷茫。

## D.1 核心概念

| 英文术语 | 中文译名 | 解释 |
|----------|----------|------|
| **Reactivity** | 响应式 | 当数据变化时，视图自动更新的机制 |
| **Proxy** | 代理 | Vue 3 实现响应式的底层技术 |
| **Virtual DOM** | 虚拟 DOM | 真实 DOM 的 JavaScript 对象描述 |
| **vnode** | 虚拟节点 | 虚拟 DOM 树上的一个节点 |
| **Component** | 组件 | 可复用的 UI 单元，包含模板、逻辑和样式 |
| **Single File Component (SFC)** | 单文件组件 | `.vue` 文件，包含 template/script/style 三个部分 |
| **Directive** | 指令 | 带有 `v-` 前缀的特殊 HTML 属性 |
| **Slot** | 插槽 | 父组件向子组件传递 UI 结构的方式 |
| **Props** | 属性 | 父组件向子组件传递数据的方式（单向） |
| **Emit** | 触发事件 | 子组件向父组件发消息的方式 |
| **v-model** | 双向绑定 | 数据和视图自动同步的语法糖 |

## D.2 Composition API 相关

| 英文术语 | 中文译名 | 解释 |
|----------|----------|------|
| **Composition API** | 组合式 API | Vue 3 的核心编程范式，按功能相关性组织代码 |
| **setup** |  setup 函数 | Composition API 的入口函数 |
| **script setup** | script setup 语法 | 简化 setup 的编译器语法糖 |
| **ref** | ref | 创建基本类型响应式数据的 API |
| **reactive** | reactive | 创建对象类型响应式数据的 API |
| **computed** | 计算属性 | 由其他数据派生出来的值，自动缓存 |
| **watch** | 侦听器 | 监听数据变化并执行副作用 |
| **watchEffect** | 响应式侦听器 | 自动追踪依赖的侦听器 |
| **toRefs** | toRefs | 把 reactive 对象转成多个 ref |
| **toRaw** | toRaw | 从 Proxy 获取原始对象 |
| **markRaw** | markRaw | 标记一个对象不需要响应式 |
| **readonly** | 只读 | 创建一个不可修改的响应式副本 |
| **shallowRef** | 浅层 ref | 只追踪 `.value` 引用的 ref |
| **shallowReactive** | 浅层 reactive | 只有第一层属性响应式的 reactive |
| **customRef** | 自定义 ref | 自定义响应式追踪逻辑 |
| **provide / inject** | 提供 / 注入 | 祖先组件向后代组件传递数据的方式 |
| **Composables** | 组合式函数 | 返回响应式状态的函数，Vue 3 的代码复用模式 |

## D.3 组件相关

| 英文术语 | 中文译名 | 解释 |
|----------|----------|------|
| **Lifecycle Hooks** | 生命周期钩子 | 组件创建→挂载→更新→销毁各阶段的回调函数 |
| **Dynamic Component** | 动态组件 | 根据条件动态切换渲染的组件 |
| **Async Component** | 异步组件 | 按需加载的组件，首屏不下载 |
| **KeepAlive** | 缓存组件 | 缓存组件实例，避免重复创建 |
| **Teleport** | 瞬移组件 | 把 DOM 渲染到指定位置 |
| **Suspense** | 异步占位 | 异步组件加载完成前的占位显示 |
| **Recursive Component** | 递归组件 | 在自己模板里引用自己的组件 |
| **Functional Component** | 函数式组件 | 无状态、无实例的轻量组件（Vue 3 已废弃） |
| **Render Function** | 渲染函数 | 返回虚拟 DOM 的函数，template 会被编译成这个 |
| **$attrs** | 属性集合 | 未被子组件 props 接收的 attributes |
| **$listeners** | 监听器集合 | 未被子组件 emit 接收的事件监听器（Vue 3 已合并到 $attrs） |
| **Scoped CSS** | 作用域 CSS | 只在当前组件生效的样式 |
| **CSS Modules** | CSS 模块 | 编译时生成唯一类名的 CSS 写法 |

## D.4 路由相关

| 英文术语 | 中文译名 | 解释 |
|----------|----------|------|
| **SPA** | 单页面应用 | 只有一个 HTML 文件，通过 JS 切换内容的应用 |
| **Router** | 路由 | URL 到组件的映射管理器 |
| **History Mode** | History 模式 | 使用 History API 的路由，URL 无 # |
| **Hash Mode** | Hash 模式 | 使用 URL hash 的路由，URL 有 # |
| **Route** | 路由 | 一条 URL 规则 |
| **Router Link** | 路由链接 | 点击后不刷新页面但切换路由的链接 |
| **Router View** | 路由视图 | 匹配路由的组件渲染的位置 |
| **Navigation Guard** | 导航守卫 | 路由切换前后的拦截器 |
| **Lazy Loading** | 懒加载 | 访问时才加载路由组件 |
| **Route Params** | 路由参数 | URL 路径中的动态参数 |
| **Query Params** | 查询参数 | URL ? 后面的参数 |
| **Nested Routes** | 嵌套路由 | 路由里包含子路由 |
| **Redirect** | 重定向 | 访问一个 URL 自动跳转到另一个 |
| **Alias** | 别名 | 一个路由的多个 URL 路径 |

## D.5 状态管理相关

| 英文术语 | 中文译名 | 解释 |
|----------|----------|------|
| **State** | 状态 | 应用中的数据 |
| **Store** | 状态仓库 | 集中管理状态的容器 |
| **Pinia** | Pinia | Vue 3 官方推荐的状态管理库 |
| **Vuex** | Vuex | Vue 2 时代的状态管理库（Vue 3 已不推荐） |
| **Getter** | 获取器 | 从 state 派生出来的计算值，类似 computed |
| **Action** | 行动 | 修改 state 的方法，可以是异步的 |
| **Mutation** | 变更 | Vuex 中修改 state 的同步操作（Pinia 已废弃） |
| **Module** | 模块 | Vuex 中把 store 拆分成多个子模块 |
| **StoreToRefs** | StoreToRefs | 解构 store 属性时保持响应式的工具 |
| **Plugin** | 插件 | 扩展 store 功能的机制（如持久化插件） |

## D.6 构建与工具相关

| 英文术语 | 中文译名 | 解释 |
|----------|----------|------|
| **Vite** | Vite | Vue 官方的新一代构建工具，开发体验极快 |
| **Webpack** | Webpack | 老牌打包工具，Vue CLI 基于此 |
| **HMR** | 热模块替换 | 代码变化时只更新变化的部分，页面不刷新 |
| **ESM** | ES 模块 | JavaScript 的官方模块系统，Vite 基于此 |
| **Tree Shaking** | 摇树优化 | 构建时移除未使用代码 |
| **Code Splitting** | 代码分割 | 把代码拆分成多个小 chunk，按需加载 |
| **Chunk** | 代码块 | 分割后的代码包 |
| **Bundler** | 打包工具 | 把多个模块合并成单个/少量文件的工具 |
| **PostCSS** | PostCSS | CSS 后处理器 |
| **AST** | 抽象语法树 | 代码的树状结构表示，Vite 和 Babel 的基础 |
| **Source Map** | 源码映射 | 构建后的代码和源码的映射关系，方便调试 |
| **Babel** | Babel | JavaScript 编译器，把新语法转成旧语法 |
| **ESLint** | ESLint | JavaScript 代码质量检查工具 |
| **Prettier** | Prettier | 代码格式化工具 |
| **TypeScript** | TypeScript | JavaScript 的超集，增加了类型系统 |
| **TSConfig** | TypeScript 配置 | `tsconfig.json` 文件，定义 TypeScript 编译选项 |
| **Monorepo** | 单仓库 | 在一个仓库里管理多个包/项目 |
| **pnpm Workspace** | pnpm 工作空间 | pnpm 的 Monorepo 解决方案 |
| **CI/CD** | 持续集成/持续部署 | 自动构建、测试和部署的流程 |
| **Docker** | Docker | 容器化平台，应用可以打包成镜像运行 |
| **nginx** | Nginx | 高性能 HTTP 服务器，常用于前端部署 |

## D.7 性能与测试相关

| 英文术语 | 中文译名 | 解释 |
|----------|----------|------|
| **LCP** | 最大内容绘制 | Core Web Vitals 指标，页面主要内容的加载速度 |
| **FID** | 首次输入延迟 | Core Web Vitals 指标，页面响应用户操作的速度 |
| **CLS** | 累积布局偏移 | Core Web Vitals 指标，页面布局稳定性 |
| **Core Web Vitals** | 核心网页指标 | Google 定义的三个关键性能指标 |
| **Long Task** | 长任务 | 阻塞主线程超过 50ms 的任务 |
| **FLIP** | FLIP 动画 | First/Last/Invert/Play，用于列表动画 |
| **Virtual Scrolling** | 虚拟滚动 | 只渲染可视区域的列表项，提升大数据量性能 |
| **Web Vitals** | 网页指标 | 衡量用户体验的指标集合 |
| **Unit Test** | 单元测试 | 对最小单元（如函数）进行测试 |
| **Integration Test** | 集成测试 | 对模块组合进行测试 |
| **E2E Test** | 端到端测试 | 模拟真实用户操作，对整个应用进行测试 |
| **Vitest** | Vitest | Vite 原生的测试框架 |
| **Jest** | Jest | Facebook 出品的测试框架 |
| **Playwright** | Playwright | 微软出品的 E2E 测试工具 |
| **Coverage** | 覆盖率 | 测试覆盖了多少代码 |
| **Mock** | 模拟 | 用假数据替代真实依赖的测试技术 |
| **Snapshot Testing** | 快照测试 | 保存输出的快照，对比变化 |

## D.8 其他常用术语

| 英文术语 | 中文译名 | 解释 |
|----------|----------|------|
| **IDE** | 集成开发环境 | 如 VS Code、WebStorm |
| **SDK** | 软件开发工具包 | 某个平台提供的开发工具集合 |
| **CDN** | 内容分发网络 | 分布式的静态资源服务器网络 |
| **API** | 应用程序接口 | 应用之间互相调用的接口 |
| **REST API** | REST API | 基于 HTTP 协议的接口设计风格 |
| **GraphQL** | GraphQL | 一种 API 查询语言 |
| **JWT** | JSON Web Token | 无状态的认证令牌 |
| **OAuth** | OAuth | 开放授权协议，第三方登录的基础 |
| **SSO** | 单点登录 | 一次登录，多个系统通用 |
| **SSR** | 服务端渲染 | 在服务端生成 HTML 的技术 |
| **SSG** | 静态站点生成 | 构建时生成静态 HTML 的技术 |
| **Hydration** | 水合作用 | SSR 页面在客户端激活的过程 |
| **SEO** | 搜索引擎优化 | 让网站在搜索引擎中排名更高的技术 |
| **PWA** | 渐进式 Web 应用 | 可以安装到桌面的 Web 应用 |
| **Service Worker** | Service Worker | 运行在后台的脚本，实现离线缓存 |
| **Manifest** | Manifest 文件 | PWA 的配置文件 |
| **IntersectionObserver** | 交集观察者 | 元素进入视口时触发回调的 API |
| **ResizeObserver** | 尺寸观察者 | 元素尺寸变化时触发回调的 API |
| **XSS** | 跨站脚本攻击 | 在页面注入恶意脚本的攻击方式 |
| **CSRF** | 跨站请求伪造 | 伪造用户请求的攻击方式 |
| **CORS** | 跨域资源共享 | 允许跨域请求的 HTTP 头机制 |
| **Debounce** | 防抖 | 等待一定时间后执行，重复触发重新计时 |
| **Throttle** | 节流 | 固定间隔执行，触发时跳过等待期间的所有调用 |

---

## 附录小结

本章整理了 Vue 3 学习和开发中常见的核心术语：

- **核心概念**：响应式、虚拟 DOM、组件、指令、插槽
- **Composition API**：ref、reactive、computed、Composables
- **组件相关**：生命周期、动态组件、KeepAlive、Teleport
- **路由相关**：History 模式、懒加载、导航守卫
- **状态管理**：Pinia、Store、Actions、Getters
- **构建工具**：Vite、Webpack、HMR、Tree Shaking
- **性能测试**：Core Web Vitals、虚拟滚动、单元测试
- **其他术语**：SSR、PWA、CORS、SEO

遇到不懂的术语随时回来查，早日把术语表变成自己的知识。

