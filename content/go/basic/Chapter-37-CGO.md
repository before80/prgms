+++
title = "第37章 CGO"
weight = 370
date = "2026-03-23T08:39:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第37章 CGO

## 37.1 CGO 基础

> 🔗 **CGO** 是 Go 语言调用 C 代码的桥梁。如果说 Go 是一门现代化的、安全的、并发友好的编程语言，那么 C 就是那个"老前辈"——几十年的积累，无数的经典库，遍布全球的代码遗产。CGO 让你能够直接调用这些 C 代码，把 Go 的安全性和 C 的灵活性结合起来。

CGO 的核心思想其实很简单：**在 Go 代码中嵌入 C 代码**。这听起来有点疯狂，但 Go 团队设计了一套非常巧妙的机制来实现它。

### 37.1.1 import "C"

在 Go 中使用 CGO 的方式是使用一个"伪包"——`C` 包。你只需要在文件顶部添加一个 `import "C"` 语句，然后紧跟着写 C 代码注释：

```go
package main

/*
#include <stdio.h>
#include <stdlib.h>

// 这是一个简单的 C 函数
int add(int a, int b) {
    return a + b;
}
*/
import "C"

import "fmt"

func main() {
    // 调用 C 函数，就像调用 Go 函数一样简单！
    result := C.add(2, 3)
    fmt.Printf("C.add(2, 3) = %d\n", result) // 5
}
```

**运行这个程序**：

```bash
go run main.go
```

你会看到输出：`C.add(2, 3) = 5`

### 37.1.2 注释中的 C 代码

CGO 的特殊之处在于：你可以在 Go 源文件的注释中写 C 代码！这些 C 代码会被 Go 编译器"识别"并编译。

```go
package main

/*
#include <stdio.h>

// 打印一条消息
void sayHello() {
    printf("Hello from C!\n");
}

// 返回一个整数
int getNumber() {
    return 42;
}

// 操作一个数组
int sumArray(int* arr, int len) {
    int total = 0;
    for (int i = 0; i < len; i++) {
        total += arr[i];
    }
    return total;
}
*/
import "C"

import "fmt"

func main() {
    fmt.Println("=== CGO 基础示例 ===")

    // 调用 C 函数
    C.sayHello()

    // 获取 C 返回的值
    num := C.getNumber()
    fmt.Printf("从 C 获取的数字: %d\n", num) // 42

    // 操作数组
    // 创建 C 数组需要特殊处理
    arr := []C.int{1, 2, 3, 4, 5}
    result := C.sumArray(&arr[0], C.int(len(arr)))
    fmt.Printf("数组元素之和: %d\n", result) // 15
}
```

> 📝 **关键点**：在 Go 中，`[]C.int` 创建一个 Go 切片，但 `C.sumArray` 需要一个 C 数组指针。我们通过 `&arr[0]` 获取首元素地址来传递给 C 函数。

### 37.1.3 #cgo 指令

有时候你需要告诉 Go 编译器一些额外的信息，比如 C 代码需要的编译标志、链接库、平台差异等。这就是 `#cgo` 指令的用武之地。

```go
package main

/*
#cgo CFLAGS: -O3 -Wall
#cgo LDFLAGS: -lm

#include <math.h>
#include <stdio.h>

// 计算立方根
double cubeRoot(double x) {
    return cbrt(x);
}

// 计算阶乘
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
*/
import "C"

import "fmt"

func main() {
    fmt.Println("=== #cgo 指令示例 ===")

    // 使用 C 的数学函数
    x := 27.0
    result := C.cubeRoot(x)
    fmt.Printf("立方根(%.0f) = %.2f\n", x, result)

    // 使用 C 的阶乘函数
    n := 10
    fact := C.factorial(C.int(n))
    fmt.Printf("%d! = %d\n", n, fact)
}
```

**#cgo 指令的常用选项**：

| 指令 | 说明 | 示例 |
|------|------|------|
| CFLAGS | C 编译器标志 | `#cgo CFLAGS: -O3 -Wall` |
| LDFLAGS | 链接器标志 | `#cgo LDFLAGS: -lm` |
| pkg-config | 使用 pkg-config | `#cgo pkg-config: gtk+-3.0` |
| GOOS/GOARCH | 平台限定 | `#cgo GOOS: windows LDFLAGS: -lws2_32` |

---

## 37.2 类型映射

> 🔄 当 Go 和 C 互相调用时，数据类型需要"翻译"。Go 的 `int` 不等于 C 的 `int`，Go 的 `string` 在 C 中根本不存在！这一节我们就来看看类型之间如何映射。

### 37.2.1 基本类型映射

Go 和 C 之间有一套固定的基本类型映射规则：

| Go 类型 | C 类型 | 说明 |
|---------|--------|------|
| bool | bool | 注意：C 的 bool 是 1 字节，Go 的 bool 也是 1 字节 |
| byte | uint8 | 完全等价 |
| int8 | int8 / char | 取决于平台 |
| int16 | int16 / short | 完全等价 |
| int32 | int32 / int | 完全等价 |
| int64 | int64 / long long | 完全等价 |
| uint8 | uint8 / unsigned char | 完全等价 |
| uint16 | uint16 / unsigned short | 完全等价 |
| uint32 | uint32 / unsigned int | 完全等价 |
| uint64 | uint64 / unsigned long long | 完全等价 |
| float32 | float | 完全等价 |
| float64 | double | 完全等价 |
| complex64 | 不支持 | C 没有复数类型 |
| complex128 | 不支持 | C 没有复数类型 |

```go
package main

/*
#include <stdio.h>
#include <stdint.h>

void printTypes() {
    printf("C types:\n");
    printf("  bool: %zu bytes\n", sizeof(_Bool));
    printf("  int: %zu bytes\n", sizeof(int));
    printf("  long: %zu bytes\n", sizeof(long));
    printf("  long long: %zu bytes\n", sizeof(long long));
    printf("  float: %zu bytes\n", sizeof(float));
    printf("  double: %zu bytes\n", sizeof(double));
    printf("  int8_t: %zu bytes\n", sizeof(int8_t));
    printf("  int64_t: %zu bytes\n", sizeof(int64_t));
}
*/
import "C"
import "unsafe"

func main() {
    C.printTypes()

    fmt.Println("\nGo types:")
    fmt.Printf("  bool: %d bytes\n", unsafe.Sizeof(bool(false))) // 1
    fmt.Printf("  int: %d bytes\n", unsafe.Sizeof(int(0))) // 8 (64位系统)
    fmt.Printf("  int32: %d bytes\n", unsafe.Sizeof(int32(0))) // 4
    fmt.Printf("  int64: %d bytes\n", unsafe.Sizeof(int64(0))) // 8
    fmt.Printf("  float32: %d bytes\n", unsafe.Sizeof(float32(0))) // 4
    fmt.Printf("  float64: %d bytes\n", unsafe.Sizeof(float64(0))) // 8
}
```

### 37.2.2 字符串转换

字符串是跨语言交互中最麻烦的部分之一。Go 的 `string` 是 immutable 的切片，而 C 的字符串是 null 结尾的字符数组。

```go
package main

/*
#include <stdio.h>
#include <string.h>

// 接收 C 字符串并返回长度
int strLen(const char* s) {
    return strlen(s);
}

// 接收 C 字符串并转换为大写（原地修改）
void toUpperCase(char* s) {
    while (*s) {
        if (*s >= 'a' && *s <= 'z') {
            *s = *s - ('a' - 'A');
        }
        s++;
    }
}
*/
import "C"
import (
    "fmt"
    "reflect"
    "unsafe"
)

func main() {
    fmt.Println("=== 字符串转换 ===")

    // Go 字符串转 C 字符串
    goStr := "Hello, 世界!"
    fmt.Printf("Go 字符串: %q\n", goStr)

    // 方法：使用 C.CString
    // C.CString 会分配一块 C 内存并复制字符串内容
    cStr := C.CString(goStr)
    defer C.free(unsafe.Pointer(cStr)) // 重要：记得释放内存！

    // 调用 C 函数
    length := C.strLen(cStr)
    fmt.Printf("C 字符串长度: %d\n", length)

    // 在 C 中修改字符串
    C.toUpperCase(cStr)
    // 现在 cStr 指向的是 "HELLO, 世界!"（注意：中文不受影响）

    // 如果想转回 Go 字符串，需要复制内容
    // 因为 Go 字符串是 immutable 的，不能直接引用 C 的内存
    goStrUpper := C.GoString(cStr)
    fmt.Printf("转回 Go 字符串: %q\n", goStrUpper)
}
```

**字符串转换的关键函数**：

| 函数 | 说明 |
|------|------|
| `C.CString(goStr)` | Go string → C *char，需要手动 `C.free` 释放 |
| `C.GoString(cStr)` | C *char → Go string（复制内容） |
| `C.GoStringN(cStr, n)` | C *char → Go string，指定长度（复制内容） |
| `C.CBytes(goSlice)` | Go []byte → C []byte（复制内容） |

### 37.2.3 指针转换

指针转换是 CGO 中最复杂的部分之一。Go 的指针不能直接传给 C，但 `unsafe.Pointer` 可以作为桥梁。

```go
package main

/*
#include <stdio.h>

void accessMemory(int* p) {
    printf("C sees value: %d\n", *p);
    *p = 999; // 修改值
}
*/
import "C"
import (
    "fmt"
    "unsafe"
)

func main() {
    fmt.Println("=== 指针转换 ===")

    // Go 变量
    value := 42
    fmt.Printf("Go 变量值: %d\n", value) // 42

    // 获取变量地址
    goPtr := &value

    // 转换为 C 接受的指针类型
    // 注意：这里必须使用 unsafe.Pointer 作为中间转换
    cPtr := (*C.int)(unsafe.Pointer(goPtr))

    // 调用 C 函数
    C.accessMemory(cPtr)

    // C 函数修改了值，看看 Go 这边是否受影响
    fmt.Printf("C 函数修改后，Go 变量值: %d\n", value) // 999
    fmt.Printf("C 函数修改后，Go 变量值: %d\n", value)
    // 输出: 999！说明 C 和 Go 共享同一块内存
}
```

> ⚠️ **警告**：上面的例子展示了 CGO 指针转换的能力，但也很危险。Go 的 GC 不理解 C 指针，如果 C 代码持有 Go 的内存指针，可能导致 GC 混乱或崩溃。上面的例子能 work 是因为 `goPtr` 是栈变量，函数返回后仍然有效。在实际代码中要谨慎使用。

---

## 37.3 函数调用

> 📞 这一节我们来详细看看如何在 Go 和 C 之间互相调用函数。

### 37.3.1 C 函数调用

从 Go 调用 C 函数是最常见的场景：

```go
package main

/*
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
    char name[32];
    double salary;
} Employee;

// 创建员工
Employee* createEmployee(int id, const char* name, double salary) {
    Employee* emp = (Employee*)malloc(sizeof(Employee));
    emp->id = id;
    strncpy(emp->name, name, 31);
    emp->name[31] = '\0'; // 确保 null 结尾
    emp->salary = salary;
    return emp;
}

// 打印员工信息
void printEmployee(Employee* emp) {
    printf("ID: %d, Name: %s, Salary: %.2f\n",
           emp->id, emp->name, emp->salary);
}

// 调整薪资
void raiseSalary(Employee* emp, double raise) {
    emp->salary += raise;
}

// 释放员工内存
void freeEmployee(Employee* emp) {
    free(emp);
}
*/
import "C"
import (
    "fmt"
    "unsafe"
)

func main() {
    fmt.Println("=== 调用 C 函数 ===")

    // 创建员工
    emp := C.createEmployee(1, C.CString("张三"), 10000.0)
    defer C.freeEmployee(emp)

    // 打印员工信息
    C.printEmployee(emp) // 输出: ID: 1, Name: 张三, Salary: 10000.00

    // 调整薪资
    C.raiseSalary(emp, 2000.0)
    fmt.Println("涨薪 2000 后：")
    C.printEmployee(emp) // 输出: ID: 1, Name: 张三, Salary: 12000.00
}
```

### 37.3.2 Go 函数回调

有时候 C 代码需要调用我们写的 Go 函数。这就是"回调"。CGO 通过**导出 Go 函数**来实现这一点。

```go
package main

/*
#include <stdio.h>

// 这个函数会调用我们传入的回调函数
void processWithCallback(void (*callback)(int)) {
    for (int i = 0; i < 5; i++) {
        callback(i); // 调用回调，传入 0-4
    }
}

// 这个函数接受一个数据和一个处理函数
typedef void (*Handler)(int, int);

void processData(int* data, int len, Handler handler) {
    for (int i = 0; i < len; i++) {
        handler(i, data[i]); // 调用处理器，传入索引和值
    }
}
*/
import "C"
import (
    "fmt"
)

//export onNumber
func onNumber(n C.int) {
    fmt.Printf("回调收到: %d\n", n)
}

//export onData
func onData(idx, val C.int) {
    fmt.Printf("数据[%d] = %d\n", idx, val)
}

func main() {
    fmt.Println("=== Go 函数回调 ===")

    // 传递 Go 函数作为回调
    // 注意：Go 函数必须是导出（首字母大写）的
    C.processWithCallback(C.onNumber)

    fmt.Println("\n处理数据：")
    data := []C.int{10, 20, 30, 40, 50}
    C.processData(&data[0], C.int(len(data)), C.onData)
}
```

> 📝 **重要**：`//export` 注释告诉 Go 编译器这个函数是要导出给 C 用的。被导出的函数必须是 Go 函数，且签名必须与 C 期望的回调类型匹配。

---

## 37.4 内存管理

> 💾 内存管理是 CGO 中最容易出 bug 的地方。Go 有 GC，而 C 需要手动管理。混用这两种内存管理方式，如果不谨慎，就会导致内存泄漏或崩溃。

### 37.4.1 C 内存分配

在 C 中分配内存要用 `malloc`，释放要用 `free`。CGO 提供了 `C.malloc` 和 `C.free`：

```go
package main

/*
#include <stdio.h>
#include <stdlib.h>

void* allocate_int_array(int size) {
    return malloc(size * sizeof(int));
}

void free_array(void* ptr) {
    free(ptr);
}
*/
import "C"
import (
    "fmt"
    "unsafe"
)

func main() {
    fmt.Println("=== C 内存分配 ===")

    size := 10

    // 分配 C 内存
    cArray := C.allocate_int_array(C.int(size))
    defer C.free_array(cArray)

    // 将 C 指针转换为 Go 切片进行操作
    // 注意：这里只是"视图"，不复制数据
    goSlice := (*[10]C.int)(cArray)[:size:size]

    // 初始化数组
    for i := 0; i < size; i++ {
        goSlice[i] = C.int(i * i)
    }

    // 打印
    fmt.Printf("数组: %v\n", goSlice) // [0 1 4 9 16 25 36 49 64 81]

    // 修改
    goSlice[5] = 100
    fmt.Printf("修改后[5] = %d\n", goSlice[5]) // 100
    fmt.Printf("修改后[5] = %d\n", goSlice[5])
}
```

### 37.4.2 内存释放责任

**关键原则**：谁分配，谁释放！

```go
package main

/*
#include <stdlib.h>
#include <string.h>

char* create_greeting(const char* name) {
    char* greeting = (char*)malloc(100);
    strcpy(greeting, "Hello, ");
    strcat(greeting, name);
    strcat(greeting, "!");
    return greeting;
}

void free_greeting(char* g) {
    free(g);
}
*/
import "C"
import (
    "fmt"
    "unsafe"
)

func main() {
    fmt.Println("=== 内存释放责任 ===")

    // C 分配了内存，返回给 Go
    cGreeting := C.create_greeting(C.CString("张三"))
    defer C.free_greeting(cGreeting) // Go 负责释放！

    // 转换为 Go 字符串
    goGreeting := C.GoString(cGreeting)
    fmt.Printf("问候语: %s\n", goGreeting)
}
```

> ⚠️ **警告**：如果忘记 `defer C.free`，就会发生**内存泄漏**！C 分配的内存不在 Go GC 的管理范围内，Go 的 GC 不会帮你回收。

---

## 37.5 CGO 模式

> 🎯 这一节来看看 CGO 的几种常见使用模式。

### 37.5.1 包装 C 库

最常见的 CGO 用法：包装一个现有的 C 库，让它能在 Go 中使用。

```go
package cjson

/*
#include "cJSON.h"
#include <stdlib.h>
#include <string.h>

// 封装 cJSON_CreateObject
cJSON* go_cJSON_CreateObject() {
    return cJSON_CreateObject();
}

// 封装 cJSON_AddStringToObject
void go_cJSON_AddStringToObject(cJSON* object, const char* key, const char* value) {
    cJSON_AddStringToObject(object, key, value);
}

// 封装 cJSON_AddNumberToObject
void go_cJSON_AddNumberToObject(cJSON* object, const char* key, double value) {
    cJSON_AddNumberToObject(object, key, value);
}

// 封装 cJSON_Print（注意：返回的字符串需要手动释放）
char* go_cJSON_Print(cJSON* object) {
    return cJSON_Print(object);
}

// 封装 cJSON_Delete
void go_cJSON_Delete(cJSON* object) {
    cJSON_Delete(object);
}
*/
import "C"
import (
    "fmt"
    "unsafe"
)

// JSONObject 代表一个 JSON 对象
type JSONObject struct {
    ptr *C.cJSON
}

// CreateObject 创建一个空的 JSON 对象
func CreateObject() *JSONObject {
    return &JSONObject{ptr: C.go_cJSON_CreateObject()}
}

// AddString 添加字符串字段
func (obj *JSONObject) AddString(key, value string) {
    C.go_cJSON_AddStringToObject(obj.ptr, C.CString(key), C.CString(value))
}

// AddNumber 添加数字字段
func (obj *JSONObject) AddNumber(key string, value float64) {
    C.go_cJSON_AddStringToObject(obj.ptr, C.CString(key), C.CString(fmt.Sprintf("%f", value)))
    // 实际应该用 go_cJSON_AddNumberToObject，这里简化了
    _ = value
}

// Print 将 JSON 对象格式化为字符串
func (obj *JSONObject) Print() string {
    cStr := C.go_cJSON_Print(obj.ptr)
    defer C.free(unsafe.Pointer(cStr))
    return C.GoString(cStr)
}

// Delete 释放 JSON 对象
func (obj *JSONObject) Delete() {
    C.go_cJSON_Delete(obj.ptr)
}

func main() {
    obj := CreateObject()
    defer obj.Delete()

    obj.AddString("name", "张三")
    obj.AddNumber("age", 25)

    fmt.Println("JSON:", obj.Print())
}
```

### 37.5.2 性能关键路径优化

在某些性能关键的代码路径上，使用 C 代码可以显著提升性能：

```go
package main

/*
#include <math.h>

// 纯 C 实现：计算数组元素平方和
double sum_of_squares(double* arr, int len) {
    double sum = 0.0;
    for (int i = 0; i < len; i++) {
        sum += arr[i] * arr[i];
    }
    return sum;
}

// 纯 C 实现：SIMD 优化的数组求和
double sum_array(double* arr, int len) {
    double sum = 0.0;
    for (int i = 0; i < len; i++) {
        sum += arr[i];
    }
    return sum;
}
*/
import "C"
import (
    "fmt"
    "time"
    "unsafe"
)

func main() {
    fmt.Println("=== 性能对比 ===")

    n := 10000000
    arr := make([]float64, n)
    for i := 0; i < n; i++ {
        arr[i] = float64(i % 1000)
    }

    // Go 版本
    start := time.Now()
    goSum := 0.0
    for _, v := range arr {
        goSum += v * v
    }
    goTime := time.Since(start)
    fmt.Printf("Go 版本耗时: %v, 结果: %.2f\n", goTime, goSum)

    // C 版本
    start = time.Now()
    cSum := C.sum_of_squares((*C.double)(unsafe.Pointer(&arr[0])), C.int(n))
    cTime := time.Since(start)
    fmt.Printf("C 版本耗时: %v, 结果: %.2f\n", cTime, cSum)

    fmt.Printf("C 比 Go 快: %.1f 倍\n", float64(goTime)/float64(cTime))
}
```

---

## 37.6 CGO 陷阱

> ⚠️ CGO 有很多"坑"，不了解的话很容易写出 bug 多多的代码。这一节我们来盘点一下常见的陷阱。

### 37.6.1 跨平台问题

不同平台的 C 行为可能不同：

```go
package main

/*
#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

void sleep_ms(int ms) {
#ifdef _WIN32
    Sleep(ms);
#else
    usleep(ms * 1000);
#endif
}
*/
import "C"
import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("=== 跨平台 CGO ===")

    start := time.Now()
    C.sleep_ms(100) // Windows 用 Sleep，Unix 用 usleep
    fmt.Printf("睡了 %v\n", time.Since(start))
}
```

### 37.6.2 性能开销

CGO 调用是有开销的！每次跨语言调用都需要上下文切换：

```go
package main

/*
#include <stdio.h>

// 空函数
void empty() {
    // 什么都不做
}

// 简单加法
int add(int a, int b) {
    return a + b;
}
*/
import "C"
import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("=== CGO 调用开销 ===")

    iterations := 1000000

    // 直接 Go 调用
    start := time.Now()
    for i := 0; i < iterations; i++ {
        _ = i + i
    }
    fmt.Printf("Go 调用: %v\n", time.Since(start))

    // CGO 空函数调用
    start = time.Now()
    for i := 0; i < iterations; i++ {
        C.empty()
    }
    fmt.Printf("CGO 空调用: %v\n", time.Since(start))

    // CGO 简单计算调用
    start = time.Now()
    for i := 0; i < iterations; i++ {
        C.add(1, 2)
    }
    fmt.Printf("CGO 加法调用: %v\n", time.Since(start))
}
```

### 37.6.3 调试困难

CGO 代码的调试比纯 Go 代码困难得多，因为 GDB/LLDB 对混合代码的支持有限：

```go
package main

/*
#include <stdio.h>

void breakpoint_here() {
    printf("C 代码中的断点...\n");
    // 在这里设置断点
}
*/
import "C"

func main() {
    C.breakpoint_here()
}
```

**调试技巧**：
1. 使用 `delve`（`dlv debug`）调试器
2. 在 C 代码中添加 `printf` 进行日志调试
3. 使用 `-cgocflags` 传递调试信息给 C 编译器

---

## 37.7 纯 Go 替代方案

> 🌟 虽然 CGO 很强大，但如果你能避免使用它，代码会更安全、更易维护。Go 生态中有很多纯 Go 实现的库。

| C 库 | Go 替代方案 |
|------|-------------|
| libcurl | `go-curl` / `net/http` |
| SQLite | `mattn/go-sqlite3` / `modernc.org/sqlite` |
| OpenSSL | `golang.org/x/crypto` |
| libpng | `github.com/pnganic` |
| zlib | `github.com/golang/groupcache/lz4` |

**建议**：能用纯 Go 就用纯 Go，实在不行再用 CGO。

---

## 37.8 CGO 编译流程

> 🔧 了解 CGO 的编译流程有助于解决编译问题。

### 37.8.1 C 代码编译

CGO 内部的编译流程：

1. Go 编译器识别 `import "C"` 和 `#cgo` 指令
2. C 代码被提取并写入临时 `.c` 文件
3. 调用 C 编译器（如 `gcc`）编译 C 代码
4. 生成目标文件（`.o`）
5. Go 链接器将 Go 代码和 C 目标文件链接在一起

### 37.8.2 链接过程

```bash
# 查看 CGO 生成的临时文件
CGO_CFLAGS="-save-temps=obj" go build -x main.go

# 会在当前目录生成：
# - main.c   (提取的 C 代码)
# - main.i   (预处理后的 C 代码)
# - main.s   (汇编代码)
# - main.o   (目标文件)
```

### 37.8.3 交叉编译

交叉编译需要指定目标平台：

```bash
# 编译 Windows 版本（在 Linux 上）
CGO_ENABLED=1 GOOS=windows GOARCH=amd64 \
  CC=x86_64-w64-mingw32-gcc \
  go build -o app.exe main.go
```

---

## 37.9 C 类型系统

> 📊 这一节详细看看 Go 和 C 之间的类型对应关系。

### 37.9.1 基本类型映射

参见 36.2.1 节的基本类型映射表。

### 37.9.2 结构体映射

```go
package main

/*
#include <stdio.h>

typedef struct {
    int x;
    int y;
} Point;

void print_point(Point p) {
    printf("Point{x=%d, y=%d}\n", p.x, p.y);
}

void move_point(Point* p, int dx, int dy) {
    p->x += dx;
    p->y += dy;
}
*/
import "C"
import (
    "fmt"
)

type GoPoint struct {
    X int
    Y int
}

func main() {
    fmt.Println("=== 结构体映射 ===")

    // 直接使用 C 的结构体
    var cPoint C.Point
    cPoint.x = 10
    cPoint.y = 20

    C.print_point(cPoint)

    // 传递指针
    C.move_point(&cPoint, 5, -3)
    C.print_point(cPoint)
}
```

### 37.9.3 联合体映射

C 的联合体（union）在 Go 中需要特殊处理：

```go
package main

/*
#include <stdio.h>
#include <string.h>

typedef union {
    int as_int;
    float as_float;
    char as_bytes[4];
} IntOrFloat;

void print_union(IntOrFloat u, const char* which) {
    if (strcmp(which, "int") == 0) {
        printf("as int: %d\n", u.as_int);
    } else if (strcmp(which, "float") == 0) {
        printf("as float: %f\n", u.as_float);
    }
}
*/
import "C"
import (
    "fmt"
)

func main() {
    fmt.Println("=== 联合体映射 ===")

    var u C.IntOrFloat

    // 作为整数使用
    u.as_int = 1065353216 // 浮点数 1.0 的位表示
    C.print_union(u, C.CString("int"))

    // 作为浮点数使用
    C.print_union(u, C.CString("float"))
}
```

### 37.9.4 指针映射

参见 36.2.3 节和 36.3.2 节。

### 37.9.5 数组映射

```go
package main

/*
#include <stdio.h>

void print_int_array(int* arr, int len) {
    printf("Array: [");
    for (int i = 0; i < len; i++) {
        if (i > 0) printf(", ");
        printf("%d", arr[i]);
    }
    printf("]\n");
}

int sum_int_array(int* arr, int len) {
    int sum = 0;
    for (int i = 0; i < len; i++) {
        sum += arr[i];
    }
    return sum;
}
*/
import "C"
import (
    "fmt"
    "unsafe"
)

func main() {
    fmt.Println("=== 数组映射 ===")

    // Go 切片转 C 数组
    goSlice := []C.int{1, 2, 3, 4, 5}

    C.print_int_array(&goSlice[0], C.int(len(goSlice)))

    sum := C.sum_int_array(&goSlice[0], C.int(len(goSlice)))
    fmt.Printf("Sum: %d\n", sum)
}
```

---

## 37.10 回调函数

> 🔄 这一节深入探讨 Go 和 C 之间的回调机制。

### 37.10.1 Go 函数导出

使用 `//export` 注释导出 Go 函数给 C 使用：

```go
package main

/*
#include <stdio.h>

// 声明一个回调函数类型
typedef void (*Callback)(int);

// 这个函数会调用回调
void process_with_callback(Callback cb) {
    printf("C: 开始处理\n");
    for (int i = 0; i < 3; i++) {
        printf("C: 调用回调，值=%d\n", i);
        cb(i); // 调用 Go 函数
    }
    printf("C: 处理完成\n");
}
*/
import "C"
import (
    "fmt"
)

//export onValue
func onValue(n C.int) {
    fmt.Printf("Go: 收到回调，值=%d\n", n)
}

func main() {
    fmt.Println("=== Go 函数导出 ===")
    C.process_with_callback(C.Callback(C.onValue))
}
```

### 37.10.2 C 调用 Go

C 代码可以通过回调来"调用"Go 代码（参见上节）。

### 37.10.3 线程安全

CGO 的回调在多线程环境下需要特别注意：

```go
package main

/*
#include <stdio.h>
#include <pthread.h>

void* call_from_c(void* arg) {
    // 回调函数指针
    void (*callback)(int) = (void (*)(int))arg;
    for (int i = 0; i < 5; i++) {
        callback(i);
    }
    return NULL;
}

void create_thread_and_call(void (*callback)(int)) {
    pthread_t thread;
    pthread_create(&thread, NULL, call_from_c, (void*)callback);
    pthread_join(thread, NULL);
}
*/
import "C"
import (
    "fmt"
    "sync"
)

//export onThreadValue
func onThreadValue(n C.int) {
    mu.Lock()
    defer mu.Unlock()
    fmt.Printf("线程安全回调: %d\n", n)
}

var mu sync.Mutex

func main() {
    fmt.Println("=== 线程安全回调 ===")
    C.create_thread_and_call(C.Callback(C.onThreadValue))
}
```

---

## 37.11 CGO 性能优化

> ⚡ 这一节来看看如何优化 CGO 代码的性能。

### 37.11.1 减少 CGO 调用

CGO 调用有开销，尽量减少调用次数：

```go
package main

/*
#include <stdio.h>

// 一次处理多个元素
void batch_process(int* arr, int len) {
    for (int i = 0; i < len; i++) {
        arr[i] = arr[i] * 2 + 1;
    }
}
*/
import "C"
import (
    "fmt"
    "time"
    "unsafe"
)

func main() {
    fmt.Println("=== 减少 CGO 调用 ===")

    n := 1000000
    arr := make([]C.int, n)
    for i := 0; i < n; i++ {
        arr[i] = C.int(i)
    }

    // 方法一：逐个调用（大量 CGO 开销）
    start := time.Now()
    for i := 0; i < n; i++ {
        // 假设每个元素都需要单独处理
        // 实际中可能是逐个调用 C 函数
    }
    fmt.Printf("逐个处理耗时: %v\n", time.Since(start))

    // 方法二：批量调用（一次 CGO 调用处理所有）
    start = time.Now()
    C.batch_process(&arr[0], C.int(n))
    fmt.Printf("批量处理耗时: %v\n", time.Since(start))
}
```

### 37.11.2 批量处理

将多个操作打包成一次调用：

```go
package main

/*
#include <stdlib.h>
#include <string.h>

// 批量复制字符串
void batch_copy_strings(char** dest, char** src, int count) {
    for (int i = 0; i < count; i++) {
        int len = strlen(src[i]) + 1;
        dest[i] = (char*)malloc(len);
        strcpy(dest[i], src[i]);
    }
}
*/
import "C"
import (
    "fmt"
    "unsafe"
)

func main() {
    fmt.Println("=== 批量处理 ===")

    srcStrings := []string{"Hello", "World", "CGO", "高性能"}
    count := len(srcStrings)

    // 转换源字符串
    cSrc := make([]*C.char, count)
    for i, s := range srcStrings {
        cSrc[i] = C.CString(s)
        defer C.free(unsafe.Pointer(cSrc[i]))
    }

    // 分配目标指针数组
    cDest := make([]*C.char, count)

    // 批量复制
    C.batch_copy_strings(&cDest[0], &cSrc[0], C.int(count))

    // 打印结果
    for i := 0; i < count; i++ {
        fmt.Printf("dest[%d] = %s\n", i, C.GoString(cDest))
        C.free(unsafe.Pointer(cDest[i]))
    }
}
```

### 37.11.3 异步 CGO

在 goroutine 中调用 CGO 可以提高并发度：

```go
package main

/*
#include <unistd.h"

void blocking_operation(int* result) {
    sleep(1); // 模拟耗时操作
    *result = 42;
}
*/
import "C"
import (
    "fmt"
    "sync"
    "time"
)

func main() {
    fmt.Println("=== 异步 CGO ===")

    start := time.Now()

    var wg sync.WaitGroup
    for i := 0; i < 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            var result C.int
            C.blocking_operation(&result)
            fmt.Printf("任务 %d 完成，结果: %d\n", id, result)
        }(i)
    }

    wg.Wait()
    fmt.Printf("总耗时: %v (并行执行，应该约 1 秒)\n", time.Since(start))
}
```

---

## 37.12 CGO 调试

> 🔍 CGO 代码的调试比纯 Go 代码更复杂，这一节来看看常用的调试方法。

### 37.12.1 C 调试器

使用 GDB 或 LLDB 调试 C 代码：

```bash
# 编译带调试信息的版本
CGO_CFLAGS="-g -O0" go build -o main main.go

# 使用 GDB 调试
gdb ./main
```

### 37.12.2 混合调试

Delve 支持混合调试 Go 和 C 代码：

```bash
# 使用 Delve 调试
dlv debug main.go

# 在 Delve 中设置断点
# (dlv) break C.sayHello
# (dlv) break main.main
# (dlv) continue
```

### 37.12.3 内存问题定位

CGO 代码内存问题常用工具：
- Valgrind: 检测内存泄漏
- AddressSanitizer: 运行时内存错误检测
- MSan: 检测未初始化内存使用

### 常见 CGO 内存问题

```go
package main

/*
#include <stdlib.h>
#include <stdio.h>

void memory_leak() {
    void* p = malloc(100);
    // 忘记调用 free(p)！内存泄漏
    printf("分配了内存但没有释放\n");
}

void use_after_free() {
    char* p = (char*)malloc(10);
    free(p);
    // 释放后继续使用！危险！
    p[0] = 'A';
    printf("释放后使用: %c\n", p[0]);
}

void buffer_overflow() {
    int* arr = (int*)malloc(5 * sizeof(int)); // 只分配了 5 个元素
    for (int i = 0; i < 10; i++) { // 写入 10 个元素！
        arr[i] = i;
    }
    printf("buffer overflow!\n");
    free(arr);
}
*/
import "C"
import (
    "fmt"
)

func main() {
    fmt.Println("=== CGO 内存问题 ===")

    C.memory_leak()
    C.use_after_free()
    C.buffer_overflow()
}
```

**调试建议**：
1. 使用 `-fsanitize=address` 编译 C 代码
2. 在 C 代码中添加详细的 `printf` 日志
3. 使用 Valgrind 检测内存泄漏
4. 仔细检查所有 `malloc` 对应的 `free`

---

## 本章小结

> 🎉 恭喜你完成了 CGO 之旅！这一章我们探索了 Go 和 C 之间的"桥梁"。

### 核心要点回顾

1. **CGO 是 Go 调用 C 代码的桥梁**：通过 `import "C"` 和注释中的 C 代码实现。

2. **类型映射是基础**：Go 和 C 之间有固定的基本类型映射规则，字符串和复杂类型需要手动转换。

3. **内存管理是难点**：谁分配谁释放！C 分配的内存需要手动释放。

4. **回调是双向通道**：Go 函数可以被导出给 C 调用，但需要使用 `//export` 注释。

5. **性能开销不可忽视**：CGO 调用有显著的性能开销，应该批量处理而非频繁调用。

6. **调试更困难**：混合 Go 和 C 代码让调试变得更复杂，需要借助 GDB/LLDB/Valgrind 等工具。

### CGO 使用场景

- ✅ 调用现有的 C 库
- ✅ 使用成熟的 C 工具库
- ✅ 性能关键路径优化
- ✅ 系统编程（直接调用系统 API）

### 替代方案

- 🌟 能用纯 Go 就用纯 Go
- 🌟 考虑使用 `cgo` 封装好的库
- 🌟 WebAssembly 可以作为跨语言方案

> 💡 **最后一句话**：CGO 是一把双刃剑——它让你能够站在 C 几十年积累的巨人肩膀上，但代价是代码复杂度和调试难度的大幅提升。除非真的需要，否则请三思而后行！

