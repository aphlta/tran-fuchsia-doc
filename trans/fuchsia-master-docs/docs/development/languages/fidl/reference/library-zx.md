 

 
# Internal library zx  内部库zx 

The `fidlc` compiler automatically generates `library zx` (internally) into [//zircon/tools/fidl/lib/library_zx.cc](/zircon/tools/fidl/lib/library_zx.cc). `fidlc`编译器自动（内部）生成`library zx`到[//zircon/tools/fidl/lib/library_zx.cc](/zircon/tools/fidl/lib/library_zx.cc）。

You will find content similar to the following:  您会发现类似于以下内容：

```fidl
[Internal]
library zx;
using status = int32;
using time = int64;
using duration = int64;
using koid = uint64;
using vaddr = uint64;
using paddr = uint64;
using paddr32 = uint32;
using gpaddr = uint64;
using off = uint64;
using procarg = uint32;
const uint64 CHANNEL_MAX_MSG_BYTES = 65536;
const uint64 CHANNEL_MAX_MSG_HANDLES = 64;
const uint64 MAX_NAME_LEN = 32;
const uint64 MAX_CPUS = 512;
```
 

You can reference this library with the `using` statement:  您可以使用`using`语句引用该库：

```fidl
using zx;
```
 

The types generally correspond to [Zircon System Types](/docs/development/api/system.md#types). For example,`zx.duration` corresponds to `zx_duration_t`. 这些类型通常对应于[Zircon系统类型]（/ docs / development / api / system.mdtypes）。例如，`zx.duration`对应于`zx_duration_t`。

