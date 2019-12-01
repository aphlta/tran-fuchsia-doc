 
# Glossary  词汇表 

 
## Overview  总览 

The purpose of this document is to provide short definitions for a collection of technical terms used in Fuchsia. 本文档的目的是为紫红色中使用的一系列技术术语提供简短的定义。

 
#### Adding new definitions  添加新定义 

 
-   A definition should provide a high-level description of a term and in most cases should not be longer than two or three sentences. -定义应提供术语的高级描述，并且在大多数情况下，不应超过两个或三个句子。
-   When another non-trivial technical term needs to be employed as part of the description, consider adding a definition for that term and linking to itfrom the original definition. -当需要使用另一个不重要的技术术语作为说明的一部分时，请考虑为该术语添加一个定义，并将其与原始定义链接。
-   A definition should be complemented by a list of links to more detailed documentation and related topics. -定义应辅以更详细的文档和相关主题的链接列表。

 
## Terms  条款 

 
#### **Agent** {#agent}  **代理商** {agent} 

An agent is a role a [component](#component) can play to execute in the background in the context of a [session](#session). An agent's life cycle is nottied to any [story](#story), is a singleton per session, and provides servicesto other components. An agent can be invoked by other components or by thesystem in response to triggers like push notifications. An agent can provideservices to components, send and receive messages, and make proposals to givesuggestions to the user. 代理是[component]（component）在[session]（session）上下文中可以在后台执行的角色。座席的生命周期被记录到任何[story]（story）中，每个会话单身，并为其他组件提供服务。代理可以由其他组件或由系统响应诸如推送通知之类的触发器来调用。代理可以为组件提供服务，发送和接收消息以及向用户提出建议。

 
#### **AppMgr** {#appmgr}  ** AppMgr ** {appmgr} 

The Application Manager (AppMgr) is responsible for launching components and managing the namespaces in which those components run. It is the first processstarted in the `fuchsia` job by the [DevMgr](#devmgr). 应用程序管理器（AppMgr）负责启动组件和管理这些组件在其中运行的名称空间。这是[DevMgr]（devmgr）在“紫红色”作业中启动的第一个过程。

 
#### **Banjo** {#banjo}  **班卓琴** {班卓琴} 

Banjo is a language for defining protocols that are used to communicate between [drivers](#driver). It is different from [FIDL](#fidl) in that it specifies anABI for drivers to use to call into each other, rather than an IPC protocol. Banjo是用于定义用于在[drivers]（driver）之间进行通信的协议的语言。它与[FIDL]（fidl）的不同之处在于，它为驱动程序指定了一个ABI以便彼此调用，而不是IPC协议。

 
#### **Base shell** {#base-shell}  **基础外壳** {base-shell} 

The platform-guaranteed set of software functionality which provides a basic user-facing interface for boot, first-use, authentication, escape from andselection of session shells, and device recovery. 平台保证的软件功能集，提供了基本的面向用户的界面，用于引导，首次使用，身份验证，会话外壳的退出和选择以及设备恢复。

 
#### **bootfs** {#bootfs}  ** bootfs ** {bootfs} 

The bootfs RAM disk contains the files needed early in the boot process when no other filesystems are available. It is part of the [ZBI](#zircon-boot-image),and is decompressed and served by [bootsvc](#bootsvc). After the early bootprocess is complete, the bootfs is mounted at `/boot`. 当没有其他文件系统可用时，bootfs RAM磁盘包含启动过程初期所需的文件。它是[ZBI]（zircon-boot-image）的一部分，并由[bootsvc]（bootsvc）解压缩并提供服务。早期引导过程完成后，bootfs将挂载在`/ boot`处。

 
-   [Documentation](/docs/concepts/booting/userboot.md#BOOTFS)  -[文档]（/ docs / concepts / booting / userboot.mdBOOTFS）

 
#### **bootsvc** {#bootsvc}  ** bootsvc ** {bootsvc} 

`bootsvc` is the second process started in Fuchsia. It provides a filesystem service for the [bootfs](#bootfs) and a loader service that loads programs fromthe same bootfs. After starting these services, it loads the third program,which defaults to `devmgr`. “ bootsvc”是在紫红色中启动的第二个进程。它为[bootfs]（bootfs）提供了文件系统服务，并提供了从同一bootfs加载程序的加载程序服务。启动这些服务后，它将加载第三个程序，默认为`devmgr`。

 
-   [Documentation](/docs/concepts/booting/bootsvc.md)  -[文档]（/ docs / concepts / booting / bootsvc.md）

 
#### **Bus Driver** {#bus-driver}  **巴士司机** {巴士司机} 

A [driver](#driver) for a device that has multiple children. For example, hardware interfaces like PCI specify a topology in which a single controller isused to interface with multiple devices connected to it. In that situation, thedriver for the controller would be a bus driver. 具有多个子代的设备的[驱动程序]（驱动程序）。例如，诸如PCI之类的硬件接口指定了一种拓扑，其中单个控制器用于与与其连接的多个设备进行接口。在这种情况下，控制器的驱动程序将是总线驱动程序。

 
#### **Cache directory** {#cache-directory}  **缓存目录** {cache-directory} 

Similar to a [data directory](#data-directory), except that the contents of a cache directory may be cleared by the system at any time, such as when thedevice is under storage pressure. Canonically mapped to /cache in the component instance’s [namespace](#namespace). 类似于[数据目录]（数据目录），不同之处在于系统可以在任何时候（例如，设备处于存储压力下）清除缓存目录的内容。规范地映射到componentinstance的[namespace]（namespace）中的/ cache。

 
-   [Testing isolated cache storage](development/testing/testing_isolated_cache_storage.md).  -[测试隔离的缓存存储]（开发/测试/testing_isolated_cache_storage.md）。

 
#### **Capability** {#capability}  **能力** {capability} 

A capability is a value which combines an *object reference* and a set of *rights*. When a program has a capability it is conferred the privilege toperform certain actions using that capability. A [handle](#handle) is a commonexample for a capability. 功能是将*对象引用*和一组*权限*组合在一起的值。当程序具有某种功能时，将被授予使用该功能执行某些操作的特权。 [handle]（handle）是功能的常见示例。

 
#### **Capability routing** {#capability-routing}  **功能路由** {capability-routing} 

A way for one [component](#component-instance) to give [capabilities](#capability) to another instance over the[component instance tree](#component-instance-tree).[Component manifests](#component-manifest) define how routing takes place, withsyntax for [service capabilities](#service-capability),[directory capabilities](#directory-capability), and[storage capabilities](#storage-capability). 一种[组件] [组件实例]通过[组件实例树] [组件实例树]将[能力] [能力]赋予另一个实例的方法。[组件清单] [组件清单]定义路由的方式发生时，具有[服务功能] [服务能力]，[目录功能] [目录能力]和[存储功能] [存储能力]的语法。

Capability routing is a [components v2](#components-v2) concept.  能力路由是[components v2]（components-v2）概念。

 
##### expose {#expose}  暴露{暴露} 

A [component instance](#component-instance) may use the `expose` [manifest](#component-manifest) keyword to indicate that it is making acapability available to its parent to route. Parents may [offer](#offer) acapability exposed by any of their children to their other children or to theirparent, but they cannot [use](#use) it themselves in order to avoid dependencycycles. [component实例]（component-instance）可以使用`expose` [manifest]（component-manifest）关键字来表示它正在使其父级可以路由。父母可以[提供]（提供）任何孩子向其他孩子或父母公开的能力，但他们不能[自己使用]（使用）以避免依赖周期。

 
##### offer {#offer}  提供{要价} 

A [component instance](#component-instance) may use the `offer` [manifest](#component-manifest) keyword to route a capability that was[exposed](#expose) to it to one of its children (other than the child thatexposed it). [component instance]（component-instance）可以使用`offer` [manifest]（component-manifest）关键字将已[exposed]（expose）的功能路由到其子级之一（已暴露的子级除外）它）。

 
##### use {#use}  使用{use} 

A [component instance](#component-instance) may use the `use` [manifest](#component-manifest) keyword to consume a capability that was[offered](#offer) to it by its parent. 一个[component instance]（component-instance）可以使用`use` [manifest]（component-manifest）关键字来消耗其父级提供给它的功能。

 
#### **Channel** {#channel}  **频道** {频道} 

A channel is an IPC primitive provided by Zircon. It is a bidirectional, datagram-like transport that can transfer small messages including[Handles](#handle). [FIDL](#fidl) protocols typically use channels as theirunderlying transport. 通道是Zircon提供的IPC原语。它是一种双向的，类似于数据报的传输方式，可以传输包括[Handles]（handle）在内的小消息。 [FIDL]（fidl）协议通常使用信道作为其基础传输。

 
-   [Channel Overview](/docs/concepts/objects/channel.md)  -[频道概述]（/ docs / concepts / objects / channel.md）
-   [Update Channel Usage Policy](/docs/contribute/best-practices/update_channel_usage_policy.md)  -[更新频道使用政策]（/ docs / contribute / best-practices / update_channel_usage_policy.md）

 
#### **Component** {#component}  **组件** {component} 

A component is a unit of executable software on Fuchsia. Components support [capability routing](#capability-routing), software composition, isolationboundaries, continuity between executions, and introspection. 组件是紫红色上的可执行软件的一个单元。组件支持[功能路由]（功能路由），软件组成，隔离边界，执行之间的连续性和自省。

 
#### **Component collection** {#component-collection}  **组件集合** {component-collection} 

A node in the [component instance tree](#component-instance-tree) whose children are dynamically instantiated rather than statically defined in a[component manifest](#component-manifest). [组件实例树]（组件实例树）中的一个节点，其子节点是动态实例化的，而不是在[组件清单]（组件清单）中静态定义的。

Component collection is a [components v2](#components-v2) concept.  组件集合是[components v2]（components-v2）概念。

 
#### **Component declaration** {#component-declaration}  **组件声明** {component-declaration} 

A component declaration is a [FIDL](#fidl) table ([fuchsia.sys2.ComponentDecl]) that includes information about a [component](#component)’s runtimeconfiguration, [capabilities](#capabilities) it [exposes](#expose),[offers](#offer), and [uses](#use), and [facets](#component-manifest-facet). 组件声明是[FIDL]（fidl）表（[fuchsia.sys2.ComponentDecl]），其中包含有关[component]（component）的运行时配置，[capabilities]（captures）[expose]（expose）， [offers]（offer），[uses]（use）和[facets]（component-manifest-facet）。

Component declaration is a [components v2](#components-v2) concept.  组件声明是[components v2]（components-v2）概念。

[fuchsia.sys2.ComponentDecl]: /sdk/fidl/fuchsia.sys2/decls/component_decl.fidl  [fuchsia.sys2.ComponentDecl]：/sdk/fidl/fuchsia.sys2/decls/component_decl.fidl

 
#### **Component Framework** {#component-framework}  **组件框架** {component-framework} 

An application framework for declaring and managing [components](#component), consisting of build tools, APIs, conventions, and system services. 一个用于声明和管理[component]（component）的应用程序框架，由构建工具，API，约定和系统服务组成。

 
-   [Components v1](#components-v1), [Components v2](#components-v2)  -[Components v1]（components-v1），[Components v2]（components-v2）

 
#### **Component instance** {#component-instance}  **组件实例** {component-instance} 

One of possibly many instances of a particular [component](#component) at runtime. A component instance has its own [environment](#environment) and[lifecycle](#lifecycle) independent of other instances. 在运行时特定[component]（component）的许多实例之一。组件实例具有独立于其他实例的自己的[environment]（环境）和[lifecycle]（生命周期）。

 
#### **Component instance tree** {#component-instance-tree}  **组件实例树** {component-instance-tree} 

A tree structure that represents the runtime state of parent-child relationships between [component instances](#component-instance). If instance A launchesinstance B then in the tree A will be the parent of B. The component instancetree is used in [static capability routing](#static-capability-routing) suchthat parents can [offer](#offer) capabilities to their children to [use](#use),and children can [expose](#expose) capabilities for their parents to expose totheir parents or offer to other children. 表示[组件实例]（component-instance）之间父子关系的运行时状态的树结构。如果实例A启动实例B，则树A将是B的父实例。组件实例树用于[静态功能路由]（static-capability-routing），以便父级可以[提供]（提供）其子代功能给[使用]（使用），孩子可以[暴露]（暴露）自己的父母与父母接触或向其他孩子求婚的能力。

Component instance tree is a [components v2](#components-v2) concept.  组件实例树是[components v2]（components-v2）概念。

 
#### **Component Manager** {#component-manager}  **组件管理器** {component-manager} 

A system service which lets [component instances](#component-instance) manage their children and [routes capabilities](#capability-routing) between them, thusimplementing the [component instance tree](#component-instance-tree). ComponentManager is the system service that implements the[components v2](#components-v2) runtime. 一种系统服务，它允许[组件实例]（component-instance）管理其子代并在它们之间[路由功能]（capability-routing），从而实现[组件实例树]（component-instance-tree）。 ComponentManager是实现[components v2]（components-v2）运行时的系统服务。

 
#### **Component Manifest** {#component-manifest}  **组件清单** {component-manifest} 

In [Components v1](#components-v1), a component manifest is a JSON file with a `.cmx` extension that contains information about a [component](#component)’sruntime configuration, services and directories it receives in its[namespace](#namespace), and [facets](#component-manifest-facet). 在[Components v1]（components-v1）中，组件清单是带有`.cmx`扩展名的JSON文件，其中包含有关[component]（component）的运行时配置，服务及其在[名称空间]中接收的目录的信息。 （命名空间）和[facets]（component-manifest-facet）。

In [Components v2](#components-v2), a component manifest is a file with a `.cm` extension, that encodes a [component declaration](#component-declaration). 在[Components v2]（components-v2）中，组件清单是具有`.cm`扩展名的文件，该文件对[component声明]（component-declaration）进行编码。

 
-   [Component manifests v2](/docs/concepts/components/component_manifests.md)  -[组件清单v2]（/ docs / concepts / components / component_manifests.md）

 
#### **Component Manifest Facet** {#component-manifest-facet}  ** Component Manifest Facet ** {component-manifest-facet} 

Additional metadata that is carried in a [component manifest](#component-manifest). This is an extension point to the[component framework](#component-framework). [组件清单]（组件清单）中携带的其他元数据。这是[组件框架]（组件框架）的扩展点。

 
#### **Components v1** {#components-v1}  **组件v1 ** {components-v1} 

A shorthand for the [Component](#component) Architecture as first implemented on Fuchsia. Includes a runtime as implemented by [appmgr](#appmgr) and[sysmgr](#sysmgr), protocols and types as defined in [fuchsia.sys], build-timetools such as [cmc], and SDK libraries such as [libsys] and [libsvc]. [Component]（component）Architecture的简写，最早在Fuchsia上实现。包括由[appmgr]（appmgr）和[sysmgr]（sysmgr）实现的运行时，[fuchsia.sys]中定义的协议和类型，诸如[cmc]的构建时间工具以及诸如[libsys]和[libsvc]。

 
-   [Components v2](#components-v2)  -[Components v2]（components-v2）

[fuchsia.sys]: /sdk/fidl/fuchsia.sys/ [cmc]: /src/sys/cmc[libsys]: /sdk/lib/sys[libsvc]: /sdk/lib/svc [fuchsia.sys]：/ sdk / fidl / fuchsia.sys / [cmc]：/ src / sys / cmc [libsys]：/ sdk / lib / sys [libsvc]：/ sdk / lib / svc

 
#### **Components v2**  {#components-v2}  **组件v2 ** {components-v2} 

A shorthand for the [Component](#component) Architecture in its modern implementation. Includes a runtime as implemented by[component_manager](#component-manager), protocols and types as defined in[fuchsia.sys2], and build-time tools such as [cmc]. [Component]（component）体系结构在现代实现中的简写。包括由[component_manager]（component-manager）实现的运行时，在[fuchsia.sys2]中定义的协议和类型，以及诸如[cmc]之类的构建时工具。

 
-   [Components v1](#components-v1)  -[Components v1]（components-v1）

[fuchsia.sys2]: /sdk/fidl/fuchsia.sys2/ [cmc]: /src/sys/cmc [fuchsia.sys2]：/sdk/fidl/fuchsia.sys2/ [cmc]：/ src / sys / cmc

 
#### **Concurrent Device Driver** {#concurrent-device-driver}  **并发设备驱动程序** {concurrent-device-driver} 

A concurrent device driver is a [hardware driver](#hardware-driver) that supports multiple concurrent operations. This may be, for example, through ahardware command queue or multiple device channels. From the perspective of the[core driver](#core-driver), the device has multiple pending operations, each ofwhich completes or fails independently. If the driven device can internallyparallelize an operation, but can only have one operation outstanding at a time,it may be better implemented with a[sequential device driver](#sequential-device-driver). 并发设备驱动程序是支持多个并发操作的[硬件驱动程序]（硬件驱动程序）。例如，这可以通过硬件命令队列或多个设备通道进行。从[核心驱动程序]（核心驱动程序）的角度来看，设备具有多个挂起的操作，每个操作都独立完成或失败。如果被驱动设备可以在内部并行执行一项操作，但一次只能完成一项操作，则最好使用“顺序设备驱动程序”（sequential-device-driver）来实现。

 
#### **Core Driver** {#core-driver}  **核心驱动器** {core-driver} 

A core driver is a [driver](#driver) that implements the application-facing RPC interface for a class of drivers (e.g. block drivers, ethernet drivers). It ishardware-agnostic. It communicates with a [hardware driver](#hardware-driver)through [banjo](#banjo) to service its requests. 核心驱动程序是[driver]（驱动程序），它为一类驱动程序（例如，块驱动程序，以太网驱动程序）实现面向应用程序的RPC接口。它与硬件无关。它通过[banjo]（banjo）与[hardware driver]（硬件驱动程序）通信以服务其请求。

 
#### **Data directory** {#data-directory}  **数据目录** {数据目录} 

A private directory within which a [component instance](#component-instance) may store data local to the device, canonically mapped to /data in the componentinstance’s [namespace](#namespace). 一个私有目录，[组件实例]（component-instance）可以在其中存储设备本地的数据，该目录通常映射到componentinstance的[namespace]（namespace）中的/ data。

 
#### **DevHost** {#devhost}  ** DevHttp ** {dev主机} 

A Device Host (`DevHost`) is a process containing one or more device drivers. They are created by the Device Manager, as needed, to provide isolation betweendrivers for stability and security. 设备主机（DevHost）是包含一个或多个设备驱动程序的进程。它们由设备管理器根据需要创建，以在驱动程序之间提供隔离，以实现稳定性和安全性。

 
#### **DevMgr** {#devmgr}  ** DevMgr ** {devmgr} 

The Device Manager (DevMgr) is responsible for enumerating, loading, and managing the life cycle of device drivers, as well as low level system tasks(providing filesystem servers for the boot filesystem, launching[AppMgr](#appmgr), and so on). 设备管理器（DevMgr）负责枚举，加载和管理设备驱动程序以及低级系统任务的生命周期（为启动文件系统提供文件系统服务器，启动[AppMgr]（appmgr）等） 。

 
#### **DDK** {#ddk}  ** DDK ** {ddk} 

The Driver Development Kit is the documentation, APIs, and ABIs necessary to build Zircon Device Drivers. Device drivers are implemented as ELF sharedlibraries loaded by Zircon's Device Manager. 驱动程序开发套件是构建Zircon设备驱动程序所需的文档，API和ABI。设备驱动程序被实现为Zircon的设备管理器加载的ELF共享库。

 
-   [DDK Overview](/docs/concepts/drivers/overview.md)  -[DDK概述]（/ docs / concepts / drivers / overview.md）
-   [DDK includes](/zircon/system/ulib/ddk/include/ddk/)  -[DDK包含]（/ zircon / system / ulib / ddk / include / ddk /）

 
#### **Directory capability** {#directory-capability}  **目录功能** {目录功能} 

A [capability](#capability) that permits access to a filesystem directory by adding it to the [namespace](#namespace) of the[component instance](#component-instance) that [uses](#use) it. If multiple[component instances](#component-instance) are offered the same directorycapability then they will have access to the same underlying filesystemdirectory. 通过将文件系统目录添加到[使用] [使用]的[组件实例] [组件实例]的[名称空间] [名称空间]，从而允许访问文件系统目录的[功能] [功能]。如果为多个[组件实例]（component-instance）提供了相同的目录功能，则它们将有权访问相同的基础文件系统目录。

Directory capability is a [components v2](#components-v2) concept.  目录功能是[components v2]（components-v2）概念。

 
-   [Capability routing](#capability-routing)  -[功能路由]（功能路由）

 
#### **Driver** {#driver}  **驾驶员** {驾驶员} 

A driver is a dynamic shared library which [DevMgr](#devmgr) can load into a [DevHost](#devhost) and that enables, and controls one or more devices. 驱动程序是动态共享库，[DevMgr]（devmgr）可以将其加载到[DevHost]（devhost）中，并且可以启用和控制一个或多个设备。

 
-   [Reference](/docs/concepts/drivers/driver-development.md)  -[参考]（/ docs / concepts / drivers / driver-development.md）
-   [Driver Sources](/zircon/system/dev)  -[驱动程序源]（/ zircon / system / dev）

 
#### **Environment** {#environment}  **环境** {环境} 

A container for a set of components, which provides a way to manage their lifecycle and provision services for them. All components in an environmentreceive access to (a subset of) the environment's services. 一组组件的容器，它提供了一种管理组件生命周期并为其提供服务的方法。环境中的所有组件都可以访问环境服务（的一部分）。

 
#### **Escher** {#escher}  ** Escher ** {escher} 

Graphics library for compositing user interface content. Its design is inspired by modern real-time and physically based rendering techniques though weanticipate most of the content it renders to have non-realistic or stylizedqualities suitable for user interfaces. 图形库，用于合成用户界面内容。它的设计灵感来自于现代的实时和基于物理的渲染技术，尽管我们预计它所渲染的大多数内容具有适合用户界面的非现实或风格化的品质。

 
#### **FAR** {#far}  **远** {far} 

The Fuchsia Archive Format is a container for files to be used by Zircon and Fuchsia. 紫红色档案格式是Zircon和紫红色使用的文件的容器。

 
-   [FAR Spec](/docs/concepts/storage/archive_format.md)  -[FAR规格]（/ docs / concepts / storage / archive_format.md）

 
#### **FBL** {#fbl}  ** FBL ** {fbl} 

FBL is the Fuchsia Base Library, which is shared between kernel and userspace.  FBL是Fuchsia Base Library，在内核和用户空间之间共享。

 
-   [Zircon C++](/docs/development/languages/c-cpp/cxx.md)  -[Zircon C ++]（/ docs / development / languages / c-cpp / cxx.md）

 
#### **fdio** {#fdio}  ** fdio ** {fdio} 

`fdio` is the Zircon IO Library. It provides the implementation of posix-style open(), close(), read(), write(), select(), poll(), etc, against the RemoteIORPC protocol. These APIs are return- not-supported stubs in libc, and linkingagainst libfdio overrides these stubs with functional implementations. fdio是Zircon IO库。它根据RemoteIORPC协议提供posix样式的open（），close（），read（），write（），select（），poll（）等实现。这些API是libc中不支持返回的存根，并且针对libfdio的链接使用功能实现覆盖了这些存根。

 
-   [Source](/zircon/system/ulib/fdio/)  -[来源]（/ zircon / system / ulib / fdio /）

 
#### **FIDL** {#fidl}  ** FIDL ** {fidl} 

The Fuchsia Interface Definition Language (FIDL) is a language for defining protocols that are typically used over [channels](#channel). FIDL is programminglanguage agnostic and has bindings for many popular languages, including C, C++,Dart, Go, and Rust. This approach lets system components written in a variety oflanguages interact seamlessly. 紫红色接口定义语言（FIDL）是一种用于定义通常在[通道]（通道）上使用的协议的语言。 FIDL与编程语言无关，并且具有对许多流行语言的绑定，包括C，C ++，Dart，Go和Rust。这种方法使以多种语言编写的系统组件可以无缝交互。

 
-   [FIDL](/docs/development/languages/fidl/)  -[FIDL]（/ docs / development / languages / fidl /）

 
#### **Flutter** {#flutter}  颤抖颤抖 

[Flutter](https://flutter.dev/) is a functional-reactive user interface framework optimized for Fuchsia and is used by many system components. Flutter also runson a variety of other platforms, including Android and iOS. Fuchsia itself doesnot require you to use any particular language or user interface framework. [Flutter]（https://flutter.dev/）是一种针对功能的反应性用户界面框架，针对紫红色进行了优化，并且被许多系统组件使用。 Flutter还运行其他各种平台，包括Android和iOS。紫红色本身并不要求您使用任何特定的语言或用户界面框架。

 
#### **Fuchsia API Surface** {#fuchsia-api-surface}  **紫红色API Surface ** {fuchsia-api-surface} 

The Fuchsia API Surface is the combination of the [Fuchsia System Interface](#fuchsia-system-interface) and the client librariesincluded in the [Fuchsia SDK](#fuchsia-sdk). Fuchsia API Surface是[Fuchsia系统接口]（fuchsia-system-interface）和[Fuchsia SDK]（fuchsia-sdk）中包含的客户端库的组合。

 
#### **Fuchsia Package** {#fuchsia-package}  **紫红色包装** {紫红色包装} 

A Fuchsia Package is a unit of software distribution. It is a collection of files, such as manifests, metadata, zero or more executables (e.g.[Components](#component)), and assets. Individual Fuchsia Packages can beidentified using [fuchsia-pkg URLs](#fuchsia-pkg-url). 紫红色的软件包是软件分发的单位。它是文件的集合，例如清单，元数据，零个或多个可执行文件（例如[Components]（component））和资产。可以使用[fuchsia-pkg URL]（fuchsia-pkg-url）来标识各个紫红色的包装。

 
#### **fuchsia-pkg URL** {#fuchsia-pkg-url}  ** fuchsia-pkg URL ** {fuchsia-pkg-url} 

The [fuchsia-pkg URL](/docs/concepts/storage/package_url.md) scheme is a means for referring to a repository, a package, or a package resource. The syntax is`fuchsia-pkg://<repo-hostname>[/<pkg-name>][#<path>]]`. E.g., for the component`echo_client_dart.cmx` published under the package `echo_dart`'s `meta`directory, from the `fuchsia.com` repository, its URL is`fuchsia-pkg://fuchsia.com/echo_dart#meta/echo_client_dart.cmx`. [fuchsia-pkg URL]（/ docs / concepts / storage / package_url.md）方案是一种用于引用存储库，程序包或程序包资源的方法。语法为`fuchsia-pkg：// <repo-hostname> [/ <pkg-name>] [<path>]]`。例如，对于在fuchsia.com存储库中的包echo_dart的meta目录下发布的组件echo_client_dart.cmx，其URL为fuchsia-pkg：//fuchsia.com/echo_dartmeta/echo_client_dart .cmx`。

 
#### **Fuchsia SDK** {#fuchsia-sdk}  **紫红色SDK ** {fuchsia-sdk} 

The Fuchsia SDK is a collection of libraries and tools that the Fuchsia project provides to Fuchsia developers. Among other things, the Fuchsia SDK contains adefinition of the [Fuchsia System Interface](#fuchsia-system-interface) as wellas a number of client libraries. Fuchsia SDK是Fuchsia项目提供给Fuchsia开发人员的库和工具的集合。 Fuchsia SDK尤其包含[Fuchsia系统接口]（fuchsia-system-interface）以及许多客户端库的定义。

 
#### **Fuchsia System Interface** {#fuchisa-system-interface}  **紫红色系统接口** {fuchisa-system-interface} 

The [Fuchsia System Interface](/docs/concepts/system/abi/system.md) is the binary interface that the Fuchsia operating system presents to software it runs. Forexample, the entry points into the vDSO as well as all the FIDL protocols arepart of the Fuchsia System Interface. [Fuchsia系统接口]（/ docs / concepts / system / abi / system.md）是Fuchsia操作系统提供给运行它的软件的二进制接口。例如，进入vDSO的入口点以及所有FIDL协议都是Fuchsia系统接口的一部分。

 
#### **Fuchsia Volume Manager** {#fuchsia-volume-manager}  **紫红色音量管理器** {fuchsia-volume-manager} 

Fuchsia Volume Manager (FVM) is a partition manager providing dynamically allocated groups of blocks known as slices into a virtual block address space.The FVM partitions provide a block interface enabling filesystems to interactwith it in a manner largely consistent with a regular block device. 紫红色的卷管理器（FVM）是一个分区管理器，可将动态分配的块组（称为片）分配到虚拟块地址空间中.FVM分区提供了一个块接口，使文件系统能够以与常规块设备基本一致的方式与其进行交互。

 
-   [Filesystems](/docs/concepts/storage/filesystems.md)  -[文件系统]（/ docs / concepts / storage / filesystems.md）

 
#### **GN** {#gn}  ** GN ** {gn} 

GN is a meta-build system which generates build files so that Fuchsia can be built with [Ninja](#ninja). GN is fast and comes with solid tools to manage andexplore dependencies. GN files, named `BUILD.gn`, are located all over therepository. GN是一个元生成系统，该系统生成生成文件，以便可以使用[Ninja]（ninja）构建紫红色。 GN快速且具有可靠的工具来管理和探索依赖性。整个仓库中都存在名为BUILD.gn的GN文件。

 
-   [Language and operation](https://gn.googlesource.com/gn/+/master/docs/language.md)  -[语言和操作]（https://gn.googlesource.com/gn/+/master/docs/language.md）
-   [Reference](https://gn.googlesource.com/gn/+/master/docs/reference.md)  -[参考]（https://gn.googlesource.com/gn/+/master/docs/reference.md）
-   [Fuchsia build overview](development/build/overview.md)  -[紫红色的构建概述]（development / build / overview.md）

 
#### **Handle** {#handle}  **句柄** {handle} 

A Handle is how a userspace process refers to a [kernel object](#kernel-object). They can be passed to other processes over [Channels](#channel). 句柄是用户空间进程如何引用[内核对象]（内核对象）的方法。它们可以通过[Channels]（channel）传递给其他进程。

 
-   [Reference](/docs/concepts/objects/handles.md)  -[参考]（/ docs / concepts / objects / handles.md）

 
#### **Hardware Driver** {#hardware-driver}  **硬件驱动器** {hardware-driver} 

A hardware driver is a [driver](#driver) that controls a device. It receives requests from its [core driver](#core-driver) and translates them intohardware-specific operations. Hardware drivers strive to be as thin as possible.They do not support RPC interfaces, ideally have no local worker threads (thoughthat is not a strict requirement), and some will have interrupt handlingthreads. They may be further classified into[sequential device drivers](#sequential-device-driver) and[concurrent device drivers](#concurrent-device-driver). 硬件驱动程序是控制设备的[驱动程序]（驱动程序）。它从其[核心驱动程序]（core-driver）接收请求，并将它们转换为特定于硬件的操作。硬件驱动程序力求尽可能地精简，它们不支持RPC接口，理想情况下没有本地工作线程（尽管这不是严格的要求），有些驱动程序具有中断处理线程。它们可以进一步分为[顺序设备驱动程序]（顺序设备驱动程序）和[并发设备驱动程序]（并发设备驱动程序）。

 
#### **Hub** {#hub}  **枢纽** {hub} 

The hub is a portal for tools to access detailed structural information about component instances at runtime, such as their names, job and process ids, andexposed capabilities. 该中心是一个门户网站，用于工具在运行时访问有关组件实例的详细结构信息，例如其名称，作业和流程ID以及公开的功能。

 
-   [Hub](/docs/concepts/components/hub.md)  -[集线]（/ docs / concepts / components / hub.md）

 
#### **Jiri** {#jiri}  **吉里** {jiri} 

Jiri is a tool for multi-repo development. It is used to checkout the Fuchsia codebase. It supports various subcommands which makes it easy for developers tomanage their local checkouts. Jiri是用于多仓库开发的工具。它用于签出Fuchsia代码库。它支持各种子命令，这使开发人员可以轻松地管理其本地结帐。

 
-   [Reference](https://fuchsia.googlesource.com/jiri/+/master/README.md)  -[参考]（https://fuchsia.googlesource.com/jiri/+/master/README.md）
-   [Sub commands](https://fuchsia.googlesource.com/jiri/+/master/README.md#main-commands-are)  -[子命令]（https://fuchsia.googlesource.com/jiri/+/master/README.mdmain-commands-are）
-   [Behaviour](https://fuchsia.googlesource.com/jiri/+/master/behaviour.md)  -[行为]（https://fuchsia.googlesource.com/jiri/+/master/behaviour.md）
-   [Tips and tricks](https://fuchsia.googlesource.com/jiri/+/master/howdoi.md)  -[提示和技巧]（https://fuchsia.googlesource.com/jiri/+/master/howdoi.md）

 
#### **Job** {#job}  **工作** {工作} 

A Job is a [kernel object](#kernel-object) that groups a set of related [processes][#process], their child processes, and their jobs (if any).Every process in the system belongs to a job and all jobs form a singlerooted tree. Job是一个[内核对象]（内核对象），它对一组相关的[process] [process]，它们的子进程及其作业（如果有）进行分组。系统中的每个进程都属于一个作业和所有作业形成单根树。

 
-   [Job Overview](/docs/concepts/objects/job.md)  -[工作概述]（/ docs / concepts / objects / job.md）

 
#### **Kernel Object** {#kernel-object}  **内核对象** {kernel-object} 

A kernel object is a kernel data structure which is used to regulate access to system resources such as memory, i/o, processor time and access to otherprocesses. Userspace can only reference kernel objects via [Handles](#handle). 内核对象是内核数据结构，用于调节对系统资源（如内存，I / O，处理器时间和对其他进程的访问）的访问。用户空间只能通过[Handles]（handle）引用内核对象。

 
-   [Reference](/docs/concepts/objects/objects.md)  -[参考]（/ docs / concepts / objects / objects.md）

 
#### **KOID** {#koid}  ** KODI ** {kodi} 

A Kernel Object Identifier.  内核对象标识符。

 
-   [Kernel Object](#kernel-object)  -[内核对象]（内核对象）

 
#### **Ledger** {#ledger}  **分类帐** {ledger} 

[Ledger](/src/ledger/docs/README.md) is a distributed storage system for Fuchsia. Applications use Ledger either directly or through statesynchronization primitives exposed by the [Modular](/docs/concepts/modular/overview.md) framework that are based onLedger under-the-hood. [分类帐]（/ src / ledger / docs / README.md）是紫红色的分布式存储系统。应用程序可以直接使用Ledger，也可以通过[Modular]（/ docs / concepts / modular / overview.md）框架公开的状态同步基元来使用Ledger，这些基元基于底层的Ledger。

 
#### **LK** {#lk}  ** LK ** {lk} 

Little Kernel (LK) is the embedded kernel that formed the core of the Zircon Kernel. LK is more microcontroller-centric and lacks support for MMUs,userspace, system calls -- features that Zircon added. Little Kernel（LK）是构成Zircon内核的核心的嵌入式内核。 LK更加以微控制器为中心，并且缺乏对MMU，用户空间，系统调用的支持-Zircon添加了这些功能。

 
-   [LK on Github](https://github.com/littlekernel/lk)  -[Github上的LK]（https://github.com/littlekernel/lk）

 
#### **Module** {#module}  **模块** {module} 

A module is a role a [component](#Component) can play to participate in a [story](#Story). Every component can be be used as a module, but typically amodule is asked to show UI. Additionally, a module can have a `module` metadatafile which describes the Module's data compatibility and semantic role. 模块是[component]（Component）可以参与[story]（Story）的角色。每个组件都可以用作模块，但是通常会要求一个模块显示UI。此外，模块可以具有描述模块的数据兼容性和语义角色的“模块”元数据文件。

 
-   [Module metadata format](/docs/concepts/modular/module.md)  -[模块元数据格式]（/ docs / concepts / modular / module.md）

 
#### **Musl** {#musl}  ** Musl ** {musl} 

Fuchsia's standard C library (libc) is based on Musl Libc.  紫红色的标准C库（libc）基于Musl Libc。

 
-   [Source](/zircon/third_party/ulib/musl/)  -[来源]（/ zircon / third_party / ulib / musl /）
-   [Musl Homepage](https://www.musl-libc.org/)  -[Musl主页]（https://www.musl-libc.org/）

 
#### **Namespace** {#namespace}  **命名空间** {namespace} 

A namespace is the composite hierarchy of files, directories, sockets, [service](#service)s, and other named objects which are offered to components bytheir [environment](#environment). 命名空间是文件，目录，套接字，[服务]（服务）和其他命名对象的组合层次结构，这些文件，目录，套接字，[服务]（服务）和其他命名对象由其[环境]（环境）提供给组件。

 
-   [Fuchsia Namespace Spec](/docs/concepts/framework/namespaces.md)  -[紫红色命名空间规范]（/ docs / concepts / framework / namespaces.md）

 
#### **Netstack** {#netstack}  ** Netstack ** {netstack} 

An implementation of TCP, UDP, IP, and related networking protocols for Fuchsia.  紫红色的TCP，UDP，IP和相关网络协议的实现。

 
#### **Ninja** {#ninja}  **忍者** {ninja} 

Ninja is the build system executing Fuchsia builds. It is a small build system with a strong emphasis on speed. Unlike other systems, Ninja files are notsupposed to be manually written but should be generated by other systems, suchas [GN](#gn) in Fuchsia. 忍者是执行紫红色构建的构建系统。这是一个小型构建系统，非常注重速度。与其他系统不同，Ninja文件不应手动编写，而应由其他系统生成，例如紫红色的[GN]（gn）。

 
-   [Manual](https://ninja-build.org/manual.html)  -[手册]（https://ninja-build.org/manual.html）
-   [Ninja rules in GN](https://gn.googlesource.com/gn/+/master/docs/reference.md#ninja_rules)  -[GN中的忍者规则]（https://gn.googlesource.com/gn/+/master/docs/reference.mdninja_rules）
-   [Fuchsia build overview](development/build/overview.md)  -[紫红色的构建概述]（development / build / overview.md）

 
#### **Outgoing directory** {#outgoing-directory}  **外发目录** {外发目录} 

A file system directory where a [component](#component) may [expose](#expose) capabilities for others to use. [组件]（组件）可以[暴露]（暴露）功能以供他人使用的文件系统目录。

 
#### **Package** {#package}  **包装** {package} 

Package is an overloaded term. Package may refer to a [Fuchsia Package](#fuchsia-package) or a [GN build package](#gn). 打包是一个重载术语。程序包可以指[Fuchsia程序包]（紫红色程序包）或[GN构建程序包]（gn）。

 
#### **Paver** {#paver}  **摊铺机** {摊铺机} 

A tool in Zircon that installs partition images to internal storage of a device.  Zircon中的一种工具，用于将分区映像安装到设备的内部存储中。

 
-   [Guide for installing Fuchsia with paver](/docs/development/workflows/paving.md).  -[使用铺路机安装紫红色的指南]（/ docs / development / workflows / paving.md）。

 
#### **Platform Source Tree** {#platform-source-tree}  **平台源代码树** {platform-source-tree} 

The Platform Source Tree is the open source code hosted on fuchsia.googlesource.com, which comprises the source code for Fuchsia. A givenFuchsia system can include additional software from outside the Platform SourceTree by adding the appropriate [Fuchsia Package](#fuchsia-package). 平台源代码树是fuchsia.googlesource.com上托管的开放源代码，其中包括Fuchsia的源代码。给定的Fuchsia系统可以通过添加适当的[Fuchsia程序包]（fuchsia-package）从Platform SourceTree外部包括其他软件。

 
#### **Process** {#process}  **处理** {处理} 

A Process is a [kernel object](#kernel-object) that represents an instance of a program as a set of instructions which are executed by one or more[threads](#thread) together with a collection of [capabilities](#capability).Every process is contained in a [job](#job). 进程是[内核对象]（内核对象），它作为一组指令来表示程序的一个实例，这些指令由一个或多个[线程]（线程）执行，并带有[功能]（功能）的集合。每个过程都包含在一个[job]（job）中。

 
-   [Process Overview](/docs/concepts/objects/process.md)  -[流程概述]（/ docs / concepts / objects / process.md）

 
#### **Realm** {#realm}  **领域** {realm} 

In [components v1](#components-v1), realm is synonymous to [environment](#environment). 在[components v1]（components-v1）中，领域与[environment]（环境）同义。

In [components v2](#components-v2), a realm is a subtree of component instances in the [component instance tree](#component-instance-tree). It acts as acontainer for component instances and capabilities in the subtree. 在[components v2]（components-v2）中，领域是[component instance tree]（component-instance-tree）中组件实例的子树。它充当子树中组件实例和功能的容器。

 
#### **Runner** {#runner}  **赛跑者** {跑步者} 

A [component](#component) that provides a runtime environment for other components, e.g. the ELF runner, the Dart AOT runner, the Chromium web runner. 一个[component]（component），它为其他组件提供运行时环境。 ELF运行器，Dart AOT运行器，Chromium网络运行器。

Every component needs a runner in order to launch. Components express their dependency on a runner in the component's [declaration](#component-declaration). 每个组件都需要一个运行器才能启动。组件在组件的[declaration]（component-declaration）中表达对运行器的依赖性。

When the [component framework](#component-framework) starts a component, it first determines the capabilities that the component should receive, then asks thecomponent's runner to launch the component. The runner is responsible for creatingany necessary processes, loading executable code, initializing language runtimes,handing control to the component's entry points, and terminating the component whenrequested by the component framework. 当[组件框架]（component-framework）启动一个组件时，它首先确定该组件应具备的功能，然后要求组件的运行者启动该组件。运行程序负责创建任何必要的进程，加载可执行代码，初始化语言运行时，将控制交给组件的入口点以及在组件框架请求时终止组件。

 
-   [ELF runner](/docs/concepts/components/elf_runner.md)  -[ELF亚军]（/ docs / concepts / components / elf_runner.md）

 
#### **Scenic** {#scenic}  **风景** {风景} 

The system compositor. Includes views, input, compositor, and GPU services.  系统合成器。包括视图，输入，合成器和GPU服务。

 
#### **Sequential Device Driver** {#sequential-device-driver}  **顺序设备驱动程序** {sequential-device-driver} 

A sequential device driver is a [hardware driver](#hardware-driver) that will only service a single request at a time. The [core driver](#core-driver)synchronizes and serializes all requests. 顺序设备驱动程序是[硬件驱动程序]（硬件驱动程序），一次只能处理一个请求。 [核心驱动程序]（core-driver）同步并序列化所有请求。

 
#### **Service** {#service}  **服务** {service} 

A service is an implementation of a [FIDL](#fidl) interface. Components can offer their creator a set of services, which the creator can either use directlyor offer to other components. 服务是[FIDL]（fidl）接口的实现。组件可以为创建者提供一组服务，创建者可以直接使用这些服务，也可以向其他组件提供服务。

Services can also be obtained by interface name from a [Namespace](#namespace), which lets the component that created the namespace pick the implementation ofthe interface. Long-running services, such as [Scenic](#scenic), are typicallyobtained through a [Namespace](#namespace), which lets many clients connect to acommon implementation. 也可以通过接口名称从[名称空间]（名称空间）获取服务，该服务使创建名称空间的组件可以选择接口的实现。诸如[Scenic]（scenic）之类的长期运行的服务通常是通过[Namespace]（namespace）获得的，该服务使许多客户端可以连接到通用实现。

 
#### **Service capability** {#service-capability}  **服务能力** {service-capability} 

A [capability](#capability) that permits communicating with a [service](#service) over a [channel](#channel) using a specified [FIDL](#fidl)protocol. The server end of the channel is held by the[component instance](#component-instance) that provides the capability. Theclient end of the channel is given to the[component instance](#component-instance) that [uses](#use) the capability. [能力] [能力]允许使用指定的[FIDL]（fidl）协议通过[通道]（通道）与[服务]（服务）进行通信。通道的服务器端由提供该功能的[component instance]（component-instance）持有。通道的客户端被赋予[使用]（使用）功能的[组件实例]（组件实例）。

 
-   [Capability routing](#capability-routing)  -[功能路由]（功能路由）

Service capability is a [components v2](#components-v2) concept.  服务能力是[components v2]（components-v2）概念。

 
#### **Session** {#session}  **会话** {session} 

An interactive session with one or more users. Has a [session shell](#session-shell), which manages the UI for the session, and zeroor more [stories](#story). A device might have multiple sessions, for example ifusers can interact with the device remotely or if the device has multipleterminals. 与一个或多个用户的交互式会话。有一个[session shell]（session-shell），用于管理该会话的UI，并且零个或多个[stories]（story）。一个设备可能具有多个会话，例如，如果用户可以与该设备进行远程交互，或者该设备具有多个终端。

 
#### **Session Shell** {#session-shell}  **会话外壳** {session-shell} 

The replaceable set of software functionality that works in conjunction with devices to create an environment in which people can interact with mods, agentsand suggestions. 与设备结合使用的可替换软件功能集，可创建一个环境，人们可以在其中与mod，agent和建议进行交互。

 
#### **Storage capability** {#storage-capability}  **存储能力** {storage-capability} 

A storage capability is a [capability](#capability) that allocates per-component isolated storage for a designated purpose within a filesystem directory.Multiple [component instances](#component-instance) may be given the samestorage capability, but underlying directories that are isolated from each otherwill be allocated for each individual use. This is different from[directory capabilities](#directory-capability), where a specific filesystemdirectory is routed to a specific component instance. 存储功能是一种[能力]（capability），用于为文件系统目录中的指定用途分配每个组件的隔离存储。可以为多个[组件实例]（component-instance）赋予相同的存储能力，但基础目录是隔离的彼此之间的分配将分配给每种单独的用途。这与[目录功能]（目录功能）不同，后者将特定的文件系统目录路由到特定的组件实例。

Isolation is achieved because Fuchsia does not support [dotdot](/docs/concepts/storage/dotdot.md). 由于紫红色不支持点（/docs/concepts/storage/dotdot.md），因此可以实现隔离。

There are three types of storage capabilities:  共有三种存储功能：

 
-   *data*: a directory is added to the [namespace](#namespace) of the [component instance](#component-instance) that [uses](#use) the capability.Acts as a [data directory](#data-directory). -* data *：将目录添加到[使用]功能的[组件实例] [组件实例]的[名称空间] [名称空间]。充当[数据目录]（数据目录） 。
-   *cache*: same as data, but acts as a [cache directory](#cache-directory).  -* cache *：与数据相同，但充当[cache目录]（cache-directory）。
-   *meta*: a directory is allocated to be used by component manager, where it will store metadata to enable features like persistent[component collections](#component-collection). -* meta *：已分配目录供组件管理器使用，该目录将存储元数据以启用诸如persistent [component collections]（component-collection）之类的功能。

Storage capability is a [components v2](#components-v2) concept.  存储功能是[components v2]（components-v2）概念。

 
-   [Capability routing](#capability-routing)  -[功能路由]（功能路由）
-   [Storage capabilities](/docs/concepts/components/capabilities/storage.md)  -[存储功能]（/ docs / concepts / components / capabilities / storage.md）

 
#### **Story** {#story}  **故事** {故事} 

A user-facing logical container encapsulating human activity, satisfied by one or more related modules. Stories allow users to organize activities in ways theyfind natural, without developers having to imagine all those ways ahead of time. 封装人类活动的面向用户的逻辑容器，由一个或多个相关模块满足。故事允许用户以自然的方式组织活动，而开发人员不必提前想象所有这些方式。

 
#### **Story Shell** {#story-shell}  ** Story Shell ** {story-shell} 

The system responsible for the visual presentation of a story. Includes the presenter component, plus structure and state information read from each story. 负责故事的视觉呈现的系统。包括演示者组件，以及从每个故事中读取的结构和状态信息。

 
#### **Thread** {#thread}  **线程** {thread} 

A Thread is a [kernel object](#kernel-object) that represents a time-shared CPU execution context. Each thread is contained in a [process](#process). 线程是一个[kernel object]（内核对象），代表一个分时的CPU执行上下文。每个线程都包含在[process]（process）中。

 
-   [Thread Overview](/docs/concepts/objects/thread.md)  -[线程概述]（/ docs / concepts / objects / thread.md）

 
#### **userboot** {#userboot}  ** userboot ** {userboot} 

userboot is the first process started by the Zircon kernel. It is loaded from the kernel image in the same way as the [vDSO](#virtual-dynamic-shared-object),instead of being loaded from a filesystem. Its primary purpose is to load thesecond process, [bootsvc](#bootsvc), from the [bootfs](#bootfs). userboot是Zircon内核启动的第一个进程。它以与[vDSO]（虚拟动态共享对象）相同的方式从内核映像加载，而不是从文件系统加载。其主要目的是从[bootfs]（bootfs）加载第二个进程[bootsvc]（bootsvc）。

 
-   [Documentation](/docs/concepts/booting/userboot.md)  -[文档]（/ docs / concepts / booting / userboot.md）

 
#### **Virtual Dynamic Shared Object** {#virtual-dynamic-shared-object}  **虚拟动态共享对象** {virtual-dynamic-shared-object} 

The Virtual Dynamic Shared Object (vDSO) is a Virtual Shared Library -- it is provided by the [Zircon](#zircon) kernel and does not appear in the filesystemor a package. It provides the Zircon System Call API/ABI to userspace processesin the form of an ELF library that's "always there." In the Fuchsia SDK and[Zircon DDK](#ddk) it exists as `libzircon.so` for the purpose of havingsomething to pass to the linker representing the vDSO. 虚拟动态共享库（vDSO）是一个虚拟共享库-它由[Zircon]（zircon）内核提供，没有出现在文件系统或软件包中。它以“始终存在”的ELF库的形式向用户空间进程提供Zircon系统调用API / ABI。在Fuchsia SDK和[Zircon DDK]（ddk）中，它以“ libzircon.so”的形式存在，目的是使某些内容传递给表示vDSO的链接器。

 
#### **Virtual Memory Address Range** {#virtual-memory-address-range}  **虚拟内存地址范围** {virtual-memory-address-range} 

A Virtual Memory Address Range (VMAR) is a Zircon [kernel object](#kernel-object) that controls where and how[Virtual Memory Objects](#virtual-memory-object) may be mapped into the addressspace of a process. 虚拟内存地址范围（VMAR）是Zircon [内核对象]（内核对象），它控制[虚拟内存对象]（虚拟内存对象）在何处以及如何映射到进程的地址空间。

 
-   [VMAR Overview](/docs/concepts/objects/vm_address_region.md)  -[VMAR概述]（/ docs / concepts / objects / vm_address_region.md）

 
#### **Virtual Memory Object** {#virtual-memory-object}  **虚拟内存对象** {virtual-memory-object} 

A Virtual Memory Object (VMO) is a Zircon [kernel object](#kernel-object) that represents a collection of pages (or the potential for pages) which may be read,written, mapped into the address space of a process, or shared with anotherprocess by passing a [Handle](#handle) over a [Channel](#channel). 虚拟内存对象（VMO）是Zircon [内核对象]（内核对象），它表示可以被读取，写入，映射到进程的地址空间或共享的页面集合（或潜在的页面）。通过[Channel]（通道）传递[Handle]（句柄）与另一个进程一起使用。

 
-   [VMO Overview](/docs/concepts/objects/vm_object.md)  -[VMO概述]（/ docs / concepts / objects / vm_object.md）

 
#### **Zircon Boot Image** {#zircon-boot-image}  ** Zircon引导映像** {zircon-boot-image} 

A Zircon Boot Image (ZBI) contains everything needed during the boot process before any drivers are working. This includes the kernel image and a[RAM disk for the boot filesystem](#bootfs). Zircon引导映像（ZBI）包含在引导过程中任何驱动程序正常工作之前所需的所有内容。这包括内核映像和[用于引导文件系统的RAM磁盘]（bootfs）。

 
-   [ZBI header file](/zircon/system/public/zircon/boot/image.h)  -[ZBI头文件]（/ zircon / system / public / zircon / boot / image.h）

 
#### **Zedboot** {#zedboot}  ** Zedboot ** {zedboot} 

Zedboot is a recovery image that is used to install and boot a full Fuchsia system. Zedboot is actually an instance of the Zircon kernel with a minimal setof drivers and services running used to bootstrap a complete Fuchsia system on atarget device. Upon startup, Zedboot listens on the network for instructionsfrom a bootserver which may instruct Zedboot to [install](#paver) a new OS. Uponcompleting the installation Zedboot will reboot into the newly installed system. Zedboot是一个恢复映像，用于安装和引导完整的Fuchsia系统。 Zedboot实际上是Zircon内核的一个实例，运行着最少的驱动程序和服务，用于在目标设备上引导完整的Fuchsia系统。启动后，Zedboot会在网络上侦听来自引导服务器的指令，这些指令可能会指示Zedboot [安装]（摊铺）新操作系统。完成安装后，Zedboot将重新引导到新安装的系统中。

 
#### **Zircon** {#zircon}  **锆石** {锆石} 

Zircon is the [microkernel](https://en.wikipedia.org/wiki/Microkernel) and lowest level userspace components (driver runtime environment, core drivers,libc, etc) at the core of Fuchsia. In a traditional monolithic kernel, many ofthe userspace components of Zircon would be part of the kernel itself. Zircon是紫红色核心的[microkernel]（https://en.wikipedia.org/wiki/Microkernel）和最低级别的用户空间组件（驱动程序运行时环境，核心驱动程序，libc等）。在传统的整体内核中，Zircon的许多用户空间组件将成为内核本身的一部分。

 
-   [Zircon Documentation](/zircon/README.md)  -[Zircon文档]（/ zircon / README.md）
-   [Zircon Concepts](/docs/concepts/kernel/concepts.md)  -[Zircon概念]（/ docs / concepts / kernel / concepts.md）
-   [Source](/zircon)  -[来源]（/锆石）

 
#### **ZX** {#zx}  ** ZX ** {zx} 

ZX is an abbreviation of "Zircon" used in Zircon C APIs/ABIs (`zx_channel_create()`, `zx_handle_t`, `ZX_EVENT_SIGNALED`, etc) and libraries(libzx in particular). ZX是Zircon C API / ABI（“ zx_channel_create（）”，“ zx_handle_t”，“ ZX_EVENT_SIGNALED”等）和库（尤其是libzx）中使用的“ Zircon”的缩写。

 
#### **ZXDB** {#zxdb}  ** ZXDB ** {zxdb} 

The native low-level system debugger.  本机低级系统调试器。

 
