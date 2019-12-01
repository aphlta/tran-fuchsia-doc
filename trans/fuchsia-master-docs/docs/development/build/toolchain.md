 
# Toolchain  工具链 

Fuchsia is using Clang as the official compiler.  紫红色使用Clang作为官方编译器。

 
## Prerequisites  先决条件 

You need [CMake](https://cmake.org/download/) version 3.8.0 and newer to execute these commands. This was the first version to support Fuchsia. 您需要[CMake]（https://cmake.org/download/）3.8.0及更高版本才能执行这些命令。这是支持紫红色的第一个版本。

While CMake supports different build systems, we recommend using [Ninja](https://github.com/ninja-build/ninja/releases) which installedto be present on your system. 虽然CMake支持不同的构建系统，但我们建议您使用[Ninja]（https://github.com/ninja-build/ninja/releases），它已安装在您的系统中。

 
## Getting Source  取得来源 

The example commands below use `${LLVM_SRCDIR}` to refer to the root of your LLVM source tree checkout and assume the [monorepolayout](https://llvm.org/docs/Proposals/GitHubMove.html#monorepo-variant).When using this layout, each sub-project has its own top-leveldirectory. 下面的示例命令使用`$ {LLVM_SRCDIR}`来引用LLVM源树检出的根并假设[monorepolayout]（https://llvm.org/docs/Proposals/GitHubMove.htmlmonorepo-variant）。使用时在这种布局下，每个子项目都有其自己的顶级目录。

The [https://fuchsia.googlesource.com/third_party/llvm-project](https://fuchsia.googlesource.com/third_party/llvm-project)repository emulates this layout via Git submodules and is updatedautomatically by Gerrit. You can use the following command to downloadthis repository including all the submodules after setting the`${LLVM_SRCDIR}` variable: [https://fuchsia.googlesource.com/third_party/llvm-project](https://fuchsia.googlesource.com/third_party/llvm-project）存储库通过Git子模块模拟此布局，并由Gerrit自动更新。设置$ {LLVM_SRCDIR}变量后，可以使用以下命令下载此存储库，包括所有子模块：

```bash
LLVM_SRCDIR=${HOME}/llvm-project
git clone --recurse-submodules https://fuchsia.googlesource.com/third_party/llvm-project ${LLVM_SRCDIR}
```
 

To update the repository including all the submodules, you can use:  要更新包括所有子模块的存储库，可以使用：

```bash
git pull --recurse-submodules
```
 

Alternatively, you can use the official monorepo [https://github.com/llvm/llvm-project](https://github.com/llvm/llvm-project)maintained by the LLVM community. This repository does not usesubmodules which means you can use the standard Git workflow: 或者，您可以使用LLVM社区维护的官方monorepo [https://github.com/llvm/llvm-project](https://github.com/llvm/llvm-project）。该存储库不使用子模块，这意味着您可以使用标准的Git工作流程：

```bash
git clone https://github.com/llvm/llvm-project ${LLVM_SRCDIR}
```
 

 
### Fuchsia SDK  紫红色SDK 

Before building the runtime libraries that are built along with the toolchain, you need a Fuchsia SDK. We expect that the SDK is located inthe directory pointed to by the `${SDK_DIR}` variable: 在构建与工具链一起构建的运行时库之前，您需要一个Fuchsia SDK。我们希望SDK位于$$ SDSD_DIR}变量指向的目录中：

```bash
SDK_DIR=${HOME}/fuchsia/sdk
```
 

To download the latest SDK, you can use the following:  要下载最新的SDK，可以使用以下工具：

```bash
cipd install fuchsia/sdk/core/linux-amd64 latest -root ${SDK_DIR}
```
 

 
## Building Clang  建筑C 

The Clang CMake build system supports bootstrap (aka multi-stage) builds. We use two-stage bootstrap build for the Fuchsia Clang compiler. Clang CMake构建系统支持引导（也称为多阶段）构建。我们对Fuchsia Clang编译器使用两阶段引导程序构建。

The first stage compiler is a host-only compiler with some options set needed for the second stage. The second stage compiler is the fullyoptimized compiler intended to ship to users. 第一级编译器是仅主机的编译器，其中设置了第二级所需的一些选项。第二阶段编译器是旨在交付给用户的经过完全优化的编译器。

Setting up these compilers requires a lot of options. To simplify the configuration the Fuchsia Clang build settings are contained in CMakecache files which are part of the Clang codebase. 设置这些编译器需要很多选择。为了简化配置，Fuchsia Clang构建设置包含在Cake代码库中的CMakecache文件中。

You can build Clang toolchain for Fuchsia using the following commands. These must be run in a separate build directory, which you must create.This directory can be a subdirectory of `${LLVM_SRCDIR}` so that youuse `LLVM_SRCDIR=..` or it can be elsewhere, with `LLVM_SRCDIR` setto an absolute or relative directory path from the build directory. 您可以使用以下命令为紫红色构建Clang工具链。它们必须在必须创建的单独的构建目录中运行。该目录可以是$ {LLVM_SRCDIR}的子目录，以便您使用LLVM_SRCDIR = ..，也可以位于其他位置，并且将LLVM_SRCDIR设置为绝对值。或构建目录中的相对目录路径。

```bash
cmake -GNinja \
  -DLLVM_ENABLE_PROJECTS="clang;lld;clang-tools-extra" \
  -DLLVM_ENABLE_RUNTIMES="compiler-rt;libcxx;libcxxabi;libunwind" \
  -DSTAGE2_FUCHSIA_SDK=${SDK_DIR} \
  -C ${LLVM_SRCDIR}/clang/cmake/caches/Fuchsia.cmake \
  ${LLVM_SRCDIR}/llvm
ninja stage2-distribution
```
 

To include compiler runtimes and C++ library for Linux, you need to use `LINUX_<architecture>_SYSROOT` flag to point at the sysroot and specifythe correct host triple. For example, to build the runtimes for`x86_64-unknown-linux-gnu` using the sysroot from your Fuchsia checkout, youwould use: 要包括用于Linux的编译器运行时和C ++库，您需要使用LINUX_ <architecture> _SYSROOT`标志指向sysroot并指定正确的主机三元组。例如，要使用来自倒挂金钟结帐的sysroot为x86_64-unknown-linux-gnu`构建运行时，您将使用：

```bash
  -DSTAGE2_LINUX_x86_64-unknown-linux-gnu_SYSROOT=${FUCHSIA}/prebuilt/third_party/sysroot/linux-x64 \
  -DSTAGE2_LINUX_aarch64-unknown-linux-gnu_SYSROOT=${FUCHSIA}/prebuilt/third_party/sysroot/linux-arm64 \
```
 

To install the compiler just built into `/usr/local`, you can use the following command: 要安装刚刚内置在`/ usr / local`中的编译器，可以使用以下命令：

```bash
ninja stage2-install-distribution
```
 

To use the compiler just built without installing it into a system-wide shared location, you can just refer to its build directory explicitly as`${LLVM_OBJDIR}/tools/clang/stage2-bins/bin/` (where `LLVM_OBJDIR` isyour LLVM build directory). 要使用刚构建的编译器而不将其安装到系统范围内的共享位置，您只需将其构建目录显式引用为$ {LLVM_OBJDIR} / tools / clang / stage2-bins / bin / LLVM构建目录）。

Note: the second stage build uses LTO (Link Time Optimization) to achieve better runtime performance of the final compiler. LTO oftenrequires a large amount of memory and is very slow. Therefore it may notbe very practical for day-to-day development. 注意：第二阶段构建使用LTO（链接时间优化）来获得最终编译器的更好的运行时性能。 LTO通常需要大量内存，并且速度很慢。因此，对于日常开发而言，它可能不是很实用。

Note: If the Fuchsia build fails due to missing `runtime.json`, `aarch64-fuchsia.manifest`, or `x86_64-fuchsia.manifest` files, you can copythem over from the prebuilt toolchain. 注意：如果由于缺少`runtime.json`，`aarch64-fuchsia.manifest`或`x86_64-fuchsia.manifest`文件而导致Fuchsia构建失败，则可以从预构建的工具链中复制它们。

 
## Developing Clang  开发C语 

When developing Clang, you may want to use a setup that is more suitable for incremental development and fast turnaround time. 开发Clang时，您可能希望使用更适合增量开发和快速周转时间的设置。

The simplest way to build LLVM is to use the following commands:  构建LLVM的最简单方法是使用以下命令：

```bash
cmake -GNinja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld" \
  ${LLVM_SRCDIR}/llvm
ninja
```
 

You can enable additional projects using the `LLVM_ENABLE_PROJECTS` variable. To enable all common projects, you would use: 您可以使用`LLVM_ENABLE_PROJECTS`变量启用其他项目。要启用所有常见项目，您可以使用：

```bash
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld;compiler-rt;libcxx;libcxxabi;libunwind"
```
 

Similarly, you can also enable some projects to be built as runtimes which means these projects will be built using the just-built ratherthan the host compiler: 类似地，您还可以将某些项目构建为运行时，这意味着这些项目将使用刚构建的而不是主机编译器构建：

```bash
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld" \
  -DLLVM_ENABLE_RUNTIMES="compiler-rt;libcxx;libcxxabi;libunwind" \
```
 

Clang is a large project and compiler performance is absolutely critical. To reduce the build time, we recommend using Clang as a host compiler, and ifpossible, LLD as a host linker. These should be ideally built using LTO andfor best possible performance also using Profile-Guided Optimizations (PGO). Clang是一个大型项目，编译器性能绝对至关重要。为了减少构建时间，我们建议使用Clang作为主机编译器，如果可能的话，建议使用LLD作为主机链接器。理想情况下，应使用LTO来构建这些组件，并且还应使用Profile-Guided Optimizations（PGO）以获得最佳性能。

To set the host compiler to Clang and the host linker to LLD, you can use the following extra flags: 要将主机编译器设置为Clang并将主机链接器设置为LLD，可以使用以下额外标志：

```bash
  -DCMAKE_C_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang \
  -DCMAKE_CXX_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang++ \
  -DLLVM_ENABLE_LLD=ON
```
 

This assumes that `${CLANG_TOOLCHAIN_PREFIX}` points to the `bin` directory of a Clang installation, with a trailing slash (as this Make variable is usedin the Zircon build). For example, to use the compiler from your Fuchsiacheckout (on Linux): 假设$$ {CLANG_TOOLCHAIN_PREFIX}指向Clang安装目录的bin目录，并带有斜杠（因为该Make变量在Zircon版本中使用）。例如，要通过Fuchsiacheckout使用编译器（在Linux上）：

```bash
CLANG_TOOLCHAIN_PREFIX=${FUCHSIA}/prebuilt/third_party/clang/linux-x64/bin/
```
 

Note: To build Fuchsia, you need a stripped version of the toolchain runtime binaries. Use `DESTDIR=/path/to/install/dir ninja install-distribution-stripped`to get a stripped install and then point your build configuration to`/path/to/install/dir/bin` as your toolchain. 注意：要构建Fuchsia，您需要工具链运行时二进制文件的简化版本。使用`DESTDIR = / path / to / install / dir ninja install-distribution-stripped`进行剥离安装，然后将构建配置指向`/ path / to / install / dir / bin`作为工具链。

 
### Sanitizers  消毒剂 

Most sanitizers can be used on LLVM tools by adding `LLVM_USE_SANITIZER=<sanitizer name>` to your cmake invocation. MSan isspecial however because some LLVM tools trigger false positives. Tobuild with MSan support you first need to build libc++ with MSansupport. You can do this in the same build. To set up a build with MSansupport first run CMake with `LLVM_USE_SANITIZER=Memory` and`LLVM_ENABLE_LIBCXX=ON`. 通过在您的cmake调用中添加LLVM_USE_SANITIZER = <sanitizer name>，可以在LLVM工具上使用大多数消毒剂。但是MSan是特殊的，因为某些LLVM工具会触发误报。要使用MSan支持进行构建，首先需要使用MSansupport构建libc ++。您可以在同一版本中执行此操作。要使用MSansupport建立构建，请先使用LLVM_USE_SANITIZER = Memory和LLVM_ENABLE_LIBCXX = ON运行CMake。

```bash
cmake -GNinja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang \
  -DCMAKE_CXX_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang++ \
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld;libcxx;libcxxabi;libunwind" \
  -DLLVM_USE_SANITIZER=Memory \
  -DLLVM_ENABLE_LIBCXX=ON \
  -DLLVM_ENABLE_LLD=ON \
  ${LLVM_SRCDIR}/llvm
```
 

Normally you would run Ninja at this point but we want to build everything using a sanitized version of libc++ but if we build now itwill use libc++ from `${CLANG_TOOLCHAIN_PREFIX}` which isn't sanitized.So first we build just the cxx and cxxabi targets. These will be used inplace of the ones from `${CLANG_TOOLCHAIN_PREFIX}` when toolsdynamically link against libcxx 正常情况下，您会在此时运行Ninja，但是我们想使用经过清理的libc ++版本来构建所有内容，但是如果现在进行构建，它将使用未经过清理的`$ {CLANG_TOOLCHAIN_PREFIX}`中的libc ++。因此，首先我们仅构建cxx和cxxabi目标。当工具动态链接到libcxx时，将用它们代替$$ {CLANG_TOOLCHAIN_PREFIX}中的那些。

```bash
ninja cxx cxxabi
```
 

Now that we have a sanitized version of libc++ we can have our build use it instead of the one from `${CLANG_TOOLCHAIN_PREFIX}` and then buildeverything. 既然我们有了libc ++的净化版本，我们就可以使用它来代替$$ {CLANG_TOOLCHAIN_PREFIX}`中的版本，然后进行所有构建。

```bash
ninja
```
 

Putting that all together:  放在一起：

```bash
cmake -GNinja \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang \
  -DCMAKE_CXX_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang++ \
  -DLLVM_USE_SANITIZER=Address \
  -DLLVM_ENABLE_LIBCXX=ON \
  -DLLVM_ENABLE_LLD=ON \
  ${LLVM_SRCDIR}/llvm
ninja libcxx libcxxabi
ninja
```
 

 
### [Googlers only] Goma  [仅限Google员工]戈马 

Ensure Goma is installed on your machine for faster builds; Goma accelerates builds by distributing compilation across many machines. Ifyou have Goma installed in `${GOMA_DIR}` (by default `${HOME}/goma`),you can enable Goma use with the following extra flags: 确保将Goma安装在您的计算机上以加快构建速度； Goma通过在许多机器之间分布编译来加速构建。如果您在$$ GOMA_DIR}中安装了Goma（默认情况下为$ {HOME} / goma`），则可以使用以下额外的标志来启用Goma使用：

```bash
  -DCMAKE_C_COMPILER_LAUNCHER=${GOMA_DIR}/gomacc \
  -DCMAKE_CXX_COMPILER_LAUNCHER=${GOMA_DIR}/gomacc \
  -DLLVM_PARALLEL_LINK_JOBS=${LINK_JOBS}
```
 

The number of link jobs is dependent on RAM size, for LTO build you will need at least 10GB for each job. 链接作业的数量取决于RAM大小，对于LTO构建，每个作业至少需要10GB。

To build Clang with Goma, use:  要使用Goma构建Clang，请使用：

```bash
ninja -j${JOBS}
```
 

Use `-j100` for Goma on macOS and `-j1000` for Goma on Linux. You may need to tune the job count to suit your particular machine and workload. 在macOS上将`-j100`用于Goma，在Linux上将`-j1000`用于Goma。您可能需要调整作业数量以适合您的特定机器和工作负载。

Note: that in order to use Goma, you need a host compiler that is supported by Goma such as the Fuchsia Clang installation. See above onhow to configure your LLVM buile to use a different host compiler. 注意：要使用Goma，您需要Goma支持的主机编译器，例如Fuchsia Clang安装。有关如何配置LLVM Buile以使用其他主机编译器的信息，请参见上文。

To verify your compiler is available on Goma, you can set `GOMA_USE_LOCAL=0 GOMA_FALLBACK=0` environment variables. If thecompiler is not available, you will see an error. 为了验证您的编译器在Goma上可用，您可以设置`GOMA_USE_LOCAL = 0 GOMA_FALLBACK = 0`环境变量。如果编译器不可用，您将看到一个错误。

 
### Fuchsia Configuration  紫红色配置 

When developing Clang for Fuchsia, you can also use the cache file to test the Fuchsia configuration, but run only the second stage, with LTOdisabled, which gives you a faster build time suitable even forincremental development, without having to manually specify all options: 在开发用于Fuchsia的Clang时，您还可以使用缓存文件来测试Fuchsia的配置，但是仅在第二阶段运行，并且禁用LTO，这为您提供了更快的构建时间，甚至适合增量开发，而无需手动指定所有选项：

```bash
cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang \
  -DCMAKE_CXX_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang++ \
  -DLLVM_ENABLE_LTO=OFF \
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld" \
  -DLLVM_ENABLE_RUNTIMES="compiler-rt;libcxx;libcxxabi;libunwind" \
  -DLINUX_x86_64-unknown-linux-gnu_SYSROOT=${FUCHSIA}/prebuilt/third_party/sysroot/linux-x64 \
  -DLINUX_aarch64-unknown-linux-gnu_SYSROOT=${FUCHSIA}/prebuilt/third_party/sysroot/linux-arm64 \
  -DFUCHSIA_SDK=${SDK_DIR} \
  -C ${LLVM_SRCDIR}/clang/cmake/caches/Fuchsia-stage2.cmake \
  ${LLVM_SRCDIR}/llvm
ninja distribution
```
 

With Goma for even faster turnaround time:  使用Goma可获得更快的周转时间：

```bash
cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang \
  -DCMAKE_CXX_COMPILER=${CLANG_TOOLCHAIN_PREFIX}clang++ \
  -DCMAKE_C_COMPILER_LAUNCHER=${GOMA_DIR}/gomacc \
  -DCMAKE_CXX_COMPILER_LAUNCHER=${GOMA_DIR}/gomacc \
  -DCMAKE_EXE_LINKER_FLAGS="-ldl -lpthread" \
  -DCMAKE_SHARED_LINKER_FLAGS="-ldl -lpthread" \
  -DLLVM_PARALLEL_LINK_JOBS=${LINK_JOBS} \
  -DLLVM_ENABLE_LTO=OFF \
  -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld" \
  -DLLVM_ENABLE_RUNTIMES="compiler-rt;libcxx;libcxxabi;libunwind" \
  -DLINUX_x86_64-unknown-linux-gnu_SYSROOT=${FUCHSIA}/prebuilt/third_party/sysroot/linux-x64 \
  -DLINUX_aarch64-unknown-linux-gnu_SYSROOT=${FUCHSIA}/prebuilt/third_party/sysroot/linux-arm64 \
  -DFUCHSIA_SDK=${SDK_DIR} \
  -C ${LLVM_SRCDIR}/clang/cmake/caches/Fuchsia-stage2.cmake \
  ${LLVM_SRCDIR}/llvm
ninja distribution -j${JOBS}
```
 

 
## Testing Clang  测试C 

To run Clang tests, you can use the `check-<component>` target:  要运行Clang测试，可以使用`check- <component>`目标：

```
ninja check-llvm check-clang
```
 

You can all use `check-all` to run all tests, but keep in mind that this can take significant amount of time depending on the number of projectsyou have enabled in your build. 您都可以使用“全部检查”来运行所有测试，但是请记住，这可能会花费大量时间，具体取决于您在构建中启用的项目数量。

 
### Building Fuchsia with custom Clang locally  在本地使用自定义Clang构建紫红色 

You can start building test binaries right away by using the Clang in `${LLVM_OBJDIR}/bin/`, or in`${LLVM_OBJDIR}/tools/clang/stage2-bins/bin/` (depending on whether youdid the two-stage build or the single-stage build, the binaries will bein a different location). However, if you want to use your Clang tobuild Fuchsia, you will need to set some more arguments/variables. 您可以使用$ {LLVM_OBJDIR} / bin /`或$ {LLVM_OBJDIR} / tools / clang / stage2-bins / bin /`中的Clang立即开始构建测试二进制文件（取决于您是否选择了两个，阶段构建或单阶段构建，二进制文件将位于不同的位置）。但是，如果要使用Clang来构建紫红色，则需要设置更多的参数/变量。

If you are only interested in building Zircon, set the following GN build arguments: 如果仅对构建Zircon感兴趣，请设置以下GN build参数：

```bash
gn gen build-zircon --args='variants = [ "clang" ] clang_tool_dir = ${CLANG_DIR}'
```
 

`${CLANG_DIR}` is the path to the `bin` directory for your Clang build, e.g. `${LLVM_OBJDIR}/bin/`. $ {CLANG_DIR}是您的Clang构建的bin目录的路径，例如`$ {LLVM_OBJDIR} / bin /`。

Note: that trailing slash is important.  注意：斜杠很重要。

Then run `fx build-zircon` as usual.  然后照常运行`fx build-zircon`。

For layers-above-Zircon, it should be sufficient to pass `--args clang_prefix="${CLANG_DIR}"` to `fx set`, then run `fx build` as usual. 对于锆石之上的层，将`--args clang_prefix =“ $ {CLANG_DIR}”`传递给`fx set`应该足够了，然后照常运行`fx build`。

 
### Building Fuchsia with custom Clang on bots (Googlers only)  在机器人上使用自定义Clang构建紫红色（仅限Google员工） 

Fuchsia's infrastructure has support for using a non-default version of Clang to build. Only Clang instances that have been uploaded to CIPD or Isolate areavailable for this type of build, and so any local changes must land inupstream and be built by the CI or production toolchain bots. 紫红色的基础架构支持使用非默认版本的Clang进行构建。这种类型的构建仅适用于已上传到CIPD或隔离的Clang实例，因此任何本地更改都必须在上游登陆，并由CI或生产工具链机器人进行构建。

You will need the infra codebase and prebuilts. Directions for checkout are on the infra page. 您将需要基础代码和预先构建的代码。结帐说明在下面的页面上。

To trigger a bot build with a specific revision of Clang, you will need the Git revision of the Clang with which you want to build. This is on the [CIPD page](https://chrome-infra-packages.appspot.com/p/fuchsia/clang),or can be retrieved using the CIPD CLI. You can then run the following command: 要使用特定版本的Clang触发机器人构建，您将需要使用其构建的Clang的Git版本。该文件位于[CIPD页面]（https://chrome-infra-packages.appspot.com/p/fuchsia/clang），也可以使用CIPD CLI进行检索。然后，您可以运行以下命令：

```bash
export FUCHSIA_SOURCE=<path_to_fuchsia>
export BUILDER=<builder_name>
export REVISION=<clang_revision>

export INFRA_PREBUILTS=${FUCHSIA_SOURCE}/fuchsia-infra/prebuilt/tools

cd ${FUCHSIA_SOURCE}/fuchsia-infra/recipes

${INFRA_PREBUILTS}/led get-builder 'luci.fuchsia.ci:${BUILDER}' | \
${INFRA_PREBUILTS}/led edit-recipe-bundle -O | \
jq '.userland.recipe_properties."$infra/fuchsia".clang_toolchain.type="cipd"' | \
jq '.userland.recipe_properties."$infra/fuchsia".clang_toolchain.instance="git_revision:${REVISION}"' | \
${INFRA_PREBUILTS}/led launch
```
 

It will provide you with a link to the BuildBucket page to track your build.  它将为您提供指向BuildBucket页面的链接，以跟踪您的构建。

You will need to run `led auth-login` prior to triggering any builds, and may need to file an infra ticket to request access to run led jobs. 在触发任何构建之前，您将需要运行`led auth-login`，并且可能需要提交一张基础票以请求访问运行led作业的权限。

 
## Additional Resources  其他资源 

Documentation:  说明文件：

 
* [Getting Started with the LLVM System](http://llvm.org/docs/GettingStarted.html)  * [LLVM系统入门]（http://llvm.org/docs/GettingStarted.html）
* [Building LLVM with CMake](http://llvm.org/docs/CMake.html)  * [使用CMake构建LLVM]（http://llvm.org/docs/CMake.html）
* [Advanced Build Configurations](http://llvm.org/docs/AdvancedBuilds.html)  * [高级构建配置]（http://llvm.org/docs/AdvancedBuilds.html）

Talks:  会谈：

 
* [2016 LLVM Developers’ Meeting: C. Bieneman "Developing and Shipping LLVM and Clang with CMake"](https://www.youtube.com/watch?v=StF77Cx7pz8)  * [2016年LLVM开发人员会议：C。Bieneman“使用CMake开发和交付LLVM和Clang”]（https://www.youtube.com/watch?v=StF77Cx7pz8）
