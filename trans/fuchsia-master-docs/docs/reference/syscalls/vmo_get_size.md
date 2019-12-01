 
# zx_vmo_get_size  zx_vmo_get_size 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Read the current size of a VMO object.  读取VMO对象的当前大小。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmo_get_size(zx_handle_t handle, uint64_t* size);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_get_size()` returns the current size of the VMO.  zx_vmo_get_size（）返回VMO的当前大小。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_vmo_get_size()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_vmo_get_size（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a VMO handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VMO句柄。

**ZX_ERR_INVALID_ARGS**  *size* is an invalid pointer or NULL.  ** ZX_ERR_INVALID_ARGS ** * size *是无效的指针或NULL。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmo_create()`]  -[`zx_vmo_create（）`]
 - [`zx_vmo_create_child()`]  -[`zx_vmo_create_child（）`]
 - [`zx_vmo_op_range()`]  -[`zx_vmo_op_range（）`]
 - [`zx_vmo_read()`]  -[`zx_vmo_read（）`]
 - [`zx_vmo_set_size()`]  -[`zx_vmo_set_size（）`]
 - [`zx_vmo_write()`]  -[`zx_vmo_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

