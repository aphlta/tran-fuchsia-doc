 
# SafeStack in Zircon & Fuchsia  锆石紫红色的SafeStack 

[TOC]  [目录]

 
## Introduction  介绍 

LLVM's [safe-stack feature](https://clang.llvm.org/docs/SafeStack.html) is a compiler mode intended to harden the generated code againststack-smashing attacks such as exploits of buffer overrun bugs. LLVM的[安全堆栈功能]（https://clang.llvm.org/docs/SafeStack.html）是一种编译器模式，旨在加强生成的代码，以抵抗诸如缓冲区溢出错误等利用堆栈破坏的攻击。

The Clang/LLVM documentation page linked above describes the general scheme.  The capsule summary is that that each thread has two stacksinstead of the usual one: a "safe stack" and an "unsafe stack".  Theunsafe stack is used for all purposes where a pointer into the stackmemory might be used, while the safe stack is used only for purposeswhere no code should ever see a pointer into the stack memory.  So, theunsafe stack is used for arrays or variables that are passed byreference to another function or have their addresses stored in theheap--memory that could be subject to buffer overrun or use-after-freebugs and their exploits.  The safe stack is used for the compiler'sregister spills, and for the return address of a function call.  Thus,for example, a simple buffer overrun bug cannot be exploited tooverwrite the return address of the containing function, which is thebasis of exploits and attacks using the so-called *ROP*("return-oriented programming") technique. 上面链接的Clang / LLVM文档页面描述了一般方案。封装摘要是，每个线程具有两个堆栈，而不是通常的堆栈：“安全堆栈”和“不安全堆栈”。非安全堆栈用于所有可能使用指向堆栈内存的指针的目的，而安全堆栈仅用于没有代码应看到指向堆栈内存的指针的目的。因此，不安全堆栈用于通过引用传递给另一个函数的数组或变量，或者将其地址存储在堆中-内存可能会遭受缓冲区溢出或释放后使用bug及其利用。安全堆栈用于编译器的寄存器溢出以及函数调用的返回地址。因此，例如，不能利用简单的缓冲区溢出错误来覆盖包含函数的返回地址，这是利用所谓的* ROP *（“面向返回的编程”）技术进行漏洞利用和攻击的基础。

The **Compatibility** section of that page does not apply to Zircon (or Fuchsia).  In Zircon user-mode code (including all of Fuchsia), theruntime support for SafeStack is included directly in the standard Cruntime library, and everything works fine in shared libraries (DSOs). 该页面的“兼容性”部分不适用于锆石（或紫红色）。在Zircon用户模式代码（包括所有的Fuchsia）中，对SafeStack的运行时支持直接包含在标准Cruntime库中，并且一切在共享库（DSO）中都可以正常工作。

The [safe-stack](https://clang.llvm.org/docs/SafeStack.html) and [shadow-call-stack](shadow_call_stack.md) instrumentation schemes and ABIs arerelated and similar but also orthogonal.  Each can be enabled or disabledindependently for any function.  Fuchsia's compiler ABI and libc alwaysinteroperate with code built with or without either kind of instrumentation,regardless of what instrumentation was or wasn't used in the particular libcbuild. [安全堆栈]（https://clang.llvm.org/docs/SafeStack.html）和[shadow-call-stack]（shadow_call_stack.md）检测方案和ABI是相关且相似的，但也是正交的。每种功能均可独立启用或禁用。紫红色的编译器ABI和libc始终可以与使用或不使用任何一种工具建立的代码进行互操作，而不管特定的libcbuild中使用或不使用什么工具。

 
## Interoperation and ABI Effects  互操作和ABI效应 

In general, safe-stack does not affect the ABI.  The machine-specific calling conventions are unchanged.  It works fine to have somefunctions in a program built with safe-stack and some not.  It doesn'tmatter if combining the two comes from directly compiled `.o` files,from archive libraries (`.a` files), or from shared libraries (`.so`files), in any combination. 通常，安全堆叠不会影响ABI。特定于计算机的调用约定不变。在具有安全堆栈功能的程序中具有某些功能，而有些功能则不能。结合使用直接编译的.o文件，归档库（.a文件）或共享库（.so文件）（两者以任意组合）两者是没有关系的。

While there is some additional per-thread state (the *unsafe stack pointer*, see below under *Implementation details*), code not usingsafe-stack does not need to do anything about this state to keep itcorrect when calling, or being called by, code that does usesafe-stack.  The only potential exceptions to this are for code thatis implementing its own kinds of non-local exits or context-switching(e.g. coroutines).  The Zircon C library's `setjmp`/`longjmp` codesaves and restores this additional state automatically, so anythingthat is based on `longjmp` already handles everything correctly evenif the code calling `setjmp` and `longjmp` doesn't know aboutsafe-stack. 尽管存在一些其他的每线程状态（*不安全堆栈指针*，请参见下面的*实现详细信息*），但未使用安全堆栈的代码无需对此状态进行任何操作即可在调用或被调用时保持其正确性，确实使用安全堆栈的代码。唯一可能的例外是正在实现自己的非本地出口或上下文切换（例如协程）的代码。 Zircon C库的`setjmp` /`longjmp`代码会自动保存并恢复此附加状态，因此，即使调用`setjmp`和`longjmp`的代码不了解安全堆栈，任何基于`longjmp`的东西都可以正确处理所有内容。

 
## Use in Zircon & Fuchsia  在锆石紫红色中使用 

This is enabled in the Clang compiler by the `-fsanitize=safe-stack` command-line option.  This is the default mode of the compiler for `*-fuchsia`targets.  To disable it for a specific compilation, use the`-fno-sanitize=safe-stack` option. 在Clang编译器中，通过`-fsanitize = safe-stack`命令行选项启用了此功能。这是** fuchsia`targets编译器的默认模式。要为特定的编译禁用它，请使用-fno-sanitize = safe-stack`选项。

Zircon supports safe-stack for both user-mode and kernel code. In the Zircon build, safe-stack is always enabled when buildingwith Clang (pass `variants = [ "clang" ]` to `GN`). Zircon支持用户模式和内核代码的安全堆栈。在Zircon构建中，使用Clang进行构建时始终启用安全堆栈（将`variants = [“ clang”]`传递至`GN`）。

 
## Implementation details  实施细节 

The essential addition to support safe-stack code is the *unsafe stack pointer*.  In the abstract, this can be thought of as an additionalregister just like the machine's normal stack pointer register.  Themachine's stack pointer register is used for the safe stack, just as italways has been.  The unsafe stack pointer is used as if it were anotherregister with a fixed purpose in the ABI, but of course the machinesdon't actually have a new register, and for compatibility safe-stackdoes not change the basic machine-specific calling conventions thatassign uses to all the machine registers. 支持不安全堆栈代码的基本补充是*不安全堆栈指针*。概括而言，可以将其视为额外的寄存器，就像机器的常规堆栈指针寄存器一样。机器的堆栈指针寄存器用于安全堆栈，就像过去一样。使用不安全的堆栈指针就好像它是ABI中具有固定用途的另一个寄存器一样，但是当然这些机器实际上没有新的寄存器，并且出于兼容性的考虑，安全堆栈不会将assign用于的特定于机器的基本调用约定更改为所有机器寄存器。

The C and C++ ABI for Zircon and Fuchsia stores the unsafe stack pointer in memory that's at a fixed offset from the thread pointer.The [`<zircon/tls.h>`](/zircon/system/public/zircon/tls.h) header definesthe offset for each machine. Zircon和Fuchsia的C和C ++ ABI将不安全的堆栈指针存储在与线程指针有固定偏移量的内存中。[`<zircon / tls.h>`]（/ zircon / system / public / zircon / tls。 h）标头定义每台机器的偏移量。

For x86 user-mode, the thread pointer is the `fsbase`, meaning access in assembly code looks like `%fs:ZX_TLS_UNSAFE_SP_OFFSET`.For the x86 kernel, the thread pointer is the `gsbase`, meaning accessin assembly code looks like `%gs:ZX_TLS_UNSAFE_SP_OFFSET`. 对于x86用户模式，线程指针是`fsbase`，这意味着在汇编代码中的访问类似于`％fs：ZX_TLS_UNSAFE_SP_OFFSET`。对于x86内核，线程指针是`gsbase`，这意味着在汇编代码中的访问类似于` ％gs：ZX_TLS_UNSAFE_SP_OFFSET`。

For Aarch64 (ARM64), in C or C++ code, `__builtin_thread_pointer()` returns the thread pointer.  In user-mode, the thread pointer is in the`TPIDR_EL0` special register and must be fetched into a normal register(with `mrs *reg*, TPIDR_EL0`) to access the memory, so it's not a singleinstruction in assembly code.  In the kernel, it's just the same butusing the `TPIDR_EL1` special register instead. 对于Aarch64（ARM64），在C或C ++代码中，__builtin_thread_pointer（）返回线程指针。在用户模式下，线程指针位于特殊寄存器“ TPIDR_EL0”中，并且必须通过普通寄存器（带有“ mrs * reg *，TPIDR_EL0”）来访存，因此它不是汇编代码中的单一指令。在内核中，它是相同的，只是使用了“ TPIDR_EL1”特殊寄存器。

 
### Notes for low-level and assembly code  低级和汇编代码的注意事项 

Most code, even in assembly, does not need to think about safe-stack issues at all.  The calling conventions are not changed.  Using thestack for saving registers, finding return addresses, etc. is all thesame with or without safe-stack.  The main exception is code that isimplementing something like a non-local exit or context switch.  Suchcode may need to save or restore the unsafe stack pointer.  Both the`longjmp` function and C++ `throw` already handle this directly, soC or C++ code using those constructs does not need to do anything new. 大多数代码，即使是汇编代码，也根本不需要考虑安全堆栈问题。调用约定不变。无论使用或不使用安全堆栈，都使用堆栈来保存寄存器，查找返回地址等。主要的例外是实现非本地出口或上下文切换之类的代码。这样的代码可能需要保存或恢复不安全的堆栈指针。 “ longjmp”函数和C ++“ throw”函数都已经可以直接处理此问题，因此使用这些结构的C或C ++代码不需要做任何新的事情。

The context-switch code in the kernel handles switching the unsafe stack pointer.  On x86, this is explicit in the code: `%gs` points to the`struct x86_percpu`, which has a member `kernel_unsafe_sp` at`ZX_TLS_UNSAFE_SP_OFFSET`; `arch_context_switch` copies this into the`unsafe_sp` field of the old thread's `struct arch_thread` and thencopies the new thread's `unsafe_sp` into `kernel_unsafe_sp`.  On ARM64,this is implicitly done by `set_current_thread`, because that changesthe `TPIDR_EL1` special register, which points directly into theper-thread `struct thread` rather than a per-CPU structure like on x86. 内核中的上下文切换代码处理不安全堆栈指针的切换。在x86上，这在代码中是明确的：％s指向结构x86_percpu，在ZX_TLS_UNSAFE_SP_OFFSET处具有成员kernel_unsafe_sp。 “ arch_context_switch”将其复制到旧线程的“ struct arch_thread”的“ unsafe_sp”字段中，然后将新线程的“ unsafe_sp”复制到“ kernel_unsafe_sp”中。在ARM64上，这是由set_current_thread隐式完成的，因为这会更改TPIDR_EL1特殊寄存器，该寄存器直接指向每个线程的结构线程，而不是像x86那样的每个CPU结构。

