 
# Debugger (zxdb)  调试器（zxdb） 

Zxdb is a console debugger for native code compiled with DWARF symbols (C, C++ and Rust). The frontend runs on the host computer and connects to the on-device`debug_agent`. This document describes how to set up these processes. Zxdb是使用DWARF符号（C，C ++和Rust）编译的本机代码的控制台调试器。前端在主机上运行，​​并连接到设备上的“ debug_agent”。本文档介绍了如何设置这些过程。

 
## Running the agent  运行代理 

The `debug_agent` is run on the target device along with the port number that it should listen to for incoming client connections. Typically this commandwill be run from a console after [ssh-ing](ssh.md) in to the system: `debug_agent`连同目标端口号一起在目标设备上运行，以侦听传入的客户端连接。通常，此命令将在[ssh-ing]（ssh.md）进入系统后从控制台运行：

```
run fuchsia-pkg://fuchsia.com/debug_agent#meta/debug_agent.cmx --port=2345
```
 

 
## Connecting the client  连接客户端 

The `zxdb` client program is run on the host computer. It can be connected to the `debug_agent` via the interactive `connect` debugger command or it canautomatically connect based on a command-line flag. Both IPv4 and IPv6addresses are supported (see [device discovery](device_discovery.md) to findthe address). The port should match the port number passed to the agent. zxdb客户端程序在主机上运行。它可以通过交互式`connect`调试器命令连接到`debug_agent`，也可以基于命令行标志自动连接。同时支持IPv4和IPv6地址（请参阅[设备发现]（device_discovery.md）以找到地址）。该端口应与传递给代理的端口号匹配。

```
zxdb -c "[f370::5051:ff:1e53:589a%qemu]:2345"
```
 

 
### Connecting via a script  通过脚本连接 

Scripts may want to automatically launch the agent and client automatically. The script should wait for the port to be open on the target system beforelaunching the client. Automatic retry is not yet implemented in the client. 脚本可能想要自动启动代理和客户端。在启动客户端之前，脚本应等待端口在目标系统上打开。客户端中尚未实现自动重试。

To clean up the debug agent gracefully when the client exits, pass the `--quit-agent-on-exit` command-line flag to the client. 要在客户端退出时优雅地清理调试代理，请将`--quit-agent-on-exit`命令行标志传递给客户端。

 
## Specifying symbol paths  指定符号路径 

The debugger expects unstripped ELF files to be available on the local host system. Symbols on the target are not used. The location where the local buildstores symbols must be passed to the `zxdb` client. 调试器希望未剥离的ELF文件在本地主机系统上可用。不使用目标上的符号。本地buildstore符号必须传递到`zxdb`客户端的位置。

Local symbols can be passed on the command line:  可以在命令行上传递本地符号：

```
zxdb --symbol-path=/path-to-symbols
```
 

The path can be any of:  路径可以是以下任何一种：

 
  * An individual symbolized ELF file.  *单个符号化ELF文件。
  * An ids.txt file mapping build IDs to local files.  *将构建ID映射到本地文件的ids.txt文件。
  * A directory name. If the directory is a GNU-style symbol repo (see below), symbols will be taken from the .build-id folder beneath it, otherwise thedirectory will be searched (non-recursively) for symbolized ELF files. *目录名称。如果该目录是GNU样式的符号存储库（请参见下文），则将从其下的.build-id文件夹中获取符号，否则将在该目录中搜索（非递归）符号ELF文件。

```
Multiple `--symbol-path` parameters may be specified if there are symbols in
more than one location. All locations will be searched.

Symbol locations can also be edited interactively in the client using the
global "symbol-paths" setting (see the interactive "get" and "set" commands).
