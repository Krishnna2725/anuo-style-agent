# 常熟阿诺 Agent Skill (anuo-style-agent)

一个用于复刻“常熟阿诺”语言风格的 AI Skill，重点是思维路径和语感，而不是单纯堆口头禅。

## 核心能力

- 听觉热启动：每次触发可调用音频脚本播放对应语境的原声切片。
- 双层控制：Behavior Layer 用英文描述流程与判定，Style Layer 用中文保留梗和语气。
- 语言锁：默认只输出简体中文，避免中英混写污染最终回复。
- 反刻板机制：短回复优先、结构轮换、收尾冷却、多轮去重。
- 短路语感：支持“句内自我打架、因果倒挂、轻微卡顿”的废话感。
- 兜圈落点：日常问答优先采用“2-3句绕圈 + 1句你是不是X了？”的互动节奏。

## 目录结构

```text
anuo-style-agent/
├── assets/
│   └── audio/                # 原声音频切片
├── scripts/
│   └── play_audio.py         # 按关键词匹配或随机播放音频
├── SKILL.md                  # 核心规则与风格设定
└── README.md
```

## 使用方式

1. 克隆仓库：

```bash
git clone https://github.com/Krishnna2725/anuo-style-agent.git
```

2. 在支持 Skill/Prompt 配置的 Agent 框架中加载 `SKILL.md`。
3. 用户输入包含“阿诺”或“诺神”时触发该风格。

## 音频脚本

脚本路径：`scripts/play_audio.py`

示例：

```bash
python scripts/play_audio.py
python scripts/play_audio.py --keyword "无糖可乐"
python scripts/play_audio.py --dry-run
```

说明：
- `--keyword` 会在 `assets/audio` 下匹配文件名并随机播放匹配项。
- 不传 `--keyword` 时会从全部音频中随机选择。

## 输出风格原则

- 默认 1-3 句，短句优先。
- 不固定“起手-索敌-反问-破防”四连模板。
- 普通提问不无故爆炸，挑衅场景才允许短促反击。
- 连续多轮尽量不复用同一结尾句。
- 结尾优先可接话的诊断问句，例如“你是不是练腿了啊？”。

## 免责声明

- 本 Skill 用于抽象人格风格模拟与娱乐创作。
- 请避免将其用于现实中的攻击、歧视、骚扰或违规内容生成场景。
