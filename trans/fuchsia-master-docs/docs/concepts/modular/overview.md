 
## Overview  总览 

Modular is the application framework for Fuchsia. It manages user experiences by composing UI, data, and users from a diverse set of components into logical andvisual containers called Stories. 模块化是紫红色的应用程序框架。它通过将UI，数据和用户（来自不同组件的集合）组合到称为Stories的逻辑和可视容器中来管理用户体验。

The framework defines classes of components to extend user experiences and provides software primitives for component composition, communication, taskdelegation, state management and data sharing. 该框架定义了组件类别以扩展用户体验，并提供了用于组件组成，通信，任务委托，状态管理和数据共享的软件原语。

 
### Requirements to use Modular  使用模块化的要求 

Modular supports software written in any language (e.g. Flutter, C++) for any Fuchsia supported runtime, as long as it is a Fuchsia Component. 只要是Fuchsia组件，Modular就可以为任何Fuchsia支持的运行时支持以任何语言（例如Flutter，C ++）编写的软件。

The Modular Framework communicates with components it launches via FIDL, the standard IPC mechanism for Fuchsia. 模块化框架通过FIDL（紫红色的标准IPC机制）与其启动的组件进行通信。

 
### Extension Points  延伸点 

The framework defines several different classes of components which can be implemented by developers to extend the behavior of user experiences: 该框架定义了几种不同类别的组件，开发人员可以使用这些组件来扩展用户体验的行为：

 
1.  [Modules](module.md) are components which display UI and are visually composed in a [Story](story.md). 1. [Modules]（module.md）是显示UI并在[Story]（story.md）中以视觉方式组成的组件。
1.  [Agents](agent.md) are components which run in the background to provide services and data to Modules and other Agents. 1. [Agents]（agent.md）是在后台运行的组件，用于向模块和其他代理提供服务和数据。
1.  [Shells](shell.md) manage system UI and mediate user interactions.  1. [Shells]（shell.md）管理系统UI并中介用户交互。
1.  [EntityProviders](entity.md) are components which provide access to data object (entities) which are shared between components running in modular. 1. [EntityProviders]（entity.md）是提供对数据对象（实体）的访问的组件，这些数据对象在以模块化方式运行的组件之间共享。

 
### `basemgr` and `sessionmgr`  `basemgr`和`sessionmgr` 

After Fuchsia device startup, `basemgr` and `sessionmgr` are processes that provide session management, component lifecycle management and state management. 在倒挂金钟设备启动后，“ basemgr”和“ sessionmgr”是提供会话管理，组件生命周期管理和状态管理的过程。

 
*   `basemgr` is responsible for user authentication and authorization. It leverages the Base Shell to present UI. *`basemgr`负责用户认证和授权。它利用Base Shell来呈现UI。

 
*   `sessionmgr` is responsible for the lifecycle of Stories, Modules and Agents, as well as service and state coordination between them.It leverages Session and Story Shells to manage the visual composition ofthese components. *`sessionmgr`负责故事，模块和代理的生命周期，以及它们之间的服务和状态协调。它利用会话和故事壳来管理这些组件的外观。

 
### Read More  阅读更多 

 
