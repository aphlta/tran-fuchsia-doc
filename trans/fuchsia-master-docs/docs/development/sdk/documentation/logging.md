 
# Logging  记录中 

The preferred way to publish logs is to use the `syslog` API, currently available for C in `//pkg/syslog`. 最好的发布日志的方法是使用`syslog` API，该API当前可用于`// pkg / syslog`中的C语言。

The library provides the ability to tag logs so that they can later be filtered upon retrieval. 该库提供了标记日志的功能，以便以后可以在检索时对其进行过滤。

```
$ log_listener
```
In order to get logs from a device, open a shell on the device as described in [this document](ssh.md) and run: 为了从设备获取日志，请按照[本文档]（ssh.md）中所述打开设备上的外壳并运行：

```
$ log_listener --tag foobar
```
To view specifics logs, add a tag specification:  要查看特定日志，请添加标签规范：

 
## Symbolization  符号化 

```
tools/symbolize --build-id-dir .build-id
```
