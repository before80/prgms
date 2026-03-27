+++
title = "第35章 CSS架构"
weight = 350
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十五章：CSS 架构与预处理器

> CSS架构让代码更易维护，预处理器让开发更高效。学会这些，你就是CSS架构师了！

## 35.1 CSS 架构模式

### 35.1.1 BEM命名规范

BEM（Block\_\_Element--Modifier）是一种三段式命名规范：Block（块）\_\_Element（元素）--Modifier（修饰符），组合起来才是完整的类名，让类名清晰易懂。

```css
/* BEM = Block__Element--Modifier */

/* Block（块）*/
.card { }

/* Element（元素）*/
.card__header { }
.card__body { }
.card__footer { }
.card__image { }
.card__title { }
.card__description { }
.card__button { }

/* Modifier（修饰符）*/
.card--featured { }
.card--disabled { }
.card__button--primary { }
.card__button--secondary { }
.card__button--disabled { }
```

```html
<div class="card card--featured">
  <div class="card__header">
    <h3 class="card__title">标题</h3>
  </div>
  <div class="card__body">
    <p class="card__description">描述内容</p>
  </div>
  <div class="card__footer">
    <button class="card__button card__button--primary">主要按钮</button>
  </div>
</div>
```

### 35.1.2 SMACSS五层架构

SMACSS把CSS分成五层，从通用到特殊。

```css
/* SMACSS五层架构 */

/* 1. Base（基础样式）*/
html, body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}

/* 2. Layout（布局样式）*/
.l-header { }
.l-sidebar { }
.l-main { }
.l-footer { }

/* 3. Module（模块样式）*/
.button { }
.card { }
.modal { }

/* 4. State（状态样式）*/
.button.is-active { }
.card.is-hidden { }
.modal.is-open { }

/* 5. Theme（主题样式）*/
.theme-dark { }
.theme-light { }
```

## 35.2 预处理器

### 35.2.1 Sass/SCSS核心功能

Sass和scss是CSS预处理器，提供变量、嵌套、Mixin等功能。

```scss
/* Sass/SCSS基本功能 */

/* 变量 */
$primary-color: #3498db;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 24px;

/* Mixin（可复用代码块）*/
@mixin flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 调用Mixin */
.container {
  @include flex-center;
}

/* 占位符 */
%button-base {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.primary-button {
  @extend %button-base;
  background: $primary-color;
}
```

## 35.3 @layer层叠规则

### 35.3.1 @layer声明

@layer可以创建命名的层，控制优先级。

```css
/* @layer基本用法 */

/* 声明层顺序 */
@layer reset, base, components, utilities;

/* 在各层中写样式 */
@layer reset {
  * { margin: 0; padding: 0; }
}

@layer base {
  body { font-size: 16px; }
}

@layer components {
  .card { background: white; }
}

@layer utilities {
  .text-center { text-align: center; }
}
```

## 35.4 可访问性

### 35.4.1 颜色对比度

文本与背景的对比度至少要4.5:1。

```css
/* 高对比度文本 */
.high-contrast-text {
  color: #333; /* 深色文字 */
  background: #fff; /* 浅色背景 */
  /* 对比度约12.6:1 ✅ */
}
```

### 35.4.2 :focus-visible

区分键盘焦点和鼠标焦点。

```css
/* :focus-visible代替:focus */
:focus-visible {
  outline: 2px solid #3498db;
  outline-offset: 2px;
}
```

---

## 本章小结

CSS架构模式让代码更易维护。

### 下章预告

下一章我们将学习交互相关属性！

