 
# zx_debug_send_command  zx_debug_send_command 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_debug_send_command(zx_handle_t resource,
                                  const char* buffer,
                                  size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

To use the `zx_debug_send_command()` function, you must specify `kernel.enable-debugging-syscalls=true` on the kernel command line. Otherwise,the function returns **ZX_ERR_NOT_SUPPORTED**. 要使用`zx_debug_send_command（）`函数，必须在内核命令行上指定`kernel.enable-debugging-syscalls = true`。否则，该函数返回** ZX_ERR_NOT_SUPPORTED **。

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*resource* must have resource kind **ZX_RSRC_KIND_ROOT**.  * resource *必须具有资源类型** ZX_RSRC_KIND_ROOT **。

 
## RETURN VALUE  返回值 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## ERRORS  错误 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## SEE ALSO  也可以看看 

 

