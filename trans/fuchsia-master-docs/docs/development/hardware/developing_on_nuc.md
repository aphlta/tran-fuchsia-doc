 
# Install Fuchsia on a NUC  在NUC上安装紫红色 

This document describes how to get a NUC up and running with Fuchsia.  本文档介绍了如何通过Fuchsia启动和运行NUC。

[TOC]  [目录]

 
## 1. Get Parts {#get-parts}  1.获取零件{get-parts} 

You need the following:  您需要以下内容：

 
- USB 3.0 Drive  -USB 3.0驱动器
- NUC  -NUC
- RAM  - 内存
- m.2 SSD  -m.2 SSD
- Keyboard  -键盘
- Mouse  - 老鼠
- Monitor that supports HDMI  -支持HDMI的显示器
- HDMI cable  -HDMI线
- ethernet cable  - 以太网电缆
- Magnetic tip phillips head screwdriver.  -磁性尖头十字螺丝刀。

This table shows what I bought from Amazon.  该表显示了我从亚马逊购买的商品。

| Item | Link | Notes: | | ---- | ---- | ------ || NUC | [B01MSZLO9P](https://www.amazon.com/gp/product/B01MSZLO9P) | Get a NUC7 (Kaby Lake) or NUC6 (Skylake) for GPU support. || RAM | [B01BIWKP58](https://www.amazon.com/gp/product/B01BIWKP58) | Works fine. || SSD | [B01IAGSDJ0](https://www.amazon.com/gp/product/B01IAGSDJ0) | Works fine. You only need one of these SSDs. || SSD | [B00TGIVZTW](https://www.amazon.com/gp/product/B00TGIVZTW) | Works fine. || SSD | [B01M9K0N8I](https://www.amazon.com/gp/product/B01M9K0N8I) | Works fine. || **Optional:** | | || Keyboard and Mouse | [B00B7GV802](https://www.amazon.com/gp/product/B00B7GV802) | Works fine.  Next time I'd get a keyboard with a smaller foot print. || Monitor | [B015WCV70W](https://www.amazon.com/gp/product/B015WCV70W) | Works fine. || HDMI Cable | [B014I8SIJY](https://www.amazon.com/gp/product/B014I8SIJY) | Works fine. || USB 3.0 drive | [B01BGTG41W](https://www.amazon.com/gp/product/B01BGTG41W) | Works fine. | |项目|友情链接注意： | ---- | ---- | ------ || NUC | [B01MSZLO9P]（https://www.amazon.com/gp/product/B01MSZLO9P）|获取NUC7（Kaby Lake）或NUC6（Skylake）以获得GPU支持。 ||内存[B01BIWKP58]（https://www.amazon.com/gp/product/B01BIWKP58）|工作正常。 ||固态硬盘| [B01IAGSDJ0]（https://www.amazon.com/gp/product/B01IAGSDJ0）|工作正常。您仅需要这些SSD之一。 ||固态硬盘| [B00TGIVZTW]（https://www.amazon.com/gp/product/B00TGIVZTW）|工作正常。 ||固态硬盘| [B01M9K0N8I]（https://www.amazon.com/gp/product/B01M9K0N8I）|工作正常。 || **可选：** | | ||键盘和鼠标| [B00B7GV802]（https://www.amazon.com/gp/product/B00B7GV802）|工作正常。下次我会得到一个脚印较小的键盘。 ||监控器[B015WCV70W]（https://www.amazon.com/gp/product/B015WCV70W）|工作正常。 || HDMI电缆| [B014I8SIJY]（https://www.amazon.com/gp/product/B014I8SIJY）|工作正常。 || USB 3.0驱动器| [B01BGTG41W]（https://www.amazon.com/gp/product/B01BGTG41W）|工作正常。 |

 
## 2. Prepare the NUC {#prepare-the-nuc}  2.准备NUC {prepare-the-nuc} 

NUCs don’t come with RAM or an SSD, so you need to install them.  NUC没有RAM或SSD，因此您需要安装它们。

<img width="50%" src="/docs/images/developing_on_nuc/parts.jpg"/>  <img width =“ 50％” src =“ / docs / images / developing_on_nuc / parts.jpg” />

Follow the instructions to install the RAM and SSD on the NUC:  按照说明在NUC上安装RAM和SSD：

 
1. Remove the phillips screws in the bottom feet of the NUC.  1.卸下NUC底脚上的十字螺丝。

   <img width="50%" src="/docs/images/developing_on_nuc/nuc_bottom.jpg"/> <img width="50%" src="/docs/images/developing_on_nuc/nuc_inside.jpg"/> <img width =“ 50％” src =“ / docs / images / developing_on_nuc / nuc_bottom.jpg” /> <img width =“ 50％” src =“ / docs / images / developing_on_nuc / nuc_inside.jpg” />
1. Install the RAM.  1.安装RAM。
1. Remove the phillips screw that will hold the SSD in place (phillips screwdriver with magnetic tip is useful here).  1.卸下将SSD固定到位的菲利普斯螺丝（在这里，带磁性尖端的菲利普斯螺丝刀非常有用）。
1. Install the SSD.  1.安装SSD。
1. Screw the SSD in place using screw from Step 3.  1.使用步骤3中的螺钉将SSD固定到位。

   <img width="50%" src="/docs/images/developing_on_nuc/parts_installed.jpg"/>  <img width =“ 50％” src =“ / docs / images / developing_on_nuc / parts_installed.jpg” />
1. Replace bottom and screw feet back in.  1.装回底部，然后重新拧上支脚。
1. (Optional) Apply fuchsia logo.  1.（可选）应用紫红色徽标。

   <img width="50%" src="/docs/images/developing_on_nuc/nuc_fuchsia.jpg"/>  <img width =“ 50％” src =“ / docs / images / developing_on_nuc / nuc_fuchsia.jpg” />
1. Plug power, ethernet, HDMI, keyboard, and mouse into NUC.  1.将电源，以太网，HDMI，键盘和鼠标插入NUC。

 
## 3. Enable EFI booting {#enable-efi-booting}  3.启用UEFI引导{enable-uefi-booting} 

 
1. Reboot NUC.  1.重新启动NUC。
1. Press F2 while booting to enter BIOS.  1.在启动时按F2键进入BIOS。
1. In the Boot Order window on the left, click the Legacy tab.  1.在左侧的“启动顺序”窗口中，单击“旧版”选项卡。
1. Uncheck ‘Legacy Boot’.  1.取消选中“旧版启动”。

   <img width="50%" src="/docs/images/developing_on_nuc/bios.jpg"/>  <img width =“ 50％” src =“ / docs / images / developing_on_nuc / bios.jpg” />
1. Click the `Advanced` button and confirm the following boot configuration:  1.单击“高级”按钮并确认以下启动配置：
    1. Select the `Boot Priority` tab.  1.选择“启动优先级”标签。
       1. Check `UEFI Boot`.  1.检查“ UEFI引导”。
       1. Set `USB` the first entry in the boot order.  1.将“ USB”设置为引导顺序中的第一项。
    1. Select the `Boot configuration` tab.  1.选择“启动配置”标签。
       1. Check `Boot Network Devices Last`.  1.选中“最后启动网络设备”。
       1. Check `Unlimited Network Boot Attepts`.  1.检查“无限网络启动尝试”。
       1. Check `USB boot devices`.  1.检查“ USB启动设备”。
       1. Set `Network boot` to `UEFI PXE & iSCSI`.  1.将“网络启动”设置为“ UEFI PXE iSCSI”。
2. Select the `Secure Boot` tab and uncheck `Secure Boot`.  2.选择“安全启动”标签，然后取消选中“安全启动”。
3. Press F10 to save the changes and exit BIOS.  3.按F10保存更改并退出BIOS。

Note: Network booting only works with the NUC's *built-in* ethernet, netbooting via USB-ethernet dongle is unsupported. 注意：网络启动仅适用于NUC的*内置*以太网，不支持通过USB-以太网加密狗进行网络启动。

If you want to remotely manage the device, see [Remote Management for NUC](nuc-remote-management.md).  如果要远程管理设备，请参阅[NUC远程管理]（nuc-remote-management.md）。

 
## 4. Build Fuchsia {#build-fuchsia}  4.构建紫红色{build-fuchsia} 

 
1. Follow the [getting started guidelines](/docs/getting_started.md). Make sure to use the board configuration `x86` when running `fx set`. For example `fx set core.x86`. 1.请遵循[入门指南]（/ docs / getting_started.md）。运行`fx set`时，请确保使用板配置`x86`。例如`fx set core.x86`。

 
## 5. Pave Fuchsia {#pave-fuchsia}  5.铺紫红色{pave-fuchsia} 

 
1. Plug in your USB key to your build workstation.  1.将USB密钥插入构建工作站。
1. Identify the path to your USB key by running `fx list-usb-disks`.  1.通过运行“ fx list-usb-disks”来确定USB密钥的路径。
1. Create a Zedboot USB by running `fx mkzedboot /path/to/usb/disk`.  1.通过运行fx mkzedboot / path / to / usb / disk创建一个Zedboot USB。
1. Plug the Zedboot USB key into the NUC and boot it.  1.将Zedboot USB密钥插入NUC并启动它。
1. When Zedboot is started, press Alt+F3 to switch to a command line prompt.  1.启动Zedboot时，按Alt + F3切换到命令行提示符。
1. Run `lsblk` on the device. Take note of the HDD or SSD's device path.  1.在设备上运行“ lsblk”。记下HDD或SSD的设备路径。
    1. An example path looks like `/dev/sys/pci/00:17.0/ahci/sata0/block`  1.一个示例路径如下所示：/dev/sys/pci/00:17.0/ahci/sata0/block
1. Run `install-disk-image init-partition-tables --block-device <BLOCK_DEVICE_PATH>` on the device.  1.在设备上运行“ install-disk-image初始化分区表--block-device <BLOCK_DEVICE_PATH>”。
