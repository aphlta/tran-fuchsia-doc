 
# Prepare a USB flash drive to be a bootable disk  准备USB闪存驱动器作为可引导磁盘 

These instructions prepare a USB flash drive to be a bootable disk for your device: this procedure only enables you to netboot or pave, it won't putanything on your internal storage. This USB flash drive can then direct yourdevice to boot from the freshly-built OS on your network-connected hostdevelopment machine (or alternately from the OS on the flash drive itself). 这些说明将USB闪存驱动器准备为设备的可引导磁盘：此过程仅使您能够进行网络引导或铺装，而不会在内部存储器上放任何东西。然后，此USB闪存驱动器可以指导您的设备从联网的主机开发计算机上的新构建的OS（或从闪存驱动器本身的OS）引导。

 
+ Execute `fx set x64` (if you haven't already)  +执行`fx set x64`（如果还没有的话）
+ Create a __zedboot__ key using, `fx mkzedboot /path/to/your/device`. The `mkzedboot` command does the following: +使用`fx mkzedboot / path / to / your / device`创建__zedboot__键。 `mkzedboot`命令执行以下操作：
  + Creates a FAT partition continaing an EFI System Partition, containing the Gigaboot EFI bootloader and a configuration that specifies to alwaysboot into Zedboot. +创建一个包含EFI系统分区的FAT分区，其中包含Gigaboot EFI引导加载程序和一个指定始终引导到Zedboot的配置。
  + Creates a ChromeOS bootable partition with a developer key signed Zedboot kernel partition. +创建一个带有开发人员签名的Zedboot内核分区的ChromeOS可启动分区。
+ On your host, run `fx build` (if you haven't already).  +在主机上，运行`fx build`（如果尚未安装）。
+ If you wish to install Fuchsia to the target device (modifying the target device harddisk), run `fx pave` on the host. IF you only wish to "netboot"the target device, and avoid modifying any disk state, run `fx netboot` onthe host instead. +如果您希望将紫红色安装到目标设备（修改目标设备硬盘），请在主机上运行`fx pave`。如果您只希望“ netboot”目标设备，并且避免修改任何磁盘状态，请在主机上运行“ fx netboot”。
+ Connect your device to your host via built-in ethernet, then power up the device. +通过内置以太网将设备连接到主机，然后打开设备电源。

 
## Manual Configuration  手动配置 

It is also relatively easy to manually create an EFI boot key with particular properites, though this will only boot on EFI systems. 手动创建具有特定属性的EFI引导密钥也相对容易，因为这样做只会在EFI系统上引导。

 
+ Format the USB key with a blank FAT partition.  +用空白的FAT分区格式化USB密钥。
+ Create a directory called `EFI/BOOT`.  +创建一个名为“ EFI / BOOT”的目录。
+ Copy `bootx64.efi` from `build-x64/bootloader` of a Zircon build into the above directory. +从Zircon版本的build-x64 / bootloader复制bootx64.efi到以上目录。
+ Copy `zircon.bin` from `build-x64` of a Zircon build into the root directory of the FAT partition. +将Zircon版本的build-x64中的zircon.bin复制到FAT分区的根目录中。
+ Copy `zedboot.bin` from `build-x64` of a Zircon build into the root directory of the FAT partition. +将Zircon版本的build-x64中的zedboot.bin复制到FAT分区的根目录中。
+ Optionally: Create a file called `cmdline` in the root fo the FAT partition. This file may contain any directives documented in[command line flags](/docs/reference/kernel/kernel_cmdline.md).The created disk will by default boot from zircon.bin instead of the network.At the Gigaboot screen, press 'm' to boot zircon vs 'z' for zedboot, or setthe default boot behavior with the `bootloader.default` flag in `cmdline`. +（可选）：在FAT分区的根目录中创建一个名为“ cmdline”的文件。该文件可能包含[命令行标志]（/ docs / reference / kernel / kernel_cmdline.md）中记录的任何指令。默认情况下，创建的磁盘将从zircon.bin而不是从网络启动。在Gigaboot屏幕上，按'm '来启动zircon vs'z'来进行zedboot，或者使用'cmdline'中的`bootloader.default`标志来设置默认的启动行为。

See also:  也可以看看：
* [Setting up the Acer device](acer12.md)  * [设置Acer设备]（acer12.md）
* [Setting up the NUC device](/docs/development/hardware/developing_on_nuc.md)  * [设置NUC设备]（/ docs / development / hardware / developing_on_nuc.md）
