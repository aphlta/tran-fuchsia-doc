 
# Dart language FIDL tutorial  Dart语言FIDL教程 

[TOC]  [目录]

 
## About this tutorial  关于本教程 

This tutorial describes how to make client calls and write servers in Dart using the FIDL InterProcess Communication (**IPC**) system in Fuchsia. 本教程介绍了如何使用紫红色的FIDL InterProcess Communication（** IPC **）系统在Dart中进行客户端调用和编写服务器。

Refer to the [main FIDL page](../README.md) for details on the design and implementation of FIDL, as well as the[instructions for getting and building Fuchsia](/docs/getting_started.md). 有关FIDL的设计和实现以及[获取和构建紫红色的说明]（/ docs / getting_started.md）的详细信息，请参见[FIDL主页]（../README.md）。

 
## Getting started  入门 

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

The examples are in Topaz at: [//topaz/examples/fidl/](https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/) 这些示例在Topaz中位于：[//topaz/examples/fidl/](https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/）

You can build the code via the following:  您可以通过以下方式构建代码：

```sh
fx set core.x64 --with //topaz/packages/examples:fidl
fx build
```
 

 
## `Echo` server  回声服务器 

The echo server implementation can be found at: [//topaz/examples/fidl/echo_server_async_dart/lib/main.dart](https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/echo_server_async_dart/). 可以在以下位置找到回显服务器的实现：[//topaz/examples/fidl/echo_server_async_dart/lib/main.dart](https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/echo_server_async_dart/） 。

This file implements the `main()` function and the `EchoImpl` class:  该文件实现`main（）`函数和`EchoImpl`类：

 
-   The `main()` function is executed when the component is loaded. `main()` registers the availability of the service with incoming connections fromFIDL. -加载组件时执行`main（）`函数。 main（）通过FIDL的传入连接注册服务的可用性。
-   `EchoImpl` processes requests on the `Echo` protocol. A new object is created for each channel. -`EchoImpl`处理基于`Echo`协议的请求。为每个通道创建一个新对象。

To understand how the code works, here's a summary of what happens in the server to execute an IPC call. We will dig into what each of these lines means, so it'snot necessary to understand all of this before you move on. 为了了解代码的工作原理，这里总结了服务器中执行IPC调用时发生的情况。我们将深入研究每行的含义，因此在继续之前不必了解所有这些内容。

 
1.  **Startup.** The FIDL Shell loads the Dart runner, which starts the VM, loads `main.dart`, and calls `main()`. 1. **启动。** FIDL Shell加载Dart运行程序，启动虚拟机，加载`main.dart`，然后调用`main（）`。
1.  **Registration** `main()` registers `EchoImpl` to bind itself to incoming requests on the `Echo` protocol. `main()` returns, but the program doesn'texit, because an [eventloop](https://dart.dev/tutorials/language/futures) to handleincoming requests is running. 1. ** Registration **`main（）`注册`EchoImpl`以将自身绑定到`Echo`协议的传入请求。 main（）返回，但程序未退出，因为正在运行用于处理传入请求的[eventloop]（https://dart.dev/tutorials/language/futures）。
1.  **Service request.** The `Echo` server package receives a request to bind `Echo` service to a new channel, so it calls the `bind()` function passed inthe previous step. 1.服务请求。Echo服务器软件包收到将Echo服务绑定到新通道的请求，因此它调用在上一步中传递的bind（）函数。
1.  **Service request.** `bind()` uses the `EchoImpl` instance.  1. **服务请求。**`bind（）`使用`EchoImpl`实例。
1.  **API request.** The `Echo` server package receives a call to `echoString()` from the channel and dispatches it to `echoString()` in the `EchoImpl`object instance bound in the last step. 1. API请求。Echo服务器软件包从通道接收对echoString（）的调用，并将其分派到最后一步绑定的EchoImpl对象实例中的echoString（）。
1.  **API request.** `echoString()` returns a future containing the response.  1. ** API请求。**`echoString（）`返回包含响应的future。

Now let's go through the details of how this works.  现在，让我们详细了解其工作原理。

 
### File headers  文件头 

Here are the import declarations in the Dart server implementation:  以下是Dart服务器实施中的导入声明：

```dart
import 'dart:async';
import 'package:fidl/fidl.dart';
import 'package:fidl_fidl_examples_echo/fidl_async.dart' as fidl_echo;
import 'package:fuchsia_services/services.dart';
```
 

 
-   `dart:async` Support for asynchronous programming with classes such as Future.  -`dart：async`支持使用诸如Future之类的异步编程。
-   `fidl.dart` exposes the FIDL runtime library for Dart. Our program needs it for `InterfaceRequest`. -`fidl.dart`公开了Dart的FIDL运行时库。我们的程序需要它用于`InterfaceRequest`。
-   `fidl_echo` contains bindings for the `Echo` protocol. This file is generated from the protocol defined in `echo.fidl`. -`fidl_echo`包含`Echo`协议的绑定。该文件是根据“ echo.fidl”中定义的协议生成的。
-   `services.dart` is required for ApplicationContext, which is where we register our service. -ApplicationContext需要`services.dart`，这是我们注册服务的位置。

 
### main()  主要（） 

Everything starts with main():  一切都以main（）开始：

```dart
void main(List<String> args) {
  _quiet = args.contains('-q');

  final context = StartupContext.fromStartupInfo();
  final echo = _EchoImpl();

  context.outgoing.addPublicService<fidl_echo.Echo>(
      echo.bind, fidl_echo.Echo.$serviceName);
}
```
 

`main()` is called by the Dart VM when your service is loaded, similar to `main()` in a C or C++ component. It binds an instance of `EchoImpl`, ourimplementation of the `Echo` protocol, to the name of the `Echo` service. 加载服务后，Dart VM会调用main（），类似于C或C ++组件中的main（）。它将“ EchoImpl”的实例（我们对“ Echo”协议的实现）绑定到“ Echo”服务的名称。

Eventually, another FIDL component will attempt to connect to our component.  最终，另一个FIDL组件将尝试连接到我们的组件。

 
### The `bind()` function  `bind（）`函数 

Here's what it looks like:  看起来是这样的：

```dart
void bind(InterfaceRequest<fidl_echo.Echo> request) {
  _binding.bind(this, request);
}
```
 

The `bind()` function is called when the first channel is received from another component. This function binds once for each service it makes available to theother component (remember that each service exposes a single protocol). Theinformation is cached in a data structure owned by the FIDL runtime, and used tocreate objects to be the endpoints for additional incoming channels. 当从另一个组件接收到第一个通道时，将调用“ bind（）”函数。此功能为它提供给其他组件的每个服务绑定一次（请记住，每个服务都公开一个协议）。该信息被缓存在FIDL运行时拥有的数据结构中，并用于创建对象作为其他传入通道的端点。

Unlike C++, Dart only has a [single thread](https://dart.dev/tutorials/language/futures)per isolate, so there's no possible confusion over which thread owns a channel. 与C ++不同，Dart每个分隔符仅具有一个[单线程]（https://dart.dev/tutorials/language/futures），因此对于哪个线程拥有一个通道不会造成任何混淆。

 
#### Is there really only one thread?  真的只有一个线程吗？ 

Both yes and no. There's only one thread in your component's VM, but the handle watcher isolate has its own, separate thread so that component isolatesdon't have to block. Component isolates can also spawn new isolates, whichwill run on different threads. 是和否。组件的VM中只有一个线程，但是handle watcher隔离具有其自己的独立线程，因此不必隔离组件隔离。组件隔离也可以生成新的隔离，这些隔离将在不同的线程上运行。

 
### The `echoString` function  `echoString`函数 

Finally we reach the implementation of the server API. Your `EchoImpl` object receives a call to the `echoString()` function. It accepts a string valueargument and it returns a Future of type String. 最后，我们实现服务器API的实现。您的`EchoImpl`对象收到了对`echoString（）`函数的调用。它接受字符串值参数，并返回String类型的Future。

 

```dart
@override
Future<String> echoString(String value) async {
  if (!_quiet) {
    print('EchoString: $value');
  }
  return value;
}
```
 

 
## `Echo` client  回声客户端 

The echo client implementation can be found at: [//topaz/examples/fidl/echo_client_async_dart/lib/main.dart](https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/echo_client_async_dart/lib/main.dart) 可以在以下位置找到回显客户端的实现：[//topaz/examples/fidl/echo_client_async_dart/lib/main.dart](https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/echo_client_async_dart/lib /main.dart）

Our simple client does everything in `main()`.  我们的简单客户端会执行`main（）`中的所有操作。

Note: a component can be a client, a service, or both, or many. The distinction in this example between Client and Server is purely fordemonstration purposes. 注意：组件可以是客户端，服务或两者兼有，也可以是多个。在此示例中，客户端和服务器之间的区别纯粹是出于演示目的。

Here is the summary of how the client makes a connection to the echo service.  这是客户端如何建立与回显服务的连接的摘要。

 
1.  **Startup.** The FIDL Shell loads the Dart runner, which starts the VM, loads `main.dart`, and calls `main()`. 1. **启动。** FIDL Shell加载Dart运行程序，启动虚拟机，加载`main.dart`，然后调用`main（）`。
1.  **Launch.** The destination server if it wasn't started already.  1. **启动。**目标服务器（如果尚未启动）。
1.  **Connect.** The destination server is specified, and we request for it to be started if it wasn't already. 1. **连接。**已指定目标服务器，如果尚未启动，我们要求将其启动。
1.  **Bind.** We bind `EchoProxy`, a generated proxy class, to the remote `Echo` service. 1. **绑定。**我们将生成的代理类`EchoProxy`绑定到远程`Echo`服务。
1.  **Invoke.** We invoke `echoString` with a value, and set a callback to handle the response. 1. **调用。**我们用一个值调用`echoString`，并设置一个回调来处理响应。
1.  **Wait.** `main()` returns, but the FIDL run loop is still waiting for messages from the remote channel. 1. **等待。**`main（）`返回，但是FIDL运行循环仍在等待来自远程通道的消息。
1.  **Handle result.** The result arrives, and our callback is executed, printing the response. 1. **处理结果。**结果到达，执行回调，打印响应。
1.  **Shutdown.** `dart_echo_server` exits.  1. **关闭。**`dart_echo_server`退出。
1.  **Shutdown.** `dart_echo_client` exits.  1. **关机。**`dart_echo_client`退出。

 
### main()  主要（） 

The `main()` function in the client contains all the client code.  客户端的main（）函数包含所有客户端代码。

```dart
Future<void> main(List<String> args) async {
  String serverUrl =
      'fuchsia-pkg://fuchsia.com/echo_server_async_dart#meta/echo_server_async_dart.cmx';
  if (args.length >= 2 && args[0] == '--server') {
    serverUrl = args[1];
  }

  final context = StartupContext.fromStartupInfo();

  /// A [DirectoryProxy] who's channels will facilitate the connection between
  /// this client component and the launched server component we're about to
  /// launch. This client component is looking for service under /in/svc/
  /// directory to connect to while the server exposes services others can
  /// connect to under /out/svc directory.
  final dirProxy = DirectoryProxy();

  // Connect. The destination server is specified, and we request for it to be
  // started if it wasn't already.
  final launchInfo = LaunchInfo(
    url: serverUrl,
    // The directoryRequest is the handle to the /out directory of the launched
    // component.
    directoryRequest: dirProxy.ctrl.request().passChannel(),
  );

  // Creates a new instance of the component described by launchInfo.
  final componentController = ComponentControllerProxy();

  await context.launcher
      .createComponent(launchInfo, componentController.ctrl.request());

  // Bind. We bind EchoProxy, a generated proxy class, to the remote Echo
  // service.
  final _echo = fidl_echo.EchoProxy();
  Incoming(dirProxy).connectToService(_echo);

  // Invoke echoString with a value and print it's response.
  final response = await _echo.echoString('hello');
  print('***** Response: $response');

  // close the echo server
  componentController.ctrl.close();

  // Shutdown, exit this Echo client
  exit(0);
}
```
 

 
### Run the sample  运行样本 

You can run the Echo example like this:  您可以像这样运行Echo示例：

```sh
$ fx shell run fuchsia-pkg://fuchsia.com/echo_client_async_dart#meta/echo_client_async_dart.cmx
```
 

 
## `Echo` across languages and runtimes  跨语言和运行时的`Echo`As a final exercise, you can now mix & match `Echo` clients and servers as you see fit. Let's try having the Dart client call the C++ server (from the[C++ version of the example](tutorial-cpp.md)). 作为最后的练习，您现在可以混合使用匹配的“ Echo”客户端和服务器。让我们尝试让Dart客户端调用C ++服务器（来自[示例的C ++版本]（tutorial-cpp.md））。

```sh
$ fx shell run fuchsia-pkg://fuchsia.com/echo_client_async_dart#meta/echo_client_async_dart.cmx--server fuchsia-pkg://fuchsia.com/echo_server_cpp#meta/echo_server_cpp.cmx
```
 

The Dart client will start the C++ server and connect to it. `EchoString()` works across language boundaries, all that matters is that the ABI defined byFIDL is observed on both ends. Dart客户端将启动C ++服务器并连接到它。 “ EchoString（）”跨语言边界工作，重要的是在两端观察到由FIDL定义的ABI。

