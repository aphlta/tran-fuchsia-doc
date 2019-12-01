 
# zx_profile_create  zx_profile_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a scheduler profile.  创建一个调度程序配置文件。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_profile_create(zx_handle_t root_job,
                              uint32_t options,
                              const zx_profile_info_t* profile,
                              zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

`zx_profile_create()` creates a new [profile](/docs/concepts/objects/profile.md) object.  zx_profile_create（）创建一个新的[profile]（/ docs / concepts / objects / profile.md）对象。

The parameter *profile* specifies the settings in the profile, which in turn will be applied to threads when [`zx_object_set_profile()`] is called. Thefields of *profile* are shown below. *options* must be zero. 参数* profile *指定配置文件中的设置，当调用[`zx_object_set_profile（）]时，这些设置将依次应用于线程。 * profile *的字段如下所示。 * options *必须为零。

```c
#define ZX_PROFILE_INFO_FLAG_PRIORITY (1 << 0)
#define ZX_PROFILE_INFO_FLAG_CPU_MASK (1 << 1)

typedef struct zx_profile_info {
  // A bitmask of ZX_PROFILE_INFO_FLAG_* values. Specifies which fields
  // below have been specified. Other fields are considered unset.
  uint32_t flags;

  // Scheduling priority. |flags| must have ZX_PROFILE_INFO_FLAG_PRIORITY set.
  int32_t priority;

  // CPUs that threads may be scheduled on. |flags| must have
  // ZX_PROFILE_INFO_FLAG_CPU_MASK set.
  zx_cpu_set_t cpu_affinity_mask;
} zx_profile_info_t;
```
 

The `flags` field specifies which fields in the `zx_profile_info_t` structure contain valid values. Values in fields without a corresponding `flag` bit setwill be ignored. This allows fields with values of `0` and unset fields to bedistinguished, even if additional fields are added in future. “ flags”字段指定“ zx_profile_info_t”结构中的哪些字段包含有效值。没有设置相应的“标志”位的字段中的值将被忽略。即使将来添加其他字段，也可以区分值为0的字段和未设置的字段。

Upon success a handle for the new profile is returned.  成功后，将返回新配置文件的句柄。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*root_job* must be of type **ZX_OBJ_TYPE_JOB** and have **ZX_RIGHT_MANAGE_PROCESS**.  * root_job *必须为** ZX_OBJ_TYPE_JOB **类型，并且必须为** ZX_RIGHT_MANAGE_PROCESS **。

 
## RETURN VALUE  返回值 

Returns **ZX_OK** and a handle to the new profile (via *out*) on success. In the event of failure, a negative error value is returned. 成功返回** ZX_OK **和新配置文件的句柄（通过* out *）。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *root_job* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * root_job *不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *root_job* is not a job handle.  ** ZX_ERR_WRONG_TYPE ** * root_job *不是作业句柄。

**ZX_ERR_ACCESS_DENIED**  *root_job* does not have **ZX_RIGHT_MANAGE_PROCESS** right, or *root_job* is not a handle to the root job. ** ZX_ERR_ACCESS_DENIED ** * root_job *没有** ZX_RIGHT_MANAGE_PROCESS **权限，或者* root_job *不是根作业的句柄。

**ZX_ERR_INVALID_ARGS**  One or more of the arguments provided were invalid:  ** ZX_ERR_INVALID_ARGS **提供的一个或多个参数无效：
  * *profile* or *out* was an invalid pointer  * * profile *或* out *是无效的指针
  * *flags* contains an unknown option  * *标志*包含未知选项
  * *options* was not zero  * *选项*不为零
  * *priority* was an invalid priority  * *优先级*是无效的优先级

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory.  ** ZX_ERR_NO_MEMORY **由于内存不足而失败。

 
## SEE ALSO  也可以看看 

 
 - [`zx_object_set_profile()`]  -[`zx_object_set_profile（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

