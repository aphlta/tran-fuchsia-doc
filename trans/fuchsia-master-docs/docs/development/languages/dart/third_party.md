 
# Third-party Dart packages  第三方Dart套件 

 

There are two types of third-party dependencies in the Fuchsia tree:  紫红色的树中有两种类型的第三方依赖项：

 
- extracted from [pub][pub];  -从[pub] [pub]中摘录；
- sync'd from Git.  -从Git同步。

 
## Pub dependencies  酒馆依赖 

Pub dependencies are host at [`//third-party/dart-pkg`][dart-3p]. That project is regularly kept up-to-date with [a script][dart-3p-script] that relies on the`pub` tool to resolve versions and fetch sources for the packages that are usedin the tree.This script uses a set of canonical local packages which are assumed to beproviding the necessary package coverage for the entire tree. Pub依赖项位于[`// third-party / dart-pkg`] [dart-3p]中。该项目会定期使用[pub]工具来更新项目，该脚本依靠pub工具来解析版本并获取树中使用的包的源。此脚本使用一组规范的本地包的数量，假定它们为整个树提供了必要的包覆盖率。

Additionally, projects may request third-party dependencies to be imported through the following procedure: 此外，项目可能要求通过以下过程导入第三方依赖项：

 
1. create a `dart_dependencies.yaml` file in the project  1.在项目中创建一个dart_dependencies.yaml文件
2. add the desired dependencies in that file:  2.在该文件中添加所需的依赖项：

```
name: my_project
dependencies:
  foo: ^4.0.0
  bar: >=0.1.0
```
 

 
3. add a reference to the file in `//scripts/dart/update_3p_packages.py`  3.在`// scripts / dart / update_3p_packages.py`中添加对该文件的引用
4. run that script  4.运行该脚本
5. merge your changes to `dart_dependencies.yaml` to master  5.合并对“ dart_dependencies.yaml”的更改以掌握
6. merge the files downloaded by running the 'update_3p_packages.py' script, and the script itself, to master.  6.将通过运行“ update_3p_packages.py”脚本和脚本本身下载的文件合并到master。
7. in the '//topaz/manifest/dart' manifest, update the project node 'third_part/dart-pkg' revision attribute with the SHA from your commit in step 6.  7.在“ // topaz / manifest / dart”清单中，使用步骤6中的提交用SHA更新项目节点“ third_part / dart-pkg”修订版属性。
8. merge your change to the '//topaz/manifest/dart' manifest file to master.  8.将您的更改合并到“ // topaz / manifest / dart”清单文件中以进行更改。

 

