+++
title = "第30章 CSS动画"
weight = 300
date = "2026-03-27T16:53:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十章：CSS 动画

> CSS动画让你的网页从"静态图片"变成"动态电影"！transition和animation是CSS给你的"电影导演椅"，让元素按照你的剧本演出！

## 30.1 transition 过渡

### 30.1.1 transition-property——要过渡的属性名

`transition-property`指定哪些CSS属性需要过渡效果。比如背景色变化、尺寸变化等。

```css
/* 过渡单个属性 */
.transition-color {
  transition-property: background-color;
  transition-duration: 0.3s;
}

/* 过渡多个属性 */
.transition-multiple {
  transition-property: background-color, transform, opacity;
  transition-duration: 0.3s;
}

/* 所有属性（不推荐）*/
.transition-all {
  transition-property: all;
  transition-duration: 0.3s;
}
```

### 30.1.2 transition-duration——过渡时长

```css
/* 秒 */
.duration-s {
  transition-duration: 0.3s;
}

/* 毫秒 */
.duration-ms {
  transition-duration: 300ms;
}
```

### 30.1.3 transition-timing-function——缓动曲线

缓动曲线让动画有"加速度"感，更自然。

```css
.ease { transition-timing-function: ease; }
.linear { transition-timing-function: linear; }
.ease-in { transition-timing-function: ease-in; }
.ease-out { transition-timing-function: ease-out; }
.ease-in-out { transition-timing-function: ease-in-out; }
.bezier { transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); }
```

### 30.1.4 transition 缩写

```css
.shorthand {
  transition: all 0.3s ease 0s;
}
```

## 30.2 animation 动画

### 30.2.1 @keyframes 定义关键帧

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(0); }
}
```

### 30.2.2 animation-name——关联关键帧名称

```css
.animated {
  animation-name: fadeIn;
  animation-duration: 0.5s;
}
```

### 30.2.3 animation-duration——动画时长

```css
.duration {
  animation-duration: 0.5s;
}
```

### 30.2.4 animation-timing-function

缓动曲线控制动画的速度节奏——是"一脚油门踩到底"还是"犹豫三秒才迈步"。

```css
.ease { transition-timing-function: ease; }
.linear { transition-timing-function: linear; }
.ease-in { transition-timing-function: ease-in; }
.ease-out { transition-timing-function: ease-out; }
.ease-in-out { transition-timing-function: ease-in-out; }
.bezier { transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); }

/* steps() 是动画界的"定格动画模式"——不像正常动画那样平滑过渡，而是一顿一顿的，像翻书动画或老式胶片电影 */
.steps-4 { animation-timing-function: steps(4); }         /* 分4步跳过去 */
.steps-start { animation-timing-function: steps(4, start); } /* 第一步立即跳，不等周期 */
.steps-end { animation-timing-function: steps(4, end); }   /* 等第一帧过去再开始（默认） */
```

> 🎞️ `steps()` 特别适合做"逐帧动画"效果，比如闪烁的警告灯、像素风格的跑步小人。

### 30.2.5 animation-delay——延迟

```css
.delay {
  animation-delay: 0.2s;
}
```

### 30.2.5.1 animation-play-state——暂停/播放

控制动画是"正在演"还是"暂停卡住"，用 JavaScript 切换这个属性可以实现点击暂停/继续的效果。

```css
.running { animation-play-state: running; }  /* 播放中 */
.paused { animation-play-state: paused; }   /* 暂停，定格在当前帧 */
```

> 🎮 想象一下视频播放器：播放是 `running`，暂停是 `paused`——没错，CSS 动画也有自己的"空格键"！

### 30.2.6 animation-iteration-count——播放次数

```css
.loop { animation-iteration-count: infinite; }
.once { animation-iteration-count: 1; }
.three { animation-iteration-count: 3; }
```

### 30.2.7 animation-direction

`animation-direction` 控制动画的播放方向。

```css
.normal { animation-direction: normal; }          /* 从头到尾正常播放 */
.reverse { animation-direction: reverse; }        /* 倒着放，从尾到头 */
.alternate { animation-direction: alternate; }    /* 来回交替，正着→倒着→正着 */
.alternate-reverse { animation-direction: alternate-reverse; } /* 也是来回，但从尾巴开始 */
```

> 💡 想象你在看乒乓球赛：`alternate` 是从左边发球开始，`alternate-reverse` 是从右边发球开始。

### 30.2.8 animation-fill-mode

`animation-fill-mode` 决定动画在播放前和播放后（尤其是`animation-delay`期间）元素该长什么样。有点像是戏剧开场前和散场后演员的"候场姿势"。

```css
.none { animation-fill-mode: none; }           /* 默认，动画前后都恢复原始状态 */
.forwards { animation-fill-mode: forwards; }  /* 动画播完后，停在最后一帧（定格在结局） */
.backwards { animation-fill-mode: backwards; } /* 动画开始前，显示第一帧（提前进入角色） */
.both { animation-fill-mode: both; }           /* 前后都占便宜，开场前显示第一帧，结束后停在最后一帧 */
```

> 🎬 `forwards` 像是电影定格在最后一幕，`backwards` 像彩排时演员提前穿好了戏服候场。

### 30.2.9 animation 缩写

所有 `animation-*` 属性可以合并成一行简写，顺序很重要（记不住？没关系，浏览器有时候比你还宽容）：

```css
.animation {
  animation: name duration timing-function delay iteration-count direction fill-mode;
}
```

> ⚠️ 简写虽爽，但调试时容易被"隐藏的默认值"坑到——比如没写的 `animation-fill-mode` 默认是 `none`，而不是你以为的 `forwards`。

## 30.3 常用动画效果

### 30.3.1 淡入

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.fade-in { animation: fadeIn 0.5s ease-out forwards; }
```

### 30.3.2 滑入

```css
@keyframes slideIn {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.slide-in { animation: slideIn 0.5s ease-out forwards; }
```

### 30.3.3 脉冲

```css
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
.pulse { animation: pulse 1s ease-in-out infinite; }
```

### 30.3.4 旋转

```css
@keyframes spin {
  to { transform: rotate(360deg); }
}
.spin { animation: spin 1s linear infinite; }
```

## 30.4 性能优化

### 30.4.1 只动画 transform 和 opacity

浏览器的GPU对这两个属性"开绿灯"，动画丝滑且不吃性能，其他属性（比如 `width`、`background-color`）则会触发"重排"（reflow），代价昂贵。

```css
.fast-animation {
  transform: translateX(100px);
  opacity: 0.5;
}
```

### 30.4.2 will-change——提前告诉浏览器"我要动啦"

`will-change` 像是提前给浏览器打预防针："嘿，这个元素接下来要变身了，你先准备好硬件加速的资源。"

```css
.will-change {
  will-change: transform, opacity;  /* 提前申请GPU加速 */
}
```

> ⚠️ 别滥用！对每个动画元素都加 `will-change` 反而会适得其反——浏览器会为"预防性储备"消耗更多内存。只对确实需要加速的元素使用，且动画结束后记得移除。

---

## 本章小结

| 概念 | 说明 |
|-------|------|
| transition | 属性值变化的过渡效果 |
| @keyframes | 定义关键帧动画 |
| animation | 完整动画属性 |
| GPU加速 | transform/opacity性能最好 |

### 下章预告

下一章我们将学习滤镜与混合模式！

