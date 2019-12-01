 
# zx_clock_create  zx_clock_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a new clock object.  创建一个新的时钟对象。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_clock_create(uint64_t options,
                            const void* args,
                            zx_handle_t* out);
```
 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

None.  没有。

 
## DESCRIPTION  描述 

Creates a new zircon clock object.  See [clocks](/docs/concepts/objects/clock.md) for an overview of clock objects. 创建一个新的锆石时钟对象。有关时钟对象的概述，请参见[clocks]（/ docs / concepts / objects / clock.md）。

 
### Options  选件 

Two options are currently defined for clock objects.  当前为时钟对象定义了两个选项。

 
+ **ZX_CLOCK_OPT_MONOTONIC** : When set, creates a clock object which is guaranteed to never run backwards.  Monotonic clocks must always move forward. + ** ZX_CLOCK_OPT_MONOTONIC **：置位时，创建一个时钟对象，该对象永远不会向后运行。单调时钟必须始终向前移动。
+ **ZX_CLOCK_OPT_CONTINUOUS** : When set, creates a clock which is guaranteed to never jump either forwards or backwards.  Continuous clocks may only bemaintained using frequency adjustments and are, by definition, also monotonic.Attempting to create a clock object with the **ZX_CLOCK_OPT_CONTINUOUS** optionspecified, but without the **ZX_CLOCK_OPT_MONOTONIC** option specified is anerror which will be signalled with **ZX_ERR_INVALID_ARGS**. + ** ZX_CLOCK_OPT_CONTINUOUS **：置位时，创建一个时钟，保证永远不会向前或向后跳跃。连续时钟只能通过频率调整来保持，并且根据定义也可以是单调的。尝试创建具有指定的** ZX_CLOCK_OPT_CONTINUOUS **选项但未指定** ZX_CLOCK_OPT_MONOTONIC **选项的时钟对象是一个错误，将通过*发出信号* ZX_ERR_INVALID_ARGS **。

 
### Arguments  争论 

One additional creation-time argument may be specified when configuring the clock, the backstop time.  See [clocks](/docs/concepts/objects/clock.md) for more details about backstop times. 配置时钟时，可以指定一个附加的创建时间参数，即逆止时间。请参阅[clocks]（/ docs / concepts / objects / clock.md）了解有关支持时间的更多详细信息。

In order to configure a backstop time, a user must pass a `zx_clock_create_args_v1_t` structure to the `zx_clock_create` call via the `args` parameter.  Additionally, the `options` bits must have`ZX_CLOCK_ARGS_VERSION(1)` set in them. 为了配置支持时间，用户必须通过args参数将zx_clock_create_args_v1_t结构传递给zxclock_create调用。另外，“ options”位必须在其中设置“ ZX_CLOCK_ARGS_VERSION（1）”。

For example, a user who wished to create a monotonic clock with a backstop time of 5500 might do something like the following. 例如，希望创建支持时间为5500的单调时钟的用户可能会执行以下操作。

```c
#include <zircon/syscalls.h>
#include <zircon/syscalls/clock.h>

zx_handle_t MakeAClock() {
  zx_clock_create_args_v1_t args;
  zx_handle_t the_clock;
  zx_status_t status;

  args.backstop_time = 5500;
  status = zx_clock_create(ZX_CLOCK_ARGS_VERSION(1) | ZX_CLOCK_OPT_MONOTONIC, &args, &the_clock);
  if (status != ZX_OK) {
    // Log the error
    return ZX_HANDLE_INVALID;
  }

  return the_clock;
}
```
 

Users do not have to supply an arguments structure.  If an explicit backstop is not required, users may omit the version bits from the options parameter and simply pass nullptr for args. 用户不必提供参数结构。如果不需要显式的后备支持，则用户可以从options参数中省略版本位，而只需为args传递nullptr即可。

 
## RETURN VALUE  返回值 

On success, returns **ZX_OK** along with a new clock object via the *out* handle.  Handles to newly created clock objects will have the **ZX_RIGHT_READ**and **ZX_RIGHT_WRITE** rights assigned to them. 成功时，通过* out *句柄返回** ZX_OK **以及新的时钟对象。新创建的时钟对象的句柄将具有** ZX_RIGHT_READ **和** ZX_RIGHT_WRITE **权限。

 
## ERRORS  错误 

 
 - **ZX_ERR_INVALID_ARGS** : An invalid option flag was specified, a bad args structure version/pointer was passed, or **ZX_CLOCK_OPT_CONTINUOUS** was specified without alsospecifying **ZX_CLOCK_OPT_MONOTONIC**. -** ZX_ERR_INVALID_ARGS **：指定了无效的选项标志，或者传递了错误的args结构版本/指针，或者指定了** ZX_CLOCK_OPT_CONTINUOUS **而不指定** ZX_CLOCK_OPT_MONOTONIC **。
 - **ZX_ERR_NO_MEMORY**  Failure due to lack of memory.  -** ZX_ERR_NO_MEMORY **由于内存不足而失败。

 
## SEE ALSO  也可以看看 

 
 - [clocks](/docs/concepts/objects/clock.md)  -[时钟]（/ docs / concepts / objects / clock.md）
 - [`zx_clock_get_details()`]  -[`zx_clock_get_details（）`]
 - [`zx_clock_read()`]  -[`zx_clock_read（）`]
 - [`zx_clock_update()`]  -[`zx_clock_update（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

