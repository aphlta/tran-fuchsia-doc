 
# Dart API Readability Rubric  Dart API可读性规则 

[TOC]  [目录]

 

 
## Overview  总览This document describes heuristics and rules for writing Dart libraries that are published in the Fuchsia SDK.  本文档介绍了在Fuchsia SDK中发布的用于编写Dart库的试探法和规则。

Unless otherwise specified, Fuchsia library authors should adhere to all the heuristics and rules recommended by the Dart team itself under [Effective Dart](https://www.dartlang.org/guides/language/effective-dart). Author’s should familiarize themselves with all sections, [Style](https://www.dartlang.org/guides/language/effective-dart/style), [Documentation](https://www.dartlang.org/guides/language/effective-dart/documentation), [Usage](https://www.dartlang.org/guides/language/effective-dart/usage) and [Design](https://www.dartlang.org/guides/language/effective-dart/design) prior to reading this rubric.  除非另有说明，否则紫红色的库作者应遵守Dart团队在[有效Dart]（https://www.dartlang.org/guides/language/effective-dart）下推荐的所有试探法和规则。作者应该熟悉所有部分，[样式]（https://www.dartlang.org/guides/language/effective-dart/style），[文档]（https://www.dartlang.org/guides/language / effective-dart / documentation），[用法]（https://www.dartlang.org/guides/language/effective-dart/usage）和[设计]（https://www.dartlang.org/guides/language / effective-dart / design）之前，请先阅读本主题。

 
### Terminology  术语There are some terms of art that Dart uses which conflict with Fuchsia’s terminology.   Dart使用的某些艺术术语与Fuchsia的术语冲突。

 
- [Fuchsia package](/garnet/go/src/pm/README.md#structure-of-a-fuchsia-package): A Fuchsia package is one or more collections of files that provide one or more programs, components or services for a Fuchsia system.  -[Fuchsia软件包]（/ garnet / go / src / pm / README.mdstructure-of-a-fuchsia-package）：Fuchsia软件包是一个或多个文件集合，可为一个或多个文件提供一个或多个程序，组件或服务。紫红色的系统。
- Fuchsia library: An informal definition for implementation code used by Fuchsia, usually found in lib or lib/src directories. Libraries are a convention, most policies for libraries are enforced socially or fallback to language specific approaches and tooling.  -紫红色的库：紫红色使用的实现代码的非正式定义，通常在lib或lib / src目录中找到。图书馆是一种惯例，大多数图书馆政策是在社会上强制执行的，或者回退到特定于语言的方法和工具上。
- [Dart package](https://dart.dev/guides/packages): The Dart package system is used to share software like libraries and tools within the Dart ecosystem, e.g. via Pub. Often a package is a collection of files with a minimum of a pubspec.yaml file and at least one Dart file, in-tree Dart packages will also have a `BUILD.gn` file.  -[Dart包]（https://dart.dev/guides/packages）：Dart包系统用于共享Dart生态系统中的软件，例如库和工具。通过Pub。通常，程序包是文件集合，其中至少包含pubspec.yaml文件和至少一个Dart文件，树内Dart程序包也将具有`BUILD.gn`文件。
- [Dart library](https://dart.dev/tools/pub/package-layout#public-libraries): A collection of Dart code (classes, constants, typedefs, etc.) isolated to a single namespace and corresponding to a single entry point, e.g. `import 'package:enchilada/enchilada.dart';` imports the enchilada library. Note that Dart libraries have a privacy boundary, e.g. private implementation details are not visible or accessible outside of the library. A Dart package can contain multiple Dart Libraries.  -[Dart库]（https://dart.dev/tools/pub/package-layoutpublic-libraries）：Dart代码的集合（类，常量，typedef等），隔离到单个名称空间并对应于单个入口点，例如`import'package：enchilada / enchilada.dart';`导入enchilada库。请注意，Dart库具有隐私边界，例如私有实现细节在库外部不可见或不可访问。 Dart程序包可以包含多个Dart库。

When writing Dart code it is important to understand the distinction in terminology in order to remain clear when communicating with team members whose primary language might be one of the other supported languages (C++, Rust, etc.).   在编写Dart代码时，重要的是要理解术语的区别，以便与主要语言可能是其他受支持的语言之一（C ++，Rust等）的团队成员进行交流时保持清晰。

 
- A Fuchsia package can contain components implemented as Dart binaries.  -紫红色的包可以包含以Dart二进制文件实现的组件。
- A Dart binary is defined within a Dart package, and often has dependencies on other Dart packages.  -Dart二进制文件在Dart程序包中定义，并且通常与其他Dart程序包具有依赖性。
- Code shared as a library in Fuchsia’s tree written in Dart is implemented as a Dart package.  -在Dart编写的紫红色的树中作为库共享的代码以Dart包的形式实现。

 
### Focus on the Interfaces  专注于界面Public classes should expose a clean user interface which clearly describes the API surface and is free from internal implementation details. Classes which contain more than a minimal amount of functionality should expose their API in an abstract class with the implementation inside a private implementation file. Doing so allows for the users of the classes to focus on the public methods and forces the implementer to think about the usage of the class before implementation.  公共类应公开一个清晰的用户界面，该界面应清楚地描述API表面，并且不应包含内部实现细节。包含大量功能的类应在一个抽象类中公开其API，并将其实现包含在私有实现文件中。这样做允许类的用户专注于公共方法，并迫使实现者在实现之前考虑类的用法。

 
### Consider Composability  考虑可组合性When designing the API consider how it will fit into the larger Dart ecosystem of libraries. For example, if writing an API which delivers events consider using Streams instead of callbacks because they compose better with libraries like Flutter.  在设计API时，请考虑它如何适合更大的Dart库生态系统。例如，如果编写提供事件的API，请考虑使用Streams而不是回调，因为它们与Flutter之类的库可以更好地组合。

 
## Lint Rules  皮棉规则Dart code written against the Fuchsia SDK should pass all the lint rules specified by the [analysis_options.yaml](https://fuchsia.googlesource.com/topaz/+/refs/heads/master/tools/analysis_options.yaml) file which lives in the topaz repository. These lint rules will help to automate the review API review process. There are situations where a lint rule may be in conflict with a specific API and may need to be explicitly ignored. If a file is opting out of a lint rule the developer must provide a comment explaining the reasoning for opting out of the lint rule.  针对Fuchsia SDK编写的Dart代码应通过[analysis_options.yaml]（https://fuchsia.googlesource.com/topaz/+/refs/heads/master/tools/analysis_options.yaml）文件指定的所有皮棉规则，生活在黄玉仓库中。这些棉绒规则将有助于自动执行审阅API审阅过程。在某些情况下，棉绒规则可能与特定的API冲突，可能需要显式忽略。如果文件选择不使用棉绒规则，则开发人员必须提供注释，说明选择不使用棉绒规则的原因。

 
## Library Structure  图书馆结构When organizing the structure of a Dart package it is important to follow the recommendations laid out by the [Effective Dart](https://www.dartlang.org/guides/language/effective-dart) style guide. Additionally, developers should consider how their code is exported. For a more complicated package, developers should avoid a singular catch all top-level export file and rather expose a top level file per logical grouping of classes that make sense to be pulled under one import line. This allows users of the library the ability to have finer grained control over which sections of the library they import. An example is a package which contains functionality for both agents and modules. In this scenario, we could have one import for agents and one for modules but they could be in the same package.   在组织Dart软件包的结构时，请务必遵循[Effective Dart]（https://www.dartlang.org/guides/language/effective-dart）样式指南提出的建议。此外，开发人员应考虑如何导出其代码。对于更复杂的程序包，开发人员应避免单个捕获所有顶级导出文件，而应按有意义的类的逻辑分组公开顶级文件，这些类有意义地被拉到一个导入行下。这使库的用户能够对他们导入的库的哪些部分进行更精细的控制。一个示例是一个包，其中包含代理和模块的功能。在这种情况下，我们可以一次导入代理，一次导入模块，但是它们可以在同一包中。

 
## Comments/Documentation  评论/文档All comments should adhere to [Effective Dart: Documentation](https://www.dartlang.org/guides/language/effective-dart/documentation) as well as the [Fuchsia Documentation](documentation.md) guide.  所有评论均应遵守[Effective Dart：Documentation]（https://www.dartlang.org/guides/language/effective-dart/documentation）和[Fuchsia Documentation]（documentation.md）指南。

 
## Dependencies  依存关系Packages written for the Dart Fuchsia SDK should not take on third party dependencies that are not themselves also in the Fuchsia SDK. Exceptions will be made for the following, well established, dependencies which are likely to be present in all environments. Any packages which should be added to this list must be approved by the [API Council](council.md).  为Dart Fuchsia SDK编写的程序包不应具有Fuchsia SDK本身也不具有的第三方依赖性。对于以下在所有环境中都可能存在的，已经建立的，良好的依赖项，将有所例外。任何应添加到此列表中的软件包都必须经过[API委员会]（council.md）的批准。

 
- [logger](https://pub.dev/packages/logging)  -[logger]（https://pub.dev/packages/logging）
- [meta](https://pub.dev/packages/meta)  -[meta]（https://pub.dev/packages/meta）
- [intl](https://pub.dev/packages/intl)  -[intl]（https://pub.dev/packages/intl）
- [flutter](https://flutter.dev/)  -[flutter]（https://flutter.dev/）

 

Packages which do take on external dependencies should consider whether they want to reexport those symbols. If the dependency is reexported then the generated documentation will generate documentation for the external dependency. However, reexporting the dependency will create a tight coupling between package versions.  确实具有外部依赖性的程序包应考虑它们是否要重新导出这些符号。如果重新导出依赖项，则生成的文档将为外部依赖项生成文档。但是，重新导出依赖项将在软件包版本之间建立紧密的耦合。

 
## Formatting  格式化Code should be formatted using the `dartfmt` tool. This is an opinionated tool that cannot be configured. Formatting all of our code with this tool will ensure consistency. In Fuchsia, you can use `fx format-code` will run `dartfmt` on all staged dart files.   代码应使用“ dartfmt”工具格式化。这是一个无法配置的工具。使用此工具格式化我们所有的代码将确保一致性。在紫红色中，您可以使用`fx format-code`在所有暂存的dart文件中运行`dartfmt`。

 
## Files  档案 

 
- DO name files after their public class name  -在文件的公共类名称之后命名文件
- PREFER placing each class into their own files, even if they’re private. It should be rare for multiple classes to live in the same file. Only private, small, simple and standalone classes can share a file with a public class.  -即使每个班级都是私人的，也应将每个班级放到各自的文件中。多个类驻留在同一文件中应该很少。只有私有，小型，简单和独立的类可以与公共类共享文件。
- AVOID creating utility classes or libraries, these tend to turn into code dumping grounds. Instead, use precise naming that clearly communicates the purpose of the code being created.  -避免创建实用程序类或库，这些倾向于变成代码转储的场所。相反，使用精确的命名可以清楚地传达所创建代码的目的。
- DON’T use the `part of` directive to avoid tight coupling of classes.  -不要使用`part of`指令来避免类的紧密耦合。

 
### Methods  方法 

 
- PREFER using named parameters vs positional parameters for public methods on public classes that have greater than 2 parameters. This aids code refactor and allowed adding extra parameters without breaking the public API contract.   -对于具有大于2个参数的公共类，对公共方法优选使用命名参数与位置参数。这有助于代码重构，并允许添加额外的参数而不会违反公共API合同。
- AVOID using functions which can do more than one thing like `void updateAndCommit();` but prefer explicit naming   -避免使用函数，这些函数可以做多个事情，例如`void updateAndCommit（）;`，但更喜欢显式命名

 
### Constructors  建设者 

 
- PREFER using named parameters with Constructors that have more than two parameters.  -优选将命名参数与具有两个以上参数的构造函数一起使用。
- DO use the meta package to indicate which parameters are required.  -不要使用meta包来指示需要哪些参数。
- DO assert on required parameters.  -确认必需的参数。
- DO throw exceptions/errors for public API which will have detrimental side effects if invalid input is passed to constructors since asserts do not run in release builds.  -不要为公共API抛出异常/错误，如果将无效输入传递给构造函数，则将产生有害的副作用，因为断言不在发行版本中运行。

```
/// Constructs a [Car] object
///
/// If [id] is not provided one will be
/// generated with a UUID4 format.
Car({
  @required this.make,
  @required this.model,
  this.id,
}) : assert(make != null),
     assert(model != null);
```
 

 
## Naming  命名If a method will use a cached object, or create it if it doesn’t exist, avoid introducing or into the name.  如果某个方法将使用缓存的对象，或者如果该方法不存在，则创建它，请避免在名称中引入或引入名称。

```
class Node {
  //BAD
  Node getOrCreateChild(String name);
              
  //GOOD
  Node child(String name);
}
```
 

When adding a function or interface which will have methods invoked in response to another action, name the methods add<NAME>Listener() and remove<NAME>Listener(). The objects which implement the <NAME>Listener interface should name the invoked methods on<EVENT>.  当添加将调用方法以响应另一个动作的函数或接口时，将方法命名为add <NAME> Listener（）和remove <NAME> Listener（）。实现<NAME> Listener接口的对象应在<EVENT>上命名调用的方法。

```
class MediaController {
  void addMediaListener(MediaListener listener) {}
  void removeMediaListener(MediaListener listener) {}
}

abstract class MediaListener {
  void onPause();
  void onPlay();
}
```
 

When appending an item to your object prefer the name add<Name> instead of append to follow the dart list naming.  将项目附加到对象时，最好使用名称add <Name>而不是append来遵循飞镖列表的命名。

When deciding between using a single member abstract or a plain `Function` as a `Listener` object consider how your API might evolve over time. If you expect that you may add more methods to the listener use a single member abstract to allow for the evolution but if the API is not likely to change use a plain function.  在决定使用单个成员摘要还是简单的“函数”作为“侦听器”对象之间时，请考虑您的API随时间的变化。如果希望您可以向侦听器添加更多方法，请使用单个成员摘要来进行演化，但是如果API不太可能更改，请使用简单函数。

```
// This could logically grow to include an onDoubleTap()
// method so it makes sense to use a single member abstract.
abstract class TapListener {
  void onTap();
}
void addTapListener(TapListener listener) { ... } 

// This will likely never need more methods so it can 
// clearly take a function type.
void addOnCloseListener(void Function() listener) { ... }
```
 

 
## Preferred Types  首选类型Concrete data types should be used instead of lower level primitives. The following types should be used when possible:  应该使用具体的数据类型代替较低级别的原语。如果可能，应使用以下类型：

 
- [Duration](https://api.dartlang.org/stable/2.4.0/dart-core/Duration-class.html) when working with a span of time.  -在一段时间内使用[Duration]（https://api.dartlang.org/stable/2.4.0/dart-core/Duration-class.html）。
- [DateTime](https://api.dartlang.org/stable/2.4.0/dart-core/DateTime-class.html) when working with dates.  -处理日期时，[DateTime]（https://api.dartlang.org/stable/2.4.0/dart-core/DateTime-class.html）。

If there is not a concrete type which can be used to represent your object at a higher level your API should expose one. For example, if we had an API which dealt with currency we would create a `Currency` data type instead of working with `num` types.   如果没有一种具体的类型可以用来在更高级别上表示您的对象，则您的API应该公开一种。例如，如果我们有一个处理货币的API，我们将创建一个“ Currency”数据类型，而不是使用“ num”类型。

```
// BAD
int getCash() { ... }

// GOOD
Currency getCash() { ... }
```
 

Your API should avoid returning unstructured JSON data but rather transform any JSON into a typed value.  您的API应该避免返回非结构化JSON数据，而应将任何JSON转换为类型化的值。

```
// BAD
Map<String, dynamic> getCar() => {
    'make': 'Toyota',
    'year': 2019, 
}

// Good
Car getCar() => Car(make: 'Toyota', year: 2019);
```
 

 
## Internationalization  国际化If a package exposes a user visible string the string should be internationalized. In the absence of an ability to internationalize a user visible string the API should return data in which a user of a library can construct an internationalized string.  如果程序包公开了用户可见的字符串，则该字符串应进行国际化。在没有国际化用户可见字符串的能力的情况下，API应该返回数据库用户可以在其中构造国际化字符串的数据。

Exceptions and log messages do not need to be internationalized if they are not intended to be user visible.  如果异常和日志消息不希望用户可见，则无需对其进行国际化。

 
## Error Handling  错误处理All error handling should adhere to [Effective Dart: Error handling](https://www.dartlang.org/guides/language/effective-dart/usage#error-handling).   所有错误处理都应遵守[有效Dart：错误处理]（https://www.dartlang.org/guides/language/effective-dart/usageerror-handling）。

 
## Error vs. Exception  错误与异常Error and its subclasses are for programmatic errors that shouldn’t be explicitly caught. An Error indicates a bug in your code, it should unwind the entire call stack, halt the program, and print a stack trace so you can locate and fix the bug.  错误及其子类用于不应明确捕获的程序错误。错误表示代码中存在错误，它应展开整个调用堆栈，暂停程序并打印堆栈跟踪，以便您可以找到并修复该错误。

Non-Error exception classes are for runtime errors. If your API implementation throws an exception, it should be documented as part of the public API and it’s expected behavior. This will facilitate programmatic handling of the exception by API clients.  非错误异常类用于运行时错误。如果您的API实现引发异常，则应将其记录为公共API的一部分，并应作为其预期的行为。这将有助于API客户端以编程方式处理异常。

Except in a few special circumstances, idiomatic Dart should throw Errors, but never catch them. They exist specifically to not be caught so that they take down the app and alert the programmer to the location of the bug.  除少数特殊情况外，惯用的Dart应该抛出错误，但决不要抓住它们。专门存在它们是为了不被捕获，以便它们关闭应用程序并警告程序员该错误的位置。

Note: often times people refer to Error when they mean Exception and vice versa. Especially developers that are coming from a different language. Apply your knowledge of their difference when developing your Dart API.  注意：通常人们在指异常时指错误，反之亦然。特别是来自不同语言的开发人员。在开发Dart API时运用它们的区别知识。

Your public API should throw well defined and typed exceptions so that users can catch them and react appropriately. If you are not in control of all the code that is being called by your package, maybe because you are using a third party library, you may not be able to know exactly which exceptions may be thrown. If this is the case, you can either attempt to catch the exception and wrap it in a type that you create or clearly document that an exception of unknown type may be thrown.  您的公共API应该引发定义明确且类型明确的异常，以便用户可以捕获它们并做出适当反应。如果您无法控制程序包正在调用的所有代码，则可能是因为使用的是第三方库，则可能无法确切知道可能会抛出哪些异常。在这种情况下，您可以尝试捕获异常并将其包装在您创建的类型中，或者清楚地记录可能抛出未知类型的异常。

If your API can fail in more than one way the exception should clearly indicate the failure method. Consider throwing different types of exceptions or adding a code to the exception so the caller can respond appropriately. Also, don’t forget to publicly document all the exceptions that are potentially thrown by a given method.  如果您的API可能以多种方式失败，则异常应明确指出失败方法。考虑抛出不同类型的异常或向异常添加代码，以便调用者可以适当地响应。另外，不要忘记公开记录给定方法可能引发的所有异常。

```
enum ErrorCode { foo, bar }

class MyException implements Exception {
  final ErrorCode code;
  MyException(this.code);
}

/// Throws MyException(ErrorCode.foo) if condition is true or
/// throws MyException(ErrorCode.bar) if not 
void baz(bool condition) {
  If (condition) {
    throw MyException(ErrorCode.foo);
  } else {
    throw MyException(ErrorCode.bar);
  }
}
```
 

 
### Assertions vs. Exceptions  断言与异常Assertions should only be used to verify conditions that should be logically impossible to be false due to programmer error, not user or data input. These conditions should only be based on inputs generated by your own code. Any checks based on external inputs should use exceptions.  断言仅应用于验证由于程序员错误而不是用户或数据输入而在逻辑上不可能为假的条件。这些条件应仅基于您自己的代码生成的输入。基于外部输入的任何检查都应使用异常。

Use asserts when you are in full control of the inputs. For example verify private functions' arguments with asserts, and using exceptions for public functions arguments.  当您完全控制输入时，请使用断言。例如，使用断言验证私有函数的参数，并为公共函数参数使用异常。

In Dart all assertions are compiled out from the production/release builds. Therefore, your program must work just as well when all assertions are removed. Do not directly assert on a value returned directly from a function as this can cause the code to not be included in release build since the entire body of the assert is removed in release builds.  在Dart中，所有断言都是从生产/发布版本中编译出来的。因此，当删除所有断言时，您的程序必须同样工作。不要直接对直接从函数返回的值进行断言，因为这可能导致代码不包含在发行版本中，因为断言的整个主体都在发行版本中删除。

```
// BAD
assert(foo()); // foo is not executed

// GOOD
final success = foo();
assert(success);
```
 

 
### FIDL Exception Handling  FIDL异常处理In Fuchsia, the generated Dart FIDL bindings are always asynchronous, thus all methods return a `Future` even if there is no return value (`Future<void>` is used). Also, when connecting to a particular service the connection is assumed to be successful even though it can fail to connect or disconnect in the future. For these reasons, the caller of any FIDL api should always assume that a specific call can fail and handle that appropriately when needed.   在Fuchsia中，生成的Dart FIDL绑定始终是异步的，因此，即使没有返回值（使用了`Future <void>`），所有方法也会返回“ Future”。同样，当连接到特定服务时，即使将来可能无法连接或断开连接，也假定连接成功。由于这些原因，任何FIDL api的调用者都应始终假定特定调用可能失败，并在需要时适当地进行处理。

```
final _proxy = fidl_myService.MyServiceProxy();
connectToAgentService('fuchsia-pkg://fuchsia.com/my_service#meta/my_service.cmx', _proxy);

_proxy
  .doSomething()
  .catchError((e, s) {
    // handle the error if needed
  });
```
 

 
## Testing  测试中Please review [Dart](https://www.dartlang.org/guides/testing) and [Flutter](https://flutter.dev/docs/testing) testing guides.  请查看[Dart]（https://www.dartlang.org/guides/testing）和[Flutter]（https://flutter.dev/docs/testing）测试指南。

 
- DO test for `Future<T>` when disambiguating a `FutureOr<T>` whose type argument could be Object.  -在消除类型参数可能是Object的FutureOr <T>时，要对Future <T>进行测试。
- DON’T use `@visibleForTesting` on public API.  -不要在公共API上使用“ @visibleForTesting”。

The API surface of your package should be well tested. However, the public API should not need to leak internal details for the class to be testable. Consider the following example:  程序包的API表面应经过良好测试。但是，公共API无需泄漏内部详细信息即可测试该类。考虑以下示例：

```
class Foo {
  // services is exposed for testing
  Foo({GlobalServices services = GlobalServices()}) { … }

  // Connects to the global service with the given name.
  Connection connectToGlobalService(String name) {
     return services.connect(name);
  }
}
```
 

Rather, consider writing your class as an abstract class so the user does not need to know about the injection of global services but tests can directly inject the global services into the implementation. These avoids leaking implementation details to the user and provides an API that the user cannot abuse or mess up. This has the added advantage of allowing the API to evolve if the GlobalServices class evolves without having to change the callers of the method.  而是考虑将您的类编写为抽象类，以便用户无需了解全局服务的注入，但是测试可以将全局服务直接注入到实现中。这些避免了将实施细节泄漏给用户，并提供了用户不能滥用或弄乱的API。这具有额外的优点，即如果GlobalServices类在不更改方法的调用程序的情况下发展，则允许API在发展。
 
```
// foo.dart
abstract class Foo {
  factory Foo() => FooImpl(services: GlobalServices);
  connectToGlobalService(String name);
}

// internal/foo_impl.dart
class FooImpl implements Foo {
  FooImpl({GlobalServices services}) { … }

  // Connects to the global service with the given name.
  Connection connectToGlobalService(String name) {
     return services.connect(name);
  }
}
```
 

Dart does not allow a private class/function to be accessed from within a test. This has the effect that any private classes cannot be tested. This may be ok if there is a corresponding public class/function that can exercise the private members but this may not always be the case. In these situations it is best to move the private class into its own file which does not get exported by the top-level export and make it public. The tests can now access your private members.  Dart不允许在测试中访问私有类/函数。这具有无法测试任何私有类的效果。如果有相应的公开课/功能可以行使私人成员的权限，则可以这样做，但情况并非总是如此。在这些情况下，最好将私有类移到其自己的文件中，该文件不会被顶层导出导出并公开。测试现在可以访问您的私人成员。

```
/// BAD - this code does not make _Taco directly testable

// dinner.dart
class Dinner {
  final _taco = _Taco();
  
  void eat() => _taco.consume();
}

// We have no way to directly test this class
class _Taco {
  void consume() {}
}

/// GOOD - this code makes Taco directly testable by moving it to its own private file

// dinner.dart
import '_taco.dart';

class Dinner {
  final _taco = Taco();
  void eat() => _taco.consume();
}

// _taco.dart 
class Taco {
  void consume() {}
}

// _taco_test.dart
import 'package:dinner/src/_taco.dart' // ignore: implementation_imports

void main() {
  test('taco consumption', () {
    expect(_Taco().consume(), runsNormally);
  });
}
```
 

 
## Design Patterns  设计模式 
### Disallowing Subclassing  禁止子类化It can be useful for a library to declare a common base class without allowing developers to extend the common base class. The common pattern for supporting this is to declare a private constructor on your public base class. This has the effect of allowing subclasses within the same file to extend the base class while not allowing users of your library to subclass the base class.   对于库声明一个公共基类而不允许开发人员扩展该公共基类可能很有用。支持此功能的常见模式是在公共基类上声明一个私有构造函数。这样的效果是允许同一文件中的子类扩展基类，而不允许库的用户子类化基类。

```
/// Base class
abstract class A {
  // private constructor disallows instantiation outside of this file
  ._();
  /// Concrete implementation of foo
  void foo() {}
}

/// A concrete implementation of [A]
class B extends A {
  () : super._();

  @override
  void foo() {
    // B implementation
    super.foo();
  }
}
```
 

It is important to note that this pattern does not restrict users from subclassing the child class since it has a public constructor. If this restriction is required see the factory constructors pattern below.   重要的是要注意，这种模式不会限制用户对子类进行子类化，因为它具有公共构造函数。如果需要此限制，请参见下面的工厂构造函数模式。

This pattern is useful if the implementation surface is small since the pattern requires all of the subclasses to live in the same file as the base class or to use the part of directive which is discouraged. If the surface area is too large for a single file consider an alternate pattern.  如果实现面很小，则此模式很有用，因为该模式要求所有子类与基类位于同一文件中，或者使用不鼓励使用的指令部分。如果单个文件的表面积太大，请考虑使用其他图案。

 

 
### Factory Constructors   工厂建设者There are times when a user only needs to interact with a single interface but which may have a different implementation depending on how the object was constructed. Requiring the user to know about the different implementations can add extra API which is not needed and only serves to confuse the user. In this situation you can define an abstract base class which defines the API surface and create factory constructors which vends the appropriate private class.  有时，用户仅需要与单个界面进行交互，但是根据对象的构造方式，该界面可能具有不同的实现。要求用户了解不同的实现方式可以添加不需要的额外API，而只会使用户感到困惑。在这种情况下，您可以定义一个抽象基类来定义API表面，并创建提供适当私有类的工厂构造函数。

```
// Publicly exported class
abstract class Foo {
  
  factory Foo() => FooImpl();

  factory Foo.withNamespace(String namespace) => NamespacedFoo(namespace);

  void update(String value);
  void revert();
}

// Private implementations not exported in public API
class FooImpl implements Foo {
  final _values = <String>[];

  @override
  void update(String name) => _values.add(name);

  @override
  void revert() => _values.removeLast();
}

class NamespacedFoo extends FooImpl {
  final String namespace;
  NamespacedFoo(this.namespace);

  @override
  void update(String name) => super.update('$namespace/$name');
}
```
 

Note: If you need to add the restriction that the base class cannot be extended you can implement the pattern defined in Disallowing Subclassing which adds a private constructor to the public base class  注意：如果需要添加不能扩展基类的限制，则可以实现“禁止子类化”中定义的模式，该模式将私有构造函数添加到公共基类中

 
### Working with FIDLs  使用FIDLTry to make a clear distinction between regular object types and FIDL types. This makes it easier for the maintainers of the code to identify FIDL types from other types and take the necessary precautions when needed. Consider using the as when importing a FIDL service and prefixing it with “fidl_”, this makes it very to identify FIDL types across the entire file.   尝试在常规对象类型和FIDL类型之间进行明确区分。这使代码的维护者更容易从其他类型中识别FIDL类型，并在需要时采取必要的预防措施。导入FIDL服务并在其前面加上“ fidl_”前缀时，请考虑使用as，这使得非常容易在整个文件中识别FIDL类型。

```
import 'package:fidl_fuchsia_foo/fidl_async.dart' as fidl_foo;

// now it is clear that the return type bar comes from fidl_foo
fidl_foo.Bar myMethod(String baz) {...} 
```
 

When subclassing FIDL types extend them so they can be interchanged with the generated FIDL files. Usually, wrappers decorate the existing type with additional functionality that compliments the original object. However, by extending it from the original FIDL it allows the existing and new API to work with original FIDL types instead of the more concrete types which is useful when interacting with other FIDLs or when developers are not using your wrapper.  子类化FIDL类型时，将它们扩展，以便可以与生成的FIDL文件互换。通常，包装器使用补充原始对象的其他功能来装饰现有类型。但是，通过从原始FIDL扩展它，它允许现有的和新的API与原始FIDL类型一起使用，而不是与更具体的类型一起使用，这在与其他FIDL交互或开发人员不使用您的包装器时非常有用。

 
### Decoupling implementation concerns  解耦实施问题Try to avoid interfaces which cover multiple areas of concerns. By breaking down the concerns users can have more flexibility with how they choose to combine the interfaces and allows composed objects to be passed to methods with specific concerns.  尽量避免覆盖多个关注领域的接口。通过分解关注点，用户可以更加灵活地选择如何组合界面，并允许将组合对象传递给具有特定关注点的方法。

```
void main() {
  final restaurant = lookupRestaurant();
  map.display(restaurant);
  phone.call(restaurant);
}

abstract class Callable {
  String get phoneNumber;
}

abstract class Location {
  String get address;
  String get displayName;
}

class Restaurant implements Callable, Location {
  final String name;
  final String phoneNumber;
  final String address;
  String get displayName => name;

  Restaurant(this.name, this.phoneNumber, this.address);
}

class Map {
  void display(Location descriptor) {}
}

class Phone {
  void call(Callable callable) {}
}
```
 

 
### Iteration of Modifiable Collections  可修改集合的迭代When exposing an API that can modify some sort of collection it is important to protect against modifying the collection during iteration. When iterating over an internal collection consider making a copy of the backing collection to iterate. This will protect from exceptions being thrown for concurrent modification of the underlying collection.  公开可以修改某种集合的API时，重要的是要防止在迭代过程中修改集合。遍历内部集合时，请考虑制作备份集合的副本以进行迭代。这样可以避免因基础集合的并发修改而引发的异常。

```
class Controller {
  final _listeners = <void Function()>[];
  void addListener(void Function() f) => _listeners.add(f);
  bool removeListener(void Function() f) => _listeners.remove(f);

  void notify() {
    // Make a copy to avoid modification of _listeners during iteration.
    for (final f in List.of(_listeners)) {
      // This method can safely call add/remove listeners
      f();
    }
  }    
}
```
 

 
## Anti Patterns  反模式The following patterns should be avoided when writing Dart libraries for the Fuchsia Dart SDK. Exposing Internal Details for TestingIt may be tempting to expose certain aspects of your API for testing concerns. However, doing so can clutter your public interface and leak implementation details which the user does not need to know about or may come to rely on. See the [Testing](#Testing) section for more details 为Fuchsia Dart SDK编写Dart库时，应避免以下模式。公开用于测试的内部详细信息可能很想公开API的某些方面以进行测试。但是，这样做可能会使您的公共界面混乱，并泄漏用户不需要了解或可能依赖的实现细节。有关更多详细信息，请参见[Testing]（测试）部分。

 
### Accepting/Returning dynamic Types  接受/返回动态类型Dart provides a dynamic type which the compiler will allow any type to be passed to a function and returned from a function. This can be useful in some situations like json encoding/decoding but in the general case it should be avoided. Using dynamic types prevents the compiler from performing static type checking at compile time and introduces hard to debug run-time errors.   Dart提供了一种动态类型，编译器将允许将任何类型传递给函数并从函数返回。在某些情况下，例如json编码/解码，这可能很有用，但在一般情况下，应避免使用。使用动态类型会阻止编译器在编译时执行静态类型检查，并引入难以调试的运行时错误。

In situations where an API might need to accept/return multiple input types consider using generics or defining an interface which the object implements instead. In situations where this will not work, consider defining multiple methods which call through to the private dynamic accepting function.  在API可能需要接受/返回多种输入类型的情况下，请考虑使用泛型或定义由对象实现的接口。在无法解决此问题的情况下，请考虑定义调用私有动态接受函数的多个方法。

 
### Using Private Methods Across Files  在文件之间使用私有方法Dart distinguishes private members from public members by prefixing them with the underscore. This creates isolation between files reduces coupling. This can be overridden by using the `part of` directive at the top of a file. This directive has the effect of combining multiple files and allowing them to access each others private members. Doing this makes it hard to rationalize about what is public and what is private and creates tight coupling between classes. Rather than using this directive, it is recommended to only interact with another object via its public interfaces. If classes must interact via private interfaces it is recommended to keep them in the same file to clearly indicate their relationship.  Dart会在私人成员和公共成员之间加上下划线，以区分他们。这在文件之间创建了隔离，减少了耦合。可以通过使用文件顶部的`part of`指令来覆盖它。该指令的作用是合并多个文件，并允许它们访问彼此的私有成员。这样做使得很难合理化什么是公共的和什么是私有的，并导致类之间的紧密耦合。建议不要通过该对象的公共接口与另一个对象进行交互，而不要使用此指令。如果类必须通过专用接口进行交互，建议将它们保留在同一文件中以清楚表明它们之间的关系。

 
### Global Static Variables  全局静态变量Global static variables can be useful in sharing state across a library but they can easily introduce race conditions and hard to debug code. Global variables can also be accessed by users of your library which may introduce unexpected side effects. It is strongly recommended that you avoid global static variables in public libraries.   全局静态变量对于在库中共享状态很有用，但是它们很容易引入竞争条件并且难以调试代码。库用户也可以访问全局变量，这可能会导致意外的副作用。强烈建议您避免在公共库中使用全局静态变量。

If there is a reason that your package does need to use a global static variable it is recommended to use zone-local static variables instead to isolate the variable from users of your library.  如果出于某种原因您的软件包确实需要使用全局静态变量，则建议使用区域局部静态变量，而不是将变量与库用户隔离。

```
void startComputation() {
  runZoned(() async {
    await collectScores(getValues());
    print('Scores: ${Zone.current[#scores]}');
  }, zoneValues: {#scores: <int>[]});
}

Future<void> collectScores(Stream<int> scores) async {
  await for (int value in scores) {
    Zone.current[#scores].add(value);
  }
}

// scores will not be affected by the call to startComputation.
final scores = <int>[1, 2, 3];

void main() {
  startComputation();
}
```
