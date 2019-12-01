 
# ACPI debugging  ACPI调试 

 
## ACPICA debug interfaces  ACPICA调试接口 

To turn on ACPICA's debug output, pass the "enable_acpi_debug = true" build argument to GN.  When this option is enabled, ACPICA uses two global variablesto control debug output. 要打开ACPICA的调试输出，请将“ enable_acpi_debug = true”构建参数传递给GN。启用此选项后，ACPICA使用两个全局变量来控制调试输出。

 
### AcpiDbgLevel  AcpiDbgLevel 

AcpiDbgLevel is a bitmap of values defined in third\_party/lib/acpica/source/include/acpica/acoutput.h with the prefix"ACPI\_LV\_".  For convenience, there are some pre-defined verbosity levels:ACPI\_LV\_VERBOSITY1, ACPI\_LV\_VERBOSITY2, ACPI\_LV\_VERBOSITY3.  These controltypes of tracing events to log.  For example, if you want to trace all functioncalls and mutex operations, you can set AcpiDbgLevel to AcpiDbgLevel是在Third \ _party / lib / acpica / source / include / acpica / acoutput.h中定义的值的位图，前缀为“ ACPI \ _LV \ _”。为方便起见，有一些预定义的详细级别：ACPI \ _LV \ _VERBOSITY1，ACPI \ _LV \ _VERBOSITY2，ACPI \ _LV \ _VERBOSITY3。这些控件类型的跟踪事件进行记录。例如，如果要跟踪所有函数调用和互斥操作，可以将AcpiDbgLevel设置为

"ACPI\_LV\_FUNCTIONS | ACPI\_LV\_MUTEX"  “ ACPI \ _LV \ _FUNCTIONS | ACPI \ _LV \ _MUTEX”

 
### AcpiDbgLayer  AcpiDbgLayer 

AcpiDbgLayer is a bitmap of values defined in third\_party/lib/acpica/source/include/acpica/acoutput.h.  These do not have acommon prefix, but are listed as "Component IDs".  These control whichsubmodules of ACPICA are to be traced.  For example, to trace through thenamespace logic and the executor, you can set AcpiDbgLayer to AcpiDbgLayer是在third \ _party / lib / acpica / source / include / acpica / acoutput.h中定义的值的位图。这些没有通用前缀，但列为“组件ID”。这些控制将跟踪ACPICA的哪些子模块。例如，要跟踪命名空间逻辑和执行程序，可以将AcpiDbgLayer设置为

"ACPI\_NAMESPACE | ACPI\_EXECUTOR"  “ ACPI \ _NAMESPACE | ACPI \ _EXECUTOR”

 
### Setting these values  设定这些值 

One easy place to set these in the AcpiOsInitialize method that we define in third\_party/lib/acpica/source/os\_specific/service\_layers/osfuchsia.cpp.One technique that may be useful is zeroing both values in AcpiOsInitialize, andsetting it to a non-zero value immediate before a call into ACPICA of interest. 在我们在third \ _party / lib / acpica / source / os \ _specific / service \ _layers / osfuchsia.cpp中定义的AcpiOsInitialize方法中设置这些值的一个简单地方。一种有用的技术是将AcpiOsInitialize中的两个值都置零，然后设置在致电感兴趣的ACPICA之前，将其设置为非零值。

 
### AcpiDebugTrace  AcpiDebugTrace 

