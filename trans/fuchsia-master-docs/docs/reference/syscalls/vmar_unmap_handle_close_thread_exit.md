 
# zx_vmar_unmap_handle_close_thread_exit  zx_vmar_unmap_handle_close_thread_exit 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Unmap memory, close handle, exit.  取消映射内存，关闭句柄，退出。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmar_unmap_handle_close_thread_exit(zx_handle_t vmar_handle,
                                                   zx_vaddr_t addr,
                                                   size_t size,
                                                   zx_handle_t close_handle);
```
 

 
## DESCRIPTION  描述 

`zx_vmar_unmap_handle_close_thread_exit()` does a sequence of three operations:  zx_vmar_unmap_handle_close_thread_exit（）执行一系列的三个操作：

 
1. `zx_vmar_unmap(vmar_handle, addr, size)`  1.`zx_vmar_unmap（vmar_handle，addr，size）`
2. `zx_handle_close(close_handle)`  2.`zx_handle_close（close_handle）`
3. `zx_thread_exit()`  3.`zx_thread_exit（）`

The expectation is that the first operation unmaps a region including the calling thread's own stack.  (It's not required, but it's permitted.)  Thisis valid for this call, though it would be invalid for [`zx_vmar_unmap()`] orany other call. 期望的是，第一个操作将取消映射包含调用线程自己的堆栈的区域。 （这不是必需的，但允许。）这对于此调用有效，尽管对[`zx_vmar_unmap（）]或其他任何调用都无效。

If the [`zx_vmar_unmap()`] operation is successful, then this call never returns. If *close_handle* is an invalid handle so that the [`zx_handle_close()`] operationfails, then the thread takes a trap (as if by `__builtin_trap();`). 如果[`zx_vmar_unmap（）`操作成功，则此调用永不返回。如果* close_handle *是无效的句柄，以致[`zx_handle_close（）`]操作失败，则线程将捕获一个陷阱（就像通过__builtin_trap（）;一样）。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_vmar_unmap_handle_close_thread_exit()` does not return on success.  zx_vmar_unmap_handle_close_thread_exit（）不会成功返回。

 
## ERRORS  错误 

Same as [`zx_vmar_unmap()`].  与[`zx_vmar_unmap（）`]相同。

 
## NOTES  笔记 

The intended use for this is for a dying thread to unmap its own stack, close its own thread handle, and exit.  The thread handle cannot be closedbeforehand because closing the last handle to a thread kills that thread.The stack cannot be unmapped beforehand because the thread must have somestack space on which to make its final system calls. 此操作的预期用途是使垂死的线程取消映射其自己的堆栈，关闭其自己的线程句柄并退出。无法关闭线程句柄，因为关闭线程的最后一个句柄会杀死该线程。无法预先取消映射堆栈，因为线程必须具有一定的堆栈空间才能进行最终系统调用。

This call is used for detached threads, while [`zx_futex_wake_handle_close_thread_exit()`]is used for joinable threads. 该调用用于分离的线程，而[`zx_futex_wake_handle_close_thread_exit（）`]用于可连接的线程。

 
## SEE ALSO  也可以看看 

 
 - [`zx_futex_wake_handle_close_thread_exit()`]  -[`zx_futex_wake_handle_close_thread_exit（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_thread_exit()`]  -[`zx_thread_exit（）`]
 - [`zx_vmar_unmap()`]  -[`zx_vmar_unmap（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

