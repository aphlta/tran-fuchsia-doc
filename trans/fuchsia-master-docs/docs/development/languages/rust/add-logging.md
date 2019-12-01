 
# Add logging to hello world  将日志记录添加到Hello World 

The following guide discusses adding the [Rust Fuchsia logger library](https://fuchsia-docs.firebaseapp.com/rust/fuchsia_syslog/index.html) to the existing [hello world example](/examples/hello_world/rust/)component. In this guide, development takes place within the Fuchsia source tree. 以下指南讨论了将[Rust Fuchsia记录器库]（https://fuchsia-docs.firebaseapp.com/rust/fuchsia_syslog/index.html）添加到现有的[hello world示例]（/ examples / hello_world / rust /）零件。在本指南中，开发在紫红色的源代码树中进行。

With the Fuchsia logger library, you can interact with log collection services. You can use Fuchsia's logging tools to log and analyze servicesand components that are written to run on Fuchsia. 使用紫红色记录器库，您可以与日志收集服务进行交互。您可以使用Fuchsia的日志记录工具来记录和分析编写为在Fuchsia上运行的服务和组件。

 

 
## Prerequisites {#prerequisites}  先决条件{prerequisites} 

 
*   A hardware device that is set up to run Fuchsia.  *设置为运行紫红色的硬件设备。
    *   The device should be paved and running. If you haven't already installed Fuchsia, see [Get Started](/docs/getting_started.md). *设备应已铺好并正在运行。如果尚未安装Fuchsia，请参阅[入门]（/ docs / getting_started.md）。
*   Rust installed on your environment.  * Rust安装在您的环境中。
    *   The Fuchsia build installs a version of Rust that can be used for Fuchsia development. If you have already built Fuchsia, you don't needto install Rust again. *紫红色的内部版本安装了可以用于紫红色开发的Rust版本。如果您已经构建了Fuchsia，则无需再次安装Rust。

 

 
## Set build to include example {#include-example}  将构建设置为包括示例{include-example} 

This guide modifies the existing hello world Rust example component. In order to run that component later, you must set the hello world component withthe `fx` tool. 本指南修改了现有的hello world Rust示例组件。为了稍后运行该组件，必须使用`fx`工具设置hello world组件。

Run `fx set`, replacing `PRODUCT` and `BOARD` with your chosen product and board.  运行“ fx set”，将“ PRODUCT”和“ BOARD”替换为您选择的产品和电路板。

<pre class="prettyprint"> fx set <b>PRODUCT</b>.<b>BOARD</b>  --with //examples/hello_world</pre> <pre class =“ prettyprint”> FX设置<b> PRODUCT </ b>。<b>委员会</ b> --with // examples / hello_world </ pre>

Note: To see a list of possible products, run: <p><pre class="prettyprint">fx list-products</pre></p>To see a list of possible boards, run: <p><pre class="prettyprint">fx list-boards</pre></p> 注意：要查看可能的产品列表，请运行：<p> <pre class =“ prettyprint”> fx list-products </ pre> </ p>要查看可能的主板列表，请运行：<p> <pre class =“ prettyprint”> fx列表板</ pre> </ p>

 
## Edit the component package {#edit-component-package}  编辑组件包{edit-component-package} 

When connecting your component to an additional service, you need to do the following: 将组件连接到其他服务时，需要执行以下操作：

 
1. [Edit the `BUILD.gn`](#edit-the-buildgn)  1. [编辑`BUILD.gn`]（edit-the-buildgn）

 
1. [Edit the source file containing the `main()`](#edit-the-source-file)  1. [编辑包含`main（）`的源文件]（edit-the-source-file）

 
1. [Edit the component manifest](#edit-the-component-manifest)  1. [编辑组件清单]（edit-the-component-manifest）

 
### Edit the BUILD.gn {#edit-the-buildgn}  编辑BUILD.gn {edit-the-buildgn} 

You can declare your component's dependencies and source files in the `BUILD.gn`.  您可以在`BUILD.gn`中声明组件的依赖关系和源文件。

For more information, see [A Short Introduction to GN](/docs/development/build/intro.md).  有关更多信息，请参见[GN简介]（/docs/development/build/intro.md）。

 
1.  Open  the `BUILD.gn` in your chosen text editor.  1.在您选择的文本编辑器中打开“ BUILD.gn”。

    ```
    vi ~/fuchsia/examples/hello_world/BUILD.gn
    ```
 

 
1.  Add `"//garnet/public/rust/fuchsia-syslog"` to the dependencies array in the `rustc_binary` target, which defines the executable. 1.将“ // garnet / public / rust / fuchsia-syslog”添加到“ rustc_binary”目标中的依赖项数组，该目标数组定义了可执行文件。

    After adding this dependency, the `rustc_binary` in your `BUILD.gn`  should look like this: 添加此依赖项后，`BUILD.gn`中的`rustc_binary`应该如下所示：

    ```
    …
    rustc_binary("bin") {
    name = "hello_world_rust"
    with_unit_tests = true
    edition = "2018"

    deps = [
    "//garnet/public/rust/fuchsia-syslog",
    ]
    test_deps = [ "//garnet/public/rust/fuchsia-async" ]
    }
    …
    ```
 

 
### Edit the source file {#edit-the-source-file}  编辑源文件{edit-the-source-file} 

The source files are included in the `src` directory of your component's package. In this guide, the source file is `main.rs`. 源文件包含在组件包的`src`目录中。在本指南中，源文件是`main.rs`。

 
1.  Open  the source file, `main.rs`, with your chosen text editor.  1.使用您选择的文本编辑器打开源文件`main.rs`。

    ```
    vi ~/fuchsia/examples/hello_world/rust/src/main.rs
    ```
 

 
1.  Add a `use` declaration for the `fuchsia_syslog` crate.  1.为`fuchsia_syslog`板条箱添加一个`use`声明。

    ```
    use fuchsia_syslog as syslog
    ```
 

 
1.  Within `main()`, initialize the `fuchsia_syslog` crate.  1.在“ main（）”中，初始化“ fuchsia_syslog”板条箱。

    ```
    syslog::init().expect("should not fail");
    ```
 

 
1.  Within `main()`, add your log message.  1.在`main（）`中，添加您的日志消息。

    ```
    fx_log_info!("{}, log!", greeting());
    ```
 

    At this point, `main.rs` should look like this:  此时，`main.rs`应该看起来像这样：

    ```rust
    use fuchsia_syslog as syslog;

    fn main() {
        syslog::init().expect("should not fail");
        fx_log_info!("{}, log!", greeting());
        println!("{}, world!", greeting());
    }
    …
    ```
 

 
### Edit the component manifest {#edit-the-component-manifest}  编辑组件清单{edit-the-component-manifest} 

The component manifest is a JSON file with the `.cmx` file extension.  组件清单是一个带有`.cmx`文件扩展名的JSON文件。

The component manifest declares what services and resources your package uses.  组件清单声明了您的包使用哪些服务和资源。

For more information, see [Component manifest](/docs/concepts/storage/component_manifest.md)  有关更多信息，请参见[组件清单]（/ docs / concepts / storage / component_manifest.md）

 
1.  Edit the component manifest, `hello_world_rust.cmx`, in your chosen text editor. 1.在您选择的文本编辑器中编辑组件清单“ hello_world_rust.cmx”。

    ```
    vi ~/fuchsia/examples/hello_world/rust/meta/hello_world_rust.cmx
    ```
 

 
    1.  Add a `sandbox` property JSON object with a `services` array.  1.添加一个带有`services`数组的`sandbox`属性JSON对象。
    1.  Include the `fuchsia.logger.LogSink` service within the `services` array. 1.在“服务”数组中包括“ fuchsia.logger.LogSink”服务。

    After completing this step, `hello_world_rust.cmx` should look like this:  完成此步骤后，`hello_world_rust.cmx`应该看起来像这样：

    ```
        {
            "program": {
                "binary": "bin/hello_world_rust"
            },
            "sandbox": {
                "services": [ "fuchsia.logger.LogSink" ]
            }
        }
    ```
 

 
1.  Execute a build of the Fuchsia image that contains your modified component Fuchsia package. 1.执行包含您修改后的组件Fuchsia包的Fuchsia映像的构建。

    ```
    fx build
    ```
 

 
### Test logging {#test-logging}  测试记录{test-logging} 

 
1.  Ensure that `fx serve` is running in a terminal window. If it is not, open a shell tab and run `fx serve`. 1.确保“ fx serve”在终端窗口中运行。如果不是，请打开一个shell选项卡并运行`fx serve`。

    ```
    cd ~/fuchsia
    ```
 

    ```
    fx serve
    ```
 

 
1.  In a new shell tab, navigate to your `fuchsia` directory and run `fx syslog.`  1.在一个新的shell选项卡中，导航到`fuchsia`目录并运行`fx syslog`。

    ```
    cd ~/fuchsia
    ```
 

    ```
    fx syslog
    ```
 

 
1.  In a new shell tab, navigate to your fuchsia directory and run the `hello_world_rust` component: 1.在一个新的shell选项卡中，导航到您的紫红色目录并运行`hello_world_rust`组件：

    ```
    cd ~/fuchsia
    ```
 

    ```
    fx shell run fuchsia-pkg://fuchsia.com/hello_world_rust#meta/hello_world_rust.cmx
    ```
 

 
1.  Navigate to the shell tab where you ran `fx syslog`. You should be able to see your logging text, which in this example is`Hello log!`. 1.导航到运行fx syslog的shell选项卡。您应该能够看到您的日志记录文本，在此示例中为“ Hello log！”。

