+++
title = "第57章：系统监控"
weight = 570
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第五十七章：系统监控

## 57.1 top/htop

### top 简介

`top` 是 Linux 下最常用的实时系统监控工具，就像给你的服务器装了一个"实时仪表盘"。

```bash
# 启动 top
top

# top 界面解读
top - 10:30:15 up 15 days,  2:33,  1 user,  load average: 0.52, 0.58, 0.59
Tasks: 245 total,   1 running, 244 sleeping,   0 stopped,   0 zombie
%Cpu(s): 12.5 us,  3.2 sy,  0.0 ni, 82.1 id,  2.1 wa,  0.0 hi,  0.1 si,  0.0 st
MiB Mem :  16384.0 total,   4096.0 free,   8192.0 used,   4096.0 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.   8192.0 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
    1 root      20   0  168.0m   5.6m   4.2m S   0.0   0.0   0:05.23 systemd
 1234 mysql     20   0 1234.5m 234.5m   0.0m S   5.2   1.4   2:34.56 mysqld
 5678 nginx     20   0   89.2m   12.3m   8.1m S   0.5   0.1   1:23.45 nginx
```

### 常用交互命令

| 按键 | 说明 |
|------|------|
| `q` | 退出 top |
| `h` | 帮助 |
| `1` | 显示所有 CPU 核心详情 |
| `P` | 按 CPU 使用率排序 |
| `M` | 按内存使用排序 |
| `T` | 按累计时间排序 |
| `k` | 杀死进程 |
| `r` | 修改进程优先级 |
| `z` | 切换彩色/单色显示 |
| `c` | 显示完整命令 |
| `f` | 设置显示字段 |

### top 常用选项

```bash
# 指定更新间隔（秒）
top -d 5

# 指定刷新次数
top -n 10

# 指定用户
top -u mysql

# 显示特定进程
top -p 1234

# 显示线程
top -H

# 显示进程树
top -c -p $(pgrep -d ',' process_name)
```

### htop（增强版）

`htop` 是 top 的升级版，界面更友好，支持鼠标操作：

```bash
# 安装
sudo apt install htop   # Ubuntu/Debian
sudo yum install htop   # CentOS

# 启动
htop
```

### htop 界面特色

```bash
# 常用选项
htop -d 10              # 10秒刷新
htop -u www-data         # 只显示某用户
htop -p 1234,5678        # 显示特定进程
htop --tree             # 显示进程树
```

htop 界面特色：
- 可视化 CPU/内存/交换分区使用条
- 支持鼠标点击操作
- 上下滚动查看进程
- F9 可发送信号
- 支持搜索和过滤

## 57.2 vmstat/iostat

### vmstat - 虚拟内存统计

```bash
# 基本用法
vmstat

# 指定采样间隔和次数
vmstat 1 5

# 输出：
# procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
#  r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
#  1  0      0 4096000 123456 789012    0    0     0     0   100  200 10  5 85  0  0
```

### vmstat 字段说明

| 字段 | 说明 |
|------|------|
| r | 运行中进程数 |
| b | 阻塞进程数 |
| swpd | 虚拟内存使用 |
| free | 空闲内存 |
| si/so | 换入/换出 |
| us/sy/id | 用户/系统/空闲 CPU |

### iostat - I/O 统计

```bash
# 安装
sudo apt install sysstat

# 基本用法
iostat

# 带时间戳
iostat -t

# 显示详细设备统计
iostat -x

# 每秒更新
iostat 1
```

### iostat 输出解读

```bash
# iostat -x 输出示例：
Linux 5.4.0 (hostname)     03/24/2026     _x86_64_        (2 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
         10.23    0.00     5.12     2.34     0.00    82.31

Device  rrqm/s  wrqm/s  r/s    w/s     rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
sda       0.00    12.34   5.23   8.45   234.56   567.89    45.23     0.12    5.23   3.21   6.45   2.15   0.05
```

### mpstat - 多核 CPU 统计

```bash
# 安装（通常在 sysstat 包中）
mpstat

# 显示每个 CPU 核心
mpstat -P ALL

# 每秒更新
mpstat 1
```

## 57.3 sar - 系统活动报告

`sar` 是最全面的系统监控工具，能收集和报告各种系统活动。

```bash
# 安装
sudo apt install sysstat

# 启用数据收集
sudo systemctl enable sysstat
sudo systemctl start sysstat

# 查看 CPU 使用率
sar -u

# 查看 CPU 使用率（所有核心）
sar -P ALL

# 查看内存使用
sar -r

# 查看交换分区
sar -S

# 查看 I/O
sar -b

# 查看网络
sar -n DEV
```

### sar 数据来源

```bash
# sar 数据保存在 /var/log/sa/
ls /var/log/sa/

# 查看指定日期的数据
sar -f /var/log/sa/sa24
```

### sar 常用组合

```bash
# CPU 和负载
sar -q

# 运行队列和负载
sar -q -r

# 内存和页面交换
sar -r -s

# 块设备 I/O
sar -d

# 网络接口
sar -n TCP,ETCP,SOCK
```

### 实时监控

```bash
# 每秒报告一次 CPU
sar 1 1

# 每2秒报告一次，共报告5次
sar -o /tmp/datafile 2 5

# 从文件读取数据
sar -f /tmp/datafile
```

## 57.4 free/df

### free - 内存使用

```bash
# 基本用法
free

# 人类可读格式
free -h

# 显示详细信息
free -l

# 显示总计
free -t

# 每秒更新
watch free -h
```

### free 输出解读

```bash
# free -h 输出：
#               total        used        free      shared  buff/cache   available
# Mem:           16Gi       8.0Gi       4.0Gi       1.0Gi       4.0Gi       8.0Gi
# Swap:         2.0Gi          0B       2.0Gi

# 字段说明：
# total    总物理内存
# used     已使用内存
# free     完全空闲内存
# shared   共享内存
# buff/cache  缓冲区/缓存
# available  可用内存（估算）
```

### df - 磁盘空间

```bash
# 基本用法
df

# 人类可读格式
df -h

# 显示 inode 信息
df -i

# 显示特定文件系统
df -h /home

# 显示所有文件系统（包括虚拟）
df -a

# 使用 1K blocks
df -k
```

### df 输出解读

```bash
# df -h 输出：
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1       100G   50G   45G  53% /
# tmpfs           2.0G     0  2.0G   0% /dev/shm
# /dev/sdb1       500G  200G  280G  42% /data

# 字段说明：
# Filesystem  文件系统
# Size        总大小
# Used        已使用
# Avail       可用
# Use%        使用率
# Mounted on  挂载点
```

### du - 目录/文件大小

```bash
# 当前目录大小
du -sh

# 指定目录大小
du -sh /var/log

# 显示子目录大小
du -h --max-depth=1 /home

# 排序显示
du -sh /var/* | sort -h

# 排除特定目录
du -sh --exclude='*.log' /var
```

## 57.5 Zabbix

Zabbix 是企业级开源监控系统，功能强大。

### 安装 Zabbix

```bash
# Ubuntu/Debian
wget https://repo.zabbix.com/zabbix/6.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.0-1+ubuntu$(lsb_release -rs)_all.deb
sudo dpkg -i zabbix-release_6.0-1+ubuntu$(lsb_release -rs)_all.deb
sudo apt update
sudo apt install zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts mysql-server

# 初始化数据库
sudo mysql
# CREATE DATABASE zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
# CREATE USER 'zabbix'@'localhost' IDENTIFIED BY 'password';
# GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';
# QUIT;

# 导入数据
zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql -u zabbix -p zabbix

# 配置 Zabbix
sudo nano /etc/zabbix/zabbix_server.conf
# DBPassword=password

# 启动服务
sudo systemctl restart zabbix-server apache2
sudo systemctl enable zabbix-server apache2
```

### Zabbix 核心概念

```mermaid
graph LR
    A[主机] --> B[监控项<br/>Items]
    A --> C[触发器<br/>Triggers]
    A --> D[图形<br/>Graphs]
    
    B --> E[数据收集]
    C --> F[告警触发]
    
    G[模板] --> A
```

| 概念 | 说明 |
|------|------|
| Host | 被监控的服务器/设备 |
| Item | 监控指标（CPU、内存、网络等） |
| Trigger | 触发条件（告警阈值） |
| Action | 触发后的动作（通知、脚本） |
| Template | 监控模板，复用配置 |

### Zabbix Agent 安装

```bash
# 安装 Agent
sudo apt install zabbix-agent

# 配置
sudo nano /etc/zabbix/zabbix_agentd.conf
# Server=192.168.1.100    # Zabbix Server IP
# ServerActive=192.168.1.100
# Hostname=web-server-01

# 启动
sudo systemctl start zabbix-agent
sudo systemctl enable zabbix-agent
```

## 57.6 Prometheus

Prometheus 是云原生监控的事实标准，与 Kubernetes 完美配合。

### 安装 Prometheus

```bash
# 下载
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvf prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64

# 配置
sudo nano prometheus.yml
```

### prometheus.yml 配置

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'linux'
    static_configs:
      - targets: ['192.168.1.101:9100']
```

### 启动 Prometheus

```bash
# 启动
./prometheus --config.file=prometheus.yml

# 或者 systemd 服务
sudo mv prometheus.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start prometheus
```

### Prometheus 数据模型

```mermaid
graph LR
    A[指标名称] --> B{标签}
    B --> C[实例]
    B --> D[作业]
    C --> E[时间序列]
```

```promql
# 查询 CPU 使用率
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 查询内存使用
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# 查询磁盘使用
100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)
```

### node_exporter（系统指标）

```bash
# 安装 node_exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.0/node_exporter-1.6.0.linux-amd64.tar.gz
tar xvf node_exporter-1.6.0.linux-amd64.tar.gz
cd node_exporter-1.6.0.linux-amd64
./node_exporter

# 默认端口 9100
# http://localhost:9100/metrics
```

## 57.7 Grafana

Grafana 是最流行的可视化平台，与 Prometheus 配合堪称完美。

### 安装 Grafana

```bash
# Ubuntu/Debian
sudo apt install -y apt-transport-https software-properties-common
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt update
sudo apt install grafana

# 启动
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

### 访问 Grafana

```
# 默认地址
http://localhost:3000

# 默认账密
用户名：admin
密码：admin
```

### 添加 Prometheus 数据源

1. 登录 Grafana
2. 点击 "Configuration" → "Data Sources"
3. 选择 "Prometheus"
4. URL: `http://localhost:9090`
5. 点击 "Save & Test"

### 创建仪表盘

```json
// Grafana Dashboard JSON 示例（CPU 使用率）
{
  "title": "System Overview",
  "panels": [
    {
      "title": "CPU Usage",
      "type": "graph",
      "targets": [
        {
          "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
          "legendFormat": "{{instance}}"
        }
      ]
    },
    {
      "title": "Memory Usage",
      "type": "graph", 
      "targets": [
        {
          "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
          "legendFormat": "{{instance}}"
        }
      ]
    }
  ]
}
```

### 常用 Dashboard ID

从 Grafana 官网导入现成仪表盘：

| Dashboard | ID | 说明 |
|-----------|-----|------|
| Node Exporter Full | 1860 | 完整的系统监控 |
| Prometheus Stats | 2 | Prometheus 自身状态 |
| Nginx | 12740 | Nginx 监控 |

### Alerting 配置

```yaml
# prometheus.yml 添加 alerting
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

# 告警规则示例
groups:
  - name: example
    rules:
    - alert: HighCPU
      expr: 100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High CPU usage on {{ $labels.instance }}"
```

## 本章小结

本章我们学习了 Linux 系统监控工具：

| 工具 | 用途 | 特点 |
|------|------|------|
| top/htop | 进程监控 | 实时、交互式 |
| vmstat | 虚拟内存 | 简洁、快速 |
| iostat | I/O 统计 | 磁盘性能 |
| sar | 综合监控 | 历史数据 |
| free/df | 资源查看 | 内存/磁盘 |
| Zabbix | 企业监控 | 功能全面 |
| Prometheus | 云原生监控 | 时序数据库 |
| Grafana | 可视化 | 仪表盘 |

监控体系架构：

```mermaid
graph TB
    A[数据采集] --> B[时序数据库]
    B --> C[查询引擎]
    C --> D[可视化平台]
    
    E[node_exporter] --> A
    F[应用程序] --> A
    G[Zabbix Agent] --> A
```

---

> 💡 **温馨提示**：
> 监控不是"出了问题才看"，而是"防患于未然"。建议设置合理的告警阈值，既不要"告警疲劳"，也不要漏掉真正的问题。记住：**没有监控的服务器就像没有仪表盘的飞机**！

---

**第五十七章：系统监控 — 完结！** 🎉

下一章我们将学习"日志管理"，掌握 journalctl、rsyslog、logrotate、ELK Stack、Loki 等日志处理工具。敬请期待！ 🚀
