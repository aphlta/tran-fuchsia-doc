 
# libc  图书馆 

 
## What do we mean by libc?  libc是什么意思？ 

On Posix-y systems, programs link against a library (either dynamically or statically) called libc. This library provides thefunctions defined by the C standard, as well as the runtimeenvironment for C programs. Many systems also define otherplatform-specific interfaces in the same library. Many of theseinterfaces are the preferred way for userspace to access kernelfunctionality. For example, Posix-y systems have an `open` function intheir libc which calls an `open` system call. Sometimes these arecross-platform standards, such as pthreads. Others are interfaces tokernel-specific functionality, such as `epoll` or `kqueue`. In anycase, this library is present on the system itself and is a stableinterface. In contrast, Windows does not provide a systemwide libc inits stable win32 interface. 在Posix-y系统上，程序链接到称为libc的库（动态或静态）。该库提供了C标准定义的功能，以及C程序的运行时环境。许多系统还在同一个库中定义其他平台特定的接口。这些接口中的许多接口是用户空间访问内核功能的首选方式。例如，Posix-y系统在其libc中具有一个“ open”功能，该功能调用“ open”系统调用。有时，这些是跨平台标准，例如pthreads。其他是特定于内核的功能的接口，例如“ epoll”或“ kqueue”。无论如何，该库都存在于系统本身，并且是一个稳定的接口。相反，Windows并未在其稳定的win32接口中提供系统范围的libc。

On Fuchsia the story is a bit different from Posix systems. First, the Zircon kernel (Fuchsia's microkernel) does not provide a typicalPosix system call interface. So a Posix function like `open` can'tcall a Zircon `open` syscall. Secondly, Fuchsia implements some partsof Posix, but omits large parts of the Posix model. Most conspicuouslyabsent are signals, fork, and exec. Third, Fuchsia does not requirethat programs use libc's ABI. Programs are free to use their own libc,or to do without. However, Fuchsia does provide a libc.so whichprograms can dynamically link, which provides implementations both ofthe C standard library and of the parts of Posix Fuchsia supports, astypical Posix systems do. 在紫红色上，故事与Posix系统略有不同。首先，Zircon内核（紫红色的微内核）没有提供典型的Posix系统调用接口。因此，像“ open”这样的Posix函数不能调用Zircon“ open”系统调用。其次，紫红色实现了Posix的某些部分，但是省略了Posix模型的大部分。最明显的是信号，派生和执行。第三，紫红色不要求程序使用libc的ABI。程序可以自由使用自己的libc，也可以自由使用。但是，Fuchsia确实提供了libc.so，程序可以动态链接，该程序可以提供C标准库以及Posix Fuchsia支持的部分（非典型Posix系统）的实现。

 
## Piece by piece  一件一件 

This is a partial list of what is implemented (or not) in Fuchsia's libc. 这是在紫红色的libc中实现（或未实现）的部分列表。

 
### The C standard library  C标准库 

Fuchsia's libc implements the C11 standard. In particular this includes the threading-related interfaces such as threads (`thrd_t`)and mutexes (`mtx_t`). A small handful of extensions are also in thisportion of the system to bridge the C11 structures, like a `thrd_t`,to underlying kernel structures, like the `zx_handle_t` underlying it. 紫红色的libc实施C11标准。特别是，这包括与线程相关的接口，例如线程（thrd_t）和互斥锁（mtx_t）。系统的这一部分也有少量扩展，可以将C11结构（如Thrd_t）桥接到基础内核结构（如其底层的zx_handle_t）。

 
### Posix  Posix 

Posix defines a number of interfaces. These include (not exhaustively): file I/O, BSD sockets, and pthreads. Posix定义了许多接口。其中包括（并非穷尽）：文件I / O，BSD套接字和pthread。

 
#### File I/O and BSD sockets  文件I / O和BSD插槽 

Recall that Zircon is a microkernel that is not in the business of implementing file I/O. Instead, other Fuchsia userspace servicesprovide filesystems. libc itself defines weak symbols for Posix fileI/O functions such as `open`, `write`, and `fstat`. However, all thesecalls simply fail. In addition to libc.so, programs can link thefdio.so library. fdio knows how to speak to those other Fuchsiaservices over[Channel IPC][zircon-concepts-message-passing], andprovides a Posix-like layer for libc to expose. Sockets are similarlyimplemented via fdio communicating with the userspace network stack. 回想一下，Zircon是一个微内核，与实现文件I / O无关。相反，其他Fuchsia用户空间服务提供了文件系统。 libc本身为Posix fileI / O功能定义了弱符号，例如“ open”，“ write”和“ fstat”。但是，所有这些调用都失败了。除了libc.so，程序还可以链接thefdio.so库。 fdio知道如何通过[Channel IPC] [zircon-concepts-message-passing]与其他Fuchsia服务进行通话，并为libc提供了类似于Posix的层来公开。套接字通过与用户空间网络堆栈通信的fdio类似地实现。

 
#### pthreads  线程 

Fuchsia's libc provides parts of the pthread standard. In particular, the core parts of `pthread_t` (those that map straightforwardly ontothe corresponding C11 concepts) and synchronization primitives like`pthread_mutex_t` are provided. Some details, like process-sharedmutexes, are not implemented. The implemented subset does not aim tobe comprehensive. 紫红色的libc提供了pthread标准的一部分。特别是，提供了“ pthread_t”的核心部分（直接映射到相应的C11概念的核心部分）和诸如“ pthread_mutex_t”之类的同步原语。某些细节（如进程共享的互斥量）未实现。实施的子集并不旨在变得全面。

 
#### Signals  讯号 

Fuchsia does not have Unix-style signals. Zircon provides no way to directly implement them (the kernel provides no way to cause anotherthread to jump off its thread of execution). Fuchsia's libc does not,therefore, have a notion of signal-safe functions, and is notimplemented internally to be aware of mechanisms like signals. 紫红色没有Unix风格的信号。 Zircon没有提供直接实现它们的方法（内核没有提供使其他线程跳出其执行线程的方法）。因此，紫红色的libc没有信号安全功能的概念，并且在内部未实现以意识到信号等机制。

Because of this fact, libc functions will not `EINTR`, and it is not necessary for Fuchsia-only code to consider that case. However, it isperfectly safe to do so. Fuchsia still defines the `EINTR` constant,and code written for both Posix and Fuchsia may still have`EINTR`-handling loops. 由于这个事实，libc函数将不会使用“ EINTR”，并且仅紫红色代码不必考虑这种情况。但是，这样做绝对是安全的。紫红色仍然定义了EINTR常量，为Posix和紫红色编写的代码可能仍然具有EINTR处理循环。

 
#### fork and exec  分叉和执行 

Zircon does not have fork or exec. Instead, process creation is provided by [fdio] (/zircon/system/ulib/fdio). While Zircon has Process andThread objects, these are pretty raw and know nothing aboutELF. The `fdio_spawn` function family knows how to turn an ELF and some initialstate into a running process. Zircon没有fork或exec。而是由fdio（/ zircon / system / ulib / fdio）提供进程创建。尽管Zircon具有Process和Thread对象，但这些对象很原始，对ELF一无所知。 fdio_spawn函数家族知道如何将ELF和一些初始状态转换为正在运行的进程。

 

