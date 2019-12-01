 
# Scenic, the Fuchsia graphics engine  风景秀丽的樱红色图形引擎 

 
- [Scenic, the Fuchsia graphics engine](#scenic-the-fuchsia-graphics-engine)  -[Scenic，紫红色图形引擎]（scenic-the-fuchsia-graphics-engine）
- [Introduction](#introduction)  -[简介]（简介）
  - [Scenic and Fuchsia](#scenic-and-fuchsia)  -[风景和倒挂金钟]（风景和倒挂金钟）
- [Concepts](#concepts)  -[概念]（概念）
  - [Scenic](#scenic)  -[风景]（风景）
  - [Sessions](#sessions)  -[工作阶段]（工作阶段）
  - [Resources](#resources)  -[资源]（资源）
    - [Nodes](#nodes)  -[节点]（节点）
    - [Scenes](#scenes)  -[场景]（场景）
    - [Compositors](#compositors)  -[合成人]（合成人）
    - [Scenic Resource Graph](#scenic-resource-graph)  -[风景资源图]（scenic-resource-graph）
    - [TODO: More Resources](#todo-more-resources)  -[待办事项：更多资源]（待办事项更多资源）
  - [Coordinate Frames and Units](#coordinate-frames-and-units)  -[坐标框架和单位]（坐标框架和单位）
    - [Units](#units)  -[单位]（单位）
    - [World Space](#world-space)  -[世界空间]（world-space）
    - [View Space](#view-space)  -[查看空间]（view-space）
  - [Views and Bounds](#views-and-bounds)  -[视图和界限]（视图和界限）
  - [Timing Model](#timing-model)  -[计时模型]（计时模型）
  - [Fences](#fences)  -[栅栏]（栅栏）
- [Examples of using Scenic](#examples-of-using-scenic)  -[使用风景的例子]（使用风景的例子）
- [API Guide](#api-guide)  -[API指南]（API指南）
  - [FIDL protocols](#fidl-protocols)  -[FIDL协议]（fidl协议）
  - [TODO](#todo)  -[待办事项]（待办事项）

 
# Introduction {#introduction}  简介{简介} 

Scenic is a system service that composes graphical objects from multiple processes into a shared scene graph.  These objects are rendered within aunified lighting environment (to a display or other render target); thismeans that the objects can cast shadows or reflect light onto each other,even if the originating processes have no knowledge of each other. Scenic是一项系统服务，它将多个过程中的图形对象组成一个共享的场景图。这些对象在统一的照明环境中渲染（到显示器或其他渲染目标）；这意味着即使发起过程彼此不了解，对象也可以相互投射阴影或反射光。

Scenic's responsibilities are:  风景区的职责是：

 
- Composition: Scenic provides a retained-mode 3D scene graph that contains content that is independently generated and linked together by itsclients.  Composition makes it possible to seamlessly intermixthe graphical content of separately implemented UI components. -合成：Scenic提供了保留模式3D场景图，其中包含由其客户端独立生成并链接在一起的内容。合成使无缝混合单独实现的UI组件的图形内容成为可能。

 
- Animation: Scenic re-evaluates any time-varying expressions within models prior to rendering each frame, thereby enabling animation of modelproperties without further intervention from clients.  Offloadinganimations to Scenic ensures smooth jank-free transitions. -动画：Scenic在渲染每一帧之前重新评估模型中任何随时间变化的表达式，从而使模型属性具有动画效果，而无需客户端的进一步干预。将动画卸载到Scenic可以确保平滑，无垃圾的过渡。

 
- Rendering: Scenic renders its scene graph using Escher, a rendering library built on Vulkan, which applies realistic lighting and shadows tothe entire scene. -渲染：Scenic使用Escher渲染其场景图，Escher是基于Vulkan构建的渲染库，该库将逼真的照明和阴影应用于整个场景。

 
- Scheduling: Scenic schedules scene updates and animations to anticipate and match the rendering target's presentation latency and refresh interval. -计划：Scenic计划场景更新和动画以预测并匹配渲染目标的演示延迟和刷新间隔。

 
- Diagnostics: Scenic provides a diagnostic interface to help developers debug their models and measure performance. -诊断：Scenic提供了一个诊断界面，以帮助开发人员调试其模型并评估性能。

 
## Scenic and Fuchsia {#scenic-and-fuchsia}  风景名胜和倒挂金钟{scenic-and-fuchsia} 

![Diagram of Scenic within Fuchsia](meta/scenic_within_fuchsia_diagram.png)  ！[紫红色的风景图]（meta / scenic_within_fuchsia_diagram.png）

Scenic's API allows any client to insert its UI into the global scene graph. Processes using the UI framework [_Flutter_](https://flutter.io/) are oneexample; the lower layer of Flutter, called [_Flutter Engine_](https://github.com/flutter/engine),contains code responsible for communicating with Scenic. Scenic的API允许任何客户端将其UI插入全局场景图。使用UI框架[_Flutter_]（https://flutter.io/）的过程就是一个例子。 Flutter的下层称为[_Flutter Engine_]（https://github.com/flutter/engine），其中包含负责与Scenic通信的代码。

Scenic has several internal subsystems. _Gfx_ owns the scene graph and is responsible for rendering. _Input_ is responsible for routing input events to clients,which also involves coordinating gesture recognition across clients. _Anim_is a yet-to-be created system for coordinating transitions across clientsas well as offloading animations to Scenic. 风景区有几个内部子系统。 _Gfx_拥有场景图并负责渲染。 _Input_负责将输入事件路由到客户端，这还涉及在客户端之间协调手势识别。 _Anim_是一个尚待创建的系统，用于协调客户端之间的过渡以及将动画卸载到Scenic中。

[_Escher_](/src/ui/lib/escher/README.md) is a Vulkan-based rendering library used by the _Gfx_ system. [_Escher _]（/ src / ui / lib / escher / README.md）是_Gfx_系统使用的基于Vulkan的渲染库。

_Root Presenter_ is an independent service which is responsible for _presenting_ the system's UI; using the Scenic API, it creates the root of aScenic scene graph, embeds the root process's UI, and reads input eventsusing its _Input Reader_ library and continually forwards them to Scenic. _Root Presenter_是一项独立的服务，负责_presenting_系统的UI；使用Scenic API，它将创建场景场景图的根，嵌入根进程的UI，并使用其_Input Reader_库读取输入事件，并将其连续转发给Scenic。

Scenic is a client of the [_Vulkan graphics driver_](/garnet/lib/magma/) and the system _Display Driver_. Scenic是[_Vulkan图形驱动程序_]（/ garnet / lib / magma /）和系统_Display Driver_的客户端。

 
# Concepts {#concepts}  概念{concepts} 

 
## Scenic {#scenic}  风景优美的{风景名胜} 

The `Scenic` FIDL protocol is Scenic's front door.  Each instance of the protocol represents a Scenic instance. Each Scenic instance is an isolatedrendering context with its own content, render targets, and scheduling loop. “ Scenic” FIDL协议位于Scenic的前门。协议的每个实例代表一个Scenic实例。每个Scenic实例都是一个隔离的渲染上下文，具有自己的内容，渲染目标和调度循环。

The `Scenic` protocol allows a client to create a [`Session`](#session) which is the communication channel used to publish graphical content to this instance. “场景”协议允许客户端创建一个“会话”（会话），该会话是用于将图形内容发布到该实例的通信通道。

A single Scenic instance can update, animate, and render multiple `Scenes` (trees of graphical objects) to multiple targets in tandem on the samescheduling loop.  This means that the timing model for a Scenic instanceis _coherent_: all of its associated content belongs to the same schedulingdomain and can be seamlessly intermixed. 单个Scenic实例可以在同一调度循环上一前一后地将多个“ Scenes”（图形对象树）更新，制作动画并渲染到多个目标。这意味着Scenic实例的时序模型是“连续的”：其所有关联内容都属于同一调度域，并且可以无缝地混合。

In practice, there is one instance of Scenic and one Scene that is rendered to a target. However, creating separate Scenic instances can be useful for renderingto targets which have very different scheduling requirements or for runningtests in isolation. Independent Scenic instances cannot share content and aretherefore not coherent amongst themselves. 在实践中，有一个场景实例和一个场景渲染到目标。但是，创建单独的Scenic实例对于渲染到具有非常不同的调度要求的目标或单独运行测试很有用。独立的Scenic实例无法共享内容，因此彼此之间也不协调。

When a Scenic instance is destroyed, all of its sessions become inoperable and its rendering ceases. 当一个Scenic实例被销毁时，其所有会话都将无法使用，并且其渲染也将停止。

`Views` typically do not deal with the Scenic instance directly; instead they receive a Scenic `Session` from the view manager. “视图”通常不会直接处理Scenic实例；取而代之的是，他们从视图管理器收到一个“风景优美的会话”。

 
## Sessions {#sessions}  会话{sessions} 

The `Session` FIDL protocol is the primary API used by clients of Scenic to contribute graphical content in the form of `Resources`.  Each session hasits own resource table and is unable to directly interact with resourcesbelonging to other sessions. 会话FIDL协议是Scenic客户端使用的主要API，以“资源”的形式提供图形内容。每个会话都有其自己的资源表，并且无法直接与属于其他会话的资源进行交互。

Each session provides the following operations:  每个会话提供以下操作：

 
- Submit operations to add, remove, or modify resources.  -提交操作以添加，删除或修改资源。
- Commit a sequence of operations to be presented atomically.  -提交一系列操作，以原子方式呈现。
- Awaiting and signaling fences.  -等待和发信号围栏。
- Schedule subsequent frame updates.  -安排后续框架更新。
- Form links with other sessions (by mutual agreement).  -与其他会议建立链接（经双方同意）。

When a session is destroyed, all of its resources are released and all of its links become inoperable. 当会话被销毁时，其所有资源都将被释放，并且其所有链接都将无法使用。

`Views` typically receive separate sessions from the view manager.  “视图”通常会从视图管理器接收单独的会话。

 
## Resources {#resources}  资源{resources} 

`Resources` represent scene elements such as nodes, shapes, materials, and animations which belong to particular `Sessions`. “资源”代表属于特定“会话”的场景元素，例如节点，形状，材质和动画。

The list of Scenic resources is described by the API: [//sdk/fidl/fuchsia.ui.gfx/resources.fidl](/sdk/fidl/fuchsia.ui.gfx/resources.fidl) 风景名胜资源列表由API描述：[//sdk/fidl/fuchsia.ui.gfx/resources.fidl](/sdk/fidl/fuchsia.ui.gfx/resources.fidl）

Clients of Scenic generate graphical content to be rendered by queuing and submitting operations to add, remove, or modify resources within theirsession. Scenic的客户端通过排队和提交操作来添加，删除或修改会话中的资源，从而生成要呈现的图形内容。

Each resource is identified within its session by a locally unique id which is assigned by the owner of the session (by arbitrary means).  Sessionscannot directly refer to resources which belong to other sessions (even ifthey happen to know their id) therefore content embedding between sessionsis performed using `Link` objects as intermediaries. 每个资源在其会话中都由会话所有者（通过任意方式）分配的本地唯一ID进行标识。会话不能直接指代属于其他会话的资源（即使它们碰巧知道它们的ID），因此在使用“链接”对象作为中介的会话之间嵌入内容。

To add a resource, perform the following steps:  要添加资源，请执行以下步骤：

 
- Enqueue an operation to add a resource of the desired type and assign it a locally unique id within the session. -排队操作以添加所需类型的资源，并在会话中为其分配本地唯一ID。
- Enqueue one or more operations to set that resource's properties given its id. -赋予一个或多个操作以给定其ID设置该资源的属性。

Certain more complex resources may reference the ids of other resources within their own definition.  For instance, a `Node` references its `Shape`thus the `Shape` must be added before the `Node` so that the node mayreference it as part of its definition. 某些更复杂的资源可能会在其自己的定义内引用其他资源的ID。例如，“节点”引用其“形状”，因此必须在“节点”之前添加“形状”，以便该节点可以将其引用作为其定义的一部分。

To modify a resource, enqueue one or more operations to set the desired properties in the same manner used when the resource was added. 要修改资源，请以添加资源时所使用的相同方式，对一个或多个操作进行排队以设置所需的属性。

The remove a resource, enqueue an operation to remove the resource.  删除资源，排队删除资源的操作。

Removing a resource causes its id to become available for reuse.  However, the session maintains a reference count for each resource which isinternally referenced.  The underlying storage will not be released (andcannot be reused) until all remaining references to the resource have beencleared *and* until the next frame which does not require the resource hasbeen presented.  This is especially important for `Memory` resources.See also [Fences](#fences). 删除资源会导致其ID可供重用。但是，会话维护内部引用的每个资源的引用计数。直到所有剩余的对资源的引用已被清除*，并且*直到下一个不需要该资源的帧出现为止，基础存储才会被释放（并且不能被重用）。这对于“内存”资源尤其重要。另请参见[Fences]（fences）。

This process of addition, modification, and removal may be repeated indefinitely to incrementally update resources within a session. 可以无限地重复此添加，修改和删除过程，以递增地更新会话中的资源。

 
### Nodes {#nodes}  节点{nodes} 

A `Node` resource represents a graphical object which can be assembled into a hierarchy called a `node tree` for rendering. “节点”资源代表一个图形对象，可以将其组装成称为“节点树”的层次结构以进行渲染。

[Here](scenic_resource_lifecycle.md) is a walk-through on how Scenic internally manages the lifecycle of Node-like resources and embedded Views. [here]（scenic_resource_lifecycle.md）是Scene的内部演练，介绍了Scenic如何在内部管理类节点资源和嵌入式View的生命周期。

TODO: Discuss this in more detail, especially hierarchical modeling concepts such as per-node transforms, groups, adding and removing children, etc. TODO：对此进行更详细的讨论，尤其是层次化建模概念，例如每个节点的变换，组，添加和删除子级等。

 
### Scenes {#scenes}  场景{场景} 

A `Scene` resource combines a tree of nodes with the scene-wide parameters needed to render it.  A Scenic instance may contain multiple scenes buteach scene must have its own independent tree of nodes. “场景”资源将节点树与渲染该场景所需的场景范围参数组合在一起。风景实例可能包含多个场景，但是每个场景必须具有其自己的独立节点树。

A scene resource has the following properties:  场景资源具有以下属性：

 
- The scene's root node.  -场景的根节点。
- The scene's global parameters such as its lighting model.  -场景的全局参数，例如其光照模型。

In order to render a scene, a `Camera` must be pointed at it.  为了渲染场景，必须将“相机”指向该场景。

 
### Compositors {#compositors}  合成人{compositors} 

Compositors are resources that come in two flavors: `DisplayCompositor` and `ImagePipeCompositor`; their job is to draw the content of a `LayerStack`into their render target.  For `DisplayCompositor`, the target display mayhave multiple hardware overlays; in this case the compositor may chooseassociate each of these with a separate layer, rather than flattening thelayers into a single image. 合成器是具有两种形式的资源：“ DisplayCompositor”和“ ImagePipeCompositor”；他们的工作是将LayerStack的内容绘制到渲染目标中。对于“ DisplayCompositor”，目标显示器可能具有多个硬件覆盖图；在这种情况下，合成者可以选择将每个层与单独的层相关联，而不是将层展平为单个图像。

A `LayerStack` resource consists of an ordered list of `Layers`.  Each layer can contain either an `Image` (perhaps transformed by a matrix), or a`Camera` that points at a `Scene` to be rendered (as described above). “ LayerStack”资源由“ Layers”的有序列表组成。每层都可以包含一个“图像”（可能通过矩阵进行转换），或一个“相机”，它指向要渲染的“场景”（如上所述）。

 
### Scenic Resource Graph {#scenic-resource-graph}  风景资源图{scenic-resource-graph} 

![Scenic Resource Graph](meta/scenic_resource_graph.png)  ！[风景资源图]（meta / scenic_resource_graph.png）

 
### TODO: More Resources {#todo-more-resources}  待办事项：更多资源{todo-more-resources} 

Add sections to discuss all other kinds of resources: shapes, materials, links, memory, images, buffers, animations, variables, renderers etc. 添加部分以讨论所有其他类型的资源：形状，材质，链接，内存，图像，缓冲区，动画，变量，渲染器等。

 
## Coordinate Frames and Units {#coordinate-frames-and-units}  坐标框架和单位{coordinate-frames and-units} 

Scenic manages a global scene graph in a three dimensional space. Some of the characteristics of this space are defined by Scenic itself, whereas some are defined by the root presenter or evenother clients. Scenic在三维空间中管理全局场景图。该空间的某些特征是由Scenic本身定义的，而某些特征是由根演示者或其他客户定义的。

![Scenic Axes](meta/scenic_axes.png)  ！[风景斧]（meta / scenic_axes.png）

 
### Units {#units}  单位{units} 

Units are configured by the root presenter. The default root presenter uses a device-independent scalable unit called "pips" for the root space. See [Units and Metrics](units_and_metrics.md) fordetails. What units are used for your view space depends on what transforms are applied to yourview by your parent. 单位由根演示者配置。默认的根表示器将与设备无关的可伸缩单元称为“ pips”作为根空间。有关详细信息，请参见[Units and Metrics]（units_and_metrics.md）。视图空间使用的单位取决于父级对视图应用的转换。

 
### World Space {#world-space}  世界空间{world-space} 

The Scenic world space is a right handed Cartesian space. It is configured by the root presenter which configures the view and projection parameters of the camera. The default root presenterwill put the origin at the top left of the screen and make +X point right, +Y point down, and+Z point into the screen. 风景世界空间是右手笛卡尔空间。它由根演示者配置，根演示者配置摄像机的视图和投影参数。默认的根目录演示者会将原点放在屏幕的左上方，并使+ X指向右，+ Y指向下，+ Z指向屏幕。

 
### View Space {#view-space}  检视空间{view-space} 

Ultimately the space of a given view depends on what transforms are applied to it by its parent View and the parent View's parent and so on. If no rotation transform is applied and all scaletransforms are positive along all axes then the View's axes will align with the axes of the rootpresenter and the handedness will match. 最终，给定视图的空间取决于其父视图和父视图的父视图对其应用了哪些转换等。如果未应用旋转变换，并且所有比例变换在所有轴上均为正，则视图的轴将与根表示者的轴对齐，并且惯用性将匹配。

The bounds of the root view are defined by a min and a max point as follows:  根视图的范围由一个最小点和一个最大点定义，如下所示：

![Scenic Root View Bounds](meta/scenic_root_view_bounds.png)  ！[Scenic Root View Bounds]（meta / scenic_root_view_bounds.png）

 
## Views and Bounds {#views-and-bounds}  视图和范围{views-and-bounds} 

[View Bounds](view_bounds.md) shows how to set up your view bounds, how to debug them with wireframe rendering, and explains how view bounds interact with hit testing. [View Bounds]（view_bounds.md）显示了如何设置您的视图边界，如何使用线框渲染调试它们，并说明了视图边界如何与点击测试相互作用。

 

 
## Timing Model {#timing-model}  时序模型{timing-model} 

[Life of a Pixel](life_of_a_pixel.md) shows how a client Present request is integrated into a Scenic frame. [像素的生命]（life_of_a_pixel.md）显示了客户端Present请求如何集成到“风景”框架中。

TODO(SCN-1202): Talk about scheduling frames, presentation timestamps, etc.  TODO（SCN-1202）：讨论计划帧，演示时间戳等。

 
## Fences {#fences}  围栏{fences} 

TODO(SCN-1228): Talk about synchronization.  TODO（SCN-1228）：讨论同步。

 
# Examples of using Scenic {#examples-of-using-scenic}  使用风景区的示例{场景使用示例} 

A simple example of using Scenic is the [bouncing ball](/src/ui/examples/bouncing_ball/README.md) app.  使用“风景”的一个简单示例是[弹跳球]（/ src / ui / examples / bouncing_ball / README.md）应用程序。

 
# API Guide {#api-guide}  API指南{api-guide} 

 
## FIDL protocols {#fidl-protocols}  FIDL协议{fidl-protocols} 

The following files define and document the collection of FIDL protocols that make up Scenic. 以下文件定义并记录了构成Scenic的FIDL协议的集合。

 
* [Scenic top-level protocols](/sdk/fidl/fuchsia.ui.scenic) (`fuchsia.ui.scenic`)  * [Scenic顶级协议]（/ sdk / fidl / fuchsia.ui.scenic）（`fuchsia.ui.scenic`）
  * [scenic.fidl](/sdk/fidl/fuchsia.ui.scenic/scenic.fidl)  * [scenic.fidl]（/ sdk / fidl / fuchsia.ui.scenic / scenic.fidl）
  * [session.fidl](/sdk/fidl/fuchsia.ui.scenic/session.fidl)  * [session.fidl]（/ sdk / fidl / fuchsia.ui.scenic / session.fidl）
  * [commands.fidl](/sdk/fidl/fuchsia.ui.scenic/commands.fidl)  * [commands.fidl]（/ sdk / fidl / fuchsia.ui.scenic / commands.fidl）
  * [events.fidl](/sdk/fidl/fuchsia.ui.scenic/events.fidl)  * [events.fidl]（/ sdk / fidl / fuchsia.ui.scenic / events.fidl）

 
* [Gfx](/sdk/fidl/fuchsia.ui.gfx) (`fuchsia.ui.gfx`)  * [Gfx]（/ sdk / fidl / fuchsia.ui.gfx）（`fuchsia.ui.gfx`）
  * [commands.fidl](/sdk/fidl/fuchsia.ui.gfx/commands.fidl)  * [commands.fidl]（/ sdk / fidl / fuchsia.ui.gfx / commands.fidl）
  * [events.fidl](/sdk/fidl/fuchsia.ui.gfx/events.fidl)  * [events.fidl]（/ sdk / fidl / fuchsia.ui.gfx / events.fidl）
  * [resources.fidl](/sdk/fidl/fuchsia.ui.gfx/resources.fidl)  * [resources.fidl]（/ sdk / fidl / fuchsia.ui.gfx / resources.fidl）
  * [nodes.fidl](/sdk/fidl/fuchsia.ui.gfx/nodes.fidl)  * [nodes.fidl]（/ sdk / fidl / fuchsia.ui.gfx / nodes.fidl）
  * [shapes.fidl](/sdk/fidl/fuchsia.ui.gfx/shapes.fidl)  * [shapes.fidl]（/ sdk / fidl / fuchsia.ui.gfx / shapes.fidl）
  * [...](/sdk/fidl/fuchsia.ui.gfx)  * [...]（/ sdk / fidl / fuchsia.ui.gfx）

 
* [Views](/sdk/fidl/fuchsia.ui.views) (`fuchsia.ui.views`)  * [查看次数]（/ sdk / fidl / fuchsia.ui.views）（`fuchsia.ui.views`）
  * [commands.fidl](/sdk/fidl/fuchsia.ui.views/commands.fidl)  * [commands.fidl]（/ sdk / fidl / fuchsia.ui.views / commands.fidl）

 
* [Input](/sdk/fidl/fuchsia.ui.input) (`fuchsia.ui.input`)  * [输入]（/ sdk / fidl / fuchsia.ui.input）（`fuchsia.ui.input`）
  * [commands.fidl](/sdk/fidl/fuchsia.ui.input/commands.fidl)  * [commands.fidl]（/ sdk / fidl / fuchsia.ui.input / commands.fidl）
  * [input_events.fidl](/sdk/fidl/fuchsia.ui.input/input_events.fidl)  * [input_events.fidl]（/ sdk / fidl / fuchsia.ui.input / input_events.fidl）

 
* [Policy](/sdk/fidl/fuchsia.ui.policy) (`fuchsia.ui.policy`)  * [政策]（/ sdk / fidl / fuchsia.ui.policy）（`fuchsia.ui.policy`）
  * [presenter.fidl](/sdk/fidl/fuchsia.ui.policy/presenter.fidl)  * [presenter.fidl]（/ sdk / fidl / fuchsia.ui.policy / presenter.fidl）
  * [presentation.fidl](/sdk/fidl/fuchsia.ui.policy/presentation.fidl)  * [presentation.fidl]（/ sdk / fidl / fuchsia.ui.policy / presentation.fidl）
  * [...](/sdk/fidl/fuchsia.ui.policy)  * [...]（/ sdk / fidl / fuchsia.ui.policy）

 
* [App](/sdk/fidl/fuchsia.ui.app) (`fuchsia.ui.app`)  * [App]（/ sdk / fidl / fuchsia.ui.app）（`fuchsia.ui.app`）
  * [view_provider.fidl](/sdk/fidl/fuchsia.ui.app/view_provider.fidl)  * [view_provider.fidl]（/ sdk / fidl / fuchsia.ui.app / view_provider.fidl）

 
* [experimental] [Vectorial](/sdk/fidl/fuchsia.ui.vectorial) (`fuchsia.ui.vectorial`)  * [实验性] [向量]（/ sdk / fidl / fuchsia.ui.vectorial）（`fuchsia.ui.vectorial`）

 
## TODO {#todo}  待办事项{todo} 

