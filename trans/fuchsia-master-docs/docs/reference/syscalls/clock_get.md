 
# zx_clock_get  zx_clock_get 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Acquire the current time.  获取当前时间。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_clock_get(zx_clock_t clock_id, zx_time_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_clock_get()` returns the current time of *clock_id* via *out*, and returns whether *clock_id* was valid. zx_clock_get（）通过* out *返回* clock_id *的当前时间，并返回* clock_id *是否有效。

 
## SUPPORTED CLOCK IDS  支持的时钟ID 

**ZX_CLOCK_MONOTONIC** number of nanoseconds since the system was powered on.  ** ZX_CLOCK_MONOTONIC **自系统加电以来的纳秒数。

**ZX_CLOCK_UTC** number of wall clock nanoseconds since the Unix epoch (midnight on January 1 1970) in UTC  自UTC的Unix纪元（1970年1月1日午夜）以来的ZX_CLOCK_UTC **挂钟纳秒数

**ZX_CLOCK_THREAD** number of nanoseconds the current thread has been running for.  ** ZX_CLOCK_THREAD **当前线程已运行的纳秒数。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

On success, `zx_clock_get()` returns **ZX_OK**.  成功时，`zx_clock_get（）`返回** ZX_OK **。

 
## ERRORS  错误 

