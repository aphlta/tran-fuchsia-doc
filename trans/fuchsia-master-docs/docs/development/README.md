 
# Development  发展历程 

This document is a top-level entry point to all of Fuchsia documentation related to **developing** Fuchsia and software running on Fuchsia. 本文档是所有与**开发中的Fuchsia和在Fuchsia上运行的软件有关的Fuchsia文档的顶级入口。

 
## Developer workflow  开发人员工作流程 

This sections describes the workflows and tools for building, running, testing and debugging Fuchsia and programs running on Fuchsia. 本节介绍了用于构建，运行，测试和调试Fuchsia的工作流和工具，以及在Fuchsia上运行的程序。

 
 - [Getting started](/docs/getting_started.md) - **start here**. This document covers getting the source, building and running Fuchsia. -[入门]（/ docs / getting_started.md）-**从这里开始**。本文档包括获取源代码，构建和运行紫红色。
 - [Source code](source_code/README.md)  -[源代码]（source_code / README.md）
 - [fx workflows](workflows/fx.md)  -[fx工作流程]（workflows / fx.md）
 - [Multiple device setup](workflows/multi_device.md)  -[多设备设置]（workflows / multi_device.md）
 - [Pushing a package](workflows/package_update.md)  -[推包]（workflows / package_update.md）
 - [Working across different petals](workflows/working_across_petals.md)  -[跨不同花瓣工作]（workflows / working_across_petals.md）
 - [Build system](build/README.md)  -[构建系统]（build / README.md）
 - [Workflow tips and FAQ](workflows/workflow_tips_and_faq.md)  -[工作流程提示和常见问题解答]（工作流程/workflow_tips_and_faq.md）
 - [Testing FAQ](testing/faq.md)  -[测试常见问题解答]（testing / faq.md）

 
## Languages  语言能力 

 
 - [README](languages/README.md) - Language usage in Fuchsia  -[自述]（languages / README.md）-紫红色的语言用法
 - [C/C++](languages/c-cpp/README.md)  -[C / C ++]（语言/c-cpp/README.md）
 - [Dart](languages/dart/README.md)  -[Dart]（语言/dart/README.md）
 - [FIDL](languages/fidl/README.md)  -[FIDL]（语言/fidl/README.md）
 - [Go](languages/go/README.md)  -[开始]（语言/开始/README.md）
 - [Rust](languages/rust/README.md)  -[Rust]（语言/rust/README.md）
 - [Python](languages/python/README.md)  -[Python]（语言/python/README.md）
 - [Flutter modules](languages/dart/mods.md) - how to write a graphical module using Flutter -[Flutter模块]（languages / dart / mods.md）-如何使用Flutter编写图形模块
 - [New language](languages/new/README.md) - how to bring a new language to Fuchsia  -[新语言]（languages / new / README.md）-如何为紫红色带来新的语言

 
## API  API 

 
 - [README](api/README.md) - Developing APIs for Fuchsia  -[README]（api / README.md）-为紫红色开发API
 - [Council](api/council.md) - Definition of the API council  -[委员会]（api / council.md）-API委员会的定义
 - [System](api/system.md) - Rubric for designing the Zircon System Interface  -[System]（api / system.md）-用于设计Zircon系统界面的专栏
 - [FIDL API][fidl-api] - Rubric for designing FIDL protocols  -[FIDL API] [fidl-api]-设计FIDL协议的规则
 - [FIDL style][fidl-style] - FIDL style rubric  -[FIDL样式] [fidl样式]-FIDL样式标题
 - [C](api/c.md) - Rubric for designing C library interfaces  -[C]（api / c.md）-设计C库接口的规则
 - [Tools](api/tools.md) - Rubrics for designing developer tools  -[工具]（api / tools.md）-设计开发人员工具的规则
 - [Devices](api/device_interfaces.md) - Rubric for designing device interfaces  -[设备]（api / device_interfaces.md）-设计设备接口的规则

 
## ABI  阿比 

 
 - [System](/docs/concepts/system/abi/system.md) - Describes scope of the binary-stable Fuchsia System Interface  -[系统]（/ docs / concepts / system / abi / system.md）-描述二进制稳定的紫红色系统接口的范围

 
## SDK  开发包 

 
 - [SDK](sdk/README.md) - information about developing the Fuchsia SDK  -[SDK]（sdk / README.md）-有关开发Fuchsia SDK的信息

 
## Hardware  硬件 

This section covers Fuchsia development hardware targets.  本节介绍了紫红色的开发硬件目标。

 
 - [Acer Switch Alpha 12][acer_12]  -[Acer Switch Alpha 12] [acer_12]
 - [Intel NUC][intel_nuc] (also [this](hardware/developing_on_nuc.md))  -[Intel NUC] [intel_nuc]（也[this]（hardware / developing_on_nuc.md））
 - [Pixelbook](hardware/pixelbook.md)  -[Pixelbook]（硬件/pixelbook.md）
 - [Toulouse][toulouse]  -[图卢兹] [图卢兹]
 - [Khadas VIM2][khadas-vim]  -[Khadas VIM2] [khadas-vim]
 - [iMX8M EVK][imx8mevk]  -[iMX8M EVK] [imx8m evk]
 - [HiKey960 (96boards.org)][hikey960]  -[HiKey960（96boards.org）] [hikey960]

 
## Testing  测试中 

 
 - [Debugging workflow](/docs/development/debugging/debugging.md)  -[调试工作流程]（/ docs / development / debugging / debugging.md）
 - [Fuzz testing with LibFuzzer](/docs/development/testing/fuzzing/libfuzzer.md)  -[使用LibFuzzer进行模糊测试]（/ docs / development / testing / fuzzing / libfuzzer.md）
 - [Test components](testing/test_component.md)  -[测试组件]（testing / test_component.md）
 - [Test environments](testing/environments.md)  -[测试环境]（testing / environments.md）
 - [Testability rubrics](testing/testability_rubric.md)  -[可测试性规则]（testing / testability_rubric.md）
 - [Test flake policy](testing/test_flake_policy.md)  -[测试薄片政策]（testing / test_flake_policy.md）
 - [Testing Isolated Cache Storage](testing/testing_isolated_cache_storage.md)  -[测试隔离式缓存存储]（testing / testing_isolated_cache_storage.md）

 
## Conventions  约定 

This section covers Fuchsia-wide conventions and best practices.  本节涵盖了整个紫红色的公约和最佳实践。

 
 - [Documentation standards](/docs/contribute/best-practices/documentation_standards.md)  -[文档标准]（/ docs / contribute / best-practices / documentation_standards.md）
 - [Endian Issues](source_code/endian.md) and recommendations  -[Endian问题]（source_code / endian.md）和建议

 
## Tracing  追踪 

 
 - [Tracing homepage](tracing/README.md)  -[追踪首页]（tracing / README.md）
 - [Tracing Quick-Start Guide](tracing/quick-start/README.md)  -[追踪快速入门指南]（追踪/快速入门/README.md）
 - [Tracing tutorial](tracing/tutorial.md)  -[入门教程]（tracing / tutorial.md）
 - [Tracing usage guide](tracing/usage-guide.md)  -[追踪使用指南]（tracing / usage-guide.md）
 - [Trace based benchmarking](benchmarking/trace_based_benchmarking.md)  -[基于跟踪的基准测试]（benchmarking / trace_based_benchmarking.md）
 - [Tracing booting Fuchsia](tracing/tracing-boot.md)  -[追踪引导紫红色]（tracing / tracing-boot.md）
 - [CPU Performance Monitor](tracing/cpuperf-provider.md)  -[CPU性能监视器]（tracing / cpuperf-provider.md）

 
## Internationalization  国际化 

 
 - [Internationalization, localization and input methods](internationalization/README.md)  -[国际化，本地化和输入法]（internationalization / README.md）

 
## Miscellaneous  杂 

 
 - [CTU analysis in Zircon](workflows/ctu_analysis.md)  -[Zircon中的CTU分析]（workflows / ctu_analysis.md）
 - [Component Inspection](inspect/README.md)  -[组件检查]（inspect / README.md）
 - [Packet capture](workflows/packet_capture.md)  -[数据包捕获]（workflows / packet_capture.md）
 - [Editor configurations](/docs/development/editors/README.md)  -[编辑器配置]（/ docs / development / editors / README.md）

 

[acer_12]: /docs/development/hardware/acer12.md "Acer 12" [pixelbook]: /docs/development/hardware/pixelbook.md "Pixelbook"[toulouse]: /docs/development/hardware/toulouse.md "Toulouse"[khadas-vim]: /docs/development/hardware/khadas-vim.md "Khadas VIM2"[imx8mevk]: /docs/development/hardware/imx8mevk.md "iMX8M EVK"[hikey960]: /docs/development/hardware/hikey960.md "HiKey960 (96boards.org)" [acer_12]：/docs/development/hardware/acer12.md“ Acer 12” [pixelbook]：/docs/development/hardware/pixelbook.md“ Pixelbook” [toulouse]：/docs/development/hardware/toulouse.md“图卢兹” [khadas-vim]：/docs/development/hardware/khadas-vim.md“ Khadas VIM2” [imx8mevk]：/docs/development/hardware/imx8mevk.md“ iMX8M EVK” [hikey960]：/ docs / development /hardware/hikey960.md“ HiKey960（96boards.org）”

