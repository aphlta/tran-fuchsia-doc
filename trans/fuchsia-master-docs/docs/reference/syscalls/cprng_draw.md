 
# zx_cprng_draw  zx_cprng_draw 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Draw from the kernel's CPRNG.  从内核的CPRNG中提取。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

void zx_cprng_draw(void* buffer, size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

`zx_cprng_draw()` draws random bytes from the kernel CPRNG.  This data should be suitable for cryptographic applications. zx_cprng_draw（）从内核CPRNG提取随机字节。此数据应适用于加密应用程序。

Clients that require a large volume of randomness should consider using these bytes to seed a user-space random number generator for better performance. 要求大量随机性的客户端应考虑使用这些字节为用户空间随机数生成器提供种子，以提高性能。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## NOTES  笔记 

`zx_cprng_draw()` triggers terminates the calling process if **buffer** is not a valid userspace pointer. 如果buffer不是有效的用户空间指针，则zx_cprng_draw（）触发器将终止调用过程。

There are no other error conditions.  If its arguments are valid, `zx_cprng_draw()` will succeed. 没有其他错误情况。如果其参数有效，则`zx_cprng_draw（）`将成功。

 
## SEE ALSO  也可以看看 

 
 - [`zx_cprng_add_entropy()`]  -[`zx_cprng_add_entropy（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

