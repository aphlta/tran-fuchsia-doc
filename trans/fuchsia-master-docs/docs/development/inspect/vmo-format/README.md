 

 
# Inspection File Format  检查文件格式 

[TOC]  [目录]

This document describes the **Component Inspection File Format** (Inspect Format).  本文档介绍了“组件检查文件格式”（检查格式）。

Files formatted using the Inspect Format are known as **Inspect Files**, which commonly have a `.inspect` file extension. 使用检查格式格式化的文件称为“检查文件”，通常具有.inspect文件扩展名。

 

 
# Overview  总览 

[Component Inspection][inspect] provides components with the ability to expose structured, hierarchical information about their state at runtime. [组件检查] [检查]使组件能够在运行时公开有关其状态的结构化层次信息。

Components host a mapped Virtual Memory Object ([VMO]) using the Inspect Format to expose an **Inspect Hierarchy** containing this internal state. 组件使用检查格式来托管映射的虚拟内存对象（[VMO]），以公开包含此内部状态的“检查层次结构”。

An Inspect Hierarchy consists of nested **Nodes** containing typed **Properties**.  检查层次结构由嵌套的**节点**组成，其中包含类型化的**属性**。

 
## Goals  目标 

The Inspect Format described in this document has the following goals:  本文档中描述的检查格式具有以下目标：

 
- **Low-overhead mutations to data**  -**数据的开销较小**

The Inspect File Format allows data to be changed in-place. For instance, the overhead of incrementing an integer is ~2 atomic increments. 检查文件格式允许就地更改数据。例如，增加整数的开销约为2个原子增量。

 
- **Support a non-static hierarchy**  -**支持非静态层次结构**

The hierarchy stored in an Inspect File can be modified at runtime. Children can be added or removed from the hierarchy at anytime. In this way, the hierarchy can closely represent the hierarchy ofobjects in the component's working set. 可以在运行时修改存储在检查文件中的层次结构。可以随时在层次结构中添加或删除子级。这样，层次结构可以紧密表示组件工作集中的对象的层次结构。

 
- **Single writer, multiple reader concurrency without explicit synchronization**  -**单个编写器，多个读取器并发，无需显式同步**

Readers operating concurrently with the writer map the VMO and attempt to take a snapshot of the data. Writers indicate being in a critical sectionthough a *generation counter* that requires no explicit synchronizationwith readers. Readers use the generation counter to determine when asnapshot of the VMO is consistent and may be safely read. 与写入器同时运行的读取器映射VMO并尝试获取数据快照。尽管*生成计数器*不需要与读者进行显式同步，但作者表示自己处于关键部分。读者使用生成计数器来确定VMO快照何时一致并且可以安全读取。

 
- **Data may remain available after component termination**  -**组件终止后数据可能仍然可用**

A reader may maintain a handle to the VMO containing Inspect data even after the writing component terminates. 即使在写入组件终止后，读取器仍可以维护包含Inspect数据的VMO的句柄。

[inspect]: /docs/development/inspect/README.md  [检查]：/docs/development/inspect/README.md

 
## Terminology  术语 

This section defines common terminology used in this document.  本节定义了本文档中使用的通用术语。

 
* Inspect File - A bounded sequence of bytes using the format described in this document.  *检查文件-使用本文档中描述的格式的有界字节序列。
* Inspect VMO - An Inspect File stored in a Virtual Memory Object (VMO).  *检查VMO-检查文件，存储在虚拟内存对象（VMO）中。
* Block - A sized section of an Inspect File. Blocks have an Index and an Order.  *块-检查文件的大小部分。块具有索引和顺序。
* Index - A unique identifier for a particular Block. `byte_offset = index * 16`  *索引-特定块的唯一标识符。 `byte_offset = index * 16`
* Order - The size of a block given as a bit shift from the minimum size. `size_in_bytes = 16 << order`. Separates blocks intoclasses by their (power of two) size. *顺序-块的大小与最小大小之间的位移。 `size_in_bytes = 16 << order`。将块按其（2的幂）大小分成几类。
* Node  - A named value in the hierarchy under which other values may be nested. Only Nodes may be parents in the Hierarchy. *节点-层次结构中可以嵌套其他值的命名值。在层次结构中，只有节点可以是父级。
* Property - A named value that contains typed data (e.g. String, Integer, etc). *属性-包含类型化数据（例如String，Integer等）的命名值。
* Hierarchy - A tree of Nodes, descending from a single "root" node, that may each contain Properties. An Inspect File contains asingle Hierarchy. 层次结构-节点树，从单个“根”节点派生而来，每个节点可能包含属性。检查文件包含单个层次结构。

This document uses MUST, SHOULD/RECOMMENDED, and MAY keywords as defined in [RFC 2119][rfc2119]  本文档使用[RFC 2119] [rfc2119]中定义的务必，应该/推荐和MAY关键字

All bit field diagrams are stored in little-endian ordering.  所有位域图均按小端顺序存储。

[rfc2119]: https://www.ietf.org/rfc/rfc2119.txt  [rfc2119]：https://www.ietf.org/rfc/rfc2119.txt

 
# Blocks  积木 

Inspect files are split into a number of `Blocks` whose size must be a power of 2. 检查文件分为多个“块”，其大小必须为2的幂。

The minimum block size must be 16 bytes (`MIN_BLOCK_SIZE`) and the maximum block size must be a multiple of 16 bytes. Implementers arerecommended specify a maximum block size less than the size of a page(typically 4096 bytes). In our reference implementation, the maximumblock size is 2048 bytes (`MAX_BLOCK_SIZE`). 最小块大小必须为16个字节（“ MIN_BLOCK_SIZE”），最大块大小必须为16个字节的倍数。建议实现者指定最大块大小小于页面大小（通常为4096字节）。在我们的参考实现中，最大块大小为2048个字节（“ MAX_BLOCK_SIZE”）。

All blocks must be aligned on 16-byte boundaries, and addressing within the VMO is in terms of an Index, specifying a 16-byte offsets (`offset =index * 16`). 所有块必须在16字节边界上对齐，并且VMO内的寻址是根据索引，指定16字节偏移量（“偏移=索引* 16”）。

We use 28 bits for indexes, so Inspect Files may be at most 4GiB.  我们使用28位作为索引，因此检查文件最多为4GiB。

A `block_header` consists of 16 bytes as follows:  “ block_header”由16个字节组成，如下所示：

![Figure: Block header organization](blockheader.png)  ！[图：块头组织]（blockheader.png）

Each block has an `order`, specifying its size.  每个块都有一个“顺序”，指定其大小。

If the maximum block size is 2048 bytes, then there are 8 possible block orders (`NUM_ORDERS`), numbered 0...7, corresponding to blocks of sizes16, 32, 64, 128, 256, 512, 1024, and 2048 bytes respectively. 如果最大块大小为2048字节，则有8个可能的块顺序（“ NUM_ORDERS”），编号为0 ... 7，对应于大小为16、32、64、128、256、512、1024和2048字节的块分别。

Each block also has a type, which is used to determine how the rest of the bytes in the block are to be interpreted. 每个块还具有一种类型，该类型用于确定如何解释该块中的其余字节。

 
## Buddy Allocation  好友分配 

This block layout permits efficient allocation of blocks using [buddy allocation][buddy]. Buddy allocation is the recommended allocationstrategy, but it is not a requirement for using the Inspect Format. 这种块布局允许使用[预算分配] [预算]有效分配块。伙伴分配是推荐的分配策略，但不是使用检查格式的要求。

 
# Types  种类 

All the supported types are defined in [//zircon/system/ulib/inspect/include/lib/inspect/cpp/vmo/block.h][block.h]which fall into categories as follows: 所有受支持的类型在[//zircon/system/ulib/inspect/include/lib/inspect/cpp/vmo/block.h][block.h]中定义，分为以下类别：

enum             | value | type name | category -----------------|-------|----------------|-------`kFree`          | 0     | `FREE`             | Internal`kReserved`      | 1     | `RESERVED`         | Internal`kHeader`        | 2     | `HEADER`           | Header`kNodeValue`     | 3     | `NODE_VALUE`       | Value`kIntValue`      | 4     | `INT_VALUE`        | Value`kUintValue`     | 5     | `UINT_VALUE`       | Value`kDoubleValue`   | 6     | `DOUBLE_VALUE`     | Value`kPropertyValue` | 7     | `PROPERTY_VALUE`   | Value`kExtent`        | 8     | `EXTENT`           | Extent`kName`          | 9     | `NAME`             | Name`kTombstone`     | 10    | `TOMBSTONE`        | Value`kArrayValue`    | 11    | `ARRAY_VALUE`      | Value`kLinkValue`     | 12    | `LINK_VALUE`       | Value 枚举价值|类型名称|类别----------------- | ------- | ---------------- | ------ -`kFree` | 0 | `FREE` |内部`kReserved` | 1 | `保留`|内部`kHeader` | 2 | `HEADER` |标头“ kNodeValue” | 3 | `NODE_VALUE` |值`kIntValue` | 4 | `INT_VALUE` |值`kUintValue` | 5 | `UINT_VALUE` |值`kDoubleValue` | 6 | `DOUBLE_VALUE` |价值`kPropertyValue` | 7 | `PROPERTY_VALUE` |价值`kExtent` | 8 | `EXTENT` |范围`kName` | 9 | `NAME` |名称`kTombstone` | 10 | `TOMBSTONE` |值`kArrayValue` | 11 | `ARRAY_VALUE` |值`kLinkValue` | 12 | `LINK_VALUE` |值

 
* *Internal* - These types are provided for implementing block allocation, and they must be ignored by readers. * *内部*-这些类型是为实现块分配而提供的，读者必须忽略它们。

 
* *Header* - This type allows readers to detect Inspect Files and reason about snapshot consistency. This block must exist at index 0. * * Header *-此类型使读者可以检测检查文件并确定快照一致性的原因。该块必须存在于索引0处。

 
* *Value* - These types appear directly in the hierarchy. Values must have a *Name* and a parent (which must be a `NODE_VALUE`). * *值*-这些类型直接显示在层次结构中。值必须具有* Name *和父项（必须为`NODE_VALUE`）。

 
* *Extent* - This type stores long binary data that may not fit in a single block.  * * Extent *-此类型存储的长二进制数据可能无法容纳在单个块中。

 
* *Name* - This type stores binary data that fits in a single block, and it is typically used to store the name of values. * *名称*-此类型存储适合单个块的二进制数据，通常用于存储值的名称。

Each type interprets the payload differently, as follows:  每种类型对有效负载的解释不同，如下所示：

 
* [FREE](#free)  * [免费]（免费）
* [RESERVED](#reserved)  * [保留]（保留）
* [HEADER](#header)  * [HEADER]（标题）
* [Common VALUE fields](#value)  * [通用值字段]（值）
* [NODE\_VALUE](#node)  * [NODE \ _VALUE]（节点）
* [INT\_VALUE](#numeric)  * [INT \ _VALUE]（数字）
* [UINT\_VALUE](#numeric)  * [UINT \ _VALUE]（数字）
* [DOUBLE\_VALUE](#numeric)  * [DOUBLE \ _VALUE]（数字）
* [PROPERTY\_VALUE](#property)  * [PROPERTY \ _VALUE]（属性）
* [EXTENT](#extent)  * [EXTENT]（范围）
* [NAME](#name)  * [NAME]（姓名）
* [TOMBSTONE](#node)  * [TOMBSTONE]（节点）
* [ARRAY\_VALUE](#array)  * [ARRAY \ _VALUE]（数组）
* [LINK](#link)  * [LINK]（链接）

 
## FREE {#free}  免费{免费} 

![Figure: Free block](freeblock.png)  ！[图：免费块]（freeblock.png）

A `FREE` block is available for allocation. Importantly, the zero-valued block (16 bytes of `\0`) is interpreted as a `FREE` block of order 0,so buffers may simply be zeroed to free all blocks. “ FREE”块可用于分配。重要的是，零值块（\ 0的16个字节）被解释为0阶的FREE块，因此可以简单地将缓冲区清零以释放所有块。

Writer implementations may use the unused bits from 8..63 of `FREE` blocks for any purpose. Writer implementation must set all other unusedbits to 0. 编写器实现可以出于任何目的使用“ FREE”块的8..63中的未使用位。编写器实现必须将所有其他未使用的位设置为0。

It is recommended that writers use the location specified above to store the index of the next free block of the same order. Using this field,free blocks may create singly linked lists of free blocks of each sizefor fast allocation. The end of the list is reached when NextFreeBlockpoints to a location that is either not `FREE` or not of the same order(commonly the Header block at index 0). 建议作者使用上面指定的位置存储相同顺序的下一个空闲块的索引。使用此字段，空闲块可以创建每种大小的空闲块的单链接列表，以进行快速分配。当NextFreeBlock指向一个不是“ FREE”或不同顺序的位置时（通常是位于索引0的Header块），到达列表的末尾。

 
## RESERVED {#reserved}  保留{reserved} 

![Figure: Reserved block](reservedblock.png)  ！[图：预留块]（reservedblock.png）

`RESERVED` blocks are simply available to be changed to a different type.  It is an optional transitional state between the allocation of ablock and setting its type that is useful for correctness checking ofimplementations (to ensure that blocks that are about to be used arenot treated as free). 可以将`RESERVED`块更改为其他类型。它是分配块与设置其类型之间的可选过渡状态，对于实现实现的正确性检查非常有用（以确保不会将要使用的块视为空闲块）。

 
## HEADER {#header}  标题{header} 

![Figure: Header block](headerblock.png)  ！[图：标题块]（headerblock.png）

There must be one `HEADER` block at the beginning of the file. It consists of a **Magic Number** ("INSP"), a **Version** (currently 0), and the**Generation Count** for concurrency control. The first byte of the headermust not be a valid ASCII character. 文件开头必须有一个“ HEADER”块。它由一个“ Magic Number”（魔数）（“ INSP”），一个“ Version”（版本）（当前为0）以及用于并发控制的“ Generation Count”组成。标头的第一个字节必须不是有效的ASCII字符。

See the [next section](#concurrency) for how concurrency control must be implemented using the generation count. 有关必须如何使用生成计数来实现并发控制的信息，请参见[下一部分]（并发）。

 
## \*\_VALUE {#value}  \ * \ _ VALUE {value} 

![Figure: general value block](generalvalue.png)  ！[图：常规值块]（generalvalue.png）

Values all start with the same prefix, consisting of the index of the parent for the value and the index of the name associated with the value. 所有值均以相同的前缀开头，由值的父级索引和与值关联的名称索引组成。

The payload is interpreted differently depending on the type of value, as below. 如下所示，根据值的类型对有效负载进行不同的解释。

 
## NODE\_VALUE and TOMBSTONE {#node}  NODE \ _VALUE和TOMBSTONE {node} 

![Figure: Node and Tombstone blocks](objtombblock.png)  ！[图：节点和墓碑块]（objtombblock.png）

Nodes are anchor points for further nesting, and the `ParentID` field of values must only refer to blocks of type `NODE_VALUE`. 节点是用于进一步嵌套的锚点，并且值的“ ParentID”字段必须仅引用类型为“ NODE_VALUE”的块。

`NODE_VALUE` blocks support optional *reference counting* and *tombstoning* to permit efficient implementations as follows: `NODE_VALUE`块支持可选的*引用计数*和*逻辑删除*，以实现如下所示的有效实现：

The `Refcount` field may contain the number of values referencing a given `NODE_VALUE` as their parent. On deletion, the `NODE_VALUE` becomes a newspecial type called `TOMBSTONE`. `TOMBSTONE`s are deleted only when their`Refcount` is 0. “ Refcount”字段可以包含将给定的“ NODE_VALUE”作为其父级引用的值的数量。删除后，`NODE_VALUE`成为新的特殊类型，称为“ TOMBSTONE”。仅当其“引用计数”为0时，“ TOMBSTONE”才被删除。

This allows for writer implementations that do not need to explicitly keep track of children for Nodes, and it prevents the following scenario: 这允许不需要显式跟踪Node的子代的writer实现，并且可以防止出现以下情况：

```
// "b" has a parent "a"
Index | Value
0     | HEADER
1     | NODE "a", parent 0
2     | NODE "b", parent 1

/* delete "a", allocate "c" as a child of "b" which reuses index 1 */

// "b"'s parent is now suddenly "c", introducing a cycle!
Index | Value
0     | HEADER
1     | NODE "c", parent 2
2     | NODE "b", parent 1
```
 

 
## \{INT,UINT,DOUBLE\}\_VALUE {#numeric}  \ {INT，UINT，DOUBLE \} \ _ VALUE {数字} 

![Figure: Numeric type block](numericblock.png)  ！[图：数字类型块]（numericblock.png）

Numeric `VALUE` blocks all contain the 64-bit numeric type inlined into the second 8 bytes of the block. 数值“ VALUE”块均包含内联到该块的后8个字节中的64位数字类型。

 
## PROPERTY\_VALUE {#property}  PROPERTY \ _VALUE {属性} 

![Figure: Property value block](stringblock.png)  ！[图：属性值块]（stringblock.png）

General `PROPERTY_VALUE` blocks reference arbitrary byte data across one or more linked `EXTENT` blocks. 一般的“ PROPERTY_VALUE”块在一个或多个链接的“ EXTENT”块中引用任意字节数据。

`PROPERTY_VALUE` blocks contain the index of the first `EXTENT` block holding the binary data, and they contain the total length of the data in bytesacross all extents. PROPERTY_VALUE块包含保存二进制数据的第一个EXTENT块的索引，并且它们包含所有扩展区中数据的总长度（以字节为单位）。

The format flags specify how the byte data should be interpreted, as follows: 格式标志指定应如何解释字节数据，如下所示：

Enum    | Value | Meaning ----    | ----  | ----kUtf8   | 0     | The byte data may be interpreted as a UTF-8 string.kBinary | 1     | The byte data is arbitrary binary data and may not be printable. 枚举价值|含义---- | ---- | ---- kUtf8 | 0 |字节数据可以解释为UTF-8字符串。 1 |字节数据是任意二进制数据，并且可能无法打印。

 
## EXTENT {#extent}  EXTENT {extent} 

![Figure: Extent block](extentblock.png)  ！[图：扩展块]（extentblock.png）

`EXTENT` blocks contain an arbitrary byte data payload and the index of the next `EXTENT` in the chain. The byte data for a property is retrievedby reading each `EXTENT` in order until **Total Length** bytes are read. EXTENT块包含一个任意字节的数据有效负载和链中下一个EXTENT的索引。通过依次读取每个“ EXTENT”来检索属性的字节数据，直到读取“总长度”字节为止。

 
## NAME {#name}  NAME {name} 

![Figure: Name block](nameblock.png)  ！[图：名称块]（nameblock.png）

`NAME` blocks give objects and values a human-readable identifier. They consist of a UTF-8 payload that fits entirely within the given block. “ NAME”块为对象和值提供人类可读的标识符。它们由完全适合给定块的UTF-8有效负载组成。

 
## ARRAY\_VALUE {#array}  ARRAY \ _VALUE {array} 

![Figure: Array block](arrayblock.png)  ！[图：数组块]（arrayblock.png）

`ARRAY_VALUE` blocks contain an array of specifically 64-bit numeric values.  The **Stored Value Type** field is interpreted exactly likethe **Type** field, but may only indicate `INT_VALUE`, `UINT_VALUE`, or`DOUBLE_VALUE`. “ ARRAY_VALUE”块包含一个专门由64位数值组成的数组。 “存储值类型”字段的解释与“类型”字段的解释完全相同，但是只能表示“ INT_VALUE”，“ UINT_VALUE”或“ DOUBLE_VALUE”。

Exactly **Count** entries of the given **Stored Value Type** appear in the bytes at offset 16 into the block. 给定“存储值类型”的确切“计数”项出现在块中偏移量为16的字节中。

The **Display Format** field is used to affect how the array should be displayed, and it is interpreted as follows: “显示格式”字段用于影响数组的显示方式，其解释如下：

Enum                  | Value | Description ---------             | ----  | ----kFlat                 | 0     | Display as an ordered flat array with no additional formatting.kLinearHistogram      | 1     | Interpret the first two entries as `floor` and `step_size` parameters for a linear histogram, as defined below.kExponentialHistogram | 2     | Interpret the first three entries as `floor`, `initial_step`, and `step_multiplier` for an exponential histogram, as defined below. 枚举价值|说明--------- | ---- | ---- kFlat | 0 |显示为没有附加格式的有序平面数组。 1 |如下所示，将前两个条目解释为线性直方图的“ floor”和“ step_size”参数。 2 |将前三个条目解释为指数直方图的“ floor”，“ initial_step”和“ step_multiplier”，如下所示。

 
### Linear Histogram  线性直方图 

The array is a linear histogram that stores its parameters inline and contains both an overflow and underflow bucket. 该数组是线性直方图，它内联存储其参数，并包含一个上溢和下溢时段。

The first two elements are parameters `floor` and `step_size`, respectively (as defined below). 前两个元素分别是参数“ floor”和“ step_size”（定义如下）。

The number of buckets (N) is implicitly `Count - 4`.  桶数（N）隐式为“ Count-4”。

The remaining elements are buckets:  其余元素是存储桶：

```
2:     (-inf, floor),
3:     [floor, floor+step_size),
i+3:   [floor + step_size*i, floor + step_size*(i+1)),
...
N+3:   [floor+step_size*N, +inf)
```
 

 
### Exponential Histogram  指数直方图 

The array is an exponential histogram that stores its parameters inline and contains both an overflow and underflow bucket. 该数组是一个指数直方图，它内联存储其参数，并包含一个上溢和下溢时段。

The first three elements are parameters `floor`, `initial_step`, and `step_multiplier` respectively (as defined below). 前三个元素分别是参数“ floor”，“ initial_step”和“ step_multiplier”（定义如下）。

The number of buckets (N) is implicitly Count - 5.  桶数（N）隐式为Count-5。

The remaining are buckets:  剩下的是水桶：

```
3:     (-inf, floor),
4:     [floor, floor+initial_step),
i+4:   [floor + initial_step * step_multiplier^i, floor + initial_step * step_multiplier^(i+1))
N+4:   [floor + initial_step * step_multiplier^N, +inf)
```
 

 
## LINK\_VALUE {#link}  LINK \ _VALUE {link} 

![Figure: Link block](linkblock.png)  ！[图：链接块]（linkblock.png）

`LINK_VALUE` blocks allow nodes to support children that are present in a separate Inspect File. LINK_VALUE块允许节点支持存在于单独的检查文件中的子级。

The **Content Index** specifies another `NAME` block whose contents are a unique identifier referring to another Inspect File. Readers areexpected to obtain a bundle of `(Identifier, File)` pairs (through eithera directory read or another interface) and they may attempt to followlinks by splicing the trees together using the stored identifiers. “内容索引”指定了另一个“名称”块，其内容是引用另一个检查文件的唯一标识符。期望读者（通过目录读取或另一个接口）获得成对的（（标识符，文件））对，并且读者可能会尝试通过使用存储的标识符将树拼接在一起来跟随链接。

The **Disposition Flags** instruct readers on how to splice the trees, as follows:  “处置标志”指示读者如何拼接树，如下所示：

Enum               | Value | Description ----               | ----  | ----kChildDisposition  | 0     | The hierarchy stored in the linked file should be a child of the `LINK_VALUE`'s parent.kInlineDisposition | 1     | The children and properties of the root stored in the linked file should be added to the `LINK_VALUE`'s parent. 枚举价值|说明---- | ---- | ---- kChildDisposition | 0 |存储在链接文件中的层次结构应该是“ LINK_VALUE”的父级的子级。 1 |链接文件中存储的根的子级和属性应添加到“ LINK_VALUE”的父级中。

For example:  例如：

```
// root.inspect
root:
  int_value = 10
  child = LINK("other.inspect")

// other.inspect
root:
  test = "Hello World"
  next:
    value = 0


// kChildDisposition produces:
root:
  int_value = 10
  child:
    test = "Hello World"
    next:
      value = 0

// kInlineDisposition produces:
root:
  int_value = 10
  test = "Hello World"
  next:
    value = 0
```
 

Note: In all cases the name of the root node in the linked file is ignored.  注意：在所有情况下，链接文件中根节点的名称都将被忽略。

In the event of a collision in child names between a Node and values being added by its inline linked child, precedence is reader defined. Mostreaders, however, would find it useful to have linked values takeprecedence so they may override the original values. 如果节点之间的子名称发生冲突，并且节点的内联链接的子项添加的值发生冲突，则由读者定义优先级。但是，大多数读者会发现使链接值具有优先级很有用，以便它们可以覆盖原始值。

 
# Concurrency Control {#concurrency}  并发控制{concurrency} 

Writers must use a global version counter so that readers can detect in-flight modifications and modifications between reads withoutcommunicating with the writer. This supports single-writer multi-readerconcurrency. 编写者必须使用全局版本计数器，以便读者可以在进行中修改和读取之间的修改，而无需与编写者进行通信。这支持单作者多读者并发。

The strategy is for writers to increment a global *generation counter* both when they begin and when they end a write operation. 该策略是让编写者在开始和结束写操作时都增加一个全局*生成计数器*。

This is a simple strategy with a significant benefit: between incrementing the version number for beginning and ending a write the writer can performany number of operations on the buffer without regard for atomicity ofdata updates. 这是一种简单的策略，具有明显的好处：在增加版本号以开始和结束写入之间，编写器可以在缓冲区上执行任意数量的操作，而无需考虑数据更新的原子性。

The main drawback is that reads could be delayed indefinitely due to a frequently updating writer, but readers can have mitigations in placein practice. 主要缺点是，由于频繁更新书写者，因此读取可能会无限期延迟，但读者在实践中可能会有所缓解。

 
## Reader Algorithm  阅读器算法 

Readers use the following algorithm to obtain a consistent snapshot of an Inspect VMO: 读者使用以下算法来获取Inspect VMO的一致快照：

 
1. Spinlock until the version number is even (no concurrent write),  1.自旋锁定，直到版本号为偶数（无并发写入），
2. Copy the entire VMO buffer, and  2.复制整个VMO缓冲区，然后
3. Check that the version number from the buffer is equal to the version number from step 1. 3.检查缓冲区中的版本号是否与步骤1中的版本号相同。

As long as the version numbers match, the client may read their local copy to construct the shared state.If the version numbers do not match, the client may retry the wholeprocess. 只要版本号匹配，客户端就可以读取其本地副本以构造共享状态。如果版本号不匹配，则客户端可以重试整个过程。

 

 
## Writer Lock Algorithm  作家锁算法 

Writers lock an Inspect VMO for modification by doing the following:  编写者可以通过执行以下操作锁定Inspect VMO进行修改：

```c
atomically_increment(generation_counter, acquire_ordering);
```
 

This locks the file against concurrent reads by setting the generation to an odd number. Acquire ordering ensures that loads are not reordered beforethis change. 通过将生成设置为奇数，可以锁定文件以防止同时读取。获取排序可确保在此更改之前不对负载进行重新排序。

 
## Writer Unlock Algorithm  作家解锁算法 

Writers unlock an Inspect VMO following modification by doing the following: 编写者可以通过以下操作解锁Inspect VMO：

```c
atomically_increment(generation_counter, release_ordering);
```
 

Unlock the file allowing concurrent reads by setting the generation to a new even number. Release ordering ensures that writes to the file arevisible before the generation count update is visible. 通过将生成设置为新的偶数来解锁允许并发读取的文件。发行顺序确保在可见世代计数更新之前，对文件的写入是可见的。

<!-- xrefs --> [buddy]: https://en.wikipedia.org/wiki/Buddy_memory_allocation[VMO]: /docs/concepts/objects/vm_object.md[block.h]: /zircon/system/ulib/inspect/include/lib/inspect/cpp/vmo/block.h <！-外部参照-> [好友]：https://en.wikipedia.org/wiki/Buddy_memory_allocation[VMO]：/docs/concepts/objects/vm_object.md[block.h]：/ zircon / system / ulib / inspect / include / lib / inspect / cpp / vmo / block.h

