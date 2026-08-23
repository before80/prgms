+++
title = "14-团队"
date = 2026-08-22T18:00:00+08:00
weight = 84
type = "docs"
description = "Clippy 团队"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Clippy Documentation](https://doc.rust-lang.org/nightly/clippy/)

# 团队 {#the-team}


> 原文链接: [https://doc.rust-lang.org/nightly/clippy/development/the_team.html](https://doc.rust-lang.org/nightly/clippy/development/the_team.html)


每一位为 Clippy 做贡献的人，都在塑造这个项目。协作与讨论是每个开源项目的命脉。Clippy 的层级非常扁平，团队主要拥有额外的仓库访问权限。

本文概述各组的加入流程、职责与访问权限。

本章提到的所有常规活动都记录在[日历仓库]中。也可下载日历文件：[clippy.ics]

## 所有人

包括你在内的所有人，都欢迎参与讨论并以 PR 等方式贡献。

你还可以使用 `@rustbot` 添加标签、认领 issue，享有一定的分诊权限。参见[使用 @rustbot 打标签][labeling with @rustbot]。

对所有人而言，都应保持健康的工作与生活平衡，需要时请休息。

## Clippy-Contributors

这是一组经常为 Clippy 做贡献的人，协助分诊工作。

### 职责

该团队旨在让常客更容易贡献，并不承担必须完成的固定职责。但我们鼓励该组成员协助分诊，包括：

1. **为 issue 打标签**

    对于 `good first issue` 标签，仍可用 `@rustbot` 订阅 issue，并在评论中向感兴趣的人提供帮助。

2. **关闭重复或已解决的 issue**

    手动关闭 issue 时，通常最好简短说明原因。

3. **两周无活动后 ping 相关人员**

    我们尽量保持 issue 分配与 PR 较为及时。两周后，可向拖延方友好 ping 一下。

    若作者较忙或想放弃，可用 `I-inactive-closed` 标签关闭 PR。若审阅者较忙，可将 PR 重新分配给其他人。

    可查看：<https://triage.rust-lang.org/triage/rust-lang/rust-clippy> 以监控 PR。

虽非正式职责，我们也鼓励贡献者审阅 PR 并在 Zulip 上帮忙。团队始终感谢任何帮助！

### 成员资格

若你已持续为 Clippy 贡献一段时间，我们可能会邀请你加入该团队。成员也可推荐他们认为适合加入的人。

该组没有正式的 onboarding 流程，你可以继续以往的工作。若愿意，可在 Clippy Zulip 频道或私信请人指导。

若你在 Clippy 上超过三个月不活跃，我们可能会将你移至校友组。随时欢迎回来。

## Clippy 团队

[Clippy 团队](https://www.rust-lang.org/governance/teams/dev-tools#team-clippy)
负责维护 Clippy。

### 职责

1. **及时响应 PR**

    若你暂时没时间审阅，完全没问题。
    可评论 `r? clippy` 将 PR 随机分配给团队成员。

2. **需要时请休息**

    你很重要！没有你就没有今天的 Clippy。因此需要时请尽早休息、恢复精力。

3. **在 Zulip 上保持响应**

    指在合理时间内回复，一两天内回复完全可以。

    也建议在 Zulip 上回复讨论，并参加每两周一次的 Clippy 会议。会议日期见[日历仓库]。

4. **将 Clippy 与 rust-lang/rust 仓库同步**

    每两周进行一次，通常由 @flip1995 负责。

5. **更新 changelog**

    每次发布（每六周）都需要完成。

### 成员资格

若你已活跃一段时间，我们可能会联系你，询问是否愿意协助审阅并最终加入 Clippy 团队。

在 onboarding 期间，你会被分配 PR 进行审阅。
还会有一位活跃团队成员作为导师，通过 Zulip 私信保持联系、提供建议与反馈。有问题请随时提问，这是最好的学习方式。审阅完成后，可 ping 导师进行完整审阅，并以双方名义 r+ 该 PR。

当导师认为你可以独立审阅时，会在活跃团队成员中发起非正式投票，正式将你加入团队。该投票通常全票通过。确认你仍有兴趣加入后，即可入队。onboarding 通常需要数周到数月。

若你在 Clippy 上超过三个月不活跃，我们可能会将你移至校友组。随时欢迎回来。

[calendar repository]: https://github.com/rust-lang/calendar/blob/main/clippy.toml
[clippy.ics]: https://rust-lang.github.io/calendar/clippy.ics
[labeling with @rustbot]: https://forge.rust-lang.org/triagebot/labeling.html
