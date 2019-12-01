 
# Zircon Fair Scheduler  Zircon Fair Scheduler 

 
## Introduction  介绍 

As part of the overall scheduler development effort, Zircon is moving to a new fair scheduler as the primary scheduler for the system. This document discussesthe properties of the scheduler and how to enable it for testing prior toroll-out. 作为整个调度程序开发工作的一部分，Zircon正在迁移到新的公平调度程序作为系统的主要调度程序。本文档讨论了调度程序的属性以及如何启用它以在推出之前进行测试。

 
## Enabling the Fair Scheduler  启用公平调度程序 

The fair scheduler is disabled by default. The new scheduler is enabled at compile time by setting the GN build argument `enable_fair_scheduler` to true. 默认情况下，公平调度程序是禁用的。通过将GN构建参数`enable_fair_scheduler`设置为true，可以在编译时启用新的调度程序。

You can set this variable in your GN invocation like this:  您可以像这样在GN调用中设置此变量：

```
gn gen build-zircon --args='enable_fair_scheduler=true'
```
 

 
## Detailed Scheduler Tracing  详细的调度程序跟踪 

The new scheduler includes detailed tracing instrumentation to analyze the behavior of the scheduler and its interaction with and impact on the competingworkloads in the system. Detailed tracing is enabled at compile time by settingthe GN build argument `detailed_scheduler_tracing` to true. 新的调度程序包括详细的跟踪工具，以分析调度程序的行为及其与系统中竞争性工作负载的相互作用以及对它们的影响。通过将GN构建参数`detailed_scheduler_tracing'设置为true，可以在编译时启用详细跟踪。

You can set this variable in your GN invocation like this:  您可以像这样在GN调用中设置此变量：

```
gn gen build-zircon --args='enable_fair_scheduler=true detailed_scheduler_tracing=true'
```
 

Use the `kernel:sched` trace category to include the detailed scheduler information in your trace session. It's a good idea to also include the`kernel:irq` category because interrupts can cause scheduler activity that mightotherwise appear unconnected to other events. 使用`kernel：sched`跟踪类别在跟踪会话中包含详细的调度程序信息。最好也包含kernel：irq类别，因为中断会导致调度程序活动，而该活动可能与其他事件无关。

```
fx traceutil record -categories kernel:sched,kernel:irq,<other categories> -stream -duration 4s -buffer-size 64
```
 

 
### Summary of Scheduler Events  调度程序事件摘要 

The detailed scheduler events are primarily duration and flow events. The events appear in Chromium Trace Viewer in the timelines labeled `cpu-0`through `cpu-N`, where `N` is the number of CPUs in the system. These timelinesrepresent per-CPU activity in the kernel, which includes interrupts andthread scheduling. 详细的调度程序事件主要是持续时间和流事件。这些事件出现在Chromium Trace Viewer中的时间轴上，标记为“ cpu-0”到“ cpu-N”，其中“ N”是系统中的CPU数量。这些时间线表示内核中每个CPU的活动，其中包括中断和线程调度。

The fair scheduler emits duration events including the following:  公平调度程序发出持续时间事件，包括以下内容：
* **sched_block**: The active thread blocks on a Zircon object, futex, kernel-internal lock. * sched_block **：Zircon对象上的活动线程块，futex，内核内部锁。
* **sched_unblock**: The active thread unblocks another thread due to interacting with a Zircon object, futex, or kernel-internal lock. * sched_unblock **：活动线程由于与Zircon对象，futex或内核内部锁的交互而解除了对另一个线程的阻塞。
* **sched_unblock_list**: A variation of **sched_block** when the action of the active thread may wake one or more threads at once (e.g.`wait_queue_wake_all`). * sched_unblock_list **：当活动线程的操作可能一次唤醒一个或多个线程时（例如，wait_queue_wake_all），是sched_block **的变体。
* **sched_yield**: The active thread called `zx_thread_yield`.  * sched_yield **：活动线程称为`zx_thread_yield`。
* **sched_preempt**: An interrupt requests re-evaluation of the run queue. This is due to either the time slice timer expiring, another CPU requesting areschedule after modifying the CPU's run queue, or a hardware interrupthandler waking up a thread on the CPU. * ** sched_preempt **：中断请求重新评估运行队列。这是由于时间片计时器到期，修改了CPU的运行队列后另一个CPU请求调度，或者是硬件中断处理程序唤醒了CPU上的线程。
* **sched_reschedule**: A kernel operation changed the run queue of the current CPU and a different thread _might_ need to run. *** sched_reschedule **：内核操作更改了当前CPU的运行队列，并且需要运行另一个线程_might_。

The fair scheduler emits flow events including the following:  公平调度程序发出流事件，包括以下内容：
* **sched_latency**: A flow that connects the point in time right after a thread enters the run queue to the point in time right before the (potentiallydifferent) target CPU context switches to the thread. This flow event isuseful for visualizing cross-CPU scheduling activity and observing therunnable-to-running scheduler latency of a thread at any point in time. * ** sched_latency **：一种将线程进入运行队列之后的时间点连接到（可能不同的）目标CPU上下文切换到线程之前的时间点的流。此流事件可用于可视化跨CPU调度活动并观察线程在任何时间点的可运行到运行的调度程序延迟。

A NOTE ABOUT FLOW EVENTS: Sometimes displaying flow events is not enabled by default in Chromium Trace Viewer. Use the `View Options` menu in the upper rightcorner of the page and make sure the `Flow events` checkbox is checked. 关于流事件的注意事项：有时在Chromium Trace Viewer中默认情况下未启用显示流事件。使用页面右上角的“查看选项”菜单，并确保选中“流事件”复选框。

You can also disable flow events display if there are too many and the rendering becomes too slow. Try zooming into a smaller region before enabling flow eventdisplay for better performance in very large traces. 如果太多并且渲染变得太慢，也可以禁用流事件显示。在启用流事件显示之前，请尝试放大到较小的区域，以在很大的迹线中获得更好的性能。

 
## Fair Scheduling Overview  公平计划概述 

Fair scheduling is a discipline that divides CPU bandwidth between competing threads, such that each receives a weighted proportion of the CPU over time.In this discipline, each thread is assigned a weight, which is somewhat similarto a priority in other scheduling disciplines. Threads receive CPU time inproportion to their weight, relative to the weights of other competing threads.This proportional bandwidth distribution has useful properties that make fairscheduling a good choice as the primary scheduling discipline in a generalpurpose operating system. 公平调度是一种在竞争线程之间划分CPU带宽的规则，以便每个线程随时间获得加权比例的CPU。在此规则中，为每个线程分配一个权重，这在某种程度上类似于其他调度规则中的优先级。与其他竞争线程的权重相比，线程得到的CPU时间与其权重成比例。此比例带宽分配具有有用的属性，使得公平调度成为通用操作系统中的主要调度准则是一个不错的选择。

Briefly, these properties are:  简而言之，这些属性是：
* **Intuitive bandwidth allocation mechanism**: A thread with twice the weight of another thread will receive approximately twice the CPU time, relative tothe other thread over time. Whereas, a thread with the same weight as anotherwill receive approximately the same CPU time, relative to the other threadover time. * **直观的带宽分配机制**：一个线程的权重是另一个线程的两倍，相对于一段时间而言，该时间将是另一个线程的两倍。相对于其他线程转换时间，权重相同的线程将获得大约相同的CPU时间。
* **Starvation free for all threads**: Proportional bandwidth division ensures that all competing threads receive CPU time in a timely manner, regardless ofhow low the thread weight is relative to other threads. Notably, this propertyprevents unbounded priority inversion. * **所有线程无饥饿**：比例带宽划分确保所有竞争线程及时获得CPU时间，无论线程权重与其他线程相比有多低。值得注意的是，此属性可防止无限优先级反转。
* **Fair response to system overload**: When the system is overloaded, all threads share proportionally in the slowdown. Solving overload conditions isoften simpler than managing complex priority interactions required in otherscheduling disciplines. * **对系统过载的正常响应**：当系统过载时，所有线程在减速中按比例共享。解决过载条件通常比管理其他计划学科中所需的复杂优先级交互更为简单。
* **Stability under evolving demands**: Adapts well to a wide range of workloads with minimal intervention compared to other scheduling disciplines. * **不断变化的需求下的稳定性**：与其他调度规则相比，以最少的干预即可很好地适应各种工作负载。

A NOTE ABOUT DEADLINES: While fair scheduling is appropriate for the vast majority of workloads, there are some tasks that require very specific timingand/or do not adapt well to overload conditions. For example, these workloadsinclude low-latency audio / graphics, high-frequency sensors, and high-rate /low-latency networking. These specialized tasks are better served with adeadline scheduler, which is planned for later in the Zircon schedulerdevelopment cycle. 关于截止时间的注意事项：尽管合理的调度适用于绝大多数工作负载，但有些任务需要非常特定的时间安排和/或不能很好地适应过载情况。例如，这些工作负载包括低延迟音频/图形，高频传感器和高速率/低延迟网络。 adeadline计划程序可以更好地服务这些专门任务，该计划将在Zircon计划程序开发周期的后期进行计划。

 
## Fair Scheduling in Zircon  锆石的公平调度 

The Zircon fair scheduler is based primarily on the Weighted Fair Queuing (WFQ) discipline, with insights from other similar queuing and scheduling disciplines.Adopting aspects of the Worst-Case Fair Weighted Fair Queuing (WF2Q) discipline,a modification of WFQ, is planned to improve control over tuning of latencyversus throughput. Zircon公平调度程序主要基于加权公平排队（WFQ）学科，并从其他类似的排队和调度学科中获得见解。改善对延迟与吞吐量调整的控制。

The following subsections outline the algorithm as implemented in Zircon. From here on, "fair scheduler" and "Zircon fair scheduler" are used interchangeably. 以下小节概述了在Zircon中实现的算法。从这里开始，“公平调度器”和“锆石公平调度器”可互换使用。

 
### Ordering Thread Execution  订购螺纹执行 

One of the primary jobs of the scheduler is to decide which order to execute competing threads on the CPU. The fair scheduler makes these decisionsseparately on each CPU. Essentially, each CPU runs a separate instance of thescheduler and manages its own run queue. 调度程序的主要工作之一是确定在CPU上执行竞争线程的顺序。公平调度程序在每个CPU上分别做出这些决定。本质上，每个CPU运行一个单独的调度程序实例并管理自己的运行队列。

In this approach, a thread may compete only on one CPU at a time. A thread can be in one of three states: _ready_, _running_ or _blocked_ (other states are notrelevant to this discussion.) For each CPU, at most one thread is in the_running_ state at any time: this thread executes on the CPU, all othercompeting threads await execution in the _ready_ state, while blocked threadsare not in competition. The threads in the _ready_ state are enqueued in theCPU's run queue; the order of threads in the run queue determines which threadruns next. 在这种方法中，线程一次只能在一个CPU上竞争。线程可以处于以下三种状态之一：_ready_，_running_或_blocked_（其他状态与本讨论无关。）对于每个CPU，任何时候最多一个线程处于[running_]状态：该线程在CPU上执行，所有其他竞争线程在_ready_状态下等待执行，而阻塞的线程则不参与竞争。处于_ready_状态的线程排入CPU的运行队列；运行队列中的线程顺序确定下一个运行的线程。

The fair scheduler, unlike **O(1)** scheduling disciplines such as priority round-robin (RR), uses an ordering criteria to compare and order threads in therun queue. This is implemented using a balanced binary tree, and means thatscheduling decisions generally cost **O(log n)** to perform. While this is moreexpensive than an **O(1)** scheduler, the result is a near-optimal worst casedelay bound (queuing time) for all competing threads. 公平调度程序与诸如优先级轮询（RR）之类的** O（1）**调度规则不同，它使用排序标准对运行队列中的线程进行比较和排序。这是使用平衡的二叉树实现的，这意味着调度决策通常要花费** O（log n）**。尽管这比** O（1）**调度程序更昂贵，但是对于所有竞争线程，结果是接近最佳的最坏情况延迟范围（排队时间）。

 
### Ordering Criteria  订购标准 

Two concepts are used to order threads in the run queue: _virtual timeline_ and per-thread _normalized rate_. The _virtual timeline_ tracks when each thread inthe run queue would finish a _normalized time slice_ if it ran to completion.A _normalized time slice_ is proportional to the thread's _normalized rate_,which in turn is inversely proportional to the thread's weight. Threads areordered in the run queue by ascending _finish time_ in the _virtual timeline_. 使用两个概念对运行队列中的线程进行排序：_virtual timeline_和每个线程_normalized rate_。 _virtual timeline_跟踪运行队列中的每个线程何时运行完成的_normalized time slice_。_normalized time slice_与线程的_normalized rate_成正比，而_normalized rate_与线程的权重成反比。通过在_virtual时间轴_中提升_finish time_来在运行队列中对线程进行排序。

The inverse proportional relationship to weight causes higher weighed threads to be inserted closer to the front of the run queue than lower weighted threadswith similar arrival times. However, this is bounded over time: the longer athread waits in the run queue, the less likely a newly arriving thread, howeverhighly weighted, will be inserted before it. This property is key to thefairness of the scheduler. 与重量成反比的关系会导致高权重的线程比具有相似到达时间的低权重的线程更靠近运行队列的前端插入。但是，这是有时间限制的：线程在运行队列中等待的时间越长，新到达的线程（无论权重如何高）插入它的可能性就越小。此属性是调度程序公平性的关键。

The following sections define the scheduler in more precise terms.  以下各节以更精确的术语定义了调度程序。

 
### Per-Thread Scheduling State  每线程调度状态 

For each thread **P[i]** we define the following state:  对于每个线程** P [i] **，我们定义以下状态：
* Weight **w[i]**: Real number representing the relative weight of the thread.  *重量** w [i] **：实数，表示线的相对重量。
* Start Time **s[i]**: The start time of the thread in the CPU's virtual timeline. *开始时间** s [i] **：CPU的虚拟时间线中线程的开始时间。
* Finish Time **f[i]**: The finish time of the thread in the CPU's virtual timeline. *完成时间** f [i] **：CPU的虚拟时间线中线程的完成时间。
* Time Slice **t[i]**: The size of the time slice for the current period.  *时间片** t [i] **：当前时间段的时间片大小。

 
### Per-CPU Scheduling State  每CPU调度状态 

For each CPU **C[j]** we define the following state:  对于每个CPU ** C [j] **，我们定义以下状态：
* Number of Threads **n[j]**: The number of runnable threads competing on the CPU. *线程数** n [j] **：CPU上竞争的可运行线程数。
* Scheduling Period **p[j]**: The period in which all competing threads on the CPU execute approximately once. *调度周期** p [j] **：CPU上所有竞争线程大约执行一次的周期。
* Total Weight **W[j]**: The sum of the weights of the threads competing on the CPU. * Total Weight ** W [j] **：在CPU上竞争的线程的权重之和。

When a thread enters competition for a CPU, its weight is added to the CPU's total weight. Likewise, when a thread blocks or is migrated to another CPU thethread's weight is subtracted from the CPU's total weight. The total includesthe weights of the _ready_ threads and the current _running_ thread. 当线程进入争用CPU的竞争时，其权重将添加到CPU的总权重中。同样，当一个线程阻塞或迁移到另一个CPU时，该线程的权重将从CPU的总权重中减去。总数包括_ready_线程和当前_running_线程的权重。

 
### Tunable State  可调状态 

We define the following tunable state, which may either be global or per-CPU:  我们定义以下可调状态，该状态可以是全局或每个CPU：
* Minimum Granularity **M**: The smallest time slice allocated to any thread.  *最小粒度** M **：分配给任何线程的最小时间片。
* Target Latency **L**: The target scheduling period for the CPU unless there are too many threads to give each thread as least one minimum granularity timeslice. * Target Latency ** L **：CPU的目标调度周期，除非线程太多，以至于不能给每个线程至少一个最小粒度时间片。

 
### Definitions  定义 

We define the following relationships for the key scheduler variables:  我们为关键调度程序变量定义以下关系：

 
#### Scheduling Period  计划期 

The scheduling period controls the size of time slices. When there are few threads competing, the scheduling period defaults to the _target latency_. Thisresults in larger time slices and fewer preemptions, improving throughput andpotentially power consumption. When the number of threads is too large thescheduling period stretches such that each task receives at least the _minimumgranularity_ time slice. 调度周期控制时间片的大小。当竞争的线程很少时，调度周期默认为_target等待时间_。这导致更长的时间片和更少的抢占，从而提高了吞吐量并潜在地降低了功耗。当线程数太大时，调度周期会延长，以至于每个任务至少会收到_minimuranularity_个时间片。

Let **N** be the maximum number of competing threads before period stretching.  令** N **为周期延长之前竞争线程的最大数量。

**N** = floor(**L** / **M**)  ** N ** =地板（** L ** / ** M **）

**p[j]** = **n[j]** > **N** --> **M** * **n[j]**, **L**  ** p [j] ** = ** n [j] **> ** N **-> ** M ** * ** n [j] **，** L **

 
#### Virtual Timeline  虚拟时间表 

When a thread enters the run queue, either by newly joining the competition for the CPU or completing a time slice, the thread's _virtual_ start and finish timeare computed. As the current fair scheduler is based on WFQ, the finish time isused to select the position for the thread in the run queue relative to otherthreads. Later, when WF2Q is implemented, both the start and finish time areconsidered. 当线程进入运行队列时，通过新加入CPU竞争或完成时间片来计算线程的_virtual_开始和结束时间。由于当前的公平调度程序基于WFQ，因此需要使用完成时间来选择线程在运行队列中相对于其他线程的位置。稍后，当实施WF2Q时，将同时考虑开始时间和结束时间。

Some WFQ implementations use the thread's actual time slice to calculate the _normalized time slice_ for the timeline. However, the actual time slice dependson the total weight of the CPU (see below), a value that changes as threads entercompetition. The Zircon fair scheduler instead uses the scheduling period as anidealized uniform time slice for the _virtual timeline_, because its valuechanges less dramatically. Using a uniform value for all threads avoids skewingthe _virtual timeline_ unfairly in favor threads that join early. 一些WFQ实现使用线程的实际时间片来计算时间轴的_normalized time slice_。但是，实际时间片取决于CPU的总重量（请参见下文），该值随着线程进入竞争状态而改变。 Zircon公平调度程序将调度周期用作_virtual timeline_的理想统一时间片，因为它的值变化不大。为所有线程使用统一的值可以避免_virtual timeline_不公平地偏向于提早加入的线程。

Let **T** be the system time of CPU **C[j]** when thread **P[i]** enters the run queue. 设** T **为线程** P [i] **进入运行队列时CPU ** C [j] **的系统时间。

**s[i]** = **T**  ** s [i] ** = ** T **

**f[i]** = **s[i]** + **p[j]** / **w[i]**  ** f [i] ** = ** s [i] ** + ** p [j] ** / ** w [i] **

 
### Time Slice  时间片 

When a thread is selected to run, its time slice is calculated based on its relative rate and the scheduling period. 选择一个线程运行时，将根据其相对速率和调度周期来计算其时间片。

Let **g** be the integer number of _minimum granularity_ units **M** in the current _scheduling period_ **p[j]** of CPU **C[j]**. 令** g **为当前CPU ** C [j] **的调度周期** p [j] **中最小粒度单位** M **的整数。

Let **R** be the relative rate of thread **P[i]**.  令** R **为线程** P [i] **的相对速率。

**g** = floor(**p[j]** / **M**)  ** g ** =底数（** p [j] ** / ** M **）

**R** = **w[i]** / **W[j]**  ** R ** = ** w [i] ** / ** W [j] **

**t[i]** = ceil(**g** * **R**) * **M**  ** t [i] ** = ceil（** g ** * ** R **）* ** M **

This definition ensures that **t[i]** is an integer multiple of the _minimum granularity_ **M**, while remaining approximately proportional to the relativerate of the thread. 该定义确保** t [i] **是_minimum granularity_ ** M **的整数倍，同时保持近似与线程的相对速率成比例。

 
### Yield  产量 

