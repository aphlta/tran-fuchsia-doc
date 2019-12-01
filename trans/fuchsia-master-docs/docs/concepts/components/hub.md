 
# Hub  毂 

 
## Definition  定义 

The hub is a portal for tools to access detailed structural information about component instances at runtime, such as their names, job and process ids, andexposed capabilities. 该中心是一个门户网站，用于工具在运行时访问有关组件实例的详细结构信息，例如其名称，作业和流程ID以及公开的功能。

 
## Organization  组织 

The hub’s structure is mostly read-only. It is not possible to create, rename, delete, or otherwise modify directories and files which form thestructure of the hub itself. However, the[outgoing](/docs/concepts/system/abi/system.md) directories ofcomponent instances may include mutable directories, files, and services whichclients can access through the hub. 集线器的结构大部分是只读的。无法创建，重命名，删除或以其他方式修改形成集线器本身结构的目录和文件。但是，组件实例的[outgoing]（/ docs / concepts / system / abi / system.md）目录可能包含可变目录，文件和客户端可以通过集线器访问的服务。

The component instance tree is reflected in the hierarchy of the hub. A given [realm's](realms.md) hub can be accessed by successively traversing instancesdown the `children/` subdirectory. Moreover, the root of a hub directory isalways scoped to a particular realm. Having opened a directory representing arealm, a client can obtain information about the realm itself, its child realms,and its component instances, but it cannot obtain any information about therealm's parent. This structure makes it easy to constrain the parts of the hubparticular clients can access. 组件实例树反映在集线器的层次结构中。可以通过在“ children /”子目录下连续遍历实例来访问给定的[realm]（realms.md）中心。此外，集线器目录的根始终位于特定领域。打开代表arealm的目录后，客户端可以获取有关领域本身，其子领域及其组件实例的信息，但无法获得有关领域父级的任何信息。这种结构使约束特定客户可以访问的部分变得容易。

 
## Schema  架构图 

The hub is organized as follows:  该中心组织如下：

 
### [Execution Independent State](#execution-independent-state)  [执行独立状态]（执行独立状态） 

The following are a set of execution independent files and subdirectories. These files and directories are visible and traversable even when a component is onlycreated but not started. 以下是一组与执行无关的文件和子目录。即使仅创建而不启动组件，这些文件和目录也是可见且可遍历的。

 
+ **url**: The component’s URL in text format.  + ** url **：文本格式的组件的URL。

 
+ **children/**: A directory of child component instances, indexed by child moniker. + ** children / **：子组件实例的目录，由child昵称索引。

 
+ **children/\<name\>/...** : A child instance (looks like the root).  + ** children / \ <名称\> /...**：一个子实例（看起来像根）。

 
### [Execution Context](#execution-context)  [执行上下文]（执行上下文） 

The following subdirectories represent the state associated with the execution context of a component instance. The execution subdirectory will only be visibleand traversable when a component instance is running on the system. 以下子目录表示与组件实例的执行上下文关联的状态。仅当组件实例在系统上运行时，执行子目录才是可见和可遍历的。

 
+ **exec/** : This directory contains information about instance's execution context, only exists while the instance is running. + ** exec / **：此目录包含有关实例的执行上下文的信息，仅在实例运行时存在。

 
+ **exec/resolved_url**: The component's resolved URL in text format.  + ** exec / resolved_url **：文本格式的组件的已解析URL。

 
+ **exec/in/**: The instance's incoming namespace, as supplied by the component manager. This contains a listing of services and directoriesaccessible to the given component instance. A component can connect directly tothese services from the Hub by opening the provided path. + ** exec / in / **：实例的传入名称空间，由组件管理器提供。这包含给定组件实例可访问的服务和目录的列表。组件可以通过打开提供的路径从集线器直接连接到这些服务。

 
+ **exec/expose/** : The instance's exposed services as listed in its manifest file. A component can connect directly to these services from the Hubby opening the provided path. + ** exec / expose / **：清单文件中列出的实例的公开服务。组件可以通过打开提供的路径从Hubby直接连接到这些服务。

 
+ **exec/out/** : The instance's outgoing namespace, served by the instance itself. A component can connect directly to these services from the Hub by opening theprovided path. + ** exec / out / **：实例本身的输出名称空间，由实例本身提供。组件可以通过打开提供的路径从集线器直接连接到这些服务。

 
+ **exec/runtime/**: Information about the instance's runtime environment supplied by its runner (e.g. ELF runner, Dart runner), organized by topic. + ** exec / runtime / **：由实例的运行程序（例如ELF运行程序，Dart运行程序）提供的有关实例运行时环境的信息，按主题进行组织。

 
+ **exec/runtime/elf/**: Information about the instance's main process and job (if it has one) if it was started by the elf runner. + ** exec / runtime / elf / **：如果实例由elf运行程序启动，则有关实例的主要过程和作业的信息（如果有）。

 
+ **exec/runtime/elf/process-id**: The instance's process id in text format. + ** exec / runtime / elf / process-id **：实例格式的实例的进程ID。

 
+ **exec/runtime/elf/job-id**: The instance's job id in text format.  + ** exec / runtime / elf / job-id **：实例的文本格式的作业ID。

 

 
+ **exec/runtime/elf/args/**: A directory of command-line arguments. These arguments are presented as a series of files from `0` onward. + ** exec / runtime / elf / args / **：命令行参数目录。从“ 0”开始，这些参数以一系列文件的形式出现。

 
## [Capability Routing](#capability-routing)  [能力路由]（能力路由） 

You can make the **/hub** directory available in any component's incoming namespace with the appropriate declaration in the component's manifest. 您可以在组件清单中使用适当的声明，使** / hub **目录在任何组件的传入名称空间中可用。

 
### Basic Example  基本范例 

In this example above, the component, `hub_client` has requested the hub in its namespace from the `framework`. The `framework` provides `hub_client` with a hubdirectory rooted at `hub_client`. In other words, `hub_client` cannot inspectinformation about component instances above it in the component hierarchy. 在上面的示例中，组件“ hub_client”已从“框架”请求其名称空间中的中心。框架为hub_client提供了一个以hub_client为根的中心目录。换句话说，“ hub_client”无法检查有关组件层次结构中位于其上方的组件实例的信息。

```
// In hub_client.cml.
{
    "program": {
        "binary": "bin/hub_client",
    },
    "use": [
        {
            "directory": "/hub", "from": "framework"
        }
    ],
}
```
 

 
### Offering Parent Hub  提供家长中心 

In this example, the parent component instance passes its view of the Hub to `hub_client` which then maps it as `/parent_hub` in its namespace. `hub_client`can inspect information about its parent and siblings through `/parent_hub`. 在此示例中，父组件实例将其对集线器的视图传递给“ hub_client”，然后将其在其命名空间中映射为“ / parent_hub”。 “ hub_client”可以通过“ / parent_hub”检查有关其父母和兄弟姐妹的信息。

In the parent component manifest:  在父组件清单中：

```
{
    // Route the root Hub to hub_client.
    "offer": [
        {
          "directory": "/hub",
          "from": "framework",
          "to": [
            {
              "dest": "#hub_client",
            },
          ],
        },
    ],
    "children": [
        {
            "name": "hub_client",
            "url": "fuchsia-pkg://fuchsia.com/hub_test#meta/hub_client.cm",
            "startup": "eager",
        },
    ],
```
 

In `hub_client.cml`:  在`hub_client.cml`中：

```
{
    "program": {
        "binary": "bin/hub_client",
    },
    "use": [
        {
          "directory": "/hub",
          "from": "realm",
          "as": "/parent_hub"
        }
    ]
}
```
 

 
### Exposing a sibling Hub  暴露同级集线器 

In this example, `hub_client_sibling` exposes its view of the Hub to its containing realm. The realm, in turn, offers that view of the Hub as`\sibling_hub` to `hub_client`. `hub_client` maps that view of the Hub to itsincoming namespace. 在此示例中，`hub_client_sibling`将其对集线器的视图暴露于其包含的领域。反过来，该领域将集线器的视图作为\\ sibling_hub`提供给`hub_client`。 “ hub_client”将集线器的视图映射到其传入的名称空间。

In `hub_client_sibling.cml`:  在`hub_client_sibling.cml`中：

```
{
    "program": {
        "binary": "bin/hub_client_sibling",
    },
    "expose": [
        {
            "directory": "/hub",
            "from": "framework",
        },
    ],
}
```
 

In the parent component manifest file:  在父组件清单文件中：

```
{
    // Route hub_client_sibling's view of the Hub to hub_client.
    "offer": [
        {
            "directory": "/hub",
            "from": "#hub_client_sibling",
            "to": [
              {
                "dest": "#hub_client",
                "as": "/sibling_hub",
              }
            ]
        }
    ],
    "children": [
        {
            "name": "hub_client_sibling",
            "url": "fuchsia-pkg://fuchsia.com/hub_test#meta/hub_client_sibling.cm",
            "startup": "eager",
        },
        {
            "name": "hub_client",
            "url": "fuchsia-pkg://fuchsia.com/hub_test#meta/hub_client.cm",
            "startup": "eager",
        },
    ],
}
```
 

In hub_client.cml:  在hub_client.cml中：

```
{
    "program": {
        "binary": "bin/hub_client",
    },
    "use": [
        {
            "directory": "/sibling_hub", "from": "realm",
        }
    ]
}
```
