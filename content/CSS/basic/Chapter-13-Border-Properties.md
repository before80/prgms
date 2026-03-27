+++
title = "第13章 边框属性"
weight = 130
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十三章：边框属性

> 边框是元素的"轮廓线"，它让元素从背景中凸显出来。学会控制边框，你的网页元素就能有清晰的边界和立体感。想象一下，一个按钮没有边框，就像一个人出门没穿裤子——技术上不是不行，但你肯定不想看到那个场面。

## 13.1 border 属性

### 13.1.1 border-width——1-4 个值，语法同 margin

```css
/* 一个值：四边相同 */
.one-value { border-width: 10px; }

/* 两个值：上下、左右 */
.two-values { border-width: 10px 20px; }

/* 三个值：上、左右、下 */
.three-values { border-width: 10px 20px 15px; }

/* 四个值：上、右、下、左 */
.four-values { border-width: 10px 20px 15px 25px; }
```

### 13.1.2 border-style——solid、dashed、dotted、double、none、hidden

```css
.solid { border-style: solid; }      /* 实线 */
.dashed { border-style: dashed; }    /* 虚线 */
.dotted { border-style: dotted; }    /* 点线 */
.double { border-style: double; }    /* 双线 */
.none { border-style: none; }        /* 无边框 */
.hidden { border-style: hidden; }    /* 隐藏边框 */
```

### 13.1.3 border-color——默认 currentColor

```css
/* 默认继承 color 属性值 */
.default {
  color: #3498db;
  border: 2px solid;  /* 边框颜色继承 color */
}

.custom-color {
  border-color: #e74c3c;
}
```

### 13.1.4 border——border-width border-style border-color 缩写

```css
/* 缩写写法 */
.shorthand {
  border: 2px solid #333;
}
```

### 13.1.5 单独设置某一边——border-top、border-bottom、border-left、border-right

```css
.top-only { border-top: 2px solid #3498db; }
.bottom-only { border-bottom: 1px dashed #ccc; }
.left-only { border-left: 3px solid #e74c3c; }
.right-only { border-right: none; }
```

---

## 13.2 border-radius 圆角

### 13.2.1 一个值——border-radius: 10px;（四角都是 10px）

```css
.rounded {
  border-radius: 10px;
}
```

### 13.2.2 四个值——border-radius: 10px 20px 30px 40px;（左上 右上 右下 左下）

```css
.four-corners {
  border-radius: 10px 20px 30px 40px;
}
```

### 13.2.3 50%——创建正圆（需要元素是正方形）或椭圆

```css
/* 正圆 */
.circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

/* 椭圆 */
.oval {
  width: 200px;
  height: 100px;
  border-radius: 50%;
}
```

### 13.2.4 椭圆半径——border-radius: 50% / 30%;

`/` 前面是水平半径，后面是垂直半径。`50% / 50%` 就是普通圆（等于直接写 `50%`），想看到真正的椭圆？得让它们不一样！

```css
.ellipse {
  /* 水平 50%，垂直 30%，这才叫椭圆 */
  border-radius: 50% / 30%;
}
```

---

## 13.3 border-image 边框图片

### 13.3.1 border-image-source——图片路径

```css
.source {
  border-image-source: url("border.png");
}
```

### 13.3.2 border-image-slice——切割图片

`fill` 关键字是点睛之笔——不加它，中间区域会被挖空；加了它，中间部分会保留下来显示在元素内部。

```css
.slice {
  border-image-slice: 30 fill;  /* 30 是偏移量，fill 保留中间区域 */
}
```

### 13.3.3 border-image-repeat——平铺方式

```css
/* stretch（默认）/ repeat / round / space */
.repeat {
  border-image-repeat: round;
}
```

### 13.3.4 border-image——缩写属性

source、slice、width、outset、repeat 可以合并成一行搞定：

```css
.banner {
  /* 语法：source slice / width / outset repeat */
  border-image: url("border.png") 30 / 10px / 0 round;
}
```

---

## 13.4 box-shadow 阴影

### 13.4.1 五参数——x偏移 y偏移 模糊半径 扩展半径 颜色

```css
.shadow {
  box-shadow: 5px 5px 10px 0 rgba(0, 0, 0, 0.3);
  /*   x     y    模糊    扩展   颜色 */
}
```

### 13.4.2 示例——box-shadow: 5px 5px 10px 0 rgba(0,0,0,0.3);

```css
/* 常用阴影效果 */
.card-shadow {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.hover-shadow {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}
```

### 13.4.3 inset 阴影——在元素内部

```css
.inset {
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
}
```

### 13.4.4 多层阴影——用逗号分隔

```css
.multi {
  box-shadow:
    0 4px 6px rgba(0, 0, 0, 0.1),
    0 10px 20px rgba(0, 0, 0, 0.08),
    0 20px 40px rgba(0, 0, 0, 0.06);
}
```

---

## 13.5 outline 属性

### 13.5.1 outline——轮廓线，与 border 类似但不占据布局空间

```css
.outline {
  outline: 2px solid #3498db;
}
```

### 13.5.2 outline-width——轮廓宽度

```css
.thick-outline {
  outline-width: 4px;
}
```

### 13.5.3 outline-color——轮廓颜色

```css
.colored-outline {
  outline-color: #e74c3c;
}
```

### 13.5.4 outline-style——solid、dashed、dotted 等

```css
.dashed-outline {
  outline-style: dashed;
}
```

### 13.5.5 outline-offset——轮廓与边框的间距

```css
.offset-outline {
  outline: 2px solid #3498db;
  outline-offset: 5px;
}
```

---

## 本章小结

恭喜你完成了第十三章的学习！边框属性让你的网页元素更有轮廓感。

### 核心知识点

| 属性 | 说明 |
|------|------|
| border | 边框（width + style + color） |
| border-radius | 圆角 |
| border-image | 边框图片 |
| box-shadow | 阴影 |
| outline | 轮廓线 |

### 边框 vs 轮廓

- **边框（border）**：占据布局空间，影响元素尺寸
- **轮廓（outline）**：不占据布局空间，绘制在元素外部

### 本章结束！

恭喜你完成了第十三章的学习！边框、圆角、阴影、轮廓……你已经学会了给元素化妆的多种手段。接下来可以去探索更多 CSS 技能点，或者直接动手做点小项目练练手！

