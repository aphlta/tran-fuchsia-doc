 
# Fuchsia System Interface  紫红色系统接口 

 
## Overview  总览 

The *Fuchsia System Interface* is the binary interface that the Fuchsia operating system presents to software it runs. The foundation of the interfaceis the vDSO, which provides access to the system calls. Programs are not allowedto issue system calls directly (e.g., by trapping into the kernel). Instead,programs use the vDSO to interface with the kernel. * Fuchsia系统接口*是Fuchsia操作系统提供给它运行的软件的二进制接口。接口的基础是vDSO，它提供对系统调用的访问。不允许程序直接发出系统调用（例如，通过陷入内核）。相反，程序使用vDSO与内核进行接口。

The bulk of the system interface is provided through inter-process communication protocols, typically defined using FIDL. These protocols arespoken over various kernel primitives, including channels and sockets. 系统接口的大部分是通过进程间通信协议提供的，该协议通常使用FIDL定义。这些协议是通过各种内核原语（包括通道和套接字）发出的。

The `fuchsia.io` FIDL library provides protocols for file and directory operations. Fuchsia uses the `fuchsia.io` protocols to provide a namespace tocomponents through which components can access system services and resources.The names in these namespaces follow certain conventions, which are part of thesystem ABI. See [namespaces](/docs/concepts/framework/namespaces.md) for more details. fuchsia.io FIDL库提供文件和目录操作的协议。 Fuchsia使用`fuchsia.io`协议为组件提供名称空间，组件可以通过这些名称空间访问系统服务和资源。这些名称空间中的名称遵循某些约定，这些约定是系统ABI的一部分。有关更多详细信息，请参见[命名空间]（/ docs / concepts / framework / namespaces.md）。

Packages themselves also provide an interface to the system in terms of directory structure and file formats. The system uses this information toinitialize processes in which components stored in these packages execute. 程序包本身还提供目录结构和文件格式方面的系统接口。系统使用此信息初始化存储在这些程序包中的组件在其中执行的进程。

 
## Terminology  术语 

The *Application Programming Interface* (API) for a system is the source-level interface to the system. Developers typically write software that uses thisinterface directly. Changes to the system API might require developers to updatetheir source code to account for the changes to the API. 系统的* Application Programming Interface *（API）是系统的源代码级接口。开发人员通常编写直接使用此接口的软件。更改系统API可能需要开发人员更新其源代码，以解决API的更改。

The *Application Binary Interface* (ABI) for a system is the binary-level interface to the system. Developers do not typically write software that usesthis interface directly. Instead, they write software against the system API.Instead, when that software is compiled, the binary artifact created by thecompiler interfaces with the system through the system ABI. Changes to thesystem ABI might require the developer to recompile their source code to accountfor the changes to the ABI. 系统的“应用程序二进制接口”（ABI）是系统的二进制级别的接口。开发人员通常不编写直接使用此接口的软件。相反，他们根据系统API编写软件。相反，在编译该软件时，编译器创建的二进制工件通过系统ABI与系统连接。对系统ABI的更改可能需要开发人员重新编译其源代码，以解决对ABI的更改。

 
## ABI Surfaces  ABI表面 

This section describes the various ABI surfaces for Fuchsia components. The ABI for drivers is described in [drivers.md](drivers.md). 本节介绍了紫红色组件的各种ABI表面。用于驱动程序的ABI在[drivers.md]（drivers.md）中进行了描述。

 
### vDSO  vDSO 

The vDSO is a virtual shared library that provides access to the kernel. Concretely, the vDSO is an ELF shared library, called `libzircon.so`, thatexports a number of symbols with a C calling convention. The source of truth forthese symbols is [//zircon/syscalls](/zircon/syscalls/). Their semantics aredescribed in [the documentation](/docs/reference/syscalls/). vDSO是一个虚拟共享库，可提供对内核的访问。具体来说，vDSO是一个ELF共享库，名为“ libzircon.so”，它使用C调用约定导出许多符号。真实的这些符号的来源是[// zircon / syscalls]（/ zircon / syscalls /）。它们的语义在[文档]（/ docs / reference / syscalls /）中进行了描述。

Of particular importance are the semantics of the clocks defined by `libzircon.so`. The semantics of these clocks are described by[clock_get.md](/docs/reference/syscalls/clock_get.md#supported-clock-ids) 特别重要的是由libzircon.so定义的时钟的语义。这些时钟的语义由[clock_get.md]（/ docs / reference / syscalls / clock_get.mdsupported-clock-ids）描述

 
### FIDL protocols  FIDL协议 

The bulk of the system interfaces are defined in the Fuchsia Interface Definition Language (FIDL). The FIDL compiler produce language specific APIs andruntime libraries, referred to as FIDL bindings, for a variety of targetlanguages. These bindings provide an idiomatic interface for sending andreceiving interprocess communication messages over Zircon channels (and otherprimitives). 大部分系统接口均以紫红色接口定义语言（FIDL）定义。 FIDL编译器为各种目标语言生成特定于语言的API和运行时库，称为FIDL绑定。这些绑定提供了惯用的接口，用于通过Zircon通道（和其他基元）发送和接收进程间通信消息。

 
#### Wire format  电汇格式 

The FIDL protocol definitions themselves and the language-specific bindings generated by the compiler are part of the system *API* but not part of thesystem *ABI*. Instead, the format of the serialized messages, called the *wireformat*, comprises the ABI. The FIDL wire format is defined by the[specification](/docs/development/languages/fidl/reference/wire-format/README.md). FIDL协议定义本身以及由编译器生成的特定于语言的绑定是系统* API *的一部分，而不是系统* ABI *的一部分。取而代之的是，序列化消息的格式称为* wireformat *，由ABI组成。 FIDL线路格式由[规范]（/docs/development/languages/fidl/reference/wire-format/README.md）定义。

 
#### User signals  用户信号 

In addition to the messages sent, some FIDL protocols make use of user signals on the underlying kernel objects. Currently, these signals are not declared inFIDL. Typically, the semantics of any associated user signals are documentedin prose in comments in the FIDL definitions. 除了发送的消息外，某些FIDL协议还利用底层内核对象上的用户信号。当前，这些信号未在FIDL中声明。通常，任何关联的用户信号的语义都以散文形式记录在FIDL定义的注释中。

 
### Namespace conventions  命名空间约定 

When run, components are given an *incoming namespace* and serve an *outgoing directory*. The names in the incoming namespace and outgoing directory followcertain conventions, which are are part of the system ABI. 运行时，组件将获得一个“传入名称空间”，并作为一个“外发目录”。传入名称空间和传出目录中的名称遵循某些约定，它们是系统ABI的一部分。

 
#### Incoming namespace  传入名称空间 

A component's incoming namespace is provided to a component during startup and lets the component interact with the rest of the system. The names in thenamespace follow certain conventions. Many of the namespace entries provideaccess to well-known protocols, most of which are defined by FIDL. For example,the component can access services through the `svc` entry in this namespace,which conventionally contains services listed by their fully qualified discoveryname. Similarly, by convention, the `pkg` entry in this namespace is mapped tothe package from which the component was run. 组件的传入名称空间在启动过程中提供给组件，并使组件与系统的其余部分进行交互。命名空间中的名称遵循某些约定。许多名称空间条目提供对众所周知协议的访问，其中大多数协议是由FIDL定义的。例如，组件可以通过此命名空间中的“ svc”条目访问服务，该条目通常包含按其完全限定的发现名称列出的服务。类似地，按照约定，此命名空间中的`pkg`条目映射到运行组件的包。

 
#### Outgoing directory {#outgoing_directory}  寄出目录{outgoing_directory} 

A component can serve an outgoing directory that lets the system and other components interact with the component. For example, the component exposesservices for other components using the `public` entry in this namespace.Similarly, the component exposes debugging interfaces through the `debug` entryin this namespace. 组件可以服务于传出目录，该目录允许系统和其他组件与该组件进行交互。例如，该组件使用此命名空间中的public条目公开其他组件的服务。类似地，该组件通过该命名空间中的debug条目公开调试接口。

 
#### Data formats  资料格式 

In addition to services, some namespaces include files with data. The data format used by these files is also part of the system ABI. For example,components access the root certificates through a namespace entry that containsa `certs.pem` file. The `pem` data format is therefore part of the system ABI. 除服务外，某些名称空间还包含带有数据的文件。这些文件使用的数据格式也是系统ABI的一部分。例如，组件通过包含“ certs.pem”文件的名称空间条目访问根证书。因此，“ pem”数据格式是系统ABI的一部分。

 
### Package conventions  包装约定 

Fuchsia packages have a directory structure that follows certain naming conventions. These conventions are also part of the system ABI. This sectiongives two examples of important packaging conventions. 紫红色的软件包具有遵循某些命名约定的目录结构。这些约定也是系统ABI的一部分。本节给出了重要包装约定的两个示例。

 
#### meta  元 

By convention, the `meta` directory in a package contains metadata files that describe the package. The structure of this metadata, include the data formatsused by these files, are part of the system ABI. 按照约定，包中的“ meta”目录包含描述包的元数据文件。此元数据的结构（包括这些文件使用的数据格式）是系统ABI的一部分。

 
#### lib  LIB 

By convention, the `lib` directory in a package contains the shared libraries used by components in the package. When the system runs an executable from thepackage, requests for shared libraries are resolved relative to this `lib`directory. 按照约定，软件包中的`lib`目录包含软件包中组件所使用的共享库。当系统从程序包运行可执行文件时，相对于此lib目录的共享库请求将得到解决。

One important difference between Fuchsia and other operating systems is that the shared libraries themselves are provided by the package creator rather than thesystem itself. For that reason, the shared libraries themselves (including`libc`) are not part of the system ABI. Fuchsia与其他操作系统之间的一个重要区别是共享库本身是由程序包创建者而不是系统本身提供的。因此，共享库本身（包括libc）不是系统ABI的一部分。

The system does provide two shared libraries: the [vDSO](#vdso) and the [Vulkan ICD](#vulkan-icd). See those sections for details. 该系统确实提供了两个共享库：[vDSO]（vdso）和[Vulkan ICD]（vulkan-icd）。有关详细信息，请参见这些部分。

 
### Process structure  工艺结构 

Processes on Fuchsia are fairly flexible and largely under the control of the executable running in the process, but some of the initial structure of theprocess is controlled by the system and part of the system ABI. 紫红色的流程相当灵活，并且很大程度上受流程中运行的可执行文件的控制，但是流程的某些初始结构由系统和系统ABI的一部分控制。

For additional details, see [Program Loading](/docs/concepts/booting/program_loading.md). 有关更多详细信息，请参见[程序加载]（/ docs / concepts / booting / program_loading.md）。

 
#### ELF loader  ELF装载机 

Fuchsia uses the ELF data format for executables. When loading an executable into a process, the loader parses contents of the executable as ELF. The loaderreads the `INTERP` directive from the executable and resolves that name as afile in the `lib` directory of the package that contained the executable. Theloader then parses the contents of the `INTERP` file as an ELF shared library,relocates the library, and maps the library into the newly created process. 紫红色将ELF数据格式用于可执行文件。将可执行文件加载到进程中时，加载程序将可执行文件的内容解析为ELF。加载程序从可执行文件中读取“ INTERP”指令，并将该名称解析为包含可执行文件的软件包的“ lib”目录中的文件。然后，加载程序将“ INTERP”文件的内容解析为ELF共享库，重新定位该库，并将该库映射到新创建的进程中。

 
#### Startup message  启动讯息 

As part of starting a process, the creator of the process supplies the process with a message that contains, for example, the command line arguments, the`environ`, the initial handles, and the incoming namespace for the process.(The outgoing directory is included in the set of initial handles for theprocess.) 作为启动过程的一部分，过程的创建者向过程提供一条消息，该消息包含例如命令行参数，环境，初始句柄以及过程的传入名称空间。（传出目录包含在该过程的初始句柄集合中。）

The format of this message, including length limitations on fields such as the command line arguments and the `environ`, are part of the system ABI, as arethe conventions around the contents of the message. For example, by convention,the `PWD` environment variable is the name the creator suggests the process useas its current working directory. 该消息的格式（包括命令行参数和“ environ”之类的字段的长度限制）是系统ABI的一部分，它也是围绕消息内容的约定。例如，按照约定，`PWD`环境变量是创建者建议该进程用作其当前工作目录的名称。

The initial handles are associated with numerical identifiers. The conventions around these identifiers are part of the system ABI. For example, by convention,the `PA_PROC_SELF` handle is a handle to the process object for the newlycreated process. In addition to the types of these handles, the rightsassociated with these handles are also part of the system ABI. 初始句柄与数字标识符关联。这些标识符周围的约定是系统ABI的一部分。例如，按照约定，`PA_PROC_SELF`句柄是新创建的过程的过程对象的句柄。除了这些句柄的类型之外，与这些句柄关联的权限也是系统ABI的一部分。

 
#### VMAR structure  VMAR结构 

Before starting a process, the creator modifies the root VMAR for the process. For example, the creator maps the vDSO and allocates a stack for the initialthread. The structure of the VMAR when the process is started is part of thesystem ABI. 在开始过程之前，创建者会修改过程的根VMAR。例如，创建者映射vDSO并为初始线程分配堆栈。启动过程时，VMAR的结构是系统ABI的一部分。

 
#### Job policy  工作方针 

Processes are run in jobs, which can apply policy to the processes and jobs they contain. The job policy applied to processes is part of the system ABI. Forexample, components run in processes with `ZX_POL_NEW_PROCESS` set to`ZX_POL_ACTION_DENY`, which forces components to use the`fuchsia.process.Launcher` service to create processes rather than issuing the`zx_process_create` system call directly. 流程在作业中运行，可以将策略应用于其包含的流程和作业。应用于流程的作业策略是系统ABI的一部分。例如，组件在将“ ZX_POL_NEW_PROCESS”设置为“ ZX_POL_ACTION_DENY”的进程中运行，这迫使组件使用“ fuchsia.process.Launcher”服务创建进程，而不是直接发出“ zx_process_create”系统调用。

 
### Vulkan ICD  Vulkan ICD 

Components that use the Vulkan API for hardware accelerated graphics link against `libvulkan.so` and specify the `vulkan` feature in their manifests. Thislibrary is provided by the package that contains the component and therefore isnot part of the system ABI. However, `libvulkan.so` loads another sharedlibrary, called the *Vulkan Installable Client Driver* (Vulkan ICD). The VulkanICD is loaded using `fuchsia.vulkan.loader.Loader`, which means the library isprovided by the system itself rather than the package that contains thecomponent. For this reason, the Vulkan ICD is part of the system ABI. 使用Vulkan API进行硬件加速的图形的组件链接到`libvulkan.so`，并在其清单中指定`vulkan`功能。该库由包含组件的软件包提供，因此不属于系统ABI。但是，`libvulkan.so`会加载另一个共享库，称为* Vulkan可安装客户端驱动程序*（Vulkan ICD）。 VulkanICD使用`fuchsia.vulkan.loader.Loader`加载，这意味着该库由系统本身而非包含组件的软件包提供。因此，Vulkan ICD是系统ABI的一部分。

The Vulkan ICD is an ELF shared library that exports exactly two symbols. These symbols are reserved for use by the Vulkan ICD and should not be used directly. Vulkan ICD是一个ELF共享库，可精确导出两个符号。这些符号保留供Vulkan ICD使用，不应直接使用。

 
 * `vk_icdGetInstanceProcAddr`  *`vk_icdGetInstanceProcAddr`
 * `vk_icdNegotiateLoaderICDInterfaceVersion`  *`vk_icdNegotiateLoaderICDInterfaceVersion`

In addition, the Vulkan ICD shared library has a `NEEDED` section that lists several shared libraries upon which the Vulkan ICD depends. The packagecontaining the component is required to provide these shared libraries. 另外，Vulkan ICD共享库有一个“ NEEDED”部分，其中列出了Vulkan ICD所依赖的几个共享库。需要包含组件的软件包来提供这些共享库。

The Vulkan ICD also imports a number of symbols. The conventions around these imported symbols, for example their parameters and semantics, are part of thesystem ABI. Vulkan ICD还导入许多符号。这些导入符号周围的约定（例如，它们的参数和语义）是系统ABI的一部分。

Currently, the `NEEDED` section and the list of imported symbols for the Vulkan ICD are both larger than we desire. Hopefully we will be able to minimize theseaspects of the system ABI. 当前，“ Vulkan ICD”的“ NEEDED”部分和导入的符号列表都比我们期望的要大。希望我们将能够最小化系统ABI的这些方面。

 
### Sockets  插座 

 
#### Datagram framing  数据报成帧 

Datagram sockets used for networking include a frame that specifies the network address associated with the datagram. This frame is also part of the system ABI. 用于联网的数据报套接字包括一个框架，该框架指定与数据报关联的网络地址。该框架也是系统ABI的一部分。

 
### Terminal protocol  终端协议 
