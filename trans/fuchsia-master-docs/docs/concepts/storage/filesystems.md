 
# Filesystem Architecture  文件系统架构 

This document seeks to describe a high-level view of the Fuchsia filesystems, from their initialization, discussion of standard filesystem operations (such asOpen, Read, Write, etc), and the quirks of implementing user-space filesystemson top of a microkernel. Additionally, this document describes the VFS-levelwalking through a namespace which can be used to communicate with non-storageentities (such as system services). 本文档旨在通过其初始化，对标准文件系统操作（如Open，Read，Write等）的讨论以及在微内核顶部实现用户空间文件系统的怪癖来描述Fuchsia文件系统的高级视图。此外，本文档还介绍了通过命名空间进行VFS级别遍历的过程，该命名空间可用于与非存储实体（例如系统服务）进行通信。

 
## Filesystems are Services  文件系统即服务 

Unlike more common monolithic kernels, Fuchsia’s filesystems live entirely within userspace. They are not linked nor loaded with the kernel; they aresimply userspace processes which implement servers that can appear asfilesystems. As a consequence, Fuchsia’s filesystems themselves can be changedwith ease -- modifications don’t require recompiling the kernel. In fact,updating to a new Fuchsia filesystem can be done without rebooting. 与更常见的单片内核不同，Fuchsia的文件系统完全位于用户空间中。它们没有链接，也没有加载内核。它们只是用户空间进程，这些进程实现了可以显示为文件系统的服务器。因此，Fuchsia的文件系统本身可以轻松更改-修改无需重新编译内核。实际上，无需重新启动即可更新到新的Fuchsia文件系统。

Like other native servers on Fuchsia, the primary mode of interaction with a filesystem server is achieved using the handle primitive rather than systemcalls. The kernel has no knowledge about files, directories, or filesystems. Asa consequence, filesystem clients cannot ask the kernel for “filesystem access”directly. 像Fuchsia上的其他本机服务器一样，与文件系统服务器交互的主要方式是通过使用句柄原语而不是系统调用来实现的。内核不了解文件，目录或文件系统。结果，文件系统客户端无法直接向内核请求“文件系统访问”。

This architecture implies that the interaction with filesystems is limited to the following interface: 此体系结构意味着与文件系统的交互限于以下接口：

 
 * The messages sent on communication channels established with the filesystem server. These communication channels may be local for a client-sidefilesystem, or remote. *在与文件系统服务器建立的通信通道上发送的消息。这些通信通道对于客户端文件系统可能是本地的，也可能是远程的。
 * The initialization routine (which is expected to be configured heavily on a per-filesystem basis; a networking filesystem would require network access,persistent filesystems may require block device access, in-memory filesystemswould only require a mechanism to allocate new temporary pages). *初始化例程（预计将在每个文件系统的基础上进行大量配置；网络文件系统将需要网络访问，持久性文件系统可能需要块设备访问，内存中文件系统仅需要一种机制来分配新的临时页面）。

As a benefit of this interface, any resources accessible via a channel can make themselves appear like filesystems by implementing the expected protocols forfiles or directories. For example, “serviceFS” (discussed in more detail laterin this document) allows for service discovery through a filesystem interface. 利用此接口，通过实现文件或目录的预期协议，可通过通道访问的任何资源都可以使自己看起来像文件系统。例如，“ serviceFS”（在本文档的后面部分有更详细的讨论）允许通过文件系统接口发现服务。

 
## File Lifecycle  文件生命周期 

 
### Establishing a Connection  建立连接 

To open a file, Fuchsia programs (clients) send RPC requests to filesystem servers using a FIDL. 为了打开文件，Fuchsia程序（客户端）使用FIDL将RPC请求发送到文件系统服务器。

FIDL defines the wire-format for transmitting messages and handles between a filesystem client and server. Instead of interacting with a kernel-implementedVFS layer, Fuchsia processes send requests to filesystem services whichimplement protocols for Files, Directories, and Devices. To send one of theseopen requests, a Fuchsia process must transmit an RPC message over an existinghandle to a directory; for more detail on this process, refer to the [life of anopen document](/docs/concepts/system/life_of_an_open.md). FIDL定义了在文件系统客户端和服务器之间传输消息和句柄的有线格式。紫红色进程没有与内核实现的VFS层进行交互，而是将请求发送到实现文件，目录和设备协议的文件系统服务。要发送这些打开请求之一，一个Fuchsia进程必须通过现有的句柄将RPC消息传输到目录。有关此过程的更多详细信息，请参阅[打开文档的生存期]（/ docs / concepts / system / life_of_an_open.md）。

 
### Namespaces  命名空间 

On Fuchsia, a [namespace](/docs/concepts/framework/namespaces.md) is a small filesystem which exists entirely within the client. At the most basic level, the idea of the clientsaving “/” as root and associating a handle with it is a very primitivenamespace. Instead of a typical singular "global" filesystem namespace, Fuchsiaprocesses can be provided an arbitrary directory handle to represent "root",limiting the scope of their namespace. In order to limit this scope, Fuchsiafilesystems [intentionally do not allow access to parent directories viadotdot](/docs/concepts/storage/dotdot.md). 在紫红色上，[namespace]（/ docs / concepts / framework / namespaces.md）是一个很小的文件系统，完全存在于客户端中。在最基本的级别上，客户端将“ /”保存为根并将其关联到句柄的想法是一个非常原始的命名空间。代替典型的单一“全局”文件系统名称空间，可以为Fuchsiaprocesses提供表示“根”的任意目录句柄，从而限制其名称空间的范围。为了限制此范围，Fuchsia文件系统[故意不允许通过dotdot访问父目录]（/ docs / concepts / storage / dotdot.md）。

Fuchsia processes may additionally redirect certain path operations to separate filesystem servers. When a client refers to “/bin”, the client may opt toredirect these requests to a local handle representing the “/bin” directory,rather than sending a request directly to the “bin” directory within the “root”directory. Namespaces, like all filesystem constructs, are not visible from thekernel: rather, they are implemented in client-side runtimes (such as[libfdio](/docs/concepts/system/life_of_an_open.md#Fdio)) and are interposed between most client codeand the handles to remote filesystems. 紫红色进程可能还会将某些路径操作重定向到单独的文件系统服务器。当客户端引用“ / bin”时，客户端可以选择将这些请求重定向到表示“ / bin”目录的本地句柄，而不是直接将请求发送到“ root”目录中的“ bin”目录。像所有文件系统构造一样，名称空间在内核中也不可见：它们是在客户端运行时中实现的（例如libfdio（/docs/concepts/system/life_of_an_open.mdFdio）），并且介于大多数客户端代码和处理远程文件系统。

Since namespaces operate on handles, and most Fuchsia resources and services are accessible through handles, they are extremely powerful concepts.Filesystem objects (such as directories and files), services, devices,packages, and environments (visible by privileged processes) all are usablethrough handles, and may be composed arbitrarily within a child process. As aresult, namespaces allows for customizable resource discovery withinapplications. The services that one process observes within “/svc” may or maynot match what other processes see, and can be restricted or redirectedaccording to application-launching policy. 由于名称空间在句柄上运行，并且大多数Fuchsia资源和服务都可以通过句柄进行访问，因此它们是非常强大的概念，文件系统对象（例如目录和文件），服务，设备，程序包和环境（由特权进程可见）都可以通过以下方式使用处理，并且可以在子进程中任意组成。因此，名称空间允许在应用程序中发现可自定义的资源。一个进程在“ / svc”中观察到的服务可能匹配或可能不匹配其他进程看到的服务，并且可以根据应用程序启动策略对其进行限制或重定向。

For more detail the mechanisms and policies applied to restricting process capability, refer to the documentation on[sandboxing](/docs/concepts/framework/sandboxing.md). 有关用于限制流程功能的机制和策略的更多详细信息，请参阅[沙盒装箱]（/ docs / concepts / framework / sandboxing.md）上的文档。

 
### Passing Data  传递数据 

Once a connection has been established, either to a file, directory, device, or service, subsequent operations are also transmitted using RPC messages.These messages are transmitted on one or more handles, using a wire format thatthe server validates and understands. 建立到文件，目录，设备或服务的连接后，还将使用RPC消息传输后续操作。这些消息将使用服务器验证并理解的有线格式在一个或多个句柄上传输。

In the case of files, directories, devices, and services, these operations use the FIDL protocol. 对于文件，目录，设备和服务，这些操作使用FIDL协议。

As an example, to seek within a file, a client would send a `Seek` message with the desired position and “whence” within the FIDL message, and thenew seek position would be returned. To truncate a file, a `Truncate`message could be sent with the new desired filesystem, and a status messagewould be returned. To read a directory, a `ReadDirents` message could besent, and a list of direntries would be returned. If these requests were sent toa filesystem entity that can’t handle them, an error would be sent, and theoperation would not be executed (like a `ReadDirents` message sent to a textfile). 作为示例，为了在文件内进行查找，客户端将发送带有所需位置的FIRST消息中的“查找”消息，并在FIDL消息中发送“因此”，然后将返回新的查找位置。要截断文件，可以发送“ Truncate”消息和新的所需文件系统，并返回状态消息。要读取目录，可能会发送“ ReadDirents”消息，并返回目录列表。如果将这些请求发送到无法处理的文件系统实体，则会发送错误，并且操作将不会执行（例如向文本文件发送的“ ReadDirents”消息）。

 
### Memory Mapping  内存映射 

For filesystems capable of supporting it, memory mapping files is slightly more complicated. To actually “mmap” part of a file, a client sends an “GetVmo”message, and receives a Virtual Memory Object, or VMO, in response. This objectis then typically mapped into the client’s address space using a Virtual MemoryAddress Region, or VMAR. Transmitting a limited view of the file’s internal“VMO” back to the client requires extra work by the intermediate messagepassing layers, so they can be aware they’re passing back a server-vendoredobject handle. 对于能够支持它的文件系统，内存映射文件要稍微复杂一些。为了实际“映射”文件的一部分，客户端发送“ GetVmo”消息，并接收虚拟内存对象（VMO）作为响应。然后，通常使用Virtual MemoryAddress Region（虚拟内存地址区域）或VMAR将这个对象映射到客户端的地址空间。将文件内部“ VMO”的有限视图发送回客户端需要中间消息传递层进行额外的工作，因此他们可以知道它们正在传递回服务器供应的对象句柄。

By passing back these virtual memory objects, clients can quickly access the internal bytes representing the file without actually undergoing the cost of around-trip IPC message. This feature makes mmap an attractive option forclients attempting high-throughput on filesystem interaction. 通过传回这些虚拟内存对象，客户端可以快速访问代表文件的内部字节，而无需实际花费往返IPC消息的费用。对于试图在文件系统交互上实现高吞吐量的客户端，mmap的这一功能使其成为有吸引力的选择。

At the time of writing, on-demand paging is not supported by the kernel, and has not been wired into filesystems. As a result, if a clientwrites to a “memory-mapped” region, the filesystem cannot reasonably identifywhich pages have and have not been touched. To cope with this restriction, mmaphas only been implemented on **read-only filesystems**, such as blobfs. 在撰写本文时，内核不支持按需分页，并且尚未将其连接到文件系统中。结果，如果客户端写入“内存映射”区域，则文件系统将无法合理地识别哪些页面已被触摸，哪些页面尚未被触摸。为了解决此限制，mmapha仅在**只读文件系统**（例如blobfs）上实现。

 
### Other Operations acting on paths  作用在路径上的其他操作 

In addition to the “open” operation, there are a couple other path-based operations worth discussing: “rename” and “link”. Unlike “open”, theseoperations actually act on multiple paths at once, rather than a singlelocation. This complicates their usage: if a call to “rename(‘/foo/bar’,‘baz’)” is made, the filesystem needs to figure out a way to: 除了“打开”操作外，还有一些其他值得讨论的基于路径的操作：“重命名”和“链接”。与“开放”不同，这些操作实际上一次作用于多个路径，而不是单个位置。这使它们的使用变得复杂：如果调用了“ rename（'/ foo / bar'，'baz'）”，则文件系统需要找出一种方法：

 
  * Traverse both paths, even when they have distinct starting points (which is the case this here; one path starts at root, and other starts at the CWD) *遍历两条路径，即使它们有不同的起点（此处就是这种情况；一条路径从根开始，另一条路径从CWD开始）
  * Open the parent directories of both paths  *打开两个路径的父目录
  * Operate on both parent directories and trailing pathnames simultaneously  *同时在父目录和尾随路径名上操作

To satisfy this behavior, the VFS layer takes advantage of a Zircon concept called “cookies”. These cookies allow client-side operations to store openstate on a server, using a handle, and refer to it later using that samehandles. Fuchsia filesystems use this ability to refer to one Vnode whileacting on the other. 为了满足此行为，VFS层利用了一种称为“ cookies”的Zircon概念。这些cookie允许客户端操作使用句柄将openstate存储在服务器上，并在以后使用相同的句柄引用它。紫红色文件系统使用此功能来引用一个Vnode，同时作用于另一个。

These multi-path operations do the following:  这些多路径操作执行以下操作：

 
  * Open the parent source vnode (for “/foo/bar”, this means opening “/foo”)  *打开父源vnode（对于“ / foo / bar”，这意味着打开“ / foo”）
  * Open the target parent vnode (for “baz”, this means opening the current working directory) and acquire a vnode token using the operation`GetToken`, which is a handle to a filesystem cookie. *打开目标父vnode（对于“ baz”，这意味着打开当前工作目录）并使用“ GetToken”操作获取vnode令牌，该操作是文件系统cookie的句柄。
  * Send a “rename” request to the source parent vnode, along with the source and destination paths (“bar” and “baz”), along with the vnode token acquiredearlier. This provides a mechanism for the filesystem to safely refer to thedestination vnode indirectly -- if the client provides an invalid handle, thekernel will reject the request to access the cookie, and the server can returnan error. *向源父vnode发送“重命名”请求，以及源路径和目标路径（“ bar”和“ baz”）以及较早获取的vnode令牌。这为文件系统提供了一种机制，可以安全地间接引用目标vnode －如果客户端提供了无效的句柄，则内核将拒绝访问cookie的请求，并且服务器可以返回错误。

 
## Filesystem Lifecycle  文件系统生命周期 

 
### Mounting  安装 

When Fuchsia filesystems are initialized, they are created with typically two handles: One handle to a channel used to communicate with the mountingfilesystem (referred to as the “mount point” channel -- the “mounting” end ofthis channel is saved as a field named “remote” in the parent Vnode, the otherend will be connected to the root directory of the new filesystem), and(optionally) another to contact the underlying [block device](block_devices.md).Once a filesystem has been initialized (reading initial state off the blockdevice, finding the root vnode, etc) it flags a signal (`ZX_USER_SIGNAL0`) onthe mount point channel. This informs the parent (mounting) system that thechild filesystem is ready to be utilized. At this point, the channel passed tothe filesystem on initialization may be used to send filesystem requests, suchas “open”. 初始化Fuchsia文件系统时，通常使用两个句柄来创建它们：用于与Mountingfilesystem进行通信的通道的一个句柄（称为“安装点”通道-该通道的“ mounting”端保存为名为的字段在父Vnode中“远程”，另一端将连接到新文件系统的根目录），（另一端）将连接到底层的[block device]（block_devices.md）。一旦文件系统被初始化（读取块设备的初始状态，找到根vnode等），它会在安装点通道上标记一个信号（“ ZX_USER_SIGNAL0”）。这会通知父（挂载）系统子文件系统已准备好使用。此时，初始化时传递给文件系统的通道可用于发送文件系统请求，例如“打开”。

At this point, the parent (mounting) filesystem “pins” the connection to the remote filesystem on a Vnode. The VFS layers capable of path walking check forthis remote handle when observing Vnodes: if a remote handle is detected, thenthe incoming request (open, rename, etc) is forwarded to the remote filesysteminstead of the underlying node. If a user actually wants to interact with themountpoint node, rather than the remote filesystem, they can pass the`O_NOREMOTE` flag to the “open” operation identify this intention. 此时，父（挂载）文件系统将连接“固定”到Vnode上的远程文件系统。能够进行路径遍历的VFS层在观察Vnode时检查此远程句柄：如果检测到远程句柄，则将传入请求（打开，重命名等）转发到远程文件系统，而不是基础节点。如果用户实际上想与装载点节点而不是与远程文件系统进行交互，则可以将O_NOREMOTE标志传递给“ open”操作以标识此意图。

Unlike many other operating systems, the notion of “mounted filesystems” does not live in a globally accessible table. Instead, the question “whatmountpoints exist?” can only be answered on a filesystem-specific basis -- anarbitrary filesystem may not have access to the information about whatmountpoints exist elsewhere. 与许多其他操作系统不同，“挂载文件系统”的概念并不存在于可全局访问的表中。取而代之的是，“什么数量点存在？”问题只能在特定于文件系统的基础上回答-任意文件系统可能无法访问有关其他位置存在的数量点的信息。

 
### Filesystem Management  文件系统管理 

There are a collection of filesystem operations which are considered related to "administration", including "unmounting the current filesystem", "querying forthe underlying block device path", etc. These operations are defined by theDirectoryAdmin interface within [io.fidl](/zircon/system/fidl/fuchsia-io/io.fidl).A connection to this interface allows access to "filesystem-wide" state, and isrestricted by an access flag `ZX_FS_RIGHT_ADMIN`. This access right must berequested explicitly, and is not granted when requested on a connection lacking`ZX_FS_RIGHT_ADMIN`. This right is provided to the root connection of afilesystem once it is mounted - a reasonable bootstrapping point foradministration - but must be preserved by the mounting tools to propagate thisaccess, or must be dropped when vending connections from the filesystem to lessprivileged clients. 有一系列文件系统操作被认为与“管理”相关，包括“卸载当前文件系统”，“查询底层块设备路径”等。这些操作由[io.fidl]（/ zircon / system / fidl / fuchsia-io / io.fidl）。与此接口的连接允许访问“文件系统范围”状态，并受访问标志“ ZX_FS_RIGHT_ADMIN”限制。此访问权限必须明确地请求，并且在缺少ZX_FS_RIGHT_ADMIN的连接上被请求时不被授予。一旦安装了文件系统，该权限将提供给文件系统的根连接（这是管理的合理引导点），但必须由安装工具保留以传播此访问权限，或者在将文件系统的连接出售给特权较少的客户端时必须将其删除。

This `ZX_FS_RIGHT_ADMIN` mechanism (occasionally referred to as `O_ADMIN`, for the POSIX interop declaration) will be superceded by an explicit service forfilesystem administration. Rather than existing as an "implicit right" attachedsilently to limited directory connections, it will be a separate interfaceexposed by filesystem components. This will (in the abstract) allow filesystemsto expose a "root directory" handle and an "administraction" handle separately,rather than overloading them on the same connection. Once this transition hasoccurred, the `ZX_FS_RIGHT_ADMIN` (and `O_ADMIN`) flags will be deprecated. 这种ZX_FS_RIGHT_ADMIN机制（对于POSIX互操作声明，有时称为O_ADMIN）将被用于文件系统管理的显式服务所取代。它不是以沉默的方式附加到有限的目录连接上，而是由文件系统组件公开的单独接口。 （抽象地），这将允许文件系统分别公开“根目录”句柄和“ administraction”句柄，而不是在同一连接上重载它们。一旦发生这种转换，将不建议使用ZX_FS_RIGHT_ADMIN（和O_ADMIN）标志。

 
## Current Filesystems  当前文件系统 

Due to the modular nature of Fuchsia’s architecture, it is straightforward to add filesystems to the system. At the moment, a handful of filesystems exist,intending to satisfy a variety of distinct needs. 由于Fuchsia架构的模块化性质，因此很容易在系统中添加文件系统。目前，存在少数文件系统，旨在满足各种不同的需求。

 
### MemFS: An in-memory filesystem  MemFS：内存文件系统 

[MemFS](/zircon/system/ulib/memfs) is used to implement requests to temporary filesystems like `/tmp`, where filesexist entirely in RAM, and are not transmitted to an underlying block device.This filesystem is also currently used for the “bootfs” protocol, where alarge, read-only VMO representing a collection of files and directories isunwrapped into user-accessible Vnodes at boot (these files are accessible in`/boot`). [MemFS]（/ zircon / system / ulib / memfs）用于执行对`/ tmp'等临时文件系统的请求，这些文件完全存在于RAM中，并且不会传输到底层块设备。该文件系统目前也用于“ bootfs”协议，在启动时将代表文件和目录集合的大型只读VMO展开到用户可访问的Vnode中（这些文件可在`/ boot`中访问）。

 
### MinFS: A persistent filesystem  MinFS：持久文件系统 

[MinFS](/zircon/system/uapp/minfs/) is a simple, traditional filesystem which is capable of storing filespersistently. Like MemFS, it makes extensive use of the VFS layers mentionedearlier, but unlike MemFS, it requires an additional handle to a block device(which is transmitted on startup to a new MinFS process). For ease of use,MinFS also supplies a variety of tools: “mkfs” for formatting, “fsck” forverification, as well as “mount” and “umount” for adding and subtracting MinFSfilesystems to a namespace from the command line. [MinFS]（/ zircon / system / uapp / minfs /）是一个简单的传统文件系统，能够持久存储文件。像MemFS一样，它广泛使用了前面提到的VFS层，但是与MemFS不同，它需要块设备的附加句柄（在启动时传输到新的MinFS进程）。为了易于使用，MinFS还提供了各种工具：用于格式化的“ mkfs”，用于验证的“ fsck”以及用于从命令行向名称空间添加和减去MinFS文件系统的“ mount”和“ umount”。

 
### Blobfs: An immutable, integrity-verifying package storage filesystem  Blobfs：不变的，通过完整性验证的程序包存储文件系统 

[Blobfs](/zircon/system/uapp/blobfs/) is a simple, flat filesystem optimized for “write-once, then read-only” [signeddata](merkleroot.md), such as [packages](package.md).Other than two small prerequisites (file names which are deterministic, contentaddressable hashes of a file’s Merkle Tree root, for integrity-verification)and forward knowledge of file size (identified to Blobfs by a call to“ftruncate” before writing a blob to storage), Blobfs appears like atypical filesystem. It can be mounted and unmounted, it appears to contain asingle flat directory of hashes, and blobs can be accessed by operations like“open”, “read”, “stat” and “mmap”. [Blobfs]（/ zircon / system / uapp / blobfs /）是一个简单的平面文件系统，已针对“一次写入，然后只读”进行了优化，[signeddata]（merkleroot.md），例如[packages]（package.md） ）。除了两个小的前提条件（文件名是确定性的，文件的Merkle树根的内容可寻址的哈希值，用于完整性验证）和转发文件大小的知识（通过在将blob写入Blob之前通过调用“ ftruncate”标识给Blobfs）之前，存储），Blobfs看起来就像非典型文件系统。它可以被安装和卸载，它似乎包含一个单一的哈希目录，并且可以通过诸如“ open”，“ read”，“ stat”和“ mmap”之类的操作来访问blob。

 
### ThinFS: A FAT filesystem written in Go  ThinGS：用Go编写的FAT文件系统 

[ThinFS](/garnet/go/src/thinfs/) is an implementation of a FAT filesystem in Go. It serves a dual purpose: first, proving that our systemis actually modular, and capable of using novel filesystems, regardless oflanguage or runtime. Secondly, it provides a mechanism for reading a universalfilesystem, found on EFI partitions and many USB sticks. [ThinFS]（/ garnet / go / src / thinfs /）是Go中FAT文件系统的实现。它具有双重目的：首先，证明我们的系统实际上是模块化的，并且能够使用新颖的文件系统，而与语言或运行时无关。其次，它提供了一种读取通用文件系统的机制，该文件系统位于EFI分区和许多USB记忆棒上。

 
### FVM  虚拟机 

[Fuchsia Volume Manager](/zircon/system/dev/block/fvm/) is a "logical volume manager" that adds flexibility on top of existing blockdevices. The current features include ability to add, remove, extend andshrink virtual partitions. To make these features possible, internally, fvmmaintains physical to virtual  mapping from (virtual partitions, blocks) to(slice, physical block). To keep maintenance overhead minimal, it allows topartitions to shrink/grow in chunks called slices. A slice is multiple of thenative block size. Metadata aside, the rest of the device is divided intoslices. Each slice is either free or it belongs to one and only one partition.If a slice belongs to a partition then FVM maintains metadata about whichpartition is using the slice, and the virtual address of the slice withinthat partition. [Fuchsia Volume Manager]（/ zircon / system / dev / block / fvm /）是一种“逻辑卷管理器”，可在现有块设备之上增加灵活性。当前的功能包括添加，删除，扩展和缩小虚拟分区的功能。为了使这些功能成为可能，fvm在内部保留了从（虚拟分区，块）到（切片，物理块）的物理到虚拟的映射。为了使维护开销降至最低，它允许分区以称为切片的块的形式缩小/增长。切片是假定块大小的倍数。除了元数据外，设备的其余部分分为多个切片。每个分片都是免费的，或者属于一个分区，并且仅属于一个分区。如果一个分片属于一个分区，则FVM会维护有关使用该分片的分区以及该分区内分片的虚拟地址的元数据。

[Superblock](/zircon/system/ulib/fvm/include/fvm/format.h#27) at block zero describe the on-disk layout of the FVM, which may look like [Superblock]（/ zircon / system / ulib / fvm / include / fvm / format.h27）在零块处描述了FVM的磁盘布局，如下所示

```c
      +---------------------------------+ <- Physical block 0
      |           metadata              |
      | +-----------------------------+ |
      | |       metadata copy 1       | |
      | |  +------------------------+ | |
      | |  |    superblock          | | |
      | |  +------------------------+ | |
      | |  |    partition table     | | |
      | |  +------------------------+ | |
      | |  | slice allocation table | | |
      | |  +------------------------+ | |
      | +-----------------------------+ | <- Size of metadata is described by
      | |       metadata copy 2       | |    superblock
      | +-----------------------------+ |
      +---------------------------------+ <- Superblock describes start of
      |                                 |    slices
      |             Slice 1             |
      +---------------------------------+
      |                                 |
      |             Slice 2             |
      +---------------------------------+
      |                                 |
      |             Slice 3             |
      +---------------------------------+
      |                                 |
```
 

The partition table is made of several virtual partition entries(`vpart_entry_t`). In addition to containing name and partitionidentifiers, each of these vpart entries contains the number of allocatedslices for this partition. 分区表由几个虚拟分区条目（`vpart_entry_t`）组成。除了包含名称和分区标识符之外，每个这些vpart条目还包含为此分区分配的切片数。

The slice allocation table is made up of tightly packed slice entries (`slice_entry_t`). Each entry contains 切片分配表由紧密打包的切片条目（slice_entry_t）组成。每个条目包含

 
 * allocation status  *分配状态
 * if it is allocated,  *如果已分配，
   * what partition it belongs to and  *它属于哪个分区，以及
   * what logical slice within partition the slice maps to  *分区映射到分区内的哪个逻辑分区

