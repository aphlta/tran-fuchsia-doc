 
# Nand testing  Nand测试 

*** note __WARNING:__ Most of these tests are destructive in nature.*** ***注意__警告：__这些测试大多数都是破坏性的。***

 
## Accessing the desired device  访问所需的设备 

In order to test a particular device, that device must not be in use by the rest of the system. There are two ways to make that happen: 为了测试特定的设备，系统的其余部分不得使用该设备。有两种方法可以实现这一目标：

 
* Prevent other drivers from binding to the device. This may involve building the system with modified binding rules for the driver that normally bindsto the desired device, or passing kernel command line arguments to disablethat driver. *防止其他驱动程序绑定到设备。这可能涉及使用通常会绑定到所需设备的驱动程序修改后的绑定规则来构建系统，或者传递内核命令行参数以禁用该驱动程序。

 
* Unbind devices that are bound to the desired device.  *取消绑定到所需设备的设备。

For example, in order to use a test tool against the core nand driver, nandpart devices may be removed like so: 例如，为了对核心nand驱动程序使用测试工具，可以这样删除nandpart设备：

```shell
$ unbind /dev/sys/platform/05:00:f/aml-raw_nand/nand/fvm
```
 

*** note __WARNING:__ Before removing a particular device, remove its descendants. Byextension, file systems must be unmounted before a block device is removed.Note that this requirement is likely to render a running system unusable, asthe backing for the OS may be going away. Netboot may be the only viable option.*** ***注意__警告：__卸下特定设备之前，请卸下其后代。通过扩展名，必须先卸载文件系统，然后再删除块设备。请注意，此要求可能会导致正在运行的系统无法使用，因为操作系统的支持可能会消失。 Netboot可能是唯一可行的选择。***

Note that all other devices created by nandpart must also be removed. Use `dm dump` to inspect the device tree. 请注意，还必须删除nandpart创建的所有其他设备。使用`dm dump`检查设备树。

 
## Protocol testing  协议测试 

*nand-test* is an integration test which performs basic tests of nand protocol drivers. * nand-test *是一个集成测试，它执行nand协议驱动程序的基本测试。

For example, this command will test an existing ram-nand device making sure the test does not modify anything outside blocks [100, 109]: 例如，此命令将测试现有的ram-nand设备，以确保测试不会修改块[100，109]之外的任何内容：

```shell
$ /boot/test/sys/nand-test --device /dev/misc/nand-ctl/ram-nand-0 --first-block 100 --num-blocks 10
```
 

 
## Correctness testing  正确性测试 

*nand-util* is a troubleshooting tool that can perform a simple read-reliability test. * nand-util *是一种故障排除工具，可以执行简单的读取可靠性测试。

```shell
$ nand-util --device /dev/misc/nand-ctl/ram-nand-0 --check
```
 

 
## Inspection / manipulation  检查/操作 

```shell
$ nand-util --device /dev/sys/platform/05:00:f/aml-raw_nand/nand --info
$ nand-util --device /dev/sys/platform/05:00:f/aml-raw_nand/nand/fvm --read --block 1 --page 2
```
 

 
## Grab an image  抓取图像 

*nand-util* can also be used to grab an image of the nand contents:  * nand-util *也可以用于获取nand内容的图像：

*** note If a file system is already mounted, unbind will fail, and forcing it to work islikely to render the system unusable. Rememer to netboot or use Zedboot asneeded.*** ***注意如果已安装文件系统，则解除绑定将失败，并且强制其工作可能会使系统无法使用。请记住需要netboot或使用Zedboot。***

```shell
$ unbind /dev/sys/platform/05:00:f/aml-raw_nand/nand/fvm/ftl/block
$ unbind /dev/sys/platform/05:00:f/aml-raw_nand/nand/fvm/ftl
$ nand-util --device /dev/sys/platform/05:00:f/aml-raw_nand/nand/fvm --save --file /tmp/image
```
 

Transfer the image file to the host:  将映像文件传输到主机：

```shell
$ zircon/build-gcc/tools/netcp :/tmp/image /tmp/saved_image_file
```
 

 
## Replay  重播 

A saved nand image can be loaded on top of a ram-nand device using nand-loader.  可以使用nand-loader将保存的nand图像加载到ram-nand设备的顶部。

First, transfer the image to a device running Zircon. For example, on the host:  首先，将映像传输到运行Zircon的设备。例如，在主机上：

```shell
echo /nand.dmp=/tmp/saved_image_file > /tmp/manifest.txt
zircon/build-gcc/tools/minfs /tmp/image.dsk create --manifest /tmp/manifest.txt
fx set bringup.x64
fx build
fx qemu -k -- -hda /tmp/image.dsk
```
 

Then, inside zircon:  然后，在锆石中：

```shell
$ mkdir data/a
$ mount /dev/class/block/000 data/a
$ nand-loader data/a/nand.dmp
```
