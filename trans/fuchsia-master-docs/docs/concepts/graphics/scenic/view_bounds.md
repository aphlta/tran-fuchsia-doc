 
# Views, Bounds, and Clipping  视图，边界和剪切 

 
- [Introduction](#introduction)  -[简介]（简介）

 
- [Concepts](#concepts)  -[概念]（概念）
  - [Setting View Bounds](#setting-view-bounds)  -[设置视图边界]（设置视图边界）
    - [Bound Extent and Insets](#bound-extent-and-insets)  -[界限和插入]（界限和插入）
    - [Example](#example-1)  -[示例]（示例1）
  - [Coordinate System](#coordinate-system)  -[坐标系]（坐标系）
    - [Example](#example-2)  -[示例]（示例2）
  - [Centering Geometry](#centering-geometry)  -[居中几何]（居中几何）
  - [Debug Wireframe Rendering](#debug-wireframe-rendering)  -[调试线框渲染]（debug-wireframe-rendering）
  - [Ray Casting and Hit Testing](#ray-casting-and-hit-testing)  -[射线投射和命中测试]（射线投射和命中测试）
    - [The Hit Ray](#the-hit-ray)  -[命中之光]（the-hit-ray）
    - [Rules](#rules)  -[规则]（规则）
    - [Edge Cases](#edge-cases)  -[边缘保护套]（边缘保护套）
    - [Pixel Offsets](#pixel-offsets)  -[像素偏移]（像素偏移）
      - [Example](#example-3)  -[示例]（示例3）

 
# Introduction  介绍 

This is a guide that explains how view bounds and clipping work in Scenic. This guide explains how to set view bounds, how to interpret what the commands are doing, and the effects that the view bounds have on existing Scenic subsystems.  这是一本指南，说明了Scene边界和裁剪如何在Scenic中工作。本指南说明了如何设置视图范围，如何解释命令的作用以及视图范围对现有的Scenic子系统的影响。

 
# Concepts  概念 

 
## Setting View Bounds {#setting-view-bounds}  设置视图边界{setting-view-bounds} 

An embedder must create a pair of tokens for a view and view holder, and must also allocate space within its view for the embedded view holder to be laid out. This is done by setting the bounds on the view holder of the embedded view. To set the view bounds on a view, you have to call `SetViewProperties` on its respective ViewHolder. You can call `SetViewProperties` either before or after the view itself is created and linked to the ViewHolder, so you do not have to worry about the order in which you do your setup. The bounds themselves are set by specifying their minimum and maximum points (xyz) in 3D space.  嵌入器必须为视图和视图持有者创建一对标记，并且还必须在其视图内分配空间以布置嵌入式视图持有者。这是通过在嵌入式视图的视图保持器上设置边界来完成的。要在视图上设置视图边界，必须在其各自的ViewHolder上调用`SetViewProperties`。您可以在创建视图本身并将其链接到ViewHolder之前或之后调用`SetViewProperties`，因此不必担心设置的顺序。通过在3D空间中指定其最小和最大点（xyz）来设置边界。

 
### Bound Extent and Insets {#bound-extent-and-insets}  绑定范围和插入{bound-extent-and-insets} 

There are four values needed to set a view's bounds properly, `bounds_min`, `bounds_max`, `inset_min` and `inset_max`. The minimum and maximum bounds represent the minimum and maximum coordinate points of an axis-aligned bounding box. The minimum and maximum insets specify the distances between the view’s bounding box and that of its parent. So the final extent of a view's bounds can be defined with the following formula:  要正确设置视图的边界，需要四个值：bounds_min，bounds_max，inset_min和inset_max。最小和最大边界表示轴对齐的边界框的最小和最大坐标点。最小和最大插图指定视图的边框与其父边框之间的距离。因此，可以使用以下公式定义视图边界的最终范围：

```cpp
{ bounds_min + inset_min, bounds_max - inset_max}
```
 

 
### Example {#example-1}  范例{example-1} 

```cpp
// Create a pair of tokens to register a view and view holder in
// the scene graph.
auto [view_token, view_holder_token] = scenic::ViewTokenPair::New();

// Create the actual view and view holder.
scenic::View view(session, std::move(view_token), "View");
scenic::ViewHolder view_holder(session, std::move(view_holder_token),
                               “ViewHolder");
// Set the bounding box dimensions on the view holder.
view_holder.SetViewProperties({.bounding_box{.min{0, 0, -200}, .max{500, 500, 0}},
                               .inset_from_min{20, 30, 0},
                               .inset_from_max{20, 30, 0}});
```
 

The above code creates a View and ViewHolder pair whose bounds start at (20,&nbsp;30,&nbsp;-200) and extend out to (480,&nbsp;470,&nbsp;0). The bounds themselves are always axis-aligned.  上面的代码创建了一个View和ViewHolder对，其边界从（20，nbsp; -30，-200）开始并扩展到（480，nbsp; 470，nbsp; 0）。边界本身始终与轴对齐。

 
## Coordinate System {#coordinate-system}  坐标系{coordinate-system} 

View bounds are specified in local coordinates, and their world-space position is determined by the global transform of the view node.  视图边界以局部坐标指定，其世界空间位置由视图节点的全局变换确定。

Input coordinates originate from input device space, which usually corresponds to pixel coordinates with an origin at the upper left of the screen. The input system works with the compositor and camera to map from input device coordinates to world space by way of [Ray Casting and Hit Testing](#ray-casting-and-hit-testing).  输入坐标源自输入设备空间，该空间通常对应于像素坐标，其原点位于屏幕左上方。输入系统与合成器和照相机配合使用，以通过[射线投射和命中测试]（射线投射和命中测试）将输入设备坐标映射到世界空间。

 
### Example {#example-2}  范例{example-2} 

```cpp
// Create a view and view-holder token pair.
auto [view_token, view_holder_token] = scenic::ViewTokenPair::New();
scenic::View view(session, std::move(view_token), "View");
scenic::ViewHolder view_holder(session, std::move(view_holder_token),
                               "ViewHolder");

// Add the view holder as a child of the scene.
scene.AddChild(view_holder);

// Translate the view holder and set view bounds.
view_holder.SetTranslation(100, 100, 200);
view_holder.SetViewProperties({.bounding_box{.max{500, 500, 200}}});
```
 

In the above code, the view bounds in local space have a min and max value of (0,&nbsp;0,&nbsp;0) and (500,&nbsp;500,&nbsp;200), but since the parent node is translated by (100,&nbsp;100,&nbsp;200) the view bounds in world space will actually have a world space bounds min and max of (100,&nbsp;100,&nbsp;200) and (600,&nbsp;600,&nbsp;400) respectively. However, the view itself doesn’t see these world-space bounds, and only deals with its bounds in its own local space.  在上面的代码中，局部空间中的视图范围的最小值和最大值分别为（0，nbsp; 0，nbsp; 0）和（500，nbsp; 500，nbsp; 200），但是由于父节点的翻译是（100，nbsp; 100，nbsp; 200）世界范围内的视图范围实际上将具有（100，nbsp; 100，nbsp; 200）和（600，nbsp; 600，nbsp; 400）的世界空间范围的最小值和最大值） 分别。但是，视图本身看不到这些世界空间范围，而仅在其自己的本地空间中处理其范围。

 
## Centering Geometry {#centering-geometry}  居中几何{centering-geometry} 

The center of mass for a piece of geometry such as a `RoundedRectangle` is its center, whereas for a view, the center of mass for its bounds is its minimum coordinate. This means that if a view and a rounded-rectangle that is a child of that view both have the same translation, the center of the rounded-rectangle will render at the minimum-coordinate of the view’s bounds. To fix this, apply another translation on the shape node to move it to the center of the view’s bounds.  诸如“ RoundedRectangle”之类的几何图形的质心是其中心，而对于视图，其边界的质心是其最小坐标。这意味着，如果一个视图和作为该视图子级的圆角矩形都具有相同的平移，则该圆角矩形的中心将在该视图边界的最小坐标处进行渲染。要解决此问题，请在形状节点上应用其他平移，以将其移动到视图边界的中心。

![Centering Geometry Diagram](meta/scenic_centering_geometry.png)  ！[居中几何图]（meta / sceniccentering geometry.png）

 
## Debug Wireframe Rendering {#debug-wireframe-rendering}  调试线框渲染{debug-wireframe-rendering} 

To help with debugging view bounds, you can render the edges of the bounds in wire-frame mode to see where exactly your view is located in world space. This functionality can be applied per-view using a Scenic command:  为了帮助调试视图边界，可以在线框模式下渲染边界的边缘，以查看视图在世界空间中的确切位置。可以使用Scenic命令按视图应用此功能：

```cpp
// This command turns on wireframe rendering of the specified
// view, which can aid in debugging.
struct SetEnableDebugViewBoundsCmd {
    uint32 view_id;
    bool display_bounds;
};
```
 

This command takes in a `view id`, and a `bool` to toggle whether or not the view bounds should be displayed. The default display color is white, but you can choose different colors by running the `SetViewHolderBoundsColorCmd` on the specified view holder:  该命令带有一个“ view id”和一个“ bool”来切换是否显示视图边界。默认显示颜色是白色，但是您可以通过在指定的视图持有人上运行`SetViewHolderBoundsColorCmd`来选择不同的颜色：

```cpp
// This command determines the color to be set on a view holder’s debug
// wireframe bounding box.
struct SetViewHolderBoundsColorCmd {
    uint32 view_holder_id;
    ColorRgbValue color;
};
```
 

 
## Ray Casting and Hit Testing {#ray-casting-and-hit-testing}  射线投射和命中测试{射线投射和命中测试} 

Hit testing by ray casting maps input device coordinates to scene geometry and coordinates. Ultimately, inputs are delivered to views with view coordinates. As described in the [Coordinate System](#coordinate-system) section, view coordinates are determined by the global transform of the view node, which maps from world space to view coordinates.  射线投射的命中测试将输入设备的坐标映射到场景的几何形状和坐标。最终，输入将传递到具有视图坐标的视图。如[坐标系]（坐标系）部分中所述，视图坐标由视图节点的全局变换确定，该节点从世界空间映射到视图坐标。

 
### The Hit Ray {#the-hit-ray}  生命之光{the-hit-ray} 

The conversion from input device space to world space involves the input system, compositor layer, and camera.  从输入设备空间到世界空间的转换涉及输入系统，合成器层和相机。

![Input Coordinate Spaces](meta/input_coordinate_spaces.png)  ！[输入坐标空间]（meta / input_coordinate_spaces.png）

The original input coordinate is a two-dimensional coordinate in screen pixels. The input system and compositor agree on a convention, illustrated above as device coordinates in 3 dimensions (blue), where the viewing volume has depth 1, the near plane is at z = 0, and the far plane is at z = -1. With this in mind, the input system constructs a hit ray with its origin at the touch coordinates at a distance of 1 behind the camera, z = 1, and direction (0,&nbsp;0,&nbsp;-1), towards the scene. (As described in [Pixel Offsets](#pixel-offsets) below, the touch coordinates are jittered by (0.5,&nbsp;0.5); not shown above for simplicity.)  原始输入坐标是屏幕像素的二维坐标。输入系统和合成器在约定上达成一致，如上图所示，为设备坐标的3维（蓝色），其中视区的深度为1，近平面为z = 0，远平面为z = -1。考虑到这一点，输入系统构造了一条命中射线，其原点在触摸坐标处，位于相机后方1处，z = 1，并且朝向场景的方向（0，nbsp; 0，nbsp; -1） 。 （如下面[像素偏移]（像素偏移）中所述，触摸坐标抖动为（0.5，nbsp; 0.5）；为简单起见，上面未显示。）

The input device space as described here is a left-handed coordinate system, a holdover from when Scenic was left-handed. Future work may adjust the z convention of input device space to match NDC or the viewing volume, as a right-handed coordinate system, and adjust the hit ray to originate at the near plane, z = 0.  此处描述的输入设备空间是左手坐标系，这是从Scenic用左手开始的保持时间。将来的工作可能会调整输入设备空间的z约定以匹配NDC或观看量（作为右手坐标系），并调整命中射线以始于近平面z = 0。

The compositor layer transforms this ray into NDC (green) and then applies the inverse camera transforms (clip-space, projection, and camera positioning) to project the ray into the scene (world coordinates, red). The above illustration reflects the orthographic camera coded into Scenic, with scene origin at the upper left of the far plane, viewing volume width and height reflecting device dimensions, and viewing depth 1000, such that the near plane is at z = -1000. (In actuality, the orthographic camera itself is positioned at z = -1010, but this does not affect the math in an orthographic projection.)  合成器层将此光线转换为NDC（绿色），然后应用反向摄影机转换（剪贴空间，投影和摄影机位置）将光线投影到场景中（世界坐标，红色）。上面的插图反映了编码为Scenic的正交摄影机，场景原点位于远平面的左上角，查看体积的宽度和高度反映了设备的尺寸，以及查看深度1000，因此近平面位于z = -1000。 （实际上，正交摄影机本身位于z = -1010处，但这并不影响正交投影中的数学运算。）

In world space then, the hit ray described above originates at (_x_,&nbsp;_y_,&nbsp;-2000) with direction (0,&nbsp;0,&nbsp;1000).  然后，在世界空间中，上述命中射线起源于（_x _，_ y _，-2000）且方向为（0，nbsp; 0，nbsp; 1000）。

 
### Rules {#rules}  规则{rules} 

When performing hit tests, Scenic runs tests against the bounds of a `ViewNode` before determining whether the ray should continue checking children of that node.  在执行命中测试时，Scenic在确定射线是否应继续检查该节点的子代之前，对ViewNode的边界进行测试。

 
* If a ray completely misses a view’s bounding box, nothing that is a child of that   view will be hit.  *如果射线完全错过了视图的边界框，则不会击中该视图的子级。

 
* If a ray does intersect a bounding box, only geometry that exists within the range of the ray’s entrance and exit from the bounding box will be considered for a hit. For example, clipped geometry cannot be hit.  *如果光线确实与边界框相交，则只会考虑光线在边界框的入口和出口范围内的几何形状。例如，剪切的几何体无法被击中。

If you forget to set the bounds for a view, any geometry that exists as a child of that view cannot be hit. This is because the bounds would be null and therefore infinitely small, which also means that there would be no geometry rendered to the screen.  如果您忘记设置视图的边界，则不会击中作为该视图的子级存在的任何几何图形。这是因为边界为零，因此无穷小，这也意味着不会在屏幕上渲染任何几何图形。

In debug mode, a null bounding box will trigger an `FXL_DCHECK` in the `escher::BoundingBox` class stating that the bounding box dimensions need to be greater than or equal to 2.  在调试模式下，空边界框将在escher :: BoundingBox类中触发FXL_DCHECK，指出边界框尺寸必须大于或等于2。

 
### Edge Cases {#edge-cases}  边箱{edge-cases} 

 Situations where a ray is perpendicular to a side of a bounding box and just grazes its edge will not count as a hit. Since the six planes that constitute the bounding box are themselves the clip planes, it follows that anything that is directly on a clip plane would also get clipped.  光线垂直于边界框的一侧并且仅掠过其边缘的情况将不算作命中。由于构成边界框的六个平面本身就是剪切平面，因此，直接在剪切平面上的任何内容也会被剪切。

 
### Collisions {#collisions}  碰撞{collisions} 

A collision occurs when a ray cast detects two or more hits at the same distance. A collision indicates that hittable targets are overlapping and occupying the same position in the scene. This is considered incorrect behavior and Scenic does not provide hit test ordering guarantees in case of collisions. The client must prevent collisions.  当射线投射在相同距离上检测到两个或更多命中时发生碰撞。发生碰撞表明可命中目标重叠并且在场景中占据相同位置。这被认为是不正确的行为，Scenic不会在碰撞情况下提供命中测试的顺序保证。客户必须防止冲突。

There are two ways collisions can occur:  发生冲突的方式有两种：

 
* Collision between nodes in the same view. The owning view must ensure the proper placement of elements within a view.  *同一视图中节点之间的冲突。拥有视图必须确保元素在视图中的正确放置。

 
* Collision between nodes in separate views. The parent view must prevent any intersection between the clip bounds of its children.  *单独视图中节点之间的冲突。父视图必须防止其子级的剪辑边界之间有任何交集。

It is also best practice to follow these rules to avoid Z-fighting for visual content.  遵循这些规则，以避免视觉内容发生Z角冲突也是最佳实践。

When a collision is detected, a warning is logged of the colliding nodes by session id and resource id.  当检测到冲突时，将通过会话ID和资源ID记录冲突节点的警告。

 
### Pixel Offsets {#pixel-offsets}  像素偏移{pixel-offsets} 

When issuing input commands in screen space, pixel values are jittered by (0.5,&nbsp;0.5) so that commands are issued from the center of the pixel and not the top-left corner. This is important to take into account when testing ray-hit tests with bounding boxes, as it will affect the ray origins in world space after they have been transformed, and thus whether or not it results in an intersection.  当在屏幕空间中发出输入命令时，像素值抖动了（0.5，nbsp; 0.5），因此命令是从像素的中心而不是左上角发出的。在使用边界框测试光线照射测试时，必须考虑到这一点，因为光线转换后会影响世界空间中的光线起点，因此是否会导致相交。

The rationale can be illustrated by imagining a 1x1 display. On such a display, to split the difference it would be reasonable for any touch events to be delivered at (0.5,&nbsp;0.5), the center of the screen, rather than at the upper left corner.  可以通过想象一个1x1的显示来说明其原理。在这样的显示器上，为了分散差异，合理的做法是在屏幕中心（0.5，nbsp; 0.5）而不是在左上角传递任何触摸事件。

 
#### Example {#example-3}  范例{example-3} 

```cpp
// Set the bounding box dimensions, just like in the examples above.
view_holder.SetViewProperties({.bounding_box{.max{5, 5, 1}}});

PointerCommandGenerator pointer(compositor_id, 1, 1,
                                PointerEventType::TOUCH);
// Touch the upper left corner of the display.
session->Enqueue(pointer.Add(0.f, 0.f));
```
 

This example shows an orthographic camera setup with a view whose min and max bound points are (0,&nbsp;0,&nbsp;0) and (5,&nbsp;5,&nbsp;1) respectively. There is a touch event at the screen space coordinate point (0,&nbsp;0). If there were no corrections to the pixel offset, an orthographic ray generated at the (0,&nbsp;0) point and transformed into world space would wind up grazing against the edge of the bounding box  and would not register as a hit. However, the “Add” command is jittered to (0.5,&nbsp;0.5) which does actually result in a ray which hits the bounding box. Doing this is the equivalent of running the following command with no jittering:  此示例显示了一个正交摄影机设置，其视图的最小和最大绑定点分别为（0，nbsp; 0，nbsp; 0）和（5，nbsp; 5，nbsp; 1）。屏幕空间坐标点（0,0）处有触摸事件。如果没有对像素偏移进行校正，则在（0,0）点生成并转换为世界空间的正交射线将掠过边界框的边缘，不会记录为命中。但是，“添加”命令会抖动为（0.5，nbsp; 0.5），实际上会导致光线击中边界框。这样做等同于运行以下命令而不会产生抖动：

```cpp
session->Enqueue(pointer.Add(0.5f, 0.5f));
```
