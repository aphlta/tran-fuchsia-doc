Naming C/C++ objects ==================== 命名C / C ++对象====================

 
## Include paths  包含路径 

The following guidelines apply to libraries which are meant to be used extensively, e.g. in an upper layer of the Fuchsia codebase or via an SDK,where "upper layer of the Fuchsia codebase" means "garnet" and above(peridot, topaz, vendor/foo). 以下准则适用于打算广泛使用的库，例如在紫红色代码库的上层或通过SDK，其中“紫红色代码库的上层”表示“石榴石”及以上（橄榄石，黄玉，供应商/富）。

There are three categories of headers: system, fuchsia, other.  标头分为三类：system，紫红色，其他。

 
#### For system headers  对于系统头 

```
<zircon/foo/bar.h>
```
 

 
###### Rationale  基本原理 

These headers describe kernel interfaces (syscalls, related structs and defines), shared definitions and data structures between kernel and userspace(and bootloader), that are often useful to higher layers as well. 这些标头描述了内核接口（系统调用，相关的结构和定义），内核与用户空间（和引导程序）之间的共享定义和数据结构，它们通常也对更高层有用。

 
###### Notes  笔记 

 
- Headers may be installed straight under `zircon/`.  -标头可以直接安装在“锆石/”下方。
- This does not include things like wrappers on syscall interfaces like zx.  -这不包括诸如zx之类的syscall接口上的包装器之类的东西。

 
###### Examples  例子 

 
- `zircon/process.h`  -`zircon / process.h`
- `zircon/syscalls/hypervisor.h`  -`zircon / syscalls / hypervisor.h`

 

 
#### For global headers  对于全局头 

```
<fuchsia/foo/bar.h>
```
 

 
###### Rationale  基本原理 

These are libraries that define a low level ABI/API in Fuchsia but are not specific to the kernel. 这些库在紫红色中定义了低级的ABI / API，但并不特定于内核。

 
###### Notes  笔记 

 
- FIDL-generated code for Fuchsia APIs in that very namespace, as well as C/C++ wrapper libraries around these APIs are installed here. -在该名称空间中为Fuchsia API生成FIDL生成的代码，以及围绕这些API的C / C ++包装器库。
- Headers may be installed straight under `fuchsia/`.  -标头可以直接安装在“紫红色/”下方。

 
###### Examples  例子 

 
- `fuchsia/fdio/fdio.h`  -`fuchsia / fdio / fdio.h`
- `fuchsia/pixelformat.h`  -`fuchsia / pixelformat.h`

 

 
#### For other headers  对于其他标题 

```
<lib/foo/bar.h>
```
 

 
###### Rationale  基本原理 

Some libraries in that space are not necessarily Fuchsia-specific, or they may be Fuchsia-specific but do not fall into either of the above categories.We use a rather bland namespace that will likely not cause any collisions inthe outside world: "lib". 该空间中的某些库不一定是特定于紫红色的，或者它们可能是特定于紫红色的，但不属于上述两种类别。 。

 
###### Notes  笔记 

 
- Headers may not be placed straight under `lib/`. Subdirectories (`lib/foo/`) are mandatory. -标头不能直接放在`lib /`下。子目录（lib / foo /`）是必需的。

 
###### Examples  例子 

 
- `lib/fit/function.h`  -`lib / fit / function.h`
- `lib/sys/cpp/component_context.h`  -`lib / sys / cpp / component_context.h`
