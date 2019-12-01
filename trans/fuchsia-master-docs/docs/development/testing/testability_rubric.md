 
# Fuchsia Testability Rubrics  紫红色可测试性指标 

 
## Goals  目标 

 
### Goals of this document  本文件目标 

Fuchsia Testability is a form of Readability that focuses on ensuring that changes to Fuchsia introduce testable and tested code. 紫红色可测试性是可读性的一种形式，其重点在于确保对紫红色的更改引入可测试的代码。

As with any Readability process, the guidelines and standards are best made publicly available, for reviewers and reviewees. This document is the FuchsiaTestability equivalent of a style guide for a programming language readabilityprocess. 与任何可读性过程一样，指南和标准最好公开提供给审阅者和受审者。该文档与FuchsiaTestability等效，等效于编程语言可读性过程的样式指南。

It’s valuable to apply the Testability standards consistently, hence it is important that anyone involved in Testability should study the doc (whetheryou’re reviewing changes or authoring them). 始终如一地应用“可测试性”标准很有价值，因此，与“可测试性”相关的任何人都应该研究该文档（无论您是查看更改还是编写更改），这一点很重要。

The exact contents of the doc may change over time.  文档的确切内容可能会随时间而变化。

 
### Your goals as a Testability reviewer  您作为可测试性审核者的目标 

 
*   **Determine if the change is tested.** Apply Testability-Review+1 if you agree that it’s tested, and consider applying Testability-1 along with anote for what’s missing if it’s not. * **确定是否已测试更改。**如果同意测试，请应用Testability-Review + 1，并考虑将Testability-1连同注释一起应用（如果未测试）。
*   Focus on whether the change is tested, not necessarily on what the change actually does. For instance you may apply Testability+1 if the change iswell tested and at the same time Code-Review-1 if you would not like to seethe change merged for other reasons. *专注于更改是否经过测试，而不必关注更改的实际作用。例如，如果对变更进行了良好的测试，则可以应用Testability + 1；如果由于其他原因而不想看到变更合并，则可以同时使用Code-Review-1。
*   Apply the standard (this doc) consistently.  *一致地应用标准（本文档）。
*   For your own changes, it is okay to self Testability-Review+1 provided that the change clearly follows this rubric. If in doubt, seek approval fromanother testability reviewer. *对于您自己的更改，只要更改明确遵循此规则，就可以进行自我Testability-Review + 1。如有疑问，请寻求另一位可测试性审核者的批准。
*   If the change needs to be amended to meet the standards, provide actionable feedback. *如果需要修改更改以符合标准，请提供可行的反馈。
*   Promote Fuchsia testing & testability.  *促进紫红色测试的可测试性。
*   Identify cases not handled by this doc and propose changes.  *找出本文档未处理的案例并提出更改建议。
*   **Uphold the standard** but also **apply your good judgement**. The goal is to improve quality and promote a culture of testing. You’re not expected toexecute a precise decision algorithm. * **坚持标准**，但也**应用您的良好判断**。目的是提高质量并促进测试文化。您不希望执行精确的决策算法。

 
### Your goals as a change author  您作为变革作者的目标 

 
*   Inform yourself of the standards by reading this doc (you’re doing it right now!). *阅读此文档，以告知自己标准（您现在就在做！）。
*   Respect that your Testability reviewer is volunteering for the role, and treat them appropriately. *尊重您的可测试性审核员自愿担任该角色，并适当对待他们。
*   Consider feedback given for ways that you could improve confidence in your change using testing. *考虑提供的反馈，以帮助您通过测试提高对变更的信心。

 
## What to test? How to test?  要测试什么？怎么测试？ 

 
*   **Changes to functionality should have a test that would have failed without said change.** * **对功能的更改应进行测试，如果没有上述更改，该测试将失败。**
*   **Tests must be local to the code being changed: dependencies with test coverage do not count as test coverage.** For example, if "A" is used by a"B", and the "B" contains tests, this does not provide coverage for "A".If bugs are caught with "B"'s tests, they will manifest indirectly, makingthem harder to pinpoint to "A". Similarly, if "B" is deprecated (or justchanges its dependencies) all coverage for "A" would be lost. * **测试必须在要更改的代码的本地进行：具有测试覆盖率的依赖项不算作测试覆盖率。**例如，如果“ A”被“ B”使用，而“ B”包含测试，则此如果“ B”的测试中发现了错误，则它们将间接显示出来，从而使它们更难指出“ A”。同样，如果不赞成使用“ B”（或只是更改其依赖性），则“ A”的所有覆盖范围都将丢失。
*   **Tests must be automated (CI/CQ when supported)**. A manual test is not sufficient, because there is no guarantee that a future change to the code(especially when authored by another engineer) will exercise the same manualtests. Exceptions may apply to some parts of the codebase to recognizeongoing automation challenges. * **测试必须是自动化的（如果支持，则为CI / CQ）**。手动测试是不够的，因为不能保证将来对代码的更改（尤其是在由另一位工程师创作时）将进行相同的手动测试。异常可能适用于代码库的某些部分，以识别持续的自动化挑战。
*   **Tests must minimize their external dependencies**. Our test infrastructure explicitly provisions each test with certain resources, but tests are ableto access more than those that are provisioned. Examples of resourcesinclude hardware, CPU, memory, persistent storage, network, other IOdevices, reserved network ports, and system services. The stability andavailability of resources that are not provisioned explicitly for a testcannot be guaranteed, so tests that access such resources are inherentlyflaky and / or difficult to reproduce. Tests must not access externalresources beyond the control of the test infrastructure. For example, testsmust not access services on the Internet. Tests should only use resourcesbeyond those provisioned explicitly for that test when necessary. Forexample, tests might have to access system services that do not have testdoubles available. A small number of exceptions to this rule are made forend-to-end tests. * **测试必须最小化其外部依赖性**。我们的测试基础架构显式地为每个测试提供了某些资源，但是测试能够访问的资源比所提供的更多。资源的示例包括硬件，CPU，内存，持久性存储，网络，其他IO设备，保留的网络端口和系统服务。不能保证没有为测试明确配置的资源的稳定性和可用性，因此访问此类资源的测试本质上是易碎的和/或难以复制的。测试不得访问超出测试基础架构控制范围的外部资源。例如，测试一定不能访问Internet上的服务。测试仅在必要时使用超出为该测试明确提供的资源。例如，测试可能必须访问没有可用的testdouble的系统服务。端到端测试是该规则的少数例外。
*   **Changes to legacy code** (old code that predates Testability requirements and is poorly tested) must be tested. Proximity to poorly-tested code is nota reason to not test new code. Untested legacy code isn’t necessarily oldand crufty, it may be proven and battle-hardened, whereas new code thatisn’t tested is more likely to fail! * **对遗留代码的更改**（早于可测试性要求且未经测试的旧代码）必须进行测试。接近测试不良的代码并不是不测试新代码的原因。未经测试的旧代码不一定是旧的，也不是笨拙的，它可能已经过验证并且经过了艰苦的努力，而未经测试的新代码更有可能失败！
*   **Changes you are making to someone else’s code** are subject to the same Testability requirements. If the author is changing code they’re notfamiliar with or responsible for, that’s more reason to test it well. Theauthor can be expected to work with the responsible individual or team tofind effective ways to test the change. Individuals responsible for the codeunder change are expected to help the author with testability with the samepriority as the author’s change. * **您对其他人的代码所做的更改**受相同的可测试性要求的约束。如果作者正在更改代码，他们不熟悉或不负责，这就是更好地对其进行测试的原因。可以期望作者与负责的个人或团队合作，以找到测试变更的有效方法。希望对代码下的变更负责的个人以与作者的变更相同的优先级帮助作者进行可测试性。

 
## What does not require testing  什么不需要测试 

Missing testing coverage for the below should not prevent a change from receiving Testability+1. 缺少以下内容的测试范围不应该阻止更改获得Testability + 1。

 
*   **Logging.** In most cases, it’s probably not worth testing the log output of components. The log output is usually treated as opaque data by the restof the system, which means changes to log output are unlikely to break othersystem. However, if the log output is load bearing in some way (e.g.,perhaps some other system depends on observing certain log messages), thenthat contract is worth testing. This can also apply to other forms ofinstrumentation, such as Tracing. This does not apply to instrumentationwhen it is used as a contract, for instance Inspect usage can be tested, andshould be if you rely on it working as intended (for instance in fx iqueryor feedback reports). * **记录。**在大多数情况下，可能不值得测试组件的日志输出。日志输出通常被系统的其余部分视为不透明数据，这意味着对日志输出的更改不太可能破坏其他系统。但是，如果日志输出以某种方式承受负载（例如，也许某些其他系统依赖于观察某些日志消息），则该合同值得测试。这也可以适用于其他形式的仪器，例如跟踪。这不适用于用作合同的工具，例如可以检查Inspect的使用情况，以及是否应该依靠它按预期工作（例如，在fx iquery或反馈报告中）。
*   **Code that we don’t own** (the source of truth is not in Fuchsia tree). Changes that pick up an update to source code that’s copied from elsewheredon’t bear testability requirements. * **我们不拥有的代码**（真理的来源不在紫红色的树中）。从其他地方复制的对源代码进行更新的更改不具备可测试性要求。
*   **Pure refactors** (changes that could have entirely been made by an automated refactor tool), such as moving files, renaming symbols, ordeleting them, don’t bear testability requirements. Some languages can havebehavior that’s exposed to such changes (e.g. runtime reflection), soexceptions may apply. * **纯重构**（可能完全由自动化重构工具进行的更改），例如移动文件，重命名符号或删除它们，不具备可测试性要求。某些语言的行为可能会受到此类更改的影响（例如，运行时反射），因此可能会出现例外情况。
*   **Generated code.** Changes that are generated by tools (such as formatting, or generated code checked in as a golden file) don’t bear testabilityrequirements. As an aside, it’s generally discouraged to check in generatedcode (rather harness the tools and have the code be generated at buildtime), but in the exceptional case don’t require tests for code written bymachines. * **生成的代码。**由工具生成的更改（例如格式或生成的代码作为黄金文件签入）不具有可测试性要求。顺便说一句，通常不建议检入生成的代码（而是利用工具并在构建时生成代码），但在特殊情况下，不需要对机器编写的代码进行测试。
*   **Testability bootstrapping.** In cases where the change is in preparation for introducing testability to the code, and this is explicitly documentedby the author, then Testability reviewers may exercise discretion and takean IOU. * **可测试性引导。**如果为准备将可测试性引入代码而进行了更改，并且作者明确记录了该内容，则可测试性审阅者可以酌情决定并采取IOU。
*   **Manual tests.** Manual tests are often themselves used to test or demonstrate functionality that is hard to test in an automated fashion.Additions or modifications to manual tests therefore do not requireautomated tests. However, it is strongly recommended that manual tests bepaired with a README.md or TESTING.md document describing how to run them. * **手动测试。**手动测试本身通常用于测试或演示难以以自动化方式进行测试的功能。因此，对手动测试的添加或修改不需要自动化测试。但是，强烈建议将手动测试与描述如何运行它们的README.md或TESTING.md文档进行配对。
*   **Hardcoded values.** Additions or changes to hardcoded values do not necessarily require tests. Oftentimes, these values control behaviors thatare not easily observable, such as unexposed implementationdetails, heuristics, or "cosmetic" changes (e.g. background color of a UI).Tests of the style `assert_eq!(CONFIG_PARAM, 5);` are not considered usefuland are not required by testability. However, if the CL results in an easilyobservable behavioral change, the CL should include a test for the newbehavior. * **硬编码的值。**硬编码值的添加或更改不一定需要测试。通常，这些值控制着不容易观察到的行为，例如未公开的实现细节，试探法或“外观”更改（例如，UI的背景色）。测试“ assert_eq！（CONFIG_PARAM，5）;”样式不被认为是有用的，并且可测性不是必需的。但是，如果CL导致容易观察到的行为变化，则CL应包括对新行为的测试。

 
## What does require testing  什么需要测试 

 
### Tests must be tested for flakiness (if supported)  测试必须进行片状测试（如果支持） 

As a testability reviewer, if a change is tested with automated tests, you should make sure the author has added the MULTIPLY feature as described belowand has run a successful tryjob that uses this feature (if supported). You cancheck to see if it worked by clicking on the tryjob and looking for a step thatsays `shard multiplied:<shard name>-<test name>` for each test. This featureis only supported for builders that test in shards. If there are no suchbuilders that run their tests, they will not be able to use this feature. 作为可测试性的审查者，如果使用自动测试对更改进行了测试，则应确保作者添加了如下所述的MULTIPLY功能，并且已经运行了使用此功能的成功尝试（如果支持）。您可以通过单击tryjob并寻找一个步骤说“ shard multiplied：<shard name>-<test name>”来检查它是否有效。仅在分片中测试的构建器支持此功能。如果没有此类构建器可以运行其测试，则他们将无法使用此功能。

As a change author, when you add or modify automated tests, you should specifiy this with a MULTIPLY field in the commit message. For example, ``MULTIPLY:`<json_string>` `` where `<json_string>` should be a list of tests followingthis schema: 作为更改作者，添加或修改自动化测试时，应在提交消息中使用MULTIPLY字段进行指定。例如，``MULTIPLY：`<json_string>```其中<json_string>应该是遵循该模式的测试列表：

```json
[
  {
    "name": <test basename, e.g., "foo_bin_test">,
    "os": <one of "fuchsia", "linux", "mac"; defaults to "fuchsia">,
    "total_runs": <any positive int; defaults to 1>
  },
  ...
]
```
 

The test name refers to the name of a test executable inside a `test_package` GN target which is located in the `out/default/tests.json` file located inyour Fuchsia directory. This file is created after you run `fx build` insideof your Fuchsia directory. The test name and OS must match one of the testsin this list for this feature to work. 测试名称是指“ test_package” GN目标内部测试可执行文件的名称，该目标位于Fuchsia目录中的“ out / default / tests.json”文件中。该文件是在您的Fuchsia目录中运行`fx build`之后创建的。测试名称和操作系统必须与该列表中的测试之一匹配，此功能才能起作用。

An example CL description should look like:  CL说明示例应如下所示：

```json
[foo] Add new foo compatibility tests

This change adds a new test.

MULTIPLY: `[
  {
    "name": "foo_tests",
    "total_runs": 30
  },
  {
    "name": "foo_host_tests",
    "os": "linux",
    "total_runs": 30
  }
]`
```
 

You should then choose a tryjob that runs your tests. These tests show as separate shards for each test, which run that test as many times as thespecified `total_runs`. The timeout for running these tests is 40 minutes. If atest takes too long, the shard may time out. It is recommended that you startwith a `total_runs` of `30`. 然后，您应该选择一个可以运行测试的tryjob。这些测试显示为每个测试的单独分片，与指定的“ total_runs”运行相同的次数。运行这些测试的超时为40分钟。如果测试花费太长时间，则分片可能会超时。建议您以“ total_runs”为“ 30”开始。

 
### Tests should not sleep  测试不应该睡觉 

Sleeps can lead to flaky tests because timing is difficult to control across different test environments.  Some factors that can contribute to thisdifficulty this are the test target's CPU speed, number of cores, and systemload along with environmental factors like temperature. 睡眠会导致测试不稳定，因为难以在不同的测试环境中控制时间。导致这种困难的一些因素是测试目标的CPU速度，内核数和系统负载以及环境因素（例如温度）。

 
    ```c++
    // Check if the callback was called.
    zx_nanosleep(zx_deadline_after(ZX_MSEC(100)));
    EXPECT_EQ(true, callback_happened);
    ```
*   Avoid something like:  *避免类似：

 
    ```c++
    // In callback
    callback() {
        sync_completion_signal(&event_);
    }

    // In test
    sync_completion_wait(&event_, ZX_TIME_INFINITE);
    sync_completion_reset(&event_);
    ```
*   Instead, explicitly wait for the condition:  *相反，显式等待条件：

    This code sample was adapted from [task-test.cc](https://fuchsia-review.googlesource.com/c/fuchsia/+/326106/7/src/camera/drivers/hw_accel/ge2d/test/task-test.cc#48).  该代码示例改编自[task-test.cc]（https://fuchsia-review.googlesource.com/c/fuchsia/+/326106/7/src/camera/drivers/hw_accel/ge2d/test/task- test.cc48）。

 
## Recently removed exemptions  最近删除的豁免 

 
*   **Engprod scripts** (e.g. `fx` commands) and associated configuration files** no longer have an exemption from testability. `fx` must have integrationtests before further changes land. Exceptions may be granted by the fx teamafter consulting with a testability reviewer. * ** Engprod脚本**（例如`fx`命令）和相关的配置文件**不再具有可测试性。 fx必须先进行集成测试，然后才能进行进一步的更改。 FX团队在与可测试性审核者协商后可以授予例外。

 
## Temporary testability exemptions  临时可测试性豁免 

The following are currently exempt from Testability, while ongoing work aims to change that. 目前，以下内容不受“可测试性”的约束，而正在进行的工作旨在改变这一点。

 
*   **Engprod scripts** in the tools/devshell/contrib and associated configuration are exempt. * ** tools / devshell / contrib中的Engprod脚本**和相关的配置是免除的。
*   **GN templates** are not easily testable. We are working on a test framework for GN templates. Until then, it's permitted for build template changes tobe manually tested only. * ** GN模板**不容易测试。我们正在为GN模板开发测试框架。在此之前，仅允许对构建模板更改进行手动测试。
*   **Resource leaks** are not easily preventable in C-style code. In the longer term, such code should be refactored to use Rust or modern C++ idioms toreduce the chances of leaks, and automation should exist that is capable ofautomatically detecting leaks. * **资源泄漏**在C风格的代码中很难防止。从长远来看，应将此类代码重构为使用Rust或现代C ++习惯用法以减少泄漏的机会，并且应该存在能够自动检测泄漏的自动化。
