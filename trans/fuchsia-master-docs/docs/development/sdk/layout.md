 
# SDK layout  SDK布局 

The SDK archive contains the Fuchsia Core SDK, which is a small set of Fuchsia-specific libraries and tools required to start building and runningprograms for Fuchsia. SDK存档包含Fuchsia Core SDK，这是一小部分针对Fuchsia的特定库和工具，这些库和工具开始为Fuchsia构建和运行程序。

This SDK differs from traditional SDKs in that it is not readily usable out of the box.For example, it does not contain any build system, favor anytoolchain, or provide standard non-Fuchsia libraries such as for crypto orgraphics.Instead, it provides metadata accurately describing its variousparts, so that this SDK can be post-processed and augmented with all the piecesnecessary for a satisfactory end-to-end development experience. 该SDK与传统SDK的不同之处在于它不易于使用，例如，它不包含任何构建系统，不支持任何工具链或提供标准的非紫红色的库（例如用于加密图形学），而是提供元数据准确描述其各个部分，以便可以对SDK进行后处理和扩充，以提供令人满意的端到端开发体验所需的所有组件。

Most developers who wish to build something for Fuchsia should not need to deal directly with this particular SDK.They will instead consume a transformed version of it, for instance within thedevelopment environment and ecosystem supporting a given language runtime.Maintainers of development environments who wish to add support for Fuchsia arethe main audience for this SDK.See [Integrating the Core SDK](integrating.md) for a description of how to process thisSDK. 大多数希望为Fuchsia构建某些东西的开发人员不需要直接处理这个特定的SDK，而是会使用它的转换版本，例如在支持给定语言运行时的开发环境和生态系统中使用。添加对紫红色的支持是此SDK的主要对象。有关如何处理此SDK的说明，请参见[集成核心SDK]（integrating.md）。

As such, the Core SDK is the representation of the Fuchsia platform developers' contract with other developers who work with Fuchsia.While that contract is absolutely necessary, as this SDK contains the very bitsthat are unique to Fuchsia, it is not sufficient and will be complemented byother "contracts".The Fuchsia Core SDK is mirroring the Fuchsia platform in that respect: highlycomposable and extensible, with a clear separation of concerns. 因此，Core SDK是Fuchsia平台开发人员与其他使用Fuchsia的开发人员签订的合同的代表，尽管该合同是绝对必要的，因为此SDK包含Fuchsia独有的功能，因此这是不够的并且将是Fuchsia Core SDK在这方面反映了Fuchsia平台：高度可组合和可扩展，并具有明确的关注点分离。

 

 
## Structure  结构体 

From this point on, the root of the SDK archive will be referred to as `//`.  从这一点开始，SDK存档的根目录将被称为“ //”。

 
### Metadata  元数据 

Metadata is present throughout this SDK in the form of JSON files. Every element in this SDK has its own metadata file: for example, a FIDL library`//fidl/fuchsia.foobar` has its metadata encoded in`//fidl/fuchsia.foobar/meta.json`. 在整个SDK中，元数据以JSON文件的形式存在。该SDK中的每个元素都有其自己的元数据文件：例如，FIDL库`// fidl / fuchsia.foobar`的元数据编码为`// fidl / fuchsia.foobar / meta.json`。

Every metadata file follows a JSON schema available under `//meta/schemas`: for example, a FIDL library's metadata file conforms to`//meta/schemas/fidl_library.json`.Schemas act as the documentation for the metadata and may be used to facilitatethe SDK ingestion process. See [understanding metadata](understanding_metadata.md). 每个元数据文件都遵循`// meta / schemas`下可用的JSON模式：例如，FIDL库的元数据文件符合`// meta / schemas / fidl_library.json`。模式充当元数据的文档，并且可能是用于促进SDK提取过程。请参阅[了解元数据]（understanding_metadata.md）。

 
### Documentation  文献资料 

General documentation is available under `//docs` in the SDK distribution, or online at [fuchsia.dev/fuchsia-src/docs/development/sdk](/docs/development/sdk).Some individual SDK elements will also provide documentation directly under thepath where they are hosted in the SDK. 常规文档可在SDK发行版的“ // docs”下找到，也可以在线访问[fuchsia.dev/fuchsia-src/docs/development/sdk](/docs/development/sdk）。某些单独的SDK元素也将提供文档直接在SDK中托管它们的路径下。

 
### Target prebuilts  目标预建 

Target prebuilts are hosted under `//arch/<architecture>`. This includes a full-fledged sysroot for each available architecture. 目标预建对象位于`// arch / <architecture>`下。这包括适用于每个可用体系结构的完整sysroot。

 
### Source libraries  源库 

The SDK contains sources for a large number of FIDL libraries (under `//fidl`) as well as a few C/C++ libraries (under `//pkg`). See [compiling C/C++](documentation/compilation.md)for details. 该SDK包含大量FIDL库（在// fidl下）和一些C / C ++库（在// pkg下）的源。有关详细信息，请参见[编译C / C ++]（documentation / compilation.md）。

 
### Host tools  主机工具 

Multiple host-side tools can be found under `//tools`. This includes tools for building programs, deploying to a device, debugging,etc...Some information about how to use these tools can be found under `//docs`.Specifically: 在// tools下可以找到多个主机端工具。这包括用于构建程序，部署到设备，调试等的工具...有关如何使用这些工具的一些信息可以在`// docs`下找到。

 
* [bootserver](documentation/bootserver.md)  * [引导服务器]（documentation / bootserver.md）
* [zxdb](documentation/debugger.md)  * [zxdb]（documentation / debugger.md）
* [dev_finder](documentation/device_discovery.md)  * [dev_finder]（文档/device_discovery.md）
* [ssh](documentation/ssh.md)  * [ssh]（文档/ssh.md）
* [logging and symbolizer](documentation/logging.md)  * [日志记录和符号器]（documentation / logging.md）
* [package manager](documentation/packages.md)  * [软件包管理器]（documentation / packages.md）

 
### Images  图片 

