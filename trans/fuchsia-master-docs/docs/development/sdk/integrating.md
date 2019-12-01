 
# Integrating the Core SDK  集成核心SDK 

Integrating the Core SDK is the process of consuming the Core SDK and turning it into something usable. 集成Core SDK是使用Core SDK并将其转变为可用的过程。

The main entry point for the ingestion process is a file at `//meta/manifest.json`.As with every metadata file in the SDK, the manifest follows a JSON schema whichis included under `//meta/schemas/manifest.json`. 提取过程的主要入口是`// meta / manifest.json`中的文件。与SDK中的每个元数据文件一样，清单遵循JSON模式，该模式包含在`//meta/schemas/manifest.json中`。

This file contains a list of all the elements included in this SDK, represented by the path to their respective metadata file.Each element file is guaranteed to contain a top-level `type` attribute, whichmay be used to apply different treatments to different element types. For example,generating a build file for a FIDL library or just moving a host tool to aconvenient location in the final development environment. 该文件包含此SDK中包含的所有元素的列表，以其各自元数据文件的路径表示。每个元素文件均保证包含顶级的“ type”属性，该属性可用于对不同元素进行不同的处理类型。例如，为FIDL库生成构建文件，或仅将主机工具移至最终开发环境中的方便位置。

The existence of the various metadata files as well as the exhaustiveness of their contents should make it so that the ingestion process may be fullyautomated.JSON schemas may even be used to generate code representing the metadatacontainers and let the ingestion program handle idiomatic data structuresinstead of raw JSON representations. 各种元数据文件的存在及其内容的穷尽性应使其完全自动化，甚至可以使用JSON模式生成代表元数据容器的代码，并让摄取程序处理原始数据结构而不是原始数据结构JSON表示形式。

The metadata schemas will evolve over time. In order to allow consumers of that metadata to adjust to schema changes, themain metadata file contains a property named `schema_version` which is an opaqueversion identifier for these schemas.This version identifier will be modified every time the metadata schemas evolvein a way that requires the attention of a developer.SDK consumers may record the version identifier of the metadata they used to lastingest an SDK and compare that version identifier to next SDK's versionidentifier in order to detect when developer action may be required. 元数据模式将随着时间而发展。为了使该元数据的使用者能够适应模式更改，主元数据文件包含一个名为“ schema_version”的属性，该属性是这些模式的opaqueversion标识符。每次元数据模式演变时，都会修改该版本标识符，要求SDK使用者可以记录他们用于持久化SDK的元数据的版本标识符，并将该版本标识符与下一个SDK的versionidentifier进行比较，以检测何时可能需要开发人员采取措施。

 

