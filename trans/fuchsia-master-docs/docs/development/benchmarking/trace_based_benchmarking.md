 
# Trace-based benchmarking  基于跟踪的基准 

 
* Updated: 2018 Sep 18  *更新时间：2018年9月18日

This document describes how to use trace-based benchmarking to measure and track performance of Fuchsia apps. 本文档介绍了如何使用基于跟踪的基准测试来衡量和跟踪Fuchsia应用程序的性能。

[TOC]  [目录]

 
## Overview  总览 

Trace-based benchmarks measure the performance of an application by running it under [tracing] and analyzing the collected traces tocompute performance metrics. 基于跟踪的基准通过在[跟踪]下运行应用程序并分析收集的跟踪以计算性能指标来衡量应用程序的性能。

For a typical **service** application (application to which clients connect over FIDL), the following components participate in a benchmarking run: 对于典型的“服务”应用程序（客户端通过FIDL连接到的应用程序），以下组件参与基准测试运行：

 
 - **service binary** - the service being benchmarked.  -**服务二进制**-被基准化的服务。
 - **benchmark app** - a client app that connects to the service and exercises the usage patterns we are interested in benchmarking. -基准测试应用程序-连接到服务并执行我们对基准测试感兴趣的使用模式的客户端应用程序。
 - **benchmark spec** - a JSON file specifying which trace events captured during a run of the benchmark app should be measured, and how. -基准测试规范-一个JSON文件，用于指定在运行基准测试应用程序期间捕获的跟踪事件以及如何进行测量。

The same framework can be also used to benchmark single binaries (without the client-server split). 相同的框架也可以用于对单个二进制文件进行基准测试（不进行客户端-服务器拆分）。

 
## Mechanics  机械学 

Trace-based benchmarks are run using the `trace` binary. The spec file needs to be passed to the tool as follows: 基于跟踪的基准测试使用`trace`二进制文件运行。规格文件需要按以下方式传递到工具：

```sh
trace record --spec-file=<path to the spec file>
```
 

 
### Specification file  规格文件 

The specification file configures tracing parameters and specifies measurements. (see [examples/benchmark] if you'd like to see a full example straight away) 规范文件配置跟踪参数并指定度量。 （如果您想立即查看完整的示例，请参见[示例/基准]）

The file supports the following top level-parameters:  该文件支持以下顶级参数：

 
 - `app`: string, url of the application to be run  -`app`：字符串，要运行的应用程序的URL
 - `args`: array of strings, startup arguments to be passed to the application  -`args`：字符串数组，要传递给应用程序的启动参数
 - `categories`: array of strings, tracing categories to be enabled  -`categories`：字符串数组，跟踪要启用的类别
 - `duration`: integer, maximum duration of tracing in seconds  -`duration`：整数，最大跟踪持续时间（以秒为单位）
 - `measure`: array of measurement specifications, see below  -`measure`：测量规范数组，请参见下文

Given the specification file, the `trace` tool runs the `app` with the given `args` for at most `duration` seconds and gathers trace events from the selected`categories`. Then, the tool computes the measurements specified in the`measure` section on the recorded trace events. 在给定规范文件的情况下，“跟踪”工具最多以“持续时间”秒运行带有给定的“ args”的“ app”，并从选定的“类别”中收集跟踪事件。然后，该工具对记录的跟踪事件计算在“测量”部分中指定的测量。

Example:  例：

```{json}
{
  "app": "benchmark_example",
  "args": [],
  "categories": ["benchmark"],
  "measure": [
    ...
  ]
}
```
 

For any tracing parameters that can be passed both as arguments to `trace record` and set in the specification file, the command line value overrides the one fromthe file. 对于任何既可以作为参数传递给“ trace record”又可以在规范文件中设置的跟踪参数，命令行值将覆盖文件中的一个。

 

 
### Measurement types  测量类型 

The `trace` tool supports the following types of measurements:  跟踪工具支持以下类型的测量：

 
 - `duration`  -`持续时间`
 - `time_between`  -`time_between`
 - `argument_value`  -`argument_value`

A `duration` measurement targets a single trace event and computes the duration of its occurrences. The target trace event can be recorded as aduration, an async, or a flow event. “持续时间”度量针对单个跟踪事件并计算其发生的持续时间。目标跟踪事件可以记录为持续时间，异步或流事件。

**Example**:  **例**：

```{json}
    {
      "type": "duration",
      "event_name": "example",
      "event_category": "benchmark"
    },
```
 

 

A `time_between` measurement targets two trace events with the specified anchors (either the beginning or the end of the events) and computes the timebetween the consecutive occurrences of the two. The target events can be"duration", "async", "flow" or "instant" (in which case the anchor doesn't matter).Takes arguments: `first_event_name`, `first_event_category`,`first_event_anchor`, `second_event_name`, `second_event_category`,`second_event_anchor`. “ time_between”测量针对具有指定锚点的两个跟踪事件（事件的开始或结束），并计算两次连续出现之间的时间。目标事件可以是“持续时间”，“异步”，“流”或“即时”（在这种情况下，锚点无关紧要）。采用参数：“ first_event_name”，“ first_event_category”，“ first_event_anchor”，“ second_event_name” ，“ second_event_category”，“ second_event_anchor”。

**Example**:  **例**：

```{json}
    {
      "type": "time_between",
      "first_event_name": "task_end",
      "first_event_category": "benchmark",
      "second_event_name": "task_start",
      "second_event_category": "benchmark"
    }
```
 

In the example above the `time_between` measurement captures the time between the two instant events and measures the time between the end of one task andthe beginning of another. 在上面的示例中，“ time_between”测量捕获两个即时事件之间的时间，并测量一个任务结束与另一个任务开始之间的时间。

 

An `argument_value` measurement is used to record a value of an argument passed to the trace event. Takes as arguments a name and category of the event, name ofthe argument to be recorded and unit in which it is measured. The type of traceevent doesn't matter, but the recorded argument must have `uint64` type. “ argument_value”度量用于记录传递给跟踪事件的参数的值。将事件的名称和类别，要记录的参数的名称和度量单位作为参数。 traceevent的类型无关紧要，但是记录的参数必须具有uint64类型。

**Example**:  **例**：

```{json}
    {
      "type": "argument_value",
      "event_name": "example",
      "event_category": "benchmark",
      "argument_name": "disk_space_used",
      "argument_unit": "Mb"
    }
```
 

 
### Samples  样品 

It is possible to specify an exact number of expected samples. In order to do so, an optional parameter `"expected_sample_count"` with a positive value must bespecified for a given measurement. In that case, if the number of recordedsamples does not match the one provided, an error will be logged and themeasurement will produce no results (failing the benchmark). 可以指定期望样本的确切数量。为此，必须为给定的测量指定具有正值的可选参数“ expected_sample_count”。在这种情况下，如果记录的样本数与提供的样本数不匹配，则会记录错误，并且该测量将不会产生任何结果（基准测试失败）。

You can also specify the `"split_first"` flag to separate the first sample from the rest. This is useful for recording the "cold run" samples (see the[best practices] section). This flag is passed to the exported file as well, incompliance with the [results schema]. 您也可以指定“ split_first”标志以将第一个样本与其余样本分开。这对于记录“冷运行”样本很有用（请参阅[最佳实践]部分）。该标志也被传递到导出的文件，这与[结果模式]不符。

 
### Full example  完整的例子 

See [examples/benchmark] for a full example of a traced-based benchmark.  有关基于跟踪的基准的完整示例，请参见[examples / benchmark]。

 

This example can be run with the following command:  可以使用以下命令运行此示例：

```{shell}
trace record --spec-file=/pkgfs/packages/benchmark/0/data/benchmark_example.tspec
```
 

 
## Best practices  最佳实践 

 
### Consider reusing benchmark binaries  考虑重用基准二进制文件 

The separation between specification files and benchmark binaries allows to define multiple benchmarks based on a single benchmark binary. Note that you canparametrize the benchmark binary by taking command line arguments which can beset to different values in each spec file. 规范文件和基准二进制文件之间的分隔允许基于单个基准二进制文件定义多个基准。请注意，您可以通过采用可以在每个spec文件中设置为不同值的命令行参数来对基准二进制文件进行参数设置。

 
### Record "cold run" samples separately  单独记录“冷运行”样本 

For any duration measurement that happens more than once, chances are that the first time has different performance characteristics that the subsequent ones.You can set `"split_first": true` to report and track the first sampleseparately. 对于任何不止一次进行的持续时间测量，很有可能第一次的性能特征与随后的不同。您可以设置“ split_first”：true来分别报告和跟踪第一个样本。

 
## Results  结果 

By default, the results are printed on the command line in a human-friendly format. 默认情况下，结果以易于使用的格式显示在命令行上。

 
### Export  出口 

If you prefer a machine-friendly format, pass the path to the output file to `trace record` as `--benchmark-results-file=<file>`.  See the [results schema]for the format of the resulting file. 如果您希望使用机器友好的格式，请将输出文件的路径作为--benchmark-results-file = <file>`传递到`trace record`。有关结果文件的格式，请参见[结果模式]。

 
### Dashboard upload  仪表板上传 

Dashboard upload integration and infra support is WIP as of March, 2018.  See the [dashboard user guide] and the instructions for [automating benchmarks]. 截至2018年3月，已完成仪表板上载集成和基础设施支持。请参阅[仪表板用户指南]和有关[自动化基准测试]的说明。

