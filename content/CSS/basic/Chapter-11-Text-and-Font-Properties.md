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

写字体栈时有几条硬规则：

- **字体名含空格（或中文名）必须加引号**，如 `"Microsoft YaHei"`。写成 `Microsoft YaHei` 是无效声明，整条 `font-family` 会被丢弃——这是很常见却难发现的错误。
- **最后一定要放一个通用字体族**（`serif`、`sans-serif`、`monospace`、`cursive`、`fantasy`、`system-ui`），它是"保底"，保证前面的字体全都没有时仍然有合理的默认外观。
- **不要用通用字体族当普通字体名加引号**：`"sans-serif"` 会被当成一个叫 sans-serif 的真实字体去查找，找不到就继续往下，等于白写。正确写法是不加引号：`sans-serif`。
- 字体栈的顺序反映优先级：越靠前越优先使用，而"具体字体名"应放在"通用族"之前。

字体族分为两大类：**通用族**（`serif` 衬线、`sans-serif` 无衬线、`monospace` 等宽、`cursive` 手写、`fantasy` 装饰）和**具体字体名**（`Arial`、`PingFang SC` 等）。一个稳妥的跨平台栈可以这样写：

```css
/* 先用系统自带的现代无衬线字体，最后落到通用族 */
body {
  font-family: system-ui, -apple-system, "Segoe UI", Roboto,
               "PingFang SC", "Microsoft YaHei", sans-serif;
}
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

### 11.2.1 px——绝对单位，不随用户的字号设置变化

```css
/* 像素是最常用的绝对单位 */
.text {
  font-size: 16px;
}

h1 {
  font-size: 32px;
}
```

这里有一个经常被误解的点：`px` 在 CSS 里是"绝对单位"，指的是它**不会随用户在浏览器里调整默认字号（比如把默认 16px 改成 20px）而自动变化**——这一点和 `rem`、`em` 不同。但是浏览器的**页面缩放**（Ctrl/⌘ + `+`）会等比放大整个页面，`px` 写的大小当然也会跟着变大。

换句话说：

- 用户改"设置 → 字体大小"→ 只有 `rem`/`em` 会跟着变，`px` 不变；
- 用户按 Ctrl/⌘ + `+` 缩放页面 → 所有单位（含 `px`）一起变大。

无障碍实践建议：正文字号用 `rem`，让用户的字号偏好生效；只在确实需要严格像素对齐的场合（图标、细边框）才用 `px`。

### 11.2.2 em——相对于父元素"计算后的"字体大小，嵌套时容易失控

```css
.parent {
  font-size: 20px;
}

.child {
  font-size: 1.5em;  /* 20px * 1.5 = 30px */
}
```

关键细节：`1em` 等于**当前元素继承来的、父元素最终计算出的** `font-size`，而不是父元素写在 CSS 里的那个声明。如果父元素自己也是 `em`，效果就会一层层放大：

```css
/* 很多人在这里踩坑 */
.level1 { font-size: 1.2em; }  /* 相对 body（16px）→ 19.2px */
.level2 { font-size: 1.2em; }  /* 相对 19.2px → 23.04px */
.level3 { font-size: 1.2em; }  /* 相对 23.04px → 27.65px */
```

三层嵌套后字号已经比预期大了一倍多。所以：

- 需要"可随父元素缩放"的场景（按钮内文字、图标旁文字）才用 `em`；
- 页面级排版用 `rem`，避免连锁放大。

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

### 11.2.5 ch——字符"0"的宽度，用于限定输入宽度

```css
/* 用于输入框最小宽度设置 */
.username-input {
  min-width: 20ch;
}
```

`1ch` 的定义是**当前字体中数字"0"的宽度**，而不是任意字符的宽度。既然"0"在多数等宽（monospace）字体里和所有其他字符一样宽，`ch` 在等宽场景下非常精确；但在比例字体（如中文正文、Arial 等）里，不同字符宽度差别很大，`ch` 只能作为"大约能放多少个数字"的粗略估计。

常见用法正是上面的输入框/验证码框：`20ch` 大致等于"能显示 20 个数字/字母的宽度"。另外要注意 `ch` 也和 `em` 一样会随字号缩放——字号变了，`20ch` 的像素宽度也会变。

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

`normal` 与 `400`、`bold` 与 `700` 完全等价，只是写法不同。另外还有两个相对值：`lighter`（比父元素轻）和 `bolder`（比父元素重），但它们按"从父元素字重往相邻档位跳"计算，实际结果依赖父元素取值，容易出乎意料，不如直接写数字清晰。

重要现实：**不是每个字体都提供全部 9 档字重**。很多中文字体只有 400 和 700 两档，此时你写 `500` 或 `600`，浏览器要么就近取 400/700，要么合成假粗体。

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

### 11.4.3 font-synthesis——控制浏览器是否"伪造"粗体/斜体

```css
/* 禁止浏览器合成字体样式 */
.no-synthesis {
  font-synthesis: none;
}
```

当一个字体只提供了常规字重（400），而你又要求 `font-weight: 700` 时，浏览器不会报错，而是把 400 的字形"描粗一点"来冒充粗体——这就是**合成（synthesis）**。它能让页面不至于变成纯常规体，但假粗体/假斜体通常比真正的粗体字、真斜体难看得多。`font-synthesis: none` 就是明确告诉浏览器"宁可保持原样，也别伪造"。

可选值：

| 值 | 含义 |
| --- | --- |
| `none` | 禁止合成（等价于 `font-synthesis-weight: none; font-synthesis-style: none; font-synthesis-small-caps: none;`） |
| `weight` | 允许合成粗体 |
| `style` | 允许合成斜体（oblique） |
| `small-caps` | 允许合成小型大写字母 |

> 规范演进提醒：早期 `font-synthesis` 只有 `none`/`weight`/`style` 三个值；CSS Fonts Module Level 4 把它细化为 `font-synthesis-weight`、`font-synthesis-style`、`font-synthesis-small-caps` 三个长属性，简写语法为 `none | [ weight || style || small-caps ]`。此外还有一个**不在简写范围内**的 `font-synthesis-position`（控制上下标是否允许合成），需要单独声明。新代码可以优先用拆分后的长属性，控制更精细。

---

## 11.5 font-optical-sizing 光学尺寸

### 11.5.1 auto（自动调整）/ none——让可变字体按字号切换"最佳形态"

```css
.auto-sizing {
  font-optical-sizing: auto;  /* 默认值，自动优化 */
}

.no-optical-sizing {
  font-optical-sizing: none;
}
```

同一款字体，用来做标题（很大）和用来做正文（很小）时，理想的笔画粗细和字距其实不一样：小字号需要更粗、更开的笔画才看得清，大字号则需要更细腻。**光学尺寸（optical sizing）**就是字体里的一条 `opsz` 轴，专门用来做这种自适应。

`font-optical-sizing: auto`（默认）让浏览器根据当前 `font-size` 自动调整这条轴；`none` 则关掉这种自动调整。注意两点：

- 只有当字体本身是**带 `opsz` 轴的可变字体**时才有可见效果，普通静态字体上它什么也不做；
- 这是"自动"行为，不需要你手动设置 `font-variation-settings: "opsz" 14`——但如果你确实手动设置了，手动值会覆盖自动值。

---

## 11.6 font-feature-settings OpenType 特性

### 11.6.1 控制连字、字距等高级 OpenType 特性

```css
/* 连字（liga）、字距调整（kern）等 */
.text-with-features {
  font-feature-settings: "liga" 1, "kern" 1, "swsh" 1;
}
```

`font-feature-settings` 是一把"万能钥匙"，用 4 字符的 OpenType 标签直接开关字体里的特性。常见标签：

| 标签 | 作用 |
| --- | --- |
| `"liga"` | 标准连字（如 `fi` 合成一个字形） |
| `"dlig"` | 自由连字 |
| `"kern"` | 字距调整 |
| `"tnum"` | 表格数字（数字等宽，便于对齐金额、表格） |
| `"pnum"` | 比例数字（默认，数字宽度不一） |
| `"onum"` | 旧式数字（高低错落，适合正文） |
| `"smcp"` | 小型大写字母 |
| `"swsh"` | 花体/装饰字形（swash） |

值 `1` 表示开启、`0` 表示关闭。但**优先使用语义化的高层属性**：`font-kerning`、`font-variant-ligatures`、`font-variant-numeric`、`font-variant-caps` 等，它们可读性更好、也能被 `font-variant` 简写覆盖；只有在高层属性没有覆盖到的冷门特性（如 `"swsh"`）上才用 `font-feature-settings`。

实践中最常用的一例是让表格里的数字对齐：

```css
/* 数字等宽 + 表格数字，金额小数点对齐不跳动 */
.price {
  font-variant-numeric: tabular-nums;
  /* 等价于 font-feature-settings: "tnum" 1; */
}
```

注意：不是所有字体都包含上述所有特性，字体里没有的标签写了也没有效果。

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

### 11.8.1 防止 iOS 横屏时自动放大字号——请用 100%，而不是 none

```css
/* 正确做法：把自动调整限制在 100%，只阻止"额外放大" */
html {
  -webkit-text-size-adjust: 100%;
}
```

背景：iOS Safari 在横屏、或页面很宽时，会猜测这是"桌面版网页"，于是自动把正文字号放大，避免文字太小。这会让精心设计的排版在横屏突然变形。`-webkit-text-size-adjust` 用来关闭这种推测。

**但千万不要写 `-webkit-text-size-adjust: none`。** 在部分浏览器/系统上，`none` 会连带**禁止用户手动双指缩放页面**，这属于严重的无障碍问题（低视力用户离不开缩放）。写 `100%` 的含义是"不要替我放大，但允许用户自己放大"，效果与 `none` 接近而不会误伤用户。

补充：`text-size-adjust` 目前仍需 `-webkit-` 前缀，写标准属性 `text-size-adjust: 100%` 是为将来做准备，两者一起写最稳妥。

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

无单位、`px`、百分比三者最关键的差别在**继承行为**上，这也是"为什么推荐无单位"的真正原因：

```css
/* 父元素字号 16px */
.parent {
  font-size: 16px;
  line-height: 150%;   /* 计算成 24px 后再继承下去 */
}

.child {
  font-size: 32px;
  /* 继承到的是固定的 24px，不是 150%！
     32px 的字配上 24px 行高 → 文字挤在一起甚至重叠 */
}
```

对比一下：

| 写法 | 继承时传递的是 | 子元素改了字号会怎样 |
| --- | --- | --- |
| `line-height: 1.5`（无单位） | 数字 `1.5` 本身 | 行高 = 子元素字号 × 1.5，**自动跟着变** |
| `line-height: 24px` | 固定的 `24px` | 不跟着变，可能过小/过大 |
| `line-height: 150%` | 固定的计算值 `24px` | 不跟着变（和 px 一样） |

所以规则很简单：**需要继承的场景一律用无单位写法**，百分比和 px 只在个别不想被继承的地方使用。

### 11.9.3 单行垂直居中——设置 line-height 等于容器高度

```css
/* 单行文字垂直居中 */
.centered-text {
  height: 60px;
  line-height: 60px;
}
```

这个技巧的前提是**单行**：容器只有一行文字，把行高撑成容器高度，文字自然就被居中。一旦文字换成两行，第二行就会溢出容器——所以更现代的写法是给容器用 `display: flex; align-items: center;`，能同时适配多行。另外 `line-height` 过大时文字会有额外的上下留白，视觉上未必"正中"（因为字体上下本来就留有余量），需要微调时可用 `padding` 配合。

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

### 11.11.1 对行内级元素和表格单元格有效，对块级元素无效

```css
/* vertical-align 对行内级元素有效 */
.inline-element {
  vertical-align: middle;
}
```

`vertical-align` 决定了元素在**它所在的那一行（line box）里**相对基线怎么摆放。因此它只对"处于行内格式化上下文中的元素"生效，具体包括：

- 行内元素（`display: inline`，如 `span`、`a`）；
- 行内块（`display: inline-block`，如内联按钮、内联图片容器）；
- 行内表格（`display: inline-table`）；
- 表格单元格（`display: table-cell`，此时语义略有不同）。

它**对块级元素无效**。所以 `div { vertical-align: middle; }` 不会有任何效果——这是初学者最常见的困惑之一。如果你想让块级元素垂直居中，应该用 Flexbox（`align-items`）、Grid，或前面的 `line-height` 技巧，而不是 `vertical-align`。

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

为什么图片底部会有空隙？因为图片默认 `vertical-align: baseline`，而基线的位置是按文字的"下缘"定的——文字下方还留有给字母下伸部（如 `g`、`y`）的空间，图片就被顶起来了，看起来像多了一条缝。

彻底一点的做法有三种：给图片设 `vertical-align: bottom`（或 `middle`/`top`）、把图片改成 `display: block`、或者干脆让父容器用 Flex 布局。第一种改动最小，第三种最"现代"。

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

关于 `text-decoration` 还有两个常被忽略的点：

**第一，它不能被子元素"取消"。** 给链接整体加下划线后，即使给里面的 `span` 写 `text-decoration: none`，下划线依然存在——因为装饰线是父元素画的，会贯穿子元素：

```css
a { text-decoration: underline; }
a span { text-decoration: none; }  /* 无效！下划线还在 */

/* 正确做法：把装饰线加在真正需要的那个子元素上 */
a { text-decoration: none; }
a span { text-decoration: underline; }
```

**第二，装饰线可以微调位置和粗细**，用 `text-underline-offset` 和 `text-decoration-thickness`：

```css
.link {
  text-decoration: underline;
  text-underline-offset: 4px;          /* 下划线上下偏移 */
  text-decoration-thickness: 2px;      /* 下划线粗细（也可用 from-font、百分比） */
  text-decoration-skip-ink: auto;      /* 下划线遇到字母下伸部自动断开（默认） */
}
```

这几个属性在做"悬停时下划线滑出"之类的高级效果时非常有用。`text-decoration` 简写**不包含** `text-underline-offset` 和 `text-decoration-thickness`，它们需要单独写。

---

## 11.13 text-transform 文本转换

### 11.13.1 uppercase（全大写）、lowercase（全小写）、capitalize（首字母大写）

```css
.uppercase { text-transform: uppercase; }    /* 全大写 */
.lowercase { text-transform: lowercase; }    /* 全小写 */
.capitalize { text-transform: capitalize; }  /* 首字母大写 */
```

三点必须知道：

- **它只改变"显示效果"，不改变数据。** 表单里输入 `hello`，套上 `text-transform: uppercase`，用户看到的、提交时传给后端的仍是 `hello`。如果业务要求"必须是大写"，服务端还要自己做转换，别依赖 CSS。
- **`capitalize` 是按"每个单词的首字母"处理**的，而单词的划分依赖语言规则。它不会把小写中间的大写"压平"，`iPHONE` 首字母本来就大写，结果是 `iPHONE` 而不是 `Iphone`。英文人名/品牌名有特殊大小写时，别指望 `capitalize`。
- **选择器匹配的是原始文本。** `text-transform: uppercase` 之后，`.uppercase::first-letter` 之类的伪元素、以及无障碍朗读读到的都是原始大小写，搜索页面内容时也按原文匹配。

> 无障碍提示：全大写（uppercase）的文字对阅读障碍用户来说更吃力，屏幕阅读器有时还会把连续大写字母逐个字母念出。重要正文尽量不要整段大写。

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

### 11.14.2 多行省略——line-clamp（旧写法为 -webkit-line-clamp）

```css
/* 标准属性和兼容写法一起写，现阶段最稳妥 */
.multi-line-ellipsis {
  line-clamp: 3;
  display: -webkit-box;      /* 现阶段仍需配合 -webkit-box 才能生效 */
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

多行省略的实现一直有点历史包袱：`-webkit-line-clamp` 原本是 WebKit 私有属性，因为太好用被各浏览器广泛支持，后来规范才加入标准的 `line-clamp`。现在写代码时把两者都写上：

| 属性 | 状态 |
| --- | --- |
| `display: -webkit-box` + `-webkit-box-orient: vertical` | 让元素变成"垂直多行盒子"，`line-clamp` 的前提 |
| `-webkit-line-clamp: 3` | 最广泛支持的实现，Chrome/Safari/Firefox 都认 |
| `line-clamp: 3` | 标准属性名，用时不带前缀 |
| `overflow: hidden` | 隐藏被截断的后续行，必须写 |

注意副作用：`display: -webkit-box` 会**覆盖**原本的 `display` 值，如果你本来设的是 `display: flex` 或 `grid`，加了多行省略后布局会变，需要额外测试。另外多行省略通常还要配合 `overflow-wrap: break-word`，否则超长英文单词撑不开容器，省略号可能不出现。

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

`white-space` 其实是两个问题的组合：**要不要合并空白**（空格、换行、制表符），以及**允许在哪儿换行**。把取值列全，理解会清楚很多：

| 值 | 连续空格 | 是否自动换行 | 行尾换行符 | 典型用途 |
| --- | --- | --- | --- | --- |
| `normal` | 合并为一个 | 允许 | 当空格忽略 | 普通正文（默认） |
| `nowrap` | 合并为一个 | **禁止** | 当空格忽略 | 单行省略、不换行的按钮文字 |
| `pre` | 原样保留 | **禁止** | 形成换行 | 需要严格保留格式且不换行 |
| `pre-wrap` | 原样保留 | 允许 | 形成换行 | 展示代码、聊天消息（最常用） |
| `pre-line` | 合并为一个 | 允许 | 形成换行 | 只尊重换行、不保留多个空格 |
| `break-spaces` | 原样保留 | 允许 | 形成换行 | 像 `pre-wrap`，但行尾空格也占位、能撑开换行 |

最实用的两个：展示用户输入的文本用 `pre-line`（尊重换行、脏空格自动清理），展示代码用 `pre-wrap`（格式一点不变，且长行会自动折行）。

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

`word-wrap` 是 `overflow-wrap` 的旧名（属于"别名"，不是独立属性），两者写法效果相同。常见的几个相关属性容易混淆，这里一次说清：

| 属性/值 | 行为 | 什么时候用 |
| --- | --- | --- |
| `overflow-wrap: normal` | 只有整个单词都放不下时才在别处换行，不会切断单词 | 默认 |
| `overflow-wrap: break-word` | 单词实在放不下时才**强行断词** | 最常用，处理 URL/长英文 |
| `overflow-wrap: anywhere` | 和 `break-word` 类似，但断词位置**会影响容器的 min-content 宽度计算** | 配合 Flex/Grid 的自动定宽 |
| `word-break: break-all` | 随时可以在任意字符处断行（对中文影响大） | 只在确实需要时用 |
| `word-break: keep-all` | 中文/日文不在字符间断行，只在标点或空格处断 | 需要避免中文被硬切断 |
| `hyphens: auto` | 按语言规则加连字符换行（需要 `lang` 属性） | 英文排版讲究时 |

一个实用组合是让中文尽量按标点/词组换行、实在放不下时才硬断：

```css
.card-title {
  overflow-wrap: break-word;
  word-break: keep-all;   /* 中文优先在标点或空格处换行，不逐字硬断 */
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

书写规则：`偏移X 偏移Y [模糊半径] 颜色`。只有 X、Y 是必需的，模糊半径可省略（省略即无模糊，得到硬边阴影），颜色可写在前面也可写在后面。多层阴影用逗号分隔，**先写的画在最上层**，所以做描边/发光时常把最"紧"的一层写在最前。

几个实用提示：

- 阴影**不占布局空间**，不会撑大元素，也不会被 `overflow: hidden` 裁掉；
- 给深色背景上的白色文字加 `text-shadow: 0 1px 2px rgba(0,0,0,.5)` 能明显提升可读性；
- 阴影是逐字渲染的，长文本叠加多层阴影会增加绘制开销，动画里慎用。

---

## 11.18 print-color-adjust（打印样式）

### 11.18.1 economy（允许省墨降质）/ exact（强制保留颜色）

> 属性改名提醒：早期规范草案里这个属性叫 `color-adjust`，后来因为名字太笼统、容易和颜色调整的其他概念混淆，标准名已改为 **`print-color-adjust`**。现在写代码应当使用新名字（`color-adjust` 作为遗留别名仍被部分浏览器识别，但不要在新项目里用）。

```css
@media print {
  .save-ink {
    print-color-adjust: economy;  /* 允许浏览器降低颜色/背景以省墨 */
  }

  .keep-color {
    print-color-adjust: exact;                        /* 强制保留颜色和背景 */
    -webkit-print-color-adjust: exact;                /* 兼容旧版 Safari/Chrome */
  }
}
```

默认行为是 `economy`：浏览器打印时可能去掉页面背景色、把深色底改成白色，以免浪费墨水。如果你确实需要打印出品牌色（比如发票上的色块），就用 `exact`。注意：**是否能真的打出颜色还取决于打印机和用户的"打印背景图"选项**，`exact` 只是让浏览器别主动丢弃，不能保证最终纸张上一定有颜色。

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

完整一点的写法通常还要指定字重、字形类型，并用 `local()` 优先尝试用户本机已装字体，以及提供多种格式兜底：

```css
@font-face {
  font-family: "MyFont";
  src: local("MyFont"),
       url("fonts/MyFont.woff2") format("woff2"),
       url("fonts/MyFont.woff")  format("woff");   /* 老浏览器兜底 */
  font-weight: 400;      /* 这个文件对应哪个字重 */
  font-style: normal;    /* 对应正体还是斜体 */
  unicode-range: U+0000-00FF;  /* 可选：只用于这批字符（做字体子集/中文分片） */
}

/* 同一字体的粗体是另一个文件，需要用同样的 font-family 再声明一次 */
@font-face {
  font-family: "MyFont";
  src: url("fonts/MyFont-Bold.woff2") format("woff2");
  font-weight: 700;
}
```

几个要点：

- **格式优先级**：现代项目首选 `woff2`（体积最小、压缩率最高），`woff` 只留给很老的浏览器。
- **`format()` 不能省**：不写的话浏览器可能下载了才发现不支持，白白浪费一次请求。
- **`font-weight`/`font-style` 描述符一定要和文件真实内容对应**。如果粗体文件没声明 `font-weight: 700`，浏览器就会认为"这个家族只有 400"，需要用粗体时要么去合成假粗体，要么继续用常规体。
- **中文项目建议拆分**：一个完整中文字体动辄几 MB，可以用 `unicode-range` 把常用字分成几个子集文件，浏览器只下载页面真正用到的那一两片。

### 11.19.2 font-display——控制"字体还没下载完时先显示什么"

```css
@font-face {
  font-family: "MyFont";
  src: url("fonts/MyFont.woff2") format("woff2");
  font-display: swap;  /* 先显示后备字体，下载完再切换 */
}
```

自定义字体要等网络下载，这段时间里文字用什么显示，由 `font-display` 决定。它有五个取值，权衡的是"文字立刻可见"和"避免闪烁"：

| 值 | 下载期间的显示 | 超时后的行为 | 适用场景 |
| --- | --- | --- | --- |
| `auto` | 由浏览器决定（通常等同 `block`） | —— | 不明确表态 |
| `block` | **短暂隐藏**（约 3 秒"白屏期"） | 超时后先用后备字体，字体到了再换 | 图标字体、必须用自定义字体才对的内容 |
| `swap` | **立刻用后备字体显示** | 字体到了直接换（可能有可见的跳动） | 正文最常用，保证首屏可读 |
| `fallback` | 只有很短的白屏期（约 100ms） | 100ms 内到就用，否则整页会话都用后备字体 | 想要折中、能接受"这次不换"|
| `optional` | 只有很短的白屏期 | 若下载太慢则**本次访问直接放弃**（可能缓存后下次用） | 追求极致性能、字体只是锦上添花 |

实践建议：

- **正文**：`swap` 或 `optional`，保证用户尽快看到内容；
- **图标字体**：`block`，宁可短暂隐藏也不能出现乱码方块；
- 想减少"换字体跳动"，可以给后备字体设置 `size-adjust`、`ascent-override` 等描述符做度量对齐，让切换前后行高基本一致。

---

## 本章小结

恭喜你完成了第十一章的学习！文字与字体属性是网页设计的基础。

### 核心知识点

| 属性 | 说明 |
|------|------|
| font-family | 字体栈；含空格的字体名必须加引号，末尾要有通用字体族 |
| font-size | 字号（px 绝对、em 相对父级、rem 相对根元素、clamp 流体、ch 数字宽） |
| font-weight | 字重（100-900，`normal`=400、`bold`=700） |
| font-style / font-synthesis | 斜体；`font-synthesis` 控制是否允许浏览器伪造粗体/斜体 |
| font-optical-sizing / font-feature-settings | 可变字体光学尺寸；OpenType 特性开关（优先用 `font-variant-*` 高层属性） |
| line-height | 行高；需继承时一定用无单位写法 |
| text-align | 文本对齐 |
| vertical-align | 垂直对齐（仅对行内级元素和表格单元格有效，对块级无效） |
| text-decoration | 文本装饰；不能被子元素取消，可配合 `text-underline-offset` 微调 |
| text-transform | 大小写转换；只改显示，不改数据 |
| text-shadow | 文字阴影（不占布局，多层时先写的在上） |
| white-space | 空白处理（`pre-wrap` 展示代码最常用） |
| overflow-wrap / word-break | 长单词与中文换行控制 |
| line-clamp | 多行省略（配合 `-webkit-line-clamp` 一起写） |
| -webkit-text-size-adjust | 移动端字号自动调整；**用 `100%` 而非 `none`**（`none` 会禁止用户缩放） |
| @font-face / font-display | 自定义字体，`font-display` 五档取值控制字体下载期间的显示 |
| print-color-adjust | 打印时是否保留颜色/背景（旧名 `color-adjust`，已废弃） |

### 下章预告

下一章我们将学习颜色与背景属性，让你的网页更加丰富多彩！
