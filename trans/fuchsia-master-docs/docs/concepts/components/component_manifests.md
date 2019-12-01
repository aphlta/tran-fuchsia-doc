Note: This document describes manifests for the new Component Manager. If your component launches with [appmgr](/docs/glossary.md#appmgr), indicatedfor instance by your manifest file ending in a `.cmx` extension, then pleaserefer to [legacy documentation](/docs/concepts/storage/component_manifest.md). 注意：本文档描述了新组件管理器的清单。如果您的组件以[appmgr]（/ docs / glossary.mdappmgr）启动，例如以清单文件结尾为.cmx扩展名指示，则请参考[旧版文档]（/ docs / concepts / storage / component_manifest.md ）。

 
# Component manifests {#component-manifests}  组件清单{component-manifests} 

A [component manifest](#component-manifest) is a file that defines a component by encoding a [component declaration](#component-declaration). This documentgives an overview of the concepts used by component declarations, and presentsthe syntax for writing [component manifest source](#component-manifest-source).Component declarations contain: [component manifest]（component-manifest）是通过对[componentclaration]（component-declaration）进行编码来定义组件的文件。本文档概述了组件声明所使用的概念，并介绍了编写[component manifest source]（component-manifest-source）的语法。组件声明包含：

 
- Information about [how to run the component](#runtime).  -有关[如何运行组件]（运行时）的信息。
- The realm's [child component instances][children] and [component collections][collections]. -领域的[子组件实例] [子代]和[组件集合] [集合]。
- [Routing rules](#capability-routing) that describe how capabilities are used, exposed, and offered between components. -[路由规则]（功能路由），描述如何在组件之间使用，公开和提供功能。
- [Freeform data ("facets")](#facet-metadata) which is ignored by the component framework but can be interpreted by third parties. -[自由格式数据（“构面”）]（构面元数据），组件框架可以忽略，但可以由第三方解释。

 
## Manifests and declarations {#manifests-and-declarations}  清单和声明{manifestsand-declarations} 

This section explains the distinction between component manifests, component manifest sources, and component declarations. 本节说明组件清单，组件清单源和组件声明之间的区别。

 
### Component manifest {#component-manifest}  组件清单{component-manifest} 

A *component manifest* is a file that encodes a [component declaration](#component-declaration), usually distributed as part ofa [package](/docs/development/sdk/documentation/packages.md). The binary formatis a JSON file mapping one-to-one onto the component declaration, typicallyending in a `.cm` extension. *组件清单*是对[组件声明]（component-declaration）进行编码的文件，通常作为[package]（/ docs / development / sdk / documentation / packages.md）的一部分分发。二进制格式是一个JSON文件，该文件一对一映射到组件声明，通常以`.cm`扩展名结尾。

A [fuchsia-pkg URL](/docs/concepts/storage/package_url.md) with a component manifest fragment identifies a component in a package. 具有组件清单片段的[fuchsia-pkg URL]（/ docs / concepts / storage / package_url.md）标识包中的组件。

 
### Component manifest source {#component-manifest-source}  组件清单来源{component-manifest-source} 

A *component manifest source* is a file that encodes part of a component manifest. Component manifest sources are written in *CML* (*component manifestlanguage*), which is the developer-facing source format for component manifests.CML files are JSON5 files that end with a `.cml` extension. Descriptions andexamples of the CML syntax are contained in this document: see[Syntax](#syntax). *组件清单源*是对部分组件清单进行编码的文件。组件清单资源以* CML *（* component manifestlanguage *）编写，这是面向组件开发人员的面向开发人员的源格式。CML文件是JSON5文件，扩展名为`.cml`。 CML语法的描述和示例包含在本文档中：请参见[语法]（语法）。

Component manifest sources are compiled to [component manifests](#component-manifest) by the [`cmc`](/src/sys/cmc) tool. 组件清单源通过[`cmc`]（/ src / sys / cmc）工具编译为[组件清单]（component-manifest）。

 
### Component declaration {#component-declaration}  组件声明{component-declaration} 

The [`ComponentDecl`](/sdk/fidl/fuchsia.sys2/decls/component_decl.fidl) FIDL table is a *component declaration*. Component declarations are used by thecomponent framework APIs to represent components and may be provided tocomponents at runtime. [`ComponentDecl`]（/ sdk / fidl / fuchsia.sys2 / decls / component_decl.fidl）FIDL表是一个*组件声明*。组件声明由组件框架API使用以表示组件，并且可以在运行时提供给组件。

 
## Concepts  概念 

 
### Runtime  运行 

The [`program`](#program) section of a component manifest declares how the component is run. For a component containing an ELF binary, this sectionconsists of a path to a binary in the package and, optionally, a list ofarguments. For a component that does not contain an executable, this section isomitted. 组件清单的[`program`]（program）部分声明了组件的运行方式。对于包含ELF二进制文件的组件，此部分包括程序包中二进制文件的路径以及（可选）参数列表。对于不包含可执行文件的组件，此部分将被省略。

See also: [ELF Runner](elf_runner.md)  另请参见：[ELF Runner]（elf_runner.md）

 
### Capability routing {#capability-routing}  能力路由{capability-routing} 

Component manifests provide a syntax for routing capabilities between components. For a detailed walkthrough about what happens during capabilityrouting, see [_Life of a service open_](life_of_a_service_open.md) 组件清单为组件之间的路由功能提供了一种语法。有关功能路由过程中发生的情况的详细演练，请参阅[_服务生命周期_]（life_of_a_service_open.md）

 
#### Capability types {#capability-types}  能力类型{capability-types} 

The following capabilities can be routed:  可以路由以下功能：

 
- `service`: A filesystem service node that can be used to open a channel to a service provider. -`service`：文件系统服务节点，可用于打开服务提供商的通道。
- `directory`: A filesystem directory.  -目录：文件系统目录。
- `storage`: A filesystem directory that is isolated to the component using it.  -`storage`：一个文件系统目录，使用它隔离到组件。

 
#### Routing terminology {#routing-terminology}  路由术语{routing-terminology} 

Component manifests declare how capabilities are routed between components. The language of capability routing consists of the following three keywords: 组件清单声明了如何在组件之间路由功能。能力路由的语言由以下三个关键字组成：

 
- `use`: When a component `uses` a capability, the capability is installed in the component's namespace. A component may `use` any capability that has been`offered` to it. -`use`：当组件使用功能时，该功能将安装在组件的名称空间中。组件可以“使用”已提供的任何功能。
- `offer`: A component may `offer` a capability to a *target*, which is either a [child][children] or [collection][collections]. When acapability is offered to a child, the child instance may `use` the capabilityor `offer` it to one of its own targets. Likewise, when a capability isoffered to a collection, any instance in the collection may `use` thecapability or `offer` it. -`offer`：组件可以向* target *提供一个功能，该目标可以是[child] [children]或[collection] [collection]。当向孩子提供能力时，孩子实例可以“使用”能力或“提供”其自己的目标之一。同样，当向集合提供功能时，集合中的任何实例都可以“使用”功能或“提供”该功能。
- `expose`: When a component `exposes` a capability to its [containing realm][realm-definitions], the parent may `offer` the capability to one of its otherchildren. A component may `expose` any capability that it provides, or thatone of its children exposes. -`expose`：当组件`向其[包含领域] [realm-definitions]公开其功能时，父级可以向其另一子级中的一个提供该功能。组件可以“公开”它提供的任何功能，或者子组件可以公开的任何功能。

When you use these keywords together, they express how a capability is routed from a component instance's [outgoingdirectory](/docs/concepts/system/abi/system.md#outgoing-directory) to anothercomponent instance's namespace: 当您一起使用这些关键字时，它们表示如何将功能从组件实例的[outgoingdirectory]（/ docs / concepts / system / abi / system.mdoutgoing-directory）路由到另一个组件实例的名称空间：

 
- `use` describes the capabilities that populate a component instance's namespace. -`use`描述填充组件实例名称空间的功能。
- `expose` and `offer` describe how capabilities are passed between component instances. Aside from their directionality, there is one significantdifference between `offer` and `expose`. While a component may `use` acapability that was `offered` to it, a component is not allowed to `use` acapability that was `exposed` to it by its child. This restriction exists toprevent dependency cycles between parent and child. -“暴露”和“提供”描述了如何在组件实例之间传递功能。除了它们的方向性外，“要约”和“公开”之间还有一个显着差异。虽然组件可以“使用”提供给它的功能，但是不允许组件“使用”其子项“暴露”给它的功能。存在此限制是为了防止父子之间的依赖周期。

 
#### Framework services {#framework-services}  框架服务{framework-services} 

A *framework service* is a service provided by the component framework. Because the component framework itself is the provider of the service, any component may`use` it without an explicit `offer`. Fuchsia supports the following frameworkservices: 框架服务是组件框架提供的服务。因为组件框架本身是服务的提供者，所以任何组件都可以“使用”它而无需明确的“报价”。紫红色支持以下框架服务：

 
- [`fuchsia.sys2.Realm`](/sdk/fidl/fuchsia.sys2/realm.fidl): Allows a component to manage and bind to its children. Scoped to the component's realm. -[`fuchsia.sys2.Realm`]（/ sdk / fidl / fuchsia.sys2 / realm.fidl）：允许组件管理并绑定到其子级。范围涉及组件的领域。

 
#### Framework directories {#framework-directories}  框架目录{framework-directories} 

A *framework directory* is a directory provided by the component framework. Because the component framework itself is the provider of the directory, anycomponent may `use` it without an explicit `offer`. Fuchsia supports thefollowing framework directories: 框架目录是组件框架提供的目录。因为组件框架本身是目录的提供者，所以任何组件都可以“使用”它而无需显式的“报价”。紫红色支持以下框架目录：

 
- [`/hub`](../../glossary.md#hub): Allows a component to perform runtime introspection of itself and its children. -[`/hub`](../../glossary.mdhub）：允许组件对其自身及其子级执行运行时自省。

 
#### Capability paths {#capability-paths}  能力路径{capability-paths} 

Service and directory capabilities are identified by paths.  A path consists of a sequence of path components, starting with and separated by `/`, where eachpath component consists one or more non-`/` characters. 服务和目录功能由路径标识。路径由一系列路径组成，以“ /”开头并以“ /”分隔，其中每个路径组成由一个或多个非“ /”字符组成。

A path may either be a *source path* or *target path*, whose meaning depends on context: 路径可以是“源路径”或“目标路径”，其含义取决于上下文：

 
- A *source path* is either a path in the component's outgoing directory (for `offer` or `expose` from `self`), or the path by which the capability wasoffered or exposed to this component. -“源路径”可以是组件的传出目录中的路径（来自“ self”的“要约”或“暴露”），也可以是向该组件提供或公开功能的路径。
- A *target path* is either a path in the component's namespace (for `use`), or the path by which the capability is being `offered` or `exposed` to anothercomponent. -目标路径可以是组件名称空间中的路径（用于“使用”），也可以是将功能“提供”或“暴露”给另一个组件的路径。

 
#### Directory Rights {#directory-rights}  目录权限{directory-rights} 

Directory rights define how a directory may be accessed in the component framework. You must specify directory rights on `use` declarations and on `expose` and `offer`declarations from `self`. On `expose` and `offer` declarations not from `self`, they are optional. 目录权限定义了如何在组件框架中访问目录。您必须在`use`声明以及`self`的`expose`和`offer`声明中指定目录权限。在`expose`和`offer`声明不是来自`self`时，它们是可选的。

A *rights* field can be defined by the combination of any of the following rights tokens:  可以通过以下任何权限标记的组合来定义* rights *字段：

```
"rights": ["connect", "enumerate", "read_bytes", "write_bytes", "execute_bytes",
            "update_attributes", "get_attributes", "traverse", "modify_directory"]
```
 

Note: See [`fuchsia.io2.Rights`](/zircon/system/fidl/fuchsia-io2/rights-abilities.fidl) for the equivalent FIDL definitions. 注意：有关等效的FIDL定义，请参见[`fuchsia.io2.Rights`]（/​​ zircon / system / fidl / fuchsia-io2 / rights-abilities.fidl）。

However *rights aliases* should be prefered where possible for clarity.  但是，为了清晰起见，应优先选择“权利别名”。

```
"rights": ["r*", "w*", "x*", "rw*", "rx*"]
```
 

Note: Except in special circumstances you will almost always want either `["r*"]` or `["rw*"]`.  注意：除非在特殊情况下，否则您几乎总是需要`[“ r *”]`或`[“ rw *”]]。

Note: Only one alias can be provided to a rights field and it must not conflict with any longform rights. 注意：只能向权限字段提供一个别名，并且该别名不能与任何长格式权限冲突。

Right aliases are simply expanded into their longform counterparts:  正确的别名可以简单地扩展为对应的长格式：

```
"r*" -> ["connect", "enumerate", "traverse", "read_bytes", "get_attributes"]
"w*" -> ["connect", "enumerate", "traverse", "write_bytes", "update_attributes", "modify_directory"]
"x*" -> ["connect", "enumerate", "traverse", "execute_bytes"]
```
 

Note: Merged aliases line `rw*` are simply `r*` and `w*` merged without duplicates.  注意：合并别名行“ rw *”只是“ r *”和“ w *”合并而没有重复。

This example shows usage of a directory use declaration annotated with rights:  此示例显示了带有权限注释的目录使用声明的用法：

```
"use": [
  {
    "directory": "/test",
    "from": "realm",
    "rights": ["rw*", "admin"],
  },
],
```
 

 
#### Storage capabilities {#storage-capabilities}  存储功能{storage-capabilities} 

Storage capabilities are not directly provided from a component instance's [outgoing directory](/docs/concepts/system/abi/system.md#outgoing-directory), butare created from preexisting directory capabilities that are declared in[`storage`](#storage) in a component manifest. This declaration describes thesource for a directory capability and can then be listed as a source foroffering storage capabilities. 存储功能不是直接从组件实例的[输出目录]（/ docs / concepts / system / abi / system.mdoutgoing-directory）中提供的，而是由在[`storage`]（storage）中声明的现有目录功能创建的组件清单。该声明描述了目录功能的来源，然后可以被列为提供存储功能的来源。

Storage capabilities cannot be [exposed](#expose).  存储功能不能[公开]（公开）。

 
#### Storage types {#storage-types}  存储类型{storage-types} 

Storage capabilities are identified by types. Valid storage types are `data`, `cache`, and `meta`, each having different semantics: 存储功能按类型标识。有效的存储类型为“数据”，“缓存”和“元”，每种都有不同的语义：

 
- `data`: A mutable directory the component may store its state in. This directory is guaranteed to be unique and non-overlapping withdirectories provided to other components. -`data`：组件可以在其中存储其状态的可变目录。保证该目录是唯一的，并且不重叠提供给其他组件的目录。
- `cache`: Identical to the `data` storage type, but the framework may delete items from this directory to reclaim space. -`cache`：与`data`存储类型相同，但是框架可以从该目录中删除项目以回收空间。
- `meta`: A directory where the framework can store metadata for the component instance. Features such as persistent collections must use this capability asthey require component manager to store data on the component's behalf. Thecomponent cannot directly access this directory. -`meta'：框架可以在其中存储组件实例元数据的目录。诸如持久性集合之类的功能必须使用此功能，因为它们要求组件管理器代表组件存储数据。该组件无法直接访问此目录。

 
#### Examples  例子 

For an example of how these keywords interact, consider the following component instance tree: 有关这些关键字如何交互的示例，请考虑以下组件实例树：

![Capability routing example](capability_routing_example.png)  ！[功能路由示例]（capability_routing_example.png）

In this example, the `echo` component instance provides an `/svc/echo` service in its outgoing directory. This service is routed to the `echo_tool` componentinstance, which uses it. It is necessary for each component instance in therouting path to propagate `/svc/echo` to the next component instance. 在这个例子中，“ echo”组件实例在其传出目录中提供了“ / svc / echo”服务。该服务被路由到使用它的`echo_tool` componentinstance。路由路径中的每个组件实例都必须将“ / svc / echo”传播到下一个组件实例。

The routing sequence is:  路由顺序为：

 
- `echo` hosts the `/svc/echo` service in its outgoing directory. Also, it exposes `/svc/echo` from `self` so the service is visible to its parent,`services`. -`echo`在其传出目录中托管`/ svc / echo`服务。同样，它从`self`中公开`/ svc / echo`，因此服务对其父服务可见。
- `services` exposes `/svc/echo` from its child `echo` to its parent, `shell`.  -`services`将`/ svc / echo`从其子`echo`暴露给其父级`shell`。
- `system` offers `/svc/echo` from its child `services` to its other child `tools`. -`system`从其子`services'到其其他子`tools'提供`/ svc / echo`。
- `tools` offers `/svc/echo` from `realm` (i.e., its parent) to its child `echo_tool`. -`tools`提供`/ svc / echo`从`realm`（即其父级）到其子级`echo_tool`。
- `echo_tool` uses `/svc/echo`. When `echo_tool` runs, it will find `/svc/echo` in its namespace. -`echo_tool`使用`/ svc / echo`。当`echo_tool`运行时，它将在其命名空间中找到`/ svc / echo`。

A working example of capability routing can be found at [//examples/components/routing](/examples/components/routing). 功能路由的工作示例可以在[// examples / components / routing]（/ examples / components / routing）中找到。

 
### Facet metadata {#facet-metadata}  构面元数据{facet-metadata} 

*Facets* are metadata that is ignored by the component framework itself, but may be interpreted by interested components. For example, a module component mightcontain [module facets](/docs/concepts/modular/module_facet.md) declaring intentsthe module subscribes to. * Facets *是元数据，其本身被组件框架忽略，但可能由感兴趣的组件解释。例如，一个模块组件可能包含[module facets]（/ docs / concepts / modular / module_facet.md）声明该模块订阅的意图。

 
## Syntax  句法 

This section explains the syntax for each section of the component manifest, in CML format. For the full schema, see[cml_schema.json](/garnet/lib/rust/cm_json/cml_schema.json). 本节以CML格式说明组件清单的每个部分的语法。有关完整架构，请参见[cml_schema.json]（/ garnet / lib / rust / cm_json / cml_schema.json）。

 
### References {#references}  参考文献{references} 

A *reference* is a string of the form `#<reference-name>`, where `<reference-name>` is a string of one or more of the following characters:`a-z`, `0-9`, `_`, `.`, `-`. * reference *是格式为<< reference-name>`的字符串，其中`<reference-name>`是以下一个或多个字符的字符串：`az`，`0-9`，`_ `，`.`，`-`。

A reference may refer to:  参考可以指：

 
- A [static child instance][static-children] whose name is `<reference-name>`. -一个名为“ <引用名称>”的[静态子实例] [static-children]。
- A [collection][collections] whose name is `<reference-name>`.  -一个名称为“ <引用名称>”的[集合] [集合]。
- A [storage declaration](#storage) whose name is `<reference-name>`.  -一个名为“ <引用名称>”的[存储声明]（存储）。

[children]: ./realms.md#child-component-instances [collections]: ./realms.md#component-collections[realm-definitions]: ./realms.md#definitions[static-children]: ./realms.md#static-children [children]：./realms.mdchild-component-instances [collections]：./realms.mdcomponent-collections[realm-definitions]：./realms.mddefinitions[static-children]：./realms.mdstatic-children

 
### program  程序 

If the component contains executable code, the content of the `program` section is determined by the runner the component uses. Some components don't haveexecutable code; the declarations for those components lack a `program` section. 如果组件包含可执行代码，则“ program”部分的内容由组件使用的运行程序确定。有些组件没有可执行代码；这些组件的声明缺少“程序”部分。

 
#### ELF runners  ELF赛跑者 

If the component uses the ELF runner, `program` is an object with the following properties: 如果组件使用ELF运行器，则“ program”是具有以下属性的对象：

 
- `binary`: Package-relative path to the executable binary  -`binary`：可执行二进制文件的软件包相对路径
- `args` *(optional)*: List of arguments  -`args` *（可选）*：参数列表

```
"program": {
    "binary": "bin/hippo",
    "args": [ "Hello", "hippos!" ],
},
```
 

See also: [ELF Runner](elf_runner.md)  另请参见：[ELF Runner]（elf_runner.md）

 
### children  孩子们 

The `children` section declares child component instances as described in [Child component instances][children] “ children”部分声明了子组件实例，如[子组件实例] [children]中所述

`children` is an array of objects with the following properties:  children是具有以下属性的对象数组：

 
- `name`: The name of the child component instance, which is a string of one or more of the following characters: `a-z`, `0-9`, `_`, `.`, `-`. -`name`：子组件实例的名称，它是一个或多个以下字符的字符串：`a-z`，`0-9`，`_`，`.`，`-`。
- `url`: The component URL for the child component instance.  -`url`：子组件实例的组件URL。
- `startup` *(optional)*: The component instance's startup mode.  -`startup` *（可选）*：组件实例的启动模式。
    - `lazy` *(default)*: Start the component instance only if another component instance binds to it. -`lazy` *（默认）*：仅当另一个组件实例绑定到该实例时，才启动该组件实例。
    - `eager`: Start the component instance as soon as its parent starts.  -`eager`：组件实例的父实例启动后立即启动。

Example:  例：

```
"children": [
    {
        "name": "logger",
        "url": "fuchsia-pkg://fuchsia.com/logger#logger.cm",
    },
    {
        "name": "pkg_cache",
        "url": "fuchsia-pkg://fuchsia.com/pkg_cache#meta/pkg_cache.cm",
        "startup": "eager",
    },
],
```
 

 
### collections  馆藏 

The `collections` section declares collections as described in [Component collections][collections]. “集合”部分声明集合，如[组件集合] [集合]中所述。

`collections` is an array of objects with the following properties:  “ collections”是具有以下属性的对象数组：

 
- `name`: The name of the component collection, which is a string of one or more of the following characters: `a-z`, `0-9`, `_`, `.`, `-`. -`name`：组件集合的名称，它是一个或多个以下字符的字符串：`a-z`，`0-9`，`_`，`.`，`-`。
- `durability`: The duration of child component instances in the collection.  -`durability`：集合中子组件实例的持续时间。
    - `transient`: The instance exists until its containing realm is stopped or it is explicitly destroyed. -`transient`：实例存在，直到其包含的域停止或被明确销毁为止。
    - `persistent`: The instance exists until it is explicitly destroyed. This mode is not yet supported. -`persistent`：实例存在直到被明确销毁为止。尚不支持此模式。

Example:  例：

```
"collections": [
    {
        "name": "tests",
        "durability": "transient",
    },
],
```
 

 
### use  使用 

The `use` section contains `use` declarations of child component instances as explained in [Routing terminology](#routing-terminology). “使用”部分包含子组件实例的“使用”声明，如[路由术语]（路由术语）中所述。

`use` is an array of objects with the following properties:  “ use”是具有以下属性的对象数组：

 
- A capability declaration, one of:  -能力声明，其中之一：
    - `service`: The [source path](#capability-paths) of a service capability.  -`service`：服务能力的[源路径]（capability-paths）。
    - `directory`: The [source path](#capability-paths) of a directory capability. -`directory`：目录功能的[源路径]（capability-paths）。
    - `storage`: The [type](#storage-types) of a storage capability. A manifest can only declare one `use` for each storage type. -`storage`：存储功能的[类型]（存储类型）。清单只能为每种存储类型声明一个“使用”。
- `as` *(optional)*: The explicit [target path](#capability-paths) for the capability. If omitted, defaults to the source path for service and directorycapabilities, and one of `/data` or `/cache` for storage capabilities. Thisproperty cannot be used for meta storage capabilities. -`as` *（可选）*：功能的显式[目标路径]（capability-paths）。如果省略，则默认使用服务和目录功能的源路径，以及/ data或/ cache之一的存储功能。此属性不能用于元存储功能。

Example:  例：

```
"use": [
    {
        "service": "/svc/fuchsia.logger.LogSink",
    },
    {
        "directory": "/data/themes",
        "as": "/themes",
    },
    {
        "storage": "data",
        "as": "/my_data",
    },
],
```
 

 
### expose  暴露 

The `expose` section declares capabilities exposed by this component, as explained in [Routing terminology](#routing-terminology). “暴露”部分声明此组件公开的功能，如[路由术语]（路由术语）中所述。

`expose` is an array of objects with the following properties:  expose是具有以下属性的对象数组：

 
- A capability declaration, one of:  -能力声明，其中之一：
    - `service`: The [source path](#capability-paths) of a service capability.  -`service`：服务能力的[源路径]（capability-paths）。
    - `directory`: The [source path](#capability-paths) of a directory capability. -`directory`：目录功能的[源路径]（capability-paths）。
- `from`: The source of the capability, one of:  -`from`：功能的来源，其中之一：
    - `self`: This component.  -`self`：此组件。
    - `#<child-name>`: A [reference](#references) to a child component instance.  -`<child-name>`：子组件实例的[reference]（引用）。
- `as` *(optional)*: The explicit [target path](#capability-paths) for the capability. If omitted, defaults to the source path. -`as` *（可选）*：功能的显式[目标路径]（capability-paths）。如果省略，则默认为源路径。

Example:  例：

```
"expose": [
    {
        "directory": "/data/themes",
        "from": "self",
    },
    {
        "service": "/svc/pkg_cache",
        "from": "#pkg_cache",
        "as": "/svc/fuchsia.pkg.PackageCache",
    },
],
```
 

 
### offer  提供 

The `offer` section declares capabilities offered by this component, as explained in [Routing terminology](#routing-terminology). “报价”部分声明了此组件提供的功能，如[路由术语]（路由术语）中所述。

`offer` is an array of objects with the following properties:  “ offer”是具有以下属性的对象数组：

 
- A capability declaration, one of:  -能力声明，其中之一：
    - `service`: The [source path](#capability-paths) of a service capability.  -`service`：服务能力的[源路径]（capability-paths）。
    - `directory`: The [source path](#capability-paths) of a directory capability. -`directory`：目录功能的[源路径]（capability-paths）。
    - `storage`: The [type](#storage-types) of a storage capability.  -`storage`：存储功能的[类型]（存储类型）。
- `from`: The source of the capability, one of:  -`from`：功能的来源，其中之一：
    - `realm`: The component's containing realm (parent). This source can be used for all capability types. -`realm`：组件的包含领域（父）。此源可用于所有功能类型。
    - `self`: This component. This source can only be used when offering service or directory capabilities. -`self`：此组件。仅在提供服务或目录功能时才能使用此源。
    - `#<child-name>`: A [reference](#references) to a child component instance. This source can only be used when offering service or directorycapabilities. -`<child-name>`：子组件实例的[reference]（引用）。仅当提供服务或目录功能时才能使用此源。
    - `#<storage-name>` A [reference](#references) to a storage declaration. This source can only be used when offering storage capabilities. -`<storage-name>`对存储声明的[引用]（引用）。仅在提供存储功能时才能使用此源。
    - `to`: An array of capability targets, each of which is a [reference](#references) to the child or collection to which thecapability is being offered, of the form `#<target-name>`. -to：to的能力目标数组，每个目标都是对提供能力的子项或集合的[reference]（引用），形式为<target-name>。
    - `as` *(optional)*: The explicit [target path](#capability-paths) for the capability. If omitted, defaults to the source path. This path cannot beused for storage capabilities. -`as` *（可选）*：功能的显式[目标路径]（capability-paths）。如果省略，则默认为源路径。该路径不能用于存储功能。

Example:  例：

```
"offer": [
    {
        "service": "/svc/fuchsia.logger.LogSink",
        "from": "#logger",
        "to": [ "#fshost", "#pkg_cache" ],
    },
    {
        "directory": "/data/blobfs",
        "from": "self",
        "to": [ "#pkg_cache" ],
        "as": "/blobfs",
    },
    {
        "directory": "/data",
        "from": "realm",
        "to": [ "#fshost" ],
    },
    {
        "storage": "meta",
        "from": "realm",
        "to": [ "#logger" ],
    },
],
```
 

 
### storage  存储 

A `storage` declaration creates three storage capabilities, for "data", "cache", and "meta" storage. These storage capabilities are backed by a preexistingdirectory capability, as explained in [Storagecapabilities](#storage-capabilities). “ storage”声明创建了三个存储功能，分别用于“数据”，“缓存”和“元”存储。如[Storagecapabilities]（存储功能）中所述，这些存储功能由预先存在的目录功能支持。

`storage` is an array of objects with the following properties:  “ storage”是具有以下属性的对象数组：

 
- `name`: A name for this storage section which can be used by an `offer`.  -`name`：此存储段的名称，可由`offer`使用。
- `from`: The source of the directory capability backing the new storage capabilities, one of: -`from`：支持新存储功能的目录功能的来源，其中之一：
    - `realm`: The component's containing realm (parent).  -`realm`：组件的包含领域（父）。
    - `self`: This component.  -`self`：此组件。
    - `#<child-name>`: A [reference](#references) to a child component instance.  -`<child-name>`：子组件实例的[reference]（引用）。
- `path`: The [source path](#capability-paths) of a directory capability.  -`path`：目录功能的[源路径]（capability-paths）。

 
### facets  方面 

The `facets` section is a JSON object containing [facets](#facet-metadata), chunks of metadata which components may interpret for their own purposes. Thecomponent framework enforces no schema for this section, but third parties mayexpect their facets to adhere to a particular schema. “ facets”部分是一个JSON对象，其中包含[facets]（facet-metadata），即元数据块，组件可以出于自身目的对其进行解释。组件框架对此部分不执行任何模式，但是第三方可以期望其各个方面遵循特定的模式。

