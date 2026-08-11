+++
title = "06-更新日志"
date = 2026-07-30T14:49:00+08:00
weight = 60
type = "docs"
description = "Cargo 各版本变更说明（与官网 CHANGELOG 对应）"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/CHANGELOG.html)（源：cargo 标签 0.98.0 / Rust 1.97 文档）

# 更新日志


> 原文链接: [https://doc.rust-lang.org/cargo/CHANGELOG.html](https://doc.rust-lang.org/cargo/CHANGELOG.html)


## Cargo 1.97 (2026-07-09)
[eb94155a...HEAD](https://github.com/rust-lang/cargo/compare/eb94155a...HEAD)


### 新增

- 为 `--manifest-path` 增加 `-m` 简写
  [#16858](https://github.com/rust-lang/cargo/pull/16858)

### 变更

- 改进误输入 `-p` 时的错误信息，会建议相似的工作空间成员名称
  [#16844](https://github.com/rust-lang/cargo/pull/16844)
- cargo-clean：当 `--target-dir` 看起来不像 Cargo 目标目录时报错。
  这可防止误删非目标目录。
  [#16712](https://github.com/rust-lang/cargo/pull/16712)
  [#16878](https://github.com/rust-lang/cargo/pull/16878)

### 修复

### 仅 Nightly

- `-Zscript`：教用户如何固定 edition
  [#16851](https://github.com/rust-lang/cargo/pull/16851)
- `-Zcargo-lints`：优先使用已定义的 lint 级别，而非默认级别
  [#16879](https://github.com/rust-lang/cargo/pull/16879)
- `-Zcargo-lints`：`unused_dependencies` 忽略 rustc 的
  `unused_crate_dependencies` lint 状态
  [#16877](https://github.com/rust-lang/cargo/pull/16877)

### 文档

- 澄清 registry 的 `config.json` 中 “api” 不应包含尾部斜杠。
  [#16869](https://github.com/rust-lang/cargo/pull/16869)

### 内部

- 更新依赖。
  [#16883](https://github.com/rust-lang/cargo/pull/16883)
- ci：将 GitHub Actions 固定到提交 SHA
  [#16867](https://github.com/rust-lang/cargo/pull/16867)
  [#16868](https://github.com/rust-lang/cargo/pull/16868)
- test：为经由 github 快路径的 cargo install 添加测试
  [#16866](https://github.com/rust-lang/cargo/pull/16866)

## Cargo 1.96 (2026-05-28)
[f298b8c8...rust-1.96.0](https://github.com/rust-lang/cargo/compare/f298b8c8...rust-1.96.0)

### 新增

- 在 Cargo 配置中支持 `target.'cfg(..)'.rustdocflags`。
  [#16846](https://github.com/rust-lang/cargo/pull/16846)
- cargo-help：为嵌套子命令显示 manpage。
  例如 `cargo help report future-incompat`。
  [#16432](https://github.com/rust-lang/cargo/pull/16432)

### 变更

- 改进查找父工作空间时的错误信息，
  解释 Cargo 为何向上搜索，并建议变通做法。
  [#16669](https://github.com/rust-lang/cargo/pull/16669)
- 澄清与 edition 相关的警告信息，
  使 `Cargo.toml` 与脚本使用更一致的措辞。
  [#16676](https://github.com/rust-lang/cargo/pull/16676)
- Shell 补全会在命令之前补全 `--config` 与 `--color`。
  [#16780](https://github.com/rust-lang/cargo/pull/16780)
- 将 `build-dir` 并发文件锁拆分为专用锁，
  同时对 `.cargo-lock` 保持共享锁，以便新旧 Cargo
  可同时在同一目标目录上运行。
  [#16708](https://github.com/rust-lang/cargo/pull/16708)
  [#16887](https://github.com/rust-lang/cargo/pull/16887)
- 依赖的多位置现已支持 `git` 与备用 registry。
  例如 `{ git = "https://...", registry = "my-registry" }`。
  [#16810](https://github.com/rust-lang/cargo/pull/16810)
- `term.progress.term-integration` 可检测 Ptyxis 终端支持。
  [#16730](https://github.com/rust-lang/cargo/pull/16730)
- 改进错误信息以遵循 rustc 诊断风格。
  [#16795](https://github.com/rust-lang/cargo/pull/16795)
  [#16711](https://github.com/rust-lang/cargo/pull/16711)
- 在 macOS 上将目标目录排除在 iCloud Drive 同步之外
  [#16728](https://github.com/rust-lang/cargo/pull/16728)
- 在 `rustc -vV` 目标发现探测期间设置 `CARGO` 环境变量
  [#16811](https://github.com/rust-lang/cargo/pull/16811)
- 当备用 registry 拒绝 token 时，提示预期的认证方案。
  [#16794](https://github.com/rust-lang/cargo/pull/16794)
- 对无效的 jobserver 文件描述符发出警告
  [#16843](https://github.com/rust-lang/cargo/pull/16843)
- cargo-clean：校验目标目录不是文件
  [#16765](https://github.com/rust-lang/cargo/pull/16765)
- cargo-install：使用非默认工具链安装时发出警告
  [#16131](https://github.com/rust-lang/cargo/pull/16131)
- cargo-publish：API 请求发送 `Content-Type: application/octet-stream` 头
  [#16832](https://github.com/rust-lang/cargo/pull/16832)
- cargo-tree：澄清在未指定包名时使用 `-i` 的错误信息
  [#16818](https://github.com/rust-lang/cargo/pull/16818)

### 修复

- 为 fetch 保留类 SCP 的子模块 URL。这是 1.94 中的回归。
  [#16727](https://github.com/rust-lang/cargo/pull/16727)
  [#16744](https://github.com/rust-lang/cargo/pull/16744)
- 修复在创建 lockfile 之后，从非 GitHub 主机
  使用非默认 refspec 拉取 git 依赖的问题。
  [#16768](https://github.com/rust-lang/cargo/pull/16768)
- 修复包 URL 规格以无版本的尾部 `#` 结尾时的 panic。
  [#16754](https://github.com/rust-lang/cargo/pull/16754)
- cargo-publish：修复工作空间发布中因循环依赖导致的静默挂起与超时。
  [#16722](https://github.com/rust-lang/cargo/pull/16722)

### 仅 Nightly

- `unstable-editions`：当包声明不稳定 edition 时，
  在错误中显示所需的 Rust 版本。
  [#16653](https://github.com/rust-lang/cargo/pull/16653)
- `native-completions`：补全 `--config` 参数
  [#16249](https://github.com/rust-lang/cargo/pull/16249)
- `-Zbuild-dir-new-layout`：在新布局中简化构建脚本二进制名称
  [#16812](https://github.com/rust-lang/cargo/pull/16812)
  [#16855](https://github.com/rust-lang/cargo/pull/16855)
- `-Zbuild-std`：在 `unused-crate-dependencies` lint 中忽略隐式 std 依赖
  [#16677](https://github.com/rust-lang/cargo/pull/16677)
- `-Zcargo-lints`：添加 `unused_dependencies` lint
  [#16600](https://github.com/rust-lang/cargo/pull/16600)
- `-Zlockfile-path`：cargo-install 忽略 `resolver.lockfile-path`
  [#16823](https://github.com/rust-lang/cargo/pull/16823)
- `-Zscript`：为 `cargo fix` 向脚本注入 edition。
  [#16678](https://github.com/rust-lang/cargo/pull/16678)
- `-Zscript`：对嵌入式内容抑制 `unused_features` lint
  [#16714](https://github.com/rust-lang/cargo/pull/16714)
- `-Zscript`：在 quiet 模式下仍强制显示脚本 edition 警告
  [#16848](https://github.com/rust-lang/cargo/pull/16848)
- `-Zjson-target-spec`：在错误信息中说明这是 cargo 的 Z flag
  [#16793](https://github.com/rust-lang/cargo/pull/16793)
- `-Zwarnings`：`build.warnings=allow` 不应隐藏被拒绝的诊断与硬警告
  [#16824](https://github.com/rust-lang/cargo/pull/16824)
  [#16827](https://github.com/rust-lang/cargo/pull/16827)
- `-Zwarnings`：使 build.warnings 忽略非本地依赖
  [#16760](https://github.com/rust-lang/cargo/pull/16760)
- `-Zwarnings`：在拒绝警告且未使用 `--keep-going` 时停止
  [#16725](https://github.com/rust-lang/cargo/pull/16725)
- `-Zwarnings`：也将警告摘要转为错误
  [#16721](https://github.com/rust-lang/cargo/pull/16721)

### 文档

- 澄清 `CARGO_TARGET_DIR` 不必是相对路径
  [#16735](https://github.com/rust-lang/cargo/pull/16735)
- 澄清构建脚本的当前目录
  [#16703](https://github.com/rust-lang/cargo/pull/16703)
- 列出依赖中不稳定 `public` 字段所需的最低 MSRV
  [#16841](https://github.com/rust-lang/cargo/pull/16841)

### 内部

- 🎉 新成员 crate [`cargo-util-terminal`](https://crates.io/crates/cargo-util-terminal)！
  其中包含 Cargo 的终端渲染工具，
  包括 shell 输出、样式与诊断报告。
  它遵循 Rust 的 [6 周发布流程](https://doc.crates.io/contrib/process/release.html#cratesio-publishing)。
  [#16809](https://github.com/rust-lang/cargo/pull/16809)
- 对 registry 网络操作使用异步
  [#16745](https://github.com/rust-lang/cargo/pull/16745)
  [#16752](https://github.com/rust-lang/cargo/pull/16752)
  [#16763](https://github.com/rust-lang/cargo/pull/16763)
- 从内部 crate 导出公共依赖
  [#16819](https://github.com/rust-lang/cargo/pull/16819)
- 将超链接逻辑抽到新的 `anstyle-hyperlink` 包
  [#16749](https://github.com/rust-lang/cargo/pull/16749)
- 将终端集成抽到新的 `anstyle-progress` 包
  [#16757](https://github.com/rust-lang/cargo/pull/16757)
- 让 git 自行决定何时运行 `git gc`，而不再手动统计 packfile。
  [#16459](https://github.com/rust-lang/cargo/pull/16459)
- cargo-test-support：从测试环境中剥离 `RUSTUP_TOOLCHAIN_SOURCE`
  [#16857](https://github.com/rust-lang/cargo/pull/16857)
- cargo-test-support：修复在长目标目录路径下的 `symlink_and_directory`。
  [#16775](https://github.com/rust-lang/cargo/pull/16775)
- ci：检测用户对 src/etc/man 的更改
  [#16736](https://github.com/rust-lang/cargo/pull/16736)
- ci：将 cargo-semver-checks 更新到 v0.47.0
  [#16723](https://github.com/rust-lang/cargo/pull/16723)
- 更新依赖。
  [#16685](https://github.com/rust-lang/cargo/pull/16685)
  [#16690](https://github.com/rust-lang/cargo/pull/16690)
  [#16710](https://github.com/rust-lang/cargo/pull/16710)
  [#16716](https://github.com/rust-lang/cargo/pull/16716)
  [#16771](https://github.com/rust-lang/cargo/pull/16771)
  [#16778](https://github.com/rust-lang/cargo/pull/16778)
  [#16786](https://github.com/rust-lang/cargo/pull/16786)
  [#16808](https://github.com/rust-lang/cargo/pull/16808)
  [#16820](https://github.com/rust-lang/cargo/pull/16820)
  [#16825](https://github.com/rust-lang/cargo/pull/16825)
  [#16828](https://github.com/rust-lang/cargo/pull/16828)
  [#16833](https://github.com/rust-lang/cargo/pull/16833)
  [#16859](https://github.com/rust-lang/cargo/pull/16859)

## Cargo 1.95 (2026-04-16)
[85eff7c8...rust-1.95.0](https://github.com/rust-lang/cargo/compare/85eff7c8...rust-1.95.0)

### 新增

### 变更

- ❗️ 禁止在主目录中执行 `cargo init`，以避免清单发现相关问题。
  这此前会导致尝试使用 Cargo 的新用户陷入令人困惑的状态。
  [#16566](https://github.com/rust-lang/cargo/pull/16566)
- HTML 计时报告现改用 SVG 而非 canvas 渲染。
  canvas 渲染选项已完全移除。
  这可提升大型依赖图上的响应性与性能，
  并支持在图表中选择文本。
  [#16602](https://github.com/rust-lang/cargo/pull/16602)
  [#16607](https://github.com/rust-lang/cargo/pull/16607)
- 改进错误信息以遵循 rustc 诊断风格。
  [#16498](https://github.com/rust-lang/cargo/pull/16498)
  [#16625](https://github.com/rust-lang/cargo/pull/16625)
  [#16643](https://github.com/rust-lang/cargo/pull/16643)
- 改进错误清单的错误信息
  [#16630](https://github.com/rust-lang/cargo/pull/16630)
- 即使在工作空间根目录之外也建议 `workspace.members` 条目
  [#16616](https://github.com/rust-lang/cargo/pull/16616)
- `term.progress.term-integration` 可检测 iTerm 是否支持 ANSI OSC 9;4 序列。
  [#16506](https://github.com/rust-lang/cargo/pull/16506)
- cargo-install：使错误信息感知 `build.build-dir`
  [#16623](https://github.com/rust-lang/cargo/pull/16623)
- cargo-remove：当要移除的依赖存在于其他表中时，
  建议 `--dev`、`--build` 或 `--target` 标志。
  [#16533](https://github.com/rust-lang/cargo/pull/16533)

### 修复

- 修复 `cargo test --frozen` 尝试下载
  指定测试实际并不需要的依赖。
  [#16221](https://github.com/rust-lang/cargo/pull/16221)
- 修复 `net.known_hosts` 对否定规则的解析。
  [#16596](https://github.com/rust-lang/cargo/pull/16596)
- 仅在 SVG 计时渲染器的 `units` 非空时计算 `y_ticks`。
  [#16575](https://github.com/rust-lang/cargo/pull/16575)
- 在建议的 fix 信息中尊重 Clippy CLI 参数 `CLIPPY_ARGS`。
  [#16652](https://github.com/rust-lang/cargo/pull/16652)
- 修复 `cargo package` 在覆盖更大的已有文件时
  生成损坏的 `.crate` 文件。
  [#16713](https://github.com/rust-lang/cargo/pull/16713)

### 仅 Nightly

- 🔥 `-Zhost-config`：添加 `host.runner` 以包装主机构建目标的执行
  [#16599](https://github.com/rust-lang/cargo/pull/16599)
  [#16674](https://github.com/rust-lang/cargo/pull/16674)
  [#16638](https://github.com/rust-lang/cargo/pull/16638)
  [#16631](https://github.com/rust-lang/cargo/pull/16631)
- `--artifact-dir`：移除已弃用的不稳定 `--out-dir`
  [#16608](https://github.com/rust-lang/cargo/pull/16608)
- `-Zbuild-analysis`：向 BuildStarted 消息添加 command 字段
  [#16577](https://github.com/rust-lang/cargo/pull/16577)
- `-Zbuild-dir-new-layout`：更新 layout 模块文档以说明新布局
  [#16502](https://github.com/rust-lang/cargo/pull/16502)
- `-Zbuild-dir-new-layout`：将产物依赖存储在构建单元目录中。
  [#16519](https://github.com/rust-lang/cargo/pull/16519)
- `-Zbuild-dir-new-layout`：在新 build-dir 布局中将构建脚本运行的 `output` 目录改为 `stdout`
  [#16644](https://github.com/rust-lang/cargo/pull/16644)
  [#16645](https://github.com/rust-lang/cargo/pull/16645)
- `-Zbuild-dir-new-layout`：为新 build-dir 布局重组构建单元目录布局
  [#16542](https://github.com/rust-lang/cargo/pull/16542)
- `-Zcargo-lints`：添加 `non_kebab_case_bins` lint
  [#16524](https://github.com/rust-lang/cargo/pull/16524)
  [#16553](https://github.com/rust-lang/cargo/pull/16553)
- `-Zcargo-lints`：添加 `missing_lints_inheritance` lint
  [#16588](https://github.com/rust-lang/cargo/pull/16588)
- `-Zcargo-lints`：添加 `unused_workspace_package_fields` lint
  [#16585](https://github.com/rust-lang/cargo/pull/16585)
- `-Zcargo-lints`：添加 `unused_workspace_dependencies` lint
  [#16571](https://github.com/rust-lang/cargo/pull/16571)
- `-Zcargo-lints`：添加 `redundant_homepage` lint
  [#16561](https://github.com/rust-lang/cargo/pull/16561)
  [#16564](https://github.com/rust-lang/cargo/pull/16564)
- `-Zcargo-lints`：添加 `redundant_readme` lint
  [#16552](https://github.com/rust-lang/cargo/pull/16552)
- `-Zcargo-lints`：添加 `non_*_case_features` lint
  [#16560](https://github.com/rust-lang/cargo/pull/16560)
- `-Zcargo-lints`：添加互斥的 `non_{kebab,snake}_case_packages`
  [#16554](https://github.com/rust-lang/cargo/pull/16554)
- `-Zcargo-lints`：每个包只显示一次 `implicit_minimum_version_req` lint 来源。
  [#16535](https://github.com/rust-lang/cargo/pull/16535)
- `-Zcargo-lints`：当 MSRV 过旧时不运行默认开启的 lint
  [#16618](https://github.com/rust-lang/cargo/pull/16618)
- `-Zfine-grain-locking`：修复并行锁定
  [#16659](https://github.com/rust-lang/cargo/pull/16659)
- `-Zhost-config`：`host.linker` 不应应用于非主机单元
  [#16641](https://github.com/rust-lang/cargo/pull/16641)
- `-Zjson-target-spec`：添加新的 `-Zjson-target-spec` flag，以协助
  使用自定义 `.json` 目标规格文件。
  [#16557](https://github.com/rust-lang/cargo/pull/16557)
- `-Zlockfile-path`：移除 `--lockfile-path`
  [#16621](https://github.com/rust-lang/cargo/pull/16621)
- `-Zlockfile-path`：在 fix、install 中尊重该配置
  [#16617](https://github.com/rust-lang/cargo/pull/16617)
- `-Zscript`：相对脚本加载配置
  [#16620](https://github.com/rust-lang/cargo/pull/16620)
- `-Zscript`：使 lockfile 特定于脚本，独立于 build-dir
  [#16619](https://github.com/rust-lang/cargo/pull/16619)
- `-Zscript`：修正帮助信息的风格
  [#16580](https://github.com/rust-lang/cargo/pull/16580)
- `-Zscript`：显示其余工作空间行为
  [#16633](https://github.com/rust-lang/cargo/pull/16633)
- `-Ztrim-paths`：使用已稳定的 `-Cremap-path-scope` rustc flag。
  [#16536](https://github.com/rust-lang/cargo/pull/16536)

### 文档

- 改进关于用构建脚本读取 cfg 值的文档
  [#16671](https://github.com/rust-lang/cargo/pull/16671)
- 讨论命令与别名
  [#16581](https://github.com/rust-lang/cargo/pull/16581)
- 移除多余的主页链接
  [#16572](https://github.com/rust-lang/cargo/pull/16572)
- cargo-report：增强 `cargo report *` 的 man page
  [#16430](https://github.com/rust-lang/cargo/pull/16430)

### 内部

- 在 `--timings` 与 `-Zbuild-analysis` 之间复用计时指标收集逻辑。
  [#16497](https://github.com/rust-lang/cargo/pull/16497)
- 添加在符号链接目标变更时检查指纹的测试
  [#16661](https://github.com/rust-lang/cargo/pull/16661)
- 更新 build-std 测试以反映编译器更新。
  [#16550](https://github.com/rust-lang/cargo/pull/16550)
  [#16551](https://github.com/rust-lang/cargo/pull/16551)
  [#16559](https://github.com/rust-lang/cargo/pull/16559)
  [#16658](https://github.com/rust-lang/cargo/pull/16658)
- 启用 triagebot 新的 `[view-all-comments-link]` 功能
  [#16629](https://github.com/rust-lang/cargo/pull/16629)
- 增加 cache_lock 测试超时
  [#16545](https://github.com/rust-lang/cargo/pull/16545)
- cargo-help：为 cargo help 测试做快照
  [#16626](https://github.com/rust-lang/cargo/pull/16626)
  [#16627](https://github.com/rust-lang/cargo/pull/16627)
- 更新依赖。
  [#16387](https://github.com/rust-lang/cargo/pull/16387)
  [#16538](https://github.com/rust-lang/cargo/pull/16538)
  [#16548](https://github.com/rust-lang/cargo/pull/16548)
  [#16570](https://github.com/rust-lang/cargo/pull/16570)
  [#16578](https://github.com/rust-lang/cargo/pull/16578)
  [#16579](https://github.com/rust-lang/cargo/pull/16579)
  [#16587](https://github.com/rust-lang/cargo/pull/16587)
  [#16589](https://github.com/rust-lang/cargo/pull/16589)
  [#16593](https://github.com/rust-lang/cargo/pull/16593)
  [#16601](https://github.com/rust-lang/cargo/pull/16601)
  [#16613](https://github.com/rust-lang/cargo/pull/16613)
  [#16615](https://github.com/rust-lang/cargo/pull/16615)
  [#16624](https://github.com/rust-lang/cargo/pull/16624)

## Cargo 1.94.1 (2026-03-26)

[85eff7c8...rust-1.94.0](https://github.com/rust-lang/cargo/compare/85eff7c8...rust-1.94.0)

### 修复

- 🚨 [CVE-2026-33055](https://github.com/advisories/GHSA-gchp-q4r4-x4ff) 与 [CVE-2026-33056](https://github.com/advisories/GHSA-j4xf-2g29-59ph)：
  解压恶意 crate 可更改类 Unix 系统上任意路径的权限。
  [#16769](https://github.com/rust-lang/cargo/pull/16769)
- 通过将 libcurl 从 8.17.0 降级到 8.15.0，修复 FreeBSD 上的证书行为。该升级在 1.94.0 中被无意引入。未来，Rust 1.95 预计会更新到 libcurl 8.19.0，届时应能从根本上解决该问题。
  [#16787](https://github.com/rust-lang/cargo/pull/16787)

## Cargo 1.94 (2026-03-05)

[2c283a9a...rust-1.94.0](https://github.com/rust-lang/cargo/compare/2c283a9a...rust-1.94.0)

### 新增

- 🎉 稳定配置项 `include` 键。
  顶层 `include` 配置键允许加载额外的配置文件，
  从而更好地在项目与环境之间组织、共享与管理 Cargo 配置。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#including-extra-configuration-files)
  [#16284](https://github.com/rust-lang/cargo/pull/16284)
- 🎉 稳定 registry 索引中的 `pubtime` 字段。
  该字段记录 crate 版本的发布时间，并为将来基于时间的依赖解析提供基础。
  注意 crates.io 会在发布新版本时逐步回填现有包。
  并非所有 crate 都已有 `pubtime`。
  [#16369](https://github.com/rust-lang/cargo/pull/16369)
  [#16372](https://github.com/rust-lang/cargo/pull/16372)
- Cargo 现为清单与配置文件解析 [TOML v1.1](https://toml.io/en/v1.1.0)。
  注意在 `Cargo.toml` 中使用这些功能会提高你的开发 MSRV，
  但已发布的清单仍与较旧解析器兼容。
  [#16415](https://github.com/rust-lang/cargo/pull/16415)
- 计时 HTML 报告现有新的 SVG 渲染选项，
  可在大型构建中获得更好的渲染性能。
  Canvas 渲染仍可用，但将被逐步淘汰。
  [#15091](https://github.com/rust-lang/cargo/pull/15091)
- `CARGO_BIN_EXE_<name>` 环境变量现不仅在编译时可访问，运行时也可访问。
  [#16421](https://github.com/rust-lang/cargo/pull/16421)
- perf：优化带多个 `--package` 说明符的 `cargo clean`。
  [#16264](https://github.com/rust-lang/cargo/pull/16264)
- perf：优化 `cargo locate-project --workspace`，在仅需工作空间根路径时
  避免完整加载工作空间。
  [#16423](https://github.com/rust-lang/cargo/pull/16423)

### 变更

- 改进 Cargo 构建目标源文件缺失时的错误信息。
  [#16338](https://github.com/rust-lang/cargo/pull/16338)
- 使用 rustc 诊断风格改进缺失依赖的错误信息。
  [#16500](https://github.com/rust-lang/cargo/pull/16500)
- 在与 patch 相关的错误信息中显示 patch 的定义位置。
  [#16407](https://github.com/rust-lang/cargo/pull/16407)
- 当请求的 feature 没有近似匹配时，列出所有可用 feature。
  [#16445](https://github.com/rust-lang/cargo/pull/16445)
- 等待文件锁时，在非常详细模式 `-vv`) 下显示 lockfile 路径。
  [#16491](https://github.com/rust-lang/cargo/pull/16491)
- cargo-new：改进包名错误信息的质量。
  [#16398](https://github.com/rust-lang/cargo/pull/16398)

### 修复

- 当 `$CARGO_HOME` 为符号链接目录时，不要重复读取配置文件。
  [#16325](https://github.com/rust-lang/cargo/pull/16325)
- cargo-info：未显式指定 registry 时，默认检查本地包。
  [#16358](https://github.com/rust-lang/cargo/pull/16358)
- cargo-info：解决 schema 查找中下划线与连字符不匹配的问题。
  [#16455](https://github.com/rust-lang/cargo/pull/16455)
- cargo-package：使用 `--list` 时跳过 registry 校验。
  [#16341](https://github.com/rust-lang/cargo/pull/16341)
- cargo-package：从工作空间成员目录运行时检测脏文件。
  [#16479](https://github.com/rust-lang/cargo/pull/16479)
- cargo-vendor：在子目录中递归过滤 `.gitattributes` 与 `.gitignores`。
  此前仅过滤顶层 Git 文件，
  导致将 vendored 代码提交到 Git 仓库时校验和失败。
  [#16439](https://github.com/rust-lang/cargo/pull/16439)
- cargo-vendor：正确从 local-registry 缓存路径解包。
  [#16435](https://github.com/rust-lang/cargo/pull/16435)

### 仅 Nightly

- 🔥 `-Zany-build-script-metadata`：允许任意构建脚本发出 `cargo::metadata=KEY=VALUE`，
  并通过 `CARGO_DEP_<name>_<key>` 环境变量暴露给依赖方。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#any-build-script-metadata)
  [#16436](https://github.com/rust-lang/cargo/pull/16436)
  [#16486](https://github.com/rust-lang/cargo/pull/16486)
  [#16489](https://github.com/rust-lang/cargo/pull/16489)
  [#16494](https://github.com/rust-lang/cargo/pull/16494)
  [#16496](https://github.com/rust-lang/cargo/pull/16496)
- `timings`：移除 `--timings=<FMT>` 可选格式值。
  `-Zbuild-analysis` 日志现为机器可读计时数据的推荐方式。
  使用不稳定的 `cargo report timings` 生成 HTML 报告。
  [#16420](https://github.com/rust-lang/cargo/pull/16420)
- `-Zlockfile-path`：添加新的 `resolver.lockfile-path` 配置以替代 CLI `--lockfile-path` 选项。
  `--lockfile-path` CLI 选项将在未来版本中移除。
  [#16510](https://github.com/rust-lang/cargo/pull/16510)
- `-Zbuild-analysis`：新增 `cargo report rebuilds` 命令，用于分析
  先前会话的重建原因。
  [#16408](https://github.com/rust-lang/cargo/pull/16408)
  [#16456](https://github.com/rust-lang/cargo/pull/16456)
- `-Zbuild-analysis`：新增 `cargo report sessions` 命令以列出构建会话 ID。
  [#16428](https://github.com/rust-lang/cargo/pull/16428)
- `-Zbuild-analysis`：新增用于 HTML 回放的 `cargo report timings` 命令。
  [#16346](https://github.com/rust-lang/cargo/pull/16346)
  [#16350](https://github.com/rust-lang/cargo/pull/16350)
  [#16352](https://github.com/rust-lang/cargo/pull/16352)
  [#16377](https://github.com/rust-lang/cargo/pull/16377)
  [#16378](https://github.com/rust-lang/cargo/pull/16378)
  [#16382](https://github.com/rust-lang/cargo/pull/16382)
  [#16390](https://github.com/rust-lang/cargo/pull/16390)
  [#16414](https://github.com/rust-lang/cargo/pull/16414)
  [#16441](https://github.com/rust-lang/cargo/pull/16441)
  [#16448](https://github.com/rust-lang/cargo/pull/16448)
  [#16485](https://github.com/rust-lang/cargo/pull/16485)
  [#16490](https://github.com/rust-lang/cargo/pull/16490)
- `-Zbuild-dir`：为构建缓存实现细粒度的单元级锁定。
  [#16155](https://github.com/rust-lang/cargo/pull/16155)
- `-Zbuild-dir-new-layout`：将构建脚本二进制移到 `deps` 目录。
  [#16515](https://github.com/rust-lang/cargo/pull/16515)
- `-Zbuild-dir-new-layout`：使用新布局时不创建 `examples` 目录。
  [#16514](https://github.com/rust-lang/cargo/pull/16514)
- `-Zbuild-dir-new-layout`：在新布局中从二进制名移除哈希。
  [#16351](https://github.com/rust-lang/cargo/pull/16351)
- `-Zbuild-dir-new-layout`：对 bin/lib 的 pkg_dirs 使用 unit_id 而非 pkg 哈希。
  [#16345](https://github.com/rust-lang/cargo/pull/16345)
- `-Zbuild-dir-new-layout`：在新构建布局中包含所有搜索路径。
  [#16348](https://github.com/rust-lang/cargo/pull/16348)
- `-Zcargo-lints`：添加类似 Clippy 的 lint 分组。
  [#16464](https://github.com/rust-lang/cargo/pull/16464)
- `-Zcargo-lints`：新增 `implicit_minimum_version_req` lint。
  [#16321](https://github.com/rust-lang/cargo/pull/16321)
- `-Zno-embed-metadata`：当该 flag 变更时使整个构建缓存失效。
  [#16513](https://github.com/rust-lang/cargo/pull/16513)
- `-Zsbom`：为空时不设置 `CARGO_SBOM_PATH`。
  [#16419](https://github.com/rust-lang/cargo/pull/16419)

### 文档

- 澄清 `OUT_DIR` 在构建之间不会被清理。
  [#16437](https://github.com/rust-lang/cargo/pull/16437)
- 记录构建脚本中 `DEBUG` 的唯一可能取值。
  [#16413](https://github.com/rust-lang/cargo/pull/16413)
- 添加如何将生成文件纳入版本控制的最佳实践。
  [#16405](https://github.com/rust-lang/cargo/pull/16405)
- 记录更多 Cargo 团队的服务与权限。
  [#16402](https://github.com/rust-lang/cargo/pull/16402)
- FAQ：加入关于磁盘空间的条目。
  [#16349](https://github.com/rust-lang/cargo/pull/16349)

### 内部

- 将 Git 子模块缓存到 Git 数据库，以加快后续 fetch。
  [#16246](https://github.com/rust-lang/cargo/pull/16246)
- 修复 Git 部分 OID 被错误地补零。
  [#16511](https://github.com/rust-lang/cargo/pull/16511)
- 将部分情况迁移到 expect/reason。
  [#16461](https://github.com/rust-lang/cargo/pull/16461)
- 为 libcargo 支持仅内存中的 `Manifest`
  [#16409](https://github.com/rust-lang/cargo/pull/16409)
- cargo-test-support：运行测试时使用测试名作为目录。
  [#16121](https://github.com/rust-lang/cargo/pull/16121)
- test：使用更大的默认终端宽度。
  [#16403](https://github.com/rust-lang/cargo/pull/16403)
  [#16391](https://github.com/rust-lang/cargo/pull/16391)
- test：为树外 build-dir 调整输出。
  [#16343](https://github.com/rust-lang/cargo/pull/16343)
- test：更新到 `proc_macro::tracked::path`。
  [#16380](https://github.com/rust-lang/cargo/pull/16380)
- test：移除未使用的构建脚本。
  [#16344](https://github.com/rust-lang/cargo/pull/16344)
- 更新依赖。
  [#16379](https://github.com/rust-lang/cargo/pull/16379)
  [#16381](https://github.com/rust-lang/cargo/pull/16381)
  [#16460](https://github.com/rust-lang/cargo/pull/16460)
  [#16457](https://github.com/rust-lang/cargo/pull/16457)
  [#16454](https://github.com/rust-lang/cargo/pull/16454)
  [#16507](https://github.com/rust-lang/cargo/pull/16507)

## Cargo 1.93 (2026-01-22)
[344c4567...rust-1.93.0](https://github.com/rust-lang/cargo/compare/344c4567...rust-1.93.0)

### 新增

- 根据 profile 设置，在构建脚本中启用 `CARGO_CFG_DEBUG_ASSERTIONS` 环境变量。
  [#16160](https://github.com/rust-lang/cargo/pull/16160)
- 添加对 Bash 中补全 `--config` 值的支持
  [#16245](https://github.com/rust-lang/cargo/pull/16245)
- cargo-clean：添加 `--workspace` 标志以清理工作空间成员的产物。
  [#16263](https://github.com/rust-lang/cargo/pull/16263)
- cargo-tree：支持 `--format` 变量的长形式
  [#16204](https://github.com/rust-lang/cargo/pull/16204)

### 变更

- ❗️ 即使未设置 `build.build-dir` 配置，`cargo publish` 也不再将 `.crate` 压缩包
  保留为最终构建产物。
  [#15915](https://github.com/rust-lang/cargo/pull/15915)
- 将更多诊断格式迁移到类似 rustc 的风格（annotate-snippets 风格）
  [#16143](https://github.com/rust-lang/cargo/pull/16143)
- 在 Cargo 清单中看到未使用字段时，指出该键属于 Cargo 配置。
  [#16256](https://github.com/rust-lang/cargo/pull/16256)
- 更新或创建 lockfile 失败时，提供更清晰的上下文与建议的
  用户操作以帮助解决。
  [#16233](https://github.com/rust-lang/cargo/pull/16233)
  [#16227](https://github.com/rust-lang/cargo/pull/16227)
- 当清单中将 GitHub pull request URL 用作依赖时，发出有帮助的错误信息。
  [#16207](https://github.com/rust-lang/cargo/pull/16207)
- 对 `check` 构建避免不必要的产物目录锁定。
  [#16230](https://github.com/rust-lang/cargo/pull/16230)
  [#16299](https://github.com/rust-lang/cargo/pull/16299)
  [#16307](https://github.com/rust-lang/cargo/pull/16307)
  [#16385](https://github.com/rust-lang/cargo/pull/16385)
  [#16386](https://github.com/rust-lang/cargo/pull/16386)
- 在 CLI 帮助文本中称为命令，而非子命令。
  [#16226](https://github.com/rust-lang/cargo/pull/16226)
- cargo-install：Cargo 曾将 `install.root` 中无尾部斜杠的相对路径
  视为相对于当前工作目录的路径。此情况
  现将收到弃用警告。这是疏忽，将来会改为
  像其他配置字段一样相对于配置文件的路径。
  [#16125](https://github.com/rust-lang/cargo/pull/16125)
- cargo-package：对不可发布到 crates.io 的包抑制缺失元数据警告
  [#16241](https://github.com/rust-lang/cargo/pull/16241)
- cargo-publish：同时指定 `package.publish` 与 `--index` 时发出警告
  [#16268](https://github.com/rust-lang/cargo/pull/16268)
- cargo-run：在帮助文本中说明如何转义参数以便字面
  转发给底层程序
  [#16225](https://github.com/rust-lang/cargo/pull/16225)

### 修复

- Zsh shell 补全变量不再泄漏到用户环境
  [#16144](https://github.com/rust-lang/cargo/pull/16144)
- 修复 Cargo 在 Windows 上生成带无效尾部反斜杠的 dep-info 文件。
  [#16223](https://github.com/rust-lang/cargo/pull/16223)
- 修复来自 `--config` CLI 的不可合并列表被环境变量覆盖。
  [#16220](https://github.com/rust-lang/cargo/pull/16220)
- 修复来自 `--config` CLI 的嵌套不可合并列表被与其他配置合并。
  [#16219](https://github.com/rust-lang/cargo/pull/16219)
- Cargo 现会在解包 `.crate` 源压缩包后，更新
  `cargo package` 生成文件的 mtime。
  这可确保文件不会有过旧的 mtime，以免某些 zip 工具无法处理。
  [#16250](https://github.com/rust-lang/cargo/pull/16250)
- 平移 `cargo check` 产物（.rmeta 文件）的 mtime。
  这修复了 rustc 增量编译跳过不必要的 rmeta 生成
  却未更新已有 rmeta 文件 mtime 的回归。
  [#16262](https://github.com/rust-lang/cargo/pull/16262)
- cargo-doc：仅清理所请求目标的已生成文档目录。
  此前当 rustc 版本不匹配时，Cargo 会移除所有已生成的文档
  目录，包括不属于本次构建的目标平台。
  [#16331](https://github.com/rust-lang/cargo/pull/16331)
- cargo-install：修复 crate 名校验中的越界错误
  [#16314](https://github.com/rust-lang/cargo/pull/16314)
- cargo-package：压缩包中生成的文件应有确定性时间戳。
  [#16242](https://github.com/rust-lang/cargo/pull/16242)
- cargo-package：通过 `CACHEDIR.TAG` 将 `target/package` 目录排除在备份之外。
  [#16272](https://github.com/rust-lang/cargo/pull/16272)
- cargo-vendor：修复 Windows 上由 `fs::rename` 回退导致的 panic。
  [#16214](https://github.com/rust-lang/cargo/pull/16214)

### 仅 Nightly

- 🔥 `-Zrustc-unicode` 在 Cargo 的错误信息中启用 `rustc` 的 unicode 错误格式。
  [#16243](https://github.com/rust-lang/cargo/pull/16243)
- 🔥 `-Zrustdoc-mergeable-info` 利用 rustdoc 的可合并 crate 信息，使
  `cargo doc` 能合并来自不同输出目录的跨 crate 信息（如搜索索引、源
  文件索引），并并行运行 `rustdoc`。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#rustdoc-mergeable-info)
  [#16309](https://github.com/rust-lang/cargo/pull/16309)
- 🔥 `cargo generate-lockfile` 现有不稳定的 `--publish-time` 标志，
  包解析将不考虑任何晚于指定时间的包。
  _在 registry 索引开始包含 `pubtime` 字段之前，这还没什么用。_
  [#16265](https://github.com/rust-lang/cargo/pull/16265)
- `build-plan`：完全移除不稳定功能 `build-plan`。
  Cargo 团队期待其他替代方案，如
  [plumbing 命令](https://github.com/crate-ci/cargo-plumbing)、
  [`--unit-graph](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#unit-graph)、
  以及 [结构化日志](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#build-analysis)
  来填补这一空缺。
  [#16212](https://github.com/rust-lang/cargo/pull/16212)
- `native-completions`：将 host-tuple 放在实际 tuple 之前
  [#16327](https://github.com/rust-lang/cargo/pull/16327)
- `native-completions`：在 `cargo tree --target` 候选中包含 `all`
  [#16322](https://github.com/rust-lang/cargo/pull/16322)
- `native-completions`：不要用括号包裹补全项帮助
  [#16215](https://github.com/rust-lang/cargo/pull/16215)
- `native-completions`：为 `cargo tree` 添加更多原生补全
  [#16296](https://github.com/rust-lang/cargo/pull/16296)
- `native-completions`：在各种命令上补全 `--package`
  [#16210](https://github.com/rust-lang/cargo/pull/16210)
- `update-breaking`：对不匹配的包说明符配合 --breaking 时静默失败
  [#16276](https://github.com/rust-lang/cargo/pull/16276)
- `-Zbindeps`：不将产物依赖传播到 proc macro 或构建依赖
  [#15788](https://github.com/rust-lang/cargo/pull/15788)
- `-Zbuild-analysis`：使用基于 JSONL 的日志基础设施发出计时信息日志。
  日志存储在 `~/.cargo/log/` 中，每次 cargo 调用有唯一文件。
  [#16150](https://github.com/rust-lang/cargo/pull/16150)
  [#16179](https://github.com/rust-lang/cargo/pull/16179)
  [#16303](https://github.com/rust-lang/cargo/pull/16303)
  [#16337](https://github.com/rust-lang/cargo/pull/16337)
- `-Zbuild-analysis`：发出重建原因日志条目。
  [#16203](https://github.com/rust-lang/cargo/pull/16203)
- `-Zbuild-build`：为 LTO 添加测试
  [#16277](https://github.com/rust-lang/cargo/pull/16277)
- `-Zbuild-dir-new-layout`：更好地区分旧/新布局
  [#16304](https://github.com/rust-lang/cargo/pull/16304)
- `-Zbuild-dir-new-layout`：用新布局清理主机构建
  [#16300](https://github.com/rust-lang/cargo/pull/16300)
- `-Zbuild-dir-new-layout`：在新布局中将 examples 放在其单元目录中
  [#16335](https://github.com/rust-lang/cargo/pull/16335)
- `-Zcargo-lints`：显示 lint 错误编号
  [#16320](https://github.com/rust-lang/cargo/pull/16320)
  [#16324](https://github.com/rust-lang/cargo/pull/16324)
- `-Zconfig-include`：允许使用 `optional = true` 以静默跳过
  缺失的配置文件。
  [#16103](https://github.com/rust-lang/cargo/pull/16103)
  [#16174](https://github.com/rust-lang/cargo/pull/16174)
  [#16180](https://github.com/rust-lang/cargo/pull/16180)
- `-Zconfig-include`：禁止在 `include.path` 中使用 glob 与模板语法
  [#16285](https://github.com/rust-lang/cargo/pull/16285)
- `-Zconfig-include`：移除单字符串简写支持
  [#16298](https://github.com/rust-lang/cargo/pull/16298)
- `-Zgit`：为 Git CLI 后端（`net.git-fetch-with-cli`）支持浅层 fetch
  [#16156](https://github.com/rust-lang/cargo/pull/16156)
- `-Zgit`：添加更多 git fetch-index 后端互操作测试
  [#16162](https://github.com/rust-lang/cargo/pull/16162)
- `-Zscript`：从 rustc 的测试套件更新脚本测试
  [#16169](https://github.com/rust-lang/cargo/pull/16169)
  [#16334](https://github.com/rust-lang/cargo/pull/16334)
- `-Zscript`：对 workspace-path-hash 回退到非规范路径。
  这可确保无法规范化的脚本路径（如 `memfd`）
  仍能工作。
  [#16248](https://github.com/rust-lang/cargo/pull/16248)
- `-Zwarnings`：build.warnings=deny 不应阻塞硬警告
  [#16213](https://github.com/rust-lang/cargo/pull/16213)


### 文档

- 将 `compile-time-deps` 移出已稳定章节
  [#16211](https://github.com/rust-lang/cargo/pull/16211)
- 将 `DEP_NAME_KEY` 重命名为 `DEP_LINKS_KEY`，使与
  `package.links` 字段的关联更清晰
  [#16205](https://github.com/rust-lang/cargo/pull/16205)
- 澄清 `cargo yank` 仅影响 Cargo 的依赖解析，
  不影响 crate 可用性
  [#16274](https://github.com/rust-lang/cargo/pull/16274)
- 在构建性能指南中，建议替代开发 profile 时链接到相关 issue。
  [#16275](https://github.com/rust-lang/cargo/pull/16275)
- cargo-metadata：记录 `-filter-platform` 也支持字面量 `"host-tuple"`。
  [#16312](https://github.com/rust-lang/cargo/pull/16312)
- contrib：链接到 rustc 诊断风格指南
  [#16216](https://github.com/rust-lang/cargo/pull/16216)
- resolver：修复伪代码中的编译错误
  [#16333](https://github.com/rust-lang/cargo/pull/16333)

### 内部

- 使在 NFS 挂载上禁用锁定成为显式行为
  [#16177](https://github.com/rust-lang/cargo/pull/16177)
- 将 ConfigValue 与配置 schema 提取到各自独立的模块
  [#16222](https://github.com/rust-lang/cargo/pull/16222)
  [#16195](https://github.com/rust-lang/cargo/pull/16195)
- 将反序列化校验逻辑嵌入 `ProgressConfig`
  [#16194](https://github.com/rust-lang/cargo/pull/16194)
- 分离 Cargo 计时数据收集与展示
  [#16282](https://github.com/rust-lang/cargo/pull/16282)
- cargo-util-schemas：为 inheritableField 添加 into_value 工具函数
  [#16234](https://github.com/rust-lang/cargo/pull/16234)
- ci：添加 typos/spellcheck CI 任务
  [#16122](https://github.com/rust-lang/cargo/pull/16122)
- ci：在更多目标上运行 clippy CI
  [#16340](https://github.com/rust-lang/cargo/pull/16340)
- mdman：修复 mdman 错误剥离 `<p>` 标签的问题
  [#16158](https://github.com/rust-lang/cargo/pull/16158)
  [#16172](https://github.com/rust-lang/cargo/pull/16172)
- test：重新启用 Windows 保留名测试，因其已不再 flaky
  [#16287](https://github.com/rust-lang/cargo/pull/16287)
- test：移除遗留的 tmpdir 支持
  [#16342](https://github.com/rust-lang/cargo/pull/16342)
- 更新到 mdbook 0.5。
  [#16292](https://github.com/rust-lang/cargo/pull/16292)
- 更新依赖。
  [#16137](https://github.com/rust-lang/cargo/pull/16137)
  [#16140](https://github.com/rust-lang/cargo/pull/16140)
  [#16178](https://github.com/rust-lang/cargo/pull/16178)
  [#16186](https://github.com/rust-lang/cargo/pull/16186)
  [#16190](https://github.com/rust-lang/cargo/pull/16190)
  [#16200](https://github.com/rust-lang/cargo/pull/16200)
  [#16224](https://github.com/rust-lang/cargo/pull/16224)
  [#16316](https://github.com/rust-lang/cargo/pull/16316)
  [#16318](https://github.com/rust-lang/cargo/pull/16318)

## Cargo 1.92 (2025-12-11)
[24bb93c3...rust-1.92.0](https://github.com/rust-lang/cargo/compare/24bb93c3...rust-1.92.0)

### 新增

- 将 Ghostty 添加为终端集成（OSC 9;4）的受支持终端
  [#15977](https://github.com/rust-lang/cargo/pull/15977)
- 在 `net.git-fetch-with-cli` 路径中为 `git fetch` 失败添加重试
  [#16016](https://github.com/rust-lang/cargo/pull/16016)

### 变更

- 将部分诊断格式迁移到类似 rustc 的风格（annotate-snippets 风格）
  [#15943](https://github.com/rust-lang/cargo/pull/15943)
  [#15945](https://github.com/rust-lang/cargo/pull/15945)
  [#16019](https://github.com/rust-lang/cargo/pull/16019)
  [#16035](https://github.com/rust-lang/cargo/pull/16035)
  [#16066](https://github.com/rust-lang/cargo/pull/16066)
  [#16113](https://github.com/rust-lang/cargo/pull/16113)
  [#16126](https://github.com/rust-lang/cargo/pull/16126)
- 来自编译诊断的建议 `cargo fix` 命令现更准确。
  [#16127](https://github.com/rust-lang/cargo/pull/16127)
- 截断进度时优先使用 unicode 省略号
  [#15955](https://github.com/rust-lang/cargo/pull/15955)
- 消除最后三种 “did you mean” 警告措辞
  [#15356](https://github.com/rust-lang/cargo/pull/15356)
- 澄清在 `patch` 中使用 `features` 或 `default-features` 的警告
  [#15953](https://github.com/rust-lang/cargo/pull/15953)
- 配置解析错误现显示带数组索引的更精确键路径
  [#16004](https://github.com/rust-lang/cargo/pull/16004)
- 改进 `rust-version` 不兼容诊断的错误信息
  [#16021](https://github.com/rust-lang/cargo/pull/16021)
- cargo-add：为工作空间依赖报告缺失源错误
  [#16063](https://github.com/rust-lang/cargo/pull/16063)
- cargo-info：建议更通用的 `cargo tree` 命令
  [#15954](https://github.com/rust-lang/cargo/pull/15954)
- cargo-publish：将“等待时按 ctrl-c”一行改为帮助信息
  [#15942](https://github.com/rust-lang/cargo/pull/15942)
- cargo-publish：软弃用 `--token` 选项
  [#16046](https://github.com/rust-lang/cargo/pull/16046)

### 修复

### 仅 Nightly

- 🔥 `immediate-abort`：添加 `panic=immediate-abort` 支持
  [#16041](https://github.com/rust-lang/cargo/pull/16041)
  [#16054](https://github.com/rust-lang/cargo/pull/16054)
- `-Zbuild-dir-new-layout`：重组 build-dir 布局
  [#15947](https://github.com/rust-lang/cargo/pull/15947)
- `-Zbuild-std`：测试从 panic_immediate_abort 迁出
  [#16006](https://github.com/rust-lang/cargo/pull/16006)
- `-Zcargo-lints`：添加关于全局使用 `hint-mostly-unused` 的 lint
  [#15995](https://github.com/rust-lang/cargo/pull/15995)
- `-Zpublic-dependency`：`cargo add` 在选择版本时现会考虑公共依赖
  [#15966](https://github.com/rust-lang/cargo/pull/15966)
- `-Zpublic-dependency`：将显示公共依赖的 `cargo tree` 从 `--depth public` 改为 `--edges public`
  [#16081](https://github.com/rust-lang/cargo/pull/16081)
- `-Zpublic-dependency`：改进 public-in-private 清单错误
  [#16002](https://github.com/rust-lang/cargo/pull/16002)
  [#16075](https://github.com/rust-lang/cargo/pull/16075)
- `-Zscript`：改进 frontmatter 解析错误质量
  [#15972](https://github.com/rust-lang/cargo/pull/15972)
  [#15939](https://github.com/rust-lang/cargo/pull/15939)
  [#15952](https://github.com/rust-lang/cargo/pull/15952)
- `-Zscript`：围栏后仅允许水平空白
  [#15975](https://github.com/rust-lang/cargo/pull/15975)
- `-Zscript`：覆盖 cargo 脚本的 arg0
  [#16027](https://github.com/rust-lang/cargo/pull/16027)
- `-Zscript`：调整 cargo 脚本的 build-dir / target-dir
  [#16086](https://github.com/rust-lang/cargo/pull/16086)
- `-Zscript`：移除严格必要之外的名称清理（sanitization）
  [#16120](https://github.com/rust-lang/cargo/pull/16120)
- `-Zscript`：将 cargo 脚本 lockfile 存储在 build-dir 中
  [#16087](https://github.com/rust-lang/cargo/pull/16087)
- `-Zscript`：使用 build-dir 模板定义 cargo 脚本的 target-dir
  [#16073](https://github.com/rust-lang/cargo/pull/16073)
- `-Zscript`：阻止 Cargo 脚本中的非脚本字段
  [#16026](https://github.com/rust-lang/cargo/pull/16026)
- `-Zscript`：将 bin.name 默认设为 package.name
  [#16064](https://github.com/rust-lang/cargo/pull/16064)
- `multiple-build-scripts`：通过 `<script-name>_OUT_DIR` 访问各构建脚本的 `OUT_DIR`
  [#15891](https://github.com/rust-lang/cargo/pull/15891)
- `native-completions`：为 `--features` 标志添加补全
  [#15309](https://github.com/rust-lang/cargo/pull/15309)
- `native-completions`：优先显示本地 crate/feature 而非其他成员
  [#15956](https://github.com/rust-lang/cargo/pull/15956)
- `native-completions`：允许补全第三方子命令名
  [#15961](https://github.com/rust-lang/cargo/pull/15961)

### 文档

- 🎉 新增「优化构建性能」章节
  [#15924](https://github.com/rust-lang/cargo/pull/15924)
  [#15970](https://github.com/rust-lang/cargo/pull/15970)
  [#15991](https://github.com/rust-lang/cargo/pull/15991)
  [#16078](https://github.com/rust-lang/cargo/pull/16078)
  [#16085](https://github.com/rust-lang/cargo/pull/16085)
  [#16107](https://github.com/rust-lang/cargo/pull/16107)
  [#16108](https://github.com/rust-lang/cargo/pull/16108)
- 澄清源替换文档中 git 源与 git registry 的区别
  [#15974](https://github.com/rust-lang/cargo/pull/15974)
- 澄清 registry 索引文档中“省略 feature”的含义
  [#15957](https://github.com/rust-lang/cargo/pull/15957)
- 澄清 lockfile 在依赖解析中的作用
  [#15958](https://github.com/rust-lang/cargo/pull/15958)
- 澄清多重版本需求的行为
  [#15979](https://github.com/rust-lang/cargo/pull/15979)
- 澄清支持 `target.<cfg>.linker`
  [#16112](https://github.com/rust-lang/cargo/pull/16112)
- 解释 Cargo 配置反序列化内部机制
  [#16105](https://github.com/rust-lang/cargo/pull/16105)
  [#16094](https://github.com/rust-lang/cargo/pull/16094)
- contrib：将文档构建流程移至贡献者指南
  [#15854](https://github.com/rust-lang/cargo/pull/15854)
- SemVer：在 Rust 版本章节中推荐 `package.rust-version`
  [#15806](https://github.com/rust-lang/cargo/pull/15806)

### 内部

- 使 GlobalContext 实现 Sync
  [#15967](https://github.com/rust-lang/cargo/pull/15967)
- 集中管理 Cargo 控制台输出样式
  [#16124](https://github.com/rust-lang/cargo/pull/16124)
  [#16135](https://github.com/rust-lang/cargo/pull/16135)
- 将 `Layout` 重构为 `BuildDirLayout` 与 `ArtifactDirLayout`
  [#16092](https://github.com/rust-lang/cargo/pull/16092)
- cargo-test-support：添加 track_caller 以获知实际失败位置
  [#16069](https://github.com/rust-lang/cargo/pull/16069)
- cargo-test-support：添加更好的文件系统布局测试工具
  [#15874](https://github.com/rust-lang/cargo/pull/15874)
- cargo-util-schemas：迁入 lockfile schema
  [#15980](https://github.com/rust-lang/cargo/pull/15980)
  [#15990](https://github.com/rust-lang/cargo/pull/15990)
  [#16039](https://github.com/rust-lang/cargo/pull/16039)
- ci：在 fork 中跳过 check-version-bump ci 任务
  [#15959](https://github.com/rust-lang/cargo/pull/15959)
- config：对 `ConfigValue` 进行各种内部清理与重构
  [#16067](https://github.com/rust-lang/cargo/pull/16067)
  [#16084](https://github.com/rust-lang/cargo/pull/16084)
  [#16091](https://github.com/rust-lang/cargo/pull/16091)
  [#16100](https://github.com/rust-lang/cargo/pull/16100)
  [#16109](https://github.com/rust-lang/cargo/pull/16109)
- perf：以更少分配处理 JSON 消息
  [#16130](https://github.com/rust-lang/cargo/pull/16130)
- test：用空终止路径检测 Windows 保留名
  [#16052](https://github.com/rust-lang/cargo/pull/16052)
- test：不查找特定 ANSI 颜色
  [#16118](https://github.com/rust-lang/cargo/pull/16118)
- test：修复假定 `CARGO_CFG_TARGET_FAMILY` 为单值的测试
  [#16079](https://github.com/rust-lang/cargo/pull/16079)
- 更新依赖。
  [#15988](https://github.com/rust-lang/cargo/pull/15988)
  [#15984](https://github.com/rust-lang/cargo/pull/15984)
  [#15989](https://github.com/rust-lang/cargo/pull/15989)
  [#15992](https://github.com/rust-lang/cargo/pull/15992)
  [#15993](https://github.com/rust-lang/cargo/pull/15993)
  [#16009](https://github.com/rust-lang/cargo/pull/16009)
  [#16031](https://github.com/rust-lang/cargo/pull/16031)
  [#16034](https://github.com/rust-lang/cargo/pull/16034)

## Cargo 1.91 (2025-10-30)
[840b83a1...rust-1.91.0](https://github.com/rust-lang/cargo/compare/840b83a1...rust-1.91.0)

### 新增

- 🎉 稳定 `build.build-dir`。
  该配置设置中间构建产物的存放目录。
  这些产物由 Cargo 与 rustc 在构建过程中生成。
  最终用户通常无需与之交互，且 `build-dir`
  内部布局是实现细节，可能在无通知的情况下变更。
  （[config 文档](https://doc.rust-lang.org/nightly/cargo/reference/config.html#buildbuild-dir)）
  （[构建缓存文档](https://doc.rust-lang.org/nightly/cargo/reference/build-cache.html)）
  [#15833](https://github.com/rust-lang/cargo/pull/15833)
  [#15840](https://github.com/rust-lang/cargo/pull/15840)
- `--target` 标志与 `build.target` 配置现可接受字面量
  `"host-tuple"` 字符串，内部会替换为主机
  机器的目标三元组。
  [#15838](https://github.com/rust-lang/cargo/pull/15838)
  [#16003](https://github.com/rust-lang/cargo/pull/16003)
  [#16032](https://github.com/rust-lang/cargo/pull/16032)

### 变更

- ❗️ 当设置了 `build.build-dir` 时，`cargo publish` 不再将 `.crate` 压缩包
  保留为最终构建产物。这些压缩包此前因疏忽被包含，
  现视为中间产物。
  若要将 `.crate` 压缩包作为最终产物，请使用 `cargo package`。
  在未来版本中，此变更将不论是否设置 `build.build-dir` 均适用。
  [#15910](https://github.com/rust-lang/cargo/pull/15910)
- 调整 Cargo 信息以匹配 rustc 诊断风格
  [#15928](https://github.com/rust-lang/cargo/pull/15928)
- 对无效的 `cargo-features = []` 给出更有帮助的错误
  [#15781](https://github.com/rust-lang/cargo/pull/15781)
- 发出 lint 与警告时不在第一个错误处停止
  [#15889](https://github.com/rust-lang/cargo/pull/15889)
- 在错误信息中显示错误的清单路径
  [#15896](https://github.com/rust-lang/cargo/pull/15896)
- 对无效的布尔依赖建议工作空间提示
  [#15507](https://github.com/rust-lang/cargo/pull/15507)
- cargo-package：打包校验期间始终复用工作空间的 target-dir。
  此前 Cargo 会在解包后的源码内创建新的独立目标目录。
  [#15783](https://github.com/rust-lang/cargo/pull/15783)
- cargo-publish：为发布失败错误信息添加更多上下文
  [#15879](https://github.com/rust-lang/cargo/pull/15879)

### 修复

### 仅 Nightly

- 🔥 `-Zsection-timings` 扩展 `cargo build --timings` 的输出。它让
  rustc 产出各个编译阶段的计时，然后显示在
  计时 HTML/JSON 输出中。
  （[文档](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#section-timings)）
  [#15780](https://github.com/rust-lang/cargo/pull/15780)
  [#15923](https://github.com/rust-lang/cargo/pull/15923)
- 🔥 `-Zbuild-dir-new-layout` 启用新的 build-dir 文件系统布局，
  可为缓存与锁定方面的改进扫清障碍。
  （[文档](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#build-dir-new-layout)）
  （[项目目标](https://rust-lang.github.io/rust-project-goals/2025h2/cargo-build-dir-layout.html)）
  [#15848](https://github.com/rust-lang/cargo/pull/15848)
- 🔥 `-Zbuild-analysis` 跨运行记录并持久化详细构建指标（计时、重建原因等），
  并提供查询历史构建的新命令。
  （[文档](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#build-analysis)）
  （[项目目标](https://rust-lang.github.io/rust-project-goals/2025h2/cargo-build-analysis.html)）
  [#15845](https://github.com/rust-lang/cargo/pull/15845)
- `multiple-build-scripts`：按正确顺序访问各构建脚本的 `OUT_DIR`
  [#15776](https://github.com/rust-lang/cargo/pull/15776)
- `-Zcargo-lints`：lint 系统基础设施改进
  [#15865](https://github.com/rust-lang/cargo/pull/15865)
- `-Zscript`：覆盖一些 frontmatter 边界情况
  [#15886](https://github.com/rust-lang/cargo/pull/15886)
- `-Zscript`：匹配 rustc 中的测试更新
  [#15878](https://github.com/rust-lang/cargo/pull/15878)
- `-Zscript`：将 frontmatter 测试改为端到端
  [#15899](https://github.com/rust-lang/cargo/pull/15899)
- `-Zscript`：对正确行号报告脚本清单错误
  [#15927](https://github.com/rust-lang/cargo/pull/15927)
- `-Zscript`：抽成独立模块
  [#15914](https://github.com/rust-lang/cargo/pull/15914)

### 文档

- 澄清 `cargo doc --no-deps` 是累积的，不会删除先前结果
  [#15800](https://github.com/rust-lang/cargo/pull/15800)
- 在文档与帮助文本中将 `--nocapture` 改为 `--no-capture`。
  [#15930](https://github.com/rust-lang/cargo/pull/15930)
- 说明 Cargo 如何获取 git 子模块
  [#15853](https://github.com/rust-lang/cargo/pull/15853)
  [#15860](https://github.com/rust-lang/cargo/pull/15860)
- 链接到 Plumbing 命令相关工作
  [#15821](https://github.com/rust-lang/cargo/pull/15821)
- 改用原生 mdbook 片段重定向
  [#15861](https://github.com/rust-lang/cargo/pull/15861)
- 重新排列 profiles 中的 `lto` 选项
  [#15841](https://github.com/rust-lang/cargo/pull/15841)
  [#15855](https://github.com/rust-lang/cargo/pull/15855)

### 内部

- 用标准库 flock 替换临时 flock 实现
  [#15935](https://github.com/rust-lang/cargo/pull/15935)
  [#15941](https://github.com/rust-lang/cargo/pull/15941)
- 为在更多地方生成 annotate-snippets `Report` 做准备
  [#15920](https://github.com/rust-lang/cargo/pull/15920)
  [#15926](https://github.com/rust-lang/cargo/pull/15926)
- test：避免硬编码目标规格 json
  [#15880](https://github.com/rust-lang/cargo/pull/15880)
- test：确保无论是否使用 rustup 行为一致
  [#15949](https://github.com/rust-lang/cargo/pull/15949)
- test：将更多凭证进程的预期结果改为快照
  [#15929](https://github.com/rust-lang/cargo/pull/15929)
- ci：添加 Arm64 Windows CI 任务
  [#15790](https://github.com/rust-lang/cargo/pull/15790)
- ci：从 CI 与测试中移除 x86_64-apple-darwin
  [#15831](https://github.com/rust-lang/cargo/pull/15831)
- 更新依赖。
  [#15795](https://github.com/rust-lang/cargo/pull/15795)
  [#15804](https://github.com/rust-lang/cargo/pull/15804)
  [#15815](https://github.com/rust-lang/cargo/pull/15815)
  [#15816](https://github.com/rust-lang/cargo/pull/15816)
  [#15819](https://github.com/rust-lang/cargo/pull/15819)
  [#15825](https://github.com/rust-lang/cargo/pull/15825)
  [#15832](https://github.com/rust-lang/cargo/pull/15832)
  [#15851](https://github.com/rust-lang/cargo/pull/15851)
  [#15898](https://github.com/rust-lang/cargo/pull/15898)
  [#15904](https://github.com/rust-lang/cargo/pull/15904)
  [#15909](https://github.com/rust-lang/cargo/pull/15909)
  [#15918](https://github.com/rust-lang/cargo/pull/15918)
  [#15950](https://github.com/rust-lang/cargo/pull/15950)

## Cargo 1.90 (2025-09-18)
[c24e1064...rust-1.90.0](https://github.com/rust-lang/cargo/compare/c24e1064...rust-1.90.0)

### 新增

- 🎉 稳定多包发布。
  这允许 cargo 在工作空间中发布多个 crate，即使它们
  有相互依赖。例如 `cargo publish --workspace` 或
  `cargo publish -p foo -p bar`。
  注意此时 `cargo publish` 仍非原子操作。若发布过程中出现
  服务端错误，工作空间会处于部分已发布状态。
  [#15636](https://github.com/rust-lang/cargo/pull/15636)
  [#15711](https://github.com/rust-lang/cargo/pull/15711)
- 添加用于代理 TLS 证书的 `http.proxy-cainfo` 配置。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#httpproxy-cainfo)
  [#15374](https://github.com/rust-lang/cargo/pull/15374)

### 变更

- cargo-package：使用 `gix` 将 Git 状态检查加速 10–20%。
  [#15534](https://github.com/rust-lang/cargo/pull/15534)
- 使计时图可随用户窗口缩放。
  [#15766](https://github.com/rust-lang/cargo/pull/15766)
- 当找不到 `name = "foo.rs"` 的构建目标时报告有效文件名
  [#15707](https://github.com/rust-lang/cargo/pull/15707)

### 修复

- cargo-credential-libsecret：为 FFI 提供正确大小的对象
  [#15767](https://github.com/rust-lang/cargo/pull/15767)
- cargo-publish：校验时在错误中包含清单路径
  [#15705](https://github.com/rust-lang/cargo/pull/15705)
- cargo-tree：修复 `no-proc-macro` 被后续 edges 覆盖。
  [#15764](https://github.com/rust-lang/cargo/pull/15764)

### 仅 Nightly

- 🔥 `multiple-build-scripts`：允许在包中拥有多个构建脚本。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#multiple-build-scripts)
  [#15630](https://github.com/rust-lang/cargo/pull/15630)
  [#15704](https://github.com/rust-lang/cargo/pull/15704)
- 🔥 `-Zprofile-hint-mostly-unused`：在 `Cargo.toml` 中添加 `[hints]` 表，
  以及 `hints.mostly-unused` 提示。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#profile-hint-mostly-unused-option)
  [#15673](https://github.com/rust-lang/cargo/pull/15673)
- `-Zfeature-unification`：实现按包的 feature 统一
  [#15684](https://github.com/rust-lang/cargo/pull/15684)
- `-Zsbom`：澄清 SBOM 中的包 ID 规格是完全限定的
  [#15731](https://github.com/rust-lang/cargo/pull/15731)

### 文档

### 内部

- build-rs：在工具链发布时自动发布
  [#15708](https://github.com/rust-lang/cargo/pull/15708)
- cargo-util-schemas：暴露 `IndexPackage`，即 Registry 索引中包的描述
  [#15770](https://github.com/rust-lang/cargo/pull/15770)
- ci：将 cargo-semver-checks 更新到 v0.42.0
  [#15730](https://github.com/rust-lang/cargo/pull/15730)
- perf：通过升级 toml 加速 TOML 解析
  [#15736](https://github.com/rust-lang/cargo/pull/15736)
  [#15779](https://github.com/rust-lang/cargo/pull/15779)
- test：改造 `cargo-test-support` 与 `testsuite` 以用 `CARGO_BIN_EXE_*` 指向 Cargo
  [#15692](https://github.com/rust-lang/cargo/pull/15692)
- test：使用不同 lint 模拟诊断重复
  [#15713](https://github.com/rust-lang/cargo/pull/15713)
  [#15717](https://github.com/rust-lang/cargo/pull/15717)
- test：将配置测试改为使用快照
  [#15729](https://github.com/rust-lang/cargo/pull/15729)
- test：从目标规格中移除不必要的 target-c-int-width
  [#15759](https://github.com/rust-lang/cargo/pull/15759)
- test：将依赖进程间阻塞行为的 cachelock 测试标为 AIX 上不支持。
  [#15734](https://github.com/rust-lang/cargo/pull/15734)
- 在 cargo-as-a-library 中暴露产物依赖 getter
  [#15753](https://github.com/rust-lang/cargo/pull/15753)
- 允许使用带 gix 的 reqwest 后端的 Cargo-as-a-library
  [#15653](https://github.com/rust-lang/cargo/pull/15653)
- 更新到 Rust 2024
  [#15732](https://github.com/rust-lang/cargo/pull/15732)
- 更新依赖。
  [#15706](https://github.com/rust-lang/cargo/pull/15706)
  [#15709](https://github.com/rust-lang/cargo/pull/15709)
  [#15722](https://github.com/rust-lang/cargo/pull/15722)

## Cargo 1.89 (2025-08-07)
[873a0649...rust-1.89.0](https://github.com/rust-lang/cargo/compare/873a0649...rust-1.89.0)

### 新增

- 为 SSH known hosts 匹配添加 `*` 与 `?` 模式支持。
  [#15508](https://github.com/rust-lang/cargo/pull/15508)
- 稳定 doctest-xcompile。交叉编译到与主机不同的目标时，doctest 现会像其他测试一样自动运行。
  [#15462](https://github.com/rust-lang/cargo/pull/15462)

### 变更

- ❗️ `cargo fix` 与 `cargo clippy --fix` 现默认仅在默认 Cargo
  目标上运行，与 `cargo check` 行为一致。若要在所有
  Cargo 目标上运行，请使用 `--all-targets` 标志。此变更使行为
  与其他命令对齐。`--edition` 与 `--edition-idioms` 等
  edition 标志默认仍隐含 `--all-targets`。
  [#15192](https://github.com/rust-lang/cargo/pull/15192)
- 与 registry 通信时，对 HTTP 429 响应尊重 `Retry-After` 头。
  [#15463](https://github.com/rust-lang/cargo/pull/15463)
- 改进以 `v` 为前缀的 `CRATE[@<VER>]` 参数的错误信息。
  [#15484](https://github.com/rust-lang/cargo/pull/15484)
- 改进含无效包名字符的 `CRATE[@<VER>]` 参数的
  错误信息。
  [#15441](https://github.com/rust-lang/cargo/pull/15441)
- cargo-add：建议名称相近的 feature
  [#15438](https://github.com/rust-lang/cargo/pull/15438)

### 修复

- 修复 `CacheState::lock` 中的潜在死锁
  [#15698](https://github.com/rust-lang/cargo/pull/15698)
  [#15699](https://github.com/rust-lang/cargo/pull/15699)
- 修复 `cargo fix` 中 `--manifest-path` 参数被忽略
  [#15633](https://github.com/rust-lang/cargo/pull/15633)
- 发布时，不要在未说明后果的情况下让人按 ctrl-c。
  [#15632](https://github.com/rust-lang/cargo/pull/15632)
- 在 shell 补全中补上缺失的 `--offline`。
  [#15623](https://github.com/rust-lang/cargo/pull/15623)
- cargo-credential-libsecret：仅加载一次 libsecret
  [#15295](https://github.com/rust-lang/cargo/pull/15295)
- 无法找到用于重建检测的文件 mtime 时，报告明确原因，而非 “stale; unknown reason”。
  [#15617](https://github.com/rust-lang/cargo/pull/15617)
- 修复 cargo add 覆盖符号链接的 Cargo.toml 文件
  [#15281](https://github.com/rust-lang/cargo/pull/15281)
- Vendor 带 .rej/.orig 后缀的文件
  [#15569](https://github.com/rust-lang/cargo/pull/15569)
- 对 registry 源使用直接解压进行 vendor。这应确保 vendored 文件始终与原始文件匹配。
  [#15514](https://github.com/rust-lang/cargo/pull/15514)
- 在网络重试信息中，最后一次重试用单数 “try”。
  [#15328](https://github.com/rust-lang/cargo/pull/15328)

### 仅 Nightly

- 🔥 `-Zno-embed-metadata`：这让 Cargo 向编译器传递 `-Zembed-metadata=no`
  标志，指示其不要在 rlib
  与 dylib 产物中嵌入元数据。此时元数据仅存储在
  `.rmeta` 文件中。
  （[文档](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#no-embed-metadata)）
  [#15378](https://github.com/rust-lang/cargo/pull/15378)
- 🔥 将 rustc `-Zhint-mostly-unused` 标志贯通为 profile 选项
  （[文档](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#profile-hint-mostly-unused-option)）
  [#15643](https://github.com/rust-lang/cargo/pull/15643)
- 添加 “future” edition
  [#15595](https://github.com/rust-lang/cargo/pull/15595)
- 添加 `-Zfix-edition`
  [#15596](https://github.com/rust-lang/cargo/pull/15596)
- 为 `cargo build` 添加永久不稳定的 `--compile-time-deps` 选项
  [#15674](https://github.com/rust-lang/cargo/pull/15674)
- `-Zscript`：使 cargo 脚本忽略工作空间。
  [#15496](https://github.com/rust-lang/cargo/pull/15496)
- `-Zpackage-workspace`：若有版本则保留 dev-dependencies。
  [#15470](https://github.com/rust-lang/cargo/pull/15470)
- 为 `cargo remove <TAB>` 添加自定义补全器
  [#15662](https://github.com/rust-lang/cargo/pull/15662)
- 为 `-Zpackage-workspace` 稳定化准备的测试改进
  [#15628](https://github.com/rust-lang/cargo/pull/15628)
- 允许用 `-Zpackage-workspace` 打包自循环
  [#15626](https://github.com/rust-lang/cargo/pull/15626)
- 使用 trim-paths 时，将所有路径重映射到 `build.build-dir`
  [#15614](https://github.com/rust-lang/cargo/pull/15614)
- 为 windows-msvc 启用更多 trim-paths 测试
  [#15621](https://github.com/rust-lang/cargo/pull/15621)
- 通过向 rustdoc-depinfo 跟踪传递 `toolchain-shared-resources` 以获取文档样式，修复文档重建检测
  [#15605](https://github.com/rust-lang/cargo/pull/15605)
- 修复 `-Zscript` frontmatter 解析器中的多个 bug
  [#15573](https://github.com/rust-lang/cargo/pull/15573)
- 移除 `-Zscript` 对 rustc frontmatter 支持的变通方案
  [#15570](https://github.com/rust-lang/cargo/pull/15570)
- 允许配置任意 codegen 后端
  [#15562](https://github.com/rust-lang/cargo/pull/15562)
- 对 `-Zpackage-workspace` 发布整个工作空间时跳过 `publish=false` 的包。
  [#15525](https://github.com/rust-lang/cargo/pull/15525)
- 更新使用 native-completions 的说明
  [#15480](https://github.com/rust-lang/cargo/pull/15480)
- 对 `-Zpackage-workspace` 在不需要时跳过 registry 检查。
  [#15629](https://github.com/rust-lang/cargo/pull/15629)

### 文档

- 澄清哪些命令需要什么，并移除令人困惑的示例
  [#15457](https://github.com/rust-lang/cargo/pull/15457)
- 更新指纹脚注
  [#15478](https://github.com/rust-lang/cargo/pull/15478)
- home：更新弃用移除的版本通知
  [#15511](https://github.com/rust-lang/cargo/pull/15511)
- docs(contrib)：将 clap URL 改为 docs.rs/clap
  [#15682](https://github.com/rust-lang/cargo/pull/15682)
- 更新贡献文档中的链接
  [#15659](https://github.com/rust-lang/cargo/pull/15659)
- docs：澄清并非所有命令都可用 `--all-features`
  [#15572](https://github.com/rust-lang/cargo/pull/15572)
- docs(README)：修复 Cargo book 中指向更新日志的链接
  [#15597](https://github.com/rust-lang/cargo/pull/15597)

### 内部

- 重构 FeatureResolver::deps 中的产物依赖
  [#15492](https://github.com/rust-lang/cargo/pull/15492)
- 为 rustc 调用添加 tracing span
  [#15464](https://github.com/rust-lang/cargo/pull/15464)
- ci：迁移 renovate 配置
  [#15501](https://github.com/rust-lang/cargo/pull/15501)
- ci：要求 schema 任务通过
  [#15504](https://github.com/rust-lang/cargo/pull/15504)
- test：移除未使用的 nightly 要求
  [#15498](https://github.com/rust-lang/cargo/pull/15498)
- 更新依赖。
  [#15456](https://github.com/rust-lang/cargo/pull/15456)
- refactor：在 IndexPackage 中用 Cow 替换 InternedString
  [#15559](https://github.com/rust-lang/cargo/pull/15559)
- 使用 `Not::not` 而非自定义的 `is_false` 函数
  [#15645](https://github.com/rust-lang/cargo/pull/15645)
- fix：使 UI 测试一致地处理超链接
  [#15640](https://github.com/rust-lang/cargo/pull/15640)
- 更新依赖
  [#15635](https://github.com/rust-lang/cargo/pull/15635)
  [#15557](https://github.com/rust-lang/cargo/pull/15557)
- refactor：清理 `clippy::perf` lint 警告
  [#15631](https://github.com/rust-lang/cargo/pull/15631)
- chore(deps)：将 alpine docker 标签更新到 v3.22
  [#15616](https://github.com/rust-lang/cargo/pull/15616)
- chore：移除 PR 模板与内联指南中的 HTML 注释
  [#15613](https://github.com/rust-lang/cargo/pull/15613)
- 添加 .git-blame-ignore-revs
  [#15612](https://github.com/rust-lang/cargo/pull/15612)
- refactor：清理 `CompileMode`
  [#15608](https://github.com/rust-lang/cargo/pull/15608)
- refactor：将 “global” 模式从 CompileMode 中分离
  [#15601](https://github.com/rust-lang/cargo/pull/15601)
- chore：升级 schemars
  [#15602](https://github.com/rust-lang/cargo/pull/15602)
- 更新 gix 与 socket2
  [#15600](https://github.com/rust-lang/cargo/pull/15600)
- chore(toml)：除非必要，禁用 `toml` 的默认功能，以缩短 cargo-util-schemas 构建时间
  [#15598](https://github.com/rust-lang/cargo/pull/15598)
- chore(gh)：添加 new-lint issue 模板
  [#15575](https://github.com/rust-lang/cargo/pull/15575)
- 修复 cargo/core/compiler/fingerprint/mod.rs 的注释
  [#15565](https://github.com/rust-lang/cargo/pull/15565)

## Cargo 1.88 (2025-06-26)
[a6c604d1...rust-1.88.0](https://github.com/rust-lang/cargo/compare/a6c604d1...rust-1.88.0)

### 新增

- 🎉 稳定化全局缓存的自动垃圾回收。

  构建时，Cargo 会下载并缓存作为依赖所需的 crate。
  历史上，这些下载的文件从不会被清理，导致
  Cargo 主目录中的磁盘占用无上限地增长。在本版本中，
  Cargo 引入了垃圾回收机制，以自动清理旧
  文件（例如 .crate 文件）。Cargo 会移除从网络下载、
  且超过 3 个月未访问的文件，以及从本地系统获取、
  且超过 1 个月未访问的文件。请注意，若以离线方式运行
  （使用 `--offline` 或 `--frozen`），则不会执行此自动垃圾回收。

  Cargo 1.78 及更新版本会跟踪此垃圾回收所需的访问信息。
  若你经常使用早于 1.78 的 Cargo 版本，
  同时还运行当前版本的 Cargo，并且预期有一些
  crate 仅由较旧版本的 Cargo 访问，又不希望
  大约每 3 个月重新下载这些 crate，则可能希望在
  Cargo 配置中设置 `cache.auto-clean-frequency = "never"`。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#cache))
  [#14287](https://github.com/rust-lang/cargo/pull/14287)
- 允许在 Cargo.toml 与配置中将布尔字面量用作 cfg 谓词。
  例如，`[target.'cfg(not(false))'.dependencies]` 是有效的 cfg 谓词。
  ([RFC 3695](https://github.com/rust-lang/rfcs/pull/3695))
  [#14649](https://github.com/rust-lang/cargo/pull/14649)

### 变更

- 不为 `CARGO` 环境变量规范化可执行文件路径。
  [#15355](https://github.com/rust-lang/cargo/pull/15355)
- 将目标和包名称打印为文件超链接格式。
  [#15405](https://github.com/rust-lang/cargo/pull/15405)
- 确保 `OUT_DIR` 内的库搜索路径优先于外部路径。
  [#15221](https://github.com/rust-lang/cargo/pull/15221)
- 在缺少 feature 时建议外观相似的 feature 名称。
  [#15454](https://github.com/rust-lang/cargo/pull/15454)
- 对 `.crate` tar 包的 gzip（解）压缩使用 `zlib-rs`。
  [#15417](https://github.com/rust-lang/cargo/pull/15417)

### 修复

- build-rs：更正 `CARGO_CFG_FEATURE` 的名称
  [#15420](https://github.com/rust-lang/cargo/pull/15420)
- cargo-tree：使输出更确定
  [#15369](https://github.com/rust-lang/cargo/pull/15369)
- cargo-package：当脏检查失败时不要使整个命令失败，
  因为 git status 检查主要是信息性的。
  [#15416](https://github.com/rust-lang/cargo/pull/15416)
  [#15419](https://github.com/rust-lang/cargo/pull/15419)
- 修复 `cargo rustc --bin` 在未知 bin 名称上 panic
  [#15515](https://github.com/rust-lang/cargo/pull/15515)
  [#15497](https://github.com/rust-lang/cargo/pull/15497)

### 仅 Nightly

- 🔥 `-Zrustdoc-depinfo`：一个新的不稳定标志，利用 rustdoc 的 dep-info
  文件来判断文档是否需要重新生成。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#rustdoc-depinfo))
  [#15359](https://github.com/rust-lang/cargo/pull/15359)
  [#15371](https://github.com/rust-lang/cargo/pull/15371)
- `build-dir`：为 build-dir 模板中未匹配的括号添加校验 
  [#15414](https://github.com/rust-lang/cargo/pull/15414)
- `build-dir`：改进 build-dir 模板变量无效时的错误消息 
  [#15418](https://github.com/rust-lang/cargo/pull/15418)
- `build-dir`：在 cargo metadata 输出中添加 `build_directory` 字段 
  [#15377](https://github.com/rust-lang/cargo/pull/15377)
- `build-dir`：为 `workspace-path-hash` 添加符号链接解析 
  [#15400](https://github.com/rust-lang/cargo/pull/15400)
- `build-dir`：在 cargo metadata 文档中添加 build_directory 
  [#15410](https://github.com/rust-lang/cargo/pull/15410)
- `unit-graph`：切换到 Package ID Spec。
  [#15447](https://github.com/rust-lang/cargo/pull/15447)
- `-Zgc`：将 `gc` 配置表重命名为 `[cache]`。
  底层设置现在位于 `[cache.global-clean]` 下。
  [#15367](https://github.com/rust-lang/cargo/pull/15367)
- `-Zdoctest-xcompile`：更新 doctest xcompile 标志。
  [#15455](https://github.com/rust-lang/cargo/pull/15455)

### 文档

- 提及 Cargo 目标命名采用 kebab-case 的约定。
  [#14439](https://github.com/rust-lang/cargo/pull/14439)
- 在 `CARGO_CFG_TARGET_ABI` 中使用更好的示例值 
  [#15404](https://github.com/rust-lang/cargo/pull/15404)

### 内部

- 修复 CliUnstable 解析的格式化
  [#15434](https://github.com/rust-lang/cargo/pull/15434)
- ci：恢复 cargo-util 的 semver-checks
  [#15389](https://github.com/rust-lang/cargo/pull/15389)
- ci：添加 aarch64 linux runner
  [#15077](https://github.com/rust-lang/cargo/pull/15077)
- rustfix：对快照测试使用 `snapbox`
  [#15429](https://github.com/rust-lang/cargo/pull/15429)
- test：防止未声明的公网访问 
  [#15368](https://github.com/rust-lang/cargo/pull/15368)
- 更新依赖。
  [#15373](https://github.com/rust-lang/cargo/pull/15373)
  [#15381](https://github.com/rust-lang/cargo/pull/15381)
  [#15391](https://github.com/rust-lang/cargo/pull/15391)
  [#15394](https://github.com/rust-lang/cargo/pull/15394)
  [#15403](https://github.com/rust-lang/cargo/pull/15403)
  [#15415](https://github.com/rust-lang/cargo/pull/15415)
  [#15421](https://github.com/rust-lang/cargo/pull/15421)
  [#15446](https://github.com/rust-lang/cargo/pull/15446)


## Cargo 1.87 (2025-05-15)
[ce948f46...rust-1.87.0](https://github.com/rust-lang/cargo/compare/ce948f46...rust-1.87.0)

### 新增

- 通过 `term.progress.term-integration` 配置字段，
  借助 ANSI OSC 9;4 序列加入终端集成。这会将进度
  报告给终端模拟器，以便在任务栏等位置显示。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#termprogressterm-integration))
  [#14615](https://github.com/rust-lang/cargo/pull/14615)
- 转发第三方子命令的 bash 补全 
  [#15247](https://github.com/rust-lang/cargo/pull/15247)
- cargo-tree：为输出着色。
  [#15242](https://github.com/rust-lang/cargo/pull/15242)
- cargo-package：添加 `--exclude-lockfile` 标志，若存在 lock 文件则
  停止验证它。
  [#15234](https://github.com/rust-lang/cargo/pull/15234)

### 变更

- ❗️ Cargo 现在依赖 OpenSSL v3。这意味着官方
  Rust 发行版中的 Cargo 在 32 位平台上将硬依赖 libatomic。
  [#15232](https://github.com/rust-lang/cargo/pull/15232)
- 向用户报告 `<target>.edition` 的弃用。
  [#15321](https://github.com/rust-lang/cargo/pull/15321)
- 借助 clap 为 `--vcs`、`--color` 与 `--message-format` 标志提供默认值。
  [#15322](https://github.com/rust-lang/cargo/pull/15322)
- 在错误消息中提及 "3" 是 "resolver" 字段的有效值 
  [#15215](https://github.com/rust-lang/cargo/pull/15215)
- 提升 windows Cygwin DLL 导入库 
  [#15193](https://github.com/rust-lang/cargo/pull/15193)
- 在目标提示消息中也包含包名。
  [#15199](https://github.com/rust-lang/cargo/pull/15199)
- cargo-add：折叠大型 feature 列表
  [#15200](https://github.com/rust-lang/cargo/pull/15200)
- cargo-vendor：添加哪个 workspace 解析失败的上下文
  [#15297](https://github.com/rust-lang/cargo/pull/15297)

### 修复

- 不将 `cargo::rustc-link-arg-cdylib` 的 cdylib 链接参数传给测试。
  [#15317](https://github.com/rust-lang/cargo/pull/15317)
  [#15326](https://github.com/rust-lang/cargo/pull/15326)
- 在 `cargo metadata` 中不使用 `$CARGO_BUILD_TARGET`。
  [#15271](https://github.com/rust-lang/cargo/pull/15271)
- 允许 `term.progress.when` 具有默认值。即使缺少其他设置，
  `CARGO_TERM_PROGRESS_WIDTH` 现在也能正确设置。
  [#15287](https://github.com/rust-lang/cargo/pull/15287)
- 修复外部子命令的 `CARGO` 环境变量指向错误的
  Cargo 二进制路径。请注意，该环境变量
  从未设计为通用的 Cargo 包装器。
  [#15208](https://github.com/rust-lang/cargo/pull/15208)
- 修复 future-incompat 报告生成的一些问题。
  [#15345](https://github.com/rust-lang/cargo/pull/15345)
- 在所有接受 `--offline` 或 `--locked` 的地方也尊重 `--frozen`。
  [#15263](https://github.com/rust-lang/cargo/pull/15263)
- cargo-package：若脏，也报告 workspace 清单的 VCS 状态。
  [#15276](https://github.com/rust-lang/cargo/pull/15276)
  [#15341](https://github.com/rust-lang/cargo/pull/15341)
- cargo-publish：修复含格式错误的 `{{#options}}` 块的手册页
  [#15191](https://github.com/rust-lang/cargo/pull/15191)
- cargo-run：区分来自不同包但同名的 bin。
  [#15298](https://github.com/rust-lang/cargo/pull/15298)
- cargo-rustc：对 crate 类型去重。
  [#15314](https://github.com/rust-lang/cargo/pull/15314)
- cargo-vendor：不要移除未缓存的源。
  [#15260](https://github.com/rust-lang/cargo/pull/15260)

### 仅 Nightly

- 🔥 cargo-package：添加不稳定的 `--message-format` 标志。该标志为
  `--list` 标志的文件列表提供另一种 JSON 输出格式。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#package-message-format))
  [#15311](https://github.com/rust-lang/cargo/pull/15311)
  [#15354](https://github.com/rust-lang/cargo/pull/15354)
- 🔥 `build-dir`：`build.build-dir` 配置选项用于设置
  存放中间构建产物的目录。
  中间产物由 Rustc/Cargo 在构建过程中生成。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#build-dir))
  [#15104](https://github.com/rust-lang/cargo/pull/15104)
  [#15236](https://github.com/rust-lang/cargo/pull/15236)
  [#15334](https://github.com/rust-lang/cargo/pull/15334)
- 🔥 `-Zsbom`：`build.sbom` 配置允许在每个编译产物旁
  生成所谓的 SBOM 前驱文件。
  ([RFC 3553](https://github.com/rust-lang/rfcs/pull/3553))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#sbom))
  [#13709](https://github.com/rust-lang/cargo/pull/13709)
- 🔥 `-Zpublic-dependency`：为 `cargo tree` 新增 `--depth public` 值，
  以显示公共依赖。
  [#15243](https://github.com/rust-lang/cargo/pull/15243)
- `-Zscript`：处理更多 frontmatter 解析边界情况
  [#15187](https://github.com/rust-lang/cargo/pull/15187)
- `-Zpackage-workspace`：修复对首字母大写的 workspace 成员索引条目的查找 
  [#15216](https://github.com/rust-lang/cargo/pull/15216)
- `-Zpackage-workspace`：在 overlay 中注册 workspace 成员重命名 
  [#15228](https://github.com/rust-lang/cargo/pull/15228)
- `-Zpackage-workspace`：确保可以打包以 '.rs' 结尾的目录 
  [#15240](https://github.com/rust-lang/cargo/pull/15240)
- `native-completions`：为 `--profile` 添加补全
  [#15308](https://github.com/rust-lang/cargo/pull/15308)
- `native-completions`：为别名添加补全
  [#15319](https://github.com/rust-lang/cargo/pull/15319)
- `native-completions`：为 `cargo add --path` 添加补全
  [#15288](https://github.com/rust-lang/cargo/pull/15288)
- `native-completions`：为 `--manifest-path` 添加补全 
  [#15225](https://github.com/rust-lang/cargo/pull/15225)
- `native-completions`：为 `--lockfile-path` 添加补全 
  [#15238](https://github.com/rust-lang/cargo/pull/15238)
- `native-completions`：为 `cargo install --path` 添加补全
  [#15266](https://github.com/rust-lang/cargo/pull/15266)
- `native-completions`：为 `+<toolchain>` 添加补全
  [#15301](https://github.com/rust-lang/cargo/pull/15301)

### 文档

- 注明 target-edition 已弃用 
  [#15292](https://github.com/rust-lang/cargo/pull/15292)
- 提及错误 URL 是 git 认证错误的原因之一 
  [#15304](https://github.com/rust-lang/cargo/pull/15304)
- 将重点转向 resolver v3 
  [#15213](https://github.com/rust-lang/cargo/pull/15213)
- 自 1.84 起始终包含 Lockfile 
  [#15257](https://github.com/rust-lang/cargo/pull/15257)
- 在示例中从 `package.include` 移除 `Cargo.toml` 
  [#15253](https://github.com/rust-lang/cargo/pull/15253)
- 更清楚地说明 `rust_version` 在编译期间会强制执行
  [#15303](https://github.com/rust-lang/cargo/pull/15303)
- 修复参考文档中 `[env]` `relative` 的描述 
  [#15332](https://github.com/rust-lang/cargo/pull/15332)
- 在 Cargo Book 中使用构建脚本时，为 `extern` 添加 `unsafe` 
  [#15294](https://github.com/rust-lang/cargo/pull/15294)
- 提及 `x.y.*` 是应避免的一种版本要求形式。 
  [#15310](https://github.com/rust-lang/cargo/pull/15310)
- contrib：扩展团队会议的描述 
  [#15349](https://github.com/rust-lang/cargo/pull/15349)

### 内部

- 通过 `CFG_VER_DESCRIPTION` 环境变量显示来自 bootstrap 的额外构建描述。
  [#15269](https://github.com/rust-lang/cargo/pull/15269)
- 用 `std::fmt` 选项控制字节显示精度。
  [#15246](https://github.com/rust-lang/cargo/pull/15246)
- 用 jiff 替换 humantime crate。
  [#15290](https://github.com/rust-lang/cargo/pull/15290)
- 在 1.86 发布前不检查 cargo-util semver 
  [#15222](https://github.com/rust-lang/cargo/pull/15222)
- Redox OS 属于 unix 家族 
  [#15307](https://github.com/rust-lang/cargo/pull/15307)
- cargo-tree：抽象 NodeId 概念 
  [#15237](https://github.com/rust-lang/cargo/pull/15237)
- cargo-tree：抽象边的概念 
  [#15233](https://github.com/rust-lang/cargo/pull/15233)
- ci：自动更新 cargo-semver-checks 
  [#15212](https://github.com/rust-lang/cargo/pull/15212)
- ci：在 Github 中可视化分组输出 
  [#15218](https://github.com/rust-lang/cargo/pull/15218)
- manifest：集中化 Cargo 目标描述 
  [#15291](https://github.com/rust-lang/cargo/pull/15291)
- 更新依赖。
  [#15250](https://github.com/rust-lang/cargo/pull/15250)
  [#15249](https://github.com/rust-lang/cargo/pull/15249)
  [#15245](https://github.com/rust-lang/cargo/pull/15245)
  [#15224](https://github.com/rust-lang/cargo/pull/15224)
  [#15282](https://github.com/rust-lang/cargo/pull/15282)
  [#15211](https://github.com/rust-lang/cargo/pull/15211)
  [#15217](https://github.com/rust-lang/cargo/pull/15217)
  [#15268](https://github.com/rust-lang/cargo/pull/15268)

## Cargo 1.86 (2025-04-03)
[d73d2caf...rust-1.86.0](https://github.com/rust-lang/cargo/compare/d73d2caf...rust-1.86.0)

### 新增

### 变更

- ❗️ 合并时，对引用程序路径及其参数的配置键，
  采用替换而非合并。
  [#15066](https://github.com/rust-lang/cargo/pull/15066)  
  这些键包括：
  - `registry.credential-provider`
  - `registries.*.credential-provider`
  - `target.*.runner`
  - `host.runner`
  - `credential-alias.*`
  - `doc.browser`
- ❗️ 若同时传入 `--package` 与 `--workspace` 但请求的
  包缺失，则报错。此前会静默忽略，这被视为
  缺陷，因为缺失的包应当被报告。
  [#15071](https://github.com/rust-lang/cargo/pull/15071)
- 更新索引缓存失败时添加警告。
  [#15014](https://github.com/rust-lang/cargo/pull/15014)
- 错误中不再使用 "did you mean"。直接说明建议是什么。
  [#15138](https://github.com/rust-lang/cargo/pull/15138)
- 为依赖源中无效的 SSH URL 提供更好的错误消息。
  [#15185](https://github.com/rust-lang/cargo/pull/15185)
- 当包没有给定 feature 时，建议相似的 feature 名称。
  [#15133](https://github.com/rust-lang/cargo/pull/15133)
- 找不到 workspace 成员时打印 glob。
  [#15093](https://github.com/rust-lang/cargo/pull/15093)
- cargo-fix：使 `--allow-dirty` 隐含 `--allow-staged`
  [#15013](https://github.com/rust-lang/cargo/pull/15013)
- cargo-login：为准备弃用，在 CLI 帮助中隐藏 `token` 参数。
  [#15057](https://github.com/rust-lang/cargo/pull/15057)
- cargo-login：使用不兼容的凭证提供程序时，不要建议 `cargo login`。
  [#15124](https://github.com/rust-lang/cargo/pull/15124)
- cargo-package：通过用 pathspec 匹配特定路径前缀，
  改进 VCS 状态检查的性能。
  [#14997](https://github.com/rust-lang/cargo/pull/14997)

### 修复

- `rerun-if-env-changed` 构建脚本指令现在能正确检测
  `[env]` 配置表中的变更。
  [#14756](https://github.com/rust-lang/cargo/pull/14756)
- 在为不受支持的 crate 类型学习 Rust 目标信息时，强制将警告作为警告发出。
  [#15036](https://github.com/rust-lang/cargo/pull/15036)
- cargo-package：当符号链接指向当前包根目录之外的路径时，
  验证其 VCS 状态。
  [#14981](https://github.com/rust-lang/cargo/pull/14981)

### 仅 Nightly

- 🔥 `-Z feature-unification`：此新的不稳定标志启用
  `resolver.feature-unification` 配置选项，以控制
  workspace 中 feature 如何统一。
  ([RFC 3529](https://github.com/rust-lang/rfcs/blob/master/text/3692-feature-unification.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#feature-unification))
  [#15157](https://github.com/rust-lang/cargo/pull/15157)
- cargo-util-schemas：纠正并更新 JSON Schema
  [#15000](https://github.com/rust-lang/cargo/pull/15000)
- cargo-util-schemas：修复 `[lints]` JSON Schema 
  [#15035](https://github.com/rust-lang/cargo/pull/15035)
- cargo-util-schemas：修复 'metadata' JSON Schema 
  [#15033](https://github.com/rust-lang/cargo/pull/15033)
- `cargo rustc --print`：为 `cargo rustc --print` 设置 cargo 环境。
  [#15026](https://github.com/rust-lang/cargo/pull/15026)
- `-Zbuild-std`：将值解析为逗号分隔列表，并将该行为
  扩展到 `build-std-features`。
  [#15065](https://github.com/rust-lang/cargo/pull/15065)
- `-Zgc`：使缓存跟踪对意外文件更具弹性。
  [#15147](https://github.com/rust-lang/cargo/pull/15147)
- `-Zscript`：合并从清单路径创建 SourceId 的逻辑 
  [#15172](https://github.com/rust-lang/cargo/pull/15172)
- `-Zscript`：将 cargo-script 逻辑集成到主解析器 
  [#15168](https://github.com/rust-lang/cargo/pull/15168)
- `-Zscript`：为 cargo-script 添加 `cargo pkgid` 支持 
  [#14961](https://github.com/rust-lang/cargo/pull/14961)
- `-Zpackage-workspace`：报告所有不可发布的包 
  [#15070](https://github.com/rust-lang/cargo/pull/15070)

### 文档

- 说明自 1.46 起，Cargo 会自动注册 `env!`
  宏中使用的变量以触发重新构建。
  [#15062](https://github.com/rust-lang/cargo/pull/15062)
- 将 changelog 移至 The Cargo Book。
  [#15119](https://github.com/rust-lang/cargo/pull/15119)
  [#15123](https://github.com/rust-lang/cargo/pull/15123)
  [#15142](https://github.com/rust-lang/cargo/pull/15142)
- 注明 `package.authors` 已弃用。
  [#15068](https://github.com/rust-lang/cargo/pull/15068)
- 修复 Package Id Specification 的错误语法。
  [#15049](https://github.com/rust-lang/cargo/pull/15049)
- 修复关于 MSRV 的倒置逻辑
  [#15044](https://github.com/rust-lang/cargo/pull/15044)
- cargo-metadata：修复 `"root"` 字段的描述。
  [#15182](https://github.com/rust-lang/cargo/pull/15182)
- cargo-package：注明始终包含 lock 文件。
  [#15067](https://github.com/rust-lang/cargo/pull/15067)
- contrib：开始 schema 设计指南。
  [#15037](https://github.com/rust-lang/cargo/pull/15037)

### 内部

- 在 Solaris 上不使用 `libc::LOCK_*`。
  [#15143](https://github.com/rust-lang/cargo/pull/15143)
- 清理 field → env var 处理。
  [#15008](https://github.com/rust-lang/cargo/pull/15008)
- 简化 SourceID Ord/Eq。
  [#14980](https://github.com/rust-lang/cargo/pull/14980)
  [#15103](https://github.com/rust-lang/cargo/pull/15103)
- 为 SourceKind 添加手动 Hash 实现并记录原因。
  [#15029](https://github.com/rust-lang/cargo/pull/15029)
- ci：在 CI 中允许 Windows 保留名 
  [#15135](https://github.com/rust-lang/cargo/pull/15135)
- cargo-test-macro：移除对 `RUSTUP_WINDOWS_PATH_ADD_BIN` 的条件
  [#15017](https://github.com/rust-lang/cargo/pull/15017)
- resolver：简化 backtrack
  [#15150](https://github.com/rust-lang/cargo/pull/15150)
- resolver：小清理 
  [#15040](https://github.com/rust-lang/cargo/pull/15040)
- test：清理浅获取测试
  [#15002](https://github.com/rust-lang/cargo/pull/15002)
- test：修复 macOS 上的 `https::self_signed_should_fail`
  [#15016](https://github.com/rust-lang/cargo/pull/15016)
- test：修复较新 git 版本下的 benchsuite 问题
  [#15069](https://github.com/rust-lang/cargo/pull/15069)
- test：修复 Windows 上运行的 shared_std_dependency_rebuild
  [#15111](https://github.com/rust-lang/cargo/pull/15111)
- test：更新测试以修复 nightly 错误
  [#15110](https://github.com/rust-lang/cargo/pull/15110)
- test：移除未使用的 `-C link-arg=-fuse-ld=lld`
  [#15097](https://github.com/rust-lang/cargo/pull/15097)
- test：使用 `LazyLock` 移除 `unsafe`
  [#15096](https://github.com/rust-lang/cargo/pull/15096)
- test：移除不必要的 into 转换
  [#15042](https://github.com/rust-lang/cargo/pull/15042)
- test：修复 panic_abort_tests 中的竞态条件
  [#15169](https://github.com/rust-lang/cargo/pull/15169)
- 更新 deny.toml
  [#15164](https://github.com/rust-lang/cargo/pull/15164)
- 更新依赖。
  [#14995](https://github.com/rust-lang/cargo/pull/14995)
  [#14996](https://github.com/rust-lang/cargo/pull/14996)
  [#14998](https://github.com/rust-lang/cargo/pull/14998)
  [#15012](https://github.com/rust-lang/cargo/pull/15012)
  [#15018](https://github.com/rust-lang/cargo/pull/15018)
  [#15041](https://github.com/rust-lang/cargo/pull/15041)
  [#15050](https://github.com/rust-lang/cargo/pull/15050)
  [#15121](https://github.com/rust-lang/cargo/pull/15121)
  [#15128](https://github.com/rust-lang/cargo/pull/15128)
  [#15129](https://github.com/rust-lang/cargo/pull/15129)
  [#15162](https://github.com/rust-lang/cargo/pull/15162)
  [#15163](https://github.com/rust-lang/cargo/pull/15163)
  [#15165](https://github.com/rust-lang/cargo/pull/15165)
  [#15166](https://github.com/rust-lang/cargo/pull/15166)

## Cargo 1.85 (2025-02-20)
[66221abd...rust-1.85.0](https://github.com/rust-lang/cargo/compare/66221abd...rust-1.85.0)

### 新增

- 🎉 Cargo 现在支持 2024 edition。
  更多信息见 [edition guide](https://doc.rust-lang.org/nightly/edition-guide/rust-2024/index.html)。
  [#14828](https://github.com/rust-lang/cargo/pull/14828)
- cargo-tree：`--depth` 标志现在接受 `workspace`，
  仅显示属于当前 workspace 成员的依赖。
  [#14928](https://github.com/rust-lang/cargo/pull/14928)
- 构建脚本现在会收到新的环境变量 `CARGO_CFG_FEATURE`，
  其中包含正在构建的包的每个已激活 feature。
  [#14902](https://github.com/rust-lang/cargo/pull/14902)
- perf：由于对 `ActivationsKey` 使用了更高效的哈希，依赖解析现在更快
  [#14915](https://github.com/rust-lang/cargo/pull/14915)

### 变更

- ❗️ cargo-rustc：尾随标志现在具有更高优先级。
  该行为自 1.83 起仅在 nightly 可用，现已稳定。
  [#14900](https://github.com/rust-lang/cargo/pull/14900)
- ❗️ Cargo 现在使用来自 `rustc-stable-hash` 的跨平台哈希算法。
  因此，依赖缓存路径中的哈希部分
  （例如 `$CARGO_HOME/registry/index/index.crates.io-<hash>`）将改变。
  这将触发 registry 索引与 `.crate` tar 包的重新下载，
  以及 Git 依赖的重新克隆。
  [#14917](https://github.com/rust-lang/cargo/pull/14917)
- 为 Cargo.toml 与 Cargo 配置中 `cfg` 里的关键字添加
  future-incompatibility 警告。像 `cfg(true)` 与 `cfg(false)` 这类
  带关键字的 `cfg` 曾被错误接受。为保持向后兼容，已引入对原始
  标识符的支持；例如，请改用 `cfg(r#true)`。
  [#14671](https://github.com/rust-lang/cargo/pull/14671)
- 依赖解析现在提供更丰富的错误消息，解释为何某些版本被拒绝、未匹配或无效。  
  [#14897](https://github.com/rust-lang/cargo/pull/14897)
  [#14921](https://github.com/rust-lang/cargo/pull/14921)
  [#14923](https://github.com/rust-lang/cargo/pull/14923)
  [#14927](https://github.com/rust-lang/cargo/pull/14927)
- cargo-doc：改进在未生成文档时 `--open` 打开文档的错误消息。
  [#14969](https://github.com/rust-lang/cargo/pull/14969)
- cargo-package：若符号链接被检出为纯文本文件则警告 
  [#14994](https://github.com/rust-lang/cargo/pull/14994)
- cargo-package：显示相对于 Git 工作目录的脏文件路径。
  [#14968](https://github.com/rust-lang/cargo/pull/14968)
  [#14970](https://github.com/rust-lang/cargo/pull/14970)

### 修复

- 设置 `GIT_DIR` 以确保在 `net.git-fetch-with-cli=true` 时
  与裸仓库兼容。
  [#14860](https://github.com/rust-lang/cargo/pull/14860)
- 修复修改 workspace Cargo.toml 未使构建缓存失效。
  [#14973](https://github.com/rust-lang/cargo/pull/14973)
- 防止更改 `RUSTFLAGS` 后丢弃构建缓存。
  [#14830](https://github.com/rust-lang/cargo/pull/14830)
  [#14898](https://github.com/rust-lang/cargo/pull/14898)
- cargo-add：规范化名称时不选择已 yank 的版本。
  [#14895](https://github.com/rust-lang/cargo/pull/14895)
- cargo-fix：对虚拟清单也将 workspace 依赖迁移到 2024 edition。
  [#14890](https://github.com/rust-lang/cargo/pull/14890)
- cargo-package：当 `package.readme` 与 `package.license-file`
  指向当前包根目录之外的路径时，验证其 VCS 状态。
  [#14966](https://github.com/rust-lang/cargo/pull/14966)
- cargo-package：确保可能阻塞的非文件（如 FIFO）不会
  被拾取用于发布。
  [#14977](https://github.com/rust-lang/cargo/pull/14977)

### 仅 Nightly

- `path-bases`：在虚拟清单的 `[patch]` 中支持 bases
  [#14931](https://github.com/rust-lang/cargo/pull/14931)
- `unit-graph`：使用已配置的 shell 打印输出。
  [#14926](https://github.com/rust-lang/cargo/pull/14926)
- `-Zbuild-std`：通过探测目标规范 JSON 中的 `metadata.std` 字段，
  检查构建目标是否支持 `std`。
  [#14183](https://github.com/rust-lang/cargo/pull/14183)
  [#14938](https://github.com/rust-lang/cargo/pull/14938)
  [#14899](https://github.com/rust-lang/cargo/pull/14899)
- `-Zbuild-std`：测试 proc-macro 时始终链接到 std。
  [#14850](https://github.com/rust-lang/cargo/pull/14850)
  [#14861](https://github.com/rust-lang/cargo/pull/14861)
- `-Zbuild-std`：清理 build-std 测试
  [#14943](https://github.com/rust-lang/cargo/pull/14943)
  [#14933](https://github.com/rust-lang/cargo/pull/14933)
  [#14896](https://github.com/rust-lang/cargo/pull/14896)
- `-Zbuild-std`：对 std workspace 哈希相对路径而非绝对路径。
  [#14951](https://github.com/rust-lang/cargo/pull/14951)
- `-Zpackage-workspace`：允许未 bump 的 workspace 进行 dry-run。
  [#14847](https://github.com/rust-lang/cargo/pull/14847)
- `-Zscript`：允许从 cargo script 添加/移除依赖
  [#14857](https://github.com/rust-lang/cargo/pull/14857)
- `-Zscript`：跨 edition 迁移 cargo script 清单
  [#14864](https://github.com/rust-lang/cargo/pull/14864)
- `-Zscript`：不要覆盖 release profile。
  [#14925](https://github.com/rust-lang/cargo/pull/14925)
- `-Ztrim-paths`：使用 `Path::push` 构造 `remap-path-prefix` 标志。
  [#14908](https://github.com/rust-lang/cargo/pull/14908)

### 文档

- 澄清如何选择 `cargo::metadata` 环境变量。
  [#14842](https://github.com/rust-lang/cargo/pull/14842)
- cargo-info：从 `cargo-info` 文档中移除对默认 registry 的引用
  [#14880](https://github.com/rust-lang/cargo/pull/14880)
- contrib：为 Rustup Cargo 变通方案补充缺失参数 
  [#14954](https://github.com/rust-lang/cargo/pull/14954)
- SemVer：添加关于 RPIT 捕获的章节 
  [#14849](https://github.com/rust-lang/cargo/pull/14849)

### 内部

- 在编译器变更之前，将 `test` cfg 添加为已知 cfg。
  [#14963](https://github.com/rust-lang/cargo/pull/14963)
- 启用 triagebot 合并冲突通知
  [#14972](https://github.com/rust-lang/cargo/pull/14972)
- 将发布触发限制为 `0.*` 标签
  [#14940](https://github.com/rust-lang/cargo/pull/14940)
- 简化 `SourceID` Hash。
  [#14800](https://github.com/rust-lang/cargo/pull/14800)
- build-rs：访问 Cargo 为构建脚本执行设置的环境变量时，
  自动发出 `rerun-if-env-changed`。
  [#14911](https://github.com/rust-lang/cargo/pull/14911)
- build-rs：在 assert 中正确引用该项 
  [#14913](https://github.com/rust-lang/cargo/pull/14913)
- build-rs：添加 'error' 指令 
  [#14910](https://github.com/rust-lang/cargo/pull/14910)
- build-rs：移除无意义的 'cargo_cfg_debug_assertions' 
  [#14901](https://github.com/rust-lang/cargo/pull/14901)
- cargo-package：将 `cargo_package` 拆分为模块 
  [#14959](https://github.com/rust-lang/cargo/pull/14959)
  [#14982](https://github.com/rust-lang/cargo/pull/14982)
- cargo-test-support：`requires` 属性接受 cmds 的字符串字面量
  [#14875](https://github.com/rust-lang/cargo/pull/14875)
- cargo-test-support：从 'exec_with_output' 切换到 'run'
  [#14848](https://github.com/rust-lang/cargo/pull/14848)
- cargo-test-support：跟踪 `.crate` 文件发布验证的调用者 
  [#14992](https://github.com/rust-lang/cargo/pull/14992)
- test：直接验证 `-Cmetadata`，而非通过 `-Cextra-filename`
  [#14846](https://github.com/rust-lang/cargo/pull/14846)
- test：确保 PGO 可用
  [#14859](https://github.com/rust-lang/cargo/pull/14859)
  [#14874](https://github.com/rust-lang/cargo/pull/14874)
  [#14887](https://github.com/rust-lang/cargo/pull/14887)
- 更新依赖。
  [#14867](https://github.com/rust-lang/cargo/pull/14867)
  [#14871](https://github.com/rust-lang/cargo/pull/14871)
  [#14878](https://github.com/rust-lang/cargo/pull/14878)
  [#14879](https://github.com/rust-lang/cargo/pull/14879)
  [#14975](https://github.com/rust-lang/cargo/pull/14975)

## Cargo 1.84 (2025-01-09)
[15fbd2f6...rust-1.84.0](https://github.com/rust-lang/cargo/compare/15fbd2f6...rust-1.84.0)

### 新增

- 🎉 稳定化 resolver v3，亦即感知 MSRV 的依赖解析器。
  稳定化包括 Cargo.toml 中的 `package.resolver = "3"`，
  以及 Cargo 配置中的 `[resolver]` 表。
  ([RFC 3537](https://github.com/rust-lang/rfcs/blob/master/text/3537-msrv-resolver.md))
  ([manifest docs](https://doc.rust-lang.org/nightly/cargo/reference/resolver.html#resolver-versions))
  ([config docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#resolver))
  [#14639](https://github.com/rust-lang/cargo/pull/14639)
  [#14662](https://github.com/rust-lang/cargo/pull/14662)
  [#14711](https://github.com/rust-lang/cargo/pull/14711)
  [#14725](https://github.com/rust-lang/cargo/pull/14725)
  [#14748](https://github.com/rust-lang/cargo/pull/14748)
  [#14753](https://github.com/rust-lang/cargo/pull/14753)
  [#14754](https://github.com/rust-lang/cargo/pull/14754)
- 新增构建脚本调用 `cargo::error=MESSAGE` 以报告错误消息。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/build-scripts.html#cargo-error))
  [#14743](https://github.com/rust-lang/cargo/pull/14743)

### 变更

- ❗️ cargo-publish：发布的 crate 中始终包含 Cargo.lock。
  原先仅对带有可执行文件或示例、
  以便与 `cargo install` 一起使用的包包含。
  [#14815](https://github.com/rust-lang/cargo/pull/14815)
- 依赖解析器性能改进，包括共享缓存、
  减少迭代开销，以及移除冗余的获取与克隆。
  [#14663](https://github.com/rust-lang/cargo/pull/14663)
  [#14690](https://github.com/rust-lang/cargo/pull/14690)
  [#14692](https://github.com/rust-lang/cargo/pull/14692)
  [#14694](https://github.com/rust-lang/cargo/pull/14694)
- 弃用 `cargo verify-project`。
  [#14736](https://github.com/rust-lang/cargo/pull/14736)
- 依赖解析期间找不到匹配包时，添加源替换信息。
  [#14715](https://github.com/rust-lang/cargo/pull/14715)
- 发现 `[patch.crates.io]` 时提示使用 `crates-io`。
  [#14700](https://github.com/rust-lang/cargo/pull/14700)
- 规范化 Cargo 目标的源路径以获得更好的诊断。
  [#14497](https://github.com/rust-lang/cargo/pull/14497)
  [#14750](https://github.com/rust-lang/cargo/pull/14750)
- 允许 registry 在索引元数据 JSON 中省略空/默认字段。
  出于向后兼容，crates.io 继续发出它们。
  [#14838](https://github.com/rust-lang/cargo/pull/14838)
  [#14839](https://github.com/rust-lang/cargo/pull/14839)
- cargo-doc：在额外详细模式下显示环境变量。
  [#14812](https://github.com/rust-lang/cargo/pull/14812)
- cargo-fix：替换仅插入式重复替换的特例处理。
  [#14765](https://github.com/rust-lang/cargo/pull/14765)
  [#14782](https://github.com/rust-lang/cargo/pull/14782)
- cargo-remove：找不到依赖时，尝试建议名称相似的
  其他依赖。
  [#14818](https://github.com/rust-lang/cargo/pull/14818)
- git：对 Git 依赖的全新检出跳过不必要的子模块校验。
  [#14605](https://github.com/rust-lang/cargo/pull/14605)
- git：增强获取 Git 依赖时找不到 refspec 的错误消息。
  [#14806](https://github.com/rust-lang/cargo/pull/14806)
- git：当 `net.git-fetch-with-cli = true` 时，默认向 git CLI 传递 `--no-tags`。
  [#14688](https://github.com/rust-lang/cargo/pull/14688)

### 修复

- 修复旧版 Cargo 无法读取构建缓存中较新格式的 dep-info。
  [#14751](https://github.com/rust-lang/cargo/pull/14751)
  [#14745](https://github.com/rust-lang/cargo/pull/14745)
- 修复重建检测不尊重 `[env]` 表中的变更。
  [#14701](https://github.com/rust-lang/cargo/pull/14701)
  [#14730](https://github.com/rust-lang/cargo/pull/14730)
- cargo-fix：为 `rustfix` 添加事务语义，以便在多个建议
  包含重叠 span 时保持代码修复处于有效状态。
  [#14747](https://github.com/rust-lang/cargo/pull/14747)

### 仅 Nightly

- 已移除不稳定环境变量 `CARGO_RUSTC_CURRENT_DIR`。
  [#14799](https://github.com/rust-lang/cargo/pull/14799)
- 🔥 Cargo 现在在源代码中包含用于 `Cargo.toml` 的实验性 JSON Schema 文件。
  它帮助外部工具验证或自动补全清单的 schema。
  ([manifest.schema.json](https://github.com/rust-lang/cargo/blob/master/crates/cargo-util-schemas/manifest.schema.json))
  [#14683](https://github.com/rust-lang/cargo/pull/14683)
- 🔥 `Zroot-dir`：新的不稳定 `-Zroot-dir` 标志，用于配置
  应从哪个路径调用 rustc。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#root-dir))
  [#14752](https://github.com/rust-lang/cargo/pull/14752)
- 🔥 `-Zwarnings`：新的不稳定功能，通过 `build.warnings` 配置字段
  控制 Cargo 如何处理警告。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#warnings))
  [#14388](https://github.com/rust-lang/cargo/pull/14388)
  [#14827](https://github.com/rust-lang/cargo/pull/14827)
  [#14836](https://github.com/rust-lang/cargo/pull/14836)
- `edition2024`：验证 2024 edition / resolver=3 不影响解析
  [#14724](https://github.com/rust-lang/cargo/pull/14724)
- `native-completions`：在 zsh 中包含描述
  [#14726](https://github.com/rust-lang/cargo/pull/14726)
- `-Zbindeps`：修复对带有交叉编译 bindep 的包运行 cargo tree 时的 panic
  [#14593](https://github.com/rust-lang/cargo/pull/14593)
- `-Zbindeps`：按 artifact 依赖的目标平台下载其有针对性的传递依赖
  [#14723](https://github.com/rust-lang/cargo/pull/14723)
- `-Zbuild-std`：移除对 `--target` 的要求。
  [#14317](https://github.com/rust-lang/cargo/pull/14317)
- `-Zpackage-workspace`：在 `cargo publish` 中支持包选择选项，
  例如 `--exclude`
  [#14659](https://github.com/rust-lang/cargo/pull/14659)
- `-Zscript`：移除对接受 `Cargo.toml` 的支持。
  [#14670](https://github.com/rust-lang/cargo/pull/14670)
- `-Zscript`：更改配置路径，仅检查 `CARGO_HOME`
  [#14749](https://github.com/rust-lang/cargo/pull/14749)
- `-Zscript`：按 RFC 3503 更新 frontmatter 解析器。
  [#14792](https://github.com/rust-lang/cargo/pull/14792)

### 文档

- 澄清 `--tests` 与 `--benches` 标志的含义。
  [#14675](https://github.com/rust-lang/cargo/pull/14675)
- 澄清工具应仅将以 `{` 开头的行解释为 JSON。
  [#14677](https://github.com/rust-lang/cargo/pull/14677)
- 澄清 `cargo package` 包含与不包含的内容
  [#14684](https://github.com/rust-lang/cargo/pull/14684)
- 记录官方外部命令：`cargo-clippy`、`cargo-fmt` 与 `cargo-miri`。
  [#14669](https://github.com/rust-lang/cargo/pull/14669)
  [#14805](https://github.com/rust-lang/cargo/pull/14805)
- 增强环境变量文档
  [#14676](https://github.com/rust-lang/cargo/pull/14676)
- 简化文档中使用的英语。
  [#14825](https://github.com/rust-lang/cargo/pull/14825)
  [#14829](https://github.com/rust-lang/cargo/pull/14829)
- 新增关于已弃用与已移除命令的文档页。
  [#14739](https://github.com/rust-lang/cargo/pull/14739)
- cargo-test-support：根据移植工作量文档化 `Execs` 断言 
  [#14793](https://github.com/rust-lang/cargo/pull/14793)

### 内部

- 🎉 将 `build-rs` crate 迁移到 `rust-lang/cargo` 仓库，作为
  Cargo 团队的有意产物。
  [#14786](https://github.com/rust-lang/cargo/pull/14786)
  [#14817](https://github.com/rust-lang/cargo/pull/14817)
- 在 triagebot 中启用 transfer 功能
  [#14777](https://github.com/rust-lang/cargo/pull/14777)
- 在需要时对 InternedString 写时复制
  [#14808](https://github.com/rust-lang/cargo/pull/14808)
- ci：将 CI 从 bors 切换到 merge queue 
  [#14718](https://github.com/rust-lang/cargo/pull/14718)
- ci：使 `lint-docs` 作业成为必需 
  [#14797](https://github.com/rust-lang/cargo/pull/14797)
- ci：检查 clippy `correctness`
  [#14796](https://github.com/rust-lang/cargo/pull/14796)
- ci：对 renovate 将 matchPackageNames 切换为 matchDepNames
  [#14704](https://github.com/rust-lang/cargo/pull/14704)
- fingerprint：跟踪每次使用 `UnitHash` 的意图
  [#14826](https://github.com/rust-lang/cargo/pull/14826)
- fingerprint：为 `rustc_fingerprint` 添加更多元数据。
  [#14761](https://github.com/rust-lang/cargo/pull/14761)
- test：将其余快照迁移到 snapbox
  [#14642](https://github.com/rust-lang/cargo/pull/14642)
  [#14760](https://github.com/rust-lang/cargo/pull/14760)
  [#14781](https://github.com/rust-lang/cargo/pull/14781)
  [#14785](https://github.com/rust-lang/cargo/pull/14785)
  [#14790](https://github.com/rust-lang/cargo/pull/14790)
- 更新依赖。
  [#14668](https://github.com/rust-lang/cargo/pull/14668)
  [#14705](https://github.com/rust-lang/cargo/pull/14705)
  [#14762](https://github.com/rust-lang/cargo/pull/14762)
  [#14766](https://github.com/rust-lang/cargo/pull/14766)
  [#14772](https://github.com/rust-lang/cargo/pull/14772)

## Cargo 1.83 (2024-11-28)
[8f40fc59...rust-1.83.0](https://github.com/rust-lang/cargo/compare/8f40fc59...rust-1.83.0)

### 新增

- `--timings` HTML 输出现在可根据浏览器偏好
  在浅色与深色配色方案之间自动切换。
  [#14588](https://github.com/rust-lang/cargo/pull/14588)
- 引入新的 `CARGO_MANIFEST_PATH` 环境变量，
  类似于 `CARGO_MANIFEST_DIR`，但直接指向清单文件。
  [#14404](https://github.com/rust-lang/cargo/pull/14404)
- manifest：添加 `package.autolib`，允许禁用 `[lib]` 自动发现。
  [#14591](https://github.com/rust-lang/cargo/pull/14591)

### 变更

- ❗️ Lockfile 格式 v4 现在是创建/更新 lockfile 的默认格式。
  Rust 工具链 1.78+ 支持 lockfile v4。
  为与更早的 MSRV 兼容，
  可考虑将 `package.rust-version` 设为 1.82 或更早。
  [#14595](https://github.com/rust-lang/cargo/pull/14595)
- ❗️ cargo-package：使用 `--package` 标志时，仅打包指定的
  包。此前，当前工作目录中的包会自动被选中打包。
  [#14488](https://github.com/rust-lang/cargo/pull/14488)
- cargo-publish：若包版本已发布则立即失败。
  [#14448](https://github.com/rust-lang/cargo/pull/14448)
- 改进缺少 feature 时的错误消息。
  [#14436](https://github.com/rust-lang/cargo/pull/14436)
- 若未见错误，则记录 `rustc` 调用失败的详细信息
  [#14453](https://github.com/rust-lang/cargo/pull/14453)
- 提升 `windows-gnullvm` 导入库，使其与 `windows-gnu` 对齐。
  [#14451](https://github.com/rust-lang/cargo/pull/14451)
- 在 `cargo search` 结果中建议 `cargo info` 命令
  [#14537](https://github.com/rust-lang/cargo/pull/14537)
- 增强依赖更新状态消息，现在以不同颜色显示更新
  （compatible、incompatible、direct-dep），
  以及消息与 MSRV。
  [#14440](https://github.com/rust-lang/cargo/pull/14440)
  [#14457](https://github.com/rust-lang/cargo/pull/14457)
  [#14459](https://github.com/rust-lang/cargo/pull/14459)
  [#14461](https://github.com/rust-lang/cargo/pull/14461)
  [#14471](https://github.com/rust-lang/cargo/pull/14471)
  [#14568](https://github.com/rust-lang/cargo/pull/14568)
- `Locking` 状态消息不再显示 workspace 成员。
  [#14445](https://github.com/rust-lang/cargo/pull/14445)

### 修复

- 防止递归调用 `cargo` 时重复的库搜索环境变量。
  [#14464](https://github.com/rust-lang/cargo/pull/14464)
- 不要对 `$CARGO_HOME/config` 缺少 `.toml` 扩展名双重警告。
  [#14579](https://github.com/rust-lang/cargo/pull/14579)
- 使用 `--message-format json` 时更正诊断计数消息。
  [#14598](https://github.com/rust-lang/cargo/pull/14598)
- cargo-add：翻译包名时执行模糊搜索
  [#13765](https://github.com/rust-lang/cargo/pull/13765)
- cargo-new：仅相对于清单自动将新包加入 workspace，
  而非相对于当前目录。
  [#14505](https://github.com/rust-lang/cargo/pull/14505)
- cargo-rustc：修复 `--crate-type` 标志中逗号分隔值的解析。
  [#14499](https://github.com/rust-lang/cargo/pull/14499)
- cargo-vendor：仅在 crate 版本来自 registry 时信任该版本。
  这会导致即使未更改，git 依赖也会被重新 vendor。
  [#14530](https://github.com/rust-lang/cargo/pull/14530)
- cargo-publish：在 dry-run 上将 version-exists 错误降级为警告
  [#14742](https://github.com/rust-lang/cargo/pull/14742)
  [#14744](https://github.com/rust-lang/cargo/pull/14744)

### 仅 Nightly

- ❗️ cargo-rustc：在 nightly 上让尾随标志具有更高优先级。
  该 nightly gate 将在几个版本后移除。
  若破坏任何工作流，请反馈。
  提供临时环境变量 `__CARGO_RUSTC_ORIG_ARGS_PRIO=1`
  以选择退出该行为。
  [#14587](https://github.com/rust-lang/cargo/pull/14587)
- 🔥 cargo-install：新的 `--dry-run` 标志，不实际安装二进制文件。
  [#14280](https://github.com/rust-lang/cargo/pull/14280)
- 🔥 `native-completions`：将手写 shell 补全脚本迁移到
  Rust 原生实现，便于我们添加、扩展与测试新补全。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#native-completions))
  [#14493](https://github.com/rust-lang/cargo/pull/14493)
  [#14531](https://github.com/rust-lang/cargo/pull/14531)
  [#14532](https://github.com/rust-lang/cargo/pull/14532)
  [#14533](https://github.com/rust-lang/cargo/pull/14533)
  [#14534](https://github.com/rust-lang/cargo/pull/14534)
  [#14535](https://github.com/rust-lang/cargo/pull/14535)
  [#14536](https://github.com/rust-lang/cargo/pull/14536)
  [#14546](https://github.com/rust-lang/cargo/pull/14546)
  [#14547](https://github.com/rust-lang/cargo/pull/14547)
  [#14548](https://github.com/rust-lang/cargo/pull/14548)
  [#14552](https://github.com/rust-lang/cargo/pull/14552)
  [#14557](https://github.com/rust-lang/cargo/pull/14557)
  [#14558](https://github.com/rust-lang/cargo/pull/14558)
  [#14563](https://github.com/rust-lang/cargo/pull/14563)
  [#14564](https://github.com/rust-lang/cargo/pull/14564)
  [#14573](https://github.com/rust-lang/cargo/pull/14573)
  [#14590](https://github.com/rust-lang/cargo/pull/14590)
  [#14592](https://github.com/rust-lang/cargo/pull/14592)
  [#14653](https://github.com/rust-lang/cargo/pull/14653)
  [#14656](https://github.com/rust-lang/cargo/pull/14656)
- 🔥 `-Zchecksum-freshness`：用文件校验和算法替换 cargo 重建检测中
  对文件 mtime 的使用。这在 mtime 实现较差的系统上，
  或在 CI/CD 中最为有用。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#checksum-freshness))
  [#14137](https://github.com/rust-lang/cargo/pull/14137)
- cargo-update：添加 `matches_prerelease` 语义
  [#14305](https://github.com/rust-lang/cargo/pull/14305)
- `build-plan`：将其记录为已弃用。
  [#14657](https://github.com/rust-lang/cargo/pull/14657)
- `edition2024`：从 2024 edition 中移除隐式 feature 移除。
  [#14630](https://github.com/rust-lang/cargo/pull/14630)
- `lockfile-path`：在 `cargo install` 上隐含 `--locked`。
  [#14556](https://github.com/rust-lang/cargo/pull/14556)
- `open-namespaces`：允许在 `PackageIdSpec` 中使用开放命名空间
  [#14467](https://github.com/rust-lang/cargo/pull/14467)
- `path-bases`：`cargo [add|remove|update]` 支持 
  [#14427](https://github.com/rust-lang/cargo/pull/14427)
- `-Zmsrv-policy`：按其中最多数量的 MSRV 确定 workspace 的 MSRV。
  [#14569](https://github.com/rust-lang/cargo/pull/14569)
- `-Zpackage-workspace`：允许在 workspace 中发布多个 crate，
  即使它们有相互依赖。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#package-workspace))
  [#14433](https://github.com/rust-lang/cargo/pull/14433)
  [#14496](https://github.com/rust-lang/cargo/pull/14496)
- `-Zpublic-dependency`：在 `cargo metadata` 中包含公共/私有依赖状态 
  [#14504](https://github.com/rust-lang/cargo/pull/14504)
- `-Zpublic-dependency`：不要求 bump MSRV
  [#14507](https://github.com/rust-lang/cargo/pull/14507)

### 文档

- 🎉 新增关于 `package.rust-version`（亦即 MSRV）的用途、支持预期与管理的
  章节。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/rust-version.html))
  [#14619](https://github.com/rust-lang/cargo/pull/14619)
  [#14636](https://github.com/rust-lang/cargo/pull/14636)
- 澄清 `target.'cfg(...)'` 不尊重构建脚本中的 cfg 
  [#14312](https://github.com/rust-lang/cargo/pull/14312)
- 澄清 `[[bin]]` 目标自动发现可以是 `src/main.rs` 和/或在 `src/bin/` 中
  [#14515](https://github.com/rust-lang/cargo/pull/14515)
- 消除 feature resolver v2 文档中 'target' 一词用法的歧义。
  [#14540](https://github.com/rust-lang/cargo/pull/14540)
- 使 `--config <PATH>` 更突出 
  [#14631](https://github.com/rust-lang/cargo/pull/14631)
- 对页面做小幅重新分组。
  [#14620](https://github.com/rust-lang/cargo/pull/14620)
- contrib：更新关于如何发布 cargo 的文档 
  [#14539](https://github.com/rust-lang/cargo/pull/14539)
- contrib：在 Cargo 章程 / crate 文档中声明每个 crate 的支持级别
  [#14600](https://github.com/rust-lang/cargo/pull/14600)
- contrib：将新的 Intentional Artifacts 声明为 'small' 变更
  [#14599](https://github.com/rust-lang/cargo/pull/14599)

### 内部

- 清理重复的 check-cfg lint 逻辑 
  [#14567](https://github.com/rust-lang/cargo/pull/14567)
- 修复因 nightly rustc 变更导致的省略生命周期
  [#14487](https://github.com/rust-lang/cargo/pull/14487)
- 改进在 `activated_features` 中找不到 feature 时的错误报告。
  [#14647](https://github.com/rust-lang/cargo/pull/14647)
- cargo-info：使用 `shell.note` 打印 note 
  [#14554](https://github.com/rust-lang/cargo/pull/14554)
- ci：提升 CI 工具
  [#14503](https://github.com/rust-lang/cargo/pull/14503)
  [#14628](https://github.com/rust-lang/cargo/pull/14628)
- perf：在可能时对编译器消息进行零拷贝反序列化
  [#14608](https://github.com/rust-lang/cargo/pull/14608)
- resolver：添加更多 SAT resolver 测试
  [#14583](https://github.com/rust-lang/cargo/pull/14583)
  [#14614](https://github.com/rust-lang/cargo/pull/14614)
- test：将更多测试迁移到 snapbox
  [#14576](https://github.com/rust-lang/cargo/pull/14576)
  [#14577](https://github.com/rust-lang/cargo/pull/14577)
- 更新依赖。
  [#14475](https://github.com/rust-lang/cargo/pull/14475)
  [#14478](https://github.com/rust-lang/cargo/pull/14478)
  [#14489](https://github.com/rust-lang/cargo/pull/14489)
  [#14607](https://github.com/rust-lang/cargo/pull/14607)
  [#14624](https://github.com/rust-lang/cargo/pull/14624)
  [#14632](https://github.com/rust-lang/cargo/pull/14632)

## Cargo 1.82 (2024-10-17)
[a2b58c3d...rust-1.82.0](https://github.com/rust-lang/cargo/compare/a2b58c3d...rust-1.82.0)

### 新增

- 🎉 添加用于显示包信息的 `cargo info` 命令。
  [docs](https://doc.rust-lang.org/nightly/cargo/commands/cargo-info.html)
  [#14141](https://github.com/rust-lang/cargo/pull/14141)
  [#14418](https://github.com/rust-lang/cargo/pull/14418)
  [#14430](https://github.com/rust-lang/cargo/pull/14430)

### 变更

- ❗️ Doctest 通过向 rustdoc 调用传递 `--color` 来尊重 Cargo 的颜色选项。
  [#14425](https://github.com/rust-lang/cargo/pull/14425)
- 改进 Cargo.toml 中同时缺少 `[package]` 与 `[workspace]` 时的错误消息。
  [#14261](https://github.com/rust-lang/cargo/pull/14261)
- 为错误消息枚举 `profile.*.debug` 的所有可能值。
  [#14413](https://github.com/rust-lang/cargo/pull/14413)

### 修复

- 使用完整形式的 gitoxide path-spec 模式。此前实现使用
  简写 pathspec，在某些情况下会产生无效语法，例如当
  清单文件路径包含前导 `_` 下划线时
  [#14380](https://github.com/rust-lang/cargo/pull/14380)
- cargo-package：修复在裸提交 git 仓库上的失败。
  [#14359](https://github.com/rust-lang/cargo/pull/14359)
- cargo-publish：不要从发送到 registry 的 HTTP JSON 正文中，
  剥离已重命名依赖的非 dev feature。
  该缺陷仅影响第三方 registry。
  [#14325](https://github.com/rust-lang/cargo/pull/14325)
  [#14327](https://github.com/rust-lang/cargo/pull/14327)
- cargo-vendor：vendor 时不要复制被排除的 Cargo 目标的源文件。
  [#14367](https://github.com/rust-lang/cargo/pull/14367)

### 仅 Nightly

- 🔥 `lockfile-path`：添加 `--lockfile-path` 标志，允许指定
  非默认路径 `<workspace_root>/Cargo.lock` 的 lockfile 路径。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#lockfile-path))
  [#14326](https://github.com/rust-lang/cargo/pull/14326)
  [#14417](https://github.com/rust-lang/cargo/pull/14417)
  [#14423](https://github.com/rust-lang/cargo/pull/14423)
  [#14424](https://github.com/rust-lang/cargo/pull/14424)
- 🔥 `path-bases`：在 Cargo 配置文件中引入路径 "bases" 表，
  可用于为路径依赖与 patch 条目的路径加前缀。
  ([RFC 3529](https://github.com/rust-lang/rfcs/blob/master/text/3529-cargo-path-bases.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#path-bases))
  [#14360](https://github.com/rust-lang/cargo/pull/14360)
- 🔥 `-Zpackage-workspace`：增强 workspace 中 crate 有依赖时
  `cargo package --workspace` 的体验。
  workspace 中的 crate 不再需要发布到实际 registry。
  这是迈向支持 `cargo publish --workspace` 的一步。
  [#13947](https://github.com/rust-lang/cargo/pull/13947)
  [#14408](https://github.com/rust-lang/cargo/pull/14408)
  [#14340](https://github.com/rust-lang/cargo/pull/14340)
- cargo-update：将预发布匹配语义限制为仅用于 `OptVersionReq::Req` 
  [#14412](https://github.com/rust-lang/cargo/pull/14412)
- `edition2024`：还原 "fix: Ensure dep/feature activates the dependency on 2024"。
  [#14295](https://github.com/rust-lang/cargo/pull/14295)
- `update-breaking`：改进 `update --breaking` 含无效 spec 时的错误消息
  [#14279](https://github.com/rust-lang/cargo/pull/14279)
- `update-breaking`：使用 `--breaking` 更新时，不要因预发布 `VersionReq` 而降级
  [#14250](https://github.com/rust-lang/cargo/pull/14250)
- `-Zbuild-std`：移除创建虚拟 std workspace 的 hack 
  [#14358](https://github.com/rust-lang/cargo/pull/14358)
  [#14370](https://github.com/rust-lang/cargo/pull/14370)
- `-Zmsrv-policy`：调整 MSRV 解析配置字段名/值。
  此前的占位符 `resolver.something-like-precedence`
  现已重命名为 `resolver.incompatible-rust-versions`。
  [#14296](https://github.com/rust-lang/cargo/pull/14296)
- `-Zmsrv-policy`：：在选择不兼容 rust-version 的包时报告
  [#14401](https://github.com/rust-lang/cargo/pull/14401)
- `-Ztarget-applies-to-host`：修复在使用 target-applies-to-host 与隐式目标时
  links-overrides 的传递
  [#14205](https://github.com/rust-lang/cargo/pull/14205)
- `-Ztarget-applies-to-host`：`-Cmetadata` 包含额外 rustflags 是否与 host 相同
  [#14432](https://github.com/rust-lang/cargo/pull/14432)
- `-Ztrim-paths`：rustdoc 支持用于诊断的 trim-paths 
  [#14389](https://github.com/rust-lang/cargo/pull/14389)

### 文档

- 将 `Workspace` 的注释转换为文档注释。
  [#14397](https://github.com/rust-lang/cargo/pull/14397)
- 修复 `workspace.package` 与 `workspace.dependencies` 的 MSRV 指示。
  [#14400](https://github.com/rust-lang/cargo/pull/14400)
- FAQ：移除过时的 Cargo 离线用法章节。
  [#14336](https://github.com/rust-lang/cargo/pull/14336)

### 内部

- 增强 `cargo-test-support` 的可用性与文档。
  [#14266](https://github.com/rust-lang/cargo/pull/14266)
  [#14268](https://github.com/rust-lang/cargo/pull/14268)
  [#14269](https://github.com/rust-lang/cargo/pull/14269)
  [#14270](https://github.com/rust-lang/cargo/pull/14270)
  [#14272](https://github.com/rust-lang/cargo/pull/14272)
- 通过使用 Arc 而非 Rc 使 summary 同步
  [#14260](https://github.com/rust-lang/cargo/pull/14260)
- 使用 `Rc` 而非 `Arc` 存储 rustflags
  [#14273](https://github.com/rust-lang/cargo/pull/14273)
- 移除对 `--check-cfg` 支持的 rustc 探测 
  [#14302](https://github.com/rust-lang/cargo/pull/14302)
- 将所有与清单规范化相关的项从 'resolved' 重命名为 'normalized'。
  [#14342](https://github.com/rust-lang/cargo/pull/14342)
- cargo-util-schemas：添加 `TomlPackage::new`、`TomlWorkspace` 的 `Default`
  [#14271](https://github.com/rust-lang/cargo/pull/14271)
- ci：将 macos aarch64 切换到 nightly 
  [#14382](https://github.com/rust-lang/cargo/pull/14382)
- mdman：渲染选项时规范化换行 
  [#14428](https://github.com/rust-lang/cargo/pull/14428)
- perf：在无操作的 `source_id::with*` 中不调用 wrap
  [#14318](https://github.com/rust-lang/cargo/pull/14318)
- test：将更多测试迁移到 snapbox
  [#14242](https://github.com/rust-lang/cargo/pull/14242)
  [#14244](https://github.com/rust-lang/cargo/pull/14244)
  [#14293](https://github.com/rust-lang/cargo/pull/14293)
  [#14297](https://github.com/rust-lang/cargo/pull/14297)
  [#14319](https://github.com/rust-lang/cargo/pull/14319)
  [#14402](https://github.com/rust-lang/cargo/pull/14402)
  [#14410](https://github.com/rust-lang/cargo/pull/14410)
- test：不依赖缺少 `RUST_BACKTRACE`
  [#14441](https://github.com/rust-lang/cargo/pull/14441)
- test：在 AIX 上使用 gmake 
  [#14323](https://github.com/rust-lang/cargo/pull/14323)
- 更新到 `gix` 0.64.0 
  [#14332](https://github.com/rust-lang/cargo/pull/14332)
- 更新到 `rusqlite` 0.32.0 
  [#14334](https://github.com/rust-lang/cargo/pull/14334)
- 更新到 `windows-sys` 0.59
  [#14335](https://github.com/rust-lang/cargo/pull/14335)
- 更新依赖。
  [#14299](https://github.com/rust-lang/cargo/pull/14299)
  [#14303](https://github.com/rust-lang/cargo/pull/14303)
  [#14324](https://github.com/rust-lang/cargo/pull/14324)
  [#14329](https://github.com/rust-lang/cargo/pull/14329)
  [#14331](https://github.com/rust-lang/cargo/pull/14331)
  [#14391](https://github.com/rust-lang/cargo/pull/14391)

## Cargo 1.81 (2024-09-05)
[34a6a87d...rust-1.81.0](https://github.com/rust-lang/cargo/compare/34a6a87d...rust-1.81.0)

### 新增

### 变更

- ❗️ cargo-package：打包期间禁止 `package.license-file` 与 `package.readme` 指向
  不存在的文件。
  [#13921](https://github.com/rust-lang/cargo/pull/13921)
- ❗️ cargo-package：始终包含生成的 `.cargo_vcs_info.json`，
  即使传入了 `--allow-dirty`。
  [#13960](https://github.com/rust-lang/cargo/pull/13960)
- ❗️ 禁止将 `--release`/`--debug` 标志与 `--profile` 标志同时使用。
  [#13971](https://github.com/rust-lang/cargo/pull/13971)
- ❗️ 移除 Cargo.toml 中对 `lib.plugin` 键的支持。
  Rust 插件支持已弃用四年，并在 1.75.0 中移除。
  [#13902](https://github.com/rust-lang/cargo/pull/13902)
  [#14038](https://github.com/rust-lang/cargo/pull/14038)
- 使 rustc 的 `-Cmetadata` 计算在各平台上保持一致。
  [#14107](https://github.com/rust-lang/cargo/pull/14107)
- 即使未设置 MSRV，在未设置 `edition` 时也发出警告。
  [#14110](https://github.com/rust-lang/cargo/pull/14110)

### 修复

- 修复来自依赖的 proc-macro 示例影响 feature 解析。
  [#13892](https://github.com/rust-lang/cargo/pull/13892)
- 不要因使用 '..' 而对重复包发出警告。
  [#14234](https://github.com/rust-lang/cargo/pull/14234)
- 不要在每次加载 git 源时执行 `du`。
  [#14252](https://github.com/rust-lang/cargo/pull/14252)
- 不要对未引用的重复包发出警告 
  [#14239](https://github.com/rust-lang/cargo/pull/14239)
- cargo-publish：不要从发送到 registry 的 HTTP JSON 正文中，
  剥离已重命名依赖的非 dev feature。
  该缺陷仅影响第三方 registry。
  [#14328](https://github.com/rust-lang/cargo/pull/14328)
- cargo-vendor：vendor 时不要复制被排除的 Cargo 目标的源文件。
  [#14368](https://github.com/rust-lang/cargo/pull/14368)

### 仅 Nightly

- 🔥 `update-breaking`：为 `cargo update` 添加 `--breaking`，
  允许将依赖升级到破坏性版本。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#update-breaking)
  [#13979](https://github.com/rust-lang/cargo/pull/13979)
  [#14047](https://github.com/rust-lang/cargo/pull/14047)
  [#14049](https://github.com/rust-lang/cargo/pull/14049)
- `--artifact-dir`：将 `--out-dir` 重命名为 `--artifact-dir`。
  保留 `--out-dir` 标志以保持兼容，
  并可能在该功能稳定后移除。
  [#13809](https://github.com/rust-lang/cargo/pull/13809)
- `edition2024`：确保未使用的可选依赖对遮蔽依赖也会触发。
  [#14028](https://github.com/rust-lang/cargo/pull/14028)
- `edition2024`：解决隐式 → 显式 feature 迁移的问题 
  [#14018](https://github.com/rust-lang/cargo/pull/14018)
- `-Zcargo-lints`：将 `unknown_lints` 添加到 lints 列表。
  [#14024](https://github.com/rust-lang/cargo/pull/14024)
- `-Zcargo-lints`：添加用于文档化 lints 的工具。
  [#14025](https://github.com/rust-lang/cargo/pull/14025)
- `-Zcargo-lints`：保持 lints 更新并已排序。
  [#14030](https://github.com/rust-lang/cargo/pull/14030)
- `-Zconfig-include`：允许在配置中启用 `config-include` 功能。
  [#14196](https://github.com/rust-lang/cargo/pull/14196)
- `-Zpublic-dependency`：从解析器中移除一些遗留的公共依赖代码
  [#14090](https://github.com/rust-lang/cargo/pull/14090)
- `-Ztarget-applies-to-host`：使用 target-applies-to-host 时，将 rustflags 传给以隐式目标构建的产物
  [#13900](https://github.com/rust-lang/cargo/pull/13900)
  [#14201](https://github.com/rust-lang/cargo/pull/14201)
- cargo-update：跟踪 `--precise <prerelease>` 的行为。
  [#14013](https://github.com/rust-lang/cargo/pull/14013)

### 文档

- 澄清 `CARGO_CFG_TARGET_FAMILY` 是多值的。
  [#14165](https://github.com/rust-lang/cargo/pull/14165)
- 记录 `CARGO_CFG_TARGET_ABI`
  [#14164](https://github.com/rust-lang/cargo/pull/14164)
- 为每个清单字段与构建脚本调用记录 MSRV。
  [#14224](https://github.com/rust-lang/cargo/pull/14224)
- 移除重复的 `strip` 章节。 
  [#14146](https://github.com/rust-lang/cargo/pull/14146)
- 更新 Cargo 配置摘要以包含缺失的键。 
  [#14145](https://github.com/rust-lang/cargo/pull/14145)
- 更新 Cargo 文档索引。
  [#14228](https://github.com/rust-lang/cargo/pull/14228)
- 不要提及不存在的 `workspace.badges` 字段。
  [#14042](https://github.com/rust-lang/cargo/pull/14042)
- contrib：建议使用带独立测试提交的原子提交。
  [#14014](https://github.com/rust-lang/cargo/pull/14014)
- contrib：记录如何为 Cargo 撰写 RFC。
  [#14222](https://github.com/rust-lang/cargo/pull/14222)
- contrib：改进分流说明 
  [#14052](https://github.com/rust-lang/cargo/pull/14052)

### 内部

- cargo-package：更改打包期间的验证顺序。 
  [#14074](https://github.com/rust-lang/cargo/pull/14074)
- ci：添加自动发布 Cargo 的工作流 
  [#14202](https://github.com/rust-lang/cargo/pull/14202)
- ci：提升 CI 工具 
  [#14062](https://github.com/rust-lang/cargo/pull/14062)
  [#14257](https://github.com/rust-lang/cargo/pull/14257)
- registry：添加本地 registry overlay。
  [#13926](https://github.com/rust-lang/cargo/pull/13926)
- registry：将 `get_source_id` 移出 registry
  [#14218](https://github.com/rust-lang/cargo/pull/14218)
- resolver：简化依赖环检查 
  [#14089](https://github.com/rust-lang/cargo/pull/14089)
- rustfix：添加 `CodeFix::apply_solution` 并实现 `Clone` 
  [#14092](https://github.com/rust-lang/cargo/pull/14092)
- source：清理 `PathSource`/`RecursivePathSource` 拆分之后的内容
  [#14169](https://github.com/rust-lang/cargo/pull/14169)
  [#14231](https://github.com/rust-lang/cargo/pull/14231)
- 移除临时的 `__CARGO_GITOXIDE_DISABLE_LIST_FILES` 环境变量。
  [#14036](https://github.com/rust-lang/cargo/pull/14036)
- 简化 feature 语法检查 
  [#14106](https://github.com/rust-lang/cargo/pull/14106)
- 不要在热路径中新建常量 `InternedString` 
  [#14211](https://github.com/rust-lang/cargo/pull/14211)
- 使用 `std::fs::absolute` 而非重新实现它 
  [#14075](https://github.com/rust-lang/cargo/pull/14075)
- 从 cargo 中移除不必要的 feature 激活。
  [#14122](https://github.com/rust-lang/cargo/pull/14122)
  [#14160](https://github.com/rust-lang/cargo/pull/14160)
- 还原 #13630，因为 rustc 在 MSVC 上忽略 `-C strip`。
  [#14061](https://github.com/rust-lang/cargo/pull/14061)
- test：在 `user_specific_cfgs` 测试中允许 `unexpected_builtin_cfgs` lint 
  [#14153](https://github.com/rust-lang/cargo/pull/14153)
- test：将 cargo_test 添加到 test-support prelude 
  [#14243](https://github.com/rust-lang/cargo/pull/14243)
- test：将 Cargo 测试套件迁移到 `snapbox`。
  完整的迁移拉取请求列表见
  [#14039](https://github.com/rust-lang/cargo/issues/14039#issuecomment-2158974033)
- 更新到 `gix` 0.64.0 
  [#14431](https://github.com/rust-lang/cargo/pull/14431)
- 更新依赖。
  [#13995](https://github.com/rust-lang/cargo/pull/13995)
  [#13998](https://github.com/rust-lang/cargo/pull/13998)
  [#14037](https://github.com/rust-lang/cargo/pull/14037)
  [#14063](https://github.com/rust-lang/cargo/pull/14063)
  [#14067](https://github.com/rust-lang/cargo/pull/14067)
  [#14174](https://github.com/rust-lang/cargo/pull/14174)
  [#14186](https://github.com/rust-lang/cargo/pull/14186)
  [#14254](https://github.com/rust-lang/cargo/pull/14254)

## Cargo 1.80 (2024-07-25)
[b60a1555...rust-1.80.0](https://github.com/rust-lang/cargo/compare/b60a1555...rust-1.80.0)

### 新增

- 🎉 稳定化 `-Zcheck-cfg`！这默认启用 rustc 在编译时对
  条件编译的检查，验证 crate 是否正确
  处理不同目标平台或 feature 的条件编译。在内部，cargo 会向所有
  rustc 与 rustdoc 调用传递新的命令行选项
  `--check-cfg`。

  随此次稳定化新增构建脚本调用
  [`cargo::rustc-check-cfg=CHECK_CFG`](https://doc.rust-lang.org/nightly/cargo/reference/build-scripts.html#rustc-check-cfg)，
  作为向预期的 cfg 名称与值列表添加自定义 cfg 的方式。

  若你的包无法使用构建脚本，Cargo 提供配置
  [`[lints.rust.unexpected_cfgs.check-cfg]`](https://doc.rust-lang.org/nightly/rustc/check-cfg/cargo-specifics.html#check-cfg-in-lintsrust-table)
  以静态添加已知的自定义 cfg。

  ([RFC 3013](https://github.com/rust-lang/rfcs/blob/master/text/3013-conditional-compilation-checking.md))
  ([docs](https://doc.rust-lang.org/nightly/rustc/check-cfg/cargo-specifics.html))
  [#13571](https://github.com/rust-lang/cargo/pull/13571)
  [#13865](https://github.com/rust-lang/cargo/pull/13865)
  [#13869](https://github.com/rust-lang/cargo/pull/13869)
  [#13884](https://github.com/rust-lang/cargo/pull/13884)
  [#13913](https://github.com/rust-lang/cargo/pull/13913)
  [#13937](https://github.com/rust-lang/cargo/pull/13937)
  [#13958](https://github.com/rust-lang/cargo/pull/13958)

- 🎉 cargo-update：允许 `--precise` 指定已 yank 的包版本，
  并会相应更新 lockfile。
  [#13974](https://github.com/rust-lang/cargo/pull/13974)

### 变更

- ❗️ manifest：禁止 `[badges]` 从 `[workspace.package.badges]` 继承。
  这被视为缺陷。
  请注意 `[badges]` 实际上已弃用。
  [#13788](https://github.com/rust-lang/cargo/pull/13788)
- build-script：根据 MSRV 建议旧语法。
  [#13874](https://github.com/rust-lang/cargo/pull/13874)
- cargo-add：通过使用字符串字面量避免转义双引号。
  [#14006](https://github.com/rust-lang/cargo/pull/14006)
- cargo-clean：通过 `-p` 标志清理特定包的性能改进。
  [#13818](https://github.com/rust-lang/cargo/pull/13818)
- cargo-new：在库模板中使用 `i32` 而非 `usize` 作为“默认整数”。
  [#13939](https://github.com/rust-lang/cargo/pull/13939)
- cargo-package：打包期间若排除 Cargo 目标则警告而非失败。
  [#13713](https://github.com/rust-lang/cargo/pull/13713)
- manifest：对 `[lints]` 表中不支持的 lint 工具警告而非报错。
  [#13833](https://github.com/rust-lang/cargo/pull/13833)
- perf：在已知 Cargo 目标时避免推断。
  [#13849](https://github.com/rust-lang/cargo/pull/13849)
- 从 Rust 的源码 tar 包构建 Cargo 时填充 git 信息。
  [#13832](https://github.com/rust-lang/cargo/pull/13832)
- 改进从部分环境变量反序列化 Cargo 配置时的错误消息。
  [#13956](https://github.com/rust-lang/cargo/pull/13956)

### 修复

- resolver：使同名的路径依赖保持锁定。
  [#13572](https://github.com/rust-lang/cargo/pull/13572)
- cargo-add：在 Unix 上的 `write_atomic` 期间保留文件权限。
  [#13898](https://github.com/rust-lang/cargo/pull/13898)
- cargo-clean：在 Windows 上移除符号链接目录。
  [#13910](https://github.com/rust-lang/cargo/pull/13910)
- cargo-fix：不要修复进标准库。
  [#13792](https://github.com/rust-lang/cargo/pull/13792)
- cargo-fix：支持仅 IPv6 的网络。
  [#13907](https://github.com/rust-lang/cargo/pull/13907)
- cargo-new：当根目录是普通包时，不要说正在加入 workspace。
  [#13987](https://github.com/rust-lang/cargo/pull/13987)
- cargo-vendor：对忘记 vendor 的警告保持静默。
  [#13886](https://github.com/rust-lang/cargo/pull/13886)
- cargo-publish/cargo-vendor：确保生成的 Cargo.toml 中的目标顺序确定。
  [#13989](https://github.com/rust-lang/cargo/pull/13989)
  [#14004](https://github.com/rust-lang/cargo/pull/14004)
- cargo-credential-libsecret：按其 `SONAME` `libsecret-1.so.0` 加载 `libsecret`。
  [#13927](https://github.com/rust-lang/cargo/pull/13927)
- 别名不包含子命令时不要 panic。
  [#13819](https://github.com/rust-lang/cargo/pull/13819)
- 规避 macOS 上 ZFS 复制文件返回 EAGAIN。
  [#13845](https://github.com/rust-lang/cargo/pull/13845)
- 即使 GitHub 快速路径失败，也获取特定提交。
  [#13946](https://github.com/rust-lang/cargo/pull/13946)
  [#13969](https://github.com/rust-lang/cargo/pull/13969)
- 区分共享相同前缀但来自不同环境变量的 Cargo 配置。
  [#14000](https://github.com/rust-lang/cargo/pull/14000)

### 仅 Nightly

- `-Zcargo-lints`：不要总是继承 workspace lints。
  [#13812](https://github.com/rust-lang/cargo/pull/13812)
- `-Zcargo-lints`：添加测试以确保 cap-lints 可用。
  [#13829](https://github.com/rust-lang/cargo/pull/13829)
- `-Zcargo-lints`：指定了不稳定 lints 但未启用时报错。
  [#13805](https://github.com/rust-lang/cargo/pull/13805)
- `-Zcargo-lints`：将 cargo-lints 添加到不稳定文档。
  [#13881](https://github.com/rust-lang/cargo/pull/13881)
- `-Zcargo-lints`：重构 cargo lint 测试。
  [#13880](https://github.com/rust-lang/cargo/pull/13880)
- `-Zcargo-lints`：移除在 lint 名称中指定 `-` 的能力。
  [#13837](https://github.com/rust-lang/cargo/pull/13837)
- `-Zscript`：移除 cargo script 中被拒绝的不稳定 frontmatter 语法。
  现在唯一允许的 frontmatter 语法是 `---`。
  [#13861](https://github.com/rust-lang/cargo/pull/13861)
  [#13893](https://github.com/rust-lang/cargo/pull/13893)
- `-Zbindeps`：当有多种类型可用时，仅构建指定的 artifact 库。
  [#13842](https://github.com/rust-lang/cargo/pull/13842)
- `-Zmsrv-policy`：将未设置的 MSRV 视为兼容。
  [#13791](https://github.com/rust-lang/cargo/pull/13791)
- `-Zgit`/`-Zgitoxide`：默认配置从环境变量与 Cargo 配置两者获取。
  [#13687](https://github.com/rust-lang/cargo/pull/13687)
- `-Zpublic-dependency`：继承依赖时不要丢失 'public'。
  [#13836](https://github.com/rust-lang/cargo/pull/13836)
- `edition2024`：继承时禁止被忽略的 `default-features`。
  [#13839](https://github.com/rust-lang/cargo/pull/13839)
- `edition2024`：像其他 Cargo 目标一样校验 bin 的 crate-types/proc-macro。
  [#13841](https://github.com/rust-lang/cargo/pull/13841)

### 文档

- cargo-package：澄清不保证 VCS 出处。
  [#13984](https://github.com/rust-lang/cargo/pull/13984)
- cargo-metadata：澄清 Cargo 目标名称中的破折号替换规则。
  [#13887](https://github.com/rust-lang/cargo/pull/13887)
- config：修复构建脚本覆盖中 `rustc-flags` 的错误类型。
  [#13957](https://github.com/rust-lang/cargo/pull/13957)
- resolver：为 `resolver-tests` 添加 README。
  [#13977](https://github.com/rust-lang/cargo/pull/13977)
- contrib：更新贡献者指南中的 UI 示例代码。
  [#13864](https://github.com/rust-lang/cargo/pull/13864)
- 修复 libcurl 代理文档链接。
  [#13990](https://github.com/rust-lang/cargo/pull/13990)
- 为插件补充缺失的 `CARGO_MAKEFLAGS` 环境变量。
  [#13872](https://github.com/rust-lang/cargo/pull/13872)
- 在持续集成章节中包含 CircleCI 参考。
  [#13850](https://github.com/rust-lang/cargo/pull/13850)

### 内部

- ci：不要对照 beta 通道检查 `cargo`。
  [#13827](https://github.com/rust-lang/cargo/pull/13827)
- test：在 apache 容器中为 git 仓库设置 safe.directory。
  [#13920](https://github.com/rust-lang/cargo/pull/13920)
- test：对运行嵌入式单元测试的警告保持静默。
  [#13929](https://github.com/rust-lang/cargo/pull/13929)
- test：因 nightly rustc 变更更新测试格式。
  [#13890](https://github.com/rust-lang/cargo/pull/13890)
  [#13901](https://github.com/rust-lang/cargo/pull/13901)
  [#13964](https://github.com/rust-lang/cargo/pull/13964)
- test：使 `git::use_the_cli` 测试真正与 locale 无关。
  [#13935](https://github.com/rust-lang/cargo/pull/13935)
- cargo-test-support：将直接断言从 cargo-test-support 过渡到 snapbox。
  [#13980](https://github.com/rust-lang/cargo/pull/13980)
- cargo-test-support：自动遮盖经过时间。
  [#13973](https://github.com/rust-lang/cargo/pull/13973)
- cargo-test-support：清理不必要的 `match_exact` 使用。
  [#13879](https://github.com/rust-lang/cargo/pull/13879)
- 从 `PathSource` 拆分出 `RecursivePathSource`。
  [#13993](https://github.com/rust-lang/cargo/pull/13993)
- 因 libgit2 1.8 变更调整来自 cert-check 的自定义错误。
  [#13970](https://github.com/rust-lang/cargo/pull/13970)
- 将诊断打印移至 Shell。
  [#13813](https://github.com/rust-lang/cargo/pull/13813)
- 更新依赖。
  [#13834](https://github.com/rust-lang/cargo/pull/13834)
  [#13840](https://github.com/rust-lang/cargo/pull/13840)
  [#13948](https://github.com/rust-lang/cargo/pull/13948)
  [#13963](https://github.com/rust-lang/cargo/pull/13963)
  [#13976](https://github.com/rust-lang/cargo/pull/13976)

## Cargo 1.79 (2024-06-13)
[2fe739fc...rust-1.79.0](https://github.com/rust-lang/cargo/compare/2fe739fc...rust-1.79.0)

### 新增

- 🎉 `cargo add` 在添加新依赖时尊重 `package.rust-version`（亦即 MSRV）。
  可通过指定版本要求，或传入 `--ignore-rust-version` 标志覆盖该行为。
  ([RFC 3537](https://github.com/rust-lang/rfcs/blob/master/text/3537-msrv-resolver.md))
  [#13608](https://github.com/rust-lang/cargo/pull/13608)
- 新的 `Locking` 状态消息在任意命令上显示依赖变更。
  对 `cargo update`，还会告知是否有任何依赖版本过时。
  [#13561](https://github.com/rust-lang/cargo/pull/13561)
  [#13647](https://github.com/rust-lang/cargo/pull/13647)
  [#13651](https://github.com/rust-lang/cargo/pull/13651)
  [#13657](https://github.com/rust-lang/cargo/pull/13657)
  [#13759](https://github.com/rust-lang/cargo/pull/13759)
  [#13764](https://github.com/rust-lang/cargo/pull/13764)

### 变更

- ❗️ `RUSTC_WRAPPER`、`RUSTC_WORKSPACE_WRAPPER` 以及 `[env]`
  表中的变量，现在也应用于 Cargo 用于探测 rustc 信息的
  初始 `rustc -vV` 调用。
  [#13659](https://github.com/rust-lang/cargo/pull/13659)
- ❗️ 将形如 `foo = { optional = true }`、相当于 `version="*"` 的依赖
  从警告变为错误。
  该行为从一开始就被视为缺陷。
  [#13775](https://github.com/rust-lang/cargo/pull/13775)
- ❗️ 若从 `package.name` 推断 `lib.name`，也将破折号替换为下划线。
  此变更与文档行为对齐。需要注意的是，Cargo 发出的 JSON 消息，
  例如通过 `cargo metadata` 或 `--message-format=json`，
  将开始报告带下划线的 lib 名称。
  [#12783](https://github.com/rust-lang/cargo/pull/12783)
- 改用 `gitoxide` 列出文件。这改进了构建脚本与 `cargo doc`
  计算缓存新鲜度的性能，
  并修复了 `cargo publish` 的一些细微缺陷。
  [#13592](https://github.com/rust-lang/cargo/pull/13592)
  [#13696](https://github.com/rust-lang/cargo/pull/13696)
  [#13704](https://github.com/rust-lang/cargo/pull/13704)
  [#13777](https://github.com/rust-lang/cargo/pull/13777)
- 对传入且不再必要的 `-Zlints` 发出警告。
  [#13632](https://github.com/rust-lang/cargo/pull/13632)
- 对虚拟 workspace 上未使用的 `workspace.dependencies` 键发出警告。
  [#13664](https://github.com/rust-lang/cargo/pull/13664)
- 仅在 msrv 不兼容时发出 1.77 构建脚本语法错误。
  [#13808](https://github.com/rust-lang/cargo/pull/13808)
- 不对 `lints.rust.unexpected_cfgs.check-cfg` 发出警告。
  [#13925](https://github.com/rust-lang/cargo/pull/13925)
- cargo-init：若值可推断，则不在 Cargo.toml 中赋值 `target.name`。
  [#13606](https://github.com/rust-lang/cargo/pull/13606)
- cargo-package：规范化 `Cargo.toml` 中的路径，包括将 `\` 替换为 `/`。
  [#13729](https://github.com/rust-lang/cargo/pull/13729)
- cargo-test：将 cargo test 的 `--doc` 标志重新归类到“目标选择”下。
  [#13756](https://github.com/rust-lang/cargo/pull/13756)

### 修复

- 确保尊重 `--config net.git-fetch-with-cli=true`。
  [#13992](https://github.com/rust-lang/cargo/pull/13992)
  [#13997](https://github.com/rust-lang/cargo/pull/13997)
- 解析空别名时不要 panic。
  [#13613](https://github.com/rust-lang/cargo/pull/13613)
- 使用 `--target` 时，默认的 debuginfo strip 规则也同样适用。
  请注意，在 Windows MSVC 上 Cargo 默认不再 strip。
  [#13618](https://github.com/rust-lang/cargo/pull/13618)
- 不要在指向多字节字符的 Cargo.toml 解析错误上崩溃
  [#13780](https://github.com/rust-lang/cargo/pull/13780)
- 若 `.cargo/{config,config.toml}` 之一是指向另一个的符号链接，
  则不要发出弃用警告。
  [#13793](https://github.com/rust-lang/cargo/pull/13793)
- 检查 GitHub 上仓库是否最新时跟随 HTTP 重定向。
  [#13718](https://github.com/rust-lang/cargo/pull/13718)
- 在 `nounset` 模式下的 Bash 补全回退。
  [#13686](https://github.com/rust-lang/cargo/pull/13686)
- 当 rustflags 变更且传入了 `--target` 时重新运行构建脚本。
  [#13560](https://github.com/rust-lang/cargo/pull/13560)
- 修复推断名称中带破折号的 lib/bin 的文档冲突。
  [#13640](https://github.com/rust-lang/cargo/pull/13640)
- cargo-add：保持依赖 feature 的排序。
  [#13682](https://github.com/rust-lang/cargo/pull/13682)
- cargo-add：更新简单依赖时保留注释
  [#13655](https://github.com/rust-lang/cargo/pull/13655)
- cargo-fix：不要应用同一建议两次。
  [#13728](https://github.com/rust-lang/cargo/pull/13728)
- cargo-package：通过 `--package` 指定的包找不到时报错
  [#13735](https://github.com/rust-lang/cargo/pull/13735)
- credential-provider：修剪来自 stdin 的 token 中的换行。
  [#13770](https://github.com/rust-lang/cargo/pull/13770)

### 仅 Nightly

- 🔥 cargo-update：允许 `--precise` 指定包的预发布版本
  ([RFC 3493](https://github.com/rust-lang/rfcs/blob/master/text/3493-precise-pre-release-cargo-update.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#precise-pre-release))
  [#13626](https://github.com/rust-lang/cargo/pull/13626)
- RFC 3491：未使用依赖清理
  [#13778](https://github.com/rust-lang/cargo/pull/13778)
- `-Zcargo-lints`：为 Cargo 添加基本 lint 系统。
  仍在开发中，尚不可供一般使用。
  [#13621](https://github.com/rust-lang/cargo/pull/13621)
  [#13635](https://github.com/rust-lang/cargo/pull/13635)
  [#13797](https://github.com/rust-lang/cargo/pull/13797)
  [#13740](https://github.com/rust-lang/cargo/pull/13740)
  [#13801](https://github.com/rust-lang/cargo/pull/13801)
  [#13852](https://github.com/rust-lang/cargo/pull/13852)
  [#13853](https://github.com/rust-lang/cargo/pull/13853)
- 🔥 `edition2024`：为 resolver v3（感知 MSRV 的解析器）添加默认 Edition2024。
  [#13785](https://github.com/rust-lang/cargo/pull/13785)
- `edition2024`：在 2024 中移除下划线字段支持。
  [#13783](https://github.com/rust-lang/cargo/pull/13783)
  [#13798](https://github.com/rust-lang/cargo/pull/13798)
  [#13800](https://github.com/rust-lang/cargo/pull/13800)
  [#13804](https://github.com/rust-lang/cargo/pull/13804)
- `edition2024`：在 Edition 2024 中对 `[project]` 报错
  [#13747](https://github.com/rust-lang/cargo/pull/13747)
- `-Zmsrv-policy`：尊重 '--ignore-rust-version'
  [#13738](https://github.com/rust-lang/cargo/pull/13738)
- `-Zmsrv-policy`：为 update/generate-lockfile 添加 `--ignore-rust-version`
  [#13741](https://github.com/rust-lang/cargo/pull/13741)
  [#13742](https://github.com/rust-lang/cargo/pull/13742)
- `-Zmsrv-policy`：将感知 MSRV 的解析器置于配置之后
  [#13769](https://github.com/rust-lang/cargo/pull/13769)
- `-Zmsrv-policy`：对 rust-version 'x' 报错而非 panic
  [#13771](https://github.com/rust-lang/cargo/pull/13771)
- `-Zmsrv-policy`：MSRV 解析回退到 'rustc -V'。
  [#13743](https://github.com/rust-lang/cargo/pull/13743)
- `-Zmsrv-policy`：为感知 MSRV 的解析添加 v3 解析器
  [#13776](https://github.com/rust-lang/cargo/pull/13776)
- `-Zmsrv-policy`：对非本地安装不尊重 MSRV
  [#13790](https://github.com/rust-lang/cargo/pull/13790)
- `-Zmsrv-policy`：跟踪 MSRV 是否被显式设置（无论何种方式）
  [#13732](https://github.com/rust-lang/cargo/pull/13732)
- test：不要压缩测试 registry crate。
  [#13744](https://github.com/rust-lang/cargo/pull/13744)

### 文档

- 澄清 `--locked` 确保 Cargo 使用 lockfile 中的依赖版本
  [#13665](https://github.com/rust-lang/cargo/pull/13665)
- 澄清 `RUSTC_WORKSPACE_WRAPPER` 与 `RUSTC_WRAPPER` 的优先级。
  [#13648](https://github.com/rust-lang/cargo/pull/13648)
- 澄清仅在根 Cargo.toml 中允许 `[workspace]` 节。
  [#13753](https://github.com/rust-lang/cargo/pull/13753)
- 澄清虚拟清单与真实清单的区别。
  [#13794](https://github.com/rust-lang/cargo/pull/13794)

### 内部

- 🎉 新的成员 crate [`cargo-test-support`](https://crates.io/crates/cargo-test-support)
  与 [`cargo-test-macro`](https://crates.io/crates/cargo-test-macro)！
  它们专为测试 Cargo 自身而设计，
  因此不保证跨版本的任何稳定性。
  该 crate 在 crates.io 上的发布与其他成员 crate 相同。
  它们遵循 Rust 的 [6 周发布流程](https://doc.crates.io/contrib/process/release.html#cratesio-publishing)。
  [#13418](https://github.com/rust-lang/cargo/pull/13418)
- 因 crates.io CDN 变更修复发布脚本
  [#13614](https://github.com/rust-lang/cargo/pull/13614)
- 将诊断复杂度推给 annotate-snippets
  [#13619](https://github.com/rust-lang/cargo/pull/13619)
- cargo-package：简化获取已发布 Manifest
  [#13666](https://github.com/rust-lang/cargo/pull/13666)
- ci：将 macos 镜像更新到 macos-13
  [#13685](https://github.com/rust-lang/cargo/pull/13685)
- manifest：拆分出解析 `Cargo.toml` 的显式步骤
  [#13693](https://github.com/rust-lang/cargo/pull/13693)
- manifest：将目标发现与 Target 创建解耦
  [#13701](https://github.com/rust-lang/cargo/pull/13701)
- manifest：为 VirtualManifests 暴露 source/spans
  [#13603](https://github.com/rust-lang/cargo/pull/13603)
- 更新依赖
  [#13609](https://github.com/rust-lang/cargo/pull/13609)
  [#13674](https://github.com/rust-lang/cargo/pull/13674)
  [#13675](https://github.com/rust-lang/cargo/pull/13675)
  [#13679](https://github.com/rust-lang/cargo/pull/13679)
  [#13680](https://github.com/rust-lang/cargo/pull/13680)
  [#13692](https://github.com/rust-lang/cargo/pull/13692)
  [#13731](https://github.com/rust-lang/cargo/pull/13731)
  [#13760](https://github.com/rust-lang/cargo/pull/13760)
  [#13950](https://github.com/rust-lang/cargo/pull/13950)

## Cargo 1.78 (2024-05-02)
[7bb7b539...rust-1.78.0](https://github.com/rust-lang/cargo/compare/7bb7b539...rust-1.78.0)

### 新增

- 稳定化全局缓存数据跟踪。`-Zgc` 标志仍不稳定。
  这仅用于让 Cargo 开始收集数据，以便在自动 gc
  稳定后，不太可能看到缓存未命中。
  [#13492](https://github.com/rust-lang/cargo/pull/13492)
  [#13467](https://github.com/rust-lang/cargo/pull/13467)
- 稳定化锁文件格式 v4。锁文件 v3 仍是默认版本。
  [#12852](https://github.com/rust-lang/cargo/pull/12852)
- 自动检测输出是否可以使用非 ASCII Unicode 字符渲染。
  新增配置值 `term.unicode` 以手动控制该行为。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#termunicode)
  [#13337](https://github.com/rust-lang/cargo/pull/13337)
- 在 Cargo 配置中支持 `target.<triple>.rustdocflags`。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#targettriplerustdocflags)
  [#13197](https://github.com/rust-lang/cargo/pull/13197)

### 变更

- cargo-add：在创建依赖 feature 时打印状态
  [#13434](https://github.com/rust-lang/cargo/pull/13434)
- cargo-add：改进从被替换源添加包时的错误消息。
  [#13281](https://github.com/rust-lang/cargo/pull/13281)
- cargo-doc：在无 `--verbose` 时折叠 `Generated` 状态。
  [#13557](https://github.com/rust-lang/cargo/pull/13557)
- cargo-new：打印 'Creating' 状态，而非 'Created'
  [#13367](https://github.com/rust-lang/cargo/pull/13367)
- cargo-new：打印 note，而非 comment，以提供更多信息
  [#13371](https://github.com/rust-lang/cargo/pull/13371)
- cargo-new：在向工作区添加成员时打印提示
  [#13411](https://github.com/rust-lang/cargo/pull/13411)
- cargo-test：为 libtest 参数建议 `--` 
  [#13448](https://github.com/rust-lang/cargo/pull/13448)
- cargo-update：告知用户部分依赖仍落后于最新版本。
  [#13372](https://github.com/rust-lang/cargo/pull/13372)
- 弃用不带扩展名的 `.cargo/config` 文件。
  [#13349](https://github.com/rust-lang/cargo/pull/13349)
- 默认在失败时不打印 rustdoc 命令行
  [#13387](https://github.com/rust-lang/cargo/pull/13387)
- 生成新锁文件时尊重 `package.rust-version`。
  [#12861](https://github.com/rust-lang/cargo/pull/12861)
- 与远程注册表通信时发送 `User-Agent: cargo/1.2.3` 头。
  此前是 `cargo 1.2.3`，不符合 HTTP 规范。
  [#13548](https://github.com/rust-lang/cargo/pull/13548)
- 当 Cargo.toml 中缺少 `package.edition` 字段时发出警告。
  [#13499](https://github.com/rust-lang/cargo/pull/13499)
  [#13504](https://github.com/rust-lang/cargo/pull/13504)
  [#13505](https://github.com/rust-lang/cargo/pull/13505)
  [#13533](https://github.com/rust-lang/cargo/pull/13533)
- 从解析虚拟清单发出警告。
  [#13589](https://github.com/rust-lang/cargo/pull/13589)
- 在收集工作区成员时的错误消息中提及工作区根位置。
  [#13480](https://github.com/rust-lang/cargo/pull/13480)
- 在 `Finished` 状态消息中澄清所用的 profile。
  [#13422](https://github.com/rust-lang/cargo/pull/13422)
- 将更多 note/warning 改为小写。
  [#13410](https://github.com/rust-lang/cargo/pull/13410)
- 报告所有与 `package.rust-version.` 不兼容的包，而非随机一个。
  [#13514](https://github.com/rust-lang/cargo/pull/13514)

### 修复

- cargo-add：若 Cargo.toml 中不存在工作区，则不将新包添加到 `workspace.members`。
  [#13391](https://github.com/rust-lang/cargo/pull/13391)
- cargo-add：修复 cargo-add 中的 markdown 换行
  [#13400](https://github.com/rust-lang/cargo/pull/13400)
- cargo-run：使用 Package ID Spec 匹配包
  [#13335](https://github.com/rust-lang/cargo/pull/13335)
- cargo-doc：doctest 在构建脚本输出中搜索原生库。
  [#13490](https://github.com/rust-lang/cargo/pull/13490)
- cargo-publish：发布时也从 Cargo.toml 中剥离开发依赖的 features。
  [#13518](https://github.com/rust-lang/cargo/pull/13518)
- 通过 `cargo add/rm/init/new` 编辑 TOML 时不重复注释。
  [#13402](https://github.com/rust-lang/cargo/pull/13402)
- 修复稀疏索引被替换源的令人困惑的错误消息。
  [#13433](https://github.com/rust-lang/cargo/pull/13433)
- 在 '--list' 和 '-Zhelp' 中尊重 `CARGO_TERM_COLOR`。
  [#13479](https://github.com/rust-lang/cargo/pull/13479)
- 通过 `CARGO_TERM_COLOR` 控制 clap 错误与帮助文本的颜色。
  [#13463](https://github.com/rust-lang/cargo/pull/13463)
- Cargo.toml 中空 span 时不 panic。
  [#13375](https://github.com/rust-lang/cargo/pull/13375)
  [#13376](https://github.com/rust-lang/cargo/pull/13376)

### 仅 Nightly

- 🔥 cargo-update：允许 `--precise` 指定包的已 yank 版本
  [#13333](https://github.com/rust-lang/cargo/pull/13333)
- `-Zcheck-cfg`：将 `docsrs` cfg 添加为已知的 `--check-cfg`
  [#13383](https://github.com/rust-lang/cargo/pull/13383)
- `-Zcheck-cfg`：静默忽略 `cargo::rustc-check-cfg`，以避免在稳定化 `-Zcheck-cfg` 时造成 MSRV 困扰。
  [#13438](https://github.com/rust-lang/cargo/pull/13438)
- `-Zmsrv-policy`：未设置 MSRV 时回退到 `rustc -v` 
  [#13516](https://github.com/rust-lang/cargo/pull/13516)
- `-Zscript`：改进与 cargo script 相关的错误
  [#13346](https://github.com/rust-lang/cargo/pull/13346)
- `-Zpanic-abort-tests`：也适用于 doctest
  [#13388](https://github.com/rust-lang/cargo/pull/13388)
- `-Zpublic-dependency`：支持通过 `-Zpublic-dependency` 标志启用。
  [#13340](https://github.com/rust-lang/cargo/pull/13340)
  [#13556](https://github.com/rust-lang/cargo/pull/13556)
  [#13547](https://github.com/rust-lang/cargo/pull/13547)
- `-Zpublic-dependency`：测试打包公共依赖
  [#13536](https://github.com/rust-lang/cargo/pull/13536)
- `-Zrustdoc-map`：为 `doc.extern-map` 选项递归添加单元的所有子项 
  [#13481](https://github.com/rust-lang/cargo/pull/13481)
  [#13544](https://github.com/rust-lang/cargo/pull/13544)
- `edition2024`：启用 2024 edition 迁移。
  [#13429](https://github.com/rust-lang/cargo/pull/13429)
- `open-namespaces`：开放命名空间的基本支持
  ([RFC 3243](https://github.com/rust-lang/rfcs/blob/master/text/3243-packages-as-optional-namespaces.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#open-namespaces))
  [#13591](https://github.com/rust-lang/cargo/pull/13591)

### 文档

- cargo-fetch：在 `--offline` man page 中隐藏 `cargo-fetch` 递归链接。
  [#13364](https://github.com/rust-lang/cargo/pull/13364)
- cargo-install：`--list` 选项描述以大写开头
  [#13344](https://github.com/rust-lang/cargo/pull/13344)
- cargo-vendor：澄清 vendored 源为只读及修改它们的方式
  [#13512](https://github.com/rust-lang/cargo/pull/13512)
- build-script：澄清通过 `cargo::metadata=KEY=VALUE` 设置的构建脚本元数据。
  [#13436](https://github.com/rust-lang/cargo/pull/13436)
- 澄清 Cargo.toml 中 `[package]` 的 `version` 字段是可选的
  [#13390](https://github.com/rust-lang/cargo/pull/13390)
- 改进“Registry Authentication”文档
  [#13351](https://github.com/rust-lang/cargo/pull/13351)
- 改进“Specifying Dependencies”文档
  [#13341](https://github.com/rust-lang/cargo/pull/13341)
- 从“发布前”列表中移除 `package.documentation`。
  [#13398](https://github.com/rust-lang/cargo/pull/13398)

### 内部

- 🎉 集成 tracing-chrome 作为 Cargo 自身的基础分析器。
  [docs](https://doc.crates.io/contrib/tests/profiling.html)
  [#13399](https://github.com/rust-lang/cargo/pull/13399)
  [#13551](https://github.com/rust-lang/cargo/pull/13551)
- 更新至 `gix` 0.58.0
  [#13380](https://github.com/rust-lang/cargo/pull/13380)
- 更新至 `git2` 0.18.2
  [#13412](https://github.com/rust-lang/cargo/pull/13412)
- 更新至 `jobserver` 0.1.28 
  [#13419](https://github.com/rust-lang/cargo/pull/13419)
- 更新至 `supports-hyperlinks` 3.0.0
  [#13511](https://github.com/rust-lang/cargo/pull/13511)
- 更新至 `rusqlite` 0.31.0
  [#13510](https://github.com/rust-lang/cargo/pull/13510)
- bump-check：比较源代码时使用对称差
    [#13581](https://github.com/rust-lang/cargo/pull/13581)
- bump-check：包含 rustfix 与 cargo-util-schemas
    [#13421](https://github.com/rust-lang/cargo/pull/13421)
- ci：启用 m1 runner
  [#13377](https://github.com/rust-lang/cargo/pull/13377)
- ci：通过 `cargo-hack` 确保 MSRV 测试期间尊重锁文件。
  [#13523](https://github.com/rust-lang/cargo/pull/13523)
- cargo-util-schemas：通过 `RustVersion::is_compatible_with` 一致地比较 MSRV。
  [#13537](https://github.com/rust-lang/cargo/pull/13537)
- console：使用新的 fancy `anstyle` API
  [#13368](https://github.com/rust-lang/cargo/pull/13368)
  [#13562](https://github.com/rust-lang/cargo/pull/13562)
- fingerprint：移除 `Freshness::Dirty` 中不必要的 Option
  [#13361](https://github.com/rust-lang/cargo/pull/13361)
- fingerprint：从磁盘索引缓存中抽象掉 `std::fs`
  [#13515](https://github.com/rust-lang/cargo/pull/13515)
- mdman：更新至 `pulldown-cmark` 0.10.0
  [#13517](https://github.com/rust-lang/cargo/pull/13517)
- refactor：将 `Config` 重命名为 `GlobalContext` 
  [#13409](https://github.com/rust-lang/cargo/pull/13409)
  [#13486](https://github.com/rust-lang/cargo/pull/13486)
  [#13506](https://github.com/rust-lang/cargo/pull/13506)
- refactor：移除未使用的 `sysroot_host_libdir`。
  [#13468](https://github.com/rust-lang/cargo/pull/13468)
- refactor：向 Manifest 暴露 source/spans 以便发出 lint
  [#13593](https://github.com/rust-lang/cargo/pull/13593)
- refactor：扁平化清单解析 
  [#13589](https://github.com/rust-lang/cargo/pull/13589)
- refactor：使锁文件 diff/打印更可复用
  [#13564](https://github.com/rust-lang/cargo/pull/13564)
- test：更新至 `snapbox` 0.5.0
  [#13441](https://github.com/rust-lang/cargo/pull/13441)
- test：通过 snapbox 的 `term-svg` 功能验证终端样式。
  [#13461](https://github.com/rust-lang/cargo/pull/13461)
  [#13465](https://github.com/rust-lang/cargo/pull/13465)
  [#13520](https://github.com/rust-lang/cargo/pull/13520)
- test：确保 `nonzero_exit_code` 测试不受开发者 `RUST_BACKTRACE` 设置影响 
  [#13385](https://github.com/rust-lang/cargo/pull/13385)
- test：添加使用 worktree 的测试。
  [#13567](https://github.com/rust-lang/cargo/pull/13567)
- test：修复 old_cargos 测试 
  [#13435](https://github.com/rust-lang/cargo/pull/13435)
- test：因 rust-lang/rust 变更而修复测试。
  [#13362](https://github.com/rust-lang/cargo/pull/13362)
  [#13382](https://github.com/rust-lang/cargo/pull/13382)
  [#13415](https://github.com/rust-lang/cargo/pull/13415)
  [#13424](https://github.com/rust-lang/cargo/pull/13424)
  [#13444](https://github.com/rust-lang/cargo/pull/13444)
  [#13455](https://github.com/rust-lang/cargo/pull/13455)
  [#13464](https://github.com/rust-lang/cargo/pull/13464)
  [#13466](https://github.com/rust-lang/cargo/pull/13466)
  [#13469](https://github.com/rust-lang/cargo/pull/13469)
- test：禁用 lldb 测试，因其在 macOS 上需要特权才能运行 
  [#13416](https://github.com/rust-lang/cargo/pull/13416)

## Cargo 1.77.1 (2024-03-28)

### 修复

- 默认不再为 Windows MSVC 目标剥离 Debuginfo。这导致了 1.77.0 中意外的回归，破坏了回溯。
  [#13654](https://github.com/rust-lang/cargo/pull/13654)

## Cargo 1.77 (2024-03-21)
[1a2666dd...rust-1.77.0](https://github.com/rust-lang/cargo/compare/1a2666dd...rust-1.77.0)

### 新增

- 🎉 将包标识符格式稳定为 [Package ID Spec](https://doc.rust-lang.org/nightly/cargo/reference/pkgid-spec.html)。
  此格式可用于 Cargo 中的大多数命令，包括
  `--package`/`-p` 标志、`cargo pkgid`、`cargo metadata`，以及来自
  `--message-format=json` 的 JSON 消息。
  [#12914](https://github.com/rust-lang/cargo/pull/12914)
  [#13202](https://github.com/rust-lang/cargo/pull/13202)
  [#13311](https://github.com/rust-lang/cargo/pull/13311)
  [#13298](https://github.com/rust-lang/cargo/pull/13298)
  [#13322](https://github.com/rust-lang/cargo/pull/13322)
- 为 `-Zhelp` 控制台输出添加颜色
  [#13269](https://github.com/rust-lang/cargo/pull/13269)
- build script：用 `cargo::` 扩展构建指令语法。
  [#12201](https://github.com/rust-lang/cargo/pull/12201)
  [#13212](https://github.com/rust-lang/cargo/pull/13212)

### 变更

- 🎉 禁用 debuginfo 现在隐含 `strip = "debuginfo"`（当未设置 `strip` 时），
  以剥离来自标准库的既有 debuginfo，
  显著减小默认 release 二进制体积
  （在 Linux x64 上 helloworld 从约 ~4.5 MiB 降至约 ~450 KiB）。
  [#13257](https://github.com/rust-lang/cargo/pull/13257)
- 为清单解析添加 `rustc` 风格错误。
  [#13172](https://github.com/rust-lang/cargo/pull/13172)
- 在 cargo 中弃用 rustc plugin 支持
  [#13248](https://github.com/rust-lang/cargo/pull/13248)
- cargo-vendor：在 vendoring 时持有 mutate 排他锁。
  [#12509](https://github.com/rust-lang/cargo/pull/12509)
- crates-io：仅对带 body 载荷的请求设置 `Content-Type: application/json`
  [#13264](https://github.com/rust-lang/cargo/pull/13264)

### 修复

- jobserver：对所有种类的 runner 从环境继承 jobserver
  [#12776](https://github.com/rust-lang/cargo/pull/12776)
- build script：为所有带构建脚本的单元设置 `OUT_DIR`
  [#13204](https://github.com/rust-lang/cargo/pull/13204)
- cargo-add：从包含多个包的 Git 仓库中，按给定 features 找到正确的包。
  [#13213](https://github.com/rust-lang/cargo/pull/13213)
- cargo-fix：始终继承 jobserver
  [#13225](https://github.com/rust-lang/cargo/pull/13225)
- cargo-fix：减少调用 rustc 的次数以提升性能。
  [#13243](https://github.com/rust-lang/cargo/pull/13243)
- cargo-new：仅当新包是成员时才继承工作区 package 表
  [#13261](https://github.com/rust-lang/cargo/pull/13261)
- cargo-update：`--precise` 接受任意 git revision
  [#13250](https://github.com/rust-lang/cargo/pull/13250)
- manifest：为 lints 表提供未使用键警告
  [#13262](https://github.com/rust-lang/cargo/pull/13262)
- rustfix：支持插入新行。
  [#13226](https://github.com/rust-lang/cargo/pull/13226)

### 仅 Nightly

- 🔥 `-Zgit`：在不稳定标志后实现浅层 libgit2 fetch
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#git)
  [#13252](https://github.com/rust-lang/cargo/pull/13252)
- 🔥 为 `cargo rustdoc` 添加不稳定的 `--output-format` 选项，为工具提供
  依赖 rustdoc 实验性 JSON 格式的方式。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#output-format-for-rustdoc)
  [#12252](https://github.com/rust-lang/cargo/pull/12252)
  [#13284](https://github.com/rust-lang/cargo/pull/13284)
  [#13325](https://github.com/rust-lang/cargo/pull/13325)
- `-Zcheck-cfg`：重做 `--check-cfg` 生成注释
  [#13195](https://github.com/rust-lang/cargo/pull/13195)
- `-Zcheck-cfg`：在未声明 features 时恢复传递空的 `values()`
  [#13316](https://github.com/rust-lang/cargo/pull/13316)
- `-Zprecise-pre-release`：已添加该标志但尚未实现。
  [#13296](https://github.com/rust-lang/cargo/pull/13296)
  [#13320](https://github.com/rust-lang/cargo/pull/13320)
- `-Zpublic-dependency`：支持发布带 `public` 字段的包。
  [#13245](https://github.com/rust-lang/cargo/pull/13245)
- `-Zpublic-dependency`：`cargo add` 的 `--public`/`--no-public` 标志帮助文本
  [#13272](https://github.com/rust-lang/cargo/pull/13272)
- `-Zscript`：添加前缀字符 frontmatter 语法支持
  [#13247](https://github.com/rust-lang/cargo/pull/13247)
- `-Zscript`：添加多种实验性清单语法
  [#13241](https://github.com/rust-lang/cargo/pull/13241)
- `-Ztrim-paths`：仅重映射公共前缀
  [#13210](https://github.com/rust-lang/cargo/pull/13210)

### 文档

- 添加了关于在清单中设置 homepage 的指导
  [#13293](https://github.com/rust-lang/cargo/pull/13293)
- 澄清了自定义子命令的查找方式。
  [#13203](https://github.com/rust-lang/cargo/pull/13203)
- 澄清了为何 `du` 函数使用 mutex
  [#13273](https://github.com/rust-lang/cargo/pull/13273)
- 突出显示“How to find features enabled on dependencies”
  [#13305](https://github.com/rust-lang/cargo/pull/13305)
- 删除关于 license 中不支持括号的句子
  [#13292](https://github.com/rust-lang/cargo/pull/13292)
- resolver：澄清依赖解析中如何处理预发布版本。
  [#13286](https://github.com/rust-lang/cargo/pull/13286)
- cargo-test：澄清测试选项的目标选择。
  [#13236](https://github.com/rust-lang/cargo/pull/13236)
- cargo-install：澄清 `--path` 是安装源而非目标
  [#13205](https://github.com/rust-lang/cargo/pull/13205)
- contrib：修复团队 HackMD 链接
  [#13237](https://github.com/rust-lang/cargo/pull/13237)
- contrib：突出显示非阻塞 feature gating 技术
  [#13307](https://github.com/rust-lang/cargo/pull/13307)

### 内部

- 🎉 新成员 crate [`cargo-util-schemas`](https://crates.io/crates/cargo-util-schemas)！
  其中包含底层 Cargo schema 类型，专注于 `serde` 与 `FromStr`，
  用于读取文件与解析命令行。
  要从这些类型得到最终语义，很可能需要其他工具
  来处理，例如 `cargo metadata`。
  该 crate 在 crates.io 上的发布与其他成员 crate 相同。
  它遵循 Rust 的 [6 周发布流程](https://doc.crates.io/contrib/process/release.html#cratesio-publishing)。
  [#13178](https://github.com/rust-lang/cargo/pull/13178)
  [#13185](https://github.com/rust-lang/cargo/pull/13185)
  [#13186](https://github.com/rust-lang/cargo/pull/13186)
  [#13209](https://github.com/rust-lang/cargo/pull/13209)
  [#13267](https://github.com/rust-lang/cargo/pull/13267)
- 更新至 `gix` 0.57.1。
  [#13230](https://github.com/rust-lang/cargo/pull/13230)
- cargo-fix：移除 `cargo fix` 中的 error-format 特例
  [#13224](https://github.com/rust-lang/cargo/pull/13224)
- cargo-credential：升级至 0.4.3
  [#13221](https://github.com/rust-lang/cargo/pull/13221)
- mdman：更新至 `handlebars` 5.0.0。
  [#13168](https://github.com/rust-lang/cargo/pull/13168)
  [#13249](https://github.com/rust-lang/cargo/pull/13249)
- rustfix：移除无用的 clippy 规则并修复一处拼写错误
  [#13182](https://github.com/rust-lang/cargo/pull/13182)
- ci：修复 Dependabot 的 MSRV 自动更新
  [#13265](https://github.com/rust-lang/cargo/pull/13265)
  [#13324](https://github.com/rust-lang/cargo/pull/13324)
  [#13268](https://github.com/rust-lang/cargo/pull/13268)
- ci：添加 [dependency dashboard](https://github.com/rust-lang/cargo/issues/13256)。
  [#13255](https://github.com/rust-lang/cargo/pull/13255)
- ci：将 alpine docker 标签更新至 v3.19
  [#13228](https://github.com/rust-lang/cargo/pull/13228)
- ci：改进 GitHub Actions CI 配置
  [#13317](https://github.com/rust-lang/cargo/pull/13317)
- resolver：排序空 summaries 时不 panic
  [#13287](https://github.com/rust-lang/cargo/pull/13287)

## Cargo 1.76 (2024-02-08)
[6790a512...rust-1.76.0](https://github.com/rust-lang/cargo/compare/6790a512...rust-1.76.0)

### 新增

- 为 Windows MSVC 构建的 `cargo.exe` 添加 Windows 应用程序清单文件。
  [#13131](https://github.com/rust-lang/cargo/pull/13131)  
  显著变更：
  - 声明与 Windows 7、8、8.1、10 和 11 的兼容性。
  - 将代码页设置为 UTF-8。
  - 启用长路径感知。
- 为 `cargo --list` 添加彩色输出。
  [#12992](https://github.com/rust-lang/cargo/pull/12992)
- cargo-add：`--optional <dep>` 会创建 `<dep> = "dep:<dep>"` feature。
  [#13071](https://github.com/rust-lang/cargo/pull/13071)
- 扩展 Package ID spec 以支持无歧义规格。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/pkgid-spec.html)
  [#12933](https://github.com/rust-lang/cargo/pull/12933)  
  具体而言，
  - 支持 `git+` 与 `path+` 方案。
  - 支持 Git ref 查询字符串，例如 `?branch=dev` 或 `?tag=1.69.0`。

### 变更

- ❗️ 禁止在虚拟工作区中使用 `[lints]`，因为它们会被忽略，而用户很可能本意是 `[workspace.lints]`。
  这是初始实现中的疏忽（例如 `[dependencies]` 会产生相同错误）。
  [#13155](https://github.com/rust-lang/cargo/pull/13155)
- 在包 ID spec 与 `cargo new` 等多处禁止空名称。
  [#13152](https://github.com/rust-lang/cargo/pull/13152)
- 尊重 `rust-lang/rust` 的 `omit-git-hash` 选项。
  [#12968](https://github.com/rust-lang/cargo/pull/12968)
- 即使只有一个错误，也以数字显示错误计数。
  [#12484](https://github.com/rust-lang/cargo/pull/12484)
- `all-static` feature 现在包含 `vendored-libgit2`。
  [#13134](https://github.com/rust-lang/cargo/pull/13134)
- crates-io：与注册表交互时支持其他 2xx HTTP 状态码。
  [#13158](https://github.com/rust-lang/cargo/pull/13158)
  [#13160](https://github.com/rust-lang/cargo/pull/13160)
- home：用 SHGetKnownFolderPath 替换 SHGetFolderPathW。
  [#13173](https://github.com/rust-lang/cargo/pull/13173)

### 修复

- 在 wincon 上彩色打印 rustc 消息。
  [#13140](https://github.com/rust-lang/cargo/pull/13140)
- 修复含空格目录中的 bash 补全。
  [#13126](https://github.com/rust-lang/cargo/pull/13126)
- 修复在 Windows 上卸载正在运行的二进制失败。
  [#13053](https://github.com/rust-lang/cargo/pull/13053)
  [#13099](https://github.com/rust-lang/cargo/pull/13099)
- 修复重复链接的错误消息。
  [#12973](https://github.com/rust-lang/cargo/pull/12973)
- 修复与嵌套子命令一起使用 `--quiet`。
  [#12959](https://github.com/rust-lang/cargo/pull/12959)
- 修复开发依赖中存在环时的 panic。
  [#12977](https://github.com/rust-lang/cargo/pull/12977)
- 解析 rustc commit-hash 失败时不 panic。
  [#12963](https://github.com/rust-lang/cargo/pull/12963)
  [#12965](https://github.com/rust-lang/cargo/pull/12965)
- 更新工作区成员时不进行 git fetch。
  [#12975](https://github.com/rust-lang/cargo/pull/12975)
- 若 CACHEDIR.TAG 已存在则避免写入。
  [#13132](https://github.com/rust-lang/cargo/pull/13132)
- 若 `--package` 标志中的 `?` 是有效的 pkgid spec 则接受它。
  [#13315](https://github.com/rust-lang/cargo/pull/13315)
  [#13318](https://github.com/rust-lang/cargo/pull/13318)
- cargo-package：仅当 `target` 目录在包根目录中时才过滤掉它。
  [#12944](https://github.com/rust-lang/cargo/pull/12944)
- cargo-package：当构建脚本不存在或在包根目录外时报错。
  [#12995](https://github.com/rust-lang/cargo/pull/12995)
- cargo-credential-1password：为 `op signin` 命令添加缺失的 `--account` 参数。
  [#12985](https://github.com/rust-lang/cargo/pull/12985)
  [#12986](https://github.com/rust-lang/cargo/pull/12986)


### 仅 Nightly

- 🔥 `-Zgc` 标志为删除 cargo 缓存中旧的、未使用的文件启用垃圾回收。
  即 `CARGO_HOME` 目录下已下载的源文件与注册表索引。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#gc)
  [#12634](https://github.com/rust-lang/cargo/pull/12634)
  [#12958](https://github.com/rust-lang/cargo/pull/12958)
  [#12981](https://github.com/rust-lang/cargo/pull/12981)
  [#13055](https://github.com/rust-lang/cargo/pull/13055)
- 🔥 添加新的环境变量 `CARGO_RUSTC_CURRENT_DIR`。
  这是调用 rustc 时所在的路径。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/environment-variables.html?highlight=CARGO_RUSTC_CURRENT_DIR#environment-variables-cargo-sets-for-crates)
  [#12996](https://github.com/rust-lang/cargo/pull/12996)
- `-Zcheck-cfg`：在 `-Zcheck-cfg` 的 fingerprint 中包含已声明的 features 列表。
  [#13012](https://github.com/rust-lang/cargo/pull/13012)
- `-Zcheck-cfg`：修复零 features 时的 `--check-cfg` 调用。
  [#13011](https://github.com/rust-lang/cargo/pull/13011)
- `-Ztrim-paths`：为 `-Zbuild-std` 重排 `--remap-path-prefix` 标志。
  [#13065](https://github.com/rust-lang/cargo/pull/13065)
- `-Ztrim-paths`：通过使用 `.` 显式重映射当前目录。
  [#13114](https://github.com/rust-lang/cargo/pull/13114)
- `-Ztrim-paths`：用真实世界调试器进行演练。
  [#13091](https://github.com/rust-lang/cargo/pull/13091)
  [#13118](https://github.com/rust-lang/cargo/pull/13118)
- `-Zpublic-dependency`：将 `exported-private-dependencies` lint 限制为库。
  [#13135](https://github.com/rust-lang/cargo/pull/13135)
- `-Zpublic-dependency`：禁止通过工作区继承依赖的 public 状态。
  [#13125](https://github.com/rust-lang/cargo/pull/13125)
- `-Zpublic-dependency`：为 `cargo add` 添加 `--public`。
  [#13046](https://github.com/rust-lang/cargo/pull/13046)
- `-Zpublic-dependency`：移除未使用的 public-deps 错误处理 
  [#13036](https://github.com/rust-lang/cargo/pull/13036)
- `-Zmsrv-policy`：优先 MSRV，而非忽略不兼容项。
  [#12950](https://github.com/rust-lang/cargo/pull/12950)
- `-Zmsrv-policy`：在 MSRV 解析器中降低无 rust-version 的优先级。
  [#13066](https://github.com/rust-lang/cargo/pull/13066)
- `-Zrustdoc-scrape-examples`：抓取文档示例时不过滤工作区成员。
  [#13077](https://github.com/rust-lang/cargo/pull/13077)

### 文档

- 推荐更广泛的与 libsecret 兼容的密码管理器选择。
  [#12993](https://github.com/rust-lang/cargo/pull/12993)
- 澄清不同目标具有不同的 `CARGO_CFG_*` 值集合。
  [#13069](https://github.com/rust-lang/cargo/pull/13069)
- 澄清 `[lints]` 表仅影响当前包的本地开发。
  [#12976](https://github.com/rust-lang/cargo/pull/12976)
- 澄清 `cargo search` 可以在备用注册表中搜索。
  [#12962](https://github.com/rust-lang/cargo/pull/12962)
- 添加了验证 `rust-version`（MSRV）字段的常见 CI 实践。
  [#13056](https://github.com/rust-lang/cargo/pull/13056)
- 添加了指向 rustc lint 级别文档的链接。
  [#12990](https://github.com/rust-lang/cargo/pull/12990)
- 添加了从相关工作区表到包 lint 表的链接 
  [#13057](https://github.com/rust-lang/cargo/pull/13057)
- contrib：向 contrib 文档添加更多资源。
  [#13008](https://github.com/rust-lang/cargo/pull/13008)
- contrib：更新凭证 crate 的发布方式。 
  [#13006](https://github.com/rust-lang/cargo/pull/13006)
- contrib：移除评审容量通知。
  [#13070](https://github.com/rust-lang/cargo/pull/13070)

### 内部

- 🎉 将 `rustfix` crate 迁移到 `rust-lang/cargo` 仓库。
  [#13005](https://github.com/rust-lang/cargo/pull/13005)
  [#13042](https://github.com/rust-lang/cargo/pull/13042)
  [#13047](https://github.com/rust-lang/cargo/pull/13047)
  [#13048](https://github.com/rust-lang/cargo/pull/13048)
  [#13050](https://github.com/rust-lang/cargo/pull/13050)
- 更新至 `curl-sys` 0.4.70，对应 curl 8.4.0。
  [#13147](https://github.com/rust-lang/cargo/pull/13147)
- 更新至 `gix-index` 0.27.1。
  [#13148](https://github.com/rust-lang/cargo/pull/13148)
- 更新至 `itertools` 0.12.0。
  [#13086](https://github.com/rust-lang/cargo/pull/13086)
- 更新至 `rusqlite` 0.30.0。
  [#13087](https://github.com/rust-lang/cargo/pull/13087)
- 更新至 `toml_edit` 0.21.0。
  [#13088](https://github.com/rust-lang/cargo/pull/13088)
- 更新至 `windows-sys` 0.52.0。
  [#13089](https://github.com/rust-lang/cargo/pull/13089)
- 更新至 `tracing` 0.1.37 以与 rustc_log 兼容。
  [#13239](https://github.com/rust-lang/cargo/pull/13239)
  [#13242](https://github.com/rust-lang/cargo/pull/13242)
- 得益于更新到 `gix-config`，重新启用不稳定的 gitoxide auth 测试。
  [#13117](https://github.com/rust-lang/cargo/pull/13117)
  [#13129](https://github.com/rust-lang/cargo/pull/13129)
  [#13130](https://github.com/rust-lang/cargo/pull/13130)
- 自用 Cargo `-Zlints` 表功能。
  [#12178](https://github.com/rust-lang/cargo/pull/12178)
- 重构 `Cargo.toml` 解析代码，为提取官方 schema API 做准备。
  [#12954](https://github.com/rust-lang/cargo/pull/12954)
  [#12960](https://github.com/rust-lang/cargo/pull/12960)
  [#12961](https://github.com/rust-lang/cargo/pull/12961)
  [#12971](https://github.com/rust-lang/cargo/pull/12971)
  [#13000](https://github.com/rust-lang/cargo/pull/13000)
  [#13021](https://github.com/rust-lang/cargo/pull/13021)
  [#13080](https://github.com/rust-lang/cargo/pull/13080)
  [#13097](https://github.com/rust-lang/cargo/pull/13097)
  [#13123](https://github.com/rust-lang/cargo/pull/13123)
  [#13128](https://github.com/rust-lang/cargo/pull/13128)
  [#13154](https://github.com/rust-lang/cargo/pull/13154)
  [#13166](https://github.com/rust-lang/cargo/pull/13166)
- 在 `query{_vec}` 函数中使用 `IndexSummary`。
  [#12970](https://github.com/rust-lang/cargo/pull/12970)
- ci：迁移 renovate 配置 
  [#13106](https://github.com/rust-lang/cargo/pull/13106)
- ci：始终一起更新 gix 包 
  [#13093](https://github.com/rust-lang/cargo/pull/13093)
- ci：尽早捕获对 AtomicU64 的幼稚使用 
  [#12988](https://github.com/rust-lang/cargo/pull/12988)
- xtask-bump-check：不对 beta/stable 分支检查 `home` 
  [#13167](https://github.com/rust-lang/cargo/pull/13167)
- cargo-test-support：处理 JSON 诊断中的 $message_type 
  [#13016](https://github.com/rust-lang/cargo/pull/13016)
- cargo-test-support：为注册表测试支持添加更多选项。 
  [#13085](https://github.com/rust-lang/cargo/pull/13085)
- cargo-test-support：向默认 Cargo.toml 文件添加 features 
  [#12997](https://github.com/rust-lang/cargo/pull/12997)
- cargo-test-support：修复 clippy-wrapper 测试竞态条件。 
  [#12999](https://github.com/rust-lang/cargo/pull/12999)
- test：不依赖 mtime 来测试变更 
  [#13143](https://github.com/rust-lang/cargo/pull/13143)
- test：为 `optionals` 测试移除不必要的包与版本 
  [#13108](https://github.com/rust-lang/cargo/pull/13108)
- test：从测试中移除已删除的 feature `test_2018_feature`。
  [#13156](https://github.com/rust-lang/cargo/pull/13156)
- test：在某些测试中移除 jobserver 环境变量。
  [#13072](https://github.com/rust-lang/cargo/pull/13072)
- test：修复使用错误构建文件名的 rustflags 测试 
  [#12987](https://github.com/rust-lang/cargo/pull/12987)
- test：修复部分测试输出验证。 
  [#12982](https://github.com/rust-lang/cargo/pull/12982)
- test：在 windows-gnu 上忽略 changing_spec_relearns_crate_types 
  [#12972](https://github.com/rust-lang/cargo/pull/12972)

## Cargo 1.75 (2023-12-28)
[59596f0f...rust-1.75.0](https://github.com/rust-lang/cargo/compare/59596f0f...rust-1.75.0)

### 新增

- `Cargo.toml` 中的 `package.version` 字段现在是可选的，默认值为 `0.0.0`。
  没有 `package.version` 字段的包无法发布。
  [#12786](https://github.com/rust-lang/cargo/pull/12786)
- `--timings` 与 `cargo doc` 输出中的链接在受支持的终端上可点击，
  可通过 `term.hyperlinks` 配置值控制。
  [#12889](https://github.com/rust-lang/cargo/pull/12889)
- 使用 `-vv` 时打印构建脚本执行的环境变量。
  [#12829](https://github.com/rust-lang/cargo/pull/12829)
- cargo-new：自动将新包添加到 [workspace.members]。
  [#12779](https://github.com/rust-lang/cargo/pull/12779)
- cargo-doc：打印新的 `Generated` 状态，显示完整路径。
  [#12859](https://github.com/rust-lang/cargo/pull/12859)

### 变更

- cargo-new：若 crate 名称不遵循 snake_case 或 kebab-case 则警告。
  [#12766](https://github.com/rust-lang/cargo/pull/12766)
- cargo-install：澄清要安装的参数 `<crate>` 是位置参数。
  [#12841](https://github.com/rust-lang/cargo/pull/12841)
- cargo-install：在 MSRV 失败时建议替代版本。
  [#12798](https://github.com/rust-lang/cargo/pull/12798)
- cargo-install：报告更详细的 SemVer 错误。
  [#12924](https://github.com/rust-lang/cargo/pull/12924)
- cargo-install：若存在重复的 crate 则只安装一次。
  [#12868](https://github.com/rust-lang/cargo/pull/12868)
- cargo-remove：澄清不同依赖种类的标志行为。
  [#12823](https://github.com/rust-lang/cargo/pull/12823)
- cargo-remove：建议要移除的依赖仅存在于另一节中。
  [#12865](https://github.com/rust-lang/cargo/pull/12865)
- cargo-update：当差异仅在构建元数据时不称之为“Downgrading”。
  [#12796](https://github.com/rust-lang/cargo/pull/12796)
- 增强帮助文本以澄清 `--test` 标志针对 Cargo 目标，而非测试函数。
  [#12915](https://github.com/rust-lang/cargo/pull/12915)
- 在构建脚本警告中包含包名/版本。
  [#12799](https://github.com/rust-lang/cargo/pull/12799)
- 为错误的 -Z 标志提供后续步骤。
  [#12857](https://github.com/rust-lang/cargo/pull/12857)
- 当找不到 `cargo-<command>` 时建议 `cargo search`。
  [#12840](https://github.com/rust-lang/cargo/pull/12840)
- 不允许空的 feature 名称。
  [#12928](https://github.com/rust-lang/cargo/pull/12928)
- 为 `--target` 与 `--exclude` 标志添加不支持的短标志建议。
  [#12805](https://github.com/rust-lang/cargo/pull/12805)
- 为 `--out-dir` 标志添加不支持的短标志建议。
  [#12755](https://github.com/rust-lang/cargo/pull/12755)
- 为 `-Z` 标志添加不支持的小写 `-z` 标志建议。
  [#12788](https://github.com/rust-lang/cargo/pull/12788)
- 为不支持的 `--path` 标志添加更好的建议。
  [#12811](https://github.com/rust-lang/cargo/pull/12811)
- 当目标目录路径无效时添加详细消息。
  [#12820](https://github.com/rust-lang/cargo/pull/12820)

### 修复

- 修复 cargo 在写入文件时被杀死导致的损坏。
  [#12744](https://github.com/rust-lang/cargo/pull/12744)
- cargo-add：保留更多注释 
  [#12838](https://github.com/rust-lang/cargo/pull/12838)
- cargo-fix：在调用 rustc 时保留 jobserver 文件描述符。
  [#12951](https://github.com/rust-lang/cargo/pull/12951)
- cargo-remove：保留 feature 注释 
  [#12837](https://github.com/rust-lang/cargo/pull/12837)
- 错误发生时移除 timings HTML 报告中不必要的反斜杠。
  [#12934](https://github.com/rust-lang/cargo/pull/12934)
- 修复关于无效 feature 名称可包含 `-` 的错误消息。
  [#12939](https://github.com/rust-lang/cargo/pull/12939)
- 当锁文件中存在某依赖的某个版本时，
  Cargo 会使用该“精确”版本，包括构建元数据。
  [#12772](https://github.com/rust-lang/cargo/pull/12772)

### 仅 Nightly

- 添加了 `Edition2024` 不稳定功能。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#edition-2024)
  [#12771](https://github.com/rust-lang/cargo/pull/12771)
- 🔥 `-Ztrim-paths` 功能添加了新的 profile 设置，以控制结果二进制中路径的清理方式。
  ([RFC 3127](https://github.com/rust-lang/rfcs/blob/master/text/3127-trim-paths.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#profile-trim-paths-option))
  [#12625](https://github.com/rust-lang/cargo/pull/12625)
  [#12900](https://github.com/rust-lang/cargo/pull/12900)
  [#12908](https://github.com/rust-lang/cargo/pull/12908)
- `-Zcheck-cfg`：针对新的 rustc 语法与行为进行了调整。
  [#12845](https://github.com/rust-lang/cargo/pull/12845)
- `-Zcheck-cfg`：移除 `-Zcheck-cfg` 警告中过时的选项。
  [#12884](https://github.com/rust-lang/cargo/pull/12884)
- `public-dependency`：支持通过工作区依赖配置 `public` 依赖。
  [#12817](https://github.com/rust-lang/cargo/pull/12817)

### 文档

- profile：添加缺失的 `strip` 信息。
  [#12754](https://github.com/rust-lang/cargo/pull/12754)
- features：关于 feature 数量新限制的说明。
  [#12913](https://github.com/rust-lang/cargo/pull/12913)
- crates-io：为 `NewCrate` 结构体添加文档注释。
  [#12782](https://github.com/rust-lang/cargo/pull/12782)
- resolver：突出显示回答依赖解析问题的命令。
  [#12903](https://github.com/rust-lang/cargo/pull/12903)
- cargo-bench：`--bench` 无条件传递给 bench harness。
  [#12850](https://github.com/rust-lang/cargo/pull/12850)
- cargo-login：在 manpage 中提及 `--` 之后的参数。
  [#12832](https://github.com/rust-lang/cargo/pull/12832)
- cargo-vendor：澄清使用 vendored 源的配置会打印到 stdout 
  [#12893](https://github.com/rust-lang/cargo/pull/12893)
- manifest：更新至 SPDX 2.3 license 表达式与 3.20 license 列表。
  [#12827](https://github.com/rust-lang/cargo/pull/12827)
- contrib：清单编辑策略 
  [#12836](https://github.com/rust-lang/cargo/pull/12836)
- contrib：在 mdbook 搜索中使用 `AND` 搜索词并修复失效链接。
  [#12812](https://github.com/rust-lang/cargo/pull/12812)
  [#12813](https://github.com/rust-lang/cargo/pull/12813)
  [#12814](https://github.com/rust-lang/cargo/pull/12814)
- contrib：描述如何添加新包 
  [#12878](https://github.com/rust-lang/cargo/pull/12878)
- contrib：移除评审容量通知。
  [#12842](https://github.com/rust-lang/cargo/pull/12842)

### 内部

- 更新至 `itertools` 0.11.0。
  [#12759](https://github.com/rust-lang/cargo/pull/12759)
- 更新至 `cargo_metadata` 0.18.0。
  [#12758](https://github.com/rust-lang/cargo/pull/12758)
- 更新至 `curl-sys` 0.4.68，对应 curl 8.4.0。
  [#12808](https://github.com/rust-lang/cargo/pull/12808)
- 更新至 `toml` 0.8.2。
  [#12760](https://github.com/rust-lang/cargo/pull/12760)
- 更新至 `toml_edit` 0.20.2。
  [#12761](https://github.com/rust-lang/cargo/pull/12761)
- 更新 `gix` 至 0.55.2 
  [#12906](https://github.com/rust-lang/cargo/pull/12906)
- 在 windows-gnu 上禁用 `custom_target::custom_bin_target` 测试。
  [#12763](https://github.com/rust-lang/cargo/pull/12763)
- 重构 `Cargo.toml` 解析代码，为提取官方 schema API 做准备。
  [#12768](https://github.com/rust-lang/cargo/pull/12768)
  [#12881](https://github.com/rust-lang/cargo/pull/12881)
  [#12902](https://github.com/rust-lang/cargo/pull/12902)
  [#12911](https://github.com/rust-lang/cargo/pull/12911)
  [#12948](https://github.com/rust-lang/cargo/pull/12948)
- 将 SemVer 逻辑拆分到其自己的模块。
  [#12926](https://github.com/rust-lang/cargo/pull/12926)
  [#12940](https://github.com/rust-lang/cargo/pull/12940)
- source：为新的 `PackageIDSpec` 语法做准备
  [#12938](https://github.com/rust-lang/cargo/pull/12938)
- resolver：整合 `VersionPreferences` 中的逻辑 
  [#12930](https://github.com/rust-lang/cargo/pull/12930)
- 将 `SourceId::precise` 字段设为 Enum。
  [#12849](https://github.com/rust-lang/cargo/pull/12849)
- shell：一次写入而非分段写入。
  [#12880](https://github.com/rust-lang/cargo/pull/12880)
- 上移查看索引 summary 枚举 
  [#12749](https://github.com/rust-lang/cargo/pull/12749)
  [#12923](https://github.com/rust-lang/cargo/pull/12923)
- 在 CI 中为 Cargo Contributor Guide 生成重定向 HTML 页面。
  [#12846](https://github.com/rust-lang/cargo/pull/12846)
- 添加新的包缓存锁模式。
  [#12706](https://github.com/rust-lang/cargo/pull/12706)
- 为 issue 6915 添加回归测试：features 与传递开发依赖。
  [#12907](https://github.com/rust-lang/cargo/pull/12907)
- PR 评审状态变更时自动打标签。
  [#12856](https://github.com/rust-lang/cargo/pull/12856)
- credential：在所有已发布 crate 中包含 license 文件。
  [#12953](https://github.com/rust-lang/cargo/pull/12953)
- credential：按操作系统过滤 `cargo-credential-*` 依赖。
  [#12949](https://github.com/rust-lang/cargo/pull/12949)
- ci：将 cargo-semver-checks 升级至 0.24.0
  [#12795](https://github.com/rust-lang/cargo/pull/12795)
- ci：自动为 Cargo 的 crate 设置并验证所有 MSRV。
  [#12767](https://github.com/rust-lang/cargo/pull/12767)
  [#12654](https://github.com/rust-lang/cargo/pull/12654)
- ci：为发布 Cargo Contributor Book 使用单独的并发组。
  [#12834](https://github.com/rust-lang/cargo/pull/12834)
  [#12835](https://github.com/rust-lang/cargo/pull/12835)
- ci：将 `actions/checkout` action 更新至 v4
  [#12762](https://github.com/rust-lang/cargo/pull/12762)
- cargo-search：改进输出的边距计算。
  [#12890](https://github.com/rust-lang/cargo/pull/12890)

## Cargo 1.74 (2023-11-16)
[80eca0e5...rust-1.74.0](https://github.com/rust-lang/cargo/compare/80eca0e5...rust-1.74.0)

### 新增

- 🎉 `[lints]` 表已稳定，允许你在 `Cargo.toml` 中为 rustc 及其他工具 lint 配置报告级别。
  ([RFC 3389](https://github.com/rust-lang/rfcs/blob/master/text/3389-manifest-lint.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/manifest.html#the-lints-section))
  [#12584](https://github.com/rust-lang/cargo/pull/12584)
  [#12648](https://github.com/rust-lang/cargo/pull/12648)
- 🎉 不稳定功能 `credential-process` 与 `registry-auth` 已稳定。
  这些功能整合了与私有注册表进行身份验证的方式。
  ([RFC 2730](https://github.com/rust-lang/rfcs/blob/master/text/2730-cargo-token-from-process.md))
  ([RFC 3139](https://github.com/rust-lang/rfcs/blob/master/text/3139-cargo-alternative-registry-auth.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/registry-authentication.html))
  [#12590](https://github.com/rust-lang/cargo/pull/12590)
  [#12622](https://github.com/rust-lang/cargo/pull/12622)
  [#12623](https://github.com/rust-lang/cargo/pull/12623)
  [#12626](https://github.com/rust-lang/cargo/pull/12626)
  [#12641](https://github.com/rust-lang/cargo/pull/12641)
  [#12644](https://github.com/rust-lang/cargo/pull/12644)
  [#12649](https://github.com/rust-lang/cargo/pull/12649)
  [#12671](https://github.com/rust-lang/cargo/pull/12671)
  [#12709](https://github.com/rust-lang/cargo/pull/12709)  
  显著变更：
  - 引入新协议，供外部与内置提供者存储和检索注册表身份验证凭证。
  - 在注册表索引的 `config.json` 中添加 `auth-required` 字段，支持经身份验证的稀疏索引、crate 下载与搜索 API。
  - 使用带身份验证的备用注册表时，必须配置凭证提供者，以避免在不知情的情况下将未加密凭证存储在磁盘上。 
  - 这些设置可在 `[registry]` 与 `[registries]` 表中配置。
- 🎉 `--keep-going` 标志已稳定，现已在每个构建命令中可用
  （`bench` 与 `test` 除外，它们改为使用 `--no-fail-fast`）。
  ([docs](commands/cargo-build.md#option-cargo-build---keep-going))
  [#12568](https://github.com/rust-lang/cargo/pull/12568)
- 为 `cargo clean` 添加了 `--dry-run` 标志以及末尾的摘要行。
  [#12638](https://github.com/rust-lang/cargo/pull/12638)
- 为 cli 选项 `--dry-run` 添加了短别名 `-n`。 
  [#12660](https://github.com/rust-lang/cargo/pull/12660)
- 添加了对 `target.'cfg(..)'.linker` 的支持。
  [#12535](https://github.com/rust-lang/cargo/pull/12535)
- 允许在无歧义时对 `--package` 等标志使用不完整版本。
  [#12591](https://github.com/rust-lang/cargo/pull/12591)
  [#12614](https://github.com/rust-lang/cargo/pull/12614)
  [#12806](https://github.com/rust-lang/cargo/pull/12806)

### 变更

- ❗️ 更改了配置中数组合并的方式。
  顺序此前未指定，现在为保持一致性而遵循其他配置类型的工作方式。
  [summary](https://blog.rust-lang.org/inside-rust/2023/08/24/cargo-config-merging.html)
  [#12515](https://github.com/rust-lang/cargo/pull/12515)
- ❗️ cargo-clean：若 `--doc` 与 `-p` 混用则报错退出。
  [#12637](https://github.com/rust-lang/cargo/pull/12637)
- ❗ cargo-new / cargo-init 不再在库的 VCS ignore 文件中排除 `Cargo.lock`。
  [#12382](https://github.com/rust-lang/cargo/pull/12382)
- cargo-update：静默弃用 `--aggressive`，改用新的 `--recursive`。
  [#12544](https://github.com/rust-lang/cargo/pull/12544)
- cargo-update：`-p/--package` 可用作位置参数。
  [#12545](https://github.com/rust-lang/cargo/pull/12545)
  [#12586](https://github.com/rust-lang/cargo/pull/12586)
- cargo-install：当包名看起来像 URL 时建议 `--git`。
  [#12575](https://github.com/rust-lang/cargo/pull/12575)
- cargo-add：当 feature 列表过长时进行汇总。
  [#12662](https://github.com/rust-lang/cargo/pull/12662)
  [#12702](https://github.com/rust-lang/cargo/pull/12702)
- `--target` 的 Shell 补全使用 rustup，但回退到 rustc。
  [#12606](https://github.com/rust-lang/cargo/pull/12606)
- 帮助用户了解可能的 `--target` 值。
  [#12607](https://github.com/rust-lang/cargo/pull/12607)
- 增强“registry index not found”错误消息。
  [#12732](https://github.com/rust-lang/cargo/pull/12732)
- 增强 `--explain` 的 CLI 帮助消息。 
  [#12592](https://github.com/rust-lang/cargo/pull/12592)
- 使用 `serde-untagged` 增强无标签枚举的反序列化错误。
  [#12574](https://github.com/rust-lang/cargo/pull/12574)
  [#12581](https://github.com/rust-lang/cargo/pull/12581)
- 增强预发布版本候选不匹配时的错误。
  [#12659](https://github.com/rust-lang/cargo/pull/12659)
- 增强对有歧义 Package ID spec 的建议。
  [#12685](https://github.com/rust-lang/cargo/pull/12685)
- 增强 TOML 解析错误以显示上下文。
  [#12556](https://github.com/rust-lang/cargo/pull/12556)
- 通过在 `std::fs::metadata` 周围添加包装器来增强文件系统错误。
  [#12636](https://github.com/rust-lang/cargo/pull/12636)
- 增强解析器版本不匹配警告。
  [#12573](https://github.com/rust-lang/cargo/pull/12573)
- 使用 clap 为不支持的参数建议替代参数。
  [#12529](https://github.com/rust-lang/cargo/pull/12529)
  [#12693](https://github.com/rust-lang/cargo/pull/12693)
  [#12723](https://github.com/rust-lang/cargo/pull/12723)
- 从 cargo new/init `--help` 输出中移除冗余信息。
  [#12594](https://github.com/rust-lang/cargo/pull/12594)
- 控制台输出与样式微调。
  [#12578](https://github.com/rust-lang/cargo/pull/12578)
  [#12655](https://github.com/rust-lang/cargo/pull/12655)
  [#12593](https://github.com/rust-lang/cargo/pull/12593)

### 修复

- 对 `cargo rustc --print --target` 使用完整目标规格。
  [#12743](https://github.com/rust-lang/cargo/pull/12743)
- 也为 EFI 目标复制 PDB。
  [#12688](https://github.com/rust-lang/cargo/pull/12688)
- 修复解析器行为与包顺序无关。
  [#12602](https://github.com/rust-lang/cargo/pull/12602)
- 修复 `cargo remove` 对 `profile.release.package."*"` 的不必要清理。
  [#12624](https://github.com/rust-lang/cargo/pull/12624)

### 仅 Nightly

- `-Zasymmetric-token`：为 asymmetric-token 支持创建专用不稳定标志。
  [#12551](https://github.com/rust-lang/cargo/pull/12551)
- `-Zasymmetric-token`：改进非对称令牌的注销消息。
  [#12587](https://github.com/rust-lang/cargo/pull/12587)
- `-Zmsrv-policy`：**非常**初步的 MSRV 解析器支持。
  [#12560](https://github.com/rust-lang/cargo/pull/12560)
- `-Zscript`：临时加入代码围栏支持。
  [#12681](https://github.com/rust-lang/cargo/pull/12681)
- `-Zbindeps`：支持来自注册表的依赖。
  [#12421](https://github.com/rust-lang/cargo/pull/12421)

### 文档

- ❗ 策略变更：将 `Cargo.lock` 纳入版本控制现在是默认选择，
  即使对于库也是如此。锁文件与 CI 集成文档也已扩充。
  [Policy docs](https://doc.rust-lang.org/nightly/cargo/faq.html#why-have-cargolock-in-version-control),
  [Lockfile docs](https://doc.rust-lang.org/nightly/cargo/guide/cargo-toml-vs-cargo-lock.html),
  [CI docs](https://doc.rust-lang.org/nightly/cargo/guide/continuous-integration.html),
  [#12382](https://github.com/rust-lang/cargo/pull/12382)
  [#12630](https://github.com/rust-lang/cargo/pull/12630)
- SemVer：更新关于移除可选依赖的文档。
  [#12687](https://github.com/rust-lang/cargo/pull/12687)
- Contrib：添加安全响应流程。
  [#12487](https://github.com/rust-lang/cargo/pull/12487)
- cargo-publish：警告上传超时。
  [#12733](https://github.com/rust-lang/cargo/pull/12733)
- mdbook：有多个词时使用 *AND* 搜索。
  [#12548](https://github.com/rust-lang/cargo/pull/12548)
- 确立发布最佳实践 
  [#12745](https://github.com/rust-lang/cargo/pull/12745)
- 澄清 caret 要求。
  [#12679](https://github.com/rust-lang/cargo/pull/12679)
- 澄清 `version` 对 `git` 依赖如何工作。
  [#12270](https://github.com/rust-lang/cargo/pull/12270)
- 澄清并区分 split-debuginfo 的默认值。
  [#12680](https://github.com/rust-lang/cargo/pull/12680)
- 在 `dev` 与 `release` profile 中添加缺失的 `strip` 条目。
  [#12748](https://github.com/rust-lang/cargo/pull/12748)

### 内部

- 更新至 `curl-sys` 0.4.66，对应 curl 8.3.0。
  [#12718](https://github.com/rust-lang/cargo/pull/12718)
- 更新至 `gitoxide` 0.54.1。
  [#12731](https://github.com/rust-lang/cargo/pull/12731)
- 更新至 `git2` 0.18.0，对应 libgit2 1.7.1。
  [#12580](https://github.com/rust-lang/cargo/pull/12580)
- 更新至 `cargo_metadata` 0.17.0。
  [#12758](https://github.com/rust-lang/cargo/pull/12610)
- 更新目标架构感知 crate 以支持 mips r6 目标 
  [#12720](https://github.com/rust-lang/cargo/pull/12720)
- publish.py：移除过时的 `sleep()` 调用。
  [#12686](https://github.com/rust-lang/cargo/pull/12686)
- 定义 `{{command}}` 供 src/doc/man/includes 使用 
  [#12570](https://github.com/rust-lang/cargo/pull/12570)
- 为网络消息设置 tracing 目标 `network`。
  [#12582](https://github.com/rust-lang/cargo/pull/12582)
- cargo-test-support：添加 `with_stdout_unordered`。
  [#12635](https://github.com/rust-lang/cargo/pull/12635)
- dep：从 `termcolor` 切换到 `anstream`。
  [#12751](https://github.com/rust-lang/cargo/pull/12751)
- 将 `Source` trait 置于 `cargo::sources` 下。
  [#12527](https://github.com/rust-lang/cargo/pull/12527)
- SourceId：将 `name` 与 `alt_registry_key` 合并为一个枚举。
  [#12675](https://github.com/rust-lang/cargo/pull/12675)
- TomlManifest：当 package_root 不是目录时失败。
  [#12722](https://github.com/rust-lang/cargo/pull/12722)
- util：增强 `network::retry` 文档。
  [#12583](https://github.com/rust-lang/cargo/pull/12583)
- refactor：抽出 cargo-add MSRV 代码以便复用 
  [#12553](https://github.com/rust-lang/cargo/pull/12553)
- refactor(install)：将值解析移至 clap 
  [#12547](https://github.com/rust-lang/cargo/pull/12547)
- 修复网络测试中的虚假错误。 
  [#12726](https://github.com/rust-lang/cargo/pull/12726)
- 对 `CARGO_LOG` 内部日志使用更紧凑的相对时间格式。
  [#12542](https://github.com/rust-lang/cargo/pull/12542)
- 使用更新的 std API 以获得更清晰的代码。
  [#12559](https://github.com/rust-lang/cargo/pull/12559)
  [#12604](https://github.com/rust-lang/cargo/pull/12604)
  [#12615](https://github.com/rust-lang/cargo/pull/12615)
  [#12631](https://github.com/rust-lang/cargo/pull/12631)
- 缓冲控制台状态消息。 
  [#12727](https://github.com/rust-lang/cargo/pull/12727)
- 使用枚举描述索引 summaries，以便在解析时 summaries 不可用时提供更丰富的信息。
  [#12643](https://github.com/rust-lang/cargo/pull/12643)
- 使用最短路径解析从给定依赖到根的路径。
  [#12678](https://github.com/rust-lang/cargo/pull/12678)
- 在同一位置读/写编码后的 `cargo update --precise` 
  [#12629](https://github.com/rust-lang/cargo/pull/12629)
- 为内部包设置 MSRV。
  [#12381](https://github.com/rust-lang/cargo/pull/12381)
- ci：更新 Renovate schema 
  [#12741](https://github.com/rust-lang/cargo/pull/12741)
- ci：在 MSRV 中忽略补丁版本 
  [#12716](https://github.com/rust-lang/cargo/pull/12716)

## Cargo 1.73 (2023-10-05)
[45782b6b...rust-1.73.0](https://github.com/rust-lang/cargo/compare/45782b6b...rust-1.73.0)

### 新增

- 在额外详细模式 `-vv` 下为 `cargo run/bench/test` 打印环境变量。
  [#12498](https://github.com/rust-lang/cargo/pull/12498)
- 在 Cargo timings 图上显示包版本。
  [#12420](https://github.com/rust-lang/cargo/pull/12420)

### 变更

- ❗️ Cargo 现在在自定义构建脚本中使用 `cargo::` 时会退出。这是
  为即将到来的构建脚本调用变更做准备。
  [#12332](https://github.com/rust-lang/cargo/pull/12332)
- ❗️ `cargo login` 不再接受 `--` 语法之后的任何令牌。
  `--` 之后的参数现在被保留，为新的凭证提供者功能做准备。
  这引入了一项回归：忽略了先前版本中对 `cargo login -- <token>` 的支持。
  [#12499](https://github.com/rust-lang/cargo/pull/12499)
- 使 Cargo `--help` 更易于浏览。
  [#11905](https://github.com/rust-lang/cargo/pull/11905)
- 若 `cargo test` 进程通过信号终止，则提示使用 `--nocapture` 标志。
  [#12463](https://github.com/rust-lang/cargo/pull/12463)
- 在获取目标信息的 rustc 调用上保留 jobserver 文件描述符。
  [#12447](https://github.com/rust-lang/cargo/pull/12447)
- 在 `--help` 中澄清 `cargo test --all-targets` 排除 doctest。
  [#12422](https://github.com/rust-lang/cargo/pull/12422)
- 发布时将 `cargo.toml` 规范为 `Cargo.toml`，并在其他 `Cargo.toml` 大小写情况下发出警告。
  [#12399](https://github.com/rust-lang/cargo/pull/12399)

### 修复

- 仅在 `~/.cargo/{git,registry}` 上跳过 mtime 检查。
  [#12369](https://github.com/rust-lang/cargo/pull/12369)
- 修复 WSL2 上 `cargo doc --open` 崩溃。
  [#12373](https://github.com/rust-lang/cargo/pull/12373)
- 修复对某些字符串启用 `http.debug` 时的 panic。
  [#12468](https://github.com/rust-lang/cargo/pull/12468)
- 修复 `cargo remove` 错误地移除仍在使用的 patches。
  [#12454](https://github.com/rust-lang/cargo/pull/12454)
- 修复 crate 校验和查找查询应匹配 semver 构建元数据。
  [#11447](https://github.com/rust-lang/cargo/pull/11447)
- 修复为 `[registries]` 表中未使用字段打印多条警告消息。
  [#12439](https://github.com/rust-lang/cargo/pull/12439)

### 仅 Nightly

- 🔥 `-Zcredential-process` 已用更清晰的方式重新实现，以便
  与不同的凭证提供者通信。若干内置提供者也
  已添加到 Cargo。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#credential-process)
  [#12334](https://github.com/rust-lang/cargo/pull/12334)
  [#12396](https://github.com/rust-lang/cargo/pull/12396)
  [#12424](https://github.com/rust-lang/cargo/pull/12424)
  [#12440](https://github.com/rust-lang/cargo/pull/12440)
  [#12461](https://github.com/rust-lang/cargo/pull/12461)
  [#12469](https://github.com/rust-lang/cargo/pull/12469)
  [#12483](https://github.com/rust-lang/cargo/pull/12483)
  [#12499](https://github.com/rust-lang/cargo/pull/12499)
  [#12507](https://github.com/rust-lang/cargo/pull/12507)
  [#12512](https://github.com/rust-lang/cargo/pull/12512)
  [#12518](https://github.com/rust-lang/cargo/pull/12518)
  [#12521](https://github.com/rust-lang/cargo/pull/12521)
  [#12526](https://github.com/rust-lang/cargo/pull/12526)  
  一些显著变更：
  - 在 Cargo 配置中将 `credential-process` 重命名为 `credential-provider`。
  - 通过 stdin/stdout 与外部凭证提供者通信的新 JSON 协议。
  - GNOME Secret 提供者现在动态加载 `libsecert`。
  - 1password 提供者不再内置。
  - 将非对称令牌的不稳定键从 `registry-auth` 更改为 `credential-process`。
- ❗️ 从 `cargo test` 与 `cargo bench` 中移除 `--keep-going` 标志支持。
  [#12478](https://github.com/rust-lang/cargo/pull/12478)
  [#12492](https://github.com/rust-lang/cargo/pull/12492)
- 修复由 `-Zscript` 生成的无效包名。
  [#12349](https://github.com/rust-lang/cargo/pull/12349)
- `-Zscript` 现在对不支持的命令——`publish` 与 `package`——报错退出。
  [#12350](https://github.com/rust-lang/cargo/pull/12350)
- 在 Cargo.lock 中为 source ID 正确编码 URL 参数。
  [#12280](https://github.com/rust-lang/cargo/pull/12280)
- 用 `panic-unwind` 替换无效的 `panic_unwind` std feature。
  [#12364](https://github.com/rust-lang/cargo/pull/12364)
- `-Zlints`：doctest 提取应尊重 `[lints]`。
  [#12501](https://github.com/rust-lang/cargo/pull/12501)

### 文档

- SemVer：添加关于更改定义良好类型的对齐、布局或大小的章节。
  [#12169](https://github.com/rust-lang/cargo/pull/12169)
- 使用标题属性控制 fragment。
  [#12339](https://github.com/rust-lang/cargo/pull/12339)
- 在解释 Cargo 对 semver 的使用时用“number”代替“digit”。
  [#12340](https://github.com/rust-lang/cargo/pull/12340)
- contrib：添加关于发布如何工作的更多细节。
  [#12344](https://github.com/rust-lang/cargo/pull/12344)
- 澄清 `cargo metadata` 中的“Package ID”与“Source ID”是不透明字符串。
  [#12313](https://github.com/rust-lang/cargo/pull/12313)
- 澄清 `rerun-if-env-changed` 不会监视其为 crate 与构建脚本
  设置的环境变量。
  [#12482](https://github.com/rust-lang/cargo/pull/12482)
- 澄清仅在元数据标签上不同的多个版本
  在 crates.io 上是不允许的。
  [#12335](https://github.com/rust-lang/cargo/pull/12335)
- 澄清 `lto` 设置传递 `-Clinker-plugin-lto`。
  [#12407](https://github.com/rust-lang/cargo/pull/12407)
- 在配置与环境变量文档中添加了 `profile.strip`。
  [#12337](https://github.com/rust-lang/cargo/pull/12337)
  [#12408](https://github.com/rust-lang/cargo/pull/12408)
- 添加了 artifact JSON debuginfo 级别的文档。
  [#12376](https://github.com/rust-lang/cargo/pull/12376)
- 添加了关于向后兼容的 `.cargo/credential` 文件存在的通知。
  [#12479](https://github.com/rust-lang/cargo/pull/12479)
- 提高对工作区内使用 `resolver = 2` 的认识。
  [#12388](https://github.com/rust-lang/cargo/pull/12388)
- 在文档中用默认分支替换 `master` 分支。
  [#12435](https://github.com/rust-lang/cargo/pull/12435)

### 内部

- 更新至 `criterion` 0.5.1。
  [#12338](https://github.com/rust-lang/cargo/pull/12338)
- 更新至 `curl-sys` 0.4.65，对应 curl 8.2.1。
  [#12406](https://github.com/rust-lang/cargo/pull/12406)
- 更新至 `indexmap` v2。
  [#12368](https://github.com/rust-lang/cargo/pull/12368)
- 更新至 `miow` 0.6.0，其移除了旧版本的 `windows-sys`。
  [#12453](https://github.com/rust-lang/cargo/pull/12453)
- ci：通过使用 `--workspace` 自动测试新包。
  [#12342](https://github.com/rust-lang/cargo/pull/12342)
- ci：使用 Renovate 每月自动更新依赖。
  [#12341](https://github.com/rust-lang/cargo/pull/12341)
  [#12466](https://github.com/rust-lang/cargo/pull/12466)
- ci：重写 `xtask-bump-check`，通过采用 `cargo-semver-checks` 以尊重 semver。
  [#12395](https://github.com/rust-lang/cargo/pull/12395)
  [#12513](https://github.com/rust-lang/cargo/pull/12513)
  [#12508](https://github.com/rust-lang/cargo/pull/12508)
- 重新排列并重命名测试目录
  [#12397](https://github.com/rust-lang/cargo/pull/12397)
  [#12398](https://github.com/rust-lang/cargo/pull/12398)
- 从 `log` 迁移到 `tracing`。
  [#12458](https://github.com/rust-lang/cargo/pull/12458)
  [#12488](https://github.com/rust-lang/cargo/pull/12488)
- 在测试中跟踪 `--help` 输出。
  [#11912](https://github.com/rust-lang/cargo/pull/11912)
- 清理并在工作区内共享包元数据。
  [#12352](https://github.com/rust-lang/cargo/pull/12352)
- `crates-io`：暴露 HTTP 头与 `Error` 类型。
  [#12310](https://github.com/rust-lang/cargo/pull/12310)
- 对于 `cargo update`，在 clap 中捕获 `--aggressive` 与 `--precise` 之间的 CLI 标志冲突。
  [#12428](https://github.com/rust-lang/cargo/pull/12428)
- 若干修复，以使 Cargo 测试套件在 nightly 或 `rust-lang/rust` 中通过。
  [#12413](https://github.com/rust-lang/cargo/pull/12413)
  [#12416](https://github.com/rust-lang/cargo/pull/12416)
  [#12429](https://github.com/rust-lang/cargo/pull/12429)
  [#12450](https://github.com/rust-lang/cargo/pull/12450)
  [#12491](https://github.com/rust-lang/cargo/pull/12491)
  [#12500](https://github.com/rust-lang/cargo/pull/12500)

## Cargo 1.72 (2023-08-24)
[64fb38c9...rust-1.72.0](https://github.com/rust-lang/cargo/compare/64fb38c9...rust-1.72.0)

### 新增

- ❗ 默认启用 `-Zdoctest-in-workspace`。运行每个文档
  测试时，工作目录设置为该测试所属包的根目录。
  [docs](https://doc.rust-lang.org/nightly/cargo/commands/cargo-test.html#working-directory-of-tests)
  [#12221](https://github.com/rust-lang/cargo/pull/12221)
  [#12288](https://github.com/rust-lang/cargo/pull/12288)
- 添加对“default”关键字的支持，以将先前设置的 `build.jobs`
  并行度重置回默认值。
  [#12222](https://github.com/rust-lang/cargo/pull/12222)

### 变更

- 🚨 [CVE-2023-40030](https://github.com/rust-lang/cargo/security/advisories/GHSA-wrrj-h57r-vx9p)：
  恶意依赖可以向 cargo 生成的 timing 报告中注入任意 JavaScript。
  为缓解此问题，feature 名称验证检查现在变为硬错误。
  该警告在 Rust 1.49 中添加。这些扩展字符在 crates.io 上不允许，
  因此这应仅影响其他注册表的用户，或不向注册表发布的人。
  [#12291](https://github.com/rust-lang/cargo/pull/12291)
- 当 edition 2021 包位于虚拟工作区中且未设置
  `workspace.resolver` 时，Cargo 现在会发出警告。建议为工作区
  显式设置解析器版本。
  [#10910](https://github.com/rust-lang/cargo/pull/10910)
- 将 IBM AIX 共享库搜索路径设置为 `LIBPATH`。
  [#11968](https://github.com/rust-lang/cargo/pull/11968)
- 不向 rustc 传递 `-C debuginfo=0`，因为那是默认值。
  [#12022](https://github.com/rust-lang/cargo/pull/12022)
  [#12205](https://github.com/rust-lang/cargo/pull/12205)
- 在 `cargo install` 失败时添加关于重用先前临时路径的消息。
  [#12231](https://github.com/rust-lang/cargo/pull/12231)
- 当 `rustup` override 简写放在错误位置时添加消息。
  [#12226](https://github.com/rust-lang/cargo/pull/12226)
- 在获取嵌套子模块时尽可能尊重类似 scp 的 URL。
  [#12359](https://github.com/rust-lang/cargo/pull/12359)
  [#12411](https://github.com/rust-lang/cargo/pull/12411)

### 修复

- `cargo clean` 使用 `remove_dir_all` 作为回退以解决竞态条件。
  [#11442](https://github.com/rust-lang/cargo/pull/11442)
- 降低 Cargo 重新格式化用户 `[features]` 表的可能性。
  [#12191](https://github.com/rust-lang/cargo/pull/12191)
- 修复嵌套 Git 子模块无法获取。
  [#12244](https://github.com/rust-lang/cargo/pull/12244)

### 仅 Nightly

- 🔥 `-Zscript` 是一项实验性功能，为 Cargo 中的单文件包添加不稳定支持，
  以便我们可以通过实现来探索设计并解决问题，从而收集反馈。
  ([eRFC 3424](https://github.com/rust-lang/rfcs/blob/master/text/3424-cargo-script.md))
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#script)
  [#12245](https://github.com/rust-lang/cargo/pull/12245)
  [#12255](https://github.com/rust-lang/cargo/pull/12255)
  [#12258](https://github.com/rust-lang/cargo/pull/12258)
  [#12262](https://github.com/rust-lang/cargo/pull/12262)
  [#12268](https://github.com/rust-lang/cargo/pull/12268)
  [#12269](https://github.com/rust-lang/cargo/pull/12269)
  [#12281](https://github.com/rust-lang/cargo/pull/12281)
  [#12282](https://github.com/rust-lang/cargo/pull/12282)
  [#12283](https://github.com/rust-lang/cargo/pull/12283)
  [#12284](https://github.com/rust-lang/cargo/pull/12284)
  [#12287](https://github.com/rust-lang/cargo/pull/12287)
  [#12289](https://github.com/rust-lang/cargo/pull/12289)
  [#12303](https://github.com/rust-lang/cargo/pull/12303)
  [#12305](https://github.com/rust-lang/cargo/pull/12305)
  [#12308](https://github.com/rust-lang/cargo/pull/12308)
- 运行 `cargo new`/`cargo init` 时自动继承工作区 lints。
  [#12174](https://github.com/rust-lang/cargo/pull/12174)
- 再次移除 `-Zjobserver-per-rustc`。
  [#12285](https://github.com/rust-lang/cargo/pull/12285)
- 为 `-Zconfig-include` 添加 `.toml` 文件扩展名限制。
  [#12298](https://github.com/rust-lang/cargo/pull/12298)
- 添加 `-Znext-lockfile-bump` 以为下一次锁文件升级做准备。
  [#12279](https://github.com/rust-lang/cargo/pull/12279)
  [#12302](https://github.com/rust-lang/cargo/pull/12302)

### 文档

- 在 Cargo FAQ 中添加了关于 `Cargo.lock` 冲突的描述。
  [#12185](https://github.com/rust-lang/cargo/pull/12185)
- 添加了关于索引忽略 SemVer 构建元数据的小注记。
  [#12206](https://github.com/rust-lang/cargo/pull/12206)
- 为 `cargo::sources` 模块中的类型及其相关项添加了文档注释。
  [#12192](https://github.com/rust-lang/cargo/pull/12192)
  [#12239](https://github.com/rust-lang/cargo/pull/12239)
  [#12247](https://github.com/rust-lang/cargo/pull/12247)
- 为 `Source` 下载函数添加了更多文档。
  [#12319](https://github.com/rust-lang/cargo/pull/12319)
- 为凭证助手添加了 README。
  [#12322](https://github.com/rust-lang/cargo/pull/12322)
- 修复了 Dependency Resolution 中的版本要求示例。
  [#12267](https://github.com/rust-lang/cargo/pull/12267)
- 澄清 cargo-install 的默认行为。
  [#12276](https://github.com/rust-lang/cargo/pull/12276)
- 澄清默认使用“default”分支而非 `main`。
  [#12251](https://github.com/rust-lang/cargo/pull/12251)
- 提供关于版本要求的指导。
  [#12323](https://github.com/rust-lang/cargo/pull/12323)

### 内部

- 更新至 `gix` 0.45 以支持多轮 pack 协商。
  [#12236](https://github.com/rust-lang/cargo/pull/12236)
- 更新至 `curl-sys` 0.4.63，对应 curl 8.1.2。
  [#12218](https://github.com/rust-lang/cargo/pull/12218)
- 更新至 `openssl` 0.10.55。
  [#12300](https://github.com/rust-lang/cargo/pull/12300)
- 更新了若干依赖。
  [#12261](https://github.com/rust-lang/cargo/pull/12261)
- 从 `windows-sys` 依赖中移除未使用的 features。
  [#12176](https://github.com/rust-lang/cargo/pull/12176)
- 重构编译器调用。
  [#12211](https://github.com/rust-lang/cargo/pull/12211)
- 重构 git 与注册表源，以及注册表数据。
  [#12203](https://github.com/rust-lang/cargo/pull/12203)
  [#12197](https://github.com/rust-lang/cargo/pull/12197)
  [#12240](https://github.com/rust-lang/cargo/pull/12240)
  [#12248](https://github.com/rust-lang/cargo/pull/12248)
- 按字典序排列 `-Z` 标志。
  [#12182](https://github.com/rust-lang/cargo/pull/12182)
  [#12223](https://github.com/rust-lang/cargo/pull/12223)
  [#12224](https://github.com/rust-lang/cargo/pull/12224)
- Cargo 自身测试基础设施的若干改进与加速。
  [#12184](https://github.com/rust-lang/cargo/pull/12184)
  [#12188](https://github.com/rust-lang/cargo/pull/12188)
  [#12189](https://github.com/rust-lang/cargo/pull/12189)
  [#12194](https://github.com/rust-lang/cargo/pull/12194)
  [#12199](https://github.com/rust-lang/cargo/pull/12199)
- 将 print-ban 从测试迁移到 clippy
  [#12246](https://github.com/rust-lang/cargo/pull/12246)
- 对 interning 用途切换到 `OnceLock`。
  [#12217](https://github.com/rust-lang/cargo/pull/12217)
- 移除一处不必要的 `.clone`。
  [#12213](https://github.com/rust-lang/cargo/pull/12213)
- 不在非 Linux 平台上尝试编译 `cargo-credential-gnome-secret`。
  [#12321](https://github.com/rust-lang/cargo/pull/12321)
- 使用宏移除可继承工作区字段 getter 的重复。
  [#12317](https://github.com/rust-lang/cargo/pull/12317)
- 提取并重新排列注册表 API 项到它们自己的模块。
  [#12290](https://github.com/rust-lang/cargo/pull/12290)
- 当容器测试失败时显示更好的错误。
  [#12264](https://github.com/rust-lang/cargo/pull/12264)

## Cargo 1.71.1 (2023-08-03)

### 修复

- 🚨 [CVE-2023-38497](https://github.com/rust-lang/cargo/security/advisories/GHSA-j3xp-wfr4-hx87)：
  Cargo 1.71.1 及更高版本在解压 crate 归档时尊重 umask。它还会
  清除其尝试访问的、由旧版 Cargo 生成的缓存。

## Cargo 1.71 (2023-07-13)
[84b7041f...rust-1.71.0](https://github.com/rust-lang/cargo/compare/84b7041f...rust-1.71.0)

### 新增

- 允许在 Cargo.toml 中使用命名 debuginfo 选项。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/profiles.html#debug)
  [#11958](https://github.com/rust-lang/cargo/pull/11958)
- 在 `cargo metadata` 的输出中添加了 `workspace_default_members`。
  [#11978](https://github.com/rust-lang/cargo/pull/11978)
- 运行 `cargo new`/`cargo init` 时自动继承工作区字段。
  [#12069](https://github.com/rust-lang/cargo/pull/12069)

### 变更

- ❗ 优化了在 `rustup` 下的使用。当 Cargo 检测到它将运行指向
  rustup 代理的 `rustc` 时，它会尝试绕过代理并直接使用底层
  二进制。这与 rustup 及 `RUSTUP_TOOLCHAIN` 的交互存在一些假设。
  不过，预计不会影响普通用户。
  [#11917](https://github.com/rust-lang/cargo/pull/11917)
- ❗ 查询包时，Cargo 只尝试原始名称、全部连字符以及
  全部下划线以处理拼写错误。此前，Cargo 会尝试连字符与
  下划线的每种组合，导致对 crates.io 的过多请求。
  [#12083](https://github.com/rust-lang/cargo/pull/12083)
- ❗ 禁止在 `[env]` 配置表中使用 `RUSTUP_HOME` 与 `RUSTUP_TOOLCHAIN`。
  这被视为 Cargo 不希望支持的用例，
  因为它很可能导致问题或造成困惑。
  [#12101](https://github.com/rust-lang/cargo/pull/12101)
  [#12107](https://github.com/rust-lang/cargo/pull/12107)
- 在 Cargo.toml 中获取到空依赖表时给出更好的错误消息。
  [#11997](https://github.com/rust-lang/cargo/pull/11997)
- 在 Cargo.toml 中指定空依赖时给出更好的错误消息。
  [#12001](https://github.com/rust-lang/cargo/pull/12001)
- `--help` 文本现在会换行，以便在窄屏幕上阅读。
  [#12013](https://github.com/rust-lang/cargo/pull/12013)
- 调整了 `--help` 文本中参数的顺序以澄清 `--bin` 的作用。
  [#12157](https://github.com/rust-lang/cargo/pull/12157)
- `rust-version` 包含在发往注册表的 `cargo publish` 请求中。
  [#12041](https://github.com/rust-lang/cargo/pull/12041)

### 修复

- 更正了 `cargo clippy --fix` 的错误报告 URL。
  [#11882](https://github.com/rust-lang/cargo/pull/11882)
- Cargo 现在将 `[env]` 应用于目标信息发现的 rust 调用。
  [#12029](https://github.com/rust-lang/cargo/pull/12029)
- 修复使用 HTTP/2 时 http debug 中令牌未被遮蔽。
  [#12095](https://github.com/rust-lang/cargo/pull/12095)
- 修复某些情况下未传递 `-C debuginfo`，导致构建缓存未命中。
  [#12165](https://github.com/rust-lang/cargo/pull/12165)
- 修复 `cargo install` 找到同名包时的歧义。
  该歧义发生在包依赖自身旧版本等情况。
  [#12015](https://github.com/rust-lang/cargo/pull/12015)
- 修复 `cargo package` 检查冲突文件时的误报。
  [#12135](https://github.com/rust-lang/cargo/pull/12135)
- 修复 `dep/feat` 语法在与 `dep:` 语法共存且
  试图启用可选依赖的 features 时不工作。
  [#12130](https://github.com/rust-lang/cargo/pull/12130)
- 修复 `cargo tree` 未正确处理带 `-e no-proc-macro` 的输出。
  [#12044](https://github.com/rust-lang/cargo/pull/12044)
- 在 `cargo package` 中对 Cargo.toml 里空的 `readme` 或 `license-file`
  发出警告而非错误。
  [#12036](https://github.com/rust-lang/cargo/pull/12036)
- 修复当使用 HTTP 代理且 Cargo 可执行文件链接到
  特定版本的系统 libcurl 时，CURL 连接可能失败。受影响的
  libcurl 版本：7.87.0、7.88.0、7.88.1。
  [#12234](https://github.com/rust-lang/cargo/pull/12234)
  [#12242](https://github.com/rust-lang/cargo/pull/12242)

### 仅 Nightly

- 🔥 `-Zgitoxide` 功能现在支持对依赖与注册表索引进行
  浅克隆与 fetch。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#gitoxide)
  [#11840](https://github.com/rust-lang/cargo/pull/11840)
- 🔥 `-Zlints` 功能支持在 Cargo.toml 中配置 lint 规则
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#lints)
  [#12148](https://github.com/rust-lang/cargo/pull/12148)
  [#12168](https://github.com/rust-lang/cargo/pull/12168)
- `-Zbuild-std` 在 `nightly-2023-05-04` 中缺失 features 的破坏
  已在 `nightly-2023-05-05` 中修复。
  [#12088](https://github.com/rust-lang/cargo/pull/12088)
- 在 profile rustflags 变更时重新编译。
  [#11981](https://github.com/rust-lang/cargo/pull/11981)
- 添加了 `-Zmsrv-policy` 功能标志占位符。
  [#12043](https://github.com/rust-lang/cargo/pull/12043)
- `cargo add` 在使用 `-Zmsrv-policy` 选择包时现在会考虑 `rust-version`。
  [#12078](https://github.com/rust-lang/cargo/pull/12078)

### 文档

- 添加了 Cargo 团队章程。
  [docs](https://doc.crates.io/contrib/team.html)
  [#12010](https://github.com/rust-lang/cargo/pull/12010)
- SemVer：在现有项上添加 `#[non_exhaustive]` 是破坏性变更。
  [#10877](https://github.com/rust-lang/cargo/pull/10877)
- SemVer：将 unsafe 函数变为 safe 不是破坏性变更。
  [#12116](https://github.com/rust-lang/cargo/pull/12116)
- SemVer：更改 MSRV 通常是次要变更。
  [#12122](https://github.com/rust-lang/cargo/pull/12122)
- 澄清何时以及如何使用 `cargo yank`。
  [#11862](https://github.com/rust-lang/cargo/pull/11862)
- 澄清 crates.io 不会立即链接到 docs.rs。
  [#12146](https://github.com/rust-lang/cargo/pull/12146)
- 澄清围绕测试目标设置的文档。 
  [#12032](https://github.com/rust-lang/cargo/pull/12032)
- 在 Index 格式中指定 `rust_version`。
  [#12040](https://github.com/rust-lang/cargo/pull/12040)
- 在 owner-remove 注册表 API 响应中指定 `msg`。
  [#12068](https://github.com/rust-lang/cargo/pull/12068)
- 添加了更多关于 artifact-dependencies 的文档。 
  [#12110](https://github.com/rust-lang/cargo/pull/12110)
- 为作为库的 cargo 的 `Source` 与构建脚本添加了文档注释。
  [#12133](https://github.com/rust-lang/cargo/pull/12133)
  [#12153](https://github.com/rust-lang/cargo/pull/12153)
  [#12159](https://github.com/rust-lang/cargo/pull/12159)
- 若干拼写与失效链接修复。
  [#12018](https://github.com/rust-lang/cargo/pull/12018)
  [#12020](https://github.com/rust-lang/cargo/pull/12020)
  [#12049](https://github.com/rust-lang/cargo/pull/12049)
  [#12067](https://github.com/rust-lang/cargo/pull/12067)
  [#12073](https://github.com/rust-lang/cargo/pull/12073)
  [#12143](https://github.com/rust-lang/cargo/pull/12143)
- home：澄清各平台上的行为
  [#12047](https://github.com/rust-lang/cargo/pull/12047)

### 内部

- 更新至 `linux-raw-sys` 0.3.2 
  [#11998](https://github.com/rust-lang/cargo/pull/11998)
- 更新至 `git2` 0.17.1，对应 libgit2 1.6.4。
  [#12096](https://github.com/rust-lang/cargo/pull/12096)
- 更新至 `windows-sys` 0.48.0 
  [#12021](https://github.com/rust-lang/cargo/pull/12021)
- 更新至 `libc` 0.2.144 
  [#12014](https://github.com/rust-lang/cargo/pull/12014)
  [#12098](https://github.com/rust-lang/cargo/pull/12098)
- 更新至 `openssl-src` 111.25.3+1.1.1t 
  [#12005](https://github.com/rust-lang/cargo/pull/12005)
- 更新至 `home` 0.5.5
  [#12037](https://github.com/rust-lang/cargo/pull/12037)
- 启用已使用的 `Win32_System_Console` feature。
  [#12016](https://github.com/rust-lang/cargo/pull/12016)
- Cargo 现在是一个 Cargo 工作区。我们终于开始自用了！
  [#11851](https://github.com/rust-lang/cargo/pull/11851)
  [#11994](https://github.com/rust-lang/cargo/pull/11994)
  [#11996](https://github.com/rust-lang/cargo/pull/11996)
  [#12024](https://github.com/rust-lang/cargo/pull/12024)
  [#12025](https://github.com/rust-lang/cargo/pull/12025)
  [#12057](https://github.com/rust-lang/cargo/pull/12057)
- 🔥 为 Cargo 贡献者提供的新的、直观的 issue 标签系统。
  [docs](https://doc.crates.io/contrib/issues.html)
  [#11995](https://github.com/rust-lang/cargo/pull/11995)
  [#12002](https://github.com/rust-lang/cargo/pull/12002)
  [#12003](https://github.com/rust-lang/cargo/pull/12003)
- 允许 win/mac 凭证管理器在所有平台上构建。
  [#11993](https://github.com/rust-lang/cargo/pull/11993)
  [#12027](https://github.com/rust-lang/cargo/pull/12027)
- 仅在非 Windows 平台上使用 `openssl`。
  [#11979](https://github.com/rust-lang/cargo/pull/11979)
- 使用受限的 Damerau-Levenshtein 算法提供拼写建议。
  [#11963](https://github.com/rust-lang/cargo/pull/11963)
- 添加了新的 xtask `cargo build-man`。
  [#12048](https://github.com/rust-lang/cargo/pull/12048)
- 添加了新的 xtask `cargo stale-label`。
  [#12051](https://github.com/rust-lang/cargo/pull/12051)
- 添加了新的 xtask `cargo unpublished`。
  [#12039](https://github.com/rust-lang/cargo/pull/12039)
  [#12045](https://github.com/rust-lang/cargo/pull/12045)
  [#12085](https://github.com/rust-lang/cargo/pull/12085)
- CI：检查成员 crate 是否需要任何版本升级。
  [#12126](https://github.com/rust-lang/cargo/pull/12126)
- 修复了一些测试基础设施问题。
  [#11976](https://github.com/rust-lang/cargo/pull/11976)
  [#12026](https://github.com/rust-lang/cargo/pull/12026)
  [#12055](https://github.com/rust-lang/cargo/pull/12055)
  [#12117](https://github.com/rust-lang/cargo/pull/12117)

## Cargo 1.70 (2023-06-01)
[9880b408...rust-1.70.0](https://github.com/rust-lang/cargo/compare/9880b408...rust-1.70.0)

### 新增

- 🎉 新增 `cargo logout` 命令，用于从本地移除 registry 的 API 令牌。
  [docs](https://doc.rust-lang.org/nightly/cargo/commands/cargo-logout.html)
  [#11919](https://github.com/rust-lang/cargo/pull/11919)
  [#11950](https://github.com/rust-lang/cargo/pull/11950)
- 为 `cargo install` 新增 `--ignore-rust-version` 标志。
  [#11859](https://github.com/rust-lang/cargo/pull/11859)
- 编译 crate 时，现在会将 `CARGO_PKG_README` 环境变量设置为
  README 文件的路径。
  [#11645](https://github.com/rust-lang/cargo/pull/11645)
- Cargo 现在会显示更丰富的 Cargo 目标编译失败信息。
  [#11636](https://github.com/rust-lang/cargo/pull/11636)

### 变更

- 🎉 `sparse` 协议现已成为 crates.io 的默认协议！
  ([RFC 2789](https://github.com/rust-lang/rfcs/blob/master/text/2789-sparse-index.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/registries.html#registry-protocols))
  [#11791](https://github.com/rust-lang/cargo/pull/11791)
  [#11783](https://github.com/rust-lang/cargo/pull/11783)
- ❗ `cargo login` 与 `cargo logout` 现在使用 `registry.default` 中指定的
  registry。这是一次非预期的回归修复。
  [#11949](https://github.com/rust-lang/cargo/pull/11949)
- `cargo update` 在降级依赖时准确显示 `Downgrading` 状态。
  [#11839](https://github.com/rust-lang/cargo/pull/11839)
- 为 HTTP 错误增加了更多信息以帮助调试。
  [#11878](https://github.com/rust-lang/cargo/pull/11878)
- 为 Cargo 的网络重试增加了延迟。
  [#11881](https://github.com/rust-lang/cargo/pull/11881)
- 优化了等待发布完成时的 `cargo publish` 消息。
  [#11713](https://github.com/rust-lang/cargo/pull/11713)
- 从 git 仓库执行 `cargo install` 但发现多个包时，
  错误消息更完善。
  [#11835](https://github.com/rust-lang/cargo/pull/11835)

### 修复

- 移除了 `cargo tree` 的 `--charset` 选项中可能值的重复项。
  [#11785](https://github.com/rust-lang/cargo/pull/11785)
- 修复了同时以带值与不带值方式定义的配置对应的 `CARGO_CFG_` 变量。
  [#11790](https://github.com/rust-lang/cargo/pull/11790)
- 打破了 `cargo add` 在新增依赖中因循环 features 导致的死循环。
  [#11805](https://github.com/rust-lang/cargo/pull/11805)
- 当 `[patch]` 参与依赖解析导致冲突时不再 panic。
  [#11770](https://github.com/rust-lang/cargo/pull/11770)
- 修复了凭据令牌格式校验。
  [#11951](https://github.com/rust-lang/cargo/pull/11951)
- 在发布时补充了缺失的令牌格式校验。
  [#11952](https://github.com/rust-lang/cargo/pull/11952)
- 修复了在 Config 快照中查找环境变量时的大小写不匹配问题。
  [#11824](https://github.com/rust-lang/cargo/pull/11824)
- `cargo new` 生成正确的 `.hgignore`，语义与其他
  VCS ignore 文件对齐。
  [#11855](https://github.com/rust-lang/cargo/pull/11855)
- 停止进行不必要的模糊 registry 索引查询。这显著减少了
  对名称中包含 `-` 或 `_` 的 crate 向远程 registry
  发起的 HTTP 请求数量。
  [#11936](https://github.com/rust-lang/cargo/pull/11936)
  [#11937](https://github.com/rust-lang/cargo/pull/11937)

### 仅 Nightly

- 新增 `-Zdirect-minimal-versions`。行为类似 `-Zminimal-versions`，但
  仅作用于直接依赖。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#direct-minimal-versions))
  [#11688](https://github.com/rust-lang/cargo/pull/11688)
- 新增 `-Zgitoxide`，将 Cargo 中所有 `git fetch` 操作切换为
  使用 `gitoxide` crate。目前仍是 MVP，但可将性能
  提升最高达 2 倍。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html##gitoxide))
  [#11448](https://github.com/rust-lang/cargo/pull/11448)
  [#11800](https://github.com/rust-lang/cargo/pull/11800)
  [#11822](https://github.com/rust-lang/cargo/pull/11822)
  [#11830](https://github.com/rust-lang/cargo/pull/11830)
- 移除了 `-Zjobserver-per-rustc`。其 rustc 对应实现从未落地。
  [#11764](https://github.com/rust-lang/cargo/pull/11764)

### 文档

- 清理了不稳定功能文档。
  [#11793](https://github.com/rust-lang/cargo/pull/11793)
- 用图表增强了 timing report 文档。
  [#11798](https://github.com/rust-lang/cargo/pull/11798)
- 澄清了发布后 registry 索引状态的相关要求。
  [#11926](https://github.com/rust-lang/cargo/pull/11926)
- 澄清了 `-C` 文档：它出现在命令之前。
  [#11947](https://github.com/rust-lang/cargo/pull/11947)
- 澄清了 `cargo test`、`cargo bench` 与
  `cargo run` 的工作目录行为。
  [#11901](https://github.com/rust-lang/cargo/pull/11901)
- 修复了 `registries.name.index` 配置的文档。
  [#11880](https://github.com/rust-lang/cargo/pull/11880)
- 在 `cargo-add` 的帮助文本中提示潜在的意外 shell 展开。
  [#11826](https://github.com/rust-lang/cargo/pull/11826)
- 更新了 external-tools JSON 文档。
  [#11918](https://github.com/rust-lang/cargo/pull/11918)
- 指出索引 JSON 与 API 或元数据之间的差异。
  [#11927](https://github.com/rust-lang/cargo/pull/11927)
- 提及 pkgid 格式时统一使用 `@`。
  [#11956](https://github.com/rust-lang/cargo/pull/11956)
- 增强了 Cargo 贡献者指南。
  [#11825](https://github.com/rust-lang/cargo/pull/11825)
  [#11842](https://github.com/rust-lang/cargo/pull/11842)
  [#11869](https://github.com/rust-lang/cargo/pull/11869)
  [#11876](https://github.com/rust-lang/cargo/pull/11876)
- 将 Cargo 贡献者指南的一部分移至 Cargo API 文档。
  [docs](https://doc.rust-lang.org/nightly/nightly-rustc/cargo)
  [#11809](https://github.com/rust-lang/cargo/pull/11809)
  [#11841](https://github.com/rust-lang/cargo/pull/11841)
  [#11850](https://github.com/rust-lang/cargo/pull/11850)
  [#11870](https://github.com/rust-lang/cargo/pull/11870)
- Cargo 团队现已安排
  [办公时间](https://github.com/rust-lang/cargo/wiki/Office-Hours)！
  [#11903](https://github.com/rust-lang/cargo/pull/11903)

### 内部

- 改用 `sha2` crate 进行 SHA256 计算。
  [#11795](https://github.com/rust-lang/cargo/pull/11795)
  [#11807](https://github.com/rust-lang/cargo/pull/11807)
- 将 benchsuite 切换为索引归档。
  [#11933](https://github.com/rust-lang/cargo/pull/11933)
- 更新至 `base64` 0.21.0。
  [#11796](https://github.com/rust-lang/cargo/pull/11796)
- 更新至 `curl-sys` 0.4.61，对应 curl 8.0.1。
  [#11871](https://github.com/rust-lang/cargo/pull/11871)
- 更新至 `proptest` 1.1.0。
  [#11886](https://github.com/rust-lang/cargo/pull/11886)
- 更新至 `git2` 0.17.0，对应 libgit2 1.6.3。
  [#11928](https://github.com/rust-lang/cargo/pull/11928)
- 更新至 `clap` 4.2。
  [#11904](https://github.com/rust-lang/cargo/pull/11904)
- 在 Cargo 自身的 CI 流水线中集成了 `cargo-deny`。
  [#11761](https://github.com/rust-lang/cargo/pull/11761)
- 使非阻塞 IO 调用更加稳健。
  [#11624](https://github.com/rust-lang/cargo/pull/11624)
- 从 `cargo-platform` 中的 `serde` 移除了 `derive` feature。
  [#11915](https://github.com/rust-lang/cargo/pull/11915)
- 用更稳健的 `try_canonicalize` 替换 `std::fs::canonicalize`。
  [#11866](https://github.com/rust-lang/cargo/pull/11866)
- 对 `std::env::var` 及其同类启用 clippy 的 `disallowed_methods` 警告。
  [#11828](https://github.com/rust-lang/cargo/pull/11828)

## Cargo 1.69 (2023-04-20)
[985d561f...rust-1.69.0](https://github.com/rust-lang/cargo/compare/985d561f...rust-1.69.0)

### 新增

- 当编译警告可自动修复时，Cargo 现在会建议 `cargo fix` 或 `cargo clippy --fix`。
  [#11558](https://github.com/rust-lang/cargo/pull/11558)
- 若尝试安装库 crate，Cargo 现在会建议使用 `cargo add`。
  [#11410](https://github.com/rust-lang/cargo/pull/11410)
- Cargo 现在也会为二进制示例设置 `CARGO_BIN_NAME` 环境变量。
  [#11705](https://github.com/rust-lang/cargo/pull/11705)

### 变更

- ❗ 当工作区依赖的 `default-features` 设为 false，
  而成员继承的依赖具有 `default-features = true` 时，
  Cargo 将启用该依赖的默认 features。
  [#11409](https://github.com/rust-lang/cargo/pull/11409)
- ❗ 禁止在 `[env]` 配置表中使用 `CARGO_HOME`。Cargo 自身不会
  读取该值，但对 cargo 的递归调用会，而这并非预期行为。
  [#11644](https://github.com/rust-lang/cargo/pull/11644)
- ❗ 构建依赖的 Debuginfo 若未显式设置，现在默认关闭。这预期
  能改善整体构建时间。
  [#11252](https://github.com/rust-lang/cargo/pull/11252)
- Cargo 现在会对 registry 令牌中的无效字母数字字符报错。
  [#11600](https://github.com/rust-lang/cargo/pull/11600)
- `cargo add` 现在仅检查 `[dependencies]` 的顺序，
  而不考虑 `[dependencies.*]`。
  [#11612](https://github.com/rust-lang/cargo/pull/11612)
- 通过更新依赖 `jobserver`，Cargo 现在支持 GNU Make 4.4 中的
  新 jobserver IPC 风格。
  [#11767](https://github.com/rust-lang/cargo/pull/11767)
- 当没有二进制目标满足要求时，`cargo install` 现在会报告所需的 features。
  [#11647](https://github.com/rust-lang/cargo/pull/11647)

### 修复

- 将 `.dwp` DWARF 包文件提升到可执行文件旁，以便调试器
  定位它们。
  [#11572](https://github.com/rust-lang/cargo/pull/11572)
- 修复了当 `rerun-if-changed` 指向文件系统未保留 mtime 的
  目录时，构建脚本触发重新编译的问题。
  [#11613](https://github.com/rust-lang/cargo/pull/11613)
- 修复了将 `[workspace.dependencies]` 中的依赖用于
  `[patch]` 时的 panic。此用法本不应受支持。
  [#11565](https://github.com/rust-lang/cargo/pull/11565)
  [#11630](https://github.com/rust-lang/cargo/pull/11630)
- 修复了 `cargo report` 多次保存相同 future-incompat 报告的问题。
  [#11648](https://github.com/rust-lang/cargo/pull/11648)
- 修复了将以 `.rs` 结尾的目录错误推断为文件的问题。
  [#11678](https://github.com/rust-lang/cargo/pull/11678)
- 修复了 `.cargo-ok` 文件被错误截断、导致无法使用依赖的问题。
  [#11665](https://github.com/rust-lang/cargo/pull/11665)
  [#11724](https://github.com/rust-lang/cargo/pull/11724)

### 仅 Nightly

- `-Zrustdoc-scrape-example` 在构建脚本出错时必须失败。
  [#11694](https://github.com/rust-lang/cargo/pull/11694)
- 将 1password 凭据管理器集成更新至版本 2 CLI。
  [#11692](https://github.com/rust-lang/cargo/pull/11692)
- 对包并不直接交互的目标上的传递性 artifact 依赖发出错误消息。
  [#11643](https://github.com/rust-lang/cargo/pull/11643)
- 新增 `-C` 标志，用于在构建开始前更改当前目录。
  [#10952](https://github.com/rust-lang/cargo/pull/10952)

### 文档

- 澄清了 `CARGO_CRATE_NAME` 与 `CARGO_PKG_NAME` 的区别。
  [#11576](https://github.com/rust-lang/cargo/pull/11576)
- 为出现目标三元组的位置添加了指向术语表 Target 小节的链接。
  [#11603](https://github.com/rust-lang/cargo/pull/11603)
- 描述了当前解析器有时会重复依赖的原因。
  [#11604](https://github.com/rust-lang/cargo/pull/11604)
- 添加了关于在 crates.io 验证邮箱地址的说明。
  [#11620](https://github.com/rust-lang/cargo/pull/11620)
- 在 `publish.timeout` 文档中提及当前默认值。
  [#11652](https://github.com/rust-lang/cargo/pull/11652)
- 为 `cargo::core::compiler` 模块增加了更多文档注释。
  [#11669](https://github.com/rust-lang/cargo/pull/11669)
  [#11703](https://github.com/rust-lang/cargo/pull/11703)
  [#11711](https://github.com/rust-lang/cargo/pull/11711)
  [#11758](https://github.com/rust-lang/cargo/pull/11758)
- 增加了如何实现不稳定功能的更多指导。
  [#11675](https://github.com/rust-lang/cargo/pull/11675)
- 修复了不稳定章节中 `codegen-backend` 的布局。
  [#11676](https://github.com/rust-lang/cargo/pull/11676)
- 添加了指向 LTO 文档的链接。
  [#11701](https://github.com/rust-lang/cargo/pull/11701)
- 在手册页中为 `cargo install` 的配置发现
  添加了文档
  [#11763](https://github.com/rust-lang/cargo/pull/11763)
- 记录了 `cargo add` 中 `-F` 标志作为 `--features` 的别名。
  [#11774](https://github.com/rust-lang/cargo/pull/11774)

### 内部

- 在 Windows 上禁用网络 SSH 测试。
  [#11610](https://github.com/rust-lang/cargo/pull/11610)
- 将部分阻塞测试改为非阻塞。
  [#11650](https://github.com/rust-lang/cargo/pull/11650)
- 在 CI 中拒绝警告，而非本地。
  [#11699](https://github.com/rust-lang/cargo/pull/11699)
- 将 `cargo_new::NewProjectKind` 重新导出为公开。
  [#11700](https://github.com/rust-lang/cargo/pull/11700)
- 使依赖按字母顺序排列。
  [#11719](https://github.com/rust-lang/cargo/pull/11719)
- 将部分测试从 `build` 切换为 `check`。
  [#11725](https://github.com/rust-lang/cargo/pull/11725)
- 统一了 Cargo 内部读取环境变量的方式。
  [#11727](https://github.com/rust-lang/cargo/pull/11727)
  [#11754](https://github.com/rust-lang/cargo/pull/11754)
- 修复了具有非确定性排序的测试
  [#11766](https://github.com/rust-lang/cargo/pull/11766)
- 添加测试以验证中间产物会保留在临时目录中。
  [#11771](https://github.com/rust-lang/cargo/pull/11771)
- 更新了 aarch64-apple-darwin 的交叉测试说明。
  [#11663](https://github.com/rust-lang/cargo/pull/11663)
- 更新至 `toml` v0.6 与 `toml_edit` v0.18 以进行 TOML 操作。
  [#11618](https://github.com/rust-lang/cargo/pull/11618)
- 更新至 `clap` v4.1.3。
  [#11619](https://github.com/rust-lang/cargo/pull/11619)
- 用 `windows-sys` crate 替换 `winapi` 以进行 Windows 绑定。
  [#11656](https://github.com/rust-lang/cargo/pull/11656)
- 改用 `url` crate 进行百分号编码，而不再使用 `percent-encoding`。
  [#11750](https://github.com/rust-lang/cargo/pull/11750)
- Cargo 贡献者在撰写文档时可受益于智能标点，例如
  `---` 会自动转换为破折号。
  ([docs](https://rust-lang.github.io/mdBook/format/markdown.html#smart-punctuation))
  [#11646](https://github.com/rust-lang/cargo/pull/11646)
  [#11715](https://github.com/rust-lang/cargo/pull/11715)
- Cargo 的 CI 流水线现在覆盖 nightly 上的 macOS。
  [#11712](https://github.com/rust-lang/cargo/pull/11712)
- 在 Cargo 自身中重新启用了部分 clippy lint。
  [#11722](https://github.com/rust-lang/cargo/pull/11722)
- 在 Cargo 的 CI 中启用了 sparse 协议。
  [#11632](https://github.com/rust-lang/cargo/pull/11632)
- Cargo 中的拉取请求现在会自动打上 `A-*` 与 `Command-*` 标签。
  [#11664](https://github.com/rust-lang/cargo/pull/11664)
  [#11679](https://github.com/rust-lang/cargo/pull/11679)

## Cargo 1.68.2 (2023-03-28)
[115f3455...rust-1.68.0](https://github.com/rust-lang/cargo/compare/115f3455...rust-1.68.0)

- 更新了 cargo 内置捆绑的 GitHub RSA SSH 主机密钥。
  该密钥于 2023-03-24 在旧密钥泄露后由
  [GitHub 轮换](https://github.blog/2023-03-23-we-updated-our-rsa-ssh-host-key/)。
  [#11883](https://github.com/rust-lang/cargo/pull/11883)
- 新增对 SSH known hosts 标记 `@revoked` 的支持。
  [#11635](https://github.com/rust-lang/cargo/pull/11635)
- 将旧的 GitHub RSA 主机密钥标记为已吊销。这将防止 Cargo
  即使在系统信任该密钥时也接受已泄露的密钥。
  [#11889](https://github.com/rust-lang/cargo/pull/11889)

## Cargo 1.68 (2023-03-09)
[f6e737b1...rust-1.68.0](https://github.com/rust-lang/cargo/compare/f6e737b1...rust-1.68.0)

### 新增

- 🎉 新的 "sparse" 协议已稳定。
  访问 crates.io 时应能带来显著的性能提升。
  ([RFC 2789](https://github.com/rust-lang/rfcs/blob/master/text/2789-sparse-index.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/registries.html#registry-protocols))
  [#11224](https://github.com/rust-lang/cargo/pull/11224)
  [#11480](https://github.com/rust-lang/cargo/pull/11480)
  [#11733](https://github.com/rust-lang/cargo/pull/11733)
  [#11756](https://github.com/rust-lang/cargo/pull/11756)
- 🎉 `home` crate 现已成为 `rust-lang/cargo` 仓库中的子 crate。欢迎！
  [#11359](https://github.com/rust-lang/cargo/pull/11359)
  [#11481](https://github.com/rust-lang/cargo/pull/11481)
- 长诊断消息现在可截断以提高可读性。
  [#11494](https://github.com/rust-lang/cargo/pull/11494)
- 即使启用了 `net.git-fetch-with-cli`，也会显示 crates.io 索引更新的进度。
  [#11579](https://github.com/rust-lang/cargo/pull/11579)
- `cargo build --verbose` 会告知更多关于为何重新编译的信息。
  [#11407](https://github.com/rust-lang/cargo/pull/11407)
- Cargo 的文件锁定机制现在通过使用 `fcntl` 支持 Solaris。
  [#11439](https://github.com/rust-lang/cargo/pull/11439)
  [#11474](https://github.com/rust-lang/cargo/pull/11474)
- 新增一条 SemVer 兼容性规则，说明围绕诊断 lint 的期望
  [#11596](https://github.com/rust-lang/cargo/pull/11596)
- `cargo vendor` 对来自同一 git 仓库的每个修订版本
  生成不同的源替换条目。
  [#10690](https://github.com/rust-lang/cargo/pull/1090)
- Cargo 贡献者可通过 triagebot 重新为 issue 打标签。
  [doc](https://forge.rust-lang.org/triagebot/labeling.html)
  [#11498](https://github.com/rust-lang/cargo/pull/11498)
- Cargo 贡献者可在容器中编写测试。
  [#11583](https://github.com/rust-lang/cargo/pull/11583)

### 变更

- Cargo 现在默认将凭据保存到 `.cargo/credentials.toml`。
  若 `.cargo/credentials` 存在，则出于向后兼容写入该文件。
  [#11533](https://github.com/rust-lang/cargo/pull/11533)
- 为防止敏感数据被记录，Cargo 在内部引入了新的包装类型。
  [#11545](https://github.com/rust-lang/cargo/pull/11545)
- 若干文档改进。
  [#11475](https://github.com/rust-lang/cargo/pull/11475)
  [#11504](https://github.com/rust-lang/cargo/pull/11504)
  [#11516](https://github.com/rust-lang/cargo/pull/11516)
  [#11517](https://github.com/rust-lang/cargo/pull/11517)
  [#11568](https://github.com/rust-lang/cargo/pull/11568)
  [#11586](https://github.com/rust-lang/cargo/pull/11586)
  [#11592](https://github.com/rust-lang/cargo/pull/11592)

### 修复

- ❗ `cargo package` 与 `cargo publish` 现在会尊重工作区的 `Cargo.lock`。
  这是预期行为，但此前被遗漏。
  [#11477](https://github.com/rust-lang/cargo/pull/11477)
- 修复了 `cargo vendor` 在解析从工作区继承的 git 依赖时失败的问题。
  [#11414](https://github.com/rust-lang/cargo/pull/11414)
- 当指定了 `workspace.default-members` 时，`cargo install` 现在可以正确安装根包。
  [#11067](https://github.com/rust-lang/cargo/pull/11067)
- 修复了目标特定依赖错误时的 panic。
  [#11541](https://github.com/rust-lang/cargo/pull/11541)
- 若子命令没有手册页，则显示 `--help`。
  [#11473](https://github.com/rust-lang/cargo/pull/11473)
- 设置 `target.cfg(…).rustflags` 不应清除 `build.rustdocflags`。
  [#11323](https://github.com/rust-lang/cargo/pull/11323)
- 不支持的 `profile.split-debuginfo` 选项现在会被忽略，
  此前这会使 Cargo 在某些平台上编译失败。
  [#11347](https://github.com/rust-lang/cargo/pull/11347)
  [#11633](https://github.com/rust-lang/cargo/pull/11633)
- 在具有极长文件名的 Windows 无头会话中不再 panic。
  [#11759](https://github.com/rust-lang/cargo/pull/11759)

### 仅 Nightly

- 实现了 registry 非对称令牌认证的初始支持。
  ([RFC 3231](https://github.com/rust-lang/rfcs/blob/master/text/3231-cargo-asymmetric-tokens.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#registry-auth))
  [#10771](https://github.com/rust-lang/cargo/pull/10771)
- 在没有 `-Z sparse-registry` 时，不对 `auth-required: true` 报错
  [#11661](https://github.com/rust-lang/cargo/pull/11661)
- 支持配置文件中 profile 的 `codegen-backend` 与 `rustflags`。
  [#11562](https://github.com/rust-lang/cargo/pull/11562)
- 当警告/错误可用 clippy 修复时，建议使用 `cargo clippy --fix`。
  [#11399](https://github.com/rust-lang/cargo/pull/11399)
- 修复了在指定 target 字段且同时存在 `optional = true` 时 artifact 依赖不工作的问题。
  [#11434](https://github.com/rust-lang/cargo/pull/11434)
- 使 Cargo 区分带与不带 artifact 目标的 `Unit`。
  [#11478](https://github.com/rust-lang/cargo/pull/11478)
- `cargo metadata` 支持 artifact 依赖。
  [#11550](https://github.com/rust-lang/cargo/pull/11550)
- 允许在可选的文档抓取期间部分 crate 的构建失败。
  [#11450](https://github.com/rust-lang/cargo/pull/11450)
- 若潜在可抓取的示例因开发依赖而被跳过，则发出警告。
  [#11503](https://github.com/rust-lang/cargo/pull/11503)
- 默认不从库目标抓取示例。
  [#11499](https://github.com/rust-lang/cargo/pull/11499)
- 修复了 proc-macro crate 的示例被抓取的问题。
  [#11497](https://github.com/rust-lang/cargo/pull/11497)

## Cargo 1.67 (2023-01-26)
[7e484fc1...rust-1.67.0](https://github.com/rust-lang/cargo/compare/7e484fc1...rust-1.67.0)

### 新增

- `cargo remove` 现在在成功移除依赖后，会清理根
  工作区清单中引用的依赖，以及 `profile`、`patch` 与 `replace` 小节。
  [#11194](https://github.com/rust-lang/cargo/pull/11194)
  [#11242](https://github.com/rust-lang/cargo/pull/11242)
  [#11351](https://github.com/rust-lang/cargo/pull/11351)
- `cargo package` 与 `cargo publish` 现在在打包后报告
  crate 的总大小与压缩后大小。
  [#11270](https://github.com/rust-lang/cargo/pull/11270)

### 变更

- ❗ 若环境中已设置 `$CARGO`，Cargo 现在会复用该值，
  并在执行外部子命令与构建脚本时转发该值。
  [#11285](https://github.com/rust-lang/cargo/pull/11285)
- ❗ 在没有 `-p` 标志时运行 `cargo update --precise`，Cargo 现在会报错。
  [#11349](https://github.com/rust-lang/cargo/pull/11349)
- ❗ 若配置中存在多个具有相同索引 URL 的 registry，Cargo 现在会报错。
  [#10592](https://github.com/rust-lang/cargo/pull/10592)
- Cargo 现在在解压 crate 文件时会考虑压缩比。
  这放宽了 1.64.0 中为缓解 zip bomb 攻击而引入的硬性大小限制。
  [#11337](https://github.com/rust-lang/cargo/pull/11337)
- 在有未提交更改的 git 仓库上运行 `cargo fix` 时，Cargo 现在会报错退出。
  [#11400](https://github.com/rust-lang/cargo/pull/11400)
- 当 `cargo tree -i <spec>` 找不到任何包时，Cargo 现在会发出警告。
  [#11377](https://github.com/rust-lang/cargo/pull/11377)
- 运行 `cargo new/init` 且项目路径中包含 `PATH` 环境分隔符时，
  Cargo 现在会发出警告。
  [#11318](https://github.com/rust-lang/cargo/pull/11318)
- 当找到多个包且
  `cargo add/remove` 感到困惑时，错误消息更完善。
  [#11186](https://github.com/rust-lang/cargo/pull/11186)
  [#11375](https://github.com/rust-lang/cargo/pull/11375)
- 当 `cargo init` 但现有 ignore 文件不是 UTF-8 时，错误消息更完善。
  [#11321](https://github.com/rust-lang/cargo/pull/11321)
- `cargo install .` 的错误消息更完善。
  [#11401](https://github.com/rust-lang/cargo/pull/11401)
- 当多个构建目标中发现相同文件路径时，警告更完善。
  [#11299](https://github.com/rust-lang/cargo/pull/11299)
- 更新了内部 HTTP 库 libcurl，包含多项修复与更新。
  [#11307](https://github.com/rust-lang/cargo/pull/11307)
  [#11326](https://github.com/rust-lang/cargo/pull/11326)

### 修复

- 修复了 `cargo clean`，使其仅移除所请求包的指纹与
  构建脚本产物
  [#10621](https://github.com/rust-lang/cargo/pull/10621)
- 修复了在设置了配置 `registry.default` 时 `cargo install --index` 不工作的问题。
  [#11302](https://github.com/rust-lang/cargo/pull/11302)
- 修复了在未找到网络配置时 git2 safe-directory 被意外禁用的问题。
  [#11366](https://github.com/rust-lang/cargo/pull/11366)
- 从 crate `atty` 迁移，以解决潜在的 soundness 问题。
  [#11420](https://github.com/rust-lang/cargo/pull/11420)
- 清理 libgit2 索引被中断时留下的陈旧 git 临时文件。
  [#11308](https://github.com/rust-lang/cargo/pull/11308)

### 仅 Nightly

- 当某些编译警告/错误可自动修复时，建议使用 `cargo fix`。
  [#10989](https://github.com/rust-lang/cargo/pull/10989)
  [#11368](https://github.com/rust-lang/cargo/pull/11368)
- 将 `rustdoc-scrape-examples` 改为目标级配置。
  [#10343](https://github.com/rust-lang/cargo/pull/10343)
  [#11425](https://github.com/rust-lang/cargo/pull/11425)
  [#11430](https://github.com/rust-lang/cargo/pull/11430)
  [#11445](https://github.com/rust-lang/cargo/pull/11445)
- 将 artifact bin 依赖的变更传播到其父指纹。
  [#11353](https://github.com/rust-lang/cargo/pull/11353)
- 修复了 `wait-for-publish` 以支持 sparse registry。
  [#11356](https://github.com/rust-lang/cargo/pull/11356)
  [#11327](https://github.com/rust-lang/cargo/pull/11327)
  [#11388](https://github.com/rust-lang/cargo/pull/11388)
- 在 sparse registry 的 `SourceId` 中存储 `sparse+` 前缀
  [#11387](https://github.com/rust-lang/cargo/pull/11387)
  [#11403](https://github.com/rust-lang/cargo/pull/11403)
- 实现了替代 registry 认证支持。
  ([RFC 3139](https://github.com/rust-lang/rfcs/blob/master/text/3139-cargo-alternative-registry-auth.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#registry-auth))
  [#10592](https://github.com/rust-lang/cargo/pull/10592)
- 添加了配置选项 `registries.crates-io.protocol` 的文档。
  [#11350](https://github.com/rust-lang/cargo/pull/11350)

## Cargo 1.66.1 (2023-01-10)

### 修复
- 🚨 [CVE-2022-46176](https://github.com/rust-lang/cargo/security/advisories/GHSA-r5w3-xm58-jv6j)：
  为 git URL 增加了 SSH 主机密钥校验。
  关于如何配置 known host 密钥，详见[文档](appendix/git-authentication.md#ssh-known-hosts)。

## Cargo 1.66 (2022-12-15)
[08250398...rust-1.66.0](https://github.com/rust-lang/cargo/compare/08250398...rust-1.66.0)

### 新增

- 🎉 新增 `cargo remove` 命令，用于从 `Cargo.toml` 移除依赖。
  [docs](https://doc.rust-lang.org/nightly/cargo/commands/cargo-remove.html)
  [#11059](https://github.com/rust-lang/cargo/pull/11059)
  [#11099](https://github.com/rust-lang/cargo/pull/11099)
  [#11193](https://github.com/rust-lang/cargo/pull/11193)
  [#11204](https://github.com/rust-lang/cargo/pull/11204)
  [#11227](https://github.com/rust-lang/cargo/pull/11227)
- 新增对具有相对路径 git 子模块的 git 依赖的支持。
  [#11106](https://github.com/rust-lang/cargo/pull/11106)
- Cargo 现在向 registry 发送带有 `Accept-Encoding` 头的请求。
  [#11292](https://github.com/rust-lang/cargo/pull/11292)
- Cargo 现在将非 UTF8 参数转发给外部子命令。
  [#11118](https://github.com/rust-lang/cargo/pull/11118)

### 变更

- ❗ 从多个角度消除源替换的歧义。
  [RFC-3289](https://github.com/rust-lang/rfcs/blob/master/text/3289-source_replacement_ambiguity.md)
  [#10907](https://github.com/rust-lang/cargo/pull/10907)
  - 当 crates-io 源被替换时，用户在执行 API 操作时必须使用 `--registry <NAME>` 指定要使用的 registry。
  - 不再允许使用 crates.io 令牌（`registry.token`）向被源替换的 crates.io 发布。
  - 在源替换中，`replace-with` 键可以引用 `[registries]` 表中替代 registry 的名称。
- ❗ `cargo publish` 现在会阻塞，直到在索引中看到已发布的包。
  [#11062](https://github.com/rust-lang/cargo/pull/11062)
  [#11210](https://github.com/rust-lang/cargo/pull/11210)
  [#11216](https://github.com/rust-lang/cargo/pull/11216)
  [#11255](https://github.com/rust-lang/cargo/pull/11255)
- Cargo 现在使用 clap v4 库进行命令行参数解析。
  [#11116](https://github.com/rust-lang/cargo/pull/11116)
  [#11119](https://github.com/rust-lang/cargo/pull/11119)
  [#11159](https://github.com/rust-lang/cargo/pull/11159)
  [#11190](https://github.com/rust-lang/cargo/pull/11190)
  [#11239](https://github.com/rust-lang/cargo/pull/11239)
  [#11280](https://github.com/rust-lang/cargo/pull/11280)
- Cargo 现在仅在用户定义的别名遮蔽外部命令时发出警告。
  [#11170](https://github.com/rust-lang/cargo/pull/11170)
- 若干文档改进。
  [#10770](https://github.com/rust-lang/cargo/pull/10770)
  [#10938](https://github.com/rust-lang/cargo/pull/10938)
  [#11082](https://github.com/rust-lang/cargo/pull/11082)
  [#11093](https://github.com/rust-lang/cargo/pull/11093)
  [#11157](https://github.com/rust-lang/cargo/pull/11157)
  [#11185](https://github.com/rust-lang/cargo/pull/11185)
  [#11207](https://github.com/rust-lang/cargo/pull/11207)
  [#11219](https://github.com/rust-lang/cargo/pull/11219)
  [#11240](https://github.com/rust-lang/cargo/pull/11240)
  [#11241](https://github.com/rust-lang/cargo/pull/11241)
  [#11282](https://github.com/rust-lang/cargo/pull/11282)

### 修复

- ❗ 通过 `cargo --config <file>` 加载的配置文件现在优先于
  环境变量。这是已文档化的行为，但旧
  实现意外弄错了。
  [#11077](https://github.com/rust-lang/cargo/pull/11077)
- ❗ Cargo 更正确地收集 `target.cfg(…).rustflags` 中的 rustflags，
  并在不足以收敛时发出警告。
  [#11114](https://github.com/rust-lang/cargo/pull/11114)
- 链接器未移除的最终产物应在编译开始前被移除。
  [#11122](https://github.com/rust-lang/cargo/pull/11122)
- `cargo add` 现在以更易发现的方式报告未知 features。
  [#11098](https://github.com/rust-lang/cargo/pull/11098)
- Cargo 现在以更多错误上下文报告命令别名失败。
  [#11087](https://github.com/rust-lang/cargo/pull/11087)
- 当 `cargo login` 提示收到空输入时，错误消息更完善。
  [#11145](https://github.com/rust-lang/cargo/pull/11145)
- 在支持工作区继承的字段类型错误时，
  错误消息更完善。
  [#11113](https://github.com/rust-lang/cargo/pull/11113)
- 混合使用 feature 语法 `dep:` 与 `/` 时，错误消息更完善。
  [#11172](https://github.com/rust-lang/cargo/pull/11172)
- 发布时清单中 `package.publish` 为 `false` 时，
  错误消息更完善。
  [#11280](https://github.com/rust-lang/cargo/pull/11280)

### 仅 Nightly

- 在 `-Zpublish-timeout` 背后新增配置选项 `publish.timeout`。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#publish-timeout)
  [#11230](https://github.com/rust-lang/cargo/pull/11230)
- 为 sparse registry 新增重试支持。
  [#11069](https://github.com/rust-lang/cargo/pull/11069)
- 修复了 sparse registry 锁文件 URL 包含 `registry+sparse+` 的问题。
  [#11177](https://github.com/rust-lang/cargo/pull/11177)
- 新增配置选项 `registries.crates-io.protocol`
  以控制 crates.io 协议。
  [#11215](https://github.com/rust-lang/cargo/pull/11215)
- 移除了 index.crates.io 的 `sparse+` 前缀。
  [#11247](https://github.com/rust-lang/cargo/pull/11247)
- 修复了依赖 sparse registry 时的发布问题。
  [#11268](https://github.com/rust-lang/cargo/pull/11268)
- 修复了使用 `-Zsparse-registry` 时令人困惑的错误消息。
  [#11283](https://github.com/rust-lang/cargo/pull/11283)
- 修复了 sparse registry 的 410 gone 响应处理。
  [#11286](https://github.com/rust-lang/cargo/pull/11286)

## Cargo 1.65 (2022-11-03)
[4fd148c4...rust-1.65.0](https://github.com/rust-lang/cargo/compare/4fd148c4...rust-1.65.0)

### 新增

- 外部子命令现在可以从 Cargo 继承 jobserver 文件描述符。
  [#10511](https://github.com/rust-lang/cargo/pull/10511)
- 为 cargo-the-library 中的私有项添加了 API 文档。参见
  <https://doc.rust-lang.org/nightly/nightly-rustc/cargo>。
  [#11019](https://github.com/rust-lang/cargo/pull/11019)

### 变更

- 若 Cargo 的 bin 路径已在 `PATH` 中，Cargo 现在停止再添加。
  [#11023](https://github.com/rust-lang/cargo/pull/11023)
- 通过对待处理作业队列排序，
  改进了 Cargo 构建调度的性能。
  [#11032](https://github.com/rust-lang/cargo/pull/11032)
- 即使在 `rev` 字段中使用部分哈希，
  也改进了从 GitHub 获取 git 依赖的性能。
  [#10807](https://github.com/rust-lang/cargo/pull/10807)
- Cargo 现在使用 git2 v0.15 与 libgit2-sys v0.14，
  带来了与 git 新行为的若干兼容性修复。
  [#11004](https://github.com/rust-lang/cargo/pull/11004)
- Registry 索引文件基于内容哈希以更细粒度的方式缓存。
  [#11044](https://github.com/rust-lang/cargo/pull/11044)
- Cargo 现在使用标准库的 `std::thread::scope`，而不再使用
  `crossbeam` crate 来生成作用域线程。
  [#10977](https://github.com/rust-lang/cargo/pull/10977)
- Cargo 现在使用标准库的 `available_parallelism`，而不再使用
  `num_cpus` crate 来确定默认并行度。
  [#10969](https://github.com/rust-lang/cargo/pull/10969)
- 当看到 `rust-version` 要求未满足的错误消息时，
  Cargo 现在会指导你如何解决。
  [#10891](https://github.com/rust-lang/cargo/pull/10891)
- 当找不到子命令时，
  Cargo 现在会告知更多可能原因及如何修复。
  [#10924](https://github.com/rust-lang/cargo/pull/10924)
- 当给定的 Cargo 目标找不到时，Cargo 现在会列出可用的目标名称。
  [#10999](https://github.com/rust-lang/cargo/pull/10999)
- 若给出 `--precise` 但没有 `--package` 标志，`cargo update` 现在会发出警告。
  这将在过渡期后变为硬性错误。
  [#10988](https://github.com/rust-lang/cargo/pull/10988)
  [#11011](https://github.com/rust-lang/cargo/pull/11011)
- `cargo bench` 与 `cargo test` 现在在测试失败后立即报告
  更精确的测试执行错误。
  [#11028](https://github.com/rust-lang/cargo/pull/11028)
- `cargo add` 现在会告知 features 是为哪个版本添加的。
  [#11075](https://github.com/rust-lang/cargo/pull/11075)
- 指出 Rust 不再支持非 ASCII 的 crate 名称。
  [#11017](https://github.com/rust-lang/cargo/pull/11017)
- 增强了清单中字段期望为数组但使用了字符串时的
  错误消息。
  [#10944](https://github.com/rust-lang/cargo/pull/10944)

### 修复

- 移除了除 Linux 以外平台上对文件锁定支持的限制。
  [#10975](https://github.com/rust-lang/cargo/pull/10975)
- 通过将 os_info 提升至 3.5.0 修复了不正确的 OS 检测。
  [#10943](https://github.com/rust-lang/cargo/pull/10943)
- 扫描包目录时现在忽略来自已损坏但被排除的
  符号链接文件的错误。
  [#11008](https://github.com/rust-lang/cargo/pull/11008)
- 修复了构建脚本在 stdin 等待输入时的死锁。
  [#11257](https://github.com/rust-lang/cargo/pull/11257)

### Nightly

- sparse registry 的进度指示变得更直观。
  [#11068](https://github.com/rust-lang/cargo/pull/11068)

## Cargo 1.64 (2022-09-22)
[a5e08c47...rust-1.64.0](https://github.com/rust-lang/cargo/compare/a5e08c47...rust-1.64.0)

### 新增

- 🎉 包现在可以从工作区继承设置，从而将设置
  集中在一处。关于如何定义这些公共设置，参见
  [`workspace.package`](https://doc.rust-lang.org/nightly/cargo/reference/workspaces.html#the-package-table)
  与
  [`workspace.dependencies`](https://doc.rust-lang.org/nightly/cargo/reference/workspaces.html#the-dependencies-table)。
  [#10859](https://github.com/rust-lang/cargo/pull/10859)
- 为 `cargo rustc` 新增
  [`--crate-type`](https://doc.rust-lang.org/nightly/cargo/commands/cargo-rustc.html#option-cargo-rustc---crate-type)
  标志以覆盖 crate 类型。
  [#10838](https://github.com/rust-lang/cargo/pull/10838)
- Cargo 命令现在可以接受多个 `--target` 标志以一次为
  多个目标构建，并且
  [`build.target`](https://doc.rust-lang.org/nightly/cargo/reference/config.html#buildtarget)
  配置选项现在可以取多个目标的数组。
  [#10766](https://github.com/rust-lang/cargo/pull/10766)
- `--jobs` 参数现在可以取负数，以从最大 CPU 数
  向后倒数。
  [#10844](https://github.com/rust-lang/cargo/pull/10844)

### 变更
- `cargo install --path` 的 Bash 补全现在支持路径补全。
  [#10798](https://github.com/rust-lang/cargo/pull/10798)
- 在 `rev` 字段中使用哈希时，显著改进了从 GitHub
  获取 git 依赖的性能。
  [#10079](https://github.com/rust-lang/cargo/pull/10079)
- 已发布的包现在将包含来自工作区的 resolver 设置，
  以确保它们在独立使用时使用相同的解析器。
  [#10911](https://github.com/rust-lang/cargo/pull/10911)
  [#10961](https://github.com/rust-lang/cargo/pull/10961)
  [#10970](https://github.com/rust-lang/cargo/pull/10970)
- `cargo add` 现在会更新 `Cargo.lock`。
  [#10902](https://github.com/rust-lang/cargo/pull/10902)
- `cargo vendor` 配置输出中的路径现在将反斜杠
  转换为正斜杠，以便设置可跨平台工作。
  [#10668](https://github.com/rust-lang/cargo/pull/10668)
- [`workspace.default-members`](https://doc.rust-lang.org/nightly/cargo/reference/workspaces.html#package-selection)
  设置现在允许在非虚拟工作区中使用 `"."` 值以引用
  根包。
  [#10784](https://github.com/rust-lang/cargo/pull/10784)

### 修复

- 🚨 [CVE-2022-36113](https://github.com/rust-lang/cargo/security/advisories/GHSA-rfj2-q3h3-hm5j)：
  解压恶意 crate 可能破坏任意文件。
  [#11089](https://github.com/rust-lang/cargo/pull/11089)
  [#11088](https://github.com/rust-lang/cargo/pull/11088)
- 🚨 [CVE-2022-36114](https://github.com/rust-lang/cargo/security/advisories/GHSA-2hvr-h6gw-qrxp)：
  解压恶意 crate 可能填满文件系统。
  [#11089](https://github.com/rust-lang/cargo/pull/11089)
  [#11088](https://github.com/rust-lang/cargo/pull/11088)
- `cargo --version --verbose` 中的 `os` 输出现在支持更多平台。
  [#10802](https://github.com/rust-lang/cargo/pull/10802)
- 若缓存的 git checkout 已损坏，现在会重新构建。这可能发生在
  使用 `net.git-fetch-with-cli` 并中断克隆
  过程时。
  [#10829](https://github.com/rust-lang/cargo/pull/10829)
- 修复了 `cargo add --offline` 中的 panic。
  [#10817](https://github.com/rust-lang/cargo/pull/10817)


### 仅 Nightly
- 修复了 `config.toml` 中不稳定 `check-cfg` 的反序列化。
  [#10799](https://github.com/rust-lang/cargo/pull/10799)


## Cargo 1.63 (2022-08-11)
[3f052d8e...rust-1.63.0](https://github.com/rust-lang/cargo/compare/3f052d8e...rust-1.63.0)

### 新增

- 🎉 新增 `--config` CLI 选项，可直接在 CLI 上传递配置选项。
  [#10755](https://github.com/rust-lang/cargo/pull/10755)
- 若清单设置了 `rust-version` 字段，编译 crate 时现在会设置
  `CARGO_PKG_RUST_VERSION` 环境变量。
  [#10713](https://github.com/rust-lang/cargo/pull/10713)


### 变更
- 在 git 依赖中遇到多个同名包时会发出警告。
  这将忽略 `publish=false` 的包。
  [#10701](https://github.com/rust-lang/cargo/pull/10701)
  [#10767](https://github.com/rust-lang/cargo/pull/10767)
- 变更跟踪现在使用 `.json` 目标规范文件的内容，而非
  其路径。若路径变化，这应有助于避免重新构建。
  [#10746](https://github.com/rust-lang/cargo/pull/10746)
- 在 `.gitmodules` 中配置了 `update=none` 策略的子模块的
  git 依赖现在会被遵守，且不会获取该子模块。
  [#10717](https://github.com/rust-lang/cargo/pull/10717)
- Crate 文件现在使用更近的日期（2006 年 7 月 23 日而非 1973 年 11 月 29 日）
  以实现确定性行为。
  [#10720](https://github.com/rust-lang/cargo/pull/10720)
- `cargo new` 使用的初始模板现在包含稍更
  真实的测试结构，在测试模块中有 `use super::*;`。
  [#10706](https://github.com/rust-lang/cargo/pull/10706)
- 更新了内部 HTTP 库 libcurl，包含多项小修复与更新。
  [#10696](https://github.com/rust-lang/cargo/pull/10696)

### 修复
- 修复了 `cargo add` 与 `cargo locate-project` 的 zsh 补全
  [#10810](https://github.com/rust-lang/cargo/pull/10810)
  [#10811](https://github.com/rust-lang/cargo/pull/10811)
- 修复了在虚拟工作区根目录中 `cargo publish` 忽略 `-p` 的问题。
  还增加了额外检查，以便在选择了多个包时生成错误（此前会选取第一个）。
  [#10677](https://github.com/rust-lang/cargo/pull/10677)
- 使用 JSON 输出时，`cargo test` 不再显示人类可读的可执行文件名。
  [#10691](https://github.com/rust-lang/cargo/pull/10691)

### 仅 Nightly

- 新增 `-Zcheck-cfg=output`，以支持构建脚本通过
  `cargo:rustc-check-cfg` 声明其支持的 `cfg` 值集合。
  [#10539](https://github.com/rust-lang/cargo/pull/10539)
- `-Z sparse-registry` 在访问 crates-io 时现在使用 https://index.crates.io/。
  [#10725](https://github.com/rust-lang/cargo/pull/10725)
- 修复了 `cargo add` 中用于工作区继承的 `.workspace` 键的格式。
  [#10705](https://github.com/rust-lang/cargo/pull/10705)
- Sparse HTTP registry URL 现在必须以 `/` 结尾。
  [#10698](https://github.com/rust-lang/cargo/pull/10698)
- 修复了 `cargo add` 与工作区继承 `default-features` 键的问题。
  [#10685](https://github.com/rust-lang/cargo/pull/10685)

## Cargo 1.62 (2022-06-30)
[1ef1e0a1...rust-1.62.0](https://github.com/rust-lang/cargo/compare/1ef1e0a1...rust-1.62.0)

### 新增

- 🎉 新增 `cargo add` 命令，可从命令行向 `Cargo.toml` 添加依赖。
  [docs](https://doc.rust-lang.org/nightly/cargo/commands/cargo-add.html)
  [#10472](https://github.com/rust-lang/cargo/pull/10472)
  [#10577](https://github.com/rust-lang/cargo/pull/10577)
  [#10578](https://github.com/rust-lang/cargo/pull/10578)
- Package ID 规格现在除了先前的 `name:version` 外，还支持 `name@version` 语法，以与 `cargo add` 及其他工具的行为对齐。`cargo install` 和 `cargo yank` 现在也支持该语法，因此版本不必再作为单独的标志传入。
  [#10582](https://github.com/rust-lang/cargo/pull/10582)
  [#10650](https://github.com/rust-lang/cargo/pull/10650)
  [#10597](https://github.com/rust-lang/cargo/pull/10597)
- 新增 CLI 选项 `-F`，作为 `--features` 的别名。
  [#10576](https://github.com/rust-lang/cargo/pull/10576)
- Cargo 主目录（通常为 `~/.cargo`）中的 `git` 和 `registry` 目录现在被标记为缓存目录，因此不会被纳入备份或内容索引（在 Windows 上）。
  [#10553](https://github.com/rust-lang/cargo/pull/10553)
- 为 `cargo yank` 新增 `--version` 标志以替代 `--vers` 标志，从而与 `cargo install` 保持一致。
  [#10575](https://github.com/rust-lang/cargo/pull/10575)
- 新增自动 `@` argfile 支持：当传给 `rustc` 的命令行超出操作系统限制时，将使用“响应文件”。
  [#10546](https://github.com/rust-lang/cargo/pull/10546)
- `cargo clean` 现在有进度条（若耗时超过半秒）。
  [#10236](https://github.com/rust-lang/cargo/pull/10236)

### 变更

- 若未找到可安装的二进制文件（例如缺少必需的 features），`cargo install` 不再报错。
  [#10508](https://github.com/rust-lang/cargo/pull/10508)
- 若指定的 target 与主机 target 相同，`cargo test` 现在会将 `--target` 传给 `rustdoc`。
  [#10594](https://github.com/rust-lang/cargo/pull/10594)
- 为二进制文件生成文档时，`cargo doc` 现在会自动传入 `-Arustdoc::private-intra-doc-links`（这会自动包含 `--document-private-items`）。
  [`private-intra-doc-links`](https://doc.rust-lang.org/rustdoc/lints.html#private_intra_doc_links)
  lint 仅在*不*为私有项生成文档时才相关，而这不适用于二进制文件。
  [#10142](https://github.com/rust-lang/cargo/pull/10142)
- `cargo --version` 输出中短 git hash 的长度现在固定为 9 个字符。此前不同平台上的长度不一致。
  [#10579](https://github.com/rust-lang/cargo/pull/10579)
- 尝试发布包含 `Cargo.toml.orig` 文件的包现在会报错。否则该文件名会与自动生成的文件冲突。
  [#10551](https://github.com/rust-lang/cargo/pull/10551)

### 修复

- `build.dep-info-basedir` 配置设置现在正确支持在路径中使用 `..` 来引用父目录。
  [#10281](https://github.com/rust-lang/cargo/pull/10281)
- 修复了在使用 cgroups v1 的系统上自动检测默认 CPU 数量的回归。
  [#10737](https://github.com/rust-lang/cargo/pull/10737)
  [#10739](https://github.com/rust-lang/cargo/pull/10739)


### 仅 Nightly

- `cargo fetch` 现在可与 `-Zbuild-std` 一起使用，以获取标准库的依赖。
  [#10129](https://github.com/rust-lang/cargo/pull/10129)
- 新增对 workspace inheritance 的支持。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#workspace-inheritance)
  [#10584](https://github.com/rust-lang/cargo/pull/10584)
  [#10568](https://github.com/rust-lang/cargo/pull/10568)
  [#10565](https://github.com/rust-lang/cargo/pull/10565)
  [#10564](https://github.com/rust-lang/cargo/pull/10564)
  [#10563](https://github.com/rust-lang/cargo/pull/10563)
  [#10606](https://github.com/rust-lang/cargo/pull/10606)
  [#10548](https://github.com/rust-lang/cargo/pull/10548)
  [#10538](https://github.com/rust-lang/cargo/pull/10538)
- 新增 `-Zcheck-cfg`，以多种形式校验 `cfg` 表达式中的未知名称和值。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#check-cfg)
  [#10486](https://github.com/rust-lang/cargo/pull/10486)
  [#10566](https://github.com/rust-lang/cargo/pull/10566)
- `--config` CLI 选项不再允许设置 registry token。
  [#10580](https://github.com/rust-lang/cargo/pull/10580)
- 修复了 proc-macros 与 `-Z rustdoc-scrape-examples` 相关的问题。
  [#10549](https://github.com/rust-lang/cargo/pull/10549)
  [#10533](https://github.com/rust-lang/cargo/pull/10533)


## Cargo 1.61 (2022-05-19)
[ea2a21c9...rust-1.61.0](https://github.com/rust-lang/cargo/compare/ea2a21c9...rust-1.61.0)

### 新增

### 变更

- `cargo test --no-run` 现在会显示测试可执行文件的路径。
  [#10346](https://github.com/rust-lang/cargo/pull/10346)
- `cargo tree --duplicates` 不再将主机与 target 之间共享的依赖报告为重复。
  [#10466](https://github.com/rust-lang/cargo/pull/10466)
- 更新到 libgit2 的 1.4.2 版本，带来若干修复
  [#10442](https://github.com/rust-lang/cargo/pull/10442)
  [#10479](https://github.com/rust-lang/cargo/pull/10479)
- `cargo vendor` 不再允许为 `--sync` 传入多个值，必须改为多次传入 `--sync` 标志。
  [#10448](https://github.com/rust-lang/cargo/pull/10448)
- 现在会对同时混用下划线与短横线变体的 manifest 键发出警告（例如同时指定 `proc_macro` 和 `proc-macro`）
  [#10316](https://github.com/rust-lang/cargo/pull/10316)
- Cargo 现在使用标准库的 `available_parallelism` 而非 `num_cpus` crate 来确定默认并行度。
  [#10427](https://github.com/rust-lang/cargo/pull/10427)
- `cargo search` 的搜索词现在会高亮显示。
  [#10425](https://github.com/rust-lang/cargo/pull/10425)

### 修复

- 传给 `hg` 等 VCS 工具的路径现在会加在 `--` 之后，以避免与 VCS 标志冲突。
  [#10483](https://github.com/rust-lang/cargo/pull/10483)
- 修复了 `http.timeout` 配置值使其真正生效。
  [#10456](https://github.com/rust-lang/cargo/pull/10456)
- 修复了 `cargo rustc --crate-type` 在某些情况下不工作的问题。
  [#10388](https://github.com/rust-lang/cargo/pull/10388)

### 仅 Nightly

- 新增 `-Z check-cfg-features` 以启用 features 的编译期检查
  [#10408](https://github.com/rust-lang/cargo/pull/10408)
- 新增 `-Z bindeps` 以支持二进制产物依赖（RFC-3028）
  [#9992](https://github.com/rust-lang/cargo/pull/9992)
- `-Z multitarget` 现在可在 `build.target` 配置值中以数组形式使用。
  [#10473](https://github.com/rust-lang/cargo/pull/10473)
- 新增 `--keep-going` 标志，即使某个 crate 编译失败也会继续编译。
  [#10383](https://github.com/rust-lang/cargo/pull/10383)
- 开始在 workspace 中继承 manifest 值的相关工作。
  [#10497](https://github.com/rust-lang/cargo/pull/10497)
  [#10517](https://github.com/rust-lang/cargo/pull/10517)
- 新增对稀疏 HTTP registries 的支持。
  [#10470](https://github.com/rust-lang/cargo/pull/10470)
  [#10064](https://github.com/rust-lang/cargo/pull/10064)
- 修复了 artifact target 用于 `[target.'cfg(<target>)'.dependencies]` 时的 panic
  [#10433](https://github.com/rust-lang/cargo/pull/10433)
- 修复了传给构建脚本的主机标志（`-Z target-applies-to-host`）
  [#10395](https://github.com/rust-lang/cargo/pull/10395)
- 为 rustdoc 新增 `-Z check-cfg-features` 支持
  [#10428](https://github.com/rust-lang/cargo/pull/10428)


## Cargo 1.60 (2022-04-07)
[358e79fe...rust-1.60.0](https://github.com/rust-lang/cargo/compare/358e79fe...rust-1.60.0)

### 新增

- 🎉 在 `[features]` 表中新增 `dep:` 前缀，用于引用可选依赖。这允许创建与依赖同名的 feature 名称，并允许“隐藏”可选依赖，使其不会隐式暴露一个 feature 名称。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/features.html#optional-dependencies)
  [#10269](https://github.com/rust-lang/cargo/pull/10269)
- 🎉 在 `[features]` 表中新增 `dep-name?/feature-name` 语法，仅当可选依赖 `dep-name` 已被某个其他 feature 启用时，才启用 feature `feature-name`。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/features.html#dependency-features)
  [#10269](https://github.com/rust-lang/cargo/pull/10269)
- 🎉 新增 `--timings` 选项，可生成关于构建耗时、并发与 CPU 使用的 HTML 报告。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/timings.html)
  [#10245](https://github.com/rust-lang/cargo/pull/10245)
- 在 registry index 中新增 `"v"` 和 `"features2"` 字段。
  `"v"` 字段为未来 index 变更提供兼容方法。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/registries.html#index-format)
  [#10269](https://github.com/rust-lang/cargo/pull/10269)
- 为 `cargo clippy` 新增 bash 补全
  [#10347](https://github.com/rust-lang/cargo/pull/10347)
- 为 `cargo report` 新增 bash 补全
  [#10295](https://github.com/rust-lang/cargo/pull/10295)
- 为构建脚本新增对 `rustc-link-arg-tests`、`rustc-link-arg-examples` 和 `rustc-link-arg-benches` 的支持。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/build-scripts.html#outputs-of-the-build-script)
  [#10274](https://github.com/rust-lang/cargo/pull/10274)

### 变更

- Cargo 现在使用 clap 3 库进行命令行参数解析。
  [#10265](https://github.com/rust-lang/cargo/pull/10265)
- `build.pipelining` 配置选项现已弃用，pipelining 现在将始终启用。
  [#10258](https://github.com/rust-lang/cargo/pull/10258)
- `cargo new` 现在生成的 `.gitignore` 仅忽略仓库根目录下的 `Cargo.lock`，而非任意目录。
  [#10379](https://github.com/rust-lang/cargo/pull/10379)
- 改进了 bash 补全的启动时间。
  [#10365](https://github.com/rust-lang/cargo/pull/10365)
- 与 `--all-features` 标志一起使用时，`--features` 标志现在会被遵循，从而允许启用其他包的 features。
  [#10337](https://github.com/rust-lang/cargo/pull/10337)
- Cargo 现在使用不同的 TOML 解析器。这不应引入任何用户可见的变更。这为支持可保留格式的程序化修改 TOML 文件铺平道路，以支持 `cargo add` 及其他未来增强。
  [#10086](https://github.com/rust-lang/cargo/pull/10086)
- 将库设置为同时产出 `dylib` 和 `cdylib` 现在是错误，因为不支持该组合。
  [#10243](https://github.com/rust-lang/cargo/pull/10243)
- `cargo --list` 现在包含 `help` 命令。
  [#10300](https://github.com/rust-lang/cargo/pull/10300)

### 修复

- 修复了对带有 dev-dependencies 的 examples 运行 `cargo doc`。
  [#10341](https://github.com/rust-lang/cargo/pull/10341)
- 修复了 `cargo install --path`：当路径相对于当前目录下 workspace 之外的目录时的问题。
  [#10335](https://github.com/rust-lang/cargo/pull/10335)
- `cargo test TEST_FILTER` 不应再构建被显式以 `test = false` 禁用的二进制文件。
  [#10305](https://github.com/rust-lang/cargo/pull/10305)
- 修复了有 `term.verbose` 而无 `term.quiet`（以及反过来）时的回归。
  [#10429](https://github.com/rust-lang/cargo/pull/10429)
  [#10436](https://github.com/rust-lang/cargo/pull/10436)

### 仅 Nightly

- 为 profile 定义新增 `rustflags` 选项。
  [#10217](https://github.com/rust-lang/cargo/pull/10217)
- 变更 `--config`，使其仅支持点分键。
  [#10176](https://github.com/rust-lang/cargo/pull/10176)
- 修复了 profile `rustflags` 在 profile overrides 中未受门控的问题。
  [#10411](https://github.com/rust-lang/cargo/pull/10411)
  [#10413](https://github.com/rust-lang/cargo/pull/10413)

## Cargo 1.59 (2022-02-24)
[7f08ace4...rust-1.59.0](https://github.com/rust-lang/cargo/compare/7f08ace4...rust-1.59.0)

### 新增

- 🎉 现在可以在 profile 中指定 `strip` 选项，以指定从二进制文件中移除符号与调试信息的行为。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/profiles.html#strip)
  [#10088](https://github.com/rust-lang/cargo/pull/10088)
  [#10376](https://github.com/rust-lang/cargo/pull/10376)
- 🎉 新增未来不兼容报告。
  这可在 `rustc` 的未来变更可能导致某个包或其任一依赖停止构建时提供报告。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/future-incompat-report.html)
  [#10165](https://github.com/rust-lang/cargo/pull/10165)
- Windows 上的 SSH 认证现在支持 ssh-agent。
  [docs](https://doc.rust-lang.org/nightly/cargo/appendix/git-authentication.html#ssh-authentication)
  [#10248](https://github.com/rust-lang/cargo/pull/10248)
- 新增 `term.quiet` 配置选项，可从配置文件启用 `--quiet` 行为。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#termquiet)
  [#10152](https://github.com/rust-lang/cargo/pull/10152)
- 新增 `-r` CLI 选项，作为 `--release` 的别名。
  [#10133](https://github.com/rust-lang/cargo/pull/10133)

### 变更

- 扫描包目录现在应对错误更具韧性，例如文件系统环或访问问题。
  [#10188](https://github.com/rust-lang/cargo/pull/10188)
  [#10214](https://github.com/rust-lang/cargo/pull/10214)
  [#10286](https://github.com/rust-lang/cargo/pull/10286)
- `cargo help <alias>` 现在会显示该别名的目标。
  [#10193](https://github.com/rust-lang/cargo/pull/10193)
- 移除了已弃用的 `--host` CLI 选项。
  [#10145](https://github.com/rust-lang/cargo/pull/10145)
  [#10327](https://github.com/rust-lang/cargo/pull/10327)
- Cargo 现在应报告其版本始终与 `rustc` 同步。
  [#10178](https://github.com/rust-lang/cargo/pull/10178)
- 将 EOPNOTSUPP 加入被忽略的文件锁定错误，这与 BSD 操作系统相关。
  [#10157](https://github.com/rust-lang/cargo/pull/10157)

### 修复

- macOS：修复了运行可执行文件会偶发被内核杀死的问题（可能始于 macOS 12）。
  [#10196](https://github.com/rust-lang/cargo/pull/10196)
- 修复了依赖的 `[lib]` 定义中 `doc=false` 设置会被遵循。
  [#10201](https://github.com/rust-lang/cargo/pull/10201)
  [#10324](https://github.com/rust-lang/cargo/pull/10324)
- JSON 选项中的 `"executable"` 字段在为二进制文件生成文档时错误地包含了 `index.html` 的路径。现在为 null。
  [#10171](https://github.com/rust-lang/cargo/pull/10171)
- 为二进制文件生成文档现在会等待包的库完成文档生成后再开始。这修复了若二进制文件对库有 intra-doc 链接时的一些竞态条件。
  [#10172](https://github.com/rust-lang/cargo/pull/10172)
- 修复了向已关闭的管道显示帮助文本时的 panic。
  [#10164](https://github.com/rust-lang/cargo/pull/10164)

### 仅 Nightly
- 为 `cargo rustc` 新增 `--crate-type` 标志。
  [#10093](https://github.com/rust-lang/cargo/pull/10093)


## Cargo 1.58 (2022-01-13)
[b2e52d7c...rust-1.58.0](https://github.com/rust-lang/cargo/compare/b2e52d7c...rust-1.58.0)

### 新增

- 在 `cargo metadata` 的包数据中新增 `rust_version` 字段。
  [#9967](https://github.com/rust-lang/cargo/pull/9967)
- 为 `cargo install` 新增 `--message-format` 选项。
  [#10107](https://github.com/rust-lang/cargo/pull/10107)

### 变更

- 当别名遮蔽外部命令时，现在会显示警告。
  [#10082](https://github.com/rust-lang/cargo/pull/10082)
- 将 curl 更新到 7.80.0。
  [#10040](https://github.com/rust-lang/cargo/pull/10040)
  [#10106](https://github.com/rust-lang/cargo/pull/10106)

### 修复

- Doctests 现在会包含来自构建脚本的 rustc-link-args。
  [#9916](https://github.com/rust-lang/cargo/pull/9916)
- 修复了 `cargo tree` 在有环状 dev-dependencies 时进入无限循环的问题。
  修复了 resolver 无法处理带有 feature 的环状 dev-dependency 的边界情况。
  [#10103](https://github.com/rust-lang/cargo/pull/10103)
- 修复了当目录路径包含 glob 字符时的 `cargo clean -p`。
  [#10072](https://github.com/rust-lang/cargo/pull/10072)
- 修复了 `cargo` 的 debug 构建：当服务器重定向带有非空正文时，下载 crate 可能 panic。
  [#10048](https://github.com/rust-lang/cargo/pull/10048)

### 仅 Nightly

- 使 future-incompat-report 输出更友好。
  [#9953](https://github.com/rust-lang/cargo/pull/9953)
- 新增支持从 `examples` 目录抓取代码示例以包含在文档中。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#scrape-examples)
  [#9525](https://github.com/rust-lang/cargo/pull/9525)
  [#10037](https://github.com/rust-lang/cargo/pull/10037)
  [#10017](https://github.com/rust-lang/cargo/pull/10017)
- 修复了 `cargo report future-incompatibilities`：检查 stdout 是否支持颜色。
  [#10024](https://github.com/rust-lang/cargo/pull/10024)

## Cargo 1.57 (2021-12-02)
[18751dd3...rust-1.57.0](https://github.com/rust-lang/cargo/compare/18751dd3...rust-1.57.0)

### 新增

- 🎉 新增自定义命名 profiles。这也使 `test` 和 `bench` profiles 从其 `dev` 和 `release` 继承设置，并且 Cargo 现在在给定命令期间只使用单一 profile，而不再对依赖与 cargo-targets 使用不同 profiles。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/profiles.html#custom-profiles)
  [#9943](https://github.com/rust-lang/cargo/pull/9943)
- git 依赖的 `rev` 选项现在支持以 `refs/` 开头的 git 引用。一个可用示例是在类似 GitHub 的服务上，于拉取请求合并之前依赖它。
  [#9859](https://github.com/rust-lang/cargo/pull/9859)
- 在 `.cargo_vcs_info.json` 文件中新增 `path_in_vcs` 字段。
  [docs](https://doc.rust-lang.org/nightly/cargo/commands/cargo-package.html#cargo_vcs_infojson-format)
  [#9866](https://github.com/rust-lang/cargo/pull/9866)

### 变更

- ❗ 构建脚本不再设置 `RUSTFLAGS`。该变更在 1.55 中已做出，但发布说明未突出强调。构建脚本应改用 `CARGO_ENCODED_RUSTFLAGS`。更多细节见
  [documentation](https://doc.rust-lang.org/nightly/cargo/reference/environment-variables.html#environment-variables-cargo-sets-for-build-scripts)。
- `cargo version` 命令现在包含一些额外信息。
  [#9968](https://github.com/rust-lang/cargo/pull/9968)
- 将 libgit2 更新到 1.3，带来若干关于 git 处理的修复与变更。
  [#9963](https://github.com/rust-lang/cargo/pull/9963)
  [#9988](https://github.com/rust-lang/cargo/pull/9988)
- Shell 补全现在包含简写 b/r/c/d 子命令。
  [#9951](https://github.com/rust-lang/cargo/pull/9951)
- `cargo update --precise` 现在允许指定不含 semver 元数据（版本号中 `+` 之后的内容）的版本。
  [#9945](https://github.com/rust-lang/cargo/pull/9945)
- zsh 补全现在可补全 `--example` 名称。
  [#9939](https://github.com/rust-lang/cargo/pull/9939)
- 进度条现在会区分正在构建 unittests 的情况。
  [#9934](https://github.com/rust-lang/cargo/pull/9934)
- 对无效 TOML 语法的一些向后兼容支持已被移除。
  [#9932](https://github.com/rust-lang/cargo/pull/9932)
- 撤销了 1.55 中对未包含任何字段的依赖规格触发错误的变更。
  [#9911](https://github.com/rust-lang/cargo/pull/9911)

### 修复

- 移除了一条可能泄漏 token 的日志消息（来自 `CARGO_LOG`）。
  [#9873](https://github.com/rust-lang/cargo/pull/9873)
- `cargo fix` 现在会避免将修复写入全局 registry 缓存。
  [#9938](https://github.com/rust-lang/cargo/pull/9938)
- 修复了与简写别名（b/c/r/d）一起使用时的 `-Z help` CLI 选项。
  [#9933](https://github.com/rust-lang/cargo/pull/9933)


### 仅 Nightly


## Cargo 1.56 (2021-10-21)
[cebef295...rust-1.56.0](https://github.com/rust-lang/cargo/compare/cebef295...rust-1.56.0)

### 新增

- 🎉 Cargo 现在支持 2021 edition。
  更多信息见 [edition
  guide](https://doc.rust-lang.org/nightly/edition-guide/rust-2021/index.html)。
  [#9800](https://github.com/rust-lang/cargo/pull/9800)
- 🎉 在 `Cargo.toml` 中新增
  [`rust-version`](https://doc.rust-lang.org/nightly/cargo/reference/manifest.html#the-rust-version-field)
  字段以指定最低支持的 Rust 版本，以及用于覆盖它的 `--ignore-rust-version` 命令行选项。
  [#9732](https://github.com/rust-lang/cargo/pull/9732)
- 在配置文件中新增 `[env]` 表，用于指定要设置的环境变量。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#env)
  [#9411](https://github.com/rust-lang/cargo/pull/9411)
- 现在可在配置文件中指定 `[patch]` 表。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#patch)
  [#9839](https://github.com/rust-lang/cargo/pull/9839)
- `cargo doc` 现在支持 `--example` 和 `--examples` 标志。
  [#9808](https://github.com/rust-lang/cargo/pull/9808)
- 🎉 构建脚本现在可为二进制文件或所有可链接目标传递额外的链接器参数。[docs](https://doc.rust-lang.org/nightly/cargo/reference/build-scripts.html#outputs-of-the-build-script)
  [#9557](https://github.com/rust-lang/cargo/pull/9557)
- 为 `cargo publish` 新增对 `-p` 标志的支持，以便发布 workspace 中的特定包。`cargo package` 现在也支持 `-p` 和 `--workspace`。
  [#9559](https://github.com/rust-lang/cargo/pull/9559)
- 新增关于第三方 registries 的文档。
  [#9830](https://github.com/rust-lang/cargo/pull/9830)
- 为 registry `config.json` 中的 URL 新增 `{sha256-checksum}` 占位符。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/registries.html#index-format)
  [#9801](https://github.com/rust-lang/cargo/pull/9801)
- 当依赖没有库时新增警告。
  [#9771](https://github.com/rust-lang/cargo/pull/9771)

### 变更

- Doc tests 现在支持 `-q` 标志以显示简洁的测试输出。
  [#9730](https://github.com/rust-lang/cargo/pull/9730)
- 在 `[replace]` 表中使用的 `features` 现在会发出警告，因为它们会被忽略。
  [#9681](https://github.com/rust-lang/cargo/pull/9681)
- 变更使得仅 `wasm32-unknown-emscripten` 可执行文件在文件名中不带 hash 构建。此前是所有 `wasm32` 目标。
  此外，所有 `apple` 二进制文件现在在文件名中带 hash 构建。这允许同时缓存多个副本，并与其他平台（除 `msvc` 外）的行为一致。
  [#9653](https://github.com/rust-lang/cargo/pull/9653)
- `cargo new` 现在生成的 example 不会在 clippy 下产生警告。
  [#9796](https://github.com/rust-lang/cargo/pull/9796)
- `cargo fix --edition` 现在仅应用 edition 特定的 lints。
  [#9846](https://github.com/rust-lang/cargo/pull/9846)
- 改进 resolver 消息以包含依赖要求。
  [#9827](https://github.com/rust-lang/cargo/pull/9827)
- `cargo fix` 现在可通过 `CARGO_LOG` 环境变量获得更多调试日志。
  [#9831](https://github.com/rust-lang/cargo/pull/9831)
- 变更 `cargo fix --edition`：在 stable 上运行且已处于最新 stable edition 时发出警告，而非报错。
  [#9792](https://github.com/rust-lang/cargo/pull/9792)
- `cargo install` 现在会在开始安装前确定所有要安装的包，这应有助于在未部分安装的情况下报告错误。
  [#9793](https://github.com/rust-lang/cargo/pull/9793)
- `cargo fix --edition` 的 resolver 报告现在包含 dev-dependencies 的差异。
  [#9803](https://github.com/rust-lang/cargo/pull/9803)
- `cargo fix` 现在会对来自 `rustc` 的异常错误显示更好的诊断。
  [#9799](https://github.com/rust-lang/cargo/pull/9799)
- `cargo --list` 中的条目现在会去重。
  [#9773](https://github.com/rust-lang/cargo/pull/9773)
- 别名现在包含在 `cargo --list` 中。
  [#9764](https://github.com/rust-lang/cargo/pull/9764)

### 修复

- 修复了 proc-macro 的 build-std 时的 panic。
  [#9834](https://github.com/rust-lang/cargo/pull/9834)
- 修复了在运行 `cargo fix` 时从 proc-macros 递归运行 `cargo`。
  [#9818](https://github.com/rust-lang/cargo/pull/9818)
- 对命令别名环返回错误，而非栈溢出。
  [#9791](https://github.com/rust-lang/cargo/pull/9791)
- 更新到 curl 7.79.1，希望能修复间歇性的 http2 错误。
  [#9937](https://github.com/rust-lang/cargo/pull/9937)

### 仅 Nightly

- 新增 `[future-incompat-report]` 配置节。
  [#9774](https://github.com/rust-lang/cargo/pull/9774)
- 修复了自定义命名 profiles 的 value-after-table 错误。
  [#9789](https://github.com/rust-lang/cargo/pull/9789)
- 新增 `different-binary-name` feature，以支持为二进制名称指定非 rust 标识符。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#different-binary-name)
  [#9627](https://github.com/rust-lang/cargo/pull/9627)
- 新增用于选择 codegen backend 的 profile 选项。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#codegen-backend)
  [#9118](https://github.com/rust-lang/cargo/pull/9118)


## Cargo 1.55 (2021-09-09)
[aa8b0929...rust-1.55.0](https://github.com/rust-lang/cargo/compare/aa8b0929...rust-1.55.0)

### 新增

- `cargo metadata` 中的包定义现在包含来自 manifest 的 `"default_run"` 字段。
  [#9550](https://github.com/rust-lang/cargo/pull/9550)
- ❗ 构建脚本现在可访问以下环境变量：
  `RUSTC_WRAPPER`、`RUSTC_WORKSPACE_WRAPPER`、`CARGO_ENCODED_RUSTFLAGS`。
  构建脚本不再设置 `RUSTFLAGS`；应改用 `CARGO_ENCODED_RUSTFLAGS`。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/environment-variables.html#environment-variables-cargo-sets-for-build-scripts)
  [#9601](https://github.com/rust-lang/cargo/pull/9601)
- 新增 `cargo d` 作为 `cargo doc` 的别名。
  [#9680](https://github.com/rust-lang/cargo/pull/9680)
- 在 `cargo tree --format` 选项中新增 `{lib}`，以显示包的库名称。
  [#9663](https://github.com/rust-lang/cargo/pull/9663)
- 为 `Workspace` API 新增 `members_mut` 方法。
  [#9547](https://github.com/rust-lang/cargo/pull/9547)

### 变更

- 使用 `--all-targets`、`--bins`、`--tests`、`--examples` 或 `--benches` 标志时，若构建命令未匹配任何目标，现在会显示警告以告知没有匹配的目标。
  [#9549](https://github.com/rust-lang/cargo/pull/9549)
- `cargo init` 检测现有源文件是二进制还是库的方式已变更，改为尊重命令行标志，而不再尝试猜测类型。
  [#9522](https://github.com/rust-lang/cargo/pull/9522)
- 在可能时现在显示 registry 名称而非 registry URL。
  [#9632](https://github.com/rust-lang/cargo/pull/9632)
- 不再显示重复的编译器诊断。这在 `cargo test` 并行构建同一代码的多份副本时经常发生。
  这也会更新警告摘要以提供更多上下文。
  [#9675](https://github.com/rust-lang/cargo/pull/9675)
- 警告或错误的输出现在已改进，更精简、更清晰，并显示更多上下文。
  [#9655](https://github.com/rust-lang/cargo/pull/9655)
- 网络发送错误现在被视为“spurious”，意味着会重试。
  [#9695](https://github.com/rust-lang/cargo/pull/9695)
- 非 git 依赖上的 Git 键（`branch`、`tag`、`rev`）现在是错误。
  此外，同时指定 `git` 和 `path` 现在也是错误。
  [#9689](https://github.com/rust-lang/cargo/pull/9689)
- 不带任何键指定依赖现在是错误。
  [#9686](https://github.com/rust-lang/cargo/pull/9686)
- resolver 现在在可能时优先使用依赖的 `[patch]` 表条目。
  [#9639](https://github.com/rust-lang/cargo/pull/9639)
- 依赖中的包名拼写错误现在会与原文对齐显示，以便更容易看出差异。
  [#9665](https://github.com/rust-lang/cargo/pull/9665)
- Windows 平台现在可能对大小写错误的环境变量发出警告。
  [#9654](https://github.com/rust-lang/cargo/pull/9654)
- 在 `[patch]` 表中使用的 `features` 现在会发出警告，因为它们会被忽略。
  [#9666](https://github.com/rust-lang/cargo/pull/9666)
- 在 Windows 上，`target` 目录现在被排除在内容索引之外。
  [#9635](https://github.com/rust-lang/cargo/pull/9635)
- 找不到 `Cargo.toml` 时，错误消息现在会检测是否因小写 `c` 而命名错误，并建议正确形式。
  [#9607](https://github.com/rust-lang/cargo/pull/9607)
- 使用新 resolver 构建 `diesel` 时会显示兼容性提示。
  [#9602](https://github.com/rust-lang/cargo/pull/9602)
- 更新了处理打开网页浏览器的 `opener` 依赖，包含若干变更，例如在 WSL 上运行时的新行为，以及在 Linux 上使用系统的 `xdg-open`。
  [#9583](https://github.com/rust-lang/cargo/pull/9583)
- 更新到 libcurl 7.78。
  [#9809](https://github.com/rust-lang/cargo/pull/9809)
  [#9810](https://github.com/rust-lang/cargo/pull/9810)

### 修复

- 修复了 dep-info 文件包含非本地构建脚本路径的问题。
  [#9596](https://github.com/rust-lang/cargo/pull/9596)
- 处理 cargo 配置文件中 “jobs = 0” 的情况
  [#9584](https://github.com/rust-lang/cargo/pull/9584)
- 实现对 `--` 之后被忽略的尾随参数的警告
  [#9561](https://github.com/rust-lang/cargo/pull/9561)
- 修复了 rustc/rustdoc 配置值相对于配置的路径解析。
  [#9566](https://github.com/rust-lang/cargo/pull/9566)
- `cargo fix` 现在支持 rustc 带有多个 spans 的建议。
  [#9567](https://github.com/rust-lang/cargo/pull/9567)
- `cargo fix` 现在串行修复每个目标，而非并行，以避免并发修复同一文件的问题。
  [#9677](https://github.com/rust-lang/cargo/pull/9677)
- 对目标 `linker` 配置值的变更现在会触发重建。
  [#9647](https://github.com/rust-lang/cargo/pull/9647)
- 使用 `cargo publish` 或 `cargo package` 的 `--allow-dirty` 标志时，现在会忽略 Git 未暂存的已删除文件。
  [#9645](https://github.com/rust-lang/cargo/pull/9645)

### 仅 Nightly

- 启用了对 2021 的 `cargo fix --edition` 支持。
  [#9588](https://github.com/rust-lang/cargo/pull/9588)
- 对命名 profiles 的若干变更。
  [#9685](https://github.com/rust-lang/cargo/pull/9685)
- 扩展了在 2021 edition 上运行 `cargo fix --edition` 时应做什么的说明。
  [#9694](https://github.com/rust-lang/cargo/pull/9694)
- 对使用 nightly features 的错误消息进行多项更新，以更好地解释情况。
  [#9657](https://github.com/rust-lang/cargo/pull/9657)
- 调整了 edition 2021 resolver 差异报告。
  [#9649](https://github.com/rust-lang/cargo/pull/9649)
- 修复了与 `doc.extern-map` 一起使用 `cargo doc --open` 时的错误。
  [#9531](https://github.com/rust-lang/cargo/pull/9531)
- 统一了 weak 与 namespaced features。
  [#9574](https://github.com/rust-lang/cargo/pull/9574)
- 对 future-incompatible 报告的各项更新。
  [#9606](https://github.com/rust-lang/cargo/pull/9606)
- `[env]` 环境变量不允许设置由 Cargo 设置的变量。
  [#9579](https://github.com/rust-lang/cargo/pull/9579)

## Cargo 1.54 (2021-07-29)
[4369396c...rust-1.54.0](https://github.com/rust-lang/cargo/compare/4369396c...rust-1.54.0)

### 新增

- 从 git 仓库（例如 crates.io index）获取时现在会显示网络传输速率。
  [#9395](https://github.com/rust-lang/cargo/pull/9395)
- 为 `cargo tree` 新增 `--prune` 选项以限制显示内容。
  [#9520](https://github.com/rust-lang/cargo/pull/9520)
- 为 `cargo tree` 新增 `--depth` 选项以限制显示内容。
  [#9499](https://github.com/rust-lang/cargo/pull/9499)
- 新增 `cargo tree -e no-proc-macro` 以隐藏过程宏依赖。
  [#9488](https://github.com/rust-lang/cargo/pull/9488)
- 新增 `doc.browser` 配置选项，用于设置用 `cargo doc --open` 打开的浏览器。
  [#9473](https://github.com/rust-lang/cargo/pull/9473)
- 为集成测试与 benches 新增设置 `CARGO_TARGET_TMPDIR` 环境变量。这在 `target` 目录中为测试与 benches 提供临时或“scratch”目录供使用。
  [#9375](https://github.com/rust-lang/cargo/pull/9375)

### 变更

- `--features` CLI 标志现在会在新的 feature resolver 下提供拼写建议。
  [#9420](https://github.com/rust-lang/cargo/pull/9420)
- Cargo 现在对 SemVer 版本使用新的解析器。这应与之前行为大体相同，但有一些小例外：无效的版本要求语法现在会被拒绝。
  [#9508](https://github.com/rust-lang/cargo/pull/9508)
- 已发布 `.crate` 包的 mtime 处理略有变更，以避免 mtime 值为 0。这会导致 lldb 拒绝读取这些文件的问题。
  [#9517](https://github.com/rust-lang/cargo/pull/9517)
- 改进了 `cargo package` 中 git status 检查的性能。
  [#9478](https://github.com/rust-lang/cargo/pull/9478)
- 使用 fossil 的 `cargo new` 现在将 ignore 设置放在新仓库中，而不再使用 `fossil settings` 进行全局设置。这也包含若干其他清理，使其与其他 VCS 配置更一致。
  [#9469](https://github.com/rust-lang/cargo/pull/9469)
- `rustc-cdylib-link-arg` 传递式应用会显示警告：这并非预期行为，未来可能变为错误。
  [#9563](https://github.com/rust-lang/cargo/pull/9563)

### 修复

- 修复了在非 git 仓库中或 vendoring 依赖时，`Cargo.toml` 中的 `package.exclude` 使用反向排除（`!somefile`）的问题。
  [#9186](https://github.com/rust-lang/cargo/pull/9186)
- Dep-info 文件现在会将构建脚本的 `rerun-if-changed` 路径调整为绝对路径。
  [#9421](https://github.com/rust-lang/cargo/pull/9421)
- 修复了在 resolver = "1" 时，非虚拟包允许未知 features 的 bug。
  [#9437](https://github.com/rust-lang/cargo/pull/9437)
- 修复了 index 缓存错误处理仅构建元数据不同的版本（例如 `110.0.0` 与 `110.0.0+1.1.0f`）的问题。
  [#9476](https://github.com/rust-lang/cargo/pull/9476)
- 修复了带有 semver 元数据版本的 `cargo install`。
  [#9467](https://github.com/rust-lang/cargo/pull/9467)

### 仅 Nightly

- 新增 `report` 子命令，并将 `cargo
  describe-future-incompatibilitie` 变更为 `cargo report
  future-incompatibilities`。
  [#9438](https://github.com/rust-lang/cargo/pull/9438)
- 在配置文件中新增 `[host]` 表，以便能为主机目标设置构建标志。还新增了 `target-applies-to-host` 以控制 `[target]` 表的行为。
  [#9322](https://github.com/rust-lang/cargo/pull/9322)
- 对构建脚本的 `rustc-link-arg-*` 指令增加了一些校验：若目标不存在则返回错误。
  [#9523](https://github.com/rust-lang/cargo/pull/9523)
- 为构建脚本新增 `cargo:rustc-link-arg-bin` 指令。
  [#9486](https://github.com/rust-lang/cargo/pull/9486)


## Cargo 1.53 (2021-06-17)
[90691f2b...rust-1.53.0](https://github.com/rust-lang/cargo/compare/90691f2b...rust-1.53.0)

### 新增

### 变更
- 🔥 Cargo 现在支持默认 `HEAD` 分支不是 “master” 的 git 仓库。这还包括切换到可正确处理默认分支的版本 3 `Cargo.lock` 格式。
  [#9133](https://github.com/rust-lang/cargo/pull/9133)
  [#9397](https://github.com/rust-lang/cargo/pull/9397)
  [#9384](https://github.com/rust-lang/cargo/pull/9384)
  [#9392](https://github.com/rust-lang/cargo/pull/9392)
- 🔥 macOS 目标现在默认使用 `unpacked` split-debuginfo。
  [#9298](https://github.com/rust-lang/cargo/pull/9298)
- ❗ 新项目的 `Cargo.toml` 不再包含 `authors` 字段。
  [#9282](https://github.com/rust-lang/cargo/pull/9282)
- `cargo update` 现在可能可与 `--offline` 标志一起工作。
  [#9279](https://github.com/rust-lang/cargo/pull/9279)
- `cargo doc` 现在会在切换不同工具链版本时擦除 `doc` 目录。存在共享的、未版本化的文件（例如搜索索引），在使用不同版本时可能会损坏。
  [#8640](https://github.com/rust-lang/cargo/pull/8640)
  [#9404](https://github.com/rust-lang/cargo/pull/9404)
- 改进了路径依赖/workspace 成员缺失时的错误消息。
  [#9368](https://github.com/rust-lang/cargo/pull/9368)

### 修复
- 修复了 `cargo doc`：在变更某些设置（例如 features）时检测是否需要重建文档。
  [#9419](https://github.com/rust-lang/cargo/pull/9419)
- `cargo doc` 现在会在运行 rustdoc 之前删除该包的输出目录，以清除任何陈旧文件。
  [#9419](https://github.com/rust-lang/cargo/pull/9419)
- 修复了 `-C metadata` 值始终为所有构建包含全部信息。此前在某些情况下，hash 仅包含包名与版本。这修复了一些问题，例如在 macOS 上使用 split-debuginfo 的增量构建在某些情况下损坏增量缓存。
  [#9418](https://github.com/rust-lang/cargo/pull/9418)
- 修复了若 `PATH` 中有 `man`，Windows 上 man pages 不工作的问题。
  [#9378](https://github.com/rust-lang/cargo/pull/9378)
- `rustc` 缓存现在会感知 `RUSTC_WRAPPER` 和 `RUSTC_WORKSPACE_WRAPPER`。
  [#9348](https://github.com/rust-lang/cargo/pull/9348)
- 若代码使用 `env!("CARGO")`，则在重建指纹中跟踪 `CARGO` 环境变量。
  [#9363](https://github.com/rust-lang/cargo/pull/9363)

### 仅 Nightly
- 修复了 config includes 不工作的问题。
  [#9299](https://github.com/rust-lang/cargo/pull/9299)
- 当 `--future-incompat-report` 无可报告内容时发出 note。
  [#9263](https://github.com/rust-lang/cargo/pull/9263)
- nightly features 标志（如 `-Z` 和 `cargo-features`）的错误消息现在提供更多信息。
  [#9290](https://github.com/rust-lang/cargo/pull/9290)
- 新增在 `Cargo.toml` 中为单个包设置 target 的能力。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#per-package-target)
  [#9030](https://github.com/rust-lang/cargo/pull/9030)
- 修复了 build-std 每次构建都更新 index 的问题。
  [#9393](https://github.com/rust-lang/cargo/pull/9393)
- `-Z help` 现在显示所有 `-Z` 选项。
  [#9369](https://github.com/rust-lang/cargo/pull/9369)
- 新增 `-Zallow-features` 以指定允许使用哪些 nightly features。
  [#9283](https://github.com/rust-lang/cargo/pull/9283)
- 新增 `cargo config` 子命令。
  [#9302](https://github.com/rust-lang/cargo/pull/9302)

## Cargo 1.52 (2021-05-06)
[34170fcd...rust-1.52.0](https://github.com/rust-lang/cargo/compare/34170fcd...rust-1.52.0)

### 新增
- 为包的 JSON 消息添加了 `"manifest_path"` 字段。
  [#9022](https://github.com/rust-lang/cargo/pull/9022)
  [#9247](https://github.com/rust-lang/cargo/pull/9247)

### 变更
- 现在禁止构建脚本在稳定版上设置 `RUSTC_BOOTSTRAP`。
  [#9181](https://github.com/rust-lang/cargo/pull/9181)
  [#9385](https://github.com/rust-lang/cargo/pull/9385)
- crates.io 现在支持 SPDX 3.11 许可证。
  [#9209](https://github.com/rust-lang/cargo/pull/9209)
- 若 `CARGO_TARGET_DIR` 为空字符串，现在会报告错误。
  [#8939](https://github.com/rust-lang/cargo/pull/8939)
- 文档测试现在会将 `--message-format` 标志传入测试，因此
  "short" 格式现在也可用于文档测试。
  [#9128](https://github.com/rust-lang/cargo/pull/9128)
- `cargo test` 现在会更清晰地指示当前正在运行的 target。
  [#9195](https://github.com/rust-lang/cargo/pull/9195)
- 若 `CARGO_TARGET_<TRIPLE>` 环境变量使用小写字母，
  现在会发出警告。
  [#9169](https://github.com/rust-lang/cargo/pull/9169)

### 修复
- 修复了带有 metadata 与 resolver 字段的包在 `Cargo.toml` 中的发布。
  [#9300](https://github.com/rust-lang/cargo/pull/9300)
  [#9304](https://github.com/rust-lang/cargo/pull/9304)
- 修复了确定 dylib 的 prefer-dynamic 时，在工作区与
  单个包之间逻辑不一致的问题。
  [#9252](https://github.com/rust-lang/cargo/pull/9252)
- 修复了排他的目标专用依赖在不同依赖种类之间重叠
  （如普通依赖与 build-dependencies）时，会错误地
  同时包含在两者中的问题。
  [#9255](https://github.com/rust-lang/cargo/pull/9255)
- 修复了向 `-p` 标志传入某些样式的 Package ID 时的 panic。
  [#9188](https://github.com/rust-lang/cargo/pull/9188)
- 当运行 cargo 且输出未到 TTY，但强制启用进度条
  与颜色时，输出现在会正确清除进度行。
  [#9231](https://github.com/rust-lang/cargo/pull/9231)
- 当 JSON 可能包含非 utf8 路径时返回错误而非 panic。
  [#9226](https://github.com/rust-lang/cargo/pull/9226)
- 修复了在损坏的 stderr 上可能发生的挂起。
  [#9201](https://github.com/rust-lang/cargo/pull/9201)
- 修复了设置 `lto=off` 时 thin-local LTO 未正确禁用的问题。
  [#9182](https://github.com/rust-lang/cargo/pull/9182)

### 仅 Nightly
- `strip` profile 选项现在支持 `true` 和 `false` 值。
  [#9153](https://github.com/rust-lang/cargo/pull/9153)
- 切换到 2021 时，若新解析器更改了 features，
  `cargo fix --edition` 现在会显示报告。
  [#9268](https://github.com/rust-lang/cargo/pull/9268)
- 在 `.cargo/config` 文件中新增 `[patch]` 表支持。
  [#9204](https://github.com/rust-lang/cargo/pull/9204)
- 新增 `cargo describe-future-incompatibilities`，用于生成
  含有未来不兼容警告的依赖报告。
  [#8825](https://github.com/rust-lang/cargo/pull/8825)
- 新增更便捷的 2021 edition 测试支持。
  [#9184](https://github.com/rust-lang/cargo/pull/9184)
- 在 2021 edition 中将默认解析器切换为 "2"。
  [#9184](https://github.com/rust-lang/cargo/pull/9184)
- `cargo fix --edition` 现在支持 2021。
  [#9184](https://github.com/rust-lang/cargo/pull/9184)
- 为 `cargo rustc` 新增 `--print` 标志，以传递给 `rustc`
  显示来自 rustc 的信息。
  [#9002](https://github.com/rust-lang/cargo/pull/9002)
- 新增 `-Zdoctest-in-workspace`，用于更改 doctest
  *运行* 与 *编译* 所在目录。
  [#9105](https://github.com/rust-lang/cargo/pull/9105)
- 支持在 `.cargo/config.toml` 中使用 `[env]` 节，以便在
  运行 cargo 时设置环境变量。
  [#9175](https://github.com/rust-lang/cargo/pull/9175)
- 为索引新增 schema 字段与 `features2` 字段。
  [#9161](https://github.com/rust-lang/cargo/pull/9161)
- 更改 JSON spec target 现在会触发重建。
  [#9223](https://github.com/rust-lang/cargo/pull/9223)

## Cargo 1.51 (2021-03-25)
[75d5d8cf...rust-1.51.0](https://github.com/rust-lang/cargo/compare/75d5d8cf...rust-1.51.0)

### 新增
- 🔥 新增 `split-debuginfo` profile 选项。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/profiles.html#split-debuginfo)
  [#9112](https://github.com/rust-lang/cargo/pull/9112)
- 为 `cargo metadata` 的包依赖列表新增 `path` 字段，
  以显示 "path" 依赖的路径。
  [#8994](https://github.com/rust-lang/cargo/pull/8994)
- 🔥 新增 feature 解析器，以及新的 CLI feature 标志行为。参见
  新的 [features](https://doc.rust-lang.org/nightly/cargo/reference/features.html#feature-resolver-version-2)
  与 [resolver](https://doc.rust-lang.org/nightly/cargo/reference/resolver.html#feature-resolver-version-2)
  文档中关于 `resolver = "2"` 选项的说明。参见
  [CLI](https://doc.rust-lang.org/nightly/cargo/reference/features.html#command-line-feature-options)
  与 [resolver 2 CLI](https://doc.rust-lang.org/nightly/cargo/reference/features.html#resolver-version-2-command-line-flags)
  选项了解新的 CLI 行为。最后，参见
  [RFC 2957](https://github.com/rust-lang/rfcs/blob/master/text/2957-cargo-features2.md)
  以详细了解变更内容。
  [#8997](https://github.com/rust-lang/cargo/pull/8997)

### 变更
- 若未找到 `Cargo.lock`，`cargo install --locked` 现在会发出警告。
  [#9108](https://github.com/rust-lang/cargo/pull/9108)
- 在命令行传入未知或歧义的 package ID 时，现在会显示
  正确 package ID 的建议。
  [#9095](https://github.com/rust-lang/cargo/pull/9095)
- 轻微优化 `cargo vendor`
  [#8937](https://github.com/rust-lang/cargo/pull/8937)
  [#9131](https://github.com/rust-lang/cargo/pull/9131)
  [#9132](https://github.com/rust-lang/cargo/pull/9132)

### 修复
- 修复了构建脚本发出的环境变量与 cfg 设置：当构建脚本
  在同一构建会话中多次运行时，这些设置会用于
  `cargo test` 与 `cargo run`。
  [#9122](https://github.com/rust-lang/cargo/pull/9122)
- 修复了 `cargo doc` 与新 feature 解析器的 panic。这还
  引入了一些启发式方法，尝试通过在存在多个变体时
  仅文档化包的一个变体（例如多个版本，或同一包
  同时用于 host 与 target 平台）来避免与 `rustdoc` 的路径冲突。
  [#9077](https://github.com/rust-lang/cargo/pull/9077)
- 修复了 Cargo 循环依赖图检测中导致栈溢出的 bug。
  [#9075](https://github.com/rust-lang/cargo/pull/9075)
- 修复了某些情况下构建脚本 `links` 环境变量（`DEP_*`）
  在测试包中未出现的问题。
  [#9065](https://github.com/rust-lang/cargo/pull/9065)
- 修复了在使用 `resolver="2"` 构建含有 proc-macro 的整个工作区
  及全部 target 的特定场景下，features 以非确定性方式
  被选择的问题。
  [#9059](https://github.com/rust-lang/cargo/pull/9059)
- 修复为使用 `~/.gitconfig` 中的 `http.proxy` 设置。
  [#8986](https://github.com/rust-lang/cargo/pull/8986)
- 修复了 V1 解析器对非成员的 --feature pkg/feat。
  [#9275](https://github.com/rust-lang/cargo/pull/9275)
  [#9277](https://github.com/rust-lang/cargo/pull/9277)
- 修复了工作区中输出文件名冲突时 `cargo doc` 的 panic。
  [#9276](https://github.com/rust-lang/cargo/pull/9276)
  [#9277](https://github.com/rust-lang/cargo/pull/9277)
- 修复了在多个包中有一个安装失败时，`cargo install`
  仍以成功退出的问题。
  [#9185](https://github.com/rust-lang/cargo/pull/9185)
  [#9196](https://github.com/rust-lang/cargo/pull/9196)
- 修复文档冲突孤儿导致的 panic。
  [#9142](https://github.com/rust-lang/cargo/pull/9142)
  [#9196](https://github.com/rust-lang/cargo/pull/9196)

### 仅 Nightly
- 移除了 `publish-lockfile` 不稳定功能，它在 1.5 年前
  无需显式标志即已稳定。
  [#9092](https://github.com/rust-lang/cargo/pull/9092)
- 为 nightly 功能（例如通过 `-Z` 标志传入，或在
  `Cargo.toml` 中用 `cargo-features` 指定的功能）新增更好的诊断、
  帮助消息与文档。
  [#9092](https://github.com/rust-lang/cargo/pull/9092)
- 新增对 Rust edition 2021 的支持。
  [#8922](https://github.com/rust-lang/cargo/pull/8922)
- 新增对项目元数据中 `rust-version` 字段的支持。
  [#8037](https://github.com/rust-lang/cargo/pull/8037)
- 为索引新增 schema 字段。
  [#9161](https://github.com/rust-lang/cargo/pull/9161)
  [#9196](https://github.com/rust-lang/cargo/pull/9196)

## Cargo 1.50 (2021-02-11)
[8662ab42...rust-1.50.0](https://github.com/rust-lang/cargo/compare/8662ab42...rust-1.50.0)

### 新增
- 为 `cargo metadata` 新增 `doc` 字段，用于指示 target
  是否被文档化。
  [#8869](https://github.com/rust-lang/cargo/pull/8869)
- 新增 `RUSTC_WORKSPACE_WRAPPER`，一种仅对本地工作区包运行的
  备用 RUSTC 包装器，并独立于非包装构建缓存其产物。
  [#8976](https://github.com/rust-lang/cargo/pull/8976)
- 为 `cargo update` 新增 `--workspace`，仅更新工作区成员，
  而不更新其依赖。若你更新了 `Cargo.toml` 中的版本并希望
  更新 `Cargo.lock` 而不运行其他命令，这尤其有用。
  [#8725](https://github.com/rust-lang/cargo/pull/8725)

### 变更
- 上传到注册表的 `.crate` 文件现在以可复现设置构建，
  因此在不同机器上创建的相同 `.crate` 文件
  应完全一致。
  [#8864](https://github.com/rust-lang/cargo/pull/8864)
- 指定了 `branch`、`tag` 或 `rev` 中不止一项的 Git 依赖
  现在会被拒绝。
  [#8984](https://github.com/rust-lang/cargo/pull/8984)
- `rerun-if-changed` 构建脚本指令现在可以指向目录，
  此时 Cargo 会检查该目录中是否有任何文件发生变化。
  [#8973](https://github.com/rust-lang/cargo/pull/8973)
- 若 Cargo 无法确定用户名或电子邮件地址，`cargo new` 将
  不再失败，而是创建空的 authors 列表。
  [#8912](https://github.com/rust-lang/cargo/pull/8912)
- 进度条宽度已减小，以便有更多空间显示
  当前正在构建的 crate。
  [#8892](https://github.com/rust-lang/cargo/pull/8892)
- `cargo new` 现在将支持 `.gitconfig` 中的 `includeIf` 指令，
  以便在确定用户名和电子邮件地址时匹配正确的目录。
  [#8886](https://github.com/rust-lang/cargo/pull/8886)

### 修复
- 修复了 `cargo metadata` 与 `cargo tree`，使其仅下载
  所请求 target 的包。
  [#8987](https://github.com/rust-lang/cargo/pull/8987)
- 更新了 libgit2，带来许多修复，尤其是修复了
  偶尔出现在 32 位系统上的 zlib 错误。
  [#8998](https://github.com/rust-lang/cargo/pull/8998)
- 修复了使用 `links` 字段的循环开发依赖导致的栈溢出。
  [#8969](https://github.com/rust-lang/cargo/pull/8969)
- 修复了在某些文件系统上 `cargo publish` 失败的问题，尤其是 WSL2 上的 9p。
  [#8950](https://github.com/rust-lang/cargo/pull/8950)

### 仅 Nightly
- 允许用 `resolver="1"` 指定原始的 feature 解析行为。
  [#8857](https://github.com/rust-lang/cargo/pull/8857)
- 新增 `-Z extra-link-arg`，添加 `cargo:rustc-link-arg-bins`
  与 `cargo:rustc-link-arg` 构建脚本选项。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#extra-link-arg)
  [#8441](https://github.com/rust-lang/cargo/pull/8441)
- 实现了外部凭据进程支持，并新增 `cargo logout`。
  ([RFC 2730](https://github.com/rust-lang/rfcs/blob/master/text/2730-cargo-token-from-process.md))
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#credential-process))
  [#8934](https://github.com/rust-lang/cargo/pull/8934)
- 修复了 `-Zbuild-std` 且无根时的 panic。
  [#8942](https://github.com/rust-lang/cargo/pull/8942)
- 将 docs.rs 设为 crates.io 的默认 extern-map
  [#8877](https://github.com/rust-lang/cargo/pull/8877)

## Cargo 1.49 (2020-12-31)
[75615f8e...rust-1.49.0](https://github.com/rust-lang/cargo/compare/75615f8e...rust-1.49.0)

### 新增
- 为 `cargo metadata` 新增 `homepage` 与 `documentation` 字段。
  [#8744](https://github.com/rust-lang/cargo/pull/8744)
- 新增 `CARGO_PRIMARY_PACKAGE` 环境变量：当包是命令行上
  选中的 "root" 包之一时，在运行 `rustc` 时会设置该变量。
  [#8758](https://github.com/rust-lang/cargo/pull/8758)
- 新增对命令行上包与 target 选择标志的 Unix 风格 glob 模式支持
  （例如 `-p 'serde*'` 或 `--test '*'`）。
  [#8752](https://github.com/rust-lang/cargo/pull/8752)

### 变更
- 计算出的 LTO 标志现在包含在文件名元数据哈希中，因此
  LTO 设置的更改会独立缓存构建产物，而不是
  覆盖先前的产物。这可在某些情况下防止重建，例如
  在某些情形下在 `cargo build` 与 `cargo test` 之间切换。
  [#8755](https://github.com/rust-lang/cargo/pull/8755)
- `cargo tree` 现在会在 proc-macro 包旁显示 `(proc-macro)`。
  [#8765](https://github.com/rust-lang/cargo/pull/8765)
- 新增警告：feature 名称允许的字符已限制为字母、数字、
  `_`、`-` 和 `+`，以适应未来的语法更改。这仍是 crates.io
  允许语法的超集，后者要求 ASCII。计划在未来
  将其改为错误。
  [#8814](https://github.com/rust-lang/cargo/pull/8814)
- 不带值的 `-p` 现在会打印工作区包名列表。
  [#8808](https://github.com/rust-lang/cargo/pull/8808)
- 将句点加入允许的 feature 名称字符。
  [#8932](https://github.com/rust-lang/cargo/pull/8932)
  [#8943](https://github.com/rust-lang/cargo/pull/8943)

### 修复
- 修复了在启用 LTO 时同时构建 "dylib" 与 "rlib" crate 类型的库。
  [#8754](https://github.com/rust-lang/cargo/pull/8754)
- 修复了 Cargo dep-info 文件中的路径。
  [#8819](https://github.com/rust-lang/cargo/pull/8819)
- 修复了显式指定 `branch="master"` 的 git 依赖在
  `cargo metadata` 中源 ID 不一致的问题。
  [#8824](https://github.com/rust-lang/cargo/pull/8824)
- 修复了重新解压包含 `.cargo-ok` 文件的依赖。
  [#8835](https://github.com/rust-lang/cargo/pull/8835)

### 仅 Nightly
- 修复了某些情况下 `cargo doc -Zfeatures=itarget` 的 panic。
  [#8777](https://github.com/rust-lang/cargo/pull/8777)
- 命名空间 features 的新实现，使用语法 `dep:serde`。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#namespaced-features)
  [#8799](https://github.com/rust-lang/cargo/pull/8799)
- 新增对 "弱" 依赖 features 的支持，使用语法
  `dep_name?/feat_name`，可在不为依赖启用依赖本身的情况下
  启用依赖的 feature。
  [#8818](https://github.com/rust-lang/cargo/pull/8818)
- 修复了新 feature 解析器下载并非严格必要的额外依赖的问题。
  [#8823](https://github.com/rust-lang/cargo/pull/8823)

## Cargo 1.48 (2020-11-19)
[51b66125...rust-1.48.0](https://github.com/rust-lang/cargo/compare/51b66125...rust-1.48.0)

### 新增
- 新增 `term.progress` 配置选项，用于控制进度条
  何时以及如何显示。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#termprogresswhen)
  [#8165](https://github.com/rust-lang/cargo/pull/8165)
- 为 `cargo locate-project` 新增 `--message-format plain` 选项，
  以不使用 JSON 显示项目位置，便于在脚本中使用。
  [#8707](https://github.com/rust-lang/cargo/pull/8707)
- 为 `cargo locate-project` 新增 `--workspace` 选项，以显示
  工作区清单的路径。
  [#8712](https://github.com/rust-lang/cargo/pull/8712)
- 新增了关于为 Cargo 本身做贡献的贡献者指南。
  发布于 <https://rust-lang.github.io/cargo/contrib/>。
  [#8715](https://github.com/rust-lang/cargo/pull/8715)
- Zsh `--target` 补全现在会补全内置的 rustc target。
  [#8740](https://github.com/rust-lang/cargo/pull/8740)

### 变更

### 修复
- 修复了 `cargo new` 创建 fossil 仓库时正确忽略 `target` 目录。
  [#8671](https://github.com/rust-lang/cargo/pull/8671)
- 使用 `cargo install` 安装远程包时，不显示关于
  当前目录工作区的警告。
  [#8681](https://github.com/rust-lang/cargo/pull/8681)
- 在 git 仓库中遇到 "Object not found" 错误时
  自动重新初始化索引。
  [#8735](https://github.com/rust-lang/cargo/pull/8735)
- 更新了 libgit2，带来若干 git 仓库处理修复。
  [#8778](https://github.com/rust-lang/cargo/pull/8778)
  [#8780](https://github.com/rust-lang/cargo/pull/8780)

### 仅 Nightly
- 修复了 `cargo install`，使其忽略本地配置文件中的 `[unstable]` 表。
  [#8656](https://github.com/rust-lang/cargo/pull/8656)
- 修复了新 feature 解析器的非确定性行为。
  [#8701](https://github.com/rust-lang/cargo/pull/8701)
- 修复了在特定情形组合下，对新 feature 解析器对
  proc-macro 运行 `cargo test` 的问题。
  [#8742](https://github.com/rust-lang/cargo/pull/8742)

## Cargo 1.47 (2020-10-08)
[4f74d9b2...rust-1.47.0](https://github.com/rust-lang/cargo/compare/4f74d9b2...rust-1.47.0)

### 新增
- `cargo doc` 现在会在左侧边栏包含包的版本。
  [#8509](https://github.com/rust-lang/cargo/pull/8509)
- 为 `cargo metadata` 的 target 新增 `test` 字段。
  [#8478](https://github.com/rust-lang/cargo/pull/8478)
- Cargo 的 man 页面现在可通过 `cargo help` 命令显示（例如
  `cargo help build`）。
  [#8456](https://github.com/rust-lang/cargo/pull/8456)
  [#8577](https://github.com/rust-lang/cargo/pull/8577)
- 新增关于[依赖解析如何工作](https://doc.rust-lang.org/nightly/cargo/reference/resolver.html)
  与 [SemVer
  兼容性](https://doc.rust-lang.org/nightly/cargo/reference/semver.html)
  的新文档章节，以及关于如何为项目版本化并与
  依赖协作的建议。
  [#8609](https://github.com/rust-lang/cargo/pull/8609)

### 变更
- 修改 `.gitignore` 时添加的注释已微调，
  增加了一些间距。
  [#8476](https://github.com/rust-lang/cargo/pull/8476)
- `cargo metadata` 输出现在应被排序以保证确定性。
  [#8489](https://github.com/rust-lang/cargo/pull/8489)
- 默认情况下，构建脚本与 proc-macro 现在以 `opt-level=0`
  与默认 codegen units 构建，即使在 release 模式下也是如此。
  [#8500](https://github.com/rust-lang/cargo/pull/8500)
- `workspace.default-members` 现在由 `workspace.exclude` 过滤。
  [#8485](https://github.com/rust-lang/cargo/pull/8485)
- `workspace.members` glob 现在忽略非目录路径。
  [#8511](https://github.com/rust-lang/cargo/pull/8511)
- git zlib 错误现在会触发重试。
  [#8520](https://github.com/rust-lang/cargo/pull/8520)
- "http" 类 git 错误现在会触发重试。
  [#8553](https://github.com/rust-lang/cargo/pull/8553)
- git 依赖现在会覆盖 `core.autocrlf` git 配置值，
  以确保跨平台行为一致，尤其是在 Windows 上
  vendor git 依赖时。
  [#8523](https://github.com/rust-lang/cargo/pull/8523)
- 若需要更新 `Cargo.lock`，则会自动
  过渡到新的 V2 格式。该格式移除了 `[metadata]`
  表，应更容易在源码控制系统中合并更改。此
  格式在 1.38 中引入，并在 1.41 中成为新项目的
  默认格式。
  [#8554](https://github.com/rust-lang/cargo/pull/8554)
- 为支持默认分支非 "master" 的 git 仓库做了准备。
  实际支持将在未来版本中到来。这引入了一些警告：
  - 若 git 依赖未指定分支，且仓库的默认分支
    不是 "master"，则警告。未来 Cargo 将获取
    默认分支。在此场景下，应显式指定分支。
  - 若工作区对同一 git 仓库有多个依赖，
    一个没有 `branch`，一个有 `branch="master"`，则警告。依赖应
    全部使用其中一种形式。
  [#8522](https://github.com/rust-lang/cargo/pull/8522)
- 若 `required-features` 条目列出不存在的 feature，
  现在会发出警告。
  [#7950](https://github.com/rust-lang/cargo/pull/7950)
- 内置别名现在包含在 `cargo --list` 中。
  [#8542](https://github.com/rust-lang/cargo/pull/8542)
- 对已被 yank 的特定版本执行 `cargo install` 时，现在会
  显示该版本已被 yank 的错误消息，而不是 "could not
  find"。
  [#8565](https://github.com/rust-lang/cargo/pull/8565)
- 对 `publish` 字段设为单个注册表、且未给出 `--registry`
  标志的包执行 `cargo publish` 时，现在会发布到该
  注册表，而不是生成错误。
  [#8571](https://github.com/rust-lang/cargo/pull/8571)

### 修复
- 修复了项目目录被移动，且某个构建脚本
  未使用 `rerun-if-changed` 指令时，该构建脚本
  被不应重建却重建的问题。
  [#8497](https://github.com/rust-lang/cargo/pull/8497)
- 控制台颜色现在应在 Windows 7 和 8 上工作。
  [#8540](https://github.com/rust-lang/cargo/pull/8540)
- `CARGO_TARGET_{triplet}_RUNNER` 环境变量现在会正确
  覆盖配置文件，而不是尝试合并命令。
  [#8629](https://github.com/rust-lang/cargo/pull/8629)
- 修复了 doctest 的 LTO。
  [#8657](https://github.com/rust-lang/cargo/pull/8657)
  [#8658](https://github.com/rust-lang/cargo/pull/8658)

### 仅 Nightly
- 新增对 `-Z terminal-width` 的支持，该选项告诉 `rustc` 终端
  宽度，以便更好地格式化诊断信息。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#terminal-width)
  [#8427](https://github.com/rust-lang/cargo/pull/8427)
- 新增通过配置文件中 `[unstable]` 表配置 `-Z` 不稳定标志的能力。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html)
  [#8393](https://github.com/rust-lang/cargo/pull/8393)
- 新增 `-Z build-std-features` 标志，用于设置标准库的 features。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#build-std-features)
  [#8490](https://github.com/rust-lang/cargo/pull/8490)

## Cargo 1.46 (2020-08-27)
[9fcb8c1d...rust-1.46.0](https://github.com/rust-lang/cargo/compare/9fcb8c1d...rust-1.46.0)

### 新增
- 注册表索引 `config.json` 中的 `dl` 键现在支持替换标记
  `{prefix}` 与 `{lowerprefix}`，以允许将 crate
  分散到多个目录，类似于索引本身的结构。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/registries.html#index-format)
  [#8267](https://github.com/rust-lang/cargo/pull/8267)
- 新增在编译期间设置的环境变量：
  - `CARGO_CRATE_NAME`：正在构建的 crate 名称。
  - `CARGO_BIN_NAME`：可执行二进制文件的名称（若这是二进制 crate）。
  - `CARGO_PKG_LICENSE`：清单中的 `license` 字段。
  - `CARGO_PKG_LICENSE_FILE`：清单中的 `license-file` 字段。
  [#8270](https://github.com/rust-lang/cargo/pull/8270)
  [#8325](https://github.com/rust-lang/cargo/pull/8325)
  [#8387](https://github.com/rust-lang/cargo/pull/8387)
- 若 `Cargo.toml` 中未指定 `readme` 的值，现在会根据是否存在
  名为 `README`、`README.md` 或 `README.txt` 的文件自动推断。
  可通过设置 `readme = false` 来抑制此行为。
  [#8277](https://github.com/rust-lang/cargo/pull/8277)
- `cargo install` 现在支持 `--index` 标志以直接从索引安装。
  [#8344](https://github.com/rust-lang/cargo/pull/8344)
- 在 `Cargo.toml` 的 `workspace` 定义中新增 `metadata` 表。
  可用于任意数据，类似于 `package.metadata` 表。
  [#8323](https://github.com/rust-lang/cargo/pull/8323)
- 为 `cargo install` 新增 `--target-dir` 标志以设置目标目录。
  [#8391](https://github.com/rust-lang/cargo/pull/8391)
- 由 [`env!`](https://doc.rust-lang.org/std/macro.env.html) 或
  [`option_env!`](https://doc.rust-lang.org/std/macro.option_env.html) 宏
  使用的环境变量发生变化时，现在会自动检测并触发重建。
  [#8421](https://github.com/rust-lang/cargo/pull/8421)
- `target` 目录现在包含 `CACHEDIR.TAG` 文件，供某些工具
  用于将该目录排除在备份之外。
  [#8378](https://github.com/rust-lang/cargo/pull/8378)
- 新增关于 rustup 的 `+toolchain` 语法的文档。
  [#8455](https://github.com/rust-lang/cargo/pull/8455)

### 变更
- 若 git 依赖的 URL 包含 `#` 片段，现在会显示警告。
  这可能令人困惑，因为 Cargo 自身会以该语法显示 git
  URL，但它在 `Cargo.lock` 文件之外没有任何含义，
  且无法正常工作。
  [#8297](https://github.com/rust-lang/cargo/pull/8297)
- 对 bitcode 嵌入与 LTO 的各种优化与修复。
  [#8349](https://github.com/rust-lang/cargo/pull/8349)
- 减少了为 git 依赖获取的数据量。若 Cargo 知道要获取的
  分支或标签，现在将仅获取该分支或标签，而不是
  所有分支和标签。
  [#8363](https://github.com/rust-lang/cargo/pull/8363)
- 增强了 git fetch 错误消息。
  [#8409](https://github.com/rust-lang/cargo/pull/8409)
- `.crate` 文件现在以 GNU tar 格式生成，而非 UStar，
  以支持更长的文件名。
  [#8453](https://github.com/rust-lang/cargo/pull/8453)

### 修复
- 修复了罕见情况：对 `Cargo.lock` 的更新失败一次，但随后
  再次运行却允许继续。
  [#8274](https://github.com/rust-lang/cargo/pull/8274)
- 移除了 Windows dylib 必须具有 `.dll` 扩展名的断言。某些
  自定义 JSON spec target 可能会更改扩展名。
  [#8310](https://github.com/rust-lang/cargo/pull/8310)
- 更新了 libgit2，带来对某些远程 git 服务器（如 googlesource.com）
  zlib 错误的修复。
  [#8320](https://github.com/rust-lang/cargo/pull/8320)
- 修复了非 master 分支上已是最新的 git 依赖的
  GitHub 快速路径检查。
  [#8363](https://github.com/rust-lang/cargo/pull/8363)
- 修复了使用 `pkg/feature` 语法启用 feature，且 `pkg` 是
  可选依赖，同时又是开发依赖，且开发依赖在注册表摘要中
  出现在可选普通依赖之前时，可选依赖不会被激活的问题。
  [#8395](https://github.com/rust-lang/cargo/pull/8395)
- 修复了若存在名为 `build` 的测试时，`clean -p` 会删除
  构建目录的问题。
  [#8398](https://github.com/rust-lang/cargo/pull/8398)
- 修复了多行 Cargo 错误消息的缩进。
  [#8409](https://github.com/rust-lang/cargo/pull/8409)
- 修复了为 rustdoc 自动包含 `--document-private-items`
  标志会覆盖传给 `cargo rustdoc` 命令的任何标志的问题。
  [#8449](https://github.com/rust-lang/cargo/pull/8449)
- Cargo 现在会在指纹目录的哈希中包含版本，
  以支持对指纹结构的向后不兼容更改。
  [#8473](https://github.com/rust-lang/cargo/pull/8473)
  [#8488](https://github.com/rust-lang/cargo/pull/8488)

### 仅 Nightly
- 新增 `-Zrustdoc-map` 功能，为 rustdoc 提供外部映射
  （例如 https://docs.rs/ 链接）。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#rustdoc-map)
  [#8287](https://github.com/rust-lang/cargo/pull/8287)
- 修复了在 `Cargo.toml` 中用下划线声明 proc-macro
  （如 `proc_macro = true`）时的 feature 计算。
  [#8319](https://github.com/rust-lang/cargo/pull/8319)
- 新增通过 `-Zdoctest-xcompile` 设置 `-Clinker` 的支持。
  [#8359](https://github.com/rust-lang/cargo/pull/8359)
- 修复了在配置文件中设置 `strip` profile 字段。
  [#8454](https://github.com/rust-lang/cargo/pull/8454)

## Cargo 1.45 (2020-07-16)
[ebda5065e...rust-1.45.0](https://github.com/rust-lang/cargo/compare/ebda5065...rust-1.45.0)

### 新增

### 变更
- 更改官方文档，推荐使用 `.cargo/config.toml` 文件名
  （带 `.toml` 扩展名）。`.toml` 扩展名支持在 1.39 中添加。
  [#8121](https://github.com/rust-lang/cargo/pull/8121)
- 不再允许 `registry.index` 配置值（已弃用
  4 年）。
  [#7973](https://github.com/rust-lang/cargo/pull/7973)
- 若同时传入 `--index` 与 `--registry` 则生成错误
  （此前 `--index` 会被静默忽略）。
  [#7973](https://github.com/rust-lang/cargo/pull/7973)
- 使用 `--index` 标志时不再使用 `registry.token` 配置值。
  这旨在避免将 crates.io 令牌潜在地泄露到另一个
  注册表。
  [#7973](https://github.com/rust-lang/cargo/pull/7973)
- 若 `registry.token` 与源替换一起使用，则新增警告。计划
  在未来版本中将其变为错误。
  [#7973](https://github.com/rust-lang/cargo/pull/7973)
- Windows GNU target 现在会将 DLL crate 类型的 `.dll.a` 导入库文件
  复制到输出目录。
  [#8141](https://github.com/rust-lang/cargo/pull/8141)
- 所有依赖的 dylib 现在无条件复制到输出目录。某些
  晦涩场景可能导致构建之间引用旧的 dylib，这可确保
  使用所有最新副本。
  [#8139](https://github.com/rust-lang/cargo/pull/8139)
- `package.exclude` 现在可以匹配目录名。若指定了目录，
  整个目录将被排除，Cargo 不会再尝试进一步检查它。
  此前 Cargo 会尝试检查目录中的每个文件，若目录包含
  不可读文件则可能出问题。
  [#8095](https://github.com/rust-lang/cargo/pull/8095)
- 使用 `cargo publish` 或 `cargo package` 打包时，Cargo 可用 git
  指导其决定包含哪些文件。此前此基于 git 的逻辑要求
  仓库根目录存在 `Cargo.toml` 文件。现在不再要求，因此
  即使仓库根目录没有 `Cargo.toml`，Cargo 也将使用基于
  git 的指导。
  [#8095](https://github.com/rust-lang/cargo/pull/8095)
- 在 Windows 上解压 crate 时，若因文件是保留的 Windows
  文件名（如 "aux.rs"）而无法写入文件，Cargo 将显示
  额外消息解释失败原因。
  [#8136](https://github.com/rust-lang/cargo/pull/8136)
- 现在忽略设置文件 mtime 的失败。某些文件系统不支持此操作。
  [#8185](https://github.com/rust-lang/cargo/pull/8185)
- 某些类别的 git 错误现在会建议启用
  `net.git-fetch-with-cli`。
  [#8166](https://github.com/rust-lang/cargo/pull/8166)
- 进行 LTO 构建时，Cargo 现在会在可能的情况下指示 rustc
  不执行 codegen。这可能带来更快的构建并使用更少的磁盘
  空间。此外，对于非 LTO 构建，Cargo 会指示 rustc 不在
  库中嵌入 LLVM bitcode，这应减小其大小。
  [#8192](https://github.com/rust-lang/cargo/pull/8192)
  [#8226](https://github.com/rust-lang/cargo/pull/8226)
  [#8254](https://github.com/rust-lang/cargo/pull/8254)
- `cargo clean -p` 的实现已重写，以便能更准确地
  移除特定包的文件。
  [#8210](https://github.com/rust-lang/cargo/pull/8210)
- Cargo 计算构建输出的方式已重写，使其更完整、更准确。
  新跟踪的文件会显示在 JSON 消息中，并在某些情况下可能
  被提升到输出目录。由此产生的部分变更包括：

  - 现在跟踪 Windows MSVC 动态库上的 `.exp` 导出文件。
  - Windows 上的 Proc-macro 跟踪导入/导出文件。
  - 所有生成单独调试文件（pdb/dSYM）的 target
    （如测试等）均被跟踪。
  - 为 wasm32-unknown-emscripten 新增 .map 文件。
  - 跟踪所有动态库（dylib/cdylib/proc-macro）以及
    构建脚本的 macOS dSYM 目录。

  由此还有多种其他变更：

  - 带连字符的 Windows MSVC 二进制示例现在会在
    examples 目录中出现两次（`foo_bar.exe` 与 `foo-bar.exe`）。此前 Cargo
    只是重命名文件而不是硬链接它。
  - 示例库现在遵循与普通库相同的连字符/下划线
    转换规则（现在将使用下划线）。

  [#8210](https://github.com/rust-lang/cargo/pull/8210)
- Cargo 尝试从 HTTP 调试的调试日志中清除任何机密。
  [#8222](https://github.com/rust-lang/cargo/pull/8222)
- 已为 Cargo 的许多文件系统操作添加上下文，因此
  错误消息现在提供更多信息，例如导致问题的路径。
  [#8232](https://github.com/rust-lang/cargo/pull/8232)
- 若干命令现在在运行时若 stdout 或 stderr 被关闭则忽略该错误。
  例如 `cargo install --list | grep -q cargo-fuzz` 此前有时会
  panic，因为 `grep -q` 可能在命令完成前关闭 stdout。常规构建
  在 stdout 或 stderr 关闭时仍会失败，与许多其他构建系统的行为一致。
  [#8236](https://github.com/rust-lang/cargo/pull/8236)
- 若 `cargo install` 给定确切版本，如 `--version=1.2.3`，且
  该版本已安装，现在将避免更新索引，并快速退出
  指示已安装。
  [#8022](https://github.com/rust-lang/cargo/pull/8022)
- 对 `[patch]` 节的更改现在会尝试自动将
  `Cargo.lock` 更新到新版本。在无法自动更新的罕见情况下，
  现在也应提供更好的错误消息。
  [#8248](https://github.com/rust-lang/cargo/pull/8248)

### 修复
- 修复了文件名包含破折号时，将 Windows `.pdb` 文件
  复制到输出目录的问题。
  [#8123](https://github.com/rust-lang/cargo/pull/8123)
- 修复了当包的任一祖先路径为符号链接时，Cargo 在扫描
  包是否位于 git 仓库内会失败的错误。
  [#8186](https://github.com/rust-lang/cargo/pull/8186)
- 修复了带有未使用 `[patch]` 的 `cargo update`，使其不会
  卡住并拒绝更新。
  [#8243](https://github.com/rust-lang/cargo/pull/8243)
- 修复了若 stderr 被关闭且编译器生成大量消息时，
  Cargo 会挂起的情况。
  [#8247](https://github.com/rust-lang/cargo/pull/8247)
- 修复了 macOS 上回溯不显示文件名或行号的问题。作为
  其后果，apple target 上的二进制可执行文件在 Cargo 缓存中
  文件名不包含哈希。这意味着 Cargo 只能跟踪一份副本，
  因此若切换 feature 或 rustc 版本，Cargo 将需要
  重建可执行文件。
  [#8329](https://github.com/rust-lang/cargo/pull/8329)
  [#8335](https://github.com/rust-lang/cargo/pull/8335)
- 修复了在 Windows 上对 dylib 使用 lld 时的指纹识别。Cargo
  曾错误地认为 dylib 永远不新鲜。
  [#8290](https://github.com/rust-lang/cargo/pull/8290)
  [#8335](https://github.com/rust-lang/cargo/pull/8335)

### 仅 Nightly
- 修复了使用 JSON spec target 时向 `rustdoc` 传递
  `--target` 完整路径的问题。
  [#8094](https://github.com/rust-lang/cargo/pull/8094)
- `-Cembed-bitcode=no` 重命名为 `-Cbitcode-in-rlib=no`
  [#8134](https://github.com/rust-lang/cargo/pull/8134)
- 在 `Cargo.toml` 中新增 `resolver` 字段，以选择加入新的
  feature 解析器。
  [#8129](https://github.com/rust-lang/cargo/pull/8129)
- `-Zbuild-std` 不再将 std 依赖视为 "local"。这意味着它
  不会对这些依赖使用增量编译，将它们从 dep-info 文件中
  移除，并将 lint 上限设为 "allow"。
  [#8177](https://github.com/rust-lang/cargo/pull/8177)
- 新增 `-Zmultitarget`，允许使用多个 `--target` 标志一次为
  多个 target 构建同一内容。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#multitarget)
  [#8167](https://github.com/rust-lang/cargo/pull/8167)
- 为 profile 新增 `strip` 选项，以移除符号与调试信息。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#profile-strip-option)
  [#8246](https://github.com/rust-lang/cargo/pull/8246)
- 修复了 `cargo tree --target=all -Zfeatures=all` 的 panic。
  [#8269](https://github.com/rust-lang/cargo/pull/8269)

## Cargo 1.44 (2020-06-04)
[bda50510...rust-1.44.0](https://github.com/rust-lang/cargo/compare/bda50510...rust-1.44.0)

### 新增
- 🔥 新增 `cargo tree` 命令。
  [docs](https://doc.rust-lang.org/nightly/cargo/commands/cargo-tree.html)
  [#8062](https://github.com/rust-lang/cargo/pull/8062)
- 若包具有 Windows 受限文件名（如 `nul`、
  `con`、`aux`、`prn` 等），则新增警告。
  [#7959](https://github.com/rust-lang/cargo/pull/7959)
- 编译完成时新增 `"build-finished"` JSON 消息，以便工具
  能检测何时可停止监听像 `cargo run` 或 `cargo test`
  这类命令的 JSON 消息。
  [#8069](https://github.com/rust-lang/cargo/pull/8069)

### 变更
- 有效包名现在限制为 Unicode XID 标识符。这与
  之前大体相同，但包名不能以数字或 `-` 开头。
  [#7959](https://github.com/rust-lang/cargo/pull/7959)
- `cargo new` 与 `init` 将警告或拒绝额外的包名
  （保留的 Windows 名称、保留的 Cargo 目录、非 ASCII 名称、
  与 std 冲突的名称如 `core` 等）。
  [#7959](https://github.com/rust-lang/cargo/pull/7959)
- 测试不再硬链接到输出目录（`target/debug/`）。
  这确保工具能访问调试符号，并以与 Cargo 相同的方式
  执行测试。工具应使用 JSON 消息发现可执行文件路径。
  [#7965](https://github.com/rust-lang/cargo/pull/7965)
- 更新 git 子模块时，现在为每个子模块显示 "Updating" 消息。
  [#7989](https://github.com/rust-lang/cargo/pull/7989)
- 解压 `.crate` 文件时现在保留文件修改时间。
  这撤销了 1.40 中不保留 mtime 的更改。
  [#7935](https://github.com/rust-lang/cargo/pull/7935)
- 构建脚本失败时，构建脚本警告现在单独显示。
  [#8017](https://github.com/rust-lang/cargo/pull/8017)
- 移除了 `git-checkout` 子命令。
  [#8040](https://github.com/rust-lang/cargo/pull/8040)
- 进度条现在对所有 unix 平台启用。此前仅在
  Linux、macOS 与 FreeBSD 上启用。
  [#8054](https://github.com/rust-lang/cargo/pull/8054)
- 由预发布版本的 `rustc` 生成的产物现在共享相同的
  文件名。这意味着更改 nightly 版本不会在构建目录中
  留下过时文件。
  [#8073](https://github.com/rust-lang/cargo/pull/8073)
- 使用重命名依赖时拒绝无效包名。
  [#8090](https://github.com/rust-lang/cargo/pull/8090)
- 将某类 HTTP2 错误添加为 "spurious"，将进行重试。
  [#8102](https://github.com/rust-lang/cargo/pull/8102)
- 允许 `cargo package --list` 成功，即使存在其他验证
  错误（例如 `Cargo.lock` 生成问题，或缺少依赖）。
  [#8175](https://github.com/rust-lang/cargo/pull/8175)
  [#8215](https://github.com/rust-lang/cargo/pull/8215)

### 修复
- Cargo 不再在内存中缓冲过量的编译器输出。
  [#7838](https://github.com/rust-lang/cargo/pull/7838)
- git 仓库中的符号链接现在在 Windows 上可用。
  [#7996](https://github.com/rust-lang/cargo/pull/7996)
- 修复了当 `Cargo.toml` 中未定义 `dev` profile 时，
  使用 `cargo test` 不会从配置文件加载 `profile.dev` 的问题。
  [#8012](https://github.com/rust-lang/cargo/pull/8012)
- 当二进制作为集成测试的隐式依赖构建时，
  现在会正确检查 `required-features` 中的 `dep_name/feature_name` 语法。
  [#8020](https://github.com/rust-lang/cargo/pull/8020)
- 修复了当先前构建被 Ctrl-C 中断时，Cargo 无法检测
  可执行文件（如集成测试）需要重建的问题。
  [#8087](https://github.com/rust-lang/cargo/pull/8087)
- 防范某些（未知）情况下，当系统单调时钟看起来不单调时
  Cargo 可能 panic 的情况。
  [#8114](https://github.com/rust-lang/cargo/pull/8114)
- 修复了若包有构建脚本时 `cargo clean -p` 的 panic。
  [#8216](https://github.com/rust-lang/cargo/pull/8216)

### 仅 Nightly
- 修复了新 feature 解析器与 required-features 的 panic。
  [#7962](https://github.com/rust-lang/cargo/pull/7962)
- 新增 `RUSTC_WORKSPACE_WRAPPER` 环境变量，提供一种仅对
  工作区成员包装 `rustc` 的方式，并影响文件名哈希，使
  包装器产生的产物单独缓存。此用法可在 nightly clippy
  中通过 `cargo clippy -Zunstable-options` 看到。
  [#7533](https://github.com/rust-lang/cargo/pull/7533)
- 新增 `--unit-graph` CLI 选项，以 JSON 显示 Cargo 的内部
  依赖图。
  [#7977](https://github.com/rust-lang/cargo/pull/7977)
- 将 `-Zbuild_dep` 更改为 `-Zhost_dep`，并将 proc-macro
  加入 feature 解耦逻辑。
  [#8003](https://github.com/rust-lang/cargo/pull/8003)
  [#8028](https://github.com/rust-lang/cargo/pull/8028)
- 修复了当 `RUSTDOCFLAGS` 中已有该标志时，不再自动传递
  `--crate-version`。
  [#8014](https://github.com/rust-lang/cargo/pull/8014)
- 修复了 `-Zfeatures=dev_dep` 与 `check --profile=test` 的 panic。
  [#8027](https://github.com/rust-lang/cargo/pull/8027)
- 修复了 `-Zfeatures=itarget` 与某些 host 依赖的 panic。
  [#8048](https://github.com/rust-lang/cargo/pull/8048)
- 新增对 `-Cembed-bitcode=no` 的支持，为非 LTO 构建提供
  性能提升与磁盘空间使用减少。
  [#8066](https://github.com/rust-lang/cargo/pull/8066)
- `-Zpackage-features` 已扩展若干更改，旨在使
  在工作区中于命令行选择 feature 更容易。
  [#8074](https://github.com/rust-lang/cargo/pull/8074)

## Cargo 1.43 (2020-04-23)
[9d32b7b0...rust-1.43.0](https://github.com/rust-lang/cargo/compare/9d32b7b0...rust-1.43.0)

### 新增
- 🔥 Profile 现在可在配置文件（及环境变量）中指定。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/config.html#profile)
  [#7823](https://github.com/rust-lang/cargo/pull/7823)
- ❗ 构建集成测试时新增 `CARGO_BIN_EXE_<name>` 环境变量。
  该变量包含包中任何 `[[bin]]` target 的路径。集成测试应使用
  `env!` 宏确定要执行的二进制文件路径。
  [docs](https://doc.rust-lang.org/nightly/cargo/reference/environment-variables.html#environment-variables-cargo-sets-for-crates)
  [#7697](https://github.com/rust-lang/cargo/pull/7697)

### 变更
- `cargo install --git` 现在会尊重 git 仓库中的工作区。这允许
  使用工作区设置，如 `[patch]`、`[replace]` 或 `[profile]`。
  [#7768](https://github.com/rust-lang/cargo/pull/7768)
- `cargo new` 现在会对新文件运行 `rustfmt`，以获取 rustfmt
  设置如 `tab_spaces`，从而使新文件匹配用户偏好的缩进设置。
  [#7827](https://github.com/rust-lang/cargo/pull/7827)
- 以 "very verbose" 输出（`-vv`）打印的环境变量现在
  会一致排序。
  [#7877](https://github.com/rust-lang/cargo/pull/7877)
- 指纹重建检测的调试日志现在包含更多信息。
  [#7888](https://github.com/rust-lang/cargo/pull/7888)
  [#7890](https://github.com/rust-lang/cargo/pull/7890)
  [#7952](https://github.com/rust-lang/cargo/pull/7952)
- 发布时若 license-file 不存在则新增警告。
  [#7905](https://github.com/rust-lang/cargo/pull/7905)
- 发布时自动包含 `license-file` 文件，即使它未在
  `include` 列表中显式列出，或位于包根目录之外。
  [#7905](https://github.com/rust-lang/cargo/pull/7905)
- 运行构建脚本时不再设置 `CARGO_CFG_DEBUG_ASSERTIONS` 与
  `CARGO_CFG_PROC_MACRO`。过去曾无意设置它们，但
  因始终为 true 而无意义。此外，`target` 表达式中
  不再支持 `cfg(proc-macro)`。
  [#7943](https://github.com/rust-lang/cargo/pull/7943)
  [#7970](https://github.com/rust-lang/cargo/pull/7970)

### 修复
- 全局命令行标志现在可与别名一起工作（如 `cargo -v b`）。
  [#7837](https://github.com/rust-lang/cargo/pull/7837)
- 使用依赖语法（如 `renamed_dep/feat_name`）的 Required-features
  现在能正确处理重命名依赖。
  [#7855](https://github.com/rust-lang/cargo/pull/7855)
- 修复了罕见情况：若构建脚本在同一构建中多次运行，
  Cargo 现在会分开保留结果，而不是丢失第一次执行的输出。
  [#7857](https://github.com/rust-lang/cargo/pull/7857)
- 修复了将环境变量 `CARGO_TARGET_*_RUNNER=true`
  错误解释为布尔值的问题。同时改进了相关环境变量
  错误消息。
  [#7891](https://github.com/rust-lang/cargo/pull/7891)
- 更新了内部 libgit2 库，为 git 支持带来各种修复。
  [#7939](https://github.com/rust-lang/cargo/pull/7939)
- `cargo package` / `cargo publish` 应不再将每个文件的
  全部内容缓冲到内存中。
  [#7946](https://github.com/rust-lang/cargo/pull/7946)
- 在 git 依赖中忽略更多无效的 `Cargo.toml` 文件。Cargo 当前
  会遍历整个仓库以查找请求的包。某些无效清单此前已跳过，
  现在应跳过全部。
  [#7947](https://github.com/rust-lang/cargo/pull/7947)

### 仅 Nightly
- 新增 `build.out-dir` 配置变量以设置输出目录。
  [#7810](https://github.com/rust-lang/cargo/pull/7810)
- 新增 `-Zjobserver-per-rustc` 功能，以支持并行 rustc 的
  性能改进。
  [#7731](https://github.com/rust-lang/cargo/pull/7731)
- 修复了 `build-std` 与诸如 `cc` 的 crate 的文件名冲突。
  [#7860](https://github.com/rust-lang/cargo/pull/7860)
- `-Ztimings` 现在即使有错误也会保存其报告。
  [#7872](https://github.com/rust-lang/cargo/pull/7872)
- 更新了 `--config` 命令行标志，以支持接受要加载的
  配置文件路径。
  [#7901](https://github.com/rust-lang/cargo/pull/7901)
- 新增了新的 feature 解析器。
  [#7820](https://github.com/rust-lang/cargo/pull/7820)
- Rustdoc 文档现在自动在侧边栏包含包的版本
  （需要 `-Z crate-versions` 标志）。
  [#7903](https://github.com/rust-lang/cargo/pull/7903)

## Cargo 1.42 (2020-03-12)
[0bf7aafe...rust-1.42.0](https://github.com/rust-lang/cargo/compare/0bf7aafe...rust-1.42.0)

### 新增
- 新增了关于 git 身份验证的文档。
  [#7658](https://github.com/rust-lang/cargo/pull/7658)
- crates.io 现已支持 Bitbucket Pipeline 徽章。
  [#7663](https://github.com/rust-lang/cargo/pull/7663)
- `cargo vendor` 现已接受 `--versioned-dirs` 选项，强制在每个包的目录名中
  始终包含版本号。
  [#7631](https://github.com/rust-lang/cargo/pull/7631)
- `proc_macro` crate 现已自动加入 proc-macro 包的 extern prelude。
  这意味着 proc-macro 不再需要 `extern crate proc_macro;`。
  [#7700](https://github.com/rust-lang/cargo/pull/7700)

### 变更
- 若在 `cfg()` 表达式中使用 `debug_assertions`、`test`、`proc_macro` 或 `feature=`，
  将发出警告。
  [#7660](https://github.com/rust-lang/cargo/pull/7660)
- 大幅更新 Cargo 文档，新增关于 Cargo
  targets、workspaces 与 features 的章节。
  [#7733](https://github.com/rust-lang/cargo/pull/7733)
- Windows：`.lib` DLL 导入库现已对所有 Windows MSVC target 复制到 dll 旁。
  此前仅支持 `pc-windows-msvc`。这为 `uwp-windows-msvc` target 增加了 DLL 支持。
  [#7758](https://github.com/rust-lang/cargo/pull/7758)
- `[target]` 配置中的 `ar` 字段不再被读取。该字段已被忽略超过 4 年。
  [#7763](https://github.com/rust-lang/cargo/pull/7763)
- 简化并更新了 Bash 补全文件以适配最新变更。
  [#7789](https://github.com/rust-lang/cargo/pull/7789)
- 凭证仅在需要时加载，而不再在每次 Cargo 命令时加载。
  [#7774](https://github.com/rust-lang/cargo/pull/7774)

### 修复
- 移除了 `--offline` 空索引检查，该检查在某些情况下会产生误报。
  [#7655](https://github.com/rust-lang/cargo/pull/7655)
- 以 `.` 开头的文件和目录现可通过将其加入 `include` 列表而包含在包中。
  [#7680](https://github.com/rust-lang/cargo/pull/7680)
- 修复了当凭证文件中已有先前条目时，`cargo login` 会移除备用 registry token 的问题。
  [#7708](https://github.com/rust-lang/cargo/pull/7708)
- 修复了 `cargo vendor` 在与备用 registry 一起使用时会 panic 的问题。
  [#7718](https://github.com/rust-lang/cargo/pull/7718)
- 修复了 fingerprint 调试日志消息中不正确的说明。
  [#7749](https://github.com/rust-lang/cargo/pull/7749)
- 多次定义的 `[source]` 现将导致错误。
  此前会随机选择一个 source，可能导致非确定性行为。
  [#7751](https://github.com/rust-lang/cargo/pull/7751)
- `cargo metadata` 中的 `dep_kinds` 现已去重。
  [#7756](https://github.com/rust-lang/cargo/pull/7756)
- 修复了在 git 仓库子目录的 `.gitignore` 中列出 `Cargo.lock` 时的打包问题。
  此前假定 `Cargo.lock` 位于仓库根目录。
  [#7779](https://github.com/rust-lang/cargo/pull/7779)
- 部分文件传输错误现将触发自动重试。
  [#7788](https://github.com/rust-lang/cargo/pull/7788)
- Linux：修复了 CPU iowait 统计下降时的 panic。
  [#7803](https://github.com/rust-lang/cargo/pull/7803)
- 修复了通过 `RUSTFLAGS` 传入 `--sysroot` 时，用于检测主机编译器设置的 sysroot 不正确的问题。
  [#7798](https://github.com/rust-lang/cargo/pull/7798)

### 仅 Nightly
- `build-std` 现使用 `--extern` 而非 `--sysroot` 来查找 sysroot
  包。
  [#7699](https://github.com/rust-lang/cargo/pull/7699)
- 新增 `--config` 命令行选项以设置配置项。
  [#7649](https://github.com/rust-lang/cargo/pull/7649)
- 新增 `include` 配置项，允许包含另一个配置文件。
  [#7649](https://github.com/rust-lang/cargo/pull/7649)
- 配置文件中的 profiles 现已支持任意命名的 profile。此前仅限于
  dev/release。
  [#7750](https://github.com/rust-lang/cargo/pull/7750)

## Cargo 1.41 (2020-01-30)
[5da4b4d4...rust-1.41.0](https://github.com/rust-lang/cargo/compare/5da4b4d4...rust-1.41.0)

### 新增
- 🔥 Cargo 现使用新的 `Cargo.lock` 文件格式。该新格式应
  支持在源代码控制系统中更轻松地合并。使用旧格式的项目将继续使用旧格式，只有新的 `Cargo.lock` 文件会
  使用新格式。
  [#7579](https://github.com/rust-lang/cargo/pull/7579)
- 🔥 `cargo install` 现将升级已安装的包，而不再失败。
  [#7560](https://github.com/rust-lang/cargo/pull/7560)
- 🔥 已添加 profile 覆盖。这允许为单个依赖或构建脚本覆盖 profiles。详见[文档](https://doc.rust-lang.org/nightly/cargo/reference/profiles.html#overrides)。
  [#7591](https://github.com/rust-lang/cargo/pull/7591)
- 新增了构建脚本的文档。
  [#7565](https://github.com/rust-lang/cargo/pull/7565)
- 新增了 Cargo JSON 输出的文档。
  [#7595](https://github.com/rust-lang/cargo/pull/7595)
- 大幅扩充了配置与环境变量文档。
  [#7650](https://github.com/rust-lang/cargo/pull/7650)
- 恢复对 `cargo doc --open` 的 `BROWSER` 环境变量支持。
  [#7576](https://github.com/rust-lang/cargo/pull/7576)
- 在 `cargo metadata` 的依赖中新增了 `kind` 与 `platform`。
  [#7132](https://github.com/rust-lang/cargo/pull/7132)
- `OUT_DIR` 值现已包含在 `build-script-executed` JSON 消息中。
  [#7622](https://github.com/rust-lang/cargo/pull/7622)

### 变更
- `cargo doc` 现默认会为二进制目标中的私有项生成文档。
  [#7593](https://github.com/rust-lang/cargo/pull/7593)
- 子命令拼写错误建议现包含别名。
  [#7486](https://github.com/rust-lang/cargo/pull/7486)
- 调整了向 `.gitignore` 添加 "already existing..." 注释的方式。
  [#7570](https://github.com/rust-lang/cargo/pull/7570)
- 忽略 token 中因复制粘贴而来的 `cargo login` 文本。
  [#7588](https://github.com/rust-lang/cargo/pull/7588)
- Windows：当文件系统不支持锁定文件时忽略相关错误。
  [#7602](https://github.com/rust-lang/cargo/pull/7602)
- 从 `.gitignore` 中移除 `**/*.rs.bk`。
  [#7647](https://github.com/rust-lang/cargo/pull/7647)

### 修复
- 修复 `build` 配置段中某些键的未使用警告。
  [#7575](https://github.com/rust-lang/cargo/pull/7575)
- Linux：解析 `/proc/stat` 时不再 panic。
  [#7580](https://github.com/rust-lang/cargo/pull/7580)
- 不在 `cargo vendor` 中显示规范路径。
  [#7629](https://github.com/rust-lang/cargo/pull/7629)

### 仅 Nightly


## Cargo 1.40 (2019-12-19)
[1c6ec66d...5da4b4d4](https://github.com/rust-lang/cargo/compare/1c6ec66d...5da4b4d4)

### 新增
- 新增 `http.ssl-version` 配置选项以控制 TLS 版本，
  以及最小/最大版本。
  [#7308](https://github.com/rust-lang/cargo/pull/7308)
- 🔥 编译器警告现已缓存到磁盘。若构建产生警告，
  重新运行构建现将重新显示这些警告。
  [#7450](https://github.com/rust-lang/cargo/pull/7450)
- 为 `cargo metadata` 新增 `--filter-platform` 选项，可将解析器图中显示的节点
  缩小为仅包含给定目标三元组所包含的包。
  [#7376](https://github.com/rust-lang/cargo/pull/7376)

### 变更
- Cargo 的 "platform" `cfg` 解析已提取到名为 `cargo-platform` 的独立 crate 中。
  [#7375](https://github.com/rust-lang/cargo/pull/7375)
- 提取到 Cargo 缓存中的依赖不再保留 mtimes，以减少系统调用开销。
  [#7465](https://github.com/rust-lang/cargo/pull/7465)
- Windows：EXE 文件名不再包含元数据哈希。
  这有助于调试器将文件名与 PDB 文件关联。
  [#7400](https://github.com/rust-lang/cargo/pull/7400)
- Wasm32：`.wasm` 文件不再被视为 "executable"，从而使
  `cargo test` 与 `cargo run` 能与生成的 `.js` 文件正常工作。
  [#7476](https://github.com/rust-lang/cargo/pull/7476)
- crates.io 现已支持 SPDX 3.6 许可证。
  [#7481](https://github.com/rust-lang/cargo/pull/7481)
- 改进了循环依赖错误消息。
  [#7470](https://github.com/rust-lang/cargo/pull/7470)
- 裸 `cargo clean` 不再锁定包缓存。
  [#7502](https://github.com/rust-lang/cargo/pull/7502)
- `cargo publish` 现允许发布没有 version 键的 dev-dependencies。
  仅含 git 或 path 的 dev-dependency 将在上传前从包清单中移除。
  [#7333](https://github.com/rust-lang/cargo/pull/7333)
- 在虚拟 workspace 根目录使用 `--features` 与 `--no-default-features`
  现将产生错误，而不再被忽略。
  [#7507](https://github.com/rust-lang/cargo/pull/7507)
- 包归档中生成的文件（如 `Cargo.toml` 与 `Cargo.lock`）
  的时间戳现设为当前时间，而非纪元起点。
  [#7523](https://github.com/rust-lang/cargo/pull/7523)
- `-Z` 标志解析器现更加严格，会拒绝更多无效语法。
  [#7531](https://github.com/rust-lang/cargo/pull/7531)

### 修复
- 修复了当包有 `include` 字段、`.gitignore` 中有 `Cargo.lock`、
  且有二进制或 example 目标、并且当前项目中存在 `Cargo.lock` 时，
  发布会失败并抱怨 `Cargo.lock` 为 dirty 的问题。
  [#7448](https://github.com/rust-lang/cargo/pull/7448)
- 修复了特定 `[patch]` 条目组合下的 panic。
  [#7452](https://github.com/rust-lang/cargo/pull/7452)
- Windows：当 `cargo test` 或 `rustc` 以异常方式崩溃（如信号或段错误）时，提供更好的错误消息。
  [#7535](https://github.com/rust-lang/cargo/pull/7535)

### 仅 Nightly
- `mtime-on-use` 功能现可通过
  `unstable.mtime_on_use` 配置选项启用。
  [#7411](https://github.com/rust-lang/cargo/pull/7411)
- 新增对命名 profiles 的支持。
  [#6989](https://github.com/rust-lang/cargo/pull/6989)
- 新增 `-Zpanic-abort-tests`，允许以 "abort" panic 策略构建并运行测试。
  [#7460](https://github.com/rust-lang/cargo/pull/7460)
- 将 `build-std` 改为使用 `--sysroot`。
  [#7421](https://github.com/rust-lang/cargo/pull/7421)
- 对 `-Ztimings` 的多项修复与增强。
  [#7395](https://github.com/rust-lang/cargo/pull/7395)
  [#7398](https://github.com/rust-lang/cargo/pull/7398)
  [#7397](https://github.com/rust-lang/cargo/pull/7397)
  [#7403](https://github.com/rust-lang/cargo/pull/7403)
  [#7428](https://github.com/rust-lang/cargo/pull/7428)
  [#7429](https://github.com/rust-lang/cargo/pull/7429)
- Profile 覆盖已将语法重命名为
  `[profile.dev.package.NAME]`。
  [#7504](https://github.com/rust-lang/cargo/pull/7504)
- 修复了 workspace 中未使用的 profile 覆盖的警告。
  [#7536](https://github.com/rust-lang/cargo/pull/7536)

## Cargo 1.39 (2019-11-07)
[e853aa97...1c6ec66d](https://github.com/rust-lang/cargo/compare/e853aa97...1c6ec66d)

### 新增
- 配置文件现可使用 `.toml` 文件名扩展名。
  [#7295](https://github.com/rust-lang/cargo/pull/7295)
- 已添加 `--workspace` 标志作为 `--all` 的别名，以帮助避免对 "all" 含义的混淆。
  [#7241](https://github.com/rust-lang/cargo/pull/7241)
- `publish` 字段已添加到 `cargo metadata`。
  [#7354](https://github.com/rust-lang/cargo/pull/7354)

### 变更
- 若解析来自 `rustc` 的输出失败，显示更多信息。
  [#7236](https://github.com/rust-lang/cargo/pull/7236)
- TOML 错误现显示列号。
  [#7248](https://github.com/rust-lang/cargo/pull/7248)
- `cargo vendor` 不再删除 `vendor` 目录中以 `.` 开头的文件。
  [#7242](https://github.com/rust-lang/cargo/pull/7242)
- `cargo fetch` 现将显示清单警告。
  [#7243](https://github.com/rust-lang/cargo/pull/7243)
- `cargo publish` 现将检查 git 子模块是否包含任何未提交的更改。
  [#7245](https://github.com/rust-lang/cargo/pull/7245)
- 在构建脚本中，`cargo:rustc-flags` 现允许不带空格的 `-l` 与 `-L` 标志。
  [#7257](https://github.com/rust-lang/cargo/pull/7257)
- 当 `cargo install` 替换包的旧版本时，现将删除新安装版本中不再存在的任何已安装二进制文件。
  [#7246](https://github.com/rust-lang/cargo/pull/7246)
- git 依赖在发布时现也可指定 `version` 键。上传的 crate 中将剥离 `git` 值，与 `path` 依赖的行为一致。
  [#7237](https://github.com/rust-lang/cargo/pull/7237)
- workspace default-members 的行为已更改。default-members
  现仅在 workspace 根目录运行 Cargo 时生效。此前无论在哪个目录运行 Cargo 都会始终生效。
  [#7270](https://github.com/rust-lang/cargo/pull/7270)
- 更新了 libgit2，纳入所有上游更改。
  [#7275](https://github.com/rust-lang/cargo/pull/7275)
- 升级用于定位主目录的 `home` 依赖。
  [#7277](https://github.com/rust-lang/cargo/pull/7277)
- 已更新 zsh 补全。
  [#7296](https://github.com/rust-lang/cargo/pull/7296)
- SSL 连接错误现将重试。
  [#7318](https://github.com/rust-lang/cargo/pull/7318)
- jobserver 已改为获取 N 个 token（而非 N-1），然后立即再获取额外的 token。此更改是为了适配 Windows 上的 `cc` crate，使其能够释放其隐式 token。
  [#7344](https://github.com/rust-lang/cargo/pull/7344)
- 选择下一个构建哪个 crate 的调度算法已更改。现选择等待其上的传递 crate 数量最多的 crate。此前使用最大拓扑深度。
  [#7390](https://github.com/rust-lang/cargo/pull/7390)
- RUSTFLAGS 不再纳入元数据与文件名哈希，
  撤销了 1.33 中加入该行为的更改。这意味着对 RUSTFLAGS 的任何更改都会导致重新编译，且不会影响符号混淆。
  [#7459](https://github.com/rust-lang/cargo/pull/7459)

### 修复
- 带有使用简写 SSH URL（如
  `git@github.com/user/repo.git`）的子模块的 git 依赖现应可正常工作。
  [#7238](https://github.com/rust-lang/cargo/pull/7238)
- 在 macOS 上创建 `.dSYM` 符号链接时处理损坏的符号链接。
  [#7268](https://github.com/rust-lang/cargo/pull/7268)
- 修复了 `[patch]` 表中同一 crate 多个版本的问题。
  [#7303](https://github.com/rust-lang/cargo/pull/7303)
- 修复了自定义目标 `.json` 文件中名称子串匹配不受支持的 crate 类型（如 "bin"）的问题。
  [#7363](https://github.com/rust-lang/cargo/issues/7363)
- 修复了为 proc-macro crate 类型生成文档的问题。
  [#7159](https://github.com/rust-lang/cargo/pull/7159)
- 修复了 Cargo 在构建线程内 panic 时的挂起。
  [#7366](https://github.com/rust-lang/cargo/pull/7366)
- 修复了若 `build.rs` 脚本在各次构建间发出不同的 `rerun-if`
  指令时的重建检测。Cargo 此前在更改后会错误地触发重建。
  [#7373](https://github.com/rust-lang/cargo/pull/7373)
- 正确处理 `[patch]` 表条目的规范 URL，防止
  patch 在首次使用后失效。
  [#7368](https://github.com/rust-lang/cargo/pull/7368)
- 修复了集成测试在开始自身构建前等待包二进制文件构建完成的问题。它们现可并发构建。
  [#7394](https://github.com/rust-lang/cargo/pull/7394)
- 修复了上一版本中对 `--features a b` 标志解释方式的意外更改，恢复为将该形式解释为 `--features a` 并将参数 `b` 传给命令的原始行为。若要传递多个 features，请用引号包裹，如 `--features "a b"`，或使用逗号，或使用多个 `--features` 标志。
  [#7419](https://github.com/rust-lang/cargo/pull/7419)

### 仅 Nightly
- 已添加直接从 Cargo 构建标准库的基本支持。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#build-std))
  [#7216](https://github.com/rust-lang/cargo/pull/7216)
- 新增 `-Ztimings` 功能，可生成关于各编译步骤耗时的 HTML 报告。这也可能在控制台输出完成步骤以及 JSON 数据。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#timings))
  [#7311](https://github.com/rust-lang/cargo/pull/7311)
- 新增交叉编译 doctests 的能力。
  ([docs](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#doctest-xcompile))
  [#6892](https://github.com/rust-lang/cargo/pull/6892)

## Cargo 1.38 (2019-09-26)
[4c1fa54d...23ef9a4e](https://github.com/rust-lang/cargo/compare/4c1fa54d...23ef9a4e)

### 新增
- 🔥 Cargo 构建流水线默认已启用，以在构建期间利用更多空闲 CPU 并行性。
  [#7143](https://github.com/rust-lang/cargo/pull/7143)
- Cargo 的 `--message-format` 选项现可多次指定，并接受逗号分隔的值列表。除先前的值外，现还接受 `json-diagnostic-short` 与
  `json-diagnostic-rendered-ansi`，用于配置 `json` 消息模式下 rustc 的输出。
  [#7214](https://github.com/rust-lang/cargo/pull/7214)
- crates.io 现已支持 Cirrus CI 徽章。
  [#7119](https://github.com/rust-lang/cargo/pull/7119)
- 引入了新的 `Cargo.lock` 格式。该新格式旨在更频繁地避免源代码控制合并冲突，并总体上使合并更改更安全。该新格式此时*尚未*启用，不过若 Cargo 看到该格式则会使用它。未来某个时候，计划将其设为默认。
  [#7070](https://github.com/rust-lang/cargo/pull/7070)
- 为 FreeBSD 添加了进度条支持。
  [#7222](https://github.com/rust-lang/cargo/pull/7222)

### 变更
- `-q` 标志不再抑制来自 Cargo 自身的错误的根错误消息。
  [#7116](https://github.com/rust-lang/cargo/pull/7116)
- Cargo Book 现使用 mdbook 0.3 发布，带来若干格式修复与改进。
  [#7140](https://github.com/rust-lang/cargo/pull/7140)
- `--features` 命令行标志现可多次指定。
  所有标志中的 features 列表会合并在一起。
  [#7084](https://github.com/rust-lang/cargo/pull/7084)
- 已移除包 include/exclude 的 glob-vs-gitignore 警告。
  包现可使用 gitignore 风格匹配而不产生任何警告。
  [#7170](https://github.com/rust-lang/cargo/pull/7170)
- 当查询 `rustc` 获取如 `cfg` 值等信息时，若解析 `rustc` 输出失败，Cargo 现显示命令与输出。
  [#7185](https://github.com/rust-lang/cargo/pull/7185)
- `cargo package`/`cargo publish` 现允许指向 git 子模块的符号链接以包含该子模块。
  [#6817](https://github.com/rust-lang/cargo/pull/6817)
- 改进了当版本需求不匹配任何版本、但存在预发布版本时的错误消息。
  [#7191](https://github.com/rust-lang/cargo/pull/7191)

### 修复
- 修复了在使用 `git-fetch-with-cli` 配置选项且设置了 `GIT_DIR` 环境变量时，更新 git 仓库使用错误目录的问题。在 git 回调中运行 cargo 时可能发生此情况。
  [#7082](https://github.com/rust-lang/cargo/pull/7082)
- 修复了具有单独调试输出的目标的 dep-info 文件被覆盖的问题。例如，带有 `.dSYM` 目录的 `-apple-` 目标上的二进制文件会覆盖 `.d` 文件。
  [#7057](https://github.com/rust-lang/cargo/pull/7057)
- 修复 `[patch]` 表未保持 "每个 source 一个主版本" 规则的问题。
  [#7118](https://github.com/rust-lang/cargo/pull/7118)
- 在 `cargo rustc` 命令的元数据哈希中忽略 `--remap-path-prefix` 标志。此前 remap 设置会无意中影响符号名称。
  [#7134](https://github.com/rust-lang/cargo/pull/7134)
- 修复了 `[patch]` 依赖中的循环检测。
  [#7174](https://github.com/rust-lang/cargo/pull/7174)
- 修复了当 `core.symlinks` git 配置为 true 时，`cargo new` 在 Windows 上留下符号链接的问题。还纳入了上游 libgit2 的若干修复与更新。
  [#7176](https://github.com/rust-lang/cargo/pull/7176)
- macOS：修复了设置标志以将 `target` 目录排除出备份的问题。
  [#7192](https://github.com/rust-lang/cargo/pull/7192)
- 修复了 `cargo fix` 在涉及多字节字符的某些情况下 panic 的问题。
  [#7221](https://github.com/rust-lang/cargo/pull/7221)

### 仅 Nightly
- 新增 `cargo fix --clippy`，将应用 Clippy 中机器可应用的修复。
  [#7069](https://github.com/rust-lang/cargo/pull/7069)
- 新增 `-Z binary-dep-depinfo` 标志，为二进制依赖（如标准库）添加变更跟踪。
  [#7137](https://github.com/rust-lang/cargo/pull/7137)
  [#7219](https://github.com/rust-lang/cargo/pull/7219)
- `cargo clippy-preview` 将始终运行，即使未做任何更改。
  [#7157](https://github.com/rust-lang/cargo/pull/7157)
- 修复了使用 `CARGO_BUILD_PIPELINING` 时的指数爆炸。
  [#7062](https://github.com/rust-lang/cargo/pull/7062)
- 修复了在 `cargo clippy-preview` 中向 clippy 传递参数的问题。
  [#7162](https://github.com/rust-lang/cargo/pull/7162)

## Cargo 1.37 (2019-08-15)
[c4fcfb72...9edd0891](https://github.com/rust-lang/cargo/compare/c4fcfb72...9edd0891)

### 新增
- 向 `cargo metadata` 新增 `doctest` 字段，以判定目标的文档是否被测试。
  [#6953](https://github.com/rust-lang/cargo/pull/6953)
  [#6965](https://github.com/rust-lang/cargo/pull/6965)
- 🔥 [`cargo
  vendor`](https://doc.rust-lang.org/nightly/cargo/commands/cargo-vendor.html)
  命令现已内置于 Cargo。该命令可用于创建所有依赖源码的本地副本。
  [#6869](https://github.com/rust-lang/cargo/pull/6869)
- 🔥 "publish lockfile" 功能现已稳定。若包包含二进制可执行目标，该功能将在发布包时自动包含 `Cargo.lock` 文件。默认情况下，Cargo 在安装包时会忽略
  `Cargo.lock`。要强制 Cargo 使用已发布包中包含的
  `Cargo.lock` 文件，请使用 `cargo install
  --locked`。这可能有助于确保 `cargo install` 一致地复现相同结果。当依赖意外发布了 semver 不兼容的更改时，这也可能有用，可回退到已知可用的版本。
  [#7026](https://github.com/rust-lang/cargo/pull/7026)
- 🔥 `default-run` 功能已稳定。当包包含多个二进制文件时，该功能允许你指定 `cargo run` 默认运行哪个二进制可执行文件。在 `Cargo.toml` 的 `[package]` 表中将 `default-run` 键设为默认使用的二进制名称。
  [#7056](https://github.com/rust-lang/cargo/pull/7056)

### 变更
- `cargo package` 现验证构建脚本不会创建空目录。
  [#6973](https://github.com/rust-lang/cargo/pull/6973)
- 若 `cargo doc` 生成重复输出（导致文件被随机覆盖），现发出警告。这可能由多种原因引起（重命名的依赖、同一包的多个版本、带有重命名库的包等）。这是一个已知 bug，需要更多工作才能正确处理。
  [#6998](https://github.com/rust-lang/cargo/pull/6998)
- 使用 `--features foo/bar` 启用依赖的 feature 时，若 `foo` 不是可选依赖，将不再以 `foo` feature 编译当前 crate。
  [#7010](https://github.com/rust-lang/cargo/pull/7010)
- 若通过 RUSTFLAGS 传入 `--remap-path-prefix`，将不再影响文件名元数据哈希。
  [#6966](https://github.com/rust-lang/cargo/pull/6966)
- libgit2 已更新至 0.28.2，Cargo 用其访问 git 仓库。自上次于 11 月更新以来，纳入了数百项更改与修复。
  [#7018](https://github.com/rust-lang/cargo/pull/7018)
- Cargo 现支持 rustc 生成的 dep-info 文件中的绝对路径。
  这为[跟踪二进制文件](https://github.com/rust-lang/rust/pull/61727)（如 libstd）以进行重建检测奠定了基础。（注意：其中包含一个已知 bug。）
  [#7030](https://github.com/rust-lang/cargo/pull/7030)

### 修复
- 修复了 zsh 补全获取命令列表的方式。
  [#6956](https://github.com/rust-lang/cargo/pull/6956)
- 当 `debug` 设为 0 时，构建摘要中不再打印 "+ debuginfo"。
  [#6971](https://github.com/rust-lang/cargo/pull/6971)
- 修复了配置为 `doc = true` 的 example 在 `cargo doc` 下正确生成文档的问题。
  [#7023](https://github.com/rust-lang/cargo/pull/7023)
- 若无法在 CARGO_HOME 中获取只读锁，不失败。这有助于在 CARGO_HOME 不存在、但使用了 `--locked`（意味着不需要 CARGO_HOME）时的情况。
  [#7149](https://github.com/rust-lang/cargo/pull/7149)
- 撤销了 1.35 中当 Cargo 阻塞于锁文件时释放 jobserver token 的更改。它在某些情况下会导致死锁。
  [#7204](https://github.com/rust-lang/cargo/pull/7204)

### 仅 Nightly
- 新增[编译器消息缓存](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#cache-messages)。
  `-Z cache-messages` 标志使 cargo 缓存编译器输出，以便后续运行可重新显示先前的警告。
  [#6933](https://github.com/rust-lang/cargo/pull/6933)
- `-Z mtime-on-use` 不再触及中间产物。
  [#7050](https://github.com/rust-lang/cargo/pull/7050)

## Cargo 1.36 (2019-07-04)
[6f3e9c36...c4fcfb72](https://github.com/rust-lang/cargo/compare/6f3e9c36...c4fcfb72)

### 新增
- 新增了关于目标自动发现的更详细文档。
  [#6898](https://github.com/rust-lang/cargo/pull/6898)
- 🔥 稳定了允许在无网络连接时使用 cargo 的 `--offline` 标志。
  [#6934](https://github.com/rust-lang/cargo/pull/6934)
  [#6871](https://github.com/rust-lang/cargo/pull/6871)

### 变更
- 可在清单中添加 `publish = ["crates-io"]`，以将发布限制为仅 crates.io。
  [#6838](https://github.com/rust-lang/cargo/pull/6838)
- macOS：仅当未设置 `DYLD_FALLBACK_LIBRARY_PATH` 时才包含默认路径。同时从默认集合中移除 `/lib`。
  [#6856](https://github.com/rust-lang/cargo/pull/6856)
- `cargo publish` 现将在登录 token 不可用时提前退出。
  [#6854](https://github.com/rust-lang/cargo/pull/6854)
- HTTP/2 流错误现被视为 "spurious" 并将触发重试。
  [#6861](https://github.com/rust-lang/cargo/pull/6861)
- 在依赖上设置 feature，而该 feature 指向*必需*依赖，现为错误。此前为警告。
  [#6860](https://github.com/rust-lang/cargo/pull/6860)
- `registry.index` 配置值现支持相对 `file:` URL。
  [#6873](https://github.com/rust-lang/cargo/pull/6873)
- macOS：`.dSYM` 目录现符号链接到不含元数据哈希的 example 二进制文件旁，以便调试器能找到它。
  [#6891](https://github.com/rust-lang/cargo/pull/6891)
- 新项目的默认 `Cargo.toml` 模板现包含指向文档的注释链接。
  [#6881](https://github.com/rust-lang/cargo/pull/6881)
- 对 crate 下载摘要的措辞做了一些改进。
  [#6916](https://github.com/rust-lang/cargo/pull/6916)
  [#6920](https://github.com/rust-lang/cargo/pull/6920)
- ✨ 将 `RUST_LOG` 环境变量改为 `CARGO_LOG`，以便使用 `log` crate 的用户代码不会显示 cargo 的调试输出。
  [#6918](https://github.com/rust-lang/cargo/pull/6918)
- 打包时始终包含 `Cargo.toml`，即使未在 `package.include` 中列出。
  [#6925](https://github.com/rust-lang/cargo/pull/6925)
- 包的 include/exclude 值现使用 gitignore 模式而非 glob
  模式。 [#6924](https://github.com/rust-lang/cargo/pull/6924)
- 当 crates.io 超时时提供更好的错误消息。同时改进其他 HTTP 响应码的错误消息。
  [#6936](https://github.com/rust-lang/cargo/pull/6936)

### 性能
- 某些情况下的解析器性能改进。
  [#6853](https://github.com/rust-lang/cargo/pull/6853)
- 通过缓存结果优化 cargo 读取索引 JSON 文件的方式。
  [#6880](https://github.com/rust-lang/cargo/pull/6880)
  [#6912](https://github.com/rust-lang/cargo/pull/6912)
  [#6940](https://github.com/rust-lang/cargo/pull/6940)
- 多项性能改进。
  [#6867](https://github.com/rust-lang/cargo/pull/6867)

### 修复
- 更仔细地跟踪依赖的磁盘上 fingerprint 信息。
  这有助于在构建被中断并重新启动的某些罕见情况下。 [#6832](https://github.com/rust-lang/cargo/pull/6832)
- `cargo run` 现正确地将非 UTF8 参数传递给子进程。
  [#6849](https://github.com/rust-lang/cargo/pull/6849)
- 修复 bash 补全以在 bash 3.2（macOS 自带版本）上运行。
  [#6905](https://github.com/rust-lang/cargo/pull/6905)
- 对 zsh 补全的多项修复与改进。
  [#6926](https://github.com/rust-lang/cargo/pull/6926)
  [#6929](https://github.com/rust-lang/cargo/pull/6929)
- 修复 `cargo update` 在缺少 `Cargo.lock` 文件时忽略 `-p` 参数的问题。
  [#6904](https://github.com/rust-lang/cargo/pull/6904)

### 仅 Nightly
- 新增 [`-Z install-upgrade`
  功能](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#install-upgrade)
  以跟踪已安装 crate 的详细信息，并在过期时更新它们。 [#6798](https://github.com/rust-lang/cargo/pull/6798)
- 新增 [`public-dependency`
  功能](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html#public-dependency)
  ，允许跟踪公共与私有依赖。
  [#6772](https://github.com/rust-lang/cargo/pull/6772)
- 通过 `build.pipelining` 配置选项（`CARGO_BUILD_PIPELINING` 环境变量）新增构建流水线。
  [#6883](https://github.com/rust-lang/cargo/pull/6883)
- `publish-lockfile` 功能有了重大更改。默认现为
  `true`，二进制 crate 将始终发布 `Cargo.lock`。
  发布期间现会重新生成 `Cargo.lock`。`cargo install` 现默认忽略
  `Cargo.lock` 文件，并需要 `--locked` 才能使用锁文件。若检测到被 yank 的依赖，会添加警告。
  [#6840](https://github.com/rust-lang/cargo/pull/6840)

## Cargo 1.35 (2019-05-23)
[6789d8a0...6f3e9c36](https://github.com/rust-lang/cargo/compare/6789d8a0...6f3e9c36)

### 新增
- 为构建脚本新增 `rustc-cdylib-link-arg` 键，以指定 cdylib crate 的链接器参数。
  [#6298](https://github.com/rust-lang/cargo/pull/6298)

### 变更
- 传递测试过滤器（如 `cargo test foo`）时，不构建 examples
  （除非它们设置了 `test = true`）。
  [#6683](https://github.com/rust-lang/cargo/pull/6683)
- 将 `--quiet` 标志从 `cargo test` 转发到 libtest harness，使测试真正安静。
  [#6358](https://github.com/rust-lang/cargo/pull/6358)
- `cargo package` 中检查是否有文件被修改的验证步骤现更严格。它使用内容哈希而非检查文件系统 mtimes。它还检查包中的*所有*文件。
  [#6740](https://github.com/rust-lang/cargo/pull/6740)
- 每当 Cargo 阻塞于文件锁时，现释放 jobserver token。
  [#6748](https://github.com/rust-lang/cargo/pull/6748)
- 针对 TOML 解析器先前允许同名多个表头的 bug 发出警告。
  [#6761](https://github.com/rust-lang/cargo/pull/6761)
- 从元数据哈希中移除了 `CARGO_PKG_*` 环境变量，并将它们加入 fingerprint。这意味着当这些值更改时，不会留下陈旧产物。还将 "repository" 值加入 fingerprint。
  [#6785](https://github.com/rust-lang/cargo/pull/6785)
- `cargo metadata` 在 `resolve.nodes.deps` 中对于没有库的依赖不再显示 `null` 字段。该依赖不再显示。
  [#6534](https://github.com/rust-lang/cargo/pull/6534)
- 若邮箱设为空字符串，`cargo new` 将不再在 `authors` 字段中包含邮箱地址。
  [#6802](https://github.com/rust-lang/cargo/pull/6802)
- `cargo doc --open` 现可在为多个包生成文档时工作。
  [#6803](https://github.com/rust-lang/cargo/pull/6803)
- `cargo install --path P` 现从目录 P 加载 `.cargo/config` 文件。 [#6805](https://github.com/rust-lang/cargo/pull/6805)
- 在版本需求中使用 semver 元数据（如 `1.0.0+1234`）现发出警告，说明它被忽略。
  [#6806](https://github.com/rust-lang/cargo/pull/6806)
- `cargo install` 现拒绝某些标志组合，其中部分标志本会被忽略。
  [#6801](https://github.com/rust-lang/cargo/pull/6801)
- 某些情况下的解析器性能改进。
  [#6776](https://github.com/rust-lang/cargo/pull/6776)

### 修复
- 修复了运行分开的命令（如先 `cargo build` 再 `cargo test`）时，第二条命令可能使用构建脚本陈旧结果的问题。
  [#6720](https://github.com/rust-lang/cargo/pull/6720)
- 修复了若 `.gitignore` 文件匹配根包目录时 `cargo fix` 不能正常工作的问题。
  [#6767](https://github.com/rust-lang/cargo/pull/6767)
- 修复了若在 profile 中设置 `panic=unwind` 时意外多次编译 lib 的问题。 [#6781](https://github.com/rust-lang/cargo/pull/6781)
- `build.target` 配置值中 JSON 文件的路径现已规范化，以修复构建依赖。
  [#6778](https://github.com/rust-lang/cargo/pull/6778)
- 修复了若构建脚本的编译被中断（如被杀死）时重新运行构建脚本的问题。 [#6782](https://github.com/rust-lang/cargo/pull/6782)
- 修复了 `cargo new` 初始化 fossil 仓库的问题。
  [#6792](https://github.com/rust-lang/cargo/pull/6792)
- 修复了在使用 `git-fetch-with-cli` 功能时支持更新发生过 force push 的 git 仓库的问题。`git-fetch-with-cli` 失败时现也显示更多错误信息。
  [#6800](https://github.com/rust-lang/cargo/pull/6800)
- 为 WASM 目标构建的 `--example` 二进制文件已修复：文件名不再包含元数据哈希，并正确出现在 `compiler-artifact` JSON 消息中。
  [#6812](https://github.com/rust-lang/cargo/pull/6812)

### 仅 Nightly
- `cargo clippy-preview` 现为内置 cargo 命令。
  [#6759](https://github.com/rust-lang/cargo/pull/6759)
- `build-override` profile 设置现包含 proc-macros 及其依赖。
  [#6811](https://github.com/rust-lang/cargo/pull/6811)
- 可选依赖与目标依赖现与 `-Z offline` 配合更好。
  [#6814](https://github.com/rust-lang/cargo/pull/6814)

## Cargo 1.34 (2019-04-11)
[f099fe94...6789d8a0](https://github.com/rust-lang/cargo/compare/f099fe94...6789d8a0)

### 新增
- 🔥 稳定了对[备用
  registry](https://doc.rust-lang.org/1.34.0/cargo/reference/registries.html)的支持。
  [#6654](https://github.com/rust-lang/cargo/pull/6654)
- 新增了关于将 builds.sr.ht 持续集成与 Cargo 一起使用的文档。
  [#6565](https://github.com/rust-lang/cargo/pull/6565)
- `Cargo.lock` 顶部现包含说明其为 `@generated` 的注释。
  [#6548](https://github.com/rust-lang/cargo/pull/6548)
- 现已支持 Azure DevOps 徽章。
  [#6264](https://github.com/rust-lang/cargo/pull/6264)
- 若 `--exclude` 标志指定了未知包，新增警告。
  [#6679](https://github.com/rust-lang/cargo/pull/6679)

### 变更
- `cargo test --doc --no-run` 不做任何事，因此现显示表明该效果的错误。 [#6628](https://github.com/rust-lang/cargo/pull/6628)
- 对 bash 补全的多项更新：添加缺失的选项与命令、支持 libtest 补全、对 `--target` 补全使用 rustup、回退到文件名补全、修复编辑命令行。
  [#6644](https://github.com/rust-lang/cargo/pull/6644)
- 发布带有 `[patch]` 段的 crate 不再产生错误。
  发布前会从清单中移除 `[patch]` 段。
  [#6535](https://github.com/rust-lang/cargo/pull/6535)
- `build.incremental = true` 配置值现与 `CARGO_INCREMENTAL=1` 同等对待，此前会被忽略。
  [#6688](https://github.com/rust-lang/cargo/pull/6688)
- 无论 HTTP 响应码如何，现始终显示来自 registry 的错误。 [#6771](https://github.com/rust-lang/cargo/pull/6771)

### 修复
- 修复了 `cargo run --example` 的 bash 补全。
  [#6578](https://github.com/rust-lang/cargo/pull/6578)
- 修复了使用*本地* registry 并同时运行多个构建同一 crate 的 cargo 命令时的竞态条件。
  [#6591](https://github.com/rust-lang/cargo/pull/6591)
- 修复了进度条的一些闪烁与过度更新。
  [#6615](https://github.com/rust-lang/cargo/pull/6615)
- 修复了使用返回不正确凭证的 git credential helper 时的挂起。 [#6681](https://github.com/rust-lang/cargo/pull/6681)
- 修复了使用本地 registry 解析被 yank 的 crate 的问题。
  [#6750](https://github.com/rust-lang/cargo/pull/6750)

### 仅 Nightly
- 新增 `-Z mtime-on-use` 标志，使 crate 被使用时更新文件系统上的 mtime。旨在未来能够跟踪陈旧产物以清理未使用的文件。
  [#6477](https://github.com/rust-lang/cargo/pull/6477)
  [#6573](https://github.com/rust-lang/cargo/pull/6573)
- 新增实验性 `-Z dual-proc-macros`，以便同时为 host 与 target 构建 proc macros。
  [#6547](https://github.com/rust-lang/cargo/pull/6547)

## Cargo 1.33 (2019-02-28)
[8610973a...f099fe94](https://github.com/rust-lang/cargo/compare/8610973a...f099fe94)

### 新增
- `compiler-artifact` JSON 消息现包含 `"executable"` 键，其中包含所构建可执行文件的路径。
  [#6363](https://github.com/rust-lang/cargo/pull/6363)
- man pages 已重写，现与 Web 文档一并发布。 [#6405](https://github.com/rust-lang/cargo/pull/6405)
- `cargo login` 保存 token 后现显示确认信息。
  [#6466](https://github.com/rust-lang/cargo/pull/6466)
- 若 `[patch]` 条目不匹配任何包，现发出警告。
  [#6470](https://github.com/rust-lang/cargo/pull/6470)
- `cargo metadata` 现包含包的 `links` 键。
  [#6480](https://github.com/rust-lang/cargo/pull/6480)
- 使用 `-vv` 的 "Very verbose" 输出现显示 cargo 运行进程时所设置的环境变量。
  [#6492](https://github.com/rust-lang/cargo/pull/6492)
- 不带参数的 `--example`、`--bin`、`--bench` 或 `--test` 现列出这些选项的可用目标。
  [#6505](https://github.com/rust-lang/cargo/pull/6505)
- Windows：若进程以扩展状态退出码失败，现显示该码的人类可读名称。
  [#6532](https://github.com/rust-lang/cargo/pull/6532)
- 为 `cargo package` 与 `cargo publish` 命令新增 `--features`、`--no-default-features` 与 `--all-features` 标志，以便在验证包时使用给定的 features。
  [#6453](https://github.com/rust-lang/cargo/pull/6453)

### 变更
- 若 `cargo fix` 无法编译修复后的代码，rustc 错误现显示在控制台上。
  [#6419](https://github.com/rust-lang/cargo/pull/6419)
- 从 `cargo login` 中隐藏未使用的 `--host` 标志。
  [#6466](https://github.com/rust-lang/cargo/pull/6466)
- 构建脚本 fingerprint 现包含 rustc 版本。
  [#6473](https://github.com/rust-lang/cargo/pull/6473)
- macOS：改为设置 `DYLD_FALLBACK_LIBRARY_PATH` 而非
  `DYLD_LIBRARY_PATH`。 [#6355](https://github.com/rust-lang/cargo/pull/6355)
- `RUSTFLAGS` 现包含在元数据哈希中，这意味着更改标志不会覆盖先前构建的文件。
  [#6503](https://github.com/rust-lang/cargo/pull/6503)
- 更新 crate 图时，不相关的被 yank crate 被错误地移除。现尽可能保持其原始版本。这导致在 `cargo update -p
  somecrate` 期间不相关的包被降级。 [#5702](https://github.com/rust-lang/cargo/issues/5702)
- TOML 文件现支持 [0.5 TOML
  语法](https://github.com/toml-lang/toml/blob/master/CHANGELOG.md#050--2018-07-11)。

### 修复
- `cargo fix` 现将忽略修改多个文件的建议。
  [#6402](https://github.com/rust-lang/cargo/pull/6402)
- `cargo fix` 现一次只修复一个目标，以处理共享相同源文件的目标。
  [#6434](https://github.com/rust-lang/cargo/pull/6434)
- 修复了 bash 补全显示 cargo 命令列表的问题。
  [#6461](https://github.com/rust-lang/cargo/issues/6461)
- `cargo init` 现将避免在 `.gitignore` 文件中创建重复条目。 [#6521](https://github.com/rust-lang/cargo/pull/6521)
- 构建现尝试检测编译过程中文件是否被修改，从而允许你再次构建并拾取新更改。这通过跟踪编译*开始*而非结束的时间来完成。另外，[#5919](https://github.com/rust-lang/cargo/pull/5919) 已撤销，意味着 cargo *不会*将相等的文件系统 mtimes 视为需要重建。 [#6484](https://github.com/rust-lang/cargo/pull/6484)

### 仅 Nightly
- 允许在 `[patch]` 表中使用 registry *名称*，而不只是 URL。
  [#6456](https://github.com/rust-lang/cargo/pull/6456)
- `cargo metadata` 为依赖新增了 `registry` 键。
  [#6500](https://github.com/rust-lang/cargo/pull/6500)
- Registry 名称现限制为与包名相同的风格（字母数字、`-` 与 `_` 字符）。
  [#6469](https://github.com/rust-lang/cargo/pull/6469)
- `cargo login` 现显示来自 registry 配置的 `/me` URL。
  [#6466](https://github.com/rust-lang/cargo/pull/6466)
- `cargo login --registry=NAME` 现支持交互式输入 token。
  [#6466](https://github.com/rust-lang/cargo/pull/6466)
- Registry 现可从 `config.json` 中省略 `api` 键，以表明它们不支持 API 访问。
  [#6466](https://github.com/rust-lang/cargo/pull/6466)
- 修复了将 `--message-format=json` 与 metabuild 一起使用时的 panic。
  [#6432](https://github.com/rust-lang/cargo/pull/6432)
- 修复了使用备用 registry 时检测发布到 crates.io 的问题。
  [#6525](https://github.com/rust-lang/cargo/pull/6525)

## Cargo 1.32 (2019-01-17)
[339d9f9c...8610973a](https://github.com/rust-lang/cargo/compare/339d9f9c...8610973a)

### 新增
- 注册表现在可以在发布成功后显示警告。
  [#6303](https://github.com/rust-lang/cargo/pull/6303)
- 在文档中新增了[术语表](appendix/glossary.md)。
  [#6321](https://github.com/rust-lang/cargo/pull/6321)
- 为 `cargo check` 新增了别名 `c`。
  [#6218](https://github.com/rust-lang/cargo/pull/6218)

### 变更
- 🔥 HTTP/2 多路复用现已默认启用。可使用 `http.multiplexing`
  配置值将其禁用。
  [#6271](https://github.com/rust-lang/cargo/pull/6271)
- 使用 ANSI 转义序列清行，而不再使用空格。
  [#6233](https://github.com/rust-lang/cargo/pull/6233)
- 检出 git 依赖时禁用 git 模板，以免引发问题。
  [#6252](https://github.com/rust-lang/cargo/pull/6252)
- 使用 `net.git-fetch-with-cli` 选项时包含 `--update-head-ok`
  git 标志。这有助于防止获取某些仓库时失败。
  [#6250](https://github.com/rust-lang/cargo/pull/6250)
- 在 `cargo package` 的验证步骤中解压 crate 时，不再设置
  文件系统 mtime，此前这在某些罕见文件系统上会失败。
  [#6257](https://github.com/rust-lang/cargo/pull/6257)
- 在 `Cargo.toml` 中，`crate-type = ["proc-macro"]` 现在与
  `proc-macro = true` 同等对待。
  [#6256](https://github.com/rust-lang/cargo/pull/6256)
- 若在虚拟工作区中设置了 `dependencies`、`features`、`target` 或
  `badges`，将报错。若在工作区成员中使用了 `replace` 或 `patch`，
  将显示警告。
  [#6276](https://github.com/rust-lang/cargo/pull/6276)
- 在某些情况下改进了解析器的性能。
  [#6283](https://github.com/rust-lang/cargo/pull/6283)
  [#6366](https://github.com/rust-lang/cargo/pull/6366)
- `.rmeta` 文件不再硬链接到基础 target 目录
  （`target/debug`）。[#6292](https://github.com/rust-lang/cargo/pull/6292)
- 若多个目标以相同的输出文件名构建，将发出警告。
  [#6308](https://github.com/rust-lang/cargo/pull/6308)
- 使用 `cargo build`（不带 `--release`）时，基准测试现在使用
  "test" profile 而非 "bench" 构建。这样更便于调试基准测试，
  并避免令人困惑的行为。
  [#6309](https://github.com/rust-lang/cargo/pull/6309)
- 用户别名现在可以覆盖内置别名（`b`、`r`、`t` 和 `c`）。
  [#6259](https://github.com/rust-lang/cargo/pull/6259)
- 设置 `autobins=false` 现在会禁用推断目标的自动发现。
  [#6329](https://github.com/rust-lang/cargo/pull/6329)
- 若项目使用不稳定特性，`cargo verify-project` 现在在稳定版上将失败。
  [#6326](https://github.com/rust-lang/cargo/pull/6326)
- 现在允许名称中含有内部 `.` 的平台目标。
  [#6255](https://github.com/rust-lang/cargo/pull/6255)
- `cargo clean --release` 现在只删除 release 目录。
  [#6349](https://github.com/rust-lang/cargo/pull/6349)

### 修复
- 避免在 `cargo new` 的电子邮件地址中添加多余的尖括号。
  [#6243](https://github.com/rust-lang/cargo/pull/6243)
- 若设置了 CI 环境变量，则禁用进度条。
  [#6281](https://github.com/rust-lang/cargo/pull/6281)
- 避免将所有 rustc 输出保留在内存中。
  [#6289](https://github.com/rust-lang/cargo/pull/6289)
- 若 JSON 解析失败且 rustc 以非零状态退出，不再丢失解析失败消息。
  [#6290](https://github.com/rust-lang/cargo/pull/6290)
- 修复了存在构建脚本时重命名项目目录的问题。
  [#6328](https://github.com/rust-lang/cargo/pull/6328)
- 修复了若示例设置了 `crate_type = ["bin"]` 时，
  `cargo run --example NAME` 无法正确工作的问题。
  [#6330](https://github.com/rust-lang/cargo/pull/6330)
- 修复了 `cargo package` git 发现过于激进的问题。
  `--allow-dirty` 现在会完全禁用 git 仓库检查。
  [#6280](https://github.com/rust-lang/cargo/pull/6280)
- 修复了 `[patch]` 依赖的构建变更跟踪问题，该问题会导致
  `cargo build` 在本不应重建时进行重建。
  [#6493](https://github.com/rust-lang/cargo/pull/6493)

### 仅 Nightly
- 允许在注册表 URL 中使用用户名。
  [#6242](https://github.com/rust-lang/cargo/pull/6242)
- 在 build-plan JSON 结构中新增了 `"compile_mode"` 键，以便区分
  运行自定义构建脚本与编译构建脚本。
  [#6331](https://github.com/rust-lang/cargo/pull/6331)
- `--out-dir` 不再复制构建脚本。
  [#6300](https://github.com/rust-lang/cargo/pull/6300)

## Cargo 1.31 (2018-12-06)
[36d96825...339d9f9c](https://github.com/rust-lang/cargo/compare/36d96825...339d9f9c)

### 新增
- 🔥 稳定了对 2018 edition 的支持。
  [#5984](https://github.com/rust-lang/cargo/pull/5984)
  [#5989](https://github.com/rust-lang/cargo/pull/5989)
- 🔥 新增了在 Cargo.toml 中[重命名
  依赖](https://doc.rust-lang.org/1.31.0/cargo/reference/specifying-dependencies.html#renaming-dependencies-in-cargotoml)
  的能力。[#6319](https://github.com/rust-lang/cargo/pull/6319)
- 🔥 新增了对 HTTP/2 流水线与多路复用的支持。设置
  `http.multiplexing` 配置值以启用。
  [#6005](https://github.com/rust-lang/cargo/pull/6005)
- 新增了 `http.debug` 配置值以调试 HTTP 连接。使用
  `CARGO_HTTP_DEBUG=true RUST_LOG=cargo::ops::registry cargo build` 可显示
  调试信息。[#6166](https://github.com/rust-lang/cargo/pull/6166)
- 构建时会根据 `Cargo.toml` 中的 repository 值设置
  `CARGO_PKG_REPOSITORY` 环境变量 。
  [#6096](https://github.com/rust-lang/cargo/pull/6096)

### 变更
- `cargo test --doc` 现在会拒绝其他标志，而不再忽略它们。
  [#6037](https://github.com/rust-lang/cargo/pull/6037)
- `cargo install` 会忽略 `~/.cargo/config`。
  [#6026](https://github.com/rust-lang/cargo/pull/6026)
- `cargo version --verbose` 现在与 `cargo -vV` 相同。
  [#6076](https://github.com/rust-lang/cargo/pull/6076)
- `Cargo.lock` 顶部的注释现在会被保留。
  [#6181](https://github.com/rust-lang/cargo/pull/6181)
- 在"非常详细"模式（`cargo build -vv`）下构建时，构建脚本
  输出会加上包名与版本的前缀，例如 `[foo 0.0.1]`。
  [#6164](https://github.com/rust-lang/cargo/pull/6164)
- 若 `cargo fix --broken-code` 在应用修复后编译失败，
  文件不再被还原，而是保留在损坏状态。
  [#6316](https://github.com/rust-lang/cargo/pull/6316)

### 修复
- Windows：使用 `cargo run` 时将 Ctrl-C 传递给进程。
  [#6004](https://github.com/rust-lang/cargo/pull/6004)
- macOS：修复 bash 补全。
  [#6038](https://github.com/rust-lang/cargo/pull/6038)
- 在 bash 补全中补全 `+toolchain` 时支持任意工具链名称。
  [#6038](https://github.com/rust-lang/cargo/pull/6038)
- 修复了解析器在对失败依赖进行回溯时的边界情况。
  [#5988](https://github.com/rust-lang/cargo/pull/5988)
- 修复了 `cargo test --all-targets` 会将 lib 测试运行三次的问题。
  [#6039](https://github.com/rust-lang/cargo/pull/6039)
- 修复了将重命名的依赖发布到 crates.io 的问题。
  [#5993](https://github.com/rust-lang/cargo/pull/5993)
- 修复了在含有多个二进制文件的 git 仓库上执行 `cargo install` 的问题。
  [#6060](https://github.com/rust-lang/cargo/pull/6060)
- 修复了 rustc 发出的深层嵌套 JSON 丢失的问题。
  [#6081](https://github.com/rust-lang/cargo/pull/6081)
- Windows：修复将 msys 终端锁定为 60 个字符的问题。
  [#6122](https://github.com/rust-lang/cargo/pull/6122)
- 修复了带连字符的重命名依赖。
  [#6140](https://github.com/rust-lang/cargo/pull/6140)
- 修复了当 dylib 同时存在于 `target/debug` 和 `target/debug/deps`
  时链接到错误 dylib 的问题。
  [#6167](https://github.com/rust-lang/cargo/pull/6167)
- 修复了使用 `panic=abort` 时某些不必要的重新编译。
  [#6170](https://github.com/rust-lang/cargo/pull/6170)

### 仅 Nightly
- 为 `cargo install` 新增了 `--registry` 标志。
  [#6128](https://github.com/rust-lang/cargo/pull/6128)
- 新增了 `registry.default` 配置值，用于指定在未传递
  `--registry` 标志时使用的默认注册表。
  [#6135](https://github.com/rust-lang/cargo/pull/6135)
- 为 `cargo new` 和 `cargo init` 新增了 `--registry` 标志。
  [#6135](https://github.com/rust-lang/cargo/pull/6135)

## Cargo 1.30 (2018-10-25)
[524a578d...36d96825](https://github.com/rust-lang/cargo/compare/524a578d...36d96825)

### 新增
- 🔥 新增了在构建期间显示进度的动画进度条。
  [#5995](https://github.com/rust-lang/cargo/pull/5995/)
- 为 `cargo metadata` 新增了 `resolve.nodes.deps` 键，其中包含更多
  关于已解析依赖的信息，并能正确处理重命名的依赖。
  [#5871](https://github.com/rust-lang/cargo/pull/5871)
- 创建包时，若无法发现 git 仓库中的文件是否 dirty，使用 `-v` 会提供
  更多细节。同时修复了 Windows 上的发现问题。
  [#5858](https://github.com/rust-lang/cargo/pull/5858)
- 诸如 `--bin`、`--test`、`--example`、`--bench` 或 `--lib` 之类的过滤器
  可在工作区中使用，而无需选择特定包。
  [#5873](https://github.com/rust-lang/cargo/pull/5873)
- `cargo run` 可在工作区中使用，而无需选择特定包。
  [#5877](https://github.com/rust-lang/cargo/pull/5877)
- `cargo doc --message-format=json` 现在会输出 rustdoc 的 JSON 消息。
  [#5878](https://github.com/rust-lang/cargo/pull/5878)
- 新增了 `--message-format=short` 以显示单行消息。
  [#5879](https://github.com/rust-lang/cargo/pull/5879)
- 在 `.crate` 包中新增了 `.cargo_vcs_info.json` 文件，用于捕获
  当前 git hash。[#5886](https://github.com/rust-lang/cargo/pull/5886)
- 新增了 `net.git-fetch-with-cli` 配置选项，使用 `git`
  可执行文件获取仓库，而不再使用内置的 libgit2
  库。[#5914](https://github.com/rust-lang/cargo/pull/5914)
- 为 `cargo metadata` 新增了 `required-features`。
  [#5902](https://github.com/rust-lang/cargo/pull/5902)
- 在包内执行 `cargo uninstall` 现在会卸载该包。
  [#5927](https://github.com/rust-lang/cargo/pull/5927)
- 为 `cargo fix` 新增了 `--allow-staged` 标志，允许在文件已
  暂存到 git 时运行。[#5943](https://github.com/rust-lang/cargo/pull/5943)
- 新增了 `net.low-speed-limit` 配置值，并且 http 操作也会遵守
  `net.timeout`。[#5957](https://github.com/rust-lang/cargo/pull/5957)
- 为 `cargo new` 新增了 `--edition` 标志。
  [#5984](https://github.com/rust-lang/cargo/pull/5984)
- 在 beta 期间临时稳定了 2018 edition 支持。
  [#5984](https://github.com/rust-lang/cargo/pull/5984)
  [#5989](https://github.com/rust-lang/cargo/pull/5989)
- 新增了对 `target.'cfg(…)'.runner` 配置值的支持，用于为使用
  配置表达式的目标指定 run/test/bench runner。
  [#5959](https://github.com/rust-lang/cargo/pull/5959)

### 变更
- Windows：主进程退出时，`cargo run` 不会终止子进程。
  [#5887](https://github.com/rust-lang/cargo/pull/5887)
- 改用 `opener` crate，在执行 `cargo doc
  --open` 时打开网页浏览器。这应能在所有平台上更可靠地选择
  系统首选浏览器。[#5888](https://github.com/rust-lang/cargo/pull/5888)
- 相等的文件 mtime 现在也会导致目标被重建。此前仅当文件
  严格*新于*上次构建时才会触发重建。
  [#5919](https://github.com/rust-lang/cargo/pull/5919)
- 运行 `cargo install` 时忽略 `build.target` 配置值。
  [#5874](https://github.com/rust-lang/cargo/pull/5874)
- 对 `cargo fix` 忽略 `RUSTC_WRAPPER`。
  [#5983](https://github.com/rust-lang/cargo/pull/5983)
- 忽略空的 `RUSTC_WRAPPER`。
  [#5985](https://github.com/rust-lang/cargo/pull/5985)

### 修复
- 修复了在 `Cargo.toml` 中带有 edition 字段时创建包的错误。
  [#5908](https://github.com/rust-lang/cargo/pull/5908)
- 在工作区中更一致地为路径依赖使用相对路径。
  [#5935](https://github.com/rust-lang/cargo/pull/5935)
- `cargo fix` 现在总会运行，即使此前已运行过。
  [#5944](https://github.com/rust-lang/cargo/pull/5944)
- Windows：尝试更可靠地检测终端宽度。基于 msys 的
  终端被强制为 60 个字符宽。
  [#6010](https://github.com/rust-lang/cargo/pull/6010)
- 允许在 `cargo doc --document-private-items` 中使用多个 target 标志。
  [6022](https://github.com/rust-lang/cargo/pull/6022)

### 仅 Nightly
- 新增了
  [metabuild](https://doc.rust-lang.org/1.30.0/cargo/reference/unstable.html#metabuild)。
  [#5628](https://github.com/rust-lang/cargo/pull/5628)

