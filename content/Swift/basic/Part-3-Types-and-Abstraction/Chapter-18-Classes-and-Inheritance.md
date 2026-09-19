+++
title = "第18章 类与继承：共享身份与运行时多态"
weight = 180
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十八章：类与继承：共享身份与运行时多态

> 结构体说：“我给你一份副本。”类说：“我们指向同一个东西。”这句话决定了类的强大和麻烦。它适合表达有身份、需要共享和继承的对象；同样也意味着你必须认真面对引用、生命周期和循环引用。

## 18.1 定义类与引用语义

类的外形和结构体几乎一样，区别藏在赋值那一刻：结构体给你一份副本，类给你一个指向同一个实例的引用。

```swift
class Counter {
    var value = 0
}

let a = Counter()
let b = a
b.value = 10
print(a.value)
// prints: 10
```

`a` 和 `b` 是两个引用，但指向同一个实例。修改 `b` 看到的自然也是 `a` 看到的值。想知道两个引用是否指向同一实例，用 `===`：

```swift
let c = Counter()
print(a === b, a === c)
// prints: true false
```

`===` 比较身份，`==` 比较内容。默认情况下，类没有自动获得内容相等语义。

（上面故意先不写 `final`——它是什么意思，18.4 节再说。）

## 18.2 继承与方法重写

继承的写法是 `class 子类: 父类`；想改写父类的实现，必须写 `override`。

```swift
class Animal {
    var name: String

    init(name: String) {
        self.name = name
    }

    func speak() -> String {
        "..."
    }
}

class Dog: Animal {
    override func speak() -> String {
        "汪汪"
    }
}

class Cat: Animal {
    override func speak() -> String {
        "喵"
    }
}
```

子类可以重写父类的方法、属性和下标，必须写 `override`。忘了写会被编译器拒绝；明明没重写却写 `override`，也会被拒绝。这是 Swift 防止你误改接口的一道保险。

```swift
let animals: [Animal] = [Dog(name: "Nova"), Cat(name: "Luna")]
for animal in animals {
    print(animal.name, animal.speak())
}
// prints: Nova 汪汪
// prints: Luna 喵
```

同一个 `speak()` 调用在不同实例上执行不同实现，这就是运行时多态。

## 18.3 `super`：调用父类实现

有时候你不想整个替换父类的实现，只想在它的结果之上再加点料。那就用 `super` 明确地叫一声父类：

```swift
class LoudDog: Dog {
    override func speak() -> String {
        super.speak() + "!!"
    }
}

print(LoudDog(name: "Max").speak())
// prints: 汪汪!!
```

子类初始化器也可以在满足规则时调用 `super.init(...)`。初始化顺序有严格的两阶段规则，第 20 章会完整讲。

## 18.4 `final` 与继承边界

`final` 表示“到此为止，不许再继承或重写”：

```swift
final class Config {
    var name = "app"
}
```

如果整个类没有设计成可继承，就标 `final`。它表达意图，也能让编译器跳过动态派发的开销。库作者尤其应该在默认情况下把类设为 `final`，需要开放继承时再开放。

`final` 方法则表示该方法不能被子类重写。

## 18.5 类的初始化与反初始化入口

类可以写自己的初始化器：

```swift
class User {
    var name: String
    var age: Int

    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }

    deinit {
        print("\(name) 离开了")
    }
}

var user: User? = User(name: "Mia", age: 28)
print(user?.name as Any)
// prints: Optional("Mia")
user = nil
// prints: Mia 离开了
```

类没有自动成员逐一初始化器。只要属性没有默认值，就必须在初始化器里全部赋值。`deinit` 在实例被释放时调用，只有类才有反初始化器。

## 18.6 向上转换与向下转换

子类实例可以安全地当成父类：

```swift
let animal: Animal = Dog(name: "Nova")
```

反过来需要显式转换，因为父类引用不一定真的指向子类：

```swift
if let dog = animal as? Dog {
    print(dog.speak())
    // prints: 汪汪
}

print(animal as? Cat as Any)
// prints: nil
```

优先使用 `as?`，不要用 `as!` 把不确定性糊弄过去。

## 18.7 类的身份、共享与生命周期

类实例有身份。它是什么对象、是否已经被释放、有多少引用指向它，都属于运行时状态。共享带来便利，也带来几个必须面对的问题：

- 别名：多个名字指向同一个对象，修改一处影响全部。
- 生命周期：引用可能比预期活得更久。
- 循环引用：两个对象互相强引用，谁都释放不了。
- 并发共享：多个任务同时修改同一对象，可能产生数据竞争。

前三点会在第 27、28 章拆解，第四点在并发篇章处理。类不是危险的，危险的是以为“它和结构体差不多”。

## 18.8 什么时候用类

倾向于使用类，当：

- 对象有明确身份，例如用户会话、网络连接、数据库事务。
- 多个持有者确实应该共享同一个实例。
- 需要继承体系或运行时多态。
- 需要 `deinit` 管理生命周期。
- 需要与 Objective-C 运行时或某些框架交互。

如果只是“一袋数据加上几个操作”，先用结构体。默认从值类型开始，需要共享身份时再升级到类，通常会更稳。

## 18.9 本章小结

| 主题 | 关键结论 |
| --- | --- |
| 引用语义 | 多个引用指向同一实例，修改会被所有引用看到 |
| `===` | 比较两个引用是否指向同一实例 |
| 继承 | 子类使用 `override` 重写父类成员 |
| `super` | 调用父类的实现或初始化器 |
| `final` | 禁止继承或重写，表达设计边界 |
| 初始化 | 类有 `init`/`deinit`，属性必须在初始化完成时合法 |
| 转换 | 向上安全，向下用 `as?` |

## 18.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 把类的赋值当成复制 | 复制的是引用，实例共享 |
| 忘了 `override` | 重写父类成员必须明确写出 |
| 到处开放继承 | 默认优先 `final`，需要时再开放 |
| 用 `as!` 转父类引用 | 不确定时使用 `as?` 并处理失败 |
| 忽略共享可变状态 | 多引用意味着任意一处都可能修改对象 |
| 以为类一定比结构体好 | 先根据身份和共享需求选择模型 |

## 18.11 下章预告

下一章把属性、方法和下标集中讲透：计算属性、属性观察器、`lazy`、类型属性、下标和属性包装器。它们决定一个类型对使用者呈现什么接口，也决定内部状态在什么时候被计算和观察。
