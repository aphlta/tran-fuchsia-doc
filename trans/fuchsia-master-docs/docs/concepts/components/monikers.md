 
# Monikers  莫尼克斯 

A moniker identifies a specific component instance in the component tree using a topological path. 名字对象使用拓扑路径在组件树中标识特定的组件实例。

Note: Use [component URLs][doc-component-urls] to identify the location from which the component's manifest and assets are retrieved; use monikers toidentify a specific instance of a component. 注意：使用[组件URL] [doc-component-urls]标识从中检索组件清单和资产的位置。使用绰号来标识组件的特定实例。

 
## Types  种类 

There are three types of monikers:  有三种类型的绰号：

 
- Child moniker: Denotes a child of a component instance relative to its parent.  -子代名词：表示组件实例相对于其父代的子代。
- Relative moniker: Denotes the path from a source component instance to a target component instance, expressed as a sequence of child monikers. -相对名字对象：表示从源组件实例到目标组件实例的路径，表示为一系列子名字对象。
- Absolute moniker: Denotes the path from the root of the component instance tree to a target component instance, expressed as a sequence of childmonikers. Every component instance has a unique absolute moniker. -绝对名称：表示从组件实例树的根到目标组件实例的路径，表示为一系列子标记。每个组件实例都有一个唯一的绝对绰号。

 
## Stability  稳定性 

Monikers are stable identifiers. Assuming the component topology does not change, the monikers used to identify component instances in the topologywill remain the same. Monikers是稳定的标识符。假设组件拓扑不变，则用于标识拓扑中组件实例的名称将保持不变。

 
## Uniqueness  独特性 

Each time a component instance is destroyed and a new component instance with the same name is created in its place in the component topology (as a childof the same parent), the new instance is assigned a unique instance identifierto distinguish it from prior instances in that place. 每次销毁一个组件实例，并在组件拓扑中以相同名称创建一个具有相同名称的新组件实例时（作为同一父实例的子实例），将为该新实例分配一个唯一的实例标识符，以将其与以前的实例区分开来。地点。

Monikers include unique instance identifiers to prevent confusion of old component instances with new component instances of the same name as thetree evolves. Monikers包含唯一的实例标识符，以防止旧的组件实例与名称相同的新组件实例与树的演变相混淆。

 
## Privacy  隐私 

Monikers may contain privacy-sensitive information about other components that the user is running. Monikers可能包含有关用户正在运行的其他组件的隐私敏感信息。

To preserve the encapsulation of the system, components should be unable to determine the identity of other components running outside of their ownrealm. Accordingly, monikers are only transmitted on a need-to-know basisor in an obfuscated form. 为了保留系统的封装，组件应无法确定在其自身领域之外运行的其他组件的身份。因此，绰号仅在需要知道的基础上以混淆形式发送。

For example, components are not given information about their own absolute moniker because it would also reveal information about their parents andancestors. 例如，没有为组件提供有关其自身绝对绰号的信息，因为它还会显示有关其父代和祖先的信息。

Monikers may be collected in system logs. They are also used to implement the component framework's persistence features. Monikers可能会收集在系统日志中。它们还用于实现组件框架的持久性功能。

TODO: Describe obfuscation strategy.  待办事项：描述混淆策略。

 
## Notation  符号 

This section describes the syntax used for displaying monikers to users.  本节介绍用于向用户显示别名的语法。

 
### Instance and Collection Names  实例和集合名称 

Parents assign names to each of their children. Dynamically created children are arranged by their parent into named collections. 父母给每个孩子分配名字。动态创建的子级由其父级安排到命名集合中。

Syntax: Each name is a string of 1 to 100 of the following characters: `a-z`, `0-9`, `_`, `.`, `-`. 语法：每个名称都是1到100个以下字符的字符串：`a-z`，`0-9`，`_`，`.`，`-`。

See [component manifest][doc-manifests] documentation for more details.  有关更多详细信息，请参见[component manifest] [doc-manifests]文档。

 
### Instance Identifiers  实例标识符 

Instance identifiers ensure uniqueness of monikers over time whenever a parent destroys a component instance and creates a new one with the same name. 每当父级销毁一个组件实例并创建一个具有相同名称的新实例时，实例标识符可确保名称随时间的唯一性。

Syntax: Decimal formatted 32-bit unsigned integer using characters: `0-9`.  语法：十进制格式的32位无符号整数，使用字符“ 0-9”。

 
### Child Monikers  儿童徒手 

Represented by the child's collection name (if any), name, and instance identifier delimited by `:`. 由孩子的集合名称（如果有），名称和实例标识符表示，以`：`分隔。

Syntax: `{name}:{id}` or `{collection}:{name}:{id}`  语法：`{name}：{id}`或`{collection}：{name}：{id}`

Examples:  例子：

 
- `truck:2`: child "truck" (instance id 2)  -`truck：2`：子级“ truck”（实例ID 2）
- `animals:bear:1`: child "bear" (instance id 1) in collection "animals"  -`animals：bear：1`：集合“ animals”中的孩子“ bear”（实例ID 1）

TODO: Add a diagram to go along with the examples.  待办事项：添加一个图和示例。

 
### Relative Monikers  相对莫尼克斯 

Represented by the minimal sequence of child monikers encountered when tracing upwards from a source to the common ancestor of the source and target and thendownwards to the target. 从源向上追溯到源和目标的共同祖先，然后再向下追溯到目标时遇到的最小子代号序列表示。

A relative path begins with `.` and is followed by path segments. `\` denotes an upwards traversal segment. `/` denotes a downwards traversal segment. Thereis no trailing `\` or `/`. 相对路径以“。”开头，后跟路径段。 “ \”表示向上遍历线段。 “ /”表示向下遍历线段。没有尾随的“ \”或“ /”。

Relative monikers are invertible; a path from source to target can be transformed into a path from target to source because information aboutboth paths is fully encoded by the representation. 相对名称是可逆的；从源到目标的路径可以转换为从目标到源的路径，因为关于这两个路径的信息都由表示形式完全编码。

In contrast, file system paths are not invertible because they use `..` to denote upwards traversal so some inverse traversal information is missing. 相反，文件系统路径不可逆，因为它们使用“ ..”表示向上遍历，因此缺少一些逆遍历信息。

Syntax: `.\{path from source to ancestor}/{path from ancestor to target}`  语法：`。\ {从源到祖先的路径} / {从祖先到目标的路径}`

Examples:  例子：

 
- `.`: self - no traversal needed  -`.`：自我-无需遍历
- `./truck:2`: a child - traverse down `truck:2`  -`./truck：2`：一个孩子-下移`truck：2`
- `./truck:2/axle:1`: a grandchild - traverse down `truck:2` then down `axle:1`  -`./truck：2 / axle：1`：孙子-下移`truck：2`然后下移`axle：1`
- `.\truck:2/animals:bear:1`: a cousin - traverse up `truck:2` then down `animals:bear:1` -`。\ truck：2 / animals：bear：1`：一个表弟-上移`truck：2`然后下移`animals：bear：1`
- `.\animals:bear:1/truck:2`: a cousin - inverse of the prior example, constructed by reversing the segments of the traversal -`。\ animals：bear：1 / truck：2`：一个堂兄-与上一个示例相反，它是通过反转遍历的各段而构造的

TODO: Add a diagram to go along with the examples.  待办事项：添加一个图和示例。

 
### Absolute Monikers  绝对魔鬼 

Represented by the absolute path from the root to the component instance as a sequence of child monikers. 从根到组件实例的绝对路径表示为一系列子代号。

An absolute path begins with `/` and is followed by downwards traversal path segments delimited by `/`. There is no trailing `/`. 绝对路径以“ /”开始，然后是由“ /”界定的向下遍历路径段。没有尾随的`/`。

Syntax: `/{path from root to target}`  语法：`/ {从根到目标的路径}`

Examples:  例子：

 
- `/`: the root itself (it has no name because it has no parent)  -`/`：根目录本身（它没有名称，因为它没有父级）
- `/objects:2/animals:deer:1`: from root traverse down `objects:2` then down `animals:deer:1` -`/ objects：2 / animals：deer：1`：从根向下遍历`objects：2`，然后再遍历`animals：deer：1`

TODO: Add a diagram to go along with the examples.  待办事项：添加一个图和示例。

