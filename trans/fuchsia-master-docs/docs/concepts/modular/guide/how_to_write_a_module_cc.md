 
# How-To: Write a Module in C++  如何：用C ++编写模块 

 
## Overview  总览 

A `Module` is a UI component that can participate in a [Story](link to story doc), potentially composed of many different `Module`s. A `Module`'s lifecycle is tightlybound to the story to which it was added. In addition to the capabilitiesprovided to all Peridot components via `fuchsia::modular::ComponentContext`, a `Module` is givenadditional capabilities via its `fuchsia::modular::ModuleContext`. “模块”是一个UI组件，可以参与[故事]（链接到故事文档），可能由许多不同的“模块”组成。一个模块的生命周期与它所添加的故事紧密相关。除了通过`fuchsia :: modular :: ComponentContext`为所有橄榄石组件提供的功能外，还通过`fuchsia :: modular :: ModuleContext`为模块提供其他功能。

 
## `SimpleMod`  `SimpleMod` 

 
### Mod Initialization  Mod初始化 

The first step to writing a `Module` is implementing the initializer.  编写模块的第一步是实现初始化程序。

```c++
#include <lib/sys/cpp/component_context.h>
#include <lib/async-loop/cpp/loop.h>
#include <lib/async-loop/default.h>
#include <ui/cpp/fidl.h>

#include "src/modular/lib/app_driver/cpp/module_driver.h"

namespace simple {

class SimpleModule : fuchsia::ui::app::ViewProvider {
 public:
	SimpleModule(
			modular::ModuleHost* module_host,
			fidl::InterfaceRequest<fuchsia::ui::app::ViewProvider> view_provider_request)
			: view_provider_binding_(this) {
		view_provider_binding_.Bind(std::move(view_provider_request));
}

 private:
	modular::ModuleHost* module_host_;
	fidl::Binding<fuchsia::ui::app::ViewProvider> view_provider_binding_;
	std::set<std::unique_ptr<SimpleView>> views_;
};

}  // namespace simple
```
 

The `ModuleHost` provides `SimpleModule` with its `StartupContext` and `fuchsia::modular::ModuleContext`. `ModuleHost`为`SimpleModule`提供`StartupContext`和`fuchsia :: modular :: ModuleContext`。

The `ViewProvider` request allows the system to connect to `SimpleModule`'s view. TODO: Update guide to explain view connections. ViewProvider请求允许系统连接到SimpleModule的视图。 TODO：更新指南以说明视图连接。

 
### Connecting to `SimpleAgent`  连接到`SimpleAgent` 

In order to provide `SimpleAgent` with a message queue `SimpleModule` first needs to connect to the agent via its `fuchsia::modular::ComponentContext`. 为了给SimpleAgent提供消息队列，SimpleModule首先需要通过其fuchsia :: modular :: ComponentContext连接到代理。

```c++
// Get the component context from the module context.
modular::fuchsia::modular::ComponentContextPtr component_context;
module_host->component_context()->svc()->Connect(
    component_context.NewRequest());

// Connect to the agent to retrieve it's outgoing services.
modular::fuchsia::modular::AgentControllerPtr agent_controller;
fuchsia::sys::ServiceProviderPtr agent_services;
component_context->ConnectToAgent("system/bin/simple_agent",
                                  agent_services.NewRequest(),
                                  agent_controller.NewRequest());
```
 

 
### Running the Module  运行模块 

```c++
int main(int argc, const char** argv) {
  async::Loop loop(&kAsyncLoopConfigAttachToCurrentThread);
  auto context = sys::ComponentContext::Create();
  modular::ModuleDriver<simple::SimpleModule> driver(context.get(),
                                                     [&loop] { loop.Quit(); });
  loop.Run();
  return 0;
}
```
 

`ModuleDriver` is a helper class that manages the `Module`'s lifecyle. Here it is given a newly created `StartupContext` and a callback that will be executedwhen the `Module` exits. `ModuleDriver` requires `SimpleModule` to implement theconstructor shown above, as well as a `Terminate`: `ModuleDriver`是管理`Module`的生命周期的助手类。这里给它一个新创建的StartupContext和一个回调，当模块退出时将执行该回调。 `ModuleDriver`需要`SimpleModule`来实现上面显示的构造函数，以及`Terminate`：

```c++
void Terminate(fit::function<void()> done);
```
 

The module is responsible for calling `done` once its shutdown sequence is complete.  一旦关闭顺序完成，模块负责调用`done`。

