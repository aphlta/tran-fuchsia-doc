 
# Test Environments  测试环境 

The build system is tightly coupled with how the continuous integration infrastructure (from here on referred to as just "infra") discovers, aggregates,and runs tests. The high-level idea is that the test authors specify how theywant their tests to run in GN and this information is propagated from the buildsystem to the infra. 构建系统与持续集成基础结构（以下简称为“基础设施”）如何发现，汇总和运行测试紧密相关。高层的想法是测试作者指定他们希望他们的测试如何在GN中运行，并且此信息从构建系统传播到基础设施。

More specifically  进一步来说

 
*   The build produces metadata files for each test specifying the required execution environments. *构建会为每个测试生成指定所需执行环境的元数据文件。
*   Infra groups the tests into shards that share the same environment.  * Infra将测试分组为共享相同环境的碎片。
*   For each shard, infra schedules a bot to run those tests.  *对于每个分片，infra安排一个机器人来运行这些测试。
*   Results from all shards are aggregated and reported.  *来自所有分片的结果汇总并报告。

 
## Environments  环境环境 

The specification of a test's `environments` in GN is what determines where and how a test is run. It is given as list of scopes of the following form: GN中测试“环境”的规范决定了在何处以及如何运行测试。它以下列形式的作用域列表形式给出：

```gn
environments = [
  {
    dimensions = {
       <dimension key> = <value>
       ...
    }
    tags = ["<environment tags...>"]
    netboot = <boolean>
  },
  ...
]
```
 

See [guest_integration_tests](/src/virtualization/tests)for an example - and below for definitions of 'dimension' and 'tags' 有关示例，请参见[guest_integration_tests]（/ src / virtualization / tests）-以下有关“尺寸”和“标签”的定义

 
### Default Behavior  默认行为 

If no environments are specified for a test, than default behavior is as follows: 如果没有为测试指定任何环境，则默认行为如下：

 
1.  `__is_fuchsia__`: test only runs in a QEMU instance running Fuchsia  1.`__is_fuchsia__`：测试仅在运行Fuchsia的QEMU实例中运行
1.  `__is_linux__`: test only runs on a Linux machine  1.`__is_linux__`：测试仅在Linux机器上运行
1.  `__is_mac__`: test only runs on a Mac machine  1.`__is_mac__`：测试仅在Mac机器上运行

(1) means that hardware is opt-in; test authors must explicitly specify hardware environments in order to run tests there. The reasoning for this is that not alltests need to run on hardware, test authors know best whether that is the case,and that hardware is a scarce resource. （1）表示硬件已启用；测试作者必须明确指定硬件环境才能在其中运行测试。这样做的原因是，并非所有测试都需要在硬件上运行，测试作者最清楚情况是否如此，并且硬件是一种稀缺资源。

 
### Predefined environments  预定义环境 

One may import [//build/testing/environments.gni](/build/testing/environments.gni)and use the environment-related convenience variables defined within. Forexample, `basic_envs` includes all of the environments that are available toanyone without special consultation with the infra team. 可以导入[//build/testing/environments.gni](/build/testing/environments.gni）并使用其中定义的与环境相关的便利变量。例如，“ basic_envs”包括所有无需与基础团队特别协商即可提供给所有人的环境。

 
### Dimensions  外型尺寸 

`dimensions` here refer to [Swarming](https://chromium.googlesource.com/infra/luci/luci-py/+/master/appengine/swarming/doc/)dimensions, where Swarming is the task distribution system used by the infra. Adimension is effectively a key-value pair that describes a bot property that canbe targeted. 这里的“尺寸”是指[Swarming]（https://chromium.googlesource.com/infra/luci/luci-py/+/master/appengine/swarming/doc/）尺寸，其中“ Swarming”是由下文。 Adimension实际上是一个键值对，描述了可以作为目标的bot属性。

 
### Tags  标签 

Tags are arbitrary strings that may be attached to an environment. Setting it amounts to removing the corresponding test from the normal testing pipeline;in order then for that test to run, infra support for a new builder (to runtests for particular tags) must be added. Labels are used for special teststhat require different configurations. Before using tags, please consult withfuchsia-infra-team@google.com" 标签是可以附加到环境的任意字符串。设置它等于从正常的测试管道中删除相应的测试；为了使该测试运行，必须添加对新构建器的基础支持（以对特定标签进行测试）。标签用于需要不同配置的特殊测试。在使用标签之前，请咨询fuchsia-infra-team@google.com”

 
### Netboot  网络启动 

Netboot specifies whether to netboot instead of paving before running the tests in the shard for that environment. If omitted, it will be treated as false. Netboot指定在该环境的分片中运行测试之前是否进行网络引导而不是铺路。如果省略，它将被视为false。

 
## Validation  验证方式 

The `test_plaforms` list in [//build/testing/platforms.gni](/build/testing/platforms.gni)is the source of truth for what platforms are available for testing and whatdimensions they possess to match against. Say an environment *matches* aplatform entry if the former's `dimensions` is a subscope of the latter; say anenvironment is *valid* for the current architecture if it matches a`test_platforms` entry that doesn't specify a `cpu` value different than`current_cpu`. [//build/testing/platforms.gni](/build/testing/platforms.gni）中的`test_plaforms`列表是可用于测试的平台及其所要匹配的尺寸的真相来源。如果前者的“维度”是后者的子范围，则说一个“匹配”平台的条目的环境；如果环境匹配“ test_platforms”条目（未指定与“ current_cpu”不同的“ cpu”值），则该环境对于当前体系结构是“有效”的。

Environment validation happens at `gn gen`-time and can be summed up as  环境验证发生在gn gen时，可以总结为

 
*   Each environment must be valid for some architecture.  *每个环境必须对某些体系结构有效。

 
*   Each test must have an environment that is valid for the given architecture.  *每个测试必须具有对给定体系结构有效的环境。

 
### Example  例 

Suppose platforms.gni consisted of  假设platform.gni由

```gn
test_platforms = [
  {  # P1
    device_type = "QEMU"
    cpu = "x64"
  },
  { # P2
    device_type = "QEMU"
    cpu = "arm64"
  },
  { # P3
    device_type = "Intel NUC Kit NUC7i5DNHE"
    cpu = "x64"
  },
]
```
 

and consider the specification of  并考虑规格

```gn
environments = [
  { # E1
     dimensions = {
       device_type = "Intel NUC Kit NUC7i5DNHE"
     }
  },
  { # E2
     dimensions = {
       device_type = "QEMU"
     }
  },
]
```
 

