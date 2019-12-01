 
# zx_object_get_child  zx_object_get_child 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Given a kernel object with children objects, obtain a handle to the child specified by the provided kernel object id.  给定具有子对象的内核对象，请获取由提供的内核对象ID指定的子对象的句柄。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_object_get_child(zx_handle_t handle,
                                uint64_t koid,
                                zx_rights_t rights,
                                zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_object_get_child()` attempts to find a child of the object referred to by *handle* which has the kernel object id specified by *koid*.  If such anobject exists, and the requested *rights* are not greater than those providedby the *handle* to the parent, a new handle to the specified child object isreturned. zx_object_get_child（）试图找到* handle *所引用对象的子对象，该对象的子对象由* koid *指定。如果存在这样的对象，并且所请求的* rights不大于* handle *给父对象提供的* rights，则返回指定子对象的新句柄。

*rights* may be **ZX_RIGHT_SAME_RIGHTS** which will result in rights equivalent to the those on the *handle*. *权利*可能是** ZX_RIGHT_SAME_RIGHTS **，这将导致与*句柄*上的权利相同的权利。

If the object is a *Process*, the *Threads* it contains may be obtained by this call. 如果对象是* Process *，则可以通过此调用获取其包含的* Threads *。

If the object is a *Job*, its (immediate) child *Jobs* and the *Processes* it contains may be obtained by this call. 如果对象是* Job *，则可以通过此调用获取其（立即）子* Jobs *和其中包含的* Processes *。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have **ZX_RIGHT_ENUMERATE**.  *句柄*必须具有** ZX_RIGHT_ENUMERATE **。

 
## RETURN VALUE  返回值 

On success, **ZX_OK** is returned and a handle to the desired child object is returned via *out*.  成功后，将返回** ZX_OK **，并通过* out *返回所需子对象的句柄。

 

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a *Process*, *Job*, or *Resource*.  ** ZX_ERR_WRONG_TYPE ** * handle *不是* Process *，* Job *或* Resource *。

**ZX_ERR_ACCESS_DENIED**   *handle* lacks the right **ZX_RIGHT_ENUMERATE** or *rights* specifies rights that are not present on *handle*. ** ZX_ERR_ACCESS_DENIED ** * handle *缺少权限** ZX_RIGHT_ENUMERATE **或* rights *指定* handle *上不存在的权限。

**ZX_ERR_NOT_FOUND**  *handle* does not have a child with the kernel object id *koid*.  ** ZX_ERR_NOT_FOUND ** * handle *没有子对象，其内核对象ID为* koid *。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_INVALID_ARGS**  *out* is an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** * out *是无效的指针。

 

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_get_info()`]  -[`zx_object_get_info（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

