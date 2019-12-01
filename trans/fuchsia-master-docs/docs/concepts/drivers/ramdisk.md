 

 

<!-- (C) Copyright 2018 The Fuchsia Authors. All rights reserved.Use of this source code is governed by a BSD-style license that can befound in the LICENSE file.--> <！-（C）版权所有2018 The Fuchsia Authors。保留所有权利。此源代码的使用由BSD样式的许可证管理，该许可证可以在LICENSE文件中找到。-->

 
# RAMdisk Device  RAMdisk设备 

This document is part of the [Driver Development Kit tutorial](ddk-tutorial.md) documentation.  本文档是[Driver Development Kit教程]（ddk-tutorial.md）文档的一部分。

 
## Overview  总览 

In this section, we'll examine a simplified RAM-disk driver.  在本节中，我们将研究简化的RAM磁盘驱动程序。

This driver introduces:  该驱动程序介绍：

 
*   the block protocol's **query()** and **queue()** ops  *块协议的** query（）**和** queue（）** ops
*   Virtual Memory Address Regions ([VMAR](/docs/concepts/objects/vm_address_region.md)s) and Virtual Memory Objects ([VMO](/docs/concepts/objects/vm_object.md)s) *虚拟内存地址区域（[VMAR]（/ docs / concepts / objects / vm_address_region.md）s）和虚拟内存对象（[VMO]（/ docs / concepts / objects / vm_object.md）s

The source is in `//zircon/system/dev/sample/ramdisk/demo-ramdisk.c`.  源位于“ //zircon/system/dev/sample/ramdisk/demo-ramdisk.c”中。

As with all drivers, the first thing to look at is how the driver initializes itself:  与所有驱动程序一样，首先要看的是驱动程序如何初始化自身：

```c
static zx_status_t ramdisk_driver_bind(void* ctx, zx_device_t* parent) {
    zx_status_t status = ZX_OK;

    // (1) create the device context block
    ramdisk_device_t* ramdev = calloc(1, sizeof((*ramdev)));
    if (ramdev == NULL) {
        return ZX_ERR_NO_MEMORY;
    }

    // (2) create a VMO
    status = zx_vmo_create(RAMDISK_SIZE, 0, &ramdev->vmo);
    if (status != ZX_OK) {
        goto cleanup;
    }

    // (3) map the VMO into our address space
    status = zx_vmar_map(zx_vmar_root_self(), 0, ramdev->vmo, 0, RAMDISK_SIZE,
                         ZX_VM_FLAG_PERM_READ | ZX_VM_FLAG_PERM_WRITE, &ramdev->mapped_addr);
    if (status != ZX_OK) {
        goto cleanup;
    }

    // (4) add the device
    device_add_args_t args = {
        .version = DEVICE_ADD_ARGS_VERSION,
        .name = "demo-ramdisk",
        .ctx = ramdev,
        .ops = &ramdisk_proto,
        .proto_id = ZX_PROTOCOL_BLOCK_IMPL,
        .proto_ops = &block_ops,
    };

    if ((status = device_add(parent, &args, &ramdev->zxdev)) != ZX_OK) {
        ramdisk_release(ramdev);
    }
    return status;

    // (5) clean up after ourselves
cleanup:
    zx_handle_close(ramdev->vmo);
    free(ramdev);
    return status;
}

static zx_driver_ops_t ramdisk_driver_ops = {
    .version = DRIVER_OPS_VERSION,
    .bind = ramdisk_driver_bind,
};

ZIRCON_DRIVER_BEGIN(ramdisk, ramdisk_driver_ops, "zircon", "0.1", 1)
    BI_MATCH_IF(EQ, BIND_PROTOCOL, ZX_PROTOCOL_MISC_PARENT),
ZIRCON_DRIVER_END(ramdisk)

```
 

At the bottom, you can see that this driver binds to a `ZX_PROTOCOL_MISC_PARENT` type of protocol, and provides `ramdisk_driver_ops` as the list of operations supported.This is no different than any of the other drivers we've seen so far. 在底部，您可以看到该驱动程序已绑定到ZX_PROTOCOL_MISC_PARENT类型的协议，并提供了ramdisk_driver_ops作为支持的操作列表，这与到目前为止我们看到的其他任何驱动程序都没有什么不同。

The binding function, **ramdisk_driver_bind()**, does the following:  绑定函数ramdisk_driver_bind（）**执行以下操作：

 
1.  Allocates the device context block.  1.分配设备上下文块。
2.  Creates a [VMO](/docs/concepts/objects/vm_object.md). The [VMO](/docs/concepts/objects/vm_object.md)is a kernel object that represents a chunk of memory.In this simplified RAM-disk driver, we're creating a[VMO](/docs/concepts/objects/vm_object.md) that's `RAMDISK_SIZE`bytes long.This chunk of memory **is** the RAM-disk &mdash; that's where the data is stored.The [VMO](/docs/concepts/objects/vm_object.md)creation call, [**zx_vmo_create()**](/docs/reference/syscalls/vmo_create.md),returns the [VMO](/docs/concepts/objects/vm_object.md) handle throughits third argument, which is a member in our context block. 2.创建一个[VMO]（/ docs / concepts / objects / vm_object.md）。 [VMO]（/ docs / concepts / objects / vm_object.md）是代表一个内存块的内核对象。在此简化的RAM磁盘驱动程序中，我们正在创建[VMO]（/ docs / concepts / objects /vm_object.md）的长度为RAMDISK_SIZE个字节。 [VMO]（/ docs / concepts / objects / vm_object.md）创建调用[** zx_vmo_create（）**]（/ docs / reference / syscalls / vmo_create.md）返回该数据的存储位置。 [VMO]（/ docs / concepts / objects / vm_object.md）处理其第三个参数，该参数是我们上下文块中的成员。
3.  Maps the [VMO](/docs/concepts/objects/vm_object.md) into our address space via [**zx_vmar_map()**](/docs/reference/syscalls/vmar_map.md).This function returns a pointer to a[VMAR](/docs/concepts/objects/vm_address_region.md)that points to the entire[VMO](/docs/concepts/objects/vm_object.md) (becausewe specified `RAMDISK_SIZE` as the mapping size argument) and gives us read andwrite access (because of the `ZX_VM_FLAG_PERM_*` flags).The pointer is stored in our context block's `mapped_addr` member. 3.通过[** zx_vmar_map（）**]（/ docs / reference / syscalls / vmar_map.md）将[VMO]（/ docs / concepts / objects / vm_object.md）映射到我们的地址空间。此函数返回一个指向[VMAR]（/ docs / concepts / objects / vm_address_region.md）的指针，该指针指向整个[VMO]（/ docs / concepts / objects / vm_object.md）（因为我们将“ RAMDISK_SIZE”指定为映射大小参数）并给予我们读写访问权限（因为有ZX_VM_FLAG_PERM_ *标志）。指针存储在上下文块的mapped_addr成员中。
4.  Adds our device via **device_add()**, just like all the examples we've seen above.The difference here, though is that we see two new members: `proto_id` and`proto_ops`.These are defined as "optional custom protocol" members.As usual, we store the newly created device in the `zxdev` member of ourcontext block. 4.通过** device_add（）**添加设备，就像上面看到的所有示例一样。这里的区别在于，我们看到了两个新成员：proto_id和proto_ops。这些定义为“可选的自定义协议”成员。通常，我们将新创建的设备存储在我们上下文块的`zxdev`成员中。
5.  Cleans up resources if there were any problems along the way.  5.如果在执行过程中出现任何问题，请清理资源。

For completeness, here's the context block:  为了完整起见，这是上下文块：

```c
typedef struct ramdisk_device {
    zx_device_t*    zxdev;
    uintptr_t       mapped_addr;
    uint32_t        flags;
    zx_handle_t     vmo;
    bool            dead;
} ramdisk_device_t;
```
 

The fields are:  这些字段是：

Type            | Field         | Description ----------------|---------------|----------------`zx_device_t*`  | zxdev         | the ramdisk device`uintptr_t`     | mapped_addr   | address of the [VMAR](/docs/concepts/objects/vm_address_region.md)`uin32_t`       | flags         | device flags`zx_handle_t`   | vmo           | a handle to our [VMO](/docs/concepts/objects/vm_object.md)`bool`          | dead          | indicates if the device is still alive 类型领域说明---------------- | --------------------- | ---------------- `zx_device_t *`| zxdev | ramdisk设备`uintptr_t` | mapping_addr | [VMAR]的地址（/docs/concepts/objects/vm_address_region.md）`uin32_t` |标志|设备标志`zx_handle_t` | vmo | [VMO]（/ docs / concepts / objects / vm_object.md）bool的句柄|死了指示设备是否仍在运行

 
### Operations  运作方式 

Where this device is different from the others that we've seen, though, is that the **device_add()**function adds two sets of operations; the "regular" one, and anoptional "protocol specific" one: 不过，该设备与我们看到的其他设备的不同之处在于** device_add（）**函数添加了两组操作； “常规”和一个可选的“特定于协议”的：

```c
static zx_protocol_device_t ramdisk_proto = {
    .version = DEVICE_OPS_VERSION,
    .message = ramdisk_message,
    .get_size = ramdisk_getsize,
    .unbind = ramdisk_unbind,
    .release = ramdisk_release,
};

static block_protocol_ops_t block_ops = {
    .query = ramdisk_query,
    .queue = ramdisk_queue,
};
```
 

The `zx_protocol_device_t` one handles control messages (**ramdisk_message()**), device size queries (**ramdisk_getsize()**), and device cleanups (**ramdisk_unbind()** and**ramdisk_release()**). zx_protocol_device_t`处理控制消息（** ramdisk_message（）**），设备大小查询（** ramdisk_getsize（）**）和设备清理（** ramdisk_unbind（）**和** ramdisk_release（）**） ）。

> @@@ should I discuss the ioctls, or were they to have been removed as part of the simplification?  > @@@我应该讨论这些ioctl，还是作为简化的一部分将其删除？

The `block_protocol_ops_t` one contains protocol operations particular to the block protocol.We bound these to the device in the `device_add_args_t` structure (step (4) above) viathe `.proto_ops` field.We also set the `.proto_id` field to `ZX_PROTOCOL_BLOCK_IMPL` &mdash; this is whatidentifies this driver as being able to handle block protocol operations. ``block_protocol_ops_t''包含特定于块协议的协议操作。我们通过``.proto_ops''字段将它们绑定到``device_add_args_t''结构（上面的步骤（4））中的设备上。 `ZX_PROTOCOL_BLOCK_IMPL`-这就是该驱动程序能够处理块协议操作的原因。

Let's tackle the trivial functions first:  让我们首先解决一些琐碎的功能：

```c
static zx_off_t ramdisk_getsize(void* ctx) {
    return RAMDISK_SIZE;
}

static void ramdisk_unbind(void* ctx) {
    ramdisk_device_t* ramdev = ctx;
    ramdev->dead = true;
    device_unbind_reply(ramdev->zxdev);
}

static void ramdisk_release(void* ctx) {
    ramdisk_device_t* ramdev = ctx;

    if (ramdev->vmo != ZX_HANDLE_INVALID) {
        zx_vmar_unmap(zx_vmar_root_self(), ramdev->mapped_addr, RAMDISK_SIZE);
        zx_handle_close(ramdev->vmo);
    }
    free(ramdev);
}

static void ramdisk_query(void* ctx, block_info_t* bi, size_t* bopsz) {
    ramdisk_get_info(ctx, bi);
    *bopsz = sizeof(block_op_t);
}
```
 

**ramdisk_getsize()** is the easiest &mdash; it simply returns the size of the resource, in bytes. In our simplified RAM-disk driver, this is hardcoded as a `#define` near the top of the file. ** ramdisk_getsize（）**是最简单的短划线；它只是返回资源的大小（以字节为单位）。在我们简化的RAM磁盘驱动程序中，该文件被硬编码为文件顶部附近的“定义”。

Next, **ramdisk_unbind()** and **ramdisk_release()** work together. When the driver is being shut down, the **ramdisk_unbind()** hook is called.It sets the `dead` flag to indicate that the driver is shutting down (this is checkedin the **ramdisk_queue()** handler, below).It's expected that the driver will finish up any I/O operations that are in progress (therewon't be any in our RAM-disk), and it should call**device_unbind_reply()**to indicate unbinding is complete. 接下来，ramdisk_unbind（）和ramdisk_release（）一起工作。关闭驱动程序时，将调用** ramdisk_unbind（）**钩子。它设置`dead`标志以指示驱动程序正在关闭（这在下面的** ramdisk_queue（）**处理函数中进行了检查） ）。预计驱动程序将完成所有正在进行的I / O操作（在我们的RAM磁盘中不会执行任何操作），并且应调用** device_unbind_reply（）**表示解除绑定已完成。

Sometime after **device_unbind_reply()** is called, the driver's **ramdisk_release()** will be called.Here we unmap the [VMAR](/docs/concepts/objects/vm_address_region.md),via [**zx_vmar_unmap()**](/docs/reference/syscalls/vmar_unmap.md), and close the[VMO](/docs/concepts/objects/vm_object.md),via [**zx_handle_close()**](/docs/reference/syscalls/handle_close.md).As our final act, we release the device context block.At this point, the device is finished. 在调用** device_unbind_reply（）**之后的某个时间，将调用驱动程序的** ramdisk_release（）**。在此，我们通过[** zx_vmar_unmap取消映射[VMAR]（/ docs / concepts / objects / vm_address_region.md）。 （）**]（/ docs / reference / syscalls / vmar_unmap.md），然后通过[** zx_handle_close（）**]（/ docs关闭[VMO]（/ docs / concepts / objects / vm_object.md） /reference/syscalls/handle_close.md）。作为最后一步，我们释放设备上下文块。此时，设备已完成。

 
### Block Operations  块操作 

The **ramdisk_query()** function is called by the block protocol in order to get information about the device.There's a data structure (the `block_info_t`) that's filled out by the driver: 块协议调用ramdisk_query（）函数以获取有关设备的信息。驱动程序填写了一个数据结构（`block_info_t`）：

```c
// from .../system/public/zircon/device/block.h:
typedef struct {
    uint64_t    block_count;        // The number of blocks in this block device
    uint32_t    block_size;         // The size of a single block
    uint32_t    max_transfer_size;  // Max size in bytes per transfer.
                                    // May be BLOCK_MAX_TRANSFER_UNBOUNDED if there
                                    // is no restriction.
    uint32_t    flags;
    uint32_t    reserved;
} block_info_t;

// our helper function
static void ramdisk_get_info(void* ctx, block_info_t* info) {
    ramdisk_device_t* ramdev = ctx;
    memset(info, 0, sizeof(*info));
    info->block_size = BLOCK_SIZE;
    info->block_count = BLOCK_COUNT;
    // Arbitrarily set, but matches the SATA driver for testing
    info->max_transfer_size = BLOCK_MAX_TRANSFER_UNBOUNDED;
    info->flags = ramdev->flags;
}
```
 

In this simplified driver, the `block_size`, `block_count`, and `max_transfer_size` fields are hardcoded numbers. 在这个简化的驱动程序中，“ block_size”，“ block_count”和“ max_transfer_size”字段是硬编码数字。

The `flags` member is used to identify if the device is read-only (`BLOCK_FLAG_READONLY`, otherwise it's read/write), removable (`BLOCK_FLAG_REMOVABLE`, otherwise it's notremovable) or has a bootable partition (`BLOCK_FLAG_BOOTPART`, otherwise it doesn't). “ flags”成员用于标识设备是只读的（“ BLOCK_FLAG_READONLY”，否则为读/写），可移动的（“ BLOCK_FLAG_REMOVABLE”，否则为不可移动）或是否具有可启动分区（“ BLOCK_FLAG_BOOTPART”，否则为）。不会）。

The final value that **ramdisk_query()** returns is the "block operation size" value through the pointer to `bopsz`.This is a host-maintained block that's big enough to contain the `block_op_t` *plus*any additional data the driver wants (appended to the `block_op_t`), like anextended context block. ** ramdisk_query（）**返回的最终值是通过指向`bopsz`指针的“块操作大小”值。这是一个主机维护的块，足够大，可以包含`block_op_t` *加*任何其他数据驱动程序想要的（附加到“ block_op_t”上），就像扩展的上下文块一样。

 
### Reading and writing  读写 

Finally, it's time to discuss the actual "block" data transfers; that is, how does data get read from / written to the device? 最后，是时候讨论实际的“块”数据传输了。也就是说，如何从设备读取/写入数据？

The second block protocol handler, **ramdisk_queue()**, performs that function.  第二个块协议处理程序** ramdisk_queue（）**执行该功能。

As you might suspect from the name, it's intended that this hook starts whatever transfer operation (a read or a write) is requested, but doesn't require thatthe operation completes before the hook returns.This is a little like what we saw in earlier chaptersin the **read()** and **write()** handlersfor devices like `/dev/misc/demo-fifo` &mdash; there, we could either returndata immediately, or put the client to sleep, waking it up later when data (or roomfor data) became available. 正如您可能从名称中怀疑的那样，此钩子旨在启动任何请求的传输操作（读取或写入），但不需要在钩子返回之前完成该操作。这有点像我们之前所看到的诸如/ dev / misc / demo-fifo`等设备的** read（）**和** write（）**处理程序中的章节；在那里，我们可以立即返回数据，也可以让客户端进入睡眠状态，然后在数据（或数据空间）可用时将其唤醒。

With **ramdisk_queue()** we get passed a block operations structure that indicates the expected operation: `BLOCK_OP_READ`, `BLOCK_OP_WRITE`, or `BLOCK_OP_FLUSH`.The structure also contains additional fields telling us the offset and size ofthe transfer (from `//zircon/system/ulib/ddk/include/ddk/protocol/block.h`): 通过ramdisk_queue（）**，我们传递了一个块操作结构，该结构指示了预期的操作：`BLOCK_OP_READ`，`BLOCK_OP_WRITE`或`BLOCK_OP_FLUSH`。该结构还包含其他字段，这些字段告诉我们转移的偏移量和大小（从`// zircon / system / ulib / ddk / include / ddk / protocol / block.h`）：

```c
// simplified from original
struct block_op {
    struct {
        uint32_t    command;    // command and flags
        uint32_t    extra;      // available for temporary use
        zx_handle_t vmo;        // vmo of data to read or write
        uint32_t    length;     // transfer length in blocks (0 is invalid)
        uint64_t    offset_dev; // device offset in blocks
        uint64_t    offset_vmo; // vmo offset in blocks
        uint64_t*   pages;      // optional physical page list
    } rw;

    void (*completion_cb)(block_op_t* block, zx_status_t status);
};
```
 

The transfer takes place to or from the `vmo` in the structure &mdash; in the case of a read, we transfer data to the [VMO](/docs/concepts/objects/vm_object.md),and vice versa for a write.The `length` indicates the number of *blocks* (not bytes) to transfer, and thetwo offset fields, `offset_dev` and `offset_vmo`, indicate the relative offsets (again,in blocks not bytes) into the device and the [VMO](/docs/concepts/objects/vm_object.md)of where the transfer should take place. 转移发生在结构mdash中的“ vmo”上或从中出来。在读取的情况下，我们将数据传输到[VMO]（/ docs / concepts / objects / vm_object.md），反之亦然，以便进行写入。`length'表示* block *的数量（不是字节）要传输的偏移量，两个偏移量字段“ offset_dev”和“ offset_vmo”指示相对偏移量（再次，以块而不是字节为单位）到设备中，以及[VMO]（/ docs / concepts / objects / vm_object.md）的位置转移应该发生。

The implementation is straightforward:  实现很简单：

```c
static void ramdisk_queue(void* ctx, block_op_t* bop) {
    ramdisk_device_t* ramdev = ctx;

    // (1) see if we should still be handling requests
    if (ramdev->dead) {
        bop->completion_cb(bop, ZX_ERR_IO_NOT_PRESENT);
        return;
    }

    // (2) what operation are we performing?
    switch ((bop->command &= BLOCK_OP_MASK)) {
    case BLOCK_OP_READ:
    case BLOCK_OP_WRITE: {
        // (3) perform validation common for both
        if ((bop->rw.offset_dev >= BLOCK_COUNT)
            || ((BLOCK_COUNT - bop->rw.offset_dev) < bop->rw.length)
            || bop->rw.length * BLOCK_SIZE > MAX_TRANSFER_BYTES) {
            bop->completion_cb(bop, ZX_ERR_OUT_OF_RANGE);
            return;
        }

        // (4) compute address
        void* addr = (void*) ramdev->mapped_addr + bop->rw.offset_dev * BLOCK_SIZE;
        zx_status_t status;

        // (5) now perform actions specific to each
        if (bop->command == BLOCK_OP_READ) {
            status = zx_vmo_write(bop->rw.vmo, addr, bop->rw.offset_vmo * BLOCK_SIZE,
                                  bop->rw.length * BLOCK_SIZE);
        } else {
            status = zx_vmo_read(bop->rw.vmo, addr, bop->rw.offset_vmo * BLOCK_SIZE,
                                 bop->rw.length * BLOCK_SIZE);
        }

        // (6) indicate completion
        bop->completion_cb(bop, status);
        break;
        }

    case BLOCK_OP_FLUSH:
        bop->completion_cb(bop, ZX_OK);
        break;

    default:
        bop->completion_cb(bop, ZX_ERR_NOT_SUPPORTED);
        break;
    }
}
```
 

As usual, we establish a context block at the top by casting the `ctx` argument. The `bop` argument is the "block operation" structure we saw above.The `command` field indicates what the **ramdisk_queue()** function should do. 像往常一样，我们通过强制使用`ctx`参数在顶部建立一个上下文块。 bop参数是我们在上面看到的“块操作”结构。command字段指示ramdisk_queue（）函数应该执行的操作。

In step (1), we check to see if we've set the `dead` flag (**ramdisk_unbind()** sets it when required).If so, it means that our device is no longer accepting new requests, so we return`ZX_ERR_IO_NOT_PRESENT` in order to encourage clients to close the device. 在步骤（1）中，我们检查是否设置了`dead`标志（** ramdisk_unbind（）**在需要时进行设置），如果是这样，则意味着我们的设备不再接受新请求，因此我们返回ZX_ERR_IO_NOT_PRESENT`以鼓励客户关闭设备。

In step (3), we handle some common validation for both read and write &mdash; neither should allow offsets that exceed the size of the device, nor transfermore than the maximum transfer size. 在步骤（3）中，我们对读写mdash进行一些通用验证；偏移量都不应超过设备的大小，也不能传输超过最大传输大小的偏移。

Similarly, in step (4) we compute the device address (that is, we establish a pointer to our [VMAR](/docs/concepts/objects/vm_address_region.md)that's offset by the appropriate number of blocks as per the request). 同样，在步骤（4）中，我们计算设备地址（即，建立指向[VMAR]（/ docs / concepts / objects / vm_address_region.md）的指针，该指针根据请求偏移了适当数量的块） 。

In step (5) we perform either a [**zx_vmo_read()**](/docs/reference/syscalls/vmo_read.md) or a [**zx_vmo_write()**](/docs/reference/syscalls/vmo_write.md), dependingon the command.This is what transfers data between a pointer within our[VMAR](/docs/concepts/objects/vm_address_region.md) (`addr`)and the client's [VMO](/docs/concepts/objects/vm_object.md) (`bop->rw.vmo`).Notice that in the read case, we *write* to the [VMO](/docs/concepts/objects/vm_object.md),and in the write case, we *read* from the [VMO](/docs/concepts/objects/vm_object.md). 在步骤（5）中，我们执行[** zx_vmo_read（）**]（/ docs / reference / syscalls / vmo_read.md）或[** zx_vmo_write（）**]（/ docs / reference / syscalls / vmo_write .md），具体取决于命令。这就是在[VMAR]（/ docs / concepts / objects / vm_address_region.md）（`addr`）和客户端的[VMO]（/ docs / concepts /请注意，在读取的情况下，我们*写入* [VMO]（/ docs / concepts / objects / vm_object.md），并在写入时情况下，我们从[VMO]（/ docs / concepts / objects / vm_object.md）中*阅读*。

Finally, in step (6) (and the other two cases), we signal completion via the `completion` callback in the block ops structure. 最后，在第（6）步（以及其他两种情况）中，我们通过块ops结构中的`completion`回调发出完成信号。

The interesting thing about completion is that:  关于完成的有趣的事情是：

 
*   it doesn't have to happen right away &mdash; we could have queued this operation and signalled completion some time later, *不必立即发生–我们本可以将该操作排入队列，并在一段时间后发出完成信号，
*   it is allowed to be called before this function returns (like we did).  *允许在此函数返回之前被调用（就像我们一样）。

The last point simply means that we are not *forced* to defer completion until after the queuing function returns.This allows us to complete the operation directly in the function.For our trivial RAM-disk example, this makes sense &mdash; we have the ability todo the data transfer to or from media instantly; no need to defer. 最后一点只是意味着我们不会被“强迫”推迟完成，直到排队函数返回之后。这使我们能够直接在函数中完成操作。对于我们平凡的RAM磁盘示例，这很有道理；我们有能力立即进行与媒体之间的数据传输；无需推迟。

 
## How is the real one more complicated?  真实的又如何复杂？ 

The RAM-disk presented above is somewhat simplified from the "real" RAM-disk device (present at `//zircon/system/dev/block/ramdisk/ramdisk.c`). 上面介绍的RAM磁盘相对于“真实” RAM磁盘设备（位于“ //zircon/system/dev/block/ramdisk/ramdisk.c”中）有所简化。

The real one adds the following functionality:  真正的功能增加了以下功能：

 
*   dynamic device creation via new VMO  *通过新的VMO动态创建设备
*   ability to use an existing VMO  *使用现有VMO的能力
*   background thread  *后台线程
*   sleep mode  *   睡眠模式

> @@@ how much, if anything, do we want to say about this one? I found the > dynamic device creation of interest, for example... > @@@我们想谈谈多少（如果有的话）？我发现感兴趣的>动态设备创建，例如...

