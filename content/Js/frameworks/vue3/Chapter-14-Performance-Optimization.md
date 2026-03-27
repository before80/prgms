+++
title = "第14章 性能优化"
weight = 140
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十四章 性能优化

> Vue 3 本身已经很快了，但如果你的应用很大或者用户群体在低网速环境下，性能优化仍然至关重要。本章我们会从加载优化、渲染优化、包体积优化、SEO 优化、Core Web Vitals、错误处理六个维度，系统讲解 Vue 3 的性能优化策略。学会这些，你写出来的应用会比别人快上一大截。

## 14.1 加载优化

### 14.1.1 路由懒加载（动态 import）

路由级别的代码分割是最有效的首屏优化手段：

```typescript
// router/index.ts
const routes = [
  // 直接 import：首屏加载全部代码（不推荐）
  // import Home from '../views/Home.vue'

  // 懒加载：访问 / 时只加载 Home，跳转 /about 时才加载 About
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/about', component: () => import('../views/About.vue') },
  { path: '/user/:id', component: () => import('../views/UserDetail.vue') },

  // 带 webpackChunkName 的懒加载（打包后文件名更友好）
  {
    path: '/products',
    component: () => import(/* webpackChunkName: "products" */ '../views/Products.vue')
  }
]
```

### 14.1.2 组件懒加载（defineAsyncComponent）

路由懒加载是路由级别的分割，组件懒加载是组件级别的分割——当某个组件不需要立即显示时，延迟加载。

```typescript
// HeavyChart.vue 只有在用户点击"查看图表"时才加载
import { defineAsyncComponent } from 'vue'

const HeavyChart = defineAsyncComponent(() =>
  import('./components/HeavyChart.vue')
)
```

### 14.1.3 第三方库按需引入

**Ant Design Vue / Element Plus 的按需引入：**

```bash
# 安装按需导入插件
pnpm add -D unplugin-vue-components unplugin-auto-import
```

```typescript
// vite.config.ts
import Components from 'unplugin-vue-components/vite'
import { AntDesignVueResolver, ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default {
  plugins: [
    Components({
      resolvers: [
        AntDesignVueResolver(),
        ElementPlusResolver()
      ]
    })
  ]
}
```

**lodash 的按需引入：**

```typescript
// ❌ 错误：引入整个 lodash（很大）
import _ from 'lodash'

// ✅ 正确：按需引入（只引入用到的函数）
import debounce from 'lodash/debounce'
import cloneDeep from 'lodash/cloneDeep'

// ✅ 或者用 lodash-es（ES Module 版本，天然按需导入）
import { debounce, cloneDeep } from 'lodash-es'
```

### 14.1.4 预加载与预取

Vite 支持在 HTML 里添加预加载提示：

```vue
<!-- 预加载关键资源 -->
<link rel="preload" href="/src/assets/main.css" as="style" />

<!-- 预取路由资源（用户可能访问的页面提前加载） -->
<link rel="prefetch" href="/about" />
```

```typescript
// vite.config.ts 中配置预取
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia'],  // 第三方库单独打包
          'utils': ['lodash-es', 'dayjs']              // 工具库单独打包
        }
      }
    }
  }
}
```

## 14.2 渲染优化

### 14.2.1 KeepAlive 缓存

详见第八章。KeepAlive 可以缓存组件实例，避免重复创建和销毁，是 Tab 切换等场景的必备优化。

### 14.2.2 虚拟滚动（vue-virtual-scroller / vxe-table）

当列表有上万条数据时，一次性渲染所有 DOM 会很卡。虚拟滚动只渲染可视区域内的少量元素，大幅降低 DOM 数量。

```bash
pnpm add vue-virtual-scroller
```

```vue
<template>
  <!-- RecycleScroller 只渲染可视区域的行 -->
  <RecycleScroller
    class="scroller"
    :items="thousandsOfItems"
    :item-size="50"
    key-field="id"
    v-slot="{ item }"
  >
    <div class="item">
      {{ item.name }} - {{ item.description }}
    </div>
  </RecycleScroller>
</template>
```

### 14.2.3 v-memo 优化

Vue 3.2 引入了 `v-memo` 指令，用于缓存模板子树，只有当依赖的值变化时才重新渲染。

```vue
<!-- 当 items 数组引用没变时，整个列表不重新渲染 -->
<div v-for="item in items" :key="item.id" v-memo="[item.id, item.type]">
  <ComplexComponent :item="item" />
</div>
```

### 14.2.4 长列表优化实战

```vue
<script setup>
import { shallowRef } from 'vue'

// 用 shallowRef 而不是 ref，避免深层响应式追踪
const list = shallowRef([])

// 加载数据
async function loadData() {
  const data = await fetch('/api/huge-list').then(r => r.json())
  list.value = data  // 整体替换，不要 push
}
</script>

<template>
  <!-- v-for + v-memo 组合 -->
  <div v-for="item in list" :key="item.id" v-memo="[item.id]">
    <HeavyComponent :data="item" />
  </div>
</template>
```

### 14.2.5 减少不必要的渲染（shallowRef）

```typescript
// ❌ ref 会深层响应式追踪，大数据量时性能差
const data = ref(hugeArray)

// ✅ shallowRef 只追踪 .value 的引用变化
const data = shallowRef(hugeArray)

// 数据更新时，整体替换而不是 push
data.value = newArray  // 触发更新
data.value.push(x)     // 不触发更新！
```

## 14.3 包体积优化

### 14.3.1 Tree Shaking

Tree Shaking 是"摇树优化"——构建时自动移除没有用到的代码。Vite 基于 Rollup 的 Tree Shaking 默认开启，只要你用 ES Module 写法 import，Rollup 就会自动帮你把没用的代码摇掉。

```typescript
// ❌ 使用 CommonJS 导入，Tree Shaking 失效
const _ = require('lodash')

// ✅ 使用 ES Module 导入，Tree Shaking 生效
import { debounce } from 'lodash-es'
// 没有用到的函数会被摇掉
```

### 14.3.2 公共依赖抽离（manualChunks）

前面我们提到 Tree Shaking 可以自动移除没有用到的代码。但有时候我们还需要**手动控制代码如何分包**——比如把第三方库（vue、lodash）和业务代码分开打包。这样做有两个好处：

1. **利用浏览器缓存**：第三方库代码变化很少，打成一个文件后可以被浏览器长期缓存。用户每次访问只需要下载变化大的业务代码。
2. **并行加载**：浏览器对同一个域名有并发请求数量限制（如 Chrome 是 6 个）。把大文件拆成多个小文件，可以让浏览器并行下载，实际加载速度更快。

`manualChunks` 就是用来手动指定如何分包的配置：

```typescript
// vite.config.ts
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // 'vue-core'：这个名字是自定义的，最终会生成 vue-core-xxxx.js 文件
          // [] 里的包会被打进这个 chunk
          'vue-core': ['vue', 'vue-router', 'pinia'],  // Vue 生态单独一个包
          'ui-lib': ['element-plus'],                  // UI 库单独一个包（通常很大）
          'utils': ['lodash-es', 'dayjs']              // 工具库单独一个包
        }
      }
    }
  }
}
```

最终构建产物可能是这样：
```
dist/js/vue-core-a1b2c3d4.js   // 200KB，第三方库，长期缓存
dist/js/ui-lib-e5f6g7h8.js       // 300KB，Element Plus，很少变化
dist/js/chunk-i9j0k1l2.js         // 业务代码，经常变化
```

**什么时候需要手动分包？**
- 第三方库总体积超过 200KB 时（建议拆分）
- 有多个不相关的功能模块时（可以按需加载）
- 想利用 HTTP 缓存优化重复访问时

### 14.3.3 图片资源压缩

图片通常是应用里体积最大的资源。一张未经压缩的 1920×1080 PNG 图片可能超过 1MB，而压缩后可能只有 100KB——体积差 10 倍！`vite-plugin-imagemin` 在构建时自动压缩图片，让你不用手动处理。

```bash
pnpm add -D vite-plugin-imagemin
```

```typescript
// vite.config.ts
import viteImagemin from 'vite-plugin-imagemin'

export default {
  plugins: [
    viteImagemin({
      // png：PNG 图片压缩配置
      // quality: 80 表示压缩到原图 80% 质量，肉眼几乎看不出区别
      png: { quality: 80 },
      // jpg：JPEG 图片压缩配置（也适用于 WebP）
      jpg: { quality: 80 },
      // gif：动图压缩（会略微降低色彩）
      gif: { quality: 60 }
    })
  ]
}
```

**注意**：图片压缩会增加构建时间（因为要处理每张图片）。如果项目图片很多，可以在开发阶段跳过压缩，只在生产构建时压缩：

```typescript
// 生产时才压缩图片
if (process.env.NODE_ENV === 'production') {
  plugins.push(viteImagemin({ ... }))
}
```

### 14.3.4 gzip 压缩

gzip 是一种**服务器端的文件压缩格式**。开启 gzip 后，服务器在发送文件给浏览器之前，先把文件压缩成 .gz 格式（体积通常能减少 60%~80%），浏览器收到后自动解压。

类比理解：就好比你网购一件毛衣，商家直接寄一个压缩包（.gz）给你，比寄一个充满空气的包裹体积小很多，运输更快。

```bash
pnpm add -D vite-plugin-compression
```

```typescript
// vite.config.ts
import viteCompression from 'vite-plugin-compression'

export default {
  plugins: [
    viteCompression({
      algorithm: 'gzip',  // 压缩算法：'gzip'（最常用）或 'brotliCompress'（压缩率更高，体积更小）
      // threshold：文件大小阈值，只有超过这个大小的文件才会压缩（单位：字节）
      // 10240 = 10KB，小于 10KB 的文件压缩意义不大，还会增加服务器解压开销
      threshold: 10240
    })
  ]
}
```

**注意**：gzip 压缩需要服务器支持（Nginx、Apache、Vercel 等主流服务器都支持）。另外，`vite-plugin-compression` 只生成 `.gz` 文件，实际启用 gzip 还需要在服务器配置里开启（`gzip on;`）。

## 14.4 SEO 优化

### 14.4.1 动态标题与 Meta

```typescript
// src/composables/useSEO.ts
import { watch } from 'vue'
import { useRoute } from 'vue-router'

export function useSEO(title: string, description: string) {
  document.title = title

  const meta = document.querySelector('meta[name="description"]')
  if (meta) {
    meta.setAttribute('content', description)
  }
}
```

### 14.4.2 预渲染（prerender-spa-plugin）

预渲染是在**构建阶段**就把页面跑一遍，把渲染好的 HTML 写死到文件里。用户访问时，服务器直接返回这份已经"拼好"的 HTML，而不是等浏览器跑完 JavaScript 再渲染。

这对于那些"内容不经常变化的页面"特别有用——比如官网首页、关于页面、文档页面。但对于"每个用户看到的内容都不一样"的页面（比如社交媒体动态），预渲染就不合适了，老老实实用 SSR。

```bash
pnpm add -D @vitejs/plugin-ssr && pnpm add -D prerender-spa-plugin
```

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { prerenderSPAPlugin } from 'prerender-spa-plugin'

export default defineConfig({
  plugins: [
    vue(),
    new prerenderSPAPlugin({
      // 要预渲染的路由
      routes: ['/', '/about', '/products'],
      // 可选：渲染等待时间（等待 JavaScript 执行完毕）
      renderWaitTime: 1000
    })
  ]
})
```

构建完成后，`dist` 目录里会多出 `/about/index.html`、`/products/index.html` 这样的文件——里面是已经填好内容的真实 HTML，搜索引擎爬虫可以直接抓取。

### 14.4.3 结构化数据（JSON-LD）

搜索引擎不只能抓文字，它还能理解数据的"含义"。**JSON-LD** 是一种结构化数据格式，让搜索引擎知道"这段文字是文章标题"、"这个链接是作者"、"这张图片是产品图"。有了结构化数据，Google 的搜索结果可能会显示更丰富的摘要（富摘要），点击率会显著提升。

```typescript
// 在路由组件的 onMounted 里注入 JSON-LD
import { onMounted } from 'vue'

onMounted(() => {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: 'Vue 3 完全指南',
    author: {
      '@type': 'Person',
      name: '小明'
    },
    datePublished: '2024-01-01',
    image: 'https://example.com/cover.jpg'
  }

  const script = document.createElement('script')
  script.type = 'application/ld+json'
  script.textContent = JSON.stringify(jsonLd)
  document.head.appendChild(script)
})
```

Google 搜索"Vue 3 完全指南"，如果这个页面有 JSON-LD，搜索结果可能会显示"作者：小明"和"发布于 2024-01-01"这样的额外信息，比干巴巴的标题+链接诱人多了。

### 14.4.4 SSR 方案（详见第 26 章 Nuxt 3）

```typescript
// 在 public/index.html 或路由组件的 mounted 里
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Article',
### 14.4.4 SSR 方案（详见第 26 章 Nuxt 3）

服务端渲染（SSR）是 SEO 的终极解决方案，让搜索引擎能看到完全渲染好的 HTML。

## 14.5 Core Web Vitals

Google 用 **Core Web Vitals（核心网页指标）** 来衡量用户体验。相当于 Google 给网站体验打的"健康分"，分数直接影响搜索排名。三个核心指标：

### 14.5.0 三大指标速览

| 指标 | 全称 | 衡量什么 | 及格线 |
|------|------|---------|--------|
| **LCP** | Largest Contentful Paint | 页面主要内容加载完成的速度 | ≤ 2.5秒 |
| **INP** | Interaction to Next Paint | 用户点击/输入到页面响应的速度 | ≤ 200毫秒 |
| **CLS** | Cumulative Layout Shift | 页面布局的稳定程度（有没有乱跳） | ≤ 0.1 |

**为什么这些指标重要？** Google 把它们纳入了搜索排名算法。用户体验好的网站，搜索排名会更靠前；用户体验差的网站，排名会下降。对于 Vue 开发者来说，优化这三个指标就是提升用户体验最直接的方式。

### 14.5.1 LCP 优化

**LCP（Largest Contentful Paint，最大内容绘制）**：从打开网页到屏幕上显示主要内容的时间。"主要内容"通常是页面中央最大的图片或文字块——比如一篇博文的封面图、一段大标题。

LCP 慢的原因通常是：**首屏图片太大、网络太慢、CSS 阻塞渲染**。优化策略：

1. **图片优化**：使用现代格式（WebP/AVIF），配置正确的宽高，用 `loading="lazy"` 懒加载非首屏图片
2. **关键 CSS 内联**：首屏 CSS 直接内联到 HTML，减少请求
3. **预连接关键资源**：`<link rel="preconnect" href="https://cdn.example.com">`
4. **Vite 的预加载**：`import()` 动态导入关键路由

### 14.5.2 INP 优化（Vue 3.4+）

**INP（Interaction to Next Paint，交互到下下一次绘制）**：用户点击按钮/输入文字，到页面实际"动起来"之间的时间。Google 在 2024 年用它取代了 FID。

用一个生活场景理解：你在餐厅点菜（触发交互），服务员记下菜单（浏览器接收事件），厨房做菜（JavaScript 执行），服务员上菜（浏览器渲染）。INP 就是从"点菜"到"上菜"的总时间。INP 越高，用户越感觉"点完没反应"。

**为什么 FID 被淘汰了？** FID 只测量"第一次交互"的延迟，但一个网站可能会被用户交互几十上百次——只测第一次太片面。INP 测量"所有交互"中最慢的一次，更能反映真实体验。

**INP 优化的核心思路是：让 Vue 的响应式更新尽可能快，不要在 watch / computed 里做太重的计算。**

```typescript
// ❌ watch 回调里做了太多事情，INP 差
watch(query, async (q) => {
  // 同步的 heavy computation
  const result = heavyComputation(q)
  // 同步的 DOM 操作
  domUpdate(result)
  // 再发请求
  await fetchData(q)
})

// ✅ 拆分任务，优先更新视图
watch(query, async (q) => {
  // 先立即更新视图（乐观更新）
  pending.value = true
  // 用 nextTick 确保 DOM 已更新，再做重计算
  await nextTick()
  const result = heavyComputation(q)
  domUpdate(result)
  await fetchData(q)
  pending.value = false
})
```

**一个重要的 Vue 性能原则：watch 回调里能 `await` 的都 `await`，不要让同步计算阻塞视图更新。**

### 14.5.3 CLS 优化

CLS（累积布局偏移）衡量页面布局稳定性——想象一下，你正准备点一个按钮，结果页面突然往上跳了一下，你误点到了广告，这就是 CLS 太高。CLS 越低，用户体验越稳定。

优化策略：

1. **给图片和视频设置宽高**：`<img width="800" height="600">`，浏览器会提前为图片预留空间，图片加载时不会挤压其他元素
2. **字体加载优化**：用 `font-display: swap` 避免字体加载时文字跳动——先用系统字体显示，字体加载完再切换
3. **广告位留固定空间**：不要在广告加载后才为其分配空间，提前用 CSS `min-height` 占好位置
4. **动态内容不要插到顶部**：如果页面顶部有动态横幅，不要用 `prepend` 插入，会把整个内容往下挤，用 `append` 加到底部更好

### 14.5.4 在 Vue 中测量 Core Web Vitals

光说不练假把式，我们来实际测量一下应用的性能。Vue 配合 Web Vitals 库，可以轻松拿到真实用户的性能数据：

```bash
pnpm add web-vitals
```

```typescript
// src/utils/vitals.ts
import { onMounted } from 'vue'
import { getCLS, getFID, getLCP, getTTFB } from 'web-vitals'

function sendToAnalytics({ name, value, id }: { name: string; value: number; id: string }) {
  // 上报到你的监控系统（如 Sentry、百度统计等）
  navigator.sendBeacon?.('/api/vitals', JSON.stringify({ name, value, id }))
}

export function useWebVitals() {
  onMounted(() => {
    getCLS(sendToAnalytics)
    getLCP(sendToAnalytics)
    getTTFB(sendToAnalytics)
  })
}
```

在根组件里调用这个 composable，真实用户的 Core Web Vitals 数据就能上报到你的服务器，让你知道真实用户感受到的性能是什么样的——这比 Chrome DevTools 里跑出来的数据准确得多。

## 14.6 错误处理

### 14.6.1 全局错误处理（errorHandler）

```typescript
// main.ts
app.config.errorHandler = (err, instance, info) => {
  console.error('全局错误：', err)
  console.error('组件实例：', instance)
  console.error('错误信息：', info)

  // 上报到监控系统
  fetch('/api/error-report', {
    method: 'POST',
    body: JSON.stringify({
      message: (err as Error).message,
      stack: (err as Error).stack,
      info,
      url: window.location.href
    })
  })
}
```

### 14.6.2 组件级错误边界（errorCaptured）

```typescript
// 父组件
import { ref, errorCaptured } from 'vue'

const hasError = ref(false)

const error = errorCaptured((err, instance, info) => {
  console.error('捕获子组件错误：', err)
  hasError.value = true
  return false  // 阻止继续传播
})
```

### 14.6.3 Promise 错误处理

```typescript
// 全局 Promise 未处理 rejection 警告
window.addEventListener('unhandledrejection', (event) => {
  event.preventDefault()  // 阻止浏览器默认警告
  console.error('未处理的 Promise rejection：', event.reason)
})
```

### 14.6.4 错误上报（Sentry）

```bash
pnpm add @sentry/vue
```

```typescript
import * as Sentry from '@sentry/vue'

Sentry.init({
  app,
  dsn: 'https://xxxxx@sentry.io/xxxxx',
  integrations: [new Sentry.BrowserTracing(), new Sentry.Replay()],
  tracesSampleRate: 0.1  // 采样率 10%
})
```

---

## 本章小结

本章我们系统讲解了 Vue 3 的性能优化六大维度：

- **加载优化**：路由懒加载、组件懒加载、按需引入、预加载预取。
- **渲染优化**：KeepAlive 缓存、虚拟滚动、v-memo、shallowRef 减少响应式追踪。
- **包体积优化**：Tree Shaking、公共依赖抽离、图片压缩、gzip 压缩。
- **SEO 优化**：动态 meta、JSON-LD 结构化数据、SSR 方案。
- **Core Web Vitals**：LCP / FID / CLS 的具体优化手段。
- **错误处理**：全局 errorHandler、errorCaptured、Promise 错误上报、Sentry 集成。

下一章我们会学习 **样式方案**——CSS 预处理器、Tailwind CSS、主题切换和暗色模式，让你的应用既有颜值又有性能！

