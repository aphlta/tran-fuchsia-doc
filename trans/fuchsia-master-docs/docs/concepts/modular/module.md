 
## Modules  模组 

A `Module` is a component which displays UI and runs as part of a `Story`.  “模块”是显示UI并作为“故事”的一部分运行的组件。

Multiple modules can be composed into a single story, and modules can add other modules to the story they are part of. Module's can either embed other moduleswithin their own content, or they can delegate visual composition to the`StoryShell`. 可以将多个模块组合成一个故事，并且模块可以将其他模块添加到它们所属的故事中。模块可以将其他模块嵌入自己的内容中，也可以将视觉合成委托给“ StoryShell”。

 
### Environment  环境 

A module is given access to two services provided by the modular framework in its incoming namespace: 一个模块可以在其传入名称空间中访问模块化框架提供的两个服务：

 
*   `fuchsia.modular.ComponentContext` which gives the agent access to functionality which is shared across components run under the modularframework (e.g. modules, shells, agents). *`fuchsia.modular.ComponentContext`，使代理能够访问在模块化框架下运行的组件（例如模块，外壳，代理）之间共享的功能。
*   `fuchsia.modular.ModuleContext` which gives modules access to module specific functionality, like adding other modules to its story and creatingentities. *`fuchsia.modular.ModuleContext`允许模块访问模块特定的功能，例如向其故事和创建实体添加其他模块。

A module is expected to provide three services to the modular framework in its outgoing namespace: 预计模块将在其传出名称空间中为模块化框架提供三项服务：

 
*   `fuchsia.ui.app.ViewProvider` which is used to display the module's UI.  *`fuchsia.ui.app.ViewProvider`，用于显示模块的UI。
*   `fuchsia.modular.Lifecycle` which allows the framework to signal the module to terminate gracefully. *`fuchsia.modular.Lifecycle`，允许框架发信号通知模块正常终止。
*   `fuchsia.modular.IntentHandler` which allows the framework to send [intents](intent.md) to the module. *`fuchsia.modular.IntentHandler`，它允许框架发送[intents]（intent.md）到模块。

 
### Lifecycle  生命周期 

A module's lifecycle is bound to the lifecycle of the story it is part of. In addition, a given module can have multiple running instances in a single story. 模块的生命周期与模块所属故事的生命周期绑定在一起。此外，一个给定的模块可以在一个故事中包含多个正在运行的实例。

When a module starts another module it is given a module controller which it can use to control the lifecycle of the started module. 当一个模块启动另一个模块时，会得到一个模块控制器，它可以用来控制启动模块的生命周期。

 
### Communication Mechanisms  沟通机制 

