# Codex Skills

这里是本地 Codex 技能库。每个技能都是一个独立目录，核心说明写在 `SKILL.md` 中，用于告诉 Codex 什么时候触发、怎么执行。

## 技能一览

| Skill | 作用 | 典型使用场景 | 路径 |
| --- | --- | --- | --- |
| code-simplifier | 精简与统一最近修改的代码，保持功能不变，提升可读性与一致性 | 代码整理、提交前清理、消除冗余与复杂度 | `code-simplifier/` |
| ruoyi-vue-pro-java-backend | ruoyi-vue-pro 风格 Java 后端规范与流程：Javadoc、日志、对象拷贝、Maven 编译 | 新增/修改后端接口、服务、持久化逻辑 | `ruoyi-vue-pro-java-backend/` |
| ui-ux-pro-max | UI/UX 设计知识库：样式、配色、字体、可用性与多技术栈指南 | 设计页面、评审 UX、生成设计系统与实施建议 | `ui-ux-pro-max/` |

## 使用方式

- 触发：在需求中直接写出技能名（例如 `code-simplifier`），或描述与技能高度匹配的任务。
- 执行：先阅读对应目录的 `SKILL.md`，按其中流程与约束实施。

## 目录结构

```
skills/
├── code-simplifier/
│   └── SKILL.md
├── ruoyi-vue-pro-java-backend/
│   └── SKILL.md
├── ui-ux-pro-max/
    └── SKILL.md

```

## 维护约定

- 每个技能目录必须包含 `SKILL.md`，作为触发与执行的唯一入口说明。
- 新技能遵循“简洁、可复用、少依赖”的原则，优先把可重复流程放到 `scripts/`。
- `.system/` 为系统技能目录，尽量只在需要时修改。
