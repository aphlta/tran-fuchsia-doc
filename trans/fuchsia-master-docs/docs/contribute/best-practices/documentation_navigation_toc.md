 
# Change table of contents navigation  更改目录导航 

The table of contents is the list of documents that is displayed on the left side of every page on fuchsia.dev. It is represented by a hierarchical set of`_toc.yaml` files. The top level `_toc.yaml` file is[`_toc.yaml`](https://fuchsia.googlesource.com/fuchsia/+show/master/docs/_toc.yaml). 目录是显示在fuchsia.dev每页左侧的文档列表。它由_toc.yaml文件的分层集表示。顶级的_toc.yaml文件是[`_toc.yaml`]（https://fuchsia.googlesource.com/fuchsia/+show/master/docs/_toc.yaml）。

If you add a new document or if you want to change how existing documents are organized in the source documentation section of[fuchsia.dev](/docs), you need to change the navigation table of contents, defined in`_toc.yaml` files. These files are located in the same directory ofthe documentation file or in a parent directory. 如果添加新文档，或者要更改[fuchsia.dev]（/ docs）的源文档部分中现有文档的组织方式，则需要更改在_toc.yaml中定义的导航目录。文件。这些文件位于文档文件的同一目录或父目录中。

 
## Existing document  现有文件 

To change the documentation navigation for an existing document:  要更改现有文档的文档导航：

 
1. Locate the corresponding `_toc.yaml` file for the document in the source code tree. 1.在源代码树中找到文档的相应“ _toc.yaml”文件。

   For example, if you want to modify the navigation for the [concepts page of Zircon](/docs/concepts/kernel/concepts.md),you can see that there is a[`_toc.yaml`](https://fuchsia.googlesource.com/fuchsia/+show/master/docs/concepts/kernel/_toc.yaml)file in the same directory. 例如，如果您想修改[Zircon的概念页面]（/ docs / concepts / kernel / concepts.md）的导航，则可以看到其中有一个[`_toc.yaml`]（https：//同一目录中的fuchsia.googlesource.com/fuchsia/+show/master/docs/concepts/kernel/_toc.yaml）文件。

 
1. Edit the `_toc.yaml` file. You have to specify the published location of the document in the`_toc.yaml` files instead of the actual path in the Fuchsia sourcecode. See [`_toc.yaml` reference](#toc-reference). 1.编辑`_toc.yaml`文件。您必须在_toc.yaml文件中指定文档的发布位置，而不是紫红色源代码中的实际路径。参见[`_toc.yaml`参考]（toc-reference）。

 
## New document  新文件 

To add navigation for a new document:  要为新文档添加导航：

 
1. Locate the closest `_toc.yaml` file for the document. If the directory where you createdthe document has a `_toc.yaml` file, use that file. If not, navigate throughthe parent directories until you locate the closest `_toc.yaml` file. 1.找到最接近文档的“ _toc.yaml”文件。如果创建文档的目录中有一个_toc.yaml文件，请使用该文件。如果不是，请浏览父目录，直到找到最近的`_toc.yaml`文件。

 
1. Edit the `_toc.yaml` file. See [`_toc.yaml` reference](#toc-reference). 1.编辑`_toc.yaml`文件。参见[`_toc.yaml`参考]（toc-reference）。

 
## `_toc.yaml` reference {#toc-reference}  `_toc.yaml`参考{toc-reference} 

A `_toc.yaml` file can contain single entries or expandable sections with multiple entries: _toc.yaml文件可以包含单个条目或具有多个条目的可扩展部分：

 
* Single entry  *一次入境

  A single entry in the table of contents navigation is represented by a title and a path in the corresponding `_toc.yaml` file. Each entry must also usethe correct indentation like the other entries in `_toc.yaml`. 目录导航中的单个条目由相应的“ _toc.yaml”文件中的标题和路径表示。每个条目还必须使用正确的缩进，如_toc.yaml中的其他条目。

  Paths must follow these requirements:  路径必须遵循以下要求：

 
  * Paths to files should be the full path from the root of the project. For example, `/docs/development/api/cli.md`. *文件路径应该是从项目根目录开始的完整路径。例如`/ docs / development / api / cli.md`。
  * Paths to directories should not include a trailing slash, and the directory must have a file named `README.md`. *目录路径中不应包含斜杠，并且目录中必须包含名为“ README.md”的文件。

  For example, to add an entry for the Zircon `concepts.md` page in its respective [`_toc.yaml`](https://fuchsia.googlesource.com/fuchsia/+show/master/docs/concepts/kernel/_toc.yaml),you should add an entry: 例如，要在Zircon`concepts.md`页面的相应[`_toc.yaml`]（https://fuchsia.googlesource.com/fuchsia/+show/master/docs/concepts/kernel/ _toc.yaml），则应添加一个条目：

  ```
  - title: "Kernel concepts"
    path: /docs/concepts/kernel/concepts.md
  ```
 

 
* Expandable section  *展开部分

  An expandable section is an expandable group of multiple entries in a table of contents. For example, see the expandable sections, such as Networkingand Graphics, in the[Concepts section](/docs/concepts/README.md). Each expandablesection has an arrow to the left of the section name. 可扩展节是目录中包含多个条目的可扩展组。例如，请参阅[概念部分]（/ docs / concepts / README.md）中的可扩展部分，例如网络和图形。每个可扩展节的节名左侧都有一个箭头。

  You can create a group of entries with a `section` element. Each section must also use the correct indentation like the other entries in `_toc.yaml`. Then,you can add single entries to the section. 您可以使用`section`元素创建一组条目。每个部分也必须使用正确的缩进，如_toc.yaml中的其他条目。然后，您可以将单个条目添加到该部分。

  For example, to add a section in the "System" table of contents [`_toc.yaml`](https://fuchsia.googlesource.com/fuchsia/+show/master/docs/concepts/_toc.yaml),add a `section` group and its corresponding entries. Usually the entries are included from another _toc.yaml file: 例如，要在“系统”目录[`_toc.yaml`]（https://fuchsia.googlesource.com/fuchsia/+show/master/docs/concepts/_toc.yaml）中添加一个部分，请添加一个“节”组及其相应的条目。通常，这些条目是从另一个_toc.yaml文件包含的：

  ```yaml
  - title: "Zircon kernel"
    section:
    - include: /docs/concepts/kernel/_toc.yaml
  ```
 

Once you have made these changes, you can submit your changes for review.  进行这些更改后，您可以提交更改以供审核。

