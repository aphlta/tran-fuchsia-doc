 
# zx_ticks_get  zx_ticks_get 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Read the number of high-precision timer ticks since boot.  读取自启动以来高精度计时器的滴答数。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_ticks_t zx_ticks_get(void);
```
 

 
## DESCRIPTION  描述 

`zx_ticks_get()` returns the number of high-precision timer ticks since boot.  zx_ticks_get（）返回自启动以来高精度计时器的滴答数。

These ticks may be processor cycles, high speed timer, profiling timer, etc. They are not guaranteed to continue advancing when the system is asleep. 这些滴答可能是处理器周期，高速计时器，配置计时器等。当系统处于睡眠状态时，不能保证它们继续前进。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_ticks_get()` returns the number of high-precision timer ticks since boot.  zx_ticks_get（）返回自启动以来高精度计时器的滴答数。

 
## ERRORS  错误 

`zx_ticks_get()` does not report any error conditions.  zx_ticks_get（）不报告任何错误情况。

 
## NOTES  笔记 

The returned value may be highly variable. Factors that can affect it include:  返回的值可能是高度可变的。可能影响它的因素包括：

 
- Changes in processor frequency  -处理器频率的变化
- Migration between processors  -处理器之间的迁移
- Reset of the processor cycle counter  -重置处理器周期计数器
- Reordering of instructions (if required, use a memory barrier)  -重新排序指令（如果需要，请使用存储屏障）

 
## SEE ALSO  也可以看看 

 

