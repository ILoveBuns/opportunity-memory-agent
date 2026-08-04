# GOAI 2026 平台字段填报稿

以下内容可直接复制到初赛平台；姓名、手机号、证件、组织归属和协议勾选留给参赛者本人填写。

| 字段 | 建议内容 |
|---|---|
| 项目名称（中文） | 机会记忆智能体 |
| Project name | Opportunity Memory Agent |
| 赛道 | Boundless Agents（无界智能体） |
| 一句话介绍 | 一个具备可审计长期记忆的机会推进智能体，将审核回复、截止时间、阻塞证据和下一步写入持久化事件流，并生成基于事实的行动队列。 |
| Target users | 同时管理竞赛、开源赏金、销售线索或资助申请的个人与小团队。 |
| Pain point | 机会流程跨周、跨平台，信息分散；普通聊天助手会遗忘历史、重复操作或越过身份与协议边界。 |
| Solution | 以 CockroachDB 保存追加式事件记忆，使用确定性评分生成优先行动队列，再让 Gemini 仅基于结构化事实生成摘要。 |
| Innovation | 事件溯源记忆；证据优先排序；受约束生成；显式人机边界；轻量容器化部署。 |
| Open-source URL | https://github.com/ILoveBuns/opportunity-memory-agent |
| License | MIT |
| Reproduction | `docker compose up --build`，随后运行 `docker compose exec api python scripts/seed_demo.py`。 |
| Current evidence | 10 项自动化测试通过；公开源码、零凭据真实界面演示、Docker Compose、AWS App Runner 配置、方案 PDF。 |
| Data and compliance | 演示数据为虚构数据；模型只接收行动队列中的结构化事实；身份、条款、付款与验证码保留为人工边界。 |
| Business path | 先服务同时管理多条机会的小团队；后续可扩展到销售、资助申请、招聘和客户成功等长期工作流。 |
| Current limitations | 尚无真实客户收入或公开云部署，不对此作虚假声明；正式平台身份与收款资料由参赛者本人提供。 |

## 必须由本人确认的字段

- 真实姓名、手机号、证件或实名信息。
- 团队成员和组织归属。
- 参赛协议、知识产权及数据授权勾选。
- 若进入前 15，能否于 2026-09-22 至 09-23 到杭州参加现场决赛和颁奖。

## 2026-08-04 平台状态

- 账号中心确认已报名，团队为 `Opportunity Memory Agent（1）`，意向赛道为 Boundless Agents。
- 初赛第一次提交记录为“机会记忆智能体”，2026-08-02 01:29:21，8.0 MB，审核中。
- 平台站内信要求受影响选手使用本地原始 ZIP 重新上传；当前已用 1/3 次，仍有两次机会。
- 重传时使用根目录的 `GOAI_SUBMISSION_PACKAGE.zip`，并按 `GOAI_REUPLOAD_GUIDE.md` 核对。
