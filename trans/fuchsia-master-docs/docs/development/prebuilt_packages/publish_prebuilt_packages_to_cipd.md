 
# Publish prebuilt packages to CIPD  将预构建的包发布到CIPD 

To integrate your software into the Fuchsia project as prebuilt packages, you need to publish your prebuilt packages toChrome Infrastructure Package Deployment([CIPD](https://github.com/luci/luci-go/tree/master/cipd){: .external}).A prebuilt package is a Fuchsia archive([FAR](/docs/concepts/storage/archive_format.md)) file thatcontains the binaries and metadata of your software. 要将软件作为预建软件包集成到Fuchsia项目中，您需要将预建软件包发布到Chrome基础架构软件包部署（[CIPD]（https://github.com/luci/luci-go/tree/master/cipd）{： .external}）。一个预先构建的软件包是一个Fuchsia归档文件（[FAR]（/ docs / concepts / storage / archive_format.md））文件，其中包含您的软件的二进制文件和元数据。

Once you set up continuous integration (CI) with Fuchsia, whenever you publish new versions of the prebuilt packages to CIPD,Fuchsia’s CI system fetches those new packages androll them into Fuchsia throughthe [global integration](https://fuchsia.googlesource.com/integration/+/refs/heads/master)process. 与Fuchsia建立持续集成（CI）后，每当您将新版本的预构建软件包发布到CIPD时，Fuchsia的CI系统都会获取这些新软件包，并通过[全局集成]将它们滚动到Fuchsia中。 / integration / + / refs / heads / master）进程。

 
## Prerequisite  先决条件 

Before you start working on publishing prebuilt packages, you need to know how to[build a prebuilt package](/docs/development/sdk/documentation/packages.md#build-package). 在开始发布预构建包之前，您需要知道如何[构建预构建包]（/ docs / development / sdk / documentation / packages.msbuild-package）。

 
## A CIPD package {#a-cipd-package}  CIPD软件包{a-cipd-package} 

The main purpose of publishing prebuilt packages to CIPD is for Fuchsia’s CI system to fetch your most recent prebuilt packagesfrom CIPD for global integration. 将预建软件包发布到CIPD的主要目的是让Fuchsia的CI系统从CIPD获取您最新的预建软件包以进行全球集成。

Note: CIPD is not a package repository for Fuchsia devices. A running Fuchsia device doesn't install prebuilt packages from CIPD. 注意：CIPD不是紫红色设备的软件包存储库。正在运行的Fuchsia设备无法从CIPD安装预构建的软件包。

Both Fuchsia and CIPD have the notion of a package. The differences between a prebuilt package and a CIPD package are: 紫红色和CIPD都有包装的概念。预先构建的软件包和CIPD软件包之间的区别是：

 
*   A prebuilt package - A Fuchsia archive (FAR) file that contains the binaries and metadata of your software. *预先构建的软件包-紫红色的存档（FAR）文件，其中包含软件的二进制文件和元数据。
*   A CIPD package - An archive that contains one or more Fuchsia’s prebuilt packages and other relevant files. * CIPD软件包-包含一个或多个Fuchsia预先构建的软件包和其他相关文件的档案。

Updating the content of a CIPD package creates a new instance of the CIPD package. Every CIPD package maintains the history of its instances(see [Figure 1](#figure-1) below). 更新CIPD软件包的内容将创建CIPD软件包的新实例。每个CIPD软件包都保留其实例的历史记录（请参见下面的[图1]（图1））。

 
## Publish your prebuilt packages to CIPD {#publish-your-prebuilt-packages-to-cipd}  将您的预构建包发布到CIPD {publish-your-prebuilt-packages-to-cipd} 

To publish your prebuilt packages to CIPD, see [Publish a CIPD package](#publish-a-cipd-package) below. 要将预构建的包发布到CIPD，请参阅下面的[发布CIPD包]（publish-a-cipd-package）。

Additionally, if your CIPD package contains [ELF binaries](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format){: .external}, see[Publish a CIPD package with unstripped ELF binaries](#publish-a-cipd-package-with-unstripped-elf-binaries)below. 此外，如果您的CIPD软件包包含[ELF二进制文件]（https://en.wikipedia.org/wiki/Executable_and_Linkable_Format）{：.external}，请参阅[发布带有未剥离的ELF二进制文件的CIPD软件包]（publish-a-cipd-带有未剥离的精灵二进制文件的软件包）。

 
### Publish a CIPD package {#publish-a-cipd-package}  发布CIPD程序包{publish-a-cipd-package} 

Fuchsia has the following requirements for a CIPD package:  紫红色对CIPD软件包具有以下要求：

 
*   Use the following naming convention:  *使用以下命名约定：

    ```
    <PROJECT>/fuchsia/<PACKAGE>-<ARCHITECTURE>
    ```
    For example, [chromium/fuchsia/webrunner-arm64](https://chrome-infra-packages.appspot.com/p/chromium/fuchsia/webrunner-arm64/+/){: .external}and[chromium/fuchsia/castrunner-amd64](https://chrome-infra-packages.appspot.com/p/chromium/fuchsia/castrunner-amd64/+/){: .external}. 例如，[chromium / fuchsia / webrunner-arm64]（https://chrome-infra-packages.appspot.com/p/chromium/fuchsia/webrunner-arm64/+/）{：.external}和[chromium / fuchsia / castrunner-amd64]（https://chrome-infra-packages.appspot.com/p/chromium/fuchsia/castrunner-amd64/+/）{：.external}。
*   Include a `LICENSE` file that contains the legal notices of the software.  *包含一个“许可”文件，其中包含软件的法律声明。
*   Provide a Fuchsia archive (FAR) file per prebuilt package. For example, `chromium.far`, `webrunner.far`. *每个预建套件都提供紫红色档案（FAR）档案。例如，“ chromium.far”，“ webrunner.far”。
*   [Tag](https://github.com/luci/luci-go/tree/master/cipd#tags){: .external} each instance with a version identifier in the form of: * [Tag]（https://github.com/luci/luci-go/tree/master/cipdtags）{：.external}每个实例的版本标识符为：

    ```
    version:<VERSION_ID_OF_INSTANCE>
    ```
    For example, `version:77.0.3835.0` and `version:176326.`  例如，版本：77.0.3835.0和版本：176326。
*   Create a [ref](https://github.com/luci/luci-go/tree/master/cipd#refs){: .external} labeled `latest` and point it to the most recent instance of your CIPD package. *创建一个标记为“ latest”的[ref]（https://github.com/luci/luci-go/tree/master/cipdrefs）{：.external}，然后将其指向CIPD软件包的最新实例。

Fuchsia developers need to be able to identify which source code is used to generate an instance of the CIPD packagebased on the version identifier of the instance.Fuchsia recommends that in your project’s documentationyou provide instructions on how to obtain an instance’s source code. Fuchsia开发人员需要能够基于实例的版本标识符来识别用于生成CIPD包实例的源代码。Fuchsia建议在您的项目文档中提供有关如何获取实例源代码的说明。

When you publish a new instance of your CIPD package, you need to update the `latest` ref so that it now points to the new instance.Fuchsia’s CI system monitors your package’s `latest` ref;when the CI system detects that the `latest` ref is updated,it fetches the new package and rolls it into Fuchsia. 当发布CIPD软件包的新实例时，您需要更新`latest'ref，以便它现在指向新实例。倒挂金钟的CI系统监视您软件包的`latest` ref；当CI系统检测到`latest` ref时。 `ref已更新，它将获取新包并将其滚动到紫红色中。

<a name="figure-1"></a> <figure><img src="/docs/images/development/prebuilt_packages/publish-prebuilt-packages-to-fuchsia-00.png"alt="The latest ref and other refs shown in the CIPD UI"><figcaption><b>Figure 1</b>. The CIPD UI showsthe latest ref and other refs used for this CIPD package instances.</figcaption></figure> <a name="figure-1"> </a> <figure> <img src =“ / docs / images / development / prebuilt_packages / publish-prebuilt-packages-to-fuchsia-00.png” alt =“最新ref和CIPD UI“> <figcaption> <b>图1 </ b>中显示的其他ref。 CIPD UI显示了此CIPD程序包实例使用的最新参考和其他参考。</ figcaption> </ figure>

The following example shows the content of a CIPD package:  以下示例显示了CIPD软件包的内容：

```
LICENSE
chromium.far
webrunner.far
```
 

 
### Publish a CIPD package with unstripped ELF binaries {#publish-a-cipd-package-with-unstripped-elf-binaries}  使用未剥离的ELF二进制文件发布CIPD软件包{publish-a-cipd-package-with-unstripped-elf-binaries} 

If your CIPD package contains [ELF binaries](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format){: .external}(executables and shared libraries),you need to publish a CIPD package that contains the unstripped versions of those ELF binaries.The unstripped ELF binaries allow Fuchsia developers to debug your software.For example, the unstripped ELF binaries enable symbolizing stack traces. 如果您的CIPD软件包包含[ELF二进制文件]（https://en.wikipedia.org/wiki/Executable_and_Linkable_Format）{：.external}（可执行文件和共享库），则需要发布包含未压缩版本的CIPD软件包ELF二进制文件。未剥离的ELF二进制文件可使Fuchsia开发人员调试您的软件。例如，未剥离的ELF二进制文件可用于符号化堆栈跟踪。

Typically the owner of prebuilt packages publishes a sibling CIPD package for the unstripped ELF binaries per architecture,in addition to publishing a CIPD package that contains the prebuilt packages.To allow these CIPD packages to be rolled together,the instances of these CIPD packages must share the same version identifier[tag](https://github.com/luci/luci-go/tree/master/cipd#tags){: .external}. 通常，预构建软件包的所有者除了发布包含预构建软件包的CIPD软件包外，还为每个体系结构的未剥离ELF二进制文件发布同级CIPD软件包。要允许这些CIPD软件包一起滚动，这些CIPD软件包的实例必须共享相同的版本标识符[标签]（https://github.com/luci/luci-go/tree/master/cipdtags）{：.external}。

Fuchsia requires a CIPD package with unstripped ELF binaries to have the following directory structure: 紫红色要求带有未剥离ELF二进制文件的CIPD软件包具有以下目录结构：

 
*   An instance of a CIPD package contains a `.tar.bz2` file per prebuilt package.  * CIPD软件包的一个实例每个预构建的软件包都包含一个.tar.bz2文件。
    *   Each `.tar.bz2` file, once uncompressed and unpacked, is a `.build-id` directory.  *每个`.tar.bz2`文件一旦解压缩并解压缩后，都是一个`.build-id`目录。

Note: Don't include a directory named `.build-id` as a root directory in the `.tar.bz2` file. The unpacked content of the `.tar.bz2`file is a collection of subdirectories (see the example below). 注意：不要在.tar.bz2文件中包含名为.build-id的目录作为根目录。 .tar.bz2文件的解压缩内容是子目录的集合（请参见下面的示例）。

 
*   A `.build-id` directory has subdirectories and the subdirectories contain unstripped ELF binaries. * .build-id目录包含子目录，并且这些子目录包含未剥离的ELF二进制文件。
    *   Each subdirectory represents the first two characters of ELF binaries’ `build-id` (see the example below). *每个子目录代表ELF二进制文件的“ build-id”的前两个字符（请参见下面的示例）。

Fuchsia requires the following requirements for an unstripped ELF binary:  紫红色对于未剥离的ELF二进制文件具有以下要求：

 
*   Use the `debug` extension, which indicates that the binary contains DWARF debug information. *使用`debug`扩展名，它指示二进制文件包含DWARF调试信息。
*   Use the first two characters of the `build-id` for the name of the subdirectory and the rest of the `build-id` for its filename.For example, if `build-id` is `1dbca0bd1be33e19`,then its subdirectory name is `1d` andits unstripped ELF binary filename is `bca0bd1be33e19.debug`. *使用build_id的前两个字符作为子目录的名称，使用build-id的其余部分作为文件名。例如，如果build-id为1dbca0bd1be33e19，则使用其子目录名称为1d，未解压缩的ELF二进制文件名为bca0bd1be33e19.debug。
*   Include the following information:  *包括以下信息：
    *   A `NT_GNU_BUILD_ID` note (obtained by passing the `-build-id` flag to the linker). * NT_GNU_BUILD_ID注释（通过将-build-id标志传递给链接器而获得）。
    *   Debug information (obtained by passing the `-g` flag to the compiler). *调试信息（通过将-g标志传递给编译器来获得）。

This example shows the directory structure of a CIPD package with unstripped ELF binaries: 此示例显示具有未剥离的ELF二进制文件的CIPD软件包的目录结构：

```none
chromium.symbols.tar.bz2
   1d/
      bca0bd1be33e19.debug
   2b/
      0e519bcf3942dd.debug
   5b/
      66bc85af2da641697328996cbc04d62b84fc58.debug

webrunner.symbols.tar.bz2
   1f/
      512abdcbe453ee.debug
      90dd45623deab1.debug
   3d/
      aca0b11beff127.debug
   5b/
      66bc85af2da641697328996cbc04d62b84fc58.debug
```
