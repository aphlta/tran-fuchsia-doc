 
# [Dockyard](README.md)  [船坞]（README.md） 

 
## Terms  条款 

This is an alphabetical glossary of terms related to the Dockyard.  这是与Dockyard相关的术语的字母顺序词汇表。

 
##### Dockyard ID  船坞IDA number used to uniquely refer to a Sample Stream or other named entity. The Dockyard ID is 1:1 with a specific Dockyard Path. 用于唯一引用样本流或其他命名实体的数字。带有特定Dockyard路径的Dockyard ID为1：1。

 
##### Dockyard Path  船坞径A UTF-8, case sensitive text string referring to a Sample Stream or other named entity. The path value is primarily used in the UI, internally the Dockyard IDis used. E.g. "cpu:0", "physMem", "procCount" are Dockyard Paths. 一个UTF-8，区分大小写的文本字符串，引用一个示例流或其他命名实体。路径值主要在UI中使用，内部使用Dockyard ID。例如。 “ cpu：0”，“ physMem”，“ procCount”是船坞路径。

 
##### Normalize  归一化A graph rendering filter. Scales the graph output so that the high and low values are framed nicely onthe screen. The data is scaled dynamically. 图形渲染过滤器。缩放图形输出，以便在屏幕上很好地构筑高值和低值。数据是动态缩放的。

 
##### Sample  样品A sample is a piece of data from the device. A Sample has a time (when it was gathered), a path (like a name), and a value. E.g. Sample z: (<time T>,"memory:used", 300000). 样本是来自设备的一条数据。样本具有时间（收集时），路径（如名称）和值。例如。样本z：（<时间T>，“存储器：已使用”，300000）。

 
##### Sample Category  样品类别The named idea of where Samples come from. E.g. "cpu", "memory", "process" are Sample Categories. 样本来自何处的命名概念。例如。 “ cpu”，“内存”，“过程”是示例类别。

 
##### Sample Set  样本集A portion of a Sample Stream. E.g. a Sample Stream might have 100,000 Samples and a Sample Set might only consist of 1,200 of those Samples. 样本流的一部分。例如。一个样本流可能有100,000个样本，而一个样本集可能只包含1200个样本。

 
##### Sample Stream Request  样本流请求A request for samples sent to the dockyard. It specifies the time range, sample streams, and filtering desired. 将样品请求发送到船坞。它指定时间范围，样本流和所需的过滤。

 
##### Sample Stream Response  样本流响应A message sent from the dockyard in response to a Sample Stream Request. It includes the filtered sample data (a Sample Set) for each of the requestedSample Streams. A filtered sample is a mathematically generated representationof 0 to many samples. 从船坞发送的一条消息，以响应“样本流请求”。它包括每个请求的样本流的过滤后的样本数据（样本集）。过滤后的样本是数学生成的0到许多样本的表示形式。

Example 1: a filtered sample might have the value 900 if filter was averaging samples of 700, 800, 1000, and 1100. Note that the filtered sample doesn't matchany of the actual samples in this example. 示例1：如果过滤器对700、800、1000和1100的样本进行平均，则过滤后的样本的值可能为900。请注意，此示例中过滤后的样本与任何实际样本都不匹配。

Example 2: when rendering 3 columns on the screen for 12 Samples, each filtered sample will be computed from 4 Samples. 示例2：在屏幕上为12个样本渲染3列时，将从4个样本中计算出每个过滤后的样本。

 
##### Sample Stream  样本流An ordered set of Samples for a given Sample Category. E.g. all the Samples for "cpu0". 给定样本类别的一组有序样本。例如。 “ cpu0”的所有样本。

 
##### Smooth  光滑A graph rendering filter that blends neighboring samples. The resulting graph will have have less dramatic highs and lows (i.e. with less noise). 混合相邻样本的图形渲染过滤器。生成的图形将具有较小的高低波动（即噪声较小）。

