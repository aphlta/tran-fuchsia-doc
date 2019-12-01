 
# Resource  资源资源 

 
## NAME  名称 

resource - Address space rights and accounting  资源-地址空间权利和会计

 
## SYNOPSIS  概要 

A resource is an immutable object that is used to validate access to syscalls that create objects backed by address space, or permit access to address space.These include [vm objects](vm_object.md), [interrupts](interrupts.md), and x86ioports. 资源是一个不可变的对象，用于验证对创建由地址空间支持的对象的系统调用的访问或允许对地址空间的访问。这些对象包括[vm objects]（vm_object.md），[interrupts]（interrupts.md），和x86ioports。

 
## DESCRIPTION  描述 

Resources are used to gate access to specific regions of address space and are required to create VMOs and IRQs, as well as accessing x86 ioports. 资源用于控制对地址空间特定区域的访问，并且是创建VMO和IRQ以及访问x86 ioport所必需的资源。

A resource object consists of a single resource *kind*, with *base* address and *len* parameters that define a range of address space the holder of the resourceis granted access to. The range covers *base* up to but not including *base* +*len*.  These objects are immutable after creation. Valid *kind*  values are**ZX_RSRC_KIND_ROOT**, **ZX_RSRC_KIND_HYPERVISOR**, **ZX_RSRC_KIND_MMIO**,**ZX_RSRC_KIND_IOPORT**, **ZX_RSRC_KIND_IRQ**, **ZX_RSRC_KIND_VMEX**, and**ZX_RSRC_KIND_SMC**. New resources may be created with an appropriate parentresource by calling [`zx_resource_create()`]. An initial rootresource is created by the kernel during boot and handed off to the firstuserspace process started by userboot. 资源对象由单个资源*类型*组成，具有*基本*地址和* len *参数，这些参数定义了允许资源持有者访问的地址空间范围。范围涵盖* base *，但不包括* base * + * len *。创建后这些对象是不可变的。有效的*类型值是** ZX_RSRC_KIND_ROOT **，** ZX_RSRC_KIND_HYPERVISOR **，** ZX_RSRC_KIND_MMIO **，** ZX_RSRC_KIND_IOPORT **，** ZX_RSRC_KIND_IRQ **，** XX_RSRC_KIND_SMC，** ZX_RSRC_KIND_VMEX。通过调用[`zx_resource_create（）]，可以使用适当的parentresource创建新资源。内核在启动期间创建了初始rootresource，并将其移交给了userboot启动的firstuserspace进程。

Appropriate parent resources are the root resource, or a resource whose own range from *base* to *base+len* contains the range requested for the new resource. The*kind* of a parent resource must match the *kind* of the resource being created.At this time, *exclusive* resources cannot be used to create new resources. Aftercreation there is no relation between the resource parent used and the new resourcecreated. 适当的父资源是根资源，或者是其自己的从* base *到* base + len *的范围包含为新资源请求的范围的资源。父资源的“种类”必须与正在创建的资源的“种类”相匹配。目前，“独占”资源不能用于创建新资源。创建之后，所使用的资源父级与创建的新资源之间没有关系。

Resource allocations can be either *shared* or *exclusive*. A shared resource grants the permission to access the given address space, but does not reservethat address space exclusively for the owner of the resource. An exclusiveresource grants access to the region to only the holder of the exclusiveresource.  Exclusive and shared resource ranges may not overlap. 资源分配可以是“共享的”或“专有的”。共享资源授予访问给定地址空间的权限，但不专门为资源所有者保留该地址空间。专有资源仅授予专有资源所有者访问该区域的权限。独占和共享资源范围可能不会重叠。

Resources are lifecycle tracked and upon the last handle being closed will be freed. In the case of exclusive resources this means the given address rangewill be released back to the allocator for the given *kind* of resource. Objectscreated through a resource do not hold a reference to the resource and thus donot keep it alive. 跟踪资源的生命周期，并在最后一个句柄关闭时释放资源。在专用资源的情况下，这意味着给定的地址范围将被释放回给定给定类型的资源。通过资源创建的对象不会保存对该资源的引用，因此不会使其保持活动状态。

 
## NOTES  笔记 

Resources are typically private to the DDK and platform bus drivers. Presently, this means ACPI and platform bus hold the root resource respectively and handout more fine-grained resources to other drivers. 资源通常是DDK和平台总线驱动程序专用的。当前，这意味着ACPI和平台总线分别持有根资源，并将更多细粒度的资源分发给其他驱动程序。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_interrupt_create()`]  -[`zx_interrupt_create（）`]
 - [`zx_ioports_request()`]  -[`zx_ioports_request（）`]
 - [`zx_resource_create()`]  -[`zx_resource_create（）`]
 - [`zx_vmo_create_physical()`]  -[`zx_vmo_create_physical（）`]

