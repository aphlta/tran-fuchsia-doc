 
# Job  工作 

 
## NAME  名称 

job - Control a group of processes  工作-控制一组流程

 
## SYNOPSIS  概要 

A job is a group of [processes](process.md) and possibly other (child) jobs. Jobs are used to track privileges to perform kernel operations (i.e., makevarious syscalls, with various options), and track and limit basic resource(e.g., memory, CPU) consumption. Every process belongs to a single job. All thejobs on a Fuchsia system form a tree, with every job, except the root job,belonging to a single (parent) job. 作业是一组[processs]（process.md）以及其他（子）作业。作业用于跟踪特权以执行内核操作（即使用各种选项进行各种syscall），以及跟踪和限制基本资源（例如内存，CPU）的消耗。每个过程都属于一个工作。倒挂金钟系统上的所有工作都形成一棵树，除根工作外，所有工作都属于一个（父）工作。

 
## DESCRIPTION  描述 

A job is an object consisting of the following:  作业是包含以下内容的对象：

 
+ a reference to a parent job  +对父母工作的参考
+ a set of child jobs (each of which has this job as its parent)  +一组子工作（每个子工作都以其父工作）
+ a set of member processes  +一组成员流程
+ a set of policies [⚠ not implemented]  +一套政策[⚠未实施]

Jobs allow "applications" that are composed of more than one process to be controlled as a single entity. 作业允许将由多个流程组成的“应用程序”作为一个实体进行控制。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_job_create()`] - create a new child job.  -[`zx_job_create（）`]-创建一个新的子作业。
 - [`zx_process_create()`] - create a new process within a job.  -[`zx_process_create（）`]-在作业中创建新流程。
 - [`zx_job_set_policy()`] - set policy for new processes in the job.  -[`zx_job_set_policy（）`]-为作业中的新流程设置策略。
 - [`zx_task_create_exception_channel()`] - listen for task exceptions  -[`zx_task_create_exception_channel（）`]-监听任务异常
 - [`zx_task_kill()`] - cause a task to stop running.  -[`zx_task_kill（）`]-使任务停止运行。

