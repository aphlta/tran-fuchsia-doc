 
# zx_object_set_profile  zx_object_set_profile 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Apply a scheduling profile to a thread.  将调度配置文件应用于线程。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_object_set_profile(zx_handle_t handle,
                                  zx_handle_t profile,
                                  uint32_t options);
```
 

 
## DESCRIPTION  描述 

`zx_object_set_profile()` applies an already created [profile] to the thread specified in *handle*. zx_object_set_profile（）将已经创建的[profile]应用于* handle *中指定的线程。

The parameter *profile* is a handle to a [profile] object created with [`zx_profile_create()`]. 参数* profile *是使用[`zx_profile_create（）]创建的[profile]对象的句柄。

*options* is currently ignored, and should be set to `0` by callers.  * options *当前被忽略，调用者应将其设置为0。

[profile]: /docs/concepts/objects/profile.md  [个人资料]：/ docs / concepts / objects / profile.md

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_THREAD** and have **ZX_RIGHT_MANAGE_THREAD**.  *句柄*必须为** ZX_OBJ_TYPE_THREAD **类型，并具有** ZX_RIGHT_MANAGE_THREAD **。

*profile* must be of type **ZX_OBJ_TYPE_PROFILE** and have **ZX_RIGHT_APPLY_PROFILE**.  * profile *必须为** ZX_OBJ_TYPE_PROFILE **类型，并具有** ZX_RIGHT_APPLY_PROFILE **。

 
## RETURN VALUE  返回值 

Returns **ZX_OK** on success. In the event of failure, a negative error value is returned. 成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a thread handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是线程句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_MANAGE_THREAD** right. ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_MANAGE_THREAD **权限。

**ZX_ERR_BAD_STATE**  The thread is still being created, is dying, or dead, and cannot have a profile applied to it. ** ZX_ERR_BAD_STATE **线程仍在创建中，即将死去或死掉，并且无法对其应用配置文件。

 
## SEE ALSO  也可以看看 

 
 - [`zx_profile_create()`]  -[`zx_profile_create（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

