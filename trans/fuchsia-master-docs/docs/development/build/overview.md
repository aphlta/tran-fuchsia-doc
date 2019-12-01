 
# The Fuchsia build system  紫红色的构建系统 

 
## Overview  总览 

The Fuchsia build system aims at building both boot images and updatable packages for various devices. To do so, it uses [GN][gn-main], a meta-buildsystem that generates build files consumed by [Ninja][ninja-main], whichexecutes the actual build. 紫红色的构建系统旨在为各种设备构建引导映像和可更新的软件包。为此，它使用[GN] [gn-main]，这是一个元生成系统，可生成[Ninja] [ninja-main]使用的生成文件，并执行实际的生成。

Note that Zircon uses a different build system, though still using GN and Ninja. 请注意，尽管仍使用GN和Ninja，但Zircon使用了不同的构建系统。

 
## Getting started  入门 

If you are unfamiliar with Fuchsia's build system and GN, see [Using GN build][gn-preso] which outlines the basic principles of the GN build system. 如果您不熟悉Fuchsia的构建系统和GN，请参阅[使用GN构建] [gn-preso]，其中概述了GN构建系统的基本原理。

 
## Boards and Products  板和产品 

The contents of the generated image are controlled by a combination of a board and a product that are the minimal starting configuration of a Fuchsiabuild. Boards and products define dependency sets that define the packagesthat are included in images, updates, and package repositories.[boards and products](boards_and_products.md) documents the structure andusage of these build configurations. 生成的图像的内容由木板和产品的组合来控制，而木板和产品是Fuchsiabuild的最小起始配置。板和产品定义了依赖集，这些依赖集定义了映像，更新和包存储库中包含的包。[板和产品]（boards_and_products.md）记录了这些构建配置的结构和使用情况。

 
## Bundles  捆绑 

A bundle is a grouping of related packages within a part of the source tree, such as all tools or all tests. An overview of bundles is provided in[bundles](bundles.md). A set of top-level bundles are defined in[`//bundles`](/bundles/README.md). 捆绑包是源树的一部分内的相关软件包的分组，例如所有工具或所有测试。捆绑包（bundles）（bundles.md）中提供了概述。在[`//bundles`](/bundles/README.md）中定义了一组顶级捆绑软件。

 
## Build targets  建立目标 

Build targets are defined in `BUILD.gn` files scattered all over the source tree. These files use a Python-like syntax to declare buildable objects: 构建目标在散布在整个源代码树中的“ BUILD.gn”文件中定义。这些文件使用类似Python的语法来声明可构建对象：

```py
import("//build/some/template.gni")

my_template("foo") {
  name = "foo"
  extra_options = "//my/foo/options"
  deps = [
    "//some/random/framework",
    "//some/other/random/framework",
  ]
}
```
 

Available commands (invoked using gn cli tool) and constructs (built-in target declaration types) are defined in the [GN reference][gn-reference]. There arealso a handful of custom templates in `.gni` files in the[`//build` project][build-project]. 可用命令（使用gn cli工具调用）和构造（内置目标声明类型）在[GN参考] [gn-reference]中定义。 [// build项目] [build-project]中的.gni文件中也有一些自定义模板。

These custom templates mostly define custom target declaration types, such as the package declaration type. 这些自定义模板主要定义自定义目标声明类型，例如包声明类型。

> TODO(pylaligand): list available templates  > TODO（pylaligand）：列出可用的模板

 
## Executing a build  执行构建 

The simplest way to this is through the `fx` tool, as described in [Getting Started](/docs/getting_started.md#Setup-Build-Environment). Read on to seewhat `fx` does under the hood. 最简单的方法是通过[fx]工具，如[入门]（/ docs / getting_started.mdSetup-Build-Environment）中所述。继续阅读以了解fx在引擎盖下的功能。

The rest of this document assumes that `gn` and `ninja` commands are available in your `PATH`. These commands can be found in`prebuilt/third_party/gn/<platform>` and`prebuilt/third_party/ninja/<platform>` respectively. Alternatively, ifyou want to avoid modifying your `PATH`, you can prefix all invocationswith `fx`, i.e. `fx gn` or `fx ninja`. 本文档的其余部分假定您在PATH中可以使用gn和ninja命令。这些命令可以分别在`prebuilt / third_party / gn / <platform>`和`prebuilt / third_party / ninja / <platform>`中找到。另外，如果您想避免修改`PATH`，则可以在所有调用前加上`fx`前缀，即`fx gn`或`fx ninja`。

 
### Gen step  根步 

First configure the primary build artifacts by choosing the board and product to build: 首先，通过选择要构建的电路板和产品来配置主要的构建工件：

```bash
$ gn gen out/default --args='import("//boards/x64.gni") import("//products/core.gni")'
```
 

This will create an `out/default` directory containing Ninja files.  这将创建一个包含忍者文件的“ out / default”目录。

The equivalent `fx set` command is:  等效的“ fx set”命令为：

```bash
$ fx set core.x64
```
 

For a list of all GN build arguments, run `gn args out/default --list`. For documentation on the `select_variant` argument, see [Variants](variants.md). 有关所有GN构建参数的列表，请运行gn args out / default --list。有关select_variant参数的文档，请参见[Variants]（variants.md）。

 
### Build step  建立步骤 

The next step is to run the actual build with Ninja:  下一步是使用Ninja运行实际的构建：

```bash
$ ninja -C out/default.zircon
$ ninja -C out/default
```
 

This is what gets run under the hood by `fx build`.  这就是`fx build`在后台运行的内容。

 
## Rebuilding  重建 

In order to rebuild the tree after modifying some sources, just rerun  **Build step**. This holds true even if you modify `BUILD.gn` files as GN addsNinja targets to update Ninja targets if build files are changed! The sameholds true for other files used to configure the build. Any change of sourcethat requires a manual re-invocation of the **Gen step** is a build bug andshould be reported. 为了在修改某些源代码之后重建树，只需重新运行** Build step **。即使您修改BUILD.gn文件也是如此，因为如果更改了构建文件，GN会添加Ninja目标以更新Ninja目标！对于用于配置构建的其他文件也是如此。需要手动重新调用“ Gen步骤”的任何源更改都是构建错误，应报告。

 
## Tips and tricks  技巧和窍门 

 
### Inspecting the content of a GN target  检查GN目标的内容 

```bash
$ gn desc out/default //path/to/my:target
```
 

 
### Finding references to a GN target  查找对GN目标的引用 

```bash
$ gn refs out/default //path/to/my:target
```
 

 
### Referencing targets for the build host  引用构建主机的目标 

Various host tools (some used in the build itself) need to be built along with the final image. 需要与最终映像一起构建各种宿主工具（一些在构建本身中使用的工具）。

To reference a build target for the host toolchain from a module file:  要从模块文件引用宿主工具链的构建目标：

```
//path/to/target(//build/toolchain:host_x64)
```
 

To reference a build target for the host toolchain from within a `BUILD.gn` file: 要从`BUILD.gn`文件中引用宿主工具链的构建目标：

```
//path/to/target($host_toolchain)
```
 

 
### Building only a specific target  仅建立特定目标 

If a target is defined in a GN build file as `//foo/bar/blah:dash`, that target (and its dependencies) can be built with: 如果在GN构建文件中将目标定义为`// foo / bar / blah：dash`，则可以使用以下命令构建该目标（及其依赖项）：

```bash
$ ninja -C out/default -j64 foo/bar/blah:dash
```
 

Note that this only works for targets in the default toolchain.  请注意，这仅适用于默认工具链中的目标。

Note: Building package targets does not result in an updated package repository, because the package repository is updated by the `updates` grouptarget. In order for updated package changes to be made available via `fxserve`, users must build the `updates` group. 注意：构建软件包目标不会导致软件包存储库的更新，因为软件包存储库是由`updates`组目标更新的。为了使更新的软件包更改可通过`fxserve`提供，用户必须建立`updates`组。

 
### Exploring Ninja targets  探索忍者目标 

GN extensively documents which Ninja targets it generates. The documentation is accessible with: GN广泛记录了Ninja生成目标的目标。可通过以下方式访问该文档：

```bash
$ gn help ninja_rules
```
 

You can also browse the set of Ninja targets currently defined in your output directory with: 您还可以使用以下方法浏览输出目录中当前定义的Ninja目标集：

```bash
$ ninja -C out/default -t browse
```
 

Note that the presence of a Ninja target does not mean it will be built - for that it needs to depend on the “default” target. 请注意，Ninja目标的存在并不意味着它将被构建-因为它需要依赖于“默认”目标。

 
### Understanding why Ninja does what it does  了解忍者为什么会做 

Add `-d explain` to your Ninja command to have it explain every step of its execution. 在您的Ninja命令中添加`-d说明`，以说明其执行的每一步。

 
### Debugging build timing issues  调试构建时序问题 

When running a build, Ninja keeps logs that can be used to generate visualizations of the build process: 在运行构建时，Ninja保留了可用于生成构建过程可视化的日志：

 
1. Delete your output directory - this is to ensure the logs represent only the build iteration you’re about to run; 1.删​​除您的输出目录-这是为了确保日志仅代表您要运行的构建迭代；
1. Run a build as you would normally do;  1.按照通常的方式运行构建；
1. Get <https://github.com/nico/ninjatracing>;  1.获取<https://github.com/nico/ninjatracing>;
1. Run `ninjatracing <output directory>/.ninja_log > trace.json`;  1.运行`ninjatracing <输出目录> /。ninja_log> trace.json`;
1. Load the resulting json file in Chrome in `about:tracing`.  1.在“ about：tracing”中将生成的json文件加载到Chrome中。

 

 
## Troubleshooting  故障排除 

 
### My GN target is not being built!  我的GN目标尚未建立！ 

Make sure it rolls up to a label defined in a module file, otherwise the build system will ignore it. 确保将其汇总到模块文件中定义的标签，否则构建系统将忽略它。

 
### GN complains about missing `sysroot`.  GN抱怨缺少sysroot。 

You likely forgot to run both commands of **Build step**.  您可能忘记了运行“构建步骤”的两个命令。

> TODO(pylaligand): command showing path to default target  > TODO（pylaligand）：命令显示默认目标的路径

 

 
### Internal GN setup  内部GN设置 

> TODO(pylaligand): .gn, default target, GN labels insertion  > TODO（pylaligand）：. gn，默认目标，GN标签插入

