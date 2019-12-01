 
# Developer tool guidelines  开发人员工具准则 

This section provides guidelines on *creating* CLI and GUI tools for Fuchsia. 本部分提供有关为Fuchsia *创建* CLI和GUI工具的准则。

For information on existing tools, please refer to documentation for those tools. 有关现有工具的信息，请参阅这些工具的文档。

 
## Other topics  其他话题 

 
- [Command-line tool requirements](cli.md)  -[命令行工具要求]（cli.md）
    - [CLI --help requirements](cli_help.md)  -[CLI-帮助要求]（cli_help.md）
- GUI Tool requirements (needs writing)  -GUI工具要求（需要编写）

 
## Packaging a tool with the core SDK  使用核心SDK打包工具 

The core SDK will contain:  核心SDK将包含：

 
  * The tool binary itself.  *工具二进制本身。

 
  * The [dev_finder](/docs/development/sdk/documentation/device_discovery.md) tool which can enumerate Fuchsia devices to get their names. * [dev_finder]（/ docs / development / sdk / documentation / device_discovery.md）工具可枚举Fuchsia设备以获取其名称。

 
  * A document in [//docs/development/sdk/documentation](/docs/development/sdk/documentation)describing the contract of this tool and how to connect it to the targetsystem. The target audience of this document is people writing integrationscripts rather than being an end-user-friendly “how-to” (debugger example). * [// docs / development / sdk / documentation]（/ docs / development / sdk / documentation）中的文档，描述了此工具的合同以及如何将其连接到目标系统。本文档的目标读者是编写集成脚本的人员，而不是最终用户友好的“操作方法”（调试器示例）。

 
## Environment-specific SDKs  特定于环境的SDK 

The `dev_finder` abstracts device listing and selection across all SDK variants. With the right tool design, the extent of integration required shouldbe to run `dev_finder` to get the address and pass the address to the tool withother environment-specific flags. In the case of the debugger the tool-specificcode would: dev_finder提取所有SDK变体中的设备列表和选择。使用正确的工具设计，所需的集成度应为运行`dev_finder`以获取地址并将该地址与其他环境特定的标志一起传递给工具。对于调试器，特定于工具的代码将：

 
  * Connect to a shell (this should be a primitive provided by the environment-specific SDK) on the target and run the `debug_agent`. *在目标上连接到外壳程序（这应该是特定于环境的SDK提供的原语）并运行`debug_agent`。

 
  * Run zxdb with the address provided by `dev_finder`, passing any local settings files and symbol paths on the command-line. *使用`dev_finder`提供的地址运行zxdb，并在命令行上传递任何本地设置文件和符号路径。

 
## Tool requirements  工具要求 

Tools should allow all environment parameters to be passed in via command-line arguments. Examples include the location of settings files and symbollocations. This allows different SDKs to be hermetic. 工具应允许所有环境参数通过命令行参数传递。示例包括设置文件的位置和符号位置。这允许不同的SDK处于封闭状态。

Tools should be written to make writing environment-specific scripts as simple as possible. For example, the debugger should automatically retry connections(DX-1091) so the current behavior of waiting for the port to be open in thelaunch scripts can be removed. 应该编写工具以使编写特定于环境的脚本尽可能简单。例如，调试器应自动重试连接（DX-1091），以便可以消除启动脚本中等待端口打开的当前行为。

Tool authors are responsible for:  工具作者负责：

 
  * Writing the tool with the appropriate interface.  *使用适当的界面编写工具。
  * Providing documentation on this interface in //docs/development/sdk/documentation.  *在// docs / development / sdk / documentation中提供有关此接口的文档。
  * Currently please reach out to get bugs filed on individual SDKs. We are working on a better process for this (DX-1066). *当前，请与我们联系以获取在各个SDK上记录的错误。我们正在为此做一个更好的过程（DX-1066）。

