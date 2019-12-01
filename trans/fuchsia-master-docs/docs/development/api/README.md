 
# API Development  API开发 

This document is a top-level entry point to documentation related to developing APIs for Fuchsia. 本文档是与为紫红色开发API相关的文档的高级入门。

 
## What this covers  这涵盖了什么 

Although the documentation in this directory applies to all Fuchsia APIs, it will be enforced for the _public facing surface area_ of Fuchsia: the FuchsiaAPIs that are surfaced to developers via SDK releases.  All public facing APIchanges will be reviewed by the [API Council](council.md) for consistency withthese guidelines. 尽管此目录中的文档适用于所有Fuchsia API，但仍将针对Fuchsia的“面向公众的表面积”实施：通过SDK版本向开发人员展示的FuchsiaAPI。 [API委员会]（council.md）将审查所有面向公众的API更改，以确保与这些准则保持一致。

 
## Rubrics  专栏 

The documentation in this directory comes in the form of _rubrics_, which are established protocols for how to design and build APIs.  Note that the listbelow is not complete: as Fuchsia evolves, more rubrics will be added. 该目录中的文档以_rubrics_的形式出现，这是有关如何设计和构建API的已建立协议。请注意，下面的列表并不完整：随着紫红色的发展，将会添加更多的标题。

 
 * [API Documentation](documentation.md)  * [API文档]（documentation.md）
 * [CLI and GUI tools](tools.md)  * [CLI和GUI工具]（tools.md）
 * Languages  *语言
   * [C API Readability](c.md)  * [C API可读性]（c.md）
   * [Dart API Readability](dart.md)  * [Dart API可读性]（dart.md）
   * [FIDL Style][fidl-style]  * [FIDL样式] [fidl样式]
   * [FIDL API][fidl-api]  * [FIDL API] [fidl-api]
 * Domain-specific areas  *特定领域
   * [Zircon System Interface](system.md)  * [Zircon系统界面]（system.md）
   * [Fuchsia Device Interface](device_interfaces.md)  * [紫红色的设备接口]（device_interfaces.md）

