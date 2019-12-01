 
# Packages  配套 

A package is the unit of installation on a Fuchsia system.  软件包是在紫红色系统上安装的单位。

 
## Anatomy  解剖学 

_To be added..._  _要添加..._

 
## Working with packages  使用软件包 

The majority of these instructions rely on the `pm` tool which is available in `//tools`. 这些指令大部分依赖于`// tools`中的`pm`工具。

This document describes the various steps to build and install a package:  本文档介绍了构建和安装软件包的各个步骤：

 
* [Build a package](#build-package)  * [构建软件包]（build-package）
* [Publish a package](#publish-package)  * [发布程序包]（发布程序包）
* [Install a package](#install-package)  * [安装软件包]（安装软件包）
* [Run a component from an installed package](#run-component)  * [从已安装的程序包运行组件]（运行组件）

For more details about each step, see `pm`'s help messages.  有关每个步骤的更多详细信息，请参见`pm`的帮助消息。

 
### Build a package {#build-package}  构建一个软件包{build-package} 

To build a package:  要构建一个包：

 
1. Create the package ID file:  1.创建程序包ID文件：

   Note: `$PACKAGE_DIR` is a staging directory where the package is built. 注意：`$ PACKAGE_DIR`是构建软件包的临时目录。

   ```
   pm -o $PACKAGE_DIR -n $PACKAGE_NAME init
   ```
 

   This generates the package ID file implicitly as `$PACKAGE_DIR/meta/package`.  Set `$PACKAGE_ID_FILE` accordinglyfor use in subsequent steps: 这将隐式生成软件包ID文件，如$ PACKAGE_DIR / meta / package。相应地设置`$ PACKAGE_ID_FILE`以便在后续步骤中使用：

   ```
   export PACKAGE_ID_FILE=${PACKAGE_DIR}/meta/package
   ```
 

   `$PACKAGE_ID_FILE` will contain the following data:  $ PACKAGE_ID_FILE将包含以下数据：

   ```
   {
     "name": "<package name>",
     "version": "<package version>"
   }
   ```
 

 
2. Create the manifest file, `$MANIFEST_FILE`, that provides the path to the package ID file.  Each line of a manifest file maps a single file thatis contained in the package and is in the form of `destination=source` where: 2.创建清单文件$ MANIFEST_FILE，该清单文件提供包ID文件的路径。清单文件的每一行都映射一个文件，该文件包含在软件包中，格式为`destination = source'，其中：

 
   * `destination` is the path to the file in the final package  *`destination`是最终包中文件的路径
   * `source` is the path to the file on the host machine  *`source`是主机上文件的路径

   The manifest file must include at least one line for the package ID file like this: 清单文件必须至少包含一行用于包ID文件的行，如下所示：

   ```
   meta/package=<package ID file>
   ```
 

 
3. Generate the package metadata archive:  3.生成软件包元数据存档：

   ```
   pm -o $PACKAGE_DIR -m $MANIFEST_FILE build
   ```
 

   This creates the metadata archive at `$PACKAGE_DIR/meta.far`.  这将在$ PACKAGE_DIR / meta.far中创建元数据存档。

 
4. Create the package archive `$PACKAGE_ARCHIVE`:  4.创建软件包归档文件“ $ PACKAGE_ARCHIVE”：

   ```
   pm -o $PACKAGE_DIR -m $MANIFEST_FILE archive
   ```
 

   This command creates the package archive implicitly as `$PACKAGE_DIR/$PACKAGE_NAME-0.far`.  Set `$PACKAGE_ARCHIVE` accordinglyfor use in subsequent steps: 该命令隐式创建软件包归档文件为$ PACKAGE_DIR / $ PACKAGE_NAME-0.far。相应地设置`$ PACKAGE_ARCHIVE`以便在后续步骤中使用：

   ```
   export PACKAGE_ARCHIVE=${PACKAGE_DIR}/${PACKAGE_NAME}-0.far
   ```
 

   If the contents of the package change, you need to re-run the `pm -o $PACKAGE_DIR -m $MANIFEST_FILE archive` command. 如果软件包内容更改，则需要重新运行`pm -o $ PACKAGE_DIR -m $ MANIFEST_FILE archive`命令。

You have succesfully built a package. You are now ready to publish the package.  您已经成功构建了一个程序包。现在您可以发布该程序包了。

 
### Publish a package {#publish-package}  发布包{publish-package} 

To publish a package:  要发布软件包：

 
1. Initialize a directory, `$REPO`, that serves as a packages repository:  1.初始化目录$ REPO，它用作软件包存储库：

   ```
   pm newrepo -repo $REPO
   ```
 

   This creates a directory structure named `$REPO` that is ready for publishing packages. 这将创建一个名为$ REPO的目录结构，该目录结构可用于发布程序包。

 
2. Publish packages to the repository `$REPO`:  2.将软件包发布到存储库$ REPO中：

   ```
   pm publish -a -r $REPO -f $PACKAGE_ARCHIVE
   ```
 

   `pm publish` parses `$PACKAGE_ARCHIVE` and publishes the package in the provided `$REPO` directory. If you run this command multiple times withdifferent package archives, `pm publish` publishes the packages to the samerepository. New versions of a same package can be published using the samecommand. `pm publish`解析`$ PACKAGE_ARCHIVE`并将包发布在提供的`$ REPO`目录中。如果您使用不同的软件包归档文件多次运行此命令，则`pm publish`会将软件包发布到相同的存储库中。可以使用相同的命令发布同一软件包的新版本。

You have successfully published a package. You are now ready to install a package. 您已经成功发布了一个程序包。现在您可以安装软件包了。

 
### Install a package {#install-package}  安装软件包{install-package} 

To install a package:  要安装软件包：

 
1. Start the package server:  1.启动软件包服务器：

   ```
   pm serve -repo $REPO
   ```
 

   By default, this starts an amber server on the host machine at port `8083`.  默认情况下，这将启动主机上端口“ 8083”上的琥珀色服务器。

 
2. (On the target device) Add the new repository as an update source with `amberctl`: 2.（在目标设备上）使用`amberctl`将新存储库添加为更新源：

   ```
   amberctl add_repo_cfg -n $REPO -f http://$HOST_ADDRESS:8083/config.json
   ```
 

   If the component is not already on the system, `amberctl` installs the package. If the package already exists, `amberctl` installs any package updates. 如果该组件尚未在系统上，则`amberctl`将安装该软件包。如果软件包已经存在，`amberctl`将安装所有软件包更新。

You have successfully installed or updated the package. You are now ready to run a component from the installed package. 您已经成功安装或更新了软件包。现在您可以从已安装的程序包中运行组件。

 
### Run a component from an installed package {#run-component}  从已安装的程序包运行组件{run-component} 

To run a component published in a package:  运行包中发布的组件：

 
1. (On the target device) Run:  1.（在目标设备上）运行：

  Note: `$COMPONENT_URI` is in this form `fuchsia-pkg://${REPO}/${PACKAGE_NAME}#meta/<component name>.cmx`. 注意：$ COMPONENT_URI的格式为fuchsia-pkg：// $ {REPO} / $ {PACKAGE_NAME} meta / <组件名称> .cmx。

  ```
  run $COMPONENT_URI
  ```
 

You have succesfully run a component from the installed package.  您已成功从已安装的程序包中运行组件。

