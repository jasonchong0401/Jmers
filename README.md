# Jmers — Hermes Agent 配置与工作流

Hermes Agent 的 skills、代码项目和工作流参考文档。

## 目录

```
hermes/
  skills/                           # Hermes skills（按类别）
    mcp/native-mcp/                 # MCP 客户端配置
    github/                         # GitHub 集成
    devops/playwright-scraping/     # Playwright 爬虫
    productivity/                   # 生产力工具
    software-development/           # 软件开发工作流
    creative/                       # 创意工具
    research/                       # 研究工具
    mlops/                          # MLOps 工具
    autonomous-ai-agents/           # 自主代理
    ...
  projects/
    playwright-investing/           # Investing.com 商品爬虫
```

## 核心内容

### MCP 配置

- `native-mcp` — Hermes MCP 客户端完整配置指南（stdio/HTTP transport、token 注入、troubleshooting）

### GitHub 工作流

- `github-auth` — GitHub 认证
- `github-repo-management` — 仓库管理
- `github-pr-workflow` — PR 工作流
- `github-issues` — Issue 管理
- `github-code-review` — 代码审查
- `github-api-workflows` — API 工作流（含空仓库陷阱）

### DevOps

- `playwright-scraping` — Investing.com Cloudflare 绕过经验总结

### 项目

- `playwright-investing/` — Investing.com 商品数据爬虫（Python + Node.js 双版本）

## 安全说明

所有文件中的 token/API key 均为占位符，无真实敏感信息。

## 关联仓库

- [jSpider](https://github.com/jasonchong0401/jSpider) — 独立的爬虫项目
