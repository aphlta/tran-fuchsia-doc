 
# How-To: Write an Agent in C++  如何：用C ++编写代理 

 
## Overview  总览 

An Agent is a component that runs without any direct user interaction. The lifetime of an Agent component instance is bounded by its session.  It can be shared by mods across many stories. Inaddition to the capabilities provided to all modular components via`fuchsia::modular::ComponentContext`, an Agent is given additional capabilities via`fuchsia::modular::AgentContext` as an incoming service. 代理是无需任何直接用户交互即可运行的组件。代理程序组件实例的生存期受其会话限制。可以在许多故事中由mod共享。除了通过`fuchsia :: modular :: ComponentContext`为所有模块化组件提供的功能外，还通过`fuchsia :: modular :: AgentContext`为代理提供附加功能，作为传入服务。

Agents must expose the `fuchsia::modular::Agent` service to receive new connections and provide services. An Agent component may implement the `fuchsia::modular::Lifecycle` service to receive termination signals and voluntarily exit. 代理必须公开`fuchsia :: modular :: Agent`服务，以接收新连接并提供服务。一个Agent组件可以实现`fuchsia :: modular :: Lifecycle`服务来接收终止信号并自愿退出。

 
## SimpleAgent  简单代理 

 
### fuchsia::modular::Agent Initialization  紫红色::模块化::代理初始化 

The first step to writing an Agent is setting up the scaffolding using the `modular::Agent` utility class. 编写Agent的第一步是使用modular :: Agent实用程序类设置脚手架。

```c++
#include <lib/modular/cpp/agent.h>

int main(int /*argc*/, const char** /*argv*/) {
  async::Loop loop(&kAsyncLoopConfigAttachToCurrentThread);
  auto context = sys::ComponentContext::Create();
  modular::Agent agent(context->outgoing(), [&loop] { loop.Quit(); });
  loop.Run();
  return 0;
}
```
 

The `modular::Agent` utility above implements and exposes `fuchsia::modular::Agent` and `fuchsia::modular::Lifecycle` services. Additionally, 上面的`modular :: Agent`实用程序实现并公开了`fuchsia :: modular :: Agent`和`fuchsia :: modular :: Lifecycle`服务。另外，

 
#### `fuchsia::modular::AgentContext`  紫红色::模块化:: AgentContext` 

`fuchsia::modular::AgentContext` is a protocol that is exposed to all Agent components. For example, it allows agents to schedule `Task`s that will be executed atspecific intervals. 紫红色:: modular :: AgentContext是向所有Agent组件公开的协议。例如，它允许代理计划以特定间隔执行的“任务”。

`fuchsia::modular::AgentContext` also gives `fuchsia::modular::Agent`s access to `fuchsia::modular::ComponentContext` which is a protocol that is exposed to allPeridot components (i.e. `fuchsia::modular::Agent` and `Module`).For example, `fuchsia::modular::ComponentContext` provides access to `Ledger`,Peridot's cross-device storage solution. `fuchsia :: modular :: AgentContext`还使`fuchsia :: modular :: Agent可以访问`fuchsia :: modular :: ComponentContext`，这是一个暴露于所有橄榄石组件的协议（即`fuchsia :: modular： ：Agent`和`Module`）。例如，`fuchsia :: modular :: ComponentContext`提供对Peridot跨设备存储解决方案“ Ledger”的访问。

 
### Advertising the `Simple` Protocol  宣传“简单”协议 

In order for the `SimpleAgent` to advertise the `Simple` protocol to other modular components, it needs to expose it as an agent service. `modular::Agent::AddService<>()` provides a way to dothis: 为了使“ SimpleAgent”能够将“ Simple”协议发布给其他模块化组件，它需要将其作为代理服务公开。 `modular :: Agent :: AddService <>（）`提供了一种方法：

```c++
  class SimpleImpl : Simple {
    SimpleImpl();
    ~SimpleImpl();

    std::string message_queue_token() const { return token_; }

  private:
    // The current message queue token.
    std::string token_;
  };

  int main(int /*argc*/, const char** /*argv*/) {
    ...
    modular::Agent agent(context->outgoing(), [&loop] { loop.Quit(); });

    SimpleImpl simple_impl;
    fidl::BindingSet<Simple> simple_bindings;

    agent.AddService<Simple>(simple_bindings.GetHandler(&simple_impl));
    ...
  }
```
 

In the code above, `SimpleAgent` adds the `Simple` service as an agent service. Now, when a component connects to the `SimpleAgent`, it will be able to connect to the `Simple` interface andcall methods on it. Those method calls will be delegated to the `simple_impl` object. 在上面的代码中，`SimpleAgent`将`Simple`服务添加为代理服务。现在，当组件连接到`SimpleAgent`时，它将能够连接到`Simple`接口并在其上调用方法。这些方法调用将委派给`simple_impl`对象。

 
## Connecting to SimpleAgent  连接到SimpleAgent 

To connect to the `SimpleAgent` from a different component:  要从其他组件连接到`SimpleAgent`，请执行以下操作：

```c++
// The agent is guaranteed to stay alive as long as |agent_controller| stays in scope.
fuchsia::modular::AgentControllerPtr agent_controller;
fuchsia::sys::ServiceProviderPtr agent_services;
SimplePtr simple;
component_context->ConnectToAgent(agent_url,
                                  agent_services.NewRequest(),
                                  agent_controller.NewRequest());
agent_services.ConnectToService(Simple::Name_, simple.NewRequest().TakeChannel());
```
 

Here the component context is asked to connect to the fuchsia::modular::Agent at `agent_url`, and is given a request for the services that the `SimpleAgent` will provide via `agent_services`,and a controller for the `fuchsia::modular::Agent` via `agent_controller`. 在这里，要求组件上下文连接到agent_url处的fuchsia :: modular :: Agent，并向其请求对SimpleAgent将通过agent_services提供的服务的请求，以及一个针对fuchsia的控制器： ：modular :: Agent`通过`agent_controller`。

Then the client connects to the `Simple` protocol by invoking `ConnectToService` with a request for a new `SimplePtr`. 然后，客户端通过请求请求新的SimplePtr的ConnectToService来连接到Simple协议。

