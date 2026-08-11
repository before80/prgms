+++
title = "49-部署与 Docker"
date = 2026-07-28T14:49:00+08:00
weight = 490
type = "docs"
description = "面向 Go 用户讲清 Rust 二进制部署、多阶段 Docker、镜像底座、健康检查与 CI 缓存"
isCJKLanguage = true
draft = false

+++

# 部署与 Docker (Deployment and Docker)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否想知道：Rust 二进制部署和 Go 有多像，release 构建要检查哪些项？
- 你是否想写最小多阶段 **Dockerfile**，却踩到缺 CA、时区、glibc 或底座选型？
- 你是否纠结：distroless / scratch / alpine / debian、何时考虑 **musl** 静态链接？
- 你是否想对齐健康检查与优雅退出、配置密钥注入、CI 里缓存 cargo 依赖？
- 你是否关心：容器资源限制、tokio worker，以及日志/metrics 怎么接可观测？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| release | — | 发布构建 | `cargo build --release`，开优化 | `go build -ldflags` 发布构建 |
| Dockerfile | — | 镜像构建脚本 | 描述如何打容器镜像 | 同名 |
| multi-stage | — | 多阶段构建 | 编译阶段与运行阶段分离，减小镜像 | 同模式 |
| **distroless** | — | 极简运行镜像 | 几乎无 shell/包管理器，只跑应用 | 同系列镜像 |
| **scratch** | — | 空镜像 | 从零开始，只 COPY 二进制等 | 同名 |
| **alpine** | — | 小体积 Linux | 常用 musl；包少、镜像小 | 同名 |
| **debian** | — | 常见 glibc 发行版 | 兼容性好、调试工具易装 | 同名 |
| **glibc** | GNU C Library | GNU C 库 | 多数 Linux 发行版默认 C 运行时 | 动态链接时常依赖 |
| **musl** | — | 另一套 C 库 | 静态链接常见搭档；alpine 用它 | `CGO_ENABLED`+musl 类比 |
| CA | Certificate Authority | 证书颁发机构 | TLS 校验需要根证书包 | `ca-certificates` |
| health check | — | 健康检查 | 探针判断进程是否就绪/存活 | Docker `HEALTHCHECK` / K8s probe |
| graceful shutdown | — | 优雅退出 | 停接新流量，等在途请求结束 | `Shutdown`；见 [40-http](../40-http-client-and-server/) |
| CI | Continuous Integration | 持续集成 | 自动构建测试流水线 | 同概念 |
| **tokio** | — | 异步运行时 | 常见 async executor；见 [31-async](../31-async-programming/) | goroutine 调度器类比 |
| metrics | — | 指标 | 延迟、QPS、错误率等数值序列 | Prometheus 客户端等 |
| stdout | — | 标准输出 | 容器日志常收集这里 | 同概念 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q7](#q7) |
| `common` | [Q6](#q6), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12) |
| `occasional` | — |
| `advanced` | — |

---

## Q1. Rust 二进制部署和 Go 有多像？ {#q1}
**Tags:** `hot` `beginner` `deploy` `binary`
**适用版本:** Rust 1.x；与 Go 单二进制文化对照

**一句话答案：**
很像：都是「编译出一个（或少数）可执行文件 + 配置/迁移资源」再拷到服务器或镜像里。差异主要在：依赖动态库（glibc/openssl）更敏感、编译更慢、release 优化要显式 `--release`，以及 async 运行时参数要按负载调。

**解答：**
相同点：

```text
Go:  go build -o app ./cmd/app
     拷贝 app + 配置 → 跑

Rust: cargo build --release
      拷贝 target/release/app + 配置 → 跑
```

不同点（部署视角）：

| 点 | Rust | Go |
|----|------|-----|
| 默认产物 | 动态链接常见（尤其 openssl/native） | 常静态感更强（视 CGO） |
| 优化开关 | 务必 `--release` | 默认已较接近发布 |
| 构建时间 | 通常更长，CI 要缓存 | 通常更快 |
| 运行时 | 可能嵌 tokio 等 | 自带调度 |

本地确认产物：

```bash
cargo build --release
# Windows: target\release\<name>.exe
# Unix:    target/release/<name>
```

「❌ 错误写法」——把 `cargo build`（debug）产物直接上生产：体积大、慢、断言行为也可能不同。

**Go 对比：**
- **Go 怎么做**：`go build` 出单文件，scp/镜像跑起来。
- **Rust 为什么不同**：同样单文件文化，但对 C 库与 profile 更「显性」。
- **Go 程序员易踩的坑**：以为 `cargo run` 的二进制就是发布物——缺 `--release`。

**记忆点：**
- 部署物 = **release 二进制** + 配置。
- 像 Go，但更盯链接与 profile。

---

## Q2. release 构建检查清单（链 03/23） {#q2}
**Tags:** `hot` `release` `checklist` `cargo`
**适用版本:** 与 [03-compilation](../03-compilation/)、[23-cargo-workflow](../23-cargo-workflow/) 一致

**一句话答案：**
用 `cargo build --release`（或 `cargo install --path .`），确认 `Cargo.lock` 已提交、目标三元组正确、需要的 feature 已打开、版本/符号信息符合发布策略。细节见编译与 Cargo 工作流两篇。

**解答：**
上线前清单：

```text
[ ] cargo build --release 成功（同一 lockfile）
[ ] 测过：cargo test --release（若关心优化下行为）
[ ] Cargo.lock 在应用仓库中已版本控制
[ ] 目标平台匹配（本机 gnu ≠ 容器 linux）
[ ] 需要的 Cargo features 与 TLS 后端已选定
[ ] 日志级别、RUST_LOG 等默认合理
[ ] 二进制能 --help / 健康检查路径可打通（有则测）
```

常用命令：

```bash
cargo build --release
cargo test --release
# 交叉或指定目标时：
# cargo build --release --target x86_64-unknown-linux-gnu
```

`Cargo.toml` 里可按需拧 profile（示意，详见 [23-cargo-workflow](../23-cargo-workflow/)）：

```toml
[profile.release]
lto = true
codegen-units = 1
# panic = "abort"   # 按团队策略，不是默认必须
```

编译原理与优化直觉见 [03-compilation](../03-compilation/)。

**Go 对比：**
```bash
go build -trimpath -ldflags="-s -w" -o app .
```
- **Go 怎么做**：ldflags 削符号、trimpath 可复现。
- **Rust 为什么不同**：优化在 `profile.release`；削符号可用 strip 等，不靠同一套 ldflags 习惯。
- **Go 程序员易踩的坑**：只在本机 Windows 编好，丢进 Debian 容器却因链接器/目标不对跑不起来。

**记忆点：**
- `--release` + lockfile + 正确 target。
- 深挖链 [03](../03-compilation/)、[23](../23-cargo-workflow/)。

---

## Q3. 最小 Dockerfile：多阶段编译 {#q3}
**Tags:** `hot` `Dockerfile` `multi-stage`
**适用版本:** Docker 多阶段；Rust 官方/社区 builder 镜像

**一句话答案：**
**builder** 阶段装工具链、`cargo build --release`；**runtime** 阶段只 COPY 二进制（和必要的证书/时区文件）。这样最终镜像不含编译器与 `target/` 中间产物。

**解答：**
最小多阶段示意：

```dockerfile
# ---- build ----
FROM rust:1.85-bookworm AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release

# ---- run ----
FROM debian:bookworm-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/target/release/myapp /usr/local/bin/myapp
ENV RUST_LOG=info
EXPOSE 8080
CMD ["myapp"]
```

依赖缓存友好写法（先只拷清单，再拷源码）可减轻 CI 重编（见 [Q9](#q9)）：

```dockerfile
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs \
 && cargo build --release \
 && rm -rf src
COPY src ./src
RUN touch src/main.rs && cargo build --release
```

「❌ 错误写法」——单阶段 `FROM rust` 直接当运行镜像：镜像巨大，还带着编译器攻击面。

**Go 对比：**
```dockerfile
FROM golang:1.26 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app .
FROM gcr.io/distroless/static
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```
- **Go 怎么做**：同样多阶段；静态时很容易进 scratch/distroless。
- **Rust 为什么不同**：动态链接时 runtime 常要 glibc/证书，不能无脑 scratch。
- **Go 程序员易踩的坑**：照抄 Go 的 `FROM scratch` 却忘了 CA 与动态库（见 [Q4](#q4)、[Q5](#q5)）。

**记忆点：**
- builder 编译，slim/distroless 运行。
- 最终镜像只留二进制与运行必需品。

---

## Q4. 为什么镜像里常缺 CA / 时区 / glibc？ {#q4}
**Tags:** `hot` `CA` `timezone` `glibc`
**适用版本:** 容器运行时依赖

**一句话答案：**
极简镜像为了小，故意不带 **CA** 根证书、tzdata、调试壳。动态链接的 Rust 二进制还依赖宿主机有匹配的 **glibc**。缺 CA → HTTPS 失败；缺时区 → 日志时间怪；缺 glibc → `not found` / loader 错误。

**解答：**
症状对照：

| 缺失 | 典型现象 |
|------|----------|
| CA 证书包 | `reqwest`/TLS 校验失败、连不上外网 HTTPS |
| tzdata / 时区 | 时间显示 UTC 或解析本地时区失败 |
| glibc（或正确版本） | 二进制无法启动，loader 报错 |

补 CA（Debian 系）：

```dockerfile
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*
```

时区（按需）：

```dockerfile
RUN apt-get update \
 && apt-get install -y --no-install-recommends tzdata \
 && rm -rf /var/lib/apt/lists/*
ENV TZ=Asia/Shanghai
```

「❌ 错误思路」——在 scratch 里跑需要 HTTPS 的动态二进制，却既不 COPY 证书也不静态链接：线上第一请求就炸。

**Go 对比：**
- **Go 怎么做**：纯 Go TLS 时常自带根证逻辑；仍可能缺时区数据。CGO 同样吃 libc。
- **Rust 为什么不同**：rustls/native-tls 都要能读到系统信任库（或显式配置）。
- **Go 程序员易踩的坑**：Go 静态镜像「能上网」的经验平移到 Rust 动态镜像——缺 `ca-certificates`。

**记忆点：**
- 极简镜像 = 你显式装什么才有什么。
- HTTPS → CA；本地时间 → tzdata；动态链 → 匹配 glibc。

---

## Q5. distroless / scratch / alpine / debian 怎么选 {#q5}
**Tags:** `hot` `distroless` `scratch` `alpine` `debian`
**适用版本:** 镜像底座选型

**一句话答案：**
要调试方便、兼容性稳 → **debian** slim。要小且接受 musl 生态 → **alpine**。要攻击面极小、无 shell → **distroless**。只要静态二进制且你自备一切 → **scratch**。多数 Rust Web 服务从 `debian:*-slim` 或 distroless 起步最省心。

**解答：**

| 底座 | 优点 | 代价 |
|------|------|------|
| debian slim | glibc 熟、包好装、排障易 | 比 alpine/distroless 大 |
| alpine | 小 | musl；部分 crate/openssl 更磨人 |
| distroless | 无包管理器/壳，攻击面小 | 难进容器 debug |
| scratch | 最小 | 必须静态（或自带 loader/.so），无 CA 要自拷 |

决策树：

```text
需要 apt/排障？ ──是──→ debian slim
        │否
要用 musl/已验证 alpine？ ──是──→ alpine
        │否
静态且自备 CA？ ──是──→ scratch / distroless static
        │否
        └─→ distroless（cc/debian 系）或 debian slim
```

**Go 对比：**
- **Go 怎么做**：`CGO_ENABLED=0` 时常 distroless/static 或 scratch。
- **Rust 为什么不同**：默认不总是「一个文件零依赖」；底座要跟链接方式绑在一起选。
- **Go 程序员易踩的坑**：Alpine + 某些 native 依赖翻车，却以为是「Rust 不行」——其实是 musl/openssl 组合问题。

**记忆点：**
- 稳妥默认：**debian slim**。
- 更小更硬：distroless；极致：scratch + 静态。

---

## Q6. musl 静态链接何时考虑（windows/gnu 不展开） {#q6}
**Tags:** `common` `musl` `static`
**适用版本:** `x86_64-unknown-linux-musl` 等 Linux musl 目标

**一句话答案：**
当你要进 **scratch/alpine**、或希望「单个二进制拷到目标机就能跑、少依赖系统 libc」时，考虑 `*-linux-musl` 目标做静态（或近似静态）链接。有复杂 openssl/native 依赖时成本上升，需单独验证——本篇不展开 Windows/gnu 细节。

**解答：**
典型动机：

```text
✓ 发布到未知 Linux，不想绑特定 glibc 版本
✓ 镜像要用 scratch / 极简 alpine
✓ 运维要求「单一可执行文件」
```

目标示意：

```bash
rustup target add x86_64-unknown-linux-musl
# 常需 musl 工具链（跨平台构建机上额外安装）
cargo build --release --target x86_64-unknown-linux-musl
```

注意：
1. 不是所有 crate 对 musl 都零摩擦（尤其捆了 C 库时）。
2. 静态 ≠ 自动有 CA；HTTPS 仍要证书来源。
3. 体积可能变大；换的是可移植性。

**Go 对比：**
```bash
CGO_ENABLED=0 go build -o app .
```
- **Go 怎么做**：关 CGO 很容易出静态二进制。
- **Rust 为什么不同**：要显式 musl target + 工具链；纯 Rust 依赖时更顺。
- **Go 程序员易踩的坑**：以为 `cargo build --release` 默认就是 musl 静态——默认常是宿主 gnu。

**记忆点：**
- 要 scratch/少 libc 绑定时再上 musl。
- 有原生 C 依赖先做验证构建。

---

## Q7. 健康检查与优雅退出（链 40） {#q7}
**Tags:** `hot` `health` `graceful-shutdown`
**适用版本:** 容器编排；HTTP 细节见 [40-http-client-and-server](../40-http-client-and-server/)

**一句话答案：**
给编排暴露 **liveness/readiness**（常是 `/healthz` `/readyz`）；收到 SIGTERM 时停止接新请求、排空在途，再退出——Rust/axum 与 Go 一样要显式做 **graceful shutdown**，细节见 [40-http](../40-http-client-and-server/)。

**解答：**
Docker 层：

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8080/healthz || exit 1
```

K8s 直觉（示意）：

```text
livenessProbe:  进程活着吗？失败 → 重启
readinessProbe: 能接流量吗？失败 → 摘流量
```

进程内优雅退出要点：
1. 监听 SIGTERM/SIGINT。
2. 停止 accept / 从负载均衡摘流（readiness 先失败）。
3. 等待在途请求完成（带超时）。
4. 关掉连接池、刷新日志，再 `exit`。

HTTP 服务侧实现模式见 [40-http-client-and-server](../40-http-client-and-server/) 优雅关停相关题。

「❌ 错误写法」——忽略信号，K8s 直接 SIGKILL：请求半截断开、连接池来不及关。

**Go 对比：**
```go
srv.Shutdown(ctx)
```
- **Go 怎么做**：`http.Server.Shutdown`。
- **Rust 为什么不同**：用 hyper/axum + signal + 取消 token；概念同。
- **Go 程序员易踩的坑**：只写了 `/healthz` 恒返回 200，依赖未就绪也标 ready。

**记忆点：**
- 探针 + SIGTERM 排空 = 基本功。
- 实现细节链 [40](../40-http-client-and-server/)。

---

## Q8. 配置与密钥注入（env/文件，链 44） {#q8}
**Tags:** `common` `config` `secrets` `env`
**适用版本:** 与 [44-configuration](../44-configuration/) 一致

**一句话答案：**
容器里用环境变量或挂载文件注入配置与密钥；**不要**把密钥烤进镜像层。读取方式与分层覆盖见 [44-configuration](../44-configuration/)：Default → 文件 → env（→ CLI）。

**解答：**
常见注入：

```text
# Compose / K8s
environment:
  DATABASE_URL: postgres://...
  REDIS_URL: redis://...
# 或
volumes:
  - ./secrets/db_password:/run/secrets/db_password:ro
```

镜像构建时：

```dockerfile
# ✅ 运行时注入
ENV RUST_LOG=info
# ❌ 不要：
# ENV DATABASE_PASSWORD=super-secret
```

应用侧只读 env（std）：

```rust
fn main() {
    match std::env::var("DATABASE_URL") {
        Ok(url) => println!("DATABASE_URL len={}", url.len()),
        Err(_) => eprintln!("DATABASE_URL missing"),
    }
}
```

密钥文件可读 `/run/secrets/...`；完整分层与 figment/serde 见 [44-configuration](../44-configuration/)。

**Go 对比：**
- **Go 怎么做**：`os.Getenv` / Viper；K8s Secret 同挂 env 或文件。
- **Rust 为什么不同**：同样模式；配置库选型见 44。
- **Go 程序员易踩的坑**：`ARG`/`ENV` 在 Dockerfile 写死密码——进层历史。

**记忆点：**
- 密钥运行时注入，不进镜像。
- 分层细节链 [44](../44-configuration/)。

---

## Q9. CI 构建缓存 cargo 依赖 {#q9}
**Tags:** `common` `CI` `cache` `cargo`
**适用版本:** GitHub Actions 等 CI；思路通用

**一句话答案：**
缓存 `~/.cargo/registry`、`~/.cargo/git` 与项目 `target`（或用 `Swatinem/rust-cache` 一类 action），并尽量让 Dockerfile/`cargo` 层在依赖未变时命中缓存，避免每次从零编依赖。

**解答：**
GitHub Actions 示意：

```yaml
- uses: actions/checkout@v4
- uses: dtolnay/rust-toolchain@stable
- uses: Swatinem/rust-cache@v2
- run: cargo test --locked
- run: cargo build --release --locked
```

手写 cache 键直觉：

```text
cache:
  - ~/.cargo/registry
  - ~/.cargo/git
  - target
key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
```

Docker 层缓存：先 COPY `Cargo.toml`/`Cargo.lock` 再假编译，后拷源码（见 [Q3](#q3)）。

「❌ 错误写法」——CI 每次 `rustup` + 冷 `cargo build`，无 cache：流水线以小时计。

**Go 对比：**
```yaml
- uses: actions/cache@v4
  with:
    path: ~/go/pkg/mod
    key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
```
- **Go 怎么做**：缓存 module 下载。
- **Rust 为什么不同**：还要缓存编译产物 `target`，因为编译更贵。
- **Go 程序员易踩的坑**：只缓存 registry 不缓存 `target`，省下的时间有限。

**记忆点：**
- 缓存 registry + git + target。
- lockfile 变才失效。

---

## Q10. 和 Go 多阶段 Docker 对照 {#q10}
**Tags:** `common` `Go` `Docker` `对照`
**适用版本:** 多阶段模式对照

**一句话答案：**
骨架相同：`FROM <lang-sdk> AS build` → `COPY --from=build` 到瘦 runtime。Go 常 `CGO_ENABLED=0` 进 scratch；Rust 要先问「动态还是 musl 静态、要不要 CA」，再选 debian slim / distroless / scratch。

**解答：**
并排心智：

```text
Go                          Rust
--------------------------  ------------------------------
golang:1.xx AS build        rust:1.xx AS builder
go build -o /out/app        cargo build --release
distroless/static|scratch   debian-slim|distroless|(scratch+musl)
COPY app                    COPY target/release/app
```

Rust 多一步决策：链接与证书（[Q4](#q4)–[Q6](#q6)）。Go 关 CGO 后决策更短。

**Go 对比：**
- **Go 怎么做**：多阶段几乎成套路。
- **Rust 为什么不同**：套路同样成立，runtime 底座选择更挑链接方式。
- **Go 程序员易踩的坑**：把 Go 的 scratch 模板原样套到未静态的 Rust 二进制上。

**记忆点：**
- 多阶段结构照搬 Go 即可。
- 差异在 runtime 依赖，不在「要不要多阶段」。

---

## Q11. 资源限制：内存、线程、tokio worker {#q11}
**Tags:** `common` `memory` `threads` `tokio`
**适用版本:** 容器 cgroup + tokio；以当前 tokio 文档为准

**一句话答案：**
给容器设 memory/CPU 限额后，要让 Rust 服务「识趣」：注意峰值 RSS、避免无界并发；**tokio** 默认 worker 约等于 CPU 核数，在共享节点上可用环境变量/显式 runtime builder 限制，防止线程与 CPU 配额打架。

**解答：**
容器侧：

```text
# Compose 示意
deploy:
  resources:
    limits:
      cpus: "1.0"
      memory: 512M
```

应用侧关注点：
1. **内存**：大缓存（moka）、大缓冲区、一次性读入文件——限住上限。
2. **阻塞线程**：`spawn_blocking` 池别被同步 Redis/文件打满（见 [48-caching](../48-caching-and-redis/#q10)）。
3. **tokio worker**：多实例挤同一节点时，默认「按机器核数」可能过猛。

```text
# 示意：限制 worker（具体 API/env 以 tokio 版本文档为准）
# TOKIO_WORKER_THREADS=2
# 或 Runtime::builder().worker_threads(2).enable_all().build()?
```

「❌ 错误写法」——K8s limit 512Mi，却无界把整表打进内存缓存：OOMKill。

**Go 对比：**
- **Go 怎么做**：`GOMAXPROCS`、容器感知（新版本更聪明）；内存靠自己与 pprof。
- **Rust 为什么不同**：对标物是 tokio worker / blocking 池，不是 GMP。
- **Go 程序员易踩的坑**：以为「async 就不会用很多线程」——阻塞调用仍会占满辅助线程。

**记忆点：**
- 容器 limit 与 runtime 线程数要对齐。
- 缓存与并发要有上限。

---

## Q12. 可观测：日志到 stdout、metrics 入口 {#q12}
**Tags:** `common` `logging` `metrics` `stdout`
**适用版本:** 容器可观测惯例

**一句话答案：**
日志打 **stdout/stderr**（JSON 或结构化文本），让平台收集；指标暴露 `/metrics`（Prometheus 文本）或 push 到网关。别只写容器内本地文件——重启即丢、也难被采集。

**解答：**
惯例：

```text
日志  → stdout / stderr → 节点 agent / 平台日志系统
指标  → :9090/metrics 或 sidecar → Prometheus
追踪  → OTLP 导出（按团队栈）
```

依赖示意（日志）：

```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
```

```text
// 示意：初始化后打到 stdout
tracing_subscriber::fmt()
    .with_env_filter("info")
    .json()
    .init();
tracing::info!(path = "/healthz", "request");
```

指标入口直觉：HTTP 服务挂 `GET /metrics`；或用独立端口，避免和业务鉴权搅在一起。

Dockerfile 别重定向到文件：

```dockerfile
# ✅ 默认就打印到 stdout
CMD ["myapp"]
# ❌ 避免：CMD ["myapp", ">", "/var/log/app.log"]
```

**Go 对比：**
```go
log.Println("listening")
http.Handle("/metrics", promhttp.Handler())
```
- **Go 怎么做**：标准库 log/slog + Prometheus client。
- **Rust 为什么不同**：常用 **tracing** + `metrics`/`prometheus` crate；习惯仍是 stdout + `/metrics`。
- **Go 程序员易踩的坑**：在容器里写 `log.txt` 却不挂 volume、也不采集 stdout。

**记忆点：**
- 日志出 stdout；指标留 scrape 入口。
- 可观测是部署的一部分，不是事后补丁。
