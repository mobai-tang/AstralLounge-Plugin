# AstralLounge Plugin

AstralLounge 插件市场 - 收集和分享各类插件

---

## 目录

- [插件列表](#插件列表)
- [安装插件](#安装插件)
- [开发插件](#开发插件)
- [使用 Trae IDE 开发](#使用-trae-ide-开发)
- [插件开发指南](#插件开发指南)

---

## 插件列表

### 内置插件

| 插件 | 版本 | 说明 | 触发词 |
|------|------|------|--------|
| ⏰ remind | 1.0.0 | 定时提醒 | `remind:`, `reminders`, `cancel-remind` |

### 第三方插件

敬请期待...

---

## 安装插件

### 方式一：放置到插件目录

将插件文件复制到 `backend/plugins/skills/` 目录：

```bash
cp your_plugin.py backend/plugins/skills/
```

### 方式二：使用 API 安装

```bash
curl -X POST http://localhost:8000/api/plugins/install -d '{"url": "https://..."}'
```

---

## 开发插件

### 快速开始

在 `backend/plugins/skills/` 目录下创建新的 Python 文件：

```python
from backend.plugins.plugin_manager import BaseSkill, SkillMetadata

class MyPlugin(BaseSkill):
    metadata = SkillMetadata(
        name="my-plugin",
        version="1.0.0",
        description="我的插件",
        author="Your Name",
        triggers=["trigger:", "/cmd"]
    )

    async def process_input(self, text: str, context: dict):
        if text.startswith("trigger:"):
            return f"处理: {text[8:]}"
        return text
```

---

## 使用 Trae IDE 开发

[Trae](https://trae.ai/) 是字节跳动推出的 AI 驱动开发者工具，完美支持本项目的插件开发。

### 安装 Trae

1. 访问 [trae.ai](https://trae.ai/) 下载安装
2. 或在 VS Code 基础上安装 Trae 扩展

### 克隆项目

```bash
git clone https://github.com/mobai-tang/AstralLounge-Plugin.git
cd AstralLounge-Plugin
```

### 配置开发环境

#### 1. 打开项目

```
文件 → 打开文件夹 → 选择 AstralLounge-Plugin
```

#### 2. 安装 Python 依赖（如需）

```bash
pip install loguru
```

#### 3. 配置 Python 解释器

1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 `Python: Select Interpreter`
3. 选择已配置的 Python 环境

### 使用 AI 辅助开发

Trae 内置 AI 助手，可大幅提升开发效率：

#### 快捷键

| 功能 | Windows | 说明 |
|------|---------|------|
| 打开 AI 助手 | `Ctrl+I` | 打开侧边 AI 面板 |
| 快速提问 | `Ctrl+L` | 在编辑器中提问 |
| 代码补全 | `Tab` | 接受 AI 建议 |
| 解释代码 | `Ctrl+Shift+T` | 解释选中代码 |

#### 使用示例

**1. 解释代码**
- 选中代码 → 右键 → "解释代码"
- 或使用 `Ctrl+Shift+T`

**2. 生成代码**
- 在 AI 助手中输入需求
- 例如："帮我写一个天气查询的 BaseSkill 插件"

**3. 重构代码**
- 选中代码 → "重构这个函数"
- AI 会提供改进建议

**4. 修复 Bug**
- 复制错误信息到 AI 助手
- AI 会分析并提供解决方案

### 开发新插件

#### 1. 创建插件文件

在项目根目录创建 `your_plugin.py`：

```python
"""
[插件名称] - [简短描述]
"""

from backend.plugins.plugin_manager import BaseSkill, SkillMetadata
from typing import Dict, Any
from loguru import logger


class YourPlugin(BaseSkill):
    """插件说明"""

    metadata = SkillMetadata(
        name="your-plugin",
        version="1.0.0",
        description="插件功能描述",
        author="Your Name",
        triggers=["trigger:", "/cmd"],
        category="tools",
        icon="🔧"
    )

    async def on_load(self):
        """插件加载时调用"""
        logger.info(f"{self.metadata.name} 已加载")

    async def on_unload(self):
        """插件卸载时调用"""
        pass

    async def process_input(self, text: str, context: Dict[str, Any]) -> str:
        """处理输入消息"""
        # 检查触发词
        for trigger in self.metadata.triggers:
            if text.startswith(trigger):
                content = text[len(trigger):].strip()
                # 处理逻辑
                return f"处理结果: {content}"
        return text
```

#### 2. 使用 AI 辅助编写插件

在 AI 助手中输入：

```
帮我写一个 [功能名称] 的 BaseSkill 插件
参考 remind.py 的结构
```

AI 会根据现有的 `remind.py` 示例生成类似的插件代码。

#### 3. 调试插件

1. 在插件代码中添加日志：

```python
from loguru import logger

async def process_input(self, text: str, context: dict):
    logger.info(f"收到消息: {text}")
    # 你的逻辑
    return result
```

2. 查看日志输出

#### 4. 测试插件

将插件文件复制到主项目的 `backend/plugins/skills/` 目录，然后重启服务。

---

## 插件开发指南

详细内容请参考 [PLUGIN_DEV_GUIDE.md](./PLUGIN_DEV_GUIDE.md)

---

## 项目结构

```
AstralLounge-Plugin/
├── README.md                 # 本文件
├── PLUGIN_DEV_GUIDE.md      # 插件开发详细指南
├── remind.py                # 提醒插件示例
└── plugins/                 # 更多插件（待添加）
```

---

## 提交插件

欢迎提交插件！请遵循以下步骤：

1. Fork 本仓库
2. 创建新分支 `git checkout -b feature/your-plugin`
3. 添加你的插件文件
4. 提交并推送到 GitHub
5. 创建 Pull Request

---

## License

MIT License
