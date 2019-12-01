 
# FIDL ABI and Source Compatibility Guide  FIDL ABI和源兼容性指南 

Date: 2019-03  日期：2019-03

Author: thatguy@google.com  作者：thatguy@google.com

Contributors: pascallouis@google.com, yifeit@google.com, cramertj@google.com  贡献者：pascallouis @ google.com，yifeit @ google.com，cramertj @ google.com

 
# Intended Audience  目标受众 

This doc is written for engineers who want to evolve FIDL APIs. It describes what can be done safely without disrupting fellow teammates ordownstream clients. 本文档是为想要发展FIDL API的工程师而写的。它描述了可以安全完成的工作，而不会打扰队友或下游客户。

 
## What is ABI compatibility?  什么是ABI兼容性？ 

ABI (application binary interface) compatibility is concerned with the encoding and decoding of data over binary interfaces.FIDL messages (method calls on FIDL protocols) end up serialized as bytesover a zircon channel. Both channel endpoints (the client and server)must agree on the size, ordering and meaning of the bytes.A mismatch in expectations leads to binary incompatibility. ABI（应用程序二进制接口）兼容性与二进制接口上数据的编码和解码有关。FIDL消息（FIDL协议上的方法调用）最终通过锆石通道序列化为字节。通道的两个端点（客户端和服务器）必须在字节的大小，顺序和含义上达成共识。期望值不匹配会导致二进制不兼容。

 
## Considerations when changing FIDL source  更改FIDL源时的注意事项 

A change to a FIDL type that is source compatible (also known as API compatible) means it is possible for someone to write code using thegenerated code for a type that compiles both before and after thechange is made.Making a source-incompatible change requires changingall client source code at the same time (difficult if clients existoutside the repository) to avoid breaking builds. 更改为与源兼容（也称为API兼容）的FIDL类型，意味着有人可以使用生成的代码为更改之前和之后进行编译的类型编写代码。进行与源不兼容的更改需要更改所有同时使用客户端源代码（如果客户端不在存储库之外，则很难），以避免破坏构建。

Note: Since Fuchsia sources (and related product code) exist in multiple repositories with integration rollers and SDK releasesbetween them, it is not enough to ensure that the fuchsia.gitrepository compiles. 注意：由于紫红色的来源（和相关的产品代码）存在于多个存储库中，并且它们之间有集成滚筒和SDK版本，因此仅确保fuchsia.gitrepository编译是不够的。

> Disclaimer: The FIDL compatibility story today contains a number of > edge cases.> Language bindings may expose interfaces whose usage may or may not> be resilient to changes in the underlying FIDL protocol.> There are ongoing efforts to standardize these interfaces, but in the> meantime, this document exists as a best-effort guide towards what> types of code may be broken by what sorts of FIDL changes.> If you discover an omission or mistake in this document, please>  suggest the appropriate change, and refrain from enacting retribution on this> document's authors. >免责声明：今天的FIDL兼容性故事包含许多>极端情况。>语言绑定可能会暴露其使用情况可能会或可能不会使用的接口>对基础FIDL协议的更改具有弹性。>正在进行使这些接口标准化的努力，但是在此期间，本文档作为尽力而为的指南，旨在指导哪些类型的FIDL更改可能破坏代码类型。>如果您发现本文档中有遗漏或错误，请>建议适当的更改，并避免对本文档的作者做出报应。

 
# The Guide  导游 

[TOC]  [目录]

 
## structs  结构 

> General guidance: once a struct is defined and in use, it cannot be changed.  >一般指导：一旦定义并使用了结构，就无法更改。

 
#### Renaming the struct  重命名结构 

```fidl
struct A {         struct A_new {
  int32 a;           int32 a;
  string b;          string b;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

**Transition Considerations**:  **转换注意事项**：

 
1. ~~Introduce an alias~~  1. ~~介绍一个别名~~
2. Make a copy of the struct with the new name  2.使用新名称复制结构
3. Migrate all clients  3.迁移所有客户
4. ~~Remove alias~~  4. ~~删除别名~~
5. Delete the old struct  5.删除旧的结构

 
#### Reordering members  重新订购会员 

```fidl
struct A {         struct A {
  int32 a;           string b;
  string b;          int32 a;
};                 };
```
 

![red x](rx.png) **ABI Compatibility**: NO  ！[red x]（rx.png）** ABI兼容性**：否

**Transition Considerations**:  **转换注意事项**：

 
* **Positional initializers will break** e.g.,:  * **位置初始化程序会中断**，例如：
    * C++:  * C ++：
        * `auto a = A{10, "foo"};`  *`auto a = A {10，“ foo”};`
    * Go:  * 走：
        * `A {10, "foo"};`  *`A {10，“ foo”};`
* **Prefer**:  * **首选**：
    * C++:  * C ++：
        * `auto a = A{`<br>&nbsp;&nbsp;`.a = 10,`<br>&nbsp;&nbsp;`.b = "foo"`<br>`}`;  *`auto a = A {`<br>＆nbsp;`.a10，`<br> nbsp; nbsp;`.b =“ foo”`<br>`}`;
    * Go:  * 走：
        * `a := A{`<br>&nbsp;&nbsp;`A:10.`<br>&nbsp;&nbsp;`B: "foo",`<br>`}`  *`a：= A {`<br>＆nbsp;`A10.` <br> nbsp;`B：“ foo”，`<br>`}`

 
#### Renaming members  重命名成员 

```fidl
struct A {         struct A {
  int32 a;           int32 a_new;
  string b;          string b;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![red x](rx.png) **Transition Considerations**: NO  ！[red x]（rx.png）**转换注意事项**：否

 
* **Named reference / initialization will break:**  * **命名参考/初始化将中断：**
    * C++: `f(a.a_new)` and `auto a = A{.a = 10};`  * C ++：`f（a.a_new）`和`auto a = A {.a = 10};`

 
#### Adding members  新增成员 

```fidl
struct A {         struct A {
  int32 a;           int32 a;
  string b;          string b;
  int32 c;
};                 };
```
 

![red x](rx.png) **ABI Compatibility**: NO  ！[red x]（rx.png）** ABI兼容性**：否

**Transition Considerations**:  **转换注意事项**：
* Depends on the language bindings.  *取决于语言绑定。
* Go positional initializers &amp; Rust and Dart struct literals will break.  *位置初始化器放大器； Rust和Dart的结构文字会中断。

 
#### Removing members  删除成员 

```fidl
struct A {         struct A {
  int32 a;           int32 a;
  string b;
};                 };
```
 

![red x](rx.png) **ABI Compatibility**: NO  ！[red x]（rx.png）** ABI兼容性**：否

![green checkmark](gc.png) **Transition Consideration**:  ！[绿色对勾]（gc.png）**转换注意事项**：
* So long as `b` is not referenced any more (including in positional initializers).  *只要不再引用“ b”（包括在位置初始值设定项中）。

 
## tables  桌子 

 
#### Renaming the table  重命名表格 

```fidl
table T {          table T_new {
  1: int32 a;        1: int32 a;
  2: string b;       2: string b;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

 
* **Transition Considerations**: **See: ["struct: Renaming the struct"](#renaming-the-struct)** * **转换注意事项**：**请参阅：[“ struct：重命名该结构”]（重命名该结构）**

 
#### Reordering members  重新订购会员 

```fidl
table T {          table T {
  1: int32 a;        2: string b;
  2: string b;       1: int32 a;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是
* Just don't change the ordinal values.  *只是不要更改序数值。

![green checkmark](gc.png) **Transition Considerations**: YES  ！[绿色复选标记]（gc.png）**转换注意事项**：是

 
#### Renaming members  重命名成员 

```fidl
table T {          table T {
  1: int32 a;        1: int32 a_new;
  2: string b;       2: string b;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![red x](rx.png) **Transition Considerations**: NO  ！[red x]（rx.png）**转换注意事项**：否

 
#### Adding members  新增成员 

```fidl
table T {          table T {
  1: int32 a;        1: int32 a;
  2: string b;       2: string b;
                     3: int32 c;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![green checkmark](gc.png) **Transition Considerations**: YES  ！[绿色复选标记]（gc.png）**转换注意事项**：是

 
#### Removing members  删除成员 

```fidl
table T {          table T {
  1: int32 a;        1: int32 a;
  2: string b;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![green checkmark](gc.png) **Transition Considerations**: YES  ！[绿色复选标记]（gc.png）**转换注意事项**：是
* So long as `b` is not referenced any more.  *只要不再引用`b`。

 
#### Adding [NoHandles]  添加[NoHandles] 

```fidl
                   [NoHandles]
table T {          table T {
  1: int32 a;        1: int32 a;
  2: string b;       2: string b;
};                 };
```
 

**ABI Compatibility**: **TODO**  ** ABI兼容性**：** TODO **

**Transition Considerations**: **TODO**  **转换注意事项**：** TODO **

 
## unions  工会 

Note: unions (vs **x**unions) are deprecated. However, they follow similar rules to [structs](#structs). 注意：联合（vs ** x ** unions）已弃用。但是，它们遵循与[structs]（structs）类似的规则。

 
## xunions  讯联 

 
#### Reordering members  重新订购会员 

```fidl
xunion A {         xunion A {
  int32 a;           string b;
  string b;          int32 a;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![green checkmark](gc.png) **Transition Considerations**: YES  ！[绿色复选标记]（gc.png）**转换注意事项**：是

 
#### Renaming members  重命名成员 

```fidl
xunion A {         xunion A {
  int32 a;           int32 a_new;
  string b;          string b;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是
* Use the `[Selector]` to retain compatibility:  *使用`[Selector]`来保持兼容性：
  * `xunion A {`<br>&nbsp;&nbsp;`[Selector = "a"]`<br>&nbsp;&nbsp;`int32 a_new;`<br>&nbsp;&nbsp;`string b;`<br>`};`  *`xunion A {`<b> nbsp;`[选择符=“ a”]`<br> nbsp;`int32 a_new;`<br> nbsp;`string b;`<br>` };`

![red x](rx.png) **Transition Considerations**: NO  ！[red x]（rx.png）**转换注意事项**：否

 
#### Adding members  新增成员 

```fidl
xunion A {         xunion A {
  int32 a;           int32 a;
  string b;          string b;
                     int32 c;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

**Transition Considerations**:  **转换注意事项**：
* Depends on language bindings.  *取决于语言绑定。
* Exhaustive matching (i.e., C++ `switch{}` on union tag) will break.  *详尽的匹配（即，联合标记上的C ++`switch {}`）会中断。

 
#### Removing members  删除成员 

```fidl
xunion A {         xunion A {
  int32 a;           int32 a;
  string b;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![green checkmark](gc.png) **Transition Considerations**: YES  ！[绿色复选标记]（gc.png）**转换注意事项**：是
* So long as `b` is not referenced any more.  *只要不再引用`b`。

 
## vectors  向量 

 
#### Changing the size  改变大小 

```fidl
vector<T>:N        vector<T>:M
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![green checkmark](gc.png) **Transition Considerations**:  ！[绿色复选标记]（gc.png）**转换注意事项**：

 
* If the maximum size of the vector is **growing** (i.e. `M > N`) then all **consumers** _MUST_ be updated first. *如果向量的最大大小是“增长中的”（即“ M> N”），则所有“消费者” _MUST_将首先更新。
* If the maximum size of the vector is **shrinking** (i.e. `M < N`) then all **producers** _MUST_ be updated first. *如果向量的最大大小是“缩小”（即“ M <N”），则所有“生产者” _MUST_都将首先更新。

 
#### Changing the element type  更改元素类型 

```fidl
vector<T>:N        vector<U>:N
```
 

In many cases, this is neither ABI compatible, nor transitionable. Specific cases can be discussed, but do not rely on this for evolvability of yourprotocols. 在许多情况下，这既不是ABI兼容的，也不是可转换的。可以讨论特定的情况，但不要以此为基础来扩展协议。

![yellow warning](yw.png) **ABI Compatibility**: DEPENDS  ！[黄色警告]（yw.png）** ABI兼容性**：取决于

![yellow warning](yw.png) **Transition Considerations**: DEPENDS  ！[黄色警告]（yw.png）**转换注意事项**：取决于

 
## strings  弦 

_Similar to vectors._  _类似于向量。_

 
## enums  枚举 

 
#### Reordering members  重新订购会员 

```fidl
enum E {           enum E {
  A = 1;             B = 2;
  B = 2;             A = 1;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![green checkmark](gc.png) **Transition Considerations**: YES  ！[绿色复选标记]（gc.png）**转换注意事项**：是

 
#### Renaming members  重命名成员 

```fidl
enum E {           enum E {
  A = 1;             A_NEW = 1;
  B = 2;             B = 2;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![red x](rx.png) **Transition Considerations**: NO  ！[red x]（rx.png）**转换注意事项**：否

 
#### Adding members  新增成员 

```fidl
enum E {           enum E {
  A = 1;             A = 1;
  B = 2;             B = 2;
                     C = 3;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

**Transition Considerations**:  **转换注意事项**：
* C++ `switch{}` without `default` will break  *没有`default`的C ++`switch {}`会中断
* Rust `match` without `"_"` will break  *没有`__`的Rust`match`会中断

 
#### Removing members  删除成员 

```fidl
enum E {           enum E {
  A = 1;             A = 1;
  B = 2;
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

**Transition Considerations**:  **转换注意事项**：
* Code which uses `E::B` will break  *使用`E :: B`的代码将中断

 
## protocol libraries & names  协议库名称 

 
#### Renaming [Discoverable]  重命名[可发现] 

```fidl
[Discoverable]     [Discoverable]
protocol P {       protocol P_new {
  M1() -> ();        M1() -> ();
  M2() -> ();        M2() -> ();
};                 };
```
 

![red x](rx.png) **ABI Compatibility**: NO  ！[red x]（rx.png）** ABI兼容性**：否

 
* Renaming breaks service discoverability; names are used for service paths in namespaces/Directories. *重命名破坏了服务的可发现性；名称用于名称空间/目录中的服务路径。

![red x](rx.png) **Transition Considerations**: NO  ！[red x]（rx.png）**转换注意事项**：否

 
#### Renaming non-[Discoverable]  重命名非[Discoverable] 

```fidl
protocol P {       protocol P_new {
  M1() -> ();        M1() -> ();
  M2() -> ();        M2() -> ();
};                 };
```
 

![red x](rx.png) **ABI Compatibility**: NO  ！[red x]（rx.png）** ABI兼容性**：否

 
* Protocol names are part of method ordinal hashes.  *协议名称是方法序数哈希的一部分。

![red x](rx.png) **Transition Considerations**: NO  ！[red x]（rx.png）**转换注意事项**：否

 
#### Renaming the library  重命名库 

```fidl
library A:         library A.new:

protocol P {       protocol P {
  M1() -> ();        M1() -> ();
  M2() -> ();        M2() -> ();
};                 };
```
 

![red x](rx.png) **ABI Compatibility**: NO  ！[red x]（rx.png）** ABI兼容性**：否

 
* Library names are part of method ordinal hashes for all protocols within them.  *库名称是其中所有协议的方法序数哈希的一部分。

![red x](rx.png) **Transition Considerations**: NO  ！[red x]（rx.png）**转换注意事项**：否

 
## protocol methods  协议方法 

Note: These rules apply only to the methods, their names & ordering. Protocol method arguments and return values follow the samerules as [structs](#structs). 注意：这些规则仅适用于方法，其名称顺序。协议方法的参数和返回值遵循与[structs]（structs）相同的规则。

 
#### Reordering members  重新订购会员 

```fidl
protocol P {       protocol P {
  M1() -> ();        M2() -> ();
  M2() -> ();        M1() -> ();
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![green checkmark](gc.png) **Transition Considerations**: YES  ！[绿色复选标记]（gc.png）**转换注意事项**：是

 

 
#### Renaming members  重命名成员 

```fidl
protocol P {       protocol P {
  M1() -> ();        M1_new() -> ();
  M2() -> ();        M2() -> ();
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

 
* Use the `[Selector]` to retain compatibility:  *使用`[Selector]`来保持兼容性：
  * `protocol P {`<br>&nbsp;&nbsp;`[Selector= "M1"]`<br>&nbsp;&nbsp;`M1_new() -> ();`<br>&nbsp;&nbsp;`M2() -> ();`<br>`};`  *`Protocol P {`[Selector =“ M1”]`<br> nbsp;`M1 New（）->（）;`<br> nbsp;`M2（ ）->（）;`<br>`};`

![red x](rx.png) **Transition Considerations**: NO  ！[red x]（rx.png）**转换注意事项**：否

 
#### Adding members  新增成员 

```fidl
protocol P {       protocol P {
  M1() -> ();        M1() -> ();
  M2() -> ();        M2() -> ();
                     M3() -> ();
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![green checkmark](gc.png) **Transition Considerations**: YES  ！[绿色复选标记]（gc.png）**转换注意事项**：是

 
* Add `[Transitional]` to the new member:  *在新成员中添加[[过渡]]：
  * `protocol P {`<br>&nbsp;&nbsp;`M1() -> ();`<br>&nbsp;&nbsp;`M2() -> ();`<br>&nbsp;&nbsp;`[Transitional="msg"]`<br>&nbsp;&nbsp;`M3() -> ();`<br>`}`  *`Protocol P {`nbsp;`M1（）->（）;`<br> nbsp;`M2（）->（）;`<br> nbsp; nbsp;`[Transitional =“ msg”]`<br> nbsp;`M3（）->（）;`<br>`}`
* See [FTP-021][ftp021]  *请参阅[FTP-021] [ftp021]

 
#### Removing members  删除成员 

```fidl
protocol P {       protocol P {
  M1() -> ();        M1() -> ();
  M2() -> ();
};                 };
```
 

![green checkmark](gc.png) **ABI Compatibility**: YES  ！[绿色对勾]（gc.png）** ABI兼容性**：是

![green checkmark](gc.png) **Transition Considerations**: YES  ！[绿色复选标记]（gc.png）**转换注意事项**：是

 
1. Add `[Transitional]` to `M2()`  1.在M2（）中添加[Transitional]
2. Remove references  2.删除参考
3. Delete from `.fidl`  3.从.fidl中删除

 
* See [FTP-021][ftp021]  *请参阅[FTP-021] [ftp021]

 
#### protocol method arguments & return values  协议方法参数返回值 

Follow the same rules as [structs](#structs).  遵循与[structs]（structs）相同的规则。

