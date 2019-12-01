 
# zx_pager_create_vmo  zx_pager_create_vmo 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Create a pager owned vmo.  创建一个寻呼机拥有的vmo。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_pager_create_vmo(zx_handle_t pager,
                                uint32_t options,
                                zx_handle_t port,
                                uint64_t key,
                                uint64_t size,
                                zx_handle_t* out);
```
 

 
## DESCRIPTION  描述 

Creates a VMO owned by a pager object. *size* will be rounded up to the next page size boundary, and *options* must be zero or **ZX_VMO_RESIZABLE**. 创建由寻呼机对象拥有的VMO。 * size *将四舍五入到下一个页面尺寸边界，并且* options *必须为零或** ZX_VMO_RESIZABLE **。

On success, the returned vmo has the same rights as a vmo created with [`zx_vmo_create()`], as well as having the same behavior with respect to **ZX_VMO_ZERO_CHILDREN**. Syscalls which operate on VMOsrequire an explicit flag to allow blocking IPC to the userspace pager service; beyond this, whetheror not a VMO is owned by a pager does not affect the semantics of syscalls. 成功后，返回的vmo拥有与使用[`zx_vmo_create（）`]创建的vmo相同的权限，并且具有与** ZX_VMO_ZERO_CHILDREN **相同​​的行为。在VMO上运行的系统调用需要一个显式标志，以允许将IPC阻止到用户空间寻呼机服务；除此之外，寻呼机是否拥有VMO都不会影响系统调用的语义。

TODO(stevend): Update differences after updates to cloning and decommit  TODO（stevend）：在更新克隆和取消提交后更新差异

Page requests will be delivered to *port* when certain conditions are met. Those packets will have *type* set to **ZX_PKT_TYPE_PAGE_REQUEST** and *key* set to the value provided to`zx_pager_create_vmo()`. The packet's union is of type `zx_packet_page_request_t`: 满足某些条件时，页面请求将传递到* port *。这些数据包的* type *设置为** ZX_PKT_TYPE_PAGE_REQUEST **，* key *设置为提供给zx_pager_create_vmo（）的值。数据包的并集类型为`zx_packet_page_request_t`：

```
typedef struct zx_packet_page_request {
    uint16_t command;
    uint16_t flags;
    uint32_t reserved0;
    uint64_t offset;
    uint64_t length;
    uint64_t reserved1;
} zx_packet_page_request_t;
```
 

*offset* and *length* are always page-aligned. The value of any bits in *flags* for which flags are not defined is unspecified - currently no flags are defined. The trigger and meaning ofthe packet depends on *command*, which can take one of the following values: *偏移*和*长度*总是页面对齐的。未指定* flags中* flags中任何未定义标志的位的值-当前未定义标志。数据包的触发和含义取决于* command *，该命令可以采用以下值之一：

**ZX_PAGER_VMO_READ**: Sent when an application accesses a non-resident page in a pager's VMO. The pager service should populate the range [offset, offset + length) in the registered vmo with[`zx_pager_supply_pages()`]. Supplying pages is an implicit positive acknowledgement of the request. ** ZX_PAGER_VMO_READ **：当应用程序访问寻呼机VMO中的非驻留页面时发送。寻呼机服务应使用[`zx_pager_supply_pages（）]填充已注册vmo中的范围[偏移，偏移+长度]。提供页面是对请求的隐式肯定确认。

**ZX_PAGER_VMO_COMPLETE**: Sent when no more pager requests will be sent for the corresponding VMO, either because of [`zx_pager_detach_vmo()`] or because no references to the VMO remain. ** ZX_PAGER_VMO_COMPLETE **：当由于[`zx_pager_detach_vmo（）]或因为不保留对VMO的引用而不再发送针对相应VMO的寻呼机请求时发送。

If *pager* is closed, then no more packets will be delivered to *port* (including no **ZX_PAGER_VMO_COMPLETE** message). Furthermore, all future accesses will behave as if[`zx_pager_detach_vmo()`] had been called. 如果* pager *关闭，则不会再有任何数据包传递到* port *（不包括** ZX_PAGER_VMO_COMPLETE **消息）。此外，所有将来的访问都将表现为已调用[`zx_pager_detach_vmo（）`]。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*pager* must be of type **ZX_OBJ_TYPE_PAGER**.  * pager *必须为** ZX_OBJ_TYPE_PAGER **类型。

*port* must be of type **ZX_OBJ_TYPE_PORT** and have **ZX_RIGHT_WRITE**.  *端口*必须为** ZX_OBJ_TYPE_PORT **类型，并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_pager_create_vmo()` returns ZX_OK on success, or one of the following error codes on failure.  zx_pager_create_vmo（）成功返回ZX_OK，失败则返回以下错误代码之一。

 
## ERRORS  错误 

**ZX_ERR_INVALID_ARGS** *out* is an invalid pointer or NULL, or *options* is any value other than 0 or **ZX_VMO_RESIZABLE**. ** ZX_ERR_INVALID_ARGS ** * out *是无效的指针或NULL，或者* options *是除0或** ZX_VMO_RESIZABLE **以外的任何值。

**ZX_ERR_BAD_HANDLE** *pager* or *port* is not a valid handle.  ** ZX_ERR_BAD_HANDLE ** * pager *或* port *不是有效的句柄。

**ZX_ERR_ACCESS_DENIED** *port* does not have **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *端口*没有** ZX_RIGHT_WRITE **。

**ZX_ERR_WRONG_TYPE** *pager* is not a pager handle or *port* is not a port handle.  ** ZX_ERR_WRONG_TYPE ** * pager *不是寻呼机句柄，或者* port *不是端口句柄。

**ZX_ERR_OUT_OF_RANGE** The requested size is larger than the maximum vmo size.  ** ZX_ERR_OUT_OF_RANGE **请求的大小大于最大vmo大小。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory.  ** ZX_ERR_NO_MEMORY **由于内存不足而失败。

 
## SEE ALSO  也可以看看 

 
 - [`zx_pager_detach_vmo()`]  -[`zx_pager_detach_vmo（）`]
 - [`zx_pager_supply_pages()`]  -[`zx_pager_supply_pages（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

