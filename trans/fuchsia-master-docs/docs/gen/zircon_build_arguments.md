 
# GN Build Arguments  GN构建参数 

 
## All builds  所有版本 

 
### asan_default_options  asan_default_optionsDefault [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) options (before the `ASAN_OPTIONS` environment variable is read atruntime).  This can be set as a build argument to affect most "asan"variants in $variants (which see), or overridden in $toolchain_args inone of those variants.  Note that setting this nonempty may conflictwith programs that define their own `__asan_default_options` Cfunction. 默认[AddressSanitizer]（https://clang.llvm.org/docs/AddressSanitizer.html）选项（在运行时读取ASAN_OPTIONS环境变量之前）。可以将其设置为build参数，以影响$ variants中的大多数“ asan”变量（请参见），或在这些变量之一的$ toolchain_args中覆盖。请注意，设置此非空值可能与定义自己的__asan_default_options C函数的程序冲突。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //public/gn/config/instrumentation/BUILD.gn:15  来自//public/gn/config/instrumentation/BUILD.gn:15

 
### assert_level  assert_level 
* 0 means no assertions, not even standard C `assert()`.  * 0表示没有断言，甚至没有标准C`assert（）`。
* 1 means `ZX_ASSERT` but not `ZX_DEBUG_ASSERT`.  * 1表示`ZX_ASSERT`，而不是`ZX_DEBUG_ASSERT`。
* 2 means both `ZX_ASSERT` and  `ZX_DEBUG_ASSERT`.  * 2表示`ZX_ASSERT`和`ZX_DEBUG_ASSERT`。

**Current value (from the default):** `2`  **当前值（默认值）：** 2

From //public/gn/config/levels.gni:9  来自//public/gn/config/levels.gni:9

 
### build_id_dir  build_id_dirDirectory to populate with `xx/yyy` and `xx/yyy.debug` links to ELF files.  For every ELF binary built, with build ID `xxyyy` (lowercasehexadecimal of any length), `xx/yyy` is a hard link to the strippedfile and `xx/yyy.debug` is a hard link to the unstripped file.Symbolization tools and debuggers find symbolic information this way. 用`xx / yyy`和`xx / yyy.debug`链接到ELF文件的目录。对于每个构建的ELF二进制文件，其构建ID为``xxyyy''（任意长度的小写十六进制），``xx / yyy''是指向strippedfile的硬链接，而``xx / yyy.debug''是指向未压缩文件的硬链接。调试器以这种方式查找符号信息。

**Current value (from the default):** `"/b/s/w/ir/k/out/build-zircon/.build-id"`  **当前值（默认值）：**`“ /b/s/w/ir/k/out/build-zircon/.build-id”`

From //public/gn/toolchain/c_toolchain.gni:18  来自//public/gn/toolchain/c_toolchain.gni:18

 
### clang_tool_dir  clang_tool_dirDirectory where the Clang toolchain binaries ("clang", "llvm-nm", etc.) are found.  If this is "", then the behavior depends on $use_prebuilt_clang.This toolchain is expected to support both Fuchsia targets and the host. 找到Clang工具链二进制文件的目录（“ clang”，“ llvm-nm”等）。如果这是“”，则行为取决于$ use_prebuilt_clang。此工具链有望同时支持Fuchsia目标和主机。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //public/gn/toolchain/clang.gni:16  来自//public/gn/toolchain/clang.gni:16

 
### crash_diagnostics_dir  crash_diagnostics_dirClang crash reports directory path. Use empty path to disable altogether.  Clang崩溃报告目录路径。使用空路径将其完全禁用。

**Current value (from the default):** `"/b/s/w/ir/k/out/build-zircon/clang-crashreports"`  **当前值（默认值）：**`“ / b / s / w / ir / k / out / build-zircon / clang-crashreports”`

From //public/gn/config/BUILD.gn:12  来自//public/gn/config/BUILD.gn:12

 
### current_cpu  current_cpu 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

 
### current_os  current_os 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

 
### default_deps  default_depsDefines the `//:default` target: what `ninja` with no arguments does.  定义`//：default`目标：不带参数的`ninja`做什么。

**Current value (from the default):** `[":build-tests", ":ids", ":images", "tools"]`  **当前值（默认值）：**`[“：build-tests”，“：ids”，“：images”，“ tools”]`

From //BUILD.gn:21  来自//BUILD.gn:21

 
### detailed_scheduler_tracing  detail_scheduler_tracingEnable detailed scheduler traces.  启用详细的调度程序跟踪。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //kernel/params.gni:38  来自//kernel/params.gni:38

 
### driver_unittest_log_flags  driver_unittest_log_flagsLog levels to be printed when logs are enabled. Default is ERROR, WARNING, & INFO. Refer to zircon/system/public/zircon/syscalls/log.h for levels. 启用日志后要打印的日志级别。默认值为错误，警告，信息。有关级别，请参考zircon / system / public / zircon / syscalls / log.h。

**Current value (from the default):** `"0x7"`  **当前值（默认值）：**`“ 0x7”`

From //system/dev/lib/fake_ddk/BUILD.gn:11  来自//system/dev/lib/fake_ddk/BUILD.gn:11

 
### enable_acpi_debug  enable_acpi_debugEnable debug output in the ACPI library (used by the ACPI bus driver).  在ACPI库中启用调试输出（由ACPI总线驱动程序使用）。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //third_party/lib/acpica/BUILD.gn:9  来自//third_party/lib/acpica/BUILD.gn:9

 
### enable_driver_unittest_logs  enable_driver_unittest_logsEnable printing of in driver logs in unittests.  在单元测试中启用驱动程序日志中的打印。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //system/dev/lib/fake_ddk/BUILD.gn:7  来自//system/dev/lib/fake_ddk/BUILD.gn:7

 
### enable_fair_scheduler  enable_fair_schedulerEnable fair scheduler by default on all architectures.  默认情况下，在所有体系结构上启用公平调度程序。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //kernel/params.gni:35  来自//kernel/params.gni:35

 
### enable_kernel_debugging_features  enable_kernel_debugging_featuresWhether to include various features (non-shipping, insecure, etc.) in the netsvc build. 是否在netsvc构建中包括各种功能（非运输，不安全等）。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //public/gn/config/product_parameters.gni:12  来自//public/gn/config/product_parameters.gni:12

 
### enable_lock_dep  enable_lock_depEnable kernel lock dependency tracking.  启用内核锁依赖项跟踪。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //kernel/params.gni:32  来自//kernel/params.gni:32

 
### enable_lock_dep_tests  enable_lock_dep_testsEnable kernel lock dependency tracking tests.  By default this is enabled when tracking is enabled, but can also be eanbled independentlyto assess whether the tests build and *fail correctly* when lockdep isdisabled. 启用内核锁依赖项跟踪测试。默认情况下，启用跟踪时会启用此功能，但也可以独立启用该功能，以评估禁用lockdep时测试是否正确建立并“失败”。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //kernel/params.gni:53  来自//kernel/params.gni:53

 
### enable_netsvc_debugging_features  enable_netsvc_debugging_features 

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //public/gn/config/product_parameters.gni:13  来自//public/gn/config/product_parameters.gni:13

 
### enable_user_pci  enable_user_pciEnable userspace PCI and disable kernel PCI.  启用用户空间PCI并禁用内核PCI。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //kernel/params.gni:41  来自//kernel/params.gni:41

 
### gcc_tool_dir  gcc_tool_dirDirectory where the GCC toolchain binaries ("gcc", "nm", etc.) are found.  If this is "", then the behavior depends on $use_prebuilt_gcc.This directory is expected to contain `aarch64-elf-*` and `x86_64-elf-*`tools used to build for the Fuchsia targets.  This directory will notbe used for host tools; if GCC is selected for host builds, only thesystem-installed tools found by the shell via `PATH` will be used. 找到GCC工具链二进制文件（“ gcc”，“ nm”等）的目录。如果为“”，则行为取决于$ use_prebuilt_gcc。此目录应包含用于为紫红色目标构建的`aarch64-elf- *`和`x86_64-elf- *`工具。该目录将不用于宿主工具；如果为主机构建选择了GCC，则仅使用Shell通过`PATH`找到的系统安装工具。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //public/gn/toolchain/gcc.gni:19  来自//public/gn/toolchain/gcc.gni:19

 
### goma_dir  goma_dirDirectory containing the Goma source code.  This can be a GN source-absolute path ("//...") or a system absolute path. 包含戈马源代码的目录。这可以是GN源绝对路径（“ // ...”）或系统绝对路径。

**Current value (from the default):** `"/home/swarming/goma"`  **当前值（默认值）：**`“ / home / swarming / goma”`

From //public/gn/toolchain/goma.gni:13  来自//public/gn/toolchain/goma.gni:13

 
### host_cpu  host_cpu 

**Current value (from the default):** `"x64"`  **当前值（默认值）：**`“ x64”`

 
### host_os  host_os 

**Current value (from the default):** `"linux"`  **当前值（默认值）：**`“ linux”`

 
### kernel_aspace_base  kernel_aspace_base 

**Current value (from the default):** `"0xffff000000000000"`  **当前值（默认值）：**`“ 0xffff000000000000”`

From //kernel/params.gni:26  来自//kernel/params.gni:26

 
### kernel_base  kernel_base 

**Current value (from the default):** `"0xffffffff00000000"`  **当前值（默认值）：**`“ 0xffffffff00000000”`

From //kernel/params.gni:18  来自//kernel/params.gni:18

 
### kernel_extra_defines  kernel_extra_definesExtra macro definitions for kernel code, e.g. "DISABLE_KASLR", "ENABLE_KERNEL_LL_DEBUG". 内核代码的额外宏定义，例如“ DISABLE_KASLR”，“ ENABLE_KERNEL_LL_DEBUG”。

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //kernel/params.gni:45  来自//kernel/params.gni:45

 
### kernel_version_string  kernel_version_stringVersion string embedded in the kernel for `zx_system_get_version`. If set to the default "", a string is generated based on theZircon git revision of the checkout. 嵌入在内核中的版本字符串，用于“ zx_system_get_version”。如果设置为默认的“”，则基于签出的Zircon git版本生成一个字符串。

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

From //kernel/lib/version/BUILD.gn:9  来自//kernel/lib/version/BUILD.gn:9

 
### malloc  分配 

**Current value (from the default):** `"scudo"`  **当前值（默认值）：**`“ scudo”`

From //third_party/ulib/musl/BUILD.gn:6  来自//third_party/ulib/musl/BUILD.gn:6

 
### opt_level  opt_level 
* -1 means really unoptimized (-O0), usually only build-tested and not run.  * -1表示实际上未优化（-O0），通常仅经过构建测试且不能运行。
* 0 means "optimized for debugging" (-Og), light enough to avoid confusion.  * 0表示“已针对调试进行了优化”（-Og），足够轻便可以避免混淆。
  1, 2, and 3 are increasing levels of optimization.  1、2和3正在提高优化水平。
* 4 is optimized for space rather than purely for speed.  * 4针对空间进行了优化，而不是单纯针对速度进行了优化。

**Current value (from the default):** `2`  **当前值（默认值）：** 2

From //public/gn/config/levels.gni:15  来自//public/gn/config/levels.gni:15

 
### smp_max_cpus  smp_max_cpus 

**Current value (from the default):** `16`  **当前值（默认值）：**`16`

From //kernel/params.gni:10  来自//kernel/params.gni:10

 
### symbol_level  symbol_level 
* 0 means no debugging information.  * 0表示没有调试信息。
* 1 means minimal debugging information sufficient to symbolize backtraces.  * 1表示最少的调试信息，足以象征回溯。
* 2 means full debugging information for use with a symbolic debugger.  * 2表示与符号调试器一起使用的完整调试信息。

**Current value (from the default):** `2`  **当前值（默认值）：** 2

From //public/gn/config/levels.gni:20  来自//public/gn/config/levels.gni:20

 
### sysroot  sysrootThe `--sysroot` directory for host compilations. This can be a string, which only applies to $host_os-$host_cpu.Or it can be a list of scopes containing `cpu`, `os`, and `sysroot`.The empty list (or empty string) means don't use `--sysroot` at all. 主机编译的目录--sysroot。它可以是仅适用于$ host_os- $ host_cpu的字符串，也可以是包含`cpu`，`os`和`sysroot`的作用域列表。空列表（或空字符串）表示不包含完全使用`--sysroot`。

```
[{
  cpu = "arm64"
  os = "linux"
  sysroot = "//../prebuilt/third_party/sysroot/linux-arm64"
}, {
  cpu = "x64"
  os = "linux"
  sysroot = "//../prebuilt/third_party/sysroot/linux-x64"
}]
```
**Current value (from the default):**  **当前值（默认值）：**

From //public/gn/config/BUILD.gn:18  来自//public/gn/config/BUILD.gn:18

 
### target_cpu  target_cpu 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

 
### target_os  target_os 

**Current value (from the default):** `""`  **当前值（默认值）：**`“”`

 
### tests_in_image  tests_in_imageWhether to include all the Zircon tests in the main standalone ZBI. TODO(mcgrathr): This will be replaced by a more sophisticated plan forwhat images to build rather than a single "everything" image that needsto be pared down. 是否在主独立ZBI中包括所有Zircon测试。 TODO（mcgrathr）：将由更复杂的计划来取代要构建的图像，而不是需要缩减的单个“所有”图像。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //BUILD.gn:18  来自//BUILD.gn:18

 
### thinlto_cache_dir  Thinlto cache_dirThinLTO cache directory path.  ThinLTO缓存目录路径。

**Current value (from the default):** `"host-arm64-linux-lto/thinlto-cache"`  **当前值（默认值）：**`“ host-arm64-linux-lto / thinlto-cache”`

From //public/gn/config/lto/BUILD.gn:22  来自//public/gn/config/lto/BUILD.gn:22

 
### thinlto_jobs  thinlto_jobsNumber of parallel ThinLTO jobs.  并行ThinLTO作业的数量。

**Current value (from the default):** `8`  **当前值（默认值）：** 8

From //public/gn/config/lto/BUILD.gn:19  来自//public/gn/config/lto/BUILD.gn:19

 
### toolchain  工具链*This must never be set as a build argument.* It exists only to be set via c_toolchain().See environment() for more information. *绝不能将其设置为构建参数。*仅可通过c_toolchain（）进行设置。有关更多信息，请参见environment（）。

```
{
  configs = []
  environment = "stub"
  globals = { }
  label = "//public/gn/toolchain:stub"
}
```
**Current value (from the default):**  **当前值（默认值）：**

From //public/gn/BUILDCONFIG.gn:20  来自//public/gn/BUILDCONFIG.gn:20

 
### use_ccache  use_ccacheSet to true to enable compiling with ccache.  设置为true以启用使用ccache进行编译。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //public/gn/toolchain/ccache.gni:9  来自//public/gn/toolchain/ccache.gni:9

 
### use_goma  use_gomaSet to true to enable distributed compilation using Goma.  设置为true以启用使用Goma的分布式编译。

**Current value (from the default):** `false`  **当前值（默认值）：** false

From //public/gn/toolchain/goma.gni:9  来自//public/gn/toolchain/goma.gni:9

 
### use_prebuilt_clang  use_prebuilt_clangIf $clang_tool_dir is "", then this controls how the Clang toolchain binaries are found.  If true, then the standard prebuilt is used.Otherwise the tools are just expected to be found by the shell via `PATH`. 如果$ clang_tool_dir为“”，则这将控制如何找到Clang工具链二进制文件。如果为true，则使用标准的预建标准，否则将仅通过shell通过PATH找到这些工具。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //public/gn/toolchain/clang.gni:11  来自//public/gn/toolchain/clang.gni:11

 
### use_prebuilt_gcc  use_prebuilt_gccIf $gcc_tool_dir is "", then this controls how the GCC toolchain binaries are found.  If true, the standard prebuilt is used.  If false,the tools are just expected to be found in PATH. 如果$ gcc_tool_dir为“”，则这将控制如何找到GCC工具链二进制文件。如果为true，则使用标准的预构建。如果为false，则只能在PATH中找到该工具。

**Current value (from the default):** `true`  **当前值（默认值）：** true

From //public/gn/toolchain/gcc.gni:11  来自//public/gn/toolchain/gcc.gni:11

 
### variants  变体List of "selectors" to request variant builds of certain targets.  Each selector specifies matching criteria and a chosen variant.  The firstselector in the list to match a given target determines which variant isused for that target. “选择器”列表，用于请求某些目标的变体版本。每个选择器都指定匹配条件和所选变体。列表中与给定目标匹配的firstselector确定该目标使用哪个变体。

The $default_variants list is appended to the list set here.  So if no selector set in $variants matches (e.g. if the list is empty, as is thedefault), then the first match in $default_variants chooses the variant. $ default_variants列表将追加到此处设置的列表中。因此，如果$ variants中没有设置的选择器匹配（例如，如果列表为空，则默认为空），则$ default_variants中的第一个匹配项将选择变量。

Each selector is either a string or a scope.  A selector that's a string is a shorthand that gets expanded to a full selector (a scope); the fullselector form is described below. 每个选择器都是字符串或范围。作为字符串的选择器是将其扩展为完整选择器（范围）的简写；全选器的形式如下所述。

If a string selector contains a slash, then it's "shorthand/filename". This is like the plain "shorthand" selector, but further constrained toapply only to a binary whose `output_name` exactly matches "filename". 如果字符串选择器包含斜杠，则为“简写/文件名”。这就像普通的“简写”选择器，但进一步限制为仅适用于`output_name`与“ filename”完全匹配的二进制文件。

The "shorthand" string (a whole string selector or the part before slash) is first looked up in $variant_shorthands, which see.  If it doesn't matcha name defined there, then it must be the name of a variant.  In that case,it's equivalent to `{ variant = "..." host = false }`, meaning it appliesto every binary not built to be a host tool. 首先在$ variant_shorthands中查找“简写”字符串（整个字符串选择器或斜杠前的部分），请参见。如果它与此处定义的名称不匹配，则它必须是变体的名称。在这种情况下，它等效于{{variant =“ ...” host = false}`，这意味着它适用于每个未构建为宿主工具的二进制文件。

A full selector is a scope with the following fields.  All the fields other than `.variant` are matching criteria.  A selector matches if all ofits matching criteria match.  Hence, a selector with no criteria definedalways matches and is referred to as a "catch-all".  The $default_variantslist ends with a catch-all, so each target always chooses some variant. 完全选择器是具有以下字段的作用域。除.variant外的所有字段均符合条件。如果选择器的所有匹配条件均匹配，则该选择器匹配。因此，没有定义任何标准的选择器总是匹配的，被称为“包罗万象”。 $ default_variantslist以包罗万象的结尾，因此每个目标始终选择某种变体。

Selector scope parameters  选择器范围参数

 
  * variant  *变体
    - Required: The variant to use when this selector matches.  If this is a string then it must match a fully-defined variant elsewhere inthe list (or in $default_variants + $standard_variants, which isappended implicitly to the $variants list).  If it's a scope thenit defines a new variant (see details below). -必需：此选择器匹配时使用的变体。如果这是一个字符串，则它必须与列表中其他位置（或$ default_variants + $ standard_variants中的隐式追加到$ variants列表中）的完全定义的变体匹配。如果是范围，则thenit定义一个新的变体（请参见下面的详细信息）。
    - Type: string or scope, described below  -类型：字符串或范围，如下所述

 
  * cpu  * 中央处理器
    - Optional: If nonempty, match only when $current_cpu is one in the  -可选：如果为非空，则仅当$ current_cpu为
    - list.  -清单。
    - Type: list(string)  -类型：列表（字符串）

 
  * os  *操作系统
    - Optional: If nonempty, match only when $current_os is one in the  -可选：如果为非空，则仅当$ current_os为
    - list.  -清单。
    - Type: list(string)  -类型：列表（字符串）

 
  * host  *主机
    - Optional: If present, match only in host environments if true or non-host environments if false.  This means a context in which$is_host is true, not specifically the build host.  For example, itwould be true when cross-compiling host tools for an SDK build butwould be false when compiling code for a hypervisor guest systemthat happens to be the same CPU and OS as the build host. -可选：如果存在，则仅在主机环境为true时匹配，在非主机环境为false。这意味着$ is_host为true的上下文，而不是具体为构建主机。例如，当交叉编译用于SDK构建的主机工具时，itwo为true，而在为与构建主机相同的CPU和OS的虚拟机监控程序来宾系统编译代码时，itwo为false。
    - Type: bool  -类型：布尔

 
  * kernel  * 核心
    - Optional: If present, match only in kernel environments if true or non-kernel environments if false.  This means a context in which$is_kernel is true, not just the "kernel" environment itself.For different machine architectures there may be multiple differentspecialized environments that set $is_kernel, e.g. for boot loadersand for special circumstances used within the kernel.  See also the$tags field in $variant, described below. -可选：如果存在，则仅在内核环境（如果为true）中匹配，在非内核环境中（如果为false）则匹配。这意味着$ is_kernel是真实的上下文，而不仅仅是“ kernel”环境本身。对于不同的机器体系结构，可能会有多个不同的设置$ is_kernel的特殊环境，例如用于引导加载程序以及内核中使用的特殊情况。另请参见$ variant中的$ tags字段，如下所述。
    - Type: bool  -类型：布尔

 
  * environment  * 环境
    - Optional: If nonempty, a list of environment names that match.  This looks at ${toolchain.environment}, which is the simple name (nodirectories) in an environment label defined by environment().  Eachelement can match either the whole environment name, or just the"base" environment, which is the part of the name before a `.` if ithas one.  For example, "host" would match both "host" and "host.fuzz". -可选：如果为非空，则为匹配的环境名称的列表。这看起来是$ {toolchain.environment}，它是由environment（）定义的环境标签中的简单名称（目录）。每个元素都可以匹配整个环境名称，也可以只匹配“基本”环境，如果有，则它是名称前面的部分。例如，“主机”将同时匹配“主机”和“ host.fuzz”。
    - Type: list(string)  -类型：列表（字符串）

 
  * target_type  * target_type
    - Optional: If nonempty, a list of target types to match.  This is one of "executable", "host_tool", "loadable_module", "driver", or"test".Note, test_driver() matches as "driver". -可选：如果为非空，则为要匹配的目标类型的列表。这是“可执行文件”，“主机工具”，“ loadable_module”，“驱动程序”或“测试”之一。注意，test_driver（）与“驱动程序”匹配。
    - Type: list(string)  -类型：列表（字符串）

 
  * label  * 标签
    - Optional: If nonempty, match only when the canonicalized target label (as returned by `get_label_info(..., "label_no_toolchain")`) is one inthe list. -可选：如果为非空，则仅在规范化的目标标签（由get_label_info（...，“ label_no_toolchain”）返回）中匹配时才匹配。
    - Type: list(label_no_toolchain)  -类型：清单（label_no_toolchain）

 
  * dir  *目录
    - Optional: If nonempty, match only when the directory part of the target label (as returned by `get_label_info(..., "dir")`) is one inthe list. -可选：如果为非空，则仅在目标标签的目录部分（由get_label_info（...，“ dir”）返回）时匹配。
    - Type: list(label_no_toolchain)  -类型：清单（label_no_toolchain）

 
  * name  * 名称
    - Optional: If nonempty, match only when the name part of the target label (as returned by `get_label_info(..., "name")`) is one in thelist. -可选：如果为非空，则仅在目标标签的名称部分（由get_label_info（...，“ name”）返回）时匹配。
    - Type: list(label_no_toolchain)  -类型：清单（label_no_toolchain）

 
  * output_name  * output_name
    - Optional: If nonempty, match only when the `output_name` of the target is one in the list.  Note `output_name` defaults to`target_name`, and does not include prefixes or suffixes like ".so"or ".exe". -可选：如果为非空，则仅当目标的`output_name'在列表中为1时匹配。注意`output_name`默认为`target_name`，并且不包含前缀或后缀，如“ .so”或“ .exe”。
    - Type: list(string)  -类型：列表（字符串）

An element with a scope for `.variant` defines a new variant.  Each variant name used in a selector must be defined exactly once.  Otherselectors can refer to the same variant by using the name string in the`.variant` field.  Definitions in $variants take precedence over the samename defined in $standard_variants, but it would probably cause confusionto use the name of a standard variant with a non-standard definition. 范围为.variant的元素定义了一个新的变体。选择器中使用的每个变体名称必须定义一次。其他选择器可以使用.variant字段中的名称字符串来引用相同的变体。 $ variants中的定义优先于$ standard_variants中定义的同名名称，但是使用带有非标准定义的标准变体名称可能会引起混淆。

Variant scope parameters  变体范围参数

 
  * name  * 名称
    - Required: Name for the variant.  This must be unique among all variants used with the same environment.  It becomes part of the GNtoolchain names defined for the environment, which in turn forms partof directory names used in $root_build_dir; so it must meet Ninja'sconstraints on file names (sticking to `[a-z0-9_-]` is a good idea). -必填：变体的名称。在同一环境下使用的所有变体中，这必须是唯一的。它成为为环境定义的GNtoolchain名称的一部分，而该名称又构成$ root_build_dir中使用的目录名称的一部分；因此它必须满足Ninja对文件名的限制（坚持使用[[a-z0-9_-]]是一个好主意）。

 
  * globals  *全球
    - Optional: Variables in this scope are introduced as globals visible to all GN code in the toolchain.  For example, the standard "gcc"variant sets `is_gcc = true` in $globals.  This should be usedsparingly and is safest when restricted to variables that$zx/public/gn/BUILDCONFIG.gn sets defaults for. -可选：该范围内的变量作为工具链中所有GN代码可见的全局变量引入。例如，标准的“ gcc”变体在$ globals中设置“ is_gcc = true”。这应该谨慎使用，并且在限制为$ zx / public / gn / BUILDCONFIG.gn设置默认值的变量时最安全。
    - Type: scope  -类型：范围

 
  * toolchain_args  * toolchain_args
    - Optional: See toolchain().  Variables in this scope must match GN build arguments defined somewhere in the build with declare_args().Use this when the variant should change something that otherwise is amanual tuning variable to set via `gn args`.  *Do not* definevariables in declare_args() just for the purpose of setting them here,i.e. if they should not *also* be available to set via `gn args` toaffect other variants that don't override them here.  Instead, useeither $globals (above) or $toolchain_vars (below). -可选：请参阅toolchain（）。该范围内的变量必须与在声明中用clarify_args（）定义的GN构建参数相匹配。当变量应更改某些内容时，可以使用此变量，否则将通过“ gn args”来设置。 *不要*在clarify_args（）中定义变量只是为了在这里设置它们。如果不应该也可以通过gn args来设置它们，以影响此处未覆盖它们的其他变体。而是使用$ globals（上方）或$ toolchain_vars（下方）。
    - Type: scope  -类型：范围

 
  * toolchain_vars  * toolchain_vars
    - Optional: Variables in this scope are visible in the scope-typed $toolchain global variable seen in toolchains for this variant.Use this to pass along interesting information without clutteringthe global scope via $globals. -可选：此范围中的变量在此变量的工具链中可见的范围类型的$ toolchain全局变量中可见。使用此变量传递有趣的信息，而不会通过$ globals干扰全局范围。
    - Type: scope  -类型：范围

 
  * configs  *配置
    - Optional: List of changes to the pre-set $configs variable in targets being defined in toolchains for this variant.  This is the same as inthe $configs parameter to environment().  Each element is either astring or a scope.  A string element is simply appended to the default$configs list: it's equivalent to a scope element of `{add=["..."]}`.The string is the GN label (without toolchain) for a config() target.A scope element can be more selective, as described below. -可选：在此变量的工具链中定义的目标中，预设$ configs变量的更改列表。这与environment（）的$ configs参数相同。每个元素都是astring或范围。字符串元素只是简单地附加到default $ configs列表：它等效于范围元素{{add = [“ ...”]}`。该字符串是config（）目标的GN标签（无工具链）范围元素可以更具选择性，如下所述。
    - Type: list(label_no_toolchain or scope)  -类型：列表（label_no_toolchain或作用域）
      * shlib  * shlib
        - Optional: If present, this element applies only when `current_toolchain == toolchain.shlib` (if true) or`current_toolchain != toolchain.shlib` (if false).  That is, itapplies only in (not ni) the companion toolchain used to compileshared_library() and loadable_module() (including driver()) code. -可选：如果存在，则此元素仅在current_toolchain == toolchain.shlib（如果为true）或current_toolchain！= toolchain.shlib（如果为false）时适用。也就是说，它仅适用于（非ni）用于编译shared_library（）和loadable_module（）（包括driver（））代码的配套工具链。
        - Type: bool  -类型：布尔

 
      * types  *类型
        - Optional: If present, this element applies only to a target whose type is one in this list (same as `target_type` in a selector,described above). -可选：如果存在，则此元素仅适用于列表中类型为目标的目标（与上述选择器中的“ target_type”相同）。
        - Type: list(string)  -类型：列表（字符串）

 
      * add  *添加
        - Optional: List of labels to append to $configs.  -可选：附加到$ configs的标签列表。
        - Type: list(label_no_toolchain)  -类型：清单（label_no_toolchain）

 
      * remove  * 去掉
        - Optional: List of labels to remove from $configs.  This does exactly `configs -= remove` so it has the normal GN semantics thatit's an error if any element in the $remove list is not present inthe $configs list beforehand. -可选：要从$ configs中删除的标签列表。这样做确实是`configs-= remove`，所以它具有正常的GN语义，如果$ remove列表中的任何元素事先没有出现在$ configs列表中，这就是错误。
        - Type: list(label_no_toolchain)  -类型：清单（label_no_toolchain）

 
  * implicit_deps  * hidden_​​deps
    - Optional: List of changes to the list added to $deps of all linking targets in toolchains for this variant.  This is the same as in the$implicit_deps parameter to environment(). -可选：此变体的列表更改列表已添加到工具链中所有链接目标的$ deps中。这与environment（）的$ implicit_deps参数相同。
    - Type: See $configs  -类型：请参阅$ configs

 
  * tags  *标签
    - Optional: List of tags that describe this variant.  This list will be visible within the variant's toolchains as ${toolchain.tags}.  Its mainpurpose is to match the $exclude_variant_tags list in an environment()definition.  For example, several of the standard variants listed in$standard_variants use the "useronly" tag.  The environment() definingthe kernel toolchains uses `exclude_variant_tags = [ "useronly" ]`.Then $variants selectors that choose variants that are incompatiblewith the kernel are automatically ignored in the kernel toolchains,so there's no need to add `kernel = false` to every such selector. -可选：描述此变体的标签列表。该列表将在变体的工具链中显示为$ {toolchain.tags}。它的主要目的是匹配环境（）定义中的$ exclude_variant_tags列表。例如，$ standard_variants中列出的几个标准变体使用“ useronly”标记。定义内核工具链的environment（）使用`exclude_variant_tags = [“ useronly”]`。然后，选择与内核不兼容的变体的$ variants选择器在内核工具链中被自动忽略，因此无需在其中添加`kernel = false`。每个这样的选择器。
    - Type: list(string)  -类型：列表（字符串）

 
  * bases  *基数
    - Optional: A list of other variant names that this one inherits from. This is a very primitive mechanism for deriving a new variant from anexisting variant.  All of fields from all the bases except for `name`and `bases` are combined with the fields defined explicitly for thenew variant.  The fields of list type are just concatenated in order(each $bases variant in the order listed, then this variant).  Thefields of scope type are merged in the same order, with a variantlater in the list overriding values set earlier (so this variant'svalues override all the bases).  There is *only one* level ofinheritance: a base variant listed in $bases cannot have $bases itself. -可选：此名称继承的其他变体名称的列表。这是从现有变体派生新变体的非常原始的机制。除“ name”和“ bases”外，所有碱基的所有字段都与为新变体明确定义的字段合并。列表类型的字段仅按顺序连接（每个$ bases变体按列出的顺序，然后是此变体）。作用域类型的字段以相同顺序合并，列表中的变量后面覆盖了较早设置的值（因此，此变量的值覆盖所有基数）。 *仅有一个*继承级别：$ bases中列出的基本变体本身不能具有$ bases。
    - Type: list(string)  -类型：列表（字符串）

 

**Current value (from the default):** `[]`  **当前值（默认值）：**`[]`

From //public/gn/toolchain/variants.gni:222  来自//public/gn/toolchain/variants.gni:222

 
### zbi_compression  zbi_compressionThis can be either "lz4f" or "zstd", optionally followed by ".LEVEL" where `LEVEL` can be an integer or "max".  It can also be just "LEVEL"to to use the default algorithm with a non-default setting. 它可以是“ lz4f”或“ zstd”，可选地后跟“ .LEVEL”，其中`LEVEL'可以是整数或“ max”。使用具有非默认设置的默认算法也可以只是“ LEVEL”。

The default level for each algorithm is tuned to balance compression speed with compression ratio.  Higher levels make image builds slower.So using the default during rapid development (quick builds, prettygood compression) and "max' for production builds (slow builds, bestcompression available) probably makes sense. 每种算法的默认级别已调整为平衡压缩速度和压缩率。较高的级别会使映像构建速度变慢。因此，在快速开发（快速构建，相当好的压缩）过程中使用默认值以及在生产构建中使用“ max”（缓慢构建，可用最佳压缩）可能是有道理的。

**Current value (from the default):** `"lz4f"`  **当前值（默认值）：**`“ lz4f”`

From //public/gn/zbi.gni:19  来自//public/gn/zbi.gni:19

 
### zx  x*This must never be set as a build argument*.  *绝不能将其设置为构建参数*。

"$zx/" is the prefix for GN "source-absolute" paths in the Zircon build.  When Zircon is built standalone, the Zircon repository is theroot of the build (where `.gn` is found) so "$zx/" becomes "//".  WhenZircon is part of a larger unified build, there is a higher-level `.gn`file that uses `default_args` to set "$zx/" to "//zircon/". “ $ zx /”是Zircon构建中GN“绝对源”路径的前缀。当Zircon独立构建时，Zircon信息库是构建的根目录（在其中找到了.gn），因此“ $ zx /”变为“ //”。当Zircon是更大的统一构建的一部分时，存在一个更高级别的.gn文件，该文件使用default_args将“ $ zx /”设置为“ // zircon /”。

**Current value (from the default):** `"/"`  **当前值（默认值）：**`“ /”`

From //public/gn/BUILDCONFIG.gn:13  来自//public/gn/BUILDCONFIG.gn:13

