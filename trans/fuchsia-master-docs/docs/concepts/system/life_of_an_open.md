 
# Life of an 'Open'  “公开赛”的生活 

To provide an end-to-end picture of filesystem access on Fuchsia, this document dives into the details of each layer which is used when doing something assimple as opening a file. It’s important to note: all of these layers exist inuserspace; even when interacting with filesystem servers and drivers, the kernelis merely used to pass messages from one component to another. 为了提供Fuchsia上文件系统访问的端到端图片，本文档将深入探讨每层的细节，这些细节在执行打开文件之类的简单操作时会使用。需要注意的是：所有这些层都存在于用户空间中；即使与文件系统服务器和驱动程序进行交互，内核也仅用于将消息从一个组件传递到另一个组件。

A call is made to:  致电至：

`open(“foobar”);`  `open（“ foobar”）;`

Where does that request go?  那个请求去哪儿了？

 
## Standard Library: Where 'open' is defined  标准库：定义“开放”的位置 

The ‘open’ call is a function, provided by a [standard library](libc.md). For C/C++ programs, this will normally be declared in `unistd.h`, which has abacking definition in [libfdio](/zircon/system/ulib/fdio/).For Go programs, there is an equivalent (but distinct) implementation in the Gostandard library. For each language and runtime, developers may opt into theirown definition of “open”. “ open”调用是由[标准库]（libc.md）提供的函数。对于C / C ++程序，通常会在`unistd.h`中声明，在[libfdio]（/ zircon / system / ulib / fdio /）中有一个辅助定义。对于Go程序，有一个等效项（但与众不同） Gostandard库中的实现。对于每种语言和运行时，开发人员可以选择自己的“开放”定义。

On a monolithic kernel, `open` would be a lightweight shim around a system call, where the kernel might handle path parsing, redirection, etc. In thatmodel, the kernel would need to mediate access to resources based on exteriorknowledge about the caller. The Zircon kernel, however, intentionally has nosuch system call. Instead, clients access filesystems through **channels** --when a process is initialized, it is provided a [namespace](/docs/concepts/framework/namespaces.md),which is a table of "absolute path" -> "handle" mappings. All paths accessedfrom within a process are opened by directing requests through this namespacemapping. 在单片内核上，“ open”将是围绕系统调用的轻量级填充程序，其中内核可能会处理路径解析，重定向等。在该模型中，内核将需要基于有关调用者的外部知识来调解对资源的访问。但是，Zircon内核故意没有这种系统调用。相反，客户端通过**通道**访问文件系统-初始化进程时，会为它提供一个[namespace]（/ docs / concepts / framework / namespaces.md），该表是“绝对路径”表-> “句柄”映射。通过在此名称空间映射中定向请求，可以打开从进程内访问的所有路径。

In this example, however, involving a request to open “foobar”, a relative path was used, so the incoming call could be sent over the path representing thecurrent working directory (which itself is represented as an absolute pathand a handle). 但是，在此示例中，涉及到打开“ foobar”的请求，因此使用了相对路径，因此可以通过代表当前工作目录的路径（其本身表示为绝对路径和句柄）发送传入呼叫。

The standard library is responsible for taking a handle (or multiple handles) and making them appear like file descriptors. As a consequence, the “filedescriptor table” is a notion that exists within a client process (if a clientchooses to use a custom runtime, they can view their resources purely ashandles -- the “file descriptor” wrapping is optional). 标准库负责获取一个（或多个）句柄并使它们看起来像文件描述符。因此，“ filedescriptor表”是客户端进程中存在的一个概念（如果客户端选择使用自定义运行时，则他们可以单纯地查看其资源，“ file描述符”包装是可选的）。

This raises a question, however: given a file descriptor to files, sockets, pipes, etc, what does the standard library do to make all these resourcesappear functionally the same? How does that client know what messages to sendover these handles? 但是，这引发了一个问题：给文件，套接字，管道等文件描述符后，标准库如何使所有这些资源在功能上相同？该客户端如何知道要通过这些句柄发送哪些消息？

 
## Fdio  菲迪欧 

A library called [**fdio**](/zircon/system/ulib/fdio/) is responsible for providing a unified interface to a variety of resources --files, sockets, services, pipes, and more. This layer defines a group offunctions, such as **read, write, open, close, seek, etc** that may be used onfile descriptors backed by a variety of protocols. Each supported protocol isresponsible for providing client-side code to interpret the specifics of theirinteraction. For example, **sockets** provide multiple handles to clients; oneacting for data flow, and one acting as a control plane. In contrast, **files**typically use only a single channel for control and data (unless extra work hasbeen done to ask for a memory mapping).  Although both sockets and files mightreceive a call to `open` or `write`, they will need to interpret those commandsdifferently. 名为[** fdio **]（/ zircon / system / ulib / fdio /）的库负责为各种资源（文件，套接字，服务，管道等）提供统一的接口。该层定义了一组功能，例如**读取，写入，打开，关闭，查找等**，可以在由各种协议支持的文件描述符上使用。每个受支持的协议负责提供客户端代码以解释其交互的细节。例如，套接字为客户端提供了多个句柄；一个充当数据流，另一个充当控制平面。相反，“文件”通常仅使用一个通道进行控制和数据处理（除非已完成额外的工作来请求内存映射）。尽管套接字和文件都可能收到对“ open”或“ write”的调用，但它们将需要不同地解释这些命令。

For the purposes of this document, we’ll be focusing on the primary protocol used by filesystem clients: [FIDL](/docs/development/languages/fidl/README.md). 在本文档中，我们将重点介绍文件系统客户端使用的主要协议：[FIDL]（/ docs / development / languages / fidl / README.md）。

 
## FIDL  FIDL 

A program calling `open("foo")` will have called into the standard library, found an “fdio” object corresponding to the current working directory, and willneed to send a request to a remote server to “please open foo”. How can this beaccomplished? The program has the following tools: 名为“ open（“ foo”）”的程序将调用标准库，找到与当前工作目录相对应的“ fdio”对象，并需要向远程服务器发送请求以“请打开foo”。如何做到这一点？该程序具有以下工具：

 
  * One or more **handles** representing a connection to the CWD  *一个或多个**句柄**表示与CWD的连接
  * [zx_channel_write](/docs/reference/syscalls/channel_write.md): A system call which can send bytes and handles (over a channel) * [zx_channel_write]（/ docs / reference / syscalls / channel_write.md）：可以发送字节和句柄（通过通道）的系统调用
  * [zx_channel_read](/docs/reference/syscalls/channel_read.md): A system call which can receive bytes and handles (over a channel) * [zx_channel_read]（/ docs / reference / syscalls / channel_read.md）：可以接收字节和处理（通过通道）的系统调用
  * [zx_object_wait_one](/docs/reference/syscalls/object_wait_one.md): A system call which can wait for a handle to be readable / writable * [zx_object_wait_one]（/ docs / reference / syscalls / object_wait_one.md）：一个系统调用，可以等待句柄可读/可写

Using these primitives, the client can write a message to the filesystem server on the CWD handle, which the server can read and then respond to with a“success” or “failure message” in a write back to the client. While the serveris crunching away, figuring out what to actually open, the client may or maynot choose to wait before trying to read the status message. 使用这些原语，客户端可以在CWD句柄上将消息写入文件系统服务器，服务器可以读取该消息，然后在回写给客户端的过程中以“成功”或“失败消息”进行响应。当服务器崩溃时，弄清楚实际要打开的内容时，客户端可能会或可能不会选择等待，然后再尝试读取状态消息。

It’s important that the client and server agree on the interpretation of those N bytes and N handles when messages are transmitted or received: if there isdisagreement between them, messages might be dropped (or worse, contorted intoan unintended behavior). Additionally, if this protocol allowed the client tohave arbitrary control over the server, this communication layer would be ripefor exploitation. 在发送或接收消息时，客户端和服务器必须对这N个字节和N个句柄的解释达成一致，这一点很重要：如果它们之间存在分歧，则消息可能会被丢弃（或更糟的是，被扭曲为意外行为）。另外，如果此协议允许客户端对服务器进行任意控制，则该通信层将变得成熟。

The [FIDL IO protocol](/zircon/system/fidl/fuchsia-io/io.fidl) describes the wire-format of what these bytes and handles should actually meanwhen transmitted between two entities. The protocol describes things like“expected number of handles”, “enumerated operation”, and “data”. In our case,`open("foo")` creates an `Open` message, and sets the “data” field of the FIDLmessage to the string “foo”. Additionally, if any flags are passed toopen (such as `O_RDONLY, O_RDWR, O_CREAT`, etc) these flags would be placed inthe “arg” field of the FIDL structure. However, if the operation was changed(to, for example, `write`), the interpretation of this message would bealtered. [FIDL IO协议]（/ zircon / system / fidl / fuchsia-io / io.fidl）描述了这些字节和句柄在两个实体之间传输时实际含义的有线格式。该协议描述了诸如“句柄的预期数量”，“枚举操作”和“数据”之类的内容。在我们的例子中，`open（“ foo”）`创建一个“ Open”消息，并将FIDLmessage的“ data”字段设置为字符串“ foo”。另外，如果将任何标志传递给open（例如O_RDONLY，O_RDWR，O_CREAT等），则这些标志将放置在FIDL结构的“ arg”字段中。但是，如果操作被更改（例如，更改为“ write”），则此消息的解释将被更改。

Exact byte agreement at this layer is critical, as it allows communication between drastically different runtimes: **processes which understand FIDL cancommunicate easily between C, C++, Go, Rust, Dart programs (and others)transparently.** 在这一层上，确切的字节协议至关重要，因为它允许在截然不同的运行时之间进行通信：**理解FIDL的进程可以轻松地在C，C ++，Go，Rust，Dart程序（和其他程序）之间透明地通信。**

**libfidl** contains both the client and server-side code for the C/C++ implementation of FIDL, and is responsible for automatically verifying the inputand output of both ends. ** libfidl **包含FIDL的C / C ++实现的客户端和服务器端代码，并负责自动验证两端的输入和输出。

In the case of the `open` operation, the FIDL protocol expects that the client will create a channel and pass one end (as a handle) to the server. Oncethe transaction is complete, this channel may be used as the mechanism tocommunicate with the opened file, just as there had previously been acommunication with the “CWD” handle. 在“打开”操作的情况下，FIDL协议希望客户端创建一个通道并将一端（作为句柄）传递给服务器。一旦交易完成，该通道就可以用作与打开的文件进行通信的机制，就像以前与“ CWD”句柄进行过通信一样。

By designing the protocol so FIDL clients provide handles, rather than servers, the communication is better suited to pipelining. Access to FIDL objects can beasynchronous; requests to the FIDL object can be transmitted before the objectis actually opened. This behavior is critical for interaction with services(which will be described in more detail in the “ServiceFS” section). 通过设计协议，以便FIDL客户端提供句柄而不是服务器，通信更适合流水线。对FIDL对象的访问可以是异步的。可以在实际打开对象之前发送对FIDL对象的请求。此行为对于与服务交互至关重要（将在“ ServiceFS”部分中进行详细说明）。

To recap, an “open” call has gone through the standard library, acted on the “CWD” fdio object, which transformed the request into a FIDL message which issent to the server using the `zx_channel_write` system call. The client canoptionally wait for the server’s response using `zx_object_wait_one`, or continueprocessing asynchronously. Either way, a channel has been created, whereone end lives with the client, and the other end is transmitted to the“server". 回顾一下，对“ CWD” fdio对象进行了“标准”库的“打开”调用，该调用将请求转换为FIDL消息，并使用“ zx_channel_write”系统调用将其发送到服务器。客户端可以选择使用“ zx_object_wait_one”等待服务器的响应，也可以异步继续处理。无论哪种方式，都已经创建了一个通道，其中一端与客户端一起生活，而另一端则传输到“服务器”。

 
## Filesystems: Server-Side  文件系统：服务器端 

 
### Dispatching  派遣 

Once the message has been transmitted from the client’s side of the channel, it lives in the server’s side of the channel, waiting to be read. The server isidentified by “whoever holds the handle to the other end of the channel” -- itmay live in the same (or a different) process as the client, use the same (or adifferent) runtime than the client, and be written in the same (or a differentlanguage) than the client. By using an agreed-upon wire-format, theinterprocess dependencies are bottlenecked at the thin communication layer thatoccurs over channels. 从通道的客户端发送完消息后，该消息将驻留在通道的服务器端，等待读取。服务器由“谁握住通道另一端的句柄的人”标识-服务器可能与客户端处于同一（或不同）进程中，使用与客户端相同（或不同）的运行时，并被写入与客户端相同（或不同的语言）。通过使用约定的线格式，进程间的依赖性在出现在通道上的瘦通信层处成为瓶颈。

At some point in the future, this server-side end of the CWD handle will need to read the message transmitted by the client. This process isn’t automatic --the server will need to intentionally wait for incoming messages on thereceiving handle, which in this case was the “current working directory”handle. When server objects (files, directories, services, etc) are opened,their handles are registered with a server-side Zircon **port** that waits fortheir underlying handles to be **readable** (implying a message has arrived) or**closed** (implying they will never receive more messages). This object whichdispatches incoming requests to appropriate handles is known as the dispatcher;it is responsible for redirecting incoming messages to a callback function,along with some previously-supplied “iostate” representing the open connection. 在将来的某个时候，CWD句柄的此服务器端将需要读取客户端发送的消息。此过程不是自动的-服务器需要有意地等待接收句柄上的传入消息，在这种情况下，该句柄是“当前工作目录”句柄。打开服务器对象（文件，目录，服务等）时，它们的句柄已在服务器端Zircon **端口**中注册，该端口等待其底层句柄被可读**（暗示消息已到达）或**关闭**（表示他们将永远不会收到更多消息）。该对象将传入的请求分配到适当的句柄，称为调度程序；它负责将传入的消息重定向到回调函数，以及先前提供的表示开放连接的“ iostate”。

For C++ filesystems using libfs, this callback function is called `vfs_handler`, and it receives a couple key pieces of information: 对于使用libfs的C ++文件系统，此回调函数称为`vfs_handler`，它接收一些关键信息：

 
  * The FIDL message which was provided by the client (or artificially constructed by the server to appear like a “close” message, if the handle was closed) *客户端提供的FIDL消息（或者如果句柄已关闭，则由服务器人工构造为显示为“关闭”消息）
  * The I/O state representing the current connection to the handle (passed as the “iostate” field, mentioned earlier). *表示当前到句柄的连接的I / O状态（通过前面提到的“ iostate”字段传递）。

`vfs_handler` can interpret the I/O state to infer additional information:  vfs_handler可以解释I / O状态以推断其他信息：

 
  * The seek pointer within the file (or within the directory, if readdir has been used)  *文件内（或目录内，如果已使用readdir）的搜索指针
  * The flags used to open the underlying resource  *用于打开基础资源的标志
  * The Vnode which represents the underlying object (and may be shared between multiple clients, or multiple file descriptors) *表示基础对象的Vnode（可以在多个客户端或多个文件描述符之间共享）

This handler function, equipped with this information, acts as a large “switch/case” table, redirecting the FIDL message to an appropriate functiondepending on the “operation” field provided by the client. In the open case, the`Open` ordinal is noticed as the operation, so (1) a handle is expected, and(2) the ‘data’ field (“foo”) is interpreted as the path. 配备了此信息的该处理程序功能充当大型“开关/案例”表，根据客户端提供的“操作”字段将FIDL消息重定向到适当的功能。在开放的情况下，“开放”序号被视为操作，因此（1）需要句柄，并且（2）“数据”字段（“ foo”）被解释为路径。

 
### VFS Layer  VFS层 

In Fuchsia, the “VFS layer” is a filesystem-independent library of code which may dispatch and interpret server-side messages, and call operations in theunderlying filesystem where appropriate. Notably, this layer is completelyoptional -- if a filesystem server does not want to link against this library,they have no obligation to use it. To be a filesystem server, a process mustmerely understand the FIDL wire format. As a consequence, there could beany number of “VFS” implementations in a language, but at the time of writing,two well-known implementations exist: one written in C++ within the[libfs library](/zircon/system/ulib/fs/),and another written in Go in the[rpc package of ThinFS](/garnet/go/src/thinfs/zircon/rpc/rpc.go). 在Fuchsia中，“ VFS层”是独立于文件系统的代码库，可以分派和解释服务器端消息，并在适当的情况下调用底层文件系统中的操作。值得注意的是，该层是完全可选的-如果文件系统服务器不想链接到该库，则它们没有使用它的义务。要成为文件系统服务器，进程必须完全了解FIDL有线格式。结果，一种语言中可以有许多“ VFS”实现，但是在撰写本文时，存在两种众所周知的实现：一种是在[libfs库]（/ zircon / system / ulib / fs中用C ++编写的实现。 /），以及用Go语言编写的另一个文件，它位于ThinFS的[rpc软件包]（/garnet/go/src/thinfs/zircon/rpc/rpc.go）中。

The VFS layer defines the interface of operations which may be routed to the underlying filesystem, including: VFS层定义了可以路由到基础文件系统的操作接口，包括：

 
  * Read/Write to a Vnode  *读/写到Vnode
  * Lookup/Create/Unlink a Vnode (by name) from a parent Vnode  *从父Vnode查找/创建/取消链接Vnode（按名称）
  * Rename/Link a Vnode by name  *通过名称重命名/链接Vnode
  * And many more  * 还有很多

To implement a filesystem (assuming a developer wants to use the shared VFS layer), one simply needs to define a Vnode implementing this interface and linkagainst a VFS layer. This will provide functionality like “path walking” and“filesystem mounting” with minimal effort, and almost no duplicated code. In aneffort to be filesystem-agnostic, the VFS layer has no preconceived notion ofthe underlying storage used by the filesystem: filesystems may require accessto block devices, networks, or simply memory to store data -- but the VFS layeronly deals with interfaces acting on paths, byte arrays of data, and vnodes. 要实现文件系统（假设开发人员要使用共享的VFS层），只需定义一个实现该接口的Vnode并与VFS层链接即可。这将以最小的努力提供“路径遍历”和“文件系统安装”等功能，并且几乎没有重复的代码。为了与文件系统无关，VFS层没有文件系统使用的底层存储的先入为主的概念：文件系统可能需要访问块设备，网络或仅访问内存来存储数据-但VFS层仅处理作用于路径的接口，数据的字节数组和vnode。

 
### Path Walking  路径行走 

To open a server-side resource, the server is provided some starting point (represented by the called handle) and a string path. This path is split intosegments by the “/” character, and each component is “looked up” with acallback to the underlying filesystem. If the lookup successfully returns avnode, and another “/” segment is detected, then the process continues until(1) `lookup` fails to find a component, (2) path processing reaches the lastcomponent in a path, or (3) `lookup` finds a **mountpoint vnode**, which is avnode that has an attached “remote” handle. For now, we will ignore mountpointvnodes, although they are discussed in a section on [filesystemmounting](/docs/concepts/storage/filesystems.md#Mounting). 要打开服务器端资源，需要为服务器提供一些起点（由调用的句柄表示）和字符串路径。该路径由“ /”字符分割成多个段，并且每个组件都通过对底层文件系统的回调来“查找”。如果查找成功返回avnode，并且检测到另一个“ /”段，则过程继续进行，直到（1）“ lookup”未能找到组件，（2）路径处理到达路径中的最后一个组件，或者（3） lookup查找一个“ mountpoint vnode”，它是具有附加的“远程”句柄的avnode。现在，我们将忽略mountpointvnode，尽管它们在[filesystemmounting]（/ docs / concepts / storage / filesystems.mdMounting）一节中进行了讨论。

Let’s assume `lookup` successfully found the “foo” Vnode. The filesystem server will proceed to call the VFS interface “Open”, verifying that the requestedresource can be accessed with the provided flags, before calling “GetHandles”asking the underlying filesystem if there are additional handles required tointeract with the Vnode. Assuming the client asked for the “foo” objectsynchronously (which is implied with the default POSIX open call), anyadditional handles required to interact with “foo” are packed into a small FIDLdescription object and passed back to the client. Alternatively, if "foo" hadfailed to open, a FIDL description object would still be returned, but with the“status” field set to an error code, indicating failure. Let’s assume the “foo”open was successful. The server will proceed to create an “iostate” object for“foo” and register it with the dispatcher. Doing so, future calls to “foo” canbe handled by the server. “Foo” has been opened, the client is now ready to sendadditional requests. 假设“ lookup”成功找到了“ foo” Vnode。文件系统服务器将继续调用VFS接口“ Open”，并在调用“ GetHandles”之前询问是否可以使用提供的标志访问所请求的资源，如果与Vnode交互还需要其他句柄，则询问基础文件系统。假设客户端同步地请求“ foo”对象（这是默认的POSIX打开调用所隐含的），则与“ foo”进行交互所需的任何其他句柄都打包到一个小的FIDLdescription对象中，并传递回客户端。或者，如果无法打开“ foo”，则仍将返回FIDL描述对象，但将“状态”字段设置为错误代码，表示失败。假设“ foo”打开成功。服务器将继续为“ foo”创建“ iostate”对象，并将其注册到调度程序中。这样做，以后可以由服务器处理对“ foo”的调用。 “ Foo”已打开，客户端现在准备发送其他请求。

From the client’s perspective, at the start of the “Open” call, a path and handle combination was transmitted over the CWD handle to a remote filesystemserver. Since the call was synchronous, the client proceeded to wait for aresponse on the handle. Once the server properly found, opened, and initializedI/O state for this file, it sent back a “success” FIDL description object. Thisobject would be read by the client, identifying that the call completedsuccessfully. At this point, the client could create an fdio objectrepresenting the handle to “foo”, reference it with an entry in a filedescriptor table, and return the fd back to whoever called the original “open”function. Furthermore, if the client wants to send any additional requests(such as “read” or “write”) to ‘foo’, then they can communicate directly withthe filesystem server by using the connection to the opened file -- there is noneed to route through the ‘CWD’ on future requests. 从客户端的角度来看，在“ Open”调用开始时，路径和句柄组合通过CWD句柄传输到了远程文件系统服务器。由于调用是同步的，因此客户端继续等待句柄上的响应。一旦服务器正确找到，打开并初始化了该文件的I / O状态，它就会发送回“成功” FIDL描述对象。客户端将读取此对象，以标识该呼叫已成功完成。此时，客户端可以创建一个fdio对象，表示“ foo”的句柄，使用filedescriptor表中的条目对其进行引用，然后将fd返回给称为原始“ open”函数的人。此外，如果客户端希望向“ foo”发送任何其他请求（例如“读”或“写”），则他们可以通过使用与打开文件的连接来直接与文件系统服务器通信-无需路由通过将来的请求通过“ CWD”。

 
## Life of an Open: Diagrams  开放的生活：图 

```
             +----------------+
             | Client Program |
+-----------------------------+
|   fd: x    |   fd: y    |
| Fdio (FIDL) | Fdio (FIDL) |
+-------------------------+
| '/' Handle | CWD Handle |
+-------------------------+
      ^            ^
      |            |
Zircon Channels, speaking FIDL                   State BEFORE open(‘foo’)
      |            |
      v            v
+-------------------------+
| '/' Handle | CWD Handle |
+-------------------------+
|  I/O State |  I/O State |
+-------------------------+
|   Vnode A  |   Vnode B  |
+------------------------------+
           | Filesystem Server |
           +-------------------+


             +----------------+
             | Client Program |
+-----------------------------+
|   fd: x    |   fd: y    |
| Fdio (FIDL) | Fdio (FIDL) |
+-------------------------+
| '/' Handle | CWD Handle |   **foo Handle x2**
+-------------------------+
      ^            ^
      |            |
Zircon Channels, speaking FIDL                   Client Creates Channel
      |            |
      v            v
+-------------------------+
| '/' Handle | CWD Handle |
+-------------------------+
|  I/O State |  I/O State |
+-------------------------+
|   Vnode A  |   Vnode B  |
+------------------------------+
           | Filesystem Server |
           +-------------------+


             +----------------+
             | Client Program |
+-----------------------------+
|   fd: x    |   fd: y    |
| Fdio (FIDL) | Fdio (FIDL) |
+-------------------------+--------------+
| '/' Handle | CWD Handle | ‘foo’ Handle |
+-------------------------+--------------+
      ^            ^
      |            |
Zircon Channels, speaking FIDL                  Client Sends FIDL message to Server
      |            |                            Message includes a ‘foo’ handle
      v            v                            (and waits for response)
+-------------------------+
| '/' Handle | CWD Handle |
+-------------------------+
|  I/O State |  I/O State |
+-------------------------+
|   Vnode A  |   Vnode B  |
+------------------------------+
           | Filesystem Server |
           +-------------------+


             +----------------+
             | Client Program |
+-----------------------------+
|   fd: x    |   fd: y    |
| Fdio (FIDL) | Fdio (FIDL) |
+-------------------------+--------------+
| '/' Handle | CWD Handle | ‘foo’ Handle |
+-------------------------+--------------+
      ^            ^
      |            |
Zircon Channels, speaking FIDL                  Server dispatches message to I/O State,
      |            |                            Interprets as ‘open’
      v            v                            Finds or Creates ‘foo’
+-------------------------+
| '/' Handle | CWD Handle |
+-------------------------+
|  I/O State |  I/O State |
+-------------------------+-------------+
|   Vnode A  |   Vnode B  |   Vnode C   |
+------------------------------+--------+
           | Filesystem Server |
           +-------------------+


             +----------------+
             | Client Program |
+-----------------------------+
|   fd: x    |   fd: y    |
| Fdio (FIDL) | Fdio (FIDL) |
+-------------------------+--------------+
| '/' Handle | CWD Handle | ‘foo’ Handle |
+-------------------------+--------------+
      ^            ^          ^
      |            |          |
Zircon Channels, FIDL         |                   Server allocates I/O state for Vnode
      |            |          |                   Responds to client-provided handle
      v            v          v
+-------------------------+--------------+
| '/' Handle | CWD Handle | ‘foo’ Handle |
+-------------------------+--------------+
|  I/O State |  I/O State |  I/O State   |
+-------------------------+--------------+
|   Vnode A  |   Vnode B  |    Vnode C   |
+------------------------------+---------+
           | Filesystem Server |
           +-------------------+


             +----------------+
             | Client Program |
+-----------------------------+----------+
|   fd: x    |   fd: y    |    fd: z     |
| Fdio (FIDL) | Fdio (FIDL) |  Fdio (FIDL)  |
+-------------------------+--------------+
| '/' Handle | CWD Handle | ‘foo’ Handle |
+-------------------------+--------------+
      ^            ^          ^
      |            |          |
Zircon Channels, speaking FIDL |                  Client recognizes that ‘foo’ was opened
      |            |          |                   Allocated Fdio + fd, ‘open’ succeeds.
      v            v          v
+-------------------------+--------------+
| '/' Handle | CWD Handle | ‘foo’ Handle |
+-------------------------+--------------+
|  I/O State |  I/O State |  I/O State   |
+-------------------------+--------------+
|   Vnode A  |   Vnode B  |    Vnode C   |
+------------------------------+---------+
           | Filesystem Server |
           +-------------------+
```
