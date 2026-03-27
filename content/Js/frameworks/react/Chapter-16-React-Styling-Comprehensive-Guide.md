+++
title = "第16章 React样式全指南"
weight = 160
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-16 - React 样式全解

## 16.1 内联样式

### 16.1.1 内联样式的基本写法

内联样式直接在 JSX 元素的 `style` 属性中传入 JavaScript 对象：

```jsx
function InlineStyleDemo() {
  const styles = {
    container: {
      padding: '20px',
      backgroundColor: '#f5f5f5',
      borderRadius: '8px'
    },
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      color: '#333'
    }
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>内联样式演示</h1>
      <p style={{ color: '#666', fontSize: '14px' }}>
        这是一段内联样式的文字
      </p>
    </div>
  )
}
```

### 16.1.2 动态样式的实现

内联样式的优势是可以轻松实现动态样式：

```jsx
function DynamicStyle({ isActive, size = 'medium' }) {
  const sizeMap = {
    small: { padding: '8px 16px', fontSize: '12px' },
    medium: { padding: '12px 24px', fontSize: '14px' },
    large: { padding: '16px 32px', fontSize: '16px' }
  }

  const styles = {
    container: {
      backgroundColor: isActive ? '#4CAF50' : '#f5f5f5',
      color: isActive ? '#fff' : '#333',
      borderRadius: '8px',
      transition: 'all 0.3s ease',
      ...sizeMap[size]
    }
  }

  return (
    <button style={styles.container}>
      {isActive ? '已激活' : '未激活'}
    </button>
  )
}
```

### 16.1.3 内联样式的优缺点

| 优点 | 缺点 |
|------|------|
| 样式和组件在一起，易于理解 | 不能使用伪类（:hover、:focus 等） |
| 动态样式实现简单 | 不能使用 CSS 动画 |
| 不需要额外的 CSS 文件 | 代码可读性差（大样式对象） |
| 适合简单的动态样式 | 样式不能复用 |

---

## 16.2 CSS Modules

### 16.2.1 CSS Modules 的配置

CSS Modules 在 Vite 中是开箱即用的，不需要额外配置。只需将 CSS 文件命名为 `*.module.css` 即可启用。

```bash
# 目录结构
src/
├── components/
│   ├── Button/
│   │   ├── Button.jsx
│   │   └── Button.module.css  # CSS Modules 文件
```

### 16.2.2 导入方式：`import styles from './Button.module.css'`

```css
/* Button.module.css */
.button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.primary {
  background-color: #4CAF50;
  color: white;
}

.secondary {
  background-color: #2196F3;
  color: white;
}

.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

```jsx
import styles from './Button.module.css'

function Button({ variant = 'primary', disabled = false, children }) {
  return (
    <button
      className={`${styles.button} ${styles[variant]} ${disabled ? styles.disabled : ''}`}
      disabled={disabled}
    >
      {children}
    </button>
  )
}
```

### 16.2.3 生成的类名自动哈希化

CSS Modules 会将类名编译成**唯一的哈希字符串**，避免全局样式冲突：

```html
<!-- 编译前 -->
<button class="button primary">点击</button>

<!-- 编译后（类名被哈希化了） -->
<button class="Button_button__3x7k2 Button_primary__1a2b3">
  点击
</button>
```

---

## 16.3 styled-components

### 16.3.1 styled-components 的安装与配置

```bash
npm install styled-components
```

Vite + React 项目不需要额外配置，直接使用即可。

### 16.3.2 基础写法：`const Button = styled.button`...``

```jsx
import styled from 'styled-components'

// 用 styled.标签名 创建带样式的组件
const Button = styled.button`
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
  background-color: #4CAF50;
  color: white;

  &:hover {
    background-color: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  &:active {
    transform: translateY(0);
  }
`

// 使用
function App() {
  return <Button>点击我</Button>
}
```

### 16.3.3 props 驱动样式：传入 props 改变样式

styled-components 最大的特点是**样式可以通过 props 动态控制**：

```jsx
const Button = styled.button`
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;

  /* 通过 props 控制背景色 */
  background-color: ${props => {
    if (props.$variant === 'primary') return '#4CAF50'
    if (props.$variant === 'danger') return '#f44336'
    if (props.$variant === 'outline') return 'transparent'
    return '#2196F3'
  }};

  /* 通过 props 控制文字颜色 */
  color: ${props => props.$variant === 'outline' ? '#2196F3' : 'white'};

  /* 通过 props 控制边框 */
  border: ${props => props.$variant === 'outline' ? '2px solid #2196F3' : 'none'};
`

function App() {
  return (
    <div>
      <Button $variant="primary">主要按钮</Button>
      <Button $variant="danger">危险按钮</Button>
      <Button $variant="outline">边框按钮</Button>
    </div>
  )
}
```

### 16.3.4 样式继承：styled(Button)

```jsx
// 基于现有的 Button 创建新的变体
const DangerButton = styled(Button)`
  background-color: #f44336;
  &:hover {
    background-color: #d32f2f;
  }
`

const LargeButton = styled(Button)`
  padding: 16px 32px;
  font-size: 18px;
`
```

### 16.3.5 全局样式与主题（ThemeProvider）

```jsx
import { ThemeProvider, createGlobalStyle } from 'styled-components'

// 全局样式
const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background-color: ${props => props.theme.background};
    color: ${props => props.theme.text};
  }
`

// 主题定义
const theme = {
  light: {
    background: '#ffffff',
    text: '#333333'
  },
  dark: {
    background: '#1a1a1a',
    text: '#ffffff'
  }
}

function App() {
  return (
    <ThemeProvider theme={theme.dark}>
      <GlobalStyle />
      <div>应用内容</div>
    </ThemeProvider>
  )
}
```

---

## 16.4 Tailwind CSS

### 16.4.1 Tailwind 的核心理念：原子化 CSS

**Tailwind CSS** 是一个"原子化 CSS"框架。它的理念是：**不提供预制的组件样式，而是提供一堆"工具类"（Utility Classes），让你像搭积木一样组合样式**。

```jsx
// 传统 CSS：定义一个 button 类
// .btn { padding: 12px 24px; background: blue; color: white; }
// <button class="btn">点击</button>

// Tailwind：直接用工具类组合
<button className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
  点击
</button>
```

### 16.4.2 在 Vite + React 中配置 Tailwind

```bash
# 安装 Tailwind CSS
npm install -D tailwindcss postcss autoprefixer

# 初始化 Tailwind 配置
npx tailwindcss init -p
```

```js
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  // ============================================================
  // content：指定哪些文件需要被 Tailwind 扫描并生成样式
  // ============================================================
  // - "./index.html"：扫描入口 HTML 文件（如果有 Tailwind 工具类直接写在 HTML 里）
  // - "./src/**/*.{js,ts,jsx,tsx}"：扫描 src 目录下所有 JS/TS/JSX/TSX 文件
  // - 为什么要配置这个？Tailwind 只会为"实际使用到的"类名生成 CSS
  //   （也叫"按需生成"，不是全量生成），所以必须告诉它去哪些文件里找类名
  // - 如果你的组件在其他目录，也要加进去，比如："./components/**/*.{js,jsx}"
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],

  // ============================================================
  // theme：自定义设计令牌（Design Tokens）
  // ============================================================
  // - 覆盖 Tailwind 的默认配置，定义项目的颜色、字体、间距等
  // - extend: 在默认配置基础上扩展，而不是完全替换
  //   （如果不写 extend，默认值会被覆盖掉）
  // - 常用可配置项：
  //   - colors: 自定义颜色（如 brand）
  //   - spacing: 自定义间距
  //   - fontFamily: 自定义字体
  //   - borderRadius: 自定义圆角
  //   - 等等……几乎所有 Tailwind 类名对应的 CSS 属性都可以在这里配置
  theme: {
    extend: {
      colors: {
        brand: '#4CAF50',  // 自定义品牌色，之后可用 bg-brand、text-brand 等
      }
    },
  },

  // ============================================================
  // plugins：Tailwind 官方或社区插件
  // ============================================================
  // - 插件可以扩展 Tailwind 的功能，提供额外的工具类
  // - 常用插件：
  //   - @tailwindcss/forms：表单样式重置（需要先安装：npm install -D @tailwindcss/forms）
  //   - @tailwindcss/typography：文章/文档排版（npm install -D @tailwindcss/typography）
  //   - @tailwindcss/aspect-ratio：宽高比控制
  // - 数组为空表示暂不启用任何插件
  plugins: [],
}
```

```css
/* src/index.css */

/* ============================================================
 * Tailwind 的三大指令（必须按顺序写！）
 * ============================================================ */
// @tailwind base：注入 Tailwind 的 CSS 重置（normalize/reset），
//                 包含盒模型、字体、浏览器默认样式重置等基础样式
@tailwind base;

// @tailwind components：注入 Tailwind 的组件类（container、card 等），
//                       以及你在 @layer components 里定义的类
@tailwind components;

// @tailwind utilities：注入所有工具类（px-4、flex、text-center 等），
//                     这是 Tailwind 的核心，生成各种原子化的工具类 CSS
@tailwind utilities;

/* ============================================================
 * @layer：组织自定义样式，避免与 Tailwind 冲突
 * ============================================================ */
// @layer base：自定义基础样式（覆盖 Tailwind 默认值）
//              这里的样式优先级高于 @tailwind base
@layer base {
  body {
    // @apply：把 Tailwind 工具类"转换"成普通 CSS，等价于：
    // body { background-color: rgb(243 244 246); color: rgb(31 41 55); }
    @apply bg-gray-100 text-gray-800;
  }
}

/* @layer components：自定义可复用的组件类 */
@layer components {
  .btn-primary {
    @apply px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition;
  }
}

/* @layer utilities：自定义工具类（一般很少用） */
@layer utilities {
  /* 例如：自定义一个旋转动画工具类 */
  .animate-spin-slow {
    animation: spin 2s linear infinite;
  }
}
```

### 16.4.3 常用工具类一览

| 工具类 | 作用 | 示例 |
|-------|------|------|
| `px-4 py-2` | 内边距 | `padding: 16px 8px` |
| `mx-auto` | 水平居中 | `margin-left: auto; margin-right: auto` |
| `flex items-center justify-between` | Flexbox 布局 | 弹性盒模型 |
| `grid grid-cols-3 gap-4` | 网格布局 | 3列网格，间距16px |
| `text-center text-xl font-bold` | 文字样式 | 居中、20px、加粗 |
| `bg-blue-500 text-white rounded-lg` | 背景和圆角 | 蓝色背景、白色文字、圆角 |
| `hover:bg-blue-600 focus:ring-2` | 交互状态 | 悬停、聚焦样式 |
| `md:flex lg:grid-cols-4` | 响应式断点 | 中屏、大屏不同样式 |
| `dark:bg-gray-900` | 深色模式 | 深色主题适配 |

### 16.4.4 使用 @apply 复用样式

```css
/* 在 CSS 文件里定义可复用的类 */
@layer components {
  .btn {
    @apply px-6 py-3 rounded-lg font-semibold transition-all duration-200;
  }

  .btn-primary {
    @apply btn bg-blue-500 text-white hover:bg-blue-600;
  }

  .btn-danger {
    @apply btn bg-red-500 text-white hover:bg-red-600;
  }
}
```

### 16.4.5 Tailwind 的动态类名问题

```jsx
// ❌ 错误：Tailwind 不能识别动态拼接的类名
const color = 'blue'
<div className={`bg-${color}-500`}>动态颜色</div>

// ✅ 正确：使用完整字面量类名
const color = 'blue'
<div className="bg-blue-500">静态颜色</div>

// ✅ 动态颜色方案：使用 style 结合 Tailwind
<div
  className="rounded-lg px-4 py-2"
  style={{ backgroundColor: dynamicColor }}
>
  动态背景色
</div>

// ✅ 或者使用 Tailwind 的任意值语法
<div className={`bg-[${dynamicColor}]`}>
  任意值语法
</div>
```

---

## 16.5 Sass/Less

### 16.5.1 Sass/Less 的安装

```bash
# Sass 安装
npm install -D sass

# Less 安装
npm install -D less
```

Vite 原生支持 Sass，不需要额外配置。Less 也只需要安装即可。

### 16.5.2 变量、嵌套、混入（Mixins）的使用

```scss
/* Button.scss */

// 变量
$primary-color: #4CAF50;
$secondary-color: #2196F3;
$border-radius: 8px;
$spacing: 12px;

// 混入（Mixin）
@mixin flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

@mixin button-base {
  padding: $spacing 2 * $spacing;
  border: none;
  border-radius: $border-radius;
  cursor: pointer;
  transition: all 0.2s ease;
}

// 嵌套
.button {
  @include button-base;
  @include flex-center;

  background-color: $primary-color;
  color: white;

  &:hover {
    background-color: darken($primary-color, 10%);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  &:active {
    transform: translateY(0);
  }

  &--secondary {
    background-color: $secondary-color;

    &:hover {
      background-color: darken($secondary-color, 10%);
    }
  }

  &--disabled {
    opacity: 0.5;
    cursor: not-allowed;

    &:hover {
      transform: none;
      box-shadow: none;
    }
  }
}
```

```jsx
// Button.jsx
import './Button.scss'

function Button({ variant = 'primary', disabled = false, children }) {
  return (
    <button
      className={`button button--${variant} ${disabled ? 'button--disabled' : ''}`}
      disabled={disabled}
    >
      {children}
    </button>
  )
}
```

### 16.5.3 在 Vite 中配置 Sass

Vite 已经内置了对 Sass 的支持，不需要额外配置。但如果你需要自定义 Sass 选项：

```js
// vite.config.js
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        // additionalData：在每个 SCSS 文件的**开头**自动注入的内容
        // ============================================================
        // 作用：全局注入变量/混入文件，从此每个 .scss 都不用手写 @import
        // 例如：在 variables.scss 里定义了 $primary-color: #4CAF50;
        //       配置后所有组件的 .scss 都能直接用 $primary-color
        // ============================================================
        // 语法要点：@import 语句末尾**必须以 ; 结尾**，否则 Sass 编译会报错
        // 路径说明：这里的路径相对于**项目根目录**（不是当前配置文件）
        additionalData: `@import "./src/styles/variables.scss";`,

        // 其他常用 scss 选项（了解即可）：
        // - silenceDeprecations: 静默某些弃用警告，如 'import'（Sass 未来版本会移除 @import）
        // - api: 'modern-compiler' | 'modern' | 'legacy'
        //   - 'modern-compiler'：使用 Dart Sass 现代编译器（更快，Vite 5.1+ 支持）
        //   'legacy'：传统编译器（默认，兼容性好）
      }
    }
  }
})
```

---

## 16.6 CSS 方案对比与选型

### 16.6.1 styled-components vs emotion vs linaria

| 方案 | 特点 | 适用场景 |
|------|------|---------|
| **styled-components** | 最流行，生态完善 | 中大型项目 |
| **emotion** | 性能更好，体积更小 | 性能敏感型应用 |
| **linaria** | 零运行时，使用 CSS-in-JS 语法但**编译时**直接生成 .css 文件 | SSR 友好、包体积极小 |

### 16.6.2 CSS Modules vs Tailwind vs CSS-in-JS：如何选择

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **CSS Modules** | 原生支持、简单直观 | 动态样式稍繁琐 | 中小型项目、组件库 |
| **Tailwind CSS** | 开发效率高、一致性好 | 学习曲线、HTML 较乱 | 快速开发、中大型项目 |
| **CSS-in-JS** | 样式和组件绑定、动态样式强 | 运行时开销、包体积大 | 动态样式多的应用 |
| **Sass/Less** | 预处理能力强、成熟稳定 | 需要构建工具 | 传统项目、喜欢预处理的项目 |

> 💡 **选型建议**：
> - 快速原型 → Tailwind CSS
> - 组件库/设计系统 → CSS Modules 或 styled-components
> - 需要强动态样式 → styled-components 或 emotion
> - 团队有预处理经验 → Sass/Less
> - SSR 优先 → CSS Modules 或 linaria

---

## 本章小结

本章我们对 React 的样式方案进行了全景式梳理：

- **内联样式**：适合简单动态样式，但不能用伪类和动画
- **CSS Modules**：Vite 原生支持，类名哈希化避免冲突，适合组件级样式
- **styled-components**：CSS-in-JS 方案，样式通过 props 动态控制，适合需要强动态样式的场景
- **Tailwind CSS**：原子化 CSS，通过工具类组合样式，开发效率极高，正在席卷前端圈
- **Sass/Less**：传统预处理方案，变量、嵌套、混入让 CSS 编写更优雅

没有"最好"的样式方案，只有"最适合"的方案。根据项目规模、团队偏好、动态样式需求来选择！下一章我们将学习 **React Router v7**——React 的路由管理神器！🛣️