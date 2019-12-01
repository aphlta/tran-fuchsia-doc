 
# zx_vmar_op_range  zx_vmar_op_range 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Perform an operation on VMOs mapped into this VMAR.  在映射到此VMAR的VMO上执行操作。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmar_op_range(zx_handle_t handle,
                             uint32_t op,
                             uint64_t address,
                             uint64_t size,
                             void* buffer,
                             size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

`zx_vmo_op_range()` performs operation *op* on VMOs mapped in the range *address* to *address*+*size*.  zx_vmo_op_range（）对映射在* address *到* address * + * size *范围内的VMO执行* op *操作。

*address* and *size* must fall entirely within this VMAR, and must meet the alignment requirements specified for *op* by [`zx_vmo_op_range()`].  * address *和* size *必须完全落入此VMAR，并且必须满足[`zx_vmo_op_range（）`]为* op *指定的对齐要求。

*buffer* and *buffer_size* are currently unused, and must be empty  * buffer *和* buffer_size *当前未使用，并且必须为空

The supported operations are:  支持的操作是：

**ZX_VMO_OP_DECOMMIT** - Requires the **ZX_RIGHT_WRITE** right, and applies only to writable mappings.  ** ZX_VMO_OP_DECOMMIT **-需要** ZX_RIGHT_WRITE **权限，并且仅适用于可写映射。

The operation's semantics are otherwise as described by [`zx_vmo_op_range()`].  否则，该操作的语义由[`zx_vmo_op_range（）`]描述。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

If *op* is **ZX_VMO_OP_DECOMMIT**, affected mappings must be writable.  如果* op *是** ZX_VMO_OP_DECOMMIT **，则受影响的映射必须是可写的。

 
## RETURN VALUE  返回值 

`zx_vmar_op_range()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned.  zx_vmar_op_range（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED**  *handle*, or one of the affected VMO mappings, does not have sufficient rights to perform the operation.  ** ZX_ERR_ACCESS_DENIED ** *句柄*或受影响的VMO映射之一，没有足够的权限执行该操作。

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_BAD_STATE**  *handle* is not a live VMAR, or the range specified by *address* and *size* spans un-mapped pages.  ** ZX_ERR_BAD_STATE ** *句柄*不是实时VMAR，或者* address *和* size *指定的范围跨越未映射的页面。

**ZX_ERR_INVALID_ARGS**  *buffer* is non-null, or *buffer_size* is non-zero, *op* is not a valid operation, *size* is zero, or *address* was not page-aligned.  ** ZX_ERR_INVALID_ARGS ** * buffer *不为空，或* buffer_size *不为零，* op *不是有效的操作，* size *为零，或* address *没有页面对齐。

**ZX_ERR_NOT_SUPPORTED**  *op* was not **ZX_VMO_OP_DECOMMIT**, or one or more mapped VMOs do not support the requested *op*.  ** ZX_ERR_NOT_SUPPORTED ** * op *不是** ZX_VMO_OP_DECOMMIT **，或者一个或多个映射的VMO不支持请求的* op *。

**ZX_ERR_OUT_OF_RANGE**  The range specified by *address* and *size* is not wholy within the VM address range specified by *handle*.  ** ZX_ERR_OUT_OF_RANGE **由* address *和* size *指定的范围不在由* handle *指定的VM地址范围内。

**ZX_ERR_WRONG_TYPE**  *handle* is not a VMAR handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VMAR句柄。

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]
 - [`zx_vmar_unmap()`]  -[`zx_vmar_unmap（）`]
 - [`zx_vmo_op_range()`]  -[`zx_vmo_op_range（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

