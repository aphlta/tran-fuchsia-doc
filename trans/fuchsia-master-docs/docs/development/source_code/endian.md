 
# Fuchsia Endian Policy and Recommendations  倒挂金钟Endian政策和建议 

 
## Background  背景 

Although we only expect Fuchsia to run on little endian (LE) CPU architectures, we still need to consider big endian (BE) issues. This doc explains: 尽管我们只希望Fuchsia在小端（LE）CPU体系结构上运行，但是我们仍然需要考虑大端（BE）问题。此文档说明：

 
 * Where endian issues arise  *出现字节顺序问题
 * How to handle them  *如何处理
 * Why we made these choices  *为什么我们做出这些选择

 
## Where endian issues arise  出现字节序问题的地方 

 
### Peripheral hardware  周边硬件 

A lot of peripheral hardware defines multi-byte BE values which must be converted. 许多外围硬件定义了必须转换的多字节BE值。

 
### Legacy formats  旧版格式 

Network byte order is BE. SCSI data structures are BE. 网络字节顺序为BE。 SCSI数据结构为BE。

 
### BE CPU execution  是CPU执行 

Even if Fuchsia never runs on a BE CPU (which it might someday, at least in theory), some of our code may be ported to a BE CPU. 即使Fuchsia从未在BE CPU上运行（至少有一天至少在理论上可能如此），我们的某些代码仍可能移植到BE CPU。

Any time we define a multi-byte value, we create the possibility that another platform may want to write or read that value, and our code (which is open source) may be ported tothat platform in order to do this. 每当我们定义一个多字节值时，我们就有可能另一个平台可能要写入或读取该值，并且我们的代码（开放源代码）可能会移植到该平台上以实现此目的。

 
## How to handle endian issues in C/C++ code and docs  如何处理C / C ++代码和文档中的字节序问题 

 
### If a module is unlikely to run into any endian issues  如果模块不太可能遇到任何字节序问题 

Many modules do not need to do anything about endian issues; their data will only be interpreted by a single CPU running Fuchsia.  许多模块不需要处理字节序问题。它们的数据只能由运行紫红色的单个CPU解释。

For those which might be ported to other OS's, or whose data might be exported by any channel:  对于那些可能已移植到其他操作系统或其数据可能通过任何渠道导出的操作系统：

Suggested style in C or C++ is to add  建议使用C或C ++样式添加

```
#include <endian.h>
...
static_assert(__BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__);
```
 

either in every file, or accompanied by a comment explaining which files are not BE compatible. 在每个文件中，或附有说明哪些文件不兼容的注释。

(It's OK to not do anything, but better to make it explicit that the code is not BE compatible.) （不做任何事情是可以的，但是最好明确指出代码不兼容。）

 
### If a module must deal with endian issues  如果模块必须处理字节序问题 

In structures that are inherently endian, it's best to include macros that "convert" little-endian data to CPU endianness; this is a form ofself-documenting code. Of course big-endian data should always use the macros. 在本质上为字节序的结构中，最好包含将“字节序”数据“转换”为CPU字节序的宏。这是一种自我记录代码。当然，大端数据应该始终使用宏。

 
#### For C/C++  对于C / C ++ 

Best style is to use the LE16 .. BE64 macros from endian.h, which should be available everywhere including DDK. 最好的样式是使用来自endian.h的LE16 .. BE64宏，该宏应可在所有地方使用，包括DDK。

```
#include <endian.h>
...
hw_le_struct.int_field = LE32(program_int);
program_long =  BE64(hw_be_struct.long_field);
```
 

 
#### For Rust  防锈 

