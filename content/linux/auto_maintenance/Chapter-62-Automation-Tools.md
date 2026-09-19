+++
title = "第62章：其他自动化工具"
weight = 620
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第六十二章：其他自动化工具

## 62.1 SaltStack

### SaltStack 简介

SaltStack（简称 Salt）是另一个强大的自动化工具，与 Ansible 有很多相似之处，但也有一些独特优势。

```mermaid
graph LR
    A[Salt Master] -->|ZeroMQ| B[Minion 1]
    A -->|ZeroMQ| C[Minion 2]
    A -->|ZeroMQ| D[Minion N]
```

| 特性 | Ansible | SaltStack |
|------|---------|-----------|
| 通信方式 | SSH（每次新建连接，可复用） | ZeroMQ 长连接（也可 `salt-ssh` 走 SSH） |
| 执行速度 | 快（主机多时受 SSH 并发限制） | 非常快（长连接下发，毫秒级响应） |
| Agent | 无 | 默认需要 Minion；`salt-ssh` / masterless 可无 |
| 实时能力 | 偏"一批任务跑完就结束" | 支持事件总线 + Reactor，可做实时响应 |
| 配置语言 | YAML（Playbook） | YAML（SLS）+ Python 渲染 |
| 配套数据层 | 变量 + ansible-vault | Grains（机器事实）+ Pillar（下发的机密） |
| 学习曲线 | 低 | 中（概念更多：Grains/Pillar/Reactor/Syndic） |

一句话概括差别：**Ansible 是"从控制机推任务下去"，Salt 是"一群常驻小兵持续听指挥"**。前者简单直接，后者在大规模、需要实时响应时更强。

### SaltStack 安装

```bash
# 说明：发行版自带的 salt 包版本往往很旧，
#       官方推荐直接配 Salt 自己的软件源（saltproject.io）。

# RHEL / Rocky / Alma 9
sudo dnf install -y https://repo.saltproject.io/salt/py3/redhat/9/x86_64/latest/SALTSTACK-GPG-KEY.pub
curl -fsSL https://repo.saltproject.io/salt/py3/redhat/9/x86_64/latest.repo | sudo tee /etc/yum.repos.d/salt.repo
sudo dnf clean expire-cache
sudo dnf install -y salt-master salt-minion

# Debian / Ubuntu
sudo mkdir -p /etc/apt/keyrings
sudo curl -fsSL https://repo.saltproject.io/salt/py3/ubuntu/22.04/amd64/latest/SALTSTACK-GPG-KEY.pub \
  -o /etc/apt/keyrings/salt-archive-keyring.pgp
echo "deb [signed-by=/etc/apt/keyrings/salt-archive-keyring.pgp] https://repo.saltproject.io/salt/py3/ubuntu/22.04/amd64/latest jammy main" \
  | sudo tee /etc/apt/sources.list.d/salt.list
sudo apt update && sudo apt install -y salt-master salt-minion

# 启动服务（Master 上通常同时跑 master 和 minion，方便用 salt-call 在本地测试）
sudo systemctl enable --now salt-master
sudo systemctl enable --now salt-minion
```

> 💡 **Salt 的 Master 端还依赖几个东西**：Python、ZeroMQ（`pyzmq`）、以及端口 **4505（发布/命令通道）和 4506（返回通道）**。防火墙要放行这两个端口：
>
> ```bash
> sudo firewall-cmd --permanent --add-port=4505-4506/tcp && sudo firewall-cmd --reload
> # Ubuntu 用 ufw：sudo ufw allow 4505:4506/tcp
> ```

### Minion 配置

```bash
# /etc/salt/minion.d/master.conf
master: 192.168.1.100      # Master 地址（也可以写主机名）
id: web-server-1           # Minion ID：**一旦确定就别改**，改了等于换了一台新机器
master_port: 4505          # Master 的发布端口；返回端口 4506 在 Master 侧由 ret_port 定义

# 启动 Minion
sudo systemctl enable --now salt-minion

# 查看自己的 ID 和生成的公钥
sudo salt-call --local grains.get id
sudo cat /etc/salt/pki/minion/minion.pub
```

> ⚠️ Minion ID 默认取主机名。**云环境中主机名经常是随机串**，建议显式设置 `id:`（或在 `/etc/salt/minion_id` 里写死），否则主机重建后 ID 变了，Master 上会多出一堆"僵尸 Minion"。

### Master 配置

```bash
# /etc/salt/master.d/master.conf
interface: 0.0.0.0
publish_port: 4505
ret_port: 4506
worker_threads: 10
timeout: 10
file_roots:
  base:
    - /srv/salt
pillar_roots:
  base:
    - /srv/pillar
```

`file_roots` 和 `pillar_roots` 是 Salt 的两大目录约定：**`/srv/salt` 放 State 和模板，`/srv/pillar` 放机密数据**。文件在 State 里通过 `salt://` 引用（对应 `/srv/salt`），Pillar 数据用 `pillar['key']` 取值。

### Salt 命令

```bash
# 查看密钥状态：Unaccepted / Accepted / Denied
sudo salt-key -L

# 查看待接受密钥的指纹，人工核对后再接受（生产环境推荐）
sudo salt-key -f web-server-1
sudo salt-key -a web-server-1      # 接受单个

# 接受全部（方便，但等于"谁连上来都放行"，仅限测试环境）
sudo salt-key -A

# 测试 Minion 连通性
sudo salt '*' test.ping

# 执行命令
sudo salt 'web-*' cmd.run "uptime"

# 按 Grains / Pillar 定向（不靠主机名）
sudo salt -G 'os:Ubuntu' test.ping
sudo salt -I 'env:prod' test.ping

# 查看某台机器的完整信息
sudo salt 'web-1' grains.items
sudo salt 'web-1' pillar.items

# 安装包
sudo salt 'db-*' pkg.install nginx

# 复制文件
sudo salt 'web-*' cp.get_file salt://nginx/nginx.conf /etc/nginx/nginx.conf
```

> ⚠️ **接受密钥前先核对**：Master 与 Minion 之间靠"密钥交换 + AES 加密"通信，但**首次握手没有任何第三方背书**。如果攻击者抢先用某台机器的 ID 连上来，你也接受了它的密钥，那么后续命令就发到攻击者机器上了。方法：Minion 上执行 `salt-call --local key.finger`，和 Master 上 `salt-key -f <id>` 显示的指纹比对。

### Salt State（SLS）

```yaml
# /srv/salt/nginx/init.sls
nginx_install:
  pkg.installed:
    - name: nginx

nginx_service:
  service.running:
    - name: nginx
    - enable: true
    - require:
      - pkg: nginx_install

nginx_config:
  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://nginx/nginx.conf
    - template: jinja
    - require:
      - pkg: nginx_install
    - watch_in:
      - service: nginx_service      # 配置文件变化时，自动重启服务
```

> ⚠️ 原示例把两个 State ID 写成了一个（`nginx_config` 下面同时出现 `file.managed` 和 `service.running`），这是无效的 YAML 结构。**一个 ID 只能对应一个 State 声明**；要让"文件变化触发服务重启"，正确写法是用 `watch_in` 反向声明（如上），或把 `watch` 写在服务那个 ID 里。

这几行 SLS 体现了 Salt 的核心思想：

- **每个 ID 声明"最终状态"**，而不是"执行什么命令"；已满足就不动（幂等）。
- **`require` / `watch` / `watch_in` 定义依赖与触发关系**：`require` 只管顺序，`watch` 额外带"发生变化就重启/重载"的语义。
- **`salt://` 指向 `file_roots`**，模板、静态文件都从那里取。

再看一个 `top.sls`——它决定"哪些机器应用哪些 State"，和 Pillar 的 `top.sls` 是两个不同的文件：

```yaml
# /srv/salt/top.sls
base:
  '*':
    - common             # 所有机器都应用 common
  'web-*':
    - match: glob
    - nginx
  'os:Ubuntu':
    - match: grain
    - ubuntu-extra
```

### 执行 State

```bash
# 应用一个指定的 State（对应 /srv/salt/nginx/init.sls）
sudo salt '*' state.apply nginx

# 等价写法
sudo salt '*' state.sls nginx

# 应用全部 State：按 top.sls 的规则给每台机器收敛到目标状态
sudo salt '*' state.highstate

# 先空跑看会改什么（test=True 是全局试运行，强烈推荐）
sudo salt '*' state.apply nginx test=True
sudo salt '*' state.highstate test=True

# 查看 top.sls 最终给每台机器生成了什么
sudo salt '*' state.show_top
sudo salt '*' state.show_highstate
```

> 💡 `state.apply nginx` 与 `state.highstate` 的区别，类似 Ansible 里"指定标签执行"和"整本剧本跑一遍"：**日常调试用 `state.apply <名字>`，新机器初始化或定期收敛用 `state.highstate`**。改动较大的时候先加 `test=True` 空跑一遍，看清将要发生什么再实跑。

### Salt Pillar

```yaml
# /srv/pillar/common.sls —— 这里只写"数据"，不写 Jinja 逻辑
mysql_root_password: "change-me-in-production"
app_version: 1.0.0

# /srv/pillar/top.sls —— 决定"哪台机器拿到哪些 pillar 文件"
base:
  '*':
    - common
  'db-*':
    - database
```

> ⚠️ 常见误区：**Pillar 文件是纯数据文件**，里面写 `{{ pillar.get(...) }}` 是没有意义的（自己引用自己）。要在 State 里取用：
>
> ```yaml
> # /srv/salt/mysql/init.sls
> mysql_config:
>   file.managed:
>     - name: /etc/mysql/my.cnf
>     - source: salt://mysql/my.cnf
>     - template: jinja
>     - defaults:
>         root_password: {{ pillar['mysql_root_password'] }}
> ```

Pillar 与 Grains 的区别，一句话说清：**Grains 是"机器自己报出来的事实"（OS、内存、IP），Pillar 是"你下发给这台机器的机密数据"（密码、证书）**。前者是只读的现状，后者是可控的配置。

### Salt Grains

Grains 是 Minion 启动时收集的静态信息（系统类型、内核、内存、IP……），也是 Salt 里最主要的"定向依据"。

```bash
# 查看某台机器的全部 grains
sudo salt 'web-*' grains.items

# 只看关心的几项
sudo salt '*' grains.item os osrelease num_cpus

# 按 grains 定向执行（-G = 按 grains 匹配）
sudo salt -G 'os:Ubuntu' pkg.install nginx
sudo salt -G 'os_family:RedHat' cmd.run 'dnf -y update'
```

自定义 grains 有两种方式：

```yaml
# 方式一：静态文件 /etc/salt/grains（简单直接）
roles:
  - webserver
  - api
environment: production
```

```yaml
# 方式二：写在 State 里，让它随配置自动生成（推荐，可版本化）
# /srv/salt/grains/init.sls
grains_role:
  grains.present:
    - name: roles
    - value: [webserver, api]
```

```bash
# 写完后刷新一下（静态文件方式需要重启 minion 或执行 saltutil.sync_grains）
sudo salt '*' saltutil.sync_grains
```

### Salt Masterless 模式

没有 Master 的 Salt，就是"本地执行的配置工具"。适合网络隔离环境、单机初始化、或者只是想用 Salt 的 State 语法而懒得搭 Master：

```bash
# 一条命令在本地应用一个 State
salt-call --local state.apply nginx

# 本地 highstate
salt-call --local state.highstate

# 本地执行命令
salt-call --local cmd.run 'df -h'
```

```yaml
# /etc/salt/minion.d/masterless.conf —— 让它彻底脱离 Master
master_type: disable
file_client: local
file_roots:
  base:
    - /srv/salt
pillar_roots:
  base:
    - /srv/pillar
```

> 💡 **Masterless + 云初始化脚本**是一个很实用的组合：把 `/srv/salt` 打进镜像或由 CI 分发，云主机开机时执行 `salt-call --local state.highstate` 完成自我配置，完全不依赖 Master 在线。

### Salt Reactor（事件驱动）

Reactor 让 Salt 能"监听事件并自动反应"，这是它比 Ansible 更进一步的自动化能力：

```yaml
# /etc/salt/master
reactor:
  - 'minion_start':            # 事件名（新的 Minion 上线时触发）
    - /srv/reactor/start.sls
  - 'salt/auth':               # 有 Minion 请求认证时触发（可自动签发或拒绝）
    - /srv/reactor/auth.sls
```

```yaml
# /srv/reactor/start.sls
# 新机器一上线就自动应用基础配置
new_minion_bootstrap:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - base_setup
```

> ⚠️ Reactor 写起来灵活但**调试困难**，一旦形成"事件链"就容易失控（A 触发 B、B 又触发 A）。建议只用于少量明确场景：新机器自动打基础配置、证书自动续期、异常登录告警。

### Salt Wheel 与 Runner

Wheel 模块用于**管理 Salt Master 自身**（主要是密钥），Runner 则是"在 Master 上执行的内置工具"：

```bash
# 列出所有 Minion 密钥（含未接受的）
sudo salt-run wheel.key.list_all

# 按匹配规则批量接受 / 拒绝
sudo salt-run wheel.key.accept match='web-*'
sudo salt-run wheel.key.reject match='bad-*'

# 查看 Master 生效的配置
sudo salt-run config.values

# 管理 job 缓存
sudo salt-run jobs.list_jobs
sudo salt-run jobs.active
```

> ⚠️ `salt-key -A`（接受全部）在自动化脚本里很方便，但**任何能连到 4505/4506 端口的机器都能请求密钥**。生产环境应该"先审核指纹再接受"，或用 Reactor 配合白名单自动签发。

### Salt Syndic（分布式 Master）

机器上千台、跨机房时，一个 Master 会扛不住。Syndic 让多台"下级 Master"汇聚到一台"顶级 Master"：

```mermaid
graph TB
    M["Top Master<br/>（全局视角）"] --> S1["Syndic<br/>机房 A"]
    M --> S2["Syndic<br/>机房 B"]
    S1 --> N1["Minion ×M"]
    S2 --> N2["Minion ×N"]
```

```yaml
# 在 Syndic 主机上：既要跑一个 Master 进程，又要跑 salt-syndic 连接上级
# /etc/salt/master（Syndic 主机）
syndic_master: 192.168.1.100
syndic_master_port: 4506
order_masters: True     # 允许上级 Master 通过本 Syndic 下发命令
```

```bash
# Syndic 主机上启用两个服务
sudo systemctl enable --now salt-master salt-syndic

# 在顶级 Master 上就能看到所有下级机器
sudo salt '*' test.ping
```

### SaltSSH（无 Agent 模式）

不想装 Minion？用 SSH 也能跑 Salt，做法和 Ansible 很像：

```yaml
# /etc/salt/roster —— 主机清单（支持正则/分组）
web1:
  host: 192.168.1.101
  user: ubuntu
  sudo: True
  # priv: /path/to/id_ed25519  # 指定私钥
```

```bash
# 安装（salt-ssh 是独立的包）
sudo dnf install -y salt-ssh

# 先测连通性
sudo salt-ssh '*' test.ping

# 执行 State / 命令
sudo salt-ssh 'web*' state.apply nginx
sudo salt-ssh 'web*' cmd.run 'uptime'
```

> 💡 四种"到达目标机"的方式对比：
>
> | 方式 | 需要 Agent | 速度 | 适用 |
> |------|-----------|------|------|
> | Salt Minion | 需要 | 毫秒级（ZeroMQ 长连接） | 长期管理的大规模机器 |
> | SaltSSH | 不需要 | 秒级（每次新建 SSH） | 临时、少量、不方便装 Agent |
> | Salt Masterless | 不需要 Master | 本地执行 | 镜像初始化、隔离网络 |
> | Ansible | 不需要 | 秒级 | 大多数场景 |

## 62.2 Puppet

### Puppet 简介

Puppet 是老牌的配置管理工具，采用声明式 DSL，有完善的企业版。

```mermaid
graph LR
    A[Puppet Master] -->|HTTPS| B[Puppet Agent 1]
    A -->|HTTPS| C[Puppet Agent 2]
    A -->|HTTPS| D[Puppet Agent N]
```

| 特性 | 说明 |
|------|------|
| 语言 | 自定义 DSL（Ruby 风格） |
| 工作模式 | Pull（Agent 拉取） |
| 配置 | 声明式（描述最终状态） |
| 幂等性 | 原生支持 |
| 企业版 | Puppet Enterprise，商业版，提供 Web 控制台与 RBAC |
| 现状 | 开源版仍在维护；新人上手成本高于 Ansible |

### Puppet 安装

```bash
# 说明：Puppet 7 已进入维护末期，新部署建议直接用 Puppet 8。
#       官方的 puppet7-release-el-7 仓库对应的是已经 EOL 的 CentOS 7，
#       新环境请选 el-8 / el-9 的仓库包。

# RHEL / Rocky / Alma 9：先装官方仓库
sudo dnf install -y https://yum.puppet.com/puppet8-release-el-9.noarch.rpm

# 在 Master（puppetserver 角色）上安装
sudo dnf install -y puppetserver
sudo systemctl enable --now puppetserver

# 在 Agent 上安装
sudo dnf install -y puppet-agent

# 检查服务与端口（Master 默认监听 8140）
systemctl status puppetserver --no-pager
sudo ss -lntp | grep 8140
```

> ⚠️ 如果 Master 端的 `puppetserver` 起不来，八成是**内存不够**（默认 JVM 堆 2GB 起）。小内存测试机可以调小：
>
> ```bash
> sudo sed -i 's/^JAVA_ARGS=.*/JAVA_ARGS="-Xms512m -Xmx512m"/' /etc/sysconfig/puppetserver
> sudo systemctl restart puppetserver
> ```

```bash
# Agent 侧需要能解析并连通 Master（防火墙放行 8140/tcp）
sudo firewall-cmd --permanent --add-port=8140/tcp && sudo firewall-cmd --reload
```

### Puppet Agent 配置

```bash
# /etc/puppetlabs/puppet/puppet.conf
[main]
server = puppet.example.com
certname = web-server-1.example.com

[agent]
# 每 30 分钟自动拉取一次配置（1800 秒）；调试时可临时设成 60
runinterval = 1800

# 首次连接需要让 Master 签发证书（Agent 会先提交 CSR 等待批准）
sudo systemctl enable --now puppet
# 在 Master 上查看待签发列表并批准
# sudo puppetserver ca list --all
# sudo puppetserver ca sign --certname web-server-1.example.com

# 手动触发一次（首次跑会先完成证书交换，可能会失败一次，再跑一次即可）
sudo puppet agent --test
```

> 💡 Puppet 的信任模型是"**每个 Agent 都要有自己的证书**"。Agent 第一次运行时生成密钥和证书请求（CSR），Master 签发后双方才能通信。批量部署时可以用 `--autosign`（自动签发）配合受限的命名规则，别把自动签发范围开得太大。

### Puppet Manifest

```puppet
# 示例：安装 Nginx
# /etc/puppetlabs/code/environments/production/manifests/nginx.pp

class nginx {
  # 安装包
  package { 'nginx':
    ensure => installed,
  }

  # 配置文件
  file { '/etc/nginx/nginx.conf':
    ensure  => file,
    source  => 'puppet:///modules/nginx/nginx.conf',
    require => Package['nginx'],
  }

  # 服务
  service { 'nginx':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    subscribe  => File['/etc/nginx/nginx.conf'],
  }
}

# 应用类
include nginx
```

> ⚠️ 上面把"定义类"和"应用类"写在了同一个文件里，只有教学时才这样写。真实项目中两者是分开的：
>
> - **类定义**放在模块里：`.../environments/production/modules/nginx/manifests/init.pp`
> - **节点分类**（哪台机器应用哪些类）放在 `manifests/site.pp` 里：
>
> ```puppet
> # manifests/site.pp
> node 'web-server-1.example.com' {
>   include nginx
> }
>
> node /^web-\d+\.example\.com$/ {     # 也支持正则匹配一组机器
>   include nginx
>   include app
> }
> ```

**资源之间的四种关系**，是读懂 Puppet 代码的关键：

| 关系 | 写法 | 含义 |
|------|------|------|
| 之前 | `before => Package['nginx']` | 我先执行，再执行你 |
| 之后 | `require => Package['nginx']` | 你先执行，再执行我 |
| 通知 | `notify => Service['nginx']` | 我变化时通知你，触发你 refresh |
| 订阅 | `subscribe => File['/etc/nginx/nginx.conf']` | 你变化时触发我（与 notify 方向相反） |

> 💡 区别只有一点：**`require` 只管顺序；`notify` / `subscribe` 还会在依赖项"发生变化"时额外触发一次 refresh**——这正是"配置改了才重启服务"的实现方式。

### Puppet 资源类型

```puppet
# 包资源
package { 'vim':
  ensure => installed,
}

# 文件资源
file { '/tmp/test.txt':
  content => "Hello Puppet\n",
  mode    => '0644',
  owner   => 'root',
}

# 服务资源
service { 'sshd':
  ensure     => running,
  enable     => true,
  hasrestart => true,
}

# 用户资源
user { 'deploy':
  ensure     => present,
  shell      => '/bin/bash',
  home       => '/home/deploy',
  managehome => true,
}

# cron 资源
cron { 'backup':
  command => '/scripts/backup.sh',
  hour    => 2,
  minute  => 0,
  ensure  => present,
}
```

### Puppet 类和模块

```puppet
# /etc/puppetlabs/code/environments/production/modules/mysql/manifests/init.pp
class mysql {
  package { 'mysql-server':
    ensure => installed,
  }

  service { 'mysqld':
    ensure => running,
    enable => true,
  }

  file { '/etc/my.cnf':
    source => 'puppet:///modules/mysql/my.cnf',
    notify => Service['mysqld'],
  }
}
```

### Puppet Hiera

```yaml
# Hiera 数据（分层配置）
# /etc/puppetlabs/code/environments/production/hieradata/common.yaml
---
ntp::servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org

# /etc/puppetlabs/code/environments/production/hieradata/production.yaml
---
ntp::servers:
  - time1.example.com
  - time2.example.com
```

Hiera 的"分层"思想：**同名数据可以写在多个文件里，越具体的越优先**（`production.yaml` 覆盖 `common.yaml`），不用复制粘贴整份配置。

```yaml
# /etc/puppetlabs/code/environments/production/hiera.yaml
version: 5
hierarchy:
  - name: "按节点"
    path: "nodes/%{trusted.certname}.yaml"
  - name: "按环境"
    path: "%{environment}.yaml"
  - name: "公共默认值"
    path: "common.yaml"
```

```puppet
# 类定义：给参数设默认值（Hiera 会自动填充）
class ntp (
  Array[String] $servers = ['0.pool.ntp.org'],
) {
  # ...
}

# 使用：不用手工传参，Hiera 会按 ntp::servers 这个键自动查找
include ntp
```

> ⚠️ 网上大量老教程还在用 `hiera('key')` 这种函数调用。那属于 **Hiera 3 的写法**，Hiera 5（Puppet 5 起）已改为**自动参数查找**：类参数叫 `$servers`，Hiera 就去找 `ntp::servers`。需要显式取数时用 `lookup('ntp::servers')`。

### Puppet 环境

```bash
# /etc/puppetlabs/puppet/puppet.conf（Master 的 [master] 段）
environmentpath = /etc/puppetlabs/code/environments
# 代码不在本机、从 Git 拉取时还会配置：
#   environment_timeout = 0        # 每次编译都重新读取代码（开发环境方便）
#   code = /etc/puppetlabs/code    # Puppet 8 新的代码目录声明

# 创建环境
mkdir -p /etc/puppetlabs/code/environments/production/{manifests,modules}
mkdir -p /etc/puppetlabs/code/environments/staging/{manifests,modules}

# 指定环境运行
puppet agent --test --environment staging

# 在 Master 上远程触发某台 Agent 立即拉取（不用等 runinterval）
sudo puppetserver ca list --all
sudo puppet kick web-server-1.example.com
```

> 💡 典型工作流：**开发分支对应 `staging` 环境，主分支对应 `production`**。代码先进 staging 验证，再合并到 production，这样"配置变更"也能像代码一样走 review 流程。用 r10k 或 Code Manager 可以把"Git 分支 → 环境目录"这一步自动化。

## 62.3 Chef 简介

Chef 是另一个老牌的配置管理工具，与 Puppet 齐名。

### Chef vs 其他工具

```mermaid
graph LR
    A[Chef Server] -->|HTTPS| B[Chef Client 1]
    A -->|HTTPS| C[Chef Client 2]
    A -->|HTTPS| D[Chef Client N]
    
    E[开发者] -->|上传| A
    F[Workstation] -->|knife| A
```

| 特性 | Chef | Puppet | Ansible |
|------|------|--------|---------|
| 配置语言 | Ruby DSL | 自定义 DSL | YAML |
| 服务器 | 可用 Chef Infra Server，也可 `chef-client -z` 本地模式 | Master 可选（`puppet apply` 可单机） | 无中心服务（AWX 只是 Web 界面） |
| Agent | Chef Client | Puppet Agent | 无或 SSH |
| 难度 | 较高 | 中高 | 较低 |
| 现状 | 开源版仍在维护，学习成本高 | 开源版仍在维护 | 生态最活跃 |

### Chef 核心概念

| 概念 | 说明 |
|------|------|
| Recipe | 食谱，描述如何配置一个组件 |
| Cookbook | 食谱书，包含多个 Recipe |
| Resource | 资源类型（package、file、service） |
| Attribute | 属性，节点的特征 |
| Template | 模板，配置文件模板 |
| Role | 角色，一组 Recipe 和属性 |
| Environment | 环境（dev、staging、prod） |

### Chef 安装

```bash
# ⚠️ 老教程里的 "Chef DK（Development Kit）" 早已停止维护，
#    现在用的是 Chef Workstation（开发机）和 Chef Infra Client（被管理机）。

# 安装 Chef Workstation（Linux；macOS 也可以 brew install --cask chef-workstation）
curl -L https://omnitruck.chef.io/install.sh | sudo bash -s -- -P chef-workstation -c stable

# 被管理节点只需要客户端
# curl -L https://omnitruck.chef.io/install.sh | sudo bash -s -- -P chef -c stable

# ⚠️ Chef 从 15 起要求显式接受许可协议，否则命令直接拒绝执行
export CHEF_LICENSE=accept-no-persist     # 也可写进 /etc/chef/client.rb 的 license 配置
# 想确认版本与许可状态：
chef --version
chef-client --version
```

> 💡 `chef --version` 是新版 Workstation 提供的统一入口（可以看 `chef -h` 列出 cookbook 相关子命令）；`chef-client` 才是真正干活的客户端。两者版本号可能不同，别混。

### Chef 基础配置

```bash
# 初始化 Chef 工作目录（生成一个标准的 chef-repo 骨架）
mkdir chef-repo && cd chef-repo
chef generate repo .

# 创建一个 cookbook
chef generate cookbook cookbooks/mycookbook
```

```text
chef-repo/
├── cookbooks/
│   └── mycookbook/
│       ├── recipes/
│       │   └── default.rb      # 默认入口：一个 Recipe 就是一个 Ruby 文件
│       ├── attributes/
│       │   └── default.rb      # cookbook 的默认属性值
│       ├── templates/
│       │   └── nginx.conf.erb  # ERB 模板
│       ├── files/
│       │   └── default/        # 直接分发的静态文件
│       ├── test/               # 集成测试（InSpec）
│       └── metadata.rb         # 名称、版本、依赖
├── roles/
└── environments/
```

> 💡 Chef 里有两个"默认文件"容易搞混：`recipes/default.rb` 是**入口 Recipe**（`recipe[mycookbook]` 默认就跑它），`attributes/default.rb` 是**默认属性**（优先级最低，可被 role / environment / node 覆盖——和 Ansible 里 `defaults/` 的定位很像）。

### Chef Recipe 示例

```ruby
# recipes/default.rb

# 安装 Nginx
package 'nginx' do
  action :install
end

# 启动服务
service 'nginx' do
  action [:enable, :start]
end

# 复制配置
template '/etc/nginx/nginx.conf' do
  source 'nginx.conf.erb'
  owner 'root'
  group 'root'
  mode '0644'
  notifies :restart, 'service[nginx]'
end

# 创建网站目录
directory '/var/www/myapp' do
  owner 'www-data'
  group 'www-data'
  mode '0755'
  action :create
end
```

Chef Recipe 的写法是纯 Ruby：**`资源类型 '资源名' do ... end`**，块里写属性，`action` 声明要做什么。几个要点：

- **不写 `action` 时用默认动作**：`package` 默认 `:install`、`service` 默认 `:enable` 和 `:start`、`file` 默认 `:create`。所以上面的"安装 Nginx"和"启动服务"两段都没写 `action`。
- **`notifies :restart, 'service[nginx]'`** 就是 Puppet 里 `notify` 的等价物——**模板内容变化时才重启服务**，没变化就不动。这是幂等的关键。
- 资源名（如 `'nginx'`）既是"名字"也是"默认的目标标识"，`service 'nginx'` 会去找名为 nginx 的服务。

和 Puppet 一样，Chef 的资源之间也有"顺序与通知"两套语义：

| 写法 | 作用 |
|------|------|
| `notifies :restart, 'service[nginx]'` | 我发生变化时，通知对方执行动作 |
| `subscribes :reload, 'template[/etc/nginx/nginx.conf]'` | 对方变化时，我执行动作 |
| `action :nothing` | 该资源只被通知时才运行 |
| `not_if` / `only_if` | 满足条件才执行（命令类资源防重复执行的关键） |

> 💡 `not_if` / `only_if` 是 Chef 里最该早点学会的两个属性。写 `execute '初始化数据库'` 这类命令资源时，没有它们就会**每次跑都执行一遍**，破坏幂等。

### Chef 资源类型

```ruby
# package 资源
package 'vim' do
  action :install
end

# service 资源
service 'nginx' do
  action [:enable, :start]
end

# file 资源
file '/tmp/test.txt' do
  content 'Hello Chef!'
  mode '0644'
  owner 'root'
end

# directory 资源
directory '/opt/myapp' do
  owner 'app'
  group 'app'
  mode '0755'
  recursive true
end

# user 资源
user 'deploy' do
  shell '/bin/bash'
  home '/home/deploy'
  manage_home true
end

# cron 资源
cron 'backup' do
  hour '2'
  minute '0'
  command '/scripts/backup.sh'
end
```

### Chef 模板

```erb
# templates/default/nginx.conf.erb
user <%= @nginx_user %>;
worker_processes <%= @worker_processes %>;
pid /run/nginx.pid;

events {
    worker_connections <%= @max_connections %>;
}

http {
    include /etc/nginx/mime.types;
    
    server {
        listen <%= @port %>;
        server_name <%= @server_name %>;
        
        location / {
            root <%= @document_root %>;
        }
    }
}
```

### Chef 角色

```ruby
# roles/webserver.rb
name 'webserver'
description 'Web Server Role'
run_list 'recipe[nginx]', 'recipe[myapp]'

default_attributes({
  'nginx' => {
    'port' => 80,
    'worker_processes' => 4
  }
})

override_attributes({
  'myapp' => {
    'environment' => 'production'
  }
})
```

### Chef 执行

```bash
# 本地模式（不需要 Server）：-z 就是 --local-mode 的简写
cd chef-repo
chef-client -z -r 'recipe[mycookbook]'

# 只跑指定 Recipe，并看详细输出
chef-client -z -r 'recipe[mycookbook::default]' --chef-license accept

# 演练：只报告将要做什么，不真正执行
chef-client -z -r 'recipe[mycookbook]' --why-run

# 有 Server 时：用 knife 上传 cookbook / 管理节点
knife cookbook upload mycookbook        # 上传到 Chef Infra Server
knife node list                         # 列出已注册节点
knife node run_list set web1 'recipe[mycookbook]'
knife role from file roles/webserver.rb
```

> ⚠️ 这些 `knife` 命令都需要**已配置好的 `knife.rb` 与客户端证书**（`.chef/` 目录），否则会直接报认证失败。新手最常见的卡点就是"命令会背了，但没上传过证书"。

### Chef Solo（历史写法，已被本地模式取代）

> ⚠️ `chef-solo` 这个命令**在 Chef 13 起就被移除**了。老教程里出现的它，现在请一律替换成 `chef-client -z`。

```bash
# 老写法（已不可用）：
# chef-solo -c /etc/chef/solo.rb
```

```bash
# 现代等价写法：本地模式 + 指定 cookbook 路径和节点属性文件
mkdir -p /etc/chef
cat > /etc/chef/client.rb << 'EOF'
cookbook_path '/srv/chef/cookbooks'
file_cache_path '/var/cache/chef'
node_path '/srv/chef/nodes'
Chef::Config[:license_acceptance] = true
EOF

chef-client -z -c /etc/chef/client.rb -j /etc/chef/node.json
```

---

## 62.4 Terraform 基础设施即代码

Terraform 是 HashiCorp 出品的"基础设施编排器"，专注于云资源管理。

> 📌 **本节只做入门速览**。Terraform 的完整内容（Provider、变量、模块、State、远端后端、CI 集成、密钥管理）在《云计算》卷的 **第 68 章 IaC** 里有系统讲解，需要实际用时建议直接读那一章。

### Terraform vs 其他工具

| 工具 | Terraform | Ansible | Chef |
|------|-----------|---------|------|
| 定位 | 基础设施 | 配置管理 | 配置管理 |
| 语言 | HCL | YAML | Ruby |
| 状态 | 有状态 | 无状态 | 无状态 |
| 用途 | 创建/销毁云资源 | 配置已有服务器 | 配置已有服务器 |

```mermaid
graph LR
    A[Terraform] --> B[AWS]
    A --> C[Azure]
    A --> D[GCP]
    A --> E[本地/其他]
```

### Terraform 安装

```bash
# macOS
brew install terraform

# Linux（推荐配官方软件源，方便升级；也可用 tfenv 管理版本）
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install -y terraform

# 验证
terraform version
```

### Terraform 基本配置

```hcl
# main.tf

# 指定 Provider 与版本约束（版本一定要锁，否则某天 Provider 升级会把资源改成"要重建"）
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  # 凭证不要写在这里：用环境变量、aws configure 或运行时角色
}

# 动态查询最新 AMI，避免写死会过期的 ami-xxxx
data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

# 创建资源
resource "aws_instance" "web" {
  ami           = data.aws_ami.al2023.id
  instance_type = "t3.micro"
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  
  tags = {
    Name        = "web-server"
    Environment = "production"
  }
}

# 创建安全组
resource "aws_security_group" "web_sg" {
  name = "web-security-group"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

> ⚠️ 安全组里**不要顺手放行 22 端口给 `0.0.0.0/0`**。SSH 应该只允许自己的出口 IP（`203.0.113.10/32`），或干脆走 SSM Session Manager / 跳板机。

### Terraform 命令

```bash
# 初始化
terraform init

# 格式化代码
terraform fmt

# 验证配置
terraform validate

# 预览执行计划
terraform plan -out=tfplan

# 应用更改（执行刚刚审核过的那份计划）
terraform apply tfplan

# 交互确认模式（会先展示计划再问 yes/no）
terraform apply

# 查看当前状态
terraform show

# 列出资源
terraform state list

# 销毁资源
terraform destroy

# 输出
terraform output
```

> ⚠️ 三条命令层面的硬规矩：
> 1. **先 plan 再 apply**，别直接 `apply` 赌运气。
> 2. **`terraform.tfstate` 千万不要进 Git**，里面明文存着资源属性和敏感值；团队协作要配远程后端（S3 + DynamoDB 锁，或 OSS + TableStore）。
> 3. **`terraform destroy` 会删掉配置里的所有资源**，执行前务必 `plan -destroy` 看清对象。

### Terraform 变量和输出

```hcl
# variables.tf
variable "instance_type" {
  description = "EC2 实例类型"
  type        = string
  default     = "t3.micro"
}

variable "environment" {
  description = "环境名称"
  type        = string
  default     = "production"
}

# 敏感变量：不写默认值，运行时用 TF_VAR_db_password 注入
variable "db_password" {
  description = "数据库密码"
  type        = string
  sensitive   = true
}

# outputs.tf
output "instance_ip" {
  description = "实例公网 IP"
  value       = aws_instance.web.public_ip
}

output "instance_id" {
  description = "实例 ID"
  value       = aws_instance.web.id
}

# 敏感输出会被日志打码，但依然存在于 state 里
output "db_connection" {
  description = "数据库连接串"
  value       = "postgres://app:${var.db_password}@db.example.com:5432/app"
  sensitive   = true
}
```

### Terraform 模块

```hcl
# modules/vpc/main.tf
module "vpc" {
  source = "./modules/vpc"
  
  cidr_block = "10.0.0.0/16"
  environment = var.environment
}
```

> 💡 模块的 `source` 可以是本地路径、Git 仓库或 Terraform Registry。生产使用第三方模块时**一定要锁版本**（`version = "5.1.2"`），否则上游一改，你的下次 apply 就可能重建整套网络。

---

## 62.5 工具对比总结

| 工具 | Ansible | SaltStack | Puppet | Chef | Terraform |
|------|---------|-----------|--------|------|-----------|
| 架构 | 无 Agent，Push（SSH） | Master-Minion（ZeroMQ） | Master-Agent，Pull | Server-Agent，Pull | 无 Agent，直连云 API |
| 配置语言 | YAML | YAML + Python | 自定义 DSL | Ruby DSL | HCL |
| 执行速度 | 快 | 非常快（长连接） | 中等（默认 30 分钟一轮） | 中等（默认一小时一轮） | 取决于云 API |
| 学习曲线 | 低 | 中 | 中高 | 高 | 中 |
| 敏感数据 | ansible-vault | Pillar（可配 GPG） | Hiera + eyaml | Encrypted Data Bag | 变量 + 云 KMS |
| 社区/生态 | 最活跃 | 活跃 | 成熟但趋缓 | 成熟但趋缓 | 非常活跃 |
| 企业版 | AWX / Red Hat AAP | SaltStack Enterprise | Puppet Enterprise | Chef Automate | Terraform Cloud/Enterprise |
| 适用场景 | 通用配置管理 | 大规模、需要实时响应 | 大型企业、强合规 | 已用 Ruby 生态的团队 | 创建/销毁云资源 |

> 💡 关键认知：**Terraform 和其余四个不是替代关系**。Terraform 负责"把机器和网络造出来"（Provisioning），Ansible/Salt/Puppet/Chef 负责"把机器配置成想要的样子"（Configuration Management）。它们是接力关系，不是竞品。

### 工具选择决策树

```mermaid
flowchart TD
    A["开始选择工具"] --> B{"要做什么？"}
    B -->|"创建/销毁云资源"| T["Terraform"]
    B -->|"配置已存在的机器"| C{"规模有多大？"}

    C -->|"几十台以内"| D{"团队更熟悉什么？"}
    C -->|"数百台以上"| E{"需要秒级实时响应吗？"}

    D -->|"YAML / 不想装 Agent"| F["Ansible"]
    D -->|"Python / 想用长连接"| G["SaltStack"]
    D -->|"已有 Ruby 技术栈"| H["Chef"]

    E -->|"需要"| G
    E -->|"不需要"| F

    F --> I{"需要 Web 界面和权限控制？"}
    I -->|"需要"| J["AWX / Red Hat AAP"]
    I -->|"不需要"| K["直接命令行 + Git 就够了"]

    T --> L["再用 Ansible/Salt 做配置"]
    F --> L
    G --> L
```

> ⚠️ 这张图是"入门建议"，不是铁律。**团队已有的技术栈和运维习惯，权重往往高于工具本身的优劣**——用一个团队不熟的"更先进"工具，事故率会比用熟悉的工具高得多。

### 实际生产环境推荐

| 场景 | 推荐工具 | 原因 |
|------|---------|------|
| 小团队，快速起步 | Ansible | 上手快，文档丰富 |
| 100+服务器，追求速度 | SaltStack | ZeroMQ 超快 |
| 大型企业，成熟流程 | Puppet | 10+年企业级方案 |
| 混合云基础设施 | Terraform + Ansible | 各司其职 |
| 容器环境 | Ansible + kubectl | 与 K8s 完美结合 |

## 62.6 常见问题排查

这几个工具"装得上、跑不通"的坑高度相似，集中列一下：

| 现象 | 常见原因 | 排查方向 |
|------|----------|----------|
| Salt 的 `test.ping` 一直没响应 | 未接受密钥 / 4505-4506 被防火墙挡住 | `salt-key -L`；`firewall-cmd --list-ports`；Minion 上 `systemctl status salt-minion` |
| Salt Minion 显示 `Minion did not return` | Minion ID 重复（克隆的机器主机名相同） | 检查 `id:` 与 `SALT_MINION_ID`；删除重复机器的密钥后重连 |
| Salt State 报"ID 重复/结构错误" | 一个 ID 下写了两个 State 声明 | 拆成两个 ID，用 `watch_in` / `require` 关联 |
| Puppet Agent 报证书错误 | CSR 未签发 / certname 变更 | Master 上 `puppetserver ca list --all` 后签发；改过主机名要清理旧证书 |
| Puppet `puppetserver` 起不来 | JVM 内存不足 / 端口 8140 被占用 | `journalctl -u puppetserver`；调小 `JAVA_ARGS` |
| Chef 命令提示 license 未接受 | Chef 15+ 强制接受许可 | `export CHEF_LICENSE=accept-no-persist` |
| Chef 找不到 cookbook | 不在 chef-repo 目录 / `cookbook_path` 没配 | `chef-client -z -r 'recipe[x]'` 时先 `cd chef-repo` |
| Hiera / 属性值"设了不生效" | 优先级被更高层级覆盖 | Puppet 用 `puppet lookup <key> --explain`；Chef 用 `ohai`/节点属性优先级排查 |
| 脚本能跑但每次都是 changed | 用了命令类资源（`cmd.run` / `execute`） | Salt 加 `onlyif`/`unless`，Chef 加 `not_if`/`only_if`，Puppet 用 `exec` 的 `creates` |

**通用的排查顺序**（对四个配置管理工具都适用）：

1. **服务/连接层**：进程在不在、端口通不通、时间是否同步（证书和密钥对时间敏感）。
2. **认证层**：Salt 密钥是否接受、Puppet 证书是否签发、Chef 证书是否上传。
3. **代码层**：语法是否合法（`test=True` / `--noop` / `--why-run` 空跑）。
4. **数据层**：变量/属性/ Hiera 优先级是否被覆盖。

```bash
# 三个工具的"空跑"对照，改动前先预演一遍
sudo salt '*' state.highstate test=True          # Salt
sudo puppet agent --test --noop                  # Puppet
chef-client -z -r 'recipe[mycookbook]' --why-run # Chef
ansible-playbook site.yml --check --diff         # Ansible
```

## 本章小结

本章我们学习了其他自动化运维工具：

| 工具 | 核心特点 | 最适合 |
|------|----------|--------|
| SaltStack | ZeroMQ 长连接、状态快、有 Grains/Pillar/Reactor | 大规模机器、需要实时响应 |
| Puppet | 声明式 DSL、证书信任模型、Hiera 分层数据 | 大型企业、强合规场景 |
| Chef | Ruby DSL、Recipe/Cookbook、可用本地模式 | 已有 Ruby 技术栈的团队 |
| Terraform | HCL、有状态（tfstate）、直连云 API | 创建和销毁云基础设施 |

选型的三句话结论：

1. **想快速起步、团队没有特殊偏好 → Ansible**（现在最主流，生态最活跃）。
2. **机器上千台、要求秒级响应，或者需要"事件驱动"→ SaltStack**。
3. **基础设施用 Terraform 造，配置用 Ansible / Salt 管**——两者配合，而不是二选一。

---

> 💡 **温馨提示**：
> 工具选型没有标准答案。**团队已经熟悉什么、出了问题谁能修**，往往比"哪个工具更先进"更重要。
>
> 对绝大多数场景，Ansible + Terraform 的组合已经足够：一个负责配置，一个负责资源。

---

**第六十二章：其他自动化工具 — 完结！** 🎉

下一章我们将学习"负载均衡"，掌握 Nginx、HAProxy、LVS、云负载均衡等内容。敬请期待！ 🚀
