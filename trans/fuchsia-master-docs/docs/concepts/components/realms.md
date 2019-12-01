 
# Realms  境界 

A *realm* is a subtree of the component instance tree. Every component instance is the root instance of a realm, known as the "component instance's realm",which is closely associated with the component instance. * realm *是组件实例树的子树。每个组件实例都是领域的根实例，称为“组件实例的领域”，它与组件实例紧密相关。

TODO: link to component instance tree  TODO：链接到组件实例树

Component instances may contain [children](#child-component-instances). Each child component instance in turn defines its own sub-realm. The union of thesesub-realms, along with the parent component instance, is equivalent to asubtree. Therefore, it is common to conceive of a realm as a component instancealong with its set of children. 组件实例可能包含[children]（child-component-instances）。每个子组件实例又定义了自己的子领域。这些子领域与父组件实例的并集等同于子树。因此，通常将领域及其子集视为组件实例。

Realms play a special role in the component framework. A realm is an *encapsulation boundary* for component instances. This means: 领域在组件框架中扮演着特殊的角色。领域是组件实例的“封装边界”。这意味着：

 
* Realms act as a capability boundary. It's up to the realm to decide whether a capability originating in the realm can be routed to component instancesoutside of the realm. This is accomplished through an [`expose`][expose]declaration in a [component manifest][component-manifests]. *领域充当能力边界。由领域决定是否可以将起源于该领域的功能路由到该领域之外的组件实例。这是通过[component manifest] [component-manifests]中的[`expose`] [expose]声明来完成的。
* The internal structure of a [sub-realm](#definitions) is opaque to the parent component instance. For example, the sub-realm could be structured either asone or multiple component instances, and from the perspective of the parentcomponent instance this looks the same as long as the sub-realm[exposes][expose] the same set of capabilities. * [sub-realm]（定义）的内部结构对于父组件实例是不透明的。例如，子领域可以构造为一个或多个组件实例，并且从父组件实例的角度来看，只要子领域[暴露] [暴露]相同的功能集，这看起来就相同。

 
## Definitions  定义 

This section contains definitions for basic terminology about realms.  本节包含有关领域的基本术语的定义。

 
- A *realm* is a subtree of the component instance tree.  -*领域*是组件实例树的子树。
- A *child component instance* is a component instance that is owned by another instance, the *parent*. -“子组件实例”是另一个实例“父”拥有的组件实例。
- A *sub-realm* is the realm corresponding to a child component instance.  -* sub-realm *是与子组件实例相对应的领域。
- A *containing realm* is the realm corresponding to the parent of a component instance. -包含领域的*是与组件实例的父实例相对应的领域。

 
## Example  例 

Here is an example of a realm with a capability routed through it:  这是一个具有路由能力的领域的示例：

![Realm example](realm_example.png)  ！[领域示例]（realm_example.png）

In this example, the `shell` component has two children: `tools` and `services`. `services` has two children, `logger` and `echo`, while `tools` has one child`echo_tool`. Components encapsulate their children, so while the `shell`component sees its own children, it has no direct knowledge of its grandchildren`echo_tool`, `logger`, or `echo`. Nevertheless, all of these component instancesare considered part of the `shell` realm. 在此示例中，“ shell”组件具有两个子元素：“工具”和“服务”。 “服务”有两个子项，“记录器”和“回声”，而“工具”有一个子项“ echo_tool”。组件封装了它们的子组件，因此，尽管“壳”组件看到了自己的子组件，但它不直接了解其子组件的“ echo_tool”，“ logger”或“ echo”。尽管如此，所有这些组件实例都被视为“ shell”领域的一部分。

The red arrows illustrate the path of an `/svc/echo` service capability that is routed through the realm from `echo` to `echo_tool`. The upward arrowscorrespond to [`expose`][expose] declarations, while the downward arrowsrepresent [`offer`][offer] declarations. The `expose` declarations cause`/svc/echo` to be exposed outside of the capability boundary of thecorresponding realms.  For example, if `services` did not expose `/svc/echo`,`shell` would not be aware that `/svc/echo` exists, and could not offer theservice to its children or access it at runtime. 红色箭头说明了通过域从“ echo”到“ echo_tool”路由的“ / svc / echo”服务功能的路径。向上箭头对应于[`expose`] [expose]声明，而向下箭头代表[`offer`] [offer]声明。 “ expose”声明使“ / svc / echo”暴露在相应领域的能力边界之外。例如，如果“服务”没有公开“ / svc / echo”，那么“ shell”将不会意识到“ / svc / echo”的存在，并且无法向其子项提供服务或在运行时访问该服务。

For a more detailed walkthrough of capability routing with this example, see the [component manifest capability routing example][component-manifest-examples]. 有关此示例的功能路由的更详细的演练，请参阅[组件清单功能路由示例] [component-manifest-examples]。

 
## Child component instances  子组件实例 

Component instances may contain children. Child component instances are considered part of the parent instance's definition and are wholly owned by theparent. This has the following implications: 组件实例可能包含子代。子组件实例被视为父实例定义的一部分，并由父实体完全拥有。这具有以下含义：

 
- A component instance decides what children it contains, and when its children are created and destroyed. -组件实例决定其包含哪些子代，以及何时创建和销毁其子代。
- A component instance cannot exist without its parent.  -没有其父级的组件实例将不存在。
- A component instance may not execute unless its parent is executing.  -除非其父级正在执行，否则组件实例不能执行。
- A component instance determines the capabilities available to its children by making [`offer`](#offer) declarations to them. -组件实例通过对它们的子代进行[`offer`]（offer）声明来确定其子代可用的功能。
- A component instance has some degree of control over the behavior of its children. For example, a component instance may bind to capabilities exposedfrom the child's realm through the [`Realm`](#the-realm-framework-service)framework service, or set hooks to intercept child lifecycle events. Thiscontrol is not absolute, however. For example, a component instance cannot usea capability from a sub-realm that was not explicitly exposed to it. -组件实例对其子代的行为有一定程度的控制。例如，组件实例可以绑定到通过[`Realm`]（therealm-framework-service）框架服务从孩子的领域公开的功能，或设置钩子以拦截孩子的生命周期事件。但是，此控件不是绝对的。例如，组件实例不能使用未明确公开给它的子领域的功能。

There are two varieties of child component instances, [static](#static-children) and [dynamic](#dynamic-children). 子组件实例有两种，[静态]（静态子代）和[动态]（动态子代）。

 
### Static children  静态儿童 

A *static child* is a component instance that was statically declared in the component's [manifest][component-manifests] by a [`children`][children]declaration. This declaration is necessary and sufficient to establish the childcomponent instance's existence. 一个“静态子代”是一个组件实例，它是通过[`children`] [children]声明在组件的[manifest] [component-manifests]中静态声明的。此声明对于建立子组件实例的存在是必要且充分的。

Typically, a child should be statically declared unless it has a reason to be dynamic (see [Dynamic children](#dynamic-children)). When a child is staticallydeclared, its definition and capabilities can be audited and capabilities can bestatically routed from it. 通常，应静态声明子级，除非有理由将其声明为动态子级（请参阅[动态子级]（dynamic-children））。静态声明子级后，可以审核其定义和功能，并可以从中静态路由功能。

A static child is defined, foremost, by two pieces of information:  静态子级首先由两条信息定义：

 
- The child instance's *name*. The name is local to the parent component instance, and is used to form monikers. It is valid to declare multiplechildren with the same URL and different names. -子实例的* name *。该名称是父组件实例的本地名称，用于形成绰号。声明具有相同URL和不同名称的多个子代是有效的。
- The child instance's component URL.  -子实例的组件网址。

For information on providing additional configuration information to child declarations, see [children][children]. 有关为子声明提供其他配置信息的信息，请参见[children] [children]。

TODO: link to component URL  TODO：链接到组件URL

TODO: link to monikers  TODO：链接到绰号

 
### Dynamic children  有活力的孩子 

A *dynamic child* is a component instance that was created at runtime in a [component collection](#component-collections). A dynamic child is always scopedto a particular collection. Dynamic children can be used to support use caseswhere the existence or cardinality of component instances cannot be determinedin advance. For example, a testing realm might declare a collection in whichtest component instances can be created. 动态子项是在运行时在[组件集合]（component-collections）中创建的组件实例。动态子级始终限于特定集合。动态子代可用于支持无法事先确定组件实例的存在或基数的用例。例如，测试领域可能会声明一个集合，可以在其中创建测试组件实例。

Most of the metadata to create a dynamic child is identical to that used to declare a static instance, except that it's provided at runtime. The name of adynamic child is implicitly scoped to its collection; thus it is possible tohave two dynamic children in two different collections with the same name. 用于创建动态子级的大多数元数据与用于声明静态实例的元数据相同，只是在运行时提供了元数据。非动态子项的名称隐式地限定于其集合；因此，可以在两个不同的集合中拥有两个具有相同名称的动态子代。

Capabilities cannot be statically routed from dynamic instances. This is an inherent restriction: there's no way to statically declare a route from acapability exposed by a dynamic instance. However, certain capabilities can berouted from the collection as a whole. TODO: service directories as an example 无法从动态实例静态路由功能。这是一个固有的限制：无法从动态实例公开的功能中静态声明路由。但是，可以从整个集合中路由某些功能。 TODO：以服务目录为例

 
### Component collections {#collections}  组件集合{collections} 

A *collection* is a container for [dynamic children](#dynamic-children) which may be created and destroyed at runtime using the[Realm](#the-realm-framework-service) framework service. * collection *是[dynamic children]（dynamic-children）的容器，可以使用[Realm]（therealm-framework-service）框架服务在运行时创建和销毁它们。

Collections support two modes of *durability*:  集合支持两种“持久性”模式：

 
- *Transient*: The instances in a *transient* collection are automatically destroyed when the instance containing the collection is stopped. -* Transient *：当包含瞬态集合的实例停止时，该实例将被自动销毁。
- *Persistent*: The instances in a *persistent* collection exist until they are explicitly destroyed or the entire collection is removed. [metastorage][glossary-storage] must be offered to the component for this option tobe available. -*持久*：*持久*集合中的实例一直存在，直到它们被明确销毁或整个集合被删除为止。必须为组件提供[metastorage] [glossary-storage]，此选项才可用。

TODO: Link to lifecycle  待办事项：链接到生命周期

Collections are declared in the [`collections`][collections] section of a component manifest. When an [`offer`][offer] declaration targets a collection,the offered capability is made available to every instance in the collection.Some capabilities can be exposed or offered from the collection as a whole, asan aggregation over the corresponding capabilities exposed by the instances inthe collection. 集合在组件清单的[`collections`] [collections]部分中声明。当[offer]]提供给集合时，所提供的功能将提供给集合中的每个实例。某些功能可以作为整体公开或从集合中提供，以汇总由集合中的实例。

TODO: service directories as an example  TODO：以服务目录为例

 
#### Example  例 

The following diagram illustrates a realm with a collection:  下图说明了具有集合的领域：

![Collection example](collection_example.png)  ！[收藏示例]（collection_example.png）

In this example, the `shell` component declares a static child `console` and a collection `(tools)`, highlighted by the dashed blue rectangle (the `()`notation denotes a collection). `(tools)` contains two dynamic instances, `ls`and `grep`. These instances are dynamic children of `shell`, scoped to`(tools)`. The use of a collection implies that the existence of `ls` and `grep`is not known in advance. This is plausible if you imagine that `ls` and `grep`are command-line tools that are instantiated on demand as the user requeststhem. 在此示例中，“ shell”组件声明了一个静态子项“ console”和一个集合“（tools）”，并用蓝色的虚线矩形突出显示（“（）”符号表示一个集合）。 （tools）包含两个动态实例，ls和grep。这些实例是“ shell”的动态子级，范围为“（工具）”。集合的使用意味着“ ls”和“ grep”的存在是事先未知的。如果您认为`ls`和`grep`是在用户请求时按需实例化的命令行工具，则这是合理的。

The example also illustrates a capability routing path with the red arrows. First, `console` [exposes][expose] `/svc/console` to its containing realm`shell`, which [offers][offer] it to `(tools)`. `/svc/console` then becomesavailable for any component instance in the collection to [use][use] -- it doesnot need to be routed to the dynamic instances independently. 该示例还用红色箭头说明了功能路由路径。首先，`console` [/ svc / console] [暴露] [/暴露] / svc / console`到其包含的领域`shell`，[提供] [提供]它给`（tools）`。然后，`/ svc / console`可供集合中的任何组件实例使用[use] [use] －不需要将其独立路由到动态实例。

 
## The Realm framework service  领域框架服务 

There is a [framework service][framework-services] available to every component, [`fuchsia.sys2.Realm`][realm.fidl]. The `Realm` service provides APIs for acomponent instance to manage the children in its realm, such as binding tochildren and creating dynamic children. See the linked FIDL definitions for fulldocumentation. 每个组件[fuchsia.sys2.Realm`] [realm.fidl]都有一个[framework服务] [framework-services]。 “领域”服务为组件实例提供API，以管理其领域中的子代，例如绑定到子代和创建动态子代。有关完整文档，请参见链接的FIDL定义。

