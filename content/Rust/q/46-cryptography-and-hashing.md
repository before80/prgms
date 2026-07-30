+++
title = "46-cryptography-and-hashing"
date = 2026-07-28T14:49:00+08:00
weight = 460
type = "docs"
description = "面向 Go 用户讲清 Rust 密码学选型、哈希/密码哈希、随机数、AES-GCM/HMAC 与密钥存放"
isCJKLanguage = true
draft = false

+++

# 密码学与哈希 (Cryptography and Hashing)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你会不会疑惑：为什么 Go 有 `crypto/*`，Rust std 却几乎不放密码学？
- 你是否分不清：内容完整性用 sha2/blake3，密码存储却绝不能裸 SHA？
- 你是否想算 SHA-256、做 HMAC、上 AES-GCM，却不知道该选哪几个 crate？
- 你是否把 `rand` 当“够随机”、把 `==` 当“安全比较”，埋下时序侧信道？
- 你是否纠结：TLS 证书该谁管、密钥怎么放才不进仓库？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| hash | — | 哈希/摘要 | 把任意长度输入压成固定长度指纹 | `crypto/...` 的 Hash |
| **SHA-256** | Secure Hash Algorithm 256-bit | 常见摘要算法 | 256 位输出的 SHA-2 家族成员 | `crypto/sha256` |
| **BLAKE3** | — | 现代快速哈希 | 可并行、常用于内容寻址/校验 | 第三方 blake3 库 |
| **MD5** | Message Digest 5 | 破损摘要 | 碰撞已破，不可用于安全场景 | `crypto/md5`（同样忌安全用） |
| password hash | — | 密码哈希 | 故意慢、带盐，抗暴力猜密码 | `golang.org/x/crypto/bcrypt` 等 |
| **Argon2** | — | 密码哈希算法 | 内存困难、当前推荐默认之一 | x/crypto 有相关实现 |
| **bcrypt** | — | 密码哈希算法 | 经典慢哈希，仍广泛可用 | `bcrypt` |
| CSPRNG | Cryptographically Secure PRNG | 密码学安全随机源 | 不可预测的随机字节 | `crypto/rand` |
| **OsRng** | OS RNG | 操作系统熵源 | 从 OS 取密码学随机 | `crypto/rand.Read` |
| AEAD | Authenticated Encryption with Associated Data | 带关联数据的认证加密 | 加密同时防篡改 | `cipher.AEAD`（GCM） |
| **AES-GCM** | AES Galois/Counter Mode | 对称认证加密 | 常用 AEAD 模式 | `crypto/aes` + GCM |
| **HMAC** | Hash-based Message Authentication Code | 基于哈希的消息认证码 | 用密钥证明消息未被改 | `crypto/hmac` |
| constant-time | — | 常量时间比较 | 比较耗时不依赖秘密内容 | `subtle.ConstantTimeCompare` |
| **subtle** | — | 常量时间工具 crate | 提供安全比较等原语 | `crypto/subtle` |
| **TLS** | Transport Layer Security | 传输层安全 | 证书、握手、信道加密 | `crypto/tls` |
| **rustls** | — | 纯 Rust TLS | 常见 TLS 实现；见 [40-http](../40-http-client-and-server/) | 自带 TLS 栈 |
| KDF | Key Derivation Function | 密钥派生函数 | 从密码/材料导出密钥 | `pbkdf2` / `hkdf` 等 |
| nonce / IV | number used once / Init Vector | 一次性随机数 | AEAD 每次加密必须唯一 | GCM nonce |
| side channel | — | 侧信道 | 用时间/功耗等泄露秘密 | 同概念 |
| **JWT** | JSON Web Token | JSON Web 令牌 | 可验证的声明格式（默认不加密 payload） | `golang-jwt` 等 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q11](#q11), [Q13](#q13) |
| `common` | [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q14](#q14) |
| `occasional` | [Q12](#q12) |
| `advanced` | — |

---

## Q1. 为什么 Rust 不像 Go 那样在 std 里放 crypto？ {#q1}
**Tags:** `hot` `beginner` `std` `crypto` `ecosystem`
**适用版本:** 设计层面；与 Rust 版本无关

**一句话答案：**
Rust 把密码学留给生态 crate（`sha2`、`ring`、`rustls` 等）：算法要快速迭代、可裁剪、可审计；std 只保留极少与系统耦合的接口（如读 OS 随机）。对标 Go 的“标准库自带一整套 `crypto/*`”，Rust 是“标准接口薄、实现外置”。

**解答：**
心智对照：

```text
Go:   std = crypto/sha256 + crypto/tls + crypto/hmac + ...
Rust: std ≈ 几乎不提供算法实现
      crates.io = sha2 / blake3 / aes-gcm / ring / rustls / argon2 / ...
```

常见理由（记三条即可）：
1. **演进速度**：哈希、曲线、TLS 套件经常更新；绑进 std 会拖版本、难弃用。
2. **可裁剪**：嵌入式/WASM 可能只要一种哈希；不想为整套 TLS 买单。
3. **审计与替换**：安全库可独立发版、换实现（`ring` ↔ 纯 Rust 栈），不必等语言发行版。

std 里你仍会碰到的相关物：
- `std::hash`：**非密码学**哈希（给 `HashMap` 用），**绝不是** SHA/HMAC。
- 读 OS 熵：常通过 `getrandom` / `rand::rngs::OsRng`（见 [Q5](#q5)），而不是 `std::crypto`。

「❌ 错误思路」——在 `std` 里找 `sha256`、或把 `std::hash::Hasher` 当摘要算法：

```text
// 错：DefaultHasher / SipHash 类是防 HashDos 的容器哈希，不是 SHA-256
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
// 算出来的 u64 不能当密码学摘要、不能当完整性校验的“正式指纹”
```

**Go 对比：**
- **Go 怎么做**：`import "crypto/sha256"` 等，标准库直接给算法。
- **Rust 为什么不同**：语言团队刻意把可变、高风险的密码学实现放在可独立升级的 crate。
- **Go 程序员易踩的坑**：一上来就在 std 文档里搜 crypto，搜不到就以为“Rust 不做安全”——其实全在 crates.io。

**记忆点：**
- 要摘要/加密 → 选 crate，不是 std。
- `std::hash` ≠ 密码学哈希。

---

## Q2. 哈希选 sha2 / blake3 / md5 怎么想？md5 何时绝不用？ {#q2}
**Tags:** `hot` `sha2` `blake3` `md5` `hash`
**适用版本:** 选型原则；crate 版本以 crates.io 为准

**一句话答案：**
完整性/通用指纹优先 **SHA-256**（`sha2`）或与生态约定一致的算法；要极速内容哈希可看 **BLAKE3**；**MD5 在任何安全场景绝对不用**（碰撞已破），只可能出现在“兼容遗留非安全校验、且已知情”的兼容层。

**解答：**
怎么选：

| 需求 | 倾向 | 说明 |
|------|------|------|
| 签名/证书/TLS 世界常见指纹 | SHA-256（sha2） | 互通性最好 |
| 内容寻址、大文件校验、要速度 | BLAKE3 | 现代、可并行 |
| 兼容旧协议校验和 | 看协议；可能是 SHA-1/MD5 | **安全属性已失效**时只能当“格式兼容” |
| 存用户密码 | **不是**这些裸哈希 | 见 [Q4](#q4) |

依赖示意：

```toml
[dependencies]
sha2 = "0.10"
blake3 = "1"
# md5 仅在遗留兼容时考虑；不要默认加
# md-5 = "0.10"
```

「❌ 绝不用 MD5」的场景（记死）：
- 密码存储、会话令牌、API 签名、证书/软件更新完整性、防篡改。
- “我加个盐再 MD5”仍然不行——碰撞与设计缺陷不靠盐补救。

「✅ 还能见到 MD5」的场景：
- 某旧对象存储/CDN 仍返回 `Content-MD5` 头做**非对抗**完整性提示；或迁移工具必须读旧库字段。此时要在代码与文档里标明 **legacy / non-security**。

**Go 对比：**
```go
import (
    "crypto/md5"    // 同样：安全场景勿用
    "crypto/sha256"
)
```
- **Go 怎么做**：算法也在 std，但官方同样警告 MD5 不适合安全。
- **Rust 为什么不同**：算法在第三方 crate，选型责任更显式。
- **Go 程序员易踩的坑**：把“Go 里 `md5.Sum` 很方便”平移成默认——两边都不该当默认安全哈希。

**记忆点：**
- 通用安全指纹 → SHA-256；要快且现代 → BLAKE3。
- MD5：兼容可，安全绝不。

---

## Q3. 计算 SHA-256 的最小写法是什么？ {#q3}
**Tags:** `hot` `sha2` `SHA-256` `digest`
**适用版本:** sha2 0.10.x（API 以当前文档为准）

**一句话答案：**
加依赖 `sha2`，`Sha256::digest(data)`（或 `update` + `finalize`）得到 32 字节摘要；需要十六进制再用 `hex`/`data-encoding` 或手写格式化。外部 crate，示意用 text。

**解答：**
`Cargo.toml`：

```toml
[dependencies]
sha2 = "0.10"
hex = "0.4"   # 可选：把字节打成 hex 字符串
```

一次性算完（最常见）：

```text
use sha2::{Digest, Sha256};

fn main() {
    let digest = Sha256::digest(b"hello");
    // digest 是 GenericArray<u8, 32>，可当 &[u8] 用
    println!("{:x}", digest); // sha2 的 Digest 常支持 LowerHex
}
```

流式（大文件/分块）：

```text
use sha2::{Digest, Sha256};

let mut hasher = Sha256::new();
hasher.update(b"hel");
hasher.update(b"lo");
let result = hasher.finalize();
```

只关心“和 Go 一样拿到 `[32]byte`”的对照：

```text
Go:  sum := sha256.Sum256([]byte("hello"))  // [32]byte
.rs: out := Sha256::digest(b"hello");       // 32 字节数组式结果
```

**Go 对比：**
```go
sum := sha256.Sum256([]byte("hello"))
fmt.Printf("%x\n", sum)
```
- **Go 怎么做**：`crypto/sha256` 一个 import。
- **Rust 为什么不同**：同一算法在 `sha2` crate；trait 叫 `Digest`。
- **Go 程序员易踩的坑**：找 `crypto/sha256` 包路径——在 Rust 里是 `sha2` + `Digest`。

**记忆点：**
- `Sha256::digest` = 最短路径。
- 分块用 `update` / `finalize`。

---

## Q4. 密码哈希为什么要用 argon2/bcrypt，不能裸 SHA？ {#q4}
**Tags:** `hot` `argon2` `bcrypt` `password` `KDF`
**适用版本:** argon2 / bcrypt crate；原则与版本无关

**一句话答案：**
用户密码要用 **密码哈希**（Argon2、bcrypt 等）：故意慢、吃内存/算力、自动带盐。裸 SHA-256/MD5 太快，GPU/彩虹表秒破；密码哈希是 **KDF**（Key Derivation Function，密钥派生函数）思路，不是普通摘要。

**解答：**
对比：

| | 裸 SHA-256 | Argon2 / bcrypt |
|--|------------|-----------------|
| 速度 | 极快 | 可调、故意慢 |
| 盐 | 你要自己管 | 库通常内嵌到输出串 |
| 抗 GPU 爆破 | 弱 | 强（尤其 Argon2id） |
| 用途 | 文件指纹等 | **仅**密码/口令存储 |

依赖示意：

```toml
[dependencies]
argon2 = "0.5"
# 或
# bcrypt = "0.15"
```

Argon2 校验直觉（text，非完整生产模板）：

```text
use argon2::{
    password_hash::{PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2,
};

// 注册：hash 后只存 PHC 字符串（含算法/参数/盐/摘要）
let salt = SaltString::generate(&mut rand_core::OsRng);
let hash = Argon2::default()
    .hash_password(b"user-password", &salt)?
    .to_string();

// 登录：用同一字符串 verify
let parsed = PasswordHash::new(&hash)?;
Argon2::default().verify_password(b"user-password", &parsed)?;
```

「❌ 错误写法」——`sha256(password)` 或 `sha256(password + salt)` 当“安全存储”：盐能挡彩虹表，挡不住高速在线/离线爆破；缺内存困难与工作因子。

**Go 对比：**
```go
hash, err := bcrypt.GenerateFromPassword([]byte(pwd), bcrypt.DefaultCost)
err = bcrypt.CompareHashAndPassword(hash, []byte(pwd))
```
- **Go 怎么做**：`golang.org/x/crypto/bcrypt`（或 argon2 实现），不是 `sha256.Sum`。
- **Rust 为什么不同**：同样用专用 crate；推荐默认常看 Argon2id。
- **Go 程序员易踩的坑**：两边都有人把 SHA 当密码哈希——错法同源。

**记忆点：**
- 密码 → argon2/bcrypt；内容指纹 → sha2/blake3。
- 存库存 PHC/bcrypt 串，不存“裸摘要”。

---

## Q5. 随机数：rand 和 getrandom / OsRng 怎么选？ {#q5}
**Tags:** `hot` `rand` `getrandom` `OsRng` `CSPRNG`
**适用版本:** rand 0.8/0.9 系；getrandom；原则通用

**一句话答案：**
**密钥、nonce、token、会话 ID** 必须用密码学安全源：**OsRng** / `getrandom`（从 OS 取熵的 **CSPRNG**）。`rand` 的普通 `thread_rng`/可种子 RNG 适合模拟与非安全随机；安全场景要显式走 `OsRng` 或文档标明 crypto 的 API。

**解答：**
分层：

```text
需要不可预测（密钥/nonce） → OsRng / getrandom / crypto-grade API
游戏/测试/抽样/打乱展示   → rand 的快速 PRNG（可种子、可复现）
```

依赖：

```toml
[dependencies]
getrandom = "0.2"
rand = "0.8"
```

读 32 字节密钥材料（示意）：

```text
use rand::rngs::OsRng;
use rand::RngCore;

let mut key = [0u8; 32];
OsRng.fill_bytes(&mut key);
```

或直接 `getrandom`：

```text
let mut buf = [0u8; 32];
getrandom::getrandom(&mut buf)?;
```

「❌ 错误写法」——用可预测种子生成会话令牌：

```text
// 错：StdRng::seed_from_u64(42) 可复现 = 可猜测
// 令牌/密钥绝不能这样
```

std 侧能做的“非密码学”示意（可编译，仅说明 `std` 不管 CSPRNG API）：

```rust
fn main() {
    // std 没有 “crypto/rand”；这里只演示普通随机不在 std 密码学路径
    let n = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_nanos() as u64)
        .unwrap_or(0);
    println!("not a CSPRNG: {n}");
}
```

**Go 对比：**
- **Go 怎么做**：安全用 `crypto/rand`；数学/测试用 `math/rand`（Go 1.20+ 也有更清晰的划分）。
- **Rust 为什么不同**：`rand` crate 同时提供多种 RNG；**你必须自己选对后端**。
- **Go 程序员易踩的坑**：看见 `rand::random()` 就当 `crypto/rand`——不一定。

**记忆点：**
- 安全随机 = OsRng / getrandom。
- 要复现的模拟 = 可种子 PRNG，别混用。

---

## Q6. 对称加密 AES-GCM 的入门直觉是什么？ {#q6}
**Tags:** `common` `AES-GCM` `AEAD` `ring` `aes-gcm`
**适用版本:** aes-gcm / ring；AEAD 原则通用

**一句话答案：**
把 **AES-GCM** 当成 **AEAD**（Authenticated Encryption with Associated Data，带关联数据的认证加密）：一次给出密文 + 认证标签，防窃听也防篡改。关键：**密钥长度对、nonce 绝不重复**；关联数据（AAD）可绑上下文字符串但不加密。常用 crate：`aes-gcm` 或经由 `ring`。

**解答：**
依赖（`aes-gcm` 路线）：

```toml
[dependencies]
aes-gcm = "0.10"
rand = "0.8"
```

加密/解密直觉（text）：

```text
use aes_gcm::{
    aead::{Aead, KeyInit},
    Aes256Gcm, Nonce,
};
use rand::rngs::OsRng;
use rand::RngCore;

let key = Aes256Gcm::generate_key(&mut OsRng);
let cipher = Aes256Gcm::new(&key);

let mut nonce_bytes = [0u8; 12];
OsRng.fill_bytes(&mut nonce_bytes);
let nonce = Nonce::from_slice(&nonce_bytes);

let ciphertext = cipher.encrypt(nonce, b"secret msg".as_ref())?;
let plaintext = cipher.decrypt(nonce, ciphertext.as_ref())?;
```

必须记住的三条：
1. **nonce/IV 唯一**：同一密钥下重复 nonce = 灾难（GCM 直接破功）。
2. **密文要带上 nonce**（或可派生的计数器状态）一起存储/传输。
3. 解密失败（标签不对）= 数据被改或密钥/nonce 错，按错误处理，别“忽略认证”。

**Go 对比：**
```go
block, _ := aes.NewCipher(key)
gcm, _ := cipher.NewGCM(block)
nonce := make([]byte, gcm.NonceSize())
// crypto/rand.Read(nonce)
out := gcm.Seal(nonce, nonce, plaintext, nil)
```
- **Go 怎么做**：`crypto/aes` + `cipher.NewGCM`。
- **Rust 为什么不同**：逻辑相同，API 在 `aes-gcm`/`ring`。
- **Go 程序员易踩的坑**：两边都容易复用 nonce——这是协议设计错，不是语言错。

**记忆点：**
- AES-GCM = 加密 + 防篡改。
- 密钥保密，nonce 唯一且常可公开。

---

## Q7. HMAC 怎么做？和 Go hmac 怎么对照？ {#q7}
**Tags:** `common` `HMAC` `sha2` `mac`
**适用版本:** hmac + sha2 crate

**一句话答案：**
**HMAC**（Hash-based Message Authentication Code）= 密钥 + 哈希算法生成消息认证码。Rust 用 `hmac` + `sha2` 的 `Hmac<Sha256>`；对标 Go `crypto/hmac` + `sha256.New`。验证时用常量时间比较（见 [Q8](#q8)），不要 `==` 字节切片。

**解答：**

```toml
[dependencies]
hmac = "0.12"
sha2 = "0.10"
hex = "0.4"
```

签名（text）：

```text
use hmac::{Hmac, Mac};
use sha2::Sha256;

type HmacSha256 = Hmac<Sha256>;

let mut mac = HmacSha256::new_from_slice(b"secret-key")?;
mac.update(b"message");
let tag = mac.finalize().into_bytes();
```

验证（text）：

```text
let mut mac = HmacSha256::new_from_slice(b"secret-key")?;
mac.update(b"message");
// 库常提供 verify_slice：内部常量时间
mac.verify_slice(&expected_tag)?;
```

对照表：

| 步骤 | Go | Rust |
|------|----|------|
| 构造 | `hmac.New(sha256.New, key)` | `Hmac::<Sha256>::new_from_slice(key)` |
| 写入 | `Write` / `Sum` | `update` / `finalize` |
| 校验 | `hmac.Equal` | `verify_slice` / `subtle` |

**Go 对比：**
```go
mac := hmac.New(sha256.New, []byte("secret-key"))
mac.Write([]byte("message"))
sum := mac.Sum(nil)
ok := hmac.Equal(sum, other)
```
- **Go 怎么做**：std `crypto/hmac`。
- **Rust 为什么不同**：`hmac` crate + 哈希实现 crate 组合。
- **Go 程序员易踩的坑**：用字符串 `==` 比 tag，或把 HMAC 密钥硬编码进仓库（见 [Q10](#q10)）。

**记忆点：**
- HMAC = 有密钥的完整性。
- 校验走 `verify`/`Equal`，别明文 `==`。

---

## Q8. 常量时间比较（subtle）为什么重要？ {#q8}
**Tags:** `common` `subtle` `constant-time` `side-channel`
**适用版本:** subtle crate；原则通用

**一句话答案：**
普通 `==` 可能“早期退出”，耗时依赖首个差异位置，给攻击者测 **侧信道**（side channel）。MAC/token/密码哈希校验要用 **常量时间比较**（`subtle::ConstantTimeEq` 或库自带的 `verify`），对标 Go `subtle.ConstantTimeCompare` / `hmac.Equal`。

**解答：**

```toml
[dependencies]
subtle = "2"
```

示意：

```text
use subtle::ConstantTimeEq;

let a: [u8; 32] = /* 期望 tag */;
let b: [u8; 32] = /* 计算 tag */;
let ok = bool::from(a.ct_eq(&b));
if !ok {
    // 拒绝
}
```

何时必须：
- HMAC/AEAD tag、API token、会话秘密的字节级比较。
- 任何“攻击者可反复提交、观察快慢”的秘密比较。

何时不强制：
- 比较两个公开字符串、业务 ID、非秘密配置——普通相等即可。

「❌ 错误写法」：

```text
if computed_mac == provided_mac { ... } // 切片/数组的短路径比较有风险
```

**Go 对比：**
```go
import "crypto/subtle"
subtle.ConstantTimeCompare(a, b) == 1
// 或 hmac.Equal(a, b)
```
- **Go 怎么做**：`crypto/subtle`。
- **Rust 为什么不同**：crate 也叫 **subtle**，API 是 `ct_eq` 一类。
- **Go 程序员易踩的坑**：知道 Go 有 `hmac.Equal`，Rust 里却随手 `==`。

**记忆点：**
- 秘密字节 → 常量时间。
- 优先用库的 `verify_*`，少手写比较。

---

## Q9. TLS 证书与校验该谁管？ {#q9}
**Tags:** `common` `TLS` `rustls` `certificate`
**适用版本:** 应用层选型；细节见 HTTP 篇

**一句话答案：**
应用一般**不自己实现 TLS**：客户端/服务器通过 **rustls**（或 native-tls）由 HTTP/gRPC 栈挂上证书与主机名校验。证书从哪来、如何轮换是运维/配置问题；密码学握手细节交给 TLS 库。展开见 [40-http-client-and-server](../40-http-client-and-server/)（rustls vs native-tls、HTTPS 客户端）。

**解答：**
职责切分：

```text
你（应用）     ：选 https://、挂服务端证书/私钥路径、配置根 CA（若私有 PKI）
HTTP 栈        ：reqwest / axum+hyper / tonic transport
TLS 实现       ：rustls 或 native-tls
操作系统/容器  ：根证书商店（native-tls 路径更依赖它）
```

和本篇其它题的边界：
- 自己算 SHA、做 AES-GCM = **应用层数据保护**。
- HTTPS 上的信道保密 = **TLS**，别重复造握手。
- “证书钉扎 / 自定义 CA”属于 TLS 配置，不是 `sha2` 题。

最小心智：开发用明文要自觉，生产默认 TLS；具体 feature 与代码见 40 篇，不在此复述一整套 Client builder。

**Go 对比：**
- **Go 怎么做**：`crypto/tls` + `http.Client` / `http.Server` 的 `TLSConfig`。
- **Rust 为什么不同**：TLS 不在 std，而在 rustls 等；经 HTTP crate 的 feature 接入。
- **Go 程序员易踩的坑**：在 Rust 里找 `crypto/tls` 包——应去 rustls + [40 篇](../40-http-client-and-server/)。

**记忆点：**
- TLS ≠ 自己实现握手。
- 证书/HTTPS 细节链到 40。

---

## Q10. 密钥怎么放？为什么别进仓库？ {#q10}
**Tags:** `common` `secret` `env` `configuration`
**适用版本:** 部署实践；与配置篇配合

**一句话答案：**
密钥、token、私钥只进 **环境变量 / 密钥管理服务 / 挂载的密钥文件**，**永不提交 git**。代码只读配置接口；本地可用 `.env`（已 gitignore）。分层与加载见 [44-configuration](../44-configuration/)。

**解答：**
推荐形状：

```text
仓库里：Config 结构体 + 默认非秘密项 + “从哪读秘密”的键名
仓库外：APP_DB_PASSWORD / 云厂商 Secret Manager / K8s Secret 挂载
```

读取示意（仅 std，可编译思路）：

```rust
fn load_api_key() -> Result<String, String> {
    std::env::var("APP_API_KEY").map_err(|_| "missing APP_API_KEY".into())
}

fn main() {
    match load_api_key() {
        Ok(k) => println!("loaded key, len={}", k.len()), // 勿打印密钥本身
        Err(e) => eprintln!("{e}"),
    }
}
```

「❌ 错误做法」：
- `const API_KEY: &str = "sk-..."` 写进源码。
- 把 `secrets.toml` / `*.pem` 提交进仓库。
- 日志/tracing 打印完整 Authorization 头或私钥。

「✅ 最小纪律」：
- `.gitignore` 掉 `.env`、私钥、本地覆盖配置。
- CI 用密文变量注入。
- 轮换密钥时只改运行环境，不改业务逻辑。

**Go 对比：**
- **Go 怎么做**：同样 `os.Getenv` / Vault 等；官方也警告别把秘密写进源码。
- **Rust 为什么不同**：实践相同；配置合并常看 figment/`config`（44 篇）。
- **Go 程序员易踩的坑**：两边都有人为省事硬编码——语言都不救你。

**记忆点：**
- 秘密在环境，不在仓库。
- 细节链到 [44-configuration](../44-configuration/)。

---

## Q11. 和 Go crypto/* 的总对照表？ {#q11}
**Tags:** `hot` `cheat-sheet` `crypto` `Go`
**适用版本:** 生态对照；crate 名以 crates.io 为准

**一句话答案：**
把 Go 的 `crypto/*` / `x/crypto` 映射到 Rust 的若干 crate：摘要→`sha2`/`blake3`，HMAC→`hmac`，AEAD→`aes-gcm`/`ring`，密码→`argon2`/`bcrypt`，随机→`getrandom`/`OsRng`，TLS→`rustls`，常量时间→`subtle`。

**解答：**

| Go | Rust 常见对应 | 本篇 |
|----|---------------|------|
| `crypto/sha256` | `sha2` | [Q3](#q3) |
| `crypto/md5` | `md-5`（仅遗留） | [Q2](#q2) |
| `crypto/hmac` | `hmac` + `sha2` | [Q7](#q7) |
| `crypto/aes` + GCM | `aes-gcm` / `ring` | [Q6](#q6) |
| `crypto/rand` | `getrandom` / `rand::rngs::OsRng` | [Q5](#q5) |
| `crypto/subtle` | `subtle` | [Q8](#q8) |
| `crypto/tls` | `rustls`（经 HTTP 栈） | [Q9](#q9) |
| `x/crypto/bcrypt` | `bcrypt` / `argon2` | [Q4](#q4) |
| `x/crypto/pbkdf2` 等 | `pbkdf2` / `argon2` 等 | 密码/KDF |
| `encoding/hex` | `hex` / `data-encoding` | 展示用 |

总原则再缩一句：

```text
Go:  一个标准库命名空间 crypto/*
Rust: 多个可替换 crate；先选对“问题类型”，再选实现
```

**Go 对比：**
- **Go 怎么做**：先 `import "crypto/..."`。
- **Rust 为什么不同**：按问题选 crate，std 不托管算法实现。
- **Go 程序员易踩的坑**：找“官方唯一包”而犹豫——先按上表选默认，再按审计需求替换。

**记忆点：**
- 先对问题类型，再对 crate 名。
- 本表可当速查书签。

---

## Q12. 什么时候必须请安全专家，而不是抄示例？ {#q12}
**Tags:** `occasional` `security` `threat-model` `review`
**适用版本:** 工程判断；与 Rust 版本无关

**一句话答案：**
一旦涉及**真实对抗模型**（钱、身份、长期密钥、合规、自研协议、新型密码学），就不要只靠博客/`Chat` 示例：请安全/密码学评审。教程代码只教 API 形状，不替你做威胁建模。

**解答：**
建议升级到专家评审的信号：
- 自研“类 JWT / 手写握手 / 自创加密模式拼接”。
- 密钥托管、多方计算、硬件密钥、HSM、合规（PCI、等保相关）。
- 处理高价值资产：支付、医疗、大规模个人数据。
- 你改了 nonce 策略、自己组合 encrypt-then-MAC、关闭证书校验“先通再说”。

教程/本篇**足够**的场景：
- 用成熟 AEAD、TLS、argon2、HMAC 的**标准用法**。
- 跟着库文档做 encrypt/decrypt、verify。

「❌ 危险抄法」：
- 从旧文复制 ECB、固定 IV、MD5 密码、`InsecureSkipVerify` 永久化。
- 把示例密钥提交进生产配置。

决策口诀：

```text
标准库/标准模式 + 官方文档推荐参数 → 可自行落地，仍要 code review
新协议 / 新组合 / 高风险资产        → 找专家，先威胁建模再写代码
```

**Go 对比：**
- **Go 怎么做**：同样不能靠 `crypto` 示例替代安全设计；`InsecureSkipVerify` 陷阱两边都有。
- **Rust 为什么不同**：crate 更多，**抄错依赖/错 feature** 的空间也更大。
- **Go 程序员易踩的坑**：以为“用了 rustls/aes-gcm 就自动安全”——用法错照样不安全。

**记忆点：**
- 示例教调用，不教威胁模型。
- 高风险或自研协议 → 请人审。

---

## Q13. JWT / 签名校验入门直觉？ {#q13}
**Tags:** `hot` `JWT` `jsonwebtoken` `signature`
**适用版本:** 选型与用法以 crates.io / 库文档为准

**一句话答案：**
**别自己拼 JWT**（**JSON Web Token**，JSON Web 令牌：Base64 三段 + 手写 HMAC 字符串）。用成熟库（常见如 **`jsonwebtoken`**）做 encode/decode，并显式校验 **算法、过期、签发方** 等 claim。JWT 是「可验证的声明格式」，不是加密保险箱——默认 payload 可读。

**解答：**
入门直觉：
1. Header + Payload + Signature；签名证明「持有密钥的人签过」，不是自动保密。
2. 校验时拒绝 `alg=none`、拒绝「库说可用但你业务不该接受」的算法漂移。
3. 密钥/公钥来自安全配置（见 [Q10](#q10)），别写进仓库。

```toml
[dependencies]
jsonwebtoken = "9"
serde = { version = "1", features = ["derive"] }
```

```text
use jsonwebtoken::{decode, encode, Algorithm, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,
    exp: usize,
}

// 签发（示意）
let claims = Claims { sub: "ada".into(), exp: /* unix 过期秒 */ 0 };
let token = encode(
    &Header::new(Algorithm::HS256),
    &claims,
    &EncodingKey::from_secret(b"use-env-secret"),
)?;

// 校验（示意）：Validation 里固定算法，检查 exp 等
let mut validation = Validation::new(Algorithm::HS256);
let data = decode::<Claims>(
    &token,
    &DecodingKey::from_secret(b"use-env-secret"),
    &validation,
)?;
```

标准库没有 JWT；对照「只做摘要」的形状可用 sha2（完整性另见 [Q3](#q3)、[Q14](#q14)）：

```rust
fn main() {
    // JWT ≠ 哈希文件；这里只强调：业务令牌别手搓协议
    let _parts = ["header", "payload", "signature"];
    assert_eq!(_parts.len(), 3);
}
```

「❌ 危险」：复制博客里的 `Validation::default()` 却关掉 `exp`、或接受多种算法「先通再说」——见 [Q12](#q12)。

**Go 对比：**

```go
import "github.com/golang-jwt/jwt/v5"
```

- **Go 怎么做**：同样用 `golang-jwt` 等库，不手写三段拼接。
- **Rust 为什么不同**：也在 crate；API 名不同，原则相同。
- **Go 程序员易踩的坑**：把「能 decode」当成「已授权」——还要查 claim 与权限模型。

**记忆点：**
- 用库，不手搓 JWT。
- 校验算法 + 时间类 claim + 密钥来源。
- JWT 默认不加密 payload。

---

## Q14. 文件 / 下载完整性怎么校验（对照 sha256sum）？ {#q14}
**Tags:** `common` `SHA-256` `integrity` `sha256sum`
**适用版本:** `sha2` crate；与系统 `sha256sum` 互相对照

**一句话答案：**
对文件字节算 **SHA-256**，把十六进制摘要和发布方提供的（或 `sha256sum` 输出）**逐字符对照**。一致才信任内容；这解决「传错/损毁/被改」，不替代签名身份体系（签名见 [Q13](#q13) / 专家场景见 [Q12](#q12)）。

**解答：**
依赖与流式哈希（大文件别一次读进内存）：

```toml
[dependencies]
sha2 = "0.10"
hex = "0.4"
```

```text
use sha2::{Digest, Sha256};
use std::fs::File;
use std::io::{Read, copy};

fn sha256_file(path: &str) -> std::io::Result<String> {
    let mut file = File::open(path)?;
    let mut hasher = Sha256::new();
    copy(&mut file, &mut hasher)?;
    Ok(hex::encode(hasher.finalize()))
}

// 与官方公布的 expected_hex 比较；或与 `sha256sum file` 输出对照
```

最小「内存中对照」示意（完整程序，无外部 crate 时先展示流程）：

```rust
fn main() {
    let expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824";
    let got = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"; // "hello" 的 SHA-256
    assert_eq!(expected, got);
}
```

命令行对照习惯：

```text
# 系统工具
sha256sum release.tar.gz
# 输出形如：<64 hex>  release.tar.gz
# 与网页/签名说明里的哈希比对
```

「❌ 不够」：只比对文件大小或文件名；或用 MD5 当安全完整性（见 [Q2](#q2)）。

**Go 对比：**

```go
import (
	"crypto/sha256"
	"encoding/hex"
	"io"
	"os"
)

func sum(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()
	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		return "", err
	}
	return hex.EncodeToString(h.Sum(nil)), nil
}
```

- **Go 怎么做**：`crypto/sha256` + `io.Copy`，与 `sha256sum` 同一摘要。
- **Rust 为什么不同**：算法在 `sha2` crate，流程一样。
- **Go 程序员易踩的坑**：用字符串 `==` 比摘要没问题；但若涉及 MAC/签名 tag，要用常量时间比较（见本篇 HMAC 相关题）。

**记忆点：**
- 文件完整性 → SHA-256 hex ↔ `sha256sum`。
- 大文件流式 `update`/`copy`。
- 完整性 ≠ 身份认证；高要求再叠加签名。
