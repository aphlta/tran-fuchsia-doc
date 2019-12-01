 
# Thread  线 

 
## NAME  名称 

thread - runnable / computation entity  线程-可运行/计算实体

 
## SYNOPSIS  概要 

TODO  去做

 
## DESCRIPTION  描述 

The thread object is the construct that represents a time-shared CPU execution context. Thread objects live associated to a particular[Process Object](process.md) which provides the memory and the handles to otherobjects necessary for I/O and computation. 线程对象是代表分时CPU执行上下文的构造。线程对象与特定的[Process Object]（process.md）相关联，该线程为I / O和计算所需的其他对象提供内存和句柄。

 
### Lifetime  一生Threads are created by calling [`zx_thread_create()`], but only start executing when either [`zx_thread_start()`] or [`zx_process_start()`] are called. Both syscallstake as an argument the entrypoint of the initial routine to execute. 线程是通过调用[`zx_thread_create（）]创建的，但是只有在调用[`zx_thread_start（）]或[`zx_process_start（）]时才开始执行。这两个系统调用都将要执行的初始例程的入口点作为参数。

The thread passed to [`zx_process_start()`] should be the first thread to start execution on a process. 传递给[`zx_process_start（）]的线程应该是开始在进程上执行的第一个线程。

A thread terminates execution:  线程终止执行：
+ by calling [`zx_thread_exit()`]  +通过调用[`zx_thread_exit（）`]
+ by calling [`zx_vmar_unmap_handle_close_thread_exit()`]  +通过调用[`zx_vmar_unmap_handle_close_thread_exit（）`]
+ by calling [`zx_futex_wake_handle_close_thread_exit()`]  +通过调用[`zx_futex_wake_handle_close_thread_exit（）`）
+ when the parent process terminates  +当父进程终止时
+ by calling [`zx_task_kill()`] with the thread's handle  +通过线程的句柄调用[`zx_task_kill（）`]
+ after generating an exception for which there is no handler or the handler decides to terminate the thread. +生成没有处理程序的异常或处理程序决定终止线程之后。

Returning from the entrypoint routine does not terminate execution. The last action of the entrypoint should be to call [`zx_thread_exit()`] or one of theabove mentioned `_exit()` variants. 从入口点例程返回不会终止执行。入口点的最后一个动作应该是调用[`zx_thread_exit（）`或上面提到的`_exit（）`变体之一。

Closing the last handle to a thread does not terminate execution. In order to forcefully kill a thread for which there is no available handle, use[`zx_object_get_child()`] to obtain a handle to the thread. This method is stronglydiscouraged. Killing a thread that is executing might leave the process in acorrupt state. 关闭线程的最后一个句柄不会终止执行。为了强制杀死没有可用句柄的线程，请使用[`zx_object_get_child（）`]获取该线程的句柄。强烈建议不要使用此方法。杀死正在执行的线程可能会使进程处于损坏状态。

Fuchsia native threads are always *detached*. That is, there is no *join()* operation needed to do a clean termination. However, some runtimes above the kernel, such asC11 or POSIX might require threads to be joined. 紫红色的本机线程始终是“分离的”。也就是说，不需要* join（）*操作即可执行干净终止。但是，某些高于内核的运行时，例如C11或POSIX，可能需要连接线程。

 
### Signals  讯号Threads provide the following signals:  线程提供以下信号：
+ `ZX_THREAD_TERMINATED`  +`ZX_THREAD_TERMINATED`
+ `ZX_THREAD_SUSPENDED`  +`ZX_THREAD_SUSPENDED`
+ `ZX_THREAD_RUNNING`  +`ZX_THREAD_RUNNING`

When a thread is started `ZX_THREAD_RUNNING` is asserted. When it is suspended `ZX_THREAD_RUNNING` is deasserted, and `ZX_THREAD_SUSPENDED` is asserted. Whenthe thread is resumed `ZX_THREAD_SUSPENDED` is deasserted and`ZX_THREAD_RUNNING` is asserted. When a thread terminates both`ZX_THREAD_RUNNING` and `ZX_THREAD_SUSPENDED` are deasserted and`ZX_THREAD_TERMINATED` is asserted. 当线程启动时，`ZX_THREAD_RUNNING`被声明。暂停时，`ZX_THREAD_RUNNING`被置为无效，并且`ZX_THREAD_SUSPENDED`被置为有效。当线程恢复时，`ZX_THREAD_SUSPENDED`被置为无效，并且`ZX_THREAD_RUNNING`被置为有效。当线程终止时，ZX_THREAD_RUNNING和ZX_THREAD_SUSPENDED都被置为无效，并且ZX_THREAD_TERMINATED被置为有效。

Note that signals are OR'd into the state maintained by the [`zx_object_wait_*()`](/docs/reference/syscalls/object_wait_one.md) family of functions thusyou may see any combination of requested signals when they return. 请注意，信号通过[[zx_object_wait _ *（）]]（/ docs / reference / syscalls / object_wait_one.md）函数族维护，因此返回时，您可能会看到请求信号的任何组合。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_thread_create()`] - create a new thread within a process  -[`zx_thread_create（）`]-在进程中创建新线程
 - [`zx_thread_exit()`] - exit the current thread  -[`zx_thread_exit（）`]-退出当前线程
 - [`zx_thread_read_state()`] - read register state from a thread  -[`zx_thread_read_state（）`]-从线程读取寄存器状态
 - [`zx_thread_start()`] - cause a new thread to start executing  -[`zx_thread_start（）`]-使新线程开始执行
 - [`zx_thread_write_state()`] - modify register state of a thread  -[`zx_thread_write_state（）`]-修改线程的寄存器状态

<br>  <br>

 
 - [`zx_task_create_exception_channel()`] - listen for task exceptions  -[`zx_task_create_exception_channel（）`]-监听任务异常
 - [`zx_task_kill()`] - cause a task to stop running  -[`zx_task_kill（）`]-导致任务停止运行

