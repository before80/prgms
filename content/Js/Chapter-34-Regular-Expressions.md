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
console.log(str.search(/\d+/)); // 打印结果: 14

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

// $`：匹配前面的部分
console.log('hello world'.replace(/world/, '$`hello '));
// 打印结果: hello hello world

// $'：匹配后面的部分
console.log('hello world'.replace(/hello/, "$' world"));
// 打印结果: hello world world

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

### URL 参数解析

```javascript
const url = 'https://example.com/search?q=javascript&page=1';

const params = {};
url.match(/[?&]([^&=]+)=([^&]*)/g).forEach(function(match) {
    const [, key, value] = match.split('=');
    params[decodeURIComponent(key)] = decodeURIComponent(value);
});

console.log(params); // 打印结果: { q: 'javascript', page: '1' }
```

### 敏感词替换

```javascript
const sensitiveWords = ['暴力', '色情', '赌博'];

function filterSensitive(text) {
    const regex = new RegExp(sensitiveWords.join('|'), 'g');
    return text.replace(regex, '***');
}

console.log(filterSensitive('这是一段包含暴力的文字')); // 打印结果: 这是一段包含***的文字
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

---

## 本章小结

本章我们学习了正则表达式：

1. **正则基础**：创建正则（字面量/RegExp）、test/exec 方法。
2. **字符与元字符**：字符类、量词、贪婪/非贪婪、边界。
3. **分组与引用**：捕获分组、非捕获分组、反向引用、或运算。
4. **字符串方法**：match、search、replace、split 与正则的结合。
5. **常用场景**：手机号、邮箱、URL参数、千分位、密码强度等验证。

正则表达式是 JavaScript 开发中的"瑞士军刀"，掌握它能让你的字符串处理能力大幅提升。

下一章，我们要学习错误处理——让程序优雅地"容错"！
