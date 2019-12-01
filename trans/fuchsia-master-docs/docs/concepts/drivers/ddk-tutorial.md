 

<!-- (C) Copyright 2018 The Fuchsia Authors. All rights reserved.Use of this source code is governed by a BSD-style license that can befound in the LICENSE file.--> <！-（C）版权所有2018 The Fuchsia Authors。保留所有权利。此源代码的使用由BSD样式的许可证管理，该许可证可以在LICENSE文件中找到。-->

 
# The Driver Development Kit Tutorial  驱动程序开发套件教程 

This document is part of the [Zircon Driver Development Kit](/docs/concepts/drivers/overview.md) documentation.  本文档是[Zircon驱动程序开发套件]（/ docs / concepts / drivers / overview.md）文档的一部分。

This Driver Development Kit (*DDK*) tutorial documentation section consists of:  该驱动程序开发套件（* DDK *）教程文档部分包括：

 
*   [Getting Started](getting_started.md) &mdash; a beginner's guide to writing device drivers  * [入门]（getting_started.md）mdash;编写设备驱动程序的初学者指南
*   [Simple Drivers](simple.md) &mdash; an overview of what a driver does, with code examples  * [简单驱动程序]（simple.md）-驱动程序功能概述，包括代码示例
*   [Hardware Interfacing](hardware.md) &mdash; how to deal with your device's hardware  * [硬件接口]（hardware.md）-如何处理设备的硬件
*   [RAMDisk Device](ramdisk.md) &mdash; walkthrough of RAMdisk block driver  * [RAMDisk设备]（ramdisk.md）mdash; RAMdisk块驱动程序演练
*   [Ethernet Devices](ethernet.md) &mdash; walkthrough of Intel Ethernet driver  * [以太网设备]（ethernet.md）mdash;英特尔以太网驱动程序演练
*   [Advanced Topics and Tips](advanced.md) &mdash; hints for experienced driver writers and comments on unusual situations * [高级主题和技巧]（advanced.md）给经验丰富的驾驶员作家的提示，以及对异常情况的评论
*   [Composite Devices](composite.md) &mdash; talks about devices that are composed of other devices * [复合设备]（composite.md）mdash;讨论由其他设备组成的设备
*   [Tracing](tracing.md) &mdash; monitoring driver performance with tracing *	[C++ DDKTL](using-ddktl.md) &mdash; Using the C++ DDK Template Library * [Tracing]（tracing.md）mdash;通过跟踪监视驱动程序性能* [C ++ DDKTL]（using-ddktl.md）使用C ++ DDK模板库
*   [Reference](reference.md) &mdash; helper functions, data structures, manifest constants  * [参考]（reference.md）mdash;辅助函数，数据结构，清单常量

The sections are listed above in default reading order, but it's perfectly fine to jump around and read them in order of interest or applicability. 上面以默认的阅读顺序列出了这些部分，但是按兴趣或适用性顺序跳转并阅读它们是完全可以的。

Generally, each section is written with increasing complexity; the first parts of each section can safely be skipped / skimmed by experts, whereas a beginner should findsufficient explanation to allow them to understand the advanced sections. 通常，每个部分的编写都越来越复杂。专家可以安全地跳过/略读每个部分的第一部分，而初学者则应找到足够的说明以使他们理解高级部分。

Indeed, the above chapter structure follows the same progression: from beginner to advanced, allowing the expert to skip / skim early sections while providing abeginner with sufficient information. 的确，以上章节的结构遵循相同的过程：从初学者到高级，使专家可以跳过/浏览早期章节，同时为初学者提供足够的信息。

