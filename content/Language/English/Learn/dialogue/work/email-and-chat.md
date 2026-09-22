+++
title = "邮件与即时消息：Slack/Teams 上的日常沟通"
linkTitle = "邮件与即时消息"
date = 2026-09-21T23:40:00+08:00
weight = 4
type = "docs"
description = "美式英语口语对话：Slack 与邮件五个细化场景——第一条消息就说正事、请人 review、催进度、礼貌拒绝加活、写一封让上司一眼看懂的周报邮件，英中对照，含线程与频道礼仪说明"
isCJKLanguage = true
categories = ["English", "口语"]
tags = ["英语口语", "场景对话", "职场英语", "邮件与即时消息", "Slack", "美式英语"]
draft = false
+++
在美国公司，**Slack / Teams 承担了过去"走到工位上说一句"的全部功能**。一天几十上百条消息：同步进展、催 review、@人、甩文档链接、临时改会议时间。写得好，你显得专业、靠谱、好合作；写得不好，要么没人回你，要么回你的人心里在翻白眼。

中国同事在消息沟通上最常见的三个问题：

| 问题 | 表现 | 后果 |
| --- | --- | --- |
| 铺垫太长 | `Hi, how are you? I hope you're well. I have a question…` | 对方不知道你要什么，先搁着 |
| 不说要什么 | `The build is failing.` | 对方回 `Okay?`，来回三轮才说清 |
| 催得太软或太硬 | `Sorry to bother you again…` / `Why no reply?` | 前者被忽略，后者得罪人 |

三条基本规则：

- **第一条消息就说正事。** 不要 `Hi` 等回复——在美国职场，**发 `Hi` 然后等对方回应再说是坏习惯**（这叫 `nohello`），正确做法是打招呼和正事写在同一条消息里。
- **说清你要对方做什么。** `Can you take a look?` 比 `There's a problem` 有效十倍。
- **催进度要给时间点，不要问"怎么样了"。** `Any update on this? I need it by Thursday.` 比 `Any news?` 好得多。

**线程（thread）是硬礼仪。** 在频道里回复要用 thread，不要开新消息，否则整个频道会被你的对话刷屏。**@人（mention）要克制**：`@channel` 是"所有人放下手里的活"级别的打扰，除了真事故不要用。

## 第一条消息就说正事：请人 review 一段代码
**Marcus**（资深工程师，你们不在同一个组，只有过几面之缘）
**You**（后端工程师，PR 挂了三天没人看）

*（周二上午十点，Slack 私聊。你的第一条消息）*

---

**You: Hey Marcus — PR #4821 is ready for review whenever you get a chance. It's the export chunking change we talked about. No rush, but I'd like to merge by Thursday.**

💬 你： 嗨 Marcus——PR #4821 有空的时候帮忙看一下。就是上次聊的导出分块改动。不急，不过我想周四之前合进去。

**Marcus: Hey. How big is it?**

💬 马库斯： 嗨。改动大吗？

**You: About 200 lines, one file. Most of it's the new windowing function.**

💬 你： 大概两百行，一个文件。大部分是新的分窗函数。

**Marcus: Okay, that's manageable. Anything I should look at specifically?**

💬 马库斯： 好，那还行。有什么需要我特别看的吗？

**You: Yeah — the boundary logic. I want a second opinion on whether the half-open interval is right.**

💬 你： 有——边界逻辑。我想让人确认一下半开区间对不对。

**Marcus: Good, that's the part that breaks. I'll take a look after standup.**

💬 马库斯： 好，那正是会出问题的地方。我站会之后看。

**You: Thanks. Also, heads-up — the diff is easier to read if you hide whitespace. There's a reformat in there.**

💬 你： 谢谢。另外提醒一下——把空白变更隐藏了更好读。里面有一次格式化。

**Marcus: Oh, good to know. That's why the line count looked high.**

💬 马库斯： 哦，还好说了。难怪行数看着多。

*（两小时后）*

**Marcus: Left three comments. Two are nits, one's real.**

💬 马库斯： 留了三条评论。两条是小问题，一条是真的。

**You: Which one's real?**

💬 你： 哪条是真的？

**Marcus: The one about the timezone. You're using local time in the window calculation.**

💬 马库斯： 时区那条。你在窗口计算里用了本地时间。

**You: Oh no. That's a real bug.**

💬 你： 哦不。那是真 bug。

**Marcus: Yeah. Everything else looks good.**

💬 马库斯： 对。其他都没问题。

**You: Fixed and pushed. Can you re-approve when you get a sec?**

💬 你： 改好推上去了。有空的时候能再批一下吗？

**Marcus: Approved. Nice work on the tests, by the way.**

💬 马库斯： 批了。顺便说，测试写得不错。

**You: Thanks — that means a lot coming from you.**

💬 你： 谢谢——你这么说我很受用。

---

### 这一幕的核心句型

| 英文 | 中文 | 备注 |
| --- | --- | --- |
| PR #4821 is ready for review whenever you get a chance. | PR #4821 有空的时候帮忙看一下。 | **请求 + 时间弹性写在同一句** |
| No rush, but I'd like to merge by Thursday. | 不急，不过我想周四之前合进去。 | **给弹性，也给时间点** |
| How big is it? | 改动大吗？ | 评审人第一句会问的 |
| Anything I should look at specifically? | 有什么需要我特别看的吗？ | **主动缩小对方的阅读范围** |
| I want a second opinion on … | 我想让人确认一下…… | 求复核的说法 |
| I'll take a look after standup. | 我站会之后看。 | 给时间预期 |
| Heads-up — the diff is easier to read if you hide whitespace. | 提醒一下——隐藏空白变更更好读。 | **减少对方的工作量** |
| Two are nits, one's real. | 两条是小问题，一条是真的。 | nit = 吹毛求疵的小意见 |
| Fixed and pushed. | 改好推上去了。 | 极简的进展同步 |
| Can you re-approve when you get a sec? | 有空能再批一下吗？ | 二次请求 |
| Nice work on the tests. | 测试写得不错。 | 具体的表扬 |
| That means a lot coming from you. | 你这么说我很受用。 | **接受表扬的得体说法** |

### 中式英语纠正

| 常见错法 | 问题 | 改成 |
| --- | --- | --- |
| `Hi, are you there?` | 发完等回复，浪费对方一个来回 | `Hey — quick one about PR #4821: …` |
| `Sorry to bother you, I know you are busy.` | 先道歉，重点被推到后面 | `PR #4821 is ready for review — no rush.` |
| `Please review my code.` | 没说是什么、多大、什么时候要 | `PR #4821 is ready — 200 lines, one file. Need it by Thursday.` |
| `Could you check it? It is very important.` | important 是主观判断，对方无感 | `The boundary logic is the part I want checked.` |
| `Why you didn't reply?` | 语法错且像在质问 | `Following up on this — any update?` |
| `Thanks for your help, sorry for the trouble.` | 感谢和道歉混在一起 | `Thanks — appreciate you looking at it.` |

### 口语小注

**1. 打招呼和正事要写在同一条消息里。**

`Hey Marcus —` 后面直接接正事，**不要分成两条**。分开写的话，对方看到 `Hey` 会等你说下文，而你可能在打字——这一个来回就浪费掉了。美国工程团队管这个叫 `nohello` 原则。

**2. 请求里必须包含三样东西：是什么、多大、什么时候要。**

`PR #4821 is ready for review` 不够，要加上 `200 lines, one file` 和 `by Thursday`。**没有时间和规模，对方无法排优先级**，你的请求就会被无限延后。

**3. 主动告诉对方哪里不用看。**

`Most of it's the new windowing function`、`hide whitespace`——这些话**减少了对方的工作量**，会显著提高你的 review 被优先处理的概率。中国的同事常常觉得"我把东西给你了，你自己看"，在美国这个习惯会让你排在队尾。

**4. `nit` 是"小意见，可以不改"。**

评审里说 `That's a nit` 意思是"这点我觉得可以更好，但不影响功能，你自己决定"。**看到 nit 不用紧张，也不用每条都改**；反过来，你自己评审别人代码时，把吹毛求疵的意见明确标成 nit，是很受欢迎的做法。

## 催进度：给时间点，不要问"怎么样了"
**Priya**（产品经理，你等她的需求确认）
**You**（后端工程师，被这个确认卡了两天）
**Dave**（你的经理，在邮件里被抄送）

*（周四下午，Slack 私聊 + 一封邮件）*

---

**You: Hey Priya — following up on the spec question from Tuesday. I'm blocked on the response format.**

💬 你： 嗨 Priya——跟进一下周二那个规格问题。我卡在返回格式上了。

**Priya: Oh, sorry. Which one again?**

💬 普里娅： 哦，抱歉。哪个来着？

**You: Whether the export returns a download link or the file itself. I asked Tuesday morning.**

💬 你： 导出是返回下载链接还是文件本身。我周二上午问的。

**Priya: Right. I need to check with the customer.**

💬 普里娅： 对。我得跟客户确认。

**You: Got it. When do you think you'll know? I need to build against one of them by Monday.**

💬 你： 好。你觉得什么时候能有答案？我周一之前得按其中一个来开发。

**Priya: I can ask them today. So probably tomorrow.**

💬 普里娅： 我今天能问。那大概明天。

**You: Tomorrow works. And if it's not settled by Friday, can we just pick one and change it later?**

💬 你： 明天可以。如果周五还没定，我们能不能先选一个，以后再改？

**Priya: Yeah, let's do that. Download link is easier for me.**

💬 普里娅： 行，就这么办。下载链接对我更简单。

**You: Download link it is. I'll start on that. Thanks.**

💬 你： 那就下载链接。我开始做。谢谢。

*（十分钟后，你补了一封邮件，抄送 Dave）*

*（邮件）* **You: Subject: Export format — going with download link**

💬 你： *（邮件）* 主题：导出格式——采用下载链接

*（邮件）* **You: Hi Priya, quick recap so we're aligned. We're going with the download link approach. I'll start building today and can switch later if the customer pushes back. No action needed from you — just flagging it. Thanks, Wei**

💬 你： *（邮件）* Priya 你好，简单同步一下确保一致。我们采用下载链接方案。我今天开始开发，如果客户有异议以后再换。你这边不需要做什么——就是同步一下。谢谢，Wei

*（邮件）* **Dave: Thanks for the recap. One question — does the switch cost us a day if it happens?**

💬 戴夫： *（邮件）* 谢谢同步。问一句——如果真要换，会多花一天吗？

*（邮件）* **You: Half a day, maybe. The response shape is behind a flag, so it's a config change.**

💬 你： *（邮件）* 大概半天。返回结构放在开关后面，所以是改配置。

*（邮件）* **Dave: Then that's the right call. Move on.**

💬 戴夫： *（邮件）* 那这个决定对。继续。

*（Slack）* **Priya: Thanks for writing that up. I hate when decisions live only in Slack.**

💬 普里娅： *（Slack）* 谢谢写下来。我最怕决定只活在 Slack 里。

**You: Same. I always forget what we agreed to.**

💬 你： 我也是。我老是忘了当时说定的是什么。

---

### 这一幕的核心句型

| 英文 | 中文 | 备注 |
| --- | --- | --- |
| Following up on the spec question from Tuesday. | 跟进一下周二那个规格问题。 | **催进度的标准开场** |
| I'm blocked on the response format. | 我卡在返回格式上了。 | blocked on = 卡在某个点 |
| Which one again? | 哪个来着？ | 对方忘了时的正常反应 |
| When do you think you'll know? | 你觉得什么时候能有答案？ | **问时间点，不问"怎么样了"** |
| I need to build against one of them by Monday. | 我周一之前得按其中一个来开发。 | 说清你的截止压力 |
| If it's not settled by Friday, can we just pick one? | 周五还没定的话，能不能先选一个？ | **给出解套方案** |
| Download link it is. | 那就下载链接。 | 干脆地确认 |
| Quick recap so we're aligned. | 简单同步一下确保一致。 | **邮件开场的标准句** |
| No action needed from you — just flagging it. | 你不需要做什么——就是同步一下。 | 说明这不是请求 |
| Does the switch cost us a day? | 换的话会多花一天吗？ | 上司会问的代价问题 |
| It's behind a flag, so it's a config change. | 放在开关后面，是改配置。 | 说明成本很低 |
| Then that's the right call. | 那这个决定对。 | 认可判断 |
| I hate when decisions live only in Slack. | 我最怕决定只活在 Slack 里。 | 真实痛点 |

### 中式英语纠正

| 常见错法 | 问题 | 改成 |
| --- | --- | --- |
| `Any update?` | 太笼统，对方回一句"还没有"就没下文了 | `Following up on this — when do you think you'll know?` |
| `Sorry to rush you, but have you checked?` | 道歉 + 质问，两头不讨好 | `I'm blocked on this — any sense of timing?` |
| `Why is it taking so long?` | 像在指责，对话会变成防御 | `I need to build against one by Monday.` |
| `Please reply to me as soon as possible.` | 命令语气，且 ASAP 已经被用烂了 | `Tomorrow works for me.` |
| `I am waiting for you.` | 把责任全推给对方 | `I'm blocked on your answer.` |
| `Let me know your decision.` | 把球丢回去，没有给方案 | `If it's not settled by Friday, can we pick one and change later?` |

### 口语小注

**1. 催进度要问"什么时候"，不要问"怎么样了"。**

`Any update?` 得到的回答永远是 `Not yet`；**`When do you think you'll know?` 逼出一个具体时间**，而且对方一旦说了时间，就等于做了承诺。这是催进度最有效的一个句式。

**2. 说自己被卡住，比说别人慢有效。**

`I'm blocked on this` 是把问题描述成客观状态；`You haven't replied` 是评价对方。**前者对方会来帮你，后者对方会来解释。**

**3. `No action needed from you — just flagging it` 是极好用的邮件收尾。**

它明确定义了**这封邮件是通知，不是请求**，对方读完就可以放下。**没有这句话，收件人会不确定要不要回复你**，然后这封邮件就挂在那里了。

**4. 重要决定一定要从 Slack 落到邮件或文档。**

Slack 消息会被刷走，搜索也难。**`Quick recap so we're aligned`** 这封邮件的作用是**留下书面记录**——Priya 那句 `I hate when decisions live only in Slack` 说明这是所有人的共识。

## 礼貌拒绝加活：手上真的满了
**Dave**（你的经理，在 Slack 上直接甩了一个新需求过来）
**You**（这周已经排满，手上有两个交付）

*（周三下午四点，Slack 私聊）*

---

**Dave: Hey — can you take on the audit log work? Legal wants it this quarter.**

💬 戴夫： 嗨——你能接一下审计日志那个活吗？法务想这个季度要。

**You: Possibly. Can I ask what the deadline is and how big we think it is?**

💬 你： 可能可以。能问一下截止时间，还有大概多大吗？

**Dave: End of the month. Maybe a week of work.**

💬 戴夫： 月底。大概一周的活。

**You: Okay. Then I need to be straight with you — I've got the export ship and the billing migration both landing this month. I can't do all three well.**

💬 你： 好。那我得跟你说实话——导出上线和计费迁移都在这个月落。三件我都做好是做不到的。

**Dave: Okay. What would you drop?**

💬 戴夫： 好。你会砍掉哪个？

**You: I wouldn't drop either. I'd push the audit log to early next month.**

💬 你： 哪个我都不想砍。我想把审计日志推到下个月初。

**Dave: Legal's asking for end of month.**

💬 戴夫： 法务要的是月底。

**You: Then I'd want to know if it's a hard date or a preferred one. If it's hard, I need someone to take part of the billing migration.**

💬 你： 那我想知道那是硬日期还是期望日期。如果是硬的，我需要有人接走计费迁移的一部分。

**Dave: Fair. Let me ask legal. If it's soft, we do it next month.**

💬 戴夫： 有道理。我去问法务。如果是软的，就下个月做。

**You: Thanks. And if it turns out to be hard, I'd rather know now than in two weeks.**

💬 你： 谢谢。如果最后发现是硬的，我宁愿现在知道，而不是两周后。

**Dave: Agreed. I'll come back to you tomorrow.**

💬 戴夫： 同意。我明天回复你。

*（第二天上午）*

**Dave: Legal says it's a preferred date. So — next month is fine.**

💬 戴夫： 法务说那是期望日期。所以下个月可以。

**You: Great. Put it on my list for the first week.**

💬 你： 好。放我第一周的清单里。

**Dave: Done. And thanks for pushing back instead of just saying yes.**

💬 戴夫： 好。另外谢谢你提出异议，而不是直接答应下来。

**You: I learned that one the hard way at my last job.**

💬 你： 这个我上一份工作是吃了亏才学会的。

**Dave: Everybody does. Okay — go ship the export.**

💬 戴夫： 大家都一样。好——去把导出上线吧。

---

### 这一幕的核心句型

| 英文 | 中文 | 备注 |
| --- | --- | --- |
| Can you take on the audit log work? | 你能接一下审计日志那个活吗？ | 加活的标准问法 |
| Possibly. Can I ask what the deadline is? | 可能可以。能问截止时间吗？ | **不立刻答应，先问信息** |
| I need to be straight with you. | 我得跟你说实话。 | 要说不之前先声明 |
| I've got X and Y both landing this month. | X 和 Y 都在这个月落。 | 用事实说明容量 |
| I can't do all three well. | 三件我都做好是做不到的。 | **拒绝的是质量，不是工作** |
| What would you drop? | 你会砍掉哪个？ | 上司的标准反问 |
| I wouldn't drop either. I'd push X. | 哪个都不想砍，我想推 X。 | 给方案而不是给问题 |
| Is it a hard date or a preferred one? | 那是硬日期还是期望日期？ | **最有用的一句追问** |
| I need someone to take part of the migration. | 我需要有人接走迁移的一部分。 | 提出资源需求 |
| Let me ask legal. | 我去问法务。 | 上司接住了 |
| I'd rather know now than in two weeks. | 我宁愿现在知道，而不是两周后。 | 说明为什么要提前确认 |
| Thanks for pushing back instead of just saying yes. | 谢谢你提出异议，而不是直接答应。 | **最好的反馈** |
| I learned that one the hard way. | 这个是吃了亏才学会的。 | 自嘲式认同 |

### 中式英语纠正

| 常见错法 | 问题 | 改成 |
| --- | --- | --- |
| `Okay, I will try my best.` | 答应了做不完，最后两头失信 | `Possibly — can I ask about the deadline first?` |
| `I am too busy, I cannot do it.` | 直接说不能，没给理由也没给方案 | `I've got two things landing this month — here are the options.` |
| `This is not my job.` | 划界限但姿态对抗 | `I can't fit it in this month without dropping something.` |
| `Maybe next month?` | 太软，等于拖延，上司不会当真 | `I'd push it to early next month — here's why.` |
| 默默接下，然后熬夜 | 短期看起来负责，长期是项目风险 | 现在就提出取舍，让上司决定 |
| `Sorry, I know I am slow.` | 把容量问题说成能力问题 | `I'd rather do two things well than three badly.` |

### 口语小注

**1. 拒绝加活的正确姿势：先问信息，再给取舍。**

`Can I ask what the deadline is and how big we think it is?` 这一步不能省。**没有信息就拒绝，是情绪；有了信息再谈，是排期。**

**2. `I can't do all three well` 比 `I can't do it` 高明得多。**

它拒绝的不是工作，是**质量不达标**。**任何经理都不会说"你就做得差一点吧"**，所以这句话几乎必然引出下一步讨论——也就是你想要的排期调整。

**3. `Is it a hard date or a preferred one?` 是整场对话里最值钱的一句。**

美国职场里大量的"截止日期"其实是**期望日期**。**问一句就可能有惊喜**（这次就推掉了一整个月）。同类问法：`Is that a real deadline, or a target?`、`Who's actually waiting on this?`

**4. 好的上司会感谢你提出异议。**

`Thanks for pushing back instead of just saying yes` 不是客套——**默默答应然后做不完，是团队里代价最高的一种"配合"**。宁可现在谈，也不要两周后崩。

## 一封让上司一眼看懂的周报邮件
**Dave**（你的经理，每周五收全组周报）
**Priya**（产品经理，被抄送）
**You**（第一次写周报，上周写得太长被提醒过）

*（周五下午四点，你写周报邮件。下面是邮件正文 + 周一 Dave 的回复）*

---

*（邮件）* **You: Subject: Wei — weekly update, week of Oct 6**

💬 你： *（邮件）* 主题：Wei — 周报，10 月 6 日这周

*（邮件）* **You: Hi Dave, three lines this week.**

💬 你： *（邮件）* Dave 你好，这周三行。

*（邮件）* **You: Shipped: export chunking is live as of Thursday. Totals match, no errors over the weekend.**

💬 你： *（邮件）* 已上线：导出分块周四上线。数字对上，周末无报错。

*（邮件）* **You: In progress: billing migration, 3 of 5 services done. Blocked on the billing team's schema change — I've pinged them twice.**

💬 你： *（邮件）* 进行中：计费迁移，五个服务做完三个。卡在计费组的表结构变更——我催过两次了。

**You: *(邮件）* Next week: audit log scoping, and I'll unblock the migration one way or another by Wednesday.**

💬 你： *（邮件）* 下周：审计日志的方案梳理，另外我会在周三之前把迁移的阻塞解决掉，不管用什么办法。

*（邮件）* **You: One ask: I need 30 minutes with the billing lead. Can you help me get on his calendar? Thanks, Wei**

💬 你： *（邮件）* 一个请求：我需要跟计费组的 lead 聊三十分钟。能帮我排进他的日程吗？谢谢，Wei

*（周一早上，邮件回复）*


*（邮件）* **Dave: This is exactly right. Three sections, one ask.**

💬 戴夫： *（邮件）* 这封写得正好。三个部分，一个请求。

*（邮件）* **Dave: I put you on his calendar for Tuesday. Also — the "no errors over the weekend" line is the part I care about most. Keep that.**

💬 戴夫： *（邮件）* 我把你排进他周二的时间了。另外——"周末无报错"那句是我最关心的。保持这个。

*（邮件）* **You: Will do. Is the "one ask" thing a rule?**

💬 你： *（邮件）* 好。这个"一个请求"是规矩吗？

*（邮件）* **Dave: It's a habit. If you send me five asks, I do zero of them.**

💬 戴夫： *（邮件）* 是习惯。你要是给我五个请求，我一个都不会做。

*（邮件）* **You: Fair. Noted.**

💬 你： *（邮件）* 有道理。记下了。

*（Slack 上，Priya 也回了）*

**Priya: Hey — saw your weekly. That's the first update I've been able to read in ten seconds.**

💬 普里娅： 嗨——看到你的周报了。这是我第一次十秒内能读完的更新。

*（laughs）* **You: My last one was a wall of text.**

💬 你： *（笑）* 我上次写的是一堵文字墙。

**Priya: I know. I didn't read it.**

💬 普里娅： 我知道。我没读。

*（laughs）* **You: That's fair. I'd have done the same.**

💬 你： *（笑）* 有道理。我也会一样。

**Priya: The "blocked on" line is the useful one. That's how I knew to chase billing.**

💬 普里娅： "卡在"那句最有用。我就是看到那句才去催计费组的。

**You: Oh — I didn't know you saw it.**

💬 你： 哦——我不知道你也看到了。

**Priya: I'm on the thread. Everyone reads the blocked section.**

💬 普里娅： 我在邮件链里。所有人都只看"卡住"那部分。

---

### 这一幕的核心句型

| 英文 | 中文 | 备注 |
| --- | --- | --- |
| Three lines this week. | 这周三行。 | **给周报定一个长度承诺** |
| Shipped: … | 已上线：…… | 周报第一段 |
| In progress: … | 进行中：…… | 周报第二段 |
| Blocked on … | 卡在…… | **周报里最被认真读的一行** |
| Next week: … | 下周：…… | 周报第三段 |
| One ask: … | 一个请求：…… | **只提一个请求** |
| Can you help me get on his calendar? | 能帮我排进他的日程吗？ | 具体、可执行的请求 |
| That's the part I care about most. | 那是我最关心的部分。 | 上司的反馈 |
| Is that a rule? | 这是规矩吗？ | 确认惯例 |
| It's a habit. | 是习惯。 | 简洁的回答 |
| If you send me five asks, I do zero of them. | 你给我五个请求，我一个都不做。 | **值得记一辈子** |
| That's the first update I've been able to read in ten seconds. | 这是我第一次十秒内读完的更新。 | 高评价 |
| I didn't read it. | 我没读。 | 美国同事的直接 |
| Everyone reads the blocked section. | 所有人都只看"卡住"那部分。 | 内部真相 |

### 中式英语纠正

| 常见错法 | 问题 | 改成 |
| --- | --- | --- |
| 写一整篇叙述性长文 | 上司不会读，等于没写 | 三段式：已做 / 在做 / 卡住 |
| `I worked on the migration this week.` | worked on 没有信息量 | `3 of 5 services done. Blocked on the schema change.` |
| `I am trying my best to finish it.` | 表态度，不表进度 | `On track for Thursday.` |
| 把五件事都写成一个请求 | 对方一个都不会做 | 只留一个 ask，其余放下周 |
| `Sorry for the long email.` | 明知长还发，道歉没用 | 直接删到三行 |
| `Please give me your feedback.` | 太笼统，上司不知道回什么 | `Can you help me get on his calendar?` |

### 口语小注

**1. 周报的三段式：已做 / 在做 / 卡住。**

`Shipped`、`In progress`、`Blocked on`——**这三行能让上司十秒读完**。想加计划就再加一行 `Next week`，**不要写成记叙文**。Dave 说 `Three sections, one ask` 就是这个格式。

**2. `Blocked on` 那一行是周报里唯一会被认真读的部分。**

Priya 的话说明了真相：**所有人都只看"卡住"那部分**，因为那是需要别人动手的地方。所以卡住的事一定要写具体：`Blocked on the billing team's schema change — I've pinged them twice.`

**3. 一封邮件只提一个请求。**

`If you send me five asks, I do zero of them.` 这是美国管理者的普遍心理。**把最重要的那一个放在邮件最后，其余留到下封**——这不是效率技巧，是对方注意力的现实。

**4. 报结果要带"证据"。**

`No errors over the weekend` 比 `It's working well` 有力得多。**能带数字就带数字**：`totals match`、`3 of 5 done`、`two customers`。**上司信任的是可核对的句子。**

## 频道礼仪：@人、开线程、别刷屏
**Kevin**（隔壁组同事，热心但不太看频道规则）
**You**（在 #platform-help 频道值班，负责回答平台相关问题）
**Dana**（频道维护者，平台组的 tech lead）

*（周四上午，#platform-help 频道，一小时内二十几条消息）*

---

**Kevin: @channel hey everyone, quick question about the deploy pipeline**

💬 凯文： @channel 大家好，快速问一个部署流水线的问题

**Dana: Kevin — can you drop the @channel? It pings 80 people.**

💬 达娜： Kevin——能把 @channel 去掉吗？它会 ping 八十个人。

**Kevin: My bad. I'll just ask here then. So our deploy is failing with a permissions error.**

💬 凯文： 我的错。那我就在这儿问吧。我们的部署报权限错误失败了。

**You: What's the error code?**

💬 你： 错误码是什么？

**Kevin: 403\. It worked yesterday.**

💬 凯文： 403。昨天还好好的。

**You: Can you paste the full message? And which repo?**

💬 你： 能把完整信息贴出来吗？还有哪个仓库？

*（pastes a 30-line log into the channel）*


**Dana: Kevin, thread please. That's half the channel now.**

💬 达娜： Kevin，请用线程。这占了半个频道了。

**Kevin: Sorry, still learning the rules here.**

💬 凯文： 抱歉，我还在学这儿的规矩。

**Dana: No worries. Rule of thumb: if it's about your thing, it goes in a thread.**

💬 达娜： 没事。大致原则是：跟你自己的事有关的，放线程里。

*（in the thread）* **You: Okay, I see it. You're using a token that expired. It's the CI token, not your personal one.**

💬 你： *（在线程里）* 好，我看到了。你用的 token 过期了。是 CI 的 token，不是你个人的。

**Kevin: Oh. How do I refresh it?**

💬 凯文： 哦。怎么刷新？

**You: There's a doc. I'll link it. *(links the doc)***

💬 你： 有个文档。我把链接发你。（发了链接）

**Kevin: Got it, thanks. That was fast.**

💬 凯文： 收到，谢谢。挺快的。

**You: No problem. And — one thing for next time — for a permissions question, ask in #platform-help, not in #general. That's the whole point of this channel.**

💬 你： 不客气。还有——下次注意一点——权限的问题在 #platform-help 问，不要在 #general。这个频道就是干这个的。

**Kevin: Yeah, noted.**

💬 凯文： 好，记下了。

*（下午，Dana 私聊你）*

**Dana: Hey, thanks for handling Kevin. You did it without making him feel stupid.**

💬 达娜： 嗨，谢谢处理 Kevin 那事。你没让他觉得难堪。

**You: He's new. I was worse my first month.**

💬 你： 他是新人。我第一个月更糟。

**Dana: You were. You @channel'd the whole company.**

💬 达娜： 你确实是。你 @channel 了全公司。

*（laughs）* **You: I did. Twice.**

💬 你： *（笑）* 对。两次。

**Dana: Anyway — I'm writing it up as a pinned post. Want to review it before I post?**

💬 达娜： 总之——我想把这写成置顶帖。发之前你要看一下吗？

**You: Sure. Can I add one thing?**

💬 你： 行。我能加一条吗？

**Dana: Go ahead.**

💬 达娜： 说。

**You: "If you're not sure which channel, ask in the smallest one." That's the rule I actually use.**

💬 你： "如果你不确定该发哪个频道，就发最小的那个。"这是我实际在用的规则。

**Dana: That's better than what I wrote. I'm using that.**

💬 达娜： 这个比我写的那个好。我用了。

---

### 这一幕的核心句型

| 英文 | 中文 | 备注 |
| --- | --- | --- |
| Quick question about … | 快速问一个…… | 频道提问的标准开场 |
| Can you drop the @channel? It pings 80 people. | 能把 @channel 去掉吗？它会 ping 八十个人。 | **指出问题 + 说明后果** |
| My bad. | 我的错。 | 最轻的道歉 |
| Can you paste the full message? | 能把完整信息贴出来吗？ | 求上下文 |
| Thread please. | 请用线程。 | 最简短的频道提醒 |
| That's half the channel now. | 这占了半个频道了。 | 说明为什么要用线程 |
| Still learning the rules here. | 我还在学这儿的规矩。 | 新人的得体回应 |
| Rule of thumb: … | 大致原则是…… | 给经验的固定说法 |
| There's a doc. I'll link it. | 有个文档。我把链接发你。 | **比打一段字更专业** |
| That's the whole point of this channel. | 这个频道就是干这个的。 | 说明规则的意义 |
| You did it without making him feel stupid. | 你没让他觉得难堪。 | 高评价 |
| I was worse my first month. | 我第一个月更糟。 | 化解尴尬 |
| Want to review it before I post? | 发之前你要看一下吗？ | 协作式收尾 |
| That's the rule I actually use. | 这是我实际在用的规则。 | 用实践支撑建议 |

### 中式英语纠正

| 常见错法 | 问题 | 改成 |
| --- | --- | --- |
| `I have a question, is anybody here?` | 无意义铺垫，还 ping 了所有人 | `Quick question about the deploy pipeline —` |
| `Sorry to interrupt everyone.` | 道歉 + 打扰全场，代价更高 | 直接问，或者发到更小的频道 |
| `Please help me, it's urgent.` | urgent 是主观判断，没人会因为你说急就急 | `Deploy's failing with a 403 — anyone seen this?` |
| 把三十行日志直接贴进频道 | 刷屏，别人无法阅读 | 贴进 thread，或者贴到代码片段工具再给链接 |
| `This is not the right channel.` | 指出错误但不给正确做法 | `Better channel for this is #platform-help.` |
| `Read the channel rules.` | 教训人 | `Rule of thumb: questions about your own thing go in a thread.` |

### 口语小注

**1. `@channel` 是"所有人放下手里的活"。**

它会给频道里每个人推送通知。**除了真事故和全员通知，一律不要用**。要找特定的人就 @ 那个人；要找值班的人，很多团队有 `@oncall` 这种专用组。

**2. 讨论要用线程（thread），不要刷频道。**

在频道里回复会自动开 thread，**不要在频道里直接开新消息**。判断标准很简单：**如果你的消息只跟一个人或一件事有关，就放线程**。Dana 说的 `if it's about your thing, it goes in a thread` 就是这个意思。

**3. 问技术问题要给三样：现象、错误信息、环境。**

`403`、`which repo`、`full message`——**给全上下文，别人才能一次答完**。只写 `It doesn't work` 会引出五轮来回，而且频道里所有人都在看你问废话。

**4. 不确定发哪个频道，就发最小的那个。**

`If you're not sure which channel, ask in the smallest one.` 这是很实用的原则：**发错了，别人会让你转；发大了，你打扰了八十个人而且收不回来。**

## 通用句型与说明
### Slack / 邮件全流程速查

| 环节 | 英文 | 中文 |
| --- | --- | --- |
| 开场 | Hey — quick one about … | 嗨——快速问一下…… |
| 请求 | …is ready for review whenever you get a chance. | ……有空的时候帮忙看一下。 |
| 请求 | No rush, but I'd like it by Thursday. | 不急，不过我想周四之前拿到。 |
| 催进度 | Following up on this — any update? | 跟进一下——有进展吗？ |
| 催进度 | When do you think you'll know? | 你觉得什么时候能有答案？ |
| 说卡住 | I'm blocked on … | 我卡在…… |
| 给方案 | If it's not settled by Friday, can we pick one? | 周五还没定的话，能不能先选一个？ |
| 拒绝加活 | I can't do all three well. | 三件我都做好做不到。 |
| 追问 | Is it a hard date or a preferred one? | 是硬日期还是期望日期？ |
| 同步 | Quick recap so we're aligned. | 简单同步一下确保一致。 |
| 免责 | No action needed — just flagging it. | 你不需要做什么，就是同步一下。 |
| 认领 | I'll take that. | 我来。 |
| 收尾 | Thanks — appreciate it. | 谢谢，感谢。 |

### 频道与线程礼仪速查

| 场景 | 该怎么做 | 英文 |
| --- | --- | --- |
| 回复某条消息 | 用线程 | `Thread please.` |
| 需要特定的人看 | @ 那个人 | `@Marcus can you take a look?` |
| 需要全频道注意 | 只在事故时用 | `@channel — the API is down.` |
| 不确定发哪 | 发最小的相关频道 | `ask in the smallest one` |
| 贴长日志 | 贴到线程或用代码片段 | `paste it in the thread` |
| 问题解决了 | 回线程说一句 | `Fixed — thanks.` |
| 别人发错频道 | 指出正确频道，别教训 | `Better channel is #platform-help.` |

**一条原则：能私聊的别发频道，能发线程的别刷频道，能 @ 个人的别 @channel。**

### 全篇词汇

| 单词 | 音标（英 / 美） | 意思 |
| --- | --- | --- |
| email | /ˈiːmeɪl/ /iˈmeɪl/ | 电子邮件 |
| message | /ˈmɛsɪdʒ/ /ˈmɛsədʒ/ | 消息 |
| chat | /tʃæt/ /tʃæt/ | 聊天、即时消息 |
| reply | /rɪˈplaɪ/ /rɪˈplaɪ/ | 回复 |
| forward | /ˈfɔːwəd/ /ˈfɔrwərd/ | 转发 |
| attached | /əˈtætʃt/ /əˈtætʃt/ | 附上的 |
| document | /ˈdɒkjʊmənt/ /ˈdɑkjəmɛnt/ | 文档 |
| draft | /drɑːft/ /dræft/ | 草稿 |
| detail | /ˈdiːteɪl/ /dɪˈteɪl/ | 细节 |
| confirm | /kənˈfɜːm/ /kənˈfɜrm/ | 确认 |
| request | /rɪˈkwɛst/ /rɪˈkwɛst/ | 请求 |
| notice | /ˈnəʊtɪs/ /ˈnoʊtəs/ | 通知、提前告知 |
| remind | /riˈmaɪnd/ /riˈmaɪnd/ | 提醒 |
| follow | /ˈfɒləʊ/ /ˈfɑloʊ/ | 跟进 |
| status | /ˈsteɪtəs/ /ˈstætəs/ | 状态、进展 |
| progress | /ˈprəʊgrɛs/ /ˈprɑˌgrɛs/ | 进展 |
| issue | /ˈɪʃuː/ /ˈɪʃu/ | 问题、事项 |
| solution | /səˈluʃən/ /səˈluʃən/ | 解决方案 |
| priority | /praɪˈɒrɪti/ /praɪˈɔrəti/ | 优先级 |
| block | /blɒk/ /blɑk/ | 阻碍 |
| delay | /dɪˈleɪ/ /dɪˈleɪ/ | 延迟 |
| due | /djuː/ /du/ | 到期的 |
| schedule | /ˈʃɛdʒuːl/ /ˈskɛdʒʊl/ | 日程、安排 |
| meeting | /ˈmiːtɪŋ/ /ˈmitɪŋ/ | 会议 |
| team | /tiːm/ /tim/ | 团队 |
| client | /ˈklaɪənt/ /ˈklaɪənt/ | 客户 |
| colleague | /ˈkɒliːg/ /ˈkɑlig/ | 同事 |
| manager | /ˈmænɪdʒə/ /ˈmænədʒər/ | 经理、上司 |
| owner | /ˈəʊnə/ /ˈoʊnər/ | 负责人 |
| decide | /dɪˈsaɪd/ /ˌdɪˈsaɪd/ | 决定 |
| decision | /dɪˈsɪʒn/ /dɪˈsɪʒən/ | 决定 |
| option | /ˈɒpʃən/ /ˈɑpʃən/ | 选项 |
| agree | /əˈgriː/ /əˈgri/ | 同意 |
| agreement | /əˈgrimənt/ /əˈgrimənt/ | 一致 |
| explain | /ɪkˈspleɪn/ /ɪkˈspleɪn/ | 解释 |
| understand | /ˌʌndəˈstænd/ /ˌʌndərˈstænd/ | 理解 |
| appreciate | /əˈpriːʃieɪt/ /əˈpriʃiˌeɪt/ | 感谢、感激 |
| apologize | /əˈpɒləˌdʒaɪz/ /əˈpɑləˌdʒaɪz/ | 道歉 |

### 关于本页音标的说明

表里标了「见下方说明」的词（**update、brief、clear**）不在本项目的校对音标表里。
按规范要求，**没有校对音标的词不写进词汇表**，所以只列中文意思，音标请查词典确认后再记。

**换成表内词也很自然：** "更新"可以说 **status**（状态）或 **progress**（进展）；"清楚的"可以说 **direct**（直接的）或 **detail**（细节）。

### 语调与发音提示

**1. `Following up on this` 语速要平缓，不要急。**

这句是催进度，但**语气必须像在记事，不能像在催**。说得快而重会变成质问；平缓地说，对方会自然地给你一个时间。

**2. `No rush` 的重音在 no，语速略慢。**

`NO rush`——重音在前，慢一点，**表示"我是真的不急"**。说快了对方会觉得你在客套，反而更急着回复你。

**3. `My bad` 要说得轻、快、短。**

/mɑɪ bæd/ 两个词一气说完，语调平。**它是最轻的道歉，说得郑重其事反而会让小事变大**。大事不要用它。

**4. `Is it a hard date or a preferred one?` 的两个重音。**

重音落在 **hard** 和 **preferred** 上，形成对比。**这是整句话的关键所在——你在区分两种截然不同的承诺。**
