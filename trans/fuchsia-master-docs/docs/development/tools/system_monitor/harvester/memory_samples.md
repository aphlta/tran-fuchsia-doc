 
# [Harvester](README.md)  [收割机]（README.md） 

 
## Memory Samples  记忆样本 

The Harvester gathers a collection of memory samples.  收集器收集内存样本的集合。

These counters are not always accurate. It’s possible for the sum of the various page types (free_bytes, mmu_overhead_bytes, free_heap_bytes, etc.) totemporarily add up to more than the total memory. In the rare cases where thevalues don't add up accurately, the differences should only one or two memorypages. 这些计数器并不总是准确的。各种页面类型（free_bytes，mmu_overhead_bytes，free_heap_bytes等）的总和可能暂时总计超过总内存。在极少数情况下，值的累加不准确，差异应该只有一个或两个存储页。

The counts are tracked by incrementing/decrementing atomic integers when a page transitions from one state to another (e.g. from free_bytes to free_heap_bytes).The relaxed accuracy allows for higher system performance. This can be adjustedin the future, but so far there's been no call to make the trade for that extratiny bit of accuracy. 当页面从一种状态转换到另一种状态（例如从free_bytes到free_heap_bytes）时，通过递增/递减原子整数来跟踪计数。宽松的精度允许更高的系统性能。将来可以对此进行调整，但是到目前为止，还没有人呼吁以这种极高的准确性进行交易。

 
##### Dockyard Paths  船坞路径 

The path to each sample will include "memory" and the sample name: e.g. "memory:free_bytes". 每个样本的路径将包括“内存”和样本名称：例如“内存：free_bytes”。

 
### Samples  样品 

Graph data collected by the Harvester along with timestamp and a Dockyard Path is called a Sample. The following sections describe the samples collected. Harvester收集的图形数据以及时间戳和Dockyard路径称为样本。以下各节描述了收集的样本。

This data is often tracked in pages. So values will change by several KB at a time. 通常在页面中跟踪此数据。因此，值将一次更改几KB。

 
#### Memory in the Device  设备内存Device memory refers to the memory within the machine. It's not specific to any process or the kernel. 设备内存是指机器中的内存。它并不特定于任何进程或内核。

 
##### memory:device_total_bytes  内存：device_total_bytesThe total physical memory available to the machine.  机器可用的总物理内存。

 
##### memory:device_free_bytes  内存：device_free_bytesThe bytes within |device_total_bytes| that are unallocated.  | device_total_bytes |中的字节未分配的。

 
#### Memory in the Kernel  内核中的内存This memory is related to the kernel rather than any user process or ipc.  此内存与内核有关，而不与任何用户进程或ipc有关。

 
##### memory:kernel_total_bytes  内存：内核总字节数The total kernel bytes as reported by page state counter.  页面状态计数器报告的内核总字节数。

 
##### memory:kernel_free_bytes  内存：内核空闲字节The bytes within |kernel_total_bytes| that are unallocated.  | kernel_total_bytes |中的字节未分配的。

 
##### memory:kernel_other_bytes  内存：kernel_other_bytesThe amount of memory reserved by and mapped into the kernel for reasons not reported elsewhere. Typically for read-only data like the RAM disk and kernelimage, and for early-boot dynamic memory. 由于未在其他地方报告的原因，由内核保留并映射到内核的内存量。通常用于只读数据，例如RAM磁盘和内核映像，以及用于早期引导的动态内存。

 
#### Categorized Memory  分类记忆These group memory used by category, with a catch-all 'other' category for miscellaneous memory that doesn't fit in another category. 这些类别的内存按类别使用，带有一个笼统的“其他”类别，用于其他类别不适合的其他内存。

 
##### memory:vmo_bytes  内存：vmo_bytesThe number of bytes used for Virtual Memory Objects. Ownership of a VMO may be transferred between processes. 虚拟内存对象使用的字节数。 VMO的所有权可以在流程之间转移。

 
##### memory:mmu_overhead_bytes  内存：mmu_overhead_bytesTracking the memory state also requires memory. This is the number of bytes of overhead used for tracking page tables. 跟踪内存状态也需要内存。这是用于跟踪页表的开销的字节数。

 
##### memory:ipc_bytes  内存：ipc_bytesCurrent amount of memory used for inter-process communication. Currently this reflects the memory used for Zircon channels, but in the future it may includememory for sockets and fifos. 当前用于进程间通信的内存量。当前，这反映了用于Zircon通道的内存，但是在将来，它可能包括套接字和fifos的内存。

 
##### memory:other_bytes  内存：other_bytes