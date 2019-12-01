 
## Intents  意向 

An `Intent` is used to instruct a module to perform an action. The intent contains the action name, the arguments for the action parameters, and anoptional handler which explicitly specifies which module is meant to perform theaction. “意图”用于指示模块执行动作。该意图包含动作名称，动作参数的参数以及一个可选的处理程序，该处理程序显式指定要执行该动作的模块。

 
### Declaring Actions  声明动作 

Modules can declare which actions they handle, and their associated parameters in their [module facet](module_facet.md). The modular framework will then indexthe module and treat it as a candidate for any incoming intents which containthe specified action, and don't have an explicit handler set. 模块可以在[module facet]（module_facet.md）中声明其处理的动作以及相关的参数。然后，模块化框架将为模块建立索引，并将其视为包含指定操作且没有显式处理程序集的所有传入意图的候选者。

 
### Handling Intents  处理意图 

When an intent is resolved the framework determines which module instance will handle it. 解决意图后，框架将确定哪个模块实例将处理该意图。

The framework then connects to the module's `fuchsia::modular::IntentHandler` service, and calls `HandleIntent()`. The framework will connect to the intenthandler interface each time a new intent is seen for a particular moduleinstance, and intents can be sent to modules which are already running. Modulesare expected to handle the transition between different intents gracefully. 然后，框架连接到模块的`fuchsia :: modular :: IntentHandler`服务，并调用`HandleIntent（）`。每当看到特定模块实例的新意图时，该框架将连接到intenthandler接口，并且可以将意图发送到已经运行的模块。期望模块能够优雅地处理不同意图之间的过渡。

 
### Example  例 

To illustrate the intended use of intents, consider the following fictional example: a new story has been created with a module displaying a list ofrestaurants and the module wants to show directions to the currently selectedrestaurant. 为了说明意图的预期用途，请考虑以下虚构示例：已创建了一个新故事，其模块显示了餐厅列表，并且该模块希望显示指向当前所选餐厅的路线。

The restaurant module creates an intent with a `com.fuchsia.navigate` action with two parameters `start` and `end`, both of type `com.fuchsia.geolocation`and passes it to the modular framework via `ModuleContext.AddModuleToStory`. restaurant模块通过两个参数“ start”和“ end”（均为com.fuchsia.geolocation）的“ com.fuchsia.navigate”动作创建一个意图，并通过“ ModuleContext.AddModuleToStory”将其传递给模块化框架。 。

At this point, the framework will search for a module which has declared support for the `com.fuchsia.navigate` action. Once such a module is found, it is addedto the story and started. The framework then connects to the started module's`IntentHandler` service and provides it with the intent. 此时，框架将搜索已声明支持“ com.fuchsia.navigate”动作的模块。一旦找到这样的模块，就将其添加到故事中并开始。然后，框架连接到已启动模块的IntentHandler服务，并为其提供意图。

At this point, the restaurant list module's selected restaurant changes. It again creates an intent, with the same action as before but with new locationarguments and calls `ModuleContext.AddModuleToStory`. 此时，餐厅列表模块的所选餐厅将更改。它再次创建一个意图，其动作与以前相同，但具有新的location参数，并调用`ModuleContext.AddModuleToStory`。

The framework now knows there is already a module instance running (in this case `AddModuleToStory` uses the `name` parameter to identify module instances)oexplicitly specify a which can handle the given action, and connects to its`IntentHandler` interface and provides it with the new intent. The navigationmodule can then update its UI to display directions to the new restaurant. 框架现在知道已经有一个模块实例在运行（在这种情况下，AddModuleToStory使用名称参数来标识模块实例）明确指定可以处理给定动作的，并连接到其IntentHandler接口并提供它以新的意图。然后，导航模块可以更新其UI，以显示前往新餐厅的路线。

