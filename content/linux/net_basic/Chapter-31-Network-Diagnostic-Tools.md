+++
title = "第31章：网络诊断工具"
weight = 310
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第三十一章：网络诊断工具

想象一下：你的网站打不开了、SSH连不上了、网页加载转圈了……这时候怎么办？

答案是：网络诊断工具。

网络诊断就像医生的听诊器——先确定"病在哪"，再决定"怎么治"。ping看通不通，traceroute看路径，nslookup/dig看DNS，netstat/ss看端口，tcpdump抓包分析……每一把扳手都有它的用武之地。

> 本章配套视频：你的服务器突然失联？别慌，先ping一下，看看是网络的问题还是你的问题。

## 31.1 ping 命令：网络连通性测试

`ping`是网络诊断的"万金油"，几乎所有人认识网络的第一个命令就是`ping`。它的原理很简单：发送ICMP Echo Request包，对方回复ICMP Echo Response包，通过往返时间判断网络是否通畅。

### 31.1.1 ping -c 4：次数

默认情况下，`ping`会一直运行下去（Ctrl+C停止）。用`-c`参数指定发送次数。

```bash
# 发送4个ping包，然后自动停止
ping -c 4 8.8.8.8
```

```bash
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=12.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=118 time=11.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=118 time=12.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=118 time=11.9 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 11.8/12.0/12.3/0.2 ms
```

输出解读：

- `icmp_seq=1,2,3,4`：ICMP序列号，每个包一个编号
- `ttl=118`：生存时间（Time To Live），是**剩余值**，每经过一个路由器减1，防止数据包在网络中无限循环。TTL收到时是118，说明这个包在到达你之前已经被沿途路由器共减去了一些（常见初始值有64、128、255）
- `time=12.3 ms`：往返延迟，12.3毫秒
- `0% packet loss`：丢包率，0%表示4个包全部收到，网络畅通
- `rtt min/avg/max/mdev`：往返时间统计（最小/平均/最大/标准差）

> **别踩这个坑**：很多人以为"用初始值减去收到的 TTL 就是跳数"，但初始 TTL 到底是 64、128 还是 255，并不确定（取决于对端操作系统和对方是否修改过）。所以只能反推一个**大致范围**：如果对端初始值为 64，收到 118 是不可能的（说明初始值至少 128），此时大约经过了 10 跳。想准确知道跳数，请用 `traceroute` 或 `mtr`，不要靠 TTL 猜。

### 31.1.2 ping -i 0.2：间隔

`-i`参数控制ping包的发送间隔（秒）。

```bash
# 每0.2秒发一个包（这是普通用户能用的最小间隔）
ping -c 10 -i 0.2 192.168.1.1

# 每5秒发一个包（减少网络负载）
ping -c 5 -i 5 www.baidu.com
```

> **权限提示**：Linux 下普通用户允许的最小间隔就是 `0.2` 秒，再小会报 `ping: cannot flood; minimal interval allowed for user is 200ms`。只有 root 才能用 `-f`（flood）或更小的 `-i`。另外第一次 ping 里 `-c 4` 默认发完约 3 秒（间隔 1 秒），不要拿 `time 3005ms` 当延迟。

```bash
# ping本机网关，测试本地网络是否正常
ping -c 4 192.168.1.1

# ping公网DNS，测试外网连接
ping -c 4 8.8.8.8

# ping域名（会先做DNS解析）
ping -c 4 www.baidu.com
```

**常见ping结果分析**：

判断时要**综合丢包率和往返延迟**（注意这里的 `time` 是上一步的 `time=` 字段，即单次 RTT，不是统计里那个 `time 3005ms`）：

| 丢包率 | RTT | 可能原因 |
|------|---------|---------|
| 0% | `time<1ms` | 极低延迟，本地网络或同机房通信 |
| 0% | `time=10-50ms` | 正常的互联网通信 |
| 0% | `time>200ms` | 跨国链路或卫星通信，延迟偏高 |
| 部分丢包 | 时快时慢 | 链路拥塞，或对端限速了 ICMP |
| 100% | 无正常回包 | 目标不可达、被防火墙拦截，或对端禁 ping |
| 100% | 报 `Name or service not known` | 不是网络不通，而是**域名解析失败**，先查 DNS |

> **有趣的现象**：你ping一个网站，发现丢包率5%。这时候不要急着骂网络质量差——很多服务器故意限制ICMP包速率，防止ping攻击。ping不通不等于网站打不开。
> 
> 🎯 **实际建议**：判断网站是否正常，最好用`curl -I http://网站地址`看HTTP响应，而不是单纯依赖ping。

## 31.2 traceroute 命令：路由追踪

`traceroute`（Linux）/ `tracert`（Windows）用于追踪数据包从你的电脑到目标主机经过的所有路由节点。

如果说`ping`是问"你在不在"，`traceroute`就是问"你去那儿的路上都经过了谁"。

### 31.2.1 traceroute 目标

```bash
# 追踪到目标主机的路由路径
traceroute www.baidu.com
```

```bash
traceroute to www.baidu.com (220.181.38.149), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  1.234 ms  1.089 ms  0.987 ms
 2  10.0.0.1 (10.0.0.1)  3.456 ms  3.123 ms  2.987 ms
 3  61.135.112.1 (61.135.112.1)  8.765 ms  8.234 ms  8.123 ms
 4  220.181.0.1 (220.181.0.1)  12.345 ms  11.987 ms  11.876 ms
 5  220.181.38.149 (220.181.38.149)  13.567 ms  13.234 ms  13.123 ms
```

每一行代表一个"跳"（hop），即经过的一个路由器。

- `1, 2, 3, 4, 5`：跳数序号
- 中间的IP：经过的路由器IP
- 最后一行`220.181.38.149`：目标服务器IP
- 每行三个时间：三次测量的延迟

**关键发现**：

- 如果某个IP之后没有更多跳，说明目标已经到达
- 如果某个跳出现`* * *`（超时），说明那个路由器**不返回**探测超时消息——可能是防火墙拦截，也可能只是该路由器配置为不回 ICMP 超时。**只要后面的跳和最终目标能到达，这一跳的 `*` 就不用担心**
- 如果某跳延迟突然飙升，说明那一段网络拥塞或路由不佳

> **判断技巧**：如果是"中间的某一跳全是 `*`，但从这一跳往后一直到目标都正常"，那通常不是故障；真正要警惕的是"从某一跳开始**后面全部** `*`，且到不了目标"。

### 31.2.2 traceroute -I：ICMP

默认情况下，Linux的`traceroute`使用UDP数据包，而Windows的`tracert`使用ICMP。

`-I`参数让`traceroute`使用ICMP包（和Windows的tracert一样）。

```bash
# 使用ICMP协议进行路由追踪
sudo traceroute -I www.baidu.com

# 使用TCP SYN进行追踪（穿透防火墙，部分管理员会封ICMP/UDP）
sudo traceroute -T -p 80 www.baidu.com
```

> **为什么都加了 sudo**：`-I`（ICMP）和 `-T`（TCP SYN）都需要原始套接字权限，普通用户直接跑会报 `Operation not permitted`。默认的 UDP 方式普通用户即可。

> **部分系统没有 traceroute**：Debian/Ubuntu 用 `sudo apt install traceroute`，RHEL 系用 `sudo dnf install traceroute`。也可以直接用 `mtr`，它自带 traceroute 功能。

> **traceroute的原理**：它发送TTL=1的包，第一个路由器收到后TTL减为0，返回超时消息——这样你就知道了第一跳；然后发送TTL=2的包，知道第二跳……依此类推，直到到达目标。

## 31.3 mtr 命令：ping 和 traceroute 结合

`mtr`（My Traceroute）是`ping`和`traceroute`的合体金刚，一边持续ping，一边绘制路由路径，实时显示网络质量统计。

### 31.3.1 mtr 目标

```bash
# 安装mtr（如果没有）
sudo apt install mtr-tiny

# 运行mtr（按q退出）
mtr www.baidu.com
```

```bash
                            My traceroute  [v0.95]
my-server (192.168.1.100)
                               Keys:  Help   Display mode   Restart statistics  Order of fields   quit
                                                                                          Packets               Pings
 Host                                                                                       Loss%   Last   Avg  Best  Wrst StDev
  1. 192.168.1.1                                                                0.0%   1.2   1.3   1.0   2.1   0.2
  2. 10.0.0.1                                                                   0.0%   3.1   3.4   2.8   4.2   0.3
  3. 61.135.112.1                                                               0.0%   8.5   9.2   8.0  12.3   1.1
  4. 220.181.0.1                                                                10.0%  15.2  13.8  12.1  18.5   2.3
  5. 220.181.38.149                                                            0.0%  13.1  13.5  12.8  14.2   0.4
```

输出解读：

- 每一行是一个跳（路由节点）
- `Loss%`：丢包率
- `Last`：最近一次延迟
- `Avg`：平均延迟
- `Best`：最佳延迟
- `Wrst`：最差延迟
- `StDev`：标准差（数值越大说明延迟波动越大）

> **注意列的差异**：交互模式（直接运行 `mtr`）的列是 `Loss% Last Avg Best Wrst StDev`；`-r` 报告模式多了一列 `Snt`（本跳已发送的探测包数），顺序是 `Loss% Snt Last Avg Wrst StDev`。列名对不上时以实际表头为准。

从上面结果看，第4跳（220.181.0.1）有10%的丢包率，但**第5跳又恢复到0%**——这种"中间跳丢包、后面正常"通常是该路由器对探测包的响应限速，不代表真实故障。真正要关注的是**最后一跳（目标）的丢包率**，它才反映端到端的真实质量。

### 31.3.2 mtr -r：报告模式

`-r`参数生成一份文本报告，适合保存或发送给别人分析。

```bash
# 生成报告并退出
mtr -r -c 10 www.baidu.com
```

```bash
Start: Mon Mar 23 22:00:00 2026
HOST: my-server                   Loss%   Snt   Last   Avg  Wrst  StDev
  1.|-- 192.168.1.1                0.0%    10    1.2   1.3   2.1   0.2
  2.|-- 10.0.0.1                   0.0%    10    3.1   3.4   4.2   0.3
  3.|-- 61.135.112.1               0.0%    10    8.5   9.2  12.3   1.1
  4.|-- 220.181.0.1               10.0%    10   15.2  13.8  18.5   2.3
  5.|-- 220.181.38.149             0.0%    10   13.1  13.5  14.2   0.4
```

> `Snt` 是"已发送探测包数"（`-c 10` 所以是10），`Loss%` 就是基于它算出来的。注意：`-r` 报告会**一次性发完指定次数**，比交互模式更适合放进脚本存档、发给同事分析。

## 31.4 nslookup 命令：DNS 查询

`nslookup`（Name Server Lookup）是DNS查询的老前辈，功能简单但实用。它的"继任者"是`dig`，但`nslookup`在Windows上原生自带，所以依然广泛使用。

### 31.4.1 nslookup 域名

```bash
# 查询域名的IP
nslookup www.baidu.com
```

```bash
Server:         8.8.8.8
Address:        8.8.8.8#53

Non-authoritative answer:
www.baidu.com   canonical name = www.a.shifen.com.
Name:   www.a.shifen.com
Address: 220.181.38.149
Name:   www.a.shifen.com
Address: 220.181.38.150
```

解读：

- `Server: 8.8.8.8`：当前使用的DNS服务器是Google DNS
- `Non-authoritative answer`：非权威应答（说明这个答案是DNS服务器缓存返回的，不是baidu.com的权威DNS服务器直接回答的）
- `canonical name = www.a.shifen.com.`：`www.baidu.com` 是别名（CNAME），真正解析到的是 `www.a.shifen.com`
- `www.a.shifen.com`有两个IP：220.181.38.149和220.181.38.150——百度做了负载均衡（同一域名返回多个IP，客户端轮流使用）

> **示例数据仅作格式示意**：域名对应的 IP、CNAME 目标、TTL 都会随时间变化，你自己执行时得到的结果和这里不同是正常的，重点是看懂输出结构。

### 31.4.2 nslookup -type=MX 域名

`-type`参数可以查询特定类型的DNS记录。

```bash
# 查询邮件交换记录（MX记录）
nslookup -type=MX baidu.com
```

```bash
baidu.com       mail exchanger = 10 mx.mail.baidu.com.
baidu.com       mail exchanger = 20 mx1.mail.baidu.com.
```

`mail exchanger = 10`：优先级是10，数字越小优先级越高。发送邮件时优先尝试10号服务器，如果10号不可用再试20号。

> **别漏掉结尾的点**：`mx.mail.baidu.com.` 末尾这个 `.` 表示它是**完全限定域名（FQDN）**。如果配置 DNS 时漏掉这个点，解析器可能会自作主张拼上当前域名，变成 `mx.mail.baidu.com.example.com`，导致邮件发不出去。

**常见DNS记录类型**：

| 类型 | 说明 | 用途 |
|------|------|------|
| A | IPv4地址 | 域名指向IPv4地址 |
| AAAA | IPv6地址 | 域名指向IPv6地址 |
| MX | 邮件交换 | 指定邮件服务器 |
| CNAME | 别名 | 域名别名 |
| NS | 域名服务器 | 指定该域名的DNS服务器 |
| TXT | 文本记录 | SPF、DKIM 等邮件验证 |
| PTR | 反向解析 | 由 IP 反查域名 |
| SOA | 起始授权记录 | 标明该域名的权威 DNS 及其序列号 |
| CAA | 证书颁发授权 | 限定哪些 CA 可以为该域名签发证书 |

## 31.5 dig 命令：详细 DNS 查询

`dig`（Domain Information Groper）是DNS查询的"瑞士军刀"，比`nslookup`功能更强大、输出更详细。DNS工程师必备工具。

### 31.5.1 dig 域名

```bash
# 基本的DNS查询
dig www.baidu.com
```

```bash
; <<>> DiG 9.18.1 <<>> www.baidu.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
;; EDNS: version 0, flags:; udp: 4096
;; QUESTION SECTION:
;www.baidu.com.                 IN      A

;; ANSWER SECTION:
www.baidu.com.          600     IN      CNAME   www.a.shifen.com.
www.a.shifen.com.       600     IN      A       220.181.38.149
www.a.shifen.com.       600     IN      A       220.181.38.150

;; Query time: 12 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Mar 23 22:00:00 CST 2026
;; MSG SIZE  rcvd: 115
```

输出解读：

- `HEADER` 里的 `ANSWER: 3`：ANSWER 段共 3 条记录（1 条 CNAME + 2 条 A）
- `QUESTION SECTION`：查询的问题（查询www.baidu.com的A记录）
- `ANSWER SECTION`：查询结果（www.baidu.com是CNAME别名，指向www.a.shifen.com，后者有两个A记录IP）
- 记录行里的 `600`：TTL，缓存生存时间600秒（`www.baidu.com. 600 IN CNAME ...` 里的 600 就是它）
- `Query time: 12 msec`：查询耗时12毫秒
- `SERVER: 8.8.8.8#53`：使用的DNS服务器

> **示例数据仅作示意**：应答记录、CNAME 目标、TTL 都会变化，重点理解各分段的含义。

### 31.5.2 dig +trace：递归查询

`+trace`参数从根域名服务器开始，完整展示DNS递归查询的整个过程——和traceroute类似，但针对DNS。

```bash
# 追踪DNS查询路径
dig +trace www.baidu.com
```

```bash
; <<>> DiG 9.18.1 <<>> +trace www.baidu.com
.                       518400  IN      NS      a.root-servers.net.
.                       518400  IN      NS      b.root-servers.net.
...（省略根服务器列表）

com.                    172800  IN      NS      a.gtld-servers.net.
...（省略.com TLD服务器）

baidu.com.              172800  IN      NS      ns.baidu.com.
baidu.com.              172800  IN      NS      dns.baidu.com.

www.baidu.com.          600     IN      CNAME   www.a.shifen.com.
www.a.shifen.com.       600     IN      A       220.181.38.149
```

可以看到DNS查询的完整链路：根服务器 → .com顶级域服务器 → baidu.com权威DNS → 最终IP。

> **+trace 的特别之处**：它会**绕过** `/etc/resolv.conf` 里配置的 DNS 服务器，从根服务器开始一级一级自己问，所以看到的是"真实解析链路"，而不是本机 DNS 缓存或转发器给出的结果。排查"某个上游 DNS 返回了错误 IP"这类问题时特别有用。

**dig的其他常用参数**：

```bash
# 只显示answer部分（简洁输出）
dig +short www.baidu.com

# 指定DNS服务器查询
dig @8.8.8.8 www.baidu.com

# 查询AAAA记录（IPv6）
dig AAAA ipv6.example.com

# 反向查询（IP反解域名）
dig -x 220.181.38.149

# 查询NS记录（域名服务器）
dig NS baidu.com

# 只查某个记录类型，输出含问题段和应答段
dig MX baidu.com

# 指定从权威服务器直接查（带 +norecurse 避免它替你递归）
dig @a.gtld-servers.net baidu.com NS +norecurse
```

## 31.6 host 命令：简单的 DNS 查询

`host`是DNS查询的"简化版"，输出比`dig`简洁，适合快速查看。

```bash
# 安装host（部分最小化安装没有）
sudo apt install dnsutils
# RHEL/CentOS/Rocky 上包名叫 bind-utils：sudo dnf install bind-utils

# 基本查询
host www.baidu.com
```

```bash
www.baidu.com is an alias for www.a.shifen.com.
www.a.shifen.com has address 220.181.38.149
www.a.shifen.com has address 220.181.38.150
```

```bash
# 反向查询
host 220.181.38.149
```

```bash
149.38.181.220.in-addr.arpa domain name pointer www.a.shifen.com.
```

> **更简洁的用法**：`host -t MX baidu.com` 查邮件记录，`host -t NS baidu.com` 查域名服务器，`host -v` 显示和 dig 一样详细的信息。想脚本里取值，用 `host www.baidu.com | awk '{print $NF}'` 或直接换 `dig +short`。

## 31.7 netstat 命令：网络状态统计

`netstat`（Network Statistics）是查看网络连接、路由表、接口统计的经典工具。它属于 `net-tools` 软件包，**较新的发行版默认不再预装**（如 Ubuntu 20.04+、较新的 RHEL/CentOS）。如果执行时报 `netstat: command not found`，优先直接用下一节的 `ss`；确实需要 `netstat` 时再安装：

```bash
# Debian/Ubuntu
sudo apt install net-tools

# RHEL/CentOS/Rocky
sudo dnf install net-tools
```

> `netstat` 已被官方标记为废弃（deprecated），维护处于停滞状态，新脚本建议一律用 `ss`。

### 31.7.1 netstat -tulpn：监听端口

查看本机正在监听的TCP和UDP端口（哪些服务在等着接受连接）。

```bash
netstat -tulpn
```

```bash
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1234/sshd: /usr/sbin
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      2345/cupsd
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      3456/mysqld
tcp6       0      0 :::80                  :::*                    LISTEN      4567/apache2
tcp6       0      0 :::443                 :::*                    LISTEN      4567/apache2
udp        0      0 0.0.0.0:68              0.0.0.0:*                          789/dhclient
udp        0      0 0.0.0.0:5353           0.0.0.0:*                          1011/avahi-daemon: r
```

参数说明：

- `-t`：TCP连接
- `-u`：UDP连接
- `-l`：仅显示监听状态的socket
- `-p`：显示占用端口的进程（**通常需要 root 才能看到其他用户的 PID/Program name**，非 root 执行对别人的进程只会显示 `-`）
- `-n`：显示数字端口（不解析服务名）

**解读常见端口监听状态**：

| 端口 | 服务 | 说明 |
|------|------|------|
| 22 | sshd | SSH服务器，等待远程登录 |
| 80 | apache2/nginx | Web服务器 |
| 443 | apache2/nginx | HTTPS服务器 |
| 3306 | mysqld | MySQL数据库 |
| 631 | cupsd | 打印机服务 |
| 68 | dhclient | DHCP客户端 |

### 31.7.2 netstat -an：所有连接

查看所有连接（包括已建立的连接），`-a`是all，`-n`是数字形式显示。

```bash
netstat -an
```

```bash
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0     36 192.168.1.100:22        203.0.113.50:54321      ESTABLISHED
tcp        0      0 127.0.0.1:3306          127.0.0.1:45678         TIME_WAIT
```

> 输出很长时用 `netstat -an | grep ESTABLISHED`、`netstat -anp | grep :3306` 之类过滤。`LISTEN` 行是服务端在等连接，`ESTABLISHED` 行是已经建立的连接（每一行对应一条连接，本机看到的"本地地址:端口"和"对端地址:端口"是成对出现的）。

连接状态（State）说明：

| 状态 | 含义 |
|------|------|
| LISTEN | 等待连接（服务端） |
| ESTABLISHED | 已建立连接（正在通信） |
| TIME_WAIT | 等待处理（连接已关闭但还有延迟包） |
| CLOSE_WAIT | 对方关闭了连接，本地还没关 |
| SYN_SENT | 正在发起连接（客户端） |
| SYN_RECEIVED | 收到连接请求，正在握手 |

### 31.7.3 netstat -r：路由表

```bash
netstat -r
```

```bash
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
default         192.168.1.1     0.0.0.0         UG        0 0          0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U         0 0          0 eth0
```

和`ip route`输出的内容一样，只是格式不同。

## 31.8 ss 命令：Socket Statistics

`ss`（Socket Statistics）是`netstat`的现代替代品，来自iproute2工具包，性能更高，信息更详细。

### 31.8.1 ss -tulpn

查看监听端口，用法类似`netstat -tulpn`，但更快。

```bash
ss -tulpn
```

```bash
State    Recv-Q   Send-Q   Local Address:Port    Peer Address:Port   Process
LISTEN   0        128            0.0.0.0:22           0.0.0.0:*       users:(("sshd",pid=1234,fd=3))
LISTEN   0        0              127.0.0.1:631        0.0.0.0:*       users:(("cupsd",pid=2345,fd=10))
LISTEN   0        0              0.0.0.0:3306         0.0.0.0:*       users:(("mysqld",pid=3456,fd=18))
LISTEN   0        0                 [::]:80              [::]:*       users:(("apache2",pid=4567,fd=4))
```

### 31.8.2 ss -s：统计摘要

`-s`参数显示各类 socket 的**统计摘要**（注意：它给的是"各类连接各有多少条"的汇总数字，**不会列出具体连接**。想列连接请用 `ss -tunap`）。排查 `TIME_WAIT` 太多、连接数异常增长这类问题时用它，一眼能看出量级。

```bash
ss -s
```

```bash
Total: 138
TCP:   12 (estab 1, closed 2, orphaned 0, synrecv 0, timewait 2), ports 0

Transport Total     IP        IPv6
*         138       -         -
RAW       0         0         0
UDP       3         3         0
TCP       12        8         4
INET      15        11        4
FRAG      0         0         0
```

解读：

- `Total: 138`：当前总的 socket 数
- `TCP: 12 (estab 1, ... timewait 2)`：TCP 共 12 条，其中已建立 1 条、TIME_WAIT 2 条
- 下半部分按 `Transport` 分类，分别统计 IPv4（IP）和 IPv6 的数量

> **TIME_WAIT 多是不是故障？** 不一定。它表示"主动关闭方"等 2MSL（约 60 秒）以确认最后的包已被对方收到，是 TCP 的正常设计。只有当它暴涨到上万条、耗尽本地端口时才算问题（多见于短连接跑得特别快的服务，比如反向代理）。

**ss的高级过滤**：

```bash
# 查看所有已建立的SSH连接
ss state established '( dport = :22 or sport = :22 )'

# 查看所有到80端口的连接
ss dst :80

# 查看所有来自特定IP的连接
ss src 203.0.113.50

# 只看 TCP，显示进程和端口号（最常用的组合，需要加引号避免 shell 展开）
sudo ss -tnp '( sport = :22 or dport = :22 )'

# 查看某状态（如 SYN-SENT、CLOSE-WAIT）的连接
ss -tan state syn-sent
```

> `-p` 显示进程同样需要 root 权限；过滤表达式一定要用单引号包起来，否则 `( sport = :22 )` 里的括号和空格会被 shell 抢先解释。

## 31.9 lsof 命令：查看端口占用

`lsof`（List Open Files）可以查看所有打开的文件和socket，网络连接也是一种"文件"。

### 31.9.1 lsof -i :80

查看哪个进程占用了80端口。

```bash
sudo lsof -i :80
```

```bash
COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx   10111   root    6u  IPv4 234567      0t0  TCP *:http (LISTEN)
nginx   10112 www-data    6u  IPv4 234567      0t0  TCP *:http (LISTEN)
```

输出解读：

- `COMMAND`：进程名（这里是 nginx）
- `PID`：进程ID
- `USER`：运行用户
- `TYPE`：socket类型（IPv4/IPv6）
- `STATE`：状态（LISTEN监听）

> **一个端口只能被一个监听进程占用**：同一时刻同一 IP:端口上通常只有一个服务在 LISTEN。如果你看到两个不同的服务（比如 nginx 和 apache2）都"占着 80"，多半是**先启动了 nginx、后来 apache2 启动失败**——真实占用的是先启动的那个。同一个服务出现多行（如上例中的 `root` 主进程和 `www-data` worker）是正常的：它们通过 fork 共享同一个监听 socket。想确认到底是哪个进程真正在监听，用 `sudo ss -tlpn 'sport = :80'` 最直接。

### 31.9.2 lsof -p PID

查看指定进程打开了哪些文件/socket。

```bash
# 查看SSH进程打开的所有文件
sudo lsof -p 1234

# 查看某个用户打开的所有网络连接（-a 是"并且"，否则会变成"或"）
sudo lsof -a -i -u www-data
```

```bash
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd    1234       root  cwd    DIR  253,0    4096    2 /
sshd    1234       root    3u  IPv4  12345      0t0  TCP *:ssh (LISTEN)
sshd    1234       root    4u  IPv6  12346      0t0  TCP *:ssh (LISTEN)
```

> **`lsof` 的条件默认是"或"**：写 `lsof -i -u www-data` 会列出"所有网络连接"**加上**"www-data 打开的所有文件"（两条条件是 OR）。要表达"既属于 www-data、又要是网络连接"，必须加 `-a`（AND）写成 `lsof -a -i -u www-data`。这是 lsof 最常见的一个坑。

## 31.10 nc/netcat 命令：网络瑞士军刀

`nc`（netcat）是网络工具中的"瑞士军刀"，可以用作端口扫描、连接测试、文件传输、代理等。

### 31.10.1 nc -zv 主机 端口

测试某个主机的某个端口是否开放（不建立完整连接，只测试）。

```bash
# 测试80端口是否开放
nc -zv 192.168.1.1 80

# 测试多个端口
nc -zv 192.168.1.1 22 80 443

# 扫描端口范围（仅 OpenBSD 版 nc 支持这种写法）
nc -zv 192.168.1.1 1-1000
```

```bash
Connection to 192.168.1.1 80 port [tcp/http] succeeded!
```

`-z`：zero-I/O模式，只测试连接，不发送数据
`-v`：verbose，输出详细信息

> **netcat 有多个"版本"，语法并不统一**：Ubuntu/Debian 默认装的是 **OpenBSD 版**（命令名 `nc`），支持 `nc -zv 主机 端口` 和 `端口范围`；而老式的 **GNU netcat** / **nmap 自带的 ncat** 对"一次传多个端口"和"范围扫描"的支持各不相同，可能报错或行为不一致。
> 因此：**扫描多个端口或端口范围，最稳妥的是用 `nmap`**（`nmap -p 22,80,443 192.168.1.1`，范围用 `-p 1-1000`），不要依赖 `nc` 的范围写法。单端口连通性测试用 `nc -zv` 就够了。

### 31.10.2 nc -l 端口：监听

在一台机器上启动监听，另一台机器连接过来——可以用于简单的聊天或文件传输。

```bash
# 机器A：在本机1234端口启动监听
nc -l 1234

# 机器B：连接到机器A的1234端口
nc 机器A的IP 1234

# 现在两台机器可以直接打字聊天了
```

> **监听写法也不同**：OpenBSD 版 `nc` 用 `nc -l 1234`（端口直接跟在 `-l` 后）；GNU netcat 传统写法是 `nc -l -p 1234`。如果报 `invalid option` 或行为异常，先 `nc -h` 看它是哪个版本。另外 OpenBSD 版默认在**客户端断开后**就退出，长时间反复接收要用 `-k`（`nc -lk 1234`）。

**用nc传输文件**：

```bash
# 机器A：发送文件
nc -l 1234 < file.txt

# 机器B：接收文件
nc 机器A的IP 1234 > received.txt
```

**用nc做端口转发（简易代理）**：

```bash
# 将本机8080端口的连接转发到192.168.1.1:80
nc -l 8080 | nc 192.168.1.1 80
```

> **注意这只是"单向"的**：上面这条只把客户端发来的数据转发给后端，后端返回的数据**不会自动回到客户端**。真正的双向转发要用 `socat`（推荐）或 `ssh -L`，例如 `socat TCP-LISTEN:8080,fork TCP:192.168.1.1:80`。`nc` 的管道写法只能用于临时、简单的场景。

> **警告**：netcat功能强大，但也很危险——它可以用来建立后门。在生产服务器上，如果不需要，请确保nc已卸载或限制访问。

## 31.11 tcpdump 命令：命令行抓包

`tcpdump`是Linux下最强大的命令行抓包工具，相当于Wireshark的命令行版。网络工程师用它来"听"网络上的数据包，分析网络问题。

### 31.11.1 tcpdump -i eth0

抓取eth0网卡上的数据包（需要root权限）。

```bash
# 抓取eth0上的所有数据包（前20个包）
sudo tcpdump -i eth0 -c 20

# 抓取并显示详细输出
sudo tcpdump -i eth0 -c 5 -v
```

```bash
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
22:00:00.123456 IP 192.168.1.100.45678 > 8.8.8.8.53: UDP, length 32
22:00:00.234567 IP 8.8.8.8.53 > 192.168.1.100.45678: UDP, length 64
22:00:00.345678 ARP, Request who-has 192.168.1.1 tell 192.168.1.100, length 46
22:00:00.345679 ARP, Reply 192.168.1.1 is-at 00:1a:2b:3c:4d:5e, length 46
22:00:00.456780 IP 192.168.1.100.22 > 203.0.113.50.54321: Flags [P.], seq 12345:12367, ack 67890, win 502, length 22
```

参数说明：

- `-i eth0`：监听eth0网卡（用`tcpdump -D`列出所有网卡）
- `-c 20`：抓20个包后自动停止
- `-v`：verbose，显示更详细的信息

### 31.11.2 tcpdump -w 文件

将抓到的包保存到文件（.pcap格式），可以用Wireshark打开分析。

```bash
# 抓包并每300秒（5分钟）滚动生成一个新文件，文件名按时间命名
sudo tcpdump -i eth0 -w capture-%Y%m%d-%H%M%S.pcap -G 300

# 捕获1000个包后停止，保存到文件
sudo tcpdump -i eth0 -w capture.pcap -c 1000

# 只抓5分钟就停止：G=每300秒轮转一次文件，W=只保留1个文件，效果就是超过300秒后覆盖/停止写入
sudo tcpdump -i eth0 -w capture.pcap -G 300 -W 1

# 或者更直接：用 timeout 在300秒后结束 tcpdump
sudo timeout 300 tcpdump -i eth0 -w capture.pcap

# 读取保存的pcap文件
sudo tcpdump -r capture.pcap

# 只显示HTTP流量
sudo tcpdump -r capture.pcap 'port 80'

# 只显示HTTPS流量
sudo tcpdump -r capture.pcap 'port 443'
```

> **`-G` 的真实含义**：`-G N` 表示"每 N 秒就把当前文件轮转（rotate）一次，起一个新的文件继续写"，**不是**"抓 N 秒后就停止"。想控制"抓多久就结束"，上面两种写法任选其一（`-G 300 -W 1` 或 `timeout 300`）。不加 `-W` 时会一直轮转、不断产生新文件，文件越来越多，别忘了清理。
> 用 `-w` 时**看不到任何包内容**（这是正常的，因为都写进文件了），需要加 `-v` 或 `-U` 观察进度，或抓完再用 Wireshark / `tcpdump -r` 打开。

**常用过滤表达式**：

```bash
# 只抓ICMP包（ping包）
sudo tcpdump -i eth0 icmp

# 只抓来自192.168.1.100的包
sudo tcpdump -i eth0 src 192.168.1.100

# 只抓发往80端口的包
sudo tcpdump -i eth0 dst port 80

# 抓HTTP GET请求（0x47455420 就是 "GET " 四个字节的十六进制）
sudo tcpdump -i eth0 -A -s0 'tcp port 80 and (tcp[((tcp[12] & 0xf0) >> 2):4] = 0x47455420)'

# 直接以ASCII显示HTTP内容（最直观，推荐先用这个）
sudo tcpdump -i eth0 -A -s0 'tcp port 80'
```

> **为什么上面那个偏移量写得那么绕**：`tcp[20:4]` 假设 TCP 头正好 20 字节（没有选项）。有 TCP 选项时头部会更长，固定偏移 20 就取错了位置。`tcp[((tcp[12] & 0xf0) >> 2):4]` 先读出"数据偏移"字段算出真实头部长度再定位，才通用。实际工作中通常不折腾这个，直接用 `-A` 看内容、或用 Wireshark 过滤。

> **别忘了 `-s0`**：老版本 tcpdump 默认只抓 68 字节（截断包），分析时看不到完整载荷，加 `-s0`（或 `-s 262144`）抓完整包。新版默认已是抓全包。

## 31.12 Wireshark：图形化抓包分析

Wireshark是世界上最流行的网络协议分析器，图形界面，操作直观。`tcpdump`擅长在服务器上抓包，`Wireshark`擅长在PC上分析抓包结果。

```bash
# Linux上安装Wireshark（需要图形环境）
sudo apt install wireshark

# 如果想非root用户运行，需要配置
sudo usermod -aG wireshark "$USER"
# 重新登录后生效
```

Wireshark的核心功能：

- 实时抓包，边抓边看
- 过滤表达式（比tcpdump更强大）
- 追踪TCP流（Follow TCP Stream）
- 解密HTTPS流量（需要SSLKEYLOGFILE）
- 专家信息分析（自动诊断网络问题）

> **关于"解密HTTPS"**：Wireshark 本身**不能**破解 TLS。它的做法是让浏览器把本次会话的密钥导出到一个文件（环境变量 `SSLKEYLOGFILE=~/sslkeys.log`），再在 Wireshark 的 `Preferences → Protocols → TLS` 里指定该文件。前提是**应用支持导出密钥日志**（Chrome、Firefox、curl 支持），而且只能解密"你自己机器上、导出了密钥的"那些会话，对别人的流量无效。

> **抓包权限的安全提醒**：把用户加入 `wireshark` 组等价于给了它抓取**本机所有网卡流量**的权限（包括明文密码、令牌），等于半个 root。只在受信任的个人机器上这么做，服务器上还是用 `tcpdump` 按需抓、抓完即删更稳妥。

**Wireshark过滤语法示例**：

```
# 只显示HTTP请求
http.request

# 只显示DNS查询
dns

# 只显示TCP RST包（重置连接）
tcp.flags.reset == 1

# 只显示与某个IP相关的包
ip.addr == 192.168.1.100

# 只显示HTTP Host为baidu.com的请求
http.host == "baidu.com"
```

## 31.13 iptraf/iftop/nethogs：流量监控

除了抓包，还有一些实时流量监控工具，可以实时查看哪些连接占用了带宽。

**iftop**：按连接查看实时流量

```bash
# 安装iftop
sudo apt install iftop

# 运行（按q退出）
sudo iftop -i eth0
```

```bash
# iftop界面示例
                            12.5Kb          25.0Kb          37.5Kb          50.0Kb
localhost:ssh-ssh                      => 203.0.113.50:54321     1.52Kb  1.23Kb  1.15Kb
                             <=                               2.34Kb  2.01Kb  1.89Kb
                       192.168.1.100:ssh                     => 192.168.1.1:domain    0b      96b     79b
                             <=                               240b    195b    161b
```

iftop显示每个连接方向的实时带宽，左边是源IP:端口，右边是目标IP:端口，中间是带宽刻度。

**nethogs**：按进程查看实时流量

```bash
# 安装nethogs
sudo apt install nethogs

# 运行（按q退出）
sudo nethogs eth0
```

```bash
  PID USER     PROGRAM                DEV        SENT      RECEIVED
 4567 root     apache2                eth0       1. KB     12.345 KB
 1234 root     sshd: session          eth0       0.789 KB      1.234 KB
  ?   root     unknown TCP                     0.000       0.000 KB
```

nethogs的好处是能看到哪个进程在占用带宽——有时候带宽跑满了，不知道是谁干的，nethogs一眼就看出来。

**iptraf-ng**：更全面的流量监控

```bash
sudo apt install iptraf-ng
sudo iptraf-ng
```

提供了TCP、UDP、ICMP等各类流量的统计。

> **iptraf-ng 已比较老旧**，不少新版发行版（如 Ubuntu 24.04）的软件源里已经不再打包，安装可能失败。需要"按接口看总流量"时用 `nload`、`bmon`（`sudo apt install nload bmon`）；需要在浏览器/终端里看交互式流量图，iftop 和 nethogs 通常够用。

---

## 本章小结

本章我们掌握了Linux网络诊断的全套工具：

- **ping**：测试网络连通性，`-c`指定次数，`-i`指定间隔
- **traceroute**：追踪路由路径，`-I`用ICMP，`-T`用TCP
- **mtr**：ping和traceroute的结合体，实时统计，`-r`生成报告
- **nslookup**：DNS查询简单版，`-type=MX`查邮件记录
- **dig**：DNS查询详细版，`+trace`追踪完整查询路径
- **host**：DNS查询简化版，输出简洁
- **netstat**：查看网络状态（连接、端口、路由），`-tulpn`查看监听端口。**已过时且新系统默认不装**，能换就换 `ss`
- **ss**：netstat的现代替代品，更快更详细，`-tulpn`看监听、`-s`看统计、带引号的过滤表达式看指定连接
- **lsof**：查看进程打开的文件/socket，`-i :端口`查占用，多个条件要加 `-a` 才是"并且"
- **nc/netcat**：网络瑞士军刀，端口扫描、连接测试、文件传输
- **tcpdump**：命令行抓包，`-i`指定网卡，`-w`保存文件，`-r`读取文件
- **Wireshark**：图形化抓包分析，功能最强大
- **iftop/nethogs/nload**：实时流量监控工具（按连接/按进程/按接口）

遇到网络问题，建议按这个顺序排查：

1. **ping**：目标通不通？如果报"名称解析失败"，说明是 DNS 问题，先跳到第 3 步
2. **mtr / traceroute**：不通或很慢时，看是哪一跳出了问题（关注**最后一跳**的丢包和延迟）
3. **nslookup / dig / host**：域名解析出来的 IP 对不对
4. **ss / netstat / lsof**：服务端口有没有在正常监听，是哪个进程在监听
5. **tcpdump / Wireshark**：还查不出原因，就抓包看数据到底发出去了没有、有没有被拒绝

> 一个常见的误区：**ping 不通 ≠ 服务有问题**。很多服务器出于安全考虑禁用了 ICMP，但 HTTP/SSH 完全正常。判断服务是否可用，用 `curl -I http://地址` 或 `nc -zv 地址 端口` 更准确。
