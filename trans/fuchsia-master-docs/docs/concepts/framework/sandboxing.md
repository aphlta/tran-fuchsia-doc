 
# Sandboxing  沙盒 

This document describes how sandboxing works in Fuchsia.  本文档介绍了沙箱在紫红色中的工作方式。

 
## An empty process has nothing  空进程没有任何东西 

On Fuchsia, a newly created process has nothing. A newly created process cannot access any kernel objects, cannot allocate memory, and cannot even execute code.Of course, such a process isn't very useful, which is why we typically createprocesses with some initial resources and capabilities. 在紫红色上，新创建的过程什么都没有。新创建的进程无法访问任何内核对象，无法分配内存甚至无法执行代码。当然，这样的进程不是很有用，这就是为什么我们通常使用一些初始资源和功能来创建进程。

Most commonly, a process starts executing some code with an initial stack, some command line arguments, environment variables, a set of initial handles. One ofthe most important initial handles is the `PA_VMAR_ROOT`, which the process canuse to map additional memory into its address space. 最常见的是，进程开始使用初始堆栈，一些命令行参数，环境变量和一组初始句柄执行一些代码。最重要的初始句柄之一是“ PA_VMAR_ROOT”，进程可以使用它来将其他内存映射到其地址空间。

 
## Namespaces are the gateway to the world  命名空间是通向世界的门户 

Some of the initial handles given to a process are directories that the process mounts into its _namespace_. These handles let the process discover andcommunicate with other processes running on the system, including file systemsand other servers. See [Namespaces](/docs/concepts/framework/namespaces.md) for more details. 给该进程的一些初始句柄是该进程装入其_namespace_的目录。这些句柄使进程可以发现并与系统上运行的其他进程进行通信，包括文件系统和其他服务器。有关更多详细信息，请参见[命名空间]（/ docs / concepts / framework / namespaces.md）。

The namespace given to a process strongly influences how much of the system the process can influence. Therefore, configuring the sandbox in which a processruns amounts to configuring the process's namespace. 给进程指定的名称空间强烈影响该进程可以影响多少系统。因此，配置运行流程的沙箱等同于配置流程的名称空间。

 
## Package namespace  包名称空间 

A [component](/docs/glossary.md#component) run from a package is given access to `/pkg`, which is a read-only view of the package containing the component. Toaccess these resources at runtime, a process can use the `/pkg` namespace. Forexample, the `root_presenter` can access `cursor32.png` using the absolute path`/pkg/data/cursor32.png`. 从包运行的[component]（/ docs / glossary.mdcomponent）可以访问`/ pkg`，这是包含该组件的包的只读视图。为了在运行时访问这些资源，进程可以使用`/ pkg`命名空间。例如，“ root_presenter”可以使用绝对路径“ /pkg/data/cursor32.png”访问“ cursor32.png”。

 
## Services  服务 

Processes that are [components](/docs/glossary.md#component) receive an `/svc` directory in their namespace. The services available through `/svc` are asubset of the services provided by the component's[environment](/docs/glossary.md#environment). This subset is determined by the[`sandbox.services`](/docs/concepts/storage/component_manifest.md#sandbox) allowlist in thecomponent's [manifest file](/docs/concepts/storage/component_manifest.md). 作为[components]（/ docs / glossary.mdcomponent）的进程在其名称空间中接收一个`/ svc`目录。通过`/ svc`可用的服务是组件的[environment]（/ docs / glossary.mdenvironment）提供的服务的子集。此子集由组件[清单文件]（/ docs / concepts / storage / component_manifest.md）中的[`sandbox.services`]（/​​ docs / concepts / storage / component_manifest.mdsandbox）允许列表确定。

A typical component will interact with a number of services from `/svc` in order to play some useful role in the system. For example, the service`fuchsia.sys.Launcher` is required if a component wishes to launch othercomponents. 一个典型的组件将与来自/ svc的许多服务交互，以便在系统中发挥某些有用的作用。例如，如果组件希望启动其他组件，则需要服务fuchsia.sys.Launcher。

Processes that are not components may or may not have `/svc`. These processes receive whatever `/svc` their creator decided to provide to them. 不是组件的进程可能具有/没有svc。这些进程接收其创建者决定提供给他们的`/ svc`。

 
## Configuring additional namespaces  配置其他名称空间 

If a process requires access to additional resources (e.g., device drivers), the package can request access to additional names by including the `sandbox`property in its  [Component Manifest](/docs/concepts/storage/component_manifest.md)for the package. For example, the following `meta/sandbox` file requestsdirect access to the input driver: 如果某个进程需要访问其他资源（例如设备驱动程序），则该程序包可以通过在其[Component Manifest]（/ docs / concepts / storage / component_manifest.md）中包含“沙盒”属性来请求访问其他名称。包。例如，以下`meta / sandbox`文件请求直接访问输入驱动程序：

```
{
    "dev": [ "class/input" ]
}
```
 

In the current implementation, the [AppMgr](/docs/glossary.md#appmgr) grants all such requests, but that is likely to change as the system evolves. 在当前的实现中，[AppMgr]（/ docs / glossary.mdappmgr）会批准所有此类请求，但是随着系统的发展，这种请求可能会发生变化。

 
## Building a package  建立一个包裹 

To build a package, use the `package()` macro in `gn` defined in [`//build/package.gni`](/build/package.gni).See the documentation for the `package()` macro for details about including resources. 要构建软件包，请使用[`//build/package.gni](/build/package.gni）中定义的`gn`中的`package（）`宏。请参阅`package（）`宏的文档有关包含资源的详细信息。

