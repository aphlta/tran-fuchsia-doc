 

 
# FIDL JSON Internal Representation  FIDL JSON内部表示 

For all backends (except C), the FIDL compiler operates in two phases. A first phase parses the FIDL file(s) and produces a JSON-based IntermediateRepresentation (**IR**).A second phase takes the IR as input, and produces the appropriate language-specific output. 对于所有后端（C除外），FIDL编译器分两个阶段运行。第一阶段解析FIDL文件并生成基于JSON的中间表示（** IR **）;第二阶段将IR作为输入，并生成适当的特定于语言的输出。

This section documents the JSON IR.  本节介绍了JSON IR。

If you are interested in the JSON IR, you can generate it by running the FIDL compiler with the `json` output directive: 如果您对JSON IR感兴趣，则可以通过使用`json`输出指令运行FIDL编译器来生成它：

```
fidlc --json outputfile.json --files inputfile.fidl
```
 

 
## A simple example  一个简单的例子 

To get started, we can see how a simple example looks. We'll use the `echo.fidl` ["Hello World Echo Protocol"](../tutorial/README.md)example from the tutorial: 首先，我们可以看到一个简单的示例。我们将使用本教程中的`echo.fidl` [“ Hello World Echo Protocol”]（../ tutorial / README.md）示例：

```fidl
library fidl.examples.echo;

[Discoverable]
protocol Echo {
    EchoString(string? value) -> (string? response);
};
```
 

The tutorial goes through this line-by-line, but the summary is that we create a discoverable protocol called `Echo` with a method called `EchoString`.The `EchoString` method takes an optional string called `value` and returnsan optional string called `response`. 本教程逐行进行了介绍，但摘要是，我们使用名为`EchoString`的方法创建了一个名为`Echo`的可发现协议。`EchoString`方法采用了名为`value`的可选字符串并返回了可选字符串称为“响应”。

Regardless of the FIDL input, the FIDL compiler generates a JSON data set with the following overall shape: 无论FIDL输入如何，FIDL编译器都会生成具有以下总体形状的JSON数据集：

```json
{
  "version": "0.0.1",
  "name": "libraryname",
  "library_dependencies": [],
  "const_declarations": [],
  "enum_declarations": [],
  "interface_declarations": [],
  "struct_declarations": [],
  "table_declarations": [],
  "union_declarations": [],
  "declaration_order": [],
  "declarations": {}
}
```
 

The JSON members (name-value pairs) are as follows:  JSON成员（名称-值对）如下：

Name                    | Meaning ------------------------|-----------------------------------------------------------------------version                 | A string indicating the version of the JSON IR schemaname                    | A string indicating the given `library` namelibrary_dependencies    | A list of dependencies on other librariesconst_declarations      | A list of constsenum_declarations       | A list of enumsinterface_declarations  | A list of protocols providedstruct_declarations     | A list of structstable_declarations      | A list of tablesunion_declarations      | A list of unionsdeclaration_order       | A list of the object declarations, in order of declarationdeclarations            | A list of declarations and their types 姓名|含义------------------------ | ------------------------ -----------------------------------------------版本|一个字符串，指示JSON IR模式名称的版本。一个字符串，指示给定的`library` namelibrary_dependencies |与其他库的依赖关系列表constsenum_declarations的列表| enumsinterface_declarations的列表|提供的协议列表structstable_declarations的列表| tablesunion_declarations的列表| unionsclaration_order的列表|对象声明的列表，按声明声明的顺序|声明及其类型列表

Not all members have content.  并非所有成员都有内容。

So, for our simple example, here's what the JSON IR looks like (line numbers have been added for reference; they are not part of the generated code): 因此，对于我们的简单示例，这是JSON IR的样子（已添加行号以供参考；它们不属于生成的代码）：

```json
[01]    {
[02]      "version": "0.0.1",
[03]      "name": "fidl.examples.echo;",
[04]      "library_dependencies": [],
[05]      "const_declarations": [],
[06]      "enum_declarations": [],
[07]      "interface_declarations": [

(content discussed below)

[53]      ],
[54]      "struct_declarations": [],
[55]      "table_declarations": [],
[56]      "union_declarations": [],
[57]      "declaration_order": [
[58]        "fidl.examples.echo/Echo"
[59]      ],
[60]      "declarations": {
[61]        "fidl.examples.echo/Echo": "interface"
[62]      }
[63]    }
```
 

Lines `[01]` and `[63]` wrap the entire JSON object.  第[01]和第[63]行包装了整个JSON对象。

Line `[02]` is the version number of the JSON IR schema.  第[02]行是JSON IR模式的版本号。

Line `[03]` is the name of the library, and is copied from the FIDL `library` directive.  第[03]行是库的名称，是从FIDL`library`指令复制而来的。

Lines `[04]`, `[05]` and `[06]` are the library dependencies, constant declarations, and enumeration declarations.Our simple example doesn't have any, so they just have a zero-sized (empty) arrayas their value ("`[]`").Similarly, there are no structs (line `[54]`), tables (`[55]`) or unions (`[56]`).The declaration order (`[57]`..`[59]`) isn't that interesting either,because there's only the one declaration, and, finally, thedeclarations member (`[60]`..`[62]`) just indicates the declared object (here,`fidl.examples.echo/Echo`) and its type (it's an `interface`). 第[04]，第[05]和第[06]行是库依赖项，常量声明和枚举声明。我们的简单示例没有任何内容，因此它们的大小为零（空）数组作为它们的值（“`[]`”）。类似地，没有结构（第[54]行），表（[55]`）或并集（[56]`）。声明顺序（` [57]`..` [59]`也没有那么有趣，因为只有一个声明，最后，declarations成员（[[60]`..` [62]`）仅表示已声明对象（此处为fidl.examples.echo / Echo）及其类型（即接口）。

 
## The protocol  协议 

Where things are interesting, though, is starting with line `[07]` &mdash; it's the protocol declaration for all protocols in the file. 不过，有趣的地方是从“ [07]”行开始。它是文件中所有协议的协议声明。

Our simple example has just one protocol, called `Echo`, so there's just one array element:  我们的简单示例只有一个协议，称为“ Echo”，因此只有一个数组元素：

```json
[07]      "interface_declarations": [
[08]        {
[09]          "name": "fidl.examples.echo/Echo",
[10]          "maybe_attributes": [
[11]            {
[12]              "name": "Discoverable",
[13]              "value": ""
[14]            }
[15]          ],
[16]          "methods": [
[17]            {
[18]              "ordinal": 1108195967,
[19]              "name": "EchoString",
[20]              "has_request": true,
[21]              "maybe_request": [
[22]                {
[23]                  "type": {
[24]                    "kind": "string",
[25]                    "nullable": true
[26]                  },
[27]                  "name": "value",
[28]                  "size": 16,
[29]                  "alignment": 8,
[30]                  "offset": 16
[31]                }
[32]              ],
[33]              "maybe_request_size": 32,
[34]              "maybe_request_alignment": 8,
[35]              "has_response": true,
[36]              "maybe_response": [
[37]                {
[38]                  "type": {
[39]                    "kind": "string",
[40]                    "nullable": true
[41]                  },
[42]                  "name": "response",
[43]                  "size": 16,
[44]                  "alignment": 8,
[45]                  "offset": 16
[46]                }
[47]              ],
[48]              "maybe_response_size": 32,
[49]              "maybe_response_alignment": 8
[50]            }
[51]          ]
[52]        }
[53]      ],
```
 

Each protocol declaration array element contains:  每个协议声明数组元素包含：

 
*   Line `[09]`: the name of the object (`fidl.examples.echo/Echo` &mdash; this gets matched up with the `declarations` member contents starting on line`[60]`), *第[09]行：对象的名称（fidl.examples.echo / Echo mdash；这与从第[60]行开始的`declarations`成员内容相匹配），
*   Lines `[10]`..`[15]`: an optional list of attributes (we had marked it as `Discoverable` &mdash; if we did not specify any attributes then we wouldn'tsee lines `[10]` through `[15]`), and * [10] ... [15]行：属性的可选列表（我们将其标记为“ Discoverable” mdash；如果未指定任何属性，则看不到“ [10]”行`[15]`）和
*   Lines `[16]`..`[51]`: an optional array of methods.  * [16] ... [51]行：可选的方法数组。

The methods array lists the defined methods in declaration order (giving details about the ordinal number, the name of the method, whether it has a requestcomponent and a response component, and indicates the sizes and alignments ofthose componenets). 方法数组按声明顺序列出定义的方法（提供有关序号，方法名称，它是否具有request组件和Response组件的详细信息，并指示这些组件的大小和对齐方式）。

The JSON output has two `bool`s, `has_request` and `has_response`, that indicate if the protocol defines a request and a response, respectively. JSON输出具有两个布尔值，即has_request和has_response，分别指示协议是否定义了请求和响应。

Since the string parameters within the request and response are both optional, the parameter description specifies `"nullable": true` (line `[25]` and `[40]`). 由于请求和响应中的字符串参数都是可选的，因此参数描述指定了““ nullable”：true”（第[25]和第[40]行）。

 
### What about the sizes?  大小呢？ 

The `size` members might be confusing at first; it's important here to note that the size refers to the size of the *container* and not the *contents*. “大小”成员起初可能会感到困惑；重要的是要注意，尺寸是指容器*的尺寸，而不是内容*的尺寸。

Note: Before reading this section, consider referring to the [on-wire](wire-format/README.md) format. 注意：在阅读本节之前，请考虑参考[on-wire]（线格式/README.md）格式。

Lines `[36]` through `[47]`, for example, define the `response` string container. It's 16 bytes long, and consists of two 64-bit values: 例如，行[36]到[47]定义了“响应”字符串容器。它长16个字节，由两个64位值组成：

 
*   a size field, indicating the number of bytes in the string (we don't rely on NUL termination), and *大小字段，指示字符串中的字节数（我们不依赖NUL终止），并且
*   a data field, which indicates presence or pointer, depending on context.  *一个数据字段，根据上下文指示存在或指针。

For the data field, two interpretations are possible. In the "wire format" version (that is, as the data is encoded for transmission),the data field has one of two values: zero indicates the string is null,and `UINTPTR_MAX` indicates that the data is present.(See the [Wire Format](wire-format/README.md) chapter for details). 对于数据字段，可能有两种解释。在“有线格式”版本中（即，由于对数据进行了编码以进行传输），数据字段具有以下两个值之一：零表示字符串为空，而“ UINTPTR_MAX”表示存在数据。（请参阅[Wire格式]（wire-format / README.md章节以了解详细信息）。

However, when this field has been read into memory and is decoded for consumption, it contains a 0 (if the string is null), otherwise it's a pointerto where the string content is stored. 但是，当将该字段读入内存并进行解码以进行使用时，它包含一个0（如果字符串为null），否则它是存储字符串内容的指针。

The other fields, like `alignment` and `offset`, also relate to the [on-wire](wire-format/README.md) data marshalling. 其他字段，例如“ alignment”和“ offset”，也与[on-wire]（wire-format / README.md）数据编组有关。

 
## Of structs, tables, and unions  结构，表和联合的 

Expanding on the structs, tables, and unions (`struct_declarations`, `table_declarations`, and `union_declarations`) from above, suppose we have a simple FIDL file likethe following: 从上面扩展结构，表和联合（“ struct_declarations”，“ table_declarations”和“ union_declarations”），假设我们有一个简单的FIDL文件，如下所示：

```fidl
library foo;

union Union1 {
    int64 x;
    float64 y;
};

table Table1 {
    1: int64 x;
    2: int64 y;
    3: reserved;
};

struct Struct1 {
    int64 x;
    int64 y;
};
```
 

The JSON that's generated will contain common elements for all three types. Generally, the form taken is: 生成的JSON将包含所有三种类型的通用元素。通常，采用的形式为：

```json
"<TYPE>_declarations": [
  {
    <HEADER>
    "members": [
      <MEMBER>
      <MEMBER>...
    ],
    <TRAILER>
  }
]
```
 

Where:  哪里：

Element     | Meaning ------------|-------------------------------------------------------------------------------------`<TYPE>`    | one of `struct`, `table`, or `union``<HEADER>`  | contains the name of the structure, table, or union, and optional characteristics`<MEMBER>`  | contains information about an element member`<TRAILER>` | contains more information about the structure, table, or union 元素|含义------------ | ------------------------------------ -------------------------------------------------` <TYPE>`| `struct`，`table`或ʻunion`` <HEADER>`中的一个|包含结构，表或联合的名称，以及可选的特征<MEMBER>包含有关元素成员`<TRAILER>`|的信息。包含有关结构，表或联合的更多信息

 
### The `struct_declarations`  `struct_declarations` 

For the `struct_declarations`, the FIDL code above generates the following (we'll come back and look at the `members` part shortly): 对于`struct_declarations`，上面的FIDL代码生成以下内容（我们将很快回来查看`members'部分）：

```json
[01] "struct_declarations": [
[02]   {
[03]     "name": "foo/Struct1",
[04]     "anonymous": false,
[05]     "members": [
[06]       <MEMBER>
[07]       <MEMBER>
[08]     ],
[09]     "size": 16,
[10]     "max_out_of_line": 0,
[11]     "alignment": 8,
[12]     "max_handles": 0
[13]   }
[14] ],
```
 

Specifically, the `<HEADER>` section (lines `[03]` and `[04]`) contains a `"name"` field (`[03]`). This is a combination of the `library` name and the name of the structure, giving `foo/Struct1`. 具体来说，“ <HEADER>”部分（第[03]和第[04]行）包含一个“名称”字段（“ [03]”）。这是库名称和结构名称的组合，为foo / Struct1。

Next, the `"anonymous"` field (`[04]`) is used to indicate if the structure is anonymous or named, just like in C.Since neither `table` nor `union` can be anonymous, this field ispresent only with `struct`. 接下来，“ anonymous”字段（“ [04]”）用于指示结构是匿名的还是命名的，就像在C中一样。由于“ table”和“ union”都不能匿名，因此该字段仅存在与`struct`。

Saving the member discussion for later, the `<TRAILER>` (lines `[09]` through `[12]`) has the following fields: 将成员讨论保存起来以备后用，`<TRAILER>`（第[09]`行至[[12]`行）具有以下字段：

Field             | Meaning ------------------|-------------------------------------------------------------------------------`size`            | The total number of bytes contained in the structure`max_out_of_line` | The maximum size of out-of-line data`alignment`       | Alignment requirements of the object`max_handles`     | The maximum number of handles 领域含义------------------ | ------------------------------ -------------------------------------------------`大小`| max_out_of_line结构|中包含的字节总数|离线数据对齐的最大大小|对象max_handles的对齐要求|最大句柄数

These four fields are common to the `table_declarations` as well as the `union_declarations`.  这四个字段是table_declarations和union_declarations共有的。

 
### The `table_declarations` and `union_declarations`  `table_declarations`和`union_declarations` 

The `table_declarations` and `union_declarations` have the same `<HEADER>` fields as the `struct_declarations`, except that they don't have an `anonymous` field,and the `table_declarations` doesn't have an `offset` field.A `table_declarations` does, however, have some additional fields in its `<MEMBER>` part,we'll discuss these below. `table_declarations`和`union_declarations`与`struct_declarations`具有相同的<HEADER>字段，除了它们没有`anonymous`字段，并且`table_declarations`没有`offset`字段。 .table_declarations`的<MEMBER>部分确实有一些附加字段，我们将在下面讨论。

 
### The `<MEMBER>` part  `<MEMBER>`部分 

Common to all three of the above (`struct_definition`, `table_definition`, and `union_definition`) is the `<MEMBER>` part. 以上三个部分（“ struct_definition”，“ table_definition”和“ union_definition”）的共同点是“ <MEMBER>”部分。

It describes each struct, table, or union member.  它描述了每个结构，表或联合成员。

Let's look at the `<MEMBER>` part for the `struct_declarations` for the first member, `int64 x`: 让我们来看一下第一个成员“ int64 x”的“ struct_declarations”的“ <MEMBER>”部分：

```json
[01] "members": [
[02]   {
[03]     "type": {
[04]       "kind": "primitive",
[05]       "subtype": "int64"
[06]     },
[07]     "name": "x",
[08]     "size": 8,
[09]     "max_out_of_line": 0,
[10]     "alignment": 8,
[11]     "offset": 0,
[12]     "max_handles": 0
[13]   },
```
 

The fields here are:  这里的字段是：

Field             | Meaning ------------------|-------------------------------------------------------------------------------`type`            | A description of the type of the member`name`            | The name of the member`size`            | The number of bytes occupied by the member`max_out_of_line` | The maximum size of out-of-line data`alignment`       | Alignment requirements of the member`offset`          | Offset of the member from the start of the structure`max_handles`     | The maximum number of handles 领域含义------------------ | ------------------------------ -------------------------------------------------`类型`|成员名称类型|的描述成员大小的名称|成员max_out_of_line`占用的字节数|离线数据对齐的最大大小|成员偏移量的对齐要求|成员从max_handles结构开始时的偏移量|最大句柄数

The second member, `int64 y` is identical except:  第二个成员int64 y相同，除了：

 
*   its `"name"` is `"y"` instead of `"x"`,  *它的“名称”是“ y”而不是“ x”，
*   its `offset` is `8` instead of `0`.  *其偏移量为8，而不是0。

 
#### `max_out_of_line`  max_out_of_line 

The `max_out_of_line` field indicates the maximum number of bytes which may be stored out-of-line. For instance with strings, the character array itself is stored out-of-line (that is, as data thatfollows the structure), with the string's size and presence indicator being stored in-line. “ max_out_of_line”字段指示可以离线存储的最大字节数。例如，对于字符串，字符数组本身是离线存储的（即，作为遵循结构的数据），而字符串的大小和存在指示符则是在线存储的。

 
#### `max_handles`  `max_handles` 

The `max_handles` field indicates the maximum number of handles to associate with the object. Since in this case it's a simple integer, the value is zero because an integer doesn't carryany handles. “ max_handles”字段指示与对象关联的最大句柄数。由于在这种情况下它是一个简单的整数，因此该值为零，因为整数不携带任何句柄。

 
#### The `<MEMBER>` part of a `table_declarations`  table_declarations的<MEMBER>部分 

A `table_declarations` has the same `<MEMBER>` fields as the `struct_declarations` described above, minus the `offset` and `anonymous` fields, plus two additional fields: 一个table_declarations与上面的struct_declarations具有相同的<MEMBER>字段，减去offset和anonymous字段，再加上两个附加字段：

Field      | Meaning -----------|--------------------------------------------------------------------------------------`ordinal`  | This is the "serial number" of this table member`reserved` | A flag indicating if this table member is reserved for future use 领域含义----------- || ------------------------------------- -------------------------------------------------`顺序`|这是该表成员保留的“序列号” |一个标志，指示此表成员是否保留供将来使用

Note: If the `reserved` flag indicates the table member is reserved for future use, then there is no definition of the member given; conversely, if the flagindicates the member is not reserved, then the member definition followsimmediately after. 注意：如果`reserved`标志表明该表成员是保留供以后使用的，则没有给定成员的定义。相反，如果该标志指示该成员未被保留，则成员定义紧随其后。

In the FIDL example above, the `table_declarations` has the following `<MEMBER>` part for the first member, `x`: 在上面的FIDL示例中，`table_declarations`对于第一个成员x具有以下<MEMBER>部分：

```json
[01] "members": [
[02]   {
[03]     "ordinal": 1,
[04]     "reserved": false,
[05]     "type": {
[06]       "kind": "primitive",
[07]       "subtype": "int64"
[08]     },
[09]     "name": "x",
[10]     "size": 8,
[11]     "max_out_of_line": 0,
[12]     "alignment": 8,
[13]     "max_handles": 0
[14]   },
```
 

Here, the `ordinal` (`[03]`) has the value `1`, and the `reserved` flag (`[04]`) indicates that this field is not reserved (this means that the field is present).This matches the FIDL declaration from above: 这里，“ ordinal”（“ [03]”）的值为“ 1”，“ reserved”标志（“ [04]”）表示该字段未保留（表示该字段存在）。这与上面的FIDL声明匹配：

```fidl
table Table1 {
    1: int64 x;
    2: int64 y;
    3: reserved;
};
```
 

The `<MEMBER>` part for the second member, `y`, is almost identical:  第二个成员y的<MEMBER>部分几乎相同：

```json
[01] "members": [
[02]   ... // member data for "x"
[03]   {
[04]     "ordinal": 2,
[05]     "reserved": false,
[06]     "type": {
[07]       "kind": "primitive",
[08]       "subtype": "int64"
[09]     },
[10]     "name": "y",
[11]     "size": 8,
[12]     "max_out_of_line": 0,
[13]     "alignment": 8,
[14]     "max_handles": 0
[15]   },
```
 

The difference is that the `ordinal` field (`[04]`) has the value `2` (again, corresponding to what we specified in the FIDL code above). 区别在于，“普通”字段（“ [04]”）的值为“ 2”（再次对应于我们在上面的FIDL代码中指定的值）。

Finally, the third `<MEMBER>`, representing the reserved member, is a little different:  最后，代表保留成员的第三个`<MEMBER>`稍有不同：

```json
[01] "members": [
[02]   ... // member data for "x"
[03]   ... // member data for "y"
[04]   {
[05]     "ordinal": 3,
[06]     "reserved": true
[07]   }
```
 

As you'd expect, the `ordinal` value (`[05]`) is `3`, and the `reserved` flag (`[06]`) is set to `true` this time, indicating that this is indeed a reserved member.The `true` value means that the field is *not* specified (that is, there are no `"type"`,`"name"`, `"size"`, and so on fields following). 如您所料，`ordinal`值（`[05]`）为`3`，并且`reserved`标志（`[06]`）这次设置为`true`，表明这确实是保留值。“ true”值表示未指定该字段（即，后面没有“ type”，“ name”，“ size”等字段）。

 
#### The `<MEMBER>` part of a `union_declarations`  union_declarations`的`<MEMBER>`部分 

The `<MEMBER>` part of a `union_declarations` is identical to that of a `struct_declarations`, except that: “ union_declarations”的“ <MEMBER>”部分与“ struct_declarations”的部分相同，除了：

 
*   there is no `max_handles` field (unions can't contain handles)  *没有`max_handles`字段（联合不能包含句柄）
*   the `offset` field may refer to the same offset for multiple members  *`offset`字段可能引用多个成员的相同偏移量

Recall that a `union` is an "overlay" &mdash; several different data layouts are considered to be sharing the space.In the FIDL code we saw above, we said that the data can be a 64-bit integer (called `x`)or it could be a floating point value (called `y`). 回想一下，“ union”是“ overlay” mdash；几种不同的数据布局被认为可以共享空间。在上面的FIDL代码中，我们说过数据可以是64位整数（称为x），也可以是浮点值（称为y）。 `）。

This explains why both `offset` fields have the same value &mdash; `x` and `y` share the same space. 这解释了为什么两个“ offset”字段都具有相同的值mdash； x和y共享相同的空间。

Here are just the `offset` parts (and some context) for the `union_declarations` from the FIDL above: 这只是上面FIDL中的`union_declarations`的`offset`部分（和一些上下文）：

```json
[01] "union_declarations": [
[02]   {
[03]     "name": "foo/Union1",
[04]     "members": [
[05]       {
[06]         "name": "x",
[07]         "offset": 8
[08]       },
[09]       {
[10]         "name": "y",
[11]         "offset": 8
[12]       }
[13]     ],
[14]     "size": 16,
[15]   }
[16] ],
```
 

The natural questions you may have are, "why do the offsets (`[07]` and `[11]`) start at 8 when there's nothing else in the union?And why is the size of the union 16 bytes (`[14]`) when there's only 8 bytes of datapresent?" 您可能会想到一个自然的问题：“当联合中没有其他内容时，为什么偏移量（[[07]`和`[11]`]从8开始？为什么联合的大小为16字节（`[ 14]`）仅存在8个字节的数据？”

Certainly, in C you'd expect that a union such as:  当然，在C语言中，您期望这样的联合：

```c
union Union1 {
  int64_t x;
  double y;  // "float64" in FIDL
};
```
 

would occupy 8 bytes (the size required to store the largest element), and that both `x` and `y` would start at offset zero. 将占用8个字节（存储最大元素所需的大小），并且x和y都将从偏移量0开始。

In FIDL, unions have the special property that there's an identifier at the beginning that is used to tell which member the union is holding.It's as if we had this in the C version: 在FIDL中，联合具有特殊的属性，即在开头有一个标识符，用于标识联合持有的成员，就像我们在C版本中拥有的那样：

```c
enum Union1_types { USING_X, USING_Y };

struct Union1 {
  Union1_types which_one;
  union {
    int64_t x;
    double y;
  };
};
```
 

That is to say, the first field of the data structure indicates which interpretation of the union should be used: the 64-bit integer `x` version, or the floating point `y`version. 也就是说，数据结构的第一个字段指示应使用联合的哪种解释：64位整数“ x”版本或浮点“ y”版本。

> In the FIDL implementation, the "tag" or "discriminant" (what we called `which_one` > in the C version) is a 32-bit unsigned integer.> Since the alignment of the union is 8 bytes, 4 bytes of padding are added after the> tag, giving a total size of 16 bytes for the union. >在FIDL实现中，“标记”或“区别的”（在C版本中，我们称为“ which_one”>）是一个32位无符号整数。>由于联合的对齐方式是8个字节，因此填充4个字节在>标记后添加，使联合的总大小为16个字节。

 
### Aggregates  骨料 

More complicated aggregations of data are, of course, possible. You may have a struct (or table or union) that contains other structures (or tablesor unions) within it. 当然，可以进行更复杂的数据聚合。您可能有一个结构（或表或联合），其中包含其他结构（或表或联合）。

As a trivial example, just to show the concept, let's include the `Union1` union as member `u` (line `[09]` below) within our previous structure: 举一个简单的例子，为了说明这个概念，让我们在前面的结构中加入作为成员u成员的Union1联合（下面的行[09]行）：

```fidl
[01] union Union1 {
[02]     int64 x;
[03]     float64 y;
[04] };
[05]
[06] struct Struct1 {
[07]     int64 x;
[08]     int64 y;
[09]     Union1 u;
[10] };
```
 

This changes the JSON output for the `Struct1` `struct_declarations` as follows:  这将更改`Struct1``struct_declarations`的JSON输出，如下所示：

```json
[01] "struct_declarations": [
[02]   {
[03]     "name": "foo/Struct1",
[04]     "anonymous": false,
[05]     "members": [
[06]       ... // member data for "x" as before
[07]       ... // member data for "y" as before
[08]       {
[09]         "type": {
[10]           "kind": "identifier",
[11]           "identifier": "foo/Union1",
[12]           "nullable": false
[13]         },
[14]         "name": "u",
[15]         "size": 16,
[16]         "max_out_of_line": 0,
[17]         "alignment": 8,
[18]         "offset": 16,
[19]         "max_handles": 0
[20]       }
[21]     ],
[22]     "size": 32,
[23]     "max_out_of_line": 0,
[24]     "alignment": 8,
[25]     "max_handles": 0
[26]   }
[27] ],
```
 

The changes are as follows:  更改如下：

 
*   New `<MEMBER>` entry for the union `u` (`[08]` through `[20]`),  *联合u的新的<MEMBER>条目（[08]至[20]），
*   The `size` (`[22]`) of the `struct_declarations` has now doubled to `32`  *`struct_declarations`的`size`（`[22]`）现在已翻倍至`32`

We'll examine these in order.  我们将按顺序检查这些内容。

Whereas in the previous examples we had simple `"type"` fields, e.g.:  而在前面的示例中，我们有简单的“ type”字段，例如：

```json
"type": {
  "kind": "primitive",
  "subtype": "int64"
},
```
 

(and, for the union's `float64 y`, we'd have `"subtype": "float64"`), we now have: （并且，对于联合会的`float64 y`，我们将具有`“ subtype”：“ float64”`），我们现在具有：

```json
"type": {
  "kind": "identifier",
  "identifier": "foo/Union1",
  "nullable": false
},
```
 

The `"kind"` is an `identifier` &mdash; this means that it's a symbol of some sort, one that is defined elsewhere (and indeed, we defined `foo/Union1` inthe FIDL file as a union). “种类”是一个标识符。这意味着它是某种符号，在其他地方定义（实际上，我们在FIDL文件中将`foo / Union1`定义为并集）。

The `"nullable"` flag indicates if the member is optional or mandatory, just like we discussed above in the section on [Protocols](#The-protocol).In this case, since `"nullable"` is `false`, the member is mandatory. 就像我们上面在[Protocols]（The-protocol）一节中讨论的那样，“ nullable”标志指示成员是可选成员还是强制成员。在这种情况下，由于“ nullable”是“ false”，因此成员是强制性的。

Had we specified:  我们是否已指定：

```fidl
union Union1 {
    int64 x;
    float64 y;
};

struct Struct1 {
    int64 x;
    int64 y;
    Union1? u;  // "?" indicates nullable
};
```
 

Then we'd see the `"nullable"` flag set to `true`, indicating that the union `u` is optional. 然后，我们将看到“ nullable”标志设置为“ true”，表明并集“ u”是可选的。

When the `nullable` flag is set (indicating optional), the union value is stored out-of-line and the in-line indication consists of just a presence andsize indicator (8 bytes).This causes the `max_out_of_line` value to change from 0 to 16 (because that'sthe size of the out-of-line data), and the size of the entire `struct_declarations`object shrinks from the 32 shown above to 24 bytes &mdash; `16 - 8 = 8` bytes less. 当设置了'nullable'标志（表示可选）时，联合值被存储在行外，并且行内指示仅由状态和大小指示符（8个字节）组成，这会导致`max_out_of_line`值发生变化从0到16（因为这是行外数据的大小），并且整个“ struct_declarations”对象的大小从上面显示的32个字节缩小为24个字节-少16-8 = 8个字节。

