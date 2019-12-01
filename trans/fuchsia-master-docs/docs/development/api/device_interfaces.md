 
# Fuchsia Device Interface Rubric  紫红色设备接口专栏 

The Fuchsia device interfaces are expressed as FIDL protocols.  These FIDL definitions should conform to the [FIDL Style Rubric][fidl-style] and[FIDL API Rubric][fidl-api]. 紫红色的设备接口表示为FIDL协议。这些FIDL定义应符合[FIDL Style Rubric] [fidl-style]和[FIDL API Rubric] [fidl-api]。

 
## Identifiers  身份标识 

Prefer descriptive identifiers.  If you are using domain-specific abbreviations, document the expansion or provide a reference for further information. 首选描述性标识符。如果您使用的是特定于域的缩写，请记录该扩展或提供参考以获取更多信息。

Every identifier that is defined as part of a protocol must be documented with a comment explaining its interpretation (in the case of fields, types, andparameters) or behavior (in the case of methods). 定义为协议一部分的每个标识符都必须带有注释，说明其解释（在字段，类型和参数的情况下）或行为（在方法的情况下）。

 
## Protocols  通讯协定 

All device interface protocols must use the `[Layout = "Simple"]` attribute.  This restriction exists to allow ease of implementing protocols in any of oursupported languages for driver development. 所有设备接口协议都必须使用[[Layout =“ Simple”]]属性。存在此限制的目的是简化使用我们支持的任何语言进行驱动程序开发的协议的实现。

 
## Method Statuses  方法状态 

Use a `zx.status` return to represent success and failure.  If a method should not be able to fail, do not provide a `zx.status` return.  If the method returns multiplevalues, the `zx.status` should come first. 使用`zx.status`返回代表成功和失败。如果某个方法不能失败，则不要提供zx.status返回。如果该方法返回多个值，则应首先使用zx.status。

 
## Arrays, Strings, and Vectors  数组，字符串和向量 

All arrays, strings, and vectors must be of bounded length.  For arbitrarily selected bounds, prefer to use a `const` identifier as the length so thatprotocol consumers can programmatically inspect the length. 所有数组，字符串和向量都必须是有界的。对于任意选择的边界，最好使用“ const”标识符作为长度，以便协议使用者可以以编程方式检查长度。

 
## Enums  枚举 

Prefer enums with explicit sizes (e.g. `enum Foo : uint32 { ... }`) to plain integer types when a field has a constrained set of non-arithmetic values. 当字段具有非算术值的约束集时，应优先选择具有显式大小的枚举（例如`enum Foo：uint32 {...}`）。

 
## Bitfields  位域 

If your protocol has a bitfield, represent its values using `bits` values. For details, see the ["bits"][bits] topic in the readability rubric. 如果您的协议具有位字段，请使用“位”值表示其值。有关详细信息，请参见可读性规则中的[“ bits”] [bits]主题。

 
## Non-channel based protocols  基于非通道的协议 

Some interface protocols may negotiate a non-channel protocol as a performance optimization (e.g. the zircon.ethernet.Device's GetFifos/SetIOBuffer methods).FIDL does not currently support expressing these protocols.  For now, representany shared data structures with `struct` definitions and provide detaileddocumentation about participation in the protocol.  Packed structures are notcurrently supported. 一些接口协议可能会协商非通道协议以优化性能（例如zircon.ethernet.Device的GetFifos / SetIOBuffer方法）.FIDL当前不支持表达这些协议。目前，用“ struct”定义表示任何共享的数据结构，并提供有关参与协议的详细文档。当前不支持打包结构。

