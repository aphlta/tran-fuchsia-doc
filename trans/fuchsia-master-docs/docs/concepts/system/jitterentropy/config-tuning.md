 
# Jitterentropy: tuning the configuration  抖动：调整配置 

The jitterentropy library is written by Stephan Mueller, is available at <https://github.com/smuellerDD/jitterentropy-library>, and is documented at<http://www.chronox.de/jent.html>. In Zircon, it's used as a simple entropysource to seed the system CPRNG. 抖动熵库由Stephan Mueller编写，可从<https://github.com/smuellerDD/jitterentropy-library>获得，并在<http://www.chronox.de/jent.html>上进行记录。在Zircon中，它用作简单的熵源，为系统CPRNG注入了种子。

[The companion document about basic configuration options to jitterentropy](config-basic.md) describes two options that fundamentally affect how jitterentropy runs. This document describesinstead the numeric parameters that control how fast jitterentropy is and how much entropy itcollects, but without fundamentally altering its principles of operation. It also describes how totest various parameters and what to look for in the output (e.g. if adding support for a new device,or to do a more thorough job of optimizing the parameters). [关于抖动熵的基本配置选项的随附文档]（config-basic.md）描述了两个从根本上影响抖动熵运行方式的选项。本文档将描述数值参数，这些数值参数控制抖动的快慢和收集的熵的数量，但不会从根本上改变其工作原理。它还描述了如何测试各种参数以及在输出中寻找什么（例如，是否添加了对新设备的支持，或者完成了优化参数的更彻底的工作）。

[TOC]  [目录]

 
## A rundown of jitterentropy's parameters  抖动熵参数的减少 

The following tunable parameters control how fast jitterentropy runs, and how fast it collects entropy: 以下可调参数控制抖动熵运行的速度以及收集熵的速度：

 
### [`kernel.jitterentropy.ll`](/docs/reference/kernel/kernel_cmdline.md#kernel-jitterentropy-ll-num)  [`kernel.jitterentropy.ll`]（/ docs / reference / kernel / kernel_cmdline.mdkernel-jitterentropy-ll-num） 

"`ll`" stands for "LFSR loops". Jitterentropy uses a (deliberately inefficient implementation of a) LFSR to exercise the CPU, as part of its noise generation. The inner loop shifts the LFSR 64 times;the outer loop repeats `kernel.jitterentropy.ll`-many times. “`ll”代表“ LFSR循环”。抖动熵使用LFSR（故意低效的实现）来锻炼CPU，这是其产生噪声的一部分。内循环将LFSR移位64次；外循环重复执行“ kernel.jitterentropy.ll”多次。

In my experience, the LFSR code significantly slows down jitterentropy, but doesn't generate very much entropy. I tested this on RPi3 and qemu-arm64 with qualitatively similar results, but it hasn'tbeen tested on x86 yet. This is something to consider when tuning: using fewer LFSR loops tends tolead to better overall performance. 以我的经验，LFSR代码显着降低了抖动熵，但并没有产生太多的熵。我在RPi3和qemu-arm64上进行了测试，结果在质量上相似，但是尚未在x86上进行测试。调整时需要考虑以下事项：使用更少的LFSR环路往往会导致更好的整体性能。

Note that setting `kernel.jitterentropy.ll=0` causes jitterentropy to choose the number of LFSR loops in a "random-ish" way. As described in [the basic config doc](config-basic.md), I discouragethe use of `kernel.jitterentropy.ll=0`. 请注意，设置`kernel.jitterentropy.ll = 0'会使抖动以“随机”的方式选择LFSR循环的数量。如[基本配置文档]（config-basic.md）中所述，我不鼓励使用`kernel.jitterentropy.ll = 0'。

 

 
### [`kernel.jitterentropy.ml`](/docs/reference/kernel/kernel_cmdline.md#kernel-jitterentropy-ml-num)  [`kernel.jitterentropy.ml`]（/ docs / reference / kernel / kernel_cmdline.mdkernel-jitterentropy-ml-num） 

"`ml`" stands for "memory access loops". Jitterentropy walks through a moderately large chunk of RAM, reading and writing each byte. The size of the chunk and access pattern are controlled by thetwo parameters below. The memory access loop is repeated `kernel.jitterentropy.ml`-many times. “`ml`”代表“内存访问循环”。抖动熵遍历一个较大的RAM块，读取和写入每个字节。块的大小和访问模式由以下两个参数控制。内存访问循环多次重复执行“ kernel.jitterentropy.ml”。

In my experience, the memory access loops are a good source of raw entropy. Again, I've only tested this on RPi3 and qemu-arm64 so far. 以我的经验，内存访问循环是原始熵的良好来源。同样，到目前为止，我仅在RPi3和qemu-arm64上进行了测试。

Much like `kernel.jitterentropy.ll`, if you set `kernel.jitterentropy.ml=0`, then jitterentropy will choose a "random-ish" value for the memory access loop count. I also discourage this. 与`kernel.jitterentropy.ll`一样，如果您设置`kernel.jitterentropy.ml = 0'，则jitterentropy将为内存访问循环计数选择一个“随机的”值。我也不鼓励这样做。

 
### [`kernel.jitterentropy.bs`](/docs/reference/kernel/kernel_cmdline.md#kernel-jitterentropy-bs-num)  [`kernel.jitterentropy.bs`]（/​​ docs / reference / kernel / kernel_cmdline.mdkernel-jitterentropy-bs-num） 

"`bs`" stands for "block size". Jitterentropy divides its chunk of RAM into blocks of this size. The memory access loop starts with byte 0 of block zero, then "byte -1" of block 1 (which is actuallythe last byte of block 0), then "byte -2" of block 2 (i.e. the second-to-last byte of block 1), andso on. This pattern ensures that every byte gets hit, and most accesses go into different blocks. “`bs`”代表“块大小”。抖动将其RAM块划分为该大小的块。内存访问循环从块0的字节0开始，然后是块1的“字节-1”（实际上是块0的最后一个字节），然后是块2的“字节-2”（即倒数第二个字节）区块1），等等。这种模式可确保每个字节都被命中，并且大多数访问都进入不同的块。

I have usually tested jitterentropy with `kernel.jitterentropy.bs=64`, based on the size of a cache line. I haven't tested yet to see whether there's a better option on some/all platforms. 我通常根据缓存行的大小，使用`kernel.jitterentropy.bs = 64`测试了抖动熵。我尚未进行测试，看看在某些/所有平台上是否还有更好的选择。

 
### [`kernel.jitterentropy.bc`](/docs/reference/kernel/kernel_cmdline.md#kernel-jitterentropy-bc-num)  [`kernel.jitterentropy.bc`]（/ docs / reference / kernel / kernel_cmdline.mdkernel-jitterentropy-bc-num） 

"`bc`" stands for "block count". Jitterentropy uses this many blocks of RAM, each of size `kernel.jitterentropy.bs`, in its memory access loops. “`bc`”代表“块数”。抖动熵在其内存访问循环中使用了这么多RAM块，每个块的大小为kernel.jitterentropy.bs。

Since I choose `kernel.jitterentropy.bs=64`, I usually choose `kernel.jitterentropy.bc=1024`. This means using 64KB of RAM, which is enough to overflow L1 cache. 因为我选择`kernel.jitterentropy.bs = 64`，所以我通常选择`kernel.jitterentropy.bc = 1024`。这意味着使用64KB的RAM，足以溢出L1缓存。

The [jitterentropy source code](/zircon/third_party/lib/jitterentropy/jitterentropy-base.c#234) in the comment before `jent_memaccess` suggests choosing the block size and count so that the RAMused is bigger than L1. Confusingly, the default values in upstream jitterentropy (block size = 32,block count = 64) aren't big enough to overflow L1. “ jent_memaccess”之前的注释中的[jitterentropy源代码]（/ zircon / third_party / lib / jitterentropy / jitterentropy-base.c234）建议选择块大小和计数，以使RAMus大于L1。令人困惑的是，上游抖动熵的默认值（块大小= 32，块计数= 64）不足以溢出L1。

 
## Tuning process  调整过程 

The basic idea is simple: on a particular target device, try different values for the parameters. Collect a large amount of data for each parameter set (ideally around 1MB), then[run the NIST test suite to analyze the data](/docs/development/testing/entropy_quality_tests.md#running-the-nist-test-suite).Determine which parameters give the best entropy per unit time. The time taken to draw the entropysamples is logged on the system under test. 基本思想很简单：在特定的目标设备上，尝试使用不同的参数值。为每个参数集收集大量数据（理想情况下约为1MB），然后[运行NIST测试套件以分析数据]（/ docs / development / testing / entropy_quality_tests.mdrunning-the-nist-test-suite）。哪些参数可以提供单位时间的最佳熵。提取熵样本所需的时间记录在被测系统上。

One complication is the startup testing built into jitterentropy. This essentially draws and discards 400 samples, after performing some basic analysis (mostly making sure that the clock ismonotonic and has a high enough resolution and variability). A more accurate test would reboot twicefor each set of parameters: once to collect around 1MB of data for analysis, and a second time toboot with the "right" amount of entropy (as computed according to the entropy estimate in the firstphase, with appropriate safety margins, etc. See["Determining the entropy\_per\_1000\_bytes statistic"](#determining-the-entropy_per_1000_bytes-statistic),below). This second phase of testing simulates a real boot, including the startup tests. Aftercompleting the second phase, choose the parameter set that boots fastest. Of course, each phase oftesting should be repeated a few times to reduce random variations. 一种复杂的情况是抖动熵内置的启动测试。在执行一些基本分析（主要确保时钟是单调的并且具有足够高的分辨率和可变性）之后，这实际上将抽取并丢弃400个样本。更加精确的测试将为每个参数集重新启动两次：一次是收集大约1MB的数据以进行分析，第二次是使用“正确的”熵（根据第一阶段的熵估计计算出的，具有适当的安全性）进行引导边距等。请参见[“确定熵\ _per \ _1000 \ _bytes统计信息”]（确定下面的entropy_per_1000_bytes统计信息）。测试的第二阶段模拟了实际的启动，包括启动测试。完成第二阶段后，选择启动最快的参数集。当然，测试的每个阶段应重复几次以减少随机变化。

 
## Determining the entropy\_per\_1000\_bytes statistic  确定熵\ _per \ __ 1000 \ _bytes统计信息 

The `crypto::entropy::Collector` interface in [kernel/lib/crypto/include/lib/crypto/entropy/collector.h](/zircon/kernel/lib/crypto/include/lib/crypto/entropy/collector.h)requires a parameter `entropy_per_1000_bytes` from its instantiations. The value relevant tojitterentropy is currently hard-coded in[kernel/lib/crypto/entropy/jitterentropy\_collector.cpp](/zircon/kernel/lib/crypto/entropy/jitterentropy_collector.cc).This value is meant to measure how much min-entropy is contained in each byte of data produced byjitterentropy (since the bytes aren't independent and uniformly distributed, this will be less than8 bits). The "per 1000 bytes" part simply makes it possible to specify fractional amounts ofentropy, like "0.123 bits / byte", without requiring fractional arithmetic (since `float` isdisallowed in kernel code, and fixed-point arithmetic is confusing). [kernel / lib / crypto / include / lib / crypto / entropy / collector.h]（/ zircon / kernel / lib / crypto / include / lib / crypto / entropy / collector中的`crypto :: entropy :: Collector`接口.h）从实例化中获取参数`entropy_per_1000_bytes`。与抖动熵相关的值当前被硬编码在[kernel / lib / crypto / entropy / jitterentropy \ _collector.cpp]（/ zircon / kernel / lib / crypto / entropy / jitterentropy_collector.cc）中。该值用于测量多少最小熵包含在由抖动熵产生的数据的每个字节中（由于字节不是独立的并且不是均匀分布的，因此它将少于8位）。 “每1000字节”部分仅需要指定小数的熵，例如“ 0.123位/字节”，而无需小数运算（因为内核代码中不允许使用“ float”，并且定点运算令人困惑）。

The value should be determined by using the NIST test suite to analyze random data samples, as described in[the entropy quality tests document](/docs/development/testing/entropy_quality_tests.md#running-the-nist-test-suite).The test suite produces an estimate of the min-entropy; repeated tests of the same RNG have (in myexperience) varied by a few tenths of a bit (which is pretty significant when entropy values can bearound 0.5 bits per byte of data!). After getting good, consistent results from the test suites,apply a safety factor (i.e. divide the entropy estimate by 2), and update the value of`entropy_per_1000_bytes` (don't forget to multiply by 1000). 如[熵质量测试文档]（/ docs / development / testing / entropy_quality_tests.mdrunning-the-nist-test-suite）中所述，应使用NIST测试套件分析随机数据样本来确定该值。套件产生最小熵的估计；对同一个RNG的重复测试（以我的经验）变化了十分之几（当熵值大约为每字节数据0.5位时，这是非常重要的！）。在从测试套件中获得良好，一致的结果后，应用安全系数（即，将熵估算值除以2），并更新“ entropy_per_1000_bytes”的值（请不要忘记乘以1000）。

Note that eventually `entropy_per_1000_bytes` should probably be configured somewhere instead of hard-coded in jitterentropy\_collector.cpp. Kernel cmdlines or even a preprocessor symbol could work. 注意，最终应该在某个地方配置“ entropy_per_1000_bytes”，而不是在jitterentropy \ _collector.cpp中进行硬编码。内核cmdlines甚至预处理器符号都可以工作。

 
## Notes about the testing script  关于测试脚本的注释 

The `scripts/entropy-test/jitterentropy/test-tunable` script automates the practice of looping through a large test matrix. The downside is that tests run in sequence on a single machine, so (1)an error will stall the test pipeline so supervision *is* required, and (2) the machine is beingconstantly rebooted rather than cold-booted (plus it's a netboot-reboot), which could conceivablyconfound the tests. Still, it beats hitting power-off/power-on a thousand times by hand! 脚本/熵测试/抖动熵/测试可调脚本可自动执行遍历大型测试矩阵的操作。缺点是测试是在一台机器上按顺序运行，因此（1）错误将使测试管道停顿，因此需要进行监督*（2）机器正在不断地重新引导而不是冷引导（加上它是网络引导） -reboot），可能会混淆测试。尽管如此，它还是要比手动关闭电源/打开电源快一千次！

Some happy notes:  一些快乐的笔记：

 
1. When netbooting, the script leaves bootserver on while waiting for netcp to successfully export the data file. If the system hangs, you can power it off and back on, and the existing bootserverprocess will restart the failed test. 1.在进行netbooting时，该脚本将在等待netcp成功导出数据文件的同时使bootserver保持打开状态。如果系统挂起，则可以关闭电源然后再打开，现有的bootserver进程将重新启动失败的测试。

 
2. If the test is going to run (say) 16 combinations of parameters 10 times each, it will go like this: 2.如果测试要运行（比如说）16个参数组合（每次10次），它将像这样：

       test # 0: ml = 1   ll = 1  bc = 1  bs = 1 test # 1: ml = 1   ll = 1  bc = 1  bs = 64test # 2: ml = 1   ll = 1  bc = 32 bs = 1test # 3: ml = 1   ll = 1  bc = 32 bs = 64...test #15: ml = 128 ll = 16 bc = 32 bs = 64test #16: ml = 1   ll = 1  bc = 1  bs = 1test #17: ml = 1   ll = 1  bc = 1  bs = 64... 测试0：ml = 1 ll = 1 bc = 1 bs = 1测试1：ml = 1 ll = 1 bc = 1 bs = 64测试2：ml = 1 ll = 1 bc = 32 bs = 1测试3：ml = 1 ll = 1 bc = 32 bs = 64 ...测试15：ml = 128 ll = 16 bc = 32 bs = 64test 16：ml = 1 ll = 1 bc = 1 bs = 1test 17：ml = 1 ll = 1 bc = 1 bs = 64 ...

   (The output files are numbered starting with 0, so I started with 0 above.)  （输出文件从0开始编号，因此我从上面的0开始。）

   So, if test #17 fails, you can delete tests #16 and #17, and re-run 9 more iterations of each test. You can at least keep the complete results from the first iteration. In theory, the testscould be smarter and also keep the existing result from test #16, but the current shell scriptsaren't that sophisticated. 因此，如果测试17失败，则可以删除测试16和17，然后重新运行每个测试的9个迭代。您至少可以保留第一次迭代中的完整结果。从理论上讲，测试可能会更聪明，并且可以保留测试16中的现有结果，但是当前的shell脚本并没有那么复杂。

The scripts don't do a two-phase process like I suggested in the ["Tuning process"](#tuning-process) section above. It's certainly possible, but again the existing scripts aren't that sophisticated. 脚本没有像我在上面的““调整过程”]（调整过程）一节中建议的那样执行两阶段过程。当然有可能，但是现有的脚本并不那么复杂。

 
## Open questions  公开问题 

 
### How much do we trust the low-entropy extreme?  我们有多相信低熵的极端？ 

It's *a priori* possible that we maximize entropy per unit time by choosing small parameter values. Most extreme is of course `ll=1, ml=1, bs=1, bc=1`, but even something like `ll=1, ml=1, bs=64,bc=32` is an example of what I'm thinking of.  Part of the concern is the variability in the testsuite: if hypothetically the tests are only accurate to within 0.2 bits of entropy per byte, and ifthey're reporting 0.15 bits of entropy per byte, what do we make of it? Hopefully running the sametest a few hundred times in a row will reveal a clear modal value, but it's still a little bit riskyto rely on that low estimate to be accurate. 通过选择较小的参数值，有可能先验地使单位时间的熵最大化。当然，最极端的是“ ll = 1，ml = 1，bs = 1，bc = 1”，但是即使像“ ll = 1，ml = 1，bs = 64，bc = 32”一样，这也是我的一个例子在想。令人担忧的部分是测试套件的可变性：如果假设测试仅在每字节熵0.2位的范围内准确，并且如果报告的每字节熵0.15位，我们怎么做？希望连续运行数百次相同的测试将揭示一个明确的模态值，但是依靠该较低的估计值来准确仍然有些冒险。

The NIST publication states (line 1302, page 35, second draft) that the estimators "work well when the entropy-per-sample is greater than 0.1". This is fairly low, so hopefully it isn't an issue inpractice. Still, the fact that there is a lower bound means we should probably leave a fairlyconservative envelope around it. NIST出版物指出（第35页第1302行，第二稿），估计器“当每个样本的熵大于0.1时工作良好”。这是相当低的，所以希望这不是实践中的问题。仍然存在下界这一事实意味着我们可能应该在其周围保留一个相当保守的信封。

 
### How device-dependent is the optimal choice of parameters?  参数的最佳选择如何与设备相关？ 

There's evidently a significant difference in the actual "bits of entropy per byte" metric on different architectures or different hardware. Is it possible that most systems are optimal atsimilar parameter values (so that we can just hard-code these values into`kernel/lib/crypto/entropy/jitterentropy_collector.cpp`? Or, do we need to put the parameters intoMDI or into a preprocessor macro, so that we can use different defaults on a per-platform basis (orwhatever level of granularity is appropriate). 在不同的体系结构或不同的硬件上，实际的“每字节熵位数”度量标准显然存在显着差异。多数系统是否有可能在相似的参数值上达到最佳状态（因此我们可以将这些值硬编码到“ kernel / lib / crypto / entropy / jitterentropy_collector.cpp”中？还是需要将参数放入MDI或预处理器宏，这样我们就可以在每个平台上使用不同的默认值（无论粒度级别如何）。

 
### Can we even record optimal parameters with enough granularity?  我们甚至可以记录具有足够粒度的最佳参数吗？ 

I mentioned it above, but one of our targets is "x86", which is what runs on any x86 PC. Naturally, x86 PCs can very quite a bit. Even if we did something like add preprocessor symbolslike `JITTERENTROPY_LL_VALUE` etc. to the build, customized in `kernel/project/target/pc-x86.mk`,could we pick a good value for *all PCs*? 我在上面提到过，但是我们的目标之一是“ x86”，它是在任何x86 PC上运行的目标。自然，x86 PC可以发挥很多作用。即使我们做了一些类似的事情，例如在内核/项目/目标/pc-x86.mk中自定义添加了诸如JITTERENTROPY_LL_VALUE等预处理器符号到构建中，我们是否也可以为*所有PC *选择一个合适的值？

If not, what are our options?  如果没有，我们有什么选择？

 
1. We could store a lookup table based on values accessible at runtime (like the exact CPU model, the core memory size, cache line size, etc.). This seems rather unwieldy. Maybe if we could findone or two simple properties to key off of, say "CPU core frequency" and "L1 cache size", wecould make this relatively non-terrible. 1.我们可以基于在运行时可访问的值（例如确切的CPU模型，核心内存大小，缓存行大小等）存储查找表。这似乎很笨拙。也许如果我们可以找到一个或两个简单的属性来禁用它们，例如“ CPU核心频率”和“ L1高速缓存大小”，我们可以使它相对不可怕。

 
2. We could try an adaptive approach: monitor the quality of the entropy stream, and adjust the parameters according on the fly. This would take a lot of testing and justification if we want totrust it. 2.我们可以尝试一种自适应方法：监视熵流的质量，并根据需要实时调整参数。如果我们要信任它，将需要大量的测试和证明。

 
