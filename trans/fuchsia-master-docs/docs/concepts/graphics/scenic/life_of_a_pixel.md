 
# Life of a Pixel  像素寿命 

A client requests a set of commands to be Presented as part of a future Scenic frame. A single Scenic frame can have multiple client "Presents", where each Present represents a Session's update to the global scene graph. Thisdoc describes the architecture internal to Scenic for how a request becomes pixels. 客户请求将一组命令呈现为将来的“风景区”框架的一部分。一个场景框架可以具有多个客户端“呈现者”，其中每个“呈现者”代表会话对全局场景图的更新。本文档描述了Scenic内部的体系结构，以了解请求如何变为像素。

The diagram below shows the steps a client Present follows when it is requested. Everything between the Scenic FIDL Boundary and the Vulkan driver is currently single-threaded and executes sequentially. (Note, there are ongoing refactors to simplify these series of steps. See SCN-1202 for more info). 下图显示了客户端提出请求时应遵循的步骤。目前，Scenic FIDL边界和Vulkan驱动程序之间的所有内容都是单线程的，并按顺序执行。 （请注意，正在进行重构以简化这些系列步骤。有关更多信息，请参见SCN-1202。）

 
0. Client Enqueue()s a set of commands to change its content, and calls Present().  0.客户端Enqueue（）提供了一组命令来更改其内容，并调用Present（）。
1. The Present request is funneled through the scenic::Session ...  1.通过风景秀丽的:: Session对当前请求进行漏斗...
2. ... through SessionHandler ...  2. ...通过SessionHandler ...
3. ... to gfx::Session. This places a wait on the Present acquire_fences, and schedules an update for the targeted presentation_time.  3. ...到gfx :: Session。这将在“当前” acquire_fences上等待，并为目标presentation_time安排更新。
4. The FrameScheduler places the request on a task. This waits for the target_presentation time, then calls SessionUpdater::UpdateSessions().  4. FrameScheduler将请求放置在任务上。这将等待target_presentation时间，然后调用SessionUpdater :: UpdateSessions（）。
5. The GfxSystem is a SessionUpdater. For each client Session, it calls ApplyScheduledUpdates(). If the acquire_fences for the Session are reached, the commands are applied to the Scene Graph (step 6).Else, if the acquire_fences are not reached, the udpate is considered "failed" and returns to the FrameScheduler. The FrameScheduler then increments the target_present time by a VSYNC interval, and retries the update on the next frame. 5. GfxSystem是一个SessionUpdater。对于每个客户端会话，它将调用ApplyScheduledUpdates（）。如果达到了会话的acquired_fences，则将命令应用于场景图（步骤6）。否则，如果未达到acquired_fences，则将udpate视为“失败”并返回到FrameScheduler。然后，FrameScheduler将target_present时间增加VSYNC间隔，并在下一帧上重试更新。
6. Commands from a Session are applied to the global scene graph. The scene graph is dirty at this time, and should not be read by other systems (i.e. input).  6.来自会话的命令将应用于全局场景图。场景图此时很脏，不应由其他系统（即输入）读取。
7. When the SessionUpdaters have successfully updated, the FrameScheduler is notified the scene graph is dirty, and triggers a RenderFrame() on the FrameRenderer.  7. SessionUpdaters成功更新后，会通知FrameScheduler场景图很脏，并在FrameRenderer上触发RenderFrame（）。
8. The gfx::Engine is a FrameRenderer. To draw a frame, its renderer traverses the scene graph and creates Escher::objects for each element in the scene. It then passes these obejcts to Escher, and calls DrawFrame(). The Escher interprets these objects as vk::commands, and sends those to the GPU.  8. gfx :: Engine是一个FrameRenderer。要绘制框架，其渲染器将遍历场景图并为场景中的每个元素创建Escher :: objects。然后，将这些对象传递给Escher，并调用DrawFrame（）。 Escher将这些对象解释为vk :: commands，并将其发送到GPU。

 

