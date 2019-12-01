 
# Zircon and LK  锆石和LK 

Zircon was born as a branch of [LK](https://github.com/littlekernel/lk) and even now many inner constructs are based on LK while the layers above are new. Forexample, Zircon has the concept of a process but LK does not. However, a Zirconprocess is made of LK-level constructs such as LK's ``thread_t``. Zircon诞生于[LK]（https://github.com/littlekernel/lk）的一个分支，即使现在，许多内部构造都基于LK，而上面的层是新的。例如，Zircon具有过程的概念，而LK没有。但是，Zirconprocess由LK级别的结构（例如LK的``thread_t''）制成。

LK is a Kernel designed for small systems typically used in embedded applications. It is a good alternative to commercial offerings like[FreeRTOS](http://www.freertos.org/) or [ThreadX](http://rtos.com/products/threadx/).Such systems often have a very limited amount of ram, a fixed set of peripheralsand a bounded set of tasks. LK是为嵌入式系统中通常使用的小型系统设计的内核。它是[FreeRTOS]（http://www.freertos.org/）或[ThreadX]（http://rtos.com/products/threadx/）等商业产品的不错选择。此类系统通常非常有限数量的ram，一组固定的外围设备和一组有限的任务。

On the other hand, Zircon targets modern phones and modern personal computers with fast processors, non-trivial amounts of ram with arbitrary peripheralsdoing open ended computation. 另一方面，Zircon的目标客户是具有快速处理器的现代电话和现代个人计算机，带有不计其数的ram的任意外围设备进行开放式计算。

More specifically, some the visible differences are:  更具体地说，一些明显的区别是：

 
+ LK can run in 32-bit systems. Zircon is 64-bit only.  LK可以在32位系统中运行。 Zircon仅是64位。
+ Zircon has first class user-mode support. LK does not.  + Zircon具有一流的用户模式支持。 LK没有。
+ Zircon has a capability-based security model. In LK all code is trusted.  + Zircon具有基于功能的安全模型。在LK中，所有代码都是受信任的。

Over time, even the low level constructs have changed to accommodate the new requirements and to better fit the rest of the system. 随着时间的流逝，即使是底层结构也发生了变化，以适应新的要求并更好地适应系统的其余部分。

