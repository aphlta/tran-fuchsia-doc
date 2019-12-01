 
# Zircon program loading and dynamic linking  Zircon程序加载和动态链接 

In Zircon, the kernel is not directly involved in normal program loading. Instead, the kernel provides the building blocks fromwhich userspace program loading is built, such as[Virtual Memory Objects](/docs/concepts/objects/vm_object.md), [processes](/docs/concepts/objects/process.md),[Virtual Memory Address Regions](/docs/concepts/objects/vm_address_region.md), and [threads](/docs/concepts/objects/thread.md). 在Zircon中，内核不直接参与正常的程序加载。相反，内核提供了构建用户空间程序加载所基于的构建块，例如[虚拟内存对象]（/ docs / concepts / objects / vm_object.md），[进程]（/ docs / concepts / objects / process.md） ，[虚拟内存地址区域]（/ docs / concepts / objects / vm_address_region.md）和[线程]（/ docs / concepts / objects / thread.md）。

Note: The only time that the kernel is involved in program loading is when you bootstrap the userspace environment at system startup. See [`userboot`](userboot.md) for more information. 注意：内核唯一参与程序加载的时间是在系统启动时引导用户空间环境。有关更多信息，请参见[`userboot`]（userboot.md）。

[TOC]  [目录]

 
## ELF and the system ABI  ELF和系统ABI 

The standard Zircon userspace environment uses the [Executable and Linkable Format (ELF)](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) for machine-code executable files, and provides a dynamic linker andC/C++ execution environment based on ELF. Zircon processes canuse [system calls] only through the Zircon [vDSO](/docs/concepts/kernel/vdso.md), which isprovided by the kernel in ELF format and uses the C/C++ calling conventionscommon to ELF-based systems. 标准的Zircon用户空间环境使用[可执行文件和可链接格式（ELF）]（https://en.wikipedia.org/wiki/Executable_and_Linkable_Format）来获取机器代码可执行文件，并提供基于以下内容的动态链接器和C / C ++执行环境： ELF。 Zircon进程只能通过Zircon [vDSO]（/ docs / concepts / kernel / vdso.md）使用[系统调用]，Zircon [vDSO]由内核以ELF格式提供，并使用基于ELF的系统常见的C / C ++调用约定。

Userspace code (given the appropriate capabilities) can use [system calls] to  directly create processes and load programs withoutusing ELF, but Zircon's standard ABI for machine code uses ELF as described here. 用户空间代码（具有适当的功能）可以使用[系统调用]直接创建进程并加载程序，而无需使用ELF，但是Zircon的机器代码标准ABI使用ELF，如此处所述。

 
## Background: Traditional ELF program loading  背景：传统的ELF程序加载 

[ELF](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) was introduced with Unix System V Release 4 and became the common standardexecutable file format for most Unix-like systems. In these systems,the kernel integrates program loading with filesystem access using the POSIX`execve` API. There are some variations in how these systems load ELF programs, butmost follow this pattern: [ELF]（https://en.wikipedia.org/wiki/Executable_and_Linkable_Format）在Unix System V Release 4中引入，并成为大多数类Unix系统的通用标准可执行文件格式。在这些系统中，内核使用POSIX`execve` API将程序加载与文件系统访问集成在一起。这些系统加载ELF程序的方式有所不同，但大多数遵循以下模式：

 
 1. The kernel loads the file by name, and checks whether it's ELF or some other kind of file that system supports. This is where `#!` scripthandling is done, and non-ELF format support when present. 1.内核按名称加载文件，并检查它是系统支持的ELF还是其他类型的文件。这是完成`！`脚本处理的地方，并且提供非ELF格式支持。
 2. The kernel maps the ELF image according to its `PT_LOAD` program headers. For an `ET_EXEC` file, this places the program's segments atfixed addresses in memory specified in `p_vaddr`. For an `ET_DYN`file, the system chooses the base address where the program's first`PT_LOAD` gets loaded, and following segments are placed according totheir `p_vaddr` relative to the first segment's `p_vaddr`. Usually thebase address is chosen randomly (ASLR). 2.内核根据其“ PT_LOAD”程序头映射ELF映像。对于`ET_EXEC`文件，这会将程序段的固定地址放在`p_vaddr`中指定的内存中。对于“ ET_DYN”文件，系统选择加载程序的第一个“ PT_LOAD”的基址，并根据它们的“ p_vaddr”相对于第一个段的“ p_vaddr”放置后续的段。通常，基地址是随机选择的（ASLR）。
 3. If there was a `PT_INTERP` program header, its contents (a range of bytes in the ELF file given by `p_offset` and `p_filesz`) is looked upas a file name to find another ELF file called the *ELF interpreter*.This must be an `ET_DYN` file. The kernel loads it in the same way as itloaded the executable, but always at a location of its own choosing.The interpreter program is usually the ELF dynamic linker with a namelike `/lib/ld.so.1` or `/lib/ld-linux.so.2`, but the kernel loadswhatever file is named. 3.如果有一个“ PT_INTERP”程序头，则将其内容（由p_offset和p_filesz给定的ELF文件中的字节范围）查找为文件名，以找到另一个称为* ELF解释器*的ELF文件。该文件必须是`ET_DYN`文件。内核以与加载可执行文件相同的方式加载它，但始终在其自己选择的位置。解释程序通常是ELF动态链接程序，其名称类似于`/ lib / ld.so.1`或`/ lib / ld-linux.so.2`，但无论文件名如何，内核都会加载。
 4. The kernel sets up the stack and registers for the initial thread, and starts the thread running with the PC at the chosen entry point address. 4.内核设置堆栈并为初始线程注册，然后在选定的入口点地址启动与PC一起运行的线程。

 
     * The entry point is the `e_entry` value from the ELF file header, adjusted by base address. When there was a `PT_INTERP`, the entrypoint is that of the interepreter rather than the main executable. *入口点是ELF文件头中的e_entry值，由基地址调整。当有一个“ PT_INTERP”时，入口点就是解释器的入口，而不是主可执行文件。
     * There is an assembly-level protocol of register and stack contents that the kernel sets up for the program to receive its argument andenvironment strings and an *auxiliary vector* of useful values. Whenthere was a `PT_INTERP`, these include the base address, entry point,and program header table address from the main executable's ELFheaders. This information allows the dynamic linker to find the mainexecutable's ELF dynamic linking metadata in memory and do its work.When dynamic linking startup is complete, the dynamic linker jumps tothe main executable's entry point address. *内核设置了一种寄存器和堆栈内容的汇编级协议，内核为程序设置了协议，以接收其自变量和环境字符串以及有用值的*辅助向量*。当有一个“ PT_INTERP”时，它们包括主可执行文件的ELFheader中的基地址，入口点和程序头表地址。通过此信息，动态链接程序可以在内存中找到主要可执行文件的ELF动态链接元数据并执行其工作。完成动态链接启动后，动态链接程序将跳转到主可执行文件的入口点地址。

Zircon program loading is inspired by this tradition, but does it somewhat differently. A key reason for the traditional pattern of loading theexecutable before loading the dynamic linker is that the dynamic linker'srandomly-chosen base address must not intersect with the fixed addressesused by an `ET_EXEC` executable file. Zircon does not supportfixed-address program loading (ELF `ET_EXEC` files) at all, onlyposition-independent executables or *PIE*s, which are ELF `ET_DYN` files. Zircon程序加载受此传统启发，但有所不同。传统的在加载动态链接器之前加载可执行文件的模式的主要原因是，动态链接器的随机选择基地址不得与ET_EXEC可执行文件使用的固定地址相交。 Zircon完全不支持固定地址的程序加载（ELF`ET_EXEC`文件），仅支持与位置无关的可执行文件或* PIE * s，它们是ELF`ET_DYN`文件。

 
## The **launchpad** library  ** launchpad **库 

The main implementation of program loading resides in the [`launchpad` library](/zircon/system/ulib/launchpad/). It has a C APIin[`<launchpad/launchpad.h>`](/zircon/system/ulib/launchpad/include/launchpad/launchpad.h) butis not formally documented. The `launchpad` API is not described here. Itstreatment of executable files and process startup forms the Zircon systemABI for program loading.The [lowest userspace layers of the system](userboot.md) implement the sameprotocols. 程序加载的主要实现位于[`launchpad`库]（/ zircon / system / ulib / launchpad /）中。它具有C APIin [`<launchpad / launchpad.h>`]（/ zircon / system / ulib / launchpad / include / launchpad / launchpad.h），但未正式记录。这里不介绍`launchpad` API。它对可执行文件的处理和进程的启动形成了Zircon systemABI，用于加载程序。[系统的最低用户空间层]（userboot.md）实施相同的协议。

Filesystems are not part of the lower layers of Zircon API. Instead, program loading is based on [VMOs](/docs/concepts/objects/vm_object.md) and on IPCprotocols used through [channels](/docs/concepts/objects/channel.md). 文件系统不属于Zircon API较低层的一部分。相反，程序加载基于[VMO]（/ docs / concepts / objects / vm_object.md）和通过[channel]（/ docs / concepts / objects / channel.md）使用的IPC协议。

A program loading request starts with:  程序加载请求始于：

 
 * A handle to a VMO containing the executable file (`ZX_RIGHT_READ` and `ZX_RIGHT_EXECUTE` rights are required) *包含可执行文件的VMO的句柄（必须具有`ZX_RIGHT_READ`和`ZX_RIGHT_EXECUTE`权限）
 * A list of argument strings (to become `argv[]` in a C/C++ program)  *参数字符串列表（在C / C ++程序中变为`argv []`）
 * A list of environment strings (to become `environ[]` in a C/C++ program)  *环境字符串列表（在C / C ++程序中成为`environ []`）
 * A list of initial [handles](/docs/concepts/objects/handles.md), each with a [*handle info entry*](#handle-info-entry) *初始[handles]列表（/docs/concepts/objects/handles.md），每个列表均带有[* handle info entry *]（handle-info-entry）

Three types of file are handled:  处理三种类型的文件：

 
### A script file starting with `#!` {#hashbang}  以`！`{hashbang}开头的脚本文件 

  The first line of the file starts with `#!` and must be no more than 127 characters long. The first non-whitespace word following `#!` is the*script interpreter name*. If there's anything after that, it alltogether becomes the *script interpreter argument*. 文件的第一行以`！`开头，并且不得超过127个字符。 “！”之后的第一个非空白单词是*脚本解释程序名称*。如果之后没有其他内容，它将一起成为* script解释器参数*。

 
   * The script interpreter name is prepended to the original argument list (to become `argv[0]`). *脚本解释器名称位于原始参数列表的前面（成为“ argv [0]”）。
   * If there was a script interpreter argument, it's inserted between the interpreter name and the original argument list (to become `argv[1]`,with the original `argv[0]` becoming `argv[2]`). *如果有脚本解释器参数，则将其插入解释器名称和原始参数列表之间（变为argv [1]，而原始argv [0]变为argv [2]）。
   * The program loader looks up the script interpreter name via the [loader service](#the-loader-service) to get a new VMO. *程序加载器通过[加载器服务]（the-loader-service）查找脚本解释器名称，以获取新的VMO。
   * Program loading restarts on that script interpreter VMO with the modified argument list but everything else the same. The VMO handlefor the original executable is just closed; the script interpreter onlygets the original `argv[0]` string to work with, not the original VMO.There is a maximum nesting limit (currently 5) constraining how manysuch restarts will be allowed before program loading just fails. *使用修改后的参数列表在该脚本解释器VMO上重新启动程序加载，但其他所有操作都相同。原始可执行文件的VMO句柄刚刚关闭；脚本解释器仅使用原始的“ argv [0]”字符串，而不使用原始的VMO。最大嵌套限制（当前为5）限制了在程序加载失败之前允许多少次此类重新启动。

 
### An ELF `ET_DYN` file with no `PT_INTERP`  没有`PT_INTERP`的ELF`ET_DYN`文件 

 
  * The system chooses a random base address for the first `PT_LOAD` segment and then maps in each `PT_LOAD` segment relative to that base address.This is done by creating a [VMAR](/docs/concepts/objects/vm_address_region.md) coveringthe whole range from the first page of the first segment to the lastpage of the last segment. *系统会为第一个“ PT_LOAD”段选择一个随机的基地址，然后相对于该基地址在每个“ PT_LOAD”段中进行映射。这是通过创建[VMAR]（/ docs / concepts / objects / vm_address_region.md ），涵盖从第一段的第一页到最后一段的最后一页的整个范围。
  * A VMO is created and mapped at another random address to hold the stack for the initial thread. If there was a `PT_GNU_STACK` program headerwith a nonzero `p_memsz`, that determines the size of the stack (roundedup to whole pages). Otherwise, a reasonable default stack size is used. *创建一个VMO并将其映射到另一个随机地址以保存初始线程的堆栈。如果有一个带有非零p_memsz的PT_GNU_STACK程序头，则确定堆栈的大小（向上舍入到整个页面）。否则，将使用合理的默认堆栈大小。
  * The [vDSO](/docs/concepts/kernel/vdso.md) is mapped into the process (another VMO containing an ELF image), also at a random base address. * [vDSO]（/ docs / concepts / kernel / vdso.md）也映射到进程（另一个包含ELF图像的VMO）中，也位于随机基址上。
  * A new thread is created in the process with [`zx_thread_create()`].  *在进程中使用[`zx_thread_create（）`]创建一个新线程。
  * A new [channel](/docs/concepts/objects/channel.md) is created, called the *bootstrap channel*. The program loader writes into this channel a messagein [the `processargs` protocol](#the-processargs-protocol) format. This*bootstrap message* includes the argument and environment strings andthe initial handles from the original request. That list is augmentedwith handles for: *创建了一个新的[channel]（/ docs / concepts / objects / channel.md），称为*引导程序通道*。程序加载器以[processargs协议]（-processargs-protocol）格式将消息写入此通道。该*引导消息*包括参数和环境字符串以及原始请求的初始句柄。该列表增加了以下内容的句柄：

 
     * the new [process](/docs/concepts/objects/process.md) itself  *新的[process]（/ docs / concepts / objects / process.md）本身
     * its root [VMAR](/docs/concepts/objects/vm_address_region.md)  *其根[VMAR]（/ docs / concepts / objects / vm_address_region.md）
     * its initial [thread](/docs/concepts/objects/thread.md)  *其初始[thread]（/ docs / concepts / objects / thread.md）
     * the VMAR covering where the executable was loaded  * VMAR涵盖了可执行文件的加载位置
     * the VMO just created for the stack  *刚刚为堆栈创建的VMO
     * optionally, a default [job](/docs/concepts/objects/job.md) so the new process itself can create more processes *（可选）默认的[job]（/ docs / concepts / objects / job.md），以便新流程本身可以创建更多流程
     * optionally, the vDSO VMO so the new process can let the processes it creates make system calls themselves * vDSO VMO是可选的，因此新进程可以让其创建的进程自己进行系统调用

    The program loader then closes its end of the channel.  程序加载器然后关闭其通道末尾。
   * The initial thread is launched with the [`zx_process_start()`] system call: *初始线程是通过[`zx_process_start（）`]系统调用启动的：

 
      * `entry` sets the new thread's PC to `e_entry` from the executable's ELF header, adjusted by base address. *`entry`从可执行文件的ELF标头中将新线程的PC设置为`e_entry`，并根据基地址进行调整。
      * `stack` sets the new thread's stack pointer to the top of the stack mapping. *`stack`将新线程的堆栈指针设置到堆栈映射的顶部。
      * `arg1` transfers the handle to the *bootstrap channel* into the first argument register in the C ABI. *`arg1`将句柄传递给*引导通道*到C ABI中的第一个参数寄存器中。
      * `arg2` passes the base address of the vDSO into the second argument register in the C ABI. *`arg2`将vDSO的基地址传递到C ABI中的第二个参数寄存器中。

     Thus, the program entry point can be written as a C function:  因此，程序入口点可以编写为C函数：

     ```c
     noreturn void _start(zx_handle_t bootstrap_channel, uintptr_t vdso_base);
     ```
 

 
### An ELF `ET_DYN` file with a `PT_INTERP` {#pt-interp}  具有`PT_INTERP` {pt-interp}的ELF`ET_DYN`文件 

  In this case, the program loader does not directly use the VMO containing the ELF executable after reading its `PT_INTERP` header. Instead, ituses the `PT_INTERP` contents as the name of an *ELF interpreter*. Thisname is used in a request to the [loader service](#the-loader-service) toget a new VMO containing the ELF interpreter, which is another ELF`ET_DYN` file. Then that VMO is loaded instead of the main executable'sVMO. Startup is as described above, with these differences: 在这种情况下，程序加载器在读取其“ PT_INTERP”标头后不会直接使用包含ELF可执行文件的VMO。相反，它使用“ PT_INTERP”内容作为* ELF解释器*的名称。此名称用于对[加载程序服务]（the-loader-service）的请求中，以获取一个包含ELF解释程序的新VMO，该解释程序是另一个ELF`ET_DYN`文件。然后，将加载该VMO而不是主可执行文件的VMO。如上所述，启动时有以下区别：

 
   * An extra message in [the `processargs` protocol](#the-processargs-protocol) is writtento the *bootstrap channel*, preceding the main bootstrap message. TheELF interpreter is expected to consume this *loader bootstrap message*itself so that it can do its work, but then leave the second bootstrapmessage in the channel and hand off the bootstrap channel handle tothe main program's entry point. The *loader bootstrap message*includes only the necessary handles added by the program loader, notthe full set that go into the main *bootstrap message*, plus these: * [bootargs协议]（the-processargs-protocol）中的一条额外消息被写入主引导程序消息之前的* bootstrap通道*。 ELF解释器应自行使用此* loader引导程序消息*，以便可以完成其工作，但随后将第二个引导程序消息留在通道中，并将引导程序通道句柄移交给主程序的入口点。 * loader bootstrap消息*仅包括程序加载器添加的必要句柄，不包括进入主* bootstrap消息*的完整句柄，以及以下内容：

 
      * the original VMO handle for main ELF executable  *主ELF可执行文件的原始VMO句柄
      * a channel handle to the [loader service](#the-loader-service)  * [加载程序服务]（the-loader-service）的通道句柄

     These allow the ELF interpreter to do its own loading of the executable from the VMO and to use the loader service to getadditional VMOs for shared libraries to load. The message alsoincludes the argument and environment strings, which lets the ELFinterpreter use `argv[0]` in its log messages, and check forenvironment variables like `LD_DEBUG`. 这些允许ELF解释器从VMO自己执行可执行文件的加载，并允许使用加载程序服务获取其他VMO，以便加载共享库。该消息还包括参数和环境字符串，这使ELF解释程序在其日志消息中使用“ argv [0]”，并检查环境变量（如LD_DEBUG）。

 
   * `PT_GNU_STACK` program headers are ignored. Instead, the program loader chooses a minimal stack size that is just large enough tocontain the *loader bootstrap message* plus some breathing room forthe ELF interpreter's startup code to use as call frames. This"breathing room" size is `PTHREAD_STACK_MIN` in the source, and istuned such that with a small bootstrap message size the whole stack isonly a single page, but a careful dynamic linker implementation hasenough space to work in. The dynamic linker is expected to read themain executable's `PT_GNU_STACK` and switch to a stack of reasonablesize for normal use before it jumps to the main executable's entrypoint. *`PT_GNU_STACK`程序头被忽略。取而代之的是，程序加载器选择一个最小的堆栈大小，该大小恰好足以容纳* loader引导消息*，并为ELF解释器的启动代码用作调用帧提供了一些喘息的空间。此“呼吸室”的大小在源中为`PTHREAD_STACK_MIN`，并且进行了调整，以使引导消息大小较小时，整个堆栈仅占一个页面，但是谨慎的动态链接器实现具有足够的工作空间。动态链接器有望读取主可执行文件的PT_GNU_STACK并切换到合理大小的堆栈以供正常使用，然后再跳转到主可执行文件的入口点。

Note: The program loader chooses three randomly-placed chunks of the new process's address space before the program (or dynamic linker) getscontrol: the vDSO, the stack, and the dynamic linker itself. To make itpossible for the program's own startup to control its address space morefully, the program loader currently ensures that these random placementsare always somewhere in the upper half of the address space. This isfor the convenience of sanitizer runtimes, which need to reserve some lowerfraction of the address space. 注意：程序加载器在程序（或动态链接器）获得控制权之前选择新进程地址空间的三个随机放置的块：vDSO，堆栈和动态链接器本身。为了使程序自己的启动能够更好地控制其地址空间，程序加载器当前确保这些随机位置始终位于地址空间的上半部分。这是为了方便清理程序运行时，后者需要保留地址空间的较小部分。

 
## The **processargs** protocol  ** processargs **协议 

[`<zircon/processargs.h>`](/zircon/system/public/zircon/processargs.h) defines the protocol for the *bootstrap message* sent on the *bootstrap channel* bythe program loader. When a process starts up, it has a handle to thisbootstrap channel and it has access to [system calls] throughthe [vDSO](/docs/concepts/kernel/vdso.md). The process has only this one handle and so it cansee only global system information and its own memory until it gets moreinformation and handles through the bootstrap channel. [`<zircon / processargs.h>`]（/ zircon / system / public / zircon / processargs.h）定义了程序加载程序在* bootstrap通道*上发送的* bootstrap消息*的协议。进程启动时，它具有此引导通道的句柄，并且可以通过[vDSO]（/ docs / concepts / kernel / vdso.md）访问[系统调用]。该进程只有一个句柄，因此它只能看到全局系统信息及其自己的内存，直到它获取更多信息并通过引导程序通道进行处理为止。

The `processargs` protocol is a one-way protocol for messages sent on the bootstrap channel. The new process is never expected to write back ontothe channel. The program loader usually sends its messages and then closesits end of the channel before the new process has even started. Thesemessages must communicate everything a new process will ever need, but thecode that receives and decodes messages in this format must run in a veryconstrained environment. Heap allocation is impossible and nontrivial whenlibrary facilities may not be available. “ processargs”协议是用于在引导程序通道上发送的消息的单向协议。切勿期望新过程会写回到通道上。程序加载器通常会发送其消息，然后在新进程开始之前关闭其通道末尾。这些消息必须传达新进程将需要的所有信息，但是以这种格式接收和解码消息的代码必须在非常受限的环境中运行。堆分配是不可能的，并且当图书馆设施不可用时，这是很重要的。

See the [header file](/zircon/system/public/zircon/processargs.h) for full details of the message format. It's anticipated that this ad hoc protocolwill be replaced with a formal IDL-based protocol eventually, but theformat will be kept simple enough to be decoded by simple hand-writtencode. 有关消息格式的完整详细信息，请参见[头文件]（/ zircon / system / public / zircon / processargs.h）。预计最终将用基于IDL的正式协议来代替该临时协议，但是该格式将保持足够简单，以便可以通过简单的手写代码进行解码。

A bootstrap message conveys:  引导消息传达：

 
 * a list of initial [handles](/docs/concepts/objects/handles.md)  *初始[handles]列表（/docs/concepts/objects/handles.md）
 * a 32-bit *handle info entry* corresponding to each handle  *与每个句柄相对应的32位*句柄信息条目*
 * a list of name strings that a *handle info entry* can refer to  *处理信息条目*可以引用的名称字符串列表
 * a list of argument strings (to become `argv[]` in a C/C++ program)  *参数字符串列表（在C / C ++程序中成为`argv []`）
 * a list of environment strings (to become `environ[]` in a C/C++ program)  *环境字符串列表（在C / C ++程序中成为`environ []`）

 
### Handle info entry {#handle-info-entry}  处理信息条目{handle-info-entry}The handles serve many purposes, indicated by the *handle info entry* type:  句柄有多种用途，由* handle info entry *类型指示：

 
 * essential handles for the process to make [system calls](/docs/reference/syscalls/README.md): [process](/docs/concepts/objects/process.md), [VMAR](/docs/concepts/objects/vm_address_region.md),[thread](/docs/concepts/objects/thread.md), [job](/docs/concepts/objects/job.md) *进行[系统调用]的过程的必要句柄：[process]（/ docs / concepts / objects / process.md），[VMAR]（/ docs / concepts / objects / vm_address_region.md），[thread]（/ docs / concepts / objects / thread.md），[job]（/ docs / concepts / objects / job.md）
 * [channel](/docs/concepts/objects/channel.md) to the [loader service](#the-loader-service)  * [channel]（/ docs / concepts / objects / channel.md）到[loader服务]（the-loader-service）
 * [vDSO](/docs/concepts/kernel/vdso.md) [VMO](/docs/concepts/objects/vm_object.md)  * [vDSO]（/ docs / concepts / kernel / vdso.md）[VMO]（/ docs / concepts / objects / vm_object.md）
 * filesystem-related handles: current directory, file descriptors, name space bindings (these encode an index into the list of name strings) *与文件系统相关的句柄：当前目录，文件描述符，名称空间绑定（这些绑定将索引编码到名称字符串列表中）
 * special handles for system processes: [resource](/docs/concepts/objects/resource.md), [VMO](/docs/concepts/objects/vm_object.md) *系统进程的特殊句柄：[资源]（/ docs / concepts / objects / resource.md），[VMO]（/ docs / concepts / objects / vm_object.md）
 * other types used for higher-layer or private protocol purposes  *用于更高层或专用协议目的的其他类型

Most of these are just passed through by the program loader, which does not need to know what they're for. 其中大多数只是由程序加载器传递的，程序加载器不需要知道它们的用途。

 
## The **loader service**  **加载程序服务** 

In dynamic linking systems, an executable file refers to and uses at runtime additional files containing shared libraries and plugins. Thedynamic linker is loaded as an [*ELF interpreter*](#pt-interp) and isresponsible getting access to all these additional files to completedynamic linking before the main program's entry point gets control. 在动态链接系统中，可执行文件引用并在运行时使用包含共享库和插件的其他文件。动态链接器作为[* ELF解释器*]（pt-interp）加载，负责在主程序的入口点得到控制之前对所有这些附加文件进行访问以完成动态链接。

All of Zircon's standard userspace uses dynamic linking, down to the very first process loaded by [`userboot`](userboot.md). Device drivers andfilesystems are implemented by userspace programs loaded this way. Soprogram loading cannot be defined in terms of higher-layer abstractionssuch as a filesystem paradigm,as[traditional systems have done](#background_traditional-elf-program-loading).Instead, program loading is based only on [VMOs](/docs/concepts/objects/vm_object.md) anda simple [channel](/docs/concepts/objects/channel.md)-based protocol. Zircon的所有标准用户空间都使用动态链接，一直到[`userboot`]（userboot.md）加载的第一个进程。设备驱动程序和文件系统由以此方式加载的用户空间程序实现。因此，程序加载不能像文件系统范式这样的高层抽象来定义，因为[传统系统已完成]（background_traditional-elf-program-loading）。相反，程序加载仅基于[VMO]（/ docs / concepts /objects/vm_object.md）和一个基于[channel]（/ docs / concepts / objects / channel.md）的简单协议。

This *loader service* protocol is how a dynamic linker acquires VMOs representing the additional files it needs to load as shared libraries. 这种* loader服务*协议是动态链接程序如何获取VMO的方式，这些VMO表示需要作为共享库加载的其他文件。

This is a simple RPC protocol, defined in [`<zircon/processargs.h>`](/zircon/system/public/zircon/processargs.h).The code sending loader servicerequests and receiving their replies during dynamic linker startup maynot have access to nontrivial library facilities. 这是一个简单的RPC协议，定义在[`<zircon / processargs.h>`]（/ zircon / system / public / zircon / processargs.h）中。在动态链接程序启动期间发送加载程序servicerequest和接收其响应的代码可能没有使用简单的图书馆设施。

An ELF interpreter receives a channel handle for its loader service in its `processargs` bootstrap message, identified by the *handle info entry*`PA_HND(PA_LDSVC_LOADER, 0)`. All requests are synchronous RPCs madewith [`zx_channel_call()`]. Both requests and replies start with the`zx_loader_svc_msg_t` header; some contain additional data; some containa VMO handle. Request opcodes are: ELF解释器在其“ processargs”引导消息中接收其加载程序服务的通道句柄，该消息由* handle info entry * PA_HND（PA_LDSVC_LOADER，0）标识。所有请求都是使用[`zx_channel_call（）`]进行的同步RPC。请求和回复都以zx_loader_svc_msg_t标头开头；有些包含其他数据；一些包含VMO句柄。请求操作码为：

 
 * `LOADER_SVC_OP_LOAD_SCRIPT_INTERP`: *string* -> *VMO handle*  *`LOADER_SVC_OP_LOAD_SCRIPT_INTERP`：*字符串*-> * VMO句柄*

   The program loader sends the *script interpreter name* from a [`#!` script](#hashbang) and gets back a VMO to execute in place ofthe script. 程序加载器从[`！`脚本]（hashbang）发送*脚本解释器名称*，然后取回VMO以代替脚本执行。

 
 * `LOADER_SVC_OP_LOAD_OBJECT`: *string* -> *VMO handle*  *`LOADER_SVC_OP_LOAD_OBJECT`：*字符串*-> * VMO句柄*

   The dynamic linker sends the name of an *object* (shared library or plugin) and gets back a VMO handle containing the file. 动态链接器发送* object *（共享库或插件）的名称，并获取包含该文件的VMO句柄。

 
 * `LOADER_SVC_OP_CONFIG` : *string* -> `reply ignored`  *`LOADER_SVC_OP_CONFIG`：*字符串*->`忽略回复'

   The dynamic linker sends a string identifying its *load configuration*. This is intended to affect how later `LOADER_SVC_OP_LOAD_OBJECT`requests decide what particular implementation file to supply for agiven name. 动态链接程序发送一个标识其“负载配置”的字符串。这旨在影响稍后的“ LOADER_SVC_OP_LOAD_OBJECT”请求如何确定要为给定名称提供的特定实现文件。

 
 * `LOADER_SVC_OP_DEBUG_PRINT`: *string* -> `reply ignored`  *`LOADER_SVC_OP_DEBUG_PRINT`：*字符串*->`答复被忽略`

   This is a simple ad hoc logging facility intended for debugging the dynamic linker and early program startup issues. It's convenientbecause the early startup code is using the loader service but doesn'thave access to many other handles or complex facilities yet. This willbe replaced in the future with some simple-to-use logging facility thatdoes not go through the loader service. 这是一个简单的临时日志记录工具，用于调试动态链接器和早期程序启动问题。之所以方便，是因为早期的启动代码正在使用加载程序服务，但尚未访问许多其他句柄或复杂的功能。将来将使用一些不通过加载程序服务的简单易用的日志记录工具来代替它。

 
 * `LOADER_SVC_OP_LOAD_DEBUG_CONFIG`: *string* -> *VMO handle*  *`LOADER_SVC_OP_LOAD_DEBUG_CONFIG`：*字符串*-> * VMO句柄*

   **This is intended to be a developer-oriented feature and might not ordinarily be available in production runs.** **这旨在成为面向开发人员的功能，通常在生产运行中可能不可用。**

   The program runtime sends a string naming a *debug configuration* of some kind and gets back a VMO to read configuration data from. Thesanitizer runtimes use this to allow large options text to be stored ina file rather than passed directly in environment strings. 程序运行时发送一个字符串，命名某种“调试配置”，然后返回VMO以从中读取配置数据。 Thesanitizer运行时使用它可以将大选项文本存储在文件中，而不是直接在环境字符串中传递。

 
 * `LOADER_SVC_OP_PUBLISH_DATA_SINK`: *string*, *VMO handle* -> `reply ignored`  *`LOADER_SVC_OP_PUBLISH_DATA_SINK`：*字符串*，* VMO句柄*->`答复被忽略`

   **This is intended to be a developer-oriented feature and might not ordinarily be available in production runs.** **这旨在成为面向开发人员的功能，通常在生产运行中可能不可用。**

   The program runtime sends a string naming a *data sink* and transfers the sole handle to a VMO it wants published there. The *data sink*string identifies a type of data, and the VMO's object name canspecifically identify the data set in this VMO. The client musttransfer the only handle to the VMO (which prevents the VMO beingresized without the receiver's knowledge), but it might still have theVMO mapped in and continue to write data to it. Code instrumentationruntimes use this to deliver large binary trace results. 程序运行时发送一个命名为“数据接收器”的字符串，并将唯一的句柄转移到要在此处发布的VMO。 *数据接收器*字符串标识数据的类型，并且VMO的对象名称可以特定地标识此VMO中的数据集。客户端必须将唯一的句柄转移到VMO（这可以防止在接收者不知情的情况下调整VMO的大小），但是客户端可能仍然映射了VMO并继续向其中写入数据。代码工具运行时使用它来传递大型二进制跟踪结果。

 
## Zircon's standard ELF dynamic linker  Zircon的标准ELF动态链接器 

The ELF conventions described above and the [`processargs`](#the-processargs-protocol)and [loader service](#the-loader-service) protocols are the permanentsystem ABI for program loading. Programs can use any implementation of amachine code executable that meets the basic ELF format conventions. Theimplementation can use the [vDSO](/docs/concepts/kernel/vdso.md) [system calls]. 上面描述的ELF约定以及[`processargs`]（-processargs-protocol）和[loader service]（the-loader-service）协议是用于程序加载的永久系统ABI。程序可以使用满足基本ELF格式约定的机器代码可执行文件的任何实现。该实现可以使用[vDSO]（/ docs / concepts / kernel / vdso.md）[系统调用]。

ABI, the `processargs` data, and the loader service facilities as it sees fit. The exact details of what handles and data that programs receive throughthese protocols depend on the higher-layer program environment. Zircon'ssystem processes use an ELF interpreter that implements basic ELF dynamiclinking, and a simple implementation of the loader service. ABI，`processargs`数据以及认为合适的加载程序服务设施。程序通过这些协议接收的处理和数据的确切详细信息取决于高层程序环境。 Zircon的系统过程使用实现基本ELF动态链接的ELF解释器以及加载程序服务的简单实现。

Zircon's standard C library and dynamic linker have a [unified implementation](/zircon/third_party/ulib/musl/) originally derivedfrom [`musl`](http://www.musl-libc.org/). It's identified by the`PT_INTERP` string `ld.so.1`. It uses the `DT_NEEDED` strings namingshared libraries as [loader service](#the-loader-service) *object* names. Zircon的标准C库和动态链接器具有[统一的实现]（/ zircon / third_party / ulib / musl /），最初是从[`musl`]（http://www.musl-libc.org/）派生的。由PT_INTERP字符串ld.so.1标识。它使用DT_NEEDED字符串命名共享库作为[loader service]（the-loader-service）* object *名称。

The simple loader service maps requests into filesystem access:  简单的加载程序服务将请求映射到文件系统访问：

 
 * *script interpreter* and *debug configuration* names must start with `/` and are used as absolute file names. *脚本解释器和调试配置名称必须以`/`开头，并用作绝对文件名。
 * *data sink* names become subdirectories in `/tmp`, and each VMO published becomes a file in that subdirectory with the VMO's object name * *数据接收器*名称成为`/ tmp`中的子目录，每个发布的VMO都成为该子目录中具有VMO对象名称的文件
 * *object* names are searched for as files in system `lib/` directories.  * *对象*名称在系统“ lib /”目录中作为文件搜索。
 * *load configuration* strings are taken as a subdirectory name, optionally followed by a `!` character. Subdirectories by that name insystem `lib/` directories searched are searched before `lib/` itself.If there was a `!` suffix, *only* those subdirectories are searched.For example, sanitizer runtimes use `asan` because that instrumentationis compatible with uninstrumented library code, but `dfsan!` becausethat instrumentation requires that all code in the process beinstrumented. * * load configuration *字符串被当作子目录名称，可以选择后面跟一个`！`字符。在名称为lib /`的目录之前会搜索系统名称为lib /的子目录，如果后缀为！，仅*搜索这些子目录，例如，消毒剂运行时使用asan，因为该工具兼容使用非工具库代码，但使用dfsan！，因为该检测要求对过程中的所有代码进行工具化。

A version of the standard runtime instrumented with LLVM [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)is identified by the `PT_INTERP` string `asan/ld.so.1`. This version sendsthe *load configuration* string `asan` before loading shared libraries.When [SanitizerCoverage](https://clang.llvm.org/docs/SanitizerCoverage.html)is enabled, it publishes a VMO to the *data sink* name `sancov` and uses aVMO name including the process KOID. LLVM [AddressSanitizer]（https://clang.llvm.org/docs/AddressSanitizer.html）配备的标准运行时版本由“ PT_INTERP”字符串`asan / ld.so.1`标识。此版本在加载共享库之前发送“加载配置”字符串“ asan”。启用[SanitizerCoverage]（https://clang.llvm.org/docs/SanitizerCoverage.html）时，它将VMO发布到*数据接收器*名称`sancov`，并使用aVMO名称，包括进程KOID。

