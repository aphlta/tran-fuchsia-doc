<!-- source for images is https://docs.google.com/document/d/1ykMBMDLKxKDpn9UnYtHYU3iJusAeNC4Aeijcra5qi-Y/edit?usp=sharing -->  <！-图像来源是https://docs.google.com/document/d/1ykMBMDLKxKDpn9UnYtHYU3iJusAeNC4Aeijcra5qi-Y/edit?usp=sharing->

Getting Started with Fuchsia's Inspect API ===== 紫红色的Inspect API入门=====

The Fuchsia **Inspect API** allows your program to provide structured information in an abstract, language-independent format for the use ofother programs and services. 紫红色的“ Inspect API” **允许您的程序以抽象的，独立于语言的格式提供结构化信息，以供其他程序和服务使用。

This document is a "Getting Started" guide to give you:  本文档是“入门”指南，可为您提供：

 
 * an overview of what the Inspect API does and how it works,  *有关Inspect API的功能及其工作原理的概述，
 * an introduction to what your program needs to provide in order to work with the API, and  *介绍您的程序需要提供什么才能使用API​​，以及
 * some use-cases to fire your imagination.  *一些用例激发您的想象力。

It includes two "quick starts" as well, for [writing a new component](#i_m-writing_a_new_component) and[modifying an existing component](#i_m-modifying-an-existing-component). 它还包括两个“快速开始”，用于[编写新组件]（i_m-writing_a_new_component）和[修改现有组件]（i_m-modification-an-existing-component）。

[TOC]  [目录]

 
# Overview  总览 

[Inspect][inspect] can be thought of as being at the top of a "get data from a program" pile:  可以将[检查] [检查]视为“从程序获取数据”堆的顶部：

![Figure: Data export](dataexport.png)  ！[图：数据导出]（dataexport.png）

At the bottom level, logging just blindly spits out fixed data. It usually goes to some kind of a system logger, and ends up in a log file.In terms of complexity, it's the simplest to implement (usually via a **printf()**-likefunction call). 在底层，日志记录只是盲目地吐出固定数据。它通常进入某种系统记录器，并最终保存在一个日志文件中。就复杂性而言，它是最简单的实现（通常通过** printf（）**之类的函数调用）。

Tracing provides more control: it can be turned on and off, and you can select the data set that you want to extract at run time.Clients can be more sophisticated with their control and consumption of tracing data. 跟踪提供了更多的控制权：可以打开和关闭它，并且可以选择要在运行时提取的数据集。客户端可以更加轻松地控制和使用跟踪数据。

Inspect, on the other hand, provides a hierarchical, structured view of the program's runtime data, allowing inspection to occur in an ad-hoc manner.However, it does take more effort to implement. 另一方面，Inspect提供了程序运行时数据的分层结构视图，允许以临时方式进行检查。但是，它确实需要花费更多的精力来实现。

> More intrusive inspection of the program is possible, of course &mdash; various debuggers, > like [`zxdb`][zxdb], allow any memory location in the program to be accessed.> But the data is accessed more "in spite of" the program, rather than cooperatively. >当然，可以对该程序进行更具侵入性的检查。各种调试器，例如[`zxdb`] [zxdb]，都允许访问程序中的任何内存位置。>但是，对数据的访问更多地是“尽管”程序，而不是协同进行。

 
# A simple example  一个简单的例子 

In this tutorial, we're going to use a persistent "black box" program for our examples.  在本教程中，我们将为示例使用一个持久的“黑匣子”程序。

The key concept here is that the program knows its own state and organization best, so it's the one that publishes it. 这里的关键概念是程序最了解自己的状态和组织，因此它是发布程序的状态。

We're going to see how to organize the data in your program so that it's readily accessible to Inspect (and that it's organized in a logical manner). 我们将了解如何在程序中组织数据，以便Inspect可以方便地访问它们（并以逻辑方式对其进行组织）。

 
## An employee management system  员工管理系统 

Our example program is an employee management system. The program manages its own state.  我们的示例程序是一个员工管理系统。该程序管理自己的状态。

The system keeps track of a corporation's employees. Each employee has a record that contains the following data: 该系统跟踪公司的员工。每位员工都有一条包含以下数据的记录：

 
 * employee's name,  * 员工的名字，
 * employee's email address,  *员工的电子邮件地址，
 * a list of tasks (if any).  *任务列表（如果有）。
 * a list of direct reports (if any).  *直接报告列表（如果有）。

> Note that the email address is used as a key, and is unique.  >请注意，电子邮件地址用作密钥，并且是唯一的。

To give you a big picture:  为了给您一个大图景：

![Figure: The corporate ladder](relations.png)  ！[图：公司阶梯]（relations.png）

> The source code for this example is in > [`//src/lib/inspect_deprecated/integration/example.cc`][example.cc]. >该示例的源代码位于> [`//src/lib/inspect_deprecated/integration/example.cc`][example.cc]中。

First, let's look at the internal organization of the data from `example.cc` (line identifiers are local to the description, not the actual file): 首先，让我们看一下example.cc中数据的内部组织（行标识符位于描述本地，而不是实际文件）：

```c++
[E01] class Employee {
[E02] ...
[E03]  private:
[E04]  std::string name_;
[E05]  std::string email_;
[E06]
[E07]   // Vector of |Task|s assigned to this |Employee|.
[E08]   std::vector<std::unique_ptr<Task>> tasks_;
[E09]
[E10]   // Vector of |Employee|s reporting to this |Employee|.
[E11]   std::vector<std::unique_ptr<Employee>> reports_;
[E12]
[E13]   // Node under which this |Employee| can expose inspect information.
[E14]   inspect::Node node_;
[E15]
[E16]   // Properties for name and email.
[E17]   inspect::StringProperty name_property_;
[E18]   inspect::StringProperty email_property_;
[E19]
[E20]   // Node under which this |Employee| nests |Task|s.
[E21]   inspect::Node task_node_;
[E22]
[E23]   // Node under which this |Employee| nests reporting |Employee|s.
[E24]   inspect::Node report_node_;
[E25]
[E26]   // Container for various computed "Lazy" metrics we wish to expose.
[E27]   std::vector<inspect::LazyMetric> lazy_metrics_;
[E28] };
```
 

Or, visually:  或者，在视觉上：

![Figure: The Employee class](employee.png)  ！[图：员工类]（employee.png）

We've divided the `Employee` class into two parts (separated by the dashed line in the diagram); the part on the right contains the "native database" members, and consists of: 我们将“ Employee”类分为两部分（图中的虚线分隔）；右边的部分包含“本地数据库”成员，并由以下部分组成：

 
 * `name_` (`[E04]`) &mdash; the employee's name (`std::string`),  *`name_`（`[E04]`）mdash;员工的名字（`std :: string`），
 * `email_` (`[E05]`) &mdash; the employee's email (`std::string`),  *`email_`（`[E05]`）mdash;员工的电子邮件（“ std :: string”），
 * `tasks_` (`[E08]`) &mdash; a list of tasks assigned to the employee (`vector<std:unique_ptr<Task>>`), and *`tasks_`（`[E08]`）mdash;分配给员工的任务列表（“ vector <std：unique_ptr <任务>>”），以及
 * `reports_` (`[E11]`) &mdash; a hierarchy of direct reports (`vector<std::unique_ptr<Employee>>`). *`reports_`（`[E11]`）mdash;直接报告的层次结构（“ vector <std :: unique_ptr <Employee >>”）。

The part on the left consists of the Inspect members:  左侧的部分由Inspect成员组成：

 
 * `node_` (`[E14]` &mdash; binding for the Inspect framework (`inspect::Node`),  *`node_`（`[E14]`mdash;为Inspect框架（`inspect :: Node`）绑定，
 * `name_property_` (`[E17]`) &mdash; the employee's name as an inspect "string" property (`inspect::StringProperty`), *`name_property_`（`[E17]`）mdash;员工姓名作为检查“字符串”属性（“ inspect :: StringProperty”），
 * `email_property_` (`[E18]`) &mdash; the employee's email (`inspect::StringProperty`),  *`email_property_`（`[E18]`）mdash;员工的电子邮件（“ inspect :: StringProperty”），
 * `task_node_` (`[E21]`) &mdash; Inspect framework binding to subordinate tasks (`inspect::Node`), *`task_node_`（`[E21]`）mdash;检查框架绑定到下级任务（“ inspect :: Node”），
 * `report_node_` (`[E24]`) &mdash; Inspect framework binding to subordinate reports (`inspect::Node`), and *`report_node_`（`[E24]`）mdash;检查框架绑定到下级报告（“ inspect :: Node”），以及
 * `lazy_metrics_` (`[E27]`) &mdash; information about the employee's metrics (`vector<inspect::LazyMetric>`). *`lazy_metrics_`（`[E27]`）mdash;有关员工指标的信息（“ vector <inspect :: LazyMetric>”）。

We'll forgo discussing the "native database" part of the implementation in depth; it's standard C++.  我们将不再深入讨论实现的“本地数据库”部分。这是标准的C ++。

> It's important to keep in mind that we have two hierarchies of employee and task > information: one is maintained by the "native database" part (via the `vector`s of> `Employee`s and `Task`s), and the other is maintained by the Inspect nodes> (`node_`, `task_node_`, and `report_node_`).>> Philosophically, we *want* to keep the two representations distinct &mdash; what gets> presented to the Inspect interface may not necessarily map one-to-one with the internal> representation, for a number of reasons.> For example, we might have additional information we don't want to expose,> or the internal representation may be optimized for the application rather than> for presentation, etc. >请务必记住，我们具有雇员和任务>信息的两个层次结构：一个由“本地数据库”部分维护（通过“雇员”和“任务”的“向量”部分），以及另一个是由“检查节点”（“ node _”，“ task_node_”和“ report_node_”）维护的。出于多种原因，>呈现给Inspect界面的内容可能不一定与internal>表示形式一对一映射。例如，我们可能不想公开其他信息，或者内部表示可以针对应用进行优化，而不是针对表示等进行优化。

In our example, we use the following Inspect types:  在我们的示例中，我们使用以下Inspect类型：

Type                      | Use --------------------------|-----------------------------------`inspect::Node`           | A node under which properties, metrics, and other nodes may be nested`inspect::StringProperty` | Property with value given by a string`inspect::LazyMetric`     | A named metric, with the value determined by evaluating a callback 类型使用-------------------------- | ---------------------- -------------`inspect :: Node` |在其下可以嵌套属性，指标和其他节点的节点inspect :: StringProperty` |属性由字符串`inspect :: LazyMetric` |给定。命名指标，其值通过评估回调确定

 
### Creating the root node  创建根节点 

The root node is where the data set for Inspect begins. There's a little bit of housekeeping in **main()** that gets that going: 根节点是Inspect数据集的开始位置。 ** main（）**中有一些整理工作可以解决这个问题：

```c++
int main(int argc, const char** argv) {
  // Standard component setup, create an event loop and obtain the
  // |StartupContext|.
  async::Loop loop(&kAsyncLoopConfigAttachToCurrentThread);
  auto context = component::StartupContext::CreateFromStartupInfo();

  // Create a root node from the context's object_dir.
  inspect::Node root_node(*context->outgoing().object_dir());
```
 

The `async::Loop` object creates the event loop for the component. Event loops are responsible for serving interfaces exposed by this component, including Inspect. async :: Loop对象创建组件的事件循环。事件循环负责服务此组件公开的接口，包括Inspect。

Calling **component::StartupContext::CreateFromStartupInfo()** provides a common set of interfaces to the environment this component is running in.One of these interfaces is for Inspection, and the root node of thisinterface is obtained by wrapping the outgoing **object_dir()**. 调用** component :: StartupContext :: CreateFromStartupInfo（）**提供了该组件运行所在的环境的一组通用接口，其中一个接口用于检查，该接口的根节点通过包装传出的*获得* object_dir（）**。

Once the `root_node` is created, we add some named metric counters to it:  一旦创建了“ root_node”，我们将为其添加一些命名的度量计数器：

```c++
  // Create global metrics and globally publish pointers to them.
  auto employee_count = root_node.CreateUIntMetric("employee_count", 0);
  auto task_count = root_node.CreateUIntMetric("task_count", 0);
  auto cleanup = SetGlobals(&employee_count, &task_count);
```
 

We'll come back to the [global metric counters later](#global-metrics).  稍后我们将返回[全局指标计数器]（global-metrics）。

And now we can populate the hierarchy. We'll start with the CEO: 现在我们可以填充层次结构了。我们将从首席执行官开始：

```c++
  // Create a CEO |Employee| nested underneath the |root_node|.
  // The name "reporting_tree" will appear as a child of the root node.
  Employee ceo("CEO", "ceo@example.com", root_node.CreateChild("reporting_tree"));
```
 

The `ceo` node is the root of both our native database and the parallel Inspect hierarchy (at `root_node`).The `Employee` constructor (starting at line `[M06]`, below) shows us how that's done: “ ceo”节点既是本机数据库又是并行Inspect层次结构（位于“ root_node”）的根。“ Employee”构造函数（从下面的“ [M06]行开始”）向我们展示了如何做到这一点：

```c++
[M01] class Employee {
[M02]  public:
[M03]   // Create a new |Employee|.
[M04]   // Note that the constructor takes an |inspect::Node| that we may use to
[M05]   // expose our own metrics, properties, and children nodes.
[M06]   Employee(std::string name, std::string email, inspect::Node node)
[M07]       : name_(std::move(name)),
[M08]         email_(std::move(email)),
[M09]         node_(std::move(node)) {
[M10]     // Increment the global employee count.
[M11]     CountEmployees(1);
[M12]
[M13]     // Create an |inspect::StringProperty| for the name and email of this
[M14]     // employee.
[M15]     name_property_ = node_.CreateStringProperty("name", name_);
[M16]     email_property_ = node_.CreateStringProperty("email", email_);
[M17]     // |Task| nodes are nested under another child node, called "tasks".
[M18]     task_node_ = node_.CreateChild("tasks");
[M19]     // Each |Employee| reporting to this |Employee|  are nested under another
[M20]     // child node, called "reports".
[M21]     report_node_ = node_.CreateChild("reports");
...
```
 

The arguments to the constructor are:  构造函数的参数为​​：

Argument | Meaning ---------|--------`name`   | The name of the employee ("CEO")`email`  | The employee's email address ("ceo@example.com")`node`   | The Inspect object associated with this node 争论含义--------- | --------`name` |员工的姓名（“ CEO”）员工的电子邮件地址（“ ceo@example.com”）`节点`|与此节点关联的Inspect对象

The `node` that we passed was generated by calling `root_node.CreateChild("reporting_tree")`.This creates a child node, "reporting_tree", and it's this childnode that is now associated with the CEO's node. 我们通过的`node`是通过调用`root_node.CreateChild（“ reporting_tree”）`生成的。这将创建一个子节点“ reporting_tree”，并且该子节点现在与CEO的节点相关联。

This is what we've built so far (omitting the native database part):  到目前为止，这是我们构建的内容（省略了本机数据库部分）：

![Figure: Starting at the top](ceo.png)  ！[图：从顶部开始]（ceo.png）

 
### Adding more reports  添加更多报告 

Let's add a few more direct reports to get the flavor of how this works:  让我们添加更多直接报告来了解其工作原理：

```c++
  // Create some reports for the CEO, named Bob, Prakash, and Svetlana.
  auto* bob = ceo.AddReport("Bob", "bob@example.com");
  auto* prakash = ceo.AddReport("Prakash", "prakash@example.com");
  auto* svetlana = ceo.AddReport("Svetlana", "svetlana@example.com");

  // Bob has 3 reports: Julie, James, and Jun.
  bob->AddReport("Julie", "julie@example.com");
  bob->AddReport("James", "james@example.com");
  bob->AddReport("Jun", "jun@example.com");
```
 

We've allocated variables for Bob, Prakash, and Svetlana because we're going to be doing more work with them later; but Julie, James, and Jun don't get storedin local variables, because we have no further need for them.We could always fetch them later by following the hierarchy if we wanted to. 我们已经为Bob，Prakash和Svetlana分配了变量，因为稍后我们将与它们做更多的工作。但是Julie，James和Jun不会存储在局部变量中，因为我们不再需要它们了。如果需要的话，我们以后总是可以通过遵循层次结构来获取它们。

The `Employee` class has a member function, **AddReport()**, that takes two strings, a name and an email, and adds them to both hierarchies: `Employee`类具有成员函数** AddReport（）**，该函数接受两个字符串，一个名称和一封电子邮件，并将它们添加到两个层次结构中：

```c++
[A01] class Employee {
[A02]  public:
[A03] ...
[A04]   // Add a new |Employee| reporting to this |Employee|.
[A05]   Employee* AddReport(std::string name, std::string email) {
[A06]     return reports_
[A07]         .emplace_back(std::make_unique<Employee>(
[A08]             std::move(name), std::string(email),
[A09]             // Note: We need to pass a Node linked under this Node into the
[A10]             // new child. We use the |email| directly, since elsewhere we
[A11]             // guarantee everyone's emails are unique.
[A12]             report_node_.CreateChild(std::move(email))))
[A13]         .get();
[A14]   }
```
 

We call **emplace_back()** to take the newly created `Employee` node (constructed on `[A07]`) and add it to the end of the native database vector `reports_`.We called the Inspect function **CreateChild()** to create a new child node, which is storedby the constructor (via `node_(std::move(node))` on line `[M09]` in the `Employee`constructor code from the previous sample.) 我们调用** emplace_back（）**以获取新创建的`Employee`节点（在[A07]上构建）并将其添加到本地数据库向量`reports_`的末尾。我们将Inspect函数** CreateChild命名为（）**以创建一个新的子节点，该子节点由构造函数存储（通过上一个示例的Employee构造函数代码中的第[M09]行的node_（std :: move（node）））。

 
### Chaining  链式 

The **AddReport()** member function is structured so that it returns a pointer to the newly added record; this makes it easy to chain multiple actions: ** AddReport（）**成员函数的结构使其返回指向新添加的记录的指针；这使得链接多个动作变得容易：

```c++
  // Prakash has two reports: Gerald and Nathan.
  prakash->AddReport("Gerald", "gerald@example.com");

  // Nathan is an intern, so assign him a task to complete his training.
  prakash->AddReport("Nathan", "nathan@example.com")
      ->AddTask("ABC-12", "Complete intern code training")
      ->SetCompletion(1);
```
 

In Gerald's case, we ignore the return value from **AddReport()**. We have no further actions to do here.But we do make use of it in Prakash's case to call **AddTask()**. 在Gerald的情况下，我们忽略了** AddReport（）**的返回值。我们在这里没有进一步的操作，但是在Prakash的案例中确实使用了它来调用** AddTask（）**。

**AddTask()** is structured similarly: it returns a pointer to the newly created `Task` element, so that we can chain a call to **SetCompletion()**. ** AddTask（）**的结构类似：它返回一个指向新创建的`Task`元素的指针，因此我们可以将调用链接到** SetCompletion（）**。

From the Inspect point of view, **AddTask()** does the same kind of work as **AddReport()**, that is, it adds a child node via **CreateChild()** (line `[T25]` below): 从Inspect的角度来看，** AddTask（）**与** AddReport（）**做相同的工作，也就是说，它通过** CreateChild（）**添加一个子节点（第[T25行]`）：

```c++
[T01] class Employee {
[T02]  public:
[T03] ...
[T04]   Task* AddTask(std::string bug_number, std::string name) {
[T05]     size_t least_loaded_count = GetTaskCount();
[T06]     Employee* least_loaded_employee = this;
[T07]
[T08]     // Iterate over reports to find the report with the least number of existing
[T09]     // tasks.
[T10]     for (auto& report : reports_) {
[T11]       if (report->GetTaskCount() <= least_loaded_count) {
[T12]         least_loaded_count = report->GetTaskCount();
[T13]         least_loaded_employee = report.get();
[T14]       }
[T15]     }
[T16]
[T17]     if (least_loaded_employee == this) {
[T18]       // If this |Employee| is the least loaded, take the |Task|...
[T19]       return tasks_
[T20]           .emplace_back(std::make_unique<Task>(
[T21]               std::move(bug_number), std::move(name),
[T22]               // Note: We need to pass a Node linked under this Node into
[T23]               // the new child. We use |inspect::UniqueName| to assign a
[T24]               // globally unique suffix to the child's name.
[T25]               task_node_.CreateChild(inspect::UniqueName("task-"))))
[T26]           .get();
[T27]     } else {
[T28]       // ... otherwise, recursively add the |Task| to the least loaded report.
[T29]       return least_loaded_employee->AddTask(std::move(bug_number),
[T30]                                             std::move(name));
[T31]     }
[T32]   }
```
 

As you can see, though, **AddTask()** does a lot more work on the native database side.  正如您所看到的，** AddTask（）**在本机数据库方面做了很多工作。

 
### Global metrics  全球指标 

One of the very first things we did in **main()** was we attached two metrics, "employee_count" and "task_count" (as unsigned integers) to the root node: 我们在** main（）**中做的第一件事之一是，将两个指标“ employee_count”和“ task_count”（作为无符号整数）附加到根节点：

```c++
  // Create global metrics and globally publish pointers to them.
  auto employee_count = root_node.CreateUIntMetric("employee_count", 0);
  auto task_count = root_node.CreateUIntMetric("task_count", 0);
  auto cleanup = SetGlobals(&employee_count, &task_count);
```
 

We call these "global" because they apply to the entire database; `employee_count` tells us the total number of employees in the hierarchy, and `task_count` tellsus the total number of tasks. 我们称它们为“全局”是因为它们适用于整个数据库。 `employee_count`告诉我们层次结构中的雇员总数，而`task_count`告诉我们任务的总数。

The values of these metrics are available (via Inspect) from the root node.  这些指标的值可从根节点获得（通过检查）。

The values themselves are updated via the various member functions as employees and tasks get added or deleted. 这些值本身会随着员工和任务的添加或删除而通过各种成员函数进行更新。

> This is another example of a "disjoint" database &mdash; the "native database" > doesn't have the concept of "employee count" or "task count", it simply> doesn't need it.> But the Inspect hierarchy provides it for external consumption. >这是“不相交”数据库mdash的另一个示例； “本地数据库”>没有“员工人数”或“任务人数”的概念，它只是>不需要。>但是Inspect层次结构将其提供给外部使用。

 
### Lazy metrics  懒指标 

Recall that our `Employee` class has a vector of `inspect::LazyMetric` values, called `lazy_metrics_`.There are two lambda functions associated with the metrics, one to compute"personal_performance" and one for "report_performance" metrics. 回想一下，我们的`Employee`类具有一个`inspect :: LazyMetric`值向量，称为`lazy_metrics_`。有两个与该指标关联的lambda函数，一个用于计算“ personal_performance”，另一个用于“ report_performance”指标。

 
#### Personal performance metric  个人绩效指标 

The computation of the personal performance lazy metric is achieved by binding a lambda function (lines `[P08` .. `P13]` below) via the Inspect function**CreateLazyMetric()**: 个人绩效懒惰指标的计算是通过Inspect函数** CreateLazyMetric（）**绑定lambda函数（下面的行[P08 ... P13]）来实现的：

```c++
[P01]class Employee {
[P02] public:
[P03]...
[P04]    // Create an |inspect::LazyMetric| for this |Employee|'s personal
[P05]    // performance. The "personal_performance" of an |Employee| is the average
[P06]    // completion of their |Task|s.
[P07]    lazy_metrics_.emplace_back(node_.CreateLazyMetric(
[P08]        "personal_performance", [this](component::Metric* out) {
[P09]          // Callbacks have an "out" parameter that is set to the desired value.
[P10]          // In this case, set it to the double value of our
[P11]          // |EmployeePerformance|.
[P12]          out->SetDouble(GetPerformance().CalculateCompletion());
[P13]        }));
```
 

The lambda function gets passed the node (via `this`) and is expected to return the value through the `out` pointer.The actual computation is handled by a native database **CalculateCompletion()** function,which returns a `double`.This `double` value is then stored in `out` by an Inspect member function **SetDouble()**on line `[P12]`. lambda函数（通过`this`）传递给节点，并期望通过`out`指针返回值。实际计算由本机数据库** CalculateCompletion（）**函数处理，该函数返回一个double型值。然后，此“双精度”值由“ [P12]”行上的Inspect成员函数** SetDouble（）**存储在“输出”中。

 
#### Report performance metric  报告效果指标 

To compute the report performance, similar code is used:  要计算报告效果，使用类似的代码：

```c++
[R01]class Employee {
[R02] public:
[R03]...
[R04]    // Create an |inspect::LazyMetric| for the performance of this
[R05]    // |Employee|'s reports. The "report" performance of an |Employee| is the
[R06]    // average completion of all |Task|s assigned to their direct reports.
[R07]    lazy_metrics_.emplace_back(node_.CreateLazyMetric(
[R08]        "report_performance", [this](component::Metric* out) {
[R09]          // Add together the performance for each report, and set the result in
[R10]          // the out parameter.
[R11]          EmployeePerformance perf = {};
[R12]          for (const auto& report : reports_) {
[R13]            perf += report->GetPerformance();
[R14]          }
[R15]          out->SetDouble(perf.CalculateCompletion());
[R16]        }));
[R17]  }
```
 

Here, the lambda function (`[R08` .. `R16]`) uses the class `EmployeePerformance` to accumulate the performance over all the reports.It too returns a `double` value, in the same way as the "personal performance" lambda above. 在这里，lambda函数（`[R08`..`R16]`）使用类'EmployeePerformance`来累积所有报告的绩效。它也返回一个'double'值，与“个人绩效”相同上面的lambda。

 
# Using iquery  使用iquery 

The [`iquery`][iquery] tool allows you to look at the Inspect database.  [`iquery`] [iquery]工具可让您查看Inspect数据库。

You first need to find your program &mdash; that is, you need to see where it got registered after startup. 首先，您需要找到程序-也就是说，您需要查看启动后在何处注册。

```
$ iquery --find /hub
/hub/c/sysmgr.cmx/4248/out/objects
/hub/c/sysmgr.cmx/4248/system_objects
/hub/r/sys/4566/c/http.cmx/19226/out/objects
/hub/r/sys/4566/c/http.cmx/19226/system_objects
...
/hub/r/sys/4566/c/libinspect_example_component.cmx/8123/out/objects
/hub/r/sys/4566/c/libinspect_example_component.cmx/8123/system_objects
...
```
 

The above command cause `iquery` to find all the processes that have registered with `/hub` as providing Inspect data.The output has been shortened for the example. 上面的命令使`iquery`查找所有向`/ hub`注册的提供Inspect数据的进程。本示例的输出已缩短。

The last two lines shown, containing `libinspect_example_component.cmx`, correspond to our employee database example.The `8123` is the process ID of the employee database, and there are two pathscontaining nodes: 显示的最后两行包含libinspect_example_component.cmx，与我们的员工数据库示例相对应.8123是员工数据库的进程ID，并且有两个路径包含节点：

Path             | Meaning -----------------|-------------------------------------------`out/objects`    | our exposed Inspect data nodes`system_objects` | system nodes 路径|含义----------------- | ------------------------------- ------------`out / objects` |我们公开的Inspect数据节点“ system_objects” |系统节点

The `system_objects` entry is populated by `appmgr` and includes information about the process itself (open handles, memory information,CPU registers, shared objects, and so on) &mdash; so we'll skip that one. “ system_objects”条目由“ appmgr”填充，并包含有关进程本身的信息（打开句柄，内存信息，CPU寄存器，共享对象等）。所以我们跳过那个。

The `out/objects` tree is the information exposed by the component itself (which is the tree from our example above). “ out / objects”树是组件本身公开的信息（这是上面示例中的树）。

To view the employee database's exposed nodes, you can run `iquery` with the `--recursive` command line option: 要查看员工数据库的公开节点，可以使用带有--recursive命令行选项的`iquery`：

```
$ iquery --recursive /hub/r/sys/4566/c/libinspect_example_component.cmx/8123/out/objects
objects:
  task_count = 16
  employee_count = 12
  reporting_tree:
    email = ceo@example.com
    name = CEO
    report_performance = 0.525000
    personal_performance = 1.000000
    reports:
...
```
 

This dumps the two public global metrics (`task_count` and `employee_count` that we created in "[Global metrics](#global-metrics)" above) as well as the `reporting_tree`hierarchy. 这将转储两个公共全局指标（我们在上面的“ [全局指标]（global-metrics）”中创建的“ task_count”和“ employee_count”）以及“ reporting_tree”层次结构。

Because we specified `--recursive`, `iquery` descends into each branch and dumps the information on that branch recursively. 因为我们指定了`--recursive`，所以`iquery`会进入每个分支并递归地转储该分支上的信息。

If you wanted to dump the data in JSON (perhaps for some post processing), you can specify the `--format=json` parameter to `iquery`: 如果您想以JSON格式转储数据（可能需要进行一些后期处理），则可以在iquery中指定`--format = json`参数：

```
$ iquery --recursive --format=json /hub/r/sys/4566/c/libinspect_example_component.cmx/8123/out/objects
[
  {
    "path": "objects",
    "contents": {
      "objects": {
        "task_count": "16",
        "employee_count": "12",
        "reporting_tree": {
          "email": "ceo@example.com",
          "name": "CEO",
          "report_performance": "0.525000",
          "personal_performance": "1.000000",
          "reports": {
...
```
 

<!--  <！-
# Details  细节 

 
- look at the FIDL API  -看看FIDL API

 
# Quick starts  快速入门 

If you want to jump in and get going, the following sections are intended to give you a quick start on [writing a new component](#) and [modifying an existing component](#).Cross references are provided back to the appropriate "Getting Started" section abovefor topics you may wish to learn about (or revisit). 如果您想进入并继续前进，以下各节旨在使您快速入门[编写新组件]（）和[修改现有组件]（）。交叉引用返回到相应的“入门”。开头”部分，您可能希望了解（或重新访问）这些主题。

 
## I'm writing a new component...  我正在写一个新的组件... 

> Show how to architect a new component to include inspection support from the beginning. > Should link to some skeleton code. >从一开始就演示如何构建一个新组件以包括检查支持。 >应该链接到一些框架代码。

 
## I'm modifying an existing component...  我正在修改现有组件... 

> Show how to add inspection into an existing component, and properly pipe through the needed nodes.  >显示如何将检查添加到现有组件中，并正确地通过所需的节点进行传递。

 
# From the "Inspection Documentation Scope" document  来自“检查文档范围”文档 

> Demonstrate how to read inspection data out of the black box component. > Note: We have received feedback that understanding "where and how" to read inspection data is a significant pain point.> This must be emphasized.> Walkthrough on how to expose inspection data on the hub, with examples of using iquery to inspect that state. >演示如何从黑匣子组件中读取检查数据。 >注意：我们收到的反馈是，理解“从何处以及如何”读取检验数据是一个重大的痛点。>必须强调。>逐步讲解如何在中心上公开检验数据，并举例说明如何使用iquery来检查检验数据。州。

From Chris:  从克里斯：

    The audience for inspect is frequently unfamiliar with components themselves, so readers will need more explanation of what is going on (they just wantto run programs and get data, but we end up forcing them to grapple with"component" concepts). I'll explain my understanding of it: 被检查的读者常常不熟悉组件本身，因此读者将需要更多有关发生情况的解释（他们只是想运行程序并获取数据，但最终迫使他们应对“组件”概念）。我将解释我对此的理解：

    The example app is built as a component here <https://fuchsia-review.googlesource.com/c/fuchsia/+/251575/2/garnet/public/lib/inspect/integration/BUILD.gn#51>.This means it has a component manifest here<https://fuchsia-review.googlesource.com/c/fuchsia/+/251575/2/garnet/public/lib/inspect/integration/meta/libinspect_example_component.cmx>.The manifest is standard boilerplate specifying which binary to run whenthe component is started, and says it has access to the Launcher andEnvironment services (this part may not be necessary, I'll take a look atit). 示例应用程序是在<https://fuchsia-review.googlesource.com/c/fuchsia/+/251575/2/garnet/public/lib/inspect/integration/BUILD.gn51>中作为组件构建的。在此处具有组件清单<https://fuchsia-review.googlesource.com/c/fuchsia/+/251575/2/garnet/public/lib/inspect/integration/meta/libinspect_example_component.cmx>。清单是标准样板指定启动组件时要运行的二进制文件，并说它有权访问Launcher和环境服务（这部分可能不是必需的，我来看一下）。

    We include the libinspect_example_component component in the "tests" group here <https://fuchsia-review.googlesource.com/c/fuchsia/+/251575/2/garnet/packages/tests/all#54>byincluding the file we defined here<https://fuchsia-review.googlesource.com/c/fuchsia/+/251575/2/garnet/packages/tests/libinspect_integration_tests>.Now a Fuchsia build including the Garnet tests package will include ourcomponent. 通过包含我们在此处定义的文件，我们将libinspect_example_component组件包含在此处的“测试”组中<https://fuchsia-review.googlesource.com/c/fuchsia/+/251575/2/garnet/packages/tests/all54> https://fuchsia-review.googlesource.com/c/fuchsia/+/251575/2/garnet/packages/tests/libinspect_integration_tests>。现在，包含Garnet测试包的Fuchsia版本将包含我们的组件。

    We first need to start our component on the Fuchsia system using:  我们首先需要使用以下命令在Fuchsia系统上启动组件：

    $ run -d fuchsia-pkg:// fuchsia.com/libinspect_integration_tests#meta/libinspect_example_component.cmx $运行-d紫红色-pkg：// fuchsia.com/libinspect_integration_testsmeta/libinspect_example_component.cmx

    This specifies the URL of the package and #meta/libinspect_example_component.cmx specifies which component inside the package to run. run -d starts thecomponent in the background. 这指定了包的URL，meta / libinspect_example_component.cmx指定了要运行包中的哪个组件。运行-d在后台启动组件。

    We can use the iquery tool to find all inspectable components on the system from the hub: 我们可以使用iquery工具从中心获取系统上所有可检查的组件：

    $ iquery --find /hub  $ iquery-查找/集线器

    This gives the path to every inspect tree available. Now the output will differ depending on whether this was run through `fx shell` or directly onthe target. `fx shell` logs the user into the "sys" realm. If you use fxshell you will see: 这为每个可用的检查树提供了路径。现在输出将有所不同，具体取决于它是通过fx shell运行还是直接在目标上运行。 “ fx shell”将用户登录到“ sys”领域。如果使用fxshell，您将看到：

    /hub/c/libinspect_example_component.cmx/<process_id>/out/objects /hub/c/libinspect_example_component.cmx/<process_id>/system_objects /hub/c/libinspect_example_component.cmx/<process_id>/out/objects /hub/c/libinspect_example_component.cmx/<process_id>/system_objects

    If you directly type in the target you will see:  如果直接输入目标，您将看到：

    /hub/r/sys/<realm_id>/c/libinspect_example_component.cmx/<process_id>/out/objects /hub/r/sys/<realm_id>/c/libinspect_example_component.cmx/<process_id>/system_objects /hub/r/sys/<realm_id>/c/libinspect_example_component.cmx/<process_id>/out/objects /hub/r/sys/<realm_id>/c/libinspect_example_component.cmx/<process_id>/system_objects

    There are two node trees exposed for the example. The system_objects tree is populated by appmgr and includes data about the process itself (openhandles, memory in use, stack dumps). The out/objects tree is theinformation exposed by the component itself (which is the tree we aredescribing in the example!). 该示例公开了两个节点树。 system_objects树由appmgr填充，并包含有关进程本身的数据（openhandles，使用中的内存，堆栈转储）。 out / objects树是组件本身公开的信息（这是我们在示例中描述的树！）。

    A comprehensive command to automatically find your component and output its nodes is: 自动查找组件并输出其节点的综合命令为：

    $ iquery --recursive `iquery --find /hub | grep libinspect_example_component.cmx | grep out/objects` $ iquery --recursive`iquery --find / hub | grep libinspect_example_component.cmx | grep out /对象`

    This will find the component wherever it is and output its information.  这将在任何位置找到组件并输出其信息。

 

    From the host, fx iquery finds all nodes on the system and includes it in a report: fx iquery从主机查找系统上的所有节点，并将其包括在报告中：

    $ fx iquery $ fx iquery -s   # include system nodes with -s$ fx iquery -f json  # set format using -f--> $ fx iquery $ fx iquery -s包括-s $ fx iquery -f json使用-f->设置格式的系统节点

