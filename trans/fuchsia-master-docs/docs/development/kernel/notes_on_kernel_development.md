 
# Notes on kernel development  内核开发注意事项 

 
## Low level kernel development  低级内核开发 

For kernel development it's not uncommon to need to monitor or break things before the gfxconsole comes up. 对于内核开发，在gfxconsole出现之前需要监视或破坏事物并不罕见。

To force-enable log output to the legacy serial console on an x64 machine, pass "kernel.serial=legacy".  For other serial configurations, see the kernel.serialdocs in [kernel_cmdline.md](/docs/reference/kernel/kernel_cmdline.md). 要在x64机器上强制将日志输出启用到旧版串行控制台，请传递“ kernel.serial = legacy”。有关其他串行配置，请参见[kernel_cmdline.md]（/ docs / reference / kernel / kernel_cmdline.md）中的kernel.serialdocs。

To enable the early console before the graphical console comes up use the ``gfxconsole.early`` cmdline option. More information can be found in[kernel_cmdline.md](/docs/reference/kernel/kernel_cmdline.md).Enabling ``startup.keep-log-visible``will ensure that the kernel log staysvisible if the gfxconsole comes up after boot. To disable the gfxconsoleentirely you can disable the video driver it is binding to via ``driver.<drivername>.disable``.On a skylake system, all these options together would look something like: 要在图形控制台启动之前启用早期控制台，请使用gfxconsole.early cmdline选项。可以在[kernel_cmdline.md]（/ docs / reference / kernel / kernel_cmdline.md）中找到更多信息。启用“ startup.keep-log-visible”将确保如果gfxconsole在启动后启动，则内核日志保持可见。要永久禁用gfx，您可以通过``driver。<drivername> .disable''禁用要绑定的视频驱动程序。在skylake系统上，所有这些选项看起来像这样：

```
$ tools/build-x86/bootserver build-x86/zircon.bin -- gfxconsole.early driver.intel-i915-display.disable
```
 

To directly output to the console rather than buffering it (useful in the event of kernel freezes) you can enable ``ENABLE_KERNEL_LL_DEBUG`` in your build like so: 要直接输出到控制台而不是对其进行缓冲（在内核冻结的情况下很有用），可以在构建中启用“ ENABLE_KERNEL_LL_DEBUG”，如下所示：

```
fx set ... --args='zircon_extra_args={kernel_extra_defines=["ENABLE_KERNEL_LL_DEBUG"]}'

```
 

There is also a kernel cmdline parameter kernel.bypass-debuglog, which can be set to true to force output to the console instead of buffering it. The reason we haveboth a compile switch and a cmdline parameter is to facilitate prints in the kernelbefore cmdline is parsed to be forced to go to the console. The compile switch settingoverrides the cmdline parameter (if both are present). Note that both the compile switchand the cmdline parameter have the side effect of disabling irq driven uart Tx. 还有一个内核cmdline参数kernel.bypass-debuglog，可以将其设置为true以强制输出到控制台而不是对其进行缓冲。我们同时具有编译开关和cmdline参数的原因是为了便于在将cmdline解析为强制进入控制台之前在内核中进行打印。编译开关设置将覆盖cmdline参数（如果同时存在）。请注意，编译开关和cmdline参数都具有禁用irq驱动的uart Tx的副作用。

 
## Changing the compiler optimization level of a module  更改模块的编译器优化级别 

You can override the default `-On` level for a module by defining in its build arguments: 您可以通过在模块的构建参数中进行定义来覆盖模块的默认“ -On”级别：

```
opt_level := <n>
```
 

 
## Requesting a backtrace  请求回溯 

 
### From within a user process  从用户流程中 

For debugging purposes, the system crashlogger can print backtraces by request. It requires modifying your source, but in the absence of adebugger, or as a general builtin debug mechanism, this can be useful. 出于调试目的，系统崩溃记录器可以根据请求打印回溯。它需要修改您的源代码，但是在没有adebugger的情况下，或者作为常规的内置调试机制，这可能会很有用。

```
#include <lib/backtrace-request/backtrace-request.h>

void my_function() {
  backtrace_request();
}
```
 

When `backtrace\_request` is called, it causes an exception used by debuggers for breakpoint handling.If a debugger is not attached, the system crashlogger willprocess the exception, print a backtrace, and then resume the thread. 当调用`backtrace \ _request`时，它会导致调试器使用异常处理断点。如果未附加调试器，则系统崩溃记录器将处理该异常，打印回溯，然后恢复线程。

 
### From a kernel thread  从内核线程 

```
#include <kernel/thread.h>

void my_function() {
  thread_print_backtrace(get_current_thread(), __GET_FRAME(0));
}
```
 

 
## Exporting debug data during boot  引导期间导出调试数据 

To support testing the system during early boot, there is a mechanism to export data files from the kernel to the /boot filesystem. To export a data file,create a VMO, give it a name, and pass it to userboot with handle\_info of typePA\_VMO\_DEBUG\_FILE (and argument 0). Then userboot will automatically pass itthrough to devmgr, and devmgr will export the VMO as a file at the path 为了支持在早期引导期间测试系统，有一种机制可以将数据文件从内核导出到/ boot文件系统。要导出数据文件，请创建一个VMO，为其命名，然后将其传递给类型为PA \ _VMO \ _DEBUG \ _FILE（和参数0）的handle \ _info的userboot。然后，userboot将自动将其传递给devmgr，devmgr会将VMO作为文件导出到路径中

```
/boot/kernel/<name-of-vmo>
```
 

