 

 
# Profile  轮廓 

 
## NAME  名称 

profile - scheduling configuration  配置文件-调度配置

 
## SYNOPSIS  概要 

A *profile* allows a set of high level scheduling priorities to be defined and later applied to one or more threads. Each profile object defines a schedulingconfiguration (though currently only thread priority is implemented). Oncecreated, the profile can be applied to one or more threads, which will thenadopt those settings. * profile *允许定义一组高级调度优先级，然后将其应用于一个或多个线程。每个概要文件对象都定义了一个调度配置（尽管当前仅实现线程优先级）。创建配置文件后，可以将其应用于一个或多个线程，然后将采用这些设置。

 
## DESCRIPTION  描述 

Profile objects define a high level scheduling policy that can be applied to threads. For example, an "audio processing" profile could be created with a highscheduling priority, and then be applied to threads in media playback jobs.Alternatively, a "background" profile could be created with a low schedulingpriority, and then be applied to threads in non-interactive jobs. 概要文件对象定义了可应用于线程的高级调度策略。例如，可以以高调度优先级创建“音频处理”配置文件，然后将其应用于媒体播放作业中的线程。或者，可以以低调度优先级创建“背景”配置文件，然后将其应用于应用程序中的线程。非交互式工作。

Policy objects are created with the [`zx_profile_create()`] syscall, passing in a scheduling configuration. The returned profile may then be applied to one ormore threads using the [`zx_object_set_profile()`] syscall. 策略对象是通过[`zx_profile_create（）`）系统调用创建的，传入调度配置。然后可以使用[`zx_object_set_profile（）`]系统调用将返回的配置文件应用于一个或多个线程。

Because profiles give significant control of the behaviour of the [kernel scheduler](/docs/concepts/kernel/kernel_scheduling.md), creating a profile requires the rootresource. Once created, profiles may be delegated freely, however. 因为配置文件对[内核调度程序]（/ docs / concepts / kernel / kernel_scheduling.md）的行为提供了重要控制，所以创建配置文件需要rootresource。创建配置文件后，即可自由委派。

Currently, only a single scheduler parameter `scheduler.priority` is supported, which determines the priority of the thread used by Zircon's [kernelscheduler](/docs/concepts/kernel/kernel_scheduling.md). [`zx_profile_create()`] describes how toconstruct a profile object with a custom scheduler priority. 当前，仅支持单个调度程序参数“ scheduler.priority”，该参数确定Zircon的[kernelscheduler]（/ docs / concepts / kernel / kernel_scheduling.md）使用的线程的优先级。 [`zx_profile_create（）`]描述了如何使用自定义调度程序优先级构造配置文件对象。

 
## SYSCALLS  SYSCALLS 

 
 - [`zx_profile_create()`] - create a new profile object  -[`zx_profile_create（）`]-创建一个新的配置文件对象
 - [`zx_object_set_profile()`] - apply a profile to a thread  -[`zx_object_set_profile（）`]-将配置文件应用于线程

