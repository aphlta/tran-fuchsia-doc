 
# Zircon System Interface Rubric  Zircon系统界面规则 

The Zircon system interface is expressed as the `libzircon.so` vDSO API surface.  Zircon系统界面表示为“ libzircon.so” vDSO API表面。

Functions that are part of the interface must have names that start with `zx_` and preprocessor macros must have names that start with `ZX_`.  Types defined aspart of the interface must have names that begin with `zx_` and end with `_t`. 属于接口的函数的名称必须以“ zx_”开头，预处理器宏的名称必须以“ ZX_”开头。定义为接口一部分的类型必须具有以“ zx_”开头和以“ _t”结尾的名称。

Every function that is part of the interface must be documented with a markdown file in /docs/zircon/syscalls/ andlinked from /docs/zircon/syscalls.md . 接口的每个功能都必须在/ docs / zircon / syscalls /中用markdown文件记录下来，并从/docs/zircon/syscalls.md中链接。

 
## Function Names  功能名称 

Functions must have names consisting entirely of lowercase letters and underscores and that conform to the following grammar: 函数的名称必须完全由小写字母和下划线组成，并且符合以下语法：

```
zx_<noun>_<verb>{_<direct-object>}
```
 

For example:  例如：

```
zx_handle_close, zx_channel_write, zx_object_signal_peer
```
 

Typically, the noun is a kernel object type but can be other nouns, such as `clock` or `ticks` for which there is no corresponding kernel object. Otherfunctions use more abstract nouns, such as `system` or `status`. 通常，名词是内核对象类型，但也可以是其他名词，例如没有相应内核对象的“ clock”或“ ticks”。其他功能使用更抽象的名词，例如“ system”或“ status”。

The nouns and verbs must not contain underscores (to avoid confusing the grammar). The noun and verb should each be single English words but acronyms (orabbreviations) may be used if there is no suitable word or the word is too long. 名词和动词一定不能包含下划线（以避免混淆语法）。名词和动词应均为单个英语单词，但如果没有合适的单词或单词太长，则可以使用首字母缩写词（或缩写）。

The direct object may contain underscores.  直接对象可能包含下划线。

Some functions perform composite operations. In such cases, the function may be named by concatenating the names of the component operations. 一些功能执行复合操作。在这种情况下，可以通过串联组件操作的名称来命名函数。

Some functions operate on several types of kernel object, in which case the noun is a more abstract object type. For example, functions with the noun `object`operate on most kernel objects and functions with the noun `task` operate onjobs, processes, and threads. 一些函数对几种类型的内核对象进行操作，在这种情况下，名词是一种更抽象的对象类型。例如，名词“ object”的函数在大多数内核对象上运行，而名词“ task”的函数在作业，进程和线程上运行。

 
## Types  种类 

Use `zx_status_t` to represent success and failure.  使用`zx_status_t`表示成功和失败。

Use fixed-size integer types. Functions must not use `short`, `int`, or `unsigned long` (or similar types). Instead, use types such as `int16_t`,`int32_t`, and `uint64_t`. 使用固定大小的整数类型。函数不得使用“ short”，“ int”或“ unsigned long”（或类似类型）。相反，请使用诸如int16_t，int32_t和uint64_t之类的类型。

Use `size_t` for buffer lengths, element sizes, and element counts.  使用`size_t`表示缓冲区的长度，元素大小和元素计数。

Use `void*` for pointers to arbitrary types in the caller's address space. Use `zx_vaddr_t` / `zx_paddr_t` for addresses that might be in other address spaces. 使用“ void *”来指向调用者地址空间中任意类型的指针。将`zx_vaddr_t` /`zx_paddr_t`用于可能在其他地址空间中的地址。

Use `zx_time_t` for timeouts, which must be expressed as absolute deadlines in nanoseconds in the `ZX_CLOCK_MONOTONIC` timebase. In scenarios where absolutedeadlines do not make sense (for example, timer slack), use `zx_duration_t` torepresent an amount of time in nanoseconds with no specific timebase. 使用`zx_time_t`表示超时，它必须表示为`ZX_CLOCK_MONOTONIC`时基中的绝对期限（以纳秒为单位）。在绝对期限没有意义的情况下（例如，计时器松弛），请使用zx_duration_t来表示无特定时基的时间（以纳秒为单位）。

 
## Parameters  参量 

 
### Receiver  接收者 

The vast majority of functions act on a handle, which is a reference to a kernel object of a type matching the *noun* in the function name. This handle is thefirst argument to such functions and is referred to as the receiver. 绝大多数函数作用在句柄上，句柄是对与函数名称中的* noun *匹配的类型的内核对象的引用。该句柄是此类函数的第一个参数，被称为接收器。

Use the name `handle` for the receiver.  接收器使用名称“ handle”。

Object creation functions (eg, `zx_channel_create`, `zx_event_create`) may not take a handle argument. These functions implicitly operate on the currentprocess. 对象创建函数（例如zx_channel_create，zxevent_create）可能不带有handle参数。这些函数隐式地在当前进程上运行。

 
### Options Parameter  选项参数 

Often functions include an `options` parameter to allow for flags which affect the operation, and include room for further flags being added to futurerevisions of the API. 通常，函数包含一个“ options”参数，以允许影响操作的标志，并包括为将来的API版本添加更多标志的空间。

Use the type `uint32_t` and the name `options` for the `options` parameter.  将`uint32_t`类型和`options`名称用作`options`参数。

When present, an `options` parameter must be the first argument after the receiver handle or the first argument overall if the function does not have areceiver. 如果存在，则“ options”参数必须是接收器句柄之后的第一个参数，或者，如果函数没有接收器，则必须是整体上的第一个参数。

An `options` parameter is not required for all functions.  并非所有功能都需要一个`options'参数。

Individual option values must be defined as preprocessor macros that cast a numeric literal to `uint32_t`. The options must be bit flags that can becombined using the bitwise `|` operator. 必须将各个选项值定义为将数字文字转换为uint32_t的预处理器宏。选项必须是可以使用按位||运算符组合的位标志。

 
### Handles  提手 

When a function is given a handle as a parameter, the function must either always consume the handle or never consume, with the following exceptions: 当为函数提供一个句柄作为参数时，该函数必须始终使用该句柄或从不使用该句柄，但以下情况除外：

 
 * If the function takes an `options` parameter, the function may have a non-default option to avoid consuming handles in various error conditions. *如果该函数采用“ options”参数，则该函数可能具有非默认选项，以避免在各种错误情况下使用句柄。

 
 * If the function does not take an `options` parameter, the function may avoid consuming handles if/when it returns `ZX_ERR_SHOULD_WAIT`. *如果该函数未使用“ options”参数，则当/返回ZX_ERR_SHOULD_WAIT时，该函数可以避免使用句柄。

 
### Buffers with Data, Count/Size, and/or Actual  具有数据，计数/大小和/或实际值的缓冲区 

Always accompany arrays or buffers with a count or size (of type `size_t`), including strings. If the buffer is written by the function, the function musthave an out parameter that returns the count or size of the data written. 数组或缓冲区始终与计数或大小（大小为“ size_t”类型）一起使用，包括字符串。如果缓冲区是由函数写入的，则函数必须具有out参数，该参数返回写入数据的计数或大小。

For read and write style operations, the pointer(s) to the buffer(s) are followed by the buffer count(s) or size(s), and if a short read or write ispossible, an out parameter provides the actual count(s) or size(s) on success: 对于读取和写入样式操作，指向缓冲区的指针后跟缓冲区计数或大小，如果可能进行简短的读取或写入，则out参数将提供实际计数（或成功的大小：

```
zx_status_t zx_socket_write(zx_handle_t handle, uint32_t options,
                            const void* buffer, size_t size, size_t* actual);
```
 

When there are multiple buffers, the buffers, lengths, and out parameters appear interleaved in a consistent order. For example, see `zx_channel_read`: 当有多个缓冲区时，缓冲区，长度和out参数以一致的顺序交错显示。例如，参见`zx_channel_read`：

```
zx_status_t zx_channel_read(zx_handle_t handle, uint32_t options,
                            void* bytes, zx_handle_t* handles,
                            uint32_t num_bytes, uint32_t num_handles,
                            uint32_t* actual_bytes, uint32_t* actual_handles);
```
 

 
### Outputs  产出 

An out parameter is a scalar value written by the function. For example, a function that returns the number of CPUs by writing to a `uint32_t` has an outparameter. If the function populates a buffer provided by the client, the bufferisn’t an out parameter. out参数是函数写入的标量值。例如，通过写入uint32_t返回一个CPU数量的函数具有一个参数。如果该函数填充了客户端提供的缓冲区，则该缓冲区不是out参数。

Out parameters always come at the end of the parameter list.  输出参数始终位于参数列表的末尾。

An out parameter must not also be an in parameter. For example, if a function has an out parameter through which it returns the number of bytes written to abuffer, that parameter must not also be used by the function to receive thelength of the buffer from the caller. out参数也不能是in参数。例如，如果函数具有out参数，通过该参数返回写入缓冲区的字节数，则该函数也不能使用该参数从调用方接收缓冲区的长度。

 
## Return Type  返回类型 

The vast majority of functions have a return type of `zx_status_t`, which is `ZX_OK` on success and `ZX_ERR_...` on failure. 绝大多数函数的返回类型为zx_status_t，成功时为ZX_OK，失败时为ZX_ERR _...。

Do not return other values through `zx_status_t`, for example using the positive value range. Instead, use an out parameter. 不要通过`zx_status_t`返回其他值，例如使用正值范围。而是使用out参数。

Other return types may be used for functions that cannot fail. For example, `zx_thread_exit` never fails to exit the thread and has a return type of void.Similarly, `zx_clock_get` cannot fail to get the current time and has a returntype of `zx_time_t`. 其他返回类型可以用于不能失败的函数。例如，`zx_thread_exit`永远不会退出线程并且返回类型为void。类似地，`zx_clock_get`不会失败获取当前时间并且返回类型为`zx_time_t`。

 
## Function-specific rules  功能特定的规则 

 
### zx_object_get_property versus zx_object_get_info  zx_object_get_property与zx_object_get_info 

