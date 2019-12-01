 
# Zircon System Calls  锆石系统调用 

 
## Handles  提手 
+ [handle_close](handle_close.md) - close a handle  + [handle_close]（handle_close.md）-关闭手柄
+ [handle_close_many](handle_close_many.md) - close several handles  + [handle_close_many]（handle_close_many.md）-关闭多个句柄
+ [handle_duplicate](handle_duplicate.md) - create a duplicate handle (optionally with reduced rights)  + [handle_duplicate]（handle_duplicate.md）-创建重复的句柄（可以选择减少权限）
+ [handle_replace](handle_replace.md) - create a new handle (optionally with reduced rights) and destroy the old one  + [handle_replace]（handle_replace.md）-创建一个新的句柄（可选地，减少权限）并销毁旧的句柄

 
## Objects  对象 
+ [object_get_child](object_get_child.md) - find the child of an object by its koid  + [object_get_child]（object_get_child.md）-通过对象的类别查找对象的子对象
+ [object_get_info](object_get_info.md) - obtain information about an object  + [object_get_info]（object_get_info.md）-获取有关对象的信息
+ [object_get_property](object_get_property.md) - read an object property  + [object_get_property]（object_get_property.md）-读取对象属性
+ [object_set_profile](object_set_profile.md) - apply a profile to a thread  + [object_set_profile]（object_set_profile.md）-将配置文件应用于线程
+ [object_set_property](object_set_property.md) - modify an object property  + [object_set_property]（object_set_property.md）-修改对象属性
+ [object_signal](object_signal.md) - set or clear the user signals on an object  + [object_signal]（object_signal.md）-设置或清除对象上的用户信号
+ [object_signal_peer](object_signal_peer.md) - set or clear the user signals in the opposite end  + [object_signal_peer]（object_signal_peer.md）-设置或清除另一端的用户信号
+ [object_wait_many](object_wait_many.md) - wait for signals on multiple objects  + [object_wait_many]（object_wait_many.md）-等待多个对象上的信号
+ [object_wait_one](object_wait_one.md) - wait for signals on one object  + [object_wait_one]（object_wait_one.md）-等待一个对象上的信号
+ [object_wait_async](object_wait_async.md) - asynchronous notifications on signal change  + [object_wait_async]（object_wait_async.md）-信号更改的异步通知

 
## Threads  线程数 
+ [thread_create](thread_create.md) - create a new thread within a process  + [thread_create]（thread_create.md）-在进程内创建新线程
+ [thread_exit](thread_exit.md) - exit the current thread  + [thread_exit]（thread_exit.md）-退出当前线程
+ [thread_read_state](thread_read_state.md) - read register state from a thread  + [thread_read_state]（thread_read_state.md）-从线程读取寄存器状态
+ [thread_start](thread_start.md) - cause a new thread to start executing  + [thread_start]（thread_start.md）-使新线程开始执行
+ [thread_write_state](thread_write_state.md) - modify register state of a thread  + [thread_write_state]（thread_write_state.md）-修改线程的寄存器状态

 
## Processes  工艺流程 
+ [process_create](process_create.md) - create a new process within a job  + [process_create]（process_create.md）-在工作中创建新流程
+ [process_read_memory](process_read_memory.md) - read from a process's address space  + [process_read_memory]（process_read_memory.md）-从进程的地址空间读取
+ [process_start](process_start.md) - cause a new process to start executing  + [process_start]（process_start.md）-使新进程开始执行
+ [process_write_memory](process_write_memory.md) - write to a process's address space  + [process_write_memory]（process_write_memory.md）-写入进程的地址空间
+ [process_exit](process_exit.md) - exit the current process  + [process_exit]（process_exit.md）-退出当前进程

 
## Jobs  职位 
+ [job_create](job_create.md) - create a new job within a job  + [job_create]（job_create.md）-在工作中创建新工作
+ [job_set_policy](job_set_policy.md) - modify policies for a job and its descendants  + [job_set_policy]（job_set_policy.md）-修改工作及其后代的策略

 
## Tasks (Thread, Process, or Job)  任务（线程，进程或作业） 
+ [task_create_exception_channel](task_create_exception_channel.md) - create an exception channel on a task  + [task_create_exception_channel]（task_create_exception_channel.md）-在任务上创建异常通道
+ [task_kill](task_kill.md) - cause a task to stop running  + [task_kill]（task_kill.md）-导致任务停止运行
+ [task_suspend](task_suspend.md) - cause a task to be suspended  + [task_suspend]（task_suspend.md）-导致任务被挂起

 
## Profiles  个人资料 
+ [profile_create](profile_create.md) - create a new profile object  + [profile_create]（profile_create.md）-创建一个新的配置文件对象

 
## Exceptions  例外情况 
+ [exception_get_thread](exception_get_thread.md) - create a handle for the exception thread  + [exception_get_thread]（exception_get_thread.md）-为异常线程创建一个句柄
+ [exception_get_process](exception_get_process.md) - create a handle for the exception process  + [exception_get_process]（exception_get_process.md）-为异常过程创建一个句柄

 
## Channels  频道 
+ [channel_call](channel_call.md) - synchronously send a message and receive a reply  + [channel_call]（channel_call.md）-同步发送消息并接收回复
+ [channel_create](channel_create.md) - create a new channel  + [channel_create]（channel_create.md）-创建一个新频道
+ [channel_read](channel_read.md) - receive a message from a channel  + [channel_read]（channel_read.md）-接收来自频道的消息
+ [channel_read_etc](channel_read_etc.md) - receive a message from a channel with handle information  + [channel_read_etc]（channel_read_etc.md）-从带有句柄信息的频道接收消息
+ [channel_write](channel_write.md) - write a message to a channel  + [channel_write]（channel_write.md）-将消息写入通道
+ [channel_write_etc](channel_write_etc.md) - write a message to the channel and modify the handles.  + [channel_write_etc]（channel_write_etc.md）-将消息写入通道并修改句柄。

 
## Sockets  插座 
+ [socket_create](socket_create.md) - create a new socket  + [socket_create]（socket_create.md）-创建一个新的套接字
+ [socket_read](socket_read.md) - read data from a socket  + [socket_read]（socket_read.md）-从套接字读取数据
+ [socket_shutdown](socket_shutdown.md) - prevent reading or writing  + [socket_shutdown]（socket_shutdown.md）-防止读写
+ [socket_write](socket_write.md) - write data to a socket  + [socket_write]（socket_write.md）-将数据​​写入套接字

 
## Fifos  菲佛斯 
+ [fifo_create](fifo_create.md) - create a new fifo  + [fifo_create]（fifo_create.md）-创建一个新的fifo
+ [fifo_read](fifo_read.md) - read data from a fifo  + [fifo_read]（fifo_read.md）-从fifo读取数据
+ [fifo_write](fifo_write.md) - write data to a fifo  + [fifo_write]（fifo_write.md）-将数据​​写入FIFO

 
## Events and Event Pairs  事件和事件对 
+ [event_create](event_create.md) - create an event  + [event_create]（event_create.md）-创建一个事件
+ [eventpair_create](eventpair_create.md) - create a connected pair of events  + [eventpair_create]（eventpair_create.md）-创建一对关联的事件
+ [system_get_event](system_get_event.md) - retrieve a handle to a system event  + [system_get_event]（system_get_event.md）-检索系统事件的句柄

 
## Ports  港口 
+ [port_create](port_create.md) - create a port  + [port_create]（port_create.md）-创建一个端口
+ [port_queue](port_queue.md) - send a packet to a port  + [port_queue]（port_queue.md）-将数据​​包发送到端口
+ [port_wait](port_wait.md) - wait for packets to arrive on a port  + [port_wait]（port_wait.md）-等待数据包到达端口
+ [port_cancel](port_cancel.md) - cancel notifications from async_wait  + [port_cancel]（port_cancel.md）-从async_wait取消通知

 
## Futexes  熔岩 
+ [futex_wait](futex_wait.md) - wait on a futex  + [futex_wait]（futex_wait.md）-等待一个futex
+ [futex_wake](futex_wake.md) - wake waiters on a futex  + [futex_wake]（futex_wake.md）-在futex上唤醒服务员
+ [futex_requeue](futex_requeue.md) - wake some waiters and requeue other waiters  + [futex_requeue]（futex_requeue.md）-唤醒一些服务员并重新排队其他服务员

 
## Virtual Memory Objects (VMOs)  虚拟内存对象（VMO） 
+ [vmo_create](vmo_create.md) - create a new vmo  + [vmo_create]（vmo_create.md）-创建一个新的vmo
+ [vmo_read](vmo_read.md) - read from a vmo  + [vmo_read]（vmo_read.md）-从vmo读取
+ [vmo_write](vmo_write.md) - write to a vmo  + [vmo_write]（vmo_write.md）-写入vmo
+ [vmo_create_child](vmo_create_child.md) - creates a child of a vmo  + [vmo create_child]（vmo create_child.md）-创建vmo的子级
+ [vmo_get_size](vmo_get_size.md) - obtain the size of a vmo  + [vmo_get_size]（vmo_get_size.md）-获取vmo的大小
+ [vmo_set_size](vmo_set_size.md) - adjust the size of a vmo  + [vmo_set_size]（vmo_set_size.md）-调整vmo的大小
+ [vmo_op_range](vmo_op_range.md) - perform an operation on a range of a vmo  + [vmo_op_range]（vmo_op_range.md）-在vmo的范围上执行操作
+ [vmo_replace_as_executable](vmo_replace_as_executable.md) - add execute rights to a vmo  + [vmo_replace_as_executable]（vmo_replace_as_executable.md）-向vmo添加执行权限
+ [vmo_create_physical](vmo_create_physical.md) - create a VM object referring to a specific contiguous range of physical memory  + [vmo_create_physical]（vmo_create_physical.md）-创建一个VM对象，该对象引用物理内存的特定连续范围
+ [vmo_set_cache_policy](vmo_set_cache_policy.md) - set the caching policy for pages held by a VMO  + [vmo_set_cache_policy]（vmo_set_cache_policy.md）-为VMO保留的页面设置缓存策略

 
## Virtual Memory Address Regions (VMARs)  虚拟内存地址区域（VMAR） 
+ [vmar_allocate](vmar_allocate.md) - create a new child VMAR  + [vmar_allocate]（vmar_allocate.md）-创建一个新的子VMAR
+ [vmar_map](vmar_map.md) - map a VMO into a process  + [vmar_map]（vmar_map.md）-将VMO映射到进程
+ [vmar_unmap](vmar_unmap.md) - unmap a memory region from a process  + [vmar_unmap]（vmar_unmap.md）-从进程取消映射内存区域
+ [vmar_protect](vmar_protect.md) - adjust memory access permissions  + [vmar_protect]（vmar_protect.md）-调整内存访问权限
+ [vmar_op_range](vmar_op_range.md) - perform an operation on VMOs mapped into a range of a VMAR  + [vmar_op_range]（vmar_op_range.md）-对映射到VMAR范围内的VMO执行操作
+ [vmar_destroy](vmar_destroy.md) - destroy a VMAR and all of its children  + [vmar_destroy]（vmar_destroy.md）-销毁VMAR及其所有子项

 
## Userspace Pagers  用户空间寻呼机 
+ [pager_create](pager_create.md) - create a new pager object  + [pager_create]（pager_create.md）-创建一个新的寻呼机对象
+ [pager_create_vmo](pager_create_vmo.md) - create a pager owned vmo  + [pager_create_vmo]（pager_create_vmo.md）-创建一个拥有寻呼机的vmo
+ [pager_detach_vmo](pager_detach_vmo.md) - detaches a pager from a vmo  + [pager_detach_vmo]（pager_detach_vmo.md）-从vmo分离寻呼机
+ [pager_supply_pages](pager_supply_pages.md) - supply pages into a pager owned vmo  + [pager_supply_pages]（pager_supply_pages.md）-将页面提供给拥有寻呼机的vmo

 
## Cryptographically Secure RNG  加密安全的RNG 
+ [cprng_add_entropy](cprng_add_entropy.md)  + [cprng_add_entropy]（cprng_add_entropy.md）
+ [cprng_draw](cprng_draw.md)  + [cprng_draw]（cprng_draw.md）

 
## Time  时间 
+ [nanosleep](nanosleep.md) - sleep for some number of nanoseconds  + [nanosleep]（nanosleep.md）-睡眠若干纳秒
+ [clock_get](clock_get.md) - read a system clock  + [clock_get]（clock_get.md）-读取系统时钟
+ [clock_get_monotonic](clock_get_monotonic.md) - read the monotonic system clock  + [clock_get_monotonic]（clock_get_monotonic.md）-读取单调系统时钟
+ [ticks_get](ticks_get.md) - read high-precision timer ticks  + [ticks_get]（ticks_get.md）-读取高精度计时器刻度
+ [ticks_per_second](ticks_per_second.md) - read the number of high-precision timer ticks in a second  + [ticks_per_second]（ticks_per_second.md）-每秒读取高精度计时器刻度的数量
+ [deadline_after](deadline_after.md) - Convert a time relative to now to an absolute deadline  + [deadline_after]（deadline_after.md）-将相对于现在的时间转换为绝对截止日期
+ [clock_adjust](clock_adjust.md) -   + [clock_adjust]（clock_adjust.md）-

 
## Timers  计时器 
+ [timer_create](timer_create.md) - create a timer object  + [timer_create]（timer_create.md）-创建一个计时器对象
+ [timer_set](timer_set.md) - start a timer  + [timer_set]（timer_set.md）-启动一个计时器
+ [timer_cancel](timer_cancel.md) - cancel a timer  + [timer_cancel]（timer_cancel.md）-取消计时器

 
## Hypervisor guests  系统管理程序来宾 
+ [guest_create](guest_create.md) - create a hypervisor guest  + [guest_create]（guest_create.md）-创建一个虚拟机监控程序来宾
+ [guest_set_trap](guest_set_trap.md) - set a trap in a hypervisor guest  + [guest_set_trap]（guest_set_trap.md）-在虚拟机监控程序来宾中设置陷阱

 
## Virtual CPUs  虚拟CPU 
+ [vcpu_create](vcpu_create.md) - create a virtual cpu  + [vcpu_create]（vcpu_create.md）-创建一个虚拟cpu
+ [vcpu_resume](vcpu_resume.md) - resume execution of a virtual cpu  + [vcpu resume]（vcpu resume.and）-恢复执行虚拟cpu
+ [vcpu_interrupt](vcpu_interrupt.md) - raise an interrupt on a virtual cpu  + [vcpu_interrupt]（vcpu_interrupt.md）-在虚拟CPU上引发中断
+ [vcpu_read_state](vcpu_read_state.md) - read state from a virtual cpu  + [vcpu_read_state]（vcpu_read_state.md）-从虚拟CPU读取状态
+ [vcpu_write_state](vcpu_write_state.md) - write state to a virtual cpu  + [vcpu_write_state]（vcpu_write_state.md）-将状态写入虚拟CPU
+ [interrupt_bind_vcpu](interrupt_bind_vcpu.md) - Bind an interrupt object to a VCPU  + [interrupt_bind_vcpu]（interrupt_bind_vcpu.md）-将中断对象绑定到VCPU

 
## Global system information  全局系统信息 
+ [system_get_dcache_line_size](system_get_dcache_line_size.md)  + [system_get_dcache_line_size]（system_get_dcache_line_size.md）
+ [system_get_features](system_get_features.md) - get hardware-specific features  + [system_get_features]（system_get_features.md）-获取特定于硬件的功能
+ [system_get_num_cpus](system_get_num_cpus.md) - get number of CPUs  + [system_get_num_cpus]（system_get_num_cpus.md）-获取CPU数量
+ [system_get_physmem](system_get_physmem.md) - get physical memory size  + [system_get_physmem]（system_get_physmem.md）-获取物理内存大小
+ [system_get_version](system_get_version.md) - get version string  + [system_get_version]（system_get_version.md）-获取版本字符串

 
## Debug Logging  调试日志 
+ [debuglog_create](debuglog_create.md) - create a kernel managed debuglog reader or writer  + [debuglog_create]（debuglog_create.md）-创建内核管理的调试日志读取器或写入器
+ [debuglog_write](debuglog_write.md) - write log entry to debuglog  + [debuglog_write]（debuglog_write.md）-将日志条目写入debuglog
+ [debuglog_read](debuglog_read.md) - read log entries from debuglog  + [debuglog_read]（debuglog_read.md）-从debuglog读取日志条目
+ [debug_read](debug_read.md) - TODO(fxbug.dev/32938)  + [debug_read]（debug_read.md）-TODO（fxbug.dev/32938）
+ [debug_write](debug_write.md) - TODO(fxbug.dev/32938)  + [debug_write]（debug_write.md）-TODO（fxbug.dev/32938）
+ [debug_send_command](debug_send_command.md) - TODO(fxbug.dev/32938)  + [debug_send_command]（debug_send_command.md）-待办事项（fxbug.dev/32938）

 
## Multi-function  多功能的 
+ [vmar_unmap_handle_close_thread_exit](vmar_unmap_handle_close_thread_exit.md) - three-in-one  + [vmar_unmap_handle_close_thread_exit]（vmar_unmap_handle_close_thread_exit.md）-三合一
+ [futex_wake_handle_close_thread_exit](futex_wake_handle_close_thread_exit.md) - three-in-one  + [futex_wake_handle_close_thread_exit]（futex_wake_handle_close_thread_exit.md）-三合一

 
## System  系统 
+ [system_mexec](system_mexec.md) - Soft reboot the system with a new kernel and bootimage  + [system_mexec]（system_mexec.md）-使用新的内核和引导映像软重启系统
+ [system_mexec_payload_get](system_mexec_payload_get.md) - Return a ZBI containing ZBI entries necessary to boot this system  + [system_mexec_payload_get]（system_mexec_payload_get.md）-返回一个ZBI，其中包含启动该系统所需的ZBI条目
+ [system_powerctl](system_powerctl.md)  + [system_powerctl]（system_powerctl.md）

 
## DDK  DDK 
+ [bti_create](bti_create.md) - create a new bus transaction initiator  + [bti_create]（bti_create.md）-创建一个新的总线事务启动器
+ [bti_pin](bti_pin.md) - pin pages and grant devices access to them  + [bti_pin]（bti_pin.md）-固定页面并授予设备访问权限
+ [bti_release_quarantine](bti_release_quarantine.md) - releases all quarantined PMTs  + [bti_release_quarantine]（bti_release_quarantine.md）-释放所有隔离的PMT
+ [cache_flush](cache_flush.md) - Flush CPU data and/or instruction caches  + [cache_flush]（cache_flush.md）-刷新CPU数据和/或指令缓存
+ [interrupt_ack](interrupt_ack.md) - Acknowledge an interrupt object  + [interrupt_ack]（interrupt_ack.md）-确认中断对象
+ [interrupt_bind](interrupt_bind.md) - Bind an interrupt object to a port  + [interrupt_bind]（interrupt_bind.md）-将中断对象绑定到端口
+ [interrupt_create](interrupt_create.md) - Create a physical or virtual interrupt object  + [interrupt_create]（interrupt_create.md）-创建物理或虚拟中断对象
+ [interrupt_destroy](interrupt_destroy.md) - Destroy an interrupt object  + [interrupt_destroy]（interrupt_destroy.md）-销毁一个中断对象
+ [interrupt_trigger](interrupt_trigger.md) - Trigger a virtual interrupt object  + [interrupt_trigger]（interrupt_trigger.md）-触发虚拟中断对象
+ [interrupt_wait](interrupt_wait.md) - Wait on an interrupt object  + [interrupt_wait]（interrupt_wait.md）-等待中断对象
+ [iommu_create](iommu_create.md) - create a new IOMMU object in the kernel  + [iommu_create]（iommu_create.md）-在内核中创建一个新的IOMMU对象
+ [pmt_unpin](pmt_unpin.md) - unpin pages and revoke device access to them  + [pmt_unpin]（pmt_unpin.md）-取消固定页面并撤消设备对其的访问权限
+ [resource_create](resource_create.md) - create a resource object  + [resource_create]（resource_create.md）-创建资源对象
+ [smc_call](smc_call.md) - Make an SMC call from user space  + [smc_call]（smc_call.md）-从用户空间拨打SMC

 
## Display drivers  显示驱动器 
+ [framebuffer_get_info](framebuffer_get_info.md)  + [framebuffer_get_info]（framebuffer_get_info.md）
+ [framebugger_set_range](framebuffer_set_range.md)  + [framebugger_set_range]（framebuffer_set_range.md）

 
## Tracing  追踪 
+ [ktrace_control](ktrace_control.md)  + [ktrace_control]（ktrace_control.md）
+ [ktrace_read](ktrace_read.md)  + [ktrace_read]（ktrace_read.md）
+ [ktrace_write](ktrace_write.md)  + [ktrace_write]（ktrace_write.md）
+ [mtrace_control](mtrace_control.md)  + [mtrace_control]（mtrace_control.md）

 
## Others/Work in progress  其他/进行中 
+ [ioports_release](ioports_release.md)  + [ioports_release]（ioports_release.md）
+ [pc_firmware_tables](pc_firmware_tables.md)  + [pc_firmware_tables]（pc_firmware_tables.md）
+ [pci_add_subtract_io_range](pci_add_subtract_io_range.md)  + [pci_add_subtract_io_range]（pci_add_subtract_io_range.md）
+ [pci_cfg_pio_rw](pci_cfg_pio_rw.md)  + [pci_cfg_pio_rw]（pci_cfg_pio_rw.md）
+ [pci_config_read](pci_config_read.md)  + [pci_config_read]（pci_config_read.md）
+ [pci_config_write](pci_config_write.md)  + [pci_config_write]（pci_config_write.md）
+ [pci_enable_bus_master](pci_enable_bus_master.md)  + [pci_enable_bus_master]（pci_enable_bus_master.md）
+ [pci_get_bar](pci_get_bar.md)  + [pci_get_bar]（pci_get_bar.md）
+ [pci_get_nth_device](pci_get_nth_device.md)  + [pci_get_nth_device]（pci_get_nth_device.md）
+ [pci_init](pci_init.md)  + [pci_init]（pci_init.md）
+ [pci_map_interrupt](pci_map_interrupt.md)  + [pci_map_interrupt]（pci_map_interrupt.md）
+ [pci_query_irq_mode](pci_query_irq_mode.md)  + [pci_query_irq_mode]（pci_query_irq_mode.md）
+ [pci_reset_device](pci_reset_device.md)  + [pci_reset_device]（pci_reset_device.md）
+ [pci_set_irq_mode](pci_set_irq_mode.md)  + [pci_set_irq_mode]（pci_set_irq_mode.md）

 

 
+ [syscall_test_0](syscall_test_0.md)  + [syscall_test_0]（syscall_test_0.md）
+ [syscall_test_1](syscall_test_1.md)  + [syscall_test_1]（syscall_test_1.md）
+ [syscall_test_2](syscall_test_2.md)  + [syscall_test_2]（syscall_test_2.md）
+ [syscall_test_3](syscall_test_3.md)  + [syscall_test_3]（syscall_test_3.md）
+ [syscall_test_4](syscall_test_4.md)  + [syscall_test_4]（syscall_test_4.md）
+ [syscall_test_5](syscall_test_5.md)  + [syscall_test_5]（syscall_test_5.md）
+ [syscall_test_6](syscall_test_6.md)  + [syscall_test_6]（syscall_test_6.md）
+ [syscall_test_7](syscall_test_7.md)  + [syscall_test_7]（syscall_test_7.md）
+ [syscall_test_8](syscall_test_8.md)  + [syscall_test_8]（syscall_test_8.md）
+ [syscall_test_wrapper](syscall_test_wrapper.md)  + [syscall_test_wrapper]（syscall_test_wrapper.md）
+ [syscall_test_handle_create](syscall_test_handle_create.md)  + [syscall_test_handle_create]（syscall_test_handle_create.md）

 
## Syscall generation  系统调用代 

Syscall support is generated from `//zircon/syscalls`. The FIDL files in that directory are first run through `fidlc` which produces an intermediate format.That intermediate format is consumed by [kazoo](/zircon/tools/kazoo) whichproduces output for both the kernel and userspace in a variety of languages.This output includes C or C++ headers for both the kernel and userspace, syscallentry points, other language bindings, and so on. Syscall支持来自`// zircon / syscalls`。该目录中的FIDL文件首先通过`fidlc`运行，后者会产生中间格式。[kazoo]（/ zircon / tools / kazoo）使用该中间格式，后者会以多种语言为内核和用户空间生成输出。此输出包括用于内核和用户空间的C或C ++标头，syscallentry点，其他语言绑定等。

This tool is invoked as a part of the build, rather than checking in its output.  该工具作为构建的一部分被调用，而不是检查其输出。

