+++
title = "第11章 文本与字体属性"
weight = 110
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十一章：文字与字体属性

> 文字是网页的灵魂，字体是文字的外衣。学会控制文字和字体，你的网页就不再是"千篇一律的系统默认字体"，而是独具特色的品牌视觉。

## 11.1 font-family 字体

### 11.1.1 字体栈——"Arial", "Helvetica", sans-serif，浏览器从左到右依次查找，找到可用字体就停止

```css
/* 字体栈：浏览器会依次尝试每个字体，直到找到可用的 */
body {
  font-family: "Arial", "Helvetica", sans-serif;
}

/* 常见字体栈 */
font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
font-family: "Georgia", "Times New Roman", serif;
```

### 11.1.2 中文字体——"Microsoft YaHei"（微软雅黑）、"PingFang SC"（苹方）、"SimSun"（宋体）

```css
/* 中文网页常用字体栈 */
body {
  font-family: "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", "Heiti SC", sans-serif;
}
```

---

## 11.2 font-size 字号

### 11.2.1 px——绝对单位，不会随页面缩放改变

```css
/* 像素是最常用的绝对单位 */
.text {
  font-size: 16px;
}

h1 {
  font-size: 32px;
}
```

### 11.2.2 em——相对于父元素的字体大小，嵌套时容易失控

```css
.parent {
  font-size: 20px;
}

.child {
  font-size: 1.5em;  /* 20px * 1.5 = 30px */
}
```

### 11.2.3 rem——相对于根元素（html）的字体大小，推荐用于响应式

```css
html {
  font-size: 16px;
}

.text {
  font-size: 1rem;  /* 16px */
}

.title {
  font-size: 2rem;  /* 32px */
}
```

### 11.2.4 clamp()——clamp(16px, 2vw, 24px) 实现流体字体，文字在最小值和最大值之间随视口平滑缩放

```css
/* 流体字体：最小 16px，最大 24px，中间随视口平滑缩放 */
.fluid-text {
  font-size: clamp(16px, 2vw, 24px);
}
```

### 11.2.5 ch——0 的宽度，用于等宽字体排版

```css
/* 用于输入框最小宽度设置 */
.username-input {
  min-width: 20ch;
}
```

---

## 11.3 font-weight 字重

### 11.3.1 关键字——normal（等于 400）、bold（等于 700）

```css
.text-normal {
  font-weight: normal;  /* 等于 400 */
}

.text-bold {
  font-weight: bold;      /* 等于 700 */
}
```

### 11.3.2 数值——100、200、300、400、500、600、700、800、900

```css
.font-thin { font-weight: 100; }
.font-extralight { font-weight: 200; }
.font-light { font-weight: 300; }
.font-normal { font-weight: 400; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }
.font-extrabold { font-weight: 800; }
.font-black { font-weight: 900; }
```

---

## 11.4 font-style 和 font-variant

### 11.4.1 font-style——normal、italic（斜体）、oblique（倾斜）

```css
.normal { font-style: normal; }
.italic { font-style: italic; }    /* 斜体，使用专门的斜体字形 */
.oblique { font-style: oblique; }  /* 倾斜，强制倾斜文字 */
```

### 11.4.2 font-variant——small-caps（小型大写字母）、normal

```css
.small-caps { font-variant: small-caps; }  /* 小型大写字母 */
.normal { font-variant: normal; }
```

### 11.4.3 font-synthesis——none（禁止浏览器合成粗体/斜体）、weight（允许合成粗体）、style（允许合成斜体）

```css
/* 禁止浏览器合成字体样式 */
.no-synthesis {
  font-synthesis: none;
}
```

---

## 11.5 font-optical-sizing 光学尺寸

### 11.5.1 auto（自动调整）/ none，应用于字体较粗细的视觉优化

```css
.auto-sizing {
  font-optical-sizing: auto;  /* 默认值，自动优化 */
}

.no-optical-sizing {
  font-optical-sizing: none;
}
```

---

## 11.6 font-feature-settings OpenType 特性

### 11.6.1 控制连字、字距等高级 OpenType 特性

```css
/* 连字（liga）、字距调整（kern）等 */
.text-with-features {
  font-feature-settings: "liga" 1, "kern" 1, "swsh" 1;
}
```

---

## 11.7 font-variant-alternates 替代字形

### 11.7.1 在 @font-feature-values 中定义字形集后使用

```css
@font-feature-values "MyFont" {
  @swash { swash-variant: 1; }
}

.flowers {
  font-variant-alternates: swash(swash-variant);  /* 使用上面定义的字形变体 */
}
```

---

## 11.8 -webkit-text-size-adjust 移动端字号

### 11.8.1 -webkit-text-size-adjust: none——防止 iOS Safari 自动调整字号

```css
/* 移动端防止自动调整字号 */
.no-auto-adjust {
  -webkit-text-size-adjust: none;
}
```

### 11.8.2 auto——允许浏览器调整字号（默认）

```css
.auto-adjust {
  -webkit-text-size-adjust: auto;  /* 默认值 */
}
```

---

## 11.9 line-height 行高

### 11.9.1 无单位写法——line-height: 1.5，推荐写法

```css
/* 推荐：无单位写法，行高是字号的倍数 */
.text {
  line-height: 1.5;  /* 推荐！ */
}
```

### 11.9.2 有单位写法——line-height: 20px 或 line-height: 150%

```css
/* 有单位写法 */
.px-height {
  line-height: 20px;
}

.percent-height {
  line-height: 150%;
}
```

### 11.9.3 单行垂直居中——设置 line-height 等于容器高度

```css
/* 单行文字垂直居中 */
.centered-text {
  height: 60px;
  line-height: 60px;
}
```

---

## 11.10 text-align 文本对齐

### 11.10.1 left（默认）、center、right、justify（两端对齐）

```css
.left { text-align: left; }
.center { text-align: center; }
.right { text-align: right; }
.justify { text-align: justify; }  /* 两端对齐，英文常用 */
```

---

## 11.11 vertical-align 垂直对齐

### 11.11.1 只对行内元素和表格单元格有效

```css
/* vertical-align 只对行内元素有效 */
.inline-element {
  vertical-align: middle;
}
```

### 11.11.2 常用值——baseline、middle、top、bottom

```css
.baseline { vertical-align: baseline; }
.middle { vertical-align: middle; }
.top { vertical-align: top; }
.bottom { vertical-align: bottom; }
```

### 11.11.3 图片底部有空隙——设 vertical-align: middle 或 bottom 解决

```css
/* 图片底部空隙问题解决 */
img {
  vertical-align: bottom;
}
```

---

## 11.12 text-decoration 文本装饰

### 11.12.1 text-decoration-line——underline（下划线）、line-through（删除线）、overline（上划线）

```css
.underline { text-decoration-line: underline; }
.line-through { text-decoration-line: line-through; }
.overline { text-decoration-line: overline; }
```

### 11.12.2 text-decoration-color——装饰线颜色

```css
.colored-line {
  text-decoration-line: underline;
  text-decoration-color: red;
}
```

### 11.12.3 text-decoration-style——solid、dashed、dotted、wavy

```css
.solid { text-decoration-style: solid; }
.dashed { text-decoration-style: dashed; }
.dotted { text-decoration-style: dotted; }
.wavy { text-decoration-style: wavy; }
```

### 11.12.4 缩写——text-decoration: underline wavy red;

```css
/* 缩写写法 */
.decorated {
  text-decoration: underline wavy red;
}
```

---

## 11.13 text-transform 文本转换

### 11.13.1 uppercase（全大写）、lowercase（全小写）、capitalize（首字母大写）

```css
.uppercase { text-transform: uppercase; }    /* 全大写 */
.lowercase { text-transform: lowercase; }    /* 全小写 */
.capitalize { text-transform: capitalize; }  /* 首字母大写 */
```

---

## 11.14 文字溢出处理

### 11.14.1 单行省略——overflow:hidden + text-overflow:ellipsis + white-space:nowrap

```css
.single-line-ellipsis {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
```

### 11.14.2 多行省略——display:-webkit-box + -webkit-line-clamp

```css
.multi-line-ellipsis {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

---

## 11.15 white-space 空白处理

### 11.15.1 normal——多个空格合并为一个（默认）

```css
.normal-whitespace {
  white-space: normal;
}
```

### 11.15.2 nowrap——不换行，所有空白合并

```css
.nowrap {
  white-space: nowrap;
}
```

### 11.15.3 pre——保留原始格式，像 pre 标签一样

```css
.pre-format {
  white-space: pre;
}
```

---

## 11.16 其他文字属性

### 11.16.1 text-indent——首行缩进

```css
.indent {
  text-indent: 2em;  /* 首行缩进，2em = 2 × 当前元素字号 */
}
```

### 11.16.2 letter-spacing——字符间距

```css
.spaced {
  letter-spacing: 2px;
}
```

### 11.16.3 word-spacing——单词间距

```css
.word-spaced {
  word-spacing: 5px;
}
```

### 11.16.4 overflow-wrap / word-wrap——长单词换行

```css
/* 防止长单词/URL撑破容器 */
.break-word {
  overflow-wrap: break-word;  /* 标准属性，推荐 */
  word-wrap: break-word;     /* 兼容旧版浏览器 */
}
```

---

## 11.17 text-shadow 文字阴影

### 11.17.1 常用写法——text-shadow: 水平偏移 垂直偏移 模糊半径 颜色

```css
/* 常用文字阴影 */
.shadow {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

/* 多层阴影 */
.multi-shadow {
  text-shadow: 1px 1px 0 #fff, 2px 2px 4px rgba(0, 0, 0, 0.3);
}

/* 发光效果 */
.glow {
  text-shadow: 0 0 10px #ff6600, 0 0 20px #ff6600;
}
```

---

## 11.18 color-adjust（打印样式）

### 11.18.1 color-adjust: economy——允许浏览器降低打印质量以节省墨水；color-adjust: exact——强制保留颜色

```css
@media print {
  .save-ink {
    color-adjust: economy;  /* 标准属性，允许降质省墨 */
    -webkit-print-color-adjust: economy;  /* 兼容 Safari */
  }

  .keep-color {
    color-adjust: exact;  /* 标准属性，强制保留颜色 */
    -webkit-print-color-adjust: exact;  /* 兼容 Safari */
  }
}
```

---

## 11.19 @font-face 自定义字体

### 11.19.1 基本语法——src: url("字体路径.woff2") format("woff2")

```css
@font-face {
  font-family: "MyFont";
  src: url("fonts/MyFont.woff2") format("woff2");
}

.custom-font {
  font-family: "MyFont", sans-serif;
}
```

### 11.19.2 font-display——swap、block、optional

```css
@font-face {
  font-family: "MyFont";
  src: url("fonts/MyFont.woff2") format("woff2");
  font-display: swap;  /* 先显示后备字体后切换 */
}
```

---

## 本章小结

恭喜你完成了第十一章的学习！文字与字体属性是网页设计的基础。

### 核心知识点

| 属性 | 说明 |
|------|------|
| font-family | 字体栈 |
| font-size | 字号（px、em、rem、clamp） |
| font-weight | 字重（100-900） |
| line-height | 行高（推荐无单位） |
| text-align | 文本对齐 |
| vertical-align | 垂直对齐（仅行内） |
| text-decoration | 文本装饰 |
| text-shadow | 文字阴影 |
| white-space | 空白处理 |
| overflow-wrap | 长单词换行 |

### 下章预告

下一章我们将学习颜色与背景属性，让你的网页更加丰富多彩！

