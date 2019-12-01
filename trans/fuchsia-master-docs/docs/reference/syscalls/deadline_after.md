 
# zx_deadline_after  zx_deadline_after 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Convert a time relative to now to an absolute deadline.  将相对于现在的时间转换为绝对期限。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_time_t zx_deadline_after(zx_duration_t nanoseconds);
```
 

 
## DESCRIPTION  描述 

`zx_deadline_after()` is a utility for converting from now-relative durations to absolute deadlines. If *nanoseconds* plus the current time is bigger than themaximum value for `zx_time_t`, the output is clamped to **ZX_TIME_INFINITE**. zx_deadline_after（）是一个实用程序，用于将当前持续时间转换为绝对截止时间。如果*纳秒*加当前时间大于`zx_time_t`的最大值，则输出将钳位为** ZX_TIME_INFINITE **。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_deadline_after()` returns the absolute time (with respect to **ZX_CLOCK_MONOTONIC**) that is *nanoseconds* nanoseconds from now. zx_deadline_after（）返回绝对时间（相对于** ZX_CLOCK_MONOTONIC **），从现在开始为*纳秒*纳秒。

 
## ERRORS  错误 

`zx_deadline_after()` does not report any error conditions.  zx_deadline_after（）不报告任何错误情况。

 
## EXAMPLES  例子 

```
// Sleep 50 milliseconds
zx_time_t deadline = zx_deadline_after(ZX_MSEC(50));
zx_nanosleep(deadline);
```
 

 
## SEE ALSO  也可以看看 

 

