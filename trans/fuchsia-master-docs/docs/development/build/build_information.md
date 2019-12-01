 
# Fuchsia Build Information  紫红色建筑信息 

Metrics and error reports are collected from devices in several ways: Cobalt, feedback reports, crashpad crashes, manual reports from developersand QA.  Interpreting these signals requires knowing where they are generatedfrom to varying levels of detail.  This document describes the places whereversion information about the system are stored for use in these types ofreports.  Note that this information only applies to the base system -dynamically or ephemerally added software will not be included here. 从设备以多种方式收集度量和错误报告：钴，反馈报告，崩溃垫崩溃，开发人员的手动报告和质量检查。解释这些信号需要知道它们从何处产生到不同的细节水平。本文档描述了存储系统版本信息以在这些类型的报告中使用的位置。请注意，此信息仅适用于基本系统-动态或短暂添加的软件将不在此处。

 

To view this data via the commandline, you can use `fx shell`. For example:  要通过命令行查看此数据，可以使用`fx shell`。例如：

```sh
fx shell cat /config/build-info/latest-commit-date
```
 

To access this data at runtime, add the feature "build-info" to the [component manifest][component-manifest] of the component that needs toread these fields.  For example: 要在运行时访问此数据，请将功能“ build-info”添加到需要读取这些字段的组件的[component manifest] [component-manifest]中。例如：

```
{% includecode gerrit_repo="fuchsia/fuchsia" gerrit_path="src/developer/feedback/crashpad_agent/tests/meta/crashpad_agent_unittest.cmx" indented_block="\"sandbox\": {" highlight="2,3" %}
```
 

 

 
## Product  产品 
### Location  地点`/config/build-info/product`  `/ config / build-info / product`

 
### Description  描述String describing the product configuration used at build time.  Defaults to the value passed as PRODUCT in fx set. Example: “products/core.gni”, “products/workstation.gni” 描述构建时使用的产品配置的字符串。默认值为在FX集中作为PRODUCT传递的值。例如：“ products / core.gni”，“ products / workstation.gni”

 
## Board  板 
### Location  地点`/config/build-info/board`  `/ config / build-info / board`

 
### Description  描述String describing the board configuration used at build time to specify the target hardware.  Defaults to the value passed as BOARD in fx set. Example: “boards/x64.gni” 描述在构建时用于指定目标硬件的电路板配置的字符串。默认为在fx设置中作为BOARD传递的值。示例：“ boards / x64.gni”

 
## Version  版 
### Location  地点`/config/build-info/version`  `/ config / build-info / version`

 
### Description  描述String describing the version of the build.  Defaults to the same string used currently in ‘latest-commit-date’.  Can be overridden by build infrastructure to provide a more semantically meaningful version, e.g. to include the release train the build was produced on.  描述构建版本的字符串。默认为“最新提交日期”中当前使用的相同字符串。可以由构建基础结构覆盖以提供更具语义意义的版本，例如包括生成该版本的发布火车。

 
## Latest-commit-date  最新提交日期 
### Location  地点`/config/build-info/latest-commit-date`  `/ config / build-info / latest-commit-date`

 
### Description  描述String containing a timestamp of the most recent commit to the integration repository (specifically, the "CommitDate" field) formatted in strict ISO 8601 format in the UTC timezone.  Example: “2019-03-28T15:42:20+00:00”.  字符串，其中包含对集成存储库（特别是“ CommitDate”字段）的最新提交的时间戳记，格式为UTC时区中的严格ISO 8601格式。示例：“ 2019-03-28T15：42：20 + 00：00”。

 
## Snapshot  快照 
### Location  地点`/config/build-info/snapshot`  `/ config / build-info / snapshot`

 
### Description  描述Jiri snapshot of the most recent ‘jiri update’  最新的“ jiri更新”的Jiri快照

 
## Kernel version  内核版本 

 
### Location  地点Stored in vDSO.  Accessed through [`zx_system_get_version`]( /docs/reference/syscalls/system_get_version.md)  存储在vDSO中。通过[`zx_system_get_version`]访问（/docs/reference/syscalls/system_get_version.md）

 
### Description  描述Zircon revision computed during the kernel build process.  在内核构建过程中计算的Zircon版本。

