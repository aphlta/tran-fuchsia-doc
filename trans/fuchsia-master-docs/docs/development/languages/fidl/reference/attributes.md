 
# FIDL Attributes  FIDL属性 

The following FIDL attributes are supported:  支持以下FIDL属性：

 
* [`[Deprecated]`](#deprecated)  * [`[不推荐使用]`]（不推荐使用）
* [`[Discoverable]`](#discoverable)  * [`[Discoverable]`]（可发现）
* [`[Doc]`](#doc)  * [`[Doc]`]（doc）
* [`[FragileBase]`](#fragilebase)  * [`[FragileBase]`]（fragilebase）
* [`[Internal]`](#internal)  * [`[Internal]`]（内部）
* [`[Layout]`](#layout)  * [`[Layout]`]（布局）
* [`[MaxBytes]`](#maxbytes)  * [`[MaxBytes]`]（maxbytes）
* [`[MaxHandles]`](#maxhandles)  * [`[MaxHandles]`]（maxhandles）
* [`[Selector]`](#selector)  * [`[选择器]`]（选择器）
* [`[Transitional]`](#transitional)  * [`[Transitional]`]（过渡）
* [`[Transport]`](#transport)  * [`[运输]`]（运输）

 
## Scope  范围 

An attribute preceeds a FIDL element, for example:  属性位于FIDL元素之前，例如：

```fidl
[Layout = "Simple"]
protocol MyProtocol {...
```
 

It's used to either modify the characteristics of the element, or provide documentation. 它用于修改元素的特征或提供文档。

Note: The attribute applies *only* to the *next* element, not all subsequent ones.Elements after the current one revert to having no attributes. 注意：该属性仅将* next *应用于* next *元素，而不是所有后续元素。当前元素之后的元素将恢复为无属性。

 
## Syntax  句法 

Attributes may include multiple values, and multiple attributes may be specified in the same element, for example: 属性可以包括多个值，并且可以在同一元素中指定多个属性，例如：

```fidl
[Layout = "Simple", Transport = "Channel"]
```
 

Illustrates both aspects:  说明了两个方面：
* there are two attributes, `Layout` and `Transport`, and  *有两个属性，即“布局”和“运输”，以及
* the `Transport` attribute takes a value from the list enumerated below.  *`Transport`属性从下面列举的列表中获取一个值。

 
## `[Deprecated]` {#deprecated}  `[Deprecated]`{deprecated} 

**USAGE**: `[Deprecated]`  **用法**：`[不推荐使用]`

**MEANING**: See [FTP-013]. **含义**：请参见[FTP-013]。

Note: Not implemented.  注意：未实现。

 
## `[Discoverable]` {#discoverable}  `[Discoverable]`{discoverable} 

**USAGE**: `[Discoverable]`  **用法**：`[可发现]`

**MEANING**: Causes the service's name to be made available for lookup.A service with a `[Discoverable]` attribute can be found at run-time.That is to say, you can "request" this service, and zircon will locate itand provide access to it. ** MEANING **：使该服务的名称可用于查找。可以在运行时找到具有`[Discoverable]`属性的服务。也就是说，您可以“请求”该服务，并使用zircon将找到它并提供对其的访问。

 
## `[Doc]` {#doc}  `[Doc]`{doc} 

**USAGE**: `[Doc = "`_string_`"]`  **用法**：`[Doc =“`_string_`”]`

**MEANING**: In FIDL, comments can start with two ("`//`") or three slashes ("`///`"),or they can be embodied within a `[Doc]` attribute.The two-slash variant does not propagate the comments to the generatedtarget, whereas both the three-slash and `[Doc]` variants do. **含义**：在FIDL中，注释可以以两个（“ //`”）或三个斜杠（“ ///`”）开头，也可以包含在`[Doc]`属性中。两斜杠变体不会将注释传播到生成的目标，而三斜杠变体和[Doc]变体都可以。

That is:  那是：

```fidl
/// Foo
struct MyFooStruct { ...
```
 

and  和

```fidl
[Doc = "Foo"]
struct MyFooStruct { ...
```
 

have the same effect &mdash; one ("`///`") is syntactic sugar for the other. The text of the comment isemitted into the generated code, in a manner compatible with the syntax ofthe target language. 具有相同的效果-一个（“ ///`”）是另一个的语法糖。注释文本以与目标语言的语法兼容的方式发送到生成的代码中。

Note: To be identical, the `[Doc]` version should be `[Doc = " Foo\n"]`. Note the space before the "Foo" and the line-feed "`\n`". 注意：为了相同，`[Doc]`版本应为`[Doc =“ Foo \ n”]`。注意“ Foo”和换行符“`\ n`”之前的空格。

 
## `[FragileBase]` {#fragilebase}  `[FragileBase]`{fragilebase} 

**USAGE**: `[FragileBase]`  **用法**：`[FragileBase]`

**MEANING**: Denotes that the interface can be composed, otherwise it cannot.See also [Protocol Composition][composition]. ** MEANING **：表示可以组成接口，否则不能组成。另请参见[协议组成] [组成]。

 
## `[Internal]` {#internal}  `[Internal]`{internal} 

**USAGE**: `[Internal]`  **用法**：`[内部]

**MEANING**: This marks internal libraries, such as library `zx`.It should be used only by Fuchsia developers. **意味**：这标记了内部库，例如库`zx`，它只能由Fuchsia开发人员使用。

 
## `[Layout]` {#layout}  `[Layout]`{layout} 

**USAGE**: `[Layout = "`_layout_`"]`  **用法**：`[Layout =“`_layout_`”]``

**MEANING**: This attribute currently has one valid value, `Simple`, and is meaningfulonly on protocols. ** MEANING **：该属性当前具有一个有效值`Simple`，仅在协议上有意义。

It's used to indicate that all arguments and returns must contain objects that are of a fixed size.The arguments and returns themselves, however, can be dynamically sizedstrings or vectors of primitives. 它用于指示所有参数和返回值必须包含固定大小的对象。但是，参数和返回值本身可以是动态大小的字符串或基元向量。

To clarify with an example, the following is valid:  为了举例说明，以下内容是有效的：

```fidl
[Layout = "Simple"]
protocol MyProtocol {
    DynamicCountOfFixedArguments(vector<uint8>:1024 inputs);
};
```
 

Here, the argument is a dynamically sized `vector` of unsigned 8-bit integers called `inputs`, with a maximum bound of 1024 elements. 在这里，参数是一个动态大小的，由无符号的8位整数组成的“向量”，称为“输入”，最大范围为1024个元素。

The benefit of `[Layout = "Simple"]` is that the data can be directly mapped without having to be copied and assembled. [[Layout =“ Simple”]]的好处是可以直接映射数据，而不必复制和组合。

 
## `[MaxBytes]` {#maxbytes}  `[MaxBytes]`{maxbytes} 

**USAGE**: `[MaxBytes = "`_number_`"]`  **用法**：`[MaxBytes =“`_number_`”]`

**MEANING**: This attribute is used to limit the number of bytes that can be transferredin a message.The compiler will issue an error if the number of bytes exceeds this limit. ** MEANING **：此属性用于限制消息中可传输的字节数。如果字节数超过此限制，则编译器将发出错误。

 
## `[MaxHandles]` {#maxhandles}  `[MaxHandles]`{maxhandles} 

**USAGE**: `[MaxHandles = "`_number_`"]`  **用法**：`[MaxHandles =“`_number_`”]`

**MEANING**: This attribute is used to limit the number of handles that can betransferred in a message.The compiler will issue an error if the number of handles exceeds this limit. ** MEANING **：此属性用于限制消息中可以传输的句柄数。如果句柄数超过此限制，则编译器将发出错误。

 
## `[Selector]` {#selector}  `[选择器]`{选择器} 

**USAGE**: `[Selector = "`_selector_`"]`  **用法**：`[Selector =“`_selector_`”]`

**MEANING**: Allows you to change the hashing basis for the method ordinal, see[FTP-020]. ** MEANING **：允许您更改方法序号的哈希基础，请参阅[FTP-020]。

It can be used to rename a method without breaking ABI compatibility. For example, if we wish to rename the `Investigate` method to `Experiment`in the `Science` interface, we can write: 它可用于重命名方法而不会破坏ABI兼容性。例如，如果我们希望在“科学”界面中将“调查”方法重命名为“实验”，则可以编写：

```fidl
interface Science {
    [Selector="Investigate"] Experiment();
};
```
 

It can also be used for `xunion` variants to keep ABI compatibility in the same way. 它也可以用于`xunion`变体，以相同的方式保持ABI兼容性。

 
## `[Transitional]` {#transitional}  `[Transitional]`{transitional} 

**USAGE**: `[Transitional = "`_description_`"]`  **用法**：`[过渡=“`_description_`”]`

**MEANING**: Instructs bindings to generate code that will successfully build, regardless ofwhether the method is implemented or not.[FTP-021] contains more details. ** MEANING **：指示绑定以生成将成功构建的代码，而不管该方法是否实现。[FTP-021]包含更多详细信息。

 
## `[Transport]` {#transport}  `[运输]`{运输} 

**USAGE**: `[Transport = "`_tranportList_`"]`  **用法**：`[Transport =“`_tranportList_`”]`

**MEANING**: Allows you to select a transport.Provide a comma-separated list of values, selected from: ** MEANING **：允许您选择一种传输方式。提供逗号分隔的值列表，该值选自：

 
* `Channel` &mdash; use a [Zircon channel][channel].  *`Channel` mdash;使用[锆石频道] [频道]。
* `Syscall` &mdash; transport used to specify that the protocol is used to define Zircon syscalls, rather than typical IPC. *`Syscall` mdash;用于指定协议用于定义Zircon系统调用的传输，而不是典型的IPC。

The default is `Channel` if none specified. If you do specify a value or values, then only those values are used (e.g.,specifying `[Transport="Foo"]` disables `Channel` and uses only`Foo`). 如果未指定，则默认为“通道”。如果您确实指定一个或多个值，则仅使用那些值（例如，指定“ [Transport =“ Foo”]“会禁用“ Channel”，而仅使用“ Foo”）。

