 
# FIDL Style Guide  FIDL样式指南 

This section contains style-related information for [Fuchsia Interface Definition Language](/docs/development/languages/fidl/README.md) files. 本节包含[Fuchsia界面定义语言]（/ docs / development / languages / fidl / README.md）文件与样式有关的信息。

[TOC]  [目录]

 
## Names  名字 

 

> The Naming of Cats is a difficult matter,<br> > It isn't just one of your holiday games;<br>>  --- T.S. Eliot >猫的命名是一件困难的事情，<br>>这不仅仅是您的假日游戏之一； <br>> --- T.S.艾略特

Names defined in FIDL are used to generate identifiers in each target language. Some languages attach semantic or conventional meaning to names of variousforms.  For example, in Go, whether the initial letter in an identifier iscapitalized controls the visibility of the identifier.  For this reason, many ofthe language back ends transform the names in your library to make them moreappropriate for their target language.  The naming rules in this section are abalancing act between readability in the FIDL source, usability in each targetlanguage, and consistency across target languages. FIDL中定义的名称用于生成每种目标语言的标识符。一些语言将语义或常规含义附加到各种形式的名称上。例如，在Go中，是否将标识符中的首字母大写控制标识符的可见性。因此，许多语言后端都会转换库中的名称，以使其更适合其目标语言。本节中的命名规则是在FIDL源代码的可读性，每种目标语言的可用性以及目标语言之间的一致性之间取得平衡。

Avoid commonly reserved words, such as `goto`.  The language back ends will transform reserved words into non-reserved identifiers, but these transformsreduce usability in those languages.  Avoiding commonly reserved words reducesthe frequency with which these transformations are applied. 避免使用诸如goto之类的常用保留字。语言后端会将保留的单词转换为非保留的标识符，但是这些转换会降低这些语言的可用性。避免使用保留字会降低应用这些转换的频率。

While some FIDL keywords are also commonly reserved words in target languages, (such as `struct` in C and C++), and should thus be avoided, other FIDLkeywords, particularly `request` and `handle`, are generally descriptive andcan be used as appropriate. 虽然某些FIDL关键字也是目标语言中的常用保留字（例如C和C ++中的“ struct”），因此应避免使用，但其他FIDL关键字（尤其是“ request”和“ handle”）通常是描述性的，可以用作适当。

Names must not contain leading or trailing underscores.  Leading or trailing underscores have semantic meaning in some languages (e.g., leading underscorescontrol visibility in Dart) and conventional meaning in other languages (e.g.,trailing underscores are conventionally used for member variables in C++).Additionally, the FIDL compiler uses leading and trailing underscores to mungeidentifiers to avoid collisions. 名称中不得包含下划线或下划线。前导或尾部下划线在某些语言中具有语义含义（例如，Dart中的前导下划线控制可见性），而在其他语言中则具有常规含义（例如，C ++中的成员变量通常使用尾部下划线）。此外，FIDL编译器使用前导和尾部下划线为了避免冲突。

Use the term `size` to name a number of bytes. Use the term `count` to name a number of some other quantity (e.g., the number of items in a vector ofstructs). 使用术语“大小”来命名多个字节。使用术语“计数”来命名一些其他数量的数字（例如，结构向量中的项目数）。

 
### Case definitions  案例定义 

Sometimes there is more than one way to decide on how to delimit words in identifiers.  Our style is as follows: 有时，有多种方法可以决定如何在标识符中定界。我们的风格如下：

 
 * Start with the original phrase in US English (e.g., "Non-Null HTTP Client")  *以美国英语中的原始短语开头（例如，“非null HTTP客户端”）
 * Remove any punctuation. ("Non Null HTTP Client")  *删除所有标点符号。 （“非空HTTP客户端”）
 * Make everything lowercase ("non null http client")  *使所有内容都小写（“非null http客户端”）
 * Do one of the following, depending on what style is appropriate for the given identifier: *根据给定标识符适合的样式，执行以下操作之一：
    * Replace spaces with underscores ('_') for _lower snake case_ (`non_null_http_client`). *用下划线（_）代替_lower snake case_（`non_null_http_client`）。
    * Capitalize and replace spaces with underscores for _upper snake case_ (`NON_NULL_HTTP_CLIENT`). *大写并用下划线替换_upper snake case_（`NON_NULL_HTTP_CLIENT`）。
    * Capitalize the first letter of each word and join all words together for _upper camel case_ (`NonNullHttpClient`). *将每个单词的首字母大写，并将所有单词结合在一起，成为_uper camel case_（`NonNullHttpClient`）。

 
#### Usage  用法 

The following table maps the case usage to the element:  下表将案例用法映射到元素：

Element                    | Casing             | Example ---------------------------|--------------------|-----------------`bits`                     | _upper camel case_ | `InfoFeatures`bitfield members           | _upper snake case_ | `WLAN_SNOOP``const`                    | _upper snake case_ | `MAX_NAMES`primitive alias            | _lower snake case_ | `hw_partition``protocol`                 | _upper camel case_ | `AudioRenderer`protocol method parameters | _lower snake case_ | `enable_powersave`protocol methods           | _upper camel case_ | `GetBatteryStatus``struct`                   | _upper camel case_ | `KeyboardEvent`struct members             | _lower snake case_ | `child_pid``table`                    | _upper camel case_ | `ComponentDecl`table members              | _lower snake case_ | `num_rx``union`                    | _upper camel case_ | `BufferFormat`union members              | _lower snake case_ | `vax_primary``xunion`                   | _upper camel case_ | `ZirconHandle`xunion members             | _lower snake case_ | `pdp8_iot``enum`                     | _upper camel case_ | `PixelFormat`enum members               | _upper snake case_ | `RGB_888` 元素|套管示例--------------------------- | -------------------- | -----------------`位`| _上驼箱`InfoFeatures`位域成员| _大蛇案_ | `WLAN_SNOOP`const` | _上蛇皮套_ | “ MAX_NAMES”原始别名| _下蛇皮套_ | `hw_partition``协议_上驼箱“ AudioRenderer”协议方法参数| _下蛇皮套_ | `enable_powersave`协议方法| _上驼箱`GetBatteryStatus``struct` | _上驼箱`KeyboardEvent`struct成员| _下蛇皮套_ | `child_pid``table` | _上驼箱`ComponentDecl`表成员| _下蛇皮套_ | `num_rx``union` | _上驼箱_ `BufferFormat`工会成员| _下蛇皮套_ | `vax_primary``xunion` | _上驼箱_ ZirconHandle`工会会员| _下蛇皮套_ | `pdp8_iot``枚举| _上驼箱`PixelFormat`枚举成员| _大蛇案_ | RGB_888

 
### Libraries  图书馆 

 
#### Syntax  句法 

Library names are period-separated lists of identifiers. Portions of the library name other than the last are also referred to as namespaces. Each component ofthe name is in lowercase and must match the following regular expression:`[a-z][a-z0-9]*`. 库名称是句点分隔的标识符列表。库名称中除最后一个以外的其他部分也称为名称空间。名称的每个组成部分均使用小写字母，并且必须匹配以下正则表达式：[[a-z] [a-z0-9] *`。

We use these restrictive rules because different target languages have different restrictions on how they qualify namespaces, libraries, or packages. We haveselected a conservative least common denominator in order for FIDL to work wellwith our current set of target languages and with potential future targetlanguages. 我们使用这些限制性规则是因为不同的目标语言对它们如何限定名称空间，库或包有不同的限制。我们选择了一个保守的最小公分母来使FIDL与我们当前的目标语言以及潜在的未来目标语言配合使用。

 
#### Identifier Names: Prefer Functional Roles with Meaning  标识符名称：具有含义的功能角色 

Prefer functional names (e.g., `fuchsia.media`) over product or code names (e.g., `fuchsia.amber` or `fuchsia.scenic`).  Product names are appropriatewhen the product has some external existence beyond Fuchsia and when theprotocol is specific to that product.  For example, `fuchsia.cobalt` is abetter name for the Cobalt interface protocol than `fuchsia.metrics` becauseother metrics implementations (e.g., Firebase) are unlikely to implement the sameprotocol. 优先使用功能名称（例如，“ fuchsia.media”）而不是产品或代码名称（例如，“ fuchsia.amber”或“ fuchsia.scenic”）。当产品在紫红色之外具有某种外部存在时，并且该协议特定于该产品时，则使用产品名称。例如，“ fuchsia.cobalt”比“ fuchsia.metrics”是Cobalt接口协议的更好的名称，因为其他度量标准实现（例如Firebase）不太可能实现相同的协议。

Identifier names should relate to the specific *role* that participants play; avoid encoding access control into the name. Names based on roles aredescriptive and won't outdate as quickly as names based on access control, whichprescribe an externally-defined relationship that is subject to change as theplatform evolves. For example, for an API involving `FocusChain` objects, anappropriate name would be `fuchsia.ui.focus`, instead of`fuchsia.ui.privileged`; if we decide to make `FocusChain` objects more widelyaccessible, then `fuchsia.ui.focus` isn't a problematic name.  The followingexample words should be avoided: 标识符名称应与参与者所扮演的特定角色相关。避免将访问控制编码为名称。基于角色的名称具有描述性，并且不会像基于访问控制的名称那样过时。基于访问控制的名称规定了外部定义的关系，该关系会随着平台的发展而改变。例如，对于涉及“ FocusChain”对象的API，适当的名称应为“ fuchsia.ui.focus”，而不是“ fuchsia.ui.privileged”；如果我们决定使“ FocusChain”对象更易于访问，则“ fuchsia.ui.focus”并不是一个有问题的名称。应避免使用以下示例词：

 
* `constrained`  *`受限制的`
* `limited`  *`受限`
* `oem`  *`oem`
* `private`  *`私人`
* `privileged`  *`特权`
* `protected`  *`受保护的`
* `special`  *`特殊`
* `vendor`  *`供应商`

Identifier names should have meaning; avoid meaningless names. If `fuchsia.foo.bar` and `fuchsia.foo.baz` share a number of concepts that youwish to factor out into a separate library, consider defining those concepts in`fuchsia.foo` rather than in `fuchsia.foo.common`. The following example wordsshould be avoided: 标识符名称应具有含义；避免使用无意义的名称。如果`fuchsia.foo.bar`和`fuchsia.foo.baz`共享许多您想分解到单独库中的概念，请考虑在`fuchsia.foo`中而不是在`fuchsia.foo.common中定义这些概念。 `。应避免使用以下示例单词：

 
* `common`  *`common`
* `service`  *`服务`
* `util`  *`util`
* `base`  *`base`
* `f<letter>l`  *`f <字母> l`
* `zx<word>`  *`zx <word>`

 
#### Fuchsia Libraries  紫红色的图书馆 

FIDL libraries defined in the Platform Source Tree (i.e., defined in fuchsia.googlesource.com) must be in the `fuchsia` top-level namespace (e.g.,`fuchsia.ui`) unless (a) the library defines portions of the FIDL languageitself or its conformance test suite, in which case the top-level namespace mustbe `fidl`, or (b) the library is used only for internal testing and is notincluded in the SDK or in production builds, in which case the top-levelnamespace must be `test`. 在平台源代码树中定义的FIDL库（即在fuchsia.googlesource.com中定义）必须位于“ fuchsia”顶级命名空间（例如“ fuchsia.ui”）中，除非（a）库定义了FIDL的一部分语言本身或它的一致性测试套件，在这种情况下，顶级名称空间必须为“ fidl”，或者（b）该库仅用于内部测试，并且不包含在SDK或生产版本中，在这种情况下，顶级命名空间必须是“测试”。

FIDL libraries defined in the Platform Source Tree for the purpose of exposing hardware functionality to applications must be in the `fuchsia.hardware`namespace.  For example, a protocol for exposing an ethernet device mightbe named `fuchsia.hardware.ethernet.Device`.  Higher-level functionality builton top of these FIDL protocols does not belong in the `fuchsia.hardware` namespace.For example, it is more appropriate for network protocols to be under`fuchsia.net` than `fuchsia.hardware`. 为了向应用程序公开硬件功能，在平台源树中定义的FIDL库必须位于“ fuchsia.hardware”命名空间中。例如，用于公开以太网设备的协议可能被命名为“ fuchsia.hardware.ethernet.Device”。这些FIDL协议之上构建的高级功能不属于`fuchsia.hardware`命名空间。例如，网络协议位于`fuchsia.net`下比`fuchsia.hardware'更合适。

 
#### Namespace Nesting: Not Too Deeply  命名空间嵌套：不太深入 

Avoid library names with more than two dots (e.g., `fuchsia.foo.bar.baz`). There are some cases when a third dot is appropriate, but those cases are rare.If you use more than two dots, you should have a specific reason for thatchoice.  For the case of the `fuchsia.hardware` namespace described above, thisis relaxed to "three" and "four" dots, instead of "two" and "three", toaccomodate the longer namespace. 避免使用超过两个点的库名称（例如，`fuchsia.foo.bar.baz`）。在某些情况下，第三个点是合适的，但这种情况很少见。如果使用两个以上的点，则应该有一个选择的特定原因。对于上述的“ fuchsia.hardware”命名空间，此位置放宽到“三个”和“四个”点，而不是“两个”和“三个”，以适应较长的命名空间。

 
#### Library Dependencies  图书馆依赖 

Prefer to introduce dependencies from libraries with more specific names to libraries with less specific names rather than the reverse.  For example,`fuchsia.foo.bar` might depend on `fuchsia.foo`, but `fuchsia.foo` should notdepend on `fuchsia.foo.bar`.  This pattern is better for extensibility becauseover time we can add more libraries with more specific names but there are onlya finite number of libraries with less specific names.  Having libraries withless specific names know about libraries with more specific names privileges thecurrent status quo relative to the future. 最好从名称更具体的库到名称更不具体的库（而不是相反）引入依赖关系。例如，`fuchsia.foo.bar`可能依赖于`fuchsia.foo`，但是`fuchsia.foo`不应该依赖于`fuchsia.foo.bar`。这种模式对于扩展性更好，因为随着时间的流逝，我们可以添加更多具有更特定名称的库，但是只有有限数量的具有较不特定名称的库。让没有特定名称的库知道具有更多特定名称的库，这些特权赋予相对于将来的当前现状。

 
### Top-level  顶层 

Avoid repeating the names from the library name.  For example, in the `fuchsia.process` library, a protocol that launches process should be named`Launcher` rather than `ProcessLauncher` because the name `process` alreadyappears in the library name.  In all target languages, top-level names arescoped by the library name in some fashion. 避免从库名称中重复名称。例如，在“ fuchsia.process”库中，启动进程的协议应命名为“ Launcher”而不是“ ProcessLauncher”，因为库名称中已经出现了“ process”名称。在所有目标语言中，顶级名称都以某种方式由库名称限定。

 
### Primitive aliases  原始别名 

Primitive aliases must not repeat names from the enclosing library.  In all target languages, primitive aliases are replaced by the underlying primitivetype and therefore do not cause name collisions. 原始别名不得重复包含库中的名称。在所有目标语言中，原始别名都由基础原始类型替换，因此不会引起名称冲突。

```fidl
using vaddr = uint64;
```
 

 
### Constants  常数 

Constant names must not repeat names from the enclosing library.  In all target languages, constant names are scoped by their enclosing library. 常量名称不得重复包含库中的名称。在所有目标语言中，常量名称受其封闭库的限制。

Constants that describe minimum and maximum bounds should use the prefix `MIN_` and `MAX_`, respectively. 描述最小和最大边界的常量应分别使用前缀“ MIN_”和“ MAX_”。

```fidl
const uint64 MAX_NAMES = 32;
```
 

 
### Protocols  通讯协定 

Protocols are specified with the `protocol` keyword.  协议使用关键字“ protocol”指定。

Protocols must be noun phrases. Typically, protocols are named using nouns that suggest an action.  Forexample, `AudioRenderer` is a noun that suggests that the protocol is relatedto rendering audio.  Similarly, `Launcher` is a noun that suggests that theprotocol is related to launching something.  Protocols can also be passivenouns, particularly if they relate to some state held by the implementation.For example, `Directory` is a noun that suggests that the protocol is used forinteracting with a directory held by the implementation. 协议必须是名词短语。通常，协议使用建议动作的名词来命名。例如，“ AudioRenderer”是一个名词，表明协议与渲染音频有关。类似地，“ Launcher”是一个名词，暗示该协议与发射某物有关。协议也可以是被动名词，尤其是当它们与实现所拥有的某种状态有关时。例如，“ Directory”是一个名词，表明协议用于与实现所拥有的目录进行交互。

A protocol may be named using object-oriented design patterns.  For example, `fuchsia.fonts.Provider` uses the `provider` suffix, which indicates that theprotocol provides fonts (rather than represents a font itself).  Similarly,`fuchsia.tracing.Controller` uses the `controller` suffix, which indicates thatthe protocol controls the tracing system (rather than represents a traceitself). 可以使用面向对象的设计模式来命名协议。例如，“ fuchsia.fonts.Provider”使用“ provider”后缀，表示该协议提供字体（而不是表示字体本身）。类似地，“ fuchsia.tracing.Controller”使用“ controller”后缀，这表示协议控制跟踪系统（而不是代表跟踪自身）。

The name `Manager` may be used as a name of last resort for a protocol with broad scope.  For example, `fuchsia.power.Manager`. However, be warned that"manager" protocols tend to attract a large amount of loosely relatedfunctionality that might be better factored into multiple protocols. 名称“ Manager”可以用作范围广泛的协议的不得已的名称。例如，`fuchsia.power.Manager`。但是，请注意，“管理器”协议倾向于吸引大量松散相关的功能，而这些功能可能会更好地分解为多个协议。

Protocols must not include the name `service.` All protocols define services. The term is meaningless. For example, `fuchsia.net.oldhttp.HttpService`violates this rubric in two ways.  First, the `http` prefix is redundant withthe library name. Second, the `service` suffix is banned.Notice that the successor library simply omits this altogether by beingexplicit in naming the service it offers `fuchsia.net.http.Loader`. 协议不得包含名称“ service”。所有协议均定义服务。该术语毫无意义。例如，“ fuchsia.net.oldhttp.HttpService”以两种方式违反了该规定。首先，`http`前缀对于库名是多余的。其次，禁止使用“ service”后缀。注意，后继库只是通过明确命名其提供的“ fuchsia.net.http.Loader”服务而完全忽略了这一点。

 
#### Methods  方法 

Methods must must be verb phrases.  方法必须是动词短语。

For example, `GetBatteryStatus` and `CreateSession` are verb phrases that indicate what action the method performs. 例如，“ GetBatteryStatus”和“ CreateSession”是动词短语，指示方法执行的操作。

Methods on `listener` or `observer` protocols that are called when an event occurs should be prefixed with `On` and describe the event that occurred in thepast tense.  For example, the `ViewContainerListener` protocol has a methodnamed `OnChildAttached`. 事件发生时调用的侦听器或观察者协议的方法应以“开”作为前缀，并描述过去时发生的事件。例如，ViewContainerListener协议具有名为OnChildAttached的方法。

 
#### Events  大事记 

Similarly, events (i.e., unsolicited messages from the server to the client) should be prefixed with `On` and describe the event that occurred in the pasttense. 类似地，事件（即，从服务器到客户端的未经请求的消息）应该以“ On”作为前缀，并描述发生在过去状态中的事件。

For example, the `AudioCapturer` protocol has an event named `OnPacketCaptured`. 例如，“ AudioCapturer”协议具有一个名为“ OnPacketCaptured”的事件。

 
### Structs, unions, xunions, and tables  结构，联合，索环和桌子 

Structs, unions, xunions, and tables must be noun phrases. For example, `Point` is a struct that defines a location in space and`KeyboardEvent` is a struct that defines a keyboard-related event. 结构，联合，xunion和表必须是名词短语。例如，“ Point”是一个定义空间位置的结构，而“ KeyboardEvent”是一个定义键盘相关事件的结构。

 
### Struct, union, xunion, and table members  结构，联合，xunion和表成员 

Prefer struct, union, xunion, and table member names with a single word when practical (single-word names render more consistently across target languages).However, do not be afraid to use multiple words if a single word would beambiguous or confusing. 在可行的情况下，最好使用单个单词来表示结构，联合，统一名和表成员的名称（单个单词的名称在目标语言之间的呈现更加一致），但是如果单个单词会造成歧义或混淆，不要害怕使用多个单词。

Member names must not repeat names from the enclosing type (or library) unless the member name is ambiguous without a name from the enclosing type.  Forexample, a member of type `KeyboardEvent` that contains the time the event wasdelivered should be named `time`, rather than `event_time`, because the name`event` already appears in the name of the enclosing type. In all targetlanguages, member names are scoped by their enclosing type. 成员名称不得重复使用封闭类型（或库）的名称，除非成员名称不明确而不包含封闭类型的名称。例如，包含事件交付时间的KeyboardEvent类型的成员应命名为time而不是event_time，因为名称event已出现在封闭类型的名称中。在所有目标语言中，成员名称受其封闭类型的限制。

However, a type `DeviceToRoom`, that associates a smart device with the room it's located in, may need to have members `device_id` and `room_name`, because`id` and `name` are ambiguous. Either of these could refer to either the deviceor the room. 但是，将智能设备与其所在房间相关联的类型“ DeviceToRoom”可能需要具有“ device_id”和“ room_name”成员，因为“ id”和“ name”不明确。这些都可以指设备或房间。

 
### Enums  枚举 

Enums must be noun phrases.  枚举必须是名词短语。

For example, `PixelFormat` is an enum that defines how colors are encoded into bits in an image. 例如，“ PixelFormat”是一个枚举，它定义如何将颜色编码为图像中的位。

 
### Enum members  枚举成员 

Enum member names must not repeat names from the enclosing type (or library). For example, members of `PixelFormat` enum should be named `ARGB` rather than`PIXEL_FORMAT_ARGB` because the name `PIXEL_FORMAT` already appears in the nameof the enclosing type. In all target languages, enum member names are scoped bytheir enclosing type. 枚举成员名称不得重复包含类型（或库）的名称。例如，“ PixelFormat”枚举的成员应命名为“ ARGB”而不是“ PIXEL_FORMAT_ARGB”，因为名称“ PIXEL_FORMAT”已经出现在封闭类型的名称中。在所有目标语言中，枚举成员名称的范围取决于其封闭类型。

 
### Bitfields  位域 

Bitfields must be noun phrases.  位域必须是名词短语。

For example, `InfoFeatures` is a bitfield that indicates which features are present on an Ethernet interface. 例如，“ InfoFeatures”是一个位域，指示以太网接口上存在哪些功能。

 
### Bitfield members  位域成员 

Bitfield members must not repeat names from the enclosing type (or library). For example, members of `InfoFeatures` bitfield should be named `WLAN`rather than `INFO_FEATURES_WLAN` because the name `INFO_FEATURES` alreadyappears in the name of the enclosing type.In all target languages, bitfield member names are scoped by theirenclosing type. 位域成员不得重复使用封闭类型（或库）的名称。例如，InfoFeatures位域的成员应命名为WLAN，而不是INFO_FEATURES_WLAN，因为名称INFO_FEATURES已经出现在封闭类型的名称中。在所有目标语言中，位域成员名均以其封闭类型为范围。

 
## Organization  组织 

 
### Syntax  句法 

 
 * Use 4 space indents.  *使用4个空格缩进。
 * Never use tabs.  *切勿使用标签。
 * Avoid trailing whitespace.  *避免尾随空格。
 * Separate declarations for `bits`, `enum`, `protocol`, `struct`, `table`, `table`, `union`, and `xunion` constructs from other declarations withone blank line (two consecutive newline characters). *位，枚举，协议，协议，结构，表，表，union和xunion的声明与其他带有空格（两个连续换行符）的声明分开。
 * End files with exactly one newline character.  *仅使用一个换行符结束文件。

 
### Comments  评论 

Comments use `///` (three forward slashes). Comments in a library will also appear in the generated code to ease development when coding against thelibrary. We say that comments "flow-through" to the target language. 注释使用`///`（三个斜杠）。库中的注释也将出现在生成的代码中，以简化在对库进行编码时的开发。我们说注释“直通”到目标语言。

Place comments above the thing being described. Except in the cases listed below, use reasonably complete sentences with proper capitalization andperiods. Limit comment widths to 80 characters unless a longer comment isunavoidable (e.g., for a long URL). 将注释放在要描述的内容上方。除下面列出的情况外，请使用适当的完整句子并加上适当的大写字母和句号。将注释宽度限制为80个字符，除非不可避免地需要较长的注释（例如，对于较长的URL）。

Comments should be written in Markdown. We rely on the [CommonMark](http://www.commonmark.org) specification for our markdown. Sometools may render output using other Markdown standards; in cases where your tooldoes not use CommonMark, we encourage developers to write Markdown that iscompatible with both CommonMark and their tool. References to FIDL elementsshould always be in code font. 评论应使用Markdown编写。我们使用[CommonMark]（http://www.commonmark.org）规范进行降价。有些工具可能会使用其他Markdown标准渲染输出；如果您的工具不使用CommonMark，我们鼓励开发人员编写与CommonMark及其工具兼容的Markdown。对FIDL元素的引用应始终使用代码字体。

A documented entity is any FIDL element that has a comment attached. The first reference to any documented entity in a comment should be given with its fullyqualified name, in the form ``[`<library>/<top level declaration>.<member>`]``(e.g., ``[`fuchsia.io/Node.clone`]``). This form may generate a hyperlink, ifthe tooling supports it.  Subsequent references to that documented entity canuse an abbreviated version, as long as that abbreviated version is unambiguous(e.g., `clone`). The form without brackets does not generate a hyperlink. 文件实体是任何带有注释的FIDL元素。注释中对任何文档化实体的首次引用应以其全限定名给出，形式为“ [`<library> / <顶级声明>。<member>`]”（例如，“ [`紫红色.io / Node.clone`]``）。如果工具支持，则此表单可能会生成超链接。只要该缩写版本是明确的（例如“ clone”），随后对该文档实体的引用都可以使用缩写版本。不带括号的表单不会生成超链接。

Request parameters, response parameters, and error types should be documented as lists of the form: 请求参数，响应参数和错误类型应记录为以下形式的列表：

```fidl
+ request `param1` <description>
+ request `param2` <description>
- response `param1` <description>
- response `param2` <description>
* error <description>
```
 

Requests, responses, and errors must appear in that order. A given set of parameters must also follow the order in which they were declared in theparameter list.  The terms "request" and "response" may be elided if theparameter names are only found in one of the request or response parameter list. 请求，响应和错误必须按该顺序出现。一组给定的参数还必须遵循在参数列表中声明的顺序。如果仅在请求或响应参数列表之一中找到参数名称，则可以省略术语“请求”和“响应”。

The first part of a doc comment describing a variable, field, or type should be a noun phrase that briefly states the intended purpose of the documented entity,including information that cannot be deduced from the name and type. Thedescription should be terminated with a period. The description should notreiterate the name of the documented entity, or its particular type of FIDLlanguage element (e.g., `struct` or `protocol`). 说明变量，字段或类型的文档注释的第一部分应为名词短语，以简要说明所记录实体的预期目的，包括无法从名称和类型推导出的信息。该说明应以句号终止。该描述不应重复文档实体的名称或FIDLlanguage元素的特定类型（例如，“ struct”或“ protocol”）。

```fidl
/// A representation of violins displayed on the screen.
struct Widget {
    /// A monotonically increasing id, uniquely identifying the widget.
    uint64 id;
    /// Location of the top left corner of the widget.
    Point location;
};
```
 

The following are examples of what you should not do:  以下是不应执行的操作的示例：

```fidl
/// BAD: Widget is a representation of violins displayed on the screen.
/// BAD: struct Widget is a representation of violins displayed on the screen.
```
 

The first part of a doc comment attached to a protocol method should be a brief description of the behavior of that method, starting with a verb, includinginformation that cannot be deduced from the name and type. The verb should bewritten in the present tense, agree with a third person singular pronoun, anduse the indicative mood (this effectively means that you should pretend the word"it" comes before the verb, and that you are making a statement of fact).  Thephrase should end with a period. 附加到协议方法上的文档注释的第一部分应该是该方法的行为的简要描述，以动词开头，包括不能从名称和类型推断出的信息。该动词应以现在时书写，并与第三人称单数代词一致，并使用指示性语气（这实际上意味着您应假装“ it”一词出现在动词之前，并且您要陈述事实）。该短语应以句号结尾。

A full example:  一个完整的例子：

```fidl

/// An abstract representation of a [`fuchsia.io/Node`] whose layout is flat.
protocol File {
    compose Node;

    /// Acquires a [`fuchsia.mem/Buffer`] representing this file, if
    /// there is one, with the requested access rights.
    ///
    /// ## Rights
    ///
    /// This method requires the following rights:
    ///
    /// * [`fuchsia.io/OPEN_RIGHT_WRITABLE`] if `flags` includes
    ///   [`fuchsia.io/VMO_FLAG_WRITE`].
    /// * [`fuchsia.io/OPEN_RIGHT_READABLE`] if `flags` includes
    ///   [`fuchsia.io/VMO_FLAG_READ`] or [`fuchsia.io/VMO_FLAG_EXEC`].
    ///
    /// + request `flags` a bit field composing any of
    ///     `VMO_FLAG_READ`, `VMO_FLAG_WRITE`, or `VMO_FLAG_EXEC`.
    /// - response `buffer` the requested `fuchsia.mem/Buffer`, or
    ///     null if there was an error, or the buffer does not exist.
    /// * error a zx_status value indicating success or failure.
    /// * see [`fuchsia.mem/Buffer`]
    /// [`fuchsia.mem/Buffer`]:
    ///    https://fuchsia.googlesource.com/fuchsia/+/9853fad50ca70256f0e86201c0e20424f1c25ab5/zircon/system/fidl/fuchsia-io/io.fidl
    GetBuffer(uint32 flags) ->
        (fuchsia.mem.Buffer? buffer) error zx.status;
};
```
 

Types or values defined by some external source of truth should be commented with references to the external thing. For example, reference the WiFispecification that describes a configuration structure.  Similarly, if astructure must match an ABI defined in a C header, reference the C header. 由某些外部真理来源定义的类型或值应通过引用外部事物进行注释。例如，请参考描述配置结构的WiFi规范。同样，如果结构必须与C标头中定义的ABI相匹配，请引用C标头。

For more information about what your comments should contain, see the [API Documentation Rubric](/docs/development/api/documentation.md). 有关注释应包含的内容的更多信息，请参见[API文档规则]（/ docs / development / api / documentation.md）。

 
#### Referencing FIDL protocols or protocol methods  引用FIDL协议或协议方法 

References to FIDL protocols or their methods in comments should follow the pattern: 在注释中引用FIDL协议或其方法应遵循以下模式：

```fidl
/// See fuchsia.library/ProtocolName.Method for more information.
```
 

When referring to a protocol in the same library as the comment, the library name may be left off: `ProtocolName.Method`. 当在注释中引用同一库中的协议时，库名称可能会保留：“ ProtocolName.Method”。

Similarly, when referring to a method in the same protocol as the comment, the library name and protocol name may be left off: `Method`. 类似地，当使用与注释相同的协议引用方法时，库名称和协议名称可以省去：“方法”。

 
#### Library Overview  图书馆概况 

You can provide a library overview as a documentation comment on the `library` statement. The 'library' statement starts FIDL files. For example: 您可以提供库概述作为对`library`语句的文档注释。 'library'语句启动FIDL文件。例如：

```fidl
/// Overview of fuchsia.library.
library fuchsia.library;

...
```
 

Library overviews should provide general documentation to define the library. They may also provide a detailed introduction to various messages, definedprotocols, and how the messages and protocols are used together. 库概述应提供定义库的常规文档。他们还可以提供各种消息，已定义的协议以及如何将消息和协议一起使用的详细介绍。

While a library can be broken down in multiple FIDL [Files](#files), there can only be a single library overview. Consider these recommendations for libraryoverviews: 虽然一个库可以分解为多个FIDL [Files]（文件），但只能有一个库概述。考虑以下有关图书馆概述的建议：

 
 * If the overview is short and the library consists of a single file, you can place the overview in the `library` statement at the top of the library file. *如果概述很短，并且库由一个文件组成，则可以将概述放在库文件顶部的“ library”语句中。
 * If the library consists of multiple files, create a standalone file `overview.fidl` to document the library. The 'overview.fidl' file should notcontain any declarations, type aliases, or protocol definitions. *如果库包含多个文件，则创建一个独立文件`overview.fidl`来记录该库。 “ overview.fidl”文件不应包含任何声明，类型别名或协议定义。

 
#### Non flow-through comments  非直通评论 

If your comments are meant for library authors, use the simpler comments `//` (two forward slashes) which do not flow-through to the target language. 如果您的注释是给图书馆作者的，请使用更简单的注释“ //”（两个正斜杠），它们不会直达目标语言。

When deciding what should be a regular `///` comment versus a non flow-through comment, keep in mind the following. 在决定应使用常规“ ///”注释而不是非流通注释时，请记住以下几点。

Regular comments:  定期评论：

 
 * Descriptions of parameters, arguments, function  *参数，参数，函数的描述
 * Usage notes  *使用说明

Non flow-through comments:  非直通评论：

 
 * Internal "todo" comments  *内部“待办事项”评论
 * Copyright notices  *版权声明
 * Implementation details  *实施细节

Both style of comments can be combined:  两种注释风格可以组合使用：

```fidl
/// A widget displaying violins on the screen.
// TODO -- widgets should use UUIDs instead of sequential ids
struct Widget {
    /// A monotonically increasing id, uniquely identifying the widget.
    uint64 id;
    /// Location of the top left corner of the widget.
    ...
};
```
 

 
### Files {#files}  文件{files} 

A library is comprised of one or more files.  The files are stored in a directory hierarchy with the following conventions: 库由一个或多个文件组成。这些文件按照以下约定存储在目录层次结构中：

```fidl
fidl/<library>/[<dir>/]*<file>.fidl
```
 

The `<library>` directory is named using the dot-separated name of the FIDL library.  The `<dir>` subdirectories are optional and typically not used forlibraries with less than a dozen files.  This directory structure matches howFIDL files are included in the Fuchsia SDK. 目录<library>是使用FIDL库的点分隔名称命名的。子目录<dir>是可选的，通常不用于文件少于十二个的库。此目录结构与Fuchsia SDK中包含FIDL文件的方式匹配。

The division of a library into files has no technical impact on consumers of the library. Declarations, including protocols, can reference each other andthemselves throughout the library, regardless of the file in which they appear.Divide libraries into files to maximize readability. 将库分为文件对库的使用者没有技术影响。声明（包括协议）可以在整个库中相互引用，也可以在整个库中相互引用，无论它们出现在哪个文件中。请将库分为文件以最大程度地提高可读性。

 
 * Prefer a DAG dependency diagram for files in a library.  *对于库中的文件，最好使用DAG依赖关系图。
 * Prefer keeping mutually referring definitions textually close to each other, ideally in the same file. *最好使相互引用的定义在文本上彼此靠近，最好在同一文件中。
 * For complex libraries, prefer defining pure data types or constants in leaf files and defining protocols that reference those types together in a trunkfile. *对于复杂的库，最好在叶文件中定义纯数据类型或常量，并在中继文件中定义将这些类型一起引用的协议。

