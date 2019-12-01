 
# zx_port_cancel  zx_port_cancel 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Cancels async port notifications on an object.  取消对象的异步端口通知。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_port_cancel(zx_handle_t handle,
                           zx_handle_t source,
                           uint64_t key);
```
 

 
## DESCRIPTION  描述 

`zx_port_cancel()` is a non-blocking syscall which cancels pending [`zx_object_wait_async()`] calls done with *source* and *key*. zx_port_cancel（）是一个非阻塞的系统调用，它取消了使用* source *和* key *完成的待处理的[`zx_object_wait_async（）`]调用。

When this call succeeds no new packets from the object pointed by *source* with *key* will be delivered to *handle*, and pending queuedpackets that match *source* and *key* are removed from the port. 当此调用成功时，不会将来自带有* key *的* source *所指向的对象的新数据包传递到* handle *，并且将与* source *和* key *匹配的未决队列分组从端口中删除。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_PORT** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_PORT **类型并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_port_cancel()` returns **ZX_OK** if cancellation succeeded and either queued packets were removed or pending [`zx_object_wait_async()`] werecanceled. 如果取消成功并且删除了排队的数据包或取消了待处理的[zx_object_wait_async（）]，则zx_port_cancel（）返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *source* or *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *源*或*句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a port handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是端口句柄。

**ZX_ERR_ACCESS_DENIED**  *source* or *handle* does not have **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *源*或*句柄*没有** ZX_RIGHT_WRITE **。

**ZX_ERR_NOT_SUPPORTED**  *source* is a handle that cannot be waited on.  ** ZX_ERR_NOT_SUPPORTED ** * source *是无法等待的句柄。

**ZX_ERR_NOT_FOUND** if either no pending packets or pending [`zx_object_wait_async()`] calls with *source* and *key* were found. ** ZX_ERR_NOT_FOUND **，如果没有找到带有* source *和* key *的未决数据包或未决的[`zx_object_wait_async（）`]调用。

 
## SEE ALSO  也可以看看 

 
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

