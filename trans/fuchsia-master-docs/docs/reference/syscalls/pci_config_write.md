 
# zx_pci_config_write  zx_pci_config_write 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_pci_config_write(zx_handle_t handle,
                                uint16_t offset,
                                size_t width,
                                uint32_t val);
```
 

 
## DESCRIPTION  描述 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_PCI_DEVICE** and have **ZX_RIGHT_READ** and have **ZX_RIGHT_WRITE**.  *句柄*的类型必须为** ZX_OBJ_TYPE_PCI_DEVICE **且具有** ZX_RIGHT_READ **和** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## ERRORS  错误 

TODO(fxbug.dev/32938)  待办事项（fxbug.dev/32938）

 
## SEE ALSO  也可以看看 

 

