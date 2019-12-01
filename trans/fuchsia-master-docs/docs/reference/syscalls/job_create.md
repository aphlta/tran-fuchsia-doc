 
# zx_job_create  zx_job_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a new job.  创建一个新工作。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_job_create(zx_handle_t parent_job,
                          uint32_t options,
                          zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_job_create()` creates a new child [job object](/docs/concepts/objects/job.md) given a parent job. “ zx_job_create（）”在给定父级工作的情况下创建了一个新的子级[job object]（/ docs / concepts / objects / job.md）。

Upon success a handle for the new job is returned.  成功后，将返回新作业的句柄。

The kernel keeps track of and restricts the "height" of a job, which is its distance from the root job. It is illegal to create a job under a parent whoseheight exceeds an internal "max height" value. (It is, however, legal to createa process under such a job.) 内核跟踪并限制作业的“高度”，即它与根作业的距离。在高度超过内部“最大高度”值的父项下创建作业是非法的。 （但是，在这样的工作下创建流程是合法的。）

Job handles may be waited on (TODO(cpu): expand this)  可能需要等待作业句柄（TODO（cpu）：对此进行扩展）

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*parent_job* must be of type **ZX_OBJ_TYPE_JOB** and have **ZX_RIGHT_MANAGE_JOB**.  * parent_job *必须是** ZX_OBJ_TYPE_JOB **类型，并且必须是** ZX_RIGHT_MANAGE_JOB **。

 
## RETURN VALUE  返回值 

`zx_job_create()` returns **ZX_OK** and a handle to the new job (via *out*) on success.  In the event of failure, a negative error valueis returned. zx_job_create（）在成功时返回** ZX_OK **和新作业的句柄（通过* out *）。发生故障时，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *parent_job* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * parent_job *不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *parent_job* is not a job handle.  ** ZX_ERR_WRONG_TYPE ** * parent_job *不是作业句柄。

**ZX_ERR_INVALID_ARGS**  *options* is nonzero, or *out* is an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** * options *非零，或* out *是无效的指针。

**ZX_ERR_ACCESS_DENIED**  *parent_job* does not have the **ZX_RIGHT_WRITE** or **ZX_RIGHT_MANAGE_JOB** right. ** ZX_ERR_ACCESS_DENIED ** ** parent_job *没有** ZX_RIGHT_WRITE **或** ZX_RIGHT_MANAGE_JOB **权限。

**ZX_ERR_OUT_OF_RANGE**  The height of *parent_job* is too large to create a child job.  ** ZX_ERR_OUT_OF_RANGE ** * parent_job *的高度太大，无法创建子作业。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_BAD_STATE**  The parent job object is in the dead state.  ** ZX_ERR_BAD_STATE **父作业对象处于失效状态。

 
## SEE ALSO  也可以看看 

 
 - [`zx_object_get_property()`]  -[`zx_object_get_property（）`]
 - [`zx_process_create()`]  -[`zx_process_create（）`]
 - [`zx_task_kill()`]  -[`zx_task_kill（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

