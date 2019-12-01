 
# Memory and resource usage  内存和资源使用 

This file contains information about memory and resource management in Zircon, and talks about ways to examine process and system memory usage. 该文件包含有关Zircon中的内存和资源管理的信息，并讨论了检查进程和系统内存使用情况的方法。

Note: **TODO**(dbort): Talk about the relationship between address spaces, [VMARs](/docs/concepts/objects/vm_address_region.md), [mappings](/docs/reference/syscalls/vmar_map.md), and[VMOs](/docs/concepts/objects/vm_object.md) 注意：** TODO **（dbort）：讨论地址空间之间的关系，[VMAR]（/ docs / concepts / objects / vm_address_region.md），[mappings]（/ docs / reference / syscalls / vmar_map.md）和[VMO]（/ docs / concepts / objects / vm_object.md）

[TOC]  [目录]

 
## Userspace memory  用户空间内存 

Which processes are using all of the memory?  哪些进程正在使用所有内存？

 
### Dump total process memory usage  转储总进程内存使用率 

Use the `ps` tool:  使用`ps`工具：

```
$ ps
TASK           PSS PRIVATE  SHARED NAME
j:1028       32.9M   32.8M         root
  p:1043   1386.3k   1384k     28k bin/devmgr
  j:1082     30.0M   30.0M         zircon-drivers
    p:1209  774.3k    772k     28k /boot/bin/acpisvc
    p:1565  250.3k    248k     28k devhost:root
    p:1619  654.3k    652k     28k devhost:misc
    p:1688  258.3k    256k     28k devhost:platform
    p:1867 3878.3k   3876k     28k devhost:pci#1:1234:1111
    p:1916   24.4M   24.4M     28k devhost:pci#3:8086:2922
  j:1103   1475.7k   1464k         zircon-services
    p:1104  298.3k    296k     28k crashlogger
    p:1290  242.3k    240k     28k netsvc
    p:2115  362.3k    360k     28k sh:console
    p:2334  266.3k    264k     28k sh:vc
    p:2441  306.3k    304k     28k /boot/bin/ps
TASK           PSS PRIVATE  SHARED NAME
```
 

**PSS** (proportional shared state) is a number of bytes that estimates how much in-process mapped physical memory the process consumes. Its value is `PRIVATE +(SHARED / sharing-ratio)`, where `sharing-ratio` is based on the number ofprocesses that share each of the pages in this process. ** PSS **（比例共享状态）是估计该进程消耗多少进程内映射物理内存的字节数。它的值是“ PRIVATE +（SHARED /共享比率）”，其中“ sharing-ratio”基于共享此进程中每个页面的进程数。

The intent is that, e.g., if four processes share a single page, 1/4 of the bytes of that page is included in each of the four process's `PSS`. If twoprocesses share a different page, then each gets 1/2 of that page's bytes. 目的是，例如，如果四个进程共享一个页面，则该页面的1/4字节包含在四个进程的“ PSS”中。如果两个进程共享不同的页面，则每个进程将获取该页面的字节的1/2。

**PRIVATE** is the number of bytes that are mapped only by this process. I.e., no other process maps this memory. Note that this does not account for privateVMOs that are not mapped. ** PRIVATE **是仅此过程映射的字节数。即，没有其他进程映射此内存。请注意，这不考虑未映射的privateVMO。

**SHARED** is the number of bytes that are mapped by this process and at least one other process. Note that this does not account for shared VMOs that are notmapped. It also does not indicate how many processes share the memory: it couldbe 2, it could be 50. ** SHARED **是此进程和至少一个其他进程映射的字节数。请注意，这不考虑未映射的共享VMO。它也不表示有多少个进程共享内存：可能是2，可能是50。

 
### Visualize memory usage  可视化内存使用情况 

If you have a Fuchsia build, you can use treemap to visualize memory usage by the system. 如果您使用的是紫红色的版本，则可以使用树形图来查看系统的内存使用情况。

 
 1. On your host machine, run the following command from the root of your Fuchsia checkout: 1.在您的主机上，从您的紫红色结帐的根目录运行以下命令：

    ```./scripts/fx shell memgraph -vt | ./scripts/memory/treemap.py > mem.html```

 2. Open `mem.html` in a browser.

The `memgraph` tool generates a JSON description of system task and memory
information, which is then parsed by the `treemap.py` script. `-vt` says
to include VMOs and threads in the output.

### Dump a process's detailed memory maps

If you want to see why a specific process uses so much memory, you can run the
`vmaps` tool on its koid (koid is the ID that shows up when running ps) to see
what it has mapped into memory.

```
$ vmaps help Usage: vmaps <process-koid> $ vmaps help用法：vmaps <process-koid>

Dumps a process's memory maps to stdout.  将进程的内存映射转储到stdout。

First column: "/A" -- Process address space"/R" -- Root VMAR"R"  -- VMAR (R for Region)"M"  -- Mapping 第一列：“ / A”-进程地址空间“ / R” –根VMAR“ R” – VMAR（区域的R）“ M” –映射

```

Column tags:

-   `:sz`: The virtual size of the entry, in bytes. Not all pages are
    necessarily backed by physical memory.
-   `:res`: The amount of memory "resident" in the entry, in bytes; i.e., the
    amount of physical memory that backs the entry. This memory may be private
    (only accessible by this process) or shared by multiple processes.
-   `:vmo`: The `koid` of the VMO mapped into this region.

```
  Indentation indicates parent/child relationship. $ vmaps 2470/A ________01000000-00007ffffffff000    128.0T:sz                    'proc:2470'/R ________01000000-00007ffffffff000    128.0T:sz                    'root'... 缩进表示父母/孩子的关系。 $ vmaps 2470 / A ________ 01000000-00007ffffffff000 128.0T：sz'proc：2470'/ R ________ 01000000-00007ffffffff000 128.0T：sz'root'...
# This 'R' region is a dynamic library. The r-x section is .text, the r--  这个“ R”区域是一个动态库。 r-x部分是.text，r-- 
# section is .rodata, and the rw- section is .data + .bss.  部分是.rodata，而rw-部分是.data + .bss。R  00000187bc867000-00000187bc881000      104k:sz                    'useralloc' M 00000187bc867000-00000187bc87d000 r-x   88k:sz   0B:res  2535:vmo 'libfdio.so'M 00000187bc87e000-00000187bc87f000 r--    4k:sz   4k:res  2537:vmo 'libfdio.so'M 00000187bc87f000-00000187bc881000 rw-    8k:sz   8k:res  2537:vmo 'libfdio.so'... R 00000187bc867000-00000187bc881000 104k：sz'useralloc'M 00000187bc867000-00000187bc87d000 rx 88k：sz 0B：res 2535：vmo'libfdio.so'M 00000187bc87e000-00000187bc87f000 r-- 4k：sz 4k：res 2537：vmo' M 00000187bc87f000-00000187bc881000 rw- 8k：sz 8k：res 2537：vmo'libfdio.so'...
# This 2MB anonymous mapping is probably part of the heap.  这个2MB的匿名映射可能是堆的一部分。M  0000246812b91000-0000246812d91000 rw-    2M:sz  76k:res  2542:vmo 'mmap-anonymous' ... M 0000246812b91000-0000246812d91000 rw- 2M：sz 76k：res 2542：vmo'mmap-anonymous'...
# This region looks like a stack: a big chunk of virtual space (:sz) with a  该区域看起来像一个堆栈：一大块虚拟空间（：sz），带有 
# slightly-smaller mapping inside (accounting for a 4k guard page), and only a  内部的映射略小（占4k保护页面），并且只有一个 
# small amount actually committed (:res).  实际提交的少量（：res）。R  0000358923d92000-0000358923dd3000      260k:sz                    'useralloc' M 0000358923d93000-0000358923dd3000 rw-  256k:sz  16k:res  2538:vmo ''... R 0000358923d92000-0000358923dd3000 260k：sz'useralloc'M 0000358923d93000-0000358923dd3000 rw- 256k：sz 16k：res 2538：vmo''...
# The stack for the initial thread, which is allocated differently.  初始线程的堆栈，分配方式不同。M  0000400cbba84000-0000400cbbac4000 rw-  256k:sz   4k:res  2513:vmo 'initial-stack' ... M 0000400cbba84000-0000400cbbac4000 rw- 256k：sz 4k：res 2513：vmo'初始堆栈'...
# The vDSO, which only has .text and .rodata.  vDSO，仅具有.text和.rodata。R  000047e1ab874000-000047e1ab87b000       28k:sz                    'useralloc' M 000047e1ab874000-000047e1ab87a000 r--   24k:sz  24k:res  1031:vmo 'vdso/full'M 000047e1ab87a000-000047e1ab87b000 r-x    4k:sz   4k:res  1031:vmo 'vdso/full'... R 000047e1ab874000-000047e1ab87b000 28k：sz'useralloc'M 000047e1ab874000-000047e1ab87a000 r-- 24k：sz 24k：res 1031：vmo'vdso / full'M 000047e1ab87a000-000047e1ab87b000 rx 4k：sz / 4k'：res 1031 ...
# The main binary for this process.  此过程的主要二进制文件。```

### Dump all VMOs associated with a process

```
```

This will also show unmapped VMOs, which neither `ps` nor `vmaps` currently
account for.

It also shows whether a given VMO is a child, along with its parent's koid.

```
R  000059f5c7068000-000059f5c708d000      148k:sz                    'useralloc' M 000059f5c7068000-000059f5c7088000 r-x  128k:sz   0B:res  2476:vmo '/boot/bin/sh'M 000059f5c7089000-000059f5c708b000 r--    8k:sz   8k:res  2517:vmo '/boot/bin/sh'M 000059f5c708b000-000059f5c708d000 rw-    8k:sz   8k:res  2517:vmo '/boot/bin/sh'...vmos <pid>$ vmos 1118rights  koid parent #chld #map #shr    size   alloc namerwxmdt  1170      -     0    1    1      4k      4k stack: msg of 0x5ar-xmdt  1031      -     2   28   14     28k     28k vdso/full R 000059f5c7068000-000059f5c708d000 148k：sz'useralloc'M 000059f5c7068000-000059f5c7088000 rx 128k：sz 0B：res 2476：vmo'/ boot / bin / sh'M 000059f5c7089000-000059f5c708b000 r-- 8k：sz 8mo：res 2517 boot / bin / sh'M 000059f5c708b000-000059f5c708d000 rw- 8k：sz 8k：res 2517：vmo'/boot/bin/sh'...vmos <pid> $ vmos 1118rights koid父chld映射shr大小分配名称rwxmdt 1170-0 1 1 4k 4k堆栈：消息的0x5ar-xmdt 1031-2 28 14 28k 28k vdso / full
     -  1298      -     0    1    1      2M     68k jemalloc-heap  -1298-0 1 1 2M 68k jemalloc-堆
     -  1381      -     0    3    1    516k      8k self-dump-thread:0x12afe79c8b38  -1381-0 3 1 516k 8k自转储线程：0x12afe79c8b38
     -  1233   1232     1    1    1   33.6k      4k libbacktrace.so  -1233 1232 1 1 1 33.6k 4k libbacktrace.so
     -  1237   1233     0    1    1      4k      4k data:libbacktrace.so ... -1237 1233 0 1 1 4k 4k数据：libbacktrace.so ...
     -  1153   1146     1    1    1  883.2k     12k ld.so.1  -1153 1146 1 1 1 883.2k 12k ld.so.1
     -  1158   1153     0    1    1     16k     12k data:ld.so.1  -1158 1153 0 1 1 16k 12k数据：ld.so.1
```

Columns:

-   `rights`: If the process points to the VMO via a handle, this column shows
    the rights that the handle has, zero or more of:
    -   `r`: `ZX_RIGHT_READ`
    -   `w`: `ZX_RIGHT_WRITE`
    -   `x`: `ZX_RIGHT_EXECUTE`
    -   `m`: `ZX_RIGHT_MAP`
    -   `d`: `ZX_RIGHT_DUPLICATE`
    -   `t`: `ZX_RIGHT_TRANSFER`
    -   **NOTE**: Non-handle entries will have a single '-' in this column.
-   `koid`: The koid of the VMO, if it has one. Zero otherwise. A VMO without a
    koid was created by the kernel, and has never had a userspace handle.
-   `parent`: The koid of the VMO's parent, if it's a child.
-   `#chld`: The number of active children of the VMO.
-   `#map`: The number of times the VMO is currently mapped into VMARs.
-   `#shr`: The number of processes that map (share) the VMO.
-   `size`: The VMO's current size, in bytes.
-   `alloc`: The amount of physical memory allocated to the VMO, in bytes.
    -   **NOTE**: If this column contains the value `phys`, it means that the
        VMO points to a raw physical address range like a memory-mapped device.
        `phys` VMOs do not consume RAM.
-   `name`: The name of the VMO, or `-` if its name is empty.

To relate this back to `ps`: each VMO contributes, for its mapped portions
(since not all or any of a VMO's pages may be mapped):

```
```

### Dump "hidden" (unmapped and kernel) VMOs

Note: This is a kernel command, and will print to the kernel console.

```
```

Similar to `vmos <pid>`, but dumps all VMOs in the system that are not mapped
into any process:

-   VMOs that userspace has handles to but does not map
-   VMOs that are mapped only into kernel space
-   Kernel-only, unmapped VMOs that have no handles

A `koid` value of zero means that only the kernel has a reference to that VMO.

A `#map` value of zero means that the VMO is not mapped into any address space.

**See also**: `k zx vmos all`, which dumps all VMOs in the system. **NOTE**:
It's very common for this output to be truncated because of kernel console
buffer limitations, so it's often better to combine the `k zx vmos hidden`
output with a `vmaps` dump of each user process.

### Limitations

Neither `ps` nor `vmaps` currently account for:

-   VMOs or VMO subranges that are not mapped. E.g., you could create a VMO,
    write 1G of data into it, and it won't show up here.

None of the process-dumping tools account for:

-   Multiply-mapped pages. If you create multiple mappings using the same range
    of a VMO, any committed pages of the VMO will be counted as many times as
    those pages are mapped. This could be inside the same process, or could be
    between processes if those processes share a VMO.

    Note that "multiply-mapped pages" includes copy-on-write.
-   Underlying kernel memory overhead for resources allocated by a process.
    E.g., a process could have a million handles open, and those handles consume
    kernel memory.

    You can look at process handle consumption with the `k zx ps` command; run
    `k zx ps help` for a description of its columns.
-   Copy-on-write (COW) cloned VMOs. The clean (non-dirty, non-copied) pages of
    a clone will not count towards "shared" for a process that maps the clone,
    and those same pages may mistakenly count towards "private" of a process
    that maps the parent (cloned) VMO.

    TODO(dbort): Fix this; the tools were written before COW clones existed.

## Kernel memory

### Dump system memory arenas and kernel heap usage

Running `kstats -m` will continuously dump information about physical memory
usage and availability.

```
     -  1159      -     0    1    1     12k     12k bss:ld.so.1 rights  koid parent #chld #map #shr    size   alloc namePRIVATE =  #shr == 1 ? alloc : 0SHARED  =  #shr  > 1 ? alloc : 0PSS     =  PRIVATE + (SHARED / #shr)k zx vmos hidden$ kstats -m--- 2017-06-07T05:51:08.021Z ---total       free       VMOs      kheap      kfree      wired        mmu2046.9M    1943.8M      20.7M       1.1M       0.9M      72.6M       7.8M -1159-0 1 1 12k 12k bss：ld.so.1权利koid父chld映射shr大小分配名称PRIVATE = shr == 1？分配：0SHARED = shr> 1？ alloc：0PSS = PRIVATE +（SHARED / shr）k zx vmos hidden $ kstats -m --- 2017-06-07T05：51：08.021Z-总计免费VMO kheap kfree有线mmu2046.9M 1943.8M 20.7M 1.1M 90万7260万780万

```

Fields:

-   `2017-06-07T05:51:08.021Z`: Timestamp of when the stats were collected, as
    an ISO 8601 string.
-   `total`: The total amount of physical memory available to the system.
-   `free`: The amount of unallocated memory.
-   `VMOs`: The amount of memory committed to VMOs, both kernel and user. A
    superset of all userspace memory. Does not include certain VMOs that fall
    under `wired`.
-   `kheap`: The amount of kernel heap memory marked as allocated.
-   `kfree`: The amount of kernel heap memory marked as free.
-   `wired`: The amount of memory reserved by and mapped into the kernel for
    reasons not covered by other fields in this struct. Typically for readonly
    data like the ram disk and kernel image, and for early-boot dynamic memory.
-   `mmu`: The amount of memory used for architecture-specific MMU metadata like
    page tables.

### Dump the kernel address space

Note: This is a kernel command, and will print to the kernel console.

```
```

Dumps the kernel's VMAR/mapping/VMO hierarchy, similar to the `vmaps` tool for
user processes.

```
```
