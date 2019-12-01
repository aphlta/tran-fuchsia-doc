 
# Understanding SDK metadata  了解SDK元数据 

The manifest of the Core SDK is a JSON file that is described using a [JSON schema](https://json-schema.org/latest/json-schema-core.html).The goal of having a metadata based description of the SDK is to allowautomated processing of the SDK to integrate it into build environments. Core SDK的清单是使用[JSON模式]（https://json-schema.org/latest/json-schema-core.html）描述的JSON文件。 SDK允许对SDK进行自动处理，以将其集成到构建环境中。

It is expected that the contents and structure of the SDK will change over time so care should be taken when interpreting the metadata during any transformations.The source of truth for the structure of the metadata is always the files contains inthe `meta/schemas` directory of the SDK. 预计SDK的内容和结构会随着时间而变化，因此在任何转换过程中解释元数据时都应格外小心。元数据结构的真实来源始终是文件包含在meta / schemas目录中的SDK。

The source for the schema is found in [`build/sdk/meta`](/build/sdk/meta).  模式的源位于[`build / sdk / meta]]（/ build / sdk / meta）中。

 
## Manifest structure  清单结构 

The [manifest](/build/sdk/meta/manifest.json) has the following required properties:  [清单]（/ build / sdk / meta / manifest.json）具有以下必需属性：

Property         |   Description :----------------|:-------------:|  arch          | Architecture targeted for this SDK. There is a host architecture and a list of target device architectures. || id             | Build id of the SDK. || parts          | The array of elements in the SDK. Each part has a type which is defined in `meta/schemas/<type>.json` || schema_version | The version of the schema for the metadata. This value should be verifyed when using an automated integration process to make sure the metadata is being interpreted correctly. | 物业|说明：---------------- |：-------------：|拱针对此SDK的体系结构。有一个主机体系结构和一个目标设备体系结构列表。 || id | SDK的版本号。 ||零件| SDK中的元素数组。每个部分都有一个在`meta / schemas / <type> .json` ||中定义的类型。 schema_version |元数据的架构版本。使用自动集成过程时，应验证此值，以确保正确解释了元数据。 |

 

 
## Element types  元素类型 
* [banjo_library](/build/sdk/meta/banjo_library.json)  * [banjo_library]（/ build / sdk / meta / banjo_library.json）
* [cc_prebuilt_library](/build/sdk/meta/cc_prebuilt_library.json)  * [cc_prebuilt_library]（/ build / sdk / meta / cc_prebuilt_library.json）
* [cc_source_library](/build/sdk/meta/cc_source_library.json)  * [cc_source_library]（/ build / sdk / meta / cc_source_library.json）
* [dart_library](/build/sdk/meta/dart_library.json)  * [dart_library]（/ build / sdk / meta / dart_library.json）
* [device_profile](/build/sdk/meta/device_profile.json)  * [device_profile]（/ build / sdk / meta / device_profile.json）
* [documentation](/build/sdk/meta/documentation.json)  * [documentation]（/ build / sdk / meta / documentation.json）
* [fidl_library](/build/sdk/meta/fidl_library.json)  * [fidl_library]（/ build / sdk / meta / fidl_library.json）
* [host_tool](/build/sdk/meta/host_tool.json)  * [host_tool]（/ build / sdk / meta / host_tool.json）
* [loadable_module](/build/sdk/meta/loadable_module.json)  * [loadable_module]（/ build / sdk / meta / loadable_module.json）
