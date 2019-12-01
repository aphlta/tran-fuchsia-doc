 
# Wire Format Specification  线格式规格 

This document is a specification of the Fuchsia Interface Definition Language (**FIDL**) message format. 本文档是Fuchsia接口定义语言（** FIDL **）消息格式的规范。

For more information about FIDL's overall purpose, goals, and requirements, see [Overview](../../README.md). 有关FIDL总体目的，目标和要求的更多信息，请参见[概述]（../../ README.md）。

[TOC]  [目录]

 
## Concepts  概念 

This section provides requisite background information for the concepts used throughout the description. 本节提供了整个说明书中使用的概念的必要背景信息。

 
### Message  信息 

A FIDL **message** is a collection of data.  FIDL消息是数据的集合。

The message is a contiguous structure consisting of a single **in-line primary object** followed by zero or more**out-of-line secondary objects**. 该消息是一个连续的结构，由一个单独的“行内主要对象” **，然后是零个或多个**行外次要对象**组成。

Objects are stored in **traversal order**, and are subject to **padding**.  对象以“遍历顺序”存储，并且需要“填充”。

![drawing](objorder.png)  ！[绘图]（objorder.png）

 
### Primary and Secondary Objects  主要和次要对象 

The first object is called the **primary object**. It is a structure of fixed size whose type and size are known from thecontext. 第一个对象称为“主要对象”。它是一个固定大小的结构，其类型和大小可从上下文中得知。

The primary object may refer to **secondary objects** (such as in the case of strings, vectors, unions, and so on) if additional variable-sizedor optional data is required. 如果需要附加的可变大小或可选数据，则主要对象可以指代“次要对象”（例如在字符串，向量，并集等情况下）。

Secondary objects are stored **out-of-line** in traversal order.  次要对象按遍历顺序“离线”存储。

Both primary and secondary objects are 8-byte aligned, and are stored without gaps (other than those required for alignment). 主对象和辅助对象都是8字节对齐的，并且存储时没有间隙（对齐所需的对象除外）。

Together, a primary object and its secondary objects are called a **message**. 主对象及其辅助对象一起被称为“消息”。

 
#### Messages for transactions  交易讯息 

A transactional FIDL message (**transactional message**) is used to send data from one application to another. 事务FIDL消息（**事务消息**）用于将数据从一个应用程序发送到另一个应用程序。

Note: The roles of the applications (e.g. **client** vs **server**) are not relevant to the formatting of the data. 注意：应用程序的角色（例如** client **与** server **）与数据格式无关。

The [transactional messages](#transactional-messages) section, describes how a transactional message is composed of a header message optionally followedby a body message. [事务消息]（事务消息）部分描述了事务消息如何由标头消息以及可选的正文消息组成。

 
### Traversal Order  遍历顺序 

The **traversal order** of a message is determined by a recursive depth-first walk of all of the **objects** it contains, as obtained by following the chainof references. 消息的“遍历顺序”由它包含的所有“对象”的递归深度优先遍历确定，这是通过遵循引用链获得的。

Given the following structure:  给出以下结构：

```fidl
struct Cart {
    vector<Item> items;
};
struct Item {
    Product product;
    uint32 quantity;
};
struct Product {
    string sku;
    string name;
    string? description;
    uint32 price;
};
```
 

The depth-first traversal order for a `Cart` message is defined by the following pseudo-code: “购物车”消息的深度优先遍历顺序由以下伪代码定义：

```
visit Cart:
    for each Item in Cart.items vector data:
        visit Item.product:
            visit Product.sku
            visit Product.name
            visit Product.description
            visit Product.price
        visit Item.quantity
```
 

 
### Dual Forms: Encoded vs Decoded  双重形式：编码与解码 

The same message content can be expressed in one of two forms: **encoded** and **decoded**.These have the same size and overall layout, but differ in terms of theirrepresentation of pointers (memory addresses) or handles (capabilities). 相同的消息内容可以用以下两种形式之一表示：**编码**和**解码**它们具有相同的大小和总体布局，但是在指针（内存地址）或句柄（功能）的表示方面有所不同）。

FIDL is designed such that **encoding** and **decoding** of messages can occur in place in memory. FIDL的设计使得消息的“编码”和“解码”可以在内存中就地发生。

Message encoding is canonical &mdash; there is exactly one encoding for a given message. 消息编码是规范的-给定消息只有一种编码。

![drawing](dual-forms.png)  ！[drawing]（dual-forms.png）

 
#### Encoded Messages  编码信息 

An **encoded message** has been prepared for transfer to another process: it does not contain pointers (memory addresses) or handles (capabilities). 已准备好**编码消息**，以传送到另一个进程：它不包含指针（内存地址）或句柄（功能）。

During **encoding**...  在**编码**期间...

 
*   All pointers to sub-objects within the message are replaced with flags which indicate whether their referent is present or not-present, *消息中所有指向子对象的指针都被标记替换，这些标记指示其引用对象存在或不存在，
*   All handles within the message are extracted to an associated **handle vector** and replaced with flags which indicate whether their referent ispresent or not-present. *消息中的所有句柄都提取到关联的“句柄向量”中，并用指示其引用对象存在或不存在的标志替换。

The resulting **encoded message** and **handle vector** can then be sent to another process using [**zx_channel_write()**][channel write] or a similar IPCmechanism.There are additional constraints on this kind of IPC. See[transactional messages](#transactional-messages). 然后可以使用[** zx_channel_write（）**] [channel write]或类似的IPC机制将生成的**编码消息**和**处理向量**发送到另一个进程。这种IPC受到其他限制。请参见[交易消息]（交易消息）。

Note: The handle vector is *not* stored as part of the message, it's sent separately (also known as "**out-of-band**, not to be confused with**out-of-line**). For example, the[**zx_channel_write()**][channel write] function takes two sets of datapointers: one for the message, and one for the handle vector. The messagedata pointer will contain all of the **in-line** and **out-of-line** data,and the handle vector pointer will contain the handles. 注意：句柄向量不是作为消息的一部分存储的，它是单独发送的（也称为“带外”，不要与“线外”混淆）。例如，[** zx_channel_write（）**] [通道写入]函数采用两组数据指针：一组用于消息，另一组用于句柄向量。messagedata指针将包含所有**行* *和** out-of-line **数据，并且句柄矢量指针将包含句柄。

 
#### Decoded Messages  解码信息 

A **decoded message** has been prepared for use within a process's address space: it may contain pointers (memory addresses) or handles (capabilities). 已准备好“已解码的消息” **以在进程的地址空间内使用：它可能包含指针（内存地址）或句柄（功能）。

During **decoding**:  在**解码**期间：

 
*   All pointers to sub-objects within the message are reconstructed using the encoded present and not-present flags. *使用编码的存在和不存在标志重建消息中所有指向子对象的指针。
*   All handles within the message are restored from the associated **handle vector** using the encoded present and not-present flags. *使用编码的存在和不存在标志从关联的“句柄向量”中还原消息中的所有句柄。

The resulting **decoded message** is ready to be consumed directly from memory.  由此产生的“解码后的消息”可以直接从内存中使用。

 
### Inlined Objects  内联对象 

Objects may also contain **inlined objects** which are aggregated within the body of the containing object, such as embedded structs and fixed-size arrays ofstructs. 对象也可能包含“内联对象”，这些对象在包含对象的主体内聚合，例如嵌入式结构和固定大小的结构数组。

 
### Example  例 

In the following example, the `Region` structure contains a vector of `Rect` structures, with each `Rect` consisting of two `Point`s.Each `Point` consists of an `x` and `y` value. 在下面的示例中，Region结构包含一个Rect结构的向量，每个Rect由两个Point组成，每个Point由x和y值组成。

```fidl
struct Region {
    vector<Rect> rects;
};
struct Rect {
    Point top_left;
    Point bottom_right;
};
struct Point { uint32 x, y; };
```
 

Examining the objects in traversal order means that we start with the `Region` structure &mdash; it's the **primary object**. 以遍历的顺序检查对象意味着我们从“ Region”结构mdash开始；这是“主要对象”。

The `rects` member is a `vector`, so its contents are stored **out-of-line**. This means that the `vector` content immediately follows the `Region` object. “ rects”成员是“ vector”，因此其内容被“离线”存储。这意味着“向量”的内容紧随“区域”对象之后。

Each `Rect` struct contains two `Point`s, which are stored **in-line** (because there are a fixed number of them), and each of the `Point`s'primitive data types (`x` and `y`) are also stored **in-line**.The reason is the same; there is a fixed number of the member types. 每个“ Rect”结构都包含两个“ Point”，它们以“行内”方式存储（因为它们的数目是固定的），并且每个“ Point”的原始数据类型（“ x”和“ y）也被在线存储。原因是相同的；成员类型的数量是固定的。

![drawing](objects.png)  ！[绘图]（objects.png）

We use **in-line** storage when the size of the subordinate object is fixed, and **out-of-line** when it's variable (includingoptional). 当下级对象的大小固定时，我们使用“行内”存储，而当变量可变时（包括可选的），我们使用“行外”存储。

 
# Type Details  类型详细信息 

In this section, we illustrate the encodings for all FIDL objects.  在本节中，我们说明所有FIDL对象的编码。

 
## Primitives  原语 

 
*   Value stored in [little-endian format][ftp-030].  *以[little-endian格式] [ftp-030]存储的值。
*   Packed with natural alignment.  *包装自然对齐。
    *   Each _m_-byte primitive is stored on an _m_-byte boundary.  *每个_m_字节原语都存储在_m_字节边界上。
*   Not nullable.  *不可为空。

The following primitive types are supported:  支持以下原始类型：

Category                | Types ----------------------- | ----------------------------Boolean                 | `bool`Signed integer          | `int8`, `int16`, `int32`, `int64`Unsigned integer        | `uint8`, `uint16`, `uint32`, `uint64`IEEE 754 floating-point | `float32`, `float64`strings                 | (not a primitive, see [Strings](#strings)) 分类|类型----------------------- | ----------------------------布尔值| `bool`签名整数| `int8`，`int16`，`int32`，`int64`无符号整数| uint8，uint16，uint32，uint64 IEEE 754浮点数| `float32`，`float64`strings | （不是基本类型，请参见[Strings]（strings））

Number types are suffixed with their size in bits.  数字类型以大小为后缀。

The Boolean type, `bool`, is stored as a single byte, and has only the value **0** or **1**. 布尔类型布尔将其存储为单个字节，并且仅具有值** 0 **或** 1 **。

All floating point values represent valid IEEE 754 bit patterns.  所有浮点值均表示有效的IEEE 754位模式。

![drawing](primitive-int.png)  ！[绘图]（primitive-int.png）

![drawing](primitive-fp.png)  ！[绘图]（primitive-fp.png）

 
## Enums and Bits  枚举 

Bit fields and enumerations are stored as their underlying primitive type (e.g., `uint32`). 位字段和枚举存储为它们的基础基本类型（例如，“ uint32”）。

 
## Handles  提手 

A handle is a 32-bit integer, but with special treatment. When encoded for transfer, the handle's on-wire representation is replaced witha present and  not-present indication, and the handle itself is stored in aseparate handle vector. When decoded, the handle presence indication isreplaced with zero (if not present) or a valid handle (if present). 句柄是32位整数，但经过特殊处理。编码以进行传输时，句柄的在线表示将替换为存在和不存在的指示，并且句柄本身存储在单独的句柄向量中。解码后，句柄存在指示将替换为零（如果不存在）或有效句柄（如果存在）。

The handle *value* itself is **not** transferred from one application to another. 句柄*值*本身不会从一个应用程序转移到另一个应用程序。

In this respect, handles are like pointers; they reference a context that's unique to each application.Handles are moved from one application's context to the other's. 在这方面，句柄就像指针。它们引用了每个应用程序唯一的上下文。句柄从一个应用程序的上下文移动到另一个应用程序的上下文。

![drawing](handlexlate.png)  ！[绘图]（handlexlate.png）

The value zero can be used to indicate a nullable handle is null[[1]](#Footnote-1).  零值可用于指示可为空的句柄为null [[1]]（Footnote-1）。

 
## Aggregate objects  汇总对象 

Aggregate objects serve as containers of other objects. They may store that data in-line or out-of-line, depending on their type. 聚合对象充当其他对象的容器。他们可以根据其类型在线或离线存储该数据。

 
### Arrays  数组 

 
*   Fixed length sequence of homogeneous elements.  *均质元素的固定长度序列。
*   Packed with natural alignment of their elements.  *带有自然对齐的元素。
    *   Alignment of array is the same as the alignment of its elements.  *数组的对齐方式与其元素的对齐方式相同。
    *   Each subsequent element is aligned on element's alignment boundary.  *每个后续元素在元素的对齐边界上对齐。
*   The stride of the array is exactly equal to the size of the element (which includes the padding required to satisfy element alignment constraints). *数组的步幅完全等于元素的大小（包括满足元素对齐约束所需的填充）。
*   Not nullable.  *不可为空。
*   There is no special case for arrays of bools. Each bool element takes one byte as usual. *布尔数组没有特殊情况。每个布尔元素照常占用一个字节。

Arrays are denoted:  数组表示为：

 
*   `array<T>:N`: where **T** can be any FIDL type (including an array) and **N** is the number of elements in the array. *`array <T>：N`：其中** T **可以是任何FIDL类型（包括数组），而** N **是数组中元素的数量。

![drawing](arrays.png)  ！[绘图]（arrays.png）

 
### Vectors  向量 

 
*   Variable-length sequence of homogeneous elements.  *同构元素的可变长度序列。
*   Nullable; null vectors and empty vectors are distinct.  *可为空；空向量和空向量是不同的。
*   Can specify a maximum size, e.g. `vector<T>:40` for a maximum 40 element vector. *可以指定最大尺寸，例如vector <T>：40`，最多可包含40个元素向量。
*   Stored as a 16 byte record consisting of:  *存储为16字节记录，包括：
    *   `size`: 64-bit unsigned number of elements  *`size`：64位无符号元素数
    *   `data`: 64-bit presence indication or pointer to out-of-line element data  *`data`：64位存在指示或指向离线元素数据的指针
*   When encoded for transfer, `data` indicates presence of content: *编码用于传输时，`data`表示存在内容：
    *   `0`: vector is null  *`0`：向量为空
    *   `UINTPTR_MAX`: vector is non-null, data is the next out-of-line object  *`UINTPTR_MAX`：向量为非空，数据为下一个离线对象
*   When decoded for consumption, `data` is a pointer to content: *当解码以供使用时，“数据”是指向内容的指针：
    *   `0`: vector is null  *`0`：向量为空
    *   `<valid pointer>`: vector is non-null, data is at indicated memory address  *`<有效指针>`：向量为非空，数据位于指定的存储器地址
*   There is no special case for vectors of bools. Each bool element takes one byte as usual. *布尔向量没有特殊情况。每个布尔元素照常占用一个字节。

Vectors are denoted as follows:  向量表示如下：

 
*   `vector<T>`: non-nullable vector of element type **T** (validation error occurs if null `data` is encountered) *`vector <T>`：元素类型为** T **的非空向量（如果遇到null`data`则发生验证错误）
*   `vector<T>?`: nullable vector of element type **T**  *`vector <T>？`：元素类型为** T **的可空向量
*   `vector<T>:N`, `vector<T>:N?`: vector with maximum length of **N** elements  *`vector <T>：N`，`vector <T>：N？`：最大长度为** N **个元素的向量

**T** can be any FIDL type.  ** T **可以是任何FIDL类型。

![drawing](vectors.png)  ！[绘图]（vectors.png）

 
### Strings  弦乐 

Strings are implemented as a vector of `uint8` bytes, with the constraint that the bytes MUST be valid UTF-8. 字符串被实现为uint8字节的向量，其约束条件是字节必须是有效的UTF-8。

 
### Structures  结构体 

A structure contains a sequence of typed fields.  结构包含一系列类型字段。

Internally, the structure is padded so that all members are aligned to the largest alignment requirement of all members.Externally, the structure is aligned on an 8-byte boundary, and may therefore containfinal padding to meet that requirement. 在内部，该结构被填充，以便所有成员都对齐到所有成员中最大的对齐要求。在外部，该结构在8字节边界上对齐，因此可能包含最终填充以满足该要求。

Here are some examples.  这里有些例子。

A struct with an **int32** and an **int8** field has an alignment of 4 bytes (due to the **int32**), and a size of 8 bytes (3 bytes of padding after the **int8**): 具有** int32 **和** int8 **字段的结构的对齐方式为4个字节（由于** int32 **），并且大小为8字节（在** int8之后填充3个字节） **）：

![drawing](struct1.png)  ！[绘图]（struct1.png）

A struct with a **bool** and a **string** field has an alignment of 8 bytes (due to the **string**) and a size of 24 bytes (7 bytes of padding after the**bool**): 具有** bool **和** string **字段的结构的对齐方式为8个字节（由于** string **）和24个字节的大小（在布尔值之后填充7个字节） *）：

![drawing](struct2.png)  ！[绘图]（struct2.png）

Note: Keep in mind that a **string** is really just a special case of `vector<uint8>`. 注意：请记住，字符串**实际上只是vector <uint8>的特例。

A struct with a **bool** and two **uint8** fields has an alignment of 1 byte and a size of 3 bytes (no padding!): 具有** bool **和两个** uint8 **字段的结构的对齐方式为1个字节，大小为3个字节（无填充！）：

![drawing](struct3.png)  ！[绘图]（struct3.png）

A structure can be:  结构可以是：

 
* empty &mdash; it has no fields. Such a structure is 1 byte in size, with an alignment of 1 byte, and is exactly equivalent to a structure containing a`uint8` with the value zero. *空mdash;它没有字段。这种结构的大小为1个字节，对齐方式为1个字节，并且完全等效于包含值为零的'uint8'的结构。
* non-nullable &mdash; the structure's contents are stored in-line.  *不可为空的短划线；结构的内容被内联存储。
* nullable &mdash; the structure's contents are stored out-of-line and accessed through an indirect reference. *可为空的短划线；该结构的内容脱机存储并通过间接引用进行访问。

Storage of a structure depends on whether it is nullable at point of reference.  结构的存储取决于在参考点是否为空。

 
* Non-nullable structures:  *非空结构：
  * Contents are stored in-line within their containing type, enabling very efficient aggregate structures to be constructed. *内容以其包含类型内联存储，从而可以构建非常有效的聚合结构。
  * The structure layout does not change when inlined; its fields are not repacked to fill gaps in its container. *内联时，结构布局不会更改；它的字段不会重新打包以填补其容器中的空白。
* Nullable structures:  *可空结构：
  * Contents are stored out-of-line and accessed through an indirect reference. *内容脱机存储并通过间接引用进行访问。
  * When encoded for transfer, stored reference indicates presence of structure: *当编码用于传输时，存储的引用指示结构的存在：
    * `0`: reference is null  *`0'：引用为空
    * `UINTPTR_MAX`: reference is non-null, structure content is the next out-of-line object *`UINTPTR_MAX`：引用非空，结构内容是下一个离线对象
  * When decoded for consumption, stored reference is a pointer:  *当解码以供使用时，存储的引用是一个指针：
    * `0`: reference is null  *`0'：引用为空
    * `<valid pointer>`: reference is non-null, structure content is at indicated memory address *`<有效指针>`：引用非空，结构内容位于指定的内存地址

Structs are denoted by their declared name (e.g. `Circle`) and nullability:  结构以其声明的名称（例如“ Circle”）和可为空性表示：

 
*   `Point`: non-nullable `Point`  *`Point`：不可为空的`Point`
*   `Color?`: nullable `Color`  *`Color？`：可为空的`Color`

The following example illustrates:  以下示例说明：

 
  * Structure layout (order, packing, and alignment)  *结构布局（订单，包装和对齐）
  * A non-nullable structure (`Point`)  *不可为空的结构（“点”）
  * A nullable structure (`Color`)  *可为空的结构（`Color`）

```fidl
struct Circle {
    bool filled;
    Point center;    // Point will be stored in-line
    float32 radius;
    Color? color;    // Color will be stored out-of-line
    bool dashed;
};
struct Point { float32 x, y; };
struct Color { float32 r, g, b; };
```
 

The `Color` content is padded to the 8 byte secondary object alignment boundary. Going through the layout in detail: “颜色”内容填充到8字节辅助对象对齐边界。详细浏览布局：

![drawing](structs.png)  ！[绘图]（structs.png）

 
1. The first member, `bool filled`, occupies one byte, but requires three bytes of padding because of the next member, which has a 4-byte alignmentrequirement. 1.第一个成员为“布尔填充”，占用一个字节，但是由于下一个成员（需要4字节对齐），因此需要填充三个字节。
2. The `Point center` member is an example of a non-nullable struct. As such, its content (the `x` and `y` 32-bit floats) are inlined, and the entire thingconsumes 8 bytes. 2.“ Point center”成员是不可为空的结构的一个示例。这样，它的内容（“ x”和“ y” 32位浮点数）是内联的，整个东西占用8个字节。
3. `radius` is a 32-bit item, requiring 4 byte alignment. Since the next available location is already on a 4 byte alignment boundary, no paddingis required. 3.`radius'是一个32位项目，需要4字节对齐。由于下一个可用位置已经在4字节对齐边界上，因此不需要填充。
4. The `Color? color` member is an example of a nullable structure. Since the `color` data may or may not be present, the most efficient way of handlingthis is to keep a pointer to the structure as the in-line data. That way,if the `color` member is indeed present, the pointer points to its data(or, in the case of the encoded format, indicates "is present"), and thedata itself is stored out-of-line (after the data for the `Circle`structure). If the `color` member is not present, the pointer is `NULL`(or, in the encoded format, indicates "is not present" by storing a zero). 4.`颜色？ color成员是可为空结构的示例。由于可能存在或不存在“颜色”数据，因此最有效的处理方法是保持指向结构的指针作为内联数据。这样，如果确实存在“ color”成员，则指针指向其数据（或在编码格式的情况下，指示“存在”），并且数据本身脱机存储（在圆形结构的数据）。如果不存在“ color”成员，则指针为“ NULL”（或以编码格式通过存储零来指示“不存在”）。
5. The `bool dashed` doesn't require any special alignment, so it goes next. Now, however, we've reached the end of the object, and all objects must be8-byte aligned. That means we need an additional 7 bytes of padding. 5.“布尔虚线”不需要任何特殊对齐，因此继续进行。但是，现在我们到达了对象的末尾，所有对象都必须对齐8字节。这意味着我们需要额外的7个字节的填充。
6. The out-of-line data for `color` follows the `Circle` data structure, and contains three 32-bit `float` values (`r`, `g`, and `b`); they require 4byte alignment and so can follow each other without padding. But, just asin the case of the `Circle` object, we require the object itself to be8-byte aligned, so 4 bytes of padding are required. 6. color的离线数据遵循Circle数据结构，并包含三个32位float值（r，g和b）；它们需要4字节对齐，因此可以互相跟随而无需填充。但是，就像“圆形”对象的情况一样，我们要求对象本身是8字节对齐的，因此需要4字节的填充。

Overall, this structure takes 48 bytes.  总体而言，此结构占用48个字节。

By moving the `bool dashed` to be immediately after the `bool filled`, though, you can realize significant space savings [[2]](#Footnote-2): 但是，通过将“布尔虚线”移动到“布尔填充”之后，可以节省大量空间[[2]]（Footnote-2）：

![drawing](struct-reorg.png)  ！[绘图]（struct-reorg.png）

 
1. The two `bool` values are "packed" together within what would have been wasted space. 1.两个“ bool”值在可能浪费的空间内“打包”在一起。
2. The padding is reduced to two bytes &mdash; this would be a good place to add a 16-bit value, or some more `bool`s or 8-bit integers. 2.填充减少为两个字节-这是添加16位值或更多“布尔”或8位整数的好地方。
3. Notice how there's no padding required after the `color` pointer; everything is perfectly aligned on an 8 byte boundary. 3.注意在`color`指针之后不需要填充；一切都在8字节边界上完美对齐。

The structure now takes 40 bytes.  该结构现在占用40个字节。

Note: While `fidlc` could automatically pack structs, like Rust, we chose not to do that in order to simplify [ABI compatibility changes](../abi-compat.md). 注意：尽管`fidlc`可以自动打包结构，例如Rust，但我们选择不这样做是为了简化[ABI兼容性更改]（../ abi-compat.md）。

 
### Unions  工会 

 
*   Tagged option type consisting of tag field and variadic contents.  *带标签的选项类型，由标签字段和可变参数内容组成。
*   Tag field is represented with a **uint32 enum**.  *标签字段用** uint32枚举**表示。
*   Size of union is the size of the tag field plus the size of the largest union variant including padding necessary to satisfy its alignment requirements. *并集大小是标签字段的大小加上最大并集变体的大小，包括满足其对齐要求所需的填充。
*   Alignment factor of union is defined by the maximal alignment factor of the tag field and any of its options. *并列的对齐系数由标签字段及其任何选项的最大对齐系数定义。
*   Union is padded so that its size is a multiple of its alignment factor. For example: *填充联合，以便其大小为其对齐因子的倍数。例如：
    1. A union with an **int32** and an **int8** option has an alignment of 4 bytes (due to the **int32**), and a size of 8 bytes including the 4 bytetag (0 or 3 bytes of padding, depending on the option / variant). 1.具有** int32 **和** int8 **选项的并集具有4个字节的对齐方式（由于** int32 **），并且其大小为8个字节，包括4个字节标记（0或3）填充字节，具体取决于选项/变体）。
    2. A union with a **bool** and a **string** option has an alignment of 8 bytes (due to the **string**), and a size of 24 bytes (4 or 19 bytes ofpadding, depending on the option or variant). 2.具有** bool **和** string **选项的并集具有8字节的对齐方式（由于** string **），并且其大小为24字节（4或19字节的填充），具体取决于在选项或变体上）。
*   In general, changing the definition of a union will break binary compatibility. Instead it is preferred that you extend interfaces byadding new methods which use new unions. *通常，更改并集的定义将破坏二进制兼容性。相反，最好通过添加使用新联合的新方法来扩展接口。

Storage of a union depends on whether it is nullable at point of reference.  并集的存储取决于它在参考点是否为空。

 
*   Non-nullable unions:  *非空联盟：
    *   Contents are stored in-line within their containing type, enabling very efficient aggregate structures to be constructed. *内容以其包含类型内联存储，从而可以构建非常有效的聚合结构。
    *   The union layout does not change when inlined; its options are not repacked to fill gaps in its container. *内联时，联合布局不会更改；它的选件不会重新包装以填补其容器中的空白。
*   Nullable unions:  *空联盟：
    *   Contents are stored out-of-line and accessed through an indirect reference. *内容脱机存储并通过间接引用进行访问。
    *   When encoded for transfer, stored reference indicates presence of union:  *当编码用于传输时，存储的参考表示存在联合：
        *   `0`: reference is `null`  *`0`：引用为`null`
        *   `UINTPTR_MAX`: reference is non-null, union content is the next out-of-line object  *`UINTPTR_MAX`：引用非空，联合内容是下一个离线对象
    *   When decoded for consumption, stored reference is a pointer:  *当解码以供使用时，存储的引用是一个指针：
        *   `0`: reference is `null`  *`0`：引用为`null`
        *   `<valid pointer>`: reference is non-null, union content is at indicated memory address  *`<有效指针>`：引用非空，联合内容位于指示的内存地址

Unions are denoted by their declared name (e.g. `Pattern`) and nullability:  联合用其声明的名称（例如“ Pattern”）和可为空性表示：

 
*   `Pattern`: non-nullable `Pattern`  *`Pattern`：不可为空的`Pattern`
*   `Pattern?`: nullable `Pattern`  *`Pattern？`：可为空的`Pattern`

The following example shows how unions are laid out according to their options.  下面的示例显示如何根据其选项对联合进行布局。

```fidl
struct Paint {
    Pattern fg;
    Pattern? bg;
};
union Pattern {
    Color color;
    Texture texture;
};
struct Color { float32 r, g, b; };
struct Texture { string name; };
```
 

When laying out `Pattern`, space is first allotted to the tag (4 bytes), then to the selected option. 布局“模式”时，首先将空间分配给标签（4个字节），然后分配给所选的选项。

![drawing](unions.png)  ！[绘图]（unions.png）

 
### Envelopes  信封 

An envelope is a container for out-of-line data, used internally by tables and extensible unions. It is not exposed to the FIDL language. 信封是用于存放离线数据的容器，表和可扩展联合在内部使用。它没有公开使用FIDL语言。

It has a fixed, 16 byte format, and is not nullable:  它具有固定的16字节格式，并且不能为空：

![drawing](envelope.png)  ！[绘图]（envelope.png）

An envelope can, however, point to empty content. In that case, `num_bytes`, `num_handles`, and the pointer will all be zero. 但是，信封可以指向空白内容。在这种情况下，“ num_bytes”，“ num_handles”和指针将全部为零。

Furthermore, because `num_bytes` represents the size of an object, it's always a multiple of 8, regardless of the actual amount of data that it points to. 此外，因为“ num_bytes”表示对象的大小，所以它始终是8的倍数，无论其指向的实际数据量是多少。

Having `num_bytes` and `num_handles` allows us to skip unknown envelope content.  具有“ num_bytes”和“ num_handles”可以使我们跳过未知的信封内容。

 
### Tables  桌子 

 
*   Record type consisting of the number of elements and a pointer.  *记录类型由元素数和指针组成。
*   Pointer points to an array of envelopes, each of which contains one element.  *指针指向一组信封，每个信封包含一个元素。
*   Each element is associated with an ordinal.  *每个元素都与一个序数关联。
*   Ordinals are sequential, gaps incur an empty envelope cost and hence are discouraged.  *普通序列是连续的，缺口会导致空信封成本，因此不鼓励使用。

Tables are denoted by their declared name (e.g., **Value**), and are not nullable:  表格以其声明的名称（例如** Value **）表示，并且不能为空：

 
*   `Value`: non-nullable `Value`  *`Value`：不可为空的`Value`

The following example shows how tables are laid out according to their fields.  下面的示例显示如何根据表的字段对表进行布局。

```fidl
table Value {
    1: int16 command;
    2: Circle data;
    3: float64 offset;
};
```
 

![drawing](tables.png)  ！[drawing]（tables.png）

 
### Extensible Unions (xunions)  可扩展的联合（工会） 

 
*   Record type consisting of an ordinal and an envelope.  *记录类型，由序数和信封组成。
*   Ordinal indicates member selection, and is represented with a **uint32**.  *序号表示成员选择，并以** uint32 **表示。
*   Ordinals are calculated by hashing the concatenated library name, xunion name, and member name, and retaining 31 bits.See [ordinal hashing] for further details. *普通数是通过对连接的库名，xunion名称和成员名进行哈希处理并保留31位来计算的。有关更多详细信息，请参见[普通哈希]。
*   Nullable xunions are represented with a `0` ordinal, and an empty envelope.  *可空的xunion以序号“ 0”和一个空信封表示。
*   Empty xunions are not allowed.  *不允许使用空的联轴器。

xunions are denoted by their declared name (e.g. `Value`) and nullability:  联轴器以其声明的名称（例如“值”）和可空性表示：

 
*   `Value`: non-nullable `Value`  *`Value`：不可为空的`Value`
*   `Value?`: nullable `Value`  *`Value？`：可为空的`Value`

The following example shows how xunions are laid out according to their fields.  以下示例显示了如何根据它们的字段布置联轴器。

```fidl
xunion Value {
    int16 command;
    Circle data;
    float64 offset;
};
```
 

![drawing](xunion.png)  ！[绘图]（xunion.png）

 
### Transactional Messages  交易讯息 

In a transactional message, there is always a **header**, followed by an optional **body**. 在事务性消息中，总会有**标头**，后跟可选的**正文**。

Both the header and body are FIDL messages, as defined above; that is, a collection of data. 头和正文都是FIDL消息，如上所述。即数据的集合。

The header has the following form:  标头具有以下形式：

![drawing](transaction-header.png)  ！[绘图]（transaction-header.png）

 
*   `zx_txid_t txid`, transaction ID (32 bits)  *`zx_txid_t txid`，交易ID（32位）
    * `txid`s with the high bit set are reserved for use by [**zx_channel_write()**][channel write] *设置了高位的`txid`保留供[** zx_channel_write（）**] [通道写入]使用
    * `txid`s with the high bit unset are reserved for use by userspace  *未设置高位的`txid`保留供用户空间使用
    * A value of `0` for `txid` is reserved for messages which do not require a response from the other side.Note: For more details on `txid` allocation, see[**zx_channel_call()**][channel call]. * txid的值为0保留给不需要对方响应的消息。注意：有关txid分配的更多详细信息，请参见[** zx_channel_call（）**] [频道调用]。
*   `uint8[3] flags`, MUST NOT be checked by bindings. These flags can be used to enable soft transitions of the wire format. See [Header Flags](#flags)for a description of the current flag definitions. *`uint8 [3]标志`，一定不能被绑定检查。这些标志可用于启用连线格式的软过渡。有关当前标志定义的说明，请参见[标题标志]（标志）。
*   `uint8 magic number`, determines if two wire formats are compatible.  * uint8幻数，确定两种线格式是否兼容。
*   `uint64 ordinal`  *`uint64 ordinal`
    *   The zero ordinal is invalid.  *零序号无效。
    *   Ordinals with the most significant bit set are reserved for control messages and future expansion. *具有最高有效位设置的普通字符保留用于控制消息和将来的扩展。
    *   Ordinals without the most significant bit set indicate method calls and responses. *没有设置最高有效位的普通字符表示方法调用和响应。

There are three kinds of transactional messages:  共有三种交易消息：

 
* method requests,  *方法要求，
* method responses, and  *方法回应，以及
* event requests.  *活动要求。

We'll use the following interface for the next few examples:  接下来的几个示例将使用以下界面：

```fidl
protocol Calculator {
    Add(int32 a, int32 b) -> (int32 sum);
    Divide(int32 dividend, int32 divisor) -> (int32 quotient, int32 remainder);
    Clear();
    -> OnError(uint32 status_code);
};
```
 

The **Add()** and **Divide()** methods illustrate both the method request (sent from the client to the server), and a method reponse(sent from the server back to the client). ** Add（）**和** Divide（）**方法既说明了方法请求（从客户端发送到服务器），又说明了方法响应（从服务器发送回客户端）。

The **Clear()** method is an example of a method request that does not have a body. ** Clear（）**方法是没有主体的方法请求的示例。

> It's not correct to say it has an "empty" body: that would imply that > there's a **body** following the **header**. In the case of **Clear()**,> there is no **body**, there is only a **header**. >说它有一个“空”主体是不正确的：这意味着> **头之后是一个**主体**。对于** Clear（）**，>没有** body **，只有** header **。

 
#### Method Request Messages  方法请求消息 

The client of an interface sends method request messages to the server in order to invoke the method. 接口的客户端向服务器发送方法请求消息，以调用该方法。

 
#### Method Response Messages  方法响应消息 

The server sends method reponse messages to the client to indicate completion of a method invocation and to provide a (possibly empty) result. 服务器将方法响应消息发送给客户端，以指示方法调用已完成，并提供（可能为空）结果。

Only two-way method requests which are defined to provide a (possibly empty) result in the protocol declaration will elicit a method response.One-way method requests must not produce a method response. 只有定义为在协议声明中提供结果（可能为空）的双向方法请求才会引发方法响应。单向方法请求不得产生方法响应。

A method response message provides the result associated with a prior method request. The body of the message contains the method results as if they were packed in a**struct**. 方法响应消息提供与先前方法请求关联的结果。消息的正文包含方法结果，就好像它们包装在** struct **中一样。

Here we see that the answer to 912 / 43 is 21 with a remainder of 9. Note the `txid` value of `1` &mdash; this identifies the transaction.The `ordinal` value of `2` indicates the method &mdash; in this case, the**Divide()** method. 在这里，我们看到912/43的答案是21，余数为9。请注意，“ txid”值为“ 1”。这是交易的识别码。原始值2表示方法mdash。在这种情况下，可以使用** Divide（）**方法。

![drawing](transaction-division.png)  ！[绘图]（transaction-division.png）

Below, we see that `123 + 456` is `579`. Here, the `txid` value is now `2` &mdash; this is simply the next transactionnumber assigned to the transaction.The `ordinal` is `1`, indicating **Add()**, and note that the result requires4 bytes of padding in order to make the **body** object have a size that'sa multiple of 8 bytes. 在下面，我们看到123 + 456是579。在这里，“ txid”的值现在是“ 2”。这只是分配给该事务的下一个事务编号。`ordinal`为`1`，表示** Add（）**，并注意结果需要4个字节的填充，以使** body **对象具有大小是8个字节的倍数。

![drawing](transaction-addition.png)  ！[绘图]（transaction-addition.png）

And finally, the **Clear()** method is different than the **Add()** and **Divide()** in two important ways: 最后，** Clear（）**方法在两个重要方面不同于** Add（）**和** Divide（）**：
* it does not have a **body** (that is, it consists solely of the **header**), and  *它没有**主体**（也就是说，它仅由**标题**组成），并且
* it does not solicit a response from the interface (`txid` is zero).  *它不从接口请求响应（`txid`为零）。

![drawing](method-clear.png)  ！[绘图]（method-clear.png）

 
#### Event Requests  活动要求 

An example of an event is the **OnError()** event in our `Calculator`.  事件的一个例子是我们的计算器中的** OnError（）**事件。

The server sends an unsolicited event request to the client to indicate that an asynchronous event occurred, as specified bythe protocol declaration. 服务器将未经请求的事件请求发送到客户端，以指示发生了异步事件，如协议声明所指定。

In the `Calculator` example, we can imagine that an attempt to divide by zero would cause the **OnError()** event to be sent with a "divide by zero" status codeprior to the connection being closed. This allows the client to distinguishbetween the connection being closed due to an error, as opposed to for otherreasons (such as the calculator process terminating abnormally). 在“计算器”示例中，我们可以想象除以零的尝试将导致在关闭连接之前以“除以零”状态代码发送** OnError（）**事件。与其他原因（例如计算器过程异常终止）相反，这允许客户端区分由于错误而关闭的连接。

![drawing](events.png)  ！[绘图]（events.png）

Notice how the `txid` is zero (indicating this is not part of a transaction), and `ordinal` is `4` (indicating the **OnError()** method). 注意txid是零（表示这不是事务的一部分），ordinal是4（表示OnError（）方法）。

The **body** contains the event arguments as if they were packed in a **struct**, just as with method result messages.Note that the body is padded to maintain 8-byte alignment. ** body **包含事件参数，就像它们被包装在** struct **中一样，就像方法结果消息一样。请注意，body被填充以保持8字节对齐。

 
#### Epitaph (Control Message Ordinal 0xFFFFFFFF)  墓志铭（控制消息顺序0xFFFFFFFF） 

An epitaph is a message with ordinal **0xFFFFFFFF**. A server may send an epitaph as the last message prior to closing the connection, to provide anindication of why the connection is being closed. No further messages may besent through the channel after the epitaph. Epitaphs are not sent from clientsto servers. 墓志铭是带有序号** 0xFFFFFFFF **的消息。服务器可以在关闭连接之前将墓志作为最后一条消息发送，以提供连接为什么被关闭的指示。墓志铭之后，可能不会再通过该通道发送任何消息。墓志铭不是从客户端发送到服务器的。

The epitaph contains an error status. The error status of the epitaph is stored in the reserved `uint32` of the message header. The reserved word is treated asbeing of type **zx_status_t**: negative numbers are reserved for system errorcodes, positive numbers are reserved for application error codes, and `ZX_OK` isused to indicate normal connection closure. The message is otherwise empty. 墓志铭包含一个错误状态。墓志铭的错误状态存储在消息头的保留“ uint32”中。保留字被视为类型** zx_status_t **：负数保留给系统错误代码，正数保留给应用程序错误代码，而`ZX_OK`用于指示正​​常的连接关闭。该消息否则为空。

 
## Details  细节 

 
#### Size and Alignment  尺寸和对齐 

`sizeof(T)` denotes the size in bytes for an object of type **T**.  sizeof（T）表示类型为** T **的对象的大小（以字节为单位）。

`alignof(T)` denotes the alignment factor in bytes to store an object of type **T**.  “ alignof（T）”表示以字节为单位的对齐因子，用于存储** T **类型的对象。

FIDL primitive types are stored at offsets in the message which are a multiple of their size in bytes. Thus for primitives **T**, `alignof(T) ==sizeof(T)`. This is called *natural alignment*. It has thenice property of satisfying typical alignment requirements of modern CPUarchitectures. FIDL原语类型存储在消息中的偏移处，该偏移量是其大小（以字节为单位）的倍数。因此，对于图元** T **，`alignof（T）== sizeof（T）`。这称为“自然对齐”。它具有满足现代CPU架构典型对齐要求的特性。

FIDL complex types, such as structs and arrays, are stored at offsets in the message which are a multiple of the maximum alignment factor of all of theirfields. Thus for complex types **T**, `alignof(T) ==max(alignof(F:T))` over all fields **F** in **T**. It has the niceproperty of satisfying typical C structure packing requirements (which can beenforced using packing attributes in the generated code). The size of a complextype is the total number of bytes needed to store its members properly alignedplus padding up to the type's alignment factor. FIDL复杂类型（例如结构和数组）存储在消息中的偏移量处，该偏移量是它们所有字段的最大对齐因子的倍数。因此，对于复杂类型** T **，在** T **中所有字段** F **上都需要alignof（T）== max（alignof（F：T））。它具有满足典型C结构打包要求（可以使用生成的代码中的打包属性强制执行）的良好特性。复杂类型的大小是正确存储其成员所需的总字节数，再加上填充类型的对齐因子。

FIDL primary and secondary objects are aligned at 8-byte offsets within the message, regardless of their contents. The primary object of a FIDL messagestarts at offset 0. Secondary objects, which are the only possible referent ofpointers within the message, always start at offsets which are a multiple of 8.(So all pointers within the message point at offsets which are a multiple of 8.) FIDL主对象和辅助对象在消息中以8字节的偏移量对齐，无论其内容如何。 FIDL消息的主要对象从偏移量0开始。辅助对象（它们是消息中指针的唯一可能的引用对象）始终从偏移量开始，偏移量为8的倍数。之8。

FIDL in-line objects (complex types embedded within primary or secondary objects) are aligned according to their type. They are not forced to 8 bytealignment. FIDL内联对象（嵌入在主对象或辅助对象中的复杂类型）根据其类型进行对齐。它们不被强制为8字节对齐。

 
##### Types  种类 

Notes:  笔记：

 
* **N** indicates the number of elements, whether stated explicity (as in `array<T>:N`, an array with **N** elements of type **T**) or implictly(a `table` consisting of 7 elements would have `N=7`). * ** N **表示元素的数量，无论是显式声明的（如`array <T>：N`，是具有** T **类型的** N **元素的数组）还是隐式声明的（表由7个元素组成的“ N = 7”）。
* The out-of-line size is always padded to 8 bytes. We indicate the content size below, excluding the padding. *离线大小始终填充为8个字节。我们在下面指示内容大小，不包括填充。
* `sizeof(T)` in the `vector` entry below is\ `in_line_sizeof(T) + out_of_line_sizeof(T)`. *下面“ vector”条目中的“ sizeof（T）”为“ in_line_sizeof（T）+ out_of_line_sizeof（T）”。
* **M** in the `table` entry below is the maximum ordinal of present field.  *下方“表格”条目中的** M **是当前字段的最大序数。
* In the `struct` entry below, the padding refers to the required padding to make the `struct` aligned to the widest element. For example,`struct{uint32;uint8}` has 3 bytes of padding, which is different than thepadding to align to 8 bytes boundaries. *在下面的“结构”条目中，填充是指使“结构”与最宽的元素对齐所需的填充。例如，“ struct {uint32; uint8}”具有3个字节的填充，这与填充以对齐8个字节的边界不同。

Type(s)                      | Size (in-line)                    | Size (out-of-line)                                              | Alignment -----------------------------|-----------------------------------|-----------------------------------------------------------------|--------------------------------`bool`                       | 1                                 | 0                                                               | 1`int8`, `uint8`              | 1                                 | 0                                                               | 1`int16`, `uint16`            | 2                                 | 0                                                               | 2`int32`, `uint32`, `float32` | 4                                 | 0                                                               | 4`int64`, `uint64`, `float64` | 8                                 | 0                                                               | 8`enum`, `bits`               | (underlying type)                 | 0                                                               | (underlying type)`handle`, et al.             | 4                                 | 0                                                               | 4`array<T>:N`                 | sizeof(T) * N                     | 0                                                               | alignof(T)`vector`, et al.             | 16                                | N * sizeof(T)                                                   | 8`struct`                     | sum(sizeof(fields)) + padding     | 0                                                               | 8`struct?`                    | 8                                 | sum(sizeof(fields)) + padding                                   | 8`union`                      | 4 + max(sizeof(fields)) + padding |  0                                                              | max(all fields)`union?`                     | 8                                 | 4 + max(sizeof(fields)) + padding                               | 8`envelope`                   | 16                                | sizeof(field)                                                   | 8`table`                      | 16                                | M * sizeof(envelope) + sum(aligned_to_8(sizeof(present fields)) | 8`xunion`, `xunion?`          | 24                                | sizeof(selected variant)                                        | 8 类型|尺寸（直列）|大小（离线）|对齐----------------------------- | ------------------- ---------------- | ------------------------------------------------- -------------------------------- | ----------------- ---------------`bool` | 1 | 0 | 1`int8`，`uint8` | 1 | 0 | 1`int16`，`uint16` | 2 | 0 | 2`int32`，`uint32`，`float32` | 4 | 0 | 4`int64`，`uint64`，`float64` | 8 | 0 | 8`enum`，`bits | | （基础类型）| 0 | （底层类型）`handle`等。 | 4 | 0 | 4`array <T>：N` | sizeof（T）* N | 0 | alignof（T）`vector`等。 | 16 | N * sizeof（T）| 8`struct` | sum（sizeof（fields））+填充| 0 | 8`struct？`| 8 | sum（sizeof（fields））+填充| 8`工会`| 4 + max（sizeof（fields））+ padding | 0 | max（所有字段）`联合？ 8 | 4 + max（sizeof（fields））+ padding | 8`信封`| 16 | sizeof（field）| 8`桌`| 16 | M * sizeof（信封）+ sum（aligned_to_8（sizeof（当前字段））| 8`xunion`，`xunion？`| 24 | sizeof（所选变体）| 8

The `handle` entry above refers to all flavors of handles, specifically `handle`, `handle?`, `handle<H>`, `handle<H>?`, `Protocol`, `Protocol?`,`request<Protocol>`, and `request<Protocol>?`. 上面的`handle`条目指的是所有类型的handle，特别是`handle`，`handle？`，`handle <H>`，`handle <H> ?、`Protocol，Protocol？，`request < Protocol>和request <Protocol>?。

Similarly, the `vector` entry above refers to all flavors of vectors, specifically `vector<T>`, `vector<T>?`, `vector<T>:N`, `vector<T>:N?`,`string`, `string?`, `string:N`, and `string:N?`. 类似地，上面的“ vector”条目是指所有的矢量风格，特别是“ vector <T>”，“ vector <T>？”，“ vector <T>：N”，“ vector <T>：N？”， `string`，`string？`，`string：N`和`string：N？`。

 
#### Padding  填充 

The creator of a message must fill all alignment padding gaps with zeros.  消息的创建者必须用零填充所有对齐填充空白。

The consumer of a message must verify that padding contains zeros (and generate an error if not). 消息的使用者必须验证填充是否包含零（如果不包含零，则产生错误）。

 
#### Maximum Recursion Depth  最大递归深度 

FIDL arrays, vectors, structures, tables, unions, and xunions enable the construction of recursive messages.Left unchecked, processing excessively deep messages couldlead to resource exhaustion of the consumer. FIDL数组，向量，结构，表，联合和轴销可构造递归消息。未经检查的左侧，处理过深的消息可能导致消耗资源。

For safety, the maximum recursion depth for all FIDL messages is limited to **32** levels of nested complex objects. The FIDL validator **must** enforcethis by keeping track of the current nesting level during message validation. 为了安全起见，所有FIDL消息的最大递归深度限制为嵌套复杂对象的** 32 **级。 FIDL验证器必须通过在消息验证期间跟踪当前嵌套级别来强制执行此操作。

Complex objects are arrays, vectors, structures, tables, unions, or xunions which contain pointers or handles which require fix-up.These are precisely the kinds ofobjects for which **encoding tables** must be generated. See [CLanguage Bindings](/docs/development/languages/fidl/tutorial/tutorial-c.md)for information about encodingtables. Therefore, limiting the nesting depth of complex objects has the effectof limiting the recursion depth for traversal of encoding tables. 复杂对象是包含需要修复的指针或句柄的数组，向量，结构，表，联合或轴心，这正是必须为其生成``编码表''的对象的种类。有关编码表的信息，请参见[语言绑定]（/ docs / development / languages / fidl / tutorial / tutorial-c.md）。因此，限制复杂对象的嵌套深度具有限制遍历编码表的递归深度的效果。

Formal definition:  正式定义：

 
*   The message body is defined to be at nesting level **0**.  *消息正文被定义为嵌套级别** 0 **。
*   Each time the validator encounters a complex object, it increments the nesting level, recursively validates the object, then decrements the nestinglevel. *验证器每次遇到复杂的对象时，都会递增嵌套级别，递归地验证对象，然后递减嵌套级别。
*   If at any time the nesting level exceeds **31**, a validation error is raised and validation terminates. *如果任何时候嵌套级别超过** 31 **，都会引发验证错误并终止验证。

 
#### Validation  验证方式 

The purpose of message validation is to discover wire format errors early before they have a chance to induce security or stability problems. 消息验证的目的是在有线格式错误有机会引起安全性或稳定性问题之前及早发现错误。

Message validation is **required** when decoding messages received from a peer to prevent bad data from propagating beyond the service entry point. 解码从对等方收到的消息时，需要进行消息验证，以防止不良数据传播到服务入口点之外。

Message validation is **optional but recommended** when encoding messages to send to a peer in order to help localize violated integrity constraints. **邮件验证是可选的，但建议**，当对要发送给对等方的邮件进行编码以帮助定位违反的完整性约束时，建议使用**。

To minimize runtime overhead, validation should generally be performed as part of a single pass message encoding or decoding process, such that only a singletraversal is needed. Since messages are encoded in depth-first traversal order,traversal exhibits good memory locality and should therefore be quite efficient. 为了使运行时开销最小化，通常应将验证作为单遍消息编码或解码过程的一部分来执行，以便仅需要单遍历。由于消息是按照深度优先遍历顺序进行编码的，因此遍历表现出良好的内存局部性，因此应该非常有效。

For simple messages, validation may be very trivial, amounting to no more than a few size checks. While programmers are encouraged to rely on their FIDL bindingslibrary to validate messages on their behalf, validation can also be donemanually if needed. 对于简单的消息，验证可能非常琐碎，总共不超过几个大小检查。虽然鼓励程序员依靠FIDL绑定库来代表他们验证消息，但是如果需要，也可以手动进行验证。

Conformant FIDL bindings must check all of the following integrity constraints:  合格的FIDL绑定必须检查以下所有完整性约束：

 
*   The total size of the message including all of its out-of-line sub-objects exactly equals the total size of the buffer that contains it. Allsub-objects are accounted for. *消息的总大小（包括其所有离线对象）完全等于包含该消息的缓冲区的总大小。考虑了所有子对象。
*   The total number of handles referenced by the message exactly equals the total size of the handle table. All handles are accounted for. *消息引用的句柄总数恰好等于句柄表的总大小。所有的手柄都占了。
*   The maximum recursion depth for complex objects is not exceeded.  *不超过复杂对象的最大递归深度。
*   All enum values fall within their defined range.  *所有枚举值都在其定义的范围内。
*   All union and xunion tag values fall within their defined range.  *所有的union和xunion标签值都在其定义的范围内。
*   Encoding only:  *仅编码：
    *   All pointers to sub-objects encountered during traversal refer precisely to the next buffer position where a sub-object is expected to appear. Asa corollary, pointers never refer to locations outside of the buffer. *遍历过程中遇到的所有指向子对象的指针均精确地指向预期出现子对象的下一个缓冲区位置。因此，指针永远不会指向缓冲区之外的位置。
*   Decoding only:  *仅解码：
    *   All present and not-present flags for referenced sub-objects hold the value **0** or **UINTPTR_MAX** only. *引用的子对象的所有存在和不存在标志仅保留值** 0 **或** UINTPTR_MAX **。
    *   All present and not-present flags for referenced handles hold the value **0** or **UINT32_MAX** only. *引用句柄的所有存在和不存在标志仅保留值** 0 **或** UINT32_MAX **。

 
#### Header Flags {#flags}  标头标志{flags} 

*Flags[0]*  *标志[0] *

| Bit     | Current Usage                                                                                                                                                                   | Past Usages | |---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|| 1       | Unused                                                                                                                                                                          |             || 1       | Unused                                                                                                                                                                          |             || 1       | Unused                                                                                                                                                                          |             || 7 (MSB) | Unused                                                                                                                                                                          |             || 6       | Unused                                                                                                                                                                          |             || 5       | Unused                                                                                                                                                                          |             || 4       | Unused                                                                                                                                                                          |             || 3       | Unused                                                                                                                                                                          |             || 2       | Unused                                                                                                                                                                          |             || 1       | Unused                                                                                                                                                                          |             || 0 (LSB) | Indicates whether static unions should be encoded as xunions, to soft transition [FTP-015](/docs/development/languages/fidl/reference/ftp/ftp-015.md) |             | |位|当前用法过去的用法| --------- | --------------------------------------- -------------------------------------------------- -------------------------------------------------- -------------------------------------- | ----------- -|| 1 |未使用|| 1 |未使用|| 1 |未使用|| 7（MSB）|未使用|| 6 |未使用|| 5 |未使用|| 4 |未使用|| 3 |未使用|| 2 |未使用|| 1 |未使用|| 0（LSB）|指示是否应将静态联合编码为xunion，以进行软过渡[FTP-015]（/ docs / development / languages / fidl / reference / ftp / ftp-015.md）| |

*Flags[1]*  *标志[1] *

| Bit     | Current Usage                                                | Past Usages | |---------|--------------------------------------------------------------|-------------|| 7 (MSB) | Unused                                                       |             || 6       | Unused                                                       |             || 5       | Unused                                                       |             || 4       | Unused                                                       |             || 3       | Unused                                                       |             || 2       | Unused                                                       |             || 1       | Unused                                                       |             || 0       | Unused                                                       |             | |位|当前用法过去的用法| --------- | --------------------------------------- ----------------------- | ------------- || 7（MSB）|未使用|| 6 |未使用|| 5 |未使用|| 4 |未使用|| 3 |未使用|| 2 |未使用|| 1 |未使用|| 0 |未使用|

*Flags[2]*  *标志[2] *

| Bit     | Current Usage                                                | Past Usages | |---------|--------------------------------------------------------------|-------------|| 7 (MSB) | Unused                                                       |             || 6       | Unused                                                       |             || 5       | Unused                                                       |             || 4       | Unused                                                       |             || 3       | Unused                                                       |             || 2       | Unused                                                       |             || 1       | Unused                                                       |             || 0       | Unused                                                       |             | |位|当前用法过去的用法| --------- | --------------------------------------- ----------------------- | ------------- || 7（MSB）|未使用|| 6 |未使用|| 5 |未使用|| 4 |未使用|| 3 |未使用|| 2 |未使用|| 1 |未使用|| 0 |未使用|

 
#### Footnote 1  脚注1 

Defining the zero handle to mean "there is no handle" means it is safe to default-initialize wire format structures to all zeros. Zero is also the valueof the `ZX_HANDLE_INVALID` constant. 将零句柄定义为“没有句柄”意味着将线格式结构默认初始化为全零是安全的。零也是ZX_HANDLE_INVALID常量的值。

 
#### Footnote 2  脚注2 

Read [The Lost Art of Structure Packing][lostart] for an in-depth treatise on the subject.  阅读[结构包装的失落的艺术] [入门]，以获取有关该主题的深入论述。

