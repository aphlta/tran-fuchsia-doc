 
## Agents  代理商 

An `Agent` is a singleton-per-session component which runs outside of the scope of a Story without any graphical UI. “代理”是每个会话的单例组件，它在没有任何图形UI的Story范围之外运行。

Agents can schedule tasks (i.e. they can register to be woken up by the framework to perform work), and provide services to other modular components. 代理可以安排任务（即他们可以注册以被框架唤醒以执行工作），并为其他模块化组件提供服务。

Any modular component can connect to an agent and access its services (including modules, shells, and other agents). 任何模块化组件都可以连接到代理并访问其服务（包括模块，外壳和其他代理）。

 
### Environment  环境 

An agent is given access to two services provided by the modular framework in its incoming namespace: 代理可以在其传入名称空间中访问由模块化框架提供的两项服务：

 
*   `fuchsia.modular.ComponentContext` which gives the agent access to functionality which is shared across components run under the modularframework (e.g. modules, shells, agents). *`fuchsia.modular.ComponentContext`，使代理能够访问在模块化框架下运行的组件（例如模块，外壳，代理）之间共享的功能。
*   `fuchsia.modular.AgentContext` which gives agents access to agent specific functionality, like creating entity references and scheduling tasks. *`fuchsia.modular.AgentContext`，它使代理能够访问特定于代理的功能，例如创建实体引用和调度任务。

An agent is expected to provide two services to the modular framework in its outgoing namespace: 期望代理在其传出名称空间中为模块化框架提供两项服务：

 
*   `fuchsia.modular.Agent` which allows the framework to forward connection requests from other components and tell the agent to run tasks. *`fuchsia.modular.Agent`，允许框架转发来自其他组件的连接请求并告诉代理运行任务。
*   `fuchsia.modular.Lifecycle` which allows the framework to signal the agent to terminate gracefully. *`fuchsia.modular.Lifecycle`，它允许框架向代理发出信号以优雅地终止。

The aforementioned services enable communication between agents and the modular framework, but agents can also expose custom FIDL services to components. For amore detailed explanation of the mechanism which enables this service exchangesee Communication Mechanisms below. 前述服务实现了代理程序和模块化框架之间的通信，但是代理程序也可以向组件公开自定义FIDL服务。有关启用此服务交换的机制的更详细说明，请参见下面的通信机制。

 
### Lifecycle  生命周期 

For most agents, when a component connects to an agent the framework will give the component an `AgentController`. When the connecting component drops the`AgentController` connection, and there are no outstanding connections, theagent will be killed by the framework. 对于大多数代理，当组件连接到代理时，框架将为该组件提供一个“ AgentController”。当连接组件删除“ AgentController”连接，并且没有未完成的连接时，该代理将被框架杀死。

There are some agents for which the `sessionmgr` maintains an `AgentController`, and thus the agent remains alive for the duration of the session. These"session" agents also get access to `fuchsia.modular.PuppetMaster` in theirincoming namespace. 对于某些代理，sessionmgr为其维护一个AgentController，因此该代理在会话期间保持活动状态。这些“会话”代理还可以在其传入的名称空间中访问“ fuchsia.modular.PuppetMaster”。

 
### Communication mechanisms  沟通机制 

Components can communicate with agents in two different ways: either by connecting to a FIDL service exposed by the agent, or over a `MessageQueue`. 组件可以通过两种不同的方式与代理进行通信：通过连接到代理公开的FIDL服务，或通过“ MessageQueue”。

Which communication method is appropriate depends on the semantics of the messages being passed. FIDL requires both agent and client to be running,whereas message queues allow the life cycles of the sender and receiver to bedifferent. 哪种通信方法合适取决于传递的消息的语义。 FIDL要求代理和客户端都在运行，而消息队列允许发送方和接收方的生命周期有所不同。

 
#### FIDL Services  FIDL服务 

The modular framework will forward a `fuchsia.sys.ServiceProvider` request via `fuchsia::modular::Agent.Connect` call, and will also provide the agent with anidentifier for the client which is requesting the service provider. 模块化框架将通过`fuchsia :: modular :: Agent.Connect`调用转发“ fuchsia.sys.ServiceProvider”请求，还将为代理提供请求服务提供者的客户端标识符。

Any services added to the service provider will be exposed directly to the connecting component. 添加到服务提供商的任何服务都将直接暴露给连接组件。

To illustrate this, consider a module connecting to an agent:  为了说明这一点，请考虑连接到代理的模块：

The module calls `ConnectToAgent` on its `ComponentContext`, which contains a `ServiceProvider` request as well as an `AgentController` request. 该模块在其“ ComponentContext”上调用“ ConnectToAgent”，其中包含“ ServiceProvider”请求和“ AgentController”请求。

The agent controller request is used by the framework to keep the agent alive until the agent controller is closed by the client. If more than one client isconnected to the same agent, the agent will be kept alive until all agentcontrollers have been closed. 框架使用代理控制器请求使代理保持活动状态，直到客户端关闭代理控制器为止。如果有多个客户端连接到同一代理，则该代理将保持活动状态，直到关闭所有代理控制器为止。

The service provider request is forwarded to the agent, along with a string which identifies the client connecting to the agent. 服务提供者请求连同标识连接到代理的客户端的字符串一起转发到代理。

 
#### Message Queues  消息队列 

