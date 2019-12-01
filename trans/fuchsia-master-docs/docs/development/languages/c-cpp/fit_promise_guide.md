 
# `fit::promise<>` User Guide  fit :: promise <>用户指南 

Welcome! You probably dislike writing code in C++ that describes multi-step asynchronous operations. 欢迎！您可能不喜欢用C ++编写描述多步异步操作的代码。

`fit::promise<>` [[1](/zircon/system/ulib/fit/include/lib/fit/promise.h)]makes this a bit easier. This guide covers common problems in asynchronouscontrol flow programming and offers common usage patterns which solve thoseproblems in the `fit::promise<>` library. fit :: promise <>`[[1]（/ zircon / system / ulib / fit / include / lib / fit / promise.h）]使此操作变得容易一些。本指南介绍了异步控制流编程中的常见问题，并提供了一些常见的使用模式，这些模式可以解决`fit :: promise <>`库中的问题。

 
## What makes asynchronous code challenging?  是什么使异步代码具有挑战性？ 

Within the `fit::promise<>` library an asynchronous task is defined as one that is made up of multiple *synchronous* blocks of code with explicit suspendpoints. 在`fit :: promise <>`库中，一个异步任务定义为一个任务，该任务由多个*同步*代码块以及显式的暂停点组成。

When defining an asynchronous task, there must be solutions for the following problems: 定义异步任务时，必须有以下问题的解决方案：

 
1. **Expressing the flow of control**: how is the *sequence* of synchronous blocks and how data flows between them expressed? How is this done in anunderstandable way? 1.“表达控制流”：同步块的“序列”如何表达以及它们之间的数据流如何表达？如何以一种易于理解的方式完成此操作？

 
2. **Management of state & resources**: what intermediate state is needed to support task execution, and what external resources must be captured? How isthis expressed and how is it done safely? 2. **状态资源的管理**：支持任务执行需要什么中间状态？必须捕获哪些外部资源？这是如何表达的，如何安全地进行？

 
## Terminology  术语 
* `fit::promise<>` is a move-only object made up of a collection of lambdas or callbacks that describes an asynchronous task which eventually produces avalue or an error. *`fit :: promise <>`是仅移动对象，由lambda或回调的集合组成，描述了最终会产生值或错误的异步任务。
* a *handler function* is a callback provided at promise creation.  *处理函数*是在诺言创建时提供的回调。
* a *continuation function* is a callback provided to various *methods of continuation* on an existing promise. *连续函数*是根据现有诺言提供给各种“连续方法”的回调。
* a `fit::executor` is responsible for scheduling and executing promises. Promises do not run until their ownership has been transferred to a`fit::executor`. At this point the executor is responsible for its schedulingand execution. * fit :: executor负责安排和执行Promise。在将其所有权转移到fit :: executor之前，承诺不会运行。在这一点上，执行者负责其调度和执行。
* `fit::context` is optionally passed to handler and continuation functions to gain access to the `fit::executor` and to low-level suspend and resumecontrols. *可以将`fit :: context`传递给处理函数和延续函数，以获得对`fit :: executor`以及低级暂停和恢复控制的访问。

 
## Building & executing your first `fit::promise<>`  执行第一个`fit :: promise <>的构建 

Let's write a simple promise.  让我们写一个简单的承诺。

```cpp
#include <lib/fit/promise.h>

...
fit::promise<> p = fit::make_promise([] {
  // This is a handler function.

  auto world_is_flat = AssessIfWorldIsFlat();
  if (world_is_flat) {
    return fit::error();
  }
  return fit::ok();
});
```
 

`p` now contains a promise that describes a simple task.  现在，“ p”包含一个描述简单任务的承诺。

In order to run the promise, it must be scheduled it on an implementation of `fit::executor`. The most commonly used executor is an `async::Executor`[[2](/zircon/system/ulib/async/include/lib/async/cpp/executor.h)]which schedules callbacks on an `async_dispatcher_t`. For the purposes oftesting and exploration, there is also `fit::single_threaded_executor` and itsassociated method `fit::run_single_threaded()`[[3](/zircon/system/ulib/fit/include/lib/fit/single_threaded_executor.h#72)]which is used here. 为了兑现承诺，必须将其安排在`fit :: executor`的实现上。最常用的执行器是`async :: Executor` [[2]（/ zircon / system / ulib / async / include / lib / async / cpp / executor.h）]，它在async_dispatcher_t上安排回调。出于测试和探索的目的，还有`fit :: single_threaded_executor`及其关联方法`fit :: run_single_threaded（）`[[3]（/ zircon / system / ulib / fit / include / lib / fit / single_threaded_executor.h72 ）]。

```cpp
// When a promise is scheduled, the `fit::executor` takes ownership of it.
fit::result<> result = fit::run_single_threaded(std::move(p));
assert(result.is_ok());
```
 

 
## Building a more complex `fit::promise<>`  构建更复杂的`fit :: promise <> 

 
### Return, error types & resolution states  返回，错误类型解析状态 

As mentioned above, the template arguments for `fit::promise<>` represent the return and error types: 如上所述，`fit :: promise <>`的模板参数代表返回和错误类型：

```cpp
fit::promise<ValueType, ErrorType>
```
 

The error type can be omitted and it will take the default error type of `void` (e.g. `fit::promise<MyValueType>` is equivalent to `fit::promise<MyValueType,void>`). 错误类型可以省略，它将采用默认的错误类型“ void”（例如，fit :: promise <MyValueType>等同于fit :: promise <MyValueType，void>）。

During execution, a promise must eventually reach one of the following states:  在执行期间，承诺必须最终达到以下状态之一：

 
* Success: the handler function or the last continuation function (see below) has returned `fit::ok()`. *成功：处理程序函数或最后一个延续函数（参见下文）已返回`fit :: ok（）`。
* Error: the handler function or some continuation function has returned `fit::error()`, *and* no subsequent continuation function has intercepted it. *错误：处理程序函数或某些延续函数已返回`fit :: error（）`，并且*且随后的延续函数均未对其进行拦截。
* Abandoned: the promise was destroyed before resolving to either Success or Error. *被遗弃：在解决成功或错误之前，承诺被破坏了。

 
### `.then()`, `.and_then()`, `.or_else()`: Chaining asynchronous blocks  .then（）、. and_then（）、. or_else（）：链接异步块 

Often complex tasks can be decomposed into smaller more granular tasks. Each of these tasks needs to be asynchronously executed, but if there is somedependency between the tasks, there is a need to preserve them. This can beachieved through different combinators, such as: 通常，复杂的任务可以分解为更小的，更精细的任务。这些任务中的每一个都需要异步执行，但是如果任务之间存在某种依赖性，则需要保留它们。这可以通过不同的组合器来实现，例如：

 
* `fit::promise::then()` becomes useful for defining task dependency, as execute task 1 then task 2, regardless of task 1's status. The prior task'sresult is received through an argument of type `fit::result<ValueType,ErrorType>&` or `const fit::result<ValueType, ErrorType>&`. *`fit :: promise :: then（）`对于定义任务依赖性非常有用，因为先执行任务1然后执行任务2，而不管任务1的状态如何。上一个任务的结果通过类型为fit :: result <ValueType，ErrorType>或const fit :: result <ValueType，ErrorType>的参数接收。

```cpp
auto execute_task_1_then_task_2 =
    fit::make_promise([]() -> fit::result<ValueType, ErrorType> {
      ...
    }).then([](fit::result<ValueType, ErrorType>& result) {
      if (result.is_ok()) {
        ...
      } else {  // result.is_error()
        ...
      }
    });
```
 

 
* `fit::promise::and_then()` becomes useful for defining task dependency only in the case of task 1's success. The prior task's result is received throughan argument of type `ValueType&` or `ValueType&`. *`fit :: promise :: and_then（）`仅在成功完成任务1的情况下才对定义任务依赖性有用。优先任务的结果是通过ValueType或ValueType类型的参数接收的。

```cpp
auto execute_task_1_then_task_2 =
    fit::make_promise([]() { ... }).and_then([](ValueType& success_value) {
      ...
    });
```
 

 
* `fit::promise::or_else()` becomes useful for defining task dependency only in the case of task 1's failure. The prior task's result is received through anargument of type `ErrorType&` or `const ErrorType&`. *`fit :: promise :: or_else（）`仅在任务1失败时才对定义任务依赖性有用。上一个任务的结果通过类型为ErrorType或const ErrorType的参数接收。

```cpp
auto execute_task_1_then_task_2 =
    fit::make_promise([]() { ... }).or_else([](ErrorType& failure_value) {
      ...
    });
```
 

 
### `fit::join_promises()` & `fit::join_promise_vector()`: Executing in parallel  fit :: join_promises（）`fit :: join_promise_vector（）：并行执行 

Sometimes, multiple promises can be executed with no dependencies between them, but the aggregate result is a dependency of the next asynchronous step. In thiscase, `fit::join_promises()` and `fit::join_promise_vector()` are used to joinon the results of multiple promises. 有时，可以在没有相互依赖关系的情况下执行多个promise，但是总的结果是下一个异步步骤的依赖关系。在这种情况下，`fit :: join_promises（）`和`fit :: join_promise_vector（）`用于合并多个promise的结果。

`fit::join_promises()` is used when each promise is referenced by a variable. `fit::join_promises()` supports heterogeneous promise types. The prior tasks'results are received through an argument of type `std::tuple<...>&` or `conststd::tuple<...>&`. 当变量引用每个promise时，使用fit :: join_promises（）。 fit :: join_promises（）支持异构诺言类型。先前任务的结果是通过类型为std :: tuple <...>或conststd :: tuple <...>的参数接收的。

```cpp
auto DoImportantThingsInParallel() {
  auto promise1 = FetchStringFromDbAsync("foo");
  auto promise2 = InitializeFrobinatorAsync();
  return fit::join_promises(std::move(promise1), std::move(promise2))
      .and_then([](std::tuple<fit::result<std::string>,
                              fit::result<Frobinator>>& results) {
        return fit::ok(std::get<0>(results).value() +
                       std::get<1>(results).value().GetFrobinatorSummary());
      });
}
```
 

`fit::join_promise_vector()` is used when the promises are stored in `std::vector<>`. This has the added constraint that all promises must behomogeneous (be of the same type). The prior tasks' results are receivedthrough an argument of type `std::vector<fit::result<ValueType, ErrorType>>&`or `const std::vector<fit::result<ValueType, ErrorType>>&`. 当promise存储在std :: vector <>中时，使用fit :: join_promise_vector（）。这就增加了约束，即所有的承诺必须是同质的（属于同一类型）。通过类型为std :: vector <fit :: result <ValueType，ErrorType >>或const std :: vector <fit :: result <ValueType，ErrorType >>的参数来接收先前任务的结果。

```cpp
auto ConcatenateImportantThingsDoneInParallel() {
  std::vector<fit::promise<std::string>> promises;
  promises.push_back(FetchStringFromDbAsync("foo"));
  promises.push_back(FetchStringFromDbAsync("bar"));
  return fit::join_promise_vector(std::move(promises))
      .and_then([](std::vector<fit::result<std::string>>& results) {
        return fit::ok(results[0].value() + "," + results[1].value());
      });
}
```
 

 
### `return fit::make_promise()`: Chaining or branching by returning new  return fit :: make_promise（）：通过返回新的链接或分支promises  诺言

It may become useful to defer the decision of which promises to chain together until runtime. This method is in contrast with chaining that is performedsyntactically (through the use of consecutive `.then()`, `.and_then()` and`.or_else()` calls). 推迟将哪个承诺链接在一起直到运行时的决定可能会很有用。该方法与语法上的链接相反（通过使用连续的.then（）、. and_then（）和.or_else（）调用）。

Instead of returning a `fit::result<...>` (using `fit::ok` or `fit::error`), the handler function may return a new promise which will be evaluated after thehandler function returns. 处理程序函数可以返回一个新的promise，而不是返回一个fit :: result <...>（使用fit :: ok或fit :: error），它会在handler函数返回后进行评估。

```cpp
fit::make_promise(...)
  .then([] (fit::result<>& result) {
    if (result.is_ok()) {
      return fit::make_promise(...); // Do work in success case.
    } else {
      return fit::make_promise(...); // Error case.
    }
  });
```
 

This pattern is also useful to decompose what could be a long promise into smaller readable chunks, such as by having a continuation function return theresult of `DoImportantThingsInParallel()` from the example above. 这种模式对于将长期承诺分解成较小的可读块也很有用，例如通过使用延续函数返回上面示例中的`DoImportantThingsInParallel（）`结果。

Note: See the gotcha "Handlers / continuation functions can return ..." below.  注意：请参见下面的陷阱“处理程序/延续函数可以返回...”。

 
### Declaring and keeping intermediate state alive  声明并保持中间状态有效 

Some tasks require state be kept alive only so long as the promise itself is either pending or executing. This state is not suited to be moved into anygiven lambda due to its need to be shared, nor is it appropriate to transferownership to a longer-lived container due to a desire for its lifecycle to becoupled to the promise. 某些任务要求状态仅在promise本身未完成或正在执行时才保持活动状态。由于需要共享此状态，因此不适合将其转移到任何给定的lambda中，由于希望将其生命周期与承诺挂钩，因此不适合将所有权转移到寿命更长的容器中。

Although not the only solution, usage of both `std::unique_ptr<>` and `std::shared_ptr<>` are common patterns: 尽管不是唯一的解决方案，但使用std :: unique_ptr <>和std :: shared_ptr <>都是常见的模式：

 
#### `std::unique_ptr<>`  `std :: unique_ptr <>` 

```cpp
fit::promise<> MakePromise() {
  struct State {
    int i;
  };
  // Create a single std::unique_ptr<> container for an instance of State and
  // capture raw pointers to the state in the handler and continuations.
  //
  // Ownership of the underlying memory is transferred to a lambda passed to
  // `.inspect()`. |state| will die when the returned promise is resolved or is
  // abandoned.
  auto state = std::make_unique<State>();
  state->i = 0;
  return fit::make_promise([state = state.get()] { state->i++; })
      .and_then([state = state.get()] { state->i--; })
      .inspect([state = std::move(state)](const fit::result<>&) {});
}
```
 

 
#### `std::shared_ptr<>`  `std :: shared_ptr <>` 

```cpp
fit::promise<> MakePromise() {
  struct State {
    int i;
  };
  // Rely on shared_ptr's reference counting to destroy |state| when it is safe
  // to do so.
  auto state = std::make_shared<State>();
  state->i = 0;
  return fit::make_promise([state] { state->i++; }).and_then([state] {
    state->i--;
  });
}
```
 

 
### `fit::scope`: Abandoning promises to avoid memory safety violations  fit :: scope`：放弃承诺以避免违反内存安全 

`fit::scope` becomes useful to tie the lifecycle of a `fit::promise<>` to a resource in memory. For example: fit :: scope`对于将fit :: promise <>的生命周期绑定到内存中的资源很有用。例如：

```cpp
#include <lib/fit/scope.h>

class A {
 public:
  fit::promise<> MakePromise() {
    // Capturing |this| is dangerous: the returned promise will be scheduled
    // and executed in an unknown context. Use |scope_| to protect against
    // possible memory safety violations.
    //
    // The call to `.wrap_with(scope_)` abandons the promise if |scope_| is
    // destroyed. Since |scope_| and |this| share the same lifecycle, it is safe
    // to capture |this|.
    return fit::make_promise([this] {
             // |foo_| is critical to the operation!
             return fit::ok(foo_.Frobinate());
           })
        .wrap_with(scope_);
  }

 private:
  Frobinator foo_;
  fit::scope scope_;
};

void main() {
  auto a = std::make_unique<A>();
  auto promise = a->MakePromise();
  a.reset();
  // |promise| will not run any more, even if scheduled, protected access to the
  // out-of-scope resources.
}
```
 

 
### `fit::sequencer`: Blocking a promise on a separate promise's completion  fit :: sequencer`：在单独的诺言完成时阻止诺言 

TODO: you can .wrap_with(sequencer) to block this promise on the completion of the last promise wrapped with the same sequencer object 待办事项：您可以使用.wrap_with（sequencer）在最后一个用相同音序器对象包装的承诺完成时阻止该承诺

```cpp
#include <lib/fit/sequencer.h>
// TODO
```
 

 
### `fit::bridge`: integrating with callback-based async functions  fit :: bridge`：与基于回调的异步函数集成 

TODO: fit::bridge is useful to chain continuation off a callback-based async function TODO：fit :: bridge对于链接基于回调的异步函数的连续性很有用

```cpp
#include <lib/fit/bridge.h>
// TODO
```
 

 
### `fit::bridge`: decoupling execution of a single chain of continuation  fit :: bridge`：解耦单个连续链的执行 

TODO: fit::bridge is also useful to decouple one chain of continuation into two promises that can be executed on different `fit::executor` instances TODO：fit :: bridge还可用于将一连串的连续性分解为两个可以在不同的`fit :: executor`实例上执行的promise

 
## Common gotchas  常见陷阱 

 
### Sequences of `and_then` or `or_else` must have compatible types  and_then`或`or_else`的序列必须具有兼容的类型 

When building promises using `and_then`, each successive continuation may have a different *ValueType* but must have the same *ErrorType* because `and_then`forwards prior errors without consuming them. 当使用`and_then`构建承诺时，每个连续的延续可能具有不同的* ValueType *，但必须具有相同的* ErrorType *，因为`and_then`会转发先前的错误而不消耗它们。

When building promises using `or_else`, each successive continuation may have a different *ErrorType* but must have the same *ValueType* because `or_else`forwards prior values without consuming them. 当使用`or_else`构建承诺时，每个连续的延续可能具有不同的* ErrorType *，但必须具有相同的* ValueType *，因为`or_else`会转发先前的值而不消耗它们。

To change types in the middle of the sequence, use `then` to consume the prior result and produce a new result of the desired type. 要在序列中间更改类型，请使用'then'消耗先前的结果并生成所需类型的新结果。

The following example does not compile because the error type returned by the last `and_then` handler is incompatible with the prior handler's result. 以下示例无法编译，因为最后一个`and_then`处理程序返回的错误类型与先前处理程序的结果不兼容。

```cpp
auto a = fit::make_promise([] {
  // returns fit::result<int, void>
  return fit::ok(4);
}).and_then([] (const int& value) {
  // returns fit::result<float, void>
  return fit::ok(value * 2.2f);
}).and_then([] (const float& value) {
  // ERROR!  Prior result had "void" error type but this handler returns const
  // char*.
  if (value >= 0)
    return fit::ok(value);
  return fit::error("bad value");
}
```
 

Use `then` to consume the result and change its type:  使用`then`使用结果并更改其类型：

```cpp
auto a = fit::make_promise([] {
  // returns fit::result<int, void>
  return fit::ok(4);
}).and_then([] (const int& value) {
  // returns fit::result<float, void>
  return fit::ok(value * 2.2f);
}).then([] (const fit::result<float>& result) -> fit::result<float, const char*> {
  if (result.is_ok() && result.value() >= 0)
    return fit::ok(value);
  return fit::error("bad value");
}
```
 

 
### Handlers / continuation functions can return `fit::result<>` or a new `fit::promise<>`, not both  处理程序/延续函数可以返回`fit :: result <>`或新的`fit :: promise <>`，不能两者都返回 

You may wish to write a handler which return a `fit::promise<>` in one conditional branch and a `fit::ok()` or `fit::error()` in another. This isillegal because there is no way for the compiler to cast a `fit::result<>` to a`fit::promise<>`. 您可能希望编写一个处理程序，该处理程序在一个条件分支中返回“ fit :: promise <>”，在另一个条件分支中返回“ fit :: ok（）”或“ fit :: error（）”。这是非法的，因为编译器无法将`fit :: result <>`强制转换为`fit :: promise <>`。

The workaround is to return a `fit::promise<>` that resolves to the result you want: 解决方法是返回一个`fit :: promise <>`来解析为您想要的结果：

```cpp
auto a = fit::make_promise([] {
  if (condition) {
    return MakeComplexPromise();
  }
  return fit::make_ok_promise(42);
});
```
 

 
### Continuation signatures  延续签名 

Have you seen an error message like this?  您是否看到过这样的错误消息？

```
../../zircon/system/ulib/fit/include/lib/fit/promise_internal.h:342:5: error: static_assert failed "The provided handler's last argument was expected to be of type V& or const V& where V is the prior result's value type and E is the prior result's error type.  Please refer to the combinator's documentation for
 a list of supported handler function signatures."
```
 

or:  要么：

```
../../zircon/system/ulib/fit/include/lib/fit/promise.h:288:5: error: static_assert failed due to requirement '::fit::internal::is_continuation<fit::internal::and_then_continuation<fit::promise_impl<fit::function_impl<16, false, fit::result<fuchsia::modular::storymodel::StoryModel, void> (fit::context &)> >, (lambda at ../../src/modular/bin/sessionmgr/story/model/ledger_story_model_storage.cc:222:17)>, void>::value' "Continuation type is invalid.  A continuation is a callable object with this signature: fit::result<V, E>(fit::context&)."
```
 

This most likely means that one of the continuation functions has a signature that isn't valid. The valid signatures for different continuation functions areshown below: 这很可能意味着延续功能之一具有无效的签名。不同的延续功能的有效签名如下所示：

For `.then()`:  对于`.then（）`：

```cpp
.then([] (fit::result<V, E>& result) {});
.then([] (const fit::result<V, E>& result) {});
.then([] (fit::context& c, fit::result<V, E>& result) {});
.then([] (fit::context& c, const fit::result<V, E>& result) {});
```
 

For `.and_then()`:  对于`.and_then（）`：

```cpp
.and_then([] (V& success_value) {});
.and_then([] (const V& success_value) {});
.and_then([] (fit::context& c, V& success_value) {});
.and_then([] (fit::context& c, const V& success_value) {});
```
 

For `.or_else()`:  对于`.or_else（）`：

```cpp
.or_else([] (E& error_value) {});
.or_else([] (const E& error_value) {});
.or_else([] (fit::context& c, E& error_value) {});
.or_else([] (fit::context& c, const E& error_value) {});
```
 

For `.inspect()`:  对于`.inspect（）`：

```cpp
.inspect([] (fit::result<V, E>& result) {});
.inspect([] (const fit::result<V, E>& result) {});
```
 

 
### Captures and Argument Lifecycle  捕获和参数生命周期 

Promises are composed of handler and continuation functions that are usually lambdas. Care must be taken when constructing lambda capture lists to avoidcapturing memory that is will not be valid when the handler or continuation inquestion executes. 承诺由通常为lambda的处理函数和延续函数组成。构造lambda捕获列表时必须小心，以免捕获在执行处理程序或继续查询时无效的内存。

For example, this promise captures memory that is guaranteed to be invalid by the time Foo() returns (and thus, when the returned promise is scheduled andexecuted). 例如，此承诺捕获在Foo（）返回时（因此，在计划并执行返回的承诺时）保证已保证无效的内存。

```cpp
fit::promise<> Foo() {
  int i;
  return fit::make_promise([&i] {
    i++;  // |i| is only valid within the scope of Foo().
  });
}
```
 

Instances in real code are more nuanced. A slightly less obvious example:  实际代码中的实例更加细致入微。一个不太明显的例子：

```cpp
fit::promise<> Foo() {
  return fit::make_promise(
      [i = 0] { return fit::make_promise([&i] { i++; }); });
}
```
 

`fit::promise` eagerly destroys handler and continuation functions: the outer-most handler will be destroyed once it returns the inner-most handler.See "Declaring and keeping intermediate state alive" above for the correctpattern to use in this case. fit :: promise急于破坏处理程序和延续函数：最外部的处理程序返回最内部的处理程序后将被破坏。有关在这种情况下使用的正确模式，请参见上面的“声明并保持中间状态有效”。

 
## >>> sections to write  >>>要写的部分 

 
* converting from one error type to another  *从一种错误类型转换为另一种错误类型
* fit::bridge  *适合::桥梁
