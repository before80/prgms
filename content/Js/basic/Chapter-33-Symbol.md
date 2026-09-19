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

两个使用上的注意点：

```javascript
// ❌ Symbol 不是构造函数，不能用 new
// new Symbol(); // TypeError: Symbol is not a constructor

// ✅ 需要包装对象时用 Object()
const boxed = Object(Symbol('s'));
console.log(typeof boxed);      // 打印结果: object
console.log(typeof Symbol('s')); // 打印结果: symbol（这才是常态）

// Symbol 不能参与算术运算和隐式字符串拼接，会直接抛类型错误
// Symbol('s') + '';  // TypeError: Cannot convert a Symbol value to a string
console.log(String(Symbol('s'))); // 打印结果: Symbol(s)（显式转换可以）
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

### Symbol 属性不会被常规遍历看到

先澄清一个流传很广的错误说法：**Symbol 属性默认是可枚举的**，只是 `Object.keys`、`for...in`、`JSON.stringify` 这些「字符串键专用」的接口按规范跳过了它。

```javascript
const obj = {
    name: '小明',
    age: 18
};

const secret = Symbol('secret');
obj[secret] = '隐藏的信息';

console.log(Object.keys(obj)); // 打印结果: ['name', 'age']（Symbol 键不在其中）
console.log(Object.getOwnPropertySymbols(obj)); // 打印结果: [Symbol(secret)]

// 它实际上是可枚举的
console.log(Object.getOwnPropertyDescriptor(obj, secret).enumerable); // 打印结果: true

// 想拿到全部键（字符串键 + Symbol 键），用 Reflect.ownKeys
console.log(Reflect.ownKeys(obj)); // 打印结果: ['name', 'age', Symbol(secret)]
```

这带来几个实用且常被忽略的行为差异：

```javascript
const id = Symbol('id');
const source = { [id]: 1, name: 'A' };

// JSON.stringify 会丢掉 Symbol 键
console.log(JSON.stringify(source)); // 打印结果: {"name":"A"}

// 但 Object.assign 和展开运算符会复制 Symbol 键
console.log(Object.assign({}, source)[id]); // 打印结果: 1
console.log({ ...source }[id]);             // 打印结果: 1

// 深拷贝的经典坑：JSON.parse(JSON.stringify(x)) 会把 Symbol 键整个抹掉
console.log(JSON.parse(JSON.stringify(source))[id]); // 打印结果: undefined
```

另一个常见误解是把 Symbol 当成「真正的私有属性」。它只是**不容易被误用**：拿不到这个 Symbol 就无法访问，但只要能拿到对象，就能用 `Object.getOwnPropertySymbols()` 把键全列出来。想要外部彻底访问不到，用 `#私有字段`。

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

准确地说，`replace`、`replaceAll`、`match`、`matchAll`、`search`、`split` 这些字符串方法都会先检查参数上有没有对应的 Symbol 方法，有就交给它执行。这就是「实现协议来接管内置行为」。

```javascript
// 自定义替换：把每个 'HELLO' 换掉
const asterisk = {
    [Symbol.replace](target, replacement) {
        return target.toUpperCase().split('HELLO').join(replacement);
    }
};
console.log('hello hello'.replace(asterisk, 'Hi')); // 打印结果: Hi Hi

// 自定义 split：逗号和分号都当作分隔符
const splitWay = {
    [Symbol.split](target) {
        return target.split(/[,;]/);
    }
};
console.log('a,b;c'.split(splitWay)); // 打印结果: ['a', 'b', 'c']

// 自定义 search
const onlyDigits = {
    [Symbol.search](target) {
        return target.search(/\d+/);
    }
};
console.log('abc123'.search(onlyDigits)); // 打印结果: 3
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

### 其他值得知道的内置 Symbol

| 内置 Symbol | 作用 | 常见出现场景 |
| --- | --- | --- |
| `Symbol.asyncIterator` | 异步迭代协议 | `for await...of`、异步生成器 |
| `Symbol.species` | 指定派生对象的构造函数 | 子类化 Array / Promise 时控制 `map`、`slice` 返回什么类型 |
| `Symbol.unscopables` | 把某些属性从 `with` 作用域里排除 | 历史遗留，现代代码不要依赖 |
| `Symbol.matchAll` | 自定义 `String.prototype.matchAll` 的行为 | 自定义匹配器 |

```javascript
// 异步迭代器：让对象可以用 for await...of 遍历
const asyncNumbers = {
    [Symbol.asyncIterator]() {
        let i = 0;
        return {
            async next() {
                if (i < 3) {
                    await new Promise((r) => setTimeout(r, 10));
                    return { value: i++, done: false };
                }
                return { done: true };
            },
        };
    },
};

(async () => {
    for await (const n of asyncNumbers) {
        console.log(n); // 依次打印 0 1 2
    }
})();
```

### 跨环境的坑：Symbol.for 的「全局」是按环境算的

`Symbol.for` 的注册表只在一个运行环境内共享：

- 同一个页面的不同 iframe 之间不共享，各自的 `Symbol.for('x')` 互不相等；
- 主线程与 Web Worker 不共享；
- Node.js 里同一进程内的模块共享，不同进程（如 cluster 起的多个进程）之间不共享；
- Symbol 本身不能跨环境传递，`postMessage` 传 Symbol 会抛错。

所以 `Symbol.for` 适合「同一环境内多个库想共享同一个键」的场景，比如给 DOM 节点挂内部状态。跨进程通信要用字符串、数组等结构化克隆支持的类型。

---

## 本章小结

本章我们学习了 Symbol：

1. **Symbol 基础**：`Symbol()` 创建独一无二的值，`Symbol.for` / `Symbol.keyFor` 使用全局注册表，Symbol 不能 `new`、不能隐式转字符串。
2. **遍历差异**：Symbol 属性不会被 `Object.keys` / `for...in` / `JSON.stringify` 看到，但**默认是可枚举的**，`Object.assign`、展开运算符、`Reflect.ownKeys` 都会带上它。
3. **内置 Symbol**：`iterator` / `asyncIterator` / `toStringTag` / `hasInstance` / `toPrimitive` / `replace` / `split` / `search` / `isConcatSpreadable` 等，通过实现协议改变对象与内置 API 的交互方式。
4. **使用边界**：Symbol 不是真私有（可被反射），`Symbol.for` 的全局范围只限于当前运行环境。

Symbol 是 JavaScript 的"秘密武器"，可以创建独一无二的属性名，避免属性名冲突，是实现协议和元编程的重要工具。

下一章，我们要学习正则表达式——字符串匹配的"神器"！
