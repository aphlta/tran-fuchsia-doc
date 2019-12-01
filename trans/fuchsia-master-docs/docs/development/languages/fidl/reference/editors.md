 
# Editors  编者 

Several editors have support for FIDL:  一些编辑器支持FIDL：

 
* [Atom](#atom)  * [Atom]（原子）
* [IntelliJ/Android Studio](#intellij)  * [IntelliJ / Android Studio]（智能）
* [Sublime Text](#sublime)  * [崇高文字]（崇高）
* [Vim](#vim)  * [Vim]（vim）
* [Visual Studio Code](#visual-studio-code)  * [Visual Studio代码]（visual-studio-code）

 
## Atom {#atom}  原子{atom} 

To install:  安装：

```
pushd ~/.atom/packages
git clone https://fuchsia.googlesource.com/atom-language-fidl
popd
```
 

 
## IntelliJ / Android Studio {#intellij}  IntelliJ / Android Studio {intellij} 

There is an IntelliJ plugin available for FIDL. It adds syntax and parsing support.To install it, select **Settings**, then **Plugins**, and then click**Browse Repositories** and search for **FIDL**. FIDL有一个IntelliJ插件。它添加了语法和解析支持。要安装它，请选择“设置”，然后选择“插件”，然后单击“浏览存储库”并搜索“ FIDL”。

 
## Sublime Text {#sublime}  崇高文字{sublime} 

[Sublime syntax highlighting support](/garnet/public/lib/fidl/tools/sublime).  [崇高语法高亮支持]（/ garnet / public / lib / fidl / tools / sublime）。

To install, select **Sublime Text**, then **Preferences**, then **Browse Packages** and copy the files `FIDL.sublime-syntax`, and`Comments (FIDL).tmPreferences` into the **User** package. 要安装，请选择“ Sublime Text”，然后选择“ Preferences”，然后选择“ Browse Packages”，然后将文件FIDL.sublime-syntax和Comments（FIDL）.tmPreferences复制到**中。用户**程序包。

 
## Vim {#vim}  Vim {vim} 

[Vim syntax highlighting support and instructions](/garnet/public/lib/fidl/tools/vim).  [Vim语法高亮显示支持和说明]（/ garnet / public / lib / fidl / tools / vim）。

 
## Visual Studio Code {#visual-studio-code}  Visual Studio代码{visual-studio-code} 

There is a an extension, [Visual Studio Code extension available](https://marketplace.visualstudio.com/items?itemName=fuchsia-authors.language-fidl). 有一个扩展，[可用Visual Studio代码扩展]（https://marketplace.visualstudio.com/items?itemName=fuchsia-authors.language-fidl）。

 
## Contributing  贡献 

Contributions to the various plugins are welcome. Their respective code is in:  欢迎为各种插件做出贡献。它们各自的代码在：

 
* [Atom](https://fuchsia.googlesource.com/atom-language-fidl/)  * [Atom]（https://fuchsia.googlesource.com/atom-language-fidl/）
* [IntelliJ](https://fuchsia.googlesource.com/intellij-language-fidl/)  * [IntelliJ]（https://fuchsia.googlesource.com/intellij-language-fidl/）
* [Sublime](/garnet/public/lib/fidl/tools/sublime)  * [Sublime]（/ garnet / public / lib / fidl / tools / sublime）
* [vim](/garnet/public/lib/fidl/tools/vim)  * [vim]（/ garnet / public / lib / fidl / tools / vim）
* [Visual Studio Code](https://fuchsia.googlesource.com/vscode-language-fidl/)  * [Visual Studio代码]（https://fuchsia.googlesource.com/vscode-language-fidl/）

