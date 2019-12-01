 
# Guide to the Entity APIs  实体API指南 

This document is a guide for using the Entity APIs. See the main [entity](../entity.md) document for a conceptual overview. 本文档是使用实体API的指南。有关概念性概述，请参见主要的[entity]（../ entity.md）文档。

 
## What is an Entity?  什么是实体？Conceptually, an Entity is a blob of data, accompanied with a type, that Agents can manufacture and pass to other components (modules and agents). The databehind an Entity is owned by the Agent that created it, and the Agent isresponsible for serving an Entity’s data when a component tries to access it. 从概念上讲，实体是数据的一滴，伴随着一种类型，代理可以制造并传递给其他组件（模块和代理）。实体背后的数据由创建它的代理拥有，当组件尝试访问实体时，代理负责提供实体的数据。

Entities are the primary mechanism by which components share semantic data with each other.  For instance, a Google Contacts agent could manufacture an entitydescribing a contact by tagging the entity with a type com.fuchsia.Contact andpassing it around to other components that want an Entity of typecom.fuchsia.Contact. When a component requests data out of the Entity, theframework will bring up the agent that created the Entity and ask it to providethe data for it. This means that agents ultimately own and supply the databacking an Entity. 实体是组件彼此共享语义数据的主要机制。例如，Google Contacts代理可以通过使用com.fuchsia.Contact类型的标签标记该实体并将其传递给需要com.fuchsia.Contact实体的其他组件来制造一个描述联系人的实体。当组件向实体请求数据时，框架将调出创建实体的代理，并要求其为其提供数据。这意味着代理最终拥有并提供支持实体的数据。

 
## How does an Agent make an Entity?  代理如何创建实体？An Agent can create an Entity by calling `AgentContext.GetReferenceFactory().CreateReference(cookie)` and supplying it a`cookie` id. This cookie is how the Agent will identify this particular Entity.For instance, `joe@domain.com` could be the cookie for a Contact whose name isJoe. When this call is made, the framework will return an opaque, persistablestring reference meant for this Entity. This reference is used by a component toget the data out of the Entity. Entity references can be persisted to disk, theledger, passed around to other components which may also do the same. Note thatbecause these references may be persisted to the ledger, it means that you cancreate an Entity on one device, but dereference it on another device to get thedata out. 代理可以通过调用AgentContext.GetReferenceFactory（）。CreateReference（cookie）并为其提供cookie ID来创建实体。该cookie是代理识别该特定实体的方式。例如，“ joe@domain.com”可以是名为Joe的联系人的cookie。进行此调用时，框架将返回一个不透明的，持久化的字符串引用，用于此Entity。组件使用此引用从实体中获取数据。实体引用可以持久保存到磁盘，分类帐中，然后传递给其他组件，这些组件也可以这样做。请注意，由于这些引用可能会保留在分类帐中，因此这意味着您可以在一个设备上创建实体，而在另一设备上取消引用以获取数据。

C++ example snippet of an Agent creating an entity.  代理创建实体的C ++示例代码段。

```
auto component_context = sys::ComponentContext::Create();
auto agent_ctx = component_context->svc()
      ->Connect<fuchsia::modular::AgentContext>();

fuchsia::modular::EntityReferenceFactory factory;
agent_ctx->GetEntityReferenceFactory(factory.NewRequest());
factory->CreateReference("iamaperson@google.com", [] (std::string entity_reference) {
  // Pass the |entity_reference| to a Module or Agent for consumption.
});
```
 

 
## How does a Module make an Entity?  模块如何构成实体？A module can make an Entity by invoking `ModuleContext.CreateEntity()` with a type and data. This entity's data will then be the framework and its referenceis valid for the duration for the Story; once the Story is deleted, allentity references manufactured by its modules also become invalid. 模块可以通过调用具有类型和数据的ModuleContext.CreateEntity（）来创建实体。然后，该实体的数据将作为框架，并且其引用在故事持续时间内有效；一旦故事被删除，由其模块制造的常识引用也将变为无效。

C++ example snippet of a Module creating an entity.  创建实体的模块的C ++示例片段。

```
auto component_context = sys::ComponentContext::Create();
auto module_ctx = component_context->svc()
      ->Connect<fuchsia::modular::ModuleContext>();

fuchsia::mem::Buffer data;
fsl::StringFromVmo("iamaperson@google.com", &data);
module_ctx->CreateEntity("com.fuchsia.Contact", std::move(data).ToTransport(),
                          entity.NewRequest(), [] (std::string entity_reference) {
  // Pass the |entity_reference| to a Module or Agent for consumption.
});
```
 

 
## How does a Module or Agent get data out of an Entity?  模块或代理如何从实体中获取数据？A component can get data out of an entity reference by first resolving the reference into an `Entity` interface, and then requesting data from it. It may doso by calling `ComponentContext.GetEntityResolver().ResolveEntity(reference)`which will give you an `Entity` interface. You can then get the supported types ordata out of the Entity by calling `Entity.GetTypes()` or`Entity.GetData(typename)`, respectively. 组件可以通过以下方式从实体引用中获取数据：首先将引用解析为“ Entity”接口，然后向其请求数据。它可以通过调用`ComponentContext.GetEntityResolver（）。ResolveEntity（reference）`来实现，这将为您提供一个'Entity'接口。然后，您可以分别通过调用Entity.GetTypes（）或Entity.GetData（typename）来从Entity中获取受支持的类型或数据。

C++ Example snippet getting data out of an `entity_reference`:  C ++示例片段从`entity_reference`中获取数据：

```
auto component_context = sys::ComponentContext::Create();
auto component_ctx = component_context->svc()
      ->Connect<fuchsia::modular::ComponentContext>();

fuchsia::modular::EntityResolverPtr resolver;
fuchsia::modular::EntityPtr entity;
component_ctx->GetEntityResolver(resolver.NewRequest());

resolver->ResolveEntity(entity_reference, entity.NewRequest());
entity->GetData("com.fuchsia.Contact", [] (fuchsia::mem::BufferPtr data) {
    // ...
});
```
 

 
## How does an Agent provide data for an Entity?  代理如何为实体提供数据？