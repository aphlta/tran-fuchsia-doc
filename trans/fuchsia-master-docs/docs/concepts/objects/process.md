 
# Process  处理 

 
## NAME  名称 

process - Process abstraction  流程-流程抽象

 
## SYNOPSIS  概要 

A zircon process is an instance of a program in the traditional sense: a set of instructions which will be executed by one or morethreads, along with a collection of resources. 锆石处理是传统意义上程序的一个实例：一组指令，这些指令将由一个或多个线程执行，并带有一组资源。

 
## DESCRIPTION  描述 

The process object is a container of the following resources:  流程对象是以下资源的容器：

 
+ [Handles](/docs/concepts/objects/handles.md)  + [句柄]（/ docs / concepts / objects / handles.md）
+ [Virtual Memory Address Regions](vm_address_region.md)  + [虚拟内存地址区域]（vm_address_region.md）
+ [Threads](thread.md)  + [线程]（thread.md）

In general, it is associated with code which it is executing until it is forcefully terminated or the program exits. 通常，它与正在执行的代码相关联，直到被强制终止或程序退出为止。

Processes are owned by [jobs](job.md) and allow an application that is composed by more than one process to be treated as a single entity, from theperspective of resource and permission limits, as well as lifetime control. 进程由[jobs]（job.md）拥有，并允许从资源和权限限制以及生命周期控制的角度将由多个进程组成的应用程序视为一个实体。

 
### Lifetime  一生A process is created via [`zx_process_create()`] and its execution begins with [`zx_process_start()`]. 通过[`zx_process_create（）]创建一个进程，并且其执行从[`zx_process_start（）]开始。

The process stops execution when:  该过程在以下情况下停止执行：

 
+ the last thread is terminated or exits  +最后一个线程终止或退出
+ the process calls [`zx_process_exit()`]  +流程调用[`zx_process_exit（）`]
+ the parent job terminates the process  +父工作终止了该过程
+ the parent job is destroyed  +父工作被破坏

The call to [`zx_process_start()`] cannot be issued twice. New threads cannot be added to a process that was started and then its last thread has exited. 对[`zx_process_start（）`的调用不能发出两次。无法将新线程添加到已启动的进程，然后该进程的最后一个线程退出。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_process_create()`] - create a new process within a job  -[`zx_process_create（）`]-在作业中创建新流程
 - [`zx_process_read_memory()`] - read from a process's address space  -[`zx_process_read_memory（）`]-从进程的地址空间读取
 - [`zx_process_start()`] - cause a new process to start executing  -[`zx_process_start（）`]-使新进程开始执行
 - [`zx_process_write_memory()`] - write to a process's address space  -[`zx_process_write_memory（）`]-写入进程的地址空间
 - [`zx_process_exit()`] - exit the current process  -[`zx_process_exit（）`]-退出当前进程

<br>  <br>

 
 - [`zx_job_create()`] - create a new job within a parent job  -[`zx_job_create（）`]-在父作业中创建新作业

<br>  <br>

 
 - [`zx_task_create_exception_channel()`] - listen for task exceptions  -[`zx_task_create_exception_channel（）`]-监听任务异常

<br>  <br>

 
 - [`zx_vmar_map()`] - Map memory into an address space range  -[`zx_vmar_map（）`]-将内存映射到地址空间范围
 - [`zx_vmar_protect()`] - Change permissions on an address space range  -[`zx_vmar_protect（）`]-更改地址空间范围的权限
 - [`zx_vmar_unmap()`] - Unmap memory from an address space range  -[`zx_vmar_unmap（）`]-从地址空间范围取消映射内存

