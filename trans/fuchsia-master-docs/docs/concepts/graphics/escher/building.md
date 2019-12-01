 
# Escher build instructions  Escher制作说明 

Escher can be built targetting both Fuchsia and Linux.  Building for Linux is useful because it allows use of Vulkan development tools that are not yet available on Fuchsia.  Escher可以针对紫红色和Linux构建。为Linux构建非常有用，因为它允许使用Fuchsia尚不可用的Vulkan开发工具。

 
## Building for Fuchsia  紫红色建筑Escher itself is part of any Fuchsia build that includes Scenic, i.e. any build that targets a device with a screen.  The Escher examples and tests are built by adding `//garnet/packages/examples:escher` and `//garnet/packages/tests:escher` to your `fx set` invocation.  Escher本身是包括Scenic的任何紫红色构建的一部分，即，任何针对带有屏幕设备的构建。通过将`// garnet / packages / examples：escher`和`// garnet / packages / tests：escher`添加到fx set调用中，可以构建Escher示例和测试。

 
## Building for Linux  为Linux构建Escher can also build on Linux.  In order to do so, you need to:  Escher也可以在Linux上构建。为此，您需要：

 
    ```
    sudo apt install libxinerama-dev libxrandr-dev libxcursor-dev libx11-xcb-dev \
    libx11-dev mesa-common-dev
    ```
  * install build dependencies  *安装构建依赖项

 
  * install a GPU driver that supports Vulkan  *安装支持Vulkan的GPU驱动程序

 
      ```
      sudo apt install nvidia-driver
      ```
    * NVIDIA: version >= 367.35  * NVIDIA：版本> = 367.35

 
      ```
      sudo apt install mesa-vulkan-drivers
      ```
    * Intel: Mesa >= 12.0  *英特尔：Mesa> = 12.0

 
    ```
    export VULKAN_SDK=$FUCHSIA_DIR/prebuilt/third_party/vulkansdk/linux/x86_64
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$VULKAN_SDK/lib
    export VK_LAYER_PATH=$VULKAN_SDK/etc/vulkan/explicit_layer.d
    ```
  * set the VK_LAYER_PATH, and LD_LIBRARY_PATH environment variables, e.g.:  *设置VK_LAYER_PATH和LD_LIBRARY_PATH环境变量，例如：

 
    ```
    cd $FUCHSIA_DIR
    fx set terminal.x64 --with='//garnet/packages/examples:escher,//garnet/packages/tests:escher' --args escher_use_null_vulkan_config_on_host=false
    ```
  * Specify that you want the Escher examples and unit-tests to be built:  *指定您要构建Escher示例和单元测试：

 
    * See [Getting started](/docs/getting_started.md) for how to set up the `fx` tool.  *有关如何设置`fx`工具的信息，请参见[使用入门]（/ docs / getting_started.md）。

 
    * The command-line above is just an example.  For example, you can use a different product than `terminal` or use a more inclusive package such as `//garnet/packages/examples:all`.  *上面的命令行只是一个示例。例如，您可以使用与“终端”不同的产品，也可以使用更具包容性的软件包，例如“ // garnet / packages / examples：all”。

 
    ```
    fx build host_x64/waterfall && out/default/host_x64/waterfall
    ```
  * Do the following each time you want to rebuild and run the `waterfall` example:  *每次要重建并运行“瀑布”示例时，请执行以下操作：

 
    ```
    fx build host_x64/escher_unittests && out/default/host_x64/escher_unittests
    ```
