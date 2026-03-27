+++
title = "第 35 章 错误处理"
weight = 350
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 35 章 错误处理

程序不可能永远正确运行。错误处理就是让程序在出问题时能够优雅地"认错"，而不是直接崩溃。

## 35.1 错误处理基础

### try...catch / try...catch...finally

```javascript
try {
    // 尝试执行这段代码
    const result = riskyOperation();
    console.log('操作成功：', result);
} catch (error) {
    // 如果出错，执行这里
    console.error('出错了：', error.message);
} finally {
    // 不管成功还是失败，都会执行
    console.log('无论成功失败，我都会执行');
}
```

### Error 对象：message / name / stack

```javascript
try {
    throw new Error('出错了！');
} catch (error) {
    console.log('错误信息：', error.message); // 错误信息
    console.log('错误名称：', error.name);   // Error
    console.log('错误堆栈：', error.stack);   // 详细错误位置
}
```

### 内置错误类型：ReferenceError / TypeError / SyntaxError / RangeError / URIError

```javascript
// ReferenceError：引用错误
try {
    console.log(undefinedVariable); // 未定义的变量
} catch (e) {
    console.log(e.name); // 打印结果: ReferenceError
}

// TypeError：类型错误
try {
    null.method(); // null 没有方法
} catch (e) {
    console.log(e.name); // 打印结果: TypeError
}

// SyntaxError：语法错误（只能在解析阶段捕获，不能在 try...catch 中捕获）
// try {
//     eval('const = 1'); // 语法错误无法捕获
// } catch (e) {
//     console.log(e.name);
// }

// RangeError：范围错误
try {
    const arr = new Array(-1); // 数组长度不能为负数
} catch (e) {
    console.log(e.name); // 打印结果: RangeError
}

// URIError：URI 错误
try {
    decodeURIComponent('%'); // 无效的 URI 编码
} catch (e) {
    console.log(e.name); // 打印结果: URIError
}
```

### throw：手动抛出

```javascript
// 抛出字符串
throw '出错了！';

// 抛出数字
throw 404;

// 抛出对象
throw {
    code: 'NOT_FOUND',
    message: '资源未找到'
};

// 抛出 Error 对象
throw new Error('出错了！');
```

### Error.cause（ES2022+）

```javascript
try {
    try {
        JSON.parse('invalid json');
    } catch (e) {
        // 在捕获错误时，附加 cause 信息
        throw new Error('解析失败', { cause: e });
    }
} catch (e) {
    console.log(e.message); // 打印结果: 解析失败
    console.log(e.cause); // 打印结果: SyntaxError: Unexpected token 'i'
}
```

### 自定义错误类型

```javascript
class ValidationError extends Error {
    constructor(message, field) {
        super(message);
        this.name = 'ValidationError';
        this.field = field;
    }
}

function validateAge(age) {
    if (typeof age !== 'number') {
        throw new ValidationError('年龄必须是数字', 'age');
    }
    if (age < 0 || age > 150) {
        throw new ValidationError('年龄必须在 0-150 之间', 'age');
    }
}

try {
    validateAge('abc');
} catch (e) {
    if (e instanceof ValidationError) {
        console.log('验证错误：', e.message, '字段：', e.field);
    } else {
        console.log('其他错误：', e.message);
    }
}
```

下一节，我们来学习异步错误处理！

## 35.2 异步错误处理

### try...catch 对 Promise 无效（同步代码中捕获）

```javascript
// ❌ try...catch 不能捕获异步代码中的错误
try {
    setTimeout(function() {
        throw new Error('异步错误！');
    }, 1000);
} catch (e) {
    console.log('捕获到了？'); // 不会执行！
}
console.log('try...catch 之外的代码'); // 立即执行
```

### async/await 的错误处理：try...catch

```javascript
async function fetchData() {
    try {
        const response = await fetch('https://invalid-url');
        const data = await response.json();
        return data;
    } catch (error) {
        console.log('请求失败：', error.message);
        return null;
    }
}

fetchData();
```

### Promise 的 .catch()

```javascript
fetch('https://invalid-url')
    .then(function(response) {
        return response.json();
    })
    .catch(function(error) {
        console.log('请求失败：', error.message);
    });
```

下一节，我们来学习全局错误处理！

## 35.3 全局错误处理

### window.onerror

```javascript
window.onerror = function(message, source, lineno, colno, error) {
    console.log('错误信息：', message);
    console.log('错误来源：', source);
    console.log('行号：', lineno);
    console.log('列号：', colno);
    console.log('错误对象：', error);
    
    // 返回 true 表示已处理，不再向上抛出
    return true;
};

// 触发错误
// window.onerror 会被调用
```

### unhandledrejection：未处理的 Promise rejection

```javascript
// 当 Promise 被 reject 但没有 .catch() 处理时触发
window.addEventListener('unhandledrejection', function(event) {
    console.log('未处理的 Promise 错误：');
    console.log('错误对象：', event.reason);
    
    // 阻止默认行为（浏览器控制台警告）
    event.preventDefault();
});

Promise.reject(new Error('未处理的错误！'));
```

---

## 本章小结

本章我们学习了错误处理：

1. **try...catch**：捕获同步代码中的错误。
2. **Error 对象**：包含 message、name、stack 信息。
3. **内置错误类型**：ReferenceError、TypeError、SyntaxError、RangeError、URIError。
4. **throw**：手动抛出错误。
5. **异步错误处理**：Promise 用 .catch()，async/await 用 try...catch。
6. **全局错误处理**：window.onerror 和 unhandledrejection。

错误处理是写出健壮代码的关键。学会优雅地处理错误，你的程序就不会轻易崩溃了。

下一章，我们要学习调试——让 bug 无所遁形！
