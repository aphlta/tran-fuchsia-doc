 
# Fuchsia Packages  紫红色包 

A Fuchsia package is one or more collections of files that provide one or more programs, components or services for a Fuchsia system. A Fuchsia package is aterm representing a unit of distribution, though unlike many other packagesystems, that unit is composed of parts. 紫红色的软件包是一个或多个文件集合，这些文件为紫红色的系统提供一个或多个程序，组件或服务。紫红色的包装是代表分配单位的术语，尽管与许多其他包装系统不同，该单位是由零件组成的。

 
## meta.far  元远 

A package as "built" by the `pm` tool is a tree of zero or more content-addressed items. At the top of this tree is a Fuchsia Archivecommonly named `meta.far`. 由pm工具“构建”的软件包是一棵零个或多个内容寻址项的树。在这棵树的顶部是一个倒挂金钟档案馆，俗称“ meta.far”。

`meta.far` contains the `meta/` directory provided as an input to a package build, and contains at minimum two files, described below. It can alsocontain additional metadata items, such as component manifests. “ meta.far”包含作为包构建输入的“ meta /”目录，并且至少包含两个文件，如下所述。它还可以包含其他元数据项，例如组件清单。

meta/package : The package identity file is a JSON file containing the name and version of: the package. meta / package：软件包标识文件是一个JSON文件，其中包含该软件包的名称和版本。

meta/contents : The contents file, typically produced automatically by `pm update` (an: implied step in `pm build`) maps the user-facing file names of a package,: to the content-addresses ([Merkle Root](/docs/concepts/storage/merkleroot.md)): of those files. meta / contents：内容文件通常由pm update自动生成（在pm build中是隐含的步骤），它将包的面向用户的文件名映射到内容地址（[Merkle Root]（ /docs/concepts/storage/merkleroot.md））：这些文件。

The format of `meta/package` and `meta/contents` are considered private specification at this time, and may be subject to change. “ meta / package”和“ meta / contents”的格式目前被视为私有规范，可能会随时更改。

 
## Additional Metadata Items  其他元数据项 

