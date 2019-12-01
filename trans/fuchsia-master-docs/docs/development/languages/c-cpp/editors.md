 
# C++ Editor/IDE Setup  C ++编辑器/ IDE设置 

[TOC]  [目录]

 
## CLion  里昂 

Follow the **Compilation Database** instructions below to create the appropriate project description file in the fuchsia root directory. 请按照下面的“编译数据库”说明在紫红色的根目录中创建适当的项目描述文件。

Then in CLion choose *Import Project from Sources* and select the fuchsia root directory. 然后在CLion中选择*“从源文件导入项目” *，然后选择紫红色根目录。

 
### CLion Performance Tweaks  CLion性能调整 

To improve performance you can try some or all of the following. They are only suggestions, we recommend checking with directly with JetBrainsat <https://intellij-support.jetbrains.com/hc> to be sure what worksbest for your environment. 要提高性能，您可以尝试以下一些或全部方法。这些仅是建议，我们建议直接与JetBrainsat <https://intellij-support.jetbrains.com/hc>进行联系，以确保最适合您的环境。

 
##### Exclude Directories  排除目录 

To speed up indexing time you can exclude directories you are not working with. You can do that in the Project View byright-clicking each directory and choosing*Mark directory as->Excluded*. Note the affected configuration is storedin `<project>/.idea/misc.xml` 为了加快索引时间，可以排除不使用的目录。您可以在项目视图中通过右键单击每个目录并选择*将目录标记为->已排除*来执行此操作。注意受影响的配置存储在`<project> /。idea / misc.xml`中。

See [Control Source, Library, and Exclude Directories \- Help \| CLion](https://www.jetbrains.com/help/clion/controlling-source-library-and-exclude-directories.html)for more information. 请参见[控制源，库和排除目录\-帮助\ | CLion]（https://www.jetbrains.com/help/clion/controlling-source-library-and-exclude-directories.html）了解更多信息。

 
##### Unregister Git Repositories  注销Git存储库 

The fuchsia source tree has a fair number of git repositories. Scanning them can use CPU cycles for CLion. You can unregister the gitrepositories you are not working on under*File -> Settings -> Version Control*. They will still be listed thereso you can add them back later if needed. 紫红色的源代码树有大量的git存储库。扫描它们可以使用CLion的CPU周期。您可以在*文件->设置->版本控制*下注销未使用的gitrepository。它们仍将在此处列出，因此您以后可以根据需要将它们重新添加。

 
##### Tune JVM Options and Platform Properties  调整JVM选项和平台属性 

See [Tuning CLion \- Help \| CLion](https://www.jetbrains.com/help/clion/tuning-the-ide.html)for general tips on tweaking CLion JVM Options and Platform Properties.As that link suggests, contact CLion support for instructionsregarding the options and values that might help you with whatever issueyou are trying to solve. 请参阅[调整CLion \-帮助\ | CLion]（https://www.jetbrains.com/help/clion/tuning-the-ide.html），了解有关调整CLion JVM选项和平台属性的一般提示。如该链接所示，请联系CLion支持以获取有关选项和操作的说明。可以帮助您解决任何问题的值。

 
## VIM  VIM 

See [Helpful Vim tools for Fuchsia development](/scripts/vim/README.md).  请参见[用于紫红色开发的有用的Vim工具]（/ scripts / vim / README.md）。

 
## Visual Studio Code (vscode) {#visual-studio-code}  Visual Studio代码（vscode）{visual-studio-code} 

There are multiple vscode setups known to work to different degrees. The sections below describe the different setups (pick one). 已知有多个vscode设置可以在不同程度上起作用。以下各节介绍了不同的设置（选择一项）。

 
### clangd  lang 

Install [vscode-clangd](https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.vscode-clangd).Disable the default C/C++ extension if you have it installed. 安装[vscode-clangd]（https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.vscode-clangd）。如果已安装，则禁用默认的C / C ++扩展名。

In settings, add:  在设置中，添加：

```
"clangd.path": "<absolute path to fuchsia root directory>/prebuilt/third_party/clang/<platform>/bin/clangd",
```
 

Note: the path to clangd does need to be absolute.  注意：clangd的路径确实需要是绝对的。

Finally, follow the **Compilation Database** instructions below to generate the `compile_commands.json` in the fuchsia root directory. Thenreload vscode to enjoy the results. 最后，按照下面的“编译数据库”说明在紫红色的根目录中生成“ compile_commands.json”。然后重新加载vscode即可享受结果。

You may also benefit from enabling background indexing and clang-tidy using the following settings:  您还可以使用以下设置来启用后台索引和clang-tidy，从而从中受益：

```
"clangd.arguments": [
    "-clang-tidy",
    "-background-index"
]
```
 

Further details on clangd setup can be found [here](https://clang.llvm.org/extra/clangd/Installation.html).  有关clangd设置的更多详细信息，请参见[here]（https://clang.llvm.org/extra/clangd/Installation.html）。

 
### default vscode C++ extension  默认的vscode C ++扩展 

Install the default [C/C++ extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) suggested by vscode. 安装vscode建议的默认[C / C ++扩展名]（https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools）。

You can use [tasks](https://code.visualstudio.com/docs/editor/tasks) to configure a compilation step. 您可以使用[任务]（https://code.visualstudio.com/docs/editor/tasks）来配置编译步骤。

 
## Compilation Database (fx compdb)  编译数据库（fx compdb） 

A [Compilation Database](https://clang.llvm.org/docs/JSONCompilationDatabase.html) filecan be generated using `fx compdb`. This will create/update the file`compile_commands.json` in the fuchsia root directory. When you add,delete, or rename source files the command needs to be rerun to updatethe `compile_commands.json` file. 可以使用`fx compdb`生成[编译数据库]（https://clang.llvm.org/docs/JSONCompilationDatabase.html）文件。这将在紫红色的根目录中创建/更新文件compile_commands.json。添加，删除或重命名源文件时，需要重新运行命令以更新compile_commands.json文件。

Note that this file is only intended to help the IDE find and parse the source files. Building should still be done with `fx build`. 请注意，此文件仅用于帮助IDE查找和解析源文件。仍然应该使用`fx build`完成构建。

