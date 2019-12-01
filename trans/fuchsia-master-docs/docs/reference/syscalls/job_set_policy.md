 
# zx_job_set_policy  zx_job_set_policy 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Set job security and resource policies.  设置作业安全性和资源策略。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_job_set_policy(zx_handle_t handle,
                              uint32_t options,
                              uint32_t topic,
                              const void* policy,
                              uint32_t policy_size);
```
 

 
## DESCRIPTION  描述 

Sets one or more security and/or resource policies to an empty job. The job's effective policies is the combination of the parent's effective policies andthe policies specified in *policy*. The effect in the case of conflict betweenthe existing policies and the new policies is controlled by *options* values: 将一项或多项安全和/或资源策略设置为空作业。作业的有效策略是父级的有效策略和* policy *中指定的策略的组合。在现有策略和新策略之间发生冲突的情况下，影响由* options *值控制：

 
+ **ZX_JOB_POL_RELATIVE** : policy is applied for the conditions not specifically overridden by the parent policy. + ** ZX_JOB_POL_RELATIVE **：策略适用于未由父策略明确覆盖的条件。
+ **ZX_JOB_POL_ABSOLUTE** : policy is applied for all conditions in *policy* or the syscall fails. + ** ZX_JOB_POL_ABSOLUTE **：策略适用于* policy *中的所有条件，否则系统调用将失败。

After this call succeeds any new child process or child job will have the new effective policy applied to it. 此调用成功后，任何新的子进程或子作业将对其应用新的有效策略。

*topic* indicates the *policy* format. Supported values are **ZX_JOB_POL_BASIC** and **ZX_JOB_POL_TIMER_SLACK**. * topic *表示* policy *格式。支持的值为** ZX_JOB_POL_BASIC **和** ZX_JOB_POL_TIMER_SLACK **。

 
### **ZX_JOB_POL_BASIC**  ** ZX_JOB_POL_BASIC ** 

A *topic* of **ZX_JOB_POL_BASIC** indicates that *policy* is an array of *count* entries of: ZX_JOB_POL_BASIC **的* topic *表示* policy *是以下项的* count *项的数组：

```
typedef struct zx_policy_basic {
    uint32_t condition;
    uint32_t policy;
} zx_policy_basic_t;

```
 

Where *condition* is one of  *条件*是以下条件之一

 
+ **ZX_POL_BAD_HANDLE** a process under this job is attempting to issue a syscall with an invalid handle.  In this case,**ZX_POL_ACTION_ALLOW** and **ZX_POL_ACTION_DENY** are equivalent:if the syscall returns, it will always return the error**ZX_ERR_BAD_HANDLE**. + ** ZX_POL_BAD_HANDLE **此作业下的进程正在尝试发出无效句柄的syscall。在这种情况下，** ZX_POL_ACTION_ALLOW **和** ZX_POL_ACTION_DENY **是等效的：如果系统调用返回，它将始终返回错误** ZX_ERR_BAD_HANDLE **。
+ **ZX_POL_WRONG_OBJECT** a process under this job is attempting to issue a syscall with a handle that does not support such operation. + ** ZX_POL_WRONG_OBJECT **此作业下的进程正在尝试发出带有不支持该操作的句柄的syscall。
+ **ZX_POL_VMAR_WX** a process under this job is attempting to map an address region with write-execute access. + ** ZX_POL_VMAR_WX **此作业下的某个进程正在尝试映射具有写执行访问权限的地址区域。
+ **ZX_POL_NEW_VMO** a process under this job is attempting to create a new vm object. + ** ZX_POL_NEW_VMO **此作业下的进程正在尝试创建新的vm对象。
+ **ZX_POL_NEW_CHANNEL** a process under this job is attempting to create a new channel. + ** ZX_POL_NEW_CHANNEL **此作业下的进程正在尝试创建新频道。
+ **ZX_POL_NEW_EVENT** a process under this job is attempting to create a new event. + ** ZX_POL_NEW_EVENT **此作业下的某个进程正在尝试创建新事件。
+ **ZX_POL_NEW_EVENTPAIR** a process under this job is attempting to create a new event pair. + ** ZX_POL_NEW_EVENTPAIR **此作业下的某个进程正在尝试创建新的事件对。
+ **ZX_POL_NEW_PORT** a process under this job is attempting to create a new port. + ** ZX_POL_NEW_PORT **此作业下的进程正在尝试创建新端口。
+ **ZX_POL_NEW_SOCKET** a process under this job is attempting to create a new socket. + ** ZX_POL_NEW_SOCKET **此作业下的进程正在尝试创建新的套接字。
+ **ZX_POL_NEW_FIFO** a process under this job is attempting to create a new fifo. + ** ZX_POL_NEW_FIFO **此作业下的进程正在尝试创建新的fifo。
+ **ZX_POL_NEW_TIMER** a process under this job is attempting to create a new timer. + ** ZX_POL_NEW_TIMER **此作业下的进程正在尝试创建新的计时器。
+ **ZX_POL_NEW_PROCESS** a process under this job is attempting to create a new process. + ** ZX_POL_NEW_PROCESS **此作业下的进程正在尝试创建新进程。
+ **ZX_POL_NEW_PROFILE** a process under this job is attempting to create a new profile. + ** ZX_POL_NEW_PROFILE **此作业下的进程正在尝试创建新的配置文件。
+ **ZX_POL_AMBIENT_MARK_VMO_EXEC** a process under this job is attempting to use [`zx_vmo_replace_as_executable()`] with a **ZX_HANDLE_INVALID**as the second argument rather than a valid **ZX_RSRC_KIND_VMEX**. + ** ZX_POL_AMBIENT_MARK_VMO_EXEC **此作业下的进程正在尝试将带有[ZX_HANDLE_INVALID **]的[`zx_vmo_replace_as_executable（）`]作为第二个参数，而不是有效的** ZX_RSRC_KIND_VMEX **。
+ **ZX_POL_NEW_ANY** is a special *condition* that stands for all of the above **ZX_NEW** conditions such as **ZX_POL_NEW_VMO**,**ZX_POL_NEW_CHANNEL**, **ZX_POL_NEW_EVENT**, **ZX_POL_NEW_EVENTPAIR**,**ZX_POL_NEW_PORT**, **ZX_POL_NEW_SOCKET**, **ZX_POL_NEW_FIFO**,and any future **ZX_NEW** policy. This will include any newkernel objects which do not require a parent object for creation. + ** ZX_POL_NEW_ANY **是特殊的*条件*，代表所有上述** ZX_NEW **条件，例如** ZX_POL_NEW_VMO **，** ZX_POL_NEW_CHANNEL **，** ZX_POL_NEW_EVENT **，** ZX_POL_NEW_EVENTPAIR ** ，** ZX_POL_NEW_PORT **，** ZX_POL_NEW_SOCKET **，** ZX_POL_NEW_FIFO **和任何以后的** ZX_NEW **政策。这将包括不需要父对象来创建的所有新内核对象。

Where *policy* is one of  * policy *是以下其中一项
+ **ZX_POL_ACTION_ALLOW**  allow *condition*.  + ** ZX_POL_ACTION_ALLOW **允许*条件*。
+ **ZX_POL_ACTION_DENY**  prevent *condition*.  + ** ZX_POL_ACTION_DENY **防止*条件*。
+ **ZX_POL_ACTION_ALLOW_EXCEPTION**  generate an exception via the debug port. An exception generated this way acts as a breakpoint. The thread may beresumed after the exception. + ** ZX_POL_ACTION_ALLOW_EXCEPTION **通过调试端口生成异常。以这种方式生成的异常充当断点。异常发生后可以恢复该线程。
+ **ZX_POL_ACTION_DENY_EXCEPTION**  just like **ZX_POL_ACTION_ALLOW_EXCEPTION**, but after resuming *condition* is denied. + ** ZX_POL_ACTION_DENY_EXCEPTION **就像** ZX_POL_ACTION_ALLOW_EXCEPTION **，但在恢复条件后被拒绝。
+ **ZX_POL_ACTION_KILL**  terminate the process.  + ** ZX_POL_ACTION_KILL **终止进程。

 
### **ZX_JOB_POL_TIMER_SLACK**  ** ZX_JOB_POL_TIMER_SLACK ** 

A *topic* of **ZX_JOB_POL_TIMER_SLACK** indicates that *policy* is:  ZX_JOB_POL_TIMER_SLACK **的* topic *表示* policy *为：

```
typedef struct zx_policy_timer_slack {
    zx_duration_t min_slack;
    uint32_t default_mode;
} zx_policy_timer_slack_t;

```
 

*min_slack* specifies the minimum amount of slack applied to timers and deadline-based events created by the job. min_slack *指定应用于作业创建的计时器和基于截止日期的事件的最小松弛量。

If the parent job's *min_slack* is greater than the specified *min_slack* then the parent job's value is used instead. In other words, a job's *min_slack* isthe maximum of the specified value and its parent job's *min_slack*. 如果父作业的* min_slack *大于指定的* min_slack *，那么将使用父作业的值。换句话说，作业的* min_slack *是指定值与其父作业的* min_slack *的最大值。

*default_mode* specifies how slack will be applied when not otherwise indicated by the syscall arguments. A job's *default_mode* may be set regardless of itsparent job's *default_mode*. The possible values for *default_mode* are: * default_mode *指定在syscall参数未另外指定时如何应用松弛。可以设置作业的* default_mode *，而不考虑其父作业的* default_mode *。 * default_mode *的可能值为：
+ **ZX_TIMER_SLACK_CENTER**  + ** ZX_TIMER_SLACK_CENTER **
+ **ZX_TIMER_SLACK_EARLY**  + ** ZX_TIMER_SLACK_EARLY **
+ **ZX_TIMER_SLACK_LATE**  + ** ZX_TIMER_SLACK_LATE **

See [timer slack](/docs/concepts/objects/timer_slack.md) for more information.  有关更多信息，请参见[timer slack]（/ docs / concepts / objects / timer_slack.md）。

When setting timer slack policy, *options* must be **ZX_JOB_POL_RELATIVE** and **count** must be 1. 设置计时器松弛策略时，* options *必须为** ZX_JOB_POL_RELATIVE **，而** count **必须为1。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_JOB** and have **ZX_RIGHT_SET_POLICY**.  *句柄*必须为** ZX_OBJ_TYPE_JOB **类型，并具有** ZX_RIGHT_SET_POLICY **。

 
## RETURN VALUE  返回值 

`zx_job_set_policy()` returns **ZX_OK** on success.  In the event of failure, a negative error value is returned. `zx_job_set_policy（）`成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## NOTES  笔记 

The **ZX_POL_BAD_HANDLE** policy does not apply when calling [`zx_object_get_info()`] with the topic **ZX_INFO_HANDLE_VALID**.  All other topics and all other syscalls thattake handles are subject to the policy. 调用主题为ZX_INFO_HANDLE_VALID **的[`zx_object_get_info（）`]时，** ZX_POL_BAD_HANDLE **策略不适用。所有其他主题以及采用句柄的所有其他syscall均受该策略约束。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *policy* was not a valid pointer, or *count* was 0, or *policy* was not **ZX_JOB_POL_RELATIVE** or **ZX_JOB_POL_ABSOLUTE**, or*topic* was not **ZX_JOB_POL_BASIC**. ** ZX_ERR_INVALID_ARGS ** * policy *不是有效的指针，或者* count *为0，或者* policy *不是** ZX_JOB_POL_RELATIVE **或** ZX_JOB_POL_ABSOLUTE **，或者* topic *不是** ZX_JOB_POL_BASIC ** 。

**ZX_ERR_BAD_HANDLE**  *handle* is not valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*无效。

**ZX_ERR_WRONG_TYPE**  *handle* is not a job handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是作业句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_POL_RIGHT_SET** right.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_POL_RIGHT_SET **权限。

**ZX_ERR_BAD_STATE**  the job has existing jobs or processes alive.  ** ZX_ERR_BAD_STATE **作业具有现有作业或活动进程。

**ZX_ERR_OUT_OF_RANGE** *count* is bigger than **ZX_POL_MAX** or *condition* is bigger than **ZX_POL_MAX**. ** ZX_ERR_OUT_OF_RANGE ** * count *大于** ZX_POL_MAX **或* condition *大于** ZX_POL_MAX **。

**ZX_ERR_ALREADY_EXISTS** existing policy conflicts with the new policy.  ** ZX_ERR_ALREADY_EXISTS **现有策略与新策略冲突。

**ZX_ERR_NOT_SUPPORTED** an entry in *policy* has an invalid value.  ** ZX_ERR_NOT_SUPPORTED ** * policy *中的条目具有无效值。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 
## SEE ALSO  也可以看看 

 
 - [`zx_job_create()`]  -[`zx_job_create（）`]
 - [`zx_object_get_info()`]  -[`zx_object_get_info（）`]
 - [`zx_process_create()`]  -[`zx_process_create（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

