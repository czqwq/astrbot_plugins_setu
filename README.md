<div align="center">

# astrbot_plugins_setu

_✨ 一个从API获取图片的插件 ✨_

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![AstrBot](https://img.shields.io/badge/AstrBot-4.0%2B-orange.svg)](https://github.com/Soulter/AstrBot)

</div>

## 📖 简介

这是一个适用于 AstrBot 的插件，可以从指定 API 获取随机图片。用户可以通过指令 `/img` 获取一张随机图片。

## 🌟 特性

- 从自定义 API 获取随机图片
- 支持黑白名单控制
- 支持自定义指令名称
- 支持 SSL 证书跳过验证（适用于某些自签名证书的场景）

## 📦 安装

在 AstrBot 的插件市场中搜索 `astrbot_plugins_setu` 并安装。

## ⚙️ 配置

| 配置项 | 类型 | 说明 |
|--------|------|------|
| api_url | string | 随机图片 API 地址 |
| group_whitelist | list | 群聊白名单，仅在此列表中的群聊可以使用插件 |
| group_blacklist | list | 群聊黑名单，此列表中的群聊无法使用插件（管理员除外） |
| user_blacklist | list | 用户黑名单，此列表中的用户无法使用插件 |
| custom_commands | list | 自定义指令名称，可以替代默认的 `/img` 指令 |

## 📝 使用方法

1. 在插件配置中设置 `api_url` 参数为你想要使用的图片 API 地址
2. （可选）配置黑白名单以控制插件的访问权限
3. （可选）配置 `custom_commands` 来更改默认指令名称
4. 在聊天中使用 `/img` 或你自定义的指令获取图片

## 🛡️ 黑白名单说明

黑白名单功能可以帮助你更好地控制插件的使用范围：

- **白名单（group_whitelist）**：只有在白名单中的群聊才能使用插件功能
- **黑名单（group_blacklist）**：黑名单中的群聊无法使用插件功能（管理员除外）
- **用户黑名单（user_blacklist）**：被列入黑名单的用户在任何地方都无法使用插件功能

注意：如果同时设置了白名单和黑名单，白名单具有更高的优先级。

## 📜 自定义指令

你可以通过修改 `custom_commands` 配置来自定义触发指令的名称：

1. 删除默认的 `img`
2. 添加你想要的新指令名称，例如 `setu`、`image`、`pic` 等
3. 保存配置后即可使用新的指令

## 📄 API 格式要求

本插件期望 API 返回如下格式的 JSON 数据：

```json
{
  "error": false,
  "data": [
    {
      "title": "图片标题",
      "author": "作者",
      "urls": {
        "original": "图片URL"
      }
    }
  ]
}
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个插件。

## 📃 许可证

本项目采用 MIT 许可证发布。