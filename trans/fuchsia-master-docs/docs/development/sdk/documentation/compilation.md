 
# Compiling C/C++ code  编译C / C ++代码 

The present document compiles a list of guidelines, recommendations, and expectations around the topic of compiling C and C++ code against the Core SDK. 本文档围绕针对核心SDK编译C和C ++代码的主题，汇编了一系列准则，建议和期望。

 

 
## Sysroot  Sysroot 

The Fuchsia sysroot for a given target architecture is available under `//arch/<architecture>/sysroot`.That directory contains a complete sysroot and may be used with any tool thataccepts a `--sysroot` flag. 在// arch / <architecture> / sysroot下可以找到给定目标体系的紫红色sysroot，该目录包含完整的sysroot，并且可以与接受--sysroot标志的任何工具一起使用。

 

 
## Prebuilts  预建 

All prebuilts have C linkage.  所有预建的都具有C链接。

 
### Debug symbols  调试符号 

Debug symbols for all prebuilts are available under `//.build-id`, which follows a [standard convention][build-id]. 在//.build-id下可以使用所有预构建的调试符号，该符号遵循[标准约定] [build-id]。

 

 
## Compilation parameters  编译参数 

 
- C++ sources are compatible with both C++14 and C++17.  -C ++源代码与C ++ 14和C ++ 17兼容。

 
### Warning flags  警告标志 

The following flags are guaranteed to not generate any warning:  保证以下标志不会产生任何警告：
- `-Wall`  -`-Wall`
- `-Wextra-semi`  -`-Wextra-semi`
- `-Wnewline-eof`  -`-Wnewline-eof`
- `-Wshadow`  -`-影子`

The following flags may generate warnings:  以下标志可能会生成警告：
- `-Wdeprecated-declarations`  -`-Wdeprecated-clarifications`

 

