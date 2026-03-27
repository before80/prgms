+++
title = "第36章 React工程化与架构"
weight = 360
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-36 - React 工程化与架构

## 36.1 项目目录结构设计

### 36.1.1 feature-based 结构

按功能/业务模块组织代码，适合中大型项目。

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── api/
│   └── products/
└── shared/
    ├── components/
    ├── hooks/
    └── utils/
```

### 36.1.2 常用目录划分

| 目录 | 职责 |
|------|------|
| `components/` | 公共 UI 组件 |
| `pages/` | 页面组件 |
| `hooks/` | 自定义 Hooks |
| `utils/` | 工具函数 |
| `api/` | API 请求 |
| `stores/` | 状态管理 |
| `types/` | TypeScript 类型 |
| `constants/` | 常量配置 |

---

## 36.2 代码质量

### 36.2.1 ESLint + Prettier 配置

```bash
npm install -D eslint prettier
npm install -D eslint-config-prettier eslint-plugin-prettier
```

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended",
    "eslint-config-prettier"  // prettier 必须放在最后，用于关闭与 Prettier 冲突的 ESLint 规则
  ],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error",  // 将 Prettier 格式化问题报告为 ESLint 错误
    "react/react-in-jsx-scope": "off",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
```

> ⚠️ **注意**：`eslint-config-prettier` 必须放在 `extends` 数组的**最后一位**！否则它会覆盖其他规则，让你的 Prettier 配置失效。同理，`eslint-plugin-prettier` 建议配合 `eslint-config-prettier` 使用，否则可能重复检查。

### 36.2.2 Conventional Commits 提交规范

```
feat: 添加了新功能
fix: 修复了 bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
test: 测试相关
chore: 构建/工具相关
```

### 36.2.3 husky + lint-staged：Git Hooks

```bash
npm install -D husky lint-staged
```

```json
// package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"]
  }
}
```

---

## 36.3 Storybook 组件文档

### 36.3.1 安装与启动

Storybook 为每个组件搭建了一个独立的"游乐场"，让你在不影响主应用的情况下开发、测试、文档化 UI 组件。

```bash
# 在已有项目中初始化（推荐）
npx storybook@latest init --type react

# 启动 Storybook 开发服务器（默认 localhost:6006）
npm run storybook
```

> 💡 首次运行会创建 `.storybook/` 配置目录和 `src/stories/` 示例文件夹，可以直接删掉示例，用自己的组件开始。

### 36.3.2 编写组件文档

Storybook 使用**故事（Story）** 来描述一个组件在不同状态下的渲染结果。每个故事对应组件的一种用法。

```jsx
// Button.stories.jsx
import React from 'react'
import { Button } from './Button'

export default {
  // title：Storybook 左侧边栏中的分组路径，支持嵌套（'Form/Button/Primary' 会显示为 Form > Button > Primary）
  // 命名惯例：通常以组件路径或类别命名，方便在 Storybook 中快速找到
  title: 'Components/Button',
  // component：关联真实组件，Storybook 会自动读取组件的 PropTypes 或 TypeScript 类型，
  // 并在 Controls 面板中生成对应的表单控件
  component: Button,
  // argTypes：描述每个 prop 在 Controls 面板中的控制方式（定义在 default export 中，为所有 story 共享）
  // 不声明 argTypes 时，Storybook 会自动根据 prop 类型推断控件；但若要自定义控件类型（如 select 下拉），
  // 则必须在 argTypes 中显式声明
  argTypes: {
    variant: {
      // control：指定在 Storybook UI 中用哪种控件编辑这个 prop
      // 可选值：'text' | 'boolean' | 'number' | 'range' | 'select' | 'radio' | 'check' | 'color' | 'date'
      // select 会渲染为下拉选择框，最适合有固定枚举值的 prop
      control: 'select',
      // options：当 control 为 'select' 或 'radio' 时，定义可选值列表
      options: ['primary', 'secondary']
    }
  }
}

// 每一种渲染状态就是一个 named export（一个"故事"）
// Storybook 会将每个 named export 识别为一个独立的 Story，在侧边栏显示为单独条目
export const Primary = {
  // args：该故事的默认 props 值（会合并到 component 的 props 上）
  // 在 Storybook UI 中修改 args，预览会实时更新，适合手动测试各种 prop 组合
  args: {
    label: '点击我',
    variant: 'primary'
  }
}

export const Secondary = {
  args: {
    label: '取消',
    variant: 'secondary'
  }
}
```

几个关键概念：
- **`title`**：Storybook 侧边栏的分组路径，支持嵌套（如 `'Form/Input/Default'`）
- **`component`**：关联真实组件后，Storybook 能自动推断 PropTypes 并生成 Controls 面板
- **`argTypes`**：描述每个 prop 的控制方式（`control: 'select'`、`control: 'boolean'`、`control: 'text'` 等），Storybook 会据此渲染对应的 Controls UI
- **`args`**：每个故事的默认 prop 值，通过 Controls 修改会实时反映在预览中

---

> 写完组件，文档就交给 Storybook 了。但当你面对的是一个"巨无霸"应用时，Storybook 也救不了你——这时候该登场的就是**微前端**了。

## 36.4 微前端

### 36.4.1 微前端的核心理念

微前端将大型应用拆分成多个独立的小应用，各自独立开发、部署。相当于把"微服务"的概念搬到了前端——每个子应用可以由不同团队负责、使用不同技术栈（React/Vue/Angular 混搭），最后组合成一个完整产品。

> 想象一下：美团外卖这种超级 App，背后可能有"商家端"、"骑手端"、"用户端"三个子应用。微前端让它们可以独立迭代，而用户感知不到任何切换。

### 36.4.2 React 项目中的微前端实践

推荐使用 **qiankun**（阿里开源，基于 single-spa，封装的 API 更友好）或 **single-spa**（更底层，灵活性更高）。

**qiankun 示例：**

```javascript
// 主应用 main/src/index.js
import { registerMicroApps, start } from 'qiankun'

registerMicroApps([
  {
    name: 'react-sub',                        // 子应用名称（唯一标识符，用于日志和调试）
    entry: '//localhost:3001',              // 子应用入口地址（开发环境用 localhost，生产环境需改为真实 URL）
    container: '#micro-container',           // 子应用挂载的 DOM 节点（主应用中的一个 div 的 id）
    activeRule: '/react'                      // 激活规则：当浏览器路径以 /react 开头时，加载并渲染该子应用
  },
  {
    name: 'vue-sub',
    entry: '//localhost:3002',
    container: '#micro-container',
    activeRule: '/vue'
  }
])

start()  // 启动 qiankun，开始监听路由变化并按需加载子应用
```

```jsx
// 主应用 App.jsx
function App() {
  return (
    <div>
      <nav>
        <Link to="/react">React 子应用</Link>
        <Link to="/vue">Vue 子应用</Link>
      </nav>
      {/* 子应用将挂载到这里 */}
      <div id="micro-container" />
    </div>
  )
}
```

> 💡 微前端虽好，但不是所有项目都需要。如果你的项目团队小于 5 人、代码库小于 10 万行，上微前端就是过度设计——先问问自己：真的需要这么复杂吗？

---

## 本章小结

本章我们学习了 React 工程化与架构：

- **目录结构**：feature-based 结构，按业务模块组织
- **代码质量**：ESLint + Prettier、Conventional Commits、husky + lint-staged
- **Storybook**：组件文档和可视化测试
- **微前端**：大型应用的拆分与组合

下一章我们将学习 **CI/CD 与自动化**！🔄