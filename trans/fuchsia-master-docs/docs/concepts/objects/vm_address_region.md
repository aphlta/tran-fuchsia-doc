 
# Virtual Memory Address Region  虚拟内存地址区域 

 
## NAME  名称 

vm_address_region - A contiguous region of a virtual memory address space  vm_address_region-虚拟内存地址空间的连续区域

 
## SYNOPSIS  概要 

Virtual Memory Address Regions (VMARs) represent contiguous parts of a virtual address space. 虚拟内存地址区域（VMAR）表示虚拟地址空间的连续部分。

 
## DESCRIPTION  描述 

VMARs are used by the kernel and userspace to represent the allocation of an address space. 内核和用户空间使用VMAR来表示地址空间的分配。

Every process starts with a single VMAR (the root VMAR) that spans the entire address space (see [`zx_process_create()`]).  Each VMARcan be logically divided up into any number of non-overlapping parts, eachrepresenting a child VMARs, a virtual memory mapping, or a gap.  Child VMARsare created using [`zx_vmar_allocate()`].  VM mappingsare created using [`zx_vmar_map()`]. 每个进程都始于跨越整个地址空间的单个VMAR（根VMAR）（请参见[`zx_process_create（）]）。每个VMAR可以在逻辑上分为任意数量的不重叠部分，每个部分代表一个子VMAR，一个虚拟内存映射或一个间隙。使用[`zx_vmar_allocate（）`]创建子VMAR。使用[`zx_vmar_map（）`]创建VM映射。

VMARs have a hierarchical permission model for allowable mapping permissions. For example, the root VMAR allows read, write, and executable mapping.  Onecould create a child VMAR that only allows read and write mappings, in whichit would be illegal to create a child that allows executable mappings. VMAR具有用于允许的映射权限的分层权限模型。例如，根VMAR允许读取，写入和可执行映射。一个人可以创建仅允许读写映射的子VMAR，在其中创建允许可执行映射的子VMAR是非法的。

When a VMAR is created using [`zx_vmar_allocate()`], its parent VMAR retains a reference to it.  Because of this, if all handles to the child VMAR are closed, the childand its descendants will remain active in the address space.  In order todisconnect the child from the address space, [`zx_vmar_destroy()`]must be called on a handle to the child. 使用[`zx_vmar_allocate（）]创建VMAR时，其父VMAR保留对其的引用。因此，如果子VMAR的所有句柄都已关闭，则子及其子代将在地址空间中保持活动状态。为了使子级与地址空间断开连接，必须在子级的句柄上调用[`zx_vmar_destroy（）`]。

By default, all allocations of address space are randomized.  At VMAR creation time, the caller can choose which randomization algorithm is used.The default allocator attempts to spread allocations widely across the fullwidth of the VMAR.  The alternate allocator, selected with**ZX_VM_COMPACT**, attempts to keep allocations close together within theVMAR, but at a random location within the range.  It is recommended to usethe default allocator. 默认情况下，所有地址空间分配都是随机的。在创建VMAR时，调用方可以选择使用哪种随机算法。默认分配器尝试在VMAR的整个宽度上广泛分配分配。用** ZX_VM_COMPACT **选择的备用分配器试图使分配在VMAR内保持靠近，但在该范围内的随机位置。建议使用默认分配器。

VMARs optionally support a fixed-offset mapping mode (called specific mapping). This mode can be used to create guard pages or ensure the relative locations ofmappings.  Each VMAR may have the **ZX_VM_CAN_MAP_SPECIFIC** permission,regardless of whether or not its parent VMAR had that permission. VMAR可选地支持固定偏移量映射模式（称为特定映射）。此模式可用于创建保护页面或确保映射的相对位置。每个VMAR都可以具有** ZX_VM_CAN_MAP_SPECIFIC **权限，无论其父VMAR是否具有该权限。

 
## EXAMPLE  例 

```c
#include <zircon/syscalls.h>

/* Map this VMO into the given VMAR, with |before| bytes of unmapped guard space
   before it and |after| bytes after it.  */
zx_status_t map_with_guard(zx_handle_t vmar, size_t before, size_t after,
                           zx_handle_t vmo, uint64_t vmo_offset,
                           size_t mapping_len, uintptr_t* mapped_addr,
                           zx_handle_t* wrapping_vmar) {

    /* wrap around check elided */
    const size_t child_vmar_size = before + after + mapping_len;
    const zx_vm_option_t child_vmar_options = ZX_VM_CAN_MAP_READ |
                                              ZX_VM_CAN_MAP_WRITE |
                                              ZX_VM_CAN_MAP_SPECIFIC;
    const zx_vm_option_t mapping_options = ZX_VM_SPECIFIC |
                                           ZX_VM_PERM_READ |
                                           ZX_VM_PERM_WRITE;

    uintptr_t child_vmar_addr;
    zx_handle_t child_vmar;
    zx_status_t status = zx_vmar_allocate(vmar, child_vmar_options, 0,
                                          child_vmar_size,
                                          &child_vmar,
                                          &child_vmar_addr);
    if (status != ZX_OK) {
        return status;
    }

    status = zx_vmar_map(child_vmar, mapping_options, before, vmo, vmo_offset,
                         mapping_len, mapped_addr);
    if (status != ZX_OK) {
        zx_vmar_destroy(child_vmar);
        zx_handle_close(child_vmar);
        return status;
    }

    *wrapping_vmar = child_vmar;
    return ZX_OK;
}
```
 

 
## SEE ALSO  也可以看看 

 
 - [vm_object](vm_object.md) - Virtual Memory Objects  -[vm_object]（vm_object.md）-虚拟内存对象

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_vmar_allocate()`] - create a new child VMAR  -[`zx_vmar_allocate（）`]-创建一个新的子VMAR
 - [`zx_vmar_map()`] - map a VMO into a process  -[`zx_vmar_map（）`]-将VMO映射到进程
 - [`zx_vmar_unmap()`] - unmap a memory region from a process  -[`zx_vmar_unmap（）`]-从进程取消映射内存区域
 - [`zx_vmar_protect()`] - adjust memory access permissions  -[`zx_vmar_protect（）`]-调整内存访问权限
 - [`zx_vmar_destroy()`] - destroy a VMAR and all of its children  -[`zx_vmar_destroy（）`]-销毁VMAR及其所有子项

