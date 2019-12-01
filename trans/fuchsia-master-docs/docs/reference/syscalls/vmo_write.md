 
# zx_vmo_write  zx_vmo_write 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Write bytes to the VMO.  将字节写入VMO。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmo_write(zx_handle_t handle,
                         const void* buffer,
                         uint64_t offset,
                         size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_write()` attempts to write exactly *buffer_size* bytes to a VMO at *offset*.  zx_vmo_write（）尝试将* buffer_size *字节精确地写入* offset *处的VMO。

*buffer* pointer to a user buffer to write bytes from.  * buffer *指向要从中写入字节的用户缓冲区的指针。

*buffer_size* number of bytes to attempt to write.  * buffer_size *尝试写入的字节数。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_WRITE**.  *句柄*的类型必须为** ZX_OBJ_TYPE_VMO **且具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_vmo_write()` returns **ZX_OK** on success, and exactly *buffer_size* bytes will have been written from *buffer*.In the event of failure, a negative error value is returned, and the number ofbytes written from *buffer* is undefined. zx_vmo_write（）成功返回** ZX_OK **，并且将从* buffer *写入正好* buffer_size *字节。如果失败，则返回负错误值，并且从* buffer写入的字节数*未定义。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a VMO handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VMO句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have the **ZX_RIGHT_WRITE** right.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WRITE **权限。

**ZX_ERR_INVALID_ARGS**  *buffer* is an invalid pointer or NULL.  ** ZX_ERR_INVALID_ARGS ** * buffer *是无效的指针或NULL。

**ZX_ERR_NOT_FOUND** *buffer* address does not map to address in address space.  ** ZX_ERR_NOT_FOUND ** *缓冲区*地址未映射到地址空间中的地址。

**ZX_ERR_NO_MEMORY**  Failure to allocate system memory to complete write.  ** ZX_ERR_NO_MEMORY **无法分配系统内存以完成写入。

**ZX_ERR_OUT_OF_RANGE**  *offset* + *buffer_size* is greater than the size of the VMO. ** ZX_ERR_OUT_OF_RANGE ** *偏移* + * buffer_size *大于VMO的大小。

**ZX_ERR_BAD_STATE**  VMO has been marked uncached and is not directly writable.  ** ZX_ERR_BAD_STATE ** VMO已被标记为未缓存，并且不能直接写入。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmo_create()`]  -[`zx_vmo_create（）`]
 - [`zx_vmo_create_child()`]  -[`zx_vmo_create_child（）`]
 - [`zx_vmo_get_size()`]  -[`zx_vmo_get_size（）`]
 - [`zx_vmo_op_range()`]  -[`zx_vmo_op_range（）`]
 - [`zx_vmo_read()`]  -[`zx_vmo_read（）`]
 - [`zx_vmo_set_cache_policy()`]  -[`zx_vmo_set_cache_policy（）`]
 - [`zx_vmo_set_size()`]  -[`zx_vmo_set_size（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

