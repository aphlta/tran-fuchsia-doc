 
# Fuchsia Tracing Usage Guide  紫红色追踪用法指南 

 
## Operational Requirements  操作要求 

Fuchsia tracing library and utilities require access to the `trace_manager`'s services in the environment, which is typically set up by the[boot sequence](/docs/concepts/framework/boot_sequence.md). 紫红色的跟踪库和实用程序需要访问环境中的`trace_manager`服务，该服务通常由[启动顺序]（/ docs / concepts / framework / boot_sequence.md）设置。

Note that capturing traces requires that the `devtools` package be included. If your build configuration does not include `devtools` by default, then you can add it manually by invoking`fx set` like: 请注意，捕获跟踪要求包含`devtools`软件包。如果您的构建配置默认不包含`devtools`，那么您可以通过调用`fx set`来手动添加它，例如：

```{shell}
fx set PRODUCT.BOARD --with-base='//garnet/packages/products:devtools'
```
 

So as a full example:  因此，举一个完整的例子：

```{shell}
fx set core.x64 --release --with-base=//garnet/packages/products:devtools,//peridot/packages/prod:sessionctl'
```
 

 
## Capturing Traces From a Development Host  从开发主机捕获跟踪 

Traces are captured using the `fx traceutil` host utility. To record a trace simply run the following on your development host: 使用`fx traceutil`主机实用程序捕获跟踪。要记录跟踪，只需在开发主机上运行以下命令：

```{shell}
fx traceutil record [program arg1 ...]
```
 

`fx traceutil record` will:  `fx traceutil record`将：

 
 * Take a trace on the target using the default options.  *使用默认选项在目标上进行跟踪。
 * Download it from the target to your development host.  *将其从目标下载到您的开发主机。
 * Convert the trace into a viewable HTML file.  *将跟踪转换为可见的HTML文件。

If a program is specified it will be run after tracing has started to not miss any early trace events in the program. 如果指定了程序，它将在跟踪开始后运行，以确保不会错过程序中的任何早期跟踪事件。

This is a great place to start an investigation. It is also a good when you are reporting a bug and are unsure what data is useful. 这是开始调查的好地方。当您报告错误并且不确定哪些数据有用时，这也是一个好方法。

Some additional command line arguments to `fx traceutil record` include:  fx traceutil record的一些其他命令行参数包括：

 
 * `-duration <time>`  *`-duration <time>`

   Sets the duration of the trace in seconds.  设置跟踪的持续时间（以秒为单位）。

 
 * `-target <hostname or ip address>`  *`-target <主机名或IP地址>`

   Specifies which target to take a trace. Useful if you have multiple targets on the same network or network discovery is not working. 指定要跟踪的目标。如果您在同一网络上有多个目标，或者网络发现不起作用，则很有用。

 
 * `-binary`  *`-binary`

   Captures the trace in Fuchsia trace format on the target and performs the conversion to JSON on the host. Defaults to true, use`-binary=false` to force the conversion to happen on the target.This flag is planned to be removed once all workflows have been tested to beworking with host-side conversion. 在目标上以Fuchsia跟踪格式捕获跟踪，并在主机上执行到JSON的转换。默认为true，使用`-binary = false`强制转换发生在目标上。一旦所有工作流都经过测试可以与主机端转换一起使用，则计划删除此标志。

 
 * `-stream`  *`-stream`

   Stream the trace output straight from the target to the host without saving the file on the target first. 将跟踪输出直接从目标流传输到主机，而无需先将文件保存在目标上。

 
 * `-compress`  *-压缩

   Compress the output stream. This is useful when saving to a small or slow local disk. If both `-stream` and `-compress` are provided, `-compress`is ignored. 压缩输出流。当保存到较小或较慢的本地磁盘时，此功能很有用。如果同时提供了-stream和-compress，则忽略-compress。

 
 * `-decouple`  *`-decouple`

   Don't stop tracing when the traced program exits. This is only valid when `program` is provided. 退出的程序退出时不要停止跟踪。仅在提供“程序”时有效。

 
 * `-detach`  *`-detach`

   Don't stop the traced program when tracing finishes. This is only valid when `program` is provided. 跟踪完成时不要停止跟踪的程序。仅在提供“程序”时有效。

 
 * `-spawn`  *`-spawn`

   Use `fdio_spawn` to run a legacy app. `-detach` will have no effect when using this option.This is only valid when `program` is provided. 使用`fdio_spawn`运行旧版应用程序。使用此选项时，-detach无效。仅在提供program时有效。

For a complete list of command line arguments run `fx traceutil record --help`.  要获取命令行参数的完整列表，请运行fx traceutil record --help。

 
## Capturing Traces From a Fuchsia Target  从紫红色的目标捕获痕迹 

Under the hood `traceutil` uses the `trace` utility on the Fuchsia target to interact with the tracing manager. To record a trace run thefollowing in a shell on your target: 在幕后，`traceutil`在紫红色的目标上使用`trace`实用程序与跟踪管理器进行交互。要记录跟踪，请在目标上的shell中执行以下操作：

```{shell}
trace record
```
 

This will save your trace in /data/trace.json by default. For more information, run `trace --help` at a Fuchsia shell. 默认情况下，这会将您的跟踪保存在/data/trace.json中。有关更多信息，请在紫红色的shell上运行`trace --help`。

 
## Viewing and Converting Between Trace Formats  在跟踪格式之间查看和转换 

There are three trace file formats that can store Fuchsia trace data.  可以存储紫红色跟踪数据的三种跟踪文件格式。

 
 * FXT, or [Fuchsia Trace Format](trace-format/README.md), is a binary format that is a direct encoding of the original trace data that is produced bythe various programs. To visualize this data, you can use the[Perfetto Trace Viewer](https://ui.perfetto.dev), which also allows you to[use SQL to query your tracedata](https://www.perfetto.dev/#/trace-processor.md). * FXT或[Fuchsia跟踪格式]（trace-format / README.md）是一种二进制格式，直接编码由各种程序产生的原始跟踪数据。要可视化此数据，可以使用[Perfetto Trace Viewer]（https://ui.perfetto.dev），它还可以[使用SQL查询您的跟踪数据]（https://www.perfetto.dev/ /trace-processor.md）。
 * JSON, or [Chrome Trace Format](https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU/edit).To visualize this data, you can use Chromium's[Trace-Viewer](https://github.com/catapult-project/catapult/tree/master/tracing). * JSON或[Chrome跟踪格式]（https://docs.google.com/document/d/1CvAClvFfyA5R-PhYUmn5OOQtYMH4h6I0nSsKchNAySU/edit）。要形象化此数据，可以使用Chromium的[Trace-Viewer]（https：// github.com/catapult-project/catapult/tree/master/tracing）。
 * HTML, a standalone file that includes both the viewer and trace data. To visualize this data, you can use a web browser such as[Chrome](https://google.com/chrome). * HTML，一个包含查看器和跟踪数据的独立文件。要形象化这些数据，可以使用网络浏览器，例如[Chrome]（https://google.com/chrome）。

You can convert one or more files from FXT to JSON, and then to HTML by running  您可以通过运行以下命令将一个或多个文件从FXT转换为JSON，然后转换为HTML

```{shell}
fx traceutil convert FILE ...
```
 

When you convert files with `fx traceutil convert`,  当您使用`fx traceutil convert`转换文件时，

 
 * FXT files produce a corresponding JSON file and a corresponding HTML file.  * FXT文件产生相应的JSON文件和相应的HTML文件。
 * JSON files produce a corresponding HTML file.  * JSON文件产生相应的HTML文件。

Note: If you record your trace with `fx traceutil record`, this conversion is done automatically. 注意：如果使用`fx traceutil record`记录跟踪，则此转换将自动完成。

 
## Advanced Tracing  进阶追踪 

 
### Tracing specification file  跟踪规范文件 

Tracing specification file is a JSON file that can be passed to `trace record` in order to configure parameters of tracing. For those parameters that can bepassed both on the command line and set in the specification file, the commandline value overrides the one from the file. 跟踪规范文件是一个JSON文件，可以将其传递给“跟踪记录”以配置跟踪参数。对于既可以在命令行上传递又可以在规范文件中设置的那些参数，命令行值将覆盖文件中的一个。

The file supports the following top level-parameters:  该文件支持以下顶级参数：

 
 - `app`: string, url of the application to be run  -`app`：字符串，要运行的应用程序的URL
 - `args`: array of strings, startup arguments to be passed to the application  -`args`：字符串数组，要传递给应用程序的启动参数
 - `categories`: array of strings, tracing categories to be enabled  -`categories`：字符串数组，跟踪要启用的类别
 - `duration`: integer, duration of tracing in seconds  -`duration`：整数，以秒为单位的跟踪持续时间
 - `measure`: array of measurement specifications, see Benchmarking  -`measure`：测量规范数组，请参阅基准测试

 
### Benchmarking  标杆管理 

Benchmarking docs moved to a [separate doc]( /docs/development/benchmarking/trace_based_benchmarking.md). 基准测试文档移至[单独的文档]（/docs/development/benchmarking/trace_based_benchmarking.md）。

 
## Configuration  组态 

The tracing configuration is a JSON file consisting of a list of known category names and descriptions. 跟踪配置是一个JSON文件，由已知类别名称和描述的列表组成。

```json
    {
      "categories": {
        "category1": "description1",
        "category2": "description2"
      },
      "providers": {
        "provider-label": "file:///provider-to-start-automatically"
      }
    }
```
