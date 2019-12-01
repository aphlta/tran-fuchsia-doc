 
# Clock  时钟 

 
## NAME  名称 

clock - Kernel object used to track the progress of time.  时钟-用于跟踪时间进度的内核对象。

 
## SYNOPSIS  概要 

A clock is a one dimensional affine transformation of the [clock monotonic](/docs/reference/syscalls/clock_get_monotonic.md) referencetimeline which may be atomically adjusted by a clock maintainer, and observed byclients. 时钟是[clock单调]（/ docs / reference / syscalls / clock_get_monotonic.md）参考时间轴的一维仿射变换，可以由时钟维护者自动调整并由客户端观察。

 
## DESCRIPTION  描述 

 
### Properties  物产 

The properties of a clock are established when the clock is created and cannot be changed afterwards.  Currently, three clock properties are defined. 时钟的属性是在创建时钟时建立的，以后不能更改。当前，定义了三个时钟属性。

 
#### **ZX_CLOCK_OPT_MONOTONIC**  ** ZX_CLOCK_OPT_MONOTONIC ** 

When set, the clock is guaranteed to have monotonic behavior.  This is to say that any sequence of observations of the clock is guaranteed to produce asequence of times which are always greater than or equal to the previousobservations.  A monotonic clock can never go backwards, although it _can_ jumpforwards.  Formally: 设置后，时钟将保证具有单调性。这就是说，保证对时钟的任何观察序列都可以产生总是大于或等于先前观察结果的时间顺序。尽管单调时钟可以向前跳，但永远不能向后退。正式地：

Given a clock _C_, Let C(x) be the function which maps from the reference timeline _C's_ timeline.  C(x) is a piecewise linear function made up of all theaffine transformation segments over all time as determined  by _C's_ maintainer._C_ is monotonic if and only if: 给定时钟_C_，令C（x）为从参考时间线_C's_时间线映射的函数。 C（x）是由_C's_保持器确定的，在整个时间内所有仿射变换段组成的分段线性函数._C_在以下情况下是单调的：

for all _R<sub>1</sub>_, _R<sub>2</sub>_ : _R<sub>2</sub> >= R<sub>1</sub>_  对于所有_R <sub> 1 </ sub> _，_R <sub> 2 </ sub> _：_R <sub> 2 </ sub>> = R <sub> 1 </ sub> _

_C(R<sub>2</sub>) >= C(R<sub>1</sub>)_  _C（R <sub> 2 </ sub>）> = C（R <sub> 1 </ sub>）_

 
#### **ZX_CLOCK_OPT_CONTINUOUS**  ** ZX_CLOCK_OPT_CONTINUOUS ** 

When set, the clock is guaranteed to have continuous behavior.  This is to say that any update to the clock transformation is guaranteed to be first ordercontinuous with the previous transformation segment.  Formally: 设置后，时钟将保证具有连续行为。这就是说，时钟转换的任何更新都保证与上一个转换段是一阶连续的。正式地：

Let _C<sub>i</sub>(x)_ be the _i<sub>th</sub>_ affine transformation segment of _C(x)_.  Let _R<sub>i</sub>_ be the first point in time on the reference timelinefor which _C<sub>i</sub>(x)_ is defined.  A clock _C_ is continuous if and onlyif: for all _i_ 令_C <sub> i </ sub>（x）_是_C（x）_的第_i <sub> </ sub> _个仿射变换段。令_R <sub> i </ sub> _为参考时间线上定义_C <sub> i </ sub>（x）_的第一个时间点。当且仅当：对于所有_i_，时钟_C_是连续的

_C<sub>i</sub>(R<sub>i + 1</sub>) = C<sub>i + 1</sub>(R<sub>i + 1</sub>)_  _C <sub> i </ sub>（R <sub> i +1 </ sub>）= C <sub> i +1 </ sub>（R <sub> i +1 </ sub>）_

 
#### **Backstop Time**  **支持时间** 

The backstop time of a clock represents the minimum value that a clock may ever be set to.  Since clocks can only tick forwards, and never backwards, it isimpossible for an observer of a clock to ever receive a value which is less thanthe backstop time configured by a clock's creator. 时钟的逆止时间表示可能已设置为时钟的最小值。由于时钟只能向前滴答，而不能向后滴答，因此时钟观察者不可能收到小于时钟创建者配置的逆止时间的值。

A backstop time may be provided via the `zx_create_args_v1_t` structure at creation time.  Otherwise, it will default to 0. 可以在创建时通过`zx_create_args_v1_t`结构提供一个后备时间。否则，它将默认为0。

During clock update operations, any attempt to set the clock's value to something less than the backstop time will fail with **ZX_ERR_INVALID_ARGS**.  Aclock which has not been initially set will always report the backstop timeconfigured for the clock.  Backtop times may never be less than the defaultvalue of zero. 在时钟更新操作期间，任何将时钟值设置为小于Backstop时间的尝试都将失败，并显示** ZX_ERR_INVALID_ARGS **。最初未设置的时钟将始终报告为该时钟配置的逆止时间。 Backtop时间永远不能小于默认值零。

 
### Implied properties  隐含属性 

 
+ The reference clock for all clock objects in the system is clock monotonic.  +系统中所有时钟对象的参考时钟是单调的时钟。
+ The nominal units of all clock objects are specified to be nanoseconds.  This property is not configurable. +所有时钟对象的标称单位指定为纳秒。此属性不可配置。
+ The units of frequency adjustment for all clock objects are specified to be parts per million, or PPM. +所有时钟对象的频率调整单位指定为百万分之一或PPM。
+ The maximum permissible range of frequency adjustment of a clock object is specified to be [-1000, +1000] PPM.  This property is not configurable. +时钟对象的频率调整的最大允许范围指定为[-1000，+1000] PPM。此属性不可配置。

 
### Reading the clock  读时钟 

Given a clock handle, users may query the current time given by that clock using the `zx_clock_read()` syscall.  Clock reads **ZX_RIGHT_READ** permissions.  Clockreads are guaranteed to be coherent for all observers.  This is to say that, iftwo observers query the clock at exactly the same reference time _R_, that theywill always see the same value _C(R)_. 给定一个时钟句柄，用户可以使用zx_clock_read（）系统调用查询该时钟给定的当前时间。时钟读取** ZX_RIGHT_READ **权限。保证所有观察者的时钟一致。这就是说，如果两个观察者在完全相同的参考时间_R_处查询时钟，则他们将始终看到相同的值_C（R）_。

 
### Reference timelines, `zx_ticks_get()`, and `zx_clock_get_monotonic()`  参考时间轴“ zx_ticks_get（）”和“ zx_clock_get_monotonic（）” 

As noted earlier, zx_clock_get_monotonic() is the reference timeline for all user-created zircon clocks.  This means that if a user knows a clock instance'scurrent transformation, then given a value on the clock instance's timeline, thecorresponding point on the clock monotonic timeline may be computed (andvice-versa).  It also means that in the absence of a rate adjustment made to thekernel clock, clock monotonic and the kernel clock will tick at exactly the samerate. 如前所述，zx_clock_get_monotonic（）是所有用户创建的锆石时钟的参考时间线。这意味着，如果用户知道时钟实例的当前转换，然后在时钟实例的时间轴上给定一个值，则可以计算时钟单调时间轴上的对应点（反之亦然）。这也意味着在没有对内核时钟进行速率调整的情况下，时钟单调性和内核时钟将以完全相同的速率滴答。

In addition to the clock monotonic timeline, the zircon kernel also exposes the "ticks" timeline via `zx_ticks_get()` and `zx_ticks_per_second()`.  Internally,ticks is actually the reference timeline for clock monotonic and is readdirectly from an architecture appropriate timer unit accessible to the kernel.Clock monotonic is actually a linear transformation of the ticks timelinenormalized to nanosecond units.  Both timelines start ticking from zero as thekernel starts. 除时钟单调时间轴外，锆石内核还通过zx_ticks_get（）和zx_ticks_per_second（）公开“ ticks”时间轴。在内部，滴答实际上是时钟单调的参考时间线，并且是从内核可以访问的体系结构适当的计时器单元中直接读取的。时钟单调实际上是将滴答时间线标准化为纳秒单位的线性变换。内核启动时，两个时间线都从零开始滴答。

Because clock monotonic is a static transformation based on ticks, and all kernel clocks are transformations based on clock monotonic, ticks may also serve as areference clock for kernel clocks in addition to clock monotonic. 由于时钟单调是基于时钟的静态转换，并且所有内核时钟都是基于时钟单调的转换，因此除了时钟单调之外，时钟也可以用作内核时钟的参考时钟。

 
### Fetching the clock's details  取得时钟的详细信息 

In addition to simply reading the current value of the clock, advanced users who possess **ZX_RIGHT_READ** permissions may also read the clock and get extendeddetails in the process using `zx_clock_get_details()`.  Upon a successful call,the details structure returned to callers will include: 除了简单地读取时钟的当前值外，拥有** ZX_RIGHT_READ **权限的高级用户还可以使用zx_clock_get_details（）读取时钟并获得扩展的详细信息。呼叫成功后，返回给呼叫者的详细信息结构将包括：

 
+ The current clock monotonic to clock transformation.  +当前时钟单调转换为时钟。
+ The current ticks to clock transformation.  +当前滴答时钟转换。
+ The current symmetric error estimate (if any) for the clock.  +时钟的当前对称误差估计（如果有）。
+ The last time the clock was updated as defined by the clock monotonic reference timeline. +上次更新时钟的时间是由时钟单调参考时间线定义的。
+ An observation of the system tick counter which was taken during the observation of the clock. +观察时钟期间对系统刻度计数器的观察。
+ All of the static properties of the clock defined at creation time.  +在创建时定义的时钟的所有静态属性。
+ A generation nonce.  +一代随机数。

Advanced users may use these details to not only compute a recent `now` value for the clock (by transforming the reported ticks-now observation using theticks-to-clock transformation, both reported by the get details operation), butto also: 高级用户不仅可以使用这些详细信息来计算时钟的最近“现在”值（通过使用“时钟到时钟”的转换来转换所报告的“现在的滴答”观察，这两者均由“获取详细信息”操作报告），还可以：

 
+ Know whether the clock transformation has been changed since the last `zx_clock_get_details()` operation (using the generation nonce). +了解自上次执行zx_clock_get_details（）操作以来，时钟转换是否已更改（使用生成随机数）。
+ Compose the clock transformation with other clocks' transformations to reason about the relationship between two clocks. +将时钟转换与其他时钟的转换组合，以推断两个时钟之间的关系。
+ Know the clock maintainer's best estimate of absolute error.  +了解时钟维护者对绝对误差的最佳估计。
+ Reason about the range of possible future values of the clock relative to the reference clock based on the last correction time, the current transformation,and the maximum permissible correction factor for the clock (see the maximumpermissive range of frequency adjustment described in the |Implied properties|section above. +基于上次校正时间，当前转换以及时钟的最大允许校正因子，确定时钟相对于参考时钟的可能未来值范围的原因（请参阅| Impplied中所述的最大频率调整范围）以上属性。

 
### Starting a clock and Clock Signals  启动时钟和时钟信号 

Immediately after creation, a clock has not yet been started.  All attempts to read the clock will return the clock's configured backstop time, which defaultsto 0 if unspecified during creation. 创建后，时钟尚未立即启动。所有尝试读取时钟的尝试都将返回时钟的配置后备时间，如果在创建过程中未指定，则默认为0。

A clock begins running after the very first update operation performed by a clock's maintainer, which **must** include a set-value operation.  The clockwill begin running at that point with a rate equal to the reference clock plusthe deviation from nominal specified by the maintainer. 在时钟的维护者执行的第一个更新操作之后，时钟开始运行，该操作必须包括设置值操作。时钟将在此点开始运行，其速率等于参考时钟加上维护人员指定的标称偏差。

Clocks also have a **ZX_CLOCK_STARTED** signal which may be used by users to know when the clock has actually been started.  Initially, this signal is notset, but it becomes set after the first successful update operation.  Oncestarted, a clock will never stop and the **ZX_CLOCK_STARTED** signal will alwaysbe asserted. 时钟还具有** ZX_CLOCK_STARTED **信号，用户可以使用它来了解时钟的实际启动时间。最初，此信号未设置，但在首次成功进行更新操作后变为设置。一旦启动，时钟将永远不会停止，并且** ZX_CLOCK_STARTED **信号将始终置为有效。

 
### Maintaining a clock.  维持时钟。 

Users who possess **ZX_RIGHT_WRITE** permissions for a clock object may act as a maintainer of the clock using the `zx_clock_update()` syscall.  Three parametersof the clock may be adjusted during each call to `zx_clock_update()`, but notall three need to be adjusted each time.  These values are: 拥有时钟对象的** ZX_RIGHT_WRITE **权限的用户可以使用zx_clock_update（）系统调用充当时钟的维护者。每次调用zx_clock_update（）时，可以调整时钟的三个参数，但并非每次都需要调整三个参数。这些值是：

 
+ The clock's absolute value.  +时钟的绝对值。
+ The frequency adjustment of the clock (deviation from nominal expressed in ppm) +时钟的频率调整（与标称值的偏差，以ppm表示）
+ The absolute error estimate of the clock (expressed in nanoseconds)  +时钟的绝对误差估计（以纳秒为单位）

Changes to a clocks transformation occur during the syscall itself.  The specific reference time of the adjustment may not be specified by the user. 对时钟转换的更改发生在系统调用本身期间。用户可能未指定调整的特定参考时间。

Any change to the absolute value of a clock with the **ZX_CLOCK_OPT_MONOTONIC** property set on it which would result in non-monotonic behavior will fail with areturn code of **ZX_ERR_INVALID_ARGS**. 设置了** ZX_CLOCK_OPT_MONOTONIC **属性的时钟绝对值的任何更改都会导致非单调的行为，将失败，返回码为** ZX_ERR_INVALID_ARGS **。

The first update operation is what starts a clock ticking and **must** include a set-value operation. 第一个更新操作是启动时钟滴答的操作，并且**必须**包含设置值操作。

Aside from the very first set-value  operation, all attempts to set the absolute value of a clock with the **ZX_CLOCK_OPT_CONTINUOUS** property set on it willfail with a return code of **ZX_ERR_INVALID_ARGS** 除了第一个设置值操作外，所有尝试在其上设置了** ZX_CLOCK_OPT_CONTINUOUS **属性的情况下设置时钟绝对值的尝试都将失败，返回码为** ZX_ERR_INVALID_ARGS **

 
## SYSCALLS  SYSCALLS 

 
 - [clock transformations](/docs/concepts/objects/clock_transformations.md)  -[时钟转换]（/ docs / concepts / objects / clock_transformations.md）
 - [`zx_clock_create()`] - create a clock  -[`zx_clock_create（）`]-创建时钟
 - [`zx_clock_read()`] - read the time of the clock  -[`zx_clock_read（）`]-读取时钟时间
 - [`zx_clock_get_details()`] - fetch the details of a clock's relationship to clock monotonic  -[`zx_clock_get_details（）`]-获取时钟与时钟单调关系的详细信息
