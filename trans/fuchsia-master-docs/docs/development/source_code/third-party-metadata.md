 
# README.fuchsia File Syntax  README.fuchsia文件语法 

`README.fuchsia` files are used to annotate third-party source libraries with some useful metadata, such as code origin, version and license. “ README.fuchsia”文件用于通过一些有用的元数据（例如代码来源，版本和许可证）来注释第三方源库。

The format of these files consists of one or more directive lines, followed by unstructured description and notes. 这些文件的格式由一个或多个指令行组成，后跟非结构化的描述和注释。

Directives consist of a directive keyword at the beginning of the line, immediately followed by a colon and a value that extends to the end ofthe line. The value may have surrounding whitespace, and blank lines mayappear before or between directives. 指令由在行首的指令关键字，紧随其后的冒号和延伸到行尾的值组成。该值可能包含空格，并且在指令之前或之间可能会出现空白行。

Several directives are described below, but other directives may appear in `README.fuchsia` files and software that consumes them should nottreat the appearance of an unknown directive as an error. Similarly,such software should match directive keywords case-insensitively. 下面描述了几个指令，但其他指令可能会出现在README.fuchsia文件中，使用它们的软件不应将未知指令的出现视为错误。同样，此类软件应区分大小写地匹配指令关键字。

Description lines are optional and follow a `Description` directive that must appear on a line by itself prior to any unstructureddescription text. 广告描述行是可选的，并遵循“描述”指令，该指令必须在任何非结构化描述文本之前单独出现在一行中。

 
## Syntax  句法 

```
file                  := directive-line* description?
directive-line        := directive | blank-line
directive             := keyword ":" SPACE* value SPACE* EOL
value                 := NONBLANK ANYCHAR*
description           := description-directive description-line*
description-directive := "Description:" SPACE* EOL
description-line      := ANYCHAR* EOL
keyword               := [A-Za-z0-9][A-Za-z0-9 ]*
blank-line            := SPACE* EOL
SPACE                 := any whitespace character
EOL                   := end of line character
NONBLANK              := any non-whitespace, non-EOL character
ANYCHAR               := any character but EOL
```
 

 
## Common directive keywords  通用指令关键字 

Common directive keywords include:  常见的指令关键字包括：

 
* `Name`  *名称

  Descriptive name of the component. This should be included if the name is not obvious from context. 组件的描述性名称。如果名称在上下文中不明显，则应包括在内。

  ```
  Name: OpenSSH
  ```
 

 
* `URL`  *`URL`

  The URL where the component lives. If the component is based on a specific release, then list that explicitly. 组件所在的URL。如果组件基于特定发行版，则显式列出。

  ```
  URL: https://ftp.openbsd.org/pub/OpenBSD/OpenSSH/openssh-7.6.tar.gz
  ```
 

  Otherwise, list the vendor's website.  否则，请列出供应商的网站。

  ```
  URL: https://www.openssh.com/
  ```
 

  This directive may be repeated to include multiple URLs if necessary.  如有必要，可以重复此指令以包含多个URL。

 
* `Version`  *`版本`

  Lists a version number or commit identifier for the software. If the version is apparent from the *URL* or commit history, then this may beomitted. 列出软件的版本号或提交标识符。如果从* URL *或提交历史记录中可以明显看到该版本，则可以忽略。

  ```
  Version: 7.6
  ```
 

 
* `License`  *`许可证`

  The license under which the component is distributed. Only standard forms are accepted, e.g. MIT/X11, BSD, Apache 2.0. 分发组件所依据的许可证。仅接受标准格式，例如MIT / X11，BSD，Apache 2.0。

  ```
  License: BSD
  ```
 

 
* `License File`  *许可证文件

  File that contains a copy of the component's license. This must name an existing file in the repository, relative to the `README.fuchsia`file. 包含组件许可证副本的文件。这必须命名存储库中相对于README.fuchsia文件的现有文件。

  ```
  License File: LICENCE
  ```
 

  This directive may be repeated to include multiple files if necessary.  如有必要，可以重复此指令以包含多个文件。

 
* `Upstream Git`  *`上游Git`

  Links to the upstream Git repository from which this component has been branched. This should be included for any software branched froman external Git repository. 链接到已从中分支此组件的上游Git存储库。从外部Git存储库分支的任何软件都应包含此文件。

  ```
  Upstream Git: https://github.com/openssh/openssh-portable
  ```
 

 
* `Description`  *`描述`

  Marks the end of directives and the beginning of unstructured description, it must appear on a line by itself. 标记指令的末尾和非结构化描述的开始，它必须单独出现在一行上。

  ```
  Description:

  A short description of what the package is and is used for.
  ```
 

 
* `Local Modifications`  *`本地修改`

  Enumerate any changes that have been made locally to the package from the shipping version listed above. 列举从上面列出的发货版本对包装进行本地更改的所有信息。

  ```
  Local Modifications:

  Added README.fuchsia.
  Ported build rules from CMake to GN.
  ```
