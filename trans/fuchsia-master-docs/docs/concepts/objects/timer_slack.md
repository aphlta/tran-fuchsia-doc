 
# Timer Slack  计时器松弛 

[Timer objects](/docs/concepts/objects/timer.md) have a concept of slack. Slack defines how the system may alter the timer's deadline. Slack allowsthe system to internally coalesce timers and timer-like events toimprove performance or efficiency. [计时器对象]（/ docs / concepts / objects / timer.md）具有松弛的概念。松弛度定义系统如何​​更改计时器的期限。松弛允许系统在内部合并计时器和类似计时器的事件，以提高性能或效率。

Slack is made up of two components, type and amount. Type describes how slack can be applied: 松弛由类型和数量两个部分组成。类型描述了松弛的应用方式：

 
+ **ZX_TIMER_SLACK_CENTER** coalescing is allowed with earlier and later timers. + ** ZX_TIMER_SLACK_CENTER **允许早期和之后的计时器合并。
+ **ZX_TIMER_SLACK_EARLY** coalescing is allowed only with earlier timers. + ** ZX_TIMER_SLACK_EARLY **仅在较早的计时器中才允许合并。
+ **ZX_TIMER_SLACK_LATE** coalescing is allowed only with later timers. + ** ZX_TIMER_SLACK_LATE **仅在以后的计时器中允许合并。

Amount is the allowed deviation from the deadline. For example, a timer with **ZX_TIMER_SLACK_EARLY** and 5us may fire up to 5us beforeits deadline. A timer with **ZX_TIMER_SLACK_CENTER** and 7ms may fireanywhere from 7ms before its deadline to 7ms after its deadline. 金额是与截止日期的允许偏差。例如，一个具有** ZX_TIMER_SLACK_EARLY **和5us的计时器可能会在截止日期之前触发最多5us。具有** ZX_TIMER_SLACK_CENTER **和7ms的计时器可以从截止日期前的7ms到截止日期后的7ms的任意时间触发。

 
## Timer-like Syscalls  类似于计时器的系统调用 

Slack may also be applied to blocking syscalls that accept a deadline argument, like [`zx_nanosleep()`]. Slack也可用于阻止接受截止参数的系统调用，例如[`zx_nanosleep（）]。

 
## Defaults and Job Policy  默认值和作业策略 

For Timer objects, slack is specified when creating and setting timers. For other syscalls that take a deadline, but no slackparameters, the slack type and amount are specified by the job'spolicy. See [`zx_job_set_policy()`]. 对于Timer对象，在创建和设置计时器时指定了松弛。对于需要截止日期但没有松弛参数的其他系统调用，松弛类型和数量由作业的策略指定。参见[`zx_job_set_policy（）`]。

