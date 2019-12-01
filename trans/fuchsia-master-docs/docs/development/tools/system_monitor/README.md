 
# System Monitor  系统监控器 

The System Monitor is a system for displaying the vital signs of a Fuchsia device and its processes. Samples are collected for global and per-process CPU,memory usage, and process list which are relayed to the Host computer fordisplay. 系统监视器是用于显示紫红色设备及其过程的生命体征的系统。收集用于全局和每个进程的CPU，内存使用情况和进程列表的样本，这些样本将中继到主机上进行显示。

 
## Main Pieces  主要作品 

There are several pieces of the System Monitor  系统监视器有几块

 
- GUI or CLI program  -GUI或CLI程序
- [Dockyard Library](dockyard/README.md)  -[船坞库]（dockyard / README.md）
- Transport  - 运输
- [Harvester](harvester/README.md)  -[Harvester]（harvester / README.md）

 
### GUI or CLI program  GUI或CLI程序 

At the highest level, the UI displays samples collected from the Fuchsia device (in graphs or charts as appropriate), which come from the Dockyard on the Host.The GUI for the System Monitor is not included in this source directory. It isimplemented at a higher level. UI在最高级别上显示从Fuchsia设备收集的样本（适当时以图形或图表形式），这些样本来自主机上的Dockyard。系统监视器的GUI不包含在此源目录中。它是在更高层次上实现的。

 
### Transport  运输 

