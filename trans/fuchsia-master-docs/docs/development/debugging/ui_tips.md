 
# UI Debugging Tips  UI调试技巧 

For general debugging info see the [Fuchsia Debugging Workflow](/docs/development/debugging/debugging.md).  有关常规调试信息，请参见[Fuchsia调试工作流程]（/ docs / development / debugging / debugging.md）。

 
## Capture the Screen  捕捉屏幕 

 
### Take a Screenshot  截图A screenshot takes a screenshot of what is currently displayed on the Fuchsia device's screen. It returns a 2D buffer. 屏幕截图截取了Fuchsia设备屏幕上当前显示的屏幕截图。它返回一个2D缓冲区。

From the Fuchsia device console, run: `screencap /tmp/filename.ppm` 在Fuchsia设备控制台中，运行：`screencap / tmp / filename.ppm`

From your host workstation, run: `fx scp [$(fx netaddr --fuchsia)]:/tmp/filename.ppm /tmp/filename.ppm` 在主机工作站上，运行：`fx scp [$（fx netaddr --fuchsia）]：/ tmp / filename.ppm / tmp / filename.ppm`

 
### Take a Snapshot  拍摄快照A snapshot takes a 3D representation of what is currently displayed on the screen. It usually takes longer to capture than a screenshot, and can be used to visualize issues with layout of 3D content. 快照以3D形式表示屏幕上当前显示的内容。通常，捕获所需的时间比截屏要长，并且可以用于可视化3D内容布局的问题。

From your host workstation, run: `fx shell gltf_export > filename.gltf` 在主机工作站上，运行：`fx shell gltf_export> filename.gltf`

You can upload `filename.gltf` to any gltf viewer, such as this [online viewer](https://gltf-viewer.donmccurdy.com/).  您可以将`filename.gltf`上传到任何gltf查看器，例如此[在线查看器]（https://gltf-viewer.donmccurdy.com/）。

 
### Dump the SceneGraph as Text  将SceneGraph转储为文本The [SceneGraph](/docs/concepts/graphics/scenic/scenic.md#scenic-resource-graph) as text is useful when you want to see all the resources, including non-visible elements such as transform matrices.  当您想查看所有资源，包括不可见元素（例如变换矩阵）时，[SceneGraph]（/ docs / concepts / graphics / scenic / scenic.mdscenic-resource-graph）作为文本很有用。

 
#### Dump the SceneGraph in Bugreport  在Bugreport中转储SceneGraphThe Fuchsia Bugreport contains the SceneGraph that is rendered to the screen. Capture it from your host workstation using the following commands:  紫红色Bugreport包含呈现到屏幕的SceneGraph。使用以下命令从主机工作站捕获它：

`fx bugreport` `unzip <bugreport output file>` `fx bugreport``解压缩<bugreport输出文件>`

Then, look for Scenic’s info in the inspect file:  然后，在检查文件中查找Scenic的信息：

`cat inspect.json | less`  `cat inspect.json |更少`

 
#### Dump the SceneGraph and all Scenic Resources  转储SceneGraph和所有风景资源To capture all the Resources created, including those that are not currently attached to the main SceneGraph, you can use `dump-scenes`. From your host workstation, run the following command: 要捕获所有创建的资源，包括当前未附加到主SceneGraph的资源，可以使用`dump-scenes`。在主机工作站上，运行以下命令：

