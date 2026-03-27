+++
title = "第39章 UI组件实现"
weight = 390
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十九章：UI 组件实现

> 用纯CSS实现常见UI组件，不依赖任何库！

## 39.1 按钮

### 39.1.1 五状态

按钮是网页最基础的交互元素。一个正经的按钮得学会看人脸色——什么时候能点，什么时候装死，什么时候让人按不动。

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  background: #3498db;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}
.btn:hover {
  background: #2980b9;
}
.btn:active {
  transform: scale(0.96);
  background: #2472a4;
}
.btn:focus-visible {
  outline: 3px solid #85c1e9;
  outline-offset: 2px;
}
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

## 39.2 卡片

### 39.2.1 悬浮效果

卡片悬浮时不仅要往上蹿，还得给自己加个阴影撑场面——否则谁知道你"浮"了？

```css
.card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}
```

## 39.3 模态框

### 39.3.1 遮罩层

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
```

## 39.4 导航栏

### 39.4.1 固定顶部

```css
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
}
```

## 39.5 加载动画

### 39.5.1 Spinner

```css
@keyframes spin {
  to { transform: rotate(360deg); }
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #eee;
  border-top-color: #3498db;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
```

## 39.6 Tooltip

### 39.6.1 悬停显示

Tooltip 就像老板的承诺——不hover不发，一hover就兑现。

```css
[data-tooltip] {
  position: relative;
}
[data-tooltip]:hover::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  white-space: nowrap;
  font-size: 14px;
  z-index: 1000;
}
```

---

## 🎉 CSS核心教程全部完成！

### 继续加油，CSS大师！

- MDN Web Docs
- CSS Tricks
- Flexbox Froggy
- Grid Garden

**祝你学习愉快！** 🚀

