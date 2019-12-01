 
# Host Side FIDL  主机端FIDL 

This document is a short summary of what's available now for host side FIDL, and what may be available in the future. 本文档简要概述了主机端FIDL现在可用的功能以及将来可能使用的功能。

 
## What is Available?  有什么可用的？ 

Encoding and decoding of structs and tables that contain no zircon handles in C++ only.  仅在C ++中对不包含锆石句柄的结构和表进行编码和解码。

 
* Use of handles (or consequently FIDL protocol requests and the like) will cause the host side libraries to fail. *使用句柄（或因此的FIDL协议请求等）将导致主机端库失败。
* In the future this will be verified through a mechanism like NoHandles.  *将来将通过NoHandles之类的机制进行验证。

 
## What is not Available?  什么不可用？ 

Any use of protocols.  协议的任何使用。

 
* Trying to use a FIDL file that mentions a protocol will cause the host side runtime to fail to compile. *尝试使用提及协议的FIDL文件将导致主机端运行时无法编译。
* In the future some verification mechanism will be available here too.  *将来，这里也会提供一些验证机制。

 
## What is out of scope?  什么超出范围？ 

Emulation of arbitrary zircon handles (particularly VMO’s).  模拟任意锆石手柄（尤其是VMO手柄）。

 
## What is possibly in scope?  范围可能是什么？ 

Protocols communicating over a socket transport (implies not exchanging handles).  通过套接字传输进行通信的协议（意味着不交换句柄）。

 
## What is undecided?  尚未决定的是什么？ 

