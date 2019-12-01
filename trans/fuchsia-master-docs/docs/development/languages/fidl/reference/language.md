 
# Language Specification  语言规格 

This document is a specification of the Fuchsia Interface Definition Language (**FIDL**) syntax. 本文档是Fuchsia接口定义语言（** FIDL **）语法的规范。

For more information about FIDL's overall purpose, goals, and requirements, see [Overview](../README.md). 有关FIDL的总体目的，目标和要求的更多信息，请参见[概述]（../ README.md）。

Also, see a modified [EBNF description of the FIDL grammar](grammar.md).  另外，请参阅修改后的[FIDL语法的EBNF说明]（grammar.md）。

[TOC]  [目录]

 
# Syntax  句法 

FIDL provides a syntax for declaring named bits, constants, enums, structs, tables, unions, xunions, and protocols.These declarations are collected into libraries for distribution. FIDL提供了一种语法，用于声明命名的位，常量，枚举，结构，表，联合，Xunion和协议，这些声明被收集到库中以进行分发。

FIDL declarations are stored in plain text UTF-8 files. Each file consists of a sequence of semicolon-delimited declarations. The order of declarations within aFIDL file, or among FIDL files within a library, is irrelevant. FIDL does notrequire (or support) forward declarations of any kind. FIDL声明存储在纯文本UTF-8文件中。每个文件都包含一系列以分号分隔的声明。 FIDL文件中或库中FIDL文件之间的声明顺序无关紧要。 FIDL不需要（或支持）任何形式的前向声明。

 
## Tokens  代币 

 
### Comments  评论 

FIDL comments start with two (`//`) or three (`///`) forward slashes, continue to the end of the line, and can contain UTF-8 content (which is, of course, ignored).The three-forward-slash variant is a "documentation comment", and causes the commenttext to be emitted into the generated code (as a comment, escaped correctlyfor the target language). FIDL注释以两个（`//`）或三个（`///`）正斜杠开头，一直到行尾，并且可以包含UTF-8内容（当然可以忽略）。三个-forward-slash变体是“文档注释”，使注释文本发送到生成的代码中（作为注释，对于目标语言正确地转义了）。

```fidl
// this is a comment
/// and this one is too, but it also ends up in the generated code
struct Foo { // plain comment
    int32 f; // as is this one
}; // and this is the last one!
```
 

Note that documentation comments can also be provided via the [`[Doc]` attribute](attributes.md#Doc). 注意，文档注释也可以通过[`[Doc]`属性]（attributes.mdDoc）提供。

 
### Keywords  关键词 

The following are keywords in FIDL.  以下是FIDL中的关键字。

```
as, bits, compose, const, enum, library,
protocol, struct, table, union, using, xunion.
```
 

 
### Identifiers  身份标识 

FIDL identifiers must match the regex `[a-zA-Z]([a-zA-Z0-9_]*[a-zA-Z0-9])?`.  FIDL标识符必须与正则表达式“ [a-zA-Z]（[a-zA-Z0-9 _] * [a-zA-Z0-9]）”匹配。

In words: identifiers must start with a letter, can contain letters, numbers, and underscores, but cannot end with an underscore. 换句话说：标识符必须以字母开头，可以包含字母，数字和下划线，但不能以下划线结尾。

Identifiers are case-sensitive.  标识符区分大小写。

```fidl
// a library named "foo"
library foo;

// a struct named "Foo"
struct Foo { };

// a struct named "struct"
struct struct { };
```
 

Note: While using keywords as identifiers is supported, it can lead to confusion, and should the be considered on a case-by-case basis.See the `Names` section of the[Style Rubric](/docs/development/languages/fidl/style.md#Names) 注意：虽然支持将关键字用作标识符，但会导致混淆，应视具体情况进行考虑。请参见[样式专栏]（/ docs / development / languages / fidl / style.mdNames）

 
### Qualified Identifiers  合格标识符 

FIDL always looks for unqualified symbols within the scope of the current library. To reference symbols in other libraries, they must be qualified byprefixing the identifier with the library name or alias. FIDL始终在当前库的范围内查找不合格的符号。要引用其他库中的符号，必须通过在标识符前面加上库名或别名来限定它们的资格。

**objects.fidl:**  ** objects.fidl：**

```fidl
library objects;
using textures as tex;

protocol Frob {
    // "Thing" refers to "Thing" in the "objects" library
    // "tex.Color" refers to "Color" in the "textures" library
    Paint(Thing thing, tex.Color color);
};

struct Thing {
    string name;
};
```
 

**textures.fidl:**  ** textures.fidl：**

```fidl
library textures;

struct Color {
    uint32 rgba;
};
```
 

 
### Literals  文字 

FIDL supports integer, floating point, boolean, string, and enumeration literals, using a simplified syntax familiar to C programmers (see below for examples). FIDL使用C程序员熟悉的简化语法支持整数，浮点数，布尔值，字符串和枚举常量（请参见下面的示例）。

 
### Constants  常数 

FIDL supports the following constant types: bits, booleans, signed and unsigned integers, floating point values, strings, and enumerations.The syntax is similar to C: FIDL支持以下常量类型：位，布尔值，有符号和无符号整数，浮点值，字符串和枚举。语法类似于C：

```fidl
const bool ENABLED_FLAG = true;
const int8 OFFSET = -33;
const uint16 ANSWER = 42;
const uint16 ANSWER_IN_BINARY = 0b101010;
const uint32 POPULATION_USA_2018 = 330000000;
const uint64 DIAMOND = 0x183c7effff7e3c18;
const uint64 FUCHSIA = 4054509061583223046;
const string USERNAME = "squeenze";
const float32 MIN_TEMP = -273.15;
const float64 CONVERSION_FACTOR = 1.41421358;
const Beverage MY_DRINK = WATER;
```
 

These declarations introduce a name within their scope. The constant's type must be either a primitive or an enum. 这些声明在其范围内引入了名称。常量的类型必须是原始或枚举。

Constant expressions are either literals or the names of other constant expressions. 常量表达式可以是文字，也可以是其他常量表达式的名称。

> For greater clarity, there is no expression processing in FIDL; that is, > you *cannot* declare a constant as having the value `6 + 5`, for> example. >为了更加清晰，FIDL中没有表达式处理；也就是说，例如，您*不能*将常量声明为值“ 6 + 5”。

 
### Default Initialization  默认初始化 

Primitive structure members may have initialization values specified in the declaration.For example: 基本结构成员可以在声明中指定初始化值，例如：

```fidl
struct Color {
     uint32 background_rgb = 0xFF77FF; // fuchsia is the default background
     uint32 foreground_rgb; // there is no default foreground color
};
```
 

If the programmer does not supply a background color, the default value of `0xFF77FF` will be used. 如果程序员不提供背景色，则将使用默认值0xFF77FF。

However, if the program does not supply a foreground color, there is no default.The foreground color must be supplied; otherwise it's a logic error onthe programmer's part. 但是，如果程序不提供前景色，则没有默认值。否则，这是程序员的逻辑错误。

There is a subtlety about the semantics and what defaults mean:  关于语义及其默认含义有一个微妙之处：

 
* If the target language can support defaults (Dart, C++)  *如果目标语言可以支持默认值（Dart，C ++）
    * then it MUST support defaults  *那么它必须支持默认值
* If the target language cannot support defaults (C, Rust, Go)  *如果目标语言不支持默认语言（C，Rust，Go）
    * then it MAY provide support that programmers can optionally invoke (e.g., a macro in C). *然后它可以提供程序员可以选择调用的支持（例如，C语言中的宏）。

 
### Declaration Separator  声明分隔符 

FIDL uses the semi-colon **';'** to separate adjacent declarations within the file, much like C. FIDL使用分号**';'**分隔文件中的相邻声明，就像C一样。

 
## Libraries  图书馆 

Libraries are named containers of FIDL declarations.  库被命名为FIDL声明的容器。

Each library has a name consisting of a single identifier (e.g., "objects"), or multiple identifiers separated by dots (e.g., "fuchsia.composition").Library names are used in [Qualified Identifiers](#qualified-identifiers). 每个库的名称均由单个标识符（例如“对象”）或由点分隔的多个标识符（例如“ fuchsia.composition”）组成。库名称用于[合格标识符]（qualified-identifiers）中。

```fidl
// library identifier separated by dots
library fuchsia.composition;

// "using" to import library "fuchsia.buffers"
using fuchsia.buffers;

// "using" to import library "fuchsia.geometry" and create a shortform called "geo"
using fuchsia.geometry as geo;

```
 

Libraries may declare that they use other libraries with a "using" declaration. This allows the library to refer to symbols defined in other libraries upon whichthey depend. Symbols which are imported this way may be accessed by: 库可以通过“使用”声明来声明它们使用其他库。这允许库引用它们所依赖的其他库中定义的符号。可以通过以下方式访问以这种方式导入的符号：

 
*   qualifying them with the fully qualified library name (as in _"fuchsia.geometry.Rect"_),  *使用完全限定的库名称对其进行限定（例如_“ fuchsia.geometry.Rect” _），
*   specifying just the library name (as in _"geometry.Rect"_), or,  *仅指定库名称（例如_“ geometry.Rect” _），或者
*   using a library alias (as in _"geo.Rect"_).  *使用库别名（如_“ geo.Rect” _）。

In the source tree, each library consists of a directory with some number of **.fidl** files. The name of the directory is irrelevant to the FIDL compilerbut by convention it should resemble the library name itself. A directory shouldnot contain FIDL files for more than one library. 在源代码树中，每个库都由一个目录以及一些**。fidl **文件组成。目录的名称与FIDL编译器无关，但按照约定，它应类似于库名称本身。一个目录不应包含多个库的FIDL文件。

The scope of "library" and "using" declarations is limited to a single file. Each individual file within a FIDL library must restate the "library"declaration together with any "using" declarations needed by that file. “库”和“使用”声明的范围仅限于单个文件。 FIDL库中的每个文件都必须重新声明“库”声明以及该文件所需的任何“使用”声明。

The library's name may be used by certain language bindings to provide scoping for symbols emitted by the code generator. 某些语言绑定可以使用库的名称来为代码生成器发出的符号提供作用域。

For example, the C++ bindings generator places declarations for the FIDL library "fuchsia.ui" within the C++ namespace"fuchsia::ui". Similarly, for languages such as Dart and Rust whichhave their own module system, each FIDL library is compiled as amodule for that language. 例如，C ++绑定生成器将FIDL库“ fuchsia.ui”的声明放置在C ++名称空间“ fuchsia :: ui”内。同样，对于Dart和Rust等具有自己的模块系统的语言，每个FIDL库都被编译为该语言的模块。

 
## Types and Type Declarations  类型和类型声明 

 
### Primitives  原语 

 
*   Simple value types.  *简单的值类型。
*   Not nullable.  *不可为空。

The following primitive types are supported:  支持以下原始类型：

 
*    Boolean                 **`bool`**  *布尔值**``布尔''**
*    Signed integer          **`int8 int16 int32 int64`**  *有符号整数**`int8 int16 int32 int64` **
*    Unsigned integer        **`uint8 uint16 uint32 uint64`**  *无符号整数**`uint8 uint16 uint32 uint64` **
*    IEEE 754 Floating-point **`float32 float64`**  * IEEE 754浮点数**`float32 float64` **

Numbers are suffixed with their size in bits, **`bool`** is 1 byte. 数字后缀有大小（以位为单位），“ bool”是1个字节。

We also alias **`byte`** to mean **`uint8`** as a [built-in alias](#built-in-aliases).  我们还对**`byte` **进行别名，以将** uint8` **表示为[内置别名]（内置别名）。

 
#### Use  使用 

```fidl
// A record which contains fields of a few primitive types.
struct Sprite {
    float32 x;
    float32 y;
    uint32 index;
    uint32 color;
    bool visible;
};
```
 

 
### Bits  位 

 
*   Named bit types.  *命名位类型。
*   Discrete subset of bit values chosen from an underlying integer primitive type. *从基础整数基本类型中选择的位值的离散子集。
*   Not nullable.  *不可为空。
*   Bits must have at least one member.  *位必须至少具有一个成员。
*   Serializing or deserializing a bits value which has a bit set that is not a member of the bits declaration is a validation error. *序列化或反序列化具有不属于位声明成员的位集的位值是验证错误。

 

 
#### Use  使用 

```fidl
// Bit definitions for Info.features field
bits InfoFeatures : uint32 {
    WLAN = 0x00000001;      // If present, this device represents WLAN hardware
    SYNTH = 0x00000002;     // If present, this device is synthetic (not backed by h/w)
    LOOPBACK = 0x00000004;  // If present, this device receives all messages it sends
};
```
 

 
### Enums  枚举 

 
*   Proper enumerated types.  *正确的枚举类型。
*   Discrete subset of named values chosen from an underlying integer primitive type. *从基础整数基本类型中选择的命名值的离散子集。
*   Not nullable.  *不可为空。
*   Enums must have at least one member.  *枚举必须至少有一个成员。
*   Serializing or deserializing an enum from a value which is not defined in FIDL is a validation error. *从FIDL中未定义的值序列化或反序列化枚举是验证错误。

 
#### Declaration  宣言 

The ordinal index is **required** for each enum element. The underlying type of an enum must be one of: **int8, uint8, int16, uint16, int32, uint32, int64,uint64**. If omitted, the underlying type is assumed to be **uint32**. 每个枚举元素的序号索引都是“必需的”。枚举的基础类型必须是以下之一：** int8，uint8，int16，uint16，int32，uint32，int64，uint64 **。如果省略，则假定基础类型为** uint32 **。

```fidl
// An enum declared at library scope.
enum Beverage : uint8 {
    WATER = 0;
    COFFEE = 1;
    TEA = 2;
    WHISKEY = 3;
};

// An enum declared at library scope.
// Underlying type is assumed to be uint32.
enum Vessel {
    CUP = 0;
    BOWL = 1;
    TUREEN = 2;
    JUG = 3;
};
```
 

 
#### Use  使用 

Enum types are denoted by their identifier, which may be qualified if needed.  枚举类型由其标识符表示，如果需要，可以对其进行限定。

```fidl
// A record which contains two enum fields.
struct Order {
    Beverage beverage;
    Vessel vessel;
};
```
 

 
### Arrays  数组 

 
*   Fixed-length sequences of homogeneous elements.  *固定长度的同类元素序列。
*   Elements can be of any type including: primitives, enums, arrays, strings, vectors, handles, structs, tables, unions. *元素可以是任何类型，包括：基元，枚举，数组，字符串，向量，句柄，结构，表，联合。
*   Not nullable themselves; may contain nullable types.  *本身不能为空；可能包含可为空的类型。

 
#### Use  使用 

Arrays are denoted **`array<T>:n`** where _T_ can be any FIDL type (including an array) and _n_ is a positiveinteger constant expression which specifies the number of elements inthe array. 数组表示为**`array <T>：n` **，其中_T_可以是任何FIDL类型（包括数组），而_n_是一个正整数常量表达式，用于指定数组中元素的数量。

```fidl
// A record which contains some arrays.
struct Record {
    // array of exactly 16 floating point numbers
    array<float32>:16 matrix;

    // array of exactly 10 arrays of 4 strings each
    array<array<string>:4>:10 form;
};
```
 

 
### Strings  弦乐 

 
*   Variable-length sequence of UTF-8 encoded characters representing text.  *表示文本的UTF-8编码字符的变长序列。
*   Nullable; null strings and empty strings are distinct.  *可为空；空字符串和空字符串是不同的。
*   Can specify a maximum size, eg. **`string:40`** for a maximum 40 byte string. *可以指定最大尺寸，例如。 **`string：40` **最多40个字节的字符串。
*   May contain embedded `NUL` bytes, unlike traditional C strings.  *可能包含嵌入的“ NUL”字节，这与传统的C字符串不同。

 
#### Use  使用 

Strings are denoted as follows:  字符串表示如下：

 
*   **`string`** : non-nullable string (validation error occurs if null is encountered) * ** string **：不可为空的字符串（如果遇到null，则会发生验证错误）
*   **`string?`** : nullable string  * ** string？`**：可为空的字符串
*   **`string:N, string:N?`** : string, and nullable string, respectively, with maximum length of _N_ bytes * ** string：N，string：N？`**：分别为字符串和可为空的字符串，最大长度为_N_个字节

```fidl
// A record which contains some strings.
struct Record {
    // title string, maximum of 40 bytes long
    string:40 title;

    // description string, may be null, no upper bound on size
    string? description;
};
```
 

> Strings should not be used to pass arbitrary binary data since bindings enforce > valid UTF-8. Instead, consider `bytes` for small data or> [`fuchsia.mem.Buffer`](/docs/development/api/fidl.md#consider-using-fuchsia_mem_buffer)> for blobs. See> [Should I use string or vector?](/docs/development/api/fidl.md#should-i-use-string-or-vector)> for details. >字符串不应用于传递任意二进制数据，因为绑定会强制执行>有效的UTF-8。相反，对于小数据，请考虑使用“字节”；对于blob，请考虑> [`fuchsia.mem.Buffer`]（/ docs / development / api / fidl.mdconsider-using-fuchsia_mem_buffer）>。有关详细信息，请参见> [我应该使用字符串还是向量？]（/ docs / development / api / fidl.mdshould-i-use-string-or-vector）>。

 
### Vectors  向量 

 
*   Variable-length sequence of homogeneous elements.  *同构元素的可变长度序列。
*   Nullable; null vectors and empty vectors are distinct.  *可为空；空向量和空向量是不同的。
*   Can specify a maximum size, eg. **`vector<T>:40`** for a maximum 40 element vector. *可以指定最大尺寸，例如。 ** vector <T>：40` **，最多可包含40个元素向量。
*   There is no special case for vectors of bools. Each bool element takes one byte as usual. *布尔向量没有特殊情况。每个布尔元素照常占用一个字节。
*   We have a [built-in alias](#built-in-aliases) for **`bytes`** to mean `vector<uint8>`, and it can be size bound in a similar fashion e.g.`bytes:1024`. *我们有一个“内置别名”（alias-in-aliases），用于表示“ bytes” **，表示“ vector <uint8>”，并且可以用类似的方式进行大小绑定，例如“ bytes：1024”。 。

 
#### Use  使用 

Vectors are denoted as follows:  向量表示如下：

 
*   **`vector<T>`** : non-nullable vector of element type _T_ (validation error occurs if null is encountered) * ** vector <T>`**：元素类型_T_的不可为空的向量（如果遇到null，则会发生验证错误）
*   **`vector<T>?`** : nullable vector of element type _T_ * ** vector <T>？`**：元素类型_T_的可为空的向量
*   **`vector<T>:N, vector<T>:N?`** : vector, and nullable vector, respectively, with maximum length of _N_ elements * ** vector <T>：N，vector <T>：N？`**：分别为向量和可为空的向量，最大长度为_N_个元素

_T_ can be any FIDL type.  _T_可以是任何FIDL类型。

```fidl
// A record which contains some vectors.
struct Record {
    // a vector of up to 10 integers
    vector<int32>:10 params;

    // a vector of bytes, no upper bound on size
    bytes blob;

    // a nullable vector of up to 24 strings
    vector<string>:24? nullable_vector_of_strings;

    // a vector of nullable strings, no upper bound on size
    vector<string?> vector_of_nullable_strings;

    // a vector of vectors of 16-element arrays of floating point numbers
    vector<vector<array<float32>:16>> complex;
};
```
 

 
### Handles  提手 

 
*   Transfers a Zircon capability by handle value.  *通过手柄值转移锆石能力。
*   Stored as a 32-bit unsigned integer.  *存储为32位无符号整数。
*   Nullable by encoding as a zero-valued handle.  *通过编码为零值句柄可以为空。

 
#### Use  使用 

Handles are denoted:  句柄表示为：

 
*   **`handle`** : non-nullable Zircon handle of unspecified type * **`handle` **：未指定类型的不可为空的Zircon句柄
*   **`handle?`** : nullable Zircon handle of unspecified type * **`handle？`**：未指定类型的可空Zircon句柄
*   **`handle<H>`** : non-nullable Zircon handle of type _H_ * **`handle <H>`**：_H_类型的不可为空的Zircon句柄
*   **`handle<H>?`** : nullable Zircon handle of type _H_ * **`handle <H>？`**：_H_类型的可空Zircon句柄

_H_ can be any [object][zircon_objects] supported by Zircon, e.g. `channel`, `thread`, `vmo`. Please refer to the [grammar][grammar] for a full list. _H_可以是Zircon支持的任何[object] [zircon_objects]，例如`channel`，`thread`，`vmo`。有关完整列表，请参阅[语法] [语法]。

```fidl
// A record which contains some handles.
struct Record {
    // a handle of unspecified type
    handle h;

    // an optional channel
    handle<channel>? c;
};
```
 

 
### Structs  结构 

 
*   Record type consisting of a sequence of typed fields.  *记录类型由一系列类型化字段组成。
*   Declaration is not intended to be modified once deployed; use protocol extension instead. *声明一旦部署，将不被修改；请改用协议扩展。
*   Reference may be nullable.  *引用可能为空。
*   Structs contain zero or more members.  *结构包含零个或多个成员。

 
#### Declaration  宣言 

```fidl
struct Point {
    float32 x;
    float32 y;
};
struct Color {
    float32 r;
    float32 g;
    float32 b;
};
```
 

 
#### Use  使用 

Structs are denoted by their declared name (eg. **Circle**) and nullability:  结构以其声明的名称（例如** Circle **）和可空性表示：

 
*   **`Circle`** : non-nullable Circle  * ** Circle` **：不可为空的圆圈
*   **`Circle?`** : nullable Circle  * ** Circle？`**：可为空的Circle

```fidl
struct Circle {
    bool filled;
    Point center;    // Point will be stored in-line
    float32 radius;
    Color? color;    // Color will be stored out-of-line
    bool dashed;
};
```
 

 
### Tables  桌子 

 
*   Record type consisting of a sequence of typed fields with ordinals.  *记录类型，该类型由一系列具有序数的类型化字段组成。
*   Declaration is intended for forward and backward compatibility in the face of schema changes.  *声明用于面对架构更改时的向前和向后兼容性。
*   Tables cannot be nullable. The semantics of "missing value" is expressed by an empty table i.e. where all members are absent, to avoid dealing with double nullability. *表不能为空。 “缺失值”的语义由一个空表表示，即所有成员都不存在的表，以避免处理双重空值。
*   Tables contain zero or more members.  *表包含零个或多个成员。

 
#### Declaration  宣言 

```fidl
table Profile {
    1: vector<string> locales;
    2: vector<string> calendars;
    3: vector<string> time_zones;
};
```
 

 
#### Use  使用 

Tables are denoted by their declared name (eg. **Profile**):  表格以其声明的名称表示（例如** Profile **）：

 
*   **`Profile`** : non-nullable Profile  * **个人资料**：不可为空的个人资料

Here, we show how `Profile` evolves to also carry temperature units. A client aware of the previous definition of `Profile` (without temperature units)can still send its profile to a server which has been updated to handle the largerset of fields. 在这里，我们展示“配置文件”如何演变为也携带温度单位。知道“配置文件”先前定义（没有温度单位）的客户端仍可以将其配置文件发送到已更新以处理更大字段集的服务器。

```fidl
enum TemperatureUnit {
    CELSIUS = 1;
    FAHRENHEIT = 2;
};

table Profile {
    1: vector<string> locales;
    2: vector<string> calendars;
    3: vector<string> time_zones;
    4: TemperatureUnit temperature_unit;
};
```
 

 
### Unions  工会 

 
*   Tagged option type consisting of tag field and variadic contents.  *带标签的选项类型，由标签字段和可变参数内容组成。
*   Declaration is not intended to be modified once deployed; use protocol extension instead. *声明一旦部署，将不被修改；请改用协议扩展。
*   Reference may be nullable.  *引用可能为空。
*   Unions contain one or more members. A union with no members would have no inhabitants and thus would make little sense in a wire format. *联盟包含一个或多个成员。没有成员的工会将没有居民，因此采用有线形式毫无意义。

> Unions are deprecated. New code should use [xunions](#Xunions).  >不赞成使用工会。新代码应使用[xunions]（Xunions）。

 
#### Declaration  宣言 

```fidl
union Pattern {
    Color color;        // the Pattern contains either a Color
    Texture texture;    // or a Texture, but not both at the same time
};
struct Color {
    float32 r;
    float32 g;
    float32 b;
};
struct Texture { string name; };
```
 

 
#### Use  使用 

Unions are denoted by their declared name (eg. **Pattern**) and nullability:  联合用其声明的名称（例如** Pattern **）和可空性表示：

 
*   **`Pattern`** : non-nullable Pattern  * ** Pattern` **：不可为空的模式
*   **`Pattern?`** : nullable Pattern  * ** Pattern？`**：可为空的模式

 
### Xunions  Xunions 

 
*   Record type consisting of an ordinal and an envelope.  *记录类型，由序数和信封组成。
*   Ordinal indicates member selection, envelope holds contents.  *序号表示会员选择，信封内含内容。
*   Declaration can be modified after deployment, while maintaining ABI compatibility. See the [Compatibility Guide](abi-compat.md#xunions) forsource-compatibility considerations. *可以在部署后修改声明，同时保持ABI兼容性。有关源兼容性注意事项，请参见[兼容性指南]（abi-compat.mdxunions）。
*   Reference may be nullable.  *引用可能为空。
*   Xunions contain one or more members. An xunion with no members would have no inhabitants and thus would make little sense in a wire format. * Xunions包含一个或多个成员。没有成员的轴心国将没有居民，因此以有线形式毫无意义。

 
#### Declaration  宣言 

```fidl
xunion Value {
    int16 command;
    Circle data;
    float64 offset;
};
```
 

 
#### Use  使用 

Xunions are denoted by their declared name (eg. **Value**) and nullability:  Xunion的声明名称（例如** Value **）和可空性表示：

 
*   **`Value`** : non-nullable Value  * **`Value` **：非空值
*   **`Value?`** : nullable Value  * ** Value？`**：可为空的值

 
### Protocols  通讯协定 

 
*   Describe methods which can be invoked by sending messages over a channel.  *描述可以通过在通道上发送消息来调用的方法。
*   Methods are identified by their ordinal index. The compiler calculates the ordinal by  *方法由其序号索引标识。编译器通过以下方式计算序数
    * Taking the SHA-256 hash of the string generated by concatenating:  *通过串联生成的字符串的SHA-256哈希：
        * The UTF-8 encoded library name, with no trailing \0 character  * UTF-8编码的库名称，不带尾随\ 0字符
        * '.' (ASCII 0x2e)  *'。' （ASCII 0x2e）
        * The UTF-8 encoded protocol name, with no trailing \0 character  * UTF-8编码的协议名称，不带尾随\ 0字符
        * '/' (ASCII 0x2f)  *'/'（ASCII 0x2f）
        * The UTF-8 encoded method name, with no trailing \0 character  * UTF-8编码的方法名称，不带尾随\ 0字符
    * Extracting the upper 32 bits of the hash value, and  *提取哈希值的高32位，并
    * Setting the upper bit of that value to 0.  *将该值的高位设置为0。
    * To coerce the compiler into generating a different value, methods can have a `Selector` attribute.  The value of the `Selector` attribute will beused in the place of the method name above. *为了强迫编译器生成不同的值，方法可以具有`Selector`属性。 Selector属性的值将在上面的方法名称处使用。
*   Each method declaration states its arguments and results.  *每个方法声明都声明其参数和结果。
    *   If no results are declared, then the method is one-way: no response will be generated by the server. *如果未声明任何结果，则该方法是单向的：服务器将不会生成任何响应。
    *   If results are declared (even if empty), then the method is two-way: each invocation of the method generates a response from the server. *如果声明了结果（即使为空），则该方法是双向的：方法的每次调用都会从服务器生成一个响应。
    *   If only results are declared, the method is referred to as an *event*. It then defines an unsolicited message from the server. *如果仅声明结果，则该方法称为*事件*。然后，它定义了来自服务器的未经请求的消息。
    *   Two-way methods may declare an error type which a server can send instead of the response. This type must be an `int32`, `uint32`, or an`enum` thereof. *双向方法可以声明服务器可以发送而不是响应的错误类型。此类型必须是“ int32”，“ uint32”或“枚举”。

 
*   When a server of a protocol is about to close its side of the channel, it may elect to send an **epitaph** message to the client to indicate thedisposition of the connection. The epitaph must be the last messagedelivered through the channel. An epitaph message includes a 32-bit intvalue of type **zx_status_t**.  Negative values are reserved for systemerror codes.  Positive values are reserved for application errors.  A statusof ZX_OK indicates successful operation. *当协议服务器即将关闭其通道一侧时，它可以选择向客户端发送一条“ epitaph”消息，以指示连接的位置。墓志铭必须是通过频道传递的最后一条消息。墓志铭消息包含类型为** zx_status_t **的32位整数值。负值保留给系统错误代码。为应用程序错误保留正值。 ZX_OK的状态指示操作成功。

 
#### Declaration  宣言 

```fidl
enum DivisionError : uint32 {
    DivideByZero = 1;
};

protocol Calculator {
    Add(int32 a, int32 b) -> (int32 sum);
    Divide(int32 dividend, int32 divisor)
        -> (int32 quotient, int32 remainder) error DivisionError;
    Clear();
    -> OnClear();
};
```
 

 
#### Use  使用 

Protocols are denoted by their name, directionality of the channel, and optionality: 协议由其名称，通道的方向性和可选性表示：

 
*   **`Protocol`** : non-nullable FIDL protocol (client endpoint of channel)  * ** Protocol` **：不可为空的FIDL协议（通道的客户端端点）
*   **`Protocol?`** : nullable FIDL protocol (client endpoint of channel)  * ** Protocol？`**：可为空的FIDL协议（通道的客户端端点）
*   **`request<Protocol>`** : non-nullable FIDL protocol request (server endpoint of channel) * ** request <Protocol>`**：不可为空的FIDL协议请求（通道的服务器端点）
*   **`request<Protocol>?`** : nullable FIDL protocol request (server endpoint of channel) * ** request <Protocol>？****：可为空的FIDL协议请求（通道的服务器端点）

```fidl
// A record which contains protocol-bound channels.
struct Record {
    // client endpoint of a channel bound to the Calculator protocol
    Calculator c;

    // server endpoint of a channel bound to the Science protocol
    request<Science> s;

    // optional client endpoint of a channel bound to the
    // RealCalculator protocol
    RealCalculator? r;
};
```
 

 
### Protocol Composition  协议组成 

A protocol can include methods from other protocols. This is called composition: you compose one protocol from other protocols. 协议可以包括其他协议中的方法。这称为组合：您可以从其他协议中组合一个协议。

Composition is used in the following cases:  在以下情况下使用合成：

 
1. you have multiple protocols that all share some common behavior(s)  1.您有多个协议，它们共享一些共同的行为
2. you have varying levels of functionality you want to expose to different audiences  2.您希望向不同的受众群体展示不同级别的功能

 
#### Common behavior  常见行为 

In the first case, there might be behavior that's shared across multiple protocols. For example, in a graphics system, several different protocols might all share acommon need to set a background and foreground color.Rather than have each protocol define their own color setting methods, a commonprotocol can be defined: 在第一种情况下，可能存在跨多个协议共享的行为。例如，在图形系统中，几种不同的协议可能都共享设置背景色和前景色的共同需要，而不是让每个协议定义自己的颜色设置方法，而是可以定义一个通用协议：

```fidl
struct Color {
    int16 r;
    int16 g;
    int16 b;
}

protocol SceneryController {
    SetBackground(Color color);
    SetForeground(Color color);
};
```
 

It can then be shared by other protocols:  然后可以由其他协议共享它：

```fidl
protocol Drawer {
    compose SceneryController;
    Circle(int x, int y, int radius);
    Square(int x, int y, int diagonal);
};

protocol Writer {
    compose SceneryController;
    Text(int x, int y, string message);
};
```
 

In the above, there are three protocols, `SceneryController`, `Drawer`, and `Writer`. `Drawer` is used to draw graphical objects, like circles and squares at given locationswith given sizes.It composes the methods **SetBackground()** and **SetForeground()** fromthe `SceneryController` protocol because it includes the `SceneryController` protocol(by way of the `compose` keyword). 在上面，有三种协议，`SceneryController`，`Drawer`和`Writer`。 ``Drawer''用于在给定位置以给定大小绘制图形对象，例如圆形和正方形，它组成了`SceneryController`协议的** SetBackground（）**和** SetForeground（）**方法，因为它包含了SceneryController协议（通过关键字compose）。

The `Writer` protocol, used to write text on the display, includes the `SceneryController` protocol in the same way. 用于在显示器上写文本的`Writer`协议以相同的方式包括`SceneryController`协议。

Now both `Drawer` and `Writer` include **SetBackground()** and **SetForeground()**.  现在`Drawer`和`Writer`都包含** SetBackground（）**和** SetForeground（）**。

This offers several advantages over having `Drawer` and `Writer` specify their own color setting methods: 与让`Drawer`和`Writer`指定它们自己的颜色设置方法相比，这具有几个优点：

 
*   the way to set background and foreground colors is the same, whether it's used to draw a circle, square, or put text on the display. *设置背景颜色和前景色的方法是相同的，无论是用来绘制圆形，正方形还是在显示器上放置文本。
*   new methods can be added to `Drawer` and `Writer` without having to change their definitions, simply by adding them to the `SceneryController` protocol. *只需将它们添加到`SceneryController`协议中，即可将新方法添加到`Drawer`和`Writer`中，而无需更改其定义。

The last point is particularly important, because it allows us to add functionality to existing protocols.For example, we might introduce an alpha-blending (or "transparency") feature toour graphics system.By extending the `SceneryController` protocol to deal with it, perhaps like so: 最后一点特别重要，因为它允许我们向现有协议中添加功能。例如，我们可以在图形系统中引入alpha混合（或“透明性”）功能。通过扩展`SceneryController`协议来处理它，也许像这样：

```fidl
protocol SceneryController {
    SetBackground(Color color);
    SetForeground(Color color);
    SetAlphaChannel(int a);
};
```
 

we've now extended both `Drawer` and `Writer` to be able to support alpha blending.  现在，我们扩展了“抽屉”和“书写器”以支持Alpha混合。

 
#### Multiple compositions  多种成分 

Composition is not a one-to-one relationship &mdash; we can include multiple compositions into a given protocol, and not all protocols need be composed of the same mix ofincluded protocols. 组成不是一对一的关系。我们可以在给定的协议中包括多个组成部分，并且并非所有协议都需要由所包含协议的相同组合组成。

For example, we might have the ability to set font characteristics. Fonts don't make sense for our `Drawer` protocol, but they do make sense for our `Writer`protocol, and perhaps other protocols. 例如，我们也许可以设置字体特征。字体对我们的`Drawer`协议没有意义，但对我们的`Writer`协议以及其他协议却有意义。

So, we define our `FontController` protocol:  因此，我们定义了`FontController`协议：

```fidl
protocol FontController {
    SetPointSize(int points);
    SetFontName(string fontname);
    Italic(bool onoff);
    Bold(bool onoff);
    Underscore(bool onoff);
    Strikethrough(bool onoff);
};
```
 

and then invite `Writer` to include it, by using the `compose` keyword:  然后使用`compose`关键字邀请`Writer`包含它：

```fidl
protocol Writer {
    compose SceneryController;
    compose FontController;
    Text(int x, int y, string message);
};
```
 

Here, we've extended the `Writer` protocol with the `FontController` protocol's methods, without disturbing the `Drawer` protocol (which doesn't need to know anything about fonts). 在这里，我们已经使用“ FontController”协议的方法扩展了“ Writer”协议，而不会干扰“ Drawer”协议（该协议不需要了解字体）。

Protocol composition is similar to [mixin]. More details are discussed in [FTP-023: Compositional Model][ftp-023]. 协议组成类似于[mixin]。在[FTP-023：组成模型] [ftp-023]中讨论了更多详细信息。

 
#### Layering  分层 

At the beginning of this section, we mentioned a second use for composition, namely exposing various levels of functionality to different audiences. 在本节的开头，我们提到了组合的第二种用法，即向不同的受众展示各种功能级别。

In this example, we have two protocols that are independently useful, a `Clock` protocol to get the current time and timezone: 在此示例中，我们有两个独立有用的协议，一个“时钟”协议，用于获取当前时间和时区：

```fidl
protocol Clock {
    Now() -> (Time time);
    CurrentTimeZone() -> (string timezone);
}
```
 

And an `Horologist` protocol that sets the time and timezone:  还有一个“时间学家”协议来设置时间和时区：

```fidl
protocol Horologist {
    SetTime(Time time);
    SetCurrentTimeZone(string timezone);
}
```
 

We may not necessarily wish to expose the more privileged `Horologist` protocol to just any client, but we do want to expose it to the system clock component.So, we create a protocol (`SystemClock`) which composes both: 我们可能不一定希望只向任何客户端公开特权更高的“ Horologist”协议，但确实希望将其公开给系统时钟组件。因此，我们创建了一个协议（“ SystemClock”），该协议由以下两种组成：

```fidl
protocol SystemClock {
    compose Clock;
    compose Horologist;
}
```
 

 
### Aliasing  混叠 

Type aliasing is supported. For example: 支持类型别名。例如：

```fidl
using StoryID = string:MAX_SIZE;
using up_to_five = vector:5;
```
 

In the above, the identifier `StoryID` is an alias for the declaration of a `string` with a maximum size of `MAX_SIZE`.The identifier `up_to_five` is an alias for a vector declaration of five elements. 上面的标识符``StoryID''是声明字符串的别名，最大长度为``MAX_SIZE''。标识符``up_to_five''是五个元素的向量声明的别名。

The identifiers `StoryID` and `up_to_five` can be used wherever their aliased definitions can be used.Consider: 可以在使用别名定义的任何地方使用``StoryID''和``up_to_five''标识符。

```fidl
struct Message {
    StoryID baseline;
    up_to_five<StoryID> chapters;
};
```
 

Here, the `Message` struct contains a string of `MAX_SIZE` bytes called `baseline`, and a vector of up to `5` strings of `MAX_SIZE` called `chapters`. 在这里，“消息”结构包含一个称为“ baseline”的字符串“ MAX_SIZE”个字节，以及一个称为“章节”的最多5个“ MAX_SIZE”字符串的向量。

Note that **`byte`** and **`bytes`** are built in aliases, [see below](#built-in-aliases).  请注意，“ bytes”和“ bytes” **是内置别名的，请参见下文（内置别名）。

 
### Built-ins  内建 

FIDL provides several built-ins:  FIDL提供了几个内置函数：

 
* convenience types (**`byte`** and **`bytes`**)  *便利类型（“字节”和“字节” **）
* `zx library` [see below](#zx-library)  *`zx库`[见下文]（zx-library）

 
#### Built-in aliases {#built-in-aliases}  内置别名{built-in-aliases} 

The types **`byte`** and **`bytes`** are built-in, and are conceptually equivalent to: 字节类型和字节类型是内置的，在概念上等效于：

```fidl
library builtin;

using byte = uint8;
using bytes = vector<byte>;
```
 

When you refer to a name without specific scope, e.g.:  当您引用没有特定范围的名称时，例如：

```fidl
struct SomeName {
    byte here;
};
```
 

we treat this as `builtin.byte` automatically (so long as there isn't a more-specific name in scope). 我们会自动将其视为“ builtin.byte”（只要范围中没有更具体的名称）。

 
#### ZX Library  ZX库 

The `fidlc` compiler automatically generates an internal [ZX library](library-zx.md) for you that contains commonly used Zircon definitions. fidlc编译器会自动为您生成一个内部[ZX库]（library-zx.md），其中包含常用的Zircon定义。

