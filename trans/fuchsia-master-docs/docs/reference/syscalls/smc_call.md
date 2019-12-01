 
# zx_smc_call  zx_smc_call 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Make Secure Monitor Call (SMC) from user space.  从用户空间进行安全监视器呼叫（SMC）。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>
#include <zircon/syscalls/smc.h>

zx_status_t zx_smc_call(zx_handle_t handle,
                        const zx_smc_parameters_t* parameters,
                        zx_smc_result_t* out_smc_result);
```
 

 
## DESCRIPTION  描述 

`zx_smc_call()` makes a Secure Monitor Call (SMC) from user space. It supports the ARM SMC Calling Convention using the `zx_smc_parameters_t` input parameter and `zx_smc_result_t` output parameter.The input *handle* must be a resource object with sufficient privileges in order to be executed. zx_smc_call（）从用户空间发出安全监视器调用（SMC）。它使用输入参数zx_smc_parameters_t和输出参数zx_smc_result_t支持ARM SMC调用约定。输入* handle *必须是具有足够特权的资源对象才能执行。

The majority of the parameters are opaque from `zx_smc_call()` perspective because they are dependent upon the *func_id*. The *func_id* informs the Secure Monitor the service and functionto be invoked. The *client_id* is an optional field intended for secure software to track andindex the calling client OS. The *secure_os_id* is an optional field intended for use when thereare multiple secure operating systems at S-EL1, so that the caller may specify the intendedsecure OS. 从zx_smc_call（）角度来看，大多数参数都是不透明的，因为它们取决于* func_id *。 * func_id *通知安全监视器要调用的服务和功能。 * client_id *是一个可选字段，用于安全软件来跟踪和索引调用方客户端操作系统。 * secure_os_id *是一个可选字段，打算在S-EL1上有多个安全操作系统时使用，以便调用方可以指定所需的安全OS。

More information is available in the [ARM SMC Calling Convention documentation]( http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.den0028b/index.html). 有关更多信息，请参见[ARM SMC调用约定文档]（http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.den0028b/index.html）。

 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_smc_call()` returns **ZX_OK** if *handle* has sufficient privilege. The return value of the smc call is returned via **out_smc_result** on success. In the event offailure, a negative error value is returned. 如果* handle *具有足够的特权，`zx_smc_call（）`将返回** ZX_OK **。成功时，通过** out_smc_result **返回smc调用的返回值。如果发生故障，则返回负错误值。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a resource handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是资源句柄。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have sufficient privileges.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有足够的特权。

**ZX_ERR_NOT_SUPPORTED**  smc_call is not supported on this system.  ** ZX_ERR_NOT_SUPPORTED **此系统不支持smc_call。

