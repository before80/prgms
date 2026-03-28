


+++
title = "第17章 编写自定义插件"
weight = 170
date = "2026-03-27T17:13:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter-17-Custom-Plugins

# 第17章：编写自定义插件

> 你已经用过很多插件了——Vue 插件、React 插件、PWA 插件、自动导入插件...
>
> 但你有没有想过：**自己写一个 Vite 插件**？
>
> 其实 Vite 插件并不神秘，它就是一段遵循特定规范的代码。这一章，我们就从零开始，手把手教你写一个自己的 Vite 插件。
>
> 学完这章，你不仅能写出自己的插件，还能深入理解 Vite 插件系统的工作原理，甚至可以把自己的插件发布到 npm！😎

---

## 17.1 插件 API 详解

### 17.1.1 插件的基本结构

**Vite 插件的基本结构**：

```javascript
// my-vite-plugin.js

// 插件函数，接受配置选项，返回插件对象
function myPlugin(options = {}) {
  // 插件的唯一名称
  const name = 'my-plugin'
  
  // 返回插件对象
  return {
    name,  // 必须：插件名称
    
    // 各种钩子函数...
    resolveId() {},
    load() {},
    transform() {},
    transformIndexHtml() {},
    configureServer() {},
    handleHotUpdate() {},
  }
}

export default myPlugin
```

### 17.1.2 插件钩子函数概览

**Vite 插件的生命周期钩子**：

| 钩子 | 执行时机 | 类型 |
|------|----------|------|
| `options` | 插件配置时 | `Sync` |
| `buildStart` | 构建开始时 | `Async` |
| `resolveId` | 解析模块路径时 | `Async` |
| `load` | 加载模块内容时 | `Async` |
| `transform` | 转换代码时 | `Async` |
| `buildEnd` | 构建结束时 | `Async` |
| `generateBundle` | 生成产物前 | `Async` |
| `writeBundle` | 输出文件时 | `Async` |

**开发服务器特有的钩子**：

| 钩子 | 执行时机 |
|------|----------|
| `configureServer` | 配置开发服务器 |
| `configurePreviewServer` | 配置预览服务器 |
| `transformIndexHtml` | 转换 index.html |
| `handleHotUpdate` | 处理热更新 |

### 17.1.3 解析钩子（resolveId）

**resolveId 钩子**：拦截模块解析，决定模块的真正路径。

```javascript
// resolveId 钩子示例
function myPlugin() {
  return {
    name: 'my-resolver',
    
    resolveId(source, importer, options) {
      // source: 模块名称（如 './utils'）
      // importer: 导入该模块的文件路径
      // options: 额外选项
      
      // 自定义模块解析
      if (source === 'my:virtual-module') {
        // 返回模块 ID（通常是一个虚拟路径）
        return '\0virtual-module'  // \0 前缀表示是虚拟模块
      }
      
      // 重写模块路径
      if (source.startsWith('@my-lib/')) {
        // 将 @my-lib/xxx 转换为 src/xxx
        const modulePath = source.replace('@my-lib/', '')
        return path.resolve(__dirname, 'src', modulePath)
      }
      
      // 返回 null 表示不处理，使用默认解析
      return null
    },
  }
}
```

### 17.1.4 加载钩子（load）

**load 钩子**：加载模块内容。

```javascript
// load 钩子示例
function virtualModulePlugin() {
  // 存储虚拟模块的内容
  const virtualModules = {
    '\0virtual:constants': `
      export const VERSION = '1.0.0'
      export const API_URL = 'https://api.example.com'
      export const FEATURES = ['auth', 'analytics', 'billing']
    `,
    '\0virtual:utils': `
      export function formatDate(date) {
        return new Date(date).toLocaleDateString()
      }
      export function debounce(fn, delay) {
        let timer = null
        return function(...args) {
          clearTimeout(timer)
          timer = setTimeout(() => fn.apply(this, args), delay)
        }
      }
    `,
  }
  
  return {
    name: 'virtual-module',
    
    resolveId(id) {
      if (id in virtualModules) {
        return id  // 返回虚拟模块 ID
      }
    },
    
    load(id) {
      if (id in virtualModules) {
        // 返回模块内容
        return virtualModules[id]
      }
    },
  }
}
```

### 17.1.5 转换钩子（transform）

**transform 钩子**：转换模块代码，最常用的钩子。

```javascript
// transform 钩子示例
function logPlugin() {
  return {
    name: 'log-plugin',
    
    transform(code, id) {
      // 跳过 node_modules
      if (id.includes('node_modules')) {
        return null
      }
      
      // 只处理 .js 和 .ts 文件
      if (!id.match(/\.(js|ts)$/)) {
        return null
      }
      
      // 在每个函数前添加日志
      const transformedCode = code.replace(
        /(function\s+\w+|[A-Z]\w*\s*\()/g,
        (match) => {
          console.log(`[Log Plugin] 函数调用: ${match}`)
          return match
        }
      )
      
      // 返回转换后的代码和 sourcemap
      return {
        code: transformedCode,
        map: null,  // 如果需要 sourcemap，使用 this.getSourcemap()
      }
    },
  }
}
```

**更完整的 transform 示例**：

```javascript
// 编译时替换插件
function replacePlugin(replacements = {}) {
  return {
    name: 'replace-plugin',
    
    transform(code, id) {
      let hasReplaced = false
      let result = code
      
      for (const [search, replacement] of Object.entries(replacements)) {
        if (result.includes(search)) {
          result = result.split(search).join(replacement)
          hasReplaced = true
        }
      }
      
      if (hasReplaced) {
        return {
          code: result,
          map: this.getSourcemap ? this.getSourcemap() : null,
        }
      }
      
      return null
    },
  }
}

// 使用
export default defineConfig({
  plugins: [
    replacePlugin({
      __BUILD_TIME__: new Date().toISOString(),
      __VERSION__: process.env.npm_package_version,
    }),
  ],
})
```

### 17.1.6 输出钩子（generateBundle）

**generateBundle 钩子**：在生成最终产物前调用。

```javascript
// generateBundle 钩子示例
function assetPlugin() {
  return {
    name: 'asset-plugin',
    
    generateBundle(options, bundle) {
      // bundle 包含所有要输出的文件
      for (const [fileName, chunk] of Object.entries(bundle)) {
        // 为每个 JS 文件添加注释头
        if (fileName.endsWith('.js')) {
          const content = `
/**
 * @file ${fileName}
 * @build ${new Date().toISOString()}
 */
${chunk.code}
          `
          // 覆盖文件内容
          this.emitFile({
            type: 'asset',
            fileName,
            content,
          })
        }
        
        // 删除特定文件
        if (fileName === 'legacy.js') {
          delete bundle[fileName]
        }
      }
    },
  }
}
```

### 17.1.7 插件选项与配置

**插件配置选项**：

```javascript
// 带配置的插件
function myPlugin(config = {}) {
  // 默认配置
  const defaultConfig = {
    prefix: '__',
    suffix: '__',
    verbose: false,
  }
  
  // 合并配置
  const options = { ...defaultConfig, ...config }
  
  return {
    name: 'my-configured-plugin',
    
    // 使用配置
    transform(code, id) {
      if (options.verbose) {
        console.log(`[my-plugin] Transforming: ${id}`)
      }
      
      const transformed = code
        .split(options.prefix).join('')
        .split(options.suffix).join('')
      
      return { code: transformed }
    },
  }
}

// 使用
export default defineConfig({
  plugins: [
    myPlugin({
      prefix: '{{',
      suffix: '}}',
      verbose: true,
    }),
  ],
})
```

---

## 17.2 虚拟模块

### 17.2.1 什么是虚拟模块

**虚拟模块**是一种"不存在于文件系统"但可以像普通模块一样导入的模块。它的内容是在插件中动态生成的。

**使用场景**：
- 自动生成常量（如版本号、构建时间）
- 生成 TypeScript 类型定义
- 创建编译时配置
- 实现条件导入

### 17.2.2 创建虚拟模块

**创建虚拟模块的完整示例**：

```javascript
// plugins/virtual-env.ts
import { defineConfig } from 'vite'

// 定义虚拟模块内容
const virtualEnvModule = `
export const MODE = '${process.env.NODE_ENV || 'development'}'
export const VERSION = '${process.env.npm_package_version || '1.0.0'}'
export const BUILD_TIME = '${new Date().toISOString()}'
export const API_URL = '${process.env.VITE_API_URL || 'http://localhost:3000'}'
export const DEBUG = ${process.env.NODE_ENV !== 'production'}
`.trim()

// 定义虚拟类型模块
const virtualTypesModule = `
export interface EnvConfig {
  MODE: string
  VERSION: string
  BUILD_TIME: string
  API_URL: string
  DEBUG: boolean
}

declare const envConfig: EnvConfig
export default envConfig
`.trim()

export default defineConfig({
  plugins: [
    {
      name: 'virtual-env',
      
      resolveId(id) {
        if (id === 'virtual:env' || id === 'virtual:types') {
          return '\0' + id  // \0 前缀是虚拟模块的约定
        }
      },
      
      load(id) {
        if (id === '\0virtual:env') {
          return virtualEnvModule
        }
        if (id === '\0virtual:types') {
          return virtualTypesModule
        }
      },
    },
  ],
})
```

**使用虚拟模块**：

```typescript
// src/main.ts

// 导入虚拟模块
import envConfig from 'virtual:env'
import { VERSION, BUILD_TIME, API_URL } from 'virtual:env'

console.log(envConfig.MODE)      // development
console.log(VERSION)             // 1.0.0
console.log(BUILD_TIME)         // 2024-03-27T08:00:00.000Z
console.log(API_URL)           // http://localhost:3000
```

### 17.2.3 应用场景

**场景一：生成构建信息**：

```javascript
// 自动在每次构建时生成版本号
function buildInfoPlugin() {
  const content = `
export const buildInfo = {
  buildTime: '${new Date().toISOString()}',
  gitCommit: '${process.env.GIT_COMMIT || 'unknown'}',
  branch: '${process.env.GIT_BRANCH || 'unknown'}',
  buildNumber: '${process.env.BUILD_NUMBER || '1'}',
}
`.trim()
  
  return {
    name: 'build-info',
    resolveId(id) {
      if (id === 'virtual:build-info') return '\0virtual:build-info'
    },
    load(id) {
      if (id === '\0virtual:build-info') return content
    },
  }
}
```

**场景二：自动导入图标**：

```javascript
// 自动导入 src/icons 目录下的所有 SVG 图标
function autoIconsPlugin() {
  const iconFiles = fs.readdirSync('./src/icons')
    .filter(f => f.endsWith('.svg'))
  
  const content = iconFiles
    .map(f => {
      const name = path.basename(f, '.svg')
      const svg = fs.readFileSync(`./src/icons/${f}`, 'utf-8')
      return `export const ${toCamelCase(name)} = ${JSON.stringify(svg)}`
    })
    .join('\n')
  
  return {
    name: 'auto-icons',
    resolveId(id) {
      if (id === 'virtual:icons') return '\0virtual:icons'
    },
    load(id) {
      if (id === '\0virtual:icons') return content
    },
  }
}
```

---

## 17.3 插件开发实战

### 17.3.1 开发环境注入代码

**自动注入脚本插件**：

```javascript
// 注入 Google Analytics 代码
function injectGAPlugin(gaId) {
  return {
    name: 'inject-ga',
    
    transformIndexHtml(html) {
      return html.replace(
        '</head>',
        `
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${gaId}');
        </script>
        </head>
        `
      )
    },
  }
}

// 使用
export default defineConfig({
  plugins: [
    injectGAPlugin('GA-MEASUREMENT-ID'),
  ],
})
```

### 17.3.2 自定义文件转换

**自动生成 SVG Sprite**：

```javascript
// 自动生成 SVG 雪碧图
function svgSpritePlugin() {
  const spriteDir = path.resolve(__dirname, 'src/icons')
  const outputFile = 'icons.svg'
  
  return {
    name: 'svg-sprite',
    
    resolveId(id) {
      if (id === 'virtual:svg-sprite') {
        return '\0virtual:svg-sprite'
      }
    },
    
    async load(id) {
      if (id === '\0virtual:svg-sprite') {
        const files = fs.readdirSync(spriteDir).filter(f => f.endsWith('.svg'))
        
        let sprite = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n'
        
        for (const file of files) {
          const name = path.basename(file, '.svg')
          const content = fs.readFileSync(path.join(spriteDir, file), 'utf-8')
          
          // 提取 SVG 内容
          const match = content.match(/<svg[^>]*>([\s\S]*?)<\/svg>/)
          if (match) {
            sprite += `  <symbol id="icon-${name}" viewBox="0 0 24 24">\n${match[1].split('\n').map(l => '    ' + l).join('\n')}\n  </symbol>\n`
          }
        }
        
        sprite += '</svg>'
        
        // 生成 JS 模块
        return `
          const sprite = ${JSON.stringify(sprite)}
          export default sprite
          
          // 注入到 DOM
          if (typeof document !== 'undefined') {
            const div = document.createElement('div')
            div.innerHTML = sprite
            div.style.display = 'none'
            document.body.appendChild(div.firstChild)
          }
        `
      }
    },
  }
}
```

### 17.3.3 构建时优化插件

**自动压缩图片插件**：

```javascript
// 构建时压缩图片
import sharp from 'sharp'

function imageOptimizerPlugin(options = {}) {
  const {
    extensions = ['.jpg', '.png', '.webp'],
    quality = 80,
  } = options
  
  const imageExtensions = new Set(extensions)
  
  return {
    name: 'image-optimizer',
    
    // 在 generateBundle 时处理图片
    async generateBundle() {
      // 这个钩子可以访问所有要输出的文件
      console.log('[image-optimizer] 开始优化图片...')
    },
    
    // 或者使用 resolveId 和 load 拦截图片
    load(id) {
      if (!imageExtensions.has(path.extname(id))) {
        return null
      }
      
      // 这里可以返回压缩后的图片
      // 但通常更好的做法是交给其他工具处理
    },
  }
}
```

### 17.3.4 处理 CSS/图片资源

**CSS 变量注入插件**：

```javascript
// 自动注入 CSS 变量
function cssVarsPlugin(vars = {}) {
  const cssVars = Object.entries(vars)
    .map(([key, value]) => `  --${key}: ${value};`)
    .join('\n')
  
  return {
    name: 'css-vars',
    
    transformIndexHtml(html) {
      return html.replace(
        '</head>',
        `
        <style>
          :root {
${cssVars}
          }
        </style>
        </head>
        `
      )
    },
  }
}

// 使用
export default defineConfig({
  plugins: [
    cssVarsPlugin({
      'primary-color': '#409eff',
      'success-color': '#67c23a',
      'warning-color': '#e6a23c',
      'danger-color': '#f56c6c',
      'font-size-base': '14px',
    }),
  ],
})
```

---

## 17.4 插件测试

### 17.4.1 插件单元测试

**Vitest 测试插件**：

```javascript
// plugins/my-plugin.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { inlineImagePlugin } from '../plugins/inline-image'

describe('inlineImagePlugin', () => {
  let plugin
  
  beforeEach(() => {
    plugin = inlineImagePlugin({
      maxSize: 1024,  // 1KB 以下的图片内联
    })
  })
  
  it('应该返回正确的插件名称', () => {
    expect(plugin.name).toBe('inline-image')
  })
  
  it('应该处理图片文件', async () => {
    const result = plugin.transform?.('<img src="./small.png">', 'test.vue')
    
    // 如果图片小于 maxSize，应该返回内联的 base64
    expect(result).toBeDefined()
  })
  
  it('应该跳过大于限制的图片', () => {
    const result = plugin.transform?.('<img src="./large.png">', 'test.vue')
    
    // 大图片不处理，返回 null
    expect(result).toBeNull()
  })
})
```

### 17.4.2 集成测试

**使用 Vite 的测试工具**：

```javascript
// plugins/my-plugin.integration.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { createServer } from 'vite'
import path from 'path'

describe('插件集成测试', () => {
  let server
  
  beforeAll(async () => {
    server = await createServer({
      root: path.resolve(__dirname, 'fixtures/test-project'),
      plugins: [myPlugin()],
    })
    await server.listen()
  })
  
  afterAll(async () => {
    await server.close()
  })
  
  it('应该正确处理模块解析', async () => {
    const { moduleGraph } = server
    
    // 获取模块信息
    const module = await moduleGraph.ensureEntryFromUrl('/src/main.ts')
    expect(module).toBeDefined()
  })
  
  it('transform 应该被正确调用', async () => {
    const { transformRequest } = server
    
    const result = await transformRequest('/src/main.ts')
    expect(result).toBeDefined()
    expect(result.code).toBeDefined()
  })
})
```

---

## 17.5 插件发布

### 17.5.1 插件打包

**使用 tsup 打包**：

```bash
pnpm add -D tsup
```

```javascript
// tsup.config.ts
import { defineConfig } from 'tsup'

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  external: ['vite'],
})
```

```json
// package.json
{
  "name": "vite-plugin-my-plugin",
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  }
}
```

### 17.5.2 发布到 npm

```bash
# 1. 登录 npm
npm login

# 2. 构建
pnpm build

# 3. 发布
npm publish --access public

# 或者发布测试版
npm publish --tag beta
```

### 17.5.3 README 编写

```markdown
# vite-plugin-my-plugin

一个超棒的 Vite 插件 ✨

## 安装

\`\`\`bash
pnpm add -D vite-plugin-my-plugin
\`\`\`

## 使用

\`\`\`javascript
// vite.config.js
import { defineConfig } from 'vite'
import myPlugin from 'vite-plugin-my-plugin'

export default defineConfig({
  plugins: [
    myPlugin({
      // 选项
    }),
  ],
})
\`\`\`

## 选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| option1 | string | - | 选项1 |
| option2 | boolean | false | 选项2 |

## 示例

### 基本用法

\`\`\`js
import myPlugin from 'vite-plugin-my-plugin'

myPlugin()
\`\`\`

## License

MIT
```

---

## 17.6 本章小结

### 🎉 本章总结

这一章我们从零开始学习了如何编写 Vite 插件：

1. **插件 API 详解**：插件的基本结构（name + 钩子函数）、resolveId 钩子（模块解析）、load 钩子（加载模块）、transform 钩子（转换代码）、generateBundle 钩子（生成产物）、插件选项配置

2. **虚拟模块**：虚拟模块的概念、创建虚拟模块（resolveId + load）、应用场景（构建信息、自动导入图标）

3. **插件开发实战**：开发环境注入代码（GA 代码）、自定义文件转换（SVG Sprite）、构建时优化插件（图片压缩）、处理 CSS/图片资源（CSS 变量注入）

4. **插件测试**：插件单元测试、集成测试

5. **插件发布**：插件打包（tsup）、发布到 npm、README 编写规范

### 📝 本章练习

1. **第一个插件**：创建一个简单的插件，在控制台打印所有被加载的模块

2. **虚拟模块**：创建一个虚拟模块，导出当前 git commit 信息

3. **实战插件**：创建一个自动在 HTML 中注入 GA 代码的插件

4. **测试**：为你的插件编写单元测试

5. **发布**：把插件发布到 npm（可以用 scope @your-org）

---

> 📌 **预告**：下一章我们将进入 **Monorepo 与大型项目**，学习 pnpm workspace、Turborepo、Nx 等工具的使用。敬请期待！
