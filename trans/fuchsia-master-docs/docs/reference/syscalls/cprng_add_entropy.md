 
# zx_cprng_add_entropy  zx_cprng_add_entropy 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Add entropy to the kernel CPRNG.  向内核CPRNG添加熵。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_cprng_add_entropy(const void* buffer, size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

`zx_cprng_add_entropy()` mixes the given entropy into the kernel CPRNG. a privileged operation.  It will accept at most **ZX_CPRNG_ADD_ENTROPY_MAX_LEN**bytes of entropy at a time. zx_cprng_add_entropy（）将给定的熵混合到内核CPRNG中。特权操作。一次最多接受** ZX_CPRNG_ADD_ENTROPY_MAX_LEN **字节的熵。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_cprng_add_entropy()` returns **ZX_OK** on success.  zx_cprng_add_entropy（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS** *buffer_size* is too large, or *buffer* is not a valid userspace pointer. ** ZX_ERR_INVALID_ARGS ** * buffer_size *太大，或者* buffer *不是有效的用户空间指针。

 
## BUGS  臭虫 

This syscall should be very privileged.  此系统调用应具有很高的特权。

 
## SEE ALSO  也可以看看 

 
 - [`zx_cprng_draw()`]  -[`zx_cprng_draw（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

