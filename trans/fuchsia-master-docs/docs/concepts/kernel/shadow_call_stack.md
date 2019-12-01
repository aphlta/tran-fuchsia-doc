 
# ShadowCallStack in Zircon & Fuchsia  Zircon紫红色的ShadowCallStack 

[TOC]  [目录]

 
## Introduction  介绍 

LLVM's [shadow-call-stack feature][shadow-call-stack] is a compiler mode intended to harden the generated code against stack-smashing attacks such asexploits of buffer overrun bugs. LLVM的[shadow-call-stack功能] [shadow-call-stack]是一种编译器模式，旨在增强生成的代码，以防止诸如缓冲区溢出错误的漏洞之类的堆栈破坏攻击。

The Clang/LLVM documentation page linked above describes the scheme.  The capsule summary is that the function return address is never reloaded from thenormal stack but only from a separate "shadow call stack".  This is anadditional stack, but rather than containing whole stack frames of whateversize each function needs, it contains only a single address word for each callframe it records: just the return address.  Since the shadow call stack isallocated independently of other stacks or heap blocks with its own randomizedaddress to which pointers are rare, it is much less likely that some sort ofbuffer overrun or use-after-free exploit will overwrite a return address inmemory so that it can cause the program to return to an instruction by theattacker. 上面链接的Clang / LLVM文档页面介绍了该方案。封装摘要是，函数返回地址从不从正常堆栈中重新加载，而仅从单独的“影子调用堆栈”中重新加载。这是一个附加的堆栈，但是它没有包含每个函数需要的任何大小的整个堆栈框架，而是针对它记录的每个调用框架仅包含一个地址字：只是返回地址。由于影子调用堆栈是通过其自身的随机地址独立于其他堆栈或堆块而分配的，而指针的随机化地址很少，因此某种缓冲区溢出或释放后使用漏洞会覆盖返回地址内存的可能性很小，因此它可以使程序返回到攻击者的指令。

The [shadow-call-stack] and [safe-stack] instrumentation schemes and ABIs are related and similar but also orthogonal.  Each can be enabled or disabledindependently for any function.  Fuchsia's compiler ABI and libc alwaysinteroperate with code built with or without either kind of instrumentation,regardless of what instrumentation was or wasn't used in the particular libcbuild. [影子呼叫堆栈]和[安全堆栈]检测方案和ABI是相关且相似的，但也是正交的。每种功能均可独立启用或禁用。紫红色的编译器ABI和libc始终可以与使用或不使用任何一种工具建立的代码进行互操作，而不管特定的libcbuild中使用或不使用什么工具。

[shadow-call-stack]: https://clang.llvm.org/docs/ShadowCallStack.html [safe-stack]: safestack.md [shadow-call-stack]：https://clang.llvm.org/docs/ShadowCallStack.html [safe-stack]：safestack.md

 
## Interoperation and ABI Effects  互操作和ABI效应 

In general, shadow-call-stack does not affect the ABI.  The machine-specific calling conventions are unchanged.  It works fine to have some functions in aprogram built with shadow-call-stack and some not.  It doesn't matter ifcombining the two comes from directly compiled `.o` files, from archivelibraries (`.a` files), or from shared libraries (`.so` files), in anycombination. 通常，影子调用堆栈不会影响ABI。特定于计算机的调用约定不变。在使用影子调用堆栈构建的程序中具有某些功能而没有某些功能，效果很好。无论是来自直接编译的.o文件，来自存档库（.a文件）还是来自共享库（.so文件）（以任何组合），两者都是没有关系的。

While there is some additional per-thread state (the *shadow call stack pointer*, [see below](#implementation-details)), code not usingshadow-call-stack does not need to do anything about this state to keep itcorrect when calling, or being called by, code that does use safe-stack.  Theonly potential exceptions to this are for code that is implementing its ownkinds of non-local exits or context-switching (e.g. coroutines).  The Zircon Clibrary's `setjmp`/`longjmp` code saves and restores this additional stateautomatically, so anything that is based on `longjmp` already handles everythingcorrectly even if the code calling `setjmp` and `longjmp` doesn't know aboutshadow-call-stack. 虽然还有一些其他的每线程状态（* shadow调用堆栈指针*，[请参见下文]（实现细节）），但未使用shadow-call-stack的代码无需对此状态进行任何操作即可在调用时保持其正确性或由使用安全堆栈的代码调用。唯一可能的例外是正在实现自己的非本地出口或上下文切换（例如协程）类型的代码。 Zircon Clibrary的`setjmp` /`longjmp`代码会自动保存并恢复此附加状态，因此即使调用`setjmp`和`longjmp`的代码不了解影子调用，基于`longjmp`的任何内容也已能够正确处理所有内容。堆。

For AArch64 (ARM64), the `x18` register is already reserved as "fixed" in the ABI generally.  Code unaware of the shadow-call-stack extension to the ABI isinteroperable with the shadow-call-stack ABI by default if it simply nevertouches `x18`. 对于AArch64（ARM64），`x18`寄存器通常已经在ABI中保留为“固定”。如果没有注意到ABI的影子调用堆栈扩展的代码，如果它根本不接触x18，则默认情况下可以与影子调用堆栈ABI互操作。

The feature is not yet supported on any other architecture.  其他任何体系结构尚不支持该功能。

 
## Use in Zircon & Fuchsia  在锆石紫红色中使用 

This is enabled in the Clang compiler by the `-fsanitize=shadow-call-stack` command-line option.  **TODO(27339)**: When the support is fully tested andthe ABI finalized for each machine, this will become the default mode of thecompiler for `*-fuchsia` targets.  To disable it for a specific compilation,use the `-fno-sanitize=shadow-call-stack` option. 在Clang编译器中，通过`-fsanitize = shadow-call-stack`命令行选项启用了此功能。 ** TODO（27339）**：当对支持进行了全面测试并针对每台机器最终确定了ABI后，这将成为**紫红色目标的编译器的默认模式。要禁用它以进行特定的编译，请使用-fno-sanitize = shadow-call-stack选项。

Zircon supports shadow-call-stack both in the kernel and for user-mode code. For AArch64 (ARM64) shadow-call-stack is now on by default for all C and C++user code in the Fuchsia build (including Zircon).  **TODO(27339)**: Code builtoutside the Fuchsia/Zircon GN build system still requires explicitly adding the`-fsanitize=shadow-call-stack` switch. Zircon在内核和用户模式代码中都支持影子调用堆栈。对于AArch64（ARM64），对于Fuchsia版本（包括Zircon）中的所有C和C ++用户代码，默认情况下，影子调用堆栈已打开。 ** TODO（27339）**：在Fuchsia / Zircon GN构建系统之外构建的代码仍然需要显式添加`-fsanitize = shadow-call-stack`开关。

As with [safe-stack], there is no separate facility for specifying the size of the shadow call stack.  Instead, the size specified for "the stack" in legacyAPIs (such as `pthread_attr_setstacksize`) and ABIs (such as `PT_GNU_STACK`) isused as the size for **each** kind of stack.  Because the different kinds ofstack are used in different proportions according to the particular programbehavior, there is no good way to choose the shadow call stack size based onthe traditional single stack size.  So each kind of stack is as big as it mightneed to be in the worst case expected by the tuned "unitary" stack size.  Whilethis seems wasteful, it is only slightly so: at worst one page is wasted perkind of stack, plus the page table overhead of using more address space forpages that are never accessed. 与[safe-stack]一样，没有单独的工具来指定影子调用堆栈的大小。相反，在legacyAPI（例如“ pthread_attr_setstacksize”）和ABI（例如“ PT_GNU_STACK”）中为“堆栈”指定的大小用作“每种”堆栈的大小。因为根据特定的程序行为，不同种类的堆栈使用的比例不同，所以没有很好的方法根据传统的单个堆栈大小来选择影子调用堆栈大小。因此，每种堆栈的大小都可能与调整后的“单一”堆栈大小所预期的最坏情况一样大。尽管这看起来很浪费，但它只是一点点：最糟糕的是，一页浪费在堆栈上，这实在是太浪费了，再加上使用更多地址空间访问从未访问过的页面的页表开销。

 
## Implementation details  实施细节 

The essential addition to support shadow-call-stack code is the *shadow call stack pointer*.  This is a register with a global use, like the traditionalstack pointer.  But each call frame pushes and pops a single return addressword rather than arbitrary data as in the normal stack frame. 支持影子调用堆栈代码的基本补充是“影子调用堆栈指针”。这是一个具有全局用途的寄存器，就像传统堆栈指针一样。但是每个调用帧都会推送并弹出单个返回地址字，而不是像正常堆栈帧中那样弹出任意数据。

For AArch64 (ARM64), the `x18` register holds the shadow call stack pointer at function entry.  The shadow call stack grows upwards with post-incrementsemantics, so `x18` always points to the next free slot.  The compiler nevertouches the register except to spill and reload the return address register(`x30`, aka LR).  The Fuchsia ABI requires that `x18` contain a valid shadowstack pointer at all times.  That is, it must **always** be valid to push anew address onto the shadow call stack at `x18` (modulo stack overflow). 对于AArch64（ARM64），`x18`寄存器将影子调用堆栈指针保存在函数入口处。影子调用栈随着后递增语义而向上增长，因此x18始终指向下一个空闲插槽。编译器从不触碰寄存器，除非溢出并重新加载返回地址寄存器（`x30`，又称LR）。紫红色ABI要求`x18'始终都包含有效的shadowstack指针。也就是说，必须始终有效，才能将新地址推入x18处的影子调用堆栈（模堆栈溢出）。

 
### Notes for low-level and assembly code  低级和汇编代码的注意事项 

Most code, even in assembly, does not need to think about shadow-call-stack issues at all.  The calling conventions are not changed.  All use of the stack(and/or the [unsafe stack][safe-stack]) is the same with or withoutshadow-call-stack; *when frame pointers are enabled*, the return address willbe stored on the machine stack next to the frame pointer as expected.  ForAArch64 (ARM64), function calls still use `x30` for the return address asnormal, though functions that clobber `x30` can choose to spill and reload itusing different memory.  Non-leaf functions written in assembly should ideallymake use of the shadow-call-stack ABI by spilling and reloading the returnaddress register there instead of on the machine stack. 大多数代码，即使是汇编代码，也根本不需要考虑影子调用堆栈问题。调用约定不变。有或没有影子调用堆栈，对堆栈（和/或[不安全堆栈] [安全堆栈]）的所有使用都是相同的； *当启用帧指针时*，返回地址将按预期方式存储在机器堆栈中靠近帧指针的位置。对于AArch64（ARM64），函数调用仍然使用`x30`作为正常的返回地址，尽管函数`x30`的函数可以选择使用不同的内存溢出并重新加载它。理想情况下，用汇编语言编写的非叶函数应该通过将影子地址栈ABI溢出并重新加载而不是在机器堆栈上，并在其中重载returnaddress寄存器来利用影子调用栈ABI。

The main exception is code that is implementing something like a non-local exit or context switch.  Such code may need to save or restore the shadow callstack pointer.  Both the `longjmp` function and C++ `throw` already handlethis directly, so C or C++ code using those constructs does not need to doanything new. 主要的例外是正在实现非本地出口或上下文切换之类的代码。此类代码可能需要保存或恢复影子调用堆栈指针。 `longjmp`函数和C ++`throw`已经可以直接处理，因此使用这些结构的C或C ++代码不需要做任何新的事情。

