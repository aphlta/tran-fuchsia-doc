 
# GN in Zircon  锆石中的GN 

This discussion assumes basic familiarity with GN syntax and concepts. [This introduction to GN](intro.md) can provide that background. 本讨论假定您基本熟悉GN语法和概念。 [GN的简介]（intro.md）可以提供该背景知识。

GN uses a templating structure to abstract many of the build details away from the end user.  Below are a subset of the templates the Zircon GN defines,focusing on the ones with which Zircon hackers are most likely to interact. GN使用模板结构从最终用户那里抽象出许多构建细节。以下是Zircon GN定义的模板的子集，重点介绍Zircon黑客最有可能与之交互的模板。

 
## `$zx/` prefix  $ zx /前缀 

**TODO(BLD-353): _This is a hold-over from the "layer cake" design and will probably change soon:_** ** TODO（BLD-353）：_这是“分层蛋糕”设计的保留，可能很快就会改变：_ **

As discussed in [the introduction](intro.md), GN uses "source-absolute" paths that look like `//a/b/c`.  In the Zircon GN files, we **never** use `//`.Instead, use `$zx/foo` to refer to `//zircon/foo`,e.g. `"$zx/system/ulib/zircon"`. 如[简介]（intro.md）中所讨论的，GN使用看起来像“ // a / b / c”的“绝对源”路径。在Zircon GN文件中，我们从未使用`//`，而是使用$ zx / foo来引用`// zircon / foo`，例如““ $ zx / system / ulib / zircon”。

 
## `executable()` and `test()`  `executable（）`和`test（）` 

The primary target type in producing a binary is `executable()`.  This produces an executable binary from the listed sources.  The Zircon build also provides ameans to indicate the location in the image wherein that binary should beinstalled via the `install_path` variable in the target scope.`install_path` can be: 产生二进制文件的主要目标类型是`executable（）`。这将从列出的源生成可执行二进制文件。 Zircon版本还提供了一些手段来指示映像中应通过目标作用域中的install_path变量安装二进制文件的位置。install_path可以是：

 
 * a string: the path relative to the root of the BOOTFS (with no leading `/`)  *字符串：相对于BOOTFS根目录的路径（不带前导`/`）
 * omitted: use the default path of `bin/<binary_name>`  *省略：使用默认路径`bin / <binary_name>`
 * `false`: do not install this file at all  *`false`：完全不安装此文件

The build also provides a `test()` target, which is identical to `executable()` except that it sets `testonly = true` and that its default`install_path` is `test/<binary_name>` instead of `bin/<binary_name>`. 该构建还提供了一个“ test（）”目标，该目标与“ executable（）”相同，除了它设置“ testonly = true”，并且其默认的“ install_path”是“ test / <binary_name>”而不是“ bin /”。 <binary_name>`。

`test()` can be used for a test program that runs on Zircon or for a test program that runs on the host side.  In fact, the same `test()` target canserve to build the same test program for both situations with no extra workrequired.  (It's just what dependency paths reach that target that willdetermine whether it's built for host or for Zircon or for both.) test（）可用于在Zircon上运行的测试程序或在主机端运行的测试程序。实际上，相同的`test（）`目标可以为两种情况构建相同的测试程序，而无需额外的工作。 （正是依赖路径到达该目标的方式将确定它是为主机还是Zircon还是为两者而构建。）

 
## `library()`  `library（）` 

The `library()` template is for any kind of "library" in the Zircon tradition, whether for the kernel, Zircon user code, or host-side code.  The basic thingit means to be a "library" is that there is an `include/` subdirectory ofpublic header files.  Dependents that list this `library()` target in their`deps` will automatically get `-I` switches for that `include/` directory. `library（）`模板适用于Zircon传统中的任何类型的“库”，无论是内核，Zircon用户代码还是主机端代码。成为“库”的基本含义是公共头文件有一个“ include /”子目录。在其`deps`中列出该`library（）`目标的依赖者将自动为该`include /`目录获得-I开关。

The default case with the most concise syntax is a static-only userland library.  Making a library available as a shared library just requires addingthe line `shared = true`.  Likewise, making a library available for host-sideuse just requires adding the line `host = true`.  These are in addition to thedefault `static = true` that makes the library available for userland staticlinking.  For a library that should *never* be statically linked (aside fromhost-side or kernel uses), you can override the default with `static = false`. 语法最简洁的默认情况是纯静态用户态库。使一个库作为共享库可用仅需要添加行“ shared = true”。同样，使库可用于主机端仅需添加“ host = true”行。这些是默认的“ static = true”的补充，该默认值使库可用于用户级静态链接。对于不应该静态链接的库（除了主机端或内核使用），可以使用static = false覆盖默认值。

For a library in the kernel, set `kernel = true`.  This is the same whether it's a kernel-only library, or is code shared between kernel and user (and/orhost).  Setting `kernel = true` changes the default to `static = false`, so ifa library can be used either in the kernel or in userland, then you must set`static = true` explicitly alongside `kernel = true` (unless you set `shared =true` and want to prohibit static linking of that library in userland). 对于内核中的库，设置`kernel = true'。无论是仅内核的库还是在内核与用户（和/或主机）之间共享的代码，这都是相同的。设置`kernel = true`会将默认值更改为`static = false`，因此，如果一个库可以在内核或用户环境中使用，则必须在`kernel = true`旁边显式设置`static = true`（除非您进行了设置） `shared = true`，并希望禁止在userland中静态链接该库）。

Note: For kernel modules that do not provide an `include/` subdirectory, use [`source_set()`](#source_set) instead of `library()`. 注意：对于不提供“ include /”子目录的内核模块，请使用[`source_set（）`]（source_set）而非“ library（）”。

Here’s an exemplar showing all the essential options.  Most actual targets will be little more than a `sources` list and a `deps` list. 这是显示所有基本选项的示例。大多数实际目标只会是一个“源”列表和一个“ deps”列表。

```gn
library("foo") {
  # Builds "libfoo.a" when static, "libfoo.so" when shared.

  static = true  # default, omitted unless kernel = true: build userland libfoo.a
  shared = true  # false if omitted: build userland libfoo.so
  kernel = true  # false if omitted: can be used from kernel
  host = true  # false if omitted: can be used in host tools

  sources = [
    "foo.c",
    "bar.cpp",
  ]

  deps = [
    # Can refer here to `source_set()` or other `library()` targets defined
    # locally.
    ":foo_minimal",  # Defined in this same BUILD.gn file.
    "foobar_subsystem",  # Defined in foobar_subsystem/BUILD.gn relative to here.

    # Explicitly link in static libbar.a even if libbar.so is available.
    "$zx/system/ulib/bar:static",

    # Be explicit about getting libbaz.so as a shared library.
    "$zx/system/ulib/baz:shared",

    # Compile with -Isystem/ulib/bozo/include, but don't link anything in.
    # This should usually not be used in `deps`, but only in `public_deps`.
    # See below.
    "$zx/system/ulib/bozo:headers",

    # Let system/ulib/quux/BUILD.gn decide whether static or shared is the
    # norm for that library.  (So far the defining `library()` will always
    # prefer the shared library if it's enabled; it would be easy to add the
    # option to build shared but default to static if that's ever useful.)
    "$zx/system/ulib/quux",

    # `library("quextras")` appears in system/ulib/quux/BUILD.gn because quux
    # and quextras want to share some private source code or for whatever
    # reason we've decided putting them in a single directory is right.
    # Because we're not using the target with the name of its directory,
    # the `:name` syntax selects the specific target within that BUILD.gn file.
    # For the derived target names, we use `.` before the suffix.
    # In fact, "quux:headers" is just an alias for "quux:quux.headers", etc.
    "$zx/system/ulib/quux:quextras",
    "$zx/system/ulib/quux:quextras_more.static",
    "$zx/system/ulib/quux:quextras_way_more.shared",

    # This is a `library()` that will set `static=false shared=true`
    # so `zircon:static` here wouldn't work but `zircon:shared` would work.
    "$zx/system/ulib/zircon",
  ]

  # Per-module compilation flags are always optional.
  # *Note*: For cases where the flag order matters, it may be necessary
  # to use a config() instead.
  cflags = [ "-Wfoo", "-fbar" ]
  cflags_cc = [ "-fonly-for-c++" ]
  cflags_c = [ "-fonly-for-c" ]
  asmflags = [ "-Wa,--some-as-switch" ]
  ldflags = [ "-Wl,--only-affects-shlib-link" ]
}
```
 

A heavily abridged real-world example of a kernel module:  内核模块的大量实际示例：

```gn
# deps = [ "$zx/kernel/object" ] gets -Ikernel/object/include
library("object") {
  kernel = true
  sources = [
    "buffer_chain.cpp",
    "process_dispatcher.cpp",
  ]
  deps = [
    "$zx/kernel/dev/interrupt",
    "$zx/system/ulib/fbl",
  ]
}
```
 

Note `system/ulib/fbl` is not `kernel/lib/fbl`: the one `fbl` serves all. Here's a heavily abridged example for that case: 注意`system / ulib / fbl`不是`kernel / lib / fbl`：一个`fbl`服务所有。这是该情况的一个精简示例：

```gn
library("fbl") {
  kernel = true
  static = true
  sources = [
    "alloc_checker.cpp",
  ]
  if (is_kernel) {
    sources += [
      "arena.cpp",
      "arena_tests.cpp",
    ]
  } else {
    sources += [ "string.cpp" ]
  }
}
```
 

The actual `fbl` is a bad example because it has other complications, but this demonstrates how a library of shared code can be maintained in one place withone `BUILD.gn` file using one library target to describe both the kernel anduserland incarnations.  They share everything, but can differ as needed basedon `is_kernel` conditionals. 实际的`fbl`是一个不好的例子，因为它还有其他复杂性，但这说明了如何使用一个库目标描述一个内核和用户化身，使用一个`BUILD.gn`文件就可以在一个地方维护共享代码的库。它们共享所有内容，但根据`is_kernel`条件可以根据需要而有所不同。

Libraries define a standard set of targets (if relevant):  图书馆定义了一组标准的目标（如果相关）：

 
 * `$target_name.headers` is always provided, for just getting the headers and not linking it in *始终提供`$ target_name.headers`，仅用于获取标题而不将其链接到
 * `$target_name.static` is provided if `static = true` (the default) *如果`static = true`（默认），则提供`$ target_name.static`。
 * `$target_name.shared` is provided if `shared = true` *如果`shared = true`则提供`$ target_name.shared`

If the library is the main target in the file (e.g. `$zx/foo:foo`)--the common case--the `static`, `shared`, and `headers` sub-targets are aliased into`$zx/foo:static`, `$zx/foo:shared`, and `$zx/foo:headers`. 如果库是文件中的主要目标（例如$ zx / foo：foo）（通常情况），则static，shared和header子目标都将别名为$ zx。 / foo：static`，$ zx / foo：shared和$ zx / foo：headers。

 
### `public_deps` for header dependencies  `public_deps`用于头文件依赖 

In addition to `deps` and `data_deps`, GN also has `public_deps`. This is used when a target exposes a dependency in its public header files and needs toforward that dependency's settings up the dependency chain. Every use of`public_deps` should have a comment explaining why it's needed: 除了`deps`和`data_deps`，GN还具有`public_deps`。当目标在其公共头文件中公开依赖项并且需要转发该依赖项的依赖关系链时，将使用此方法。每次对public_deps的使用都应有一条注释，说明为什么需要这样做：

For example, `library("async-loop")` contains this:  例如，`library（“ async-loop”）`包含以下内容：

```gn
  public_deps = [
    # <lib/async-loop/loop.h> has #include <lib/async/dispatcher.h>.
    "$zx/system/ulib/async:headers",
  ]
```
 

 
## `source_set()` and `static_library()`  `source_set（）`和`static_library（）` 

Some code that doesn't have an include directory can just use the native GN `source_set()` or `static_library()` targets. 某些没有包含目录的代码只能使用本机GN`source_set（）`或`static_library（）`目标。

A source set (see `gn help source_set`) is a way to create a logical grouping of files or to scope compilation switches narrowly. The object files will belinked directly into final binaries without going through any intermediatelibraries. In contrast, the files in a static library are only pulled inas-needed to resolve symbols. 源集（请参阅gn help source_set）是一种创建文件的逻辑分组或缩小范围的编译开关的方法。目标文件将直接链接到最终二进制文件，而无需通过任何中间库。相比之下，静态库中的文件仅按需要提取以解析符号。

 
  * Code in the kernel itself should always use `source_set`. Static libraries currently interact poorly with inline assembly (Googlers see bug124318741). *内核中的代码应始终使用`source_set`。当前，静态库与内联汇编的交互性较差（Google员工请参见bug124318741）。

 
  * A `source_set` *must* be used when creating groups of tests since the test harness depends on static initializers while the static librarylinking rules will strip the tests. All kernel code. *创建测试组时必须使用`source_set` *，因为测试工具依赖于静态初始化程序，而静态库链接规则将剥离测试。所有内核代码。

 
  * A `static_library` should be used for higher-level things that looks like libraries or a part of one. The dead code stripping is more efficient which canproduce faster links and smaller binaries in cases where some code isn'tneeded. *“ static_library”应用于看起来像库或其中一部分的更高级的东西。死代码剥离效率更高，在不需要某些代码的情况下，可以产生更快的链接和更小的二进制文件。

```gn
source_set("some_code") {
  sources = [
    "this.c",
    "that.cpp",
  ]
}
```
 

 
## `loadable_module()`  `loadable_module（）` 

This is not really used in the Zircon build so far, but could be. A loadable module is a shared object that's not linked directly but rather loadeddynamically via `dlopen()` or the like. 到目前为止，Zircon版本中并未真正使用过，但是可能会使用。可加载模块是一个共享的对象，它不是直接链接的，而是通过dlopen（）等动态加载的。

`loadable_module()` takes the `install_path` parameter like `executable()` does.  But it has no default path, so it's like `install_path = false` unlessyou supply a path explicitly. `loadable_module（）`接受`install_path`参数，就像`executable（）`一样。但是它没有默认路径，因此除非您明确提供了路径，否则它类似于install_path = false。

Zircon device drivers are loadable modules, but they have their own special templates that should be used instead of `loadable_module()`. Zircon设备驱动程序是可加载模块，但是它们具有自己的特殊模板，而不是`loadable_module（）`。

 
## `driver()` and `test_driver()`  `driver（）`和`test_driver（）` 

Drivers are loadable modules with some special support and constraints.  驱动程序是可加载模块，具有一些特殊的支持和约束。

 
 * They get a default `install_path` appropriate for drivers, so they will be found by `devmgr`. *它们会得到适合驱动程序的默认`install_path`，因此它们会被`devmgr`找到。
 * They implicitly depend on `libdriver` so it shouldn't be listed in `deps`.  *它们隐式依赖于`libdriver`，因此不应在`deps`中列出。
 * They implicitly use the static C++ standard library.  *他们隐式使用静态C ++标准库。

`test_driver()` is to `driver()` as `test()` is to `executable()`.  test_driver（）是驱动程序（test）可执行文件（executable）。

```gn
driver("fvm") {
  sources = [
    "fvm.cpp",
  ]
  deps = [
    "$zx/system/ulib/ddktl",
    "$zx/system/ulib/fs",
    "$zx/system/ulib/zircon",
  ]
}
```
 

 
### `resources()` and `firmware()`  `resources（）`和`firmware（）` 

A `resource()` target declares some file that might be needed in the BOOTFS image, but doesn’t directly cause anything to happen in the build.  The styleof the rule is as if it’s a copy from a source file to an output file in thebuild; it’s modelled on GN’s native `copy()` rule, and `gn help copy` explainswhy its syntax is exactly the way it is.  `outputs` is single-element listcontaining a path in the BOOTFS. 一个“ resource（）”目标声明了BOOTFS映像中可能需要的一些文件，但不会直接导致构建中发生任何事情。规则的样式就像是从源文件到构建中输出文件的副本一样；它以GN的本机“ copy（）”规则为模型，而“ gn help copy”则说明了为什么其语法确实如此。 `outputs`是包含BOOTFS中路径的单元素列表。

```gn
import("$zx/public/gn/resource.gni")

resource("tables") {
  sources = [
    "data.tbl",
  ]
  outputs = [
    "data/some_lib/data_v1.tbl",
  ]
}
```
 

The purpose of `resource()` is to be listed in the `data_deps` of the target that uses the data: “ resource（）”的目的将在使用数据的目标的“ data_deps”中列出：

```gn
library("uses_tables") {
  sources = [
    "read_table.cc",
  ]
  data_deps = [
    ":tables",
  ]
}
```
 

This can be a `library()`, an `executable()`, a `source_set()`, etc.  Good practice is to put the `data_deps` in the finest-grained target that holds thecode that uses the file at runtime.  Doing so ensures that the relevantresource will be available at runtime. 这可以是一个“ library（）”，“ executable（）”，“ source_set（）”等。好的做法是将“ data_deps”放到最细粒度的目标中，该目标中包含在运行时使用该文件的代码。这样做可以确保相关资源在运行时可用。

If the resource is generated by the build, then the path in the `sources` list identifies its location in the build directory, usually using`$target_out_dir` or `$target_gen_dir`.  In that case, the `resource()` mustalso have a `deps` list that includes the target that generates that file. 如果资源是由构建生成的，则“源”列表中的路径通常使用$ target_out_dir或$ target_gen_dir标识其在构建目录中的位置。在这种情况下，`resource（）`还必须具有`deps`列表，其中包括生成该文件的目标。

The build also allows for a special type of resource that is generated from the dependency graph.  Using `generated_resource()` creates a resource filethat is intended for use in `data_deps`, as in a normal `resource()`, butinstead of using an existing source file it will generate a file at `gn gen`time with fixed contents or based on a metadata collection (see `gn helpgenerated_file` for details). 该构建还允许从依赖关系图生成特殊类型的资源。与通常的`resource（）`一样，使用`generated_resource（）`创建一个旨在供`data_deps`使用的资源文件，但不是使用现有的源文件，而是在`gn gen`时生成具有固定内容的文件。或基于元数据集合（有关详细信息，请参见gn helpgenic_file）。

`firmware()` is a special-case variant of `resource()`, intended for drivers. It places the resource in `/lib/firmware/$path`, where `$path` is a relativepath to the resource in the `/lib/firmware` root.  This mimics the callingconvention in `devhost`, where a driver calls `load_firmware(...)` on arelative path. `firmware（）`是`resource（）`的一种特殊情况，用于驱动程序。它将资源放置在/ lib / firmware / $ path中，其中$ path是相对于/ lib / firmware根目录中资源的相对路径。这模仿了`devhost`中的callingconvention，其中驱动程序在相对路径上调用`load_firmware（...）`。

 
## `fidl_library()`  `fidl_library（）` 

This template allows the definition of a FIDL library and its associated bindings.  Declaring a `fidl_library()` target will cause the build togenerate bindings for all supported languages. 该模板允许定义FIDL库及其关联的绑定。声明一个`fidl_library（）`目标将导致构建生成所有受支持语言的绑定。

Note: To use this template, you must import the `fidl.gni` file scope.  注意：要使用此模板，您必须导入`fidl.gni`文件作用域。

```gn
import("$zx/public/gn/fidl.gni")

# Defined in $zx/system/fidl/fuchsia-io/BUILD.gn
fidl_library("fuchsia-io") {
  sources = [
    "io.fidl",
  ]
  public_deps = [
    "$zx/system/fidl/fuchsia-mem",
  ]
}
```
 

Note the use of [`public_deps`](#public_deps).  When a FIDL library's source files have `using other_library;` that's equivalent to a C/C++ library using`#include <other_library/header>` in its public headers.  Since this is verycommon for FIDL (and Banjo) libraries, we don't require comments on every casewhen it follows this simple pattern. 注意使用[`public_deps`]（public_deps）。当FIDL库的源文件具有“ using other_library;”功能时，等效于C / C ++库，在其公共头文件中使用“ include <other_library / header>”。由于这在FIDL（和Banjo）库中很常见，因此在遵循这种简单模式时，我们不需要在每种情况下都添加注释。

Depending on which bindings are defined, the above example will generate a set of targets of the form `$zx/system/fidl/fuchsia-io:fuchsia-io.<language>`, or,in the case where the target name is the same as the directory name as above,`$zx/system/fidl/fuchsia-io:<language>`. 根据定义的绑定，上面的示例将生成一组目标，形式为`$ zx / system / fidl / fuchsia-io：fuchsia-io。<language>`，或者，如果目标名称为与上面的目录名称相同，即$ zx / system / fidl / fuchsia-io：<语言>。

The common case today is `"$zx/system/fidl/fuchsia-io:c"`.  今天的常见情况是““ $ zx / system / fidl / fuchsia-io：c”`。

 
## `banjo_library()`  banjo_library（） 

The definition of Banjo libraries is similar to that of FIDL libraries.  A `banjo_libary()` target will generate bindings for all supported languages,though the set of supported languages will be different from that of FIDL. Banjo库的定义与FIDL库的定义相似。一个`banjo_libary（）`目标将为所有支持的语言生成绑定，尽管支持的语言集将与FIDL的语言集不同。

```gn
import("$zx/public/gn/banjo.gni")

banjo_library("ddk-driver") {
  sources = [
    "driver.banjo",
  ]
}
```
 

Currently, listing the plain target with no `:<language>` suffix in `deps` gets both the C and C++ bindings.  This will probably change in the nearfuture to more closely follow the FIDL model: specify exactly which bindingsyou depend on. 当前，在`deps`中列出没有后缀'：<language>`的普通目标既可以获取C绑定，也可以获取C ++绑定。这可能会在不久的将来发生变化，以更紧密地遵循FIDL模型：准确指定您所依赖的绑定。

