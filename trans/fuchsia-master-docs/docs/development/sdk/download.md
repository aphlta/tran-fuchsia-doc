 
# Download the Fuchsia SDK  下载Fuchsia SDK 

You can download the Fuchsia SDK using the links below. Please be aware that Fuchsia is under active development and its API surface is subject to frequentchanges. The Fuchsia SDK is produced continuously as Fuchsia is developed. 您可以使用下面的链接下载Fuchsia SDK。请注意，紫红色正在积极开发中，其API的表面可能会经常变化。随着紫红色的发展，紫红色SDK不断生产。

Because the [Fuchsia System Interface](/docs/concepts/system/abi/system.md) is changing, you will need to run software built using a particular version of the SDK on a Fuchsiasystem with a matching version. The [Core SDK](#core) contains a matching systemimage appropriate for running in [Qemu](#qemu). 由于[Fuchsia系统界面]（/ docs / concepts / system / abi / system.md）发生了变化，因此您需要在具有匹配版本的Fuchsia系统上运行使用特定版本的SDK构建的软件。 [Core SDK]（core）包含适合在Qemu（qemu）中运行的匹配系统映像。

 
## Core  核心 

The Core SDK is a version of the SDK that is build system agnostic. The Core SDK contains metadata that can be used by an [SDK backend](README.md#backend) togenerate an SDK for a specific build system. Core SDK是与构建系统无关的SDK版本。核心SDK包含[SDK后端]（README.mdbackend）可以使用的元数据，以生成特定构建系统的SDK。

 
* [Linux](https://chrome-infra-packages.appspot.com/p/fuchsia/sdk/core/linux-amd64/+/latest)  * [Linux]（https://chrome-infra-packages.appspot.com/p/fuchsia/sdk/core/linux-amd64/+/latest）
* [MacOS](https://chrome-infra-packages.appspot.com/p/fuchsia/sdk/core/mac-amd64/+/latest)  * [MacOS]（https://chrome-infra-packages.appspot.com/p/fuchsia/sdk/core/mac-amd64/+/latest）

 
## Qemu  mu木 

A distribution of [Qemu](https://www.qemu.org/) that has been tested to work with Fuchsia system images contained in the SDK. Qemu（https://www.qemu.org/）的发行版已通过测试，可与SDK中包含的Fuchsia系统映像一起使用。

 
* [Linux (amd64)](https://chrome-infra-packages.appspot.com/p/fuchsia/qemu/linux-amd64/+/latest)  * [Linux（amd64）]（https://chrome-infra-packages.appspot.com/p/fuchsia/qemu/linux-amd64/+/latest）
* [Linux (arm64)](https://chrome-infra-packages.appspot.com/p/fuchsia/qemu/linux-arm64/+/latest)  * [Linux（arm64）]（https://chrome-infra-packages.appspot.com/p/fuchsia/qemu/linux-arm64/+/latest）
