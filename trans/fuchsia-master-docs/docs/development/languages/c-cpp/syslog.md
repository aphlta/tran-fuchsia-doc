 
# Syslog  系统日志 

This document explains how to get started with syslogger APIs.  本文档介绍了如何开始使用syslogger API。

 
## In C  在C中 

 
### BUILD.gn dependency  BUILD.gn依赖性 

```gn
//zircon/public/lib/syslog
```
 

 
### Initialization  初始化 

Logger can only be initialized once.  记录器只能初始化一次。

 
#### Basic initialization  基本初始化 

```C
#include <lib/syslog/global.h>

int main(int argc, char** argv) {
    fx_log_init();
}
```
 

 
#### Initialization with tags  用标签初始化 

```C
#include <lib/syslog/global.h>

int main(int argc, char** argv) {
    fx_logger_config_t config = {.min_severity = FX_LOG_INFO,
                                 .console_fd = -1,
                                 .log_service_channel = ZX_HANDLE_INVALID,
                                 .tags = (const char * []) {"gtag", "gtag2"},
                                 .num_tags = 2};
    fx_log_init_with_config(&config);
}
```
 

 
### Log messages  日志信息 

```C
FX_LOGF(INFO, "tag", "my msg: %d", 10);
FX_LOG(INFO, "tag", "my msg");
FX_LOGF(INFO, NULL, "my msg: %d", 10);
```
 

 
### Reference  参考 

[C APIs](/zircon/system/ulib/syslog/include/lib/syslog/global.h)  [C API]（/ zircon / system / ulib / syslog / include / lib / syslog / global.h）

 
## In C++  在C ++中 

 
### BUILD.gn dependency  BUILD.gn依赖性 

```gn
//src/lib/syslog/cpp
```
 

 
### sandboxing dependency  沙箱依赖 

```
{
    "sandbox": {
        "services": [
            "fuchsia.logger.LogSink"
        ]
    }
}
```
 

 
### Initialization  初始化 

Logger can only be initialized once.  记录器只能初始化一次。

 
#### Basic initialization  基本初始化 

```C++
#include "src/lib/syslog/cpp/logger.h"

int main(int argc, char** argv) {
    syslog::InitLogger();
}
```
 

 
#### Initialization with tags  用标签初始化 

```C++
#include "src/lib/syslog/cpp/logger.h"

int main(int argc, char** argv) {
     syslog::InitLogger({"tag1", "tag2"});
}
```
 

 
#### Initialization using command line  使用命令行初始化 

```C++
#include "src/lib/fsl/syslogger/init.h"
#include "src/lib/fxl/command_line.h"

int main(int argc, char** argv) {
    auto command_line = fxl::CommandLineFromArgcArgv(argc, argv);
    fsl::InitLoggerFromCommandLine(command_line, {"my_program"});
}
```
 

 
### Log messages  日志信息 

```C++
FX_LOGS(INFO) << "my message";
FX_LOGST(INFO, "tag") << "my message";
```
 

 
### Reference  参考 

