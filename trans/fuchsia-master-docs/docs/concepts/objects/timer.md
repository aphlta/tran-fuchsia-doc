 
# Timer  计时器 

 
## NAME  名称 

timer - An object that may be signaled at some point in the future  计时器-可能在将来某个时刻发出信号的对象

 
## SYNOPSIS  概要 

A timer is used to wait until a specified point in time has occurred or the timer has been canceled. 计时器用于等待直到指定的时间点发生或计时器已取消。

 
## DESCRIPTION  描述 

Like other waitable objects, timers can be waited on via [`zx_object_wait_one()`], [`zx_object_wait_many()`], or[`zx_object_wait_async()`]. 像其他可等待对象一样，可以通过[`zx_object_wait_one（）`]，[`zx_object_wait_many（）`]或[`zx_object_wait_async（）`]等待计时器。

A given timer can be used over and over.  给定的计时器可以反复使用。

Once **ZX_TIMER_SIGNALED** is asserted, it will remain asserted until the timer is canceled ([`zx_timer_cancel()`]) or reset ([`zx_timer_set()`]). 断言** ZX_TIMER_SIGNALED **之前，它将一直保持断言，直到取消计时器（[`zx_timer_cancel（）`]）或将其复位（[`zx_timer_set（）`]）为止。

The typical lifecycle is:  典型的生命周期是：

 
1. `zx_timer_create()`  1.`zx_timer_create（）`
2. `zx_timer_set()`  2.`zx_timer_set（）`
3. wait for the timer to be signaled  3.等待计时器发出信号
4. optionally reset and reuse the timer (i.e. goto #2)  4.（可选）重置并重新使用计时器（即转到2）
5. `zx_handle_close()`  5.`zx_handle_close（）`

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_timer_create()`] - create a timer  -[`zx_timer_create（）`]-创建一个计时器
 - [`zx_timer_set()`] - set a timer  -[`zx_timer_set（）`]-设置一个计时器
 - [`zx_timer_cancel()`] - cancel a timer  -[`zx_timer_cancel（）`]-取消计时器

 
## SEE ALSO  也可以看看 

 
+ [timer slack](/docs/concepts/objects/timer_slack.md)  + [计时器松弛]（/ docs / concepts / objects / timer_slack.md）

