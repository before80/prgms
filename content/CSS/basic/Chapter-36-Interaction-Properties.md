+++
title = "第36章 交互属性"
weight = 360
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十六章：交互与用户相关属性

> 网页不只是看的，更要"玩"的！学会CSS交互属性，让用户爱上你的网页！

## 36.1 pointer-events

### 36.1.1 pointer-events属性

`pointer-events` 控制元素是否响应鼠标事件。

```css
/* 元素本身不响应鼠标事件：hover、click 会"穿透"到它下方的元素 */
.no-click {
  pointer-events: none;
}

/* 恢复正常响应（默认值） */
.can-click {
  pointer-events: auto;
}
```

> 💡 **常见用途**：给覆盖在按钮上的装饰层（图形、水印）设置 `pointer-events: none`，这样用户点到装饰层时，事件会落到下面的按钮上，不会"点空"。反过来，如果想用一个透明遮罩挡住下面的所有交互（比如弹窗背景），保持默认的 `auto` 即可。

## 36.2 user-select

### 36.2.1 文本选择控制

`user-select` 决定用户能不能用鼠标拖选这段文字。注意它只影响"选中"这一个动作，并不等于禁止复制——用户仍可能通过右键菜单或开发者工具拿到文本。

```css
/* 禁止选择 */
.no-select {
  user-select: none;
}

/* 允许选择 */
.can-select {
  user-select: text;
}

/* 禁止选择（Safari 需要 -webkit- 前缀） */
.no-select-but-copy {
  user-select: none;
  -webkit-user-select: none; /* Safari */
}

/* 更精确的做法：父级禁止，指定子元素可选择 */
.protected-text {
  user-select: none;
}
.protected-text .copyable {
  user-select: text; /* 内部可复制 */
}
```

## 36.3 cursor

### 36.3.1 常用光标样式

`cursor` 用来改变鼠标悬停在元素上时的指针形状，是最直接的"可交互"暗示。

```css
.pointer { cursor: pointer; }
.move { cursor: move; }
.grab { cursor: grab; }
.grabbing { cursor: grabbing; }
.wait { cursor: wait; }
.not-allowed { cursor: not-allowed; }
```

## 36.4 resize

### 36.4.1 调整元素大小

`resize` 让用户可以用鼠标拖拽元素右下角来改变它的尺寸，常用于 `<textarea>`。它**必须配合 `overflow` 不为 `visible`** 才生效。

```css
/* 可拖动调整大小 */
.resizable {
  resize: both;
  overflow: auto; /* 必须配合overflow使用 */
}

/* 只可水平调整 */
.resizable-h {
  resize: horizontal;
  overflow: auto;
}

/* 只可垂直调整 */
.resizable-v {
  resize: vertical;
  overflow: auto;
}
```

## 36.5 scroll-behavior

### 36.5.1 平滑滚动

`scroll-behavior: smooth` 让滚动（包括点击锚点跳转）走"动画"而不是瞬间跳过去。

```css
/* 全局启用平滑滚动 */
html {
  scroll-behavior: smooth;
}

/* 注意：scroll-behavior 要设置在"产生滚动的那个盒子"上。
   写在 <a> 上是没用的（锚点本身不滚动），要写就写在 html 或具体的滚动容器上： */
.scroll-container {
  scroll-behavior: smooth;
}

/* 配合 scroll-margin，让跳转目标不要贴着容器顶部 */
#target {
  scroll-margin-top: 80px; /* 顶部留出 80px 再停下 */
}
```

## 36.6 overscroll-behavior

### 36.6.1 控制滚动边界

`overscroll-behavior` 用来控制"滚到头之后会发生什么"——比如是否连带滚动父容器、是否触发下拉刷新。

```css
/* 阻止滚动链：拉到底部不会连带滚动父容器 */
.no-scroll-chain {
  overscroll-behavior: contain;
}

/* 也可以按 x / y 分别设置，简写顺序是 <x> <y> */
.no-pull-to-refresh {
  overscroll-behavior: none contain; /* x: none, y: contain */
}
```

---

## 本章小结

交互属性提升用户体验！pointer-events 控制点击、user-select 控制选择、cursor 控制指针、resize 控制调整大小、scroll-behavior 控制滚动平滑度、overscroll-behavior 控制滚动边界。

### 下章预告

下一章我们将学习固定搭配速查！
