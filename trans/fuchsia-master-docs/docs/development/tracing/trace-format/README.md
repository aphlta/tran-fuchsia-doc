 
# Fuchsia Trace Format  紫红色痕迹格式 

This document describes the binary format used to collect, store, and transmit Fuchsia trace records. 本文档介绍了用于收集，存储和传输紫红色跟踪记录的二进制格式。

See [Fuchsia Tracing System Design](../design.md) for an overview.  有关概述，请参见[紫红色的跟踪系统设计]（../ design.md）。

 
## Purpose  目的 

While a trace is running, _trace providers_ write records into a trace buffer VMO shared with the trace manager using the binary format described in thisdocument. 跟踪运行时，_trace provider_使用本文档中描述的二进制格式将记录写入与跟踪管理器共享的跟踪缓冲区VMO中。

The binary format is designed to introduce minimal impact upon the performance of the subject under trace while writing traces.  The recordsare also written sequentially so that if a trace terminates (normally orabnormally), the trace manager can still recover partial trace data alreadystored in the trace buffer by reading everything up to the last well-formedrecord. 二进制格式旨在在编写跟踪时对跟踪下的对象性能产生最小的影响。记录也按顺序写入，因此，如果跟踪终止（正常或异常），则跟踪管理器仍可以通过读取所有内容直到最后一个格式正确的记录来恢复已存储在跟踪缓冲区中的部分跟踪数据。

As the trace progresses, the _trace manager_ aggregates records from all trace providers which are participating in trace collection and concatenatesthem together with some special metadata records to form a trace archive. 随着跟踪的进行，_trace manager_聚集来自所有参与跟踪收集的跟踪提供程序的记录，并将它们与一些特殊的元数据记录连接起来以形成跟踪存档。

Once the trace completes, tools such as the `trace` command-line program can read the trace records within the trace archive to visualize the resultsor save them to a file for later consumption. 跟踪完成后，诸如“ trace”命令行程序之类的工具可以读取跟踪档案中的跟踪记录，以可视化结果或将其保存到文件中以备后用。

 
## Features  特征 

 
- Small footprint  -占地面积小
  - Trace records are compact, packing information into a small number of bits.  -跟踪记录紧凑，将信息打包为少量位。
  - Pooling strings, processes, and threads further compacts the trace data.  -合并字符串，进程和线程可进一步压缩跟踪数据。
- Memory aligned  -内存对齐
  - Trace records maintain an 8 byte alignment in memory to facilitate writing them directly into memory mapped VMOs. -跟踪记录在内存中保持8字节对齐，以便于将它们直接写入内存映射的VMO。
- Variable size records  -可变大小的记录
  - Overall record size is limited to 32 KB.  -总记录大小限制为32 KB。
  - Large objects may need to be broken up into multiple records.  -大型对象可能需要分解成多个记录。
- Extensible  -可扩展
  - There's room to define new record types as needed.  -可以根据需要定义新的记录类型。
  - Unrecognized or malformed trace records can be skipped.  -可以跳过无法识别或格式不正确的跟踪记录。

 
## Encoding Primitives  编码原语 

 
### Records  记录 

A trace record is a binary encoded piece of trace information consisting of a sequence of [atoms](#atoms). 跟踪记录是跟踪信息的二进制编码段，由一系列[atoms]（原子）组成。

All records include a header word which contains the following basic information: 所有记录均包含标题词，其中包含以下基本信息：

 
- **Record Type**: A 4-bit field which identifies the type of the record and the information it contains.  See [Record Types](#record-types). -**记录类型**：4位字段，用于标识记录的类型及其包含的信息。请参见[记录类型]（记录类型）。
- **Record Size**: Typically, a 12-bit field which indicates the number of words (multiples of 8 byte units) within the record _including the recordheader itself_.  The maximum possible size of a record is 4095 words(32760 bytes).  Very simple records may be just 1 word (8 bytes) long.Large records use a 32-bit size field and therefore have a highermaximum size. -**记录大小**：通常是一个12位字段，指示记录_中的字数（8字节单位的倍数），包括记录头本身。一条记录的最大可能大小为4095个字（32760字节）。非常简单的记录可能只有1个字（8个字节）长。大型记录使用32位大小的字段，因此具有更大的最大大小。

Records are always a multiple of 8 bytes in length and are stored with 8 byte alignment. 记录的长度总是8字节的倍数，并以8字节对齐方式存储。

 
### Atoms  原子 

Each record is constructed as a sequence of atoms.  每个记录被构造成一个原子序列。

Each atom is written with 8 byte alignment and has a size which is also a multiple of 8 bytes so as to preserve alignment. 每个原子以8字节对齐方式写入，并且其大小也是8字节的倍数，以保留对齐方式。

There are two kinds of atoms:  有两种原子：

 
- **Word**: A 64-bit value which may be further subdivided into bit fields. Words are stored in machine word order (little-endian on all currentlysupported architectures). -**字**：64位值，可以进一步细分为位字段。字以机器字顺序存储（在所有当前支持的体系结构上为小端）。
- **Stream**: A sequence of bytes padded with zeros to the next 8 byte boundary.  Streams are stored in byte order.  Streams which are an exactmultiple of 8 bytes long are not padded (there is no zero terminator). -**流**：字节序列，用零填充到下一个8字节边界。流以字节顺序存储。不填充长度为8字节的正整数倍的流（不存在零终止符）。

**Fields** are subdivisions of 64-bit **Words**, denoted `[<least significant bit> .. <most significant bit>]` where the first andlast bit positions are inclusive.  All unused bits are reserved for futureuse and must be set to 0. **字段**是64位**字的细分，表示为[[<最低有效位> .. <最高有效位>]]，其中首尾位置包括在内。所有未使用的位保留供将来使用，必须将其设置为0。

**Words** and **Fields** store unsigned integers unless otherwise specified by the record format. 除非记录格式另外指定，否则Words和Fields存储无符号整数。

**Streams** may store either UTF-8 strings or binary data, as specified by the record format. **流**可以存储记录格式指定的UTF-8字符串或二进制数据。

 
### Archives  档案 

A trace archive is a sequence of trace records, concatenated end to end, which stores information collected by trace providers while a trace isrunning together with metadata records which identify and delimit sectionsof the trace produced by each trace provider. 跟踪档案是一系列跟踪记录，端对端连接在一起，用于存储跟踪提供者收集的信息，同时跟踪正在运行，跟踪数据与元数据记录一起识别并界定每个跟踪提供者产生的跟踪部分。

Trace archives are intended to be read sequentially since records which appear earlier in the trace may influence the interpretation of recordswhich appear later in the trace.  The trace system provides tools forextracting information from trace archives and converting it into otherforms for visualization. 跟踪存档旨在按顺序读取，因为在跟踪中较早出现的记录可能会影响在跟踪中较晚出现的记录的解释。跟踪系统提供了用于从跟踪归档中提取信息并将其转换为其他形式以进行可视化的工具。

 
### Timestamps  时间戳记 

Timestamps are represented as 64-bit ticks derived from a hardware counter. The trace initialization record describes the number of ticks per secondof real time. 时间戳表示为从硬件计数器派生的64位滴答声。跟踪初始化记录描述了每秒的实时滴答数。

By default, we assume that 1 tick equals 1 nanosecond.  默认情况下，我们假设1个滴答等于1纳秒。

 
### String References  字符串引用 

Strings are encoded as **String Refs** which are 16-bit values of the following form: 字符串编码为“字符串引用”，它们是以下形式的16位值：

 
- **Empty strings**: Value is zero.  -**空字符串**：值为零。
- **Indexed strings**: Most significant bit is zero.  The lower 15 bits denote an index in the **string table** which was previously assigned using a**String Record**. -**索引字符串**：最高有效位为零。低15位表示“字符串表”中的索引，该索引先前是使用“字符串记录”分配的。
- **Inline strings**: Most significant bit is one.  The lower 15 bits denote the length of the string in bytes.  The string's content appearsinline in another part of the record as specified by the record format. -**内联字符串**：最高有效位为1。低15位表示字符串的长度（以字节为单位）。字符串的内容按记录格式指定在记录的另一部分内联显示。

To make traces more compact, frequently referenced strings, such as event category and name constants, should be registered into the **string table**using **String Records** then referenced by index. 为了使跟踪更紧凑，应使用“字符串记录”将经常引用的字符串（例如事件类别和名称常量）注册到“字符串表”中，然后由索引引用。

There can be at most 32767 strings in the string table.  If this limit is reached, additional strings can be encoded by replacing existing entriesor by encoding strings inline. 字符串表中最多可以有32767个字符串。如果达到此限制，则可以通过替换现有条目或内联编码字符串来编码其他字符串。

String content itself is stored as a UTF-8 **Stream** without termination.  字符串内容本身存储为UTF-8流而不终止。

The theoretical maximum length of a string is 32767 bytes but in practice this will be further reduced by the space required to store the rest of the recordwhich contains it, so we set a conservative maximum string length limit of32000 bytes. 字符串的理论最大长度为32767字节，但实际上，存储包含该记录的其余记录所需的空间将进一步减少，因此我们将保守的最大字符串长度限制设置为32000字节。

 
### Thread References  线程引用 

Thread and process kernel object ids (koids) are encoded as **Thread Refs** which are 8-bit values of the following form: 线程和进程内核对象ID（koid）被编码为“ Thread Refs”，它们是以下形式的8位值：

 
- **Inline threads**: Value is zero.  The thread and process koid appears inline in another part of the record as specified by the record format. -**内联线程**：值为零。线程和进程主题在记录的另一部分按记录格式内联显示。
- **Indexed threads**: Value is non-zero.  The value denotes an index in the **thread table** which was previously assigned using a **Thread Record**. -**索引线程**：值不为零。该值表示“线程表”中的索引，该索引先前是使用“线程记录”分配的。

To make traces more compact, frequently referenced threads should be registered into the **thread table** using **Thread Records** then referenced by index. 为了使跟踪更紧凑，应使用“线程记录”将经常引用的线程注册到“线程表”中，然后由索引引用。

There can be at most 255 threads in the string table.  If this limit is reached, additional threads can be encoded by replacing existing entriesor by encoding threads inline. 字符串表中最多可以有255个线程。如果达到此限制，则可以通过替换现有条目或通过内联编码线程来编码其他线程。

 
### Userspace Object Information  用户空间对象信息 

Traces can include annotations about userspace objects (anything that can be referenced using a pointer-like value such as a C++ or Dart object) in theform of **Userspace Object Records**.  Trace providers typically generatesuch records when the object is created. 跟踪可以以“用户空间对象记录”的形式包含有关用户空间对象的注释（可以使用类似指针的值（例如C ++或Dart对象）引用的任何注释）。跟踪提供者通常在创建对象时生成此类记录。

Thereafter, any **Pointer Arguments** which refer to the same pointer will be associated with the referent's annotations. 此后，引用同一指针的任何“指针参数”都将与引用者的注释关联。

This makes it easy to associate human-readable labels and other information with objects which appear later in the trace. 这使得将人类可读的标签和其他信息与稍后显示在跟踪中的对象相关联变得容易。

 
### Kernel Object Information  内核对象信息 

Traces can include annotations about kernel objects (anything that can be referenced using a Zircon koid such as a process, channel, or event)form of **Kernel Object Records**.  Trace providers typically generate suchrecords when the object is created. 跟踪可以包含有关“内核对象记录” **形式的内核对象（可以使用Zircon koid引用的任何对象，例如进程，通道或事件）的注释。创建对象时，跟踪提供程序通常会生成此类记录。

Thereafter, any **Kernel Object Id Arguments** which refer to the same koid will be associated with the referent's annotations. 此后，任何引用相同koid的“内核对象ID参数”将与引用者的注释关联。

This makes it easy to associate human-readable labels and other information with objects which appear later in the trace. 这使得将人类可读的标签和其他信息与稍后显示在跟踪中的对象相关联变得容易。

In particular, this is how the tracing system associates names with process and thread koids. 特别是，这就是跟踪系统将名称与进程和线程孩子相关联的方式。

 
### Arguments  争论 

Arguments are typed key value pairs.  参数是键入的键值对。

Many record types allow up to 15 arguments to be appended to the record to provide additional information from the developer. 许多记录类型最多允许将15个参数附加到记录中，以提供来自开发人员的其他信息。

Arguments are size-prefixed like ordinary records so that unrecognized argument types can be skipped. 参数像普通记录一样具有大小前缀，因此可以跳过无法识别的参数类型。

See also [Argument Types](#argument-types).  另请参见[Argument Types]（参数类型）。

 
## Extending the Format  扩展格式 

The trace format can be extended in the following ways:  跟踪格式可以通过以下方式扩展：

 
- Defining new record types.  -定义新的记录类型。
- Storing new information in reserved fields of existing record types.  -在现有记录类型的保留字段中存储新信息。
- Appending new information to existing record types (the presence of this information can be detected by examining the record's size and payload). -将新信息追加到现有记录类型（可以通过检查记录的大小和有效负载来检测此信息的存在）。
- Defining new argument types.  -定义新的参数类型。

_To preserve compatibility as the trace format evolves, all extensions must be documented authoritatively in this file.  Currently there is no support forprivate extensions._ 为了在跟踪格式发展时保持兼容性，必须在该文件中权威性地记录所有扩展名。当前不支持私人扩展。

 
## Notation  符号 

In the record format descriptions which follow, each constituent atom is labeled in italics followed by a bullet-point description of its contents. 在下面的记录格式描述中，每个组成原子都用斜体标记，然后是其内容的项目符号点描述。

 
## Record Types  记录类型 

 
### Record Header  记录标题 

All records include this header which specifies the record's type and size together with 48 bits of data whose usage varies by record type. 所有记录都包括此标头，用于指定记录的类型和大小以及48位数据，这些数据的使用情况随记录类型而异。

 
##### Format  格式 

![drawing](record.png)  ！[绘图]（record.png）

_header word_  标题字

 
- `[0 .. 3]`: record type  -`[0 .. 3]`：记录类型
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 63]`: varies by record type (must be zero if unused)  -`[16 .. 63]`：因记录类型而异（如果未使用，则必须为零）

 
### Large Record Header  大记录标题 

Provides support for records larger than 32KB. Large records have a  提供对大于32KB的记录的支持。大记录有一个
32 bit size field rather than the normal 12 bits.  32位大小字段，而不是正常的12位。

![drawing](largerecord.png)  ！[绘图]（largerecord.png）

_header word_  标题字

 
- `[0 ..  3]`: record type (15)  -`[0 .. 3]`：记录类型（15）
- `[4 .. 35]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 35]`：记录大小（包括此字）为8字节的倍数
- `[36 .. 39]`: large record type  -`[36 .. 39]`：大记录类型
- `[40 .. 63]`: varies by large record type (must be zero if unused)  -`[40 .. 63]`：因大型记录类型而异（如果未使用，则必须为零）

 
### Metadata Record (record type = 0)  元数据记录（记录类型= 0） 

Provides metadata about trace data which follows.  提供有关跟踪数据的元数据。

This record type is reserved for use by the _trace manager_ when generating trace archives.  It must not be emitted by trace providers themselves.If the trace manager encounters a **Metadata Record** within a trace producedby a trace provider, it treats it as garbage and skips over it. 保留此记录类型，以供_trace manager_在生成跟踪归档时使用。它不能由跟踪提供程序自己发出。如果跟踪管理器在跟踪提供程序生成的跟踪中遇到“元数据记录”，则会将其视为垃圾并跳过。

There are several metadata record subtypes, each of which contain different information. 有几种元数据记录子类型，每种子类型包含不同的信息。

 
##### Format  格式 

![drawing](metadata.png)  ！[绘图]（metadata.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (0)  -`[0 .. 3]`：记录类型（0）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 19]`: metadata type  -`[16 .. 19]`：元数据类型
- `[20 .. 63]`: varies by metadata type (must be zero if unused)  -`[20 .. 63]`：因元数据类型而异（如果未使用，则必须为零）

 
#### Provider Info Metadata (metadata type = 1)  提供者信息元数据（元数据类型= 1） 

This metadata identifies a trace provider which has contributed information to the trace. 该元数据标识已向跟踪提供信息的跟踪提供者。

All data which follows until the next **Provider Section Metadata** or **Provider Info Metadata** is encountered must have been collected from thesame provider. 在遇到下一个“提供者部分元数据”或“提供者信息元数据”之前，所有随后的数据必须已从同一提供者处收集。

 
##### Format  格式 

![drawing](metadata1.png)  ！[绘图]（metadata1.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (0)  -`[0 .. 3]`：记录类型（0）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 19]`: metadata type (1)  -`[16 .. 19]`：元数据类型（1）
- `[20 .. 51]`: provider id (token used to identify the provider in the trace)  -`[20 .. 51]`：提供者ID（用于在跟踪中标识提供者的令牌）
- `[52 .. 59]`: name length in bytes  -`[52 .. 59]`：名称长度（以字节为单位）
- `[60 .. 63]`: reserved (must be zero)  -`[60 .. 63]`：保留（必须为零）

_provider name stream_  _提供商名称流_

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

 
#### Provider Section Metadata (metadata type = 2)  提供者部分元数据（元数据类型= 2） 

This metadata delimits sections of the trace which have been obtained from different providers. 此元数据定界了从不同提供程序获得的跟踪部分。

All data which follows until the next **Provider Section Metadata** or **Provider Info Metadata** is encountered is assumed to have been collectedfrom the same provider. 假定遇到下一个“提供者部分元数据”或“提供者信息元数据”之前的所有数据都是从同一提供者那里收集的。

When reading a trace consisting of an accumulation of traces from different trace providers, the reader must maintain state separately for each provider'straces (such as the initialization data, string table, thread table,userspace object table, and kernel object table) and switch contextswhenever it encounters a new **Provider Section Metadata** record. 当读取由来自不同跟踪提供程序的跟踪的累积组成的跟踪时，读取器必须分别维护每个提供程序的跟踪的状态（例如初始化数据，字符串表，线程表，用户空间对象表和内核对象表）并进行切换每当遇到新的“提供者部分元数据”记录时。

 
##### Format  格式 

![drawing](metadata2.png)  ！[绘图]（metadata2.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (0)  -`[0 .. 3]`：记录类型（0）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 19]`: metadata type (2)  -`[16 .. 19]`：元数据类型（2）
- `[20 .. 51]`: provider id (token used to identify the provider in the trace)  -`[20 .. 51]`：提供者ID（用于在跟踪中标识提供者的令牌）
- `[52 .. 63]`: reserved (must be zero)  -`[52 .. 63]`：保留（必须为零）

 
#### Provider Event Metadata (metadata type = 3)  提供者事件元数据（元数据类型= 3） 

This metadata provides running notification of events that the provider wants to report.This record may appear anywhere in the output, and does not delimit whatcame before it or what comes after it. 此元数据提供了提供者要报告的事件的运行通知。此记录可能出现在输出中的任何位置，并且不限制在它之前或之后的事件。

 
##### Format  格式 

![drawing](metadata3.png)  ！[绘图]（metadata3.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (0)  -`[0 .. 3]`：记录类型（0）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 19]`: metadata type (3)  -`[16 .. 19]`：元数据类型（3）
- `[20 .. 51]`: provider id (token used to identify the provider in the trace)  -`[20 .. 51]`：提供者ID（用于在跟踪中标识提供者的令牌）
- `[52 .. 55]`: the event id  -`[52 .. 55]`：事件ID
- `[56 .. 63]`: reserved (must be zero)  -`[56 .. 63]`：保留（必须为零）

 
##### Events  大事记 

The following events are defined.  定义了以下事件。

 
- `0`: a buffer filled up, records were likely dropped  -'0'：缓冲区已满，记录可能会丢失

 
#### Trace Info Metadata (metadata type = 4)  跟踪信息元数据（元数据类型= 4） 

This metadata provides information about the trace as a whole. This record is not associated with a particular provider. 此元数据提供有关整个跟踪的信息。该记录与特定的提供者无关。

 
##### Format  格式 

_header word_  标题字

 
- `[0 .. 3]`: record type (0)  -`[0 .. 3]`：记录类型（0）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 19]`: metadata type (4)  -`[16 .. 19]`：元数据类型（4）
- `[20 .. 23]`: trace info type  -`[20 .. 23]`：跟踪信息类型
- `[24 .. 63]`: varies by trace info type (must be zero if unused)  -`[24 .. 63]`：因跟踪信息类型而异（如果未使用，则必须为零）

 
#### Magic Number Record (trace info type = 0)  幻数记录（跟踪信息类型= 0） 

This record serves as an indicator that the binary data is in the Fuchsia tracing format. Generally it should appear at the start of a trace. It carriesno other information. The magic number 0x16547846 is the string "FxT"followed by a byte that was chosen at random. 该记录可以指示二进制数据为紫红色的跟踪格式。通常，它应该出现在跟踪的开头。它不包含其他信息。魔术数字0x16547846是字符串“ FxT”，其后是随机选择的字节。

To allow the first eight bytes of a trace to be treated together as a magic number without caring about the internal record structure, this record type is_not_ extensible. The record must not contain any words other than the headerword, and there are no reserved fields. As an eight byte number, the entirerecord has the value 0x0016547846040010. 为了使跟踪的前八个字节一起被视为幻数，而无需关心内部记录结构，此记录类型为is_not_可扩展。记录中不得包含标题词以外的任何词，并且没有保留字段。作为一个八字节数字，整个记录的值为0x0016547846040010。

Note that the byte order of that value, and all other words in the trace, depends on the endianness of the system that wrote the trace. For a littleendian system, the first eight bytes are 10 00 04 46 78 54 16 00. On a bigendian system, it will be the reverse: 00 16 54 78 46 04 00 10. 请注意，该值的字节顺序以及跟踪中的所有其他单词，取决于编写跟踪的系统的字节顺序。对于littleendian系统，前八个字节为10 00 04 46 78 54 1600。在bigendian系统上，则相反：00 16 54 78 46 04 00 10。

 
##### Format  格式 

_header word_  标题字

 
- `[0 .. 3]`: record type (0)  -`[0 .. 3]`：记录类型（0）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes (1)  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数（1）
- `[16 .. 19]`: metadata type (4)  -`[16 .. 19]`：元数据类型（4）
- `[20 .. 23]`: trace info type (0)  -`[20 .. 23]`：跟踪信息类型（0）
- `[24 .. 55]`: the magic number 0x16547846  -`[24 .. 55]`：魔术数字0x16547846
- `[56 .. 63]`: zero  -`[56 .. 63]`：零

 
### Initialization Record (record type = 1)  初始化记录（记录类型= 1） 

Provides parameters needed to interpret the records which follow.  In absence of this record, the reader may assume that 1 tick is 1 nanosecond. 提供解释后续记录所需的参数。在没有此记录的情况下，读者可以假定1个滴答声是1纳秒。

 
##### Format  格式 

![drawing](initialization.png)  ！[绘图]（initialization.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (1)  -`[0 .. 3]`：记录类型（1）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 63]`: reserved (must be zero)  -`[16 .. 63]`：保留（必须为零）

_tick multiplier word_  _tick乘数词_

 
- `[0 .. 63]`: number of ticks per second  -`[0 .. 63]`：每秒的滴答数

 
### String Record (record type = 2)  字符串记录（记录类型= 2） 

Registers a string in the string table, assigning it a string index in the range `0x0001` to `0x7fff`.  The registration replaces any prior registrationfor the given string index when interpreting the records which follow. 在字符串表中注册一个字符串，并为其分配一个字符串索引，范围为0x0001到0x7fff。在解释随后的记录时，该注册将替换给定字符串索引的任何先前注册。

String records which attempt to set a value for string index `0x0000` must be ignored since this value is reserved to represent the empty string. 尝试为字符串索引“ 0x0000”设置值的字符串记录必须被忽略，因为该值被保留以表示空字符串。

String records which contain empty strings must be tolerated but they're pointless since the empty string can simply be encoded as zero in a string ref. 必须容忍包含空字符串的字符串记录，但它们毫无意义，因为在字符串引用中可以将空字符串简单地编码为零。

 
##### Format  格式 

![drawing](string.png)  ！[绘图]（string.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (2)  -`[0 .. 3]`：记录类型（2）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 30]`: string index (range 0x0001 to 0x7fff)  -`[16 .. 30]`：字符串索引（范围0x0001至0x7fff）
- `[31]`: always zero (0)  -`[31]`：始终为零（0）
- `[32 .. 46]`: string length in bytes (range 0x0000 to 0x7fff)  -`[32 .. 46]`：字符串长度（以字节为单位）（范围0x0000至0x7fff）
- `[47]`: always zero (0)  -`[47]`：始终为零（0）
- `[48 .. 63]`: reserved (must be zero)  -`[48 .. 63]`：保留（必须为零）

_string value stream_  字符串值流

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

 
### Thread Record (record type = 3)  线程记录（记录类型= 3） 

Registers a process id and thread id pair in the thread table, assigning it a thread index in the range `0x01` to `0xff`.  The registration replaces anyprior registration for the given thread index when interpreting the recordswhich follow. 在线程表中注册一个进程ID和一个线程ID对，并为其分配一个在0x01到0xff范围内的线程索引。在解释随后的记录时，该注册将替换给定线程索引的任何先前注册。

Thread index `0x00` is reserved to denote the use of an inline thread id in a thread ref.  Thread records which attempt to set a value for this valuemust be ignored. 保留线程索引“ 0x00”以表示在线程引用中使用内联线程ID。试图为该值设置值的线程记录必须被忽略。

 
##### Format  格式 

![drawing](thread.png)  ！[绘图]（thread.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (3)  -`[0 .. 3]`：记录类型（3）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 23]`: thread index (never 0x00)  -`[16 .. 23]`：线程索引（从不0x00）
- `[24 .. 63]`: reserved (must be zero)  -`[24 .. 63]`：保留（必须为零）

_process id word_  _进程ID字_

 
- `[0 .. 63]`: process koid (kernel object id)  -`[0 .. 63]`：流程类（内核对象ID）

_thread id word_  _thread id word_

 
- `[0 .. 63]`: thread koid (kernel object id)  -`[0 .. 63]`：线程koid（内核对象ID）

 
### Event Record (record type = 4)  事件记录（记录类型= 4） 

Describes a timestamped event.  描述带有时间戳的事件。

This record consists of some basic information about the event including when and where it happened followed by event arguments and event subtypespecific data. 该记录包含有关事件的一些基本信息，包括事件发生的时间和地点以及事件参数和事件子类型特定的数据。

 
##### Format  格式 

![drawing](event.png)  ！[绘图]（event.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (4)  -`[0 .. 3]`：记录类型（4）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 19]`: event type  -`[16 .. 19]`：事件类型
- `[20 .. 23]`: number of arguments  -`[20 .. 23]`：参数数量
- `[24 .. 31]`: thread (thread ref)  -`[24 .. 31]`：线程（线程参考）
- `[32 .. 47]`: category (string ref)  -`[32 .. 47]`：类别（字符串ref）
- `[48 .. 63]`: name (string ref)  -`[48 .. 63]`：名称（字符串ref）

_timestamp word_  _时间戳词_

 
- `[0 .. 63]`: number of ticks  -`[0 .. 63]`：跳动数

_process id word_ (omitted unless thread ref denotes inline thread)  _process id word_（省略，除非线程ref表示嵌入式线程）

 
- `[0 .. 63]`: process koid (kernel object id)  -`[0 .. 63]`：流程类（内核对象ID）

_thread id word_ (omitted unless thread ref denotes inline thread)  _thread id word_（省略，除非线程ref表示嵌入式线程）

 
- `[0 .. 63]`: thread koid (kernel object id)  -`[0 .. 63]`：线程koid（内核对象ID）

_category stream_ (omitted unless string ref denotes inline string)  _category stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_name stream_ (omitted unless string ref denotes inline string)  _name stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_argument data_ (repeats for each argument)  _argument data_（每个参数重复）

 
- (see below)  - （见下文）

_event-type specific data_  _事件类型专用数据_

 
- (see below)  - （见下文）

 
#### Instant Event (event type = 0)  即时事件（事件类型= 0） 

Marks a moment in time on this thread.  These are equivalent to Zircon kernel probes. 在该线程上标记时间。这些等效于Zircon内核探针。

 
##### Format  格式 

![drawing](event0.png)  ！[绘图]（event0.png）

No event-type specific data required.  不需要特定于事件类型的数据。

 
#### Counter Event (event type = 1)  计数器事件（事件类型= 1） 

Records sample values of each argument as data in a time series associated with the counter's name and id.  The values may be presented graphically as astacked area chart. 将每个参数的样本值记录为与计数器名称和ID相关的时间序列中的数据。这些值可以图形方式显示为堆积面积图。

 
##### Format  格式 

![drawing](event1.png)  ！[绘图]（event1.png）

_counter word_  _反词_

 
- `[0 .. 63]`: counter id  -`[0 .. 63]`：计数器ID

 
#### Duration Begin Event (event type = 2)  持续时间开始事件（事件类型= 2） 

Marks the beginning of an operation on a particular thread.  Must be matched by a **Duration End Event**.  May be nested. 标记特定线程上的操作的开始。必须与“持续时间结束事件”相匹配。可能是嵌套的。

 
##### Format  格式 

![drawing](event23.png)  ！[绘图]（event23.png）

No event-type specific data required.  不需要特定于事件类型的数据。

 
#### Duration End Event (event type = 3)  持续时间结束事件（事件类型= 3） 

Marks the end of an operation on a particular thread.  标记特定线程上的操作结束。

 
##### Format  格式 

![drawing](event23.png)  ！[绘图]（event23.png）

No event-type specific data required.  不需要特定于事件类型的数据。

 
#### Duration Complete Event (event type = 4)  持续时间完成事件（事件类型= 4） 

Marks the beginning and end of an operation on a particular thread.  标记特定线程上的操作的开始和结束。

 
##### Format  格式 

![drawing](event4.png)  ！[绘图]（event4.png）

_end time word_  _结束时间字_

 
- `[0 .. 63]`: end time number of ticks  -`[0 .. 63]`：结束时间的滴答数

 
#### Async Begin Event (event type = 5)  异步开始事件（事件类型= 5） 

Marks the beginning of an operation which may span threads.  Must be matched by an **Async End Event** using the same async correlation id. 标记可能跨越线程的操作的开始。必须与使用相同异步相关ID的“异步结束事件”匹配。

 
##### Format  格式 

![drawing](event567.png)  ！[绘图]（event567.png）

_async correlation word_  _异步相关词_

 
- `[0 .. 63]`: async correlation id  -`[0 .. 63]`：异步相关ID

 
#### Async Instant Event (event type = 6)  异步即时事件（事件类型= 6） 

Marks a moment within an operation which may span threads.  Must appear between **Async Begin Event** and **Async End Event** using the same asynccorrelation id. 标记可能跨越线程的操作中的时刻。必须使用相同的asynccorrelation id在“异步开始事件”和“异步结束事件”之间出现。

 
##### Format  格式 

![drawing](event567.png)  ！[绘图]（event567.png）

_async correlation word_  _异步相关词_

 
- `[0 .. 63]`: async correlation id  -`[0 .. 63]`：异步相关ID

 
#### Async End Event (event type = 7)  异步结束事件（事件类型= 7） 

Marks the end of an operation which may span threads.  标记可能跨越线程的操作结束。

 
##### Format  格式 

![drawing](event567.png)  ！[绘图]（event567.png）

_async correlation word_  _异步相关词_

 
- `[0 .. 63]`: async correlation id  -`[0 .. 63]`：异步相关ID

 
#### Flow Begin Event (event type = 8)  流开始事件（事件类型= 8） 

Marks the beginning of an operation which results in a sequence of actions which may span multiple threads or abstraction layers.  Must be matched by a**Flow End Event** using the same flow correlation id.  This can be envisionedas an arrow between duration events. 标记操作的开始，该操作将导致一系列可能跨越多个线程或抽象层的操作。必须使用相同的流关联ID与“流结束事件”进行匹配。可以将其想象为持续时间事件之间的箭头。

The beginning of the flow is associated with the enclosing duration event for this thread; it begins where the enclosing **Duration Event** ends. 流的开始与该线程的封闭持续时间事件相关；它从封闭的“持续时间事件”结束的地方开始。

 
##### Format  格式 

![drawing](event8910.png)  ！[绘图]（event8910.png）

_flow correlation word_  _流相关词_

 
- `[0 .. 63]`: flow correlation id  -`[0 .. 63]`：流相关ID

 
#### Flow Step Event (event type = 9)  流步事件（事件类型= 9） 

Marks a point within a flow.  在流中标记一个点。

The step is associated with the enclosing duration event for this thread; the flow resumes where the enclosing duration event begins then is suspendedat the point where the enclosing **Duration Event** event ends. 该步骤与此线程的封闭持续时间事件相关；流程从封闭持续时间事件开始的地方继续，然后在封闭“持续时间事件”事件结束的地方暂停。

 
##### Format  格式 

![drawing](event8910.png)  ！[绘图]（event8910.png）

_flow correlation word_  _流相关词_

 
- `[0 .. 63]`: flow correlation id  -`[0 .. 63]`：流相关ID

 
#### Flow End Event (event type = 10)  流结束事件（事件类型= 10） 

Marks the end of a flow.  标记流程结束。

The end of the flow is associated with the enclosing duration event for this thread; the flow resumes where the enclosing **Duration Event** begins. 流的结尾与该线程的封闭持续时间事件相关；流程从封闭的“持续时间事件”开始的地方继续。

 
##### Format  格式 

![drawing](event8910.png)  ！[绘图]（event8910.png）

_flow correlation word_  _流相关词_

 
- `[0 .. 63]`: flow correlation id  -`[0 .. 63]`：流相关ID

 
### Blob Record (record type = 5)  Blob记录（记录类型= 5） 

Provides uninterpreted bulk data to be included in the trace.  This can be useful for embedding captured trace data in other formats. 提供未解释的批量数据以包括在跟踪中。这对于以其他格式嵌入捕获的跟踪数据很有用。

The blob name uniquely identifies separate blob data streams within the trace. By writing multiple blob records with the same name, additional chunks ofdata can be appended to a previously created blob. Blob名称唯一地标识跟踪中的单独Blob数据流。通过写入多个具有相同名称的Blob记录，可以将其他数据块附加到先前创建的Blob。

The blob type indicates the representation of the blob's content.  Blob类型表示Blob内容的表示形式。

 
##### Format  格式 

![drawing](blob.png)  ！[绘图]（blob.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (5)  -`[0 .. 3]`：记录类型（5）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 31]`: blob name (string ref)  -`[16 .. 31]`：Blob名称（字符串ref）
- `[32 .. 46]`: blob payload size in bytes (excluding padding)  -`[32 .. 46]`：Blob有效负载大小（以字节为单位）（不包括填充）
- `[47 .. 47]`: reserved (must be zero)  -`[47 .. 47]`：保留（必须为零）
- `[48 .. 55]`: blob type  -`[48 .. 55]`：Blob类型
- `[56 .. 63]`: reserved (must be zero)  -`[56 .. 63]`：保留（必须为零）

_blob name stream_ (omitted unless string ref denotes inline string)  _blob name stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_payload stream_ (variable size)  _有效负载流_（可变大小）

 
- binary data, padded with zeros to 8 byte alignment  -二进制数据，用零到8字节对齐填充

 
##### Blob Types  斑点类型 

The following blob types are defined:  定义了以下Blob类型：

 
- `TRACE_BLOB_TYPE_DATA` = `0x01`: Raw untyped data. The consumer is expected to know how to consume it, perhaps based on context. -`TRACE_BLOB_TYPE_DATA` =`0x01`：原始未类型化数据。可能希望消费者根据上下文知道如何消费它。
- `TRACE_BLOB_TYPE_LAST_BRANCH` = `0x02`: Last Branch Record of Intel Performance Monitor. The format is defined by the [Cpuperf Trace Provider](../cpuperf-provider.md). -`TRACE_BLOB_TYPE_LAST_BRANCH` =`0x02`：英特尔性能监视器的最后一个分支记录。该格式由[Cpuperf跟踪提供程序]（../ cpuperf-provider.md）定义。

 
### Userspace Object Record (record type = 6)  用户空间对象记录（记录类型= 6） 

Describes a userspace object, assigns it a label, and optionally associates key/value data with it as arguments.  Information about the object is addedto a per-process userspace object table. 描述用户空间对象，为其分配标签，并可以选择将键/值数据与其关联作为参数。有关对象的信息被添加到每个进程的用户空间对象表中。

When a trace consumer encounters an event with a **Pointer Argument** whose value matches an entry in the process's object table, it can cross-referencethe argument's pointer value with a prior **Userspace Object Record** to find adescription of the referent. 当跟踪使用者遇到带有“指针参数”的事件，该事件的值与流程的对象表中的条目匹配时，它可以将参数的指针值与先前的“用户空间对象记录”进行交叉引用，以查找引用对象的说明。 。

 
##### Format  格式 

![drawing](userspace.png)  ！[绘图]（userspace.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (6)  -`[0 .. 3]`：记录类型（6）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 23]`: process (thread ref)  -`[16 .. 23]`：进程（线程参考）
- `[24 .. 39]`: name (string ref)  -`[24 .. 39]`：名称（字符串ref）
- `[40 .. 43]`: number of arguments  -`[40 .. 43]`：参数数量
- `[44 .. 63]`: reserved (must be zero)  -`[44 .. 63]`：保留（必须为零）

_pointer word_  _指针字_

 
- `[0 .. 63]`: pointer value  -`[0 .. 63]`：指针值

_process id word_ (omitted unless thread ref denotes inline thread)  _process id word_（省略，除非线程ref表示嵌入式线程）

 
- `[0 .. 63]`: process koid (kernel object id)  -`[0 .. 63]`：流程类（内核对象ID）

_name stream_ (omitted unless string ref denotes inline string)  _name stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_argument data_ (repeats for each argument)  _argument data_（每个参数重复）

 
- (see below)  - （见下文）

 
### Kernel Object Record (record type = 7)  内核对象记录（记录类型= 7） 

Describes a kernel object, assigns it a label, and optionally associates key/value data with it as arguments.  Information about the object is addedto a global kernel object table. 描述内核对象，为其分配标签，并可以选择将键/值数据与其作为参数关联。有关对象的信息将添加到全局内核对象表中。

When a trace consumer encounters an event with a **Koid Argument** whose value matches an entry in the kernel object table, it cancross-reference the argument's koid value with a prior **Kernel Object Record**to find a description of the referent. 当跟踪使用者遇到带有“ Koid Argument”的事件，该事件的值与内核对象表中的条目相匹配时，它可以将引用的koid值与先前的“ Kernel Object Record”交叉引用，以找到对指称对象。

 
##### Format  格式 

![drawing](kernel.png)  ！[drawing]（kernel.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (7)  -`[0 .. 3]`：记录类型（7）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 23]`: kernel object type (one of the ZX_OBJ_TYPE_XXX constants from <zircon/syscalls/object.h>)  -`[16 .. 23]`：内核对象类型（<zircon / syscalls / object.h>中的ZX_OBJ_TYPE_XXX常量之一）
- `[24 .. 39]`: name (string ref)  -`[24 .. 39]`：名称（字符串ref）
- `[40 .. 43]`: number of arguments  -`[40 .. 43]`：参数数量
- `[44 .. 63]`: reserved (must be zero)  -`[44 .. 63]`：保留（必须为零）

_kernel object id word_  _内核对象ID word_

 
- `[0 .. 63]`: koid (kernel object id)  -`[0 .. 63]`：koid（内核对象ID）

_name stream_ (omitted unless string ref denotes inline string)  _name stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_argument data_ (repeats for each argument)  _argument data_（每个参数重复）

 
- (see below)  - （见下文）

 
##### Argument Conventions  参数约定 

By convention, the trace writer should include the following named arguments when writing kernel object records about objects of particular types.  Thishelps trace consumers correlate relationships among kernel objects. 按照惯例，在编写有关特定类型对象的内核对象记录时，跟踪编写器应包括以下命名参数。这有助于跟踪使用者关联内核对象之间的关系。

_This information may not always be available._  _此信息可能并不总是可用。

 
- `"process"`: for `ZX_OBJ_TYPE_THREAD` objects, specifies the koid of the process which contains the thread -`“ process”`：对于`ZX_OBJ_TYPE_THREAD`对象，指定包含线程的进程的koid

 
### Context Switch Record (record type = 8)  上下文切换记录（记录类型= 8） 

Describes a context switch during which a CPU handed off control from an outgoing thread to an incoming thread which resumes execution. 描述上下文切换，在此期间，CPU将控制权从输出线程移交给继续执行的输入线程。

The record specifies the new state of the outgoing thread following the context switch.  By definition, the new state of the incoming thread is"running" since it was just resumed. 该记录指定了上下文切换之后传出线程的新状态。根据定义，进入线程的新状态是“正在运行”，因为它刚刚恢复。

 
##### Format  格式 

![drawing](context.png)  ！[绘图]（context.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (8)  -`[0 .. 3]`：记录类型（8）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 23]`: cpu number  -`[16 .. 23]`：CPU编号
- `[24 .. 27]`: outgoing thread state (any of the values below except "running")  -`[24 .. 27]`：传出线程状态（以下任何值，“运行中”除外）
- `[28 .. 35]`: outgoing thread (thread ref)  -`[28 .. 35]`：传出线程（线程参考）
- `[36 .. 43]`: incoming thread (thread ref)  -`[36 .. 43]`：传入线程（线程参考）
- `[44 .. 51]`: outgoing thread priority  -`[44 .. 51]`：输出线程优先级
- `[52 .. 59]`: incoming thread priority  -`[52 .. 59]`：传入线程优先级
- `[60 .. 63]`: reserved  -`[60 .. 63]`：保留

_timestamp word_  _时间戳词_

 
- `[0 .. 63]`: number of ticks  -`[0 .. 63]`：跳动数

_outgoing process id word_ (omitted unless outgoing thread ref denotes inline thread)  _outgoing process id word_（省略，除非传出线程ref表示嵌入式线程）

 
- `[0 .. 63]`: process koid (kernel object id)  -`[0 .. 63]`：流程类（内核对象ID）

_outgoing thread id word_ (omitted unless outgoing thread ref denotes inline thread)  _outgoing thread id word_（省略，除非传出线程ref表示嵌入式线程）

 
- `[0 .. 63]`: thread koid (kernel object id)  -`[0 .. 63]`：线程koid（内核对象ID）

_incoming process id word_ (omitted unless incoming thread ref denotes inline thread)  _incoming process id word_（除非传入线程ref表示嵌入式线程，否则省略）

 
- `[0 .. 63]`: process koid (kernel object id)  -`[0 .. 63]`：流程类（内核对象ID）

_incoming thread id word_ (omitted unless incoming thread ref denotes inline thread)  _incoming thread id word_（省略，除非传入线程ref表示嵌入式线程）

 
- `[0 .. 63]`: thread koid (kernel object id)  -`[0 .. 63]`：线程koid（内核对象ID）

 
##### Thread States  线程状态 

The following thread states are defined:  定义了以下线程状态：

 
- `0`: new  -`0`：新
- `1`: running  -`1`：正在运行
- `2`: suspended  -`2`：已暂停
- `3`: blocked  -3：已封锁
- `4`: dying  -`4`：快死了
- `5`: dead  -`5`：已死

These values align with the `ZX_THREAD_STATE_XXX` constants from <zircon/syscalls/object.h>.  这些值与<zircon / syscalls / object.h>中的`ZX_THREAD_STATE_XXX`常量对齐。

 
### Log Record (record type = 9)  日志记录（记录类型= 9） 

Describes a message written to the log at a particular moment in time.  描述在特定时间写入日志的消息。

 
##### Format  格式 

![drawing](log.png)  ！[drawing]（logo.png）

_header word_  标题字

 
- `[0 .. 3]`: record type (9)  -`[0 .. 3]`：记录类型（9）
- `[4 .. 15]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：记录大小（包括此字）为8字节的倍数
- `[16 .. 30]`: log message length in bytes (range 0x0000 to 0x7fff)  -`[16 .. 30]`：以字节为单位的日志消息长度（范围0x0000至0x7fff）
- `[31]`: always zero (0)  -`[31]`：始终为零（0）
- `[32 .. 39]`: thread (thread ref)  -`[32 .. 39]`：线程（线程参考）
- `[40 .. 63]`: reserved (must be zero)  -`[40 .. 63]`：保留（必须为零）

_timestamp word_  _时间戳词_

 
- `[0 .. 63]`: number of ticks  -`[0 .. 63]`：跳动数

_process id word_ (omitted unless thread ref denotes inline thread)  _process id word_（省略，除非线程ref表示嵌入式线程）

 
- `[0 .. 63]`: process koid (kernel object id)  -`[0 .. 63]`：流程类（内核对象ID）

_thread id word_ (omitted unless thread ref denotes inline thread)  _thread id word_（省略，除非线程ref表示嵌入式线程）

 
- `[0 .. 63]`: thread koid (kernel object id)  -`[0 .. 63]`：线程koid（内核对象ID）

_log message stream_  _日志消息流_

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

 
### Large Blob Record (record type = 15, large type = 0)  大Blob记录（记录类型= 15，大类型= 0） 

Provides large binary blob data to be embedded within a trace. It uses the large record header. 提供大的二进制blob数据以嵌入到跟踪中。它使用大记录头。

The large blob record supports a number of different formats. These formats can be used for varying the types of blob data and metadataincluded in the record. 大的Blob记录支持多种不同的格式。这些格式可用于更改记录中包含的Blob数据和元数据的类型。

 
##### Format  格式 

![drawing](largeblob.png)  ！[绘图]（large blob.png）

_header word_  标题字

 
- `[0 ..  3]`: record type (15)  -`[0 .. 3]`：记录类型（15）
- `[4 .. 35]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 35]`：记录大小（包括此字）为8字节的倍数
- `[36 .. 39]`: large record type (0)  -`[36 .. 39]`：大记录类型（0）
- `[40 .. 43]`: blob format type  -`[40 .. 43]`：Blob格式类型
- `[44 .. 63]`: reserved, must be zero  -`[44 .. 63]`：保留，必须为零

 
#### In Band Large Blob Record With Metadata (blob format = 0)  带元数据的带内大Blob记录（blob格式= 0） 

This type contains the blob data and metadata within the record itself. The metadata includes a timestamp, thread/processinformation, and arguments, in addition to a category and name. 此类型包含记录本身内的Blob数据和元数据。元数据除了类别和名称之外，还包括时间戳，线程/进程信息和参数。

The name should be sufficient to identify the type of data contained within the blob. 该名称应足以识别blob中包含的数据类型。

 
##### Format  格式 

![drawing](largeblob0.png)  ！[绘图]（largeblob0.png）

_header word_  标题字

 
- `[0 ..  3]`: record type (15)  -`[0 .. 3]`：记录类型（15）
- `[4 .. 35]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 35]`：记录大小（包括此字）为8字节的倍数
- `[36 .. 39]`: large record type (0)  -`[36 .. 39]`：大记录类型（0）
- `[40 .. 43]`: blob format type (0)  -`[40 .. 43]`：Blob格式类型（0）
- `[44 .. 63]`: reserved, must be zero  -`[44 .. 63]`：保留，必须为零

_format header word_  格式标题字

 
- `[0 .. 15]`: category (string ref)  -`[0 .. 15]`：类别（字符串ref）
- `[16 .. 31]`: name (string ref)  -`[16 .. 31]`：名称（字符串ref）
- `[32 .. 35]`: number of arguments  -`[32 .. 35]`：参数数量
- `[36 .. 43]`: thread (thread ref)  -`[36 .. 43]`：线程（线程参考）
- `[44 .. 63]`: reserved, must be zero  -`[44 .. 63]`：保留，必须为零

_category stream_ (omitted unless string ref denotes inline string)  _category stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_name stream_ (omitted unless string ref denotes inline string)  _name stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_timestamp word_  _时间戳词_

 
- `[0 .. 63]`: number of ticks  -`[0 .. 63]`：跳动数

_process id word_ (omitted unless thread ref denotes inline thread)  _process id word_（省略，除非线程ref表示嵌入式线程）

 
- `[0 .. 63]`: process koid (kernel object id)  -`[0 .. 63]`：流程类（内核对象ID）

_thread id word_ (omitted unless thread ref denotes inline thread)  _thread id word_（省略，除非线程ref表示嵌入式线程）

 
- `[0 .. 63]`: thread koid (kernel object id)  -`[0 .. 63]`：线程koid（内核对象ID）

_argument data_ (repeats for each argument)  _argument data_（每个参数重复）

 
- (see below)  - （见下文）

_blob size word_  _blob size word_

 
- `[0 .. 63]`: blob payload size in bytes (excluding padding)  -`[0 .. 63]`：Blob有效载荷大小，以字节为单位（不包括填充）

_payload stream_ (variable size)  _有效负载流_（可变大小）

 
- binary data, padded with zeros to 8 byte alignment  -二进制数据，用零到8字节对齐填充

 
#### In Band Large Blob Record No Metadata (blob format = 1)  带内大Blob记录无元数据（blob格式= 1） 

This type contains the blob data within the record itself, but does not include metadata. The record only containsa category and name. 此类型包含记录本身内的Blob数据，但不包含元数据。该记录仅包含类别和名称。

The name should be sufficient to identify the type of data contained within the blob. 该名称应足以识别blob中包含的数据类型。

 
##### Format  格式 

![drawing](largeblob1.png)  ！[绘图]（largeblob1.png）

_header word_  标题字

 
- `[0 ..  3]`: record type (15)  -`[0 .. 3]`：记录类型（15）
- `[4 .. 35]`: record size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 35]`：记录大小（包括此字）为8字节的倍数
- `[36 .. 39]`: large record type (0)  -`[36 .. 39]`：大记录类型（0）
- `[40 .. 43]`: blob format type (1)  -`[40 .. 43]`：Blob格式类型（1）
- `[44 .. 63]`: reserved, must be zero  -`[44 .. 63]`：保留，必须为零

_format header word_  格式标题字

 
- `[0 .. 15]`: category (string ref)  -`[0 .. 15]`：类别（字符串ref）
- `[16 .. 31]`: name (string ref)  -`[16 .. 31]`：名称（字符串ref）
- `[32 .. 63]`: reserved, must be zero  -`[32 .. 63]`：保留，必须为零

_category stream_ (omitted unless string ref denotes inline string)  _category stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_name stream_ (omitted unless string ref denotes inline string)  _name stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_blob size word_  _blob size word_

 
- `[0 .. 63]`: blob payload size in bytes (excluding padding)  -`[0 .. 63]`：Blob有效载荷大小，以字节为单位（不包括填充）

_payload stream_ (variable size)  _有效负载流_（可变大小）

 
- binary data, padded with zeros to 8 byte alignment  -二进制数据，用零到8字节对齐填充

 

 
## Argument Types  参数类型 

Arguments associate typed key/value data records.  They are used together with **Event Record** and **Userspace Object Record** and**Kernel Object Record**. 参数关联键入的键/值数据记录。它们与“事件记录”和“用户空间对象记录”以及“内核对象记录”一起使用。

Each argument consists of a one word header followed by a variable number words of payload.  In many cases, the header itself is sufficient to encodethe content of the argument. 每个自变量包含一个单词头，后跟可变数量的有效载荷单词。在许多情况下，标头本身足以对自变量的内容进行编码。

 
### Argument Header  参数标题 

All arguments include this header which specifies the argument's type, name, and size together with 32 bits of data whose usage varies byargument type. 所有参数都包含此标头，用于指定参数的类型，名称和大小以及32位数据，这些数据的用法因参数类型而异。

 
##### Format  格式 

![drawing](argument.png)  ！[绘图]（argument.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type  -`[0 .. 3]`：参数类型
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 63]`: varies (must be zero if not used)  -`[32 .. 63]`：变化（如果不使用，则必须为零）

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

 
### Null Argument (argument type = 0)  空参数（参数类型= 0） 

Represents an argument which appears in name only without a value.  表示仅在名称中显示而没有值的参数。

 
##### Format  格式 

![drawing](argument0.png)  ！[绘图]（argument0.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type (0)  -`[0 .. 3]`：参数类型（0）
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 63]`: reserved (must be zero)  -`[32 .. 63]`：保留（必须为零）

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

 
### 32-bit Signed Integer Argument (argument type = 1)  32位带符号整数参数（参数类型= 1） 

Represents a 32-bit signed integer.  表示一个32位有符号整数。

 
##### Format  格式 

![drawing](argument1.png)  ！[绘图]（argument1.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type (1)  -`[0 .. 3]`：参数类型（1）
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 63]`: 32-bit signed integer  -`[32 .. 63]`：32位有符号整数

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

 
### 32-bit Unsigned Integer Argument (argument type = 2)  32位无符号整数参数（参数类型= 2） 

Represents a 32-bit unsigned integer.  表示一个32位无符号整数。

 
##### Format  格式 

![drawing](argument2.png)  ！[绘图]（argument2.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type (2)  -`[0 .. 3]`：参数类型（2）
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 63]`: 32-bit unsigned integer  -`[32 .. 63]`：32位无符号整数

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

 
### 64-bit Signed Integer Argument (argument type = 3)  64位带符号整数参数（参数类型= 3） 

Represents a 64-bit signed integer.  If a value will fit in 32-bits, prefer using the **32-bit Signed Integer Argument** type instead. 表示一个64位有符号整数。如果值适合32位，请改用** 32位带符号整数参数**类型。

 
##### Format  格式 

![drawing](argument3.png)  ！[绘图]（argument3.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type (3)  -`[0 .. 3]`：参数类型（3）
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 63]`: reserved (must be zero)  -`[32 .. 63]`：保留（必须为零）

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_argument value word_  _参数值word_

 
- `[0 .. 63]`: 64-bit signed integer  -`[0 .. 63]`：64位有符号整数

 
### 64-bit Unsigned Integer Argument (argument type = 4)  64位无符号整数参数（参数类型= 4） 

Represents a 64-bit unsigned integer.  If a value will fit in 32-bits, prefer using the **32-bit Unsigned Integer Argument** type instead. 表示一个64位无符号整数。如果值适合32位，请改用** 32位Unsigned Integer Argument **类型。

 
##### Format  格式 

![drawing](argument4.png)  ！[绘图]（argument4.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type (4)  -`[0 .. 3]`：参数类型（4）
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 63]`: reserved (must be zero)  -`[32 .. 63]`：保留（必须为零）

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_argument value word_  _参数值word_

 
- `[0 .. 63]`: 64-bit unsigned integer  -`[0 .. 63]`：64位无符号整数

 
### Double-precision Floating Point Argument (argument type = 5)  双精度浮点参数（参数类型= 5） 

Represents a double-precision floating point number.  表示双精度浮点数。

 
##### Format  格式 

![drawing](argument5.png)  ！[绘图]（argument5.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type (5)  -`[0 .. 3]`：参数类型（5）
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 63]`: reserved (must be zero)  -`[32 .. 63]`：保留（必须为零）

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_argument value word_  _参数值word_

 
- `[0 .. 63]`: double-precision floating point number  -`[0 .. 63]`：双精度浮点数

 
### String Argument (argument type = 6)  字符串参数（参数类型= 6） 

Represents a string value.  表示一个字符串值。

 
##### Format  格式 

![drawing](argument6.png)  ！[绘图]（argument6.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type (6)  -`[0 .. 3]`：参数类型（6）
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 47]`: argument value (string ref)  -`[32 .. 47]`：参数值（字符串ref）
- `[48 .. 63]`: reserved (must be zero)  -`[48 .. 63]`：保留（必须为零）

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_argument value stream_ (omitted unless string ref denotes inline string)  _参数值stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

 
### Pointer Argument (argument type = 7)  指针参数（参数类型= 7） 

Represents a pointer value.  Additional information about the referent can be provided by a **Userspace Object Record** associated with the same pointer. 表示一个指针值。可以通过与同一指针关联的“用户空间对象记录”来提供有关引用对象的其他信息。

 
##### Format  格式 

![drawing](argument7.png)  ！[绘图]（argument7.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type (7)  -`[0 .. 3]`：参数类型（7）
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 63]`: reserved (must be zero)  -`[32 .. 63]`：保留（必须为零）

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_argument value word_  _参数值word_

 
- `[0 .. 63]`: the pointer value  -`[0 .. 63]`：指针值

 
### Kernel Object Id Argument (argument type = 8)  内核对象ID参数（参数类型= 8） 

Represents a koid (kernel object id).  Additional information about the referent can be provided by a **Kernel Object Record** associated with thesame koid. 表示一个koid（内核对象ID）。可以通过与相同的koid相关联的“内核对象记录”来提供有关引用对象的其他信息。

 
##### Format  格式 

![drawing](argument8.png)  ！[绘图]（argument8.png）

_argument header word_  _参数标题词

 
- `[0 .. 3]`: argument type (8)  -`[0 .. 3]`：参数类型（8）
- `[4 .. 15]`: argument size (inclusive of this word) as a multiple of 8 bytes  -`[4 .. 15]`：参数大小（包括此字）为8字节的倍数
- `[16 .. 31]`: argument name (string ref)  -`[16 .. 31]`：参数名称（字符串ref）
- `[32 .. 63]`: reserved (must be zero)  -`[32 .. 63]`：保留（必须为零）

_argument name stream_ (omitted unless string ref denotes inline string)  _参数名称stream_（除非字符串ref表示内联字符串，否则省略）

 
- UTF-8 string, padded with zeros to 8 byte alignment  -UTF-8字符串，用零填充到8字节对齐

_argument value word_  _参数值word_

 
- `[0 .. 63]`: the koid (kernel object id)  -`[0 .. 63]`：类（内核对象ID）

<!-- xrefs -->  <！-外部参照->

<!-- drawings are sourced from https://docs.google.com/document/d/19nQHHSc-TdZ1BPovkrUd5Uk5l5T3YuxTNuVl9zv0whU/edit -->  <！-图纸来自https://docs.google.com/document/d/19nQHHSc-TdZ1BPovkrUd5Uk5l5T3YuxTNuVl9zv0whU/edit->

