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

proxy.age = 18; // 报错：属性值必须是字符串
console.log(proxy.name); // 报错：属性 age 不存在
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
        return Object.defineProperty(target, prop, descriptor);
    },
    
    preventExtensions: function(target) {
        console.log('阻止扩展对象');
        return Object.preventExtensions(target);
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

1. **Proxy**：代理器，可以拦截对对象的所有操作（属性读写、函数调用、new 操作等）。
2. **Reflect**：Object 的替代者，提供了更合理、更一致的操作对象的方法。
3. **应用**：数据验证、私有变量、响应式数据、链式调用等。

下一章，我们要学习 Symbol——JavaScript 的"独一无二"！
