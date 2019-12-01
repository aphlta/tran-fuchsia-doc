 
# Dot Dot Considered Harmful  点被认为有害 

Child processes on Fuchsia are only capable of accessing the resources provided to them -- this is an essential idea encompassing microkernels, and other“capability-based” systems. If a handle is provided to a service, access tothat handle implies the client can use it. 紫红色的子进程只能访问为其提供的资源-这是包含微内核和其他“基于能力”系统的基本思想。如果为服务提供了句柄，则对该句柄的访问意味着客户端可以使用它。

Intuitively, this concept can be applied to filesystems: If a handle is provided to a directory, it should imply access to resources within thatdirectory (and additionally, their subdirectories). Unfortunately, however, aholdout from POSIX prevents directory handles from cleanly integrating withthese concepts in a capability system: “..”. If a handle is provided to adirectory, the client can simply request “..”, and the handle will be“upgraded” to access the parent directory, with broader scope. As aconsequence, this implies that a handle to a directory can be upgradedarbitrarily to access the entire filesystem. 直观地，该概念可以应用于文件系统：如果将句柄提供给目录，则它应意味着访问该目录（及其子目录）中的资源。但是，不幸的是，POSIX的保留使目录句柄无法与这些概念完全集成到能力系统“ ..”中。如果为目录提供了句柄，则客户端可以简单地请求“ ..”，并且句柄将被“升级”以访问父目录，范围更广。因此，这意味着可以任意升级目录的句柄以访问整个文件系统。

Traditionally, filesystems have tried to combat this using "chroot", which changes the notion of a filesystem root, preventing access beyond ".." intrivial cases of path traversal. However, this approach has some problems: 传统上，文件系统尝试使用“ chroot”来解决此问题，该更改会更改文件系统根目录的概念，从而防止超出路径遍历的“ ..”特殊情况。但是，这种方法存在一些问题：

 
  * Chroot changes the notion of root on a coarse, "per-program" basis, not on a per-descriptor basis * Chroot在“每个程序”的基础上而不是在每个描述符的基础上更改了root的概念
  * Chroots are often misused (i.e., fchdir to a different open handle which sits outside the chroot) * chroot通常被滥用（例如，将fchdir替换为位于chroot之外的其他打开句柄）
  * Chroots are not "on by default", so it may be tempting for programs to simply not use them. * Chroots并非“默认情况下处于启用状态”，因此程序可能会很愿意不使用它们。

To overcome these deficiencies, Fuchsia does not implement traditional dot dot semantics on filesystem servers, which would allow open directories to traverseupward. More specifically, it disallows access to “..”, preventing clientsfrom trivially accessing parent directories. This provides some strongproperties for process creation: If an application manager only wants to give aprocess access to "/data/my_private_data", then it can simply provide a handleto that open directory to the child process, and it will "automatically" besandboxed. 为了克服这些缺陷，Fuchsia没有在文件系统服务器上实现传统的点点语义，这将允许打开的目录向上移动。更具体地说，它不允许访问“ ..”，从而防止客户端琐碎地访问父目录。这为进程创建提供了一些强大的属性：如果应用程序管理器仅希望授予进程对“ / data / my_private_data”的访问权限，则它可以简单地为子进程提供该打开目录的句柄，并且它将“自动”被装箱。

 
## What about paths which can be resolved without the filesystem server?  没有文件系统服务器就可以解析的路径呢？ 

Certain paths, such as “foo/../bar”, which can be transformed to “bar”, can be determined without accessing a filesystem server in the absence of symboliclinks (and at the time of writing, symbolic links do not exist on Fuchsia).These paths may be canonicalized, or cleaned, on the client-side, prior tosending path-based requests to filesystem servers: the libfdio library alreadydoes this for any fdio operations which are eventually transmitted tofilesystem servers in a function called `__fdio_cleanpath`. 在没有符号链接的情况下，无需访问文件系统服务器就可以确定某些路径，例如可以转换为“ bar”的“ foo /../ bar”（并且在撰写本文时，符号链接不存在于在将基于路径的请求发送到文件系统服务器之前，可以在客户端规范化或清除这些路径：libfdio库已经对所有fdio操作执行了此操作，最终这些fdio操作最终通过称为__fdio_cleanpath的函数传输到文件系统服务器。 。

 
## What about shell traversal?  壳遍历怎么样？ 

I.e, if someone “cd”s into a directory, how can they leave? Internally, the notion of “CWD” isn’t merely a file descriptor to an open directory; rather,it’s a combination of “file descriptor” and “absolute path interpreted to meanCWD”. If all operations to cd act on this absolute path, then “..” can alwaysbe resolved locally on a client, rather than being transmitted to a filesystemserver. For example, if the CWD is “/foo/bar”, and a user calls “cd ..”, thenthe underlying call may be transformed into “chdir /foo/bar/..”, which can becanonicalized to “/foo”. 也就是说，如果有人“ cd”进入目录，他们如何离开？在内部，“ CWD”的概念不仅仅是打开目录的文件描述符。相反，它是“文件描述符”和“解释为MeanCWD的绝对路径”的组合。如果对cd的所有操作都在此绝对路径上起作用，则“ ..”始终可以在客户端上本地解析，而不是传输到文件系统服务器。例如，如果CWD为“ / foo / bar”，并且用户调用“ cd ..”，则基础调用可以转换为“ chdir / foo / bar / ..”，可以将其规范化为“ / foo” 。

