 
# zx_system_mexec  zx_system_mexec 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Soft reboot the system with a new kernel and bootimage.  使用新的内核和引导映像软重启系统。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_system_mexec(zx_handle_t resource,
                            zx_handle_t kernel_vmo,
                            zx_handle_t bootimage_vmo);
```
 

 
## DESCRIPTION  描述 

`zx_system_mexec()` accepts two vmo handles: *kernel_vmo* should contain a kernel image and *bootimage_vmo* should contain an initrd whose address shallbe passed to the new kernel as a kernel argument. zx_system_mexec（）接受两个vmo句柄：* kernel_vmo *应包含内核映像，而* bootimage_vmo *应包含initrd，其地址应作为内核参数传递给新内核。

To supplant the running kernel, a *resource* of **ZX_RSRC_KIND_ROOT** must be supplied. 要取代正在运行的内核，必须提供*资源* ** ZX_RSRC_KIND_ROOT **。

Upon success, `zx_system_mexec()` shall supplant the currently running kernel image with the kernel image contained within *kernel_vmo*, load the ramdiskcontained within *bootimage_vmo* to a location in physical memory and branchdirectly into the new kernel while providing the address of the loaded initrdto the new kernel. 成功后，`zx_system_mexec（）`将用* kernel_vmo *中包含的内核映像取代当前正在运行的内核映像，将* bootimage_vmo *中包含的ramdisk加载到物理内存中的位置，并直接分支到新内核中，同时提供内核的地址。将initrd加载到新内核。

To use the `zx_system_mexec()` function, you must specify `kernel.enable-debugging-syscalls=true` on the kernel command line. Otherwise,the function returns **ZX_ERR_NOT_SUPPORTED**. 要使用zx_system_mexec（）函数，必须在内核命令行上指定kernel.enable-debugging-syscalls = true。否则，该函数返回** ZX_ERR_NOT_SUPPORTED **。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*resource* must have resource kind **ZX_RSRC_KIND_ROOT**.  * resource *必须具有资源类型** ZX_RSRC_KIND_ROOT **。

*kernel_vmo* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_READ**.  * kernel_vmo *必须为** ZX_OBJ_TYPE_VMO **类型，且必须为** ZX_RIGHT_READ **。

*bootimage_vmo* must be of type **ZX_OBJ_TYPE_VMO** and have **ZX_RIGHT_READ**.  * bootimage_vmo *必须为** ZX_OBJ_TYPE_VMO **类型，并且必须为** ZX_RIGHT_READ **。

 
## RETURN VALUE  返回值 

`zx_system_mexec()` shall not return upon success.  zx_system_mexec（）成功后不会返回。

**ZX_ERR_NOT_SUPPORTED**  `kernel.enable-debugging-syscalls` is not set to `true` on the kernel command line. ** ZX_ERR_NOT_SUPPORTED **`kernel.enable-debugging-syscalls`在内核命令行上未设置为`true`。

 
## SEE ALSO  也可以看看 

 
 - [`zx_system_mexec_payload_get()`]  -[`zx_system_mexec_payload_get（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

