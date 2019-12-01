 
# zxdb: Fuchsia native debugger user guide  zxdb：紫红色的本地调试器用户指南 

This is the command usage guide for zxdb. Please see also:  这是zxdb的命令用法指南。另请参阅：

 
  * The [setup and troubleshooting guide](README.md).  * [设置和故障排除指南]（README.md）。

 
## Quick start  快速开始 

 
### Connecting in-tree  连接树中 

In-tree developers should use the `fx debug` command to start the debugger. The system must already be running and reachable via networking from your computer: 树内开发人员应使用“ fx debug”命令启动调试器。该系统必须已经在运行，并且可以通过计算机通过网络访问：

```
$ scripts/fx debug
Attempting to start the Debug Agent.
Waiting for the Debug Agent to start.
Connecting (use "disconnect" to cancel)...
Connected successfully.
[zxdb]
```
 

The `status` command will give the current state of the debugger. Be aware if the remote system dies the debugger won't always notice the connection is gone. 状态命令将给出调试器的当前状态。请注意，如果远程系统死了，调试器将不会总是注意到连接已消失。

 
### Debugging a process or component.  调试过程或组件。 

Running a process on Fuchsia is more complicated than in other systems because there are different loader environments (see "A note about launcherenvironments" below). 在Fuchsia上运行进程比在其他系统上更为复杂，因为存在不同的加载器环境（请参见下面的“有关启动器环境的说明”）。

The only want to reliably debug all types of processes is to create a filter on the process name via "attach" and start it the normal way you would start thatprocess. The process name is usually the name of the build target thatgenerates it. To check what this is, use "ps" (either in the debugger or from asystem shell) with it running. 要可靠地调试所有类型的进程，唯一的希望是通过“ attach”在进程名称上创建一个过滤器，并以正常方式启动该进程来启动它。进程名称通常是生成它的构建目标的名称。要检查这是什么，请在运行时使用“ ps”（在调试器中或从系统外壳程序中）。

> Note: only the first 32 bytes of the name are included in the Zircon process > description. Sometimes the number of path components can cause the name to be> truncated. If the filter isn't working, check the actual name in "ps". We hope> to have a better way to match this in the future. >注意：名称的前32个字节仅包含在Zircon进程>描述中。有时，路径组件的数量可能会导致名称>被截断。如果过滤器不起作用，请检查“ ps”中的实际名称。我们希望>将来有更好的方法来匹配此功能。

This example sets a pending breakpoint on `main` to stop at the beginning of execution, and waits for a process called "my_app" to start: 本示例在`main`上设置一个待处理的断点以在执行开始时停止，并等待一个名为“ my_app”的进程启动：

```
[zxdb] attach my_app
Waiting for process matching "my_app"

[zxdb] break main
Breakpoint 1 (Software) on Global, Enabled, stop=All, @ main
Pending: No matches for location, it will be pending library loads.
```
 

Then run the process the way you would in normal use (direcly on the command line, via `fx run-test`, via the shell's `run fuchsia-pkg://...`, or anotherway. The debugger should then immediately break on `main` (it may take sometime to load symbols so you may see a delay before showing the source code): 然后以您通常使用的方式运行该过程（直接在命令行上，通过`fx run-test`，或者通过shell的`run fuchsia-pkg：// ...，或者以其他方式运行。然后，调试器应立即在`main`上中断（加载符号可能需要一些时间，因此您可能会在显示源代码之前看到延迟）：

```
Attached Process 1 [Running] koid=51590 my_app.cmx
🛑 on bp 1 main(…) • main.cc:222
   220 }
   221
 ▶ 222 int main(int argc, const char* argv[]) {
   223   foo::CommandLineOptions options;
   224   cmdline::Status status = ParseCommandLine(argc, argv, &options);
```
 

You can then do basic commands that are similar to GDB:  然后，您可以执行类似于GDB的基本命令：

```
next
step
print argv[1]
continue
quit
```
 

 
#### A note about launcher environments  关于启动器环境的说明 

The following loader environments all have different capabilities (in order from least capable to most capable): 以下加载器环境均具有不同的功能（从能力最差到能力最强）：

 
  * The debugger's `run <file name>` command (base system process stuff).  *调试器的“运行<文件名>”命令（基本系统进程的东西）。
  * The system console or `fx shell` (adds some libraries).  *系统控制台或`fx shell`（添加了一些库）。
  * The base component environment via the shell's `run` and the debugger's `run -c <package url>` (adds component capabilities). *通过shell的`run`和调试器的`run -c <package url>`的基本组件环境（添加了组件功能）。
  * The test environment via `fx run-test`.  *通过`fx run-test`测试环境。
  * The user environment when launched from a "story" (adds high-level services like scenic). *从“故事”启动时的用户环境（添加了风景秀丽的高级服务）。

This panoply of environments is why the debugger can't have a simple "run" command that always works. 如此多的环境是为什么调试器无法使用始终有效的简单“运行”命令的原因。

 
### Launching simple command-line processes  启动简单的命令行过程 

Minimal console apps including some unit tests can be launched directly from within the debugger which avoids the "attach" dance: 可以从调试器中直接启动包含某些单元测试的最小控制台应用程序，从而避免“附加”冲突：

```
[zxdb] break main
Breakpoint 1 (Software) on Global, Enabled, stop=All, @ @main
Pending: No matches for location, it will be pending library loads.

[zxdb] run /bin/cowsay
```
 

If you get a shared library load error or errors about files or services not being found, it means the app can't be run from within the debugger's launcherenvironment. This is true even for things that may seem relatively simple. 如果您遇到共享库加载错误或有关找不到文件或服务的错误，则意味着该应用程序无法在调试器的启动器环境中运行。即使对于看似相对简单的事情也是如此。

 
### Directly launching components  直接启动组件 

Components that can be executed with the console comand `run fuchsia-pkg://...` can be loaded in the debugger with the following command, substituting yourcomponent's URL: 可以使用以下命令替换urlcomponents URL，将可通过控制台命令`run fuchsia-pkg：// ...`执行的组件加载到调试器中：

```
[zxdb] run -c fuchsia-pkg://fuchsia.com/your_app#meta/your_app.cmx
```
 

Not all components can be launched this way since most higher-level services won't be accessible: if you can't do `run ...` from the system console, itwon't work from the debugger either. Note also that `fx run-test` is adifferent environment. According to your test's dependencies, it may or may notwork from the debugger's `run` command. 由于无法访问大多数更高级别的服务，因此并非所有组件都可以通过这种方式启动：如果无法从系统控制台执行“运行...”，那么调试器也将无法运行。还要注意，`fx run-test`是不同的环境。根据测试的依赖性，调试器的run命令可能会也可能无法工作。

 
### Attaching to an existing process  附加到现有流程 

You can attach to most running processes given the process’ KOID. You can get the KOID by running `ps` on the target Fuchsia system. zxdb also has a built-in`ps` command: 给定进程的KOID，您可以将其附加到大多数正在运行的进程。您可以通过在目标紫红色系统上运行`ps`来获得KOID。 zxdb还具有内置的ps命令：

```
[zxdb] ps
j: 1030 root
  j: 1079 zircon-drivers
    p: 1926 devhost:sys
...
```
 

Then to attach:  然后附上：

```
[zxdb] attach 3517
Process 1 Running koid=1249 pwrbtn-monitor
```
 

When you’re done, you can choose to `detach` (keep running) or `kill` (terminate) the process. 完成后，您可以选择“分离”（继续运行）或“杀死”（终止）过程。

 
## Interaction model  互动模式 

Most command-line debuggers use an exclusive model for input: you’re either interacting with the debugged process’ stdin and stdout, or you’re interactingwith the debugger. In contrast, zxdb has an asynchronous model similar to mostGUI debuggers. In this model, the user is exclusively interacting with thedebugger while arbitrary processes or threads are running or stopped. 大多数命令行调试器使用专用模型进行输入：您是在与调试进程的stdin和stdout进行交互，还是在与调试器进行交互。相反，zxdb具有类似于大多数GUI调试器的异步模型。在此模型中，当任意进程或线程正在运行或停止时，用户仅与调试器进行交互。

When the debugger itself launches a program it will print the program's stdout and stderr to the console. When you attach (either with a filter or with the`attach` command) they will go to the original place. Currently there is no wayto interact with a process’ stdin. 当调试器本身启动程序时，它将打印程序的stdout和stderr到控制台。当您附加（使用过滤器或使用`attach`命令）时，它们将转到原始位置。当前没有与流程的标准输入进行交互的方法。

zxdb has a regular noun/verb model for typed commands. The rest of this section gives an overview of the syntax that applies to all commands. Specific commandswill be covered in the “Task guide” section below. zxdb具有用于键入命令的常规名词/动词模型。本节的其余部分概述了适用于所有命令的语法。具体的命令将在下面的“任务指南”部分中介绍。

 
### Nouns  名词 

The possible nouns (and their abbreviations) are:  可能的名词（及其缩写）为：

 
  * `process` (`pr`)  *`process`（`pr`）
  * `job` (`j`)  *`job`（`j`）
  * `thread` (`t`)  *`thread`（`t`）
  * `frame` (`f`)  *`frame`（`f`）
  * `breakpoint` (`bp`)  *`breakpoint`（`bp`）

 
#### Listing nouns  列出名词 

If you type a noun by itself, it lists the available objects of that type:  如果您自己键入一个名词，它将列出该类型的可用对象：

 
  * List attached processes  *列出附加流程

    ```
    [zxdb] process
      # State       Koid Name
    ▶ 1 Not running 3471 debug_agent_unit_tests.cmx
    ```
 

 
  * List attached jobs  *列出附加工作

    ```
    [zxdb] job
      # State   Koid Name
    ▶ 1 running 3471 sys
    ```
 

 
  * List threads in the current process:  *列出当前进程中的线程：

    ```
    [zxdb] thread
      # State   Koid Name
    ▶ 1 Blocked 1348 initial-thread
      2 Blocked 1356 some-other-thread
    ```
 

 
  * List stack frames in the current thread (the thread must be stopped—see `pause` below): *列出当前线程中的堆栈帧（该线程必须停止，请参阅下面的“暂停”）：

    ```
    [zxdb] frame
    ▶ 0 fxl::CommandLineFromIterators<const char *const *>() • command_line.h:203
      1 fxl::CommandLineFromArgcArgv() • command_line.h:224
      2 main() • main.cc:174
    ```
 

 
#### Selecting defaults  选择默认值 

If you type a noun and its index, you select that as the default for subsequent commands. It also tells you the stats about the new default. 如果键入名词及其索引，则将其选择为后续命令的默认值。它还会告诉您有关新默认值的统计信息。

 
  * Select thread 3 to be the default for future commands:  *选择线程3作为以后命令的默认值：

    ```
    [zxdb] thread 3
    Thread 3 Blocked koid=9940 worker-thread
    ```
 

 
  * Select breakpoint 2 to be the default:  *选择断点2​​为默认值：

    ```
    [zxdb] breakpoint 2
    Breakpoint 2 (Software) on Global, Enabled, stop=All, @ MyFunction
    ```
 

 
### Verbs  动词 

By default, a verb (`run`, `next`, `print`, etc.) applies to the current defaults. So to evaluate an expression in the context of the current stackframe, just type `print` by itself: 默认情况下，动词（“ run”，“ next”，“ print”等）适用于当前默认值。因此，要在当前堆栈框架的上下文中评估表达式，只需单独键入`print`即可：

```
[zxdb] print argv[1]
"--foo=bar"
```
 

You can override the default context by prefixing the verb with a noun and its index. So to evaluate an expression in the context of a specific stack frame(in this case, frame 2 of the current thread): 您可以通过在动词之前加上名词及其索引来覆盖默认上下文。因此，要在特定堆栈框架（在本例中为当前线程的框架2）的上下文中评估表达式：

```
[zxdb] frame 2 print argv[1]
"--foo=bar"
```
 

You can keep adding different types of context. This specifies the process, thread, and frame for the print command: 您可以继续添加不同类型的上下文。这指定了打印命令的进程，线程和框架：

```
[zxdb] process 1 thread 1 frame 2 print argv[1]
"--foo=bar"
```
 

 
# Attaching and running  附加并运行 

 
### Debugging drivers  调试驱动程序 

It's not currently possible to set up the debugger early enough in system startup to debug most driver initialization. And since zxdb itself uses thenetwork, no drivers associated with network communication can be debugged. 当前无法在系统启动时足够早地设置调试器来调试大多数驱动程序初始化。而且由于zxdb本身使用网络，因此无法调试与网络通信关联的驱动程序。

Driver debugging support is tracked in issue [5456](<https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5456). 在问题[5456]（<https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5456）中跟踪了驱动程序调试支持。

You can debug running drivers by attaching like any other process (see “Attaching to an existing process” below). You can delay initialization toallow time to attach by adding a busyloop at the beginning of your code: 您可以通过附加任何其他进程来调试正在运行的驱动程序（请参见下面的“附加到现有进程”）。您可以通过在代码的开头添加一个busyloop来延迟初始化以留出时间来附加：

```
volatile bool stop = false;
while (!stop) {}
```
 

To break out of the loop after attaching, either set the variable to true:  要在附加后脱离循环，可以将变量设置为true：

```
[zxdb] print stop = true
true
[zxdb] continue
```
 

Or jump to the line after the loop:  或在循环后跳到该行：

```
[zxdb] jump <line #>
[zxdb] continue
```
 

 
### Debugging crash dumps  调试故障转储 

You can load a minidump generated by a crash report. Use the "opendump" verb and supply the local file name of the dump. The debugger must not be attachedto another dump or a running system (use "disconnect" first if so). 您可以加载崩溃报告生成的小型转储。使用“ opendump”动词并提供转储的本地文件名。调试器不得连接到其他转储或正在运行的系统（如果是，请首先使用“断开连接”）。

```
[zxdb] opendump upload_file_minidump-e71256ba30163a0.dmp
Opening dump file
Dump loaded successfully.
```
 

Now the thread, stack, and memory commands can be used to inspect the state of the program. Use "disconnect" to close the dump. 现在，线程，堆栈和内存命令可用于检查程序的状态。使用“断开连接”关闭转储。

For in-tree users, the `fx debug` command can take the path to a core file as an argument.  对于树内用户，`fx debug`命令可以将核心文件的路径作为参数。

```
fx debug -c upload_file_minidump-e71256ba30163a0.dmp
```
 

 
#### Downloading symbols  下载符号 

You can tell `zxdb` to look for debug symbols for your core dump in a GCS bucket and download them automatically. You'll need to run with a few command-line options: 您可以告诉`zxdb`在GCS存储桶中查找核心转储的调试符号，然后自动下载它们。您需要使用一些命令行选项来运行：

```
zxdb --symbol-cache $HOME --symbol-server gs://my-bucket-name
```
 

In-tree users will automatically have these options set, with the server pointed to a bucket containing symbols for all release builds. 树内用户将自动设置这些选项，服务器指向包含所有发行版本符号的存储桶。

The first time you use the symbol server, you will have to authenticate using the `auth` command. The authentication flow will require you to complete part of the authentication in your browser. 首次使用符号服务器时，必须使用auth命令进行身份验证。身份验证流程将要求您在浏览器中完成部分身份验证。

```
[zxdb] auth
To authenticate, please supply an authentication token. You can retrieve a token from:

https://accounts.google.com/o/oauth2/v2/< very long URL omitted >

Once you've retrieved a token, run 'auth <token>'

[zxdb] auth 4/hAF-pASODIFUASDIFUASODIUFSADF329827349872V6
Successfully authenticated with gs://fuchsia-infra-debug-symbols
```
 

 
### Debugging multiple processes  调试多个进程 

You can debug many arbitrary processes at the same time. When you start, one “process context” (the container that may or may not have a running process)is created for you to use. When you run or attach, that process becauseassociated with that context. 您可以同时调试许多任意进程。当您开始时，将创建一个“进程上下文”（可能具有也可能没有正在运行的进程的容器）供您使用。当您运行或附加时，该过程是与该上下文相关联的。

To debug a second program, create a new context with:  要调试第二个程序，请使用以下命令创建一个新的上下文：

```
[zxdb] process new
```
 

This will clone the current process’ settings into a new context but not run anything yet. You can then run or attach as normal. 这样会将当前流程的设置克隆到新的上下文中，但尚未运行任何内容。然后，您可以正常运行或附加。

Recall from the “Interaction model” section you can list the current processes with: 在“交互模型”部分中，您可以使用以下命令列出当前进程：

```
[zxdb] process
  # State       Koid Name
▶ 1 Running     1249 pwrbtn-monitor
  2 Not running 7235 pwrbtn-monitor
```
 

Select one of those as the default by providing its index (not KOID):  通过提供其索引（不是KOID）来选择其中之一作为默认值：

```
[zxdb] process 2
```
 

Or apply commands to a specific process (even if it’s not the default) with:  或使用以下命令将命令应用于特定进程（即使不是默认命令）：

```
[zxdb] process 2 pause
```
 

 
# Running  跑步 

 
### Working with breakpoints  使用断点 

Breakpoints stop execution when some code is executed. To create a breakpoint, use the `break` command (`b` for short) and give it a location: 当执行某些代码时，断点将停止执行。要创建一个断点，使用`break`命令（简称`b`）并为其指定一个位置：

```
[zxdb] break main
Breakpoint 3 (Software) on Global, Enabled, stop=All, @ main
   180
 ◉ 181 int main(int argc, char**argv) {
   182     fbl::unique_fd dirfd;
```
 

A location can be expressed in many different ways.  位置可以用许多不同的方式表示。

 
  * Plain function name. This will match functions with the name in any namespace: *普通函数名称。这将使函数与任何名称空间中的名称匹配：

    ```
    break main
    ```
 

 
  * Member function or functions inside a specific namespace or class:  *成员函数或特定命名空间或类内的函数：

    ```
    break my_namespace::MyClass::MyFunction
    break ::OtherFunction
    ```
 

 
  * Source file + line number (separate with a colon):  *源文件+行号（以冒号分隔）：

    ```
    break mymain.cc:22
    ```
 

 
  * Line number within the current frame’s current source file (useful when stepping): *当前帧当前源文件中的行号（步进时很有用）：

    ```
    break 23
    ```
 

 
  * Memory address:  *内存地址：

    ```
    break 0xf72419a01
    ```
 

To list all breakpoints:  列出所有断点：

```
[zxdb] breakpoint
```
 

> Note: this is the “breakpoint” noun (a noun by itself lists the things > associated with it). It is not plural. >注意：这是“断点”名词（名词本身会列出与之关联的事物）。它不是复数。

To clear a specific breakpoint, give that breakpoint index as the context for the clear command (see “Interaction model” above). Here’s we’re using theabbreviation for `breakpoint` (`bp`): 要清除特定的断点，请将该断点索引作为clear命令的上下文（请参见上面的“交互模型”）。这是我们为`breakpoint`（`bp`）使用的缩写：

```
[zxdb] bp 2 clear
```
 

Or you can clear the current breakpoint:  或者您可以清除当前断点：

```
[zxdb] clear
```
 

Whenever you create or stop on a breakpoint, that breakpoint becomes the default automatically so clear always clears the one you just hit. Note thatunlike GDB, “clear” takes a breakpoint context before the verb and there arenever any arguments after it. Support for GDB-like “clear <location>” isissue [5452](https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5452). 每当您在断点上创建或停止时，该断点将自动成为默认断点，因此clear始终清除您刚刚命中的断点。请注意，与GDB不同，“清除”在动词之前使用断点上下文，并且在其后没有任何自变量。支持类似GDB的“ clear <location>” isissue [5452]（https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5452）。

 
### Programatic breakpoints  程序断点 

You can insert a hardcoded breakpoint in your code if you want to catch some specific condition. Clang has a builtin (it won't work in GCC Zircon builds): 如果要捕获某些特定条件，可以在代码中插入硬编码的断点。 Clang具有内置功能（不适用于GCC Zircon构建）：

```
__builtin_debugtrap();
```
 

If the debugger is already attached to the process, it will stop as if a normal breakpoint was hit. You can step or continue from there. If the debugger isnot already attached, this will cause a crash. 如果调试器已经连接到该进程，它将停止，就像遇到了正常的断点一样。您可以步进或从那里继续。如果尚未附加调试器，则将导致崩溃。

 
### Working with threads  使用线程 

To list the current process’ threads (see “Interaction model” above for more):  要列出当前进程的线程（有关更多信息，请参见上面的“交互模型”）：

```
[zxdb] thread
  # State   Koid Name
▶ 1 Blocked 1323 initial-thread
  2 Running 3462 worker-thread
```
 

Often when you attach to a process the thread will be “blocked”, meaning it is stopped on a system call. For asynchronous programs this will typically be somekind of wait. 通常，当您附加到进程时，线程将被“阻塞”，这意味着它在系统调用时停止了。对于异步程序，这通常会有点等待。

Most thread control and introspection commands only work when a thread is suspended (not blocked or running). A thread will be suspended when it isstopped at a breakpoint or crashes. You can explicitly suspend a thread withthe `pause` command: 大多数线程控制和自省命令仅在线程挂起（而不是阻塞或运行）时才起作用。当线程在断点处停止或崩溃时，该线程将被挂起。您可以使用“ pause”命令显式暂停线程：

```
[zxdb] thread 2 pause
🛑 syscalls-x86-64.S:67
   65 m_syscall zx_port_create 60 2 1
   66 m_syscall zx_port_queue 61 2 1
 ▶ 67 m_syscall zx_port_wait 62 3 0
   68 m_syscall zx_port_cancel 63 3 1
   69 m_syscall zx_timer_create 64 3 1
```
 

> When a thread is paused the debugger will show the current source code > location. Often threads will be in a system call which will resolve to the> location in the assembly-language macro file that generated the system call> as shown in the above example. >线程暂停时，调试器将显示当前源代码>位置。通常线程将在系统调用中，该调用将解析为生成系统调用的汇编语言宏文件中的>位置，如上例所示。

Running `pause` by itself with no context will pause all threads of all processes currently attached: 在没有上下文的情况下单独运行`pause`将暂停当前连接的所有进程的所有线程：

```
[zxdb] pause
```
 

Unpause a thread with `continue`. As before, `continue` with no context will resume all threads: 用`continue`取消暂停线程。和以前一样，没有上下文的`continue`将恢复所有线程：

```
[zxdb] continue
```
 

Or continue a specific thread:  或继续特定的线程：

```
[zxdb] thread 1 continue
```
 

 
### Working with stack frames  使用堆栈框架 

A stack frame is a function call. When a function calls another function, a new nested frame is created. So listing the frames of a thread tells you the callstack. You can only see the stack frames when a thread is suspended (see“Working with threads” above). 堆栈框架是一个函数调用。当一个函数调用另一个函数时，将创建一个新的嵌套框架。因此，列出线程的帧会告诉您调用堆栈。仅当线程被挂起时，您才能看到堆栈帧（请参见上面的“使用线程”）。

To list the current thread’s stack frames (the `f` abbreviation will also work). 要列出当前线程的堆栈框架（f的缩写也可以）。

```
[zxdb] frame
▶ 0 fxl::CommandLineFromIterators<const char *const *>() • command_line.h:203
  1 fxl::CommandLineFromArgcArgv() • command_line.h:224
  2 main() • main.cc:174
```
 

And to select a given frame as the default:  并选择给定的框架作为默认框架：

```
[zxdb] frame 2
```
 

Frames are numbered with “0” being the top of the stack. Increasing numbers go backwards in time. 帧以堆栈顶部的“ 0”编号。越来越多的数字会倒退。

For more context, you can use the `backtrace` command. This is identical to `frame` but gives more detailed address information as well as functionparameters. This command can be abbreviated `bt`: 要获得更多上下文，可以使用`backtrace`命令。与`frame`相同，但提供了更详细的地址信息以及功能参数。该命令可以缩写为“ bt”：

```
[zxdb] bt
▶ 0 fxl::CommandLineFromIteratorsFindFirstPositionalArg<const char *const *>() • command_line.h:185
      IP = 0x10f982cf2ad0, BP = 0x66b45a01af50, SP = 0x66b45a01af38
      first = (const char* const*) 0x59f4e1268dc0
      last = (const char* const*) 0x59f4e1268dc8
      first_positional_arg = (const char* const**) 0x0
  1 fxl::CommandLineFromIterators<const char *const *>() • command_line.h:204
      IP = 0x10f982cf2ac0, BP = 0x66b45a01af50, SP = 0x66b45a01af40
      first = <'first' is not available at this address. >
      last = <'last' is not available at this address. >
...
```
 

Each stack frame has a code location. Use the `list` command to look at source code. By itself, it lists the source code around the current stack frame’sinstruction pointer: 每个堆栈帧都有一个代码位置。使用“ list”命令查看源代码。它单独列出当前堆栈框架指令指针周围的源代码：

```
[zxdb] list
   183 inline CommandLine CommandLineFromIteratorsFindFirstPositionalArg(
   184     InputIterator first, InputIterator last,
 ▶ 185     InputIterator* first_positional_arg) {
   186   if (first_positional_arg)
   187     *first_positional_arg = last;
```
 

You can list code around the current instruction pointer of other stack frames, too: 您也可以在其他堆栈帧的当前指令指针周围列出代码：

```
[zxdb] frame 3 list
```
 

Or you can list specific things like functions:  或者，您可以列出诸如函数之类的特定内容：

```
[zxdb] list MyClass::MyFunc
```
 

File/line numbers:  文件/行号：

```
[zxdb] list foo.cc:43
```
 

Or whole files:  或整个文件：

```
[zxdb] list --all myfile.cc:1
```
 

 
### Printing values  打印值 

The `print` command can evaluate simple C/C++ expressions in the context of a stack frame. When a thread is suspended (see “Working with threads” above) justtype: “ print”命令可以在堆栈框架的上下文中评估简单的C / C ++表达式。当线程被挂起时（请参见上面的“使用线程”），请输入：

```
[zxdb] print i
34
```
 

Expressions can use most simple C/C++ syntax:  表达式可以使用最简单的C / C ++语法：

```
[zxdb] print &foo->bar[baz]
(const MyStruct*) 0x59f4e1268f70

```
 

You can also evaluate expressions in the context of other stack frames without switching to them (see “Interaction model” above for more): 您还可以在其他堆栈框架的上下文中求值表达式而无需切换到它们（有关更多信息，请参见上面的“交互模型”）：

```
[zxdb] frame 2 print argv[0]
"/bin/cowsay"
```
 

Often you will want to see all local variables:  通常，您将需要查看所有局部变量：

```
[zxdb] locals
argc = 1
argv = (const char* const*) 0x59999ec02dc0
```
 

You can also set variables to integer and boolean values (as long as those variables are in memory and not registers): 您还可以将变量设置为整数和布尔值（只要这些变量在内存中而不是寄存器中）：

```
[zxdb] print done_flag = true
true
[zddb] print i = 56
56
```
 

Things that don’t currently work are:  当前不起作用的是：

 
  * Math ([5458](https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5458))  *数学（[5458]（https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5458））
  * Function calls ([5457](https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5457))  *函数调用（[5457]（https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5457））
  * Pretty-printing (especially for STL) ([5459](https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5459))  *印刷精美（尤其是STL）（[5459]（https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=5459））
  * Various Rust-isms (please file feature requests!).  *各种Rust-ism（请提供文件功能要求！）。

 
### Controlling execution (stepping, etc.)  控制执行（步进等） 

When a thread is suspended (see “Working with threads” above) you can control its execution: 当线程被挂起时（请参见上面的“使用线程”），您可以控制其执行：

`next` / `n`: Advances to the next line, stepping over function calls.  `next` /`n`：前进到下一行，跳过函数调用。

```
[zxdb] n
```
 

`step` / `s`: Advances to the next line. If a function call happens before the next line, that function will be stepped into and execution will stop at thebeginning of it. You can also supply an argument which is a substring to matchof a specific function call. Function names not containing this substring willbe skipped and only matching ones will be stepped into: `step` /`s`：前进到下一行。如果在下一行之前发生函数调用，则该函数将进入其中，并且在函数开始时将停止执行。您还可以提供参数，该参数是与特定函数调用匹配的子字符串。不包含该子字符串的函数名称将被跳过，只有匹配的函数名称会进入：

```
[zxdb] s
[zxdb] s MyFunction
```
 

`finish` / `fi`: Exits the function and stops right after the call.  `finish` /`fi`：退出函数并在调用后立即停止。

```
[zxdb] finish
```
 

`until` / `u`: Given a location (the same as breakpoints, see above), continues the thread until execution gets there. For example, to run until line 45 of thecurrent file: `until` /`u`：给定位置（与断点相同，见上文），继续执行线程，直到执行到那里为止。例如，要运行到当前文件的第45行：

```
[zxdb] u 45
```
 

`jump`: Move the instruction pointer to a new address.  跳转：将指令指针移至新地址。

```
[zxdb] jump 22  // Line number
[zxdb] jump 0x87534123  // Address
```
 

There different things you can do with context. For example, to run until execution gets back to a given stack frame: 您可以使用上下文执行不同的操作。例如，要运行直到执行返回给定的堆栈帧：

```
[zxdb] frame 2 until
```
 

 
### Assembly language  汇编语言 

There are commands that deal with assembly language:  有一些处理汇编语言的命令：

 
  * `disassemble` / `di`: Disassemble at the current location (or a given location) *`disassemble` /`di`：在当前位置（或给定位置）拆卸

 
  * `nexti` / `ni`: Step to the next instruction, stepping over function calls.  *`nexti` /`ni`：转到下一条指令，跳过函数调用。

 
  * `stepi` / `si`: Step the next instruction, following function calls.  *`stepi` /`si`：在函数调用之后执行下一条指令。

 
  * `regs`: Get the CPU registers.  *`regs`：获取CPU寄存器。

zxdb maintains information about whether the last command was an assembly command or a source-code and will show that information on stepping orbreakpoint hits. To switch to assembly-language mode, type `disassemble`, andto switch back to source-code mode, type `list`. zxdb维护有关最后一个命令是汇编命令还是源代码的信息，并将显示有关步进或断点命中的信息。要切换到汇编语言模式，请键入“ disassemble”，然后切换回源代码模式，请键入“ list”。

 
### Low-level memory  低级内存 

 
  * `mem-read` / `x`: Dumps memory  *`mem-read` /`x`：转储内存

 
