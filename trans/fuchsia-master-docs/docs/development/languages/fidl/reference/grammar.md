 
# Grammar  语法 

 
## Modified BNF rules  修改后的BNF规则 

This is the grammar for FIDL source files. The grammar is expressed in a modified BNF format. 这是FIDL源文件的语法。语法以修改后的BNF格式表示。

A nonterminal symbol matches a sequence of other symbols, delimited by commas. 非终结符与以逗号分隔的其他符号序列匹配。

```
nonterminal = list , of , symbols ;
```
 

Some symbols are terminals, which are either in all caps or are in double quotes. 一些符号是终端，要么全部大写，要么用双引号引起来。

```
another-nonterminal = THESE , ARE , TERMINALS , AND , SO , IS , "this" ;
```
 

Alternation is expressed with a pipe.  替换用管道表示。

```
choice = this | that | the-other ;
```
 

An option (zero or one) is expressed with parentheses.  选项（零或一）用括号表示。

```
optional = ( maybe , these ) , but , definitely , these ;
```
 

Repetition (zero or more) is expressed with parentheses and a star.  重复（零个或多个）用括号和星号表示。

```
zero-or-more = ( list-part )* ;
```
 

Repetition (one or more) is expressed with parentheses and a plus.  重复（一个或多个）用括号和加号表示。

```
one-or-more = ( list-part )+ ;

```
 

 
## Tokens  代币 

Whitespace and comments are ignored during lexing, and thus not present in the following grammar. Comments are C++-style `//` untilthe end of the line. 空格和注释在词法分析过程中被忽略，因此在以下语法中不存在。注释是C ++样式的“ //”，直到行尾为止。

TODO(US-238): Eventually comments will be read as part of a documentation generation system. TODO（US-238）：最终，注释将作为文档生成系统的一部分被读取。

 
## The grammar  语法 

`file` is the starting symbol.  文件是起始符号。

```
file = library-header , ( using-list ) , declaration-list ;

library-header = ( attribute-list ) , "library" , compound-identifier , ";" ;

using-list = ( using , ";" )* ;

using = "using" , compound-identifier , ( "as" , IDENTIFIER ) ;

declaration-list = ( declaration , ";" )* ;

compound-identifier = IDENTIFIER ( "." , IDENTIFIER )* ;

declaration = bits-declaration | const-declaration | enum-declaration | protocol-declaration
            | struct-declaration | table-declaration | union-declaration | xunion-declaration
            | type-alias-declaration | service-declaration ;

const-declaration = ( attribute-list ) , "const" , type-constructor , IDENTIFIER , "=" , constant ;

enum-declaration = ( attribute-list ) , ( "strict" ) , "enum" , IDENTIFIER , ( ":" , type-constructor ) ,
                   "{" , ( bits-or-enum-member , ";" )+ , "}" ; [NOTE 1]

bits-declaration = ( attribute-list ) , ( "strict" ) , "bits" , IDENTIFIER , ( ":" , type-constructor ) ,
                   "{" , ( bits-or-enum-member , ";" )+ , "}" ; [NOTE 2]

bits-or-enum-member = ( attribute-list ) , IDENTIFIER , "=" , bits-or-enum-member-value ;

bits-or-enum-member-value = IDENTIFIER | literal ; [NOTE 3]

protocol-declaration = ( attribute-list ) , "protocol" , IDENTIFIER ,
                       "{" , ( protocol-member , ";" )*  , "}" ;

protocol-member = protocol-method | protocol-event | protocol-compose ;

protocol-method = ( attribute-list ) , IDENTIFIER , parameter-list,
                  ( "->" , parameter-list , ( "error" type-constructor ) ) ; [NOTE 4]

protocol-event = ( attribute-list ) , "->" , IDENTIFIER , parameter-list ;

parameter-list = "(" , ( parameter ( "," , parameter )+ ) , ")" ;

parameter = type-constructor , IDENTIFIER ;

protocol-compose = "compose" , compound-identifier ;

struct-declaration = ( attribute-list ) , "struct" , IDENTIFIER , "{" , ( struct-field , ";" )* , "}" ;

struct-field = ( attribute-list ) , type-constructor , IDENTIFIER , ( "=" , constant ) ;

union-declaration = ( attribute-list ) , "union" , IDENTIFIER , "{" , ( union-field , ";" )+ , "}" ;

xunion-declaration = ( attribute-list ) , ( "strict" ) , "xunion" , IDENTIFIER , "{" , ( union-field , ";" )* , "}" ;

union-field = ( attribute-list ) , type-constructor , IDENTIFIER ;

table-declaration = ( attribute-list ) , ( "strict" ) , "table" , IDENTIFIER , "{" , ( table-field , ";" )* , "}" ;

table-field = ( attribute-list ) , table-field-ordinal , table-field-declaration ; [NOTE 5]

table-field-ordinal = ordinal , ":" ;

table-field-declaration = struct-field | "reserved" ;

type-alias-declaration = ( attribute-list ) , "using" , IDENTIFIER ,  "=" , type-constructor ;

service-declaration = ( attribute-list ) , "service" , IDENTIFIER , "{" , ( service-member , ";" )* , "}" ;

service-member = ( attribute-list ) , type-constructor , IDENTIFIER ; [NOTE 6]

attribute-list = "[" , attributes , "]" ;

attributes = attribute | attribute , "," , attributes ;

attribute = IDENTIFIER , ( "=" , STRING-LITERAL ) ;

type-constructor = compound-identifier ( "<" type-constructor ">" ) , (  type-constraint ) , ( "?" )
                 | handle-type ;

handle-type = "handle" , ( "<" , handle-subtype , ">" ) , ( "?" ) ;

handle-subtype = "bti" | "channel" | "debuglog" | "event" | "eventpair" | "exception"
               | "fifo" | "guest" | "interrupt" | "iommu" | "job" | "pager" | "pcidevice"
               | "pmt" | "port" | "process" | "profile" | "resource" | "socket" | "suspendtoken"
               | "thread" | "timer" | "vcpu" | "vmar" | "vmo" ;

type-constraint = ":" , constant ;

constant = compound-identifier | literal ;

ordinal = NUMERIC-LITERAL ;

literal = STRING-LITERAL | NUMERIC-LITERAL | "true" | "false" ;
```
 

----------  ----------

 
### NOTE 1  注1The `enum-declaration` allows the more liberal `type-constructor` in the grammar, but the compiler limits this to signed or unsigned integer types,see [primitives]. “枚举声明”在语法上允许使用更自由的“类型构造函数”，但是编译器将其限制为有符号或无符号整数类型，请参阅[primitives]。

 
### NOTE 2  笔记2The `bits-declaration` allows the more liberal `type-constructor` in the grammar, but the compiler limits this to unsigned integer types, see [primitives]. “位声明”在语法上允许使用更自由的“类型构造函数”，但编译器将其限制为无符号整数类型，请参见[primitives]。

 
### NOTE 3  注3The `bits-or-enum-member-value` allows the more liberal `literal` in the grammar, but the compiler limits this to:  “位或枚举成员值”允许语法上更自由的“文字”，但编译器将其限制为：

 
* A `NUMERIC-LITERAL` in the context of an `enum`;  *在“枚举”上下文中的“ NUMERIC-LITERAL”；
* A `NUMERIC-LITERAL` which must be a power of two, in the context of a `bits`.  *一个“ NUMERIC-LITERAL”，在“ bits”的上下文中必须为2的幂。

 
### NOTE 4  注4The `protocol-method` error stanza allows the more liberal `type-constructor` in the grammar, but the compiler limits this to an `int32`, `uint32`, oran enum thereof. “协议方法”错误节允许语法中使用更自由的“类型构造函数”，但编译器将其限制为“ int32”，“ uint32”或其一个枚举。

 
### NOTE 5  注5Attributes cannot be placed on a reserved member.  属性不能放在保留成员上。

 
### NOTE 6  注6The `service-member` allows the more liberal `type-constructor` in the grammar, but the compiler limits this to protocols. “服务成员”允许语法中使用更自由的“类型构造器”，但是编译器将其限制为协议。

<!-- xrefs --> [primitives]: /docs/development/languages/fidl/reference/language.md#primitives <！-外部参照-> [primitives]：/docs/development/languages/fidl/reference/language.mdprimitives

