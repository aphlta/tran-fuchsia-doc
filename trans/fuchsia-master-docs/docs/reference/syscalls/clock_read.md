 
# zx_clock_read  zx_clock_read 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Perform a basic read of the clock.  对时钟进行基本读取。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_clock_read(zx_handle_t handle, zx_time_t* now);
```
 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_CLOCK** and have **ZX_RIGHT_READ**.  *句柄*的类型必须为** ZX_OBJ_TYPE_CLOCK **并具有** ZX_RIGHT_READ **。

 
## DESCRIPTION  描述 

Perform a basic read of the clock object and return its current time in the *now* out parameter. 对Clock对象执行基本读取，并在* now * out参数中返回其当前时间。

 
## RETURN VALUE  返回值 

On success, returns **ZX_OK** along with the clock's current time in the *now* output parameter.  成功时，在* now *输出参数中返回** ZX_OK **以及时钟的当前时间。

 
## ERRORS  错误 

 
 - **ZX_ERR_BAD_HANDLE** : *handle* is either an invalid handle, or a handle to an object type which is not **ZX_OBJ_TYPE_CLOCK**. -** ZX_ERR_BAD_HANDLE **：* handle *是无效的句柄，或者是不是** ZX_OBJ_TYPE_CLOCK **的对象类型的句柄。
 - **ZX_ERR_ACCESS_DENIED** : *handle* lacks the **ZX_RIGHT_READ** right.  -** ZX_ERR_ACCESS_DENIED **：*句柄*缺少** ZX_RIGHT_READ **权限。
 - **ZX_ERR_BAD_STATE** : The clock object has never been updated.  No initial time has been established yet. -** ZX_ERR_BAD_STATE **：时钟对象从未更新。尚未确定初始时间。

 
## SEE ALSO  也可以看看 

 
 - [clocks](/docs/concepts/objects/clock.md)  -[时钟]（/ docs / concepts / objects / clock.md）
 - [`zx_clock_create()`]  -[`zx_clock_create（）`]
 - [`zx_clock_get_details()`]  -[`zx_clock_get_details（）`]
 - [`zx_clock_update()`]  -[`zx_clock_update（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

