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

在浏览器环境中，`window` 对象是 JavaScript 的"全局老大"：它同时也是 ECMAScript 规范里的全局对象（也就是 `globalThis`）。

不过要注意一个常见误会——**不是所有"顶层声明"都会变成 `window` 的属性**：`var` 和函数声明会，`let`、`const`、`class` 不会。

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
// var 和 function 声明会挂到 window 上
console.log('访问 hoistedVar:', typeof hoistedVar);  // 'undefined'
// 这里没报错、而是打印出字符串 'undefined'，
// 是因为 var 声明被提升后已存在，只是还没赋值。

var hoistedVar = '我被提升了';

function hoistedFunc() {
  return '我也是函数声明，被提升了';
}

console.log(window.hoistedFunc());   // 我也是函数声明，被提升了
console.log(window.hoistedVar);      // 我被提升了
```

```javascript
// let / const / class 不会挂到 window 上
let notOnWindow = 'let 变量';
const alsoNotOnWindow = 'const 常量';
class AlsoNotOnWindow {}

console.log(window.notOnWindow);         // undefined
console.log(window.alsoNotOnWindow);     // undefined
console.log(window.AlsoNotOnWindow);     // undefined

// 但它们仍然是"全局作用域"里的变量，任何地方都能直接访问：
console.log(notOnWindow);                // let 变量

// ⭐ 两者的关键区别：var 会覆盖 window 上的同名内置属性，let 不会报错但会遮蔽
// 例如 window.name 是浏览器的内置属性，用 var name = 'x' 会直接改掉它，
// 而 let name = 'x' 只是在全局作用域里遮蔽，不会碰 window.name。
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
// setTimeout 的 this 问题（经典坑！）
const obj = {
  name: '测试对象',
  greet() {
    console.log('this.name:', this.name);
  }
};

// obj.greet()  → this.name: 测试对象
// 但下面这行结果完全不一样：
setTimeout(obj.greet, 3000);
// 3秒后输出：this.name:        ← 注意是"空"的
//
// 为什么不是 undefined？因为回调是以"普通函数调用"的方式执行的，
// 非严格模式下 this 指向全局对象 window，
// 而 window.name 恰好是浏览器内置的一个字符串属性，默认值是空字符串 ''。
// 也就是说这里拿到了 window.name，而不是 obj.name。
// （如果脚本是 ES Module 或严格模式，this 是 undefined，会直接 TypeError）

// 解决方案1：bind 锁定 this
setTimeout(obj.greet.bind(obj), 3000);

// 解决方案2：用箭头函数包一层（最常用）
setTimeout(() => obj.greet(), 3000);

// 解决方案3：提前写成一个不依赖 this 的函数
const greet = obj.greet.bind(obj);
setTimeout(greet, 3000);
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
// setInterval 的问题：不保证精确执行，而且会"丢拍"
let count = 0;
const intervalId = setInterval(() => {
  count++;
  console.log(`第${count}次执行`);
}, 100);

// 模拟主线程阻塞 5 秒
const start = Date.now();
while (Date.now() - start < 5000) {
  // 死循环占住主线程
}
console.log('阻塞结束');

// ⭐ 常见误解："这 5 秒里回调会排队 50 次，然后一次性全打印出来"。
// 事实并非如此。定时器任务不会被重复入队，
// 解阻塞后浏览器只会补跑一次回调，然后按 100ms 继续。
// 也就是说它丢掉了约 49 次执行机会——这正是 setInterval 做倒计时会"越走越慢"的原因。

// ⭐ 更严重的问题：如果回调自己耗时超过 interval，
// 上一次还没跑完下一次就来了，回调会重叠执行，造成逻辑错乱。

// 所以需要用"等上一次跑完再排下一次"的写法（见下一小节）。
```

---

### 最小延迟问题：浏览器最小为 4ms

```javascript
// 浏览器的定时器最小延迟
// HTML 规范规定：连续嵌套超过 5 层的定时器，最小延迟被钳制为 4ms。
// 也就是说，在 setTimeout 回调里再写 setTimeout(..., 0)，
// 第 6 层往后每次至少会等 4ms，而不是"立刻"。

// ⚠️ 常见误解："嵌套越深，延迟越大（8ms、16ms 一路涨上去）"。
// 事实是它稳定在 4ms 这条下限，不会再继续变大。
// 另外，页面处于后台标签页时，定时器还会被进一步节流到 1 秒甚至更久，
// 所以千万不要用定时器做精确计时（计时请用 performance.now() 记录真实时间）。
```

```javascript
// 用 setTimeout 模拟 setInterval：等上一次执行完再排下一次
// 好处是一能避免回调重叠，二能避免长时间阻塞后的"丢拍"错位。
function mySetInterval(callback, interval) {
  let timeoutId = null;
  let stopped = false;

  async function loop() {
    if (stopped) return;
    try {
      await callback();            // 支持 async 回调：等它真正跑完
    } finally {
      if (!stopped) {
        timeoutId = setTimeout(loop, interval);   // 跑完才排下一次
      }
    }
  }

  timeoutId = setTimeout(loop, interval);

  return {
    clear() {
      stopped = true;
      clearTimeout(timeoutId);
    }
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

`requestAnimationFrame` 是浏览器提供的专门用于动画的 API：它在浏览器"下一次重绘之前"调用你的回调，天然跟屏幕刷新率对齐，比 setInterval 更平滑、更省电。

```javascript
// requestAnimationFrame：回调会在下一次重绘前执行
// 它会把一个高精度时间戳（performance.now() 同源）作为参数传进来
let rafId = null;

function animate(timestamp) {
  console.log('动画帧，时间戳：', timestamp);
  rafId = requestAnimationFrame(animate);   // 继续排下一帧
}

// 启动动画（真正的启动时机由浏览器决定）
rafId = requestAnimationFrame(animate);

// 停止动画：必须在"下一帧真正执行之前"取消才有效
// 实际项目里通常这样收尾：
// function stop() {
//   cancelAnimationFrame(rafId);
//   rafId = null;
// }

// ⭐ 三个容易忽略的特性：
// 1. 页面切到后台时，rAF 会自动暂停，回来时再继续——天然省电
// 2. 它跟着显示器的真实刷新率走，120Hz 屏幕上就是每秒 120 次
// 3. 用 setTimeout(..., 16) 想模拟它是不行的，
//    因为 16ms 和屏幕的 16.67ms 不对齐，会周期性"错过"一帧造成抖动
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
// 判断元素"是否完整地"在视口内（注意：只是部分露出来时这个函数会返回 false）
function isFullyInViewport(element) {
  const rect = element.getBoundingClientRect();
  const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
  const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= viewportHeight &&
    rect.right <= viewportWidth
  );
}

// 如果只想判断"有没有露出一部分"，条件要换成：
// rect.bottom > 0 && rect.top < viewportHeight &&
// rect.right > 0 && rect.left < viewportWidth

// 💡 现代浏览器其实有内置方案，能用 IntersectionObserver 就别手写：
// const io = new IntersectionObserver(entries => {
//   entries.forEach(e => console.log(e.isIntersecting, e.intersectionRatio));
// });
// io.observe(element);

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
}

// ⚠️ 你可能见过 location.reload(true) 这种写法，意思是"强制从服务器重新加载"。
// 这个参数从未进入标准，现代浏览器会直接忽略它，等同于 reload()。
// 真要绕过缓存，得从 HTTP 响应头（Cache-Control: no-store）或请求侧下手。
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

// ⭐ 三者其实是同一套机制的两个不同入口：
// location.href = url   ≡     location.assign(url)
// 都是"新增一条历史记录后跳转"。
// location.replace(url) 则是"用新页面顶掉当前这条记录"，所以回不去。

// reload：重新加载当前页面（相当于按刷新键）
location.reload();
// 注意：reload() 的参数在标准里是不存在的，写成 reload(true) 也不会强制刷新缓存
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
// pushState 的签名：history.pushState(state, unused, url)
// ⭐ 第二个参数（标题）在所有主流浏览器里都被忽略了，传 null 或 '' 都行。
//    它改不了浏览器标签页上的文字，想改标题请用 document.title。

// 示例：单页应用的最小路由
const routes = {
  '/': { title: '首页', template: '<h1>首页</h1>' },
  '/about': { title: '关于', template: '<h1>关于</h1>' },
  '/contact': { title: '联系', template: '<h1>联系</h1>' }
};

// ⭐ 关键：把"渲染"和"改历史"拆成两件事，否则按后退键会越退越多
function render(path) {
  const route = routes[path] || routes['/'];
  document.title = route.title;
  document.getElementById('app').innerHTML = route.template;
}

// 用户主动点链接：渲染 + 新增一条历史记录
function navigate(path) {
  render(path);
  history.pushState({ path }, '', path);
}

// 浏览器前进/后退：⭐ 只渲染，绝不能再 pushState！
window.addEventListener('popstate', (event) => {
  render(location.pathname);
});

// 拦截站内链接
document.addEventListener('click', (e) => {
  const link = e.target.closest('a[data-link]');
  if (!link) return;
  e.preventDefault();
  // ⭐ 必须取 pathname，不能把完整 URL 直接丢给 navigate，
  //    否则 routes['https://site.com/about'] 找不到对应路由。
  navigate(new URL(link.href).pathname);
});

// 首次进入页面时也要渲染一次
render(location.pathname);
```

```javascript
// replaceState：替换当前历史记录（不新增）
// 使用场景：表单提交成功后把 URL 里的 ?step=2 改成 ?step=3，
// 让用户按后退时不会又回到那个已经提交过的表单。
history.replaceState({ step: 3 }, '', '/form?step=3');

// ⚠️ 注意两个限制：
// 1. 只能改同源 URL，改到别的域名会抛 SecurityError
// 2. 只改地址栏，不会触发页面刷新，也不会触发 popstate 事件
```

```javascript
// pushState / replaceState 的区别（关键看"历史条数"有没有增加）

// 假设当前位置是 /home
history.pushState({ page: 1 }, '', '/page1');   // 新增一条 → 历史: /home, /page1
history.pushState({ page: 2 }, '', '/page2');   // 新增一条 → 历史: /home, /page1, /page2
history.back();                                  // 回到 /page1（并触发 popstate）

// 再假设当前位置是 /home
history.replaceState({ page: 1 }, '', '/page1');  // 顶掉 /home → 历史: /page1
history.replaceState({ page: 2 }, '', '/page2');  // 顶掉 /page1 → 历史: /page2
history.back();                                    // ⭐ 直接回到 /page2 之前的那一页，
                                                   //    根本不会出现 /page1（它已被顶掉）

// 一句话记忆：pushState 是"另起一页"，replaceState 是"就地改写"。
// 两者都只改地址栏，页面内容必须由你手动重新渲染。
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
// navigator.platform：平台信息（同样已不推荐使用，Mac 上会得到 "MacIntel"）
console.log('平台:', navigator.platform);

// navigator.appName / appVersion：早就废弃了，而且返回值毫无意义
// 无论你用 Chrome、Firefox 还是 Safari，appName 永远是 'Netscape'
console.log('App名称:', navigator.appName);    // Netscape
console.log('App版本:', navigator.appVersion);
```

```javascript
// ⭐ 如果只是想判断"是不是手机"，优先用功能检测而不是解析 UA

// 方案1（推荐）：UA Client Hints，专门为此设计，值也由浏览器如实提供
if (navigator.userAgentData) {
  console.log('是否移动设备:', navigator.userAgentData.mobile);
  console.log('平台:', navigator.userAgentData.platform);  // 'Windows' / 'macOS' ...
}

// 方案2：媒体查询——"设备是否有指针、是否支持悬停"才是真正影响交互的因素
const isTouchDevice = window.matchMedia('(pointer: coarse)').matches;
console.log('触摸设备:', isTouchDevice);

// ⚠️ 为什么不要解析 UA 字符串？因为它是可以伪造的，而且格式反复变化：
// - Safari 和 Chrome 的 UA 里都写着 "AppleWebKit" 和 "Safari"
// - 安卓平板有时不带 "Mobile"，iPad 从 iPadOS 13 起默认伪装成 Mac
// - 各家浏览器的 UA 已经开始"冻结"，版本号不再如实更新
// 结论：能用功能检测（'xxx' in window）就别查 UA。
```

---

### screen.width / height / availWidth / availHeight

`screen` 对象包含屏幕的信息。

```javascript
// screen.width / height：屏幕分辨率（CSS 像素，不是物理像素）
console.log('屏幕宽度:', screen.width);   // 1920
console.log('屏幕高度:', screen.height);  // 1080

// screen.availWidth / availHeight：可用区域（扣掉任务栏、Dock 等）
console.log('可用宽度:', screen.availWidth);   // 1920
console.log('可用高度:', screen.availHeight);  // 1040

// ⭐ 高分屏（Retina / HiDPI）下的常见困惑：
// 一台 4K 显示器上 screen.width 可能只有 1920，
// 因为这里统计的是 CSS 像素，物理像素要多一倍：
console.log('像素比:', window.devicePixelRatio);  // 例如 2
console.log('物理宽度:', screen.width * window.devicePixelRatio);  // 3840

// 💡 所以给 canvas 做高清适配时，要按 devicePixelRatio 放大画布尺寸，
// 再用 CSS 把它缩回原来的大小，否则在高分屏上会糊。
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
- 浏览器里的全局对象，同时也是 `globalThis`；`var` 和 `function` 声明会挂上去，`let/const/class` 不会
- `innerWidth/innerHeight` 视口尺寸，`outerWidth/outerHeight` 窗口尺寸
- `window.open/close` 打开关闭窗口

### 2. 定时器
- `setTimeout/clearTimeout`：一次性定时
- `setInterval/clearInterval`：周期性定时，回调耗时过长会重叠或丢拍
- `requestAnimationFrame`：动画帧，最精确的动画 API
- 嵌套超过 5 层的定时器最小延迟被钳制为 4ms，后台标签页还会被进一步节流

### 3. location 对象
- `href/protocol/host/hostname/pathname/search/hash`
- `assign()`：导航（可后退）
- `replace()`：替换（不可后退）
- `reload()`：重新加载

### 4. history 对象
- `back/forward/go`：历史记录导航
- `pushState`：添加历史记录（可后退）
- `replaceState`：替换历史记录（不可后退）
- 两者第二个参数（标题）被浏览器忽略，且只能改同源 URL；内容渲染要自己做

### 5. navigator 与 screen
- `navigator.userAgent/platform`：浏览器和平台信息（都已不推荐用于判断环境，优先功能检测或用 `userAgentData`）
- `screen.width/height/availWidth/availHeight`：屏幕信息
- `window.devicePixelRatio`：CSS 像素与物理像素的比值，高清屏适配要用它

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
