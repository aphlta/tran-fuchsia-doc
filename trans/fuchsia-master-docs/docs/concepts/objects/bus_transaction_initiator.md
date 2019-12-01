 
# Bus Transaction Initiator  公交交易发起人 

 
## NAME  名称 

bus_transaction_initiator - DMA configuration capability  bus_transaction_initiator-DMA配置功能

 
## SYNOPSIS  概要 

Bus Transaction Initiators (BTIs) represent the bus mastering/DMA capability of a device, and can be used for granting a device access to memory. 总线事务启动器（BTI）表示设备的总线主控/ DMA功能，可用于授予设备对内存的访问权限。

 
## DESCRIPTION  描述 

Device drivers are provided one BTI for each bus transaction ID each of its devices can use.  A bus transaction ID in this context is a hardware transactionidentifier that may be used by an IOMMU (e.g. PCI addresses on Intel's IOMMUand StreamIDs on ARM's SMMU). 为设备驱动程序提供了每个设备可以使用的每个总线事务ID一个BTI。在这种情况下，总线事务ID是IOMMU可以使用的硬件事务标识符（例如Intel的IOMMU上的PCI地址和ARM的SMMU上的StreamID）。

A BTI can be used to pin memory used in a Virtual Memory Object (VMO). If a caller pins memory from a VMO, they are given device-physical addressesthat can be used to issue memory transactions to the VMO (provided thetransaction has the correct bus transaction ID).  If transactions affectingthese addresses are issued with a different transaction ID, the transactionmay fail and the issuing device may need a reset in order to continue functioning. BTI可用于固定虚拟内存对象（VMO）中使用的内存。如果呼叫者从VMO固定内存，则会为它们提供设备物理地址，可用于向VMO发出内存事务（前提是该事务具有正确的总线事务ID）。如果使用不同的交易ID发行影响这些地址的交易，则该交易可能会失败，并且发行设备可能需要重置才能继续运行。

A BTI manages a list of quarantined PMTs.  If a PMT was created from a BTI using [`zx_bti_pin()`], and the PMT's handle is released without [`zx_pmt_unpin()`] beingcalled, the PMT will be quarantined.  Quarantined PMTs will prevent theirunderlying physical memory from being released to the system for reuse, in orderto prevent DMA to memory that has since been reallocated.  The quarantine may becleared by invoking [`zx_bti_release_quarantine()`]. BTI管理隔离的PMT列表。如果使用[`zx_bti_pin（）]从BTI创建了一个PMT，并且释放了PMT的句柄而没有调用[`zx_pmt_unpin（）`]，则将隔离PMT。隔离的PMT将阻止将其底层物理内存释放到系统中以供重用，以防止DMA到此后重新分配的内存中。可以通过调用[`zx_bti_release_quarantine（）`来清除隔离区。

TODO(teisenbe): Add details about failed transaction notification.  TODO（teisenbe）：添加有关失败交易通知的详细信息。

 
## SEE ALSO  也可以看看 

 
 - [pmt](pinned_memory_token.md) - Pinned Memory Tokens  -[pmt]（pinned_memory_token.md）-固定内存令牌
 - [vm_object](vm_object.md) - Virtual Memory Objects  -[vm_object]（vm_object.md）-虚拟内存对象

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_bti_create()`] - create a new bus transaction initiator  -[`zx_bti_create（）`]-创建一个新的总线事务发起者
 - [`zx_bti_pin()`] - pin memory and grant access to it to the BTI  -[`zx_bti_pin（）`]-引脚存储器并将其访问权授予BTI
 - [`zx_bti_release_quarantine()`] - release quarantined PMTs  -[`zx_bti_release_quarantine（）`]-发布隔离的PMT
 - [`zx_pmt_unpin()`] - revoke access and unpin memory  -[`zx_pmt_unpin（）`]-撤消访问权限并取消固定内存

[`zx_bti_create()`]: /docs/reference/syscalls/bti_create.md  [`zx_bti_create（）`]：/docs/reference/syscalls/bti_create.md

[`zx_bti_pin()`]: /docs/reference/syscalls/bti_pin.md [`zx_bti_release_quarantine()`]: /docs/reference/syscalls/bti_release_quarantine.md[`zx_pmt_unpin()`]: /docs/reference/syscalls/pmt_unpin.md [`zx_bti_pin（）`]：/docs/reference/syscalls/bti_pin.md [`zx_bti_release_quarantine（）`]：/docs/reference/syscalls/bti_release_quarantine.md [`zx_pmt_unpin（）`]：/ docs / reference / syscalls /pmt_unpin.md

