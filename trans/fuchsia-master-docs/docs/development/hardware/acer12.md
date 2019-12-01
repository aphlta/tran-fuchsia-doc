 
# Acer Switch Alpha 12  宏cer Switch Alpha 12 

WARNING:  These are directions to configure the machine and boot an experimental, in-development OS on it.  警告：这些是配置机器并在其上引导实验性的开发中操作系统的指导。

 
## Powering the Machine On  开启机器电源To power on you must hold the power button (lefthand side, above the Volume rocker) for several seconds, then let go.  You can safely let go when the tiny blue light on the power button itself turns on (yes, this is really hard to see when you’re holding the power button), or when the display backlight turns on.  If you hold too long it may end up power right back off again.  要打开电源，必须按住电源按钮（在音量摇杆上方的左侧）几秒钟，然后松开。当电源按钮本身的小蓝灯点亮时（是的，当您按住电源按钮时确实很难看到），或者显示屏背光灯打开时，您可以放手。如果按住时间过长，可能会再次断电。

 
## Powering the Machine Off  关闭机器电源If you boot into Windows 10 or something hangs or crashes and you need to power things off, Press and Hold the power button until the display shuts off.  To be sure, hold for about 10 seconds total.  如果您启动进入Windows 10或因某些原因而挂起或崩溃，并且需要关闭电源，请按住电源按钮，直到显示屏关闭。可以肯定的是，总共保持约10秒钟。

 
## Entering the BIOS  进入BIOSWith the machine off, Press and hold Volume Up, then continue to hold while pressing and holding the Power button.  Let go of the Power button when the display backlight turns on.  Alternatively, hold F2 on an attached keyboard while powering the machine on.  在机器关闭的情况下，按住音量调高，然后在按住电源按钮的同时继续按住。显示屏背光打开时，松开电源按钮。或者，在打开机器电源的同时，在连接的键盘上按住F2键。

 
## Enabling Zircon Boot  启用Zircon引导 
1. Boot the machine and enter the BIOS  1.引导计算机并进入BIOS
2. Select “Security” from the tabs at the left  2.从左侧的标签中选择“安全性”
3. Tap the “[clean]” gray bar under “Supervisor Password Is”  3.点击“超级用户密码为”下方的“ [干净]”灰色栏。
4. Enter a supervisor password, enter it again, press OK  4.输入管理员密码，再次输入，然后按确定。
5. Select “Boot” from the tabs at the left  5.从左侧的选项卡中选择“启动”
6. Tap the “[Enabled]” gray bar under “Secure Boot” (if there’s no gray bar, you have not set a supervisor password, go back and do that now) 6.点击“安全启动”下的“ [启用]”灰色栏（如果没有灰色栏，则说明您尚未设置管理员密码，请返回并立即执行）
7. Select “Disabled” from the menu  7.从菜单中选择“禁用”
8. The “Boot priority order” list may be adjusted using the up/down arrows to the right of each item  8.可以使用每个项目右边的向上/向下箭头来调整“启动优先顺序”列表
9. Order the list like so:  9.像这样订购列表：
   - USB HDD  -USB硬碟
   - USB FDD  -USB FDD
   - USB CDROM  -USB CDROM
   - HDD: \<MFG\> \<SERIALNO\>  -硬盘：\ <MFG \> \ <SERIALNO \>
   - Network Boot-IPV4  -网络启动IPV4
   - Network Boot-IPV6  -网络启动IPV6
   - Windows Boot Manager 10. Select the “Main” tab on the left and set the time and date by pressing “[SetTime]” and “[SetDate]” buttons respectfully. This is necessary for proper network operation.11. (Optional)  Go back to the “Security” tab and set the supervisor password back to nothing.Otherwise you’ll need to enter the password every time you use the BIOS.A password is required to modify the secure boot setting, but “disabled” will persist without one.12. Select “Exit” from the tabs at the left13. Select “Exit Saving Changes”14. Continue to [Setup with USB flash drive](usb_setup.md) -Windows启动管理器10.选择左侧的“主”选项卡，然后分别按“ [SetTime]”和“ [SetDate]”按钮设置时间​​和日期。这对于正确的网络操作是必不可少的。11。 （可选）返回“安全性”选项卡，将超级用户密码设置为空。否则，每次使用BIOS时都需要输入密码。修改安全启动设置需要输入密码，但是“已禁用” ”将持续存在而没有1.12。从左侧的标签中选择“退出” 13。选择“退出保存更改” 14。继续进行[使用USB闪存驱动器进行设置]（usb_setup.md）

 
## What if you end up in the Windows 10 Setup?  如果最终进入Windows 10安装程序怎么办？If you don’t enter the BIOS and haven’t installed another OS, You’ll end up on a blue background “Hi there” screen asking you to select country, language, etc.  如果您没有输入BIOS且未安装其他操作系统，则最终将显示在蓝色背景的“您好”屏幕上，要求您选择国家/地区，语言等。

 
1. Press Power and Hold it for about 10 seconds (the screen will turn off after 2-3 seconds).  1.按住电源约10秒钟（屏幕将在2-3秒钟后关闭）。
2. Boot into the BIOS as described above.  2.如上所述，启动进入BIOS。

 
## What if you get stuck in Windows 10 Recovery?  如果您陷在Windows 10恢复中怎么办？It’s possible to end up in a situation where the machine *really* wants to help you recover your failed boots into Windows 10 and dumps you into a recovery screen -- blue background, “Recovery” in the upper left, and some text saying “It looks like Windows didn’t load correctly”.  最终可能会出现以下情况：机器“确实”希望帮助您将失败的引导程序恢复到Windows 10中，并将您转储到恢复屏幕中-蓝色背景，左上方的“ Recovery”，以及一些显示“ Windows似乎无法正确加载”。

 
1. Select “See advanced repair options”  1.选择“查看高级修复选项”
2. Select “Troubleshoot” (screwdriver and wrench icon)  2.选择“疑难解答”（螺丝刀和扳手图标）
3. Select “Advanced options” (checkmarks and lines icon)  3.选择“高级选项”（复选标记和线条图标）
4. Select “UEFI Firmware Settings” (integrated circuit and gear icon)  4.选择“ UEFI固件设置”（集成电路和齿轮图标）
5. When prompted “Restart to change UEFI firmware settings”, select “Restart”  5.当提示“重新启动以更改UEFI固件设置”时，选择“重新启动”
6. The machine should now reboot into the BIOS  6.机器现在应该重新启动进入BIOS
7. Check that “Windows Boot Manager” didn’t get moved to the top of the boot order, fix it if it did  7.检查“ Windows启动管理器”没有移到启动顺序的顶部，如果已解决，请进行修复

 
## Quirks  怪癖It has been observed that USB initialization is racy on a cold boot.  So if you're starting from a cold boot and trying to boot to USB, you may find that you boot to disk instead.  已经观察到，USB初始化在冷启动时非常流行。因此，如果您是从冷启动开始并尝试启动到USB，则可能会发现自己启动到了磁盘。

Mitigations:  缓解措施：

 
- It's useful to use a `cmdline` file to set `zircon.nodename=foo` to know during the boot screen whether you're booting from USB or disk.  -使用`cmdline`文件设置`zircon.nodename = foo`很有用，以便在引导屏幕期间知道是从USB引导还是从磁盘引导。
- If the Acer is booting from disk and you want to boot from USB, remove and reinsert the USB drive, then reboot with `ctrl-alt-del` (not the power button.)  -如果Acer从磁盘引导，并且您想从USB引导，请卸下并重新插入USB驱动器，然后使用ctrl-alt-del（而不是电源按钮）重新引导。
