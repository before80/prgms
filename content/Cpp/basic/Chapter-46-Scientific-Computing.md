+++
title = "第46章 科学计算：C++的"数学家梦工厂""
weight = 460
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第46章 科学计算：C++的"数学家梦工厂"

> 🎯 章前语：你知道吗？天气预报、飞机设计、股票期权定价、核爆模拟——这些听起来高大上的东西，背后都是科学计算。而C++，就是那个在数学家和工程师之间"左右逢源"的硬核语言。它既有数学的优雅，又有机器的效率。难怪那些跑在超级计算机上的科学程序，十有八九都是C++写的。

## 46.1 科学计算概述：为什么C++是科学家的"梦中情语"

### 46.1.1 科学计算是个什么鬼？

科学计算（Scientific Computing）是利用计算机解决科学和工程中的数学问题。它不同于你写的那些"增删改查"业务代码——科学计算关心的是：

- **数值精度**：.double够不够？还是得祭出.long double？
- **计算稳定性**：一个微小的舍入误差会不会让结果跑出太阳系？
- **性能极限**：同样的算法，别人跑1小时，你能不能优化到10分钟？
- **并行扩展**：单核不够，能不能扩展到10000核？

**科学计算的应用战场：**
| 领域 | 典型问题 | C++贡献度 |
|------|----------|-----------|
| 计算流体力学（CFD） | 飞机翼型优化 | ⭐⭐⭐⭐⭐ |
| 有限元分析（FEA） | 大桥会不会塌 | ⭐⭐⭐⭐⭐ |
| 量子化学 | 分子轨道计算 | ⭐⭐⭐⭐⭐ |
| 机器学习/深度学习 | 神经网络训练 | ⭐⭐⭐⭐ |
| 金融工程 | 期权定价、风险评估 | ⭐⭐⭐⭐⭐ |
| 气候建模 | 全球变暖预测 | ⭐⭐⭐⭐⭐ |

### 46.1.2 C++凭什么成为科学计算扛把子？

科学家们可选的语言多了去了：Fortran（老而弥坚）、Python（方便但慢）、MATLAB（贵但专业）、Julia（新生代网红）。那C++凭什么杀出重围？

1. **性能碾压一切脚本语言**：Python跑一个矩阵分解要几天？C++可能只需要几小时。
2. **抽象不丢性能**：模板元编程让你写出"通用但零抽象成本"的代码。
3. **库生态丰富**：Eigen、LAPACK、PETSc、Boost.Odeint——全是现成的轮子。
4. **GPU支持好**：CUDA、ROCm、HIP，C++都能无缝对接。
5. **工业级成熟度**：航空航天、石油勘探、金融建模等领域几十年积累的C++代码库。

> 💡 Fortran的倔强：Fortran在科学计算界是"活化石"，很多超级计算机上的老代码都是Fortran的。但新一代科学家大多转向C++了——毕竟，谁想维护那些全是GOTO的1960年代代码呢？

### 46.1.3 科学计算的"Hello World"——还是那个朴素的一元二次方程

我们从最简单的开始热热身：

```cpp
// 46_01_quadratic.cpp
// 科学计算的Hello World——求根公式
#include <iostream>
#include <cmath>
#include <complex>

// 朴素版：直接套公式，但小心浮点陷阱！
std::pair<std::complex<double>, std::complex<double>> solveQuadratic_naive(
    double a, double b, double c) {
    double delta = b * b - 4 * a * c;
    std::complex<double> sqrt_delta = std::sqrt(std::complex<double>(delta, 0));
    std::complex<double> x1 = (-b + sqrt_delta) / (2 * a);
    std::complex<double> x2 = (-b - sqrt_delta) / (2 * a);
    return {x1, x2};
}

// 数值稳定版：利用共轭关系避免大数吃小数
std::pair<double, double> solveQuadratic_stable(double a, double b, double c) {
    if (a == 0) {
        throw std::invalid_argument("这不是二次方程！");
    }
    // 选一个数值上更稳定的公式分支
    double sign_b = (b >= 0) ? 1.0 : -1.0;
    double q = -0.5 * (b + sign_b * std::sqrt(b * b - 4 * a * c));
    double x1 = q / a;
    double x2 = c / q;
    // 保证 x1 >= x2
    if (x1 < x2) std::swap(x1, x2);
    return {x1, x2};
}

int main() {
    // 测试 case: x^2 - 1000.001x + 1 = 0
    // 根非常接近：~1000 和 ~0.001
    auto [x1, x2] = solveQuadratic_stable(1.0, -1000.001, 1.0);
    std::cout << std::fixed;
    std::cout << "数值稳定版根: x1 = " << x1 << ", x2 = " << x2 << "\n";
    
    // 验证
    std::cout << "验证: x1 + x2 = " << (x1 + x2) << " (应为 1000.001)\n";
    std::cout << "验证: x1 * x2 = " << (x1 * x2) << " (应为 1.0)\n";
    
    // 复数根测试
    auto [cx1, cx2] = solveQuadratic_naive(1.0, 1.0, 1.0);
    std::cout << "复数根测试: x^2 + x + 1 = 0\n";
    std::cout << "  x1 = " << cx1 << ", x2 = " << cx2 << "\n";
    
    return 0;
}
```

编译运行：
```bash
g++ -std=c++20 -O3 -o 46_01_quadratic 46_01_quadratic.cpp && ./46_01_quadratic
```

> ⚠️ 科学计算的"生死劫"：这个例子告诉我们，同样是套公式，数值稳定性可能就是"程序算得对"和"程序算到宇宙尽头"的区别。记住：**永远不要直接用 `(-b ± sqrt(b*b - 4*a*c)) / (2*a)` 这个公式！** 当b很大而a、c很小时，b*b会丢失4ac的贡献。

## 46.2 向量和矩阵：C++的"线性代数入门课"

### 46.2.1 手写向量和矩阵——从轮子造起

科学计算里最核心的数据结构就是向量和矩阵。虽然我们有Eigen这样的库，但理解底层原理很重要——万一哪天你需要在GPU上写矩阵乘法呢？

```cpp
// 46_02_vector_matrix.cpp
#include <iostream>
#include <vector>
#include <iomanip>
#include <cmath>
#include <stdexcept>

// ============ 向量类 ============
class Vec3 {
public:
    double x, y, z;
    
    Vec3() : x(0), y(0), z(0) {}
    Vec3(double x, double y, double z) : x(x), y(y), z(z) {}
    
    // 加法
    Vec3 operator+(const Vec3& v) const {
        return Vec3(x + v.x, y + v.y, z + v.z);
    }
    
    // 减法
    Vec3 operator-(const Vec3& v) const {
        return Vec3(x - v.x, y - v.y, z - v.z);
    }
    
    // 标量乘法
    Vec3 operator*(double s) const {
        return Vec3(x * s, y * s, z * s);
    }
    
    // 点积
    double dot(const Vec3& v) const {
        return x * v.x + y * v.y + z * v.z;
    }
    
    // 叉积
    Vec3 cross(const Vec3& v) const {
        return Vec3(
            y * v.z - z * v.y,
            z * v.x - x * v.z,
            x * v.y - y * v.x
        );
    }
    
    // 模长
    double norm() const {
        return std::sqrt(dot(*this));
    }
    
    // 归一化
    Vec3 normalized() const {
        double n = norm();
        if (n < 1e-12) throw std::runtime_error("零向量无法归一化！");
        return *this * (1.0 / n);
    }
    
    void print(const std::string& name) const {
        std::cout << std::fixed << std::setprecision(4);
        std::cout << name << " = (" << x << ", " << y << ", " << z << ")\n";
    }
};

// ============ 通用矩阵类（行优先） ============
class Matrix {
    int rows_, cols_;
    std::vector<double> data_;  // 行优先存储
    
public:
    Matrix(int rows, int cols, double init = 0.0) 
        : rows_(rows), cols_(cols), data_(rows * cols, init) {}
    
    int rows() const { return rows_; }
    int cols() const { return cols_; }
    
    double& at(int i, int j) { return data_[i * cols_ + j]; }
    double at(int i, int j) const { return data_[i * cols_ + j]; }
    
    // 矩阵乘法: this(m×k) * other(k×n) = result(m×n)
    Matrix operator*(const Matrix& other) const {
        if (cols_ != other.rows_) {
            throw std::invalid_argument("矩阵维度不匹配！");
        }
        Matrix result(rows_, other.cols_);
        
        // 朴素实现：O(m×n×k)
        for (int i = 0; i < rows_; ++i) {
            for (int j = 0; j < other.cols_; ++j) {
                double sum = 0.0;
                for (int k = 0; k < cols_; ++k) {
                    sum += at(i, k) * other.at(k, j);
                }
                result.at(i, j) = sum;
            }
        }
        return result;
    }
    
    // 矩阵-向量乘法
    std::vector<double> operator*(const std::vector<double>& vec) const {
        if ((int)vec.size() != cols_) {
            throw std::invalid_argument("向量维度与矩阵列数不匹配！");
        }
        std::vector<double> result(rows_, 0.0);
        for (int i = 0; i < rows_; ++i) {
            for (int j = 0; j < cols_; ++j) {
                result[i] += at(i, j) * vec[j];
            }
        }
        return result;
    }
    
    // 打印矩阵
    void print(const std::string& name) const {
        std::cout << name << " (" << rows_ << "×" << cols_ << "):\n";
        std::cout << std::fixed << std::setprecision(2);
        for (int i = 0; i < rows_; ++i) {
            std::cout << "  [";
            for (int j = 0; j < cols_; ++j) {
                std::cout << std::setw(8) << at(i, j);
                if (j < cols_ - 1) std::cout << ", ";
            }
            std::cout << "]\n";
        }
    }
    
    // 转置
    Matrix transpose() const {
        Matrix result(cols_, rows_);
        for (int i = 0; i < rows_; ++i) {
            for (int j = 0; j < cols_; ++j) {
                result.at(j, i) = at(i, j);
            }
        }
        return result;
    }
};

// ============ 主程序 ============
int main() {
    std::cout << "========== 向量运算演示 ==========\n";
    Vec3 v1(1.0, 2.0, 3.0);
    Vec3 v2(4.0, 5.0, 6.0);
    
    v1.print("v1");
    v2.print("v2");
    
    Vec3 v3 = v1 + v2;
    v3.print("v1 + v2");
    
    Vec3 v4 = v1 * 2.0;
    v4.print("v1 * 2.0");
    
    std::cout << "v1 · v2 = " << v1.dot(v2) << "\n";
    
    Vec3 v5 = v1.cross(v2);
    v5.print("v1 × v2 (叉积)");
    
    std::cout << "|v1| = " << v1.norm() << "\n";
    
    std::cout << "\n========== 矩阵运算演示 ==========\n";
    // 创建3×3矩阵
    Matrix A(3, 3);
    A.at(0, 0) = 1; A.at(0, 1) = 2; A.at(0, 2) = 3;
    A.at(1, 0) = 4; A.at(1, 1) = 5; A.at(1, 2) = 6;
    A.at(2, 0) = 7; A.at(2, 1) = 8; A.at(2, 2) = 10;
    A.print("A");
    
    // 创建向量
    std::vector<double> x = {1.0, 0.0, 0.0};
    auto y = A * x;
    std::cout << "A * [1,0,0]^T = [";
    for (size_t i = 0; i < y.size(); ++i) {
        std::cout << y[i];
        if (i < y.size() - 1) std::cout << ", ";
    }
    std::cout << "]^T\n";
    
    // 矩阵乘法
    Matrix B(3, 3);
    B.at(0, 0) = 1; B.at(0, 1) = 0; B.at(0, 2) = 0;
    B.at(1, 0) = 0; B.at(1, 1) = 1; B.at(1, 2) = 0;
    B.at(2, 0) = 0; B.at(2, 1) = 0; B.at(2, 2) = 1;
    B.print("B (单位矩阵)");
    
    auto C = A * B;  // A * I = A
    C.print("A * B");
    
    return 0;
}
```

### 46.2.2 Eigen库——"用了就回不去"的矩阵利器

手写矩阵虽然有助于理解，但生产环境还是用Eigen吧！它快、准、而且接口优雅到哭。

```cpp
// 46_03_eigen_demo.cpp
// 编译: g++ -std=c++20 -I/usr/include/eigen3 46_03_eigen_demo.cpp -o 46_03_eigen_demo
// Windows: g++ -std=c++20 -IC:\eigen 46_03_eigen_demo.cpp -o 46_03_eigen_demo
#include <iostream>
#include <Eigen/Dense>
#include <iomanip>

int main() {
    std::cout << std::fixed << std::setprecision(6);
    
    // ========== 向量 ==========
    Eigen::Vector3d v1(1.0, 2.0, 3.0);
    Eigen::Vector3d v2(4.0, 5.0, 6.0);
    
    std::cout << "v1 = " << v1.transpose() << "\n";
    std::cout << "v2 = " << v2.transpose() << "\n";
    std::cout << "v1 + v2 = " << (v1 + v2).transpose() << "\n";
    std::cout << "v1.dot(v2) = " << v1.dot(v2) << "\n";
    std::cout << "v1.cross(v2) = " << v1.cross(v2).transpose() << "\n";
    std::cout << "v1.norm() = " << v1.norm() << "\n";
    
    // ========== 矩阵 ==========
    Eigen::Matrix3d A;
    A << 1, 2, 3,
         4, 5, 6,
         7, 8, 10;
    
    Eigen::Matrix3d I = Eigen::Matrix3d::Identity();
    
    std::cout << "\nA =\n" << A << "\n";
    std::cout << "A^T =\n" << A.transpose() << "\n";
    std::cout << "A^-1 =\n" << A.inverse() << "\n";
    std::cout << "det(A) = " << A.determinant() << "\n";
    
    // ========== 解线性方程组 Ax = b ==========
    Eigen::Vector3d b(14.0, 32.0, 53.0);
    Eigen::Vector3d x = A.colPivHouseholderQr().solve(b);
    std::cout << "\n解 Ax = b, b = " << b.transpose() << "\n";
    std::cout << "x = " << x.transpose() << "\n";
    std::cout << "验证: Ax = " << (A * x).transpose() << "\n";
    
    // ========== 特征值分解 ==========
    Eigen::SelfAdjointEigenSolver<Eigen::Matrix3d> eigensolver(A);
    std::cout << "\nA的特征值:\n" << eigensolver.eigenvalues() << "\n";
    std::cout << "A的特征向量:\n" << eigensolver.eigenvectors() << "\n";
    
    // ========== 奇异值分解（SVD） ==========
    Eigen::Matrix3d B;
    B << 1, 2, 3,
         4, 5, 6,
         7, 8, 9;  // 秩亏矩阵
    
    Eigen::JacobiSVD<Eigen::Matrix3d> svd(B, Eigen::ComputeFullU | Eigen::ComputeFullV);
    std::cout << "\n奇异值:\n" << svd.singularValues() << "\n";
    std::cout << "B的秩 = " << svd.rank() << "\n";
    
    // ========== 动态大小矩阵 ==========
    Eigen::MatrixXd big(5, 5);
    big.setRandom();
    std::cout << "\n5×5随机矩阵:\n" << big << "\n";
    std::cout << "范数: " << big.norm() << "\n";
    
    return 0;
}
```

> 💡 Eigen使用指南：
> - **默认double**；需要float或高精度.long double可以改模板参数
> - **解线性方程组用`colPivHouseholderQr()`**：数值稳定又快
> - **求特征值用`SelfAdjointEigenSolver`**：对称矩阵专用，快到飞起
> - **SVD用`JacobiSVD`**：最稳定，但大矩阵可能慢

## 46.3 数值方法：数学公式的"C++化身"

### 46.3.1 方程求根：牛顿法与二分法的"速度与激情"

**问题**：求 $f(x) = 0$ 的根。比如：$f(x) = x^3 - x - 1$ 的根在哪里？

```cpp
// 46_04_root_finding.cpp
#include <iostream>
#include <cmath>
#include <functional>
#include <iomanip>
#include <algorithm>

// ========== 二分法 ==========
// 简单粗暴，但收敛慢（线性收敛）
// 适用于：连续函数，且区间两端异号
double bisection(std::function<double(double)> f, 
                 double a, double b, 
                 double tol = 1e-10, int max_iter = 1000) {
    if (f(a) * f(b) >= 0) {
        throw std::invalid_argument("区间两端必须异号！");
    }
    
    double c = a;
    for (int i = 0; i < max_iter; ++i) {
        c = (a + b) / 2.0;
        double fc = f(c);
        
        if (std::abs(fc) < tol || (b - a) / 2.0 < tol) {
            std::cout << "二分法: 迭代 " << i << " 次收敛\n";
            return c;
        }
        
        if (fc * f(a) < 0) {
            b = c;
        } else {
            a = c;
        }
    }
    std::cout << "二分法: 达到最大迭代次数\n";
    return c;
}

// ========== 牛顿法 ==========
// 收敛快（二次收敛），但需要导数，且可能发散
// x_{n+1} = x_n - f(x_n) / f'(x_n)
double newton(std::function<double(double)> f,
             std::function<double(double)> df,
             double x0,
             double tol = 1e-10, int max_iter = 100) {
    double x = x0;
    
    for (int i = 0; i < max_iter; ++i) {
        double fx = f(x);
        double dfx = df(x);
        
        if (std::abs(dfx) < 1e-14) {
            throw std::runtime_error("导数接近零，牛顿法失败！");
        }
        
        double dx = fx / dfx;
        x -= dx;
        
        if (std::abs(dx) < tol) {
            std::cout << "牛顿法: 迭代 " << i << " 次收敛\n";
            return x;
        }
    }
    std::cout << "牛顿法: 达到最大迭代次数\n";
    return x;
}

// ========== 简化牛顿法（不需要导数） ==========
// 用数值导数近似：f'(x) ≈ f(x+eps) - f(x)) / eps
double secant(std::function<double(double)> f,
              double x0, double x1,
              double tol = 1e-10, int max_iter = 100) {
    double x = x1;
    double x_prev = x0;
    
    for (int i = 0; i < max_iter; ++i) {
        double fx = f(x);
        double fx_prev = f(x_prev);
        double denom = fx - fx_prev;
        
        if (std::abs(denom) < 1e-14) {
            throw std::runtime_error("函数值差太小，割线法失败！");
        }
        
        double x_new = x - fx * (x - x_prev) / denom;
        x_prev = x;
        x = x_new;
        
        if (std::abs(f(x)) < tol) {
            std::cout << "割线法: 迭代 " << i << " 次收敛\n";
            return x;
        }
    }
    std::cout << "割线法: 达到最大迭代次数\n";
    return x;
}

// ========== 主程序 ==========
int main() {
    std::cout << std::setprecision(12);
    
    // 目标函数: x^3 - x - 1 = 0
    // 真实根约为 1.324717957244746
    auto f = [](double x) { return x * x * x - x - 1.0; };
    auto df = [](double x) { return 3.0 * x * x - 1.0; };
    
    std::cout << "========== 方程求根: x^3 - x - 1 = 0 ==========\n";
    std::cout << "真实根（参考）: 1.324717957244746...\n\n";
    
    // 二分法
    double x_bisect = bisection(f, 1.0, 2.0);
    std::cout << "二分法结果: " << x_bisect << "\n";
    std::cout << "残差: |f(x)| = " << std::abs(f(x_bisect)) << "\n\n";
    
    // 牛顿法
    try {
        double x_newton = newton(f, df, 1.5);
        std::cout << "牛顿法结果: " << x_newton << "\n";
        std::cout << "残差: |f(x)| = " << std::abs(f(x_newton)) << "\n\n";
    } catch (const std::exception& e) {
        std::cout << "牛顿法失败: " << e.what() << "\n\n";
    }
    
    // 割线法
    try {
        double x_secant = secant(f, 1.0, 2.0);
        std::cout << "割线法结果: " << x_secant << "\n";
        std::cout << "残差: |f(x)| = " << std::abs(f(x_secant)) << "\n\n";
    } catch (const std::exception& e) {
        std::cout << "割线法失败: " << e.what() << "\n\n";
    }
    
    // ========== 再来一个: sin(x) = x/10 ==========
    std::cout << "========== 方程求根: sin(x) = x/10 ==========\n";
    auto g = [](double x) { return std::sin(x) - x / 10.0; };
    
    double x_g = bisection(g, 0.0, 5.0);
    std::cout << "二分法结果: " << x_g << "\n";
    std::cout << "验证: sin(" << x_g << ") = " << std::sin(x_g) 
              << ", " << x_g << "/10 = " << x_g/10 << "\n";
    
    return 0;
}
```

**三种方法的对比：**

| 方法 | 收敛速度 | 优点 | 缺点 |
|------|---------|------|------|
| 二分法 | 线性（每次精度翻倍） | 100%稳定，保证收敛 | 慢，需要区间 |
| 牛顿法 | 二次（精度平方增长） | 极快 | 需要导数，可能发散 |
| 割线法 | 超线性（≈1.618阶） | 不需导数，也较快 | 比牛顿法慢一点 |

### 46.3.2 数值积分：蒙特卡洛方法的"随机之美"

**问题**：求 $\int_a^b f(x) dx$。当解析积分不可能时，我们就得上数值积分了。

```cpp
// 46_05_numerical_integration.cpp
#include <iostream>
#include <cmath>
#include <functional>
#include <random>
#include <iomanip>
#include <chrono>

// ========== 梯形法则 ==========
// 简单但精度低：O(h^2)
double trapezoidal(std::function<double(double)> f, 
                   double a, double b, int n = 1000) {
    double h = (b - a) / n;
    double sum = f(a) + f(b);  // 端点权重为1
    for (int i = 1; i < n; ++i) {
        sum += 2.0 * f(a + i * h);  // 内点权重为2
    }
    return sum * h / 2.0;
}

// ========== 辛普森法则 ==========
// 精度高：O(h^4)，适合光滑函数
double simpson(std::function<double(double)> f,
               double a, double b, int n = 1000) {
    if (n % 2 == 1) n++;  // n必须是偶数
    double h = (b - a) / n;
    double sum = f(a) + f(b);  // 端点
    
    for (int i = 1; i < n; i += 2) {
        sum += 4.0 * f(a + i * h);  // 奇数点权重为4
    }
    for (int i = 2; i < n - 1; i += 2) {
        sum += 2.0 * f(a + i * h);  // 偶数点权重为2
    }
    return sum * h / 3.0;
}

// ========== 自适应积分 ==========
// 递归细分，直到达到精度要求
double adaptiveSimpson(std::function<double(double)> f,
                       double a, double b, 
                       double tol = 1e-10, 
                       int maxDepth = 50) {
    // 完整实现：递归地对子区间细分
    auto simpsonHelper = [&](auto&& self, double a, double b, 
                             double fa, double fm, double fb,
                             double whole, double tol, int depth) -> double {
        double m = (a + b) / 2.0;
        double h = b - a;
        double left  = h / 6.0 * (fa + 4.0 * fm + fb);
        
        if (depth >= maxDepth) {
            return left;  // 达到最大深度，返回近似值
        }
        
        double lm = (a + m) / 2.0;
        double rm = (m + b) / 2.0;
        double flm = f(lm);
        double frm = f(rm);
        
        double leftVal  = (m - a) / 6.0 * (fa + 4.0 * flm + fm);
        double rightVal = (b - m) / 6.0 * (fm + 4.0 * frm + fb);
        double combined = leftVal + rightVal;
        
        if (std::abs(combined - whole) <= 15.0 * tol) {
            // 误差足够小，使用Richardson外推改进
            return combined + (combined - whole) / 15.0;
        }
        
        // 继续细分
        return self(self, a, m, fa, flm, fm, leftVal, tol / 2.0, depth + 1) +
               self(self, m, b, fm, frm, fb, rightVal, tol / 2.0, depth + 1);
    };
    
    double fa = f(a);
    double fb = f(b);
    double fm = f((a + b) / 2.0);
    double whole = (b - a) / 6.0 * (fa + 4.0 * fm + fb);
    
    return simpsonHelper(simpsonHelper, a, b, fa, fm, fb, whole, tol, 0);
}

// ========== 蒙特卡洛积分 ==========
// 利用随机采样求积分
// 精度: O(1/sqrt(N))，与维度无关！
// 适合高维积分！
double monteCarloIntegral(std::function<double(double)> f,
                          double a, double b, int N = 1000000) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(a, b);
    
    double sum = 0.0;
    for (int i = 0; i < N; ++i) {
        double x = dis(gen);
        sum += f(x);
    }
    return (b - a) * sum / N;
}

// 多维蒙特卡洛（以2D为例）
double monteCarlo2D(std::function<double(double, double)> f,
                    double xmin, double xmax,
                    double ymin, double ymax,
                    int N = 1000000) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> disx(xmin, xmax);
    std::uniform_real_distribution<> disy(ymin, ymax);
    
    double sum = 0.0;
    for (int i = 0; i < N; ++i) {
        double x = disx(gen);
        double y = disy(gen);
        sum += f(x, y);
    }
    double area = (xmax - xmin) * (ymax - ymin);
    return area * sum / N;
}

// ========== 主程序 ==========
int main() {
    auto start = std::chrono::high_resolution_clock::now();
    
    std::cout << std::setprecision(12);
    
    // 测试1: ∫₀¹ e^(-x²) dx = sqrt(pi)/2 * erf(1)
    // 真实值 ≈ 0.746824132812427
    auto gauss = [](double x) { return std::exp(-x * x); };
    double true_val = std::sqrt(std::acos(-1.0)) / 2.0 * std::erf(1.0);
    
    std::cout << "========== ∫₀¹ e^(-x²) dx ==========\n";
    std::cout << "真实值: " << true_val << "\n\n";
    
    std::cout << "梯形法则 (n=1000):   " << trapezoidal(gauss, 0, 1, 1000) << "\n";
    std::cout << "                     误差: " 
              << std::abs(trapezoidal(gauss, 0, 1, 1000) - true_val) << "\n\n";
    
    std::cout << "辛普森法则 (n=1000): " << simpson(gauss, 0, 1, 1000) << "\n";
    std::cout << "                     误差: " 
              << std::abs(simpson(gauss, 0, 1, 1000) - true_val) << "\n\n";
    
    std::cout << "辛普森法则 (n=10000): " << simpson(gauss, 0, 1, 10000) << "\n";
    std::cout << "                     误差: " 
              << std::abs(simpson(gauss, 0, 1, 10000) - true_val) << "\n\n";
    
    std::cout << "蒙特卡洛 (N=1e6):     " << monteCarloIntegral(gauss, 0, 1, 1000000) << "\n";
    std::cout << "                     误差: " 
              << std::abs(monteCarloIntegral(gauss, 0, 1, 1000000) - true_val) << "\n\n";
    
    // 测试2: 二维积分 ∫₀¹∫₀¹ sin(x+y) dxdy
    auto sin2d = [](double x, double y) { return std::sin(x + y); };
    // 解析解: [1 - cos(2)]/2 ≈ 0.429203673205103
    double true2d = (1.0 - std::cos(2.0)) / 2.0;
    std::cout << "========== ∫₀¹∫₀¹ sin(x+y) dxdy ==========\n";
    std::cout << "真实值: " << true2d << "\n";
    std::cout << "蒙特卡洛 2D: " << monteCarlo2D(sin2d, 0, 1, 0, 1, 1000000) << "\n";
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "\n耗时: " << duration.count() << " ms\n";
    
    return 0;
}
```

> 💡 积分方法选用指南：
> - **一维光滑函数**：`simpson`就够用了，精度高速度快
> - **震荡函数**（如sin(x)/x）：用自适应积分或者FFT方法
> - **高维积分**：蒙特卡洛是唯一出路！其他方法复杂度随维度指数爆炸
> - **金融期权定价**：蒙特卡洛几乎是标配

### 46.3.3 常微分方程（ODE）数值解：RK4的"四阶魔法"

**问题**：已知 $y'(t) = f(t, y)$，$y(t_0) = y_0$，求 $y(t)$。

```cpp
// 46_06_ode_solver.cpp
#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>
#include <fstream>

// ========== 通用ODE求解器框架 ==========
struct ODESolution {
    std::vector<double> t;
    std::vector<std::vector<double>> y;  // y[i][dim]
    
    void add(double time, const std::vector<double>& state) {
        t.push_back(time);
        y.push_back(state);
    }
};

// ========== 4阶龙格-库塔法（RK4） ==========
// 工业标准！精度高，稳定又好用
// 注意：这是单个状态的版本
std::pair<std::vector<double>, std::vector<std::vector<double>>> 
rk4_integrate(std::function<std::vector<double>(double, const std::vector<double>&)> f,
               std::vector<double> y0,
               double t0, double t1, double dt,
               bool record = true) {
    std::vector<double> times;
    std::vector<std::vector<double>> states;
    
    double t = t0;
    std::vector<double> y = y0;
    
    if (record) {
        times.push_back(t);
        states.push_back(y);
    }
    
    int steps = static_cast<int>((t1 - t0) / dt);
    
    for (int i = 0; i < steps; ++i) {
        // RK4的四个斜率
        std::vector<double> k1 = f(t, y);
        
        std::vector<double> y2(y.size());
        for (size_t j = 0; j < y.size(); ++j) {
            y2[j] = y[j] + k1[j] * dt / 2.0;
        }
        std::vector<double> k2 = f(t + dt / 2.0, y2);
        
        std::vector<double> y3(y.size());
        for (size_t j = 0; j < y.size(); ++j) {
            y3[j] = y[j] + k2[j] * dt / 2.0;
        }
        std::vector<double> k3 = f(t + dt / 2.0, y3);
        
        std::vector<double> y4(y.size());
        for (size_t j = 0; j < y.size(); ++j) {
            y4[j] = y[j] + k3[j] * dt;
        }
        std::vector<double> k4 = f(t + dt, y4);
        
        // 加权组合
        for (size_t j = 0; j < y.size(); ++j) {
            y[j] += dt / 6.0 * (k1[j] + 2*k2[j] + 2*k3[j] + k4[j]);
        }
        
        t += dt;
        
        if (record) {
            times.push_back(t);
            states.push_back(y);
        }
    }
    
    return {times, states};
}

// ========== 例题1: 简谐振子 ==========
// y'' = -y, y(0)=0, y'(0)=1
// 解: y = sin(t)
std::vector<double> harmonicOscillator(double t, const std::vector<double>& state) {
    // state = [y, y']
    return {state[1], -state[0]};  // return [y', y'']
}

// ========== 例题2: 洛伦兹吸引子 ==========
// dx/dt = σ(y - x)
// dy/dt = x(ρ - z) - y  
// dz/dt = xy - βz
// σ=10, ρ=28, β=8/3 (经典混沌参数)
std::vector<double> lorenzAttractor(double t, const std::vector<double>& state) {
    double sigma = 10.0;
    double rho = 28.0;
    double beta = 8.0 / 3.0;
    
    double x = state[0], y = state[1], z = state[2];
    return {
        sigma * (y - x),
        x * (rho - z) - y,
        x * y - beta * z
    };
}

// ========== 例题3: 药物动力学（单室模型） ==========
// dC/dt = -k * C, C(0) = C0
// 解: C(t) = C0 * exp(-kt)
std::vector<double> drugPK(double t, const std::vector<double>& state) {
    double k = 0.1;  // 消除速率常数 (1/hour)
    return {-k * state[0]};  // C' = -kC
}

// ========== 主程序 ==========
int main() {
    std::cout << std::fixed << std::setprecision(8);
    
    // ========== 测试1: 简谐振子 ==========
    std::cout << "========== 简谐振子 y'' = -y ==========\n";
    std::cout << "解析解: y(t) = sin(t)\n\n";
    
    auto [t1, y1] = rk4_integrate(harmonicOscillator, {0.0, 1.0}, 0.0, 10.0, 0.01);
    
    // 打印前几个和最后几个
    std::cout << "t=0.00: y=" << y1[0][0] << ", y'=" << y1[0][1] << "\n";
    std::cout << "t=0.25: y=" << y1[25][0] << ", 解析=" << std::sin(0.25) << "\n";
    std::cout << "t=0.50: y=" << y1[50][0] << ", 解析=" << std::sin(0.50) << "\n";
    std::cout << "t=1.00: y=" << y1[100][0] << ", 解析=" << std::sin(1.00) << "\n";
    std::cout << "t=2.00: y=" << y1[200][0] << ", 解析=" << std::sin(2.00) << "\n";
    
    // 计算误差
    double max_error = 0.0;
    for (size_t i = 0; i < y1.size(); ++i) {
        double error = std::abs(y1[i][0] - std::sin(t1[i]));
        max_error = std::max(max_error, error);
    }
    std::cout << "最大误差: " << max_error << "\n";
    
    // ========== 测试2: 洛伦兹吸引子 ==========
    std::cout << "\n========== 洛伦兹吸引子 (混沌系统) ==========\n";
    auto [t2, y2] = rk4_integrate(lorenzAttractor, {1.0, 0.0, 0.0}, 0.0, 25.0, 0.01);
    
    std::cout << "t=0,   x=" << y2[0][0] << ", y=" << y2[0][1] << ", z=" << y2[0][2] << "\n";
    std::cout << "t=10,  x=" << y2[1000][0] << ", y=" << y2[1000][1] << ", z=" << y2[1000][2] << "\n";
    std::cout << "t=20,  x=" << y2[2000][0] << ", y=" << y2[2000][1] << ", z=" << y2[2000][2] << "\n";
    std::cout << "t=25,  x=" << y2[2500][0] << ", y=" << y2[2500][1] << ", z=" << y2[2500][2] << "\n";
    std::cout << "\n（注意：初值微小的变化会导致完全不同的轨迹——蝴蝶效应！）\n";
    
    // ========== 测试3: 药物动力学 ==========
    std::cout << "\n========== 药物动力学: dC/dt = -0.1*C ==========\n";
    std::cout << "解析解: C(t) = C0 * exp(-0.1t)\n\n";
    
    auto [t3, y3] = rk4_integrate(drugPK, {100.0}, 0.0, 24.0, 0.1);
    
    for (int i = 0; i < (int)t3.size(); i += 50) {
        double analytical = 100.0 * std::exp(-0.1 * t3[i]);
        std::cout << "t=" << std::setw(5) << t3[i] 
                  << "h: C=" << y3[i][0] 
                  << " (解析=" << analytical 
                  << ", 误差=" << std::abs(y3[i][0] - analytical) << ")\n";
    }
    std::cout << "\n24小时后药物浓度降至 " << y3.back()[0] << " (原为100)\n";
    
    return 0;
}
```

> 💡 ODE求解器选用指南：
> - **RK4（龙格-库塔4阶）**：大多数情况首选，稳定、快速、精度够用
> - **自适应步长**：当解变化剧烈时自动缩小步长，适合刚性问题
> - **隐式方法**：刚性系统（如化学反应、控制理论）需要用隐式RK或Gear方法

## 46.4 快速傅里叶变换（FFT）：频域分析的"神器"

### 46.4.1 从DFT到FFT——算法的"弯道超车"

FFT是科学计算中最伟大的算法之一——它将离散傅里叶变换的计算复杂度从 $O(n^2)$ 降到 $O(n \log n)$。

```cpp
// 46_07_fft.cpp
#include <iostream>
#include <vector>
#include <complex>
#include <cmath>
#include <algorithm>
#include <iomanip>

const double PI = std::acos(-1.0);

// ========== Cooley-Tukey FFT（递归版） ==========
// 输入: 时域信号
// 输出: 频域复数序列
void fft(std::complex<double>* x, int n) {
    if (n <= 1) return;
    
    // 分治：奇偶分离
    std::vector<std::complex<double>> even(n/2);
    std::vector<std::complex<double>> odd(n/2);
    
    for (int i = 0; i < n/2; ++i) {
        even[i] = x[2*i];
        odd[i] = x[2*i + 1];
    }
    
    // 递归FFT
    fft(even.data(), n/2);
    fft(odd.data(), n/2);
    
    // 合并：蝶形运算
    for (int i = 0; i < n/2; ++i) {
        double angle = -2.0 * PI * i / n;
        std::complex<double> t = std::exp(std::complex<double>(0, angle)) * odd[i];
        x[i] = even[i] + t;
        x[i + n/2] = even[i] - t;
    }
}

// ========== 逆FFT ==========
void ifft(std::complex<double>* x, int n) {
    // 逆FFT就是共轭后FFT再除以n
    for (int i = 0; i < n; ++i) {
        x[i] = std::conj(x[i]);
    }
    fft(x, n);
    for (int i = 0; i < n; ++i) {
        x[i] = std::conj(x[i]) / static_cast<double>(n);
    }
}

// ========== 生成测试信号 ==========
std::vector<std::complex<double>> generateSignal(double duration, double fs) {
    int n = static_cast<int>(duration * fs);
    std::vector<std::complex<double>> signal(n);
    
    double f1 = 50.0;   // 50 Hz 信号
    double f2 = 120.0;  // 120 Hz 噪声
    double f3 = 17.0;   // 17 Hz 低频干扰
    
    for (int i = 0; i < n; ++i) {
        double t = i / fs;
        double value = 
            3.0 * std::sin(2.0 * PI * f1 * t) +  // 50Hz, 幅值3
            1.0 * std::sin(2.0 * PI * f2 * t) +  // 120Hz, 幅值1  
            0.5 * std::sin(2.0 * PI * f3 * t);   // 17Hz, 幅值0.5
        signal[i] = std::complex<double>(value, 0);
    }
    
    return signal;
}

// ========== 计算幅度谱 ==========
std::vector<double> amplitudeSpectrum(const std::vector<std::complex<double>>& X) {
    int n = X.size();
    std::vector<double> amp(n);
    for (int i = 0; i < n; ++i) {
        amp[i] = std::abs(X[i]) * 2.0 / n;  // 归一化
    }
    return amp;
}

// ========== 主程序 ==========
int main() {
    std::cout << std::fixed << std::setprecision(4);
    
    double fs = 1000.0;        // 采样率 1000 Hz
    double duration = 1.0;    // 信号时长 1 秒
    int n = static_cast<int>(duration * fs);
    
    std::cout << "========== FFT 频谱分析演示 ==========\n";
    std::cout << "采样率: " << fs << " Hz, 采样点数: " << n << "\n";
    std::cout << "频率分辨率: " << fs/n << " Hz\n\n";
    
    // 生成信号
    auto signal = generateSignal(duration, fs);
    
    // 复制一份做FFT
    std::vector<std::complex<double>> X = signal;
    
    // 执行FFT
    fft(X.data(), n);
    
    // 计算幅度谱
    auto amp = amplitudeSpectrum(X);
    
    // 只看正频率部分（0 到 Nyquist）
    int half = n / 2;
    
    // 找峰值频率
    double max_amp = 0;
    int max_idx = 0;
    for (int i = 1; i < half; ++i) {  // 跳过DC分量
        if (amp[i] > max_amp) {
            max_amp = amp[i];
            max_idx = i;
        }
    }
    double peak_freq = max_idx * fs / n;
    std::cout << "检测到的峰值频率: " << peak_freq << " Hz (幅值: " << max_amp << ")\n";
    std::cout << "（应该是 50 Hz，幅值 3.0）\n\n";
    
    // 打印前几个峰值
    std::cout << "幅度谱（只显示 > 0.3 的频率分量）:\n";
    for (int i = 1; i < half; ++i) {
        double freq = i * fs / n;
        if (amp[i] > 0.3) {
            std::cout << "  f = " << std::setw(6) << freq << " Hz, 幅值 = " << amp[i] << "\n";
        }
    }
    
    // 逆FFT验证
    std::cout << "\n========== 逆FFT验证 ==========\n";
    std::vector<std::complex<double>> X_copy = X;
    ifft(X_copy.data(), n);
    
    std::cout << "原始信号第一个点: " << signal[0].real() << "\n";
    std::cout << "逆FFT后第一个点: " << X_copy[0].real() << "\n";
    std::cout << "误差: " << std::abs(signal[0].real() - X_copy[0].real()) << "\n";
    
    return 0;
}
```

> 💡 FFT实用技巧：
> - **N必须是2的幂**：如果不是，补零到最近的2的幂
> - **频率分辨率** = 采样率 / 采样点数，想要高分辨率？延长采样时间！
> - **加窗函数**：矩形窗外加Hanning或Hamming窗可以减少频谱泄漏
> - **复数信号直接FFT**：实数信号会得到对称的频谱，只分析前半部分即可

## 46.5 随机数与蒙特卡洛方法："骰子"统治世界

### 46.5.1 随机数生成器：科学计算的"掷骰子"

```cpp
// 46_08_random.cpp
#include <iostream>
#include <random>
#include <vector>
#include <algorithm>
#include <numeric>
#include <iomanip>
#include <map>

// ========== 均匀分布 ==========
void demo_uniform() {
    std::random_device rd;
    std::mt19937 gen(rd());  // Mersenne Twister 随机数生成器
    
    std::uniform_real_distribution<double> dis(0.0, 1.0);
    
    std::cout << "10个 [0, 1) 均匀随机数:\n";
    for (int i = 0; i < 10; ++i) {
        std::cout << dis(gen) << " ";
    }
    std::cout << "\n\n";
}

// ========== 正态分布（Box-Muller变换） ==========
void demo_normal() {
    std::random_device rd;
    std::mt19937 gen(rd());
    
    std::normal_distribution<double> dis(0.0, 1.0);  // 均值0，标准差1
    
    std::cout << "10个 N(0,1) 正态随机数:\n";
    for (int i = 0; i < 10; ++i) {
        std::cout << std::setprecision(4) << dis(gen) << " ";
    }
    std::cout << "\n\n";
}

// ========== 用蒙特卡洛估算π ==========
// 单位圆内切于正方形 [-1,1]×[-1,1]
// 面积比 = π/4
// 所以 π ≈ 4 * (圆内点数 / 总点数)
double estimate_pi(int n) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dis(-1.0, 1.0);
    
    int inside = 0;
    for (int i = 0; i < n; ++i) {
        double x = dis(gen);
        double y = dis(gen);
        if (x*x + y*y <= 1.0) {
            inside++;
        }
    }
    return 4.0 * inside / n;
}

// ========== 用重要性采样估算积分 ==========
// 估算 ∫₀^∞ x² * exp(-x) dx = 2
// 用重要性采样：选择 g(x) = exp(-x) (指数分布)
// f(x)/g(x) = x²
double estimate_integral重要性采样(int n) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::exponential_distribution<double> dist(1.0);  // 参数λ=1的指数分布
    
    double sum = 0.0;
    for (int i = 0; i < n; ++i) {
        double x = dist(gen);  // 从指数分布采样
        sum += x * x;          // f(x)/g(x) = x²
    }
    return sum / n;  // E[x²] under g
}

// ========== 主程序 ==========
int main() {
    std::cout << std::fixed << std::setprecision(6);
    
    std::cout << "========== 随机数生成 ==========\n";
    demo_uniform();
    demo_normal();
    
    std::cout << "========== 蒙特卡洛估算π ==========\n";
    std::cout << "真实π = " << std::acos(-1.0) << "\n";
    
    std::vector<int> sample_sizes = {100, 1000, 10000, 100000, 1000000};
    for (int n : sample_sizes) {
        double pi_est = estimate_pi(n);
        std::cout << "N = " << std::setw(10) << n 
                  << " → π ≈ " << pi_est 
                  << " (误差: " << std::abs(pi_est - std::acos(-1.0)) << ")\n";
    }
    
    std::cout << "\n========== 重要性采样估算∫x²e^(-x)dx ==========\n";
    std::cout << "真实值 = 2.0\n";
    for (int n : {100, 1000, 10000, 100000}) {
        std::cout << "N = " << std::setw(10) << n 
                  << " → 积分 ≈ " << estimate_integral重要性采样(n) << "\n";
    }
    
    return 0;
}
```

### 46.5.2 金融蒙特卡洛：期权的蒙特卡洛定价

```cpp
// 46_09_finance_monte_carlo.cpp
#include <iostream>
#include <random>
#include <vector>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <chrono>

// ========== Black-Scholes期权定价（解析解，用于对比） ==========
// 假设股票价格遵循几何布朗运动
// dS = μS dt + σS dW
// 看涨期权价格 = S0*N(d1) - K*e^(-rT)*N(d2)
double blackScholesCall(double S0, double K, double r, double sigma, double T) {
    double d1 = (std::log(S0/K) + (r + 0.5*sigma*sigma)*T) / (sigma*std::sqrt(T));
    double d2 = d1 - sigma * std::sqrt(T);
    
    // 标准正态分布的CDF
    auto normCDF = [](double x) {
        return 0.5 * std::erfc(-x * M_SQRT1_2);
    };
    
    return S0 * normCDF(d1) - K * std::exp(-r*T) * normCDF(d2);
}

// ========== 蒙特卡洛期权定价 ==========
// 使用几何布朗运动路径模拟
double monteCarloCall(double S0, double K, double r, double sigma, 
                      double T, int numPaths, int numSteps) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<double> dist(0.0, 1.0);
    
    double dt = T / numSteps;
    double drift = (r - 0.5 * sigma * sigma) * dt;
    double diffusion = sigma * std::sqrt(dt);
    
    double sumPayoff = 0.0;
    
    for (int i = 0; i < numPaths; ++i) {
        double S = S0;
        
        // 模拟路径
        for (int j = 0; j < numSteps; ++j) {
            double Z = dist(gen);
            S *= std::exp(drift + diffusion * Z);
        }
        
        // 计算payoff
        double payoff = std::max(S - K, 0.0);
        sumPayoff += payoff;
    }
    
    // 折现期望值
    return std::exp(-r * T) * sumPayoff / numPaths;
}

// ========== 主程序 ==========
int main() {
    std::cout << std::fixed << std::setprecision(6);
    
    // 期权参数
    double S0 = 100.0;    // 当前股价
    double K = 100.0;     // 行权价
    double r = 0.05;      // 无风险利率
    double sigma = 0.2;   // 波动率
    double T = 1.0;       // 到期时间（1年）
    
    std::cout << "========== Black-Scholes期权定价 ==========\n";
    std::cout << "参数: S0=" << S0 << ", K=" << K << ", r=" << r 
              << ", σ=" << sigma << ", T=" << T << "年\n\n";
    
    double bsPrice = blackScholesCall(S0, K, r, sigma, T);
    std::cout << "Black-Scholes解析解: " << bsPrice << "\n\n";
    
    std::cout << "========== 蒙特卡洛期权定价 ==========\n";
    std::vector<std::pair<int, int>> configs = {
        {1000, 50},
        {10000, 50},
        {100000, 50},
        {100000, 100},
        {1000000, 100},
    };
    
    for (auto [paths, steps] : configs) {
        auto start = std::chrono::steady_clock::now();
        
        double mcPrice = monteCarloCall(S0, K, r, sigma, T, paths, steps);
        
        auto end = std::chrono::steady_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        std::cout << "路径=" << std::setw(10) << paths 
                  << ", 步数=" << std::setw(5) << steps
                  << " → 价格=" << std::setw(10) << mcPrice
                  << ", 误差=" << std::setw(10) << std::abs(mcPrice - bsPrice)
                  << ", 耗时=" << duration.count() << "μs\n";
    }
    
    return 0;
}
```

> 💡 蒙特卡洛收敛法则：
> - 精度 ∝ 1/√N——要提高10倍精度，需要100倍计算量
> - **方差缩减技术**（控制变量、对偶变量、重要性采样）可以让精度提升几倍到几十倍
> - **并行化**：每个路径相互独立，天然适合多线程/GPU加速

## 46.6 并行科学计算：多核时代的"加速秘籍"

### 46.6.1 OpenMP：让循环"飞起来"

科学计算中最常见的并行就是循环并行化——把一个for循环分散到多个线程上执行。

```cpp
// 46_10_openmp_vector_add.cpp
// 编译: g++ -std=c++20 -fopenmp -O3 46_10_openmp_vector_add.cpp -o 46_10_openmp_vector_add
#include <iostream>
#include <vector>
#include <chrono>
#include <omp.h>

// ========== 朴素版：串行向量加法 ==========
void vectorAdd_serial(const std::vector<double>& a, 
                      const std::vector<double>& b,
                      std::vector<double>& c) {
    for (size_t i = 0; i < a.size(); ++i) {
        c[i] = a[i] + b[i];
    }
}

// ========== OpenMP并行版 ==========
void vectorAdd_parallel(const std::vector<double>& a,
                       const std::vector<double>& b,
                       std::vector<double>& c) {
    #pragma omp parallel for
    for (size_t i = 0; i < a.size(); ++i) {
        c[i] = a[i] + b[i];
    }
}

// ========== 矩阵-向量乘法的并行化 ==========
void matVec_parallel(const std::vector<std::vector<double>>& A,
                     const std::vector<double>& x,
                     std::vector<double>& y) {
    size_t n = A.size();
    
    #pragma omp parallel for schedule(dynamic, 16)
    for (size_t i = 0; i < n; ++i) {
        double sum = 0.0;
        for (size_t j = 0; j < x.size(); ++j) {
            sum += A[i][j] * x[j];
        }
        y[i] = sum;
    }
}

// ========== 主程序 ==========
int main() {
    std::cout << "OpenMP 最大线程数: " << omp_get_max_threads() << "\n";
    
    // 测试向量加法
    const size_t N = 10'000'000;
    std::vector<double> a(N, 1.0), b(N, 2.0), c(N, 0.0);
    
    // 串行版本
    auto start = std::chrono::high_resolution_clock::now();
    vectorAdd_serial(a, b, c);
    auto end = std::chrono::high_resolution_clock::now();
    auto serial_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    // 并行版本
    start = std::chrono::high_resolution_clock::now();
    vectorAdd_parallel(a, b, c);
    end = std::chrono::high_resolution_clock::now();
    auto parallel_time = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "\n========== 向量加法 (N=" << N << ") ==========\n";
    std::cout << "串行耗时:   " << serial_time.count() << " μs\n";
    std::cout << "并行耗时:   " << parallel_time.count() << " μs\n";
    std::cout << "加速比:     " << (double)serial_time.count() / parallel_time.count() << "x\n";
    
    // 测试矩阵-向量乘法
    const size_t M = 5000;
    std::vector<std::vector<double>> A(M, std::vector<double>(M));
    std::vector<double> x(M, 1.0), y(M, 0.0);
    
    // 初始化矩阵（简单赋值）
    for (size_t i = 0; i < M; ++i) {
        for (size_t j = 0; j < M; ++j) {
            A[i][j] = (i + j) * 0.001;
        }
    }
    
    start = std::chrono::high_resolution_clock::now();
    matVec_parallel(A, x, y);
    end = std::chrono::high_resolution_clock::now();
    auto matvec_time = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "\n========== 矩阵-向量乘法 (" << M << "×" << M << ") ==========\n";
    std::cout << "并行耗时: " << matvec_time.count() << " ms\n";
    std::cout << "结果验证: y[0]=" << y[0] << ", y[M/2]=" << y[M/2] << ", y[M-1]=" << y[M-1] << "\n";
    
    return 0;
}
```

### 46.6.2 SIMD：让一条指令干多个数的事

SIMD（Single Instruction Multiple Data）允许一条CPU指令同时处理多个数据。

```cpp
// 46_11_simd.cpp
// 编译: g++ -std=c++20 -O3 -march=native -ffast-math 46_11_simd.cpp -o 46_11_simd
// 注意：需要CPU支持AVX2或AVX-512
#include <iostream>
#include <vector>
#include <chrono>
#include <immintrin.h>

// ========== 朴素版：串行求和 ==========
double sum_serial(const std::vector<double>& v) {
    double sum = 0.0;
    for (double x : v) {
        sum += x;
    }
    return sum;
}

// ========== 手写SIMD版（AVX2） ==========
double sum_simd(const std::vector<double>& v) {
    double sum[4] = {0.0, 0.0, 0.0, 0.0};  // 4个累加器，对应AVX2的256-bit寄存器
    __m256d acc0 = _mm256_setzero_pd();
    __m256d acc1 = _mm256_setzero_pd();
    __m256d acc2 = _mm256_setzero_pd();
    __m256d acc3 = _mm256_setzero_pd();
    
    size_t i = 0;
    size_t limit = (v.size() / 16) * 16;
    
    // 每次处理16个double（128字节）
    for (; i < limit; i += 16) {
        acc0 = _mm256_add_pd(acc0, _mm256_loadu_pd(&v[i]));
        acc1 = _mm256_add_pd(acc1, _mm256_loadu_pd(&v[i + 4]));
        acc2 = _mm256_add_pd(acc2, _mm256_loadu_pd(&v[i + 8]));
        acc3 = _mm256_add_pd(acc3, _mm256_loadu_pd(&v[i + 12]));
    }
    
    // 合并累加器
    __m256d acc01 = _mm256_add_pd(acc0, acc1);
    __m256d acc23 = _mm256_add_pd(acc2, acc3);
    __m256d acc0123 = _mm256_add_pd(acc01, acc23);
    
    // 水平加法：把所有元素加起来
    _mm256_storeu_pd(sum, acc0123);
    double total = sum[0] + sum[1] + sum[2] + sum[3];
    
    // 处理剩余元素
    for (; i < v.size(); ++i) {
        total += v[i];
    }
    
    return total;
}

// ========== 主程序 ==========
int main() {
    // 编译时检查SIMD支持
#if defined(__AVX2__)
    std::cout << "AVX2 支持: ✓\n";
#elif defined(__AVX__)
    std::cout << "AVX 支持: ✓\n";
#else
    std::cout << "AVX 不支持: 将使用朴素实现\n";
#endif
    
    const size_t N = 10'000'000;
    std::vector<double> v(N, 1.0);
    
    std::cout << "N = " << N << "\n\n";
    
    // 串行版本
    auto start = std::chrono::high_resolution_clock::now();
    double s1 = sum_serial(v);
    auto end = std::chrono::high_resolution_clock::now();
    auto t1 = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    // SIMD版本
    start = std::chrono::high_resolution_clock::now();
    double s2 = sum_simd(v);
    end = std::chrono::high_resolution_clock::now();
    auto t2 = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "串行结果: " << s1 << ", 耗时: " << t1.count() << " μs\n";
    std::cout << "SIMD结果: " << s2 << ", 耗时: " << t2.count() << " μs\n";
    std::cout << "加速比: " << (double)t1.count() / t2.count() << "x\n";
    
    return 0;
}
```

## 46.7 科学计算库生态：从"造轮子"到"站在巨人肩上"

### 46.7.1 必知库一览

| 库名 | 领域 | 特点 |
|------|------|------|
| **Eigen** | 线性代数 | Header-only，性能接近手写C |
| **Boost.Multiprecision** | 高精度计算 | 任意精度整数、浮点、有理数 |
| **Boost.Odeint** | ODE求解 | 封装好的各种求解器 |
| **FFTW** | FFT | 世界上最快的FFT |
| **PETSc** | 偏微分方程 | 大规模并行稀疏矩阵求解 |
| **deal.II** | 有限元 | 学术级FEM框架 |
| **Armadillo** | 线性代数 | MATLAB风格接口 |
| **xtensor** | 多维数组 | NumPy风格，header-only |

### 46.7.2 高精度计算示例：Boost.Multiprecision

```cpp
// 46_12_high_precision.cpp
// 编译: g++ -std=c++20 -O2 46_12_high_precision.cpp -o 46_12_high_precision
#include <iostream>
#include <boost/multiprecision/cpp_dec_float.hpp>
#include <boost/multiprecision/cpp_int.hpp>
#include <iomanip>
#include <vector>
#include <cmath>

using namespace boost::multiprecision;

// 高精度浮点：100位精度
typedef cpp_dec_float_100 high_float;

// 计算圆周率的BBP公式
high_float piBBP(int digits) {
    high_float pi = 0;
    int terms = digits / 14 + 10;  // 每项大约贡献14位
    
    for (int k = 0; k < terms; ++k) {
        // BBP公式: (1/16)^k * (4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6))
        // 注意：C++中^是按位异或运算符（优先级极低！），不能用a^b表示指数！
        high_float term = 
            pow(high_float(16), -k) * (
                high_float(4) / high_float(8 * k + 1) -
                high_float(2) / high_float(8 * k + 4) -
                high_float(1) / high_float(8 * k + 5) -
                high_float(1) / high_float(8 * k + 6)
            );
        pi += term;
    }
    return pi;
}

// 高精度整数：大数阶乘
cpp_int factorial(int n) {
    cpp_int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

// 主程序
int main() {
    std::cout << std::fixed;
    
    std::cout << "========== 高精度计算 ==========\n\n";
    
    // 计算100位圆周率
    std::cout << "100位圆周率 (BBP公式):\n";
    high_float pi = piBBP(100);
    std::cout << std::setprecision(100) << pi << "\n\n";
    
    // 对比标准double
    std::cout << "double 精度:\n";
    std::cout << std::setprecision(17) << 3.141592653589793 << "\n\n";
    
    // 大数阶乘
    std::cout << "100! (高精度整数):\n";
    cpp_int f100 = factorial(100);
    std::string f100_str = f100.convert_to<std::string>();
    std::cout << "共 " << f100_str.size() << " 位\n";
    std::cout << "前20位: " << f100_str.substr(0, 20) << "...\n";
    std::cout << "后20位: ..." << f100_str.substr(f100_str.size() - 20) << "\n\n";
    
    // 高精度浮点运算验证
    std::cout << "高精度运算验证:\n";
    high_float x = 1;
    for (int i = 1; i <= 100; ++i) {
        x *= i;
    }
    std::cout << "100! 作为浮点数: " << std::setprecision(50) << x << "\n";
    
    return 0;
}
```

## 本章小结

### 核心知识点回顾

| 知识点 | 章节 | 关键词 |
|--------|------|--------|
| 数值稳定性 | 46.1.3 | 浮点陷阱、大数吃小数、稳定求根公式 |
| 向量/矩阵运算 | 46.2 | 手写实现 vs Eigen库 |
| 方程求根 | 46.3.1 | 二分法、牛顿法、割线法、收敛阶数 |
| 数值积分 | 46.3.2 | 梯形法则、辛普森法则、蒙特卡洛积分 |
| ODE求解 | 46.3.3 | RK4、龙格-库塔、刚性系统 |
| FFT | 46.4 | 频谱分析、DFT→FFT、Nyquist频率 |
| 随机数 | 46.5 | MT算法、均匀/正态分布、Box-Muller |
| 蒙特卡洛 | 46.5 | π估算、期权定价、方差缩减 |
| 并行计算 | 46.6 | OpenMP、SIMD、加速比 |
| 高精度计算 | 46.7 | Boost.Multiprecision、大数运算 |

### 实践建议

1. **不要重复造轮子**：Eigen、FFTW、Boost这些库已经足够可靠，直接用就行。
2. **数值稳定性是生死线**：一个微小的舍入误差可能让你的"科学计算"变成"玄学计算"。
3. **先验证，后优化**：用简单方法得到正确结果，再考虑并行化/SIMD优化。
4. **并行化要谨慎**：OpenMP的共享内存模型虽然简单，但数据竞争一旦出现就是噩梦。
5. **蒙特卡洛不是万能药**：对于低维光滑函数，确定性方法（辛普森）通常更好。

### 延伸学习路线

```
初级（能写科学计算程序）
├── 线性代数基础（矩阵运算、特征值、SVD）
├── 数值分析（误差、收敛性、稳定性）
└── 学习Eigen、Boost.Odeint等库

中级（能进行性能优化）
├── OpenMP并行编程
├── SIMD向量化
├── 稀疏矩阵存储格式（CSR、CSC）
└── 性能分析与profiling

高级（能解决实际问题）
├── 偏微分方程数值解法（FEM、FDM、FVM）
├── 大规模并行计算（MPI、GPU CUDA）
├── 优化算法（L-BFGS、Trust-Region）
└── 专业领域深化（计算物理、计算金融、机器学习）
```

> 🎯 课后思考题：
> 1. 为什么说"永远不要用 `(-b + sqrt(b*b - 4*a*c)) / (2*a)` 这个公式"？你能构造一个反例吗？
> 2. 如果用蒙特卡洛方法估算n维球体的体积，它的收敛速度是多少？与确定性方法相比呢？
> 3. 为什么说洛伦兹吸引子是"确定性混沌"？这与天气预报有什么关系？
> 4. 如果你要用C++实现一个图像模糊滤镜（卷积运算），你会如何并行化它？

---

*本章代码均可在支持C++20的编译器上编译运行（部分需要安装对应库）。*
