+++
title = "包管理与模块"
date = 2026-09-19T09:10:00+08:00
weight = 5
type = "docs"
description = "18 种语言的包管理与模块对照：模块与命名空间、依赖声明与锁定、包仓库与发布、版本约束与常见坑"
isCJKLanguage = true
draft = false
+++

# 包管理与模块：18 种语言对照

"包管理"要回答四个问题：**代码怎么分组**（模块/命名空间）、**依赖怎么声明与锁定**（清单 + 锁文件）、**包怎么发布与获取**（注册中心）、**版本怎么解析**（语义化版本与冲突处理）。本页按这四个主题组织，每个主题一套 18 语言标签页；命令与文件名都给可直接照抄的写法。

## 包管理与模块

**一页速览**

| 语言 | 模块单位 | 包管理器 | 清单 / 锁文件 | 注册中心 |
| --- | --- | --- | --- | --- |
| Rust | crate + mod | Cargo | `Cargo.toml` / `Cargo.lock` | crates.io |
| Swift | target（module） | SwiftPM | `Package.swift` / `Package.resolved` | Git 仓库（无中心仓库） |
| Go | package（目录） | go 命令 | `go.mod` / `go.sum` | 无（模块 = Git 仓库） |
| Python | module + package | pip / uv / poetry | `pyproject.toml` / `uv.lock`、`poetry.lock` | PyPI |
| Kotlin | package | Gradle / Maven | `build.gradle.kts` / 无默认锁 | Maven Central |
| Java | package（+ JPMS module） | Maven / Gradle | `pom.xml` / 无默认锁（用 BOM） | Maven Central |
| C++ | namespace + 头文件/模块 | vcpkg / Conan | `vcpkg.json` / `vcpkg-lock.json` | 无官方（vcpkg、Conan Center） |
| C | 翻译单元 + 头文件 | 系统包管理器 | 无 | 无（发行版 / 源码） |
| Julia | module | Pkg | `Project.toml` / `Manifest.toml` | General Registry |
| C# | namespace + assembly | NuGet | `.csproj` / `packages.lock.json`（可选） | NuGet.org |
| Dart | library | pub | `pubspec.yaml` / `pubspec.lock` | pub.dev |
| R | package | R CMD + renv | `DESCRIPTION` / `renv.lock` | CRAN、Bioconductor |
| Zig | 文件即模块 | `zig build` | `build.zig.zon`（哈希即锁） | 无（URL + 哈希） |
| Lua | 文件 + table | LuaRocks | `.rockspec` / 无锁 | luarocks.org |
| TypeScript | ES module | npm / pnpm / yarn | `package.json` / lock 文件 | npm Registry |
| JavaScript | ESM / CommonJS | npm / pnpm / yarn | `package.json` / lock 文件 | npm Registry |
| PHP | namespace | Composer | `composer.json` / `composer.lock` | Packagist |
| Ruby | module / class | Bundler + RubyGems | `Gemfile` / `Gemfile.lock` | RubyGems.org |

### 模块与命名空间

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

模块树由 `mod` 组成，**crate 才是编译单元**（`bin` 或 `lib`）；文件即模块（`mod foo;` 对应 `foo.rs` 或 `foo/mod.rs`）。

```rust
// src/lib.rs
pub mod parser;          // 引入 src/parser.rs
pub(crate) mod internal;  // 只在当前 crate 可见

use crate::parser::parse;
use std::collections::HashMap;
```

可见性有 `pub`、`pub(crate)`、`pub(super)`、`pub(in path)` 四档；`crate::` 从根开始、`super::` 上一级、`self::` 当前模块。

📘 [Rust Reference · Modules](https://doc.rust-lang.org/reference/items/modules.html)

{{% /tab %}}

{{% tab header="Swift" %}}

模块 = SwiftPM 的 target（或 Xcode 的 framework/library target）；默认可见性是 `internal`（同模块可见），跨模块要用 `public`/`open`。

```swift
// Package.swift 中的 target 就是模块
// Sources/Parser/Parse.swift
public struct Parser {          // 跨模块可见
    public init() {}
    internal func helper() {}     // 同模块可见
}
```

```swift
import Parser                    // 引入另一个模块
@testable import Parser           // 测试里可见 internal 成员
```

Swift 没有"命名空间"关键字：模块名 + 类型名就是天然的命名空间；`@testable` 是测试专用后门。

📘 [SwiftPM · 模块](https://www.swift.org/documentation/package-manager/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 里**一个目录就是一个 package**，import 路径就是模块路径 + 目录；导出与否只看首字母大小写。

```go
// 文件头声明所属 package
package parser

func Parse(s string) (int, error) { ... }   // 导出（大写）
func helper() {}                             // 未导出（小写）
```

```go
import (
    "example.com/demo/parser"   // 自己模块里的包
    "github.com/pkg/errors"
)

p, err := parser.Parse("42")
```

`internal/` 目录下的包只能被同一模块内部引用（编译器强制）；`go mod init` 里的模块路径就是 import 前缀。

📘 [Go · 包](https://go.dev/ref/spec#Packages)

{{% /tab %}}

{{% tab header="Python" %}}

`module` 是一个 `.py` 文件，`package` 是带 `__init__.py` 的目录（PEP 420 的"命名空间包"可以没有）。

```python
# mypkg/__init__.py
from .parser import parse          # 相对导入
__all__ = ["parse"]                 # 控制 from mypkg import * 的内容

# mypkg/parser.py
def parse(s: str) -> int: return int(s)
```

```python
import mypkg.parser as p           # 绝对导入（推荐）
from mypkg import parse
```

PEP 8 建议优先用绝对导入；相对导入（`.parser`）只在包内部使用，且不能用于顶层脚本。

📘 [Python · 模块](https://docs.python.org/3/tutorial/modules.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

`package` 是逻辑命名空间，**不要求目录结构一致**；`internal` 表示"模块内可见"（Gradle 模块/编译单元）。

```kotlin
package com.example.parser

internal fun parse(s: String): Int = s.toInt()   // 模块内可见
fun publicApi() {}
```

```kotlin
import com.example.parser.publicApi
```

Kotlin 的可见性只有 `public`/`internal`/`protected`/`private` 四档；`internal` 的边界是"同一个编译模块"（Gradle 里通常是一个 module）。

📘 [Kotlin · 可见性](https://kotlinlang.org/docs/visibility-modifiers.html)

{{% /tab %}}

{{% tab header="Java" %}}

`package` 与目录结构一致；Java 9 起还有 **JPMS 模块**（`module-info.java`），用 `requires`/`exports` 精确声明依赖与导出。

```java
// module-info.java
module com.example.demo {
    requires java.sql;
    exports com.example.demo.api;      // 只有这个包对外可见
}
```

```java
package com.example.demo.api;
import java.util.List;                  // 普通 import
```

普通项目只用 package + classpath 就够了；JPMS 的价值在于"显式依赖 + 强封装"，代价是需要额外的模块声明与迁移工作。

📘 [JLS · 包](https://docs.oracle.com/javase/specs/jls/se25/html/jls-7.html)

{{% /tab %}}

{{% tab header="C++" %}}

`namespace` 是逻辑分组；物理分组靠头文件 + 源文件，C++20 起还有真正的**模块**（`import`/`export module`）。

```cpp
// 头文件方式
namespace demo { int parse(const std::string&); }

inline namespace v1 { }        // 版本化命名空间（ABI 技巧）
namespace { int helper(); }     // 匿名命名空间：仅本翻译单元可见
```

```cpp
// C++20 模块
export module demo.parser;
export int parse(const std::string&);
```

头文件 + `#include` 仍是主流（模块支持取决于工具链）；匿名命名空间是"文件级私有"的标准做法。

📘 [cppreference · Namespaces](https://en.cppreference.com/w/cpp/language/namespace)、[Modules](https://en.cppreference.com/w/cpp/language/modules)

{{% /tab %}}

{{% tab header="C" %}}

C **没有模块与命名空间**：代码分组靠"头文件 + 翻译单元"，可见性靠 `static`（内部链接）与命名前缀（如 `demo_parse`）。

```c
/* demo_parser.h */
#ifndef DEMO_PARSER_H
#define DEMO_PARSER_H
int demo_parse(const char *s);
#endif

/* demo_parser.c */
static int helper(void) { return 0; }   /* 仅本文件可见 */
int demo_parse(const char *s) { return helper(); }
```

头文件用 include guard（或 `#pragma once`）防止重复包含；符号冲突全靠前缀约定与 `static` 控制。

📘 [C · 翻译单元](https://en.cppreference.com/w/c/language/translation_phases)

{{% /tab %}}

{{% tab header="Julia" %}}

`module ... end` 是命名空间，`using`/`import` 引入包，`export` 决定 `using` 后哪些名字直接可见。

```julia
module Demo
export parse

parse(s::AbstractString) = tryparse(Int, s)

module Internal          # 子模块
    helper() = 1
end
end

using .Demo               # 相对路径引入当前项目里的模块
using .Demo.Internal
```

`using Demo` 会带来导出的名字，`import Demo` 只引入模块名（要写 `Demo.parse`）；`..`/`.` 前缀表示相对当前模块。

📘 [Julia · 模块](https://docs.julialang.org/en/v1/manual/modules/)

{{% /tab %}}

{{% tab header="C#" %}}

`namespace` 是逻辑分组，**assembly**（`.csproj`）才是物理单元；C# 10 起支持 file-scoped namespace，`internal` 表示程序集内可见。

```csharp
namespace Demo.Parser;            // file-scoped namespace（C# 10+）

internal sealed class Parser { }   // 程序集内可见
public record Result(int Value);    // 跨程序集可见
```

```csharp
using Demo.Parser;                 // 引入命名空间
global using System.Text.Json;      // global using（C# 10+）：整个项目生效
```

`InternalsVisibleTo` 可以让测试程序集访问 `internal` 成员；`global using` 适合把常用命名空间集中声明一次。

📘 [MS Learn · 命名空间](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/namespaces)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的可见性单位是**库（library）**——通常就是一个文件；`_` 开头的成员只在库内可见。`import`/`export`/`part` 组织代码。

```dart
// lib/parser.dart
class Parser {
  int _helper() => 0;      // 库级私有
  int parse(String s) => int.parse(s);
}
```

```dart
import 'package:demo/parser.dart' show Parser;   // 只引入部分成员
import 'dart:async' as async;                     // 起别名
export 'src/impl.dart';                           // 转发导出
```

`package:` 导入指向 `lib/` 下的路径（需要 `pubspec.yaml` 的 `name`），相对导入用于包内文件。

📘 [Dart · 库与可见性](https://dart.dev/language/libraries)

{{% /tab %}}

{{% tab header="R" %}}

R 的"模块"就是 **package**：`DESCRIPTION` + `NAMESPACE` 两个文件定义元数据、导出与依赖；`pkg::fun` 是显式调用。

```r
library(dplyr)            # 挂到搜索路径（可直接用函数名）
require(dplyr)             # 类似，但返回 TRUE/FALSE
dplyr::filter(df, x > 0)    # 显式命名空间（推荐在包/脚本里用）
```

```r
# NAMESPACE 里由 roxygen2 生成
export(parse)
importFrom(stats, median)
```

函数名冲突时 `::` 是唯一可靠的写法；包内部一律用 `pkg::fun` 或 `@importFrom`，避免依赖用户的 `library()` 顺序。

📘 [R · 命名空间](https://cran.r-project.org/doc/manuals/r-release/R-exts.html#Package-namespaces)

{{% /tab %}}

{{% tab header="Zig" %}}

**文件即模块**：用 `@import("file.zig")` 引入，`pub` 决定是否导出；`build.zig` 里可以把依赖注册成模块。

```zig
// src/parser.zig
pub fn parse(s: []const u8) !u32 { return 42; }

// src/main.zig
const parser = @import("parser.zig");
pub fn main() !void {
    const v = try parser.parse("42");
    _ = v;
}
```

```zig
// build.zig 片段：把依赖注册为模块
const dep = b.dependency("zap", .{});
exe.root_module.addImport("zap", dep.module("zap"));
```

没有命名空间关键字：路径 + `pub` 就是全部；`std` 也是一个模块（`@import("std")`）。

📘 [Zig · @import](https://ziglang.org/documentation/master/#import)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有模块语法：`require("mod")` 按 `package.path` 找文件，**惯例是文件返回一个 table**；`module()` 函数在 5.2 已被移除。

```lua
-- parser.lua
local Parser = {}
function Parser.parse(s) return tonumber(s) end
return Parser               -- 返回模块表
```

```lua
local parser = require("parser")
print(parser.parse("42"))

print(package.path)         -- 查看搜索路径（LUA_PATH）
```

模块名与文件名对应（`parser` → `parser.lua` 或 `parser/init.lua`）；`require` 会缓存结果，改代码要重启进程或清 `package.loaded`。

📘 [Lua 5.5 · require](https://www.lua.org/manual/5.5/manual.html#pdf-require)

{{% /tab %}}

{{% tab header="TypeScript" %}}

用 ES module 的 `import`/`export`（早期还有 `namespace`，现在主要用来给全局脚本分组）；类型声明放在 `.d.ts` 里。

```ts
// src/parser.ts
export function parse(s: string): number { return Number(s); }
export type Result = { value: number };

import { parse, type Result } from "./parser.js";   // 相对路径 + 扩展名（NodeNext）
```

```ts
// 给没有类型的库写声明
declare module "legacy-lib" {
  export function doThing(x: number): string;
}
```

tsconfig 的 `moduleResolution`/`paths` 决定解析规则；monorepo 用 project references 把多个包连起来。

📘 [TS · 模块](https://www.typescriptlang.org/docs/handbook/modules.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

两套模块系统并存：**ESM**（`import`/`export`）与 **CommonJS**（`require`/`module.exports`）；`package.json` 的 `type` 与文件扩展名决定用哪套。

```js
// ESM（.mjs 或 "type": "module"）
import { parse } from "./parser.js";
export function run() {}

// CommonJS（.cjs）
const { parse } = require("./parser.cjs");
module.exports = { run };
```

```jsonc
// package.json
{ "type": "module", "exports": { ".": "./dist/index.js" } }
```

`exports` 字段决定外部能 import 哪些路径（比 `main` 更严格）；ESM 与 CJS 互操作有诸多限制，混用时要看清 `default` 包装。

📘 [Node.js · 模块](https://nodejs.org/api/packages.html)

{{% /tab %}}

{{% tab header="PHP" %}}

`namespace` + `use` 是语言层机制；自动加载靠 Composer 的 PSR-4 映射（命名空间前缀 → 目录）。

```php
namespace App\Parser;

use App\Support\Result;

final class Parser {
    public function parse(string $s): Result { return new Result((int) $s); }
}
```

```jsonc
// composer.json
{ "autoload": { "psr-4": { "App\\": "src/" } } }
```

PSR-4 的规则是"前缀对应目录、其余对应路径"，所以 `App\Parser\Parser` 必须在 `src/Parser/Parser.php`；改完映射要 `composer dump-autoload`。

📘 [PSR-4](https://www.php-fig.org/psr/psr-4/)

{{% /tab %}}

{{% tab header="Ruby" %}}

`module` 既是命名空间也是 mixin；文件用 `require`/`require_relative` 引入，gem 用 `lib/` 目录约定。

```ruby
module Demo
  module Parser
    def self.parse(s) = Integer(s)
  end
end

Demo::Parser.parse("42")        # 用 :: 访问命名空间
```

```ruby
require_relative "parser"        # 相对当前文件（推荐）
require "json"                    # 从 $LOAD_PATH / gem 加载
```

Rails 用 Zeitwerk 按"文件名 → 常量名"自动加载（`app/services/user_mailer.rb` → `UserMailer`），不需要手写 `require`。

📘 [Ruby · 模块](https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 依赖声明与锁定

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `Cargo.toml`（`[dependencies]`） |
| 锁文件 | `Cargo.lock`（二进制项目提交，库项目通常不提交） |
| 常用命令 | `cargo add`、`cargo remove`、`cargo update`、`cargo tree` |

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1.40", features = ["rt-multi-thread", "macros"] }
```

`cargo add` 写清单、`cargo update` 只改锁文件；`cargo tree -d` 能看出同一个 crate 被解析成了多个版本。

📘 [Cargo · 依赖](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html)

{{% /tab %}}

{{% tab header="Swift" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `Package.swift` |
| 锁文件 | `Package.resolved` |
| 常用命令 | `swift package resolve`、`update`、`show-dependencies` |

```swift
dependencies: [
    .package(url: "https://github.com/apple/swift-argument-parser.git", from: "1.5.0"),
]
```

SwiftPM 的依赖就是 Git 仓库 + 版本标签；`from:` 等价于"语义化版本范围"，`Package.resolved` 记录解析结果（应提交）。

📘 [SwiftPM · 依赖](https://www.swift.org/documentation/package-manager/)

{{% /tab %}}

{{% tab header="Go" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `go.mod` |
| 锁文件 | `go.sum`（校验和）+ `go.mod` 里的精确版本 |
| 常用命令 | `go get`、`go mod tidy`、`go mod download`、`go mod graph` |

```
module example.com/demo

go 1.27

require github.com/gin-gonic/gin v1.10.0
```

```bash
go mod tidy        # 补齐缺失、删除未用
go mod graph       # 依赖图
go list -m all     # 所有依赖的最终版本
```

Go 用**最小版本选择（MVS）**：每个依赖取满足所有要求的最低版本，因此升级要用显式 `go get pkg@version`。

📘 [Go Modules 参考](https://go.dev/ref/mod)

{{% /tab %}}

{{% tab header="Python" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `pyproject.toml`（推荐）、`requirements.txt`（传统） |
| 锁文件 | `uv.lock`、`poetry.lock`、`pdm.lock`（pip 无锁文件） |
| 常用命令 | `pip install`、`uv add/sync`、`poetry add/install` |

```toml
[project]
name = "demo"
dependencies = ["httpx>=0.27", "pydantic>=2.8"]

[project.optional-dependencies]
dev = ["pytest", "ruff"]
```

```bash
uv sync              # 按 uv.lock 精确安装
pip install -e ".[dev]"
```

没有锁文件就无法保证"昨天能装、今天也能装"；团队项目建议统一用带锁的工具（uv/poetry/pdm）。

📘 [Python 打包](https://packaging.python.org/)、[uv](https://docs.astral.sh/uv/)

{{% /tab %}}

{{% tab header="Kotlin" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `build.gradle.kts` + `settings.gradle.kts` |
| 锁文件 | 默认无；可开 `dependencyLocking` |
| 常用命令 | `./gradlew dependencies`、`build`、`dependencyUpdates` |

```kotlin
dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
    testImplementation(kotlin("test"))
}
```

版本集中在 `gradle/libs.versions.toml`（version catalog）里声明，避免散落在各处；`gradle wrapper` 固定 Gradle 版本。

📘 [Gradle · 依赖管理](https://docs.gradle.org/current/userguide/dependency_management.html)

{{% /tab %}}

{{% tab header="Java" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `pom.xml`（Maven）/ `build.gradle(.kts)` |
| 锁文件 | 无；用 BOM 或 `dependencyManagement` 固定版本 |
| 常用命令 | `mvn dependency:tree`、`mvn versions:display-dependency-updates` |

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.junit</groupId>
      <artifactId>junit-bom</artifactId>
      <version>5.11.0</version>
      <type>pom</type><scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

BOM（导入的 pom）把一组依赖的版本统一起来；`dependency:tree` 用来排查"某个传递依赖从哪来"。

📘 [Maven · 依赖机制](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)

{{% /tab %}}

{{% tab header="C++" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `vcpkg.json`（vcpkg）/ `conanfile.txt`（Conan） |
| 锁文件 | `vcpkg-lock.json`、`conan.lock`（可选） |
| 常用命令 | `vcpkg install`、`conan install`、`cmake --preset` |

```jsonc
// vcpkg.json
{ "name": "demo", "version": "0.1.0",
  "dependencies": ["fmt", "nlohmann-json"] }
```

```bash
vcpkg install --triplet arm64-osx
cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

没有锁文件时，vcpkg 的"基线（baseline）"就是隐式锁定：`builtin-baseline` 指向一个 commit，保证所有人拿到同一版本。

📘 [vcpkg manifest](https://learn.microsoft.com/en-us/vcpkg/concepts/manifest-mode)

{{% /tab %}}

{{% tab header="C" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | 无（依赖系统包管理器） |
| 锁文件 | 无 |
| 常用命令 | `pkg-config --cflags --libs`、`apt/dnf/brew install` |

```bash
cc main.c $(pkg-config --cflags --libs libcurl) -o app
pkg-config --modversion libcurl
```

要"自带依赖"就把源码 vendor 进仓库（如 `deps/`），或用 CMake 的 `FetchContent`/`ExternalProject` 在构建时拉取并固定 commit。

📘 [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/)

{{% /tab %}}

{{% tab header="Julia" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `Project.toml` |
| 锁文件 | `Manifest.toml`（必须提交） |
| 常用命令 | `Pkg.add`、`Pkg.rm`、`Pkg.instantiate`、`Pkg.status` |

```julia
using Pkg
Pkg.activate(".")
Pkg.add(["DataFrames", "CSV"])
Pkg.instantiate()          # 按 Manifest.toml 精确还原
```

`Project.toml` 记直接依赖与兼容范围，`Manifest.toml` 记完整依赖树与精确版本；只有两者都在，环境才可复现。

📘 [Pkg · Project 与 Manifest](https://pkgdocs.julialang.org/v1/toml-files/)

{{% /tab %}}

{{% tab header="C#" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `.csproj`（`PackageReference`） |
| 锁文件 | `packages.lock.json`（`RestorePackagesWithLockFile`） |
| 常用命令 | `dotnet add package`、`dotnet restore`、`dotnet list package` |

```xml
<ItemGroup>
  <PackageReference Include="Serilog" Version="4.2.0" />
</ItemGroup>
<PropertyGroup>
  <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
</PropertyGroup>
```

```bash
dotnet restore --locked-mode     # CI 里强制按锁文件还原
```

中央包管理（`Directory.Packages.props` + `ManagePackageVersionsCentrally`）让整个解决方案的版本集中在一处。

📘 [NuGet · 包引用](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files)

{{% /tab %}}

{{% tab header="Dart" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `pubspec.yaml` |
| 锁文件 | `pubspec.lock`（应用提交，库通常不提交） |
| 常用命令 | `dart pub get`、`upgrade`、`outdated`、`add` |

```yaml
dependencies:
  http: ^1.2.0
  path: any                 # any：不限制版本（慎用）
dev_dependencies:
  test: ^1.25.0
```

```bash
dart pub add http            # 自动写入并解析
dart pub upgrade --major-versions
```

Dart 3.6+ 的 pub workspace 让多个包共享一份 `pubspec.lock`，monorepo 里更一致。

📘 [pubspec](https://dart.dev/tools/pub/pubspec)

{{% /tab %}}

{{% tab header="R" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `DESCRIPTION`（`Imports`/`Suggests`） |
| 锁文件 | `renv.lock` |
| 常用命令 | `install.packages`、`renv::snapshot()`、`renv::restore()` |

```r
renv::init()                # 为项目建立环境与 renv.lock
renv::snapshot()             # 记录当前包版本
renv::restore()               # 按锁文件还原
```

CRAN 上的包随时可能更新，`renv` 的价值就是把"某个时间点的版本集合"冻结下来，保证脚本长期可复现。

📘 [renv](https://rstudio.github.io/renv/)

{{% /tab %}}

{{% tab header="Zig" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `build.zig.zon` |
| 锁文件 | 不需要——URL + 内容哈希即锁定 |
| 常用命令 | `zig fetch --save`、`zig build` |

```zig
.dependencies = .{
    .zap = .{ .url = "https://.../zap-0.10.0.tar.gz", .hash = "zap-0.10.0-..." },
},
```

```bash
zig fetch --save https://github.com/zigzap/zap/archive/refs/tags/v0.10.0.tar.gz
```

哈希不匹配就拒绝构建，这是 Zig 与众不同的"锁定方式"：没有版本范围，只有"这个确切内容"。

📘 [Zig · build.zig.zon](https://ziglang.org/documentation/master/#Zig-Build-System)

{{% /tab %}}

{{% tab header="Lua" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `.rockspec` |
| 锁文件 | 无 |
| 常用命令 | `luarocks install`、`luarocks make`、`luarocks list` |

```lua
-- demo-0.1.0-1.rockspec 片段
dependencies = { "lua >= 5.4", "luafilesystem >= 1.8" }
build = { type = "builtin", modules = { demo = "demo.lua" } }
```

```bash
luarocks make              # 用当前 rockspec 构建并安装
luarocks install --local demo
```

LuaRocks 没有锁文件；要可复现就写清版本范围，或把依赖连同 rockspec 一起 vendor 进仓库。

📘 [LuaRocks · rockspec](https://github.com/luarocks/luarocks/wiki/Rockspec-format)

{{% /tab %}}

{{% tab header="TypeScript" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `package.json` |
| 锁文件 | `package-lock.json`、`pnpm-lock.yaml`、`yarn.lock` |
| 常用命令 | `npm ci`、`npm install`、`pnpm add`、`pnpm why` |

```jsonc
{
  "dependencies": { "zod": "^3.23.0" },
  "devDependencies": { "typescript": "^7.0.0", "@types/node": "^26.0.0" }
}
```

```bash
npm ci             # 严格按锁文件安装（CI 专用）
pnpm why zod       # 看某个包为什么被装进来
```

`devDependencies` 与 `dependencies` 要分清：类型包、构建工具放 dev，运行时用到的放 dependencies。

📘 [npm · package.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-json)

{{% /tab %}}

{{% tab header="JavaScript" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `package.json` |
| 锁文件 | `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` |
| 常用命令 | `npm install`、`npm ci`、`npm audit`、`npm outdated` |

```jsonc
{
  "engines": { "node": ">=26" },
  "overrides": { "minimist": "^1.2.8" },     // npm 强制指定传递依赖版本
  "scripts": { "start": "node src/main.js" }
}
```

```bash
npm ls --all | head
npm audit fix
```

`overrides`（npm）/`resolutions`（yarn）/`pnpm.overrides` 用来强行统一传递依赖版本，是排查"某个老版本漏洞包"的直接手段。

📘 [npm · package-lock.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json)

{{% /tab %}}

{{% tab header="PHP" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `composer.json` |
| 锁文件 | `composer.lock`（必须提交） |
| 常用命令 | `composer install`、`require`、`update`、`show --tree` |

```jsonc
{
  "require": { "php": "^8.5", "guzzlehttp/guzzle": "^7.9" },
  "config": { "platform": { "php": "8.5.0" } }
}
```

```bash
composer install            # 按 composer.lock 安装（CI/生产）
composer update             # 升级并更新锁文件（本地）
composer show --tree guzzlehttp/guzzle
```

`config.platform` 可以模拟目标 PHP 版本/扩展，避免"本地 8.5 装得上、线上 8.3 装不上"。

📘 [Composer · 依赖](https://getcomposer.org/doc/04-schema.md)

{{% /tab %}}

{{% tab header="Ruby" %}}

| 项目 | 内容 |
| --- | --- |
| 清单 | `Gemfile`（应用）/ `.gemspec`（库） |
| 锁文件 | `Gemfile.lock`（必须提交） |
| 常用命令 | `bundle install`、`bundle update`、`bundle exec`、`bundle why` |

```ruby
# Gemfile
source "https://rubygems.org"
gem "rails", "~> 8.0"
gem "puma", ">= 6.4"
```

```bash
bundle install                # 按 Gemfile.lock 安装
bundle update rails            # 只升级 rails
bundle exec ruby main.rb        # 使用锁定版本运行
```

`bundle exec` 是 Ruby 项目的纪律：不加前缀就可能用到系统里另一个版本的 gem。

📘 [Bundler · Gemfile](https://bundler.io/man/gemfile.5.html)

{{% /tab %}}

{{< /tabpane >}}

### 包仓库与发布

发布这件事在各语言里的门槛差别很大：有的一个命令就进中心仓库，有的根本没有中心仓库（只能给 Git URL）。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | crates.io |
| 发布 | `cargo publish`（需 `cargo login`） |
| 撤回 | `cargo yank --version 1.0.1` |
| 私有源 | 在 `~/.cargo/config.toml` 里换 registry（如 Artifactory） |

```bash
cargo login <token>
cargo publish --dry-run     # 先本地检查
cargo publish
```

`publish` 前会被 `cargo package` 的检查拦住明显问题（缺 license、路径依赖等）；`yank` 只是阻止新项目选它，已有 `Cargo.lock` 不受影响。

📘 [cargo publish](https://doc.rust-lang.org/cargo/commands/cargo-publish.html)

{{% /tab %}}

{{% tab header="Swift" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | 无（Swift Package Index 只是目录） |
| 发布 | 打 Git tag，仓库即包 |
| 私有 | 私有 Git 仓库 + 凭据 |

```bash
git tag 1.5.0 && git push origin 1.5.0     # tag 就是"发布"
swift package archive-source                # 打包源码（可选）
```

SwiftPM 直接按 URL + 版本标签抓取依赖，所以"发布"等于"打语义化版本的 tag"；Swift Package Index 负责索引与兼容性检查。

📘 [Swift Package Index](https://swiftpackageindex.com/)

{{% /tab %}}

{{% tab header="Go" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | 无（模块 = Git 仓库） |
| 发布 | `git tag v1.2.3` 并推送 |
| 代理 | `GOPROXY`（proxy.golang.org 或私有代理） |
| 私有 | `GOPRIVATE`/`GONOSUMDB` 绕过校验 |

```bash
git tag v1.2.3 && git push origin v1.2.3
go list -m -versions example.com/demo        # 查看可用版本
GOPROXY=off go build                          # 完全离线（配合 vendor）
```

主版本 ≥ 2 时，模块路径必须带 `/v2`（`example.com/demo/v2`），这是 Go 的强制约定。

📘 [Go · 模块版本](https://go.dev/ref/mod#versions)

{{% /tab %}}

{{% tab header="Python" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | PyPI（测试用 TestPyPI） |
| 发布 | `python -m build` + `twine upload`（或 `uv publish`） |
| 私有源 | `--index-url`/`PIP_INDEX_URL` 指向私有仓库 |

```bash
python -m build                    # 生成 wheel 与 sdist
twine check dist/*
twine upload --repository testpypi dist/*
twine upload dist/*
```

先用 TestPyPI 验证一遍（版本号不能重复）；私有包常见做法是自建 devpi/Artifactory 或直接 `pip install git+https://...`。

📘 [PyPI · 发布](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/)

{{% /tab %}}

{{% tab header="Kotlin" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | Maven Central（通过 Sonatype） |
| 发布 | `maven-publish` 插件 + `publishToMavenCentral` |
| 本地 | `publishToMavenLocal` |
| 私有 | Nexus / Artifactory |

```kotlin
plugins { `maven-publish` }
publishing {
    publications { create<MavenPublication>("lib") { from(components["java"]) } }
}
```

```bash
./gradlew publishToMavenLocal
./gradlew publish
```

发布到 Maven Central 需要签名（GPG）与命名空间验证，一次性配置好之后就是流水线里的一个任务。

📘 [Maven Central 发布](https://central.sonatype.org/publish/)

{{% /tab %}}

{{% tab header="Java" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | Maven Central |
| 发布 | `mvn deploy`（配 distributionManagement） |
| 本地 | `mvn install` |
| 私有 | Nexus / Artifactory |

```xml
<distributionManagement>
  <repository><id>central</id><url>https://...</url></repository>
</distributionManagement>
```

```bash
mvn -DskipTests deploy
```

`mvn install` 只进本地仓库，`deploy` 才推送；Central 要求提供 sources/javadoc 附件并签名。

📘 [Maven · 部署](https://maven.apache.org/plugins/maven-deploy-plugin/)

{{% /tab %}}

{{% tab header="C++" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | 无官方；vcpkg registry、Conan Center |
| 发布 | vcpkg 提交 port / `conan upload` |
| 私有 | 自建 Conan server、私有 vcpkg registry |

```bash
conan create . --build=missing
conan upload demo/0.1.0 -r my-remote
vcpkg x-add-version demo            # 向 vcpkg 提交新版本
```

C++ 的现实是：**分发源码与构建脚本**比分发二进制更常见（ABI 不统一）；二进制分发通常绑定具体编译器/标准库版本。

📘 [Conan · 上传](https://docs.conan.io/2/reference/commands/upload.html)、[vcpkg registry](https://learn.microsoft.com/en-us/vcpkg/producers/packaging/registries)

{{% /tab %}}

{{% tab header="C" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | 无 |
| 发布 | 打源码 tarball + `make install`；或交给发行版打包 |
| 私有 | 内部源码仓库 / 内部 apt 源 |

```bash
./configure --prefix=/usr/local && make && sudo make install
make dist                      # Autotools 的源码包目标
```

分发约定是 `./configure && make && make install` 或 CMake 的 `cmake --install`；`pkg-config` 文件随包安装，供其他项目发现。

📘 [GNU 编码标准 · 发布](https://www.gnu.org/prep/standards/html_node/Releases.html)

{{% /tab %}}

{{% tab header="Julia" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | General Registry（GitHub PR 提交） |
| 发布 | 打 tag + 向 Registry 提 PR（可用 `Pkg.Registry`/`LocalRegistry`） |
| 私有 | 自建 registry（Git 仓库）+ `Pkg.Registry.add` |

```julia
using Pkg
Pkg.activate(".")
Pkg.Registry.add("General")
# 发布：给包仓库打 tag 后向 General registry 提 PR
```

Julia 的注册中心本质是一个 Git 仓库（记录包名、UUID、版本与仓库地址），所以私有 registry 就是"自己的一个 Git 仓库"。

📘 [Registries](https://pkgdocs.julialang.org/v1/registries/)

{{% /tab %}}

{{% tab header="C#" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | NuGet.org |
| 发布 | `dotnet pack` + `dotnet nuget push` |
| 私有 | `nuget.config` 配置私有 feed |

```bash
dotnet pack -c Release -o out
dotnet nuget push out/Demo.1.0.0.nupkg --api-key $KEY --source https://api.nuget.org/v3/index.json
```

内部包常见于 Azure Artifacts / GitHub Packages / 自建 BaGet；`nuget.config` 决定还原时按什么顺序查源。

📘 [dotnet pack](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-pack)

{{% /tab %}}

{{% tab header="Dart" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | pub.dev |
| 发布 | `dart pub publish` |
| 私有 | Git 依赖、`dependency_overrides`、自建 pub server |

```bash
dart pub publish --dry-run     # 先检查要发布什么
dart pub publish
```

发布前 pub.dev 会做静态检查（分数）；私有包通常直接用 `git:` 依赖或 `path:` 依赖，团队内共享即可。

📘 [dart pub publish](https://dart.dev/tools/pub/publishing)

{{% /tab %}}

{{% tab header="R" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | CRAN（人工审核）、Bioconductor、R-universe |
| 发布 | `devtools::release()` / `R CMD check --as-cran` + 提交 |
| 私有 | 内部包仓库（miniCRAN、drat） |

```r
devtools::check_win_devel()      # 提交前的多平台检查
devtools::release()               # 引导式发布流程
```

CRAN 审核严格（示例、文档、跨平台检查都要过），所以很多团队先用 R-universe 或内部仓库分发，成熟后再上 CRAN。

📘 [CRAN · 提交](https://cran.r-project.org/submit.html)

{{% /tab %}}

{{% tab header="Zig" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | 无 |
| 发布 | 打 tarball / 推 Git tag，消费方用 URL + 哈希 |
| 私有 | 任意 HTTP 服务或私有 Git |

```bash
zig fetch --save https://example.com/demo-0.1.0.tar.gz
```

没有版本解析，所以"发布"就是提供不可变内容（tarball 或 tag）；哈希由消费方第一次 fetch 时记录并提交进 `build.zig.zon`。

📘 [Zig · 依赖](https://ziglang.org/documentation/master/#Zig-Build-System)

{{% /tab %}}

{{% tab header="Lua" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | luarocks.org |
| 发布 | `luarocks upload` |
| 私有 | 自建 rocks server 或只走源码 |

```bash
luarocks upload demo-0.1.0-1.rockspec --api-key $KEY
luarocks install demo
```

发布前先用 `luarocks make` 在本地走一遍完整构建，确认 `dependencies` 与 `build.modules` 正确。

📘 [LuaRocks · 上传](https://github.com/luarocks/luarocks/wiki/luarocks-upload)

{{% /tab %}}

{{% tab header="TypeScript" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | npm Registry |
| 发布 | `npm publish`（scope 包需 `--access public`） |
| 私有 | 私有 scope + 私有 registry（Verdaccio、GitHub Packages） |

```bash
npm login
npm publish --dry-run           # 检查会发布哪些文件
npm publish --access public
npm version patch && npm publish  # 自动改版本并发布
```

`files` 字段与 `.npmignore` 决定包里带什么；TypeScript 包要同时发 `.js` 与 `.d.ts`（`declaration: true`）。

📘 [npm · 发布](https://docs.npmjs.com/cli/v11/commands/npm-publish)

{{% /tab %}}

{{% tab header="JavaScript" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | npm Registry |
| 发布 | `npm publish`（`prepublishOnly` 里跑测试/构建） |
| 私有 | scoped 包 + 私有 registry |

```jsonc
{
  "files": ["dist"],
  "scripts": { "prepublishOnly": "npm test && npm run build" }
}
```

```bash
npm pack            # 生成 tarball 并检查内容（发布前强烈建议）
npm publish
```

`npm pack` 是最便宜的预检：它把将要上传的 tarball 解出来给你看，避免把源码、密钥或测试数据打进包里。

📘 [npm · 包内容](https://docs.npmjs.com/cli/v11/using-npm/developers)

{{% /tab %}}

{{% tab header="PHP" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | Packagist |
| 发布 | 提交 VCS 地址即可（打 tag 触发更新） |
| 私有 | Private Packagist、Satis、Composer 的 `repositories` |

```bash
composer validate --strict
# 在 Packagist 提交 https://github.com/you/demo 后，推 tag 即发布版本
git tag v1.0.0 && git push origin v1.0.0
```

Packagist 不存代码，只做索引：`composer.json` 里的 `name` + VCS 仓库 + tag 就是一次发布；私有包用 `repositories` 指向内部 VCS 或 Satis。

📘 [Packagist](https://packagist.org/about)

{{% /tab %}}

{{% tab header="Ruby" %}}

| 项目 | 内容 |
| --- | --- |
| 注册中心 | RubyGems.org |
| 发布 | `gem build` + `gem push`（rake release 自动化） |
| 私有 | 私有 gem server（Gem in a Box、Gemfury） |

```bash
gem build demo.gemspec
gem push demo-0.1.0.gem
rake release            # 打 tag + 构建 + 推送（项目里常用）
```

`gem push` 前确认 `spec.files` 用 `git ls-files` 之类的方式限定，避免把本地临时文件带进包里。

📘 [RubyGems · 发布](https://guides.rubygems.org/publishing/)

{{% /tab %}}

{{< /tabpane >}}

### 版本约束、工作区与常见坑

最后看三件事：**版本号怎么写**、**多包项目怎么组织（workspace）**、**最常踩的坑**。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | `"1.2.3"` = `^1.2.3`（≥1.2.3 且 <2.0.0）、`~1.2.3`、`=1.2.3`、`*` |
| 工作区 | `[workspace]` 共享 `Cargo.lock` 与 `target/` |
| 常见坑 | 同一 crate 出现多个大版本（`cargo tree -d`）、feature 统一（unification）导致意外启用 |

```toml
[workspace]
members = ["crates/*"]
resolver = "3"

[workspace.dependencies]
serde = "1"
```

`resolver = "2"`/`"3"` 决定 feature 与目标平台的合并规则；子 crate 用 `serde.workspace = true` 复用统一版本。

📘 [Cargo · 工作区](https://doc.rust-lang.org/cargo/reference/workspaces.html)

{{% /tab %}}

{{% tab header="Swift" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | `from: "1.5.0"`（语义化范围）、`.exact("1.5.0")`、`.branch`、`.revision` |
| 工作区 | 一个 `Package.swift` 可有多个 target/product；多包用本地路径依赖 |
| 常见坑 | 同一依赖被要求不同版本 → 解析失败；`Package.resolved` 冲突 |

```swift
.package(path: "../LocalLib"),
.package(url: "https://.../swift-arg.git", exact: "1.5.0"),
```

SwiftPM 对每个依赖只能选**一个**版本（不像 Cargo 允许多版本共存），所以版本冲突必须显式解决。

📘 [SwiftPM · 依赖规则](https://www.swift.org/documentation/package-manager/)

{{% /tab %}}

{{% tab header="Go" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | 语义化标签 `v1.2.3`；伪版本 `v0.0.0-20260919120000-abcdef123456` |
| 工作区 | `go.work`（多模块本地开发） |
| 常见坑 | 主版本 ≥2 必须在模块路径写 `/v2`；`replace` 只在本机生效 |

```bash
go work init ./a ./b
go work use ./c
```

```
// go.mod
require example.com/demo/v2 v2.1.0     // 主版本必须体现在路径里
replace example.com/demo => ../demo    // 本地调试用
```

Go 的 MVS 只会**升**不会自动降；要降版本得显式 `go get pkg@older`。

📘 [Go · 模块版本](https://go.dev/ref/mod#versions)

{{% /tab %}}

{{% tab header="Python" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | `~=1.4.2`（兼容版本）、`>=1.2,<2`、`==1.4.2`、`*` |
| 工作区 | 单仓库多包常用 `src/` 布局 + path 依赖；uv 支持 workspace |
| 常见坑 | 无锁文件不可复现、依赖冲突（ResolutionImpossible）、extras 写法遗漏 |

```toml
dependencies = ["httpx>=0.27,<1"]

[project.optional-dependencies]
dev = ["pytest>=8"]
```

```bash
uv sync --all-extras
pip install "httpx>=0.27,<1"
```

pip 的解析器从 20.3 起会回溯求解，但冲突时仍可能报 `ResolutionImpossible`；用 uv 这类带锁的工具能提前发现问题。

📘 [PEP 440 · 版本标识](https://peps.python.org/pep-0440/)

{{% /tab %}}

{{% tab header="Kotlin" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | Gradle 的 `1.2.3` 表示"最高 1.2.3"；可用 `strictly`/`prefer`/`require` 精确控制 |
| 工作区 | Gradle 多模块（`settings.gradle.kts` 里 `include`） |
| 常见坑 | 传递依赖版本冲突默认选最高、Kotlin 插件版本与 Gradle 版本匹配 |

```kotlin
dependencies {
    implementation("org.slf4j:slf4j-api") { version { strictly("2.0.16") } }
}
```

多模块项目用 `implementation(project(":core"))` 引用本地模块；版本集中在 `libs.versions.toml` 管理最省心。

📘 [Gradle · 版本约束](https://docs.gradle.org/current/userguide/dependency_constraints_conflicts.html)

{{% /tab %}}

{{% tab header="Java" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | Maven 范围 `[1.0,2.0)`、`[1.0,)`；普通写法表示"推荐版本" |
| 工作区 | Maven 多模块（父 pom + `<modules>`） |
| 常见坑 | 最近优先（nearest-wins）导致传递依赖版本漂移、依赖冲突只在运行期暴露 |

```xml
<dependency>
  <groupId>com.google.guava</groupId>
  <artifactId>guava</artifactId>
  <version>[33.0,34.0)</version>
</dependency>
```

用 `dependencyManagement` 把关键传递依赖钉在顶层，是防漂移的标准手段；`mvn dependency:tree -Dverbose` 能看出被剪掉的版本。

📘 [Maven · 依赖调解](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html#dependency-mediation)

{{% /tab %}}

{{% tab header="C++" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | vcpkg 用 `overrides` 固定版本；Conan 用 `requires` + 语义化版本 |
| 工作区 | CMake 的 `add_subdirectory` 或 Conan workspace |
| 常见坑 | ABI 不一致（编译器/标准库不同）、ODR 违规、同名符号冲突 |

```jsonc
{ "overrides": [{ "name": "fmt", "version": "11.0.2" }] }
```

C++ 的"依赖地狱"根源是**二进制不兼容**：即使版本号相同，编译器或 `-D_GLIBCXX_USE_CXX11_ABI` 不同也可能链不上。

📘 [vcpkg · 版本控制](https://learn.microsoft.com/en-us/vcpkg/users/versioning)

{{% /tab %}}

{{% tab header="C" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | 无（依赖系统包管理器） |
| 工作区 | 无（Make/CMake 子目录） |
| 常见坑 | 头文件与库版本不匹配、符号冲突、`pkg-config` 找不到时静默用错版本 |

```bash
pkg-config --modversion openssl
pkg-config --exists "openssl >= 3.0" && echo ok
```

在 `configure`/CMake 里显式检查版本（而不只是"找到了库"）能避免运行期才暴露的 ABI 问题。

📘 [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/)

{{% /tab %}}

{{% tab header="Julia" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | `[compat]` 写 `"1.7"`（= 1.7 ≤ x < 2）、`"~1.7.2"`、`"=1.7.2"` |
| 工作区 | 多个项目共用 `Manifest.toml` 或用 `Pkg.develop` 挂本地包 |
| 常见坑 | Manifest 与 Project 不一致、忘记 `Pkg.instantiate`、registry 未更新 |

```toml
[compat]
DataFrames = "1.7"
julia = "1.13"
```

`[compat]` 是 Julia 包发布的必需项：没有它，下游无法保证兼容范围。

📘 [Pkg · 兼容性](https://pkgdocs.julialang.org/v1/compatibility/)

{{% /tab %}}

{{% tab header="C#" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | NuGet 范围 `[1.0,2.0)`、`1.2.*`、`[1.0]` |
| 工作区 | 解决方案（`.sln`）+ 中央包管理 |
| 常见坑 | 传递依赖降级（NU1605 警告，可提升为错误）、多目标框架差异 |

```xml
<PackageReference Include="Serilog" Version="[4.2.0,5.0.0)" />
```

```bash
dotnet restore -warnaserror:NU1605     # 把降级警告当错误
```

中央包管理（`Directory.Packages.props`）让版本只写一次；多目标框架用 `Condition` 区分。

📘 [NuGet · 版本范围](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning)

{{% /tab %}}

{{% tab header="Dart" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | `^1.2.0`（默认，<2.0.0）、`>=1.2.0 <2.0.0`、`any` |
| 工作区 | pub workspace（Dart 3.6+） |
| 常见坑 | 版本求解失败（多个包要求互斥区间）、`any` 引入不兼容更新 |

```yaml
dependency_overrides:      # 应急：强制覆盖某个包的依赖
  http: ^1.2.0
```

`dart pub outdated` 会列出"可升级、可大版本升级、被约束卡住"三类，是排查求解失败的第一步。

📘 [pub · 版本约束](https://dart.dev/tools/pub/dependencies)

{{% /tab %}}

{{% tab header="R" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | `DESCRIPTION` 里写 `pkg (>= 1.2.0)`，没有范围语法 |
| 工作区 | `renv` 项目级环境（一个项目一份锁文件） |
| 常见坑 | CRAN 包不保证向后兼容、系统库依赖（libcurl/openssl）缺失、Bioconductor 版本与 R 版本绑定 |

```r
# DESCRIPTION
Imports: dplyr (>= 1.1.0), tidyr
```

```r
renv::diagnostics()      # 检查环境与锁文件是否一致
```

Bioconductor 的包按 R 版本发布（BiocManager 会选匹配版本），跨版本升级要整体走一次 release 流程。

📘 [renv · 版本](https://rstudio.github.io/renv/articles/renv.html)

{{% /tab %}}

{{% tab header="Zig" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | 无范围：URL + 哈希（哈希即精确版本） |
| 工作区 | 无（build.zig 里组合模块） |
| 常见坑 | 依赖 API 不稳定（0.x 时代常破坏性变更）、重新打包 tarball 会改变哈希 |

```bash
zig fetch --save=dep https://example.com/dep.tar.gz   # 记录哈希
zig build --summary all                                # 查看依赖与耗时
```

因为哈希对内容敏感，依赖方不要"重新打包"上游 tarball；直接引用官方发布物或 Git archive。

📘 [Zig · 包管理](https://ziglang.org/documentation/master/#Zig-Build-System)

{{% /tab %}}

{{% tab header="Lua" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | rockspec 里 `dependencies = { "lua >= 5.4", "lfs ~> 1.8" }` |
| 工作区 | 无（`LUA_PATH`/`LUA_CPATH` 控制搜索路径） |
| 常见坑 | 全局安装互相污染、C 模块与 Lua 版本/ABI 绑定、路径写错导致 require 失败 |

```lua
print(package.path)     -- 查看模块搜索路径
print(package.cpath)     -- C 模块搜索路径
```

团队项目建议 `luarocks install --tree ./lua_modules --local` 把依赖装进项目目录，再用 `LUA_PATH` 指向它。

📘 [LuaRocks · 依赖](https://github.com/luarocks/luarocks/wiki/Dependencies)

{{% /tab %}}

{{% tab header="TypeScript" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | `^1.2.3`（默认）、`~1.2.3`、`>=1.2 <2`、`workspace:*` |
| 工作区 | npm/pnpm/yarn workspaces、TS project references |
| 常见坑 | peer 依赖缺失、锁文件不同步导致 `npm ci` 失败、幽灵依赖（pnpm 收紧） |

```jsonc
{ "workspaces": ["packages/*"] }
```

```bash
npm ci                          # 锁文件与 package.json 不一致会直接报错
pnpm -r exec tsc --noEmit        # 在所有工作区跑类型检查
```

类型包与运行时包版本要对齐（`@types/node` 与 Node 版本），否则会出现在编译期能过、运行期属性不存在的怪问题。

📘 [npm workspaces](https://docs.npmjs.com/cli/v11/using-npm/workspaces)

{{% /tab %}}

{{% tab header="JavaScript" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | 同 npm（`^`/`~`/`>=`），`overrides` 强制传递依赖版本 |
| 工作区 | workspaces + 单一锁文件 |
| 常见坑 | 多个版本的同名包被打进 bundle（体积翻倍）、CJS/ESM 双包问题（dual package hazard） |

```bash
npm ls lodash            # 看是否装了多个版本
npm dedupe                # 尽量合并版本
```

打包前用 `npm ls <pkg>` 确认没有重复版本；库作者要同时提供 ESM 与 CJS 时，注意"同一模块被加载两次"的状态问题。

📘 [npm · overrides](https://docs.npmjs.com/cli/v11/configuring-npm/package-json#overrides)

{{% /tab %}}

{{% tab header="PHP" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | `^1.2`、`~1.2`、`>=1.2 <2.0`、`dev-main` |
| 工作区 | 无（多包用 path repository） |
| 常见坑 | 平台扩展要求（`ext-json`、`ext-mbstring`）、`composer.lock` 与生产不一致、dev 分支被误用 |

```jsonc
{
  "require": { "php": "^8.5", "ext-json": "*" },
  "repositories": [{ "type": "path", "url": "../local-lib" }]
}
```

`composer check-platform-reqs` 能在部署前验证目标环境是否满足扩展与 PHP 版本要求。

📘 [Composer · 版本约束](https://getcomposer.org/doc/articles/versions.md)

{{% /tab %}}

{{% tab header="Ruby" %}}

| 项目 | 内容 |
| --- | --- |
| 版本语法 | `~> 1.2`（≥1.2 且 <2.0）、`~> 1.2.3`（≥1.2.3 且 <1.3）、`>= 1.2` |
| 工作区 | 无原生 workspace；多 gem 用 path 依赖 |
| 常见坑 | 原生扩展编译失败、`Gemfile.lock` 平台差异、Bundler 版本不一致 |

```ruby
gem "rails", "~> 8.0"
gem "local_lib", path: "../local_lib"
```

```bash
bundle lock --add-platform x86_64-linux    # 让锁文件兼容部署平台
bundle platform                             # 查看当前平台
```

`~>` 的宽度取决于位数：`~> 1.2` 允许到 2.0 之前，`~> 1.2.3` 只到 1.3 之前——这是 Ruby 里最容易写错的版本约束。

📘 [Bundler · Gemfile](https://bundler.io/man/gemfile.5.html)

{{% /tab %}}

{{< /tabpane >}}

---

> 本页覆盖 18 种语言的包管理与模块：**模块与命名空间、依赖声明与锁定、包仓库与发布、版本约束与工作区**。清单/锁文件名与命令均按各语言当前稳定版整理；"没有"这种机制的语言（C 的模块、Go/Zig 的中心仓库）也在正文中说明了替代做法。

> 版本基线（2026-09）：Rust 1.98、Swift 6.4、Go 1.27、Python 3.14、Kotlin 2.4、Java 26（LTS 25）、C++23、C23、Julia 1.13、C# 14 / .NET 10、Dart 3.13、R 4.6、Zig 0.15、Lua 5.5、TypeScript 7、Node 26、PHP 8.5、Ruby 4.0。
