 
# FIDL  FIDL 

FIDL (or "**F**uchsia **I**nterface **D**efinition **L**anguage") is the IPC system for Fuchsia.  FIDL（或“ **紫红色**接口**定义**语言”）是紫红色的IPC系统。

 
## Start here  从这里开始 

The [tutorial](tutorial/README.md) presents a simple "*Hello, world*" client and server, showing the FIDL language definitions and continuing with sectionsspecific to each supported target language (e.g., C++, Dart). [tutorial]（tutorial / README.md）提供了一个简单的“ * Hello，world *”客户端和服务器，显示了FIDL语言定义，并继续了每种受支持目标语言（例如C ++，Dart）的特定部分。

Read the [Introduction](intro/README.md) section to get a brief overview of what FIDL is, including some of its design goals, requirements, and workflow. 阅读[Introduction]（intro / README.md）部分，以简要了解FIDL是什么，包括FIDL的一些设计目标，要求和工作流程。

 
## Language support  语言支持 

The FIDL code generator creates code in a multitude of target languages. The following table gives you a reference to the details of the language implementaion,as well as pointers to the code generated from the [tutorial's](tutorial/README.md)"*Hello, world*" client and server examples. FIDL代码生成器以多种目标语言创建代码。下表为您提供了有关语言实现的详细信息的参考，以及从[教程]（tutorial / README.md）“ * Hello，world *”客户端和服务器示例生成的代码的指针。

Language                     | Examples -----------------------------|---------------------------------------------[C][c-lang]                  |                        [server][csrv-ex][Low-Level C++][llcpp-lang]  | [client][llcppcli-ex], [server][llcppsrv-ex][High-Level C++][hlcpp-lang] | [client][hlcppcli-ex], [server][hlcppsrv-ex][Dart][dart-lang]            | [client][dartcli-ex],  [server][dartsrv-ex][Rust][rust-lang]            | [client][rustcli-ex],  [server][rustsrv-ex] 语言|例子----------------------------- | ------------------- -------------------------- [C] [c-lang] | [服务器] [csrv-ex] [低级C ++] [llcpp-lang] | [客户端] [llcppcli-ex]，[服务器] [llcppsrv-ex] [高级C ++] [hlcpp-lang] | [客户] [hlcppcli-ex]，[服务器] [hlcppsrv-ex] [Dart] [dart-lang] | [客户] [dartcli-ex]，[服务器] [dartsrv-ex] [Rust] [rust-lang] | [客户] [rustcli-ex]，[服务器] [rustsrv-ex]

 
# Contributing  贡献Please read the [CONTRIBUTING](CONTRIBUTING.md) chapter for more information.  请阅读[CONTRIBUTING]（CONTRIBUTING.md）一章以获取更多信息。

 
# References  参考文献 

 
* [ABI and Source Compatibility Guide](reference/abi-compat.md) &mdash; how to evolve FIDL APIs  * [ABI和源兼容性指南]（reference / abi-compat.md）mdash;如何发展FIDL API
* [API Rubric][fidl-api] &mdash; design patterns and best practices  * [API专栏] [fidl-api] mdash;设计模式和最佳做法
* [Style Rubric][fidl-style] &mdash; style guide  * [Style Rubric] [fidl-style] mdash;时尚指南
* [Attributes](reference/attributes.md) &mdash; describes the available FIDL attributes  * [属性]（reference / attributes.md）–描述可用的FIDL属性
* [Bindings](reference/bindings.md) &mdash; requirements for FIDL language bindings  * [绑定]（reference / bindings.md）mdash; FIDL语言绑定的要求
* [Compiler](reference/compiler.md) &mdash; describes the organization of the compiler  * [编译器]（reference / compiler.md）-描述编译器的组织
* [Linter](reference/linter.md) &mdash; describes how to check API readability with the FIDL linter  * [Linter]（reference / linter.md）mdash;介绍如何使用FIDL linter检查API的可读性
* [Editors](reference/editors.md) &mdash; discusses support for FIDL in IDEs and stand-alone editors  * [编辑]（reference / editors.md）-讨论在IDE和独立编辑器中对FIDL的支持
* [FIDL Tuning Proposals](reference/ftp/README.md) &mdash; accepted and rejected changes for FIDL  * [FIDL调整建议]（reference / ftp / README.md）mdash;接受和拒绝FIDL的更改
* [Grammar](reference/grammar.md) &mdash; the FIDL grammar  * [语法]（reference / grammar.md）mdash; FIDL语法
* [Host](reference/host.md) &mdash; summary of the parts of FIDL that are allowed on host  * [Host]（reference / host.md）mdash;主机上允许的FIDL部分的摘要
* [JSON IR](reference/json-ir.md) &mdash; a tour of the JSON Intermediate Representation (**JSON IR**) generator * [JSON IR]（reference / json-ir.md）mdash; JSON中间表示（** JSON IR **）生成器浏览
* [Language](reference/language.md) &mdash; defines the syntax of the FIDL language  * [Language]（reference / language.md）mdash;定义FIDL语言的语法
* [`library zx`](reference/library-zx.md) &mdash; the Zircon system library  * [`library zx`]（reference / library-zx.md）mdash; Zircon系统库
* [Wire Format](reference/wire-format/README.md) &mdash; details the byte-by-byte organization of data * [Wire格式]（reference / wire-format / README.md）mdash;详细说明数据的逐字节组织

<!-- xrefs --> [fidl-style]: /docs/development/languages/fidl/style.md[fidl-api]: /docs/development/api/fidl.md <！-外部参照-> [fidl-style]：/docs/development/languages/fidl/style.md[fidl-api]：/docs/development/api/fidl.md

<!-- these in particular make the table manageable, and have the form: <language>-lang (the language part)<language>cli-ex (the client example)<language>srv-ex (the server example)--> <！-这些尤其使表易于管理，并具有以下形式：<language> -lang（语言部分）<language> cli-ex（客户端示例）<language> srv-ex（服务器示例）- ->

[c-lang]: tutorial/tutorial-c.md [csrv-ex]: /garnet/examples/fidl/echo_server_c/ [c-lang]：tutorial / tutorial-c.md [csrv-ex]：/ garnet / examples / fidl / echo_server_c /

[llcpp-lang]: tutorial/tutorial-llcpp.md [llcppcli-ex]: /garnet/examples/fidl/echo_client_llcpp/[llcppsrv-ex]: /garnet/examples/fidl/echo_server_llcpp/ [llcpp-lang]：tutorial / tutorial-llcpp.md [llcppcli-ex]：/ garnet / examples / fidl / echo_client_llcpp / [llcppsrv-ex]：/ garnet / examples / fidl / echo_server_llcpp /

[hlcpp-lang]: tutorial/tutorial-cpp.md [hlcppcli-ex]: /garnet/examples/fidl/echo_client_cpp/[hlcppsrv-ex]: /garnet/examples/fidl/echo_server_cpp/ [hlcpp-lang]：tutorial / tutorial-cpp.md [hlcppcli-ex]：/ garnet / examples / fidl / echo_client_cpp / [hlcppsrv-ex]：/ garnet / examples / fidl / echo_server_cpp /

[dart-lang]: /docs/development/languages/fidl/tutorial/tutorial-dart.md [dartcli-ex]: https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/echo_client_async_dart/[dartsrv-ex]: https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/echo_server_async_dart/ [dart-lang]：/docs/development/languages/fidl/tutorial/tutorial-dart.md [dartcli-ex]：https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/echo_client_async_dart/ [dartsrv-ex]：https://fuchsia.googlesource.com/topaz/+/master/examples/fidl/echo_server_async_dart/

