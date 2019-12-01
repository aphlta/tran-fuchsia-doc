 
# fx workflows  FX工作流程 

`fx` is the front-door to a collection of scripts that make many tasks related to Fuchsia development easier. It contains a large number ofsubcommands, which can be discovered by running `fx help`. If you use `bash`or `zsh` as a shell, you can get some auto-completion for `fx` by sourcing`scripts/fx-env.sh` into your shell. fx是一系列脚本的前门，这些脚本使许多与Fuchsia开发相关的任务变得更加容易。它包含大量子命令，可以通过运行`fx help`来发现。如果您将`bash`或`zsh`用作shell，则可以通过将`scripts / fx-env.sh`采购到shell中来自动完成`fx`。

 
## Setting up fx {#setting-up-fx}  设置FX {setting-up-fx} 

It is strongly recommended that you `source scripts/fx-env.sh` into your shell. This is tested and regularly used with Bash and ZSH. It may work forother compatible shells. 强烈建议您将“ scripts / fx-env.sh”源到您的shell中。这是经过测试并经常与Bash和ZSH一起使用的。它可能适用于其他兼容的外壳。

```shell
# In your fuchsia checkout:
$ cd fuchsia
# Add a configuration to your shell to include fx-env.sh
$ echo "source \"$PWD/scripts/fx-env.sh\"" >> "$HOME/.$(basename "$SHELL")rc"
# If you would like additional convenience tools from the Fuchsia scripts, also
# optionally run the following:
$ echo "fx-update-path" >> "$HOME/.$(basename "$SHELL")rc"
# Restart your shell
$ exec "$SHELL"
```
 

The above method provides the most well defined feature set, and should be generally non-invasive. If it causes bugs in your shell environment, pleasefile project bugs. 上面的方法提供了定义最明确的功能集，通常应该是非侵入性的。如果它在您的Shell环境中引起错误，请提交项目错误。

If for some reason you need to work with multiple Fuchsia checkouts (recommended workflows below should obviate such a need), then you may wishto do something other than the above. In this case, there are a few wellsupported methods: 如果由于某种原因您需要使用多个Fuchsia结帐（下面的推荐工作流程应避免这种需求），那么您可能希望做除上述之外的事情。在这种情况下，有一些受支持的方法：

 
* Always execute `$FUCHSIA_DIR/scripts/fx` explicitly  *始终明确执行`$ FUCHSIA_DIR / scripts / fx`
* Use something like a cdenter or dotenv feature to add `$FUCHSIA_DIR/.jiri_root/bin` to your `$PATH` while working in a particularFuchsia directory. *使用cdenter或dotenv功能，在特定的Fuchsia目录中工作时，将$ FUCHSIA_DIR / .jiri_root / bin添加到$ PATH中。

Caution: It is not recommended (though presently works) to copy `fx` to other places, such as `~/bin/fx` (as this could one day break), or to add`$FUCHSIA_DIR/scripts` to your `$PATH` (as reviewers of code in `//scripts`)do not block the addition of files in that directory which could lead tounpredictable behaviors (for example, that directory contains binaries withgeneric names like "bootstrap" which may unintentionally override thebehavior of other systems).cco 注意：不建议（尽管目前可行）将fx复制到其他地方，例如〜/ bin / fx（因为这可能一天休息），或将$ FUCHSIA_DIR / scripts添加到您的` $ PATH`（作为“ // scripts”中代码的审阅者）不会阻止在该目录中添加文件，这可能导致无法预料的行为（例如，该目录包含具有通用名称的二进制文件，例如“ bootstrap”，可能会无意中覆盖该文件的行为）其他系统）.cco
## Common daily tools {#common-daily-tools}  日常常用工具{common-daily-tools} 

The first thing you will want to do after checking out a Fuchsia tree is to build Fuchsia, and then get it onto a device. `fx` has some commands to helpwith this: 检出紫红色的树后，您要做的第一件事是构建紫红色，然后将其安装到设备上。 `fx`有一些命令可以帮助您：

 
* `fx set` [configure a build](#configure-a-build)  *`fx set` [配置内部版本]（configure-a-build）
* `fx build` [execute a build](#execute-a-build)  *`fx build` [执行构建]（execute-a-build）
* `fx flash ; fx mkzedboot` [flash a target; or prepare a zedboot USB key](#flash-a-board-and-prepare-zedboot)  *`fx闪光; fx mkzedboot` [刷新目标；或准备一个zedboot USB密钥]（闪存并准备zedboot）
* `fx serve` [serve a build](#serve-a-build)  *`fx serve` [服务构建]（serve-a-build）
* `fx update` [update a target](#update-a-target-device)  *`fx update` [更新目标]（更新目标设备）
* `fx run-test` [execute tests](#execute-tests)  *`fx run-test` [执行测试]（execute-tests）
* `fx shell` [connect to a target shell](#connect-to-a-target-shell)  *`fx shell` [连接到目标外壳]（连接到目标外壳）
* [and many other small tasks](#performing-other-common-tasks)  * [和许多其他小任务]（执行其他常见任务）

 
## Configure a build {#configure-a-build}  配置构建{configure-a-build} 

First let's configure the build. To do this we need to make a few choices:  首先，让我们配置构建。为此，我们需要做出一些选择：

 
* What [product configuration](#key-product-configurations) do you want? (unsure: try `workstation`) *您想要什么[产品配置]（关键产品配置）？ （不确定：尝试使用“工作站”）
* What board are you building for? (unsure: try `x64`)  *您要为哪个板子建造？ （不确定：尝试使用“ x64”）
* What extra [bundles](#key-bundles) do you want? (unsure: try `tools`, and if you're working on features, you probably want `tests`) *您还想要什么[捆绑包]（钥匙包）？ （不确定：尝试使用“工具”，如果您正在使用功能，则可能需要使用“测试”）

Armed with our above choices (if you didn't read above, do so now), you are ready to configure your build: 有了我们上面的选择（如果您没有阅读上面的内容，请现在就做），您就可以配置构建了：

```shell
$ fx set workstation.x64 --with //bundles:tests
```
 

This command stores the configuration in an `args.gn` file in the build directory (which is `out/default` by default). You can edit this file using the`fx args` command to create more elaborate configurations. 该命令将配置存储在构建目录的“ args.gn”文件中（默认为“ out / default”）。您可以使用fx args命令编辑此文件以创建更详细的配置。

 
### What just happened?  刚刚发生了什么？ 

 
* We selected the architecture `x64`  *我们选择了架构“ x64”
* We selected the product `workstation` (run `fx list-products` for a list of other product configurations) *我们选择了产品“工作站”（运行“ fx list-products”以获取其他产品配置的列表）
* We selected the board `x64` (on arm64 boards, the board choice is very important! Run `fx list-boards` for a list of board configurations) *我们选择了板卡“ x64”（在arm64板上，板卡的选择非常重要！运行“ fx list-boards”以获取板卡配置列表）
* We selected to build "tests", but not have them included in our [paving](#what-is-paving) images. *我们选择构建“测试”，但没有将它们包含在我们的[铺装]（正在铺装）图像中。

So what are `base`, `cache` and `universe`? (new names)  那么什么是base，cache和Universe？ （新名称）

Configurations ultimately specify dependencies (mostly packages) that contribute to output artifacts of the build (mostly images and packagerepositories). The build is parameterized to determine which dependencies(mostly packages) are added to which output artifacts (images or packagerepositories). The three axes are called "base", "cache", and "universe": 配置最终指定了依赖关系（主要是软件包），这些依赖关系会导致构建的输出工件（主要是映像和软件包存储库）。对构建进行参数化，以确定将哪些依赖项（主要是软件包）添加到哪些输出工件（图像或软件包存储库）。这三个轴称为“基础”，“高速缓存”和“通用”：

 
* *Base*: Packages that are added to base are included in [paving](#what-is-paving) images produced by the build. They are included inover-the-air updates, and are always updated as a single unit. Packages inbase can not be evicted from a device at runtime - they encode theminimum possible size of a configuration. * *基础*：添加到基础的软件包包含在构建生成的[paving]（正在铺装）图像中。它们包含在空中更新中，并且始终作为一个单元进行更新。无法在运行时从设备中收回inbase软件包-它们对配置的最小可能大小进行编码。
* *Cache*: Packages in cache are included in [paving](#what-is-paving) images, but they are not included in over-the-airsystem updates, and are allowed to be evicted from the system in response toresource demands, such as disk-space pressure. Packages in cache can beupdated at any time that updates are available, and each of these packagesmay be updated independently. This is software that is "optional", but isgood to have available instantly "out of the box". * *缓存*：缓存中的程序包包含在[铺装]（正在铺装）图像中，但不包含在空中更新中，因此可以根据资源需求从系统中逐出，例如磁盘空间压力。缓存中的软件包可以在有可用更新的任何时间进行更新，并且每个软件包都可以独立更新。这是“可选”软件，但可以“即开即用”地立即使用。
* *Universe*: Packages in universe are additional optional packages that can be fetched and run on-demand, but are not pre-baked into any[paving](#what-is-paving) images. * * Universe *：Universe中的程序包是其他可选程序包，可以按需获取和运行，但不能预烘焙到任何[paving]（正在铺装）图像中。

The "board" and "product" configurations pick a predefined set of members for each of these package sets. Most commonly the board configurations specify aset of boot-critical drivers to add to the base dependency set, and couldfor example include some optional but common peripheral drivers in thecache set. The board configuration may also include some board-specificdevelopment tools (more commonly host tools, rather than target packages) forinteracting with the board in "universe". The product configurations makechoices to add more or less software to the base, cache or universepackage sets based on the definition and feature set of the product theyrepresent. A speaker product, for example, adds many audio-media-relatedpackages to the base. A workstation product adds a wide range of GUI,media and many other packages to the base. “板”和“产品”配置为这些包装组中的每个包装组选择了一组预定义的成员。最常见的板配置指定一组启动关键的驱动程序以添加到基本依赖项集，例如可以在缓存集中包括一些可选的但通用的外围设备驱动程序。电路板配置可能还包括一些特定于电路板的开发工具（更常见的是主机工具，而不是目标软件包），用于在“ Universe”中与电路板进行交互。产品配置可以根据它们所代表的产品的定义和功能集，选择向基本，高速缓存或Universe软件包集中添加更多或更少的软件。例如，扬声器产品在基座上增加了许多与音频媒体相关的程序包。工作站产品为基础增加了各种GUI，媒体和许多其他软件包。

 
### Key product configurations {#key-product-configurations}  关键产品配置{key-product-configurations} 

There are many more than below, but the following three particularly important configurations to be familiar with: 除了下面的内容外，还有很多其他内容，但您需要熟悉以下三个特别重要的配置：

 
* `bringup` is a minimal feature set product that is focused on being very simple and very lean. It exists to provide fast builds and small images(primarily used in a [netboot](#what-is-netbooting) rather than[paved](#what-is-paving) fashion), and is great for working on verylow-level facilities, such as the Zircon kernel or board-specific driversand configurations. It lacks most network capabilities, and therefore isnot able to add new software at runtime or upgrade itself. *`bringup`是一个最小的功能集产品，致力于非常简单和精益。它的存在是为了提供快速的构建和较小的映像（主要用于[netboot]（是什么，netbooting）而不是[paved]（是，什么是铺砌）时尚），并且非常适合用于非常底层的设施，例如Zircon内核或特定于板的驱动程序和配置。它缺少大多数网络功能，因此无法在运行时添加新软件或自行升级。
* `core` is a minimal feature set that can install additional software (such as items added to the "universe" dependency set). It is the starting point forall higher-level product configurations. It has common network capabilitiesand can update a system over-the-air. *`core`是最小功能集，可以安装其他软件（例如添加到“ Universe”依赖集的项）。这是所有更高级别产品配置的起点。它具有通用的网络功能，可以通过无线方式更新系统。
* `workstation` is a basis for a general purpose development environment, good for working on UI, media and many other high-level features. This is alsothe best environment for enthusiasts to play with and explore. *“工作站”是通用开发环境的基础，非常适合使用UI，媒体和许多其他高级功能。这也是发烧友玩耍和探索的最佳环境。

 
### Key bundles {#key-bundles}  钥匙包{key-bundles} 

As with products, there are many more, but the following bundles are most important to be familiar with: 与产品一样，还有更多，但以下捆绑对于您来说是最重要的：

 
* `tools` contains a broad array of the most common developer tools. This includes tools for spawning components from command-line shells, tools forreconfiguring and testing networks, making http requests, debuggingprograms, changing audio volume, and so on. The core product includes`bundles:tools` in the universe package set by default. *`tools`包含各种最常见的开发人员工具。这包括用于从命令行外壳生成组件的工具，用于重新配置和测试网络，发出http请求，调试程序，更改音频音量等的工具。核心产品在默认情况下设置的Universe软件包中包含“ bundles：tools”。
* `tests` causes all test programs to be built. Most test programs can be invoked using `run-test-component` on the device, or via `fx run-test`. *`tests`导致所有测试程序被构建。大多数测试程序可以使用设备上的“运行测试组件”或通过“ fx运行测试”来调用。
* `kitchen_sink` is a target that causes all other build targets to be included. It is useful when testing the impact of core changes, or whenmaking large scale changes in the code base. It also may be a funconfiguration for enthusiasts to play with, as it includes all softwareavailable in the source tree. Note that kitchen sink will produce more than20GB of build artifacts and requires at least 2GB of storage on the targetdevice (size estimates from Q1/2019). *`kitchen_sink`是一个导致所有其他构建目标都包括在内的目标。在测试核心更改的影响或在代码库中进行大规模更改时，此功能很有用。对于发烧友来说，这可能也是一种有趣的配置，因为它包括源代码树中所有可用的软件。请注意，厨房水槽将产生超过20GB的构件，并在目标设备上至少需要2GB的存储空间（根据2019年第一季度的估计量）。

 
## Execute a build {#execute-a-build}  执行构建{execute-a-build} 

For most use cases, only `fx build` is needed. `fx build` builds both Zircon and the Fuchsia portions of the build. The build process is optimizedfor fast incremental rebuilds, as such, repeating this command does theminimal work required after code has been changed, and no work if the sourcefiles are unchanged. 对于大多数用例，只需要`fx build`。 `fx build`会同时构建锆石和紫红色部分。生成过程已针对快速增量重建进行了优化，因此，重复此命令可以在代码更改后执行所需的最少工作，并且在源文件不变的情况下不会执行任何工作。

Additionally to `fx build`, a few other build related commands provide more granular control: 除了`fx build`，其他一些与构建相关的命令还提供了更精细的控制：

 
* `fx clean` clear out all build artifacts.  *`fx clean`清除所有构建工件。
* `fx clean-build` perform a clean, then a build.  *`fx clean-build`先执行清洁，然后进行构建。
* `fx gen` repeat the `gn gen` process that `fx set` performed. Users making fine grained build argument changes (e.g. by editing `args.gn` directly) canrun `fx gen` to reconfigure their build. *`fx gen`重复执行`fx set`执行的`gn gen`过程。进行细粒度的构建参数更改的用户（例如，通过直接编辑args.gn）可以运行fx gen来重新配置其构建。

 
### Building a specific target {#building-a-specific target}  建立特定目标{建立特定目标} 

`fx build` can be given the name of a specific target or file to build. For example, a target with the label `//examples/hello_world:hello_world` can be built with`fx build examples/hello_world:hello_world`. 可以给“ fx build”指定要构建的特定目标或文件的名称。例如，可以使用fx build examples / hello_world：hello_world构建带有标签“ // examples / hello_world：hello_world”的目标。

Note that this only works for targets declared in the default GN toolchain. For targets in other toolchains, the path of an output file may be used instead. Forexample, an executable target with the label`//foo/bar:blah(//build/toolchain:host_x64)` can be built with`fx build <output_dir>/host_x64/blah`. 请注意，这仅适用于默认GN工具链中声明的目标。对于其他工具链中的目标，可以代替使用输出文件的路径。例如，可以使用fx build <output_dir> / host_x64 / blah来构建标签为// foo / bar：blah（// build / toolchain：host_x64）的可执行目标。

See the [build system overview][build-overview] for a more detailed discussion of build targets. 有关构建目标的更详细讨论，请参见[构建系统概述] [构建概述]。

 
## Flash a board and prepare Zedboot {#flash-a-board-and-prepare-zedboot}  刷新板并准备Zedboot {flash-a-board-and-prepare-zedboot} 

The exact preparation required to put Fuchsia onto a target device varies by specific device, but there are two general groups in common use today, madeconvenient behind `fx` commands: 将紫红色置于目标设备上所需的确切准备工作因特定设备而异，但当今有两个通用组，在`fx'命令后面很方便：

 
* `fx flash` is used with most `arm64` devices to perform a raw write of Zedboot to the device, preparing it for [Paving](#what-is-paving). *`fx flash`用于大多数`arm64`设备，以对设备进行Zedboot的原始写入，为[Paving]（正在铺装）做准备。
* `fx mkzedboot` is used with most `x64` devices to prepare a bootable USB key that boots into Zedboot, preparing the device for [Paving](#what-is-paving). * fx mkzedboot用于大多数x64设备，以准备引导到Zedboot的可引导USB密钥，以准备用于[Paving]（正在铺装）设备。

 
### What is Zedboot? {#what-is-zedboot}  什么是Zedboot？ {what-is-zedboot} 

Zedboot is a special configuration of Zircon that contains a simple network stack, a simple device advertisement and discovery protocols, and a suite ofprotocols to write Fuchsia to a target disk and/or to network boot a targetsystem. Zedboot is a term used for both the overall process, as well as aspecial build configuration. Many people come to know it as "the blue screenwith ASCII art". Zedboot是Zircon的特殊配置，它包含一个简单的网络堆栈，一个简单的设备公告和发现协议以及一套协议，用于将Fuchsia写入目标磁盘和/或通过网络引导目标系统。 Zedboot是一个用于整个过程以及特殊构建配置的术语。许多人开始将其称为“带有ASCII艺术的蓝屏”。

To enter Zedboot on an arm64 target, power on the device while triggering a boot into fastboot flashing mode (often this involves holding a particularbutton while rebooting or powering on that varies by particular hardwaretarget). Once in flashing mode, execute `fx flash` on the host system. 要在arm64目标上输入Zedboot，请在启动引导进入快速启动闪烁模式的同时打开设备电源（通常这涉及在重新启动或按住电源时按住特定的按钮，具体取决于特定的硬件目标）。进入闪烁模式后，在主机系统上执行“ fx flash”。

To enter Zedboot on an x64 target, first produce a Zedboot USB key using `fx mkzedboot <path-to-usb-device>` (to list suitable USB devices on yoursystem, execute `fx list-usb-disks`). Remove the USB key after completion,insert it to the target device, and reboot the target device, selecting "Bootfrom USB" from the boot options, or in the device BIOS. There are additionalinstructions for preparing a [Pixelbook](/docs/development/hardware/pixelbook.md). 要在x64目标上输入Zedboot，请首先使用`fx mkzedboot <path-to-usb-device>`生成一个Zedboot USB密钥（要列出您系统上合适的USB设备，请执行`fx list-usb-disks'）。完成后拔出USB密钥，将其插入目标设备，然后重新引导目标设备，从引导选项中或在设备BIOS中选择“从USB引导”。还有准备[Pixelbook]的其他说明（/docs/development/hardware/pixelbook.md）。

 
### What is Paving? {#what-is-paving}  什么是铺路？ {铺砌什么} 

Paving is in many ways similar to "flashing" from other worlds, however, it has some differences. Specifically, paving refers to a group of processes andprotocols in Fuchsia to transfer a set of artifacts to a target system thatwill be written into various partitions on a target system. By contrast, theprocess of "flashing" is more of a raw process of writing a raw data streamto a raw disk device, and not strictly partition-oriented. 铺路在许多方面类似于来自其他世界的“刮水”，但是有一些区别。具体而言，铺装是指紫红色中用于将一组工件转移到目标系统的一组过程和协议，这些工件将被写入目标系统的各个分区中。相反，“刷新”过程更多是将原始数据流写入原始磁盘设备的原始过程，而不是严格面向分区的。

Users can start a paving process by first flashing Zedboot using `fx flash`, or by booting a Zedboot USB key made by `fx mkzedboot`, then executing `fx pave`on the host system. In general most users actually will want to use `fx serve`instead of `fx pave`. `fx serve` is covered in the [serve a build](#serve-a-build)section. 用户可以通过首先使用“ fx flash”刷新Zedboot或启动由“ fx mkzedboot”制成的Zedboot USB密钥，然后在主机系统上执行“ fx pave”来启动铺路过程。通常，大多数用户实际上会希望使用“ fx服务”而不是“ fx铺路”。 [fx serve]在[serve a build]（serve-a-build）部分中介绍。

 
### What is Netbooting? {#what-is-netbooting}  什么是网络引导？ {what-is-netbooting} 

In Fuchsia, "netboot" refers to sending a set of artifacts to a Zedboot instance that instead of making changes to the disk, will just be booted fromRAM. Users can perform a "netboot" by first booting a device into Zedboot byusing either `fx flash` (arm64) or `fx mkzedboot` (x64), and then executing`fx netboot` on the host system. 在紫红色中，“ netboot”是指将一组工件发送到Zedboot实例，而不是对磁盘进行更改，而只是从RAM进行引导。用户可以通过以下方式执行“ netboot”：首先使用“ fx flash”（arm64）或“ fx mkzedboot”（x64）将设备引导至Zedboot，然后在主机系统上执行“ fx netboot”。

Note: the `netboot` artifacts are not produced by all builds by default, because for larger builds such as the "workstation" product configurationsuch builds are extremely large, and producing them many times a day is bothslow as well as measurably wearing on host disk hardware. The `bringup`configuration always prepares `netboot` artifacts. For all other buildconfigurations, a user can optionally build the netboot artifacts using`fx build netboot`. 注意：默认情况下，并非所有版本都生成“ netboot”工件，因为对于较大的版本（例如“工作站”产品配置），此类版本非常大，并且每天多次生成它们既缓慢又可测量地磨损在主机磁盘上硬件。 “ bringup”配置总是准备“ netboot”构件。对于所有其他构建配置，用户可以选择使用fx build netboot来构建netboot构件。

 
## Serve a build {#serve-a-build}  服务构建{serve-a-build} 

A lot of build configurations for Fuchsia include software that is not immediately included in the base images that a build produces, that arewritten to devices during paving. Such software is instead made available totarget devices on-demand, which is often colloquially referred to as"ephemeral software". 倒挂金钟的许多构建配置都包含未立即包含在构建生成的基本映像中的软件，这些软件会在铺路期间写入设备。相反，这种软件按需提供给目标设备，通常俗称“临时软件”。

The command `fx serve` performs two functions internally:  命令“ fx serve”在内部执行两个功能：

 
* `fx pave` start a paving server, used for "fresh installs" of a Fuchsia device from a Zedboot state. *`fx pave`启动铺路服务器，用于从Zedboot状态对Fuchsia设备进行“全新安装”。
* `fx serve-updates` start a package repository server, used for dynamic installation of software at runtime, as well as whole-system updates. *`fx serve-updates`启动软件包存储服务器，用于在运行时动态安装软件以及整个系统更新。

Internally the `fx serve-updates` command also searches for a device to configure, and upon discovery (which may be restricted/modulated with`fx set-device` or `fx -d`) the target device is configured to use therepository server as a source of dynamic packages and system updates. 在内部，“ fx serve-updates”命令还搜索要配置的设备，并且在发现（可能会通过“ fx set-device”或“ fx -d”进行限制/调制）后，将目标设备配置为使用存储库服务器作为动态软件包和系统更新的来源。

 
## Update a target device {#update-a-target-device}  更新目标设备{update-a-target-device} 

As described in prior sections, there are different groups of software on a Fuchsia device: 如前几节所述，紫红色设备上有不同的软件组：

 
* Software that is part of the core system "base", that is updated in a single transaction. *作为核心系统“基础”一部分的软件，可以在单个事务中进行更新。
* Software that is part of Zedboot images other than base (cache) that can be updated ephemerally. *是Zedboot映像（基础（缓存）以外）一部分的软件，可以临时更新。
* Software that is always ephemeral (universe).  *总是短暂的（宇宙）软件。

For new user development workflows, the most general command to assist with updating a target device is `fx update`. The `fx update` command firstupdates all "cache" software, and then performs an `fx ota` or, a coresystem update. This command reboots the target device when it is complete.The end result of this process should be indistinguishable in terms ofsoftware versions from performing a fresh pave of a device. 对于新的用户开发工作流程，协助更新目标设备的最通用命令是“ fx update”。 “ fx update”命令首先更新所有“缓存”软件，然后执行“ fx ota”或核心系统更新。完成此命令后，它将重新引导目标设备。就软件版本而言，此过程的最终结果与执行设备的全新铺装应该是无法区分的。

As the `fx update` process causes a device reboot, it is sometimes not the most efficient process for diagnosis, debugging or other non-testing basedworkflows or needs. In these cases a user has some options for how to ensurethat software on a device is being regularly updated. 由于“ fx更新”过程会导致设备重新启动，因此对于诊断，调试或其他基于非测试的工作流程或需求，有时它不是最有效的过程。在这些情况下，用户可以选择如何确保定期更新设备上的软件。

The `fx serve` process configures a Fuchsia software repository with automatic update features. The repository informs the target device of newlyupdated software every time the underlying repository is updated (whichhappens at the end of every successful `fx build`). For many softwarecomponents, the easiest way to update them during development is to ensurethat they are not included in the base set, but instead included ineither "cache" or "universe". In that case, simply restarting thesoftware on the target (e.g. by closing it completely, or by invoking`killall`) will result in the software being immediately updated when it isstarted again. Specifically for shutting down Modular and all dependantcomponents, use `sessionctl shutdown_basemgr`. “ fx serve”过程配置具有自动更新功能的Fuchsia软件存储库。每当基础存储库被更新时，该存储库就将新更新的软件通知目标设备（发生在每次成功的“ fx构建”结束时）。对于许多软件组件，在开发过程中更新它们的最简单方法是确保它们不包含在基本集中，而是包含在“缓存”或“ Universe”中。在这种情况下，只需在目标上重新启动软件（例如，通过完全关闭目标软件或通过调用killall），就会导致该软件在再次启动时立即被更新。专门用于关闭模块化组件和所有依赖组件，请使用“ sessionctl shutdown_basemgr”。

The commands `fx push-package` and `fx build-push` perform manual, forceful updates of packages on a target device. These commands do not however knowhow to re-start software on the device, as such they provide little benefitover simply restarting software correctly which, along with `fx serve`, willcause software to be updated as a natural course of restarting. Thesecommands are sometimes used to diagnose issues, or in cases where automaticupdates are disabled in special build configurations. 命令“ fx push-package”和“ fx build-push”执行目标设备上软件包的手动，有力的更新。然而，这些命令并不知道如何重新启动设备上的软件，因此，与正确地重新启动软件相比，它们提供的益处不多，与“ fx serve”一起，将导致软件作为重新启动的自然过程进行更新。这些命令有时用于诊断问题，或者在特殊的构建配置中禁用自动更新的情况下。

Note: some software may not appear to be updating because it is being run inside of a "runner" process or some other surrounding environment that is"holding on" to resources for the previous package version, only spawningprograms from the old package. As packages in Fuchsia are immutable andcontent-addressed, when host environments retain resources in this manner,there is nothing that the update system can do to forcefully trigger updatesin the rest of the system. Users who find themselves with this issue mostlyneed to find efficient workflow methods to fully restart the relevantsoftware stack. 注意：某些软件可能似乎没有更新，因为它是在“运行程序”进程内部运行或正在“保留”先前程序包版本资源的某些其他周围环境中运行，仅从旧程序包中生成程序。由于紫红色的软件包是不可变的且内容寻址，因此当主机环境以这种方式保留资源时，更新系统无法执行任何操作来强制触发系统其余部分的更新。遇到此问题的用户通常需要找到有效的工作流程方法以完全重新启动相关的软件堆栈。

 
## Execute tests {#execute-tests}  执行测试{execute-tests} 

The Fuchsia codebase contains many tests. Most of these tests are themselves Components, and can be launched on the target device in the same way as othercomponents. On the target device, some programs also assist with testspecific concerns for component launching, such as `runtests` and`/bin/run-test-component`. The process can also conveniently be controlledfrom the development host by way of `fx run-test`. 紫红色的代码库包含许多测试。这些测试大多数本身就是组件，并且可以与其他组件相同的方式在目标设备上启动。在目标设备上，某些程序还可以帮助测试组件启动所需的测试特定问题，例如“ runtests”和“ / bin / run-test-component”。也可以通过“ fx run-test”从开发主机方便地控制该过程。

The command `fx run-test <package-name>` requires the user to specify a particular package name to execute. A package may contain one or more tests.Arguments after `fx run-test package-name` are passed to the program`runtests`. One particularly common use case is to execute:`fx run-test <package-of-many-tests> -t <name-of-one-test>` to execute only asingle test. To list the packages that are members of the current buildconfiguration, run `fx list-packages`. 命令“ fx run-test <程序包名称>”要求用户指定要执行的特定程序包名称。一个包可能包含一个或多个测试。fx run-test package-name之后的参数将传递给程序runtests。一种特别常见的用例是执行：fx run-test <许多测试包> -t <name-one-test>只执行单个测试。要列出作为当前buildconfiguration成员的软件包，运行`fx list-packages`。

Some users find that an effective high focus workflow is to have the system build, push and execute tests whenever they save their source code. This canbe achieved with `fx` very easily, for example: 一些用户发现，有效的高度关注的工作流程是在保存源代码时让系统构建，推送和执行测试。可以很容易地通过`fx`实现，例如：

```shell
$ fx -i run-test rolldice-tests
```
 

The above command will execute the rolldice tests every time a change is made to the source code in the tree. The `-i` flag to `fx` causes `fx` to repeatthe rest of its command every time the source code in the tree is changed.As the `fx run-test` command first performs a build, then executes a test ona target, this combination provides a convenient auto-test loop, great forhigh focus workflows like test driven development. 每当对树中的源代码进行更改时，以上命令将执行rolldice测试。 fx的-i标志使每次树中的源代码更改时fx重复其命令的其余部分。fx run-test命令首先执行构建，然后执行ona测试目标，此组合提供了一个方便的自动测试循环，非常适合诸如测试驱动开发之类的重点工作流程。

Note: Iterative mode (indicated by the *-i* option) requires the `inotify-tools` or `fswatch` package on the host system. 注意：迭代模式（由* -i *选项指示）需要主机系统上的“ inotify-tools”或“ fswatch”软件包。

 
## Connect to a target shell {#connect-to-a-target-shell}  连接到目标外壳{connect-to-a-target-shell} 

Most [product configurations](#key-product-configurations) include an SSH server with a Fuchsia specific configuration. The command `fx shell` is aconvenient wrapper to connect to the target device over SSH and providesaccess to a very simply POSIX-style shell. Users should note that while theshell is a fork of a POSIX shell, it does not provide all features of acommon Unix shell. In particular users will find that CTRL+C has odd quirks,and may often find quirks for sub-shell expressions and certain more advancedIO redirections or environment variable propagations. These misfeatures areside effects of Fuchsia not being a POSIX system. 大多数[产品配置]（关键产品配置）都包括具有紫红色特定配置的SSH服务器。命令“ fx shell”是方便的包装器，可通过SSH连接到目标设备，并提供对非常简单的POSIX样式的外壳的访问。用户应注意，尽管shell是POSIX shell的一个分支，但它不提供常见Unix shell的所有功能。特别是，用户会发现CTRL + C具有奇怪的怪癖，并且可能经常会发现子外壳表达式和某些更高级的I / O重定向或环境变量传播的怪癖。这些功能不足是紫红色不是POSIX系统的副作用。

Nonetheless the shell made available via `fx shell` is extremely useful for imperatively executing programs on the Fuchsia target, as well as exploringsome of the diagnostic / debug interfaces made available in a filesystemtree, such as `/hub` and `/dev`. It is also useful for invoking programs suchas `/bin/run` that provides facilities for launching Fuchsia components. Ifthe `tools` bundle is available in the build configuration, many tools commonto unix shell environments have been ported and are available, such as `ps`,`ls`, `cat`, `curl`, `vim`, `fortune` and so on. 尽管如此，通过`fx shell`提供的shell对于强制执行Fuchsia目标上的程序以及探索文件系统树中提供的某些诊断/调试接口（例如`/ hub`和`/ dev`）非常有用。对于调用诸如提供启动紫红色组件功能的`/ bin / run`之类的程序也很有用。如果工具包在构建配置中可用，那么许多unix外壳环境通用的工具已被移植并可用，例如ps，ls，cat，curl，vim，fortune。等等。

 
## Performing other common tasks {#performing-other-common-tasks}  执行其他常见任务{performing-other-common-tasks} 

 
### Getting logs {#getting-logs}  获取日志{getting-logs} 

`fx syslog` captures all logs from low-level and high-level programs, including the kernel, drivers and other userspace programs. `fx syslog`depends upon a working high level network stack and SSH. As such, `fx syslog`does not work with Zedboot or "bringup" product configurations. If a deviceis in a state where `fx syslog` ceases to function, it is often useful toswitch to `fx log` to capture more information about probable causes. fx syslog捕获来自低级和高级程序的所有日志，包括内核，驱动程序和其他用户空间程序。 fx syslog取决于有效的高级网络堆栈和SSH。因此，`fx syslog`不适用于Zedboot或“ bringup”产品配置。如果设备处于“ fx syslog”停止运行的状态，则切换到“ fx log”以捕获有关可能原因的更多信息通常很有用。

`fx log` captures only a low-level log stream called "klog". The klog stream includes logs from the Zircon kernel itself, as well as a subset of userspacesoftware (most notably drivers and low-level core software). `fx log` dependson a lightweight network stack called `netsvc` that has a tendency to remainavailable even after problems in higher-level software. The netsvc suite isalso always available in "bringup" product configurations, as such, `fx log`is most useful when working on low-level software, such as the Zircon kernel,or drivers. “ fx log”仅捕获称为“ klog”的低级日志流。 klog流包括来自Zircon内核本身的日志，以及一部分用户空间软件（最著名的是驱动程序和底层内核软件）。 “ fx log”依赖于称为“ netsvc”的轻量级网络堆栈，即使在高级软件出现问题后，该堆栈也有保持可用的趋势。 netsvc套件在“ bringup”产品配置中也始终可用，因此，“ fx log”在使用低级软件（例如Zircon内核）或驱动程序时最有用。

 
### Copying files {#copying-files}  复制文件{copying-files} 

`fx cp` provides a basic wrapper around `scp`, similar to how `fx shell` is a wrapper around `ssh`. `fx cp`提供了围绕`scp`的基本包装，类似于`fx shell`是围绕`ssh`的包装。

```shell
# copy ./book.txt from the host, to /tmp/book.txt on the target
$ fx cp book.txt /tmp/book.txt
# copy /tmp/poem.txt on the target to poem.txt on the host
$ fx cp --to-host /tmp/poem.txt poem.txt
```
 

 
### Start Fuchsia in an Emulator {#start-fuchsia-in-emu}  在模拟器中启动樱红色{sta​​rt-fuchsia-in-emu} 

`fx emu` starts a Fuchsia build under the Fuchsia emulator, a general purpose virtual machine. fx emu在通用虚拟机Fuchsia仿真器下启动Fuchsia构建。

In order to run ephemerally delivered programs, users will need to setup TAP based networking, the full details of which are beyond the scope of thisdocument. A quick overview is as follows: 为了运行临时提供的程序，用户将需要设置基于TAP的网络，其详细信息超出了本文档的范围。快速概述如下：

On macOS: Install "http://tuntaposx.sourceforge.net/download.xhtml" On Linux: Run `sudo ip tuntap add dev qemu mode tap user $USER && sudo ip link set qemu up` 在macOS上：安装“ http://tuntaposx.sourceforge.net/download.xhtml”。在Linux上：运行`sudo ip tuntap add dev qemu mode tap user $ USER sudo ip link set qemu`

Then to run the emulator using TAP networking, execute `fx emu -N`. You can attach a package server by running: `fx serve` as you would with a physicaltarget device. 然后要使用TAP网络运行仿真器，执行`fx emu -N`。您可以通过运行以下命令来附加软件包服务器：与物理目标设备一样，运行“ fx serve”。

 
### Using multiple Fuchsia devices {#using-multiple-fuchsia-devices}   使用多个紫红色装置{using-multiple-fuchsia-devices} 

Some users will have more than one Fuchsia device on a network, and will want to limit the effects of various commands to particular of those devices. The`fx set-device` command exists to help with this use case. 一些用户在网络上将有多个Fuchsia设备，并希望将各种命令的影响限制在这些设备中的特定设备上。存在fx set-device命令来帮助解决这个用例。

The `fx set-device` command binds a particular device node name to a particular build directory. This is particularly useful when a user wishes tokeep several different devices in several build configurations, and could besetup as follows: fx set-device命令将特定的设备节点名称绑定到特定的构建目录。当用户希望将几种不同的设备保持在几种构建配置中并且可以按以下方式进行设置时，这特别有用：

```shell
$ fx --dir out/workstation set workstation.x64
$ fx build
$ fx set-device <workstation-node-name>

$ fx --dir out/core set core.arm64
$ fx build
$ fx set-device <core-node-name>

# Start a server for the workstation:
$ fx --dir=out/workstation serve
# Set the default build-dir and target device to the arm64 core, and
# connect to a shell on that device:
$ fx use out/core
$ fx shell
```
 

Additionally, for users who wish to execute a command against a single Fuchsia device from the current default build directory, as a one-offcommand, the `fx` global flag `-d` allows overriding the target node name fora single command invocation. 另外，对于希望从当前默认构建目录中的单个Fuchsia设备执行命令的用户，作为一个命令，`fx`全局标志`-d'允许为单个命令调用覆盖目标节点名称。

 
### Reboot a device {#reboot-a-device}  重新启动设备{reboot-a-device} 

`fx reboot`  FX重启

On some devices (most arm64 devices at present) there are also some useful flags:  在某些设备（当前为大多数arm64设备）上，还有一些有用的标志：

 
* `fx reboot -r` reboot into "recovery" (Zedboot)  *`fx reboot -r`重新启动进入“恢复”（Zedboot）
* `fx reboot -b` reboot into "bootloader" (Flash)  *`fx reboot -b`重启进入“ bootloader”（闪存）

 
### Determine a CL's status {#determine-a-cls-status}  确定CL的状态{determine-a-cls-status} 

`fx whereiscl <query>`  fx whereiscl <查询>

This command tells whether the given CL is merged, and if so whether it passed Global Integration. The query can be either a Gerrit review URL, a CL number, aChange-Id, or a git revision. 此命令告诉给定的CL是否已合并，如果已合并，则是否已通过全局集成。该查询可以是Gerrit审核URL，CL编号，aChange-Id或git修订版。

```shell
$ fx whereiscl fxr/286748
CL status: MERGED
GI status: PASSED

$ fx whereiscl
https://fuchsia-review.googlesource.com/c/fuchsia/+/287311/1/garnet/go/src/amber/source/source.go
CL status: NEW

$ fx whereiscl I94c56fa4e59842d398bfa90a48c45b388f095184
CL status: MERGED
GI status: PASSED

$ fx whereiscl 6575aee
CL status: MERGED
GI status: PENDING
```
 

 
### Debugging and developing `fx` commands {#debugging-and-developing-fx-commands}  调试和开发fx命令{debugging-and-developing-fx-commands} 

 
* `fx -x` the `-x` flag turns on tracing for the `fx` scripts, printing out all expressions evaluated during the `fx` invocation. *`fx -x` -x标志打开对fx脚本的跟踪，打印出在fx调用期间求值的所有表达式。
* `fx exec` executes an abitrary program that follows inside of the current `fx` environment. As an example `fx exec env` prints all environmentvariables in that environment (`fx exec env | grep FUCHSIA` is likely ofinterest). *`fx exec`执行一个在当前`fx`环境内部遵循的任意程序。例如，`fx exec env`打印该环境中的所有环境变量（“ fx exec env | grep FUCHSIA”可能很有意义）。

 
### Getting help with `fx` {#getting-help-with-fx}  获得`fx`的帮助{get-help-with-fx} 

`fx help <command>` provides the best introductory documentation for that command. Some commands also support/provide `fx <command> -h` or`fx <command> --help`, however this help is not available for all commands.This is unusual, but is a function of implementation details. Internally many`fx` commands just run other programs, most often those produced by thebuild, and flags are in many cases passed on unaltered to those programs. Inthose cases, passing the usual `-h` or `--help` flags may not providedocumentation for `fx <command>`, but instead for the program invokeddownstream of `fx`. fx help <命令>提供了该命令的最佳入门文档。有些命令还支持/提供`fx <command> -h`或`fx <command> --help`，但是此帮助并非对所有命令都可用，这很不寻常，但这是实现细节的功能。在内部，许多fx命令仅运行其他程序，通常是由build生成的那些程序，并且在许多情况下，标志不会改变地传递给那些程序。在这种情况下，传递通常的-h或--help标志可能不会提供fx <command>的文档，而是提供给fx下游的程序调用。

Users should always start with `fx help <command>`.  用户应始终以“ fx help <命令>”开头。

`fx help` with no other arguments provides a list of all available commands in `fx`, as well as documentation for `fx` global flags. 没有其他参数的`fx help`提供了`fx`中所有可用命令的列表，以及`fx`全局标志的文档。

