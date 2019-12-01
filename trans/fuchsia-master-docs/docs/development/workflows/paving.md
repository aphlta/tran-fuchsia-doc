 
# Putting Fuchsia on a Device  将紫红色放在设备上 

One of the best ways to experience Fuchsia is by running it on actual hardware. This guide will help you get Fuchsia installed on your device. Fuchsia has goodsupport for a few different hardware platforms including the Acer Switch 12,Intel NUC, and Google Pixelbook (not to be confused with the Chromebook Pixel).The install process is not currently compatible with ARM-based targets. TheFuchsia install process, called 'paving', requires two machines, the machine onwhich you want to run Fuchsia ("target") and the machine on which you buildFuchsia ("host"). Host and target must be able to communicate over a local areanetwork. On your host system you will build Fuchsia, create a piece of installmedia, and stream a large portion of the system over the network to the target. 体验紫红色的最好方法之一是在实际硬件上运行它。本指南将帮助您在设备上安装紫红色。 Fuchsia对Acer Switch 12，Intel NUC和Google Pixelbook（不要与Chromebook Pixel混淆）等几种不同的硬件平台提供良好的支持。安装过程当前与基于ARM的目标不兼容。紫红色的安装过程称为“铺路”，需要两台机器，要在其上运行紫红色的计算机（“目标”）和要在其上构建紫红色的计算机（“主机”）。主机和目标必须能够通过局域网进行通信。在您的主机系统上，您将构建Fuchsia，创建一个installmedia，然后将大部分系统通过网络流式传输到目标。

The `fx` command will be used throughout these instructions. If you have fx mapped into your command path you can follow the instructions verbatim. If youdon't have fx in your path, it can be found at `//scripts/fx` and you'll needto use the appropriate relative path in the supplied commands. Many of fxcommands are relatively thin wrappers around build actions in GN coupled withtool invocations. If your use case isn't quite served by what's currentlyavailable there may a few GN targets you can build or some GN templates you canextend to allow you to build what you need. 在这些说明中将使用`fx`命令。如果已将fx映射到命令路径，则可以逐字遵循说明。如果您的路径中没有fx，可以在`// scripts / fx`中找到它，并且需要在提供的命令中使用适当的相对路径。许多fxcommands是GN中与工具调用相结合的构建动作的相对较薄的包装器。如果您的用例不能完全满足当前的需求，则可以构建一些GN目标，或者可以扩展一些GN模板以构建所需的对象。

 
## TL;DR  TL; DR 

Read this all before? See the [quickstart guide](build_and_pave_quickstart.md)for a workflow summary. 都读完了吗？有关工作流摘要，请参见[快速入门指南]（build_and_pave_quickstart.md）。

 
## Building {#building}  建筑{building} 

Detailed instructions for obtaining and building Fuchsia are available from the [Getting Started](/docs/getting_started.md) guide, but we'll assume here that thetarget system is x86-based and that you want to build a complete system. Toconfigure our build for this we can run `fx set {product_name}.x64` and then build with`fx build`. For Pixelbook, rather than using the x64 build, you need to specify theChromebook board. Example: `fx set core.chromebook-x64`. 可从[Getting Started]（/ docs / getting_started.md）指南中获得有关获取和构建紫红色的详细说明，但是在此我们假定目标系统是基于x86的，并且您要构建一个完整的系统。要为此配置构建，我们可以运行`fx set {product_name} .x64`，然后使用`fx build`进行构建。对于Pixelbook，您需要指定Chromebook板，而不是使用x64构建。例如：`fx set core.chromebook-x64`。

 
## Creating install media {#creating-install-media}  创建安装媒体{creating-install-media} 

To create your install media we recommend using a USB drive since these are well-supported as boot media by most systems. Note that the install mediacreation process **will wipe everything** from the USB drive being used. Insert theUSB drive and then run `fx mkzedboot <device_path>`, which on Linux istypically something like /dev/sd&lt;X&gt; where X is a letter and on Mac is typicallysomething like /dev/disk&lt;N&gt; where 'N' is a number. **Be careful not to selectthe wrong device**. Once this is done, remove the USB drive. 要创建您的安装媒体，我们建议您使用USB驱动器，因为大多数系统都将它们作为启动媒体予以支持。请注意，安装介质创建过程将**擦除正在使用的USB驱动器中的所有内容**。插入USB驱动器，然后运行`fx mkzedboot <device_path>`，在Linux上通常类似/ dev / sdlt; Xgt;。其中X是字母，在Mac上通常是/ dev / disklt; Ngt;其中“ N”是数字。 **请注意不要选择错误的设备**。完成此操作后，卸下USB驱动器。

 
## Paving {#paving}  铺路{铺路} 

Now we'll build the artifacts to transfer over the network during the paving process. What is transferred is dependent on the target device. For UEFI basedsystems (like Intel NUC or Acer Switch 12) our output target type is 'efi'. ForChromeOS-based systems (like Pixelbook) that use vboot-format images, the targettype is 'vboot'. To start the bootserver with the correct image just run `fx pave`. 现在，我们将构建工件以在摊铺过程中通过网络传输。传输的内容取决于目标设备。对于基于UEFI的系统（例如Intel NUC或Acer Switch 12），我们的输出目标类型为'efi'。对于使用vboot格式图像的基于ChromeOS的系统（例如Pixelbook），目标类型为“ vboot”。要以正确的映像启动引导服务器，只需运行`fx pave`。

Insert the install media into the target device that you want to pave. The target device's boot settings may need to be changed to boot from the USB device andthis is typically device-specific. For the guides listed below, **only** gothrough the steps to set the boot device, don't continue with any instructions oncreating install media. 将安装媒体插入要铺装的目标设备。目标设备的启动设置可能需要更改才能从USB设备启动，这通常是特定于设备的。对于下面列出的指南，“仅” **仅执行设置引导设备的步骤，不要继续任何有关创建安装介质的说明。

 
* [Acer Switch Alpha 12](/docs/development/hardware/acer12.md)  * [Acer Switch Alpha 12]（/ docs / development / hardware / acer12.md）
* [Intel NUC](/docs/development/hardware/developing_on_nuc.md)  * [Intel NUC]（/ docs / development / hardware / developing_on_nuc.md）
* [Google Pixelbook](/docs/development/hardware/pixelbook.md)  * [Google Pixelbook]（/ docs / development / hardware / pixelbook.md）

Paving should occur automatically after the device is booted into Zedboot from the USB drive. After the paving process completes, the system should boot into theZircon kernel. After paving, the whole system is installed on internal storage. Atthis point the USB key can be removed since the system has everything it needsstored locally. If you plan to re-pave frequently it may be useful to keep theUSB drive inserted so your system boots into Zedboot by default where pavingwill happen automatically. After the initial pave on UEFI systems that useGigaboot, another option for re-paving is to press 'z' while in Gigaboot toselect Zedboot. For vboot-based systems using the USB drive is currently theonly option for re-paving. In all cases the bootserver needs to have beenstarted with `fx pave` 从USB驱动器将设备引导到Zedboot之后，应自动进行铺路。铺装过程完成后，系统应启动进入Zircon内核。铺装后，整个系统将安装在内部存储器上。此时，由于系统已将其需要的所有内容存储在本地，因此可以删除USB密钥。如果您打算经常重新铺砌，则保持插入USB驱动器的状态可能很有用，这样您的系统默认情况下会引导进入Zedboot，在此情况下铺砌将自动进行。在使用Gigaboot的UEFI系统上进行初始铺装后，另一种重新铺装的方法是在Gigaboot中按“ z”以选择Zedboot。对于使用USB驱动器的基于vboot的系统，当前是重新铺设的唯一选项。在所有情况下，引导服务器都必须使用`fx pave`启动。

 
## Troubleshooting {#troubleshooting}  疑难解答{疑难解答} 

In some cases paving may fail because you have a disk layout that is incompatible. In these cases you will see a message that asks you to run'install-disk-image wipe'. If it is incompatible because it contains an olderFuchsia layout put there by installer (vs the paver) you can fix this by killingthe fx pave process on the host, switching to a different console (Alt+F3) onthe target, and running `install-disk-image wipe`. Then reboot the target,re-run `fx pave` on the host, and the pave should succeed. 在某些情况下，由于磁盘布局不兼容，铺装可能会失败。在这些情况下，您将看到一条消息，要求您运行“安装磁盘映像擦除”。如果它不兼容，因为它包含安装程序（与摊铺机）放置的较旧的紫红色布局，则可以通过终止主机上的fx铺装过程，切换到目标上的另一个控制台（Alt + F3）并运行`install-来解决此问题。磁盘映像擦除。然后重新启动目标，在主机上重新运行“ fx pave”，并且铺装应该成功。

In some cases paving may fail on an Acer with some error indicating "couldn't find space in gpt". In these cases (as long as you don't want to keep the otherOS, i.e. Windows, parts) run `lsblk` and identify the partition that isn't yourUSB (it shouldn't have RE in the columns). Identify the number in the firstcolumn for your partition (likely to be either 000 or 003). Then run`gpt init /dev/class/block/N` where N is the number previously identified. Thiswill clear all Windows partitions from the disk. Once this is done, reboot intozedboot and paving should work. 在某些情况下，Acer的铺装可能会失败，并显示“无法在gpt中找到空间”的错误。在这些情况下（只要您不想保留其他操作系统，即Windows，部件）运行`lsblk`并识别不是USB的分区（列中不应包含RE）。在分区的第一列中标识数字（可能是000或003）。然后运行gpt init / dev / class / block / N`，其中N是先前确定的数字。这将从磁盘上清除所有Windows分区。完成此操作后，将其重新引导到zedboot并进行铺路即可。

 
## Changing boot target (localboot, netboot, etc) default  更改引导目标（本地引导，网络引导等）默认值 

