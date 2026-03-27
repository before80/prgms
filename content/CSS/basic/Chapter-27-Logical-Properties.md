+++
title = "第27章 逻辑属性"
weight = 270
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十七章：逻辑属性与书写模式

> 想象一下，你写了一个网页，上面的文字是从左往右读的。但突然有一天，你要把网页翻译成阿拉伯文或者希伯来文——这些文字是从右往左读的！你怎么办？从头重写所有 CSS 吗？逻辑属性就是来解决这个问题的！它让你的 CSS 不受书写方向影响，全球化网站必备技能！学会这章，你就是"跨境电商"级别的 CSS 大师！

## 27.1 逻辑属性

### 27.1.1 物理方向 vs 逻辑方向

传统的 CSS 属性如 `margin-top`、`margin-left` 是基于物理方向的——"上"、"下"、"左"、"右"永远固定不变。但当页面方向改变时（比如变成从右到左的 RTL 布局），这些属性就会出问题。

**什么是物理方向和逻辑方向？**

打个比方：物理方向就像指南针——北永远是北，南永远是南。逻辑方向就像"前面"和"后面"——如果你面朝西，你的"前面"就变成了西，但"前面"这个词本身没有变。

```css
/* 物理方向属性（传统）*/
.physical {
  margin-top: 10px;      /* 上边距，永远是上方 */
  margin-right: 20px;    /* 右边距，永远是右方 */
  margin-bottom: 15px;   /* 下边距，永远是下方 */
  margin-left: 25px;    /* 左边距，永远是左方 */
  padding-top: 10px;      /* 上内边距 */
  padding-right: 20px;    /* 右内边距 */
}

/* 逻辑方向属性（现代）*/
.logical {
  margin-block-start: 10px;   /* 块级方向开始边 */
  margin-block-end: 15px;     /* 块级方向结束边 */
  margin-inline-start: 25px; /* 行内方向开始边 */
  margin-inline-end: 20px;   /* 行内方向结束边 */
  padding-block-start: 10px;  /* 块级方向开始内边距 */
  padding-inline-start: 25px; /* 行内方向开始内边距 */
}
```

```
物理方向 vs 逻辑方向：

物理方向（传统）：
       上（top）
         ↑
         │
         │
左←────────┼────────→右（right）
         │
         │
         ↓
       下（bottom）

逻辑方向（现代）：
块级方向（block）：
         开始（block-start）
              ↑
              │
              │
行内方向（inline）←─┼──→ 行内方向
         开始（inline-start）│  结束（inline-end）
              │
              ↓
         结束（block-end）
```

### 27.1.2 逻辑边距

逻辑边距用 `margin-block-start`、`margin-inline-end` 等替代传统的 `margin-top`、`margin-right` 等。

```css
/* 传统物理边距 */
.physical-margins {
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: 30px;
  margin-right: 30px;
}

/* 现代逻辑边距 */
.logical-margins {
  /* 块级方向边距（类似上下边距）*/
  margin-block-start: 20px;    /* 上边距 */
  margin-block-end: 20px;      /* 下边距 */

  /* 行内方向边距（类似左右边距）*/
  margin-inline-start: 30px;   /* 左边距 */
  margin-inline-end: 30px;     /* 右边距 */
}

/* 或者用缩写 */
.abbr-logical {
  /* block 方向：block-start block-end */
  margin-block: 20px 0;  /* 上下20px，左右0 */

  /* inline 方向：inline-start inline-end */
  margin-inline: 0 30px;  /* 上下0，左右30px */
}
```

### 27.1.3 逻辑内边距

逻辑内边距 `padding-block`、`padding-inline` 同样替代传统的 `padding-top` 等。

```css
/* 传统物理内边距 */
.physical-padding {
  padding-top: 16px;
  padding-bottom: 16px;
  padding-left: 20px;
  padding-right: 20px;
}

/* 现代逻辑内边距 */
.logical-padding {
  /* 块级方向内边距 */
  padding-block-start: 16px;   /* 上内边距 */
  padding-block-end: 16px;     /* 下内边距 */

  /* 行内方向内边距 */
  padding-inline-start: 20px;  /* 左内边距 */
  padding-inline-end: 20px;    /* 右内边距 */
}

/* 或者用缩写 */
.abbr-padding {
  /* block 方向 */
  padding-block: 16px;  /* 上下 */

  /* inline 方向 */
  padding-inline: 20px;  /* 左右 */
}
```

### 27.1.4 逻辑定位

逻辑定位用 `inset-block-start`、`inset-inline-end` 替代传统的 `top`、`left` 等。

```css
/* 传统物理定位 */
.physical-position {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}

/* 现代逻辑定位 */
.logical-position {
  position: absolute;
  inset-block-start: 0;   /* 上 */
  inset-block-end: 0;     /* 下 */
  inset-inline-start: 0;   /* 左 */
  inset-inline-end: 0;     /* 右 */
}
```

### 27.1.5 inset 缩写

`inset` 是四个方向定位的缩写，类似 `margin` 和 `padding` 的缩写语法。

```css
/* inset 缩写语法 */

/* 四个值：top right bottom left（顺时针）*/
.inset-all {
  inset: 10px 20px 15px 25px;
  /* 等于 top: 10px; right: 20px; bottom: 15px; left: 25px; */
  /* 在 RTL 布局下，left 实际显示在物理右侧 */
}

/* 两个值：top-bottom left-right */
.inset-two {
  inset: 10px 20px;
  /* 等于 top: 10px; bottom: 10px; left: 20px; right: 20px; */
}

/* 三个值：top left-right bottom */
.inset-three {
  inset: 10px 20px 15px;
  /* 等于 top: 10px; right: 20px; bottom: 15px; left: 20px;（left 默认等于 right）*/
}
```

### 27.1.6 逻辑溢出

逻辑溢出用 `overflow-block`、`overflow-inline` 替代传统的 `overflow-y`、`overflow-x`。

```css
/* 传统物理溢出 */
.physical-overflow {
  overflow-x: hidden;  /* 水平溢出隐藏 */
  overflow-y: auto;    /* 垂直溢出滚动 */
}

/* 现代逻辑溢出 */
.logical-overflow {
  overflow-block: auto;     /* 块级方向溢出 */
  overflow-inline: hidden;   /* 行内方向溢出 */
}
```

### 27.1.7 逻辑边框（重要遗漏！）

逻辑属性家族还包括 `border-block-start`、`border-inline-start`、`border-block-end`、`border-inline-end`，以及对应的 `border-block-start-width`、`border-inline-start-color` 等细分属性。

```css
/* 传统物理边框 */
.physical-border {
  border-top: 2px solid red;
  border-left: 2px solid blue;
}

/* 现代逻辑边框 */
.logical-border {
  border-block-start: 2px solid red;   /* 块级方向开始边（类似 border-top）*/
  border-inline-start: 2px solid blue; /* 行内方向开始边（类似 border-left，LTR 下同）*/
}
```

> 💡 小技巧：逻辑边框配合 `border-radius` 的逻辑属性（`border-start-start-radius`、`border-start-end-radius` 等），可以在 RTL 页面中完美保持圆角方向，而物理边框的圆角会"跟着物理方向走"，RTL 下可能看起来很奇怪。

---

## 27.2 书写模式

### 27.2.1 writing-mode——horizontal-tb / vertical-rl / vertical-lr

`writing-mode` 决定了文字的书写方向。默认是从左到右、从上到下，但有些语言（比如中文竖排、蒙古文）有不同的书写方向。

**什么是 writing-mode？**

想象你是一本书的作者，你决定书页是竖排还是横排。`writing-mode` 就是 CSS 决定"书页排版方式"的属性。

```css
/* horizontal-tb：水平从上到下，从左到右读（默认，最常见）*/
.default-mode {
  writing-mode: horizontal-tb;
}

/* vertical-rl：垂直从右到左（日语竖排、传统中文）*/
.vertical-rl {
  writing-mode: vertical-rl;
  /* 文字从上到下，阅读方向从右到左 */
}

/* vertical-lr：垂直从左到右（蒙古文）*/
.vertical-lr {
  writing-mode: vertical-lr;
  /* 文字从上到下，阅读方向从左到右 */
}
```

```html
<!-- 水平书写模式（默认）-->
<div class="default-mode">
  <p>这是水平书写的文字，从左往右读。</p>
</div>

<!-- 垂直书写模式 -->
<div class="vertical-rl">
  <p>这是垂直书写的文字，从上往下读。</p>
  <p>垂直模式下，文字流向是垂直的。</p>
</div>
```

```
writing-mode 效果：

horizontal-tb（默认）：
┌──────────────────┐
│ 从左到右，从上到下│
│ 横向文字1         │
│ 横向文字2         │
└──────────────────┘

vertical-rl：
┌───┐
│垂 │
│直 │
│文 │
│字 │
│1  │
└───┘
 ↑
 从右往左读

vertical-lr：
┌───┐
│垂 │
│直 │
│文 │
│字 │
│1  │
└───┘
↓
 从左往右读
```

### 27.2.2 direction——ltr（从左到右）/ rtl（从右到左）

`direction` 属性配合 `writing-mode` 决定了文字的基本流向。

```css
/* direction 属性 */

/* ltr：从左到右（Left-To-Right）*/
.ltr {
  direction: ltr;
  /* 用于英文、中文等从左到右的语言 */
}

/* rtl：从右到左（Right-To-Left）*/
.rtl {
  direction: rtl;
  /* 用于阿拉伯文、希伯来文等从右到左的语言 */
}
```

**direction 和 writing-mode 的配合：**

```css
/* 阿拉伯语页面布局 */
.arabic-page {
  direction: rtl;  /* 文字从右到左 */
}

.arabic-page .logo {
  /* logo 会在右边显示 */
  text-align: right;
}

.arabic-page .menu {
  /* 菜单项会从右往左排列 */
}
```

### 27.2.3 text-orientation——mixed（横排文字横躺，默认）/ upright（所有文字正向）/ sideways（所有文字横向旋转）

`text-orientation` 决定了多语言混合文本中，不同语言的文字如何显示朝向。

```css
/* text-orientation 属性 */

/* mixed：横排文字（如英文）旋转90°横躺，垂直文字（如中文）保持正向（默认）*/
.mixed-orientation {
  text-orientation: mixed;
}

/* upright：所有文字字符都正向显示（每个字符保持自身原始朝向）*/
.upright-orientation {
  text-orientation: upright;
  /* 适合竖排混合语言文本 */
}

/* sideways：所有文字都横向显示（即所有字符统一旋转90°横躺）*/
.sideways-orientation {
  text-orientation: sideways;
  /* 竖排文字也横躺过去 */
}
```

```html
<div class="vertical-rl">
  <p class="mixed-orientation">
    英文 word 和中文混合
  </p>
  <p class="upright-orientation">
    所有文字都正向显示
  </p>
</div>
```

---

## 本章小结

### 核心知识点

| 属性 | 说明 |
|------|------|
| margin-inline-start/end | 行内方向边距 |
| margin-block-start/end | 块级方向边距 |
| padding-inline-start/end | 行内方向内边距 |
| padding-block-start/end | 块级方向内边距 |
| border-inline-start/end | 行内方向边框 |
| border-block-start/end | 块级方向边框 |
| inset-block-start/end | 块级方向定位 |
| inset-inline-start/end | 行内方向定位 |
| overflow-block | 块级方向溢出 |
| overflow-inline | 行内方向溢出 |
| writing-mode | 书写模式 |
| direction | 文字方向 |
| text-orientation | 文字朝向 |

### 逻辑属性映射表

| 物理属性 | 逻辑属性 |
|-----------|-----------|
| margin-top | margin-block-start |
| margin-bottom | margin-block-end |
| margin-left | margin-inline-start |
| margin-right | margin-inline-end |
| padding-top | padding-block-start |
| padding-bottom | padding-block-end |
| padding-left | padding-inline-start |
| padding-right | padding-inline-end |
| top | inset-block-start |
| bottom | inset-block-end |
| left | inset-inline-start |
| right | inset-inline-end |
| overflow-x | overflow-inline |
| overflow-y | overflow-block |

### 书写模式

| 值 | 说明 |
|-----|------|
| horizontal-tb | 水平从左到右（默认）|
| vertical-rl | 垂直从右到左 |
| vertical-lr | 垂直从左到右 |

### 下章预告

下一章我们将学习渐变，让网页告别单调的纯色背景！

