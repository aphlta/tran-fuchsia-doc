 
# zx_object_get_property  zx_object_get_property 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Ask for various properties of various kernel objects.  询问各种内核对象的各种属性。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_object_get_property(zx_handle_t handle,
                                   uint32_t property,
                                   void* value,
                                   size_t value_size);
```
 

 
## DESCRIPTION  描述 

`zx_object_get_property()` requests the value of a kernel object's property. Getting a property requires **ZX_RIGHT_GET_PROPERTY** rights on the handle. zx_object_get_property（）请求内核对象属性的值。获取属性需要在手柄上具有** ZX_RIGHT_GET_PROPERTY **权限。

The *handle* parameter indicates the target kernel object. Different properties only work on certain types of kernel objects, as described below. * handle *参数指示目标内核对象。如下所述，不同的属性仅适用于某些类型的内核对象。

The *property* parameter indicates which property to get/set. Property values have the prefix **ZX_PROP_**, and are described below. * property *参数指示要获取/设置的属性。属性值的前缀为** ZX_PROP _ **，如下所述。

The *value* parameter holds the property value, and must be a pointer to a buffer of *value_size* bytes. Different properties expect different valuetypes/sizes as described below. * value *参数保存属性值，并且必须是指向* value_size *个字节的缓冲区的指针。如下所述，不同的属性期望不同的值类型/大小。

 
## PROPERTIES  性质 

Property values have the prefix **ZX_PROP_**, and are defined in  属性值的前缀为** ZX_PROP _ **，并且在

```
#include <zircon/syscalls/object.h>
```
 

 
### ZX_PROP_NAME  ZX_PROP_NAME 

*handle* type: **(Most types)**  *句柄*类型：**（大多数类型）**

*value* type: `char[ZX_MAX_NAME_LEN]`  *值*类型：`char [ZX_MAX_NAME_LEN]`

Allowed operations: **get**, **set**  允许的操作：**获取**，**设置**

The name of the object, as a NUL-terminated string.  对象的名称，以NULL终止的字符串。

 
### ZX_PROP_REGISTER_FS and ZX_PROP_REGISTER_GS  ZX_PROP_REGISTER_FS和ZX_PROP_REGISTER_GS 

*handle* type: **Thread**  *手柄*类型：**螺纹**

*value* type: `uintptr_t`  *值*类型：`uintptr_t`

Allowed operations: **set**  允许的操作：**设置**

The value of the x86 FS or GS segment register. `value` must be a canonical address, and must be a userspace address. x86 FS或GS段寄存器的值。 “值”必须是规范地址，并且必须是用户空间地址。

Only defined for x86-64.  仅针对x86-64定义。

 
### ZX_PROP_PROCESS_DEBUG_ADDR  ZX_PROP_PROCESS_DEBUG_ADDR 

*handle* type: **Process**  *句柄*类型：**处理**

*value* type: `uintptr_t`  *值*类型：`uintptr_t`

Allowed operations: **get**, **set**  允许的操作：**获取**，**设置**

The value of ld.so's `_dl_debug_addr`. This can be used by debuggers to interrogate the state of the dynamic loader. ld.so的_dl_debug_addr的值。调试器可以使用它来查询动态加载器的状态。

If this value is set to `ZX_PROCESS_DEBUG_ADDR_BREAK_ON_SET` on process creation, the loader will manually issue a debug breakpoint when the propertyhas been set to its correct value. This gives an opportunity to read or modifythe initial state of the program. 如果在创建进程时将此值设置为`ZX_PROCESS_DEBUG_ADDR_BREAK_ON_SET`，则当属性设置为正确值时，加载程序将手动发出调试断点。这为读取或修改程序的初始状态提供了机会。

 
### ZX_PROP_PROCESS_BREAK_ON_LOAD  ZX_PROP_PROCESS_BREAK_ON_LOAD 

*handle* type: **Process**  *句柄*类型：**处理**

*value* type: `uintptr_t`  *值*类型：`uintptr_t`

Allowed operations: **get**, **set**  允许的操作：**获取**，**设置**

Determines whether the dynamic loader will issue a debug trap on every load of a shared library. If set before the first thread of a process runs, it will alsotrigger a debug trap for the initial load. 确定动态加载程序是否将在共享库的每次加载时发出调试陷阱。如果在进程的第一个线程运行之前设置，它还将触发调试陷阱以进行初始加载。

The dynamic loader sets the expected value of `ZX_PROP_PROCESS_DEBUG_ADDR` before triggering this debug trap. Exception handlers can use this property to query thedynamic loader's state. 动态加载程序在触发此调试陷阱之前，会设置ZX_PROP_PROCESS_DEBUG_ADDR的期望值。异常处理程序可以使用此属性查询动态加载程序的状态。

When the dynamic loader issues the debug trap, it sets the value of the `r_brk_on_load` member on the `r_debug` struct exposed by the dynamic loader. The address of thisstruct can be obtained by the `ZX_PROP_PROCESS_DEBUG_ADDR` property. 当动态加载程序发出调试陷阱时，它会在动态加载程序公开的`r_debug`结构上设置`r_brk_on_load`成员的值。这个结构的地址可以通过`ZX_PROP_PROCESS_DEBUG_ADDR`属性获得。

Any non-zero value is considered to activate this feature. Setting this property to zero will disable it. 任何非零值都被认为可以激活此功能。将此属性设置为零将禁用它。

Note: Depending on the architecture, the address reported by the exception might be different that the one reported by this property. For example, an x64 platform reportsthe instruction pointer *after* it executes the instruction.  This means that an x64platform reports an instruction pointer one byte higher than this property. 注意：根据体系结构，异常报告的地址可能与此属性报告的地址不同。例如，x64平台在执行指令后*后报告指令指针。这意味着x64平台报告的指令指针比此属性高一个字节。

 
### ZX_PROP_PROCESS_VDSO_BASE_ADDRESS  ZX_PROP_PROCESS_VDSO_BASE_ADDRESS 

*handle* type: **Process**  *句柄*类型：**处理**

*value* type: `uintptr_t`  *值*类型：`uintptr_t`

Allowed operations: **get**  允许的操作：**获取**

The base address of the vDSO mapping, or zero.  vDSO映射的基地址，或者为零。

 
### ZX_PROP_SOCKET_RX_THRESHOLD  ZX_PROP_SOCKET_RX_THRESHOLD 

*handle* type: **Socket**  *手柄*类型：**插座**

*value* type: `size_t`  *值*类型：`size_t`

Allowed operations: **get**, **set**  允许的操作：**获取**，**设置**

The size of the read threshold of a socket, in bytes. Setting this will assert ZX_SOCKET_READ_THRESHOLD if the amount of data that can be readis greater than or equal to the threshold. Setting this property to zerowill result in the deasserting of ZX_SOCKET_READ_THRESHOLD. 套接字的读取阈值大小，以字节为单位。如果可以读取的数据量大于或等于阈值，则设置此项将声明ZX_SOCKET_READ_THRESHOLD。将此属性设置为零将导致ZX_SOCKET_READ_THRESHOLD的无效。

 
### ZX_PROP_SOCKET_TX_THRESHOLD  ZX_PROP_SOCKET_TX_THRESHOLD 

*handle* type: **Socket**  *手柄*类型：**插座**

*value* type: `size_t`  *值*类型：`size_t`

Allowed operations: **get**, **set**  允许的操作：**获取**，**设置**

The size of the write threshold of a socket, in bytes. Setting this will assert ZX_SOCKET_WRITE_THRESHOLD if the amount of space available for writingis greater than or equal to the threshold. Setting this property to zerowill result in the deasserting of ZX_SOCKET_WRITE_THRESHOLD. Setting thewrite threshold after the peer has closed is an error, and results in aZX_ERR_PEER_CLOSED error being returned. 套接字的写阈值大小，以字节为单位。如果可用于写入的空间量大于或等于阈值，则设置此项将声明ZX_SOCKET_WRITE_THRESHOLD。将此属性设置为零将导致ZX_SOCKET_WRITE_THRESHOLD的无效。在对等方关闭后设置写阈值是错误的，并导致返回ZX_ERR_PEER_CLOSED错误。

 
### ZX_PROP_JOB_KILL_ON_OOM  ZX_PROP_JOB_KILL_ON_OOM 

*handle* type: **Job**  *手柄*类型：**工作**

*value* type: `size_t`  *值*类型：`size_t`

Allowed operations: **set**  允许的操作：**设置**

The value of 1 means the Job and its children will be terminated if the system finds itself in a system-wide low memory situation. Called with 0(which is the default) opts out the job from being terminated in thisscenario. 值1表示如果系统发现自己处于系统范围内的内存不足情况，则作业及其子项将被终止。调用0（这是默认值）可以使作业退出此方案。

 
### ZX_PROP_EXCEPTION_STATE  ZX_PROP_EXCEPTION_STATE 

*handle* type: **Exception**  *句柄*类型：**例外**

*value* type: `uint32_t`  *值*类型：`uint32_t`

Allowed operations: **get**, **set**  允许的操作：**获取**，**设置**

When set to `ZX_EXCEPTION_STATE_HANDLED`, closing the exception handle will finish exception processing and resume the underlying thread.`ZX_EXCEPTION_STATE_TRY_NEXT` will instead continue exception processing bytrying the next handler in order. 当设置为`ZX_EXCEPTION_STATE_HANDLED`时，关闭异常句柄将完成异常处理并恢复基础线程。`ZX_EXCEPTION_STATE_TRY_NEXT`将通过依次尝试下一个处理程序来继续异常处理。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have **ZX_RIGHT_GET_PROPERTY**.  *句柄*必须具有** ZX_RIGHT_GET_PROPERTY **。

If *property* is **ZX_PROP_PROCESS_DEBUG_ADDR**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS**.  如果* property *是** ZX_PROP_PROCESS_DEBUG_ADDR **，则* handle *必须是** ZX_OBJ_TYPE_PROCESS **类型。

If *property* is **ZX_PROP_PROCESS_BREAK_ON_LOAD**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS**.  如果* property *是** ZX_PROP_PROCESS_BREAK_ON_LOAD **，则* handle *必须是** ZX_OBJ_TYPE_PROCESS **类型。

If *property* is **ZX_PROP_PROCESS_VDSO_BASE_ADDRESS**, *handle* must be of type **ZX_OBJ_TYPE_PROCESS**.  如果* property *是** ZX_PROP_PROCESS_VDSO_BASE_ADDRESS **，则* handle *必须是** ZX_OBJ_TYPE_PROCESS **类型。

If *property* is **ZX_PROP_SOCKET_RX_THRESHOLD**, *handle* must be of type **ZX_OBJ_TYPE_SOCKET**.  如果* property *是** ZX_PROP_SOCKET_RX_THRESHOLD **，则* handle *必须是** ZX_OBJ_TYPE_SOCKET **类型。

If *property* is **ZX_PROP_SOCKET_TX_THRESHOLD**, *handle* must be of type **ZX_OBJ_TYPE_SOCKET**.  如果* property *是** ZX_PROP_SOCKET_TX_THRESHOLD **，则* handle *必须是** ZX_OBJ_TYPE_SOCKET **类型。

 
## RETURN VALUE  返回值 

`zx_object_get_property()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned. zx_object_get_property（）成功返回** ZX_OK **。如果发生故障，将返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**: *handle* is not a valid handle  ** ZX_ERR_BAD_HANDLE **：* handle *不是有效的句柄

**ZX_ERR_WRONG_TYPE**: *handle* is not an appropriate type for *property*  ** ZX_ERR_WRONG_TYPE **：*句柄*不适用于*属性*

**ZX_ERR_ACCESS_DENIED**: *handle* does not have the necessary rights for the operation ** ZX_ERR_ACCESS_DENIED **：*句柄*没有必要的操作权限

**ZX_ERR_INVALID_ARGS**: *value* is an invalid pointer  ** ZX_ERR_INVALID_ARGS **：* value *是无效的指针

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_BUFFER_TOO_SMALL**: *value_size* is too small for *property*  ** ZX_ERR_BUFFER_TOO_SMALL **：* value_size *对于* property *而言太小

**ZX_ERR_NOT_SUPPORTED**: *property* does not exist  ** ZX_ERR_NOT_SUPPORTED **：*属性*不存在

 
## SEE ALSO  也可以看看 

 
 - [`zx_object_set_property()`]  -[`zx_object_set_property（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

