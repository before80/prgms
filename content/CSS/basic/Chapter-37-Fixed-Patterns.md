+++
title = "第37章 固定搭配速查"
weight = 370
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十七章：固定搭配速查

> 这些固定搭配收藏起来，编码效率翻倍！

## 37.1 文字类

### 37.1.1 单行省略

```css
.single-line {
  width: 100%;           /* 必须有明确宽度，ellipsis 才生效 */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

### 37.1.2 多行省略

```css
.multi-line {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

## 37.2 布局类

### 37.2.1 Flex居中

```css
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### 37.2.2 清除浮动

```css
/* 方案1：::after 伪元素（最常用）*/
.clearfix::after {
  content: "";
  display: block;
  clear: both;
}

/* 方案2：display: flow-root（现代简洁）*/
.parent { display: flow-root; }

/* 方案3：overflow: hidden（需注意裁剪问题）*/
.parent { overflow: hidden; }
```

## 37.3 动画类

### 37.3.1 悬浮放大

```css
.hover-scale {
  transition: transform 0.2s;
}
.hover-scale:hover {
  transform: scale(1.05);
}
```

## 37.4 表单类

### 37.4.1 accent-color

```css
input[type="checkbox"] {
  accent-color: #3498db;
}
```

---

## 本章小结

收藏备用！

### 下章预告

下一章常见问题与坑！

