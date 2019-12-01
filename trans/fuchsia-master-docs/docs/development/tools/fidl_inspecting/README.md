 
# fidlcat: Monitor and debug your fidl calls  fidlcat：监视和调试您的fidl调用 

 
## Overview  总览 

fidlcat is a tool that allows users to monitor FIDL connections. Currently, it can attach to or launch a process on a Fuchsia device, and will report its FIDLtraffic. fidlcat是允许用户监视FIDL连接的工具。当前，它可以附加到紫红色设备上或在其上启动一个过程，并将报告其FIDLtraffic。

 
## Enabling it  启用它 

To run fidlcat in-tree, you first build it, which you can do the following way:  要在树中运行fidlcat，首先要构建它，您可以通过以下方式进行：

```sh
fx set <whatever> --with //bundles:tools
fx build
```
 

If you want to add it to your existing gn args, you can do so by adding this stanza to the bottom of your <build_dir>/args.gn. 如果要将其添加到现有的gn args中，可以通过将此节添加到<build_dir> /args.gn的底部来实现。

```
universe_package_labels += [ "//bundles:tools" ]
```
 

To run fidlcat, you must boot with networking enabled.  要运行fidlcat，必须在启用网络的情况下引导。

For QEMU networking support, you need to setup your system with a TUN/TAP interface. Then, run: 为了获得QEMU网络支持，您需要使用TUN / TAP界面设置系统。然后，运行：

```sh
fx emu -N
```
 

In a separate console, you need to ensure your target is able to fetch updates:  在单独的控制台中，您需要确保目标能够获取更新：

```sh
fx serve
```
 

 
## Running it  运行它 

When your environment is properly set up, and fidlcat is built, you should be able to use it to monitor FIDL messages from processes on the target. There areseveral ways to do this. 正确设置环境并构建fidlcat后，您应该可以使用它来监视来自目标上进程的FIDL消息。有几种方法可以做到这一点。

 
### Attaching to a running process  附加到正在运行的进程 

If you run the `ps` command in the shell, you can get a pid you want to monitor, and run: 如果在外壳中运行“ ps”命令，则可以获取要监视的pid，然后运行：

```sh
fx fidlcat --remote-pid=<pid>
```
 

If your code is executed by a runner, you are likely to want to attach to the runner. For Dart JIT-executed code, run `ps` on the target, and look for the process named `dart_jit_runner`: 如果您的代码是由运行程序执行的，则您可能希望附加到运行程序。对于Dart JIT执行的代码，在目标上运行`ps`，并查找名为`dart_jit_runner`的进程：

```sh
host$ fx shell ps
[...]
        j:21102           17.6M   17.6M
          p:21107         17.6M   17.6M     32k         dart_jit_runner.cmx
```
 

You can then attach directly to that process, and view all FIDL messages sent by Dart programs: 然后，您可以直接附加到该过程，并查看Dart程序发送的所有FIDL消息：

```sh
host$ fx fidlcat --remote-pid=21107
```
 

You can use the `--remote-pid` flag multiple times to connect to multiple processes:  您可以多次使用--remote-pid标志来连接到多个进程：

```sh
fx fidlcat --remote-pid=<pid1> --remote-pid=<pid2>
```
 

 
### Launching a component with fidlcat  使用fidlcat启动组件 

Alternatively, you can launch a component directly using its URL:  另外，您可以直接使用其URL启动组件：

```sh
fx fidlcat run fuchsia-pkg://fuchsia.com/echo_client_rust#meta/echo_client_rust.cmx
```
 

You can also specify the URL with a bash regex that matches a unique URL known to the build:  您还可以使用bash正则表达式指定该URL，该正则表达式与构建已知的唯一URL相匹配：

```sh
fx fidlcat run "echo_client_cpp_synchronous.*"
fx fidlcat run echo_client_cpp.cmx
```
 

 
### Attaching to a program on startup  启动时附加到程序 

You can also attach to programs with their names by passing a regex to match their names. Fidlcat will attach to all currently running andsubsequently started programs that satisfy the regex. If you issue the followingcommand, fidlcat will connect to the system, and attach to all programs with thesubstring "echo_client". 您还可以通过传递正则表达式以匹配其名称来附加其名称的程序。 Fidlcat将附加到满足正则表达式的所有当前正在运行且随后启动的程序。如果发出以下命令，则fidlcat将连接到系统，并使用“ echo_client”子字符串附加到所有程序。

```sh
fx fidlcat --remote-name=echo_client
```
 

 
### Mixed use  混合使用 

All three options --remote-pid, --remote-name and run can be used together. However, run must always be the last one. --remote-pid，-remote-name和run这三个选项可以一起使用。但是，运行必须始终是最后一个。

When --remote-name and run are used together, only processes which match --remote-name are monitored. 当--remote-name和run一起使用时，仅监视与--remote-name匹配的进程。

Examples (echo_server is launched by echo_client):  示例（echo_server由echo_client启动）：

```sh
fx fidlcat run echo_client_cpp.cmx
```
Run and monitor echo_client.  运行并监视echo_client。

```sh
fx fidlcat --remote-name=echo_client run echo_client_cpp.cmx
```
Run and monitor echo_client.  运行并监视echo_client。

```sh
fx fidlcat --remote-name=echo_server run echo_client_cpp.cmx
```
Run echo_client and monitor echo_server.  运行echo_client并监视echo_server。

```sh
fx fidlcat --remote-name=echo run echo_client_cpp.cmx
```
Run echo_client and monitor echo_client and echo_server.  运行echo_client并监视echo_client和echo_server。

```sh
fx fidlcat --remote-name=echo_client --remote-name=echo_server run echo_client_cpp.cmx
```
Run echo_client and monitor echo_client and echo_server.  运行echo_client并监视echo_client和echo_server。

 
## Running without the fx tool  在没有FX工具的情况下运行 

Note that fidlcat needs two sources of information to work:  请注意，fidlcat需要两个信息源才能工作：

 
 * First, it needs the symbols for the executable. In practice, if you are running in-tree, the symbols should be provided to fidlcat automatically.Otherwise, you can provide fidlcat a symbol path, which can be a text filethat maps build ids to debug symbols, an explicit ELF file path, or adirectory it will scan for ELF files and index. The -s flag can take a) adirectory containing ELF files, b) a directory containing a .build_idsubfolder adhering to the standard for such subfolders, or c) an ELF file.An alternate flag, --symbol-repo-paths, can be used to pass a directorycontaining the contents of a build_id folder (this is useful if the directoryis not named .build_id). *首先，它需要可执行文件的符号。实际上，如果您在树中运行，则应将符号自动提供给fidlcat，否则，可以为fidlcat提供符号路径，该路径可以是将构建ID映射到调试符号的文本文件，显式ELF文件路径或目录将扫描ELF文件和索引。 -s标志可以包含a）包含ELF文件的目录，b）包含遵循此类子文件夹标准的.build_id子文件夹的目录，或c）ELF文件。-symbol-repo-paths可以是另一个标志用于传递包含build_id文件夹内容的目录（如果该目录未命名为.build_id，则很有用）。

 
 * Second, it needs the intermediate representation for the FIDL it ingests, so it can produce readable output. If you are running in-tree, the IR should beprovided to fidlcat automatically. Otherwise, you can provide fidlcat an IRpath, which can be an explicit IR file path, a directory it will scan for IRfiles, or an argument file containing explicit paths. This can be providedto fidlcat with the `--fidl-ir-path` flag. The argument files need to beprepended with a `@` character: `--fidl-ir-path @argfile`. *其次，它需要它所摄取的FIDL的中间表示形式，以便可以产生可读的输出。如果您在树中运行，则应该自动将IR设置为fidlcat。否则，您可以为fidlcat提供一个IRpath，该IRpath可以是显式IR文件路径，它将扫描IRfile的目录或包含显式路径的参数文件。可以用--fidl-ir-path`标志提供给fidlcat。参数文件必须以'@`字符开头：--fidl-ir-path @ argfile`。

 
 * Third, regex URL matching does not work outside of the fx tool. You must specify the entire package URL. *第三，正则表达式URL匹配在fx工具之外不起作用。您必须指定整个程序包URL。

Finally, if you are running fidlcat without the fx tool, the debug agent needs to be running on the target. Connect to the target and run: 最后，如果您在没有fx工具的情况下运行fidlcat，则调试代理需要在目标上运行。连接到目标并运行：

```sh
run fuchsia-pkg://fuchsia.com/debug_agent#meta/debug_agent.cmx --port=8080
```
 

And, when you run fidlcat on the host, make sure you connect to that agent:  并且，在主机上运行fidlcat时，请确保连接到该代理：

```sh
tools/fidlcat --connect [$(fx netaddr --fuchsia)]:8080 <other args>
```
 

 
## Read the guide  阅读指南 

The [fidlcat guide](fidlcat_usage.md) describes all the flags which modify the output. It also gives some examples of display interpretation. [fidlcat指南]（fidlcat_usage.md）描述了所有修改输出的标志。它还提供了一些显示解释的示例。

 
## Where is the code?  代码在哪里？ 

