+++
title = "第15章 样式方案"
weight = 150
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十五章 样式方案

> CSS 是 Vue 应用的门面。好看的样式能让用户愉悦，难看的样式能让人崩溃。本章我们会讲解 Vue 项目中的各种样式解决方案——CSS 预处理器（SCSS/Less/Stylus）、UnoCSS 原子化方案、CSS 变量实现主题切换、暗色模式适配。这些工具组合起来，能让你的样式开发效率提升好几倍。

## 15.1 样式基础

### 15.1.1 scoped 样式隔离

每个 `.vue` 文件的 `<style scoped>` 只对当前组件生效，不会污染其他组件。这是 Vue 单文件组件最常用的样式隔离方式。

**为什么需要 scoped？** 想象一下，你的项目有 10 个组件，其中 8 个都用了一个叫 `.title` 的 class。如果没有 scoped，这 8 个组件的 `.title` 会互相覆盖——后编译的组件样式会覆盖先编译的，结果就是谁的 class 名先注册谁就赢，完全不可控。scoped 就是来解决这个"样式串台"问题的。

scoped 的工作原理是：Vue 会在编译时给模板里的每个元素加上一个唯一的 `data-v-xxxxx` 属性（xxxxx 是随机生成的哈希值），同时把 CSS 选择器都变成 `[data-v-xxxxx] .title`。这样，每个组件的样式只作用于加了对应属性标记的元素，和其他组件井水不犯河水。

```vue
<style scoped>
.card {
  padding: 16px;
}

/* 编译后实际生成的 CSS 会变成：*/
/* .card[data-v-xxxxxxxx] { padding: 16px; } */
/* Vue 通过给元素加 data-v-xxxxx 属性，让样式精准命中目标元素 */
</style>
```

什么时候用 scoped，什么时候用全局样式？原则很简单：**绝大多数样式都加 scoped，只有那些"人人需要"的样式才不加**——比如 CSS 重置（`* { margin: 0 }`）、全局字体设置、动画定义等。

### 15.1.2 深度选择器（:deep / ::v-deep）

想给子组件内部元素加样式时用 `:deep()`：

```vue
<style scoped>
/* 穿透到子组件内部 */
:deep(.el-input__inner) {
  border-radius: 20px;
}

/* ::v-deep 是旧语法，和 :deep 效果一样 */
::v-deep(.el-dialog__body) {
  padding: 0;
}
</style>
```

### 15.1.3 全局样式与局部样式

```vue
<style>
/* 没有 scoped，就是全局样式 */
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
}
</style>

<style scoped>
/* 有 scoped，只影响当前组件 */
.button {
  background: #42b883;
}
</style>
```

### 15.1.4 Shadow DOM 支持（Vue 3.5+）

Vue 3.5 为组件样式引入了 Shadow DOM 支持，这是 Web Components 标准的一部分。用 `:host` 选择器可以给组件的根元素本身加样式，这在做**可复用的 UI 组件库**时特别有用——组件的样式完全封装，不会泄漏到外部，也不受外部样式影响。

```vue
<!-- 组件的根元素就是 :host -->
<style>
:host {
  display: block;
  /* CSS 变量可以通过 shadow DOM 渗透到组件内部 */
  --primary-color: #42b883;
  /* 也可以在这里设置组件的默认 display 类型 */
}

:host([disabled]) {
  opacity: 0.5;
  pointer-events: none;
}
</style>
```

`:host` 还有一个很酷的特性：**可以通过 HTML 属性选择器来根据组件的属性来改变样式**。比如 `:host([type="danger"])` 可以让组件在传入 `type="danger"` 属性时显示不同的样式。这种"组件 스스로 根据属性改变外观"的能力，是 Shadow DOM 带来的原生能力，不需要 JavaScript 逻辑。

## 15.2 CSS 预处理器——让 CSS 也能"编程"

原生 CSS 的问题相信你深有体会：没有变量、没有函数、不能嵌套，写久了就像用记事本写小说——能写，但很憋屈。

**CSS 预处理器**就是在 CSS 之上加了一层"编译器"：你写的是一种"类 CSS"的特殊语法（变量、嵌套、Mixin、函数等），经过编译器处理后，生成普通 CSS 文件。这个过程就像 TypeScript 编译成 JavaScript——你用更强大的语法写代码，生产环境得到的是普通 CSS。

目前最主流的三种预处理器是：
- **SCSS / Sass**：功能最全面，社区最大，Vue 官方文档用的就是 SCSS
- **Less**：语法简洁，适合不喜欢 SCSS 那种"括号语法"的人
- **Stylus**：极度简洁，连大括号和分号都可以省略，极客最爱

### 15.2.1 Sass / SCSS

SCSS（Sassy CSS）是 Sass 语言的两种语法之一（另一种叫"缩进语法"，`.sass` 后缀）。SCSS 是"CSS 超集"——所有普通 CSS 语法在 SCSS 里都是合法的，写惯了 CSS 的人可以无缝切换。功能强大、生态成熟，是目前最流行的选择。

```bash
pnpm add -D sass
```

```scss
// 变量定义
$primary-color: #42b883;
$border-radius: 8px;
$font-size-base: 14px;

// 嵌套规则（避免重复写父选择器）
.card {
  padding: 16px;

  .title {
    font-size: 18px;
    font-weight: bold;
  }

  // & 表示父选择器
  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  // &--modifier 命名法（BEM）
  &--active {
    border-color: $primary-color;
  }
}

// 混入（Mixin）：可复用的样式块
@mixin flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

@mixin text-ellipsis($lines: 1) {
  overflow: hidden;
  @if $lines == 1 {
    text-overflow: ellipsis;
    white-space: nowrap;
  } @else {
    display: -webkit-box;
    -webkit-line-clamp: $lines;
    -webkit-box-orient: vertical;
  }
}

.container {
  @include flex-center;
}

.title {
  @include text-ellipsis(2);
}

// 继承（Extend）
%button-base {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  @extend %button-base;
  background: $primary-color;
  color: white;
}
```

### 15.2.2 Less——比 SCSS 更简洁的预处理器

Less 和 SCSS 的功能几乎一样——同样支持变量、嵌套、Mixin、继承。但 Less 的语法更接近 CSS，上手更快，特别适合不喜欢 SCSS 那套括号语法的人。

Less 和 SCSS 最大的区别是**变量声明符号**：SCSS 用 `$primary-color`，Less 用 `@primary-color`。

```bash
pnpm add -D less
```

```less
// 变量：Less 用 @ 声明（SCSS 用 $）
@primary-color: #42b883;

// 嵌套：和 SCSS 几乎一样
.card {
  padding: 16px;
  .title {
    font-size: 18px;
  }
  // & 表示父选择器（和 SCSS 一样）
  &:hover {
    background: #f5f5f5;
  }
}

// 混入：Less 用 () 定义 Mixin
// 注意：Less 的 Mixin 定义时带括号，和 SCSS 用 @mixin 稍有不同
.flex-center() {
  display: flex;
  justify-content: center;
  align-items: center;
}

// 使用混入：用 .类名() 调用
.container {
  .flex-center();
}
```

**Less vs SCSS 该选哪个？**

| | SCSS | Less |
|---|---|---|
| 变量符号 | `$` | `@` |
| 社区生态 | 更大（Vue 官方文档用 SCSS） | 较小 |
| 学习曲线 | 稍陡 | 平缓 |
| 特色 | 功能最全 | 语法最接近 CSS |

### 15.2.3 Stylus——极简主义的预处理器

Stylus 是三个预处理器里最"极简"的——它连大括号 `{}`、冒号 `:`、分号 `;` 都可以省略。用 Stylus 写样式，就像是用"人类自然语言"写代码。

```bash
pnpm add -D stylus
```

```stylus
// 变量：不用 $，直接用等号赋值（和普通编程语言一样）
primary-color = #42b883

// 缩进语法：大括号完全不需要！
// 想象一下，不用写任何一个 {} 或 ; 就能写 CSS
.card
  padding 16px
  .title
    font-size 18px
  &:hover
    background #f5f5f5

// 混入（MIXIN）也用缩进表示
flex-center()
  display flex
  justify-content center
  align-items center

.container
  flex-center()
```

Stylus 的哲学是"当你写得越少，编译器帮你补全"。如果你喜欢极简风格，Stylus 会让你写代码有"行云流水"的感觉。但它的缺点是：团队协作时，缩进格式必须严格统一，否则很容易出 bug。如果你和队友习惯了大括号风格，SCSS 或 Less 可能更安全。

```bash
pnpm add -D stylus
```

```stylus
// 变量（不用 $，直接用 =）
primary-color = #42b883

// 缩进语法，不需要大括号
.card
  padding 16px
  .title
    font-size 18px
  &:hover
    background #f5f5f5
```

## 15.3 Tailwind CSS——不用写 CSS 的 CSS 方案

写传统 CSS 的时候，你是不是经常遇到这种痛苦——写一个按钮，要同时改 `.css` 文件和 `.vue` 文件；改了 class 名，其他地方用到的样式全乱了；想复用一套按钮样式，得抽成一个公共组件……有没有一种方式，可以**在 HTML 里直接写样式**，不用切换到单独的 CSS 文件？

**Tailwind CSS** 就是这个思路。它把 CSS 的每一个属性都拆成了原子级别的"工具类"：`flex` = `display: flex`，`text-xl` = `font-size: 1.25rem`，`bg-primary` = `background-color: primary`，你只需要在 HTML 标签上堆叠这些工具类，就能完成整个界面，而不需要写一行传统的 CSS 代码。

这种写法的最大好处是：**样式和 HTML 在同一个地方**，你不需要在 `.vue`、`.css`、`.scss` 之间来回横跳。改样式直接改 HTML，改 HTML 直接改样式，效率拉满。

### 15.3.1 安装与配置

```bash
pnpm add -D tailwindcss postcss autoprefixer
pnpm exec tailwindcss init -p
```

```js
// tailwind.config.js
module.exports = {
  // content：告诉 Tailwind 需要扫描哪些文件来生成 CSS
  // Tailwind 会从这些文件里找到用到的工具类，只生成对应的 CSS（实现按需打包）
  // './index.html' → 扫描入口 HTML
  // './src/**/*.{vue,js,ts}' → 扫描 src 目录下所有 .vue、.js、.ts 文件
  // 常见问题：加了新工具类但没生效？很可能是文件没加到 content 里！
  content: ['./index.html', './src/**/*.{vue,js,ts}'],

  // theme：自定义设计系统（覆盖 Tailwind 默认值）
  theme: {
    extend: {
      // extend.colors：扩展主题色
      // 有了这个配置后，模板里就能用 bg-primary、text-primary 等工具类
      colors: {
        primary: '#42b883'  // 定义主色（可自定义任意名字和色值）
        // 'primary-dark': '#35495e'  // 示例：再定义一个深色主色
      }
    }
  },

  // plugins：Tailwind 官方或社区的插件（需要先 pnpm add 安装）
  // 常用插件如 @tailwindcss/forms（表单样式重置）、@tailwindcss/typography（文章排版）
  plugins: []
  // plugins: [require('@tailwindcss/forms')]  // 示例：安装表单插件
}
```

```css
/* src/assets/main.css */
/* @tailwind 是 Tailwind 的指令，会在构建时替换成实际的 CSS */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 15.3.2 常用工具类

```vue
<template>
  <!-- 布局 -->
  <div class="flex items-center justify-between p-4">
    <!-- 间距 -->
    <div class="m-4 p-4">
      <!-- 字体 -->
      <p class="text-xl font-bold text-gray-700">
        标题
      </p>
      <!-- 颜色 -->
      <button class="bg-primary text-white px-4 py-2 rounded hover:bg-blue-600">
        按钮
      </button>
    </div>
  </div>
</template>
```

### 15.3.3 响应式设计

Tailwind 的响应式设计基于**断点（Breakpoint）**。每个断点对应一个媒体查询，当屏幕宽度达到阈值时，对应的样式就会生效：

| 前缀 | 最小宽度 | 对应屏幕尺寸 |
|------|---------|-------------|
| `sm:` | 640px | 平板竖屏（>= 640px）|
| `md:` | 768px | 平板横屏（>= 768px）|
| `lg:` | 1024px | 小笔记本（>= 1024px）|
| `xl:` | 1280px | 台式机（>= 1280px）|
| `2xl:` | 1536px | 大屏（>= 1536px）|

**工作原理**：加了 `sm:` 前缀的类，只在屏幕宽度 >= 640px 时生效；不加前缀的类，则在所有屏幕宽度生效（"手机优先"）。

```vue
<!-- grid-cols-1：默认（所有屏幕）都是 1 列 -->
<!-- sm:grid-cols-2：>= 640px 时变成 2 列 -->
<!-- md:grid-cols-3：>= 768px 时变成 3 列 -->
<!-- lg:grid-cols-4：>= 1024px 时变成 4 列 -->
<!-- 这样就可以用一套代码适配手机→平板→电脑 -->
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
  <div v-for="item in items" :key="item.id">{{ item.name }}</div>
</div>
```

**实战技巧**：
- 移动端优先：先写手机样式（不用前缀），再逐级加断点
- 常用断点组合：`sm:` 处理平板，`lg:` 处理笔记本，`xl:` 处理大屏
- Tailwind 的响应式不需要写任何 `@media` 查询语句，只需要在工具类前加前缀即可

### 15.3.4 自定义配置

通过 `theme.extend` 可以扩展 Tailwind 的默认配置（在保留所有默认工具类的基础上增加新配置）：

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      // colors：扩展主题色（覆盖方式见下）
      colors: {
        primary: '#42b883',        // 基础主色：bg-primary、text-primary
        'primary-dark': '#35495e'  // 深色主色：bg-primary-dark
      },

      // borderRadius：自定义圆角值
      // 命名规范：和 Tailwind 默认名不冲突，用自定义名如 'xl'、'2xl'
      // 使用方式：rounded-xl、rounded-2xl
      borderRadius: {
        'xl': '1rem',   // 16px 圆角
        '2xl': '1.5rem' // 24px 圆角
      },

      // boxShadow：自定义阴影
      // Tailwind 默认有 shadow-sm、shadow、shadow-lg 等
      // 自定义阴影可以直接起名，用法：shadow-card
      boxShadow: {
        'card': '0 2px 8px rgba(0, 0, 0, 0.1)' // 卡片阴影
      }
    }
  }
  // 如果不用 extend，想直接替换整个 theme（而不是扩展），去掉 extend: {} 这一层，直接写在 theme: {} 里
}
}
```

### 15.3.5 UnoCSS——更快的原子化 CSS（新时代选择）

如果说 Tailwind CSS 是"瑞士军刀"，那 **UnoCSS** 就是"激光剑"——同样都是原子化 CSS，但 UnoCSS 更快、更强、更灵活。UnoCSS 是 Anthony Fu（Vue/Vite 核心团队成员）开发的，它的核心理念和 Tailwind 一脉相承，但提供了更强大的自定义能力和更快的性能。

UnoCSS 凭什么比 Tailwind 更快？因为它基于**虚拟 CSS**——不像 Tailwind 那样生成一大段真实的 CSS 字符串，UnoCSS 的工具类是在运行时按需生成的，体积可以压缩到极致。

**安装 UnoCSS：**

```bash
pnpm add -D unocss
```

**配置（`uno.config.ts`）：**

```typescript
// uno.config.ts
import { defineConfig, presetUno, presetAttributify, presetIcons } from 'unocss'

export default defineConfig({
  // presetUno 是 UnoCSS 的核心预设，提供和 Tailwind 类似的工具类
  presets: [
    presetUno(),
    // attributify 预设：可以在 HTML 属性里直接写工具类，而不用写一堆 class
    presetAttributify(),
    // icons 预设：自动把图标名转换成 SVG
    // 图标从 CDN 按需加载，不需要预先安装图标库
    presetIcons({
      scale: 1.2,  // 图标相对于文字大小的倍数（如文字 16px，图标的 font-size = 16 * 1.2）
      // cdn：图标 SVG 文件从哪里加载
      // 'https://esm.sh/' → 从 esm.sh CDN 按需获取（推荐，无需本地安装图标库）
      // 'https://cdn.jsdelivr.net/npm/' → jsdelivr CDN
      // 或者不填 cdn，在项目里本地安装图标库：pnpm add @iconify-json/carbon
      cdn: 'https://esm.sh/'
    })
  ],

  // 自定义主题色
  theme: {
    colors: {
      primary: '#42b883'
    }
  }
})
```

**在 Vite 中引入：**

```typescript
// vite.config.ts
import UnoCSS from 'unocss/vite'

export default {
  plugins: [
    UnoCSS()  // 放在 vue() 之后也行
  ]
}
```

```typescript
// main.ts
import 'virtual:uno.css'  // 引入生成的 CSS
```

**在 Vue 组件中使用：**

```vue
<!-- 基础工具类（和 Tailwind 几乎一样） -->
<div class="flex items-center justify-between p-4">
  <p class="text-xl font-bold text-gray-700">标题</p>
  <button class="bg-primary text-white px-4 py-2 rounded hover:bg-blue-600">
    按钮
  </button>
</div>

<!-- attributify 模式：工具类写在 HTML 属性里，看起来更整洁 -->
<template>
  <button
    flex="~"
    items-center
    justify-center
    px-4
    py-2
    bg="primary hover:blue-600"
    text="white"
    rounded
  >
    图标按钮
  </button>
</template>
```

**用图标（presetIcons）：**

```vue
<!-- 直接写图标名，自动从 CDN 获取 SVG -->
<div class="i-carbon-sun dark:i-carbon-moon" />
<div class="i-logos-vue text-3xl" />
<div class="i-carbon-settings" />
```

UnoCSS 的图标库非常丰富，支持 Carbon、Lucide、Tabler 等主流图标集，只需要知道图标名就能用，不需要下载任何东西。

**UnoCSS vs Tailwind CSS 怎么选？**

| | UnoCSS | Tailwind CSS |
|---|---|---|
| 性能 | 极快（虚拟 CSS） | 快 |
| 图标集成 | 内置（esm.sh CDN） | 需额外安装 |
| 自定义程度 | 极高 | 高 |
| 生态 | 较新，社区增长中 | 成熟稳定 |
| 学习曲线 | 稍陡（新概念多） | 平缓 |
| 推荐场景 | Vite 项目、追求极致性能 | 任意项目，尤其不熟悉新工具的团队 |

**如果你用 Vite 创建 Vue 项目，UnoCSS 是更现代的选择**——它和 Vite 出自同一团队，集成度极高，社区也越来越活跃。但如果你的团队更熟悉 Tailwind 的生态，或者项目需要长期维护，Tailwind 也是完全可靠的选择。无论选哪个，原子化 CSS 都是提升样式开发效率的利器。

## 15.4 主题与暗色模式

### 15.4.1 CSS 变量实现主题切换

```css
/* src/assets/variables.css */
:root {
  --primary-color: #42b883;
  --bg-color: #ffffff;
  --text-color: #333333;
  --border-color: #e5e5e5;
}

/* 暗色主题 */
[data-theme="dark"] {
  --primary-color: #35495e;
  --bg-color: #1a1a1a;
  --text-color: #e5e5e5;
  --border-color: #333333;
}
```

```vue
<script setup>
// 切换主题
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme')
  document.documentElement.setAttribute(
    'data-theme',
    current === 'dark' ? 'light' : 'dark'
  )
}
</script>

<style scoped>
.card {
  background: var(--bg-color);
  color: var(--text-color);
  border: 1px solid var(--border-color);
}
</style>
```

### 15.4.2 动态主题切换

```typescript
import { watch } from 'vue'

function setTheme(theme: 'light' | 'dark') {
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

// 初始化
const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null
setTheme(savedTheme || 'light')

// 监听系统主题变化
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (!localStorage.getItem('theme')) {
    setTheme(e.matches ? 'dark' : 'light')
  }
})
```

### 15.4.3 prefers-color-scheme 媒体查询

```css
@media (prefers-color-scheme: dark) {
  :root {
    --primary-color: #35495e;
    --bg-color: #1a1a1a;
  }
}
```

### 15.4.4 Element Plus / Ant Design Vue 主题配置

```bash
# Element Plus 在线主题生成器：https://element-plus.org/zh-CN/guide/theming.html
# 生成后下载主题文件，在 main.ts 中引入
import 'element-plus/theme-chalk/dark/css-vars.css'
```

---

## 本章小结

本章我们学习了 Vue 项目的样式解决方案：

- **scoped 样式隔离**：每个组件的样式独立，不会互相污染。
- **CSS 预处理器**：SCSS 的变量、嵌套、Mixin、Extend 四大特性让 CSS 开发效率大幅提升。
- **Tailwind CSS**：原子化 CSS 方案，通过组合工具类快速构建界面。
- **CSS 变量 + 主题切换**：用 CSS 变量实现动态主题和暗色模式，`prefers-color-scheme` 监听系统主题。

下一章我们会学习 **动画与过渡**——Vue 内置的 transition 系统、列表过渡、状态过渡和第三方动画库，让你的应用动起来！

