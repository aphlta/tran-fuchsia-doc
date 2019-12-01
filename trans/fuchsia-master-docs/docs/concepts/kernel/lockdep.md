 
# Runtime Lock Validation in Zircon  Zircon中的运行时锁定验证 

 
## Introduction  介绍 

Zircon integrates a runtime lock validator to diagnose inconsistent lock ordering that could lead to deadlocks. This document discusses how thevalidator is integrated, how to enable and tune the validator at build time,and what output the validator produces. Zircon集成了运行时锁验证器，以诊断可能导致死锁的不一致的锁顺序。本文档讨论了验证器如何集成，如何在构建时启用和调整验证器以及验证器产生什么输出。

The theory of operation for the validator itself can be found in the [design document](lockdep-design.md). 验证程序本身的工作原理可以在[设计文档]（lockdep-design.md）中找到。

 
## Enabling the Lock Validator  启用锁定验证器 

Lock validation is disabled by default. **When disabled the lock instrumentation is transparent, acting as a zero-overhead wrapper for the underlying lockingprimitives**. 默认情况下禁用锁验证。 **禁用时，锁定工具是透明的，充当基础锁定基元的零开销包装器**。

The validator is enabled at compile time by setting the GN build argument `enable_lock_dep` to true. As of this writing logic for this variable ishandled by [kernel/BUILD.gn](/zircon/kernel/BUILD.gn). 通过将GN构建参数`enable_lock_dep'设置为true，可以在编译时启用验证器。截至本文撰写时，此变量的逻辑由[kernel / BUILD.gn]（/ zircon / kernel / BUILD.gn）处理。

You can set this variable in your GN invocation like this:  您可以像这样在GN调用中设置此变量：

```
fx set <your build options> --args 'zircon_extra_args = { enable_lock_dep = true }'
```
 

When the lock validator is enabled a set of global lock-free, wait-free data structures are generated to track the relationships between the instrumentedlocks. The acquire/release operations of the locks are augmented to updatethese data structures. 启用锁验证器后，将生成一组全局无锁，无等待的数据结构，以跟踪已检测的锁之间的关系。锁的获取/释放操作得到了增强，以更新这些数据结构。

 
## Lock Instrumentation  锁具 

The current incarnation of the runtime lock validator requires manually instrumenting each lock in kernel with a wrapper type. The wrapper type providesthe context the validator needs to properly identify the lock and generate aglobal tracking structure for locks with the same context or role. 运行时锁验证器的当前形式要求使用包装类型手动检测内核中的每个锁。包装器类型提供了验证者正确识别锁并为具有相同上下文或角色的锁生成全局跟踪结构所需的上下文。

The kernel defines utility macros for this purpose in `kernel/spinlock.h` and `kernel/mutex.h`. 内核为此在`kernel / spinlock.h`和`kernel / mutex.h`中定义了工具宏。

 
### Member Locks  会员锁 

A type with a lock member like this:  具有锁定成员的类型，如下所示：

```C++
#include <kernel/mutex.h>

class MyType {
public:
	// ...
private:
	mutable fbl::Mutex lock_;
	// ...
};
```
 

May be instrumented like this:  可以这样检测：

```C++
#include <kernel/mutex.h>

class MyType {
public:
	// ...
private:
	mutable DECLARE_MUTEX(MyType) lock_;
	// ...
};
```
 

Note that the containing type is passed to the macro `DECLARE_MUTEX(containing_type)`. This type provides the context the validatorneeds to distinguish locks that are members of `MyType` from locks that aremembers of other types. 注意，包含类型被传递给宏`DECLARE_MUTEX（containing_type）`。这种类型提供了验证器需要的上下文，以区分作为MyType成员的锁与作为其他类型成员的锁。

The macro `DECLARE_SPINLOCK(containing_type)` provides similar support for instrumenting `SpinLock` members. 宏`DECLARE_SPINLOCK（contains_type）`为检测`SpinLock`成员提供了类似的支持。

For those who are curious, the macro in the example above expands to this type expression: `::lockdep::LockDep<containing_type, fbl::Mutex, __LINE__>`. Thisexpression results in a unique instantiation of the `lockdep::LockDep<>` type,both across different containing types, and within a containing type wherethere is more than one mutex. 对于那些好奇的人，上面示例中的宏扩展为以下类型表达式：`:: lockdep :: LockDep <contains_type，fbl :: Mutex，__LINE __>`。这个表达式会导致一个`lockdep :: LockDep <>`类型的唯一实例化，既跨越不同的包含类型，又包含一个以上互斥量的包含类型。

 
### Global Locks  全局锁 

Global locks are instrumented using a singleton-type pattern. The kernel defines utility macros for this purpose in `kernel/mutex.h` and `kernel/spinlock.h`. 全局锁使用单例类型的模式进行检测。内核为此在`kernel / mutex.h`和`kernel / spinlock.h`中定义了实用程序宏。

In Zircon global locks are typically defined either at global/namespace scope or within another type as a static member. 在Zircon中，全局锁通常在全局/命名空间范围内或在另一种类型内定义为静态成员。

example.h:  example.h：

```C++
#include <kernel/mutex.h>

extern fbl::Mutex a_global_lock;

class MyType {
public:
	// ...
private:
	static fbl::Mutex all_objects_lock_;
};
```
 

example.cpp:  example.cpp：

```C++
#include "example.h"

fbl::Mutex a_global_lock;

fbl::Mutex MyType::all_objects_lock_;
```
 

The instrumentation simplifies declaring locks by declaring singleton types that may be used in either scope and handles ODR-use automatically. 该工具通过声明可以在任一范围内使用的单例类型来简化声明锁，并自动处理ODR使用。

example.h:  example.h：

```
#include <kernel/mutex.h>

DECLARE_SINGLETON_MUTEX(AGlobalLock);

class MyType {
public:
	// ...
private:
	DECLARE_SINGLETON_MUTEX(AllObjectsLock);
};
```
 

These macro invocations declare new singleton types, `AGlobalLock` and `MyType::AllObjectsLock` respectively. These types have a static `Get()` methodthat returns the underlying global lock with all of the necessaryinstrumentation. Note that there is no need to separately define storage for thelocks, this is handled automatically by the supporting template types. 这些宏调用分别声明了新的单例类型，分别为AGlobalLock和MyType :: AllObjectsLock。这些类型都有一个静态的Get（）方法，该方法返回具有所有必要工具的基础全局锁。请注意，无需单独定义锁的存储，这由支持模板类型自动处理。

The macro `DECLARE_SINGLETON_SPINLOCK(name)` provides similar support for declaring a global `SpinLock`. 宏`DECLARE_SINGLETON_SPINLOCK（name）`为声明全局`SpinLock`提供了类似的支持。

 
### Lock Guards  锁卫 

Instrumented locks are acquired and released using the scoped capability types `Guard` and `GuardMultiple`. In the kernel these types are defined in`kernel/lockdep.h`. 使用锁定的功能类型“ Guard”和“ GuardMultiple”来获取和释放已检测的锁。在内核中，这些类型在`kernel / lockdep.h`中定义。

The operation of `Guard` for simple mutexes is similar to `AutoLock`:  简单互斥的Guard的操作类似于AutoLock：

```C++
#include <kernel/mutex.h>

class MyType {
public:
	// ...

	int GetData() const {
		Guard<fbl::Mutex> guard{&lock_};
		return data_;
	}

	int DoSomething() {
		Guard<fbl::Mutex> guard{&lock_};
		int data_copy = data_;
		guard.Release();

		return DoWorkUnlocked(data_copy);
	}

private:
	mutable DECLARE_MUTEX(MyType) lock_;
	int data_{0} TA_GUARDED(lock_);
};
```
 

`SpinLock` types require an additional template argument to `Guard` to select one of a few possible options when acquiring the lock: `IrqSave`, `NoIrqSave`,and `TryLockNoIrqSave`. Omitting one of these type tags results in acompile-time error. “ SpinLock”类型需要“ Guard”的附加模板参数，以在获取锁时选择一些可能的选项之一：“ IrqSave”，“ NoIrqSave”和“ TryLockNoIrqSave”。忽略这些类型标签之一会导致编译时错误。

```C++
#include <kernel/spinlock.h>

class MyType {
public:
	// ...

	int GetData() const {
		Guard<SpinLock, IrqSave> guard{&lock_};
		return data_;
	}

	void DoSomethingInIrqContext() {
		Guard<SpinLock, NoIrqSave> guard{&lock_};
		// ...
	}

	bool TryToDoSomethingInIrqContext() {
		if (Guard<SpinLock, TryLockNoIrqSave> guard{&lock_}) {
			// ...
			return true;
		}
		return false;
	}

private:
	mutable DECLARE_SPINLOCK(MyType) lock_;
	int data_{0} TA_GUARDED(lock_);
};
```
 

Instrumented global locks work similarly:  检测到的全局锁的工作方式类似：

```C++
#include <kernel/mutex.h>
#include <fbl/intrusive_double_list.h>

class MyType : public fbl::DoublyLinkedListable<MyType> {
public:
	// ...

	void AddToList(MyType* object) {
		Guard<fbl::Mutex> guard{AllObjectsLock::Get()};
		all_objects_list_.push_back(*object);
	}

private:
	DECLARE_SINGLETON_MUTEX(AllObjectsLock);
	fbl::DoublyLinkedList<MyType> all_objects_list_ TA_GUARDED(AllObjectsLock::Get());
};
```
 

Note that instrumented locks do not have manual `Acquire()` and `Release()` methods; using a `Guard` is the only way to acquire the locks directly. Thereare two important reasons for this: 注意，插装的锁没有手动的`Acquire（）`和`Release（）`方法。使用`Guard'是直接获取锁的唯一方法。有两个重要原因：

 
1. Manual acquire/release operations are more error prone than guard, plus manual release when necessary. 1.手动获取/释放操作比后卫更容易出错，必要时还要加上手动释放。
2. When lock validation is enabled the guard provides the storage that the validator uses to account for actively held locks. This approach permitstemporary storage of validator state on the stack only for the duration thelock is held, which corresponds with the use patterns of guard objects.Without this approach the tracking data would either have to be stored witheach lock instance, increasing memory use even when locks are not held, orstored in heap allocated memory. Neither of these alternatives is desirable. 2.启用锁验证后，警卫队将提供验证者用来说明有效持有的锁的存储。这种方法只允许在持有锁的持续时间内将验证器状态临时存储在堆栈上，这与保护对象的使用模式相对应。没有这种方法，跟踪数据要么必须与每个锁实例一起存储，要么即使在锁时也要增加内存使用量不保留或存储在堆分配的内存中。这些选择都不是理想的。

In rare circumstances the underlying lock may be accessed using the `lock()` accessor of the instrumented lock. This should be done with care as manipulatingthe underlying lock directly may result inconsistency between the state of thelock and the state the lock validator; at best this may lead to missing a lockorder warning and at worst may lead to a deadlock. **You have been warned!** 在极少数情况下，可以使用检测到的锁的“ lock（）”访问器来访问基础锁。应当谨慎执行此操作，因为直接操作基础锁可能会导致锁状态与锁验证程序的状态不一致。充其量这可能会导致缺少锁定命令警告，而最坏的情况可能会导致死锁。 **你被警告了！**

 
## Clang Static Analysis and Instrumented Locks  lang静态分析和仪表锁 

The lock instrumentation is designed to interoperate with Clang static lock analysis. In general usage, an instrumented lock may be used as a "mutex"capability and specified in any of the static lock annotations. 锁定工具旨在与Clang静态锁定分析进行互操作。在一般用法中，检测到的锁可以用作“互斥”功能，并且可以在任何静态锁注释中指定。

There are two special cases that need some extra attention:  有两种特殊情况需要特别注意：

 
1. Returning pointers or references to capabilities.  1.返回功能的指针或引用。
2. Unlocking a guard passed by reference.  2.解锁通过引用传递的警卫。

 
### Pointers and References to Capabilities  能力的指针和参考 

When returning a lock by pointer or reference it may be convenient or necessary to use a uniform type. Recall from earlier that instrumented locks are wrappedin a type that captures the containing type, the underlying lock type, and theline number to disambiguate locks belonging to different types(`::lockdep::LockDep<Class, Locktype, Index>`). This can lead to difficulty whenreturning a lock from a uniform (virtual) interface (e.g. kernel`Dispatcher::get_lock()`). 通过指针或引用返回锁时，使用统一类型可能很方便或有必要。回想一下以前，已检测到的锁被包装为捕获包含类型，基础锁类型和行号的类型，以消除属于不同类型的锁的歧义（`:: lockdep :: LockDep <Class，Locktype，Index>`）。从统一（虚拟）接口返回锁时可能会导致困难（例如kernel`Dispatcher :: get_lock（）`）。

Fortunately there is a straightforward solution: every instrumented lock is also a subclass of `::lockdep::Lock<LockType>` (or simply `Lock<LockType>` in thekernel). This type only depends on the underlying `LockType`, not the context inwhich the instrumented lock is declared, making it convenient to use as apointer or reference type to refer to an instrumented lock more generically.This type may be used in type annotations as well. 幸运的是，有一个简单的解决方案：每个插入的锁也是`:: lockdep :: Lock <LockType>的子类（或者在内核中只是`Lock <LockType>`）。该类型仅取决于底层的LockType，而不依赖于声明已检测到的锁的上下文，从而可以更方便地用作指针或引用类型来更通用地引用已检测到的锁。此类型也可以在类型注释中使用。 。

The following illustrates the pattern, which is similar to that employed by the kernel `Dispatcher` types. 下面说明了这种模式，它与内核“ Dispatcher”类型所采用的模式相似。

```C++
#include <kernel/mutex.h>


struct LockableInterface {
	virtual ~LockableInterface() {}
	virtual Lock<fbl::Mutex>* get_lock() = 0;
	virtual void DoSomethingLocked() TA_REQ(get_lock()) = 0;
};

class A : public LockableInterface {
public:
	Lock<fbl::Mutex>* get_lock() override { return &lock_; }
	void DoSomethingLocked() override {
		data_++;
	}
	void DoSomething() {
		Guard<fbl::Mutex> guard{get_lock()};
		DoSomethingLocked();
		// ...
	}
private:
	mutable DECLARE_MUTEX(A) lock_;
	int data_ TA_GUARDED(get_lock());
};

class B : public LockableInterface {
public:
	Lock<fbl::Mutex>* get_lock() override { return &lock_; }
	void DoSomethingLocked() override {
		// ...
	}
	void DoSomething() {
		Guard<fbl::Mutex> guard{get_lock()};
		DoSomethingLocked();
		// ...
	}
private:
	mutable DECLARE_MUTEX(B) lock_;
	char data_[32] TA_GUARDED(get_lock());
};
```
 

Note that the type of `A::lock_` is `::lockdep::LockDep<A, fbl::Mutex, __LINE__>` and the type of `B::lock_` is`::lockdep::LockDep<B, fbl::Mutex, __LINE__>`. However, both of these types aresubclasses of `Lock<fbl::Mutex>`, so we can treat them uniformly as this type inpointer and reference expressions. 注意，A :: lock_的类型是::: lockdep :: LockDep <A，fbl :: Mutex，__LINE __>`，B :: lock_的类型是::: lockdep :: LockDep <B ，fbl :: Mutex，__LINE __>`。但是，这两种类型都是`Lock <fbl :: Mutex>`的子类，因此我们可以将它们统一视为此类型的指针和引用表达式。

While this is very convenient, a limitation in Clang static analysis prevents it from understanding that `LockableInterface::get_lock()` is equivalent to`A::lock_` or `B::lock_`, even in their local contexts. For this reason is itnecessary to use `get_lock()` in all of the lock annotations. 尽管这很方便，但是Clang静态分析的局限性使其无法理解LockableInterface :: get_lock（）等同于A :: lock_或B :: lock_，即使在它们的本地上下文中也是如此。因此，必须在所有锁注释中使用`get_lock（）`。

 
### Unlocking a Guard Passed by Reference  解锁通过引用传递的警卫 

In very rare circumstances it is useful to release a `Guard` instance held in a function from a callee of the function. 在极少数情况下，从函数的被调用者释放函数中保存的`Guard'实例非常有用。

**TODO(eieio): Complete documentation of this feature.**  ** TODO（eieio）：此功能的完整文档。**

 
## Lock Validation Errors  锁验证错误 

The lock validator detects and reports two broad classes of violations:  锁验证器检测并报告两大类违规：

 
1. Pair-wise violations reported at the point of acquisition.  1.在获取时报告成对违反。
2. Multi-lock cycles reported asynchronously by a dedicated loop detection thread. 2.专用环路检测线程异步报告多锁周期。

 
### Violations Reported at Acquisition  发生收购时举报的违规行为 

When a violation is detected at the point of lock acquisition the validator produces a message like the following in the kernel log: 在获取锁的时刻检测到违规时，验证器会在内核日志中生成类似以下的消息：

{# Disable variable substition to avoid {{ being interpreted by the template engine #} {% verbatim %} {禁用变量替换以避免{{被模板引擎解释} {逐字％}

```
[00002.668] 01032:01039> ZIRCON KERNEL OOPS
[00002.668] 01032:01039> Lock validation failed for thread 0xffff000001e53598 pid 1032 tid 1039 (userboot:userboot):
[00002.668] 01032:01039> Reason: Out Of Order
[00002.668] 01032:01039> Bad lock: name=lockdep::LockClass<SoloDispatcher<ThreadDispatcher, 316111>, Mutex, 282, (lockdep::LockFlags)0> order=0
[00002.668] 01032:01039> Conflict: name=lockdep::LockClass<SoloDispatcher<ProcessDispatcher, 447439>, Mutex, 282, (lockdep::LockFlags)0> order=0
[00002.668] 01032:01039> {{{module:0:kernel:elf:0bf16acb54de1ceef7ffb6ee4449c6aafc0ab392}}}
[00002.668] 01032:01039> {{{mmap:0xffffffff10000000:0x1ae1f0:load:0:rx:0xffffffff00000000}}}
[00002.668] 01032:01039> {{{mmap:0xffffffff101af000:0x49000:load:0:r:0xffffffff001af000}}}
[00002.668] 01032:01039> {{{mmap:0xffffffff101f8000:0x1dc8:load:0:rw:0xffffffff001f8000}}}
[00002.668] 01032:01039> {{{mmap:0xffffffff10200000:0x76000:load:0:rw:0xffffffff00200000}}}
[00002.668] 01032:01039> {{{bt:0:0xffffffff10088574}}}
[00002.668] 01032:01039> {{{bt:1:0xffffffff1008f324}}}
[00002.668] 01032:01039> {{{bt:2:0xffffffff10162860}}}
[00002.668] 01032:01039> {{{bt:3:0xffffffff101711e0}}}
[00002.668] 01032:01039> {{{bt:4:0xffffffff100edae0}}}
```
 

{# Re-enable variable substition #} {% endverbatim %} {重新启用变量替换} {％和逐字％}

The error is informational and non-fatal. The first line identifies the thread and process where the kernel lock violation occurred. The next line identifiesthe type of violation. The next two lines identify which locks were found to beinconsistent with previous observations: the "Bad lock" is the lock that isabout to be acquired, while "Conflict" is a lock that is already held by thecurrent context and is the point of inconsistency with the lock that is about tobe acquired. All of the lines following this are part of the stack trace leadingup to the bad lock. 该错误是信息性的，不是致命的。第一行标识发生内核锁冲突的线程和进程。下一行标识违规的类型。接下来的两行标识发现哪些锁与先前的观察结果不一致：“坏锁”是即将获取的锁，而“冲突”是当前上下文已经持有的锁，并且是与之不一致的地方。将要获得的锁。此后的所有行都是导致错误锁的堆栈跟踪的一部分。

 
### Multi-Lock Cycles  多锁循环 

Circular dependencies between three or more locks are detected with a dedicated loop detection thread. Because this detection happens in a separate context fromthe lock operations that caused the cycle a stack trace is not provided. 使用专用的循环检测线程来检测三个或更多锁之间的循环依赖关系。因为此检测发生在与导致周期的锁定操作不同的上下文中，所以未提供堆栈跟踪。

Reports from the loop detection thread look like this:  来自循环检测线程的报告如下所示：

```
[00002.000] 00000.00000> ZIRCON KERNEL OOPS
[00002.000] 00000.00000> Circular lock dependency detected:
[00002.000] 00000.00000>   lockdep::LockClass<VmObject, fbl::Mutex, 249, (lockdep::LockFlags)0>
[00002.000] 00000.00000>   lockdep::LockClass<VmAspace, fbl::Mutex, 198, (lockdep::LockFlags)0>
[00002.000] 00000.00000>   lockdep::LockClass<SoloDispatcher<VmObjectDispatcher>, fbl::Mutex, 362, (lockdep::LockFlags)0>
[00002.000] 00000.00000>   lockdep::LockClass<SoloDispatcher<PortDispatcher>, fbl::Mutex, 362, (lockdep::LockFlags)0>
```
 

Each of the locks involved in the cycle are reported in a group. Frequently only two of the circularly-dependent locks are acquired by a single thread at anygiven time, making manual detection difficult or impossible. However, thepotential for deadlock between three or more threads is real and should beaddressed for long-term system stability. 循环中涉及的每个锁都在一个组中报告。在任何给定时间，单个线程通常仅获取两个依赖于循环的锁，这使得手动检测变得困难或不可能。但是，三个或更多线程之间发生死锁的可能性是真实的，应该解决这个问题，以确保长期的系统稳定性。

 
## Kernel Commands  内核命令 

When the lock validator is enabled the following kernel commands are available:  启用锁验证器后，以下内核命令可用：

 
* `k lockdep dump` - dumps the dependency graph and connected sets (loops) for all instrumented locks. *`k lockdep dump`-转储所有检测到的锁的依赖关系图和连接集（循环）。
