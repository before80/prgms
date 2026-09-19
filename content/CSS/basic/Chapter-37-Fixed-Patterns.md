+++
title = "第37章 固定搭配速查"
weight = 370
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十七章：固定搭配速查

> 这些固定搭配收藏起来，编码效率翻倍！

## 37.1 文字类

### 37.1.1 单行省略

一行放不下时用"…"收尾。四个属性缺一不可：`white-space: nowrap` 不让换行、`overflow: hidden` 把超出部分裁掉、`text-overflow: ellipsis` 画省略号，而元素本身必须有一个"确定"的宽度（`width`/`max-width`），否则它会被内容撑开，永远不触发省略。

```css
.single-line {
  width: 100%;           /* 必须有明确宽度，ellipsis 才生效 */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

### 37.1.2 多行省略

限制最多显示几行，超出部分显示省略号。经典写法依赖 `-webkit-box` 这一套老私有属性，兼容性好但目前属"事实标准"；新的 `line-clamp` 标准写法正在普及（`display: block` + `line-clamp`），可以两个都写、让新浏览器优先。

```css
.multi-line {
  /* 经典写法：兼容性最好 */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 新标准写法（Chrome 直接认，其他内核逐步跟进） */
.multi-line-modern {
  line-clamp: 3;
  overflow: hidden;
}
```

> ⚠️ **注意**：`-webkit-line-clamp` 一旦生效，元素就变成"按行截断的盒子"，此时不要再给它加 `height`，否则会和行高打架。

## 37.2 布局类

### 37.2.1 Flex居中

让子元素在容器里**水平+垂直双向居中**，是现代 CSS 里最短的居中方案。`justify-content` 管主轴、`align-items` 管交叉轴；只要容器本身有高度（或是个 flex 容器且父级给了高度），就能居中。

```css
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### 37.2.2 清除浮动

浮动元素会脱离常规流，导致父容器"高度塌陷"。三种清除方式按现代推荐度排序如下：

```css
/* 方案1：::after 伪元素（最常用）*/
.clearfix::after {
  content: "";
  display: block;
  clear: both;
}

/* 方案2：display: flow-root（现代简洁）*/
.parent { display: flow-root; }

/* 方案3：overflow: hidden（需注意裁剪问题）*/
.parent { overflow: hidden; }
```

> 💡 **怎么选**：新项目直接用 `display: flow-root`——它专门为"建立 BFC、包住浮动子元素"而生，副作用最小；老项目里大量存在的 `.clearfix` 伪元素写法继续用也没问题；`overflow: hidden` 能生效，但会顺手把溢出的内容（比如下拉菜单、阴影）裁掉，属于下策。

## 37.3 动画类

### 37.3.1 悬浮放大

鼠标移上去时把卡片稍微放大一点点，是提升"可点击感"的经典手法。`transition` 放在**常态**规则里，`transform` 放在 `:hover` 里，这样移入移出都有平滑过渡。

```css
.hover-scale {
  transition: transform 0.2s;
}
.hover-scale:hover {
  transform: scale(1.05);
}
```

> ⚠️ **别用 `width`/`height` 做放大**：那会触发整个页面重新布局（reflow），而 `transform` 只做合成层变换，性能好得多。

## 37.4 表单类

### 37.4.1 accent-color

一行代码就能把复选框、单选框、进度条等"原生控件"的主题色换成品牌色，不需要再写自定义组件。

```css
input[type="checkbox"] {
  accent-color: #3498db;
}
```

> 💡 **适用范围**：目前对 `checkbox`、`radio`、`range`、`progress` 生效；`<select>`、`<button>` 不一定买账，还是要靠自定义样式。

---

## 本章小结

收藏备用！

### 下章预告

下一章常见问题与坑！
