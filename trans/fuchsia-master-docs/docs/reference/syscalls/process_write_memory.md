 
# zx_process_write_memory  zx_process_write_memory 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Write into the given process's address space.  写入给定进程的地址空间。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_process_write_memory(zx_handle_t handle,
                                    zx_vaddr_t vaddr,
                                    const void* buffer,
                                    size_t buffer_size,
                                    size_t* actual);
```
 

 
## DESCRIPTION  描述 

`zx_process_write_memory()` attempts to write memory of the specified process.  zx_process_write_memory（）尝试写入指定进程的内存。

This function will eventually be replaced with something vmo-centric.  该功能最终将被以vmo为中心的东西所取代。

*vaddr* the address of the block of memory to write.  * vaddr *要写入的内存块的地址。

*buffer* pointer to a user buffer containing the bytes to write.  * buffer *指向包含要写入字节的用户缓冲区的指针。

*buffer_size* number of bytes to attempt to write. *buffer* buffer must be large enough for at least this many bytes. *buffer_size* must be greater thanzero and less than or equal to 64MB. * buffer_size *尝试写入的字节数。 * buffer *缓冲区必须足够大，至少可以容纳这么多字节。 * buffer_size *必须大于零且小于或等于64MB。

*actual_size* the actual number of bytes written is stored here. Less bytes than requested may be returned if *vaddr*+*buffer_size* extends beyond thememory mapped in the process. * actual_size *实际写入的字节数存储在此处。如果* vaddr * + * buffer_size *超出了进程中映射的主题，则返回的字节数可能少于请求的字节数。

To use the `zx_process_write_memory()` function, you must specify `kernel.enable-debugging-syscalls=true` on the kernel command line. Otherwise,the function returns **ZX_ERR_NOT_SUPPORTED**. 要使用zx_process_write_memory（）函数，必须在内核命令行上指定kernel.enable-debugging-syscalls = true。否则，该函数返回** ZX_ERR_NOT_SUPPORTED **。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_PROCESS** and have **ZX_RIGHT_WRITE**.  *句柄*的类型必须为** ZX_OBJ_TYPE_PROCESS **且具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_process_write_memory()` returns **ZX_OK** on success. In the event of failure, a negative error value is returned, and the number ofbytes written to *buffer* is undefined. zx_process_write_memory（）成功返回** ZX_OK **。发生故障时，将返回负错误值，并且未定义写入* buffer *的字节数。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED**  *handle* does not have the **ZX_RIGHT_WRITE** right or the address range to write falls into a protected area like the vDSO. ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WRITE **权限，或者要写入的地址范围属于vDSO之类的受保护区域。

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_BAD_STATE**  the process's memory is not accessible (e.g., the process is being terminated),or the requested memory is not cacheable. ** ZX_ERR_BAD_STATE **进程的内存不可访问（例如，进程正在终止），或者请求的内存不可缓存。

**ZX_ERR_INVALID_ARGS**  *buffer* is an invalid pointer or NULL, or *buffer_size* is zero or greater than 64MB. ** ZX_ERR_INVALID_ARGS ** * buffer *是无效的指针或NULL，或者* buffer_size *为零或大于64MB。

**ZX_ERR_NO_MEMORY**  the process does not have any memory at the requested address. ** ZX_ERR_NO_MEMORY **进程在请求的地址处没有任何内存。

**ZX_ERR_NOT_SUPPORTED**  `kernel.enable-debugging-syscalls` is not set to `true` on the kernel command line. ** ZX_ERR_NOT_SUPPORTED **`kernel.enable-debugging-syscalls`在内核命令行上未设置为`true`。

**ZX_ERR_WRONG_TYPE**  *handle* is not a process handle.  ** ZX_ERR_WRONG_TYPE ** *句柄*不是进程句柄。

 
## SEE ALSO  也可以看看 

 
 - [`zx_process_read_memory()`]  -[`zx_process_read_memory（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

