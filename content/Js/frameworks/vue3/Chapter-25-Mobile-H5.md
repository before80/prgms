+++
title = "第25章 实战：移动端 H5 项目与 PWA"
weight = 250
date = "2026-03-25T12:54:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十五章 实战：移动端 H5 项目与 PWA

> PC 端的 Vue 项目你可能已经玩得很溜了，但移动端完全是另一个世界——屏幕小、触控操作、网络不稳定、性能有限、还需要考虑在各种奇怪尺寸的设备上正常显示。本章教你如何用 Vue 3 开发真正能在手机上跑起来的 H5 应用，包括移动端适配方案、手势操作、移动端性能优化，以及让 H5 应用拥有接近原生体验的 PWA 技术。学完这章，你的 Vue 技能树又解锁了一个新分支。

## 25.1 移动端适配方案

### 25.1.1 viewport 视口配置

移动端适配的第一步，是正确配置 `<meta name="viewport">`。viewport 是浏览器用来控制页面缩放和布局的窗口，不配置的话，移动端浏览器会默认以 980px 的宽度来渲染页面，然后缩放到屏幕大小——结果是页面被缩小成一团，根本看不清。

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <!-- viewport 配置是移动端适配的第一步 -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="format-detection" content="telephone=no">
  <meta name="theme-color" content="#42b883">
  <title>Vue3 移动端应用</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

**viewport 各参数详解**：

| 参数 | 作用 |
|------|------|
| `width=device-width` | 视口宽度等于设备宽度 |
| `initial-scale=1.0` | 初始缩放比例为 1（不缩放） |
| `maximum-scale=1.0` | 最大缩放比例（禁止用户放大） |
| `minimum-scale=1.0` | 最小缩放比例（禁止用户缩小） |
| `user-scalable=no` | 禁止用户缩放（完全锁定，可根据需求调整） |
| `viewport-fit=cover` | 让视口填满整个屏幕（包括刘海屏等异形屏） |

### 25.1.2 rem 适配方案

rem 是相对于根元素（`<html>`）字体大小的单位。rem 适配的核心思路是：**根据屏幕宽度动态设置 `<html>` 的 font-size`，这样所有使用 rem 的元素都会自动按比例缩放**。

```javascript
// rem.js - 在 main.ts 入口文件的最前面引入
// 动态计算并设置 html 的 font-size

// 设计稿宽度（通常 375，对应 iPhone 6/7/8）
const DESIGN_WIDTH = 375
// 最小支持宽度
const MIN_WIDTH = 320
// 最大支持宽度
const MAX_WIDTH = 540

function setRem() {
  // 获取视口宽度
  let htmlWidth = document.documentElement.clientWidth

  // 限制在最小和最大宽度之间
  htmlWidth = Math.max(htmlWidth, MIN_WIDTH)
  htmlWidth = Math.min(htmlWidth, MAX_WIDTH)

  // 计算 font-size
  // 公式：屏幕宽度 / 设计稿宽度 * 100
  // 乘以 100 是为了让计算结果更好记（10rem = 屏幕宽度的 1/10）
  const fontSize = (htmlWidth / DESIGN_WIDTH) * 100

  // 设置到 html 元素
  document.documentElement.style.fontSize = `${fontSize}px`
}

// 初始化
setRem()

// 监听窗口大小变化（屏幕旋转、调整窗口大小时重新计算）
window.addEventListener('resize', setRem)
window.addEventListener('orientationchange', setRem)

// 也可以用 ResizeObserver 监听
// const observer = new ResizeObserver(setRem)
// observer.observe(document.documentElement)
```

```scss
// variables.scss - 全局样式变量
// 假设设计稿宽度是 375px，元素在设计稿上量出来是 100px

// 使用方式：
// 设计稿上 100px -> 代码里写 1rem（因为 font-size 是 37.5px 时，1rem = 37.5px）
// 设计稿上 75px  -> 代码里写 0.75rem
// 设计稿上 50px  -> 代码里写 0.5rem

// 常用设计尺寸换算（基于设计稿 375px）
$base-font-size: 37.5px;  // 即 (375/375) * 37.5 = 37.5px

// 或者直接用函数
@function px2rem($px) {
  @return $px / $base-font-size * 1rem;
}

// 使用示例
.box {
  width: px2rem(100);  // 100px
  height: px2rem(50);  // 50px
  padding: px2rem(15); // 15px
}
```

### 25.1.3 vw/vh 适配方案

vw（Viewport Width）和 vh（Viewport Height）是 CSS3 新增的单位，分别表示视口宽度的 1% 和视口高度的 1%。相比 rem，vw/vh 方案更简洁，是目前流行的适配方案之一。

```scss
// vw 适配（不需要 JS，纯 CSS）
// 100vw 等于屏幕宽度，1vw = 屏幕宽度的 1%
// 设计稿 375px 上的 100px -> 100/375*100 = 26.67vw

// scss 函数
$design-width: 375;

@function vw($px) {
  @return $px / $design-width * 100vw;
}

// 使用
.box {
  width: vw(100);
  height: vw(50);
  font-size: vw(16);
  padding: vw(15);
}

// PostCSS 插件自动转换（推荐）
// 安装 postcss-px-to-viewport
// 配置后可以直接写 px，插件自动转成 vw
```

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    'postcss-px-to-viewport': {
      viewportWidth: 375,      // 设计稿宽度
      viewportHeight: 812,    // 设计稿高度（可选）
      unitPrecision: 5,        // 转换精度
      viewportUnit: 'vw',      // 转换成的单位
      fontViewportUnit: 'vw',  // 字体转换成的单位
      selectorBlackList: ['.ignore', '.hairlines'],  // 不转换的类名
      minPixelValue: 1,        // 最小转换值（小于1px不转换）
      mediaQuery: false,       // 是否转换媒体查询中的 px
      exclude: [/node_modules/] // 排除的文件
    }
  }
}
```

### 25.1.4 移动端特殊样式处理

```scss
// global.scss
// 移动端常用样式重置

* {
  box-sizing: border-box;
  -webkit-tap-highlight-color: transparent;  // 去除点击高亮
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;  // 字体抗锯齿
  -moz-osx-font-smoothing: grayscale;
  text-size-adjust: 100%;  // 禁止微信浏览器自动调整字体大小
}

// 禁止长按弹出菜单
.no-select {
  -webkit-user-select: none;
  user-select: none;
}

// 禁止系统默认长按行为
.no-touch-callout {
  -webkit-touch-callout: none;
  touch-callout: none;
}

// 安全区域适配（iPhone X 及以后的刘海屏）
body {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

// 滚动优化（支持惯性滚动）
.scroller {
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

// 1px 边框（高清屏幕上的 1px 边框问题）
.border-1px {
  position: relative;
  &::after {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 1px;
    background: #e5e5e5;
    transform: scaleY(0.5);  // 缩小到一半，即物理 1px
  }
}

// flex 布局快速工具类
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-1 { flex: 1; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.gap-1 { gap: 0.1rem; }
.gap-2 { gap: 0.2rem; }
```

## 25.2 手势与交互

### 25.2.1 常见移动端手势

移动端的手势远比 PC 端的鼠标点击丰富。常见的手势包括：
- **点击（Tap）**：快速触摸并抬起
- **长按（Long Press）**：触摸并保持一段时间
- **滑动（Swipe）**：在一个方向上快速滑动
- **拖拽（Drag）**：触摸并移动
- **捏合缩放（Pinch）**：两指捏合放大或缩小
- **旋转（Rotate）**：两指旋转

```typescript
// composables/useTouch.ts
import { ref, onMounted, onUnmounted } from 'vue'

interface TouchState {
  startX: number
  startY: number
  currentX: number
  currentY: number
  deltaX: number
  deltaY: number
  offsetX: number
  offsetY: number
  direction: 'left' | 'right' | 'up' | 'down' | null
  distance: number
  duration: number
  scale: number
  rotation: number
}

export function useTouch(elementRef: HTMLElement | null) {
  const state = ref<TouchState>({
    startX: 0,
    startY: 0,
    currentX: 0,
    currentY: 0,
    deltaX: 0,
    deltaY: 0,
    offsetX: 0,
    offsetY: 0,
    direction: null,
    distance: 0,
    duration: 0,
    scale: 1,
    rotation: 0
  })

  let startTime = 0
  let initialDistance = 0
  let initialRotation = 0
  let initialScale = 1

  const handleTouchStart = (e: TouchEvent) => {
    const touch = e.touches[0]
    state.value.startX = touch.clientX
    state.value.startY = touch.clientY
    state.value.currentX = touch.clientX
    state.value.currentY = touch.clientY
    state.value.deltaX = 0
    state.value.deltaY = 0
    state.value.offsetX = 0
    state.value.offsetY = 0
    startTime = Date.now()

    // 多点触控（用于缩放和旋转）
    if (e.touches.length === 2) {
      initialDistance = getDistance(e.touches[0], e.touches[1])
      initialRotation = getRotation(e.touches[0], e.touches[1])
      initialScale = state.value.scale
    }
  }

  const handleTouchMove = (e: TouchEvent) => {
    const touch = e.touches[0]
    state.value.currentX = touch.clientX
    state.value.currentY = touch.clientY
    state.value.deltaX = state.value.currentX - state.value.startX
    state.value.deltaY = state.value.currentY - state.value.startY
    state.value.offsetX = state.value.deltaX
    state.value.offsetY = state.value.deltaY

    // 判断滑动方向
    if (Math.abs(state.value.deltaX) > Math.abs(state.value.deltaY)) {
      state.value.direction = state.value.deltaX > 0 ? 'right' : 'left'
      state.value.distance = Math.abs(state.value.deltaX)
    } else {
      state.value.direction = state.value.deltaY > 0 ? 'down' : 'up'
      state.value.distance = Math.abs(state.value.deltaY)
    }

    // 多点触控：计算缩放和旋转
    if (e.touches.length === 2) {
      const currentDistance = getDistance(e.touches[0], e.touches[1])
      const currentRotation = getRotation(e.touches[0], e.touches[1])

      state.value.scale = initialScale * (currentDistance / initialDistance)
      state.value.rotation = currentRotation - initialRotation
    }
  }

  const handleTouchEnd = () => {
    state.value.duration = Date.now() - startTime
    // 重置缩放和旋转（单手操作时）
    if (state.value.scale !== 1) {
      state.value.scale = 1
      state.value.rotation = 0
    }
  }

  // 计算两点之间的距离
  const getDistance = (p1: Touch, p2: Touch) => {
    const dx = p2.clientX - p1.clientX
    const dy = p2.clientY - p1.clientY
    return Math.sqrt(dx * dx + dy * dy)
  }

  // 计算两点的旋转角度
  const getRotation = (p1: Touch, p2: Touch) => {
    const dx = p2.clientX - p1.clientX
    const dy = p2.clientY - p1.clientY
    return Math.atan2(dy, dx) * (180 / Math.PI)
  }

  onMounted(() => {
    if (!elementRef) return
    elementRef.addEventListener('touchstart', handleTouchStart, { passive: true })
    elementRef.addEventListener('touchmove', handleTouchMove, { passive: true })
    elementRef.addEventListener('touchend', handleTouchEnd, { passive: true })
  })

  onUnmounted(() => {
    if (!elementRef) return
    elementRef.removeEventListener('touchstart', handleTouchStart)
    elementRef.removeEventListener('touchmove', handleTouchMove)
    elementRef.removeEventListener('touchend', handleTouchEnd)
  })

  return { state }
}
```

### 25.2.2 滑动删除与左滑操作

移动端列表常见的"左滑删除"功能：

```vue
<!-- components/SwipeCell.vue -->
<template>
  <div
    ref="containerRef"
    class="swipe-cell"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <!-- 左侧插槽（通常放操作按钮） -->
    <div class="swipe-cell-left" :style="{ width: leftWidth + 'px' }">
      <slot name="left">
        <div class="action-btn" style="background: #1989fa" @click="handleLeftClick">
          {{ leftText }}
        </div>
      </slot>
    </div>

    <!-- 主内容 -->
    <div class="swipe-cell-content" :style="{ transform: `translateX(${offset}px)` }">
      <slot />
    </div>

    <!-- 右侧插槽（通常放删除按钮） -->
    <div class="swipe-cell-right" :style="{ width: rightWidth + 'px' }">
      <slot name="right">
        <div class="action-btn" style="background: #ee0a24" @click="handleRightClick">
          {{ rightText }}
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  leftWidth?: number   // 左侧操作区宽度
  rightWidth?: number  // 右侧操作区宽度
  leftText?: string
  rightText?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  leftWidth: 80,
  rightWidth: 80,
  leftText: '收藏',
  rightText: '删除',
  disabled: false
})

const emit = defineEmits<{
  (e: 'left-click'): void
  (e: 'right-click'): void
  (e: 'swipe', direction: 'left' | 'right'): void
}>()

const containerRef = ref<HTMLElement | null>(null)
const offset = ref(0)
const startX = ref(0)
const startY = ref(0)
const isMoving = ref(false)

const handleTouchStart = (e: TouchEvent) => {
  if (props.disabled) return

  const touch = e.touches[0]
  startX.value = touch.clientX
  startY.value = touch.clientY
  isMoving.value = false
}

const handleTouchMove = (e: TouchEvent) => {
  if (props.disabled || !isMoving.value) return

  const touch = e.touches[0]
  const deltaX = touch.clientX - startX.value
  const deltaY = touch.clientY - startY.value

  // 判断是否为水平滑动（水平位移大于垂直位移）
  if (!isMoving.value && Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 10) {
    isMoving.value = true
  }

  if (isMoving.value) {
    e.preventDefault()  // 阻止默认滚动

    // 计算偏移量，限制在操作区宽度内
    if (deltaX < 0) {
      // 向左滑，显示右侧操作区
      offset.value = Math.max(deltaX, -props.rightWidth)
    } else {
      // 向右滑，显示左侧操作区
      offset.value = Math.min(deltaX, props.leftWidth)
    }
  }
}

const handleTouchEnd = () => {
  if (!isMoving.value) {
    isMoving.value = true  // 下次可以重新触发
    return
  }

  // 根据偏移量判断是打开还是关闭
  const threshold = (props.leftWidth + props.rightWidth) / 2

  if (offset.value < -threshold / 2) {
    // 打开右侧操作区
    offset.value = -props.rightWidth
    emit('swipe', 'right')
  } else if (offset.value > threshold / 2) {
    // 打开左侧操作区
    offset.value = props.leftWidth
    emit('swipe', 'left')
  } else {
    // 关闭
    offset.value = 0
  }

  isMoving.value = true  // 重置，下次需要重新判断
}

const handleLeftClick = () => {
  offset.value = 0
  emit('left-click')
}

const handleRightClick = () => {
  offset.value = 0
  emit('right-click')
}

// 外部可以调用此方法关闭操作区
const close = () => {
  offset.value = 0
}

defineExpose({ close })
</script>

<style scoped lang="scss">
.swipe-cell {
  position: relative;
  overflow: hidden;
  display: flex;
}

.swipe-cell-content {
  flex: 1;
  transition: transform 0.2s ease-out;
  will-change: transform;
}

.swipe-cell-left,
.swipe-cell-right {
  position: absolute;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.swipe-cell-left {
  left: 0;
  transform: translateX(-100%);
}

.swipe-cell-right {
  right: 0;
  transform: translateX(100%);
}

.action-btn {
  height: 100%;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
}
</style>
```

### 25.2.3 下拉刷新与上拉加载

```typescript
// composables/usePullRefresh.ts
import { ref } from 'vue'

interface UsePullRefreshOptions {
  onRefresh: () => Promise<void>
  distance?: number  // 触发刷新的下拉距离阈值
}

export function usePullRefresh(options: UsePullRefreshOptions) {
  const { onRefresh, distance = 50 } = options

  const isPulling = ref(false)
  const pullDistance = ref(0)
  const isRefreshing = ref(false)

  const handleTouchMove = (e: TouchEvent, containerTop: number) => {
    if (isRefreshing.value || isPulling.value) return

    const touch = e.touches[0]

    // 只有在顶部才能下拉刷新
    if (containerTop >= 0) {
      // 下拉距离（限制最大值）
      pullDistance.value = Math.min(touch.clientY / 2, distance * 2)
    }
  }

  const handleTouchEnd = async () => {
    if (isRefreshing.value) return

    if (pullDistance.value >= distance) {
      // 触发刷新
      isRefreshing.value = true
      pullDistance.value = 0

      try {
        await onRefresh()
      } finally {
        isRefreshing.value = false
        pullDistance.value = 0
      }
    } else {
      pullDistance.value = 0
    }
  }

  return {
    isPulling,
    pullDistance,
    isRefreshing,
    handleTouchMove,
    handleTouchEnd
  }
}
```

```vue
<!-- components/PullRefresh.vue -->
<template>
  <div
    ref="containerRef"
    class="pull-refresh"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <!-- 下拉提示 -->
    <div class="pull-tip" :class="{ 'is-pulling': pullDistance > 0, 'is-refreshing': isRefreshing }">
      <span v-if="!isRefreshing">下拉刷新</span>
      <span v-else>刷新中...</span>
    </div>

    <!-- 内容 -->
    <div class="content">
      <slot />
    </div>

    <!-- 加载更多 -->
    <div class="load-more">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="noMore" class="no-more">没有更多了</div>
      <div v-else class="load-tip">上拉加载更多</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  onRefresh: () => Promise<void>
  onLoadMore?: () => Promise<void>
  loading?: boolean
  noMore?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  noMore: false
})

const containerRef = ref<HTMLElement | null>(null)
const isPulling = ref(false)
const pullDistance = ref(0)
const isRefreshing = ref(false)

let startY = 0

const handleTouchStart = (e: TouchEvent) => {
  startY = e.touches[0].clientY
  isPulling.value = true
}

const handleTouchMove = (e: TouchEvent) => {
  if (!isPulling.value || isRefreshing.value) return

  const deltaY = e.touches[0].clientY - startY
  // 只有下拉时才计算距离
  if (deltaY > 0) {
    pullDistance.value = Math.min(deltaY / 2, 100)
  }
}

const handleTouchEnd = async () => {
  if (!isPulling.value) return

  if (pullDistance.value >= 50 && !isRefreshing.value) {
    isRefreshing.value = true
    pullDistance.value = 0

    try {
      await props.onRefresh()
    } finally {
      isRefreshing.value = false
      pullDistance.value = 0
    }
  } else {
    pullDistance.value = 0
  }

  isPulling.value = false
}
</script>

<style scoped lang="scss">
.pull-refresh {
  min-height: 100vh;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.pull-tip {
  text-align: center;
  padding: 16px;
  font-size: 14px;
  color: #969799;
  transform: translateY(-100%);
  transition: opacity 0.2s;

  &.is-pulling {
    opacity: 1;
  }

  &.is-refreshing {
    opacity: 1;
  }
}

.content {
  min-height: calc(100vh - 100px);
}

.load-more {
  text-align: center;
  padding: 16px;
  font-size: 14px;
  color: #969799;
}
</style>
```

## 25.3 移动端性能优化

### 25.3.1 图片懒加载

移动端流量宝贵，图片懒加载是必须的。可以使用 `loading="lazy"` 属性（原生支持），也可以使用 Intersection Observer API：

```vue
<!-- components/LazyImage.vue -->
<template>
  <div class="lazy-image" :class="{ 'is-loaded': isLoaded }">
    <!-- 占位区域 -->
    <div v-if="!isLoaded" class="placeholder">
      <img v-if="placeholder" :src="placeholder" alt="" />
      <div v-else class="skeleton" />
    </div>

    <!-- 真实图片 -->
    <img
      v-if="shouldLoad"
      ref="imgRef"
      :src="src"
      :alt="alt"
      class="image"
      :class="{ 'is-visible': isLoaded }"
      @load="handleLoad"
      @error="handleError"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Props {
  src: string
  alt?: string
  placeholder?: string
  rootMargin?: string  // 提前加载的偏移量
}

const props = withDefaults(defineProps<Props>(), {
  alt: '',
  rootMargin: '50px'
})

const imgRef = ref<HTMLImageElement | null>(null)
const isLoaded = ref(false)
const shouldLoad = ref(false)

let observer: IntersectionObserver | null = null

onMounted(() => {
  // 如果浏览器不支持 IntersectionObserver，直接加载
  if (!('IntersectionObserver' in window)) {
    shouldLoad.value = true
    return
  }

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // 进入视口，加载图片
          shouldLoad.value = true
          // 加载完成后停止观察
          observer?.disconnect()
        }
      })
    },
    {
      rootMargin: props.rootMargin,  // 提前 50px 开始加载
      threshold: 0
    }
  )

  if (imgRef.value) {
    observer.observe(imgRef.value)
  }
})

onUnmounted(() => {
  observer?.disconnect()
})

const handleLoad = () => {
  isLoaded.value = true
}

const handleError = () => {
  console.error('图片加载失败:', props.src)
}
</script>

<style scoped lang="scss">
.lazy-image {
  position: relative;
  overflow: hidden;
  background: #f5f5f5;
}

.placeholder {
  width: 100%;
  height: 100%;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.skeleton {
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s;

  &.is-visible {
    opacity: 1;
  }
}
</style>
```

### 25.3.2 路由懒加载与组件懒加载

移动端首屏加载速度至关重要，懒加载能显著减少初始 bundle 体积：

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

// 直接 import 的方式（同步加载，所有路由打包到一个文件）
// import Home from '@/views/Home.vue'

// 懒加载方式（每个路由单独打包）
const Home = () => import('@/views/Home.vue')
const List = () => import('@/views/List.vue')
const Detail = () => import('@/views/Detail.vue')
const User = () => import(/* webpackChunkName: "user" */ '@/views/User.vue')

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/list', name: 'List', component: List },
  { path: '/detail/:id', name: 'Detail', component: Detail },
  // 同一个 chunk 名会打包到一起
  { path: '/user/profile', name: 'UserProfile', component: User },
  { path: '/user/settings', name: 'UserSettings', component: User }
]
```

### 25.3.3 长列表虚拟滚动

对于超长列表（比如商品列表、聊天记录），即使懒加载了图片，DOM 节点太多也会卡顿。**虚拟滚动**的思路是：只渲染当前屏幕可见的元素，随着滚动动态替换显示内容，保持 DOM 节点数量在一个可控范围内。

```vue
<!-- components/VirtualList.vue -->
<template>
  <div
    ref="containerRef"
    class="virtual-list"
    :style="{ height: containerHeight + 'px' }"
    @scroll="handleScroll"
  >
    <!-- 占位区域：撑开滚动高度 -->
    <div class="phantom" :style="{ height: totalHeight + 'px' }" />

    <!-- 实际渲染的内容 -->
    <div class="content" :style="{ transform: `translateY(${offsetY}px)` }">
      <div
        v-for="item in visibleItems"
        :key="item.index"
        class="item"
        :style="{ height: itemHeight + 'px' }"
      >
        <slot :item="item.data" :index="item.index" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface Props {
  items: any[]           // 完整数据列表
  itemHeight: number      // 每项高度（固定高度）
  containerHeight: number  // 可视区域高度
  buffer?: number        // 缓冲数量（上下各多渲染几个）
}

const props = withDefaults(defineProps<Props>(), {
  buffer: 3
})

const containerRef = ref<HTMLElement | null>(null)
const scrollTop = ref(0)

// 总高度
const totalHeight = computed(() => props.items.length * props.itemHeight)

// 计算可见区域的起始和结束索引
const visibleRange = computed(() => {
  const start = Math.floor(scrollTop.value / props.itemHeight)
  const visibleCount = Math.ceil(props.containerHeight / props.itemHeight)

  const startIndex = Math.max(0, start - props.buffer)
  const endIndex = Math.min(props.items.length - 1, start + visibleCount + props.buffer)

  return { startIndex, endIndex }
})

// 可见的列表项
const visibleItems = computed(() => {
  const { startIndex, endIndex } = visibleRange.value
  const result: Array<{ index: number; data: any }> = []

  for (let i = startIndex; i <= endIndex; i++) {
    result.push({
      index: i,
      data: props.items[i]
    })
  }

  return result
})

// translateY 的偏移量
const offsetY = computed(() => visibleRange.value.startIndex * props.itemHeight)

const handleScroll = (e: Event) => {
  scrollTop.value = (e.target as HTMLElement).scrollTop
}

// 外部可以调用此方法滚动到指定位置
const scrollToIndex = (index: number) => {
  if (containerRef.value) {
    containerRef.value.scrollTop = index * props.itemHeight
  }
}

defineExpose({ scrollToIndex })
</script>

<style scoped lang="scss">
.virtual-list {
  overflow-y: auto;
  position: relative;
}

.phantom {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  z-index: -1;
}

.content {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
}

.item {
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-bottom: 1px solid #f0f0f0;
}
</style>
```

## 25.4 PWA 支持（Manifest + Service Worker）

### 25.4.1 Web App Manifest

Manifest 是 PWA 的"安装清单"，它让浏览器知道这是一个可以"安装"到桌面的 Web 应用：

```json
// public/manifest.json
{
  "name": "Vue3 移动应用",
  "short_name": "Vue3 App",
  "description": "一个使用 Vue 3 构建的移动端应用",
  "start_url": "/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#ffffff",
  "theme_color": "#42b883",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "categories": ["shopping", "lifestyle"],
  "screenshots": [
    {
      "src": "/screenshots/home.png",
      "sizes": "1080x1920",
      "type": "image/png"
    }
  ]
}
```

在 `index.html` 中引用：

```html
<link rel="manifest" href="/manifest.json">
<!-- iOS Safari 需要额外配置 -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Vue3 App">
<link rel="apple-touch-icon" href="/icons/icon-192x192.png">
```

**display 模式说明**：
- `fullscreen`：全屏显示，完全没有浏览器 UI
- `standalone`：独立窗口显示，有状态栏但没有地址栏
- `minimal-ui`：比 standalone 更精简，只有返回按钮
- `browser`：普通浏览器模式

### 25.4.2 Service Worker 基础

Service Worker 是 PWA 的核心技术，它是一个运行在浏览器后台的脚本，可以拦截网络请求、缓存资源、推送通知、实现离线访问。

```javascript
// public/sw.js - Service Worker 文件
// 注意：SW 文件必须在 public 目录下，且不能有 import

const CACHE_NAME = 'vue3-app-v1'
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json'
]

// 安装事件：缓存静态资源
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...')
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Caching static assets')
      return cache.addAll(STATIC_ASSETS)
    })
  )
  // 跳过等待，立即激活
  self.skipWaiting()
})

// 激活事件：清理旧缓存
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...')
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      )
    })
  )
  // 立即接管所有页面
  self.clients.claim()
})

// 请求拦截：缓存优先，网络其次
self.addEventListener('fetch', (event) => {
  const { request } = event

  // 只处理同源请求和 CDN 请求
  if (!request.url.startsWith(self.location.origin) &&
      !request.url.includes('cdn.example.com')) {
    return
  }

  // 对于 API 请求，使用网络优先策略
  if (request.url.includes('/api/')) {
    event.respondWith(networkFirst(request))
    return
  }

  // 对于静态资源，使用缓存优先策略
  event.respondWith(cacheFirst(request))
})

// 缓存优先策略
async function cacheFirst(request) {
  const cached = await caches.match(request)
  if (cached) {
    return cached
  }

  try {
    const response = await fetch(request)
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME)
      cache.put(request, response.clone())
    }
    return response
  } catch (error) {
    // 网络请求失败且没有缓存，返回离线页面
    return caches.match('/offline.html')
  }
}

// 网络优先策略
async function networkFirst(request) {
  try {
    const response = await fetch(request)
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME)
      cache.put(request, response.clone())
    }
    return response
  } catch (error) {
    const cached = await caches.match(request)
    if (cached) {
      return cached
    }
    throw error
  }
}

// 推送通知
self.addEventListener('push', (event) => {
  if (!event.data) return

  const data = event.data.json()
  const options = {
    body: data.body || '您有一条新消息',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/'
    }
  }

  event.waitUntil(
    self.registration.showNotification(data.title || '新通知', options)
  )
})

// 点击通知
self.addEventListener('notificationclick', (event) => {
  event.notification.close()

  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  )
})
```

### 25.4.3 在 Vue 中注册 Service Worker

```typescript
// src/utils/registerServiceWorker.ts
import { register } from 'register-service-worker'

if (import.meta.env.PROD) {
  register(`${import.meta.env.BASE_URL}sw.js`, {
    ready(registration) {
      console.log('[SW] Service Worker 准备就绪')
      console.log('[SW] App content is now cacheable for offline use.')
    },

    registered(registration) {
      console.log('[SW] Service Worker 已注册:', registration.scope)
    },

    cached(registration) {
      console.log('[SW] Content has been cached for offline use.')
    },

    updatefound(registration) {
      console.log('[SW] New content is downloading.')
      const newWorker = registration.installing
      if (newWorker) {
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            // 检测到新版本
            console.log('[SW] New content is available; please refresh.')
            // 可以在这里触发更新提示 UI
          }
        })
      }
    },

    offline() {
      console.log('[SW] No internet connection found. App is running in offline mode.')
    },

    error(error) {
      console.error('[SW] Error during service worker registration:', error)
    }
  })
}
```

```typescript
// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import { registerSW } from 'virtual:pwa-register'

// PWA 更新提示
const updateSW = registerSW({
  onNeedRefresh() {
    // 发现新版本，询问用户是否刷新
    if (confirm('有新版本可用，是否刷新？')) {
      updateSW(true)
    }
  },
  onOfflineReady() {
    console.log('应用已准备好离线使用')
  }
})

createApp(App).mount('#app')
```

### 25.4.4 离线页面与降级策略

```vue
<!-- src/views/Offline.vue -->
<template>
  <div class="offline-page">
    <div class="content">
      <div class="icon">📡</div>
      <h2>网络走丢了~</h2>
      <p>别担心，你的页面还在这里。</p>
      <p>检查一下网络连接，稍后再试吧。</p>
      <el-button type="primary" @click="handleRetry">重试</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

const emit = defineEmits<{
  (e: 'retry'): void
}>()

const handleRetry = () => {
  emit('retry')
}

// 监听网络恢复
const handleOnline = () => {
  emit('retry')
}

onMounted(() => {
  window.addEventListener('online', handleOnline)
})

onUnmounted(() => {
  window.removeEventListener('online', handleOnline)
})
</script>

<style scoped lang="scss">
.offline-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  padding: 20px;

  .content {
    text-align: center;

    .icon {
      font-size: 64px;
      margin-bottom: 16px;
    }

    h2 {
      font-size: 20px;
      color: #333;
      margin-bottom: 8px;
    }

    p {
      font-size: 14px;
      color: #999;
      margin: 4px 0;
    }

    .el-button {
      margin-top: 24px;
    }
  }
}
</style>
```

## 25.5 本章小结

本章聚焦移动端 H5 应用开发的独特挑战，从 viewport 配置、rem/vw 适配方案讲起，介绍了移动端特有的交互方式（手势操作、下拉刷新、上拉加载），以及移动端性能优化的核心手段（图片懒加载、路由懒加载、虚拟滚动）。

PWA 是让 H5 应用拥有"原生体验"的关键技术。通过 Manifest，H5 应用可以被"安装"到桌面和主屏幕；通过 Service Worker，应用可以实现离线访问、消息推送、后台同步等功能。PWA 不是要替代原生应用，而是在某些场景下提供一种"免安装、原生体验"的轻量级选择。

**核心要点回顾**：
- viewport 配置是移动端适配的第一步，`width=device-width, initial-scale=1.0` 是基础配置
- rem 方案用 JS 动态设置 `<html>` 的 font-size，vw 方案纯 CSS 实现，各有优劣
- 移动端手势（滑动、长按等）需要用 Touch 事件手动实现或使用手势库
- 图片懒加载和路由懒加载是移动端性能优化的标配
- 虚拟滚动解决超长列表的 DOM 性能问题
- PWA = Manifest（安装能力）+ Service Worker（离线/推送能力）
- Service Worker 有生命周期（install -> activate -> fetch），理解其工作原理是掌握 PWA 的关键
