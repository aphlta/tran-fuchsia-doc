 
# Avoiding a problem with the SYSRET instruction  避免SYSRET指令出现问题 

On x86-64, the kernel uses the SYSRET instruction to return from system calls.  We must be careful not to use a non-canonical return address withSYSRET, at least on Intel CPUs, because this causes the SYSRET instructionto fault in kernel mode, which is potentially unsafe.  (In contrast, on AMDCPUs, SYSRET faults in user mode when used with a non-canonical returnaddress.) 在x86-64上，内核使用SYSRET指令从系统调用中返回。我们必须小心，至少在英特尔CPU上不要对SYSRET使用非规范的返回地址，因为这会导致SYSRET指令在内核模式下发生错误，这可能是不安全的。 （相比之下，在AMDCPU上，当与非规范的返回地址一起使用时，SYSRET在用户模式下出错。）

Usually, the lowest non-negative non-canonical address is 0x0000800000000000 (== 1 << 47).  One way that a user process could cause the syscall returnaddress to be non-canonical is by mapping a 4k executable page immediatelybelow that address (at 0x00007ffffffff000), putting a SYSCALL instructionat the end of that page, and executing the SYSCALL instruction. 通常，最低的非负非规范地址是0x0000800000000000（== 1 << 47）。用户进程可能导致syscall返回地址不规范的一种方式是，将一个4k可执行页面立即映射到该地址下方（0x00007ffffffff000），将SYSCALL指令放在该页面的末尾，然后执行SYSCALL指令。

To avoid this problem:  为避免此问题：

 
* We disallow mapping a page when the virtual address of the following page will be non-canonical. *当下一页的虚拟地址不规范时，我们不允许映射页面。

 
* We disallow setting the RIP register to a non-canonical address using [`zx_thread_write_state()`] when the address would be used with SYSRET. *当该地址将与SYSRET一起使用时，我们不允许使用[`zx_thread_write_state（）`]将RIP寄存器设置为非规范地址。

For more background, see "A Stitch In Time Saves Nine: A Case Of Multiple OS Vulnerability", Rafal Wojtczuk(https://media.blackhat.com/bh-us-12/Briefings/Wojtczuk/BH_US_12_Wojtczuk_A_Stitch_In_Time_WP.pdf). 有关更多背景信息，请参见Rafal Wojtczuk（https://media.blackhat.com/bh-us-12/Briefings/Wojtczuk/BH_US_12_Wojtczuk_A_Stitch_In_Time_WP.pdf）中的“省时省力：多操作系统漏洞的情况”。

