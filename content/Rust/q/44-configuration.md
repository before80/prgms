+++
title = "44-配置管理"
date = 2026-07-28T14:49:00+08:00
weight = 440
type = "docs"
description = "面向 Go 用户讲清 env/文件/默认值分层、serde 读配置、figment 与 clap 覆盖顺序"
isCJKLanguage = true
draft = false

+++

# 配置管理 (Configuration)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否想把「默认值 + 配置文件 + 环境变量」叠成一层可读的 `Config`，却不知道从哪下手？
- 你是否分不清：只读 `std::env`、dotenvy、serde 读 TOML、`config`/`figment` 各自何时上场？
- 你是否纠结：缺配置该 `panic` 还是返回 `Err`？密钥怎么分层？要不要热更新？
- 你是否想对齐 Go 的 Viper，并把 **clap** CLI 盖在最上层？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| env | environment variable | 环境变量 | 进程环境里的键值，常用于部署注入 | `os.Getenv` / `os.LookupEnv` |
| dotenv | — | 点环境文件 | 本地 `.env` 载入进程环境的习惯 | joho/godotenv |
| **dotenvy** | — | Rust dotenv crate | 从 `.env` 加载到环境变量 | godotenv |
| TOML | Tom's Obvious Minimal Language | TOML 配置格式 | Cargo 同款，适合静态配置文件 | 常用 YAML/JSON；也有 TOML 库 |
| serde | SERialize/DEserialize | 序列化框架 | 把文件内容解码进 struct；见 [36-serde](../36-serde-and-serialization/) | `encoding/json` 等 |
| **figment** | — | 配置合并库 | 多源（文件/env/序列化）合并成一份 | Viper 的合并思路 |
| **config** crate | — | 分层配置库 | 另一套常见的多层配置加载 | Viper |
| clap | Command Line Argument Parser | 命令行解析 | CLI 覆盖层；见 [38-clap](../38-cli-with-clap/) | `flag` / Cobra / Viper BindPFlags |
| Default | — | 默认值 trait | `Config::default()` 提供底座 | 结构体零值 / 手写默认 |
| Option | — | 可缺省字段 | `None` 表示「这一层没给」 | 指针 / `sql.Null*` 思路不同 |
| secret | — | 密钥/机密 | 密码、token；只进 env/密钥库 | 同概念 |
| hot reload | — | 热更新 | 进程不重启就换配置 | Viper `WatchConfig` |
| Viper | — | Go 配置库 | 文件+env+flag 合并的事实标准之一 | —（本题对标物） |
| 12-factor | twelve-factor app | 十二要素 | 「配置存环境」的著名部署原则 | 同原则 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q6](#q6), [Q9](#q9), [Q11](#q11) |
| `common` | [Q5](#q5), [Q7](#q7), [Q10](#q10), [Q12](#q12), [Q13](#q13), [Q14](#q14) |
| `occasional` | [Q8](#q8) |
| `advanced` | — |

---

## Q1. 默认值、配置文件、环境变量三层怎么叠？ {#q1}
**Tags:** `hot` `beginner` `layered` `env` `file`
**适用版本:** 模式与 Rust 1.0+ std；文件解码常依赖 serde

**一句话答案：**
自下而上：**Default（代码默认）→ 配置文件 → 环境变量（→ 可选 CLI）**。每一层只覆盖「有提供的字段」，最后得到一份完整 `Config`。对标 Viper 的多层 merge。

**解答：**
心智模型：

```text
CLI flags          （最高，可选，见 [Q9](#q9) / [38-clap](../38-cli-with-clap/)）
    ↑ 覆盖
环境变量
    ↑ 覆盖
配置文件（TOML/JSON…）
    ↑ 覆盖
Default::default() （底座）
```

最小「两层」只用 std（默认 + env）：

```rust
#[derive(Debug, Clone)]
struct Config {
    host: String,
    port: u16,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            host: "127.0.0.1".into(),
            port: 8080,
        }
    }
}

fn from_env(mut c: Config) -> Config {
    if let Ok(h) = std::env::var("APP_HOST") {
        c.host = h;
    }
    if let Ok(p) = std::env::var("APP_PORT") {
        if let Ok(n) = p.parse() {
            c.port = n;
        }
    }
    c
}

fn main() {
    let cfg = from_env(Config::default());
    println!("{}:{}", cfg.host, cfg.port);
}
```

加上文件层时，先 serde 读 TOML 得到「文件配置」，再与 Default/env 合并（见 [Q4](#q4)、[Q5](#q5)）。数据库连接串同样走 env——见 [43-database-and-sql](../43-database-and-sql/#q3)。

**Go 对比：**

```go
viper.SetDefault("port", 8080)
viper.SetConfigFile("config.yaml")
_ = viper.ReadInConfig()
viper.AutomaticEnv()
```

- **Go 怎么做**：Viper 一套 API 完成默认/文件/env。
- **Rust 为什么不同**：std 只给 env；文件与合并要 serde 或 figment/config。
- **Go 程序员易踩的坑**：以为有「官方 Viper」；其实是自己叠层或引 crate。

**记忆点：**
- 默认 → 文件 → env → CLI。
- 层越高越「部署相关」，层越低越「代码兜底」。

---

## Q2. 只读环境变量怎么写才稳？ {#q2}
**Tags:** `hot` `beginner` `std::env` `VarError`
**适用版本:** Rust 1.0+

**一句话答案：**
用 `std::env::var` / `var_os`：存在得 `Ok`，不存在得 `Err(VarError::NotPresent)`。必选配置在入口转换成应用错误；可选配置用 `ok()` / `unwrap_or`。

**解答：**

```rust
fn required(key: &str) -> Result<String, String> {
    std::env::var(key).map_err(|_| format!("missing env {key}"))
}

fn optional(key: &str, default: &str) -> String {
    std::env::var(key).unwrap_or_else(|_| default.to_string())
}

fn main() {
    let port = optional("APP_PORT", "8080");
    println!("port={port}");
    // let url = required("DATABASE_URL")?;  // 在返回 Result 的 main 里
}
```

区分「没设置」和「设了但非法」：

```rust
fn parse_port() -> Result<u16, String> {
    match std::env::var("APP_PORT") {
        Err(std::env::VarError::NotPresent) => Ok(8080),
        Err(e) => Err(e.to_string()),
        Ok(s) => s.parse::<u16>().map_err(|e| e.to_string()),
    }
}

fn main() {
    match parse_port() {
        Ok(p) => println!("port={p}"),
        Err(e) => eprintln!("bad APP_PORT: {e}"),
    }
}
```

进程如何带着 env 启动见 [04-running](../04-running/)。

**Go 对比：**

```go
v, ok := os.LookupEnv("APP_PORT")
if !ok {
    v = "8080"
}
```

- **Go 怎么做**：`Getenv`（空串与未设置难分）或 `LookupEnv`。
- **Rust 为什么不同**：`var` 用 `Result` 明确 NotPresent；空字符串仍是 `Ok("")`。
- **Go 程序员易踩的坑**：把空串当成「未设置」；或到处 `unwrap` 导致库代码直接炸。

**记忆点：**
- 必选：`var` → `Err` 往上抛。
- 可选：默认值；空串要不要接受，显式定规则。

---

## Q3. dotenvy 和仓库里的 `.env` 怎么用？ {#q3}
**Tags:** `hot` `dotenvy` `secrets` `git`
**适用版本:** dotenvy 0.15.x 一类；习惯重于版本号

**一句话答案：**
**dotenvy** 在开发机把 `.env` 载入进程环境；**不要**把含密钥的 `.env` 提交进 git。仓库只留 `.env.example`（无秘密）。生产靠平台注入 env，而不是依赖 dotenv 文件。

**解答：**

```toml
[dependencies]
dotenvy = "0.15"
```

```text
// 启动最早调用；找不到文件就忽略
dotenvy::dotenv().ok();
let url = std::env::var("DATABASE_URL").expect("DATABASE_URL");
```

仓库约定：

```text
# .gitignore
.env
.env.local

# 可提交
.env.example
DATABASE_URL=postgres://user:pass@localhost:5432/app
APP_PORT=8080
```

```rust
// 无 dotenv 时，测试可用 set_var（注意并行测试争用；示意）
fn main() {
    std::env::set_var("APP_PORT", "9090");
    assert_eq!(std::env::var("APP_PORT").unwrap(), "9090");
}
```

十二要素（**12-factor**，twelve-factor app，十二要素应用方法论）强调：配置进环境；dotenv 只是本地模拟。

**Go 对比：**

```go
_ = godotenv.Load()
```

- **Go 怎么做**：godotenv 同样只建议开发用。
- **Rust 为什么不同**：crate 名是 dotenvy；原则相同。
- **Go 程序员易踩的坑**：`.env` 进 git；或生产镜像里还依赖一份磁盘 `.env`。

**记忆点：**
- dotenvy = 本地糖；生产 = 真 env。
- 提交 example，忽略真实 `.env`。

---

## Q4. 用 serde 读 TOML 配置文件怎么写？ {#q4}
**Tags:** `hot` `serde` `toml` `file`
**适用版本:** serde 1.x + toml crate；详见 [36-serde-and-serialization](../36-serde-and-serialization/)

**一句话答案：**
定义 `Config` + `Deserialize`，`fs::read_to_string` 后 `toml::from_str`。类型就是 schema；缺字段可用 `#[serde(default)]`。

**解答：**

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
toml = "0.8"
```

```text
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct Config {
    host: String,
    #[serde(default = "default_port")]
    port: u16,
}

fn default_port() -> u16 { 8080 }

fn load(path: &str) -> Result<Config, Box<dyn std::error::Error>> {
    let text = std::fs::read_to_string(path)?;
    let cfg: Config = toml::from_str(&text)?;
    Ok(cfg)
}
```

示例文件：

```toml
# config.toml
host = "0.0.0.0"
port = 3000
```

只要 JSON/YAML，换 `serde_json` / `serde_yaml` 即可，struct 可共用——见 [36-serde-and-serialization](../36-serde-and-serialization/)。

标准库负责读字节，不负责「配置合并」：

```rust
fn main() {
    let path = "config.toml";
    match std::fs::read_to_string(path) {
        Ok(s) => println!("read {} bytes from {path}", s.len()),
        Err(e) => eprintln!("no file yet: {e}"),
    }
}
```

**Go 对比：**

```go
type Config struct {
    Host string `mapstructure:"host"`
    Port int    `mapstructure:"port"`
}
```

- **Go 怎么做**：Viper + mapstructure，或手动 `json.Unmarshal`。
- **Rust 为什么不同**：serde 派生是生态中心；格式 crate 可插拔。
- **Go 程序员易踩的坑**：字段是 `Option` 还是带 default，和「文件里没写」语义纠缠——先定规则再建模。

**记忆点：**
- struct + `Deserialize` = 配置 schema。
- 文件只是一层；env/CLI 另叠。

---

## Q5. `config` / `figment` 何时用？ {#q5}
**Tags:** `common` `figment` `config-crate` `merge`
**适用版本:** 选型；以 crates.io 当前文档为准

**一句话答案：**
手写「Default + 读文件 + 读 env」够用就别上框架。源多、要统一 merge/优先级、讨厌样板代码时，再用 **figment** 或 **config** crate。对标「我需要 Viper，而不只是 encoding/json」。

**解答：**

| 情况 | 建议 |
|------|------|
| 二进制小、字段少 | Default + `env::var` + 可选 toml |
| 多文件、多格式、要嵌套 merge | figment / config |
| 已有 clap，只要覆盖几个字段 | clap + 少量手写（见 [Q9](#q9)） |
| 库代码 | 让调用方传入 `Config`，别在库里偷偷读全局 |

```toml
[dependencies]
figment = { version = "0.10", features = ["toml", "env"] }
serde = { version = "1", features = ["derive"] }
```

```text
// 示意：figment 合并 TOML + 环境变量前缀
use figment::{Figment, providers::{Format, Toml, Env}};
use serde::Deserialize;

#[derive(Deserialize)]
struct Config {
    host: String,
    port: u16,
}

let cfg: Config = Figment::new()
    .merge(Toml::file("config.toml"))
    .merge(Env::prefixed("APP_"))
    .extract()?;
```

**Go 对比：**
- **Go 怎么做**：中小型也常直接上 Viper。
- **Rust 为什么不同**：serde 先解决「解码」；「多层合并」是可选复杂度。
- **Go 程序员易踩的坑**：Hello World 就引入重配置框架，调试优先级比业务还难。

**记忆点：**
- 先手写三层；痛了再 figment/config。
- 库要注入，不要全局隐式加载。

---

## Q6. 缺配置时该 `panic` 还是返回 `Err`？ {#q6}
**Tags:** `hot` `error-handling` `panic` `Result`
**适用版本:** Rust 1.0+；错误观见 [21-error-handling](../21-error-handling/)

**一句话答案：**
**二进制入口**：缺必选配置可以清晰 `Err` 后 `exit(1)`，或有意 `expect("DATABASE_URL")`；**库代码**：返回 `Result`，禁止安静 `unwrap`。可恢复/可调用方决策的，一律 `Err`。

**解答：**

```rust
fn load_url() -> Result<String, String> {
    std::env::var("DATABASE_URL").map_err(|_| "DATABASE_URL required".into())
}

fn main() {
    match load_url() {
        Ok(u) => println!("url len={}", u.len()),
        Err(e) => {
            eprintln!("config error: {e}");
            std::process::exit(1);
        }
    }
}
```

对比两种入口风格：

```rust
fn main() {
    // 崩溃信息短、适合「配置错了就不该起来」
    let _url = std::env::var("DATABASE_URL").expect("DATABASE_URL must be set");
}
```

| 位置 | 缺必选配置 |
|------|------------|
| `main` / 启动函数 | `Result` + 非 0 退出，或 `expect` |
| 库函数 | `Result` / 自定义错误类型 |
| 测试 | 用 `#[should_panic]` 仅测 panic 契约；一般造完整配置 |

**Go 对比：**

```go
if os.Getenv("DATABASE_URL") == "" {
    log.Fatal("DATABASE_URL required")
}
```

- **Go 怎么做**：启动时 `Fatal` / 返回 `error` 都很常见。
- **Rust 为什么不同**：`panic` 与 `Result` 边界更强调「库不要替进程决定死活」。
- **Go 程序员易踩的坑**：在深层库里 `expect`，调用方无法改成「缺省则禁用某功能」。

**记忆点：**
- 库：`Result`；进程边界：失败即退出。
- `expect` 写清「缺的是什么」。

---

## Q7. 分层配置和密钥（secret）怎么放？ {#q7}
**Tags:** `common` `secrets` `layered` `security`
**适用版本:** 部署习惯；与具体云厂商无关

**一句话答案：**
非机密（端口、特性开关）可进文件；**secret**（密码、token、私钥）只进环境变量或密钥管理服务，永不进仓库与日志。文件里可留「密钥的引用名」，不留明文。

**解答：**

```toml
# config.toml —— 可提交
host = "0.0.0.0"
port = 8080
database_url_env = "DATABASE_URL"  # 只记「去哪个 env 找」
```

```rust
fn resolve_db_url(env_key: &str) -> Result<String, String> {
    std::env::var(env_key).map_err(|_| format!("secret env {env_key} missing"))
}

fn main() {
    let key = "DATABASE_URL";
    match resolve_db_url(key) {
        Ok(u) => println!("db url configured (len={})", u.len()), // 勿打印全文
        Err(e) => eprintln!("{e}"),
    }
}
```

分层示意：

| 内容 | 文件 | env | 密钥库 |
|------|------|-----|--------|
| listen port | ✅ | ✅ 可覆盖 | 不必 |
| feature flag | ✅ | ✅ | 不必 |
| DB 密码 | ❌ | ✅ | ✅ 更好 |
| 第三方 API token | ❌ | ✅ | ✅ |

日志里打印 `Config` 时跳过 secret 字段（手写 `Debug` 或标记红名单）。

**Go 对比：**
- **Go 怎么做**：同样「Viper 读文件 + 密钥走 env/KMS」。
- **Rust 为什么不同**：无特殊语言能力；纪律相同。
- **Go 程序员易踩的坑**：`Debug` 一把梭把 token 打进日志。

**记忆点：**
- 文件公开，密钥旁路。
- 日志只打「有没有配置」，不打明文。

---

## Q8. 热更新（hot reload）现实吗？ {#q8}
**Tags:** `occasional` `hot-reload` `watch`
**适用版本:** 架构建议；与具体 notify 版本无关

**一句话答案：**
多数服务 **不值得** 上配置热更新：重启/滚动发布更简单可审计。若要做，只热更新「安全、可逆」的项（日志级别、开关），连接串/密钥变更仍应重建客户端或重启。

**解答：**
现实约束：

| 配置项 | 热更新？ |
|--------|----------|
| 日志级别 | 相对容易 |
| 功能开关 | 可以，注意竞态 |
| 监听地址 / TLS 证书 | 通常要重建 listener |
| `DATABASE_URL` | 应换池/重启，不建议半热更 |

```rust
// 示意：用 ArcSwap / RwLock 持有「当前配置快照」
use std::sync::{Arc, RwLock};

#[derive(Clone, Debug)]
struct Config {
    log_level: String,
}

fn main() {
    let cfg = Arc::new(RwLock::new(Config {
        log_level: "info".into(),
    }));
    // 后台任务读文件 → write 锁替换
    // 请求路径只 read 锁 / clone 快照
    let snap = cfg.read().unwrap().clone();
    println!("level={}", snap.log_level);
}
```

真要看文件变化，可用 `notify` 等 crate 看路径；复杂度与测试成本显著上升。

**Go 对比：**
- **Go 怎么做**：Viper `WatchConfig` 存在，但生产仍常靠重启。
- **Rust 为什么不同**：生态也能做，没有「必须热更」的文化包袱。
- **Go 程序员易踩的坑**：热更了文件却忘了重建连接池，进程「半新半旧」。

**记忆点：**
- 默认：改配置 → 滚动发布。
- 热更只留给无状态、可即时生效的开关。

---

## Q9. CLI / env / 文件的覆盖顺序怎么定？如何链上 clap？ {#q9}
**Tags:** `hot` `clap` `override` `precedence`
**适用版本:** clap 4.x；详见 [38-cli-with-clap](../38-cli-with-clap/)

**一句话答案：**
推荐优先级：**CLI > env > 文件 > Default**。用 clap 声明参数，并可设 `env = "APP_PORT"` 做「CLI 与 env」双通道；文件层先载入再被 clap 结果覆盖。

**解答：**

```toml
[dependencies]
clap = { version = "4", features = ["derive", "env"] }
```

```text
use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "app")]
struct Cli {
    /// 监听端口（CLI 优先；否则读 APP_PORT）
    #[arg(long, env = "APP_PORT", default_value_t = 8080)]
    port: u16,

    /// 配置文件路径
    #[arg(long, default_value = "config.toml")]
    config: String,
}

// 合并步骤（文件解码用 serde，见 [Q4](#q4)）：
// 1. let cli = Cli::parse();
// 2. let file_cfg = load_toml(&cli.config).unwrap_or_default();
// 3. 以 file 为底，把 cli 里「显式传入」的字段盖上去
```

完整合并时注意：clap 的 `default_value` 与「用户是否真的传了 flag」有时要靠 `Option<T>` 区分——见 [Q10](#q10) 与 [38-cli-with-clap](../38-cli-with-clap/)。

```rust
// 无 clap 时的优先级示意
fn pick<'a>(cli: Option<&'a str>, env: Option<&'a str>, file: &'a str, def: &'a str) -> &'a str {
    cli.or(env).unwrap_or(if !file.is_empty() { file } else { def })
}

fn main() {
    assert_eq!(pick(Some("1"), Some("2"), "3", "4"), "1");
    assert_eq!(pick(None, Some("2"), "3", "4"), "2");
    assert_eq!(pick(None, None, "3", "4"), "3");
}
```

**Go 对比：**

```go
viper.BindPFlag("port", flag.Lookup("port"))
viper.AutomaticEnv()
```

- **Go 怎么做**：Viper 绑 flag，文档约定优先级。
- **Rust 为什么不同**：clap 很强；文件层常手写或 figment，优先级要自己保证一致。
- **Go 程序员易踩的坑**：文件默认值与 clap `default_value` 双默认，分不清谁赢。

**记忆点：**
- 写进 README：CLI > env > 文件 > Default。
- clap `env = "..."` 打通两层；文件另合并。

---

## Q10. `Default` + `Option` 字段怎么建模？ {#q10}
**Tags:** `common` `Default` `Option` `partial`
**适用版本:** Rust 1.0+；serde 可选

**一句话答案：**
「完整运行配置」用具体类型 + `Default`；「某一层提供的补丁」用 `Option` 字段（`None` = 本层未设置）。合并时 `Option::or` / `unwrap_or` 叠上去。

**解答：**

```rust
#[derive(Debug, Clone)]
struct Config {
    host: String,
    port: u16,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            host: "127.0.0.1".into(),
            port: 8080,
        }
    }
}

#[derive(Debug, Default)]
struct ConfigPatch {
    host: Option<String>,
    port: Option<u16>,
}

fn merge(base: Config, patch: ConfigPatch) -> Config {
    Config {
        host: patch.host.unwrap_or(base.host),
        port: patch.port.unwrap_or(base.port),
    }
}

fn main() {
    let cfg = merge(
        Config::default(),
        ConfigPatch {
            port: Some(3000),
            ..Default::default()
        },
    );
    assert_eq!(cfg.port, 3000);
    assert_eq!(cfg.host, "127.0.0.1");
}
```

serde 文件层也可直接 `Option`：

```text
#[derive(serde::Deserialize, Default)]
struct FileConfig {
    host: Option<String>,
    port: Option<u16>,
}
```

**Go 对比：**
- **Go 怎么做**：指针字段 / `mapstructure` 区分「零值」与「未设置」。
- **Rust 为什么不同**：`Option` 是一等公民，正好表达「未设置」。
- **Go 程序员易踩的坑**：用 `port: 0` 表示未设置，和「真想监听 0」冲突。

**记忆点：**
- 完整配置：具体类型；补丁层：`Option`。
- 合并用 `unwrap_or`，别让零值冒充「未设置」。

---

## Q11. 和 Go Viper 总对照？ {#q11}
**Tags:** `hot` `viper` `cheatsheet`
**适用版本:** 心智对照

**一句话答案：**
Viper 的「默认/文件/env/flag 合一」在 Rust 里拆成：**serde 读文件** + **`std::env`** + **clap**（+ 可选 figment/config）。没有单一官方库，但能力一一可对上。

**解答：**

| Viper | Rust 常见对应 |
|-------|----------------|
| `SetDefault` | `Default` / serde `default` |
| `SetConfigFile` + `ReadInConfig` | `fs` + `toml::from_str` / serde |
| `AutomaticEnv` / `BindEnv` | `std::env::var` / clap `env` |
| `BindPFlag` | clap `Parser` |
| `Unmarshal` | serde `Deserialize` |
| `WatchConfig` | 一般不做；或 `notify` + 自管状态 |
| 远程配置 | 各自 SDK；仍解码进 struct |

```text
Viper 一站式          Rust 组合拳
─────────────────────────────────
viper.ReadInConfig  →  serde + toml
viper.AutomaticEnv  →  env::var / clap env
viper.BindPFlag     →  clap
viper.Unmarshal     →  Deserialize
```

最小「Viper 移民」路径：先 [Q1](#q1) 手写三层 → 需要 CLI 加 [38-clap](../38-cli-with-clap/) → 仍痛再 figment。

**Go 对比：**
- **Go 怎么做**：一个 Viper 搞定。
- **Rust 为什么不同**：解码（serde）与参数（clap）都是强生态，配置合并反成可选。
- **Go 程序员易踩的坑**：寻找 `viper` 同名 crate 当唯一答案，忽略 clap/serde 已覆盖 80% 需求。

**记忆点：**
- Viper ≈ Default + serde 文件 + env + clap。
- 先组合，再框架。

---

## Q12. 最小配置清单（落地检查表）？ {#q12}
**Tags:** `common` `checklist` `production`
**适用版本:** 实践清单

**一句话答案：**
落地时按清单勾选：有 `Config` 类型、有默认、文件可选、密钥只走 env、优先级写进 README、启动失败信息可读、测试不依赖开发者机器上的私密 `.env`。

**解答：**
检查表：

```text
[ ] 1. 定义 Config struct（可 Debug，secret 字段脱敏）
[ ] 2. impl Default 或 serde default
[ ] 3. 可选 config.toml + .env.example（无秘密）
[ ] 4. .gitignore 忽略 .env
[ ] 5. 必选：DATABASE_URL / 监听地址等启动时校验
[ ] 6. 文档写明：CLI > env > 文件 > Default
[ ] 7. 需要 CLI 时用 clap（38-clap），env feature 按需打开
[ ] 8. 测试用 set_var / 测试专用文件，不读开发者密钥
[ ] 9. 生产不依赖 dotenvy
[ ] 10. 改连接串等危险项走滚动发布，不半吊子热更
```

最小依赖组合示例：

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
toml = "0.8"
clap = { version = "4", features = ["derive", "env"] }
# 开发可选：
# dotenvy = "0.15"
```

```rust
fn main() {
    // 启动门禁示意
    if std::env::var("DATABASE_URL").is_err() {
        eprintln!("DATABASE_URL is required");
        std::process::exit(1);
    }
    println!("config gate passed");
}
```

相关：[36-serde](../36-serde-and-serialization/)、[38-clap](../38-cli-with-clap/)、[04-running](../04-running/)、[43-database-and-sql](../43-database-and-sql/#q3)。

**Go 对比：**
- **Go 怎么做**：Viper + `Fatal` + godotenv 开发。
- **Rust 为什么不同**：清单相同，零件换成 serde/clap/env。
- **Go 程序员易踩的坑**：清单只写依赖、不写优先级与密钥边界。

**记忆点：**
- 类型化 Config + 四层优先级 + 密钥旁路。
- 能手写就不先上重框架。

---

## Q13. YAML 配置怎么读（serde_yaml）？ {#q13}
**Tags:** `common` `yaml` `serde_yaml` `serde`
**适用版本:** serde 1.x + `serde_yaml`（版本以 crates.io 为准）

**一句话答案：**
和读 TOML 同一套路：`Config` + `Deserialize`，`fs::read_to_string` 后换 **`serde_yaml::from_str`**。struct 可与 TOML/JSON **共用**；只换格式 crate。见 [Q4](#q4)、[36-serde-and-serialization](../36-serde-and-serialization/)。

**解答：**

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_yaml = "0.9"
```

```text
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct Config {
    host: String,
    #[serde(default = "default_port")]
    port: u16,
}

fn default_port() -> u16 { 8080 }

fn load_yaml(path: &str) -> Result<Config, Box<dyn std::error::Error>> {
    let text = std::fs::read_to_string(path)?;
    let cfg: Config = serde_yaml::from_str(&text)?;
    Ok(cfg)
}
```

示例文件：

```text
# config.yaml
host: "0.0.0.0"
port: 3000
```

标准库只负责读文件；解码在外部 crate：

```rust
fn main() {
    let path = "config.yaml";
    match std::fs::read_to_string(path) {
        Ok(s) => println!("yaml text {} bytes", s.len()),
        Err(e) => eprintln!("no yaml yet: {e}"),
    }
}
```

注意：YAML 特性比 TOML 多（锚点、多文档等），团队若无特殊需求，许多 Rust 项目仍偏好 TOML；选 YAML 往往是「已有 YAML 运维习惯」而不是「serde 更好」。

**Go 对比：**

```go
import "gopkg.in/yaml.v3"

type Config struct {
	Host string `yaml:"host"`
	Port int    `yaml:"port"`
}
```

- **Go 怎么做**：`yaml.Unmarshal` + struct tag。
- **Rust 为什么不同**：serde 派生统一；换格式几乎只换 `from_str` 的 crate。
- **Go 程序员易踩的坑**：以为必须上 Viper 才能读 YAML——serde + `serde_yaml` 就够类型化读取。

**记忆点：**
- YAML ≈ 把 `toml::from_str` 换成 `serde_yaml::from_str`。
- schema 仍是那个 `Deserialize` struct。

---

## Q14. 配置加载后怎么做字段校验？ {#q14}
**Tags:** `common` `validation` `validator`
**适用版本:** 手写任意版本；`validator` crate 以 crates.io 为准

**一句话答案：**
serde 只保证「能反序列化成类型」，**不保证**业务合法（端口范围、URL 非空、互斥字段）。加载后加一层：**手写 `validate(&Config) -> Result`**，或字段多时用 **`validator`** 等派生校验；失败要在启动期报清晰错误。

**解答：**
手写（小配置首选）：

```rust
#[derive(Debug)]
struct Config {
    host: String,
    port: u16,
}

fn validate(cfg: &Config) -> Result<(), String> {
    if cfg.host.trim().is_empty() {
        return Err("host must not be empty".into());
    }
    if cfg.port == 0 {
        return Err("port must be non-zero".into());
    }
    Ok(())
}

fn main() {
    let cfg = Config { host: "127.0.0.1".into(), port: 8080 };
    validate(&cfg).expect("config ok");
}
```

「❌ 只 Deserialize、不校验」——`port: 0` 或空 `host` 也能「加载成功」，运行时才爆：

```rust
fn main() {
    let port: u16 = 0; // 类型合法 ≠ 业务合法
    assert_eq!(port, 0);
}
```

字段规则多、想声明式时再用 crate（示意，需依赖）：

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
validator = { version = "0.19", features = ["derive"] }
```

```text
use serde::Deserialize;
use validator::Validate;

#[derive(Debug, Deserialize, Validate)]
struct Config {
    #[validate(length(min = 1))]
    host: String,
    #[validate(range(min = 1, max = 65535))]
    port: u16,
}

fn load_and_check(cfg: Config) -> Result<Config, validator::ValidationErrors> {
    cfg.validate()?;
    Ok(cfg)
}
```

决策：

| 情况 | 建议 |
|------|------|
| 字段少、规则简单 | 手写 `validate` |
| 大量 length/range/email | `validator` 等 |
| 跨字段约束（A 有则 B 必有） | 手写更清晰 |

**Go 对比：**
- **Go 怎么做**：手写 check，或 `go-playground/validator` 之类 tag。
- **Rust 为什么不同**：serde ≠ validate；两步要分开想。
- **Go 程序员易踩的坑**：以为「类型反序列化成功 = 配置可用」。

**记忆点：**
- Deserialize 之后再 Validate。
- 小就手写，大再上 `validator`。
