 
# zx_clock_update  zx_clock_update 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Make adjustments to a clock object.  调整时钟对象。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_clock_update(zx_handle_t handle,
                            uint64_t options,
                            const void* args);
```
 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_CLOCK** and have **ZX_RIGHT_WRITE**.  *句柄*的类型必须为** ZX_OBJ_TYPE_CLOCK **并具有** ZX_RIGHT_WRITE **。

 
## DESCRIPTION  描述 

Three different parameters may be dynamically controlled by a clock maintainer. They are 时钟维护者可以动态控制三个不同的参数。他们是

 
+ The clock's current value.  +时钟的当前值。
+ The clock's rate adjustment, expressed in PPM deviation from nominal.  +时钟的速率调整，以PPM与额定值的偏差表示。
+ The clock's current estimated error bounds.  +时钟的当前估计误差范围。

When a clock maintainer wishes to change one or more of these parameters, they may do so using the `zx_clock_update` syscall.  Updating a clock's parameters isan atomic operation from the perspective of all other users in the system. 当时钟维护者希望更改这些参数中的一个或多个时，他们可以使用`zx_clock_update`系统调用来进行更改。从系统中所有其他用户的角度来看，更新时钟参数是一项原子操作。

The first update operation performed by a clock maintainer must inclue a valid value.  This update is the update that starts the clock and defines its initialvalue.  Before this update operation has succeeded, the **ZX_CLOCK_STARTED**signal will be de-asserted, and afterwards it will be asserted and remain so forthe lifetime of the clock. 时钟维护者执行的第一次更新操作必须包含有效值。此更新是启动时钟并定义其初始值的更新。在此更新操作成功之前，将取消声明** ZX_CLOCK_STARTED **信号，然后将其置为有效并在时钟的整个生命周期内保持不变。

In order to update a clock, a user fills out the fields of a `zx_clock_update_args_v1_t` structure that they wish to adjust, then passes thestructure to the update call, setting the bits in `options` which indicate whichof these fields are valid and should be set.  Defined `options` bits are 为了更新时钟，用户填写他们希望调整的“ zx_clock_update_args_v1_t”结构的字段，然后将该结构传递给更新调用，并在“ options”中设置指示这些字段中的哪些有效且应为组。定义的“选项”位是

 
+ **ZX_CLOCK_UPDATE_OPTION_VALUE_VALID**  + ** ZX_CLOCK_UPDATE_OPTION_VALUE_VALID **
+ **ZX_CLOCK_UPDATE_OPTION_RATE_ADJUST_VALID**  + ** ZX_CLOCK_UPDATE_OPTION_RATE_ADJUST_VALID **
+ **ZX_CLOCK_UPDATE_OPTION_ERROR_BOUND_VALID**  + ** ZX_CLOCK_UPDATE_OPTION_ERROR_BOUND_VALID **

In addition, maintainer **must** indicate that they are using the V1 version of the struct using the ZX_CLOCK_ARGS_VERSION(...) macro. 另外，维护者**必须**通过ZX_CLOCK_ARGS_VERSION（...）宏指示正在使用结构的V1版本。

For example  例如

```c
#include <zircon/syscalls.h>
#include <zircon/syscalls/clock.h>

void MaintainMyClock(zx_handle_t the_clock) {
  zx_clock_update_args_v1_t args;
  zx_handle_t the_clock;
  zx_status_t status;

  // Set the clock's value to 1500.  Note that this also starts the clock.
  args.value = 1500;
  status = zx_clock_update(the_clock,
                           ZX_CLOCK_ARGS_VERSION(1) | ZX_CLOCK_UPDATE_OPTION_VALUE_VALID,
                           &args);
  if (status != ZX_OK) {
    // Panic!
    return;
  }

  // Make the clock run 23 PPM slower than nominal relative to clock monotonic.
  args.rate_adjust = -23;
  status = zx_clock_update(the_clock,
                           ZX_CLOCK_ARGS_VERSION(1) | ZX_CLOCK_UPDATE_OPTION_RATE_ADJUST_VALID,
                           &args);
  if (status != ZX_OK) {
    // Halt and catch fire
    return;
  }

  // Set the clock to 100,000, make it run 50 PPM faster than nominal, and specify an error bound of
  // +/- 400mSec, all at the same time.
  const uint64_t options = ZX_CLOCK_ARGS_VERSION(1) |
                           ZX_CLOCK_UPDATE_OPTION_VALUE_VALID |
                           ZX_CLOCK_UPDATE_OPTION_RATE_ADJUST_VALID |
                           ZX_CLOCK_UPDATE_OPTION_ERROR_BOUND_VALID;
  args.value = 100000;
  args.rate_adjust = 50;
  args.error_bound = ZX_MSEC(400);
  status = zx_clock_update(the_clock, options, &args);
  if (status != ZX_OK) {
    // Burn down, fall over, and then sink into the swamp.
    return;
  }
}
```
 

 
## RETURN VALUE  返回值 

On success, returns **ZX_OK**.  成功后，返回** ZX_OK **。

 
## ERRORS  错误 

 
 - **ZX_ERR_BAD_HANDLE** : *handle* is either an invalid handle, or a handle to an object type which is not **ZX_OBJ_TYPE_CLOCK**. -** ZX_ERR_BAD_HANDLE **：* handle *是无效的句柄，或者是不是** ZX_OBJ_TYPE_CLOCK **的对象类型的句柄。
 - **ZX_ERR_ACCESS_DENIED** : *handle* lacks the **ZX_RIGHT_WRITE** right.  -** ZX_ERR_ACCESS_DENIED **：*句柄*缺少** ZX_RIGHT_WRITE **权限。
 - **ZX_ERR_INVALID_ARGS** : The update request made is incompatible with the properties of the clock.  See the **DESCRIPTION** section for details ofpermissible clock update operations.  Otherwise, the version/pointer ofthe arguments structure is incorrect. -** ZX_ERR_INVALID_ARGS **：发出的更新请求与时钟的属性不兼容。有关允许的时钟更​​新操作的详细信息，请参见“说明”部分。否则，参数结构的版本/指针不正确。

 
## SEE ALSO  也可以看看 

 
 - [clocks](/docs/concepts/objects/clock.md)  -[时钟]（/ docs / concepts / objects / clock.md）
 - [`zx_clock_create()`]  -[`zx_clock_create（）`]
 - [`zx_clock_get_details()`]  -[`zx_clock_get_details（）`]
 - [`zx_clock_read()`]  -[`zx_clock_read（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

