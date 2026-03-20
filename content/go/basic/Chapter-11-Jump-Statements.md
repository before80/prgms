+++
title = "第11章 跳转语句"
weight = 110
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第11章 跳转语句



## 11.1 goto 语句

### 11.1.1 语法规则

**goto 是什么？**

`goto` 是编程语言中最古老、最简单、同时也是最"人人喊打"的一个跳转语句。它的原理粗暴得像个野蛮人——直接告诉电脑："别废话，跳到那个标签那里去执行！"

在 Go 语言里，`goto` 的语法是这样的：

```go
goto 标签名

// ... 中间省略一万行代码 ...

标签名:
fmt.Println("我被跳过来了")
```

看到了吗？你在代码的某个地方写一个"标签名:"（注意那个冒号），然后在别的地方写 `goto 标签名`，程序就会像被传送门传送一样，直接跳到标签那里执行，完全无视中间的代码。

这就像你看电视剧，看到第 10 集不想看了，直接快进到第 50 集——中间的第 11-49 集全部被你跳过了。`goto` 就是那个遥控器上的"快进键"。

**goto 的基本语法**

```go
package main

import "fmt"

func main() {

    fmt.Println("1. 这是第一行") // 1. 这是第一行
    fmt.Println("2. 这是第二行") // 2. 这是第二行

    goto skip

    fmt.Println("3. 这一行会被跳过")
    fmt.Println("4. 这一行也会被跳过")
    fmt.Println("5. 这一行还是会被跳过")

skip:
    fmt.Println("6. 我是标签 skip，程序跳到这里执行") // 6. 我是标签 skip，程序跳到这里执行
    fmt.Println("7. 程序继续正常执行") // 7. 程序继续正常执行
}
```

> `goto` 就像是你的浏览器书签。你在网上冲浪，突然想起有个重要的页面还没看，你就说"跳转到书签：工作邮箱"，浏览器二话不说，直接带你飞过去。中间那些乱七八糟的网页？统统不看。`goto` 就是代码世界里的"网页书签"。

**goto 可以往前跳，也可以往后跳**

`goto` 不只能往后跳（跳过代码），还能往前跳（回到之前的代码）。这就像你看电视剧，突然觉得前面那个悬念太精彩了，倒回去重看一遍：

```go
package main

import "fmt"

func main() {

    count := 0

loop:
    fmt.Printf("count = %d\n", count) // count = 0
    count++
    if count < 5 {
        goto loop // 跳回 loop 标签
    }

    fmt.Printf("最终 count = %d\n", count) // 最终 count = 5
}
```

> `goto` 往前跳就像你打游戏时的"读档"——死了？没关系，倒回去重新打。往后跳就像"跳过教程"——教程太无聊了？直接快进到正式关卡。一句话：`goto` 就是代码世界里的时光机，想去哪就去哪。



### 11.1.2 使用限制

**goto 的使用限制是什么？**

Go 语言虽然保留了 `goto`，但对它设置了重重限制——这就像你买了一辆车，但被规定不能上高速公路、不能进城、不能在雨天开。为什么要这样限制？因为 `goto` 实在是太危险了，稍不留神就会把代码搞成一碗意大利面条。

Go 语言对 `goto` 的限制主要有以下几条：

**限制一：不能跳转到其他函数里**

```go
package main

import "fmt"

func main() {

    goto label

    fmt.Println("主函数里的代码")
}

func other() {
label:
    fmt.Println("other 函数里的标签")
}
```

上面这段代码是**错误的**！`goto` 不能跨越函数边界跳转。你不能从 `main` 函数跳到 `other` 函数里——这在 Go 里是不允许的。

**限制二：不能跳转到内部代码块里**

```go
package main

import "fmt"

func main() {

    goto label // 跳入 if 内部

    if true {
label: // 标签不能放在内部代码块里
        fmt.Println("这里")
    }
}
```

上面这段代码是**错误的**！`goto` 不能"跳入"一个代码块（比如 `if`、`for`、`switch` 等）内部。标签只能放在**外层**或者**同一层级**的代码块里。

**限制三：不能跳转到变量声明之前**

```go
package main

import "fmt"

func main() {

    goto label // 跳到变量声明之前
    fmt.Println(x) // x 未声明
    x := 10
label:
    fmt.Println("这里")
}
```

上面这段代码是**错误的**！`goto` 不能跳转到变量声明之前，否则会出现"使用未声明变量"的错误。

**限制四：不能跳转到循环外部**

```go
package main

import "fmt"

func main() {

    goto label

    for i := 0; i < 3; i++ {
        fmt.Println("循环内部")
    }

label:
    fmt.Println("标签在循环外部")
}
```

上面这段代码是**正确的**！标签可以在循环外部，`goto` 可以从循环外部跳到循环内部。

```go
package main

import "fmt"

func main() {

loop:
    for i := 0; i < 3; i++ {
        goto skip // 跳到循环外部
        fmt.Println("这行会被跳过")
    }

skip:
    fmt.Println("跳到循环外部") // 跳到循环外部
}
```

上面这段代码是**正确的**！可以跳到循环外部。

**限制五：不能跳入 if 内部**

```go
package main

import "fmt"

func main() {

    goto label
    if true {
        fmt.Println("if 内部")
    }

    // 不行！不能从外面跳入 if 内部
}
```

**为什么要有这些限制？**

这些限制的目的很简单：**防止代码变成"意大利面条"**。

没有限制的 `goto` 可以让你的代码在任何地方跳来跳去，今天跳到这里，明天跳到那里，用不了多久，你的代码就会变成一团乱麻，连你自己都看不懂。Go 语言的 designers 故意加了这些限制，让 `goto` 只能在一个"合理"的范围内使用。

> `goto` 的限制就像交通规则——你可以在城市里开车，但不能闯红灯、不能逆行、不能开到人行道上。这些规则不是为了刁难你，而是为了保护你自己和别人的安全。`goto` 的限制也是为了保护你的代码——不让它变成一团无法维护的乱码。

**一个合法的 goto 用法示例**

```go
package main

import "fmt"

func main() {

    fmt.Println("开始执行") // 开始执行

    goto skip

    fmt.Println("这行被跳过")

skip:
    fmt.Println("跳到这里执行") // 跳到这里执行

    for i := 0; i < 3; i++ {
        if i == 1 {
            goto skip // 从循环内部跳到标签（合法！）
        }
        fmt.Printf("循环 i = %d\n", i) // 循环 i = 0
    }

skip:
    fmt.Println("最终跳到这里") // 最终跳到这里
}
```

### 11.1.3 适用场景

**goto 的适用场景有哪些？**

虽然 `goto` 被广泛认为是有害的，但在某些特定场景下，它反而是最简单、最清晰的解决方案。Go 语言的 designers 说："我们保留了 `goto`，因为有些场景 `goto` 就是最好的选择。"

下面让我们来看看 `goto` 的几个"正当用途"：

**场景一：跳出多层嵌套循环**

这是 `goto` 最经典的用法。当你有多层嵌套循环，想要从内层循环直接跳到外层循环之外时，`goto` 是最简洁的方式。

```go
package main

import "fmt"

func main() {

    fmt.Println("开始查找...") // 开始查找...

    for i := 0; i < 5; i++ {
        for j := 0; j < 5; j++ {
            fmt.Printf("检查 (%d,%d)\n", i, j) // 检查 (0,0)
            if i == 2 && j == 3 {
                fmt.Printf("找到了！位置 (%d,%d)\n", i, j) // 找到了！位置 (2,3)
                goto found // 跳出所有循环
            }
        }
    }

    fmt.Println("没找到")

found: // 标签在函数层级，可以从任意嵌套深度跳到这里
    fmt.Println("搜索结束") // 搜索结束
}
```

> 重试循环就像你追一个女孩子。追了，没成功；再追，还没成功；继续追……终于有一天，她被你感动了，你就不用再追了（`goto` 到成功分支）。如果用 `for` 循环实现，你得写一个"努力程度"的变量，然后判断努力程度够不够——哪有直接喊"再来一次"（`goto retry`）这么简单粗暴？

**场景四：状态机**

某些场景下，`goto` 可以写出非常清晰的状态机代码：

```go
package main

import "fmt"

func main() {

    state := "idle"

    fmt.Println("状态机启动，当前状态: idle") // 状态机启动，当前状态: idle

next:
    switch state {
    case "idle":
        fmt.Println("执行: 空闲状态，等待事件...")
        state = "running"
    case "running":
        fmt.Println("执行: 运行状态，处理任务...")
        state = "paused"
    case "paused":
        fmt.Println("执行: 暂停状态，可以恢复或停止...")
        state = "stopped"
    case "stopped":
        fmt.Println("执行: 停止状态，退出...")
        return
    }

    goto next
}
```

> 状态机 `goto` 就像你看悬疑剧。你说"先看第一集"，看完后说"播放下一集"，看完后说"播放下一集"……直到看到大结局（return）。你不用记住每一集讲了什么，只需要知道"播完了就播下一集"（`goto next`）。这就是最简单的状态机。

**什么时候不该用 goto？**

虽然 `goto` 有以上这些合法用途，但绝大多数情况下，你都应该用更现代的控制结构：

- 想循环？用 `for`
- 想分支？用 `if`
- 想选择？用 `switch`
- 想提前退出？用 `return`

记住一个原则：**只有当其他控制结构会让你代码更复杂时，才考虑用 `goto`。**



## 11.2 return 语句

### 11.2.1 无结果 return

**无结果 return 是什么？**

无结果 return，就是**最简单的 return**——它不返回任何值，只表示"我要走了，这个函数结束了"。

这就像你下班，直接说"我走了"，然后推门出去。不需要跟任何人交代"我走去哪了"。

无结果 return 主要用于两种场景：

1. **主动退出**：函数执行完了，正常返回
2. **提前返回**：函数还没执行完，但因为某些条件不想继续了，直接走人

**主动退出**

```go
package main

import "fmt"

func greet() {
    fmt.Println("Hello, world!") // Hello, world!
    return // 这个 return 可以省略，但写上也不报错
}

func main() {
    greet()
    fmt.Println("函数执行完毕")
}
```

> 无结果 return 就像你在排队买奶茶。排到你的时候，你突然想起自己忘带钱包了——你会说"不好意思，我不买了"，然后直接走人（return），不会继续跟奶茶店员废话。"提前返回"就是那个"不好意思，我不买了"。

**return 和 fmt.Println 的区别**

你可能会问：为什么不直接用 `fmt.Println` 退出，还要用 `return`？

好问题！`fmt.Println` 只是"打印一行文字"，程序还会继续往下执行；而 `return` 是"直接结束这个函数"，后面的代码全部不执行。

```go
package main

import "fmt"

func test() {
    fmt.Println("第一行")

    fmt.Println("第二行")

    return // 退出函数

    fmt.Println("第三行") // 这行永远不会执行
    fmt.Println("第四行") // 这行永远不会执行
}

func main() {
    test()
    fmt.Println("test 函数结束了")
}
```

> `fmt.Println` 就像你发了一条微信消息，只是"告知"；`return` 就像你直接退出微信，**彻底离开**。发消息之后对方还能继续跟你说话，但退出微信之后，你就已经"不在服务区"了。



### 11.2.2 表达式 return

**表达式 return 是什么？**

表达式 return 就是**带值的 return**——函数不仅要说"我走了"，还要说"我把 XXX 留给你们了"。

这就像你下班的时候，跟同事说"我走了，这个项目文件我放你桌上啦"——你走的时候，留下了一个东西。

在 Go 里，表达式 return 用于有返回值的函数（不是 `void`，而是有具体类型的函数）。

**基本用法**

```go
package main

import "fmt"

func add(a, b int) int {
    sum := a + b
    return sum // 返回 a + b 的结果
}

func main() {
    result := add(3, 5)
    fmt.Println("3 + 5 =", result) // 3 + 5 = 8
}
```

**直接返回表达式**

Go 语言的函数可以写得很简洁，不需要中间变量：

```go
package main

import "fmt"

func add(a, b int) int {
    return a + b // 直接返回表达式
}

func multiply(a, b int) int {
    return a * b // 直接返回表达式
}

func main() {
    fmt.Println("3 + 5 =", add(3, 5)) // 3 + 5 = 8
    fmt.Println("3 * 5 =", multiply(3, 5)) // 3 * 5 = 15
}
```

**多个返回值中的表达式 return**

Go 的函数可以返回多个值，表达式 return 可以返回这些值：

```go
package main

import "fmt"

func divide(a, b int) (int, int) {
    quotient := a / b  // 商
    remainder := a % b // 余数
    return quotient, remainder // 返回两个值
}

func main() {
    q, r := divide(10, 3)
    fmt.Printf("10 / 3 = %d ... %d\n", q, r) // 10 / 3 = 3 ... 1
}
```

**函数式 return**

Go 支持把函数作为返回值，可以写得很优雅：

```go
package main

import "fmt"

func multiplier(factor int) func(int) int {
    return func(x int) int {
        return x * factor // 返回表达式
    }
}

func main() {
    double := multiplier(2)
    triple := multiplier(3)

    fmt.Println("5 * 2 =", double(5)) // 5 * 2 = 10
    fmt.Println("5 * 3 =", triple(5)) // 5 * 3 = 15
}
```

> 表达式 return 就像你点外卖——你不仅"下单"（调用函数），还要"收货"（接收返回值）。你说"给我来一份宫保鸡丁"（`result := add(3, 5)`），商家不仅做了，还给你送来了（`return sum`）。你收到的是一份热腾腾的宫保鸡丁，而不是"您的订单已处理"这条文字信息。

**表达式 return 的注意事项**

1. **返回值类型必须匹配**：声明返回 `int`，就必须返回 `int`，不能返回 `string`

```go
package main

import "fmt"

func getValue() int {
    return 42 // 正确：返回 int
}

func main() {
    fmt.Println("value =", getValue()) // value = 42
}
```

2. **return 后面的表达式会被计算**

```go
package main

import "fmt"

func compute(a, b int) int {
    return a + b*2 // 先计算 b*2，再加上 a
}

func main() {
    fmt.Println("result =", compute(3, 4)) // result = 3 + 4*2 = 11
}
```

> 表达式 return 的求值顺序就像做数学题：先算乘除（`b*2`），后算加减（`a + b*2`）。编译器会把表达式算好，然后把结果返回给你。



### 11.2.3 裸 return

**裸 return 是什么？**

裸 return（Named Return）是 Go 语言的一个特殊语法——在函数声明时给返回值起个名字（命名返回值），然后在函数里直接用 `return` 返回，不需要写具体的值。

这就像你买外卖，商家说"您的订单我们记住了"（命名返回值），你取餐的时候只需要说"给我那份"（`return`），不用再报一遍"宫保鸡丁、微辣、加辣"。

**基本语法**

```go
package main

import "fmt"

func split(sum int) (x, y int) {
    x = sum * 4 / 9 // 给命名返回值赋值
    y = sum - x     // 给命名返回值赋值
    return          // 裸 return，不需要写返回值
}

func main() {
    fmt.Println(split(17)) // 7 10
}
```

看到了吗？`split` 函数的返回值被命名为 `x` 和 `y`，函数体里直接给 `x` 和 `y` 赋值，最后 `return` 的时候不用写 `return x, y`，直接写 `return` 就行——编译器会帮你把 `x` 和 `y` 传回去。

**裸 return 的原理**

Go 会在函数开头创建两个变量 `x` 和 `y`，就像你声明了 `var x, y int` 一样。你在函数里给它们赋值，最后 `return` 会返回它们的当前值。

```go
package main

import "fmt"

func rectProps(width, height float64) (area, perimeter float64) {
    area = width * height         // 计算面积
    perimeter = 2 * (width + height) // 计算周长
    return // 裸 return
}

func main() {
    a, p := rectProps(3.5, 4.2)
    fmt.Printf("面积 = %.2f, 周长 = %.2f\n", a, p) // 面积 = 14.70, 周长 = 15.40
}
```

**裸 return 的注意事项：不要在复杂逻辑中使用**

裸 return 虽然方便，但有个坑——如果你在函数里有多个 `return`，裸 return 容易让人混淆到底返回的是什么。

```go
package main

import "fmt"

func findCode(name string) (code string, err error) {
    // 模拟查表
    if name == "Alice" {
        code = "A100"
        return // 返回 code="A100", err=nil
    }
    if name == "Bob" {
        code = "B200"
        return // 返回 code="B200", err=nil
    }
    // 没找到
    err = fmt.Errorf("name not found: %s", name)
    return // 返回 code="", err=error
}

func main() {
    code, err := findCode("Alice")
    fmt.Printf("Alice: code=%s, err=%v\n", code, err) // Alice: code=A100, err=<nil>

    code, err = findCode("Tom")
    fmt.Printf("Tom: code=%s, err=%v\n", code, err) // Tom: code=, err=name not found: Tom
}
```

**裸 return 与 defer 配合使用的真相**

`defer` 会在 `return` 语句执行**之后**、函数真正返回**之前**执行。注意这个顺序：

1. 先执行 `return` 语句（把返回值赋给命名返回值）
2. 再执行 `defer`
3. 函数返回

这意味着：**defer 里修改命名返回值是 会生效 的**！最终函数返回的是 defer 修改之后的值。

```go
package main

import "fmt"

func test() (n int) {
    defer func() {
        n = 200 // 在 defer 里修改命名返回值！
        fmt.Println("defer 里看到的 n =", n) // defer 里看到的 n = 200
    }()
    n = 100
    return // 先把 n=100 赋给返回值，然后执行 defer（n 变成 200），最终返回 200
}

func main() {
    result := test()
    fmt.Println("函数返回:", result) // 函数返回: 200
}
```

> 裸 return 就像你点外卖，商家在订单上写"加辣、加葱"（命名返回值）。你取餐的时候，外卖小哥说"您的宫保鸡丁"（return），然后你发现外卖已经被外卖小哥偷偷加了辣和葱（defer 修改了命名返回值）。所以裸 return 返回的，是 defer 修改之后的值。

**Go 的 return 执行机制**

Go 的 return 机制是这样的：

```go
n = 100      // 第一步：给命名返回值 n 赋值为 100
return        // 第二步：把 n 的值（100）拷贝到"返回值"这个位置
defer {
    n = 200  // 第三步：defer 修改了 n，n 变成了 200
}
             // 第四步：函数返回，此时 Go 发现命名返回值 n 被 defer 修改了
             //         于是返回 n 的当前值（200）而不是之前的"返回值"（100）
```

Go 的实现比较特殊：**defer 执行完毕后，最终返回的是命名返回值当时的值**，而不是 return 语句执行时拷贝到"返回值"位置的原始值。

> 所以说，**裸 return 返回的是 defer 修改后的值**——这是 Go 的设计，不是 bug。

**裸 return 什么时候用？**

1. **简单函数**：返回值不多，逻辑不复杂，裸 return 能让代码更简洁
2. **需要 defer 清理**：defer 可以在 return 之前做一些清理工作
3. **错误处理**：配合 Go 的多返回值，裸 return 很优雅

```go
package main

import "fmt"

func readFile(name string) (content string, err error) {
    // 模拟读取文件
    if name == "" {
        err = fmt.Errorf("文件名不能为空")
        return
    }
    content = "文件内容: " + name
    return
}

func main() {
    content, err := readFile("test.txt")
    if err != nil {
        fmt.Println("错误:", err)
        return
    }
    fmt.Println(content) // 文件内容: test.txt
}
```

> 裸 return 是 Go 语言的一个"语法糖"——它不是必需的（你完全可以写 `return x, y`），但它能让代码更简洁。不过要记住，**裸 return 返回的是 defer 修改后的值**，这个坑你踩过一次就记住了。



## 11.3 panic 语句

### 11.3.1 panic 触发

**panic 是什么？**

`panic` 是 Go 语言的"紧急刹车"——当程序遇到**无法恢复的错误**时，就会触发 `panic`，程序会立即停止正常执行，进入"恐慌模式"。

这就像你开车时突然爆胎——你不能假装什么都没发生继续开，必须立即停车（触发 panic），打开双闪灯（打印恐慌信息），然后等待救援（程序崩溃退出）。

`panic` 是 Go 错误处理的最**后手段**。只有在"真的没办法了"的情况下才使用，比如：

- 程序遇到了根本无法处理的错误（比如数组越界、空指针）
- 程序员犯了错，需要立即停止程序（比如忘记了某个必选项）

**触发 panic 的两种方式**

方式一：**程序自动触发**（比如数组越界、空指针等）

```go
package main

import "fmt"

func main() {

    fmt.Println("程序开始") // 程序开始

    arr := []int{1, 2, 3}
    fmt.Println("访问 arr[10]...", arr[10]) // 触发 panic: index out of range
}
```

方式二：**手动触发**（调用 `panic()` 函数）

```go
package main

import "fmt"

func main() {

    fmt.Println("程序开始") // 程序开始

    panic("我故意的，程序遇到无法处理的错误！")

    fmt.Println("这行不会执行") // 不会执行
}
```

> panic 就像你点外卖，结果送来的不是你点的宫保鸡丁，而是一盘热气腾腾的"仰望天空"（一道黑暗料理）。你当场崩溃（panic），把外卖扔了（程序中断），然后打电话给客服投诉（打印错误信息）。客服说"非常抱歉，我们会处理"——然后你的订单就取消了（程序退出）。

**panic 的传播机制**

panic 不会只在一个地方停下来——它会**一层层向上传播**，就像多米诺骨牌一样，从触发点一直传到程序最顶层。

```go
package main

import "fmt"

func level3() {
    fmt.Println("level3 开始")
    panic("level3 出错了！")
    fmt.Println("level3 结束")
}

func level2() {
    fmt.Println("level2 开始")
    level3()
    fmt.Println("level2 结束")
}

func level1() {
    fmt.Println("level1 开始")
    level2()
    fmt.Println("level1 结束")
}

func main() {
    fmt.Println("main 开始")
    level1()
    fmt.Println("main 结束")
}
```

> panic 参数 + recover 就像你玩吃鸡游戏时被击倒了（panic），但你的队友及时扶起了你（recover），你说"我被打了"（获取 panic 参数），然后你继续战斗（程序继续运行）。如果你没有被扶起来（没有 recover），你就直接退出了游戏（程序崩溃）。

**什么时候用 panic + recover？**

1. **库/框架级别的错误处理**：在最外层捕获所有 panic，防止整个程序崩溃
2. **关键路径的错误处理**：某个关键函数出错，整个业务就没法继续了
3. **测试时的断言**：单元测试中，某些条件不满足就 panic

但要注意：**正常业务逻辑不要用 panic + recover**，用 error 就行。

```go
package main

import "fmt"

// BAD EXAMPLE（不推荐）
func badDivide(a, b int) int {
    defer func() {
        recover()
    }()
    if b == 0 {
        panic("除数不能为 0")
    }
    return a / b
}

// GOOD EXAMPLE（推荐）
func goodDivide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("除数不能为 0")
    }
    return a / b, nil
}

func main() {
    // 不好：panic + recover 容易滥用
    result := badDivide(10, 0)
    fmt.Println("result =", result) // result = 0

    // 好：用 error 处理正常业务错误
    result, err := goodDivide(10, 0)
    if err != nil {
        fmt.Println("错误:", err) // 错误: 除数不能为 0
    }
}
```

> **记住**：panic 是"紧急刹车"，recover 是"紧急救援"。正常情况下不要急刹车，只有在真正紧急的情况下（比如车要撞了）才用。日常开车（正常业务），用刹车（error）就够了。



## 本章小结

本章我们深入探讨了 Go 语言的三大跳转语句：`goto`、`return` 和 `panic`。虽然 Go 语言以"简洁"著称，但这三个跳转语句各有各的用武之地。

**核心要点回顾：**

1. **`goto`：最古老也最危险的跳转语句**
   - 可以往前跳、往后跳
   - Go 对它施加了诸多限制（不能跨函数、不能跳入代码块内部等）
   - 经典用法：跳出多层嵌套循环、错误处理 goto、状态机
   - 记住：**只有当其他控制结构会让代码更复杂时，才考虑用 goto**

2. **`return`：函数的"退出票"**
   - 无结果 return：只说"我走了"，不返回任何值
   - 表达式 return：说"我走了，把 XXX 留给你们了"
   - 裸 return：命名返回值，可以直接 `return` 不写具体值
   - defer 会修改裸 return 的返回值——这是个经典坑！

3. **`panic`：程序的"紧急刹车"**
   - 触发方式：程序自动触发（数组越界、空指针等）或手动调用 `panic()`
   - panic 会一层层向上传播，直到被 `recover()` 捕获或程序崩溃
   - `recover()` 只能在 `defer` 中使用
   - **可预期的错误用 error，不可恢复的错误用 panic**

**一句话总结：**

`goto` 是老古董，用的时候要三思；`return` 是日常必需，用好裸 return 可以让代码更优雅；`panic` 是核弹，能不爆就不爆，爆了也要用 `recover` 来收拾残局。

**继续下一章前，先问自己几个问题：**

- `goto` 为什么被 Go 语言施加了那么多限制？
- `goto` 的经典使用场景有哪些？
- 裸 return 和普通 return 有什么区别？
- `defer` 为什么能修改裸 return 的返回值？
- `panic` 和 `error` 应该在什么场景下使用？
- `recover` 为什么只能在 `defer` 里调用？

如果能回答上来，说明你已经掌握了 Go 跳转语句的精髓！


