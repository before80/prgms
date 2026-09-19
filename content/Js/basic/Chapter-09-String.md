+++
title = "第 9 章 字符串"
weight = 90
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 9 章 字符串

> 如果说数字是编程世界的原子，那么字符串就是分子——它们组合起来能表达一切，从"Hello, World!"到"老板，这个需求做不了"。

## 9.1 基础操作

### 模板字符串：反引号 + ${}

各位同学，请把你们的双引号和单引号都收起来，今天我们要隆重介绍字符串家族的贵族——**模板字符串**（Template Literal）。

这玩意儿有多厉害？想象一下，你要拼接一个句子：

```javascript
const name = "张三";
const age = 25;
const job = "前端工程师";

// 以前的拼接方式（令人窒息的 + 地狱）
const bio = name + "今年" + age + "岁，是一名" + job + "，正在加班。";

// 模板字符串方式（优雅得体）
const bioTemplate = `${name}今年${age}岁，是一名${job}，正在加班。`;

console.log(bioTemplate); // 张三今年25岁，是一名前端工程师，正在加班。
```

看到没？用反引号（Esc 键下面那个 ` `` `，不是单引号）包裹字符串，然后在 `${}` 里面直接写变量或者表达式，这就是传说中的**模板字符串**！

${} 里面不仅可以放变量，还可以放表达式：

```javascript
const a = 10;
const b = 20;

// 表达式？没问题！
console.log(`a + b = ${a + b}`); // a + b = 30

// 三元表达式？小意思！
console.log(`今天是${new Date().getDay() === 0 ? '星期天' : '工作日'}`); // 今天是工作日

// 函数调用？安排！
function getWeather() {
  return "晴";
}
console.log(`今天天气：${getWeather()}`); // 今天天气：晴
```

多行字符串？以前你想写个诗，得用 `\n` 拼来拼去，现在直接回车就行：

```javascript
const poem = `床前明月光，
疑是地上霜，
举头望明月，
低头思故乡。`;

console.log(poem);
// 床前明月光，
// 疑是地上霜，
// 举头望明月，
// 低头思故乡。
```

> 💡 小提示：模板字符串会保留空格和换行，所以排版要注意哦！不然你的代码可能会变成"艺术字"。

---

### 模板标签函数（Tagged Template）

如果说模板字符串是个贵族，那模板标签函数就是贵族中的007——低调奢华还自带特异功能！

什么叫模板标签函数？就是你可以在模板字符串前面加一个"标签"，这个标签本质上是一个函数，它可以接收模板字符串的各个部分作为参数，然后返回你想要的内容。

```javascript
// 定义一个"安全"标签函数，用于防止 XSS 攻击（假装有个简单的转义函数）
function safeHtml(strings, ...values) {
  // strings 是字符串字面量部分的数组
  // values 是 ${} 表达式的值组成的数组
  let result = '';
  strings.forEach((str, i) => {
    let value = values[i];
    // 简单转义 HTML 特殊字符
    if (typeof value === 'string') {
      value = value
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }
    result += str + (value ?? '');
  });
  return result;
}

const userName = '<script>alert("hack!")</script>';
const message = safeHtml`<p>欢迎 ${userName} 访问我们的网站！</p>`;

console.log(message);
// <p>欢迎 &lt;script&gt;alert("hack!")&lt;/script&gt; 访问我们的网站！</p>
```

解释一下这个魔法：

1. 当 JavaScript 引擎看到 `safeHtml\`...\`` 时，它不是直接返回一个字符串
2. 而是调用 `safeHtml` 函数，传入：
   - `strings`: 模板中的静态字符串部分数组
   - `...values`: 动态表达式的值

拿上面的例子来说：
- `strings` = [`<p>欢迎 `, ` 访问我们的网站！</p>`]
- `values` = [`<script>alert("hack!")</script>`]

这个特性在 Vue 的模板语法、GraphQL 的查询语言、React 的 styled-components 等库中都有广泛应用。可以说，不懂标签函数，你都不好意思跟别人说你会现代前端框架！

---

### 长度与访问：length / charAt / charCodeAt

#### length 属性

`length` 返回的是**UTF-16 编码单元（code unit）的个数**，既不是字节数，也不总是「字符数」。这个区别在遇到 emoji 或生僻字时会立刻显形：

```javascript
const str1 = "Hello";
const str2 = "你好";
const str3 = "🎉";

console.log(str1.length); // 5（ASCII 字符，1 个字符 = 1 个编码单元）
console.log(str2.length); // 2（常用汉字在 BMP 内，同样是 1 个编码单元）
console.log(str3.length); // 2！🎉 是 U+1F389，超出 BMP，需要一对「代理项」来表示

// 想按「码点」数个数，先展开成数组
console.log([...str3].length);       // 1
console.log(Array.from(str3).length); // 1

// 汉字在内存里通常占 3 个字节，但 length 不算字节
console.log(new TextEncoder().encode("你好").length); // 6（浏览器 / Node 都支持）
```

> 记住一句话：`length` 数的是「编码单元」，不是肉眼看到的字符数。第 9.5 节会专门讲怎么正确处理 emoji。

#### charAt(index)

`charAt` 方法返回指定位置的字符，就像点名一样：

```javascript
const str = "Hello";

console.log(str.charAt(0)); // H
console.log(str.charAt(1)); // e
console.log(str.charAt(2)); // l
console.log(str.charAt(3)); // l
console.log(str.charAt(4)); // o
console.log(str.charAt(5)); // ""（空字符串，超出范围不报错）
```

其实你也可以用数组下标的方式访问，更简洁：

```javascript
const str = "Hello";

console.log(str[0]); // H
console.log(str[4]); // o
console.log(str[5]); // undefined（注意这里是 undefined，不是空字符串）
```

> ⚠️ 注意：`str[5]` 返回 `undefined`，而 `str.charAt(5)` 返回 `""`。这就是两者的区别——前者访问越界会返回 `undefined`，后者始终返回空字符串。

#### charCodeAt(index)

这个方法返回指定位置字符的 **Unicode 编码**（UTF-16 编码值），一个数字。这个数字有什么用？可以用来判断字符的类型：

```javascript
const str = "Hello";

console.log(str.charCodeAt(0)); // 72（H 的 Unicode 编码）
console.log(str.charCodeAt(1)); // 101（e 的 Unicode 编码）

// 判断是否是字母
function isAlpha(char) {
  const code = char.charCodeAt(0);
  return (code >= 65 && code <= 90) || (code >= 97 && code <= 122);
}

console.log(isAlpha('A')); // true
console.log(isAlpha('Z')); // true
console.log(isAlpha('9')); // false
console.log(isAlpha('中')); // false（中文不在 ASCII 范围内）
```

反过来，你也可以用 `String.fromCharCode()` 把 Unicode 编码转回字符：

```javascript
console.log(String.fromCharCode(72)); // H
console.log(String.fromCharCode(101)); // e
console.log(String.fromCharCode(20013)); // 中
console.log(String.fromCharCode(0x4E2D)); // 中（十六进制也可以）
```

```javascript
// charCodeAt 同样只处理 16 位编码单元，遇到 emoji 会被「劈成两半」
const emoji = "🎉";
console.log(emoji.charCodeAt(0));    // 55356（0xD83C，高代理项）
console.log(emoji.charCodeAt(1));    // 57225（0xDF89，另一半）
console.log(emoji.codePointAt(0));   // 127881（0x1F389，才是完整的码点）

// 想还原完整字符，用 codePointAt + fromCodePoint 配对
console.log(String.fromCodePoint(emoji.codePointAt(0))); // "🎉"
// 而 fromCharCode 对超出 BMP 的码点会「拆成两个字符」
console.log(String.fromCharCode(0x1F389).codePointAt(0).toString(16)); // "f389"
// 结果是一个毫不相干的私用区字符，跟 🎉 没有关系，别这么用

// 实践中更简单：直接按码点遍历
for (const ch of "a🎉b") {
  console.log(ch, ch.codePointAt(0));
}
// a 97
// 🎉 127881
// b 98
```

---

### 字符串的不可变性

**重要的事情说三遍：字符串是不可变的！字符串是不可变的！字符串是不可变的！**

什么叫不可变？就是你不能像数组那样直接修改字符串中的某个字符：

```javascript
const str = "Hello";

// ❌ 错误示范：字符串不能这样修改
str[0] = 'h';  // 不报错，但也没用
console.log(str); // "Hello" —— 纹丝不动！

// ✅ 正确做法：创建一个新的字符串
const newStr = 'h' + str.slice(1);
console.log(newStr); // "hello"
```

这个设计其实很有道理——字符串在很多语言中都是 immutable（不可变）的，这带来了很多好处：

1. **线程安全**：多个线程同时读取同一个字符串，不用担心被其他线程修改
2. **性能优化**：JavaScript 引擎可以对字符串进行缓存、内部存储等优化
3. **安全**：防止了各种奇怪的指针操作和缓冲区溢出

虽然每次"修改"都像是创建了一个新字符串，但由于 JavaScript 引擎的优化，大多数情况下性能开销是可以接受的。而且现代浏览器的字符串拼接已经优化得很好了，不用太担心性能问题。

```javascript
// 字符串的所有"修改"方法，其实都返回新字符串
const original = "Hello";

console.log(original.toUpperCase()); // "HELLO" —— original 保持不变
console.log(original);               // "Hello" —— 仍然是 Hello

const upper = original.toUpperCase(); // 新建了一个字符串
console.log(upper);                   // "HELLO"
```

记住这个原则：你对字符串做的任何操作，要么返回一个新字符串，要么返回其他数据类型，原字符串永远不会改变！

---

## 9.2 查找与替换

### indexOf / lastIndexOf / includes / startsWith / endsWith

如果说字符串是一锅汤，那么这些方法就是你的各种捞汤工具——有的专门捞指定位置的菜，有的看看汤里有没有你想要的食材。

#### indexOf — 从左向右找

`indexOf` 方法会在字符串中查找指定字符或子字符串，**从左到右**查找，返回找到的位置（索引），找不到就返回 `-1`：

```javascript
const str = "Hello World, Hello JavaScript";

console.log(str.indexOf("Hello"));      // 0（第一个 Hello 的位置）
console.log(str.indexOf("World"));      // 6
console.log(str.indexOf("hello"));      // -1（区分大小写！）
console.log(str.indexOf("o"));          // 4（第一个 o 的位置）
console.log(str.indexOf("o", 5));      // 7（从索引5开始找，找第二个 o）
```

注意：`indexOf` 区分大小写！"hello" 和 "Hello" 是两个不同的字符串。

#### lastIndexOf — 从右向左找

`lastIndexOf` 和 `indexOf` 正好相反，它从字符串的**末尾开始向前找**：

```javascript
const str = "Hello World, Hello JavaScript";

console.log(str.lastIndexOf("Hello"));  // 13（第二个 Hello 的位置）
console.log(str.lastIndexOf("o"));     // 21（从右边数第一个 o）
console.log(str.lastIndexOf("o", 20));  // 7（从索引20往前找）
console.log(str.lastIndexOf("xyz"));    // -1（找不到）
```

#### includes — 看看有没有

`includes` 方法返回一个布尔值，告诉你字符串里有没有指定的内容，简单粗暴：

```javascript
const email = "user@example.com";

console.log(email.includes("@"));       // true
console.log(email.includes("gmail"));   // false
console.log(email.includes("@", 5));    // false（从索引5开始查找）
```

这个方法是 ES6 引入的，比 `indexOf !== -1` 这种写法直观多了！

#### startsWith — 是不是以...开头

顾名思义，检查字符串是不是以指定内容开头：

```javascript
const url = "https://www.example.com";

console.log(url.startsWith("https://"));   // true
console.log(url.startsWith("http://"));    // false（注意是 https 不是 http）
console.log(url.startsWith("www", 8));    // true（从索引8开始检查）
```

第二个参数很多人不知道，它允许你指定从哪里开始检查！

#### endsWith — 是不是以...结尾

和 `startsWith` 相反，检查字符串是不是以指定内容**结尾**：

```javascript
const filename = "document.pdf";

console.log(filename.endsWith(".pdf"));    // true
console.log(filename.endsWith(".txt"));     // false
console.log(filename.endsWith("ment"));     // false（"ment" 出现在中间，但结尾是 "pdf"）
console.log(filename.endsWith("ment", 8));  // true（限定只看前 8 个字符，也就是 "document"）
console.log(filename.slice(0, 8).endsWith("ment")); // true —— 第二个参数等价于这种写法
```

> 💡 小技巧：判断文件类型用 `endsWith` 比用 `indexOf` + `=== -1` 优雅多了！

> ⚠️ 注意 `endsWith` 的第二个参数是「把字符串截断到这么长再判断」，语义和 `startsWith` 的「从第几位开始」正好相反，很容易记混。

#### 综合对比

| 方法 | 返回值 | 区分大小写 | 第二个参数 |
|------|--------|-----------|-----------|
| `indexOf` | 索引数字或 -1 | ✅ 是 | ✅ 从该索引开始查找 |
| `lastIndexOf` | 索引数字或 -1 | ✅ 是 | ✅ 从该索引往前查找 |
| `includes` | 布尔值 | ✅ 是 | ✅ 从该索引开始查找 |
| `startsWith` | 布尔值 | ✅ 是 | ✅ 从该索引开始检查 |
| `endsWith` | 布尔值 | ✅ 是 | ✅ 检查前N个字符 |

---

### search：正则查找

如果说 `indexOf` 是拿着放大镜找东西，那 `search` 就是派出了侦探——它支持**正则表达式**！

```javascript
const str = "我的邮箱是 user@email.com，他的邮箱是 admin@test.org";

console.log(str.search("邮箱"));           // 2（第一个「邮」的位置）
console.log(str.search(/\d+/));            // -1（这段文字里根本没有数字！）
console.log(str.search(/[a-z]+@[a-z]+\.[a-z]+/i)); // 6（"user@email.com" 的起始位置）
console.log(str.search("xyz"));            // -1（找不到）

// 想找数字，得换一段带数字的文本
const order = "订单号：20240101，总价：999.5元";
console.log(order.search(/\d+/)); // 4（第一个数字的位置）
```

`search` 方法返回的是匹配内容的**起始位置**，和 `indexOf` 一样，找不到就返回 `-1`。

它的好处是你可以使用正则表达式的强大能力：

```javascript
const text = "订单号：20240101，总价：999.5元";

console.log(text.search(/\d{8}/));        // 4（8位数字，订单号）
console.log(text.search(/[\u4e00-\u9fa5]+/)); // 0（匹配中文）
console.log(text.search(/^\d/));           // -1（不是以数字开头）
```

> ⚠️ 注意：`search` 不支持正则表达式的 `g`（全局）标志，如果你需要找所有匹配，用正则表达式的 `match` 方法或者字符串的 `matchAll` 方法。

---

### replace / replaceAll

#### replace — 替换一个

`replace` 方法可以替换字符串中的内容，**只替换第一个找到的**：

```javascript
const str = "Hello World, Hello JavaScript";

console.log(str.replace("Hello", "Hi"));     // "Hi World, Hello JavaScript"
// 注意：只替换了第一个 Hello，第二个没动！

// 如果想全部替换，可以用正则表达式（带 g 标志）
console.log(str.replace(/Hello/g, "Hi"));    // "Hi World, Hi JavaScript"
```

`replace` 方法接收两个参数：
- 第一个：要查找的内容（字符串或正则表达式）
- 第二个：替换成什么（字符串或函数）

第二个参数如果是函数，这个函数会在每次匹配时调用，函数的返回值会作为替换文本：

```javascript
const str = "张三买了5个苹果，李四买了10个梨";

const result = str.replace(/\d+/g, (match) => {
  const num = parseInt(match, 10);
  return num * 2;  // 数字翻倍
});

console.log(result); // "张三买了10个苹果，李四买了20个梨"
```

#### replaceAll — 替换所有（ES2021+）

ES2021 引入了 `replaceAll`，顾名思义，替换**所有**匹配项：

```javascript
const str = "Hello World, Hello JavaScript";

// replaceAll 直接替换所有，不需要正则
console.log(str.replaceAll("Hello", "Hi")); // "Hi World, Hi JavaScript"
```

> ⚠️ 注意：如果第一个参数是字符串而不是正则表达式，`replace` 只替换第一个，而 `replaceAll` 会替换所有。这是它们的核心区别！

```javascript
// 字符串参数的行为差异
"aaa".replace("a", "b");      // "baa" — 只替换第一个
"aaa".replaceAll("a", "b");   // "bbb" — 替换所有
```

如果第一个参数是正则表达式，`replaceAll` 会**强制要求**你带上 `g` 标志，否则直接抛 `TypeError`：

```javascript
// 用正则表达式 + g，两者效果相同
"aaa".replace(/a/g, "b");      // "bbb"
"aaa".replaceAll(/a/g, "b");   // "bbb"

// 少了 g 标志，replaceAll 会直接报错（这点和 replace 不同）
// "aaa".replaceAll(/a/, "b");  // TypeError: replaceAll must be called with a global RegExp
"aaa".replace(/a/, "b");       // "baa" —— replace 只在第一个匹配处动手

// 另一个区别：replaceAll 传字符串时是「字面量」匹配，不需要转义正则元字符
"1.2.3".replaceAll(".", "-");  // "1-2-3"
"1.2.3".replace(/./g, "-");    // "-----" —— 正则里 . 匹配任意字符，踩坑现场
```

> 💡 小贴士：浏览器兼容性需要注意——`replaceAll` 是 ES2021 新增的，比较老的浏览器可能不支持。如果你需要兼容旧环境，用 `replace` + 正则表达式是更稳妥的选择。

---

## 9.3 提取与分割

### slice / substring / substr：字符串提取

JavaScript 给了你三把切割字符串的刀：`slice`、`substring`、`substr`。它们都能切，但各有脾气。

#### slice — 切片面包刀（推荐使用）

`slice` 方法从字符串中提取一部分，返回提取的部分。语法：
```javascript
str.slice(startIndex, endIndex)
```

- `startIndex`：起始位置（包含）
- `endIndex`：结束位置（**不包含**），省略则切到末尾

```javascript
const str = "Hello World";

console.log(str.slice(0, 5));    // "Hello" — 从0到5，不包含5
console.log(str.slice(6));       // "World" — 从6到末尾
console.log(str.slice(-5));      // "World" — 负数从末尾开始数，-5就是倒数第5个字符
console.log(str.slice(-5, -1));  // "Worl" — 从倒数第5个到倒数第1个，不包含最后一个
console.log(str.slice(0));       // "Hello World" — 复制整个字符串的妙招
```

> 🎯 小技巧：`slice(0)` 可以用来复制字符串，虽然听起来多此一举，但在某些需要保证返回新字符串而不是原字符串引用的场景下很有用！

#### substring — 类似 slice，但有区别

`substring` 的语法和 `slice` 几乎一样：
```javascript
str.substring(startIndex, endIndex)
```

```javascript
const str = "Hello World";

console.log(str.substring(0, 5));    // "Hello"
console.log(str.substring(6));        // "World"
console.log(str.substring(10, 0));   // "Hello" — 自动交换 start > end
```

等等，最后一行发生了什么？当 `startIndex > endIndex` 时，`substring` 会自动交换它们！这个特性让 `substring` 比 `slice` 更"包容"，但也可能掩盖一些问题。

**`slice` vs `substring` 的关键区别：**

```javascript
const str = "Hello World";

// 负数的处理完全不同！
console.log(str.slice(-3));       // "rld" — 支持负数，从末尾开始
console.log(str.substring(-3));  // "Hello World" — 负数被当作0处理
```

所以，能用 `slice` 就用 `slice`，它的行为更符合直觉。

#### substr — 已废弃，请远离！

**警告：`substr` 已被废弃！请使用 `slice` 或 `substring` 代替！**

虽然有些老代码中还能看到 `substr`，但它已经在 ECMAScript 规范中被标记为过时：

```javascript
const str = "Hello World";

// ⚠️ 废弃的语法，强烈不推荐！
console.log(str.substr(0, 5));   // "Hello" — 从0开始，长度为5
console.log(str.substr(6, 5));    // "World" — 从6开始，长度为5
```

`substr` 的第二个参数是**长度**而不是结束位置，这种不一致性是它被废弃的原因之一。

**三者对比总结：**

| 方法 | 第二个参数 | 负数支持 | 推荐程度 |
|------|-----------|---------|---------|
| `slice` | 结束位置（不含） | ✅ 支持 | ⭐⭐⭐ 强烈推荐 |
| `substring` | 结束位置（不含） | ❌ 负数当0 | ⭐⭐ 可用 |
| `substr` | 长度 | ❌ 负数当0 | ❌ 已废弃 |

---

### split：分割为数组

`split` 方法是字符串分割成数组的神器，它根据你指定的分隔符把字符串拆成数组：

```javascript
const email = "user@example.com";

console.log(email.split("@"));    // ["user", "example.com"]
console.log(email.split("."));    // ["user@example", "com"]

const sentence = "我 爱 JavaScript";
console.log(sentence.split(" ")); // ["我", "爱", "JavaScript"]

// 如果分隔符不存在，返回包含整个字符串的数组
console.log("hello".split("-"));  // ["hello"]

// 空字符串分隔符会把字符串拆成单个字符数组
console.log("hello".split(""));   // ["h", "e", "l", "l", "o"]
```

`split` 还可以接受第二个参数，限制返回数组的长度：

```javascript
const numbers = "1,2,3,4,5";

console.log(numbers.split(","));       // ["1", "2", "3", "4", "5"]
console.log(numbers.split(",", 3));    // ["1", "2", "3"] — 只返回前3个
console.log(numbers.split(",", 9));    // ["1", "2", "3", "4", "5"] - 不够9个, 返回全部的5个
```

`split` 方法在处理 CSV 数据、解析路径、拆分单词等场景中非常有用：

```javascript
// 解析 URL
const url = "https://www.example.com/path/to/page";
const parts = url.split("/");
console.log(parts);
// ["https:", "", "www.example.com", "path", "to", "page"]

// 解析文件名和扩展名
const filename = "report.2024.pdf";
const lastDotIndex = filename.lastIndexOf(".");
const name = filename.substring(0, lastDotIndex);
const ext = filename.substring(lastDotIndex + 1);
console.log(name, ext); // "report.2024" "pdf"

// 更优雅的方式：用 split
const [baseName, ...rest] = "report.2024.pdf".split(".");
const extension = rest.join(".");
console.log(baseName, extension); // "report" "2024.pdf"
```

> 💡 小技巧：配合数组的 `join` 方法，可以实现字符串的替换和重组：
> ```javascript
> const str = "Hello World";
> const result = str.split("").reverse().join(""); // "dlroW olleH" — 字符串反转！
> ```
>
> ⚠️ 不过 `split("")` 是按编码单元切的，只要字符串里有 emoji，反转结果就会被切碎。要处理任意文本，请写成 `[...str].reverse().join("")`（详见 9.5 节）。

---

## 9.4 转换与格式化

### toUpperCase / toLowerCase / toLocaleUpperCase

这三个方法是字符串的大小写转换工具，相当于字符串的"变形金刚"。

#### toUpperCase — 全部变大写

```javascript
const str = "Hello World";

console.log(str.toUpperCase()); // "HELLO WORLD"
```

#### toLowerCase — 全部变小写

```javascript
const str = "Hello World";

console.log(str.toLowerCase()); // "hello world"
```

#### toLocaleUpperCase / toLocaleLowerCase — 本地化转换

等等，既然有 `toUpperCase`，为什么还要 `toLocaleUpperCase`？

因为世界上不是所有语言都只有 A-Z！比如：

```javascript
// 土耳其语
const str = "i";

console.log(str.toUpperCase());          // "I" — 英语思维
console.log(str.toLocaleUpperCase("tr")); // "İ" — 土耳其语：i 变成 İ（带点的 I）

// 德语
const german = "straße";

console.log(german.toUpperCase());          // "STRASSE" — 不区分语言，直接做 Unicode 大写的默认映射
console.log(german.toLocaleUpperCase("de")); // "STRASSE" — 德语里 ß 的大写同样写作 SS

// 那 toLocaleUpperCase 到底什么时候有用？看土耳其语，它把 i 的大写定为带点的 İ
const turkish = "i";
console.log(turkish.toUpperCase());            // "I"
console.log(turkish.toLocaleUpperCase("tr"));  // "İ"（带点的大写 I）
```

土耳其语有一个著名的"点I问题"——在土耳其语中，大写的 "i" 不是 "I"，而是 "İ"（带点的 I）。如果你在做国际化应用，用户名 "istay" 的大写形式应该是 "İSTAY"，而不是 "ISTAY"。

> ⚠️ 默认的 `toUpperCase()` / `toLowerCase()` 走的是「语言无关」的 Unicode 映射；一旦你的应用面向土耳其语、德语、立陶宛语等用户，大小写转换和比较就应该带上 locale。

```javascript
// 英语环境下的比较
const username = "istay";
const input = "ISTAY";
console.log(username.toUpperCase() === input.toUpperCase()); // true

// 到了土耳其语环境，用 locale 版本才符合当地习惯
console.log(username.toLocaleUpperCase("tr")); // "İSTAY"
console.log(input.toLocaleUpperCase("tr"));    // "ISTAY"（这里的 I 是原来的大写 I）

// 真正稳的大小写不敏感比较，推荐用 localeCompare 的 sensitivity 选项
console.log("İSTAY".localeCompare("istay", "tr", { sensitivity: "base" })); // 0 表示视为相同
```

---

### trim / trimStart / trimEnd

用户输入的字符串经常带有前后空格，比如从表单提交的数据、从文件读取的内容等。这些空格可能是用户不小心敲的，也可能是从其他系统带过来的，总之——你需要处理它们。

#### trim — 去掉前后空格

```javascript
const userInput = "   你好，世界！   ";

console.log("|" + userInput + "|");           // |   你好，世界！   |
console.log("|" + userInput.trim() + "|");   // |你好，世界！|
```

#### trimStart / trimEnd — 只去掉一边

有时候你只需要去掉某一边的空格：

```javascript
const str = "   Hello   ";

console.log(str.trimStart()); // "Hello   " — 只去前面
console.log(str.trimEnd());   // "   Hello" — 只去后面
```

> 💡 小技巧：这些方法不仅去空格，还会去掉制表符 `\t`、换行符 `\n` 等空白字符。

```javascript
const messy = "\n\t  Hello World  \r\n";

console.log(messy.trim()); // "Hello World"
```

---

### repeat / padStart / padEnd

#### repeat — 重复字符串

```javascript
const laugh = "Ha";

console.log(laugh.repeat(3));   // "HaHaHa"
console.log(laugh.repeat(0));  // "" — 重复0次返回空字符串
console.log("=".repeat(10));   // "==========" — 分隔线神器
```

这个方法在生成分隔线、填充字符等场景中非常有用：

```javascript
// 生成标题装饰
function decorate(title) {
  const line = "=".repeat(30);
  return `${line}\n${title}\n${line}`;
}

console.log(decorate("欢迎来到JavaScript世界"));
// ==============================
// 欢迎来到JavaScript世界
// ==============================
```

#### padStart / padEnd — 字符串填充

`padStart` 在字符串**前面**填充，直到达到指定长度；`padEnd` 在字符串**后面**填充。

```javascript
const num = "5";

console.log(num.padStart(3, "0"));    // "005" — 前面补0
console.log(num.padStart(5, "*"));    // "****5" — 前面补*

console.log(num.padEnd(3, "0"));      // "500" — 后面补0
console.log("5".padEnd(5, "."));      // "5...."
```

经典的用法是格式化数字显示：

```javascript
// 格式化时间
const hours = "9";
const minutes = "3";

console.log(`${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`); // "09:03"

// 格式化订单号
const orderId = "12345";
console.log(orderId.padStart(8, "0")); // "00012345"

// 对齐输出
const items = ["苹果", "香蕉", "火龙果"];
items.forEach(item => {
  console.log(`${item.padEnd(6, ' ')}: ¥10`);
});
// 苹果   : ¥10
// 香蕉   : ¥10
// 火龙果 : ¥10
```

---

### concat / 拼接

`concat` 方法用于连接两个或多个字符串，返回一个新的字符串：

```javascript
const str1 = "Hello";
const str2 = " ";
const str3 = "World";

console.log(str1.concat(str2, str3)); // "Hello World"
```

但是，等等！我们不是有 `+` 运算符和模板字符串吗？

```javascript
const a = "Hello";
const b = "World";

// 三种方式对比
console.log(a + b);                   // "HelloWorld" — 加号拼接
console.log(`${a} ${b}`);             // "Hello World" — 模板字符串
console.log(a.concat(" ", b));        // "Hello World" — concat 方法
```

实际上，`+` 运算符和模板字符串是更常用的选择，因为：
1. 语法更简洁
2. 性能更好（JavaScript 引擎对 `+` 做了大量优化）
3. 代码可读性更高

`concat` 的存在更多是为了与其他编程语言的 API 保持一致性。某些情况下，如果你有一个字符串数组需要拼接，用 `join` 方法更合适：

```javascript
const parts = ["path", "to", "file"];

console.log(parts.join("/"));         // "path/to/file"
console.log(parts.join(""));          // "pathtofile"
console.log(["a", "b", "c"].join());  // "a,b" — 默认用逗号连接
```

---

### localeCompare：本地化比较

最后登场的是 `localeCompare`——这个方法的名字听起来很高大上，确实，它也确实是用于做**本地化字符串比较**的。

什么叫本地化比较？就是考虑语言习惯的比较。比如德语中，"ä" 应该被认为在 "a" 之后（或者等同于 "ae"）；瑞典语中，"ä" 在 "z" 之后。这可不是简单的 Unicode 编码比较能搞定的！

```javascript
const str1 = "ä";
const str2 = "z";

console.log(str1.localeCompare(str2));              // -1（在德语中，ä < z）
console.log(str1.localeCompare(str2, "de"));         // -1（德语）
console.log(str1.localeCompare(str2, "sv"));         // 1（瑞典语，ä > z）
```

`localeCompare` 返回值规则：
- 返回 **负数**：第一个字符串在第二个前面
- 返回 **0**：两个字符串相等
- 返回 **正数**：第一个字符串在第二个后面

```javascript
const names = ["张三", "李四", "王五", "赵六"];

// 按拼音排序
console.log(names.sort((a, b) => a.localeCompare(b, "zh")));
// ["李四", "王五", "张三", "赵六"]
```

> 🎯 小技巧：如果你需要对大量字符串进行排序，`localeCompare` 是首选！它考虑了语言习惯，排序结果更符合人类阅读习惯。
>
> 不过要注意，`localeCompare` 每次比较都要走 ICU 的本地化规则，比直接用 `a > b` 这种方法慢不少。当排序的数据量很大、又在热路径上时，可以先用 `Intl.Collator` 建一个比较器复用，它的开销比反复调用 `localeCompare` 小得多。

```javascript
// 大数据量排序的正确姿势：复用 Intl.Collator
const collator = new Intl.Collator("zh");
const words = ["张三", "李四", "王五", "赵六"];

words.sort((a, b) => collator.compare(a, b));
console.log(words); // ["李四", "王五", "张三", "赵六"]

// localeCompare 支持的选项比 > < 丰富得多
console.log("2".localeCompare("10", "en", { numeric: true })); // -1（按数字大小比，而不是按字符）
console.log("a".localeCompare("A", "en", { sensitivity: "base" })); // 0（忽略大小写差异）
```

---

## 9.5 字符串与 Unicode：那些年我们踩过的坑

前面反复提到「编码单元」和「码点」，这一节把它们串起来，顺便补齐几个很实用但容易被忽略的 API。

### 为什么会踩坑

JavaScript 的字符串底层是 UTF-16。BMP（基本多文种平面，码点 U+0000 ~ U+FFFF）里的字符占 1 个编码单元，而 emoji、部分生僻汉字、数学符号等超出 BMP 的字符要占 2 个（一对「代理项」）。

```javascript
const s = "a🎉b";

console.log(s.length);          // 4（不是 3！🎉 占了 2 格）
console.log(s[1]);              // "\uD83C" —— 半个 emoji，控制台看起来像乱码
console.log(s.charAt(1));       // "\uD83C"（同样是半截）
console.log(s.codePointAt(1));  // 127881（从这个位置能读到完整码点，但只对这种恰好落在高位的情形有效）

// 正确的遍历方式
console.log([...s]);            // ["a", "🎉", "b"]
console.log(Array.from(s));     // 同上
```

```javascript
// 反面教材：用 length / split("") 数长度、反转字符串
const emoji = "👍🏽"; // 一个 emoji 加上肤色修饰符
console.log(emoji.length);           // 4
console.log([...emoji].length);      // 2（手势 + 肤色修饰符）

// 用 split("") 反转会把代理对拆散，得到一堆乱码
console.log("🎉a".split("").reverse().join("")); // "a" 后面跟着两个乱码字符（代理对被切碎了）
// 按码点反转就安全得多
console.log([..."🎉a"].reverse().join(""));      // "a🎉"

// 但严格来说，「字素簇」才是最接近人眼认知的「一个字符」
console.log("👍🏽".length);                        // 4
console.log([..."👍🏽"].length);                   // 2
// 用 Intl.Segmenter 按字素簇切分（Node 16+ / 现代浏览器）
const segmenter = new Intl.Segmenter("zh", { granularity: "grapheme" });
console.log([...segmenter.segment("👍🏽🇨🇳")].map(seg => seg.segment)); // [ '👍🏽', '🇨🇳' ]
```

### at()：支持负索引的取值（ES2022）

`charAt` 不认负数，`str[-1]` 是 `undefined`，于是以前只能写 `str[str.length - 1]`。现在有了 `at()`：

```javascript
const str = "Hello";

console.log(str.at(0));   // "H"
console.log(str.at(-1));  // "o"（倒数第一个）
console.log(str.at(-2));  // "l"
console.log(str.at(99));  // undefined（越界返回 undefined）
console.log(str.charAt(-1)); // ""（charAt 不认负数，返回空字符串）
console.log(str[-1]);     // undefined（下标写法不支持负数）

// 数组也有 at()
console.log([1, 2, 3].at(-1)); // 3
```

### match / matchAll：一次性拿到所有匹配

```javascript
const text = "2024-01-02 下单，2024-02-15 发货，2024-03-20 收货";

// match + g：返回所有匹配的字符串，但拿不到分组信息
console.log(text.match(/\d{4}-\d{2}-\d{2}/g));
// ["2024-01-02", "2024-02-15", "2024-03-20"]

// matchAll：返回迭代器，每一项都带 index 和 groups，信息最全
for (const m of text.matchAll(/(\d{4})-(\d{2})-(\d{2})/g)) {
  console.log(m[0], "年:", m[1], "位置:", m.index);
}
// 2024-01-02 年: 2024 位置: 0
// 2024-02-15 年: 2024 位置: 14
// 2024-03-20 年: 2024 位置: 28
// 注意：matchAll 的正则必须带 g 标志，否则会抛 TypeError

// 想快速拿到「所有分组」的数组，可以配合扩展运算符
const all = [...text.matchAll(/(\d{4})-(\d{2})-(\d{2})/g)].map(m => m.slice(1));
console.log(all); // [["2024","01","02"], ["2024","02","15"], ["2024","03","20"]]
```

### String.raw：让转义符保持原样

```javascript
// 反斜杠在普通字符串里是转义符，写路径很痛苦
console.log("C:\\new\\test");        // C:\new\test（要写两层反斜杠）
console.log(String.raw`C:\new\test`); // C:\new\test（String.raw 原样保留）

// 注意：String.raw 不会处理 \n 之类的转义 —— 它就是要原样
console.log(String.raw`第一行\n第二行`); // 第一行\n第二行（字面量，不是换行）
```

### normalize：统一 Unicode 的写法

同一个「é」，可能是单个码点 U+00E9，也可能是 e + 组合重音 U+0301。两者肉眼一样，但 `===` 会判不等：

```javascript
const nfc = "é".normalize("NFC");  // 合成形式，长度 1
const nfd = "é".normalize("NFD");  // 分解形式，长度 2

console.log(nfc.length, nfd.length); // 1 2
console.log(nfc === nfd);            // false（字面量不同）
console.log(nfc.normalize() === nfd.normalize()); // true（都归一化成 NFC）

// 实践建议：比较、查找、存储用户输入前，先统一 normalize("NFC")
```

### 其他值得记一笔的细节

```javascript
// 1. repeat 的边界情况
console.log("ab".repeat(2.9)); // "abab"（小数会被截断）
console.log("ab".repeat(0));   // ""
// "ab".repeat(-1);            // RangeError: Invalid count value

// 2. padStart / padEnd 的长度也按编码单元算，emoji 会「多占格」
console.log("🎉".padStart(3, "-")); // "-🎉"（🎉 已占 2 格，所以只补 1 个字符）
console.log("🎉".length);           // 2，所以 padStart(3) 只会补 1 个字符

// 3. String.prototype 上的方法对原始字符串调用时会自动装箱，但别去改原型
console.log("abc".toUpperCase()); // "ABC"

// 4. 用 includes / startsWith / endsWith 时，第二个参数是「起始位置」
console.log("abcabc".includes("abc", 1)); // true（从索引 1 开始找）
```

> 一句话总结：处理 ASCII 之外的文本时，先问自己一句「这里是按编码单元、码点还是字素簇在数？」——大多数莫名其妙的 bug 都源于这三者的混淆。

---

## 本章小结

字符串是 JavaScript 中最常用的数据类型之一，可以说是无处不在。本章我们学习了：

1. **基础操作**：模板字符串（反引号 + `${}`）让字符串拼接优雅无比；模板标签函数让你可以自定义模板解析逻辑；`length` / `charAt` / `charCodeAt` 让你能获取字符串的长度和字符信息；最重要的是——字符串是不可变的！

2. **查找与替换**：`indexOf` / `lastIndexOf` 从前后查找子串；`includes` / `startsWith` / `endsWith` 判断是否包含/开头/结尾（`endsWith` 的第二个参数是「截断长度」，语义和 `startsWith` 相反）；`search` 支持正则但忽略 `g`；`replace` 只替换第一个匹配，`replaceAll` 替换全部且传正则时必须带 `g`。

3. **提取与分割**：`slice` / `substring` 提取子串（`substr` 已废弃）；`slice` 支持负数、`substring` 会自动交换参数并把负数当 0；`split` 把字符串分割成数组，反转字符串记得用 `[...str]` 而不是 `split("")`。

4. **转换与格式化**：`toUpperCase` / `toLowerCase` 走语言无关映射，面向土耳其语等场景要用 `toLocaleUpperCase` / `toLocaleLowerCase`；`trim` 系列去空白；`repeat` / `padStart` / `padEnd` 填充；`concat` 拼接；`localeCompare` 做本地化比较，大数据量排序请复用 `Intl.Collator`，需要数字感知排序用 `{ numeric: true }`。

5. **Unicode 与工具方法**：`length` 数的是 UTF-16 编码单元，emoji 会占 2 格甚至更多；`codePointAt` / `String.fromCodePoint` 处理完整码点；`at(-1)` 取末尾；`matchAll` 拿到带位置的完整匹配；`String.raw` 写路径；`normalize("NFC")` 统一等价字符；`Intl.Segmenter` 按字素簇切分才是人眼意义上的「一个字符」。

字符串的方法还有很多，但掌握这些核心方法足够让你在 JavaScript 世界里自由翱翔了！

> 📊 图示：字符串方法分类
>
> ```mermaid
> graph TD
>     A[字符串 String] --> B[基础操作]
>     A --> C[查找与替换]
>     A --> D[提取与分割]
>     A --> E[转换与格式化]
>
>     B --> B1["模板字符串（反引号 + 表达式）"]
>     B --> B2[模板标签函数]
>     B --> B3[length / charAt / charCodeAt]
>     B --> B4[不可变性]
>
>     C --> C1[indexOf / lastIndexOf]
>     C --> C2[includes / startsWith / endsWith]
>     C --> C3[search]
>     C --> C4[replace / replaceAll]
>
>     D --> D1[slice / substring]
>     D --> D2[substr ⚠️已废弃]
>     D --> D3[split]
>
>     E --> E1[大小写转换]
>     E --> E2[trim 系列]
>     E --> E3[repeat / padStart / padEnd]
>     E --> E4[concat / localeCompare]
>
>     A --> F[Unicode 与工具方法]
>     F --> F1[codePointAt / fromCodePoint]
>     F --> F2["at(-1)"]
>     F --> F3[matchAll]
>     F --> F4[String.raw]
>     F --> F5["normalize / Intl.Segmenter"]
> ```

---

**下章预告**：下一章我们将学习 JavaScript 的数学与数值处理——`Math` 对象、进制转换、精度问题...准备好了吗？ 🚀
