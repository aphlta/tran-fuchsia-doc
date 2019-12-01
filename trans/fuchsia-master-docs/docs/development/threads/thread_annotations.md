 
# Zircon thread safety annotations  锆石螺纹安全注释 

Zircon code takes advantage of clang's thread safety analysis feature to document and machine-verify some of our synchronization invariants. Theseannotations are checked when building for clang (see[getting started](/docs/development/kernel/getting_started.md) for instructions on building withclang). Zircon代码利用clang的线程安全分析功能来记录和机器验证我们的一些同步不变量。在构建clang时会检查这些注释（有关使用clang进行构建的说明，请参见[入门]（/ docs / development / kernel / getting_started.md））。

 
## How to use  如何使用 

[Clang's documentation](https://clang.llvm.org/docs/ThreadSafetyAnalysis.html)  [Clang的文档]（https://clang.llvm.org/docs/ThreadSafetyAnalysis.html）

In Zircon, we provide our own set of macros wrapping the annotations and have annotated our synchronization primitives. When writing new code involvingsynchronization or annotating existing code, in most cases you should use thethread annotation macros provided by[<lib/zircon-internal/thread\_annotations.h](/zircon/system/ulib/zircon-internal/include/lib/zircon-internal/thread_annotations.h).These macros all begin with the prefix `"TA_"` for thread analysis. The mostcommonly used ones are: 在Zircon中，我们提供了一组自己的宏，这些宏包装了注释并为同步原语添加了注释。在编写涉及同步或注释现有代码的新代码时，大多数情况下，应使用[<lib / zircon-internal / thread \ _annotations.h]（/ zircon / system / ulib / zircon-internal / include / lib提供的线程注释宏/zircon-internal/thread_annotations.h）。这些宏均以前缀“ TA_”开头，以进行线程分析。最常用的是：

 
* `TA_GUARDED(x)` the annotated variable is guarded by the capability (e.g. lock) `x`  * TA_GUARDED（x）带注释的变量由功能（例如锁）x保护。
* `TA_ACQ(x...)` function acquires all of the mutexes in the set `x` and hold them after returning  *`TA_ACQ（x ...）`函数获取集合`x`中的所有互斥锁并在返回后将其保留
* `TA_REL(x...)` function releases all of the mutexes in the set `x`  *`TA_REL（x ...）`函数释放集合x中的所有互斥量
* `TA_REQ(x...)` function requires that the caller hold all of the mutexes in the set `x`  *`TA_REQ（x ...）`函数要求调用者将集合x中的所有互斥锁都保存
* `TA_EXCL(x...)` function requires that the caller not be holding any of the mutexes in the set `x`  * TA_EXCL（x ...）函数要求调用者不持有集合x中的任何互斥量

For example, a class containing a member variable `'int foo_'` protected by a mutex would be annotated like so: 例如，一个包含由互斥量保护的成员变量''int foo_''的类将被注释为：

```
// example.h

class Example {
public:
    // Public function has no locking requirements and thus needs no annotation.
    int IncreaseFoo(int by);

private:
    // This is an internal helper routine that can only be called with |lock_|
    // held. Calling this without holding |lock_| is a compile-time error.
    // Annotations like TA_REQ, TA_ACQ, TA_REL, etc are part of the function's
    // interface and must be on the function declaration, usually in the header,
    // not the definition.
    int IncreaseFooLocked(int by) TA_REQ(lock_);

    // This internal routine requires that both |lock_| and |foo_lock_| be held by the
    // caller.
    int IncreaseFooAndBarLocked(int foo_by, int bar_by) TA_REQ(lock_) TA_REQ(bar_lock_);

    // The TA_GUARDED(lock_) annotation on |foo_| means that |lock_| must be
    // held to read or write from |foo_|.
    int foo_ TA_GUARDED(lock_);

    // |lock_| can be declared after annotations referencing it,
    // if desired.
    Mutex lock_;

    Mutex bar_lock_;
};

// example.cpp

int Example::IncreaseFoo(int by) {
    int new_value;
    {
        AutoLock lock(&lock_);  // fbl::AutoLock is annotated
        new_value = IncreaseFooLocked(by);
    }
    return new_value;
}
```
 

Note that for annotations which allow sets of mutex objects, one may either apply the annotation multiple times, or provided a comma separated list to theannotation.  In other words, the following two declarations are equivalent. 请注意，对于允许互斥对象集的注释，可以多次应用注释，也可以为注释提供逗号分隔的列表。换句话说，以下两个声明是等效的。

```
    int IncreaseFooAndBarLocked(int foo_by, int bar_by) TA_REQ(lock_) TA_REQ(bar_lock_);
    int IncreaseFooAndBarLocked(int foo_by, int bar_by) TA_REQ(lock_, bar_lock_);
```
 

Library code exposed through the sysroot must use the more awkwardly named macros provided by[system/public/zircon/compiler.h](/zircon/system/public/zircon/compiler.h) toavoid collisions with consumers of the sysroot. 通过sysroot公开的库代码必须使用[system / public / zircon / compiler.h]（/ zircon / system / public / zircon / compiler.h）提供的名称更笨拙的宏，以避免与sysroot使用者发生冲突。

 
## Best practices  最佳实践 

Annotations should complement the comments and identifiers to make the code understandable. Annotations do not replace comments or clear names. Try tofollow these best practices when writing code involving locking: 注释应补充注释和标识符，以使代码易于理解。注释不能替代注释或明确的名称。编写涉及锁定的代码时，请尝试遵循以下最佳实践：

 
* Group member variables protected by a lock with the lock. Where it makes sense, document what is protected by what with a comment in addition to theannotations. For example when several member variables are protected by one lockand several are protected by a different lock, a comment is easier to read thangoing through each annotation. *组成员变量受带有锁的锁保护。在有意义的地方，除注释外，还用注释记录受保护的内容。例如，当几个成员变量受一个锁保护而几个受另一个锁保护时，注释比遍历每个注释更容易阅读。

 
* Name functions that require a lock be held with a 'Locked()' suffix. If there are multiple locks that could be plausibly held to call the function, considermaking the choice clear in the function name. Keep in mind readers of callingcode will not be able to see the annotations. *需要锁定的名称函数带有'Locked（）'后缀。如果可以合理地持有多个锁来调用该函数，请考虑在函数名称中明确选择。请记住，callingcode的读者将看不到注释。

 
## Limitations  局限性 

The thread safety analysis is a purely static check done at compile time and cannot understand conditionally held locks or locking patterns that spancompilation units in ways not expressible via static annotations. In manysituations, this analysis is still useful but there are situations that theanalysis simply cannot understand. The main escape hatch for disabling analysisis to add the annotation `TA_NO_THREAD_SAFETY_ANALYSIS` to the function definitioncontaining the code the analysis is confused by. Other escape mechanisms areavailable as well - see the Clang documentation for details. Situations thatrequire disabling the analysis are likely to be complex for humans to understandas well as machines and should be accompanied by a comment indicating theinvariants in use. 线程安全性分析是在编译时进行的纯静态检查，无法理解通过静态注释无法表达的，跨越编译单元的有条件保持的锁或锁定模式。在许多情况下，此分析仍然有用，但是在某些情况下该分析根本无法理解。禁用分析的主要方法是在函数定义中添加注释“ TA_NO_THREAD_SAFETY_ANALYSIS”，其中包含分析所混淆的代码。也可以使用其他转义机制-有关详细信息，请参见Clang文档。需要禁用分析的情况对于人类以及机器而言可能很复杂，并且应随附说明使用中不变式的注释。

