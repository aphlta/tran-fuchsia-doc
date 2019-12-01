iquery(3) ===== iquery（3）=====

 
# NAME  名称 

`iquery` - the Fuchsia Inspect API Query Toolkit  iquery-紫红色Inspect API查询工具包

 
# SYNOPSIS  概要 

```
iquery [MODE] [--recursive] [--format=<FORMAT>]
       [--sort]
       [(--full_paths|--absolute_paths)]
       PATH [...PATH]
```
 

 
# DESCRIPTION  描述 

`iquery` is a utility program for inspecting component nodes exposed over the [Inspect API](gsw-inspect.md).It accepts a list of paths to process, and howthey are processed depends on the `MODE` setting and options. iquery是用于检查暴露在[Inspect API]（gsw-inspect.md）上的组件节点的实用程序。它接受要处理的路径列表，其处理方式取决于“ MODE”设置和选项。

 
# MODES  模式 

`MODE=(--cat|--ls|--find|--report)`  MODE =（-cat | --ls | --find | --report）`

 
## `--cat`  `--cat`> DEFAULT. Treat each `PATH` as a node directory to open, and print > the properties and metrics for those nodes. >默认。将每个“ PATH”都视为要打开的节点目录，然后打印>这些节点的属性和度量。

 
## `--ls`  `--ls`> Treat each `PATH` as a node directory, and list the children for those nodes.  >将每个`PATH`视为节点目录，并列出这些节点的子级。

 
## `--find`  `-找到`> Recursively find all node directories under the filesystem paths > passed in, and output the relative path one per line. >递归地找到传入的文件系统路径下的所有节点目录，并每行输出一个相对路径。

 
## `--report`  `--report`> Outputs a default system-wide report. Ignores all options other than > --format. >输出默认的系统范围报告。忽略除--format之外的所有选项。

 
# OPTIONS  选件 

 
## `--recursive`  `-递归`> Continue to step down the hierarchy of elements. Mode dependent.  >继续逐步降低元素的层次结构。与模式有关。

```
cat: If false, will print the top level node only. True will output the complete node hierarchy.
Example:
$ find .
a/
a/fuchsia.inspect.Inspect
b/c

$ iquery --ls a
a_key
a_key2

$ iquery --cat a_key
a_key:
  a_value

$ iquery --cat --recursive a
a:
  a_key = a_value
  a_key2 = 3.4

find: If false, it will descend into each branch until it finds a valid node.
      True will output the complete tree, including nested nodes.

Example:
$ find .
a/
a/fuchsia.inspect.Inspect
b/c
b/c/fuchsia.inspect.Inspect

$ iquery --find .
a/
b/c

$ iquery --find --recursive .
a
a#a_key
a#a_key2
b/c
b/c#c_val
b/c#c_val2

```
 

 
## `--format=<FORMAT>`  --format = <FORMAT>> What format the output should be in.  >输出应采用哪种格式。

```
Current supported formatters:
- text: Meant for human inspection. This is the default option.
- json: Meant for machine consumption.
```
 

 
## `--sort`  `--sort`> When specified, sort the values for each Node before printing.  >指定后，在打印之前对每个节点的值进行排序。

```
$ iquery root.inspect
root:
  c:
  a:
  b:

$ iquery --sort root.inspect
root:
  a:
  b:
  c:

$ iquery numeric.inspect
root:
  11:
  2:
  1:

# When all children are numeric, iquery sorts numerically.
$ iquery --sort numeric.inspect
root:
  1:
  2:
  11:
```
 

 
## `--full_paths`  `--full_paths`> Rename each node to have its own relative path.  >重命名每个节点以具有其自己的相对路径。

```
$ iquery a a/b
a:
b:
$ iquery --full_paths a a/b
a:
a/b:
```
 

 
## `--absolute_paths`  `--absolute_paths`> Rename each node to have its own absolute path from the root.  >重命名每个节点，使其具有从根到其自身的绝对路径。

```
$ cd /hub/c/
$ iquery a a/b
a:
b:
$ iquery --absolute_paths a a/b
/hub/c/a:
/hub/c/a/b:
```
