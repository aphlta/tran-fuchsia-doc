 
# Zircon Kernel Concepts  锆石内核概念 

 
## Introduction  介绍 

The kernel manages a number of different types of Objects. Those which are accessible directly via system calls are C++ classes which implement theDispatcher interface. These are implemented in[kernel/object](/zircon/kernel/object). Many are self-contained higher-level Objects.Some wrap lower-level [lk](/docs/glossary.md#lk) primitives. 内核管理许多不同类型的对象。那些可以通过系统调用直接访问的是实现Dispatcher接口的C ++类。这些在[kernel / object]（/ zircon / kernel / object）中实现。许多是自包含的高级对象。有些包装了较低级的[lk]（/ docs / glossary.mdlk）原语。

 
## [System Calls](/docs/reference/syscalls/README.md)  [系统调用]（/ docs / reference / syscalls / README.md） 

Userspace code interacts with kernel objects via system calls, and almost exclusively via [Handles](/docs/concepts/objects/handles.md).  In userspace, a Handle is represented as32bit integer (type zx_handle_t).  When syscalls are executed, the kernel checksthat Handle parameters refer to an actual handle that exists within the callingprocess's handle table.  The kernel further checks that the Handle is of thecorrect type (passing a Thread Handle to a syscall requiring an event handlewill result in an error), and that the Handle has the required Rights for therequested operation. 用户空间代码通过系统调用与内核对象进行交互，并且几乎只能通过[Handles]（/ docs / concepts / objects / handles.md）进行交互。在用户空间中，句柄表示为32位整数（类型zx_handle_t）。当执行系统调用时，内核检查Handle参数是否引用了存在于调用过程的handle表中的实际句柄。内核进一步检查该句柄的类型是否正确（将线程句柄传递给需要事件句柄的syscall会导致错误），并且该句柄具有所请求操作的必需权限。

System calls fall into three broad categories, from an access standpoint:  从访问的角度来看，系统调用分为三大类：

 
1. Calls which have no limitations, of which there are only a very few, for example [`zx_clock_get()`](/docs/reference/syscalls/clock_get.md)and [`zx_nanosleep()`](/docs/reference/syscalls/nanosleep.md) may be called by any thread. 1.没有限制的呼叫，只有很少的呼叫，例如[`zx_clock_get（）`]（/ docs / reference / syscalls / clock_get.md）和[`zx_nanosleep（）`]（/ docs / reference / syscalls / nanosleep.md）可以由任何线程调用。
2. Calls which take a Handle as the first parameter, denoting the Object they act upon, which are the vast majority, for example [`zx_channel_write()`](/docs/reference/syscalls/channel_write.md)and [`zx_port_queue()`](/docs/reference/syscalls/port_queue.md). 2.以句柄为第一个参数的调用，表示要对其执行操作的对象，该调用占绝大多数，例如[`zx_channel_write（）`]（/ docs / reference / syscalls / channel_write.md）和[`zx_port_queue （）`]（/ docs / reference / syscalls / port_queue.md）。
3. Calls which create new Objects but do not take a Handle, such as [`zx_event_create()`](/docs/reference/syscalls/event_create.md) and[`zx_channel_create()`](/docs/reference/syscalls/channel_create.md).  Access to these (and limitationsupon them) is controlled by the Job in which the calling Process is contained. 3.创建新对象但不使用句柄的调用，例如[`zx_event_create（）`]（/ docs / reference / syscalls / event_create.md）和[`zx_channel_create（）`]（/ docs / reference / syscalls /channel_create.md）。对它们（及其限制）的访问由包含调用进程的Job控制。

System calls are provided by libzircon.so, which is a "virtual" shared library that the Zircon kernel provides to userspace, better known as the[*virtual Dynamic Shared Object* or vDSO](vdso.md).They are C ELF ABI functions of the form `zx_noun_verb()` or`zx_noun_verb_direct-object()`. 系统调用由libzircon.so提供，libzircon.so是Zircon内核提供给用户空间的“虚拟”共享库，通常称为[*虚拟动态共享对象*或vDSO]（vdso.md）。它们是C ELF ABI zx_noun_verb（）或zx_noun_verb_direct-object（）形式的函数。

The system calls are defined in a customized form of FIDL in [//zircon/syscalls](/zircon/syscalls/). Those definitions are first processed by `fidlc`, and then by `kazoo` which takes the IRrepresentation from `fidlc` and outputs various formats that are used as glue in the VDSO, kernel,etc. 系统调用以[// zircon / syscalls]（/ zircon / syscalls /）中FIDL的定制形式定义。这些定义首先由fidlc处理，然后由kazoo处理，后者从fidlc获取IR表示并输出在VDSO，内核等中用作粘合的各种格式。

 
## [Handles](/docs/concepts/objects/handles.md) and  [句柄]（/ docs / concepts / objects / handles.md）和[Rights](/docs/concepts/kernel/rights.md)  [权利]（/ docs / concepts / kernel / rights.md）

Objects may have multiple Handles (in one or more Processes) that refer to them.  对象可能有多个句柄（在一个或多个进程中）引用它们。

For almost all Objects, when the last open Handle that refers to an Object is closed, the Object is either destroyed, or put into a final state that may not be undone. 对于几乎所有对象，当最后一个引用对象的打开句柄关闭时，该对象要么被销毁，要么处于可能无法撤消的最终状态。

Handles may be moved from one Process to another by writing them into a Channel (using [`zx_channel_write()`](/docs/reference/syscalls/channel_write.md)), or by using[`zx_process_start()`](/docs/reference/syscalls/process_start.md) to pass a Handle as the argumentof the first thread in a new Process. 通过将句柄写入Channel（使用[`zx_channel_write（）`]（/ docs / reference / syscalls / channel_write.md））或使用[`zx_process_start（）`]（/ docs / reference / syscalls / process_start.md）传递一个Handle作为新Process中第一个线程的参数。

The actions which may be taken on a Handle or the Object it refers to are governed by the Rights associated with that Handle.  Two Handles that refer to the same Objectmay have different Rights. 在句柄或它所引用的对象上可能采取的动作受与该句柄关联的权利支配。引用同一对象的两个句柄可能具有不同的权限。

The [`zx_handle_duplicate()`](/docs/reference/syscalls/handle_duplicate.md) and [`zx_handle_replace()`](/docs/reference/syscalls/handle_replace.md) system calls may be used toobtain additional Handles referring to the same Object as the Handle passed in,optionally with reduced Rights.  The [`zx_handle_close()`](/docs/reference/syscalls/handle_close.md)system call closes a Handle, releasing the Object it refers to, if that Handle isthe last one for that Object. The [`zx_handle_close_many()`](/docs/reference/syscalls/handle_close_many.md)system call similarly closes an array of handles. [`zx_handle_duplicate（）`]（/ docs / reference / syscalls / handle_duplicate.md）和[`zx_handle_replace（）`]（/ docs / reference / syscalls / handle_replace.md）系统调用可用于获取其他引用的句柄与传入的句柄相同的对象，可以选择减少权限。 [`zx_handle_close（）`]（/ docs / reference / syscalls / handle_close.md）系统调用会关闭一个Handle，如果该Handle是该对象的最后一个，则释放它所引用的Object。 [`zx_handle_close_many（）`]（/ docs / reference / syscalls / handle_close_many.md）系统调用类似地关闭句柄数组。

 

 
## Kernel Object IDs  内核对象ID 

Every object in the kernel has a "kernel object id" or "koid" for short. It is a 64 bit unsigned integer that can be used to identify the objectand is unique for the lifetime of the running system.This means in particular that koids are never reused. 内核中的每个对象都有一个“内核对象ID”或“ koid”。它是一个64位无符号整数，可用于标识对象，并且在运行系统的生命周期中是唯一的，这尤其意味着永远不要重用koid。

There are two special koid values:  有两个特殊的koid值：

**ZX_KOID_INVALID** Has the value zero and is used as a "null" sentinel.  ** ZX_KOID_INVALID **的值为零，并用作“空”标记。

**ZX_KOID_KERNEL** There is only one kernel, and it has its own koid.  ** ZX_KOID_KERNEL **只有一个内核，并且有自己的内核。

Kernel generated koids only use 63 bits (which is plenty). This leaves space for artificially allocated koids by having the mostsignificant bit set. The sequence in which kernel generated koids are allocatedis unspecified and subject to change. 内核生成的koid仅使用63位（足够多）。通过设置最高位，可以为人为分配的koid留出空间。内核生成的类固醇分配的顺序不确定，并且可能会更改。

Artificial koids exist to support things like identifying artificial objects, like virtual threads in tracing, for consumption by tools.How artificial koids are allocated is left to each program,this document does not impose any rules or conventions. 存在人工虚构函数来支持诸如识别虚构对象（例如跟踪中的虚拟线程）之类的东西，以供工具使用。人工虚构体的分配方式留给每个程序，本文档没有施加任何规则或约定。

 

 
## Running Code: Jobs, Processes, and Threads.  运行代码：作业，进程和线程。 

Threads represent threads of execution (CPU registers, stack, etc) within an address space which is owned by the Process in which they exist.  Processes areowned by Jobs, which define various resource limitations.  Jobs are owned byparent Jobs, all the way up to the Root Job which was created by the kernel atboot and passed to [`userboot`, the first userspace Process to begin execution](/docs/concepts/booting/userboot.md). 线程表示存在它们的进程所拥有的地址空间内的执行线程（CPU寄存器，堆栈等）。流程归Jobs所有，这些流程定义了各种资源限制。作业一直由父作业拥有，一直到由内核atboot创建并传递给[`userboot`，这是开始执行的第一个用户空间进程]（/ docs / concepts / booting / userboot.md）的根作业。

Without a Job Handle, it is not possible for a Thread within a Process to create another Process or another Job. 如果没有作业句柄，则流程中的线程无法创建另一个流程或另一个作业。

[Program loading](/docs/concepts/booting/program_loading.md) is provided by userspace facilities and protocols above the kernel layer. [程序加载]（/ docs / concepts / booting / program_loading.md）由内核层以上的用户空间工具和协议提供。

See: [`zx_process_create()`](/docs/reference/syscalls/process_create.md), [`zx_process_start()`](/docs/reference/syscalls/process_start.md),[`zx_thread_create()`](/docs/reference/syscalls/thread_create.md),and [`zx_thread_start()`](/docs/reference/syscalls/thread_start.md). 参见：[`zx_process_create（）`]（/ docs / reference / syscalls / process_create.md），[`zx_process_start（）`]（/ docs / reference / syscalls / process_start.md），[`zx_thread_create（）`] [ /docs/reference/syscalls/thread_create.md）和[`zx_thread_start（）`]（/ docs / reference / syscalls / thread_start.md）。

 

 
## Message Passing: Sockets and Channels  消息传递：套接字和通道 

Both Sockets and Channels are IPC Objects which are bi-directional and two-ended. Creating a Socket or a Channel will return two Handles, one referring to each endpointof the Object. 套接字和通道都是双向和两端的IPC对象。创建一个套接字或一个通道将返回两个句柄，一个指向对象的每个端点。

Sockets are stream-oriented and data may be written into or read out of them in units of one or more bytes.  Short writes (if the Socket's buffers are full) and short reads(if more data is requested than in the buffers) are possible. 套接字是面向流的，数据可以以一个或多个字节为单位写入或读出。可以进行短写（如果Socket的缓冲区已满）和短读（如果请求的数据多于缓冲区）。

Channels are datagram-oriented and have a maximum message size given by **ZX_CHANNEL_MAX_MSG_BYTES**, and may also have up to **ZX_CHANNEL_MAX_MSG_HANDLES** Handles attached to a message.They do not support short reads or writes -- either a message fits or it does not. 通道是面向数据报的，并且最大消息大小由** ZX_CHANNEL_MAX_MSG_BYTES **给出，并且还可能具有最多** ZX_CHANNEL_MAX_MSG_HANDLES **消息句柄，它们不支持短读或写-消息适合或没有。

When Handles are written into a Channel, they are removed from the sending Process. When a message with Handles is read from a Channel, the Handles are added to the receivingProcess.  Between these two events, the Handles continue to exist (ensuring the Objectsthey refer to continue to exist), unless the end of the Channel which they have been writtentowards is closed -- at which point messages in flight to that endpoint are discarded andany Handles they contained are closed. 将句柄写入通道后，会将其从发送过程中删除。从通道读取带有句柄的消息时，句柄将添加到receiveProcess。在这两个事件之间，除非关闭了已写入它们的通道的末尾，否则句柄继续存在（确保它们所引用的Objects继续存在）-在该点处，传递到该端点的消息将被丢弃，并且将丢弃任何它们的句柄包含已关闭。

See: [`zx_channel_create()`](/docs/reference/syscalls/channel_create.md), [`zx_channel_read()`](/docs/reference/syscalls/channel_read.md),[`zx_channel_write()`](/docs/reference/syscalls/channel_write.md),[`zx_channel_call()`](/docs/reference/syscalls/channel_call.md),[`zx_socket_create()`](/docs/reference/syscalls/socket_create.md),[`zx_socket_read()`](/docs/reference/syscalls/socket_read.md),and [`zx_socket_write()`](/docs/reference/syscalls/socket_write.md). 参见：[`zx_channel_create（）`]（/ docs / reference / syscalls / channel_create.md），[`zx_channel_read（）`]（/ docs / reference / syscalls / channel_read.md），[`zx_channel_write（）`] [ /docs/reference/syscalls/channel_write.md),[`zx_channel_call()`](/docs/reference/syscalls/channel_call.md),[`zx_socket_create()`](/docs/reference/syscalls/socket_create.md ），[`zx_socket_read（）`]（/ docs / reference / syscalls / socket_read.md）和[`zx_socket_write（）`]（/ docs / reference / syscalls / socket_write.md）。

 
## Objects and Signals  物体和信号 

Objects may have up to 32 signals (represented by the zx_signals_t type and the ZX_*_SIGNAL_* defines) which represent a piece of information about their current state.  Channels and Sockets,for example, may be READABLE or WRITABLE.  Processes or Threads may be TERMINATED.  And so on. 对象最多可具有32个信号（由zx_signals_t类型和ZX _ * _ SIGNAL_ *定义表示），这些信号表示有关其当前状态的一条信息。例如，通道和套接字可以是READABLE或WRITABLE。进程或线程可能被终止。等等。

Threads may wait for signals to become active on one or more Objects.  线程可以等待信号在一个或多个对象上变为活动状态。

See [signals](/docs/concepts/kernel/signals.md) for more information.  有关更多信息，请参见[signals]（/ docs / concepts / kernel / signals.md）。

 
## Waiting: Wait One, Wait Many, and Ports  等待中：等待一个，等待多个和端口 

A Thread may use [`zx_object_wait_one()`](/docs/reference/syscalls/object_wait_one.md) to wait for a signal to be active on a single handle or[`zx_object_wait_many()`](/docs/reference/syscalls/object_wait_many.md) to wait forsignals on multiple handles.  Both calls allow for a timeout afterwhich they'll return even if no signals are pending. 线程可以使用[`zx_object_wait_one（）`]（/ docs / reference / syscalls / object_wait_one.md）等待信号在单个句柄上处于活动状态，或[[zx_object_wait_many（）`]（/ docs / reference / syscalls /object_wait_many.md）以等待多个句柄上的信号。这两个调用都允许超时，即使没有信号挂起，它们也会返回。

Timeouts may deviate from the specified deadline according to timer slack. See [timer slack](/docs/concepts/objects/timer_slack.md) for more information. 超时可能会由于计时器松弛而偏离指定的期限。有关更多信息，请参见[timer slack]（/ docs / concepts / objects / timer_slack.md）。

If a Thread is going to wait on a large set of handles, it is more efficient to use a Port, which is an Object that other Objects may be bound to such that when signalsare asserted on them, the Port receives a packet containing information about thepending Signals. 如果线程要等待大量的句柄，使用端口是更有效的方法，该端口是其他对象可能绑定的对象，这样当在它们上声明信号时，端口会收到一个包含以下信息的包：待处理信号。

See: [`zx_port_create()`](/docs/reference/syscalls/port_create.md), [`zx_port_queue()`](/docs/reference/syscalls/port_queue.md),[`zx_port_wait()`](/docs/reference/syscalls/port_wait.md),and [`zx_port_cancel()`](/docs/reference/syscalls/port_cancel.md). 请参阅：[`zx_port_create（）`]（/ docs / reference / syscalls / port_create.md），[`zx_port_queue（）`]（/ docs / reference / syscalls / port_queue.md），[`zx_port_wait（）`]（ /docs/reference/syscalls/port_wait.md）和[`zx_port_cancel（）`]（/ docs / reference / syscalls / port_cancel.md）。

 

 
## Events, Event Pairs.  事件，事件对。 

An Event is the simplest Object, having no other state than its collection of active Signals.  事件是最简单的对象，除了其活动信号的集合外没有其他状态。

An Event Pair is one of a pair of Events that may signal each other.  A useful property of Event Pairs is that when one side of a pair goes away (all Handles to it have beenclosed), the PEER_CLOSED signal is asserted on the other side. 事件对是可能会相互发出信号的一对事件中的一个。事件对的一个有用属性是，当一对的一侧消失（对它的所有句柄都已关闭）时，PEER_CLOSED信号在另一侧被声明。

See: [`zx_event_create()`](/docs/reference/syscalls/event_create.md), and [`zx_eventpair_create()`](/docs/reference/syscalls/eventpair_create.md). 请参阅：[`zx_event_create（）`]（/ docs / reference / syscalls / event_create.md）和[`zx_eventpair_create（）`]（/ docs / reference / syscalls / eventpair_create.md）。

 

 
## Shared Memory: Virtual Memory Objects (VMOs)  共享内存：虚拟内存对象（VMO） 

Virtual Memory Objects represent a set of physical pages of memory, or the *potential* for pages (which will be created/filled lazily, on-demand). 虚拟内存对象代表一组物理内存页面，或页面的“潜在*”（将按需延迟创建/填充）。

They may be mapped into the address space of a Process with [`zx_vmar_map()`](/docs/reference/syscalls/vmar_map.md) and unmapped with[`zx_vmar_unmap()`](/docs/reference/syscalls/vmar_unmap.md).  Permissions ofmapped pages may be adjusted with [`zx_vmar_protect()`](/docs/reference/syscalls/vmar_protect.md). 可以使用[`zx_vmar_map（）`]（/ docs / reference / syscalls / vmar_map.md）将它们映射到进程的地址空间，并使用[`zx_vmar_unmap（）`]（/ docs / reference / syscalls / vmar_unmap .md）。映射页面的权限可以通过[`zx_vmar_protect（）`]（/ docs / reference / syscalls / vmar_protect.md）进行调整。

VMOs may also be read from and written to directly with [`zx_vmo_read()`](/docs/reference/syscalls/vmo_read.md) and [`zx_vmo_write()`](/docs/reference/syscalls/vmo_write.md).Thus the cost of mapping them into an address space may be avoided for one-shot operationslike "create a VMO, write a dataset into it, and hand it to another Process to use." 也可以通过[`zx_vmo_read（）`]（/ docs / reference / syscalls / vmo_read.md）和[`zx_vmo_write（）`]（/ docs / reference / syscalls / vmo_write.md）读取和直接写入VMO。因此，可以避免像“创建VMO，将数据集写入其中，并将其交给另一个进程使用”这样的一次性操作将它们映射到地址空间中的开销。

 
## Address Space Management  地址空间管理 

Virtual Memory Address Regions (VMARs) provide an abstraction for managing a process's address space.  At process creation time, a handle to the root VMARis given to the process creator.  That handle refers to a VMAR that spans theentire address space.  This space can be carved up via the[`zx_vmar_map()`](/docs/reference/syscalls/vmar_map.md) and[`zx_vmar_allocate()`](/docs/reference/syscalls/vmar_allocate.md) interfaces.[`zx_vmar_allocate()`](/docs/reference/syscalls/vmar_allocate.md) can be used to generate newVMARs (called subregions or children) which can be used to group togetherparts of the address space. 虚拟内存地址区域（VMAR）提供了用于管理进程地址空间的抽象。在流程创建时，会将根VMAR的句柄提供给流程创建者。该句柄是指跨越整个地址空间的VMAR。该空间可以通过[`zx_vmar_map（）`]（/ docs / reference / syscalls / vmar_map.md）和[`zx_vmar_allocate（）`]（/ docs / reference / syscalls / vmar_allocate.md）接口进行划分。 zx_vmar_allocate（）]（/ docs / reference / syscalls / vmar_allocate.md）可用于生成新的VMAR（称为子区域或子区域），可用于将地址空间的各个部分组合在一起。

See: [`zx_vmar_map()`](/docs/reference/syscalls/vmar_map.md), [`zx_vmar_allocate()`](/docs/reference/syscalls/vmar_allocate.md),[`zx_vmar_protect()`](/docs/reference/syscalls/vmar_protect.md),[`zx_vmar_unmap()`](/docs/reference/syscalls/vmar_unmap.md),and [`zx_vmar_destroy()`](/docs/reference/syscalls/vmar_destroy.md), 参见：[`zx_vmar_map（）`]（/ docs / reference / syscalls / vmar_map.md），[`zx_vmar_allocate（）`]（/ docs / reference / syscalls / vmar_allocate.md），[`zx_vmar_protect（）`]（ /docs/reference/syscalls/vmar_protect.md)、[`zx_vmar_unmap()`](/docs/reference/syscalls/vmar_unmap.md）和[`zx_vmar_destroy（）`]（/ docs / reference / syscalls / vmar_destroy。 md），

 
## Futexes  熔岩 

Futexes are kernel primitives used with userspace atomic operations to implement efficient synchronization primitives -- for example, Mutexes which only need to makea syscall in the contended case.  Usually they are only of interest to implementers ofstandard libraries.  Zircon's libc and libc++ provide C11, C++, and pthread APIs formutexes, condition variables, etc, implemented in terms of Futexes. Futex是与用户空间原子操作一起使用的内核原语，用于实现有效的同步原语-例如，互斥量（Mutex），在竞争情况下仅需要进行syscall。通常，它们仅对标准库的实现者有意义。 Zircon的libc和libc ++为Muttex，条件变量等提供了基于Futex的C11，C ++和pthread API。

