Fuchsia Boot Sequence ===================== 紫红色引导顺序=====================

This document describes the boot sequence for Fuchsia from the time the Zircon layer hands control over to the Garnet layer.  This document is a work inprogress that will need to be extended as we bring up more of the system. 本文档介绍了从Zircon层移交给Garnet层以来紫红色的启动顺序。本文档是一项正在进行的工作，随着我们提出更多的系统，需要对此进行扩展。

 
# Layer 1: [appmgr](/src/sys/appmgr)  第1层：[appmgr]（/ src / sys / appmgr） 

`appmgr`'s job is to host the environment tree and help create processes in these environments.  Processes created by `appmgr`have an `zx::channel` back to their environment, which lets them create otherprocesses in their environment and to create nested environments. appmgr的工作是托管环境树并帮助在这些环境中创建进程。由appmgr创建的进程具有返回其环境的zx :: channel，这使他们可以在其环境中创建其他进程并创建嵌套环境。

At startup, `appmgr` creates an empty root environment and creates the initial apps listed in `/system/data/appmgr/initial.config` inthat environment. Typically, these applications create environments nesteddirectly in the root environment. The default configuration contains one initialapp: `bootstrap`. 在启动时，“ appmgr”会创建一个空的根环境，并在该环境中创建“ /system/data/appmgr/initial.config”中列出的初始应用。通常，这些应用程序创建直接嵌套在根环境中的环境。默认配置包含一个initialapp：`bootstrap`。

 
# Layer 2: [sysmgr](/src/sys/sysmgr/)  第2层：[sysmgr]（/ src / sys / sysmgr /） 

`sysmgr`'s job is to create the boot environment and create a number of initial components in the boot environment. sysmgr的工作是创建引导环境并在引导环境中创建许多初始组件。

The services that `sysmgr` offers in the boot environment are not provided by bootstrap itself. Instead, when `sysmgr` receives a request for a service forthe first time, `sysmgr` lazily creates the appropriate app to implement thatservice and routes the request to that app. The table of which componentsimplement which services is contained in the`/system/data/bootstrap/services.config` file. Subsequent requests for the sameservice are routed to the already running app. If the app terminates,`sysmgr` will start it again the next time it receives a request for aservice implemented by that app. 引导程序本身不提供sysmgr在引导环境中提供的服务。取而代之的是，当sysmgr第一次收到服务请求时，sysmgr会懒惰地创建适当的应用程序来实现该服务并将请求路由到该应用程序。哪个组件实现了哪些服务的表包含在/system/data/bootstrap/services.config文件中。随后对相同服务的请求将路由到已经运行的应用程序。如果该应用程序终止，则sysmgr将在下次收到该应用程序实施的服务请求时再次启动它。

`sysmgr` also runs a number of components in the boot environment at startup. The list of components to run at startup is contained in the`/system/data/bootstrap/apps.config` file. `sysmgr`在启动时还在引导环境中运行许多组件。在启动时要运行的组件列表包含在/system/data/bootstrap/apps.config文件中。

 
# Layer 3: [basemgr](/src/modular/bin/basemgr/)  第3层：[basemgr]（/ src / modular / bin / basemgr /） 

`basemgr`'s job is to setup the interactive flow for user login and user management. basemgr的工作是为用户登录和用户管理设置交互式流程。

It first gets access to the root view of the system, starts up Device Shell and draws the Device Shell UI in the root view starting the interactive flow. It alsomanages a user database that is exposed to Device Shell via the User ProviderFIDL API. 它首先获得对系统根视图的访问权，启动Device Shell，并在根视图中绘制Device Shell UI，以启动交互流程。它还管理通过用户提供程序FIDL API向设备外壳公开的用户数据库。

This API allows the Device Shell to add a new user, delete an existing user, enumerate all existing users and login as an existing user or in incognito mode. 该API允许Device Shell添加新用户，删除现有用户，枚举所有现有用户并以现有用户身份或隐身模式登录。

Adding a new user is done using an Account Manager service that can talk to an identity provider to get an id token to access the user's[Ledger](/src/ledger/bin/). 使用帐户管理器服务可以添加新用户，该服务可以与身份提供者进行对话以获取ID令牌以访问用户的[Ledger]（/ src / ledger / bin /）。

Logging-in as an existing user starts an instance of `sessionmgr` with that user's id token and with a namespace that is mapped within and managed by`basemgr`'s namespace. 以现有用户身份登录时，将使用该用户的ID令牌和名称空间（由basemgr名称空间映射并由其管理）来启动“ sessionmgr”实例。

