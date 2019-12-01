 
# YouCompleteMe integration  YouCompleteMe整合 

[YouCompleteMe](http://ycm-core.github.io/YouCompleteMe/) is a semantic code-completion engine. YouCompleteMe works natively with Vim but it can also beintegrated with other editors through [ycmd](https://github.com/Valloric/ycmd). [YouCompleteMe]（http://ycm-core.github.io/YouCompleteMe/）是一个语义代码完成引擎。 YouCompleteMe与Vim一起使用，但也可以通过[ycmd]（https://github.com/Valloric/ycmd）与其他编辑器集成。

 
### Install YouCompleteMe in your editor  在编辑器中安装YouCompleteMe{% dynamic if user.is_googler %}  {如果user.is_googler％，则为动态％}
#### gLinux (Googlers only)  gLinux（仅限Googlers） 

(This applies to anyone compiling on gLinux, even if editing over SSHFS on MacOS) See the Google intranet specific instructions [go/ycm](http://go/ycm). （这适用于在gLinux上编译的任何人，即使在MacOS上通过SSHFS进行编辑也是如此）。请参阅Google Intranet特定说明[go / ycm]（http：// go / ycm）。

You'll also need to setup `${FUCHSIA_DIR}/scripts/youcompleteme/default_settings.json` as the defaultsettings path in your editor, in order to disable the internal `use_clangd`flag. If you want to use clangd, you can additionally edit that file to set`use_clangd` to 1, and `clang_binary_path` to`${FUCHSIA_DIR}/prebuilt/third_party/clang/${HOST_PLATFORM}/bin/clangd`.Remember that in that case, you'll need to build a compilation database with`fx compdb`. 您还需要在编辑器中将$$ {FUCHSIA_DIR} / scripts / youcompleteme / default_settings.json`设置为默认设置路径，以禁用内部的“ use_clangd”标记。如果要使用clangd，则可以另外编辑该文件，以将use_clangd设置为1，将clang_binary_path设置为$ {FUCHSIA_DIR} / prebuilt / third_party / clang / $ {HOST_PLATFORM} / bin / clangd`。在这种情况下，您需要使用fx compdb建立编译数据库。

{% dynamic else %}  {％动态否则％}

See the [installation guide](https://github.com/Valloric/YouCompleteMe#installation). 请参阅[安装指南]（https://github.com/Valloric/YouCompleteMeinstallation）。

Note: Installing YCM on MacOS with Homebrew is not recommended because of library compatibility errors. Use the official installation guide instead. 注意：由于库兼容性错误，不建议在带有Homebrew的MacOS上安装YCM。请使用官方安装指南。

{%dynamic endif %}  {％dynamic endif％}

 
### Generate compilation database  生成编译数据库 

YouCompleteMe (and other tools like clang-tidy) require a [JSON compilation database](https://clang.llvm.org/docs/JSONCompilationDatabase.html) thatspecifies how each file is compiled. This database is normally stored in a filecalled `compile_commands.json`. You can build a compilation database with `fx compdb`,or `fx -i compdb` if you want it rebuilt automatically as you edit files. YouCompleteMe（和其他类似clang-tidy的工具）需要[JSON编译数据库]（https://clang.llvm.org/docs/JSONCompilationDatabase.html），用于指定每个文件的编译方式。该数据库通常存储在名为compile_commands.json的文件中。您可以使用`fx compdb`或`fx -i compdb`构建编译数据库，如果您希望在编辑文件时自动重建它。

If this database is not present, then VIM can be configured to fall back to the configuration in [/scripts/youcompleteme/ycm_extra_conf.py](/scripts/youcompleteme/ycm_extra_conf.py). See[VIM configuration](vim.md) for how to set this up. 如果此数据库不存在，则可以将VIM配置为回退到[/scripts/youcompleteme/ycm_extra_conf.py](/scripts/youcompleteme/ycm_extra_conf.py）中的配置。有关设置方法，请参见[VIM配置]（vim.md）。

 
### Use it  用它 

YouCompleteMe will use `compile_commands.json` to do code completion and find symbol definitions/declarations. See your editor's YouCompleteMe docs fordetails. The editor should pick up `compile_commands.json` file automatically. YouCompleteMe将使用compile_commands.json来完成代码并查找符号定义/声明。有关详细信息，请参见编辑器的YouCompleteMe文档。编辑器应自动提取`compile_commands.json`文件。

See [vim setup](vim.md) for instructions on configuring VIM for Fuchsia development.  有关为紫红色开发配置VIM的说明，请参见[vim设置]（vim.md）。

 
### Other editors (ycmd)  其他编辑（ycmd） 

You'll need to set the ycmd config option `global_ycm_extra_conf` to point to `${FUCHSIA_DIR}/scripts/youcompleteme/ycm_extra_conf.py`.Note you may need to manually replace `${FUCHSIA_DIR}` with the correct path. 您需要将ycmd配置选项“ global_ycm_extra_conf”设置为指向“ $ {FUCHSIA_DIR} /scripts/youcompleteme/ycm_extra_conf.py”。请注意，您可能需要使用正确的路径手动替换“ $ {FUCHSIA_DIR}”。

Alternatively, you can create a `.ycm_extra_conf.py` symbolic link to let YCM automatically find the config for any fuchsia repository: 另外，您可以创建一个.ycm_extra_conf.py符号链接，以使YCM自动查找任何紫红色存储库的配置：

```shell
ln -s $FUCHSIA_DIR/scripts/youcompleteme/ycm_extra_conf.py $FUCHSIA_DIR/.ycm_extra_conf.py
```
