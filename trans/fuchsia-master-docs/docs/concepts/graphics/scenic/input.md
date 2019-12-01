 
# Scenic Input System  景区输入系统 

This document describes how RootPresenter and Scenic process visually-related input, such as touch, mouse, and keyboard. We'll work roughly bottom up throughthe layers of abstraction, from device to gesture. 本文档介绍了RootPresenter和Scenic如何处理与视觉相关的输入，例如触摸，鼠标和键盘。我们将从设备到手势的抽象层大致进行自下而上的工作。

Other inputs, such as buttons, audio, and video, are out of scope for this document. 其他输入（例如按钮，音频和视频）不在本文档的讨论范围之内。

 
## Major Entities and Their High-Level Role  主要实体及其高级角色 

Zircon - gives us inputs as HID reports.  Zircon-给我们提供输入作为HID报告。

RootPresenter - routes input from Zircon to Scenic  RootPresenter-从Zircon到Scenic的路线输入

Scenic - routes input from RootPresenter to UI Clients (touch and mouse inputs), and from RootPresenter to TextService (text inputs only). 风景区-将输入从RootPresenter路由到UI客户端（触摸和鼠标输入），从RootPresenter路由到TextService（仅文本输入）。

TextService - routes text input from Scenic to IME  TextService-将文本输入从Scenic路由到IME

IME - routes and transforms text input from TextService to UI Clients  IME-将文本输入从TextService路由并转换到UI客户端

UI Client - consumes inputs from Scenic and IMEs to drive UI  UI客户端-使用Scenic和IME的输入来驱动UI

 
## Zircon Sends Raw Inputs  锆石发送原始输入 

Zircon provides access to input peripherals through the file system under `/dev/class/input`. These are presented as HID devices, with associated controlsto retrieve the description report. Simple reads from these HID devices willreturn HID reports, which generally are expected to follow the[HID Usage Tables](https://www.usb.org/document-library/hid-usage-tables-112). Zircon通过“ / dev / class / input”下的文件系统提供对输入外围设备的访问。这些以HID设备的形式显示，并带有关联的控件以检索描述报告。从这些HID设备的简单读取将返回HID报告，通常希望这些报告遵循[HID使用表]（https://www.usb.org/document-library/hid-usage-tables-112）。

 
## RootPresenter Transforms and Routes Inputs  RootPresenter转换和路由输入 

Generally, the RootPresenter is the singleton process that has detailed and specific knowledge about the entire device, such as details about the display,peripherals, sensors, etc. It takes care of device management details, such asreading out HID reports from Zircon, and packages them into FIDL structs forconsumption by Scenic or other entities. 通常，RootPresenter是具有整个设备详细和特定知识的单例过程，例如有关显示器，外围设备，传感器等的详细信息。它负责设备管理的详细信息，例如从Zircon读取HID报告和程序包将它们转换成FIDL结构以供Scenic或其他实体消费。

It also instructs Scenic to create the top-level (or "root") elements of the scene graph, and vends the[Presenter API](/sdk/fidl/fuchsia.ui.policy/presenter.fidl)that UI clients use to attach their visual content to the scene graph. 它还指示Scenic创建场景图的顶层（或“根”）元素，并出售UI客户端用于的[Presenter API]（/ sdk / fidl / fuchsia.ui.policy / presenter.fidl）。将其视觉内容附加到场景图。

The general transformation for an input event through RootPresenter is from HID report, to[`InputReport`](/sdk/fidl/fuchsia.ui.input/input_reports.fidl),to[`InputEvent`](/sdk/fidl/fuchsia.ui.input/input_events.fidl).The `InputEvent` is sent to Scenic. 通过RootPresenter对输入事件进行的一般转换是从HID报告转换为[`InputReport`]（/ sdk / fidl / fuchsia.ui.input / input_reports.fidl），到[`InputEvent`]（/ sdk / fidl / fuchsia .ui.input / input_events.fidl）。“ InputEvent”被发送到Scenic。

 
### Implementation  实作 

The [`InputReader` library](/src/ui/lib/input_reader/)is the code responsible for actually monitoring `/dev/class/input` for newperipherals, and reacting to new reports from existing peripherals. It forwardsnew events for processing to other parts of RootPresenter.More information on `InputReader` can be found[here](/src/ui/lib/input_reader/README.md). [`InputReader`库]（/ src / ui / lib / input_reader /）是负责实际监视/ dev / class / input新外围设备并响应来自现有外围设备的新报告的代码。它会将新事件转发给RootPresenter的其他部分。有关InputInputer的更多信息，请参见[此处]（/ src / ui / lib / input_reader / README.md）。

For each new peripheral (an input device), `InputReader` assigns a new `InputInterpreter` object that reads the HID descriptor report for a singleinput device, and performs bookkeeping by pushing a[`DeviceDescriptor`](/sdk/fidl/fuchsia.ui.input/input_reports.fidl)and its designated event forwarding channel, an[`InputDevice`](/sdk/fidl/fuchsia.ui.input/input_device_registry.fidl#17),to the[`InputDeviceRegistry`](/sdk/fidl/fuchsia.ui.input/input_device_registry.fidl#12)FIDL protocol. (The `InputDeviceRegistry` protocol also enables programmaticinput injection from outside RootPresenter.) The `InputDeviceRegistry` protocolis vended by RootPresenter, and in addition to bookkeeping (details below),informs each `Presentation` about the new peripheral. 对于每个新的外围设备（输入设备），InputReader分配一个新的InputInterpreter对象，该对象读取单个输入设备的HID描述符报告，并通过按下DeviceRescriptor来执行簿记。（/ sdk / fidl / fuchsia）。 ui.input / input_reports.fidl）及其指定的事件转发通道，将[InputDevice`]（/ sdk / fidl / fuchsia.ui.input / input_device_registry.fidl17）发送至[`InputDeviceRegistry`]（/ sdk / fidl /fuchsia.ui.input/input_device_registry.fidl12)FIDL协议。 （“ InputDeviceRegistry”协议还允许从RootPresenter外部进行程序化的输入注入。）“ InputDeviceRegistry”协议由RootPresenter进行销售，除了簿记（以下详细信息）之外，还向每个“ Presentation”通知有关新外围设备的信息。

For each new event, `InputInterpreter` reads and decodes a HID report, transforms it into an `InputReport`, and forwards it on`InputDevice::DispatchReport`. 对于每个新事件，“ InputInterpreter”会读取并解码HID报告，将其转换为“ InputReport”，然后在InputDevice :: DispatchReport上转发。

The [implementation of `DispatchReport`](/src/lib/ui/input/input_device_impl.h)forwards the `InputReport` to the registered `InputDeviceImpl::Listener`,typically the RootPresenter itself. In turn, the `InputReport` is forwarded tothe active `Presentation`. [DispatchReport`的实现]（/ src / lib / ui / input / input_input_device_impl.h）将InputReport传递给已注册的InputDeviceImpl :: Listener，通常是RootPresenter本身。依次地，将“ InputReport”转发到活动的“ Presentation”。

For internal bookkeeping, each `Presentation` keeps a mapping of `InputDevice` ID to an associated `DeviceState`. The `DeviceState` is used to create a littlepersistent state for each peripheral, e.g., keeping track of a mouse device'sDOWN/MOVE/UP state. In `Presentation`, the `InputReport` is routed to itsrelevant `DeviceState`, where it is transformed into an appropriate`InputEvent`, and is sent to the `OnEventCallback` that was registered at the`DeviceState`'s constructor (when the peripheral was first added). 对于内部簿记，每个“ Presentation”都会保留一个“ InputDevice” ID到关联的“ DeviceState”的映射。 DeviceState用于为每个外围设备创建一点持久的状态，例如，跟踪鼠标设备的DOWN / MOVE / UP状态。在“演示文稿”中，“ InputReport”被路由到与其相关的“ DeviceState”，在此它被转换成适当的“ InputEvent”，并被发送到在“ DeviceState”的构造函数中注册的“ OnEventCallback”（当首先添加外围设备）。

The `InputEvent` is now handled by RootPresenter's `OnEvent` callback. It looks for global hooks, displays a mouse cursor, adjusts for predetermined screenrotation, and finally enqueues the `InputEvent` as an `InputCmd` to Scenic. 输入事件现在由RootPresenter的OnEvent回调处理。它寻找全局钩子，显示鼠标光标，为预定的屏幕旋转进行调整，最后将InputEvent作为InputCmd排队到Scenic。

 
### Sensor Inputs  传感器输入 

Sensor HID reports are handled in an analogous fashion. Some differences are:  传感器HID报告以类似的方式处理。一些区别是：

 
*   Sensors typically don't have state to manage, so they have no `DeviceState`.  *传感器通常没有要管理的状态，因此它们没有“ DeviceState”。
*   The `InputReport` is typically enough for plumbing out to clients.  *通常，“ InputReport”足以满足客户需求。
*   Interfaces for sensor data is vended by RootPresenter itself; this may change in the future. *传感器数据接口由RootPresenter本身提供；将来可能会改变。

 
## Scenic Routes Inputs to UI Clients  UI客户端的风景路线输入 

In contrast to RootPresenter, Scenic has less knowledge about the device. Instead of knowing about peripherals, it receives `InputEvent` FIDL structs fromRootPresenter. Generally, it owns and manages the large-scale visual elementsthat each UI client creates (the scene graph), as well as handling inputdispatch to each UI client. 与RootPresenter相比，Scenic对设备的了解较少。它不知道外围设备，而是从RootPresenter接收“ InputEvent” FIDL结构。通常，它拥有和管理每个UI客户端创建的大规模视觉元素（场景图），以及处理向每个UI客户端的输入调度。

Scenic accepts commands from a client over its session. RootPresenter is a privileged client that may submit input commands, each of which encapsulates an`InputEvent`. The Scenic-side implementation of session logic has an[`InputCommandDispatcher`](/src/ui/scenic/lib/input/input_system.h)that farms out different types of events to appropriate dispatch logic. Scenic在其会话期间接受来自客户端的命令。 RootPresenter是一个特权客户端，可以提交输入命令，每个命令都封装一个InputEvent。会话逻辑的风景级端实现具有一个[`InputCommandDispatcher`]（/ src / ui / scenic / lib / input / input_system.h），可将不同类型的事件植入适当的调度逻辑中。

We outline some representative event flows below.  我们在下面概述了一些代表性事件流。

 
### Pointer Event Handling  指针事件处理 

Pointer events, such as touch, typically follow an ADD &rarr; DOWN &rarr; MOVE\* &rarr; UP &rarr; REMOVE state sequence, encoded as[`PointerEventPhase`](/sdk/fidl/fuchsia.ui.input/input_events.fidl). 指针事件（例如触摸）通常遵循ADD rarr； DOWN rarr; MOVE \ * rarr; UP rarr;删除状态序列，编码为[`PointerEventPhase`]（/ sdk / fidl / fuchsia.ui.input / input_events.fidl）。

On ADD, we identify the set of potential clients by performing a hit test, and forward this event to these clients. To associate future touch events by thesame finger to the same clients, we track the set of clients for that particularfinger. Parallel dispatch is used to enable gesture disambiguation (TBD), wherethe touch events should eventually be owned by a single client. 在ADD上，我们通过执行点击测试来确定一组潜在客户，并将此事件转发给这些客户。为了将同一根手指未来的触摸事件关联到同一客户，我们跟踪该特定手指的客户集。并行调度用于启用手势歧义消除（TBD），其中触摸事件最终应归单个客户端所有。

On DOWN, we send a `FocusEvent` to the single client that is "on top". We also send a `FocusEvent` with `focused=false` to the previously focused client. 在DOWN时，我们向“顶部”的单个客户端发送一个“ FocusEvent”。我们还向先前关注的客户端发送一个带有focused = false的FocusEvent。

On MOVE and UP, we merely forward them to existing clients.  在MOVE和UP上，我们仅将它们转发给现有客户。

On REMOVE, we forward it to existing clients, and then remove the tracking association. 在REMOVE上，我们将其转发到现有客户端，然后删除跟踪关联。

For an overview of pointer coordinate mapping, see [Ray Casting and Hit Testing](view_bounds.md#ray-casting-and-hit-testing).  有关指针坐标映射的概述，请参见[射线投射和命中测试]（view_bounds.mdray-casting-and-hit-testing）。

 
### Keyboard Event Handling  键盘事件处理 

Keyboard events are a little more involved, due to the need for mediation by an IME ("soft keyboard"). We distinguish *hard* key events, generated by a physicalkeyboard, from *soft* key events, generated by an IME. 由于需要通过IME（“软键盘”）进行调解，因此涉及到键盘事件的情况要多一些。我们将物理键盘产生的*硬键事件与IME产生的*软键事件区分开。

Scenic deals exclusively with hard key events, but must typically not forward them directly to clients. Instead, Scenic sends all hard key events to theTextService, which vends IMEs to UI clients. The TextService routes hard keyevents to an IME associated with a particular UI client that has received the`FocusEvent`. 风景优美的交易仅处理硬键事件，但通常不得直接将其转发给客户。相反，Scenic将所有硬键事件发送到TextService，后者将IME出售给UI客户端。 TextService将硬键事件路由到与已收到“ FocusEvent”的特定UI客户端关联的IME。

