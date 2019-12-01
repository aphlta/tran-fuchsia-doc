 
# SSH  SSH协议 

SSH is the supported protocol for communication between a Fuchsia target device and a host device.This document describes how to properly set up an SSH connection between thesedevices. SSH是Fuchsia目标设备与主机设备之间通信的受支持协议。本文档介绍了如何在这些设备之间正确建立SSH连接。

 
## Prerequisites  先决条件 

On the host side, a proper SSH distribution is required.  在主机端，需要正确的SSH分发。

A public/private keypair is also needed. It may be generated via the `ssh-keygen` command, or extracted from the runningSSH agent via `ssh-add -L`. 还需要一个公共/私有密钥对。它可以通过ssh-keygen命令生成，也可以通过ssh-add -L从正在运行的SSH代理中提取。

 
## Provisioning a device  调配设备 

There are two options for installing the public key onto the target.  有两个选项可将公钥安装到目标上。

 
### By installing it during paving (preferred)  通过在铺路过程中安装（首选） 

```
$ bootserver --authorized-keys $PUBLIC_KEY <other args>
```
Follow the instruction for [paving](bootserver.md) the target device, and add an extra argument to the `bootserver` call pointing to the public key: 请遵循[paving]（bootserver.md）目标设备的说明，并在指向公用密钥的`bootserver`调用中添加一个额外的参数：

 
### By modifying the Fuchsia image directly  通过直接修改紫红色图像 

```
$ zbi -o $FUCHSIA_DOT_ZBI -e data/ssh/authorized_keys=$PUBLIC_KEY
```
The `fuchsia.zbi` image may be modified to include the public key using the `zbi` tool: 可以使用`zbi`工具将`fuchsia.zbi`图像修改为包括公共密钥：

Note that this method is mainly designed for situations where paving is not necessarily an efficient option (e.g. testing on an emulator).Use with care. 请注意，此方法主要设计用于铺路不一定是有效选择的情况（例如在仿真器上进行测试）。

 
## Connecting to a device  连接到设备 

```
$ ssh -i $PRIVATE_KEY fuchsia@$TARGET_ADDRESS
```
Provided that the address of the target device is known as `$TARGET_ADDRESS`, open a shell on that device with: 假设目标设备的地址为$ TARGET_ADDRESS，请使用以下命令在该设备上打开外壳：

Note that if you got the key from your SSH agent, or if the key is in a well known location (`$SSH_HOME`) under a well known name (`id_*`), you may omit the`-i` argument. 请注意，如果您从SSH代理那里获得了密钥，或者该密钥位于一个众所周知的名称（`id_ *`）下的一个众所周知的位置（$ SSH_HOME）中，则可以省略-i参数。

```
-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null
```
