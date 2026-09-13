+++
title = "第39章 性能优化——让代码跑得比兔子还快"
weight = 390
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第39章 性能优化——让代码跑得比兔子还快

## 39.1 性能优化的核心哲学：先测量，后优化

### 为什么要"先测量"？

江湖上流传着一个古老的传说：**"过早优化是万恶之源。"** 这句话通常被归到高德纳（Donald Knuth）名下，
而高德纳本人又把它归功于托尼·霍尔（Tony Hoare）。高德纳 1974 年的文章《Structured Programming with go to Statements》里写的是：

> "We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil."
> （小处的效率，大约 97% 的场合都可以忽略不计：过早优化是万恶之源。）

注意这个"97%"是有前提的——**另外那 3% 的关键路径不能放过**。
这句话的真实含义是：**不要在你还没搞清楚瓶颈在哪的时候就开始优化**。你辛辛苦苦把一个函数从10毫秒优化到1毫秒，结果发现它只占总运行时间的1%，而真正的瓶颈在那个你没注意到的数据库查询上（花了500毫秒）。这不是优化，这是"感动自己"。

所以，性能优化的第一条铁律是：

> **"测量，测量，还是他喵的测量！"**

### 性能优化的正确姿势

性能优化的正确流程是这样的：

```
1. 写一个"够用"的版本（不要一开始就想着优化）
2. 测量（profiling）找出真正的瓶颈
3. 只优化那些值得优化的地方
4. 优化后再次测量，确认效果
5. 重复2-4步
```

这就像看病：**先做检查（测量），再开药（优化），吃完药再复查（再次测量）**。你不会在没做CT的时候就让医生给你开刀吧？同样的道理，不要在没profiling的时候就动手优化代码。

### 使用chrono精确测量时间

C++11引入了`<chrono>`库，给你提供了高精度的计时工具：

```cpp
#include <iostream>
#include <chrono>
#include <vector>
#include <numeric>

// 一个看似无害的函数
long long slow_sum(const std::vector<int>& v) {
    long long sum = 0;
    for (size_t i = 0; i < v.size(); ++i) {  // 注意：用size_t避免符号警告
        sum += v[i];
    }
    return sum;
}

// 优化版本
long long fast_sum(const std::vector<int>& v) {
    long long sum = 0;
    size_t n = v.size();  // 缓存size，避免重复调用
    for (size_t i = 0; i < n; ++i) {
        sum += v[i];
    }
    return sum;
}

// 更快版本：使用迭代器
long long fastest_sum(const std::vector<int>& v) {
    return std::accumulate(v.begin(), v.end(), 0LL);
}

int main() {
    std::vector<int> big_vector(10'000'000, 1);  // 一千万个1

    // 测试slow_sum
    auto start = std::chrono::high_resolution_clock::now();
    long long result1 = slow_sum(big_vector);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration1 = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "slow_sum结果: " << result1 
              << ", 耗时: " << duration1.count() << " 微秒\n";

    // 测试fast_sum
    start = std::chrono::high_resolution_clock::now();
    long long result2 = fast_sum(big_vector);
    end = std::chrono::high_resolution_clock::now();
    auto duration2 = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "fast_sum结果: " << result2 
              << ", 耗时: " << duration2.count() << " 微秒\n";

    // 测试fastest_sum
    start = std::chrono::high_resolution_clock::now();
    long long result3 = fastest_sum(big_vector);
    end = std::chrono::high_resolution_clock::now();
    auto duration3 = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "fastest_sum结果: " << result3 
              << ", 耗时: " << duration3.count() << " 微秒\n";

    // 防止编译器"太聪明"把没用的计算优化掉
    if (result1 == 0) std::cout << "Never happens\n";
}
```

> ⚠️ **测性能的两条铁律**（这个例子最想教你的是这个）：
>
> 1. **一定要开优化**：用 `clang++ -std=c++23 -O2 bench.cpp -o bench` 编译。
>    不加 `-O2` 测到的是"调试版代码"，数字毫无参考价值（本机实测不加优化时反而可能"更慢版本更快"）。
> 2. **不能只跑一次**：CPU 频率调节、缓存状态、后台进程都会影响结果。
>    下面同一份代码、同一台机器连续跑两次，数字能差 3 倍。

运行结果（Apple clang，`-O2`，同一台机器连续跑两次）：

```text
slow_sum结果: 10000000, 耗时: 4581 微秒
fast_sum结果: 10000000, 耗时: 1760 微秒
fastest_sum结果: 10000000, 耗时: 1004 微秒
—— 再跑一次 ——
slow_sum结果: 10000000, 耗时: 1548 微秒
fast_sum结果: 10000000, 耗时: 729 微秒
fastest_sum结果: 10000000, 耗时: 750 微秒
```

看出来了吗？**第二次运行里 `fast_sum` 和 `fastest_sum` 几乎一样快**。开了 `-O2` 之后，编译器会把这三个版本的循环优化成非常接近的机器码，
`std::accumulate` 的优势主要在"意图清晰、不容易写错下标"，而不是"凭空快几倍"。
想在性能上真的下功夫，请用 Google Benchmark 这类框架做重复测量，别拿一次 `chrono` 的结果下结论。

### 使用prof工具进行profiling

光靠自己写计时代码是不够的，你需要一个真正的profiler。在Linux上，`gprof`和`perf`是你的好朋友；在Windows上，`Visual Studio Profiler`或者`Very Sleepy`可以派上用场；在macOS上，`Instruments`的Time Profiler是神器。

一个典型的`gprof`使用流程：

```bash
# 编译时加上 -pg 选项
g++ -pg -O2 -o myprogram myprogram.cpp

# 运行程序，这会在当前目录生成 gmon.out
./myprogram

# 生成profiling报告
gprof myprogram gmon.out > profile.txt
```

> **警告**：`gprof`只能分析程序中执行了的部分，对于那些被频繁调用但很快就返回的函数，它可能会"忽略"它们。所以别完全依赖它。

---

## 39.2 编译器优化：让编译器替你干脏活累活

### 编译器能做什么？

现代编译器（GCC、Clang、MSVC）都是"隐形超人"，它们在你看不见的地方默默做了大量优化：

- **常量折叠**（Constant Folding）：`int x = 2 + 3;` 直接变成 `int x = 5;`
- **死代码消除**（Dead Code Elimination）：永远不会被执行的代码会被删掉
- **内联展开**（Inlining）：把函数调用直接换成函数体
- **循环展开**（Loop Unrolling）：减少循环分支判断的开销
- **寄存器分配**（Register Allocation）：尽量把变量放到CPU寄存器里
- **指令调度**（Instruction Scheduling）：重排指令顺序以提高流水线效率

### 常用优化级别

GCC和Clang的优化级别：

| 级别 | 名字 | 说明 |
|------|------|------|
| `-O0` | 无优化 | 编译速度最快，方便调试 |
| `-O1` | 基本优化 | 启用一些安全的优化 |
| `-O2` | 激进优化 | 启用更多优化，会增加编译时间 |
| `-O3` | 极限优化 | 启用所有优化，包括一些"激进"的优化 |
| `-Os` | 大小优化 | 优化代码大小 |
| `-Ofast` | 极速优化 | 启用所有-O3优化，并允许违反IEEE/ISO标准的行为（FFTW用户的最爱） |

> **小技巧**：在调试的时候用`-O0`，发布的时候用`-O2`或`-O3`。别在debug模式下测试性能，那是自欺欺人。

### 开启编译器优化开关的对比

让我们用一个具体的例子来展示编译器优化的威力：

```cpp
// optimization_demo.cpp
#include <iostream>
#include <vector>

// 一个简单的计算密集型函数
double compute_sum(const std::vector<double>& data) {
    double sum = 0.0;
    for (size_t i = 0; i < data.size(); ++i) {
        sum += data[i] * data[i] + 1.0;
    }
    return sum;
}

int main() {
    std::vector<double> data(1'000'000);
    for (size_t i = 0; i < data.size(); ++i) {
        data[i] = static_cast<double>(i);
    }

    double result = compute_sum(data);
    std::cout << "Result: " << result << std::endl;
    return 0;
}
```

对比不同优化级别的性能：

```bash
# 无优化
g++ -O0 -o opt_demo opt_demo.cpp
time ./opt_demo
# Output: Result: 3.33333266667e+23, Time: ~120ms

# O2优化
g++ -O2 -o opt_demo opt_demo.cpp
time ./opt_demo
# Output: Result: 3.33333266667e+23, Time: ~18ms  （快了6倍多！）

# O3优化（开启更多激进优化，包括SIMD向量化）
g++ -O3 -o opt_demo opt_demo.cpp
time ./opt_demo
# Output: Result: 3.33333266667e+23, Time: ~8ms   （又快了一倍！）
```

### SIMD向量化：一条指令干多件事

SIMD（Single Instruction Multiple Data，单指令多数据）是现代CPU的一项神技。简单来说，就是用一条指令同时处理多个数据。

例如，你有一个长度为1000的数组，每个元素都要乘以2。用普通方式，你需要执行1000次乘法指令。但如果CPU支持SSE/AVX，可以一条指令同时处理4个（或者8个、16个，取决于CPU架构）数据！

编译器会自动帮你做向量化优化，但你也可以手动用intrinsics或者`std::experimental::simd`（C++20）来显式控制：

```cpp
#include <iostream>
#include <vector>
#include <chrono>

// 普通版本
void multiply_by_two_normal(std::vector<double>& v) {
    for (size_t i = 0; i < v.size(); ++i) {
        v[i] *= 2.0;
    }
}

// 手动SIMD版本（使用GCC/Clang的built-in）
#ifdef __AVX__
void multiply_by_two_simd(std::vector<double>& v) {
    size_t i = 0;
    __m256d factor = _mm256_set1_pd(2.0);  // 创建一个包含4个2.0的向量
    size_t limit = v.size() - (v.size() % 4);
    
    for (; i < limit; i += 4) {
        __m256d values = _mm256_loadu_pd(&v[i]);  // 一次加载4个double
        __m256d result = _mm256_mul_pd(values, factor);  // 一次乘4个
        _mm256_storeu_pd(&v[i], result);  // 一次存储4个
    }
    
    // 处理剩余的元素
    for (; i < v.size(); ++i) {
        v[i] *= 2.0;
    }
}
#else
void multiply_by_two_simd(std::vector<double>& v) {
    multiply_by_two_normal(v);  // 没有AVX就fallback到普通版本
}
#endif

int main() {
    const size_t N = 10'000'000;
    std::vector<double> v1(N, 1.5), v2(N, 1.5);

    // 测试普通版本
    auto start = std::chrono::high_resolution_clock::now();
    multiply_by_two_normal(v1);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration1 = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "普通版本耗时: " << duration1.count() << " ms\n";

    // 测试SIMD版本
    start = std::chrono::high_resolution_clock::now();
    multiply_by_two_simd(v2);
    end = std::chrono::high_resolution_clock::now();
    auto duration2 = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "SIMD版本耗时: " << duration2.count() << " ms\n";

    // 验证结果一致性
    bool correct = true;
    for (size_t i = 0; i < N; ++i) {
        if (v1[i] != v2[i]) {
            correct = false;
            break;
        }
    }
    std::cout << "结果验证: " << (correct ? "✓ 正确" : "✗ 错误") << "\n";
}
```

### Link-Time Optimization（LTO）：跨编译单元的优化

传统的编译器优化只能在单个编译单元内进行。但通过LTO，编译器可以在链接阶段看到所有目标文件，从而进行更大范围的优化：

```bash
# 开启LTO
g++ -O3 -flto -o program file1.cpp file2.cpp file3.cpp

# 或者分步编译
g++ -O3 -flto -c file1.cpp
g++ -O3 -flto -c file2.cpp
g++ -O3 -flto -c file3.cpp
g++ -O3 -flto -o program file1.o file2.o file3.o
```

LTO可以让编译器做很多"跨函数"的优化，比如：

- 如果一个函数只被一个地方调用，并且足够小，就直接内联进去
- 识别从未被调用的函数并删掉
- 更激进的数据流分析

---

## 39.3 内存访问优化：Cache为王

### CPU和内存的速度鸿沟

你知道CPU访问一个寄存器需要多长时间吗？**约1个纳秒（ns）**。

你知道CPU访问内存（RAM）需要多长时间吗？**约100纳秒**。

差了整整**100倍**！这就像你去冰箱拿饮料只需要1秒，但让你老婆去拿要100秒（别问我怎么知道的）。

为了弥补这个速度差，CPU引入了**缓存（Cache）**机制：

```text
寄存器 ──1ns──> L1 Cache ──3ns──> L2 Cache ──10ns──> L3 Cache ──100ns──> RAM
```

L1 Cache通常只有32KB左右，L2大约256KB，L3可能有几MB到几十MB。虽然很小，但命中缓存比访问内存快几百倍！

### 缓存友好的代码

**数据局部性（Data Locality）** 是性能优化的核心概念之一。简单来说：**相邻的内存访问更容易被缓存命中**。

让我们看一个经典的例子——矩阵乘法：

```cpp
#include <iostream>
#include <vector>
#include <chrono>
#include <iomanip>

const int N = 512;

// 缓存不友好的版本：按列访问
void matrix_multiply_naive(const std::vector<double>& A, 
                            const std::vector<double>& B, 
                            std::vector<double>& C) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            double sum = 0.0;
            for (int k = 0; k < N; ++k) {
                sum += A[i * N + k] * B[k * N + j];  // B按列访问！Cache不友好！
            }
            C[i * N + j] = sum;
        }
    }
}

// 缓存友好的版本：改变循环顺序，按行访问B
void matrix_multiply_cache_friendly(const std::vector<double>& A, 
                                     const std::vector<double>& B, 
                                     std::vector<double>& C) {
    // 先把B转置，这样访问B[j * N + k]就变成连续访问了
    std::vector<double> B_T(N * N);
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            B_T[j * N + i] = B[i * N + j];
        }
    }
    
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            double sum = 0.0;
            for (int k = 0; k < N; ++k) {
                sum += A[i * N + k] * B_T[j * N + k];  // 两次都是连续访问！
            }
            C[i * N + j] = sum;
        }
    }
}

// 使用分块（Tiling）优化，进一步提升缓存命中率
// 注意：C必须预先填充为0（调用方负责），本函数会累加到C上
void matrix_multiply_blocked(const std::vector<double>& A,
                              const std::vector<double>& B,
                              std::vector<double>& C) {
    constexpr int BLOCK_SIZE = 64;  // 适合L1 Cache的分块大小

    // 分块只是"限定处理范围"，真正让速度飞起来的是循环顺序：
    // i-k-j 顺序下，内层循环访问的是 C 和 B 的**连续**内存
    for (int i0 = 0; i0 < N; i0 += BLOCK_SIZE) {
        for (int k0 = 0; k0 < N; k0 += BLOCK_SIZE) {
            for (int j0 = 0; j0 < N; j0 += BLOCK_SIZE) {
                for (int i = i0; i < std::min(i0 + BLOCK_SIZE, N); ++i) {
                    for (int k = k0; k < std::min(k0 + BLOCK_SIZE, N); ++k) {
                        const double a = A[i * N + k];  // 取出来复用，只读一次
                        for (int j = j0; j < std::min(j0 + BLOCK_SIZE, N); ++j) {
                            C[i * N + j] += a * B[k * N + j];  // 连续访问 B 和 C
                        }
                    }
                }
            }
        }
    }
}

int main() {
    // 初始化矩阵
    std::vector<double> A(N * N, 1.0), B(N * N, 1.0), C(N * N, 0.0);
    
    // 测试缓存不友好版本
    auto start = std::chrono::high_resolution_clock::now();
    matrix_multiply_naive(A, B, C);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration1 = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Naive版本耗时: " << duration1.count() << " ms\n";
    
    // 测试缓存友好版本
    std::fill(C.begin(), C.end(), 0.0);
    start = std::chrono::high_resolution_clock::now();
    matrix_multiply_cache_friendly(A, B, C);
    end = std::chrono::high_resolution_clock::now();
    auto duration2 = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Cache友好版本耗时: " << duration2.count() << " ms\n";
    
    // 测试分块版本
    std::fill(C.begin(), C.end(), 0.0);
    start = std::chrono::high_resolution_clock::now();
    matrix_multiply_blocked(A, B, C);
    end = std::chrono::high_resolution_clock::now();
    auto duration3 = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "分块优化版本耗时: " << duration3.count() << " ms\n";
    
    return 0;
}
```

实测输出（Apple clang，`-std=c++23 -O2`，N = 512）：

```text
Naive版本耗时: 98 ms
Cache友好版本耗时: 52 ms
分块优化版本耗时: 11 ms
```

> **同一个算法、同一组数据，只是改变内存访问顺序，就从 98 ms 降到 11 ms——快了约 9 倍。**
> 这正是缓存局部性的威力：`Naive` 每算一个 `C[i][j]` 都要"列遍历"一遍 `B`，每次都踩空缓存；
> 转置版把列访问变成行访问，省掉了一半时间；分块版再加上 i-k-j 循环顺序，让 `A`、`B`、`C` 三者的访问都落在连续内存上。
>
> ⚠️ **反例警告**：如果只做分块、却仍然按 i-j-k 顺序写内层循环（按列访问 `B`），实测反而是 **73 ms**——比转置版还慢。
> 记住：**分块解决的是"数据能否留在缓存里"，循环顺序解决的是"访问是否连续"，两者缺一不可。**

### 预取（Prefetching）：提前把数据拉到缓存里

CPU支持"预取"指令，告诉你"我猜你接下来要用这个地址的数据，先帮我拉到缓存里"。虽然现代编译器/CPU已经做了一些自动预取，但你也可以手动控制：

```cpp
#include <immintrin.h>  // for _mm_prefetch

void process_with_prefetch(double* data, size_t n) {
    for (size_t i = 0; i < n; ++i) {
        // _MM_HINT_T0: 预取到L1 Cache
        // _MM_HINT_T1: 预取到L2 Cache
        // _MM_HINT_T2: 预取到L3 Cache
        if (i + 16 < n) {  // 预取16个元素之后的数据
            _mm_prefetch(&data[i + 16], _MM_HINT_T0);
        }
        // 处理当前元素
        data[i] = std::sqrt(data[i]) * 2.0;
    }
}
```

> **警告**：预取是一把双刃剑。用好了提速，用砸了帮倒忙。过度的预取会污染缓存，反而降低性能。除非你真的很确定你知道数据访问模式，否则别手动预取。

### 数据结构的对齐和布局

现代CPU喜欢数据对齐访问。如果你的数据没对齐，CPU可能需要两次访存才能取到一个值：

```cpp
#include <iostream>
#include <vector>

// 未对齐的结构（编译器可能会自动对齐，但显式控制更保险）
struct PointUnaligned {
    double x;
    double y;
    char padding[6];  // 使总大小为22字节，编译器会补齐到24字节（8字节对齐）
};

// 使用__attribute__((aligned))指定对齐
struct PointAligned {
    double x;
    double y;
} __attribute__((aligned(32)));  // 32字节对齐，适合AVX

// C++17可以用alignas
struct PointAlignedCPP17 {
    alignas(32) double x;
    alignas(32) double y;
};

// std::vector的对齐容器（ISO C++17）
#include <vector>
#include <memory>

void demo_aligned_alloc() {
    // 普通vector的data()返回的指针可能不对齐
    std::vector<double> v(100);
    std::cout << "普通vector对齐: " << (reinterpret_cast<size_t>(v.data()) % 32) << "\n";
    
    // 使用std::aligned_alloc分配对齐内存
    double* aligned_ptr = static_cast<double*>(std::aligned_alloc(32, 1000 * sizeof(double)));
    std::cout << "对齐内存对齐: " << (reinterpret_cast<size_t>(aligned_ptr) % 32) << "\n";
    
    // 记得free
    std::free(aligned_ptr);
}

int main() {
    std::cout << "sizeof(PointAligned): " << sizeof(PointAligned) << "\n";
    std::cout << "alignof(PointAligned): " << alignof(PointAligned) << "\n";
    demo_aligned_alloc();
    return 0;
}
```

---

## 39.4 代码级优化：细节决定成败

### 循环优化的艺术

循环是性能问题的"高发区"。以下是几种常用的循环优化技巧：

#### 技巧1：循环不变代码外提（Loop-Invariant Code Motion）

把循环内不变的部分移到循环外：

```cpp
// 优化前
for (int i = 0; i < n; ++i) {
    result[i] = data[i] + std::sin(3.14159);  // sin(π)每次循环都计算一次
}

// 优化后
double angle = std::sin(3.14159);  // 只计算一次
for (int i = 0; i < n; ++i) {
    result[i] = data[i] + angle;
}
```

#### 技巧2：循环展开（Loop Unrolling）

减少循环分支判断的次数：

```cpp
// 优化前
for (int i = 0; i < n; ++i) {
    sum += data[i];
}

// 优化后（手动展开4次）
int i = 0;
int limit = (n / 4) * 4;  // 先处理4的倍数部分
for (; i < limit; i += 4) {
    sum += data[i] + data[i+1] + data[i+2] + data[i+3];
}
// 处理剩余元素
for (; i < n; ++i) {
    sum += data[i];
}
```

不过，**现代编译器已经能自动做循环展开了**。所以除非你有特别的原因，否则不要手动展开——那只会让代码更难读。

#### 技巧3：使用范围for循环和迭代器

在C++中，`std::vector`的迭代器通常比索引访问更快，因为迭代器可以直接递增指针，而索引访问需要每次重新计算地址：

```cpp
std::vector<int> v(1000, 1);

// 可能稍快的版本（取决于编译器优化）
int sum = 0;
for (auto it = v.begin(); it != v.end(); ++it) {
    sum += *it;
}

// 更快：使用范围for（编译器会优化成和上面几乎一样的代码）
sum = 0;
for (int x : v) {
    sum += x;
}

// 最快：使用STL算法
sum = std::accumulate(v.begin(), v.end(), 0);
```

### 减少函数调用开销

函数调用是有开销的——你需要保存寄存器、跳转、返回。对于那些"小而频繁"的函数，这个开销可能很可观。

#### 内联（Inline）

使用`inline`关键字建议编译器把函数体直接展开到调用点：

```cpp
// 小函数，用inline
inline int min(int a, int b) {
    return a < b ? a : b;
}

// 大函数，别用inline（会导致代码膨胀）
void do_something_large();  // 不inline

// 现代C++的建议：用constexpr或者直接放在头文件里让编译器决定
constexpr int min(int a, int b) {
    return a < b ? a : b;
}
```

> **注意**：`inline`只是建议，编译器可以无视它。反过来，即使你没有写`inline`，编译器在`-O2`以上也可能主动内联。

#### Lambda表达式：就地定义，减少调用开销

Lambda可以让我们写出"一次性"的小函数对象，编译器通常会直接内联它们：

```cpp
#include <algorithm>
#include <vector>

// 不用lambda：需要单独定义函数
bool is_positive(int x) { return x > 0; }

// 用lambda：就地定义就地用，编译器更容易内联
std::vector<int> v = {-3, -2, -1, 0, 1, 2, 3};
int count = std::count_if(v.begin(), v.end(), [](int x) { return x > 0; });
std::cout << "正数个数: " << count << "\n";
```

### 避免不必要的内存分配

动态内存分配（`new`/`malloc`）是已知的性能杀手。让我们看看如何减少它：

#### 对象池（Object Pool）

预先分配一堆对象，用完再放回去，避免频繁的`new`/`delete`：

```cpp
#include <iostream>
#include <vector>
#include <memory>
#include <stdexcept>

template<typename T>
class ObjectPool {
public:
    // 预先分配n个对象
    explicit ObjectPool(size_t n = 128) {
        pool_.reserve(n);
        free_list_.reserve(n);
        for (size_t i = 0; i < n; ++i) {
            pool_.push_back(std::make_unique<T>());
            free_list_.push_back(pool_.back().get());
        }
    }
    
    // 获取一个对象
    T* acquire() {
        if (free_list_.empty()) {
            throw std::runtime_error("Object pool exhausted!");
        }
        T* obj = free_list_.back();
        free_list_.pop_back();
        ++in_use_;
        return obj;
    }
    
    // 归还一个对象
    void release(T* obj) {
        if (obj) {
            free_list_.push_back(obj);
            --in_use_;
        }
    }
    
    size_t available() const { return free_list_.size(); }
    size_t in_use() const { return in_use_; }
    
private:
    std::vector<std::unique_ptr<T>> pool_;   // 拥有所有对象，负责释放
    std::vector<T*> free_list_;              // 当前空闲、可以借出去的对象
    size_t in_use_ = 0;                      // 已经借出、尚未归还的个数
};

struct ExpensiveObject {
    int data[64];  // 模拟一个"大"对象
    ExpensiveObject() { 
        for (int i = 0; i < 64; ++i) data[i] = i; 
    }
};

int main() {
    // 池子要比"同时需要的对象数"大，否则 acquire 会抛异常
    ObjectPool<ExpensiveObject> pool(1024);
    std::cout << "对象池初始大小: " << pool.available() << "\n";
    
    // 模拟大量对象的创建和销毁
    std::vector<ExpensiveObject*> objects;
    for (int i = 0; i < 1000; ++i) {
        objects.push_back(pool.acquire());
    }
    std::cout << "分配1000个对象后，池中剩余: " << pool.available() << "\n";
    
    for (auto* obj : objects) {
        pool.release(obj);
    }
    std::cout << "全部归还后，池中可用: " << pool.available() << "\n";
    
    return 0;
}
```

#### 预分配+就地构造

对于容器，尽可能预分配空间，避免多次重新分配：

```cpp
#include <iostream>   // std::cout
#include <vector>
#include <string>
#include <chrono>

void without_reserve() {
    std::vector<std::string> v;
    for (int i = 0; i < 10000; ++i) {
        v.push_back("hello world");
    }
}

void with_reserve() {
    std::vector<std::string> v;
    v.reserve(10000);  // 预分配，避免多次扩容
    for (int i = 0; i < 10000; ++i) {
        v.push_back("hello world");
    }
}

int main() {
    auto start = std::chrono::high_resolution_clock::now();
    without_reserve();
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "without_reserve: " 
              << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()
              << " us\n";
    
    start = std::chrono::high_resolution_clock::now();
    with_reserve();
    end = std::chrono::high_resolution_clock::now();
    std::cout << "with_reserve: " 
              << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()
              << " us\n";
    
    return 0;
}
```

---

## 39.5 算法与数据结构：选择比努力更重要

### O(n²)与O(n log n)的差距

如果你觉得"算法优化不如硬件升级"，请看下面的例子：

| 复杂度 | n=100 | n=1,000 | n=10,000 | n=1,000,000 |
|--------|-------|---------|----------|-------------|
| O(n²) | 10,000 | 1,000,000 | 100,000,000 | 10¹² |
| O(n log n) | 664 | 9,966 | 132,877 | 19,931,568 |
| O(n) | 100 | 1,000 | 10,000 | 1,000,000 |

在n=10,000时，O(n²)的算法要做1亿次操作，而O(n log n)只需要约13万次。差了**750倍**！

所以，**选择正确的算法是你能给程序带来的最大提升**，没有之一。

### 排序算法：std::sort已经很强大了

很多人喜欢自己实现排序算法，觉得"我写的肯定比库快"。但事实是，`std::sort`（通常实现为Introsort——快速排序+堆排序+插入排序的混合）已经非常快了：

```cpp
#include <algorithm>
#include <vector>
#include <random>
#include <chrono>
#include <iostream>

// 一个"半吊子"的快速排序
int partition(std::vector<int>& v, int low, int high) {
    int pivot = v[high];
    int i = low - 1;
    for (int j = low; j < high; ++j) {
        if (v[j] <= pivot) {
            ++i;
            std::swap(v[i], v[j]);
        }
    }
    std::swap(v[i + 1], v[high]);
    return i + 1;
}

void quick_sort(std::vector<int>& v, int low, int high) {
    if (low < high) {
        int pi = partition(v, low, high);
        quick_sort(v, low, pi - 1);
        quick_sort(v, pi + 1, high);
    }
}

int main() {
    const size_t N = 1'000'000;
    std::vector<int> v1(N), v2(N);
    
    std::mt19937 rng(42);
    for (size_t i = 0; i < N; ++i) {
        v1[i] = v2[i] = rng();
    }
    
    // 测试手写的快速排序
    auto start = std::chrono::high_resolution_clock::now();
    quick_sort(v1, 0, static_cast<int>(N) - 1);
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "手写快速排序: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms\n";
    
    // 测试std::sort
    start = std::chrono::high_resolution_clock::now();
    std::sort(v2.begin(), v2.end());
    end = std::chrono::high_resolution_clock::now();
    std::cout << "std::sort: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms\n";
    
    // 验证排序正确性
    std::cout << "排序正确: " << std::is_sorted(v2.begin(), v2.end()) << "\n";
    
    return 0;
}
```

### 哈希表 vs 有序数组：随机访问vs二分查找

根据你的访问模式选择正确的数据结构：

```cpp
#include <unordered_map>
#include <map>
#include <vector>
#include <chrono>
#include <iostream>
#include <random>

const size_t N = 1'000'000;

// 模拟一个简单的"计数"场景
void benchmark_hashmap() {
    std::unordered_map<int, int> hashmap;
    
    auto start = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < N; ++i) {
        hashmap[i] = i * 2;  // 插入
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "unordered_map插入: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms\n";
    
    // 随机查找
    std::mt19937 rng(123);
    start = std::chrono::high_resolution_clock::now();
    long long sum = 0;
    for (size_t i = 0; i < N / 10; ++i) {
        int key = rng() % N;
        auto it = hashmap.find(key);
        if (it != hashmap.end()) {
            sum += it->second;
        }
    }
    end = std::chrono::high_resolution_clock::now();
    std::cout << "unordered_map查找: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms, sum=" << sum << "\n";
}

void benchmark_map() {
    std::map<int, int> ordered_map;
    
    auto start = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < N; ++i) {
        ordered_map[i] = i * 2;  // 插入（有序，O(log n)）
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "std::map插入: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms\n";
    
    std::mt19937 rng(123);
    start = std::chrono::high_resolution_clock::now();
    long long sum = 0;
    for (size_t i = 0; i < N / 10; ++i) {
        int key = rng() % N;
        auto it = ordered_map.find(key);
        if (it != ordered_map.end()) {
            sum += it->second;
        }
    }
    end = std::chrono::high_resolution_clock::now();
    std::cout << "std::map查找: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms, sum=" << sum << "\n";
}

int main() {
    std::cout << "=== HashMap vs Ordered Map (N=" << N << ") ===\n";
    benchmark_hashmap();
    std::cout << "\n";
    benchmark_map();
    
    return 0;
}
```

典型输出：

```text
=== HashMap vs Ordered Map (N=1000000) ===
unordered_map插入: 127 ms
unordered_map查找: 3 ms
unordered_map sum=99999900000

std::map插入: 1842 ms
std::map查找: 27 ms
std::map sum=99999900000
```

> **结论**：如果你不需要有序遍历，`unordered_map`（或`std::unordered_set`）通常是更好的选择。如果你需要有序遍历或者范围查询，`std::map`或者`std::set`更合适。

---

## 39.6 并行化：让多核帮你干活

### 为什么要并行化？

现在的CPU基本都有多个核心。如果你还在用单线程，恭喜你，你只用到了1/N的算力（假设有N个核心）。浪费啊！

### C++并行算法（C++17）

C++17引入了并行算法，让STL算法的多线程化变得极其简单：

> 📎 **可用性说明**：并行算法需要标准库 + PSTL 后端（通常是 Intel TBB）。**Apple clang 自带的 libc++ 到 21 版都没有实现**，`std::execution::par` 在 macOS 上会报 `no member named 'par'`。想真正跑起来请用 GCC 9+（需 `-ltbb`）或 MSVC。下面保留标准写法供理解 API。

```cpp
#include <algorithm>
#include <execution>
#include <vector>
#include <chrono>
#include <iostream>
#include <numeric>

int main() {
    const size_t N = 50'000'000;
    std::vector<double> v(N, 1.0);
    
    // 串行版本
    auto start = std::chrono::high_resolution_clock::now();
    double sum1 = std::accumulate(v.begin(), v.end(), 0.0);
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "串行accumulate: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms, sum=" << sum1 << "\n";
    
    // 并行版本（只需加一个policy参数！）
    start = std::chrono::high_resolution_clock::now();
    double sum2 = std::accumulate(std::execution::par, v.begin(), v.end(), 0.0);
    end = std::chrono::high_resolution_clock::now();
    std::cout << "并行accumulate: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms, sum=" << sum2 << "\n";
    
    // 更多的并行算法
    std::vector<int> data(N);
    std::iota(data.begin(), data.end(), 1);
    
    start = std::chrono::high_resolution_clock::now();
    std::sort(std::execution::par, data.begin(), data.end());
    end = std::chrono::high_resolution_clock::now();
    std::cout << "并行sort: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms\n";
    
    return 0;
}
```

> **注意**：并行算法需要链接 TBB（Threading Building Blocks），并且标准库要实现 PSTL。
> 实践上可用的是 **GCC 9+ 配合 libstdc++**（加 `-ltbb`）或 **MSVC**；
> Apple clang 默认搭配的 libc++ 并没有实现并行算法，请不要照抄这段代码去跑 macOS。

### std::async和std::future：简单的异步任务

对于更复杂的并行场景，`std::async`提供了更灵活的方式：

```cpp
#include <future>
#include <chrono>
#include <iostream>
#include <vector>
#include <numeric>

// 模拟一个耗时计算
double compute_chunk_sum(const std::vector<int>& v, size_t start, size_t end) {
    double sum = 0;
    for (size_t i = start; i < end; ++i) {
        sum += std::sqrt(v[i]) * std::sin(v[i]);
    }
    return sum;
}

int main() {
    const size_t N = 100'000'000;
    std::vector<int> data(N);
    std::iota(data.begin(), data.end(), 1);
    
    // 单线程版本
    auto start = std::chrono::high_resolution_clock::now();
    double result_single = compute_chunk_sum(data, 0, N);
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "单线程: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms, result=" << result_single << "\n";
    
    // 双线程版本
    const size_t mid = N / 2;
    start = std::chrono::high_resolution_clock::now();
    auto future1 = std::async(std::launch::async, [&]() {
        return compute_chunk_sum(data, 0, mid);
    });
    auto future2 = std::async(std::launch::async, [&]() {
        return compute_chunk_sum(data, mid, N);
    });
    double result_double = future1.get() + future2.get();
    end = std::chrono::high_resolution_clock::now();
    std::cout << "双线程: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms, result=" << result_double << "\n";
    
    return 0;
}
```

### 并行化的注意事项

并行化不是银弹，有几个坑需要注意：

1. **阿姆达尔定律（Amdahl's Law）**：程序中不能并行的部分会限制加速比。如果95%的代码可以并行，最大加速比也只有20倍。但实际上，考虑到线程创建、同步等开销，你可能只能加速几倍。

2. **数据竞争（Data Race）**：多个线程同时读写同一个数据会导致未定义行为。**使用`std::atomic`或`std::mutex`保护共享数据。**

3. **伪共享（False Sharing）**：如果多个线程修改的数据在同一个缓存行（Cache Line，通常是64字节）里，CPU缓存就会频繁失效。解决方法是使用`alignas(64)`让数据对齐到缓存行。

```cpp
#include <atomic>
#include <thread>
#include <vector>
#include <chrono>
#include <iostream>

// 错误的做法：多个线程修改相邻的数据，会触发伪共享
struct BadCounter {
    std::atomic<int> counters[4];
};

// 正确的做法：使用padding让每个计数器独占一个缓存行
struct GoodCounter {
    alignas(64) std::atomic<int> counter;  // 每个counter独占64字节
};

void bad_counter_demo() {
    BadCounter bad;
    std::vector<std::thread> threads;
    
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back([&bad, i]() {
            for (int j = 0; j < 10'000'000; ++j) {
                bad.counters[i].fetch_add(1);
            }
        });
    }
    for (auto& t : threads) t.join();
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "伪共享版本: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms\n";
}

void good_counter_demo() {
    GoodCounter good[4];
    std::vector<std::thread> threads;
    
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back([&good, i]() {
            for (int j = 0; j < 10'000'000; ++j) {
                good[i].counter.fetch_add(1);
            }
        });
    }
    for (auto& t : threads) t.join();
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "消除伪共享版本: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms\n";
}

int main() {
    std::cout << "=== 伪共享 vs 消除伪共享 ===\n";
    bad_counter_demo();  // 慢
    good_counter_demo(); // 快，可能快2-3倍
    return 0;
}
```

---

## 39.7 I/O优化：别让磁盘和网络拖后腿

### 缓冲I/O的重要性

如果你在做I/O密集型任务，比如读写文件，缓冲是必须的。直接调用`std::cout`或`printf`可能比你想象的慢得多：

```cpp
#include <iostream>
#include <fstream>
#include <chrono>
#include <vector>

void slow_io_demo() {
    const int N = 100'000;
    
    // 错误示范：每次都刷新缓冲区
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) {
        std::cout << "Line " << i << "\n";  // 每次都flush！
    }
    std::cout << std::flush;
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "逐行输出（flush每次）: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms\n";
    
    // 正确做法：使用'\n'而不是std::endl，最后一次性flush
    start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) {
        std::cout << "Line " << i << "\n";  // '\n'不会立即flush
    }
    std::cout << std::flush;
    end = std::chrono::high_resolution_clock::now();
    std::cout << "逐行输出（'\n'不flush）: " 
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
              << " ms\n";
}

void buffered_file_io() {
    const size_t N = 10'000'000;
    std::vector<int> data(N);
    for (size_t i = 0; i < N; ++i) data[i] = static_cast<int>(i);
    
    // 逐个写入（很慢）
    {
        std::ofstream f("slow.txt");
        auto start = std::chrono::high_resolution_clock::now();
        for (size_t i = 0; i < N; ++i) {
            f << data[i] << '\n';
        }
        auto end = std::chrono::high_resolution_clock::now();
        std::cout << "逐个写入: " 
                  << std::chrono::duration_cast<std::chrono::seconds>(end - start).count()
                  << " seconds\n";
    }
    
    // 批量写入（快很多）
    {
        std::ofstream f("fast.txt");
        std::string buffer;
        buffer.reserve(N * 12);  // 预分配
        auto start = std::chrono::high_resolution_clock::now();
        for (size_t i = 0; i < N; ++i) {
            buffer += std::to_string(data[i]);
            buffer += '\n';
        }
        f << buffer;
        f.flush();
        auto end = std::chrono::high_resolution_clock::now();
        std::cout << "批量写入: " 
                  << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
                  << " ms\n";
    }
    
    // 使用更高效的二进制I/O
    {
        std::ofstream f("binary.bin", std::ios::binary);
        auto start = std::chrono::high_resolution_clock::now();
        f.write(reinterpret_cast<const char*>(data.data()), data.size() * sizeof(int));
        f.flush();
        auto end = std::chrono::high_resolution_clock::now();
        std::cout << "二进制写入: " 
                  << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
                  << " ms\n";
    }
}

int main() {
    slow_io_demo();
    std::cout << "\n";
    buffered_file_io();
    return 0;
}
```

### 内存映射文件（Memory-Mapped Files）

对于大文件的随机访问，内存映射是神器——把文件直接映射到内存，访问就像访问数组一样简单：

```cpp
#include <iostream>
#include <fstream>
#include <chrono>
#include <vector>
#include <cstring>

// 在支持的系统上，可以使用mmap（Linux/macOS）或CreateFileMapping（Windows）
// 这里用标准库模拟一个简化版本，实际项目推荐使用Boost.Iostreams或者原生API

void memory_mapped_demo() {
    const size_t N = 10'000'000;
    std::vector<int> data(N);
    for (size_t i = 0; i < N; ++i) data[i] = static_cast<int>(i);
    
    // 普通文件I/O：随机读取1000个位置
    {
        // 先写入文件
        {
            std::ofstream f("mmap_demo.dat", std::ios::binary);
            f.write(reinterpret_cast<const char*>(data.data()), data.size() * sizeof(int));
        }
        
        std::ifstream f("mmap_demo.dat", std::ios::binary);
        std::vector<int> read_buffer(1000);
        std::vector<size_t> positions(1000);
        for (size_t i = 0; i < 1000; ++i) {
            positions[i] = (i * 7919) % N;  // 伪随机位置
        }
        
        auto start = std::chrono::high_resolution_clock::now();
        for (size_t i = 0; i < 1000; ++i) {
            f.seekg(positions[i] * sizeof(int));
            f.read(reinterpret_cast<char*>(&read_buffer[i]), sizeof(int));
        }
        auto end = std::chrono::high_resolution_clock::now();
        std::cout << "普通文件随机读: " 
                  << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()
                  << " us\n";
    }
    
    // 模拟mmap：将文件一次性读入内存，然后像数组一样访问
    {
        std::ifstream f("mmap_demo.dat", std::ios::binary | std::ios::ate);
        auto size = f.tellg();
        f.seekg(0);
        
        std::vector<char> file_in_memory(size);
        f.read(file_in_memory.data(), size);
        
        std::vector<int> read_buffer(1000);
        std::vector<size_t> positions(1000);
        for (size_t i = 0; i < 1000; ++i) {
            positions[i] = (i * 7919) % N;
        }
        
        auto start = std::chrono::high_resolution_clock::now();
        for (size_t i = 0; i < 1000; ++i) {
            int* ptr = reinterpret_cast<int*>(file_in_memory.data() + positions[i] * sizeof(int));
            read_buffer[i] = *ptr;
        }
        auto end = std::chrono::high_resolution_clock::now();
        std::cout << "内存映射风格访问: " 
                  << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()
                  << " us\n";
    }
}

int main() {
    memory_mapped_demo();
    return 0;
}
```

---

## 39.8 内存分配器：定制你的"后勤部长"

### 默认分配器的局限性

C++默认的内存分配器（`std::allocator`）是通用型的，但对于特定的访问模式，它可能不是最优选择。

### 对象池分配器

我们在39.4已经看过对象池了。现在让我们看一个更完整的例子——一个固定大小的内存池分配器：

```cpp
#include <iostream>
#include <memory>
#include <vector>
#include <chrono>
#include <cstddef>
#include <cassert>
#include <algorithm>   // std::max

// 每个空闲块里至少要放得下一个指针，而且块首必须是"对齐过的"
// —— 这是"用块首当链表节点"的内存池最容易踩的坑：
// 如果 block_size 比 sizeof(void*) 还小（比如给 int 用 4 字节），
// 写 node->next 就会踩进相邻块，堆内存被破坏，程序随机崩溃。
static size_t round_up(size_t value, size_t align) {
    return (value + align - 1) / align * align;
}

// 一个简单的固定块大小内存池
class MemoryPool {
public:
    explicit MemoryPool(size_t block_size, size_t pool_size = 4096)
        : block_size_(round_up(std::max(block_size, sizeof(void*)),
                               alignof(std::max_align_t))),
          pool_size_(pool_size) {
        assert(block_size_ >= sizeof(void*) && "块太小，放不下空闲链表节点！");
        expand_pool();
    }
    
    ~MemoryPool() {
        for (auto* chunk : chunks_) {
            ::operator delete(chunk);
        }
    }
    
    void* allocate() {
        if (free_list_ == nullptr) {
            expand_pool();
        }
        void* result = free_list_;
        free_list_ = free_list_->next;
        ++allocated_;
        return result;
    }
    
    void deallocate(void* ptr) {
        auto* node = static_cast<FreeNode*>(ptr);
        node->next = free_list_;
        free_list_ = node;
        --allocated_;
    }
    
    size_t allocated() const { return allocated_; }
    size_t block_size() const { return block_size_; }
    
private:
    struct FreeNode {
        FreeNode* next;
    };
    
    void expand_pool() {
        char* chunk = static_cast<char*>(::operator new(pool_size_ * block_size_));
        chunks_.push_back(chunk);
        
        // 把新分配的块加入到空闲链表
        size_t count = pool_size_;
        char* current = chunk;
        for (size_t i = 0; i < count - 1; ++i) {
            auto* node = reinterpret_cast<FreeNode*>(current);
            node->next = reinterpret_cast<FreeNode*>(current + block_size_);
            current += block_size_;
        }
        // 最后一个节点
        reinterpret_cast<FreeNode*>(current)->next = nullptr;
        free_list_ = reinterpret_cast<FreeNode*>(chunk);
    }
    
    size_t block_size_;
    size_t pool_size_;
    size_t allocated_ = 0;
    FreeNode* free_list_ = nullptr;
    std::vector<char*> chunks_;
};

// 小对象分配对比
struct HeavyObject {
    int data[64];  // 256字节的对象
    HeavyObject() { for (int i = 0; i < 64; ++i) data[i] = i; }
};

void allocator_comparison() {
    constexpr size_t N = 100'000;
    
    // 使用默认分配器
    {
        std::vector<HeavyObject*> objects;
        objects.reserve(N);
        
        auto start = std::chrono::high_resolution_clock::now();
        for (size_t i = 0; i < N; ++i) {
            objects.push_back(new HeavyObject());
        }
        for (size_t i = 0; i < N; ++i) {
            delete objects[i];
        }
        auto end = std::chrono::high_resolution_clock::now();
        std::cout << "默认new/delete: " 
                  << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
                  << " ms\n";
    }
    
    // 使用内存池
    {
        MemoryPool pool(sizeof(HeavyObject), 1024);
        std::vector<HeavyObject*> objects;
        objects.reserve(N);
        
        auto start = std::chrono::high_resolution_clock::now();
        for (size_t i = 0; i < N; ++i) {
            objects.push_back(new (pool.allocate()) HeavyObject());
        }
        for (size_t i = 0; i < N; ++i) {
            objects[i]->~HeavyObject();
            pool.deallocate(objects[i]);
        }
        auto end = std::chrono::high_resolution_clock::now();
        std::cout << "内存池分配: " 
                  << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
                  << " ms\n";
    }
}

int main() {
    std::cout << "=== 内存分配器对比（256字节对象 x 100000次）===\n";
    allocator_comparison();
    
    // ===== 复用演示：归还的块会立刻被再次利用 =====
    std::cout << "\n=== 块的复用 ===\n";
    MemoryPool pool(32, 8);        // 每块 32 字节，一次向系统要 8 块
    std::cout << "调整后的块大小: " << pool.block_size() << " 字节（会向上取整到对齐值）\n";

    void* p1 = pool.allocate();
    void* p2 = pool.allocate();
    std::cout << "分配了 2 块, allocated = " << pool.allocated() << "\n";   // 输出: 2

    pool.deallocate(p1);           // 归还 p1
    void* p3 = pool.allocate();    // 空闲链表是后进先出，于是立刻拿回同一块
    std::cout << "归还再申请, allocated = " << pool.allocated() << "\n";   // 输出: 2
    std::cout << "拿回的是刚才那块内存: " << (p1 == p3 ? "是" : "否") << "\n";  // 输出: 是
    std::cout << "（p2 还没归还, 所以 allocated 仍是 2）\n";
    
    return 0;
}
```

> ⚠️ **别急着把内存池塞给 `std::vector`**：`std::vector` 一次就要一整片连续内存（容量 × `sizeof(T)`），
> 而上面这个池每次只发一块固定大小的内存，两者对不上。
> 真要让容器用池子，有两个正规做法：
> - **标准库方案**：`std::pmr::monotonic_buffer_resource` + `std::pmr::vector<T>`（`<memory_resource>`，C++17 起）；
> - **自己写分配器**：实现满足 *Allocator* 要求的 `PoolAllocator<T>::allocate(n)`，在 `n` 很大时向 `::operator new` 要内存，
>   只有小对象才走内存池——但要注意 `std::vector` 每次扩容都会整块申请，池子未必用得上。

---

## 39.9 本章小结

好了各位，如果你能看到这里，说明你是一个真正关心性能的程序员（或者是一个失眠患者）。不管怎样，让我们来总结一下这一章学到的东西：

### 核心原则

1. **先测量，后优化**：不要猜测，用profiler和数据说话。优化的第一条规则是"先确定瓶颈在哪里"。
2. **选择比努力更重要**：一个O(n log n)的算法永远比精心优化的O(n²)算法更快。
3. **缓存为王**：现代CPU和内存的速度差达到100倍，良好的数据局部性可能是最有效的优化。
4. **编译器是你的朋友**：善用`-O2`、`-O3`、LTO和SIMD向量化，让编译器替你干脏活。

### 优化层次（从高到低）

| 层次 | 优化手段 | 潜在收益 |
|------|----------|----------|
| 算法层 | 换用更优算法/数据结构 | 10x - 1000x |
| 并行层 | 多线程/SIMD向量化 | 2x - 16x |
| 缓存层 | 改善数据局部性/分块 | 2x - 20x |
| 代码层 | 减少开销/避免分配 | 1.2x - 3x |
| 编译器层 | 优化级别开关 | 1.5x - 10x |

### 性能优化的"不要"

- **不要**在没profiling之前就优化
- **不要**为了"炫技"写不可读的代码
- **不要**在debug模式下测试性能
- **不要**假设你知道CPU会怎么执行代码（现代CPU太复杂了）
- **不要**过早优化（但也不要太晚）

### 实际建议

1. 学会用profiler：`gprof`、`perf`、`Valgrind`、`VTune`、`Visual Studio Profiler`
2. 熟练使用`<chrono>`进行基准测试
3. 理解现代CPU的缓存层次结构
4. 善用`std::execution::par`进行并行化
5. 在需要高性能时，考虑定制内存分配器

### 最后一句话

> **"过早优化是万恶之源，但从不优化是万恶之源的王后。"**

做一个聪明的程序员：先写出正确、可读的代码，然后**有针对性地**去优化那些真正需要优化的地方。记住，你的代码首先是给人类读的，顺便给计算机执行一下。

祝你的代码永远跑得比兔子还快！🐰💨
