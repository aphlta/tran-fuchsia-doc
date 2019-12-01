 
# Validator Architecture  验证器架构 

Validator applies automated interactive tests to a stateful library such as Inspect or file systems - an interactive golden file framework. 验证程序将自动交互式测试应用于有状态的库，例如Inspect或文件系统-交互式黄金文件框架。

The Validator architecture includes:  验证器架构包括：

 
* A set of tests to validate functionality.  *一组测试以验证功能。
* A FIDL protocol to invoke operations to be tested.  * FIDL协议调用要测试的操作。
* One or more puppet programs which receive FIDL commands and invoke library calls. *一个或多个接收FIDL命令并调用库调用的木偶程序。
* A reference implementation or simulation of the desired behavior.  *所需行为的参考实现或模拟。
* Analysis of puppet results, comparison to local results, and reporting.  *分析木偶结果，与本地结果进行比较并进行报告。

 
## Inspect Validator  检查验证器 

The Inspect Validator implementation includes:  Inspect Validator实现包括：

 
* [Core Validator program](/src/diagnostics/inspect_validator/src)  * [核心验证程序]（/ src / diagnostics / inspect_validator / src）
    * [Tests](/src/diagnostics/inspect_validator/src/trials.rs)  * [测试]（/ src / diagnostics / inspect_validator / src / trials.rs）
    * [FIDL](/src/diagnostics/inspect_validator/fidl/validate.test.fidl)  * [FIDL]（/ src / diagnostics / inspect_validator / fidl / validate.test.fidl）
    * [Reading the puppet's output](/src/diagnostics/inspect_validator/src/data/scanner.rs)  * [读取人偶的输出]（/ src / diagnostics / inspect_validator / src / data / scanner.rs）
    * [Reference Behavior and comparison](/src/diagnostics/inspect_validator/src/data.rs)  * [参考行为和比较]（/ src / diagnostics / inspect_validator / src / data.rs）
    * [Analysis](/src/diagnostics/inspect_validator/src/runner.rs) and [more analysis](/src/diagnostics/inspect_validator/src/metrics.rs) * [分析]（/ src / diagnostics / inspect_validator / src / runner.rs）和[更多分析]（/ src / diagnostics / inspect_validator / src / metrics.rs）
    * [Reporting](/src/diagnostics/inspect_validator/src/results.rs)  * [报告]（/ src / diagnostics / inspect_validator / src / results.rs）
* [Rust Puppet](/src/diagnostics/inspect_validator/lib/rust/src/main.rs). See also [Inspect Validator Puppet Architecture](puppet.md) * [Rust Puppet]（/ src / diagnostics / inspect_validator / lib / rust / src / main.rs）。另请参见[检查验证器木偶体系结构]（puppet.md）
