 
# Fuchsia  紫红色 

Pink + Purple == Fuchsia (a new Operating System)  粉色+紫色==紫红色（新操作系统）

Welcome to Fuchsia! This document has everything you need to get started with Fuchsia. 欢迎来到紫红色！本文档包含您开始使用紫红色的一切。

Note: The Fuchsia source includes [Zircon](/zircon/README.md), the core platform that underpins Fuchsia. The Fuchsia build process willbuild Zircon as a side-effect; to work on Zircon only, read and followZircon's [Getting Started](/docs/development/kernel/getting_started.md) doc. 注意：紫红色的来源包括[Zircon]（/ zircon / README.md），它是支持紫红色的核心平台。紫红色的建造过程会产生锆石的副作用。要仅在Zircon上工作，请阅读并遵循Zircon的[Getting Started]（/ docs / development / kernel / getting_started.md）文档。

[TOC]  [目录]

 
## Prerequisites  先决条件 

 
### Prepare your build environment (once per build environment)  准备构建环境（每个构建环境一次） 

 
#### Debian  德比安 

```
sudo apt-get install build-essential curl git python unzip
```
 

 
#### macOS  苹果系统 

 
1.  Install Command Line Tools:  1.安装命令行工具：

    ```
    xcode-select --install
    ```
 

 
1.  In addition to Command Line Tools, you also need to install a recent version of [Xcode](https://developer.apple.com/xcode/). 1.除了命令行工具外，您还需要安装[Xcode]（https://developer.apple.com/xcode/）的最新版本。

 
## Get the Source  获取来源 

Follow [the instructions to get the Fuchsia source](development/source_code/README.md) and then return to this document. 请按照[获取紫红色来源的说明]（development / source_code / README.md），然后返回此文档。

 
## Build Fuchsia  建立紫红色 

Note: A quick overview of the basic build-and-pave workflow can be found [here](development/workflows/build_and_pave_quickstart.md).  注意：可以在[此处]（development / workflows / build_and_pave_quickstart.md）中找到基本的构建和铺装工作流程的快速概述。

 

If you added `.jiri_root/bin` to your path as part of getting the source code, the `fx` command should already be in your path. If not, the command is alsoavailable as `scripts/fx`. 如果作为获取源代码的一部分在路径中添加了.jiri_root / bin，则fx命令应该已经在您的路径中。如果没有，该命令也可以作为`scripts / fx`使用。

```sh
fx set core.x64 --with //bundles:kitchen_sink
fx build
```
 

The `fx set` command configures the contents of your build and generates build rules and metadata in the default output directories, `out/default` and`out/default.zircon`. The argument `core.x64` refers to[product and board definitions](development/build/boards_and_products.md) thatdescribe, among other things, what packages are built and availableto your Fuchsia device. fx set命令配置构建的内容，并在默认输出目录out / default和out / default.zircon中生成构建规则和元数据。参数`core.x64`指的是[产品和电路板定义]（development / build / boards_and_products.md），它描述了构建或可用于您的Fuchsia设备的软件包。

A Fuchsia device can ephemerally download and install packages over the network, and in a development environment, your development workstation is the source ofthese ephemeral packages. The board and product definitions contain a set of packages,but if you need to add other packages, use the `--with` flag. This exampleincludes `kitchen_sink`, which is an idiom in english meaning "practicallyeverything". As you become more focused in your development, you will probablyuse more specific `--with` options to minimize build times. 紫红色的设备可以通过网络临时下载和安装软件包，在开发环境中，您的开发工作站就是这些临时软件包的来源。电路板和产品定义包含一组软件包，但是如果您需要添加其他软件包，请使用--with标志。此示例包括“ kitchen_sink”，它是英语中的一个成语，意思是“实践中的一切”。随着您更加专注于开发，您可能会使用更具体的“ --with”选项来最大程度地减少构建时间。

The `fx build` command executes the build, transforming source code into packages and other build artifacts. If you modify source code,you can do an incremental build by re-running the `fx build` command alone.`fx -i build` starts a watcher and automatically builds whenever a file is changed. “ fx build”命令执行构建，将源代码转换为包和其他构建工件。如果您修改源代码，则可以通过单独重新运行fx build命令来进行增量构建。fx -i build启动观察程序并在文件更改时自动进行构建。

See the [underlying build system](development/build/README.md) for more details.  有关更多详细信息，请参见[底层构建系统]（development / build / README.md）。

{% dynamic if user.is_googler %}  {如果user.is_googler％，则为动态％}
### Accelerate the build with goma  使用goma加速构建 

`goma` accelerates builds by distributing compilation across many machines.  If you have `goma` installed in `~/goma`, it is used by default. `goma`通过在许多机器之间分布编译来加速构建。如果您在`〜/ goma`中安装了`goma`，则默认使用它。

If goma cannot be found, `ccache` is used if available.  如果无法找到goma，则使用`ccache`（如果可用）。

It is also used by default in preference to `ccache`.  默认情况下，它也优先于`ccache`使用。

To disable using goma, pass `--no-goma` to `fx set`.  要禁用使用goma，请将`--no-goma`传递给`fx set`。

{% dynamic endif %}  {％动态endif％}

 
### _Optional:_ Accelerate the build with ccache  _Optional：_使用ccache加速构建[`ccache`](https://ccache.dev/){: .external} accelerates builds by caching artifacts from previous builds. `ccache` is enabled automatically if the `CCACHE_DIR` environmentvariable is set and refers to a directory that exists. [`ccache`]（https://ccache.dev/）{：.external}通过缓存来自先前构建的工件来加速构建。如果设置了“ CCACHE_DIR”环境变量并引用了一个存在的目录，则“ ccache”会自动启用。

To override the default behaviors, pass flags to `fx set`:  要覆盖默认行为，请将标志传递给`fx set`：

```sh
--ccache     # force use of ccache even if goma is available
--no-ccache  # disable use of ccache
```
 

 
## Boot Fuchsia  引导紫红色 

 
### Installing and booting from hardware  从硬件安装和引导 

To get Fuchsia running on hardware requires using the paver, which these [instructions](development/workflows/paving.md) will help you get up and runningwith. 要使Fuchsia在硬件上运行，需要使用摊铺机，这些[说明]（开发/工作流程/paving.md）将帮助您起步并开始使用。

Note: A quick overview of the basic build-and-pave workflow can be found [here](development/workflows/build_and_pave_quickstart.md). 注意：可以在[此处]（development / workflows / build_and_pave_quickstart.md）中找到基本的构建和铺装工作流程的快速概述。

 
### Boot from QEMU  从QEMU引导 

If you don't have the supported hardware, you can run Fuchsia under emulation using [QEMU](/docs/development/emulator/qemu.md).Fuchsia includes prebuilt binaries for QEMU under `prebuilt/third_party/qemu`. 如果您没有受支持的硬件，则可以使用[QEMU]（/ docs / development / emulator / qemu.md）在仿真下运行Fuchsia。Fuchsia在“ prebuilt / third_party / qemu”下包括QEMU的预构建二进制文件。

The `fx emu` command will launch Fuchsia within QEMU, using the locally built disk image: fx emu命令将使用本地构建的磁盘映像在QEMU中启动Fuchsia：

```sh
fx emu
```
 

There are various flags for `fx emu` to control the emulator configuration:  fx emu有各种标志来控制仿真器配置：

 
* `-N` enables networking (see below).  *`-N`启用网络连接（见下文）。
* `--headless` disable graphics (see below).  *`--headless`禁用图形（见下文）。
* `-c` pass additional arguments to the kernel.  * -c将附加参数传递给内核。

Use `fx emu -h` to see all available options.  使用`fx emu -h`查看所有可用选项。

Note: Before you can run any commands, you will need to follow the instructions in the [Explore Fuchsia](#explore-fuchsia) section below.  注意：在运行任何命令之前，您需要按照下面的[Explore Fuchsia]（explore-fuchsia）部分中的说明进行操作。

 
#### Enabling Network  启用网络 

In order for ephemeral software to work in the emulator, an IPv6 network must be configured. 为了使临时软件在仿真器中工作，必须配置IPv6网络。

On macOS: Install "http://tuntaposx.sourceforge.net/download.xhtml" On Linux: Run `sudo ip tuntap add dev qemu mode tap user $USER && sudo ip link set qemu up` 在macOS上：安装“ http://tuntaposx.sourceforge.net/download.xhtml”。在Linux上：运行`sudo ip tuntap add dev qemu mode tap user $ USER sudo ip link set qemu`

Now the emulator can be run with networking enabled:  现在，仿真器可以在启用网络的情况下运行：

```
fx emu -N
```
 

The above is sufficient for ephemeral software (that is served by `fx serve`, see below) to work, including many tools such as `uname` and `fortune` (ifbuilt). 上面的内容足以使临时软件（由fx serve提供服务，请参见下文）工作，包括许多工具，如uname和fortune（如果已构建）。

Users who also wish to reach the internet from the emulator will need to configure some manner of IP forwarding and IPv4 support on the emulator TAPinterface. Details of this process are beyond the scope of this document. 还希望从仿真器访问Internet的用户将需要在仿真器TAP接口上配置某种IP转发和IPv4支持的方式。此过程的详细信息超出了本文档的范围。

 
## Explore Fuchsia {#explore-fuchsia}  探索紫红色{explore-fuchsia} 

In a separate shell, start the development update server, if it isn't already running: 在单独的外壳中，启动开发更新服务器（如果尚未运行）：

```sh
fx serve
```
 

Boot Fuchsia with networking. This can be done either in QEMU via the `-N` flag, or on a paved hardware, both described above.When Fuchsia has booted and displays the "$" shell prompt, you can run programs! 通过网络启动紫红色。这可以通过QEMU中的-N标志来完成，也可以在已安装的硬件上完成，如上所述。当Fuchsia启动并显示“ $” shell提示符时，您可以运行程序！

For example, to receive deep wisdom, run:  例如，要获得深刻的智慧，请运行：

```sh
fortune
```
 

To shutdown or reboot Fuchsia, use the `dm` command:  要关闭或重启紫红色，请使用`dm`命令：

```sh
dm shutdown
dm reboot
```
 

 
### Change some source  更改一些来源 

Almost everything that exists on a Fuchsia system is stored in a Fuchsia package. A typical development[workflow](development/workflows/package_update.md) involves re-building andpushing Fuchsia packages to a development device or QEMU virtual device. 紫红色系统上几乎所有的东西都存储在紫红色的包装中。典型的开发[工作流程]（development / workflows / package_update.md）涉及将紫红色的软件包重新构建并推送到开发设备或QEMU虚拟设备。

Make a change to the rolldice binary in `examples/rolldice/src/main.rs`.  在`examples / rolldice / src / main.rs`中更改rolldice二进制文件。

Re-build and push the rolldice package to a running Fuchsia device with:  重新构建rolldice软件包并将其推入运行中的Fuchsia设备，方法是：

```sh
fx build-push rolldice
```
 

From a shell prompt on the Fuchsia device, run the updated rolldice component with: 在Fuchsia设备的shell提示符下，使用以下命令运行更新的rolldice组件：

```sh
rolldice
```
 

 
### Select a tab  选择一个标签 

Fuchsia shows multiple tabs after booting [with graphics enabled](#enabling-graphics). The currently selected tab is highlighted inyellow at the top of the screen. 紫红色在启动[启用图形]（启用图形）后显示多个选项卡。当前选择的选项卡在屏幕顶部以黄色突出显示。

The following keyboard shortcuts help you navigate the terminal:  以下键盘快捷键可帮助您浏览终端：

 
- Alt+Tab switches between tabs.  -Alt + Tab在选项卡之间切换。
- Alt+F{1,2,...} switches directly to a tab.  -Alt + F {1,2，...}直接切换到标签。
  - Tab zero is the console, which displays the boot and component log.  -选项卡零是控制台，它显示引导和组件日志。
  - Tabs 1, 2 and 3 contain shells.  -选项卡1、2和3包含外壳。
  - Tabs 4 and higher contain components you've launched.  -标签4和更高版本包含您已启动的组件。
- Alt+Up/Down scrolls up and down by lines.  -Alt + Up / Down按行上下滚动。
- Shift+PgUp/PgDown scrolls up and down by half page.  -Shift + PgUp / PgDown上下滚动半页。
- Ctrl+Alt+Delete reboots.  -Ctrl + Alt + Delete重新启动。

Note: To select tabs, you may need to enter "console mode". See the next section for details.  注意：要选择选项卡，您可能需要输入“控制台模式”。有关详细信息，请参见下一部分。

 
### Launch a graphical component  启动图形组件 

Warning: QEMU does not support Vulkan and therefore cannot run our graphics stack. Commands in this section will not work on QEMU.  警告：QEMU不支持Vulkan，因此无法运行我们的图形堆栈。本节中的命令不适用于QEMU。

Most graphical components in Fuchsia use the [Scenic](/src/ui/scenic/) system compositor. You can launch such components, commonly found in `/system/apps`,like this: 紫红色中的大多数图形组件都使用[Scenic]（/ src / ui / scenic /）系统合成器。您可以启动通常在`/ system / apps`中找到的此类组件，如下所示：

```sh
present_view fuchsia-pkg://fuchsia.com/spinning_square_view#meta/spinning_square_view.cmx
```
 

Source code for Scenic example apps is [here](/src/ui/examples).  Scenic示例应用程序的源代码是[here]（/ src / ui / examples）。

When you launch something that uses Scenic, uses hardware-accelerated graphics, or if you build the [default](https://fuchsia.googlesource.com/topaz/+/master/packages) package (which willboot into the Fuchsia System UI), Fuchsia will enter "graphics mode", which will not display anyof the text shells. In order to use the text shell, you will need to enter "console mode" bypressing Alt-Escape. In console mode, Alt-Tab will have the behavior described in the previoussection, and pressing Alt-Escape again will take you back to the graphical shell. 当您启动使用Scenic的东西时，使用硬件加速的图形，或者您构建了[default]（https://fuchsia.googlesource.com/topaz/+/master/packages）程序包（它将引导进入Fuchsia系统UI） ），紫红色将进入“图形模式”，该模式将不显示任何文本外壳。为了使用文本外壳，您将需要通过按Alt-Escape进入“控制台模式”。在控制台模式下，Alt-Tab将具有上一节中所述的行为，再次按Alt-Escape将使您返回图形外壳。

 
## Running tests  运行测试 

Compiled test binaries are cached in pkgfs like other components, and are referenced by a URI. You can run a test by invoking it in the terminal. For example: 像其他组件一样，已编译的测试二进制文件也缓存在pkgfs中，并由URI引用。您可以通过在终端中调用来运行测试。例如：

```sh
run fuchsia-pkg://fuchsia.com/ledger_tests#meta/ledger_unittests.cmx
```
 

If you want to leave Fuchsia running and recompile and re-run a test, run Fuchsia with networking enabled in one terminal, then in another terminal, run: 如果要让Fuchsia保持运行状态，然后重新编译并重新运行测试，请在一个终端中启用联网的情况下运行Fuchsia，然后在另一终端中运行：

```sh
fx run-test <test name> [<test args>]
```
 

You may wish to peruse the [testing FAQ](development/testing/faq.md).  您不妨仔细阅读[测试常见问题解答]（development / testing / faq.md）。

 
## Contribute changes  贡献变化 

 
* See [CONTRIBUTING.md](/CONTRIBUTING.md).  *请参阅[CONTRIBUTING.md]（/ CONTRIBUTING.md）。

 
## Additional helpful documents  其他有用的文件 

 
* [Fuchsia documentation](README.md) hub  * [紫红色文档]（README.md）集线器
* Working with Zircon - [copying files, network booting, log viewing, and more](/docs/development/kernel/getting_started.md#Copying-files-to-and-from-Zircon) *使用Zircon-[复制文件，网络启动，日志查看等]（/docs/development/kernel/getting_started.md将文件复制到Zircon和从Zircon复制）
* [Documentation Standards](/docs/contribute/best-practices/documentation_standards.md) - best practices for documentation * [文档标准]（/ docs / contribute / best-practices / documentation_standards.md）-文档的最佳做法
* [Information on the system bootstrap component](/src/sys/sysmgr/).  * [有关系统引导程序组件的信息]（/ src / sys / sysmgr /）。
