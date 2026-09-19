+++
title = "第20章 初始化与反初始化：让对象安全地诞生和离开"
weight = 200
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十章：初始化与反初始化：让对象安全地诞生和离开

> 创建对象不是“把内存填满”这么粗暴。Swift 要求实例在初始化结束时每个存储属性都合法，父类在子类准备好之前不能被随便用，失败时可以明确返回 `nil`。理解这些规则，才能写出不会在诞生半途炸掉的对象。

## 20.1 初始化器与默认值

初始化器的任务只有一个：把新对象带到“所有属性都合法”的状态。结构体会自动获得一个成员逐一初始化器，属性有默认值时它还会顺手变短。

```swift
struct Account {
    var owner: String
    var balance: Int = 0

    init(owner: String) {
        self.owner = owner
    }
}

let account = Account(owner: "Lin")
print(account.owner, account.balance)
// prints: Lin 0
```

属性有默认值时，可以在初始化器里省略赋值；没有默认值的存储属性必须在初始化结束前赋值。结构体如果没有自定义初始化器，会自动获得成员逐一初始化器：

```swift
struct Size {
    var width: Int
    var height: Int
}

let size = Size(width: 10, height: 5)
print(size.width, size.height)
// prints: 10 5
```

一旦在类型主体里写了自定义初始化器，自动生成的成员逐一初始化器就会被替代。想同时保留两者，可以把额外初始化器放进扩展。

## 20.2 结构体的初始化器委托

结构体可以有多个初始化器，并通过 `self.init` 委托给另一个初始化器：

```swift
struct Point {
    var x: Int
    var y: Int

    init(x: Int, y: Int) {
        self.x = x
        self.y = y
    }

    init() {
        self.init(x: 0, y: 0)
    }
}

print(Point().x, Point(x: 3, y: 4).y)
// prints: 0 4
```

一旦在初始化器里调用 `self.init`，就不能同时在前面给属性赋值；委托发生前，实例还没有准备好。

## 20.3 类的指定初始化器与便利初始化器

类初始化器分两类：

- 指定初始化器负责初始化本类所有存储属性，并调用父类指定初始化器。
- 便利初始化器用 `convenience init` 标记，必须最终委托到本类的某个初始化器。

```swift
class User {
    var name: String
    var age: Int

    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }

    convenience init(name: String) {
        self.init(name: name, age: 0)
    }
}

let user = User(name: "Nova")
print(user.name, user.age)
// prints: Nova 0
```

类没有自动成员逐一初始化器；属性必须在所有指定初始化器里赋值。便利初始化器不能直接初始化属性，它必须把工作交给本类的其他初始化器。

## 20.4 继承中的初始化规则

子类指定初始化器必须先初始化自己的属性，再调用 `super.init`：

```swift
class Animal {
    var name: String
    init(name: String) { self.name = name }
}

class Dog: Animal {
    var breed: String

    init(name: String, breed: String) {
        self.breed = breed          // 先保证自己的属性合法
        super.init(name: name)      // 再初始化父类部分
    }
}

let dog = Dog(name: "Nova", breed: "Corgi")
print(dog.name, dog.breed)
// prints: Nova Corgi
```

如果子类没有定义任何指定初始化器，它会继承父类的全部指定初始化器。如果子类实现了父类全部指定初始化器，它也会继承父类的便利初始化器。规则听起来绕，其实是在保证对象从底层到表层都完整地建立起来。

## 20.5 两阶段初始化

Swift 的类初始化严格分为两个阶段：

1. 每个类把自己引入的存储属性赋值，并向上调用 `super.init`。
2. 所有属性都稳定后，才能访问 `self`、调用实例方法、读取属性，或者使用 `self` 作为参数。

这意味着初始化器里不能在调用 `super.init` 前使用 `self` 的方法：

```swift
class Puppy: Animal {
    init(name: String, tag: Int) {
        bark()                 // 还没 super.init，就动用了 self
        super.init(name: name)
    }

    func bark() {}
}
```

```text
error: 'self' used in method call 'bark' before 'super.init' call
```

（消息里的 `'bark'` 就是被调用的方法名。）

这条规则看起来严苛，但它避免了“父类方法访问到尚未初始化的子类状态”。对象必须先完整，再开始工作。

## 20.6 可失败初始化器

`init?` 可以在输入不合法时返回 `nil`：

```swift
struct RangeValue {
    let lower: Int
    let upper: Int

    init?(lower: Int, upper: Int) {
        guard lower <= upper else { return nil }
        self.lower = lower
        self.upper = upper
    }
}

print(RangeValue(lower: 3, upper: 1) as Any)
// prints: nil
print(RangeValue(lower: 1, upper: 3)?.upper as Any)
// prints: Optional(3)
print(RangeValue(lower: 1, upper: 3) != nil)
// prints: true
```

第二行故意只取 `.upper`：如果直接 `print(... as Any)` 打印整个可选值，输出里会带上模块名前缀（形如 `Optional(模块名.RangeValue(lower: 1, upper: 3))`），在不同模块里长得不一样，不适合当固定结果展示。

`init!` 是隐式解包版本，失败时会崩溃。它适合历史接口兼容，现代代码一般不用。

## 20.7 `required` 初始化器

如果父类要求所有子类都必须实现某个初始化器，就用 `required`：

```swift
class Node {
    var name: String

    required init(name: String) {
        self.name = name
    }
}

class FileNode: Node {
    required init(name: String) {
        super.init(name: name)
    }
}
```

子类实现 `required init` 时也必须写 `required`，不能写 `override`。

## 20.8 反初始化：资源的最后一道门

`deinit` 只在类实例即将释放时自动调用，不能手动调用：

```swift
final class Connection {
    let name: String
    init(name: String) {
        self.name = name
        print("打开 \(name)")
    }
    deinit {
        print("关闭 \(name)")
    }
}

do {
    let connection = Connection(name: "db")
    print(connection.name)
}
// prints: 打开 db
// prints: db
// prints: 关闭 db
```

`deinit` 适合释放非内存资源、取消注册、写入最后的审计信息。不要在里面启动复杂异步工作，也不要依赖它一定在某个线程立刻执行；释放时机由引用计数决定。

## 20.9 `isolated deinit`

Swift 6.2 引入了隔离的反初始化器，让 `deinit` 可以安全访问 actor 隔离状态：

（`actor` 是"自带隔离状态的类型"，第 31 章的主角。这里先把它理解成一个"同一时刻只允许一个任务进来改它"的并发安全盒子。）

```swift
actor Cache {
    var values: [String: Int] = [:]

    func store(_ key: String, _ value: Int) {
        values[key] = value
    }

    isolated deinit {                 // 在 deinit 里直接碰 actor 的隔离状态
        values.removeAll()
        print("缓存清理完成，剩 \(values.count) 项")
    }
}

@MainActor
func runCache() async {
    do {
        let cache = Cache()
        await cache.store("a", 1)
    }                                 // 作用域结束，cache 的最后一个引用消失
    print("作用域结束")
}

@main
struct App {
    static func main() async {
        await runCache()
        try? await Task.sleep(for: .milliseconds(50))   // 给运行时一点时间完成释放
        print("主函数结束")
    }
}
// prints: 缓存清理完成，剩 0 项
// prints: 作用域结束
// prints: 主函数结束
```

两条注意：`isolated deinit` 由运行时调度，别依赖它和后续语句的先后顺序（上面的顺序只是这一次运行的样子）；它还需要较新的系统版本，部署目标太旧时会直接报 `isolated deinit is only available in macOS 15.4.0 or newer`。

`isolated deinit` 是并发进阶特性。普通类型不需要它；只有 `deinit` 必须接触隔离状态时，它才值得出场。

## 20.10 本章小结

| 主题 | 关键结论 |
| --- | --- |
| 存储属性 | 初始化结束时必须都有合法值 |
| 结构体初始化器 | 可用 `self.init` 委托 |
| 指定初始化器 | 负责本类属性并调用父类指定初始化器 |
| 便利初始化器 | 必须委托到本类初始化器 |
| 继承规则 | 子类可能继承父类初始化器，也可能不继承 |
| 两阶段初始化 | 先完成所有属性，再访问 `self` 的能力 |
| 可失败初始化器 | `init?` 返回可选，`init!` 失败即崩溃 |
| `deinit` | 类释放时自动调用，不能手动调用 |

## 20.11 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 在 `super.init` 前调用 `self` 的方法 | 两阶段初始化禁止 |
| 在便利初始化器里直接给属性赋值 | 便利初始化器必须委托 |
| 以为类会自动生成成员逐一初始化器 | 类不会 |
| 自定义初始化器后还期待结构体的自动初始化器 | 通常需要把额外初始化器放进扩展 |
| 在 `deinit` 中做复杂异步任务 | 对象即将消失，不适合依赖它完成异步工作 |
| 认为 `deinit` 一定会立刻执行 | 只要还有强引用，它就不会离开 |

## 20.12 下章预告

已经定义好的类型还能继续长本事吗？可以。下一章讲扩展和嵌套类型：给已有类型添加方法、计算属性、初始化器与协议实现，同时保持原类型的身份不变。
