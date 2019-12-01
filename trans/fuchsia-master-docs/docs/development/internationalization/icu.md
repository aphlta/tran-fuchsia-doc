 
# International Components for Unicode (ICU) use in Fuchsia  紫红色使用的Unicode国际组件（ICU） 

Fuchsia uses the [ICU library](http://site.icu-project.org/) for the commonly shared internationalization services such as date, time, timezone, locale andlanguage handling. 紫红色将[ICU库]（http://site.icu-project.org/）用于常见的共享国际化服务，例如日期，时间，时区，语言环境和语言处理。

The ICU library consists roughly of two different parts: the ICU library *code* which contains the ICU algorithms, and the ICU library *data*, which containslocale-specific information that is packaged for independent reuse. ICU库大致由两个不同部分组成：ICU库* code *包含ICU算法，ICU库* data *包含特定于语言环境的信息，这些信息打包后可以独立重用。

The code is available through appropriate shared libraries in `//third_party/icu` (see below). 可通过`// third_party / icu`中的适当共享库获得该代码（请参见下文）。

 
# Prerequisites  先决条件 

 
## `icu_data` library  `icu_data`库 

In Fuchsia, the ICU data is made available to be loaded at runtime. Please see the [ICU data use instructions](icu_data.md) on how to load this data. 在紫红色中，可以在运行时加载ICU数据。有关如何加载此数据，请参阅[ICU数据使用说明]（icu_data.md）。

 
## `icu_data` `BUILD.gn` rules need changing  需要修改icu_data`BUILD.gn`规则 

Since `icu_data` needs the ICU data files to be made available in the Fuchsia package, please see [ICU data use instructions](icu_data.md) for an exaple ofhow to make the data files available. 由于`icu_data`需要在Fuchsia软件包中提供ICU数据文件，因此请参见[ICU数据使用说明]（icu_data.md），以了解如何使数据文件可用。

 
# Using the ICU library  使用ICU库 

This section assumes that you have read and followed the instructions from the Prerequisites section in full detail. 本部分假定您已阅读并完全按照“先决条件”部分中的说明进行操作。

 
## C and C++  C和C ++ 

The ICU library is imported through a third-party dependency `//third_party/icu`. As an example use of the library, one can look at the [C++wisdom example][wisdomcpp].  This is a sample client-server collaboration thatrequests, serves and prints on screen date and time information using severaldifferent languages, calendars and scripts. ICU库是通过第三方依赖项“ // third_party / icu”导入的。作为该库的示例使用，可以查看[C ++智慧示例] [wisdomcpp]。这是示例的客户机/服务器协作，它使用几种不同的语言，日历和脚本来请求，提供服务并在屏幕上显示日期和时间信息。

 
## Rust  锈 

The ICU library is available in rust programs as well, through a binding of the ICU4C library into Rust. 通过将ICU4C库绑定到Rust，也可以在rust程序中使用ICU库。

The library is subdivided into [several crates](https://fuchsia-docs.firebaseapp.com/rust/?search=rust_icu), each onecorresponding to a specific part of the ICU4C headers, and named after thecorresponding one.  Today, the functionality is partial, and is constructed toserve Fuchsia's Unicode needs. 该库可细分为[几个板条箱]（https://fuchsia-docs.firebaseapp.com/rust/?search=rust_icu），每个库对应于ICU4C标头的特定部分，并以对应的标头命名。今天，该功能是部分功能，旨在满足Fuchsia的Unicode需求。

As a demonstration of the rust bindings for ICU4C, we made a rust equivalent of the wisdom server.  This example is available as the [rust wisdomexample][wisdomrust]. 为了说明ICU4C的锈绑定，我们制作了与智能服务器等效的锈。该示例可用作[rust智慧示例] [wisdomrust]。

