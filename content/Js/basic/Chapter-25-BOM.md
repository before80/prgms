+++
title = "第 25 章 BOM"
weight = 250
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 25 章 BOM

> BOM——Browser Object Model，浏览器给 JavaScript 开的一扇窗！

## 25.1 window 对象

### 全局作用域

在浏览器环境中，`window` 对象是 JavaScript 的"全局老大"。所有全局变量和函数都是 `window` 的属性和方法。

```javascript
// 全局变量是 window 的属性
var globalVar = '我是全局变量';
let letVar = '我是 let 变量';

console.log('globalVar:', globalVar);  // 我是全局变量
console.log('window.globalVar:', window.globalVar);  // 我是全局变量

console.log('letVar:', letVar);  // 我是 let 变量
// console.log(window.letVar);  // undefined（let 不是 window 的属性）
```

```javascript
// 全局函数是 window 的方法
function greet(name) {
  return `你好，${name}！`;
}

console.log(greet('小明'));  // 你好，小明！
console.log(window.greet('小红'));  // 你好，小红！

// 两者等价！
```

```javascript
// var 和 function 声明会提升到 window
console.log('提升前:', typeof hoistedVar);  // undefined（var 声明会提升）
var hoistedVar = '我被提升了';

function hoistedFunc() {
  return '我也是函数声明，被提升了';
}

console.log(window.hoistedFunc());  // 我也是函数声明，被提升了
```

```javascript
// let/const 不会提升到 window
let notOnWindow = 'let 变量';
const alsoNotOnWindow = 'const 常量';

// console.log(window.notOnWindow);  // undefined
// console.log(window.alsoNotOnWindow);  // undefined
```

---

### innerWidth / innerHeight / outerWidth / outerHeight

这些属性告诉你浏览器窗口的尺寸。

```javascript
// innerWidth / innerHeight：视口（viewport）的尺寸
// 不包括地址栏、书签栏等浏览器 chrome
console.log('视口宽度:', window.innerWidth);   // 例如：1920
console.log('视口高度:', window.innerHeight);  // 例如：937

// outerWidth / outerHeight：整个浏览器窗口的尺寸
// 包括地址栏、书签栏等
console.log('窗口宽度:', window.outerWidth);   // 例如：1920
console.log('窗口高度:', window.outerHeight);  // 例如：1040
```

```javascript
// 响应式布局中使用
function handleResize() {
  const width = window.innerWidth;
  if (width < 768) {
    console.log('移动端视图');
  } else if (width < 1024) {
    console.log('平板视图');
  } else {
    console.log('桌面视图');
  }
}

window.addEventListener('resize', handleResize);
```

---

### window.open / close

```javascript
// window.open：打开新窗口
const newWindow = window.open('https://example.com', 'myWindow', 'width=800,height=600');

// 参数：
// 1. URL
// 2. 窗口名称（target）
// 3. 窗口特性（features）

// 关闭自己打开的窗口
// newWindow.close();

// 关闭当前窗口（大部分浏览器会阻止）
// window.close();
```

```javascript
// window.open 的第三个参数（features）
const features = [
  'width=800',           // 窗口宽度
  'height=600',          // 窗口高度
  'left=100',            // 距离屏幕左边
  'top=100',             // 距离屏幕顶部
  'menubar=yes',         // 显示菜单栏
  'toolbar=no',          // 不显示工具栏
  'location=no',         // 不显示地址栏
  'status=no',           // 不显示状态栏
  'resizable=yes',       // 可调整大小
  'scrollbars=yes'       // 显示滚动条
].join(',');

window.open('https://example.com', '_blank', features);
```

> 💡 **本章小结（第25章第1节）**
> 
> `window` 对象是浏览器中的全局对象，所有全局变量和函数都是它的属性和方法。`var` 声明的变量和 `function` 声明的函数会挂在 `window` 上，`let/const` 不会。`innerWidth/innerHeight` 是视口尺寸，`outerWidth/outerHeight` 是整个浏览器窗口的尺寸。`window.open/close` 可以打开和关闭窗口。

---

## 25.2 定时器

### setTimeout / clearTimeout：一次性定时

```javascript
// setTimeout：延迟执行一次
const timeoutId = setTimeout(() => {
  console.log('3秒后执行！');
}, 3000);

// 取消定时器
clearTimeout(timeoutId);
```

```javascript
// setTimeout 的参数
// setTimeout(callback, delay, ...args)
// callback: 回调函数
// delay: 延迟毫秒数（默认0）
// ...args: 传递给回调函数的参数

setTimeout((name, age) => {
  console.log(`${name}今年${age}岁了！`);
}, 1000, '小明', 18);
// 1秒后输出：小明今年18岁了！
```

```javascript
// setTimeout 的 this 问题
const obj = {
  name: '测试对象',
  greet() {
    console.log('this.name:', this.name);  // 这里的 this 指向什么？
  }
};

// 3秒后输出：this.name: undefined（因为 this 指向 window）
setTimeout(obj.greet, 3000);

// 解决方案1：bind
setTimeout(obj.greet.bind(obj), 3000);

// 解决方案2：箭头函数
setTimeout(() => obj.greet(), 3000);
```

```javascript
// setTimeout 的最小延迟
// 浏览器通常有最小延迟（约4ms），即使设置为0也会有延迟
console.time('setTimeout 0ms');
setTimeout(() => {
  console.timeEnd('setTimeout 0ms');  // 实际可能需要几毫秒
}, 0);
```

---

### setInterval / clearInterval：周期性定时

```javascript
// setInterval：每隔一段时间执行一次
const intervalId = setInterval(() => {
  console.log('每秒钟执行一次');
}, 1000);

// 停止定时器
clearInterval(intervalId);
```

```javascript
// setInterval 的典型应用：倒计时
function countdown(seconds) {
  let remaining = seconds;
  const intervalId = setInterval(() => {
    if (remaining > 0) {
      console.log(`倒计时：${remaining}秒`);
      remaining--;
    } else {
      console.log('时间到！');
      clearInterval(intervalId);
    }
  }, 1000);
}

countdown(5);
```

```javascript
// setInterval 的问题：不保证精确执行
// 如果主线程被阻塞，定时器可能会延迟
let count = 0;
const intervalId = setInterval(() => {
  count++;
  console.log(`第${count}次执行`);
}, 100);

// 模拟主线程阻塞
const start = Date.now();
while (Date.now() - start < 5000) {
  // 阻塞5秒
}
console.log('阻塞结束');
// 注意：这期间 setInterval 的回调会堆积，执行多次
```

---

### 最小延迟问题：浏览器最小为 4ms

```javascript
// 浏览器的定时器最小延迟
// HTML5 规范规定，嵌套（nested）的定时器最小延迟为 4ms
// 这意味着如果你在 setTimeout 回调中再次 setTimeout，即使设置为0也会有4ms延迟

// 嵌套层级越高，最小延迟越大
// 为了绕过这个限制，可以使用 requestAnimationFrame
```

```javascript
// 使用 setTimeout 模拟 setInterval（更精确）
function mySetInterval(callback, interval) {
  let timeoutId;

  function loop() {
    callback();
    timeoutId = setTimeout(loop, interval);
  }

  timeoutId = setTimeout(loop, interval);

  return {
    clear: () => clearTimeout(timeoutId)
  };
}

const timer = mySetInterval(() => {
  console.log('执行了！');
}, 100);

// 3秒后停止
setTimeout(() => timer.clear(), 3000);
```

---

### requestAnimationFrame / cancelAnimationFrame：动画帧

`requestAnimationFrame` 是浏览器提供的专门用于动画的 API，比 setInterval 更精确、更高效。

```javascript
// requestAnimationFrame：下一帧执行
function animate() {
  console.log('动画帧！');
  requestAnimationFrame(animate);
}

// 启动动画
const rafId = requestAnimationFrame(animate);

// 停止动画
cancelAnimationFrame(rafId);
```

```javascript
// 使用 requestAnimationFrame 实现动画
function animateBox(element, targetX, duration) {
  const startX = element.getBoundingClientRect().left;
  const startTime = performance.now();

  function step(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    // 缓动函数（ease-out）
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const currentX = startX + (targetX - startX) * easeOut;

    element.style.transform = `translateX(${currentX - startX}px)`;

    if (progress < 1) {
      requestAnimationFrame(step);
    }
  }

  requestAnimationFrame(step);
}

// 使用
const box = document.querySelector('.box');
animateBox(box, 500, 1000);  // 1秒内移动到500px
```

```javascript
// requestAnimationFrame vs setInterval
// setInterval: 可能掉帧，不保证在最佳时机执行
// requestAnimationFrame: 与浏览器刷新率同步，保证每帧最多执行一次

// 假设屏幕刷新率是60fps
// requestAnimationFrame 大约每16.67ms执行一次
// setInterval(16) 可能会有抖动
```

```javascript
// 判断元素是否在视口内
function isInViewport(element) {
  const rect = element.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

// 使用 requestAnimationFrame 检测滚动
function onScroll(callback) {
  let ticking = false;

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        callback();
        ticking = false;
      });
      ticking = true;
    }
  });
}

onScroll(() => {
  console.log('滚动了！');
});
```

> 💡 **本章小结（第25章第2节）**
> 
> BOM 定时器包括 `setTimeout/clearTimeout`（一次性）、`setInterval/clearInterval`（周期性）。定时器的最小延迟约 4ms，实际延迟可能更长。`requestAnimationFrame` 是专门为动画设计的 API，与浏览器刷新率同步，每帧最多执行一次，更精确更高效。对于动画，推荐使用 `requestAnimationFrame`。

---

## 25.3 location 对象

`location` 对象包含当前 URL 的信息，是 BOM 中最常用的对象之一。

```javascript
// location 的属性
console.log('完整URL:', location.href);        // https://example.com:8080/path/to/page?query=123#section
console.log('协议:', location.protocol);         // https:
console.log('主机名:', location.hostname);         // example.com
console.log('端口:', location.port);               // 8080
console.log('主机:', location.host);               // example.com:8080
console.log('路径:', location.pathname);           // /path/to/page
console.log('查询字符串:', location.search);       // ?query=123
console.log('锚点:', location.hash);               // #section
```

---

### href / protocol / host / hostname / pathname / search / hash

```javascript
// location.href：完整 URL（可读可写）
console.log('当前URL:', location.href);

// 跳转到新页面
// location.href = 'https://new-page.com';

// location.assign()：导航到新页面（会记录历史）
function goToPage(url) {
  location.assign(url);
}

// location.replace()：替换当前页面（不记录历史）
function replacePage(url) {
  location.replace(url);
}

// location.reload()：重新加载当前页面
function refreshPage() {
  location.reload();
  // location.reload(true); // 强制从服务器重新加载
}
```

```javascript
// 解析 URL 参数
function getQueryParams() {
  const params = {};
  const searchParams = new URLSearchParams(location.search);
  for (const [key, value] of searchParams) {
    params[key] = value;
  }
  return params;
}

// 假设 URL 是 /page?sort=name&order=asc
// getQueryParams() 返回 { sort: 'name', order: 'asc' }
```

```javascript
// 设置 URL 参数
function setQueryParam(key, value) {
  const url = new URL(location.href);
  url.searchParams.set(key, value);
  location.href = url.toString();
}

function addQueryParam(key, value) {
  const url = new URL(location.href);
  url.searchParams.append(key, value);
  location.href = url.toString();
}
```

---

### assign / replace / reload

```javascript
// assign：导航到新页面（可后退）
location.assign('https://example.com');
// 用户可以点击后退按钮返回

// replace：替换当前页面（不可后退）
location.replace('https://example.com');
// 用户无法点击后退按钮返回（当前页面被替换了）

// reload：重新加载当前页面
location.reload();
// 等同于点击刷新按钮
location.reload(true);
// true 表示强制从服务器重新加载（绕过缓存）
```

---

## 25.4 history 对象

`history` 对象提供了浏览器历史记录的访问能力。

```javascript
// history 的基本属性
console.log('历史记录数量:', history.length);  // 例如：42

// history 的方法
// history.back() - 后退一页
// history.forward() - 前进一页
// history.go(n) - 跳转到历史记录中的第n页
```

---

### back / forward / go

```javascript
// 后退一页
function goBack() {
  history.back();
}

// 前进一页
function goForward() {
  history.forward();
}

// 跳转到指定位置
// history.go(-2) - 后退两页
// history.go(3) - 前进三页
// history.go(0) - 刷新当前页

// 等价于
// history.go(0) === location.reload()
```

---

### pushState / replaceState

`pushState` 和 `replaceState` 是 HTML5 提供的 History API，可以在不刷新页面的情况下修改 URL。

```javascript
// pushState：添加新的历史记录
function pushState(url, title, data) {
  history.pushState(data, title, url);
}

// 示例：单页应用的路由
const routes = {
  '/': { title: '首页', template: '<h1>首页</h1>' },
  '/about': { title: '关于', template: '<h1>关于</h1>' },
  '/contact': { title: '联系', template: '<h1>联系</h1>' }
};

function navigate(path) {
  const route = routes[path];
  if (route) {
    document.title = route.title;
    document.getElementById('app').innerHTML = route.template;
    history.pushState(null, route.title, path);
  }
}

// 监听 popstate（点击后退/前进按钮时触发）
window.addEventListener('popstate', (event) => {
  const path = location.pathname;
  navigate(path);
});

// 监听链接点击
document.addEventListener('click', (e) => {
  if (e.target.matches('a[data-link]')) {
    e.preventDefault();
    navigate(e.target.href);
  }
});
```

```javascript
// replaceState：替换当前历史记录
function replaceState(url, title, data) {
  history.replaceState(data, title, url);
}

// 使用场景：表单提交后替换当前历史记录
// 防止用户点击后退按钮回到已提交的表单
```

```javascript
// pushState/replaceState 的区别
// pushState：创建新的历史记录（可后退）
history.pushState({ pageId: 1 }, 'Page 1', '/page1');
history.pushState({ pageId: 2 }, 'Page 2', '/page2');
history.back();  // 回到 /page1

// replaceState：替换当前历史记录（不可后退到替换前）
history.replaceState({ pageId: 1 }, 'Page 1', '/page1');
history.replaceState({ pageId: 2 }, 'Page 2', '/page2');
history.back();  // 回到 /page1（不是替换前的页面）
```

> 💡 **本章小结（第25章第3-4节）**
> 
> `location` 对象包含 URL 的所有信息：`href`、`protocol`、`host`、`hostname`、`pathname`、`search`、`hash`。`location.assign()` 导航到新页面（可后退），`location.replace()` 替换当前页面（不可后退），`location.reload()` 重新加载页面。`history` 对象提供历史记录访问能力，`pushState/replaceState` 可以在不刷新页面的情况下修改 URL，是单页应用（SPA）路由的基础。

---

## 25.5 navigator 与 screen

### userAgent / platform

`navigator` 对象包含浏览器的信息。

```javascript
// navigator.userAgent：用户代理字符串
console.log('用户代理:', navigator.userAgent);
// Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36

// 注意：不要用 userAgent 来判断浏览器类型
// 应该使用功能检测
```

```javascript
// navigator.platform：平台信息
console.log('平台:', navigator.platform);  // Win32

// navigator.appName / appVersion（已废弃）
console.log('App名称:', navigator.appName);    // Netscape
console.log('App版本:', navigator.appVersion);  // 5.0 (Windows...)
```

```javascript
// 检测用户设备类型
function getDeviceType() {
  const ua = navigator.userAgent.toLowerCase();
  if (/mobile|android|iphone|ipad|tablet/.test(ua)) {
    return 'mobile';
  }
  return 'desktop';
}

console.log('设备类型:', getDeviceType());
```

---

### screen.width / height / availWidth / availHeight

`screen` 对象包含屏幕的信息。

```javascript
// screen.width / height：屏幕分辨率
console.log('屏幕宽度:', screen.width);   // 1920
console.log('屏幕高度:', screen.height);  // 1080

// screen.availWidth / availHeight：可用区域（不包括任务栏等）
console.log('可用宽度:', screen.availWidth);   // 1920
console.log('可用高度:', screen.availHeight);  // 1040
```

```javascript
// 居中弹窗计算
function openCenteredWindow(url, width, height) {
  const left = (screen.availWidth - width) / 2;
  const top = (screen.availHeight - height) / 2;
  const features = `width=${width},height=${height},left=${left},top=${top}`;
  window.open(url, '_blank', features);
}

openCenteredWindow('https://example.com', 800, 600);
```

---

## 25.6 其他

### print()：打印页面

```javascript
// 打印当前页面
function printPage() {
  window.print();
}

// 监听打印事件
window.addEventListener('beforeprint', () => {
  console.log('即将打印...');
  // 可以在这里隐藏不需要打印的元素
});

window.addEventListener('afterprint', () => {
  console.log('打印完成');
  // 可以在这里恢复元素
});
```

---

### matchMedia()：媒体查询

```javascript
// matchMedia：检查媒体查询
const mediaQuery = window.matchMedia('(min-width: 768px)');

console.log('匹配状态:', mediaQuery.matches);  // true 或 false
console.log('媒体查询:', mediaQuery.media);    // (min-width: 768px)

// 添加监听
function handleMediaChange(e) {
  if (e.matches) {
    console.log('现在是桌面视图');
  } else {
    console.log('现在是移动视图');
  }
}

mediaQuery.addEventListener('change', handleMediaChange);
```

```javascript
// 常用媒体查询
const queries = {
  mobile: window.matchMedia('(max-width: 767px)'),
  tablet: window.matchMedia('(min-width: 768px) and (max-width: 1023px)'),
  desktop: window.matchMedia('(min-width: 1024px)'),
  portrait: window.matchMedia('(orientation: portrait)'),
  landscape: window.matchMedia('(orientation: landscape)'),
  dark: window.matchMedia('(prefers-color-scheme: dark)'),
  light: window.matchMedia('(prefers-color-scheme: light)'),
  reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)')
};

// 检测深色模式
if (queries.dark.matches) {
  document.body.classList.add('dark-mode');
}
```

---

### crossOriginIsolated：跨域隔离状态

```javascript
// crossOriginIsolated：页面是否处于跨域隔离状态
console.log('跨域隔离:', window.crossOriginIsolated);  // true 或 false

// 当 crossOriginIsolated 为 true 时，可以使用 SharedArrayBuffer
// SharedArrayBuffer 用于 Web Workers 之间共享内存
// 由于 Spectre 漏洞，默认是禁用的，需要正确配置 CORS 头才能启用
```

```javascript
// 检查 SharedArrayBuffer 是否可用
if (typeof SharedArrayBuffer !== 'undefined') {
  console.log('SharedArrayBuffer 可用');
} else {
  console.log('SharedArrayBuffer 不可用（需要跨域隔离）');
}

// 或者
if (window.crossOriginIsolated) {
  console.log('可以创建 SharedArrayBuffer');
}
```

> 💡 **本章小结（第25章第5-6节）**
> 
> `navigator` 对象提供浏览器和用户环境的信息，如 `userAgent`（用户代理）、`platform`（平台）。`screen` 对象提供屏幕信息，如 `width/height`（分辨率）、`availWidth/availHeight`（可用区域）。其他 BOM 功能包括 `print()` 打印页面、`matchMedia()` 媒体查询、`crossOriginIsolated` 跨域隔离状态。合理使用这些 API 可以实现响应式布局、设备检测、打印优化等功能。

---

## 本章小结（第25章）

### 1. window 对象
- 全局作用域，`var` 和 `function` 声明是 `window` 的属性
- `innerWidth/innerHeight` 视口尺寸，`outerWidth/outerHeight` 窗口尺寸
- `window.open/close` 打开关闭窗口

### 2. 定时器
- `setTimeout/clearTimeout`：一次性定时
- `setInterval/clearInterval`：周期性定时
- `requestAnimationFrame`：动画帧，最精确的动画 API
- 定时器最小延迟约 4ms

### 3. location 对象
- `href/protocol/host/hostname/pathname/search/hash`
- `assign()`：导航（可后退）
- `replace()`：替换（不可后退）
- `reload()`：重新加载

### 4. history 对象
- `back/forward/go`：历史记录导航
- `pushState`：添加历史记录（可后退）
- `replaceState`：替换历史记录（不可后退）

### 5. navigator 与 screen
- `navigator.userAgent/platform`：浏览器和平台信息
- `screen.width/height/availWidth/availHeight`：屏幕信息

### 6. 其他
- `print()`：打印页面
- `matchMedia()`：媒体查询
- `crossOriginIsolated`：跨域隔离状态

### 记忆口诀
```
BOM 是浏览器的窗口，
window 是全局老大，
location 管地址，
history 管历史，
navigator 报信息，
screen 报屏幕，
定时器要记牢，
动画用 RAF 最可靠！
```