 
# Process Creation  流程创建 

The kernel provides low-level facilities for creating and setting up processes. However, these facilities are difficult to use because they involve directlymapping memory for executables, shared libraries, and stacks. Instead, you shoulduse one of the higher-level mechanisms for creating processes. 内核提供了用于创建和设置进程的低级功能。但是，这些工具很难使用，因为它们涉及直接为可执行文件，共享库和堆栈映射内存。相反，您应该使用更高级别的机制之一来创建流程。

 
## fuchsia.process.Launcher  紫红色工艺 

Fuchsia provides a service, `fuchsia.process.Launcher`, that does the low-level work of constructing processes for you. You provide this service with all thekernel objects needed to construct the process (e.g., the job object in whichthe process should be created, the executable image, and the standard input andoutput handles), and the service does the work of parsing the ELF executableformat, configuring the address space for the process, and sending the processthe startup message. 紫红色提供了一个名为“ fuchsia.process.Launcher”的服务，该服务为您完成了构建流程的底层工作。您向该服务提供构造流程所需的所有内核对象（例如，应在其中创建流程的作业对象，可执行文件映像以及标准的输入和输出句柄），并且该服务将执行ELF可执行文件格式的解析工作，配置进程的地址空间，并向进程发送启动消息。

Most clients do not need to use this service directly. Instead, most clients can use the simple C frontend in the FDIO library called `fdio_spawn`. Thisfunction, and its more advanced `fdio_spawn_etc` and `fdio_spawn_vmo`companions, connect to the `fuchsia.process.Launcher` service and send theservice the appropriate messages to create the process.  The`fdio_spawn_action_t` array passed to `fdio_spawn_etc` can be used to customizethe created process. 大多数客户不需要直接使用此服务。相反，大多数客户端可以使用FDIO库中名为fdio_spawn的简单C前端。该功能及其更高级的fdio_spawn_etc和fdio_spawn_vmo伴侣连接到fuchsia.process.Launcher服务，并向该服务发送适当的消息以创建过程。传递给fdio_spawn_etc的fdio_spawn_action_t数组可用于自定义创建的过程。

Regardless of whether you use the `fuchsia.process.Launcher` service directly or the `fdio_spawn` frontend, this approach to creating processes is mostappropriate for creating processes within your own namespace because you needto supply all the kernel objects for the new process. 无论是直接使用fuchsia.process.Launcher服务还是使用fdio_spawn前端，这种创建进程的方法最适合在自己的命名空间中创建进程，因为您需要为新进程提供所有内核对象。

 
## fuchsia.sys.Launcher  紫红色的启动器 

To create a process in its own namespace, Fuchsia provides the `fuchsia.sys.Launcher` service. Rather than providing this process all thekernel objects needed to construct the new process, you simply provide theservice a high-level description of the process you wish to create and the`fuchsia.sys.Launcher` implementation supplies the new process with theappropriate kernel objects. For example, if you provide the URL of a componentwithin a package, `fuchsia.sys.Launcher` will create a process for thatcomponent in a namespace appropriate for that component with access to its ownpackage and whatever other resources are declared in the `sandbox` section ofits manifest. 为了在自己的名称空间中创建进程，Fuchsia提供了“ fuchsia.sys.Launcher”服务。无需向该进程提供构建新进程所需的所有内核对象，而是仅向服务提供要创建的进程的高级描述，而fuchsia.sys.Launcher的实现为新进程提供适当的内核对象。例如，如果在包中提供组件的URL，`fuchsia.sys.Launcher`将在适合该组件的名称空间中为该组件创建一个进程，该进程可以访问其自己的包以及在`sandbox'中声明的任何其他资源。它的清单部分。

Rather than returning a `zx::process` handle directly, `fuchsia.sys.Launcher` returns a `fuchsia.sys.ComponentController` interface. This layer ofabstraction lets `fuchsia.sys.Launcher` create components that are not backedby individual processes. For example, if you launch a component written inDart, the component might run in an instance of the Dart VM that is sharedbetween a number of components with compatible security constraints. 不是直接返回`zx :: process`句柄，而是`fuchsia.sys.Launcher`返回一个`fuchsia.sys.ComponentController`接口。这层抽象使`fuchsia.sys.Launcher`创建不受单个进程支持的组件。例如，如果启动用Dart编写的组件，则该组件可能在Dart VM的实例中运行，该实例在具有兼容安全性约束的多个组件之间共享。

 
## Early boot  早期启动 

Early on in the boot process, the system does create a number of processes manually. For example, the kernel manually creates the first userspace process,`userboot`, which creates `devmgr` in turn. These low-level mechanisms use the`liblaunchpad.so` shared library, which contains the logic for parsing ELFfiles. Direct construction of processes is prohibited in the `fuchsia` job treeusing a job policy. 在启动过程的早期，系统确实会手动创建许多过程。例如，内核手动创建第一个用户空间进程“ userboot”，该进程依次创建“ devmgr”。这些低级机制使用liblaunchpad.so共享库，其中包含用于解析ELF文件的逻辑。在“紫红色”作业树中，禁止使用作业策略直接构建流程。

