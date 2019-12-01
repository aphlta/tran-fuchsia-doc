 
# zx_fifo_write  zx_fifo_write 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Write data to a fifo.  将数据写入FIFO。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_fifo_write(zx_handle_t handle,
                          size_t elem_size,
                          const void* data,
                          size_t count,
                          size_t* actual_count);
```
 

 
## DESCRIPTION  描述 

`zx_fifo_write()` attempts to write up to *count* elements (`count * elem_size` bytes) from *data* to the fifo specified by *handle*. zx_fifo_write（）尝试将最多* count *个元素（“ count * elem_size”个字节）从* data *写入到* handle *指定的fifo。

Fewer elements may be written than requested if there is insufficient room in the fifo to contain all of them. The number ofelements actually written is returned via *actual_count*. 如果fifo中没有足够的空间容纳所有元素，则可以写入少于请求的元素。实际写入的元素数量通过* actual_count *返回。

The element size specified by *elem_size* must match the element size that was passed into [`zx_fifo_create()`]. * elem_size *指定的元素大小必须与传递给[`zx_fifo_create（）`]的元素大小匹配。

*actual_count* is allowed to be NULL. This is useful when writing a single element: if *count* is 1 and `zx_fifo_write()` returns **ZX_OK**,*actual_count* is guaranteed to be 1 and thus can be safely ignored. * actual_count *允许为NULL。这在编写单个元素时很有用：如果* count *为1并且`zx_fifo_write（）`返回** ZX_OK **，则* actual_count *保证为1，因此可以安全地忽略。

It is not legal to write zero elements.  写零元素是不合法的。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_FIFO** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_FIFO **类型并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_fifo_write()` returns **ZX_OK** on success, and returns the number of elements written (at least one) via *actual_count*. zx_fifo_write（）成功返回** ZX_OK **，并通过* actual_count *返回写入的元素数量（至少一个）。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE**  *handle* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄。

**ZX_ERR_WRONG_TYPE**  *handle* is not a fifo handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是fifo句柄。

**ZX_ERR_INVALID_ARGS**  *data* is an invalid pointer or *actual_count* is an invalid pointer. ** ZX_ERR_INVALID_ARGS ** * data *是无效的指针或* actual_count *是无效的指针。

**ZX_ERR_OUT_OF_RANGE**  *count* is zero or *elem_size* is not equal to the element size of the fifo. ** ZX_ERR_OUT_OF_RANGE ** * count *为零或* elem_size *不等于fifo的元素大小。

**ZX_ERR_ACCESS_DENIED**  *handle* does not have **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WRITE **。

**ZX_ERR_PEER_CLOSED**  The other side of the fifo is closed.  ** ZX_ERR_PEER_CLOSED ** FIFO的另一侧已关闭。

**ZX_ERR_SHOULD_WAIT**  The fifo is full.  ** ZX_ERR_SHOULD_WAIT ** FIFO已满。

 

 
## SEE ALSO  也可以看看 

 
 - [`zx_fifo_create()`]  -[`zx_fifo_create（）`]
 - [`zx_fifo_read()`]  -[`zx_fifo_read（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

