 
# zx_thread_start  zx_thread_start 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Start execution on a thread.  开始在线程上执行。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_thread_start(zx_handle_t handle,
                            zx_vaddr_t thread_entry,
                            zx_vaddr_t stack,
                            uintptr_t arg1,
                            uintptr_t arg2);
```
 

 
## DESCRIPTION  描述 

`zx_thread_start()` causes a thread to begin execution at the program counter specified by *thread_entry* and with the stack pointer set to *stack*. Thearguments *arg1* and *arg2* are arranged to be in the architecture specificregisters used for the first two arguments of a function call before the threadis started.  All other registers are zero upon start. zx_thread_start（）导致线程在* thread_entry *指定的程序计数器处开始执行，并且堆栈指针设置为* stack *。参数* arg1 *和* arg2 *安排在特定于体系结构的寄存器中，该寄存器用于在线程启动之前用于函数调用的前两个参数。启动时所有其他寄存器均为零。

When the last handle to a thread is closed, the thread is destroyed.  当关闭线程的最后一个句柄时，该线程将被销毁。

Thread handles may be waited on and will assert the signal **ZX_THREAD_TERMINATED** when the thread stops executing (due to[`zx_thread_exit()`] being called). 线程句柄可以等待，并在线程停止执行（由于调用[`zx_thread_exit（）]）时断言信号** ZX_THREAD_TERMINATED **。

*thread_entry* shall point to a function that must call [`zx_thread_exit()`] or [`zx_futex_wake_handle_close_thread_exit()`] or[`zx_vmar_unmap_handle_close_thread_exit()`] before reaching the last instruction.Below is an example: * thread_entry *指向必须在到达最后一条指令之前必须调用[`zx_thread_exit（）]或[`zx_futex_wake_handle_close_thread_exit（）]或[`zx_vmar_unmap_handle_close_thread_exit（）`的函数。下面是一个示例：

```
void thread_entry(uintptr_t arg1, uintptr_t arg2) __attribute__((noreturn)) {
	// do work here.

	zx_thread_exit();
}
```
 

Failing to call one of the exit functions before reaching the end of the function will cause an architecture / toolchain specific exception. 在到达函数结束之前未能调用退出函数之一将导致特定于体系结构/工具链的异常。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_THREAD** and have **ZX_RIGHT_MANAGE_THREAD**.  *句柄*必须为** ZX_OBJ_TYPE_THREAD **类型，并具有** ZX_RIGHT_MANAGE_THREAD **。

 
## RETURN VALUE  返回值 

`zx_thread_start()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_thread_start（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *thread* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *线程*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *thread* is not a thread handle.  ** ZX_ERR_WRONG_TYPE ** * thread *不是线程句柄。

**ZX_ERR_ACCESS_DENIED**  The handle *thread* lacks **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED **句柄* thread *缺少** ZX_RIGHT_WRITE **。

**ZX_ERR_BAD_STATE**  *thread* is not ready to run or the process *thread* is part of is no longer alive. ** ZX_ERR_BAD_STATE ** *线程*尚未准备好运行，或者*线程*所在的进程不再活跃。

 
## SEE ALSO  也可以看看 

 
 - [`zx_futex_wake_handle_close_thread_exit()`]  -[`zx_futex_wake_handle_close_thread_exit（）`]
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]
 - [`zx_thread_create()`]  -[`zx_thread_create（）`]
 - [`zx_thread_exit()`]  -[`zx_thread_exit（）`]
 - [`zx_vmar_unmap_handle_close_thread_exit()`]  -[`zx_vmar_unmap_handle_close_thread_exit（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

