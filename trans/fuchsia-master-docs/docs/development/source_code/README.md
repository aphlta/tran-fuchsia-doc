 
# Fuchsia Source  紫红色的来源 

Fuchsia uses the `jiri` tool to manage git repositories. This tool manages a set of repositories specified by a manifest. Jiri is located at[https://fuchsia.googlesource.com/jiri](https://fuchsia.googlesource.com/jiri). 紫红色使用`jiri`工具来管理git仓库。该工具管理清单所指定的一组存储库。 Jiri位于[https://fuchsia.googlesource.com/jiri](https://fuchsia.googlesource.com/jiri）。

See [Source code layout](layout.md) for an overview of how the Fuchsia repository is organized. 有关紫红色存储库的组织方式的概述，请参见[源代码布局]（layout.md）。

For how to prepare your developer environment and build Fuchsia, see Fuchsia's [Getting Started](/docs/getting_started.md) doc. 有关如何准备开发人员环境和构建Fuchsia的方法，请参见Fuchsia的[Getting Started]（/ docs / getting_started.md）文档。

 
## Creating a new Fuchsia checkout  创建一个新的紫红色结帐 

Fuchsia provides a bootstrap script that sets up your development environment and syncs with the Fuchsia source repository. It requires that you have thefollowing installed and up to date: Fuchsia提供了一个引导脚本，该脚本可设置您的开发环境并与Fuchsia源存储库同步。它要求您已安装以下最新版本：

 
 * Curl  *卷曲
 * Python  * Python
 * Unzip  *解压缩
 * Git  * Git

 
 1. To install these tools, run the following script. This command will install them if they are missing or update if they exist.  1.要安装这些工具，请运行以下脚本。如果缺少它们，此命令将对其进行安装；如果存在，则将对其进行更新。

    ```
    sudo apt-get install build-essential curl git python unzip
    ```
 

 
 1. Go to the directory where you want to set up your workspace for the Fuchsia codebase. This can be anywhere, but this example uses your home directory. 1.转到要为Fuchsia代码库设置工作区的目录。它可以在任何地方，但是本示例使用您的主目录。

    ```
    cd ~
    ```
 

 
 1. Run the script to bootstrap your development environment. This script automatically creates a `fuchsia` directory for the source code: 1.运行脚本以引导您的开发环境。这个脚本会自动为源代码创建一个“ fuchsia”目录：

    ```
    curl -s "https://fuchsia.googlesource.com/fuchsia/+/master/scripts/bootstrap?format=TEXT" | base64 --decode | bash
    ```
 

Downloading Fuchsia source can take up to 60 minutes.  下载紫红色源可能需要60分钟。

 
### Setting up environment variables  设置环境变量 

Upon success, the bootstrap script should print a message recommending that you add the `.jiri_root/bin` directory to your PATH. This will add `jiri` to yourPATH, which is recommended and is assumed by other parts of the Fuchsiatoolchain. 成功后，引导脚本应显示一条消息，建议您将.jiri_root / bin目录添加到PATH中。这将在您的PATH中添加“ jiri”，这是推荐的，并且由Fuchsiatoolchain的其他部分采用。

Another tool in `.jiri_root/bin` is `fx`, which helps configuring, building, running and debugging Fuchsia. See `fx help` for all available commands. .jiri_root / bin中的另一个工具是fx，它可以帮助配置，构建，运行和调试紫红色。有关所有可用命令，请参见`fx help`。

You can also source `scripts/fx-env.sh`, but sourcing `fx-env.sh` is not required. It defines a few environment variables that are commonly used in thedocumentation, such as `$FUCHSIA_DIR`, and provides useful shell functions, forinstance `fd` to change directories effectively. See comments in`scripts/fx-env.sh` for more details. 您也可以获取`scripts / fx-env.sh`的源代码，但不需要采购`fx-env.sh`。它定义了一些文档中常用的环境变量，例如$ FUCHSIA_DIR，并提供了有用的shell函数，例如fd可以有效地更改目录。有关更多详细信息，请参见scripts / fx-env.sh中的注释。

 
### Working without altering your PATH  在不改变路径的情况下工作 

If you don't like having to mangle your environment variables, and you want `jiri` to "just work" depending on your current working directory, just copy`jiri` into your PATH.  However, **you must have write access** (without `sudo`)to the **directory** into which you copy `jiri`.  If you don't, then `jiri`will not be able to keep itself up-to-date. 如果您不喜欢修改环境变量，并且希望`jiri`根据当前工作目录“正常工作”，只需将`jiri`复制到PATH中即可。但是，**您必须对复制`jiri`的目录**具有写访问权限（没有`sudo`）。如果您不这样做，那么`jiri`将无法使其保持最新状态。

```
cp .jiri_root/bin/jiri ~/bin
```
 

To use the `fx` tool, you can either symlink it into your `~/bin` directory:  要使用`fx`工具，可以将其符号链接到`〜/ bin`目录中：

```
ln -s `pwd`/scripts/fx ~/bin
```
 

or just run the tool directly as `scripts/fx`. Make sure you have **jiri** in your PATH. 或者只是直接以`scripts / fx`运行该工具。确保PATH中有** jiri **。

 
## Who works on the code  谁负责代码 

In the root of every repository and in many other directories are OWNERS files. These list email addresses of individuals who arefamiliar with and can provide code review for the contents of thecontaining directory. See [owners.md](owners.md) for morediscussion. OWNERS文件在每个存储库的根目录以及许多其他目录中。这些列出了熟悉的个人的电子邮件地址，并可以提供对包含目录内容的代码审查。有关更多讨论，请参见[owners.md]（owners.md）。

 
## How to handle third-party code  如何处理第三方代码 

See the [guidelines](third-party-metadata.md) on writing the metadata for third-party code in README.fuchsia files. 有关在README.fuchsia文件中编写第三方代码的元数据，请参阅[guidelines]（third-party-metadata.md）。

 
## Troubleshooting  故障排除 

 
### Authentication errors  验证错误 

