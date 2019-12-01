 
# Cross Translation Unit Static Analysis in Zircon  锆石中的交叉翻译单元静态分析 

This document describes:  本文描述：

 
* How to set up cross-translation-unit analysis (**CTU**) with the Clang Static Analyzer (**CSA**) in Zircon;  *如何在Zircon中使用Clang静态分析器（** CSA **）设置跨翻译单元分析（** CTU **）；
* The work done by Kareem Khazem during his internship; and  * Kareem Khazem实习期间所做的工作；和
* The remaining work needed to get CTU fully supported on Zircon.  *在Zircon上完全支持CTU所需的剩余工作。

 
## Setting up and running CTU on Zircon  在Zircon上设置并运行CTU 

**Summary**: Download the source for Clang, and apply several non-mainline patches to it before compiling it. Run my wrapper script around the analysis tools. Download the `CodeChecker` tool; use it to digest the results of the analysis, and start a web server to view the results with a web interface.  **摘要**：下载Clang的源代码，并在编译之前对其应用一些非主线补丁。在分析工具周围运行我的包装脚本。下载“ CodeChecker”工具；使用它来消化分析结果，并启动Web服务器以通过Web界面查看结果。

 
## CTU-enabling patches  支持CTU的补丁 

There are two patchsets to be aware of:  有两个要注意的补丁集：

 
* The [Samsung](https://github.com/haoNoQ/clang/tree/summary-ipa-draft) patchset, which is an enormous patch adding AST merging support to Clang. It consists mostly of additions to `lib/AST/ASTImporter.cpp`. There is also a (primitive, not working very well) set of tools for CTU analysis under `tools/xtu-build/*`. This patchset is based on an old revision of Clang; this fact, as well as its large size, makes it very difficult to rebase wholesale onto tip-of-tree (**ToT**) Clang.  * [Samsung]（https://github.com/haoNoQ/clang/tree/summary-ipa-draft）补丁集，这是一个巨大的补丁，为Clang添加了AST合并支持。它主要由`lib / AST / ASTImporter.cpp`添加。在“ tools / xtu-build / *”下还有一组（原始的，效果不佳）用于CTU分析的工具。该补丁集基于Clang的旧版本；这个事实以及它的大尺寸使得很难将批发重新建立到树梢（** ToT **）Clang上。
* The [Ericsson](https://github.com/dkrupp/clang/blob/ctu-master/tools/xtu-build-new/xtu-analyze.py) patchset, which includes a subset of Samsung’s AST merging work and also adds several new tools (`tools/xtu-build-new/*` and `tools/scan-build-py/*`) that allow for CTU analysis. The xtu-build-new tools improve on, and are somewhat different to, Samsung’s xtu-build tools. This patchset is much newer than the Samsung one, and the authors are making an effort to keep it rebased on ToT.  * [Ericsson]（https://github.com/dkrupp/clang/blob/ctu-master/tools/xtu-build-new/xtu-analyze.py）补丁集，其中包括三星AST合并工作的子集和还添加了一些允许进行CTU分析的新工具（“ tools / xtu-build-new / *”和“ tools / scan-build-py / *”）。 xtu-build-new工具改进了三星的xtu-build工具，并且与三星的xtu-build工具有所不同。这个补丁集比三星的补丁集新得多，作者正在努力使其重新基于ToT。

We will be patching Clang with Ericsson’s patchset, since the AST merging work rebases cleanly and we also get the newer analysis tools. However, note that CTU support for Zircon is incomplete; in some cases, the Samsung patchset contains code that provides the required functionality (more details below).  我们将使用爱立信的补丁集为Clang修补，因为AST合并工作会重新整理，并且我们还将获得更新的分析工具。但是，请注意，CTU对Zircon的支持不完整。在某些情况下，三星补丁集包含提供所需功能的代码（更多详细信息在下面）。

 
### Steps to build CTU-capable CSA  建立具有CTU功能的CSA的步骤 

 
1. Download and build Clang and LLVM as usual.  1.照常下载并构建Clang和LLVM。
2. In a separate directory, clone Ericsson’s fork of Clang and switch to the ctu-master branch.  2.在另一个目录中，克隆爱立信的Clang分支，并切换到ctu-master分支。
3. Download [this script](https://gist.github.com/karkhaz/d11efa611a1bde23490c2773dc0da60d) into Ericsson’s fork and run it. It should dump a series of patches into a patches directory. I purposely only dump the commits from the beginning of Ericsson’s changes until 1bb3636, which was the latest revision during my internship.  3.将[此脚本]（https://gist.github.com/karkhaz/d11efa611a1bde23490c2773dc0da60d）下载到爱立信的fork中并运行它。它应该将一系列补丁转储到补丁目录中。我特意只转储从爱立信变更开始到1bb3636（这是我实习期间的最新修订版）之前的提交内容。
    * If you want more up-to-date changes from Ericsson, you can experiment with changing 1bb3636 to HEAD in the script. Make sure to skip commits that merge upstream commits into the ctu-master branch by specifying additional ranges in the script. git log --graph can be helpful to determine what the upstream commits vs. Ericsson’s commits are, I use  *如果要从爱立信获得更多最新更改，可以尝试在脚本中将1bb3636更改为HEAD。通过在脚本中指定其他范围，确保跳过将上游提交合并到ctu-master分支中的提交。 git log --graph有助于确定上游提交与爱立信的提交是什么，我使用

    ```
    git log --graph  --decorate --date=relative --format=format:'%C(green)%h%C(yellow) %s%C(reset)%w(0,6,6)%C(bold green)\n%C(cyan)%G? %C(bold red)%aN%C(reset) %cr%C(reset)%w(0,0,0)\n%-D\n%C(reset)' --all
    ```
 

 
4. Apply the generated patches to *upstream* Clang (not the Ericsson fork) one at a time.  4.一次将一个生成的补丁应用到*上游* Clang（不是爱立信分支）。

   ```
   for p in $(ls $PATCH_DIR/*.patch | sort -n); do git am < $p; done
   ```
 

 
5. Apply Kareem Khazem’s patches that are listed [below](#zircon-patches) if they haven’t already landed  5.如果尚未着陆，请套用[下面]列出的Kareem Khazem补丁（锆石补丁）
6. Re-build upstream Clang & LLVM.  6.重新构建上游Clang LLVM。

 
## Running CTU analysis  运行CTU分析 

**Summary:** Run my wrapper script. This builds Zircon normally, then builds it again but dumping serialised ASTs instead of object files, and then finally analyses each file using the dumped ASTs to achieve CTU.  **摘要：**运行我的包装器脚本。这将正常构建Zircon，然后再次构建Zircon，但转储序列化的AST而不是目标文件，然后最终使用转储的AST分析每个文件以实现CTU。

 
### How CTU works  CTU如何运作 

First, the story backwards:  首先，故事倒退：

Non-CTU static analysis analyzes the AST of each TU; any function calls to external functions are treated as opaque. Roughly, CTU analysis seeks to *substitute* the opaque function call node with the AST of that function’s implementation.  非CTU静态分析会分析每个TU的AST；任何对外部函数的函数调用均视为不透明。粗略地讲，CTU分析试图用该函数实现的AST“替代”不透明的函数调用节点。

Thus, a CTU analysis will start analyzing an AST as usual, but when it encounters a function call node, it will try to *merge in* the AST for that function. This relies on the AST for the function already having been serialized to disk beforehand, so that the analyzer can re-load the AST into memory. It also relies on support for AST merging, which is what the Samsung patch to `ASTImporter.cpp` (and the Ericsson patch derived from it) is for.  因此，CTU分析将照常开始分析AST，但是当它遇到函数调用节点时，它将尝试“合并”该函数的AST。这依赖于AST，因为该功能已经预先序列化到磁盘，因此分析仪可以将AST重新加载到内存中。它还依赖于对AST合并的支持，这就是针对ASTImporter.cpp的三星补丁（以及由此衍生的爱立信补丁）的目的。

In order to serialize the ASTs to disk, we need to emulate the real build process. The way to do this is to actually do a real build of Zircon while recording the compiler invocations; this allows us to ‘play back’ the invocations, but with the compiler flags modified to dump AST files rather than object files.  为了将AST序列化到磁盘，我们需要模拟实际的构建过程。这样做的方法是在记录编译器调用的同时实际构建Zircon。这使我们可以“回放”调用，但是修改了编译器标志以转储AST文件而不是目标文件。

So to summarise, forwards this time:  总结一下，这次转发：

 
* Build zircon using Clang, and wrap the build process in a program like [bear](https://github.com/rizsotto/Bear) in order to record compiler invocations and generate a JSON compilation database.  *使用Clang生成Zircon，并将生成过程包装在[bear]（https://github.com/rizsotto/Bear）之类的程序中，以便记录编译器调用并生成JSON编译数据库。
* Replay the same compilation steps, but dumping AST files instead of object files. This is what the [xtu-build.py](https://github.com/dkrupp/clang/blob/ctu-master/tools/xtu-build-new/xtu-build.py) tool does.  *重播相同的编译步骤，但转储AST文件而不是目标文件。这就是[xtu-build.py]（https://github.com/dkrupp/clang/blob/ctu-master/tools/xtu-build-new/xtu-build.py）工具的作用。
* Perform static analysis as usual, but deserialize the AST of every called function when needed. This is what the [xtu-analyze.py](https://github.com/dkrupp/clang/blob/ctu-master/tools/xtu-build-new/xtu-analyze.py) tool does at the top level, by invoking tools in the [scan-build-py/libscanbuild](https://github.com/dkrupp/clang/tree/ctu-master/tools/scan-build-py/libscanbuild) directory through the thin [scan-build replacement](https://github.com/dkrupp/clang/blob/ctu-master/tools/scan-build-py/bin/scan-build) written by the Ericsson team.  *照常执行静态分析，但是在需要时反序列化每个调用函数的AST。这就是[xtu-analyze.py]（https://github.com/dkrupp/clang/blob/ctu-master/tools/xtu-build-new/xtu-analyze.py）工具在顶层执行的操作，通过精简的[scan -build替换]（https://github.com/dkrupp/clang/blob/ctu-master/tools/scan-build-py/bin/scan-build），由爱立信团队撰写。

These steps are captured in the [Fuchsia wrapper](#fuchsia-wrapper-script) mentioned below. The result of all this is a directory full of reports, in [Apple plist](https://en.wikipedia.org/wiki/Property_list) format, which contain details of reported bugs.  这些步骤在下面提到的[Fuchsia wrapper]（fuchsia-wrapper-script）中捕获。所有这些操作的结果是一个充满报告的目录，格式为[Apple plist]（https://en.wikipedia.org/wiki/Property_list），其中包含已报告错误的详细信息。

 
### Ericsson’s wrapper scripts {#ericsson-wrapper-script}  爱立信的包装器脚本{ericsson-wrapper-script} 

There are two sets of tools for running cross-translation-unit analysis:  有两套用于运行跨翻译单元分析的工具：

 
* The tools under `tools/xtu-build-new` are the top-level scripts. Since the underlying analyzer can fail (i.e. due to the CSA crashing), I’ve patched `xtu-analyze.py` (in Ericsson’s branch) so that it dumps the output of the analyzer (stdout/stderr, not the report) to a file. The output goes in ``$OUT_DIR/{passes,fails}`` depending on the return code of the analyzer, where `$OUT_DIR` is the directory passed to the `-o` argument of `xtu-analyze.py`. The particularly helpful part of those files is the *second line* that starts with `analyze: DEBUG: exec command in`, which is emitted by the `libscanbuild` tools (next bullet point). That command is the actual invocation to the CSA after the long, tedious process of modifying its command line. Therefore, it’s the command that you will need if you want to run the CSA on a troublesome file using gdb.  *“ tools / xtu-build-new”下的工具是顶级脚本。由于基础分析器可能会失败（即由于CSA崩溃），因此我对xtu-analyze.py（在爱立信的分支中）进行了修补，以便将分析器的输出（stdout / stderr，而不是报告）转储到一份文件。根据分析器的返回代码，输出将进入$ OUT_DIR / {passes，fails}中，其中$ OUT_DIR是传递到xtu-analyze.py的-o参数的目录。这些文件特别有用的部分是第二行，该行以“ analyze：DEBUG：exec command in”开头，由“ libscanbuild”工具发出（下一个要点）。该命令是经过漫长而繁琐的CSA命令行修改过程后对CSA的实际调用。因此，如果您想使用gdb在有问题的文件上运行CSA，则需要使用该命令。
* The tools under `tools/scan-build-py` are a bird’s nest of tools to wrap around the actual invocation to Clang. They are responsible for modifying the command line. I’m not too familiar with them, and haven’t had to interfere with them in the past.  *“ tools / scan-build-py”下的工具是一堆嵌套的工具，用于包装对Clang的实际调用。他们负责修改命令行。我对它们不太熟悉，过去也不必干预它们。

 
### Fuchsia wrapper script {#fuchsia-wrapper-script}  紫红色的包装脚本{fuchsia-wrapper-script} 

[This very small shell script](https://gist.github.com/karkhaz/c8ded50e564d73853731266fec729454) wraps the Ericsson `xtu-build-new` wrappers. To do a complete analysis of Zircon, make sure to clean first, and specify the correct path to your build of Clang. Then, in the zircon directory:  [这个非常小的shell脚本]（https://gist.github.com/karkhaz/c8ded50e564d73853731266fec729454）包装了爱立信的xtu-build-new`包装器。要对Zircon进行完整的分析，请确保先进行清洁，然后指定构建Clang的正确路径。然后，在zircon目录中：

```
ninja -t clean && ninja && ./run.sh
```
 

In order to build only the kernel, specify a `TARGET` as an environment variable:  为了只构建内核，请指定一个“ TARGET”作为环境变量：

```
ninja -t clean && ninja clean && TARGET=./build-zircon-pc-x64/zircon.elf ./run.sh
```
 

The script also requires [clangify.py](https://gist.github.com/karkhaz/2ab5e8c7a8783318d44ceca715f20438) to be in the zircon directory with executable bit set. After the analysis has finished, there will be a `.result-xtu` directory, containing:  该脚本还要求[clangify.py]（https://gist.github.com/karkhaz/2ab5e8c7a8783318d44ceca715f20438）位于具有可执行位设置的zircon目录中。分析完成后，将有一个.result-xtu目录，其中包含：

 
* A bunch of Apple plist files, which are the bug reports;  *一堆Apple plist文件，它们是错误报告；
* A fails directory, containing the std{out,err} of analyzer invocations that returned non-zero;  *失败目录，包含返回非零的分析器调用的std {out，err}；
* A passes directory, containing the std{out,err} of analyzer invocations that returned 0.  *通过目录，其中包含返回0的分析器调用的std {out，err}。

 
## Viewing analysis results  查看分析结果 

At the moment, the only way of parsing the plist reports and viewing them with a web interface is by using the [CodeChecker](https://github.com/Ericsson/codechecker) tool, which is developed at Ericsson and used for code comprehension and many other tasks. CodeChecker needs a large number of dependencies installed, and it’s best to install them with **pip** or **npm** or whatever rather than using **apt-get**. In short, after performing the analysis and dumping the plists into .result-xtu, you can invoke `CodeChecker plist` to parse the plists:  目前，解析plist报告并通过Web界面查看报告的唯一方法是使用[CodeChecker]（https://github.com/Ericsson/codechecker）工具，该工具在爱立信开发并用于代码理解力和许多其他任务。 CodeChecker需要大量安装的依赖性，而且最好有** PIP安装它们** **或** NPM或什么，而不是使用** apt-get的**。总之，执行分析和倾倒的Plist成。结果，湘潭后，你可以调用`CodeChecker plist`解析Plist档案：

```
CodeChecker plist -d .result-xtu -n 2016-12-12T21:47_uniq_name -j 48
```
 

The argument to `-n` needs to be unique on each invocation of `CodeChecker plist`, as it represents a single parse run. CodeChecker complains otherwise. Then, run `CodeChecker server` to start a webserver on `localhost:8001`, which will display the reports of all previous parsing runs.  在每次调用CodeChecker plist时，-n参数必须唯一，因为它表示单个解析运行。 CodeChecker则相反。然后，运行`CodeChecker server`在`localhost：8001`上启动一个网络服务器，它将显示以前所有解析运行的报告。

 
## Getting Help  获得帮助 

The Samsung patchset was authored by [Aleksei Sidorin](mailto:a.sidorin@samsung.com) and his team. Aleksei is quite knowledgeable about `ASTImporter.cpp` and other AST merging aspects, and was very helpful. He and [Sean Callanan](mailto:scallanan@apple.com) were happy to review my AST Importer patches. Aleksei also [gave a relevant talk](https://www.youtube.com/watch?v=jbLkZ82mYE4) about summary-based interprocedural analysis at the 2016 LLVM Developers Meeting.  三星补丁集由[Aleksei Sidorin]（mailto：a.sidorin@samsung.com）和他的团队撰写。 Aleksei对`ASTImporter.cpp`和其他AST合并方面非常了解，并且非常有帮助。他和[Sean Callanan]（mailto：scallanan@apple.com）很高兴查看我的AST Importer补丁。 Aleksei还在[2016年LLVM开发人员会议上]进行了基于总结的过程间分析的相关演讲[https://www.youtube.com/watch?v=jbLkZ82mYE4]。

The Ericsson patchset was authored by [Gábor Horváth](mailto:xazax.hun@gmail.com) and his team. Gábor was very helpful with advice on how to run CTU analysis with the `xtu-build-new` tools.  爱立信补丁集由[GáborHorváth]（mailto：xazax.hun@gmail.com）及其团队撰写。 Gábor对于如何使用xtu-build-new`工具运行CTU分析的建议非常有帮助。

I ([Kareem Khazem](mailto:karkhaz@karkhaz.com)) am also happy to help out where I can.  我（[Kareem Khazem]（mailto：karkhaz@karkhaz.com））也很乐意为您提供帮助。

The LLVM irc channel can also be helpful.  LLVM irc通道也可能会有所帮助。

 
## Zircon-specific analyses  锆石专用分析 

Upstream Clang has been very receptive to receiving patches for Zircon-specific Clang checkers. The [MutexInInterruptContext](https://reviews.llvm.org/D27854) checker is one example (ported from an LLVM pass written by Farid Molazem Tabrizi), as are the [SpinLockChecker](https://reviews.llvm.org/D26340) and [MutexChecker](https://reviews.llvm.org/D26342). Potential reviewers for Clang checks are Devin Coughlin (from Apple), Artem Dergachev (on Aleksei Sidorin’s team at Samsung) and Anna Zaks (also at Apple).  上游Clang非常乐于接受Zircon专用Clang检查器的补丁。 [MutexInInterruptContext]（https://reviews.llvm.org/D27854）检查器是一个示例（从Farid Molazem Tabrizi编写的LLVM通道移植），[Spin​​LockChecker]（https://reviews.llvm.org也是如此） / D26340）和[MutexChecker]（https://reviews.llvm.org/D26342）。可能进行Clang检查的审稿人包括来自Apple的Devin Coughlin，来自三星的Aleksei Sidorin团队的Artem Dergachev和来自苹果的Anna Zaks。

These checkers are typically *opt-in*, meaning that you need to pass a flag to the analyzer to enable them: something like `-analyzer-checker=optin.zircon.MutexInInterruptContext`.  这些检查器通常是“选择加入”的，这意味着您需要将一个标志传递给分析器以启用它们：类似“ -analyzer-checker = optin.zircon.MutexInInterruptContext”。

If those patches haven’t landed in Clang, you will need to apply them. To use them for analyzing Zircon with the [Ericsson wrapper scripts](#ericsson-wrapper-script), you should modify the [Fuchsia wrapper script](#fuchsia-wrapper-script) by adding the option `-e optin.zircon.MutexInInterruptContext` to the invocation of `xtu-analyze.py` at the end of the file. The patch for `MutexInInterruptContext` has a test suite, which can be used as an example of what the analysis is capable of.  如果这些补丁尚未登陆Clang，则需要应用它们。要将它们用于通过[Ericsson包装器脚本]（ericsson-wrapper-script）分析Zircon，应通过添加选项-e optin.zircon.MutexInInterruptContext来修改[紫红色包装器脚本]（fuchsia-wrapper-script）。在文件末尾调用xtu-analyze.py。 “ MutexInInterruptContext”的补丁有一个测试套件，可以用作分析功能的示例。

 
# Progress on CTU support in Zircon  Zircon中CTU支持的进展 

 
## Problems fixed in the AST importer  AST导入器中解决的问题 

The upstream CSA crashes on the vast majority of Zircon files. This section describes some of the problems that Kareem Khazem encountered and their fixes.  上游CSA在绝大多数Zircon文件上崩溃。本节描述了Kareem Khazem遇到的一些问题及其解决方法。

 
### Unsupported AST Nodes {#zircon-patches}  不支持的AST节点{zircon-patches} 

The Clang Static Analyzer is unable to import a lot of Zircon code, due to not having implemented support for importing certain kinds of AST nodes. Patches to support these nodes are listed here:  由于尚未实现对某些种类的AST节点的导入支持，因此Clang Static Analyzer无法导入很多Zircon代码。支持这些节点的补丁列在这里：

AtomicType                    | Patch merged into upstream ------------------------------|--------------------------------`CXXDependentScopeMemberExpr` | [`https://reviews.llvm.org/D26904`](https://reviews.llvm.org/D26904)`UnresolvedLookupExpr`        | [`https://reviews.llvm.org/D27033`](https://reviews.llvm.org/D27033)`DependentSizedArray`         | &nbsp;`CXXUnresolvedConstructExpr`  | &nbsp;`UsingDecl`                   | [`https://reviews.llvm.org/D27181`](https://reviews.llvm.org/D27181)`UsingShadowDecl`             | [`https://reviews.llvm.org/D27181`](https://reviews.llvm.org/D27181)`FunctionTemplateDecl`        | [`https://reviews.llvm.org/D26904`](https://reviews.llvm.org/D26904) 原子类型|修补程序合并到上游------------------------------ | --------------- -----------------`CXXDependentScopeMemberExpr` | [`https：// reviews.llvm.org / D26904`]（https://reviews.llvm.org/D26904）`UnresolvedLookupExpr` | [`https：// reviews.llvm.org / D27033`]（https://reviews.llvm.org/D27033）`DependentSizedArray` | CXXUnresolvedConstructExpr | | UsingDecl` | [`https：// reviews.llvm.org / D27181`]（https://reviews.llvm.org/D27181）`UsingShadowDecl` | [`https：// reviews.llvm.org / D27181`]（https://reviews.llvm.org/D27181）`FunctionTemplateDecl` | [`https://reviews.llvm.org/D26904`](https://reviews.llvm.org/D26904）

In general, when implementing support for new node types, one must implement a `VisitNode` function in `ASTImporter.cpp`, and also unit tests and functional tests; Kareem’s patches above contain examples. There are still quite a few unsupported AST nodes remaining; grep the analyzer output directory for `error: cannot import unsupported AST node`.  通常，在实现对新节点类型的支持时，必须在ASTImporter.cpp中实现“ VisitNode”功能，以及单元测试和功能测试。上面Kareem的补丁包含示例。仍然还有许多不受支持的AST节点； grep分析器输出目录的错误：无法导入不受支持的AST节点。

The Ericsson patchset contains only a subset of the `ASTImporter` code in the Samsung patchset. In some cases, the `Visit` function for an unsupported node can be taken straight from the Samsung patchset. However, the Samsung patchset does not include any tests, so it will still be necessary to write tests before the support for that node is upstreamed.  爱立信补丁集仅包含三星补丁集中“ ASTImporter”代码的一部分。在某些情况下，可以直接从Samsung补丁集获取不支持节点的“访问”功能。但是，三星补丁集不包含任何测试，因此仍需要在对该节点的支持上行之前编写测试。

 
### Segfaults galore  Segfaults嘉豪 

A lot of the code in `ASTImporter.cpp` is buggy. Sometimes Aleksei has private patches for issues, like [this one](https://reviews.llvm.org/D26753), so it’s worth giving him (**a-sid**) a quick ping on IRC. My strategy for debugging is to look through the wrapper output for the *second* string starting with `analyze: DEBUG: exec command in` (followed by the actual command line of the analyzer), and running that command line through gdb. It often takes only a few hours to track down where a segfault is coming from.  ASTImporter.cpp中的许多代码都是错误的。有时Aleksei拥有针对此问题的私人补丁程序，例如[this]（https://reviews.llvm.org/D26753），因此值得对他（** a-sid **）进行快速IRC查验。我的调试策略是从包装器输出中查找* second *字符串，该字符串以`analyze：DEBUG：exec command in`（随后是分析器的实际命令行）开头，然后通过gdb运行该命令行。通常只需要几个小时就可以找出分段错误的来源。

 
## Bugs found before and after CTU  在CTU之前和之后发现的错误 

 
### Possible bug in VFS?  VFS中可能存在错误？ 

This is a double-free of `oldparent`, which is declared uninitialized on `system/ulib/fs/vfs.c:vfs_rename`. Two lines later, `vfs_walk` (same file) is called with `oldparent` as its second argument. It is possible to return from `vfs_walk` without assigning to `oldparent` by entering the for loop and hitting the `return r` statement on the first loop. If the value of `r` is greater than zero, then we go to the `else if` statement, which calls `vn_release` on `oldparent` (which is still uninitialized).  这是`oldparent`的双重释放，它在`system / ulib / fs / vfs.c：vfs_rename`上声明为未初始化。两行之后，调用`vfs_walk`（相同的文件），并以`oldparent`作为第二个参数。通过进入for循环并在第一个循环中点击return r语句，可以从vfs_walk返回而不分配给oldparent。如果r的值大于零，则转到else if语句，该语句在oldparent上调用vn_release（仍未初始化）。

 
### Possible bug in thread?  线程中可能存在错误？ 

This is a use-after-free. The path is:  这是无用的。路径是：

 
* `kernel/kernel/thread.c:thread_detach_and_resume`  *`kernel / kernel / thread.c：thread_detach_and_resume`
    * Call `thread_detach(t)`  *呼叫`thread_detach（t）`
        * Return `thread_join(t, NULL, 0)`  *返回`thread_join（t，NULL，0）`
            * free `t` and return `NO_ERROR`  *免费`t`并返回`NO_ERROR`
        * Return `NO_ERROR`  *返回`NO_ERROR`
    * Check for error is 1false1  *检查错误为1false1
    * Call `thread_resume(t)`, which has been freed.  *调用已被释放的“ thread_resume（t）”。
        * `thread_resume` then accesses `t`’s fields.  *然后`thread_resume`访问`t`的字段。

 
## CTU false positives  CTU误报 

 
* The CSA cannot resolve the implementation of functions that are called through function pointers. This means that it cannot make any assumptions about what the return value of the function might be, nor any effects that the function might have on output parameters.  * CSA无法解析通过函数指针调用的函数的实现。这意味着它不能对函数的返回值做任何假设，也不能对函数对输出参数的影响做任何假设。
* There are several classes of function whose implementations are not accessible to the analyzer. Again, the analyzer cannot know that such functions touch their output arguments, so they will spuriously report that the following code reads from a garbage value:  *分析器无法访问其功能的几种类别。再次，分析器无法知道此类函数是否触及它们的输出参数，因此它们会虚假地报告以下代码是从垃圾值中读取的：

  ```
  struct timeval tv;
  gettimeofday(&tv, NULL);
  printf("%d\n", tv.tv_usec);   // [SPURIOUS REPORT] Access to
                                // uninitialized variable ‘tv’
  ```
 

 
* Some kinds of functions that are vulnerable to this kind of imprecision include:  *易受这种不精确性影响的某些功能包括：
    * System calls (like `gettimeofday`)  *系统调用（如“ gettimeofday”）
