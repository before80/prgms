+++
title = "第32章 clip-path裁剪"
weight = 320
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十二章：clip-path 裁剪

> clip-path就是CSS给你的"裁纸刀"，可以裁剪出任意形状！菱形、圆形、六边形...只有你想不到，没有它裁不到！

## 32.1 基础形状函数

### 32.1.1 inset()——矩形裁剪

`inset()` 可以裁剪出一个矩形区域。值分别是上右下左四个方向的裁剪量。

```css
/* inset() 裁剪的基本用法 */

/* 四个值：上、右、下、左 */
.inset-all {
  clip-path: inset(10px 20px 30px 40px);
  /* 上边裁剪10px，右边20px，下边30px，左边40px。 */
}

/* 两个值：上下、左右 */
.inset-two {
  clip-path: inset(20px 30px);
  /* 上下各裁剪20px，左右各裁剪30px。 */
}

/* 一个值：四边相同 */
.inset-one {
  clip-path: inset(20px);
  /* 四边各裁剪20px。 */
}
```

```html
<div class="inset-demo" style="width: 200px; height: 150px;">
  <div class="inset-all" style="background: #3498db; padding: 40px; color: white;">
    inset(10px 20px 30px 40px) 裁剪效果
  </div>
</div>
```

**带圆角的 inset 裁剪：**

```css
/* inset 带圆角 */
.inset-round {
  clip-path: inset(10px round 20px);
  /* 裁剪后四个角都变成20px圆角。 */
}

.inset-diff-rounds {
  clip-path: inset(10px round 10px 20px 30px 40px);
  /* 分别是左上、右上、右下、左下的圆角半径。 */
}
```

### 32.1.2 circle()——圆形裁剪

`circle()` 裁剪出圆形或椭圆形区域。

```css
/* circle() 裁剪的基本用法 */

/* 圆形裁剪 */
.circle {
  clip-path: circle(50%);
  /* 50%是相对于元素尺寸的圆形半径。 */
}

/* 指定半径的圆形 */
.circle-small {
  clip-path: circle(30%);
  /* 30%半径的圆。 */
}

/* 指定圆心位置 */
.circle-at {
  clip-path: circle(40% at 30% 70%);
  /* 40%半径，圆心在元素内30% 70%的位置。 */
}
```

```html
<img class="circle" src="photo.jpg" alt="圆形裁剪" style="width: 200px; height: 200px; object-fit: cover;">
<img class="circle-at" src="photo.jpg" alt="偏心圆形" style="width: 200px; height: 200px; object-fit: cover;">
```

### 32.1.3 ellipse()——椭圆形裁剪

`ellipse()` 裁剪出椭圆形区域。

```css
/* ellipse() 裁剪的基本用法 */

/* 椭圆形裁剪 */
.ellipse {
  clip-path: ellipse(50% 30%);
  /* 50%是x轴半径，30%是y轴半径。 */
}

/* 指定圆心的椭圆 */
.ellipse-at {
  clip-path: ellipse(40% 50% at 50% 50%);
  /* 圆心在中心的椭圆。 */
}
```

### 32.1.4 polygon()——多边形裁剪

`polygon()` 是最灵活的裁剪函数，用坐标对定义多边形的顶点。

```css
/* polygon() 裁剪的基本用法 */

/* 菱形 */
.diamond {
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
  /* 四个顶点：顶部中心、右边中心、底部中心、左边中心。 */
}

/* 三角形 */
.triangle {
  clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
  /* 三个顶点构成三角形。 */
}

/* 六边形 */
.hexagon {
  clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
}
```

```html
<img class="diamond" src="photo.jpg" alt="菱形" style="width: 200px; height: 200px; object-fit: cover;">
<img class="hexagon" src="photo.jpg" alt="六边形" style="width: 200px; height: 200px; object-fit: cover;">
```

## 32.2 常用场景

### 32.2.1 菱形图片

```css
/* 菱形图片裁剪 */
.diamond-img {
  width: 300px;
  height: 300px;
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
  transition: clip-path 0.3s;
}

.diamond-img:hover {
  clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%);
  /* hover时变成梯形，优雅地"倒下" */
}
```

### 32.2.2 斜切卡片

```css
/* 斜切卡片效果 */
.beveled-card {
  clip-path: polygon(
    0% 0%,           /* 左上顶点 */
    100% 0%,         /* 右上顶点 */
    100% calc(100% - 20px),  /* 右侧切角起点 */
    calc(100% - 20px) 100%,  /* 右下切角终点 */
    0% 100%              /* 左下顶点 */
  );
  background: #3498db;
  padding: 24px;
  transition: clip-path 0.3s;
}

.beveled-card:hover {
  clip-path: polygon(
    0% 0%,
    100% 0%,
    100% 100%,
    0% 100%
  );
}
```

## 32.3 动画效果

### 32.3.1 clip-path过渡动画

```css
/* clip-path 过渡动画 */
.morphing {
  clip-path: circle(50%);
  transition: clip-path 0.5s ease;
}

.morphing:hover {
  clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
}
```

---

## 本章小结

clip-path是CSS的裁纸刀，支持inset、circle、ellipse、polygon四种基本形状函数。

### 核心函数

| 函数 | 说明 |
|------|------|
| inset() | 矩形裁剪 |
| circle() | 圆形裁剪 |
| ellipse() | 椭圆形裁剪 |
| polygon() | 多边形裁剪 |

### 下章预告

下一章我们将学习层叠与继承！

