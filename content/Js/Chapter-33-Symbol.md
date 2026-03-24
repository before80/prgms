+++
title = "第 33 章 Symbol"
weight = 330
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 33 章 Symbol

Symbol 是 ES6 引入的一种新数据类型，代表一个"独一无二"的值。就像每个人都有自己的身份证号一样，每个 Symbol 都是唯一的。

## 33.1 Symbol 基础

### Symbol()：创建独一无二的值

```javascript
// 创建 Symbol
const s1 = Symbol();
const s2 = Symbol();

console.log(s1 === s2); // 打印结果: false（每次 Symbol() 都是独一无二的）

// Symbol 可以有描述
const s3 = Symbol('mySymbol');
const s4 = Symbol('mySymbol');

console.log(s3 === s4); // 打印结果: false（描述相同，但值不同）
console.log(s3.description); // 打印结果: mySymbol
```

### Symbol.for / Symbol.keyFor：全局注册表

Symbol.for 创建在全局注册表中的 Symbol，同一个 key 会返回同一个 Symbol。

```javascript
// Symbol.for：在全局注册表中查找或创建
const s1 = Symbol.for('globalSymbol');
const s2 = Symbol.for('globalSymbol');

console.log(s1 === s2); // 打印结果: true（同一个 key 返回同一个值）

// Symbol.keyFor：从全局注册表中获取 key
const key = Symbol.keyFor(s1);
console.log(key); // 打印结果: globalSymbol

// 普通 Symbol 不在全局注册表中
const s3 = Symbol('notGlobal');
console.log(Symbol.keyFor(s3)); // 打印结果: undefined
```

### Symbol 不可枚举

```javascript
const obj = {
    name: '小明',
    age: 18
};

const secret = Symbol('secret');
obj[secret] = '隐藏的信息';

console.log(Object.keys(obj)); // 打印结果: ['name', 'age']（Symbol 属性不可枚举）
console.log(Object.getOwnPropertySymbols(obj)); // 打印结果: [Symbol(secret)]
```

下一节，我们来学习内置 Symbol！

## 33.2 内置 Symbol

### Symbol.iterator：可迭代协议

Symbol.iterator 让对象变成可迭代的，可以用 for...of 遍历。

```javascript
const myArray = {
    items: ['苹果', '香蕉', '橙子'],
    [Symbol.iterator]: function() {
        let index = 0;
        const self = this;
        return {
            next: function() {
                if (index < self.items.length) {
                    return {
                        value: self.items[index++],
                        done: false
                    };
                }
                return { done: true };
            }
        };
    }
};

for (const item of myArray) {
    console.log(item); // 打印结果: 苹果 香蕉 橙子
}
```

### Symbol.toStringTag：自定义 toString 结果

```javascript
const person = {
    [Symbol.toStringTag]: 'Person'
};

console.log(Object.prototype.toString.call(person)); // 打印结果: [object Person]
```

### Symbol.hasInstance：自定义 instanceof 行为

```javascript
class Even {
    static [Symbol.hasInstance](instance) {
        return typeof instance === 'number' && instance % 2 === 0;
    }
}

console.log(2 instanceof Even); // 打印结果: true
console.log(3 instanceof Even); // 打印结果: false
```

### Symbol.toPrimitive：自定义类型转换

```javascript
const obj = {
    value: 42,
    [Symbol.toPrimitive](hint) {
        if (hint === 'number') {
            return this.value;
        }
        if (hint === 'string') {
            return String(this.value);
        }
        return this.value;
    }
};

console.log(+obj); // 打印结果: 42（hint = 'number'）
console.log(String(obj)); // 打印结果: 42（hint = 'string'）
console.log(obj + ''); // 打印结果: 42（hint = 'default'）
```

### Symbol.replace / Symbol.split：自定义字符串方法

```javascript
const replacer = {
    [Symbol.replace](target, replacement) {
        return target.toUpperCase().replace('HELLO', replacement);
    }
};

console.log('hello'.replace(replacer, 'Hi')); // 打印结果: Hi
```

### Symbol.isConcatSpreadable：控制 concat 展开

```javascript
const array = [1, 2];
const likeArray = {
    0: 'a',
    1: 'b',
    length: 2,
    [Symbol.isConcatSpreadable]: true
};

console.log([].concat(array, likeArray)); // 打印结果: [1, 2, 'a', 'b']
```

---

## 本章小结

本章我们学习了 Symbol：

1. **Symbol 基础**：创建独一无二的值，Symbol.for/keyFor 全局注册表，不可枚举。
2. **内置 Symbol**：Symbol.iterator、Symbol.toStringTag、Symbol.hasInstance、Symbol.toPrimitive 等，让对象具有特殊行为。

Symbol 是 JavaScript 的"秘密武器"，可以创建独一无二的属性名，避免属性名冲突，是实现协议和元编程的重要工具。

下一章，我们要学习正则表达式——字符串匹配的"神器"！
