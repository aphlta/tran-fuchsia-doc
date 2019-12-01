 
# Helpful Vim tools for Fuchsia development  紫红色开发有用的Vim工具 

 
## Features  特征 

 
* Configure [YouCompleteMe](youcompleteme.md) to provide error checking, code completion, and source navigation within the Fuchsia tree. *配置[YouCompleteMe]（youcompleteme.md）以在紫红色的树中提供错误检查，代码完成和源导航。
* Set path so that `:find` and `gf` know how to find files.  *设置路径，以便`：find`和`gf`知道如何查找文件。
* Fidl syntax highlighting (using /lib/fidl/tools/vim/).  * Fidl语法高亮显示（使用/ lib / fidl / tools / vim /）。
* Basic build system integration so that `:make` builds and populates the QuickFix window. *基本的构建系统集成，以便`：make`可以构建并填充QuickFix窗口。

 
## Installation  安装 

 
1. Update your login script:  1.更新您的登录脚本：

   Steps #2 and #3 depend on configuration set by the `fx set` command. Add these lines to your startup script (typically `~/.bashrc`). 第2步和第3步取决于`fx set`命令设置的配置。将这些行添加到您的启动脚本中（通常是〜/ .bashrc）。

   ```shell
   export FUCHSIA_DIR=/path/to/fuchsia-dir
   fx set core.x64
   ```
 

 
1. Update your vim startup file:  1.更新您的vim启动文件：

   If this line exists in your `~/.vimrc file`, remove it:  如果您的〜/ .vimrc文件中存在此行，请将其删除：

   ```
   filetype plugin indent on
   ```
 

   Then add these lines to your `~/.vimrc`.  然后将这些行添加到您的〜/ .vimrc中。

   ```
   if $FUCHSIA_DIR != ""
     source $FUCHSIA_DIR/scripts/vim/fuchsia.vim
   endif
   filetype plugin indent on
   ```
 

 
1. Install YouCompleteMe (YCM):  1.安装YouCompleteMe（YCM）：

   Optionally [install YouCompleteMe](youcompleteme.md) for fancy completion, source navigation and inline errors. （可选）[安装YouCompleteMe]（youcompleteme.md），以实现出色的完成效果，源导航和内联错误。

   If it's installed, `fuchsia.vim` configures YCM properly.  如果已安装，`fuchsia.vim`会正确配置YCM。

   If everything is working properly, you can place the cursor on an identifier in a .cc or .h file then hit Ctrl+], to navigateto the definition of the identifier. 如果一切正常，则可以将光标放在.cc或.h文件中的标识符上，然后按Ctrl +]，导航到标识符的定义。

   Use `fx compdb` to build a compilation database. YCM will use the compilation database which is more reliable and efficient thanthe default `ycm_extra_config.py` configuration. 使用`fx compdb`建立一个编译数据库。 YCM将使用比默认配置ycm_extra_config.py更可靠，更高效的编译数据库。

 
## TODO  去做 

In the future it would be nice to support:  将来最好支持：
* Fidl indentation  * Fidl缩进
* GN indentation  * GN缩进
* Dart, Go and Rust support  * Dart，Go和Rust支持
