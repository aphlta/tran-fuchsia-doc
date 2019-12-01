 
## Entities  实体 

The Fuchsia entity model facilitates information interchange by defining a common interface for _describing_, _referencing_, _accessing_, and _mutating_data objects (entities) which are shared between components (modules, agents,shells) running in the modular framework. It consists of the following majorconcepts: 紫红色的实体模型通过为在模块化框架中运行的组件（模块，代理，外壳）之间共享的_describing _，_ referencing _，_ accessing_和_mutating_data对象（实体）定义公共接口，从而促进了信息交换。它包含以下主要概念：

 
*   Entities: the data objects shared between components.  *实体：组件之间共享的数据对象。
*   Entity references: a serializable token which can be used to retrieve an `Entity` handle. *实体引用：可序列化的令牌，可用于检索“实体”句柄。
*   `Entity`: An interface which gives access to a shared data object.  *实体：一个接口，可以访问共享数据对象。
*   `EntityProvider`: the interface which allows agents to expose entities to the system. *`EntityProvider`：允许代理将实体公开给系统的接口。
*   `EntityResolver`: the Fuchsia API for requesting an `Entity` handle for a given reference. *`EntityResolver`：紫红色API，用于请求给定引用的`Entity`句柄。

 
### Lifecycle  生命周期 

The lifecycle of the data backing an `Entity` is controlled by the `EntityProvider`. The lifecycle of the `Entity` handle is controlled by`sessionmgr`. 支持“ Entity”的数据的生命周期由“ EntityProvider”控制。实体句柄的生命周期由sessionmgr控制。

 
#### Entities owned by Agents  代理商拥有的实体 

Agents don't create `Entity` handles directly. Agents connect to the `EntityReferenceFactory` which provides the agent with an entity reference inexchange for a `cookie`. The entity reference can then be shared with othermodular components which can use their `EntityResolver` to dereference it intoan `Entity` interface. 代理不会直接创建“实体”句柄。代理连接到“ EntityReferenceFactory”，后者为代理提供“ cookie”的实体引用交换。然后，实体引用可以与其他模块化组件共享，这些组件可以使用其“ EntityResolver”将其解引用到“ Entity”接口中。

Calls on that `Entity` interface will then be forwarded to the agent, along with the associated cookie. 然后，对该“ Entity”接口的调用将与关联的Cookie一起转发给代理。

The agent is thus responsible for storing and providing the entity data, associating it with the correct cookie, and optionally handling requests formutating the entity data. 因此，代理负责存储和提供实体数据，将其与正确的cookie关联，并可选地处理对实体数据进行更改的请求。

 
#### Entities owned by a Story  故事拥有的实体 

Modules can create entities explicitly via their `ModuleContext` by providing a `fuchsia.mem.Buffer` and an associated type. The framework manages the lifecycleof such entities by storing them in the story's record. For this reason, whenthe story is deleted, so is the entity. Agents and modules outside the story candereference the entity so long as the story still exists. 模块可以通过提供其“ fuchsia.mem.Buffer”和关联的类型，通过其“ ModuleContext”显式创建实体。该框架通过将此类实体存储在故事的记录中来管理它们的生命周期。因此，故事被删除时，实体也被删除。只要故事仍然存在，故事外部的代理和模块就可以取消引用实体。

 
#### Entity Resolution  实体解析 

This section describes the internals of entity resolution.  本节描述实体解析的内部。

`EntityProviderRunner` implements the `fuchsia::modular::EntityResolver` interface, and is also responsible for creating entity references byimplementing the `fuchsia::modular::EntityReferenceFactory` interface. A singleinstance of the `EntityProviderRunner` manages all the entity providers runningin the system. EntityProviderRunner实现了fuchsia :: modular :: EntityResolver接口，并通过实现fuchsia :: modular :: EntityReferenceFactory接口来创建实体引用。 `EntityProviderRunner`的一个实例管理系统中运行的所有实体提供者。

The first step in entity resolution (i.e. the first thing which happens when `ResolveEntity` is called) is the runner determines whether the entity isprovided by an agent or by the modular framework by inspecting the entityreference. The runner then asks an `EntityProviderLauncher` to launch theappropriate entity provider. 实体解析的第一步（即，在调用“ ResolveEntity”时发生的第一件事）是运行程序，它通过检查实体引用来确定是由代理还是由模块化框架提供实体。跑步者然后要求“ EntityProviderLauncher”启动适当的实体提供者。

If the entity provider is an agent, an `AgentController` is passed to the launcher, and the runner keeps the agent controller alive until the clientcloses the `Entity`. 如果实体提供者是代理，则将“ AgentController”传递给启动器，并且运行程序使代理控制器保持活动状态，直到客户端关闭“ Entity”为止。

Each `Entity` request has an associated `EntityController` which the entity runner owns. The `EntityController` owns the `AgentController` if the entityprovider was an agent, and is responsible for forwarding the entity interfacemethods to the entity provider. 每个“实体”请求都有一个关联的“实体控制器”，实体运行者拥有。如果entityprovider是代理，则“ EntityController”拥有“ AgentController”，并负责将实体接口方法转发给实体提供者。

 
### Read More  阅读更多 

 
