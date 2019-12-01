 
# Low-Level C++ Language FIDL Tutorial  低级C ++语言FIDL教程 

[TOC]  [目录]

 
## About this tutorial  关于本教程 

This tutorial describes how to make client calls and write servers in C++ using the Low-Level C++ Bindings (LLCPP). 本教程描述了如何使用底层C ++绑定（LLCPP）在C ++中进行客户端调用和编写服务器。

[Getting Started](#getting-started) has a walk-through of using the bindings with an example FIDL library. The [reference](#reference) section documentsthe detailed bindings interface and design. [入门]（入门）具有将绑定与示例FIDL库一起使用的演练。 [reference]（参考）部分记录了详细的绑定界面和设计。

See [Comparing C, Low-Level C++, and High-Level C++ Language Bindings](c-family-comparison.md) for a comparative analysis of the goals anduse cases for all the C-family language bindings. 有关对所有C系列语言绑定的目标和用例的比较分析，请参见[比较C，低级C ++和高级C ++语言绑定]（c-family-comparison.md）。

Note: LLCPP is in currently in beta. The bindings are designed to exploit the compatibility between FIDL wire-format and C++ memory layouts, and offerprecise control over allocation. As such, viewers are encouraged tofamiliarize themselves with the [C Language Bindings](tutorial-c.md#reference)and the [FIDL wire-format](../reference/wire-format/README.md). Parts of thistutorial assume knowledge of these related concepts. 注意：LLCPP目前处于测试阶段。绑定旨在利用FIDL有线格式和C ++内存布局之间的兼容性，并提供对分配的精确控制。因此，鼓励观众熟悉[C语言绑定]（tutorial-c.mdreference）和[FIDL有线格式]（../ reference / wire-format / README.md）。本教程的某些部分假定您具有这些相关概念的知识。

 
# Getting Started  入门 

Two build setups exist in the source tree: the Zircon build and the Fuchsia build. The LLCPP code generator is not supported by the Zircon build. Therefore,the steps to use the bindings depend on where the consumer code is located: 源代码树中存在两种构建设置：Zircon构建和紫红色构建。 Zircon版本不支持LLCPP代码生成器。因此，使用绑定的步骤取决于使用者代码所在的位置：

 
*   **Code is outside `zircon/`:** Add `//[library path]:[library name]_llcpp` to the GN dependencies e.g.`"//sdk/fidl/fuchsia.math:fuchsia.math_llcpp"`, and the bindings codewill be automatically generated as part of the build. * **代码在`zircon /`之外：**将`// [库路径]：[库名称] _llcpp`添加到GN依赖项中，例如`“ //sdk/fidl/fuchsia.math:fuchsia.math_llcpp”` ，并且绑定代码将作为构建的一部分自动生成。
*   **Code is inside `zircon/`:** Add a GN dependency of the form: `"$zx/system/fidl/[library-name]:llcpp"`.Run a special [command](/tools/fidlgen_llcpp_zircon/README.md) whichextracts the set of FIDL libraries used through LLCPP in Zircon, and buildsand runs the code generator during the Fuchsia build phase. The generatedcode is placed in a `gen` folder next to the corresponding FIDL definition,and has to be checked into source control([example](/zircon/system/fidl/fuchsia-io/gen/llcpp)). Whenever the FIDLlibrary changes, re-run the command to update the checked in bindings. * **代码位于`zircon /`内部：**添加格式为`“ $ zx / system / fidl / [library-name]：llcpp”`的GN依赖项。运行特殊的[command]（/ tools / fidlgen_llcpp_zircon / README.md）提取在Zircon中通过LLCPP使用的FIDL库集，并在紫红色的构建阶段构建并运行代码生成器。生成的代码放在相应FIDL定义旁边的“ gen”文件夹中，并且必须检查到源代码管理中（[示例]（/ zircon / system / fidl / fuchsia-io / gen / llcpp））。每当FIDLlibrary更改时，请重新运行命令以更新签入的绑定。

 
## Preliminary Concepts  初步概念 

 
*   **Decoded Message:** A FIDL message in [decoded form](../reference/wire-format#Decoded-Messages)is a contiguous buffer that is directly accessible by reinterpreting thememory as the corresponding LLCPP FIDL type. That is, all pointers pointwithin the same buffer, and the pointed objects are in a specific orderdefined by the FIDL wire-format. When making a call, a response buffer isused to decode the response message. * **解码消息：** [解码形式]（../ reference / wire-formatDecoded-Messages）的FIDL消息是一个连续的缓冲区，可通过将主题重新解释为相应的LLCPP FIDL类型来直接访问。也就是说，所有指针都指向同一缓冲区内，并且指向的对象按照FIDL有线格式定义的特定顺序。进行呼叫时，使用响应缓冲区对响应消息进行解码。

 
*   **Encoded Message:** A FIDL message in [encoded form](../reference/wire-format#Encoded-Messages)is an opaque contiguous buffer plus an array of handles. The buffer isof the same length as the decoded counterpart, but pointers are replacedwith placeholders, and handles are moved to the accompanying array.When making a call, a request buffer is used to encode the request message. * **编码的消息：**以[编码形式]（../ reference / wire-formatEncoded-Messages）的FIDL消息是不透明的连续缓冲区以及一个句柄数组。缓冲区的长度与解码后的缓冲区的长度相同，但是指针被占位符替换，并且句柄被移至随附的数组。进行调用时，请求缓冲区用于对请求消息进行编码。

 
*   **Message Linearization:** FIDL messages have to be in a contiguous buffer packed according to thewire-format. When making a call however, the arguments to the bindings codeand out-of-line objects are usually scattered in memory, unless carefulattention is spent to follow the wire-format order. The process of walkingdown the tree of objects and packing them is termed *linearization*, andusually involves `O(message size)` copying. * **消息线性化：** FIDL消息必须根据有线格式包装在连续的缓冲区中。但是，在进行调用时，绑定代码和脱机对象的参数通常会散布在内存中，除非您花费足够的精力遵循有线格式的顺序。下移对象树并将其打包的过程称为“线性化”，通常涉及“ O（消息大小）”复制。

 
*   **Message Ownership:** Crucially, LLCPP generated structures are views over some underlying buffer;they do not own memory or handles located out-of-line. In practice, onemust ensure the object managing the buffer outlives the views. * **消息所有权：**至关重要的是，LLCPP生成的结构是在某些基础缓冲区上的视图；它们不拥有内存或位于离线位置的句柄。实际上，必须确保管理缓冲区的对象的寿命超过视图。

 
## Generated API Overview  生成的API概述 

Low-Level C++ bindings are full featured, and support control over allocation as well as zero-copy encoding/decoding. (Note that contrary to the C bindings theyare meant to replace, the LLCPP bindings cover non-simple messages.) 低级C ++绑定功能齐全，并支持对分配以及零拷贝编码/解码的控制。 （请注意，与它们打算替换的C绑定相反，LLPP绑定涵盖了非简单消息。）

Let's use this FIDL protocol as a motivating example:  让我们将此FIDL协议用作激励示例：

```fidl
// fleet.fidl
library fuchsia.fleet;

struct Planet {
    string name;
    float64 mass;
    handle<channel> radio;
};
```
 

The following code is generated (simplified for readability):  生成以下代码（为便于阅读而简化）：

```cpp
// fleet.h
struct Planet {
  fidl::StringView name;
  double mass;
  zx::channel radio;
};
```
 

Note that `string` maps to `fidl::StringView`, hence the `Planet` struct will not own the memory associated with the `name` string. Rather, all stringspoint within some buffer space that is managed by the bindings library, or thatthe caller could customize. The same goes for the `fidl::VectorView<Planet>`in the code below. 注意，字符串映射到fidl :: StringView，因此，Planet结构将不拥有与name字符串关联的内存。而是，所有字符串都指向由绑定库管理或调用者可以自定义的某些缓冲区空间内。以下代码中的fidl :: VectorView <Planet>也是一样。

Continuing with the FIDL protocol:  继续FIDL协议：

```fidl
// fleet.fidl continued...
protocol SpaceShip {
    SetHeading(int16 heading);
    ScanForPlanets() -> (vector<Planet> planets);
};
```
 

The following code is generated (simplified for readability):  生成以下代码（为便于阅读而简化）：

```cpp
// fleet.h continued...
class SpaceShip final {
 public:
  struct SetHeadingRequest final {
    fidl_message_header_t _hdr;
    int16_t heading;
  };

  struct ScanForPlanetsResponse final {
    fidl_message_header_t _hdr;
    fidl::VectorView<Planet> planets;
  };
  using ScanForPlanetsRequest = fidl::AnyZeroArgMessage;

  class SyncClient final { /* ... */ };
  class Call final { /* ... */ };
  class Interface { /* ... */ };

  static bool TryDispatch(Interface* impl, fidl_msg_t* msg, fidl::Transaction* txn);
  static bool Dispatch(Interface* impl, fidl_msg_t* msg, fidl::Transaction* txn);

  class ResultOf final { /* ... */ };
  class UnownedResultOf final { /* ... */ };
  class InPlace final { /* ... */ };
};
```
 

Notice that every request and response is modelled as a `struct`: `SetHeadingRequest`, `ScanForPlanetsResponse`, etc.In particular, `ScanForPlanets()` has a request that contains no arguments, andwe provide a special type for that, `fidl::AnyZeroArgMessage`. 请注意，每个请求和响应都被建模为struct：SetHeadingRequest，ScanForPlanetsResponse等，特别是ScanForPlanets（）的请求不包含任何参数，为此我们提供了特殊的类型fidl :: AnyZeroArgMessage`。

Following those, there are three related concepts in the generated code:  在这些之后，生成的代码中包含三个相关的概念：

 
+ [`SyncClient`](#sync-client): A class that owns a Zircon channel, providing methods to make requests to the FIDL server. + [`SyncClient`]（sync-client）：拥有Zircon通道的类，提供了向FIDL服务器发出请求的方法。
+ [`Call`](#static-functions): A class that contains static functions to make sync FIDL calls directly on an unowned channel, avoiding setting up a`SyncClient`. This is similar to the simple client wrappers from the Cbindings, which take a `zx_handle_t`. + [`Call`]（static-functions）：包含静态函数的类，可直接在未拥有的频道上进行FIDL同步调用，而无需设置“ SyncClient”。这与Cbindings中的简单客户端包装程序相似，后者采用`zx_handle_t`。
+ `Interface` and `[Try]Dispatch`: A server should implement the `Interface` pure virtual class, which allows `Dispatch` to call one of the definedhandlers with a received FIDL message. +`Interface`和`[Try] Dispatch`：服务器应实现`Interface`纯虚拟类，该类允许`Dispatch`用收到的FIDL消息调用已定义的处理程序之一。

[`[Unowned]ResultOf`](#resultof-and-unownedresultof) are "scoping" classes containing return type definitions of FIDL calls inside `SyncClient` and `Call`.This allows one to conveniently write `ResultOf::SetHeading` to denote theresult of calling `SetHeading`. [`[Unown] ResultOf`]（resultof-and-unownedresultof）是“作用域”类，其中包含在“ SyncClient”和“ Call”中对FIDL调用的返回类型定义。这使人们可以方便地编写“ ResultOf :: SetHeading”来表示结果就是调用SetHeading。

[`InPlace`](#in_place-calls) is another "scoping" class that houses functions to make a FIDL call with encoding and decoding performed in-place directly onthe user buffer. It is more efficient than those `SyncClient` or `Call`, butcomes with caveats. We will dive into these separately. [`InPlace`]（in_place-calls）是另一个“作用域”类，其中包含用于直接在用户缓冲区上进行编码和解码的FIDL调用的函数。它比那些“ SyncClient”或“ Call”更有效，但有一些警告。我们将分别介绍这些内容。

 
## Client API  客户端API 

 
### Sync Client `(Protocol::SyncClient)`  同步客户端`（Protocol :: SyncClient）` 

The following code is generated for `SpaceShape::SyncClient`. Each FIDL method always correspond to two overloads which differ in memory management strategies,termed *flavors* in LLCPP: *managed flavor* and *caller-allocating flavor*. 以下代码是为“ SpaceShape :: SyncClient”生成的。每个FIDL方法始终对应于两个重载，这两个重载在内存管理策略上有所不同，在LLCPP中称为“风味”：“托管风味”和“调用者分配风味”。

```cpp
class SyncClient final {
 public:
  SyncClient(zx::channel channel);

  // FIDL: SetHeading(int16 heading);
  ResultOf::SetHeading SetHeading(int16_t heading);
  UnownedResultOf::SetHeading SetHeading(fidl::BytePart request_buffer, int16_t heading);

  // FIDL: ScanForPlanets() -> (vector<Planet> planets);
  ResultOf::ScanForPlanets ScanForPlanets();
  UnownedResultOf::ScanForPlanets ScanForPlanets(fidl::BytePart response_buffer);
};
```
 

The one-way FIDL method `SetHeading(int16 heading)` maps to:  单向FIDL方法SetHeading（int16 heading）映射到：

 
+ `ResultOf::SetHeading SetHeading(int16_t heading)`: This is the *managed flavor*.Buffer allocation for requests and responses are entirely handled within thisfunction, as is the case in simple C bindings. The bindings calculate a safebuffer size specific to this call at compile time based on FIDL wire-format andmaximum length constraints. The buffers are allocated on the stack if they fitunder 512 bytes, or else on the heap. Here is an example of using it: +`ResultOf :: SetHeading SetHeading（int16_t heading）`：这是“托管形式”。请求和响应的缓冲区分配完全在此函数内处理，就像简单的C绑定一样。绑定根据FIDL线格式和最大长度约束在编译时计算特定于此调用的安全缓冲区大小。如果缓冲区小于512字节，则在堆栈上分配缓冲区，否则在堆上分配缓冲区。这是使用它的一个例子：

```cpp
// Create a client from a Zircon channel.
SpaceShip::SyncClient client(zx::channel(client_end));

// Calling |SetHeading| with heading = 42.
SpaceShip::ResultOf::SetHeading result = client.SetHeading(42);

// Check the transport status (encoding error, channel writing error, etc.)
if (result.status() != ZX_OK) {
  // Handle error...
}
```
 

In general, the managed flavor is easier to use, but may result in extra allocation. See [ResultOf](#resultof-and-unownedresultof) for details on buffermanagement. 通常，托管风味更易于使用，但可能会导致额外的分配。有关缓冲区管理的详细信息，请参见[ResultOf]（结果和未拥有的结果）。

 
+ `UnownedResultOf::SetHeading SetHeading(fidl::BytePart request_buffer, int16_t heading)`: This is the *caller-allocating flavor*, which defers all memory allocationresponsibilities to the caller.Here we see an additional parameter `request_buffer` which is always the firstargument in this flavor. The type `fidl::BytePart` references a buffer addressand size. It will be used by the bindings library to construct the FIDL request,hence it must be sufficiently large.The method parameters (e.g. `heading`) are *linearized* to appropriate locationswithin the buffer. If `SetHeading` had a return value, this flavor would ask fora `response_buffer` too, as the last argument. Here is an example of using it: +`UnownedResultOf :: SetHeading SetHeading（fidl :: BytePart request_buffer，int16_t heading）`：这是“分配给调用者的味道”，将所有内存分配职责推迟给调用者。在这里，我们看到了一个附加参数“ request_buffer”，它总是这种风味的第一个论点。类型“ fidl :: BytePart”引用缓冲区的地址和大小。绑定库将使用它来构造FIDL请求，因此它必须足够大。方法参数（例如“标题”）被“线性化”到缓冲区内的适当位置。如果`SetHeading`具有返回值，则此风格也会要求`response_buffer`作为最后一个参数。这是使用它的一个例子：

```cpp
// Call SetHeading with an explicit buffer, there are multiple ways...

// 1. On the stack
fidl::Buffer<SetHeadingRequest> request_buffer;
auto result = client.SetHeading(request_buffer.view(), 42);

// 2. On the heap
auto request_buffer = std::make_unique<fidl::Buffer<SetHeadingRequest>>();
auto result = client.SetHeading(request_buffer->view(), 42);

// 3. Some other means, e.g. thread-local storage
constexpr uint32_t request_size = fidl::MaxSizeInChannel<SetHeadingRequest>();
uint8_t* buffer = allocate_buffer_of_size(request_size);
fidl::BytePart request_buffer(/* data = */buffer, /* capacity = */request_size);
auto result = client.SetHeading(std::move(request_buffer), 42);

// Check the transport status (encoding error, channel writing error, etc.)
if (result.status() != ZX_OK) {
  // Handle error...
}

// Don't forget to free the buffer at the end if approach #3 was used...
```
 

> When the caller-allocating flavor is used, the `result` object borrows the > request and response buffers (hence its type is under `UnownedResultOf`).> Make sure the buffers outlive the `result` object.> See [UnownedResultOf](#resultof-and-unownedresultof). >当使用分配给调用方的样式时，`result`对象将借用>请求和响应缓冲区（因此其类型位于`UnownedResultOf`下）。>确保缓冲区的寿命超过`result`对象。>请参见[UnownedResultOf] （结果和无结果）。

Caution: Buffers passed to the bindings must be aligned to 8 bytes. The `fidl::Buffer` helper class does this automatically. Failure to align wouldresult in a run-time error. 注意：传递给绑定的缓冲区必须对齐8个字节。 fidl :: Buffer`辅助类会自动执行此操作。未能对齐将导致运行时错误。

 
* * * *  * * * *

The two-way FIDL method `ScanForPlanets() -> (vector<Planet> planets)` maps to: 双向FIDL方法`ScanForPlanets（）->（vector <Planet> planets）`映射到：

 
+ `ResultOf::ScanForPlanets ScanForPlanets()`: This is the *managed flavor*. Different from the C bindings, response argumentsare not returned via out-parameters. Instead, they are accessed through thereturn value. Here is an example to illustrate: +`ResultOf :: ScanForPlanets ScanForPlanets（）`：这是“托管风味”。与C绑定不同，响应参数不是通过out参数返回的。而是通过turnturn值访问它们。这是一个示例说明：

```cpp
// It is cleaner to omit the |UnownedResultOf::ScanForPlanets| result type.
auto result = client.ScanForPlanets();

// Check the transport status (encoding error, channel writing error, etc.)
if (result.status() != ZX_OK) {
  // handle error & early exit...
}

// Obtains a pointer to the response struct inside |result|.
// This requires that the transport status is |ZX_OK|.
SpaceShip::ScanForPlanetsResponse* response = result.Unwrap();

// Access the |planets| response vector in the FIDL call.
for (const auto& planet : response->planets) {
  // Do something with |planet|...
}
```
 

> When the managed flavor is used, the returned object (`result` in this > example) manages ownership of all buffer and handles, while `result.Unwrap()`> returns a view over it. Therefore, the `result` object must outlive any> references to the response. >使用托管风格时，返回的对象（在本示例中为`result`）管理所有缓冲区和句柄的所有权，而`result.Unwrap（）`>返回其上的视图。因此，`result`对象必须比对响应的任何引用都有效。

 
+ `UnownedResultOf::ScanForPlanets ScanForPlanets(fidl::BytePart response_buffer)`: The *caller-allocating flavor* receives the message into `response_buffer`.Here is an example using it: +`UnownedResultOf :: ScanForPlanets ScanForPlanets（fidl :: BytePart response_buffer）`：*分配给调用方的风味*将消息接收到`response_buffer`中，以下是使用该示例的示例：

```cpp
fidl::Buffer<ScanForPlanetsResponse> response_buffer;
auto result = client.ScanForPlanets(response_buffer.view());
if (result.status() != ZX_OK) { /* ... */ }
auto response = result.Unwrap();
// |response->planets| points to a location within |response_buffer|.
```
 

> The buffers passed to caller-allocating flavor do not have to be initialized. > A buffer may be re-used multiple times, as long as it is large enough for> the calls involved. >传递给分配给调用方的味道的缓冲区不必初始化。 >缓冲区可以重复使用多次，只要缓冲区足够大以用于所涉及的调用即可。

Note: Since each `Planet` has a handle `zx::channel radio`, and the `fidl::VectorView<Planet>` type does not own the individual `Planet` objects,there needs to be a reliable way to capture the lifetime of those handles.Here the return value `result` owns them, and takes care of closing them whenit goes out of scope.If any handle is `std::move`ed away, `result` would not accidentally close it. 注意：由于每个`Planet`都有一个`zx :: channel radio`句柄，并且`fidl :: VectorView <Planet>`类型不拥有单独的`Planet`对象，因此需要一种可靠的方式来捕获这些句柄的生命周期。在这里，返回值`result`拥有它们，并在超出范围时负责关闭它们。如果任何句柄被`std :: move`移开，则`result`不会意外关闭它。

 
### Static Functions `(Protocol::Call)`  静态函数`（Protocol :: Call）` 

The following code is generated for `SpaceShape::Call`:  下面的代码是为SpaceShape :: Call生成的：

```cpp
class Call final {
 public:
  static ResultOf::SetHeading
  SetHeading(zx::unowned_channel client_end, int16_t heading);
  static UnownedResultOf::SetHeading
  SetHeading(zx::unowned_channel client_end, fidl::BytePart request_buffer, int16_t heading);

  static ResultOf::ScanForPlanets
  ScanForPlanets(zx::unowned_channel client_end);
  static UnownedResultOf::ScanForPlanets
  ScanForPlanets(zx::unowned_channel client_end, fidl::BytePart response_buffer);
};
```
 

These methods are similar to those found in `SyncClient`. However, they do not own the channel. This is useful if one is migrating existing code from theC bindings to low-level C++. Another use case is when implementing C APIswhich take a raw `zx_handle_t`. For example: 这些方法类似于在“ SyncClient”中找到的方法。但是，他们不拥有该频道。如果将现有代码从C绑定迁移到低级C ++，这将很有用。另一个用例是在实现带有原始zx_handle_t的C API时。例如：

```cpp
// C interface which does not own the channel.
zx_status_t spaceship_set_heading(zx_handle_t spaceship, int16_t heading) {
  auto result = fuchsia::fleet::SpaceShip::Call::SetHeading(
      zx::unowned_channel(spaceship), heading);
  return result.status();
}
```
 

 
### ResultOf and UnownedResultOf  ResultOf和UnownedResultOf 

For a method named `Foo`, `ResultOf::Foo` is the return type of the *managed flavor*. `UnownedResultOf::Foo` is the return type of the *caller-allocatingflavor*. Both types define the same set of methods: 对于名为“ Foo”的方法，`ResultOf :: Foo`是“托管风味”的返回类型。 `UnownedResultOf :: Foo`是* caller-allocatingflavor *的返回类型。两种类型定义了相同的方法集：

 
*   `zx_status status() const` returns the transport status. it returns the first error encountered during (if applicable) linearizing, encoding, makinga call on the underlying channel, and decoding the result.If the status is `ZX_OK`, the call has succeeded, and vice versa. *`zx_status status（）const`返回传输状态。它返回线性化，编码，在基础通道上进行调用以及对结果进行解码（如果适用）时遇到的第一个错误。如果状态为“ ZX_OK”，则调用成功，反之亦然。
*   `const char* error() const` contains a brief error message when status is not `ZX_OK`. Otherwise, returns `nullptr`. *`const char * error（）const`当状态不是`ZX_OK`时包含一个简短的错误信息。否则，返回`nullptr`。
*   **(only for two-way calls)** `FooResponse* Unwrap()` returns a pointer to the FIDL response message. For `ResultOf::Foo`, the pointer points tomemory owned by the result object. For `UnownedResultOf::Foo`, the pointerpoints to a caller-provided buffer. `Unwrap()` should only be called whenthe status is `ZX_OK`. * **（仅用于双向呼叫）**`FooResponse * Unwrap（）`返回指向FIDL响应消息的指针。对于`ResultOf :: Foo`，指针指向结果对象拥有的内存。对于`UnownedResultOf :: Foo`，指针指向调用者提供的缓冲区。仅当状态为ZX_OK时才调用Unwrap（）。

 
#### Allocation Strategy And Move Semantics  分配策略和移动语义 

`ResultOf::Foo` stores the response buffer inline if the message is guaranteed to fit under 512 bytes. Since the result object is usually instantiated on thecaller's stack, this effectively means the response is stack-allocated when itis reasonably small. If the maximal response size exceeds 512 bytes,`ResultOf::Foo` instead contains a `std::unique_ptr` to a heap-allocated buffer. 如果保证消息适合512个字节以下，则`ResultOf :: Foo`内联存储响应缓冲区。由于结果对象通常是在调用者的堆栈上实例化的，因此，这实际上意味着在合理小范围内将响应分配给堆栈。如果最大响应大小超过512字节，则resultOf :: Foo包含一个std :: unique_ptr到分配给堆的缓冲区。

Therefore, a `std::move()` on `ResultOf::Foo` may be costly if the response buffer is inline: the content has to be copied, and pointers to out-of-lineobjects have to be updated to locations within the destination object.Consider the following snippet: 因此，如果响应缓冲区是内联的，则在`ResultOf :: Foo`上的`std :: move（）`可能会很昂贵：必须复制内容，并且必须将指向离线对象的指针更新到其中的位置目标对象。请考虑以下代码段：

```cpp
int CountPlanets(ResultOf::ScanForPlanets result) { /* ... */ }

auto result = client.ScanForPlanets();
SpaceShip::ScanForPlanetsResponse* response = result.Unwrap();
Planet* planet = &response->planets[0];
int count = CountPlanets(std::move(result));    // Costly
// In addition, |response| and |planet| are invalidated due to the move
```
 

It may be written more efficiently as:  它可能更有效地写为：

```cpp
int CountPlanets(fidl::VectorView<SpaceShip::Planet> planets) { /* ... */ }

auto result = client.ScanForPlanets();
int count = CountPlanets(result.Unwrap()->planets);
```
 

> If the result object need to be passed around multiple function calls, > consider pre-allocating a buffer in the outer-most function and use the> caller-allocating flavor. >如果需要在多个函数调用之间传递结果对象，则>考虑在最外部的函数中预分配缓冲区，并使用>分配调用方的样式。

 
### In-Place Calls  就地通话 

Both the *managed flavor* and the *caller-allocating flavor* will copy the arguments into the request buffer. When there is out-of-line data involved,*message linearization* is additionally required to collate them as per thewire-format. When the request is large, these copying overhead can add up.LLCPP supports making a call directly on a caller-provided buffer containinga request message in decoded form, without any parameter copying. The requestis encoded in-place, hence the name of the scoping class `InPlace`. *托管风味*和*调用者分配风味*都将参数复制到请求缓冲区中。当涉及到离线数据时，还需要*消息线性化*以按照有线格式整理它们。当请求很大时，这些复制开销会加起来。LLCPP支持直接在调用方提供的缓冲区中进行呼叫，该缓冲区包含解码形式的请求消息，而无需任何参数复制。该请求是就地编码的，因此是作用域类“ InPlace”的名称。

```cpp
class InPlace final {
 public:
  static ::fidl::internal::StatusAndError
  SetHeading(zx::unowned_channel client_end,
             fidl::DecodedMessage<SetHeadingRequest> params);

  static ::fidl::DecodeResult<ScanForPlanets>
  ScanForPlanets(zx::unowned_channel client_end,
                 fidl::DecodedMessage<ScanForPlanetsRequest> params,
                 fidl::BytePart response_buffer);
};
```
 

These functions always take a [`fidl::DecodedMessage<FooRequest>`](#fidl_decodedmessage_t) which wraps theuser-provided buffer. To use it properly, initialize the request buffer with aFIDL message in decoded form. *In particular, out-of-line objects have to bepacked according to the wire-format, and therefore any pointers in the messagehave to point within the same buffer.* 这些函数始终采用[fidl :: DecodedMessage <FooRequest>`]（fidl_decodedmessage_t）来包装用户提供的缓冲区。要正确使用它，请使用解码形式的FIDL消息初始化请求缓冲区。 *特别是，离线对象必须根据有线格式进行打包，因此消息中的任何指针都必须指向同一缓冲区内。

When there is a response defined, the generated functions additionally ask for a `response_buffer` as the last argument. The response buffer does not have to beinitialized. 当定义了一个响应时，生成的函数会额外要求一个“ response_buffer”作为最后一个参数。响应缓冲区不必初始化。

```cpp
// Allocate buffer for in-place call
fidl::Buffer<SetHeadingRequest> request_buffer;
fidl::BytePart request_bytes = request_buffer.view();
memset(request_bytes.data(), 0, request_bytes.capacity());

// Manually construct the message
auto msg = reinterpret_cast<SetHeadingRequest*>(request_bytes.data());
msg->heading = 42;
// Here since our message is a simple struct,
// the request size is equal to the capacity.
request_bytes.set_actual(request_bytes.capacity());

// Wrap with a fidl::DecodedMessage
fidl::DecodedMessage<SetHeadingRequest> request(std::move(request_bytes));

// Finally, make the call.
auto result = SpaceShape::InPlace::SetHeading(channel, std::move(request));
// Check result.status(), result.error()
```
 

Despite the verbosity, there is actually very little work involved. The buffer passed to the underlying `zx_channel_call` system call is in fact`request_bytes`. The performance benefits become apparent when say the requestmessage contains a large inline array. One could set up the buffers once, thenmake repeated calls while mutating the array by directly editing the bufferin between. 尽管冗长，但实际上只涉及很少的工作。传递给基础zx_channel_call系统调用的缓冲区实际上是request_bytes。当说requestmessage包含一个大的内联数组时，性能优势变得显而易见。一个人可以设置一次缓冲区，然后通过直接编辑它们之间的缓冲区在重复更改数组的同时进行重复调用。

Key Point: in-place calls only reduce overhead in the request part of the call. Responses are already processed in-place even in the managed andcaller-allocating flavors. 关键点：就地呼叫仅减少呼叫请求部分的开销。即使在托管和呼叫者分配风格中，响应也已就地处理。

 
## Server API  服务器API 

```cpp
class Interface {
 public:
  virtual void SetHeading(int16_t heading,
                          SetHeadingCompleter::Sync completer) = 0;

  class ScanForPlanetsCompleterBase {
   public:
    void Reply(fidl::VectorView<Planet> planets);
    void Reply(fidl::BytePart buffer, fidl::VectorView<Planet> planets);
    void Reply(fidl::DecodedMessage<ScanForPlanetsResponse> params);
  };

  using ScanForPlanetsCompleter = fidl::Completer<ScanForPlanetsCompleterBase>;

  virtual void ScanForPlanets(ScanForPlanetsCompleter::Sync completer) = 0;
};

bool TryDispatch(Interface* impl, fidl_msg_t* msg, fidl::Transaction* txn);
```
 

The generated `Interface` class has pure virtual functions corresponding to the method calls defined in the FIDL protocol. One may override these functions ina subclass, and dispatch FIDL messages to a server instance by calling`TryDispatch`.The bindings runtime would invoke these handler functions appropriately. 生成的“接口”类具有与FIDL协议中定义的方法调用相对应的纯虚函数。可以在子类中重写这些函数，然后通过调用TryDispatch将FIDL消息分发到服务器实例。绑定运行时将适当地调用这些处理函数。

```cpp
class MyServer final : fuchsia::fleet::SpaceShip::Interface {
 public:
  void SetHeading(int16_t heading,
                  SetHeadingCompleter::Sync completer) override {
    // Update the heading...
  }
  void ScanForPlanets(ScanForPlanetsCompleter::Sync completer) override {
    fidl::VectorView<Planet> discovered_planets = /* perform planet scan */;
    // Send the |discovered_planets| vector as the response.
    completer.Reply(discovered_planets);
  }
};
```
 

Each handler function has an additional last argument `completer`. It captures the various ways one may complete a FIDL transaction, by sending areply, closing the channel with epitaph, etc.For FIDL methods with a reply e.g. `ScanForPlanets`, the corresponding completerdefines up to three overloads of a `Reply()` function(managed, caller-allocating, in-place), similar to the client side API.The completer always defines a `Close(zx_status_t)` function, to close theconnection with a specified epitaph. 每个处理程序函数都有一个附加的最后一个参数`completer`。它捕获了可以通过发送areply，使用墓志铭关闭通道等方式完成FIDL事务的各种方式。与客户端API相似，ScanForPlanets对应的完成程序最多定义Reply（）函数的三个重载（托管，调用方分配，就地）。完成程序始终定义一个Close（zx_status_t）函数，以关闭具有指定墓志的连接。

 
### Responding Asynchronously  异步响应 

Notice that the type for the completer `ScanForPlanetsCompleter::Sync` has `::Sync`. This indicates the default mode of operation: the server mustsynchronously make a reply before returning from the handler function.Enforcing this allows optimizations: the bookkeeping metadata for makinga reply may be stack-allocated.To asynchronously make a reply, one may call the `ToAsync()` method on a `Sync`completer, converting it to `ScanForPlanetsCompleter::Async`. The `Async`completer supports the same `Reply()` functions, and may out-live the scope ofthe handler function by e.g. moving it into a lambda capture. 注意，完成器“ ScanForPlanetsCompleter :: Sync”的类型具有“ :: Sync”。这表示默认的操作模式：服务器必须在从处理程序函数返回之前同步做出答复，这可以优化：可以将用于做出答复的簿记元数据分配给堆栈。要异步做出答复，可以调用`ToAsync （）`同步器上的方法，将其转换为ScanForPlanetsCompleter :: Async`。异步完成器支持相同的Reply（）函数，并且可能超出处理程序函数的作用域，例如将其移动到lambda捕获中。

```cpp
void ScanForPlanets(ScanForPlanetsCompleter::Sync completer) override {
  // Suppose scanning for planets takes a long time,
  // and returns the result via a callback...
  EnqueuePlanetScan(some_parameters)
      .OnDone([completer = completer.ToAsync()] (auto planets) mutable {
        // Here the type of |completer| is |ScanForPlanetsCompleter::Async|.
        completer.Reply(planets);
      });
}
```
 

 
# Reference  参考 

 
## Design  设计 

 
### Goals  目标 

 
*   Support encoding and decoding FIDL messages with C++17.  *支持使用C ++ 17编码和解码FIDL消息。
*   Provide fine-grained control over memory allocation.  *提供对内存分配的细粒度控制。
*   More type-safety and more features than the C language bindings.  *比C语言绑定更具类型安全性和更多功能。
*   Match the size and efficiency of the C language bindings.  *匹配C语言绑定的大小和效率。
*   Depend only on a small subset of the standard library.  *仅取决于标准库的一小部分。
*   Minimize code bloat through table-driven encoding and decoding.  *通过表驱动的编码和解码使代码膨胀最小化。
*   Reuse encoders, decoders, and coding tables generated for C language bindings. *重用为C语言绑定生成的编码器，解码器和编码表。

 
## Code Generator  代码生成器 

 
### Mapping FIDL Types to Low-Level C++ Types  将FIDL类型映射到低级C ++类型 

This is the mapping from FIDL types to Low-Level C++ types which the code generator produces. 这是代码生成器生成的从FIDL类型到低级C ++类型的映射。

FIDL                                        | Low-Level C++ --------------------------------------------|------------------------------------------------------`bool`                                      | `bool`, *(requires sizeof(bool) == 1)*`int8`                                      | `int8_t``uint8`                                     | `uint8_t``int16`                                     | `int16_t``uint16`                                    | `uint16_t``int32`                                     | `int32_t``uint32`                                    | `uint32_t``int64`                                     | `int64_t``uint64`                                    | `uint64_t``float32`                                   | `float``float64`                                   | `double``handle`, `handle?`                         | `zx::handle``handle<T>`,`handle<T>?`                    | `zx::T` *(subclass of zx::object\<T\>)*`string`                                    | `fidl::StringView``string?`                                   | `fidl::StringView``vector<T>`                                 | `fidl::VectorView<T>``vector<T>?`                                | `fidl::VectorView<T>``array<T>:N`                                | `fidl::Array<T, N>`*protocol, protocol?*                       | `zx::channel`*request\<Protocol\>, request\<Protocol\>?* | `zx::channel`*struct* Struct                             | *struct* Struct*struct?* Struct                            | *struct* Struct**table* Table                               | (not yet supported)*union* Union                               | *struct* Union*union?* Union                              | *struct* Union**xunion* Xunion                             | *struct* Xunion*xunion?* Xunion                            | *struct* Xunion**enum* Foo                                  | *enum class Foo : data type* FIDL |底层C ++ -------------------------------------------- |- -------------------------------------------------- ---`bool` | `bool`，*（需要sizeof（bool）== 1）*`int8` | `int8_t``uint8` | `uint8_t``int16` | `int16_t``uint16` | `uint16_t``int32` | `int32_t``uint32` | `uint32_t``int64` | `int64_t``uint64` | `uint64_t``float32` | `float``float64` | `double``handle`，`handle？`| `zx :: handle``handle <T>`，`handle <T>？`| `zx :: T` *（zx :: object \ <T \>的子类）*`string` | `fidl :: StringView``string？`| fidl :: StringView``vector <T>`| fidl :: VectorView <T>``vector <T>？`| fidl :: VectorView <T>``array <T>：N` | fidl :: Array <T，N>`*协议，协议？* | `zx :: channel` * request \ <Protocol \>，request \ <Protocol \>？* | `zx :: channel` * struct *结构| * struct * Struct * struct？* Struct | *结构*结构**表*表| （尚不支持）*工会*联盟| * struct * Union * union？* Union | * struct * Union ** xunion * Xunion | * struct * Xunion * xunion？* Xunion | *结构* Xunion **枚举* Foo | *枚举类Foo：数据类型*

 
#### fidl::StringView  fidl :: StringView 

Defined in [lib/fidl/llcpp/string_view.h](/zircon/system/ulib/fidl/include/lib/fidl/llcpp/string_view.h)  定义于[lib / fidl / llcpp / string_view.h]（/ zircon / system / ulib / fidl / include / lib / fidl / llcpp / string_view.h）

Holds a reference to a variable-length string stored within the buffer. C++ wrapper of **fidl_string**. Does not own the memory of the contents. 保存对存储在缓冲区中的可变长度字符串的引用。 fidl_string **的C ++包装器。不拥有内容的内存。

`fidl::StringView` may be constructed by supplying the pointer and number of UTF-8 bytes (excluding trailing `\0`) separately. Alternatively, one could passa C++ string literal, or any value which implements `[const] char* data()`and `size()`. The string view would borrow the contents of the container. 可以通过分别提供指针和UTF-8字节数（不包括尾随\ 0）来构造fidl :: StringView。或者，可以传递C ++字符串文字或任何实现“ [const] char * data（）”和“ size（）”的值。字符串视图将借用容器的内容。

It is memory layout compatible with **fidl_string**.  它是与** fidl_string **兼容的内存布局。

 
#### fidl::VectorView\<T\>  fidl :: VectorView \ <T \> 

Defined in [lib/fidl/llcpp/vector_view.h](/zircon/system/ulib/fidl/include/lib/fidl/llcpp/vector_view.h)  定义于[lib / fidl / llcpp / vector_view.h]（/ zircon / system / ulib / fidl / include / lib / fidl / llcpp / vector_view.h）

Holds a reference to a variable-length vector of elements stored within the buffer. C++ wrapper of **fidl_vector**. Does not own the memory of elements. 保存对存储在缓冲区中的元素的可变长度向量的引用。 fidl_vector **的C ++包装器。不拥有元素的记忆。

`fidl::VectorView` may be constructed by supplying the pointer and number of elements separately. Alternatively, one could pass any value which supports[`std::data`](https://en.cppreference.com/w/cpp/iterator/data), such as astandard container, or an array. The vector view would borrow the contents ofthe container. fidl :: VectorView可以通过分别提供指针和元素数量来构造。或者，可以传递任何支持[`std :: data`]（https://en.cppreference.com/w/cpp/iterator/data）的值，例如标准容器或数组。矢量视图将借用容器的内容。

It is memory layout compatible with **fidl_vector**.  它是与** fidl_vector **兼容的内存布局。

 
#### fidl::Array\<T, N\>  fidl :: Array \ <T，N \> 

Defined in [lib/fidl/llcpp/array.h](/zircon/system/ulib/fidl/include/lib/fidl/llcpp/array.h)  定义在[lib / fidl / llcpp / array.h]（/ zircon / system / ulib / fidl / include / lib / fidl / llcpp / array.h）

Owns a fixed-length array of elements. Similar to `std::array<T, N>` but intended purely for in-place use. 拥有元素的固定长度数组。与`std :: array <T，N>`类似，但仅用于就地使用。

It is memory layout compatible with FIDL arrays, and is standard-layout. The destructor closes handles if applicable e.g. it is an array of handles. 它是与FIDL阵列兼容的内存布局，并且是标准布局。析构函数关闭句柄（如果适用），例如它是一个句柄数组。

 
## Bindings Library  绑定库 

 
### Dependencies  依存关系 

The low-level C++ bindings depend only on a small subset of header-only parts of the standard library. As such, they may be used in environments where linkingagainst the C++ standard library is discouraged or impossible. 低级C ++绑定仅取决于标准库中仅标头部分的一小部分。这样，它们可用于不鼓励或无法与C ++标准库进行链接的环境中。

 
### Helper Types  助手类型 

 
#### fidl::DecodedMessage\<T\>  fidl :: DecodedMessage \ <T \> 

Defined in [lib/fidl/llcpp/decoded_message.h](/zircon/system/ulib/fidl/include/lib/fidl/llcpp/decoded_message.h)  定义于[lib / fidl / llcpp / decoded_message.h]（/ zircon / system / ulib / fidl / include / lib / fidl / llcpp / decoded_message.h）

Manages a FIDL message in [decoded form](../reference/wire-format#Dual-Forms_Encoded-vs-Decoded). The message type is specified in the template parameter `T`.This class takes care of releasing all handles which were not consumed(std::moved from the decoded message) when it goes out of scope. 以[解码形式]（../reference/wire-formatDual-Forms_Encoded-vs-Decoded）管理FIDL消息。消息类型在模板参数“ T”中指定。此类在超出范围时会释放所有未使用的句柄（已解码消息中的std :: moved）。

`fidl::Encode(std::move(decoded_message))` encodes in-place.  fidl :: Encode（std :: move（decoded_message））`就地编码。

 
#### fidl::EncodedMessage\<T\>  fidl :: EncodedMessage \ <T \> 

Defined in [lib/fidl/llcpp/encoded_message.h](/zircon/system/ulib/fidl/include/lib/fidl/llcpp/encoded_message.h) Holds a FIDL message in [encoded form](../reference/wire-format#Dual-Forms_Encoded-vs-Decoded),that is, a byte array plus a handle table.The bytes part points to an external caller-managed buffer, while the handles partis owned by this class. Any handles will be closed upon destruction. 在[lib / fidl / llcpp / encoded_message.h]中定义（/zircon/system/ulib/fidl/include/lib/fidl/llcpp/encoded_message.h）以[编码形式]（../ reference / wire-formatDual-Forms_Encoded-vs-Decoded），即字节数组加上句柄表。字节部分指向外部调用方管理的缓冲区，而句柄部分则归此类所有。销毁后将关闭所有手柄。

`fidl::Decode(std::move(encoded_message))` decodes in-place.  fidl :: Decode（std :: move（encoded_message））`就地解码。

 
##### Example  例 

```cpp
zx_status_t SayHello(const zx::channel& channel, fidl::StringView text,
                     zx::handle token) {
  assert(text.size() <= MAX_TEXT_SIZE);

  // Manually allocate the buffer used for this FIDL message,
  // here we assume the message size will not exceed 512 bytes.
  uint8_t buffer[512] = {};
  fidl::DecodedMessage<example::Animal::SayRequest> decoded(
      fidl::BytePart(buffer, 512));

  // Fill in header and contents
  example::Animal::SetTransactionHeaderFor::SayRequest(&decoded);

  decoded.message()->text = text;
  // Handle types have to be moved
  decoded.message()->token = std::move(token);

  // Encode the message in-place
  fidl::EncodeResult<example::Animal::SayRequest> encode_result =
      fidl::Encode(std::move(decoded));
  if (encode_result.status != ZX_OK) {
    return encode_result.status;
  }

  fidl::EncodedMessage<example::Animal::SayRequest>& encoded =
      encode_result.message;
  return channel.write(0, encoded.bytes().data(), encoded.bytes().size(),
                       encoded.handles().data(), encoded.handles().size());
}
```
