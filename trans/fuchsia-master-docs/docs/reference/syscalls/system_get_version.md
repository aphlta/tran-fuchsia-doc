 
# zx_system_get_version  zx_system_get_version 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Get version string for system.  获取系统的版本字符串。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

zx_status_t zx_system_get_version(char* version, size_t version_size);
```
 

 
## DESCRIPTION  描述 

`zx_system_get_version()` fills in the given character array with a string identifying the version of the Zircon system currently running.The provided size must be large enough for the complete stringincluding its null terminator. zx_system_get_version（）在给定的字符数组中填充一个字符串，用于标识当前正在运行的Zircon系统的版本。提供的大小必须足够大，以完整的字符串（包括其空终止符）为单位。

The version string is guaranteed to never require more than 64 bytes of storage including the null terminator. 保证版本字符串绝不需要超过64个字节的存储空间（包括空终止符）。

The first four characters identify the version scheme. An example of the string returned is "git-8a07d52603404521038d8866b297f99de36f9162". 前四个字符标识版本方案。返回的字符串的示例是“ git-8a07d526034045210210dd6206b297f99de36f9162”。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_system_get_version()` returns **ZX_OK** on success.  `zx_system_get_version（）`成功返回** ZX_OK **。

 
## ERRORS  错误 

**ZX_ERR_BUFFER_TOO_SMALL**  *version_size* is too short.  ** ZX_ERR_BUFFER_TOO_SMALL ** * version_size *太短。

 
## NOTES  笔记 

 
## SEE ALSO  也可以看看 

 

