 
# Logging  记录中 

 

It is highly recommended that you use `lib.logging` package when you want to add logging statements to your Dart package. 想要向Dart包中添加日志记录语句时，强烈建议您使用`lib.logging`包。

Include the `fuchsia_logger`, which wraps `lib.logging`, package in your BUILD.gn target as a dependency: 在BUILD.gn目标中包括包装了`lib.logging`包的`fuchsia_logger`作为依赖项：

```
deps = [
  ...
   "//topaz/public/dart/fuchsia_logger",
  ...
]
```
 

In the .cmx file the `fuchsia.logger.LogSink` needs to be added to the sandbox:  在.cmx文件中，需要将“ fuchsia.logger.LogSink”添加到沙箱中：

```
{
    "sandbox": {
        "services": [
            "fuchsia.logger.LogSink",
            ...
        ]
    }
}
```
 

 

In the main function of your Dart / Flutter app, call the `setupLogger()` function to make sure logs appear in the Fuchsia console in the desired format. 在Dart / Flutter应用程序的主要功能中，调用`setupLogger（）`函数以确保日志以所需的格式显示在Fuchsia控制台中。

```dart
import 'package:fuchsia_logger/logger.dart';

main() {
  setupLogger();
}
```
 

After setting this up, you can call one of the following log methods to add log statements to your code: 设置完成后，您可以调用以下日志方法之一，将日志语句添加到您的代码中：

```dart
import 'package:fuchsia_logger/logger.dart';


// add logging statements somewhere in your code as follows:
log.info('hello world!');
```
 

The `log` object is a [Logger][logger-doc] instance.  log对象是[Logger] [logger-doc]实例。

 

 
## Log Levels  日志级别 

The log methods are named after the supported log levels. To list the log methods in descending order of severity: 日志方法以支持的日志级别命名。要以严重性降序列出日志方法：

```dart
    log.shout()    // maps to LOG_FATAL in FXL.
    log.severe()   // maps to LOG_ERROR in FXL.
    log.warning()  // maps to LOG_WARNING in FXL.
    log.info()     // maps to LOG_INFO in FXL.
    log.fine()     // maps to VLOG(1) in FXL.
    log.finer()    // maps to VLOG(2) in FXL.
    log.finest()   // maps to VLOG(3) in FXL.
```
 

By default, all the logs of which level is INFO or higher will be shown in the console. Because of this, Dart / Flutter app developers are highly encouraged touse `log.fine()` for their typical logging statements for development purposes. 默认情况下，所有级别为INFO或更高级别的日志都将显示在控制台中。因此，强烈建议Dart / Flutter应用程序开发人员在开发过程中使用log.fine（）作为其典型的日志记录语句。

Currently, the log level should be adjusted in individual Dart apps by providing the `level` parameter in the `setupLogger()` call. For example: 当前，应该通过在setupLogger（）调用中提供level参数来调整各个Dart应用中的日志级别。例如：

```dart
setupLogger(level: Level.ALL);
```
 

will make all log statements appear in the console.  The console is visible by running [`fx syslog`][getting_logs]. 将使所有日志语句出现在控制台中。通过运行[`fx syslog`] [getting_logs]，可以看到控制台。

 

