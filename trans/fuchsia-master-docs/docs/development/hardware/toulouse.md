 
# Toulouse  图卢兹 

Toulouse is a nickname for a [Jetway PC](http://www.jetwayipc.com/product/hbjc130f731-series/) that Fuchsia developers use as a platform for writing networking software. It has multiple ethernet portsand mini-PCIe ports for adding wireless network adapters. 图卢兹是[Jetway PC]（http://www.jetwayipc.com/product/hbjc130f731-series/）的昵称，Fuchsia开发人员将其用作编写网络软件的平台。它具有多个以太网端口和mini-PCIe端口，用于添加无线网络适配器。

 
## Toulouse Setup & Configuration  图卢兹设置配置 

You will need:  你会需要：

 
- Toulouse hardware  -图卢兹硬件
- Power supply (included with Toulouse)  -电源（图卢兹附带）
- Ethernet cable(s)  -以太网电缆
- USB stick to get started  -USB记忆棒开始
- At least one of:  -至少之一：
  - Serial cable (e.g., StarTech USB null modem cable)  -串行电缆（例如，StarTech USB空调制解调器电缆）
  - HDMI + USB keyboard  -HDMI + USB键盘

Tested Wifi/Bluetooth adapters include:  经过测试的Wifi /蓝牙适配器包括：

 
* QCA6174A  * QCA6174A
* QCA9880  * QCA9880

In your `fx set` commandline, add the following arguments:  在您的`fx set`命令行中，添加以下参数：

 
* `--board "garnet/boards/toulouse.gni"`  *`--board“ garnet / boards / toulouse.gni”`
* `--product "garnet/products/toulouse.gni"`  *`-产品“石榴石/产品/toulouse.gni”`
* [optional] `--args "always_zedboot=true"`  * [可选]`--args“ always_zedboot = true”`

The last option will always boot to zedboot instead of booting off the paved image. You have to press 'm' before the timeout if you want to boot from disk, or re-pave without'always_zedboot=true'. One possible workaround is to use 'always_zedboot=true' when preparing theUSB stick, and leaving the USB stick in when you want to netboot. Without the USB stick it will runoff disk. 最后一个选项将始终引导到zedboot而不是引导已铺好的映像。如果要从磁盘引导，则必须在超时前按'm'，否则，如果不使用'always_zedboot = true'重新进行铺装。一种可能的解决方法是在准备USB记忆棒时使用'always_zedboot = true'，而在要进行网络引导时使用USB记忆棒。没有USB记忆棒，它将使磁盘溢出。

By default the device boots from the internal storage first, and you cannot set USB drives as a generic default. 默认情况下，设备会先从内部存储启动，并且您无法将USB驱动器设置为通用默认设置。

Prepare a USB drive, using `fx mkzedboot` (see the [docs](usb_setup.md) for details, and see above for how to make a USB stick that can netboot). 使用`fx mkzedboot`准备USB驱动器（有关详细信息，请参见[docs]（usb_setup.md），有关如何制作可以进行网络引导的USB闪存，请参见上文）。

Insert the USB drive before powering on the device. Note: if the drive isn’t recognized, try using the other USB port. Some ports are flaky. 在打开设备电源之前，请插入USB驱动器。注意：如果无法识别驱动器，请尝试使用其他USB端口。一些端口是片状的。

On boot, press Esc or Del to enter the BIOS. This works over serial as well once the serial console is enabled (see below). 在启动时，按Esc或Del键进入BIOS。启用串行控制台后，这也可以在串行上运行（请参见下文）。

In the "Boot" section, find the entry for USB UEFI and use the '+' key to move it to the top of the list. Press F4 to save and reset. 在“启动”部分中，找到USB UEFI的条目，然后使用“ +”键将其移至列表顶部。按F4保存并重置。

To use the serial port on Debian/Ubuntu Linux, you may need to remove the 'brltty' program that wants to take over every serial port: `sudo apt-get remove brltty`. You will need to unplug/replugyour serial cable after this to get it to work. 要在Debian / Ubuntu Linux上使用串行端口，您可能需要删除要接管每个串行端口的'brltty'程序：`sudo apt-get remove brltty`。之后，您需要拔下/重新插入串行电缆，以使其正常工作。

 
## Serial consoles  串行控制台 

 
### Enabling serial for the BIOS  为BIOS启用串行 

In the "Advanced" section, open the "Serial Port Console Redirection" settings. Enable "Console Redirection" and ensure the "Console Redirection Settings" look similar to the following. (You maytune these to taste, if you know what you're doing.) 在“高级”部分，打开“串行端口控制台重定向”设置。启用“控制台重定向”，并确保“控制台重定向设置”与以下内容类似。 （如果您知道自己在做什么，则可以调整它们的口味。）

 
* Terminal Type: VT-UTF8  *端子类型：VT-UTF8
* Bits per second: 115200  *每秒位数：115200
* Data Bits: 8  *数据位：8
* Parity: None  *奇偶校验：无
* Stop Bits: 1  *停止位：1
* Flow Control: Off  *流量控制：关闭

The other settings may be left at their default values.  其他设置可以保留为默认值。

 
### Example Linux serial consoles (assumes a serial device at /dev/ttyUSB0)  示例Linux串行控制台（假设串行设备位于/ dev / ttyUSB0） 
* screen /dev/ttyUSB0 115200  *屏幕/ dev / ttyUSB0 115200
* picocom -b 115200 /dev/ttyUSB0  * picocom -b 115200 / dev / ttyUSB0
* miniterm.py /dev/ttyUSB0 115200  * miniterm.py / dev / ttyUSB0 115200
* minicom -o -t vt100 -b 115200 -D /dev/ttyUSB0  (Supports control chars. Use Ctrl+a q to quit)  * minicom -o -t vt100 -b 115200 -D / dev / ttyUSB0（支持控制字符。使用Ctrl + a q退出）

 
### Serial console on MacOS  MacOS上的串行控制台