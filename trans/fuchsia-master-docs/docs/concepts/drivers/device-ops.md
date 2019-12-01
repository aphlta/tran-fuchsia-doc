 

 
# The Device Protocol  设备协议 

Please refer to the [header comments][device] for descriptions of the methods.  请参阅[标题注释] [设备]中有关方法的说明。

 
## Hook ordering guarantees  挂钩订购保证 

![Hook ordering guarantees](/docs/images/zircon/ddk/driver-hook-ordering.png)  ！[挂钩订购保证]（/ docs / images / zircon / ddk / driver-hook-ordering.png）

The hooks that a driver implements will be invoked by other drivers and by the runtime.  These invocations in some occasions may occur in parallel withinvocations of other or even the same hook.  This section will describe theordering properties that you may rely on. 一个驱动程序实现的挂钩将由其他驱动程序和运行时调用。在某些情况下，这些调用可能在其他乃至同一钩子的并行调用中发生。本节将描述您可能依赖的排序属性。

 
### Terminology  术语 

This section uses the terms *unsequenced*, *indeterminately sequenced*, and *sequenced before* as they are used in the C++ execution model. 本节使用术语“未排序”，“不确定排序”和“在...之前排序”，因为它们在C ++执行模型中使用。

 
### Driver Initialization  驱动程序初始化 

The [zx_driver_ops_t][driver] *init* hook will execute completely before any other hooks for that driver. [zx_driver_ops_t] [driver] * init *钩子将完全执行该驱动器的任何其他钩子。

 
### Driver Teardown  司机拆解 

The [zx_driver_ops_t][driver] *release* hook will begin execution only after all devices created by this driver have been released. 仅在释放由该驱动程序创建的所有设备之后，[zx_driver_ops_t] [driver] * release *挂钩才会开始执行。

 
### Driver Bind  驱动程序绑定 

If tests are enabled, the [zx_driver_ops_t][driver] *bind* hook will begin execution only after the run_unit_tests hook. 如果启用了测试，则[zx_driver_ops_t] [driver] * bind *挂钩仅在run_unit_tests挂钩之后才会开始执行。

 
### Device Lifecycle  设备生命周期 

The device lifecycle begins when some driver successfully invokes **device_add()**.  This may occur on any thread.  No [zx_device_ops_t][device] hooks will run before thedevice's lifecycle has begun or after it has ended. 当一些驱动程序成功调用** device_add（）**时，设备生命周期开始。这可能在任何线程上发生。在设备生命周期开始之前或结束之后，不会运行[zx_device_ops_t] [device]挂钩。

The device lifecycle ends when the device's *release* hook has begun executing.  当设备的* release *挂钩开始执行时，设备生命周期结束。

The [zx_device_ops_t][device] hooks are unsequenced with respect to each other unless otherwise specified. 除非另有说明，否则[zx_device_ops_t] [device]挂钩彼此之间没有顺序。

**Note**: This means that any code that occurs after a call to **device_add()**, even in *bind* hooks, is unsequenced with respect to the end of the created device's lifecycle. **注意**：这意味着在调用** device_add（）**之后发生的任何代码，即使在* bind *挂钩中，也不会对所创建设备生命周期的结束进行排序。

 
### Device Connection Lifecycle  设备连接生命周期 

A device connection lifecycle begins when the [zx_device_ops_t][device] *open* hook begins executing.  None of the [zx_device_ops_t][device] *read*/*write*/*message*/*close* hookswill be invoked if the number of alive device connections is 0. 当[zx_device_ops_t] [device] * open *挂钩开始执行时，设备连接生命周期开始。如果活动设备连接的数量为0，则不会调用[zx_device_ops_t] [device] * read * / * write * / * message * / * close *钩子。

A device connection lifecycle ends when the [zx_device_ops_t][device] *close* hook begins executing.  Any execution of *read*/*write*/*message* hooks is sequenced beforethis. 当[zx_device_ops_t] [device] * close *挂钩开始执行时，设备连接生命周期结束。在此之前，* read * / * write * / * message *挂钩的任何执行都被排序。

Since the *read*/*write*/*message* hooks only execute on the devhost's main thread, they will never be executed concurrently but the processing of outstanding requests fromdifferent connections will be indeterminately sequenced. 由于* read * / * write * / * message *挂钩仅在devhost的主线程上执行，因此它们永远不会同时执行，但是来自不同连接的未完成请求的处理将被不确定地排序。

 
### Device Power Management  设备电源管理 

The [zx_device_ops_t][device] *suspend_new* hook is sequenced before itself (e.g. if a request to suspend to D1 happens, and while that is being executed arequest to suspend to D2 happens, the first will finish before the latterbegins).  It is also sequenced before the *resume_new* hook. [zx_device_ops_t] [device] * suspend_new *钩子在其本身之前进行了排序（例如，如果发生暂停到D1的请求，并且正在执行暂停到D2的请求，则第一个将在后面开始之前完成）。它还在* resume_new *钩子之前排序。

The `set_performance_state` hook is sequenced before itself. It has no particular ordering with suspend/resume hooks.After the driver returns from the set_performance_state hook with success,it is assumed by power manager that the device is operating at the requestedperformance state whenever the device is in working state. Since the hook onlyexecutes on the devhost's main thread, multiple requests are not executedconcurrently.On success, the out_state and the requested_state is same. If the device is in aworking state, the performance state will be changed to requested_state immediately.If the device is in non-working state, the performance state will be the requested_statewhenever the device transitions to working state.On failure, the out_state will have the state that the device can go into. set_performance_state挂钩在其本身之前被排序。它没有特定的挂起/恢复挂接顺序。驱动程序成功从set_performance_state挂接返回后，只要设备处于工作状态，电源管理器就会假定该设备在请求的性能状态下运行。由于钩子仅在devhost的主线程上执行，因此不会并发执行多个请求。成功后，out_state和requested_state相同。如果设备处于工作状态，则性能状态将立即更改为request_state;如果设备处于非工作状态，则无论何时设备转换为工作状态，性能状态均为requested_state;失败时，out_state将具有指出设备可以进入的状态。

The `configure_autosuspend` hook is sequenced before itself and is used to configure whether devices can suspend or resume themselves depending on their idleness. The hook is called withthe deepest sleep state the device is expected to be in which is when the device is suspended.If the entire system is being suspended to a sleep state, the driver should expect `suspend_new`hook to be called, even if the auto suspend is configured. It is not supported to selectivelysuspend a device when auto suspend is configured. configure_autosuspend钩子在其自身之前进行排序，用于配置设备是否可以根据其空闲状态来挂起或恢复自身。该挂接以设备处于挂起状态时应处于的最深睡眠状态被调用。如果整个系统都被挂起到睡眠状态，即使驱动程序挂起，驱动程序也应该希望调用“ suspend_new”挂接。自动挂起已配置。配置了自动挂起后，不支持有选择地挂起设备。

 
### Misc Device APIs  杂项设备API 

The [zx_device_ops_t][device] *get_size* and *get_protocol* hooks are unsequenced with respect to all hooks (including concurrent invocations of themselves).The one exception to this is that they are sequenced before the *release* hook. [zx_device_ops_t] [device] * get_size *和* get_protocol *挂钩对于所有挂钩（包括它们的并发调用）均未排序。唯一的例外是它们在* release *挂钩之前进行了排序。

