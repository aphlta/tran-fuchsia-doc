 
# Fuchsia's libc  紫红色的libc 

Fuchsia's libc started as a fork of musl libc. It has since diverged significantly, but the approximate source code layout remains the same. Thesource can be found in[`zircon/third_party/ulib/musl`](/zircon/third_party/ulib/musl). 紫红色的libc最初是Musl libc的分支。此后已经大相径庭，但是近似的源代码布局保持不变。可以在[`zircon / third_party / ulib / musl]（/ zircon / third_party / ulib / musl）中找到源。

TODO(ZX-1598) Type more here.  TODO（ZX-1598）在此处输入更多。

 
## Standards  标准品 

 
### C11  C11 

Fuchsia's libc supports most of the [C11][c11std] standard. This in particular includes the atomic and threading portions of thestandard library. 紫红色的libc支持大多数[C11] [c11std]标准。这尤其包括标准库的原子和线程部分。

 
### POSIX  POSIX 

Fuchsia implements a subset of POSIX.  紫红色实现POSIX的子集。

Things at least partially supported include the basics of POSIX I/O (open/close/read/write/stat/...), and pthreads (threads and mutexes). 至少部分受支持的事物包括POSIX I / O（打开/关闭/读取/写入/状态/ ...）和pthread（线程和互斥体）的基础。

On Fuchsia, the portion of file paths beginning with a sequence of `..` is resolved locally. See [this writeup][dotdot] for moreinformation. 在Fuchsia上，文件路径中以“ ..”序列开头的部分在本地解析。有关更多信息，请参见[此文章] [点]。

Similarly, symlinks are not supported on Fuchsia.  同样，紫红色不支持符号链接。

Conspicuously not supported are UNIX signals, fork, and exec.  明显不支持UNIX信号，fork和exec。

 
## FDIO  FDIO 

Fuchsia's libc does not directly support I/O operations. Instead it provides weak symbols that another library can override. This istypically done by [fdio.so][fdio]. 紫红色的libc不直接支持I / O操作。相反，它提供了其他库可以覆盖的弱符号。通常由[fdio.so] [fdio]完成。

 
## Linking  连结中 

Statically linking libc is not supported. Everything dynamically links libc.so.  不支持静态链接libc。一切都动态链接libc.so。

 
## Dynamic linking and loading  动态链接和加载 

libc.so is also the dynamic linker.  libc.so也是动态链接器。

