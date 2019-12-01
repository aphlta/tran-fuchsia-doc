 
# Zircon vDSO  锆石vDSO 

The Zircon vDSO is the sole means of access to [system calls](/docs/reference/syscalls/README.md)in Zircon. vDSO stands for *virtual Dynamic Shared Object*. (*DynamicShared Object* is a term used for a shared library in the ELF format.)It's *virtual* because it's not loaded from an ELF file that sits in afilesystem. Instead, the vDSO image is provided directly by the kernel. Zircon vDSO是访问Zircon中[系统调用]（/ docs / reference / syscalls / README.md）的唯一方法。 vDSO代表*虚拟动态共享对象*。 （* DynamicShared Object *是用于ELF格式的共享库的术语。）它是* virtual *，因为它不是从文件系统中的ELF文件加载的。而是由内核直接提供vDSO映像。

[TOC]  [目录]

 
## Using the vDSO  使用vDSO 

 
### System Call ABI  系统调用ABI 

The vDSO is a shared library in the ELF format. It's used in the normal way that ELF shared libraries are used, which is to look up entry points bysymbol name in the ELF *dynamic symbol table* (the `.dynsym` section,located via `DT_SYMTAB`). ELF defines a hash table format to optimizelookup by name in the symbol table (the `.hash` section, located via`DT_HASH`); GNU tools have defined an improved hash table format that makeslookups much more efficient (the `.gnu_hash` section, located via`DT_GNU_HASH`). Fuchsia ELF shared libraries, including the vDSO, use the`DT_GNU_HASH` format exclusively. (It's also possible to use the symboltable directly via linear search, ignoring the hash table.) vDSO是ELF格式的共享库。它以通常使用ELF共享库的方式使用，即在ELF *动态符号表*（。dynsym`部分，通过`DT_SYMTAB`定位）中通过符号名称查找入口点。 ELF定义了一种哈希表格式，以通过符号表中的名称优化查找（.hash节，通过DT_HASH定位）； GNU工具定义了一种改进的哈希表格式，使查找效率更高（.gnu_hash节，可通过DT_GNU_HASH定位）。紫红色ELF共享库（包括vDSO）仅使用DT_GNU_HASH格式。 （也可以通过线性搜索直接使用symboltable，而忽略哈希表。）

The vDSO uses a [simplified layout](#Read_Only-Dynamic-Shared-Object-Layout) that has no writable segment and requires no dynamic relocations. Thismakes it easier to use the system call ABI without implementing ageneral-purpose ELF loader and full ELF dynamic linking semantics. vDSO使用没有可写段且不需要动态重定位的[简化布局]（Read_Only-Dynamic-Shared-Object-Layout）。这使得在不实现通用ELF加载程序和完整ELF动态链接语义的情况下，更易于使用系统调用ABI。

ELF symbol names are the same as C identifiers with external linkage. Each [system call](/docs/reference/syscalls/README.md) corresponds to an ELF symbol in the vDSO,and has the ABI of a C function. The vDSO functions use only the basicmachine-specific C calling conventions governing the use of machineregisters and the stack, which is common across many systems that use ELF,such as Linux and all the BSD variants. They do not rely on complexfeatures such as ELF Thread-Local Storage, nor on Fuchsia-specific ABIelements such as the [SafeStack](/docs/concepts/kernel/safestack.md) unsafe stack pointer. ELF符号名称与具有外部链接的C标识符相同。每个[系统调用]（/ docs / reference / syscalls / README.md）对应于vDSO中的ELF符号，并具有C函数的ABI。 vDSO函数仅使用基本的特定于机器的C调用约定来控制机器寄存器和堆栈的使用，这在使用ELF的许多系统（例如Linux和所有BSD变体）中是常见的。它们不依赖于诸如ELF线程本地存储之类的复杂功能，也不依赖于特定于紫红色的ABIelements，例如[SafeStack]（/ docs / concepts / kernel / safestack.md）不安全的堆栈指针。

 
### vDSO Unwind Information  vDSO展开信息 

The vDSO has an ELF program header of type `PT_GNU_EH_FRAME`. This points to unwind information in the GNU `.eh_frame` format, which is a closerelative of the standard DWARF Call Frame Information format. Thisinformation makes it possible to recover the register values from callframes in the vDSO code, so that a complete stack trace can be reconstructedfrom any thread's register state with a PC value inside the vDSO code.These formats and their use are just the same in the vDSO as they are in anynormal ELF shared library on Fuchsia or other systems using common GNU ELFextensions, such as Linux and all the BSD variants. vDSO具有类型为“ PT_GNU_EH_FRAME”的ELF程序标头。这指向以GNU`.eh_frame`格式展开信息，该格式与标准DWARF调用帧信息格式有关。该信息使得可以从vDSO代码中的调用帧中恢复寄存器值，从而可以从任何线程的寄存器状态（在vDSO代码中包含PC值）重建完整的堆栈跟踪。这些格式及其用法在vDSO中是相同的就像它们在Fuchsia或使用通用GNU ELF扩展的其他系统上的任何普通ELF共享库中一样，例如Linux和所有BSD变体。

 
### vDSO Build ID  vDSO内部版本ID 

The vDSO has an ELF *Build ID*, as other ELF shared libraries and executables built with common GNU extensions do. The Build ID is a uniquebit string that identifies a specific build of that binary. This is storedin ELF note format, pointed to by an ELF program header of type `PT_NOTE`.The payload of the note with name `"GNU"` and type `NT_GNU_BUILD_ID` is asequence of bytes that constitutes the Build ID. vDSO与其他ELF共享库和使用通用GNU扩展构建的可执行文件一样，具有ELF * Build ID *。内部版本ID是一个uniquebit字符串，用于标识该二进制文件的特定内部版本。它以ELF注释格式存储，由类型为PT_NOTE的ELF程序标头指向。名称为“ GNU”且类型为NT_GNU_BUILD_ID的注释的有效载荷是构成构建ID的字节顺序。

One main use of Build IDs is to associate binaries with their debugging information and the source code they were built from. The vDSO binary isinnately tied to (and embedded within) the kernel binary and includesinformation specific to each kernel build, so the Build ID of the vDSOdistinguishes kernels as well. 构建ID的主要用途之一是将二进制文件与其调试信息和构建它们的源代码相关联。 vDSO二进制文件与内核二进制文件有先天的联系（并嵌入在其中），并且包含特定于每个内核构建的信息，因此vDSO的Build ID也可以区分内核。

 
### `zx_process_start()` argument  zx_process_start（）参数 

The [`zx_process_start()`] system call is how a program loader tells the kernel to start a new process's first threadexecuting. The final argument (`arg2`in the [`zx_process_start()`] documentation) is aplain `uintptr_t` value passed to the new thread in a register. [`zx_process_start（）]系统调用是程序加载器告诉内核启动新进程的第一个线程执行的方式。最后一个参数（[zx_process_start（）]文档中的“ arg2”）是传递给寄存器中新线程的“ uintptr_t”值。

By convention, the program loader maps the vDSO into each new process's address space (at a random location chosen by the system) and passes thebase address of the image to the new process's first thread in the `arg2`register. This address is where the ELF file header can be found in memory,pointing to all the other ELF format elements necessary to look up symbolnames and thus make system calls. 按照惯例，程序加载器将vDSO映射到每个新进程的地址空间（在系统选择的随机位置），并将映像的基址传递到arg2寄存器中新进程的第一个线程。该地址是可以在内存中找到ELF文件头的位置，它指向查找符号名并进行系统调用所必需的所有其他ELF格式元素。

 
### **PA_VMO_VDSO** handle  ** PA_VMO_VDSO **句柄 

The vDSO image is embedded in the kernel at compile time. The kernel exposes it to userspace as a read-only [VMO](/docs/concepts/objects/vm_object.md). vDSO映像在编译时嵌入到内核中。内核将其作为只读[VMO]（/ docs / concepts / objects / vm_object.md）公开给用户空间。

When a program loader sets up a new process, the only way to make it possible for that process to make system calls is for the program loader tomap the vDSO into the new process's address space before its first threadstarts running. Hence, each process that will launch other processescapable of making system calls must have access to the vDSO VMO. 当程序加载器设置新进程时，使该进程进行系统调用的唯一方法是，在第一个线程开始运行之前，程序加载器将vDSO映射到新进程的地址空间中。因此，将启动能够进行系统调用的其他进程的每个进程都必须有权访问vDSO VMO。

By convention, a VMO handle for the vDSO is passed from process to process in the `zx_proc_args_t` bootstrap message sent to each new process(see [`<zircon/processargs.h>`](/zircon/system/public/zircon/processargs.h)).The VMO handle's entry in the handle table is identified by the *handleinfo entry* `PA_HND(PA_VMO_VDSO, 0)`. 按照惯例，用于vDSO的VMO句柄在发送到每个新进程的`zx_proc_args_t`引导消息中从一个进程传递到另一个进程（请参阅[[zircon / processargs.h>]]（/ zircon / system / public / zircon / VDE句柄表中的条目由* handleinfo条目* PA_HND（PA_VMO_VDSO，0）标识。

 
## vDSO Implementation Details  vDSO实施详细信息 

 
### **kazoo** tool  ** kazoo **工具 

The [`kazoo` tool](/zircon/tools/kazoo/) generates both C/C++ function declarations that form the public [systemcall](/docs/reference/syscalls/README.md) API, and some C++ and assembly codeused in the implementation of the vDSO. Both the public API and the privateinterface between the kernel and the vDSO code are specified by the .fidl filesin [//zircon/syscalls](/zircon/syscalls). [`kazoo`工具]（/ zircon / tools / kazoo /）生成构成公共[systemcall]（/ docs / reference / syscalls / README.md）API的C / C ++函数声明，以及一些已使用的C ++和汇编代码在vDSO的实施中。内核和vDSO代码之间的公共API和私有接口均由[// zircon / syscalls]（/ zircon / syscalls）中的.fidl文件指定。

The syscalls fall into the following groups, distinguished by the presence of attributes after the system call name: syscall分为以下几类，以系统调用名称后的属性的存在来区分：

 
* Entries with neither `vdsocall` nor `internal` are the simple cases (which are the majority of the system calls) where the public API andthe private API are exactly the same. These are implemented entirelyby generated code. The public API functions have names prefixed by`_zx_` and `zx_` (aliases). *不带“ vdsocall”和“ internal”的条目都是简单的情况（占系统调用的大部分），其中公共API和私有API完全相同。这些完全由生成的代码实现。公用API函数的名称以`_zx_`和`zx_`（别名）开头。

 
* `vdsocall` entries are simply declarations for the public API. These functions are implemented by normal, hand-written C++ code found in[`system/ulib/zircon/`](/zircon/system/ulib/zircon/). Those sourcefiles `#include "private.h"` and then define the C++ function for thesystem call with its name prefixed by `_zx_`. Finally, they use the`VDSO_INTERFACE_FUNCTION` macro on the system call's name prefixed by`zx_` (no leading underscore). This implementation code can call theC++ function for any other system call entry (whether a publicgenerated call, a public hand-written `vdsocall`, or an `internal`generated call), but must use its private entry point alias, which hasthe `VDSO_zx_` prefix. Otherwise the code is normal (minimal) C++, butmust be stateless and reentrant (use only its stack and registers). *`vdsocall`条目只是公共API的声明。这些功能由在[`system / ulib / zircon /`]（/ zircon / system / ulib / zircon /）中找到的普通手写C ++代码实现。这些源文件包含“ private.h”，然后为系统调用定义C ++函数，其名称以`_zx_'为前缀。最后，他们在系统调用名称上以`zx_`为前缀使用`VDSO_INTERFACE_FUNCTION`宏（不带下划线）。该实现代码可以为任何其他系统调用条目（无论是公共生成的调用，公共手写的“ vdsocall”还是“内部”生成的调用）调用C ++函数，但是必须使用其私有入口点别名，该别名具有“ VDSO_zx_”。 `前缀。否则，代码将是普通的（最小）C ++，但必须是无状态的且可重入的（仅使用其堆栈和寄存器）。

 
* `internal` entries are declarations of a private API used only by the vDSO implementation code to enter the kernel (i.e., by other functionsimplementing `vdsocall` system calls). These produce functions in thevDSO implementation with the same C signature that would be declaredin the public API given the signature of the system call entry.However, instead of being named with the `_zx_` and `zx_` prefixes,these are only available through `#include "private.h"` with`VDSO_zx_` prefixes. *内部条目是私有API的声明，仅由vDSO实现代码用于进入内核（即，通过实现vdsocall系统调用的其他函数）。这些在vDSO实现中产生具有相同C签名的函数，这些签名将在给定系统调用条目的签名的情况下在公共API中声明。但是，这些前缀不是通过`_zx_`和`zx_`前缀来命名，而是只能通过`包括带有“ VDSO_zx_”前缀的“ private.h”。

 
### Read-Only Dynamic Shared Object Layout  只读动态共享对象布局 

The vDSO is a normal ELF shared library and can be treated like any other. But it's intentionally kept to a small subset of what an ELFshared library in general is allowed to do. This has several benefits: vDSO是普通的ELF共享库，可以像对待其他任何库一样对待。但有意将其保留为允许一般ELFshared库执行的操作的一小部分。这有几个好处：

 
 * Mapping the ELF image into a process is straightforward and does not involve any complex corner cases of general support for ELF `PT_LOAD`program headers. The vDSO's layout can be handled by special-casecode with no loops that reads only a few values from ELF headers. *将ELF映像映射到一个过程很简单，并且不涉及一般支持ELF`PT_LOAD`程序头的任何复杂情况。 vDSO的布局可以由特殊情况的代码处理，没有循环，该循环仅从ELF标头读取一些值。
 * Using the vDSO does not require full-featured ELF dynamic linking. In particular, the vDSO has no dynamic relocations. Mapping in theELF `PT_LOAD` segments is the only setup that needs to be done. *使用vDSO不需要全功能的ELF动态链接。特别是，vDSO没有动态重定位。在ELF`PT_LOAD`段中的映射是唯一需要完成的设置。
 * The vDSO code is stateless and reentrant. It refers only to the registers and stack with which it's called. This makes it usable ina wide variety of contexts with minimal constraints on how user codeorganizes itself, which is appropriate for the mandatory ABI of anoperating system. It also makes the code easier to reason about andaudit for robustness and security. * vDSO代码是无状态且可重入的。它仅指调用它的寄存器和堆栈。这使得它可以在各种上下文中使用，并且对用户代码组织方式的限制极小，这适用于操作系统的强制性ABI。这也使代码更易于推理和审核健壮性和安全性。

The layout is simply two consecutive segments, each containing aligned whole pages: 布局只是两个连续的段，每个段包含对齐的整个页面：

 
 1. The first segment is read-only, and includes the ELF headers and metadata for dynamic linking along with constant data private to thevDSO's implementation. 1.第一部分是只读的，包括用于动态链接的ELF标头和元数据以及vDSO实施专用的常量数据。
 2. The second segment is executable, containing the vDSO code.  2.第二段是可执行的，包含vDSO代码。

The whole vDSO image consists of just these two segments' pages, present in the ELF image just as they should appear in memory. To map in thevDSO requires only two values gleaned from the vDSO's ELF headers: thenumber of pages in each segment. 整个vDSO映像仅由这两个段的页面组成，它们在ELF映像中的显示方式与它们在内存中的显示方式相同。要在vDSO中进行映射，仅需要从vDSO的ELF标头中收集两个值：每个段中的页数。

 
### Boot-time Read-Only Data  引导时只读数据 

Some system calls simply return values that are constant throughout the runtime of the whole system, though the ABI of the system is that theirvalues must be queried at runtime and cannot be compiled into user code.These values either are fixed in the kernel at compile time or aredetermined by the kernel at boot time from hardware or boot parameters.Examples include [`zx_system_get_version()`],[`zx_system_get_num_cpus()`], and [`zx_ticks_per_second()`]. 尽管系统的ABI要求必须在运行时查询它们的值并且不能将其编译为用户代码，但某些系统调用只是返回在整个系统运行时恒定的值，这些值在编译时已在内核中固定或由内核在启动时根据硬件或启动参数确定。示例包括[`zx_system_get_version（）`]，[`zx_system_get_num_cpus（）]和[`zx_ticks_per_second（）]。

Because these values are constant, there is no need to pay the overhead of entering the kernel to read them. Instead, the vDSO implementationsof these are simple C++ functions that just return constants read fromthe vDSO's read-only data segment. Values fixed at compile time (such asthe system version string) are simply compiled into the vDSO. 由于这些值是恒定的，因此无需支付进入内核以读取它们的开销。相反，这些的vDSO实现是简单的C ++函数，它们仅返回从vDSO的只读数据段读取的常量。编译时固定的值（例如系统版本字符串）可以简单地编译到vDSO中。

For the values determined at boot time, the kernel must modify the contents of the vDSO. This is accomplished by the boot-time code thatsets up the vDSO VMO, before it starts the first userspace process andgives it the VMO handle. At compile time, the offset into the vDSO imageof the[`vdso_constants`](/zircon/kernel/lib/userabi/include/lib/userabi/vdso-constants.h)data structure is extracted from the vDSO ELF file that will be embeddedin the kernel. At boot time, the kernel temporarily maps the pages ofthe VMO covering `vdso_constants` into its own address space long enoughto initialize the structure with the right values for the current run ofthe system. 对于引导时确定的值，内核必须修改vDSO的内容。这是通过在启动第一个用户空间进程并将其交给VMO句柄之前，设置vDSO VMO的启动时代码来完成的。在编译时，[vdso_constants]]（/ zircon / kernel / lib / userabi / include / lib / userabi / vdso-constants.h）数据结构在vDSO映像中的偏移量将从vDSO ELF文件中提取。嵌入内核。在启动时，内核将足以覆盖“ vdso_constants”的VMO页面临时映射到其自身的地址空间中，时间足够长，可以使用当前系统运行的正确值来初始化结构。

 
### Enforcement  执法 

The vDSO entry points are the only means to enter the kernel for system calls. The machine-specific instructions used to enter the kernel (e.g.`syscall` on x86) are not part of the system ABI and it's invalid foruser code to execute such instructions directly. The interface betweenthe kernel and the vDSO code is a private implementation detail. vDSO入口点是进入内核进行系统调用的唯一方法。用于输入内核的机器特定指令（例如x86上的syscall）不是系统ABI的一部分，对于用户代码而言，直接执行此类指令无效。内核和vDSO代码之间的接口是私有的实现细节。

Because the vDSO is itself normal code that executes in userspace, the kernel must robustly handle all possible entries into kernel mode fromuserspace. However, potential kernel bugs can be mitigated somewhat byenforcing that each kernel entry be made only from the proper vDSO code.This enforcement also avoids developers of userspace code circumventingthe ABI rules (because of ignorance, malice, or misguided intent to workaround some perceived limitation of the official ABI), which could leadto the private kernel-vDSO interface becoming a *de facto* ABI forapplication code. 因为vDSO本身是在用户空间中执行的普通代码，所以内核必须健壮地处理所有可能从用户空间进入内核模式的条目。但是，通过强制每个内核条目只能通过正确的vDSO代码进行操作，可以在某种程度上缓解潜在的内核错误。这种执行方式还可以避免用户空间代码的开发人员规避ABI规则（由于无知，恶意或错误的意图来解决某些可感知的限制）官方ABI），这可能导致专用内核-vDSO接口成为应用程序代码的*事实上* ABI。

The kernel enforces correct use of the vDSO in two ways:  内核通过两种方式来强制正确使用vDSO：

 
 1. It constrains how the vDSO VMO can be mapped into a process.  1.它限制了如何将vDSO VMO映射到流程中。

    When a [`zx_vmar_map()`] call is made using the vDSO VMO and requesting `ZX_VM_PERM_EXECUTE`, the kernel requires that the offsetand size of the mapping exactly match the vDSO's executable segment.It also allows only one such mapping. Once the valid vDSO mappinghas been established in a process, it cannot be removed. Attempts tomap the vDSO a second time into the same process, to unmap the vDSOcode from a process, or to make an executable mapping of the vDSOthat don't use the correct offset and size, fail with`ZX_ERR_ACCESS_DENIED`. 当使用vDSO VMO调用[`zx_vmar_map（）]并请求`ZX_VM_PERM_EXECUTE`时，内核要求映射的偏移量和大小与vDSO的可执行段完全匹配。它也只允许一个这样的映射。一旦在过程中建立了有效的vDSO映射，就无法将其删除。尝试再次将vDSO映射到同一进程中，从进程中取消映射vDSOcode或对未使用正确偏移量和大小的vDSO进行可执行映射，都将失败，并显示ZX_ERR_ACCESS_DENIED。

    At compile time, the offset and size of the vDSO's code segment are extracted from the vDSO ELF file and used as constants in thekernel's mapping enforcement code. 在编译时，将从vDSO ELF文件中提取vDSO代码段的偏移量和大小，并将其用作内核映射实施代码中的常量。

    When the one valid vDSO mapping is established in a process, the kernel records the address for that process so it can be checkedquickly. 在一个进程中建立一个有效的vDSO映射后，内核会记录该进程的地址，以便可以对其进行快速检查。

 
 2. It constrains what PC locations can be used to enter the kernel.  2.它限制了可用于进入内核的PC位置。

    When a user thread enters the kernel for a system call, a register indicates which low-level system call is being invoked. Thelow-level system calls are the private interface between the kerneland the vDSO; many correspond directly the system calls in thepublic ABI, but others do not. 当用户线程进入内核进行系统调用时，寄存器指示正在调用哪个低级系统调用。底层系统调用是内核与vDSO之间的专用接口。许多直接对应于公共ABI中的系统调用，而其他人则没有。

    For each low-level system call, there is a fixed set of PC locations in the vDSO code that invoke that call. The source code for the vDSOdefines internal symbols identifying each such location. At compiletime, these locations are extracted from the vDSO's symbol table andused to generate kernel code that defines a PC validity predicatefor each low-level system call. Since there is only one definitionof the vDSO code used by all user processes in the system, thesepredicates simply check for known, valid, constant offsets from thebeginning of the vDSO code segment. 对于每个低级系统调用，在vDSO代码中都有一组固定的PC位置来调用该调用。 vDSO的源代码定义标识每个此类位置的内部符号。在编译时，将从vDSO的符号表中提取这些位置，并用于生成内核代码，该内核代码为每个低级系统调用定义PC有效性谓词。由于系统中所有用户进程使用的vDSO代码只有一个定义，因此这些谓词仅从vDSO代码段的开头检查已知，有效，恒定的偏移量。

    On entry to the kernel for a system call, the kernel examines the PC location of the `syscall` instruction on x86 (or equivalentinstruction on other machines). It subtracts the base address of thevDSO code recorded for the process at [`zx_vmar_map()`] time fromthe PC, and passes the resulting offset to the validity predicatefor the system call being invoked. If the predicate rules the PCinvalid, the calling thread is not allowed to proceed with thesystem call and instead takes a synthetic exception similar to themachine exception that would result from invoking an undefined orprivileged machine instruction. 在进入内核进行系统调用时，内核会检查x86（或其他计算机上的等效指令）上syscall指令的PC位置。它从PC减去[zx_vmar_map（）]时在该过程中记录的vDSO代码的基地址，然后将所得偏移量传递给正在调用的系统调用的有效性谓词。如果谓词使PCinvalid无效，则不允许调用线程继续进行系统调用，而是采用类似于计算机异常的综合异常，该异常是由调用未定义或特权的机器指令而导致的。

 
### Variants  变体 

**TODO(mcgrathr)**: vDSO *variants* are an experimental feature that is not yet in real use. There is a proof-of-concept implementation andsimple tests, but more work is required to implement the conceptrobustly and determine what variants will be made available. The conceptis to provide variants of the vDSO image that export only a subset ofthe full vDSO system call interface. For example, system calls intendedonly for use by device drivers might be elided from the vDSO variantused for normal application code. ** TODO（mcgrathr）**：vDSO *变体*是一项实验性功能，尚未真正使用。有概念验证的实现和简单的测试，但是要稳健地实现该概念并确定将提供哪些变体，还需要做更多的工作。该概念旨在提供仅导出完整vDSO系统调用接口的子集的vDSO映像的变体。例如，可能仅用于设备驱动程序的系统调用会从用于常规应用程序代码的vDSO变体中消失。

