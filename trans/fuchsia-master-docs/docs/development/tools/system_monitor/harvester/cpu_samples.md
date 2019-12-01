 
# CPU Samples  CPU样本 

The [Harvester](README.md) gathers a collection of CPU samples from each CPU on the device. This document describes how the data is labelled and what the valuesrepresent. [Harvester]（README.md）从设备上的每个CPU收集CPU样本的集合。本文档介绍了如何标记数据以及值的含义。

 
##### Dockyard Paths  船坞路径 

The path to each sample will include "cpu", the processor index, and the sample name: e.g. "cpu:0:busy_time". 每个样本的路径将包括“ cpu”，处理器索引和样本名称： “ cpu：0：busy_time”。

 
### Samples  样品 

Data collected by the Harvester along with timestamp and a Dockyard Path is called a Sample. The following sections describe CPU samples collected. They aregrouped in four broad categories. 收割机连同时间戳记和船坞路径一起收集的数据称为样本。以下各节描述了收集的CPU示例。它们分为四大类。

 
#### Load  加载 

The busy and idle times are complementary. The busy time is derived from the idle time. 忙/闲时间是相辅相成的。繁忙时间是从空闲时间得出的。

 
##### cpu:count  cpu：计数The number of main CPUs. For the "cpu:\*:" sample paths the "\*" will be a number from 0 to (cpu:count - 1). 主CPU的数量。对于“ cpu：\ *：”示例路径，“ \ *”将是一个从0到（cpu：count-1）的数字。

 
##### cpu:\*:busy_time  cpu：\ *：busy_timeThe total accumulated time this processor has been busy.  该处理器繁忙的总累积时间。

 
##### cpu:\*:idle_time  cpu：\ *：idle_timeThe total accumulated time this processor was not doing work (not running any threads). 该处理器不工作（不运行任何线程）的总累积时间。

 
#### Kernel scheduler counters  内核调度程序计数器 

The scheduler schedules threads. It determines which thread a given CPU should be running. 调度程序调度线程。它确定给定的CPU应该运行哪个线程。

 
##### cpu:\*:reschedules  cpu：\ *：重新安排How many potential context_switches occurred. All context_switches are preceded by a reschedule, but not all reschedules result in a context_switch. 发生了多少个潜在的context_switchs。所有context_switch都带有重排，但并非所有重排都会导致context_switch。

 
##### cpu:\*:context_switches  cpu：\ *：context_switchesHow many thread switches have occurred. A high value may indicate threads are thrashing (spending an inordinate amount of time switching places ratherthan doing work). 发生了多少个线程切换。较高的值可能表明线程正在抖动（花费过多的时间切换位置而不是工作）。

 
##### cpu:\*:meaningful_irq_preempts  cpu：\ *：含义ful_irq_preemptsHow many thread preemptions have occurred due to an interrupt (irq) while the CPU is not idle. If the thread is idle the interrupt is not consideredmeaningful and is not tracked here. 当CPU不空闲时，由于中断（irq）而发生了多少线程抢占。如果线程空闲，则中断不被认为是有意义的，因此不在此处跟踪。

 
##### cpu:\*:preempts  cpu：\ *：抢占How many thread preemptions have occurred. (Not currently used).  发生了多少个线程抢占。 （当前未使用）。

 
##### cpu:\*:yields  cpu：\ *：收益How many times a thread has yielded its use of a processor to allow another thread to execute. 一个线程放弃使用处理器以允许另一个线程执行多少次。

 
#### CPU level interrupts and exceptions  CPU级别的中断和异常 

An interrupt causes the current flow of a thread to be "interrupted". The thread is stopped, the state is preserved (so it can be resumed) and the processorexecutes an interrupt handler (function). 中断导致线程的当前流被“中断”。线程停止，状态被保留（以便可以恢复），处理器执行中断处理程序（函数）。

 
##### cpu:\*:external_hardware_interrupts  cpu：\ *：external_hardware_interruptsExternal hardware interrupts indicate a signal or event happening outside of the machine. Common examples are serial input, or a physical button like avolume up or down button. Does not include timer or inter-processor interrupts. 外部硬件中断表示机器外部发生信号或事件。常见的示例是串行输入，或者是物理按钮，例如音量增大或减小按钮。不包括计时器或处理器间中断。

 
##### cpu:\*:timer_interrupts  cpu：\ *：timer_interruptsA timer interrupt occurs when a "clock" (or some kind of time keeping device) creates an interrupt. 当“时钟”（或某种计时设备）创建中断时，将发生计时器中断。

 
##### cpu:\*:timer_callbacks  cpu：\ *：timer_callbacksHow many times a function (callback) has been called due to a timer. Each time a timer interrupt occurs, zero-to-many timer callbacks may be called. 由于计时器而已调用一个函数（回调）多少次。每次发生计时器中断时，都可以调用零到多个计时器回调。

 
##### cpu:\*:syscalls  cpu：\ *：syscallsHow many system (kernel) API calls have been made.  已经进行了多少次系统（内核）API调用。

 
#### Inter-processor interrupts  处理器间中断 

An inter-processor interrupt occurs when a processor signals another processor.  当一个处理器向另一个处理器发出信号时，发生处理器间中断。

 
##### cpu:\*:reschedule_ipis  cpu：\ *：reschedule_ipisThe count of times the scheduler (running on some CPU) has requested a schedule change (waking up another CPU). 调度程序（在某些CPU上运行）请求更改日程表（唤醒另一个CPU）的次数。

 
##### cpu:\*:generic_ipis  cpu：\ *：generic_ipisThe count of inter-process interrupts that were not a schedule change (tracked as reschedule_ipis), ipi interrupt (untracked), or ipi halt (untracked). 不是计划更改（跟踪为reschedule_ipis），ipi中断（未跟踪）或ipi暂停（未跟踪）的进程间中断的计数。

