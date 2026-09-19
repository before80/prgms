+++
title = "第28章：定时任务"
weight = 280
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第二十八章：定时任务

你有没有过这种需求：
- 每天凌晨3点自动备份数据库
- 每周一早上9点发送周报
- 每个月1号清理一次过期文件

这些**定时自动执行的任务**，在Linux里叫**定时任务（Cron Job）**。

这一章，让我们学会给Linux安排"日程表"！

---

## 28.1 什么是定时任务？自动执行的任务

**定时任务**就是"到点就自动执行的任务"，不需要你手动触发。

想象一下：
- 你雇了一个保姆，每天早上8点自动给你做早餐——这就是**定时任务**
- 你设置了一个闹钟，每天早上7点响——这也是一种**定时任务**

在Linux里，最常用的定时任务工具是**cron**，它会在指定的时间自动运行你安排好的命令。

---

## 28.2 cron 定时任务：系统自带定时任务

### 28.2.1 cron 服务

**cron**是一个**守护进程**（服务），它一直在后台运行，每分钟检查一次是否有任务要执行。

```bash
# 检查cron服务状态
systemctl status cron

# 或者
systemctl status crond

# 输出大概是：
# ● cron.service - Regular background program processing daemon
#    Loaded: loaded (/lib/systemd/system/cron.service; enabled)
#    Active: active (running) since Mon 2026-03-23 10:00:00 CST; 2h 30min ago
```

### 28.2.2 crond 守护进程

cron的守护进程叫**crond**，它会：
1. 每分钟被唤醒一次
2. 检查任务调度表（crontab）
3. 执行到点的任务
4. 继续睡眠

```mermaid
graph LR
    A["crond守护进程"] --> B["每分钟检查一次"]
    B --> C["有任务到点？"]
    C --> D["执行任务"]
    C --> E["没有到点的任务"]
    D --> F["返回睡眠"]
    E --> F
    
    style A fill:#ff6b6b
    style D fill:#51cf66
```

---

## 28.3 crontab 命令：用户定时任务

### 28.3.1 crontab -e：编辑

```bash
# 编辑当前用户的crontab
crontab -e

# 第一次运行会让你选择编辑器
# 推荐选择nano（简单）或vim（功能强大）
# 选择后，以后都会用这个编辑器打开crontab

# 如果没有crontab，先安装
sudo apt install cron    # Debian/Ubuntu
sudo yum install cronie  # RHEL/CentOS
```

执行后会打开编辑器，每一行是一个定时任务，格式是：

```
分 时 日 月 周 命令
```

### 28.3.2 crontab -l：查看

```bash
# 查看当前用户的crontab
crontab -l

# 输出大概是：
# # m h dom mon dow command
# 0 3 * * * /usr/bin/backup.sh
# 30 9 * * 1 /usr/bin/send-report.sh
```

```bash
# 查看其他用户的crontab（需要root）
sudo crontab -u longx -l
```

### 28.3.3 crontab -r：删除

```bash
# 删除当前用户的所有crontab任务
crontab -r
```

```bash
# 想让它先问一句？加 -i（interactive）
crontab -i -r
# crontab: really delete longx's crontab? (y/n)
```

> 🚨 **`crontab -r` 是本章最危险的命令，没有之一**。它**不会问你任何问题**，敲下回车，当前用户的所有定时任务立刻消失，而且**没有回收站、无法撤销**。老资料里常见的 `crontab -r -f` 更是张冠李戴——`crontab` 根本没有 `-f` 选项，`-f` 是 `rm` 的参数。
>
> 好习惯是：**改 crontab 之前先备份**。
>
> ```bash
> crontab -l > ~/crontab.backup.$(date +%F)   # 先备份
> crontab -e                                  # 再编辑
> crontab ~/crontab.backup.2026-03-23         # 出错时从备份恢复
> ```

### 28.3.4 crontab -u 用户：指定用户

```bash
# 编辑指定用户的crontab（需要root）
sudo crontab -u longx -e

# 查看指定用户的crontab
sudo crontab -u longx -l
```

---

## 28.4 cron 表达式

cron表达式就是定时任务的"时间表"，告诉cron什么时候执行任务。

### 28.4.1 * * * * *：分 时 日 月 周

```bash
# cron表达式格式：
# ┌───────────── 分钟 (0-59)
# │ ┌───────────── 小时 (0-23)
# │ │ ┌───────────── 日 (1-31)
# │ │ │ ┌───────────── 月 (1-12)
# │ │ │ │ ┌───────────── 星期 (0-7, 0和7都是周日)
# │ │ │ │ │
# * * * * * command
```

| 字段 | 范围 | 特殊字符 |
|------|------|----------|
| 分钟 | 0-59 | * , - / |
| 小时 | 0-23 | * , - / |
| 日 | 1-31 | * , - / |
| 月 | 1-12 | * , - / |
| 周 | 0-7 | * , - / |

**特殊字符**：
- `*`（星号）：代表"每一"（每分钟、每小时、每天等）
- `,`（逗号）：列表，如`1,3,5`表示1点、3点、5点
- `-`（减号）：范围，如`1-5`表示1点到5点
- `/`（斜杠）：间隔，如`*/5`表示每5个单位

### 28.4.2 0 * * * *：每小时

```bash
# 每小时的第0分钟执行（比如1:00、2:00、3:00...）
0 * * * * /usr/bin/backup-hourly.sh
```

### 28.4.3 0 0 * * *：每天

```bash
# 每天午夜0点执行（也就是"每天"）
0 0 * * * /usr/bin/daily-backup.sh

# 每天早上8点执行
0 8 * * * /usr/bin/morning-task.sh
```

### 28.4.4 0 0 * * 0：每周

```bash
# 每周日（周日是0或7）午夜执行
0 0 * * 0 /usr/bin/weekly-cleanup.sh

# 每周一早上9点执行
0 9 * * 1 /usr/bin/send-weekly-report.sh

# 工作日每天执行
0 9 * * 1-5 /usr/bin/workday-task.sh
```

### 28.4.5 0 0 1 * *：每月

```bash
# 每月1号午夜执行
0 0 1 * * /usr/bin/monthly-report.sh

# 每月15号下午3点执行
0 15 15 * * /usr/bin/mid-month-task.sh

# 每季度第一天执行
0 0 1 1,4,7,10 * /usr/bin/quarterly-task.sh
```

### 📊 cron表达式速查表

```mermaid
graph LR
    A["0 3 * * *"] --> A2["每天凌晨 3:00"]
    B["0 9 * * 1-5"] --> B2["工作日早上 9:00"]
    C["0 0 1 * *"] --> C2["每月 1 号 0:00"]
    D["*/5 * * * *"] --> D2["每 5 分钟一次"]
    E["30 4 1,15 * *"] --> E2["每月 1 号和 15 号的 4:30"]

    style A fill:#ff6b6b,color:#fff
    style B fill:#4ecdc4,color:#000
    style C fill:#45b7d1,color:#fff
    style D fill:#51cf66,color:#000
    style E fill:#ffd43b,color:#000
```

| 表达式 | 含义 |
|--------|------|
| `* * * * *` | 每分钟 |
| `0 * * * *` | 每小时 |
| `0 0 * * *` | 每天午夜 |
| `0 9 * * 1-5` | 工作日早上9点 |
| `0 0 * * 0` | 每周日 |
| `0 0 1 * *` | 每月1号 |
| `*/15 * * * *` | 每15分钟 |
| `0 */2 * * *` | 每2小时 |
| `30 4 1,15 * *` | 每月1号和15号凌晨4:30 |

---

## 28.5 系统定时任务：/etc/cron.d/

除了用户crontab，Linux还有**系统级**的定时任务目录。

```bash
# 查看系统cron.d目录
ls -la /etc/cron.d/

# 输出：
# total 16
# drwxr-xr-x  2 root root 4096 Mar 23 10:00 .
# drwxr-xr-x 10 root root 4096 Mar 23 10:00 ..
# -rw-r--r-- 1 root root  220 Mar 23 10:00 anacron
# -rw-r--r--  1 root root  395 Mar 23 10:00 sysstat
```

```bash
# 系统cron.d文件的格式和用户crontab稍有不同
# 多了一个用户名字段
cat /etc/cron.d/sysstat

# 输出：
# # Run system activity accounting tool every 10 minutes
# */10 * * * * root cd /usr/lib/sa && /usr/lib/sa/sa1 1 1
```

---

## 28.6 系统定时目录

Linux预定义了几个**定时目录**，方便你放置脚本。

### 28.6.1 /etc/cron.daily/：每天

```bash
# 每天凌晨会自动执行这个目录里的脚本
# 通常是凌晨3点到6点之间随机执行
ls /etc/cron.daily/

# 输出：
# apt-compat  man-db  systemd-logrotate
# 如果你想让自己的脚本每天执行，放到这！
```

```bash
# 创建一个每天执行的脚本
sudo bash -c 'cat > /etc/cron.daily/my-daily-task.sh << EOF
#!/bin/bash
# 每天早上7点执行的任务
echo "每天早上好！" >> /var/log/daily.log
EOF'

sudo chmod +x /etc/cron.daily/my-daily-task.sh
```

### 28.6.2 /etc/cron.hourly/：每小时

```bash
# 每小时执行这个目录里的脚本
ls /etc/cron.hourly/
```

### 28.6.3 /etc/cron.weekly/：每周

```bash
# 每周执行这个目录里的脚本
ls /etc/cron.weekly/
```

### 28.6.4 /etc/cron.monthly/：每月

```bash
# 每月执行这个目录里的脚本
ls /etc/cron.monthly/
```

> [!NOTE]
> 这些目录里的脚本需要是**可执行的**（chmod +x），并且要有shebang（`#!/bin/bash`）。

---

## 28.7 at 命令：延时执行一次任务

**at**是用来执行**一次性任务**的，和cron的"重复执行"不同。

### 28.7.1 at 时间：安排任务

```bash
# 安装at（如果没有）
sudo apt install at

# 启动at服务
sudo systemctl enable --now atd

# 安排一个任务，3分钟后执行
at now + 3 minutes

# 进入at交互界面
# at> echo "Hello from at!" >> /tmp/at-test.log
# at> 按Ctrl+D保存
```

```bash
# at支持的时间格式很灵活
at 14:30           # 今天下午2:30
at 14:30 today      # 今天下午2:30
at 14:30 tomorrow   # 明天下午2:30（14:30 就是 24 小时制的下午 2 点半）
at noon             # 中午12:00
at midnight          # 午夜
at now + 1 hour     # 1小时后
at now + 3 days     # 3天后的这个时间
at 3pm + 2 days     # 2天后下午3点
```

### 28.7.2 at -l：查看

```bash
# 查看待执行的at任务
at -l

# 输出：
# 1   Mon Mar 23 15:30:00 2026 a longx
# 2   Tue Mar 24 10:00:00 2026 a longx
```

### 28.7.3 atrm 编号：删除

```bash
# 删除编号为1的at任务
atrm 1

# 查看确认
at -l
```

---

## 28.8 anacron 非实时定时

**anacron**是用来执行**非实时定时任务**的工具。

cron的问题是：如果电脑在任务该执行的时候关机了，cron不会补上这个任务。**anacron**就是来解决这个问题的。

```bash
# anacron的特点：
# 1. 如果任务该执行时电脑关机了，开机后会补上
# 2. 不要求精确的时间，只保证"每天/每周/每月至少执行一次"

# 查看anacron配置
cat /etc/anacrontab

# 输出：
# # /etc/anacrontab: configuration file for anacron
# SHELL=/bin/sh
# PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# 1       5       cron.daily       run-parts /etc/cron.daily
# 7       10      cron.weekly      run-parts /etc/cron.weekly
# @monthly 15      cron.monthly    run-parts /etc/cron.monthly
```

| 字段 | 含义 |
|------|------|
| 周期 | 多少天执行一次 |
| 延迟 | 开机后延迟多少分钟执行 |
| 任务标识 | 任务的名字 |
| 命令 | 要执行的命令 |

---

## 28.9 systemd timer：systemd 定时任务

除了cron，Systemd也有自己的定时任务功能——**systemd timer**。

### 28.9.1 .service 单元：定义"要做什么"

systemd 的定时任务由**两个文件配对**组成：`.service` 说明"干什么"，`.timer` 说明"什么时候干"。先写 service：

```bash
# 创建一个定时任务：每5分钟执行一次
# 1. 创建.service文件
sudo bash -c 'cat > /etc/systemd/system/my-timer-task.service << EOF
[Unit]
Description=My Timer Task Service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/my-task.sh
EOF'
```

### 28.9.2 .timer 单元：定义"什么时候做"

```bash
# 2. 创建.timer文件
sudo bash -c 'cat > /etc/systemd/system/my-timer.timer << EOF
[Unit]
Description=My Timer Timer
Requires=my-timer-task.service

[Timer]
OnBootSec=5min        # 启动5分钟后第一次执行
OnUnitActiveSec=5min   # 之后每5分钟执行一次
Unit=my-timer-task.service

[Install]
WantedBy=timers.target
EOF'
```

```bash
# 3. 启用定时器
sudo systemctl daemon-reload
sudo systemctl enable --now my-timer.timer

# 4. 查看定时器状态
systemctl list-timers

# 输出：
# NEXT                        LEFT     LAST                        PASSED  UNIT
# Mon 2026-03-23 15:05:00  4min 55s Mon 2026-03-23 15:00:00  4s     my-timer.timer
```

```bash
# 常用timer选项
[Timer]
OnBootSec=5min        # 开机5分钟后执行
OnUnitActiveSec=1hour  # 每小时执行一次
OnCalendar=*:0/5       # 每5分钟（和cron的 */5 一样）
OnCalendar=daily        # 每天
OnCalendar=weekly       # 每周
```

---

## 28.10 cron 的"经典翻车现场"

"脚本手动跑没问题，一放进 crontab 就不干活"——这是运维新手最常见的困扰。原因基本跑不出下面这几条。

### 28.10.1 环境变量不一样：PATH 是头号杀手

**cron 执行任务时用的是一套极简环境**，它不会读你的 `.bashrc`、`.profile`，`PATH` 通常只有 `/usr/bin:/bin`。所以你在终端里能跑的 `node`、`docker`、`python3`，到了 cron 里可能直接 "command not found"。

```bash
# ❌ 危险写法：依赖 PATH
yunying-task deploy

# ✅ 写法一：全部用绝对路径
/usr/local/bin/yunying-task deploy

# ✅ 写法二：在 crontab 顶部显式声明环境（crontab 支持这种"变量赋值行"）
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=me@example.com
```

> 调试技巧：如果怀疑是环境问题，先让 cron 把环境"打印"出来看看——
> ```bash
> * * * * * env > /tmp/cron-env.txt
> ```
> 一分钟后打开 `/tmp/cron-env.txt`，和你在终端里 `env` 的结果对比，差异一目了然。

### 28.10.2 命令里的 `%` 要转义

cron 把 `%` 当成特殊字符：**第一个未转义的 `%` 之后的内容会被当作"标准输入"**，而不是命令的一部分。所以带 `%` 的命令（比如 `date +%F`）必须写成 `\%`。

```bash
# ❌ 错误：后面的内容被当成 stdin
0 3 * * * tar -czf /backup/log-$(date +%F).tar.gz /var/log

# ✅ 正确：% 前面加反斜杠
0 3 * * * tar -czf /backup/log-$(date +\%F).tar.gz /var/log

# ✅ 更省心的写法：把逻辑放进脚本里，crontab 只负责调用脚本
0 3 * * * /usr/local/bin/backup-logs.sh
```

### 28.10.3 没有日志，等于盲飞

cron 默认会把命令的**标准输出和错误**通过邮件发给用户；如果机器没配邮件服务，这些输出就石沉大海。规范做法是**自己重定向到日志文件**：

```bash
# 把 stdout 和 stderr 都追加到日志（注意 2>&1 要在 >> 之后）
0 3 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1

# 什么都不想要？丢进黑洞（但强烈建议至少留 stderr）
0 3 * * * /usr/local/bin/backup.sh > /dev/null 2>&1
```

> 但要注意：日志文件会一直长大。**要么用 logrotate 管理它，要么在脚本里自己控制大小**，否则某天日志把磁盘写满，又是一场事故。

### 28.10.4 任务重叠：上一次还没跑完，下一次又开始了

如果任务耗时超过间隔（比如每 5 分钟一次，但脚本要跑 20 分钟），你会同时跑起好几个实例，互相抢资源、抢锁、写坏数据。用 `flock` 加把锁：

```bash
# -n 表示"拿不到锁就直接退出"，绝不排队堆积
*/5 * * * * /usr/bin/flock -n /tmp/backup.lock /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1
```

### 28.10.5 其他容易忽略的点

| 现象 | 原因 |
|------|------|
| 每月 31 号的任务有时不执行 | 2 月、4 月没有 31 号。写"每月最后一天"应该用 `28-31` 配合脚本内部判断 |
| 任务是"日"和"周"同时限定时行为诡异 | cron 对 `日` 和 `周` 两个字段的匹配是**"或"**关系（`5 4 1 * 1` 表示"每月 1 号**或**每周一"），不是"并且"。不确定就别同时写 |
| 整点任务全挤在一起 | 大量任务都写 `0 * * * *`，整点机器负载飙升。**错峰**一下，比如写成 `7 * * * *`、`23 * * * *` |
| 夏令时切换时任务重复/跳过 | 以系统时区为准。重要任务尽量避开切换时刻（凌晨 2~3 点） |
| 改完 crontab 不生效 | `crontab -e` 保存即生效，不需要重启服务；但如果改的是 `/etc/cron.d/` 下的文件，注意**文件末尾必须留一个空行**，否则最后一行任务会被忽略 |

> 一句话总结：**crontab 里只放"一行调用脚本"最省事**，把复杂的逻辑、环境准备、日志处理、加锁都写进脚本本身。脚本能手动跑通，再放进 cron，成功率会高得多。

---

## 本章小结

本章我们学习了Linux定时任务：

### 🔑 核心知识点

1. **cron定时任务**：
   - crond是守护进程，每分钟检查一次
   - `crontab -e`编辑任务
   - `crontab -l`查看任务

2. **cron表达式**：
   - 格式：`分 时 日 月 周 命令`
   - `*`每一，`,`列表，`-`范围，`/`间隔

3. **系统定时目录**：
   - `/etc/cron.daily/`：每天
   - `/etc/cron.hourly/`：每小时
   - `/etc/cron.weekly/`：每周
   - `/etc/cron.monthly/`：每月

4. **一次性任务**：
   - `at`命令安排一次性的延时任务
   - `at -l`查看
   - `atrm`删除

5. **Systemd定时器**：
   - `.timer`单元配`.service`单元
   - 比cron更现代，功能更强大

### 💡 记住这个原则

> **重复任务用cron，一次任务用at。** cron负责日常自动化，at负责临时延时任务。
