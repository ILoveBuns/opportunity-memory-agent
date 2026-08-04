# GOAI 初赛附件重传清单

平台账号中心在 2026-08-03 发布站内信：部分网站上传的 ZIP 在存储过程中损坏，要求参赛者使用本地保存的原始 ZIP 重新上传。当前初赛记录显示已提交 1/3 次，因此仍有两次提交机会；截止前最后一次成功提交为评审版本。

## 上传文件

- 文件：`GOAI_SUBMISSION_PACKAGE.zip`
- 上传前运行：`unzip -t GOAI_SUBMISSION_PACKAGE.zip`
- 上传前运行：`sha256sum GOAI_SUBMISSION_PACKAGE.zip`
- 必须看到 `No errors detected in compressed data`。

不要使用此前从平台下载回来的附件。应使用本仓库打包脚本刚生成、并在本地通过完整性检查的文件。

## 表单字段

| 字段 | 内容 |
|---|---|
| 作品名称 | 机会记忆智能体 |
| 代码仓库 | https://github.com/ILoveBuns/opportunity-memory-agent |
| Demo 链接 | 可留空；当前没有公开云部署，不虚构在线 Demo |
| 作品附件 | `GOAI_SUBMISSION_PACKAGE.zip` |

收件人姓名、手机号、详细地址和短袖尺码属于个人资料，必须由参赛者本人填写并确认。

## 成功标准

1. 页面显示初赛“已提交 2/3 次”。
2. 新记录时间晚于 2026-08-03 的重传通知。
3. 新记录显示“已提交”或“审核中”。
4. 记录中的附件大小与本地新包一致。
5. 保存成功页或站内信作为证据。
