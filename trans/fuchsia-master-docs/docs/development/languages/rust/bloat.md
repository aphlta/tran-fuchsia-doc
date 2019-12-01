Last Refreshed: 2019-09-03  上次刷新：2019-09-03

 
# Measuring Rust Binary Bloat  测量生锈二进制膨胀 

Instructions for analyzing the binary size and composition of Rust programs on Fuchsia. The examples use the `//src/diagnostics/archivist` package. 分析紫红色的Rust程序的二进制大小和组成的说明。这些示例使用`// src / diagnostics / archivist`包。

 
## Prerequisites  先决条件 

 
* [cargo-bloat](#cargo-bloat)  * [货膨胀]（货膨胀）
* [fargo](#fargo)  * [fargo]（fargo）
* [Run `fx build`](#run-a-build)  * [运行`fx build`]（运行一个build）
* [Create Cargo.toml](#create-cargotoml)  * [创建Cargo.toml]（create-cargotoml）

 
### cargo-bloat  货膨胀 

These instructions cover the installation and use of [cargo-bloat][bloat], a tool for Rust projects inspired by [Bloaty McBloatface][google-bloaty]. 这些说明涵盖[cargo-bloat] [bloat]的安装和使用，这是受[Bloaty McBloatface] [google-bloaty]启发的Rust项目工具。

To install:  安装：

```
cargo install cargo-bloat --features regex-filter [--force]
```
 

If you've installed a previous version or would like to add regex filtering support to an existing installation, you may need to add `--force`. 如果您已经安装了以前的版本，或者想为现有安装添加正则表达式过滤支持，则可能需要添加--force。

 
### fargo  法戈 

This example uses cargo subcommands from crates.io, so you must [install fargo][fargo].  本示例使用来自crates.io的cargo子命令，因此您必须[install fargo] [fargo]。

 
### Run `fx build`  运行`fx build` 

Consult the [fx common tools documentation][fx-common-tools] for information about including the correct binary target in your build args. 有关在构建args中包含正确的二进制目标的信息，请参考[fx通用工具文档] [fx-common-tools]。

Next, run `fx build` within your Fuchsia source directory.  接下来，在您的紫红色源目录中运行`fx build`。

 
### Create Cargo.toml  创建Cargo.toml 

Follow the instructions to [generate a `Cargo.toml` for your project][gen-cargo].  按照说明[为您的项目生成`Cargo.toml`] [gen-cargo]。

 
## Build with fargo  用Fargo构建 

`cargo-bloat` doesn't currently support passing an arbitrary manifest path, you'll need to `cd` to the directory with the generated `Cargo.toml`: `cargo-bloat`当前不支持传递任意清单路径，您需要将`cd`到生成的`Cargo.toml`目录中：

```
cd $FUCHSIA_DIR/src/diagnostics/archivist
```
 

From that directory, ensure you can produce a release build with fargo:  从该目录中，确保可以使用fargo生成发行版本：

```
fargo build --release
```
 

Run the release build from plain fargo first, as cargo-bloat will swallow any build errors.  首先运行从普通fargo发行的版本，因为货膨胀会吞下任何版本错误。

 
## Measure size contributions with cargo-bloat  通过货膨胀测量尺寸贡献 

Once we're sure that fargo can produce a release binary for our target, run cargo-bloat:  一旦我们确定fargo可以为我们的目标生成一个发行二进制文件，请运行cargo-bloat：

```
fargo cargo bloat -- --release -n 5
Compiling ...
Analyzing .../src/../out/cargo_target/x86_64-fuchsia/release/archivist

 File  .text     Size              Crate Name
 1.7%   4.5%  38.0KiB              regex <regex::exec::ExecNoSync as regex::re_trait::Regular...
 1.0%   2.5%  21.4KiB       regex_syntax regex_syntax::ast::parse::ParserI<P>::parse_with_comments
 0.8%   2.1%  17.7KiB fuchsia_component? <fuchsia_component::server::ServiceFs<ServiceObjTy> as...
 0.4%   0.9%   8.0KiB              regex regex::re_unicode::Regex::shortest_match_at
 0.4%   0.9%   7.8KiB                std _ZN9libunwind10CFI_ParserINS_17LocalAddressSpaceEE17paI...
33.8%  89.0% 751.9KiB                    And 6152 smaller methods. Use -n N to show more.
38.0% 100.0% 844.8KiB                    .text section size, the file size is 2.2MiB
```
 

It's important to measure binary size in release, as it can be difficult to predict the impact of changes on debug builds. 测量发行版中的二进制大小非常重要，因为很难预测更改对调试版本的影响。

The `-n 5` arguments limit output to 5 lines. Run `cargo bloat --help` for all options, and see below for several commonly used ones. -n 5参数将输出限制为5行。对所有选项运行`cargo bloat --help`，并在下面查看一些常用选项。

 
### Group functions by crate  按板条箱分组功能 

Use the `--crates` flag to group bloat analysis by an estimate of the source crate:  使用`--crates`标志通过对源条板箱的估计将膨胀分析分组：

```
fargo cargo bloat -- --release -n 5 --crates
Compiling ...
Analyzing .../src/../out/cargo_target/x86_64-fuchsia/release/archivist

 File  .text     Size Crate
13.3%  34.9% 294.8KiB std
 6.3%  16.7% 141.0KiB regex
 5.0%  13.2% 111.3KiB regex_syntax
 2.1%   5.5%  46.1KiB fidl
 1.8%   4.7%  39.5KiB json5
 9.6%  25.1% 212.2KiB And 64 more crates. Use -n N to show more.
38.0% 100.0% 844.8KiB .text section size, the file size is 2.2MiB

Note: numbers above are a result of guesswork. They are not 100% correct and never will be.
```
 

Attributing generic functions to their originating crate is an error-prone heuristic analysis and you should drill down with filters and granular output to confirm any discoveries from crate-groupedoutput. 将通用功能分配给其原始包装箱是易于出错的启发式分析，您应深入研究过滤器和粒度输出，以确认来自包装箱分组输出的发现。

 
### Filter functions  过滤功能 

To drill down into the sources of bloat in a particular crate, you can filter by source crate name or regex over the function name (with the feature flag enabled) with the `--filter` flag: 要深入了解特定包装箱中的膨胀来源，您可以使用`--filter`标志按功能名称（启用了功能标志）按源包装箱名称或正则表达式进行过滤：

```
fargo cargo bloat -- --release -n 5 --filter regex_syntax
Compiling ...
Analyzing .../src/../out/cargo_target/x86_64-fuchsia/release/archivist

File .text     Size        Crate Name
1.0%  2.5%  21.4KiB regex_syntax regex_syntax::ast::parse::ParserI<P>::parse_with_comments
0.3%  0.8%   6.4KiB regex_syntax regex_syntax::ast::parse::ParserI<P>::parse_escape
0.2%  0.5%   3.8KiB regex_syntax <regex_syntax::hir::translate::TranslatorI as regex_syntax::ast...
0.1%  0.2%   1.8KiB regex_syntax <regex_syntax::hir::translate::TranslatorI as regex_syntax::ast...
0.1%  0.2%   1.7KiB regex_syntax regex_syntax::unicode::class
3.4%  9.0%  76.2KiB              And 698 smaller methods. Use -n N to show more.
5.0% 13.2% 111.2KiB              filtered data size, the file size is 2.2MiB
```
 

 

