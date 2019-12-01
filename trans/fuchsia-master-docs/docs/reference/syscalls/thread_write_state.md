 
# zx_thread_write_state  zx_thread_write_state 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Write one aspect of thread state.  写线程状态的一方面。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_thread_write_state(zx_handle_t handle,
                                  uint32_t kind,
                                  const void* buffer,
                                  size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

`zx_thread_write_state()` writes one aspect of state of the thread. The thread state may only be written when the thread is halted for an exception or thethread is suspended. zx_thread_write_state（）写入线程状态的一方面。仅当线程因异常而暂停或线程被挂起时，才可以写入线程状态。

The thread state is highly processor specific. See the structures in zircon/syscalls/debug.h for the contents of the structures on each platform. 线程状态是高度特定于处理器的。有关每个平台上结构的内容，请参见zircon / syscalls / debug.h中的结构。

 
## STATES  状态 

See [`zx_thread_read_state()`] for the list of available states and their corresponding values. 有关可用状态及其对应值的列表，请参见[`zx_thread_read_state（）`]。

 
### ZX_THREAD_STATE_DEBUG_REGS  ZX_THREAD_STATE_DEBUG_REGS 

 
#### ARM  臂 

ARM has a variable amount of debug breakpoints and watchpoints. For this architecture, `zx_thread_state_debug_regs_t` is big enough to hold the maximumamount of breakpoints possible. But in most cases a given CPU implementationholds a lesser amount, meaning that the upper values beyond the limit are notused. ARM具有可变数量的调试断点和观察点。对于这种架构，`zx_thread_state_debug_regs_t`足够大，可以容纳最大数量的断点。但是在大多数情况下，给定的CPU实现所占的份额较小，这意味着不使用超出限制的上限值。

The kernel will write all the available registers in the hardware independent of the given breakpoint/watchpoint count value. This means that all the correctstate must be set for the call. 内核将与给定的断点/监视点计数值无关地将所有可用寄存器写入硬件。这意味着必须为该呼叫设置所有正确的状态。

You can get the current state of the registers by calling [`zx_thread_read_state()`](thread_read_state.md#zx_thread_state_debug_regs). 您可以通过调用[`zx_thread_read_state（）`]（thread_read_state.mdzx_thread_state_debug_regs）来获取寄存器的当前状态。

 
#### ARM Debug Hardware Debug Registers  ARM调试硬件调试寄存器 

ARM debug registers are highly configurable via their DBGBCR<n> registers. However, Zircon limits that functionality to _Unlinked Address Matching_ HWbreakpoints. This means that HW breakpoints will only issue exceptions uponexception on the given address in the corresponding DBGBVR register. ARM调试寄存器可通过其DBGBCR <n>寄存器进行高度配置。但是，Zircon将该功能限制为_Unlinked Address Matching_ HWbreakpoints。这意味着硬件断点将仅在相应DBGBVR寄存器中给定地址的异常时发出异常。

Because of this, all the values within DBGBCR will be ignored except for the E bit, which is used to determine whether that particular breakpoint is activatedor not. Said in another way, in order to activate a HW breakpoint, all that isneeded is to set the correct address in DBGBVR and write 1 to DBGBCR. 因此，将忽略DBGBCR中的所有值（E位除外），E位用于确定是否激活了该特定断点。换句话说，为了激活硬件断点，所需要做的就是在DBGBVR中设置正确的地址并将1写入DBGBCR。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_THREAD** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_THREAD **类型，并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_thread_write_state()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_thread_write_state（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not that of a thread.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是线程的句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* lacks **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少** ZX_RIGHT_WRITE **。

**ZX_ERR_INVALID_ARGS**  *kind* is not valid, *buffer* is an invalid pointer, *buffer_size* doesn't match the size of the structure expected for *kind* orthe given values to set are not valid. ** ZX_ERR_INVALID_ARGS ** * kind *无效，* buffer *是无效的指针，* buffer_size *与* kind *预期的结构大小不匹配，或者给定的设置值无效。

 

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_BAD_STATE**  The thread is not stopped at a point where state is available. The thread state may only be read when the thread is stopped dueto an exception. ** ZX_ERR_BAD_STATE **线程不会在状态可用时停止。仅当线程由于异常而停止时，才可以读取线程状态。

**ZX_ERR_NOT_SUPPORTED**  *kind* is not supported. This can happen, for example, when trying to read a register set thatis not supported by the hardware the program is currently running on. ** ZX_ERR_NOT_SUPPORTED ** *不支持*。例如，当尝试读取程序当前正在运行的硬件不支持的寄存器集时，可能会发生这种情况。

 
#### ARM  臂 

**ZX_ERR_INVALID_ARGS**   If the address provided to a DBGBVR register is not valid (ie. not addressable from userspace). Also if any value is set for a HWbreakpoint beyond the number provided by the platform (see above forinformation about retrieving that number). ** ZX_ERR_INVALID_ARGS **如果提供给DBGBVR寄存器的地址无效（即，无法从用户空间寻址）。同样，如果为HWbreakpoint设置的值超出了平台提供的数字（请参阅上面的有关获取该数字的信息）。

 
## SEE ALSO  也可以看看 

 
 - [`zx_thread_read_state()`]  -[`zx_thread_read_state（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

