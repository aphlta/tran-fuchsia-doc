 
# zx_object_signal_peer  zx_object_signal_peer 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Signal an object's peer.  发信号通知对象的对等体。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_object_signal_peer(zx_handle_t handle,
                                  uint32_t clear_mask,
                                  uint32_t set_mask);
```
 

 
## DESCRIPTION  描述 

`zx_object_signal_peer()` asserts and deasserts the userspace-accessible signal bits on the object's peer. A object peer is the opposite endpoint of a*channel*, *socket*, *fifo*, or *eventpair*. zx_object_signal_peer（）声明和取消声明对象对等点上用户空间可访问的信号位。对象对等体是* channel *，* socket *，* fifo *或* eventpair *的相对端点。

Most of the 32 signals are reserved for system use and are assigned to per-object functions, like **ZX_CHANNEL_READABLE** or **ZX_TASK_TERMINATED**. Thereare 8 signal bits available for userspace processes to use as they see fit:**ZX_USER_SIGNAL_0** through **ZX_USER_SIGNAL_7**. 32个信号中的大多数保留给系统使用，并分配给每个对象的功能，例如** ZX_CHANNEL_READABLE **或** ZX_TASK_TERMINATED **。有8个信号位可供用户空间进程使用，如它们认为合适：** ZX_USER_SIGNAL_0 **至** ZX_USER_SIGNAL_7 **。

*Eventpair* objects also allow control over the **ZX_EVENTPAIR_SIGNALED** bit.  * Eventpair *对象还允许控制** ZX_EVENTPAIR_SIGNALED **位。

The *clear_mask* is first used to clear any bits indicated, and then the *set_mask* is used to set any bits indicated. * clear_mask *首先用于清除指示的任何位，然后* set_mask *用于设置指示的任何位。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have **ZX_RIGHT_SIGNAL_PEER**.  *句柄*必须具有** ZX_RIGHT_SIGNAL_PEER **。

 
## RETURN VALUE  返回值 

`zx_object_signal_peer()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_object_signal_peer（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* lacks the right **ZX_RIGHT_SIGNAL_PEER**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*缺少正确的** ZX_RIGHT_SIGNAL_PEER **。

**ZX_ERR_INVALID_ARGS**  *clear_mask* or *set_mask* contain bits that are not allowed.  ** ZX_ERR_INVALID_ARGS ** * clear_mask *或* set_mask *包含不允许的位。

**ZX_ERR_NOT_SUPPORTED**  Used on an object lacking a peer.  ** ZX_ERR_NOT_SUPPORTED **用于缺少对等对象的对象。

**ZX_ERR_PEER_CLOSED**  Called on an object with a closed peer.  ** ZX_ERR_PEER_CLOSED **调用具有封闭同级的对象。

 
## SEE ALSO  也可以看看 

 
 - [`zx_eventpair_create()`]  -[`zx_eventpair_create（）`]
 - [`zx_object_signal()`]  -[`zx_object_signal（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

