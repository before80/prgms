+++
title = "第 34 章 正则表达式"
weight = 340
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 34 章 正则表达式

正则表达式是 JavaScript 里的"字符串匹配神器"。学会了它，你就能在字符串里"大海捞针"，甚至"以一敌百"。

## 34.1 正则基础

### 创建正则：字面量 / new RegExp()

```javascript
// 字面量方式（推荐）
const regex1 = /hello/;

// 构造函数方式（可以动态创建）
const regex2 = new RegExp('hello');

// 两者等价
console.log(regex1.test('hello world')); // 打印结果: true
console.log(regex2.test('hello world')); // 打印结果: true
```

### test() / exec()

```javascript
// test()：返回布尔值，简单快速
const regex = /hello/;
console.log(regex.test('hello world')); // 打印结果: true
console.log(regex.test('goodbye')); // 打印结果: false

// exec()：返回匹配结果或 null，更详细
const result = regex.exec('hello world');
if (result) {
    console.log('匹配到：' + result[0]); // 打印结果: 匹配到：hello
    console.log('索引：' + result.index); // 打印结果: 索引：0
}
```

### 修饰符（flags）

写在正则最后一个 `/` 后面的字母就是修饰符，可以叠加：

| 修饰符 | 名称 | 作用 |
| --- | --- | --- |
| `g` | global | 找出全部匹配，而不是找到第一个就停 |
| `i` | ignoreCase | 忽略大小写 |
| `m` | multiline | 让 `^` `$` 匹配每一行的开头和结尾 |
| `s` | dotAll | 让 `.` 也能匹配换行符 |
| `u` | unicode | 按 Unicode 码点处理，支持 `\p{...}`，能正确处理 emoji 等 |
| `y` | sticky | 从 `lastIndex` 处**紧挨着**开始匹配（`g` 是往后找，`y` 是必须贴住） |
| `d` | hasIndices | 让匹配结果带上每个分组的 `indices` 下标信息 |

```javascript
console.log('Hello hello'.match(/hello/gi)); // 打印结果: ['Hello', 'hello']
console.log(/^b/m.test('a\nb'));              // 打印结果: true（m 让 ^ 匹配第二行行首）
console.log(/a.b/s.test('a\nb'));             // 打印结果: true（s 让 . 匹配换行）
```

> **一个必须知道的坑**：带 `g` 或 `y` 的正则对象是有状态的，`test()` 和 `exec()` 每次调用都会从 `lastIndex` 继续往后找。同一个带 `g` 的正则反复 `test()` 同一个字符串，结果会在 `true`/`false` 之间来回跳。

```javascript
const re = /a/g;
console.log(re.test('a')); // true（lastIndex 变成 1）
console.log(re.test('a')); // false（从 1 开始找，没找到，lastIndex 归零）
console.log(re.test('a')); // true（又从 0 开始）

// 解决方式一：每次都新建一个正则
// 解决方式二：用完手动复位
re.lastIndex = 0;

// 循环取全部匹配时，也要注意 exec 返回 null 后 lastIndex 会自动归零
```

下一节，我们来学习字符与元字符！

## 34.2 字符与元字符

### 字符类：[abc] / [0-9] / [^abc] / \d \D \w \W \s \S / .

```javascript
// [abc]：匹配 a、b 或 c
console.log(/[aeiou]/.test('hello')); // 打印结果: true

// [0-9]：匹配数字
console.log(/[0-9]/.test('hello')); // 打印结果: false

// [^abc]：匹配除了 a、b、c 以外的字符
console.log(/[^aeiou]/.test('hello')); // 打印结果: true

// \d：匹配数字，等价于 [0-9]
console.log(/\d/.test('abc123')); // 打印结果: true

// \D：匹配非数字，等价于 [^0-9]
console.log(/\D/.test('123')); // 打印结果: false

// \w：匹配单词字符，等价于 [a-zA-Z0-9_]
console.log(/\w/.test('_')); // 打印结果: true

// \W：匹配非单词字符
console.log(/\W/.test('!')); // 打印结果: true

// \s：匹配空白字符（空格、制表符、换行符等）
console.log(/\s/.test('hello world')); // 打印结果: true

// \S：匹配非空白字符
console.log(/\S/.test('   ')); // 打印结果: false

// .：匹配除换行符以外的任意字符
console.log(/./.test('\n')); // 打印结果: false
```

### 量词：{n} / {n,} / {n,m} / * / + / ?

```javascript
// {n}：正好匹配 n 次
console.log(/a{3}/.test('aa')); // 打印结果: false
console.log(/a{3}/.test('aaa')); // 打印结果: true

// {n,}：至少匹配 n 次
console.log(/a{2,}/.test('a')); // 打印结果: false
console.log(/a{2,}/.test('aaa')); // 打印结果: true

// {n,m}：匹配 n 到 m 次
console.log(/a{2,4}/.test('aaa')); // 打印结果: true

// *：匹配 0 次或多次，等价于 {0,}
console.log(/ab*c/.test('ac')); // 打印结果: true
console.log(/ab*c/.test('abc')); // 打印结果: true

// +：匹配 1 次或多次，等价于 {1,}
console.log(/ab+c/.test('ac')); // 打印结果: false
console.log(/ab+c/.test('abc')); // 打印结果: true

// ?：匹配 0 次或 1 次，等价于 {0,1}
console.log(/colou?r/.test('color')); // 打印结果: true
console.log(/colou?r/.test('colour')); // 打印结果: true
```

### 贪婪 vs 非贪婪：.*? / +? / ??

贪婪匹配会尽可能多地匹配，非贪婪匹配会尽可能少地匹配。

```javascript
// 贪婪匹配：.* 会尽可能多地匹配
console.log('"hello" and "world"'.match(/".*"/)[0]); // 打印结果: "hello" and "world"

// 非贪婪匹配：.*? 会尽可能少地匹配
console.log('"hello" and "world"'.match(/".*?"/)[0]); // 打印结果: "hello"
```

### 边界：^ / $ / \b / \B

```javascript
// ^：匹配字符串开头
console.log(/^hello/.test('hello world')); // 打印结果: true
console.log(/^hello/.test('hi hello')); // 打印结果: false

// $：匹配字符串结尾
console.log(/world$/.test('hello world')); // 打印结果: true
console.log(/world$/.test('world hi')); // 打印结果: false

// \b：匹配单词边界
console.log(/\bword\b/.test('a word here')); // 打印结果: true
console.log(/\bword\b/.test('sword here')); // 打印结果: false

// \B：匹配非单词边界
console.log(/\Bword/.test('sword')); // 打印结果: true
```

下一节，我们来学习分组与引用！

## 34.3 分组与引用

### 捕获分组：(abc)

```javascript
// 捕获分组：用圆括号包裹，会被捕获
const result = /(\d{4})-(\d{2})-(\d{2})/.exec('2024-03-24');
console.log(result[0]); // 打印结果: 2024-03-24
console.log(result[1]); // 打印结果: 2024
console.log(result[2]); // 打印结果: 03
console.log(result[3]); // 打印结果: 24
```

### 非捕获分组：(?:abc)

```javascript
// 非捕获分组：用 (?:)，不会捕获
const result = /(?:\d{4})-(\d{2})-(\d{2})/.exec('2024-03-24');
console.log(result[0]); // 打印结果: 2024-03-24
console.log(result[1]); // 打印结果: 03（只捕获第二个和第三个）
console.log(result[2]); // 打印结果: 24
```

### 反向引用：\1 \2

```javascript
// 反向引用：\1 引用第一个分组，\2 引用第二个分组
console.log(/(\w)\1/.test('aa')); // 打印结果: true（两个相同的字母）
console.log(/(\w)\1/.test('ab')); // 打印结果: false

// 应用：匹配重复的单词
console.log(/\b(\w+)\s\1\b/.test('the the')); // 打印结果: true
```

### 或运算：|

```javascript
// 或运算：|
console.log(/cat|dog/.test('I have a cat')); // 打印结果: true
console.log(/cat|dog/.test('I have a dog')); // 打印结果: true

// 分组中使用或
console.log(/(foo|bar)baz/.test('foobaz')); // 打印结果: true
console.log(/(foo|bar)baz/.test('barbaz')); // 打印结果: true
```

下一节，我们来学习字符串方法！

## 34.4 字符串方法

### match / search / replace / split + 正则

```javascript
const str = 'Hello World! 123';

// match：返回所有匹配
console.log(str.match(/\d+/g)); // 打印结果: ['123']

// search：返回第一个匹配的索引
console.log(str.search(/\d+/)); // 打印结果: 13（从 0 开始数：'!' 在 11，空格在 12，'1' 在 13）

// replace：替换匹配
console.log(str.replace(/\d+/, '456')); // 打印结果: Hello World! 456

// split：分割字符串
console.log('a,b,c'.split(/,/)); // 打印结果: ['a', 'b', 'c']
```

### replace 回调函数与反向引用：$1 $2 $` $' $&

```javascript
// $1, $2：引用分组
console.log('2024-03-24'.replace(/(\d{4})-(\d{2})-(\d{2})/, '$3/$2/$1'));
// 打印结果: 24/03/2024

// $&：整个匹配
console.log('hello'.replace(/\w+/, '[$&]')); // 打印结果: [hello]

// $`：替换文本 = 匹配位置「之前」的全部内容
console.log('hello world'.replace(/world/, "[$`]"));
// 匹配到的是 'world'，它前面的内容是 'hello '
// 于是 'world' 被替换成 '[hello ]'
// 打印结果: hello [hello ]

// $'：替换文本 = 匹配位置「之后」的全部内容
console.log('hello world'.replace(/hello/, "[$']"));
// 匹配到的是 'hello'，它后面的内容是 ' world'
// 于是 'hello' 被替换成 '[ world]'
// 打印结果: [ world] world

// $n 与 $<name>：引用分组（下标分组和命名分组都支持）
console.log('2024-03-24'.replace(/(?<y>\d{4})-(?<m>\d{2})-(?<d>\d{2})/, '$<d>/$<m>/$<y>'));
// 打印结果: 24/03/2024

// $$ 表示一个字面量 $
console.log('price'.replace(/price/, '$$9.9')); // 打印结果: $9.9

// 回调函数
console.log('2024-03-24'.replace(/(\d{4})-(\d{2})-(\d{2})/, function(match, y, m, d) {
    return m + '/' + d + '/' + y;
}));
// 打印结果: 03/24/2024
```

下一节，我们来学习常用场景！

## 34.5 常用场景

### 手机号验证

```javascript
// 中国大陆手机号：1开头，11位数字
const phoneRegex = /^1[3-9]\d{9}$/;
console.log(phoneRegex.test('13812345678')); // 打印结果: true
console.log(phoneRegex.test('12812345678')); // 打印结果: false（1开头，但2不符合）
console.log(phoneRegex.test('1381234567')); // 打印结果: false（只有10位）
```

### 邮箱验证

```javascript
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
console.log(emailRegex.test('test@example.com')); // 打印结果: true
console.log(emailRegex.test('invalid@email')); // 打印结果: false
```

邮箱的完整语法（RFC 5321/5322）极其复杂，上面这种简化写法**不能**用来判断「邮箱是否真实存在」，它的定位只是「快速拦掉明显写错的内容」。实践中的做法是：

- 前端只做宽松校验（有 `@`、有域名、长度合理），校验失败不阻塞用户继续修改；
- 真正可靠的验证手段是**给该邮箱发一封验证邮件**；
- 需要严格遵循标准时用成熟库（如 `validator.js` 的 `isEmail`），不要手写。

另外两个细节：`[a-zA-Z0-9.-]` 这种字符类里，`.` 已经失去「任意字符」的含义，只是普通的点号；但连续的点（`a..b@x.com`）依然会被放行，需要额外判断。

### URL 参数解析

```javascript
const url = 'https://example.com/search?q=javascript&page=1';

// ✅ 推荐写法：浏览器和 Node.js 都内置了 URL 与 URLSearchParams
const params = Object.fromEntries(new URL(url).searchParams);
console.log(params); // 打印结果: { q: 'javascript', page: '1' }

// ✅ 正则写法：必须用 matchAll（或 exec 循环）才能拿到分组
const paramsByRegex = {};
for (const m of url.matchAll(/[?&]([^&=]+)=([^&]*)/g)) {
    paramsByRegex[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
}
console.log(paramsByRegex); // 打印结果: { q: 'javascript', page: '1' }

// 需要处理 '+' 号表示空格、中文参数等情况时，交给 URLSearchParams 更稳妥
console.log(new URL('https://e.com/s?q=a+b%20c').searchParams.get('q')); // 打印结果: a b c
```

> 这个例子也解释了一个高频疑问：**`String.prototype.match` 传入带 `g` 标志的正则时，返回值里只有每段匹配的完整文本，捕获分组全部丢失**。想同时拿到分组内容，就用 `matchAll` 或 `exec` 循环。

### 敏感词替换

```javascript
const sensitiveWords = ['暴力', '色情', '赌博'];

function filterSensitive(text) {
    const regex = new RegExp(sensitiveWords.join('|'), 'g');
    return text.replace(regex, '***');
}

console.log(filterSensitive('这是一段包含暴力的文字')); // 打印结果: 这是一段包含***的文字
```

用 `new RegExp` 从词库拼正则时，有两个必须处理的细节：

1. **词库里的内容要转义**。如果某个词包含 `.`、`*`、`(`、`?` 这类元字符，直接拼进正则会改变含义甚至让整个正则失效。
2. **中文没有「单词边界」**，所以不能靠 `\b` 精确匹配，只能做整段替换；这也意味着上面这种替换很容易被空格、标点、拼音、繁体等写法绕过，只能作为**最基础的展示层过滤**，真正的文本审核要交给专业服务。

```javascript
// 转义正则元字符，再拼成正则
function escapeRegExp(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const regex = new RegExp(sensitiveWords.map(escapeRegExp).join('|'), 'g');
```

### 千分位格式化

```javascript
// 数字千分位格式化
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

console.log(formatNumber(1234567)); // 打印结果: 1,234,567
console.log(formatNumber(1234567.89)); // 打印结果: 1,234,567.89
```

### 密码强度验证

```javascript
function validatePassword(password) {
    const errors = [];
    
    if (password.length < 8) errors.push('密码至少8位');
    if (!/[a-z]/.test(password)) errors.push('需要包含小写字母');
    if (!/[A-Z]/.test(password)) errors.push('需要包含大写字母');
    if (!/\d/.test(password)) errors.push('需要包含数字');
    if (!/[!@#$%^&*]/.test(password)) errors.push('需要包含特殊字符');
    
    return {
        valid: errors.length === 0,
        errors: errors
    };
}

console.log(validatePassword('Abc123!')); // 打印结果: { valid: true, errors: [] }
console.log(validatePassword('weak')); // 打印结果: { valid: false, errors: [...] }
```

### trim 的正则实现

```javascript
// 去除首尾空白
function trim(str) {
    return str.replace(/^\s+|\s+$/g, '');
}

console.log(trim('  hello world  ')); // 打印结果: hello world
```

## 34.6 进阶特性

### 命名捕获分组：(?<name>...)

用下标 `result[1]` 取分组，一旦分组变多就很难看懂，命名分组可以让代码自解释：

```javascript
const re = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
const { groups } = re.exec('2024-03-24');
console.log(groups.year);  // 打印结果: 2024
console.log(groups.month); // 打印结果: 03
console.log(groups.day);   // 打印结果: 24
```

### 断言（环视）：(?=) (?!) (?<=) (?<!)

断言只「看一眼」而不消耗字符，因此常用来做「只替换某段内容」：

| 写法 | 含义 |
| --- | --- |
| `X(?=Y)` | 匹配后面跟着 `Y` 的 `X`（正向前瞻） |
| `X(?!Y)` | 匹配后面不是 `Y` 的 `X`（负向前瞻） |
| `(?<=Y)X` | 匹配前面是 `Y` 的 `X`（正向后顾） |
| `(?<!Y)X` | 匹配前面不是 `Y` 的 `X`（负向后顾） |

```javascript
// 只给数字加单位，不改动数字本身
console.log('价格 120 元'.replace(/\d+(?= 元)/, '$&.00')); // 打印结果: 价格 120.00 元

// $ 加千分位就是靠 \B(?=(\d{3})+(?!\d)) 这种「位置断言」实现的

// 后顾断言：只替换￥后面的数字
console.log('￥120 and $99'.replace(/(?<=￥)\d+/, '***')); // 打印结果: ￥*** and $99
```

### Unicode 属性转义：\p{...}

处理 emoji、各国文字时，字符类的写法会失效，要配合 `u` 标志使用 Unicode 属性：

```javascript
// 匹配所有表情符号
console.log('Hi 👋 世界'.match(/\p{Emoji}/gu)); // 打印结果: ['👋']

// 匹配所有中文字符
console.log('abc中文'.match(/\p{Script=Han}/gu)); // 打印结果: ['中', '文']
```

注意：`.` 默认按 UTF-16 码元匹配，不加 `u` 时一个 emoji 会被拆成两半：

```javascript
console.log('👋'.length);        // 打印结果: 2（UTF-16 长度）
console.log([...'👋'].length);   // 打印结果: 1（按码点计数）
console.log(/^.$/.test('👋'));   // 打印结果: false
console.log(/^.$/u.test('👋'));  // 打印结果: true
```

### 动态创建正则时记得转义：RegExp.escape

把用户输入当作「普通文本」去搜索时，必须转义元字符。规范中已新增 `RegExp.escape()`：

```javascript
const keyword = 'a+b';

// ❌ 会被当成「一个或多个 a 后面跟 b」
new RegExp(keyword).test('aaab');

// ✅ 转义后按字面量匹配
if (typeof RegExp.escape === 'function') {
    console.log(new RegExp(RegExp.escape(keyword)).test('a+b')); // 打印结果: true
}

// 兼容旧环境的等价写法（见上一节 escapeRegExp）
```

### replaceAll 与字符串方法

`String.prototype.replaceAll`（ES2021）语义更直白：传字符串时替换全部，传正则时**必须带 `g` 标志**，否则会抛错。

```javascript
console.log('a-b-c'.replaceAll('-', '+'));   // 打印结果: a+b+c
console.log('a-b-c'.replaceAll(/-/g, '+'));  // 打印结果: a+b+c
// console.log('a-b-c'.replaceAll(/-/, '+')); // TypeError: replaceAll must be called with a global RegExp
```

### 什么时候不该用正则

正则是处理**扁平文本**的利器，但它不是万能的：

- **不要用正则解析 HTML、XML、JSON 等嵌套结构**，标签嵌套、属性顺序、注释、CDATA 都会让它出错，应该用 DOMParser 或专用解析器。
- **不要用正则实现「判断是否包含某个域名」这类安全检查**，`evil.com` 可以写成 `evil.com.attacker.net`、`evil.com@attacker.net` 等多种形式，必须用 URL 解析后比较 `hostname`。
- **正则性能要留意灾难性回溯**：像 `(a+)+b` 这种嵌套量词，遇到不匹配的长字符串会让引擎指数级尝试。避免嵌套量词、避免 `.*` 重复、能用更精确的字符类就别用 `.`。

```javascript
// ❌ 嵌套量词，长字符串上可能卡死主线程
const bad = /(a+)+b/;

// ✅ 用精确字符类，匹配过程是线性的
const good = /a+b/;
```

---

## 本章小结

本章我们学习了正则表达式：

1. **正则基础**：创建正则（字面量/RegExp）、test/exec 方法、修饰符 flags，以及带 `g` 的正则有状态这个坑。
2. **字符与元字符**：字符类、量词、贪婪/非贪婪、边界。
3. **分组与引用**：捕获分组、非捕获分组、反向引用、或运算。
4. **字符串方法**：match、search、replace、split 与正则的结合，以及 `$&`、`$1`、`$<name>`、`matchAll`、`replaceAll`。
5. **常用场景**：手机号、邮箱、URL 参数、千分位、密码强度等验证。
6. **进阶特性**：命名分组、环视断言、Unicode 属性转义、`RegExp.escape`。
7. **使用边界**：不要解析嵌套结构、不要做域名白名单判断、注意灾难性回溯。

正则表达式是 JavaScript 开发中的"瑞士军刀"，掌握它能让你的字符串处理能力大幅提升。

下一章，我们要学习错误处理——让程序优雅地"容错"！
