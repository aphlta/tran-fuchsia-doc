 
# zx_system_get_event  zx_system_get_event 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Retrieve a handle to a system event.  检索系统事件的句柄。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_system_get_event(zx_handle_t root_job,
                                uint32_t kind,
                                zx_handle_t* event);
```
 

 
## DESCRIPTION  描述 

*root_job* must be a handle to the root job of the system with the MANAGE_PROCESS right. * root_job *必须是具有MANAGE_PROCESS权限的系统根作业的句柄。

The only valid value for *kind* is ZX_SYSTEM_EVENT_LOW_MEMORY.  * kind *的唯一有效值为ZX_SYSTEM_EVENT_LOW_MEMORY。

When *kind* is ZX_SYSTEM_EVENT_LOW_MEMORY, an *event* will be returned that will assert ZX_EVENT_SIGNALED when the system is nearing an out-of-memory situation.A process that is waiting on this event must quickly perform any importantshutdown work. It is unspecified how much memory is available at the time thisevent is signaled, and unspecified how long the waiting process has to actbefore the kernel starts terminating processes or starting a full system reboot. 当* kind *为ZX_SYSTEM_EVENT_LOW_MEMORY时，将返回* event *，当系统接近内存不足的情况时将断言ZX_EVENT_SIGNALED。正在等待此事件的进程必须快速执行任何重要的关机工作。未指定在发出此事件时有多少可用内存，也未指定在内核开始终止进程​​或开始完全重启系统之前等待进程必须执行多长时间。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## RETURN VALUE  返回值 

`zx_system_get_event()` returns ZX_OK on success, and *event* will be a valid handle, or an error code from below on failure. `zx_system_get_event（）`成功返回ZX_OK，* event *将是有效的句柄，失败则返回错误代码。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** The calling process' policy was invalid, the handle *root_job* did not have ZX_RIGHT_MANAGE_PROCESS rights, *root_job* was not theroot job of the system. ** ZX_ERR_ACCESS_DENIED **调用进程的策略无效，句柄* root_job *不具有ZX_RIGHT_MANAGE_PROCESS权限，* root_job *不是系统的root作业。

