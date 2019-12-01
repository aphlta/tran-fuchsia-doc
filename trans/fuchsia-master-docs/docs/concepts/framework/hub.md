 
# Hub  毂 

 
## What do we mean by hub?  集线器是什么意思？ 

The hub is a portal for introspection.  It enables tools to access detailed structural information about realms and component instances at runtime,such as their names, job and process ids, and published services. 该中心是自省的门户。它使工具能够在运行时访问有关领域和组件实例的详细结构信息，例如它们的名称，作业和流程ID以及发布的服务。

 
## Organization  组织 

The hub is organized as a tree of directories and files which describe individual realms and component instances at runtime. 集线器被组织为目录树和文件树，它们描述了运行时的各个领域和组件实例。

The hub’s structure is mostly **read-only**.  It is not possible to create, rename, delete, or otherwise modify directories and files whichform the structure of the hub itself.  However, the **outgoing**directories of component instances may include mutable directories,files, and services which clients can access via the hub. 集线器的结构大部分是“只读”的。无法创建，重命名，删除或以其他方式修改形成集线器本身结构的目录和文件。但是，组件实例的“外发”目录可能包括客户端可以通过集线器访问的可变目录，文件和服务。

The hub's structure is **observable**.  Clients can watch the filesystem to observe changes such as realms being created or destroyed as indicatedby directories being added or removed. 集线器的结构是“可观察的”。客户端可以观察文件系统以观察更改，例如正在添加或删除目录所指示的正在创建或破坏的领域。

The hub's structure is **scope constrained**.  Successively deeper levels of the hub's directory tree are scoped to successively more specific objects.For example, having opened a directory representing a realm, a clientcan obtain information about the realm itself, its child realms, andits component instances, but it cannot obtain any information aboutthe realm's parent.  This structure makes it easier to constrain theparts of the hub particular clients can access. 集线器的结构受“范围约束”。集线器目录树的层次越来越深，其作用域依次是特定对象。例如，打开代表领域的目录后，客户端可以获取有关领域本身，其子领域及其组件实例的信息，但它无法获取任何信息关于领域的父母。这种结构使限制特定客户可以访问的集线器部分变得更加容易。

 
## Schema  架构图 

_Note: this document is describing the hub provided by `appmgr`. Hub directories provided by component manager have a different schema._ _注意：该文档描述了`appmgr`提供的集线器。组件管理器提供的集线器目录具有不同的架构。

The hub is organized as follows:  该中心组织如下：

**\<realm name\>/\<realm id\>/**: realm directory > A read-only directory containing information about a realm.  The root realm’s> realm directory is typically mounted at /hub in the root development shell. ** \ <领域名称\> / \ <领域ID \> / **：领域目录>包含有关领域信息的只读目录。根领域的>领域目录通常安装在根开发外壳程序的/ hub中。

**\<realm id\>/name**: realm name > A read-only file containing the name of the realm, in UTF-8 without padding or> terminators. ** \ <领域ID \> /名称**：领域名称>包含领域名称的只读文件，格式为UTF-8，不带填充或>终止符。

**\<realm id\>/job-id**: realm’s job id > A read-only file containing the koid of the realm’s job, in decimal ASCII> without padding or terminators. ** \ <领域ID \> / job-id **：领域的作业ID>只读文件，包含领域作业的类别，以十进制ASCII>，不带填充符或终止符。

**\<realm id\>/svc**: realm’s services > Contains all the services which are available in this realm. ls command> will only show the services which were directly created in this realm. ** \ <领域ID \> / svc **：领域的服务>包含该领域中可用的所有服务。 ls命令>将仅显示在此领域中直接创建的服务。

**\<realm id\>/r/**: child realm list > A read-only directory containing a list of child realms. ** \ <领域ID \> / r / **：子领域列表>包含子领域列表的只读目录。

**\<realm id\>/r/\<child realm name\>/\<child realm id\>/**: child realm directory > A read-only directory containing information about a child realm. ** \ <领域ID \> / r / \ <子领域名称\> / \ <子领域ID \> / **：子领域目录>包含有关子领域信息的只读目录。

**\<realm id\>/c/**: component instance list > A read-only directory containing a list of component instances. ** \ <领域ID \> / c / **：组件实例列表>包含组件实例列表的只读目录。

**\<realm id\>/c/\<component name\>/\<component instance id\>/**: component instance directory > A read-only directory containing information about a component. ** \ <领域ID \> / c / \ <组件名称\> / \ <组件实例ID \> / **：组件实例目录>包含有关组件信息的只读目录。

**\<component instance id\>/name**: component’s short name > A read-only file containing just the name of the component, in UTF-8 without> padding or terminators. ** \ <组件实例ID \> /名称**：组件的简称>一个仅包含组件名称的只读文件，格式为UTF-8，不带>填充或终止符。

**\<component instance id\>/args**: component’s original command-line arguments > A read-only file containing the component’s original command-line arguments,> in UTF-8 without padding or terminators. ** \ <组件实例ID \> / args **：组件的原始命令行参数>包含组件的原始命令行参数的只读文件，>以UTF-8格式，没有填充或终止符。

**\<component instance id\>/url**: component’s url > A read-only file containing the component’s url. ** \ <组件实例ID \> / url **：组件的url>包含组件的url的只读文件。

**\<component instance id\>/job-id**: component’s job id > A read-only file containing the koid of the component’s job, in decimal ASCII> without padding or terminators. Multiple component instances may coexist> within the same job. Components may also create new jobs of their own, which> are not reflected here. ** \ <组件实例ID \> / job-id **：组件的作业ID>只读文件，其中包含组件作业的类别，以十进制ASCII>，不带填充符或终止符。多个组件实例可以在同一作业中共存。组件也可以创建自己的新作业，这在此处未反映。

**\<component instance id\>/process-id**: component’s process id > A read-only file containing the koid of the component’s process, in decimal> ASCII without padding or terminators. Multiple component instances may> coexist within the same process. Components may also create new processes of> their own, which are not reflected here. ** \ <组件实例ID \> / process-id **：组件的进程ID>只读文件，其中包含组件进程的类别，以十进制> ASCII，不带填充或终止符。多个组件实例可以>在同一进程中共存。组件也可能会创建自己的新过程，此处未反映。

**\<component instance id\>/system\_objects**: system-level component inspection > A directory tree exposing objects conforming to the [Inspect API](/docs/development/inspect/README.md).> This directory tree is managed by the system to expose system-level> information about the components. ** \ <组件实例ID \> / system \ _objects **：系统级组件检查>暴露符合[Inspect API]（/ docs / development / inspect / README.md）的对象的目录树。该树由系统管理，以暴露有关组件的系统级信息。

**\<component instance id\>/in/**: component's incoming namespace > A directory tree exposing objects that have been offered to the component by> its parent or are ambiently offered by the Component Framework. ** \ <组件实例ID \> / in / **：组件的传入名称空间>目录树，它公开了由其父对象提供给组件的对象或由组件框架提供的对象。

**\<component instance id\>/in/svc**: component's incoming services directory > A directory containing the services that are available to the component> (either from its parent or from the Component Framework).>> This maps to `/svc` in the component's own namespace. ** \ <组件实例ID \> / in / svc **：组件的传入服务目录>包含该组件可用服务的目录>（从其父级或从组件框架）。>>映射到组件自己的名称空间中的“ / svc”。

**\<component instance id\>/out/**: component’s out directory > A directory containing objects which the component has exported, such as its> services.  May be absent if the component exports nothing.  May contain> read-write objects. ** \ <组件实例ID \> / out / **：组件的出目录>包含组件已导出对象的目录，例如>服务。如果组件不输出任何内容，则可能不存在。可能包含>读写对象。

**\<component instance id\>/out/svc**: component’s exported public object directory > A directory containing objects which the component has exported to its host,> such as its services.  May contain read-write objects. ** \ <组件实例ID \> / out / svc **：组件的导出公共对象目录>包含组件已导出到其主机的对象的目录，例如服务。可能包含读写对象。

**\<component instance id\>/out/ctrl**: component’s exported control object directory > A directory containing objects which the component has offered to the realm> manager for lifecycle control.  May contain read-write objects. ** \ <组件实例ID \> / out / ctrl **：组件的导出控制对象目录>包含组件已提供给领域>管理器以进行生命周期控制的对象的目录。可能包含读写对象。

**\<component instance id\>/out/debug**: component’s exported debug object directory > A directory containing objects which the component has published for debugging> purposes, such as introspection files and services.  May contain read-write> objects. ** \ <组件实例ID \> / out / debug **：组件的导出调试对象目录>包含组件已发布以进行调试的对象的目录，例如自省文件和服务。可能包含读写对象。

**\<component instance id\>/out/objects**: component’s exported structured objects > A directory tree exposing objects conforming to the [Inspect API](/docs/development/inspect/README.md).> This directory tree is exposed by the component itself to allow inspection> of component-specific data. ** \ <组件实例ID \> / out / objects **：组件导出的结构化对象>暴露符合[Inspect API]（/ docs / development / inspect / README.md）的对象的目录树。>此目录树由组件本身暴露，以允许检查>特定于组件的数据。

