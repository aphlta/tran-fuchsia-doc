 
# zx_process_exit  zx_process_exit 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Exits the currently running process.  退出当前正在运行的进程。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

[[noreturn]] void zx_process_exit(int64_t retcode);
```
 

 
## DESCRIPTION  描述 

The `zx_process_exit()` call ends the calling process with the given return code. The return code of a process can be queried via the**ZX_INFO_PROCESS** request to [`zx_object_get_info()`]. zx_process_exit（）调用以给定的返回码结束调用过程。可以通过对[`zx_object_get_info（）]的** ZX_INFO_PROCESS **请求来查询进程的返回码。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_process_exit()` does not return.  zx_process_exit（）不返回。

 
## ERRORS  错误 

`zx_process_exit()` cannot fail.  zx_process_exit（）不能失败。

 
## SEE ALSO  也可以看看 

 
 - [`zx_object_get_info()`]  -[`zx_object_get_info（）`]
 - [`zx_process_create()`]  -[`zx_process_create（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

