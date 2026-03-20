+++
title = "第12章 数组"
weight = 120
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第12章 数组



## 12.1 数组类型

### 12.1.1 数组定义

**数组是什么？**

数组是 Go 语言中最基础的数据结构——它是一组**相同类型**的元素，按**顺序**排列，放在一个"连续的内存空间"里。

打个比方：如果你有一栋楼，这栋楼有 10 层，每层只能住一个人（都是同一个物种，比如都是人类），这就是一个"数组"。这栋楼的每一层就是一个"元素"，楼层编号就是"索引"，整栋楼就是"数组"。

用更技术的话说：**数组是一个固定长度的、连续存储的、同一类型的元素序列**。

**数组的定义语法**

在 Go 里，定义数组的语法是这样的：

```go
var 数组名 [长度]元素类型
```

注意那个 `[长度]`——数组的长度是**类型的一部分**，这很重要，后面会详细讲。

**一个完整的例子**

```go
package main

import "fmt"

func main() {

    // 定义一个数组，包含 5 个 int 类型的元素
    var scores [5]int

    // 给数组赋值
    scores[0] = 90
    scores[1] = 85
    scores[2] = 78
    scores[3] = 92
    scores[4] = 88

    // 访问数组元素
    fmt.Println("第一个成绩:", scores[0]) // 第一个成绩: 90
    fmt.Println("第二个成绩:", scores[1]) // 第二个成绩: 85
    fmt.Println("第三个成绩:", scores[2]) // 第三个成绩: 78
    fmt.Println("第四个成绩:", scores[3]) // 第四个成绩: 92
    fmt.Println("第五个成绩:", scores[4]) // 第五个成绩: 88

    // 打印整个数组
    fmt.Println("所有成绩:", scores) // 所有成绩: [90 85 78 92 88]
}
```

**数组的初始化**

定义数组时可以同时初始化，不用一个一个赋值：

```go
package main

import "fmt"

func main() {

    // 方式一：完整初始化
    var nums1 [3]int = [3]int{1, 2, 3}
    fmt.Println("nums1:", nums1) // nums1: [1 2 3]

    // 方式二：简短初始化（编译器自动推断长度）
    nums2 := [...]int{4, 5, 6, 7}
    fmt.Println("nums2:", nums2) // nums2: [4 5 6 7]

    // 方式三：部分初始化（未初始化的元素为该类型的零值）
    nums3 := [5]int{1, 2, 3}
    fmt.Println("nums3:", nums3) // nums3: [1 2 3 0 0]
}
```

> 数组就像是你家的鞋柜。你家玄关有一个固定大小的鞋柜（比如 5 格），每格只能放一双鞋（同一类型），而且鞋是按顺序放的（第一格放拖鞋，第二格放运动鞋……）。鞋柜的大小是固定的——你不能硬塞进去第六双鞋。如果哪一格空了，那就是零值（对于鞋子来说就是"没有鞋"）。



### 12.1.2 长度属性

**长度属性是什么？**

Go 数组有一个内置的属性，叫做 `len()`（length 的缩写），用来获取数组的长度。这就像你数一数鞋柜里有多少格，就能知道鞋柜能放多少双鞋。

**使用 len() 获取长度**

```go
package main

import "fmt"

func main() {

    var arr [5]int
    fmt.Println("数组长度:", len(arr)) // 数组长度: 5

    arr2 := [3]string{"苹果", "香蕉", "橙子"}
    fmt.Println("arr2 长度:", len(arr2)) // arr2 长度: 3

    arr3 := [...]int{1, 2, 3, 4, 5, 6, 7, 8, 9}
    fmt.Println("arr3 长度:", len(arr3)) // arr3 长度: 9
}
```

#### 12.1.2.1 长度是类型组成部分

**长度是类型的一部分意味着什么？**

在 Go 语言中，数组的长度是**类型的一部分**。这意味着 `[5]int` 和 `[10]int` 是**两种完全不同的类型**，就像"5座车"和"7座车"是两种不同的车型一样。

```go
package main

import "fmt"

func main() {

    var arr1 [5]int
    var arr2 [5]int
    var arr3 [10]int

    fmt.Printf("arr1 的类型: %T\n", arr1) // arr1 的类型: [5]int
    fmt.Printf("arr2 的类型: %T\n", arr2) // arr2 的类型: [5]int
    fmt.Printf("arr3 的类型: %T\n", arr3) // arr3 的类型: [10]int

    // arr1 和 arr2 类型相同，可以赋值
    arr1 = arr2
    fmt.Println("arr1 = arr2 成功:", arr1) // arr1 = arr2 成功: [0 0 0 0 0]

    // arr1 和 arr3 类型不同，不能直接赋值！
    // arr1 = arr3 // 编译错误：cannot use arr3 (type [10]int) as type [5]int
    fmt.Println("arr1 和 arr3 类型不同，不能直接赋值")
}
```

> 长度是类型的一部分，就像"5座车"和"7座车"是两种不同的车型。你不能把一辆 7 座商务车塞进 5 座车库里——空间不够。同理，你也不能把 `[10]int` 的值赋给 `[5]int` 的变量——类型不匹配。

**长度不同的数组不能互相赋值**

```go
package main

import "fmt"

func printArray(arr [5]int) {
    fmt.Println("接收到的数组:", arr)
}

func main() {

    arr5 := [5]int{1, 2, 3, 4, 5}
    arr10 := [10]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

    printArray(arr5)   // 正确：类型是 [5]int
    // printArray(arr10) // 错误：类型是 [10]int，不能传给 [5]int 的参数
}
```

这是 Go 数组和切片（slice）的最大区别之一。切片的长度不是类型的一部分，所以 `[...]int{1,2,3}` 和 `[...]int{1,2,3,4}` 可以赋给同一个 `[]int` 变量，但数组不行。

#### 12.1.2.2 长度必须是常量

**长度必须是常量意味着什么？**

Go 数组的长度必须是**常量表达式**——也就是说，长度必须在编译时就确定，不能是变量。

```go
package main

import "fmt"

func main() {

    // 正确：长度是常量
    var arr1 [5]int
    fmt.Println("arr1 长度:", len(arr1)) // arr1 长度: 5

    // 正确：用常量表达式作为长度
    const size = 10
    var arr2 [size]int
    fmt.Println("arr2 长度:", len(arr2)) // arr2 长度: 10

    // 正确：用字面量作为长度
    var arr3 [3 + 4]int
    fmt.Println("arr3 长度:", len(arr3)) // arr3 长度: 7

    // 错误！长度不能是变量
    // n := 5
    // var arr4 [n]int // 编译错误：array length N must be constant
}
```

> 长度必须是常量，就像你订制鞋柜时，厂家问你"要几格的？"，你不能回答"看情况吧"——必须给一个确切的数字。因为鞋柜的大小是在生产时就确定的，不能等摆进去的时候再说"好像有点挤，再加一格吧"。

**为什么长度必须是常量？**

这是因为数组的大小直接关系到内存分配。编译器需要知道要分配多少内存，才能生成正确的代码。如果长度是变量，编译器就无法确定要分配多少内存——这在编译时是无法解决的。

```go
package main

import "fmt"

const MaxSize = 100

func main() {

    // 正确：可以用 const 关键字声明的常量
    var arr1 [MaxSize]int
    fmt.Println("arr1 长度:", len(arr1)) // arr1 长度: 100

    // 正确：可以用枚举值
    type Color int
    const (
        Red Color = iota
        Green
        Blue
    )
    var arr2 [Blue + 1]int
    fmt.Println("arr2 长度:", len(arr2)) // arr2 长度: 3

    // 错误：运行时才知道的值
    // n := 5
    // var arr3 [n]int // 编译错误
}
```



### 12.1.3 元素类型

**元素类型是什么？**

Go 数组的每个元素都必须是**相同类型**的。这个类型是在定义数组时声明的，一旦声明，就不能改变。

打个比方：你买了一个"整数鞋柜"（`[5]int`），那就只能放整数进去；你买了一个"字符串鞋柜"（`[5]string`），那就只能放字符串进去。你不能把一只猫放进"人类鞋柜"里——这不是鞋柜的问题，是你自己搞错了。

**不同元素类型的数组**

```go
package main

import "fmt"

func main() {

    // int 数组
    intArr := [3]int{1, 2, 3}
    fmt.Println("intArr:", intArr) // intArr: [1 2 3]

    // float64 数组
    floatArr := [3]float64{1.5, 2.7, 3.14}
    fmt.Println("floatArr:", floatArr) // floatArr: [1.5 2.7 3.14]

    // string 数组
    strArr := [3]string{"hello", "world", "go"}
    fmt.Println("strArr:", strArr) // strArr: [hello world go]

    // bool 数组
    boolArr := [3]bool{true, false, true}
    fmt.Println("boolArr:", boolArr) // boolArr: [true false true]

    // 混合类型？不行！
    // mixedArr := [3]interface{}{1, "hello", true} // 这不是数组，这是切片！
}
```

**数组元素类型是类型的一部分**

就像长度是类型的一部分一样，元素类型也是类型的一部分。`[5]int` 和 `[5]string` 是完全不同的两种类型。

```go
package main

import "fmt"

func main() {

    var arr1 [5]int
    var arr2 [5]string

    fmt.Printf("arr1 的类型: %T\n", arr1) // arr1 的类型: [5]int
    fmt.Printf("arr2 的类型: %T\n", arr2) // arr2 的类型: [5]string

    // arr1 和 arr2 类型不同，不能互相赋值
    // arr1 = arr2 // 编译错误：cannot use arr2 (type [5]string) as type [5]int
}
```

**数组的元素可以是数组（嵌套数组）**

Go 的数组元素可以是任意类型，包括数组——这就形成了**多维数组**。

```go
package main

import "fmt"

func main() {

    // 一个 2x3 的二维数组（本质上是一个"数组的数组"）
    var matrix [2][3]int

    // 给二维数组赋值
    matrix[0][0] = 1
    matrix[0][1] = 2
    matrix[0][2] = 3
    matrix[1][0] = 4
    matrix[1][1] = 5
    matrix[1][2] = 6

    fmt.Println("matrix:", matrix) // matrix: [[1 2 3] [4 5 6]]

    // 直接初始化二维数组
    matrix2 := [2][3]int{
        {10, 20, 30},
        {40, 50, 60},
    }
    fmt.Println("matrix2:", matrix2) // matrix2: [[10 20 30] [40 50 60]]
}
```

> 元素类型是数组的"基因"——你买了一个"整数基因"的数组，它就永远只能装整数；你买了一个"字符串基因"的数组，它就永远只能装字符串。这不是歧视，这是类型系统的规则。如果你想要能装"任意类型"的容器，请使用**切片（slice）**或者**接口切片（[]interface{}）**。

**元素类型的零值**

数组的元素如果没有被初始化，会有一个默认值（零值）：

```go
package main

import "fmt"

func main() {

    var intArr [3]int
    fmt.Println("intArr 零值:", intArr) // intArr 零值: [0 0 0]

    var strArr [3]string
    fmt.Println("strArr 零值:", strArr) // strArr 零值: [  ]

    var boolArr [3]bool
    fmt.Println("boolArr 零值:", boolArr) // boolArr 零值: [false false false]

    var floatArr [3]float64
    fmt.Println("floatArr 零值:", floatArr) // floatArr 零值: [0 0 0]
}
```

| 类型 | 零值 |
|------|------|
| int 系列 | 0 |
| float 系列 | 0.0 |
| string | ""（空字符串）|
| bool | false |
| pointer | nil |



### 12.1.4 值语义

**值语义是什么？**

Go 数组的赋值和传递是**值语义**——也就是说，当你把一个数组赋值给另一个变量，或者传给函数时，**整个数组都会被拷贝一份**。

这就像你把一本书复印了一份，原件和复印件是**完全独立的**。你修改复印件，不会影响原件；修改原件，也不会影响复印件。

**值语义赋值**

```go
package main

import "fmt"

func main() {

    // 定义一个数组
    original := [3]int{1, 2, 3}
    fmt.Println("original:", original) // original: [1 2 3]

    // 把 original 赋值给 copy（会拷贝整个数组）
    copy := original

    // 修改 copy 的第一个元素
    copy[0] = 100

    // 打印两个数组
    fmt.Println("original:", original) // original: [1 2 3]（没变！）
    fmt.Println("copy:", copy) // copy: [100 2 3]
}
```

看到了吗？修改 `copy` 完全没有影响 `original`，因为它们是两个独立的数组。

#### 12.1.4.1 数组赋值

**数组赋值的特点**

Go 数组的赋值是**整个拷贝**，不是引用传递。这与一些其他语言（如 C 语言的数组名作为指针不同）。

```go
package main

import "fmt"

func main() {

    // 定义数组
    arr1 := [3]int{10, 20, 30}
    arr2 := [3]int{100, 200, 300}

    fmt.Println("赋值前:")
    fmt.Println("arr1:", arr1) // arr1: [10 20 30]
    fmt.Println("arr2:", arr2) // arr2: [100 200 300]

    // 把 arr1 赋值给 arr2（会拷贝所有元素）
    arr2 = arr1

    fmt.Println("赋值后:")
    fmt.Println("arr1:", arr1) // arr1: [10 20 30]
    fmt.Println("arr2:", arr2) // arr2: [10 20 30]

    // 修改 arr1
    arr1[0] = 999

    fmt.Println("修改 arr1 后:"
    fmt.Println("arr1:", arr1) // arr1: [999 20 30]
    fmt.Println("arr2:", arr2) // arr2: [10 20 30]（没变！）
}
```

> 数组赋值就像你把一首歌从手机拷贝到电脑。拷贝完成后，两边都有这首歌的完整副本。你在电脑上删了这首歌，手机上的原唱还在；你在手机上改了歌名，电脑上的还是老名字。这就是"值语义"——拷贝之后，两边互不影响。

#### 12.1.4.2 数组传参

**数组传参的特点**

把数组传给函数时，也会**拷贝整个数组**。这意味着函数内部对数组的修改，不会影响外面的原始数组。

```go
package main

import "fmt"

func modifyArray(arr [3]int) {
    // 修改传入数组的第一个元素
    arr[0] = 999
    fmt.Println("函数内部，修改后 arr:", arr) // 函数内部，修改后 arr: [999 20 30]
}

func main() {

    // 定义数组
    original := [3]int{1, 2, 3}
    fmt.Println("调用函数前，original:", original) // 调用函数前，original: [1 2 3]

    // 把数组传给函数
    modifyArray(original)

    fmt.Println("调用函数后，original:", original) // 调用函数后，original: [1 2 3]（没变！）
}
```

> 数组传参就像你把一本书借给你的朋友。你朋友在书上加了批注，但你的原书还是干干净净的——因为朋友拿到的是书的**复印件**，不是原件。你朋友在复印件上画再多圈圈，原件也不会有任何一个圈圈。

**传参的性能问题**

由于数组是值语义，传参时会拷贝整个数组。如果数组很大（比如有 100 万个元素），拷贝的代价会非常高昂！

```go
package main

import "fmt"

// 危险！这会拷贝整个数组
func dangerousFunc(arr [1000000]int) {
    // ...
}

// 安全：使用切片
func safeFunc(arr []int) {
    // ...
}

func main() {

    // 创建一个大数组
    bigArr := [1000000]int{}
    fmt.Println("bigArr 大小:", len(bigArr)) // bigArr 大小: 1000000

    // 传给函数，会拷贝 100 万个元素！
    dangerousFunc(bigArr)

    // 传给切片，不会拷贝
    safeFunc(bigArr[:])
}
```

> 传大数组的问题就像你搬家——如果你要把一栋楼（100 万个元素的数组）从 A 地搬到 B 地，你得把整栋楼拆了（拷贝），运到 B 地再重建（赋值）。这得多慢啊！但如果你是租了一栋楼（切片），你只需要把钥匙（指针）交给对方，让对方去住那栋楼（共享底层数据），快多了！

#### 12.1.4.3 性能考量

**数组的性能特点**

Go 数组是值语义，这带来了以下性能特点：

1. **赋值和传参都需要拷贝整个数组**
2. **大数组的拷贝开销很大**
3. **但正因为是值语义，数据是独立存储的，安全性好**

**如何优化数组的性能？**

1. **尽量用切片代替数组**——切片是引用语义，赋值和传参只拷贝指针，不拷贝数据

```go
package main

import "fmt"

func main() {

    // 数组（值语义）
    arr := [3]int{1, 2, 3}
    copy := arr // 拷贝整个数组
    fmt.Println("数组赋值，拷贝了", len(arr), "个元素") // 数组赋值，拷贝了 3 个元素

    // 切片（引用语义）
    slice := []int{1, 2, 3}
    sliceCopy := slice // 只拷贝了指针（8字节），没拷贝数据
    fmt.Println("切片赋值，只拷贝了指针")
}
```

2. **如果必须用数组，尽量用指针传递**

```go
package main

import "fmt"

func modifyViaPointer(arr *[3]int) {
    // 用指针传递，只拷贝 8 字节的指针
    arr[0] = 999
}

func main() {

    arr := [3]int{1, 2, 3}
    fmt.Println("修改前:", arr) // 修改前: [1 2 3]
    modifyViaPointer(&arr)
    fmt.Println("修改后:", arr) // 修改后: [999 2 3]
}
```

3. **不要返回大数组**——返回大数组也会触发拷贝

```go
package main

import "fmt"

// BAD：返回大数组（会拷贝）
func badReturn() [1000000]int {
    arr := [1000000]int{}
    arr[0] = 42
    return arr // 拷贝 100 万个元素！
}

// GOOD：返回切片（只拷贝指针）
func goodReturn() []int {
    slice := make([]int, 1000000)
    slice[0] = 42
    return slice // 只拷贝 8 字节的指针！
}

func main() {
    // ...
}
```

> 性能考量就像你搬家。搬一栋楼（数组）费时费力，搬一张房产证（切片指针）就快多了。所以，**日常使用中优先选择切片**，只有在需要"固定长度"和"值语义"的场景下才使用数组。



## 12.2 数组创建

### 12.2.1 显式长度创建

**显式长度创建是什么？**

显式长度创建就是在定义数组时，**明确写出数组的长度**。这是最直接的创建方式。

语法：

```go
var 数组名 [长度]元素类型
数组名 := [长度]元素类型{初始化值}
数组名 := [长度]元素类型{索引0: 值0, 索引1: 值1, ...}
```

**一个完整的例子**

```go
package main

import "fmt"

func main() {

    // 方式一：先声明，后赋值
    var arr1 [5]int
    arr1[0] = 10
    arr1[1] = 20
    arr1[2] = 30
    arr1[3] = 40
    arr1[4] = 50
    fmt.Println("arr1:", arr1) // arr1: [10 20 30 40 50]

    // 方式二：声明时初始化
    arr2 := [5]int{10, 20, 30, 40, 50}
    fmt.Println("arr2:", arr2) // arr2: [10 20 30 40 50]

    // 方式三：只初始化部分元素
    arr3 := [5]int{1, 2, 3}
    fmt.Println("arr3:", arr3) // arr3: [1 2 3 0 0]

    // 方式四：指定索引初始化
    arr4 := [5]int{0: 100, 4: 500}
    fmt.Println("arr4:", arr4) // arr4: [100 0 0 0 500]

    // 方式五：混合初始化
    arr5 := [5]int{1, 2, 4: 100, 3: 50}
    fmt.Println("arr5:", arr5) // arr5: [1 2 0 50 100]
}
```

> 显式长度创建就像你买车。你告诉 4S 店："我要买一辆 5 座的 SUV"。这辆车的座位数（长度）是固定的 5 座，不能多也不能少。你可以选择要什么颜色（初始化值），但座位数就是 5 座，不会因为你没选装某个配置就变成 4 座或者 6 座。

**显式长度的应用场景**

1. **固定长度的配置数据**
2. **需要明确数组大小的场景**
3. **性能敏感的的场景（数组比切片更快）**

```go
package main

import "fmt"

func main() {

    // 一年 12 个月，可以用固定长度的数组存储
    months := [12]string{
        "一月", "二月", "三月", "四月",
        "五月", "六月", "七月", "八月",
        "九月", "十月", "十一月", "十二月",
    }

    fmt.Println("一年有", len(months), "个月") // 一年有 12 个月
    fmt.Println("第 1 个月是:", months[0]) // 第 1 个月是: 一月
    fmt.Println("第 12 个月是:", months[11]) // 第 12 个月是: 十二月
}
```



### 12.2.2 推导长度创建

**推导长度创建是什么？**

推导长度创建就是在定义数组时，用 `...` 代替长度，让编译器**根据初始化值的数量自动计算长度**。

语法：

```go
数组名 := [...]元素类型{值1, 值2, 值3, ...}
```

编译器会数一数你给了几个初始值，然后自动把 `...` 替换成那个数字。

**一个完整的例子**

```go
package main

import "fmt"

func main() {

    // 用 ... 让编译器自动推断长度
    arr1 := [...]int{1, 2, 3}
    fmt.Println("arr1 长度:", len(arr1)) // arr1 长度: 3
    fmt.Println("arr1:", arr1) // arr1: [1 2 3]

    // 推断长度为 5
    arr2 := [...]string{"苹果", "香蕉", "橙子", "西瓜", "葡萄"}
    fmt.Println("arr2 长度:", len(arr2)) // arr2 长度: 5
    fmt.Println("arr2:", arr2) // arr2: [苹果 香蕉 橙子 西瓜 葡萄]

    // 推断长度为 7
    arr3 := [...]bool{true, false, true, true, false, false, true}
    fmt.Println("arr3 长度:", len(arr3)) // arr3 长度: 7
    fmt.Println("arr3:", arr3) // arr3: [true false true true false false true]
}
```

#### 12.2.2.1 ... 语法

**... 语法详解**

`...` 是 Go 语言的一个特殊语法，用在数组定义中表示"让编译器自动计算长度"。

注意：`...` 只用在**声明数组时**的长度位置，不能用在其他任何地方。

```go
package main

import "fmt"

func main() {

    // 正常写法
    arr1 := [3]int{1, 2, 3}

    // 用 ... 替代长度
    arr2 := [...]int{1, 2, 3}

    // 两者是等价的
    fmt.Println("arr1:", arr1) // arr1: [1 2 3]
    fmt.Println("arr2:", arr2) // arr2: [1 2 3]

    // arr1 和 arr2 类型相同吗？
    fmt.Printf("arr1 类型: %T\n", arr1) // arr1 类型: [3]int
    fmt.Printf("arr2 类型: %T\n", arr2) // arr2 类型: [3]int
}
```

**... 和 明确长度的区别**

| 写法 | 类型 | 说明 |
|------|------|------|
| `[3]int{1,2,3}` | `[3]int` | 长度固定为 3 |
| `[...]int{1,2,3}` | `[3]int` | 编译器推断为 3 |
| `[]int{1,2,3}` | `[]int` | 这是切片，不是数组！|

```go
package main

import "fmt"

func main() {

    // 数组：长度固定
    arr := [3]int{1, 2, 3}
    fmt.Printf("arr 类型: %T, 值: %v\n", arr, arr) // arr 类型: [3]int, 值: [1 2 3]

    // 切片：长度可变
    slice := []int{1, 2, 3}
    fmt.Printf("slice 类型: %T, 值: %v\n", slice, slice) // slice 类型: []int, 值: [1 2 3]

    // 注意！[...] 是数组，不是切片！
    arrFromDot := [...]int{1, 2, 3}
    fmt.Printf("arrFromDot 类型: %T, 值: %v\n", arrFromDot, arrFromDot) // arrFromDot 类型: [3]int, 值: [1 2 3]
}
```

> `...` 语法就像你点外卖时说"来一份"——老板会根据你点的菜自动给你配一份，不用你事先说"我要 3 个菜"。"来一份"让老板自己数，`[...]` 让编译器自己数。数的过程在编译时完成，所以生成的代码跟手动写长度是一样的。

**... 的限制**

`...` 只能用于**数组声明时**，不能用于其他任何地方：

```go
package main

import "fmt"

func main() {

    // 正确：... 用于数组声明
    arr := [...]int{1, 2, 3, 4, 5}
    fmt.Println("arr:", arr) // arr: [1 2 3 4 5]

    // 错误！... 不能用在其他地方
    // n := ... // 错误！
    // fmt.Println(arr[...]) // 错误！
}
```



### 12.2.3 索引初始化

**索引初始化是什么？**

索引初始化就是在创建数组时，**明确指定每个索引位置的值**，而不是按顺序排列。

这就像你搬家时跟搬家工人说："第一格放电视，第二格放冰箱，第三格放洗衣机……"——而不是让他们按顺序把东西塞进去。

语法：

```go
数组名 := [长度]元素类型{索引0: 值0, 索引1: 值1, 索引2: 值2, ...}
```

**一个完整的例子**

```go
package main

import "fmt"

func main() {

    // 指定索引初始化
    arr := [5]int{0: 100, 2: 200, 4: 300}
    fmt.Println("arr:", arr) // arr: [100 0 200 0 300]

    // 其他索引位置的元素为零值
    fmt.Println("arr[1]:", arr[1]) // arr[1]: 0
    fmt.Println("arr[3]:", arr[3]) // arr[3]: 0
}
```

#### 12.2.3.1 指定索引

**指定索引的语法**

```go
package main

import "fmt"

func main() {

    // 指定部分索引
    fruits := [5]string{0: "苹果", 2: "香蕉", 4: "橙子"}
    fmt.Println("fruits:", fruits) // fruits: [苹果  香蕉  橙子]
    fmt.Println("fruits[0]:", fruits[0]) // fruits[0]: 苹果
    fmt.Println("fruits[1]:", fruits[1]) // fruits[1]:  (空字符串)
    fmt.Println("fruits[2]:", fruits[2]) // fruits[2]: 香蕉
    fmt.Println("fruits[3]:", fruits[3]) // fruits[3]:  (空字符串)
    fmt.Println("fruits[4]:", fruits[4]) // fruits[4]: 橙子

    // 索引可以乱序
    arr := [5]int{4: 100, 0: 10, 2: 50}
    fmt.Println("arr:", arr) // arr: [10 0 50 0 100]
}
```

**指定索引的好处**

1. **可以跳着初始化**：不用按顺序
2. **可以只初始化部分元素**：其他位置为零值
3. **代码更清晰**：明确知道每个索引放的是什么

```go
package main

import "fmt"

func main() {

    // 用指定索引初始化一个"成绩单"
    scores := [10]int{
        0: 90,  // 第1个学生：90分
        3: 85,  // 第4个学生：85分
        7: 92,  // 第8个学生：92分
        // 其他学生：0分（未参加考试）
    }

    fmt.Println("成绩单:", scores) // 成绩单: [90 0 0 85 0 0 0 92 0 0]
    fmt.Printf("第1个学生: %d分\n", scores[0]) // 第1个学生: 90分
    fmt.Printf("第4个学生: %d分\n", scores[3]) // 第4个学生: 85分
    fmt.Printf("第8个学生: %d分\n", scores[7]) // 第8个学生: 92分
}
```

#### 12.2.3.2 稀疏初始化

**稀疏初始化是什么？**

稀疏初始化就是数组的很多元素是"空"的（零值），只有少数几个位置有值。这在初始化"稀疏数据"（比如邻接表、配置表）时非常有用。

```go
package main

import "fmt"

func main() {

    // 创建一个很大的数组，但只初始化少数几个位置
    // 这就是"稀疏"数组——大部分位置都是零值
    sparse := [1000]int{
        0: 1,
        500: 2,
        999: 3,
        // 其他 997 个位置都是 0
    }

    fmt.Println("sparse[0]:", sparse[0]) // sparse[0]: 1
    fmt.Println("sparse[500]:", sparse[500]) // sparse[500]: 2
    fmt.Println("sparse[999]:", sparse[999]) // sparse[999]: 3
    fmt.Println("sparse[1]:", sparse[1]) // sparse[1]: 0
    fmt.Println("sparse[998]:", sparse[998]) // sparse[998]: 0

    fmt.Println("sparse 长度:", len(sparse)) // sparse 长度: 1000
}
```

**稀疏初始化的应用场景**

1. **邻接表**：图论中表示稀疏图
2. **配置表**：很多配置项有默认值，只有少数需要设置
3. **字典映射**：用数组索引模拟稀疏映射

```go
package main

import "fmt"

func main() {

    // 用稀疏数组模拟一个"年龄分布统计"
    // 假设只统计 0-9岁、30-39岁、80-89岁三个年龄段的人数
    ageStats := [100]int{
        0: 5,   // 0-9岁有5个人（这里用索引0代表0-9岁区间）
        30: 12, // 30-39岁有12个人
        80: 3,  // 80-89岁有3个人
    }

    fmt.Println("年龄分布统计:")
    fmt.Printf("0-9岁: %d人\n", ageStats[0]) // 0-9岁: 5人
    fmt.Printf("30-39岁: %d人\n", ageStats[30]) // 30-39岁: 12人
    fmt.Printf("80-89岁: %d人\n", ageStats[80]) // 80-89岁: 3人

    total := ageStats[0] + ageStats[30] + ageStats[80]
    fmt.Printf("总人数: %d人\n", total) // 总人数: 20人
}
```

> 稀疏初始化就像你在一张巨大的 Excel 表里填表。表有 1000 行，但你只填了 3 行，其他行都是空的（零值）。这张表虽然大，但只占你 3 个格子的内容，其他格子虽然存在但是空的。稀疏数组也是这个道理——数组长度是固定的 1000，但只初始化了 3 个位置。



### 12.2.4 零值初始化

**零值初始化是什么？**

零值初始化就是只声明数组，**不初始化**，数组的每个元素会自动获得该类型的"零值"（默认值）。

这就像你买了一个鞋柜（声明数组），但还没往里面放鞋（初始化），鞋柜里的每一格都是空的（零值）。

**零值初始化的例子**

```go
package main

import "fmt"

func main() {

    // 声明一个数组，但不初始化
    var arr [5]int
    fmt.Println("arr:", arr) // arr: [0 0 0 0 0]

    // 声明一个字符串数组
    var strArr [3]string
    fmt.Println("strArr:", strArr) // strArr: [  ]

    // 声明一个布尔数组
    var boolArr [3]bool
    fmt.Println("boolArr:", boolArr) // boolArr: [false false false]

    // 声明一个浮点数组
    var floatArr [3]float64
    fmt.Println("floatArr:", floatArr) // floatArr: [0 0 0]
}
```

**零值的类型对应表**

| 类型 | 零值 |
|------|------|
| int 系列 | 0 |
| float 系列 | 0.0 |
| string | ""（空字符串）|
| bool | false |
| pointer | nil |
| array | 递归地，每个元素都是其类型的零值 |

```go
package main

import "fmt"

func main() {

    // 二维数组的零值
    var matrix [2][3]int
    fmt.Println("matrix 零值:", matrix) // matrix 零值: [[0 0 0] [0 0 0]]

    // 数组的数组的零值
    var nested [2][2][2]int
    fmt.Println("nested 零值:", nested) // nested 零值: [[[0 0] [0 0]] [[0 0] [0 0]]]
}
```

**零值初始化的用途**

1. **延迟初始化**：先声明，后赋值
2. **默认值处理**：某些场景下零值就是合理的默认值
3. **安全初始化**：确保数组不会有"脏数据"

```go
package main

import "fmt"

func main() {

    // 场景一：先声明，后赋值
    var nums [5]int
    fmt.Println("声明后:", nums) // 声明后: [0 0 0 0 0]

    nums[0] = 100
    nums[4] = 500
    fmt.Println("赋值后:", nums) // 赋值后: [100 0 0 0 500]

    // 场景二：累加器数组
    var count [10]int
    count[3]++
    count[3]++
    count[7]++
    fmt.Println("计数数组:", count) // 计数数组: [0 0 0 2 0 0 0 1 0 0]

    // 场景三：布尔标志数组
    var visited [5]bool
    visited[2] = true
    fmt.Println("访问记录:", visited) // 访问记录: [false false true false false]
}
```

> 零值初始化就像你搬进一个新房子——所有房间都是空的（零值），你想放什么家具（赋值）都行。但如果你买的是二手房（已初始化的数组），房间里可能还有前任住户留下的旧家具（旧数据），你得先清理干净才能用。Go 的零值初始化保证了每个数组都是"新房"——干干净净，不会出现奇怪的数据。



## 12.3 数组操作

### 12.3.1 元素访问

**元素访问是什么？**

数组的元素访问就是通过**索引**（下标）来读取或修改数组中的某个元素。

Go 的数组索引从 **0** 开始，到 **len-1** 结束。第一个元素的索引是 0，第二个是 1，以此类推。

这就像你住在一栋 10 层楼的公寓里——第一层的门牌号是 101，第二层是 102，以此类推。你想找第 5 层的人，就得去 501（索引 4）。

#### 12.3.1.1 索引访问

**索引访问的语法**

```go
数组名[索引] // 读取
数组名[索引] = 值 // 写入
```

```go
package main

import "fmt"

func main() {

    arr := [5]int{10, 20, 30, 40, 50}

    // 读取元素
    fmt.Println("第一个元素:", arr[0]) // 第一个元素: 10
    fmt.Println("第二个元素:", arr[1]) // 第二个元素: 20
    fmt.Println("第三个元素:", arr[2]) // 第三个元素: 30
    fmt.Println("第四个元素:", arr[3]) // 第四个元素: 40
    fmt.Println("第五个元素:", arr[4]) // 第五个元素: 50

    // 写入元素
    arr[0] = 100
    arr[4] = 500
    fmt.Println("修改后:", arr) // 修改后: [100 20 30 40 500]
}
```

**索引越界的陷阱**

Go 的数组索引是**严格检查**的——如果你访问的索引超出了数组的范围，程序会**立即 panic**，而不是像某些语言那样返回undefined或者自动扩展数组。

```go
package main

import "fmt"

func main() {

    arr := [5]int{1, 2, 3, 4, 5}

    fmt.Println("arr[4]:", arr[4]) // arr[4]: 5

    // 越界访问！数组只有 5 个元素，索引最大是 4
    // arr[5] 会 panic！
    fmt.Println("arr[5]:", arr[5]) // panic: index out of bounds [5] with length 5
}
```

> 索引越界就像你住在一栋 5 层楼的公寓里，但你非要去 6 楼找朋友——保安会把你拦住，说"这栋楼没有 6 楼！"Go 语言的索引检查就是这么严格——它不会让你"误闯"，而是直接让你"死机重启"（panic）。

#### 12.3.1.2 越界检查

**越界检查是什么？**

Go 编译器会在运行时**自动检查数组索引**，一旦发现越界，就会触发 panic。这就是为什么 Go 比 C 语言更安全——C 语言的数组越界是"未定义行为"，可能不会报错，但会导致不可预期的结果。

**越界的各种情况**

```go
package main

import "fmt"

func main() {

    arr := [3]int{1, 2, 3}

    // 情况一：索引为负数
    // arr[-1] 会 panic

    // 情况二：索引等于长度
    // arr[3] 会 panic（合法索引是 0, 1, 2）

    // 情况三：索引大于长度
    // arr[100] 会 panic

    // 正确访问
    fmt.Println("arr[0]:", arr[0]) // arr[0]: 1
    fmt.Println("arr[1]:", arr[1]) // arr[1]: 2
    fmt.Println("arr[2]:", arr[2]) // arr[2]: 3

    // 打印数组长度
    fmt.Println("数组长度:", len(arr)) // 数组长度: 3
    fmt.Println("最大合法索引:", len(arr)-1) // 最大合法索引: 2
}
```

**如何避免越界错误？**

1. **使用循环时确保索引从 0 到 len-1**
2. **访问前先检查长度**
3. **使用 `range` 遍历代替索引遍历**

```go
package main

import "fmt"

func main() {

    arr := [5]int{10, 20, 30, 40, 50}

    // 安全遍历方式一：for 循环
    for i := 0; i < len(arr); i++ {
        fmt.Printf("arr[%d] = %d\n", i, arr[i])
    }

    fmt.Println("---")

    // 安全遍历方式二：for range（更推荐）
    for i, v := range arr {
        fmt.Printf("arr[%d] = %d\n", i, v)
    }
}
```

> 越界检查是 Go 语言的一道"安全门"——它不允许你做危险的事情。相比之下，C 语言的数组越界是"门没锁，随便进"——你可能进去偷东西（读取脏数据），也可能进去放炸弹（写入脏数据），后果不可预期。Go 语言直接把门锁死，"进门请刷卡"，虽然麻烦一点，但安全多了。



### 12.3.2 数组遍历

**数组遍历是什么？**

数组遍历就是按顺序访问数组中的每个元素。Go 语言支持两种遍历方式：索引遍历（`for` + 索引）和 `range` 遍历。

#### 12.3.2.1 索引遍历

**索引遍历的语法**

```go
for i := 0; i < len(arr); i++ {
    fmt.Println(arr[i])
}
```

```go
package main

import "fmt"

func main() {

    fruits := [4]string{"苹果", "香蕉", "橙子", "西瓜"}

    // 索引遍历
    for i := 0; i < len(fruits); i++ {
        fmt.Printf("索引 %d: %s\n", i, fruits[i])
    }
}
```

#### 12.3.2.2 range 遍历

**range 遍历的语法**

```go
for i, v := range arr {
    fmt.Println(i, v)
}
```

`range` 会返回一个索引和一个值（副本）。

```go
package main

import "fmt"

func main() {

    fruits := [4]string{"苹果", "香蕉", "橙子", "西瓜"}

    // range 遍历
    for i, fruit := range fruits {
        fmt.Printf("索引 %d: %s\n", i, fruit)
    }
}
```

> `range` 返回的副本就像你复印了一份文件，你在复印件上画圈圈，原件不会有任何变化。如果你想修改原件，必须用原件的"房间钥匙"（索引）去改，不能靠复印件。

**索引遍历 vs range 遍历：选哪个？**

| 场景 | 推荐方式 |
|------|----------|
| 需要修改数组元素 | `for i := range arr` |
| 只读访问 | `for _, v := range arr` |
| 需要跳着访问（步进）| `for i := 0; i < len(arr); i += 2` |
| 需要同时知道索引和值 | `for i, v := range arr` |

```go
package main

import "fmt"

func main() {

    arr := [5]int{1, 2, 3, 4, 5}

    // 场景一：修改元素 -> 用索引遍历
    for i := range arr {
        arr[i] += 10
    }
    fmt.Println("加10后:", arr) // 加10后: [11 12 13 14 15]

    // 场景二：只读打印 -> 用 range
    for _, v := range arr {
        fmt.Printf("%d ", v) // 11 12 13 14 15
    }
    fmt.Println()

    // 场景三：跳着访问 -> 用 for 循环
    for i := 0; i < len(arr); i += 2 {
        fmt.Printf("arr[%d] = %d\n", i, arr[i]) // arr[0] = 11
    }
}
```



### 12.3.3 数组比较

**数组比较是什么？**

Go 数组支持使用 `==` 和 `!=` 进行比较。两个数组相等，当且仅当它们的**所有元素都相等**。

这就像比较两副扑克牌——如果两副牌的每张牌都完全相同（包括花色和点数），那这两副牌就是相等的；如果有任何一张牌不同，它们就不相等。

#### 12.3.3.1 可比较条件

**什么类型的数组可以比较？**

Go 语言的数组只有在**元素类型可比较**的情况下才能比较。

可比较的类型包括：

- 数值类型（int、float 系列）
- 字符串类型（string）
- 布尔类型（bool）
- 指针类型（pointer）
- 结构体（如果所有字段都可比较）
- 数组（如果元素类型可比较）

不可比较的类型包括：

- 切片（slice）
- 映射（map）
- 函数（func）
- 接口（interface）

```go
package main

import "fmt"

func main() {

    // 可比较的数组
    arr1 := [3]int{1, 2, 3}
    arr2 := [3]int{1, 2, 3}
    arr3 := [3]int{1, 2, 4}

    fmt.Println("arr1 == arr2:", arr1 == arr2) // arr1 == arr2: true
    fmt.Println("arr1 == arr3:", arr1 == arr3) // arr1 == arr3: false

    // 字符串数组可比较
    strArr1 := [2]string{"hello", "world"}
    strArr2 := [2]string{"hello", "world"}
    strArr3 := [2]string{"hello", "go"}
    fmt.Println("strArr1 == strArr2:", strArr1 == strArr2) // strArr1 == strArr2: true
    fmt.Println("strArr1 == strArr3:", strArr1 == strArr3) // strArr1 == strArr3: false
}
```

**不可比较的数组**

如果数组元素是切片、map 等不可比较的类型，编译就会报错：

```go
package main

import "fmt"

func main() {

    // 切片不可比较，所以包含切片的数组也不可比较
    // sliceArr := [2][]int{{1, 2}, {3, 4}}
    // fmt.Println(sliceArr) // 编译错误：invalid operation: sliceArr == sliceArr2 (cannot compare slice)

    // map 也不可比较
    // mapArr := [2]map[string]int{}
    // fmt.Println(mapArr) // 编译错误
}
```

> 数组比较就像你查账——会计会逐行核对两本账本，如果每一行都相同，那就是"账目相符"；如果有任何一行不同，那就是"账目不符"。Go 语言的数组比较就是这个原理——逐元素比较，只有完全相同才相等。

#### 12.3.3.2 比较语义

**比较语义详解**

Go 数组的比较是**逐元素比较**，并且是**深度比较**——对于嵌套的数组或结构体，会递归比较到最底层。

```go
package main

import "fmt"

func main() {

    // 基本类型数组比较
    arr1 := [3]int{1, 2, 3}
    arr2 := [3]int{1, 2, 3}
    arr3 := [3]int{1, 2, 4}

    fmt.Println("arr1 == arr2:", arr1 == arr2) // true
    fmt.Println("arr1 == arr3:", arr1 == arr3) // false

    // 嵌套数组比较
    nested1 := [2][2]int{{1, 2}, {3, 4}}
    nested2 := [2][2]int{{1, 2}, {3, 4}}
    nested3 := [2][2]int{{1, 2}, {3, 5}}

    fmt.Println("nested1 == nested2:", nested1 == nested2) // true
    fmt.Println("nested1 == nested3:", nested1 == nested3) // false（第二行的第二个元素不同）

    // 字符串数组比较（按字典顺序）
    strArr1 := [3]string{"apple", "banana", "cherry"}
    strArr2 := [3]string{"apple", "banana", "cherry"}
    strArr3 := [3]string{"apple", "banana", "date"}

    fmt.Println("strArr1 == strArr2:", strArr1 == strArr2) // true
    fmt.Println("strArr1 == strArr3:", strArr1 == strArr3) // false
}
```

**比较的注意事项**

1. **长度必须相同**才能比较——`[3]int` 和 `[5]int` 是不同类型，不能比较

```go
package main

import "fmt"

func main() {

    arr3 := [3]int{1, 2, 3}
    arr5 := [5]int{1, 2, 3, 4, 5}

    // arr3 == arr5 // 编译错误！不同类型不能比较
}
```

2. **数组比较不能用 `<` 或 `>`**，只能用 `==` 和 `!=`

```go
package main

import "fmt"

func main() {

    arr1 := [3]int{1, 2, 3}
    arr2 := [3]int{4, 5, 6}

    // arr1 < arr2 // 编译错误！invalid operation: arr1 < arr2 (cannot compare [3]int)
    fmt.Println("arr1 != arr2:", arr1 != arr2) // true
}
```

3. **数组比较比遍历比较更快**——因为是编译器优化的直接比较，而不是循环

```go
package main

import "fmt"

func main() {

    // 用 == 比较（推荐）
    arr1 := [1000000]int{}
    arr2 := [1000000]int{}

    for i := 0; i < 1000000; i++ {
        arr1[i] = i
        arr2[i] = i
    }

    // 直接用 == 比较（Go 编译器会优化为单次内存比较）
    fmt.Println("arr1 == arr2:", arr1 == arr2) // true
}
```

> 比较语义就像你核对两副扑克牌。你不用一张一张翻着比，而是把它们背靠背摆在一起——如果两副牌完全相同，它们就会严丝合缝；只要有任何一张牌不同，就会有缝隙。Go 的数组比较就是这个原理——编译器会把"逐元素比较"优化为"一次内存比较"，非常快。



## 12.4 多维数组

### 12.4.1 二维数组

**二维数组是什么？**

二维数组是"数组的数组"——它的每个元素本身也是一个数组。你可以把它想象成一张表格（矩阵），有行有列。

这就像你家的停车场——每一层（第一维）有多个车位（第二维），整个停车场（整体）有很多层。

**二维数组的定义**

```go
var 数组名 [行数][列数]元素类型
```

```go
package main

import "fmt"

func main() {

    // 定义一个 2 行 3 列的整型二维数组
    var matrix [2][3]int

    // 给元素赋值
    matrix[0][0] = 1
    matrix[0][1] = 2
    matrix[0][2] = 3
    matrix[1][0] = 4
    matrix[1][1] = 5
    matrix[1][2] = 6

    fmt.Println("matrix:", matrix) // matrix: [[1 2 3] [4 5 6]]
}
```

**二维数组的初始化**

```go
package main

import "fmt"

func main() {

    // 方式一：声明后逐个赋值
    var arr1 [2][3]int
    arr1[0][0] = 1
    arr1[0][1] = 2
    arr1[1][2] = 6

    // 方式二：声明时初始化
    arr2 := [2][3]int{
        {1, 2, 3},
        {4, 5, 6},
    }
    fmt.Println("arr2:", arr2) // arr2: [[1 2 3] [4 5 6]]

    // 方式三：部分初始化
    arr3 := [2][3]int{
        {1, 2},          // 第一行：1, 2, 0（未初始化的为 0）
        {4, 5, 6},       // 第二行：4, 5, 6
    }
    fmt.Println("arr3:", arr3) // arr3: [[1 2 0] [4 5 6]]

    // 方式四：只初始化部分行
    arr4 := [2][3]int{
        {1, 2, 3}, // 第一行完整
        // 第二行未初始化，默认为全 0
    }
    fmt.Println("arr4:", arr4) // arr4: [[1 2 3] [0 0 0]]
}
```

**二维数组的访问**

```go
package main

import "fmt"

func main() {

    arr := [2][3]int{
        {1, 2, 3},
        {4, 5, 6},
    }

    // 访问单个元素
    fmt.Println("第一行第一列:", arr[0][0]) // 第一行第一列: 1
    fmt.Println("第二行第三列:", arr[1][2]) // 第二行第三列: 6

    // 访问整行
    fmt.Println("第一行:", arr[0]) // 第一行: [1 2 3]
    fmt.Println("第二行:", arr[1]) // 第二行: [4 5 6]

    // 遍历二维数组
    fmt.Println("=== 遍历二维数组 ===")
    for i := 0; i < 2; i++ {
        for j := 0; j < 3; j++ {
            fmt.Printf("arr[%d][%d] = %d\n", i, j, arr[i][j])
        }
    }
}
```

> 二维数组就像一张 Excel 表格——有行有列。你想找"A3"单元格，就是表格的第三行第一列（索引 [2][0]）。二维数组也是同理，第一维是"行"，第二维是"列"。



### 12.4.2 多维数组创建

**多维数组创建详解**

Go 语言支持任意维度的数组，但实际开发中最常用的是二维和三维。更高的维度会让代码变得难以理解，所以如果需要高维数据，通常会用切片代替。

**二维数组的创建**

```go
package main

import "fmt"

func main() {

    // 创建一个 3x4 的矩阵，初始化为 0
    var matrix [3][4]int
    fmt.Println("3x4 零值矩阵:", matrix)
    // 输出：
    // [[0 0 0 0]
    //  [0 0 0 0]
    //  [0 0 0 0]]

    // 创建一个 2x3x4 的三维数组
    var tensor [2][3][4]int
    tensor[0][0][0] = 100
    tensor[1][2][3] = 200
    fmt.Println("3D 数组:", tensor) // [[[100 0 0 0] [0 0 0 0] [0 0 0 0]] [[0 0 0 0] [0 0 0 0] [0 0 0 200]]]
}
```

**初始化多维数组**

```go
package main

import "fmt"

func main() {

    // 完整初始化
    arr1 := [2][3]int{
        {1, 2, 3},
        {4, 5, 6},
    }
    fmt.Println("完整初始化:", arr1)

    // 指定行初始化（其余为 0）
    arr2 := [2][3]int{
        {1, 2},          // 第一行：1, 2, 0
        {4, 5, 6},       // 第二行：4, 5, 6
    }
    fmt.Println("部分初始化:", arr2)

    // 指定索引初始化
    arr3 := [2][3]int{
        0: {100, 200, 300}, // 第 0 行：100, 200, 300
        1: {400, 500, 600}, // 第 1 行：400, 500, 600
    }
    fmt.Println("索引初始化:", arr3)

    // 嵌套初始化
    arr4 := [2][2][2]int{
        {
            {1, 2},
            {3, 4},
        },
        {
            {5, 6},
            {7, 8},
        },
    }
    fmt.Println("三维数组:", arr4)
}
```

**多维数组的值语义**

多维数组也是值语义——赋值时会拷贝整个数组。

```go
package main

import "fmt"

func main() {

    original := [2][3]int{
        {1, 2, 3},
        {4, 5, 6},
    }

    // 拷贝整个数组
    copy := original

    // 修改拷贝不影响原数组
    copy[0][0] = 999

    fmt.Println("original:", original) // original: [[1 2 3] [4 5 6]]
    fmt.Println("copy:", copy) // copy: [[999 2 3] [4 5 6]]
}
```

**创建不规则数组（锯齿数组）**

Go 的多维数组要求每一行长度相同。如果你想创建"不规则"的数组，需要用**切片**而不是数组：

```go
package main

import "fmt"

func main() {

    // 用切片创建"不规则"二维数组（每行长度不同）
    jagged := [][]int{
        {1, 2, 3},         // 3 列
        {4, 5},            // 2 列
        {6, 7, 8, 9},      // 4 列
    }
    fmt.Println("不规则数组（切片）:", jagged)

    // 注意！不能用数组创建不规则数组！
    // 下面的代码是错误的：
    // var badArr [2][3]int // 固定每行 3 列
    // badArr[0] = {1, 2} // 错误！不能给数组的行赋值
}
```

> 多维数组创建就像你规划一个小区。2D 数组是一栋每层都有相同户型的楼；3D 数组是一个由多栋楼组成的小区，每栋楼都长得一样。但如果你想要"个性化"——有的楼是 3 户型，有的楼是 5 户型——那就得用切片，因为数组的"户型"（每行长度）是固定的。



### 12.4.3 多维数组访问

**多维数组访问详解**

多维数组的访问是通过多个索引完成的。对于二维数组，用 `[行索引][列索引]` 访问；对于三维数组，用 `[层索引][行索引][列索引]` 访问。

```go
package main

import "fmt"

func main() {

    // 二维数组
    arr2D := [2][3]int{
        {1, 2, 3},
        {4, 5, 6},
    }

    // 访问单个元素
    fmt.Println("arr2D[0][0]:", arr2D[0][0]) // arr2D[0][0]: 1
    fmt.Println("arr2D[1][2]:", arr2D[1][2]) // arr2D[1][2]: 6

    // 访问整行
    fmt.Println("arr2D[0]:", arr2D[0]) // arr2D[0]: [1 2 3]
    fmt.Println("arr2D[1]:", arr2D[1]) // arr2D[1]: [4 5 6]
}
```

**遍历二维数组**

```go
package main

import "fmt"

func main() {

    matrix := [3][4]int{
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12},
    }

    // 方式一：普通 for 循环
    fmt.Println("=== 普通 for 循环 ===")
    for i := 0; i < 3; i++ {
        for j := 0; j < 4; j++ {
            fmt.Printf("%4d", matrix[i][j])
        }
        fmt.Println()
    }

    // 方式二：for range 循环
    fmt.Println("=== for range 循环 ===")
    for i, row := range matrix {
        for j, val := range row {
            fmt.Printf("%4d", val)
        }
        fmt.Println()
    }
}
```

> 多维数组访问就像你在电影院找座位。你说"第 3 排第 5 座"，售票员就知道你要的是哪一张票。`arr[2][4]` 就是"第 3 排第 5 座"——第一维是"排"（行），第二维是"座"（列）。如果你说"第 5 排第 3 座"，但电影院只有 4 排，那售票员就会告诉你"不好意思，没有第 5 排"（越界 panic）。



## 12.5 数组与切片的关系

### 12.5.1 切片基于数组

**切片基于数组是什么？**

Go 的切片（slice）是在数组的基础上构建的——切片是数组的"视图"或"窗户"，它让你能够看到数组的一部分（或全部）元素。

这就像你有一本书（数组），但你不想每次都翻整本书，只需要翻第 10 页到第 20 页。你就拿一个"书签"（切片）夹在第 10 页和第 20 页之间——这个书签不会复制一本书，它只是一个"指向这本书的引用"。

**切片 vs 数组**

```go
package main

import "fmt"

func main() {

    // 数组：完整的书
    arr := [5]int{1, 2, 3, 4, 5}
    fmt.Println("数组:", arr) // 数组: [1 2 3 4 5]

    // 切片：书的某一页或某几页
    slice := arr[0:3] // 看到第 0 到第 2 页（索引 0, 1, 2）
    fmt.Println("切片 (arr[0:3]):", slice) // 切片 (arr[0:3]): [1 2 3]
}
```

**切片的底层结构**

Go 的切片实际上是一个结构体，包含三个字段：

1. **指针**：指向底层数组的某个元素
2. **长度**：切片中元素的数量
3. **容量**：从指针位置到底层数组末尾的元素数量

```go
package main

import "fmt"

func main() {

    arr := [10]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

    // 创建切片 s1，指向 arr 的 2-5 元素
    s1 := arr[2:6]
    fmt.Printf("s1: %v, len=%d, cap=%d\n", s1, len(s1), cap(s1))
    // s1: [2 3 4 5], len=4, cap=8

    // 创建切片 s2，指向 arr 的 3-6 元素
    s2 := arr[3:7]
    fmt.Printf("s2: %v, len=%d, cap=%d\n", s2, len(s2), cap(s2))
    // s2: [3 4 5 6], len=4, cap=7
}
```

> 切片基于数组，就像窗户基于墙——没有墙（数组），窗户（切片）就没有意义。你不能在空中凭空建一个窗户，它必须依附于一面墙。切片也是，它必须依附于一个底层数组。

### 12.5.2 切片表达式

**切片表达式是什么？**

切片表达式用于从数组或切片中"切出"一部分，形成新的切片。语法是 `array[start:end]`——从索引 `start` 开始，到索引 `end-1` 结束。

语法格式：

```go
s[low:high]      // 从 low 到 high-1
s[low:]          // 从 low 到末尾
s[:high]         // 从开头到 high-1
s[:]             // 整个切片（拷贝一份新的切片，但不是拷贝底层数组）
```

```go
package main

import "fmt"

func main() {

    arr := [10]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

    // 完整切片
    s1 := arr[:]
    fmt.Println("s1 (完整):", s1) // s1 (完整): [0 1 2 3 4 5 6 7 8 9]

    // 从中间切
    s2 := arr[2:6]
    fmt.Println("s2 (arr[2:6]):", s2) // s2 (arr[2:6]): [2 3 4 5]

    // 从开头切到某个位置
    s3 := arr[:5]
    fmt.Println("s3 (arr[:5]):", s3) // s3 (arr[:5]): [0 1 2 3 4]

    // 从某个位置切到末尾
    s4 := arr[5:]
    fmt.Println("s4 (arr[5:]):", s4) // s4 (arr[5:]): [5 6 7 8 9]
}
```

**切片表达式的容量**

切片表达式的容量（capacity）是从"起始索引"到底层数组末尾的元素数量。

```go
package main

import "fmt"

func main() {

    arr := [10]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

    s := arr[2:5]
    fmt.Printf("切片: %v, len=%d, cap=%d\n", s, len(s), cap(s))
    // 切片: [2 3 4], len=3, cap=8
    // 解释：起始索引是 2，底层数组从索引 2 到末尾还有 8 个元素 (2,3,4,5,6,7,8,9)

    // 如果从索引 5 开始切，取 3 个元素
    s2 := arr[5:8]
    fmt.Printf("s2: %v, len=%d, cap=%d\n", s2, len(s2), cap(s2))
    // s2: [5 6 7], len=3, cap=5
    // 解释：起始索引是 5，底层数组从索引 5 到末尾还有 5 个元素 (5,6,7,8,9)
}
```

### 12.5.3 底层数组共享

**底层数组共享是什么？**

切片表达式不会复制底层数组，它只是创建了一个新的"视图"，指向同一个底层数组。这意味着：**多个切片可能共享同一个底层数组**，修改一个切片会影响其他切片。

```go
package main

import "fmt"

func main() {

    arr := [5]int{1, 2, 3, 4, 5}
    fmt.Println("原始数组:", arr) // 原始数组: [1 2 3 4 5]

    // 创建两个切片，共享同一个底层数组
    s1 := arr[0:3] // [1, 2, 3]
    s2 := arr[2:5] // [3, 4, 5]

    fmt.Println("s1:", s1) // s1: [1 2 3]
    fmt.Println("s2:", s2) // s2: [3 4 5]

    // 通过 s1 修改数组
    s1[2] = 100

    fmt.Println("修改 s1[2] = 100 后:")
    fmt.Println("arr:", arr)  // arr: [1 2 100 4 5]
    fmt.Println("s1:", s1)   // s1: [1 2 100]
    fmt.Println("s2:", s2)   // s2: [100 4 5]（被影响了！）
}
```

## 12.6 数组模式

### 12.6.1 数组作为常量

**数组作为常量是什么？**

Go 的数组可以用 `const` 声明为常量——但注意，数组本身不能是 `const`，数组的**元素可以是指向常量的**。

更准确地说，Go 没有"数组常量"的语法，但可以用**未命名数组**配合 `iota` 来创建"枚举常量"类型的数组。

```go
package main

import "fmt"

func main() {

    // 用 const 配合 iota 创建枚举数组
    const (
        Sunday    = iota // 0
        Monday          // 1
        Tuesday         // 2
        Wednesday       // 3
        Thursday        // 4
        Friday          // 5
        Saturday        // 6
    )

    // 数组存储星期几的名字
    dayNames := [7]string{
        Sunday:    "星期日",
        Monday:    "星期一",
        Tuesday:   "星期二",
        Wednesday: "星期三",
        Thursday:  "星期四",
        Friday:    "星期五",
        Saturday:  "星期六",
    }

    fmt.Println("今天是:", dayNames[Wednesday]) // 今天是: 星期三
}
```

**数组常量模式的经典应用：查表**

```go
package main

import "fmt"

func main() {

    // ASCII 码表（部分）
    ascii := [128]string{
        0:   "NUL",
        10:  "LF",
        13:  "CR",
        32:  "Space",
        33:  "!",
        48:  "0",
        57:  "9",
        65:  "A",
        90:  "Z",
        97:  "a",
        122: "z",
    }

    fmt.Printf("字符 65 是: %s\n", ascii[65]) // 字符 65 是: A
    fmt.Printf("字符 10 是: %s\n", ascii[10]) // 字符 10 是: LF
}
```

### 12.6.2 数组零值初始化

**数组零值初始化的应用**

利用数组的零值特性，可以很方便地实现"计数器"、"标志位"等模式：

```go
package main

import "fmt"

func main() {

    // 计数器数组：统计 0-9 每个数字出现的次数
    count := [10]int{}

    // 模拟一些数据
    data := []int{1, 3, 5, 7, 9, 1, 3, 5, 1, 7, 1, 3, 1}

    for _, n := range data {
        count[n]++ // 对应数字的计数器 +1
    }

    fmt.Println("数字统计:")
    for i := 0; i < 10; i++ {
        fmt.Printf("数字 %d: %d 次\n", i, count[i])
    }
}
```

### 12.6.3 数组拷贝优化

**数组拷贝优化的技巧**

由于数组是值语义，直接赋值会拷贝整个数组。对于大数组，这可能是性能瓶颈。以下是几种优化方法：

**方法一：使用指针传递**

```go
package main

import "fmt"

func modifyViaPointer(arr *[1000000]int) {
    // 只拷贝 8 字节的指针
    arr[0] = 999
}

func main() {

    arr := [1000000]int{}
    modifyViaPointer(&arr)
    fmt.Println("arr[0]:", arr[0]) // arr[0]: 999
}
```

**方法二：使用切片代替数组**

```go
package main

import "fmt"

func modifySlice(slice []int) {
    // 切片是引用语义，传递的是指针
    slice[0] = 999
}

func main() {

    arr := [1000000]int{}
    // 把数组转换成切片传递
    modifySlice(arr[:])
    fmt.Println("arr[0]:", arr[0]) // arr[0]: 999
}
```

**方法三：原地修改（避免返回新数组）**

```go
package main

import "fmt"

func doubleInPlace(arr *[5]int) {
    for i := range arr {
        arr[i] *= 2
    }
}

func main() {

    arr := [5]int{1, 2, 3, 4, 5}
    doubleInPlace(&arr)
    fmt.Println("翻倍后:", arr) // 翻倍后: [2 4 6 8 10]
}
```

> 数组拷贝优化就像搬家——如果你要搬一栋楼（100万个元素的数组），你肯定不会真的把楼拆了搬过去。你会让新住户直接去原地址住（指针传递），或者在同一个小区再建一栋一模一样的楼然后让新住户搬进去（原地修改）。直接"拆楼搬运"（拷贝整个数组）太费劲了。



## 12.7 数组与性能

### 12.7.1 缓存友好性

**缓存友好性是什么？**

计算机的 CPU 访问内存时，会把附近的数据一起加载到 CPU 缓存（cache）中。这意味着，如果你访问一个内存位置的数据，附近的数据也会被一起加载到缓存，下次访问时会快很多。

Go 的数组是**连续存储**的，所以访问数组的相邻元素时，CPU 缓存可以"预取"到附近的数据，速度很快。这就是数组的"缓存友好性"。

**数组 vs 链表：缓存友好性对比**

```go
package main

import "fmt"

func main() {

    // 数组：连续存储，缓存友好
    arr := [1000000]int{}
    for i := 0; i < 1000000; i++ {
        arr[i] = i
    }

    // 切片：基于数组，也是连续存储
    slice := make([]int, 1000000)
    for i := 0; i < 1000000; i++ {
        slice[i] = i
    }

    fmt.Println("数组长度:", len(arr))
    fmt.Println("切片长度:", len(slice))
    fmt.Println("两者都是连续存储，访问效率都很高")
}
```

> 缓存友好性就像你逛超市。如果你想要买的东西都在同一个货架上（数组），你只需要走一趟就能全部拿齐。但如果它们分散在超市的各个角落（链表），你就得走来走去，累死了。数组的连续存储保证了"物品都在同一个货架上"，CPU 访问起来特别快。

**什么是缓存行？**

现代 CPU 的缓存是以"缓存行"（cache line）为单位加载的，通常是 64 字节。当你访问一个数组元素时，CPU 会把该元素所在的整个缓存行（包含附近的其他元素）一起加载到缓存。

```go
package main

import "fmt"

func main() {

    // 一个缓存行通常能存 8 个 int64（8 * 8 = 64 字节）
    // 所以访问 arr[0] 时，arr[1] ~ arr[7] 可能已经被预取到缓存了

    arr := [1000]int64{}
    for i := 0; i < 1000; i++ {
        arr[i] = int64(i)
    }

    // 顺序访问：快（利用缓存预取）
    for i := 0; i < 1000; i++ {
        _ = arr[i]
    }

    // 跳着访问：慢（缓存预取失效）
    for i := 0; i < 1000; i += 100 {
        _ = arr[i]
    }
}
```

### 12.7.2 数组 vs 切片选择

**什么时候用数组？**

1. **固定长度**的场景——长度在编译时就确定，不会变
2. **值语义**的需求——需要拷贝整个数据，而不是共享引用
3. **性能敏感**的场景——数组比切片有轻微的性能优势
4. **需要比较**的场景——数组可以直接用 `==` 比较

```go
package main

import "fmt"

// 场景一：固定长度的配置
type IPv4 [4]byte

func main() {

    // IPv4 地址可以用数组表示
    localhost := IPv4{127, 0, 0, 1}
    fmt.Println("localhost:", localhost) // localhost: [127 0 0 1]
}
```

**什么时候用切片？**

1. **长度会变化**的场景——需要在运行时添加/删除元素
2. **不确定长度**的场景——长度只有运行时才知道
3. **大数组传参**——避免拷贝整个数组
4. **需要追加元素**——切片有 `append()` 函数
5. **共享数据**——切片是引用语义，多个变量可以共享同一个底层数组

```go
package main

import "fmt"

func main() {

    // 切片：长度可变
    slice := []int{1, 2, 3}
    slice = append(slice, 4, 5, 6) // 动态添加元素
    fmt.Println("切片:", slice) // 切片: [1 2 3 4 5 6]

    // 数组：长度固定，不能追加
    // arr := [3]int{1, 2, 3}
    // arr = append(arr, 4) // 错误！不能给数组 append
}
```

**数组 vs 切片对比表**

| 特性 | 数组 | 切片 |
|------|------|------|
| 长度 | 固定，编译时确定 | 可变，运行时可调整 |
| 赋值 | 值语义，拷贝整个数组 | 引用语义，共享底层数组 |
| 传参 | 拷贝整个数组（开销大）| 只拷贝切片头（开销小）|
| 比较 | 可以用 `==` | 不能用 `==`（要用 `reflect.DeepEqual`）|
| append | 不支持 | 支持（动态扩容）|
| 适用场景 | 固定长度、值语义 | 长度可变、引用语义 |

```go
package main

import "fmt"

func main() {

    // 数组：用 == 比较
    arr1 := [3]int{1, 2, 3}
    arr2 := [3]int{1, 2, 3}
    arr3 := [3]int{1, 2, 4}
    fmt.Println("arr1 == arr2:", arr1 == arr2) // true
    fmt.Println("arr1 == arr3:", arr1 == arr3) // false

    // 切片：不能用 == 比较
    s1 := []int{1, 2, 3}
    s2 := []int{1, 2, 3}
    // fmt.Println(s1 == s2) // 错误！invalid operation: s1 == s2 (slice can only be compared to nil)
}
```

> 选择数组还是切片，就像是选择买房子还是租房。买房子（数组）——你拥有完整的产权（值语义），但要一次性付清全款（拷贝开销）；租房（切片）——你只需要付押金（切片头），每月付租金（引用传递），但房子不是你的（共享底层数据）。怎么选？取决于你的需求和预算。



## 本章小结

本章我们全面深入地学习了 Go 语言的数组（Array）。数组是 Go 最基础的数据结构，虽然在实际开发中切片（Slice）用得更多，但理解数组对于理解切片和内存管理至关重要。

**核心要点回顾：**

1. **数组是固定长度的、连续存储的、同一类型的元素序列**
   - 长度是类型的一部分：`[5]int` 和 `[10]int` 是不同的类型
   - 长度必须是常量，不能是变量
   - 元素类型也是类型的一部分

2. **数组是值语义**
   - 赋值和传参都会拷贝整个数组
   - 对于大数组，这可能是性能瓶颈
   - 可以用指针传递来避免拷贝

3. **数组的创建方式**
   - 显式长度创建：`[5]int{}`
   - 推导长度创建：`[...]int{1, 2, 3}`
   - 索引初始化：`[5]int{0: 100, 4: 500}`
   - 零值初始化：`var arr [5]int`（所有元素为零值）

4. **数组的访问和遍历**
   - 通过索引访问：`arr[0]`、`arr[len-1]`
   - 越界访问会 panic
   - 支持两种遍历方式：索引遍历和 `range` 遍历
   - `range` 返回的是值的副本，修改副本不影响原数组

5. **数组可以比较**
   - 只有可比较类型的数组才能比较
   - 使用 `==` 和 `!=` 进行比较
   - 逐元素比较，深度比较

6. **多维数组**
   - 本质上是"数组的数组"
   - 二维数组：`[2][3]int`
   - 支持任意维度（但高维数组难理解，通常用切片代替）

7. **数组与切片的关系**
   - 切片基于数组，是数组的"视图"
   - 多个切片可以共享同一个底层数组
   - 修改一个切片可能影响其他切片

8. **数组与性能**
   - 数组是连续存储，缓存友好
   - 选择数组还是切片，取决于场景需求
   - 固定长度、值语义、需比较 → 用数组
   - 长度可变、引用语义、需 append → 用切片

**一句话总结：**

数组是 Go 语言的"基石"——它简单、朴素、但非常强大。切片是对数组的封装，提供了更灵活的操作。理解数组，你就能理解切片的底层原理；理解切片的底层原理，你就能更好地写出高效的 Go 代码。

**继续下一章前，先问自己几个问题：**

- `[5]int` 和 `[...]int{1,2,3,4,5}` 类型相同吗？
- 数组赋值和切片赋值有什么区别？
- 为什么切片比数组更适合做大数组传参？
- 两个共享底层数组的切片，修改一个会影响另一个吗？
- 数组越界访问会发生什么？

如果能回答上来，说明你已经掌握了 Go 数组的精髓！


