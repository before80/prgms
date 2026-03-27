+++
title = "第33章 React生态系统与优秀库"
weight = 330
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-33 - React 生态精选库

## 33.1 动画：Framer Motion

### 33.1.1 motion 组件的基本用法

**为什么需要动画库？** 想象没有动画库的时候，你想让一个 div 淡入+移动+缩放，要写一堆 `setInterval` + `CSS transition`，还要手动管理动画状态。代码又臭又长，动画间的协调更是噩梦。

Framer Motion 是 React 中最流行的动画库，它的核心理念是：**把动画当成组件的"属性"来声明**——你要做的只是描述"从哪到哪"，框架帮你搞定中间的一切。

```bash
npm install framer-motion
```

```jsx
import { motion } from 'framer-motion'

function AnimatedBox() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.5 }}  // 初始状态
      animate={{ opacity: 1, scale: 1 }}     // 最终状态
      transition={{ duration: 0.5 }}          // 过渡配置
      whileHover={{ scale: 1.1 }}           // 悬停时动画
    >
      Hello, Animation!
    </motion.div>
  )
}
```

### 33.1.2 过渡动画：animate / initial / exit

```jsx
import { motion, AnimatePresence } from 'framer-motion'

function Modal({ isOpen }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <ModalContent />
        </motion.div>
      )}
    </AnimatePresence>
  )
}
```

### 33.1.3 手势动画：drag / hover / tap

```jsx
function DraggableBox() {
  return (
    <motion.div
      drag                          // 可拖拽
      dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
    >
      拖我！
    </motion.div>
  )
}
```

### 33.1.4 页面过渡动画

```jsx
import { motion } from 'framer-motion'

const pageVariants = {
  initial: { opacity: 0, x: '-100%' },
  in: { opacity: 1, x: 0 },
  out: { opacity: 0, x: '100%' }
}

function Page({ children }) {
  return (
    <motion.div
      initial="initial"
      animate="in"
      exit="out"
      variants={pageVariants}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}
```

---

## 33.2 拖拽：dnd-kit

### 33.2.1 DndContext 的使用

**为什么需要拖拽库？** 拖拽听起来简单（鼠标按下→移动→松开），但背后涉及：碰撞检测、坐标计算、DOM 位置更新、性能优化（拖拽时 60fps 不能卡）……自己写能写，但很容易写出一堆 bug。

`dnd-kit` 是目前 React 生态中最现代的拖拽库，**专为性能优化而生**——它用 CSS transform 而不是 top/left 定位，天然避开了重排（reflow）的性能陷阱。

```bash
npm install @dnd-kit/core @dnd-kit/sortable
```

```jsx
import { DndContext, closestCenter } from '@dnd-kit/core'

function App() {
  return (
    <DndContext collisionDetection={closestCenter}>
      <SortableContext items={items}>
        {items.map(id => <SortableItem key={id} id={id} />)}
      </SortableContext>
    </DndContext>
  )
}
```

### 33.2.2 sortable 列表的实现

```jsx
import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'

function SortableItem({ id }) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition
  }

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {id}
    </div>
  )
}
```

---

## 33.3 图表：Recharts / ECharts

### 33.3.1 Recharts 的基础图表

**为什么需要图表库？** Canvas / SVG 画图表并不难，但坐标轴、刻度、图例、Tooltip、响应式……这些"配套零件"要写半天。图表库的价值就是把这些繁琐的东西封装好，让你"告诉它数据，它帮你画图"。

Recharts 是 React 中最流行的图表库，API 设计直观，用法接近 React 组件思维——每个图表都是 React 组件，数据是 props，灵活组合。

```jsx
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'

function ChartDemo() {
  const data = [
    { name: '1月', value: 400 },
    { name: '2月', value: 300 },
    { name: '3月', value: 200 }
  ]

  return (
    <>
      {/* 折线图 */}
      <LineChart data={data}>
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
      </LineChart>

      {/* 柱状图 */}
      <BarChart data={data}>
        <Bar dataKey="value" fill="#82ca9d" />
      </BarChart>

      {/* 饼图 */}
      <PieChart>
        <Pie
          data={data}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={80}
          label
        >
          {data.map((_, index) => (
            <Cell key={`cell-${index}`} fill={['#8884d8', '#82ca9d', '#ffc658'][index % 3]} />
          ))}
        </Pie>
      </PieChart>
    </>
  )
}
```

Recharts 约定：`data` 数组中每项的 `name` 字段自动作为 X 轴或标签，其他字段绑定 `dataKey` 即可。上手成本极低，画个折线图通常不超过 10 行代码。

### 33.3.2 ECharts for React：echarts-for-react

如果 Recharts 满足不了你的图表复杂度和视觉要求，可以试试 **ECharts**（百度开源，图表类型非常全面）。配合 `echarts-for-react` 封装成 React 组件：

```bash
npm install echarts echarts-for-react
```

```jsx
import ReactECharts from 'echarts-for-react'

function EChartsDemo() {
  const option = {
    title: { text: '月度销售额' },
    tooltip: {},
    xAxis: { data: ['1月', '2月', '3月'] },
    yAxis: {},
    series: [{
      name: '销售额',
      type: 'bar',
      data: [400, 300, 200]
    }]
  }

  return <ReactECharts option={option} style={{ height: 400 }} />
}
```

ECharts 的优点是图表类型极其丰富（地图、热力图、关系图等），自定义能力强；缺点是配置项较多、学习曲线比 Recharts 陡一些。

---

## 33.4 国际化：react-i18next

### 33.4.1 i18n 的基本配置

```bash
npm install react-i18next i18next
```

```jsx
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: { greeting: 'Hello' } },
    zh: { translation: { greeting: '你好' } }
  },
  lng: 'zh',
  fallbackLng: 'en'
})
```

### 33.4.2 useTranslation Hook 的使用

```jsx
import { useTranslation } from 'react-i18next'

function Greeting() {
  const { t, i18n } = useTranslation()

  return (
    <div>
      <p>{t('greeting')}</p>
      <button onClick={() => i18n.changeLanguage('en')}>EN</button>
      <button onClick={() => i18n.changeLanguage('zh')}>中文</button>
    </div>
  )
}
```

---

## 本章小结

本章我们学习了 React 生态中的精选库：

- **Framer Motion**：最流行的动画库，支持过渡动画、手势动画、页面过渡
- **dnd-kit**：现代拖拽库，性能优秀
- **Recharts**：图表库，支持折线图、柱状图、饼图
- **react-i18next**：国际化解决方案

这些库覆盖了动画、拖拽、图表、国际化等常见需求！下一章我们将学习 **React 与 AI**！🤖