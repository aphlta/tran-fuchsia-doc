 
# ELF Runner  ELF亚军 

The ELF runner is the runner responsible for launching [components][glossary-components] based on standard executable files (ELFformat). ELF运行程序是负责基于标准可执行文件（ELFformat）启动[components] [glossary-components]的运行程序。

For a detailed explanation of how processes are created, please see [`//docs/concepts/booting/program_loading.md`][program-loading]. 有关如何创建进程的详细说明，请参见[`//docs/concepts/booting/program_loading.md`][program-loading]。

 
## Using the ELF Runner  使用ELF Runner 

The ELF runner receives instructions from the `program` section of the [component manifest][glossary-component-manifests]. The `binary` field holds thepath to an executable file in the package the manifest comes from, and the`args` field holds any additional string arguments that should be provided tothe process when it is created. ELF运行程序从[组件清单] [glossary-component-manifests]的“程序”部分接收指令。 Binary字段包含清单所来自的包中的可执行文件的路径，而args字段包含创建该过程时应提供给该进程的任何其他字符串参数。

This is an example manifest that launches `bin/echo` with the arguments `Hello` and `world!`: 这是一个示例清单，它使用参数“ Hello”和“ world！”启动“ bin / echo”：

```cml
{
    "program": {
        "binary": "bin/echo",
        "args": [ "Hello", "world!" ],
    }
}
```
 

