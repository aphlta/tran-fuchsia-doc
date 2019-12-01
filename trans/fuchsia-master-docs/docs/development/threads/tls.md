 
# Thread Local Storage #  线程本地存储 

The ELF Thread Local Storage ABI (TLS) is a storage model for variables that allows each thread to have a unique copy of a global variable. This modelis used to implement C++'s `thread_local` storage model. On thread creation thevariable will be given its initial value from the initial TLS image. TLSvariables are for instance useful as buffers in thread safe code or for perthread book keeping. C style errors like errno or dlerror can also be handledthis way. ELF线程本地存储ABI（TLS）是变量的存储模型，该模型允许每个线程具有全局变量的唯一副本。该模型用于实现C ++的`thread_local`存储模型。在创建线程时，将从初始TLS映像中为变量赋予其初始值。 TLS变量例如可用作线程安全代码中的缓冲区或用于保留每个线程。像errno或dlerror这样的C风格错误也可以通过这种方式处理。

TLS variables are much like any other global/static variable. In implementation their initial data winds up in the `PT_TLS` segment. The `PT_TLS` segmentis inside of a read only `PT_LOAD` segment despite TLS variables being writable.This segment is then copied into the process for each thread in a uniquewritable location. The location the `PT_TLS` segment is copied to is influencedby the segment's alignment to ensure that the alignment of TLS variables isrespected. TLS变量与任何其他全局/静态变量非常相似。在实现中，它们的初始数据在PT_TLS段中结束。尽管TLS变量是可写的，但PT_TLS段位于只读的PT_LOAD段中，然后将该段复制到每个线程中唯一可写位置的进程中。 PT_TLS段被复制到的位置受段对齐方式的影响，以确保遵守TLS变量的对齐方式。

 
## ABI ##  阿比 

The actual interface that the compiler, linker, and dynamic linker must adhere to is actually quite simple despite the details of the implementation being morecomplex. The compiler and the linker must emit code and dynamic relocations thatuse one of the 4 access models (described in a following section). The dynamiclinker and thread implementation must then set everything up so that thisactually works. Different architectures have different ABIs but they're similarenough at broad strokes that we can speak about most of them as if there wasjust one ABI. This document will assume that either x86-64 or AArch64 is beingused and will point out differences when they occur. 尽管实现细节更加复杂，但是编译器，链接器和动态链接器必须遵循的实际接口实际上非常简单。编译器和链接器必须发出使用4种访问模型之一的代码和动态重定位（在下一节中介绍）。然后，dynamiclinker和线程实现必须进行所有设置，以使其真正起作用。不同的体系结构具有不同的ABI，但是它们在广泛的方面都足够相似，我们可以谈论它们中的大多数，就好像只有一个ABI。本文档将假定正在使用x86-64或AArch64，并将在出现差异时指出差异。

The TLS ABI makes use of a few terms:  TLS ABI使用以下术语：

 
  * Thread Pointer: This is a unique address in each thread, generally stored in a register. Thread local variables lie at offsets from the thread pointer.Thread Pointer will be abbreviated and used as `$tp` in this document. `$tp`is what `__builtin_thread_pointer()` returns on AArch64. On AArch64 `$tp`is given by a special register named `TPIDR_EL0` that can be accessed using`mrs <reg>, TPIDR_EL0`. On `x86_64` the `fs.base` segment base is used andcan be accessed with `%fs:` and can be loaded from `%fs:0` or `rdfsbase`instruction. *线程指针：这是每个线程中的唯一地址，通常存储在寄存器中。线程局部变量位于与线程指针的偏移量处。线程指针将被缩写并在本文档中用作$ tp。 $ tp是__builtin_thread_pointer（）在AArch64上返回的内容。在AArch64上，$ tp由名为TPIDR_EL0的特殊寄存器赋予，可以使用mrs <reg>，TPIDR_EL0进行访问。在`x86_64`上，使用`fs.base`段段库，并且可以通过`％fs：`访问，并且可以从`％fs：0`或`rdfsbase`指令加载。
  * TLS Segment: This is the image of data in each module and specified by the `PT_TLS` program header in each module. Not every module has a `PT_TLS`program header and thus not every module has a TLS segment. Each modulehas at most one TLS segment and correspondingly at most one `PT_TLS`program header. * TLS段：这是每个模块中数据的图像，并由每个模块中的“ PT_TLS”程序标头指定。并非每个模块都有一个“ PT_TLS”程序头，因此也不是每个模块都有一个TLS段。每个模块最多具有一个TLS段，并且相应地具有最多一个“ PT_TLS”程序头。
  * Static TLS set: This is the sum total of modules that are known to the dynamic linker at program start up time. It consists of the main executableand every library transitively mentioned by `DT_NEEDED`. Modules thatrequire being in the Static TLS set have `DF_STATIC_TLS` set on their`DT_FLAGS` entry in their dynamic table (given by the `PT_DYNAMIC` segment). *静态TLS集：这是程序启动时动态链接程序已知的模块总数。它由主要可执行文件和DT_NEEDED传递提及的每个库组成。要求位于静态TLS集中的模块在其动态表的DT_FLAGS条目中设置了DF_STATIC_TLS（由PT_DYNAMIC段提供）。
  * TLS Region: This is a contiguous region of memory unique to each thread. `$tp` will point to some point in this region. It contains theTLS segment of every module in Static TLS set as well as someimplementation-private data which is sometimes called the TCB (ThreadControl Block). On AArch64 a 16-byte reserved space starting at `$tp` isalso sometimes called the TCB. We will refer to this space as the "ABI TCB"in this doc. * TLS区域：这是每个线程唯一的连续内存区域。 $ tp将指向该区域中的某个点。它包含静态TLS集中的每个模块的TLS段，以及一些有时称为TCB（线程控制块）的实现专用数据。在AArch64上，从$ tp开始的16字节保留空间有时也称为TCB。在本文档中，我们将此空间称为“ ABI TCB”。
  * TLS Block: This is an individual thread's copy of a TLS segment. There is one TLS block per TLS segment per thread. * TLS块：这是TLS段的单个线程的副本。每个线程的每个TLS段有一个TLS块。
  * Module ID: The module ID is not statically known except for the main executable's module ID which is always 1. Other module's module IDs arechosen by the dynamic linker. It's just a unique non-zero ID for eachmodule. In theory it could be any non-zero 64-bit value that is unique tothe module like a hash or something. In practice it's just a simple counterthat the dynamic linker maintains. *模块ID：除主可执行文件的模块ID始终为1之外，模块ID并不是一成不变的。动态链接程序选择其他模块的模块ID。这只是每个模块的唯一非零ID。从理论上讲，它可以是模块唯一的任何非零64位值，例如哈希或其他内容。实际上，它只是动态链接程序维护的一个简单计数器。
  * The main executable: This is the module that contains the start address. It, is also treated in a special way in one of the access models. It alwayshas a Module ID of 1. This is the only module that can use fixed offsetsfrom `$tp` via the Local Exec model described below. *主要可执行文件：这是包含起始地址的模块。在访问模型之一中，也以特殊方式对其进行处理。它始终具有1的模块ID。这是唯一可以通过下面描述的Local Exec模型使用来自$ tp的固定偏移量的模块。

To comply with the ABI all access models must be supported.  为了遵守ABI，必须支持所有访问模型。

 
#### Access Models ####  访问模型 

There are 4 access models specified by the ABI:  ABI指定了4种访问模式：

 
  * `global-dynamic`  *`global-dynamic`
  * `local-dynamic`  *`local-dynamic`
  * `initial-exec`  *`initial-exec`
  * `local-exec`  *`local-exec`

These are the values that can be used for `-ftls-model=...` and `__attribute__((tls_model("...")))` 这些是可用于`-ftls-model = ...`和`__attribute __（（tls_model（“ ...”））））的值。

Which model is used relates to:  使用哪种模型涉及：

 
1. Which module is performing the access:  1.哪个模块正在执行访问：
  1. The main executable  1.主要可执行文件
  2. A module in the static TLS set  2.静态TLS集中的一个模块
  3. A module that was loaded after startup, e.g. by `dlopen`  3.在启动后加载的模块，例如由`dlopen`
2. Which module the variable being accessed is defined in:  2.在以下位置定义要访问的变量的模块：
  1. Within the same module (i.e. `local-*`)  1.在同一个模块内（即“ local- *”）
  2. In a different module (i.e. `global-*`)  2.在其他模块（即`global- *`）中

 
* `global-dynamic` Can be used from anywhere, for any variable.  *`global-dynamic`可以在任何地方用于任何变量。
* `local-dynamic` Can be used by any module, for any variable defined in that same module. *`local-dynamic`可以被任何模块使用，用于同一模块中定义的任何变量。
* `initial-exec` Can be used by any module for any variable defined in the static TLS set. *`initial-exec`可以被任何模块用于静态TLS集中定义的任何变量。
* `local-exec` Can be used by the main executable for variables defined in the main executable. *`local-exec`可由主可执行文件用于主可执行文件中定义的变量。

 
###### Global Dynamic ######  全球动态 

Global dynamic is the most general access format. It is also the slowest. Any thread-local global variable should be accessible with this method. Thisaccess model *must* be used if a dynamic library accesses a symbol defined inanother module (see exception in section on Initial Exec). Symbols definedwithin the executable need not use this access model. The main executable canalso avoid using this access model. This is the default access model whencompiling with `-fPIC` as is the norm for shared libraries. 全局动态是最通用的访问格式。它也是最慢的。任何线程局部全局变量都可以使用此方法访问。如果动态库访问在另一个模块中定义的符号，则必须使用此访问模型（请参阅初始执行部分中的异常）。可执行文件中定义的符号不需要使用此访问模型。主可执行文件还可以避免使用此访问模型。与共享库的规范一样，这是在使用-fPIC进行编译时的默认访问模型。

This access model works by calling a function defined in the dynamic linker. There are two ways functions might be called, via TLSDESC, or via`__tls_get_addr`. 该访问模型通过调用动态链接器中定义的函数来工作。可以通过TLSDESC或通过__tls_get_addr调用函数的方法有两种。

In the case of `__tls_get_addr` it is passed the pair of `GOT` entries associated with this symbol. Specifically it is passed the pointer to the firstand the second entry comes right after it. For a given symbol `S`, the firstentry, denoted `GOT_S[0]`, must contain the Module ID of the module in which`S` was defined. The second entry, denoted `GOT_S[1]`, must contain offset intoTLS Block which is the same as the offset of the symbol in the `PT_TLS` segmentof the associated module. The pointer to `S` is then computed using`__tls_get_addr(GOT_S)`. The implementation of `__tls_get_addr` will bediscussed later. 如果是__tls_get_addr，则传递与此符号关联的一对GOT条目。具体来说，它传递的是指向第一个条目的指针，第二个条目紧随其后。对于给定的符号“ S”，表示为“ GOT_S [0]”的第一个条目必须包含定义了“ S”的模块的模块ID。第二个条目，表示为“ GOT_S [1]”，必须包含TLS块的偏移量，该偏移量与关联模块的“ PT_TLS”段中符号的偏移量相同。然后使用__tls_get_addr（GOT_S）计算指向S的指针。 __tls_get_addr的实现将在以后讨论。

TLSDESC is an alternative ABI for `global-dynamic` access (and `local-dynamic`) where a different pair of `GOT` slots are used where the first `GOT` slotcontains a function pointer. The second contains some dynamic linker definedauxiliary data. This allows the dynamic linker a choice over which function iscalled depending on circumstance. TLSDESC是用于“全局动态”访问（和“本地动态”）的备用ABI，其中使用了不同的一对“ GOT”插槽，其中第一个“ GOT”插槽包含一个函数指针。第二个包含一些动态链接器定义的辅助数据。这允许动态链接器根据情况选择调用哪个函数。

In both cases the calls to these functions must be implemented by a specific code sequence and a specific set of relocs. This allows the linker to recognizethese accesses and potentially relax them to the `local-dynamic` access model. 在这两种情况下，对这些函数的调用都必须通过特定的代码序列和一组特定的重定位来实现。这使链接器可以识别这些访问，并有可能将其放宽到“本地动态”访问模型。

(NOTE: The following paragraph contains details about how the compiler upholds its end of the ABI. Skip this paragraph if you don't care about that.) （注意：以下段落包含有关编译器如何维护其ABI末尾的详细信息。如果您不关心此内容，请跳过本段。）

For the compiler to emit code for this access model a call needs to be emitted against `__tls_get_addr` (defined by the dynamic linker) and a reference to thesymbol name. Specifically the compiler the emits code for (minding theadditional relocation needed for the GOT itself) `__tls_get_addr(GOT_S)`. Thelinker then emits two dynamic relocations when generating the GOT. On `x86_64`these are `R_X86_64_DTPMOD` and `R_X86_64_DTPOFF`. On AArch64 these are`R_AARCH64_DTPMOD` and `R_AARCH64_DTPOFF`. These relocations reference the symbolregardless of whether or not the module defines a symbol by that name or not. 为了使编译器能够为此访问模型发出代码，需要针对__tls_get_addr（由动态链接器定义）和对符号名称的引用进行调用。具体地说，编译器发出用于（注意GOT本身所需的其他重定位）“ __ tls_get_addr（GOT_S）”的代码。然后，链接器在生成GOT时会发出两个动态重定位。在`x86_64`上是`R_X86_64_DTPMOD`和`R_X86_64_DTPOFF`。在AArch64上，它们是R_AARCH64_DTPMOD和R_AARCH64_DTPOFF。无论模块是否通过该名称定义符号，这些重定位均引用该符号。

 
###### Local Dynamic ######  局部动态 

Local dynamic the same as Global Dynamic but for local symbols. It can be thought of as a single `global-dynamic` access to the TLS block of this module.Then because every variable defined in the module is at fixed offsets from theTLS block the compiler can optimize multiple `global-dynamic` calls into one.The compiler will relax a `global-dynamic` access to a `local-dynamic` accesswhenever the variables are local/static or have hidden visibility. The linkermay sometimes be able to relax some `global-dynamic` accesses to `local-dynamic`as well. 局部动态与全局动态相同，但局部符号相同。可以将其视为对该模块TLS块的单一“全局动态”访问。然后，由于模块中定义的每个变量都与TLS块处于固定偏移量，因此编译器可以将多个“全局动态”调用优化为一个每当变量是局部/静态或具有隐藏的可见性时，编译器都会放宽对“局部动态”访问的“全局动态”访问。链接器有时也可以放松对“局部动态”的某些“全局动态”访问。

The following gives an example of how the compiler might emit code for this access model: 下面给出了一个示例，说明了编译器如何为此访问模型发出代码：

```
static thread_local char buf[buf_cap];
static thread_local size_t buf_size = 0;
while(*str && buf_size < buf_cap) {
  buf[buf_size++] = *str++;
}
```
 

might be lowered to  可能会降低到

```
// GOT_module[0] is the module ID of this module
// GOT_module[1] is just 0
// <X> denotes the offset of X in this module's TLS block
tls = __tls_get_addr(GOT_module)
while(*str && *(size_t*)(tls+<buf_size>) < buf_cap) {
  (char*)(tls+<buf>)[*(size_t*)(tls+<buf_size>)++] = *str++;
}
```
 

If this code used global dynamic it would have to make at least 2 calls, one to get the pointer for buf and the other to get the pointer for `buf_size`. 如果此代码使用全局动态，则必须至少进行两次调用，一个调用获取buf的指针，另一个调用获取“ buf_size”的指针。

 
###### Initial Exec ######  初始执​​行 

This access model can be used anytime the compiler knows the module that the symbol being accessed is defined in will be loaded in the initial set ofexecutables rather than opened using `dlopen`. This access model is generallyonly used when the main executable is accessing a global symbol with defaultvisibility. This is because compiling an executable is the only time thecompiler knows that any code generated will be in the initial executable set. Ifa DSO is compiled to make thread local accesses use this model then the DSOcannot be safely opened with `dlopen`. This is acceptable in performancecritical applications and in cases where you know the binary will never bedlopen-ed such as in the case of libc. Modules compiled/linked this way havetheir `DF_STATIC_TLS` flag set. 只要编译器知道定义要访问的符号的模块将装入初始可执行文件集中，而无需使用dlopen打开，即可使用此访问模型。通常仅在主可执行文件以默认可见性访问全局符号时使用此访问模型。这是因为编译可执行文件是编译器唯一一次知道所生成的任何代码将在初始可执行文件集中的时间。如果编译了DSO以使线程本地访问使用此模型，则无法使用dlopen安全地打开DSO。在对性能至关重要的应用程序中，以及在您知道二进制文件永远不会被公开的情况下（例如libc），这是可以接受的。通过这种方式编译/链接的模块设置了其DF_STATIC_TLS标志。

Initial Exec is the default when compiling without `-fPIC`.  不使用-fPIC进行编译时，Initial Exec是默认设置。

The compiler emits code without even calling `__tls_get_addr` for this access model. It does so using a single GOT entry which we'll denote `GOT_s` for symbol`s` which the compiler emits relocations for to ensure that 对于此访问模型，编译器甚至不会调用`__tls_get_addr`来发出代码。它使用单个GOT条目来执行此操作，我们将其表示为符号s的GOT_s，编译器将为其发出重新定位以确保

```
extern thread_local int a;
extern thread_local int b;
int main() {
  return a + b;
}
```
 

would be lowered to something like the following  将被降低为以下内容

```
int main() {
  return *(int*)($tp + GOT[a]) + *(int*)($tp + GOT[b]);
}
```
 

Note that on x86 architectures `GOT[s]` will actually resolve to a negative value. 注意，在x86架构上，`GOT [s]`实际上会解析为负值。

 
###### Local Exec ######  本地执行 

This is the fastest access model and can only be used if the symbol is in the first TLS block which is the TLS block of the main executable. In practice onlythe main executable can use this access mode because any shared library can't(and normally wouldn't need to) know if it is accessing something from the mainexecutable. The linker will relax `initial-exec` to `local-exec`. The compilercan't do this without explicit instructions via `-ftls-model` or`__attribute__((tls_model("...")))` because the compiler cannot know if thecurrent translation unit is going to be linked into a main executable or ashared library. 这是最快的访问模型，仅当符号在第一个TLS块（即主要可执行文件的TLS块）中时才能使用。在实践中，只有主可执行文件才能使用此访问模式，因为任何共享库都无法（通常不需要）知道它是否正在访问来自mainexecutable的内容。链接器会将“ initial-exec”放宽到“ local-exec”。如果没有通过`-ftls-model`或`__attribute __（（tls_model（“ ...”）））`的明确指令，编译器将无法执行此操作，因为编译器无法知道当前翻译单元是否将链接至主可执行文件或共享库。

The precise details of how this offset is computed changes a bit from architecture to architecture. 如何计算此偏移量的精确细节在架构之间有所不同。

example code:  示例代码：

```
static thread_local int a;
static thread_local int b;

int main() {
  return a + b;
}
```
 

would be lowered to  会降低到

```
int main() {
  return (int*)($tp+TPOFF_a) + (int*)($tp+TPOFF_b));
}
```
 

On AArch64 `TPOFF_a == max(16, p_align) + <a>` where `p_align` is exactly the `p_align` field of the main executable's `PT_TLS` segment and `<a>` is theoffset of `a` from the beginning of the main executable's TLS segment. 在AArch64上，TPOFF_a == max（16，p_align）+ <a>`，其中`p_align`正是主可执行文件`PT_TLS`段的`p_align`字段，而`<a>`是`a`从主可执行文件的TLS段的开头。

On `x86_64` `TPOFF_a == -<a>` where `<a>` is the offset of the `a` from the *end* of the main executable's TLS segment. 在`x86_64`上`TPOFF_a ==-<a>`其中`<a>`是`a`与主要可执行文件TLS段的* end *的偏移量。

The linker is aware of what `TPOFF_X` is for any given `X` and fills in this value. 链接器知道对于任何给定的“ X”而言，“ TPOFF_X”是什么，并填写该值。

 
## Implementation ##  实作 

This section discusses the implementation as it is implemented on Fuchsia. This said the broad strokes here are widely similar across different libcimplementations including musl and glibc. 本节讨论在紫红色上实现的实现。这就是说，在包括musl和glibc在内的不同libcimplementations中，此处的粗略笔画是非常相似的。

The actual implementation of all of this introduces a few more details. Namely the so-called "DTV" (Dynamic Thread Vector) (denoted `dtv` in this doc) whichindexes TLS blocks by module ID. The following diagram shows what the initialexecutable set looks like. In Fuchsia's implementation we actually store abunch of meta information in a thread descriptor struct along with theABI TCB (denoted `tcb` below). In our implementation we use the first 8 bytesof this space to point to the DTV. At first `tcb` points to `dtv` as shown inthe below diagrams but after a dlopen this can change. 所有这些的实际实现引入了更多细节。即所谓的“ DTV”（动态线程向量）（在本文档中表示为“ dtv”），它按模块ID为TLS块编制索引。下图显示了初始可执行集的外观。在Fuchsia的实现中，我们实际上将大量的元信息与ABI TCB（以下称为“ tcb”）一起存储在线程描述符结构中。在我们的实现中，我们使用该空间的前8个字节指向DTV。最初，“ tcb”指向“ dtv”，如下图所示，但是在dlopen之后，它可以改变。

arm64:  arm64：

```
*------------------------------------------------------------------------------*
| thread | tcb | X | tls1 | ... | tlsN | ... | tls_cnt | dtv[1] | ... | dtv[N] |
*------------------------------------------------------------------------------*
^         ^         ^             ^            ^
td        tp      dtv[1]       dtv[n+1]       dtv
```
 

Here `X` has size `min(16, tls_align) - 16` where `tls_align` is the maximum alignment of all loaded TLS segments from the static TLS set. This is set bythe static linker since the static linker resolves `TPOFF_*` values. Thispadding is set that so that if, as required, `$tp` is aligned to mainexecutable's `PT_TLS` segment's `p_align` value then `tls1 - $tp` will be`max(16, p_align)`. This ensures that there is always at least a 16 byte spacefor the ABI TCB (denoted `tcb` in the diagram above). 这里的`X`的大小为`min（16，tls_align）-16`，其中`tls_align`是来自静态TLS集的所有已加载TLS段的最大对齐方式。这是由静态链接器设置的，因为静态链接器解析“ TPOFF_ *”值。设置该填充以使如果根据需要将$ tp与mainexecutable的PT_TLS段的p_align值对齐，则tls1-$ tp将为max（16，p_align）。这样可以确保ABI TCB始终至少有16个字节的空间（在上图中表示为“ tcb”）。

x86:  x86：

```
*-----------------------------------------------------------------------------*
| tls_cnt | dtv[1] | ... | dtv[N] | ... | tlsN | ... | tls1 | tcb |  thread   |
*-----------------------------------------------------------------------------*
^                                       ^             ^       ^
dtv                                  dtv[n+1]       dtv[1]  tp/td
```
 

Here `td` denotes the "thread descriptor pointer". In both implementations this points to the thread descriptor. A subtle point not made apparent in thesediagrams is that `tcb` is actually a member of the thread descriptor struct inboth cases but on AArch64 it is the last member and on `x86_64` it is the firstmember. 这里的“ td”表示“线程描述符指针”。在这两种实现中，这都指向线程描述符。在这些图中没有显示出一个微妙的要点，在这两种情况下，“ tcb”实际上是线程描述符struct的成员，但在AArch64上它是最后一个成员，而在“ x86_64”上它是第一个成员。

 
#### dlopen ####  dlopen 

This picture explains what happens for the initial executables but it doesn't explain what happens in the `dlopen` case. When `__tls_get_addr` is called itfirst checks to see if `tls_cnt` is such that the module ID (given by `GOT_s[0]`) is within the `dtv`. If it is then it simply looks up `dtv[GOT_s[0]] + GOT_s[1]`but if it isn't something more complicated happens. See the implementation of`__tls_get_new` in [dynlink.c](/zircon/third_party/ulib/musl/ldso/dynlink.c). 这张图解释了初始可执行文件的情况，但没有解释dlopen情况下的情况。当调用__tls_get_addr时，它首先检查tls_cnt是否使模块ID（由GOT_s [0]给出）在dtv内。如果是，那么它只是查找`dtv [GOT_s [0]] + GOT_s [1]`，但如果不是这样，则会发生更复杂的事情。请参阅[dynlink.c]（/ zircon / third_party / ulib / musl / ldso / dynlink.c）中的__tls_get_new的实现。

