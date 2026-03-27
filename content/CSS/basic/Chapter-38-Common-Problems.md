+++
title = "第38章 常见问题"
weight = 380
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十八章：常见问题与坑

> 踩坑是成长的必经之路，这一章帮你提前知道这些坑在哪里！

## 38.1 盒模型

### 38.1.1 父元素高度塌陷

浮动元素导致父容器高度塌陷。

```css
/* 解决方案 */
.parent { display: flow-root; }
```

### 38.1.2 margin上下重叠

```css
/* 方案1：父元素 overflow: hidden（简单但可能有副作用）*/
.parent { overflow: hidden; }

/* 方案2：父元素 padding 代替子元素 margin（推荐）*/
.parent { padding: 20px 0; }

/* 方案3：子元素使用单方向 margin（推荐）*/
.child { margin-top: 20px; } /* 只用 top 或 bottom */
```

## 38.2 布局

### 38.2.1 Flex项目被压缩

```css
.item { flex-shrink: 0; }
```

### 38.2.2 inline-block间隙

inline-block元素之间会产生空白间距，解决方案是把父元素设为flex或grid。

```css
/* 方案1：父元素用flex（最简单粗暴）*/
.parent { display: flex; }

/* 方案2：父元素font-size归零 */
.parent {
  font-size: 0;
}
.parent > * {
  font-size: 16px; /* 子元素恢复字体大小 */
}
```

## 38.3 动画

### 38.3.1 height:auto无法过渡

`height: auto` 是无法参与过渡动画的——浏览器根本不知道 auto 该渐变到哪个值。

```css
/* ❌ 这样写，动画不会生效 */
.box {
  height: 0;
  transition: height 0.3s;
}
.box.open {
  height: auto; /* 浏览器：auto 是多少？我不会渐变到 auto 啊 */
}

/* ✅ 正确做法：用 max-height 代替，指定一个足够大的具体值 */
.collapsible {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.collapsible.open {
  max-height: 1000px; /* 足够大，大过内容实际高度即可 */
}
```

> 💡 进阶方案：用 `grid-template-rows: 0fr / 1fr` 配合 `transition`（CSS Grid 特有），可以实现真正意义的 `height: auto` 动画，且无需估算具体数值。

### 38.3.2 动画性能差

CSS 动画的性能取决于你动了什么属性。记住一个原则：**能不动 layout 就别动，能跳过 paint 就跳过**。

| 属性类型 | 示例 | 性能 | 代价 |
|---|---|---|---|
| ** compositor-only ** | `transform`、`opacity` | 🚀 极快 | 仅 CPU/合成器参与 |
| paint 相关 | `background`、`color`、`box-shadow` | 🐢 较慢 | 触发重绘 |
| layout 相关 | `width`、`height`、`margin`、`padding`、`top/left` | 🐌 慢 | 触发回流重绘 |

```css
/* ✅ 好：transform 和 opacity 由合成器处理，不触发 layout 和 paint */
.fast {
  transform: translateX(100px);
  opacity: 0.5;
}

/* ❌ 差：left/top 每次动画都会触发回流，性能极差 */
.slow {
  left: 100px;
  top: 100px;
}
```

> 💡 所有现代动画库（Framer Motion、GSAP 等）底层都在用 `transform` + `opacity`，原因就在这里。所以下次想给元素做位移动画时，请默念：`left` 是魔鬼，`transform` 是朋友。

---

## 本章小结

踩坑是成长！

### 下章预告

最后一章UI组件！

