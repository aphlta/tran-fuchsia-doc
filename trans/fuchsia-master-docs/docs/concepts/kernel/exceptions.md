 
# Exception Handling  异常处理 

 
## Introduction  介绍 

When a thread encounters a fault condition, for example a segfault, execution is paused and the thread enters exception handling. Handlers which haveregistered to receive these exceptions are notified and given a chance toinspect or correct the condition. 当线程遇到故障情况（例如segfault）时，执行将暂停，线程将进入异常处理。将通知已注册接收这些异常的处理程序，并为他们提供检查或纠正条件的机会。

This functionality is commonly used by debuggers or crash loggers, which want to have a chance to interact with threads before they would otherwise crash.For applications that just want to track task lifecycles without needing tointercept crashes, [signals](signals.md) may be a better choice. 调试器或崩溃记录器通常使用此功能，它们希望在线程崩溃之前有机会与线程进行交互。对于只想跟踪任务生命周期而无需拦截崩溃的应用程序，[signals]（signals.md）可能成为更好的选择。

 
## The Basics  基础 

Exceptions are handled from userspace by creating an exception channel on a task (thread, process, or job) with the [`zx_task_create_exception_channel()`]system call. The created handle is a standard Zircon[channel](/docs/concepts/objects/channel.md), but is created read-only so can only be usedfor receiving exception messages. 通过使用[`zx_task_create_exception_channel（）`]系统调用在任务（线程，进程或作业）上创建异常通道，可以从用户空间处理异常。创建的句柄是标准的Zircon [channel]（/ docs / concepts / objects / channel.md），但创建为只读，因此只能用于接收异常消息。

When an exception occurs, the thread is paused and a message containing a `zx_exception_info_t` and an exception handle is sent to the channel. Thelifetime of the exception is bound to the lifetime of this exception handle, sowhen the receiver is done processing, closing this exception handle will resumethe exception. This exception handle is non-copyable, meaning that at any giventime, there is only one handler for this exception. 当发生异常时，线程被暂停，并且包含`zx_exception_info_t'和异常句柄的消息被发送到通道。异常的生存期与该异常句柄的生存期绑定，因此当接收器完成处理后，关闭此异常句柄将恢复该异常。此异常句柄是不可复制的，这意味着在任何给定时间，此异常只有一个处理程序。

By default, closing an exception handle will keep the thread paused and send the exception to the next handler. If the receiver has corrected the exceptionand wants the thread to resume execution instead, it can change the exceptionstate to `ZX_EXCEPTION_STATE_HANDLED` via [`zx_object_set_property()`] beforeclosing. 默认情况下，关闭异常句柄将使线程暂停，并将异常发送到下一个处理程序。如果接收者已经纠正了异常并希望线程恢复执行，则可以在关闭前通过[`zx_object_set_property（）]将异常状态更改为`ZX_EXCEPTION_STATE_HANDLED`。

 
## Exception Handles  异常处理 

Exception handles behave similarly to suspend tokens by keeping the thread paused until they are closed. Additionally, exception handles have functionsto help receivers process the exception: 异常句柄的行为类似于暂停令牌，方法是保持线程暂停直到关闭它们。此外，异常句柄具有帮助接收者处理异常的功能：

 
* [`zx_object_set_property()`] with `ZX_PROP_EXCEPTION_STATE` to set behavior on handle close * [`zx_object_set_property（）`和`ZX_PROP_EXCEPTION_STATE`用于设置句柄关闭的行为
* [`zx_exception_get_thread()`] to get a handle to the exception thread  * [`zx_exception_get_thread（）`]获取异常线程的句柄
* [`zx_exception_get_process()`] to get a handle to the exception process (process or job exception channels only) * [`zx_exception_get_process（）`]获取异常处理的句柄（仅用于处理或作业异常通道）

Task handles retrieved from exceptions will have the same rights as the task originally passed into [`zx_task_create_exception_channel()`]. 从异常中检索的任务句柄将具有与最初传递给[`zx_task_create_exception_channel（）`]的任务相同的权限。

 
### Example  例 

This simple example creates an exception channel and loops reading exceptions until the task closes. 这个简单的示例创建一个异常通道并循环读取异常，直到任务关闭。

```cpp
void ExceptionHandlerLoop(zx_handle_t task) {
  // Create the exception channel.
  uint32_t options = 0;
  zx_handle_t channel;
  zx_status_t status = zx_task_create_exception_channel(task, options,
                                                        &channel);
  // ... check status ...

  while (true) {
    // Wait until we get ZX_CHANNEL_READABLE (exception) or
    // ZX_CHANNEL_PEER_CLOSED (task terminated).
    zx_signals_t signals = 0;
    status = zx_object_wait_one(channel,
                                ZX_CHANNEL_READABLE | ZX_CHANNEL_PEER_CLOSED,
                                ZX_TIME_INFINITE, &signals);
    // ... check status ...

    if (signals & ZX_CHANNEL_READABLE) {
      // Read the exception info and handle from the channel.
      zx_exception_info_t info;
      zx_handle_t exception;
      status = zx_channel_read(channel, 0, &info, &exception, sizeof(info), 1,
                               nullptr, nullptr);
      // ... check status ...

      // Send the exception out to some other function for processing, which
      // returns true if the exception has been handled and we can resume the
      // thread, or false to pass the exception to the next handler.
      bool handled = process_exception(info, exception);
      if (handled) {
        uint32_t state = ZX_EXCEPTION_STATE_HANDLED;
        status = zx_object_set_property(exception, ZX_PROP_EXCEPTION_STATE,
                                        &state, sizeof(state));
        // ... check status ...
      }

      // Close the exception to finish handling.
      zx_handle_close(exception);
    } else {
      // We got ZX_CHANNEL_PEER_CLOSED, the task has terminated.
      zx_handle_close(channel);
      return;
    }
  }
}
```
 

 
## Exception Types  异常类型 

At a high level there are two types of exceptions: architectural and synthetic. Architectural exceptions are things like a segfault (e.g., dereferencing theNULL pointer) or executing an undefined instruction. Synthetic exceptions arethings like thread start/stop notifications or[policy violations](/docs/reference/syscalls/job_set_policy.md). 从总体上讲，有两种例外类型：建筑例外和综合例外。架构异常是诸如段错误（例如，取消引用NULL指针）或执行未定义指令之类的事情。合成异常是诸如线程启动/停止通知或[违反策略]（/ docs / reference / syscalls / job_set_policy.md）之类的东西。

Architectural and policy exceptions are considered fatal, and will cause the process to be killed if they are unhandled. Debugger-only exceptions - threadstart/stop and process start - are informational and will continue executionnormally even if the thread isn't explicitly resumed. These exceptions aremeant to give a debugger a chance to react to these lifetime events correctly,as the corresponding thread will be paused until the exception is resumed. 体系结构和策略异常被认为是致命的，如果不加以处理，将导致该流程被终止。仅调试程序的异常（线程启动/停止和进程启动）是信息性的，即使未明确恢复线程，该异常也将正常继续执行。这些异常旨在使调试器有机会正确响应这些生存期事件，因为相应的线程将被暂停，直到恢复异常为止。

Exception types are defined in [`<zircon/syscalls/exception.h>`](/zircon/system/public/zircon/syscalls/exception.h). 异常类型在[`<zircon / syscalls / exception.h>`]（/ zircon / system / public / zircon / syscalls / exception.h）中定义。

 
## Exception Channel Types  异常通道类型 

Exception channels have different characteristics depending on the task type and whether the `ZX_EXCEPTION_CHANNEL_DEBUGGER` flag is passed to[`zx_task_create_exception_channel()`]. The table below summarizes thedifferences between the various channel types: 异常通道具有不同的特征，具体取决于任务类型以及是否将ZX_EXCEPTION_CHANNEL_DEBUGGER标志传递给[zx_task_create_exception_channel（）]。下表总结了各种通道类型之间的差异：

Channel Type  | `get_thread` | `get_process` | Architectural & Policy Exceptions | Thread Start/Stop Exceptions | Process Start Exception ------------- | :----------: | :-----------: | :-------------------------------: | :--------------------------: | :---------------------:Thread        | X            |               | X                                 |                              |Process       | X            | X             | X                                 |                              |Process Debug | X            | X             | X                                 | X                            |Job           | X            | X             | X                                 |                              |Job Debug     | X            | X             |                                   |                              | X 频道类型| `get_thread` | `get_process` |建筑政策例外|线程启动/停止异常|进程启动异常------------- | ：----------：| ：-----------：| ：-------------------------------：| ：--------------------------：| ：---------------------：线程| X | | X | |工艺| X | X | X | |过程调试| X | X | X | X |工作| X | X | X | |作业调试| X | X | | | X

The channel type also determines the order in which exception channels will be given the chance to handle an exception: 通道类型还确定给予异常通道处理异常机会的顺序：

 
1. process debug  1.流程调试
2. thread  2.线程
3. process  3.过程
4. job (parent job -> grandparent job -> etc)  4.工作（父工作->祖父母工作->等）

If there are no remaining exception channels to try, the kernel terminates the process as if [`zx_task_kill()`] was called. The return code of a processterminated by an exception is `ZX_TASK_RETCODE_EXCEPTION_KILL`, and can beobtained with [`zx_object_get_info()`] using `ZX_INFO_PROCESS`. 如果没有其他可尝试的异常通道，则内核将终止进程，就像调用[`zx_task_kill（）`]一样。由异常终止的进程的返回码为`ZX_TASK_RETCODE_EXCEPTION_KILL`，并且可以使用``ZX_INFO_PROCESS`通过[`zx_object_get_info（）`]获取。

Each task only supports a single exception channel per type, so for example given a process with a debug exception channel attached, trying to createa second debug exception channel will fail, but creating a non-debug channelwill succeed. 每个任务每个类型仅支持一个异常通道，因此，例如，给定一个附加了调试异常通道的进程，尝试创建第二个调试异常通道将失败，但是创建非调试通道将成功。

 
### `ZX_EXCP_PROCESS_STARTING` and Job Debugger Channels  ZX_EXCP_PROCESS_STARTING和作业调试器通道 

The `ZX_EXCP_PROCESS_STARTING` behaves differently than other exceptions. It is only sent to job debugger exception channels, and is only sent to thefirst found handler, essentially assuming `ZX_EXCEPTION_STATE_HANDLED`regardless of actual handler behavior. This is also the only exception thatjob debugger channels receive, making them a special-case handler for justdetecting new processes. ZX_EXCP_PROCESS_STARTING的行为与其他异常不同。它仅被发送到作业调试器异常通道，并且仅被发送到第一个找到的处理程序，实质上假定“ ZX_EXCEPTION_STATE_HANDLED”与实际的处理程序行为无关。这也是作业调试器通道收到的唯一例外，这使它们成为仅检测新进程的特殊情况处理程序。

 
### Process Debugger First  流程调试器优先 

In Zircon the process debugger exception channel is tried first. This is useful for at least a few reasons: 在Zircon中，首先尝试过程调试器异常通道。至少出于以下几个原因，这很有用：

 
- Allows "fix and continue" debugging, e.g. if a thread gets a segfault, the debugger user can fix the segfault and resume the thread without anynon-debugger channels seeing the exception. -允许“修复并继续”调试，例如如果线程遇到段错误，调试器用户可以修复段错误并继续执行线程，而没有任何非调试程序通道会看到异常。
- Ensures debugger breakpoints get sent directly to the debugger without other handlers having to explicitly pass them along. -确保将调试器断点直接发送到调试器，而无需其他处理程序将其明确传递。

 
## Interaction with Task Suspension  与任务暂停的交互 

Exceptions and thread suspensions are treated separately. In other words, a thread can be both in an exception and be suspended.This can happen if the thread is suspended while waiting for a responsefrom an exception handler. The thread stays paused until it is resumedfor both the exception and the suspension: 异常和线程挂起分别处理。换句话说，线程可以同时处于异常状态和被挂起，如果线程在等待异常处理程序的响应时被挂起，则会发生这种情况。线程保持暂停状态，直到针对异常和挂起都恢复运行：

```cpp
zx_handle_close(exception);
zx_handle_close(suspend_token);
```
 

The order does not matter.  顺序无关紧要。

 
## Interaction with Task Kill  与任务杀死的互动 

[`zx_task_kill()`] stops any exception handling on the task. If it is called on a thread (or its parent process/jobs) while the thread is in an exception: [`zx_task_kill（）`]停止任务上的任何异常处理。如果在线程处于异常中时在线程（或其父进程/作业）上调用它：

 
- the thread will stop waiting for the current exception handler  -线程将停止等待当前的异常处理程序
- no further exception handlers will receive the exception  -没有其他的异常处理程序会收到异常
- [`zx_exception_get_thread()`] and [`zx_exception_get_process()`] on the outstanding exception handle will continue to provide valid task handles -未完成的异常句柄上的[`zx_exception_get_thread（）`]和[`zx_exception_get_process（）`]将继续提供有效的任务句柄
- [`zx_object_set_property()`] to set the exception's state will still return `ZX_OK`, though the state won't have any effect since the thread is no longerblocking on the handler -设置异常状态的[zx_object_set_property（）]仍将返回ZX_OK，尽管该状态不会产生任何影响，因为线程不再在处理程序上阻塞

Additionally, a killed thread will still send a `ZX_EXCP_THREAD_EXITING` exception (if a process debug handler is registered), but as above will notwait for a response from the handler. 此外，被杀死的线程仍将发送ZX_EXCP_THREAD_EXITING异常（如果已注册进程调试处理程序），但是如上所述，它不会等待处理程序的响应。

Although [`zx_task_kill()`] is generally asynchronous, meaning the thread may not finish terminating by the time the syscall returns, it does synchronouslystop exception handling such that once it returns, closing an exception handlewill not resume the thread or pass the exception to another handler. 虽然[`zx_task_kill（）`]通常是异步的，这意味着线程可能无法在系统调用返回时完成终止，但它会同步停止异常处理，以便一旦返回，关闭异常句柄将不会继续线程或将异常传递给另一个处理程序。

 
## Signals  讯号 

[Signals](signals.md) are the core Zircon mechanism for observing state changes on kernel objects (a channel becoming readable, a process terminating, an eventbecoming signaled, etc). [Signals]（signals.md）是Zircon的核心机制，用于观察内核对象的状态变化（通道变得可读，进程终止，事件已发出信号等）。

Unlike exceptions, signals do not require a response from an exception handler. On the other hand signals are sent to whomever is waiting on the thread'shandle, instead of being sent to the exception channel that could be bound tothe thread's process. 与异常不同，信号不需要异常处理程序的响应。另一方面，将信号发送给正在线程线程等待的任何人，而不是将其发送到可能绑定到线程进程的异常通道。

A common pattern in Zircon is to have a message loop that waits for signals on one or more objects and handles them as they come in. To incorporate exceptionhandling into this pattern, use [`zx_object_wait_async()`] to wait for`ZX_CHANNEL_READABLE` (and optionally `ZX_CHANNEL_PEER_CLOSED`) on theexception channel: Zircon中的一种常见模式是有一个消息循环，等待一个或多个对象上的信号并在它们进入时对其进行处理。要将异常处理合并到此模式中，请使用[`zx_object_wait_async（）`]等待`ZX_CHANNEL_READABLE（（以及可选的异常通道上的“ ZX_CHANNEL_PEER_CLOSED”）：

```cpp
zx_handle_t port;
zx_status_t status = zx_port_create(0, &port);
// ... check status ...

// Start waiting on relevant signals on the exception channel.
status = zx_object_wait_async(exception_channel, port, kMyExceptionKey,
                              ZX_CHANNEL_READABLE | ZX_CHANNEL_PEER_CLOSED, 0);
// ... check status ...

// ... add other objects to |port| with wait_async() ...

while (1) {
  zx_port_packet_t packet;
  status = zx_port_wait(port, ZX_TIME_INFINITE, &packet);
  // ... check status ...

  if (packet.key == kMyExceptionKey) {
    if (packet.signal.observed & ZX_CHANNEL_READABLE) {
      // ... extract exception from |exception_channel| and process it ...

      // wait_async() is one-shot so we need to reload it to continue
      // receiving signals.
      status = zx_object_wait_async(
          exception_channel, port, kMyExceptionKey,
          ZX_CHANNEL_READABLE | ZX_CHANNEL_PEER_CLOSED, 0);
      // ... check status ...
    } else {
      // Got ZX_CHANNEL_PEER_CLOSED, task has terminated.
      zx_handle_close(exception_channel);
    }
  } else {
    // ... handle other objects added to |port| ...
  }
}
```
 

Note: There is both an exception and a signal for thread termination. The `ZX_EXCP_THREAD_EXITING` exception is sent first. When the thread is finallyterminated the `ZX_THREAD_TERMINATED` signal is set. 注意：线程终止有一个例外和一个信号。首先发送“ ZX_EXCP_THREAD_EXITING”异常。当线程最终终止时，将设置“ ZX_THREAD_TERMINATED”信号。

 
## Comparison with Posix (and Linux)  与Posix（和Linux）比较 

This table shows equivalent terms, types, and function calls between Zircon and Posix/Linux for exceptions and the kinds of things exceptionhandlers generally do. 下表显示了Zircon和Posix / Linux之间针对异常以及异常处理程序通常执行的操作的等效术语，类型和函数调用。

Zircon                             | Posix/Linux ------                             | -----------Exception/Signal                   | SignalZX_EXCP_*                          | SIG*zx_task_create_exception_channel() | ptrace(ATTACH,DETACH)zx_task_suspend()                  | kill(SIGSTOP),ptrace(KILL(SIGSTOP))zx_handle_close(suspend_token)     | kill(SIGCONT),ptrace(CONT)zx_handle_close(exception)         | kill(SIGCONT),ptrace(CONT)zx_task_kill()                     | kill(SIGKILL)N/A                                | kill(everything_else)TBD                                | signal()/sigaction()zx_port_wait()                     | wait*()various                            | W*() macros from sys/wait.hzx_exception_info_t                | siginfo_tzx_exception_context_t             | siginfo_tzx_thread_read_state()             | ptrace(GETREGS,GETREGSET)zx_thread_write_state()            | ptrace(SETREGS,SETREGSET)zx_process_read_memory()           | ptrace(PEEKTEXT)zx_process_write_memory()          | ptrace(POKETEXT) 锆石| Posix / Linux ------ | -----------异常/信号| SignalZX_EXCP_ * | SIG * zx_task_create_exception_channel（）| ptrace（ATTACH，DETACH）zx_task_suspend（）| kill（SIGSTOP），ptrace（KILL（SIGSTOP））zx_handle_close（suspend_token）| kill（SIGCONT），ptrace（CONT）zx_handle_close（异常）| kill（SIGCONT），ptrace（CONT）zx_task_kill（）|杀死（SIGKILL）不适用|杀死（everything_else）TBD | signal（）/ sigaction（）zx_port_wait（）|等待*（）各种|来自sys / wait.hzx_exception_info_t的W *（）宏| siginfo_tzx_exception_context_t | siginfo_tzx_thread_read_state（）| ptrace（GETREGS，GETREGSET）zx_thread_write_state（）| ptrace（SETREGS，SETREGSET）zx_process_read_memory（）| ptrace（PEEKTEXT）zx_process_write_memory（）| ptrace（POKETEXT）

Zircon does not have asynchronous signals like `SIGINT`, `SIGQUIT`, `SIGTERM`, `SIGUSR1`, `SIGUSR2`, and so on. Zircon没有异步信号，例如SIGINT，SIGQUIT，SIGTERM，SIGUSR1，SIGUSR2等。

Another significant difference from Posix is that in Zircon a thread cannot handle its own exceptions, since Zircon exception handling is a synchronousoperation driven by userspace rather than an asynchronous callback invoked bythe kernel. 与Posix的另一个重要区别是，在Zircon中，线程无法处理其自身的异常，因为Zircon异常处理是由用户空间驱动的同​​步操作，而不是内核调用的异步回调。

 
## Examples  例子 

Zircon code that uses exceptions can be viewed for further examples, including:  可以查看使用异常的Zircon代码以获取更多示例，包括：

 
- `system/core/svchost/crashsvc`: system-level crash handler  -`system / core / svchost / crashsvc`：系统级崩溃处理程序
- `system/utest/exception`: exception unit tests  -`system / utest / exception`：异常单元测试
- `system/utest/debugger`: debugger-related functionality unit tests  -`system / utest / debugger`：与调试器相关的功能单元测试

 
## See Also  也可以看看 

 
- [`zx_task_create_exception_channel()`]  -[`zx_task_create_exception_channel（）`]
- [`zx_exception_get_thread()`]  -[`zx_exception_get_thread（）`]
- [`zx_exception_get_process()`]  -[`zx_exception_get_process（）`]
- [`zx_object_set_property()`]  -[`zx_object_set_property（）`]
- [`zx_port_wait()`]  -[`zx_port_wait（）`]

