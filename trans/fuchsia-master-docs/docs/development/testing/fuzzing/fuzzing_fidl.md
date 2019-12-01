 
# Fuzzing the FIDL host tools  模糊化FIDL主机工具 

Some notes on fuzzing the `tools/fidl` parser using [afl-fuzz](http://lcamtuf.coredump.cx/afl/). 关于使用[afl-fuzz]（http://lcamt​​uf.coredump.cx/afl/）模糊化“ tools / fidl”解析器的一些注意事项。

 
## Build afl-fuzz  建立afl-fuzz 

Download and build it, then:  下载并构建它，然后：

```
export AFL_PATH=~/src/afl-2.41b/
```
 

with whatever path you downloaded and built it with.  使用您下载并构建的任何路径。

 
## Patch the parser to not trap on invalid syntax  修补解析器以使其不陷入无效语法 

afl-fuzz treats crashes as interesting but the parser currently calls `__builtin_trap()` when it encounters invalid syntax.Remove that line in [parser.h](/zircon/tools/fidl/include/fidl/parser.h) - its in the `Parser::Fail()` method. afl-fuzz将崩溃视为有趣的事件，但解析器在遇到无效语法时当前会调用__builtin_trap（）。在[parser.h]（/ zircon / tools / fidl / include / fidl / parser.h）中删除该行-在Parser :: Fail（）方法中。

 
## Build the `fidl` tool with afl-fuzz's instrumentation  用afl-fuzz的工具构建`fidl`工具 

Clear any existing build and then build with the afl-fuzz compiler wrappers.  清除所有现有构建，然后使用afl-fuzz编译器包装器进行构建。

```
cd $ZIRCON_DIR
rm -fr build-x86
PATH=$PWD/prebuilt/downloads/clang+llvm-x86_64-linux/bin/:$PATH:$AFL_PATH make \
  build-x86/tools/fidl HOST_TOOLCHAIN_PREFIX=afl-
```
 

adjusting if you're not building on x86 Linux, etc.  如果您不在x86 Linux等平台上构建，请进行调整。

 
## Run the fuzzer  运行模糊器 

The parser includes some examples to use as inputs. As FIDL becomes adopted we can expand our inputs to include all of the different protocolsdeclared across our tree, but for now we use what's in `tools/fidl/examples`. 解析器包括一些用作输入的示例。随着FIDL的采用，我们可以扩展我们的输入以包括在我们的树中声明的所有不同协议，但是现在我们使用`tools / fidl / examples`中的内容。

```
$AFL_PATH/afl-fuzz -i tools/fidl/examples -o fidl-fuzz-out build-x86/tools/fidl dump '@@'
```
 

 
## Results  结果 

