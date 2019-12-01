 
# Jitterentropy: basic configuration  抖动：基本配置 

The jitterentropy library is written by Stephan Mueller, is available at <https://github.com/smuellerDD/jitterentropy-library>, and is documented at<http://www.chronox.de/jent.html>. In Zircon, it's used as a simple entropysource to seed the system CPRNG. 抖动熵库由Stephan Mueller编写，可从<https://github.com/smuellerDD/jitterentropy-library>获得，并在<http://www.chronox.de/jent.html>上进行记录。在Zircon中，它用作简单的熵源，为系统CPRNG注入了种子。

This document describes and analyzes two (independent) configuration options of jitterentropy: 本文档描述并分析了抖动的两个（独立）配置选项：

 
1. Whether to use a variable, pseudorandom number of iterations in the noise generating functions. 1.是否在噪声生成函数中使用可变的伪随机迭代次数。
2. Whether to post-process the raw noise samples with jitterentropy's internal processing routines. 2.是否使用抖动的内部处理例程对原始噪声样本进行后处理。

I consider these basic configuration options because the affect the basic process that jitterentropy uses. I'm contrasting them to tunable parameters(like the precise value used for loop counts if they are not chosenpseudorandomly, or the size of the scratch memory used internal byjitterentropy), since the tunable parameters don't greatly affect the means bywhich jitterentropy collects entropy, just the amount it collects and the timeit takes. 我考虑这些基本配置选项，因为这会影响抖动熵使用的基本过程。我将它们与可调参数进行对比（例如，如果不是随机选择的，则用于循环计数的精确值，或者内部抖动抖动所使用的暂存存储器的大小），因为可调参数不会极大地影响抖动熵收集熵的方式，只是收集的金额和时间。

My full conclusions are at the end of this document, but in summary I think that we should avoid both choosing pseudorandom iteration numbers and using thejitterentropy post-processed data. 我的完整结论在本文结尾处，但是总之，我认为我们应该避免选择伪随机迭代数和使用抖动熵后处理数据。

[TOC]  [目录]

 
## Brief explanation of jitterentropy  抖动熵的简要说明 

The author's documentation is available in HTML form at <http://www.chronox.de/jent/doc/CPU-Jitter-NPTRNG.html>, or in PDF form at<http://www.chronox.de/jent/doc/CPU-Jitter-NPTRNG.pdf>. In brief, the librarycollects random bits from variations in CPU instruction timing. 在<http://www.chronox.de/jent/doc/CPU-Jitter-NPTRNG.html>上可以HTML形式获得作者的文档，在<http://www.chronox.de/jent上可以PDF形式获得作者的文档。 /doc/CPU-Jitter-NPTRNG.pdf>。简而言之，该库从CPU指令时序的变化中收集随机位。

Jitterentropy maintains a random state, in the form of a 64-bit number that is affected by many of the jitterentropy functions, and ultimately is used as theoutput randomness. 抖动熵以64位数字的形式保持随机状态，该状态受许多抖动函数的影响，最终被用作输出随机性。

There are two noise sources, both of which are blocks of relatively slow-running code whose precise runtime is measured (using a system clock, requiring roughlynanosecond resolution). The precise time to complete these blocks of code willvary. We test these times to ensure that they are unpredictable; while we can'tbe perfectly certain that they are, the test results (including the resultsbelow) are encouraging. Note however that the purpose of this document is not tojustify our estimates for the min-entropy in jitterentropy samples, but ratherto discuss the two configuration options listed above. 有两个噪声源，这两个噪声源都是运行速度相对较慢的代码块，它们的精确运行时间被测量（使用系统时钟，需要大约纳秒的分辨率）。完成这些代码块的确切时间将有所不同。我们测试这些时间以确保它们是不可预测的；虽然我们不能完全确定它们是，但测试结果（包括下面的结果）令人鼓舞。但是请注意，本文档的目的不是为了调整我们对抖动熵样本中的最小熵的估计，而是要讨论上面列出的两个配置选项。

The first of the code blocks used as a noise source is a CPU-intensive LFSR loop, implemented in[the `jent_lfsr_time` function](/zircon/third_party/lib/jitterentropy/jitterentropy-base.c#185).The number of times the LFSR logic is repeated is controlled by the`kernel.jitterentropy.ll` cmdline ("`ll`" stands for "LFSR loops"). If `ll = 0`,a pseudorandom count is used, and otherwise the value of `ll` is used.Looking at the source code, the outer loop repeats according to the `ll`parameter.  The inner loop advances an LFSR by 64 steps, each time XOR-ing inone bit from the most recent time sample. Passing the time sample through theLFSR this way serves as a processing step, generally tending to whiten therandom timesteps. As described in the[entropy quality testing doc](/docs/development/testing/entropy_quality_tests.md), it's important toskip this processing when testing the entropic content of the CPU timevariations.  It's also the case that enabling the processing increases theentropy estimates by a suspicious amount in some cases (see[the "Effects of processing the raw samples" section](#effects-of-processing-the-raw-samples)). 用作噪声源的第一个代码块是CPU密集型LFSR循环，在[jent_lfsr_time函数]（/ zircon / third_party / lib / jitterentropy / jitterentropy-base.c185）中实现。由kernel.jitterentropy.ll命令行控制LFSR逻辑的重复（“ ll”代表“ LFSR循环”）。如果ll = 0，则使用伪随机计数，否则使用ll的值。查看源代码，外循环根据ll参数重复。内循环将LFSR推进64步，每次对最新时间样本的一位进行XOR运算。以这种方式将时间样本传递通过LFSR充当处理步骤，通常趋向于使随机时间步长变白。如[熵质量测试文档]（/ docs / development / testing / entropy_quality_tests.md）中所述，在测试CPU时间变化的熵内容时，跳过此处理很重要。在某些情况下，启用处理也会使熵估计值增加可疑的数量（请参阅[“处理原始样本的效果”部分]（原始样本的处理效果））。

The second noise source is a memory access loop, in [the `jent_memaccess` function](/zircon/third_party/lib/jitterentropy/jitterentropy-base.c#261).The memory access loop is repeated according to the `kernel.jitterentropy.ml`cmdline ("`ml`" for "memory loops"), where again a value of 0 activates thepseudorandom loop count, and any non-zero value overrides the pseudorandomcount. Each iteration of the actual memory access loop both reads and writes arelatively large chunk of memory, divided into `kernel.jitterentropy.bc`-manyblocks of size `kernel.jitterentropy.bs` bytes each. The default values when Iwrote the current document are `bc = 1024` and `bs = 64`; up-to-date defaultsshould be documented in[the cmdline document](/docs/reference/kernel/kernel_cmdline.md). For comparison, the defaults inthe jitterentropy source code are `bc = 64` and `bs = 32`,[defined here](/zircon/third_party/lib/jitterentropy/include/lib/jitterentropy/jitterentropy.h#79).Per the comment above the `jent_memaccess` function, the total memory sizeshould be larger than the L1 cache size of the target machine. Confusingly,`bc = 64` and `bs = 32` produce a memory size of 2048 bytes, which is muchsmaller than even most L1 caches (I couldn't find any CPU with more than 0 bytesbut less than 4KB of L1). Using `bs = 64` and `bc = 1024` result in 64KB ofmemory, which is usually enough to overflow L1 data caches. 第二个噪声源是[jent_memaccess]函数中的内存访问循环（/zircon/third_party/lib/jitterentropy/jitterentropy-base.c261）。根据`kernel.jitterentropy.ml'重复进行内存访问循环。 cmdline（“ ml”表示“内存循环”），其中值0再次激活伪随机循环计数，任何非零值都将覆盖伪随机计数。实际内存访问循环的每次迭代都读取和写入相对较大的内存块，分为“ kernel.jitterentropy.bc”-每个大小为“ kernel.jitterentropy.bs”字节的块。写当前文档时的默认值为bc = 1024和bs = 64。最新的默认值应记录在[cmdline文档]（/ docs / reference / kernel / kernel_cmdline.md）中。为了进行比较，抖动熵源代码中的默认值为“ bc = 64”和“ bs = 32”，[在此定义]（/ zircon / third_party / lib / jitterentropy / include / lib / jitterentropy / jitterentropy.h79）。在“ jent_memaccess”函数上方，总内存大小应大于目标计算机的L1缓存大小。令人困惑的是，“ bc = 64”和“ bs = 32”产生的内存大小为2048字节，甚至比大多数L1高速缓存都小得多（我找不到任何CPU的字节数大于0但小于4KB的L1）。使用bs = 64和bc = 1024将产生64KB的内存，通常足以溢出L1数据高速缓存。

 
### Option 1: Pseudorandom loop counts  选项1：伪随机循环计数 

Jitterentropy was originally designed so that the two noise generating functions run a pseudorandom number of times. Specifically,[the `jent_loop_shuffle` function](/zircon/third_party/lib/jitterentropy/jitterentropy-base.c#125)mixes together (1) the time read from the high-resolution clock and (2)jitterentropy's internal random state in order to decide how many times to runthe noise sources. 最初设计了抖动熵，以便两个噪声生成函数运行伪随机次数。具体来说，[jent_loop_shuffle`函数]（/ zircon / third_party / lib / jitterentropy / jitterentropy-base.c125）将（1）从高分辨率时钟读取的时间和（2）抖动熵的内部随机状态混合在一起，以便确定运行噪声源的次数。

We added the ability to override these pseudorandom loop counts, and tested jitterentropy's performance both with and without the override. The results arediscussed in more depth in[the "Effects of pseudorandom loop counts" section](#effects-of-pseudorandom-loop-counts),but in summary: the statistical tests suggested that the pseudorandom loopcounts increased the entropy far more than expected.  This makes me mistrustthese higher entropy counts, so I recommend using the lower estimates andpreferring deterministic loop counts to pseudorandom. 我们增加了覆盖这些伪随机循环计数的功能，并测试了有无覆盖情况下的抖动熵性能。结果在“伪随机循环计数的影响”部分（伪随机循环计数的影响）中进行了更深入的讨论，但总而言之：统计测试表明，伪随机循环计数增加的熵远远超过了预期。这使我对较高的熵计数不信任，因此我建议使用较低的估计值，并且将确定性循环计数推荐为伪随机数。

 
### Jitterentropy's random data processing  抖动熵的随机数据处理 

As mentioned above, jitterentropy can process its random data, which makes the data look "more random".  Specifically, the processing should decrease (andideally remove) the deviation of the random data from the uniform distribution,and reduce (ideally, remove) any intercorrelations between random bytes. 如上所述，抖动熵可以处理其随机数据，这使数据看起来“更随机”。具体而言，该处理应减小（理想地消除）随机数据与均匀分布的偏差，并减小（理想地消除）随机字节之间的任何相互关系。

The main function of interest for generating processed samples is [`jent_gen_entropy`](/zircon/third_party/lib/jitterentropy/jitterentropy-base.c#462),which is called in a loop by[`jent_read_entropy`](/zircon/third_party/lib/jitterentropy/jitterentropy-base.c#544)to produce an arbitrarily large number of random bytes.In essence, `jent_gen_entropy` calls the noise functions in a loop 64 times.Each of the 64 invocations of `jent_lfsr_time` mixes the noisy time measurementinto the jitterentropy random state. 生成处理后的样本所需的主要功能是[`jent_gen_entropy`]（/ zircon / third_party / lib / jitterentropy / jitterentropy-base.c462），它在循环中由[`jent_read_entropy`]（/ zircon / third_party / lib / jitterentropy / jitterentropy-base.c544）产生任意数量的随机字节。本质上，`jent_gen_entropy`会在循环中调用噪声函数64次。`jent_lfsr_time`的64次调用中的每一次都会将有噪声的时间测量混入抖动熵随机状态。

After these 64 iterations, the random state is optionally "stirred" in [`jent_stir_pool`](/zircon/third_party/lib/jitterentropy/jitterentropy-base.c#403)by XOR-ing with a "mixer" value, itself dependent on the jitterentropy randomstate. As noted in the source code, this operation cannot increase or decreasethe entropy in the pool (since XOR is bijective), but it can potentially improvethe statistical appearance of the random state. 在这64次迭代之后，可以通过与[mixer]值进行XOR运算，在[`jent_stir_pool`]（/ zircon / third_party / lib / jitterentropy / jitterentropy-base.c403）中随意“搅拌”随机状态，该值取决于抖动熵随机状态。如源代码中所述，此操作不能增加或减小池中的熵（因为XOR是双射的），但是可以潜在地改善随机状态的统计外观。

In principle, invoking the noise source functions 64 times should produce 64 times as much entropy, up to the maximum 64 bits that the random state can hold.This assumes that the mixing operation in `jent_lfsr_time` is cryptographicallysound. I'm not an expert in cryptanalysis, but a LFSR itself is not acryptographically secure RNG, since 64 successive bits reveal the entire stateof a 64-bit LFSR, after which all past and future values can be easilycomputed. I am not sure that the jitterentropy scheme &mdash; XOR-ing the timemeasurement into the "bottom" of the LFSR as the LFSR is shifted &mdash; is moresecure. Without careful cryptographic examination of this scheme (which for allI know may exist, but the I did not see it mentioned in the jitterentropydocumentation), I would lean towards using unprocessed samples, and mixing theminto our system entropy pool in a known-good way (e.g. SHA-2, as we do now). 原则上，调用噪声源函数64次应产生64倍的熵，最多可以产生随机状态可以容纳的64位。这假设jent_lfsr_time中的混合操作是加密声音。我不是密码分析专家，但是LFSR本身并不是加密安全的RNG，因为64个连续位揭示了64位LFSR的整个状态，之后可以轻松计算所有过去和将来的值。我不确定抖动熵方案是否正确；当LFSR移位时，将时间测量异或到LFSR的“底部”；更安全。如果不对此方案进行仔细的密码检查（我所知道的可能全部存在，但是我在抖动熵文档中没有看到它），我倾向于使用未处理的样本，并将其以已知的好方法混合到我们的系统熵池中（例如SHA-2，就像我们现在所做的那样。

That said, I did run the NIST test suite against processed data samples. My results are in[the "Effects of processing the raw samples" section](#effects-of-processing-the-raw-samples))below. 也就是说，我确实针对处理过的数据样本运行了NIST测试套件。我的结果在下面的“处理原始样本的效果”部分中（原始样本的处理效果）。

 
## Testing process  测试过程 

The procedure for running entropy source quality tests is documented in [the entropy quality tests document](/docs/development/testing/entropy_quality_tests.md). 运行熵源质量测试的过程记录在[熵质量测试文档]（/ docs / development / testing / entropy_quality_tests.md）中。

These preliminary results were gathered on a Zircon debug build on Raspberry Pi  这些初步结果收集在基于Raspberry Pi的Zircon调试版本中
3, built from commit 18358de5e90a012cb1e042efae83f5ea264d1502 in the now-obsolete project: https://fuchsia.googlesource.com/zircon/+/a1a80a6a7d "\[virtio]\[entropy] Basic virtio-rng driver". The following flags were set inmy `local.mk` file when building: 3，从已过时的项目中的提交18358de5e90a012cb1e042efae83f5ea264d1502构建：https://fuchsia.googlesource.com/zircon/+/a1a80a6a7d“ \ [virtio] \ [entropy] Basic virtio-rng驱动程序”。构建时，在我的`local.mk`文件中设置了以下标志：

```
ENABLE_ENTROPY_COLLECTOR_TEST=1
ENTROPY_COLLECTOR_TEST_MAXLEN=1048576
```
 

I ran the boot-time tests after netbooting the debug kernel on the Pi with the following kernel cmdline, varying the values of `$ML`, `$LL`, and `$RAW`: 我使用以下内核cmdline在Pi上对Boot调试内核进行了网络引导之后，运行了引导时间测试，并更改了$ ML，$ LL和$ RAW的值：

```
kernel.entropy-test.src=jitterentropy
kernel.jitterentropy.bs=64
kernel.jitterentropy.bc=1024
kernel.jitterentropy.ml=$ML
kernel.jitterentropy.ll=$LL
kernel.jitterentropy.raw=$RAW
```
 

 
## Test results and analysis  测试结果与分析 

 
### Effects of pseudorandom loop counts  伪随机循环计数的影响 

 
#### Raw Data  原始数据 

Following the logic in the jitterentropy source code (search for [`MAX_FOLD_LOOP_BIT`](/zircon/third_party/lib/jitterentropy/jitterentropy-base.c#191)and[`MAX_ACC_LOOP_BIT`](/zircon/third_party/lib/jitterentropy/jitterentropy-base.c#265))the pseudorandom loop counts vary within these ranges: 遵循抖动熵源代码中的逻辑（搜索[`MAX_FOLD_LOOP_BIT`]（/ zircon / third_party / lib / jitterentropy / jitterentropy-base.c191）和[`MAX_ACC_LOOP_BIT`]（/ zircon / third_party / lib / jitterentropy / jitterentropy- base.c265））伪随机循环计数在以下范围内变化：

```
ml: 1 .. 128 (inclusive)
ll: 1 .. 16 (inclusive)
```
 

I have included the overall min-entropy estimate from the NIST suite in this table, as well as two contributing estimates: the compression estimate and theMarkov estimate. The NIST min-entropy estimate is the minimum of 10 differentestimates, including these two. The compression estimate is generally thesmallest for jitterentropy raw samples with deterministic loop counts, and theMarkov estimate is generally smallest for jitterentropy with otherconfigurations. 我在此表中包括了NIST套件的总体最小熵估计，以及两个有用的估计：压缩估计和Markov估计。 NIST最小熵估计是10个不同估计中的最小值，包括这两个。对于具有确定性循环计数的抖动熵原始样本，压缩估计值通常是最小的，对于其他配置的抖动熵，Markov估计值通常是最小的。

| `ml`              | `ll`             | min-entropy (bits / byte) | Compression estimate | Markov estimate | |:-----------------:|:----------------:|:-------------------------:|:--------------------:|:---------------:|| random (1 .. 128) | random (1 .. 16) | 5.77                      | 6.84                 | 5.77            || 128               | 16               | 1.62                      | 1.62                 | 3.60            || 1                 | 1                | 0.20                      | 0.20                 | 0.84            | | `ml` | `ll` |最小熵（位/字节）|压缩估算|马尔可夫估计| |：-----------------：|：----------------：|：--------- ----------------：|：------------------------------------ ||：-------- -------：||随机（1 .. 128）|随机（1 .. 16）| 5.77 | 6.84 | 5.77 || 128 | 16 | 1.62 | 1.62 | 3.60 || 1 | 1 | 0.20 | 0.20 | 0.84 |

 

In other words, varying the loop counts pseudorandomly increased the min-entropy estimate for raw samples by 4.15 bits (or 250%), compared to the deterministicversion that always used the maximum values from the pseudorandom ranges. 换句话说，与始终使用伪随机范围中的最大值的确定性转换相比，改变循环计数伪随机地将原始样本的最小熵估计值提高了4.15位（或250％）。

 
#### Analysis  分析 

The pseudorandom loop count values are determined by adding one extra time sample per noise function. First, these time samples are not independent of thenoise function time measurements, since the gaps between the loop count timesamples correspond predictably to the noise function time measurements. As aresult it would be highly questionable to assume that they increase themin-entropy of the output data at all.  Second, it is absurd to imagine that theloop count time samples were somehow about 250% as random as the noise functiontime measurements, since both rely on the same noise source, except that thevery first loop count time samples maybe get a small boost from the randomamount of time needed to boot the system enough to run the test. 伪随机循环计数值是通过每个噪声函数添加一个额外的时间样本来确定的。首先，这些时间采样不独立于噪声函数时间测量，因为循环计数时间采样之间的间隙可预测地对应于噪声函数时间测量。因此，假设它们完全增加了输出数据的最小熵将是非常可疑的。其次，可以想象，循环计数时间样本的随机性大约是噪声函数时间测量值的250％，这是荒谬的，因为它们都依赖于相同的噪声源，只是每个第一次循环计数时间样本可能会从随机量中获得很小的提升引导系统所需的时间足以运行测试。

Consequently, I suspect that what happened is that the pseudorandom loop counts were enough to "fool" the particular suite of statistical tests andpredictor-based tests in the NIST suite, but that a predictor test written withspecific knowledge of how the jitterentropy pseudorandom loop counts are derivedcould in fact predict the output with far better accuracy. I think the "true"min-entropy in the pseudorandom loop count test, against an adversary that'sspecifically targeting our code, is within the bounds of the two deterministictests, i.e. between about 0.20 and 1.62 bits per byte. 因此，我怀疑发生的事情是伪随机循环计数足以“欺骗” NIST套件中的特定统计测试套件和基于预测变量的测试，但是编写的预测变量测试具有关于抖动熵伪随机循环计数的具体知识派生实际上可以以更高的精度预测输出。我认为针对专门针对我们代码的对手，伪随机循环计数测试中的“真实”最小熵在两个确定性测试的范围之内，即每字节大约0.20到1.62位。

Using pseudorandom counts forces us to make an additional decision: do we conservatively estimate the actual entropy content at 0.20 bits per byte (as ifthe pseudorandom count function always chose `ml = 1` and `ll = 1`)? Or do wechose an average entropy content (there is probably a more intelligent averagingtechnique than to compute (1.62 + 0.20) / 2 = 0.91 bits / byte, but that willserve for the purpose of this discussion) and risk the pseudorandom loop countsoccasionally causing us to undershoot this average entropy content? If we aretoo conservative, we will spend more time collecting entropy than is needed; ifwe are too optimistic, we might have a security vulnerability. Ultimately, thisforces a trade-off between security (which prefers conservative entropyestimates) and efficiency (which prefers optimistic entropy estimates). 使用伪随机计数会迫使我们做出另外一个决定：我们是否以每字节0.20位保守地估计实际的熵含量（好像伪随机计数函数总是选择“ ml = 1”和“ ll = 1”）？还是选择平均熵含量（可能有一种比计算（1.62 + 0.20）/ 2 = 0.91位/字节更智能的平均技术，但这将用于本次讨论）并冒着伪随机循环数的风险，有时使我们低于这个平均熵含量？如果我们太保守，我们将花费更多的时间来收集熵，而不是需要的时间。如果我们过于乐观，则可能存在安全漏洞。最终，这迫使安全性（偏爱保守的熵估计）和效率（偏爱乐观的熵估计）之间进行权衡。

 
### Effects of processing the raw samples  原始样品处理的影响 

 
#### Raw Data  原始数据 

I repeated the three tests reported above, but with jitterentropy's internal processing turned on (with `kernel.jitterentropy.raw = false` instead of thedefault value `true`). For convenience, the tables below include both the rawsample results (copied from above) in the top three rows, and the processedresults (newly added) in the bottom three rows. 我重复了上面报告的三个测试，但是启用了抖动熵的内部处理（使用kernel.jitterentropy.raw = false代替默认值“ true”）。为方便起见，下表在前三行中同时包含了原始样品结果（从上方复制），在后三行中还包含了处理后的结果（新添加）。

| `ml`              | `ll`             | raw   | min-entropy (bits / byte) | Compression estimate | Markov estimate | |:-----------------:|:----------------:|:-----:|:-------------------------:|:--------------------:|:---------------:|| random (1 .. 128) | random (1 .. 16) | true  | 5.77                      | 6.84                 | 5.77            || 128               | 16               | true  | 1.62                      | 1.62                 | 3.60            || 1                 | 1                | true  | 0.20                      | 0.20                 | 0.84            | | `ml` | `ll` |原料|最小熵（位/字节）|压缩估算|马尔可夫估计| |：-----------------：|：----------------：|：-----：|：- ------------------------：|：--------------------：|： ---------------：||随机（1 .. 128）|随机（1 .. 16）|真实| 5.77 | 6.84 | 5.77 || 128 | 16 |真实| 1.62 | 1.62 | 3.60 || 1 | 1 |真实| 0.20 | 0.20 | 0.84 |

| `ml`              | `ll`             | raw   | min-entropy (bits / byte) | Compression estimate | Markov estimate | |:-----------------:|:----------------:|:-----:|:-------------------------:|:--------------------:|:---------------:|| random (1 .. 128) | random (1 .. 16) | false | 5.79                      | 6.59                 | 5.79            || 128               | 16               | false | 5.78                      | 6.97                 | 5.78            || 1                 | 1                | false | 5.77                      | 6.71                 | 5.77            | | `ml` | `ll` |原料|最小熵（位/字节）|压缩估算|马尔可夫估计| |：-----------------：|：----------------：|：-----：|：- ------------------------：|：--------------------：|： ---------------：||随机（1 .. 128）|随机（1 .. 16）|错误5.79 | 6.59 | 5.79 || 128 | 16 |错误5.78 | 6.97 | 5.78 || 1 | 1 |错误5.77 | 6.71 | 5.77 |

 
#### Analysis  分析 

The post-processing min-entropy estimates are all essentially equal (up to slight variations easily explained by randomness), and also equal to themin-entropy estimate for raw samples with pseudorandom loop counts. 后处理的最小熵估计值基本上都相等（由随机性可以轻松解释的微小变化），也等于具有伪随机循环计数的原始样本的最小熵估计值。

Recall that jitterentropy's processed entropy is formed from 64 separate random data samples, mixed together in a 64-bit internal state buffer. Each of the rawsamples corresponds to a sample in the `raw = true` table. In particular, it'sabsurd to think that combining 64 samples with `ml = 1` and `ll = 1` thenprocessing these could produce (5.77 \* 8) = 46.2 bits of entropy per 8 bytes ofprocessed output, since that would imply (46.2 / 64) = 0.72 bits of entropy perunprocessed sample as opposed to the measured value of 0.20 bits. 回想一下，抖动熵的处理后的熵是由64个独立的随机数据样本组成的，这些样本在64位内部状态缓冲区中混合在一起。每个原始样本都对应于“ raw = true”表中的一个样本。特别是，我们认为将64个样本分别与“ ml = 1”和“ ll = 1”相结合然后对其进行处理，每8个字节的处理输出可产生（5.77 \ * 8）= 46.2比特的熵，这是荒谬的，因为这意味着（ 46.2 / 64）= 0.72位的熵未处理样本，而不是0.20位的测量值。

This argument applies against the `ml = 1`, `ll = 1`, `raw = false` measurement, but does *not* apply to `ml = 128`, `ll = 16`, `raw = false`. In particular,combining 64 raw samples with `ml = 128` and `ll = 16` could in principlecollect (1.64 \* 64 / 8) = 13.1 bits of entropy per processed byte, except thatof course there is a hard limit at 8 bits per byte. 该参数适用于“ ml = 1”，“ ll = 1”，“ raw = false”测量，但*不*适用于“ ml = 128”，“ ll = 16”，“ raw = false”。特别是，将64个原始样本与“ ml = 128”和“ ll = 16”组合在一起时，原则上每个处理后的字节可收集（1.64 \ * 64/8）= 13.1位熵，当然，硬限制是8位每字节。

Interestingly, the minimal entropy estimator switches from the compression estimate to the Markov estimator. My theory is that the additional "confusion"from post-processing is enough to "fool" the compression estimate. If there is acryptographic vulnerability in the jitterentropy processing routine, it may bepossible to write a similar estimator that reveals a significantly smallermin-entropy. If we use the general-purpose tests to decide how many raw samplesto collect in order to have 256 of min-entropy, but an adversary uses a targetedattack, then (relative to this targeted attack) our system may have less entropyin its entropy pool than we expect. This is a security vulnerability. 有趣的是，最小熵估计器从压缩估计切换到马尔可夫估计。我的理论是，后处理带来的额外“混乱”足以“愚弄”压缩估计。如果在抖动熵处理例程中存在加密漏洞，则可能写出一个类似的估算器来揭示最小的最小熵。如果我们使用通用测试来确定要采集多少原始样本以具有256的最小熵，而对手使用目标攻击，则（相对于此目标攻击）我们系统的熵池中的熵可能少于我们期待。这是一个安全漏洞。

If there is a very bad weakness in the jitterentropy processing routine, it may in fact be reducing the "true" entropy in jitterentropy's internal pool. Thearithmetical argument regarding `ml = 1` and `ll = 1` shows that we can't trustthe NIST test suite to accurately measure the actual min-entropy in theprocessed data, so it is possible that the processing actually reducesmin-entropy and our tools just can't detect the loss. This would exacerbate thevulnerability described in the previous paragraph. 如果在抖动熵处理例程中存在非常严重的弱点，则实际上可能会降低抖动熵内部池中的“真实”熵。关于“ ml = 1”和“ ll = 1”的算术参数表明，我们不能相信NIST测试套件可以准确测量处理后数据中的实际最小熵，因此处理实际上可能会减小最小熵和我们的工具就是无法检测到损失。这将加剧上一段中描述的漏洞。

 
## Conclusions  结论 

Jitterentropy's pseudorandom loop counts are of questionable benefit at best, and if used they force us to make a security/efficiency trade-off. Unless we canshow convincing evidence that the pseudorandom times really do drasticallyincrease entropy estimates rather than just defeating the NIST test suite, weshould use deterministic loop counts, ideally tuned for performance on aper-target basis. 抖动熵的伪随机循环计数充其量是可疑的，如果使用，它们将迫使我们进行安全性/效率的权衡。除非我们能提供令人信服的证据，证明伪随机时间确实确实在极大地增加熵估计，而不仅仅是击败NIST测试套件，否则我们应该使用确定性循环计数，理想情况下应根据目标性能调整性能。

Jitterentropy's processing is also questionable, since (to my knowledge) it hasn't been subjected to enough cryptographic analysis and testing to betrusted. Furthermore, we can't directly measure the min-entropy in thepost-processed data via the NIST test suite, so if there is a cryptographicvulnerability we can't easily detect it. I think we should instead rely on theentropy mixing code in the Zircon CPRNG (based on SHA-2), and leavejitterentropy's processing disabled. 抖动熵的处理也值得怀疑，因为（据我所知）它尚未受到足够的密码分析和测试以至于无法信任。此外，我们无法通过NIST测试套件直接测量后处理数据中的最小熵，因此，如果存在加密漏洞，我们将无法轻松地检测到它。我认为我们应该改为依靠Zircon CPRNG（基于SHA-2）中的熵混合代码，并且禁用假抖动熵的处理。

 
## TODOs  待办事项 

 
1. Repeat the tests reported above against different versions of Zircon, and ensure that the entropy estimates remain consistent. 1.对不同版本的锆石重复上述报告的测试，并确保熵估计值保持一致。
2. Repeat the tests on different platforms and targets (note: x86 targets don't currently have access to a system clock during early boot, so the early bootentropy tests and early boot CPRNG seeding don't yet support jitterentropy onx86). 2.在不同的平台和目标上重复测试（注意：x86目标当前无法在早期引导期间访问系统时钟，因此早期引导熵测试和早期引导CPRNG播种尚不支持onx86上的抖动熵）。
3. Automate the process of running the tests and generating the reports in this document. Specifically, the tests should compare: 3.自动运行测试并生成本文档中的报告的过程。具体而言，测试应进行比较：

 
   - pseudorandom loop counts versus various deterministic loop count values  -伪随机循环计数与各种确定性循环计数值
