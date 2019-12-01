 
# Syslog  系统日志 

This document explains how to use rust syslogger library.  本文档说明了如何使用rust syslogger库。

 

 
## BUILD.gn dependency  BUILD.gn依赖性 

```gn
"//garnet/public/rust/fuchsia-syslog"
```
 

 
### Initialization  初始化 

Logger can only be initialized once.  记录器只能初始化一次。

 
#### Basic initialization  基本初始化 

```rust
#[macro_use]
extern crate fuchsia_syslog as syslog;

fn main() {
    syslog::init().expect("should not fail");
}
```
 

 
#### Initialization with tags  用标签初始化 

```rust
#[macro_use]
extern crate fuchsia_syslog as syslog;

fn main() {
    syslog::init_with_tags(&["my_tags"]).expect("should not fail");
}
```
 

 
### Log messages  日志信息 

```rust
fx_log_info!("my msg: {}", 10);
fx_log_info!(tag: "tag", "my msg: {}", 10);

fx_log_err!("my msg: {}", 10);
fx_log_err!(tag: "tag", "my msg: {}", 10);

fx_log_warn!("my msg: {}", 10);
fx_log_warn!(tag: "tag", "my msg: {}", 10);

fx_vlog!(1, "my msg: {}", 10); // verbose logs
fx_vlog!(tag: "tag", 1, "my msg: {}", 10); // verbose logs
```
 

This can also be used with rust log crate  也可以与锈木箱一起使用

```rust
info!("my msg: {}", 10);
warn!("my msg: {}", 10);
error!("my msg: {}", 10);
```
 

 

 
### Reference  参考