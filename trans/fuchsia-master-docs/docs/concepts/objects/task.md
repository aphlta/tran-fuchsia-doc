 
# Task  任务 

 
## NAME  名称 

Task - "Runnable" subclass of kernel objects (threads, processes, and jobs)  任务-内核对象（线程，进程和作业）的“可运行”子类

 
## SYNOPSIS  概要 

[Threads](thread.md), [processes](process.md), and [jobs](job.md) objects are all tasks. They share the ability to be suspended, resumed, andkilled. [线程]（thread.md），[进程]（process.md）和[jobs]（job.md）对象都是任务。他们具有被暂停，恢复和杀死的能力。

 
## DESCRIPTION  描述 

TODO  去做

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_task_create_exception_channel()`] - listen for task exceptions  -[`zx_task_create_exception_channel（）`]-监听任务异常
 - [`zx_task_kill()`] - cause a task to stop running  -[`zx_task_kill（）`]-导致任务停止运行

