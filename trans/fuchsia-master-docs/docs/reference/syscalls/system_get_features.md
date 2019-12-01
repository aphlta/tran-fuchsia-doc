 
# zx_system_get_features  zx_system_get_features 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Get supported hardware capabilities.  获得支持的硬件功能。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_system_get_features(uint32_t kind, uint32_t* features);
```
 

 
## DESCRIPTION  描述 

`zx_system_get_features()` populates *features* with a bit mask of hardware-specific features.  *kind* indicates the specific type of featuresto retrieve, e.g. **ZX_FEATURE_KIND_CPU**.  The supported kinds and the meaningof individual feature bits is hardware-dependent. zx_system_get_features（）使用硬件特定功能的位掩码填充功能。 *类型*表示要检索的特征的特定类型，例如** ZX_FEATURE_KIND_CPU **。支持的种类和各个功能位的含义取决于硬件。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_system_get_features()`  returns **ZX_OK** on success.  zx_system_get_features（）成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_NOT_SUPPORTED**  The requested feature kind is not available on this platform. ** ZX_ERR_NOT_SUPPORTED **所请求的功能种类在该平台上不可用。

 
## NOTES  笔记Refer to [Architecture Support](/docs/concepts/architecture/architecture_support.md) for supported processor architectures. 有关受支持的处理器体系结构，请参阅[体系结构支持]（/ docs / concepts / architecture / architecture_support.md）。

Refer to [zircon/features.h](/zircon/system/public/zircon/features.h) for kinds of features and individual feature bits. 有关功能的种类和单个功能位，请参考[zircon / features.h]（/ zircon / system / public / zircon / features.h）。

 
## SEE ALSO  也可以看看 

 
 - [`zx_system_get_num_cpus()`]  -[`zx_system_get_num_cpus（）`]
 - [`zx_system_get_physmem()`]  -[`zx_system_get_physmem（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

