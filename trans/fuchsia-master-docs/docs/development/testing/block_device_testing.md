 
# Block device testing  块设备测试 

__WARNING: All of the following tests are destructive, and they may not ask for confirmation before executing. Run at your own risk.__ __警告：以下所有测试都是破坏性的，在执行之前它们可能不要求确认。运行风险自负。__

 
## Protocol testing  协议测试 

*blktest* is an integration which may be used to check adherence to the block protocol.  * blktest *是一个集成，可用于检查对块协议的遵守情况。

```shell
$ blktest -d /dev/class/block/000
```
 

 
## Filesystem testing  文件系统测试 

*fs-test* is a filesystem integration test suite that can be used to verify Fuchsia filesystem correctness on a filesystem. * fs-test *是文件系统集成测试套件，可用于验证文件系统上的Fuchsia文件系统正确性。

To avoid racing with the auto-mounter, it is recommended to run this test with the kernel command line option "zircon.system.disable-automount=true". 为了避免与自动安装程序竞争，建议使用内核命令行选项“ zircon.system.disable-automount = true”运行此测试。

TODO(ZX-1604): Ensure this filesystem test suite can execute on large partitions. It is currently recommended to use this test on a 1-2 GB GPTpartition on the block device. TODO（ZX-1604）：确保此文件系统测试套件可以在大型分区上执行。当前建议在块设备上的1-2 GB GPT分区上使用此测试。

```shell
$ /boot/test/fs/fs-test -d /dev/class/block/000 -f minfs
```
 

 
## Correctness testing  正确性测试 

*iochk* is a tool which pseudorandomly reads and writes to a block device to check for errors.  * iochk *是一种伪随机读取和写入块设备以检查错误的工具。

```shell
$ iochk -bs 32k -t 8 /dev/class/block/000
```
 

 
## Performance testing  性能测试 

*iotime* is a benchmarking tool which tests the read and write performance of block devices.  iotime *是一个基准测试工具，用于测试块设备的读写性能。

```shell
$ iotime read fifo /dev/class/block/000 64m 4k
```
 

 

