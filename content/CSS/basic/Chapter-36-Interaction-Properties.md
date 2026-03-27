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
/* 禁止点击穿透 */
.no-click {
  pointer-events: none;
}

/* 允许点击（默认）*/
.can-click {
  pointer-events: auto;
}
```

## 36.2 user-select

### 36.2.1 文本选择控制

```css
/* 禁止选择 */
.no-select {
  user-select: none;
}

/* 允许选择 */
.can-select {
  user-select: text;
}

/* 禁止选择但可复制（通常仍可通过右键菜单复制）*/
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

```css
/* 全局启用平滑滚动 */
html {
  scroll-behavior: smooth;
}

/* 锚点跳转时平滑过渡 */
a[href^="#"] {
  scroll-behavior: smooth;
}
#target {
  scroll-margin-top: 80px; /* 距离顶部 80px 时停下 */
}
```

## 36.6 overscroll-behavior

### 36.6.1 控制滚动边界

```css
/* 防止滚动穿透（推荐）—— 拉到底部不会触发父容器滚动 */
.no-scroll-chain {
  overscroll-behavior: contain;
}

/* 禁用下拉刷新（推荐用简写）*/
.no-pull-to-refresh {
  overscroll-behavior: none contain; /* x: none, y: contain */
}
```

---

## 本章小结

交互属性提升用户体验！pointer-events 控制点击、user-select 控制选择、cursor 控制指针、resize 控制调整大小、scroll-behavior 控制滚动平滑度、overscroll-behavior 控制滚动边界。

### 下章预告

下一章我们将学习固定搭配速查！

