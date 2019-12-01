 
# zx_fifo_create  zx_fifo_create 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a fifo.  创建一个fifo。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_fifo_create(size_t elem_count,
                           size_t elem_size,
                           uint32_t options,
                           zx_handle_t* out0,
                           zx_handle_t* out1);
```
 

 
## DESCRIPTION  描述 

`zx_fifo_create()` creates a fifo, which is actually a pair of fifos of *elem_count* entries of *elem_size* bytes.  Two endpoints arereturned.  Writing to one endpoint enqueues an element into the fifothat the opposing endpoint reads from. zx_fifo_create（）创建一个fifo，它实际上是一对* elem_size *个字节的* elem_count *个条目的fifo。返回两个端点。写入一个端点会使一个元素进入相反端点读取的对象。

Fifos are intended to be the control plane for shared memory transports. Their read and write operations are more efficient than *sockets* or*channels*, but there are severe restrictions on the size of elementsand buffers. Fifos旨在成为共享内存传输的控制平面。它们的读写操作比* socket *或* channels *更有效，但是对元素和缓冲区的大小有严格的限制。

The *elem_count* must be a power of two.  The total size of each fifo (`elem_count * elem_size`) may not exceed 4096 bytes. * elem_count *必须为2的幂。每个fifo的总大小（“ elem_count * elem_size”）不得超过4096个字节。

The *options* argument must be 0.  * options *参数必须为0。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_fifo_create()` returns **ZX_OK** on success. In the event of failure, one of the following values is returned. zx_fifo_create（）成功返回** ZX_OK **。发生故障时，将返回以下值之一。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS**  *out0* or *out1* is an invalid pointer or NULL or *options* is any value other than 0. ** ZX_ERR_INVALID_ARGS ** * out0 *或* out1 *是无效的指针，或者NULL或* options *是除0以外的任何值。

**ZX_ERR_OUT_OF_RANGE**  *elem_count* or *elem_size* is zero, or *elem_count* is not a power of two, or *elem_count* * *elem_size* is greater than 4096. ** ZX ERR_OUT_OF_RANGE ** * elem_count *或* elem_size *为零，或者* elem_count *不是2的幂，或者* elem_count * * * elem_size *大于4096。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

 

 
## SEE ALSO  也可以看看 

 
 - [`zx_fifo_read()`]  -[`zx_fifo_read（）`]
 - [`zx_fifo_write()`]  -[`zx_fifo_write（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

