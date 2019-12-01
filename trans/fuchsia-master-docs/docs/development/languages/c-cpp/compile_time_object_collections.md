 
# Compile-Time Object Collections Discussion  编译时对象集合讨论 

This document covers active discussion about building compile-time collections of objects in C++. The following use cases are examples of where compile-timecollections are useful: 本文档涵盖有关在C ++中构建对象的编译时集合的积极讨论。以下用例是在编译时收集有用的示例：

 
* StringRef - A type that supports building a compile-time collection of string labels with associated unique numeric ids for tracing purposes. * StringRef-一种类型，它支持构建带有关联的唯一数字ID的字符串标签的编译时集合，以进行跟踪。
* LockClass - A type that supports building a compile-time collection of state objects for runtime lock validation purposes. LockClass-一种类型，支持出于运行时锁定验证目的而构建状态对象的编译时集合。

The following sections discuss common and unique requirements of each use case, the current challenges with the implementations, and proposed solutions. 以下各节讨论每个用例的共同和独特需求，实施中的当前挑战以及建议的解决方案。

 
## StringRef  字符串引用 

StringRef is a type that implements the concept of string references. A string reference is a mapping from a numeric id to a character string. Using themapping makes more economical use of the trace buffer: an (id, string)pair is emitted once in a tracing session and then subsequent events may referto the string by id instead of including the full character sequence inline. StringRef是一种实现字符串引用的概念的类型。字符串引用是从数字ID到字符串的映射。使用它们封装可以更经济地使用跟踪缓冲区：（id，字符串）对在跟踪会话中发出一次，然后随后的事件可以按id引用字符串，而不是内联完整的字符序列。

The following is a simple example of `StringRef` in action:  以下是运行中的StringRef的简单示例：

```C++
#include <lib/ktrace.h>

template <typename Op, typename... Args>
inline DoSomething(Op&& op, Args&&... args) {
    ktrace_probe(TraceAlways, TraceContext::Thread, "DoSomething"_stringref);
    // ...
}
```
 

Here the string literal operator `_stringref` returns an instance of `StringRef` that provides the facility to map the string "DoSomething" to a numeric idused by the tracing function. 这里，字符串文字运算符“ _stringref”返回“ StringRef”的实例，该实例提供了将字符串“ DoSomething”映射到跟踪函数所使用的数字的便利。

 
### Requirements  要求 

 
* Emit each (id, string) mapping at most once per tracing session, prior to any trace event that references the id. Ideally the full set of mappings isemitted at once at the start of a tracing session to avoid the overhead ofemitting mappings in the middle of timing sensitive code however, this is nota hard requirement. *在引用ID的任何跟踪事件之前，每个跟踪会话最多发出一次每个（ID，字符串）映射。理想情况下，在跟踪会话开始时立即发出完整的映射集，以避免在对时间敏感的代码中间发送映射的开销，但是，这并不是一个硬性要求。
* A dense id space is desirable so that down stream processing code can use a linear pre-allocated array or vector to implement the id-to-string lookup,however this is not a hard requirement. *需要一个密集的ID空间，以便下游处理代码可以使用线性预分配的数组或向量来实现ID到字符串的查找，但这并不是硬性要求。
* Some method to unique duplicate string references, since trace calls must be supported in template and inline functions and methods. *唯一重复字符串引用的某些方法，因为模板和内联函数和方法必须支持跟踪调用。

 
### Current Implementation  当前实施 

The following is an outline of the current `StringRef` implementation.  以下是当前`StringRef`实现的概述。

```C++
struct StringRef {
    static constexpr int kInvalidId = -1;

    const char* string{nullptr};
    ktl::atomic<int> id{kInvalidId};
    StringRef* next{nullptr};

    int GetId() {
        const int ref_id = id.load(ktl::memory_order_relaxed);
        return ref_id == kInvalidId ? Register(this) : ref_id;
    }

    // Returns the head of the global string ref linked list.
    static StringRef* head() { return head_.load(ktl::memory_order_acquire); }

private:
    // Registers a string ref in the global linked list.
    static int Register(StringRef* string_ref);

    static ktl::atomic<int> id_counter_;
    static ktl::atomic<StringRef*> head_;
};

// Returns an instance of StringRef that corresponds to the given string
// literal.
template <typename T, T... chars>
inline StringRef* operator""_stringref() {
    static const char storage[] = {chars..., '\0'};
    static StringRef string_ref{storage};
    return &string_ref;
}
```
 

 
## LockClass  锁类 

LockClass is a type that captures information about a lock that is common to all instances of the lock (e.g. its containing type if it is a struct/class member,the type of the underlying lock primitive, flags describing its behavior). TheLockClass type is used by the runtime lock validator to determine which orderingrules apply to each lock and to locate the per-lock-class tracking structureused to record ordering observations. LockClass是一种类型，它捕获有关该锁的所有实例通用的锁的信息（例如，如果它是struct / class成员，则包含它的类型，底层锁基元的类型，描述其行为的标志）。运行时锁验证器使用LockClass类型来确定将哪些排序规则应用于每个锁，并查找用于记录排序观察值的每个锁类跟踪结构。

The following is a simplified example of LockClass in action:  以下是LockClass的简化示例：

```C++
struct Foo {
    LockClass<Foo, fbl::Mutex> lock;
    // ...
};

struct Bar {
    LockClass<Bar, fbl::Mutex> lock;
};
```
 

 
### Requirements  要求 

 
* Ability to iterate the tracking state for all instantiations of LockClass, for cycle detection and error reporting purposes. *能够为LockClass的所有实例迭代跟踪状态，以进行周期检测和错误报告。
* Some method to unique duplicate tracking state, since instantiations of LockClass may be visible from multiple compilation units, depending on how thecontaining types (e.g. Foo and Bar) are used. *某种独特的重复跟踪状态的方法，因为LockClass的实例化可能在多个编译单元中可见，具体取决于如何使用包含的类型（例如Foo和Bar）。
* A dense id space is desirable so that down stream processing code can simplify id storage however, this is not a hard requirement. *需要一个密集的ID空间，以便下游处理代码可以简化ID存储，但这并不是硬性要求。

 
### Current Implementation  当前实施 

The following is a simplified implementation of LockClass:  以下是LockClass的简化实现：

```C++
template <typename ContainingType, typename LockType>
class LockClass {
    // ...
private:
    static LockClassState lock_class_state_;
};
```
 

Each instantiation of `LockClass` creates a unique instance of `LockClassState` to track the online lock order observations related to locks of class(`ContainingType`, `LockType`). The current implementation of `LockClassState`constructs a linked list of all instances in a global ctor to support theiteration requirement. LockClass的每个实例创建一个LockClassState的唯一实例，以跟踪与类锁（ContainingType，LockType）有关的在线锁定顺序观察。 LockClassState的当前实现在全局ctor中构造所有实例的链表，以支持迭代要求。

 
## Compile-Time Array Solution  编译时阵列解决方案 

One way to address the requirements of both types is to build a compile-time array of de-duplicated static instances, using COMDAT sections and groups. Thiscompletely removes the need to build linked lists of objects at init time orruntime and supports all of the requirements for each type. 解决这两种类型需求的一种方法是使用COMDAT节和组来构建经过重复数据删除的静态实例的编译时数组。这完全消除了在初始化时或运行时构建对象的链接列表的需要，并支持每种类型的所有要求。

For example:  例如：

```C++
// Defined in the linker script mark the beginning and end of the section:
// .data.lock_class_state_table.
extern "C" LockClassState __start_lock_class_state_table[];
extern "C" LockClassState __end_lock_class_state_table[];

template <typename ContainingType, typename LockClass>
class LockClass {
    // ...
private:
    static LockClassState lock_class_state_ __SECTION(".data.lock_class_state_table");
};

// Defined in the linker script to make the beginning and end of the section:
// .rodata.string_ref_table.
extern "C" StringRef __start_string_ref_table[];
extern "C" StirngRef __end_string_ref_table[];

struct StringRef {
    const char* const string;
    size_t GetId() const {
        return static_cast<size_t>(this - __start_string_ref_table);
    }
};

template <typename T, T... chars>
inline StringRef* operator""_stringref() {
    static const char storage[] = {chars..., '\0'};
    static StringRef string_ref __SECTION(".rodata.string_ref_table") {storage};
    return &string_ref;
}
```
 

