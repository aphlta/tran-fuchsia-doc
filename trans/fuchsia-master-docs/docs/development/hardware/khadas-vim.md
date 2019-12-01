 
# Zircon on Khadas VIM2 Board  卡达斯VIM2板上的锆石 

This document describes running Zircon on the Khadas VIM2 board. Additional documentation can be found at [docs.khadas.com](http://docs.khadas.com/) 本文档介绍了在Khadas VIM2板上运行Zircon的过程。可以在[docs.khadas.com]（http://docs.khadas.com/）上找到其他文档。

When describing the location of buttons, pins and other items on the board, we will refer to the side with the USB, ethernet and HDMI connectors as the front of the boardand the opposite side the back of the board. 在描述板上的按钮，引脚和其他项目的位置时，我们将带有USB，以太网和HDMI连接器的一侧称为板的正面，将其相对的另一侧称为板的背面。

 
## Heat Sink  散热器 

Before you start, you need a heat sink. A passive chip heat sink will allow you to run 2 cores out of 8 at full speed before reaching 80C, the criticaltemperature at which cores have to be throttled down. 在开始之前，您需要一个散热器。无源芯片散热器可让您在达到80C（必须降低内核温度的临界温度）之前，全速运行8个内核中的2个。

 
## Setup  设定 

 
- USB C port: Connect to host. Provides power and `fastboot`.  -USB C端口：连接到主机。提供电源和“ fastboot”。
- Ethernet: Connect cable directly to board (do not use a USB ethernet adapter).  -以太网：将电缆直接连接到板（请勿使用USB以太网适配器）。
- HDMI: Optional. Connects to display.  -HDMI：可选。连接到显示器。
- Serial Console: Optional but very useful. See next section.  -串行控制台：可选，但非常有用。请参阅下一节。

 
## Serial Console  串行控制台 

The debug UART for the serial console is exposed on the 40 pin header at the back of the board. You may use a 3.3v FTDI USB to serial cable to access the serial console.On the front row of the header: 串行控制台的调试UART暴露在板背面的40针接头连接器上。您可以使用3.3v FTDI USB转串行电缆访问串行控制台。在标题的第一行上：

 
- 2nd from right: TX (Yellow wire)  -右二：TX（黄线）
- 3rd from right: RX (Orange wire)  -从右至第3：RX（橙色线）
- 4th from right: Ground (Black wire)  -从右至第4：地线（黑线）

For FTDI serial cables with black, white, red and green wires, use this:  对于带有黑，白，红和绿线的FTDI串行电缆，请使用以下命令：

 
- 2nd from right: TX (White wire)  -右二：TX（白线）
- 3rd from right: RX (Green wire)  -右三：RX（绿线）
- 4th from right: Ground (Black wire)  -从右至第4：地线（黑线）

In [this diagram](http://docs.khadas.com/vim1/GPIOPinout.html) of the 40 pin header, these correspond to pins 17 through 19. 在40针接头连接器的[此图]（http://docs.khadas.com/vim1/GPIOPinout.html）中，它们对应于针脚17至19。

 
## Buttons  纽扣 

The VIM2 has 3 buttons on the left side of the board. On the board schematic, SW1 (switch closest to the USB plug) is the reset switch. SW3 (farthest away from the USB plug on the schematic) can be used for entering flashing mode. If SW3 is held down while the board is reset or power cycled , the bootloader will enter flashing mode instead of booting the kernel normally.  VIM2在板子的左侧有3个按钮。在电路板上，SW1（最靠近USB插头的开关）是复位开关。 SW3（距离原理图上的USB插头最远）可用于进入闪烁模式。如果在复位或重启电源时按住SW3，则引导加载程序将进入闪烁模式，而不是正常引导内核。

 
## VIM2 Bootloader  VIM2引导程序 

Booting Zircon on the VIM2 requires a custom bootloader.  在VIM2上引导Zircon需要自定义引导程序。

 
### [Googlers only]  [仅限Google员工]Within Google, this can be found at [go/vim2-bootloader](http://go.corp.google.com/vim2-bootloader). Download the .bin file and follow the instructions in the document.  在Google中，可以在[go / vim2-bootloader]（http://go.corp.google.com/vim2-bootloader）中找到该文件。下载.bin文件，然后按照文档中的说明进行操作。

If you are not at Google, hang on until we make this publicly available.  如果您不在Google，请耐心等待，直到我们将其公开。

To find out what version of the bootloader you have, grep for "zircon-bootloader" in the kernel boot log. You should see something like: "cmdline: zircon-bootloader=0.11" 要找出您所使用的引导加载程序的版本，请在内核引导日志中使用grep表示“ zircon-bootloader”。您应该看到类似“ cmdline：zircon-bootloader = 0.11”的内容。

 
## Building  建造 

```
fx set bringup.vim2
fx build
```
 

Be sure you've already set up your network before proceeding to the next step.  在继续下一步之前，请确保您已经设置了网络。

 
## Flashing & Paving  摊铺机 

First enter fastboot mode by holding down SW3 (leftmost button), pressing SW1 (rightmost button) quickly and keeping pressing SW3 for a few seconds.  首先按住SW3（最左边的按钮），快速按下SW1（最右边的按钮）并持续按住SW3几秒钟，进入快速启动模式。

```
fx flash --pave
```
 

In order to get into zedboot you can reboot into the recovery:  为了进入zedboot，您可以重新引导进入恢复：

```
dm reboot-recovery
```
 

Alternatively, you can get to zedboot by resetting your vim2 by pressing SW1(rightmost button) quickly and keeping pressing SW2 for a few seconds.  另外，您可以通过快速按下SW1（最右边的按钮）并按住SW2几秒钟来重置vim2，从而进入zedboot。

 
### netbooting  网络启动 

```
fx set bringup.vim2 --netboot && fx build && fx netboot -1
```
 

You should be able to see "Issued boot command to ..." message printed out if this step is successful.  如果此步骤成功，您应该能够看到“已将启动命令发布给...”消息。

 
### Paving  铺路 

Paving is available from the "core" product and above. Run the following under the fuchsia directory:  摊铺可从“核心”产品及以上的产品中获得。在紫红色目录下运行以下命令：

```
fx set core.vim2 && fx build && fx pave -1
```
 

 
### Fuchsia logo  紫红色徽标 

To update the boot splash screen to be the Fuchsia logo, do this in fastboot mode:  要将引导启动屏幕更新为紫红色徽标，请在快速引导模式下执行以下操作：

```
fastboot flash logo kernel/target/arm64/board/vim2/firmware/logo.img
```
