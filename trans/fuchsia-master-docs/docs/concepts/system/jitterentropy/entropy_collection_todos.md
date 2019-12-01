 
# Entropy collection TODOs  熵收集待办事项 

I'm writing this at the end of my internship to record some of the things I didn't get to.  我在实习结束时写这篇文章是为了记录一些我没有去做的事情。

[TOC]  [目录]

 
## Proper use of RdRand  正确使用RdRand 

On x86, `RdRand` reads from a deterministic CPRNG (which is seeded from a hardware entropy source). The newer `RdSeed` instruction reads from the underlying entropy source directly (well, with somepost-processing). Currently, we prefer to use `RdSeed` but if that isn't available we fall back on`RdRand`. However, we just draw random bits directly from `RdRand`, in contravention of the IntelHWRNG guide([online here](https://software.intel.com/en-us/articles/intel-digital-random-number-generator-drng-software-implementation-guide);see section 4.2.5 "Guaranteeing DBRG Reseeding"). We should fix that. 在x86上，“ RdRand”从确定性CPRNG（从硬件熵源中获取）读取。较新的`RdSeed`指令直接从底层的熵源中读取（当然，需要进行一些后期处理）。当前，我们更喜欢使用`RdSeed`，但是如果不可用，我们将退回到`RdRand`。但是，我们只是直接从`RdRand`中提取随机位，这违反了IntelHWRNG指南（[在线此处]（https://software.intel.com/en-us/articles/intel-digital-random-number-generator -drng-software-implementation-guide）；请参阅第4.2.5节“保证DBRG重新播种”。我们应该解决这个问题。

Googlers: see issue ZX-983  Google员工：请参阅问题ZX-983

 
## Reseeding the CPRNG during runtime  在运行时重新播种CPRNG 

My hacky virtio driver will reseed the CPRNG on qemu (on a five minute recurring timer). I think that's the only entropy source that is currently used to reseed after system startup. 我的hacker virtio驱动程序将在qemu上重新设置CPRNG（定期重播五分钟）。我认为这是系统启动后当前用于重新设定种子的唯一熵源。

As a start, we should be able to use the entropy sources built into the kernel (RdRand and jitterentropy). Just running these on a periodic timer would improve our reseeding story. Note thatonce every 5 minutes is probably more often than we need. 首先，我们应该能够使用内核中内置的熵源（RdRand和抖动熵）。仅在定期计时器上运行它们可以改善我们的播种故事。请注意，每5分钟一次可能比我们需要的次数更多。

We've talked about reseeding more often if large amounts of data have been drawn from the CPRNG (on the order of 2^48 bits, I think). 如果从CPRNG提取了大量数据（我们认为约为2 ^ 48位），我们讨论的播种次数更多。

 
## Monitoring entropy sources  监测熵源 

Entropy sources can potentially fail, either totally or partially.  熵源可能全部或部分失效。

Total failures like "the device was unplugged" or "the device is not responding to I/O" will hopefully be reported by the hardware layer. 希望通过硬件层报告诸如“设备已拔出”或“设备未响应I / O”之类的全部故障。

Partial failures, where the device returns data but with less entropy than expected, are scarier. We should run simple health tests to try to detect partial failures. See for example the continuoushealth tests in NIST SP800-90B, section 4.4. The health tests there are pretty simple and requireminimal resources. They do require storing some statistics about recent entropy source outputs,which presents some security risk. 设备返回数据但熵小于预期的部分故障更为可怕。我们应该运行简单的运行状况测试以尝试检测部分故障。参见例如NIST SP800-90B中的持续健康测试，第4.4节。那里的运行状况测试非常简单，并且需要最少的资源。他们确实需要存储有关最近的熵源输出的一些统计信息，这带来了一些安全风险。

The NIST SP also suggests (well, requires, but I'm not aware of any immediate plans for certification) running startup tests. The NIST startup tests involve running the continuous testsover at least 4096 samples (see section 4.3 #12), after which these samples may be reused to seedthe CPRNG. NIST SP还建议（很好，需要，但我不知道有任何立即的认证计划）运行启动测试。 NIST启动测试包括对至少4096个样本进行连续测试（请参阅第4.3 12节），然后可以将这些样本重新用于CPRNG播种。

Once monitoring is in place, we need to decide how to respond to entropy source failures. If one of six different entropy sources fails, we might treat that as a minor hardware failure that getslogged. If the system has only one entropy source and it fails, we need to take more drastic action(on the order of shutting off the CPRNG or halting the system). 监控到位后，我们需要确定如何响应熵源故障。如果六个不同的熵源之一发生故障，我们可以将其视为已记录的轻微硬件故障。如果系统只有一个熵源而失败了，我们需要采取更严厉的行动（以关闭CPRNG或暂停系统的顺序）。

 
## Userspace RNG drivers  用户空间RNG驱动程序 

Once DDK settles down, we should add to and improve our RNG drivers. Currently, there are two RNG-related drivers: TPM and virtio-rng. DDK解决后，我们应该添加和改进RNG驱动程序。当前，有两个与RNG相关的驱动程序：TPM和virtio-rng。

An important requirement is to restrict access to the `zx_cprng_add_entropy` syscall, via a Resource or similar mechanism. We should also use this to differentiate between the devices providingentropy, for monitoring purposes. It would also be nice if the kernel can send start/stop signals tothe drivers through this Resource. 一个重要的要求是通过资源或类似机制来限制对`zx_cprng_add_entropy`系统调用的访问。我们还应该使用它来区分提供熵的设备，以进行监视。如果内核可以通过此资源向驱动程序发送启动/停止信号，那也很好。

Here are some currently unused entropy sources to consider:  以下是一些当前未使用的熵源：

 
- There's an existing TPM driver, which calls `cprng_add_entropy` in its `bind()` callback. We should add support for TPM 2.0, for better coverage. -现有一个TPM驱动程序，在其`bind（）`回调函数中调用`cprng_add_entropy`。我们应该添加对TPM 2.0的支持，以实现更好的覆盖范围。

 
- There are plenty of commercially available hardware RNGs, often connecting over USB. We could add drivers for those, but it probably makes sense to expect third party drivers instead. -有大量的商用硬件RNG，通常通过USB连接。我们可以为这些驱动程序添加驱动程序，但是期望使用第三方驱动程序可能更有意义。

 
- There's also apparently a hardware RNG built into the SoC in Raspberry Pis, according to [the Raspberry Pi forums](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=19334&p=273944#p273944).In general we could check other specific targets (i.e. not "pc-x86-64") for hardware RNGs and wirethose up. If we're lucky, many of these will be accessible from the kernel for use during orimmediately after boot. -根据[Raspberry Pi论坛]（https://www.raspberrypi.org/forums/viewtopic.php?f=29t=19334p=273944p273944)，Raspberry Pis的SoC中显然还内置有硬件RNG。通常，我们可以检查其他特定的目标（例如，不是“ pc-x86-64”）以获取硬件RNG和接线。如果幸运的话，很多这些都可以从内核访问，以便在启动后立即使用。

 
- Finally, we could record entropy from hardware IRQs, especially for hard disks, network cards, input devices, and other classic entropy sources. This won't be anywhere near as fast as adedicated hardware RNG, but it's attractive since a few lines of code added in the right places inour driver stack should enable entropy collection from a wide variety of very common devices. -最后，我们可以记录来自硬件IRQ的熵，尤其是硬盘，网卡，输入设备和其他经典熵源的熵。这不会像专用的硬件RNG那样快，但是它很吸引人，因为在驱动程序堆栈的正确位置添加了几行代码，应该可以从各种非常常见的设备中收集信息。

Googlers: SEC-29  Google员工：SEC-29

 
## Jitterentropy  抖动熵 

 
### Replace the noise-generating functions by assembly, and remove '-O0'  通过组装来替换产生噪声的功能，并删除“ -O0” 

Right now, jitterentropy is compiled at optimization level `-O0` (as per the author's documentation). The reason is the two noise-generating functions: `jent_lfsr_time` and`jent_memaccess`. We should replace these C functions by assembly code (probably by compiling withflags `-S -O0`), then compile the rest of jitterentropy with optimizations enabled. After this, weshould re-test to make sure our entropy estimates remain accurate. 现在，抖动熵是在优化级别-O0上编译的（根据作者的文档）。原因是两个产生噪声的函数：“ jent_lfsr_time”和“ jent_memaccess”。我们应该用汇编代码替换这些C函数（可能通过编译`-S -O0`标记），然后在启用优化的情况下编译其余的抖动熵。此后，我们应该重新测试以确保我们的熵估计保持准确。

Googlers: SEC-14  Google员工：SEC-14

 
### Test jitterentropy more thoroughly  更彻底地测试抖动熵 

I've been testing on the same handful of physical devices. We should test jitterentropy on a few other PCs, RPis, etc. 我一直在同一批物理设备上进行测试。我们应该在其他几台PC，RPis等上测试抖动熵。

Googlers: SEC-22  Google员工：SEC-22

 
### Test jitterentropy at runtime  在运行时测试抖动 

Right now, jitterentropy only runs (and was only tested) during the single-core part of the boot sequence. We should test jitterentropy during SMP runtime, and consider whether we need to (say)disable interrupts or pin ourselves to a CPU inside jitterentropy. 目前，抖动熵仅在引导序列的单核部分运行（并且仅经过测试）。我们应该在SMP运行时测试抖动熵，并考虑是否需要（说）禁用中断或将自己固定到抖动熵内的CPU。

Googlers: ZX-1024  Google员工：ZX-1024

 
### More tuning  更多调音 

See [the tuning doc](/docs/concepts/system/jitterentropy/config-tuning.md). The current universally hard-coded parameters seem to be decent, so this probably isn't incredibly urgent. Still, since jitterentropy is on thecritical path for every single boot and since it will run during runtime as well (hopefully soon!),it's probably worth optimizing at some point. 请参阅[调整文档]（/ docs / concepts / system / jitterentropy / config-tuning.md）。当前通用的硬编码参数似乎是不错的，因此这可能并不是紧迫的事情。不过，由于抖动是每次引导的关键路径，并且抖动也将在运行时运行（希望很快！），因此在某个时候可能值得进行优化。

We should probably at least tune jitterentropy on a per-architecture basis, and ideally per-target. Note that right now, the `entropy_per_1000_bytes` statistic in`kernel/lib/crypto/entropy/jitterentropy_collector.cpp` is hard-coded and not arch/target dependent.That should probably also be configurable. 我们可能至少应该在每个架构的基础上调整抖动熵，理想情况下应该是每个目标。请注意，现在，kernel / lib / crypto / entropy / jitterentropy_collector.cpp中的`entropy_per_1000_bytes`统计信息是硬编码的，并且不依赖于arch / target，这也应该是可配置的。

Googlers: ZX-1022  Google员工：ZX-1022

 
## Cloning the NIST test suite  克隆NIST测试套件 

