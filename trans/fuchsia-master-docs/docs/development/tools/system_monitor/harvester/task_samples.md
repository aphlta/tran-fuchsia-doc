 
# Task Samples  任务样本 

The [Harvester](README.md) gathers Task samples from jobs, processes, and threads on the Fuchsia device. This document describes how the data is labelledand what the values represent. [Harvester]（README.md）从Fuchsia设备上的作业，进程和线程中收集Task示例。本文档介绍了如何标记数据以及值代表什么。

 
##### Dockyard Paths  船坞路径 

The path to each sample will include "koid", the kernel object ID (koid), and the sample name: e.g. "koid:12345:zircon-services". 每个样本的路径将包括“ koid”，内核对象ID（koid）和样本名称： “ koid：12345：zircon-services”。

 
### Samples  样品 

Data collected by the Harvester along with timestamp and a Dockyard Path is called a Sample. The following sections describe Task samples collected. Theyare presented in three groups, some values (e.g. name) appear in multiplegroups. 收割机连同时间戳记和船坞路径一起收集的数据称为样本。以下各节描述了收集的任务样本。它们分为三组，某些值（例如名称）出现在多个组中。

 
#### Job  工作 

A job has permissions. A job will have one or more processes (which have memory mappings), and each process will have one or more thread (which execute on aCPU). 作业具有权限。一个作业将具有一个或多个进程（具有内存映射），并且每个进程将具有一个或多个线程（在CPU上执行）。

 
##### koid:\*:type  koid：\ *：typeThis will always be `dockyard::KoidType::JOB` for a job.  对于工作，这将始终是`dockyard :: KoidType :: JOB`。

 
##### koid:\*:parent_koid  koid：\ *：parent_koidThe koid of the object that started this job.  开始这项工作的对象的类别。

 
##### koid:\*:name  koid：\ *：nameA UTF-8 string label for the job. May not be unique.  作业的UTF-8字符串标签。可能不是唯一的。

 
##### koid:\*:kill_on_oom  koid：\ *：kill_on_oomIf the Fuchsia device is low on memory (i.e. oom or Out Of Memory) this job (and its child processes and their threads) may be 'killed' (i.e. terminated) for thegood of the rest of the system. E.g. the job is not critical. A Boolean value,1 is true (will be killed) and 0 is false. 如果Fuchsia设备的内存不足（即oom或Out of Memory），则可能会为了系统的其余部分而``杀死''（即终止）该作业（及其子进程及其线程）。例如。这项工作并不重要。布尔值，1为true（将被终止），0为false。

 
#### Process  处理 

A process has memory. In contrast, a thread accesses memory owned by the Process, but threads themselves don't have their own (memory) address range. 进程有内存。相反，线程访问进程拥有的内存，但是线程本身没有自己的（内存）地址范围。

A byte of memory is considered committed if it's backed by physical memory. Some of the memory may be double-mapped, and thus double-counted. Samples wherethis may occur are marked "May be counted by more than one mapping" below. 如果一个字节的内存由物理内存支持，则视为已提交。某些内存可能被双重映射，因此被重复计数。可能发生这种情况的示例在下面标记为“可能被多个映射计数”。

 
##### koid:\*:type  koid：\ *：typeThis will always be `dockyard::KoidType::PROCESS` for a process.  对于一个进程，这将始终是`dockyard :: KoidType :: PROCESS`。

 
##### koid:\*:parent_koid  koid：\ *：parent_koidThe koid of the object that started this process (e.g. its job).  开始此过程的对象的类别（例如其工作）。

 
##### koid:\*:name  koid：\ *：nameA UTF-8 string label for the job. May not be unique.  作业的UTF-8字符串标签。可能不是唯一的。

 
##### koid:\*:memory_mapped_bytes  koid：\ *：memory_mapped_bytesThe total size of mapped memory ranges in the process, though not all will be backed by physical memory. 在此过程中，映射内存的总大小范围虽然不是全部都由物理内存支持。

 
##### koid:\*:memory_private_bytes  kodi：\ *：内存专用字节Committed memory that is only mapped into this process. May be counted by more than one mapping. 仅映射到此进程的已提交内存。可能被多个映射计数。

 
##### koid:\*:memory_shared_bytes  koid：\ *：memory_shared_bytesCommitted memory that is mapped into this and at least one other process. May be counted by more than one mapping. 映射到此进程和至少一个其他进程的已提交内存。可能被多个映射计数。

 
##### koid:\*:memory_scaled_shared_bytes  koid：\ *：memory_scaled_shared_bytesAn estimate of the prorated number of mem_shared_bytes used by this process.  此过程使用的按比例分配的mem_shared_bytes数量的估计值。

Calculated by: For each shared, committed byte,memory_scaled_shared_bytes += 1 / (number of process mapping this byte) 计算依据：对于每个共享的，已提交的字节，memory_scaled_shared_bytes + = 1 /（映射此字节的进程数）

The memory_scaled_shared_bytes will be smaller than memory_shared_bytes. May be counted by more than one mapping. memory_scaled_shared_bytes将小于memory_shared_bytes。可能被多个映射计数。

See zx_info_task_stats_t in zircon/system/public/zircon/syscalls/object.h for up to date information. 有关最新信息，请参见zircon / system / public / zircon / syscalls / object.h中的zx_info_task_stats_t。

 
#### Thread  线 

A thread exists within a process and each process will have at least one thread. Threads actually execute (use the CPU) while a process does not. 一个进程中存在一个线程，每个进程将至少有一个线程。线程实际上执行（使用CPU），而进程没有执行。

A thread does not have its own memory address space. Instead threads use the memory address space of their parent process. 线程没有自己的内存地址空间。相反，线程使用其父进程的内存地址空间。

 
##### koid:\*:type  koid：\ *：typeThis will always be `dockyard::KoidType::THREAD` for a thread.  对于一个线程，这将始终是`dockyard :: KoidType :: THREAD`。

 
##### koid:\*:parent_koid  koid：\ *：parent_koidThe koid of the object that started this thread (e.g. its process).  启动此线程的对象的类（例如其进程）。

 
##### koid:\*:name  koid：\ *：nameA UTF-8 string label for the job. May not be unique.  作业的UTF-8字符串标签。可能不是唯一的。

 
##### koid:\*:thread_state  koid：\ *：thread_stateWhether the thread is running, waiting, etc. The current (when this was written) thread states are: 线程是否正在运行，正在等待等。当前（写入时）线程状态为：

```
Basic thread states, in zx_info_thread_t.state.
    ZX_THREAD_STATE_NEW                 0x0000
    ZX_THREAD_STATE_RUNNING             0x0001
    ZX_THREAD_STATE_SUSPENDED           0x0002
    // ZX_THREAD_STATE_BLOCKED is never returned by itself.
    // It is always returned with a more precise reason.
    // See ZX_THREAD_STATE_BLOCKED_* below.
    ZX_THREAD_STATE_BLOCKED             0x0003
    ZX_THREAD_STATE_DYING               0x0004
    ZX_THREAD_STATE_DEAD                0x0005

More precise thread states.
    ZX_THREAD_STATE_BLOCKED_EXCEPTION   0x0103
    ZX_THREAD_STATE_BLOCKED_SLEEPING    0x0203
    ZX_THREAD_STATE_BLOCKED_FUTEX       0x0303
    ZX_THREAD_STATE_BLOCKED_PORT        0x0403
    ZX_THREAD_STATE_BLOCKED_CHANNEL     0x0503
    ZX_THREAD_STATE_BLOCKED_WAIT_ONE    0x0603
    ZX_THREAD_STATE_BLOCKED_WAIT_MANY   0x0703
    ZX_THREAD_STATE_BLOCKED_INTERRUPT   0x0803
    ZX_THREAD_STATE_BLOCKED_PAGER       0x0903
```
 

