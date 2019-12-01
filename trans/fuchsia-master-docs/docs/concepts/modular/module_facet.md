 
# Module Facet  模块面 

Modules declare their run-time capabilities (e.g. which Intent actions they handle) in the module facet of their [component manifest][component-manifest](i.e. their `.cmx` file). 模块在其[组件清单] [component-manifest]（即他们的.cmx文件）的模块方面中声明其运行时功能（例如，它们处理哪些Intent动作）。

 
## What is a facet?  什么是刻面？ 

Component facets are sections in the component manifest which aren't consumed directly by the component manager, but are left to be defined and consumed byother parts of Fuchsia. The Modular framework defines a `fuchsia.module` facetwhich module authors use to define module specific properties. 组件构面是组件清单中的部分，组件管理者不直接使用这些部分，而是由紫红色的其他部分定义和使用。模块化框架定义了一个“ fuchsia.module”方面，模块作者使用该方面来定义模块特定的属性。

This document describes how to declare a module facet in your component manifest. 本文档介绍了如何在组件清单中声明模块构面。

 
## Example  例 

The following is an excerpt of a component manifest that defines a module facet.  以下是定义模块构面的组件清单的摘录。

```
{
   "facets": {
      "fuchsia.module": {
         "@version": 2,
         "suggestion_headline": "See details about person",
         "intent_filters": [
            {
               "action": "com.google.fuchsia.preview.v1",
               "parameters": [
                  {
                     "name": "entityToPreview",
                     "type": "https://fuchsia.com/types/Friend"
                  }
               ]
            }
         ],
         "composition_pattern": "ticker"
      }
   }
}
```
 

This module can be launched using an Intent with the action `com.google.fuchsia.preview.v1` action, and a `entityToPreview` parameter oftype `https://fuchsia.com/types/Friend`. 可以使用具有动作“ com.google.fuchsia.preview.v1”动作和类型为“ https://fuchsia.com/types/Friend”的“ entityToPreview”参数的Intent来启动此模块。

 
## Module Facet fields  模块构面字段 

The module facet is defined under the `fuchsia.module` facet in a component manifest. See [example](#example). 模块构面在组件清单的“ fuchsia.module”构面下定义。参见[示例]（示例）。

 
*   `@version` **unsigned integer** *(required)*  *`@ version` **无符号整数** *（必填）*
    -   Describes the version of the module facet. The fields below indicate which minimum `@version` they require. -描述模块构面的版本。下面的字段指示他们需要的最低@@ version版本。
    -   **example**: `2`  -**示例**：`2`
*   `composition_pattern`: **string** *(optional)*  *`composition_pattern`：**字符串** *（可选）*
    -   **minimum `@version`**: 1  -**最低`@ version` **：1
    -   **possible values:**  -**可能的值：**
    *   `ticker`: Show the module at the bottom of the screen underneath another module. *`ticker`：在屏幕底部的另一个模块下方显示该模块。
    *   `comments-right`: show the module to the right of other modules.  *`comments-right`：在其他模块的右边显示该模块。
    -   **example**: `"ticker"`  -**示例**：`“ ticker”
    -   Specifies the compositional pattern that will be used by the story shell to display this module along-side other modules in the story. Forexample, the ticker pattern gives a signal to the story shell that themodule should be placed below another module that it may share a linkwith. -指定故事外壳将用于在故事中的其他模块旁边显示此模块的构图模式。例如，代码模式向故事外壳发出信号，表明该模块应放置在可能与之共享链接的另一个模块下方。
*   `suggestion_headline`: **string** *(optional)*  *`suggestion_headline`：**字符串** *（可选）*
    -   **minimum `@version`**: 2  -**最低`@ version` **：2
    -   **possible values**: UTF-8 string  -**可能的值**：UTF-8字符串
    -   **example**: `"See details about this person"`  -** example **：`“查看此人的详细信息”
    -   A human-readable string that may be used when suggesting this Module.  -在建议该模块时可以使用的人类可读字符串。
*   `placeholder_color`: **string** *(optional)*  *`placeholder_color`：**字符串** *（可选）*
    -   **minimum `@version`**: 2  -**最低`@ version` **：2
    -   **possible values**: hex color code, leading with a hashtag (`#`)  -**可能的值**：十六进制颜色代码，以井号（``）开头
    -   **example**: `"#ff00ff"`  -**示例**：`“ ff00ff”`
    -   Defines the color of the placeholder widget used while the module loads.  -定义模块加载时使用的占位小部件的颜色。
*   `intent_filters`: **IntentFilter[]** *(optional)*  *`intent_filters`：** IntentFilter [] ** *（可选）*
    -   **minimum `@version`**: 2  -**最低`@ version` **：2
    -   **possible values**: JSON list of [IntentFilter](#IntentFilter)  -**可能的值**：[IntentFilter]（IntentFilter）的JSON列表
    -   **example**: See [example](#example).  -**示例**：请参见[示例]（示例）。
    -   A list of different Intent types this Module is able to handle. An action dictates a semantic function this Module implements, as well asthe role of each of its parameters. When resolving an intent to amodule, the intent resolver uses an index of these intent filter liststo determine which modules can handle an intent. -此模块能够处理的不同Intent类型的列表。动作决定了该模块实现的语义功能及其每个参数的作用。在将意图解析为模块时，意图解析器使用这些意图过滤器列表的索引来确定哪些模块可以处理意图。

 
### IntentFilter  IntentFilter 

`IntentFilter` is a JSON object used to describe an intent type that a module is able to handle. The following describes the fields of the IntentFilter JSONobject: IntentFilter是一个JSON对象，用于描述模块能够处理的意图类型。以下描述了IntentFilter JSONobject的字段：

 
*   `action`: **string** *(required)*  *`action`：**字符串** *（必填）*
    -   **minimum `@version`**: 2  -**最低`@ version` **：2
    -   **possible values**: ASCII string  -**可能的值**：ASCII字符串
    -   The action this module is able to handle.  -该模块能够处理的动作。
*   `parameters`: **ParameterConstraint[]** *(required)*  *`parameters`：** ParameterConstraint [] ** *（必填）*
    -   **minimum `@version`**: 2  -**最低`@ version` **：2
    -   **possible values**: JSON List of [ParameterConstraint](#ParameterConstraint) -**可能的值**：[ParameterConstraint]（ParameterConstraint）的JSON列表
    -   Describes the names and types of the parameters required to execute the specified action. Parameters are typically passed in as Entities. -描述执行指定操作所需的参数的名称和类型。参数通常作为实体传递。

 
### ParameterConstraint  参数约束 

`ParameterConstraint` describes a particular intent parameter's name, and it's acceptable type. “ ParameterConstraint”描述了一个特定的意图参数的名称，它是可接受的类型。

 
*   `name`: **string** *(required)*  *`name`：**字符串** *（必填）*
    -   **minimum `@version`**: 2  -**最低`@ version` **：2
*   `type`: **string** *(required)*  *`type`：**字符串** *（必填）*
    -   **minimum `@version`**: 2  -**最低`@ version` **：2
    -   Type that is valid for this parameter.  -对此参数有效的类型。

See [example](#example).  参见[示例]（示例）。

