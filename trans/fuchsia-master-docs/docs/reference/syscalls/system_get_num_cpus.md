 
# zx_system_get_num_cpus  zx_system_get_num_cpus 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Get number of logical processors on the system.  获取系统上逻辑处理器的数量。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

uint32_t zx_system_get_num_cpus(void);
```
 

 
## DESCRIPTION  描述 

`zx_system_get_num_cpus()` returns the number of CPUs (logical processors) that exist on the system currently running.  This number cannot changeduring a run of the system, only at boot time. zx_system_get_num_cpus（）返回当前正在运行的系统上存在的CPU（逻辑处理器）的数量。仅在引导时，该数字不能更改系统的运行。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_system_get_num_cpus()` returns the number of CPUs.  zx_system_get_num_cpus（）返回CPU的数量。

 
## ERRORS  错误 

`zx_system_get_num_cpus()` cannot fail.  zx_system_get_num_cpus（）不能失败。

 
## NOTES  笔记 

 
## SEE ALSO  也可以看看 

 
 - [`zx_system_get_physmem()`]  -[`zx_system_get_physmem（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

