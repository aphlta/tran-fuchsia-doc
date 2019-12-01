 
# Harvester  收割机 

The Harvester runs on the Fuchsia device, acquiring Samples (units of introspection data) that it sends to the Host using the Transport system. TheHarvester does not store samples. 收割机在紫红色的设备上运行，获取其使用传输系统发送给主机的样本（自省数据的单位）。 TheHarvester不存储样本。

The Harvester relies on kernel APIs (to gather data) and a Transport layer (to transmit data to the Dockyard). Harvester依赖于内核API（用于收集数据）和传输层（用于将数据传输到Dockyard）。

See also: [System Monitor](../README.md)  另请参见：[系统监视器]（../ README.md）

 
## Samples  样品 

Various kinds of data are collected by the Harvester  收割机收集各种数据

 
- [CPU Samples](cpu_samples.md)  -[CPU样本]（cpu_samples.md）
- [Memory Samples](memory_samples.md)  -[内存样本]（memory_samples.md）
- [Task Samples](task_samples.md)  -[任务样本]（task_samples.md）
