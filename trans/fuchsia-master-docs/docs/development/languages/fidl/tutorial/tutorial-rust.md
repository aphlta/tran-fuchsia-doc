 
# Rust language FIDL tutorial  Rust语言FIDL教程 

[TOC]  [目录]

 
## About this tutorial  关于本教程 

This tutorial describes how to make client calls and write servers in Rust using the FIDL InterProcess Communication (**IPC**) system in Fuchsia. 本教程描述了如何使用紫红色的FIDL InterProcess Communication（** IPC **）系统在Rust中进行客户端调用和编写服务器。

Refer to the [main FIDL page](../README.md) for details on the design and implementation of FIDL, as well as the[instructions for getting and building Fuchsia](/docs/getting_started.md). 有关FIDL的设计和实现以及[获取和构建紫红色的说明]（/ docs / getting_started.md）的详细信息，请参见[FIDL主页]（../README.md）。

 
## Getting started  入门 

We'll use the `echo.test.fidl` sample that we discussed in the [FIDL Tutorial](README.md) introduction section, by opening[//garnet/examples/fidl/services/echo.test.fidl](/garnet/examples/fidl/services/echo.test.fidl). 我们将通过打开[//garnet/examples/fidl/services/echo.test.fidl]（在[FIDL教程]（README.md）简介部分中讨论过的`echo.test.fidl`示例）来使用（ /garnet/examples/fidl/services/echo.test.fidl）。

<!-- NOTE: the code snippets here need to be kept up to date manually by copy-pasting from the actual source code. Please update a snippetif you notice it's out of date. --> <！-注意：此处的代码段需要通过从实际源代码中粘贴粘贴来手动保持最新。如果发现片段已过时，请更新。 ->

 

```fidl
{% includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="garnet/examples/fidl/services/echo.test.fidl" adjust_indentation="auto" %}
```
 

 
## Build  建立 

 
* To build the echo server, add `--with //garnet/examples/fidl/echo_server_rust` to your `fx set` invocation.  *要构建回显服务器，请在`fx set`调用中添加`--with // garnet / examples / fidl / echo_server_rust`。
* To build the echo client, add `--with //garnet/examples/fidl/echo_client_rust` to your `fx set` invocation.  *要构建回显客户端，请在`fx set`调用中添加`--with // garnet / examples / fidl / echo_client_rust`。

 
## `Echo` server  回声服务器 

The echo server implementation can be found at: [//garnet/examples/fidl/echo_server_rust/src/main.rs](/garnet/examples/fidl/echo_server_rust/src/main.rs). 可以在以下位置找到回显服务器的实现：[//garnet/examples/fidl/echo_server_rust/src/main.rs](/garnet/examples/fidl/echo_server_rust/src/main.rs）。

This file has two functions: `main()`, and `spawn_echo_server`:  该文件具有两个函数：main（）和spawn_echo_server：

 
-   The `main()` function creates an asynchronous task executor and a `ServicesServer` and runs the `ServicesServer` to completion onthe executor. -main（）函数创建一个异步任务执行器和一个ServicesServer，并在执行器上运行ServicesServer使其完成。
-   `spawn_echo_server` spawns a new asynchronous task which will handle incoming echo service requests. -`spawn_echo_server`产生一个新的异步任务，它将处理传入的回显服务请求。

To understand how the code works, here's a summary of what happens in the server to execute an IPC call. We will dig into what each of these lines means, so it'snot necessary to understand all of this before you move on. 为了了解代码的工作原理，这里总结了服务器中执行IPC调用时发生的情况。我们将深入研究每行的含义，因此在继续之前不必了解所有这些内容。

 
1.  **Services Server:** The `ServicesServer` is the main top-level future being run on the executor. It binds itself to the startup handle of thecurrent process and listens for incoming service requests. 1. **服务服务器：**服务服务器是在执行程序上运行的主要顶级将来。它将自身绑定到当前进程的启动句柄，并侦听传入的服务请求。
1.  **Service Request:** When another component needs to access an "Echo" server, it sends a request to the `ServicesServer` containing the name ofthe service to connect to ("Echo") and a channel to connect. 1. **服务请求：**当另一个组件需要访问“ Echo”服务器时，它将向“ ServicesServer”发送一个请求，其中包含要连接的服务的名称（“ Echo”）和要连接的通道。
1.  **Service Lookup:** The incoming service request wakes up the `async::Executor` executor and tells it that the `ServicesServer` taskcan now make progress and should be run. The `ServicesServer` wakes up,sees the request available on the startup handle of the process, and looksup the name of the requested service in the list of`(service_name, service_startup_func)` provided through calls to`add_service`. If a matching `service_name` exists, it calls`service_startup_func` with the channel to connect to the new service. 1. **服务查找：**传入的服务请求将唤醒async :: Executor执行程序，并告诉其ServicesServer任务现在可以取得进展，应该运行。 “ ServicesServer”被唤醒，在进程的启动句柄上看到可用的请求，并在通过调用“ add_service”提供的“（service_name，service_startup_func）”列表中查找所请求服务的名称。如果存在匹配的“ service_name”，它将通过通道调用“ service_startup_func”以连接到新服务。
1.  **Server Creation:**  At this point in our example, `|chan| spawn_echo_server(chan)` is called with the channel that wants tobe connected to an `Echo` service. `spawn_echo_server` creates a newfuture which loops over each value in the incoming stream of requests.It spawns that future to be run on the thread-local `async::Executor`. 1. **服务器创建：**在此示例中，`| chan | spawn_echo_server（chan）是通过要连接到`Echo`服务的通道调用的。 spawn_echo_server创建一个新的功能，该功能将循环请求的输入流中的每个值，并生成将来在线程本地的async :: Executor上运行的功能。
1.  **API Request:** An `echo_string` request is sent on the channel. This makes the channel the `Echo` service is running on readable, whichwakes up the asynchronous task spawned in `spawn_echo_server`. The taskreads the request off of the channel and yields a value from the`try_next()` future. 1. ** API请求：**在通道上发送一个`echo_string`请求。这使得通道“ Echo”服务以可读的方式运行，从而唤醒了“ spawn_echo_server”中产生的异步任务。任务从通道中读取请求，并从try_next（）未来产生一个值。
1.  **API Response:** Upon receiving a request, the task sends a response back to the client with `responder.send`. 1. ** API响应：**收到请求后，任务将使用`responder.send`将响应发送回客户端。

Now let's go through the code and see how this works.  现在，让我们看一下代码，看看它是如何工作的。

 
### File headers  文件头 

Here are the import declarations in the Rust server implementation:  这是Rust服务器实现中的导入声明：

```rust
{% includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="garnet/examples/fidl/echo_server_rust/src/main.rs" region_tag="import_declarations" adjust_indentation="auto" %}
```
 

 
-   `failure` provides conveniences for error handling, including a standard dynamically-dispatched `Error` type as well as a extension trait that addsthe `context` method to `Result` for providing extra information aboutwhere the error occurred. -failure为错误处理提供了便利，包括标准的动态分配的Error类型以及扩展特性，该扩展特性将context方法添加到Results中以提供有关错误发生位置的额外信息。
-   `fidl_fidl_examples_echo` contains bindings for the `Echo` protocol. This file is generated from the protocol defined in `echo.test.fidl`.These bindings include: -`fidl_fidl_examples_echo`包含`Echo`协议的绑定。该文件是根据`echo.test.fidl`中定义的协议生成的，这些绑定包括：
    -   The `EchoRequest` type, an enum over all of the different request types that can be received. -`EchoRequest`类型，它是可以接收的所有不同请求类型的枚举。
    -   The `EchoRequestStream` type, a [`Stream`] of incoming requests for the server to handle. -EchoRequestStream类型，服务器要处理的传入请求的[Stream]。
-   `ServiceFs` links service requests to service launcher functions.  -`ServiceFs`将服务请求链接到服务启动器功能。
-   `fuchsia_async`, often aliased to the abbreviated `fasync`, is the runtime library for running asynchronous tasks on Fuchsia. It also providesasynchronous bindings to a number of Fuchsia primitives, such as channels,sockets, and TCP/UDP. -`fuchsia_async`，通常是缩写为`fasync`的别名，是用于在Fuchsia上运行异步任务的运行时库。它还提供对许多紫红色原语的异步绑定，例如通道，套接字和TCP / UDP。
-   `futures` is a crate for working with asynchronous tasks. These tasks are composed of asynchronous units of work that may produce a single value(a `Future`) or many values (a `Stream`). Futures can be `await!`ed insidean `async` function or block, which will cause the current task to besuspended until the future is able to make more progress.For more about futures, see [the crate's documentation][docs].To understand more about how futuresare structured internally, see [this post][Tokio internals] on how futuresconnect to system waiting primitives like `epoll` and Fuchsia's ports.Note that Fuchsia does not use Tokio, but employs a very similar strategyfor managing asynchronous tasks. -`futures`是用于处理异步任务的板条箱。这些任务由异步工作单元组成，这些异步工作单元可能产生单个值（“ Future”）或多个值（“ Stream”）。可以在async函数或块中对Future进行“等待”，这将导致当前任务被暂停，直到Future能够取得更大的进展。有关Future的更多信息，请参见[crate's documentation] [docs]。要了解有关期货内部结构的更多信息，请参阅[本文] [Tokio内部]，以了解期货如何连接到诸如epoll和Fuchsia的端口之类的系统等待原语。请注意，Fuchsia不使用Tokio，而是采用非常相似的策略来管理异步任务。

[docs]: https://rust-lang-nursery.github.io/futures-api-docs/0.3.0-alpha.5/futures/ [`Stream`]: https://docs.rs/futures/0.2.0/futures/stream/trait.Stream.html[Tokio internals]: https://cafbit.com/post/tokio_internals/[zero-sized type]: https://doc.rust-lang.org/nomicon/exotic-sizes.html#zero-sized-types-zsts [docs]：https://rust-lang-nursery.github.io/futures-api-docs/0.3.0-alpha.5/futures/ [Stream]]：https://docs.rs/futures/ 0.2.0 / futures / stream / trait.Stream.html [Tokio内部]：https://cafbit.com/post/tokio_internals/ [零尺寸类型]：https://doc.rust-lang.org/nomicon /exotic-sizes.htmlzero-sized-types-zsts

 
### `fn main`  `fn main` 

Everything starts with main():  一切都以main（）开始：

```rust
{% includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="garnet/examples/fidl/echo_server_rust/src/main.rs" region_tag="main" adjust_indentation="auto" %}
```
 

`main` creates a `ServiceFs` and asynchronously runs it to completion. You may notice that `main` is `async`.The `run_singlethreaded`, `run`, and `run_until_stalled` macros fromthe `fuchsia_async` crate can be used to run asynchronous `main` or testfunctions to completion using the `fuchsia_async::Executor`. main会创建一个ServiceFs并异步运行它以完成操作。您可能会注意到main是异步的。fuchsia_async板条箱中的run_singlethreaded`，run和run_until_stalled宏可用于运行异步main或测试功能，并使用fuchsia_async完成：执行器`。

`main` also returns `Result<(), Error>`. If an `Error` is returned from `main` as a result of one of the `?` lines, the error will be `Debug` printed andthe program will return with a status code indicating failure. `main`还返回`Result <（），Error>`。如果由于“？”行之一从“ main”返回“ Error”，则将打印“ Debug”错误，程序将返回状态代码，指示失败。

The `ServiceFs` represents a filesystem containing various services. Services exposed inside the `"svc"` directory will be offered to othercomponents. The `add_fidl_service` function can be used to offer a`\[Discoverable\]` FIDL service inside the file system. “ ServiceFs”代表包含各种服务的文件系统。在“ svc”目录中公开的服务将提供给其他组件。 `add_fidl_service`函数可用于在文件系统内部提供\\ [Discoverable \] FIDL服务。

The `add_fidl_service` function accepts any closure with a `RequestStream` argument type. This closure can return a value of any type, but the returntype of all closures passed to `add_fidl_service` must match. The returnvalues of all `add_fidl_service` closures will become the elements in the`ServiceFs` stream. add_fidl_service函数接受带有RequestStream参数类型的任何闭包。这个闭包可以返回任何类型的值，但是传递给`add_fidl_service`的所有闭包的returntype必须匹配。所有add_fidl_service闭包的返回值将成为ServiceFs流中的元素。

In this case, the argument to `add_fidl_service` is an `IncomingService` enum variant constructor which accepts a value of type `EchoRequestStream`and returns a value of type `IncomingService`. In this simple example, the`IncomingService` enum is redundant and could be replaced with a simplefunction `|stream| stream` that directly passed-through the`EchoRequestStream` (causing the `ServiceFs` stream to yield values of type`EchoRequestSTream` rather than values of type `IncomingService`).However, more complex servers may offer multiple services, in which case thevarious types of incoming `RequestStream`s will need to be returned from thestream as a single `enum` type. 在这种情况下，add_fidl_service的参数是IncomingService枚举变量构造函数，该构造函数接受类型为EchoRequestStream的值并返回类型为IncomingService的值。在这个简单的示例中，IncomingService枚举是多余的，可以用简单的功能|| stream |代替。直接通过EchoRequestStream的流（导致ServiceFs流产生EchoRequestSTream类型的值，而不是IncomingService类型的值）。但是，更复杂的服务器可能会提供多种服务，在这种情况下，输入的RequestStream类型将需要作为单个enum类型从stream中返回。

In order to offer services to the outside world, we need to call the `take_and_serve_directory_handle` function. This function removes thecurrent process's directory handle and connects it to `ServiceFs`.Note that, since this removes the handle from the process's handle table,this function can only be called once per process. If you wish to providea `ServiceFs` to a different channel, you can use the `serve_connection`function. 为了向外界提供服务，我们需要调用`take_and_serve_directory_handle`函数。该函数删除当前进程的目录句柄，并将其连接到“ ServiceFs”。请注意，由于这会从进程的句柄表中删除该句柄，因此每个进程只能调用一次此函数。如果您希望向另一个频道提供“ ServiceFs”，则可以使用“ serve_connection”功能。

To actually run our filesystem, we'll need to handle the incoming stream of request streams (one request stream per client connection). We use`for_each_concurrent` to loop over the `IncomingService`s and`run_echo_server` for each of them. Note that we use `for_each_concurrent`rather than `for_each` or a manual `while let` loop in order to servemultiple client connections concurrently. 为了实际运行我们的文件系统，我们需要处理请求流的传入流（每个客户端连接一个请求流）。我们使用for_each_concurrent来循环访问IncomingService和run_echo_server。注意，我们使用`for_each_concurrent`而不是`for_each`或手动的`while let`循环，以便同时服务多个客户端连接。

 
### `fn run_echo_server`  `fn run_echo_server` 

```rust
{% includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="garnet/examples/fidl/echo_server_rust/src/main.rs" region_tag="run_echo_server" adjust_indentation="auto" %}
```
 

In `run_echo_server`, we serve all requests for a particular client connection (one `EchoRequestStream`). Because we don't need to do any asynchronous workwhen processing a request, there's no value in processing requests concurrently,so we use a simple `while let` loop to iterate over and respond to each request. 在`run_echo_server`中，我们为一个特定的客户端连接（一个`EchoRequestStream`）提供所有请求。由于在处理请求时不需要执行任何异步工作，因此并发处理请求没有任何价值，因此我们使用一个简单的“ while let”循环来迭代并响应每个请求。

The `.try_next()` function will return a future which yields a value of type `Result<Option<EchoRequest>, fidl::Error>`. We `await!` the future, causingthe current task to yield if no request is yet available. When a valuebecomes available, `await!` returns the result. We apply a `context("...")`to give some information about the error that may have occurred, and use`?` to return early in the error case. If no request is available, thisexpression will result in `None`, the `while` loop will exit, and we return`Ok`. `.try_next（）`函数将返回一个future，该future的结果类型为`Result <Option <EchoRequest>，fidl :: Error>。我们“等待”未来，如果没有可用的请求，则导致当前任务产生。当值变为可用时，`await！`返回结果。我们使用“ context（“ ...”）”来提供有关可能发生的错误的一些信息，并使用“？”在错误情况下尽早返回。如果没有请求可用，则此表达式将导致“无”，退出“ while”循环，然后返回“确定”。

When a request is received, we use pattern-matching to extract the contents of the `EchoString` variantof the `EchoRequest` enum. For a protocol with more than one type of request,we would instead write `|x| match x { MyServiceRequest::Req1 { ... } => ... }`.In our case, we receive `value`, an optional string, and `responder`, a controlhandle with a `send` method for sending a response. 当收到请求时，我们使用模式匹配来提取EchoRequest枚举的EchoString变体的内容。对于具有多种请求类型的协议，我们改写`| x | match x {MyServiceRequest :: Req1 {...} => ...}`。在我们的示例中，我们收到了“ value”（一个可选字符串）和“ responder”（一个带有处理方法，用于发送发送请求的控件句柄）响应。

We log the request using `println!`, and then convert `Option<String>` into `Option<&str>`. This is necessary because `s` is an `Option<String>`, but our `send` method takes back an`Option<&str>` (to allow sending back non-heap-allocated strings). To convert betweenthe two, we use `.as_ref()` to go from `Option<String>` to `Option<&String>`,and then `.map(|s| s.as_str())` to go from `Option<&String>` to `Option<&str>`. 我们使用println！记录请求，然后将Option <String>转换为Option <str>。这是必需的，因为s是一个Option <String>，但是我们的send方法会返回一个Option <str>（以允许发送回未分配的字符串）。要在两者之间进行转换，我们使用.as_ref（）从Option <String>转到Option <String>，然后使用.map（| s | s.as_str（））从Option <String>`到`Option <str>`。

You might well ask why we used `as_ref` at all, since we immediately dereference the resulting `&String` (this happens implicitly, when wecall the `.as_str()` method). This is necessary in order to make sure thatwe're still borrowing from the initial `Option<String>` value. `Option::map`takes `self` by value and so consumes its input, but we want to instead createa *reference* to its input. 您可能会问为什么我们完全使用`as_ref`，因为我们立即取消了对结果`String`的引用（这在我们调用`.as_str（）方法时隐式发生）。为了确保我们仍然从初始的Option <String>值中借用，这是必要的。 Option :: map通过值获取self，因此消耗其输入，但是我们想改为为其输入创建引用。

Once we've done the conversion from `Option<String>` to `Option<&str>`, we call `send`, which returns a `Result<(), Error>` which we use `?` on to return anerror on failure. 一旦完成从Option <String>到OptionOption的转换，我们将调用send，它返回一个result <（），Error>，并使用`？`返回错误。失败。

Finally, we call `.unwrap_or_else(|e| ...)` on our `async move { ... }` block to handle the case in which an error occurred. 最后，我们在异步移动{...}块上调用`.unwrap_or_else（| e | ...）`来处理发生错误的情况。

 
## `Echo` client  回声客户端 

The echo client implementation can be found at:  回显客户端实现可以在以下位置找到：

[//garnet/examples/fidl/echo_client_rust/src/main.rs](/garnet/examples/fidl/echo_client_rust/src/main.rs)  [//garnet/examples/fidl/echo_client_rust/src/main.rs](/garnet/examples/fidl/echo_client_rust/src/main.rs）

Our simple client does everything in `main()`.  我们的简单客户端会执行`main（）`中的所有操作。

Note: a component can be a client, a service, or both, or many. The distinction in this example between Client and Server is purely fordemonstration purposes. 注意：组件可以是客户端，服务或两者兼有，也可以是多个。在此示例中，客户端和服务器之间的区别纯粹是出于演示目的。

Here is the summary of how the client makes a connection to the echo service.  这是客户端如何建立与回显服务的连接的摘要。

 
1.  **Launch:** The server component is specified, and we request for it to be launched if it wasn't already. Note that this step isn't included inmost production FIDL-using components: generally you're connecting withan already-running server component. 1. **启动：**已指定服务器组件，如果尚未启动，我们要求启动它。请注意，此步骤并未包含在大多数使用FIDL的生产组件中：通常，您正在与一个已经在运行的服务器组件进行连接。
1.  **Connect:** We call `connect_to_service` on the launched server component and get back a proxy with methods for making IPC calls tothe remote server. 1. **连接：**我们在已启动的服务器组件上调用`connect_to_service`，并返回具有对远程服务器进行IPC调用的方法的代理。
1.  **Call:** We call the `echo_string` method with the desired value to echo, get back a `Future` of the response, and `map` the future so thatthe response will be logged once it is received. 1. ** Call：**我们调用具有所需值的`echo_string`方法以回显，获取响应的'Future'，并映射'future'，以便一旦接收到响应就将其记录下来。
1.  **Run:** We run the future to completion on an asynchronous task executor.  1. **运行：**我们将未来运行在异步任务执行器上。

```rust
{% includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="garnet/examples/fidl/echo_client_rust/src/main.rs" region_tag="main" adjust_indentation="auto" %}
```
 

 
### Run the sample  运行样本 

You can run the echo example like this:  您可以这样运行echo示例：

```sh
$ run fuchsia-pkg://fuchsia.com/echo_client_rust#meta/echo_client_rust.cmx
```
 

