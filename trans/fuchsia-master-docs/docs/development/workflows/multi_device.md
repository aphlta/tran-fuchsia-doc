Multi Device Setup ============ 多设备设置============

This guide will walk you through the process of getting two Fuchsia devices set up and synchronizing story state using the[Ledger](/src/ledger/docs/). 本指南将引导您完成设置两个Fuchsia设备并使用[Ledger]（/ src / ledger / docs /）同步故事状态的过程。

 
## Setup  设定 

 
### Devices  设备 

Follow the steps at in the [top level docs](../README.md) to:  请按照[顶级文档]（../ README.md）中的步骤进行操作：

 
* Check out the source and build Fuchsia.  *查看源代码并构建紫红色。
* Install it on two devices (or emulators).  *将其安装在两个设备（或仿真器）上。
* Connect the devices to the network.  *将设备连接到网络。

 
### [Googlers only] Private Test Network Setup  [仅限Googlers]专用测试网络设置 

Follow netboot instructions.  按照netboot的说明进行操作。

 
### Identify Test Machines  识别测试机 

Each Fuchsia device has a unique node name based on its MAC address.  It is of the form `power-nerd-saved-santa`.  You can list the nodes on your network withthe `netls` command. 每个紫红色设备都基于其MAC地址具有唯一的节点名称。它的格式为“ power-nerd-saved-santa”。您可以使用“ netls”命令列出网络上的节点。

```
> netls
    device glad-bats-hunk-lady (fe80::f64d:30ff:fe68:2620/6)
    device blurt-chip-sugar-wish (fe80::8eae:4cff:feee:4f40/6)
```
 

 
### Running Commands On Test Machines  在测试机上运行命令 

The `netruncmd <nodename> <command>` command can be used to run commands on remote machines.  The output of the command is not shown.  If you need to seethe output, use the `loglistener [<nodename>]` command. netruncmd <nodename> <command>命令可用于在远程计算机上运行命令。该命令的输出未显示。如果需要查看输出，请使用loglistener [<nodename>]命令。

 
### Ledger Setup  分类帐设置 

Ledger is a distributed storage system for Fuchsia.  Stories use it to synchronize their state across multiple devices.  Follow the steps in Ledger's[User Guide](/src/ledger/docs/user_guide.md)to: Ledger是紫红色的分布式存储系统。故事使用它在多个设备之间同步其状态。请遵循Ledger的[用户指南]（/ src / ledger / docs / user_guide.md）中的步骤执行以下操作：

 
* Set up [persistent storage](/docs/concepts/filesystems/minfs.md). (optional)  *设置[永久存储]（/ docs / concepts / filesystems / minfs.md）。 （可选的）
* Verify the network is connected.  *确认网络已连接。
* Configure a Firebase instance.  *配置Firebase实例。
* Setup sync on each device using `configure_ledger`.  *使用`configure_ledger`在每个设备上设置同步。

 
## Run Stories  运行故事 

 
### Virtual consoles.  虚拟控制台。 

The systems boots up with three virtual consoles.  Alt-F1 through Alt-F3 can be used to switch between virtual consoles. 系统使用三个虚拟控制台启动。 Alt-F1至Alt-F3可用于在虚拟控制台之间切换。

 
### Wipe Data  抹掉数据 

The format of the Ledger as well as the format of the data each story syncs is under rapid development and no effort is currently made towards forwards andbackwards compatibility.  Because of this, after updating the Fuchsia code, itis a good idea to wipe your remote and local data using `cloud_sync clean`. 分类帐的格式以及每个故事同步的数据格式正在快速开发中，并且目前不进行任何向前和向后兼容性的工作。因此，在更新了Fuchsia代码后，使用“ cloud_sync clean”擦除远程和本地数据是一个好主意。

```
$ netruncmd <nodename> cloud_sync clean
```
 

 
### Start A Story On One Device  在一个设备上开始故事 

Use the `basemgr` to start a story on one device:  使用`basemgr`在一个设备上启动故事：

```
$ netruncmd <first-node-name> "basemgr --session_shell=dev_session_shell \
  --session_shell_args=--root_module=example_todo_story"
```
 

Using `loglistener <first-node-name>` take note of the story ID from a line the following: 使用`loglistener <first-node-name>`从以下一行记录故事ID：

```
... DevSessionShell Starting story with id: IM7U9hBcCt
```
 

 
### Open The Same Story On The Second Device.  在第二个设备上打开同一个故事。 

The story can be started on the second device either through the system UI or by specifying the story ID. 故事可以通过系统UI或通过指定故事ID在第二个设备上启动。

 
#### System UI, aka Session Shell, aka Armadillo  系统UI，又名Session Shell，又名ArmadilloLaunch the system UI using `basemgr`:  使用basemgr启动系统用户界面：

```
$ netruncmd <second-node-name> "basemgr"
```
 

Once the system UI starts, you should be able to see the story started in the step above.  Click on that to open it. 系统用户界面启动后，您应该可以看到上述步骤中启动的故事。点击打开它。

 
#### By Story ID  按故事ID 

With the story ID noted above from launch the story from a shell:  从外壳启动故事后，上面已经提到了故事ID：

```
$ netruncmd <second-node-name> "basemgr \
  --session_shell=dev_session_shell \
  --session_shell_args=--story_id=<story_id>
```
