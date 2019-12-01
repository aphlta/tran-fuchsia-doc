 
# Source code layout  源代码布局 

 
## Status  状态 

We are currently migrating to this source code layout. Some aspects of this document reflect the current reality, but some aspects are still aspirational. 我们目前正在迁移到此源代码布局。该文档的某些方面反映了当前的现实，但某些方面仍然是理想的。

 
## Overview  总览 

Most first-party, open-source code is in the ["fuchsia.git" repository](https://fuchsia.googlesource.com/fuchsia). Most code in thisrepository is organized into a recursive tree of *areas*. 大多数第一方开放源代码都在[“ fuchsia.git”存储库]（https://fuchsia.googlesource.com/fuchsia）中。此存储库中的大多数代码都组织成* area *的递归树。

Areas have a regular internal and dependency structure. The `fuchsia.git` repository itself follows the structure of an area, but also has additionalstructure unique to the top level. 区域具有规则的内部和依存结构。 `fuchsia.git`存储库本身遵循区域的结构，但也具有顶层唯一的其他结构。

Specifically, the `src` top level directory of `fuchsia.git` can be considered the root area. It follows the structure required of an area, and is the placewhere sub areas are located. However, some directories required of an area alsoexist next to `src` rather than inside it, e.g. `third_party`. These can bethought of global ones for all areas to depend on. There are also other placesoutside `src` that hold further top-level areas, e.g. in `vendor/*`.Being open source code `third_party` is available to all areas. 具体来说，可以将fuchsia.git的src顶级目录视为根区域。它遵循区域所需的结构，并且是子区域所在的位置。但是，某些区域所需的目录也存在于``src''旁边而不是内部，例如`third_party`。这些可以被认为是全球性的，所有领域都可以依靠。除了src之外，还有其他地方可以容纳其他顶级区域，例如在`vendor / *`中。开源代码third_party在所有地区都可用。

Source repositories, whether open- or closed-source, also follow the conventions for areas and are mapped into subdirectories of `src` in fuchsia.git. Currently,we have small number of such "petal" repositories, but we will "promote" areascurrently in the `fuchsia.git` repository into separate repositories as thesystem stabilizes. 源存储库，无论是开放源代码库还是封闭源代码库，都遵循区域约定，并映射到fuchsia.git中的src子目录中。当前，我们只有很少的此类“花瓣”存储库，但随着系统的稳定，我们目前将“ fuchsia.git”存储库中的区域“提升”到单独的存储库中。

The `vendor/*` directories contain closed-source code, organized by the vendor of that code. Nothing outside of `//vendor` can depend on `//vendor`.Dependencies between different vendors is supported, `vendor/A` can have adepency on `vendor/B`. “ vendor / *”目录包含由源代码组织的封闭源代码。 `// vendor`之外的任何东西都不能依赖`// vendor`。支持不同供应商之间的依赖关系，`vendor / A`可以兼容`vendor / B`。

The `products` directory contains a list of products that you can build. Some products are quite small and build quickly (e.g., the [core](/products/core.gni)product), whereas others are more elaborate (e.g., the[workstation](/products/workstation.gni) product). “ products”目录包含可以构建的产品列表。一些产品很小，并且可以快速构建（例如[core]（/ products / core.gni）产品），而另一些产品则更加精细（例如[workstation]（/ products / workstation.gni）产品）。

Most third-party dependencies are stored in separate repositories. These repositories are included in a local checkout only when needed to support one ofthe following source tree configurations: 大多数第三方依赖项都存储在单独的存储库中。仅在需要支持以下源树配置之一时，这些存储库才包含在本地签出中：

 
 * Bringup. This source tree configuration contains enough code to build the [bringup](/products/bringup.gni) product. * 培养。此源树配置包含足够的代码来构建[bringup]（/ products / bringup.gni）产品。
 * Open Source. This source tree configuration contains all the open source code in the Fuchsia Source Tree. *开源。此源代码树配置包含“紫红色源代码树”中的所有开放源代码。
 * All Source.  This source tree configuration contains all the open and closed source code in the Fuchsia Source Tree. *所有来源。此源代码树配置包含“紫红色”源代码树中所有打开和关闭的源代码。

 
## Areas  地区 

Most code is organized into a recursive tree of areas. Each area has a regular internal and dependency structure, which helps people understand code structureacross the whole project. 大多数代码被组织成区域的递归树。每个区域都具有规则的内部结构和依赖关系结构，这有助于人们了解整个项目中的代码结构。

 
### Directory Structure  目录结构 

Each area is required to have an [OWNERS](owners.md) file as well as documentation and tests. Areas can also include binaries, libraries, drivers,and other source code. In addition, areas can have subareas, which repeat thepattern: 每个区域都必须具有[OWNERS]（owners.md）文件以及文档和测试。区域还可以包括二进制文件，库，驱动程序和其他源代码。此外，区域可以具有子区域，这些子区域会重复此模式：

 
 * `OWNERS`  *`OWNERS`
    * Each area or subarea must have a [list of owners](owners.md)  *每个区域或子区域必须具有[所有者列表]（owners.md）
 * `BUILD.gn`  *`BUILD.gn`
    * Build file defining the [canonical targets](#canonical-targets) for the area. The area owners may add additional targets to this in addition tothe canonical targets. *构建文件，定义该区域的[规范目标]（canonical-targets）。区域所有者可以在规范目标之外添加其他目标。
 * `docs/`  *`docs /`
    * This directory should contain docs for people working in this area  *此目录应包含该领域工作人员的文档
    * Docs for end-developers (or people working in other areas of Fuchsia) should be in the top-level docs or sdk repository *最终开发人员（或在紫红色其他地区工作的人）的文档应位于顶级文档或sdk存储库中
 * `bundles/`  *`bundles /`
    * This directory contains bundles of package targets in this area. Each area should contain at least a `tests` bundle with unit tests for the area, butmay include other bundles. *此目录包含此区域中的软件包目标捆绑包。每个区域至少应包含一个“ tests”捆绑包以及该区域的单元测试，但可能包括其他捆绑包。
 * `bin/` (optional)  *`bin /`（可选）
 * `lib/` (optional)  *`lib /`（可选）
 * `drivers/` (optional)  *`drivers /`（可选）
 * `examples/` (optional)  *`examples /`（可选）
 * `fidl/` (optional)  *`fidl /`（可选）
    * In some cases, an area might have internal FIDL interfaces that are not exposed to other areas or to end-developers. Rather than put thoseinterfaces in the SDK, an area can put those interfaces in this directory. *在某些情况下，某个区域可能具有内部FIDL接口，而这些接口并未暴露给其他区域或最终开发人员。可以将这些接口放在此目录中，而不是将这些接口放在SDK中。
 * `tests/` (optional)  *`tests /`（可选）
    * This directory contains integration tests that span multiple source code directories within the area *此目录包含跨该区域内多个源代码目录的集成测试
    * If disparate areas can have tests in subdirectories, it is suggested to add OWNERS files for different test directories to clarify ownership. *如果不同区域可以在子目录中进行测试，建议为不同的测试目录添加OWNERS文件，以阐明所有权。
    * Unit tests that cover a single binary or library are better placed alongside the code they test *覆盖单个二进制文件或库的单元测试最好与它们测试的代码一起放置
 * `testing/` (optional)  *`testing /`（可选）
    * This directory contains utilities and libraries useful for writing tests in this area and subareas. *此目录包含实用程序和库，可用于在此区域和子区域中编写测试。
    * Targets in this directory can only be depended on by testonly targets.  *此目录中的目标只能由testonly目标来依赖。
 * `third_party/` (optional)  *`third_party /`（可选）
    * Most third_party dependencies should be in separate repositories  *大多数third_party依赖项应位于单独的存储库中
    * Include third_party dependencies in an area only if all of the following:  *仅在满足以下所有条件时，才在区域中包含third_party依赖项：
        * The code is required to be in a third_party directory by policy  *根据政策，该代码必须位于第三方目录中
        * You intend to fork upstream (i.e., make major changes and not plan to integrate future changes from upstream) *您打算分叉上游（即进行重大更改，而不打算整合上游的未来更改）
        * You make a new name for the code that (a) does not match upstream and (b) does not appear in any other third_party directory anywhere in theFuchsia Source Tree *您为（a）上游不匹配和（b）不在紫红色源树中任何其他第三方目录中的代码重新命名
        * The code is open source  *该代码是开源的
 * `tools/` (optional)  *`tools /`（可选）
   * This directory contains command-line tools provided by the area.  These are usually things that can (or must) be built for the development hostrather than for Fuchsia.  They may or may not be used directly in thearea's own build, but can also be used by developers.  They may or maynot be published in an SDK.  Special-purpose tools that are used in thebuild but really are not intended for developers to use directly shouldbe kept near their uses rather than here. *此目录包含该区域提供的命令行工具。这些通常是可以（或必须）为开发主机而非紫红色构建的。它们可能会或可能不会直接在区域自己的构建中使用，但也可由开发人员使用。它们可能会或可能不会在SDK中发布。在构建中使用但实际上不打算供开发人员直接使用的专用工具应放在靠近其用途的地方，而不是在此处。
   * This should contain a a subdirectory named for each tool (or collection of related tools with a natural collective name), rather than putting allof the area's tools together into the top `tools/BUILD.gn` file. *这应该包含一个为每个工具命名的子目录（或具有自然集合名称的相关工具的集合），而不是将该区域的所有工具放到顶部的tools / BUILD.gn文件中。
 * `[subareas]` (optional)  *`[子区域]`（可选）
    * Subareas should follow the generic area template  *子区域应遵循通用区域模板
    * Do not create deeply nested area structures (e.g., three should be enough)  *不要创建深度嵌套的区域结构（例如，三个就足够了）

Areas may use additional directories for internal organization in addition to the enumerated directories. 除了列举的目录外，区域还可以使用其他目录进行内部组织。

 
### OWNERS  拥有者 

A directory inside an area that contains an `OWNERS` file is considered a subarea and must adhere to the contract for areas. A directory lacking an`OWNERS` file is considered part of the same area. 包含“ OWNERS”文件的区域内的目录被视为子区域，并且必须遵守区域合同。缺少OWNERS文件的目录被视为同一区域的一部分。

In the `fuchsia.git` repository, there exist directories with `OWNERS` that are not considered areas, e.g. the top level `products` directory, or subdirectoriesof the `/src/lib` directory. 在`fuchsia.git`存储库中，存在带有`OWNERS`的目录，这些目录不被视为区域，例如顶级“产品”目录或“ / src / lib”目录的子目录。

One exception is the `//src/tests` directory where tests from different areas that cover multiple aspects of the system (not just a particular area) areexpected to live. Because of this, every area should add OWNERS files for anytests that live in this directory. 一个例外是“ // src / tests”目录，该目录中的预期覆盖系统多个方面（而不仅仅是特定区域）的不同区域的测试将继续进行。因此，每个区域都应为该目录中存在的任何测试添加OWNERS文件。

 
### Dependency Structure  依赖结构 

In addition to depending on itself, an area can depend only on the top-level `build`, `sdk`, and `third_party` directories, as well as the `lib` directoriesof its ancestors: 除了依赖于自身之外，区域还只能依赖于其祖先的顶层“ build”，“ sdk”和“ third_party”目录以及“ lib”目录：

 
 * `//build`  *`// build`
 * `//sdk`  *`// sdk`
 * `//third_party`  *`// third_party`
 * `(../)+lib/`  *`（../)+ lib /`

Targets in an area that are marked testonly in the build system may additionally depend on the `testing` directory in that area and ancestors: 在构建系统中标记为testonly的区域中的目标可能还取决于该区域中的`testing'目录和祖先：

 
 * `(../)+testing/` (testonly=true targets only)  *`（../)+ testing /`（testonly =仅真目标）

 
### Canonical targets  规范目标 

Each area and subarea must define the following canonical targets in their top-level BUILD.gn file: 每个区域和子区域必须在其顶级BUILD.gn文件中定义以下规范目标：

 
* `tests`  *`测试`
  * All of the tests within this area  *此区域内的所有测试

 
## Repository layout  仓库布局 

This section depicts the directory layout for the Fuchsia Source Tree. Non-bold entries are directories or files in the fuchsia.git repository. Bold entries areseparate repositories that are mapped into the directory structure using `jiri`(except for the prebuilt directory, which is populated from CIPD). 本节描述了紫红色源树的目录布局。非粗体条目是fuchsia.git存储库中的目录或文件。粗体条目是单独的存储库，使用`jiri`映射到目录结构中（预建目录除外，该目录是从CIPD填充的）。

 
 * `.clang-format`  *`.clang-format`
 * `.dir-locals.el`  *`.dir-locals.el`
 * `.gitattributes`  *`.gitattributes`
 * `.gitignore`  *`.gitignore`
 * `AUTHORS`  *`作者`
 * `CODE_OF_CONDUCT.md`  *`CODE_OF_CONDUCT.md`
 * `CONTRIBUTING.md`  *`CONTRIBUTING.md`
 * `LICENSE`  *许可
 * `OWNERS`  *`OWNERS`
 * `PATENTS`  *`Patents`
 * `README.md`  *`README.md`
 * `rustfmt.toml`  *`rustfmt.toml`
 * `sdk/banjo/ddk.protocol.gpio/`  *`sdk / banjo / ddk.protocol.gpio /`
 * `sdk/banjo/...`  *`sdk / banjo / ...`
 * `sdk/fidl/fuchsia.media/`  *`sdk / fidl / fuchsia.media /`
 * `sdk/fidl/fuchsia.mediacodec/`  *`sdk / fidl / fuchsia.mediacodec /`
 * `sdk/fidl/...`  *`sdk / fidl / ...`
 * `sdk/lib/ddk/`  *`sdk / lib / ddk /`
 * `sdk/lib/fit/`  *`sdk / lib / fit /`
 * `sdk/lib/fidl/`  *`sdk / lib / fidl /`
 * `sdk/lib/zircon/`  *`sdk / lib / zircon /`
 * `sdk/lib/...`  *`sdk / lib / ...`
 * `.gn`  *`.gn`
 * `BUILD.gn`  *`BUILD.gn`
 * `build/`  *`build /`
 * `bundles/`  *`bundles /`
 * `configs/`  *`configs /`
 * `infra/`  *`infra /`
    * `configs/`  *`configs /`
       * `generated/`  *`generated /`
 * `integration/`  *`整合/`
 * `products/`  *`产品/`
 * `scripts/`  *`scripts /`
 * `docs/`  *`docs /`
 * `examples/`  *`examples /`
 * `third_party/`  *`third_party /`
    * **`boringssl/`**  * **`boringssl /`**
    * **`icu/`**  * **`icu /`**
    * **`rust_crates/`**  * **`rust_crates /`**
    * **`...`**  * **`...`**
 * `prebuilt/`  *`prebuilt /`
    * **`chromium/`**  * **铬/`**
    * **`dart/`**  * **飞镖/`**
    * **`flutter/`**  *颤抖/ **
    * **`llvm/`**  * **`llvm /`**
 * `tools/`  *`工具/`
    * `banjo/`  *`班卓琴/`
    * `fidl/bin/backend/{c,cpp,dart,go,llcpp,rust}`  *`fidl / bin / backend / {c，cpp，dart，go，llcpp，rust}`
    * `fidl/bin/frontend/`  *`fidl / bin / frontend /`
    * `fidl/docs/`  *`fidl / docs /`
    * `fidl/examples/`  *`fidl / examples /`
    * `fidl/tests/`  *`fidl / tests /`
 * `src/`  *`src /`
    * `lib/`  *`lib /`
    * `cobalt/`  *`钴/`
    * `component/`  *`component /`
    * `connectivity/`  *`connectivity /`
    * `developer/`  *`开发人员/`
    * **`experiences/`**  * **`经验/`**
    * `graphics/`  *`graphics /`
    * `identity/`  *`identity /`
    * `ledger/`  *`分类帐/`
    * `media/`  *`media /`
    * `modular/`  *`模块化/`
    * `storage/`  *`storage /`
    * `testing/`  *`testing /`
    * `updater/`  *`updater /`
    * `virtualization/`  *虚拟化/
    * `zircon/kernel/`  *`锆石/内核/`
    * `zircon/drivers/`  *`zircon / drivers /`
    * `zircon/userspace/`  *`zircon / userspace /`
 * `vendor/`  *`供应商/`
    * **`[closed-source code from various vendors]`**  * ** [各种供应商的封闭源代码]`**

 
## Evolution  演化 

As the system stabilizes, we can promote areas out of fuchsia.git into separate repositories. Generally, we should promote an area to a separate repository whenthe interface between the area and the rest of the system is sufficiently stable(requires approval by top-level OWNERS). 随着系统的稳定，我们可以将fuchsia.git中的区域推广到单独的存储库中。通常，当区域与系统其余部分之间的接口足够稳定（需要获得顶级OWNERS的批准）时，我们应该将区域提升为一个单独的存储库。

New code can be:  新代码可以是：

 
 * Added to an existing directory in fuchsia.git  *添加到fuchsia.git中的现有目录
 * Added to a new top-level area or subarea of an existing area  *添加到新的顶层区域或现有区域的子区域
 * Added to an existing repository  *添加到现有存储库
