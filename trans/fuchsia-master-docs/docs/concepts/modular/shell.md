 
## Shells  炮弹 

Shells are components which are responsible for composing UI. There are three shells: 外壳是负责组成UI的组件。有三个外壳：

 
*   `BaseShell` displays UI associated with a device, prior to a session being started. *`BaseShell`在启动会话之前显示与设备关联的UI。
*   `SessionShell` displays the UI associated with a given session (e.g. list of stories, settings UI). *`SessionShell`显示与给定会话相关的UI（例如，故事列表，设置UI）。
*   `StoryShell` displays a single story (i.e. the composition of the modules in a story, each story gets its own `StoryShell` instance). *`StoryShell`显示单个故事（即故事中模块的组成，每个故事都有自己的`StoryShell`实例）。

 
### Environment  环境 

A shell is given access to two services provided by the modular framework in its incoming namespace: 允许外壳访问模块框架在其传入名称空间中提供的两个服务：

 
*   `fuchsia.modular.ComponentContext` gives the agent access to functionality which is shared across components run under the modular framework (e.g.modules, shells, agents). *`fuchsia.modular.ComponentContext`使代理能够访问在模块化框架下运行的组件之间共享的功能（例如，模块，外壳，代理）。
*   `fuchsia.modular.[Base,Session,Story]ShellContext` gives access to shell specific functionality for each type of shell, respectively. *`fuchsia.modular。[Base，Session，Story] ​​ShellContext`分别为每种类型的外壳提供对外壳特定功能的访问。

A shell is expected to provide two services to the modular framework in its outgoing namespace: 外壳程序应在其传出名称空间中为模块化框架提供两项服务：

 
*   `fuchsia.modular.[Base,Session,Story]Shell` the modular framework uses to communicate requests to display UI. *`fuchsia.modular。[Base，Session，Story] ​​Shell`模块化框架用于传达显示UI的请求。
*   `fuchsia.modular.Lifecycle` allows the framework to signal the shell to terminate gracefully. *`fuchsia.modular.Lifecycle`允许框架向外壳发出信号以优雅地终止。

 
### Lifecycle  生命周期 

The three shells have varying lifecycles:  这三个外壳具有不同的生命周期：

 
*   `BaseShell` runs between the time `basemgr` starts up until a session has been established, and on demand thereafter to faciliate authenticationrequests. * BaseShell在从basemgr启动开始直到建立会话之间运行，此后根据需求按需进行身份验证请求。
*   `SessionShell` runs for the duration of a session.  *`SessionShell`在会话期间运行。
