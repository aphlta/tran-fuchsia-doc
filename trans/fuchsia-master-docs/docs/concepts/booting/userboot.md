 
# Zircon kernel to userspace bootstrapping (`userboot`)  Zircon内核到用户空间的引导（`userboot`） 

Zircon has a microkernel style of design.  A complexity for microkernel designs is how to bootstrap the initial userspace processes.  Often thisis accomplished by having the kernel implement minimal versions offilesystem reading and program loading just for the purpose ofbootstrapping, even when those kernel facilities are never used after boottime.  Zircon takes a different approach. 锆石具有微内核设计风格。微内核设计的复杂性是如何重新引导初始用户空间过程。通常，这是通过使内核仅出于引导目的而实现文件系统读取和程序加载的最低版本来实现的，即使这些内核功能在引导后从未使用过也是如此。锆石采用不同的方法。

[TOC]  [目录]

 
## Boot loader and kernel startup  引导加载程序和内核启动 

A boot loader loads the kernel into memory and transfers control to the kernel's startup code.  The details of the boot loader protocols are notdescribed here.  The boot loaders used with Zircon load both the kernelimage and a data blob in Zircon Boot Image format.The [ZBI format](/zircon/system/public/zircon/boot/image.h) is asimple container format that embeds items passed by the boot loader,including hardware-specific information,the [kernel "command line"](/docs/reference/kernel/kernel_cmdline.md) giving boot options, and RAMdisk images (which are usually compressed).  The kernel extracts someessential information for its own use in the early stages of booting. 引导加载程序将内核加载到内存中，并将控制权转移到内核的启动代码。引导加载程序协议的详细信息在此不再描述。与Zircon一起使用的引导加载程序以Zircon引导映像格式加载内核映像和数据Blob。[ZBI格式]（/ zircon / system / public / zircon / boot / image.h）是嵌入了传递的项目的简单容器格式引导加载程序，包括特定于硬件的信息，提供引导选项的[内核“命令行”]（/ docs / reference / kernel / kernel_cmdline.md）和RAMdisk映像（通常已压缩）。内核会在启动的早期阶段提取一些必需的信息供自己使用。

 
## BOOTFS  引导程序 

One of the items embedded in the Zircon Boot Image is an initial RAM disk filesystem image.  The image is usually compressed using the **LZ4**format.  Once decompressed, the image is in **BOOTFS** format.  This is atrivial read-only filesystem format that simply lists file names, and foreach file the offset and size within the BOOTFS image (both values must bepage-aligned both fields and are limited to 32 bits). Zircon引导映像中嵌入的项目之一是初始RAM磁盘文件系统映像。该图像通常使用** LZ4 **格式压缩。解压缩后，图像为** BOOTFS **格式。这是一种非专有的只读文件系统格式，仅列出文件名，并为每个文件提供BOOTFS映像内的偏移量和大小（这两个值都必须两个页面都页对齐，并且限制为32位）。

The primary BOOTFS image contains everything that the userspace system needs to run: executables, shared libraries, and data files.  These includethe implementations of device drivers and more advanced filesystems thatmake it possible to read more code and data from storage or networkdevices. 主要的BOOTFS映像包含用户空间系统需要运行的所有内容：可执行文件，共享库和数据文件。其中包括设备驱动程序的实现和更高级的文件系统，使从存储设备或网络设备中读取更多代码和数据成为可能。

After the system has bootstrapped itself, the files in the primary BOOTFS become the read-only filesystem tree rooted at `/boot` (and served bybootsvc). 系统自启动后，主BOOTFS中的文件将成为以/ boot为根（并由bootsvc提供）的只读文件系统树。

 
## Kernel loads userboot  内核加载userboot 

The kernel does not include any code for decompressing LZ4 format, nor any code for interpreting the BOOTFS format.  Instead, all of this workis done by the first userspace process, called `userboot`. 内核不包含用于解压缩LZ4格式的任何代码，也不包含用于解释BOOTFS格式的任何代码。相反，所有这些工作都是由第一个用户空间进程（称为“ userboot”）完成的。

`userboot` is a normal userspace process.  It can only make the standard system calls through the [vDSO](/docs/concepts/kernel/vdso.md) like any other process would, andis subject to the full [vDSO enforcement](/docs/concepts/kernel/vdso.md#Enforcement) regime.What's special about `userboot` is the way it gets loaded. `userboot`是一个普通的用户空间进程。它只能像其他任何进程一样通过[vDSO]（/ docs / concepts / kernel / vdso.md）进行标准系统调用，并且要服从完整的[vDSO强制执行]（/ docs / concepts / kernel / vdso。 mdEnforcement）机制。`userboot`的特别之处在于它的加载方式。

`userboot` is built as an ELF dynamic shared object, using the same [RODSO layout](/docs/concepts/kernel/vdso.md#Read_Only-Dynamic-Shared-Object-Layout) asthe vDSO.  Like the vDSO, the `userboot` ELF image is embedded in thekernel at compile time.  Its simple layout means that loading it doesnot require the kernel to interpret ELF headers at boot time.  Thekernel only needs to know three things: the size of the read-onlysegment, the size of the executable segment, and the address of the`userboot` entry point.  At compile time, these values are extractedfrom the `userboot` ELF image and used as constants in the kernel code. 使用与vDSO相同的[RODSO布局]（/ docs / concepts / kernel / vdso.mdRead_Only-Dynamic-Shared-Object-Layout），将“ userboot”构建为ELF动态共享对象。像vDSO一样，`userboot` ELF映像在编译时嵌入内核中。它的简单布局意味着加载它不需要内核在启动时解释ELF头。内核只需要知道三件事：只读段的大小，可执行段的大小以及“ userboot”入口点的地址。在编译时，这些值是从“ userboot” ELF映像中提取的，并用作内核代码中的常量。

Like any other process, `userboot` must start with the vDSO already mapped into its address space so it can make system calls.  The kernelmaps both `userboot` and the vDSO into the first user process, and thenstarts it running at the `userboot` entry point. 像任何其他进程一样，“ userboot”必须从已经映射到其地址空间的vDSO开始，以便可以进行系统调用。内核将“ userboot”和vDSO都映射到第一个用户进程，然后在“ userboot”入口点启动它。

 
## Kernel sends `processargs` message  内核发送`processargs`消息 

In normal [program loading](program_loading.md), a [*bootstrap message*](program_loading.md#the-processargs-protocol) issent to each new process.  The process's first thread receivesa [channel](/docs/concepts/objects/channel.md) handle in a register.  It can then readdata and handles sent by its creator. 在正常的[程序加载]（program_loading.md）中，向每个新进程发送[* bootstrap消息*]（program_loading.mdthe-processargs-protocol）。进程的第一个线程在寄存器中接收[channel]（/ docs / concepts / objects / channel.md）句柄。然后，它可以读取其创建者发送的数据和句柄。

The kernel uses the exact same protocol to start `userboot`.  The kernel command line is split into words that become the environment strings in thebootstrap message.  All the handles that `userboot` itself will need, andthat the rest of the system will need to access kernel facilities, areincluded in this message.  Following the normal format, *handle infoentries* describe the purpose of each handle.  These includethe [`PA_VMO_VDSO` handle](/docs/concepts/kernel/vdso.md#pa_vmo_vdso-handle). 内核使用完全相同的协议来启动“ userboot”。内核命令行被拆分为单词，这些单词成为引导消息中的环境字符串。该消息中包含“ userboot”本身将需要的所有句柄以及系统其余部分将需要访问内核功能的所有句柄。按照句柄格式，* handle infoentries *描述每个句柄的用途。这些包括[`PA_VMO_VDSO`句柄]（/ docs / concepts / kernel / vdso.mdpa_vmo_vdso-handle）。

 
## userboot finds system calls in the vDSO  userboot在vDSO中查找系统调用 

The [standard convention](/docs/concepts/kernel/vdso.md#process_start_argument) for informing a new process of its vDSO mapping requires the process to interpret thevDSO's ELF headers and symbol table to locate system call entry points.To avoid this complexity, `userboot` finds the entry points in the vDSOin a different way. 用于通知vDSO映射新过程的[标准约定]（/ docs / concepts / kernel / vdso.mdprocess_start_argument）要求该过程解释vDSO的ELF头和符号表以定位系统调用入口点。为避免这种复杂性， userboot`以不同的方式在vDSO中找到入口点。

When the kernel maps `userboot` into the first user process, it chooses a random location in memory, just as normal program loading does.However, when it maps the vDSO in it doesn't choose another randomlocation as is normal.  Instead, it places the vDSO image immediatelyafter the `userboot` image in memory.  This way, the vDSO code is alwaysat fixed offsets from the `userboot` code. 当内核将userboot映射到第一个用户进程时，它会像正常加载程序一样在内存中选择一个随机位置。但是，当将vDSO映射到其中时，它不会像平常那样选择另一个随机位置。而是将vDSO映像放置在内存中的“ userboot”映像之后。这样，vDSO代码始终与“ userboot”代码保持固定的偏移量。

At compile time, the symbol table entries for all the system call entry points are extracted from the vDSO ELF image.  These are then massagedinto linker script symbol definitions that use each symbol's fixedoffset into the vDSO image to define that symbol at that fixed offsetfrom the linker-provided `_end` symbol.  In this way, the `userboot`code can make direct calls to each vDSO entry point in the exactlocation it will appear in memory after the `userboot` image itself. 在编译时，将从vDSO ELF映像中提取所有系统调用入口点的符号表入口。然后，这些是Massagedinto链接程序脚本符号定义，使用每个符号的fixedoffset到vDSO映像中，以与链接器提供的_end符号的固定偏移量定义该符号。这样，`userboot`代码可以直接调用每个vDSO入口点的确切位置，该位置将出现在`userboot`映像本身之后的内存中。

 
## userboot decompresses BOOTFS  userboot解压BOOTFS 

The first thing `userboot` does is to read the bootstrap message sent by the kernel.  Among the handles it gets from the kernel is one with*handle info entry* `PA_HND(PA_VMO_BOOTDATA, 0)`.  This isa [VMO](/docs/concepts/objects/vm_object.md) containing the ZBI from theboot loader.  `userboot` reads the ZBI headers from this VMOlooking for the first item with type `ZBI_TYPE_STORAGE_BOOTFS`.  Thatcontains the [BOOTFS](#BOOTFS) image.  The item's ZBI headerindicates if it's compressed, which it usually is.  `userboot` maps inthis portion of the VMO.  `userboot` contains LZ4 format support code,which it uses to decompress the item into a fresh VMO. userboot的第一件事是读取内核发送的引导消息。它从内核获取的句柄中有一个带有* handle info entry *`PA_HND（PA_VMO_BOOTDATA，0）`。这是一个[VMO]（/ docs / concepts / objects / vm_object.md），其中包含来自引导加载程序的ZBI。 `userboot`从该VMO中读取ZBI标头，以查找类型为“ ZBI_TYPE_STORAGE_BOOTFS”的第一项。包含[BOOTFS]（BOOTFS）图像。该项目的ZBI标头指示其是否已压缩（通常是压缩的）。 `userboot`映射VMO的此部分。 “ userboot”包含LZ4格式的支持代码，用于将项目解压缩为新的VMO。

 
## userboot loads the first "real" user process from BOOTFS  userboot从BOOTFS加载第一个“真实”用户进程 

Next, `userboot` examines the environment strings it received from the kernel, which represent the kernel command line.  If there is a string`userboot=`*file* then *file* will be loaded as the first real userprocess.  If no such option is present, the default *file* is `bin/bootsvc`.The files are found in the BOOTFS image. 接下来，`userboot`检查它从内核接收的环境字符串，它们代表内核命令行。如果有一个字符串`userboot =`* file *，那么* file *将被加载为第一个实际的用户进程。如果不存在这样的选项，则默认* file *为`bin / bootsvc`。这些文件位于BOOTFS映像中。

To load the file, `userboot` implements a full-featured ELF program loader. Usually the file being loaded is a dynamically-linked executable with a`PT_INTERP` program header.  In this case, `userboot` looks for the filenamed in `PT_INTERP` and loads that instead. 为了加载文件，`userboot`实现了一个功能齐全的ELF程序加载器。通常，正在加载的文件是带有程序头的PT_INTERP动态链接的可执行文件。在这种情况下，“ userboot”会在“ PT_INTERP”中查找文件名，然后加载该文件名。

Then `userboot` loads the vDSO at a random address.  It starts the new process with the standard conventions, passing it a channel handle and thevDSO base address.  On that channel, `userboot` sends thestandard [`processargs`](program_loading.md#the-processargs-protocol)messages.  It passes on all the important handles it received from thekernel (replacing specific handles such as the process-self and thread-selfhandles with those for the new process rather than for `userboot` itself). 然后`userboot`将vDSO加载到一个随机地址。它以标准约定开始新过程，并向其传递通道句柄和vDSO基址。在该通道上，`userboot`发送标准的[`processargs`]（program_loading.mdthe-processargs-protocol）消息。它传递了从内核接收到的所有重要句柄（将进程自身和线程自身的句柄之类的特定句柄替换为新进程的句柄，而不是“ userboot”本身）。

 
## userboot loader service  userboot loader服务 

Following the standard program loading protocol, when `userboot` loads a program via `PT_INTERP`, it sends an additional `processargs` messagebefore the main message, intended for the use of the dynamic linker.  Thismessage includes a `PA_LDSVC_LOADER` handle for a channel on which `userboot`provides a minimal implementation of thestandard [loader service](program_loading.md#the-loader-service). 按照标准程序加载协议，当userboot通过PT_INTERP加载程序时，它将在主消息之前发送一条附加的processargs消息，以供动态链接器使用。该消息包括一个通道的“ PA_LDSVC_LOADER”句柄，在该通道上，“ userboot”提供了对标准[loader service]（program_loading.mdthe-loader-service）的最小实现。

`userboot` has only a single thread, which remains in a loop handling loader service requests until the channel is closed.  When it receives a`LOADER_SVC_OP_LOAD_OBJECT` request, it looks up the object name prefixedby `lib/` as a file in BOOTFS and returns a VMO of its contents.  Thus, thefirst "real" user process can be (and usually is) a dynamically linkedexecutable needing various shared libraries.  The dynamic linker, theexecutable, and the shared libraries are all loaded from the same BOOTFSpages that will later appear as files in `/boot`. “ userboot”只有一个线程，该线程将一直循环处理加载程序服务请求，直到关闭通道为止。当它收到“ LOADER_SVC_OP_LOAD_OBJECT”请求时，它将在BOOTFS中查找以“ lib /”为前缀的对象名称作为文件，并返回其内容的VMO。因此，第一个“真实”用户进程可以是（通常是）动态链接的可执行文件，需要各种共享库。动态链接器，可执行文件和共享库均从相同的BOOTFS页面加载，这些页面随后将在文件中显示为/ boot。

An executable that will be loaded by `userboot` (i.e. [`bootsvc`](bootsvc.md)) should normally close its loader service channel once it's completed startup.That lets `userboot` know that it's no longer needed. 通常，一旦完成启动，将由userboot加载的可执行文件（即[bootsvc]（bootsvc.md））应关闭其加载程序服务通道。这使`userboot`不再需要它。

 
## userboot rides off into the sunset  userboot进入日落 

When the loader service channel is closed (or if the executable had no `PT_INTERP` and so no loader service was required, then as soon as theprocess has been started), `userboot` no longer has anything to do. 当关闭加载程序服务通道时（或者如果可执行文件没有`PT_INTERP`，因此不需要加载程序服务，则在进程启动后立即运行），`userboot'不再需要执行任何操作。

If [the `userboot.shutdown` option was given on the kernel command line](/docs/reference/kernel/kernel_cmdline.md#userboot-shutdown), then `userboot` waits for the process it started to exit, and then shutsdown the system (as if by the `dm shutdown` command).  This can be usefulto run a single test program and then shut down the machine (or emulator).For example, the command line `userboot=bin/core-tests userboot.shutdown`runs the Zircon core tests and then shuts down. 如果[内核命令行上给出了`userboot.shutdown`选项]（/ docs / reference / kernel / kernel_cmdline.mduserboot-shutdown），则`userboot`等待它开始退出的过程，然后关闭系统。 （就像通过`dm shutdown`命令一样）。这对于运行单个测试程序然后关闭机器（或仿真器）很有用。例如，命令行“ userboot = bin / core-tests userboot.shutdown”运行Zircon核心测试，然后关闭。

