+++
title = "第12章 颜色与背景属性"
weight = 120
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十二章：颜色与背景属性

> 颜色是网页的灵魂，背景是页面的外衣。学会控制颜色和背景，你的网页就能从"黑白电视"升级到"彩色电视"。

## 12.1 color 颜色

### 12.1.1 设置文字颜色

```css
.text-red { color: red; }
.text-blue { color: #3498db; }
.text-rgb { color: rgb(52, 152, 219); }
.text-hsl { color: hsl(204, 70%, 53%); }
```

### 12.1.2 currentColor——关键字，继承 color 属性值

```css
/* currentColor 继承元素的 color 属性 */
.icon {
  color: #3498db;
  fill: currentColor;  /* SVG 填充色继承 color */
}
```

---

## 12.2 background-color 背景色

### 12.2.1 默认值是 transparent（透明），不是白色

> 🔍 **新手陷阱：** 很多同学以为元素背景默认是白色，兴冲冲地写了个半透明效果，结果底下透出的不是期待的内容——而是隔壁 div 的背景色。罪魁祸首就是 `background-color` 的默认值其实是 `transparent`，而不是 `white`。所以记得：没有样式表加持，背景就是透明的空气。

```css
/* 背景默认是透明的 */
.transparent {
  background-color: transparent;
}

/* 设置背景色 */
.colored {
  background-color: #f5f5f5;
}
```

---

## 12.3 background-image 背景图片

### 12.3.1 基本用法——background-image: url("图片路径")

```css
.hero {
  background-image: url("hero-bg.jpg");
  background-size: cover;
  background-position: center;
}
```

### 12.3.2 多重背景——background-image: url("图1.png"), url("图2.png")

```css
.multi-bg {
  background-image: url("图1.png"), url("图2.png");
  /* 前面的在更上层 */
}
```

### 12.3.3 渐变背景——linear-gradient() 或直接写在 background 属性里

```css
.gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

---

## 12.4 background-repeat 平铺

### 12.4.1 repeat（默认）、no-repeat、repeat-x、repeat-y

```css
.no-repeat {
  background-repeat: no-repeat;
}

.repeat-x {
  background-repeat: repeat-x;
}

.repeat-y {
  background-repeat: repeat-y;
}
```

---

## 12.5 background-position 位置

### 12.5.1 关键字——left/center/right 和 top/center/bottom 组合

```css
.center-center {
  background-position: center center;
}

.left-bottom {
  background-position: left bottom;
}
```

### 12.5.2 数值——20px 30px（水平偏移 20px，垂直偏移 30px）

```css
.offset {
  background-position: 20px 30px;
}
```

### 12.5.3 百分比——50% 50% 表示居中

```css
.percent-position {
  background-position: 50% 50%;
}
```

---

## 12.6 background-size 尺寸

### 12.6.1 cover——图片等比缩放，完全覆盖容器

```css
.cover {
  background-size: cover;
  /* 可能裁剪部分图片 */
}
```

### 12.6.2 contain——图片等比缩放，完整装入容器

```css
.contain {
  background-size: contain;
  /* 可能有空白区域 */
}
```

### 12.6.3 具体数值——400px 300px 或 50% 100%

```css
.exact-size {
  background-size: 400px 300px;
}

.percent-size {
  background-size: 50% 100%;
}
```

---

## 12.7 background-attachment

### 12.7.1 scroll（默认）——背景随元素滚动

```css
.scroll {
  background-attachment: scroll;
}
```

### 12.7.2 fixed——背景固定在视口，页面滚动时背景不动

```css
.fixed {
  background-attachment: fixed;
  /* 背景钉在视口上，不随页面滚动 ✨ */
}
```

> ⚠️ **历史小知识：** 早年 `fixed` 背景确实能轻松实现"经典视差"效果，但现代浏览器（尤其是移动端 WebKit/blink）对 `fixed` 背景的限制越来越多，曾经的视差黑科技已成玄学。如果你在手机上发现 `fixed` 背景"不动了"，恭喜你——你遇到了浏览器的爱与恨。真想好好做视差？建议用 `transform: translate3d()` 或专门的视差库。

### 12.7.3 local——背景随元素内容滚动

```css
.local {
  background-attachment: local;
}
```

---

## 12.8 background-origin 与 background-clip

### 12.8.1 background-origin——背景起始区域（从哪儿开始画）

```css
/* padding-box（默认）: 从 padding 区开始画 */
.origin-padding {
  background-origin: padding-box;
}

/* border-box: 从 border 区开始画，背景可以延伸到边框下方 */
.origin-border {
  background-origin: border-box;
}

/* content-box: 从 content 区开始画 */
.origin-content {
  background-origin: content-box;
}
```

### 12.8.2 background-clip——背景裁剪区域（画完从哪里"剪掉"）

```css
/* border-box（默认）: 背景延伸至边框外缘 */
.clip-border {
  background-clip: border-box;
}

/* padding-box: 裁掉边框区域的背景 */
.clip-padding {
  background-clip: padding-box;
}

/* text: 背景只保留在文字下方（超酷炫的文字填充效果！）*/
.clip-text {
  background-clip: text;
  color: transparent;              /* 文字要透明才能看见背景 */
  background: linear-gradient(90deg, #667eea, #764ba2);
}
```

> 💡 **两者的区别：** `background-origin` 决定"从哪开始画"，`background-clip` 决定"画完从哪里切掉"。想象你在墙上贴海报——`origin` 是你站的位置（从门边还是墙角开始贴），`clip` 是你用剪刀裁掉哪一块。

---

## 12.9 background-blend-mode 混合模式

### 12.9.1 背景图片与背景色/多层图片之间的混合

```css
.blend {
  background-image: url("texture.png");
  background-color: #3498db;
  background-blend-mode: multiply;   /* multiply、screen、overlay、soft-light... */
}
```

### 12.9.2 多重背景各自独立混合

```css
.multi-blend {
  background-image: url("overlay.png"), url("base.jpg");
  background-color: #764ba2;
  background-blend-mode: screen, normal; /* 每层可以不同模式 */
}
```

> 🎨 常见的混合模式：`normal`（默认）、`multiply`（正片叠底，参考 Photoshop 图层混合）、`screen`（屏幕）、`overlay`（叠加）、`darken`（变暗）、`lighten`（变亮）、`color-dodge`（颜色减淡）……总有一款适合你的设计。

---

## 12.10 background 缩写

### 12.10.1 顺序——background: color image repeat attachment position/size

```css
/* 完整写法 */
.hero {
  background:
    #3498db                    /* 颜色 */
    url("hero.jpg")             /* 图片 */
    no-repeat                  /* 平铺方式 */
    center                     /* 位置 */
    / cover;                   /* 尺寸 */
}
```

---

## 本章小结

恭喜你完成了第十二章的学习！

### 核心知识点

| 属性 | 说明 |
|------|------|
| color | 文字颜色 |
| currentColor | 继承 color 属性值的关键字 |
| background-color | 背景色（默认 transparent） |
| background-image | 背景图片（支持多重背景） |
| background-repeat | 平铺方式 |
| background-position | 位置 |
| background-size | 尺寸（cover/contain） |
| background-attachment | 滚动方式（scroll/fixed/local） |
| background-origin | 背景绘制起始区域 |
| background-clip | 背景裁剪区域 |
| background-blend-mode | 背景混合模式 |
| background | 缩写属性 |

### 下章预告

下一章我们将学习边框属性，让你的网页元素更有轮廓感！


