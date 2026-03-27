+++
title = "第6章  Create Next App相关配置"
weight = 60
date = "2026-03-27T21:12:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第六章 · 相关配置


## 6.1 创建时自动生成的配置文件

当你敲完 `npx create-next-app@latest my-app` 并且选完所有选项之后，屏幕上会哗啦啦涌现出一堆文件。这些文件就像是你的新家刚装修好时送的"家具大礼包"——你可能不知道每件家具是干嘛用的，但你知道它们肯定有用。本节我们就来逐一认识这些配置文件，看看它们到底是何方神圣。

### 6.1.1 package.json（项目依赖与 scripts）

**package.json** 是 Node.js 项目的核心配置文件，相当于项目的"户口本"——上面登记了项目叫什么名字、版本是多少、依赖哪些包、以及可以做哪些操作。你可以把它想象成一个餐厅的菜单：菜单上写着这家餐厅提供哪些菜（scripts），以及做这些菜需要哪些原材料（dependencies）。

当你使用 TypeScript + Tailwind CSS + ESLint + App Router 的组合创建一个 Next.js 项目时，生成的 `package.json` 大致长这样：

```json
{
  "name": "my-app",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "next": "15.1.6"
  },
  "devDependencies": {
    "@types/node": "^20.17.10",
    "@types/react": "^18.3.18",
    "@types/react-dom": "^18.3.5",
    "typescript": "^5.7.3",
    "tailwindcss": "^3.4.17",
    "postcss": "^8.5.1",
    "autoprefixer": "^10.4.20",
    "eslint": "^8",
    "eslint-config-next": "15.1.6"
  }
}
```

下面我们来逐行解释一下这个文件的各个部分：

- **`name`**：项目的名字，这里是 `my-app`。这个名字会在 `package-lock.json`、npm 搜索、以及项目发布时用到。名字要符合 npm 的命名规范——全小写、禁止空格、禁止特殊字符（除了连字符和下划线）。给项目起名字是个技术活，既要体现项目的精髓，又要足够独特让人一眼记住，比如 `nextjs-blog`、`awesome-todo-app` 都是合规的，而 `My App`（有空格）、`😀`（emoji）都是不合规的。

- **`version`**：项目的当前版本号。这里用的是语义化版本（SemVer）格式 `主版本.次版本.补丁版本`。`0.1.0` 意味着这是一个还处于早期开发阶段的项目。当你正式对外发布第一个稳定版本时，通常会升级到 `1.0.0`。关于语义化版本的更多细节，可以去 [semver.org](https://semver.org/) 深入了解，这里就不展开讲了，否则又可以写一章。

- **`private`**：设置为 `true` 表示这个包是私有的，不会被发布到 npm 官方仓库。这很重要——如果没有这一行，而你又手滑执行了 `npm publish`，那么恭喜你，你可能会把一个半成品项目发布到全世界面前，然后收到来自陌生人的"为什么这个项目打不开"的邮件轰炸。

- **`scripts`**：这是一个命令映射表，定义了你可以用 `npm run <command>` 执行的各种快捷命令。这里的 `dev`、`build`、`start`、`lint` 是 Next.js 项目中最常用的四个命令，我们会在 6.3 节详细讲解它们。此处需要注意的是，并不是所有的 scripts 都必须以 `npm run` 开头——如果你执行的是 `npm run dev` 或者 `yarn dev`，效果是一样的，只是包管理器不同而已。另外，如果你定义了一个名字为 `start` 或者 `test` 的脚本，那么可以直接用 `npm start` 或者 `npm test` 来执行（不需要加 `run`），不过为了保险起见，大多数人还是会写 `npm run start`。

- **`dependencies`**：项目运行时必须依赖的包。比如 `react` 和 `react-dom` 是 React 的核心库，`next` 是 Next.js 框架本身。这些包在生产环境也需要存在，因为用户访问你的网站时，浏览器需要下载并执行这些代码。

- **`devDependencies`**：开发阶段才需要的包。比如 TypeScript 类型定义（`@types/react`）、Tailwind CSS、PostCSS、ESLint 等。这些包只在开发者的电脑上起作用——它们帮助我们更好地写代码、检查错误、编译样式，但最终用户访问网站时，浏览器根本不需要这些工具。形象地说，`dependencies` 是你住进新家后每天都要用的家具（床、桌子、椅子），而 `devDependencies` 是装修时用到的工具（电钻、锤子、油漆），装修完成后这些工具就被收进储藏间了。

> **提示**：在团队协作中，当你把项目 clone 下来之后，第一件事应该是运行 `npm install`（或者 `yarn install`、`pnpm install`），这会根据 `package-lock.json` 或 `yarn.lock` 中的精确版本信息安装所有依赖。如果你直接开始写代码然后运行项目，可能会得到"找不到模块"的神秘错误。

### 6.1.2 next.config.ts / next.config.js（Next.js 框架配置）

**next.config.ts**（或者 `next.config.js`，取决于你创建项目时选择的配置）是 Next.js 框架的核心配置文件。这个文件决定了 Next.js 在构建和运行项目时的各种行为——比如是否开启图片优化、配置环境变量、设置重定向规则、配置 Webpack 或者 Turbopack 的一些高级特性等。

你可以把 `next.config.ts` 理解为 Next.js 的"使用说明书"。当你买了一个功能复杂的电器（比如微波炉），说明书上会告诉你怎么调节火力、怎么设置定时、哪些东西不能放进去。类似地，`next.config.ts` 就是 Next.js 这个"电器"的说明书，告诉它哪些事情该怎么做。

一个典型的 `next.config.ts` 长这样：

```typescript
import type { NextConfig } from 'next'

// NextConfig 是 Next.js 提供的一个类型，用于约束配置对象的结构
// 使用 TypeScript 的好处就是：当你写错了配置项的名字，IDE 会立即报错
const nextConfig: NextConfig = {
  // 项目配置内容写在这里
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        port: '',
        pathname: '/images/**',
      },
    ],
  },
}

export default nextConfig
```

几点说明：

- 在 Next.js 15+ 的项目中，默认使用 `.ts` 扩展名，并使用 `export default` 导出配置对象。
- `NextConfig` 类型来自于 `next` 包本身，它提供了类型安全的配置验证。如果你传入了一个不存在的配置项，TypeScript 会在编译时报错，而不是等到运行时才莫名其妙地出问题。
- 配置文件的名字必须是 `next.config.ts` 或 `next.config.js`，不能改成其他名字（比如 `next.config.production.ts` 是无效的），但你可以在不同环境使用不同的配置文件名，具体方式我们在后续章节会提到。

### 6.1.3 tsconfig.json / jsconfig.json（类型配置 + 路径别名）

**tsconfig.json** 是 TypeScript 项目的配置文件，它告诉 TypeScript 编译器如何处理你的代码——比如支持哪些语法特性、是否启用严格类型检查、哪些目录是源代码目录、路径别名怎么解析等等。如果你创建项目时选择了 TypeScript（这是目前的推荐选项），就会生成 `tsconfig.json`；如果选择了 JavaScript，则会生成 `jsconfig.json`。

`tsconfig.json` 的作用类似于一个"翻译官的工作手册"——TypeScript 编译器就像一个严格的翻译官，它需要知道：你说的这门语言支持哪些词汇（target）、你的口音是哪种方言（module）、哪些话可以含糊其辞哪些必须字字落实（strict）、以及听到某些缩写词时应该展开成什么全称（paths）。

一个典型的 `tsconfig.json` 长这样：

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

让我们详细拆解一下这些配置项：

- **`target`**：指定编译输出的 JavaScript 版本。`ES2017` 意味着 TypeScript 会把新语法（如 `async/await`、`class` 等）编译成兼容 ES2017 的代码。版本号越低，兼容的浏览器越多，但可用的新语法就越少。目前主流的做法是使用 `ES2017` 到 `ES2022` 之间的版本。

- **`lib`**：指定要包含的内置 API 类型声明。`dom` 让你可以使用 `document.getElementById` 这样的 DOM API；`dom.iterable` 支持 `NodeList.prototype.forEach` 等迭代器方法；`esnext` 包含了最新的 JavaScript 特性的类型定义。选择合适的 `lib` 可以让你的 IDE 智能提示更准确。

- **`allowJs`**：允许在项目中导入 `.js` 文件。如果你有一段旧的 JavaScript 代码还没有迁移到 TypeScript，可以先保留它，同时逐步迁移新代码。

- **`skipLibCheck`**：跳过对 `node_modules` 中第三方库的类型检查。这可以大大加快类型检查的速度，因为 `node_modules` 中可能有非常多类型定义文件，每个都检查一遍会很慢。

- **`strict`**：开启严格模式，包含多个子检查：`strictNullChecks`（不允许 null/undefined 值，除非显式声明）、`noImplicitAny`（不允许隐式 any 类型）、`strictFunctionTypes`（函数参数类型必须精确匹配）等。开启 `strict` 就像是给自己请了一个特别挑剔的代码审查员，它会帮你揪出各种潜在的 bug，但同时你也会经常被它"骂"得怀疑人生。

- **`noEmit`**：告诉 TypeScript 编译器只做类型检查，不要输出任何文件。Next.js 使用了自己的构建系统（Babel 或者 SWC）来进行代码转译，所以 TypeScript 编译器只需要做类型检查即可，不需要生成 `.js` 输出文件。

- **`esModuleInterop`**：允许使用默认导入语法导入 CommonJS 模块。比如在没有这个选项的情况下，你必须写 `import * as React from 'react'`，有了这个选项就可以写 `import React from 'react'`。

- **`module`** 和 **`moduleResolution`**：`module` 指定模块系统为 `esnext`（现代的 ES Module）；`moduleResolution` 设置为 `bundler` 是 Next.js 推荐的解析策略，它会像打包工具（如 Webpack、Vite）那样解析模块路径，支持 `package.json` 中的 `exports` 字段等特性。

- **`paths`**：路径别名配置。这是非常实用的一个选项！`"@/*": ["./*"]` 意思是：以 `@/` 开头的导入路径都相对于项目根目录解析。比如你可以在代码中写 `import Button from '@/components/Button'`，而不需要写 `import Button from '../../components/Button'`。这样不仅写起来更方便，而且当文件移动位置时，导入路径也不容易出错（因为路径是相对于项目根目录的，而不是相对于当前文件的）。`**/*` 是通配符，匹配任意深度的目录。

- **`include`**：指定哪些文件应该被 TypeScript 编译器处理。`next-env.d.ts` 是 Next.js 自动生成的文件，用于支持 Next.js 的类型特性；`"**/*.ts"` 和 `"**/*.tsx"` 匹配所有 TypeScript 文件；`.next/types/**/*.ts` 是 Next.js App Router 生成的类型文件。

- **`exclude`**：指定哪些文件不应该被 TypeScript 编译器处理。`node_modules` 当然是必须排除的，否则 TypeScript 会试图编译整个 npm 生态圈，那得等到天荒地老。

### 6.1.4 tailwind.config.ts（Tailwind CSS 配置，如有）

**tailwind.config.ts** 是 Tailwind CSS 框架的配置文件（如果你在创建项目时选择了 Tailwind CSS 的话）。这个文件允许你自定义 Tailwind 的主题颜色、字体、断点（breakpoints）、间距系统等等。

Tailwind CSS 的核心理念是"原子化 CSS"——它不为你写好的 HTML 元素编写一长串 CSS 类名，而是提供一系列低层次的工具类（utility classes），让你可以直接在 HTML 标签上组合使用这些类来控制样式。比如 `<div class="bg-blue-500 text-white p-4 rounded-lg">` 就能创建一个蓝色背景、白色文字、内边距为 4 个 Tailwind 单位、圆角的 div 元素。这种方式的好处是你不需要来回切换 HTML 和 CSS 文件，坏处是 HTML 标签可能会变得很长，长到让你怀疑人生。

`tailwind.config.ts` 的内容大致如下：

```typescript
import type { Config } from 'tailwindcss'

// Config 类型来自 tailwindcss 包，用于约束配置对象的结构
const config: Config = {
  content: [
    // 指定哪些文件应该被 Tailwind 扫描，以找出用到的类名
    // './pages/**/*.{js,ts,jsx,tsx,mdx}' 扫描 pages 目录下的所有页面文件
    // './components/**/*.{js,ts,jsx,tsx,mdx}' 扫描 components 目录下的组件文件
    // './app/**/*.{js,ts,jsx,tsx,mdx}' 扫描 app 目录下的文件（App Router 模式）
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    // extend 是用来扩展默认主题配置的，而不是完全覆盖它
    extend: {
      // 自定义颜色：如果默认的 blue-500 不够用，可以在这里添加项目专属的颜色
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          900: '#0c4a6e',
        },
      },
      // 自定义字体：如果默认字体不够优雅，可以在这里配置项目专属字体
      fontFamily: {
        sans: ['var(--font-geist-sans)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-geist-mono)', 'monospace'],
      },
      // 自定义断点：用于响应式设计
      screens: {
        '3xl': '1920px', // 也许你需要为一个巨屏用户提供特殊待遇
      },
    },
  },
  plugins: [
    // 插件系统允许你扩展 Tailwind 的功能
    // 比如 @tailwindcss/forms 插件可以重置表单元素的默认样式
    // require('@tailwindcss/forms'),
  ],
}

export default config
```

几点说明：

- **`content`** 是 Tailwind 3.x+ 版本最重要的配置项之一。Tailwind 需要知道你的源代码在哪里，才能分析出哪些类名被使用了，然后把没被用到的类名从最终生成的 CSS 中剔除（这个过程叫做"摇树"，tree-shaking）。如果你写了一个类名但 Tailwind 没有扫描到，它就不会出现在最终的 CSS 中，视觉效果就是"为什么这个样式不生效"的困惑时刻。

- **`theme.extend`** 用于在默认主题基础上添加自定义内容，而 **`theme`** 则用于完全替换默认主题。如果你直接写 `theme: { colors: { brand: {...} } }`，那么除了 `brand` 之外的所有默认颜色都会消失，这通常不是你想要的结果。

- Tailwind CSS 3.4+ 推荐使用 `import type { Config } from 'tailwindcss'` 的写法来获取类型提示，而不是旧版本的 `const config = require('tailwindcss')`。

### 6.1.5 postcss.config.mjs（PostCSS 配置，如有 Tailwind）

**postcss.config.mjs** 是 PostCSS 的配置文件。PostCSS 是一个用 JavaScript 插件来转换 CSS 的工具，它本身并不做任何事情，关键在于插件。在 Next.js + Tailwind CSS 项目中，PostCSS 主要负责两件事：运行 Tailwind CSS 的处理流程，以及处理 CSS 的浏览器兼容性前缀（通过 Autoprefixer 插件）。

你可以把 PostCSS 想象成一个"CSS 流水线"——CSS 文件从一端进去，经过一系列处理工序（插件），从另一端出来时就变成了优化过的、浏览器友好的版本。而 `postcss.config.mjs` 就是这个流水线的"工艺说明书"，告诉每个工序用什么参数。

一个典型的 `postcss.config.mjs` 长这样：

```javascript
// postcss.config.mjs
// .mjs 扩展名表示这是一个 ES Module 格式的 JavaScript 文件
// 使用 ES Module 语法（import/export）而不是 CommonJS 语法（require/module.exports）

const config = {
  // plugins 是 PostCSS 处理 CSS 时使用的插件列表
  plugins: {
    // tailwindcss 插件：Tailwind CSS 的 PostCSS 集成
    // 这个插件会读取 tailwind.config.ts 中的配置，并处理 @tailwind 指令
    tailwindcss: {},
    // autoprefixer 插件：自动为 CSS 属性添加浏览器前缀
    // 例如：transform: rotate(45deg) 会自动变成：
    // -webkit-transform: rotate(45deg);
    // transform: rotate(45deg);
    // 这确保了你的 CSS 在新旧浏览器中都能正常工作
    autoprefixer: {},
  },
}

export default config
```

几点说明：

- PostCSS 插件的执行顺序是从右到左（或者更准确地说，从数组的最后一个开始往前执行）。所以 `tailwindcss` 会先处理 `@tailwind` 指令和 Tailwind 类名，然后 `autoprefixer` 再对结果进行前缀处理。

- 如果你不使用 Tailwind CSS，而只是想用 PostCSS 做其他事情（比如自动给 CSS 属性加前缀，或者压缩 CSS），`postcss.config.mjs` 仍然会存在，只是插件列表会有所不同。

- `.mjs` 扩展名表示这是一个 ES Module 文件。在 Node.js 环境中，默认情况下 `.js` 文件会被当作 CommonJS 模块来解析，而 `.mjs` 文件始终被当作 ES Module 来解析。使用 `.mjs` 可以避免在某些环境下因为模块类型不匹配而产生的奇怪错误。

### 6.1.6 .eslintrc.json（ESLint 配置，如有）

**ESLint** 是一个静态代码分析工具，它可以在不运行代码的情况下检查你的代码是否存在潜在错误、是否符合编码规范、是否有不良风格。想象一个超级挑剔的语文老师，不仅改你的作文内容，连标点符号和空格都要管。

**.eslintrc.json** 是 ESLint 的配置文件，它定义了 ESLint 要检查哪些规则、以什么级别报错（错误还是警告）、以及使用哪些插件来扩展检查能力。

一个典型的 `.eslintrc.json` 长这样：

```json
{
  "root": true,
  "extends": [
    "next/core-web-vitals",
    "next/typescript"
  ],
  "rules": {
    // 规则配置可以覆盖或补充 extends 中继承的规则
    // 0 = off（关闭），1 = warning（警告），2 = error（错误）
    // "@typescript-eslint/no-unused-vars": "warn",
    // 如果你实在受不了某个规则的唠叨，可以在这里关掉它
    // "@next/next/no-html-link-for-pages": "off"
  }
}
```

让我们详细解释一下：

- **`root: true`**：这个配置是当前目录的根配置，告诉 ESLint 不要继续往上层目录寻找 `.eslintrc.json` 文件。如果没有这一行，ESLint 可能会错误地使用上层目录中的配置（如果有的话），导致意想不到的结果。

- **`extends`**：继承其他 ESLint 配置。`next/core-web-vitals` 是 Next.js 官方提供的配置，它启用了一系列与 Core Web Vitals（网页核心性能指标）相关的最佳实践规则；`next/typescript` 则启用了 TypeScript 相关的规则检查。

- **`rules`**：自定义规则配置。在这里你可以覆盖 `extends` 中继承的规则的严重级别，或者调整规则的具体参数。

> **提示**：在 Next.js 项目中，ESLint 会在你运行 `npm run dev` 和 `npm run build` 时自动执行。如果你不喜欢某些规则（比如强迫你每行代码末尾必须加分号），可以在 `.eslintrc.json` 中关闭它们，但请确保你了解每个规则背后的理由——毕竟 ESLint 的规则大多是为了帮助你写出更健壮、更易维护的代码。

### 6.1.7 .gitignore（Git 忽略配置）

**.gitignore** 是 Git 的忽略配置文件，它告诉 Git 哪些文件或目录不需要被纳入版本控制。这在 Next.js 项目中非常重要——你肯定不希望把 `node_modules` 目录（里面可能有成千上万个文件）提交到仓库里，这样不仅会让仓库体积暴涨，还会让协作变得异常痛苦。

`.gitignore` 的工作原理很简单：每行写一个模式，Git 会根据这些模式来决定忽略哪些文件。支持通配符（`*` 匹配任意字符，`**` 匹配目录分隔符，`?` 匹配单个字符）。

一个典型的 `.gitignore` 长这样：

```
# 依赖目录 - 这个目录通常有几万到几十万个小文件，提交上去简直是灾难
node_modules/

# Next.js 构建产物 - 这些都是根据源代码自动生成的，不需要版本控制
.next/
out/

# 生产环境构建输出
build/
dist/

# 包含依赖版本锁定信息的文件，可以提交，但通常 .next 等不需要
# package-lock.json
# yarn.lock
# pnpm-lock.yaml

# 环境变量文件 - 包含敏感信息（数据库密码、API 密钥等），绝对不能提交
.env
.env.local
.env.*.local

# 开发日志文件
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE 配置（如果你想保持团队 IDE 配置的一致性，也可以不忽略这个）
# .vscode/
# .idea/

# 操作系统生成的垃圾文件
.DS_Store
Thumbs.db

# 测试覆盖率报告
coverage/

# Next.js 特定的类型缓存（自动生成，但很大）
.next/types/

# Turbopack 缓存
.turbo/
```

几点说明：

- `.gitignore` 中以 `#` 开头的行是注释，不会被执行。
- 模式前加 `/` 表示只匹配项目根目录下的该文件或目录，比如 `/node_modules` 只忽略根目录的 `node_modules`，而不忽略 `./src/node_modules`。
- 模式前不加 `/` 表示递归匹配任意位置的文件或目录。
- 以 `/` 结尾的模式表示匹配目录。
- 以 `!` 开头的模式表示反向忽略（即使是匹配到的文件也会被包含进来），这个技巧比较高级，但很有用。

> **警告**：`.env.local` 和 `.env.production` 等文件通常包含数据库密码、第三方 API 密钥等敏感信息，绝对不能提交到 Git 仓库中。即便是团队内部仓库也不行，因为 Git 历史会永久保存这些信息，一旦泄露后果不堪设想。如果你确实需要让团队成员共享某些环境变量的名字（比如变量名而不是值），可以创建一个 `.env.local.example` 文件，把敏感值替换成占位符，然后把这个 example 文件提交到仓库中。

### 6.1.8 .env.local.example（环境变量示例）

在 Next.js 项目中，**环境变量**（Environment Variables）是管理配置的一种方式，它允许你把那些随着部署环境（开发、测试、生产）变化而变化的值（如数据库连接字符串、API 地址、第三方服务密钥等）从代码中抽离出来，放到单独的文件中。

**`.env.local.example`** 是一个示例文件，它展示了项目需要哪些环境变量，但不包含实际的值。当新的团队成员或者在新的机器上搭建项目时，可以复制这个文件为 `.env.local`，然后填入真实的值。

`.env.local.example` 的内容通常长这样：

```bash
# .env.local.example
# 复制这个文件为 .env.local，然后填入真实值
# 不要把 .env.local 提交到 Git 仓库！

# Next.js 公开环境变量 - 这些变量在客户端代码中也可以访问（小心使用！）
# 变量名必须以 NEXT_PUBLIC_ 开头
# NEXT_PUBLIC_API_URL=https://api.example.com

# Next.js 私有环境变量 - 只在服务端可用，不会泄露到客户端
# 数据库连接字符串
# DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# 第三方服务密钥
# STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxx
# STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxx

# OpenAI API 密钥
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

几点说明：

- 在 Next.js 中，环境变量文件有多种后缀，代表不同的加载优先级和作用域：`.env`（所有环境都会加载）、`.env.local`（仅本地开发加载，不会被 Git 提交）、`.env.development`（仅开发环境）、`.env.production`（仅生产环境）、`.env.test`（仅测试环境）。后缀越具体，优先级越高。

- 以 `NEXT_PUBLIC_` 开头的环境变量会被嵌入到客户端 JavaScript bundle 中，所以它们必须是不敏感的信息（比如 API 的公开端点、功能开关等）。而服务端专用的环境变量（不以 `NEXT_PUBLIC_` 开头）只会出现在服务器端代码中，不会泄露给浏览器。

- `.env.local` 文件（注意没有 `.example`）默认会被 `.gitignore` 忽略，不会被提交到 Git 仓库，这是 Next.js 创建项目时自动配置好的。如果你发现 `.env.local` 被提交了，请立即修改 `.gitignore` 并从 Git 历史中清除该文件（这需要使用 `git filter-branch` 或 `git filter-repo`，操作有一定风险，请谨慎）。

> **经验之谈**：很多新手会问"为什么不把所有配置都写在代码里？"答案很简单：因为代码会被复制到多台机器、多人协作、多次部署，而配置值（比如密码）每台机器都不一样。把配置抽离出来，意味着你只需要改一个文件，而不需要改几十个文件。

## 6.2 next.config.ts 常用配置

上一节我们认识了 `next.config.ts` 的基本面貌，这一节我们来深入探讨几个最常用的配置项。这些配置项就像是厨房里的调味料——虽然不起眼，但放对了地方能让你的项目"味道"大增，放错了可能会让你的项目"味道"大变。

### 6.2.1 images.remotePatterns（图片优化：允许外部域名）

Next.js 自带一个强大的图片优化组件 `<Image>`，它可以自动调整图片大小、格式（WebP、AVIF）和质量，还可以实现懒加载和模糊占位图等高级功能。但是，为了安全起见，`next/image` 默认只允许加载同域名下的图片。如果你尝试从外部域名加载图片（比如 `<img src="https://example.com/photo.jpg" />`），Next.js 会毫不客气地拒绝。

**`images.remotePatterns`** 就是用来解决这个问题配置的——它告诉 Next.js："除了我的域名之外，我还信任这些域名，你也可以优化来自这些域名的图片。"

```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    // remotePatterns 允许你指定可信的外部图片域名
    // 不配置这个的话，从外部域名加载图片会报错
    remotePatterns: [
      {
        // protocol: 图片资源使用的协议，通常是 https
        protocol: 'https',
        // hostname: 允许加载图片的域名，支持通配符模式
        // 例如：'*.amazon.com' 可以匹配 'images.amazon.com'、'cdn.amazon.com'
        hostname: 'images.unsplash.com',
        // port: 端口号，空字符串表示默认端口（80 for http, 443 for https）
        // 如果你需要指定非默认端口，比如 https://example.com:8080，可以写 '8080'
        port: '',
        // pathname: 域名下的路径前缀，用于更精确地限定范围
        // '/photos/**' 只允许 /photos/ 路径下的图片，不允许其他路径
        pathname: '/photos/**',
      },
      {
        protocol: 'https',
        hostname: 'avatars.githubusercontent.com',
        port: '',
        pathname: '/u/*', // 允许 /u/<user-id> 路径下的头像图片
      },
      {
        // 如果你需要允许所有子域名的图片，可以使用通配符模式
        protocol: 'https',
        hostname: '*.pexels.com',
        port: '',
        pathname: '/**',
      },
    ],
    // 除了 remotePatterns 之外，还有一些其他常用图片配置：
    // formats: 指定优化的图片格式，默认是 ['image/avif', 'image/webp']
    // 如果你需要兼容更老的浏览器，可以只使用 webp：
    // formats: ['image/webp'],
    // deviceSizes: 定义响应式图片的断点宽度，单位是像素
    // 配合 <Image> 组件的 sizes 属性使用，Next.js 会自动选择最合适的图片尺寸
    // deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048],
    // imageSizes: 定义非响应式图片的尺寸（通常是固定宽度的图片）
    // imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
}

export default nextConfig
```

几点说明：

- **`protocol`**：必须是 `'http'` 或 `'https'` 之一。出于安全考虑，不推荐允许 `http` 协议的图片，因为它们容易受到中间人攻击。

- **`hostname`**：支持通配符模式。`*.example.com` 可以匹配所有子域名，但 `example.com` 只能匹配这个精确域名，不能匹配 `www.example.com` 或 `api.example.com`。

- **`pathname`**：用于限定只允许特定路径下的图片。比如只允许 `example.com/cdn/` 下的图片，而不允许 `example.com/private/` 下的图片。这是一个很好的安全实践——即使 `example.com` 是你可信的域名，也不应该无限制地允许所有图片。

- 还有一个更宽松的配置方式 `images: { unoptimized: true }`，但这会完全禁用 Next.js 的图片优化功能，不推荐在生产环境使用。

### 6.2.2 experimental.turbo（开启 Turbopack 实验特性）

**Turbopack** 是 Next.js 14+ 引入的新一代打包工具，它是用 Rust 编写的，目标是比 Webpack 快 10 倍以上（理想情况下）。`experimental.turbo` 配置项允许你开启一些尚在实验阶段的 Turbopack 特性。

"实验阶段"（experimental）这个词在软件世界里意味着"这个东西很酷，但可能会在你意想不到的时候爆炸"。所以如果你在生产环境使用 experimental 功能，请务必做好心理准备——以及备份。

```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // experimental.turbo 下的配置项可能会随着 Next.js 版本更新而变化或移除
  experimental: {
    turbo: {
      // resolveAlias 允许你为模块路径设置别名，类似 tsconfig.json 中的 paths
      // 但这个是在打包时生效的，比 tsconfig 的 paths 更底层
      resolveAlias: {
        // 把 'underscore' 别名指向 'lodash'，用于某些库的错误导入
        underscore: 'lodash',
      },
      // resolveExtensions 允许你配置模块解析时尝试的扩展名顺序
      // 当你 import 一个没有扩展名的模块时，Turbopack 会按这个列表依次尝试
      resolveExtensions: [
        '.jsx',
        '.js',
        '.ts',
        '.tsx',
        '.mjs',
        '.mts',
      ],
      // memoryLimit 限制 Turbopack 的内存使用上限（单位：字节）
      // 如果你的项目非常大，可能会占用很多内存，设置这个可以防止内存溢出
      // memoryLimit: 4096 * 1024 * 1024, // 4GB
      // rules 允许你为特定类型的文件配置自定义加载器（loader）
      // 类似于 Webpack 的 module.rules
      // rules: [
      //   {
      //     // 匹配所有 .svg 文件
      //     test: /\.svg$/,
      //     use: ['@svgr/webpack'],
      //   },
      // ],
    },
  },
}

export default nextConfig
```

几点说明：

- `experimental` 命名空间下的配置项不是 Next.js 官方稳定 API 的一部分，它们可能会在任何版本中发生变化，甚至被移除。使用这些配置时请务必确认你的 `package.json` 中 Next.js 的版本号。

- `experimental.turbo` 下的很多功能实际上可以通过 `turbo.json`（Turbo 构建系统的配置文件）来配置，尤其是当你使用 Turbo 生态圈中的其他工具（如 Turborepo）时。

- 想要完全开启 Turbopack，只需要运行 `npm run dev -- --turbo`，不需要在 `next.config.ts` 中添加任何配置。我们会在 6.3.5 节详细讲解。

### 6.2.3 常用配置项一览

除了前面两节介绍的内容之外，`next.config.ts` 还有许多其他常用的配置项。下面我们用一个综合示例来展示一些常见的配置场景：

```typescript
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // ============================================
  // 📦 构建与编译配置
  // ============================================
  // output: 'export' 会把 Next.js 项目构建为一个静态站点（Static Site Generation）
  // 适用于不需要服务端功能的简单网站，如博客、文档站点
  // 注意：开启这个选项后，API Routes 和 ISR 等服务端功能将不可用
  // output: 'export',

  // reactStrictMode 开启 React 的严格模式
  // 在开发环境下，React 会双重调用某些函数来帮助你发现副作用问题
  // 开启后，如果你的代码有副作用（side effects）问题，会在控制台看到警告
  reactStrictMode: true,

  // swcMinify 决定是否使用 SWC（Speedy Web Compiler）来压缩代码
  // SWC 是用 Rust 编写的，比传统的 Terser 压缩速度快得多
  // 默认值是 true，通常不需要修改
  // swcMinify: true,

  // ============================================
  // 🖼️ 图片配置
  // ============================================
  images: {
    // 详见 6.2.1 节
    // 这里再补充一些常见配置
    // formats: 指定优化的目标格式，AVIF 比 WebP 更先进但支持度稍低
    formats: ['image/avif', 'image/webp'],
    // deviceSizes 和 imageSizes 定义响应式图片的尺寸断点
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },

  // ============================================
  // 🔒 安全与头部配置
  // ============================================
  // async headers() 函数允许你配置 HTTP 头部，用于安全、缓存、CORS 等场景
  async headers() {
    return [
      {
        // 匹配所有路由
        source: '/(.*)',
        headers: [
          {
            // X-Frame-Options 防止页面被嵌入到 iframe 中
            // 可以防止点击劫持（clickjacking）攻击
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            // X-Content-Type-Options 防止浏览器 MIME 类型嗅探
            // 如果服务器声明文件是 "text/html" 但实际是 JavaScript，
            // 浏览器不会执行它（这叫 MIME 混淆攻击）
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            // Strict-Transport-Security 强制使用 HTTPS 连接
            // max-age 是浏览器缓存这个规则的时间（单位：秒）
            // includeSubDomains 表示这个规则也适用于所有子域名
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload',
          },
          {
            // Content-Security-Policy 控制页面可以加载哪些资源
            // 这是一个强大的安全机制，但配置不当可能导致页面无法正常加载
            // default-src 'self' 表示默认只允许同源资源
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
          },
        ],
      },
    ]
  },

  // ============================================
  // 🔄 重定向与重写配置
  // ============================================
  async redirects() {
    return [
      // 重定向示例：从 /old-blog/:slug 永久重定向到 /blog/:slug
      // {
      //   source: '/old-blog/:slug',
      //   destination: '/blog/:slug',
      //   permanent: true, // 301 永久重定向，浏览器会缓存
      // },
      // 临时重定向示例：
      // {
      //   source: '/temporary',
      //   destination: '/new-path',
      //   permanent: false, // 302 临时重定向，浏览器不缓存
      // },
    ]
  },

  async rewrites() {
    return [
      // 重写示例：把对 /api-docs 的请求代理到外部 API 文档
      // 用户访问 /api-docs，但实际内容来自外部 URL
      // {
      //   source: '/api-docs',
      //   destination: 'https://docs.example.com/api',
      // },
      // 带参数的重写示例：
      // {
      //   source: '/users/:id',
      //   destination: 'https://api.example.com/users/:id',
      // },
    ]
  },

  // ============================================
  // 📁 目录配置
  // ============================================
  // distDir 自定义构建输出目录，默认是 .next
  // 如果你想把构建产物放到别的目录，可以修改这个选项
  // distDir: 'build',

  // ============================================
  // ⚠️ 实验性功能
  // ============================================
  experimental: {
    // 详见 6.2.2 节
    // 推荐先不加这些配置，等稳定了再加
    // optimizeCss: true, // 开启 CSS 优化（需要安装 critters）
    // serverActions: { allowedOrigins: ['example.com'] }, // 服务端 Action 配置
  },
}

export default nextConfig
```

> **提示**：配置项非常多，不可能全部记住。最好的做法是通读一遍这些配置的文档（[Next.js 官方配置文档](https://nextjs.org/docs/app/api-reference/next-config-js)），了解每个配置的作用，然后在实际遇到需求时再查阅具体用法。"不知道有什么配置"和"知道有这个配置但不知道具体用法"是两回事，前者是视野问题，后者是记忆问题。

## 6.3 package.json scripts

上一章我们认识了 `package.json` 的结构，其中 `scripts` 部分定义了你可以用 `npm run` 执行的命令。在 Next.js 项目中，这部分通常包含五个核心命令：`dev`、`build`、`start`、`lint`，以及一个可选的 `dev -- --turbo`。下面我们就来逐一深入了解这些命令——它们是 Next.js 开发者的日常，是每天要敲几十遍的魔法咒语。

### 6.3.1 npm run dev（开发服务器）

`npm run dev` 是启动 Next.js 开发服务器的 命令。当你执行这个命令时，Next.js 会在本地启动一个 Web 服务器，默认监听 `http://localhost:3000`。这个服务器有以下特点：

- **热模块替换（Hot Module Replacement，HMR）**：当你修改代码并保存时，浏览器会自动刷新（或者在不刷新页面的情况下替换变化的模块），速度极快。这是因为 Next.js 使用了 Webpack（或者 Turbopack，详见 6.4.1 节）的热更新功能，它只需要重新编译变化的部分，而不需要重新编译整个项目。

- **错误友好**：如果你的代码有语法错误或者运行时错误，Next.js 会在浏览器页面和终端中显示详细的错误信息，包括错误发生在哪个文件、哪一行、可能的原因是什么。有些错误信息甚至会给出修复建议，比某些"态度恶劣"的编译器不知道高到哪里去了。

- **类型检查（部分）**：Next.js 会使用 `next/link` 和 `next/image` 等组件时会显示类型错误。但请注意，这并不等于完整的 TypeScript 类型检查——如果你想要完整的类型检查，还是需要单独运行 `tsc` 或者使用 IDE 的类型检查功能。

```bash
# 启动开发服务器
npm run dev

# 如果 3000 端口被占用了，Next.js 会尝试使用 3001、3002 等端口
# 但你也可以手动指定端口：
npm run dev -- --port 4000

# 其他有用的 flags：
# --turbo 开启 Turbopack 加速（详见 6.3.5 节）
# --hostname 指定监听的 host，比如你想在局域网内用手机访问：
# npm run dev -- --hostname 192.168.1.100
```

执行 `npm run dev` 后，终端会显示类似这样的输出：

```
  ▲ Next.js 15.1.6

  - Local:        http://localhost:3000
  - Ready

  ✓ Ready in 2.3s
```

当你访问 `http://localhost:3000` 时，就能看到你的 Next.js 应用了。如果还没创建页面，会显示 Next.js 的默认欢迎页面。

### 6.3.2 npm run build（生产构建）

`npm run build` 是将 Next.js 应用打包成生产环境可部署状态的命令。这个过程会做很多事：编译 TypeScript/React 代码、优化图片、压缩资源、生成静态文件（如果使用了 SSG）、创建服务端 bundle 等。

执行 `npm run build` 后，终端会分阶段显示构建进度：

```
$ npm run build

  ▲ Next.js 15.1.6

  ✓ Collecting page data           # 收集页面数据（SSR、ISR 等）
  ✓ Generating static pages (65)    # 生成静态页面
  ○ Compiling /dashboard ...       # 编译动态页面
  ✓ Compiled /dashboard            # 动态页面编译完成
  ✓ Build failed                   # 哦不，构建失败了！
  ✗ Error: Cannot find module './utils/api'  # 错误原因

  Import trace for requested module:

   ./app/page.tsx
   └── ./utils/api.ts

  ✗ 2 modules with errors

  × Build failed because of compile errors

  > full build output in /path/to/my-app/.next/analyze/...
```

如果没有错误，最终会显示构建成功的信息：

```
  ✓ Compiled successfully

  Route (app)                    Size     First Load JS
  ┌ ○ /                      3.38 kB        91.2 kB
  ├ ○ /about                 2.54 kB        88.4 kB
  ├ ○ /blog                  3.12 kB        90.1 kB
  └ ○ /blog/[slug]           3.45 kB        93.2 kB

  Route (pages)                 Size     First Load JS
  └ ○ /dashboard              5.67 kB       112.5 kB

  ○  (Static)          ●  (SSG)     ●  (Dynamic)
  ✓  (ISR)             □  (Server)

  The route /dashboard is using an unstableAvoidFirebaseHostingFlag
  which is deprecated. Read more at https://nextjs.org/docs/messages/
  unstable-unavoidable-hosting-header

  ✓ Build completed successfully in 12.3s
```

关于输出信息的解读：

- **`○`（空心圆）**：静态页面（Static），在构建时就已经渲染好了，直接从 CDN 读取，速度最快。
- **`●`（实心圆）**：增量静态再生（ISR），页面是静态的，但可以定时重新验证更新。
- **`○`（空心圆 Dynamic）**：动态页面（Dynamic），每次请求时服务器实时渲染。
- **`□`（方框）**：纯服务端渲染（Server），不涉及客户端 hydration。

`build` 命令通常在以下场景使用：

1. **部署前**：在你把代码部署到 Vercel、AWS、阿里云等平台之前，需要先构建好生产版本的产物。
2. **CI/CD 流水线**：持续集成/持续部署系统会运行 `npm run build` 来验证代码能否成功构建。
3. **本地预览生产效果**：如果你想看看代码在生产环境下的实际效果（不包括缓存和 CDN 分发），可以在本地运行 `npm run build && npm run start`。

### 6.3.3 npm run start（生产服务）

`npm run start` 是启动 Next.js 生产服务器的 命令——注意，这里的"生产"不是说它会帮你把代码部署到服务器上，而是说它会启动一个模拟生产环境的服务器，用来预览 `npm run build` 生成的产物。

`npm run start` 有一个重要特点：**它必须在 `npm run build` 之后执行**。如果你直接运行 `npm run start` 而没有先构建，Next.js 会报错并拒绝启动：

```
  ▲ Next.js 15.1.6

  ✗ No build cache found. Please run 'next build' before 'next start'.
```

```bash
# 启动生产服务器（前提是已经执行过 npm run build）
npm run start

# 指定端口（如果你不想用默认的 3000）
npm run start -- --port 4000

# 指定 host（用于局域网访问）
npm run start -- --hostname 0.0.0.0
```

执行 `npm run start` 后，终端显示类似：

```
  ▲ Next.js 15.1.6

  - Local:        http://localhost:3000
  --ready

  ✓ Ready in 1.2s
```

> **提示**：`npm run start` 启动的服务器不使用 HMR，每次修改代码后都需要重新构建。所以它只适合用来预览最终效果，不适合用来开发。如果你在开发阶段误用了 `npm run start`，然后抱怨"为什么改代码不生效"，那就是用错工具了。

### 6.3.4 npm run lint（代码检查）

`npm run lint` 是运行 ESLint 检查代码质量的命令。这个命令会扫描 `src`、`app`、`pages`、`components`、`lib`、`hooks` 等目录下的文件，检查是否存在代码风格问题、潜在 bug、不安全的模式等。

```bash
# 运行 ESLint 检查
npm run lint

# 如果你想自动修复一些可以自动修复的问题（比如空格、缩进、末尾分号等）
npm run lint -- --fix

# 指定要检查的目录或文件
npm run lint -- --fix --ext .ts,.tsx app pages components
```

ESLint 输出示例（没有问题时）：

```
$ npm run lint

  ✓ No ESLint warnings or errors
```

ESLint 输出示例（有问题时）：

```
$ npm run lint

  ✘ http://eslint.org/docs/rules/no-unused-vars

  'count' is defined but never used.

    5 │ export function add(a: number, b: number) {
    6 │   const sum = a + b
  > 7 │   const count = sum > 10 ? 1 : 0
      │         ^^^^^
    8 │   return sum
    9 │ }

  ./app/page.tsx
    12:10  warning  Image elements must have an alt prop  jsx-a11y/alt-text
    28:5   error    Expected indentation of 8 spaces      react/jsx-indent

  ✗ 2 problems (1 error, 1 warning)

  ○ Tip: If you're unsure what to do, check out the ESLint documentation:
    https://nextjs.org/docs/app/building-your-application/configuring/eslint
```

ESLint 的错误级别：

- **Error（错误）**：会导致 `npm run lint` 以非零退出码退出，在 CI/CD 流水线中会触发构建失败。
- **Warning（警告）**：不会导致构建失败，但 ESLint 会提示你注意这些问题。警告多了也不是好事，因为它会让真正重要的警告被淹没在噪音里。

> **经验之谈**：ESLint 是代码质量的守门员，但它不是银弹。有些团队会把 ESLint 规则设置得非常严格，导致每次提交前都要花费大量时间修复 lint 错误，结果开发者开始把 lint 警告视为噪音——这是一个典型的"狼来了"效应。建议：把真正重要的规则设为 error，把一些风格相关的规则设为 off 或 warning，保持一个合理的平衡。

### 6.3.5 npm run dev -- --turbo（Turbopack 加速构建）

`npm run dev -- --turbo` 是在开发模式下使用 **Turbopack**（下一代打包工具）来启动开发服务器的命令。`--turbo` 是一个命令行参数，它告诉 Next.js 的开发服务器使用 Turbopack 而不是默认的 Webpack 来进行代码打包和热更新。

```bash
# 使用 Turbopack 启动开发服务器
npm run dev -- --turbo

# 同样可以指定端口和 host
npm run dev -- --turbo --port 4000 --hostname 0.0.0.0
```

执行后的终端输出与普通 `dev` 类似，但会有 Turbopack 的标识：

```
  ▲ Next.js 15.1.6 (Turbopack)

  - Local:        http://localhost:3000
  -ready

  ✓ Ready in 1.8s
```

Turbopack 的优势在于速度——根据 Vercel 官方的测试数据，Turbopack 的冷启动速度比 Webpack 快约 10 倍，热更新速度也显著更快。对于大型项目来说，这能节省大量的等待时间。

但 Turbopack 也有一些局限性：

- 它目前还在快速迭代中，某些 Webpack 插件和配置可能不完全兼容。
- 生产构建仍然使用 Webpack（或 SWC），`--turbo` 只影响开发服务器。
- 如果遇到奇怪的构建问题，可以尝试去掉 `--turbo` 看看是否是 Turbopack 的问题。

> **幽默一刻**：Turbopack 的速度快到让你怀疑人生——当你还在 Webpack 的"构建中..."转圈圈时，使用 Turbopack 的你已经喝完了一杯咖啡并且改完了三个 bug。这就是科技的力量，或者说，这就是 Rust 的力量（Turbopack 是用 Rust 写的）。

## 6.4 相关工具链

如果说 Next.js 是一个超级英雄，那么它的工具链就是围绕在英雄身边的盟友、小跟班、以及偶尔出现的反派——每个工具都有它的用途，有些让你事半功倍，有些则会让你陷入"这破玩意儿怎么又报错了"的绝望深渊。本节我们就来认识这些工具链，看看它们各自负责什么，以及如何正确地与它们相处。

### 6.4.1 Turbopack（新一代打包工具，Next.js 14+ 支持）

**Turbopack** 是 Vercel 团队开发的下一代打包工具，用 Rust 语言编写，目标是极致的速度和开发体验。它是 Webpack 的继任者，但并不是完全重写——你可以把它理解为Webpack 的"精神继承者"，它借鉴了 Webpack 的核心概念（入口、输出、loader、chunk），但用更高效的底层实现来重写了这些功能。

Turbopack 的核心特性：

- **Rust 实现**：Rust 以其内存安全性和高性能著称。用 Rust 编写打包工具意味着 CPU 密集型的构建任务能被高效处理，而且不存在 JavaScript 的运行时开销。

- **增量编译**：Turbopack 只会重新编译发生变化的文件及其依赖图，而不是每次都全量编译。这听起来很美好，但实际效果取决于项目结构——如果你改了一个被几百个文件导入的工具函数，Turbopack 还是需要重新编译所有依赖方。

- **自适应 chunk 分割**：Turbopack 会根据代码的使用情况自动决定如何分割 chunk，生成最优的代码分割策略。

```mermaid
flowchart LR
    A["源代码<br/>(TS/JS/React)"] --> B{"Turbopack<br/>Rust Powered"}
    B --> C["优化后的<br/>JavaScript Bundle"]
    A1["静态资源<br/>(图片/CSS)"] --> B
    B --> C1["优化后的<br/>静态资源"]
    
    style B fill:#f9f,stroke:#333,stroke-width:2px
```

> **历史趣闻**：Turbopack 的前身是 Webpack 5 中引入的 SWC（Speedy Web Compiler），SWC 是一个用 Rust 写的 JavaScript/TypeScript 编译器，比 Babel 快得多。Next.js 从 12 版本开始就用 SWC 替代了 Babel。而 Turbopack 则更进一步，不仅替换了编译器，还替换了整个打包系统。所以 Turbopack 可以说是 SWC 的"终极进化形态"。

### 6.4.2 Vercel（Next.js 官方部署平台）

**Vercel** 是 Next.js 的创造者（Vercel 公司）提供的云平台，也是 Next.js 官方推荐的部署目标。使用 Vercel 部署 Next.js 应用非常简单——你只需要把代码推送到 GitHub/GitLab/Bitbucket 仓库，然后在 Vercel 上导入项目，点一下"Deploy"，几十秒后你的网站就上线了。

Vercel 的特点：

- **零配置部署**：对于 Next.js 项目，Vercel 不需要任何额外配置就能自动识别并正确部署。它会智能地处理 SSR、SSG、ISR 等各种渲染模式。

- **边缘网络（Edge Network）**：Vercel 在全球部署了大量边缘服务器，用户访问时会自动连接到最近的服务器，实现极低的延迟。

- **预览部署（Preview Deployments）**：每次你在分支上推送代码，Vercel 都会自动生成一个唯一的预览 URL，方便你在正式上线前让设计师、产品经理等非技术人员验收。

- **持续集成/持续部署（CI/CD）**：Git push 即可触发构建和部署流程，不需要手动操作。

```mermaid
flowchart LR
    A["git push"] --> B["GitHub/GitLab"]
    B --> C["Vercel 构建服务器"]
    C --> D{"构建成功？"}
    D -->|是| E["部署到边缘网络"]
    D -->|否| F["显示错误日志"]
    E --> G["用户访问你的网站<br/>全球 CDN 加速"]
    
    style C fill:#ff9900,stroke:#333,stroke-width:2px
    style E fill:#00c853,stroke:#333,stroke-width:2px
    style G fill:#2979ff,stroke:#333,stroke-width:2px
```

Vercel 的商业模式：

- ** Hobby 计划（免费）**：每月 100GB 带宽，足够个人项目和小网站使用。
- ** Pro 计划（$20/月起）**：无限带宽，适合专业网站和小型商业项目。
- ** Enterprise 计划（价格面议）**：适合大型企业，有 SLA 保障和专属支持。

> **温馨提示**：Vercel 的免费计划有一个限制——如果你的网站一个月内没有任何访问，Vercel 会将其"休眠"（Sleep），下次访问时需要等待几十秒重新唤醒。这对于不活跃的个人项目来说问题不大，但对于商业网站来说可能不太友好。

### 6.4.3 @next/codemod（官方代码迁移工具，用于大版本升级）

**@next/codemod** 是 Next.js 官方提供的代码转换工具，用于在大版本升级时自动迁移代码。codemod（code modification）是一种自动化代码重构的技术，它使用 JavaScript/TypeScript 来分析和修改源代码。

为什么需要 codemod？因为 Next.js 每次大版本升级都会带来一些破坏性变更（breaking changes），比如：

- App Router 发布时，Pages Router 的很多 API 发生了变化
- 从 `next/image` 的 `loader` 切换到新的配置方式
- 从 `getServerSideProps`/`getStaticProps` 迁移到新的数据获取方式

手动修改这些代码是痛苦的——如果你的项目有几百个文件，每个文件都要改一遍，那简直是噩梦。codemod 就是来解决这个问题的，它能自动识别旧代码模式并替换成新代码。

```bash
# 安装 @next/codemod
npm install -D @next/codemod

# 查看可用的 codemod 列表
npx @next/codemod --help

# 运行一个具体的 codemod
# 下面的例子是把 Next.js 13 的 image 组件配置迁移到新版本
npx @next/codemod next-image-to-legacy-image ./path/to/your/project
```

常见的 @next/codemod 迁移脚本：

- **`name-default-component`**：将 `name` 属性从图片组件迁移到其他组件（比如 `<Image name="icon" />` 变成 `<Image name="icon" />`，这个改动实际上是因为 React 19 的变化）。
- **`new-link`**：将 `<a>` 标签包裹的 `<Link>` 简化为直接使用 `<Link>` 组件（App Router 中的改进）。
- **`add-missing-react-import`**：为缺少 `import React from 'react'` 的文件自动添加这个导入。
- **`url-to-withrouter`**：将已弃用的 `router.events` 用法迁移到新的 API。

```bash
# 示例：运行 url-to-withrouter codemod
npx @next/codemod url-to-withrouter ./app

# 示例：运行 add-missing-react-import codemod
npx @next/codemod add-missing-react-import ./app
```

> **重要提示**：在运行任何 codemod 之前，请务必确保你的代码已经提交到 Git！因为 codemod 会直接修改源代码，如果出了差错，你可以用 `git checkout -- .` 来恢复。另外，建议分步骤运行 codemod——先运行一个，检查结果，没问题再运行下一个。

### 6.4.4 create-next-app 源码（github.com/vercel/next.js/tree/main/packages/create-next-app）

如果你想深入了解 `create-next-app` 到底做了什么，或者你想为它贡献代码，那么阅读其源码是最好的方式。`create-next-app` 的源码托管在 GitHub 上的 Next.js 仓库中。

仓库地址：[github.com/vercel/next.js/tree/main/packages/create-next-app](https://github.com/vercel/next.js/tree/main/packages/create-next-app)

源码结构大致如下：

```
packages/create-next-app/
├── index.ts                  # 主入口文件，解析命令行参数
├── create-next-app.ts        # 核心创建逻辑
├── templates/                # 项目模板目录
│   ├── app-default/         # App Router + 默认设置模板
│   ├── app-twc/             # App Router + Tailwind CSS + tRPC 模板
│   ├── app-tailwind-ts/     # App Router + Tailwind CSS + TypeScript 模板
│   ├── pages-default/       # Pages Router + 默认设置模板
│   └── ...
├── helpers/                  # 辅助函数
│   ├── getNpmCommand.ts     # 检测当前环境的包管理器
│   ├── writePackageJson.ts  # 生成 package.json
│   ├── install.ts           # 安装依赖的逻辑
│   └── ...
└── __tests__/               # 测试文件
```

阅读源码的意义：

- **理解框架内部**：当你遇到一个奇怪的创建行为时，源码能帮你找到答案。比如"为什么我选 TypeScript 的时候，它默认的 target 是 ES2017？"——答案就在 `create-next-app` 的模板配置里。

- **自定义创建流程**：如果你需要在团队内部创建一个定制版的 `create-next-app`（比如预装团队专属的组件库、ESLint 规则等），阅读源码能帮你理解如何修改和扩展。

- **贡献开源**：也许你会发现一个 bug，或者想到一个很酷的功能改进，那你就可以给 Next.js 仓库提 PR 了。

### 6.4.5 Next.js CLI（npx next：开发服务器、构建、生产启动等运行时命令）

**Next.js CLI** 是 Next.js 提供的命令行工具集。除了通过 `package.json` 中的 `scripts` 来调用 `next` 命令之外，你还可以直接使用 `npx next` 来执行一些高级操作。

```bash
# 使用 npx next 启动开发服务器
npx next dev

# 使用 npx next 构建生产版本
npx next build

# 使用 npx next 启动生产服务器
npx next start

# 使用 npx next 运行 lint 检查
npx next lint

# 查看所有可用命令和帮助信息
npx next --help
```

`npx next --help` 的输出示例：

```
Usage
  $ next <command>

Available commands
  build       Create a production build
  dev         Start the development server
  start       Start the production server
  lint        Run ESLint on the given directories
  telemetry   Enable or disable Next.js telemetry
  info        Print relevant system info useful for debugging
  export      Exports pages to static HTML (Pages Router only)
  server      Starts the Next.js production server with the built-in runtime

Options
  --turbo     Enable Turbopack dev server (beta)
  --port      Specify a port number
  --hostname  Specify a hostname
  --help      Show this help message
```

`npx next info` 命令非常有用——当你遇到问题需要向他人求助时，运行这个命令会打印出你的环境信息（操作系统、Node.js 版本、npm 版本、Next.js 版本等），方便排查问题：

```bash
npx next info

# 输出示例：
# Operating System:
#   Platform: win32
#   Arch: x64
#   Version: Windows 10 Pro
#   Platform: 10.0.19045
# Runtime:
#   Node.js: 22.14.0
#   npm: 10.9.2
#   Yarn: 1.22.22
#   pnpm: 9.15.0
# Binaries:
#   Node: 22.14.0
#   npm: 10.9.2
#   Yarn: 1.22.22
#   pnpm: 9.15.0
# Relevant packages:
#   next: 15.1.6 (site: https://nextjs.org)
#   react: 18.3.1
#   react-dom: 18.3.1
```

### 6.4.6 create-next-app 与 npx next 的区别（前者负责初始化项目，后者负责运行项目）

很多初学者容易混淆 `create-next-app` 和 `npx next` 这两个命令——它们都包含 `next`，都跟 Next.js 相关，但职责完全不同。让我用一个生活化的比喻来解释：

- **`create-next-app`** 就像是一个"新房装修队"。当你决定要住进 Next.js 这个"小区"时，你需要调用装修队来帮你把房子从毛坯状态装修好——它会帮你安装好基础家具（React、Next.js 核心包）、配置好各种管道电线（TypeScript、ESLint、Prettier）、铺好地板和墙漆（Tailwind CSS）、甚至帮你买好一些装饰品（示例页面）。装修完成后，装修队就走了。

- **`npx next`** 就像是一个"物业管理系统"。当你住进去之后，遇到的所有问题都要找物业——水管漏了找物业（开发服务器），电梯坏了找物业（生产构建），要交物业费了找物业（生产服务启动）。物业管理系统是在你入住之后才需要用到的。

```mermaid
flowchart TD
    A["create-next-app<br/>初始化阶段"] --> B["生成项目文件"]
    A --> C["安装依赖"]
    A --> D["配置工具链"]
    B --> E["项目已就绪"]
    C --> E
    D --> E
    
    F["npx next<br/>运行阶段"] --> G["开发服务器<br/>npm run dev"]
    F --> H["生产构建<br/>npm run build"]
    F --> I["生产服务<br/>npm run start"]
    
    E --> F
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#9f9,stroke:#333,stroke-width:2px
```

具体来说：

```bash
# 第一步：用 create-next-app 创建一个新项目（只需执行一次）
npx create-next-app@latest my-project

# 进入项目目录
cd my-project

# 第二步：在项目目录中，使用 npx next（或者通过 npm scripts）来运行项目
npm run dev
# 或者直接用 npx next dev，效果是一样的
npx next dev

# 后续的日常开发中，你只会用到 npm run dev/build/start/lint
# create-next-app 不会再被用到，除非你要创建另一个新项目
```

> **一图胜千言**：
> - `create-next-app`：一次性的项目脚手架工具，创建项目时用
> - `npx next`：日常开发工具，每次写代码、构建、部署时都会用到

## 本章小结

本章我们深入探索了 Next.js 项目创建后自动生成的那些配置文件，以及围绕 Next.js 的工具链生态。这些内容虽然不像写页面、调样式那样"看得见摸得着"，但它们构成了整个项目的地基——地基不稳，地动山摇。

**核心要点回顾**：

1. **package.json** 是项目的"户口本"，记录了项目名称、版本、依赖包和可执行命令。其中 `dependencies` 是运行时必须的包，`devDependencies` 是开发时用到的工具。

2. **next.config.ts** 是 Next.js 的"使用说明书"，控制了框架的方方面面——图片优化、重定向、安全头部、实验特性等。

3. **tsconfig.json** 是 TypeScript 编译器的"工作手册"，路径别名（`@/`）功能让你的导入路径更简洁优雅。

4. **Tailwind CSS 相关配置**（tailwind.config.ts、postcss.config.mjs）负责样式系统的定制和 PostCSS 流水线的构建。

5. **ESLint 配置**（.eslintrc.json）是你代码的"挑剔语文老师"，帮你揪出各种潜在问题。

6. **.gitignore** 是 Git 的"门卫"，把不该进版本库的垃圾文件挡在门外。`.env.local` 永远不要提交！

7. **package.json scripts** 中的 `dev`、`build`、`start`、`lint` 是日常开发的四大金刚。其中 `npm run dev` 启动开发服务器，`npm run build` 构建生产版本，`npm run start` 预览生产效果，`npm run lint` 检查代码质量。

8. **Turbopack** 是用 Rust 写的新一代打包工具，`--turbo` 参数可以加速开发服务器，但生产构建目前仍使用 Webpack/SWC。

9. **Vercel** 是 Next.js 的官方部署平台，Git push 即可自动部署，零配置。

10. **@next/codemod** 是大版本升级时的救星，能自动迁移旧代码到新 API，但运行前务必先提交 Git。

11. **create-next-app 负责初始化项目，npx next 负责运行项目**，两者职责不同，不要混淆。

配置文件虽然看起来枯燥，但它们是每个严肃的 Next.js 开发者必须掌握的基本功。当你遇到"为什么图片加载不出来"、"为什么样式不生效"、"为什么构建报错"这类问题时，这些知识就会派上用场。祝你在 Next.js 的世界里玩得开心，少踩坑，多产出！
