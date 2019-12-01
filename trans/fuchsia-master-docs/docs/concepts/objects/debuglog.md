 
# Log  日志记录 

 
## NAME  名称 

Debuglog - Kernel debuglog  Debuglog-内核调试日志

 
## SYNOPSIS  概要 

Debuglog objects allow userspace to read and write to kernel debug logs.  Debuglog对象允许用户空间读取和写入内核调试日志。

 
## DESCRIPTION  描述 

TODO  去做

 
## NOTES  笔记 

Debuglog objects will likely cease being generally available to userspace processes in the future. 将来，Debuglog对象可能通常不再对用户空间进程可用。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_debuglog_create()`] - create a kernel managed debuglog reader or writer  -[`zx_debuglog_create（）`]-创建内核管理的调试日志读取器或写入器
 - [`zx_debuglog_write()`] - write log entry to debuglog  -[`zx_debuglog_write（）`]-将日志条目写入debuglog
 - [`zx_debuglog_read()`] - read log entries from debuglog  -[`zx_debuglog_read（）`]-从debuglog读取日志条目

