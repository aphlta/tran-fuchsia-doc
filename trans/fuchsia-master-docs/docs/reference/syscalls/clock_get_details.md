 
# zx_clock_get_details  zx_clock_get_details 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Fetch all of the low level details of the clock's current status.  获取时钟当前状态的所有低层详细信息。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_clock_get_details(zx_handle_t handle,
                                 uint64_t options,
                                 void* details);
```
 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_CLOCK** and have **ZX_RIGHT_READ**.  *句柄*的类型必须为** ZX_OBJ_TYPE_CLOCK **并具有** ZX_RIGHT_READ **。

 
## DESCRIPTION  描述 

Fetches the fine grained details of the clock object.  See [clocks](/docs/concepts/objects/clock.md) for the specifics of the detailsreported.  Currently, there is only one details structure defined for clocks,`zx_clock_details_v1_t`.  Users must specify the version of the structure usingthe options parameter as well as providing at least`sizeof(zx_clock_details_v1_t)` bytes of storage via the `details`.  Forexample: 获取时钟对象的细粒度细节。有关报告的详细信息，请参见[clocks]（/ docs / concepts / objects / clock.md）。当前，仅为时钟定义了一个细节结构，即zx_clock_details_v1_t。用户必须使用options参数指定结构的版本，并通过“ details”至少提供“ sizeof（zx_clock_details_v1_t）”字节的存储空间。例如：

```c
#include <zircon/syscalls.h>
#include <zircon/syscalls/clock.h>

void GetSomeDetails(zx_handle_t the_clock) {
  zx_clock_details_v1_t details;
  zx_status_t status;

  status = zx_clock_get_details(the_clock, ZX_CLOCK_ARGS_VERSION(1), &details);
  if (status == ZX_OK) {
    // Do great things with our details.
  }
}
```
 

 
## RETURN VALUE  返回值 

On success, returns **ZX_OK** along with clock details stored in the *details* out parameter. 成功时，返回** ZX_OK **以及存储在* details * out参数中的时钟详细信息。

 
## ERRORS  错误 

 
 - **ZX_ERR_BAD_HANDLE** : *handle* is either an invalid handle, or a handle to an object type which is not **ZX_OBJ_TYPE_CLOCK**. -** ZX_ERR_BAD_HANDLE **：* handle *是无效的句柄，或者是不是** ZX_OBJ_TYPE_CLOCK **的对象类型的句柄。
 - **ZX_ERR_ACCESS_DENIED** : *handle* lacks the **ZX_RIGHT_READ** right.  -** ZX_ERR_ACCESS_DENIED **：*句柄*缺少** ZX_RIGHT_READ **权限。
 - **ZX_ERR_INVALID_ARGS** : The version of the details structure signaled by `options` is invalid, or the pointer of the structure passed via `details` is bad. -** ZX_ERR_INVALID_ARGS **：用`options`表示的细节结构的版本无效，或者通过`details`传递的结构的指针是错误的。

 
## SEE ALSO  也可以看看 

 
 - [clock transformations](/docs/concepts/objects/clock_transformations.md)  -[时钟转换]（/ docs / concepts / objects / clock_transformations.md）
 - [clocks](/docs/concepts/objects/clock.md)  -[时钟]（/ docs / concepts / objects / clock.md）
 - [`zx_clock_create()`]  -[`zx_clock_create（）`]
 - [`zx_clock_read()`]  -[`zx_clock_read（）`]
 - [`zx_clock_update()`]  -[`zx_clock_update（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

