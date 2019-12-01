 
# zx_mtrace_control  zx_mtrace_control 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_mtrace_control(zx_handle_t handle,
                              uint32_t kind,
                              uint32_t action,
                              uint32_t options,
                              void* ptr,
                              size_t ptr_size);
```
 

 
## DESCRIPTION  描述 

To use the `zx_mtrace_control()` function, you must specify `kernel.enable-debugging-syscalls=true` on the kernel command line. Otherwise,the function returns **ZX_ERR_NOT_SUPPORTED**. 要使用zx_mtrace_control（）函数，必须在内核命令行上指定kernel.enable-debugging-syscalls = true。否则，该函数返回** ZX_ERR_NOT_SUPPORTED **。

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have resource kind **ZX_RSRC_KIND_ROOT**.  *句柄*必须具有资源种类** ZX_RSRC_KIND_ROOT **。

 
## RETURN VALUE  返回值 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## ERRORS  错误 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## SEE ALSO  也可以看看 

 

