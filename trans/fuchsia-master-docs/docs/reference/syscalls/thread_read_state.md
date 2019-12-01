 
# zx_thread_read_state  zx_thread_read_state 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Read one aspect of thread state.  阅读线程状态的一方面。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_thread_read_state(zx_handle_t handle,
                                 uint32_t kind,
                                 void* buffer,
                                 size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

`zx_thread_read_state()` reads one aspect of state of the thread. The thread state may only be read when the thread is halted for an exception or the threadis suspended. zx_thread_read_state（）读取线程状态的一方面。仅当线程因异常而暂停或线程被挂起时，才可以读取线程状态。

The thread state is highly processor specific. See the structures in zircon/syscalls/debug.h for the contents of the structures on each platform. 线程状态是高度特定于处理器的。有关每个平台上结构的内容，请参见zircon / syscalls / debug.h中的结构。

 
## STATES  状态 

 
### ZX_THREAD_STATE_GENERAL_REGS  ZX_THREAD_STATE_GENERAL_REGS 

The buffer must point to a `zx_thread_state_general_regs_t` structure that contains the general registers for the current architecture. 缓冲区必须指向包含当前架构通用寄存器的zx_thread_state_general_regs_t结构。

 
### ZX_THREAD_STATE_FP_REGS  ZX_THREAD_STATE_FP_REGS 

The buffer must point to a `zx_thread_state_fp_regs_t` structure. On 64-bit ARM platforms, float point state is in the vector registers and this structureis empty. 缓冲区必须指向“ zx_thread_state_fp_regs_t”结构。在64位ARM平台上，浮点状态在向量寄存器中，并且此结构为空。

 
### ZX_THREAD_STATE_VECTOR_REGS  ZX_THREAD_STATE_VECTOR_REGS 

The buffer must point to a `zx_thread_state_vector_regs_t` structure.  缓冲区必须指向“ zx_thread_state_vector_regs_t”结构。

 
### ZX_THREAD_STATE_DEBUG_REGS  ZX_THREAD_STATE_DEBUG_REGS 

The buffer must point to a `zx_thread_state_debug_regs_t` structure. All input fields will be ignored and overwritten with the actual values for the thread. 缓冲区必须指向“ zx_thread_state_debug_regs_t”结构。所有输入字段将被忽略，并被线程的实际值覆盖。

 
### ZX_THREAD_STATE_SINGLE_STEP  ZX_THREAD_STATE_SINGLE_STEP 

The buffer must point to a `zx_thread_state_single_step_t` value which may contain either 0 (normal running), or 1 (single stepping enabled). 缓冲区必须指向一个“ zx_thread_state_single_step_t”值，该值可能包含0（正常运行）或1（启用单步执行）。

 
### ZX_THREAD_X86_REGISTER_FS  ZX_THREAD_X86_REGISTER_FS 

The buffer must point to a `zx_thread_x86_register_fs_t` structure which contains a uint64. This is only relevant on x86 platforms. 缓冲区必须指向包含uint64的zx_thread_x86_register_fs_t结构。这仅在x86平台上相关。

 
### ZX_THREAD_X86_REGISTER_GS  ZX_THREAD_X86_REGISTER_GS 

The buffer must point to a `zx_thread_x86_register_gs_t` structure which contains a uint64. This is only relevant on x86 platforms. 缓冲区必须指向包含uint64的zx_thread_x86_register_gs_t结构。这仅在x86平台上相关。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_THREAD** and have **ZX_RIGHT_READ**.  *句柄*必须为** ZX_OBJ_TYPE_THREAD **类型，并具有** ZX_RIGHT_READ **。

 
## RETURN VALUE  返回值 

`zx_thread_read_state()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_thread_read_state（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not that of a thread.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是线程的句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* lacks **ZX_RIGHT_READ**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少** ZX_RIGHT_READ **。

**ZX_ERR_INVALID_ARGS**  *kind* is not valid or *buffer* is an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** *类型*无效或*缓冲区*无效。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_BUFFER_TOO_SMALL**  The buffer length *buffer_size* is too small to hold the data required by *kind*. ** ZX_ERR_BUFFER_TOO_SMALL **缓冲区长度* buffer_size *太小，无法容纳* kind *所需的数据。

**ZX_ERR_BAD_STATE**  The thread is not stopped at a point where state is available. The thread state may only be read when the thread is stopped dueto an exception. ** ZX_ERR_BAD_STATE **线程不会在状态可用时停止。仅当线程由于异常而停止时，才可以读取线程状态。

**ZX_ERR_NOT_SUPPORTED**  *kind* is not supported. This can happen, for example, when trying to read a register set thatis not supported by the hardware the program is currently running on. ** ZX_ERR_NOT_SUPPORTED ** *不支持*。例如，当尝试读取程序当前正在运行的硬件不支持的寄存器集时，可能会发生这种情况。

 
## SEE ALSO  也可以看看 

 

