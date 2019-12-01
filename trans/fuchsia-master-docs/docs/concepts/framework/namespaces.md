 
# Fuchsia Namespaces  紫红色命名空间 

Namespaces are the backbone of file access and service discovery in Fuchsia.  命名空间是紫红色中文件访问和服务发现的基础。

 
## Definition  定义 

A namespace is a composite hierarchy of files, directories, sockets, services, devices, and other named objects which are provided to a component by itsenvironment. 命名空间是文件，目录，套接字，服务，设备以及其他由其环境提供给组件的命名对象的复合层次结构。

Let's unpack that a little bit.  让我们打开包装。

**Objects are named**: The namespace contains _objects_ which can be enumerated and accessed by name, much like listing a directory or opening a file. **对象被命名**：名称空间包含_objects_，可以通过名称进行枚举和访问，就像列出目录或打开文件一样。

**Composite hierarchy**: The namespace is a _tree_ of objects which has been assembled by _combining_ together subtrees of objects from other namespacesinto a composite structure where each part has been assigned a path prefixby convention. **复合层次结构**：命名空间是对象的_tree_，由_combining_组合了来自其他命名空间的对象的子树到一个复合结构中，其中每个部分均已按约定分配了路径前缀。

**Namespace per component**: Every component receives its own namespace tailored to meet its own needs.  It can also publish objects of its ownto be included in other namespaces. **每个组件的名称空间**：每个组件都具有适合其自身需求的量身定制的命名空间。它还可以发布自己的对象以包含在其他名称空间中。

**Constructed by the environment**: The environment which instantiates a component is responsible for constructing an appropriate namespace for thatcomponent within that scope. **由环境构造**：实例化组件的环境负责在该范围内为该组件构造适当的名称空间。

Namespaces can also be created and used independently from components although this document focuses on typical component-bound usage. 命名空间也可以独立于组件创建和使用，尽管本文档重点介绍典型的组件绑定用法。

 
## Namespaces in Action  实际使用的命名空间 

You have probably already spent some time exploring a Fuchsia namespace; they are everywhere.  If you type `ls /` at a command-line shell promptyou will see a list of some of the objects which are accessible from theshell's namespace. 您可能已经花了一些时间探索Fuchsia命名空间。他们无处不在。如果在命令行shell提示符下输入`ls /`，您将看到一些可从shell名称空间访问的对象的列表。

Unlike other operating systems, Fuchsia does not have a "root filesystem". As described earlier, namespaces are defined per-component rather thanglobally or per-process. 与其他操作系统不同，紫红色没有“根文件系统”。如前所述，名称空间是按组件而不是全局或进程定义的。

This has some interesting implications:  这具有一些有趣的含义：

 
- There is no global "root" namespace.  -没有全局“根”名称空间。
- There is no concept of "running in a chroot-ed environment" because every component [effectively has its own private "root"](/docs/concepts/storage/dotdot.md). -没有“在chroot环境中运行”的概念，因为每个组件[有效地都有自己的私有“根”]（/ docs / concepts / storage / dotdot.md）。
- Components receive namespaces which are tailored to their specific needs.  -组件接收根据其特定需求量身定制的名称空间。
- Object paths may not be meaningful across namespace boundaries.  -跨越命名空间边界的对象路径可能没有意义。
- A process may have access to several distinct namespaces at once.  -一个进程可以一次访问几个不同的名称空间。
- The mechanisms used to control access to files can also be used to control access to services and other named objects on a per-component basis. -用于控制对文件的访问的机制也可以用于按组件控制对服务和其他命名对象的访问。

 
## Objects  对象 

The items within a namespace are called objects.  They come in various flavors, including: 命名空间中的项目称为对象。它们有多种口味，包括：

 
- Files: objects which contain binary data  -文件：包含二进制数据的对象
- Directories: objects which contain other objects  -目录：包含其他对象的对象
- Sockets: objects which establish connections when opened, like named pipes  -套接字：打开时建立连接的对象，例如命名管道
- Services: objects which provide FIDL services when opened  -服务：打开时提供FIDL服务的对象
- Devices: objects which provide access to hardware resources  -设备：提供对硬件资源访问的对象

 
### Accessing Objects  访问对象 

To access an object within a namespace, you must already have another object in your possession.  A component typically receives channel handles forobjects in the scope of its namespace during[Namespace Transfer](#namespace-transfer). 要访问命名空间中的对象，您必须已经拥有另一个对象。组件通常在[命名空间转移]（namespace-transfer）期间在其命名空间范围内接收对象的通道句柄。

You can also create new objects out of thin air by implementing the appropriate FIDL protocols. 您还可以通过实施适当的FIDL协议来凭空创建新对象。

Given an object's channel, you can open a channel for one of its sub-objects by sending it a FIDL message which includes an object relative path expressionwhich identifies the desired sub-object.  This is much like opening filesin a directory. 给定对象的通道，您可以通过向其发送FIDL消息为其子对象之一打开通道，该消息包括对象相对路径表达式，该表达式标识所需的子对象。这很像在目录中打开文件。

Notice that you can only access objects which are reachable from the ones you already have access to.  There is no ambient authority. 请注意，您只能访问那些已经可以访问的对象可以访问的对象。没有环境权限。

We will now define how object names and paths are constructed.  现在，我们将定义对象名称和路径的构造方式。

 
### Object Names  对象名称 

An object name is a locally unique label by which an object can be located within a container (such as a directory).  Note that the name is a propertyof the container's table of sub-objects rather than a property of the objectitself. 对象名称是一个本地唯一的标签，通过它可以在容器（例如目录）中定位对象。请注意，该名称是容器的子对象表的属性，而不是对象本身的属性。

For example, `cat` designates a furry object located within some unspecified recipient of an `Open()` request. 例如，“ cat”指定一个毛茸茸的对象，该对象位于“ Open（）”请求的某些未指定收件人内。

Objects are fundamentally nameless but they may be called many names by others.  对象从根本上来说是无名的，但是其他人可能将它们称为许多名称。

Object names are represented as binary octet strings (arbitrary sequences of bytes) subject to the following constraints: 对象名称表示为二进制八位字节字符串（字节的任意序列），但受以下约束：

 
- Minimum length of 1 byte.  -最小长度为1个字节。
- Maximum length of 255 bytes.  -最大长度为255个字节。
- Does not contain NULs (zero-valued bytes).  -不包含NUL（零值字节）。
- Does not contain `/`.  -不包含`/`。
- Does not equal `.` or `..`.  -不等于`.`或`..`。
- Always compared using byte-for-byte equality (implies case-sensitive).  -始终使用逐字节相等进行比较（意味着区分大小写）。

Object names are valid arguments to a container's `Open()` method. See [FIDL Protocols](#fidl-protocols). 对象名称是容器的Open（）方法的有效参数。请参阅[FIDL协议]（fidl-protocols）。

It is intended that object names be encoded and interpreted as human-readable sequences of UTF-8 graphic characters, however this property is not enforcedby the namespace itself. 目的是将对象名称编码并解释为人类可读的UTF-8图形字符序列，但是名称空间本身不强制执行此属性。

Consequently clients are responsible for deciding how to present names which contain invalid, undisplayable, or ambiguous character sequences tothe user. 因此，客户负责决定如何向用户呈现包含无效，不可显示或模糊字符序列的名称。

_TODO(jeffbrown): Document a specific strategy for how to present names._  _TODO（jeffbrown）：记录如何显示名称的特定策略。_

 
### Object Relative Path Expressions  对象相对路径表达式 

An object relative path expression is an object name or a `/`-delimited sequence of object names designating a sequence of nested objects to betraversed in order to locate an object within a container (such as adirectory). 对象相对路径表达式是对象名称或对象名称的“ /”定界序列，该序列指定要遍历的嵌套对象序列以便在容器（例如目录）中定位对象。

For example, `house/box/cat` designates a furry object located within its containing object called `box` located within its containing object called`house` located within some unspecified recipient of an `Open()` request. 例如，“ house / box / cat”表示位于其包含对象“ box”内的毛茸茸对象，位于其包含“ house”的包含对象内，该对象位于“ Open（）”请求的某些未指定接收者内。

An object relative path expression always traverses deeper into the namespace. Notably, the namespace does not directly support upwards traversal out ofcontainers (e.g. via `..`) but this feature may be partially emulated byclients (see below). 对象相对路径表达式始终遍历名称空间。值得注意的是，名称空间不直接支持容器外的向上遍历（例如，通过`..`），但是客户端可以部分模拟此功能（请参见下文）。

Object relative path expressions have the following additional constraints:  对象相对路径表达式具有以下附加约束：

 
- Minimum length of 1 byte.  -最小长度为1个字节。
- Maximum length of 4095 bytes.  -最大长度为4095字节。
- Does not begin or end with `/`.  -不以`/`开头或结尾。
- All segments are valid object names.  -所有段都是有效的对象名称。
- Always compared using byte-for-byte equality (implies case-sensitive).  -始终使用逐字节相等进行比较（意味着区分大小写）。

Object relative path expressions are valid arguments to a container's `Open()` method.  See [FIDL Protocols](#fidl-protocols). 对象相对路径表达式是容器的Open（）方法的有效参数。请参阅[FIDL协议]（fidl-protocols）。

 
### Client Interpreted Path Expressions  客户端解释的路径表达式 

A client interpreted path expression is a generalization of object relative path expressions which includes optional features which may be emulatedby client code to enhance compatibility with programs which expect a rootedfile-like interface. 客户端解释的路径表达式是对象相对路径表达式的概括，其中包括可选功能，这些可选功能可以由客户端代码进行仿真，以增强与期望类似于rootedfile的接口的程序的兼容性。

Technically these features are beyond the scope of the Fuchsia namespace protocol itself but they are often used so we describe them here. 从技术上讲，这些功能超出了Fuchsia名称空间协议本身的范围，但经常使用它们，因此我们在此处进行描述。

 
- A client may designate one of its namespaces to function as its "root". This namespace is denoted `/`. -客户端可以指定其名称空间之一作为其“根”。该名称空间表示为“ /”。
- A client may construct paths relative to its designated root namespace by prepending a single `/`. -客户端可以通过在单个“ /”之前添加相对于其指定的根名称空间的路径。
- A client may construct paths which traverse upwards from containers using `..` path segments by folding segments together (assuming the container'spath is known) through a process known as client-side "canonicalization". -客户端可以使用称为“ ..”的路径段，通过将段折叠在一起（假设已知容器的路径），通过称为客户端“规范化”的过程来构造从容器向上遍历的路径。
- These features may be combined together.  -这些功能可以组合在一起。

For example, `/places/house/box/../sofa/cat` designates a furry object located at `places/house/sofa/cat` within some client designated "root"container. 例如，“ / places / house / box /../ sofa / cat”指定位于某些指定为“根”容器的客户端中的“ places / house / sofa / cat”中的毛茸茸的对象。

Client interpreted path expressions that contain these optional features are not valid arguments to a container's `Open()` method; they must betranslated by the client prior to communicating with the namespace.See [FIDL Protocols](#fidl-protocols). 包含这些可选功能的客户端解释路径表达式不是容器的Open（）方法的有效参数；在与名称空间通信之前，它们必须由客户端进行翻译。请参见[FIDL协议]（fidl-protocols）。

For example, `fdio` implements client-side interpretation of `..` paths in file manipulation APIs such as `open()`, `stat()`, `unlink()`, etc. 例如，fdio在文件操作API中实现客户端对..路径的解释，例如open（），stat（），unlink（）等。

 
## Namespace Transfer  命名空间转移 

When a component is instantiated in an environment (e.g. its process is started), it receives a table which maps one or more namespace path prefixesto object handles. 在环境中实例化组件时（例如，启动其过程），它会收到一个表，该表将一个或多个名称空间路径前缀映射到对象句柄。

The path prefixes in the table encode the intended significance of their associated objects by convention.  For example, the `pkg` prefix shouldbe associated with a directory object which contains the component's ownbinaries and assets. 表中的路径前缀按照约定编码了其关联对象的预期重要性。例如，`pkg`前缀应与包含组件自己的二进制文件和资产的目录对象相关联。

More on this in the next section.  下一节将对此进行更多介绍。

 
## Namespace Conventions  命名空间约定 

This section describes the conventional layout of namespaces for typical components running on Fuchsia. 本节描述了在Fuchsia上运行的典型组件的名称空间的常规布局。

The precise contents and organization of a component's namespace varies greatly depending on the component's role, type, identity, scope,relation to other components, and rights. See [Sandboxing](sandboxing.md) forinformation about how namespaces are used to create sandboxes for components. 组件名称空间的确切内容和组织会根据组件的角色，类型，标识，范围，与其他组件的关系以及权限而有很大不同。有关如何使用名称空间为组件创建沙箱的信息，请参见[Sandboxing]（sandboxing.md）。

_For more information about the namespace your component can expect to receive from its environment, please consult the documentation related tothe component type you are implementing._ _有关组件期望从其环境中接收到的名称空间的更多信息，请查阅与您正在实现的组件类型相关的文档。_

 
### Typical Objects  典型对象 

There are some typical objects which a component namespace might contain:  组件名称空间可能包含一些典型的对象：

 
- Read-only executables and assets from the component's package.  -组件包中的只读可执行文件和资产。
- Private local persistent storage.  -私有本地持久存储。
- Private temporary storage.  -私人临时存储。
- Services offered to the component by the system, the component framework, or by the client which started it. -由系统，组件框架或启动它的客户端提供给组件的服务。
- Device nodes (for drivers and privileged components).  -设备节点（用于驱动程序和特权组件）。
- Configuration information.  -配置信息。

 
### Typical Directory Structure  典型目录结构 

 
- `pkg/`: the contents of the current program's package  -`pkg /`：当前程序包的内容
  - `bin/`: executable binaries within the package  -`bin /`：包中的可执行二进制文件
  - `lib/`: shared libraries within the package  -`lib /`：包中的共享库
  - `data/`: data, such as assets, within the package  -`data /`：数据包中的数据，例如资产
- `data/`: local persistent storage (read-write, private to the package)  -`data /`：本地持久性存储（读写，对程序包私有）
- `tmp/`: temporary storage (read-write, private to the package)  -`tmp /`：临时存储（读写，对程序包私有）
- `svc/`: services offered to the component  -`svc /`：提供给组件的服务
  - `fuchsia.process.Launcher`: launch processes  -`fuchsia.process.Launcher`：启动过程
  - `fuchsia.logger.Log`: log messages  -`fuchsia.logger.Log`：记录消息
  - `vendor.topic.Interface`: service defined by a _vendor_  -`vendor.topic.Interface`：由_vendor_定义的服务
- `dev/`: device tree (relevant portions visible to privileged components as needed)  -`dev /`：设备树（相关部分根据需要对特权组件可见）
  - `class/`, ...  -`class /`，...
- `hub/`: introspect the system, see [Hub](hub.md) (privileged components only)  -`hub /`：对系统进行内部检查，请参见[Hub]（hub.md）（仅限特权组件）
- `config/`: configuration data for the component  -`config /`：组件的配置数据

 
## Namespace Participants  命名空间参与者 

Here is some more information about a few abstractions which interact with and support the Fuchsia namespace protocol. 这是有关与Fuchsia名称空间协议交互并支持Fuchsia名称空间协议的一些抽象的更多信息。

 
### Filesystems  文件系统 

Filesystems make files available in namespaces.  文件系统使文件在名称空间中可用。

A filesystem is simply a component which publishes file-like objects which are included in someone else's namespace. 文件系统只是一个组件，它发布包含在其他人的命名空间中的类似文件的对象。

 
### Services  服务 

Services live in namespaces.  服务位于名称空间中。

A service is a well-known object which provides an implementation of a FIDL protocol which can be discovered using the namespace. 服务是众所周知的对象，它提供可以使用名称空间发现的FIDL协议的实现。

A service name corresponds to a path within the `svc` branch of the namespace from which a component can access an implementation of the service. 服务名称对应于名称空间的svc分支内的路径，组件可以从该路径访问服务的实现。

For example, the name of the default Fuchsia logging service is `fuchsia.logger.Log` and its location in the namespace is`svc/fuchsia.logger.Log`. 例如，默认的Fuchsia日志记录服务的名称为`fuchsia.logger.Log`，其在命名空间中的位置为`svc / fuchsia.logger.Log`。

 
### Components  组件 

Components consume and extend namespaces.  组件使用和扩展名称空间。

A component is an executable program object which has been instantiated within some environment and given a namespace. 组件是一个可执行程序对象，已在某些环境中实例化并指定了名称空间。

A component participates in the Fuchsia namespace in two ways:  组件以两种方式参与Fuchsia命名空间：

 
1. It can use objects from the namespace which it received from its environment, notably to access its own package contents and incoming services. 1.它可以使用从其环境接收到的命名空间中的对象，特别是访问其自己的包内容和传入服务。

 
2. It can publish objects through its environment in the form of a namespace, parts of which its environment may subsequently make available to othercomponents upon request.  This is how services are implemented bycomponents. 2.它可以通过其环境以名称空间的形式发布对象，其环境的某些部分随后可以应要求提供给其他组件。这就是组件实现服务的方式。

 
### Environments  环境环境 

Environments construct namespaces.  环境构造名称空间。

An environment is a container of components.  Each environment is responsible for _constructing_ the namespace which its components will receive. 环境是组件的容器。每个环境负责_constructing_其组件将接收的名称空间。

The environment decides what objects a component may access and how the component's request for services by name will be bound to specificimplementations. 环境决定组件可以访问哪些对象，以及如何按名称将组件的服务请求绑定到特定的实现。

 
### Configuration  组态 

Components may have different kinds of configuration data exposed to them depending on the features listed in their [ComponentManifest](/docs/concepts/storage/component_manifest.md) which are exposed as files inthe /config namespace entry. These are defined by the feature set of thecomponent. 组件可能会根据它们的[ComponentManifest]（/ docs / concepts / storage / component_manifest.md）中列出的功能向其公开不同类型的配置数据，这些功能作为文件在/ config命名空间条目中公开。这些由组件的功能集定义。

 
## FIDL Protocols  FIDL协议 

