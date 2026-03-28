


+++
title = "第13章 测试与调试"
weight = 130
date = "2026-03-27T17:13:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# Chapter-13-Testing-And-Debugging

# 第13章：测试与调试

> "测试？那是什么？能吃吗？"
>
> 如果你也是这么想的，那这章就是你的"觉醒时刻"。没有测试的代码就像没有安全带的赛车——可能跑得很快，但一出事就是大事。
>
> 这一章我们要聊的话题：Vitest 怎么写单元测试？Playwright 怎么写 E2E 测试？VS Code 怎么调试？Chrome DevTools 怎么用？GitHub Actions 怎么配置 CI？
>
> 准备好了吗？让我们一起告别"改完代码手动刷新浏览器"的时代！🧪

---

## 13.1 单元测试

### 13.1.1 Vitest 简介与安装

**Vitest** 是一个由 Vite 驱动的单元测试框架，由 Vue 官方团队成员 Anthony Fu 创建。它的特点是：
- **极速**：和 Vite 一样快，因为使用了相同的 transform 机制
- **开箱即用**：零配置，和 Vite 项目无缝集成
- **TypeScript 支持**：原生 TypeScript 支持
- **HMR 支持**：测试文件修改后自动重新运行

**Vitest vs Jest vs Mocha**：

| 框架 | 特点 | 与 Vite 集成 |
|------|------|-------------|
| **Vitest** | 极速，Vite 原生，Vue 官方推荐 | ⭐⭐⭐⭐⭐ |
| Jest | 老牌稳定，但较慢 | ⭐⭐ |
| Mocha | 灵活，但配置复杂 | ⭐⭐ |

**安装 Vitest**：

```bash
# Vue 项目
pnpm add -D vitest @vue/test-utils

# React 项目
pnpm add -D vitest @testing-library/react @testing-library/jest-dom

# 如果需要 JSX 支持
pnpm add -D @vitejs/plugin-react

# 如果需要覆盖率报告
pnpm add -D @vitest/coverage-v8
```

### 13.1.2 编写第一个测试

**Vitest 配置**：

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import jsx from '@vitejs/plugin-vue-jsx'

export default defineConfig({
  plugins: [
    vue(),
    jsx(),
  ],
  test: {
    // 全局配置
    globals: true,  // 使用全局 describe/it/expect 等函数（不需要 import）
    environment: 'jsdom',  // 测试环境：jsdom / node / happy-dom
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
    exclude: ['node_modules', 'dist'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
})
```

```typescript
// vitest.config.ts（更完整的配置）
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import jsx from '@vitejs/plugin-vue-jsx'

export default defineConfig({
  plugins: [vue(), jsx()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/tests/setup.ts'],
    include: ['src/**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/tests/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/dist/',
      ],
    },
  },
})
```

**第一个测试**：

```typescript
// src/utils/math.test.ts

// 导入要测试的函数
import { describe, it, expect, test } from 'vitest'
import { add, multiply, divide, factorial } from './math'

// describe：测试套件，把相关的测试组织在一起
describe('数学工具函数', () => {
  // it 或 test：定义一个测试用例
  it('add 函数：两个数相加', () => {
    // expect：断言，验证实际值是否符合预期
    expect(add(1, 2)).toBe(3)
    expect(add(-1, 1)).toBe(0)
    expect(add(0, 0)).toBe(0)
  })

  test('multiply 函数：两个数相乘', () => {
    expect(multiply(3, 4)).toBe(12)
    expect(multiply(-2, 3)).toBe(-6)
    expect(multiply(0, 100)).toBe(0)
  })

  test('divide 函数：两个数相除', () => {
    expect(divide(10, 2)).toBe(5)
    expect(divide(9, 3)).toBe(3)
    expect(divide(5, 2)).toBe(2.5)
  })

  test('divide 函数：除以 0 应该抛出错误', () => {
    // toThrow：断言函数会抛出错误
    expect(() => divide(10, 0)).toThrow('不能除以 0')
  })

  test('factorial 函数：阶乘', () => {
    expect(factorial(0)).toBe(1)
    expect(factorial(1)).toBe(1)
    expect(factorial(5)).toBe(120)
    expect(factorial(10)).toBe(3628800)
  })

  // 异步测试
  test('asyncAdd：异步加法', async () => {
    // 注意：这里的 add 是同步函数
    // 如果要测试异步加法，需要先 resolve Promise
    const result = await add(await Promise.resolve(1), await Promise.resolve(2))
    expect(result).toBe(3)
  })
})
```

**运行测试**：

```bash
# 运行所有测试
pnpm test

# 监听模式（文件修改后自动重新运行）
pnpm test:watch

# 只运行一次
pnpm test:run

# 运行指定文件
pnpm test src/utils/math.test.ts

# 运行指定测试
pnpm test --grep "add 函数"
```

### 13.1.3 测试命令配置

**package.json 脚本配置**：

```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",          // 单次运行（CI 常用）
    "test:watch": "vitest --watch",     // 监听模式
    "test:coverage": "vitest run --coverage",  // 带覆盖率
    "test:ui": "vitest --ui"           // 浏览器 UI
  }
}
```

### 13.1.4 组件测试（Vue Testing Library）

**Vue Testing Library** 专注于测试组件的行为，而不是实现细节。

**安装**：

```bash
pnpm add -D @vue/test-utils vitest
```

**Vue 组件测试**：

```vue
<!-- src/components/Counter.vue -->
<template>
  <div class="counter">
    <h1>计数器：{{ count }}</h1>
    <p>双倍计数：{{ doubleCount }}</p>
    
    <button @click="decrement" :disabled="count <= 0">-</button>
    <button @click="increment">+</button>
    <button @click="reset">重置</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  initialCount: {
    type: Number,
    default: 0,
  },
})

const emit = defineEmits(['update', 'reset'])

const count = ref(props.initialCount)

const doubleCount = computed(() => count.value * 2)

function increment() {
  count.value++
  emit('update', count.value)
}

function decrement() {
  if (count.value > 0) {
    count.value--
    emit('update', count.value)
  }
}

function reset() {
  count.value = 0
  emit('reset')
}

defineExpose({ count, increment, decrement, reset })
</script>
```

**测试文件**：

```typescript
// src/components/Counter.test.ts
import { describe, it, expect, test, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import Counter from './Counter.vue'

describe('Counter 组件', () => {
  it('初始渲染', () => {
    const wrapper = mount(Counter)
    
    // 查找文本内容
    expect(wrapper.text()).toContain('计数器：0')
    expect(wrapper.text()).toContain('双倍计数：0')
  })

  test('初始值配置', () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 10 },
    })
    
    expect(wrapper.text()).toContain('计数器：10')
    expect(wrapper.text()).toContain('双倍计数：20')
  })

  test('增加按钮', async () => {
    const wrapper = mount(Counter)
    const incrementBtn = wrapper.findAll('button')[1]  // 第二个按钮是 +
    
    await incrementBtn.trigger('click')
    await incrementBtn.trigger('click')
    await incrementBtn.trigger('click')
    
    expect(wrapper.text()).toContain('计数器：3')
    expect(wrapper.text()).toContain('双倍计数：6')
  })

  test('减少按钮', async () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 5 },
    })
    
    const decrementBtn = wrapper.find('button:first-child')  // 第一个按钮是 -
    await decrementBtn.trigger('click')
    
    expect(wrapper.text()).toContain('计数器：4')
  })

  test('减少到 0 后禁用', async () => {
    const wrapper = mount(Counter, { props: { initialCount: 0 } })
    
    const decrementBtn = wrapper.find('button:first-child')
    
    // 初始时应该禁用
    expect(decrementBtn.attributes('disabled')).toBeDefined()
    
    // 点击增加
    await wrapper.findAll('button')[1].trigger('click')
    
    // 取消禁用
    expect(decrementBtn.attributes('disabled')).toBeUndefined()
  })

  test('重置按钮', async () => {
    const wrapper = mount(Counter, { props: { initialCount: 10 } })
    
    // 点击增加几次
    await wrapper.findAll('button')[1].trigger('click')
    await wrapper.findAll('button')[1].trigger('click')
    
    // 期望是 12
    expect(wrapper.text()).toContain('计数器：12')
    
    // 点击重置
    await wrapper.find('button:last-child').trigger('click')
    
    // 回到初始值 10
    expect(wrapper.text()).toContain('计数器：10')
  })

  test('emit 事件', async () => {
    const wrapper = mount(Counter, { props: { initialCount: 0 } })
    
    await wrapper.findAll('button')[1].trigger('click')
    
    // 检查 emit 的事件
    expect(wrapper.emitted('update')).toBeTruthy()
    expect(wrapper.emitted('update')![0]).toEqual([1])  // 参数是 [1]
  })

  test('暴露的方法', async () => {
    const wrapper = mount(Counter)
    
    // 获取组件实例（Vue 3 + @vue/test-utils v2 使用 componentVM）
    const vm = wrapper.componentVM as any
    
    // 调用暴露的方法
    vm.increment()
    vm.increment()
    
    expect(wrapper.text()).toContain('计数器：2')
  })
})
```

### 13.1.5 组件测试（React Testing Library）

**React Testing Library** 的理念和 Vue Testing Library 一样：测试行为，而不是实现。

**安装**：

```bash
pnpm add -D @testing-library/react @testing-library/jest-dom @testing-library/user-event vitest
```

**React 组件测试**：

```tsx
// src/components/Counter.tsx
import { useState } from 'react'

interface CounterProps {
  initialCount?: number
  onUpdate?: (count: number) => void
  onReset?: () => void
}

export function Counter({ 
  initialCount = 0, 
  onUpdate, 
  onReset 
}: CounterProps) {
  const [count, setCount] = useState(initialCount)

  const doubleCount = count * 2

  function increment() {
    const newCount = count + 1
    setCount(newCount)
    onUpdate?.(newCount)
  }

  function decrement() {
    if (count > 0) {
      const newCount = count - 1
      setCount(newCount)
      onUpdate?.(newCount)
    }
  }

  function reset() {
    setCount(initialCount)
    onReset?.()
  }

  return (
    <div className="counter">
      <h1>计数器：{count}</h1>
      <p>双倍计数：{doubleCount}</p>
      
      <button onClick={decrement} disabled={count <= 0}>-</button>
      <button onClick={increment}>+</button>
      <button onClick={reset}>重置</button>
    </div>
  )
}
```

**测试文件**：

```tsx
// src/components/Counter.test.tsx
import { describe, it, expect, test, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Counter } from './Counter'

describe('Counter 组件', () => {
  it('初始渲染', () => {
    render(<Counter />)
    
    expect(screen.getByText('计数器：0')).toBeInTheDocument()
    expect(screen.getByText('双倍计数：0')).toBeInTheDocument()
  })

  test('初始值配置', () => {
    render(<Counter initialCount={10} />)
    
    expect(screen.getByText('计数器：10')).toBeInTheDocument()
    expect(screen.getByText('双倍计数：20')).toBeInTheDocument()
  })

  test('增加按钮', async () => {
    const user = userEvent.setup()
    render(<Counter />)
    
    const incrementBtn = screen.getByRole('button', { name: '+' })
    await user.click(incrementBtn)
    await user.click(incrementBtn)
    await user.click(incrementBtn)
    
    expect(screen.getByText('计数器：3')).toBeInTheDocument()
  })

  test('减少按钮', async () => {
    const user = userEvent.setup()
    render(<Counter initialCount={5} />)
    
    const decrementBtn = screen.getByRole('button', { name: '-' })
    await user.click(decrementBtn)
    
    expect(screen.getByText('计数器：4')).toBeInTheDocument()
  })

  test('减少到 0 后禁用', async () => {
    const user = userEvent.setup()
    render(<Counter initialCount={0} />)
    
    const decrementBtn = screen.getByRole('button', { name: '-' })
    expect(decrementBtn).toBeDisabled()
    
    const incrementBtn = screen.getByRole('button', { name: '+' })
    await user.click(incrementBtn)
    
    expect(decrementBtn).not.toBeDisabled()
  })

  test('onUpdate 回调', async () => {
    const onUpdate = vi.fn()
    const user = userEvent.setup()
    render(<Counter onUpdate={onUpdate} />)
    
    await user.click(screen.getByRole('button', { name: '+' }))
    
    expect(onUpdate).toHaveBeenCalledWith(1)
    expect(onUpdate).toHaveBeenCalledTimes(1)
  })
})
```

### 13.1.6 覆盖率报告

**配置覆盖率**：

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      reportsDirectory: './coverage',
      exclude: [
        'node_modules/**',
        'src/tests/**',
        '**/*.d.ts',
        '**/*.config.*',
        '**/dist/**',
        '**/virtual:**',
        '**/__xhm__/**',
      ],
      thresholds: {
        // 设置覆盖率门槛
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80,
      },
    },
  },
})
```

**覆盖率报告输出**：

```
---------------------------|---------|----------|---------|---------|
File                       | % Stmts | % Branch | % Funcs | % Lines |
---------------------------|---------|----------|---------|---------|
src/utils/math.ts          |   100.00|    100.00|   100.00|   100.00|
src/components/Counter.vue |    85.71|    100.00|    66.67|    85.71|
---------------------------|---------|----------|---------|---------|
All files                  |    91.67|    100.00|    80.00|    91.67|
---------------------------|---------|----------|---------|---------|
```

### 13.1.7 Mock 函数与模块

**Mock 函数**：

```typescript
// src/utils/api.test.ts
import { describe, it, expect, test, vi, beforeEach } from 'vitest'
import { fetchUser, fetchUsers } from './api'

// Mock fetch
const mockFetch = vi.fn()
global.fetch = mockFetch

describe('API 函数', () => {
  beforeEach(() => {
    mockFetch.mockReset()  // 每个测试前重置
  })

  test('fetchUser 返回用户数据', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, name: '小明', age: 25 }),
    })

    const user = await fetchUser(1)
    
    expect(user).toEqual({ id: 1, name: '小明', age: 25 })
    expect(mockFetch).toHaveBeenCalledWith('/api/users/1')
  })

  test('fetchUsers 返回用户列表', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [
        { id: 1, name: '小明' },
        { id: 2, name: '小红' },
      ],
    })

    const users = await fetchUsers()
    
    expect(users).toHaveLength(2)
    expect(users[0].name).toBe('小明')
  })

  test('fetchUser 处理错误', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
    })

    await expect(fetchUser(999)).rejects.toThrow('用户不存在')
  })
})
```

**Mock 模块**：

```typescript
// src/utils/date.test.ts
import { describe, it, expect, vi } from 'vitest'

// Mock dayjs
vi.mock('dayjs', () => ({
  default: vi.fn(() => ({
    format: vi.fn().mockReturnValue('2024-03-27'),
    add: vi.fn().mockReturnThis(),
    subtract: vi.fn().mockReturnThis(),
  })),
}))

import dayjs from 'dayjs'
import { formatDate, addDays } from './date'

describe('日期工具', () => {
  it('formatDate 格式化日期', () => {
    const result = formatDate(new Date('2024-03-27'))
    
    expect(dayjs).toHaveBeenCalledWith(new Date('2024-03-27'))
    expect(result).toBe('2024-03-27')
  })
})
```

### 13.1.8 Vitest 配置详解

**vitest.config.ts 完整配置**：

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    // 全局 API
    globals: true,
    
    // 测试环境
    // 'jsdom' | 'node' | 'happy-dom'
    environment: 'jsdom',
    
    // 全局 setup 文件
    setupFiles: ['./src/tests/setup.ts'],
    
    // 包含的文件
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    
    // 排除的文件
    exclude: ['node_modules', 'dist', '**/*.md'],
    
    // 依赖反转
    // transformMode: {},
    
    // 覆盖
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/'],
    },
    
    // 线程数
    // workers: 4,
    
    // 测试超时
    testTimeout: 5000,
    
    // 断言超时
    expectTimeout: 5000,
    
    // 序列执行
    // sequence: { type: 'serial' },
    
    // 并行执行
    // sequence: { type: 'parallel' },
    
    // 慢测试报告
    // slowTestThreshold: 200,
    
    // 序列
    // sequence: { shuffle: false },
    
    // 重试次数
    // retry: 0,
    
    // 单独运行
    // isolate: true,
    
    // 报告器
    // reporters: ['default', 'verbose'],
    
    // 输出
    outputFile: {
      json: './coverage/test-results.json',
    },
  },
})
```

### 13.1.9 快照测试

**快照测试**：保存组件渲染结果，下次运行时对比。

```typescript
// src/components/Header.test.tsx
import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import { Header } from './Header'

describe('Header 组件', () => {
  it('渲染结果与快照匹配', () => {
    const { container } = render(<Header title="测试标题" />)
    
    // toMatchSnapshot：与上次保存的快照对比
    expect(container).toMatchSnapshot()
  })

  it('更新快照', async () => {
    // 当组件确实改变了，需要更新快照
    // 运行：vitest --update
    // 或者：vitest -u
  })
})
```

### 13.1.10 测试覆盖率门槛

**设置强制覆盖率门槛**：

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      thresholds: {
        // 文件级别
        perFile: true,
        
        // 全局门槛
        statements: 80,
        branches: 75,
        functions: 80,
        lines: 80,
        
        // 特定文件的门槛
        'src/utils/**/*.ts': {
          statements: 90,
          branches: 90,
        },
      },
    },
  },
})
```

### 13.1.11 测试并行执行

Vitest 默认并行执行测试，可以提高速度。

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    // 并行线程数
    workers: 4,
    
    // 使用 V8 并行引擎（更快）
    pool: 'forks',  // 'threads' | 'forks' | 'vmForks'
    
    // 序列执行（调试用）
    poolOptions: {
      threads: {
        // 线程数
        singleThread: false,
      },
      forks: {
        // 最大并行进程数
        maxForks: 4,
      },
    },
  },
})
```

---

## 13.2 E2E 测试

### 13.2.1 Playwright 集成

**Playwright** 是微软出品的 E2E 测试框架，支持所有现代浏览器。

**安装**：

```bash
pnpm add -D @playwright/test
pnpm exec playwright install chromium
```

### 13.2.2 Playwright 配置

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  // 测试目录
  testDir: './tests/e2e',
  
  // 并行执行
  fullyParallel: true,
  
  // 失败时重试
  retries: process.env.CI ? 2 : 0,
  
  // 工作线程数
  workers: process.env.CI ? 4 : undefined,
  
  // 报告器
  reporter: [
    ['html'],
    ['list'],
  ],
  
  // 全局超时
  timeout: 30 * 1000,
  
  // 期望超时
  expect: {
    timeout: 5000,
  },
  
  // 全局预处理
  use: {
    // 基础 URL
    baseURL: 'http://localhost:5173',
    
    // 截图模式
    screenshot: 'only-on-failure',
    
    // 视频录制
    video: 'retain-on-failure',
    
    // 跟踪
    trace: 'on-first-retry',
    
    // 截图
    headless: true,
  },
  
  // 项目配置
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
  
  // WebServer 配置
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
})
```

### 13.2.3 测试用例编写

```typescript
// tests/e2e/home.spec.ts
import { test, expect } from '@playwright/test'

test.describe('首页', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('页面标题正确', async ({ page }) => {
    await expect(page).toHaveTitle(/我的应用/)
  })

  test('导航链接存在', async ({ page }) => {
    await expect(page.locator('nav')).toContainText('首页')
    await expect(page.locator('nav')).toContainText('关于')
    await expect(page.locator('nav')).toContainText('用户')
  })

  test('点击导航到关于页', async ({ page }) => {
    await page.click('text=关于')
    await expect(page).toHaveURL(/\/about/)
    await expect(page.locator('h1')).toContainText('关于')
  })

  test('计数器增加功能', async ({ page }) => {
    // 查找 + 按钮
    const incrementBtn = page.locator('button', { hasText: '+' })
    
    // 初始值应该是 0
    await expect(page.locator('text=计数器：0')).toBeVisible()
    
    // 点击 + 按钮
    await incrementBtn.click()
    await expect(page.locator('text=计数器：1')).toBeVisible()
    
    // 双倍计数应该是 2
    await expect(page.locator('text=双倍计数：2')).toBeVisible()
  })

  test('表单提交', async ({ page }) => {
    await page.fill('input[name="username"]', 'testuser')
    await page.fill('input[name="password"]', 'password123')
    await page.click('button[type="submit"]')
    
    // 等待成功消息
    await expect(page.locator('.success-message')).toBeVisible({ timeout: 5000 })
    await expect(page.locator('.success-message')).toContainText('登录成功')
  })

  test('404 页面', async ({ page }) => {
    await page.goto('/non-existent-page')
    await expect(page.locator('h1')).toContainText('404')
  })
})
```

### 13.2.4 Cypress 集成

**Cypress** 是另一个流行的 E2E 测试框架。

**安装**：

```bash
pnpm add -D cypress
```

### 13.2.5 Nightwatch 集成

**Nightwatch.js** 是基于 Selenium 的 E2E 测试框架。

**安装**：

```bash
pnpm add -D nightwatch @nightwatch/browserstack
```

### 13.2.6 测试报告与分析

**Playwright HTML 报告**：

```bash
# 运行测试，生成报告
pnpm playwright test

# 查看 HTML 报告
pnpm playwright show-report
```

---

## 13.3 调试技巧

### 13.3.1 VS Code 调试配置

**launch.json**：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug: Vite Dev Server",
      "type": "pwa-node",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "runtimeExecutable": "pnpm",
      "runtimeArgs": ["dev"],
      "skipFiles": ["<node_internals>/**"],
      "console": "integratedTerminal",
      "env": {
        "NODE_ENV": "development"
      }
    },
    {
      "name": "Debug: Vitest",
      "type": "pwa-node",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "runtimeExecutable": "pnpm",
      "runtimeArgs": ["test", "--run"],
      "skipFiles": ["<node_internals>/**"],
      "console": "integratedTerminal"
    },
    {
      "name": "Debug: Vite Build",
      "type": "pwa-node",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "runtimeExecutable": "pnpm",
      "runtimeArgs": ["build"],
      "skipFiles": ["<node_internals>/**"],
      "console": "integratedTerminal"
    },
    {
      "name": "Debug: Current Test File",
      "type": "pwa-node",
      "request": "launch",
      "cwd": "${workspaceFolder}",
      "runtimeExecutable": "pnpm",
      "runtimeArgs": ["test", "--run", "${relativeFile}"],
      "skipFiles": ["<node_internals>/**"],
      "console": "integratedTerminal"
    }
  ]
}
```

**tasks.json（辅助任务）**：

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Vite: Dev Server",
      "type": "shell",
      "command": "pnpm dev",
      "problemMatcher": [],
      "group": "none",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Vite: Build",
      "type": "shell",
      "command": "pnpm build",
      "problemMatcher": [],
      "group": "build",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Vitest: Run",
      "type": "shell",
      "command": "pnpm test:run",
      "problemMatcher": [],
      "group": "test"
    },
    {
      "label": "Vitest: Watch",
      "type": "shell",
      "command": "pnpm test",
      "problemMatcher": [],
      "group": "test"
    }
  ]
}
```

### 13.3.2 Chrome DevTools 调试

**Sources 面板**：

1. 打开 DevTools（F12）
2. 切换到 Sources 标签
3. 找到你的源码文件（在 `vite://` 目录下，这是 Vite 的源码标识）
4. 在代码行号上点击设置断点

**Vue DevTools**：

```bash
# Vue 项目安装 Vue DevTools
# Chrome 扩展商店搜索 "Vue DevTools"
```

**React DevTools**：

```bash
# Chrome 扩展商店搜索 "React DevTools"
```

### 13.3.3 源码映射问题排查

**sourcemap 不生效？**：

```javascript
// vite.config.js
export default defineConfig({
  build: {
    // 生成 sourcemap
    sourcemap: true,
    
    // 或者只生成，不内联
    sourcemap: 'hidden',
  },
})
```

### 13.3.4 Network 网络请求调试

**Network 面板使用技巧**：

1. **过滤请求**：输入 URL 或关键字过滤
2. **查看请求详情**：点击请求，查看 Headers/Payload/Response
3. **复制请求**：右键请求，选择 Copy → Copy as fetch/cURL
4. **重发请求**：右键请求，选择 Replay XHR/fetch

### 13.3.5 性能分析

**Performance 面板**：

1. 打开 DevTools（F12）
2. 切换到 Performance 标签
3. 点击录制，执行操作，然后停止
4. 查看火焰图，分析性能瓶颈

### 13.3.6 内存泄漏排查

**Memory 面板**：

1. 打开 DevTools（F12）
2. 切换到 Memory 标签
3. 选择 Heap Snapshot
4. 点击 Take Snapshot
5. 执行一些操作
6. 再拍一张快照
7. 对比两张快照，查找内存增长

---

## 13.4 CI 环境测试

### 13.4.1 GitHub Actions 集成

**.github/workflows/test.yml**：

```yaml
name: Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 9
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      
      - name: Run type check
        run: pnpm type-check
      
      - name: Run unit tests
        run: pnpm test:run --coverage
      
      - name: Run e2e tests
        run: pnpm test:e2e
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
          fail_ci_if_error: false
```

### 13.4.2 GitLab CI 集成

**.gitlab-ci.yml**：

```yaml
stages:
  - install
  - test
  - build

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .pnpm-store/

install:
  stage: install
  image: node:20
  script:
    - corepack enable
    - pnpm install --frozen-lockfile

unit-test:
  stage: test
  image: node:20
  script:
    - pnpm test:run --coverage
  coverage: /All files[^|]*\|[^|]*\s+([\d\.]+)/
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

e2e-test:
  stage: test
  image: cypress/base:18
  script:
    - pnpm test:e2e:run
  artifacts:
    when: always
    paths:
      - playwright-report/
      - test-results/

build:
  stage: build
  image: node:20
  script:
    - pnpm build
  artifacts:
    paths:
      - dist/
```

### 13.4.3 Jenkins 集成

**Jenkinsfile**：

```groovy
pipeline {
  agent any
  
  stages {
    stage('Install') {
      steps {
        sh 'corepack enable'
        sh 'pnpm install --frozen-lockfile'
      }
    }
    
    stage('Test') {
      steps {
        sh 'pnpm test:run --coverage'
        junit 'junit.xml'
        publishHTML([
          reportDir: 'coverage',
          reportFiles: 'index.html',
          reportName: 'Coverage Report'
        ])
      }
    }
    
    stage('Build') {
      steps {
        sh 'pnpm build'
      }
    }
  }
  
  post {
    always {
      cleanWs()
    }
  }
}
```

### 13.4.4 测试命令优化

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",
    "test:all": "pnpm test:run && pnpm test:e2e"
  }
}
```

### 13.4.5 测试覆盖率集成

**Codecov 集成**：

```bash
pnpm add -D @codecov/vite-plugin
```

```yaml
# GitHub Actions 中
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    files: ./coverage/lcov.info
    fail_ci_if_error: false
```

---

## 13.5 本章小结

### 🎉 本章总结

这一章我们学习了 Vite 项目中的测试与调试技能：

1. **单元测试**：Vitest 安装与配置、第一个测试用例、Vue Testing Library（Vue 组件测试）、React Testing Library（React 组件测试）、覆盖率报告、Mock 函数与模块、快照测试

2. **E2E 测试**：Playwright 安装与配置、测试用例编写、Cypress 集成、测试报告分析

3. **调试技巧**：VS Code launch.json 配置、Chrome DevTools 调试、源码映射、网络请求调试、性能分析、内存泄漏排查

4. **CI 环境测试**：GitHub Actions 配置、GitLab CI 配置、Jenkins 配置、测试命令优化、覆盖率集成

### 📝 本章练习

1. **Vitest 实战**：为你的工具函数编写 3-5 个单元测试

2. **组件测试**：为你的 Vue/React 组件编写测试用例

3. **Playwright E2E**：编写 3 个 E2E 测试用例，覆盖主要功能流程

4. **GitHub Actions**：配置一个完整的 CI 流程

5. **覆盖率提升**：把测试覆盖率提升到 80% 以上

---

> 📌 **预告**：下一章我们将进入 **完整项目实战**，从零开始搭建一个完整的 Vue/React 项目，包含需求分析、技术选型、项目搭建、功能开发、移动端适配、国际化、部署上线。敬请期待！
