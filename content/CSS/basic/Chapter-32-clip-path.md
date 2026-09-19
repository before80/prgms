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

`circle()` 只能裁出**正圆**（想要椭圆请用下一节的 `ellipse()`，它俩可不是一回事）。

```css
/* circle() 裁剪的基本用法 */

/* 圆形裁剪 */
.circle {
  clip-path: circle(50%);
  /* 百分比半径的基准是 sqrt(宽² + 高²) / √2（不是宽或高本身）；
     对正方形元素来说，50% 刚好就是它的内切圆。 */
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
  clip-path: circle(20% at 30% 70%);
}
```

> ⚠️ **形状函数之间不能随便"变形"！** 上面例子两端用的都是 `circle()`，只是半径和圆心不同，
> 所以能平滑过渡。如果你把 `:hover` 那头换成 `polygon(...)`（比如前面的菱形），
> 因为**不同形状函数之间无法插值**，浏览器会直接"啪"地跳过去，而不是动画——这是 clip-path
> 动画最常见的失望来源。
>
> 想做出"形状变形"的效果，记住两条路：
> 1. 两头用**同一种函数**：`circle()` → `circle()`，或者最经典的 **polygon() → polygon()**，
>    而且**顶点数量必须一致**（4 个点只能变 4 个点，多一个少一个都会退化成跳变）。
> 2. 顶点不够就"凑数"：把多出来的顶点放在同一个位置（例如重复写 `50% 50%`），
>    让两边顶点数相同即可。

```css
/* 真正的"多边形变形"：顶点数一致，才能平滑过渡 */
.blob {
  clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
  transition: clip-path 0.6s ease;
}

.blob:hover {
  clip-path: polygon(50% 10%, 90% 50%, 70% 100%, 30% 100%, 10% 50%);
}
```

> 📌 **补充几个小知识：**
> - `clip-path` 会把**指针事件一起裁掉**：被剪掉的区域点不到，这常常是"按钮点不着"的原因。
> - 除了四个基本形状，还有 `path('M...')`（直接写 SVG 路径）和 `url(#id)`（引用 SVG `<clipPath>`）。
> - 所有百分比都相对于**参考框（reference box）**计算，默认是 `border-box`，
>   可以用 `clip-path: circle(50% at 50% 50%) padding-box` 这样的写法换框。

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
