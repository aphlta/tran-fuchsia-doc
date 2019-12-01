 
# Time units  时间单位 

 
## Userspace exposed time units  用户空间公开的时间单位 

*zx\_time\_t* is in nanoseconds.  * zx \ _time \ _t *以纳秒为单位。

Use [`zx_clock_get()`] to get the current time.  使用[`zx_clock_get（）`]获取当前时间。

 
## Kernel-internal time units  内核内部时间单位 

*lk\_time\_t* is in nanoseconds.  * lk \ _time \ _t *以纳秒为单位。

To get the current time since boot, use:  要获取自启动以来的当前时间，请使用：

```
#include <platform.h>

lk_time_t current_time(void);
```
 

