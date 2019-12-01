 
# Guidelines for contributing to Zircon  锆石贡献准则 

Zircon is under active development and at this time Zircon is not seeking major changes or new features from new contributors.However, small bugfixes are encouraged. Zircon正在积极开发中，目前Zircon并未寻求新贡献者的重大更改或新功能。但是，建议您进行一些小错误修正。

Here are some general guidelines for patches to Zircon.  以下是有关Zircon修补程序的一些一般准则。

 
## Process  处理 

 
*   Follow the process for Fuchsia patches outlined in [Contribute changes](/docs/development/source_code/contribute_changes.md).  *请遵循[贡献更改]（/ docs / development / source_code / contribute_changes.md）中概述的紫红色补丁程序。

 
*   Patches are handled through [Gerrit Code Review](https://fuchsia-review.googlesource.com/#/q/project:zircon).  *补丁是通过[Gerrit代码审核]（https://fuchsia-review.googlesource.com//q/project:zircon）处理的。

 
*   Additionally, make sure Zircon is buildable for all major targets (x86-64, arm64) at every change. Use `fx multi bringup-cq` so that Zircon is buildable.See [Building Zircon for all targets](/docs/development/kernel/getting_started.md#building_zircon_for_all_targets)for more information. *此外，每次更改时，请确保Zircon可针对所有主要目标（x86-64，arm64）构建。使用`fx multi Bringup-cq`可以构建Zircon。有关更多信息，请参见[为所有目标构建Zircon]（/ docs / development / kernel / getting_started.mdbuilding_zircon_for_all_targets）。

 
*   Avoid breaking the unit tests. Boot Zircon and [run the tests](/docs/development/testing/testing.md) to verify that they're all passing. *避免破坏单元测试。引导Zircon并[运行测试]（/ docs / development / testing / testing.md）以验证它们都通过了。

 
*   Avoid whitespace or style changes. Especially do not mix style changes with patches that do other things as the style changes are a distraction. Use `fx format-code`to format the code with the consistent style. *避免空格或样式更改。特别是不要将样式更改与做其他事情的补丁混合使用，因为样式更改会分散注意力。使用`fx format-code`来格式化具有一致风格的代码。

 
*   Avoid changes that touch multiple modules at once if possible. Most changes should be to a single library, driver, app, etc. *如果可能的话，避免更改一次接触多个模块。大多数更改应针对单个库，驱动程序，应用程序等。

 
## Documentation for Zircon  Zircon的文档 

Writing documentation is a great idea and is encouraged:  编写文档是一个不错的主意，我们建议您：

 
*   Documentation should be in Markdown files.  *文档应位于Markdown文件中。
*   Zircon documentation is located in [/docs/concepts/kernel][googlesource-docs].  * Zircon文档位于[/ docs / concepts / kernel] [googlesource-docs]中。
*   Before submitting documetation, make sure that the markdown renders correctly.  *在提交文档之前，请确保标记正确呈现。

When editing or adding `syscalls` or `cmdlines`, update these documents:  在编辑或添加syscalls或cmdlines时，请更新以下文档：

 
*   A list of `syscalls` in [/docs/reference/syscalls/README.md][syscall-doc]  * [/docs/reference/syscalls/README.md][syscall-doc]中的“ syscalls”列表
*   A list of kernel `cmdline` options in [/docs/reference/kernel/kernel_cmdline.md][cmdline-doc].  * [/docs/reference/kernel/kernel_cmdline.md][cmdline-doc]中的内核`cmdline`选项列表。

 
## Notes  笔记 

 
## How to deprecate #define constants  如何弃用定义常量 

You can create a deprecated `typedef` and have the constant definition cast to that type.  The warning or error that is generated includes the nameof the deprecated `typedef`. 您可以创建一个过时的`typedef`，并将常量定义强制转换为该类型。生成的警告或错误包括已弃用的“ typedef”的名称。

```
typedef int ZX_RESUME_NOT_HANDLED_DEPRECATION __attribute__((deprecated));
#define ZX_RESUME_NOT_HANDLED ((ZX_RESUME_NOT_HANDLED_DEPRECATION)(2))
```
 

