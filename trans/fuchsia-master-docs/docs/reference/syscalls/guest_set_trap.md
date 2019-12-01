 
# zx_guest_set_trap  zx_guest_set_trap 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Sets a trap within a guest.  在访客中设置陷阱。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_guest_set_trap(zx_handle_t handle,
                              uint32_t kind,
                              zx_vaddr_t addr,
                              size_t size,
                              zx_handle_t port_handle,
                              uint64_t key);
```
 

 
## DESCRIPTION  描述 

`zx_guest_set_trap()` sets a trap within a guest, which generates a packet when there is an access by a VCPU within the address range defined by *addr* and*size*, within the address space defined by *kind*. zx_guest_set_trap（）设置来宾系统中的陷阱，当VCPU在* kind *定义的地址范围内，在* addr *和* size *定义的地址范围内VCPU进行访问时，该陷阱将生成一个数据包。

*kind* may be either **ZX_GUEST_TRAP_BELL**, **ZX_GUEST_TRAP_MEM**, or **ZX_GUEST_TRAP_IO**. If **ZX_GUEST_TRAP_BELL** or **ZX_GUEST_TRAP_MEM** isspecified, then *addr* and *size* must both be page-aligned.**ZX_GUEST_TRAP_BELL** is an asynchronous trap, and both **ZX_GUEST_TRAP_MEM**and **ZX_GUEST_TRAP_IO** are synchronous traps. *种类*可以是** ZX_GUEST_TRAP_BELL **，** ZX_GUEST_TRAP_MEM **或** ZX_GUEST_TRAP_IO **。如果指定了** ZX_GUEST_TRAP_BELL **或** ZX_GUEST_TRAP_MEM **，则* addr *和* size *都必须是页面对齐的。 **是同步陷阱。

Packets for synchronous traps will be delivered through [`zx_vcpu_resume()`] and packets for asynchronous traps will be delivered through *port_handle*. 同步陷阱的数据包将通过[`zx_vcpu_resume（）]传递，异步陷阱的数据包将通过* port_handle *传递。

*port_handle* must be **ZX_HANDLE_INVALID** for synchronous traps. For asynchronous traps *port_handle* must be valid and a packet for the trap will bedelivered through *port_handle* each time the trap is triggered. A fixed numberof packets are pre-allocated per trap. If all the packets are exhausted,execution of the VCPU that caused the trap will be paused. When at least onepacket is dequeued, execution of the VCPU will resume. To dequeue a packet from*port_handle*, use [`zx_port_wait()`]. Multiple threads may use[`zx_port_wait()`] to dequeue packets, enabling the use of a thread pool tohandle traps. 对于同步陷阱，“ port_handle *”必须为“ ZX_HANDLE_INVALID **”。对于异步陷阱* port_handle *必须有效，并且每次触发陷阱时都会通过* port_handle *传递陷阱的数据包。每个陷阱会预先分配固定数量的数据包。如果所有数据包都已用尽，则导致陷阱的VCPU的执行将暂停。当至少一个数据包出队后，VCPU的执行将恢复。要从* port_handle *中取出数据包，请使用[`zx_port_wait（）`]。多个线程可以使用[`zx_port_wait（）`]使数据包出队，从而允许使用线程池来处理陷阱。

*key* is used to set the key field within `zx_port_packet_t`, and can be used to distinguish between packets for different traps. * key *用于设置`zx_port_packet_t`中的key字段，并且可以用于区分不同陷阱的数据包。

 

**ZX_GUEST_TRAP_BELL** is a type of trap that defines a door-bell. If there is an access to the memory region specified by the trap, then a packet is generatedthat does not fetch the instruction associated with the access. The packet willthen be delivered asynchronously via *port_handle*. ** ZX_GUEST_TRAP_BELL **是一种定义门铃的陷阱。如果存在对陷阱指定的存储区的访问，则会生成一个数据包，该数据包不提取与该访问相关的指令。然后，将通过* port_handle *异步传送数据包。

To identify what *kind* of trap generated a packet, use **ZX_PKT_TYPE_GUEST_MEM**, **ZX_PKT_TYPE_GUEST_IO**, **ZX_PKT_TYPE_GUEST_BELL**,and **ZX_PKT_TYPE_GUEST_VCPU**. **ZX_PKT_TYPE_GUEST_VCPU** is a special packet,not caused by a trap, that indicates that the guest requested to start anadditional VCPU. 要确定是什么类型的陷阱生成了数据包，请使用ZX_PKT_TYPE_GUEST_MEM **，ZX_PKT_TYPE_GUEST_IO **，ZX_PKT_TYPE_GUEST_BELL **和ZX_PKT_TYPE_GUEST_VCPU **。 ** ZX_PKT_TYPE_GUEST_VCPU **是一个特殊数据包，不是由陷阱引起的，它指示来宾已请求启动其他VCPU。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

*handle* must be of type **ZX_OBJ_TYPE_GUEST** and have **ZX_RIGHT_WRITE**.  *句柄*必须为** ZX_OBJ_TYPE_GUEST **类型，并具有** ZX_RIGHT_WRITE **。

*port_handle* must be of type **ZX_OBJ_TYPE_PORT** and have **ZX_RIGHT_WRITE**.  * port_handle *必须为** ZX_OBJ_TYPE_PORT **类型，且必须为** ZX_RIGHT_WRITE **。

 
## RETURN VALUE  返回值 

`zx_guest_set_trap()` returns **ZX_OK** on success. On failure, an error value is returned. `zx_guest_set_trap（）`成功返回** ZX_OK **。失败时，将返回错误值。

 
## ERRORS  错误 

**ZX_ERR_ACCESS_DENIED** *handle* or *port_handle* do not have the **ZX_RIGHT_WRITE** right. ** ZX_ERR_ACCESS_DENIED ** * handle *或* port_handle *没有** ZX_RIGHT_WRITE **权限。

**ZX_ERR_ALREADY_EXISTS** A trap with the same *kind* and *addr* already exists.  ** ZX_ERR_ALREADY_EXISTS **具有相同* kind *和* addr *的陷阱已存在。

**ZX_ERR_BAD_HANDLE** *handle* or *port_handle* are invalid handles.  ** ZX_ERR_BAD_HANDLE ** * handle *或* port_handle *是无效的句柄。

**ZX_ERR_INVALID_ARGS** *kind* is not a valid address space, *addr* or *size* do not meet the requirements of *kind*, *size* is 0, or **ZX_GUEST_TRAP_MEM** wasspecified with a *port_handle*. ** ZX_ERR_INVALID_ARGS ** * kind *不是有效的地址空间，* addr *或* size *不满足* kind *的要求，* size *为0，或者** ZX_GUEST_TRAP_MEM **由* port_handle *指定。

**ZX_ERR_NO_MEMORY**  Failure due to lack of memory. There is no good way for userspace to handle this (unlikely) error.In a future build this error will no longer occur. ** ZX_ERR_NO_MEMORY **由于内存不足而失败。用户空间没有很好的方法来处理此（不太可能）错误。在将来的版本中，将不再发生此错误。

**ZX_ERR_OUT_OF_RANGE** The region specified by *addr* and *size* is outside of of the valid bounds of the address space *kind*. ** ZX_ERR_OUT_OF_RANGE **由* addr *和* size *指定的区域在地址空间* kind *的有效范围之外。

**ZX_ERR_WRONG_TYPE** *handle* is not a handle to a guest, or *port_handle* is not a handle to a port. ** ZX_ERR_WRONG_TYPE ** * handle *不是来宾的句柄，或者* port_handle *不是端口的句柄。

 
## NOTES  笔记 

**ZX_GUEST_TRAP_BELL** shares the same address space as **ZX_GUEST_TRAP_MEM**.  ** ZX_GUEST_TRAP_BELL **与** ZX_GUEST_TRAP_MEM **共享相同的地址空间。

On x86-64, if *kind* is **ZX_GUEST_TRAP_BELL** or **ZX_GUEST_TRAP_MEM** and *addr* is the address of the local APIC, then *size* must be equivalent to the size ofa page. This is due to a special page being mapped when a trap is requested at theaddress of the local APIC. This allows us to take advantage of hardwareacceleration when available. 在x86-64上，如果* kind *是** ZX_GUEST_TRAP_BELL **或** ZX_GUEST_TRAP_MEM **且* addr *是本地APIC的地址，则* size *必须等于页面的大小。这是由于在本地APIC的地址上请求陷阱时映射了特殊页面。这使我们可以利用可用的硬件加速功能。

 
## SEE ALSO  也可以看看 

 
 - [`zx_guest_create()`]  -[`zx_guest_create（）`]
 - [`zx_port_create()`]  -[`zx_port_create（）`]
 - [`zx_port_wait()`]  -[`zx_port_wait（）`]
 - [`zx_vcpu_create()`]  -[`zx_vcpu_create（）`]
 - [`zx_vcpu_interrupt()`]  -[`zx_vcpu_interrupt（）`]
 - [`zx_vcpu_read_state()`]  -[`zx_vcpu_read_state（）`]
 - [`zx_vcpu_resume()`]  -[`zx_vcpu_resume（）`]
 - [`zx_vcpu_write_state()`]  -[`zx_vcpu_write_state（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

