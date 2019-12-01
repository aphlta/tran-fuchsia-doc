 
# Zircon Kernel Commandline Options  Zircon内核命令行选项 

The Zircon kernel receives a textual commandline from the bootloader, which can be used to alter some behaviours of the system.  Kernel commandlineparameters are in the form of *option* or *option=value*, separated byspaces, and may not contain spaces. Zircon内核从引导加载程序接收文本命令行，该命令行可用于更改系统的某些行为。内核命令行参数采用* option *或* option = value *的形式，以空格分隔，并且不得包含空格。

For boolean options, *option=0*, *option=false*, or *option=off* will disable the option.  Any other form (*option*, *option=true*, *option=wheee*,etc) will enable it. 对于布尔选项，* option = 0 *，* option = false *或* option = off *将禁用该选项。任何其他形式（* option *，* option = true *，* option = wheee *等）都会启用它。

The kernel commandline is passed from the kernel to the userboot process and the device manager, so some of the options described below apply tothose userspace processes, not the kernel itself. 内核命令行是从内核传递到userboot进程和设备管理器的，因此下面描述的某些选项适用于那些用户空间进程，而不是内核本身。

If keys are repeated, the last value takes precedence, that is, later settings override earlier ones. 如果重复按键，则最后一个值优先，也就是说，以后的设置会覆盖以前的设置。

The devmgr reads the file /boot/config/devmgr (if it exists) at startup and imports name=value lines into its environment, augmenting or overridingthe values from the kernel commandline.  Leading whitespace is ignored andlines starting with # are ignored.  Whitespace is not allowed in names. devmgr在启动时会读取文件/ boot / config / devmgr（如果存在），并将name = value行导入其环境中，以从内核命令行扩展或覆盖值。前导空格将被忽略，以开头的行将被忽略。名称中不允许使用空格。

 
## aslr.disable  禁用 

If this option is set, the system will not use Address Space Layout Randomization. 如果设置此选项，则系统将不使用“地址空间布局随机化”。

 
## aslr.entropy_bits=\<num\>  aslr.entropy_bits = \ <数字\> 

For address spaces that use ASLR this controls the number of bits of entropy in the randomization. Higher entropy results in a sparser address space and usesmore memory for page tables. Valid values range from 0-36, with default being 30. 对于使用ASLR的地址空间，这控制了随机化过程中熵的位数。较高的熵导致稀疏的地址空间，并为页表使用更多的内存。有效值为0-36，默认值为30。

 
## bootsvc.next=\<bootfs path\>  bootsvc.next = \ <bootfs路径\> 

Controls what program is executed by bootsvc to continue the boot process. If this is not specified, the default next program will be used. 控制bootsvc执行什么程序以继续引导过程。如果未指定，将使用默认的下一个程序。

Arguments to the program can optionally be specified using a comma separator between the program and individual arguments. For example,'bootsvc.next=bin/mybin,arg1,arg2'. 可以选择使用程序和各个参数之间的逗号分隔符来指定程序的参数。例如，“ bootsvc.next = bin / mybin，arg1，arg2”。

 
## clock\.backstop=\<seconds\>  时钟\ .backstop = \ <秒数> 

Sets the initial offset (from the Unix epoch, in seconds) for the UTC clock. The clock will be set by the device coordinator at boot time, and then later,if an RTC is present, the RTC clock will be sanitized to at least this time. 设置UTC时钟的初始偏移量（从Unix纪元开始，以秒为单位）。时钟将在启动时由设备协调器设置，然后，如果存在RTC，则至少在该时间之前将RTC时钟清除。

 
## cpu\.hwp=\<bool\>  cpu \ .hwp = \ <布尔值> 

This settings enables HWP (hardware P-states) on supported chips. This feature lets Intel CPUs automatically scale their own clock speed. Defaults to false. 此设置在支持的芯片上启用HWP（硬件P状态）。此功能使Intel CPU可以自动扩展自己的时钟速度。默认为false。

 
## devmgr\.require-system=\<bool\>  devmgr \ .require-system = \ <布尔\> 

Instructs the devmgr that a /system volume is required. Without this, devmgr assumes this is a standalone Zircon build and not a full Fuchsia system. 指示devmgr需要/ system卷。没有这个，devmgr会假定这是一个独立的Zircon版本，而不是完整的紫红色系统。

 
## devmgr\.suspend-timeout-fallback  devmgr \ .suspend-timeout-fallback 

If this option is set, the system invokes kernel fallback to reboot or poweroff the device when the operation did not finish in 10 seconds. 如果设置此选项，则当操作在10秒钟内未完成时，系统将调用内核回退以重新引导或关闭设备电源。

 
## devmgr\.devhost\.asan  devmgr \ .devhost \ .asan 

This option must be set if any drivers not included directly in /boot are built with `-fsanitize=address`.  If there are `-fsanitize=address` drivers in /boot,then all `-fsanitize=address` drivers will be supported regardless of thisoption.  If this option is not set and there are no such drivers in /boot, thendrivers built with `-fsanitize=address` cannot be loaded and will be rejected. 如果使用`-fsanitize = address`构建没有直接包含在/ boot中的驱动程序，则必须设置该选项。如果/ boot中有`-fsanitize = address`驱动程序，则无论此选项如何，都将支持所有`-fsanitize = address`驱动程序。如果未设置此选项，并且/ boot中没有此类驱动程序，则无法加载使用-fsanitize = address`构建的驱动程序，并且该驱动程序将被拒绝。

 
## devmgr\.devhost\.strict-linking  devmgr \ .devhost \ .strict链接 

If this option is set, devmgr will only allow `libasync-default.so`, `libdriver.so`, and `libfdio.so` to be dynamically linked into a devhost. Thisprevents drivers from dynamically linking with libraries that they should not.All other libraries should be statically linked into a driver. 如果设置了该选项，devmgr将仅允许将“ libasync-default.so”，“ libdriver.so”和“ libfdio.so”动态链接到devhost中。这样可以防止驱动程序动态链接不应使用的库。所有其他库都应静态链接到驱动程序中。

 
## devmgr\.verbose  devmgr \ .verbose 

Turn on verbose logging.  打开详细日志记录。

 
## driver.\<name>.compatibility-tests-enable  驱动程序。\ <名称> .compatibility-tests-enable 

If this option is set, devmgr will run compatibility tests for the driver. zircon\_driver\_info, and can be found as the first argument to theZIRCON\_DRIVER\_BEGIN macro. 如果设置此选项，devmgr将运行驱动程序的兼容性测试。 zircon \ _driver \ _info，可以作为ZIRCON \ _DRIVER \ _BEGIN宏的第一个参数找到。

 
## driver.\<name>.compatibility-tests-wait-time  驱动程序。\ <名称> .compatibility-tests-wait-time 

This timeout lets you configure the wait time in milliseconds for each of bind/unbind/suspend hooks to complete in compatibility tests.zircon\_driver\_info, and can be found as the first argument to theZIRCON\_DRIVER\_BEGIN macro. 通过此超时，您可以为每个绑定/取消绑定/挂起挂钩配置等待时间（以毫秒为单位），以完成兼容性测试。zircon \ _driver \ _info，并且可以作为ZIRCON \ _DRIVER \ _BEGIN宏的第一个参数找到。

 
## driver.\<name>.disable  驱动程序。\ <名称>。禁用 

Disables the driver with the given name. The driver name comes from the zircon\_driver\_info, and can be found as the first argument to theZIRCON\_DRIVER\_BEGIN macro. 禁用具有给定名称的驱动程序。驱动程序名称来自zircon \ _driver \ _info，可以作为ZIRCON \ _DRIVER \ _BEGIN宏的第一个参数找到。

Example: `driver.usb_audio.disable`  示例：`driver.usb_audio.disable`

 
## driver.\<name>.log=\<flags>  驱动程序。\ <名称> .log = \ <标志> 

Set the log flags for a driver.  Flags are one or more comma-separated values which must be preceded by a "+" (in which case that flag is enabled)or a "-" (in which case that flag is disabled).  The textual constants"error", "warn", "info", "trace", "spew", "debug1", "debug2", "debug3", and "debug4"may be used, and they map to the corresponding bits in DDK_LOG_... in `ddk/debug.h`The default log flags for a driver is "error", "warn", and "info". 设置驱动程序的日志标志。标志是一个或多个逗号分隔的值，必须在其前面加上“ +”（在这种情况下启用标志）或“-”（在这种情况下禁用标志）。可以使用文本常量“错误”，“警告”，“信息”，“跟踪”，“ spew”，“ debug1”，“ debug2”，“ debug3”和“ debug4”，它们映射到相应的位在DDK_LOG _...中，在ddk / debug.h中，驱动程序的默认日志标志是“错误”，“警告”和“信息”。

Individual drivers may define their own log flags beyond the eight mentioned above. 各个驱动程序可以定义上述八个之外的自己的日志标志。

Example: `driver.usb_audio.log=-error,+info,+0x1000`  范例：`driver.usb_audio.log = -error，+ info，+ 0x1000`

Note again that the name of the driver is the "Driver" argument to the ZIRCON\_DRIVER\_BEGIN macro. It is not, for example, the name of the device,which for some drivers is almost identical, except that the device may benamed "foo-bar" whereas the driver name must use underscores, e.g., "foo_bar". 再次注意，驱动程序的名称是ZIRCON \ _DRIVER \ _BEGIN宏的“ Driver”参数。例如，它不是设备的名称，对于某些驱动程序，它几乎是相同的，只是设备的名称可能是“ foo-bar”，而驱动程序的名称必须使用下划线，例如“ foo_bar”。

 
## driver.\<name>.tests.enable=\<bool>  驱动程序。\ <名称> .tests.enable = \ <布尔> 

Enable the unit tests for an individual driver. The unit tests will run before the driver binds any devices. If `driver.tests.enable` is true then thisdefaults to enabled, otherwise the default is disabled. 为单个驱动程序启用单元测试。该单元测试将在驱动程序绑定任何设备之前运行。如果`driver.tests.enable`为true，则默认为启用，否则默认为禁用。

Note again that the name of the driver is the "Driver" argument to the ZIRCON\_DRIVER\_BEGIN macro. It is not, for example, the name of the device,which for some drivers is almost identical, except that the device may benamed "foo-bar" whereas the driver name must use underscores, e.g., "foo_bar". 再次注意，驱动程序的名称是ZIRCON \ _DRIVER \ _BEGIN宏的“ Driver”参数。例如，它不是设备的名称，对于某些驱动程序，它几乎是相同的，只是设备的名称可能是“ foo-bar”，而驱动程序的名称必须使用下划线，例如“ foo_bar”。

 
## driver.sysmem.protected_memory_size=\<num>  driver.sysmem.protected_memory_size = \ <数字> 

Overrides the board-driver-specified size for sysmem's default protected memory pool. Value is in bytes. 覆盖sysmem的默认受保护内存池的板驱动程序指定的大小。值以字节为单位。

 
## driver.sysmem.protected_memory_size=\<num>  driver.sysmem.protected_memory_size = \ <数字> 

Overrides the board-driver-specified size for sysmem's contiguous memory pool. Value is in bytes. 覆盖sysmem连续内存池的主板驱动程序指定的大小。值以字节为单位。

 
## driver.tests.enable=\<bool>  driver.tests.enable = \ <布尔> 

Enable the unit tests for all drivers. The unit tests will run before the drivers bind any devices. It's also possible to enable tests for an individualdriver, see `driver.\<name>.enable_tests`. The default is disabled. 对所有驱动程序启用单元测试。单元测试将在驱动程序绑定任何设备之前运行。也可以为单个驱动程序启用测试，请参见`driver。\ <name> .enable_tests`。默认设置为禁用。

 
## driver.tracing.enable=\<bool>  driver.tracing.enable = \ <布尔> 

Enable or disable support for tracing drivers. When enabled drivers may participate in [Fuchsia tracing](/docs/concepts/drivers/tracing.md). 启用或禁用对跟踪驱动程序的支持。启用后，驱动程序可能会参与[Fuchsia跟踪]（/ docs / concepts / drivers / tracing.md）。

Implementation-wise, what this option does is tell each devhost whether to register as "trace provider". 在实现方面，此选项的作用是告诉每个devhost是否注册为“跟踪提供程序”。

The default is enabled. This options exists to provide a quick fallback should a problem arise. 默认启用。存在此选项是为了在出现问题时提供快速回退。

 
## gfxconsole.early=\<bool>  gfxconsole.early = \ <布尔> 

This option (disabled by default) requests that the kernel start a graphics console during early boot (if possible), to display kernel debug printmessages while the system is starting.  When userspace starts up, a usermodegraphics console driver takes over. 此选项（默认情况下禁用）请求内核在早期引导期间启动图形控制台（如果可能），以在系统启动时显示内核调试打印消息。用户空间启动时，将由用户模式图形控制台驱动程序接管。

The early kernel console can be slow on some platforms, so if it is not needed for debugging it may speed up boot to disable it. 早期的内核控制台在某些平台上可能会很慢，因此，如果不需要调试，可能会加快引导速度以禁用它。

 
## gfxconsole.font=\<name>  gfxconsole.font = \ <名称> 

This option asks the graphics console to use a specific font.  Currently only "9x16" (the default) and "18x32" (a double-size font) are supported. 此选项要求图形控制台使用特定字体。当前仅支持“ 9x16”（默认）和“ 18x32”（双倍字体）。

 
## iommu.enable=\<bool>  iommu.enable = \ <布尔> 

This option (disabled by default) allows the system to use a hardware IOMMU if present. 此选项（默认情况下禁用）允许系统使用硬件IOMMU（如果存在）。

 
## kernel.bypass-debuglog=\<bool>  kernel.bypass-debug日志= \ <book> 

When enabled, forces output to the console instead of buffering it. The reason we have both a compile switch and a cmdline parameter is to facilitate printsin the kernel before cmdline is parsed to be forced to go to the console.The compile switch setting overrides the cmdline parameter (if both are present).Note that both the compile switch and the cmdline parameter have the side effectof disabling irq driven uart Tx. 启用后，强制输出到控制台而不是缓冲它。我们同时具有compile开关和cmdline参数的原因是为了便于在将cmdline解析为强制进入控制台之前在内核中进行打印.compile开关设置会覆盖cmdline参数（如果两者都存在）。编译开关和cmdline参数具有禁用irq驱动的uart Tx的副作用。

 
## kernel.cprng-reseed-require.hw-rng=\<bool>  kernel.cprng-reseed-require.hw-rng = \ <布尔> 

When enabled and if HW RNG fails at reseeding, CPRNG panics. Defaults to false.  启用后，如果硬件RNG重新播种失败，则CPRNG会慌张。默认为false。

 
## kernel.cprng-reseed-require.jitterentropy=\<bool>  kernel.cprng-reseed-require.jitterentropy = \ <布尔> 

When enabled and if jitterentropy fails at reseeding, CPRNG panics. Defaults to false. 启用后，如果在重新播种时抖动熵失败，则CPRNG会恐慌。默认为false。

 
## kernel.cprng-seed-require.hw-rng=\<bool>  kernel.cprng-seed-require.hw-rng = \ <布尔> 

When enabled and if HW RNG fails at initial seeding, CPRNG panics. Defaults to false. 启用后，如果HW RNG在初始播种时失败，则CPRNG会慌张。默认为false。

 
## kernel.cprng-seed-require.jitterentropy=\<bool>  kernel.cprng-seed-require.jitterentropy = \ <布尔> 

When enabled and if jitterentrop fails initial seeding, CPRNG panics. Defaults to false. 启用后，如果jitterentrop无法初始播种，则CPRNG会出现恐慌。默认为false。

 
## kernel.cprng-seed-require.cmdline=\<bool>  kernel.cprng-seed-require.cmdline = \ <布尔> 

When enabled and if you do not provide entropy input from the kernel command line, CPRNG panics. Defaults to false. 启用后，如果不从内核命令行提供熵输入，则CPRNG会发生混乱。默认为false。

 
## kernel.enable-debugging-syscalls=\<bool>  kernel.enable-debugging-syscalls = \ <布尔> 

When disabled, certain debugging-related syscalls will fail with `ZX_ERR_NOT_SUPPORTED`. Defaults to false (debugging syscalls disabled). 禁用后，某些与调试相关的系统调用将失败，并带有ZX_ERR_NOT_SUPPORTED。默认为false（禁用调试系统调用）。

 
## kernel.entropy-mixin=\<hex>  kernel.entropy-mixin = \ <十六进制> 

Provides entropy to be mixed into the kernel's CPRNG.  提供熵以混合到内核的CPRNG中。

 
## kernel.entropy-test.len=\<len>  kernel.entropy-test.len = \ <len> 

When running an entropy collector quality test, collect the provided number of bytes. Defaults to the maximum value `ENTROPY_COLLECTOR_TEST_MAXLEN`. 在运行熵收集器质量测试时，收集提供的字节数。默认为最大值“ ENTROPY_COLLECTOR_TEST_MAXLEN”。

The default value for the compile-time constant `ENTROPY_COLLECTOR_TEST_MAXLEN` is 1MiB. 编译时常量“ ENTROPY_COLLECTOR_TEST_MAXLEN”的默认值为1MiB。

 
## kernel.entropy-test.src=\<source>  kernel.entropy-test.src = \ <源> 

When running an entropy collector quality test, use the provided entropy source. Currently recognized sources: `hw_rng`, `jitterentropy`. This option is ignoredunless the kernel was built with `ENABLE_ENTROPY_COLLECTOR_TEST=1`. 在运行熵收集器质量测试时，请使用提供的熵源。目前公认的来源：“ hw_rng”，“抖动熵”。除非内核使用“ ENABLE_ENTROPY_COLLECTOR_TEST = 1”构建内核，否则将忽略此选项。

 
## kernel.halt-on-panic=\<bool>  kernel.halt-on-panic = \ <布尔> 

If this option is set (disabled by default), the system will halt on a kernel panic instead of rebooting. To enable halt-on-panic,pass the kernel commandline argument `kernel.halt-on-panic=false`. 如果设置了此选项（默认情况下处于禁用状态），则系统将在内核崩溃时停止而不是重新启动。要启用紧急停止功能，请传递内核命令行参数`kernel.halt-on-panic = false`。

Since the kernel can't reliably draw to a framebuffer when the GPU is enabled, the system will reboot by default if the kernel crashes or panics. 由于启用GPU时内核无法可靠地吸引帧缓冲区，因此默认情况下，如果内核崩溃或出现紧急情况，系统将重新启动。

If the kernel crashes and the system reboots, the log from the kernel panic will appear at `/boot/log/last-panic.txt`, suitable for viewing, downloading, etc. 如果内核崩溃并且系统重新启动，来自内核恐慌的日志将显示在`/ boot / log / last-panic.txt`中，适合查看，下载等。

> Please attach your `last-panic.txt` and `zircon.elf` files to any kernel > panic bugs you file. >请将您的`last-panic.txt`和`zircon.elf`文件附加到您提交的任何内核>紧急错误中。

If there's a `last-panic.txt`, that indicates that this is the first successful boot since a kernel panic occurred. 如果有一个“ last-panic.txt”，则表明这是自发生内核恐慌以来的首次成功引导。

It is not "sticky" -- if you reboot cleanly, it will be gone, and if you crash again it will be replaced. 它不是“粘性”的-如果您干净地重新启动，它将消失，并且如果再次崩溃，它将被替换。

 
## kernel.jitterentropy.bs=\<num>  kernel.jitterentropy.bs = \ <数字> 

Sets the "memory block size" parameter for jitterentropy (the default is 64). When jitterentropy is performing memory operations (to increase variation in CPUtiming), the memory will be accessed in blocks of this size. 设置抖动熵的“内存块大小”参数（默认值为64）。当抖动熵正在执行内存操作（以增加CPUtiming的变化）时，将以该大小的块访问内存。

 
## kernel.jitterentropy.bc=\<num>  kernel.jitterentropy.bc = \ <数字> 

Sets the "memory block count" parameter for jitterentropy (the default is 512). When jitterentropy is performing memory operations (to increase variation in CPUtiming), this controls how many blocks (of size `kernel.jitterentropy.bs`) areaccessed. 设置抖动熵的“内存块计数”参数（默认值为512）。当抖动熵正在执行内存操作（以增加CPUtiming的变化）时，这将控制访问多少个块（大小为kernel.jitterentropy.bs）。

 
## kernel.jitterentropy.ml=\<num>  kernel.jitterentropy.ml = \ <数字> 

Sets the "memory loops" parameter for jitterentropy (the default is 32). When jitterentropy is performing memory operations (to increase variation in CPUtiming), this controls how many times the memory access routine is repeated.This parameter is only used when `kernel.jitterentropy.raw` is true. If thevalue of this parameter is `0` or if `kernel.jitterentropy.raw` is `false`,then jitterentropy chooses the number of loops is a random-ish way. 为抖动设置“内存循环”参数（默认为32）。当抖动熵正在执行内存操作（以增加CPUtiming的变化）时，它控制重复执行内存访问例程的次数。仅当`kernel.jitterentropy.raw'为true时，才使用此参数。如果此参数的值为0或kernel.jitterentropy.raw的值为false，则jitterentropy选择循环数的方式是随机的。

 
## kernel.jitterentropy.ll=\<num>  kernel.jitterentropy.ll = \ <数字> 

Sets the "LFSR loops" parameter for jitterentropy (the default is 1). When jitterentropy is performing CPU-intensive LFSR operations (to increase variationin CPU timing), this controls how many times the LFSR routine is repeated.  Thisparameter is only used when `kernel.jitterentropy.raw` is true. If the value ofthis parameter is `0` or if `kernel.jitterentropy.raw` is `false`, thenjitterentropy chooses the number of loops is a random-ish way. 为抖动熵设置“ LFSR循环”参数（默认为1）。当抖动熵正在执行CPU密集型LFSR操作（以增加CPU时序的差异）时，这将控制LFSR例程重复多少次。仅当`kernel.jitterentropy.raw`为true时才使用该参数。如果此参数的值为0或kernel.jitterentropy.raw为false，则jitterentropy选择循环数是一种随机的方式。

 
## kernel.jitterentropy.raw=\<bool>  kernel.jitterentropy.raw = \ <布尔> 

When true (the default), the jitterentropy entropy collector will return raw, unprocessed samples. When false, the raw samples will be processed byjitterentropy, producing output data that looks closer to uniformly random. Notethat even when set to false, the CPRNG will re-process the samples, so theprocessing inside of jitterentropy is somewhat redundant. 如果为true（默认值），则抖动熵熵收集器将返回未处理的原始样本。如果为假，则将通过抖动熵处理原始样本，从而生成看起来更接近均匀随机的输出数据。请注意，即使设置为false，CPRNG也会重新处理样本，因此抖动熵内部的处理有些多余。

 
## kernel.memory-limit-dbg=\<bool>  kernel.memory-limit-dbg = \ <布尔> 

This option enables verbose logging from the memory limit library.  该选项启用了内存限制库中的详细日志记录。

 
## kernel.memory-limit-mb=\<num>  kernel.memory-limit-mb = \ <数字> 

This option tells the kernel to limit system memory to the MB value specified by 'num'. Using this effectively allows a user to simulate the system havingless physical memory than physically present. 该选项告诉内核将系统内存限制为“ num”指定的MB值。有效地使用它允许用户模拟物理内存少于物理内存的系统。

 
## kernel.mexec-force-high-ramdisk=\<bool>  kernel.mexec-force-high-ramdisk = \ <布尔> 

This option is intended for test use only. When set to `true` it forces the mexec syscall to place the ramdisk for the following kernel in high memory(64-bit address space, >= 4GiB offset). The default value is `false`. 此选项仅用于测试。当设置为“ true”时，它将强制mexec syscall将后面内核的虚拟磁盘放置在高内存（64位地址空间，> = 4GiB偏移量）中。默认值为“ false”。

 
## kernel.oom.behavior=\<string>  kernel.oom.behavior = \ <字符串> 

This option can be used to configure the behavior of the kernel when encountering an OOM situation. Valid values are `jobkill`, and `reboot`. Ifunset or set to an invalid value, defaults to `reboot`. 遇到OOM情况时，此选项可用于配置内核的行为。有效值为“ jobkill”和“ reboot”。如果未设置或设置为无效值，则默认为`reboot`。

If set to `jobkill`, when encountering OOM, the kernel attempts to kill jobs that have the `ZX_PROP_JOB_KILL_ON_OOM` bit set to recover memory. 如果设置为“ jobkill”，则在遇到OOM时，内核会尝试杀死设置为“ ZX_PROP_JOB_KILL_ON_OOM”的作业以恢复内存。

If set to `reboot`, when encountering OOM, the kernel signals an event (see `zx_system_get_event()`), delays briefly, and then reboots the system. 如果设置为“ reboot”，则在遇到OOM时，内核会发出一个事件信号（请参阅“ zx_system_get_event（）”），短暂延迟，然后重新引导系统。

 
## kernel.oom.enable=\<bool>  kernel.oom.enable = \ <布尔> 

This option (true by default) turns on the out-of-memory (OOM) kernel thread, which kills processes when the PMM has less than `kernel.oom.redline_mb` freememory, sleeping for `kernel.oom.sleep_sec` between checks. 此选项（默认为true）打开内存不足（OOM）内核线程，当PMM的可用内存少于“ kernel.oom.redline_mb”空闲内存时，它将杀死进程，并在两次检查之间为“ kernel.oom.sleep_sec”休眠。

The OOM thread can be manually started/stopped at runtime with the `k oom start` and `k oom stop` commands, and `k oom info` will show the current state. OOM线程可以在运行时使用“ k oom start”和“ k oom stop”命令手动启动/停止，并且“ k oom info”将显示当前状态。

See `k oom` for a list of all OOM kernel commands.  有关所有OOM内核命令的列表，请参见`k oom`。

 
## kernel.oom.redline-mb=\<num>  kernel.oom.redline-mb = \ <数字> 

This option (50 MB by default) specifies the free-memory threshold at which the out-of-memory (OOM) thread will trigger a low-memory event and begin killingprocesses. 此选项（默认为50 MB）指定空闲内存阈值，在该阈值内存不足（OOM）线程将触发内存不足事件并开始终止进程​​。

The `k oom info` command will show the current value of this and other parameters. koom info命令将显示此参数和其他参数的当前值。

 
## kernel.oom.sleep-sec=\<num>  kernel.oom.sleep-sec = \ <编号> 

This option (1 second by default) specifies how long the out-of-memory (OOM) kernel thread should sleep between checks. 此选项（默认情况下为1秒）指定两次检查之间内存不足（OOM）内核线程应休眠的时间。

The `k oom info` command will show the current value of this and other parameters. koom info命令将显示此参数和其他参数的当前值。

 
## kernel.x86.disable_spec_mitigations=\<bool>  kernel.x86.disable_spec_mitigations = \ <布尔> 

If set, disable all speculative execution information leak mitigations.  如果设置，请禁用所有推测性执行信息泄漏缓解措施。

If clear, the per-mitigation defaults will be used.  如果清除，将使用每个缓解的默认设置。

This option only affects x86 systems.  此选项仅影响x86系统。

 
## kernel.x86.pti.enable=\<int>  kernel.x86.pti.enable = \ <整数> 

Page table isolation configures user page tables to not have kernel text or data mapped. This may impact performance negatively. This is a mitigationfor Meltdown (AKA CVE-2017-5754). 页表隔离将用户页表配置为不映射内核文本或数据。这可能会对性能产生负面影响。这是Meltdown的缓解措施（AKA CVE-2017-5754）。

 
* If set to 1, this force-enables page table isolation.  *如果设置为1，则强制启用页表隔离。
* If set to 0, this force-disables page table isolation. This may be insecure.  *如果设置为0，这将强制禁用页表隔离。这可能是不安全的。
* If set to 2 or unset (the default), this enables page table isolation on CPUs vulnerable to Meltdown. *如果设置为2或未设置（默认值），则可以在容易崩溃的CPU上启用页表隔离。

This option only affects x86 systems.  此选项仅影响x86系统。

 
## kernel.x86.spec_store_bypass_disable=\<bool>  kernel.x86.spec_store_bypass_disable = \ <布尔> 

Spec-store-bypass (Spectre V4) is a speculative execution information leak vulnerability that affects many Intel and AMD x86 CPUs. It targets memorydisambiguation hardware to infer the contents of recent stores. The attackonly affects same-privilege-level, intra-process data. Spec-by-bypass（Spectre V4）是一个推测性执行信息泄漏漏洞，它会影响许多Intel和AMD x86 CPU。它针对内存消除歧义硬件，以推断最近存储的内容。该攻击仅影响相同特权级别的进程内数据。

This command line option controls whether a mitigation is enabled. The mitigation has negative performance impacts. 此命令行选项控制是否启用缓解措施。缓解措施会对性能产生负面影响。

 
* If true, the mitigation is enabled on CPUs that need it.  *如果为true，则在需要缓解的CPU上启用该缓解。
* If false (the default), the mitigation is not enabled.  *如果为false（默认值），则不会启用缓解措施。

 
## kernel.x86.md_clear_on_user_return=\<bool>  kernel.x86.md_clear_on_user_return = \ <布尔> 

MDS (Microarchitectural Data Sampling) is a family of speculative execution information leak bugs that allow the contents of recent loads or stores to beinferred by hostile code, regardless of privilege level (CVE-2019-11091,CVE-2018-12126, CVE-2018-12130, CVE-2018-12127). For example, this could allowuser code to read recent kernel loads/stores. MDS（微体系结构数据采样）是推测性执行信息泄漏错误家族，无论特权级别（CVE-2019-11091，CVE-2018-12126，CVE-2018），都允许通过敌对代码推断最近加载或存储的内容-12130，CVE-2018-12127）。例如，这可能允许用户代码读取最近的内核加载/存储。

To avoid this bug, it is required that all microarchitectural structures that could leak data be flushed on trust level transitions. Also, it isimportant that trust levels do not concurrently execute on a single physicalprocessor core. 为避免此错误，要求在信任级别转换时清除所有可能泄漏数据的微体系结构。同样，重要的是信任级别不能在单个物理处理器内核上同时执行。

This option controls whether microarchitectual structures are flushed on the kernel to user exit path, if possible. It may have a negative performanceimpact. 如果可能，此选项控制是否在内核上将微体系结构结构刷新到用户出口路径。它可能会对性能产生负面影响。

 
* If set to true, structures are flushed if the processor is vulnerable.  *如果设置为true，则在处理器容易受到攻击时刷新结构。
* If set to false (the default), no flush is executed on structures.  *如果设置为false（默认值），则不对结构执行刷新。

This option only affects x86 systems.  此选项仅影响x86系统。

 
## kernel.mexec-pci-shutdown=\<bool>  kernel.mexec-pci-shutdown = \ <布尔> 

If false, this option leaves PCI devices running when calling mexec. Defaults to true. 如果为false，则此选项使PCI设备在调用mexec时运行。默认为true。

 
## kernel.serial=\<string\>  kernel.serial = \ <字串\> 

This controls what serial port is used.  If provided, it overrides the serial port described by the system's bootdata.  The kernel debug serial port isa reserved resource and may not be used outside of the kernel. 这控制使用哪个串行端口。如果提供，它将覆盖系统引导数据描述的串行端口。内核调试串行端口是保留的资源，不得在内核外部使用。

If set to "none", the kernel debug serial port will be disabled and will not be reserved, allowing the default serial port to be used outside the kernel. 如果设置为“ none”，则内核调试串行端口将被禁用并且不会被保留，从而允许在内核外部使用默认串行端口。

 
### x64 specific values  x64特定值 

On x64, some additional values are supported for configuring 8250-like UARTs:  在x64上，支持一些其他值来配置类似8250的UART：

 
- If set to "legacy", the legacy COM1 interface is used.  -如果设置为“旧版”，则使用旧版COM1接口。
- A port-io UART can be specified using "ioport,\<portno>,\<irq>".  -可以使用“ ioport，\ <端口号>，\ <irq>”指定端口io UART。
- An MMIO UART can be specified using "mmio,\<physaddr>,\<irq>".  -可以使用“ mmio，\ <physaddr>，\ <irq>”指定MMIO UART。

For example, "ioport,0x3f8,4" would describe the legacy COM1 interface.  例如，“ ioport，0x3f8,4”将描述旧式COM1接口。

All numbers may be in any base accepted by *strtoul*().  所有数字都可以使用* strtoul *（）接受的任何基数。

All other values are currently undefined.  所有其他值当前未定义。

 
## kernel.shell=\<bool>  kernel.shell = \ <布尔> 

This option tells the kernel to start its own shell on the kernel console instead of a userspace sh. 这个选项告诉内核在内核控制台而不是用户空间sh上启动它自己的shell。

 
## kernel.smp.maxcpus=\<num>  kernel.smp.maxcpus = \ <数字> 

This option caps the number of CPUs to initialize.  It cannot be greater than *SMP\_MAX\_CPUS* for a specific architecture. 此选项限制了要初始化的CPU的数量。对于特定体系结构，它不能大于* SMP \ _MAX \ _CPUS *。

 
## kernel.smp.ht=\<bool>  kernel.smp.ht = \ <布尔> 

This option can be used to disable the initialization of hyperthread logical CPUs.  Defaults to true. 此选项可用于禁用超线程逻辑CPU的初始化。默认为true。

 
## kernel.wallclock=\<name>  kernel.wallclock = \ <名称> 

This option can be used to force the selection of a particular wall clock.  It only is used on pc builds.  Options are "tsc", "hpet", and "pit". 此选项可用于强制选择特定的挂钟。它仅用于PC版本。选项为“ tsc”，“ hpet”和“ pit”。

 
## ktrace.bufsize  ktrace.bufsize 

This option specifies the size of the buffer for ktrace records, in megabytes. The default is 32MB. 此选项指定ktrace记录的缓冲区大小（以兆字节为单位）。默认值为32MB。

 
## ktrace.grpmask  ktrace.grpmask 

This option specifies what ktrace records are emitted. The value is a bitmask of KTRACE\_GRP\_\* values from zircon/ktrace.h.Hex values may be specified as 0xNNN. 此选项指定发出哪些ktrace记录。该值是zircon / ktrace.h中的KTRACE \ _GRP \ _ \ *值的位掩码。十六进制值可以指定为0xNNN。

 
## ldso.trace  ldso.trace 

This option (disabled by default) turns on dynamic linker trace output. The output is in a form that is consumable by clients like IntelProcessor Trace support. 此选项（默认情况下禁用）打开动态链接器跟踪输出。输出的格式可以由诸如IntelProcessor Trace支持之类的客户端使用。

 
## zircon.autorun.boot=\<command>  zircon.autorun.boot = \ <命令> 

This option requests that *command* be run at boot, after devmgr starts up.  此选项要求devmgr启动后在引导时运行* command *。

Any `+` characters in *command* are treated as argument separators, allowing you to pass arguments to an executable. * command *中的所有`+`字符都被当作参数分隔符，使您可以将参数传递给可执行文件。

 
## zircon.autorun.system=\<command>  zircon.autorun.system = \ <命令> 

This option requests that *command* be run once the system partition is mounted and *init* is launched.  If there is no system bootfs or system partition, itwill never be launched. 一旦安装了系统分区并启动了* init *，此选项就要求运行* command *。如果没有系统bootfs或系统分区，则将永远不会启动它。

Any `+` characters in *command* are treated as argument separators, allowing you to pass arguments to an executable. * command *中的所有`+`字符都被当作参数分隔符，使您可以将参数传递给可执行文件。

 
## zircon.system.disable-automount=\<bool>  zircon.system.disable-automount = \ <布尔> 

This option prevents the fshost from auto-mounting any disk filesystems (/system, /data, etc), which can be useful for certain low level test setups.It is false by default.  It is implied by **netsvc.netboot=true** 此选项可防止fshost自动挂载任何磁盘文件系统（/ system，/ data等），这对于某些低级测试设置很有用。默认情况下为false。 ** netsvc.netboot = true **暗示

 
## zircon.system.pkgfs.cmd=\<command>  zircon.system.pkgfs.cmd = \ <命令> 

This option requests that *command* be run once the blob partition is mounted. Any `+` characters in *command* are treated as argument separators, allowingyou to pass arguments to an executable. 此选项要求在安装Blob分区后运行* command *。 * command *中的所有`+`字符都被当作参数分隔符，使您可以将参数传递给可执行文件。

The executable and its dependencies (dynamic linker and shared libraries) are found in the blob filesystem.  The executable *path* is *command* before thefirst `+`.  The dynamic linker (`PT_INTERP`) and shared library (`DT_NEEDED`)name strings sent to the loader service are prefixed with `lib/` to produce a*path*.  Each such *path* is resolved to a blob ID (i.e. merkleroot in ASCIIhex) using the `zircon.system.pkgfs.file.`*path* command line argument.  Inthis way, `/boot/config/devmgr` contains a fixed manifest of files used tostart the process. 可执行文件及其依赖项（动态链接器和共享库）位于blob文件系统中。可执行文件* path *是第一个+之前的* command *。发送到加载程序服务的动态链接器（`PT_INTERP`）和共享库（`DT_NEEDED`）名称字符串以`lib /`为前缀，以生成a * path *。使用* path *命令行参数将每个此类* path *解析为一个Blob ID（即ASCIIhex中的merkleroot）。这样，`/ boot / config / devmgr`包含用于启动进程的文件的固定清单。

The new process receives a `PA_USER0` channel handle at startup that will be used as the client filesystem handle mounted at `/pkgfs`.  The command isexpected to start serving on this channel and then signal its process handlewith `ZX_USER_SIGNAL_0`.  Then `/pkgfs/system` will be mounted as `/system`. 新进程在启动时会收到一个“ PA_USER0”通道句柄，它将用作挂载在“ / pkgfs”上的客户端文件系统句柄。预计该命令将开始在此通道上提供服务，然后通过`ZX_USER_SIGNAL_0`发出信号通知其进程句柄。然后`/ pkgfs / system`将被挂载为`/ system`。

 
## zircon.system.pkgfs.file.*path*=\<blobid>  zircon.system.pkgfs.file。* path * = \ <blobid> 

Used with [`zircon.system.pkgfs.cmd`](#zircon.system.pkgfs.cmd), above.  与上面的[zircon.system.pkgfs.cmd]（zircon.system.pkgfs.cmd）一起使用。

 
## zircon.system.volume=\<arg>  zircon.system.volume = \ <arg> 

This option specifies where to find the "/system" volume.  此选项指定在何处查找“ / system”卷。

It may be set to: "any", in which case the first volume of the appropriate type will be used."local" in which the first volume that's non-removable of the appropriate typewill be used."none" (default) which avoids mounting anything. 它可以设置为：“ any”，在这种情况下将使用适当类型的第一个卷。“ local”在其中将使用不可移动的适当类型的第一个卷。“ none”（默认）避免安装任何东西。

A "/system" ramdisk provided by bootdata always supersedes this option.  bootdata提供的“ / system” ramdisk始终会取代该选项。

 
## zircon.system.filesystem-check=\<bool>  zircon.system.filesystem-check = \ <布尔> 

This option requests that filesystems automatically mounted by the system are pre-verified using a filesystem consistency checker before being mounted. 该选项要求在挂载之前使用文件系统一致性检查器对由系统自动挂载的文件系统进行预验证。

By default, this option is set to false.  默认情况下，此选项设置为false。

 
## zircon.system.wait-for-data=\<bool>  zircon.system.wait-for-data = \ <布尔> 

This option initializes `pkgfs` and `appmgr` only after a persistent data partition appears. 仅在出现持久数据分区后，此选项才会初始化pkgfs和appmgr。

By default, this option is set to true.  默认情况下，此选项设置为true。

 
## netsvc.netboot=\<bool>  netsvc.netboot = \ <布尔> 

If true, zircon will attempt to netboot into another instance of zircon upon booting. 如果为true，则Zircon将在引导时尝试通过Netboot进入另一个Zircon实例。

More specifically, zircon will fetch a new zircon system from a bootserver on the local link and attempt to kexec into the new image, thereby replacing thecurrently running instance of zircon. 更具体地说，Zircon将从本地链接上的引导服务器获取新的Zircon系统，并尝试kexec进入新映像，从而替换当前正在运行的Zircon实例。

This setting implies **zircon.system.disable-automount=true**  此设置意味着** zircon.system.disable-automount = true **

 
## netsvc.disable=\<bool>  netsvc.disable = \ <布尔> 

If set to true (default), `netsvc` is disabled.  如果设置为true（默认），则禁用“ netsvc”。

 
## netsvc.advertise=\<bool>  netsvc.advertise = \ <布尔> 

If true, netsvc will seek a bootserver by sending netboot advertisements. Defaults to true. 如果为true，netsvc将通过发送netboot广告来寻找引导服务器。默认为true。

 
## netsvc.interface=\<path>  netsvc.interface = \ <路径> 

This option instructs netsvc to use only the ethernet device at the given topological path. All other ethernet devices are ignored by netsvc. Thetopological path for a device can be determined from the shell by running the`lsdev` command on the ethernet class device (e.g., `/dev/class/ethernet/000`). 此选项指示netsvc在给定的拓扑路径上仅使用以太网设备。 netsvc将忽略所有其他以太网设备。设备的拓扑路径可以通过在以太网类设备（例如，/ dev / class / ethernet / 000）上运行lsdev命令来从外壳程序中确定。

This is useful for configuring network booting for a device with multiple ethernet ports which may be enumerated in a non-deterministic order. 这对于为具有多个以太网端口的设备配置网络启动很有用，这些端口可能以不确定的顺序枚举。

 
## netsvc.all-features=\<bool>  netsvc.all-features = \ <布尔> 

This option makes `netsvc` work normally and support all features. By default, `netsvc` starts in a minimal mode where only device discovery is supported. 这个选项使`netsvc`能够正常工作并支持所有功能。默认情况下，“ netsvc”以最小模式启动，其中仅支持设备发现。

 
## userboot=\<path>  userboot = \ <路径> 

This option instructs the userboot process (the first userspace process) to execute the specified binary within the bootfs, instead of following thenormal userspace startup process (launching the device manager, etc). 此选项指示用户引导进程（第一个用户空间进程）在bootfs中执行指定的二进制文件，而不是遵循正常的用户空间启动过程（启动设备管理器等）。

It is useful for alternate boot modes (like a factory test or system unit tests). 对于备用引导模式（例如工厂测试或系统单元测试）很有用。

The pathname used here is relative to `userboot.root` (below), if set, or else relative to the root of the BOOTFS (which later is ordinarilyseen at `/boot`).  It should not start with a `/` prefix. 此处使用的路径名相对于`userboot.root`（在下面）（如果已设置），或者相对于BOOTFS的根目录（以后通常在`/ boot`中看到）。它不能以`/`前缀开头。

If this executable uses `PT_INTERP` (i.e. the dynamic linker), the userboot process provides a [loader service](/docs/concepts/booting/program_loading.md#the-loader-service) toresolve the `PT_INTERP` (dynamic linker) name and any shared library names itmay request.  That service simply looks in the `lib/` directory (under`userboot.root`) in the BOOTFS. 如果此可执行文件使用“ PT_INTERP”（即动态链接器），则用户启动进程将提供[loader服务]（/ docs / concepts / booting / program_loading.mdthe-loader-service）来解析“ PT_INTERP”（动态链接器）名称和它可能要求的任何共享库名称。该服务只是在BOOTFS的lib /目录下（在userboot.root下）。

Example: `userboot=bin/core-tests`  例如：`userboot = bin / core-tests`

 
## userboot.root=\<path>  userboot.root = \ <路径> 

This sets a "root" path prefix within the BOOTFS where the `userboot` path and the `lib/` directory for the loader service will be found.  By default, thereis no prefix so paths are treated as exact relative paths from the root of theBOOTFS.  e.g. with `userboot.root=pkg/foo` and `userboot=bin/app`, the namesfound in the BOOTFS will be `pkg/foo/bin/app`, `pkg/foo/lib/ld.so.1`, etc. 这会在BOOTFS中设置一个“ root”路径前缀，在该路径中将找到loader服务的`userboot`路径和`lib /`目录。默认情况下，没有前缀，因此将路径视为从BOOTFS根目录开始的确切相对路径。例如使用`userboot.root = pkg / foo`和`userboot = bin / app`，在BOOTFS中找到的名称将是`pkg / foo / bin / app`，`pkg / foo / lib / ld.so.1，等等

 
## userboot.reboot  userboot.reboot 

If this option is set, userboot will attempt to reboot the machine after waiting 3 seconds when the process it launches exits. 如果设置了此选项，则在启动进程退出后等待3秒后，userboot将尝试重新启动计算机。

*If running a "ZBI test" image in QEMU, this will cause the system to continually run tests and reboot.*  For QEMU, `userboot.shutdown` is usuallypreferable. *如果在QEMU中运行“ ZBI测试”映像，则将导致系统连续运行测试并重新启动。*对于QEMU，通常首选`userboot.shutdown`。

 
## userboot.shutdown  userboot.shutdown 

If this option is set, userboot will attempt to power off the machine when the process it launches exits.  Note if `userboot.reboot` is setthen `userboot.shutdown` will be ignored. 如果设置此选项，则userboot将在启动计算机的进程退出时尝试关闭计算机电源。注意，如果设置了“ userboot.reboot”，那么“ userboot.shutdown”将被忽略。

 
## vdso.ticks_get_force_syscall=\<bool>  vdso.ticks_get_force_syscall = \ <布尔> 

If this option is set, the `zx_ticks_get` vDSO call will be forced to be a true syscall, even if the hardware cycle counter registers are accessible fromuser-mode.  Defaults to false. 如果设置了该选项，则即使可以从用户模式访问硬件循环计数器寄存器，也将强制zz_ticks_getvDSO调用为真正的syscall。默认为false。

 
## vdso.clock_get_monotonic_force_syscall=\<bool>  vdso.clock_get_monotonic_force_syscall = \ <布尔> 

If this option is set, the `zx_clock_get_monotonic` vDSO call will be forced to be a true syscall, instead of simply performing a transformation of the tickcounter in user-mode.  Defaults to false. 如果设置了此选项，则将强制zz_clock_get_monotonic vDSO调用为真正的syscall，而不是简单地在用户模式下执行滴答计数器的转换。默认为false。

 
## virtcon.disable  禁用病毒 

Do not launch the virtual console service if this option is present.  如果存在此选项，请不要启动虚拟控制台服务。

 
## virtcon.hide-on-boot  virtcon.hide-on-boot 

If this option is present, the virtual console will not take ownership of any displays until the user switches to it with a device control key combination. 如果存在此选项，则在用户使用设备控制键组合切换到虚拟控制台之前，虚拟控制台将不会拥有任何显示的所有权。

 
## virtcon.keep-log-visible  virtcon.keep-log-visible 

If this option is present, the virtual console service will keep the debug log (vc0) visible instead of switching to the first shell (vc1) at startup. 如果存在此选项，则虚拟控制台服务将使调试日志（vc0）保持可见，而不是在启动时切换到第一个shell（vc1）。

 
## virtcon.keymap=\<name>  virtcon.keymap = \ <名称> 

Specify the keymap for the virtual console.  "qwerty" and "dvorak" are supported.  指定虚拟控制台的键盘映射。支持“ qwerty”和“ dvorak”。

 
## virtcon.font=\<name>  virtcon.font = \ <名称> 

Specify the font for the virtual console.  "9x16" and "18x32" are supported.  指定虚拟控制台的字体。支持“ 9x16”和“ 18x32”。

 
## zircon.nodename=\<name>  zircon.nodename = \ <名称> 

Set the system nodename, as used by `bootserver`, `loglistener`, and the `net{addr,cp,ls,runcmd}` tools.  If omitted, the system will generate ahuman-readable nodename from its MAC address.  This cmdline is honored byGigaBoot and Zircon. 设置系统节点名，如“ bootserver”，“ loglistener”和“ net {addr，cp，ls，runcmd}”工具所使用。如果省略，则系统将从其MAC地址生成人类可读的节点名。此cmdline由GigaBoot和Zircon表示荣幸。

 
## console.path=\<path>  console.path = \ <路径> 

Specify console device path. If not specified device manager will open `/dev/misc/console`. Only has effect if kernel.shell=false. 指定控制台设备路径。如果未指定，设备管理器将打开`/ dev / misc / console`。仅在kernel.shell = false时有效。

 
## console.is_virtio=\<bool>  console.is_virtio = \ <布尔> 

Specify if the device given with `console.path` is a virtio-console device. Defaults to false.  This is needed as a workaround due to drivers not being ableto implement fuchsia.io.File themselves. 指定用`console.path`给出的设备是否是virtio-console设备。默认为false。由于驱动程序自身无法实现fuchsia.io.File，因此需要此解决方法。

 
# Additional Gigaboot Commandline Options  其他Giga Boot命令行选项 

 
## bootloader.timeout=\<num>  bootloader.timeout = \ <数字>This option sets the boot timeout in the bootloader, with a default of 3 seconds. Set to zero to skip the boot menu. 此选项在引导加载程序中设置引导超时，默认值为3秒。设置为零可跳过启动菜单。

 
## bootloader.fbres=\<w>x\<h>  bootloader.fbres = \ <w> x \ <h>This option sets the framebuffer resolution. Use the bootloader menu to display available resolutions for the device. 此选项设置帧缓冲区分辨率。使用引导加载程序菜单显示设备的可用分辨率。

Example: `bootloader.fbres=640x480`  范例：`bootloader.fbres = 640x480`

 
## bootloader.default=\<network|local|zedboot>  bootloader.default = \ <网络|本地| zedboot>This option sets the default boot device to netboot, use a local zircon.bin or to netboot via zedboot.  此选项将默认引导设备设置为netboot，使用本地zircon.bin或通过zedboot进行netboot。

 
# How to pass the commandline to the kernel  如何将命令行传递给内核 

 
## in the emulator or Qemu, using fx emu or fx qemu  在仿真器或Qemu中，使用fx emu或fx qemu 

Pass each option using -c, for example:  使用-c传递每个选项，例如：

```
fx qemu -c gfxconsole.font=18x32 -c gfxconsole.early=false
```
 

 
## in GigaBoot20x6, when netbooting  网络引导时，在GigaBoot20x6中 

Pass the kernel commandline at the end, after a -- separator, for example:  在-分隔符之后，最后传递内核命令行，例如：

```
bootserver zircon.bin bootfs.bin -- gfxconsole.font=18x32 gfxconsole.early=false
```
 

 
## in GigaBoot20x6, when booting from USB flash  从USB闪存启动时，在GigaBoot20x6中 

