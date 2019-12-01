 
# zx_system_mexec_payload_get  zx_system_mexec_payload_get 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Return a ZBI containing ZBI entries necessary to boot this system.  返回包含启动该系统所需的ZBI条目的ZBI。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_system_mexec_payload_get(zx_handle_t resource,
                                        void* buffer,
                                        size_t buffer_size);
```
 

 
## DESCRIPTION  描述 

`zx_system_mexec_payload_get()` accepts a resource handle and a pointer/length corresponding to an output buffer and fills the buffer with anincomplete ZBI containing a sequence of entries that should be appended to aZBI before passing that image to [`zx_system_mexec()`]. zx_system_mexec_payload_get（）接受资源句柄和对应于输出缓冲区的指针/长度，并用不完整的ZBI填充缓冲区，该ZBI包含应在将图像传递到[`zx_system_mexec（）]之前附加到aZBI的条目序列。

*resource* must be of type **ZX_RSRC_KIND_ROOT**.  *资源*必须为** ZX_RSRC_KIND_ROOT **类型。

*buffer* and *buffer_size* must point to a buffer that is no longer than 16KiB.  * buffer *和* buffer_size *必须指向不超过16KiB的缓冲区。

To use the `zx_system_mexec_payload_get()` function, you must specify `kernel.enable-debugging-syscalls=true` on the kernel command line. Otherwise,the function returns **ZX_ERR_NOT_SUPPORTED**. 要使用`zx_system_mexec_payload_get（）`函数，必须在内核命令行上指定`kernel.enable-debugging-syscalls = true`。否则，该函数返回** ZX_ERR_NOT_SUPPORTED **。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*resource* must have resource kind **ZX_RSRC_KIND_ROOT**.  * resource *必须具有资源类型** ZX_RSRC_KIND_ROOT **。

 
## RETURN VALUE  返回值 

`zx_system_mexec_payload_get()` returns **ZX_OK** on success.  zx_system_mexec_payload_get（）成功返回** ZX_OK **。

**ZX_ERR_NOT_SUPPORTED**  `kernel.enable-debugging-syscalls` is not set to `true` on the kernel command line. ** ZX_ERR_NOT_SUPPORTED **`kernel.enable-debugging-syscalls`在内核命令行上未设置为`true`。

 
## SEE ALSO  也可以看看 

 
 - [`zx_system_mexec()`]  -[`zx_system_mexec（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

