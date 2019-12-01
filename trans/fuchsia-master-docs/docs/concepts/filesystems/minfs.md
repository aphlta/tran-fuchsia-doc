 
# MinFS  MinFS 

MinFS is a simple, unix-like filesystem built for Zircon.  MinFS是为Zircon构建的简单，类似于Unix的文件系统。

It currently supports files up to 4 GB in size.  当前，它支持最大4 GB的文件。

 
## Using MinFS  使用MinFS 

 
### Host Device (QEMU Only)  主机设备（仅QEMU） 

 
 * Create a disk image which stores MinFS  *创建一个存储MinFS的磁盘映像

  ```shell
  # (Linux)
  $ truncate --size=16G blk.bin
  # (Mac)
  $ mkfile -n 16g blk.bin
  ```
 

 
 * Execute the run zircon script on your platform with the '--' to pass arguments directly to QEMU and then use '-hda' to point to the file. If youwish to attach additional devices, you can supply them with '-hdb', '-hdc,and so on. *在平台上使用'-'执行run zircon脚本，以将参数直接传递给QEMU，然后使用'-hda'指向文件。如果您希望连接其他设备，则可以为其提供'-hdb'，'-hdc等。

  ```shell
  fx set bringup.x64
  fx build
  fx qemu -- -hda blk.bin
  ```
 

 
### Target Device (QEMU and Real Hardware)  目标设备（QEMU和真实硬件） 

Warning: On real hardware, `/dev/class/block/...` refers to **REAL** storage devices (USBs, SSDs, etc). 警告：在实际硬件上，`/ dev / class / block / ...`指的是** REAL **存储设备（USB，SSD等）。

**BE CAREFUL NOT TO FORMAT THE WRONG DEVICE.** If in doubt, only run the following commands through QEMU.The `lsblk` command can be used to see more information about the devicesaccessible from Zircon. **请不要格式化错误的设备。**如果有疑问，请仅通过QEMU运行以下命令。`lsblk`命令可用于查看有关可从Zircon访问的设备的更多信息。

 
 * Within zircon, `lsblk` can be used to list the block devices currently on the system. On this example system below, `/dev/class/block/000` is a rawblock device. *在锆石中，`lsblk`可用于列出系统上当前的块设备。在下面的示例系统中，`/ dev / class / block / 000`是rawblock设备。

  ```
  > lsblk
  ID  DEV      DRV      SIZE TYPE           LABEL
  000 block    block     16G
  ```
 

 
 * Let's add a GPT to this block device.  *让我们向该块设备添加GPT。

  ```
  > gpt init /dev/class/block/000
  ...
  > lsblk
  ID  DEV      DRV      SIZE TYPE           LABEL
  002 block    block     16G
  ```
 

 
 * Now that we have a GPT on this device, let's check what we can do with it. (NOTE: after manipulating the gpt, the device number may change. Use `lsblk`to keep track of how to refer to the block device). *现在我们已经在该设备上安装了GPT，让我们检查一下我们可以使用它做些什么。 （注意：操纵gpt后，设备号可能会更改。使用`lsblk`来跟踪如何引用块设备）。

  ```
  > gpt dump /dev/class/block/002
  blocksize=512 blocks=33554432
  Partition table is valid
  GPT contains usable blocks from 34 to 33554398 (inclusive)
  Total: 0 partitions
  ```
 

 
 * `gpt dump` tells us some important info: it tells us (1) How big blocks are, and (2) which blocks we can actually use.Let's fill part of the disk with a MinFS filesystem. *`gpt dump`告诉我们一些重要信息：它告诉我们（1）有多少大块，以及（2）我们可以实际使用的块。让我们用MinFS文件系统填充磁盘的一部分。

  ```
  > gpt add 34 20000000 minfs /dev/class/block/002
  ```
 

 
 * Within Zircon, format the partition as MinFS. Using `lsblk` you should see a block device which is the whole disk and a slightly smaller device whichis the partition. In the above output, the partition is device 003, and wouldhave the path `/dev/class/block/003` *在Zircon中，将分区格式化为MinFS。使用“ lsblk”，您应该看到一个块设备，它是整个磁盘，而一个较小的设备是分区。在上面的输出中，分区是设备003，并将具有路径`/ dev / class / block / 003`。

  ```
  > mkfs <PARTITION_PATH> minfs
  ```
 

 
 * If you want the device to be mounted automatically on reboot, use the GPT tool to set its type. As we did above, **you must** use `lsblk` **again**to locate the entry for the disk. We want to edit the type of the zero-thpartition.  Here we use the keyword 'fuchsia-data' to set the type GUID, butif you wanted to use an arbitrary GUID you would supply it where'fuchsia-data' is used. *如果要在重新启动时自动安装设备，请使用GPT工具设置其类型。和上面一样，**您必须**再次使用`lsblk`来找到磁盘的条目。我们要编辑零分区的类型。在这里，我们使用关键字'fuchsia-data'设置类型GUID，但是如果您想使用任意GUID，则可以在使用'fuchsia-data'的地方提供它。

  ```
  > gpt edit 0 type fuchsia-data <DEVICE_PATH>
  ```
 

 
 * On any future boots, the partition will be mounted automatically at `/data`.  *在以后的启动中，该分区将自动挂载在`/ data`处。

 
 * If you don't want the partition to be mounted automatically, you can update the visibility (or GUID) of the partition, and simply mount it manually. *如果您不希望自动安装该分区，则可以更新该分区的可见性（或GUID），而只需手动安装即可。

  ```
  > mount <PARTITION_PATH> /data
  ```
 

 
 * Any files written to `/data` (the mount point for this GUID) will persist across boots. To test this, try making a file on the new MinFS volume,rebooting, and observing it still exists. *写入`/ data`（此GUID的挂载点）的所有文件将在启动时保持不变。要对此进行测试，请尝试在新的MinFS卷上制作文件，重新启动，并观察其是否仍然存在。

  ```
  > touch /data/foobar
  > dm reboot
  > ls /data
  ```
 

 
 * To find out which block device/file system is mounted at each subdirectory under a given path, use the following command: *要找出在给定路径下的每个子目录中安装了哪个块设备/文件系统，请使用以下命令：

  ```
  > df <PATH>
  ```
