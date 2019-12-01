 
# Pinned Memory Token  固定内存令牌 

 
## NAME  名称 

pinned_memory_token - Representation of a device DMA grant  pinned_memory_token-设备DMA授予的表示

 
## SYNOPSIS  概要 

Pinned Memory Tokens (PMTs) represent an outstanding access grant to a device for performing DMA. 固定内存令牌（PMT）表示对设备的未完成访问授权，以执行DMA。

 
## DESCRIPTION  描述 

PMTs are obtained by [pinning memory with a BTI object](/docs/reference/syscalls/bti_pin.md). It is valid for the device associated with the BTI to access the memory representedby the PMT for as long as the PMT object is around.  When the PMT object isdestroyed, either via [`zx_handle_close()`], [`zx_pmt_unpin()`], or processtermination, access to the represented memory becomes illegal (this isenforced by hardware on systems with the capability to do so, such as IOMMUs). 通过[使用BTI对象固定内存]（/ docs / reference / syscalls / bti_pin.md）获得PMT。只要PMT对象存在，与BTI关联的设备就可以访问由PMT表示的内存。当通过[`zx_handle_close（）`，[`zx_pmt_unpin（）`]或进程终止销毁PMT对象时，对所表示内存的访问将变得非法（这由具有此功能的系统上的硬件强制执行） IOMMU）。

If a PMT object is destroyed by means other than [`zx_pmt_unpin()`], the underlying memory is *quarantined*.  See[bus_transaction_initiator](bus_transaction_initiator.md) for more details. 如果PMT对象不是通过[`zx_pmt_unpin（）`]销毁的，则基础内存将被“隔离”。有关更多详细信息，请参见[bus_transaction_initiator]（bus_transaction_initiator.md）。

 
## SEE ALSO  也可以看看 

 
 - [bus_transaction_initiator](bus_transaction_initiator.md) - Bus Transaction Initiators  -[bus_transaction_initiator]（bus_transaction_initiator.md）-公交交易发起者

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_bti_pin()`] - pin memory and grant access to it to the BTI  -[`zx_bti_pin（）`]-引脚存储器并将其访问权授予BTI
 - [`zx_pmt_unpin()`] - revoke access and unpin memory  -[`zx_pmt_unpin（）`]-撤消访问权限并取消固定内存

