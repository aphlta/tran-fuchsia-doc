 
# zx_port_queue  zx_port_queue 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Queue a packet to a port.  将数据包排队到端口。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>
#include <zircon/syscalls/port.h>

zx_status_t zx_port_queue(zx_handle_t handle, const zx_port_packet_t* packet);
```
 

 
## DESCRIPTION  描述 

`zx_port_queue()` queues a *packet* to the port specified by *handle*. zx_port_queue（）将* packet *排队到* handle *指定的端口上。

```
typedef struct zx_port_packet {
    uint64_t key;
    uint32_t type;
    zx_status_t status;
    union {
        zx_packet_user_t user;
        zx_packet_signal_t signal;
    };
} zx_port_packet_t;

```
 

In *packet* *type* should be **ZX_PKT_TYPE_USER** and only the **user** union element is considered valid: 在* packet *中，* type *应该是** ZX_PKT_TYPE_USER **，并且只有** user **联合元素被认为是有效的：

```
typedef union zx_packet_user {
    uint64_t u64[4];
    uint32_t u32[8];
    uint16_t u16[16];
    uint8_t   c8[32];
} zx_packet_user_t;

```
 

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_PORT** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_PORT **类型并具有** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_port_queue()` returns **ZX_OK** on successful queue of a packet.  zx_port_queue（）在数据包成功排队时返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BAD_HANDLE** *handle* isn't a valid handle  ** ZX_ERR_BAD_HANDLE ** *句柄*不是有效的句柄

**ZX_ERR_INVALID_ARGS** *packet* is an invalid pointer.  ** ZX_ERR_INVALID_ARGS ** *数据包*是无效的指针。

**ZX_ERR_WRONG_TYPE** *handle* is not a port handle.  ** ZX_ERR_WRONG_TYPE ** * handle *不是端口句柄。

**ZX_ERR_ACCESS_DENIED** *handle* does not have **ZX_RIGHT_WRITE**.  ** ZX_ERR_ACCESS_DENIED ** *句柄*没有** ZX_RIGHT_WRITE **。

**ZX_ERR_SHOULD_WAIT** the port has too many pending packets. Once a thread has drained some packets a new `zx_port_queue()` call will likely succeed. ** ZX_ERR_SHOULD_WAIT **端口有太多待处理数据包。一旦线程耗尽了一些数据包，新的“ zx_port_queue（）”调用将可能成功。

 
## NOTES  笔记 

The queue is drained by calling [`zx_port_wait()`].  通过调用[`zx_port_wait（）`]耗尽队列。

 

 
## SEE ALSO  也可以看看 

 
 - [`zx_port_create()`]  -[`zx_port_create（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

