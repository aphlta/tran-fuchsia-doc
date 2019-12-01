 
# zx_nanosleep  zx_nanosleep 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

High resolution sleep.  高分辨率睡眠。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_nanosleep(zx_time_t deadline);
```
 

 
## DESCRIPTION  描述 

`zx_nanosleep()` suspends the calling thread execution until *deadline* passes on **ZX_CLOCK_MONOTONIC**. A *deadline* value less than or equal to **0** immediatelyyields the thread. *deadline* will be automatically adjusted according to the job's[timer slack] policy. zx_nanosleep（）暂停调用线程的执行，直到* deadline *通过** ZX_CLOCK_MONOTONIC **为止。小于或等于** 0 **的* deadline *值会立即产生线程。 *最后期限*将根据工作的[计时器松弛]政策自动进行调整。

To sleep for a duration, use [`zx_deadline_after()`] and the **ZX_\<time-unit\>** helpers: 要睡眠一段时间，请使用[`zx_deadline_after（）`]和** ZX _ \ <time-unit \> **助手：

```
#include <zircon/syscalls.h> // zx_deadline_after, zx_nanosleep
#include <zircon/types.h> // ZX_MSEC et al.

// Sleep 50 milliseconds
zx_nanosleep(zx_deadline_after(ZX_MSEC(50)));
```
 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_nanosleep()` always returns **ZX_OK**.  zx_nanosleep（）总是返回** ZX_OK **。

 
## SEE ALSO  也可以看看 

 
 - [timer slack](/docs/concepts/objects/timer_slack.md)  -[计时器松弛]（/ docs / concepts / objects / timer_slack.md）
 - [`zx_deadline_after()`]  -[`zx_deadline_after（）`]
 - [`zx_timer_cancel()`]  -[`zx_timer_cancel（）`]
 - [`zx_timer_create()`]  -[`zx_timer_create（）`]
 - [`zx_timer_set()`]  -[`zx_timer_set（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

