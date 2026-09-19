+++
title = "第 26 章 DOM 基础"
weight = 260
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 26 章 DOM 基础

> DOM——Document Object Model，JavaScript 操作网页的桥梁！

## 26.1 DOM 概述

### DOM（Document Object Model）：文档对象模型

**DOM** 是一种让程序访问和操作 HTML/XML 文档的接口。简单来说，DOM 就是浏览器把 HTML 文档解析成一棵树，JavaScript 可以通过这棵树来"操控"网页。

```html
<!DOCTYPE html>
<html>
<head>
  <title>我的网页</title>
</head>
<body>
  <h1>Hello World</h1>
  <p>这是一个段落</p>
</body>
</html>
```

```mermaid
graph TD
    A["document"] --> B["html"]
    B --> C["head"]
    C --> D["title"]
    D --> E["文本: 我的网页"]
    B --> F["body"]
    F --> G["h1"]
    G --> H["文本: Hello World"]
    F --> I["p"]
    I --> J["文本: 这是一个段落"]
```

---

### DOM Tree：树形结构，根节点是 document

```javascript
// DOM 树的基本结构
// document 是 DOM 树的根节点
console.log('根节点:', document);  // #document

// document 的父节点是 null
console.log('document.parentNode:', document.parentNode);  // null

// document.documentElement 是 <html> 元素
console.log('html元素:', document.documentElement);  // <html>...</html>

// document.body 是 <body> 元素
console.log('body元素:', document.body);  // <body>...</body>
```

---

### Node 类型：元素(1) / 属性(2) / 文本(3) / 注释(8) / document(9) / DocumentFragment(11)

DOM 规范定义了 12 种节点类型，常用的有：

| 类型 | 值 | 说明 |
|------|-----|------|
| Element | 1 | HTML 元素 |
| Attr | 2 | 属性节点（仍存在，但不再出现在子节点列表里，日常几乎不用） |
| Text | 3 | 文本节点 |
| Comment | 8 | 注释 |
| Document | 9 | document 对象 |
| DocumentFragment | 11 | 文档片段 |

> ⚠️ 关于 `Attr` 的一个常见误解：属性并不是「被删掉的概念」，而是从 DOM4 开始**属性节点不再继承自 `Node`，也不会作为子节点出现**：
>
> ```javascript
> const div = document.createElement('div');
> div.title = '提示';
> const attr = div.getAttributeNode('title');
> console.log(attr.nodeType);      // 2（仍然有 nodeType）
> console.log(attr.parentNode);    // null（不属于 DOM 树）
> console.log(div.childNodes.length); // 0（属性不算子节点）
> ```
>
> 日常操作属性直接用 `getAttribute` / `setAttribute` / `dataset` 就够了，见第 27 章。

```javascript
// 检测节点类型
const element = document.createElement('div');
const textNode = document.createTextNode('Hello');
const comment = document.createComment('这是一条注释');

console.log('元素节点类型:', element.nodeType);  // 1
console.log('文本节点类型:', textNode.nodeType);  // 3
console.log('注释节点类型:', comment.nodeType);  // 8
console.log('document节点类型:', document.nodeType);  // 9
```

---

### NodeType 值

```javascript
// NodeType 的常量（Node.ELEMENT_NODE 等）
console.log('ELEMENT_NODE:', Node.ELEMENT_NODE);         // 1
console.log('TEXT_NODE:', Node.TEXT_NODE);               // 3
console.log('COMMENT_NODE:', Node.COMMENT_NODE);         // 8
console.log('DOCUMENT_NODE:', Node.DOCUMENT_NODE);       // 9
console.log('DOCUMENT_FRAGMENT_NODE:', Node.DOCUMENT_FRAGMENT_NODE);  // 11

// 使用常量判断节点类型
if (element.nodeType === Node.ELEMENT_NODE) {
  console.log('这是一个元素节点');
}
```

> 💡 **本章小结（第26章第1节）**
> 
> DOM（Document Object Model）是访问和操作 HTML/XML 文档的接口。浏览器把 HTML 解析成一棵树（DOM Tree），根节点是 `document`。树上有不同类型的节点：元素节点（1）、文本节点（3）、注释节点（8）、document 节点（9）等。每个节点都有 `nodeType` 属性标识类型。

---

## 26.2 选择元素

### getElementById：通过 ID 获取（最快，浏览器内部有索引）

```javascript
// getElementById：根据 ID 获取单个元素
// ID 在 HTML 中应该是唯一的
const header = document.getElementById('header');
console.log('header:', header);

// 如果找不到元素，返回 null
const nonExistent = document.getElementById('non-existent');
console.log('不存在的元素:', nonExistent);  // null
```

```javascript
// 注意：ID 区分大小写
// <div id="myId"> vs <div id="MyId"> 是不同的 ID
```

```javascript
// getElementById 是最高效的选择方法
// 主流浏览器内部为 ID 维护了索引，查找接近 O(1)；
// 规范并没有强制要求这样做，但无论如何它都是最快的选择方式。
// 代价是它只能按 ID 找，表达式能力最弱
```

---

### getElementsByClassName / getElementsByTagName：返回 HTMLCollection（动态集合）

```javascript
// getElementsByClassName：根据类名获取元素集合
const buttons = document.getElementsByClassName('btn');
console.log('按钮数量:', buttons.length);  // HTMLCollection 是动态的

// HTMLCollection 可以用索引访问
console.log('第一个按钮:', buttons[0]);

// HTMLCollection 有 namedItem 方法
// const submitBtn = buttons.namedItem('submit');
```

```javascript
// getElementsByTagName：根据标签名获取元素集合
const allDivs = document.getElementsByTagName('div');
const allLinks = document.getElementsByTagName('a');

console.log('div 数量:', allDivs.length);
console.log('链接数量:', allLinks.length);
```

```javascript
// HTMLCollection 是动态的！
// 当 DOM 变化时，集合会自动更新
const items = document.getElementsByClassName('item');

console.log('初始数量:', items.length);  // 例如：3

// 添加一个新元素
const newItem = document.createElement('div');
newItem.className = 'item';
document.body.appendChild(newItem);

console.log('添加后数量:', items.length);  // 自动变成 4！
```

```javascript
// HTMLCollection 不是数组！
// 它有 length 属性，可以用索引访问
// 但没有数组的方法（如 forEach、map 等）

const elements = document.getElementsByClassName('item');
// elements.forEach(...)  // 报错！HTMLCollection 没有 forEach

// 需要转成数组
const array = Array.from(elements);
// 或者
const array2 = [...elements];
```

---

### querySelector / querySelectorAll：CSS 选择器，返回 NodeList（多为静态）

```javascript
// querySelector：获取第一个匹配的元素
const firstButton = document.querySelector('.btn');
const submitBtn = document.querySelector('#submit-btn');
const activeLink = document.querySelector('a.active');
```

```javascript
// querySelectorAll：获取所有匹配的元素
const allButtons = document.querySelectorAll('.btn');
const allInputs = document.querySelectorAll('input[type="text"]');

// NodeList 支持 forEach
allButtons.forEach(btn => {
  console.log(btn.textContent);
});
```

```javascript
// NodeList vs HTMLCollection
// 判断「动态」还是「静态」，看的是来源，而不是类名：
// - querySelectorAll → NodeList，静态快照
// - childNodes        → NodeList，但是【动态】的
// - getElementsBy* / children → HTMLCollection，动态的

// 静态：拿到之后 DOM 再变，集合不变
const staticList = document.querySelectorAll('.item');

// 动态：DOM 一变，集合跟着变（下面以 #list 的子节点为例）
const listEl = document.getElementById('list');
const liveList = listEl.childNodes;
console.log(liveList.length);   // 假设是 2

const item = document.createElement('div');
item.className = 'item';
listEl.appendChild(item);       // 往被观察的容器里插节点

console.log(staticList.length); // 不变，仍是查询那一刻的快照
console.log(liveList.length);   // 变成 3，动态集合立即反映了变化
```

```javascript
// NodeList 有 forEach 方法
const elements = document.querySelectorAll('div.container');
elements.forEach((el, index) => {
  console.log(`div #${index}:`, el.className);
});

// NodeList 转数组
const array = Array.from(elements);
// 或
const array2 = [...elements];
```

---

### HTMLCollection vs NodeList 对比

| 特性 | HTMLCollection | NodeList |
|------|----------------|----------|
| 来源 | getElementsBy* | querySelectorAll |
| 动态性 | 动态 | 多为静态（querySelectorAll） |
| forEach | 无 | 有 |
| 数组方法 | 无 | 部分支持（forEach） |
| namedItem | 有 | 无 |

```javascript
// HTMLCollection 示例
const htmlCollection = document.getElementsByClassName('item');

// NodeList 示例
const nodeList = document.querySelectorAll('.item');

// HTMLCollection 没有 forEach
// htmlCollection.forEach(...)  // 报错

// NodeList 有 forEach
nodeList.forEach((el) => {
  console.log(el.textContent);
});
```

### 动态集合必须小心：边遍历边修改会出错

```javascript
// ❌ 用动态集合边删边遍历，会跳过元素
const liveItems = document.getElementsByClassName('item'); // 动态集合
for (let i = 0; i < liveItems.length; i++) {
  liveItems[i].remove();   // 删除后集合立即缩短，i 却继续累加 → 漏掉一半元素
}

// ✅ 先转成静态数组再操作
const snapshot = Array.from(document.getElementsByClassName('item'));
snapshot.forEach((el) => el.remove());

// ✅ querySelectorAll 返回的就是静态快照，可以直接遍历
document.querySelectorAll('.item').forEach((el) => el.remove());
```

### 其他常用节点判断与查找

```javascript
// matches：判断当前元素是否匹配某个选择器（只判断自己，不含祖先）
const link = document.querySelector('a');
console.log(link.matches('.nav > a'));        // true / false

// closest：从自己开始向上找最近的匹配祖先（包含自己）
console.log(link.closest('.nav'));            // 最近的 .nav 祖先，找不到返回 null

// 事件委托里最常用的一对组合
document.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-action]');
  if (!button) return;
  console.log('点击了操作按钮：', button.dataset.action);
});

// isConnected：节点当前是否在文档中（比 document.contains 更直观）
const detached = document.createElement('div');
console.log(detached.isConnected);            // false
document.body.appendChild(detached);
console.log(detached.isConnected);            // true
```

### querySelectorAll 的作用范围：不包含自己

```javascript
const box = document.querySelector('.box');

// 只在 box 的子孙里查找，不会匹配 box 本身
console.log(box.querySelectorAll('.box').length); // 0（如果只有它自己带 .box）

// 想包含自身，用 matches 或从父节点查
console.log(box.matches('.box'));                 // true
```

> 💡 **本章小结（第26章第2节）**
> 
> 选择元素有四种方法：`getElementById`（最快，O(1)）、`getElementsByClassName`（返回动态 HTMLCollection）、`getElementsByTagName`（返回动态 HTMLCollection）、`querySelector/querySelectorAll`（CSS 选择器，返回 NodeList）。HTMLCollection 是动态的，会随 DOM 变化自动更新；NodeList（querySelectorAll 返回的）大多是静态的。NodeList 有 `forEach`，HTMLCollection 没有。

---

## 26.3 遍历节点

### 节点树遍历：parentNode / childNodes / firstChild / lastChild / nextSibling / previousSibling

这些属性遍历所有节点（包括文本节点和注释）。

```html
<div id="container">
  <!-- 这是一个注释 -->
  <p>第一段</p>
  <p>第二段</p>
</div>
```

```javascript
const container = document.getElementById('container');

// parentNode：父节点
console.log('父节点:', container.parentNode);

// childNodes：所有子节点（文本、元素、注释等）
console.log('子节点数量:', container.childNodes.length);
// 7：换行缩进产生的空白文本 + 注释 + 空白文本 + p + 空白文本 + p + 末尾空白文本
// 很多人以为只有 5 个，正是忽略了空白文本节点

// 只算元素就简单多了
console.log('子元素数量:', container.children.length);  // 2

// firstChild：第一个子节点
console.log('第一个子节点:', container.firstChild);  // 可能是空白文本节点

// lastChild：最后一个子节点
console.log('最后一个子节点:', container.lastChild);  // 可能是空白文本节点

// nextSibling：下一个兄弟节点
console.log('下一个兄弟:', container.nextSibling);

// previousSibling：上一个兄弟节点
console.log('上一个兄弟:', container.previousSibling);
```

---

### 元素树遍历：parentElement / children / firstElementChild / lastElementChild / nextElementSibling / previousElementSibling

这些属性只遍历元素节点，不包括文本节点和注释。

```javascript
const container = document.getElementById('container');

// parentElement：父元素
console.log('父元素:', container.parentElement);

// children：所有子元素
console.log('子元素数量:', container.children.length);  // 2（两个 p 标签）

// firstElementChild：第一个子元素
console.log('第一个子元素:', container.firstElementChild);  // 第一个 <p>

// lastElementChild：最后一个子元素
console.log('最后一个子元素:', container.lastElementChild);  // 第二个 <p>

// nextElementSibling：下一个兄弟元素
console.log('下一个兄弟元素:', container.nextElementSibling);

// previousElementSibling：上一个兄弟元素
console.log('上一个兄弟元素:', container.previousElementSibling);
```

---

### childNodes（含文本节点）vs children（仅元素节点）对比

```javascript
const ul = document.querySelector('ul');

console.log('childNodes 数量:', ul.childNodes.length);  // 包括空白文本节点
console.log('children 数量:', ul.children.length);       // 只有元素

// 遍历 childNodes（包含所有节点）
ul.childNodes.forEach(node => {
  if (node.nodeType === Node.ELEMENT_NODE) {
    console.log('元素节点:', node.tagName);
  } else if (node.nodeType === Node.TEXT_NODE) {
    console.log('文本节点:', node.textContent.trim());
  }
});
```

---

### firstChild vs firstElementChild 对比

```html
<ul>
  <li>第一项</li>
  <li>第二项</li>
</ul>
```

```javascript
const ul = document.querySelector('ul');

// firstChild：可能是空白文本节点（因为 ul 和第一个 li 之间可能有空白）
const first = ul.firstChild;
console.log('firstChild:', first);  // 可能是 #text（空白）

// firstElementChild：一定是第一个元素
const firstElement = ul.firstElementChild;
console.log('firstElementChild:', firstElement);  // <li>第一项</li>
```

```mermaid
graph LR
    A["遍历方式"] --> B["节点树"]
    A --> C["元素树"]
    
    B --> B1["parentNode"]
    B --> B2["childNodes"]
    B --> B3["firstChild / lastChild"]
    B --> B4["nextSibling / previousSibling"]
    
    C --> C1["parentElement"]
    C --> C2["children"]
    C --> C3["firstElementChild / lastElementChild"]
    C --> C4["nextElementSibling / previousElementSibling"]
```

---

## 26.4 节点属性

### nodeName / nodeType / nodeValue

```javascript
// nodeName：节点名称
const div = document.createElement('div');
const text = document.createTextNode('Hello');
const comment = document.createComment('注释');

console.log('元素节点名称:', div.nodeName);    // DIV
console.log('文本节点名称:', text.nodeName);   // #text
console.log('注释节点名称:', comment.nodeName); // #comment

// 对于元素节点，nodeName 等于 tagName
console.log('tagName:', div.tagName);  // DIV
```

```javascript
// nodeType：节点类型
console.log('元素节点类型:', Node.ELEMENT_NODE);   // 1
console.log('文本节点类型:', Node.TEXT_NODE);      // 3
console.log('注释节点类型:', Node.COMMENT_NODE);   // 8
console.log('文档节点类型:', Node.DOCUMENT_NODE);  // 9
```

```javascript
// nodeValue：节点的值
// 对于文本节点，nodeValue 是文本内容
// 对于元素节点，nodeValue 是 null
const textNode = document.createTextNode('Hello World');
console.log('文本节点值:', textNode.nodeValue);  // Hello World

const elem = document.createElement('div');
console.log('元素节点值:', elem.nodeValue);  // null
```

---

### textContent：纯文本内容

```javascript
// textContent：获取或设置元素的纯文本内容
// 会忽略所有 HTML 标签

const container = document.createElement('div');
container.innerHTML = '<p>Hello <strong>World</strong></p>';

console.log('textContent:', container.textContent);  // Hello World
console.log('innerHTML:', container.innerHTML);     // <p>Hello <strong>World</strong></p>
```

```javascript
// 设置 textContent 会替换所有子节点
const div = document.createElement('div');
div.innerHTML = '<p>第一段</p><p>第二段</p>';
console.log('初始:', div.innerHTML);

div.textContent = '纯文本';
console.log('设置后:', div.innerHTML);  // 纯文本（HTML 标签被移除了）
```

```javascript
// textContent vs innerText
// textContent：获取所有文本，包括隐藏元素的文本
// innerText：只获取可见文本，会忽略 display: none 的元素

const div = document.createElement('div');
div.innerHTML = '<span style="display:none">隐藏</span>可见';
console.log('textContent:', div.textContent);  // "隐藏可见"（不受样式影响）
console.log('innerText:', div.innerText);      // 这个元素还没插入文档
// 未渲染的元素无法计算可见性，此时 innerText 会退化成 textContent，同样输出 "隐藏可见"

// 插入文档后才能真正体现差异（display:none 的内容会被跳过）
document.body.appendChild(div);
console.log('innerText（在文档中）:', div.innerText);  // "可见"
```

两者的取舍很清楚：

| | `textContent` | `innerText` |
| --- | --- | --- |
| 是否受 CSS 影响 | 否，返回全部文本 | 是，跳过不可见内容 |
| 是否触发排版计算 | 否，速度快 | **是**，会强制浏览器计算布局，慢 |
| 对空白与换行的处理 | 原样保留 | 会按渲染结果折叠 |
| 推荐用途 | 读取/设置纯文本、防 XSS | 确实需要「用户看到的文字」时 |

**默认用 `textContent`**：它更快，而且设置时不会解析 HTML，天然避免 XSS。

```javascript
// 安全考虑：使用 textContent 而不是 innerHTML 来设置用户输入
// 可以防止 XSS 攻击

function safeSetText(element, userInput) {
  element.textContent = userInput;  // 用户输入被当作纯文本
  // 如果用 innerHTML = userInput，可能导致 XSS
}
```

> 💡 **本章小结（第26章第3-4节）**
> 
> DOM 遍历有两种方式：**节点树遍历**（包括文本节点）和**元素树遍历**（只包括元素）。`childNodes` 包含空白文本节点，`children` 只有元素。`firstChild` 可能是空白文本，`firstElementChild` 一定是第一个元素。节点属性包括 `nodeName`（节点名称）、`nodeType`（节点类型）、`nodeValue`（节点值）、`textContent`（纯文本内容）。使用 `textContent` 设置用户输入更安全，可以防止 XSS。

---

## 本章小结（第26章）

### 1. DOM 概述
- DOM（Document Object Model）是访问和操作 HTML 文档的接口
- 浏览器把 HTML 解析成 DOM 树，根节点是 `document`
- 节点类型：元素(1)、文本(3)、注释(8)、document(9) 等

### 2. 选择元素
- `getElementById`：最快（浏览器内部有 ID 索引），返回单个元素或 `null`
- `getElementsByClassName/getElementsByTagName`：返回动态 HTMLCollection
- `querySelector/querySelectorAll`：CSS 选择器，返回 NodeList
- **动态还是静态看来源**：`querySelectorAll` 是静态快照；`getElementsBy*`、`children`、`childNodes` 都是动态的
- 动态集合不能边遍历边删，先 `Array.from` 转成快照再操作
- `matches` 判断自身是否匹配选择器，`closest` 从自身向上找最近祖先；`isConnected` 判断是否在文档中

### 3. 遍历节点
- 节点树：`parentNode`、`childNodes`、`firstChild`、`lastChild`、`nextSibling`、`previousSibling`
- 元素树：`parentElement`、`children`、`firstElementChild`、`lastElementChild`、`nextElementSibling`、`previousElementSibling`
- `childNodes` 包含空白文本节点，`children` 只有元素

### 4. 节点属性
- `nodeName`：节点名称（元素返回标签名）
- `nodeType`：节点类型（1=元素，3=文本，8=注释，9=document）
- `nodeValue`：节点值（元素为 null，文本为内容）
- `textContent`：纯文本内容，速度快、不受样式影响，设置时不会解析 HTML
- `innerText`：返回渲染后可见的文字，会触发排版计算，只在确需「用户看到的文字」时使用

### 记忆口诀
```
DOM 是网页的树，
document 是根，
节点类型要记清，
选择元素用哪个快？
getElementById 最快，
querySelectorAll 最灵活，
遍历要用元素树，
childNodes 有文本！
```
