 
# Fuchsia Flake Policy  紫红色片状政策 

This document codifies the best practice for interacting with test flakes on Fuchsia. 该文档整理了与紫红色上的测试薄片进行交互的最佳实践。

 
## Background: What is a flaky test?  背景：什么是片状测试？ 

A **flaky test** is a test that sometimes passes and sometimes fails, when run using the exact same revision of the code. 当使用完全相同的代码修订版运行时，“不稳定测试”是有时通过但有时失败的测试。

Flaky tests are bad because they:  片状测试很糟糕，因为它们：

 
-   Risk letting real bugs slip past our commit queue (CQ) infrastructure.  -冒着使实际错误越过我们的提交队列（CQ）基础结构的风险。
-   Devalue otherwise useful tests.  -降低本来有用的测试的价值。
-   Increase the failure rate of CQ, thereby increasing latency for modifying code.  -增加CQ的失败率，从而增加修改代码的等待时间。

This document is specific to *test flakes*, not infrastructure flakes.  本文档特定于*测试片*，而不是基础架构片。

 
## Requirements: Goals for flaky tests  要求：片状测试的目标 

 
1.  **Flakes should be removed from the critical path of CQ as quickly as possible**. 1. **应尽快从CQ的关键路径中移除薄片**。
2.  Since flakes present themselves as a failing test, **flakes should not be ignored** once taken off of CQ. They represent a real problem that should befixed. 2.由于鳞片本身表现为不合格测试，因此一旦从CQ中取出，鳞片就不应被忽略。它们代表了应该解决的实际问题。
3.  Tests may flake at any time, and as a consequence, the observer of these bugs may not necessarily be the person best equipped to fix it. **Theprocess for reporting bugs must be fast, easy, and decoupled from diagnosisand patching.** 3.测试可能会随时剥落，因此，这些漏洞的观察者不一定是最有能力修复漏洞的人。 **报告错误的过程必须快速，轻松，并且与诊断和修补程序脱钩。**

 
## Policy  政策 

The following provides the expected & recommended lifetime of a flake:  以下提供了预期的薄片寿命：

 
0.  A test flakes in CI or CQ.  0. CI或CQ中的测试片。
1.  Identify: The test is *automatically* identified as a flake.  1.识别：测试被“自动”识别为薄片。
2.  Track: An issue is *automatically* filed for the identified flake under the Flake component.  2.跟踪：“自动”针对已识别的薄片在薄片组件下提交问题。
3.  Remove: The test is removed from CQ immediately.  3.删除：立即从CQ中删除测试。
4.  Fix: The offending test is fixed offline and re-enabled.  4.修复：有问题的测试已脱机修复并重新启用。

 
#### Identify  识别 

A flake fetching tool is currently in use to identify the vast majority of flakes.  目前正在使用薄片提取工具来识别绝大多数薄片。

The tool looks for test failures in CQ where the same test succeeded when retried on the same patch set. 该工具在CQ中查找测试失败，当在同一补丁集上重试时，该测试成功进行了同一测试。

(Googlers-Only) To see the source code for this tool, visit [http://go/fuchsia-flake-tool](http://go/fuchsia-flake-tool). （仅限Google员工）要查看此工具的源代码，请访问[http：// go / fuchsia-flake-tool]（http：// go / fuchsia-flake-tool）。

 
#### Track  跟踪 

(Googlers-Only) After flakes are identified, tooling should automatically file an issue for the flake under the Flake component with label FlakeFetcher. These issues are currently beingmanually triaged and assigned. If you experience a test flake, please update existing issuesrather than opening new ones. （仅限Google员工）识别出薄片后，工具应自动将薄片问题提交到带有标签FlakeFetcher的Flake组件下。这些问题目前正在手动分类和分配。如果您遇到测试问题，请更新现有问题，而不要打开新问题。

To see a list of the currently outstanding flakes, visit [http://go/flakes-fuchsia](http://go/flakes-fuchsia). 要查看当前出色的薄片列表，请访问[http：// go / flakes-fuchsia]（http：// go / flakes-fuchsia）。

 
#### Remove  去掉 

One should prioritize, above all else, removing the test from the commit queue. This can be achieved in the following ways: 首先，应优先考虑从提交队列中删除测试。这可以通过以下方式实现：

 
-   If the flake has been prompted by a recent patch: Submitting a revert of a patch which triggers this flake. -如果最近的补丁程序提示了该薄片，请执行以下操作：提交触发该薄片的补丁的还原。
-   [Disable the test](/docs/development/testing/faq.md#disable-test).  -[禁用测试]（/ docs / development / testing / faq.mddisable-test）。

The above mechanisms are recommended because they remove the flaky test and prevent the commit queue from becoming unreliable. The first option (reverting code)is preferred, but it is not as easy as the second option (disabling test), whichreduces test coverage. Importantly, neither of these options prevent diagnosisand fixing of the flake, but they allow it to be processed offline. 建议使用上述机制，因为它们可以消除不稳定的测试并防止提交队列变得不可靠。首选第一个选项（还原代码），但它不如第二个选项（禁用测试）那么容易，因为后者会减少测试的覆盖范围。重要的是，这些选项均不能阻止薄片的诊断和修复，但是它们允许离线处理薄片。

It is **not** recommended to attempt to fix the test without first removing it from CQ. This causes CQ to be unreliable for all othercontributors, which allows additional flakes to compound in the codebase. 不建议不要先将测试从CQ中删除就尝试修复测试。这导致CQ对所有其他贡献者都不可靠，从而使其他片状代码在代码库中复合。

 
#### Fix  固定 

At this point, one can take the filed issue, locally re-enable the test, and work on reproducing the failure. This will enable them to find the root cause, and fix theissue. Once the issue has been fixed, the bug can be closed, and the test can bere-enabled. If any reverted patches need to re-land, they can re-land safely. 在这一点上，人们可以采取已提出的问题，在本地重新启用测试，并努力重现故障。这将使他们能够找到根本原因并修复问题。解决此问题后，可以关闭该错误，然后可以重新启用测试。如果有任何还原的补丁需要重新着陆，则可以安全地重新着陆。

 
## Improvements and Tooling  改进和工具 

Ongoing efforts to improve tooling surrounding flakes are actively underway.  改善薄片周围工具的持续努力正在积极进行中。

These include:  这些包括：

 
-   Automatically assigning issues for resolving flakes, based on information present in OWNERs files. Tracked by 10435. -根据OWNERs文件中的信息自动分配解决薄片的问题。被10435跟踪。
-   "Deflaking" infrastructure, to re-run tests in high volume before they are committed. Tracked by 10011. -“整理”基础架构，以便在提交测试之前重新进行大量测试。被10011跟踪。

