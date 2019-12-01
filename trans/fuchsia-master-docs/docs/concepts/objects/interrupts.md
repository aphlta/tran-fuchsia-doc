 
# Interrupts  中断 

 
## NAME  名称 

interrupts - Usermode I/O interrupt delivery  中断-用户模式I / O中断传递

 
## SYNOPSIS  概要 

Interrupt objects allow userspace to create, signal, and wait on hardware interrupts. 中断对象允许用户空间创建，发出信号并等待硬件中断。

 
## DESCRIPTION  描述 

TODO  去做

 
## NOTES  笔记 

Interrupt Objects are private to the DDK and not generally available to userspace processes. 中断对象是DDK专用的，通常对用户空间进程不可用。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_interrupt_create()`] - Create an interrupt handle  -[`zx_interrupt_create（）`]-创建一个中断句柄
 - [`zx_interrupt_destroy()`] - Destroy an interrupt handle  -[`zx_interrupt_destroy（）`]-销毁中断句柄
 - [`zx_interrupt_bind()`] - Bind an interrupt vector to interrupt handle  -[`zx_interrupt_bind（）`]-绑定中断向量以中断句柄
 - [`zx_interrupt_wait()`] - Wait for an interrupt on an interrupt handle  -[`zx_interrupt_wait（）`]-等待中断句柄上的中断
 - [`zx_interrupt_trigger()`] - Triggers a virtual interrupt on an interrupt handle  -[`zx_interrupt_trigger（）`]-在中断句柄上触发虚拟中断
 - [`zx_interrupt_ack()`] - Acknowledge an interrupt and re-arm it  -[`zx_interrupt_ack（）`]-确认中断并重新布防

