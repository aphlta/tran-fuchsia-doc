 
# Component manifest  组件清单 

A component manifest (.cmx) is a JSON file with the file extension `.cmx`. Component manifests are often located in a package’s `meta/` directory. Themanifest contains information that declares how to run the component and whatresources it receives. In particular, the component manifest describes howthe component is sandboxed. 组件清单（.cmx）是文件扩展名为.cmx的JSON文件。组件清单通常位于软件包的“ meta /”目录中。该清单包含一些信息，这些信息声明如何运行该组件以及它收到的资源。特别是，组件清单描述了如何对组件进行沙盒处理。

Here's a simple example of a cmx for an ELF binary component:  这是ELF二进制组件的cmx的简单示例：

```
{
    "program": {
        "binary": "bin/example_app",
        "args": [ "--example", "args" ]
    },
    "sandbox": {
        "system": [ "data/sysmgr" ],
        "services": [ "fuchsia.sys.Launcher", "fuchsia.netstack.Netstack" ]
    }
}
```
 

And one for a flutter/dart component:  还有一个用于颤振/飞镖组件：

```
{
    "program": {
        "data": "data/simple_flutter"
    },
    "runner": "flutter_jit_runner"
}
```
 

 
## program  程序 

The `program` property describes the resources to execute the component.  “ program”属性描述了执行组件的资源。

If [`runner`](#runner) is absent, the `program` property is a JSON object with the following schema: 如果不存在[`runner`]（runner），则“ program”属性是具有以下架构的JSON对象：

```
{
    "type": "object",
    "properties": {
        "binary": {
            "type": "string"
        },
        "args": {
            "type": "array",
            "items": {
              "type": "string"
            },
        },
    }
}
```
 

The `binary` property describes where in the package namespace to find the binary to run the component, and the optional `args` property contains thestring arguments to be provided to the process. Binary属性描述了在包名称空间中查找要运行组件的二进制文件的位置，而可选的args属性包含要提供给进程的字符串参数。

If [`runner`](#runner) is present, `program` is a freeform string-string JSON object interpreted as args to pass to the runner. 如果存在[`runner`]（runner），则“ program”是一个自由形式的字符串JSON对象，解释为args传递给跑步者。

For instance, for a flutter/dart component, its format is:  例如，对于颤振/飞镖组件，其格式为：

```
{
    "type": "object",
    "properties": {
        "data": {
            "type": "string"
        }
    }
}
```
 

Where `data` should describe the location of the flutter/dart binaries. By default, it is under `data/<component-name>`. 数据应该描述颤振/飞镖二进制文件的位置。默认情况下，它位于“ data / <component-name>”下。

 
## runner  跑步者 

`runner` is an optional property that names another component (or a package that contains one) to which execution is to be delegated. The target componentmust expose the [`Runner`][runner] service. runner是一个可选属性，用于命名要委托执行的另一个组件（或包含一个组件的包）。目标组件必须公开[`Runner`] [runner]服务。

If `runner` is present, [`program`](#program) is a freeform string-string JSON object interpreted as args to pass to the runner. 如果存在`runner`，则[`program`]（program）是一个自由格式的字符串JSON对象，解释为args传递给运行器。

If `runner` is absent, it is assumed that `program.binary` is an ELF binary or shell script. 如果不存在“ runner”，则假定“ program.binary”是ELF二进制或Shell脚本。

The `runner` property is a JSON string.  runner属性是一个JSON字符串。

 
## facets  方面 

`facets` is an optional property that contains free-form JSON about the component. Facets can be consumed by things on the system to acquire additionalmetadata about a component. facets是一个可选属性，其中包含有关组件的自由格式JSON。系统中的事物可以消耗方面，以获取有关组件的其他元数据。

The schema for `facets` is:  facets的架构为：

```
{
    "type": "object"
}
```
 

As an example of a facet, the `fuchsia.test` field is used to convey what additional services should be [injected into testingenvironments][test-components]. 作为一个方面的示例，“ fuchsia.test”字段用于传达应将哪些附加服务[注入到测试环境] [测试组件]。

 
## sandbox  沙盒 

The `sandbox` property controls the environment in which the component executes. Specifically, the property controls which directories the componentcan access during execution. sandbox属性控制组件执行的环境。具体来说，该属性控制在执行期间组件可以访问的目录。

The `sandbox` property is a JSON object with the following schema:  sandbox属性是具有以下架构的JSON对象：

```
{
    "type": "object",
    "properties": {
        "dev": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "services": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "system": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "pkgfs": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "features": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
}
```
 

The `dev` array contains a list of well-known device directories that are provided to the component. For example, if the string `class/input` appears inthe `dev` array, then `/dev/class/input` will appear in the namespaces of componentsloaded from the package. To allow access to a `misc` device, such as`/dev/misc/sysinfo`, add the string `misc` to the `dev` array. Unfortunately,allowing access to individual `misc` devices is not possible currently. dev数组包含提供给组件的知名设备目录的列表。例如，如果字符串“ class / input”出现在“ dev”数组中，则“ / dev / class / input”将出现在从包中加载的组件的名称空间中。为了允许访问`/ dev / misc / sysinfo`等`misc`设备，请将字符串`misc`添加到`dev`数组中。不幸的是，当前无法访问各个`misc`设备。

The `system` array contains a list of well-known paths within the system package that are provided to the component. For example, if the string `bin` appearsin the `system` array, then `/system/bin` will appear in the namespaces ofcomponents loaded from the package. system数组包含系统软件包中提供给组件的众所周知路径的列表。例如，如果字符串“ bin”出现在“ system”数组中，则“ / system / bin”将出现在从程序包加载的组件的名称空间中。

The `pkgfs` array contains a list of well-known paths within the pkgfs tree that are provided to the component. For example, if the string `versions`appears in the `pkgfs` array, then `/pkgfs/versions` will appear in thenamespaces of components loaded from the package, providing access to allpackages fully cached on the system. pkgfs数组包含pkgfs树中提供给组件的众所周知路径的列表。例如，如果字符串“ versions”出现在“ pkgfs”数组中，则“ / pkgfs / versions”将出现在从软件包加载的组件的命名空间中，从而提供对系统上完全缓存的所有软件包的访问。

The `services` array defines a list of services from `/svc` that the component may access. A typical component will require a number services from`/svc` in order to play some useful role in the system. For example, if`"services" = [ "fuchsia.sys.Launcher", "fuchsia.netstack.Netstack" ]`, thecomponent will have the ability to launch other components and access networkservices. A component may declare any list of services in its `services`,but it will only be able to access services present in its[environment](/docs/glossary.md#environment). This property should be defined byall new components, and soon a migration will take place to convert allcomponents to define `services`. “服务”数组定义了组件可以访问的“ / svc”服务列表。一个典型的组件将需要来自/ svc的许多服务，以便在系统中发挥某些有用的作用。例如，如果“ services” = [“ fuchsia.sys.Launcher”，“ fuchsia.netstack.Netstack”]`，则该组件将具有启动其他组件和访问网络服务的能力。组件可以在其“服务”中声明任何服务列表，但只能访问其环境中的服务（/docs/glossary.mdenvironment）。所有新组件都应定义该属性，不久将进行迁移以将所有组件转换为“服务”。

The `features` array contains a list of well-known features that the package wishes to use. Including a feature in this list is a request for the environmentin which the contents of the package execute to be given the resources requiredto use that feature. “功能”数组包含该软件包希望使用的一系列知名功能。在此列表中包括一个功能是对环境的请求，在该环境中将执行程序包的内容，并为其提供使用该功能所需的资源。

The set of currently known features are as follows:  当前已知的功能集如下：

 
- `config-data`, which will provide any configuration data available to the package this component is in that was provided in the [config-data](/docs/development/components/config_data.md)package on the system. -`config-data`，它将提供该组件所在的软件包可用的任何配置数据，该配置数据是系统上[config-data]（/ docs / development / components / config_data.md）软件包中提供的。

 
- `introspection`, which requests access to introspect the system. The introspection namespace will be located at `/info_experimental`. -`introspection`，请求访问以进行系统自检。自省名称空间将位于`/ info_experimental`。

 
- `isolated-persistent-storage`, which requests access to persistent storage for the device, located in `/data` in the package's namespace. This storage isisolated from the storage provided to other components. -`isolated-persistent-storage`，它请求访问设备的持久性存储，位于包名称空间的`/ data`中。该存储与提供给其他组件的存储隔离。

 
- `isolated-cache-storage`, which requests access to persistent storage for the device, located in `/cache` in the package's namespace. This storage isisolated from the storage provided to other components. Unlike`isolated-persistent-storage`, items placed in the storage provided by thisfeature will be deleted by the system to reclaim space when disk usage isnearing capacity. -`isolated-cache-storage`，它请求访问设备的持久性存储，位于包名称空间的`/ cache`中。该存储与提供给其他组件的存储隔离。与“孤立的持久存储”不同，此功能提供的存储中放置的项目将在磁盘使用减少容量时被系统删除，以回收空间。

 
- `isolated-temp`, which requests that a temp directory be installed into the component's namespace at `/tmp`. This is isolated from the system temp andthe temp directories of other component instances. -`isolated-temp`，它要求将临时目录安装到组件的名称空间中的/ tmp处。这与系统临时目录和其他组件实例的临时目录隔离。

 
- `root-ssl-certificates`, which requests access to the root SSL certificates for the device. These certificates are provided in the `/config/ssl` directoryin the package's namespace. -`root-ssl-certificates`，它请求访问设备的根SSL证书。这些证书在软件包名称空间的/ config / ssl目录中提供。

 
- `hub`, which requests access to the [Hub directory](/docs/concepts/framework/hub.md) scoped to the component instance's realm. -`hub`，请求访问范围为组件实例领域的[Hub目录]（/ docs / concepts / framework / hub.md）。

 
- `deprecated-shell`, which requests access to the resources appropriate for an interactive command line. Typically, shells are granted access to all theresources available in the current environment. The `deprecated-shell` featurealso implies the `root-ssl-certificates` and `hub` features.As the name suggests, this feature is to be removed. Current uses of thisfeature are explicitly allowlisted, and new uses are discouraged. -`preprecated-shell`，它请求访问适用于交互式命令行的资源。通常，shell被授予对当前环境中所有可用资源的访问权限。 deprecated-shell`功能还意味着'root-ssl-certificates`和`hub`功能。顾名思义，该功能将被删除。明确列出了此功能的当前用途，不鼓励使用新功能。

 
- `shell-commands`, which requests access to the currently available shell binaries (note: not "installed", but "available"). Binaries are mapped into`/bin` in the requesters namespace. Running these commands may require the`fuchsia.process.Resolver` and `fuchsia.process.Launcher` services alsobe requested. -`shell-commands`，它请求访问当前可用的shell二进制文件（注意：不是“已安装”，而是“可用”）。二进制文件映射到请求者名称空间中的“ / bin”中。运行这些命令可能需要fuchsia.process.Resolver和fuchsia.process.Launcher服务。

 
- `system-temp`, which requests access to the system temp directory, located at `/tmp` in the package's namespace. (Future work will likely remove access tothe system temp directory in favor of a local temp directory for eachprocess.) -`system-temp`，它请求访问系统临时目录，该目录位于软件包名称空间的`/ tmp`中。 （未来的工作可能会删除对系统临时目录的访问，而为每个进程提供本地临时目录。）

 
- `vulkan`, which requests access to the resources required to use the Vulkan graphics interface. This adds layer configuration data in the `/config/vulkan`directory in the package's namespace. -`vulkan`，请求访问使用Vulkan图形界面所需的资源。这会将层配置数据添加到包名称空间的`/ config / vulkan`目录中。

 
- `deprecated-ambient-replace-as-executable`, which provides legacy support for using the invalid handle with replace_as_executable. -`deprecated-ambient-replace-as-executable`，它为将无效句柄与replace_as_executable结合使用提供了传统支持。

See [sandboxing.md](/docs/concepts/framework/sandboxing.md) for more information about sandboxing.  有关沙箱的更多信息，请参见[sandboxing.md]（/ docs / concepts / framework / sandboxing.md）。

