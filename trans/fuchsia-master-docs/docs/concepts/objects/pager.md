 
# Pager  传呼机 

 
## NAME  名称 

pager - Mechanism for userspace paging  pager-用户空间分页机制

 
## SYNOPSIS  概要 

Pagers provide a mechanism for a userspace process to provide demand paging for VMOs.  寻呼机为用户空间进程提供了一种机制，以为VMO提供按需寻呼。

 
## DESCRIPTION  描述 

A pager object allows a userspace pager service (typically a filesystem) to create VMOs that serve as in-memory caches for external data. For a given VMO created by a pager object, the kerneldelivers page requests to an associated port. The pager service is then responsible for fulfillingthe requests by supplying the appropriate pages to the VMO. 寻呼机对象允许用户空间寻呼机服务（通常是文件系统）创建用作外部数据的内存中缓存的VMO。对于由寻呼机对象创建的给定VMO，内核将寻呼请求传递到关联的端口。然后，寻呼机服务通过向VMO提供适当的页面来负责满足请求。

The kernel does not do prefetching; it is the responsibility of the pager service to implement any applicable prefetching. 内核不进行预取；寻呼机服务负责实施任何适用的预取。

It is possible for a single pager to simultaniously back multiple VMOs. Requests for the different VMOs can be differentiated by the *key* parameter used when creating the VMO. It is also possiblefor multiple independent pager objects to exist simultaniously. 单个寻呼机有可能同时备份多个VMO。创建VMO时，可以通过使用* key *参数来区分对不同VMO的请求。多个独立的寻呼机对象也可以同时存在。

Creating a pager is not a privileged operation. However, the default behavior of syscalls which operate on VMOs is to fail if the operation would require blocking on IPC back to a userspaceprocess, so applications generally need to be aware of when they are operating on pager ownedVMOs. This means that services which provide pager owned VMOs to clients should be explicit aboutdoing so as part of their API. Whether or not accesses into a VMO may result in a pager requestcan be determined by checking for the **ZX_INFO_VMO_PAGER_BACKED** flag returned by[`zx_object_get_info()`] in `zx_info_vmo_t`. 创建寻呼机不是特权操作。但是，如果操作需要在IPC上阻塞回用户空间进程，则该操作在VMO上进行的系统调用的默认行为将失败，因此应用程序通常需要了解它们何时在具有寻呼机的VMO上进行操作。这意味着向客户提供传呼机拥有的VMO的服务应明确地这样做，作为其API的一部分。可以通过检查zx_info_vmo_t中[zx_object_get_info（）]返回的** ZX_INFO_VMO_PAGER_BACKED **标志来确定是否访问VMO可能导致寻呼请求。

TODO(stevensd): Writeback is not currently implemented. Update the documentation when it is.  TODO（stevensd）：当前未实现写回。在更新文档时。

 
## SEE ALSO  也可以看看 

 
+ [vm_object](vm_object.md) - Virtual Memory Objects  + [vm_object]（vm_object.md）-虚拟内存对象

 
## SYSCALLS  SYSCALLS 

 
+ [pager_create](/docs/reference/syscalls/pager_create.md) - create a new pager object  + [pager_create]（/ docs / reference / syscalls / pager_create.md）-创建一个新的寻呼机对象
+ [pager_create_vmo](/docs/reference/syscalls/pager_create_vmo.md) - create a vmo owned by a pager  + [pager_create_vmo]（/ docs / reference / syscalls / pager_create_vmo.md）-创建由寻呼机拥有的vmo
+ [pager_detach_vmo](/docs/reference/syscalls/pager_detach_vmo.md) - detaches a pager from a vmo  + [pager_detach_vmo]（/ docs / reference / syscalls / pager_detach_vmo.md）-从vmo分离寻呼机
