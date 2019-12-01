 
# Units and Metrics  单位和度量 

This document defines the system of units and metrics used by the Fuchsia graphics system. 本文档定义了樱红色图形系统使用的单位和度量标准系统。

[TOC]  [目录]

 
## Goals  目标 

The purpose of this system of units and metrics is to solve the following problems: 此单位和度量标准系统的目的是解决以下问题：

 
* Define a device-specific unit, the **pixel (px)**, used to describe low-level characteristics of targets or sources of image data. *定义特定于设备的单位**像素（px）**，用于描述目标或图像数据源的低级特征。

 
* Define a physical unit, the **millimeter (mm)**, used as a physical basis for scale calculations. *定义物理单位**毫米（mm）**，用作比例计算的物理基础。

 
* Define a scalable unit, the **pip (pp)**, used by UI frameworks for layout purposes.  Its scale is derived from physical quantities, well-definedconfiguration parameters, and through the use of empirical models to ensurea consistent visual impact and to optimize usability for a user or group ofusers across a broad range of devices and viewing environments. *定义可伸缩单位** pip（pp）**，UI框架将其用于布局。它的规模是从物理量，定义明确的配置参数以及使用经验模型得出的，以确保一致的视觉效果并在广泛的设备和观看环境中为用户或一组用户优化可用性。

 
* Help creators develop intuition about the perceptual significance of individual measurements expressed in scalable units.  For example, **14 pp**might be generally a good number for small readable text.  Please refer to theuser interface design guidelines for the actual numbers. *帮助创作者对以可伸缩单位表示的单个测量的感知重要性形成直觉。例如，对于小尺寸可读文本，** 14 pp **通常可能是一个很好的数字。请参阅用户界面设计指南以获取实际编号。

 
* Allow software to determine how many pixels to render for optimum fidelity.  *允许软件确定要渲染多少像素以获得最佳保真度。

 
* Allow software to determine known physical relations.  For example, it is possible to draw a graduated ruler accurately when the display's physicalsize and density are accurately known. *允许软件确定已知的物理关系。例如，当准确知道显示器的物理尺寸和密度时，可以精确地绘制刻度尺。

 
## System of Units  单位制 

Fuchsia's graphics systems uses a few units of measure for distinct purposes, as summarized in this table. 樱红色的图形系统使用几个度量单位来达到不同的目的，如下表所示。

| Name and Notation   | Definition      | Purpose                  | |---------------------|-----------------|--------------------------|| **Pixel (px)**      | Device-specific | Rendering and Sampling   || **Millimeter (mm)** | Physical        | Scale Factor Calibration || **Pip (pp)**        | Scalable        | Layout Position and Size | |名称和符号定义|目的| | --------------------- | ----------------- | --------- ----------------- || **像素（px）** |特定于设备|渲染和采样|| **毫米（mm）** |物理|比例因子校准|| **点（pp）** |可扩展布局位置和大小|

The following sections describe each unit in more detail.  以下各节将更详细地介绍每个单元。

 
### Pixels (px)  像素（px） 

The **pixel** is a device-specific unit of length for expressing dimensions as a range of addressable picture elements for a particular device.For the purposes of this definition, a **device** is considered to be anytarget or source of image data such as a display, a camera, or a texture. ``像素''是特定于设备的长度单位，用于将尺寸表示为特定设备的可寻址图像元素的范围。出于此定义的目的，``设备''被视为任何目标或来源图像数据，例如显示器，照相机或纹理。

It is common to express the size of a planar graphical object in the device's coordinate system in terms of its width and height in whole or fractional pixelunits.  Similarly it is common to use pixel units to express positions andvectors in that space. 通常，以设备坐标系中平面图形对象的大小（以其整体或分数像素单位的宽度和高度）来表示。类似地，通常使用像素单位来表示该空间中的位置和向量。

Pixel units are not used to describe depth or elevation.  像素单位不用于描述深度或高程。

A **pixel** can also mean a single addressable picture element which measures exactly **1 px** wide by **1 px** high. “像素”也可以表示单个可寻址像素，其尺寸正好为“ 1像素”宽乘以“ 1像素”高。

 
#### Details  细节 

Fuchsia's graphics system uses **pixel units** when performing device-specific graphical operations such as when rendering a scene, drawing text, decoding avideo, or sampling from a texture. 紫红色的图形系统在执行特定于设备的图形操作时（例如，渲染场景，绘制文本，解码视频或从纹理采样时）使用“像素单位”。

Pixel units should not be used directly for user interface layout because they are not scalable and therefore cannot adapt across devices; use **pip units**instead. 像素单元不应直接用于用户界面布局，因为它们不可扩展，因此无法在所有设备之间适应。改为使用“点子单位”。

Pixel units may have different physical manifestations depending on the device they relate to.  It is common for all pixel units of a given device to be ofthe same physical size and to have a square aspect ratio but this may notbe true for some devices. 像素单元可能取决于其所涉及的设备而具有不同的物理表现形式。给定设备的所有像素单元通常具有相同的物理尺寸并具有平方长宽比，但这对于某些设备可能并非如此。

 
#### Examples  例子 

 
* A 1080p display operating at its native resolution is **1920 px** wide by **1080 px** high.  Assuming each pixel is encoded in 32 bits, a linear framebuffer for this display would require a total of 8294400 bytes(1920 x 1080 x 4). *以原始分辨率运行的1080p显示器宽** 1920像素**高** 1080像素**。假设每个像素都以32位编码，则此显示的线性帧缓冲区总共需要8294400字节（1920 x 1080 x 4）。

 
* A single frame of YV12 encoded 720p video is **1280 px** wide by **720 px** high although its effective color resolution is lower due to theuse of chroma subsampling. * YV12编码的720p视频的单个帧的宽度为1280像素**高720像素**，尽管由于使用色度二次采样，其有效色彩分辨率较低。

 
### Millimeters (mm)  毫米（mm） 

The **millimeter** is a standard unit of length for expressing the physical dimensions and spatial relations of real world objects and their analogues.It is equivalent to 1/1000th of a **meter** as defined by the InternationalSystem of Units (SI). 毫米''是用于表示现实世界物体及其类似物的物理尺寸和空间关系的标准长度单位，相当于国际单位制定义的``米''的1/1000（ SI）。

It is common to express the size of physical objects in whole or fractional millimeter units or as ratios involving millimeters such as **pixels permillimeter (px/mm)**. 通常以整数或分数毫米为单位表示物理对象的大小，或者以涉及毫米的比率表示物理对象的大小，例如**像素/毫米（px / mm）**。

 
#### Details  细节 

Fuchsia's graphics system uses known physical measurements in **millimeters** to calibrate other units, such as **pip units** (see below).  When these physicalmeasurements are not known, the system will use different formulations tocompensate for the lack of this information. 紫红色的图形系统使用已知的以“毫米”为单位的物理尺寸来校准其他单位，例如“点单位”（请参见下文）。当这些物理测量值未知时，系统将使用不同的公式来弥补此信息的不足。

Millimeters are commonly used to express physical relationships with other units in the form of ratios, such as the number of pixels per millimeter of a display. 毫米通常用于以比率的形式表示与其他单位的物理关系，例如显示器每毫米的像素数。

Millimeters should not be used directly for user interface layout because they do not capture the perceptual effects of viewing distance and other usabilityconcerns; use **pip units** instead. 毫米不能直接用于用户界面布局，因为它们不能捕获观看距离和其他可用性问题的感知影响；请改用“点子单位”。

 
#### Examples  例子 

 
* One particular display might have an active area that is **257.8 mm** high by **171.9 mm** wide with a pixel density of **8.4 px/mm**. *一种特定的显示器可能具有** 257.8 mm **高** 171.9 mm **宽的有效区域，像素密度为** 8.4 px / mm **。

 
* The nominal viewing distance of that particular display in a typical viewing environment might be approximately **500 mm**. *在典型的观看环境中，该特定显示器的标称观看距离可能约为** 500 mm **。

 
### Pip Units (pp)  点数单位（pp） 

The **pip** is a device-independent scalable unit of length for layout of user interfaces and other graphical content in Fuchsia.  Its purpose is to ensure aconsistent visual impact and to optimize usability for a user or group of usersacross a broad range of devices and viewing environments. pip **是与设备无关的可扩展长度单位，用于在紫红色中布局用户界面和其他图形内容。其目的是确保在广泛的设备和观看环境中为用户或一组用户提供一致的视觉冲击并优化可用性。

It is common to express the size of an idealized planar or volumetric graphical object in terms of its width, height, and depth in whole or fractional pips.Similarly it is common to use pips to express positions and vectors in a userinterface. 通常用理想的平面或体积图形对象的宽度，高度和深度来表示整个或小数点的大小。类似地，通常使用点来表示用户界面中的位置和矢量。

The pip unit has a **equilateral cube aspect ratio**: objects whose width, height, and depth have equal dimension in pip units will have an equalapparent width, height, and depth when rendered to the output device. pip单位具有“等边立方长宽比” **：以pip单位的宽度，高度和深度具有相等尺寸的对象在渲染到输出设备时将具有相等的表观宽度，高度和深度。

A **pip unit square** is a square which measures **1 pp** wide by **1 pp** high.  **点单位平方**是一个正方形，其尺寸为** 1 pp **宽乘** 1 pp **高。

A **pip unit cube** is a cube which measures **1 pp** wide by **1 pp** high by **1 pp** deep. 点子单位立方体**是一个立方体，其尺寸为：** 1 pp **宽*** 1 pp **高*** 1 pp **深。

Pip units are used at design time and on the device at run time to provide a form of scale invariance. 点设计单位在设计时使用，在运行时在设备上使用，以提供一种形式不变的尺度。

 
* At design time, the developer uses pip units to describe the size and position of idealized graphical objects based on the user interfacedesign guidelines. *在设计时，开发人员根据用户界面设计准则使用点子单位描述理想图形对象的大小和位置。

 
* At run time, the system dynamically calculates an appropriate **pip unit transformation* to map pip units to pixel units for each outputdevice.  This transformation takes into account the device pixel density,nominal viewing distance, and other factors to maintain a consistentvisual impact across a range of configurations.  It is adjusted as neededwhenever any of its underlying factors changes. *在运行时，系统动态计算适当的**点单位转换*，以将点单位映射到每个输出设备的像素单位。此转换考虑了设备像素密度，标称观看距离和其他因素，以在各种配置范围内保持一致的视觉效果。每当其任何基本因素发生变化时，都会根据需要进行调整。

 
* Changes in the pip unit transformation affect the level of detail required to maintain graphical fidelity.  For example, if the pip to pixel ratioincreases by a factor of two, then a view may need to allocate texturestwice as many pixels wide and tall to prevent content from becoming blurryat that scale.  The view's node metrics provide the necessary informationto determine the required level of detail. *点子单位转换中的更改会影响保持图形保真度所需的详细程度。例如，如果点对像素的比例增加了两倍，则视图可能需要分配两倍于宽度和高度的像素，以防止内容在该比例下变得模糊。视图的节点指标提供了必要的信息，以确定所需的详细程度。

 
* Because the scene graph is dimensioned in scalable units, its overall layout is invariant under camera movements; only the level of detailchanges.  This would not be true if the scene graph were dimensions in pixels. *由于场景图以可伸缩单位标注尺寸，因此其整体布局在摄像机移动的情况下是不变的；仅更改细节的级别。如果场景图是以像素为单位的尺寸，则情况并非如此。

 
* By convention, the local coordinate system of the root node of each view is one-to-one with pips.  Thus the contents of each view can be directlymeasured in pips assuming no other local coordinate transformations areapplied by the view to its content. *按照惯例，每个视图的根节点的局部坐标系与点是一对一的。因此，假设该视图没有将其他局部坐标转换应用到其内容，则可以直接以点为单位测量每个视图的内容。

 
#### Details  细节 

Fuchsia's graphics system uses *pip units* extensively for layout in the scene graph and applies a transformation at rendering time. 紫红色的图形系统在场景图中广泛使用* pip单位*进行布局，并在渲染时进行变换。

The pip unit transformation is a combination of the following factors.  点单位转换是以下因素的组合。

 
* Aspect ratio correction: Preserves equal apparent width, height, and depth for objects of equal width, height, and depth in pip units. *宽高比校正：对于宽度，高度和深度相同的对象，以pip单位保留相同的外观宽度，高度和深度。

 
* Angular size correction: Adapts the scale of objects to a common resolution- independent baseline taking into account the physical pixel density and thenominal viewing distance.  Although pip units scale proportionally withangular resolution, other corrections cause them not to have a constantapparent angular size in practice. *角度大小校正：考虑到物理像素密度和标称观看距离，将对象的比例调整为与分辨率无关的通用基线。尽管点子单位与角度分辨率成比例地缩放，但其他校正导致它们在实践中不具有恒定的视在角度大小。

 
* Ergonomic correction: Adapts the scale of objects to compensate for the information architecture needs of particular classes of devices due to howthey are intended to be used, allowing for the presentation of more or lessinformation in the same canvas. *人机工程学校正：调整对象的比例，以补偿特定类别设备的信息体系结构需求，这取决于它们的使用方式，从而允许在同一画布中显示或多或少的信息。

 
* Perceptual correction: Adapts the scale of objects to compensate for perceptual effects which occur based on the user's context and viewingenvironment. *感知校正：调整对象的比例以补偿根据用户的上下文和观看环境而发生的感知效果。

 
* User correction: Adapts the scale of objects to compensate for user preferences such as their accessibility needs.  This term has no effectwhen default user settings are in effect. *用户校正：调整对象的比例以补偿用户的偏好，例如其可访问性需求。当默认用户设置生效时，该术语无效。

See [Display Metrics](#display_metrics) for more details about how the pip unit transformation is actually determined and used. 有关如何实际确定和使用点单位转换的更多详细信息，请参见[显示指标]（display_metrics）。

 
#### Examples  例子 

 
* **1 pp** on a handheld information device typically used at arm's length with default settings corresponds to a visual angle of approximately 0.0255 degrees.This is similar to the **Android density-independent pixel (dp)** unit. *手持信息设备上的** 1 pp **通常在默认设置下与手臂保持一致，对应的可视角度约为0.0255度。这类似于** Android密度无关像素（dp）**单位。

 
* By comparison, the [CSS Reference Pixel](https://www.w3.org/TR/css-values-3/#reference-pixel) is defined to have a visual angle of 0.0213 degrees. *通过比较，[CSS参考像素]（https://www.w3.org/TR/css-values-3/reference-pixel）被定义为具有0.0213度的视角。

 
## Metrics  指标 

Fuchsia's graphics system provides APIs for programs to access scale factors, physical dimensions, and other information essential to adapting graphicaloutput for a particular rendering context. 紫红色的图形系统为程序提供API，以访问比例因子，物理尺寸以及其他对于使图形输出适应特定渲染环境必不可少的信息。

These properties are collectively known as **Metrics** and are summarized in the following tables. 这些属性统称为“指标”，并在下表中进行了汇总。

 
### Display Metrics {#display_metrics}  显示指标{display_metrics} 

Display metrics describe the physical characteristics of a particular display and its basic scale factors. 显示指标描述了特定显示器的物理特性及其基本比例因子。

| Name            | Unit  | Definition                                               | |-----------------|-------|----------------------------------------------------------|| Scalable Width  | pp    | Width of visible content area in pips                    || Scalable Height | pp    | Height of visible content area in pips                   || Pip Scale X     | px/pp | Nominal pixels per pip unit in X                         || Pip Scale Y     | px/pp | Nominal pixels per pip unit in Y                         || Pip Density     | pp/mm | Physical pip unit density (optional)                     || Display Width   | px    | Width of visible content area in pixels                  || Display Height  | px    | Height of visible content area in pixels                 || Physical Width  | mm    | Width of visible content area in millimeters (optional)  || Physical Height | mm    | Height of visible content area in millimeters (optional) | |姓名|单位定义| | ----------------- | ------- | ----------------------- ----------------------------------- ||可缩放宽度| pp |可见内容区域的宽度，以点为单位可扩展高度pp |可见内容区域的高度，以点为单位磅秤X | px / pp |每点单位的名义像素X ||磅秤Y | px / pp |每点单位的名义像素Y ||点密度pp /毫米|物理点单位密度（可选）||显示宽度px |可见内容区域的宽度，以像素为单位||显示高度px |可见内容区域的高度（以像素为单位）||物理宽度|毫米可见内容区域的宽度，以毫米为单位（可选）||物理高度|毫米可见内容区域的高度，以毫米为单位（可选）|

 
### View Metrics  查看指标 

View metrics describe the local layout constraints of an individual user interface component based on the view is embedded into the view hierarchy. 视图度量基于嵌入视图层次结构中的视图来描述单个用户界面组件的局部布局约束。

Views receive this information at runtime in the form of **ViewProperties**. View properties may change dynamically in response to view hierarchy changeswhich affect the view's layout. 视图在运行时以** ViewProperties **的形式接收此信息。视图属性可以响应于影响视图布局的视图层次结构更改而动态更改。

| Name               | Unit  | Definition                 | |--------------------|-------|----------------------------|| View Width         | pp    | Width constraint in pips   || View Height        | pp    | Height constraint in pips  || View Max Elevation | pp    | Maximum elevation in pips  | |姓名|单位定义| | -------------------- | ------- | -------------------- -------- ||查看宽度| pp |以点为单位的宽度限制||查看高度| pp |以点为单位的高度限制||查看最大高程| pp |最大高度（点）|

The view is generally expected to layout its content so as to fill the available width and height at elevation zero. 通常希望该视图对内容进行布局，以填充零高程处的可用宽度和高度。

Since views can be three dimensional, the maximum elevation places an upper bound on the elevation of the airspace which the view is allowed to use. 由于视图可以是三维的，因此最大标高为允许使用该视图的空域标高设置了上限。

 
### Node Metrics  节点指标 

Node metrics describe the local rendering context of a node in the scene graph based on the characteristics of the rendering target into which the node isprojected and the transformations applied by the node's ancestors. 节点度量基于节点要投影到的渲染目标的特征以及节点祖先应用的转换来描述场景图中节点的本地渲染上下文。

Nodes receive this information at runtime in the form of **MetricsEvents**. Node metrics may change dynamically in response to scene graph changeswhich affect the node's projection into the rendering target. 节点在运行时以** MetricsEvents **的形式接收此信息。节点度量可以响应于场景图变化而动态变化，这影响了节点到渲染目标中的投影。

| Name             | Unit  | Definition                           | |------------------|-------|--------------------------------------|| Pip Unit Scale X | px/pp | Nominal pixels per pip unit in X     || Pip Unit Scale Y | px/pp | Nominal pixels per pip unit in Y     || Pip Unit Density | pp/mm | Physical pip unit density (optional) | |姓名|单位定义| | ------------------ | ------- | ---------------------- ---------------- ||点单位比例X | px / pp |每点单位的名义像素X ||点子单位比例Y | px / pp |每点单位的名义像素Y ||点单位密度| pp /毫米|物理点单位密度（可选）|

The pip unit scale factor is important for deciding the resolution of textures needed to achieve optimum fidelity on the rendering target.  For example, givena uniform pip unit scale factor of **2.5**, the ideal texture size to fill aa **150 pp** by **100 pp** rectangle is **375 px** by **250 px**. 点单位比例因子对于确定在渲染目标上实现最佳保真度所需的纹理分辨率至关重要。例如，给定一个统一的点数单位缩放系数** 2.5 **，则以** 100 pp **矩形填充** 150 pp **的理想纹理尺寸为** 375 px ** ** 250 px * *。

The pip unit density is useful for mapping scalable dimensions to or from physical dimensions, although this may not be possible if the rendering target'sphysical resolution is unknown. 点单位密度对于将可缩放的尺寸映射到物理尺寸或从物理尺寸映射可缩放的尺寸很有用，尽管如果渲染目标的物理分辨率未知，则可能无法实现。

These metrics are designed to consider the overall context of the node in the scene graph.  For example, if an ancestor of the node applies a 200% scaletransformation to the subtree containing the node, then the node will receivean updated metrics event containing values which are scaled up by 200%.This informs the node that it may need to allocate higher resolution texturesto maintain optimum fidelity. 这些度量标准旨在考虑场景图中节点的整体上下文。例如，如果节点的祖先对包含该节点的子树应用200％scaletransformation，则该节点将接收到一个更新的指标事件，其中包含按比例放大200％的值，这通知该节点可能需要分配更高的值分辨率纹理可保持最佳保真度。

TODO(SCN-378): Node metrics currently do not take into account the effects of certain transformations such as perspective projections and rotationswhich could affect the necessary level of detail required to maintain optimumfidelity or the accuracy of physical registration.  We should considerintroducing additional factors in Scenic to help estimate these effects. TODO（SCN-378）：节点度量标准当前未考虑某些转换（例如透视投影和旋转）的影响，这些转换可能会影响保持最佳保真度或物理配准准确性所需的必要细节水平。我们应该考虑在“风景区”中引入其他因素来帮助估计这些影响。

 
## Model Parameters  型号参数 

The Fuchsia graphics system automatically calculates metrics based on an empirical model using information about a display's physical characteristics,its viewing environment, user preferences, and other contextual cues. 紫红色的图形系统使用与显示器的物理特性，其观看环境，用户偏好和其他上下文提示有关的信息，基于经验模型自动计算度量。

For this model to function correctly, it needs accurate parameters.  为了使该模型正确运行，需要准确的参数。

In particular, when a model parameter is not accurately known a priori, such as the display's exact physical size and pixel density, then it must bereported as having an unknown value. 特别地，当模型参数没有被先验地准确地知道时，例如显示器的确切物理尺寸和像素密度，则必须将其报告为具有未知值。

Do not provide fake or poorly estimated input parameters; report them as unknown instead.  The display model is responsible for choosing sensibledefaults based on what actually is known. 不要提供虚假的或估计错误的输入参数；将其报告为未知。显示模型负责根据实际已知的信息选择合理的默认值。

In some situations, it may be appropriate to prompt the end-user to supply missing information during setup to optimize fidelity. 在某些情况下，可能会提示最终用户在设置过程中提供丢失的信息以优化保真度。

Refer to the **DisplayModel** class for more details.  有关更多详细信息，请参考** DisplayModel **类。

TODO(SCN-379): Document specific calibration procedures and expected accuracy bounds for each model parameter. TODO（SCN-379）：记录每个模型参数的特定校准程序和预期精度范围。

 
### Display Information  显示信息 

The display information describes the physical characteristics of a particular display. 显示信息描述了特定显示器的物理特性。

| Name            | Unit  | Definition                                | |-----------------|-------|-------------------------------------------|| Display Width   | px    | Width of visible content area             || Display Height  | px    | Height of visible content area            || Physical Width  | mm    | Width of visible content area (optional)  || Physical Height | mm    | Height of visible content area (optional) || Pixel Density   | px/mm | Pixel density of active area (optional)   | |姓名|单位定义| | ----------------- | ------- | ----------------------- -------------------- ||显示宽度px |可见内容区域的宽度||显示高度px |可见内容区域的高度||物理宽度|毫米可见内容区域的宽度（可选）||物理高度|毫米可见内容区域的高度（可选）||像素密度|像素/毫米|活动区域的像素密度（可选）|

 
### Environment Information  环境信息 

The environment information describes the physical characteristics of how a display is typically used and perceived in a given environment. 环境信息描述了在给定环境中通常如何使用和感知显示器的物理特征。

| Name             | Unit  | Definition                                   | |------------------|-------|----------------------------------------------|| Usage            | usage | Intended usage of the display (optional)     || Viewing Distance | mm    | Nominal apparent viewing distance (optional) | |姓名|单位定义| | ------------------ | ------- | ---------------------- ------------------------ ||用法用法显示屏的预期用途（可选）观看距离|毫米标称视距（可选）|

The usage classification expresses how a particular display is intended to be used in a given context.  This information helps the system selectappropriate defaults and adjust the information architecture to suit the roleof that display. 使用分类表示如何在给定的上下文中使用特定的显示。此信息有助于系统选择适当的默认值，并调整信息体系结构以适合该显示角色。

 
* **Unknown**: The role of the display is unknown.  * **未知**：显示器的作用未知。
* **Handheld**: The display is mounted in a device which is typically supported by the user in one or both hands.  The user interface will be optimized forsingle-user direct manipulation.  Like a phone or tablet. * **手持**：显示器安装在用户通常会用一只手或两只手支撑的设备中。用户界面将针对单用户直接操作进行优化。就像手机或平板电脑一样。
* **Close**: The display is mounted in a device which is typically located well within arm's reach of the user.  The user interface will be optimizedfor single-user direct and indirect manipulation.  Like a laptop. * **关闭**：显示器安装在通常位于用户可及范围内的设备中。用户界面将针对单用户直接和间接操作进行优化。就像一台笔记本电脑。
* **Near**: The display is mounted in a device which is typically located at arm's reach from the user.  The user interface will be optimized forsingle-user indirect manipulation.  Like a desktop. * **近**：显示器安装在通常位于用户伸手可及之处的设备中。用户界面将针对单用户间接操作进行优化。就像台式机一样。
* **Far**: The display is mounted in a device which is typically located well beyond arm's reach of the user or a group of users and is intended to beviewed from a variety of distances.  The user interface will be optimized forsingle-user and multi-user interaction and media consumption.  Like a TV. * **远**：显示器安装在设备上，该设备通常位于用户或一组用户无法触及的范围内，并且可以从各种距离观看。用户界面将针对单用户和多用户交互以及媒体消耗进行优化。就像电视一样。

The viewing distance estimates how far away objects presented on the display at a zero elevation will appear to the user. 观看距离估计以零仰角显示在显示器上的对象将向用户显示多远。

 
### User Information  用户信息 

The user information describes the user's preferences and accessibility needs which may override some of the behavior of the model. 用户信息描述了用户的首选项和可访问性需求，这些需求可能会覆盖模型的某些行为。

| Name              | Unit  | Definition                           | |-------------------|-------|--------------------------------------|| User Scale Factor | pp/pp | Magnification Ratio (default is 1.0) | |姓名|单位定义| | ------------------- | ------- | --------------------- ----------------- ||用户比例因子| pp / pp |放大倍率（默认为1.0）

