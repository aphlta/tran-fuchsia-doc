 
# Getting started with Zircon  Zircon入门 

 
## Checking out the Zircon source code  签出Zircon源代码 

Note: The Fuchsia source includes Zircon. See Fuchsia's [Getting Started](/docs/getting_started.md) documentation. 注意：紫红色的来源包括锆石。请参阅Fuchsia的[使用入门]（/ docs / getting_started.md）文档。

 

This guide assumes that the Fuchsia project is checked out into $FUCHSIA_DIR, and `fx` has been configured. 本指南假定Fuchsia项目已签入$ FUCHSIA_DIR，并且已配置`fx`。

 
## Build Zircon with the default toolchain  使用默认工具链构建Zircon 

The `fx` command wraps the various tools used to configure, build and interact with Fuchsia. The `fx set` is used to specify the "bringup" product and the board architecture. The "bringup"product identifies the Zircon components and excludes all other Fuchsia components from the build.For example, to build Zircon for arm64: fx命令包装了用于配置，构建和与紫红色交互的各种工具。 “ fx set”用于指定“ bringup”产品和电路板架构。 “ bringup”产品标识Zircon组件，并从构建中排除所有其他的Fuchsia组件。例如，为arm64构建Zircon：

```sh
fx set bringup.arm64
```
 

Fuchsia uses the concept of [products](/docs/development/build/boards_and_products.md#products) to create a collection of build targets. The "bringup" product is the smallest product,other product configurations can be listed by running: 紫红色使用[产品]（/ docs / development / build / boards_and_products.mdproducts）的概念来创建构建目标的集合。 “ bringup”产品是最小的产品，其他产品配置可以通过运行列出：

```sh
fx list-products
```
 

The defined board architectures are listed by running:  通过运行列出已定义的板体系结构：

```sh
fx list-boards
```
 

To execute the build:  要执行构建：

```sh
fx build
```
 

The build results are saved in $FUCHSIA_DIR/out/default.zircon.  构建结果保存在$ FUCHSIA_DIR / out / default.zircon中。

 
## Explictly set the target toolchain  明确设置目标工具链 

By default Fuchsia uses the `clang` toolchain.  This can be set to `gcc` by using the `variants` argument with `fx set`: 紫红色默认使用`clang`工具链。可以通过在`fx set`中使用`variants`参数将其设置为`gcc`：

```sh
fx set bringup.x64 --variant gcc
```
 

You can also enable asan by using the variant flag.  您还可以通过使用variant标志启用asan。

 

 
## Building Zircon for all targets  为所有目标建造锆石 

You can build for all targets with `fx multi` and using a file that contains all the specifications to build. The outputfor each target is found in $FUCHSIA_DIR/out/<product>.<board>.variant.An example of a multi build spec is [bringup-cq](/tools/devshell/lib/multi-specs/bringup-cq)which approximates what is built for a CQ test. 您可以使用`fx multi`并使用包含所有要构建规范的文件来为所有目标构建。每个目标的输出都在$ FUCHSIA_DIR / out / <product>。<board> .variant中。多版本规格的示例是[bringup-cq]（/ tools / devshell / lib / multi-specs / bringup-cq ），这近似于为CQ测试构建的内容。

Please build for all targets before submitting to ensure builds work on all architectures. 在提交之前，请针对所有目标进行构建，以确保构建可在所有体系结构上进行。

 
## QEMU  量化宽松 

You can skip this if you're only testing on actual hardware, but the emulator is handy for quick local tests and generally worth having around. 如果仅在实际硬件上进行测试，则可以跳过此步骤，但是该仿真器非常方便进行快速本地测试，通常值得一试。

See [QEMU](/docs/development/emulator/qemu.md) for information on building and using QEMU with zircon.  请参阅[QEMU]（/ docs / development / emulator / qemu.md），以获取有关将QEMU与锆石一起使用和使用的信息。

 

 
## Build Toolchains (Optional)  构建工具链（可选） 

If the prebuilt toolchain binaries do not work for you, you can build your own from vanilla upstream sources. 如果预构建的工具链二进制文件不适合您，则可以从原始上游资源构建自己的二进制文件。

 
 * The Clang toolchain is used to build Zircon by default or if you build with `variants = [ "clang" ]` or `variants = [ "asan" ]`. *默认情况下，或者使用`variants = [“ clang”]`或`variants = [“ asan”]进行编译时，将使用Clang工具链来构建Zircon。
 * The Clang toolchain is also used by default to build host-side code, but any C++14-capable toolchain for your build host should work fine. *默认情况下，也使用Clang工具链来构建主机端代码，但是用于构建主机的任何具有C ++ 14功能的工具链都可以正常工作。
 * The GCC toolchain is also available.  *也提供GCC工具链。

Build one or the other or both, as needed for how you want build Zircon.  根据您要构建Zircon的需要，构建一个或另一个或两个。

 
### GCC Toolchain  GCC工具链 

We use GNU `binutils` 2.30[^1] and GCC 8.2, configured with `--enable-initfini-array --enable-gold`, and with `--target=x86_64-elf--enable-targets=x86_64-pep` for x86-64 or `--target=aarch64-elf` for ARM64. 我们使用GNU binutils 2.30 [^ 1]和GCC 8.2，分别配置为--enable-initfini-array --enable-gold和-target = x86_64-elf-enable-targets = x86_64- pep用于x86-64或--target = aarch64-elf用于ARM64。

For `binutils`, we recommend `--enable-deterministic-archives` but that switch is not necessary to get a working build. 对于`binutils`，我们推荐`--enable-deterministic-archives`，但是该开关对于获得有效的构建不是必需的。

For GCC, it's necessary to pass `MAKEOVERRIDES=USE_GCC_STDINT=provide` on the `make` command line.  This should ensure that the `stdint.h` GCC installs isone that works standalone (`stdint-gcc.h` in the source) rather than one thatuses `#include_next` and expects another `stdint.h` file installed elsewhere. 对于GCC，有必要在make命令行上传递MAKEOVERRIDES = USE_GCC_STDINT = provide。这应该确保安装的`stdint.h` GCC是独立运行的（源中的`stdint-gcc.h`），而不是使用`include_next`并且期望在其他位置安装了另一个`stdint.h`文件的GCC。

Only the C and C++ language support is required and no target libraries other than `libgcc` are required, so you can use various `configure` switches todisable other things and make your build of GCC itself go more quickly and useless storage, e.g. `--enable-languages=c,c++ --disable-libstdcxx--disable-libssp --disable-libquadmath`.  See the GCC installationdocumentation for more details. 仅需要C和C ++语言支持，而除了`libgcc`之外就不需要目标库，因此您可以使用各种`configure`开关来禁用其他功能，并使GCC本身的构建更快，更无用，例如。 --enable-languages = c，c ++ --disable-libstdcxx-disable-libssp --disable-libquadmath有关更多详细信息，请参见GCC安装文档。

You may need various other `configure` switches or other prerequisites to build on your particular host system.  See the GNU documentation. 您可能需要各种其他“配置”开关或其他先决条件才能在您的特定主机系统上构建。请参阅GNU文档。

[^1]: The `binutils` 2.30 release has some harmless `make check` failures in the `aarch64-elf` and `x86_64-elf` configurations.  These are fixed on theupstream `binutils-2_30-branch` git branch, which is what we actually build.But the 2.30 release version works fine for building Zircon; it just has somespurious failures in its own test suite. [^ 1]：binutils 2.30发行版在aarch64-elf和x86_64-elf配置中有一些无害的make make故障。这些已固定在上游binutils-2_30-branch` git分支上，这是我们实际构建的。但是2.30发行版可以很好地构建Zircon。它在自己的测试套件中仅存在一些虚假的故障。

 
### Clang/LLVM Toolchain  Clang / LLVM工具链 

We use a trunk snapshot of Clang and update to new snapshots frequently.  Any build of recent-enough Clang with support for `x86_64` and `aarch64` compiledin should work.  You'll need a toolchain that also includes the runtimelibraries.  We normally also use the same build of Clang for the host as wellas for the `*-fuchsia` targets.  See[here](/docs/development/build/toolchain.md)for details on how we build Clang. 我们使用Clang的主干快照，并经常更新到新快照。任何支持x86_64和aarch64的最近版本的Clang编译都应该起作用。您将需要一个包含运行时库的工具链。通常，我们也将相同版本的Clang用于主机以及`* -fuchsia`目标。请参阅[此处]（/ docs / development / build / toolchain.md），了解有关我们如何构建Clang的详细信息。

 
### Set up build arguments for toolchains  设置工具链的构建参数 

If you're using the prebuilt toolchains, you can skip this step, since the build will find them automatically. 如果您使用的是预先构建的工具链，则可以跳过此步骤，因为构建会自动找到它们。

Set the build argument that points to where you installed the toolchains:  设置构建参数以指向安装工具链的位置：

```sh
fx set bringup.x64 --variant clang --args clang_tool_dir = "<absolute path to>/clang-install/bin/"
```
 

or for GCC:  或对于GCC：

```sh
fx set bringup.x64 --variant gcc --args gcc_tool_dir = "<absolute path to>/gcc-install/bin/"
```
 

Note that `*_tool_dir` should have a trailing slash. If the `clang` or `gcc` in your `PATH` works for Zircon, you can just use empty prefixes. 注意`* _tool_dir`应该有一个斜杠。如果您的“ PATH”中的“ clang”或“ gcc”适用于Zircon，则可以使用空前缀。

 
## Copying files to and from Zircon  在Zircon之间复制文件 

With local link IPv6 configured you can use `fx cp` to copy files to and from the device. 配置了本地链接IPv6后，您可以使用“ fx cp”在设备之间复制文件。

 

 
## Including Additional Userspace Files  包括其他用户空间文件 

The Zircon build creates a bootfs image containing necessary userspace components for the system to boot (the device manager, some device drivers, etc).  The kernelis capable of including a second bootfs image which is provided by QEMU or thebootloader as a ramdisk image. Zircon构建会创建一个bootfs映像，其中包含系统启动所需的用户空间组件（设备管理器，某些设备驱动程序等）。内核能够包含第二个bootfs映像，该映像由QEMU或bootloader提供，作为ramdisk映像。

To create such a bootfs image, use the zbi tool that's generated as part of the build.  It can assemble a bootfs image for either source directories (in whichcase every file in the specified directory and its subdirectories are included) orvia a manifest file which specifies on a file-by-file basis which files to include. 要创建这样的bootfs映像，请使用在构建过程中生成的zbi工具。它可以为源目录（在这种情况下，指定目录中的每个文件及其子目录都包括在内）或清单文件（每个文件逐个指定要包括的文件）组装一个bootfs映像。

```
$BUILDDIR/tools/zbi -o extra.bootfs @/path/to/directory

echo "issue.txt=/etc/issue" > manifest
echo "etc/hosts=/etc/hosts" >> manifest
$BUILDDIR/tools/zbi -o extra.bootfs manifest
```
 

On the booted Zircon system, the files in the bootfs will appear under /boot, so in the above manifest example, the "hosts" file would appear at /boot/etc/hosts. 在引导的Zircon系统上，bootfs中的文件将出现在/ boot下，因此在上述清单示例中，“主机”文件将出现在/ boot / etc / hosts中。

 
## Network Booting  网络启动 

Network booting is supported via two mechanisms: Gigaboot and Zirconboot. Gigaboot is an EFI based bootloader whereas zirconboot is a mechanism thatallows a minimal zircon system to serve as a bootloader for zircon. 通过两种机制支持网络启动：Gigaboot和Zirconboot。 Gigaboot是基于EFI的引导程序，而zirconboot是一种机制，它允许最小的Zircon系统充当Zircon的引导程序。

On systems that boot via EFI (such as Acer and NUC), either option is viable. On other systems, zirconboot may be the only option for network booting. 在通过EFI引导的系统（例如Acer和NUC）上，这两种方法都是可行的。在其他系统上，zirconboot可能是网络引导的唯一选项。

 
### Via Gigaboot  通过GigabootThe [GigaBoot20x6](/zircon/bootloader) bootloader speaks a simple network boot protocol (over IPV6 UDP) which does not require any special host configuration or privileged access to use. [GigaBoot20x6]（/ zircon / bootloader）引导程序讲一种简单的网络引导协议（通过IPV6 UDP），不需要任何特殊的主机配置或特权访问。

It does this by taking advantage of IPV6 Link Local Addressing and Multicast, allowing the device being booted to advertise its bootability and the host to findit and send a system image to it. 它通过利用IPV6链路本地寻址和多播功能来做到这一点，从而使被引导的设备能够公告其可引导性，而主机则可以找到它并向其发送系统映像。

If you have a device (for example a Broadwell or Skylake Intel NUC) running GigaBoot20x6, first [create a USB drive](/docs/development/hardware/usb_setup.md). 如果您有运行GigaBoot20x6的设备（例如Broadwell或Skylake Intel NUC），请首先[创建USB驱动器]（/ docs / development / hardware / usb_setup.md）。

```
$BUILDDIR/tools/bootserver $BUILDDIR/zircon.bin

# if you have an extra bootfs image (see above):
$BUILDDIR/tools/bootserver $BUILDDIR/zircon.bin /path/to/extra.bootfs
```
 

By default bootserver will continue to run and every time it observes a netboot beacon it will send the kernel (and bootfs if provided) to that device.  If youpass the -1 option, bootserver will exit after a successful boot instead. 默认情况下，bootserver将继续运行，并且每次观察到netboot信标时，它将把内核（和bootfs，如果提供）发送到该设备。如果您通过-1选项，则引导服务器将在成功引导后退出。

 

 
### Via Zirconboot  通过ZirconbootZirconboot is a mechanism that allows a zircon system to serve as the bootloader for zircon itself. Zirconboot speaks the same boot protocol asGigaboot described above. Zirconboot是一种机制，它允许Zircon系统充当Zircon本身的引导程序。 Zirconboot的引导协议与上述Gigaboot相同。

To use zirconboot, pass the `netsvc.netboot=true` argument to zircon via the kernel command line. When zirconboot starts, it will attempt to fetch and bootinto a zircon system from a bootserver running on the attached host. 要使用zirconboot，请通过内核命令行将`netsvc.netboot = true`参数传递给zircon。当zirconboot启动时，它将尝试从在连接的主机上运行的引导服务器获取并引导进入Zircon系统。

 
## Network Log Viewing  网络日志查看 

The default build of Zircon includes a network log service that multicasts the system log over the link local IPv6 UDP.  Please note that this is a quick hackand the protocol will certainly change at some point. Zircon的默认内部版本包括网络日志服务，该服务通过链接本地IPv6 UDP多播系统日志。请注意，这是一个快速的技巧，协议肯定会在某个时候改变。

For now, if you're running Zircon on QEMU with the -N flag or running on hardware with a supported ethernet interface (ASIX USB Dongle or Intel Ethernet on NUC),the loglistener tool will observe logs broadcast over the local link: 现在，如果您在带有-N标志的QEMU上运行Zircon或在具有受支持的以太网接口（NUX上的ASIX USB Dongle或Intel以太网）的硬件上运行，loglistener工具将观察通过本地链接广播的日志：

```
$BUILDDIR/tools/loglistener
```
 

 
## Debugging  调试 

For random tips on debugging in the zircon environment see [debugging](/docs/development/debugging/tips.md). 有关在Zircon环境中进行调试的随机提示，请参见[debugging]（/ docs / development / debugging / tips.md）。

 
## Contribute changes  贡献变化 
