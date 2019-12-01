 
# Virtual Memory Object  虚拟内存对象 

 
## NAME  名称 

vm\_object - Virtual memory containers  vm \ _object-虚拟内存容器

 
## SYNOPSIS  概要 

A Virtual Memory Object (VMO) represents a contiguous region of virtual memory that may be mapped into multiple address spaces. 虚拟内存对象（VMO）表示虚拟内存的连续区域，可以将其映射到多个地址空间中。

 
## DESCRIPTION  描述 

VMOs are used in by the kernel and userspace to represent both paged and physical memory. They are the standard method of sharing memory between processes, as well as between the kernel anduserspace. 内核和用户空间使用VMO来表示页面内存和物理内存。它们是在进程之间以及内核和用户空间之间共享内存的标准方法。

VMOs are created with [`zx_vmo_create()`] and basic I/O can be performed on them with [`zx_vmo_read()`] and [`zx_vmo_write()`].A VMO's size may be set using [`zx_vmo_set_size()`].Conversely, [`zx_vmo_get_size()`] will retrieve a VMO's current size. 使用[`zx_vmo_create（）]创建VMO，并可以使用[`zx_vmo_read（）]和[`zx_vmo_write（）]对它们执行基本I / O。可以使用[`zx_vmo_set_size（）设置VMO的大小。相反，[`zx_vmo_get_size（）`]将检索VMO的当前大小。

The size of a VMO will be rounded up to the next page size boundary by the kernel.  VMO的大小将由内核四舍五入到下一页的大小边界。

Pages are committed (allocated) for VMOs on demand through [`zx_vmo_read()`], [`zx_vmo_write()`], or by writing to a mapping of the VMO created using [`zx_vmar_map()`]. Pages can be committed and decommitted from a VMO manually by calling [`zx_vmo_op_range()`] with the **ZX_VMO_OP_COMMIT** and **ZX_VMO_OP_DECOMMIT**operations, but this should be considered a low level operation. [`zx_vmo_op_range()`] can also be used for cache and locking operations against pages a VMO holds. 通过[`zx_vmo_read（）]，[`zx_vmo_write（）]或通过写入使用[`zx_vmar_map（）创建的VMO的映射）按需提交（分配）VMO的页面。可以通过** ZX_VMO_OP_COMMIT **和** ZX_VMO_OP_DECOMMIT **操作调用[`zx_vmo_op_range（）`]来从VMO手动提交和取消页面，但这应视为低级操作。 [`zx_vmo_op_range（）`]也可以用于对VMO保留的页面进行缓存和锁定操作。

Processes with special purpose use cases involving cache policy can use [`zx_vmo_set_cache_policy()`] to change the policy of a given VMO.This use case typically applies to device drivers. 具有涉及缓存策略的特殊用途的过程可以使用[`zx_vmo_set_cache_policy（）`]更改给定VMO的策略。该用例通常适用于设备驱动程序。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_vmo_create()`] - create a new vmo  -[`zx_vmo_create（）`]-创建一个新的vmo
 - [`zx_vmo_read()`] - read from a vmo  -[`zx_vmo_read（）`]-从vmo读取
 - [`zx_vmo_write()`] - write to a vmo  -[`zx_vmo_write（）`]-写入vmo
 - [`zx_vmo_get_size()`] - obtain the size of a vmo  -[`zx_vmo_get_size（）`]-获取vmo的大小
 - [`zx_vmo_set_size()`] - adjust the size of a vmo  -[`zx_vmo_set_size（）`]-调整vmo的大小
 - [`zx_vmo_op_range()`] - perform an operation on a range of a vmo  -[`zx_vmo_op_range（）`]-在vmo范围内执行操作
 - [`zx_vmo_set_cache_policy()`] - set the caching policy for pages held by a vmo  -[`zx_vmo_set_cache_policy（）`]-为vmo保留的页面设置缓存策略

<br>  <br>

 
 - [`zx_vmar_map()`] - map a VMO into a process  -[`zx_vmar_map（）`]-将VMO映射到进程
 - [`zx_vmar_unmap()`] - unmap memory from a process  -[`zx_vmar_unmap（）`]-从进程取消映射内存

