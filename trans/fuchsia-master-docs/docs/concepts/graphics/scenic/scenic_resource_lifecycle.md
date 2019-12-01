 
# Lifecycle of a Scene Graph Resource  场景图资源的生命周期 

This document describes the lifecycle of the basic resources that a client adds to and removes from the scene graph. It focuses on resources that are attachedas Nodes and Views, and is a reference for Scenic's internal handling of theseresources. 本文档描述了客户端添加到场景图中或从场景图中删除的基本资源的生命周期。它专注于作为节点和视图附加的资源，并且是Scenic对这些资源的内部处理的参考。

Many Resources follow the Node lifecycle: Resources are created and added to the ResourceMap. Resources are kept alive by reference counting. As such,inter-scene graph references will keep resources in the scene graph alive, evenif the client calls `ReleaseResource`. The release command removes the Resourcefrom the client's internally-managed `ResourceMap`, which means that the clientcannot apply any future commands to that Resource. This document highlights howthe scene graph can keep Resources added to it alive, with the key exception ofthe View resource  -- which is solely held onto via the client's ResourceMap. 许多资源遵循节点生命周期：创建资源并将其添加到ResourceMap。通过引用计数使资源保持活动状态。这样，即使客户端调用“ ReleaseResource”，场景间图引用也将使场景图中的资源保持活动状态。 release命令从客户端内部管理的“ ResourceMap”中删除资源，这意味着客户端无法将任何将来的命令应用于该资源。本文档重点介绍了场景图如何使添加的资源保持活动状态，但View资源的关键例外-视图资源仅通过客户端的ResourceMap保留。

This follows a simple embedded-embeddee client pair, and assumes the clients have set up all [necessary resources](scenic.md#scenic-resource-graph) to addNodes and Views to the global, retained scene graph. 这遵循一个简单的嵌入式嵌入式客户端对，并假定客户端已设置所有[必要资源]（scenic.mdscenic-resource-graph），以将Nodes和Views添加到全局保留场景图。

> Note: the code shown below is typically handled by the UI C++ SDK wrappers. All code examples show FIDL commands, as they are seen by Scenic. >注意：下面显示的代码通常由UI C ++ SDK包装程序处理。所有代码示例均显示FIDL命令，如Scenic所见。

 
## Node Lifecycle  节点生命周期 

 
### Adding a Node to the Scene  向场景添加节点 

Say the embedder client (Client A) has created a root Scene node in its Session, accessed via `root_id`. Client A can create children and add that to the rootnode via the following commands: 假设嵌入式客户端（客户端A）在其会话中创建了一个根场景节点，可通过“ root_id”访问。客户端A可以创建子代，然后通过以下命令将其添加到rootnode：

```c++
CreateScene(root_id);
CreateEntityNode(entity_node_id);
AddChild(root_id, entity_node_id);
```
 

Internally, this creates a Node, adds it to the Session's ResourceMap, and sets the EntityNode as the child of the root node in the scene graph: 在内部，这将创建一个Node，将其添加到Session的ResourceMap中，并将EntityNode设置为场景图中根节点的子级：

![Image of a simple scene graph. There is a root Scene node with a strong link to its child entity node. Client A's ResourceMap also has a strong reference toboth the root node and the entity node. There is a second image to the right,labeled "projected scene", that shows a blank screen.](meta/scene_graph_lifecycle_root.png) ！[简单场景图的图像。有一个根场景节点，该节点具有与其子实体节点的牢固链接。客户端A的ResourceMap对根节点和实体节点也有很强的引用。右边还有第二个图像，标记为“投影场景”，显示空白屏幕。]（meta / scene_graph_lifecycle_root.png）

Client A can apply commands to the EntityNode as long as it maintains a reference to it in the ResourceMap. For example: 客户端A可以将命令应用于EntityNode，只要它在ResourceMap中维护对其的引用即可。例如：

```c++
SetTranslation(entity_node_id, {0, h/2, 0});
CreateShapeNode(shape_node_id);
CreateShape(shape_node_id, triangle);
AddChild(entity_node_id, shape_node_id);
```
 

![Image of the expanded scene graph. There is a root Scene node with a strong link to its child entity node. The entity node has a strong link to is child,a shape node with a triangle shape. Client A's ResourceMap also has a strongreference to all the nodes in the scene. There is a second image to the right,labeled "projected scene", that shows a triangle on the bottom half of thescreen.](meta/scene_graph_lifecycle_node_scene.png) ！[展开的场景图的图像。有一个根场景节点，该节点具有与其子实体节点的牢固链接。实体节点与子节点（三角形）的形状节点有很强的联系。客户端A的ResourceMap还具有对场景中所有节点的强烈引用。右边还有第二个图像，标记为“投影场景”，在屏幕的下半部分显示一个三角形。]（meta / scene_graph_lifecycle_node_scene.png）

 
### Removing a Node  删除节点 

Releasing the Resource releases it from the ResourceMap. It does not release it from the Scene graph, due to a strong reference from the parent. Client A canrelease the Resources backing the "triangle dialog", and it will still remainon the screen: 释放资源会从ResourceMap中释放它。由于父级的强烈引用，它不会从“场景”图中释放它。客户端A可以释放支持“三角形对话框”的资源，它仍然保留在屏幕上：

```c++
ReleaseResource(entity_node_id);
```
 

![Image of the scene graph in the image above. Client A's ResourceMap no longer has a strong reference to the entity node. The "projected scene" image isunchanged.](meta/scene_graph_lifecycle_node_scene_2.png) ！[上图中的场景图图像。客户端A的ResourceMap不再对实体节点具有强引用。 “投影场景”图像未更改。]（meta / scene_graph_lifecycle_node_scene_2.png）

To remove the triangle from the screen, the client would have to explicitly detach the nodes from the scene graph. When the `Resource` is removed from boththe ResourceMap and from the scene graph, the resource is destroyed. 要从屏幕上删除三角形，客户端必须从场景图中显式分离节点。当从ResourceMap和场景图中同时删除“ Resource”时，资源将被销毁。

```c++
DetachChildren(root_id);
```
 

![Image of the scene graph. Its only node is the root scene node. The ResourceMap has a strong reference to the root node and the shape nodecontaining the triangle shape. There is no entity node. The "projected scene"image is a blank screen](meta/scene_graph_lifecycle_node_scene_detach.png) ！[场景图的图像。它唯一的节点是根场景节点。 ResourceMap对根节点和包含三角形的形状节点有很强的引用。没有实体节点。 “投影场景”图像是黑屏]（meta / scene_graph_lifecycle_node_scene_detach.png）

 
## Embedding a View  嵌入视图 

 
### Add a ViewHolder to the SceneGraph  将ViewHolder添加到SceneGraph 

To embed a View from another Session, Client A must make a `ViewHolder` Resource, and add it as a child of a node to add it to the scene graph. 要从另一个会话嵌入视图，客户端A必须创建一个“ ViewHolder”资源，并将其添加为节点的子代，以将其添加到场景图。

```c++
CreateEntityNode(entity_node_id);
AddChild(root_id, entity_node_id);

CreateViewHolder(view_holder_id, view_holder_token);
AddChild(entity_node_id, view_holder_id);
```
 

![Image of the scene graph containing a scene root node with a child EntityNode. The EntityNode has a ViewHolder child. Client A's ResourceMap has a strongreference to the Scene, EntityNode, and the ViewHolder.](meta/scene_graph_lifecycle_viewholder.png) ！[场景图的图像包含带有子EntityNode的场景根节点。 EntityNode有一个ViewHolder子级。客户端A的ResourceMap强烈引用了Scene，EntityNode和ViewHolder。]（meta / scene_graph_lifecycle_viewholder.png）

The ViewHolder follows the same lifecycle rules as a Node, [described above](#node-lifecycle). It will remain part of the scene graph as long as it is connected to something inthe scene graph. However, the client cannot add children to the ViewHolder:instead, its corresponding View is linked by Scenic. ViewHolder遵循与节点相同的生命周期规则，[如上所述]（node-lifecycle）。只要它连接到场景图中的某物，它将一直保留在场景图中。但是，客户端无法将子代添加到ViewHolder：相反，其相应的View由Scenic连接。

 
### Link a View to a ViewHolder  将视图链接到ViewHolder 

The `view_token` from the ViewHolder/View token pair is passed to the embedded Session (Client B). When Client B creates a View from that token, a `View` iscreated and added to the client's ResourceMap. Scenic creates links between theView to the ViewHolder to establish this cross-Session connection. The Viewthen creates a "phantom `ViewNode`", and sets that as the child of theViewHolder. The ViewNode represents Client B's root node in the scene graph. 来自ViewHolder / View令牌对的`view_token`被传递到嵌入式会话（客户端B）。当客户端B从该令牌创建视图时，将创建一个“视图”并将其添加到客户端的ResourceMap。 Scenic将在View和ViewHolder之间创建链接以建立此跨会话连接。 Viewthen创建一个“ phantom`ViewNode`”，并将其设置为ViewHolder的子级。 ViewNode表示场景图中客户端B的根节点。

```c++
CreateView(view_id, view_token);
```
 

![Image of the scene graph above: Client A's ResourceMap maintains a strong reference to the ViewHolder, EntityNode, and Scene, all added to the scenegraph. Client B's View and ViewNode are also added to the scene graph: theViewHolder maintains a strong reference to the ViewNode, and a weak reference tothe View. The View also maintains a strong reference to the ViewNode. Client B'sResourceMap only points to the View.](meta/scene_graph_lifecycle_embedded_view.png) 上面场景图的图像：客户端A的ResourceMap维护了对ViewHolder，EntityNode和Scene的强烈引用，所有这些都添加到了场景图中。客户端B的View和ViewNode也添加到场景图中：ViewHolder维护对ViewNode的强引用，而对View的弱引用。视图还维护着对ViewNode的强烈引用。客户B的资源地图仅指向视图。]（meta / scene_graph_lifecycle_embedded_view.png）

Client B can then add children to the View, just like it can to Nodes. Under the hood, the ViewNode maintains the children's connections to the scene graph: 然后，客户端B可以将子代添加到视图，就像它可以添加到节点一样。在后台，ViewNode维护子级与场景图的连接：

```c++
CreateShapeNode(shape_node_id);
CreateShape(shape_node_id, rectangle);
AddChild(view_id, shape_node_id);
```
 

![Image of the scene graph above. A ShapeNode containing a rectangle is added to the scene graph as the child of the ViewNode. Client B's ResourceMap also has astrong reference to the ShapeNode. The "projected scene" image shows a rectangleon the screen.](meta/scene_graph_lifecycle_embedded_view_with_nodes.png) ！[上方场景图的图像。包含矩形的ShapeNode作为ViewNode的子级添加到场景图。客户端B的ResourceMap还具有对ShapeNode的强烈引用。 “投影场景”图像在屏幕上显示一个矩形。]（meta / scene_graph_lifecycle_embedded_view_with_nodes.png）

 
### Removing a View  删除视图 

A View is a viable Resource and added to the scene as long as it is in the client's ResourceMap. It differs from a traditional Node because the scene graphdoes not maintain a strong reference to the View Resource. To perform removal ofa View, Client B must command Scenic to release the View resource. Unlike anode, the client does not have to command Scenic to detach it from the scenegraph. Releasing the View Resource destroys the View and its phantom ViewNode,and detaches the View and its subtree from the global scene graph: 视图是可行的资源，只要它在客户端的ResourceMap中，它就被添加到场景中。它与传统的Node不同，因为场景图不维护对View资源的强烈引用。要执行View的移除，客户端B必须命令Scenic释放View资源。与阳极不同，客户端不必命令Scenic将其与场景图形分离。释放View资源会破坏View及其幻影ViewNode，并将View及其子树与全局场景图分离：

```c++
ReleaseResource(view_id);
```
 

![Image of the scene graph with Client A's nodes still attached. Client B's View and ViewNode are destroyed, but its ResourceMap maintains a strong reference tothe ShapeNode.](meta/scene_graph_lifecycle_embedded_view_detach.png) ！[场景图的图像，客户端A的节点仍处于连接状态。客户端B的View和ViewNode被销毁，但其ResourceMap维护了对ShapeNode的强烈引用。]（meta / scene_graph_lifecycle_embedded_view_detach.png）

> Note: if either the View or ViewHolder is destroyed, its pair is delivered a disconnected event (i.e. `fuchsia.ui.gfx.ViewHolderDisconnected` or`fuchsia.ui.gfx.ViewDisconnected`, respectively). >注意：如果View或ViewHolder中的任何一个被销毁，则它们的对将传递一个断开连接的事件（即，分别为fuchsia.ui.gfx.ViewHolderDisconnected或fuchsia.ui.gfx.ViewDisconnected）。

 
### Removing a ViewHolder  卸下ViewHolder 

A ViewHolder is treated as another child node in a Session, and so follows the same [lifecycle rules](#removing-a-node). If a ViewHolder is released as aResource, and detached from the scene graph, the ViewHolder is destroyed. ViewHolder被视为会话中的另一个子节点，因此遵循相同的[生命周期规则]（删除节点）。如果ViewHolder作为资源发布，并且与场景图分离，则ViewHolder被销毁。

Say that Client B has not released its View. When the ViewHolder is destroyed, this breaks any link to the View, and destroys the strong reference to the childViewNode. The embedded View is thus detached from the scene. The embeddedSession and embedded View's subtree may still be intact, though no longervisible. 假设客户B尚未发布其视图。销毁ViewHolder时，这会断开与View的任何链接，并销毁对childViewNode的强引用。因此，嵌入的View与场景分离。尽管不再可见，embeddedSession和Embedded View的子树可能仍然完好无损。

```c++
Detach(view_holder_id);
ReleaseResource(view_holder_id);
```
 

![Image of the scene graph shows just the Scene root in the graph; Client A maintains a strong reference to the Scene node. There is no ViewHolder. ClientB's subtree maintains the strong reference between the ViewNode and its childShapeNode, and Client B's ResourceMap maintains its links to the View and theShapeNode. The "projected scene" image is a blank screen.](meta/scene_graph_lifecycle_destroyed_viewholder.png) ！[场景图的图像仅显示图中的场景根；客户端A维护对Scene节点的强烈引用。没有ViewHolder。 ClientB的子树维护ViewNode及其childShapeNode之间的强引用，而Client B的ResourceMap维护其与View和theShapeNode的链接。 “投影场景”图像是空白屏幕。]（meta / scene_graph_lifecycle_destroyed_viewholder.png）

> Note: Any embedded Sessions are notified if they are detached from the scene via the `fuchsia.ui.gfx.ViewDetachedFromSceneEvent`. >注意：如果任何嵌入式Session通过“ fuchsia.ui.gfx.ViewDetachedFromSceneEvent”与场景分离，则会收到通知。

 

 

 

