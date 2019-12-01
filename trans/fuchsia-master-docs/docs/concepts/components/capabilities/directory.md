 
# Directory capabilities  目录功能 

[Directory capabilities][glossary-directory] allow components to connect to directories provided by other components. [目录功能] [词汇表目录]允许组件连接到其他组件提供的目录。

 
## Creating directory capabilities  创建目录功能 

When a component wants to make one of its directories available to other components, it specifies the path of that directory in its [outgoingdirectory][glossary-outgoing] in one of the following ways: 当某个组件希望将其目录之一提供给其他组件使用时，它会通过以下其中一种方式在[outgoingdirectory] ​​[glossary-outgoing]中指定该目录的路径：

 
- [Exposing][expose] the directory to the containing realm.  -将目录[暴露] [暴露]到包含的领域。

  ```
  {
      "expose": [{
          "directory": "/data",
          "from": "self",
      }],
  }
  ```
 

 

 
- Or [offering][offer] the directory to some of the component's children.  -或[提供] [提供]目录给组件的某些子项。

  ```
  {
      "offer": [{
          "directory": "/data",
          "from": "self",
          "to": [{
              { "dest": "#child-a" },
              { "dest": "#child-b" },
          }],
      }],
  }
  ```
 

 
## Consuming directory capabilities  消耗目录功能 

When a component wants to make use of a directory from its containing realm, it does so by [using][use] the directory. This will make the directory accessiblefrom the component's [namespace][glossary-namespace]. 当组件要使用其包含领域中的目录时，可以通过[使用] [使用]目录来使用。这将使该目录可从组件的[namespace] [glossary-namespace]访问。

This example shows a directory named `/data` that is included in the component's namespace. If the component instance accesses this directory during itsexecution, the component framework performs [capabilityrouting][capability-routing] to find the component that provides it. Then, theframework connects the directory from the component's namespace to thisprovider. 本示例显示了一个名为`/ data`的目录，该目录包含在组件的名称空间中。如果组件实例在执行期间访问此目录，则组件框架将执行[capabilityrouting] [capability-routing]以查找提供该目录的组件。然后，框架将目录从组件的名称空间连接到此提供程序。

```
{
    "use": [{
        "directory": "/data",
    }],
}
```
 

See [`//examples/components/routing`][routing-example] for a working example of routing a directory capability from one component to another. 有关将目录功能从一个组件路由到另一个组件的工作示例，请参见[`// examples / components / routing`] [routing-example]。

 
### Framework directory capabilities  框架目录功能 

Some directory capabilities are available to all components through the framework. When a component wants to use one of these directories, it does so by[using][use] the directory with a source of `framework`. 通过该框架，所有组件都可以使用某些目录功能。当组件想要使用这些目录之一时，它通过[使用] [使用]带有框架源的目录来使用。

```
{
    "use": [{
        "directory": "/hub",
        "from": "framework",
    }],
}
```
 

 
## Directory paths  目录路径 

The paths used to refer to directories can be renamed when being [offered][offer], [exposed][expose], or [used][use]. 当[提供] [提供]，[公开] [公开]或[使用] [使用]时，可以重命名用于引用目录的路径。

In the following example, there are three components, `A`, `B`, and `C`, with the following layout: 在下面的示例中，具有三个组件，`A`，`B`和`C`，其布局如下：

```
 A  <- offers directory "/data" from "self" to B as "/intermediary"
 |
 B  <- offers directory "/intermediary" from "realm" to B as "/intermediary2"
 |
 C  <- uses directory "/intermediary2" as "/config"
```
 

Each component in this example changes the path used to reference the directory when passing it along in this chain. When component `C` accesses the `/config`directory in its namespace, it will be connected to directory `/data` incomponent `A`'s outgoing directory. 在此示例中，每个组件在传递此链时都会更改用于引用目录的路径。当组件“ C”访问其命名空间中的“ / config”目录时，它将连接到组件“ A”的输出目录中的目录“ / data”。

```
A.cml:
{
    "offer": [{
        "directory": "/data",
        "from": "self",
        "to": [{
            { "dest": "#B", "as": "/intermediary" },
        }],
    }],
    "children": [{
        "name": "B",
        "url": "fuchsia-pkg://fuchsia.com/B#meta/B.cm",
    }],
}
```
 

```
B.cml:
{
    "offer": [{
        "directory": "/intermediary",
        "from": "self",
        "to": [{
            { "dest": "#C", "as": "/intermediary2" },
        }],
    }],
    "children": [{
        "name": "C",
        "url": "fuchsia-pkg://fuchsia.com/C#meta/C.cm",
    }],
}
```
 

```
C.cml:
{
    "use": [{
        "directory": "/intermediary2",
        "as": "/config",
    }],
}
```
 

If any of the names didn't match in this chain, any attempts by `C` to list or open items in this directory would fail. 如果此链中的任何名称都不匹配，则C试图在该目录中列出或打开项目的任何尝试都将失败。

