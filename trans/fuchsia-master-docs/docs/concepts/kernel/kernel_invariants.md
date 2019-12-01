 
# Zircon Kernel Invariants  锆石内核不变量 

On x86, Zircon needs to maintain the following invariants for code running in ring 0 (kernel mode). 在x86上，Zircon需要维护在环0（内核模式）下运行的代码的以下不变量。

These invariants are documented here because they are not necessarily easy to test -- breaking an invariant will not necessarily be caught byZircon's test suite. 这些不变量在此处进行了记录，因为它们不一定易于测试-打破不变式不一定会被Zircon的测试套件捕获。

 
* Flags register:  *标志注册：

 
  * The direction flag (DF) should be 0.  This is required by the x86 calling conventions. *方向标志（DF）应该为0。这是x86调用约定所必需的。

    If this flag is set to 1, uses of x86 string instructions (e.g. `rep movs` in `memcpy()` or inlined by the compiler) can go wrong and copyin the wrong direction.  It is OK for a function to set this flag to 1temporarily as long as it changes it back to 0 before returning orcalling other functions. 如果将此标记设置为1，则使用x86字符串指令（例如，“ memcpy（）”中的“ rep movs”或由编译器内联）可能会出错，并会沿错误的方向复制。只要在返回或调用其他函数之前将其更改回0，就可以将该标志临时设置为1。

 
  * The alignment check flag (AC) should normally be 0.  On CPUs that support SMAP, this prevents the kernel from accidentally reading orwriting userland data. *对齐检查标志（AC）通常应为0。在支持SMAP的CPU上，这可以防止内核意外读取或写入用户态数据。

 
* The `gs_base` register must point to the current CPU's `x86_percpu` struct whenever running in kernel mode with interrupts enabled.`gs_base` should only be changed to point to something else whileinterrupts are disabled.  For example, the `swapgs` instruction shouldonly be used when interrupts are disabled. *每当在启用了中断的内核模式下运行时，gs_base寄存器都必须指向当前CPU的x86_percpu结构。gs_base只能在禁止中断的情况下更改为指向其他对象。例如，仅当禁用中断时才应使用“ swapgs”指令。

 
* The following are partially enforced by the compiler:  *以下部分由编译器强制执行：

 
  * No use of extended registers (SSE, AVX, x87, etc.) is allowed, because that would clobber userland's register state. *不允许使用扩展寄存器（SSE，AVX，x87等），因为这会破坏用户区的寄存器状态。

    This is partially achieved by passing `-mno-sse` to the compiler.  This option is necessary to prevent the compiler from using SSE registers inoptimizations (e.g. memory copies). 这可以通过将-mno-sse传递给编译器来部分实现。该选项对于防止编译器使用SSE寄存器优化（例如内存副本）是必需的。

    We would like to prevent accidentally using the `float` or `double` types in kernel code, but GCC and Clang won't do that for us in allcases.  `-mno-sse` does not prevent using `float`/`double` with eithercompiler -- the compilers will use x87 instructions instead. 我们希望防止在内核代码中意外使用`float`或`double`类型，但是GCC和Clang在所有情况下都不会为我们这样做。 `-mno-sse`不会阻止在两个编译器中使用`float` /`double`-编译器将改用x87指令。

    We compile with `-msoft-float`, which seems to prevent GCC from generating x87 instructions (and hence using x87 registers): GCC 6.3.0will give an error on `float`/`double` arithmetic and return values,but it does not prevent passing these types around as arguments.However, passing `-msoft-float` to Clang seems to have no effect: Clang7.0.0 will still generate x87 instructions (and use x87 registers) forcode using `float` or `double`. 我们使用`-msoft-float`进行编译，这似乎阻止了GCC生成x87指令（并因此使用x87寄存器）：GCC 6.3.0将在`float` /`double`算术上给出错误并返回值，但确实如此不能阻止将这些类型作为参数传递。但是，将-msoft-float传递给Clang似乎没有效果：Clang7.0.0仍会使用xfloat或double生成x87指令（并使用x87寄存器）进行编码。

 
  * No storing data below `%rsp` on the stack.  Note that userland code can do this: the SysV x86-64 ABI allows functions to store data in the "redzone", which is the 128 bytes below %rsp.  However, kernel code cannotuse the red zone because interrupts may clobber this region -- the CPUpushes data onto the stack immediately below %rsp when it invokes aninterrupt handler. *不在堆栈上的`％rsp'下面存储数据。请注意，用户级代码可以执行此操作：SysV x86-64 ABI允许函数将数据存储在“红色区域”中，该区域位于％rsp以下128字节。但是，内核代码不能使用红色区域，因为中断可能会破坏该区域-CPU在调用中断处理程序时将数据直接推送到％rsp下方的堆栈上。

