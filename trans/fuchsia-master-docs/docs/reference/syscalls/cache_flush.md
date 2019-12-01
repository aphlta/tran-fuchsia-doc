 
# zx_cache_flush  zx_cache_flush 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Flush CPU data and/or instruction caches.  刷新CPU数据和/或指令缓存。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_cache_flush(const void* addr, size_t size, uint32_t options);
```
 

 
## DESCRIPTION  描述 

`zx_cache_flush()` flushes CPU caches covering memory in the given virtual address range.  If that range of memory is not readable, thenthe thread may fault as it would for a data read. zx_cache_flush（）刷新CPU缓存，覆盖给定虚拟地址范围内的内存。如果该范围的内存不可读，则该线程可能会像读取数据一样出错。

*options* is a bitwise OR of:  * options *是以下各项的按位或

 
 * **ZX_CACHE_FLUSH_DATA**  * ** ZX_CACHE_FLUSH_DATA **

   Clean (write back) data caches, so previous writes on this CPU are visible in main memory. 清理（​​回写）数据高速缓存，因此该CPU上的先前写入在主内存中可见。

 
 * **ZX_CACHE_FLUSH_INVALIDATE** (valid only when combined with **ZX_CACHE_FLUSH_DATA**) * ** ZX_CACHE_FLUSH_INVALIDATE **（仅当与** ZX_CACHE_FLUSH_DATA **结合使用时有效）

   Clean (write back) data caches and then invalidate data caches, so previous writes on this CPU are visible in main memory and futurereads on this CPU see external changes to main memory. 清理（​​写回）数据高速缓存，然后使数据高速缓存无效，因此在该CPU上的先前写入在主内存中可见，而在该CPU上的将来读取将看到对主内存的外部更改。

 
 * **ZX_CACHE_FLUSH_INSN**  * ** ZX_CACHE_FLUSH_INSN **

   Synchronize instruction caches with data caches, so previous writes on this CPU are visible to instruction fetches.  If this is combinedwith **ZX_CACHE_FLUSH_DATA**, then previous writes will be visible tomain memory as well as to instruction fetches. 将指令高速缓存与数据高速缓存同步，因此指令提取对此CPU的先前写入可见。如果将其与** ZX_CACHE_FLUSH_DATA **结合使用，则先前的写入对于主存储器以及指令提取将是可见的。

At least one of **ZX_CACHE_FLUSH_DATA** and **ZX_CACHE_FLUSH_INSN** must be included in *options*. * options *中必须至少包含** ZX_CACHE_FLUSH_DATA **和** ZX_CACHE_FLUSH_INSN **之一。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_cache_flush()` returns **ZX_OK** on success, or an error code on failure.  zx_cache_flush（）成功返回** ZX_OK **失败返回错误代码。

 
## ERRORS  错误 

