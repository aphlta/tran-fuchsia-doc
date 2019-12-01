 
# zx_ticks_per_second  zx_ticks_per_second 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Read the number of high-precision timer ticks in a second.  每秒读取高精度计时器刻度的数量。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_ticks_t zx_ticks_per_second(void);
```
 

 
## DESCRIPTION  描述 

`zx_ticks_per_second()` returns the number of high-precision timer ticks in a second. zx_ticks_per_second（）返回一秒钟内高精度计时器刻度的数量。

This can be used together with [`zx_ticks_get()`] to calculate the amount of time elapsed between two subsequent calls to [`zx_ticks_get()`]. 可以将其与[`zx_ticks_get（）`]一起使用，以计算两次对[`zx_ticks_get（）]的后续调用之间经过的时间。

This value can vary from boot to boot of a given system. Once booted, this value is guaranteed not to change. 该值在给定系统的引导之间可能有所不同。一旦启动，就保证此值不会更改。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_ticks_per_second()` returns the number of high-precision timer ticks in a second. zx_ticks_per_second（）返回一秒钟内高精度计时器刻度的数量。

 
## ERRORS  错误 

`zx_ticks_per_second()` does not report any error conditions.  zx_ticks_per_second（）不报告任何错误情况。

 
## EXAMPLES  例子 

```
zx_ticks_t ticks_per_second = zx_ticks_per_second();
zx_ticks_t ticks_start = zx_ticks_get();

// do some more work

zx_ticks_t ticks_end = zx_ticks_get();
double elapsed_seconds = (ticks_end - ticks_start) / (double)ticks_per_second;

```
 

 
## SEE ALSO  也可以看看 

 
 - [`zx_ticks_get()`]  -[`zx_ticks_get（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

