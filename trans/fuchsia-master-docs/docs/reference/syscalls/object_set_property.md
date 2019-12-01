 
# zx_object_set_property  zx_object_set_property 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Set various properties of various kernel objects.  设置各种内核对象的各种属性。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_object_set_property(zx_handle_t handle,
                                   uint32_t property,
                                   const void* value,
                                   size_t value_size);
```
 

 
## DESCRIPTION  描述 

`zx_object_set_property()` modifies the value of a kernel object's property. Setting a property requires **ZX_RIGHT_SET_PROPERTY** rights on the handle. zx_object_set_property（）修改内核对象属性的值。设置属性需要在手柄上具有** ZX_RIGHT_SET_PROPERTY **权限。

See [`zx_object_get_property()`] for a full description.  有关完整说明，请参见[`zx_object_get_property（）`]。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have **ZX_RIGHT_SET_PROPERTY**.  *句柄*必须具有** ZX_RIGHT_SET_PROPERTY **。

If *property* is **ZX_PROP_PROCESS_DEBUG_ADDR**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS**.  如果* property *是** ZX_PROP_PROCESS_DEBUG_ADDR **，则* handle *必须是** ZX_OBJ_TYPE_PROCESS **类型。

If *property* is **ZX_PROP_PROCESS_BREAK_ON_LOAD**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS**.  如果* property *是** ZX_PROP_PROCESS_BREAK_ON_LOAD **，则* handle *必须是** ZX_OBJ_TYPE_PROCESS **类型。

If *property* is **ZX_PROP_SOCKET_RX_THRESHOLD**, *handle* must be of type **ZX_OBJ_TYPE_SOCKET**.  如果* property *是** ZX_PROP_SOCKET_RX_THRESHOLD **，则* handle *必须是** ZX_OBJ_TYPE_SOCKET **类型。

If *property* is **ZX_PROP_SOCKET_TX_THRESHOLD**, *handle* must be of type **ZX_OBJ_TYPE_SOCKET**.  如果* property *是** ZX_PROP_SOCKET_TX_THRESHOLD **，则* handle *必须是** ZX_OBJ_TYPE_SOCKET **类型。

If *property* is **ZX_PROP_JOB_KILL_ON_OOM**, *handle* must be of type **ZX_OBJ_TYPE_JOB**.  如果* property *是** ZX_PROP_JOB_KILL_ON_OOM **，则* handle *必须是** ZX_OBJ_TYPE_JOB **类型。

 
## SEE ALSO  也可以看看 

 
 - [`zx_object_get_property()`]  -[`zx_object_get_property（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

