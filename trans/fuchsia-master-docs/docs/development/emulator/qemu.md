 
# QEMU  量化宽松 

Zircon can [run under emulation](/docs/getting_started.md#Boot-from-QEMU) using QEMU. QEMU can either be installed via prebuilt binaries, or builtlocally. Zircon可以使用QEMU [在仿真下运行]（/ docs / getting_started.mdBoot-from-QEMU）。 QEMU可以通过预构建的二进制文件安装，也可以通过本地安装。

 
## Prebuilt QEMU  预制QEMU 

QEMU is downloaded by `jiri` as part of `jiri update` or `jiri run-hooks`.  QEMU由“ jiri”下载，作为“ jiri update”或“ jiri run-hooks”的一部分。

QEMU is fetched into `//prebuilts/third_party/qemu`. You can run it most conveniently using `fx qemu` (see below). QEMU被提取到`// prebuilts / third_party / qemu`中。您可以使用`fx qemu`来最方便地运行它（见下文）。

 
## Build QEMU  建立QEMU 

 
### Install Prerequisites  安装先决条件 

Building QEMU on macOS requires a few packages. As of macOS 10.12.1:  在macOS上构建QEMU需要一些软件包。从macOS 10.12.1开始：

```
# Using http://brew.sh
brew install pkg-config glib automake libtool

# Or use http://macports.org ("port install ...") or build manually
```
 

 
### Build  建立 

```
cd $SRC
git clone --recursive https://fuchsia.googlesource.com/third_party/qemu
cd qemu
./configure --target-list=aarch64-softmmu,x86_64-softmmu
make -j32
sudo make install
```
 

If you don't want to install in /usr/local (the default), which will require you to be root, add --prefix=/path/to/install (perhaps $HOME/qemu). Then you'lleither need to add /path/to/install/bin to your PATH or use -q /path/to/installwhen invoking run-zircon-{arch}. 如果您不想安装在/ usr / local（默认设置）中（这将要求您是root用户），请添加--prefix = / path / to / install（也许$ HOME / qemu）。然后，您需要在调用run-zircon- {arch}时将/ path / to / install / bin添加到PATH或使用-q / path / to / install。

 
## Run Zircon under QEMU  在QEMU下运行Zircon 

```
# for aarch64
fx set bringup.arm64
fx build
fx qemu

# for x86
fx set bringup.x64
fx build
fx qemu
```
 

If QEMU is not on your path, use -q <directory> to specify its location.  如果QEMU不在路径上，请使用-q <directory>指定其位置。

The -h flag will list a number of options, including things like -b to rebuild first if necessary and -g to run with a graphical framebuffer. -h标志将列出许多选项，包括-b如果需要的话首先进行重建，以及-g与图形帧缓冲区一起运行。

To exit qemu, enter Ctrl-a x. Use Ctrl-a h to see other commands.  要退出qemu，请输入Ctrl-a x。使用Ctrl-a h查看其他命令。

 
## Enabling Networking under QEMU  在QEMU下启用网络 

The run-zircon script, when given the -N argument will attempt to create a network interface using the Linux tun/tap network device named "qemu".  QEMUdoes not need to be run with any special privileges for this, but you need tocreate a persistent tun/tap device ahead of time (which does require you be root): 当给定-N参数时，run-zircon脚本将尝试使用名为“ qemu”的Linux tun / tap网络设备创建网络接口。 QEMU不需要为此具有任何特殊特权即可运行，但是您需要提前创建一个持久的tun / tap设备（这需要您是root用户）：

On Linux:  在Linux上：

```
sudo ip tuntap add dev qemu mode tap user $USER
sudo ifconfig qemu up
```
 

This is sufficient to enable link local IPv6 (as the loglistener tool uses).  这足以启用链接本地IPv6（如loglistener工具使用的那样）。

On macOS:  在macOS上：

macOS does not support tun/tap devices out of the box; however, there is a widely used set of kernel extensions called tuntaposx which can be downloaded[here](http://tuntaposx.sourceforge.net/download.xhtml). Once the installercompletes, the extensions will create up to 16 tun/tap devices. Therun-zircon-x64 script uses /dev/tap0. macOS不支持开箱即用的tun / tap设备;但是，有一组广泛使用的内核扩展，称为tuntaposx，可以在此处下载（http://tuntaposx.sourceforge.net/download.xhtml）。安装程序完成后，扩展程序最多可以创建16个tun / tap设备。 therun-zircon-x64脚本使用/ dev / tap0。

```
sudo chown $USER /dev/tap0

# Run zircon in QEMU, which will open /dev/tap0
fx qemu -N

# (In a different window) bring up tap0 with a link local IPv6 address
sudo ifconfig tap0 inet6 fc00::/7 up
```
 

<aside class="note"> One caveat with tuntaposx is that the network interface willautomatically go down when QEMU exits and closes the network device. So thenetwork interface needs to be brought back up each time QEMU is restarted. Toautomate this, you can use the -u flag to run a script on qemu startup. Anexample startup script containing the above command is located inscripts/qemu-ifup-macos, so QEMU can be started with: <aside class =“ note”>关于tuntaposx的一个警告是，当QEMU退出并关闭网络设备时，网络接口将自动关闭。因此，每次重新启动QEMU时都需要恢复网络接口。要自动执行此操作，可以使用-u标志在qemu启动时运行脚本。包含上述命令的示例启动脚本位于inscripts / qemu-ifup-macos中，因此可以使用以下命令启动QEMU：

<pre> fx qemu -Nu ./scripts/qemu-ifup-macos</pre></aside> <pre> fx qemu -Nu ./scripts/qemu-ifup-macos</pre> </ aside>

 
## Using Emulated Disk under QEMU  在QEMU下使用仿真磁盘 

Using builds based on core (really any product above bringup) will automatically imply a disk that is provided to serve the `fvm` partition thatincludes a minfs partition for mutable storage, and a blobfs partition forpackage data storage. 使用基于内核的构建（实际上是在buildup之后的任何产品）都会自动暗示提供了一个磁盘来服务`fvm'分区，其中包括用于可变存储的minfs分区和用于软件包数据存储的blobfs分区。

You can attach additional images using flags as follows:  您可以使用标志附加其他图像，如下所示：

```
fx qemu -d [-D <disk_image_path (default: "blk.bin")>]
```
 

 

 
## Debugging the kernel with GDB  使用GDB调试内核 

 
### Sample session  样本会议 

Here is a sample session to get you started.  这是一个示例会话，可以帮助您入门。

In the shell you're running QEMU in:  在Shell中，您在以下位置运行QEMU：

```
shell1$ fx qemu -- -s -S
[... some QEMU start up text ...]
```
 

This will start QEMU but freeze the system at startup, waiting for you to resume it with "continue" in GDB.If you want to run QEMU without GDB, but be able to attach with GDB laterthen start QEMU without "-S" in the above example: 这将启动QEMU，但会在启动时冻结系统，等待您在GDB中使用“继续”来恢复它。如果要在没有GDB的情况下运行QEMU，但稍后又可以与GDB相连，则在启动时不带“ -S”的情况下启动QEMU。上面的例子：

```
shell1$ fx qemu -- -s
[... some QEMU start up text ...]
```
 

And then in the shell you're running GDB in: [Commands here are fully spelled out, but remember most can be abbreviated.] 然后在Shell中运行GDB：[此处的命令已完全拼出，但请记住大多数命令都可以缩写。

```
shell2$ gdb build-x86/zircon.elf
(gdb) target extended-remote :1234
Remote debugging using :1234
0x000000000000fff0 in ?? ()
(gdb) # Don't try to do too much at this point.
(gdb) # GDB can't handle architecture switching in one session,
(gdb) # and at this point the architecture is 16-bit x86.
(gdb) break lk_main
Breakpoint 1 at 0xffffffff8010cb58: file kernel/top/main.c, line 59.
(gdb) continue
Continuing.

Breakpoint 1, lk_main (arg0=1, arg1=18446744071568293116, arg2=0, arg3=0)
    at kernel/top/main.c:59
59	{
(gdb) continue
```
 

At this point Zircon boots and back in shell1 you'll be at the Zircon prompt. 此时，Zircon启动并返回shell1，您将在Zircon提示符下。

```
mxsh>
```
 

If you Ctrl-C in shell2 at this point you can get back to GDB.  如果此时在shell2中使用Ctrl-C，则可以返回到GDB。

```
(gdb) # Having just done "continue"
^C
Program received signal SIGINT, Interrupt.
arch_idle () at kernel/arch/x86/64/ops.S:32
32	    ret
(gdb) info threads
  Id   Target Id         Frame
  4    Thread 4 (CPU#3 [halted ]) arch_idle () at kernel/arch/x86/64/ops.S:32
  3    Thread 3 (CPU#2 [halted ]) arch_idle () at kernel/arch/x86/64/ops.S:32
  2    Thread 2 (CPU#1 [halted ]) arch_idle () at kernel/arch/x86/64/ops.S:32
* 1    Thread 1 (CPU#0 [halted ]) arch_idle () at kernel/arch/x86/64/ops.S:32
```
 

QEMU reports one thread to GDB for each CPU.  QEMU为每个CPU向GDB报告一个线程。

 
### The zircon.elf-gdb.py script  zircon.elf-gdb.py脚本 

The scripts/zircon.elf-gdb.py script is automagically loaded by gdb. It provides several things: 脚本/zircon.elf-gdb.py脚本由gdb自动加载。它提供了几件事：

 
- Pretty-printers for zircon objects (alas none at the moment).  -锆石物体的漂亮打印机（目前还没有）。

 
- Several zircon specific commands, all with a "zircon" prefix. To see them:  -几个特定于Zircon的命令，所有命令均带有“ zircon”前缀。去看他们：

```
(gdb) help info zircon
(gdb) help set zircon
(gdb) help show zircon
```
 

 
- Enhanced unwinder support for automagic unwinding through kernel faults.  -增强的解卷器支持通过内核故障自动解卷。

Heads up: This script isn't always updated as zircon changes.  请注意：该脚本并非总是随着锆石的变化而更新。

 
### Terminating the session  终止会议 

To terminate QEMU you can send commands to QEMU from GDB:  要终止QEMU，可以从GDB向QEMU发送命令：

```
(gdb) monitor quit
(gdb) quit
```
 

 
### Interacting with QEMU from Gdb  与Gdb中的QEMU进行交互 

To see the list of QEMU commands you can execute from GDB:  要查看可以从GDB执行的QEMU命令列表：

```
(gdb) monitor help
```
 

 
### Saving system state for debugging  保存系统状态以进行调试 

If you have a crash that is difficult to debug, or that you need help with debugging, it's possible to save system state akin to a core dump. 如果您遇到难以调试的崩溃，或者需要调试方面的帮助，则可以保存类似于核心转储的系统状态。

```
bash$ qemu-img create -f qcow2 /tmp/my_snapshots.qcow2 32M
```
 

will create a "32M" block storage device.  Next launch QEMU and tell it about the device, but don't tell it to attach the device to the guest system.This is OK; we don't plan on using it to back up the disk state, we just wanta core dump.  Note: all of this can be skipped if you are already emulatinga block device and it is using the qcow2 format. 将创建一个“ 32M”块存储设备。接下来启动QEMU并告诉它有关设备的信息，但是不要告诉它将设备连接到客户机系统。我们不打算使用它来备份磁盘状态，我们只是想要一个核心转储。注意：如果您已经在模拟块设备并且使用qcow2格式，则可以跳过所有这些操作。

```
bash$ qemu <normal_launch_args> -drive if=none,format=qcow2,file=/tmp/my_snapshots.qcow2
```
 

When you get to a point where you want to save the core state, drop to the QEMU console using <C-a><C-c>.  You should get the (qemu) prompt at this point.From here, just say: 当您要保存核心状态时，请使用<C-a> <C-c>转到QEMU控制台。此时您应该会收到（qemu）提示，从这里说：

```
(qemu) savevm my_backup_tag_name
```
 

Later on, from an identical machine (one launched with the same args as before), you can drop to the console and run: 稍后，从同一台机器（一台与以前相同的args启动的机器），您可以放到控制台并运行：

```
(qemu) loadvm my_backup_tag_name
```
 

to restore the state.  Alternatively, you can do it from the cmd line with:  恢复状态。或者，您可以从命令行使用以下命令执行此操作：

```
bash$ qemu <normal_launch_args> -drive if=none,format=qcow2,file=/tmp/my_snapshots.qcow2 -loadvm my_backup_tag_name
```
 

In theory, you could package up the qcow2 image along with your build output directory and anyone should be able to restore your state and start to pokeat stuff from the QEMU console. 从理论上讲，您可以将qcow2映像与构建输出目录打包在一起，任何人都应该能够恢复您的状态并开始从QEMU控制台中提取内容。

 

