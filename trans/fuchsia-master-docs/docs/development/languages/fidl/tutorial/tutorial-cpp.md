 
# C++ language FIDL tutorial  C ++语言FIDL教程 

[TOC]  [目录]

 
## About this tutorial  关于本教程 

This tutorial describes how to make client calls and write servers in C++ using the FIDL InterProcess Communication (**IPC**) system in Fuchsia. 本教程描述了如何使用紫红色的FIDL InterProcess Communication（** IPC **）系统以C ++进行客户端调用和编写服务器。

Refer to the [main FIDL page](../README.md) for details on the design and implementation of FIDL, as well as the[instructions for getting and building Fuchsia](/docs/getting_started.md). 有关FIDL的设计和实现以及[获取和构建紫红色的说明]（/ docs / getting_started.md）的详细信息，请参见[FIDL主页]（../README.md）。

The [reference](#reference) section documents the high-level C++ interface bindings. [reference]（参考）部分记录了高级C ++接口绑定。

 
# Getting started  入门 

We'll use the `echo.test.fidl` sample that we discussed in the [FIDL Tutorial](README.md) introduction section, by opening[//garnet/examples/fidl/services/echo.test.fidl](/garnet/examples/fidl/services/echo.test.fidl). 我们将通过打开[//garnet/examples/fidl/services/echo.test.fidl]（在[FIDL教程]（README.md）简介部分中讨论过的`echo.test.fidl`示例）来使用（ /garnet/examples/fidl/services/echo.test.fidl）。

<!-- NOTE: the code snippets here need to be kept up to date manually by copy-pasting from the actual source code. Please update a snippetif you notice it's out of date. --> <！-注意：此处的代码段需要通过从实际源代码中粘贴粘贴来手动保持最新。如果发现片段已过时，请更新。 ->

 

```fidl
library fidl.examples.echo;

[Discoverable]
protocol Echo {
    EchoString(string? value) -> (string? response);
};
```
 

 
## Build  建立 

You can build the code via the following:  您可以通过以下方式构建代码：

```sh
fx set core.x64 --with //garnet/packages/examples:fidl
fx build
```
 

 
### Generated files  生成的文件 

Building runs the FIDL compiler automatically. It writes the glue code that allows the protocols to be used from different languages.Below are the implementation files created for C++. Building将自动运行FIDL编译器。它编写了粘合代码，允许使用不同语言的协议。以下是为C ++创建的实现文件。

```
./out/default/fidling/gen/garnet/examples/fidl/services/fidl/examples/echo/cpp/fidl.cc
./out/default/fidling/gen/garnet/examples/fidl/services/fidl/examples/echo/cpp/fidl.h
```
 

 
## `Echo` server  回声服务器 

The echo server implementation can be found at: [//garnet/examples/fidl/echo_server_cpp/](/garnet/examples/fidl/echo_server_cpp/). 可以在以下位置找到回显服务器的实现：[// garnet / examples / fidl / echo_server_cpp /]（/ garnet / examples / fidl / echo_server_cpp /）。

Find the implementation of the main function, and that of the `Echo` protocol.  查找主要功能的实现以及“ Echo”协议的实现。

To understand how the code works, here's a summary of what happens in the server to execute an IPC call. 为了了解代码的工作原理，这里总结了服务器中执行IPC调用时发生的情况。

 
1.  Fuchsia loads the server executable, and your `main()` function starts.  1.紫红色加载服务器可执行文件，然后您的`main（）`函数启动。
1.  `main` creates an `EchoServerApp` object which will bind to the service protocol when it is constructed. 1.`main`创建一个`EchoServerApp`对象，该对象在构建时将绑定到服务协议。
1.  `EchoServerApp()` registers itself with the `StartupContext` by calling `context->outgoing().AddPublicService<Echo>()`. It passes a lambda functionthat is called when a connection request arrives. 1. EchoServerApp（）通过调用context-> outgoing（）。AddPublicService <Echo>（）来向StartupContext注册。它传递一个lambda函数，该函数在连接请求到达时被调用。
1.  Now `main` starts the run loop, expressed as an `async::Loop`.  1.现在`main`开始运行循环，表示为`async :: Loop`。
1.  The run loop receives a request to connect from another component, so calls the lambda created in `EchoServerApp()`. 1.运行循环收到来自另一个组件的连接请求，因此调用在“ EchoServerApp（）”中创建的lambda。
1.  That lambda binds the `EchoServerApp` instance to the request channel.  1.该lambda将`EchoServerApp`实例绑定到请求通道。
1.  The run loop receives a call to `EchoString()` from the channel and dispatches it to the object bound in the last step. 1.运行循环从通道接收对“ EchoString（）”的调用，并将其分派到最后一步中绑定的对象。
1.  `EchoString()` issues an async call back to the client using `callback(value)`, then returns to the run loop. 1.`EchoString（）`使用`callback（value）`向客户端发出异步回调，然后返回运行循环。

Let's go through the details of how this works.  让我们详细了解其工作原理。

 
### File headers  文件头 

First the namespace definition. This matches the namespace defined in the FIDL file in its "library" declaration, but that's incidental: 首先是名称空间定义。这与FIDL文件的“库”声明中定义的名称空间匹配，但这是偶然的：

```cpp
namespace echo {
```
 

Here are the #include files used in the server implementation:  这是服务器实现中使用的包含文件：

```cpp
#include <fidl/examples/echo/cpp/fidl.h>
#include <lib/async-loop/cpp/loop.h>
#include <lib/async-loop/default.h>
#include <lib/zx/channel.h>

#include "src/lib/component/cpp/startup_context.h"
```
 

 
-   `fidl.h` contains the generated C++ definition of our `Echo` FIDL protocol.  -`fidl.h`包含我们的`Echo` FIDL协议的C ++定义。
-   `startup_context.h` is used by `EchoServerApp` to expose service implementations.  -EchoServerApp使用startup_context.h公开服务实现。

 
### main  主要 

Most `main()` functions for FIDL components look very similar. They create a run loop using `async::Loop` or some other construct, and bind serviceimplementations. The `Loop.Run()` function enters the message loop to processrequests that arrive over channels. FIDL组件的大多数`main（）`函数看起来非常相似。他们使用async :: Loop或其他构造方法创建运行循环，并绑定服务实现。 Loop.Run（）函数进入消息循环以处理通过通道到达的请求。

Eventually, another FIDL component will attempt to connect to our component.  最终，另一个FIDL组件将尝试连接到我们的组件。

 
### The `EchoServerApp()` constructor  `EchoServerApp（）`构造函数 

Note that a connection is defined as the _first_ channel with another component. Any additional channels are not "connections".Therefore, service registration is performed before the run loopbegins and before the first connection is made. 注意，将连接定义为与其他组件的_first_通道。任何其他通道都不是“连接”。因此，服务注册是在运行循环开始之前和进行第一个连接之前执行的。

Here's what the `EchoServerApp` constructor looks like:  这是`EchoServerApp`构造函数的样子：

```cpp
EchoServerApp()
    : context_(fuchsia::sys::ComponentContext::CreateFromStartupInfo()) {
  context_->outgoing().AddPublicService<Echo>(
      [this](fidl::InterfaceRequest<Echo> request) {
        bindings_.AddBinding(this, std::move(request));
      });
```
 

The function calls `AddPublicService` once for each service it makes available to the other component (remember that each service exposes a singleprotocol). The information is cached by `StartupContext` and used to decidewhich `Interface` factory to use for additional incoming channels. A newchannel is created every time someone calls `ConnectToService()` on the otherend. 该函数为每个可用于其他组件的服务调用一次“ AddPublicService”（请记住，每个服务都公开一个协议）。该信息由StartupContext缓存，并用于决定将哪个Interface接口工厂用于其他传入通道。每当有人在另一端调用`ConnectToService（）`时，都会创建一个新通道。

If you read the code carefully, you'll see that the parameter to `AddPublicService` is actually a lambda function that captures `this`. Thismeans that the lambda function won't be executed until a channel tries to bindto the protocol, at which point the object is bound to the channel and willreceive calls from other components. Note that these calls havethread-affinity, so calls will only be made from the same thread. 如果仔细阅读代码，您会发现AddPublicService的参数实际上是一个捕获this的lambda函数。这意味着在通道尝试绑定到协议之前，lambda函数将不会执行，此时该对象已绑定到该通道，并将接收来自其他组件的调用。请注意，这些调用具有线程亲和性，因此只能从同一线程进行调用。

The function passed to `AddPublicService` can be implemented in different ways. The one in `EchoServerApp` uses the same object for all channels. That's a goodchoice for this case because the implementation is stateless. Other, morecomplex implementations could create a different object for each channel orperhaps re-use the objects in some sort of caching scheme. 传递给AddPublicService的函数可以用不同的方式实现。 EchoServerApp中的一个对所有通道使用相同的对象。对于这种情况，这是一个很好的选择，因为实现是无状态的。其他更复杂的实现可能会为每个通道创建一个不同的对象，或者可能以某种缓存方案重新使用这些对象。

Connections are always point to point. There are no multicast connections.  连接始终是点对点的。没有多播连接。

 
### The `EchoString()` function  `EchoString（）`函数 

Finally we reach the end of our server discussion. When the message loop receives a message in the channel to call the `EchoString()` function in the`Echo` protocol, it will be directed to the implementation below: 最后，我们到达服务器讨论的结尾。当消息循环在通道中接收到一条消息以调用Echo协议中的EchoString（）函数时，它将定向至以下实现：

```cpp
void EchoString(fidl::StringPtr value, EchoStringCallback callback) override {
  printf("EchoString: %s\n", value->data());
  callback(std::move(value));
}
```
 

Here's what's interesting about this code:  以下是此代码的有趣之处：

 
-   The first parameter to `EchoString()` is a `fidl::StringPtr`. As the name suggests, a `fidl::StringPtr` can be null. Strings in FIDL are UTF-8. -EchoString（）的第一个参数是fidl :: StringPtr。顾名思义，`fidl :: StringPtr`可以为null。 FIDL中的字符串为UTF-8。
-   The `EchoString()` function returns void because FIDL calls are asynchronous. Any value we might otherwise return wouldn't have anywhere togo. -因为FIDL调用是异步的，所以`EchoString（）`函数返回void。我们否则返回的任何值都将无处可去。
-   The last parameter to `EchoString()` is the client's callback function. In this case, the callback takes a `fidl::StringPtr`. -EchoString（）的最后一个参数是客户端的回调函数。在这种情况下，回调函数会使用`fidl :: StringPtr`。
-   `EchoServerApp::EchoString()` returns its response to the client by calling the callback. The callback invocation is also asynchronous, so the calloften returns before the callback is run in the client. -`EchoServerApp :: EchoString（）`通过调用回调将其响应返回给客户端。回调调用也是异步的，因此calloften在客户端中运行回调之前会返回。
-   Because the callback is async, the callback also returns void.  -因为回调是异步的，所以回调也返回void。

Any call to a protocol in FIDL is asynchronous. This is a big shift if you are used to a procedural world where function calls return after the work iscomplete. Because it's async, there's no guarantee that the call will everactually happen, so your callback may never be called. The remote FIDLcomponent might close, crash, be busy, etc. FIDL中对协议的任何调用都是异步的。如果您习惯于在工作完成后返回函数调用的过程世界，这将是一个很大的转变。因为它是异步的，所以不能保证调用会确实发生，因此您的回调可能永远不会被调用。远程FIDL组件可能关闭，崩溃，忙碌等。

 
## `Echo` client  回声客户端 

Let's take a look at the client implementation:  让我们看一下客户端的实现：

[//garnet/examples/fidl/echo_client_cpp/](/garnet/examples/fidl/echo_client_cpp/)  [// garnet / examples / fidl / echo_client_cpp /]（/ garnet / examples / fidl / echo_client_cpp /）

The structure of the client is similar to that of the server, with a `main` function and an `async::Loop`. The difference is that the client immediatelykicks off work once everything is initialized. In contrast, the server does nowork until a connection is accepted. 客户端的结构类似于服务器的结构，具有“ main”功能和“ async :: Loop”。不同之处在于，一旦一切都初始化，客户端将立即开始工作。相反，在接受连接之前，服务器不起作用。

Note: a component can be a client, a server, or both, or many. The distinction in this example between Client and Server is purely fordemonstration purposes. 注意：一个组件可以是客户端，服务器或两者兼有，也可以是多个。在此示例中，客户端和服务器之间的区别纯粹是出于演示目的。

Here is the summary of how the client makes a connection to the echo service.  这是客户端如何建立与回显服务的连接的摘要。

 
1.  The shell loads the client executable and calls `main`.  1. Shell加载客户端可执行文件并调用`main`。
1.  `main()` creates an `EchoClientApp` object to handle connecting to the server, calls `Start()` to initiate the connection, and then starts themessage loop. 1.“ main（）”创建一个“ EchoClientApp”对象来处理与服务器的连接，调用“ Start（）”以启动连接，然后启动主题循环。
1.  In `Start()`, the client calls `context_->launcher()->CreateComponent` with the url to the server component. If the server component is notalready running, it will be created at this point. 1.在“ Start（）”中，客户端使用服务器组件的URL调用“ context _-> launcher（）-> CreateComponent”。如果服务器组件尚未运行，则将在此时创建它。
1.  Next, the client calls `ConnectToService()` to open a channel to the server component. 1.接下来，客户端调用`ConnectToService（）`打开服务器组件的通道。
1.  `main` calls into `echo_->EchoString(...)` and passes the callback. Because FIDL IPC calls are async, `EchoString()` will probably return before theserver processes the call. 1.`main`调用`echo _-> EchoString（...）`并传递回调。由于FIDL IPC调用是异步的，因此EchoString（）可能会在服务器处理该调用之前返回。
1.  `main` then blocks on a response on the protocol.  1.`main`然后阻止对协议的响应。
1.  Eventually, the response arrives, and the callback is called with the result. 1.最终，响应到达，并使用结果调用回调。

 
### main  主要 

main() in the client is very different from the server, as it's synchronous on the server response. 客户端中的main（）与服务器非常不同，因为它在服务器响应上是同步的。

```cpp
int main(int argc, const char** argv) {
  std::string server_url = "fuchsia-pkg://fuchsia.com/echo_server_cpp#meta/echo_server_cpp.cmx";
  std::string msg = "hello world";
  for (int i = 1; i < argc - 1; ++i) {
    if (!strcmp("--server", argv[i])) {
      server_url = argv[++i];
    } else if (!strcmp("-m", argv[i])) {
      msg = argv[++i];
    }
  }
  async::Loop loop(&kAsyncLoopConfigAttachToCurrentThread);
  echo::EchoClientApp app;
  app.Start(server_url);
  app.echo()->EchoString(msg, [&loop](fidl::StringPtr value) {
    printf("***** Response: %s\n", value->data());
    loop.Quit();
  });
  return loop.Run();
}
```
 

 
### Start  开始 

`Start()` is responsible for connecting to the remote `Echo` service.  Start（）负责连接到远程的Echo服务。

```cpp
void Start(std::string server_url) {
  fuchsia::sys::LaunchInfo launch_info;
  launch_info.url = server_url;
  launch_info.directory_request = echo_provider_.NewRequest();
  context_->launcher()->CreateComponent(std::move(launch_info),
                                          controller_.NewRequest());
  echo_provider_.ConnectToService(echo_.NewRequest().TakeChannel(),
                                  Echo::Name_);
}
```
 

First, `Start()` calls `CreateComponent()` to launch `echo_server`. Then, it calls `ConnectToService()` to bind to the server's `Echo` protocol. The exactmechanism is somewhat hidden, but the particular protocol is automaticallyinferred from the type of `EchoPtr`, which is a typedef for`fidl::InterfacePtr<Echo>`. 首先，Start（）调用CreateComponent（）启动echo_server。然后，它调用ConnectToService（）绑定到服务器的Echo协议。确切的机制在某种程度上是隐藏的，但是从“ EchoPtr”的类型自动推断出特定的协议，“ EchoPtr”是“ fidl :: InterfacePtr <Echo>”的类型定义。

The second parameter to `ConnectToService()` is the service name.  ConnectToService（）的第二个参数是服务名称。

Next the client calls `EchoString()` in the returned protocol. FIDL protocols are asynchronous, so the call itself does not wait for `EchoString()` tocomplete remotely before returning. `EchoString()` returns void because of theasync behavior. 接下来，客户端在返回的协议中调用`EchoString（）`。 FIDL协议是异步的，因此调用本身不会在返回之前等待EchoString（）远程完成。由于异步行为，`EchoString（）`返回void。

Since the client has nothing to do until the server response arrives, and is done working immediately after, `main()` then blocks using `loop.Run()`,then exits. When the response will arrive, then the callback given to`EchoString()`, will execute first, then `Run()` will return,allowing `main()` to return and the program to terminate. 由于客户端在服务器响应到达之前无事可做，并且在此之后立即完成工作，因此main（）然后使用loop.Run（）进行阻塞，然后退出。当响应到达时，将首先执行给予EchoString（）的回调，然后返回Run（），从而允许main（）返回并终止程序。

 
### Run the sample  运行样本 

You can run the Hello World example like this:  您可以像这样运行Hello World示例：

```sh
$ run fuchsia-pkg://fuchsia.com/echo_client_cpp#meta/echo_client_cpp.cmx
```
 

You do not need to specifically run the server because the call to `CreateComponent()` in the client will automatically launch the server. 您不需要专门运行服务器，因为在客户端中对`CreateComponent（）`的调用将自动启动服务器。

 
# Reference  参考 

This section builds on the [C Language Bindings](tutorial-c.md#reference) and reuses many of its elements where appropriate. 本节以[C语言绑定]（tutorial-c.mdreference）为基础，并在适当的地方重用了其许多元素。

See [Comparing C, Low-Level C++, and High-Level C++ Language Bindings](c-family-comparison.md) for a comparative analysis of the goals anduse cases for all the C-family language bindings. 有关对所有C系列语言绑定的目标和用例的比较分析，请参见[比较C，低级C ++和高级C ++语言绑定]（c-family-comparison.md）。

 
## Design  设计 

 
### Goals  目标 

 
*   Support encoding and decoding FIDL messages with C++14.  *支持使用C ++ 14编码和解码FIDL消息。
*   Small, fast, efficient.  *小型，快速，高效。
*   Depend only on a small subset of the standard library.  *仅取决于标准库的一小部分。
*   Minimize code expansion through table-driven encoding and decoding.  *通过表驱动的编码和解码最大程度地减少代码扩展。
*   All code produced can be stripped out if unused.  *如果未使用，可以清除所有产生的代码。
*   Reuse encoders, decoders, and coding tables generated for C language bindings.  *重用为C语言绑定生成的编码器，解码器和编码表。

 
## Code Generator  代码生成器 

 
### Mapping Declarations  映射声明 

 
#### Mapping FIDL Types to C++ Types  将FIDL类型映射到C ++类型 

This is the mapping from FIDL types to C types which the code generator produces. 这是代码生成器生成的从FIDL类型到C类型的映射。

FIDL                                        | High-Level C++ --------------------------------------------|----------------------------------`bool`                                      | `bool``int8`                                      | `int8_t``uint8`                                     | `uint8_t``int16`                                     | `int16_t``uint16`                                    | `uint16_t``int32`                                     | `int32_t``uint32`                                    | `uint32_t``int64`                                     | `int64_t``uint64`                                    | `uint64_t``float32`                                   | `float``float64`                                   | `double``handle`, `handle?`                         | `zx::handle``handle<T>`,`handle<T>?`                    | `zx::T` *(subclass of zx::object<T>)*`string`                                    | `std::string``string?`                                   | `fidl::StringPtr``vector<T>`                                 | `std::vector<T>``vector<T>?`                                | `fidl::VectorPtr<T>``array<T>:N`                                | `std::array<T, N>`*protocol, protocol?* Protocol              | *class* ProtocolPtr*request\<Protocol\>, request\<Protocol\>?* | `fidl::InterfaceRequest<Protocol>`*struct* Struct                             | *class* Struct*struct?* Struct                            | `std::unique_ptr<Struct>`*table* Table                               | *class* Table*union* Union                               | *class* Union*union?* Union                              | `std::unique_ptr<Union>`*xunion* Xunion                             | *class* Xunion*xunion?* Xunion                            | `std::unique_ptr<Xunion>`*enum* Foo                                  | *enum class Foo : data type* FIDL |高级C ++ -------------------------------------------- |- ---------------------------------`bool` | `bool``int8` | `int8_t``uint8` | `uint8_t``int16` | `int16_t``uint16` | `uint16_t``int32` | `int32_t``uint32` | `uint32_t``int64` | `int64_t``uint64` | `uint64_t``float32` | `float``float64` | `double``handle`，`handle？`| `zx :: handle``handle <T>`，`handle <T>？`| `zx :: T` *（zx :: object <T>的子类）*`string` | `std :: string``string？`| fidl :: StringPtr``vector <T>`| `std :: vector <T>``vector <T>？`| fidl :: VectorPtr <T>``array <T>：N` | `std :: array <T，N>`*协议，协议？*协议| * class * ProtocolPtr * request \ <Protocol \>，request \ <Protocol \>？* | `fidl :: InterfaceRequest <Protocol>`* struct *结构| * class * Struct * struct？* Struct | `std :: unique_ptr <Struct>`* table *表| *类*表*工会*联合| * class * Union * union？* Union | `std :: unique_ptr <Union>`* xunion * Xunion | *类* Xunion * xunion？* Xunion | `std :: unique_ptr <Xunion>`* enum * Foo | *枚举类Foo：数据类型*

 
#### Mapping FIDL Identifiers to C++ Identifiers  将FIDL标识符映射到C ++标识符 

TODO: discuss reserved words, name mangling  TODO：讨论保留字，名称修饰

 
#### Mapping FIDL Type Declarations to C++ Types  将FIDL类型声明映射到C ++类型 

TODO: discuss generated namespaces, constants, enums, typedefs, encoding tables  待办事项：讨论生成的名称空间，常量，枚举，类型定义，编码表

 
## Bindings Library  绑定库 

 
### Dependencies  依存关系 

Depends only on Zircon system headers, libzx, and a portion of the C and C++ standard libraries. 仅取决于Zircon系统标头，libzx以及C和C ++标准库的一部分。

Does not depend on libftl or libmtl.  不依赖于libftl或libmtl。

 
### Code Style  代码风格 

To be discussed.  要讨论的。

The bindings library could use Google C++ style to match FIDL v1.0 but though this may ultimately be more confusing, especially given style choices inZircon so we may prefer to follow the C++ standard library style here as well. 绑定库可以使用Google C ++样式来匹配FIDL v1.0，但这虽然最终可能会更加令人困惑，尤其是在Zircon中选择了样式之后，所以我们在这里也可能更喜欢C ++标准库样式。

 
### High-Level Types  高级类型 

TODO: adopt main ideas from FIDL 1.0  TODO：采用FIDL 1.0中的主要思想

InterfacePtr<T> / interface_ptr<T>?  InterfacePtr <T> / interface_ptr <T>？

InterfaceRequest<T> / interface_req<T>?  InterfaceRequest <T> / interface_req <T>？

async waiter  异步服务员

etc...  等等...

 
## Suggested API Improvements over FIDL v1  在FIDL v1上建议的API改进 

The FIDL v1 API for calling and implementing FIDL protocols has generally been fairly effective so we would like to retain most of its structure in theidiomatic FIDL v2 bindings. However, there are a few areas that could beimproved. 通常，用于调用和实现FIDL协议的FIDL v1 API相当有效，因此我们希望将其大部分结构保留在流行的FIDL v2绑定中。但是，有一些地方可以改进。

TODO: actually specify the intended API  TODO：实际指定所需的API

 
### Handling Connection Errors  处理连接错误 

Handling connection errors systematically has been a cause of concern for clients of FIDL v1 because method result callbacks and connection errorcallbacks are implemented by different parts of the client program. 系统地处理连接错误已成为FIDL v1客户端关注的原因，因为方法结果回调和连接错误回调是由客户端程序的不同部分实现的。

It would be desirable to consider an API which allows for localized handling of connection errors at the point of method calls (in addition to protocol levelconnection error handling as before). 期望考虑一种API，该API允许在方法调用时对连接错误进行本地化处理（除了之前的协议级连接错误处理）。

See https://fuchsia-review.googlesource.com/#/c/23457/ for one example of how a client would otherwise work around the API deficiency. 有关客户端如何解决API缺陷的一个示例，请参阅https://fuchsia-review.googlesource.com//c/23457/。

One approach towards a better API may be constructed by taking advantage of the fact that std::function<> based callbacks are always destroyed even if they arenot invoked (such as when a connection error occurs). It is possible toimplement a callback wrapper which distinguishes these cases and allows clientsto handle them more systematically. Unfortunately such an approach may not beable to readily distinguish between a connection error vs. proxy destruction. 一种利用更好的API的方法可以通过利用以下事实来构造，即即使没有调用基于std :: function <>的回调，这些回调也总是被销毁（例如，发生连接错误时）。可以实现一个回调包装器，以区分这些情况并允许客户端更系统地处理它们。不幸的是，这种方法可能无法轻易地区分连接错误与代理破坏。

Alternately we could wire in support for multiple forms of callbacks or for multiple callbacks. 或者，我们可以连线支持多种形式的回调或多种回调。

Or we could change the API entirely in favor of a more explicit Promise-style mechanism. 或者，我们可以完全更改API以支持更明确的Promise样式机制。

There are lots of options here...  这里有很多选择...

