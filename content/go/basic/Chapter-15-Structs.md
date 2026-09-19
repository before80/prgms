+++
title = "第15章 结构体"
weight = 150
date = "2026-03-20T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第15章 结构体

> "数组是把同类东西装进一个盒子，结构体是把不同类东西装进一个盒子。" —— 这是结构体存在的意义。

如果说数组是把同一种类型的数据打包成一组，那结构体就是把**不同类型**的数据打包成一个整体。你可以把结构体想象成一张**表格**：每一行是一个字段（field），每行有自己的名字和类型。比如一张学生信息表，有姓名（字符串）、年龄（整数）、身高（浮点数）——这些字段类型各不相同，只有结构体能装下它们。

结构体是 Go 里最重要的自定义类型之一。很多语言里有"类（class）"的概念，Go 没有类，但用结构体 + 方法（method）可以完全实现面向对象的编程风格。所以这一章是理解 Go OOP 的基础。

---

## 15.1 结构体类型

### 15.1.1 结构体定义

用 `type` 关键字定义一个结构体类型：

```go
type Person struct {
    Name string
    Age  int
    City string
}
```

这就是定义了一个叫 `Person` 的结构体类型，它有三个字段：
- `Name`：字符串类型
- `Age`：整数类型
- `City`：字符串类型

定义完了之后，就可以像使用内置类型一样使用它：

```go
var p Person  // 声明一个 Person 类型的变量
p.Name = "Alice"
p.Age = 30
p.City = "Beijing"
fmt.Println(p)  // {Alice 30 Beijing}
```

### 15.1.2 字段声明

#### 15.1.2.1 命名字段

结构体的字段必须有一个名字（除了后面要讲的匿名/嵌入字段）。字段名是标识符，符合 Go 的命名规则。

```go
type Point struct {
    X int
    Y int
}
```

#### 15.1.2.2 字段类型

字段的类型可以是任何类型——内置类型、数组、其他结构体、map、切片、函数、通道……全都可以：

```go
type Config struct {
    Name      string
    Ports     []int          // 切片类型字段
    Meta      map[string]any // map 类型字段
    OnStart   func()         // 函数类型字段
    Done      chan struct{}  // 通道类型字段
    Inner     Point          // 其他结构体类型字段
}

cfg := Config{
    Name:    "myapp",
    Ports:   []int{80, 443},
    Meta:    map[string]any{"version": "1.0"},
    OnStart: func() { fmt.Println("Started!") },
    Done:    make(chan struct{}),
    Inner:   Point{X: 10, Y: 20},
}
```

#### 15.1.2.3 字段顺序

结构体字段的**顺序**也是类型的一部分。字段顺序不同的两个结构体类型，即使字段名和字段类型都一样，Go 也认为它们是不同的类型：

```go
// 具名类型之间永远不相等——即使字段一模一样
type A struct{ X, Y int }
type B struct{ X, Y int }
// A 和 B 是不同的类型，不能互相赋值（要转必须显式写成 A(b)）

// 字段顺序属于结构体类型本身，对匿名结构体类型也一样成立
var c struct{ X, Y int }
var d struct{ Y, X int }
// c = d  // 编译错误：cannot use d (variable of type struct{Y int; X int}) as struct{X int; Y int} value
```

这一点很重要：字段的**名字、类型和顺序**共同构成了结构体类型。顺序不同就是不同的类型，同理字段名不同、类型不同也都是不同的类型。（另外，**标签**也参与类型标识：两个字段完全一样、只有 `json` 标签不同的结构体，也是不同的类型。）

### 15.1.3 嵌入字段

这是 Go 里一个独特且强大的特性，叫**类型嵌入（type embedding）**。它允许你把一个已有的类型作为"匿名字段"嵌入到结构体里，这个字段的方法会直接"提升"到外层结构体上。

#### 15.1.3.1 类型嵌入

把一个类型名单独写在一行、不给它起字段名，这个字段就叫**匿名字段**，这种写法叫**嵌入（embedding）**。嵌入类型自己的字段和它的方法都会被**提升**到外层结构体上：

```go
type Base struct {
    Name string
}

func (b Base) Greet() {
    fmt.Println("Hello, I'm", b.Name)
}

type Derived struct {
    Base      // 嵌入 Base，Base 是匿名字段
    Age  int
}
```

从使用者的角度看，Derived 好像"继承"了 Base 的字段和方法：

```go
d := Derived{}
d.Name = "Alice"      // 直接访问 Base 的 Name 字段
d.Age = 30
d.Greet()             // 直接调用 Base 的 Greet 方法
fmt.Println(d.Base.Name) // 也可以显式访问
```

但要记住两个关键区别，否则很容易把 Go 当成 C++ 或 Java 来写：

1. **这不是继承，而是组合加语法糖。** 字段其实还在 `d.Base` 里，只是编译器允许你写 `d.Name` 来省掉中间那一层。
2. **提升的方法，接收者是内层的值。** `d.Greet()` 完全等价于 `d.Base.Greet()`——收到的是 `d.Base` 这个副本，不是 `d`。所以如果 Greet 里想读 `d.Age`，是读不到的（编译不过）。

#### 15.1.3.2 指针嵌入

嵌入的类型也可以是指针：

```go
type Base struct {
    Name string
}

type Derived struct {
    *Base  // 嵌入 Base 的指针类型
    Age    int
}

d := Derived{
    Base: &Base{Name: "Bob"},  // 传指针
    Age:  25,
}
d.Name = "Bob"       // 仍然可以直接访问
d.Base.Name = "Charlie"  // 也可以通过 Base 指针访问
```

#### 15.1.3.3 嵌入接口

嵌入接口时，接口的方法同样会被提升到外层结构体上——于是外层结构体也就满足了这个接口：

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Logger struct {
    Reader  // 嵌入接口
    Prefix string
}

// Logger 现在也有 Read 方法，所以它满足 Reader 接口
var _ Reader = Logger{}
```

⚠️ 这个特性的一个直接后果是：**即使你根本没写 Read 的实现，`Logger` 也"看起来"满足 `Reader`**。如果嵌入的 `Reader` 字段是 nil，调用 `Read` 会在运行时 panic（nil 接口调用）。所以嵌入接口适合两种场景：

- 想在自己的类型里内嵌一个已有实现，只覆写其中少数几个方法；
- 故意用嵌入接口来"占位"，强制实现者补齐方法（类似未实现方法直接 panic 的技巧）。

---

## 15.2 结构体创建

### 15.2.1 字段名初始化

#### 15.2.1.1 完整初始化

用字段名指定每个字段的值来创建结构体变量：

```go
p := Person{
    Name: "Alice",
    Age:  30,
    City: "Beijing",
}
fmt.Println(p)  // {Alice 30 Beijing}
```

#### 15.2.1.2 部分初始化

只初始化部分字段，未初始化的字段自动获得其类型的**零值**：

```go
p := Person{
    Name: "Bob",
    // Age 和 City 没写，使用零值
}
fmt.Println(p)  // {Bob 0 } // Age=0（int零值），City=""（string零值）
```

#### 15.2.1.3 字段顺序无关

用字段名初始化时，字段的顺序可以随意排列：

```go
p1 := Person{City: "Shanghai", Name: "Carol", Age: 25}
p2 := Person{Name: "Carol", Age: 25, City: "Shanghai"}
fmt.Println(p1 == p2)  // true — 内容相同
```

### 15.2.2 位置初始化

如果不写字段名，只按字段声明的顺序写值：

```go
p := Person{"Dave", 28, "Guangzhou"}
fmt.Println(p)  // {Dave 28 Guangzhou}
```

> **警告**：位置初始化是危险的做法！一旦结构体字段的顺序或数量发生变化（哪怕只是插了一个新字段），所有使用位置初始化的代码都会编译失败或者行为错误。建议只用字段名初始化。

### 15.2.3 指针创建

#### 15.2.3.1 取地址

最常用的创建结构体指针的方式：

```go
p := &Person{Name: "Eve", Age: 22, City: "Shenzhen"}
fmt.Println(p)       // &{Eve 22 Shenzhen}
fmt.Println(p.Name)   // Eve — 直接用 . 访问，指针自动解引用
```

Go 允许直接用 `.` 访问指针指向的结构体字段，不需要先解引用（`*p.Name`），编译器会自动处理。

#### 15.2.3.2 new 函数

内置函数 `new(T)` 为类型 `T` 分配零值内存并返回 `*T`：

```go
p := new(Person)  // *Person，返回指向零值 Person 的指针
p.Name = "Frank"
p.Age = 35
fmt.Println(p)  // &{Frank 35 }
```

`new(Person)` 等价于 `&Person{}`。

---

## 15.3 结构体操作

### 15.3.1 字段访问

#### 15.3.1.1 直接访问

结构体变量用点号访问字段，读和写是同一个语法：

```go
p := Person{Name: "Alice", Age: 30, City: "Beijing"}
fmt.Println(p.Name)  // Alice
fmt.Println(p.Age)   // 30
```

#### 15.3.1.2 指针访问

结构体指针不需要先写 `*` 再取字段，Go 会自动解引用——`p.Name` 和 `(*p).Name` 完全等价：

```go
p := &Person{Name: "Bob", Age: 25, City: "Shanghai"}
fmt.Println(p.Name)   // Bob — 自动解引用
fmt.Println((*p).Name) // Bob — 手动解引用，跟上面等价
```

### 15.3.2 字段提升

当结构体 A 嵌入了结构体 B，B 的字段会"提升"到 A 上，可以直接用 A 的名字访问 B 的字段，就像 A 自己有这些字段一样。

#### 15.3.2.1 提升规则

提升的查找规则很直白：沿着嵌入链由外向内逐层查找，外层先命中就返回。下面这个例子里，`Name`、`ID` 都来自内层，`Age` 来自外层：

```go
type Base struct {
    Name string
    ID   int
}

type Derived struct {
    Base
    Age int
}

d := Derived{
    Base: Base{Name: "Alice", ID: 100},
    Age:  30,
}

fmt.Println(d.Name)   // Alice — 提升字段，可以直接访问
fmt.Println(d.ID)     // 100 — 提升字段
fmt.Println(d.Base.Name) // Alice — 显式访问也可以
fmt.Println(d.Age)    // 30 — Derived 自有的字段
```

#### 15.3.2.2 命名冲突

如果 Derived 和 Base 都有同名字段怎么办？Go 规定：**外层优先**（shadowing 规则）。 Derived 自己的字段会"遮蔽" Base 的同名提升字段：

```go
type Base struct {
    Name string
}

type Derived struct {
    Base
    Name string  // Derived 有自己的 Name，跟 Base 同名
}

d := Derived{}
d.Name = "Outer"    // 访问的是 Derived 自己的 Name
d.Base.Name = "Inner" // 要访问 Base 的 Name，必须显式通过 Base
fmt.Println(d.Name)  // Outer
fmt.Println(d.Base.Name) // Inner
```

#### 15.3.2.3 指针嵌入提升

同样的提升规则也适用于指针嵌入：

```go
type Base struct {
    Name string
}

type Derived struct {
    *Base
    Name string
}

d := Derived{Base: &Base{Name: "BaseName"}, Name: "DerivedName"}
fmt.Println(d.Name)       // DerivedName — 外层优先
fmt.Println(d.Base.Name)   // BaseName — 显式访问
```

### 15.3.3 结构体比较

#### 15.3.3.1 可比较条件

如果结构体的所有字段都是**可比较类型**，这个结构体就是可比较的：

```go
type Point struct {
    X, Y int
}

p1 := Point{1, 2}
p2 := Point{1, 2}
fmt.Println(p1 == p2)  // true

// 如果包含不可比较字段（如切片、map、函数），结构体不可比较
type Person struct {
    Name  string
    Slice []int  // 切片不可比较！
}
// p1 := Person{Name: "Alice", Slice: []int{1,2}}
// p2 := Person{Name: "Alice", Slice: []int{1,2}}
// fmt.Println(p1 == p2) // 编译错误！invalid operation: p1 == p2
```

#### 15.3.3.2 比较语义

结构体的 `==` 操作会**递归比较**所有字段：

```go
type Inner struct{ A, B int }
type Outer struct{ Inner Inner; Name string }

o1 := Outer{Inner: Inner{A: 1, B: 2}, Name: "test"}
o2 := Outer{Inner: Inner{A: 1, B: 2}, Name: "test"}
fmt.Println(o1 == o2)  // true — 递归比较所有字段
```

---

## 15.4 结构体标签

### 15.4.1 标签语法

结构体标签是写在字段声明后面的一串字符串，用反引号包裹：

```go
type Person struct {
    Name string `json:"name" db:"person_name"`
    Age  int    `json:"age" db:"person_age"`
}
```

标签由多个键值对组成，格式是 `key:"value"`，多个标签用空格分隔。

### 15.4.2 标签读取

使用 `reflect` 包读取结构体标签：

```go
import "reflect"

type Person struct {
    Name string `json:"full_name" db:"name"`
    Age  int    `json:"how_old" db:"age"`
}

t := reflect.TypeOf(Person{})
field, _ := t.FieldByName("Name")
fmt.Println(field.Tag.Get("json"))  // full_name
fmt.Println(field.Tag.Get("db"))     // name
```

### 15.4.3 常见用途

结构体标签最常见的用途是配合序列化/反序列化库：

```go
import "encoding/json"

type Person struct {
    Name      string `json:"name"`            // JSON key 叫 "name"
    Age       int    `json:"age,omitempty"`   // omitempty：零值时不输出
    Password  string `json:"-"`               // 忽略此字段，不序列化
    Internal  string `json:"internal"`        // JSON key 叫 "internal"
}

p := Person{Name: "Alice", Age: 0, Password: "secret", Internal: "data"}
b, _ := json.Marshal(p)
fmt.Println(string(b))
// {"name":"Alice","internal":"data"}
// Age=0 因为 omitempty 被省略了
// Password 因为 json:"-" 被完全忽略了
```

---

## 15.5 结构体模式

### 15.5.1 构造函数模式

#### 15.5.1.1 普通构造函数

Go 没有构造函数语法，通常用一个普通函数来充当构造函数，返回一个初始化好的结构体实例（或指针）：

```go
type Config struct {
    Host string
    Port int
}

func NewConfig(host string, port int) *Config {
    return &Config{
        Host: host,
        Port: port,
    }
}

cfg := NewConfig("localhost", 8080)
fmt.Println(cfg.Host)  // localhost
```

#### 15.5.1.2 功能选项模式（Functional Options）

这是 Go 里最流行的高级构造函数模式，适合有大量可选参数、需要默认值的场景：

```go
import "time"

type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) {
        s.Port = port
    }
}

func WithTimeout(timeout time.Duration) Option {
    return func(s *Server) {
        s.Timeout = timeout
    }
}

func WithTLS(certFile, keyFile string) Option {
    return func(s *Server) {
        s.TLS = &TLSConfig{Cert: certFile, Key: keyFile}
    }
}

type Server struct {
    Host     string
    Port     int
    Timeout  time.Duration
    TLS      *TLSConfig
}

type TLSConfig struct {
    Cert, Key string
}

func NewServer(host string, options ...Option) *Server {
    s := &Server{
        Host: host,
        Port: 8080,  // 默认端口
        Timeout: 30 * time.Second,  // 默认超时
    }
    for _, opt := range options {
        opt(s)  // 应用每个选项
    }
    return s
}

// 使用示例
s1 := NewServer("localhost")  // 全部使用默认值
s2 := NewServer("localhost", WithPort(9090))  // 自定义端口
s3 := NewServer("localhost", WithPort(443), WithTLS("cert.pem", "key.pem"))  // 自定义端口和 TLS
```

功能选项模式的优势：
- 每个选项都是函数，可以写在任何地方，不用改构造函数签名
- 选项可以组合，按需启用
- 有默认值，调用方可以只关心自己需要定制的部分

### 15.5.2 不可变对象模式

Go 的 `const` 只能用于编译期常量，对结构体值无能为力。想模拟不可变对象，常用套路是：**小写字段 + 只暴露 getter + 用 `WithXXX` 返回新实例**：

```go
type Config struct {
    host    string  // 小写字段，导包不可见
    port    int
}

// NewConfig 返回值类型（不是指针），无法被调用方修改
func NewConfig(host string, port int) Config {
    return Config{host: host, port: port}
}

// 只提供 getter，不提供 setter
func (c Config) Host() string { return c.host }
func (c Config) Port() int     { return c.port }

// 提供 WithXXX 方法，返回新实例（保持原实例不变）
func (c Config) WithPort(port int) Config {
    next := c      // 值接收者拿到的是副本，改的是副本
    next.port = port
    return next
}

cfg := NewConfig("localhost", 8080)
cfg2 := cfg.WithPort(9090)  // cfg 不变，cfg2 是新实例
fmt.Println(cfg.Port())   // 8080
fmt.Println(cfg2.Port())  // 9090
```

### 15.5.3 对象池模式

用 sync.Pool 缓存频繁创建和销毁的结构体：

```go
import "sync"

type PooledBuffer struct {
    Data []byte
}

var bufferPool = sync.Pool{
    New: func() any {
        return &PooledBuffer{Data: make([]byte, 1024)}
    },
}

buf := bufferPool.Get().(*PooledBuffer)
buf.Data = append(buf.Data[:0], "hello"...)  // 复用底层数组，先截断再写
// ... 使用 buf ...

buf.Data = buf.Data[:0]   // 放回前一定要重置状态！
bufferPool.Put(buf)       // 放回池中，供下次使用
```

> ⚠️ 两个容易踩的坑：(1) 从池里取出的对象**状态是上一次留下的**，必须自己重置；(2) `sync.Pool` 里的对象随时可能被 GC 回收，**不能**把它当缓存用，也不能依赖"放进去就还在"。

---

## 15.6 结构体内存布局

### 15.6.1 字段对齐

Go 编译器会自动对结构体字段进行**内存对齐（padding）**，以确保每个字段都从合适的地址开始访问（通常是字段大小的倍数）。这由 CPU 的访问粒度决定。

```go
type A struct {
    A byte    // 1字节
    B int64   // 8字节（对齐到8字节边界，A后面会补7字节padding）
    C int32   // 4字节
}
fmt.Println(unsafe.Sizeof(A{}))  // 24 — A占1字节 + 7填充 + B占8字节 + C占4字节 + 4填充=24
```

### 15.6.2 内存填充

上面例子中，A 和 B 之间插入了 7 个字节的填充（padding），以保证 B 从 8 的倍数地址开始。这是一个重要的概念：结构体的大小不一定等于所有字段大小的和，因为有填充。

### 15.6.3 字段重排优化

通过合理安排字段顺序，可以减少内存填充，提高内存利用率：

```go
// 优化前：字段顺序不合理
type BadLayout struct {
    A byte    // 1 + 7padding
    B int64   // 8
    C byte    // 1 + 3padding
    D int32   // 4
}
// Sizeof: 24

// 优化后：按大小降序排列
type GoodLayout struct {
    B int64   // 8
    D int32   // 4
    C byte    // 1
    A byte    // 1 + 2padding
}
// Sizeof: 16
```

> 内存布局优化通常只在数据结构巨大且频繁创建时才值得做（比如用在数据库ORM、协议解析等场景）。日常业务代码，优先保证可读性。

---

## 15.7 结构体序列化

### 15.7.1 JSON 标签

#### 15.7.1.1 字段映射

用 `json` 标签指定序列化后的 key 名：

```go
type Response struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
}
```

#### 15.7.1.2 忽略字段

标签写 `json:"-"` 表示这个字段**完全跳过**序列化和反序列化；写 `omitempty` 则表示"值为零值时不输出"，注意它只是**不输出**，反序列化时照常接收：

```go
type User struct {
    Username string `json:"username"`
    Password string `json:"-"`  // 完全忽略，不序列化也不反序列化
    Token    string `json:"token,omitempty"` // 空值时不输出
}
```

#### 15.7.1.3 空值处理

不加 `omitempty` 时，零值字段会老老实实出现在 JSON 里：

```go
type Item struct {
    Name  string `json:"name"`
    Price int    `json:"price"`
}

i := Item{Name: "", Price: 0}
b, _ := json.Marshal(i)
fmt.Println(string(b))  // {"name":"","price":0} — 空值正常输出
// 加了 omitempty 后空值才会被省略
```

#### 15.7.1.4 嵌套结构

结构体字段是另一个结构体时，JSON 会自然地嵌套一层：

```go
type Inner struct{ Value int }
type Outer struct {
    Inner Inner `json:"inner"`
}

b, _ := json.Marshal(Outer{Inner: Inner{Value: 42}})
fmt.Println(string(b))  // {"inner":{"value":42}}
```

### 15.7.2 其他格式标签

#### 15.7.2.1 XML 标签

`encoding/xml` 用 `>` 表示嵌套层级：`xml:"server>host"` 意思是把 Host 放在外层 `<server>` 标签里的 `<host>` 中：

```go
type Config struct {
    Host string `xml:"server>host"`
    Port int    `xml:"server>port"`
}
```

#### 15.7.2.2 YAML 标签

YAML 不是标准库，需要引入第三方库（如 `gopkg.in/yaml.v3`），它读取的是 `yaml` 标签：

```go
type Config struct {
    Host string `yaml:"host"`
    Port int    `yaml:"port"`
}
```

#### 15.7.2.3 数据库标签

`db` 标签本身不是标准库识别的，而是 `database/sql` 生态里的库（如 `sqlx`）约定俗成的字段名映射方式：

```go
type User struct {
    ID   int    `db:"id"`
    Name string `db:"name"`
    Age  int    `db:"age"`
}
```

---

## 15.8 结构体与面向对象

### 15.8.1 封装实现

Go 通过**首字母大写 = 导出，首字母小写 = 不导出**的规则来实现封装。结构体的字段如果小写，就只能在本包内访问：

```go
// 同一个包内可以访问小写字段
type Counter struct {
    count int  // 小写，包外不可见
}

func (c *Counter) Inc() {
    c.count++  // 包内可以修改
}
```

### 15.8.2 继承模拟

Go 没有继承，但可以通过**嵌入**来模拟"继承"的效果：

```go
type Animal struct {
    Name string
}

func (a Animal) Speak() {
    fmt.Println("...")
}

type Dog struct {
    Animal  // 嵌入，等于"继承"了 Animal 的字段和方法
    Breed string
}

func (d Dog) Speak() {  // 覆盖（遮蔽）Animal 的提升方法
    fmt.Println("Woof!")
}

dog := Dog{}
dog.Name = "Buddy"  // 提升字段
dog.Speak()          // Woof! — 命中外层的 Dog.Speak，Animal.Speak 被遮蔽
dog.Animal.Speak()   // ...   — 想调内层的，必须显式写出来
```

⚠️ 这不是虚函数重写。Go 的方法调用是**编译期静态确定**的，没有虚函数表，也不会在运行时"按实际类型分发"。看下面这段：

```go
type Animal struct{ Name string }

func (a Animal) Speak() { fmt.Println("...") }

func (a Animal) Describe() {
    fmt.Print("I am ", a.Name, " and I say ")
    a.Speak()   // 这里的 a 静态类型是 Animal，永远调用 Animal.Speak
}

type Dog struct{ Animal }

func (d Dog) Speak() { fmt.Println("Woof!") }

d := Dog{Animal{Name: "Buddy"}}
d.Describe()   // 输出：I am Buddy and I say ...   ← 不是 Woof!
```

想得到真正的多态，必须走接口（见下一节）。

### 15.8.3 多态实现

Go 用**接口**来实现多态——一个接口类型的变量可以持有任何实现了该接口的结构体：

```go
type Speaker interface {
    Speak()
}

func MakeItSpeak(s Speaker) {
    s.Speak()
}

type Cat struct{}
func (c Cat) Speak() { fmt.Println("Meow!") }

type Dog struct{}
func (d Dog) Speak() { fmt.Println("Woof!") }

MakeItSpeak(Cat{})  // Meow!
MakeItSpeak(Dog{})  // Woof!
```

---

## 15.9 结构体与 JSON/XML

### 15.9.1 序列化规则

Go 的 `encoding/json` 包在序列化结构体时：
- 只序列化**导出字段**（首字母大写）
- 用字段名作为 JSON key（除非有 `json` 标签）
- 值为零值的字段默认输出（加 `omitempty` 则省略）

```go
import (
    "encoding/json"
    "fmt"
)

// 有无 omitempty 的对比示例
type Person struct {
    Name string `json:"full_name"`
    Age  int    `json:"age"`            // 无 omitempty，零值照常输出
}

type PersonWithOmit struct {
    Name string `json:"full_name"`
    Age  int    `json:"age,omitempty"`  // 有 omitempty，零值被省略
}

p1 := Person{Name: "Alice", Age: 0}
p2 := PersonWithOmit{Name: "Alice", Age: 0}

b1, _ := json.Marshal(p1)
b2, _ := json.Marshal(p2)

fmt.Println(string(b1))  // {"full_name":"Alice","age":0}
fmt.Println(string(b2))  // {"full_name":"Alice"}
// 有无 omitempty 的区别：一目了然
```

### 15.9.2 自定义序列化

通过实现 `MarshalJSON` 和 `UnmarshalJSON` 方法自定义序列化行为：

```go
import (
    "encoding/json"
    "fmt"
)

type IP [4]byte

func (ip IP) MarshalJSON() ([]byte, error) {
    return json.Marshal(fmt.Sprintf("%d.%d.%d.%d", ip[0], ip[1], ip[2], ip[3]))
}

func (ip *IP) UnmarshalJSON(data []byte) error {
    var s string
    if err := json.Unmarshal(data, &s); err != nil {
        return err
    }
    _, err := fmt.Sscanf(s, "%d.%d.%d.%d", &ip[0], &ip[1], &ip[2], &ip[3])
    return err
}
```

### 15.9.3 未知字段处理

反序列化 JSON 时，结构体里没有对应字段的键会被**静默丢弃**——拼错的字段名不会报错，只会悄悄变成零值。这是线上事故的常见来源。想发现它们有两种办法：

```go
import (
    "encoding/json"
    "fmt"
    "strings"
)

type Result struct {
    Known string `json:"known"`
}

data := []byte(`{"known":"ok","extra":42}`)

// 办法一：先解到 map，再和结构体的字段对照
var m map[string]json.RawMessage
_ = json.Unmarshal(data, &m)
var r Result
_ = json.Unmarshal(data, &r)
fmt.Println(r.Known)     // ok
fmt.Println(string(m["extra"]))  // 42 —— 结构体里没有字段接住它

// 办法二：开严格模式，遇到未知字段直接报错
dec := json.NewDecoder(strings.NewReader(`{"known":"ok","extra":42}`))
dec.DisallowUnknownFields()
var r2 Result
err := dec.Decode(&r2)
fmt.Println(err)  // json: unknown field "extra"
```

> `DisallowUnknownFields` 的代价是接口不能向后兼容地加字段，所以更适合内部服务之间的协议解析，用在前端传来的 JSON 上要慎重。

---

## 15.10 结构体与数据库

### 15.10.1 ORM 映射

使用 GORM 等 ORM 库时，结构体直接映射到数据库表：

```go
import "gorm.io/gorm"

type User struct {
    ID        uint      `gorm:"primaryKey"`
    Name      string    `gorm:"size:255;not null"`
    Email     string    `gorm:"uniqueIndex;size:255"`
    Age       int       `gorm:"default:0"`
    CreatedAt time.Time
    UpdatedAt time.Time
}

// GORM 会自动创建表
// db.AutoMigrate(&User{})
```

### 15.10.2 标签配置

常用的 GORM 标签：

```go
type Product struct {
    ID        uint    `gorm:"primaryKey"`
    Name      string  `gorm:"column:name;size:100;not null"`
    Price     float64 `gorm:"type:decimal(10,2)"`
    CategoryID uint    `gorm:"index"`
}
```

### 15.10.3 关系映射

GORM 用结构体字段来表达表之间的关系。下面是最常见的两种：`belongs to`（子表持有外键）和 `has many`（子表反向持有外键）：

```go
type Order struct {
    ID     uint `gorm:"primaryKey"`
    UserID uint `gorm:"index"`
    // belongs to：外键 UserID 就在本表上
    User User `gorm:"foreignKey:UserID"`
}

type Company struct {
    ID   uint   `gorm:"primaryKey"`
    Name string
    // has many：外键 CompanyID 在 Employee 表上
    Employees []Employee `gorm:"foreignKey:CompanyID"`
}
```

> 别把 `belongs to` 叫成"一对一"：`Order` 持有 `User` 只是"这个订单属于某个用户"，一个用户可以有多个订单。

---

## 本章小结

结构体是 Go 语言里组织异构数据的基本方式，它把不同类型的命名字段打包成一个整体。相比数组（同类数据集合），结构体更像一张表格——每行一个字段，每行有自己的名字和类型。

**核心知识点：**

1. **定义与字段**：用 `type T struct { ... }` 定义结构体。字段有名字和类型，顺序是类型签名的一部分。字段类型可以是任何类型。

2. **创建方式**：字段名初始化（最推荐，`Person{Name: "Alice", Age: 30}`）、位置初始化（危险，不推荐）、`&Person{}`（指针创建）、`new(Person)`（返回零值指针）。

3. **类型嵌入**：把已有类型作为匿名字段嵌入，它的字段和方法会被**提升**到外层结构体上。但这是组合加语法糖，不是继承：提升方法的接收者是内层的那个值，Go 也没有虚函数，多态必须靠接口。

4. **字段访问**：结构体变量用 `.` 访问字段，指针变量也用 `.`（编译器自动解引用）。嵌入字段可以直接访问（提升）。

5. **结构体比较**：如果所有字段都是可比较类型，结构体可以用 `==` 比较。比较会递归比较所有字段。

6. **结构体标签**：写在字段声明后的反引号字符串，用于元数据（JSON序列化、ORM映射、反射读取等）。常见 `json:"name"`、`db:"column_name"`、`omitempty`、`-`（忽略）。

7. **构造函数模式**：Go 没有构造函数，用普通函数模拟。功能选项模式（Functional Options）是最优雅的方案，适合大量可选参数的场景。

8. **内存布局**：Go 编译器会自动做字段对齐和填充。按字段大小降序排列可以减少内存浪费，但通常不值得牺牲可读性来手动优化。

9. **序列化**：结构体序列化时只有导出字段（首字母大写）会被处理。可以通过实现 `MarshalJSON`/`UnmarshalJSON` 自定义序列化行为。

10. **OOP 模拟**：Go 用结构体+方法+接口模拟面向对象。封装靠首字母大/小写，控制导出。继承靠嵌入模拟。重写靠同名方法遮蔽。接口实现是隐式的，满足即实现。

11. **不可变对象**：通过返回非指针值、提供 `WithXXX` 方法返回新实例来模拟不可变性。
