 
# Life of a service open  服务的生命是开放的 

This document describes the steps that occur when a component attempts to connect to a service in its namespace. 本文档描述了组件尝试连接到其命名空间中的服务时发生的步骤。

These steps apply to the components v2 model as run under component manager. Portions of it also apply to the components v1 model as run under appmgr. 这些步骤适用于在组件管理器下运行的组件v2模型。它的某些部分也适用于在appmgr下运行的组件v1模型。

At a high level these steps are:  在较高级别上，这些步骤是：

 
- Component manager will [construct a component's namespace][ns-construction] based on the `use` declarations in its manifest. -组件管理器将基于清单中的`use`声明来[构造组件的名称空间] [ns-construction]。
- Once running, a component will attempt to [open a service][service-open] in its namespace. -一旦运行，组件将尝试在其命名空间中[打开服务] [service-open]。
- This `Open` request is received by component manager, which performs the [capability routing][cap-routing] necessary to find the component providingthe service. -组件管理器接收到此“打开”请求，组件管理器执行查找提供服务的组件所需的[功能路由] [功能路由]。
- Component manager [binds to the component providing the service][binding] and connects the `Open` request to it -组件管理器[绑定到提供服务的组件] [绑定]，并将“打开”请求与其连接

 
## Constructing a component's namespace  构造组件的名称空间 

A [_namespace_][namespaces] is a set of directories that are offered to a component when it is started. Each directory is associated with a file systempath through which the component may access files and services offered by othercomponents. [_namespace _] [namespaces]是在启动组件时提供给组件的一组目录。每个目录都与文件系统路径相关联，组件可以通过该文件系统路径访问其他组件提供的文件和服务。

These directories take the form of [handles][handle] to [channels][channel], over which the component can use [the `fuchsia.io.Directory` FIDLprotocol][fuchsia.io]. 这些目录采用[handles] [handle]到[channels] [channel]的形式，组件可以在其上使用[fuchsia.io.Directory` FIDLprotocol] [fuchsia.io]。

For example, all components will receive a handle to the contents of the package from which they were created at `/pkg`. This means that a component can see whatbinaries are available in their package by reading the contents of `/pkg/bin`. 例如，所有组件都将在`/ pkg`处接收到用于创建包内容的句柄。这意味着组件可以通过读取`/ pkg / bin`的内容来查看其程序包中可用的二进制文件。

The `use` declarations in [the component's manifest][component-manifests] determine how the namespace is populated. When a service capability is used... [组件清单] [component-manifests]中的`use`声明确定如何填充名称空间。使用服务功能时...

```cml
"use": [
    {
        "service": "/svc/fuchsia.example.Foo",
    },
]
```
 

...component manager will add an entry to the component's namespace for the parent directory of the service. In this example, this means that componentmanager will add a handle for `/svc` to the namespace. ...组件管理器将在服务的父目录的组件名称空间中添加一个条目。在此示例中，这意味着componentmanager将向名称空间添加`/ svc`的句柄。

This service directory is provided by component manager itself, and component manager will respond to requests for services to this directory for the lifetimeof the component. 该服务目录由组件管理器本身提供，并且组件管理器将在组件的生存期内响应对该目录的服务请求。

The exact semantics of what appears in the namespace varies based on capability type. For example if a directory capability is used instead of the servicecapability... 命名空间中出现的确切语义根据功能类型而有所不同。例如，如果使用目录功能而不是服务功能...

```cml
"use": [
    {
        "directory": "/example/data",
    },
]
```
 

...a handle for the directory itself appears in the namespace instead of a handle for the parent directory. In this example, this means that a handle for`/example/data` will appear in the namespace, whereas if this path was used fora service capability `/example` would appear in the namespace. ...目录本身的句柄出现在名称空间中，而不是父目录的句柄。在此示例中，这意味着“ / example / data”的句柄将出现在名称空间中，而如果将此路径用于服务功能，则“ / example”将出现在名称空间中。

 
## A component opens a service  组件打开服务 

When a component wants to open a service it creates a new channel pair, and sends one end of this pair via an `Open` request over a channel in itsnamespace. For example, if the component wanted to open a connection to`/svc/fuchsia.example.Foo`, one end of the new channel pair would be sent overthe `/svc` handle in its namespace. The component may then call the`fuchsia.example.Foo` protocol over the channel. 当组件想要打开服务时，它会创建一个新的通道对，并通过其命名空间中的通道上的“ Open”请求发送该对的一端。例如，如果组件想要打开到/svc/fuchsia.example.Foo的连接，则新通道对的一端将通过其名称空间中的/ svc句柄发送。然后，该组件可以通过该通道调用“ fuchsia.example.Foo”协议。

Since service directories are provided by component manager, it is component manager that will receive the server end of the new channel via the `Open`request sent by the component. Component manager then must identify thecomponent providing the service over this channel. 由于服务目录由组件管理器提供，因此组件管理器将通过组件发送的“ Open”请求接收新通道的服务器端。然后，组件管理器必须标识通过此通道提供服务的组件。

 
## The `Open` triggers capability routing  “打开”触发功能路由 

To determine the component that provides the service over the channel, component manager must walk the tree of components, following `offer` and `expose`declarations to find the capability's source. This process is referred to as_capability routing_. 为了确定通过通道提供服务的组件，组件管理者必须遵循“要约”和“公开”声明来查找组件的树，以找到功能的来源。此过程称为“能力路由”。

Starting at the parent of the component that triggered the capability routing, component manager will inspect each component's manifest, looking for an `offer`declaration whose destination matches the child. The offer will specify a sourceof either `realm`, `self`, or the name of a child. If the offer came from thecomponent's realm it will continue to walk up the tree, and if the offer camefrom one of the component's children it will walk down the tree to that child. 从触发功能路由的组件的父组件开始，组件管理器将检查每个组件的清单，以寻找目的地与子组件匹配的“要约”声明。该报价将指定“领域”，“自我”或孩子的名字的来源。如果要约来自组件的领域，它将继续沿着树走，如果要约来自组件的一个子对象，它将沿着树走到那个孩子。

Once the routing begins walking down the tree it will look for `expose` declarations, which will specify a source of either `self` or the name of achild. If the capability came from a child then component manager will continueto walk down the tree. 一旦路由开始沿着树走，它将寻找`expose`声明，该声明将指定`self'或achild名称的来源。如果功能来自孩子，则组件管理器将继续沿树走下去。

Once an `offer` or `expose` declaration with a source of `self` is found, then component manager can hand off the channel to that component. 一旦找到带有“ self”源的“ offer”或“ expose”声明，组件管理器便可以将通道移交给该组件。

If at any step of the way the chain is invalid, component manager will log an error and close the channel it received from the `Open` call. This can be causedby various situations, such as: 如果链的任何步骤无效，则组件管理器将记录一个错误并关闭从“打开”调用中接收到的通道。这可能是由多种情况引起的，例如：

 
- A component `C` offered a capability from `realm`, but its parent `R` did not offer the capability to `C`. -组件C提供了来自realm的功能，但其父类R没有提供给C的功能。
- A component `C` offered a capability from its child `D`, but child `D` did not expose the capability to `C`. -组件“ C”提供了其子“ D”的功能，但子“ D”并未向“ C”公开该功能。

For example, consider the following tree of components and their manifests:  例如，考虑以下组件树及其清单：

```
    C
   / \
  B   D
 /
A

A.cml:
{
    "program": {
        "binary": "bin/hippo",
    },
    "expose: [
        {
            "service": "/svc/fuchsia.example.Foo",
            "from": "self",
        },
    ],
}

B.cml:
{
    "expose: [
        {
            "service": "/svc/fuchsia.example.Foo",
            "from": "#A",
        },
    ],
    "children": [
        {
            "name": "A",
            "url": "fuchsia-pkg://fuchsia.com/a#meta/a.cm",
        },
    ]
}

C.cml:
{
    "offer": [
        {
            "service": "/svc/fuchsia.example.Foo",
            "from": "#B",
            "to": [
                { "dest": "#D" },
            ],
        },
    ]
    "children": [
        {
            "name": "B",
            "url": "fuchsia-pkg://fuchsia.com/b#meta/b.cm",
        },
        {
            "name": "D",
            "url": "fuchsia-pkg://fuchsia.com/d#meta/d.cm",
        },
    ]
}

D.cml:
{
    "program": {
        "binary": "bin/hippo",
    },
    "use": [
        {
            "service": "/svc/fuchsia.example.Foo",
        },
    ],
}
```
 

When `D` calls `Open` on `/svc/fuchsia.example.Foo` in its namespace, component manager will walk the tree to find the component that should provide thisservice. It will start at `D`'s parent, `C`, and from there: 当D在其名称空间中的/svc/fuchsia.example.Foo上调用Open时，组件管理器将遍历树以查找应提供此服务的组件。它将从“ D”的父代“ C”开始，并从那里开始：

 
- Look for the `offer` declaration for `fuchsia.example.Foo` to `D`, and see that it comes from child `B`. -在`D`中查找`fuchsia.example.Foo`的`offer`声明，并查看它是否来自子项`B`。
- Look for the `expose` declaration for `fuchsia.example.Foo` from `B`, and see that it comes from `A`. -在`B`中寻找`fuchsia.example.Foo`的`expose`声明，并查看它是否来自`A`。
- Look for the `expose` declaration for `fuchsia.example.Foo` from `A`, and see that it comes from `self`. This means that `A` is the component providing thecapability that `D` is attempting to use. -在A中寻找fuchsia.example.Foo的expose声明，并查看它是否来自self。这意味着“ A”是提供“ D”正在尝试使用的功能的组件。

Now that the provider component has been found, component manager can attempt to hand off the channel it received via the `Open` request. 现在已经找到了提供者组件，组件管理器可以尝试切换通过“打开”请求接收到的通道。

 
## Binding to a component and sending a service channel  绑定组件并发送服务通道 

With the provider found the client component is now bound to the provider. This will cause the component to start running if it is currently stopped. 找到提供程序后，客户端组件便已绑定到提供程序。如果组件当前已停止，这将导致该组件开始运行。

Every component upon being started receives a server handle to an [_outgoing directory_][abi-system] in its handle table. When a component is bound to,component manager forwards the server end of the service channel to theproviding component's outgoing directory, under the source path in the providingcomponent's `offer` or `expose` declaration 每个组件在启动时都会在其句柄表中接收到[_outgoing directory _] [abi-system]的服务器句柄。当绑定一个组件时，组件管理器将服务通道的服务器端转发到提供组件的“ offer”或“ expose”声明中的源路径下的提供组件的传出目录。

In the above example component manager will send an `Open` request over the outgoing directory handle for component `A` to the `/svc/fuchsia.example.Foo`path, providing the channel handle that it received from component `D` when itcalled `Open` to component manager. 在上面的示例中，组件管理器将通过对组件A的传出目录句柄向其/svc/fuchsia.example.Foo路径发送一个“打开”请求，并提供当它从组件D接收到的通道句柄。它向组件管理器开放。

It is then up to component `A` to receive this request and start responding to messages over the channel it was given. 然后由组件“ A”来接收此请求并开始通过给定的通道对消息进行响应。

Since component manager directly forwards the server end of the service channel to the provider component's outgoing directory, it is not involved in messageproxying and is entirely out of the picture after capability routing iscompleted. Once a connection to another component is established, they talkdirectly to each other with no arbiter in the middle. 由于组件管理器将服务通道的服务器端直接转发到提供程序组件的传出目录，因此它不参与消息代理，并且在功能路由完成后完全不在画面之列。建立与另一个组件的连接后，它们将彼此直接对话，而中间没有仲裁器。

 
## Caveats  注意事项 

 
### Runtime unpredictability  运行时不可预测 

Due to the runtime nature of capability routing and the behavior of the components providing capabilities, there is no way to know if a given componentcan successfully access a capability in its namespace before it attempts to doso. Even if a valid offer/expose chain exists for the capability, packageupdates could break this chain at runtime, and it's entirely possible acomponent that claims to provide a capability in its manifest will fail to do sowhen run. 由于功能路由的运行时性质以及提供功能的组件的行为，因此在尝试执行操作之前，无法知道给定组件是否可以成功访问其命名空间中的功能。即使为该功能存在有效的要约/公开链，packageupdates可能在运行时中断该链，并且声称在其清单中提供功能的组件很可能在运行时不会这样做。

 
### Offered vs ambient capabilities  提供与环境功能 

Some capabilities are provided by the component framework itself, and can be directly used by (or will be implicitly provided to) components without theirparent offering these capabilities. Currently these are: 某些功能由组件框架本身提供，并且可以直接由组件使用（或将隐式提供给组件），而无需其父级提供这些功能。当前这些是：

 
- `/pkg`: a handle to the package from which the component was created.  -`/ pkg`：从中创建组件的包的句柄。
- [`/svc/fuchsia.sys2.Realm`][realm.fidl]: a protocol which components can use to manage their own realm. -[`/svc/fuchsia.sys2.Realm`][realm.fidl]：一种协议，组件可以使用该协议来管理自己的领域。

 
### Parent may not `use` capabilities exposed to it  父级可能不会“使用”公开的功能 

Parent components can access capabilities offered by their children at runtime by calling the [`fuchsia.sys2.Realm.BindChild`][realm.fidl] method to start thechild and receive a directory containing the child's exposed services. 父组件可以通过调用[`fuchsia.sys2.Realm.BindChild`] [realm.fidl]方法来访问其子级在运行时提供的功能，以启动子级并接收包含子级公开服务的目录。

To prevent service dependency cycles from occurring in component namespaces, a parent component cannot declare a static dependency on the services of itschildren with `use` declarations; it must use `BindChild()`. 为了防止服务依赖关系周期发生在组件名称空间中，父组件不能使用use声明来声明对其子服务的静态依赖关系。它必须使用`BindChild（）`。

[ns-construction]: #constructing-a-components-namespace [service-open]: #a-component-opens-a-service[cap-routing]: #the-open-triggers-capability-routing[binding]: #binding-to-a-component-and-sending-a-service-channel [ns-construction]：构造一个组件命名空间[service-open]：a-component-opens-a-service [cap-routing]：open-triggers-capability-routing [binding]：绑定到组件并发送服务通道

