 
# zx_vmar_protect  zx_vmar_protect 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Set protection of virtual memory pages.  设置虚拟内存页面的保护。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_vmar_protect(zx_handle_t handle,
                            zx_vm_option_t options,
                            zx_vaddr_t addr,
                            uint64_t len);
```
 

 
## DESCRIPTION  描述 

`zx_vmar_protect()` alters the access protections for the memory mappings in the range of *len* bytes starting from *addr*. The *options* argument shouldbe a bitwise-or of one or more of the following: zx_vmar_protect（）在从* addr *开始的* len *个字节的范围内更改内存映射的访问保护。 * options *参数应按位或以下一项或多项：

 
- **ZX_VM_PERM_READ**  Map as readable.  It is an error if *handle* does not have **ZX_VM_CAN_MAP_READ** permissions or *handle* doesnot have the **ZX_RIGHT_READ** right.  It is also an error if the VMO handleused to create the mapping did not have the **ZX_RIGHT_READ** right. -** ZX_VM_PERM_READ **映射为可读。如果* handle *不具有** ZX_VM_CAN_MAP_READ **权限或* handle *不具有** ZX_RIGHT_READ **权限，则是错误的。如果用于创建映射的VMO处理不具有** ZX_RIGHT_READ **权限，这也是一个错误。
- **ZX_VM_PERM_WRITE**  Map as writable.  It is an error if *handle* does not have **ZX_VM_CAN_MAP_WRITE** permissions or *handle* doesnot have the **ZX_RIGHT_WRITE** right.  It is also an error if the VMO handleused to create the mapping did not have the **ZX_RIGHT_WRITE** right. -** ZX_VM_PERM_WRITE **映射为可写。如果* handle *不具有** ZX_VM_CAN_MAP_WRITE **权限或* handle *不具有** ZX_RIGHT_WRITE **权限，则是错误的。如果用于创建映射的VMO处理不具有** ZX_RIGHT_WRITE **权限，这也是一个错误。
- **ZX_VM_PERM_EXECUTE**  Map as executable.  It is an error if *handle* does not have **ZX_VM_CAN_MAP_EXECUTE** permissions or *handle* doesnot have the **ZX_RIGHT_EXECUTE** right.  It is also an error if the VMO handleused to create the mapping did not have the **ZX_RIGHT_EXECUTE** right. -** ZX_VM_PERM_EXECUTE **映射为可执行文件。如果* handle *不具有** ZX_VM_CAN_MAP_EXECUTE **权限，或者* handle *不具有** ZX_RIGHT_EXECUTE **权限，则是错误的。如果用于创建映射的VMO句柄没有** ZX_RIGHT_EXECUTE **权限，这也是一个错误。

*len* must be page-aligned.  * len *必须页面对齐。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

If *options* & **ZX_VM_PERM_READ**, *handle* must be of type **ZX_OBJ_TYPE_VMAR** and have **ZX_RIGHT_READ**.  如果* options * ** ZX_VM_PERM_READ **，则* handle *必须为** ZX_OBJ_TYPE_VMAR **类型，并且必须为** ZX_RIGHT_READ **。

If *options* & **ZX_VM_PERM_WRITE**, *handle* must be of type **ZX_OBJ_TYPE_VMAR** and have **ZX_RIGHT_WRITE**.  如果* options * ** ZX_VM_PERM_WRITE **，则* handle *必须为** ZX_OBJ_TYPE_VMAR **类型并具有** ZX_RIGHT_WRITE **。

If *options* & **ZX_VM_PERM_EXECUTE**, *handle* must be of type **ZX_OBJ_TYPE_VMAR** and have **ZX_RIGHT_EXECUTE**.  如果* options * ** ZX_VM_PERM_EXECUTE **，则* handle *必须为** ZX_OBJ_TYPE_VMAR **类型并具有** ZX_RIGHT_EXECUTE **。

 
## RETURN VALUE  返回值 

`zx_vmar_protect()` returns **ZX_OK** on success.  zx_vmar_protect（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a VMAR handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是VMAR句柄。

**ZX_ERR_INVALID_ARGS**  *prot_flags* is an unsupported combination of flags (e.g., **ZX_VM_PERM_WRITE** but not **ZX_VM_PERM_READ**), *addr* isnot page-aligned, *len* is 0, or some subrange of the requested range isoccupied by a subregion. ** ZX_ERR_INVALID_ARGS ** * prot_flags *是不受支持的标志组合（例如，** ZX_VM_PERM_WRITE **但不是** ZX_VM_PERM_READ **），* addr *不是页面对齐，* len *为0或请求的范围由一个子区域占用。

**ZX_ERR_NOT_FOUND**  Some subrange of the requested range is not mapped.  ** ZX_ERR_NOT_FOUND **所请求范围的某些子范围未映射。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have the proper rights for the requested change, the original VMO handle used to create the mapping did nothave the rights for the requested change, or the VMAR itself does not allowthe requested change. ** ZX_ERR_ACCESS_DENIED ** *句柄*没有所请求更改的正确权限，用于创建映射的原始VMO句柄没有所请求更改的权限，或者VMAR本身不允许所请求的更改。

 
## NOTES  笔记 

 
## SEE ALSO  也可以看看 

 
 - [`zx_vmar_allocate()`]  -[`zx_vmar_allocate（）`]
 - [`zx_vmar_destroy()`]  -[`zx_vmar_destroy（）`]
 - [`zx_vmar_map()`]  -[`zx_vmar_map（）`]
 - [`zx_vmar_unmap()`]  -[`zx_vmar_unmap（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

