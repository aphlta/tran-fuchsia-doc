 
# zxdb: Fuchsia native debugger setup and troubleshooting  zxdb：紫红色的本机调试器设置和故障排除 

 
## Overview  总览 

The debugger is for C/C++ code running on Fuchsia compiled in-tree for either CPU (ARM64 or x64). Rust works but is less feature-complete. The state oflanguages including Rust can be seen [here](#other-languages). 该调试器用于在Fuchsia上为CPU（ARM64或x64）在树中编译的C / C ++代码。 Rust可以工作，但是功能不完善。可以在[here]（其他语言）中看到包括Rust在内的语言状态。

This is the very detailed setup guide. Please see:  这是非常详细的设置指南。请参见：

 
  * The [user guide](debugger_usage.md) for help on debugger commands.  * [用户指南]（debugger_usage.md）提供有关调试器命令的帮助。

The debugger runs remotely only (you can't do self-hosted debug).  调试器仅在远程运行（您不能进行自托管调试）。

 
### Bugs  虫子 

 
  * [Open zxdb bugs](https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5040)  * [打开zxdb错误]（https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5040）

 
  * [Report a new zxdb bug](https://bugs.fuchsia.dev/p/fuchsia/issues/entry?components=DeveloperExperience%3Ezxdb)  * [报告新的zxdb错误]（https://bugs.fuchsia.dev/p/fuchsia/issues/entry?components=DeveloperExperience%3Ezxdb）

 
## Binary location (for SDK users)  二进制位置（适用于SDK用户） 

The binary is `tools/zxdb` in the Fuchsia SDK. SDK users will have to do an extra step to set up your symbols. See "Running out-of-tree" below for more. 在Fuchsia SDK中，二进制文件是`tools / zxdb`。 SDK用户将不得不执行额外的步骤来设置您的符号。有关更多信息，请参见下面的“在树外运行”。

 
## Compiling (for Fuchsia team members)  编译（针对紫红色团队成员） 

A Fuchsia "core" build includes (as of this writing) the necessary targets for the debugger. So this build configuration is sufficient: 紫红色的“核心”构建包括（截至撰写本文时）调试器的必要目标。因此，此构建配置已足够：

```sh
fx --dir=out/x64 set core.x64
```
 

If you're compiling with another product, you may not get it by default. If you don't have the debugger in your build, add `//bundles:tools` to your"universe", either with: 如果要使用其他产品进行编译，则默认情况下可能无法获得它。如果您的构建中没有调试器，则使用以下命令将“ // bundles：tools”添加到“ universe”中：

```
fx <normal_stuff_you_use> --with //bundles:tools
```
 

Or you can edit your GN args directly by editing `<build_dir>/args.gn` and adding to the bottom: 或者，您可以通过编辑`<build_dir> / args.gn`并添加到底部来直接编辑GN args：

```
universe_package_labels += [ "//bundles:tools" ]
```
 

 
## Running  跑步 

 
### Preparation: Boot with networking  准备：通过网络启动 

Boot the target system with networking support:  通过网络支持引导目标系统：

 
  * Hardware devices: use the device instructions.  *硬件设备：使用设备说明。
  * AEMU: `fx emu -N`  * AEMU：`fx emu -N`
  * QEMU: `fx qemu -N`  * QEMU：`fx qemu -N`

(If using x64 with an emulator on a Linux host, we also recommend the "-k" flag which will make it run faster). （如果在Linux主机上将x64与仿真器一起使用，我们还建议使用“ -k”标志，这将使其运行得更快）。

To manually validate network connectivity run `fx shell` or `fx netaddr`.  要手动验证网络连通性，请运行“ fx shell”或“ fx netaddr”。

 
### Simple method  简单的方法 

You can use the fx utility to start the debug agent and connect automatically.  您可以使用fx实用程序启动调试代理并自动连接。

For most build configurations, the debug agent will be in the "universe" (i.e. "available to use") but not in the base build so won't be on the system beforeboot. You will need to run: 对于大多数构建配置，调试代理将位于“ Universe”（即“可使用”）中，而不位于基本构建中，因此在启动前不会在系统上。您将需要运行：

```sh
fx serve
```
 

to make the debug agent's package avilable for serving to the system. Otherwise you will get the message "Timed out trying to find the Debug Agent". 使调试代理的软件包可用于系统。否则，您将收到消息“尝试查找调试代理超时”。

Once the server is running, launch the debugger in another terminal window:  服务器运行后，在另一个终端窗口中启动调试器：

```sh
fx debug
```
 

To manually validate packages can be loaded, run "ls" from within the Fuchsia shell (for most setups this requires "fx serve" to be successfully servingpackages). 要手动验证是否可以加载软件包，请在Fuchsia shell中运行“ ls”（对于大多数设置，这要求“ fx serve”才能成功提供软件包）。

 
### Manual method  手动方式 

In some cases you may want to run the debug agent and connect manually. To do so, follow these steps: 在某些情况下，您可能需要运行调试代理并手动连接。这样做，请按照下列步骤操作：

 
#### 1. Run the debug agent on the target  1.在目标上运行调试代理 

On the target system pick a port and run the debug agent:  在目标系统上，选择一个端口并运行调试代理：

```sh
run fuchsia-pkg://fuchsia.com/debug_agent#meta/debug_agent.cmx --port=2345
```
 

If you get an error "Cannot create child process: ... failed to resolve ..." it means the debug agent can't be loaded. You may need to run `fx serve` or itsequivalent in your environment to make it available. 如果收到错误“无法创建子进程：...无法解决...”，则表明无法加载调试代理。您可能需要在您的环境中运行`fx serve`或等效的服务，以使其可用。

You will want to note the target's IP address. Run `ifconfig` _on the target_ to see this, or run `fx netaddr` on the host. 您将需要记下目标的IP地址。在目标服务器上运行`ifconfig`来查看此信息，或在主机上运行`fx netaddr`。

 
#### 2. Run the client and connect  2.运行客户端并连接 

On the host system (where you do the build), run the client. Use the IP address of the target and the port you picked above in the `connect` command.If running in-tree, `fx netaddr` will tell you this address. 在主机系统（执行构建的位置）上，运行客户端。使用目标的IP地址和您在connect命令中在上面选择的端口。如果在树中运行，则fx netaddr将告诉您该地址。

For QEMU, we recommend using IPv6 and link local addresses. These addresses have to be annotated with the interface they apply to, so make sure the addressyou use includes the appropriate interface (should be the name of the bridgedevice). 对于QEMU，我们建议使用IPv6并链接本地地址。这些地址必须使用它们所应用的接口进行注释，因此请确保您使用的地址包括适当的接口（应为网桥设备的名称）。

The address should look like `fe80::5054:4d:fe63:5e7a%br0`  地址应类似于`fe80 :: 5054：4d：fe63：5e7a％br0`

```sh
fx zxdb

or

out/<out_dir>/host_x64/zxdb

[zxdb] connect [fe80::5054:4d:fe63:5e7a%br0]:2345
```
 

(Substitute your build directory as-needed).  （根据需要替换您的构建目录）。

If you're connecting or running many times, there are command-line switches:  如果您要连接或运行多次，则可以使用以下命令行开关：

```sh
zxdb -c [fe80::5054:4d:fe63:5e7a%br0]:2345
```
 

 
  * The `status` command will give you a summary of the current state of the debugger. *`status`命令将为您提供调试器当前状态的摘要。

 
  * See `help connect` for more examples, including IPv6 syntax.  *有关更多示例，包括IPv6语法，请参见“帮助连接”。

 
### Read the user guide  阅读用户指南 

Once you're connected, the [user guide](debugger_usage.md) has detailed instructions! 建立连接后，[用户指南]（debugger_usage.md）具有详细的说明！

 
## Tips  提示 

 
### Running out-of-tree  用完树 

You can run with kernels or user programs compiled elsewhere with some extra steps. We hope this will become easier over time. 您可以使用一些其他步骤来在其他位置编译的内核或用户程序运行。我们希望随着时间的推移，这会变得更加容易。

Be aware that we aren't yet treating the protocol as frozen. Ideally the debugger will be from the same build as the operating system itself (moreprecisely, it needs to match the debug\_agent). But the protocol does notchange very often so there is some flexibility. 请注意，我们尚未将协议视为冻结协议。理想情况下，调试器将与操作系统本身具有相同的内部版本（更确切地说，它需要与debug \ _agent匹配）。但是协议不会经常更改，因此具有一定的灵活性。

When you run out-of-tree, you will need to tell zxdb where your symbols and source code are on the local development box (Linux or Mac). Zxdb can not usesymbols in the binary that you pushedf to the Fuchsia target device. 在树外运行时，您需要告诉zxdb，您的符号和源代码在本地开发箱（Linux或Mac）上的位置。 Zxdb不能在推送到Fuchsia目标设备的二进制文件中使用符号。

See [Diagnosing symbol problems](#diagnosing-symbol-problems).  请参阅[诊断符号问题]（诊断符号问题）。

 
#### Set the symbol location  设置符号位置 

To specify new symbol locations for zxdb, use the `-s` command-line flag:  要为zxdb指定新的符号位置，请使用-s命令行标志：

```sh
zxdb -s path/to/my_binary -s some/other_location
```
 

Or add it to the `symbol_paths` list option in the interactive UI:  或将其添加到交互式UI中的“ symbol_paths”列表选项中：

```
[zxdb] set symbol-paths += /my/new/symbol/path
```
 

It's best if your build makes a ".build-id" directory. You then pass the parent directory as a symbol dir. For example, the Fuchsia build itself makes a".build-id" directory inside the build directory. For example, if your builddirectory is `out/x64`: 最好是您的构建创建一个“ .build-id”目录。然后，您将父目录作为符号目录传递。例如，紫红色的构建本身在构建目录中创建一个“ .build-id”目录。例如，如果您的构建目录是“ out / x64”：

```sh
out/x64/host_x64/zxdb -s out/x64
```
 

Some builds produce a file called "ids.txt" that lists build IDs and local paths to the corresponding binaries. This is the second-best option. 一些内部版本会生成一个名为“ ids.txt”的文件，其中列出了内部版本ID和相应二进制文件的本地路径。这是第二好的选择。

If you don't have that, you can just list the name of the file you're debugging directly. You can pass multiple "-s" flags to list multiple symbol locations. 如果没有，您可以直接列出要调试的文件的名称。您可以传递多个“ -s”标志来列出多个符号位置。

The `-s` flag accepts three possible things:  -s标志接受三种可能的情况：

 
   * Directory names. If the given directory contains a ".build-id" subdirectory that will be used. Otherwise all ELF files in the givendirectory will be indexed. *目录名称。如果给定目录包含将使用的“ .build-id”子目录。否则，将索引给定目录中的所有ELF文件。

 
   * File names ending in ".txt". Zxdb will treat this as a "ids.txt" file mapping build IDs to binaries. *文件名以“ .txt”结尾。 Zxdb会将其视为将构建ID映射到二进制文件的“ ids.txt”文件。

 
   * Any other file name will be treated as an ELF file with symbols.  *任何其他文件名将被视为带符号的ELF文件。

 
#### Set the source code location {#set-source-code-location}  设置源代码位置{set-source-code-location} 

The Fuchsia build generates symbols relative to the build directory so relative paths look like `../../src/my_component/file.cc`). 紫红色的构建相对于构建目录生成符号，因此相对路径类似于“ ../../src/my_component/file.cc”）。

If your files are not being found with the default build directories, you will need to provide a build directory to locate the files. This build directory doesnot need have been used to build, it just needs to produce correct absolute pathswhen concatenated with the relative paths from the symbol file. 如果找不到默认构建目录中的文件，则需要提供一个构建目录来查找文件。此构建目录不需要用于构建，仅在与符号文件中的相对路径连接在一起时才需要产生正确的绝对路径。

You can add additional build directories on the command line:  您可以在命令行上添加其他构建目录：

```sh
zxdb -b /home/me/fuchsia/out/x64
```
 

Or interactively from within the debugger:  或在调试器中以交互方式进行：

```
[zxdb] set build-dirs += /home/me/fuchsia/out/x64
```
 

If debugger is finding the wrong file, you can replace the entire build directory list by omitting the `+=`: 如果调试器找到错误的文件，则可以通过省略`+ =`来替换整个构建目录列表：

```
[zxdb] set build-dirs /home/me/fuchsia/out/x64
```
 

If your build produces DWARF symbols with absolute file paths the files must be in that location on the local system. Absolute file paths in the symbols are notaffected by the build search path. Clang users should use the`-fdebug-prefix-map` which will also help with build hermeticity. 如果您的构建产生带有绝对文件路径的DWARF符号，则文件必须位于本地系统上的该位置。符号中的绝对文件路径不受构建搜索路径的影响。 lang语用户应使用-fdebug-prefix-map，这也有助于建立密封性。

 
### Diagnosing symbol problems  诊断符号问题 

 
#### Can't find symbols  找不到符号 

The `sym-stat` command will tell you status for symbols. With no running process, it will give stats on the different symbol locations you havespecified. If your symbols aren't found, make sure these stats match yourexpectations: sym-stat命令将告诉您符号的状态。在没有运行过程的情况下，它将为您指定的不同符号位置提供统计信息。如果找不到您的符号，请确保这些统计信息符合您的期望：

```
[zxdb] sym-stat
Symbol index status

  Indexed  Source path
 (folder)  /home/me/.build-id
 (folder)  /home/me/build/out/x64
        0  my_dir/my_file
```
 

If you see "0" in the "Indexed" column of the "Symbol index stats" that means that the debugger could not find where your symbols are. Try the `-s` flag (see"Running out-of-tree" above) to specify where your symbols are. 如果在“符号索引统计信息”的“索引”列中看到“ 0”，则表示调试器找不到符号所在的位置。尝试使用-s标志（请参见上面的“超出树范围运行”）以指定符号的位置。

Symbol sources using the ".build-id" hierarchy will list "(folder)" for the indexed symbols since this type of source does not need to be indexed. To checkif your hierarchy includes a given build ID, go to ".build-id" inside it, thento the folder with the first to characters of the build ID to see if there is amatching file. 使用“ .build-id”层次结构的符号源将为索引的符号列出“（文件夹）”，因为这种类型的源不需要索引。要检查层次结构是否包含给定的内部版本ID，请转到其中的“ .build-id”，然后转到具有内部版本ID的第一个字符的文件夹，以查看是否存在匹配的文件。

When you have a running program, sym-stat will additionally print symbol information for each binary loaded into the process. If you're not gettingsymbols, find the entry for the binary or shared library in this list. If itsays: 当您有一个正在运行的程序时，sym-stat还将为加载到进程中的每个二进制文件打印符号信息。如果没有符号，请在此列表中找到二进制或共享库的条目。如果有：

```
    Symbols loaded: No
```
 

then that means it couldn't find the symbolized binary on the local computer for the given build ID in any of the locations listed in "Symbol index status".You may need to add a new location with `-s`. 那么这意味着它无法在“符号索引状态”中列出的任何位置的本地计算机上找到给定版本ID的符号二进制文件。您可能需要使用-s添加新位置。

If instead it says something like this:  如果相反，它说像这样：

```
    Symbols loaded: Yes
    Symbol file: /home/foo/bar/...
    Source files indexed: 1
    Symbols indexed: 0
```
 

where "Source files indexed" and "Symbols indexed" is 0 or a very low integer, that means that the debugger found a symbolized file but there are few or nosymbols in it. Normally this means the binary was not built with symbolsenabled or the symbols were stripped. Check your build, you should be passingthe path to the unstripped binary and the original compile line should have a`-g` in it to get symbols. 其中“已索引源文件”和“已索引符号”为0或非常低的整数，这意味着调试器找到了已符号化的文件，但其中几乎没有符号。通常，这意味着二进制文件不是在启用符号的情况下构建的，或者没有删除符号。检查您的构建，您应该将路径传递给未剥离的二进制文件，并且原始编译行中应包含`-g`以获取符号。

 
#### Mismatched source lines  源代码行不匹配 

Sometimes the source file listings may not match the code. The most common reason is that the build is out-of-date and no longer matches the source. Thedebugger will check that the symbol file modification time is newer than thesource file, but it will only print the warning the first time the file isdisplayed. Check for this warning if you suspect a problem. 有时源文件列表可能与代码不匹配。最常见的原因是内部版本已过时并且不再与源匹配。调试器将检查符号文件的修改时间是否比源文件新，但是它只会在第一次显示文件时打印警告。如果您怀疑有问题，请检查此警告。

Some people have multiple checkouts. If it's finding a file in the wrong one, override the `build-dirs` option as described above in [Set the source codelocation](#set-source-code-location). 有些人有多个结帐。如果找到错误的文件，请覆盖上面的[设置源代码位置]（set-source-code-location）中所述的“ build-dirs”选项。

To display the file name of the file it found from `list`, use the `-f` option:  要显示从“列表”找到的文件的文件名，请使用-f选项：

```
[zxdb] list -f
/home/me/fuchsia/out/x64/../../src/foo/bar.cc
 ... <source code> ...
```
 

You can also set the `show-file-paths` option. This will increase file path information: 您还可以设置`show-file-paths`选项。这将增加文件路径信息：

 
  * It will show the full resolved path in source listings as in `list -f`.  *它将在源列表中显示完整的解析路径，如`list -f`中所示。
  * It will show the full path instead of just the file name in other places such as backtraces. *在回溯之类的其他位置，它将显示完整路径，而不仅仅是文件名。

```
[zxdb] set show-file-paths true
```
 

You may notice a mismatch when setting a breakpoint on a specific line where the displayed breakpoint location doesn't match the line number you typed. Inmost cases, this is because this symbols did not identifty any code on thespecified line so the debugger used the next line. It can happen even inunoptimized builds, and is most common for variable declarations. 在显示的断点位置与您键入的行号不匹配的特定行上设置断点时，您可能会发现不匹配。在大多数情况下，这是因为该符号未标识指定行上的任何代码，因此调试器使用了下一行。甚至在未优化的构建中也可能发生这种情况，这在变量声明中最为常见。

```
[zxdb] b file.cc:23
Breakpoint 1 (Software) @ file.cc:138
   138   int my_value = 0;
 ◉ 139   DoSomething(&my_value);
   140   if (my_value > 0) {
```
 

 
## Debugging the debugger and running the tests  调试调试器并运行测试 

 
### Client  客户 

For developers working on the debugger, you can activate the `--debug-mode` flag that will activate many logging statements for the debugger: 对于使用调试器的开发人员，您可以激活--debug-mode标志，该标志将为调试器激活许多日志记录语句：

```
zxdb --debug-mode
```
 

You can also debug the client on GDB or LLDB on your host machine. You will want to run the unstripped binary: `out/<yourbuild>/host_x64/exe.unstripped/zxdb`.Since this path is different than the default, you will need to specify thelocation of ids.txt (in the root build directory) with `-s` on the command line. 您还可以在主机上的GDB或LLDB上调试客户端。您将要运行解压缩后的二进制文件：`out / <yourbuild> / host_x64 / exe.unstripped / zxdb`。由于此路径与默认路径不同，因此您需要指定ids.txt的位置（在根构建目录中） ），并在命令行上使用`-s`。

There are tests for the debugger that run on the host. These are relevant if you're working on the debugger client. 在主机上运行调试器的测试。如果您在调试器客户端上工作，则这些是相关的。

```sh
fx run-host-tests zxdb_tests
```
 

or directly with  或直接与

```sh
out/x64/host_tests/zxdb_tests
```
 

 
### Debug Agent  调试代理 

Similar as with the client, the debug agent is programmed to log many debug statements when run with the `--debug-mode` flag: 与客户端类似，调试代理被编程为在使用`--debug-mode`标志运行时记录许多调试语句：

```
run fuchsia-pkg://fuchsia.com/debug_agent#meta/debug_agent.cmx --debug-mode
```
 

It is also possible to attach the debugger to the debugger. The preferred way to do this is to make zxdb catch the debugger on launch using the filteringfeature. This is done frequently by the debugger team. See the[user guide](debugger_usage.md) for more details: 也可以将调试器附加到调试器。首选的方法是使用过滤功能使zxdb在启动时捕获调试器。调试器团队经常这样做。有关更多详细信息，请参见[用户指南]（debugger_usage.md）：

```
// Run the debugger that will attach to the "to-be-debugged" debug agent.
fx debug

// * Within zxdb.
[zxdb] attach debug_agent

// Launch another debug agent manually
// * Within the target (requires another port).
run fuchsia-pkg://fuchsia.com/debug_agent#meta/debug_agent.cmx --port=5000 --debug-mode

// * Within the first zxdb:
Attached Process 1 [Running] koid=12345 debug_agent.cmx
  The process is currently in an initializing state. You can set pending
  breakpoints (symbols haven't been loaded yet) and "continue".
[zxdb] continue

// Now there is a running debug agent that is attached by the first zxdb run.
// You can also attach to it using another client (notice the port):
fx zxdb --connect [<IPv6 to target>]:5000 --debug-mode

// Now you have two running instances of the debugger!
```
 

Note: Only one debugger can be attached to the main job in order to auto-attach to new processes. Since you're using it for the first debugger, you won't beable to launch components with the second one, only attach to them. 注意：为了自动附加到新进程，只能将一个调试器附加到主作业。由于您将其用于第一个调试器，因此无法与第二个调试器一起启动组件，而只能将它们附加到它们。

To run the debug agent tests:  要运行调试代理测试：

```
fx run-test debug_agent_tests
```
 

 
## Other Languages  其他语言 

Rust mostly works but there [are issues](https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5462). Go currently is currently not supported. Rust大部分可以工作，但是有[问题]（https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5462）。当前不支持“ Go Go”。

