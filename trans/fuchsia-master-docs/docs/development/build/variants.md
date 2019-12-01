 
# Fuchsia Build System: Variants  紫红色的构建系统：变体 

The Fuchsia GN build machinery allows for separate components to be built in different "variants".  A variant usually just means using extra compileroptions, but they can do more than that if you write some more GN code.The variants defined so far enable things like[sanitizers](https://github.com/google/sanitizers/wiki) and[LTO](https://llvm.org/docs/LinkTimeOptimization.html). 紫红色GN建造机械允许在不同的“变体”中建造独立的组件。变体通常只是意味着使用额外的编译器选项，但是如果您编写更多的GN代码，它们可能会做得更多。到目前为止定义的变体启用了[sanitizers]（https://github.com/google/sanitizers/wiki）之类的功能。和[LTO]（https://llvm.org/docs/LinkTimeOptimization.html）。

The GN build argument [`select_variant`](/docs/gen/build_arguments.md#select_variant)controls which components are built in which variants.  It appliesautomatically to every `executable`, `loadable_module`, or `driver_module`target in GN files.  It's a flexible mechanism in which you give a list ofmatching rules to apply to each target to decide which variant to use (ifany).  To support this flexibility, the value for `select_variant` uses adetailed GN syntax.  For simple cases, this can just be a list of strings. GN构建参数[`select_variant`]（/ docs / gen / build_arguments.mdselect_variant）控制在哪些变量中构建哪些组件。它会自动应用于GN文件中的每个“可执行文件”，“ loadable_module”或“ driver_module”目标。这是一种灵活的机制，您可以在其中提供一系列匹配规则以应用于每个目标，以决定使用哪个变体（如果有）。为了支持这种灵活性，select_variant的值使用详细的GN语法。对于简单的情况，这可以只是一个字符串列表。

Using `fx set`:  使用`fx set`：

```sh
fx set core.x64 --variant=host_asan --variant=asan/cat --variant=asan/ledger
```
 

Alternatively, you can add or modify the variants on an existing build by editing the GN args (substituting your build's GN output directoryfor `out/default` as necessary): 另外，您可以通过编辑GN args在现有版本上添加或修改变体（必要时将版本的GN输出目录替换为“ out / default”）：

```sh
gn args out/default
```
 

That command will bring up an editor. Append to that file:  该命令将显示一个编辑器。附加到该文件：

```
select_variant = [ "host_asan", "asan/cat", "asan/ledger" ]
```
 

 
 1. The first switch applies the `host_asan` matching rule, which enables [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)for all the executables built to run on the build host. 1.第一个开关应用“ host_asan”匹配规则，该规则为所有要在构建主机上运行的可执行文件启用[AddressSanitizer]（https://clang.llvm.org/docs/AddressSanitizer.html）。

 
 2. The second switch applies the `asan` matching rule, which enables AddressSanitizer for executables built to run on the target (i.e. theFuchsia device).  The `/cat` suffix constrains this matching rule onlyto the binary named `cat`. 2.第二个开关应用“ asan”匹配规则，该规则使AddressSanitizer能够针对在目标设备（即紫红色设备）上运行的可执行文件进行操作。后缀“ / cat”仅将此匹配规则限制在名为“ cat”的二进制文件中。

 
 3. The third switch is like the second, but matches the binary named `ledger`.  3.第三个开关与第二个类似，但与名为“ ledger”的二进制文件匹配。

The GN code supports much more flexible matching rules than just the binary name, but there are no shorthands for those. See the[`select_variant`](/docs/gen/build_arguments.md#select_variant)build argument documentation for more details. GN代码不仅支持二进制名称，而且还支持更加灵活的匹配规则，但是这些规则没有简写形式。有关更多详细信息，请参见[`select_variant`]（/ docs / gen / build_arguments.mdselect_variant）构建参数文档。

To see the list of variants available and learn more about how to define new ones, see the[`known_variants`](/docs/gen/build_arguments.md#known_variants)build argument. 要查看可用的变体列表并了解有关如何定义新变体的更多信息，请参见[`known_variants`]（/​​ docs / gen / build_arguments.mdknown_variants）build参数。

 
## Troubleshooting notes  故障排除说明 

 
### Replicating ASan failures  复制ASan故障 

Our commit queue runs tests in an ASan-enabled configuration. To replicate the build in this configuration, use the following `args.gn` file: 我们的提交队列在启用ASan的配置中运行测试。要在此配置中复制构建，请使用以下`args.gn`文件：

```sh
import("//boards/<x64-or-arm64>.gni")
import("//products/core.gni")

base_package_labels+=[ "//bundles/buildbot:core" ]
goma_dir="<path-to-goma-dir>"
is_debug=true
select_variant=["asan","host_asan"]
target_cpu="<x64-or-arm64>"
use_goma=true
```
 

Replace `x64-or-arm64` with your desired target architecture, and replace `<path-to-goma-dir>` with the path to your goma dir (for those who use goma). Thiscan also be generated from the command line with: 将x64-or-arm64替换为所需的目标体系结构，并将<path-to-goma-dir>替换为goma目录的路径（对于使用goma的用户）。也可以从命令行使用以下命令生成：

```sh
fx set core.x64 --with-base //bundles/buildbot:core --variant host_asan --variant asan --goma
```
 

Note that this will build all of the tests that are run by the commit queue and install them in the system image. This may be undesirable for two reasons: 请注意，这将构建由提交队列运行的所有测试，并将它们安装在系统映像中。由于以下两个原因，这可能是不可取的：

 
 * Building all of the tests is typically slow and unnecessary. Developers may find it more effective to limit the package labels to the tests they need. *建立所有测试通常很慢且不必要。开发人员可能会发现将包装标签限制为他们需要的测试更为有效。
 * Installing all of the tests in the system image ahead of time means that the software deployment workflow does not get exercised. *提前在系统映像中安装所有测试，意味着不会执行软件部署工作流。

 
### Launching executables from within ASan-enabled binaries  从启用ASan的二进制文件中启动可执行文件 

If you are trying to use the ASan variant, you may encounter an error that looks like this: 如果您尝试使用ASan变体，则可能会遇到如下错误：

```sh
launcher: error: Launch: elf_load: handle_interp failed
dlsvc: could not open 'asan/ld.so.1'
```
 

Fuchsia is structured around packages and components. Each component contains all of the shared libraries it needs to run. This helps Fuchsia avoid libraryversioning issues that plague other operating systems. It also means that, ifyou want to run a binary from within a component, you must provide theappropriate shared library loader for that binary. 紫红色是围绕包装和组件构造的。每个组件都包含它需要运行的所有共享库。这有助于紫红色避免困扰其他操作系统的库版本转换问题。这也意味着，如果要从组件中运行二进制文件，则必须为该二进制文件提供适当的共享库加载器。

There are a set of command line programs located in the `/boot/` directory of Fuchsia installs that are not contained in packages, but in the boot filesystem.These programs do not have their own shared library loader, and will usewhatever shared libraries the component executing them provides. This normallyworks, as programs like `sh` and `ls` have very minimal, very commondependencies. However, there's no guarantee that the component's package willhave sufficient or compatible shared libraries for the command line program'sneeds. ASan-enabled packages usually do not contain the right launcher for theseprograms, so most ASan-enabled components cannot run executables out of`/boot`. If an ASan-enabled component tries to do so, it gets the error above. 在Fuchsia安装目录的/ boot /目录中有一组命令行程序，它们不包含在软件包中，而是包含在引导文件系统中。这些程序没有自己的共享库加载器，将使用任何共享库执行它们的组件提供。这通常是可行的，因为像`sh`和`ls`这样的程序具有非常小的，非常常见的依赖性。但是，不能保证组件的程序包将具有足够或兼容的共享库来满足命令行程序的需求。启用ASan的软件包通常不包含这些程序的正确启动器，因此大多数启用ASan的组件无法在/ boot之外运行可执行文件。如果启用了ASan的组件尝试这样做，则会得到上面的错误。

