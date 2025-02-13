# ComfyUI-DeepSeek-API

ComfyUI-DeepSeek-API 是一个旨在将 DeepSeek 的强大 AI 功能集成到 ComfyUI 工作流中的自定义节点。通过此集成，用户可以在 ComfyUI 的可视化界面中，直接调用 DeepSeek 的聊天和指令模型，实现无缝的 AI 交互体验。

一、主要特性：

1. 双重操作模式：

聊天模式： 支持带有对话记忆的连续交流。
单次指令模式： 适用于一次性的指令执行。

2. 生图prompt优化：

内置prompt优化提示词。
与 ComfyUI 的视觉工作流无缝对接。

3. 高级配置：

可自定义最大令牌限制。
可选择是否显示推理过程。
可配置聊天历史管理。

二、安装与配置：

1.获取 API 密钥：

（1） 前往 无问芯穹 的 API 大模型服务平台 https://cloud.infini-ai.com/genstudio/model ，注册账号并获取 API 密钥。

（2）前往 DeepSeek 的 API 平台 https://platform.deepseek.com/ ，注册账号并获取 API 密钥。

2.配置 ComfyUI：

在 ComfyUI 的配置文件 config.json 中，添加以下内容：

    {
      "name": "无问DeepSeek-R1",
      "model": "deepseek-r1",
      "api_key": "",
      "base_url": "https://cloud.infini-ai.com/maas/v1/"
    }

3. 使用自定义节点：

在 ComfyUI 的工作流中，添加对应自定义节点。

配置该节点的参数，以满足你的具体需求。

三、注意事项：

推荐使用无问芯穹的API，DeepSeek 的官方 API 服务可能会因服务器资源限制而暂停充值。请关注官方公告，以获取最新的服务状态。 

在使用 API 时，务必遵守其使用条款和政策。

如需更多关于 ComfyUI 的信息，请访问其官方 GitHub 仓库：

如需更多关于 DeepSeek 的信息，请访问其官方网站：

四、联系方式：

如在使用过程中遇到问题，欢迎通过以下方式联系我：

姓名： 卷儿（juaner）
邮箱： juaner0211@163.com

希望这个项目能帮助你更好地将 DeepSeek 的能力融入到 ComfyUI 的工作流中，提升你的工作效率。
