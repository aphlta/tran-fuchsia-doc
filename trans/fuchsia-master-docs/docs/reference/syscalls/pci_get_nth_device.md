 
# zx_pci_get_nth_device  zx_pci_get_nth_device 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_pci_get_nth_device(zx_handle_t handle,
                                  uint32_t index,
                                  zx_pcie_device_info_t* out_info,
                                  zx_handle_t* out_handle);
```
 

 
## DESCRIPTION  描述 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must have resource kind **ZX_RSRC_KIND_ROOT**.  *句柄*必须具有资源种类** ZX_RSRC_KIND_ROOT **。

 
## RETURN VALUE  返回值 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## ERRORS  错误 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## SEE ALSO  也可以看看 

 

