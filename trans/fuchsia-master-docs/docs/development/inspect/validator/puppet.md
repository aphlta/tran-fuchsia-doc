 
# Inspect Validator Puppet Architecture  检查验证器木偶体系结构 
## Overview  总览 

The Validator program sends FIDL commands to control a "puppet" program, which invokes library functionality to modify some state which the Validator thenevaluates. For more information about the Inspect Validator, see the[README](README.md). 验证程序发送FIDL命令来控制“ a”程序，该程序调用库功能来修改验证程序评估的某些状态。有关检查验证器的更多信息，请参见[README]（README.md）。

The Puppet includes these parts:  木偶包括以下部分：

 
* Serving a FIDL protocol.  *提供FIDL协议。
* Unpacking the protocol and making library calls.  *解压缩协议并进行库调用。
* Building an integration test that includes the Puppet and Validator programs.  *构建一个包含Puppet和Validator程序的集成测试。

This doc focuses on the Inspect Validator Rust Puppet located at [//src/diagnostics/inspect_validator/lib/rust/src/main.rs](/src/diagnostics/inspect_validator/lib/rust/src/main.rs). 本文档重点介绍位于[//src/diagnostics/inspect_validator/lib/rust/src/main.rs]（/src/diagnostics/inspect_validator/lib/rust/src/main.rs）中的Inspect Validator Rust木偶。

 
## FIDL design  FIDL设计 

The FIDL protocol for Inspect Validator is defined in [//src/diagnostics/inspect_validator/fidl/validate.test.fidl](/src/diagnostics/inspect_validator/fidl/validate.test.fidl).The FIDL protocol corresponds closely to the functions in the[Inspect library API](/docs/development/inspect/gsw-inspect.md)which defines actions to be applied to any Inspect API implementation. The FIDLAPI is written to correspond to the[Rust API](https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/index.html). 用于Inspect Validator的FIDL协议在[//src/diagnostics/inspect_validator/fidl/validate.test.fidl](/src/diagnostics/inspect_validator/fidl/validate.test.fidl）中定义。FIDL协议与[Inspect库API]（/ docs / development / inspect / gsw-inspect.md）中的函数，这些函数定义了要应用于任何Inspect API实现的操作。 FIDLAPI被编写为对应于[Rust API]（https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/index.html）。

(Note: Inspect APIs are allowed to differ from the Rust API; such APIs may require puppet code architecture modifications.) （注意：Inspect API允许与Rust API有所不同；此类API可能需要修改p代码体系结构。）

 
## Serving FIDL  服务FIDL 

The `main()` function performs boilerplate to serve a single FIDL client through `run_driver_service()` which receives either `Initialize` or `Act`events from the FIDL stream. `Act` events are unpacked by the `Actor` objectwhich maintains the state necessary to control the Inspect library. main（）函数通过“ run_driver_service（）”执行样板服务单个FIDL客户端，该“ run_driver_service（）”从FIDL流中接收“ Initialize”或“ Act”事件。 Act事件由Actor对象解包，Actor对象保持控制Inspect库所必需的状态。

 
## Actor and the Inspect library  演员和检查库 

`Actor` contains an `Inspector` (the Inspect library's entry-point object), a hashmap of `nodes`, and a hashmap of `properties`. It implements onefunction, `act()`, which contains a giant `match` statement ("switch" or "case"in other languages) to invoke each action that the library implements.Puppets can report `Unimplemented` for actions the library doesn't support. Actor包含一个Inspector（Inspect库的入口点对象），一个node的hashmap和一个properties的hashmap。它实现了一个函数“ act（）”，其中包含一个巨大的“ match”语句（用其他语言表示“ switch”或“ case”）来调用该库实现的每个动作。木偶可以报告该库未执行的动作“未实现”。不支持。

After the Validator invokes each action, it will test the library's effect on the VMO. The library should handle propagating the effects of actions so thatthe Validator can see them. 验证程序调用每个操作后，它将测试库对VMO的影响。库应处理动作的传播效果，以便验证者可以看到它们。

The hashmaps of `nodes` and `properties` store values that are returned by the Inspect library. Since Rust is an RAII language that cleans up automaticallywhen reference to memory is lost, failing to store a node or property wouldcause immediate deletion of that node or property. Also, storing propertiesallows updating their values in response to FIDL commands. 节点和属性的哈希图存储Inspect库返回的值。由于Rust是一种RAII语言，当丢失对内存的引用时，它会自动清除，因此无法存储节点或属性将导致该节点或属性的立即删除。同样，存储属性允许响应FIDL命令更新其值。

 
## Testing and the build system  测试和构建系统 

The Validator and Puppet combination should make a hermetic integration test.  Validator和Puppet的组合应进行密封集成测试。

Note: due to limitations in the Dart build-system macros, the Dart test isn't fully hermetic. 注意：由于Dart构建系统宏中的限制，Dart测试不是完全密封的。

 
### Dependencies and names  依存关系和名称 

[Validator's BUILD.gn file](/src/diagnostics/inspect_validator/BUILD.gn#21) defines a `validator_bin` target which is used by the[Rust puppet's BUILD.gn file](/src/diagnostics/inspect_validator/lib/rust/BUILD.gn#33)as a dependency to the `test_package()` named `inspect_validator_test_rust`which is the test that exercises the Rust puppet. [Validator的BUILD.gn文件]（/ src / diagnostics / inspect_validator / BUILD.gn21）定义了一个[validator_bin]目标，供[Rust puppet的BUILD.gn文件]（/ src / diagnostics / inspect_validator / lib / rust / BUILD.gn33）依赖于名为test_package（）的名为inspect_validator_test_rust的测试，该测试是练习Rust木偶的测试。

The Rust puppet itself is [built as a standard rustc_binary](/src/diagnostics/inspect_validator/lib/rust/BUILD.gn#10).That build rule produces two names, `inspect_validator_rust_puppet_bin` whichis included in the deps of the `test_package()` rule, and`inspect_validator_rust_puppet` which is included in the binaries of the`test_package()`. Rust木偶本身[作为标准rustc_binary构建]（/ src / diagnostics / inspect_validator / lib / rust / BUILD.gn10）。该构建规则产生两个名称，即“ inspect_validator_rust_puppet_bin”，包含在test_package（）的deps中。规则和包含在test_package（）二进制文件中的inspect_validator_rust_puppet。

The `validator_bin` target from the [Validator's Build.gn file](/src/diagnostics/inspect_validator/BUILD.gn#21)has a name of `validator` which is referred to in the `tests` of the`test_package()`. [Validator的Build.gn文件]（/ src / diagnostics / inspect_validator / BUILD.gn21）中的`validator_bin`目标具有`validator'的名称，该名称在test_package（）的`tests'中引用。

 
### CQ/CI  CQ / CI 

Putting `inspect_validator_test_rust` in the `deps` of `group("tests")` in its [BUILD.gn](/src/diagnostics/inspect_validator/lib/rust/BUILD.gn#59)makes it easy to include `inspect_validator/lib/rust:tests` in the `deps` of`group("tests")` of [src/diagnostics/BUILD.gn](/src/diagnostics/BUILD.gn).This will be picked up by the build system and cause the Inspect Validator RustPuppet test to be run in CQ and CI. 将`inspect_validator_test_rust`放入其[BUILD.gn]（/ src / diagnostics / inspect_validator / lib / rust / BUILD.gn59）的`group（“ tests”）`的`deps中，可以很容易地包含`inspect_validator / lib / rust：tests在[src / diagnostics / BUILD.gn]（/ src / diagnostics / BUILD.gn）组的“ deps”中（“测试”）。这将由构建系统和使Inspect Validator RustPuppet测试在CQ和CI中运行。

 
### Meta .cmx files  元.cmx文件 

There are the following CMX files in [//src/diagnostics/inspect_validator/lib/rust/meta](/src/diagnostics/inspect_validator/lib/rust/meta):  [// src / diagnostics / inspect_validator / lib / rust / meta]（/ src / diagnostics / inspect_validator / lib / rust / meta）中包含以下CMX文件：

 
* [inspect_validator_rust_puppet.cmx](/src/diagnostics/inspect_validator/lib/rust/meta/inspect_validator_rust_puppet.cmx)  * [inspect_validator_rust_puppet.cmx]（/ src / diagnostics / inspect_validator / lib / rust / meta / inspect_validator_rust_puppet.cmx）

  Lets the puppet binary run and use the logger. It's referred to in the `meta` section of `test_package("inspect_validator_test_rust")`. 让人偶二进制文件运行并使用记录器。在test_package（“ inspect_validator_test_rust”）`的“ meta”部分中进行了引用。
* [validator.cmx](/src/diagnostics/inspect_validator/lib/rust/meta/validator.cmx)  * [validator.cmx]（/ src / diagnostics / inspect_validator / lib / rust / meta / validator.cmx）

  This CMX file is implicitly referred to by the `tests: name: "validator"` that you specified in `test_package()`.  您在test_package（）中指定的tests：name：“ validator”隐式引用此CMX文件。
    * `sandbox: services` specifies the services that the Validator needs to run.  *`sandbox：services`指定验证程序需要运行的服务。
    * `program: args` supplies command-line arguments to the Validator, including the complete URL of the Rust puppet. *`program：args`向Validator提供命令行参数，包括Rust木偶的完整URL。
    * `program: binary` confirms that you want to run the `tests: name: "validator"`. *`program：binary`确认您要运行`tests：name：“ validator”`。

 
## Running Validator  运行验证器 

