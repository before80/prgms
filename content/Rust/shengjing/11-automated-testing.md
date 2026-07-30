+++
title = "11-自动化测试"
date = 2026-07-28T14:49:00+08:00
weight = 110
type = "docs"
description = "《Rust语言圣经》「自动化测试」精要速成"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「自动化测试」

# 测试

> 测试可以有效发现缺陷，但无法证明程序不存在缺陷 — Edsger W. Dijkstra

Rust 的类型系统保证类型正确，不能保证逻辑正确。测试通过函数验证行为；不要迷信测试。

## 编写测试及控制执行

测试三步：设置数据/状态 → 运行被测代码 → 断言结果。

### 测试函数

- `cargo new --lib` 自动生成 `#[cfg(test)] mod tests { ... }`
- 测试函数用 `#[test]` 标注；模块内可混写辅助非测试函数
- 运行：`cargo test`（编译临时可执行文件后删除）

输出字段速记：

| 字段 | 含义 |
|------|------|
| `passed/failed/ignored/measured/filtered` | 通过/失败/忽略/基准/过滤 |
| `Doc-tests` | 文档注释中的测试 |

### 失败与自定义信息

- 测试失败：`panic!` 或断言宏触发
- 默认每测试一线程；一测试 panic 则整体标记失败
- `assert!` / `assert_eq!` 可追加格式化参数作自定义错误信息

### 测试 panic

- `#[should_panic]`：期望函数 panic
- `#[should_panic(expected = "...")]`：`expected` 为 panic 信息前缀即可

### 使用 Result

```rust
#[test]
fn it_works() -> Result<(), String> { ... }
```

返回 `Err` 即失败；此模式下不能用 `#[should_panic]`。

### 命令行参数

`cargo test [cargo参数] -- [测试二进制参数]`

常用测试二进制参数：

| 参数 | 作用 |
|------|------|
| `--test-threads=1` | 顺序执行，避免共享状态竞争 |
| `--show-output` | 显示通过测试的 stdout |

### 过滤与忽略

- 运行单个/部分：`cargo test 名称片段`（前缀或中间匹配，非多参数列表）
- 按模块：`cargo test tests::` 过滤模块名
- `#[ignore]` 默认跳过；`cargo test -- --ignored` 只跑被忽略项
- `cargo test -- --include-ignored` 全部运行

## 单元测试和集成测试

### 单元测试

- 与待测代码同文件；`#[cfg(test)]` 仅在 `cargo test` 时编译（省 build 时间、减体积）
- `use super::*;` 可测试私有函数
- 测函数/单元级逻辑

### 集成测试

- 项目根 `tests/` 目录（与 `src` 同级）；每文件独立 crate
- `use 包名;` 引入库；**只能**调用 `pub` API
- 无需 `#[cfg(test)]`；测功能/接口级行为
- 单元全过 ≠ 集成全过

### 集成测试的组织

- `tests/common/mod.rs` 放共享辅助（非自动测试）
- 子目录测试需在子目录建 `mod.rs` 或单独文件

## 断言 assertion

| 宏 | 作用 | 模式 |
|----|------|------|
| `assert!` | 布尔为 true | 全模式 |
| `assert_eq!` / `assert_ne!` | 相等/不等 | 全模式 |
| `debug_assert!` 系列 | 同上 | 仅 Debug |

- `assert_eq!`/`assert_ne!` 要求类型实现 `PartialEq + Debug`；自定义类型可 `#[derive(PartialEq, Debug)]`
- 生产环境常用 `debug_assert!` 系列避免运行时开销

## 用 GitHub Actions 进行持续集成

CI：定期拉代码 → 自动构建/测试/发布，无需人工介入。

### GitHub Actions 要点

- **Workflow**：`.github/workflows/*.yml`
- **触发**：`on: push/pull_request/workflow_dispatch`
- **Job**：`runs-on` + `steps`
- **Action 引用**：`user/repo@version`（分支/tag/commit）
- Rust 典型步骤：`actions/checkout` → `actions-rs/toolchain` → `cargo test`

常用 action 来源：GitHub Marketplace、awesome-actions、starter-workflows。

## 基准测试 benchmark

两种：**官方 `test` 基准**（需 nightly）与 **`criterion`**（推荐 stable）。

### 官方 benchmark

1. `rustup override set nightly`
2. `#![feature(test)]` + `extern crate test;`
3. `#[bench] fn f(b: &mut Bencher) { b.iter(|| ...); }`
4. **`cargo bench`** 运行（`cargo test` 会把 bench 当普通测试）

建议：

- 初始化放 `b.iter` 外
- `iter` 内代码短、幂等、不做累加状态
- LLVM 可能优化掉无副作用调用 → 用 `std::hint::black_box`（书中示例用 `test::black_box`）

### criterion.rs

- stable 可用；统计更可靠（置信区间、图表）
- 独立 crate：`criterion = "0.3"` + `[[bench]]` 配置
- 运行：`cargo bench`

---

**速查命令**

```text
cargo test                          # 全部测试
cargo test add                      # 名称过滤
cargo test -- --test-threads=1      # 顺序
cargo test -- --show-output         # 显示输出
cargo test -- --ignored             # 仅 ignored
cargo bench                         # 基准测试
```
