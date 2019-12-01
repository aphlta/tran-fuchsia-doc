 
# Service capabilities  服务能力 

[Service capabilities][glossary-service] allow components to connect to [FIDL][glossary-fidl] services provided either by other components or thecomponent framework itself. [服务功能] [词汇服务]允许组件连接到其他组件或组件框架本身提供的[FIDL] [词汇表]服务。

 
## Creating service capabilities  创建服务能力 

When a component has a service that is made available to other components, the service's path in the component's [outgoing directory][glossary-outgoing] is[exposed][expose] to the component's parent... 当某个组件具有可用于其他组件的服务时，该组件的[传出目录] [词汇表-传出]中的服务路径会[暴露] [暴露给]组件的父级...

```
{
    "expose": [{
        "service": "/svc/fuchsia.example.ExampleService",
        "from": "self",
    }],
}
```
 

... or [offered][offer] to some of the component's children.  ...或[提供] [提供]给组件的某些子项。

```
{
    "offer": [{
        "service": "/svc/fuchsia.example.ExampleService",
        "from": "self",
        "to": [{
            { "dest": "#child-a" },
            { "dest": "#child-b" },
        }],
    }],
}
```
 

 
## Consuming service capabilities  消费服务能力 

When a service capability is offered to a component from its containing realm it can be [used][use] to make the service accessible through the component's[namespace][glossary-namespace]. 当从其包含的领域向组件提供服务功能时，可以使用[使用] [使用]通过组件的[名称空间] [词汇表名称空间]访问该服务。

This example shows a directory named `/svc` that is included in the component's namespace. When the component attempts to open the`fuchsia.example.ExampleService` item in this directory, the component frameworkperforms [capability routing][capability-routing] to find the component thatprovides this service. Then, the framework connects the newly opened channel tothis provider. 本示例显示了一个名为`/ svc`的目录，该目录包含在组件的名称空间中。当组件尝试在此目录中打开“ fuchsia.example.ExampleService”项时，组件框架将执行[功能路由] [功能路由]以查找提供此服务的组件。然后，框架将新打开的通道连接到此提供程序。

```
{
    "use": [{
        "service": "/svc/fuchsia.example.ExampleService",
    }],
}
```
 

See [life of a service open][life-of-a-service-open] for a detailed walkthrough of what happens during this open request. 有关此开放请求期间发生的情况的详细演练，请参见[服务的生命周期] [服务生命周期]。

See [`//examples/components/routing`][routing-example] for a working example of routing a service capability from one component to another. 有关将服务功能从一个组件路由到另一个组件的工作示例，请参见[`// examples / components / routing`] [routing-example]。

 
## Consuming service capabilities provided by the framework  框架提供的消费服务功能 

Some service capabilities are provided by the component framework, and thus can be [used][use] by components without their parents [offering][offer] them. 组件框架提供了某些服务功能，因此组件可以在不使用其父项的情况下[使用] [使用]。

For a list of these services and what they can be used for, see the [framework services][framework-services] section of the component manifests documentation. 有关这些服务及其用途的列表，请参阅组件清单文档的[framework services] [framework-services]部分。

```
{
    "use": [{
        "service": "/svc/fuchsia.sys2.Realm",
        "from": "framework",
    }],
}
```
 

 
## Service paths  服务路径 

The path used to refer to a given service provides a hint to clients which protocol the server expects clients to use, but this is entirely a convention.The paths can even be renamed when being [offered][offer], [exposed][expose], or[used][use]. 用于引用给定服务的路径向客户端提示服务器希望服务器使用的协议，但这完全是一个约定。甚至可以在[提供] [提供]，[公开] [公开]时重命名路径。 ]或[二手] [使用]。

In the following example, there are three components, `A`, `B`, and `C`, with the following layout: 在下面的示例中，具有三个组件，`A`，`B`和`C`，其布局如下：

```
 A  <- offers service "/svc/fidl.example.X" from "self" to B as "/intermediary"
 |
 B  <- offers service "/intermediary" from "realm" to B as "/intermediary2"
 |
 C  <- uses service "/intermediary2" as "/service/example"
```
 

Each component in this example changes the path used to reference the service when passing it along in this chain, and so long as components `A` and `C` knowwhich FIDL protocol to use over the channel, this will work just fine. 在此示例中，每个组件在传递此链中的服务时都会更改用于引用服务的路径，只要组件“ A”和“ C”知道在通道上使用哪种FIDL协议，就可以正常工作。

```
A.cml:
{
    "offer": [{
        "service": "/svc/fidl.example.X",
        "from": "self",
        "to": [{
            { "dest": "#B", "as": "/intermediary" },
        }],
    }],
    "children": [{
        "name": "B",
        "url": "fuchsia-pkg://fuchsia.com/B#B.cm",
    }],
}
```
 

```
B.cml:
{
    "offer": [{
        "service": "/intermediary",
        "from": "realm",
        "to": [{
            { "dest": "#C", "as": "/intermediary2" },
        }],
    }],
    "children": [{
        "name": "C",
        "url": "fuchsia-pkg://fuchsia.com/C#C.cm",
    }],
}
```
 

```
C.cml:
{
    "use": [{
        "service": "/intermediary2",
        "as": "/service/example",
    }],
}
```
 

When `C` attempts to open the `example` node in its `/service` directory, `A` will see an open request for `/svc/fidl.example.X`. If any of the names didn'tmatch in this chain, `C` would see the opened `example` node be closed. 当C试图在其/ service目录中打开example节点时，A将会看到对/svc/fidl.example.X的打开请求。如果此链中的任何名称都不匹配，则C会看到打开的example节点被关闭。

