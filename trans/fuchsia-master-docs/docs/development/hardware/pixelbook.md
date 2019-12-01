 
# Install Fuchsia on Pixelbook  在Pixelbook上安装紫红色 

 
## Prerequisites  先决条件Ensure that you have a chromebook build for Fuchsia. Note that Chromebook is now a distinct board configuration from other x64 devices. See [Paving](/docs/development/workflows/paving.md#building) formore information. 确保您拥有用于紫红色的chromebook版本。请注意，Chromebook现在是与其他x64设备不同的主板配置。有关更多信息，请参见[Paving]（/ docs / development / workflows / paving.mdbuilding）。

 
## Update ChromeOS  更新ChromeOS 

If your Pixelbook has never been booted, it is best to boot it normally to check for any critical updates, as follows: 如果您的Pixelbook从未启动过，那么最好正常启动它以检查是否有关键更新，如下所示：

 
1. Boot the Pixelbook normally. Opening the lid usually powers on the device. If this doesn't work, the power button is on the left side of the device, nearthe front of the wrist rest. 1.正常启动Pixelbook。打开盖子通常会打开设备电源。如果此操作不起作用，则电源按钮位于设备左侧，靠近腕托的前部。
2. Tap the "Let's go" button.  2.点击“开始”按钮。
3. Connect to a wired or wireless network.  3.连接到有线或无线网络。
4. Accept the terms to proceed to the update check step.  4.接受条款以继续进行更新检查步骤。
5. The device should check for updates, install any found.  5.设备应检查更新，安装找到的任何更新。
6. After rebooting from any updates, tap 'Browse as Guest' in the lower left corner. 6.从任何更新重新启动后，点击左下角的“以访客身份浏览”。
7. From the browser UI, go into "Settings->About Chrome OS" or "Help->About Chrome OS" and confirm the version is &gt;=62. 7.从浏览器UI中，转到“设置->关于Chrome OS”或“帮助->关于Chrome OS”，并确认版本为gt; = 62。

 
## Put your device into developer mode  将设备置于开发人员模式***WARNING: This will erase any state stored locally on your Pixelbook***  ***警告：这将清除Pixelbook本地存储的所有状态***

 
1. Power off the Pixelbook.  1.关闭Pixelbook的电源。
2. Go into Recovery Mode. Hold down Esc+Refresh (first and third buttons on the top row of the keyboard).Then press the Power button (bottom left side of the device). 2.进入恢复模式。按住Esc + Refresh（键盘第一行的第一个和第三个按钮），然后按电源按钮（设备左下方）。
3. Start by disabling OS verification by pressing Ctrl+D. You should see "To turn OS verification OFF, press ENTER". Press Enter to confirm.  3.首先通过按Ctrl + D禁用OS验证。您应该看到“要关闭OS验证，请按ENTER”。按Enter确认。
4. When your device reboots, you'll get confirmation that OS verification is OFF. Press Ctrl+D again to enter Developer Mode.  4.设备重启后，将确认操作系统验证已关闭。再次按Ctrl + D进入开发人员模式。
5. Wait for the device to re-configure itself, which will take several minutes. Initially it may not appear to be doing anything. Let the device sit for aminute or two. You will hear two loud &lt;BEEP&gt;s early in the process. Theprocess is complete when you hear two more loud &lt;BEEP&gt;s. 5.等待设备重新配置自身，这将需要几分钟。最初，它似乎没有做任何事情。让设备坐一两分钟。您将在此过程的早期听到两声大声的<BEEPgt>。当您听到两个更大的LT; BEEPgt时，该过程完成。
6. The device should reboot itself when the Developer Mode transition is complete. You can now jump to Step #2 in the "Boot from USB" section. 6.开发人员模式转换完成后，设备应自行重启。现在，您可以跳至“从USB引导”部分中的步骤2。

 
## Boot from USB  从USB启动 

 
1. Boot into ChromeOS.  1.启动ChromeOS。
2. You should see a screen that says "OS verification is OFF" and approximately  2.您应该看到一个屏幕，显示“操作系统验证已关闭”，大约
30 seconds later the boot will continue. Wait for the Welcome or Login screen to load. **Ignore** any link for "Enable debugging features". 30秒后，引导将继续。等待“欢迎”或“登录”屏幕加载。 **忽略**“启用调试功能”的任何链接。
3. Press Ctrl+Alt+Refresh/F3 to enter a command shell. If pressing this key combination has no effect, try rebooting the Pixelbook once more. 3.按Ctrl + Alt + Refresh / F3进入命令外壳。如果按此键无效，请再次尝试重新启动Pixelbook。
4. Enter 'chronos' as the user with a blank password  4.以空白密码输入“ chronos”作为用户
5. Enable USB booting by running `sudo crossystem dev_boot_usb=1`  5.通过运行sudo crossystem dev_boot_usb = 1启用USB引导。
6. (optional) Default to USB booting by running `sudo crossystem dev_default_boot=usb`.  6.（可选）通过运行sudo crossystem dev_default_boot = usb来默认启动USB。
7. Plug the USB drive into the Pixelbook.  7.将USB驱动器插入Pixelbook。
8. Reboot by typing `sudo reboot`  8.键入sudo reboot重新启动
9. On the "OS verification is OFF" screen press Ctrl+U to bypass the timeout and boot from USB immediately. (See [Tips and Tricks](#tips-and-tricks) for othershort circuit options) 9.在“ OS验证已关闭”屏幕上，按Ctrl + U绕过超时并立即从USB启动。 （有关其他短路选项，请参见[技巧和窍门]（技巧和窍门））

The USB drive is only needed for booting when you want to re-pave or otherwise netboot the device. If you didn't make USB booting the default (Step #6), youwill need to press Ctrl+U at the grey 'warning OS-not verified' screen to bootfrom USB when you power on your device. If the device tries to boot from USB,either because that is the default or you pressed Ctrl+U, and the device failsto boot from USB you'll hear a fairly loud &lt;BEEP&gt;. Note that ChromeOSbootloader USB enumeration during boot has been observed to be slow. If you'rehaving trouble booting from USB, it may be helpful to remove other USB devicesuntil the device is through the bootloader and also avoid using a USB hub. 仅当您要重新铺设设备或以其他方式通过网络引导设备时，才需要USB驱动器进行引导。如果未将USB引导设为默认引导（步骤6），则需要在灰色的“警告操作系统未验证”屏幕上按Ctrl + U，以在打开设备电源时从USB引导。如果设备尝试从USB引导（因为这是默认设置）或您按了Ctrl + U，并且设备无法从USB引导，您将听到相当大的<BEEPgt>。请注意，已观察到引导过程中的ChromeOSbootloader USB枚举速度很慢。如果从USB引导时遇到问题，则删除其他USB设备可能会有所帮助，直到该设备通过引导加载程序为止，并且避免使用USB集线器。

 
## Tips and Tricks {#tips-and-tricks}  提示和技巧{tips-and-tricks} 

By default the ChromeOS bootloader has a long timeout to allow you to press buttons. To shortcut this you can press Ctrl+D or Ctrl+U when on the grey screenthat warns that the OS will not be verified. Ctrl+D will cause the device toskip the timeout and boot from its default source. Ctrl+U will skip the timeoutand boot the device from USB. 默认情况下，ChromeOS引导加载程序的超时时间较长，因此您可以按按钮。要简化此操作，在灰色屏幕上警告您将无法验证操作系统时，您可以按Ctrl + D或Ctrl + U。 Ctrl + D将导致设备跳过超时并从其默认源启动。 Ctrl + U将跳过超时并从USB启动设备。

 
### Going back to ChromeOS  回到ChromeOS 

To go back to ChromeOS you must modify the priority of the Fuchsia kernel partition to be lower than that of at least one of the two ChromeOS kernelpartitions. 要返回ChromeOS，您必须将Fuchsia内核分区的优先级修改为低于两个ChromeOS内核分区中至少一个的优先级。

 
1. Press Alt+Esc to get to a virtual console if not already on one  1.如果尚未在虚拟控制台上，请按Alt + Esc键进入虚拟控制台
2. Press Alt+Fullscreen to get to a terminal emulator on Fuchsia  2.按Alt + Fullscreen进入紫红色的终端模拟器
3. Find the disk that contains the KERN-A, KERN-B, and KERN-C partitions with the `lsblk` command. Below this is device 000, note how the device path of thekernel partitions is an extension of that device. 3.使用“ lsblk”命令找到包含KERN-A，KERN-B和KERN-C分区的磁盘。在设备000的下面，请注意内核分区的设备路径是该设备的扩展。

        $ lsblk ID  SIZE TYPE             LABEL                FLAGS  DEVICE000 232G                                              /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block001   5G data             STATE                       /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-000/block002  16M cros kernel      KERN-A                      /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-001/block003   4G cros rootfs      ROOT-A                      /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-002/block004  16M cros kernel      KERN-B                      /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-003/block005   4G cros rootfs      ROOT-B                      /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-004/block006  64M cros kernel      KERN-C                      /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-005/block007   4G cros rootfs      ROOT-C                      /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-006/block $ lsblk ID大小类型标签设备232 G /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block001 5G数据状态/dev/sys/pci/00:1e.4/pci-sdhci / sdhci / sdmmc / block / part-000 / block002 16M cros内核KERN-A /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-001/block003 4G cros rootfs ROOT -A /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-002/block004 16M cros内核KERN-B /dev/sys/pci/00:1e.4/pci -sdhci / sdhci / sdmmc / block / part-003 / block005 4G cros rootfs ROOT-B /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-004/block006 64M cros内核KERN-C /dev/sys/pci/00:1e.4/pci-sdhci/sdhci/sdmmc/block/part-005/block007 4G cros rootfs ROOT-C /dev/sys/pci/00:1e.4 / pci-sdhci / sdhci / sdmmc / block / part-006 / block
4. Use the `gpt` command to look at the device's (eg. 000) partition map.  4.使用gpt命令查看设备的分区图（例如000）。

        $ gpt dump /dev/class/block/000 blocksize=0x200 blocks=488554496Partition table is validGPT contains usable blocks from 34 to 488554462 (inclusive)Paritition 0: STATEStart: 478035968, End: 488521727 (10485760 blocks)id:   51E8D442-0419-2447-96E5-49CB60CF0B25type: EBD0A0A2-B9E5-4433-87C0-68B6B72699C7flags: 0x0000000000000000Paritition 1: KERN-AStart: 20480, End: 53247 (32768 blocks)id:   054CD627-F23C-5C40-8035-C188FA57DE9Ctype: FE3A2A5D-4F32-41A7-B725-ACCC3285A309flags: priority=2 tries=0 successful=1Paritition 2: ROOT-AStart: 8704000, End: 17092607 (8388608 blocks)id:   936E138F-1ACF-E242-9C5B-3667FAA3C10Ctype: 3CB8E202-3B7E-47DD-8A3C-7FF2A13CFCECflags: 0x0000000000000000Paritition 3: KERN-BStart: 53248, End: 86015 (32768 blocks)id:   A8667891-8209-8648-9D5E-63DC9B8D0CB3type: FE3A2A5D-4F32-41A7-B725-ACCC3285A309flags: priority=1 tries=0 successful=1Paritition 4: ROOT-BStart: 315392, End: 8703999 (8388608 blocks)id:   8B5D7BB4-590B-E445-B596-1E7AA1BB501Ftype: 3CB8E202-3B7E-47DD-8A3C-7FF2A13CFCECflags: 0x0000000000000000Paritition 5: KERN-CStart: 17092608, End: 17223679 (131072 blocks)id:   C7D6B203-C18F-BC4D-9160-A09BA8970CE1type: FE3A2A5D-4F32-41A7-B725-ACCC3285A309flags: priority=3 tries=15 successful=1Paritition 6: ROOT-CStart: 17223680, End: 25612287 (8388608 blocks)id:   769444A7-6E13-D74D-B583-C3A9CF0DE307type: 3CB8E202-3B7E-47DD-8A3C-7FF2A13CFCECflags: 0x0000000000000000 $ gpt dump / dev / class / block / 000块大小= 0x200块= 488554496分区表有效GPT包含从34到488554462（含）的可用块类别0：STATE起始：478035968，结束：488521727（10485760块）id：51E8D442-0419- 2447-96E5-49CB60CF0B25类型：EBD0A0A2-B9E5-4433-87C0-68B6B72699C7标志：0x0000000000000000类别1：KERN-A开始：20480，结束：53247（32768块）ID：054CD627-F23C-5C40-8035-C188FA57DE9A2A4A-41 B725-ACCC3285A309标志：优先级= 2尝试= 0成功= 1类别2：ROOT-A开始：8704000，结束：17092607（8388608块）id：936E138F-1ACF-E242-9C5B-3667FAA3C10Ctype：3CB8E202-3B7E-47DD-8A3C-7FF2A13CFCECflag 0x0000000000000000类别3：KERN-B开始：53248，结束：86015（32768块）id：A8667891-8209-8648-9D5E-63DC9B8D0CB3类型：FE3A2A5D-4F32-41A7-B725-ACCC3285A309标志：优先级= 1尝试= 0成功= 1类别4：ROOT -B开始：315392，结束：8703999（8388608块）ID：8B5D7BB4-590B-E445-B596-1E7AA1BB501F类型：3CB8E202-3B7E-47DD-8A3C-7F F2A13CFCEC标志：0x0000000000000000类别5：KERN-C开始：17092608，结束：17223679（131072块）id：C7D6B203-C18F-BC4D-9160-A09BA8970CE1类型：FE3A2A5D-4F32-41A7-B725-ACCC3285Aititition ==优先级6 =优先级：ROOT-C开始：17223680，结束：25612287（8388608块）id：769444A7-6E13-D74D-B583-C3A9CF0DE307类型：3CB8E202-3B7E-47DD-8A3C-7FF2A13CFCEC标志：0x0000000000000000
5. KERN-C typically hosts the Zircon kernel. KERN-A and KERN-B typically have ChromeOS kernels. To go to ChromeOS we need to lower the priority of KERN-Chere by referencing the **partition** index on the **disk** that has thatpartition. 5. KERN-C通常托管Zircon内核。 KERN-A和KERN-B通常具有ChromeOS内核。要转到ChromeOS，我们需要通过引用具有该分区的“磁盘”上的“分区”索引来降低KERN-Chere的优先级。

        $ gpt edit_cros 5 -P 0 /dev/class/block/000  $ gpt edit_cros 5 -P 0 / dev / class / block / 000
6. Reboot  6.重新启动

