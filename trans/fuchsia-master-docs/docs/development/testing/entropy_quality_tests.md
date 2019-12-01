 
# Entropy quality tests  熵质量测试 

This document describes how we test the quality of the entropy sources used to seed the Zircon CPRNG. 本文描述了我们如何测试用于Zircon CPRNG种子的熵源的质量。

[TOC]  [目录]

 
## Theoretical concerns  理论问题 

Approximately speaking, it's sometimes easy to tell that a stream of numbers is not random by recognizing a pattern in it. It's impossible to be sure that thenumbers are truly random. The state of the art seems to be running severalstatistical tests on the data, and hoping to detect any exploitable weaknesses. 大致来说，通过识别数字流有时可以很容易地看出数字流不是随机的。不可能确定这些数字是真正随机的。现有技术似乎正在对数据进行一些统计测试，并希望检测出任何可利用的弱点。

The problem of testing for randomness gets more difficult when the random numbers aren't perfectly random (when their distributions aren't uniform, orwhen there are some limited correlations between numbers in the sequence). Astream of non-perfect random numbers still contains some randomness, but it'shard to determine how random it is. 当随机数不是完全随机时（当它们的分布不均匀或序列中数字之间的相关性有限时），测试随机性的问题变得更加困难。非完美随机数的流仍然包含一些随机性，但是很难确定其随机性。

For our purposes, a good measure of how much randomness is contained in a stream of non-perfectly random numbers is the min-entropy. This is related to theShannon entropy used in information theory, but is always takes a smaller value.The min-entropy controls how much randomness we can reliably extract from theentropy source; see, for example<https://en.wikipedia.org/wiki/Randomness_extractor#Formal_definition_of_extractors> 出于我们的目的，最小熵是衡量非完全随机数流中包含多少随机性的一个好方法。这与信息论中使用的香农熵有关，但总是取较小的值。最小熵控制着我们可以可靠地从熵源中提取多少随机性；参见例如<https://en.wikipedia.org/wiki/Randomness_extractorFormal_definition_of_extractors>

From a practical standpoint, we can use the test suite described in US NIST SP800-90B to analyze samples of random from an entropy source. A prototypeimplementation for the tests is available from<https://github.com/usnistgov/SP800-90B_EntropyAssessment>. The suite takes asample data file (say, 1MB of random bytes) as input. The nice thing about thistest suite is that it can handle non-perfect RNGs, and it reports an estimatefor how much min-entropy is contained in each byte of the random data stream. 从实际的角度来看，我们可以使用US NIST SP800-90B中描述的测试套件来分析来自熵源的随机样本。测试的原型实现可从<https://github.com/usnistgov/SP800-90B_EntropyAssessment>获得。该套件将样本数据文件（例如1MB的随机字节）作为输入。关于此测试套件的好处是它可以处理非完美的RNG，并且可以报告随机数据流的每个字节中包含多少最小熵的估计。

 
### The importance of testing unprocessed data  测试未处理数据的重要性 

After drawing entropy from our entropy sources, we will mix it into the CPRNG in a "safe" way that basically gets rid of detectable correlations anddistributional imperfections in the raw random byte stream from the entropysource. This is a very important thing to do when actually generating randomnumbers to use, but we must avoid this mixing and processing phase when testingthe entropy source itself. 从我们的熵源中提取熵之后，我们将以“安全”的方式将其混合到CPRNG中，该方法基本上摆脱了来自熵源的原始随机字节流中可检测的相关性和分布缺陷。在实际生成要使用的随机数时，这是一件非常重要的事情，但是在测试熵源本身时，我们必须避免这种混合和处理阶段。

For a stark example of why it's important to test unprocessed data if we want to test our actual entropy sources, here's an experiment. It should run on anymodern linux system with OpenSSL installed. 举一个明显的例子，如果我们要测试实际的熵源，为什么测试未处理的数据很重要，这是一个实验。它应该在安装了OpenSSL的任何现代Linux系统上运行。

    head -c 1000000 /dev/zero >zero.bin openssl enc -aes-256-ctr -in zero.bin -out random.bin -nosalt -k "password" 头-c 1000000 / dev / zero> zero.bin openssl enc -aes-256-ctr -in零.bin -out random.bin -nosalt -k“ password”

This takes one million bytes from /dev/zero, encrypts them via AES-256, with a weak password and no salt (a terrible crypto scheme, of course!). The fact thatthe output looks like good random data is a sign that AES is working asintended, but this demonstrates the risk of estimating entropy content fromprocessed data: together, /dev/zero and "password" provide ~0 bits of entropy,but our tests are way more optimistic about the resulting data! 这会从/ dev / zero中获取一百万个字节，并通过AES-256对其进行加密，并且使用弱密码且不加盐（当然，这是一种糟糕的加密方案！）。输出看起来像是很好的随机数据这一事实表明AES正在按预期工作，但这证明了从处理后的数据估计熵含量的风险：/ dev / zero和“ password”一起提供了〜0位熵，但是我们进行了测试对结果数据更加乐观！

For a more concrete Zircon-related example, consider jitterentropy (the RNG discussed here: <http://www.chronox.de/jent/doc/CPU-Jitter-NPTRNG.html>).Jitterentropy draws entropy from variations in CPU timing. The unprocessed dataare how long it took to run a certain block of CPU- and memory-intensive code(in nanoseconds). Naturally, these time data are not perfectly random: there'san average value that they center around, with some fluctuations. Eachindividual data sample might be several bits (e.g. a 64-bit integer) but onlycontribute 1 bit or less of min-entropy. 对于与Zircon相关的更具体的示例，请考虑抖动熵（此处讨论了RNG：<http://www.chronox.de/jent/doc/CPU-Jitter-NPTRNG.html>）。抖动熵从CPU时序的变化中得出熵。 。未处理的数据是运行某个占用大量CPU和内存的代码块所花费的时间（以纳秒为单位）。当然，这些时间数据并不是完全随机的：它们周围存在一个平均值，并且会有一些波动。每个单独的数据样本可能是几位（例如64位整数），但仅贡献了1位或更少的最小熵。

The full jitterentropy RNG code takes several raw time data samples and processes them into a single random output (by shifting through a LFSR, amongother things). If we test the processed output, we're seeing apparent randomnessboth from the actual timing variations and from the LFSR. We want to focus onjust the timing variation, so we should test the raw time samples. Note thatjitterentropy's built-in processing can be turned on and off via the`kernel.jitterentropy.raw` cmdline. 完整的抖动熵RNG代码获取几个原始时间数据样本，并将它们处理为单个随机输出（通过LFSR进行移位）。如果我们测试处理后的输出，我们会从实际时序变化和LFSR中看到明显的随机性。我们要专注于调整时间变化，因此我们应该测试原始时间样本。请注意，可以通过kernel.jitterentropy.rawcmdline打开和关闭抖动熵的内置处理。

 
## Quality test implementation  质量测试实施 

As mentioned above, the NIST test suite takes a file full of random bytes as input. We collect those bytes on a Zircon system (possibly with a thin Fuchsialayer on top), then usually export them to a more capable workstation to run thetest suite. 如上所述，NIST测试套件将充满随机字节的文件作为输入。我们在Zircon系统上收集这些字节（可能在顶部带有薄的Fuchsialayer），然后通常将它们导出到功能更强大的工作站上以运行测试套件。

 
## Boot-time tests  引导时间测试 

Some of our entropy sources are read during boot, before userspace is started. To test these entropy sources in a realistic environment, we run the testsduring boot. The relevant code is in`kernel/lib/crypto/entropy/quality\_test.cpp`, but the basic idea is that thekernel allocates a large static buffer to hold test data during early boot(before the VMM is up, so before it's possible to allocate a VMO). Later on, thedata is copied into a VMO, and the VMO is passed to userboot and devmgr, whereit's presented as a pseudo-file at `/boot/kernel/debug/entropy.bin`. Userspaceapps can read this file and export the data (by copying to persistent storage orusing the network, for example). 在启动用户空间之前，会在引导过程中读取一些我们的熵源。为了在实际环境中测试这些熵源，我们在启动期间运行测试。相关的代码在`kernel / lib / crypto / entropy / quality \ _test.cpp`中，但是基本思想是内核在早期引导期间分配了一个较大的静态缓冲区来保存测试数据（在VMM启动之前，因此在启动之前）。可以分配一个VMO）。稍后，将数据复制到VMO中，并将VMO传递到userboot和devmgr，在此处以伪文件的形式显示在`/ boot / kernel / debug / entropy.bin`中。 Userspaceapps可以读取此文件并导出数据（例如，通过复制到永久性存储或使用网络）。

In theory, you should be able to build Zircon with entropy collector testing enabled using `scripts/entropy-test/make-parallel`, and then you should be ableto run a single boot-time test with the script`scripts/entropy-test/run-boot-test`. The `run-boot-test` script is mostlyintended to be invoked by other scripts, so it's a little bit rough around theedges (for example, most of its arguments are passed via command line optionslike `-a x86-64`, but many of these "options" are in fact mandatory). 从理论上讲，您应该能够使用`scripts / entropy-test / make-parallel`启用熵收集器测试来构建Zircon，然后应该能够使用scripts / entropy-test脚本运行单个引导时间测试/ run-boot-test`。 `run-boot-test`脚本主要旨在由其他脚本调用，因此在边缘处有点粗糙（例如，其大多数参数都是通过命令行选项传递的，例如-a x86-64，但是很多这些“选项”实际上是强制性的）。

Assuming the `run-boot-test` script succeeds, it should produce two files in the output directory: `entropy.000000000.bin` and `entropy.000000000.meta`. Thefirst is the raw data collected from the entropy source, and the second is asimple text file, where each line is a key-value pair. The keys are single wordsmatching `/[a-zA-Z0-9_-]+/`, and the values are separated by whitespace matching`/[ \t]+/`. This file can be pretty easily parsed via `read` in Bash,`str.split()` in Python, or (with the usual caution about buffer overruns)`scanf` in C. 假设“ run-boot-test”脚本成功执行，它将在输出目录中生成两个文件：“ entropy.000000000.bin”和“ entropy.000000000.meta”。第一个是从熵源收集的原始数据，第二个是asimple文本文件，其中每一行都是键值对。键是单字匹配`/ [a-zA-Z0-9 _-] + /`，并且值由空格匹配`/ [\ t] + /`隔开。通过Bash中的read或Python中的str.split（）或C语言中的scanf，可以很容易地解析该文件。

In practice, I'm nervous about bit-rot in these scripts, so the next couple sections document what the scripts are supposed to do, to make it easier to runthe tests manually or fix the scripts if/when they break. 在实践中，我担心这些脚本中的位腐烂，因此接下来的几节记录了脚本应该执行的操作，以使手动运行测试或在脚本损坏时更容易进行修复。

 
### Boot-time tests: building  引导时间测试：构建 

Since the boot-time entropy test requires that a large block of memory be permanently reserved (for the temporary, pre-VMM buffer), we don't usually buildthe entropy test mode into the kernel. The tests are enabled by passing the`ENABLE_ENTROPY_COLLECTOR_TEST` flag at build time, e.g. by adding the line 由于引导时熵测试要求永久保留一大块内存（用于VMM之前的临时缓冲区），因此我们通常不将熵测试模式构建到内核中。在构建时通过传递ENABLE_ENTROPY_COLLECTOR_TEST标志来启用测试。通过添加线

```
EXTERNAL_DEFINES += ENABLE_ENTROPY_COLLECTOR_TEST=1
```
 

to `local.mk`. Currently, there's also a build-time constant, `ENTROPY_COLLECTOR_TEST_MAXLEN`, which (if provided) is the size of thestatically allocated buffer. The default value if unspecified is 1MiB. 到`local.mk`。当前，还有一个构建时常量“ ENTROPY_COLLECTOR_TEST_MAXLEN”，（如果提供的话）是静态分配缓冲区的大小。如果未指定，则默认值为1MiB。

 
### Boot-time tests: configuring  引导时间测试：配置 

The boot-time tests are controlled via kernel cmdlines. The relevant cmdlines are `kernel.entropy-test.*`, documented in[kernel\_cmdline.md](/docs/reference/kernel/kernel_cmdline.md). 引导时间测试是通过内核cmdlines控制的。相关的cmdline是“ kernel.entropy-test。*”，记录在[kernel \ _cmdline.md]（/ docs / reference / kernel / kernel_cmdline.md）中。

Some entropy sources, notably jitterentropy, have parameter values that can be tweaked via kernel cmdline. Again, see [kernel\_cmdline.md](/docs/reference/kernel/kernel_cmdline.md)for further details. 一些熵源，特别是抖动熵，具有可以通过内核cmdline进行调整的参数值。再次，请参阅[kernel \ _cmdline.md]（/ docs / reference / kernel / kernel_cmdline.md）了解更多详细信息。

 
### Boot-time tests: running  引导时间测试：正在运行 

The boot-time tests will run automatically during boot, as long as the correct kernel cmdlines are passed (if there are problems with the cmdlines, errormessages will be printed instead). The tests run just before the first stage ofRNG seeding, which happens at LK\_INIT\_LEVEL\_PLATFORM\_EARLY, shortly beforethe heap the VMM are brought up. If running a large test, boot will often slowdown noticeably. For example, collecting 128kB of data from jitterentropy onrpi3 can take around a minute, depending on the parameter values. 只要通过了正确的内核cmdlines，引导时测试就会在引导过程中自动运行（如果cmdlines存在问题，则会打印错误消息）。这些测试恰好在RNG播种的第一阶段之前进行，该阶段发生在LK​​ \ _INIT \ _LEVEL \ _PLATFORM \ _EARLY，即在提起VMM之前不久。如果运行大型测试，启动通常会明显减慢速度。例如，根据参数值，从抖动熵onrpi3收集128kB数据可能需要一分钟左右。

 
## Run-time tests  运行时测试 

*TODO(SEC-29): discuss actual user-mode test process*  * TODO（SEC-29）：讨论实际的用户模式测试过程*

*Current rough ideas: only the kernel can trigger hwrng reads. To test, userspace issues a kernel command (e.g. `k hwrng test`), with some arguments tospecify the test source and length. The kernel collects random bytes into theexisting VMO-backed pseudo-file at `/boot/kernel/debug/entropy.bin`, assumingthat this is safely writeable. Currently unimplemented; blocked by lack of auserspace HWRNG driver. Can test the VMO-rewriting mechanism first.* *当前的粗略想法：只有内核才能触发hwrng读取。为了测试，用户空间发出了内核命令（例如`k hwrng test`），并带有一些参数来指定测试源和长度。假设此文件是安全可写的，内核会在/boot/kernel/debug/entropy.bin处将随机字节收集到现有VMO支持的伪文件中。目前尚未实现；由于缺少用户空间HWRNG驱动程序而被阻止。可以先测试VMO重写机制。*

 
## Test data export  测试数据导出 

Test data is saved in `/boot/kernel/debug/entropy.bin` in the Zircon system under test. So far I've usually exported the data file manually via `netcp`.Other options include `scp` if you build with the correct Fuchsia packages, orsaving to persistent storage. 测试数据保存在被测Zircon系统的`/ boot / kernel / debug / entropy.bin`中。到目前为止，我通常是通过`netcp`手动导出数据文件的，其他选项包括`scp`如果您使用正确的Fuchsia软件包进行构建，或者保存到持久存储中。

 
## Running the NIST test suite  运行NIST测试套件 

*Note: the NIST tests aren't actually mirrored in Fuchsia yet. Today, you need to clone the tests from the repo at<https://github.com/usnistgov/SP800-90B_EntropyAssessment>.* *注：紫红色尚未真正反映出NIST测试。今天，您需要从以下版本的仓库中克隆测试：<https://github.com/usnistgov/SP800-90B_EntropyAssessment>。*

The NIST test suite has three entry points (as of the version committed on Oct. 25, 2016): `iid_main.py`, `noniid_main.py`, and `restart.py`. The two "main"scripts perform the bulk of the work. The `iid_main.py` script is meant forentropy sources that produce independent, identically distributed data samples.Most of the testing is to validate the iid condition. Many entropy sources willnot be iid, so the `noniid_main.py` test implements several entropy estimatorsthat don't require iid data. NIST测试套件具有三个入口点（截至2016年10月25日提交的版本）：`iid_main.py`，`noniid_main.py`和`restart.py`。这两个“主要”脚本完成了大部分工作。 iid_main.py脚本是用于产生独立的，均匀分布的数据样本的熵源。大多数测试是为了验证iid条件。许多熵源都不会被iid所接受，因此`noniid_main.py`测试实现了一些不需要iid数据的熵估计量。

Note that the test binaries from the NIST repo are Python scripts without a shebang line, so you probably need to explicitly call `python` on the commandline when invoking them. 请注意，NIST存储库中的测试二进制文件是不带shebang行的Python脚本，因此您可能需要在调用命令行时在命令行上显式调用Python。

The first two scripts take two arguments, both mandatory: the data file to read, and the number of significant bits per sample (if less than 8, only the low `N`bits will be used from each byte). They optionally accept a `-v` flag to produceverbose output or `-h` for help. 前两个脚本采用两个参数，两个参数都是强制性的：要读取的数据文件，以及每个样本的有效位数（如果小于8，则每个字节仅使用低N位）。他们可以选择接受-v标志来产生详细的输出，或接受-h来获取帮助。

The `noniid_main.py` also optionally accepts a `-u <int>` flag that can reduce the number of bits below the `N` value passed in the second mandatory argument.I'm not entirely sure why this flag is provided; it seems functionallyredundant, but passing it does change the verbose output slightly. My best guessis that this is provided because the noniid Markov test only works on samples ofat most 6 bits, so 7- or 8-bit datasets will be reduced to their low 6 bits forthis test. In contrast, all the iid tests can run on 8-bit samples. `noniid_main.py`还可以选择接受-u <int>`标志，该标志可以减少第二个强制参数中传递的`N`值以下的位数。在功能上似乎是多余的，但是通过它确实会稍微改变详细的输出。我最好的猜测是提供此信息，因为非偶数马尔可夫检验仅适用于最多6位的样本，因此对于此测试，7或8位数据集将减少为低6位。相反，所有iid测试都可以在8位样本上运行。

A sample invocation of the `iid_main.py` script:  `iid_main.py`脚本的示例调用：

```
python2 -- $FUCHSIA_DIR/third_party/sp800-90b-entropy-assessment/iid_main.py -v /path/to/datafile.bin 8
```
 

The `restart.py` script takes the same two arguments, plus a third argument: the min-entropy estimate returned by a previous run of `iid_main.py` or`noniid_main.py`. This document doesn't describe restart tests. For now, seeNIST SP800-90B for more details. restart.py脚本使用相同的两个参数，外加第三个参数：上一次运行iid_main.py或noniid_main.py返回的最小熵估计。本文档没有描述重启测试。目前，请参阅NIST SP800-90B了解更多详细信息。

 
## Future directions  未来发展方向 

 
### Automation  自动化 

