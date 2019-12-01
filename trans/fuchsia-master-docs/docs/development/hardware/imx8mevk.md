 
#  Zircon on iMX8M EVK  iMX8M EVK上的锆石Periodically check this file as the setup workflow will change/improve.  定期检查此文件，因为设置工作流程将更改/改进。

 

Please refer to the following documents for SoC and board related information:  请参考以下文档以获取与SoC和主板相关的信息：

i.MX 8M EVK Board Hardawre User's Guide: https://www.nxp.com/docs/en/user-guide/IMX8MDQLQEVKHUG.pdf i.MX 8M EVK电路板Hardawre用户指南：https://www.nxp.com/docs/en/user-guide/IMX8MDQLQEVKHUG.pdf

iMX8M Technical Reference Manual: https://www.nxp.com/docs/en/reference-manual/IMX8MDQLQRM.pdf iMX8M技术参考手册：https://www.nxp.com/docs/zh/reference-manual/IMX8MDQLQRM.pdf

u-Boot Source: https://source.codeaurora.org/external/imx/uboot-imx/https://source.codeaurora.org/external/imx/uboot-imx/log/?h=imx_v2017.03_4.9.51_imx8m_ga u-Boot来源：https://source.codeaurora.org/external/imx/uboot-imx/https://source.codeaurora.org/external/imx/uboot-imx/log/?h=imx_v2017.03_4。 9.51_imx8m_ga

 
## Flashing Zircon on eMMC:  在eMMC上闪烁Zircon： 

The board will boot out of eMMC by default. In order to boot Zircon, a custom u-boot binary is needed. The binary can be found at: go/imx8m-bootloader 默认情况下，该板将退出eMMC。为了引导Zircon，需要自定义的u-boot二进制文件。可以在以下位置找到该二进制文件：go / imx8m-bootloader

First step involves flashing the board with the custom u-boot binary:  第一步涉及使用自定义u-boot二进制文件刷新板：

 
# Requirements:  要求： 
 + Linux Host Machine  + Linux主机
 + For serial console: connect USB from your host to the Micro USB port on the board  +对于串行控制台：将USB从主机连接到板上的Micro USB端口
 + For fastboot: connect USB cable from your host to the USB-C port on the board  +对于快速启动：将USB电缆从主机连接到板上的USB-C端口
 + Create a file under /etc/udev/rules.d/70-nxp.rules with the following content:  +在/etc/udev/rules.d/70-nxp.rules下创建一个文件，其内容如下：

 SUBSYSTEM=="usb", ATTR{idVendor}=="0525", MODE="0664", GROUP="plugdev", TAG+="uaccess"  SUBSYSTEM ==“ usb”，ATTR {idVendor} ==“ 0525”，MODE =“ 0664”，GROUP =“ plugdev”，TAG + =“ uaccess”

 

 
# From Device (iMX8 EVK):  从设备（iMX8 EVK）： 

 
+ Reboot board and in serial console press space to halt autoboot  +重新启动板并在串行控制台中按空格以停止自动启动
+ From u-boot command line do the following:  +从u-boot命令行执行以下操作：
    + fastboot 0  + fastboot 0

 
# From Linux Host:  从Linux主机： 
 + fastboot flash bootloader0 /PATH/TO/CUSTOM/UBOOT/u-boot.imx  + fastboot flash引导加载程序0 /PATH/TO/CUSTOM/UBOOT/u-boot.imx
 + fastboot reboot  + fastboot重新启动

 If successful, the new U-Boot prompt should be "zircon-u-boot=>"  如果成功，则新的U-Boot提示符应为“ zircon-u-boot =>”

Once the custom U-Boot has been flashed, perform the following:  自定义U-Boot刷新后，请执行以下操作：
+ Reboot board and press space to halt autoboot  +重新启动板并按空格键以停止自动启动
+ From u-boot command line do the following:  +从u-boot命令行执行以下操作：
    + fastboot 0  + fastboot 0

From the host side, go to your zircon repository and run the following command:  从主机端，转到您的zircon存储库并运行以下命令：
+ ./scripts/flash-nxp  + ./scripts/flash-nxp

