 
# Library restrictions  图书馆限制 

 
## third_party/absl-cpp  third_party / absl-cpp 

Decision: **do not use** `<absl/synchronization/*>`. On Fuchsia, these classes bottom out in `pthread_mutex_t` and `pthread_cond_t`, which are not the mostefficient primitives on Fuchsia. When `ABSL_INTERNAL_USE_NONPROD_MUTEX` isdefined, these primitives bottom out in something much more sophisticated.Instead, please use `<lib/sync/*.h>`, which bottoms out in optimalsynchronization primitives on Fuchsia. 决策：**不使用**`<absl / synchronization / *>`。在Fuchsia上，这些类在`pthread_mutex_t`和`pthread_cond_t`中触底，这不是Fuchsia上效率最高的原语。当定义了“ ABSL_INTERNAL_USE_NONPROD_MUTEX”时，这些原语会以更复杂的方式触底，而请使用`<lib / sync / *。h>`，其会以倒挂金钟的最佳同步原语触底。

 
## third_party/googletest  third_party / googletest 

Note: The googletest library includes both the former gtest and gmock projects. 注意：googletest库包括以前的gtest和gmock项目。

 
### Gtest  测验 

Use the Gtest framework for writing tests everywhere except the Zircon directory. It provides the `TEST` and `TEST_F` macros as well as the `ASSERT`and `EXPECT` variants we use. 使用Gtest框架在除Zircon目录之外的任何地方编写测试。它提供了“ TEST”和“ TEST_F”宏，以及我们使用的“ ASSERT”和“ EXPECT”变体。

Inside the Zircon directory, use `system/ulib/zxtest` instead. It provides a Gtest-like interface with fewer dependencies on higher-level OS concepts likemutexes (things we want to test). It also supports writing tests inC which is required for some layers. 在Zircon目录中，改用`system / ulib / zxtest`。它提供了一个类似于Gtest的界面，对诸如互斥对象（我们要测试的东西）等更高层次的OS概念的依赖较少。它还支持在某些层中用inC编写测试。

 
### Gmock  m 

Gmock has several components. We allow the gmock matchers such as `ElementsAre()`. Gmock有几个组件。我们允许gmock匹配器，例如`ElementsAre（）`。

There are varying opinions on the team on the function mocking functions (`MOCK_METHOD` and `EXPECT_CALL`). 关于函数模拟功能（`MOCK_METHOD`和`EXPECT_CALL`），团队意见各异。

Pros:  优点：

 
  * It can be very efficient to do certain types of mocking.  *进行某些类型的模拟可能非常有效。
  * Some people feel that Gmock-generated mocks are easier to read than the equivalent custom code. *有些人认为Gmock生成的模拟比等效的自定义代码更易于阅读。
  * Lack of a mocking library means some people might not write good tests.  *缺少模拟库意味着某些人可能不会编写好的测试。

Cons:  缺点：

 
  * Gmock provides a domain-specific language. Not everybody understands this language, and the complex use of templates and macros make it hard todiagnose problems. * Gmock提供了特定领域的语言。并不是每个人都懂这种语言，并且模板和宏的复杂使用使诊断问题变得困难。
  * Some aspects of Gmock encourage overly constrained mocks.  * Gmock的某些方面鼓励过度限制模拟。
  * Combinations of the above can make it harder to make changes to mocked code later. *上面的组合可能使以后更难更改模拟代码。

