Vulkan Development ================== Vulkan开发==================

 
## Runtime dependencies  运行时依赖 

The magma driver and libraries should already be built into a complete Fuchsia image, however you should have your project depend on the 'magma' package to be sure that the necessary files are included in the system image of whatever build includes your project.  岩浆驱动程序和库应该已经内置到完整的Fuchsia映像中，但是您应该使项目依赖于“ magma”包，以确保必要的文件包含在任何包含您的项目的系统映像中。

 
## Buildtime dependencies  建立时间依赖性 

In order for your project to access the Vulkan headers, and to link against the Vulkan loader libvulkan.so, add the following GN dependency:  为了使您的项目访问Vulkan标头并链接到Vulkan加载程序libvulkan.so，请添加以下GN依赖项：

`//garnet/public/lib/vulkan`  `// garnet / public / library / vulkan`

 
## Rendering onscreen  在屏幕上渲染 

There are two options for displaying your rendered output:  有两个选项可显示渲染的输出：

 
1. The system compositor  1.系统合成器

   See Scenic documentation for details.  有关详细信息，请参见Scenery文档。

 
2. Directly to the display  2.直接显示

   This method is not compatible with a system that has a system compositor.  此方法与具有系统合成器的系统不兼容。

You can use a custom version of the WSI swapchain:  您可以使用WSI交换链的自定义版本：

https://www.khronos.org/registry/vulkan/specs/1.0-extensions/html/vkspec.html#_wsi_swapchain  https://www.khronos.org/registry/vulkan/specs/1.0-extensions/html/vkspec.html_wsi_swapchain

For details on the magma customization, refer to the vkcube example here:  有关岩浆定制的详细信息，请参见此处的vkcube示例：

`third_party/vkcube/cube.cc`  `third_party / vkcube / cube.cc`

 
## Interaction with the graphics console  与图形控制台的交互 

The magma display driver supports toggling ownership between the main display owner, and the graphics console.  岩浆显示驱动程序支持在主显示所有者和图形控制台之间切换所有权。

Currently, on system startup the gfxconsole owns the display.  当前，在系统启动时，gfxconsole拥有显示器。

When a Vulkan application starts, it will take over the display.  Vulkan应用程序启动时，它将接管显示。

To toggle display ownership between the Vulkan app and the gfxconsole, press alt-esc.  要在Vulkan应用程序和gfxconsole之间切换显示所有权，请按alt-esc。

 
## Reporting issues  报告问题 

Keep an eye on the system log for various types of graphics driver specific issues, and file tickets on the Magma project. The driver should kill the connection corresponding to the context that was executing when these issues occurred; but otherwise should handle this failure gracefully. 密切注意系统日志中各种类型的图形驱动程序特定问题以及Magma项目上的文件凭单。驱动程序应终止与发生这些问题时正在执行的上下文相对应的连接。但否则应妥善处理此故障。

If nothing works afterward, please file that as an issue as well.  如果事后没有任何效果，请也将其作为问题提出。

 
### Gpu fault  GPU故障 

Looks something like the following. This can happen due to user error or driver bug. Please make sure your app has no validation layer issues.  看起来像以下内容。由于用户错误或驱动程序错误，可能会发生这种情况。请确保您的应用没有验证层问题。

If you believe your app is innocent, please file a Magma ticket and include at least this portion of the log, plus ideally a recipe to repro:  如果您认为自己的应用是无辜的，请提交一份岩浆票，并至少包括日志的这一部分，以及理想情况下可以复制的食谱：

```
> [WARNING] GPU fault detected
> ---- device dump begin ----
> RELEASE build
> Device id: 0x1916
> RENDER_COMMAND_STREAMER
> sequence_number 0x1003
> active head pointer: 0x1f328
> ENGINE FAULT DETECTED
> engine 0x0 src 0x3 type 0x0 gpu_address 0x1000000
> mapping cache footprint 11.9 MB cap 190.0 MB
> ---- device dump end ----
> [WARNING] resetting render engine
```
 

 
### Gpu hang  Gpu坑 

If a command buffer fails to complete within a certain amount of time, the gpu driver should detect the condition and treat it as if a fault occurred.  如果命令缓冲区在一定时间内未能完成，则gpu驱​​动程序应检测到这种情况并将其视为发生故障。

Again, may be an application error or driver bug. If you believe your app is innocent, please file a Magma ticket and include at least this portion of the log, plus ideally a recipe to repro:  同样，可能是应用程序错误或驱动程序错误。如果您认为自己的应用是无辜的，请提交一份岩浆票，并至少包括日志的这一部分，以及理想情况下可以复制的食谱：

```
> [WARNING] Suspected GPU hang: last submitted sequence number 0x1007 master_interrupt_control 0x80000000
> ---- device dump begin ----
> DEBUG build
> Device id: 0x1916
> RENDER_COMMAND_STREAMER
> sequence_number 0x1006
> active head pointer: 0x20
> No engine faults detected.
> mapping cache footprint 0.0 MB cap 0.0 MB
> ---- device dump end ----
> [WARNING] resetting render engine
```
 

 
## Demo  演示版 

