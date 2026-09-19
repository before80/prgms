+++
title = "第 32 章 Proxy 与 Reflect"
weight = 320
date = "2026-03-24T22:08:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 32 章 Proxy 与 Reflect

Proxy 和 Reflect 是 ES6 引入的两个高级特性。Proxy 就像一个"拦截器"，可以拦截对对象的各种操作；Reflect 是 Object 的"替代者"，提供了更合理的操作对象的方法。

## 32.1 Proxy

### 概念：代理器，拦截对象的所有操作

Proxy 就像一个"中间人"——你不能直接访问对象，而是通过 Proxy 来访问，Proxy 可以在访问过程中"动手脚"。

```javascript
const target = { name: '小明', age: 18 };

const proxy = new Proxy(target, {
    // get 拦截读取操作
    get: function(target, property, receiver) {
        console.log('读取了属性：' + property);
        return target[property];
    },
    
    // set 拦截写入操作
    set: function(target, property, value, receiver) {
        console.log('设置了属性：' + property + ' = ' + value);
        target[property] = value;
        return true;
    }
});

console.log(proxy.name);  // 触发 get
proxy.age = 20;          // 触发 set
```

### new Proxy(target, handler)

```javascript
// target：被代理的目标对象
// handler：代理配置对象，包含各种拦截函数

const target = { message: 'Hello' };
const proxy = new Proxy(target, {
    // 拦截读取属性
    get(target, prop, receiver) {
        return target[prop];
    },
    // 拦截写入属性
    set(target, prop, value, receiver) {
        target[prop] = value;
        return true;
    }
});
```

### get / set：属性读写拦截

```javascript
const user = {};

const proxy = new Proxy(user, {
    get: function(target, property, receiver) {
        if (!(property in target)) {
            throw new Error('属性 ' + property + ' 不存在');
        }
        return target[property];
    },
    
    set: function(target, property, value, receiver) {
        if (typeof value !== 'string') {
            throw new Error('属性值必须是字符串');
        }
        target[property] = value;
        return true;
    }
});

proxy.name = '小明'; // 成功
console.log(proxy.name); // 打印结果: 小明

// proxy.age = 18;      // 报错：属性值必须是字符串
// console.log(proxy.age); // 报错：属性 age 不存在

// 还有一个容易忽略的细节：set 拦截器必须返回一个布尔值
// 返回 false（或在严格模式下返回假值）会让赋值直接抛 TypeError，
// 而不是「静默地什么都不做」
```

### has：in 运算符拦截

```javascript
const target = { name: '小明', age: 18 };

const proxy = new Proxy(target, {
    has: function(target, property) {
        console.log('检查属性是否存在：' + property);
        return property in target;
    }
});

console.log('name' in proxy); // 触发 has，打印结果: true
console.log('gender' in proxy); // 触发 has，打印结果: false
```

### deleteProperty：delete 拦截

```javascript
const target = { name: '小明', age: 18 };

const proxy = new Proxy(target, {
    deleteProperty: function(target, property) {
        console.log('尝试删除属性：' + property);
        delete target[property];
        return true;
    }
});

delete proxy.name; // 触发 deleteProperty
console.log(target); // 打印结果: { age: 18 }
```

### apply：函数调用拦截

```javascript
function sum(a, b) {
    return a + b;
}

const proxySum = new Proxy(sum, {
    apply: function(target, thisArg, args) {
        console.log('调用函数，参数：', args);
        return target.apply(thisArg, args);
    }
});

console.log(proxySum(3, 5)); // 打印结果: 8
```

### construct：new 操作符拦截

```javascript
function Person(name) {
    this.name = name;
}

const ProxyPerson = new Proxy(Person, {
    construct: function(target, args, newTarget) {
        console.log('使用 new 创建对象');
        return new target(...args);
    }
});

const p = new ProxyPerson('小明'); // 触发 construct
console.log(p.name); // 打印结果: 小明
```

### getOwnPropertyDescriptor / defineProperty / preventExtensions / ownKeys

```javascript
const target = { name: '小明', age: 18 };

const proxy = new Proxy(target, {
    getOwnPropertyDescriptor: function(target, prop) {
        console.log('获取属性描述符：' + prop);
        return Object.getOwnPropertyDescriptor(target, prop);
    },
    
    defineProperty: function(target, prop, descriptor) {
        console.log('定义属性：' + prop);
        // 必须返回布尔值：Object.defineProperty 返回的是对象本身，
        // 虽然在布尔上下文里也算「真」，但规范要求这里明确返回 true/false
        return Reflect.defineProperty(target, prop, descriptor);
    },
    
    preventExtensions: function(target) {
        console.log('阻止扩展对象');
        // 同样必须返回布尔值
        return Reflect.preventExtensions(target);
    },
    
    ownKeys: function(target) {
        console.log('获取所有属性键');
        return Reflect.ownKeys(target);
    }
});

console.log(Object.keys(proxy)); // 触发 ownKeys
```

### 应用：响应式数据 / 数据验证 / 私有变量 / 观察者模式 / 链式调用

**数据验证**：

```javascript
function createValidator(schema) {
    return new Proxy({}, {
        set: function(target, property, value) {
            const validator = schema[property];
            if (validator && !validator(value)) {
                throw new Error('属性 ' + property + ' 的值无效');
            }
            target[property] = value;
            return true;
        }
    });
}

const user = createValidator({
    age: function(v) { return typeof v === 'number' && v >= 0; }
});

user.age = 18; // 成功
user.age = -5; // 报错：属性 age 的值无效
```

**私有变量**：

```javascript
function createPrivate(obj) {
    return new Proxy(obj, {
        get: function(target, prop) {
            if (prop.startsWith('_')) {
                throw new Error('不能访问私有属性 ' + prop);
            }
            return target[prop];
        },
        set: function(target, prop, value) {
            if (prop.startsWith('_')) {
                throw new Error('不能修改私有属性 ' + prop);
            }
            target[prop] = value;
            return true;
        }
    });
}

const user = createPrivate({ name: '小明', _secret: '123456' });
console.log(user.name); // 打印结果: 小明
console.log(user._secret); // 报错：不能访问私有属性 _secret
```

**更实用的两个应用**：

```javascript
// 1. 数组负索引：arr[-1] 直接取最后一个元素
function createArrayProxy(arr) {
    return new Proxy(arr, {
        get(target, prop, receiver) {
            if (typeof prop === 'string' && /^-\d+$/.test(prop)) {
                const index = Number(prop);
                return target[index < 0 ? target.length + index : index];
            }
            return Reflect.get(target, prop, receiver);
        },
    });
}

const list = createArrayProxy([1, 2, 3]);
console.log(list[-1]); // 打印结果: 3
console.log(list[0]);  // 打印结果: 1

// 2. 属性值缓存：把开销大的计算结果记住
function createCacheProxy(fn) {
    const cache = new Map();
    return new Proxy(fn, {
        apply(target, thisArg, args) {
            const key = JSON.stringify(args);
            if (!cache.has(key)) {
                cache.set(key, Reflect.apply(target, thisArg, args));
            }
            return cache.get(key);
        },
    });
}

const slowAdd = createCacheProxy((a, b) => {
    console.log('真的算了一次');
    return a + b;
});
slowAdd(1, 2); // 输出「真的算了一次」
slowAdd(1, 2); // 直接命中缓存，不再打印
```

### 不变量：代理不能「撒谎」

Proxy 看似无所不能，但规范给每个拦截器都加了**不变量（invariants）**，防止代理破坏 JavaScript 对象的基本保证。违反不变量会直接抛 `TypeError`，这是初学 Proxy 时最常遇到的报错来源：

| 场景 | 被禁止的行为 |
| --- | --- |
| 目标对象的属性是不可写、不可配置的 | `get` 不能返回不同的值 |
| 目标对象的属性是不可配置的 | `getOwnPropertyDescriptor` 不能报告它不存在或改成可配置 |
| 目标是不可扩展的 | `ownKeys` 不能返回目标上不存在的键 |
| 目标上存在不可配置的属性 | `ownKeys` 不能把它漏掉 |
| 目标对象不可扩展 | `defineProperty` 不能新增属性 |

```javascript
const target = {};
Object.defineProperty(target, 'id', {
    value: 1,
    writable: false,
    configurable: false,
});

const proxy = new Proxy(target, {
    get(t, prop, receiver) {
        if (prop === 'id') return 999;   // 想骗过调用方
        return Reflect.get(t, prop, receiver);
    },
});

// proxy.id;
// TypeError: 'get' on proxy: property 'id' is a read-only and
// non-configurable data property on the proxy target but the proxy
// did not return its actual value

// ✅ 正确做法：要么老老实实返回真实值，要么在拦截前先把属性设成可配置
```

### Proxy 的局限与代价

1. **拦不住类里的私有字段**。`#x` 只能在定义它的类内部访问，通过 Proxy 访问会抛错，这是语言层面的限制：

```javascript
class Counter {
    #count = 0;
    increment() { this.#count++; }
    get value() { return this.#count; }
}

const counter = new Proxy(new Counter(), {});
// ❌ 两个操作都会抛错，原因都是「this 变成了 proxy」
// counter.value;
// TypeError: Cannot read private member #count from an object
//   whose class did not declare it
// counter.increment();
// 同样的 TypeError
```

默认的 `get` 行为会以**代理对象**作为 `receiver` 去调用 getter 和方法，而 `#count` 只认「声明它的那个类创建的原始对象」。解决办法是在 `get` 里把方法绑回目标对象：

```javascript
const safeProxy = new Proxy(new Counter(), {
    get(target, prop, receiver) {
        const value = Reflect.get(target, prop, target); // 关键：receiver 传 target
        return typeof value === 'function' ? value.bind(target) : value;
    },
});

console.log(safeProxy.value); // 打印结果: 0
safeProxy.increment();
console.log(safeProxy.value); // 打印结果: 1
```

如果类里面大量使用私有字段，最好**显式提供一套面向代理的方法**，而不是靠自动绑定去绕过。

2. **只拦截「通过代理访问」的操作**。对象内部直接访问自己的属性（例如方法里写 `this.name`），只要 `this` 不是代理，就完全绕过拦截。

3. **有性能开销**，而且不小。每次属性访问都要走一遍拦截函数，比直接访问慢一个数量级。所以不要在热路径（大循环、逐帧渲染）里滥用，把它留给「需要统一行为的边界层」。

```javascript
// 判断一个对象是不是代理，没有官方 API，只能靠约定（例如打一个标记）
// 这也是为什么很多库会自己在对象上挂一个 Symbol 标记
```

### 可撤销代理：Proxy.revocable

有时你希望「临时授权访问，用完立刻失效」，`Proxy.revocable` 正好提供这个能力：

```javascript
const { proxy, revoke } = Proxy.revocable({ secret: '数据' }, {});

console.log(proxy.secret); // 打印结果: 数据

revoke(); // 撤销代理

// 撤销之后任何操作都会抛 TypeError
try {
    console.log(proxy.secret);
} catch (e) {
    console.log(e.name); // TypeError: Cannot perform 'get' on a proxy that has been revoked
}

// 典型场景：把对象交给第三方代码使用一小段时间，用完立即收回
```

下一节，我们来学习 Reflect！

## 32.2 Reflect

### 概念：Object 的替代者，提供操作对象的方法

Reflect 是 ES6 引入的另一个新特性，它提供了一组操作对象的方法，和 Object 类似，但更合理、更一致。

```javascript
// Reflect 的方法
Reflect.get(target, property, receiver);
Reflect.set(target, property, value, receiver);
Reflect.has(target, property);
Reflect.deleteProperty(target, property);
Reflect.ownKeys(target);
Reflect.getOwnPropertyDescriptor(target, property);
Reflect.defineProperty(target, property, descriptor);
Reflect.preventExtensions(target);
Reflect.apply(target, thisArg, args);
Reflect.construct(target, args, newTarget);
```

### Reflect 与 Object 的差异

Reflect 和 Object 上看起来有不少重名方法，但设计取向不同：**Object 走「失败就抛错」的路线，Reflect 走「返回布尔值、把判断交给调用方」的路线**，而且 Reflect 的方法都是函数式的，可以直接当作一等公民传递。

| 操作 | Object 风格 | Reflect 风格 | 关键差异 |
| --- | --- | --- | --- |
| 定义属性 | `Object.defineProperty(o, k, d)` | `Reflect.defineProperty(o, k, d)` | 前者失败抛错，后者返回 `false` |
| 获取原型 | `Object.getPrototypeOf(o)` | `Reflect.getPrototypeOf(o)` | 基本等价 |
| 设置原型 | `Object.setPrototypeOf(o, p)` | `Reflect.setPrototypeOf(o, p)` | 前者失败抛错，后者返回布尔值 |
| 列举键 | `Object.keys(o)` | `Reflect.ownKeys(o)` | 前者只有「自有可枚举字符串键」，后者包含 Symbol 与不可枚举键 |
| 删除属性 | `delete o.k` | `Reflect.deleteProperty(o, k)` | 后者返回值，前者在严格模式下会抛错 |
| 是否可扩展 | `Object.isExtensible(o)` | `Reflect.isExtensible(o)` | 基本等价 |
| 阻止扩展 | `Object.preventExtensions(o)` | `Reflect.preventExtensions(o)` | 前者返回对象，后者返回布尔值 |
| 属性是否存在 | `k in o` | `Reflect.has(o, k)` | 后者可当作函数传递 |
| 调用函数 | `fn.apply(thisArg, args)` | `Reflect.apply(fn, thisArg, args)` | 后者不需要函数本身带 `apply` |
| new | `new Fn(...args)` | `Reflect.construct(Fn, args, newTarget)` | 后者可动态指定 `newTarget` |

一句话总结：**在代理的拦截器内部，优先用 Reflect 对应方法**。它不会抛错打断流程、返回值语义统一，而且天然和 Proxy 的拦截器一一对应。

### receiver 到底在做什么

所有带 `receiver` 参数的 Reflect 方法（`get`、`set`、`getOwnPropertyDescriptor` 等）都遵循同一个规则：**如果取到的是一个访问器（getter），那么 getter 里的 `this` 就是 `receiver`**。这直接影响「在代理上是否继续触发拦截」：

```javascript
const target = {
    first: 'A',
    get full() {
        return this.first + '!';   // 这里的 this 取决于 receiver
    },
};

function demo(useReflect) {
    const log = [];
    const p = new Proxy(target, {
        get(t, prop, receiver) {
            log.push('trap:' + prop);
            // 关键差别：
            // ✅ Reflect.get(t, prop, receiver) —— getter 里的 this 是代理，this.first 会再次触发拦截
            // ❌ t[prop]                        —— getter 里的 this 是原始对象，this.first 绕过拦截
            return useReflect ? Reflect.get(t, prop, receiver) : t[prop];
        },
    });
    console.log(p.full, log);
}

demo(false); // A! [ 'trap:full' ]                     —— 没拦到对 first 的读取
demo(true);  // A! [ 'trap:full', 'trap:first' ]      —— 连内部读取都被拦到了
```

这就是「透明代理」必须写 `Reflect.get(target, property, receiver)` 而不是 `target[property]` 的真正原因。写成 `target[property]` 时，代理看起来能用，但在涉及 getter、继承、链式访问的场景里会悄悄漏掉拦截。

### Reflect.get / set / has / deleteProperty / ownKeys

```javascript
const target = { name: '小明', age: 18 };

// 获取属性
console.log(Reflect.get(target, 'name')); // 打印结果: 小明

// 设置属性
Reflect.set(target, 'age', 20);
console.log(target.age); // 打印结果: 20

// 检查属性
console.log(Reflect.has(target, 'name')); // 打印结果: true

// 删除属性
Reflect.deleteProperty(target, 'age');
console.log(target); // 打印结果: { name: '小明' }

// 获取所有属性键
console.log(Reflect.ownKeys(target)); // 打印结果: ['name']
```

### Reflect.apply / construct / defineProperty

```javascript
// apply：调用函数
function greet(greeting, name) {
    return greeting + ', ' + name;
}
console.log(Reflect.apply(greet, null, ['Hello', '小明'])); // 打印结果: Hello, 小明

// construct：new 操作符
function Person(name) {
    this.name = name;
}
const p = Reflect.construct(Person, ['小明']);
console.log(p.name); // 打印结果: 小明

// defineProperty：定义属性
Reflect.defineProperty(target, 'age', { value: 18, writable: true });
console.log(target.age); // 打印结果: 18
```

### Proxy + Reflect 实现透明代理

Proxy 和 Reflect 配合使用，可以实现"透明代理"——对代理对象的操作，都转发给目标对象。

```javascript
const target = { name: '小明', age: 18 };

const proxy = new Proxy(target, {
    get: function(target, property, receiver) {
        // 使用 Reflect.get，确保 this 绑定正确
        return Reflect.get(target, property, receiver);
    },
    
    set: function(target, property, value, receiver) {
        // 使用 Reflect.set，确保 this 绑定正确
        return Reflect.set(target, property, value, receiver);
    },
    
    has: function(target, property) {
        return Reflect.has(target, property);
    },
    
    deleteProperty: function(target, property) {
        return Reflect.deleteProperty(target, property);
    }
});

console.log(proxy.name); // 打印结果: 小明
proxy.age = 20;
console.log(proxy.age); // 打印结果: 20
console.log('name' in proxy); // 打印结果: true
```

---

## 本章小结

本章我们学习了 Proxy 和 Reflect：

1. **Proxy**：代理器，可拦截对象的各种操作（属性读写、`in`、`delete`、函数调用、`new`、键枚举等）；`set` 与 `deleteProperty` 等拦截器必须返回布尔值。
2. **不变量**：代理不能「撒谎」，不能对不可配置、不可写的属性返回假值，否则会抛 `TypeError`。
3. **Reflect**：与 Proxy 拦截器一一对应的一套函数式 API，失败时返回布尔值，而不是抛错。
4. **receiver**：带 receiver 的方法会把 getter 里的 `this` 设为 receiver；透明代理必须写 `Reflect.get(target, prop, receiver)`，写成 `target[prop]` 会漏掉内部访问的拦截。
5. **应用**：数据验证、私有字段保护、负索引数组、函数结果缓存、`Proxy.revocable` 可撤销授权。
6. **局限**：拦不住类私有字段（需绑定到目标对象）、只拦截「通过代理」的访问、有明显性能开销，不要用在热路径上。
7. **实际影响**：Vue 3 的响应式系统正是用 Proxy + Reflect 实现的——这也是它比 Vue 2 的 `Object.defineProperty` 方案能监听到新增属性、数组下标修改与 `delete` 操作的原因。

下一章，我们要学习 Symbol——JavaScript 的"独一无二"！
