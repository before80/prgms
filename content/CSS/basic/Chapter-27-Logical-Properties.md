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

物理方向（传统）——四个方向永远是固定的东南西北：
                上 / top
                   ↑
                   │
      左 / left ←───┼───→ 右 / right
                   │
                   ↓
                下 / bottom

逻辑方向（现代）——"从哪儿开始读"决定了一切：

  horizontal-tb + ltr（横排英文/中文，最常见）
  ┌──────────────────────────────┐
  │  block-start（= top）         │
  │  ┌─────────────────────────┐ │
  │  │ 文字从这里开始写 →        │ │  ← inline-start 在左边
  │  └─────────────────────────┘ │
  │  block-end（= bottom）        │
  └──────────────────────────────┘

  horizontal-tb + rtl（阿拉伯文，行内方向翻转）
  ┌──────────────────────────────┐
  │  block-start（仍然 = top）    │
  │  ┌─────────────────────────┐ │
  │  │        ← 文字从这里开始写 │ │  ← inline-start 跑到了右边
  │  └─────────────────────────┘ │
  │  block-end（仍然 = bottom）   │
  └──────────────────────────────┘

  vertical-rl（竖排，块级方向翻转）
  ┌────┬────┬────┐
  │ 第 │ 第 │ 第 │  ← 列从左往右数，但文字块是"从右往左"排列
  │ 三 │ 二 │ 一 │     所以 block-start 在右边
  │ 列 │ 列 │ 列 │     而 inline-start 在每列的上边
  └────┴────┴────┘
```

**三个关键词必须先分清**（"逻辑"到底相对谁）：

| 概念 | 含义 | 例子 |
|------|------|------|
| 物理方向 | 屏幕上的固定方位 | `top` / `right` / `bottom` / `left` |
| 块级方向（block） | **文字"一行一行"推进的方向** | 横排是"从上到下"，竖排是"从右到左" |
| 行内方向（inline） | **一行文字内部书写推进的方向** | 横排 LTR 是"从左到右"，RTL 是"从右到左" |

**抽象方向 → 物理方向的实际映射表**（摘自 CSS Writing Modes 规范，`ltr` 指 `direction: ltr`）：

| 逻辑概念 | horizontal-tb（横排） | vertical-rl（竖排） | vertical-lr（竖排） |
|----------|----------------------|---------------------|---------------------|
| `block-size` 对应 | `height` | `width` | `width` |
| `inline-size` 对应 | `width` | `height` | `height` |
| `block-start` 在 | 上 | 右 | 左 |
| `block-end` 在 | 下 | 左 | 右 |
| `inline-start` 在 | 左（ltr）/ 右（rtl） | 上 | 上 |
| `inline-end` 在 | 右（ltr）/ 左（rtl） | 下 | 下 |

> 💡 **这张表是理解整章的钥匙**：逻辑属性本身不"知道"东南西北，它只认"块级/行内 + 开始/结束"。横排时 `inline-start` 等于左边，可一旦换成竖排，它就变成了上边。所以用逻辑属性写出来的组件，能在四种书写模式之间自动适应。

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
  /* 块级方向边距（横排下就是上下边距）*/
  margin-block-start: 20px;    /* 块级开始边（横排 = 上边距）*/
  margin-block-end: 20px;      /* 块级结束边（横排 = 下边距）*/

  /* 行内方向边距（横排 LTR 下就是左右边距）*/
  margin-inline-start: 30px;   /* 行内开始边（横排 LTR = 左边距）*/
  margin-inline-end: 30px;     /* 行内结束边（横排 LTR = 右边距）*/
}

/* 或者用缩写 */
.abbr-logical {
  /* margin-block：依次给 block-start 和 block-end
     （横排下就是"上、下"，和左右无关！）*/
  margin-block: 20px 0;   /* 上 20px，下 0 */

  /* margin-inline：依次给 inline-start 和 inline-end
     （横排 LTR 下就是"左、右"）*/
  margin-inline: 0 30px;  /* 行内开始 0，行内结束 30px（LTR 下即 左 0、右 30px）*/

  /* 两个缩写都遵循"1~2 个值"的规则：
     写一个值 = 两端相同；写两个值 = 先 start 后 end，
     注意它没有物理 margin 那种"上右下左"四值写法 */
  margin-block: 10px;     /* 上 10px，下 10px */
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

先纠正一个常见误解：**`inset` 是"物理方向"的缩写**，它直接展开成 `top` / `right` / `bottom` / `left`（规范原文：*This shorthand property sets the top, right, bottom, and left properties*）。想要逻辑方向，要用 `inset-block` / `inset-inline`。

```css
/* inset 缩写语法 */

/* 四个值：top right bottom left（顺时针）——纯物理方向 */
.inset-all {
  inset: 10px 20px 15px 25px;
  /* 等于 top: 10px; right: 20px; bottom: 15px; left: 25px; */
  /* ⚠️ 即使切换成 RTL，它也是"物理左/物理右"，不会跟着文字方向翻转 */
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

/* 逻辑方向要用 inset-block / inset-inline
   它们只能写 1~2 个值：start 和 end */
.inset-logical {
  position: absolute;
  inset-block: 0;          /* 块级开始和结束都为 0（横排 = 上下贴边）*/
  inset-inline-start: 0;   /* 行内开始边为 0（横排 LTR = 左贴边；RTL 会自动变右）*/
  inset-inline: 0 40px;    /* 行内开始 0、行内结束 40px */
}
```

> 📋 **"inset 家族"对照表：**
>
> | 写法 | 类型 | 能写几个值 | 展开成 |
> |------|------|-----------|--------|
> | `inset` | 物理 | 1~4（同 `margin`） | `top` / `right` / `bottom` / `left` |
> | `inset-block` | 逻辑 | 1~2 | `inset-block-start` / `inset-block-end` |
> | `inset-inline` | 逻辑 | 1~2 | `inset-inline-start` / `inset-inline-end` |
>
> 一句话记法：**带 `block` / `inline` 的才是逻辑属性，光秃秃的 `inset` 是物理属性。** 这个规律对 `margin` / `padding` / `border` 一样成立（`border` 本身也是物理的，`border-inline` 才是逻辑的）。

### 27.1.6 逻辑尺寸——inline-size 与 block-size

这是最容易被忽略、但最重要的一对逻辑属性：**`width` / `height` 也有逻辑版本**。

```css
/* 物理尺寸 */
.physical-size {
  width: 300px;        /* 宽 */
  height: 200px;       /* 高 */
  max-width: 100%;
  min-height: 120px;
}

/* 逻辑尺寸 */
.logical-size {
  inline-size: 300px;  /* 行内方向尺寸：横排 = 宽；竖排 = 高 */
  block-size: 200px;   /* 块级方向尺寸：横排 = 高；竖排 = 宽 */
  max-inline-size: 100%;  /* 对应 max-width（横排）*/
  min-block-size: 120px;  /* 对应 min-height（横排）*/
}
```

| 逻辑属性 | 横排（horizontal-tb）| 竖排（vertical-rl / vertical-lr）|
|----------|---------------------|----------------------------------|
| `inline-size` | 等于 `width` | 等于 `height` |
| `block-size` | 等于 `height` | 等于 `width` |
| `min-inline-size` / `max-inline-size` | `min-width` / `max-width` | `min-height` / `max-height` |
| `min-block-size` / `max-block-size` | `min-height` / `max-height` | `min-width` / `max-width` |

> 💡 **什么时候值得用逻辑尺寸？** 组件需要在"横排/竖排"之间复用的时候（比如同一套卡片样式同时用于横排正文和竖排诗句），或者你在做多语言、多书写模式的组件库。**日常只做横排 LTR 页面时，继续写 `width` / `height` 完全没问题**——逻辑属性是为了"少写一份样式"，不是用来炫技的。
>
> ⚠️ `inline-size` / `block-size` 的值类型和 `width` / `height` 一致（长度、百分比、`auto`、`min-content`、`fit-content` 等）。但对**行内元素**（非替换）设这两组尺寸仍然无效——这一点和 `width` / `height` 一样，需要先改成 `block` / `inline-block`。

### 27.1.7 逻辑溢出

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

### 27.1.8 逻辑边框

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

/* 逻辑边框的缩写：1~2 个值 = start / end */
.logical-border-abbr {
  border-block: 1px dashed #ccc;         /* 块级开始 + 块级结束两条边 */
  border-inline: 4px solid #3498db;      /* 行内开始 + 行内结束两条边 */
  border-inline-start: 3px solid red;    /* 只给行内开始边 */
}

/* 细分长属性也存在：
   border-block-start-width / -style / -color
   border-inline-end-width / -style / -color  ... 依此类推 */
.logical-border-parts {
  border-inline-start-width: 4px;
  border-inline-start-style: dashed;
  border-inline-start-color: #e74c3c;
}
```

**逻辑圆角：`border-radius` 也有逻辑版本。** 命名规则是"两个方向依次说"——先块级、后行内：

```css
/* 逻辑圆角：border-<块级端>-<行内端>-radius */
.logical-radius {
  border-start-start-radius: 12px;  /* 块级开始 + 行内开始 那个角（横排 LTR = 左上角）*/
  border-start-end-radius: 12px;    /* 块级开始 + 行内结束（横排 LTR = 右上角）*/
  border-end-start-radius: 12px;    /* 横排 LTR = 左下角 */
  border-end-end-radius: 12px;      /* 横排 LTR = 右下角 */
}

/* 对照物理写法 */
.physical-radius {
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}
```

> 💡 **为什么圆角也要逻辑化？** 因为物理圆角在 RTL / 竖排下会"站错角"：一个"左上角圆、右下角方"的对话气泡，在阿拉伯语页面里就应该是"右上角圆"。用 `border-start-start-radius` 写，翻转书写模式时圆角会自己跟着走。浏览器支持：`border-*-radius` 逻辑属性在 Chrome 89+、Firefox 66+、Safari 15+。

### 27.1.9 其他常用逻辑属性

逻辑属性不只有 `margin` / `padding` / `border` / `inset`，下面这些也很常用：

```css
/* 1. 逻辑浮动 / 清除浮动（关键字，不是独立属性）*/
.float-start {
  float: inline-start;   /* LTR 下 = left；RTL 下自动变成 right */
}

.float-end {
  float: inline-end;
}

.clear-both {
  clear: both;           /* 还有 inline-start / inline-end 等关键字 */
}

/* 2. 文本对齐：start / end 永远"从文字开始的那一侧"开始 */
.text-align-logical {
  text-align: start;     /* 推荐：等价于 LTR 的 left、RTL 的 right */
  /* text-align: end;  */
}

/* 3. 表格标题放在哪一侧 */
.caption-start {
  caption-side: inline-start;  /* 表格标题跟随书写方向 */
}

/* 4. 滚动相关也有逻辑版本 */
.scroll-logical {
  scroll-margin-block-start: 24px;      /* 对应 scroll-margin-top（横排）*/
  overscroll-behavior-block: contain;   /* 对应 overscroll-behavior-y（横排）*/
}

/* 5. 尺寸相关的"百分比基准"也会跟着逻辑方向走 */
.resizable {
  resize: block;   /* 只允许在块级方向拉伸（横排 = 上下拉），还有 inline / both 等 */
}
```

> 📋 **一句话总结怎么选：**
>
> - 组件要在**多种书写模式 / 语言**下复用 → 优先逻辑属性；
> - 页面只做**横排单一语言**、又不想让同事看着陌生 → 物理属性也没问题，**两套可以混用**（浏览器会按 `writing-mode` / `direction` 把它们统一映射到物理盒子上）；
> - 混用时如果同一个边同时被物理和逻辑属性指定，**看书写顺序：后写的（或特异性更高的）赢**，与属性类型无关。

---

## 27.2 书写模式

### 27.2.1 writing-mode——horizontal-tb / vertical-rl / vertical-lr

`writing-mode` 决定了文字的书写方向。默认是从左到右、从上到下，但有些语言（比如中文竖排、蒙古文）有不同的书写方向。

**什么是 writing-mode？**

想象你是一本书的作者，你决定书页是竖排还是横排。`writing-mode` 就是 CSS 决定"书页排版方式"的属性。

```css
/* horizontal-tb：行内方向水平，块级方向从上到下（默认值，最常见）*/
.default-mode {
  writing-mode: horizontal-tb;
  /* 行内文字是横着的；一行结束后，下一行出现在下方 */
}

/* vertical-rl：垂直从右到左（日语竖排、传统中文）*/
.vertical-rl {
  writing-mode: vertical-rl;
  /* 行内方向竖直向下；一行（一列）结束后，下一列出现在左边
     → 所以整篇文章看起来是"从右往左"排列 */
}

/* vertical-lr：垂直从左到右（蒙古文等）*/
.vertical-lr {
  writing-mode: vertical-lr;
  /* 行内方向竖直向下；下一列出现在右边 → 看起来是"从左往右"排列 */
}

/* sideways-rl / sideways-lr：字形整体"躺倒"90° 的竖排 */
.sideways-rl {
  writing-mode: sideways-rl;
  /* 所有字形（包括本来是竖排的汉字）都朝右侧倒；
     适合"把一段横排内容整体转 90°"的场景，不适合正常的中文竖排 */
}

.sideways-lr {
  writing-mode: sideways-lr;
}

/* ⚠️ 下面这些是给 SVG 文档用的历史值，在 CSS 里已被废弃：
   lr / lr-tb / rl / rl-tb → 请改用 horizontal-tb
   tb / tb-lr              → 请改用 vertical-lr
   tb-rl                   → 请改用 vertical-rl  */
```

```css
/* writing-mode 的两个重要特性 */

/* 1. 它是"继承属性"：写在容器上，里面所有后代都跟着变 */
.vertical-article {
  writing-mode: vertical-rl;   /* 下面整篇文章都变成竖排 */
}

/* 想让标题保持横排？在子元素上再改回来 */
.vertical-article h1 {
  writing-mode: horizontal-tb;
}

/* 2. 它不适用于表格的行/列（以及 ruby 注音容器）：
   table-row、table-column、table-row-group、table-column-group
   这些元素上的 writing-mode 不会生效 */

/* 3. 要改整份文档的书写模式，应该写在根元素上 */
html {
  writing-mode: vertical-rl;   /* 全站竖排（例如竖排小说站点）*/
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

horizontal-tb（默认）：行从下往上叠，每行内从左往右读
┌────────────────────┐
│ 第一行文字 →        │
│ 第二行文字 →        │
│ 第三行文字 →        │
└────────────────────┘

vertical-rl：列从右往左排，每列内从上往下读（中文/日文竖排）
┌──────┬──────┬──────┐
│ 第三 │ 第二 │ 第一 │
│ 列文 │ 列文 │ 列文 │
│ 字 ↓ │ 字 ↓ │ 字 ↓ │
└──────┴──────┴──────┘
         ← 阅读顺序（从右开始）

vertical-lr：列从左往右排，每列内从上往下读（蒙古文）
┌──────┬──────┬──────┐
│ 第一 │ 第二 │ 第三 │
│ 列文 │ 列文 │ 列文 │
│ 字 ↓ │ 字 ↓ │ 字 ↓ │
└──────┴──────┴──────┘
  → 阅读顺序（从左开始）
```

> ⚠️ **竖排下"宽高会互换角色"。** 这是初学逻辑属性时最容易踩的坑：在 `vertical-rl` 的盒子里，`width` 控制的是**水平方向（也就是"一列有多高"）**，`height` 控制的是**竖直方向（一列能放多少字）**——纯粹看物理方向。但**布局计算规则会跟着换轴**：横排时按宽度算的那些规则（比如 `margin: auto` 居中、`width: 50%` 的百分比基准），竖排时会改用高度。规范的说法是："原来作用于水平方向的布局规则，现在作用于竖直方向，反之亦然。"
>
> 所以如果你一边开竖排一边用物理属性，非常容易出现"明明设了 width，看起来动的却是高度"的错觉——这正是逻辑属性存在的意义。

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
  /* ✅ 用 start：LTR 下等于 left，RTL 下自动变成 right，
        不需要因为换语言再改一行 CSS */
  text-align: start;
}

.arabic-page .menu {
  /* 菜单项会从右往左排列 */
}
```

> ⚠️ **规范明确建议：在 HTML 文档里不要用 `direction`，请用 `dir` 属性。** 原因是"CSS 可能被关掉"（比如某些阅读模式、邮件客户端、爬虫渲染）。用 `dir` 能让方向信息成为**内容**的一部分，样式没了也不会反过来：
>
> ```html
> <!-- ✅ 推荐：语义写在 HTML 上 -->
> <html lang="ar" dir="rtl">
> <p dir="ltr">这段技术术语保持从左到右</p>
> <bdo dir="rtl">强制从右往左显示</bdo>
>
> <!-- 用户提交的内容方向不确定时，"auto" 会按内容首字符自动判断 -->
> <p dir="auto">مرحبا</p>
> ```
>
> ```css
> /* CSS 里的 direction 仍然有它的用途：
>    动态切换主题/预览、以及在 Shadow DOM 或第三方组件里兜底 */
> .force-rtl {
>   direction: rtl;
> }
> ```

**`direction` 到底影响什么？**（规范列出的四件事）

| 受影响的东西 | 说明 |
|--------------|------|
| 双向文字的基准方向 | 阿拉伯文、希伯来文与数字/英文混排时的先后顺序 |
| 表格列的顺序 | `direction: rtl` 时，第一个 `<td>` 出现在最右列 |
| 水平溢出的方向 | `overflow` 的起始边跟着翻转 |
| 文本的默认对齐 | `text-align` 的初始表现是"向开始边对齐"，也就是 RTL 下默认右对齐 |

> 💡 **两个容易踩的细节：**
>
> 1. **`direction` 是继承属性，而且只对"块级容器/内联盒"生效**；想让一个**行内元素**（比如 `<span>`）单独改变方向，还需要配合 `unicode-bidi`：
>
>    ```css
>    .inline-rtl {
>      direction: rtl;
>      unicode-bidi: isolate;  /* 让它成为独立的双向文本区间 */
>    }
>    ```
>
> 2. **它不会"翻转物理属性"**：`margin-left: 20px` 在 RTL 下依然是物理左边距。想要"跟着方向走"的边距，要换成 `margin-inline-start`。这也是本章前半部分强调物理/逻辑区别的原因。

### 27.2.3 text-orientation——mixed（默认）/ upright / sideways

`text-orientation` 决定**竖排时每个字符朝哪个方向**。

> ⚠️ **它只在竖排（`vertical-*` / `sideways-*`）下起作用**——在默认的 `horizontal-tb` 里写它等于没写。它也是**继承属性**，写在容器上会影响所有后代。

```css
/* text-orientation 属性 */

/* mixed：默认值。各字符按自己语言的惯例摆
   中文、日文汉字保持"正着站"；拉丁字母/数字旋转 90° 躺着 */
.mixed-orientation {
  text-orientation: mixed;
}

/* upright：所有字符一律"正着站"，
   于是英文单词会变成一列竖着的字母（每个字母一个格）
   → 适合汉字、假名；不适合长英文单词 */
.upright-orientation {
  text-orientation: upright;
}

/* sideways：所有字符统一"躺倒"90°，并按横向排版
   （早期写法叫 sideways-right，已被 sideways 取代）*/
.sideways-orientation {
  text-orientation: sideways;
}
```

> 💡 **竖排里放英文缩写、两位数字怎么办？** 这正是日文排版里的"縦中横（tate-chu-yoko）"需求——希望 `12` 或者 `A4` 横着占一个字的空间。标准做法是把 `text-orientation: upright` 和 `text-combine-upright` 搭配使用：
>
> ```css
> .vertical-cjk {
>   writing-mode: vertical-rl;
>   text-orientation: upright;   /* 让字母也正着站 */
> }
>
> .vertical-cjk .tcy {
>   text-combine-upright: all;   /* 把这个 span 里的字符横着"挤"进一格 */
> }
> ```
>
> ```html
> <p class="vertical-cjk">平成<span class="tcy">12</span>年の記録</p>
> ```
>
> 这样 `12` 会横着显示在一个汉字的宽度内，符合日文实体书的排版习惯。

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

> 📌 **浏览器支持速查：** `text-orientation: upright / mixed` 需要 Chrome 48+ / Firefox 41+ / Safari 14+（更早的 Safari 要用 `-webkit-text-orientation`）；`sideways` 更早就可用（Chrome 12+ / Firefox 44+ / Safari 7+），但旧名的 `sideways-right` 不要再用。

---

## 本章小结

### 核心知识点

| 属性 | 说明 |
|------|------|
| inline-size / block-size | 行内 / 块级方向的尺寸（横排时对应 width / height） |
| min-inline-size / max-block-size 等 | 逻辑尺寸的最小/最大值 |
| margin-inline-start/end | 行内方向边距 |
| margin-block-start/end | 块级方向边距 |
| padding-inline-start/end | 行内方向内边距 |
| padding-block-start/end | 块级方向内边距 |
| border-inline-start/end | 行内方向边框 |
| border-block-start/end | 块级方向边框 |
| border-start-start-radius 等 | 逻辑圆角 |
| inset-block-start/end | 块级方向定位 |
| inset-inline-start/end | 行内方向定位 |
| overflow-block | 块级方向溢出 |
| overflow-inline | 行内方向溢出 |
| float / clear 的 inline-start / inline-end | 逻辑浮动与清除浮动 |
| text-align: start / end | 逻辑文本对齐 |
| writing-mode | 书写模式 |
| direction | 文字方向 |
| text-orientation | 文字朝向 |
| text-combine-upright | 竖排中把若干字符横排进一格（縦中横） |

### 逻辑属性映射表

> ⚠️ **先看前提：下表左边→右边的对应关系，只在"横排 + `direction: ltr`"时成立。** 一旦换成竖排或 RTL，`inline-*` / `block-*` 具体落到哪个物理方向就会变（见 27.1.1 的映射表）。

| 物理属性 | 逻辑属性 | 备注 |
|-----------|-----------|------|
| width | inline-size | 竖排时两者互换 |
| height | block-size | 竖排时两者互换 |
| min-width / max-width | min-inline-size / max-inline-size | 竖排时对应 height 那一组 |
| min-height / max-height | min-block-size / max-block-size | 竖排时对应 width 那一组 |
| margin-top | margin-block-start | 横排下 |
| margin-bottom | margin-block-end | 横排下 |
| margin-left | margin-inline-start | 横排 LTR 下 |
| margin-right | margin-inline-end | 横排 LTR 下 |
| padding-top | padding-block-start | 横排下 |
| padding-bottom | padding-block-end | 横排下 |
| padding-left | padding-inline-start | 横排 LTR 下 |
| padding-right | padding-inline-end | 横排 LTR 下 |
| border-top | border-block-start | 横排下 |
| border-left | border-inline-start | 横排 LTR 下 |
| top | inset-block-start | 横排下 |
| bottom | inset-block-end | 横排下 |
| left | inset-inline-start | 横排 LTR 下 |
| right | inset-inline-end | 横排 LTR 下 |
| border-top-left-radius | border-start-start-radius | 横排 LTR 下 |
| overflow-x | overflow-inline | 横排下；竖排时会反过来 |
| overflow-y | overflow-block | 横排下；竖排时会反过来 |

> 💡 **速记口诀：** `inline-*` 管"读一行"的方向，`block-*` 管"换一行"的方向；每个方向再分 `start`（开始那一端）和 `end`（结束那一端）。至于它最终在屏幕上是上下还是左右——**由 `writing-mode` 和 `direction` 决定，物理属性负责的正是"锁死方向"**。

### 书写模式

| 值 | 说明 |
|-----|------|
| horizontal-tb | 行内水平、块级从上到下（默认值） |
| vertical-rl | 行内竖直向下、列从右往左排（中文/日文竖排） |
| vertical-lr | 行内竖直向下、列从左往右排（蒙古文等） |
| sideways-rl | 竖排，但所有字形整体向右侧倒 90° |
| sideways-lr | 竖排，但所有字形整体向左侧倒 90° |
| lr / rl / tb / tb-rl 等 | SVG 时代的历史值，CSS 中已废弃 |

### 本章易错点速查

| 容易写错的地方 | 正确认识 |
|----------------|----------|
| `margin-block: 20px 0` 是"上下 20px、左右 0" | 错。它只给**块级**的 start/end（横排＝上/下）赋值，跟左右无关；逻辑缩写只有 1~2 个值，没有"四个值"写法 |
| `margin-block-start` 永远等于"上边距" | 只在横排时等于上边距；竖排时它是"右边距"（vertical-rl）或"左边距"（vertical-lr） |
| `inset` 是逻辑属性 | 错。`inset` 展开成 `top`/`right`/`bottom`/`left`，是**物理**属性；逻辑版是 `inset-block` / `inset-inline` |
| RTL 下 `inset: 10px 20px 15px 25px` 里的 left 会变成右边 | 不会。物理属性不随方向翻转，想要翻转请用逻辑属性 |
| 逻辑属性只能替代 margin/padding | 错。尺寸（`inline-size`/`block-size`）、圆角、浮动、文本对齐、表格标题位置都有逻辑版本 |
| `width` / `height` 是唯一写法 | 想跨书写模式复用组件时用 `inline-size` / `block-size`；顺带一提竖排下 `width` 管的是"水平方向"，和直觉相反 |
| 竖排下布局规则照旧 | 竖排会"换轴"：原来看宽度算的规则改用高度，看高度算的改用宽度 |
| 用 `direction: rtl` 来支持阿拉伯语 | 规范建议 HTML 文档改用 `dir` 属性（`<html dir="rtl">`、`dir="auto"`），因为样式可能被关掉 |
| `direction: rtl` 会翻转 `margin-left` | 不会。它只影响双向文字基准方向、表格列顺序、水平溢出方向与默认文本对齐 |
| 给 `<span>` 加 `direction` 就能单独改方向 | 行内元素还需要 `unicode-bidi: isolate`（或 `embed`）才完整生效 |
| 在 RTL 页面里写 `text-align: right` | 更推荐写 `text-align: end` / `start`，这样同一份 CSS 在 LTR / RTL 下都正确 |
| `text-orientation` 写在横排里也有作用 | 它只在竖排模式下生效，横排里写等于没写 |
| 竖排里的英文缩写数字只能一个字母一行 | 用 `text-orientation: upright` + `text-combine-upright: all` 可以做"縦中横" |
| `sideways-rl` 和 `vertical-rl` 差不多 | 两者完全不同：`vertical-rl` 里汉字保持正立，`sideways-*` 会把**所有**字形整体倒 90° |

### 下章预告

下一章我们将学习渐变，让网页告别单调的纯色背景！
