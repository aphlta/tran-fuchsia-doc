 
# Catapult User Guide (Version 1)  弹射器用户指南（版本1） 

 
* Updated: 2018 July 27  *更新时间：2018年7月27日

[TOC]  [目录]

 
## Overview  总览 

The Catapult dashboard is the UI we send benchmark results to for monitoring and visualization.  The dashboard is maintained by the Chrome team.  This a short guide on howto find and use the results of your benchmarks in the dashboard. Catapult仪表板是我们将基准测试结果发送到以进行监视和可视化的UI。资讯主页由Chrome小组维护。这是有关如何在仪表板中查找和使用基准测试结果的简短指南。

 

 
## Accessing the Dashboard  访问仪表板 

**Be sure to sign into your google.com account or else Fuchsia data will be hidden.**  **请务必登录您的google.com帐户，否则紫红色数据将被隐藏。**

The login button is in the top right corner of the screen.  登录按钮在屏幕的右上角。

The dashboard can be found at [https://chromeperf.appspot.com/report](https://chromeperf.appspot.com/report).  仪表板可以在[https://chromeperf.appspot.com/report](https://chromeperf.appspot.com/report）中找到。

 

 
## Searching and Adding Graphs  搜索和添加图形 

The dashboard displays a list of search boxes.  The placeholder names are relics from the days when Chrome infrastructure was still using BuildBot.  Since they are not relevant toFuchsia infrastructure, we map our own data into these fields with the following scheme: 仪表板显示搜索框列表。占位符名称是Chrome基础架构仍在使用BuildBot以来的遗物。由于它们与倒挂金钟基础设施无关，因此我们使用以下方案将我们自己的数据映射到这些字段中：

 
* `Test suite` == the name of the benchmark suite.  *`Test suite` ==基准套件的名称。
* `Bot` == A Fuchsia LUCI builder that has run the benchmark at least once.  *`Bot` ==至少运行一次基准测试的Fuchsia LUCI构建器。
* `Subtest` == The name of the test case in your benchmark suite.  *`Subtest` ==您的基准套件中测试用例的名称。

Type the name of your benchmark suite in the first box to begin searching.   As an example, we can see the zircon_benchmarks suite if we type "zircon" 在第一个框中输入基准套件的名称以开始搜索。例如，如果我们键入“ zircon”，我们可以看到zircon_benchmarks套件。

![test_suite_example](/docs/images/benchmarking/test_suite_example.png "test_suite_example")  ！[test_suite_example]（/ docs / images / benchmarking / test_suite_example.png“ test_suite_example”）

Select a builder and a subtest.  Note that if your subtest is named "foo", there will be multiple "foo_<metric_name>" subtests to choose from.  Each of these represents a metriccomputed from the sample(s) of that subtest.   For example: if "foo" generates N samplepoints each time the benchmark is run, then the subtest "foo_avg" is a plot of theaverages of these N samples. 选择一个构建器和一个子测试。请注意，如果您的子测试名为“ foo”，则将有多个“ foo_ <metric_name>”子测试可供选择。这些中的每一个都代表从该子测试的样本计算得出的指标。例如：如果每次运行基准测试时“ foo”生成N个采样点，则子测试“ foo_avg”是这N个采样的平均值的图。

When you're finished filling out each field, click "Add" to add your graph to the UI. You should see something like this: 完成填写每个字段后，单击“添加”以将图形添加到UI。您应该会看到以下内容：

![graph_example](/docs/images/benchmarking/graph_example.png "graph_example")  ！[graph_example]（/ docs / images / benchmarking / graph_example.png“ graph_example”）

 

 
## Viewing sample metadata  查看样本元数据 

If you hover over a point in a graph, you can see some extra information such as the point's value, the date it was recorded, and a link to the log page of the build thatgenerated it. 如果将鼠标悬停在图形中的某个点上，则可以看到一些其他信息，例如该点的值，记录该点的日期以及指向生成该点的构建的日志页面的链接。

![tooltip_example](/docs/images/benchmarking/tooltip_example.png "tooltip_example")  ！[tooltip_example]（/ docs / images / benchmarking / tooltip_example.png“ tooltip_example”）

 

 
## Saving the View  保存视图 

v1 of the Catapult dashboard UI does not have a built in mechanism for saving a collection of Graphs.  If you want to save a list of graphs so that you can share with others orre-open the list later, you can copy the URL from the Chrome Address Bar. Catapult仪表板UI的v1没有用于保存图形集合的内置机制。如果您要保存图表列表以便与他人共享或稍后重新打开列表，则可以从Chrome地址栏中复制URL。

Beware, you will have to re-copy the URL each time you add, modify or remove a graph. This includes moving the green slider beneath a graph or making any selections in the box tothe right of the graph. 请注意，每次添加，修改或删除图形时，都必须重新复制URL。这包括将绿色滑块移动到图形下方或在图形右侧的框中进行选择。

 

 
## Enabling Regression Detection  启用回归检测 

To enable regression detection, you must enable "monitoring" for a test by clicking the "Request Monitoring for Tests" button under the "Report issue" dropdown at the top of thepage. 要启用回归检测，您必须通过单击页面顶部“报告问题”下拉菜单下的“请求监视测试”按钮来启用“监视”。

![monitoring_button_example](/docs/images/benchmarking/monitoring_button_example.png "monitoring_button_example")  ！[monitoring_button_example]（/ docs / images / benchmarking / monitoring_button_example.png“ monitoring_button_example”）

This will open a bug form you can fill out to enable monitoring for a benchmark.  The Chrome team has a Sheriff rotation (oncall rotation) to triage regression alerts.  Thedashboard only allows triaging bugs in monorail, so we'll have to make due without JIRAsupport. 这将打开一个错误表单，您可以填写该错误表单以启用对基准的监视。 Chrome小组有一个警长轮换（呼叫轮换），可以对回归警报进行分类。仪表板仅允许分类单轨火车中的错误，因此我们必须在没有JIRA支持的情况下进行检查。

See this link for more information about the [Sheriff rotation]  有关[警长轮换]的更多信息，请参见此链接。

