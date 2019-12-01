 
# zx_clock_get_monotonic  zx_clock_get_monotonic 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Acquire the current monotonic time.  获取当前单调时间。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_time_t zx_clock_get_monotonic(void);
```
 

 
## DESCRIPTION  描述 

`zx_clock_get_monotonic()` returns the current time in the system monotonic clock. This is the number of nanoseconds since the system waspowered on. It does not always reset on reboot and does not adjust duringsleep, and thus should not be used as a reliable source of uptime. zx_clock_get_monotonic（）返回系统单调时钟中的当前时间。这是自系统启动以来的纳秒数。它并不总是在重启时重置，也不会在睡眠期间进行调整，因此不应用作可靠的正常运行时间来源。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

[`zx_clock_get()`] returns the current monotonic time.  [`zx_clock_get（）`]返回当前单调时间。

 
## ERRORS  错误 

`zx_clock_get_monotonic()` cannot fail.  zx_clock_get_monotonic（）不会失败。

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

