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

先纠正一个常见混淆：**Sass 才是预处理器本身，SCSS 只是它的两种语法之一**。
Sass 提供两套写法——`.sass`（靠缩进，没有大括号和分号）和 `.scss`（长得几乎和 CSS 一样，
有大括号和分号）。因为 `.scss` 更贴近原生 CSS、迁移成本低，现在几乎都用它，
所以大家说"Sass"和"SCSS"时常常混着叫。它提供变量、嵌套、Mixin、`@extend` 等功能。

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

> ⚠️ **@layer 的三条关键规则**（不知道就会莫名其妙被覆盖）：
>
> 1. **层的先后顺序由"第一次出现"决定**：上面第一行的 `@layer reset, base, components, utilities;`
>    就把顺序钉死了——**越靠后的层优先级越高**。所以 `utilities` 里的工具类能盖住 `components`。
> 2. **没写进任何层的样式，优先级最高**。也就是说，普通的（unlayered）CSS 规则会打败所有
>    分层规则，不管层里写了多少选择器。这一点最反直觉，也最容易踩。
> 3. **`!important` 会把顺序反过来**：带 `!important` 的声明里，**越靠前的层越强**，
>    而普通未分层的 `!important` 变成最弱的那个。这是规范为了"逃生舱"故意设计的。

> 💡 除了 BEM / SMACSS，还有几个常见思路值得一提：**OOCSS**（把结构和皮肤拆开）、
> **ITCSS**（按"从泛到专"分 7 层组织文件）、**Utility-first**（Tailwind 那一派，用小工具类拼装）。
> 它们没有优劣之分，选出团队能一致执行的那一种，比选"最先进"的那一种更重要。

## 35.4 可访问性

### 35.4.1 颜色对比度

WCAG 对文字对比度的要求分两档：

- **普通正文：至少 4.5:1**（AA 级）
- **大号文字：至少 3:1**（约 ≥24px，或 ≥18.66px 且加粗）
- 追求更严格的 AAA 级则是 7:1 / 4.5:1

```css
/* 高对比度文本 */
.high-contrast-text {
  color: #333; /* 深色文字 */
  background: #fff; /* 浅色背景 */
  /* 对比度约12.6:1 ✅ */
}
```

> 🧮 **对比度是怎么算的？** 先把两色的相对亮度（把 sRGB 通道归一化后做 γ 校正再加权：0.2126R + 0.7152G + 0.0722B）
> 算出来，再代入 `(L1 + 0.05) / (L2 + 0.05)`（L1 是较亮的一个）。#333 对 #fff 约为 12.6:1，确实很安全。
> 懒得手算就用浏览器 DevTools 的取色器——它会直接告诉你对比度是多少、达不达标。

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
