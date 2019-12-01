 
# Benchmark Results Schema  基准结果架构 

 
* Updated: 2018 August 9  *更新时间：2018年8月9日

[TOC]  [目录]

This document describes the JSON schema that Fuchsia benchmark results must follow in order to be uploaded to the performance dashboard. 本文档描述了Fuchsia基准测试结果必须遵循的JSON模式，才能将其上载到性能仪表板。

 
## Helper Libraries  助手库 

If you're creating a [trace-based benchmark], your exported results will already have the correct schema. 如果要创建[基于跟踪的基准]，则导出的结果将已经具有正确的架构。

If you're writing your own benchmark program, then you can use the existing Fuchsia libraries for your language for emitting the JSON data: 如果您正在编写自己的基准测试程序，那么可以使用现有的Fuchsia库作为您的语言来发出JSON数据：

 
* [C/C++]  * [C / C ++]
* [Go]  * [走]
* [Dart]  * [飞镖]

Note: If your benchmark is in a different language, please provide a reuseable library or file a bug against IN to request one. 注意：如果基准测试使用其他语言，请提供可重用的库或针对IN提交错误以请求一个。

[C/C++]: /zircon/system/ulib/perftest [Go]: /garnet/go/src/benchmarking[Dart]: /sdk/testing/sl4f/client/lib/src/trace_processing/metrics_results.dart[Rust]: /src/developer/fuchsia-criterion[trace-based benchmark]: trace_based_benchmarking.md [C / C ++]：/ zircon / system / ulib / perftest [执行]：/ garnet / go / src /基准测试[Dart]：/sdk/testing/sl4f/client/lib/src/trace_processing/metrics_results.dart[Rust ]：/ src / developer / fuchsia-criterion [基于跟踪的基准]：trace_based_benchmarking.md

 
## JSON Description  JSON说明 

```json
[
    {
        "label":       string     // Name of the test case in the performance dashboard.
        "test_suite":  string     // Name of the test suite in the performance dashboard.
        "unit":        string     // One of the supported units (see below)
        "values":      [v1, v2..] // Numeric values collected in this test case
        "split_first": bool       // Whether to split the first element in |values| from the rest.
    },
    {
        ...
    }
]
```
 

 
## Supported Units:  支持单位： 

In order to convert benchmark results to the format required by the performance dashboard, `unit` must be one of the following strings, which describe the unitsof the result's `values`. 为了将基准结果转换为性能仪表板所需的格式，“ unit”必须是以下字符串之一，这些字符串描述了结果“值”的单位。

 
* `nanoseconds`  or `ns`  *`nanoseconds`或`ns`
* `milliseconds` or `ms`  *“毫秒”或“ ms”
* `bytes/second`  *`bytes / second`
* `bytes`  *`bytes`

 

 
### Example  例 

```json
[
    {
        "label": "Channel/WriteRead/64bytes",
        "test_suite": "fuchsia.zircon_benchmarks",
        "unit": "nanoseconds",
        "values": [105.45, 697.916667, 672.743056],
        "split_first": true
    },
    {
        "label":"Channel/WriteRead/1024bytes",
        "test_suite":"fuchsia.zircon_benchmarks",
        "unit":"nanoseconds",
        "values":[102.23, 1004.340278, 906.250000],
        "split_first": true
    }
]
```
 

 
## split_first behavior  split_first行为 

split_first is useful when the first value in the test results is usually skewed due to external influence on the test (e.g. empty caches).  When true, benchmarkresults will appear as two separate series in the performance dashboard: 当测试结果中的第一个值通常由于外部对测试的影响而倾斜时（例如空缓存），split_first很有用。设置为true时，基准结果将在性能仪表板中显示为两个单独的系列：

 
1. `$label/samples_0_to_0` which tracks the first element in `values`, and  1.`$ label / samples_0_to_0`，用于跟踪“ values”中的第一个元素，以及
