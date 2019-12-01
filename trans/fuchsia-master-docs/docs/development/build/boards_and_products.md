 
# Products and Boards  产品和板 

[**Products**][products-source] and [**Boards**][boards-source] are GN includes used in combination to provide a baseline configuration for aFuchsia build. [** Products **] [products-source]和[** Boards **] [boards-source]是GN include的组合，可为紫红色构建提供基线配置。

It is expected that a GN build configuration include exactly one board GNI file, and one product GNI file. In [fx][fx] this pair is the primary argumentto the `fx set` command. 预计GN构建配置将仅包含一个板GNI文件和一个产品GNI文件。在[fx] [fx]中，这对是`fx set`命令的主要参数。

In a Fuchsia GN build configuration the board is always included first. The board starts the definition of three dependency lists that are then augmentedby the imported product (and later, optional GN inclusions). Those list are[Base](#base), [Cache](#cache) and [Universe](#universe) respectively, andare defined below. 在Fuchsia GN构建配置中，始终首先包含该板。该委员会开始定义三个依赖项列表，然后再通过导入的产品（以及以后的可选GN包含项）对其进行扩展。这些列表分别是[Base]（基本），[Cache]（缓存）和[Universe]（universe），并在下面定义。

 
## Boards  板子 

A board defines the architecture that the build produces for, as well as key features of the device upon which the build is intended to run. Thisconfiguration includes what drivers are included, and may also influencedevice specific kernel parameters. 电路板定义了构建生成的体系结构，以及打算在其上运行构建的设备的关键功能。此配置包括所包含的驱动程序，并且还可能影响设备特定的内核参数。

The available boards can be listed using `fx list-boards`.  可使用`fx list-boards'列出可用的板卡。

 
## Products  产品展示 

A product defines the software configuration that a build will produce. Most critically, a product typically defines the kinds of user experiences thatare provided for, such as what kind of graphical shell the user mightobserve, whether or not multimedia support is included, and so on. 产品定义了构建将产生的软件配置。最关键的是，产品通常会定义所提供的用户体验的类型，例如用户可能会观察到的图形外壳类型，是否包括多媒体支持等等。

The available products can be listed using `fx list-products`.  可使用`fx list-products'列出可用产品。

 
## Dependency Sets  依赖集 

Boards define, and products augment three lists of dependencies, Base, Cache and Universe. These dependencies are GN labels that ultimately contributepackages to various system artifacts, such as disk images and signed packagemetadata, as well as various development artifacts such as host tools andtests. 董事会定义了产品，并增加了三个依赖关系列表，即基本，缓存和Universe。这些依赖项是GN标签，最终将包贡献给各种系统工件，例如磁盘映像和签名的包元数据，以及各种开发工件，例如主机工具和测试。

 
### Base  基础 

The `base` dependency list contributes packages to disk images and system updates as well as the package repository. A package included by the `base`dependency set takes precedence over a duplicate membership in the `cache`dependency set. Base packages in a system configuration are considered systemand security critical. They are updated as an atomic unit and are neverevicted at runtime regardless of resource pressure. 基本依赖性列表将软件包提供给磁盘映像，系统更新以及软件包存储库。 “ base”依赖集所包含的软件包优先于“ cache”依赖集中的重复成员资格。系统配置中的基本软件包被认为对系统和安全性至关重要。它们将作为原子单位进行更新，并且无论资源压力如何，都不会在运行时退出。

 
### Cache  快取 

The `cache` dependency list contributes packages that are pre-cached in the disk image artifacts of the build, and will also be made available in thepackage repository. These packages are not added to the system updates, butwould instead be updated ephemerally. Cached packages can also be evictedfrom running systems in order to free resources based on runtime resourcedemands. “ cache”依赖项列表提供了已预先缓存在构建的磁盘映像工件中的软件包，并且还将在软件包存储库中提供。这些软件包不会添加到系统更新中，而是会暂时更新。也可以从正在运行的系统中逐出缓存的软件包，以便根据运行时资源需求释放资源。

 
### Universe  宇宙 

The `universe` dependency list contributes packages to the package repository only. These packages will be available for runtime caching and updating, butare not found in system update images nor are they pre-cached in any diskimages. All members of `base` and `cache` are inherently also members of`universe`. “ universe”依赖项列表仅将软件包贡献到软件包存储库。这些软件包可用于运行时缓存和更新，但在系统更新映像中找不到，也未预先缓存在任何磁盘映像中。 “ base”和“ cache”的所有成员本质上也是“ universe”的成员。

 
## Key Product Configurations  关键产品配置 

There are many more than below, but the following three particularly important configurations to be familiar with: 除了下面的内容外，还有很多其他内容，但您需要熟悉以下三个特别重要的配置：

 
* `bringup` is a minimal feature set product that is focused on being very simple and very lean. It exists to provide fast builds and small images(primarily used in a [netboot][fx-netboot] rather than [paved][fx-paving]fashion), and is great for working on very low-level facilities, such asthe Zircon kernel or board-specific drivers and configurations. It lacksmost network capabilities, and therefore is not able to add new software atruntime or upgrade itself. *`bringup`是一个最小的功能集产品，致力于非常简单和精益。它的存在是为了提供快速构建和较小的映像（主要用于[netboot] [fx-netboot]，而不是[paved] [fx-paving] fashion），并且非常适合用于底层设备，例如Zircon。特定于内核或主板的驱动程序和配置。它缺乏大多数网络功能，因此无法在运行时添加新软件或自行升级。
* `core` is a minimal feature set that can install additional software (such as items added to the "universe" dependency set). It is the starting point forall higher-level product configurations. It has common network capabilitiesand can update a system over-the-air. *`core`是最小功能集，可以安装其他软件（例如添加到“ Universe”依赖集的项）。这是所有更高级别产品配置的起点。它具有通用的网络功能，可以通过无线方式更新系统。
* `workstation` is a basis for a general purpose development environment, good for working on UI, media and many other high-level features. This is alsothe best environment for enthusiasts to play with and explore. *“工作站”是通用开发环境的基础，非常适合使用UI，媒体和许多其他高级功能。这也是发烧友玩耍和探索的最佳环境。

