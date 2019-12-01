 

 
# Run the examples  运行示例 

While exploring the source code, you may have noticed the `examples` directory. This guide will show you how to build Fuchsia to include some examples and thenrun them on the device. 在浏览源代码时，您可能已经注意到“ examples”目录。本指南将向您展示如何构建Fuchsia以包含一些示例，然后在设备上运行它们。

 
## Explore the hello_world example  探索hello_world示例 

Open the [`examples/hello_world/BUILD.gn`](/examples/hello_world/BUILD.gn) file.  打开[`examples / hello_world / BUILD.gn`]（/ examples / hello_world / BUILD.gn）文件。

If you aren't familiar with GN, take a look at the [introductory presentation](https://docs.google.com/presentation/d/15Zwb53JcncHfEwHpnG_PoIbbzQ3GQi_cpujYwbpcbZo/view#slide=id.g119d702868_0_12) (slides 5-16 cover the core concepts, andslides 17-21 describe debugging commands) or [docs](https://gn.googlesource.com/gn/+/master/docs/).In short, GN is a meta build system. Its output files serve as inputs to[Ninja](https://ninja-build.org/), the actual build system. 如果您不熟悉GN，请查看[介绍性演示]（https://docs.google.com/presentation/d/15Zwb53JcncHfEwHpnG_PoIbbzQ3GQi_cpujYwbpcbZo/viewslide=id.g119d702868_0_12）（幻灯片5-16封面，幻灯片17-21描述了调试命令）或[docs]（https://gn.googlesource.com/gn/+/master/docs/）。简而言之，GN是一个元构建系统。它的输出文件用作实际构建系统[Ninja]（https://ninja-build.org/）的输入。

In this file, the `hello_world` target is a group containing other dependencies, notably `cpp` and `rust`. Using this target will build both of them. 在此文件中，“ hello_world”目标是一个包含其他依赖项的组，尤其是“ cpp”和“ rust”。使用此目标将同时建立它们。

```gn
group("hello_world") {
  testonly = true
  deps = [
    ":tests",
    "cpp",
    "rust",
  ]
}
```
 

Note: You can look at the [`build/package.gni`](/build/package.gni) file to learn more about how Fuchsia packages are defined by GN. 注意：您可以查看[`build / package.gni`]（/ build / package.gni）文件，以了解有关GN如何定义Fuchsia软件包的更多信息。

This example outputs `Hello, world!` and is written in both C++ and Rust. Each language-dependent directory has its own `BUILD.gn` file that defines a packagefor the specific example, as well as a `meta` subdirectory with `.cmx` files. 这个例子输出`Hello，world！`，并且用C ++和Rust编写。每个与语言相关的目录都有其自己的“ BUILD.gn”文件，该文件定义了用于特定示例的程序包，以及带有“ .cmx”文件的“ meta”子目录。

The `.cmx` file is known as a [component manifest](/docs/glossary.md#component-manifest) and describes how to runthe application on Fuchsia as a [component](/docs/glossary.md#component). This isthe proper way to create a [Fuchsia package](/docs/glossary.md#fuchsia-package). .cmx文件被称为[component manifest]（/ docs / glossary.mdcomponent-manifest），并描述了如何在Fuchsia上作为[component]（/ docs / glossary.mdcomponent）运行应用程序。这是创建[Fuchsia包]（/ docs / glossary.mdfuchsia-package）的正确方法。

You run a Fuchsia component by referencing its [Fuchsia package URI](/docs/glossary.md#fuchsia-pkg-url). To run one of theexamples: 您可以通过引用其[Fuchsia包URI]（/ docs / glossary.mdfuchsia-pkg-url）运行Fuchsia组件。要运行以下示例之一：

 
1.  Make sure `fx serve` is running in a terminal window. If it's not running, start it:  1.确保“ fx serve”在终端窗口中运行。如果它没有运行，请启动它：

    ```sh
    fx serve
    ```
 

 
1.  In another terminal, run:  1.在另一个终端中，运行：

    ```sh
    fx shell run fuchsia-pkg://fuchsia.com/hello_world_cpp#meta/hello_world_cpp.cmx
    ```
 

This should fail with a message stating the package was not found.  这应该失败，并显示一条消息，指出未找到该软件包。

Note: If it succeeds and prints "Hello World!", then your current fx target includes these examples already. You may need to modify your target and repavethe device, then return to this page to continue. 注意：如果成功并显示“ Hello World！”，则您当前的fx目标已经包括这些示例。您可能需要修改目标并重新设置设备，然后返回此页面继续。

 
## Set the build to include examples  设置构建以包含示例 

You can include the examples in the build, but you need to determine where they will be included: 您可以在构建中包含示例，但是您需要确定将这些示例包含在何处：

 
*   Base: Packages that are included in paving images produced by the build. They are included in over-the-air updates and are always updated as asingle unit. *基础：构建生成的铺装图像中包含的软件包。它们包含在空中更新中，并且始终作为单个单元进行更新。

 
*   Cache: Packages that are included in paving images, but are not included in over-the-air system updates. These packages can be updated at any time thatupdates are available. *缓存：铺装图像中包含的软件包，但无线系统更新中不包含的软件包。这些软件包可以在可用更新的任何时间进行更新。

 
*   Universe: Packages that are additional optional packages that can be fetched and run on-demand, but are not pre-baked into any paving images. * Universe：这些软件包是可以作为附加可选软件包的软件包，可以按需获取并按需运行，但不会预先烘焙到任何铺路图像中。

(For more information, see [fx workflows](/docs/development/workflows/fx.md).)  （有关更多信息，请参见[fx工作流程]（/ docs / development / workflows / fx.md）。）

To include this package in Universe so it can be fetched on-demand, use the `--with` flag when setting the product and board: 要将此软件包包含在Universe中以便可以按需获取，请在设置产品和电路板时使用`--with`标志：

```sh
fx set ... --with //examples/hello_world
fx build
```
 

You now have a build that includes the examples.  您现在拥有一个包含示例的构建。

 
## Run the examples  运行示例 

 
1.  Make sure `fx serve` is running in a terminal window. If it's not running, start it:  1.确保“ fx serve”在终端窗口中运行。如果它没有运行，请启动它：

    ```sh
    fx serve
    ```
 

 
1.  In another terminal, run:  1.在另一个终端中，运行：

    ```sh
    fx shell run fuchsia-pkg://fuchsia.com/hello_world_cpp#meta/hello_world_cpp.cmx
    ```
 

You should see the following output:  您应该看到以下输出：

```uglyprint
Hello, World!
```
 

Important: If `fx serve` is not running, you should get an error from the device (for example,`fuchsia-pkg://fuchsia.com/hello_world_cpp#meta/hello_world_cpp.cmx: notfound`). 重要提示：如果未运行“ fx serve”，则设备应会出现错误（例如，fuchsia-pkg：//fuchsia.com/hello_world_cppmeta/hello_world_cpp.cmx：未找到）。

The `run` command can expand a string to a URI if the string only matches one component in your product configuration: 如果该字符串仅匹配您产品配置中的一个组件，则“运行”命令可以将字符串扩展为URI：

```sh
fx shell run hello_world_cpp
```
 

If there are multiple matches, the command will list them for you to choose from: 如果有多个匹配项，该命令将列出它们以供您选择：

```sh
fx shell run hello
```
 

```uglyprint
fuchsia-pkg://fuchsia.com/hello_world_cpp#meta/hello_world_cpp.cmx
fuchsia-pkg://fuchsia.com/hello_world_rust#meta/hello_world_rust.cmx
Error: "hello" matched multiple components.
```
 

You can explore what components are in your product configuration using the `locate` command. 您可以使用“ locate”命令探索产品配置中的哪些组件。

 
*   Find your favorite component.  *查找您喜欢的组件。

    ```
    fx shell locate hello_world_cpp
    ```
 

 
*   Find all runnable components.  *查找所有可运行的组件。

    ```
    fx shell locate --list cmx
    ```
 

 
*   Find multiple test components.  *查找多个测试组件。

    ```
    fx shell locate --list test
    ```
