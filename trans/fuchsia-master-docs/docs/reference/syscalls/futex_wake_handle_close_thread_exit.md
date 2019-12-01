 
# zx_futex_wake_handle_close_thread_exit  zx_futex_wake_handle_close_thread_exit 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Write to futex, wake futex, close handle, exit.  写入futex，唤醒futex，关闭句柄，退出。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

[[noreturn]] void zx_futex_wake_handle_close_thread_exit(
    const zx_futex_t* value_ptr,
    uint32_t wake_count,
    int32_t new_value,
    zx_handle_t close_handle);
```
 

 
## DESCRIPTION  描述 

`zx_futex_wake_handle_close_thread_exit()` does a sequence of four operations:  zx_futex_wake_handle_close_thread_exit（）执行一系列的四个操作：

 
1. `atomic_store_explicit(value_ptr, new_value, memory_order_release);`  1.`atomic_store_explicit（value_ptr，new_value，memory_order_release）;`
2. `zx_futex_wake(value_ptr, wake_count);`  2.`zx_futex_wake（value_ptr，wake_count）；`
3. `zx_handle_close(close_handle);`  3.`zx_handle_close（close_handle）;`
4. `zx_thread_exit();`  4.`zx_thread_exit（）;`

The expectation is that as soon as the first operation completes, other threads may unmap or reuse the memory containing the callingthread's own stack.  This is valid for this call, though it would beinvalid for plain [`zx_futex_wake()`] or any other call. 预期一旦第一个操作完成，其他线程可能会取消映射或重用包含调用线程自己的堆栈的内存。这对于此调用有效，尽管对纯[`zx_futex_wake（）`]或任何其他调用无效。

If any of the operations fail, then the thread takes a trap (as if by `__builtin_trap();`).  如果任何一个操作失败，那么线程将捕获一个陷阱（就像通过__builtin_trap（）;一样）。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_futex_wake_handle_close_thread_exit()` does not return.  zx_futex_wake_handle_close_thread_exit（）不返回。

 
## ERRORS  错误 

None.  没有。

 
## NOTES  笔记 

The intended use for this is for a dying thread to alert another thread waiting for its completion, close its own thread handle, and exit.The thread handle cannot be closed beforehand because closing the lasthandle to a thread kills that thread.  The write to *value_ptr* can't bedone before this call because any time after the write, a joining thread mightreuse or deallocate this thread's stack, which may cause issues with callingconventions into this function. 垂死的线程的预期用途是提醒另一个线程等待其完成，关闭其自己的线程句柄并退出。该线程句柄无法预先关闭，因为关闭线程的最后一个句柄会杀死该线程。在此调用之前无法对* value_ptr *进行写操作，因为在写操作之后的任何时间，连接线程都可能会重用或取消分配该线程的堆栈，这可能会导致在此函数中调用约定。

This call is used for joinable threads, while [`zx_vmar_unmap_handle_close_thread_exit()`]is used for detached threads. 该调用用于可连接线程，而[`zx_vmar_unmap_handle_close_thread_exit（）`]用于分离线程。

 
## SEE ALSO  也可以看看 

 
 - [futex objects](/docs/concepts/objects/futex.md)  -[futex对象]（/ docs / concepts / objects / futex.md）
 - [`zx_futex_wake()`]  -[`zx_futex_wake（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_thread_exit()`]  -[`zx_thread_exit（）`]
 - [`zx_vmar_unmap_handle_close_thread_exit()`]  -[`zx_vmar_unmap_handle_close_thread_exit（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

