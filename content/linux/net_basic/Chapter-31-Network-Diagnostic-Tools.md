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
- `ttl=118`：生存时间（Time To Live），每经过一个路由器减1，防止数据包在网络中无限循环。TTL=118说明到达目标经过了约7个路由器（初始值128减118=7跳）
- `time=12.3 ms`：往返延迟，12.3毫秒
- `0% packet loss`：丢包率，0%表示4个包全部收到，网络畅通
- `rtt min/avg/max/mdev`：往返时间统计（最小/平均/最大/标准差）

### 31.1.2 ping -i 0.2：间隔

`-i`参数控制ping包的发送间隔（秒）。

```bash
# 每0.2秒发一个包（快速ping，用于压力测试）
ping -c 10 -i 0.2 192.168.1.1

# 每5秒发一个包（减少网络负载）
ping -c 5 -i 5 www.baidu.com
```

```bash
# ping本机网关，测试本地网络是否正常
ping -c 4 192.168.1.1

# ping公网DNS，测试外网连接
ping -c 4 8.8.8.8

# ping域名（会先做DNS解析）
ping -c 4 www.baidu.com
```

**常见ping结果分析**：

| 结果 | 可能原因 |
|------|---------|
| `0% packet loss, time<1ms` | 极低延迟，本地网络或同机房通信 |
| `0% packet loss, time=10-50ms` | 正常互联网通信 |
| `0% packet loss, time>200ms` | 跨国或卫星通信，延迟较高 |
| `100% packet loss` | 目标不可达，可能是防火墙拦截了ICMP |
| `timeout` | 完全不通，网络路径断了或目标主机挂了 |

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
- 如果某个跳出现`* * *`，说明那个路由器不响应traceroute（可能是防火墙拦截）
- 如果某跳延迟突然飙升，说明那一段网络拥塞或路由不佳

### 31.2.2 traceroute -I：ICMP

默认情况下，Linux的`traceroute`使用UDP数据包，而Windows的`tracert`使用ICMP。

`-I`参数让`traceroute`使用ICMP包（和Windows的tracert一样）。

```bash
# 使用ICMP协议进行路由追踪
sudo traceroute -I www.baidu.com

# 使用TCP SYN进行追踪（穿透防火墙，部分管理员会封ICMP/UDP）
sudo traceroute -T -p 80 www.baidu.com
```

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

从上面结果看，第4跳（220.181.0.1）有10%的丢包率，说明问题可能出在这一段网络上。

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
Name:   www.baidu.com
Address: 220.181.38.149
Name:   www.baidu.com
Address: 220.181.38.150
```

解读：

- `Server: 8.8.8.8`：当前使用的DNS服务器是Google DNS
- `Non-authoritative answer`：非权威应答（说明这个答案是DNS服务器缓存返回的，不是baidu.com的权威DNS服务器直接回答的）
- `www.baidu.com`有两个IP：220.181.38.149和220.181.38.150——百度做了负载均衡

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

**常见DNS记录类型**：

| 类型 | 说明 | 用途 |
|------|------|------|
| A | IPv4地址 | 域名指向IPv4地址 |
| AAAA | IPv6地址 | 域名指向IPv6地址 |
| MX | 邮件交换 | 指定邮件服务器 |
| CNAME | 别名 | 域名别名 |
| NS | 域名服务器 | 指定该域名的DNS服务器 |
| TXT | 文本记录 |  SPF、DKIM验证等 |

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
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

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

- `QUESTION SECTION`：查询的问题（查询www.baidu.com的A记录）
- `ANSWER SECTION`：查询结果（www.baidu.com是CNAME别名，指向www.a.shifen.com，后者有两个A记录IP）
- `TTL 600`：缓存生存时间600秒
- `Query time: 12 msec`：查询耗时12毫秒
- `SERVER: 8.8.8.8#53`：使用的DNS服务器

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
```

## 31.6 host 命令：简单的 DNS 查询

`host`是DNS查询的"简化版"，输出比`dig`简洁，适合快速查看。

```bash
# 安装host（部分最小化安装没有）
sudo apt install dnsutils

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

## 31.7 netstat 命令：网络状态统计

`netstat`（Network Statistics）是查看网络连接、路由表、接口统计的经典工具。虽然逐渐被`ss`取代，但仍然是很多老系统的标配。

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
- `-p`：显示占用端口的进程
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
netstat -an | head -20
```

```bash
Active Internet connections (established and bound to wildcard addresses)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0     36 192.168.1.100:22        203.0.113.50:54321      ESTABLISHED
tcp        0      0 127.0.0.1:3306          127.0.0.1:45678         TIME_WAIT
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN
```

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

### 31.8.2 ss -s：统计

`-s`参数显示各类socket的统计摘要。

```bash
ss -s
```

```bash
Total: 138 (kernel 0)
TCP:   12 (estab 1, closed 2, orphaned 0, synrecv 0, timewait 2)

Local Address:Port    Peer Address:Port
192.168.1.100:22      203.0.113.50:54321
192.168.1.100:22      203.0.113.51:54322

TCP ESTABLISHED: 1     # 当前有1个已建立的SSH连接
TCP TIME_WAIT: 2       # 有2个连接处于TIME_WAIT状态
```

**ss的高级过滤**：

```bash
# 查看所有已建立的SSH连接
ss state established '( dport = :22 or sport = :22 )'

# 查看所有到80端口的连接
ss dst :80

# 查看所有来自特定IP的连接
ss src 203.0.113.50
```

## 31.9 lsof 命令：查看端口占用

`lsof`（List Open Files）可以查看所有打开的文件和socket，网络连接也是一种"文件"。

### 31.9.1 lsof -i :80

查看哪个进程占用了80端口。

```bash
sudo lsof -i :80
```

```bash
COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
apache2  4567   root    4u  IPv6 123456      0t0  TCP *:http (LISTEN)
apache2  7890 www-data    4u  IPv6 123456      0t0  TCP *:http (LISTEN)
nginx   10111   root    6u  IPv4 234567      0t0  TCP *:http (LISTEN)
```

输出解读：

- `COMMAND`：进程名（apache2、nginx）
- `PID`：进程ID
- `USER`：运行用户
- `TYPE`：socket类型（IPv4/IPv6）
- `STATE`：状态（LISTEN监听）

### 31.9.2 lsof -p PID

查看指定进程打开了哪些文件/socket。

```bash
# 查看SSH进程打开的所有文件
sudo lsof -p 1234

# 查看某个用户打开的所有网络连接
sudo lsof -i -u www-data
```

```bash
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd    1234       root  cwd    DIR  253,0    4096    2 /
sshd    1234       root    3u  IPv4  12345      0t0  TCP *:ssh (LISTEN)
sshd    1234       root    4u  IPv6  12346      0t0  TCP *:ssh (LISTEN)
```

## 31.10 nc/netcat 命令：网络瑞士军刀

`nc`（netcat）是网络工具中的"瑞士军刀"，可以用作端口扫描、连接测试、文件传输、代理等。

### 31.10.1 nc -zv 主机 端口

测试某个主机的某个端口是否开放（不建立完整连接，只测试）。

```bash
# 测试80端口是否开放
nc -zv 192.168.1.1 80

# 测试多个端口
nc -zv 192.168.1.1 22 80 443

# 端口扫描（1-1000范围）
nc -zv 192.168.1.1 1-1000
```

```bash
Connection to 192.168.1.1 80 port [tcp/http] succeeded!
```

`-z`：zero-I/O模式，只测试连接，不发送数据
`-v`：verbose，输出详细信息

### 31.10.2 nc -l 端口：监听

在一台机器上启动监听，另一台机器连接过来——可以用于简单的聊天或文件传输。

```bash
# 机器A：在本机1234端口启动监听
nc -l 1234

# 机器B：连接到机器A的1234端口
nc 机器A的IP 1234

# 现在两台机器可以直接打字聊天了
```

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
# 捕获5分钟的数据包，保存到capture.pcap
sudo tcpdump -i eth0 -w capture.pcap -G 300

# 捕获1000个包后停止，保存到文件
sudo tcpdump -i eth0 -w capture.pcap -c 1000

# 读取保存的pcap文件
sudo tcpdump -r capture.pcap

# 只显示HTTP流量
sudo tcpdump -r capture.pcap 'port 80'

# 只显示HTTPS流量
sudo tcpdump -r capture.pcap 'port 443'
```

**常用过滤表达式**：

```bash
# 只抓ICMP包（ping包）
sudo tcpdump -i eth0 icmp

# 只抓来自192.168.1.100的包
sudo tcpdump -i eth0 src 192.168.1.100

# 只抓发往80端口的包
sudo tcpdump -i eth0 dst port 80

# 抓HTTP GET请求
sudo tcpdump -i eth0 'port 80 and tcp[20:4] = 0x47455420'
```

## 31.12 Wireshark：图形化抓包分析

Wireshark是世界上最流行的网络协议分析器，图形界面，操作直观。`tcpdump`擅长在服务器上抓包，`Wireshark`擅长在PC上分析抓包结果。

```bash
# Linux上安装Wireshark（需要图形环境）
sudo apt install wireshark

# 如果想非root用户运行，需要配置
sudo usermod -aG wireshark $USER
# 重新登录后生效
```

Wireshark的核心功能：

- 实时抓包，边抓边看
- 过滤表达式（比tcpdump更强大）
- 追踪TCP流（Follow TCP Stream）
- 解密HTTPS流量（需要SSLKEYLOGFILE）
- 专家信息分析（自动诊断网络问题）

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

---

## 本章小结

本章我们掌握了Linux网络诊断的全套工具：

- **ping**：测试网络连通性，`-c`指定次数，`-i`指定间隔
- **traceroute**：追踪路由路径，`-I`用ICMP，`-T`用TCP
- **mtr**：ping和traceroute的结合体，实时统计，`-r`生成报告
- **nslookup**：DNS查询简单版，`-type=MX`查邮件记录
- **dig**：DNS查询详细版，`+trace`追踪完整查询路径
- **host**：DNS查询简化版，输出简洁
- **netstat**：查看网络状态（连接、端口、路由），`-tulpn`查看监听端口
- **ss**：netstat的现代替代品，更快更详细，`-s`显示统计
- **lsof**：查看进程打开的文件/socket，`-i :端口`查占用
- **nc/netcat**：网络瑞士军刀，端口扫描、连接测试、文件传输
- **tcpdump**：命令行抓包，`-i`指定网卡，`-w`保存文件，`-r`读取文件
- **Wireshark**：图形化抓包分析，功能最强大
- **iftop/nethogs/iptraf**：实时流量监控工具

遇到网络问题，诊断思路：先ping（通不通）→ traceroute（哪一跳慢）→ nslookup/dig（DNS正常吗）→ netstat/ss（端口开着吗）→ tcpdump（抓包看细节）。
