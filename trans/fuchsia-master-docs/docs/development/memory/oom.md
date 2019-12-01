 
# Out-of-memory (OOM) system  内存不足（OOM）系统 

This file contains information about the systems that watch for and respond to out-of-memory (OOM) events. 该文件包含有关监视和响应内存不足（OOM）事件的系统的信息。

[TOC]  [目录]

 
## Behavior  行为 

When the system runs out of memory and the kernel OOM thread is running, you should see a series of log messages like: 当系统内存不足并且内核OOM线程正在运行时，您应该看到一系列日志消息，例如：

```
OOM: 5915.8M free (+0B) / 8072.4M total
OOM: oom_lowmem(shortfall_bytes=524288) called
OOM: Process mapped committed bytes:
OOM:   proc  1043  397M 'bin/devmgr'
OOM:   proc  2107   88M 'devhost:pci#1:8086:1916'
OOM:   proc  1297   12M 'virtual-console'
OOM:   proc  3496   17M 'netstack'
OOM:   proc  4157  170M 'flutter:userpicker_device_shell'
OOM:   proc 28708  353M 'flutter:armadillo_user_... (+3)'
OOM:   proc 31584    9M 'dart:weather_agent'
OOM:   proc 32093   14M 'dart:mi_dashboard.dartx'
OOM: Finding a job to kill...
OOM:   (skip) job  57930 'story-8cf82cb9f742d9ecc77f1d449'
OOM:   (skip) job  37434 'story-10293ae401bc0358b3ce52d2a'
OOM:   *KILL* job  29254 'agent'
OOM:        + proc 32093  run 'dart:mi_dashboard.dartx'
OOM:        = 1 running procs (1 total), 0 jobs
OOM:   (next) job  29247 'agent'
OOM:   (next) job  29240 'agent'
OOM:   (next) job  29233 'agent'
```
 

The first line shows the current state of system memory:  第一行显示系统内存的当前状态：

```
OOM: 45.8M free (-12.4M) / 8072.4M total
```
 

The next section prints a list of processes that are consuming large amounts of memory, in no particular order: 下一部分将以不特定的顺序打印消耗大量内存的进程列表：

```
OOM: Process mapped committed bytes:
OOM:   proc  1043  397M 'bin/devmgr'
OOM:   proc  2107   88M 'devhost:pci#1:8086:1916'
OOM:   proc  1297   12M 'virtual-console'
OOM:   ...
             ^koid  ^mem
```
 

The next section shows the walk through the ranked job list, printing skipped jobs (which don't have killable process descendants), the job that will bekilled, and the next jobs on the chopping block: 下一部分显示了经过排序的作业列表，打印跳过的作业（没有可杀死的进程后代），将被杀死的作业以及砧板上的下一个作业：

```
OOM: Finding a job to kill...
OOM:   (skip) job  57930 'story-8cf82cb9f742d9ecc77f1d449'
OOM:   (skip) job  37434 'story-10293ae401bc0358b3ce52d2a'
OOM:   *KILL* job  29254 'agent'
OOM:        + proc 32093  run 'dart:mi_dashboard.dartx'
OOM:        = 1 running procs (1 total), 0 jobs
OOM:   (next) job  29247 'agent'
OOM:   (next) job  29240 'agent'
OOM:   (next) job  29233 'agent'

                   ^koid ^name
```
 

The `*KILL*` entry will also show all process descendants of the to-be-killed job. “ * KILL *”条目还将显示待杀死工作的所有进程后代。

 
## Components  组件 

 
### Kernel OOM thread  内核OOM线程 

A kernel thread that periodically checks the amount of free memory in the system, and kills a job if the free amount is too low (below the "redline"). 内核线程会定期检查系统中的可用内存量，如果可用量太低（在“红线”之下），则会终止作业。

Use `k oom info` to see the state of the OOM thread (on the kernel console):  使用`k oom info`来查看OOM线程的状态（在内核控制台上）：

```
$ k oom info
OOM info:
  running: true
  printing: false
  simulating lowmem: false
  sleep duration: 1000ms
  redline: 50M (52428800 bytes)
```
 

The redline, sleep duration, and auto-start values are controlled by `kernel.oom.*` [kernel commandline flags](/docs/reference/kernel/kernel_cmdline.md). 红线，睡眠持续时间和自动启动值由kernel.oom。* [内核命令行标志]（/ docs / reference / kernel / kernel_cmdline.md）控制。

The thread can be started with `k oom start` and stopped with `k oom stop`.  线程可以通过“ k oom start”启动，也可以通过“ k oom stop”停止。

`k oom print` will toggle a flag that prints the current free and total memory every time the thread wakes up. “ k oom print”将切换一个标志，该标志将在每次线程唤醒时打印当前的可用内存和总内存。

`k oom lowmem` will trigger a false low-memory event the next time the thread wakes up, potentially killing a job. “ k oom lowmem”将在线程下次唤醒时触发错误的低内存事件，从而有可能杀死工作。

 
### OOM-ranker driver  OOM等级驱动程序 

