 
# Fuchsia Tracing Quick Start  紫红色追踪快速入门 

This document describes how to generate and visualize traces using Fuchsia's Tracing System. 本文档介绍了如何使用紫红色的跟踪系统生成和可视化跟踪。

For more in-depth documentation see the [table of contents](README.md).  有关更深入的文档，请参见[目录]（README.md）。

 
## Collecting A Trace  收集痕迹 

Tracing is typically collected with the `traceutil` program run from your development host. The simplest invocation is: 跟踪通常是从开发主机运行的`traceutil`程序收集的。最简单的调用是：

```shell
$ fx traceutil record
```
 

That will collect 10 seconds of trace data using the default set of categories, which is enough for basic graphics data and thread cpu usage. 这将使用默认类别集收集10秒的跟踪数据，这足以满足基本图形数据和线程cpu的使用。

The will produce an HTML file that you can view in Chrome.  会产生一个HTML文件，您可以在Chrome中查看该文件。

 
## Collection Example  收集实例 

In this example, we want to see what the system is doing when we run the `du` (show disk usage) command. 在这个例子中，我们想看看当我们运行“ du”（显示磁盘使用情况）命令时系统在做什么。

We will show this using the `QEMU` version of Fuchsia, hosted on a Linux box.  我们将使用Linux盒子上托管的Fuchsia的QEMU版本来展示这一点。

First, on the Linux box, we start Fuchsia:  首先，在Linux系统上，我们启动Fuchsia：

```shell
linux-shell-1$ fx emu -N
```
 

This configures and runs Fuchsia. After Fuchsia comes up, you can run the `traceutil` program in another Linuxshell: 这将配置并运行紫红色。在紫红色出现之后，您可以在另一个Linuxshell中运行`traceutil`程序：

```shell
linux-shell-2$ fx traceutil record --buffer-size=64 \
    --categories=all --spawn \
    /boot/bin/sh -c "'\
        sleep 2 ;\
        i=0 ;\
        while [ \$i -lt 10 ] ;\
        do /bin/du /boot ;\
            i=\$(( \$i + 1 )) ;\
        done'"
```
 

> Note that the extra quoting and backslashes are required because the command > string has to travel through two shells (first the Linux shell and then the> native Fuchsia shell).> Some fonts don't render the above code sample well, so note that the ordering> is double-quote then single-quote on the first line, and the opposite on> the last line. >请注意，需要额外的引号和反斜杠，因为命令>字符串必须经过两个shell（首先是Linux shell，然后是> native Fuchsia shell）。>有些字体不能很好地呈现上述代码示例，因此请注意那么在第一行中，ordering>是双引号，然后是单引号，而在最后一行则相反。

This invokes the `traceutil` utility with the following command line options:  这会使用以下命令行选项调用`traceutil`实用程序：

 
* `record` &mdash; instructs the `trace` utility to begin recording.  *`record` mdash;指示`trace`实用程序开始记录。
* `--buffer=size=64` &mdash; specifies the buffer size, in megabytes, for the recording buffer. *`--buffer = size = 64` mdash;指定记录缓冲区的缓冲区大小（以兆字节为单位）。
* `--categories=all` &mdash; specifies the collection of all trace categories.  *`--categories = all` mdash;指定所有跟踪类别的集合。
* `--spawn` &mdash; instructs the `trace` utility to launch the program with **fdio_spawn()**. *`--spawn` mdash;指示`trace`实用程序使用** fdio_spawn（）**启动程序。

The command that we're tracing is a small shell script. The shell script waits for 2 seconds (the `sleep 2`) and then enters a `while`loop that iterates 10 times.At each iteration, the `du` command is invoked to print out how much disk spaceis used by `/boot`, the loop variable `i` is incremented, and the `while` conditionis re-evaluated to see if the loop is done. 我们正在跟踪的命令是一个小的Shell脚本。 shell脚本等待2秒（``sleep 2''），然后进入一个``while''循环，该循环重复10次。每次迭代时，都会调用``du''命令以打印出/ boot使用了多少磁盘空间。 ，将循环变量“ i”增加，并重新评估“ while”条件，以查看循环是否完成。

This produces an HTML trace file in the current directory.  这将在当前目录中生成一个HTML跟踪文件。

 
## Visualizing A Trace  可视化轨迹 

To visualize the trace, load the HTML file into Chrome, just as you would any other local file.For example, if the file lives in `/tmp/trace.html` on your machine, you canenter a URL of `file:///tmp/trace.html` to access it (note the triple forward slash). 要可视化跟踪，将HTML文件与其他任何本地文件一样加载到Chrome中，例如，如果该文件位于计算机上的`/ tmp / trace.html`中，则可以输入`file：/ // tmp / trace.html`进行访问（请注意三重正斜杠）。

The display will now show:  显示屏现在将显示：

![drawing](trace-example-overview.png)  ！[绘图]（trace-example-overview.png）

You'll notice that this page has a ton of detail! Although not visible from this high level view, there's a tinytime scale at the very top, showing this entire trace spans about2 and a half seconds. 您会注意到该页面上有很多细节！尽管从此高层次视图中看不到，但在最上方有一个微小的时间刻度，显示整个轨迹大约需要2秒半。

> At this point, you may wish to familiarize yourself with the navigation > controls.> There's a small **`?`** icon near the top right of the screen.> This brings up a help window.> Some important keys are:>> * `w` and `s` to zoom in and out,> * `W` and `S` to zoom in/out by greater steps,> * `a` and `d` to pan left and right, and> * `A` and `D` to pan left/right by greater steps.>> Zooming in is centered around the current mouse position; it's a little> strange at first but really quite handy once you get used to it. >此时，您可能希望熟悉导航>控件。>屏幕右上角附近有一个小**`？`**图标。>这会弹出一个帮助窗口。>一些重要的按键是：>> *`w`和`s`进行放大和缩小，> *`W`和`S`进行较大的放大/缩小，> *`a`和`d`左右移动，和> *`A`和`D`可以向左/向右平移。>>放大以当前鼠标位置为中心；刚开始时有点奇怪，但是一旦习惯了它就非常方便了。

In the sample above, the yellow circle shows the CPU usage area. Here you can see the overall CPU usage on all four cores. 在上面的示例中，黄色圆圈显示CPU使用率区域。在这里，您可以看到所有四个内核的总体CPU使用率。

The "staircase" pattern on the right, indicated by the green circle, is the `du` program's execution. 右侧的“楼梯”模式（由绿色圆圈表示）是“ du”程序的执行。

Notice that there are 10 invocations of the `du` command &mdash; we expected this because our `while` loop ran 10 times, and started a **new** `du`process each time.Therefore, we get 10 new `du` process IDs, one after the other. 注意，`du`命令mdash共有10次调用。我们之所以这样想是因为while循环运行了10次，每次都启动了一个新的du进程，因此，我们获得了10个新的du进程ID，一个接一个。

The real power of tracing is the ability to see correlations and drill down to see where time is spent.Notice the bottom right part of the image, with the blue circle titled "blobfs CPU usage"Here you see little bursts of CPU time, with each burst seemingly related toa `du` invocation. 跟踪的真正功能是查看关联并向下钻取以查看时间的能力。注意，在图像的右下角带有蓝色圆圈的标题为“ blobfs CPU use”的蓝色圆圈在这里您看到很少的CPU时间爆发，每个突发似乎与du调用有关。

Of course, at this high level it's hard to tell what the exact correlation is. Is the cpu usage caused by the **loading** of `du` from the filesystem?Or is it caused by the **execution** of `du` itself as it runs through the targetfilesystem to see how much space is in use? 当然，在如此高的水平下，很难说出确切的相关性是什么。 cpu的使用是由文件系统中的du加载引起的还是由du在目标文件系统中运行以查看正在使用多少空间时本身的执行所引起的？

Let's zoom in (a lot!) and see what's really going on.  让我们放大（很多！），看看实际发生了什么。

> Chrome tracing allows you to deselect ("turn off") process rows. > In order to make the diagram readable, we've turned off a bunch of processes> that we weren't interested in. This is done via a little "x" icon at the far> right of each row. > Chrome跟踪允许您取消选择（“关闭”）过程行。 >为了使该图易于阅读，我们关闭了一些我们不感兴趣的过程。这是通过每行最右边的一个小“ x”图标来完成的。

![drawing](trace-example-zoom1.png)  ！[绘图]（trace-example-zoom1.png）

In the above, we see just two `du` program executions (the first is highlighted with a green oval at the top of the image, and the second follows it below).We deleted the other `du` program executions in order to focus. 在上面的代码中，我们只看到两个`du`程序执行（第一个在图像顶部以绿色椭圆突出显示，第二个在下面显示），我们删除了其他`du`程序执行以集中精力。

Notice also that the first `blobfs` cpu burst actually consist of three main clusters and a bunch of little spikes (subsequent `blobfs` cpu bursts have twoclusters). 还要注意，第一个“ blobfs” cpu突发实际上由三个主要簇和一堆小尖峰组成（随后的“ blobfs” cpu突发具有两个集群）。

At this point, we can clearly see that the `blobfs` bursts are **before** the `du` program invocation.This rules out our earlier supposition that the `blobfs` bursts were the`du` program reading the filesystem.Instead, it confirms our guess that they're related to loading the `du` programitself. 在这一点上，我们可以清楚地看到`blobfs`突发是在`du`程序调用之前的**，这排除了我们之前的假设，`blobfs`突发是`du`程序在读取文件系统。 ，这证实了我们的猜测，即它们与加载`du`程序本身有关。

Let's see what's *really* going on in the `blobfs` burst!  让我们看看“ blobfs”爆发中到底发生了什么！

![drawing](trace-example-blobfs1.png)  ！[绘图]（trace-example-blobfs1.png）

We've cropped out quite a bit of information so that we could again focus on just a few facets.First off, notice the time scale.We're now dealing with a time period spanning from 2,023,500 microseconds frombeginning of tracing through to just past 2,024,500 &mdash; that is, a bitmore than 1,000 microseconds (or 1 millisecond). 我们已经收获了很多信息，以便我们可以再次专注于几个方面。首先，请注意时间范围。我们现在正在处理从追溯到过去的2023500毫秒的时间段2,024,500 mdash;也就是说，超过1000微秒（或1毫秒）。

During that millisecond, `blobfs` executed a bunch of code, starting with something that identified itself as `FileReadAt`, which then called `Blob::Read`, whichthen called `Blob::ReadInternal` and so on. 在那一毫秒内，blobfs执行了很多代码，首先将其自身标识为FileReadAt，然后将其称为Blob :: Read，然后将其称为Blob :: ReadInternal，依此类推。

To correlate this with the code, we need to do a little bit more digging. Notice how at the bottom of the image, it says "Nothing selected. Tap stuff." 要将其与代码关联起来，我们需要做更多的挖掘工作。请注意，在图像底部如何显示“没有选择。点东西”。

This is an invitation to get more information on a given object.  邀请您获取有关给定对象的更多信息。

If we "tap" on top of the `FileReadAt`, we see the following:  如果我们在“ FileReadAt”顶部“点击”，则会看到以下内容：

![drawing](trace-example-filereadat.png)  ！[绘图]（trace-example-filereadat.png）

This tells us a few important things.  这告诉我们一些重要的事情。

 
1. The `Category` is `vfs` &mdash; categories are a high level grouping created by the developers in order to keep functionality together. Knowing that it'sin the `vfs` category allows us to search for it. 1.`Category`是`vfs` mdash;类别是由开发人员创建的高层分组，目的是将功能保持在一起。知道它在`vfs`类别中，就可以搜索它。
2. We get the high resolution timing information. Here we see exactly how long the function executed for. 2.我们获得高分辨率定时信息。在这里，我们确切地看到函数执行了多长时间。

> For the curious reader, you could look at > [//zircon/system/ulib/fs/connection.cc][connection] and see exactly how the> tracing is done for `FileReadAt` &mdash; it's a slightly convoluted macro> expansion. >对于好奇的读者，您可以查看> [//zircon/system/ulib/fs/connection.cc] [连接]，并确切地了解> FileReadAt`跟踪的方式。这是一个稍微复杂的宏>扩展。

Things are even more interesting with `Blob::Read`:  使用`Blob :: Read`，事情变得更加有趣：

![drawing](trace-example-blobread.png)  ！[绘图]（trace-example-blobread.png）

It lives in [//zircon/system/ulib/blobfs/blob.cc][blob], and is very short: 它位于[//zircon/system/ulib/blobfs/blob.cc][blob]中，并且很短：

```cpp
zx_status_t Blob::Read(void* data,
                       size_t len,
                       size_t off,
                       size_t* out_actual) {
    TRACE_DURATION("blobfs", "Blob::Read", "len", len, "off", off);
    LatencyEvent event(&blobfs_->GetMutableVnodeMetrics()->read,
                       blobfs_->CollectingMetrics());

    return ReadInternal(data, len, off, out_actual);
}
```
 

Notice how it calls **TRACE_DURATION()** with the category of `blobfs`, a name of `Blob::Read`, and two additional, named arguments: a length andan offset. 请注意，它是如何使用“ blobfs”类别，“ Blob :: Read”的名称以及另外两个名为“ length”和“ offset”的参数调用** TRACE_DURATION（）**的。

These conveniently show up in the trace, and you can then see the offset and length where the read operation was taking place! 这些内容方便地显示在轨迹中，然后您可以查看发生读取操作的偏移量和长度！

The tracing continues, down through the layers, until you hit the last one, `object_wait_one`, which is a kernel call. 跟踪继续进行，直至遍历所有层，直到您找到最后一个对象“ object_wait_one”，即内核调用。

 
## More on Chrome's Tracing  有关Chrome的跟踪的更多信息 

For documentation on using Chrome's trace view [see here][chrome].  有关使用Chrome的跟踪视图的文档，请参见[chrome]。

