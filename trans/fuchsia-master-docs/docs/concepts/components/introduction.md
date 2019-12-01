 
# Introduction to the Fuchsia Component Framework  紫红色组件框架简介 

This document offers a brief conceptual overview of the component framework along with links to more detailed documents on specific topics. 本文档提供了组件框架的简要概念概述，以及指向特定主题的更详细文档的链接。

Note: The component framework is under active development. This document only covers the [new architecture][glossary-components-v2] implemented by`component_manager`. The [old architecture][glossary-components-v1] implementedby `appmgr` is still in use but will be removed once the transition to thenew architecture is complete. 注意：组件框架正在积极开发中。本文档仅涵盖由component_manager实现的[新架构] [glossary-components-v2]。由appmgr实现的[旧体系结构] [glossary-components-v1]仍在使用中，但一旦完成向新体系结构的过渡，便将其删除。

 
## Components and the Component Framework  组件和组件框架 

A [component][glossary-component] is a program that runs in its own sandbox on Fuchsia and that interacts with other components using inter-processcommunication [channels][glossary-channel]. [component] [glossary-component]是一个程序，它在紫红色的自己的沙箱中运行，并且使用进程间通信[通道] [glossary-channel]与其他组件进行交互。

The component framework is a [framework][wiki-software-framework] for developing [component-based software][wiki-component-based-software] for Fuchsia. 组件框架是用于开发用于紫红色的[基于组件的软件] [基于Wiki组件的软件]的[框架] [wiki-软件框架]。

The component framework is responsible for running nearly all software on Fuchsia so it is important for developers to learn how it works and how touse it effectively. 组件框架负责在Fuchsia上运行几乎所有软件，因此对于开发人员来说，了解其工作方式和有效使用方式非常重要。

 
## Purpose  目的 

The component framework emphasizes [separation of concerns][wiki-separation-of-concerns] by helping developersto write simpler programs as components that work together to support morecomplex systems through composition. 组件框架通过帮助开发人员将更简单的程序编写为组件，从而协同工作以通过组合支持更复杂的系统，从而强调了[关注点分离] [wiki-separation-of-cerns]。

Each component typically has a small number of responsibilities. For example, an ethernet driver component exposes a hardware interface service that thenetwork stack component uses to send and receive ethernet frames. Thesecomponents can work together smoothly because they agree on a common setof protocols even though they may have been authored by different partiesor distributed separately. 每个组件通常都有少量职责。例如，以太网驱动程序组件公开了硬件接口服务，网络堆栈组件使用该接口发送和接收以太网帧。这些组件可以顺利地工作，因为即使它们可能是由不同的参与方创作或单独分发的，但它们都同意一组通用的协议。

Software composition offers numerous advantages:  软件组成具有许多优点：

 
- Configurability: The behavior of the system can be changed easily by adding, upgrading, removing, or replacing individual components. -可配置性：可以通过添加，升级，删除或更换单个组件轻松更改系统的行为。
- Extensibility: As components are added, the functionality of the system grows.  -可扩展性：随着组件的添加，系统的功能也随之增长。
- Reliability: The system can recover from faults gracefully by stopping or restarting individual components. -可靠性：系统可以通过停止或重新启动各个组件来从故障中恢复。
- Reuse: General purpose components can be reused and composed with other components to solve new problems. -重用：通用组件可以被重用，并与其他组件组合在一起以解决新问题。
- Testability: Prior to integration, each component can be verified separately so it is easier to isolate bugs. 可测试性：在集成之前，可以分别验证每个组件，因此更容易隔离错误。
- Uniformity: All components describe their capabilities in the same way independent of their origin, purpose, or implementation language. -统一性：所有组件都以相同的方式描述其功能，而与它们的来源，目的或实现语言无关。

Fuchsia takes software composition to its logical conclusion by building almost the entire system from components (including device drivers). Thecomponent framework makes it easier to update and improve the systemincrementally as new software becomes available. 紫红色通过从组件（包括设备驱动程序）构建几乎整个系统，将软件组合推到了逻辑上的结论。随着新软件的推出，组件框架使升级和改进系统变得更加容易。

 
## Everything is a Component (Almost)  一切都是一个组成部分（几乎） 

Components are ubiquitous. They are governed by the same mechanisms and they all work together seamlessly. 组件无处不在。它们由相同的机制控制，并且都可以无缝地协同工作。

Almost all programs run as components on Fuchsia, including:  几乎所有程序都在Fuchsia上作为组件运行，包括：

 
- Command-line tools  -命令行工具
- Device drivers  - 设备驱动程序
- End-user applications  -最终用户应用
- Filesystems  -文件系统
- Media codecs  -媒体编解码器
- Network stacks  -网络堆栈
- Tests  -测试
- Web pages  - 网页

There are only a few exceptions, notably:  只有少数例外，尤其是：

 
- Bootloaders  -引导程序
- Device firmware  -设备固件
- Kernels  -内核
- Bootstrap for the component manager itself  -组件管理器本身的引导程序
- Virtual machine guest operating systems  -虚拟机来宾操作系统

 
## A Component is a Hermetic Composable Isolated Program  组件是密封的可组合隔离程序 

A component is a **program**.  组件是一个程序。

 
- It is a unit of executable software.  -它是可执行软件的一个单元。
- It is identified by a URL from which its code can be loaded and instantiated.  -由URL标识，可以从中加载和实例化其代码。
- Its behavior can be implemented in any programming language for which a suitable component runner exists. -它的行为可以用适合组件运行器的任何编程语言来实现。
- It has a [declaration][glossary-component-declaration] that describes what it can do and how to run it. -它具有[说明] [词汇表组件说明]，它描述了它可以做什么以及如何运行。

A component is an **isolated** program.  组件是一个“隔离的”程序。

 
- Each of its instances runs in its own separate "sandbox".  -每个实例都在其自己的单独“沙盒”中运行。
- It is granted limited [capabilities][glossary-capability] to perform its task according to the [Principle of Least Privilege][wiki-least-privilege]. -根据[最小特权原则] [wiki-最小特权]被授予执行任务的有限[能力] [词汇能力]。
- It cannot access capabilities other than those it has been granted.  -它不能访问已授予的功能。
- Its lifecycle and state are independent from that of other components.  -它的生命周期和状态独立于其他组件。
- It primarily communicates with other components via IPC.  -它主要通过IPC与其他组件进行通信。
- Its faults and misbehavior cannot compromise the integrity of the entire system. -其故障和不当行为不会损害整个系统的完整性。

A component is a **composable** isolated program.  组件是一个“可组合的”隔离程序。

 
- It can be combined with other components to form more complex components.  -可以与其他组件组合以形成更复杂的组件。
- It can reuse the functionality of other components by adding instances of them as its children given their URL, both statically and dynamically. -它可以通过静态地和动态地添加其他组件的实例作为给定其URL的子组件来重用其他组件的功能。
- It grants capabilities to its children using [capability routing](#capability-routing). -它使用[功能路由]（capability-routing）向其子级授予功能。

A component is a **hermetic** composable isolated program.  组件是“可密封的”可组合隔离程序。

 
- It represents an encapsulation boundary.  -它表示封装边界。
- Its implementation can be changed without affecting other components as long as it exposes the same capabilities to them. -只要可以向其他组件公开相同的功能，就可以在不影响其他组件的情况下更改其实现。
- It is distributed in a form that includes everything its [component runner][doc-runners] needs to run it, including its shared libraries. -它以包括[组件运行器] [doc-runners]运行它所需的所有内容的形式分发，包括其共享库。

 
## Component Manager and the Boot Process {#component-manager}  组件管理器和引导过程{component-manager} 

The [component manager][glossary-component-manager] is the heart of the component framework. It manages the lifecycle of all components, provides themwith the [capabilities][doc-capabilities] they require, and keeps them isolatedfrom one another. [组件管理器] [词汇表组件管理器]是组件框架的核心。它管理所有组件的生命周期，为它们提供所需的[功能] [文档功能]，并使它们彼此隔离。

The system starts the component manager very early in the boot process. The component manager first starts the root component. The root componentthen asks the component manager to start other components including the devicemanager, filesystems, network stack, and other essential services. 系统非常在启动过程的早期启动组件管理器。组件管理器首先启动根组件。然后，根组件要求组件管理器启动其他组件，包括设备管理器，文件系统，网络堆栈和其他基本服务。

As more and more components are started, the system springs to life. Eventually, the [session framework][glossary-session-framework] starts the user interfacecomponents and the user takes control. 随着越来越多的组件启动，该系统如虎添翼。最终，[会话框架] [glossary-session-framework]启动了用户界面组件，并由用户控制。

 
## Component Instances {#component-instances}  组件实例{component-instances} 

A [component instance][glossary-component-instance] is a distinct copy of a component running in its own sandbox with its own state that is separate fromthat of any other component instance. [组件实例] [glossary-component-instance]是在其自己的沙箱中运行且其自身状态与任何其他组件实例的状态独立的组件的不同副本。

The terms component and component instance are often used interchangeably when the context is clear. For example, it would be more precise to talk about"starting a component instance" rather than "starting a component" but youcan easily infer that "starting a component" requires an instance of thatcomponent to be created first so that the instance can be started. 当上下文明确时，术语“组件”和“组件实例”通常可以互换使用。例如，谈论“启动组件实例”比“启动组件”更为精确，但是您可以轻松推断出“启动组件”要求首先创建该组件的实例，以便可以启动该实例。 。

 
## Component Lifecycle {#component-lifecycle}  组件生命周期{component-lifecycle} 

Component instances progress through four major lifecycle events: create, start, stop, and destroy. 组件实例通过四个主要生命周期事件进行处理：创建，启动，停止和销毁。

Unlike [processes][glossary-process], component instances continue to exist and can retain state even when they are not running thereby allowing them tobe stopped and restarted repeatedly while preserving the[illusion of continuity](#continuity). 与[process] [glossary-process]不同，组件实例继续存在并且即使在它们不运行时也可以保持状态，从而允许它们在保持连续性（连续性）的同时被停止和重复启动。

Refer to [lifecycle][doc-lifecycle] for more details.  有关更多详细信息，请参考[lifecycle] [doc-lifecycle]。

 
### Create  创建 

When a component instance is created, the component frameworks assigns a unique identity to the instance, adds it to the[component topology](#component-topology), and makes its capabilitiesavailable for other components to use. 创建组件实例后，组件框架将为该实例分配唯一的标识，并将其添加到[组件拓扑]（组件拓扑），并使其功能可供其他组件使用。

Once created, a component instance can then be started or destroyed.  创建组件实例后，即可启动或销毁它。

 
### Start  开始 

Starting a component instance loads and runs the component's program and provides it access to the capabilities that it requires. 启动组件实例将加载并运行组件的程序，并为其提供对其所需功能的访问权限。

[Every component runs for a reason](#accountability). The component framework only starts a component instance when it has work to do, such as whenanother component requests to use its the instance's capabilities. [每个组件运行都有原因]（问责制）。组件框架仅在有工作要做时才启动组件实例，例如当另一个组件请求使用其实例的功能时。

Once started, a component instance continues to run until it is stopped.  一旦启动，组件实例将继续运行直到停止。

 
### Stop  停止 

Stopping a component instance terminates the component's program but preserves its [persistent state][doc-storage] so that it can continue where it left offwhen subsequently restarted. 停止组件实例将终止该组件的程序，但保留其[持久状态] [doc-storage]，以便它可以在随后重新启动时停止的地方继续运行。

The component framework may stop a component instance for a variety of reasons, such as: 组件框架可能由于多种原因而停止组件实例，例如：

 
- When all of its clients have disconnected.  -当其所有客户端断开连接时。
- When its parent is being stopped.  -停止其父项时。
- When its package needs to be updated.  -需要更新其软件包时。
- When there are insufficient resources to keep running the component.  -当资源不足以继续运行组件时。
- When other components need resources more urgently.  -当其他组件更急需资源时。
- When the component is about to be destroyed.  -当组件即将被销毁时。
- When the system is shutting down.  -系统关闭时。

A component can implement a [lifecycle handler][doc-lifecycle] to be notified of its impending termination and other events on a best effort basis. Notethat a component can be terminated involuntarily and without notice incircumstances such as resource exhaustion, crashes, or power failure. 组件可以实现[lifecycle handler] [doc-lifecycle]，以便尽力而为地通知其即将终止和其他事件。请注意，组件可以非自愿地终止，并且在没有通知的情况下（例如资源耗尽，崩溃或断电）。

Once stopped, a component instance can then be restarted or destroyed.  一旦停止，就可以重新启动或销毁组件实例。

 
### Destroy  破坏 

Destroying a component instance permanently deletes all of its associated state and releases the system resources it consumed. 销毁组件实例将永久删除其所有关联状态，并释放其消耗的系统资源。

Once destroyed, a component instance ceases to exist and cannot be restarted. New instances of the same component can still be created but they will eachhave their own identity and state distinct from all prior instances. 一旦销毁，组件实例将不复存在并且无法重新启动。仍然可以创建相同组件的新实例，但是它们将具有与所有先前实例不同的身份和状态。

 
## Component Declarations {#component-declarations}  组件声明{component-declarations} 

A [component declaration][doc-manifests] is a machine-readable description of what the component can do and how to run it. It containsmetadata that the component framework requires to instantiate the componentand to compose the component with others. [组件声明] [doc-manifests]是组件可以做什么以及如何运行的机器可读描述。它包含组件框架实例化组件以及与其他组件组成组件所需的元数据。

Every component has a declaration. For components that are distributed in [packages][glossary-package], the declaration typically takes the form ofa [component manifest file][doc-manifests]. 每个组件都有一个声明。对于以[程序包] [词汇表程序包]分发的组件，声明通常采用[组件清单文件] [doc-manifests]的形式。

Components can also be distributed in other forms such as web applications with the help of a suitable [resolver][doc-resolvers] and [runner][doc-runners]which provide the necessary component declaration and take care of running thecomponent. 组件也可以在适当的[resolver] [doc-resolvers]和[runner] [doc-runners]的帮助下以其他形式分发，例如Web应用程序，它们提供必要的组件声明并负责运行组件。

For example, the declaration for a calculator component might specify the following information: 例如，计算器组件的声明可能指定以下信息：

 
- The location of the calculator program within its package.  -计算器程序在其程序包中的位置。
- The name of the [runner][doc-runners] used to run the program.  -用于运行程序的[runner] [doc-runners]的名称。
- A request for persistent storage to save the contents of the calculator's accumulator across restarts. -请求持久存储以在重新启动时保存计算器累加器的内容。
- A request to use capabilities to present a user interface.  -使用功能来呈现用户界面的请求。
- A request to expose capabilities to allow other components to access the calculator's accumulator register using inter-process communication. -请求公开功能以允许其他组件使用进程间通信访问计算器的累加器寄存器。

 
## Component URLs {#component-urls}  组件网址{component-urls} 

A component URL specifies the location from which a component's declaration, program, and assets are retrieved. 组件URL指定从中检索组件的声明，程序和资产的位置。

Components can be retrieved from many different sources as indicated by the URL scheme. These are some common URL schemes you may encounter: 可以从URL方案指示的许多不同来源检索组件。这些是您可能会遇到的一些常见URL方案：

 
- `fuchsia-boot`: The component is resolved from the system boot image. This scheme is used for retrieving components that are essential to the system'soperation during early boot before the package system is available. -`fuchsia-boot`：该组件是从系统启动映像中解析的。此方案用于在软件包系统可用之前在早期引导期间检索对于系统操作必不可少的组件。
  - Example: "fuchsia-boot:///#meta/devcoordinator.cm"  -示例：“ fuchsia-boot：///meta/devcoordinator.cm”
- [`fuchsia-pkg`][doc-package-url]: The component is resolved by the Fuchsia package resolver. This scheme is used for components that aredistributed in the form of packages which can be downloaded on demand andkept up-to-date. -[`fuchsia-pkg`] [doc-package-url]：该组件由Fuchsia包解析器解析。此方案用于以软件包形式分发的组件，这些组件可以按需下载并保持最新状态。
  - Example: "fuchsia-pkg://fuchsia.com/netstack#meta/netstack.cm"  -示例：“ fuchsia-pkg：//fuchsia.com/netstackmeta/netstack.cm”
- `http` and `https`: The component is resolved as a web application by a web resolver. This scheme is used to integrate web-based content with thecomponent framework. -`http`和`https`：该组件由Web解析器解析为Web应用程序。该方案用于将基于Web的内容与组件框架集成在一起。
  - Example: "https://fuchsia.dev/"  -例如：“ https://fuchsia.dev/”

Note: The set of URL schemes available in each [realm](#realms) is configured with [capability routing](#capability-routing) in accordance with the realm'sneed to access components from various sources. The examples presented aboveare not universal. 注意：每个[领域]（领域）中可用的URL方案集根据领域访问各种来源组件的需要而配置了[功能路由]（capability-routing）。上面提供的示例不是通用的。

Note: Use [monikers](#monikers) to identify specific instances of components instead of their source. 注意：使用[monikers]（monikers）标识组件的特定实例，而不是其来源。

 
## Component Topology {#component-topology}  组件拓扑{component-topology} 

The component topology is an abstract data structure that describes the relationships among component instances. It is made of three parts: 组件拓扑是描述组件实例之间关系的抽象数据结构。它由三部分组成：

 
- Component instance tree: Describes how component instances are [composed](#composition) together (their parent-child relationships). -组件实例树：描述如何将组件实例[组成]（组成）在一起（它们的父子关系）。
- Capability routing graph: Describes how component instances gain access to [use capabilities](#capability-routing) exposed by other component instances(their provider-consumer relationships). -能力路由图：描述组件实例如何访问其他组件实例（其提供者与消费者之间的关系）所公开的[使用能力]（能力路由）。
- Compartment tree: Describes how component instances are [isolated](#compartments) from one another and the resources their sandboxesmay share at runtime (their isolation relationships). -隔间树：描述组件实例如何相互隔离（隔间）以及它们的沙箱在运行时可以共享的资源（它们的隔离关系）。

TODO: Add a picture or a thousand words.  待办事项：添加图片或一千个单词。

The structure of the component topology greatly influences component lifecycle and use of capabilities. 组件拓扑的结构极大地影响了组件的生命周期和功能的使用。

 
### Hierarchical Composition {#composition}  层次组成{组成} 

Any number of components can be combined together to make more complex components through hierarchical composition. 可以将任意数量的组件组合在一起，以通过层次结构组成更复杂的组件。

In hierarchical composition, a parent component creates instances of other components which are known as its children. The newly created children belongto the parent and are dependent upon the parent to provide them with thecapabilities that they need to run. Meanwhile, the parent gains access to thecapabilities exposed by its children through[capability routing](#capability-routing). 在层次结构中，父组件创建其他组件的实例，这些实例称为其子组件。新创建的子代属于父代，并且依赖于父代为他们提供运行所需的功能。同时，父母可以通过[能力路由]（能力路由）访问其子女暴露的能力。

Children can be created in two ways:  可以通过两种方式创建子代：

 
- Statically: The parent declares the existence of the child in its own [component declaration](#component-declarations). The child is destroyedautomatically if the child declaration is removed in an updated version ofthe parent's software. -静态：父级在其自己的[componentclaration]（component-declarations）中声明子级的存在。如果在父级软件的更新版本中删除了子级声明，则会自动销毁该子级。
- Dynamically: The parent uses [realm services][doc-realms] to add a child to a [component collection][doc-collections] that the parent declared.The parent destroys the child in a similar manner. -动态：父级使用[领域服务] [doc-realms]将子级添​​加到父级声明的[组件集合] [doc-collections]中。父级以类似方式销毁该子级。

Children remain forever dependent upon their parent; they cannot be reparented and they cannot outlive their parent. When a parent is destroyed so are all ofits children. 孩子永远永远依赖父母。他们不能成为父母，也不能超过父母。当父母被摧毁时，其所有子女也被摧毁。

The component topology represents the structure of these parent-child relationships as a [component instance tree][glossary-component-instance-tree]. 组件拓扑将这些父子关系的结构表示为[组件实例树] [词汇表组件实例树]。

TODO: Add a diagram of a component instance tree.  TODO：添加一个组件实例树图。

 
### Encapsulation {#encapsulation}  封装{encapsulation} 

The capabilities of child components cannot be directly accessed outside of the scope of their parent; they are encapsulated. 子组件的功能不能在其父组件范围之外直接访问；它们被封装。

This model resembles [composition][wiki-object-composition] in object-oriented programming languages. 该模型类似于面向对象编程语言中的[composition] [wiki-object-composition]。

 
### Realms {#realms}  领域{realms} 

A realm is a subtree of component instances formed by [hierarchical composition](#composition). Each realm is rooted by a componentinstance and includes all of that instance's children and their descendants. 领域是由[分层组成]（组成）形成的组件实例的子树。每个领域都以componentinstance为根，并包括该实例的所有子代及其子代。

Realms are important [encapsulation](#encapsulation) boundaries in the component topology. The root of each realm receives certain privileges toinfluence the behavior of components, such as: 领域是组件拓扑中重要的[封装]（封装）边界。每个领域的根都获得某些特权来影响组件的行为，例如：

 
- Declaring how capabilities flow into, out of, and within the realm.  -声明功能如何流入，流出和进入领域。
- Binding to child components to access their services.  -绑定到子组件以访问其服务。
- Creating and destroying child components.  -创建和销毁子组件。

See the [realms documentation][doc-realms] for more information.  有关更多信息，请参见[领域文档] [doc-realms]。

 
### Monikers {#monikers}  莫尼克斯{monikers} 

A moniker identifies a specific component instance in the component tree using a topological path. Monikers are collected in system logs and forpersistence. 名字对象使用拓扑路径在组件树中标识特定的组件实例。 Monikers收集在系统日志和持久性中。

See the [monikers documentation][doc-monikers] for details.  有关详细信息，请参见[monikers文档] [doc-monikers]。

 
### Capability Routing {#capability-routing}  能力路由{capability-routing} 

Components gain access to use capabilities exposed by other components through capability routing. 组件可以通过功能路由访问其他组件公开的使用功能。

TODO: Refactor existing [manifests][doc-manifests] and [capabilities][doc-capabilities] to explain the basic concepts here.Draw parallels with constructor dependency injection. Include links tocapability types. 待办事项：重构现有的[清单] [doc-manifests]和[capabilities] [doc-capabilities]在这里解释基本概念。包括功能类型的链接。

 
### Compartments {#compartments}  隔间{compartments} 

A compartment is an isolation boundary for component instances. It is an essential mechanism for preserving the[confidentiality, integrity, and availability][wiki-infosec] of components. 隔离专区是组件实例的隔离边界。这是保留组件的[机密性，完整性和可用性] [wiki-infosec]的基本机制。

Physical hardware can act as a compartment. Components running on the same physical hardware share CPU, memory, persistent storage, and peripherals.They may be vulnerable to side-channels, privilege elevation, physical attacks,and other threats that are different from those faced by components runningon different physical hardware. System security relies on making effectivedecisions about what capabilities to entrust to components. 物理硬件可以充当隔离专区。在同一物理硬件上运行的组件共享CPU，内存，持久性存储和外围设备。它们可能容易受到旁通道，特权提升，物理攻击以及其他与在不同物理硬件上运行的组件所面临的威胁不同的威胁。系统安全性取决于有效决定将哪些功能委托给组件。

A [job][glossary-job] can act as a compartment. Running a component in its own job ensures that the component's [processes][glossary-process] cannotaccess the memory or capabilities of processes belonging to other componentsin other jobs. The component framework can also kill the job to kill all ofthe component's processes (assuming the component could not create processesin other jobs). The kernel strongly enforces this isolation boundary. 一个[job] [glossary-job]可以充当隔离专区。在自己的作业中运行组件可确保该组件的[进程] [词汇表进程]无法访问其他作业中属于其他组件的进程的内存或功能。组件框架还可以杀死该作业以杀死所有组件的进程（假设该组件无法在其他作业中创建进程）。内核严格执行此隔离边界。

A [runner][doc-runners] provides a compartment for each component that it runs. The runner is responsible for protecting itself and its runnees from eachother, particularly if they share a runtime environment (such as a process)that limits the kernel's ability to enforce isolation. [runner] [doc-runners]为运行的每个组件提供了一个隔离专区。运行程序负责保护自己及其流氓彼此之间的相互保护，尤其是当它们共享一个运行时环境（例如进程）时，该运行时环境会限制内核强制执行隔离的能力。

Compartments nest: runner provided compartments reside in job compartments which themselves reside in hardware compartments. This encapsulation clarifiesthe responsibilities of each compartment: the kernel is responsible forenforcing job isolation guarantees so a runner doesn't have to. 隔层嵌套：跑步者提供的隔间位于作业隔间中，而作业隔间本身位于硬件隔间中。这种封装阐明了每个隔离专区的职责：内核负责执行工作隔离保证，因此运行程序不必这样做。

Some compartments offer weaker isolation guarantees than others. A job offers stronger guarantees than a runner so sometimes it makes sense to run multipleinstances of the same runner in different job compartments to obtain those stronger guarantees on behalf of runnees. Similarly, running each componenton separate hardware might offer the strongest guarantees but would beimpractical. There are trade-offs. 某些隔离专区的隔离保证要弱于其他隔离专项。一项工作提供的保证比奔跑者要强，因此有时在不同的工作隔间中运行同一位奔跑者的多个实例来代表流鼻涕获得那些更强的保证是有意义的。同样，在单独的硬件上运行每个组件可能提供最有力的保证，但不切实际。需要权衡。

TODO: Fill in more details when component framework APIs for assigning components to compartments have been formalized. 待办事项：将组件分配给隔离专区的组件框架API形式化后，请填写更多详细信息。

 
## Framework Capabilities  框架能力 

Components use framework capabilities to interact with their environment:  组件使用框架功能与环境交互：

 
- [Instrumentation Hooks][doc-hooks]: Diagnose and debug components.  -[Instrumentation Hooks] [doc-hooks]：诊断和调试组件。
- [Hub][doc-hub]: Examine the component topology at runtime.  -[集线] [doc-hub]：在运行时检查组件拓扑。
- [Realm][doc-realms]: Manage and bind to child components.  -[领域] [doc-realms]：管理并绑定到子组件。
- [Lifecycle][doc-lifecycle]: Listen and handle lifecycle events.  -[生命周期] [doc-lifecycle]：监听和处理生命周期事件。
- [Shutdown][doc-shutdown]: Initiate an orderly shut down of the system.  -[关闭] [doc-shutdown]：启动系统的有序关闭。
- [Work Scheduler][doc-scheduler]: Schedule deferrable work.  -[工作计划程序] [doc-scheduler]：计划可延迟的工作。

 
## Framework Extensions  框架扩展 

Components use framework extensions to integrate the component framework with software ecosystems: 组件使用框架扩展将组件框架与软件生态系统集成在一起：

 
- [Runners][doc-runners]: Integrate programming language runtimes and software frameworks. -[运行者] [doc-runners]：集成编程语言运行时和软件框架。
- [Resolvers][doc-resolvers]: Integrate software delivery systems.  -[解析器] [doc-resolvers]：集成了软件交付系统。

 
## Component Development  组件开发 

TODO: Link to docs about how to build components, diagnostic tools, and debugging features. TODO：链接到有关如何构建组件，诊断工具和调试功能的文档。

 
## Design Principles  设计原则 

 
### Accountability {#accountability}  问责制{accountability} 

System resources are finite. There's only so much memory, disk, or CPU time available on a computing device. The component framework keeps track of howresources are used by components to ensure they are being used efficientlyand that they can be reclaimed when no longer required or when they are moreurgently needed for other purposes if the system is oversubscribed. 系统资源是有限的。计算设备上只有太多的内存，磁盘或CPU时间。组件框架跟踪组件如何使用资源，以确保资源得到有效使用，并在不再需要时或在系统超额预定的情况下迫切需要将其回收时，可以对其进行回收。

Resources must be used for a reason.  必须使用资源是有原因的。

For example, every running process must belong to at least one component instance whose capabilities are currently in use, were recently of use, or willsoon be of use; any outliers are considered to be running for no reason and arepromptly stopped. 例如，每个正在运行的进程必须至少属于一个组件实例，该组件实例的功能当前正在使用，最近已使用或即将使用；任何异常值均被视为无缘无故运行，并被立即停止。

Similarly, the system may terminate processes if they exceed the resource constraints of the components that are responsible for them. 同样，如果进程超出了负责这些进程的组件的资源限制，则系统可能会终止进程。

Here are some more examples of accountability:  以下是一些问责制示例：

 
- Every component exists for a reason: Parent component instances are responsible for determining the existence of their children by destroyingchildren that are no longer of use. Parents also play a role in settingresource constraints for their children. -每个组件的存在都是有原因的：父组件实例负责通过销毁不再使用的子代来确定其子代的存在。父母在设定孩子的资源约束方面也发挥着作用。
- Every component runs for a reason: The component framework starts component instances when they have work to do, such as in response toincoming service requests from other components, and stops them when thedemand is gone (or has lesser priority than other demands that contend forthe same resources). -每个组件都运行是有原因的：组件框架在有工作要做时会启动组件实例，例如响应其他组件的传入服务请求，而在需求消失时（或优先级低于争用该组件的其他需求）则停止它们相同的资源）。
- Metrics: The component framework provides mechanisms for diagnostics tools to audit resource usage by components over time. -指标：组件框架提供了诊断工具的机制，可用于随着时间的推移审核组件的资源使用情况。

As a general rule, every resource in the system must be accounted for in some way so the system can ensure they are being used effectively. 通常，必须以某种方式说明系统中的每个资源，以便系统可以确保有效地使用它们。

 
### The Illusion of Continuity {#continuity}  连续性的幻想{continuity} 

The component framework offers mechanisms to preserve the illusion of continuity: the user should generally not be concerned about restarting theirsoftware because it will automatically resume right where they left off,even when they reboot or replace their devices. 组件框架提供了保持连续性幻觉的机制：用户通常不应该担心重新启动软件，因为即使在重新启动或更换设备时，它也会自动从中断的位置继续恢复。

The fidelity of the illusion depends on how well the following properties are preserved across restarts: 错觉的保真度取决于重新启动后以下属性的保留程度：

 
- State: Preserving the user-visible state of component instances.  -状态：保留组件实例的用户可见状态。
- Capabilities: Preserving the rights granted to component instances.  -功能：保留授予组件实例的权限。
- Structure: Preserving the relationships between collaborating component instances such that they can reestablish communication as required. -结构：保留协作组件实例之间的关系，以便它们可以根据需要重新建立通信。
- Behavior: Preserving the runtime behavior of component instances.  -行为：保留组件实例的运行时行为。

In practice, the illusion is imperfect. The system cannot guarantee faithful reproduction in the presence of software upgrades, non-determinism, bugs,faults, and external dependencies on network services. 实际上，这种幻想是不完美的。在存在软件升级，不确定性，错误，故障以及对网络服务的外部依赖性的情况下，系统无法保证真实再现。

While it might seem simpler to keep components running forever, eventually the system will run out of resources so it needs a way to balance its workingset size by stopping less essential components at a moment's notice. 虽然使组件永久运行似乎更简单，但最终系统将耗尽资源，因此它需要一种方法，通过立即停止不那么重要的组件来平衡工作集大小。

