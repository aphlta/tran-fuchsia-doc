 
# zx_system_get_physmem  zx_system_get_physmem 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Get amount of physical memory on the system.  获取系统上的物理内存量。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

uint64_t zx_system_get_physmem(void);
```
 

 
## DESCRIPTION  描述 

`zx_system_get_physmem()` returns the total size of physical memory on the machine, in bytes. zx_system_get_physmem（）返回机器上物理内存的总大小，以字节为单位。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_system_get_physmem()` returns a number in bytes.  zx_system_get_physmem（）返回以字节为单位的数字。

 
## ERRORS  错误 

`zx_system_get_physmem()` cannot fail.  zx_system_get_physmem（）不会失败。

 
## NOTES  笔记 

Currently the total size of physical memory cannot change during a run of the system, only at boot time.  This might change in the future. 当前，物理内存的总大小仅在引导时才能在系统运行期间更改。将来可能会改变。

 
## SEE ALSO  也可以看看 

 
 - [`zx_system_get_num_cpus()`]  -[`zx_system_get_num_cpus（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

