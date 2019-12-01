 
# Storage capabilities  储存能力 

[Storage capabilities][glossary-storage] are a way for components to define, [offer][offer], and [use][use] directories, but they have different semanticsthan [directory capabilities][directory-capabilities]. [存储功能] [词汇表存储]是组件定义，[提供] [提供]和[使用] [使用]目录的一种方法，但是它们的语义与[目录功能] [目录功能]不同。

Directories provided by storage capabilities are guaranteed to be unique and non-overlapping for each [component instance][component-instance], preventingany component instances from accessing files belonging to any other componentinstance (including their own children). 对于每个[component instance] [component-instance]，存储功能所提供的目录均保证是唯一且不重叠的，从而防止任何组件实例访问属于任何其他componentinstance（包括其自己的子实例）的文件。

 
## Directory vs storage capabilities  目录与存储功能 

As an example, if component instance `a` receives a _directory_ capability from its [realm][realm] and both [uses][use] it and [offers][offer] it to `b`, whichalso uses the directory, both component instances can see and interact with thesame directory. 例如，如果组件实例a从其[realm] [realm]接收到一个_directory_功能，并且[uses] [use]和[offers] [offer]都将其提供给`b`，后者也使用该目录，组件实例可以查看相同目录并与之交互。

```
<a's realm>
    |
    a
    |
    b

a.cml:
{
    "use": [ {"directory": "/example_dir" } ],
    "offer": [
        {
            "directory": "/example_dir",
            "from": "realm",
            "to": [ { "dest": "#b" } ],
        },
    ],
}

b.cml:
{
    "use": [ {"directory": "/example_dir" } ],
}
```
 

In this example if component instance `a` creates a file named `hippos` inside `/example_dir` then `b` will be able to see and read this file. 在这个例子中，如果组件实例“ a”在“ / example_dir”内部创建了一个名为“ hippos”的文件，那么“ b”将能够查看和读取该文件。

If the component instances use storage capabilities instead of directory capabilities, then component instance `b` cannot see and read the `hippos` file. 如果组件实例使用存储功能而不是目录功能，则组件实例“ b”将无法查看和读取“ hippos”文件。

```
<a's realm>
    |
    a
    |
    b

a.cml:
{
    "use": [ { "storage": "data", "as": "/example_dir" } ],
    "offer": [
        {
            "storage": "data",
            "from": "realm",
            "to": [ { "dest": "#b" } ],
        },
    ],
}

b.cml:
{
    "use": [ { "storage": "data", "as": "/example_dir" } ],
}
```
 

In this example any files that `a` creates are not be visible to `b`, as storage capabilities provide unique non-overlapping directories to eachcomponent instance. 在此示例中，`a`创建的任何文件都不对`b`可见，因为存储功能为每个组件实例提供了唯一的不重叠目录。

 
## Creating storage capabilities  创建存储功能 

Storage capabilities can be created with a [`storage` declaration][storage-syntax] in a [component manifest][manifests]. Once storagecapabilities have been declared, they can then be offered to other componentinstances by referencing the declaration by name. 可以使用[组件清单] [清单]中的[`storage`声明] [storage-syntax]创建存储功能。声明存储功能后，可以通过按名称引用声明将其提供给其他组件实例。

A `storage` declaration must include a reference to a directory capability, which is the directory from which the component manager will create isolateddirectories for each component instance using the storage capability. “存储”声明必须包含对目录功能的引用，该目录是组件管理器将使用该存储功能为每个组件实例创建隔离目录的目录。

For example, the following manifest describes new storage capabilities backed by the `/memfs` directory exposed by the child named `memfs`. From this storagedeclaration a data storage capability is offered to the child named`storage_user`. 例如，以下清单描述了由名为“ memfs”的子项公开的“ / memfs”目录支持的新存储功能。根据该存储声明，为名为“ storage_user”的子级提供了数据存储功能。

```

{
    "storage": [
        {
            "name": "mystorage",
            "from": "#memfs",
            "path": "/memfs",
        },
    ],
    "offer": [
        {
            "storage": "data",
            "from": "#mystorage",
            "to": [ { "dest": "#storage_user" } ],
        },
    ],
    "children": [
        { "name": "memfs", "url": "fuchsia-pkg://..." },
        { "name": "storage_user", "url": "fuchsia-pkg://...", },
    ],
}
```
 

 
## Storage capability semantics  存储功能语义 

A directory capability that backs storage capabilities can be used to access the files of any component that uses the resulting storage capabilities. This typeof directory capability should be routed carefully to avoid exposing thiscapability to too many component instances. 支持存储功能的目录功能可用于访问使用所得存储功能的任何组件的文件。应该仔细路由这种类型的目录功能，以避免将此功能暴露给太多的组件实例。

When a component instance attempts to access the directory provided to it through a storage capability, the framework binds to and generatessub-directories in the component instance that provides the backing directorycapability. Then, the framework provides the component instance access to aunique sub-directory. 当组件实例尝试通过存储功能访问提供给它的目录时，框架将绑定到组件实例并在该组件实例中生成提供后备目录功能的子目录。然后，该框架为组件实例提供对唯一子目录的访问。

The sub-directory to which a component instance is provided access is determined by the type of storage and its location in the component topology. This meansthat if a component instance is renamed in its parent manifest or moved to adifferent parent then it will receive a different sub-directory than it didbefore the change. 组件实例可访问的子目录由存储的类型及其在组件拓扑中的位置确定。这意味着，如果组件实例在其父清单中重命名或移动到另一个父实例，则它将收到与更改前不同的子目录。

