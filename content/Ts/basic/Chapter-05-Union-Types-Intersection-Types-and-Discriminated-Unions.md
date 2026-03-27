+++
title = "第5章 联合类型、交叉类型与可辨识联合"
weight = 50
date = "2026-03-26T21:05:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 5 章 联合类型、交叉类型与可辨识联合

## 5.1 联合类型（Union Types）

**联合类型**是TypeScript中表示"可以是多种类型之一"的类型。它就像一把钥匙能开多把锁——一个变量可以是几种类型中的任意一种。

---

### 5.1.1 联合类型的声明：`string | number`

```typescript
// 声明联合类型
let value: string | number = "hello";
console.log(value); // hello

value = 42;
console.log(value); // 42

// value = true; // 错误！boolean不在允许的范围内
```

---

### 5.1.2 联合类型的值域概念

#### 5.1.2.1 联合类型的值域 = 各成员类型值域的并集；值可以是任意一个成员类型的值，但不能同时是两个

```typescript
// string | number的值域 = {所有字符串} ∪ {所有数字}
let mixed: string | number;

mixed = "hello";    // OK
mixed = 123;        // OK
mixed = true;       // 错误！

// 不能同时是两种类型
mixed = "hello" + 123; // 这个表达式的结果是"hello123"（字符串），不是同时有两个类型
```

#### 5.1.2.2 联合类型的宽度随成员数量增加而扩大，类型收窄（narrowing）可以逐步缩小为具体成员

```typescript
// 成员越多，类型越宽
type Narrow = "A";
type Medium = "A" | "B";
type Wide = "A" | "B" | "C" | "D";

// 类型收窄：从宽类型到窄类型
function process(value: string | number | boolean) {
    if (typeof value === "string") {
        // 在这里，value的类型被收窄为string
        console.log(value.toUpperCase());
    } else if (typeof value === "number") {
        // 在这里，value的类型被收窄为number
        console.log(value.toFixed(2));
    } else {
        // 在这里，value的类型是boolean
        console.log(value ? "真" : "假");
    }
}

process("hello");   // HELLO
process(3.14159);   // 3.14
process(true);      // 真
```

---

### 5.1.3 为什么联合类型用 `|`

#### 5.1.3.1 `|` 在数学上是「并集」符号；TypeScript 参考了数学集合论的语言

在数学中，`|` 代表集合的**并集**。TypeScript采用了这个符号：

```typescript
// 集合论中的A ∪ B
// TypeScript中对应 A | B
type A = string;
type B = number;
type Union = A | B; // string | number

// 多个并集
type Status = "pending" | "active" | "failed";
```

---

### 5.1.4 联合类型的方法访问规则

#### 5.1.4.1 联合类型的值只能访问所有成员共有的方法/属性（交集）

```typescript
// string | number 只能访问两者共有的成员
let value: string | number = Math.random() > 0.5 ? "hello" : 42;

console.log(value.toString()); // OK —— toString是string和number共有的
// console.log(value.toUpperCase()); // 错误！toUpperCase只有string有
// console.log(value.toFixed(2)); // 错误！toFixed只有number有
```

这是一个重要的规则：**联合类型的值只能访问"所有成员共有的"方法**。这确保了代码的安全性——无论实际值是什么类型，访问的方法一定存在。

#### 5.1.4.2 示例：`string | number` 只能访问 `.toString()`（两者共有），不能访问 `.split()`（string 独有）

```typescript
function process(value: string | number) {
    // 两者共有的方法
    console.log(value.toString()); // OK
    console.log(value.valueOf());  // OK
    
    // 只有string有
    // value.split(); // 错误！
    // value.toUpperCase(); // 错误！
    
    // 只有number有
    // value.toFixed(2); // 错误！
    
    // 类型收窄后就可以访问了
    if (typeof value === "string") {
        console.log(value.split("")); // OK！在string分支里
        console.log(value.toUpperCase()); // OK！
    } else {
        console.log(value.toFixed(2)); // OK！在number分支里
    }
}
```

---

### 5.1.5 字面量联合类型

#### 5.1.5.1 用字面量（字符串、数字、布尔）作为联合成员：`type Direction = 'Up' | 'Down' | 'Left' | 'Right'`

```typescript
// 字符串字面量联合类型
type Direction = "Up" | "Down" | "Left" | "Right";

function move(dir: Direction) {
    console.log("移动方向：" + dir);
}

move("Up");    // OK
move("Down");  // OK
move("Left");  // OK
move("Right"); // OK
move("Diagonal"); // 错误！"Diagonal"不在允许的范围内
```

#### 5.1.5.2 应用场景：模拟枚举（当枚举过于重型时）、状态机、有限集合

```typescript
// 状态机
type OrderStatus = 
    | "pending"    // 待处理
    | "paid"       // 已支付
    | "shipped"    // 已发货
    | "delivered"  // 已送达
    | "cancelled"; // 已取消

function getStatusMessage(status: OrderStatus): string {
    switch (status) {
        case "pending":   return "订单待处理";
        case "paid":     return "订单已支付";
        case "shipped":  return "商品已发货";
        case "delivered": return "商品已送达";
        case "cancelled": return "订单已取消";
    }
}

console.log(getStatusMessage("pending")); // 订单待处理
```

#### 5.1.5.3 类型收窄后，TS 将联合成员作为独立原子类型处理，可精确匹配 switch case

```typescript
type Shape = 
    | { kind: "circle"; radius: number }
    | { kind: "rectangle"; width: number; height: number }
    | { kind: "triangle"; base: number; height: number };

function getArea(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "rectangle":
            return shape.width * shape.height;
        case "triangle":
            return (shape.base * shape.height) / 2;
    }
}

const circle = { kind: "circle" as const, radius: 5 };
const rectangle = { kind: "rectangle" as const, width: 4, height: 6 };

console.log(getArea(circle));    // 78.54
console.log(getArea(rectangle)); // 24
```



## 5.2 交叉类型（Intersection Types）

如果说联合类型是"或"，那交叉类型就是"且"——**值必须同时满足所有类型**。

---

### 5.2.1 交叉类型的声明：`A & B`

```typescript
// 交叉类型：必须同时满足A和B
type A = { name: string };
type B = { age: number };
type AB = A & B; // { name: string; age: number }

const obj: AB = {
    name: "孙悟空",
    age: 500
};

console.log(obj.name); // 孙悟空
console.log(obj.age); // 500
```

---

### 5.2.2 交叉类型的语义

#### 5.2.2.1 逻辑「且」：值必须同时属于 A 和 B

```typescript
interface CanWalk { walk(): void; }
interface CanSwim { swim(): void; }

// 交叉类型：同时具备两种能力
type Amphibian = CanWalk & CanSwim;

const frog: Amphibian = {
    walk() {
        console.log("跳着走");
    },
    swim() {
        console.log("游泳");
    }
};

frog.walk(); // 跳着走
frog.swim(); // 游泳
```

---

### 5.2.3 联合类型与交叉类型的组合（分配律）

#### 5.2.3.1 并集对交集的分配律：`(A | B) & C` → `(A & C) | (B & C)`（单向成立）

这是数学中的分配律，TypeScript也遵循：

```typescript
// (string | number) & boolean
// 分配律：string & boolean | number & boolean
// 结果是 (string & boolean) | (number & boolean)
type Result = (string | number) & boolean;

// 展开后：
// = (string & boolean) | (number & boolean)
// = never | never (因为字符串和数字都不可能是boolean)
// = never

// 实际验证
let value: Result = "hello" as any; // 实际上是never

// 但如果是函数类型，行为会不同
type F1 = ((x: string) => void) | ((x: number) => void);
type F2 = ((x: string) => void) & ((x: number) => void);

// F1：可以是接受string的函数，或者接受number的函数
// F2：必须是同时接受string和number的函数（矛盾，所以是never）
```

#### 5.2.3.2 示例：`(string | number) & object` 的实际含义

`(string | number) & object` 根据分配律展开为：

```typescript
// 分配律展开
type Result = (string | number) & object;
// 第一步：应用分配律
// = (string & object) | (number & object)
// 第二步：计算每个交叉
// string & object = never —— 字符串是原始类型，不是对象，永远不可能同时是"字符串"又是"对象"
// number & object = never —— 数字也是原始类型，同样不可能
// 第三步：never | never = never
// 最终结果 = never
type Final = (string | number) & object; // never
```

**为什么 `string & object = never`？**

在TypeScript的结构化类型系统中，`string`是原始类型（值类型），而`object`代表引用类型。两者在结构上永远不可能兼容——一个值不可能同时是"字符串"又是"对象"。

```typescript
// 验证
type T1 = string & object;  // never —— string永远不是object
type T2 = number & object;  // never —— number永远不是object

// 所以 (string | number) & object = never | never = never
type Final = (string | number) & object; // never
```

> 💡 **一个更实际的例子**：假设有一个API返回类型是`User | null & Serializable`，这个交集操作要求值必须同时是User类型且实现了Serializable接口——这时交叉类型就派上用场了。



#### 5.2.3.3 反向分配（交集对并集）不一定成立：`(A & B) | C` ≠ `A & (B | C)`

```typescript
// 验证：分配律不是双向的
type LHS = (string & number) | boolean; // never | boolean = boolean
type RHS = string & (number | boolean);  // string & (number | boolean) = (string & number) | (string & boolean) = never | never = never

// LHS = boolean
// RHS = never
// 两者不相等！
```

---

### 5.2.4 为什么需要交叉类型

#### 5.2.4.1 JavaScript 对象可以动态混合多个来源的属性；Mixins 模式需要「同时满足多个类型」的表达能力

JavaScript的对象可以随时添加任意属性，TypeScript的交叉类型正好可以描述这种灵活性：

```typescript
// Mixins模式：用交叉类型混合多个功能
function withLog<T extends object>(obj: T): T & { log(): void } {
    return {
        ...obj,
        log() {
            console.log("log:", JSON.stringify(obj));
        }
    } as T & { log(): void };
}

function withTimestamp<T extends object>(obj: T): T & { timestamp: Date } {
    return {
        ...obj,
        timestamp: new Date()
    } as T & { timestamp: Date };
}

const base = { name: "孙悟空", age: 500 };
const enhanced = withLog(withTimestamp(base));

console.log(enhanced.name);     // 孙悟空
console.log(enhanced.timestamp); // 当前时间
enhanced.log();                  // log: {"name":"孙悟空","age":500}
```

---

### 5.2.5 交叉类型的实际用途

#### 5.2.5.1 Mixins 混入模式：同时混入多个能力到同一个对象

```typescript
// Mixin函数
function Timestamped<T extends object>(Base: T) {
    return class extends Base {
        timestamp = new Date();
    };
}

function Serializable<T extends object>(Base: T) {
    return class extends Base {
        serialize() {
            return JSON.stringify(this);
        }
    };
}

// 组合多个Mixin
class User {
    name: string;
}

const TimestampedUser = Timestamped(Serializable(User));
const user = new TimestampedUser();
user.name = "Tom";
console.log(user.timestamp); // 当前时间
console.log(user.serialize()); // {"name":"Tom","timestamp":"..."}
```

#### 5.2.5.2 配置合并：多个配置源交叉后得到完整配置

```typescript
// 默认配置
type DefaultConfig = {
    timeout: number;
    retries: number;
    debug: boolean;
};

// 开发环境配置
type DevConfig = {
    debug: true;
    logLevel: "debug" | "info";
};

// 生产环境配置
type ProdConfig = {
    debug: false;
    logLevel: "warn" | "error";
};

// 开发配置 = 默认配置 + 开发特定配置
type DevFullConfig = DefaultConfig & DevConfig;
const devConfig: DevFullConfig = {
    timeout: 5000,
    retries: 3,
    debug: true,
    logLevel: "debug"
};

// 生产配置 = 默认配置 + 生产特定配置
type ProdFullConfig = DefaultConfig & ProdConfig;
const prodConfig: ProdFullConfig = {
    timeout: 10000,
    retries: 1,
    debug: false,
    logLevel: "error"
};
```

#### 5.2.5.3 类型扩展：为已有类型动态添加额外属性（如 `User & { role: 'admin' }`）

```typescript
interface User {
    name: string;
    email: string;
}

// 扩展User类型
type Admin = User & {
    role: "admin";
    permissions: string[];
};

const admin: Admin = {
    name: "管理员",
    email: "admin@example.com",
    role: "admin",
    permissions: ["read", "write", "delete"]
};

console.log(admin.role); // admin
```



## 5.3 可辨识联合（Tagged Union / Discriminated Union）

**可辨识联合**是TypeScript中处理多态类型的一种强大模式。它结合了联合类型和类型收窄，让你能够安全地处理多种可能的状态。

---

### 5.3.1 可辨识联合的概念与实现

#### 5.3.1.1 用一个公共字面量属性（判别属性）区分联合成员

可辨识联合的关键是**判别属性**（Discriminant Property）——一个所有联合成员都有的、类型为字面量类型的公共属性：

```typescript
// 定义三种不同的事件类型
interface SuccessEvent {
    type: "success";      // 判别属性：字面量类型
    data: unknown;
    timestamp: Date;
}

interface ErrorEvent {
    type: "error";         // 判别属性
    error: Error;
    timestamp: Date;
}

interface LoadingEvent {
    type: "loading";       // 判别属性
    message: string;
}

// 联合类型
type AppEvent = SuccessEvent | ErrorEvent | LoadingEvent;

// 使用：TypeScript会根据type自动收窄
function handleEvent(event: AppEvent) {
    switch (event.type) {
        case "success":
            console.log("成功！数据：", event.data);    // event是SuccessEvent
            console.log("时间：", event.timestamp);
            break;
        case "error":
            console.error("错误：", event.error.message); // event是ErrorEvent
            console.log("时间：", event.timestamp);
            break;
        case "loading":
            console.log("加载中：", event.message);     // event是LoadingEvent
            break;
    }
}

// 测试
handleEvent({
    type: "success",
    data: { id: 1 },
    timestamp: new Date()
});
// 输出：成功！数据：{ id: 1 } 时间：2026-03-26T...

handleEvent({
    type: "error",
    error: new Error("网络错误"),
    timestamp: new Date()
});
// 输出：错误：网络错误 时间：2026-03-26T...
```

#### 5.3.1.2 `type Action = { type: 'increment'; delta: number } | { type: 'decrement'; delta: number }`

这个模式在Redux等状态管理库中非常常见：

```typescript
// Redux风格的Action
type CounterAction =
    | { type: "increment"; delta: number }
    | { type: "decrement"; delta: number }
    | { type: "reset" };

function reducer(state: number, action: CounterAction): number {
    switch (action.type) {
        case "increment":
            return state + action.delta; // action.delta存在
        case "decrement":
            return state - action.delta; // action.delta存在
        case "reset":
            return 0;
    }
}

console.log(reducer(10, { type: "increment", delta: 5 })); // 15
console.log(reducer(10, { type: "decrement", delta: 3 })); // 7
console.log(reducer(10, { type: "reset" }));               // 0
```

---

### 5.3.2 可辨识联合的穷举检查

#### 5.3.2.1 default 分支返回 never；若漏掉 case，编译时报错

这是可辨识联合最强大的特性——**穷举检查**：

```typescript
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rectangle"; width: number; height: number }
    | { kind: "triangle"; base: number; height: number };

function getArea(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "rectangle":
            return shape.width * shape.height;
        case "triangle":
            return (shape.base * shape.height) / 2;
        default:
            // 穷举检查：如果漏掉了某个case，TS会报错
            const _exhaustive: never = shape;
            throw new Error("不可能的形状：" + JSON.stringify(_exhaustive));
    }
}
```

如果以后添加了新的Shape变体但忘记处理，TypeScript会在default分支报错：

```typescript
// 添加新形状
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rectangle"; width: number; height: number }
    | { kind: "triangle"; base: number; height: number }
    | { kind: "ellipse"; a: number; b: number }; // 新增

// TS会在getArea的default分支报错：
// Type '{ kind: "ellipse"; a: number; b: number; }' is not assignable to type 'never'.
```

---

### 5.3.3 为什么叫「可辨识」

#### 5.3.3.1 判别属性让 TypeScript 能区分联合成员；类似代数数据类型（ADT）的概念

"可辨识"这个名字来自于判别属性能够"辨识"每个联合成员：

```mermaid
graph TD
    A[AppEvent 联合类型] --> B[SuccessEvent<br/>type: "success"]
    A --> C[ErrorEvent<br/>type: "error"]
    A --> D[LoadingEvent<br/>type: "loading"]
    
    B --> E[通过 type === 'success'<br/>识别为SuccessEvent]
    C --> F[通过 type === 'error'<br/>识别为ErrorEvent]
    D --> G[通过 type === 'loading'<br/>识别为LoadingEvent]
```

这个概念来自**代数数据类型（Algebraic Data Types，ADT）**，在Haskell、F#、Rust等语言中很常见。TypeScript的可辨识联合是ADT思想在JavaScript生态中的实现。

---

### 5.3.4 应用场景：Redux/状态管理、网络请求结果（SuccessResponse | ErrorResponse）

```typescript
// 网络请求结果
type ApiResult<T> =
    | { status: "success"; data: T; code: 200 }
    | { status: "client_error"; error: string; code: 400 | 401 | 403 }
    | { status: "server_error"; error: string; code: 500 }
    | { status: "network_error"; error: string };

async function fetchUser(id: number): Promise<ApiResult<{ name: string; age: number }>> {
    try {
        const response = await fetch(`/api/user/${id}`);
        if (!response.ok) {
            return { status: "client_error", error: "请求失败", code: response.status as 400 | 401 | 403 };
        }
        const data = await response.json();
        return { status: "success", data, code: 200 };
    } catch (err) {
        return { status: "network_error", error: "网络连接失败" };
    }
}

// 使用
async function main() {
    const result = await fetchUser(1);
    
    switch (result.status) {
        case "success":
            console.log("用户信息：", result.data);
            break;
        case "client_error":
            console.error("客户端错误：", result.error, "状态码：", result.code);
            break;
        case "server_error":
            console.error("服务器错误：", result.error, "状态码：", result.code);
            break;
        case "network_error":
            console.error("网络错误：", result.error);
            break;
    }
}

main();
```

```typescript
// 状态机
type TrafficLight =
    | { state: "red"; duration: number }
    | { state: "yellow"; duration: number }
    | { state: "green"; duration: number };

function getNextLight(current: TrafficLight): TrafficLight {
    switch (current.state) {
        case "red":
            return { state: "green", duration: 3000 };
        case "green":
            return { state: "yellow", duration: 1000 };
        case "yellow":
            return { state: "red", duration: 5000 };
    }
}

let light: TrafficLight = { state: "red", duration: 5000 };
for (let i = 0; i < 3; i++) {
    console.log(`当前灯：${light.state}，持续${light.duration}ms`);
    light = getNextLight(light);
}
```

---

> 📝 **本节小结**：可辨识联合（Tagged Union）通过一个公共的字面量属性（判别属性）来区分联合成员。TypeScript会根据判别属性的值自动收窄类型，从而安全地访问每个成员特有的属性。可辨识联合配合switch语句和穷举检查，可以确保所有可能的情况都被处理。添加新的联合成员时，TypeScript会在编译时报错，提示需要处理新的情况。

---

## 本章小结

本章学习了TypeScript中三种强大的类型组合工具：联合类型、交叉类型和可辨识联合。

**联合类型**用`|`表示"或"的关系，值可以是任意一个成员类型，但同时只能是一个。联合类型的值只能访问所有成员共有的方法/属性。字面量联合类型适合表示有限集合、状态机等场景。类型收窄可以逐步缩小联合类型的范围。

**交叉类型**用`&`表示"且"的关系，值必须同时满足所有类型。交叉类型常用于Mixins模式（混入多个功能）、配置合并（多个配置源交叉）、类型扩展。分配律在联合类型和交叉类型之间单向成立。

**可辨识联合**（Tagged Union）是处理多态类型的强大模式。它通过一个公共的字面量属性（判别属性）来区分联合成员。TypeScript会根据判别属性的值自动收窄类型。可辨识联合配合穷举检查和default返回never，可以确保所有情况都被处理，添加新成员时编译器会报错。

这三种类型组合工具是TypeScript类型系统的核心，掌握它们可以写出更精确、更安全的类型代码。

---

恭喜你完成了TypeScript核心类型的全部内容！从原始类型到特殊类型，从接口到类型别名，从联合类型到可辨识联合——你已经具备了TypeScript类型系统的坚实基础。

下一阶段的内容将是更高级的TypeScript特性，包括泛型、类型操作符、条件类型、映射类型等。继续保持这个学习节奏，你正在成为一个TypeScript高手！





