 
#  Zircon on HiKey960 (96boards.org)  Zircon在HiKey960（96boards.org）上Periodically check this file as the setup workflow will change/improve.  定期检查此文件，因为设置工作流程将更改/改进。

 

 
## Requirements  要求 

__The following hardware is required:__  __需要以下硬件：__

 
+ HiKey960 board  + HiKey960板
+ Power adapter (most will require a DC plug converter -- more info [here](http://www.96boards.org/product/hikey960/)) +电源适配器（大多数将需要DC插头转换器-更多信息[此处]（http://www.96boards.org/product/hikey960/））
+ USB-C cable (to connect to workstation for flashing the board)  + USB-C电缆（用于连接工作站以刷新板）
+ One of the following (to connect to workstation for serial console):  +以下之一（用于连接到串行控制台的工作站）：
  + (Recommended) [Mezzanine board](https://www.seeedstudio.com/96Boards-UART-p-2525.html),plus a micro-USB cable (not included with mezzanine board), or +（推荐）[Mezzanine板]（https://www.seeedstudio.com/96Boards-UART-p-2525.html），外加micro-USB电缆（夹层板不附带），或
  + (Alternate) [1.8v FTDI Serial Adapter cable](https://www.digikey.com/products/en?keywords=768-1070-ND) +（备用）[1.8v FTDI串行适配器电缆]（https://www.digikey.com/products/zh_CN?keywords=768-1070-ND）

__The following software is required:__  __需要以下软件：__

 
+ `fastboot`  +`fastboot`

  To install on Ubuntu: `sudo apt-get install android-tools-fastboot`  要在Ubuntu上安装：`sudo apt-get install android-tools-fastboot`

 
## Overview  总览 

At a high level, these are the steps for getting a HiKey development environment fully working: 从总体上讲，这些是使HiKey开发环境完全运行的步骤：

 
+ Build a Zircon boot image  +构建Zircon启动映像
+ Enable the serial console (useful for debugging subsequent steps)  +启用串行控制台（用于调试后续步骤）
+ Flash the HiKey's low-level firmware  +刷新HiKey的底层固件
+ Flash the Zircon boot image onto the HiKey (this image -- specifically zedboot -- will receive and boot your subsequent Fuchsia builds) +将Zircon启动映像闪存到HiKey上（此映像-特别是zedboot-将接收并启动后续的Fuchsia构建）
+ Build and boot Fuchsia  +构建并启动紫红色

Once the system is correctly configured, your development workflow should resemble a workflow on other hardware (repeated builds done with `fx build`,a persistent instance of `fx pave` to automatically update the hardware, and apersistent instance of `fx log` to capture console output). 系统正确配置后，您的开发工作流程应类似于其他硬件上的工作流程（使用fx build进行的重复构建，fx pave的持久实例以自动更新硬件，以及fx log的持久实例捕获控制台输出）。

 

 
## Useful Information  有用的信息 

 
+ [HiKey960 Development Board User Manual](https://www.96boards.org/documentation/ConsumerEdition/HiKey960/HardwareDocs/HardwareUserManual.md.html)  + [HiKey960开发板用户手册]（https://www.96boards.org/documentation/ConsumerEdition/HiKey960/HardwareDocs/HardwareUserManual.md.html）
+ [96boards-hikey github page](https://github.com/96boards-hikey)  + [96boards-hikey github页面]（https://github.com/96boards-hikey）
+ [96boards Getting Started page](https://www.96boards.org/documentation/ConsumerEdition/HiKey960/GettingStarted/)  + [96boards入门页面]（https://www.96boards.org/documentation/ConsumerEdition/HiKey960/GettingStarted/）
+ [SoC Reference](https://github.com/96boards/documentation/raw/master/consumer/hikey/hikey960/hardware-docs/HiKey960_SoC_Reference_Manual.pdf)  + [SoC参考]（https://github.com/96boards/documentation/raw/master/consumer/hikey/hikey960/hardware-docs/HiKey960_SoC_Reference_Manual.pdf）
+ [AOSP HiKey960 Information](https://source.android.com/source/devices#hikey960)  + [AOSP HiKey960信息]（https://source.android.com/source/deviceshikey960）
+ [HiKey960 Schematic](http://www.lemaker.org/product-hikeysecond-download-62.html)  + [HiKey960原理图]（http://www.lemaker.org/product-hikeysecond-download-62.html）

 
## Building the Zircon boot image  构建Zircon引导映像 

To build zircon, invoke the following command from the top level Zircon directory (ensure that you have checked out the ARM64 toolchains). For moreinformation, see `docs/getting_started.md`: 要构建Zircon，请从顶级Zircon目录中调用以下命令（确保已签出ARM64工具链）。有关更多信息，请参见`docs / getting_started.md`：

```
gn gen build-zircon
ninja -C build-zircon
```
 

 
## Setting up the serial console  设置串行控制台 

First, get the device to show up on your dev host machine as a serial device. Following that, install and configure a console app. 首先，让该设备作为串行设备显示在您的开发主机上。之后，安装并配置控制台应用程序。

 
#### Serial hardware setup  串行硬件设置 

If using a __mezzanine board__, follow the instructions included with it. Additional tips: 如果使用__夹层板__，请按照其附带的说明进行操作。其他提示：

 
  + Take care not to install the mezzanine board backwards on the connector. The micro-USB port should face outward; the corner pushbutton should be in thecenter of the HiKey board. +注意不要将夹层板向后安装在连接器上。微型USB端口应朝外；角按钮应在HiKey板的中央。

 
  + Some standard micro-USB cables have a button to enable/disable the data lines. When using one of these cables, ensure that these lines are enabled -the LED should be _amber_ (not green). +一些标准的micro-USB电缆带有一个按钮，用于启用/禁用数据线。使用这些电缆之一时，请确保已启用这些线路-LED应该为_amber_（不是绿色）。

 
  + The mezzanine board receives power through the micro-USB cable, so power need not be applied to the main HiKey board yet. +夹层板通过micro-USB电缆供电，因此还不需要将电源施加到主HiKey板上。

If using a __FTDI-style serial adapter cable__:  如果使用__FTDI型串行适配器电缆__：

 
  + The signals are available on the 40 pin LS connector ([reference](https://github.com/96boards/documentation/blob/master/consumer/hikey/hikey960/additional-docs/images/images-hw-user-manual/HiKey960_Numbered_Front2.png?raw=true)) +信号可在40针LS连接器上使用（[参考]（https://github.com/96boards/documentation/blob/master/consumer/hikey/hikey960/additional-docs/images/images-hw-user-手册/HiKey960_Numbered_Front2.png?raw=true））
    + Pin 1  - GND  +引脚1-GND
    + Pin 11 - UART TX (HiKey960 --> Host)  +引脚11-UART TX（HiKey960->主机）
    + PIN 13 - UART RX (HiKey960 <-- Host)  + PIN 13-UART RX（HiKey960 <-主机）

 

 
  + This means that for a common [FTDI style adapter](https://www.digikey.com/products/en?keywords=768-1070-ND):  +这意味着对于常见的[FTDI样式适配器]（https://www.digikey.com/products/zh_CN?keywords=768-1070-ND）：
    + Black  --> Pin1  +黑色-> Pin1
    + Yellow --> Pin11  +黄色-> Pin11
    + Orange --> Pin13  +橙色-> Pin13

 

 
  + (Optional) an active low reset is available on pin 6 of the 40 pin LS connector. A jumper wire intermittently shorted from this pin to GND (shieldsof the connectors are all grounded) can provide an easy way to reset the boardand place it in fastboot mode. +（可选）40引脚LS连接器的6引脚提供低电平有效复位。从该引脚到GND的接地线（该连接器的屏蔽层均已接地）间断地短路，可以提供一种简便的方法来复位电路板并将其置于快速启动模式。

Once you have correctly configured the hardware (via either method), the device should appear to your host machine as a USB-connected UART, listed in your /devdirectory as `/dev/ttyUSB0` (or USB1, etc). If this is _not_ the case, you mayhave forgotten to enable the data lines (LED should be amber), or you may have abad micro-USB cable or mezzanine board. Regardless, do not proceed until yourHiKey board is detected and enumerated in the `/dev` directory as a tty device. 一旦正确配置了硬件（通过任何一种方法），设备就应该在主机上显示为USB连接的UART，在/ dev目录中以`/ dev / ttyUSB0`（或USB1等）列出。如果不是这种情况，您可能忘记了启用数据线（LED应该为琥珀色），或者您的Micro-USB电缆或夹层板不正确。无论如何，只有在检测到yourHiKey板并将其作为tty设备枚举到/ dev目录中之后，再进行操作。

 
#### Serial console software  串行控制台软件 

Use a host application such as screen or putty to connect to the serial port and provide console functionality. Use a baud rate of 115200. 使用主机应用程序（例如屏幕或腻子）连接到串行端口并提供控制台功能。使用115200的波特率。

Example commands using **screen**:  使用** screen **的示例命令：
  + `screen /dev/ttyUSB0 115200,-ixoff`  +`屏幕/ dev / ttyUSB0 115200，-ixoff`
  + `Ctrl-a, Esc` to enable scrolling (then k-up, j-down, q-done scrolling)  +`Ctrl-a，Esc`启用滚动（然后进行k向上，j向下，q完成滚动）
  + `Ctrl-a, d` to detach from the session (`screen -r -d` to reattach)  +`Ctrl-a，d`从会话中分离（`screen -r -d`重新连接）
  + `Ctrl-a, \` to kill all screen sessions.  +`Ctrl-a，\`杀死所有屏幕会话。

If you receive an error when connecting to your tty/USBn, you may need to run your serial console application as `sudo`. Alternately, you can add a udev rulethat allows applications to connect to this device: 如果连接到tty / USBn时收到错误，则可能需要以sudo身份运行串行控制台应用程序。或者，您可以添加udev规则，该规则允许应用程序连接到此设备：

 
  + Create file `/etc/udev/rules.d/99-ttyusb.rules` containing the following:  +创建文件“ /etc/udev/rules.d/99-ttyusb.rules”，其中包含以下内容：

    `SUBSYSTEM=="tty", GROUP="dialout"`  `SUBSYSTEM ==“ tty”，GROUP =“ dialout”`

 
  + Then `sudo udevadm control --reload-rules`  +然后`sudo udevadm control --reload-rules`

 

 
## Entering fastboot mode  进入快速启动模式 
##### (needed for flashing low-level firmware and/or Zircon)  （需要用于刷新低级固件和/或Zircon） 

Connect the power supply if you have not already. If the power plug doesn't seem to fit, you may have forgotten to get a DC adapter. The power plug for theHiKey boards has a 4.75mm diameter and 1.7mm center pin, whereas most DC powersupplies in this class have a 5.5mm diameter and 2.1mm center pin. 如果尚未连接电源。如果电源插头似乎不合适，则您可能已经忘记了购买直流适配器。 HiKey板的电源插头的直径为4.75mm，中心引脚为1.7mm，而大多数此类直流电源的直径为5.5mm，中心引脚为2.1mm。

To flash the board, it must be connected to your workstation via the USB-C OTG connection on the HiKey960 main board. Additionally, the HiKey960 must be infastboot mode. You can enter fastboot in one of two ways: 要刷新该板，必须通过HiKey960主板上的USB-C OTG连接将其连接到您的工作站。此外，HiKey960必须处于快速启动模式。您可以通过以下两种方式之一输入fastboot：

 
+ __DIP Switch method__  Use the switches on the back of the board. (Older HiKeys may have jumpers instead of DIP switches.) To boot into fastboot mode,the switches should be in the following positions: + __DIP开关方法__使用板子背面的开关。 （较早的HiKey可能具有跳线而不是DIP开关。）要启动进入快速启动模式，开关应位于以下位置：

        Auto Power up(Switch 1)   closed/ON Recovery(Switch 2)        open/OFFFastboot(Switch 3)        closed/ON 自动开机（开关1）已关闭/开启恢复（开关2）已开启/关闭快速启动（开关3）已关闭/开启

  Once the switches are in these positions, unplug/plug power or reset the board. It will then boot into _fastboot_ mode, awaiting commands from thehost. If you are using the serial adapter cable, just a reminder that this canbe done with the jumper wire on pin 6, as mentioned earlier. 将开关置于这些位置后，拔下电源插头或重置板。然后它将引导进入_fastboot_模式，等待主机的命令。如果您使用的是串行适配器电缆，请注意，这可以通过引脚6上的跳线完成，如前所述。

  Note: after you have performed the last of your flash operations, you want the device to boot normally going forward, so you should open (turn OFF) DIPswitch 3 _before_ your final boot (once firmware and Zircon updates arecomplete, before booting into Zircon for the first time). 注意：执行完最后一次闪存操作后，您希望设备正常启动，因此，应在最终引导之前打开（关闭）DIPswitch 3（一旦固件和Zircon更新完成，则引导至Zircon进行）。第一次）。

 
+ __Double-Reset method__  Using the button on the mezzanine board, reset the board, then reset it _again_ after seeing the following console messages: + __Double-Reset方法__使用夹层板上的按钮，重置板，然后在看到以下控制台消息后_again_重置它：

        C3R,V0x00000016 e:113 C0R,V0x00000017 e:66C1R,V0x00000017 e:66C2R,V0x00000017 e:66C3R,V0x00000017 e:66 C3R，V0x00000016 e：113 C0R，V0x00000017 e：66C1R，V0x00000017 e：66C2R，V0x00000017 e：66C3R，V0x00000017 e：66

  The second reset instructs the board to restart into fastboot __for the next boot cycle only__. The timing on this double-reset is a little tricky, but youwill know you got the timing right if you see the following console messagesat the end of the boot spew: 第二次重置将指示板仅在下一个引导周期__时重新启动进入快速引导。两次重设的时间有些棘手，但是如果您在引导启动结束时看到以下控制台消息，您将知道时间正确。

        usbloader: bootmode is 4 usb: [USBFINFO]USB RESETusb: [USBFINFO]USB CONNDONE, highspeedusb: [USBFINFO]USB RESETusb: [USBFINFO]USB CONNDONE, highspeedusbloader: usb: online (highspeed)usb: [USBFINFO]usb enum done usbloader：引导模式为4 usb：[USBFINFO] USB RESETusb：[USBFINFO] USB CONNDONE，高速usb：[USBFINFO] USB RESETusb：[USBFINFO] USB CONNDONE，高速usbloader：usb：联机（高速）usb：[USBFINFO] usb枚举完成

  These messages confirm that the device has restarted into fastboot mode. If you do not see these messages, use the button to reset the board and try againuntil you are successful. 这些消息确认设备已重新启动进入快速启动模式。如果没有看到这些消息，请使用按钮重置主板，然后重试直到成功。

  As a reminder, with this method, the DIP switches on the HiKey should remain in _normal_ mode (closed/ON open/OFF open/OFF), not the 'fastboot' modementioned in the previous option. 提醒一下，使用此方法时，HiKey上的DIP开关应保持为_normal_模式（关闭/ ON打开/ OFF打开/ OFF），而不是先前选项中提到的“快速启动”模式。

Once the board is in fastboot mode (regardless of which method you use), it is ready to be flashed with firmware updates and/or the Zircon boot image. 一旦该板进入快速启动模式（无论使用哪种方法），就可以通过固件更新和/或Zircon引导映像进行刷新。

 
## Install Firmware  安装固件 

We have run into inconsistent behavior between different HiKey 960 boards, depending on the low level firmware came installed on the device. We recommendsetting up your board with known good firmware from the Android AOSP project. 根据设备上安装的低级别固件，我们在不同的HiKey 960板之间遇到了不一致的行为。我们建议您使用Android AOSP项目中已知良好的固件来设置您的开发板。

To install firmware, put your board in fastboot mode and run the following:  要安装固件，请将您的电路板置于快速启动模式并运行以下命令：

      ./scripts/flash-hikey -f  ./scripts/flash-hikey -f

 
## Recover the device  恢复设备 

If the hikey gets into a bad state you can try the recovery mechanism. The script should automate the process, including reinstalling the firmware. Youfirst need to put the device into recovery mode: 如果远足者陷入不良状态，您可以尝试恢复机制。该脚本应自动执行该过程，包括重新安装固件。您首先需要将设备置于恢复模式：

        Auto Power up(Switch 1)   closed/ON Recovery(Switch 2)        closed/ONFastboot(Switch 3)        open/OFF 自动开机（开关1）关闭/开恢复（开关2）关闭/开快速启动（开关3）开/关

Then run:  然后运行：

      ./scripts/flash-hikey -r  ./scripts/flash-hikey -r

The recovery process communicates with the device over the USB-C cable, but it can be a bit flaky at times. If the script complains that it can't open theserial device first check what serial devices are connected (`ls/dev/serial/by-id/`) and make sure the script is using the correct device. Youcan specify which serial port to use with `-p`. Sometimes you just need to try afew times or power cycle the device. Occasionally the script will fail whenattempting to install firmware, which can usually be fixed by starting again. 恢复过程通过USB-C电缆与设备进行通信，但有时可能会有些不稳定。如果脚本抱怨无法打开串行设备，请首先检查已连接的串行设备（“ ls / dev / serial / by-id /”），并确保脚本使用了正确的设备。您可以指定与-p一起使用的串行端口。有时，您只需要尝试几次或重启设备即可。有时，在尝试安装固件时脚本将失败，通常可以通过重新启动来修复该脚本。

 
## Installing Zircon  安装锆石 

Once the HiKey board is in fastboot mode, run the following script from the zircon root directory to flash the necessary files onto the board: 一旦HiKey板进入快速启动模式，请从zircon根目录运行以下脚本，以将必要的文件刷新到板上：

      ./scripts/flash-hikey  ./scripts/flash-hikey

 
## Zedboot  Zedboot 

If you would like to boot future kernels via the network, instead of flashing them directly, then run the script with the `-m` option. 如果您想通过网络引导将来的内核，而不是直接刷新它们，请使用-m选项运行脚本。

      ./scripts/flash-hikey -m  ./scripts/flash-hikey -m

This is the last flash update, and all subsequent boots should use normal mode (not fastboot or recovery). If you used the DIP Switch method to place the boardin fastboot mode, you should flip the fastboot switch (switch 3) back toopen/OFF _before_ running this script, so that it will boot into Zircon afterflashing (otherwise, it will boot back into fastboot mode). 这是最后一次闪存更新，所有后续启动都应使用普通模式（而不是快速启动或恢复）。如果您使用DIP Switch方法将电路板置于快速启动模式，则应在运行此脚本之前将快速启动开关（开关3）翻转回open / OFF，以便在刷新后将其启动到Zircon中（否则，它将重新启动至fastboot）模式）。

If you used the double-tap reset method to place the board into fastboot mode, no further reconfiguration is needed: the board will boot into the kernel afterit completes flashing. 如果您使用两次轻击重置方法将板置于快速启动模式，则无需进行进一步的重新配置：板将在完成刷新后启动进入内核。

For now, the ethernet connectivity needed for zedboot is actually provided by zircon via USB. This is automatically enabled on the HiKey USB-C connector, ifit is changed from host mode into device mode. If all flash steps appear tocomplete successfully, but the device does not restart into Zedboot, you mayneed to manually place the device into USB 'device' mode. Enter the followingcommand in your console: 到目前为止，zirboot实际通过zircon通过USB提供了zedboot所需的以太网连接。如果将其从主机模式更改为设备模式，则会在HiKey USB-C连接器上自动启用此功能。如果所有闪存步骤似乎均已成功完成，但是设备没有重新启动进入Zedboot，则可能需要手动将设备置于USB“设备”模式。在控制台中输入以下命令：

      usbctl mode device  USB模式设备

This step must be repeated each time the device is fully powered-down/up. At some point in the near future, the Fuchsia build will include support for USBNICs via USB-A, at which time this `usbctl` step will be unnecessary. 每次设备完全断电/上电时，都必须重复此步骤。在不久的将来的某个时候，Fuchsia版本将包括通过USB-A支持USBNIC的信息，届时将不再需要“ usbctl”步骤。

Once your device restarts and displays 'Zedboot' in the console, the setup process is complete. You can now use your usual build, boot and log commands.When powering up (not simply resetting) the device, you may need to press thereset button for the device to show up again as /dev/ttyUSBn. Recall that thisis needed before connecting the serial console and interacting with the device. 设备重新启动并在控制台中显示“ Zedboot”后，设置过程即告完成。现在您可以使用常规的构建，引导和日志命令。在打开设备电源（而不是简单地重置）时，可能需要按按钮以使设备再次显示为/ dev / ttyUSBn。回想一下，在连接串行控制台并与设备交互之前，这是必需的。

 

 
## Manually Installing Low-Level Firmware  手动安装低级固件 

Note: the following requires fastboot in your execution path.  注意：以下要求在您的执行路径中使用fastboot。

To install firmware, put your board in fastboot mode and run the following:  要安装固件，请将您的电路板置于快速启动模式并运行以下命令：

      git clone https://android.googlesource.com/device/linaro/hikey hikey-firmware git -C hikey-firmware checkout 972114436628f874ac9ca28ef38ba82862937fbffastboot flash ptable hikey-firmware/installer/hikey960/ptable.imgfastboot flash xloader hikey-firmware/installer/hikey960/sec_xloader.imgfastboot flash fastboot hikey-firmware/installer/hikey960/fastboot.imgfastboot flash nvme hikey-firmware/installer/hikey960/nvme.imgfastboot flash fw_lpm3 hikey-firmware/installer/hikey960/lpm3.imgfastboot flash trustfirmware hikey-firmware/installer/hikey960/bl31.bin git clone https://android.googlesource.com/device/linaro/hikey远足固件git -C远足固件检出972114436628f874ac9ca28ef38ba82862937fbffastboot flash ptable远足固件/安装程序/hikey960/ptable.img快速启动Flash xloader远足固件/安装程序/ hikey960 /sec_xloader.imgfastboot闪存fastboot徒步旅行者固件/安装程序/hikey960/fastboot.imgfastboot闪存nvme徒步旅行者固件/安装程序/hikey960/nvme.imgfastboot闪存fw_lpm3徒步旅行者固件/安装程序/hikey960/lpm3.imgfastboot闪存可信赖的固件徒步旅行者固件/安装程序/hikey960/bl31.bin

This installs all the AOSP firmware except Android itself. To use a different bootloader altogether (not the one from AOSP), first complete the above commandsand then install your bootloader. 这将安装除Android本身以外的所有AOSP固件。要完全使用其他引导加载程序（不是AOSP中的引导加载程序），请首先完成上述命令，然后安装引导加载程序。

 
## Device support  设备支持 

