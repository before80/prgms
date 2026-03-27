+++
title = "第29章 CSS变换"
weight = 290
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十九章：CSS 变换 transform

> 想象一下，你是一个魔法师，可以让元素变大、缩小、旋转、倾斜——transform 就是 CSS 给你的魔法棒！学会了 transform，你的网页就能做出各种炫酷效果，让用户目不转睛！

## 29.1 二维变换函数

### 29.1.1 translate(x, y)——平移元素

`translate()` 就像是一个"瞬移术"，可以让元素从当前位置"瞬移"到新位置，但它不是消失再出现，而是平滑地移动过去。

**什么是 translate？**

想象你站在房间中央，`translate(50px, 100px)` 就像是你被瞬移了——向右移动50px，向下移动100px，但你的"存在感"（占位）还在原来的地方，没人知道你偷偷跑了。

```css
/* translate 的基本用法 */

/* 单值：水平移动 */
.translate-x {
  transform: translate(50px);
  /* 向右移动50px */
}

/* 两值：水平+垂直 */
.translate-xy {
  transform: translate(50px, 100px);
  /* 向右移动50px，向下移动100px */
}

/* 负值：反方向移动 */
.translate-negative {
  transform: translate(-30px, -50px);
  /* 向左移动30px，向上移动50px */
}
```

```html
<div class="translate-demo">
  <div class="box">原位置</div>
  <div class="box translate-x">右移50px</div>
  <div class="box translate-xy">右移50px下移100px</div>
</div>
```

```css
.translate-demo {
  display: flex;
  gap: 20px;
  padding: 20px;
}

.box {
  width: 100px;
  height: 100px;
  background: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.translate-x {
  transform: translate(50px);
}

.translate-xy {
  transform: translate(50px, 100px);
}
```

### 29.1.2 rotate(deg)——旋转元素

`rotate()` 就像是一个"原地转圈陀螺"，可以让元素绕着自己的中心点（默认）或你指定的原点疯狂旋转。

**什么是 rotate？**

想象你面前有一个转盘，`rotate(45deg)` 就像是你把转盘转了45度。

```css
/* rotate 的基本用法 */

/* 正值：顺时针旋转 */
.rotate-cw {
  transform: rotate(45deg);
  /* 顺时针旋转45度 */
}

/* 负值：逆时针旋转 */
.rotate-ccw {
  transform: rotate(-45deg);
  /* 逆时针旋转45度 */
}

/* 360度：转一圈 */
.rotate-full {
  transform: rotate(360deg);
  /* 转一整圈，回到原位 */
}
```

### 29.1.3 scale(x, y)——缩放元素

`scale()` 就像是一个"伸缩自如侠"，可以让元素变大或变小——1.5倍就是放大50%，0.5倍就是缩小一半，随你所欲！

**什么是 scale？**

想象你面前有一个东西，`scale(1.5)` 就像是用1.5倍放大镜看它——变大了50%。

```css
/* scale 的基本用法 */

/* 单值：宽高同比例缩放 */
.scale-same {
  transform: scale(1.5);
  /* 放大1.5倍 */
}

/* 两值：分别控制宽高 */
.scale-xy {
  transform: scale(1.5, 0.8);
  /* 宽放大1.5倍，高缩小到0.8倍 */
}

/* 负值：翻转（镜像）效果 */
.scale-flip {
  transform: scale(-1, 1);
  /* 水平镜像翻转（就像照镜子，左边跑到右边去了）*/
  /* 如果是 scale(-1, -1)，那就是中心点对称翻转 */
}
```

### 29.1.4 skew(x, y)——倾斜元素

`skew()` 就像是一个"拉扁侠"，可以让元素被"扯歪"——上下或左右地被一股神秘力量推斜。

**什么是 skew？**

想象你面前有一张照片，你用手从左边推了一下（别问为什么，你有超能力），`skewX(20deg)` 就像是你把它硬生生扯歪了20度。要是从右边推，那就是负的20度——方向全由你掌控！

```css
/* skew 的基本用法 */

/* skewX：水平倾斜 */
.skew-x {
  transform: skewX(20deg);
  /* 水平倾斜20度 */
}

/* skewY：垂直倾斜 */
.skew-y {
  transform: skewY(-15deg);
  /* 垂直倾斜-15度 */
}

/* 两值：同时倾斜（skewX + skewY 一起上） */
.skew-xy {
  transform: skew(20deg, -15deg);
  /* 水平歪20度，垂直歪-15度，双重扭曲！ */
}
```

## 29.2 transform-origin 变换原点

### 29.2.1 默认值——元素中心（50% 50%）

所有变换默认都是绕着元素的中心点进行的。

```css
/* transform-origin 默认是中心点 */

/* 默认值 */
.origin-default {
  transform-origin: center center;
  /* 或 50% 50%，中心点就是元素的心脏 */
}

/* 0 0 = 左上角（top-left），所有偏移量都从这儿算起 */
.origin-0-0 {
  transform-origin: 0 0;
}

/* 关键字组合 */
.origin-top-left {
  transform-origin: top left;
}

.origin-bottom-right {
  transform-origin: bottom right;
}

.origin-top-center {
  transform-origin: top center;
}
```

## 29.3 三维变换

### 29.3.1 perspective——透视效果

三维变换让你的元素不只是平面上的变换，而是有"深度感"的立体变换。`perspective` 就是创造3D效果的"透视法"——就像画画时的透视原理，近大远小，近的物体看起来大，远的物体看起来小。

```css
/* 透视效果需要设置在父元素上 */
.perspective-container {
  perspective: 1000px;
  /* 值越小，透视效果越明显 */
  /* 值越大，透视效果越轻微 */
}

.perspective-box {
  transform: rotateY(45deg);
  /* 在透视容器中，旋转会有3D感 */
}
```

### 29.3.2 translateZ / translate3d

Z轴就是"前后"方向，`translateZ()` 让元素"靠近你"或"远离你"。

```css
/* translateZ：沿Z轴移动 */
.translate-z {
  transform: translateZ(100px);
  /* 向屏幕外（靠近你）移动100px */
}

/* translate3d：三轴同时移动 */
.translate-3d {
  transform: translate3d(50px, 100px, 200px);
  /* 向右50px，下100px，向屏幕外（朝向你）200px */
}
```

### 29.3.3 rotateX / rotateY / rotateZ

三维旋转让元素可以绕着X轴、Y轴或Z轴旋转。

```css
/* rotateX：绕X轴旋转（低头抬头感，像翻筋斗、前空翻）*/
.rotate-x {
  transform: rotateX(45deg);
}

/* rotateY：绕Y轴旋转（左右扭腰，照镜子般的左右翻转）*/
.rotate-y {
  transform: rotateY(45deg);
}

/* rotateZ：绕Z轴旋转（就是平面上转圈，和2D的rotate一回事）*/
.rotate-z {
  transform: rotateZ(45deg);
}
```

### 29.3.4 transform-style: preserve-3d

让元素的子元素保持3D空间，不被"压平"。

```css
/* 保持3D空间 */
.preserve-3d {
  transform-style: preserve-3d;
}

/* 压平（默认）*/
.flat {
  transform-style: flat;
}
```

### 29.3.5 backface-visibility——背面可见性

控制元素背面是否可见。

```css
/* 背面不可见（翻过去就消失了）*/
.back-hidden {
  backface-visibility: hidden;
}

/* 背面可见（默认值，不用写也能看见背面）*/
.back-visible {
  backface-visibility: visible;
}
```

## 29.4 常用场景

### 29.4.1 元素居中

```css
.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

### 29.4.2 悬浮放大

```css
.hover-scale {
  transition: transform 0.3s ease;
}

.hover-scale:hover {
  transform: scale(1.1);
}
```

### 29.4.3 卡片翻转

```css
.flip-card {
  perspective: 1000px;
}

.flip-card-inner {
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}
```

---

## 本章小结

transform 是CSS的魔法棒！常用函数：translate、rotate、scale、skew。三维变换配合 perspective 使用效果更佳。

### 下章预告

下一章我们将学习动画！

