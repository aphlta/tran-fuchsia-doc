Zircon Scheduling ================= 锆石调度=================

Background ========== 背景==========

The primary responsibility of any scheduler is to share the limited resource of processor time between all threads that wish to use it. In ageneral purpose operating system, it tries to do so in a fair way,ensuring that all threads are allowed to make some progress. 任何调度程序的主要职责是在希望使用它的所有线程之间共享有限的处理器时间资源。在通用操作系统中，它尝试以公平的方式这样做，以确保允许所有线程取得一定的进展。

Our scheduler is an evolution of LK’s scheduler. As such it started as a minimal scheduler implementation and was extended to meetour needs as the project grew. 我们的调度程序是LK调度程序的改进。因此，它起初只是一个最小的调度程序实施，随着项目的发展，扩展到满足我们的需求。

Design ====== 设计======

 
#### Overview  总览 

In essence there is a scheduler running on each logical CPU in the machine. These schedulers run independently and use IPI (Inter-ProcessorInterrupts) to coordinate. However each CPU is responsible forscheduling the threads that are running on it. See [*CPUAssignment*](#cpu-assignment-and-migration) below for how we decidewhich CPU a thread is on, and how/when it migrates. 本质上，机器中的每个逻辑CPU上都有一个调度程序。这些调度程序独立运行，并使用IPI（处理器间中断）进行协调。但是，每个CPU负责调度在其上运行的线程。有关我们如何确定线程在哪个CPU上以及如何/何时进行迁移的信息，请参见下面的[* CPUAssignment *]（CPU分配和迁移）。

Each CPU has its own set of priority queues. One for each priority level in the system, currently 32. Note that these are fifo queues, not the datastructure known as a priority queue. In each queue is an ordered list ofrunnable threads awaiting execution. When it is time for a new thread to run,the scheduler simply looks at the highest numbered queue that contains a thread,pops the head off of that queue and runs that thread.See[*Priority Management*](#priority-management) below for more detailsabout how it decides which thread should be in which queue. If there are nothreads in the queues to run it will instead run the idle thread, see [*Realtimeand Idle Threads*](#realtime-and-idle-threads) below for more details. 每个CPU都有其自己的优先级队列集。系统中每个优先级一个，当前为32。请注意，这些是fifo队列，而不是称为优先级队列的数据结构。每个队列中都有一个等待执行的可运行线程的有序列表。当需要运行一个新线程时，调度程序会简单地查看包含线程的编号最高的队列，将队列的头部弹出并运行该线程。请参见下面的[* Priority Management *]（优先级管理）有关如何决定哪个线程应该在哪个队列中的更多详细信息。如果队列中没有要运行的线程，它将改为运行空闲线程，有关更多详细信息，请参见下面的[* Realtime和Idle Threads *]（实时和空闲线程）。

Each thread is assigned the same timeslice size (THREAD_INITIAL_TIME_SLICE) when it is picked to start running. If it uses its whole timeslice it will bereinserted at the end of the appropriate priority queue. However if it hassome of its timeslice remaining from a previous run it will be inserted at thehead of the priority queue so it will be able to resume as quickly as possible.When it is picked back up again it will only run for the remainder of itsprevious timeslice. 选取每个线程开始运行时，每个线程都分配有相同的时间片大小（THREAD_INITIAL_TIME_SLICE）。如果使用整个时间片，它将在适当的优先级队列的末尾重新插入。但是，如果它的时间片有上次运行的剩余时间，它将被插入优先级队列的开头，这样它就可以尽快恢复。再次取回它时，它将只运行其先前的剩余时间时间片。

When the scheduler selects a new thread from the priority queue it sets the CPU's preemption timer for either a full timeslice, or the remainder of theprevious timeslice. When that timer fires the scheduler will stop execution onthat thread, add it to the appropriate queue, select another thread and startover again. 当调度程序从优先级队列中选择新线程时，它将为完整的时间片或之前时间片的其余部分设置CPU的抢占计时器。当计时器触发时，调度程序将停止在该线程上执行，将其添加到适当的队列中，选择另一个线程并再次启动。

If a thread blocks waiting for a shared resource then it's taken out of its priority queue and is placed in a wait queue for the shared resource.When it is unblocked it will be reinserted in the appropriate priorityqueue of an eligible CPU ([*CPUAssignment*](#cpu-assignment-and-migration)) and if it had remaining timesliceto run it will be added to the front of the queue for expedited handling. 如果线程阻塞了等待共享资源的线程，那么它将被从其优先级队列中取出，并放置在等待共享资源的队列中。取消阻塞时，它将被重新插入到合格CPU的适当优先级队列中（[* CPUAssignment * ]（cpu-assignment-and-migration），如果还有剩余的时间片要运行，它将被添加到队列的最前面以加快处理速度。

 
#### Priority Management  优先管理 

There are three different factors used to determine the effective priority of a thread, the effective priority being what is used todetermine which queue it will be in. 有三种不同的因素可用来确定线程的有效优先级，有效优先级是用来确定线程将进入哪个队列的。

The first factor is the base priority, which is simply the thread’s requested priority. There are currently 32 levels with 0 being thelowest and 31 being the highest. 第一个因素是基本优先级，它只是线程的请求优先级。当前有32个级别，其中0最低，31最高。

The second factor is the priority boost. This is a value bounded between \[-MAX_PRIORITY_ADJ, MAX_PRIORITY_ADJ\] used to offset the base priority, it ismodified by the following cases: 第二个因素是优先级提升。这是一个用于偏移基本优先级的\ [-MAX_PRIORITY_ADJ，MAX_PRIORITY_ADJ \]之间的值，在以下情况下会对其进行修改：

 
-   When a thread is unblocked, after waiting on a shared resource or sleeping, it is given a one point boost. -当线程被解除阻塞时，在等待共享资源或休眠后，线程将获得单点提升。

 
-   When a thread yields (volunteers to give up control), or volunteers to reschedule, its boost is decremented by one but is capped at 0(won’t go negative). -当某个线程退出（自愿者放弃控制权）或自愿重新安排时间时，其提升会减少1，但上限为0（不会变为负数）。

 
-   When a thread is preempted and has used up its entire timeslice, its boost is decremented by one but is able to go negative. -当一个线程被抢占并用尽其整个时间片时，其增强将减一，但可以变为负数。

The third factor is its inherited priority. If the thread is in control of a shared resource and it is blocking another thread of a higherpriority then it is given a temporary boost up to that thread’s priorityto allow it to finish quickly and allow the higher priority thread toresume. 第三个因素是其继承的优先级。如果该线程控制着共享资源，并且阻塞了另一个更高优先级的线程，则可以暂时提高该线程的优先级，以使其能够快速完成并允许更高优先级的线程恢复。

The effective priority of the thread is either the inherited priority, if it has one, or the base priority plus its boost. When this prioritychanges, due to any of the factors changing, the scheduler will move itto a new priority queue and reschedule the CPU. Allowing it to havecontrol if it is now the highest priority task, or relinquish control ifit is no longer highest. 线程的有效优先级是继承的优先级（如果有的话），或者是基本优先级加上其提升。当此优先级更改时，由于任何因素的更改，调度程序会将其移至新的优先级队列并重新调度CPU。如果现在是最高优先级的任务，则允许它控制；如果不再是最高优先级，则放弃控制。

The intent in this system is to ensure that interactive threads are serviced quickly. These are usually the threads that interact directlywith the user and cause user-perceivable latency. These threads usuallydo little work and spend most of their time blocked awaiting anotheruser event. So they get the priority boost from unblocking whilebackground threads that do most of the processing receive the prioritypenalty for using their entire timeslice. 该系统的目的是确保交互式线程得到快速服务。这些通常是与用户直接交互并导致用户可察觉的延迟的线程。这些线程通常很少工作，并且大部分时间都在等待另一个用户事件时被阻塞。因此，它们通过解除阻塞而获得优先级提升，而执行大多数处理的后台线程因使用其整个时间片而受到优先级惩罚。

 
#### CPU Assignment and Migration  CPU分配和迁移 

Threads are able to request which CPUs on which they wish to run using a CPU affinity mask, a 32 bit mask where 0b001 is CPU 1, 0b100 is CPU 3,and 0b101 is either CPU 1 or CPU 3. This mask is usually respected butif the CPUs it requests are all inactive it will be assigned to anotherCPU. Also notable, if it is “pinned” to a CPU, that is its mask containsonly one CPU, and that CPU becomes inactive the thread will situnserviced until that CPU becomes active again. See [*CPUActivation*](#cpu-activation) below for details. 线程能够使用CPU亲缘性掩码，32位掩码（其中0b001是CPU 1、0b100是CPU 3、0b101是CPU 1或CPU 3）来请求它们希望在哪些CPU上运行。它请求的所有CPU均处于非活动状态，它将分配给另一个CPU。同样值得注意的是，如果将其“固定”到CPU，即其掩码仅包含一个CPU，并且该CPU变为非活动状态，则该线程将处于未服务状态，直到该CPU再次变为活动状态。有关详细信息，请参见下面的[* CPUActivation *]（cpu-activation）。

When selecting a CPU for a thread the scheduler will choose, in order:  为线程选择CPU时，调度程序将按以下顺序选择：

 
1.  The CPU doing the selection, if it is **idle** and in the affinity mask.  1.如果选择的是“ idle”（空闲），则在关联掩码中，CPU会进行选择。

 
2.  The CPU the thread last ran on, if it is **idle** and in the affinity mask.  2.上次运行线程的CPU（如果它是idle **）并在关联掩码中。

 
3.  Any **idle** CPU in the affinity mask.  3.关联掩码中的任何“空闲” CPU。

 
4.  The CPU the thread last ran on, if it is active and in the affinity mask.  4.线程上次运行的CPU（如果处于活动状态）在关联掩码中。

 
5.  The CPU doing the selection, if it is the only one in the affinity mask or all cpus in the mask are not active. 5.如果选择是在亲和力掩码中唯一的CPU或掩码中的所有cpus都不活动，则正在进行选择的CPU。

 
6.  Any active CPU in the affinity mask.  6.相似性掩码中的所有活动CPU。

If the thread is running on a CPU not in its affinity mask (due to case 5 above) the scheduler will try to rectify this every time the thread ispreempted, yields, or voluntarily reschedules. Also if the threadchanges its affinity mask the scheduler may migrate it. 如果线程不在其亲和力掩码中（而不是上面的情况5）在CPU上运行，则每次线程被抢占，产生或自动重新调度时，调度程序都将尝试纠正此问题。同样，如果线程更改其亲和力掩码，则调度程序可以迁移它。

Every time a thread comes back from waiting on a shared resource or sleeping and needs to be assigned a priority queue, the scheduler willre-evaluate its CPU choice for the thread, using the above logic, andmay move it. 每当线程因等待共享资源或睡眠而返回并且需要分配优先级队列时，调度程序将使用上述逻辑重新评估其对线程的CPU选择，然后移动它。

 
#### CPU Activation  CPU激活 

When a CPU is being deactivated, that is shutdown and removed from the system, the scheduler will transition all running threads onto otherCPUs. The only exception is threads that are “pinned”, that is they onlyhave the deactivating CPU in their affinity mask, these threads are putback into the run queue where they will sit unserviced until the CPU isreactivated. 当一个CPU被停用时，即被关闭并从系统中删除，调度程序会将所有正在运行的线程转换到其他CPU上。唯一的例外是“固定”线程，也就是说，它们仅在其亲和力掩码中具有正在停用的CPU，这些线程被放回到运行队列中，在该队列中它们将不再处于服务状态，直到重新激活CPU。

When a CPU is reactivated it will service the waiting pinned threads and threads that are running on non-Affinity CPUs should be migrated backpretty quickly by their CPUs scheduler due to the above rules. There isno active rebalancing of threads to the newly awakened CPU, but as itshould be idle more often, it should see some migration due to the logiclaid out above in [*CPU Assignment andMigration*](#cpu-assignment-and-migration). 重新激活CPU后，它将为等待的固定线程提供服务，由于上述规则，非亲和CPU上运行的线程应由其CPU调度程序快速反向迁移。没有对新唤醒的CPU进行主动的线程重新平衡，但是由于它应该更频繁地处于空闲状态，因此由于[* CPU Assignment and Migration *]（cpu-assignment-and-migration）中上面列出的逻辑，它应该会看到一些迁移。

 
#### Realtime and Idle Threads  实时和空闲线程 

These are special threads that are treated a little differently.  这些是特殊线程，它们的处理方式有所不同。

The idle thread runs when no other threads are runnable. There is one on each CPU and it lives outside of the priority queues, but effectively ina priority queue of -1. It is used to track idle time and can be used byplatform implementations for a low power wait mode. 当没有其他线程可运行时，空闲线程将运行。每个CPU上只有一个，它位于优先级队列之外，但实际上在优先级队列-1中。它用于跟踪空闲时间，并且平台实现可将其用于低功耗等待模式。

