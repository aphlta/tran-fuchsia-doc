 
# Bundles  捆绑 

Bundles are GN group labels that provide common major groups of features. They can be included into one of the [dependencysets](boards_and_products.md#dependency-sets). 捆绑包是GN组标签，提供常见的主要特征组。它们可以包含在[dependencysets]（boards_and_products.mddependency-sets）之一中。

When using the `fx set` command, bundles are most commonly added to the `universe` dependency set by use of the `--with` flag. See [fx buildconfiguration][fx-build-config] for more information. 当使用`fx set`命令时，捆绑通常是使用`--with`标志添加到`universe`依赖集中的。有关更多信息，请参见[fx buildconfiguration] [fx-build-config]。

More information on the currently available bundles can be found in [`//bundles`](/bundles/README.md). 可在[`//bundles`](/bundles/README.md）中找到有关当前可用捆绑软件的更多信息。

 
## Key bundles  钥匙包 

 
* `tools` contains a broad array of the most common developer tools. This includes tools for spawning components from command-line shells, tools forreconfiguring and testing networks, making http requests, debugging programs,changing audio volume, and so on. *`tools`包含各种最常见的开发人员工具。这包括用于从命令行外壳生成组件的工具，用于重新配置和测试网络，发出http请求，调试程序，更改音频音量等的工具。
* `tests` causes all test programs to be built. Most test programs can be invoked using `run-test-component` on the device, or via `fx run-test`. *`tests`导致所有测试程序被构建。大多数测试程序可以使用设备上的“运行测试组件”或通过“ fx运行测试”来调用。
* `kitchen_sink` is a target that causes all other build targets to be included. It is useful when testing the impact of core changes, or whenmaking large scale changes in the code base. It also may be a funconfiguration for enthusiasts to play with, as it includes all softwareavailable in the source tree. Note that kitchen sink will produce more than20GB of build artifacts and requires at least 2GB of storage on the targetdevice (size estimates from Q1/2019). *`kitchen_sink`是一个导致所有其他构建目标都包括在内的目标。在测试核心更改的影响或在代码库中进行大规模更改时，此功能很有用。对于发烧友来说，这可能也是一种有趣的配置，因为它包括源代码树中所有可用的软件。请注意，厨房水槽将产生超过20GB的构件，并在目标设备上至少需要2GB的存储空间（根据2019年第一季度的估计量）。

