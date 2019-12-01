 
# Build and Pave Quickstart  建立并铺装快速入门 

This document captures the common-case workflow for building and deploying Fuchsia onto a device using `fx` development commands. Most such commandshave options for less common situations; see `fx help <command>` for details. 本文档介绍了使用fx开发命令将紫红色构建和部署到设备上的常见工作流程。对于不太常见的情况，大多数此类命令共享选项；有关详细信息，请参见`fx help <command>`。

 
## Initial Build and Deploy  初始构建和部署 

The initial build and deploy workflow using `fx` is as follows:  使用`fx`的初始构建和部署工作流程如下：

 
1.  `fx set core.x64` Configures the build to build the "core" product on a generic x64 board.See `fx list-products` and `fx list-boards` for lists of available productsand boards, respectively. 1.`fx set core.x64`配置构建以在通用x64板上构建“核心”产品。有关可用产品和板的列表，请分别参见“ fx list-products”和“ fx list-boards”。
1.  `fx build` Builds Zircon, then the rest of Fuchsia. 1.`fx build`构建Zircon，然后构建紫红色的其余部分。
1.  `fx mkzedboot <usb_drive_device_path>` Builds the Zedboot media and installs to the USB drive target. See belowfor notes on obtaining the USB drive device path. 1.`fx mkzedboot <usb_drive_device_path>`生成Zedboot介质并安装到USB驱动器目标。有关获取USB驱动器设备路径的说明，请参见下文。
1.  Attach Zedboot USB to device and reboot.  1.将Zedboot USB连接到设备并重新启动。
1.  Run `lsblk` on the device. Take note of the HDD or SSD's device path.  1.在设备上运行“ lsblk”。记下HDD或SSD的设备路径。
    1. An example path looks like `/dev/sys/pci/00:17.0/ahci/sata0/block`  1.一个示例路径如下所示：/dev/sys/pci/00:17.0/ahci/sata0/block
1.  Run `install-disk-image init-partition-tables <BLOCK_DEVICE_PATH>` on the device.  1.在设备上运行`install-disk-image init-partition-tables <BLOCK_DEVICE_PATH>`。
1.  Run `fx pave` on your workstation. Starts the bootserver. The bootserver connects to the device to upload the pave image,and then paves the device. 1.在工作站上运行“ fx pave”。启动引导服务器。引导服务器连接到设备上载铺装映像，然后铺装设备。

 
### USB drive device path  USB驱动器设备路径 

Instructions for determining the correct path to your USB drive are as follows, depending on the host OS. In either case, you can run the command once with theUSB drive disconnected, then run again with it connected, to see thedifference. 根据主机操作系统，有关确定USB驱动器正确路径的说明如下。在这两种情况下，您都可以在USB驱动器断开连接的情况下运行一次命令，然后在连接USB驱动器的情况下再次运行该命令，以查看差异。

 
* Linux users:  * Linux用户：
  - `sudo fdisk -l` Drives are usually of the form /dev/sd[x], e.g. '/dev/sdc'. Selectthe drive rather than a specific partition. -`sudo fdisk -l`驱动器通常采用/ dev / sd [x]的形式，例如'/ dev / sdc'。选择驱动器而不是特定的分区。
* Mac users:  * Mac用户：
  - `diskutil list | grep external` Drives are usually of the form /dev/disk[n], e.g. '/dev/disk2'. -`diskutil列表| grep external`驱动器通常采用/ dev / disk [n]的形式，例如'/ dev / disk2'。
  - If you see 'ERROR: Can't open /dev/disk[n]: Resource busy' then you will have to unmount the usb drive.For this run `hdiutil unmount /dev/disk[n]`.If this does not fix the error, try reformating the drive:`diskutil eraseDisk JHFSX <name_of_the_usb_stick> /dev/disk[n]`. -如果看到“错误：无法打开/ dev / disk [n]：资源繁忙”，则必须卸载USB驱动器。为此，请运行“ hdiutil unmount / dev / disk [n]”。要解决错误，请尝试重新格式化驱动器：`diskutil擦除磁盘JHFSX <名称_usb_stick> / dev / disk [n]。

 
## Subsequent Build and Deploy  随后的构建和部署 

The workflow for re-building and re-deploying using `fx` is slightly different:  使用`fx`进行重建和重新部署的工作流程略有不同：

 
1.  Check the [build dashboard](https://luci-milo.appspot.com/p/fuchsia). Helps ensure that HEAD is in a good state to pull. 1.检查[构建仪表板]（https://luci-milo.appspot.com/p/fuchsia）。帮助确保HEAD处于良好的可拉状态。
1.  `jiri update` Fetches the latest code. 1.`jiri update`获取最新代码。
1.  `fx build` Builds Zircon, then the rest of Fuchsia. 1.`fx build`构建Zircon，然后构建紫红色的其余部分。
1.  `fx setup-macos` Sets up firewall rules (Mac users ONLY)  1.`fx setup-macos`设置防火墙规则（仅Mac用户）
1.  `fx serve` Starts a development package server on the host. 1.`fx serve`在主机上启动开发包服务器。
1.  Boot the device *without* Zedboot USB attached. Boots the device into its last-paved state. 1.引导设备*未连接* Zedboot USB。将设备引导到其最后铺砌的状态。
1.  `fx ota` Pushes updated packages to the device. 1.`fx ota`将更新的软件包推送到设备。

Note: If desired, the device can be re-paved using Zedboot USB as per steps 4-5 in the previous section. This is slower, but may be necessary in some caseswhere the system handles the OTA less than gracefully. 注意：如果需要，可以按照上一节中的步骤4-5使用Zedboot USB重新铺设设备。这速度较慢，但​​是在某些情况下，系统对OTA的处理不够优雅。

 
## Troubleshooting  故障排除 

 
