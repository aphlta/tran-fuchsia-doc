 
# zx_thread_exit  zx_thread_exit 

 
## NAME  名称 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

Terminate the current running thread.  终止当前正在运行的线程。

 
## SYNOPSIS  概要 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

```c
#include <zircon/syscalls.h>

[[noreturn]] void zx_thread_exit(void);
```
 

 
## DESCRIPTION  描述 

`zx_thread_exit()` causes the currently running thread to cease running and exit. zx_thread_exit（）导致当前正在运行的线程停止运行并退出。

The signal **ZX_THREAD_TERMINATED** will be asserted on the thread object upon exit and may be observed via [`zx_object_wait_one()`]or [`zx_object_wait_many()`] on a handle to the thread. 信号** ZX_THREAD_TERMINATED **将在退出时在线程对象上声明，并且可以通过线程句柄上的[`zx_object_wait_one（）]或[`zx_object_wait_many（）`]观察到。

 
## RIGHTS  权利 

<!-- Updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新，请勿编辑。 ->

TODO(ZX-2399)  待办事项（ZX-2399）

 
## RETURN VALUE  返回值 

`zx_thread_exit()` does not return.  zx_thread_exit（）不返回。

 
## SEE ALSO  也可以看看 

 
 - [`zx_handle_close()`]  -[`zx_handle_close（）`]
 - [`zx_handle_duplicate()`]  -[`zx_handle_duplicate（）`]
 - [`zx_object_wait_async()`]  -[`zx_object_wait_async（）`]
 - [`zx_object_wait_many()`]  -[`zx_object_wait_many（）`]
 - [`zx_object_wait_one()`]  -[`zx_object_wait_one（）`]
 - [`zx_thread_create()`]  -[`zx_thread_create（）`]
 - [`zx_thread_start()`]  -[`zx_thread_start（）`]

<!-- References updated by update-docs-from-fidl, do not edit. -->  <！-由update-docs-from-fidl更新的引用，请勿编辑。 ->

