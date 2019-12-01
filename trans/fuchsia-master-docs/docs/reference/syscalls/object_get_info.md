 
# zx_object_get_info  zx_object_get_info 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Query information about an object.  查询有关对象的信息。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_object_get_info(zx_handle_t handle,
                               uint32_t topic,
                               void* buffer,
                               size_t buffer_size,
                               size_t* actual,
                               size_t* avail);
```
 

 
## DESCRIPTION  描述 

`zx_object_get_info()` requests information about the provided handle (or the object the handle refers to). The *topic* parameter indicates what specificinformation is desired. zx_object_get_info（）请求有关提供的句柄（或该句柄引用的对象）的信息。 * topic *参数指示所需的特定信息。

*buffer* is a pointer to a buffer of size *buffer_size* to return the information. * buffer *是指向大小为* buffer_size *的缓冲区的指针，以返回信息。

*actual* is an optional pointer to return the number of records that were written to buffer. * actual *是一个可选的指针，用于返回已写入缓冲区的记录数。

*avail* is an optional pointer to return the number of records that are available to read. * avail *是一个可选的指针，用于返回可读取的记录数。

If the buffer is insufficiently large, *avail* will be larger than *actual*.  如果缓冲区不够大，则* avail *将大于* actual *。

[TOC]  [目录]

 
## TOPICS  话题 

 
### ZX_INFO_HANDLE_VALID  ZX_INFO_HANDLE_VALID 

*handle* type: **Any**  *句柄*类型：**任何**

*buffer* type: **n/a**  *缓冲区*类型：**不适用**

Returns **ZX_OK** if *handle* is valid, or **ZX_ERR_BAD_HANDLE** otherwise. No records are returned and *buffer* may be NULL. 如果* handle *有效，则返回** ZX_OK **，否则返回** ZX_ERR_BAD_HANDLE **。没有记录返回，并且* buffer *可能为NULL。

 
### ZX_INFO_HANDLE_BASIC  ZX_INFO_HANDLE_BASIC 

*handle* type: **Any**  *句柄*类型：**任何**

*buffer* type: `zx_info_handle_basic_t[1]`  *缓冲区*类型：`zx_info_handle_basic_t [1]`

```
typedef struct zx_info_handle_basic {
    // The unique id assigned by kernel to the object referenced by the
    // handle.
    zx_koid_t koid;

    // The immutable rights assigned to the handle. Two handles that
    // have the same koid and the same rights are equivalent and
    // interchangeable.
    zx_rights_t rights;

    // The object type: channel, event, socket, etc.
    uint32_t type;                // zx_obj_type_t;

    // If the object referenced by the handle is related to another (such
    // as the other end of a channel, or the parent of a job) then
    // |related_koid| is the koid of that object, otherwise it is zero.
    // This relationship is immutable: an object's |related_koid| does
    // not change even if the related object no longer exists.
    zx_koid_t related_koid;

    // Set to ZX_OBJ_PROP_WAITABLE if the object referenced by the
    // handle can be waited on; zero otherwise.
    uint32_t props;               // zx_obj_props_t;
} zx_info_handle_basic_t;
```
 

 
### ZX_INFO_HANDLE_COUNT  ZX_INFO_HANDLE_COUNT 

*handle* type: **Any**  *句柄*类型：**任何**

*buffer* type: `zx_info_handle_count_t[1]`  *缓冲区*类型：`zx_info_handle_count_t [1]`

```
typedef struct zx_info_handle_count {
    // The number of outstanding handles to a kernel object.
    uint32_t handle_count;
} zx_info_handle_count_t;
```
 

The *handle_count* should only be used as a debugging aid. Do not use it to check that an untrusted processes cannot modify a kernel object. Due toasynchronous nature of the system scheduler, there might be a time windowduring which it is possible for an object to be modified by a previous handleowner even as the last handle is transferred from one process to another. * handle_count *仅应用作调试辅助。不要使用它来检查不受信任的进程是否不能修改内核对象。由于系统调度程序的异步特性，可能会有一个时间窗口，在此期间，即使最后一个句柄从一个进程转移到另一个进程，也可能由先前的句柄所有者修改对象。

 
### ZX_INFO_PROCESS_HANDLE_STATS  ZX_INFO_PROCESS_HANDLE_STATS 

*handle* type: **Process**  *句柄*类型：**处理**

*buffer* type: `zx_info_process_handle_stats_t[1]`  *缓冲区*类型：`zx_info_process_handle_stats_t [1]`

```
typedef struct zx_info_process_handle_stats {
    // The number of outstanding handles to kernel objects of each type.
    uint32_t handle_count[ZX_OBJ_TYPE_LAST];
} zx_info_process_handle_stats_t;
```
 

 
### ZX_INFO_JOB  ZX_INFO_JOB 

*handle* type: **Job**  *手柄*类型：**工作**

*buffer* type: `zx_info_job_t[1]`  *缓冲区*类型：`zx_info_job_t [1]`

```
typedef struct zx_info_job {
    // The job's return code; only valid if |exited| is true.
    // If the job was killed, it will be one of the ZX_TASK_RETCODE values.
    int64_t return_code;

    // If true, the job has exited and |return_code| is valid.
    bool exited;

    // True if the ZX_PROP_JOB_KILL_ON_OOM property was set.
    bool kill_on_oom;

    // True if a debugger is attached to the job.
    bool debugger_attached;
} zx_info_job_t;
```
 

 
### ZX_INFO_PROCESS  ZX_INFO_PROCESS 

*handle* type: **Process**  *句柄*类型：**处理**

*buffer* type: `zx_info_process_t[1]`  *缓冲区*类型：`zx_info_process_t [1]`

```
typedef struct zx_info_process {
    // The process's return code; only valid if |exited| is true.
    // Guaranteed to be non-zero if the process was killed by |zx_task_kill|.
    int64_t return_code;

    // True if the process has ever left the initial creation state,
    // even if it has exited as well.
    bool started;

    // If true, the process has exited and |return_code| is valid.
    bool exited;

    // True if a debugger is attached to the process.
    bool debugger_attached;
} zx_info_process_t;
```
 

 
### ZX_INFO_PROCESS_THREADS  ZX_INFO_PROCESS_THREADS 

*handle* type: **Process**  *句柄*类型：**处理**

*buffer* type: `zx_koid_t[n]`  *缓冲区*类型：`zx_koid_t [n]`

Returns an array of `zx_koid_t`, one for each running thread in the Process at that moment in time. 返回“ zx_koid_t”的数组，该数组在该时刻对应于进程中每个正在运行的线程。

N.B. Getting the list of threads is inherently racy. This can be somewhat mitigated by first suspending all the threads,but note that an external thread can create new threads.*actual* will contain the number of threads returned in *buffer*.*avail* will contain the total number of threads of the process atthe time the list of threads was obtained, it could be larger than *actual*. N.B.本质上讲，获取线程列表很简单。可以通过先挂起所有线程来缓解这种情况，但是请注意，外部线程可以创建新线程。* actual *将包含* buffer *中返回的线程数。* avail *将包含该线程的总数。在获取线程列表时进行处理，它可能大于* actual *。

 
### ZX_INFO_THREAD  ZX_INFO_THREAD 

*handle* type: **Thread**  *手柄*类型：**螺纹**

*buffer* type: `zx_info_thread_t[1]`  *缓冲区*类型：`zx_info_thread_t [1]`

```
typedef struct zx_info_thread {
    // One of ZX_THREAD_STATE_* values.
    uint32_t state;

    // If |state| is ZX_THREAD_STATE_BLOCKED_EXCEPTION, the thread has gotten
    // an exception and is waiting for the exception to be handled by the
    // specified channel.
    // The value is one of ZX_EXCEPTION_CHANNEL_TYPE_*.
    uint32_t wait_exception_channel_type;

    // CPUs this thread may be scheduled on, as specified by
    // a profile object applied to this thread.
    //
    // The kernel may not internally store invalid CPUs in the mask, so
    // this may not exactly match the mask applied to the thread for
    // CPUs beyond what the system is able to use.
    zx_cpu_set_t cpu_affinity_mask;
} zx_info_thread_t;
```
 

The values in this struct are mainly for informational and debugging purposes at the moment. 目前，此结构中的值主要用于提供信息和调试目的。

The various **ZX_THREAD_STATE_** values are defined by  各种** ZX_THREAD_STATE _ **值由定义

```
#include <zircon/syscalls/object.h>
```
 

 
*   **ZX_THREAD_STATE_NEW**: The thread has been created but it has not started running yet.  * ** ZX_THREAD_STATE_NEW **：该线程已创建，但尚未开始运行。
*   **ZX_THREAD_STATE_RUNNING**: The thread is running user code normally.  * ** ZX_THREAD_STATE_RUNNING **：线程正在正常运行用户代码。
*   **ZX_THREAD_STATE_SUSPENDED**: Stopped due to [`zx_task_suspend()`].  * ** ZX_THREAD_STATE_SUSPENDED **：由于[`zx_task_suspend（）`]而停止。
*   **ZX_THREAD_STATE_BLOCKED**: In a syscall or handling an exception. This value is never returned by itself.See **ZX_THREAD_STATE_BLOCKED_\*** below. * ** ZX_THREAD_STATE_BLOCKED **：在系统调用中或正在处理异常。此值永远不会单独返回。请参见下面的** ZX_THREAD_STATE_BLOCKED _ \ ***。
*   **ZX_THREAD_STATE_DYING**: The thread is in the process of being terminated, but it has not been stopped yet. * ** ZX_THREAD_STATE_DYING **：线程正在终止中，但尚未停止。
*   **ZX_THREAD_STATE_DEAD**: The thread has stopped running.  * ** ZX_THREAD_STATE_DEAD **：线程已停止运行。

When a thread is stopped inside a blocking syscall, or stopped in an exception, the value returned in **state** is one of the following: 当线程在阻塞的系统调用内停止或在异常中停止时，以** state **返回的值是以下之一：

 
*   **ZX_THREAD_STATE_BLOCKED_EXCEPTION**: The thread is stopped in an exception.  * ** ZX_THREAD_STATE_BLOCKED_EXCEPTION **：线程在异常中停止。
*   **ZX_THREAD_STATE_BLOCKED_SLEEPING**: The thread is stopped in [`zx_nanosleep()`].  * ** ZX_THREAD_STATE_BLOCKED_SLEEPING **：该线程在[`zx_nanosleep（）`]中停止。
*   **ZX_THREAD_STATE_BLOCKED_FUTEX**: The thread is stopped in [`zx_futex_wait()`].  * ** ZX_THREAD_STATE_BLOCKED_FUTEX **：该线程在[`zx_futex_wait（）`]中停止。
*   **ZX_THREAD_STATE_BLOCKED_PORT**: The thread is stopped in [`zx_port_wait()`].  * ** ZX_THREAD_STATE_BLOCKED_PORT **：该线程在[`zx_port_wait（）`]中停止。
*   **ZX_THREAD_STATE_BLOCKED_CHANNEL**: The thread is stopped in [`zx_channel_call()`].  * ** ZX_THREAD_STATE_BLOCKED_CHANNEL **：该线程在[`zx_channel_call（）`]中停止。
*   **ZX_THREAD_STATE_BLOCKED_WAIT_ONE**: The thread is stopped in [`zx_object_wait_one()`].  * ** ZX_THREAD_STATE_BLOCKED_WAIT_ONE **：线程在[`zx_object_wait_one（）`]中停止。
*   **ZX_THREAD_STATE_BLOCKED_WAIT_MANY**: The thread is stopped in [`zx_object_wait_many()`].  * ** ZX_THREAD_STATE_BLOCKED_WAIT_MANY **：该线程在[`zx_object_wait_many（）`]中停止。
*   **ZX_THREAD_STATE_BLOCKED_INTERRUPT**: The thread is stopped in [`zx_interrupt_wait()`].  * ** ZX_THREAD_STATE_BLOCKED_INTERRUPT **：线程在[`zx_interrupt_wait（）`]中停止。

The various **ZX_EXCEPTION_CHANNEL_TYPE_** values are defined by  各种** ZX_EXCEPTION_CHANNEL_TYPE _ **值由以下项定义

```
#include <zircon/syscalls/exception.h>
```
 

 
*   **ZX_EXCEPTION_CHANNEL_TYPE_NONE**  * ** ZX_EXCEPTION_CHANNEL_TYPE_NONE **
*   **ZX_EXCEPTION_CHANNEL_TYPE_DEBUGGER**  * ** ZX_EXCEPTION_CHANNEL_TYPE_DEBUGGER **
*   **ZX_EXCEPTION_CHANNEL_TYPE_THREAD**  * ** ZX_EXCEPTION_CHANNEL_TYPE_THREAD **
*   **ZX_EXCEPTION_CHANNEL_TYPE_PROCESS**  * ** ZX_EXCEPTION_CHANNEL_TYPE_PROCESS **
*   **ZX_EXCEPTION_CHANNEL_TYPE_JOB**  * ** ZX_EXCEPTION_CHANNEL_TYPE_JOB **
*   **ZX_EXCEPTION_CHANNEL_TYPE_JOB_DEBUGGER**  * ** ZX_EXCEPTION_CHANNEL_TYPE_JOB_DEBUGGER **

 
### ZX_INFO_THREAD_EXCEPTION_REPORT  ZX_INFO_THREAD_EXCEPTION_REPORT 

*handle* type: **Thread**  *手柄*类型：**螺纹**

*buffer* type: `zx_exception_report_t[1]`  *缓冲区*类型：`zx_exception_report_t [1]`

```
#include <zircon/syscalls/exception.h>
```
 

If the thread is currently in an exception and is waiting for an exception response, then this returns the exception report as a single`zx_exception_report_t`, with status **ZX_OK**. 如果线程当前处于异常中并且正在等待异常响应，则这将以状态为ZX_OK **的单个zx_exception_report_t返回异常报告。

Returns **ZX_ERR_BAD_STATE** if the thread is not in an exception and waiting for an exception response. 如果线程不在异常中并正在等待异常响应，则返回** ZX_ERR_BAD_STATE **。

 
### ZX_INFO_THREAD_STATS  ZX_INFO_THREAD_STATS 

*handle* type: **Thread**  *手柄*类型：**螺纹**

*buffer* type: `zx_info_thread_stats[1]`  *缓冲区*类型：`zx_info_thread_stats [1]`

```
typedef struct zx_info_thread_stats {
    // Total accumulated running time of the thread.
    zx_duration_t total_runtime;

    // CPU number that this thread was last scheduled on, or ZX_INFO_INVALID_CPU
    // if the thread has never been scheduled on a CPU. By the time this call
    // returns, the thread may have been scheduled elsewhere, so this
    // information should only be used as a hint or for statistics.
    uint32_t last_scheduled_cpu;
} zx_info_thread_stats_t;
```
 

 
### ZX_INFO_CPU_STATS  ZX_INFO_CPU_STATS 

Note: many values of this topic are being retired in favor of a different mechanism.  注意：为了支持其他机制，本主题的许多价值观已被淘汰。

*handle* type: **Resource** (Specifically, the root resource)  *处理*类型：**资源**（具体来说，是根资源）

*buffer* type: `zx_info_cpu_stats_t[1]`  *缓冲区*类型：`zx_info_cpu_stats_t [1]`

```
typedef struct zx_info_cpu_stats {
    uint32_t cpu_number;
    uint32_t flags;

    zx_duration_t idle_time;

    // kernel scheduler counters
    uint64_t reschedules;
    uint64_t context_switches;
    uint64_t irq_preempts;
    uint64_t preempts;
    uint64_t yields;

    // cpu level interrupts and exceptions
    uint64_t ints;          // hardware interrupts, minus timer interrupts
                            // inter-processor interrupts
    uint64_t timer_ints;    // timer interrupts
    uint64_t timers;        // timer callbacks
    uint64_t page_faults;   // (deprecated, returns 0)
    uint64_t exceptions;    // (deprecated, returns 0)
    uint64_t syscalls;

    // inter-processor interrupts
    uint64_t reschedule_ipis;
    uint64_t generic_ipis;
} zx_info_cpu_stats_t;
```
 

 
### ZX_INFO_VMAR  ZX_INFO_VMAR 

*handle* type: **VM Address Region**  *句柄*类型：** VM地址区域**

*buffer* type: `zx_info_vmar_t[1]`  *缓冲区*类型：`zx_info_vmar_t [1]`

```
typedef struct zx_info_vmar {
    // Base address of the region.
    uintptr_t base;

    // Length of the region, in bytes.
    size_t len;
} zx_info_vmar_t;
```
 

This returns a single `zx_info_vmar_t` that describes the range of address space that the VMAR occupies. 这将返回一个单一的“ zx_info_vmar_t”，该值描述了VMAR占用的地址空间范围。

 
### ZX_INFO_VMO  ZX_INFO_VMO 

*handle* type: **VM Object**  *句柄*类型：** VM对象**

*buffer* type: `zx_info_vmo_t[1]`  *缓冲区*类型：`zx_info_vmo_t [1]`

```
typedef struct zx_info_vmo {
    // The koid of this VMO.
    zx_koid_t koid;

    // The name of this VMO.
    char name[ZX_MAX_NAME_LEN];

    // The size of this VMO.
    uint64_t size_bytes;

    // If this VMO is a child, the koid of its parent. Otherwise, zero.
    zx_koid_t parent_koid;

    // The number of children of this VMO, if any.
    size_t num_children;

    // The number of times this VMO is currently mapped into VMARs.
    size_t num_mappings;

    // An estimate of the number of unique address spaces that
    // this VMO is mapped into.
    size_t share_count;

    // Bitwise OR of ZX_INFO_VMO_* values.
    uint32_t flags;

    // If |ZX_INFO_VMO_TYPE(flags) == ZX_INFO_VMO_TYPE_PAGED|, the amount of
    // memory currently allocated to this VMO.
    uint64_t committed_bytes;

    // If |flags & ZX_INFO_VMO_VIA_HANDLE|, the handle rights.
    // Undefined otherwise.
    zx_rights_t handle_rights;

    // VMO mapping cache policy. One of ZX_CACHE_POLICY_*
    uint32_t cache_policy;
} zx_info_vmo_t;
```
 

This returns a single `zx_info_vmo_t` that describes various attributes of the VMO. 这将返回一个描述VMO各种属性的“ zx_info_vmo_t”。

 
### ZX_INFO_SOCKET  ZX_INFO_SOCKET 

*handle* type: **Socket**  *手柄*类型：**插座**

*buffer* type: `zx_info_socket_t[1]`  *缓冲区*类型：`zx_info_socket_t [1]`

```
typedef struct zx_info_socket {
    // The options passed to zx_socket_create().
    uint32_t options;

    // The maximum size of the receive buffer of a socket, in bytes.
    //
    // The receive buffer may become full at a capacity less than the maximum
    // due to overhead.
    size_t rx_buf_max;

    // The size of the receive buffer of a socket, in bytes.
    size_t rx_buf_size;

    // The amount of data, in bytes, that is available for reading in a single
    // zx_socket_read call.
    //
    // For stream sockets, this value will match |rx_buf_size|. For datagram
    // sockets, this value will be the size of the next datagram in the receive
    // buffer.
    size_t rx_buf_available;

    // The maximum size of the transmit buffer of a socket, in bytes.
    //
    // The transmit buffer may become full at a capacity less than the maximum
    // due to overhead.
    //
    // Will be zero if the peer endpoint is closed.
    size_t tx_buf_max;

    // The size of the transmit buffer of a socket, in bytes.
    //
    // Will be zero if the peer endpoint is closed.
    size_t tx_buf_size;
} zx_info_socket_t;
```
 

 
### ZX_INFO_TIMER  ZX_INFO_TIMER 

*handle* type: **Timer**  *手柄*类型：**计时器**

*buffer* type: `zx_info_timer_t[1]`  *缓冲区*类型：`zx_info_timer_t [1]`

```
typedef struct zx_info_timer {
    // The options passed to zx_timer_create().
    uint32_t options;

    // The deadline with respect to ZX_CLOCK_MONOTONIC at which the timer will
    // fire next.
    //
    // This value will be zero if the timer is not set to fire.
    zx_time_t deadline;

    // Specifies a range from deadline - slack to deadline + slack during which
    // the timer is allowed to fire. The system uses this parameter as a hint to
    // coalesce nearby timers.
    //
    // The precise coalescing behavior is controlled by the options parameter
    // specified when the timer was created.
    //
    // This value will be zero if the timer is not set to fire.
    zx_duration_t slack;
} zx_info_timer_t;
```
 

 
### ZX_INFO_JOB_CHILDREN  ZX_INFO_JOB_CHILDREN 

*handle* type: **Job**  *手柄*类型：**工作**

*buffer* type: `zx_koid_t[n]`  *缓冲区*类型：`zx_koid_t [n]`

Returns an array of `zx_koid_t`, one for each direct child Job of the provided Job handle. 返回`zx_koid_t`的数组，每个数组对应提供的Job句柄的每个直接子Job。

 
### ZX_INFO_JOB_PROCESSES  ZX_INFO_JOB_PROCESSES 

*handle* type: **Job**  *手柄*类型：**工作**

*buffer* type: `zx_koid_t[n]`  *缓冲区*类型：`zx_koid_t [n]`

Returns an array of `zx_koid_t`, one for each direct child Process of the provided Job handle. 返回一个数组“ zx_koid_t”，一个数组用于提供的作业句柄的每个直接子进程。

 
### ZX_INFO_TASK_STATS  ZX_INFO_TASK_STATS 

*handle* type: **Process**  *句柄*类型：**处理**

*buffer* type: `zx_info_task_stats_t[1]`  *缓冲区*类型：`zx_info_task_stats_t [1]`

Returns statistics about resources (e.g., memory) used by a task.  返回有关任务使用的资源（例如内存）的统计信息。

```
typedef struct zx_info_task_stats {
    // The total size of mapped memory ranges in the task.
    // Not all will be backed by physical memory.
    size_t mem_mapped_bytes;

    // For the fields below, a byte is considered committed if it's backed by
    // physical memory. Some of the memory may be double-mapped, and thus
    // double-counted.

    // Committed memory that is only mapped into this task.
    size_t mem_private_bytes;

    // Committed memory that is mapped into this and at least one other task.
    size_t mem_shared_bytes;

    // A number that estimates the fraction of mem_shared_bytes that this
    // task is responsible for keeping alive.
    //
    // An estimate of:
    //   For each shared, committed byte:
    //   mem_scaled_shared_bytes += 1 / (number of tasks mapping this byte)
    //
    // This number is strictly smaller than mem_shared_bytes.
    size_t mem_scaled_shared_bytes;
} zx_info_task_stats_t;
```
 

Additional errors:  其他错误：

 
*   **ZX_ERR_BAD_STATE**: If the target process has terminated  * ** ZX_ERR_BAD_STATE **：如果目标进程已终止

 
### ZX_INFO_PROCESS_MAPS  ZX_INFO_PROCESS_MAPS 

*handle* type: **Process** other than your own, with **ZX_RIGHT_READ**  *处理*类型：**处理**，而不是您自己处理的** ZX_RIGHT_READ **

*buffer* type: `zx_info_maps_t[n]`  *缓冲区*类型：`zx_info_maps_t [n]`

The `zx_info_maps_t` array is a depth-first pre-order walk of the target process's Aspace/VMAR/Mapping tree. As per the pre-order traversal baseaddresses will be in ascending order. zx_info_maps_t数组是目标进程的Aspace / VMAR / Mapping树的深度优先的预排序。根据预遍历基址将按升序排列。

```
typedef struct zx_info_maps {
    // Name if available; empty string otherwise.
    char name[ZX_MAX_NAME_LEN];
    // Base address.
    zx_vaddr_t base;
    // Size in bytes.
    size_t size;

    // The depth of this node in the tree.
    // Can be used for indentation, or to rebuild the tree from an array
    // of zx_info_maps_t entries, which will be in depth-first pre-order.
    size_t depth;
    // The type of this entry; indicates which union entry is valid.
    uint32_t type; // zx_info_maps_type_t
    union {
        zx_info_maps_mapping_t mapping;
        // No additional fields for other types.
    } u;
} zx_info_maps_t;
```
 

The *depth* field of each entry describes its relationship to the nodes that come before it. Depth 0 is the root Aspace, depth 1 is the root VMAR, and allother entries have depth 2 or greater. 每个条目的* depth *字段描述了它与之前的节点的关系。深度0是根Aspace，深度1是根VMAR，所有其他条目的深度为2或更大。

To get a full picture of how a process uses its VMOs and how a VMO is used by various processes, you may need to combine this information withZX_INFO_PROCESS_VMOS. 为了全面了解一个进程如何使用其VMO以及各种进程如何使用VMO，您可能需要将此信息与ZX_INFO_PROCESS_VMOS结合使用。

See the `vmaps` command-line tool for an example user of this topic, and to dump the maps of arbitrary processes by koid. 有关该主题的示例用户，请参见`vmaps`命令行工具，并按koid来转储任意进程的映射。

Additional errors:  其他错误：

 
*   **ZX_ERR_ACCESS_DENIED**: If the appropriate rights are missing, or if a process attempts to call this on a handle to itself. It's not safe toexamine yourself: *buffer* will live inside the Aspace being examined, andthe kernel can't safely fault in pages of the buffer while walking theAspace. * ** ZX_ERR_ACCESS_DENIED **：如果缺少适当的权限，或者进程尝试在其自身的句柄上调用此权限。检查自己是不安全的：* buffer *将存在于被检查的Aspace中，并且内核在遍历Aspace时无法安全地在缓冲区的页面中出错。
*   **ZX_ERR_BAD_STATE**: If the target process has terminated, or if its address space has been destroyed * ** ZX_ERR_BAD_STATE **：如果目标进程已终止，或者其地址空间已被破坏

 
### ZX_INFO_PROCESS_VMOS  ZX_INFO_PROCESS_VMOS 

*handle* type: **Process** other than your own, with **ZX_RIGHT_READ**  *处理*类型：**处理**，而不是您自己处理的** ZX_RIGHT_READ **

*buffer* type: `zx_info_vmos_t[n]`  *缓冲区*类型：`zx_info_vmos_t [n]`

The `zx_info_vmos_t` array is list of all VMOs pointed to by the target process. Some VMOs are mapped, some are pointed to by handles, and some are both. zx_info_vmos_t数组是目标进程指向的所有VMO的列表。有些VMO已映射，有些由句柄指向，而有些则两者都有。

Note: The same VMO may appear multiple times due to multiple mappings or handles, or because a handle to the VMO has been removed and then readdedconcurrently with this call. VMOs can change as the target process runs whichmay result in the same VMO having different values each time it appears. Thecaller must resolve any duplicate values. 注意：由于多个映射或句柄，或者由于已删除VMO的句柄，然后与此调用同时读取，因此同一VMO可能会出现多次。 VMO会随着目标进程的运行而变化，这可能导致同一VMO每次出现时具有不同的值。呼叫者必须解析任何重复的值。

To get a full picture of how a process uses its VMOs and how a VMO is used by various processes, you may need to combine this information withZX_INFO_PROCESS_MAPS. 要全面了解一个进程如何使用其VMO以及各种进程如何使用VMO，您可能需要将此信息与ZX_INFO_PROCESS_MAPS结合在一起。

```
// Describes a VMO.
typedef struct zx_info_vmo {
    // The koid of this VMO.
    zx_koid_t koid;

    // The name of this VMO.
    char name[ZX_MAX_NAME_LEN];

    // The size of this VMO; i.e., the amount of virtual address space it
    // would consume if mapped.
    uint64_t size_bytes;

    // If this VMO is a child , the koid of its parent. Otherwise, zero.
    // See |flags| for the type of child.
    zx_koid_t parent_koid;

    // The number of child of this VMO, if any.
    size_t num_children;

    // The number of times this VMO is currently mapped into VMARs.
    // Note that the same process will often map the same VMO twice,
    // and both mappings will be counted here. (I.e., this is not a count
    // of the number of processes that map this VMO; see share_count.)
    size_t num_mappings;

    // An estimate of the number of unique address spaces that
    // this VMO is mapped into. Every process has its own address space,
    // and so does the kernel.
    size_t share_count;

    // Bitwise OR of ZX_INFO_VMO_* values.
    uint32_t flags;

    // If |ZX_INFO_VMO_TYPE(flags) == ZX_INFO_VMO_TYPE_PAGED|, the amount of
    // memory currently allocated to this VMO; i.e., the amount of physical
    // memory it consumes. Undefined otherwise.
    uint64_t committed_bytes;

    // If |flags & ZX_INFO_VMO_VIA_HANDLE|, the handle rights.
    // Undefined otherwise.
    zx_rights_t handle_rights;
} zx_info_vmo_t;
```
 

See the `vmos` command-line tool for an example user of this topic, and to dump the VMOs of arbitrary processes by koid. 有关该主题的示例用户，请参见`vmos`命令行工具，并通过koid转储任意进程的VMO。

 
### ZX_INFO_KMEM_STATS  ZX_INFO_KMEM_STATS 

*handle* type: **Resource** (Specifically, the root resource)  *处理*类型：**资源**（具体来说，是根资源）

*buffer* type: `zx_info_kmem_stats_t[1]`  *缓冲区*类型：`zx_info_kmem_stats_t [1]`

Returns information about kernel memory usage.  返回有关内核内存使用情况的信息。

```
typedef struct zx_info_kmem_stats {
    // The total amount of physical memory available to the system.
    // Note, the values below may not exactly add up to this total.
    size_t total_bytes;

    // The amount of unallocated memory.
    size_t free_bytes;

    // The amount of memory reserved by and mapped into the kernel for reasons
    // not covered by other fields in this struct. Typically for readonly data
    // like the ram disk and kernel image, and for early-boot dynamic memory.
    size_t wired_bytes;

    // The amount of memory allocated to the kernel heap.
    size_t total_heap_bytes;

    // The portion of |total_heap_bytes| that is not in use.
    size_t free_heap_bytes;

    // The amount of memory committed to VMOs, both kernel and user.
    // A superset of all userspace memory.
    // Does not include certain VMOs that fall under |wired_bytes|.
    //
    // TODO(dbort): Break this into at least two pieces: userspace VMOs that
    // have koids, and kernel VMOs that don't. Or maybe look at VMOs
    // mapped into the kernel aspace vs. everything else.
    size_t vmo_bytes;

    // The amount of memory used for architecture-specific MMU metadata
    // like page tables.
    size_t mmu_overhead_bytes;

    // Non-free memory that isn't accounted for in any other field.
    size_t other_bytes;
} zx_info_kmem_stats_t;
```
 

 
### ZX_INFO_RESOURCE  ZX_INFO_RESOURCE 

*handle* type: **Resource**  *句柄*类型：**资源**

*buffer* type: `zx_info_resource_t[1]`  *缓冲区*类型：`zx_info_resource_t [1]`

Returns information about a resource object via its handle.  通过其句柄返回有关资源对象的信息。

```
typedef struct zx_info_resource {
    // The resource kind
    uint32_t kind;
    // Resource's low value (inclusive)
    uint64_t low;
    // Resource's high value (inclusive)
    uint64_t high;
} zx_info_resource_t;
```
 

The resource kind is one of  资源种类是其中一种

 
*   **ZX_RSRC_KIND_ROOT**  * ** ZX_RSRC_KIND_ROOT **
*   **ZX_RSRC_KIND_MMIO**  * ** ZX_RSRC_KIND_MMIO **
*   **ZX_RSRC_KIND_IOPORT**  * ** ZX_RSRC_KIND_IOPORT **
*   **ZX_RSRC_KIND_IRQ**  * ** ZX_RSRC_KIND_IRQ **
*   **ZX_RSRC_KIND_HYPERVISOR**  * ** ZX_RSRC_KIND_HYPERVISOR **
*   **ZX_RSRC_KIND_VMEX**  * ** ZX_RSRC_KIND_VMEX **
*   **ZX_RSRC_KIND_SMC**  * ** ZX_RSRC_KIND_SMC **

 
### ZX_INFO_BTI  ZX_INFO_BTI 

*handle* type: **Bus Transaction Initiator**  *句柄*类型：**公交交易发起人**

*buffer* type: `zx_info_bti_t[1]`  *缓冲区*类型：`zx_info_bti_t [1]`

```
typedef struct zx_info_bti {
    // zx_bti_pin will always be able to return addresses that are contiguous for at
    // least this many bytes.  E.g. if this returns 1MB, then a call to
    // zx_bti_pin() with a size of 2MB will return at most two physically-contiguous runs.
    // If the size were 2.5MB, it will return at most three physically-contiguous runs.
    uint64_t minimum_contiguity;

    // The number of bytes in the device's address space (UINT64_MAX if 2^64).
    uint64_t aspace_size;
} zx_info_bti_t;
```
 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

If *topic* is **ZX_INFO_PROCESS**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_PROCESS **，则* handle *必须为** ZX_OBJ_TYPE_PROCESS **类型且具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_JOB**, *handle* must be of type **ZX_OBJ_TYPE_JOB** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_JOB **，则* handle *必须为** ZX_OBJ_TYPE_JOB **类型并具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_PROCESS_THREADS**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_ENUMERATE**.  如果* topic *为** ZX_INFO_PROCESS_THREADS **，则* handle *必须为** ZX_OBJ_TYPE_PROCESS **类型且具有** ZX_RIGHT_ENUMERATE **。

If *topic* is **ZX_INFO_JOB_CHILDREN**, *handle* must be of type **ZX_OBJ_TYPE_JOB** and have **ZX_RIGHT_ENUMERATE**.  如果* topic *为** ZX_INFO_JOB_CHILDREN **，则* handle *必须为** ZX_OBJ_TYPE_JOB **类型并具有** ZX_RIGHT_ENUMERATE **。

If *topic* is **ZX_INFO_JOB_PROCESSES**, *handle* must be of type **ZX_OBJ_TYPE_JOB** and have **ZX_RIGHT_ENUMERATE**.  如果* topic *为** ZX_INFO_JOB_PROCESSES **，则* handle *必须为** ZX_OBJ_TYPE_JOB **类型并具有** ZX_RIGHT_ENUMERATE **。

If *topic* is **ZX_INFO_THREAD**, *handle* must be of type **ZX_OBJ_TYPE_THREAD** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_THREAD **，则* handle *必须为** ZX_OBJ_TYPE_THREAD **类型且具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_THREAD_EXCEPTION_REPORT**, *handle* must be of type **ZX_OBJ_TYPE_THREAD** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_THREAD_EXCEPTION_REPORT **，则* handle *必须为** ZX_OBJ_TYPE_THREAD **类型并具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_THREAD_STATS**, *handle* must be of type **ZX_OBJ_TYPE_THREAD** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_THREAD_STATS **，则* handle *必须为** ZX_OBJ_TYPE_THREAD **类型且具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_TASK_STATS**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_TASK_STATS **，则* handle *必须为** ZX_OBJ_TYPE_PROCESS **类型且具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_PROCESS_MAPS**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_PROCESS_MAPS **，则* handle *必须为** ZX_OBJ_TYPE_PROCESS **类型且具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_PROCESS_VMOS**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_PROCESS_VMOS **，则* handle *必须为** ZX_OBJ_TYPE_PROCESS **类型且具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_VMO**, *handle* must be of type **ZX_OBJ_TYPE_VMO**.  如果* topic *为** ZX_INFO_VMO **，则* handle *必须为** ZX_OBJ_TYPE_VMO **类型。

If *topic* is **ZX_INFO_VMAR**, *handle* must be of type **ZX_OBJ_TYPE_VMAR** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_VMAR **，则* handle *必须为** ZX_OBJ_TYPE_VMAR **类型并具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_CPU_STATS**, *handle* must have resource kind **ZX_RSRC_KIND_ROOT**.  如果* topic *是** ZX_INFO_CPU_STATS **，则* handle *必须具有资源种类** ZX_RSRC_KIND_ROOT **。

If *topic* is **ZX_INFO_KMEM_STATS**, *handle* must have resource kind **ZX_RSRC_KIND_ROOT**.  如果* topic *是** ZX_INFO_KMEM_STATS **，则* handle *必须具有资源类型** ZX_RSRC_KIND_ROOT **。

If *topic* is **ZX_INFO_RESOURCE**, *handle* must be of type **ZX_OBJ_TYPE_RESOURCE** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_RESOURCE **，则* handle *必须为** ZX_OBJ_TYPE_RESOURCE **类型且具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_HANDLE_COUNT**, *handle* must have **ZX_RIGHT_INSPECT**.  如果* topic *是** ZX_INFO_HANDLE_COUNT **，则* handle *必须具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_BTI**, *handle* must be of type **ZX_OBJ_TYPE_BTI** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_BTI **，则* handle *必须为** ZX_OBJ_TYPE_BTI **类型且具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_PROCESS_HANDLE_STATS**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_PROCESS_HANDLE_STATS **，则* handle *必须为** ZX_OBJ_TYPE_PROCESS **类型且具有** ZX_RIGHT_INSPECT **。

If *topic* is **ZX_INFO_SOCKET**, *handle* must be of type **ZX_OBJ_TYPE_SOCKET** and have **ZX_RIGHT_INSPECT**.  如果* topic *为** ZX_INFO_SOCKET **，则* handle *必须为** ZX_OBJ_TYPE_SOCKET **类型且具有** ZX_RIGHT_INSPECT **。

 
## RETURN VALUE  返回值 

`zx_object_get_info()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_object_get_info（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE** *handle* is not an appropriate type for *topic*  ** ZX_ERR_WRONG_TYPE ** *句柄*不适用于* topic *

**ZX_ERR_ACCESS_DENIED**: If *handle* does not have the necessary rights for the operation. ** ZX_ERR_ACCESS_DENIED **：如果* handle *没有必要的操作权限。

**ZX_ERR_INVALID_ARGS** *buffer*, *actual*, or *avail* are invalid pointers.  ** ZX_ERR_INVALID_ARGS ** * buffer *，* actual *或* avail *是无效的指针。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_BUFFER_TOO_SMALL** The *topic* returns a fixed number of records, but the provided buffer is not large enough for these records. ** ZX_ERR_BUFFER_TOO_SMALL ** * topic *返回固定数量的记录，但是提供的缓冲区不足以容纳这些记录。

**ZX_ERR_NOT_SUPPORTED** *topic* does not exist.  ** ZX_ERR_NOT_SUPPORTED ** *主题*不存在。

 
## EXAMPLES  例子 

```
bool is_handle_valid(zx_handle_t handle) {
    return zx_object_get_info(
        handle, ZX_INFO_HANDLE_VALID, NULL, 0, NULL, NULL) == ZX_OK;
}

zx_koid_t get_object_koid(zx_handle_t handle) {
    zx_info_handle_basic_t info;
    if (zx_object_get_info(handle, ZX_INFO_HANDLE_BASIC,
                           &info, sizeof(info), NULL, NULL) != ZX_OK) {
        return 0;
    }
    return info.koid;
}

void examine_threads(zx_handle_t proc) {
    zx_koid_t threads[128];
    size_t count, avail;

    if (zx_object_get_info(proc, ZX_INFO_PROCESS_THREADS, threads,
                           sizeof(threads), &count, &avail) != ZX_OK) {
        // Error!
    } else {
        if (avail > count) {
            // More threads than space in array;
            // could call again with larger array.
        }
        for (size_t n = 0; n < count; n++) {
            do_something(thread[n]);
        }
    }
}
```
 

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_handle_replace()`]  -[`zx_handle_replace（）`]
 - [`zx_object_get_child()`]  -[`zx_object_get_child（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

