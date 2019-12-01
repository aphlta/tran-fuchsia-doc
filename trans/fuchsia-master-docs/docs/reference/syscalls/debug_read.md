 
# zx_debug_read  zx_debug_read 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_debug_read(zx_handle_t handle,
                          char* buffer,
                          size_t buffer_size,
                          size_t* actual);
```
 

 
## DESCRIPTION  描述 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

To use the `zx_debug_read()` function, you must specify `kernel.enable-debugging-syscalls=true` on the kernel command line. Otherwise,the function returns **ZX_ERR_NOT_SUPPORTED**. 要使用`zx_debug_read（）`函数，必须在内核命令行上指定`kernel.enable-debugging-syscalls = true`。否则，该函数返回** ZX_ERR_NOT_SUPPORTED **。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have resource kind **ZX_RSRC_KIND_ROOT**.  *句柄*必须具有资源种类** ZX_RSRC_KIND_ROOT **。

 
## RETURN VALUE  返回值 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## ERRORS  错误 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

**ZX_ERR_NOT_SUPPORTED**  `kernel.enable-debugging-syscalls` is not set to `true` on the kernel command line. ** ZX_ERR_NOT_SUPPORTED **`kernel.enable-debugging-syscalls`在内核命令行上未设置为`true`。

 
## SEE ALSO  也可以看看 

 

