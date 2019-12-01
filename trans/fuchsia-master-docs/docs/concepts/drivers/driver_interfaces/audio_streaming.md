 
# Audio Driver Streaming Interface  音频驱动程序流接口 

This document describes the audio streaming interface exposed by audio drivers in Zircon. It is meant to serve as a reference for both users anddriver-authors, and to unambiguously define the interface contract which driversmust implement and users must follow. 本文档介绍了Zircon中的音频驱动程序公开的音频流接口。它旨在为用户和驱动程序作者提供参考，并明确定义驱动程序必须实现且用户必须遵循的接口协定。

 
## Overview  总览 

Audio streams are device nodes published by driver services intended to be used by applications in order to capture or render audio on a Zircon device, or both.Each stream in the system (input or output) represents a stream of digital audioinformation which may be either received or transmitted by device. Streams aredynamic and may created or destroyed by the system at any time. Which streamsexist at any given point in time, and what controls their lifecycles areconsidered to be issues of audio policy and codec management and are notdiscussed in this document. Additionally, the information present in audiooutputs streams is exclusive to the application owner of the stream. Mixing ofaudio is not a service provided by the audio stream interface. 音频流是由驱动程序服务发布的设备节点，旨在供应用程序使用，以便在Zircon设备上捕获或呈现音频，或同时在这两者上。系统中的每个流（输入或输出）均表示数字音频信息流，可以是由设备接收或发送。流是动态的，可由系统随时创建或销毁。在任何给定的时间点存在哪些流以及控制它们的生命周期的是音频策略和编解码器管理的问题，在本文档中不会进行讨论。另外，音频输出流中存在的信息是该流的应用程序所有者专有的。音频流不是音频流接口提供的服务。

> TODO: extend this interface to support the concept of low-latency hardware > mixers. > TODO：扩展此接口以支持低延迟硬件>混音器的概念。

 
### Basic Vocabulary  基本词汇 

| Term                          | Definition                                   | | ----------------------------- | -------------------------------------------- || Sample                        | A representation of the sound rendered by a  |:                               : single speaker, or captured by a single      ::                               : microphone, at a single instant in time.     :| LPCM                          | Linear pulse code modulation. The specific   |:                               : representation of audio samples present in   ::                               : all Zircon uncompressed audio streams. LPCM  ::                               : audio samples are representations of the     ::                               : amplitude of the audio signal at an instant  ::                               : in time where the numeric values of the      ::                               : encoded audio are linearly distributed       ::                               : across the amplitude levels of the rendering ::                               : or capture device. This is in contrast to    ::                               : A-law and &mu;-law encodings which have      ::                               : non-linear mappings from numeric value to    ::                               : amplitude level.                             :| Channel                       | Within an audio stream, the subset of        |:                               : information which will be rendered by a      ::                               : single speaker, or which was captured by a   ::                               : single microphone in a stream.               :| Frame                         | A set of audio samples for every channel of  |:                               : a audio stream captured/rendered at a single ::                               : instant in time.                             :| Frame Rate                    | a.k.a. "Sample Rate". The rate (in Hz) at    |:                               : which audio frames are produced or consumed. ::                               : Common sample rates include 44.1 KHz, 48     ::                               : KHz, 96 KHz, and so on.                      :| Client or User or Application | These terms are used interchangeably in this |:                               : document. They refer to modules that use     ::                               : these interfaces to communicate with an      ::                               : audio driver/device.                         : |条款|定义| | ----------------------------- | -------------------------------------------- ||样品由|：：单个扬声器呈现的声音或由单个::：麦克风捕获的声音的表示，在单个时间点上。 ：| LPCM |线性脉冲编码调制。 | ::::: Zircon所有未压缩音频流中存在的音频样本的特定| ::表示形式。 LPCM ::：音频样本表示音频信号:::：瞬时::：的时间，其中:: ::编码音频的数值在渲染的幅度级别上呈线性分布::： ::：或捕获设备。这与::: A-law和mu; -law编码相反，后者具有从数字值到:::幅度级别的:::非线性映射。 ：|频道|在音频流中，|：：信息的子集将由::：单个扬声器呈现，或由::：单个麦克风在流中捕获。 ：|框架|：：每个通道的一组音频样本，这些音频流是在一个:::瞬时捕获/渲染的。 ：|影格速率|又称为“采样率”。 |：处产生或使用的音频帧的速率（以Hz为单位）。 ::：常见采样率包括44.1 KHz，48 ::：KHz，96 KHz等。 ：|客户或用户或应用程序|这些术语在此|：：文档中可以互换使用。它们是指使用::：这些接口与:: ::音频驱动程序/设备进行通信的模块。 ：

> TODO: do we need to extend this interface to support non-linear audio sample > encodings? This may be important for telephony oriented microphones which> deliver &mu;-law encoded samples. > TODO：我们是否需要扩展此接口以支持非线性音频样本>编码？这对于>传递μ律编码样本的面向电话的麦克风可能很重要。

 
### Basic Operation  基本操作 

Communication with an audio stream device is performed using messages sent over a [channel](/docs/concepts/objects/channel.md). Applications open the device node for astream and obtain a channel by issuing a FIDL request. After obtaining thechannel, the device node may be closed. All subsequent communication with thestream occurs using channels. 使用通过[channel]（/ docs / concepts / objects / channel.md）发送的消息执行与音频流设备的通信。应用程序打开设备节点进行流式处理，并通过发出FIDL请求获得通道。在获得信道之后，可以关闭设备节点。与流的所有后续通信都使用通道进行。

The stream channel is used for most command and control tasks, including:  流通道用于大多数命令和控制任务，包括：

 
*   Capability interrogation  *能力询问
*   Format negotiation  *格式协商
*   Hardware gain control  *硬件增益控制
*   Determining outboard latency  *确定舷外延迟
*   Plug detection notification  *插头检测通知
*   Access control capability detection and signalling  *访问控制能力检测和信令

> TODO: Should plug/unplug detection be done by sending notifications over the > stream channel (as it is today), or by publishing/unpublishing the device> nodes (and closing all channels in the case of unpublished channels)? > TODO：应该通过通过>流通道发送通知（如今天），还是通过发布/取消发布device>节点（并在未发布的情况下关闭所有通道）来完成插入/拔出检测？

In order to actually send or receive audio information on the stream, the specific format to be used must first be set. The response to a successful`SetFormat` operation will contain a new "ring-buffer" channel. The ring-bufferchannel may be used to request a shared buffer from the stream (delivered in theform of a [VMO](/docs/concepts/objects/vm_object.md)) which may be mapped into the addressspace of the application and used to send or receive audio data as appropriate.Generally, the operations conducted over the ring buffer channel include: 为了实际在流上发送或接收音频信息，必须首先设置要使用的特定格式。对SetFormat操作成功的响应将包含一个新的“ ring-buffer”通道。环形缓冲区通道可用于从流中请求共享缓冲区（以[VMO]（/ docs / concepts / objects / vm_object.md）的形式提供），该缓冲区可映射到应用程序的地址空间并用于通常，通过环形缓冲区通道进行的操作包括：

 
*   Requesting a shared buffer  *请求共享缓冲区
*   Starting and Stopping stream playback/capture  *开始和停止流播放/捕获
*   Receiving notifications of playback/capture progress  *接收播放/捕获进度的通知
*   Receiving notifications of error conditions such as HW FIFO under/overflow, bus transaction failure, etc. *接收错误条件的通知，例如硬件先入先出的下溢/溢出，总线事务失败等。
*   Receiving clock recovery information in the case that the audio output clock is based on a different oscillator than the oscillator which backs[ZX_CLOCK_MONOTONIC](/docs/reference/syscalls/clock_get.md) *在音频输出时钟基于与支持[ZX_CLOCK_MONOTONIC]（/ docs / reference / syscalls / clock_get.md）的振荡器不同的振荡器的情况下，接收时钟恢复信息

 
## Operational Details  运作细节 

 
### Protocol definition  协议定义 

In order to use the C API definitions of the [audio](/zircon/system/public/zircon/device/audio.h) protocol, applications anddrivers simply say 为了使用[audio]（/ zircon / system / public / zircon / device / audio.h）协议的C API定义，应用程序和驱动程序简单地说

```C
#include <device/audio.h>
```
 

 
### Device nodes  设备节点 

Audio stream device nodes **must** be published by drivers using the protocol preprocessor symbol given in the table below. This will cause stream devicenodes to be published in the locations given in the table. Applications canmonitor these directories in order to discover new streams as they are publishedby the drivers. 音频流设备节点必须由驱动程序使用下表中给出的协议预处理器符号发布。这将导致流devicenode在表中指定的位置中发布。应用程序可以监视这些目录，以发现驱动程序发布的新流。

Stream Type | Protocol                   | Location ----------- | -------------------------- | -----------------------Input       | `ZX_PROTOCOL_AUDIO_INPUT`  | /dev/class/audio-inputOutput      | `ZX_PROTOCOL_AUDIO_OUTPUT` | /dev/class/audio-output 流类型|协议|位置----------- | -------------------------- | -----------------------输入| ZX_PROTOCOL_AUDIO_INPUT | / dev / class / audio-inputOutput | ZX_PROTOCOL_AUDIO_OUTPUT | / dev / class / audio-output

 
### Establishing the stream channel  建立流通道 

After opening the device node, client applications may obtain a stream channel for subsequent communication using the`fuchsia.hardware.audio.Device/GetChannel` FIDL message. For example: 打开设备节点后，客户端应用程序可以使用“ fuchsia.hardware.audio.Device / GetChannel” FIDL消息获取流通道，以进行后续通信。例如：

```C
zx_handle_t OpenStream(const char* dev_node_path) {
    zx_handle_t local, remote;
    zx_status_t status = zx_channel_create(0, &local, &remote);
    if (status != ZX_OK) {
      return ZX_HANDLE_INVALID;
    }
    status = fdio_service_connect(dev_node_path, remote);
    if (status != ZX_OK) {
      LOG("Failed to open \"%s\" (res %d)\n", dev_node_path, status);
      zx_handle_close(local);
      return ZX_HANDLE_INVALID;
    }

    zx_handle_t audio_channel;
    status = fuchsia_hardware_audio_DeviceGetChannel(local, &audio_channel);
    if (status != ZX_OK) {
      printf("Failed to obtain channel (res %d)\n", status);
      return ZX_HANDLE_INVALID;
    }
    zx_handle_close(local);
    return audio_channel;
}
```
 

 
### Client side termination of the stream channel  流通道的客户端端接 

Clients **may** terminate the connection to the stream at any time simply by calling [zx_handle_close(...)](/docs/reference/syscalls/handle_close.md) on the streamchannel. Drivers **must** close any active ring-buffer channels establishedusing this stream channel and **must** make every attempt to gracefully quiesceany on-going streaming operations in the process. 客户端可以随时通过在流通道上调用[zx_handle_close（...）]（/ docs / reference / syscalls / handle_close.md）随时终止与流的连接。驱动程序必须关闭使用此流通道建立的任何活动的环形缓冲区通道，并且必须尽一切努力优雅地静默该过程中正在进行的流传输操作。

 
### Sending and receiving messages on the stream and ring-buffer channels  在流和环形缓冲区通道上发送和接收消息 

All of the messages and message payloads which may be sent or received over stream and ring buffer channels are defined in the[audio](/zircon/system/public/zircon/device/audio.h) protocol header. Messagesmay be sent to the driver using the[zx_channel_write(...)](/docs/reference/syscalls/channel_write.md) syscall. If a response isexpected, it may be read using the[zx_channel_read(...)](/docs/reference/syscalls/channel_read.md) syscall. Best practice,however, is to queue packets for your [channel(s)](/docs/concepts/objects/channel.md)[port](/docs/concepts/objects/port.md) using the[zx_port_queue(...)](/docs/reference/syscalls/port_queue.md) syscall, and use the[zx_port_wait(...)](/docs/reference/syscalls/port_wait.md) syscall to determine when your setof channels have messages (either expected responses or asynchronousnotifications) to be read. 在[音频]（/ zircon / system / public / zircon / device / audio.h）协议头中定义了可以通过流和环形缓冲区通道发送或接收的所有消息和消息有效负载。消息可以使用[zx_channel_write（...）]（/ docs / reference / syscalls / channel_write.md）系统调用发送给驱动程序。如果期望响应，则可以使用[zx_channel_read（...）]（/ docs / reference / syscalls / channel_read.md）syscall进行读取。但是，最佳实践是使用[zx_port_queue（）将[channel]（/ docs / concepts / objects / channel.md）[port]（/ docs / concepts / objects / port.md）的数据包排队。 ..）]（/ docs / reference / syscalls / port_queue.md）syscall，并使用[zx_port_wait（...）]（/ docs / reference / syscalls / port_wait.md）syscall来确定您的setof通道何时有消息（预期的响应或异步通知）被读取。

All messages either sent or received over stream and ring buffer channels are prefaced with an `audio_cmd_hdr_t` structure which contains a 32-bit transactionID and an `audio_cmd_hdr_t` enumeration value indicating the specific commandbeing requested by the application, the specific command being responded to bythe driver, or the asynchronous notification being delivered by the driver tothe application. 在流和环形缓冲区通道上发送或接收的所有消息都以“ audio_cmd_hdr_t”结构开头，该结构包含一个32位transactionID和一个“ audio_cmd_hdr_t”枚举值，该值指示应用程序所请求的特定命令，该特定命令由响应驱动程序，或由驱动程序传递给应用程序的异步通知。

When sending a command to the driver, applications **must** place a transaction ID in the header's `transaction_id` field which is not equal to`AUDIO_INVALID_TRANSACTION_ID`. If a response to a command needs to be sent bythe driver to the application, the driver **must** use the transaction ID and`audio_cmd_t` values sent by the client during the request. When sendingasynchronous notification to the application, the driver **must** use`AUDIO_INVALID_TRANSACTION_ID` as the transaction ID for the message.Transaction IDs may be used by clients for whatever purpose they desire, howeverif the IDs are kept unique across all transactions in-flight, the[zx_channel_call(...)](/docs/reference/syscalls/channel_call.md) may be used to implement asimple synchronous calling interface. 当向驱动程序发送命令时，应用程序必须将事务ID放置在标头的“ transaction_id”字段中，该字段不等于“ AUDIO_INVALID_TRANSACTION_ID”。如果驱动程序需要将对命令的响应发送到应用程序，则驱动程序必须使用请求期间客户端发送的事务ID和audio_cmd_t值。当向应用程序发送异步通知时，驱动程序必须使用AUDIO_INVALID_TRANSACTION_ID作为消息的事务ID。客户端可以出于任何目的使用事务ID，但是如果这些ID在所有事务中保持唯一，飞行中，[zx_channel_call（...）]（/ docs / reference / syscalls / channel_call.md）可用于实现简单的同步调用接口。

 
### Validation requirements  验证要求 

All drivers **must** validate requests and enforce the protocol described above. In case of any violation, drivers **should** immediately quiesce their hardwareand **must** close the channel, terminating any operations which happen to be inflight at the time. Additionally, they **may** log a message to a centrallogging service to assist in application developers in debugging the cause ofthe protocol violation. Examples of protocol violation include: 所有驱动程序都必须验证请求并执行上述协议。万一发生任何违规情况，驱动程序**应立即**静默其硬件并**必须**关闭通道，以终止当时发生的所有操作。此外，他们可以**将消息记录到中央日志记录服务中，以帮助应用程序开发人员调试引起协议违规的原因。违反协议的示例包括：

 
*   Using `AUDIO_INVALID_TRANSACTION_ID` as the value of `message.hdr.transaction_id` *使用“ AUDIO_INVALID_TRANSACTION_ID”作为“ message.hdr.transaction_id”的值
*   Using a value not present in the `audio_cmd_t` enumeration as the value of `message.hdr.cmd` *使用在audio_cmd_t枚举中不存在的值作为message.hdr.cmd的值
*   Supplying a payload whose size does not match the size of the request payload for a given command. *提供有效载荷，其大小与给定命令的请求有效载荷的大小不匹配。

 
## Format Negotiation  格式协商 

 
### Sample Formats  样本格式 

Sample formats are described using the `audio_sample_format_t` type. It is a bitfield style enumeration which describes either the numeric encoding of theuncompressed LPCM audio samples as they reside in memory, or indicating that theaudio stream consists of a compressed bitstream instead of uncompressed LPCMsamples. Refer to the [audio](/zircon/system/public/zircon/device/audio.h)protocol header for exact symbol definitions. 样本格式是使用`audio_sample_format_t`类型描述的。它是一种位域样式枚举，它描述未压缩的LPCM音频样本驻留在内存中时的数字编码，或者指示音频流由压缩的比特流而不是未压缩的LPCM样本组成。请参阅[audio]（/ zircon / system / public / zircon / device / audio.h）协议标头，以获取准确的符号定义。

The formats described by `audio_sample_format_t` have the following properties:  “ audio_sample_format_t”描述的格式具有以下属性：

 
*   With the exception of `FORMAT_BITSTREAM`, samples are always assumed to use linear PCM encoding. BITSTREAM is used for transporting compressed audioencodings (such as AC3, DTS, and so on) over a digital interconnect to adecoder device somewhere outside of the system. *除“ FORMAT_BITSTREAM”外，始终假定样本使用线性PCM编码。 BITSTREAM用于通过数字互连将压缩的音频编码（例如AC3，DTS等）传输到系统外部的adecoder设备。
*   By default, multi-byte sample formats are assumed to use host-endianness. If the `INVERT_ENDIAN` flag is set on the format, the format uses the oppositeof host endianness. eg. A 16 bit little endian PCM audio format would havethe `INVERT_ENDIAN` flag set on it in a when used on a big endian host. The`INVERT_ENDIAN` flag has no effect on COMPRESSED, 8BIT or FLOAT encodings. *默认情况下，假定多字节样本格式使用主机字节顺序。如果在格式上设置了“ INVERT_ENDIAN”标志，则该格式使用与主机字节序相反的格式。例如。当在大型endian主机上使用时，一种16位的Little Endian PCM音频格式会在上面设置“ INVERT_ENDIAN”标志。 INVERT_ENDIAN标志对COMPRESSED，8BIT或FLOAT编码无效。
*   The `32BIT_FLOAT` encoding uses specifically the [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) floating pointrepresentation. * 32BIT_FLOAT编码专门使用[IEEE 754]（https://en.wikipedia.org/wiki/IEEE_754）浮点表示。
*   By default, non-floating point PCM encodings are assumed expressed using [two's complement](https://en.wikipedia.org/wiki/Two%27s_complement) signedintegers. eg. the bit values for a 16 bit PCM sample format would range from[0x8000, 0x7FFF] with 0x0000 representing zero speaker deflection. If theUNSIGNED flag is set on the format, the bit values would range from [0x0000,0xFFFF] with 0x8000 representing zero deflection. *默认情况下，假定非浮点PCM编码使用[二进制补码]（https://en.wikipedia.org/wiki/Two%27s_complement）带符号的整数表示。例如。 16位PCM采样格式的位值范围为[0x8000，0x7FFF]，其中0x0000表示扬声器偏转为零。如果在格式上设置了UNSIGNED标志，则位值的范围为[0x0000,0xFFFF]，其中0x8000表示零偏转。
*   When used to set formats, exactly one non-flag bit **must** be set.  *当用于设置格式时，必须**设置一个非标志位。
*   When used to describe supported formats, any number of non-flag bits **may** be set. Flags (when present) apply to all of the relevant non-flag bits inthe bitfield. eg. If a stream supports BITSTREAM, 16BIT and 32BIT_FLOAT, andthe UNSIGNED bit is set, it applies only to the 16BIT format. *当用于描述支持的格式时，可以**设置任意数量的非标志位。标志（如果存在）适用于位域中的所有相关非标志位。例如。如果流支持BITSTREAM，16BIT和32BIT_FLOAT，并且UNSIGNED位置1，则它仅适用于16BIT格式。
*   When encoding a smaller sample size in a larger container (eg 20 or 24bit in 32), the most significant bits of the 32 bit container are used while theleast significant bits should be zero. eg. a 20 bit sample would be mappedonto the range [12,32] of the 32 bit container. *在较大的容器（例如20或32中的24位）中编码较小的样本大小时，将使用32位容器的最高有效位，而最低有效位应为零。例如。 20位样本将映射到32位容器的范围[12,32]。

> TODO: can we make the claim that the LSBs will be ignored, or do we have to > require that they be zero? > TODO：我们可以声称LSB将被忽略，还是必须>要求它们为零？

> TODO: describe what 20-bit packed audio looks like in memory. Does it need to > have an even number of channels in the overall format? Should we strike it> from this list if we cannot find a piece of hardware which demands this format> in memory? > TODO：描述20位压缩音频在内存中的外观。它是否需要>在整个格式中具有偶数个通道？如果我们在内存中找不到需要这种格式的硬件，我们应该从列表中删除它吗？

 
### Enumeration of supported formats  列举支持的格式 

In order to determine the formats supported by a given audio stream, applications send an `AUDIO_STREAM_CMD_GET_FORMATS` message over the streamchannel. No additional parameters are required. Drivers **must** respond to thisrequest using one or more `audio_stream_cmd_get_formats_resp_t` messages, evenif only to report that there are no formats currently supported. 为了确定给定音频流支持的格式，应用程序通过流通道发送“ AUDIO_STREAM_CMD_GET_FORMATS”消息。不需要其他参数。驱动程序“必须”使用一个或多个“ audio_stream_cmd_get_formats_resp_t”消息来响应此请求，即使仅报告当前不支持任何格式也是如此。

 
### Range structures  范围结构 

Drivers indicate support for formats by sending messages containing zero or more `audio_stream_format_range_t` structures. Each structure contains fields whichdescribe: 驱动程序通过发送包含零个或多个“ audio_stream_format_range_t”结构的消息来表示对格式的支持。每个结构都包含描述以下内容的字段：

 
*   A bitmask of supported sample formats.  *支持的样本格式的位掩码。
*   A minimum and maximum number of channels.  *最小和最大通道数。
*   A set of frame rates.  *一组帧频。

A single range structure indicates support for each of the combinations of the three different sets of values (sample formats, channel counts, and framerates). For example, if a range structure indicated support for: 单一范围结构表示支持三种不同值集（样本格式，通道计数和帧速率）的每种组合。例如，如果范围结构表明支持：

 
*   16 bit signed LPCM samples  * 16位带符号PCM样本
*   48000, and 44100 Hz frame rates  * 48000和44100 Hz帧频
*   1 and 2 channels  * 1和2频道

Then the fully expanded set of supported formats indicated by the range structure would be: 然后，范围结构指示的完全扩展的受支持格式集将是：

 
*   Stereo 16-bit 48 KHz audio  *立体声16位48 KHz音频
*   Stereo 16-bit 44.1 KHz audio  *立体声16位44.1 KHz音频
*   Mono 16-bit 48 KHz audio  *单声道16位48 KHz音频
*   Mono 16-bit 44.1 KHz audio  *单声道16位44.1 KHz音频

See the Sample Formats section (above) for a description of how sample formats are encoded in the `sample_formats` member of a range structure. 有关在范围结构的sample_formats成员中如何编码示例格式的说明，请参见上面的示例格式部分。

Supported channel counts are indicated using a pair of min/max channels fields which indicate an exclusive range of channel counts which apply to this range.For example, a min/max channels range of [1, 4] would indicate that this audiostream supports 1, 2, 3 or 4 channels. A range of [2, 2] would indicate thatthis audio stream supports only stereo audio. 支持的通道计数使用一对最小/最大通道字段指示，该字段指示适用于此范围的唯一通道计数范围。例如，最小/最大通道范围为[1，4]表示此音频流支持1 ，2、3或4个频道。范围[2，2]将指示此音频流仅支持立体声音频。

Supported frame rates are signalled similarly to channel counts using a pair of min/max frame per second fields along with a flags field. While the min/maxvalues provide an inclusive range of frame rates, the flags determine how tointerpret this range. Currently defined flags include: 使用每秒的最小/最大帧对字段和标志字段，以类似于信道计数的方式发送支持的帧速率。最小值/最大值提供了帧速率的范围，而标志则决定了如何解释该范围。当前定义的标志包括：

| Flag                              | Definition                               | | --------------------------------- | ---------------------------------------- || `ASF_RANGE_FLAG_FPS_CONTINUOUS`   | The frame rate range is continuous. All  |:                                   : frame rates in the range [min, max] are  ::                                   : valid.                                   :| `ASF_RANGE_FLAG_FPS_48000_FAMILY` | The frame rate range includes the        |:                                   : members of the 48 KHz family which exist ::                                   : in the range [min, max]                  :| `ASF_RANGE_FLAG_FPS_44100_FAMILY` | The frame rate range includes the        |:                                   : members of the 44.1 KHz family which     ::                                   : exist in the range [min, max]            : |标记|定义| | --------------------------------- | ---------------------------------------- || `ASF_RANGE_FLAG_FPS_CONTINUOUS` |帧速率范围是连续的。 [| ，:]范围内的所有|：：帧速率均为::：有效。 ：| `ASF_RANGE_FLAG_FPS_48000_FAMILY` |帧频范围包括[::]在[min，max]：|范围内的:::：存在的:::：成员。 `ASF_RANGE_FLAG_FPS_44100_FAMILY` |帧频范围包括44.1 KHz系列中的|：：成员，:::在[min，max]范围内：

So, conceptually, the valid frame rates are the union of the sets produced by applying each of the flags which are set to the inclusive [min, max] range. Forexample, if both the 48 KHz and 44.1 KHz were set, and the range given was[16000, 47999], then the supported frame rates for this range would be 因此，从概念上讲，有效帧速率是通过应用设置为包含（最小，最大）范围的每个标志而产生的集合的并集。例如，如果同时设置了48 KHz和44.1 KHz，并且给定的范围为[16000，47999]，则该范围支持的帧速率为

 
*   16000 Hz  * 16000赫兹
*   22050 Hz  * 22050赫兹
*   32000 Hz  * 32000赫兹
*   44100 Hz  * 44100赫兹

The official members of the 48 KHz and 44.1 KHz families are  48 KHz和44.1 KHz系列的正式成员是

| Family                            | Frame Rates                        | | --------------------------------- | ---------------------------------- || `ASF_RANGE_FLAG_FPS_48000_FAMILY` | 8000, 16000, 32000, 48000, 96000,  |:                                   : 192000, 384000, 768000             :| `ASF_RANGE_FLAG_FPS_44100_FAMILY` | 11025, 22050, 44100, 88200, 176400 | |家庭|影格速率| | --------------------------------- | ---------------------------------- || `ASF_RANGE_FLAG_FPS_48000_FAMILY` | 8000，16000，32000，48000，96000，|：：192000，384000，768000：| `ASF_RANGE_FLAG_FPS_44100_FAMILY` | 11025、22050、44100、88200、176400 |

Drivers **must** set at least one of the flags, or else the set of supported frame rates is empty and this range structure is not allowed. Also note that theset of valid frame rates is the union of the frame rates produce by applyingeach of the set flags. If the `ASF_RANGE_FLAG_FPS_CONTINUOUS` flag is set theother flags have no effect. While it is legal to do so, drivers **should** avoidthis behavior. 驱动器必须至少设置一个标志，否则支持的帧速率集为空，并且不允许使用此范围结构。还要注意，有效帧频的集合是通过应用每个设置的标志产生的帧频的并集。如果设置了“ ASF_RANGE_FLAG_FPS_CONTINUOUS”标志，则其他标志无效。虽然这样做是合法的，但驾驶员应**避免这种行为。

 
### Transporting range structures  运输范围结构 

Range structures are transmitted from drivers to applications within the `audio_stream_cmd_get_formats_resp_t` message. If a large number of formats aresupported by a stream, drivers may need to send multiple messages to enumerateall available modes. Messages include the following fields: 范围结构在“ audio_stream_cmd_get_formats_resp_t”消息中从驱动程序传输到应用程序。如果流支持大量格式，则驱动程序可能需要发送多个消息以枚举所有可用模式。消息包括以下字段：

 
*   A standard `audio_cmd_hdr_t` header. **All** messages involved in the response to an `AUDIO_STREAM_CMD_GET_FORMATS` request **must** use thetransaction ID of the original request, and the cmd field in the header**must** be `AUDIO_STREAM_CMD_GET_FORMATS`. *标准的audio_cmd_hdr_t标头。 **响应AUDIO_STREAM_CMD_GET_FORMATS请求的所有消息必须使用原始请求的事务ID，并且标头中的cmd字段必须为AUDIO_STREAM_CMD_GET_FORMATS。
*   A `format_range_count` field. This indicates the total number of format range structures which will be sent in this response to the application.This number **must** be present in **all** messages involved in theresponse, and **must not** change from message to message. *`format_range_count`字段。这表示将在此响应中发送给应用程序的格式范围结构的总数。此数量必须在响应所涉及的所有消息中存在，并且绝不能从消息中更改发消息。
*   A `first_format_range_ndx` field indicating the zero-based index of the first format range being specified in this particular message. See below fordetails. *“ first_format_range_ndx”字段指示在此特定消息中指定的第一格式范围的从零开始的索引。请参阅下面的详细信息。
*   An array of `audio_stream_cmd_get_formats_resp_t` structures which is at most `AUDIO_STREAM_CMD_GET_FORMATS_MAX_RANGES_PER_RESPONSE` elements long. *一个audio_stream_cmd_get_formats_resp_t结构的数组，最多不超过AUDIO_STREAM_CMD_GET_FORMATS_MAX_RANGES_PER_RESPONSE个元素。

Drivers **must**:  司机**必须**：

 
*   Always transmit all of the available audio format ranges.  *始终传输所有可用的音频格式范围。
*   Always transmit the available audio format ranges in ascending index order.  *始终以升序传输可用的音频格式范围。
*   Always pack as many ranges as possible in the fixed size message structure.  *始终在固定大小的消息结构中打包尽可能多的范围。
*   Never overlap index regions or leave gaps.  *切勿重叠索引区域或留有空隙。

Given these requirements, if the maximum number of ranges per response were 15, and a driver needed to send 35 ranges in response to an application's request,then 3 messages in total would be needed, and the `format_range_count` and`first_format_range_ndx` fields for each message would be as follows. 给定这些要求，如果每个响应的最大范围数为15，并且驱动程序需要发送35个范围来响应应用程序的请求，则总共需要3条消息，并且“ format_range_count”和“ first_format_range_ndx”字段用于每个消息如下。

Msg # | `format_range_count` | `first_format_range_ndx` ----- | -------------------- | ------------------------ 讯息| `format_range_count` | `first_format_range_ndx` ----- | -------------------- | ------------------------
1     | 35                   | 0  1 | 35 | 0
2     | 35                   | 15  2 | 35 | 15
3     | 35                   | 30  3 | 35 | 30

`first_format_range_ndx` **must** never be greater than `format_range_count`, however `format_range_count` **may** be zero if an audio stream currentlysupports no formats. The total number of `audio_stream_format_range_t`structures in an `audio_stream_cmd_get_formats_resp_t` message is given by theformula “ first_format_range_ndx” **必须大于“ format_range_count”，但是如果音频流当前不支持任何格式，则“ format_range_count` **”可能为零。 “ audio_stream_cmd_get_formats_resp_t”消息中“ audio_stream_format_range_t”结构的总数由公式给出

```C
valid_ranges = MIN(AUDIO_STREAM_CMD_GET_FORMATS_MAX_RANGES_PER_RESPONSE,
                   msg.format_range_count - msg.first_format_range_ndx);
```
 

Drivers **may** choose to always send an entire `audio_stream_cmd_get_formats_resp_t` message, or to send a truncated messagewhich ends after the last valid range structure in the `format_ranges` array.Applications **must** be prepared to receive up to`sizeof(audio_stream_cmd_get_formats_resp_t)` bytes for each message, but alsoaccept messages as short as `offsetof(audio_stream_cmd_get_formats_resp_t,format_ranges)` 驱动程序可能会选择始终发送完整的audio_stream_cmd_get_formats_resp_t消息，或者发送一条截断的消息，该消息在format_ranges数组中的最后一个有效范围结构之后结束。应用程序必须准备接收多达每个消息的sizeof（audio_stream_cmd_get_formats_resp_t）个字节，但也接受短至offoffof（audio_stream_cmd_get_formats_resp_t，format_ranges）的消息。

> TODO: how do devices signal a change of supported formats (e.g., HDMI hot-plug > event)? Are such devices required to simply remove and republish the device? > TODO：设备如何发出支持的格式更改的信号（例如HDMI热插拔>事件）？是否需要这些设备来简单地删除并重新发布该设备？

> TODO: define how to enumerate supported compressed bitstream formats.  > TODO：定义如何枚举支持的压缩比特流格式。

 
### Setting the desired stream format  设置所需的流格式 

In order to select a stream format, applications send an `AUDIO_STREAM_CMD_SET_FORMAT` message over the stream channel. In the message,for uncompressed audio streams, the application specifies: 为了选择流格式，应用程序通过流通道发送“ AUDIO_STREAM_CMD_SET_FORMAT”消息。在消息中，对于未压缩的音频流，应用程序指定：

 
*   The frame rate of the stream in Hz using the `frames_per_second` field (in the case of an uncompressed audio stream). *使用`frames_per_second`字段以Hz为单位的流的帧率（在未压缩音频流的情况下）。
*   The number of channels packed into each frame using the `channels` field.  *使用“通道”字段填充到每个帧中的通道数。
*   The format of the samples in the frame using the `sample_format` field (see Sample Formats, above) *使用`sample_format`字段在帧中的样本格式（请参见上面的样本格式）

Success or failure, drivers **must** respond to a request to set format using a `audio_stream_cmd_set_format_resp_t`. 成功或失败，驱动程序“必须”使用“ audio_stream_cmd_set_format_resp_t”响应设置格式的请求。

In the case of success, drivers **must** set the `result` field of the response to `ZX_OK` and **must** return a new ring buffer channel over which streamingoperations will be conducted. If a previous ring buffer channel had beenestablished and was still active, the driver **must** close this channel andmake every attempt to gracefully quiesce any on-going streaming operations inthe process. 在成功的情况下，驱动程序必须将响应的result字段设置为ZX_OK，并且必须返回新的环形缓冲区通道，在该通道上进行流操作。如果先前的环形缓冲区通道已建立并且仍处于活动状态，则驱动程序必须关闭该通道，并尽一切努力使该过程中所有正在进行的流式操作安静下来。

In the case of failure, drivers **must** indicate the cause of failure using the `result` field of the message and **must not** simply close the stream channelas is done for a generic protocol violation. Additionally, they **may** chooseto preserve a pre-existing ring-buffer channel, or to simply close such achannel as is mandated for a successful operation. 在失败的情况下，驱动程序“必须”使用消息的“结果”字段指示失败的原因，并且“绝对不能”像针对一般协议违规那样简单地关闭流通道。另外，他们可以**选择保留一个预先存在的环形缓冲区通道，或者简单地关闭为成功操作所必需的通道。

> TODO: specify how compressed bitstream formats will be set  > TODO：指定如何设置压缩比特流格式

 
## Determining external latency  确定外部延迟 

The external latency of an audio stream is defined as the amount of time it takes outbound audio to travel from the system's interconnect to the speakersthemselves, or inbound audio to travel from the microphone to the system'sinterconnect. As an example, consider an external codec connected to the systemusing a TDM interconnect: if this interconnect introduces a 4 frame delaybetween the reception of a TDM frame and the rendering of that frame at thespeakers themselves, then the external delay of this audio path is the timeduration equivalent to 4 audio frames. 音频流的外部等待时间定义为出站音频从系统互连传输到扬声器自身所花费的时间，或者入站音频从麦克风传输到系统互连所花费的时间。例如，考虑使用TDM互连连接到系统的外部编解码器：如果此互连在TDM帧的接收和扬声器本身对该帧的渲染之间引入了4帧延迟，则此音频路径的外部延迟为时间长度等于4个音频帧。

External delay is reported in the `external_delay_nsec` field of a successful `AUDIO_STREAM_CMD_SET_FORMAT` response as a non-negative number of nanoseconds.Drivers **should** make their best attempt to accurately report the total of allof the sources of delay the driver knows about. Information about this delay canfrequently be found in codec data sheets, dynamically reported as properties ofcodecs using protocols such as Intel HDA or the USB Audio specifications, orreported by down stream devices using mechanisms such as EDID when using HDMI orDisplayPort interconnects. 外部延迟在成功的AUDIO_STREAM_CMD_SET_FORMAT响应的external_delay_nsec字段中报告为非负的纳秒数。驾驶员**应尽最大努力准确报告驾驶员知道的所有延迟源。关于。有关此延迟的信息通常可以在编解码器数据表中找到，可以使用诸如Intel HDA或USB音频规范之类的协议动态报告为编解码器的属性，或者在使用HDMI或DisplayPort互连时由下游设备使用诸如EDID之类的机制来报告。

 
## Hardware Gain Control  硬件增益控制 

 
### Hardware gain control capability reporting  硬件增益控制功能报告 

In order to determine a stream's gain control capabilities, applications send an `AUDIO_STREAM_CMD_GET_GAIN` message over the stream channel. No parameters needto be supplied with this message. All stream drivers **must** respond to thismessage, regardless of whether or not the stream hardware is capable of any gaincontrol. All gain values are expressed using 32 bit floating point numbersexpressed in dB. 为了确定流的增益控制能力，应用程序通过流通道发送“ AUDIO_STREAM_CMD_GET_GAIN”消息。此消息不需要提供任何参数。所有流驱动程序**必须**响应此消息，而不管流硬件是否能够进行任何增益控制。所有增益值均使用以dB表示的32位浮点数表示。

Drivers respond to this message with values which indicate the current gain settings of the stream, as well as the stream's gain control capabilities.Current gain settings are expressed using a bool/float tuple indicating if thestream is currently muted or not along with the current dB gain of the stream.Gain capabilities consist of bool and 3 floats. The bool indicates whether ornot the stream can be muted. The floats give the minimum and maximum gainsettings, along with the `gain step size`. The `gain step size` indicates thesmallest increment with which the gain can be controlled counting from theminimum gain value. 驱动程序用指示流的当前增益设置以及流的增益控制能力的值响应此消息。当前增益设置使用布尔/浮动元组表示，指示流当前是否被静音以及当前的dB。流的增益。增益能力包括bool和3个浮点。布尔值指示是否可以使流静音。浮点数给出最小和最大增益设置，以及“增益步长”。 “增益步长”表示从最小增益值开始计数可控制的最小增量。

For example, an amplifier which has 5 gain steps of 7.5 dB each and a maximum 0 dB gain would indicate a range of (-30.0, 0.0) and a step size of 7.5.Amplifiers capable of functionally continuous gain control **may** encode theirgain step size as 0.0. 例如，如果一个放大器具有5个增益级，每个增益级为7.5 dB，最大增益为0 dB，则表示范围为（-30.0，0.0），步长为7.5。可以连续进行增益控制的放大器**可能**将其增益步长编码为0.0。

Regardless of mute capabilities, drivers for fixed gain streams **must** report their min/max gain as (0.0, 0.0). The gain step size is meaningless in thissituation, but drivers **should** report their step size as 0.0. 无论静音功能如何，固定增益流的驱动器**必须**将其最小/最大增益报告为（0.0，0.0）。增益步长在这种情况下是没有意义的，但是驱动器“应该”将其步长报告为0.0。

 
### Setting hardware gain control levels  设置硬件增益控制级别 

In order to change a stream's current gain settings, applications send an `AUDIO_STREAM_CMD_SET_GAIN` message over the stream channel. Two parameters aresupplied with this message, a set of flags which control the request, and afloat indicating the dB gain which should be applied to the stream. 为了更改流的当前增益设置，应用程序通过流通道发送“ AUDIO_STREAM_CMD_SET_GAIN”消息。该消息提供了两个参数，一组用于控制请求的标志，以及浮动的，指示应应用于流的dB增益。

Three valid flags are currently defined:  当前定义了三个有效标志：

 
*   `AUDIO_SGF_MUTE_VALID`. Set when the application wishes to set the muted/un-muted state of the stream. Clear if the application wishes topreserve the current muted/un-muted state. *`AUDIO_SGF_MUTE_VALID`。在应用程序希望设置流的静音/取消静音状态时设置。如果应用程序希望保留当前的静音/取消静音状态，则清除。
*   `AUDIO_SGF_GAIN_VALID`. Set when the application wishes to set the dB gain state of the stream. Clear if the application wishes to preserve the currentgain state. *`AUDIO_SGF_GAIN_VALID`。在应用程序希望设置流的dB增益状态时设置。如果应用程序希望保留当前增益状态，则清除。
*   `AUDIO_SGF_MUTE`. Indicates the application's desired mute/un-mute state for the stream. Significant only if `AUDIO_SGF_MUTE_VALID` is also set. *`AUDIO_SGF_MUTE`。指示应用程序所需的流静音/取消静音状态。仅当还设置了“ AUDIO_SGF_MUTE_VALID”时才有意义。

Drivers **must** fail the request with an `ZX_ERR_INVALID_ARGS` result if the application's request is incompatible with the stream's capabilities.Incompatible requests include: 如果应用程序的请求与流的功能不兼容，则驱动程序**必须使请求失败并显示ZX_ERR_INVALID_ARGS结果。不兼容的请求包括：

 
*   The requested gain is less than the minimum support gain for the stream.  *请求的增益小于流的最小支持增益。
*   The requested gain is more than the maximum support gain for the stream.  *请求的增益大于流的最大支持增益。
*   Mute was requested, but the stream does not support an explicit mute.  *请求了静音，但流不支持显式静音。

Presuming that the request is valid, drivers **should** round the request to the nearest supported gain step size. For example, if a stream can control its gainon the range from -60.0 to 0.0 dB, using a gain step size of 0.5 dB, then arequest to set the gain to -33.3 dB **should** result in a gain of -33.5 beingapplied. A request to that same stream for a gain of -33.2 dB **should** resultin a gain of -33.0 being applied. 假设请求有效，驱动器应将请求四舍五入至最接近的支持增益步长。例如，如果流可以使用0.5 dB的增益步长将其增益控制在-60.0到0.0 dB的范围内，则要求将增益设置为-33.3 dB，**应该**产生-33.5的增益被应用。对相同流的增益为-33.2 dB的请求**应该**产生-33.0的增益。

Applications **may** choose not to receive an acknowledgement of a `SET_GAIN` command by setting the `AUDIO_FLAG_NO_ACK` flag on their command. No responsemessage will be sent to the application, regardless of the success or failure ofthe command. If an acknowledgement was requested by the application, driversrespond with a message indicating the success or failure of the operation aswell as the current gain/mute status of the system (regardless of whether therequest was a success). 应用程序可能会通过在命令上设置“ AUDIO_FLAG_NO_ACK”标志来选择不接收对“ SET_GAIN”命令的确认。无论命令是成功还是失败，都不会将响应消息发送到应用程序。如果应用程序请求确认，则驱动程序将以一条消息进行响应，该消息指示操作成功或失败以及系统的当前增益/静音状态（无论请求是否成功）。

 
## Plug Detection  插头检测 

In addition to streams being published/unpublished in response to being connected or disconnected to/from their bus, streams may have the ability to beplugged or unplugged at any given point in time. For example, a set of USBheadphones may publish a new output stream when connected to USB, but choose tobe "hardwired" from a plug detection standpoint. A different USB audio adapterwith a standard 3.5mm phono jack might publish an output stream when connectedvia USB, but choose to change its plugged/unplugged state as the user plugs andunplugs an analog device via the 3.5mm jack. 除了响应于连接到总线或从总线断开连接而发布/取消发布流之外，流还可以在任何给定时间点被插入或拔出。例如，一组USB耳机在连接到USB时可能会发布新的输出流，但是从插头检测的角度出发，选择“硬连线”。通过USB连接时，带有标准3.5毫米唱机插孔的其他USB音频适配器可能会发布输出流，但是当用户通过3.5毫米插孔插入和拔出模拟设备时，选择更改其插入/拔出状态。

The ability to query the currently plugged or unplugged state of a stream, and to register for asynchonous notifications of plug state changes (if supported)is handled via plug detection messages. 查询流的当前已插入或未插入状态，以及注册插件状态更改的异步通知（如果支持）的能力是通过插件检测消息来处理的。

 
### AUDIO_STREAM_CMD_PLUG_DETECT  AUDIO_STREAM_CMD_PLUG_DETECT 

In order to determine a stream's plug detection capabilities and current plug state, and to enable or disable for asynchronous plug detection notifications,applications send a `AUDIO_STREAM_CMD_PLUG_DETECT` command over the streamchannel. Drivers respond with a set of `audio_pd_notify_flags_t`, along with atimestamp referenced from `ZX_CLOCK_MONOTONIC` indicating the last time the plugstate changed. 为了确定流的插件检测功能和当前插件状态，并启用或禁用异步插件检测通知，应用程序在流通道上发送“ AUDIO_STREAM_CMD_PLUG_DETECT”命令。驱动程序以一组audio_pd_notify_flags_t以及从ZX_CLOCK_MONOTONIC引用的时间戳来响应，该时间戳指示上次更改插入状态。

Three valid plug-detect notification flags (PDNF) are currently defined:  当前定义了三个有效的插头检测通知标志（PDNF）：

 
*   `AUDIO_PDNF_HARDWIRED` is set when the stream hardware is considered to be "hardwired". In other words, the stream is considered to be connected aslong as the device is published. Examples include a set of built-inspeakers, a pair of USB headphones, or a pluggable audio device with no plugdetection functionality. *当流硬件被认为是“硬连线的”时，设置“ AUDIO_PDNF_HARDWIRED”。换句话说，只要发布设备，就认为该流已连接。示例包括一组内置扬声器，一对USB耳机或没有插头检测功能的可插拔音频设备。
*   `AUDIO_PDNF_CAN_NOTIFY` is set when the stream hardware is capable of both asynchronously detecting that a device's plug state has changed, and sendinga notification message if the client has requested these notifications. *当流硬件既可以异步检测设备的插头状态已更改，又可以在客户端请求这些通知时发送通知消息时，将设置“ AUDIO_PDNF_CAN_NOTIFY”。
*   `AUDIO_PDNF_PLUGGED` is set when the stream hardware considers the stream to be currently in the "plugged-in" state. *当流硬件认为流当前处于“插入”状态时，将设置“ AUDIO_PDNF_PLUGGED”。

When responding to the `PLUG_DETECT` message, drivers for "hardwired" streams **must not** set the `CAN_NOTIFY` flag, and **must** set the `PLUGGED` flag.Additionally, these drivers **should** always set the plug state time to thetime at which the stream device was published by the driver. 当响应`PLUG_DETECT`消息时，“硬连线”流的驱动程序**必须**设置CAN_NOTIFY标志，**必须设置PLUGGED标志。此外，这些驱动程序也应**始终将插头状态时间设置为驱动程序发布流设备的时间。

Applications **may** choose not to receive an acknowledgement of a `PLUG_DETECT` command by setting the `AUDIO_FLAG_NO_ACK` flag on their command. No responsemessage will be sent to the application, regardless of the success or failure ofthe command. The most common use for this would be when an application wanted todisable asynchronous plug state detection messages and was not actuallyinterested in the current plugged/unplugged state of the stream. 应用程序可以通过在命令上设置“ AUDIO_FLAG_NO_ACK”标志来选择不接收对“ PLUG_DETECT”命令的确认。无论命令是成功还是失败，都不会将响应消息发送到应用程序。最常见的用法是当应用程序想要禁用异步插头状态检测消息并且实际上对流的当前插入/未插入状态不感兴趣时​​。

 
### AUDIO_STREAM_PLUG_DETECT_NOTIFY  AUDIO_STREAM_PLUG_DETECT_NOTIFY 

Applications may request that streams send them asynchronous notifications of plug state changes, using the flags field of the `AUDIO_STREAM_CMD_PLUG_DETECT`command. 应用程序可以使用“ AUDIO_STREAM_CMD_PLUG_DETECT”命令的标志字段来请求流向它们发送有关插头状态变化的异步通知。

Two valid flags are currently defined:  当前定义了两个有效标志：

 
*   `AUDIO_PDF_ENABLE NOTIFICATIONS` is set by clients in order to request that the stream proactively generate `AUDIO_STREAM_PLUG_DETECT_NOTIFY` messageswhen its plug state changes, if the stream has this capability. *“ AUDIO_PDF_ENABLE NOTIFICATIONS”由客户端设置，以请求流在其插接状态更改时主动生成“ AUDIO_STREAM_PLUG_DETECT_NOTIFY”消息，如果该流具有此功能。
*   `AUDIO_PDF_DISABLE_NOTIFICATIONS` is set by clients in order to request that NO subsequent `AUDIO_STREAM_PLUG_DETECT_NOTIFY` messages should be sent,regardless of the stream's ability to generate them. *客户端设置了“ AUDIO_PDF_DISABLE_NOTIFICATIONS”，以请求不发送任何后续的“ AUDIO_STREAM_PLUG_DETECT_NOTIFY”消息，而与流的生成能力无关。

In order to request the current plug state without altering the current notification behavior, clients simply set neither `ENABLE` nor `DISABLE` --passing either 0, or the value `AUDIO_PDF_NONE`. Clients **should** not set bothflags at the same time. If they do, drivers **must** interpret this to mean thatthe final state of the system should be _disabled_. 为了在不改变当前通知行为的情况下请求当前插头状态，客户端只需设置为0或值AUDIO_PDF_NONE即可，而不设置ENABLE或DISABLE。客户端**不应该同时设置两个标志。如果这样做，驱动程序**必须**将此解释为意味着系统的最终状态应为“已禁用”。

Clients which request asynchronous notifications of plug state changes **should** always check the `CAN_NOTIFY` flag in the driver response. Streamsmay be capable of plug detection (i.e. if `HARDWIRED` is not set), yet beincapable of detecting plug state changes asynchronously. Clients may stilllearn of plug state changes, but only by periodically polling the state with`PLUG_DETECT` commands. Drivers for streams which do not set the `CAN_NOTIFY`flag are free to ignore enable/disable notification requests from applications,and **must** not ever send an `AUDIO_STREAM_PLUG_DETECT_NOTIFY` message. Notethat even such a driver must always respond to a `AUDIO_STREAM_CMD_PLUG_DETECT`message. 请求异步通知插头状态更改的客户端应**始终在驱动程序响应中检查CAN_NOTIFY标志。流可能能够进行插件检测（即，如果未设置“ HARDWIRED”），但无法异步检测插件状态变化。客户端仍然可以了解插头状态的变化，但是只能通过使用PLUG_DETECT命令定期轮询状态。没有设置CAN_NOTIFY标志的流的驱动程序可以随意忽略来自应用程序的启用/禁用通知请求，并且**绝不要发送AUDIO_STREAM_PLUG_DETECT_NOTIFY消息。请注意，即使是这样的驱动程序也必须始终响应“ AUDIO_STREAM_CMD_PLUG_DETECT”消息。

 
## Access control capability detection and signaling  访问控制能力检测和信令 

> TODO: specify how this works. In particular, specify how drivers indicate to > applications support for various digital access control mechanisms such as> S/PDIF control words and HDCP. > TODO：指定其工作方式。特别是，指定驱动程序如何指示>应用程序支持各种数字访问控制机制，例如> S / PDIF控制字和HDCP。

 
## Stream purpose and association  流目的和关联 

> TODO: specify how drivers can indicate the general "purpose" of an audio > stream in the system (if known), as well as its relationship to other streams> (if known). For example, an embedded target like a phone or a tablet needs to> indicate which output stream is the built-in speaker vs. which is the headset> jack output. In addition, it needs to make clear which input stream is the> microphone associated with the headset output vs. the builtin speaker. > TODO：指定驱动程序如何指示音频>系统中流的一般“用途”（如果已知），以及它与其他流的关系（如果已知）。例如，诸如电话或平板电脑之类的嵌入式目标需要>指示哪个输出流是内置扬声器，而哪个是耳机>插孔输出。此外，还需要弄清楚与头戴式耳机输出和内置扬声器相关联的麦克风是哪个输入流。

 
## Ring-Buffer Channels  环形缓冲区通道 

 
### Overview  总览 

Once an application has successfully set the format of a stream, it receives in the response a new [channel](/docs/concepts/objects/channel.md) representing its connectionto the stream's ring-buffer. Clients use the ring-buffer channel to establish ashared memory buffer and start/stop playback/capture of audio stream data. 一旦应用程序成功设置了流的格式，它就会在响应中接收一个新的[channel]（/ docs / concepts / objects / channel.md），表示它与流的环形缓冲区的连接。客户端使用环形缓冲区通道建立共享的内存缓冲区，并开始/停止播放/捕获音频流数据。

Once started, stream consumption/production is assumed to proceed at the nominal rate from the point in time given in a successful response to the start command,allowing clients to operate without the need to receive any periodicnotifications about consumption/production position from the ring buffer itself.Note that the ring-buffer will almost certainly have some form of FIFO bufferbetween the memory bus and the audio hardware which causes it to eitherread-ahead in the stream (in the case of playback), or potentially hold ontodata (in the case of capturing). In the case of open-loop operation, it isimportant for clients to query the size of this buffer before beginningoperation so they know how far ahead/behind the stream's nominal inferredread/write position they need to stay in order to prevent audio glitching. 一旦启动，就假定流消耗/生产从成功响应启动命令给出的时间点开始以标称速率进行，从而使客户端可以进行操作，而无需从环形缓冲区接收有关消耗/生产位置的任何定期通知请注意，环形缓冲区几乎肯定会在内存总线和音频硬件之间具有某种形式的FIFO缓冲区，这会导致环形缓冲区在流中进行预读（在播放的情况下）或可能保留在数据上（在这种情况下）捕获）。在开环操作的情况下，对于客户端来说，在开始操作之前查询此缓冲区的大小很重要，因此客户端知道他们需要保持在流的名义推断读/写位置的前/后，以防止音频毛刺。

Also note that because of the shared buffer nature of the system, and the fact that drivers are likely to be DMA-ing directly from this buffer to hardware, itis important for clients running on architectures which are not automaticallycache coherent to be sure that they have properly written-back their cache afterwriting playback data to the buffer, or invalidated their cache before readingcaptured data. 还要注意，由于系统具有共享缓冲区的性质，并且驱动程序很可能直接从该缓冲区直接DMA到硬件，因此对于运行在没有自动缓存一致性以确保它们具有以下特性的体系结构上的客户端来说，这一点很重要。在将播放数据写入缓冲区之后，适当地写回其缓存，或者在读取捕获的数据之前使它们的缓存无效。

 
### Determining the FIFO depth  确定FIFO深度 

Applications determine a stream's FIFO depth using the `AUDIO_RB_CMD_GET_FIFO_DEPTH` command. Drivers **must** return their FIFO depth,expressed in bytes, in the `fifo_depth` field of the response. To ensure properplayback or capture of audio, applications and drivers must be careful torespect this value. Drivers must not read beyond the nominal playback positionof the stream plus this number of bytes when playing audio stream data.Applications must stay this number of bytes behind the nominal capture point ofthe stream when capturing audio stream data. 应用程序使用“ AUDIO_RB_CMD_GET_FIFO_DEPTH”命令确定流的FIFO深度。驱动程序必须在响应的“ fifo_depth”字段中返回其FIFO深度（以字节表示）。为确保正确播放或捕获音频，应用程序和驱动程序必须小心遵守此值。播放音频流数据时，驱动程序读取的内容不得超出流的标称播放位置再加上此字节数。捕获音频流数据时，应用程序必须将字节数保留在流的标称捕获点之后。

Once the format of a stream is set and a ring-buffer channel has been opened, the driver **must not** change this value. From an application's point of view,it is a constant property of the ring-buffer channel. 一旦设置了流的格式并打开了环形缓冲区通道，驱动程序“绝不能”更改此值。从应用程序的角度来看，它是环形缓冲区通道的恒定属性。

 
### Obtaining a shared buffer  获取共享缓冲区 

To send or receive audio, the application must first establish a shared memory buffer. This is done by sending an `AUDIO_RB_CMD_GET_BUFFER` request over thering-buffer channel. This may only be done while the ring-buffer is stopped.Applications **must** specify two parameters when requesting a ring buffer:`min_ring_buffer_frames` and `notifications_per_ring`. 要发送或接收音频，应用程序必须首先建立共享内存缓冲区。这是通过在环形缓冲区通道上发送“ AUDIO_RB_CMD_GET_BUFFER”请求来完成的。这只能在环形缓冲区停止时完成。应用程序在请求环形缓冲区时必须指定两个参数：min_ring_buffer_frames和notifications_per_ring。

 
#### `min_ring_buffer_frames`  min_ring_buffer_frames 

The minimum number of frames of audio the client needs allocated for the ring buffer. Drivers **may** make this buffer larger to meet hardware requirements.Clients **must** use the returned VMOs size (in bytes) to determine the actualsize of the ring buffer. Clients **may not** assume that the size of the buffer(as determined by the driver) is exactly the size they requested. Drivers**must** ensure that the size of the ring buffer is an integral number of audioframes. 客户端需要为环形缓冲区分配的音频的最小帧数。驱动程序可能会增大此缓冲区以满足硬件要求。客户端必须使用返回的VMO大小（以字节为单位）来确定环形缓冲区的实际大小。客户端**可能不会**认为缓冲区的大小（由驱动程序确定）恰好是他们所请求的大小。驱动程序**必须**确保环形缓冲区的大小是音频帧的整数。

> TODO : Is it reasonable to require that drivers produce buffers which are an > integral number of audio frames in length? It certainly makes the audio> client's life easier (client code never needs to split or re-assemble a frame> before processing), but it might make it difficult for some audio hardware to> meet its requirements without making the buffer significantly larger than the> client asked for. > TODO：要求驱动程序产生的缓冲区的长度是音频帧的整数倍是否合理？当然，这可以使音频>客户端的工作更加轻松（客户端代码无需在处理之前拆分或重新组装框架），但是这可能会使某些音频硬件难以满足其要求而又不使缓冲区明显大于缓冲区。 >客户要求。

 
#### `notifications_per_ring`  `notifications_per_ring` 

The number of position update notifications (`audio_rb_position_notify_t`) the client would like the driver to send per cycle through the ring buffer. Driversshould attempt to space notifications uniformly throughout the ring. Clients**may not** rely on perfectly uniform spacing of the update notifications.Clients are not required to request any notifications and may use only starttime and FIFO depth information to determine the driver's playout or captureposition. 客户端希望驱动程序每个周期通过环形缓冲区发送的位置更新通知的数量（audio_rb_position_notify_t）。驾驶员应尝试在整个环网中均匀分布通知。客户**可能不会**依靠更新通知的完全均匀的间距，不需要客户请求任何通知，而是可以仅使用开始时间和FIFO深度信息来确定驾驶员的比赛或比赛位置。

Success or failure, drivers **must** respond to a `GET_BUFFER` request using an `audio_rb_cmd_get_buffer_resp_t` message. If the driver fails the requestbecause a buffer has already been established and the ring-buffer has alreadybeen started, it **must not** either stop the ring-buffer, or discard theexisting shared memory. If the application requests a new buffer after havingalready established a buffer while the ring buffer is stopped, it **must**consider the existing buffer is has to be invalid. Success or failure, the oldbuffer is now gone. 成功或失败，驱动程序必须使用“ audio_rb_cmd_get_buffer_resp_t”消息来响应“ GET_BUFFER”请求。如果驱动程序失败，因为已经建立了一个缓冲区并且已经启动了环形缓冲区，则该请求“必须”不要停止环形缓冲区或丢弃现有的共享内存。如果在停止环形缓冲区的同时已经建立了缓冲区的应用程序请求新缓冲区，则必须考虑现有缓冲区必须无效。成功或失败，旧缓冲区现在不见了。

If the request succeeds, the driver **must** return a handle to a [VMO](/docs/concepts/objects/vm_object.md) with permissions which allow applications to mapthe VMO into their address space using [zx_vmar_map](/docs/reference/syscalls/vmar_map.md),and to read/write data in the buffer in the case of playback, or simply to readthe data in the buffer in the case of capture. Additionally, the driver **must**report the actual number of frames of audio it will use in the buffer via the`num_ring_buffer_frames` field of the `audio_rb_cmd_get_buffer_resp_t` message.The size of the VMO returned (as reported by[zx_vmo_get_size()](/docs/reference/syscalls/vmo_get_size.md)) **must not** be larger thanthis number of frames (when converted to bytes). This number **may** be largerthan the `min_ring_buffer_frames` request from the client but **must not** besmaller than this number. 如果请求成功，则驱动程序**必须**返回[VMO]（/ docs / concepts / objects / vm_object.md）的句柄，并具有允许应用程序使用[zx_vmar_map]（/ docs / reference / syscalls / vmar_map.md），并在播放时读取/写入缓冲区中的数据，或者在捕获时读取/写入缓冲区中的数据。另外，驱动程序必须通过“ audio_rb_cmd_get_buffer_resp_t”消息的“ num_ring_buffer_frames”字段“报告”它将在缓冲区中使用的音频的实际帧数。返回的VMO的大小（由[zx_vmo_get_size（）报告） ]（/ docs / reference / syscalls / vmo_get_size.md））**不得大于此帧数（转换为字节时）。这个数字“可能”大于客户端发出的“ min_ring_buffer_frames”请求，但“一定不要”小于这个数字。

 
### Starting and Stopping the ring-buffer  启动和停止环形缓冲区 

Clients may request that a ring-buffer start or stop using the `AUDIO_RB_CMD_START` and `AUDIO_RB_CMD_STOP` commands. Success or failure,drivers **must** send a response to these requests. Attempting to start a streamwhich is already started **must** be considered a failure. Attempting to stop astream which is already stopped **should** be considered a success. Ring-bufferscannot be either stopped or started until after a shared buffer has beenestablished using the `GET_BUFFER` operation. 客户可以使用“ AUDIO_RB_CMD_START”和“ AUDIO_RB_CMD_STOP”命令来请求启动或停止环形缓冲区。成功或失败，驱动程序“必须”发送对这些请求的响应。尝试启动已经开始的流（必须**）被视为失败。尝试停止已经**停止的流媒体**应视为成功。直到使用“ GET_BUFFER”操作建立共享缓冲区后，才能停止或启动环形缓冲区。

Upon successfully starting a stream, drivers **must** provide their best estimate of the time at which their hardware began to transmit or capture thestream in the `start_time` field of the response. This time stamp **must** betaken from the clock exposed via the[ZX_CLOCK_MONOTONIC](/docs/reference/syscalls/clock_get.md) syscall. Along with the FIFOdepth property of the ring buffer, this timestamp allows applications to send orreceive stream data without the need for periodic position updates from thedriver. Along with the outboard latency estimate provided by the stream channel,this timestamp allows applications to synchronize presentation of audioinformation across multiple streams, or even multiple devices (provided that anexternal time synchronization protocol is used to synchronize the[ZX_CLOCK_MONOTONIC](/docs/reference/syscalls/clock_get.md) timelines across the cohort ofsynchronized devices). 成功启动流后，驱动程序**必须**在响应的“ start_time”字段中提供其硬件开始传输或捕获流的时间的最佳估计。此时间戳必须通过通过[ZX_CLOCK_MONOTONIC]（/ docs / reference / syscalls / clock_get.md）syscall公开的时钟进行测试。连同环形缓冲区的FIFOdepth属性，此时间戳允许应用程序发送或接收流数据，而无需驱动程序进行定期位置更新。加上流通道提供的外部等待时间估计，此时间戳允许应用程序跨多个流甚至跨多个设备同步音频信息的表示（前提是使用外部时间同步协议来同步[ZX_CLOCK_MONOTONIC]（/ docs / reference / syscalls / clock_get.md）同步设备群组中的时间轴）。

> TODO: Redefine `start_time` to allow it to be an arbitrary 'audio stream > clock' instead of the `ZX_CLOCK_MONOTONIC` clock. If the stream clock is made> to count in audio frames since start, then this `start_time` can be replaced> with the terms for a segment of a piecewise linear transformation which can be> subsequently updated via notifications sent by the driver in the case that the> audio hardware clock is rooted in a different oscillator from the system's> tick counter. Clients can then use this transformation either to control the> rate of consumption of input streams, or to determine where to sample in the> input stream to effect clock correction. > TODO：重新定义“ start_time”以使其成为任意的“音频流>时钟”，而不是“ ZX_CLOCK_MONOTONIC”时钟。如果使流时钟>从开始以来就在音频帧中计数，则可以用分段线性变换的分段的项代替该“ start_time”，然后可以通过驱动器在这种情况下发送的通知对其进行更新。 >音频硬件时钟植根于系统>滴答计数器的不同振荡器。然后，客户可以使用此转换来控制输入流的消耗速率，或确定在输入流中进行采样的位置以实现时钟校正。

Upon successfully starting a stream, drivers **must** guarantee that no position notifications will be sent before the start response has been enqueued into thering-buffer channel. 成功启动流后，驱动程序必须保证在启动响应进入环形缓冲区通道之前不会发送任何位置通知。

Upon successfully stopping a stream, drivers **must** guarantee that no position notifications will be enqueued into the ring-buffer channel after the stopresponse has been enqueued. 在成功停止流之后，驱动程序必须保证在将stopresponse排队后，不会将任何位置通知排队到环形缓冲区通道中。

 
### Position notifications  职位通知 

If requested by the client during the `GET_BUFFER` operation, the driver will periodically send updates to the client informing it of its current productionor consumption position in the buffer. This position is expressed in bytes inthe `ring_buffer_pos` field of the `audio_rb_position_notify_t` message. Themessage also includes a `monotonic_time` field that contains the time (aszx_time_t) that this byte position was valid. AUDIO_RB_POSITION_NOTIFY messages**must** only be sent while the ring-buffer is started. Note, these positionnotifications indicate where in the buffer the driver has consumed or produceddata, *not* the nominal playback or capture position (sometimes called the"write cursor" or "read cursor" respectively). The timing of their arrival isnot guaranteed to be perfectly uniform and should not be used to effect clockrecovery. However, the correspondence pair (`monotonic_time`, `ring_buffer_pos`)values themselves ARE intended to be used to recover the clock for the audiostream. If a client discovers that a driver has consumed past the point in thering buffer where that client has written playback data, audio presentation isundefined. Clients should increase their clock lead time and be certain to stayahead of this point in the stream in the future. Likewise, clients which captureaudio **should not** attempt to read beyond the point in the ring bufferindicated by the most recent position notification sent by the driver. 如果在“ GET_BUFFER”操作期间客户端请求，驱动程序将定期向客户端发送更新，以通知其当前在缓冲区中的生产或消费状况。该位置在“ audio_rb_position_notify_t”消息的“ ring_buffer_pos”字段中以字节表示。 Themessage还包含一个`monotonic_time`字段，其中包含该字节位置有效的时间（aszx_time_t）。 AUDIO_RB_POSITION_NOTIFY消息**必须仅在启动环形缓冲区时发送。注意，这些位置通知指示驱动程序已在缓冲区中消费或产生数据的位置，而不是标称的播放或捕获位置（有时分别称为“写入游标”或“读取游标”）。它们到达的时间不能保证是完全一致的，不应用于实现时钟恢复。但是，对应对（“ monotonic_time”，“ ring_buffer_pos”）的值本身旨在用于恢复音频流的时钟。如果客户端发现驱动程序消耗了超过该客户端已写入回放数据的环形缓冲区中的点，则音频表示未定义。客户应增加其时钟提前期，并确保将来在这一点上保持领先。同样，捕获音频的客户端“不应”尝试读取超出驾驶员发送的最新位置通知所指示的环形缓冲区中的点。

Driver playback/capture position **must** *always* begin at ring buffer byte 0, immediately following a successful `AUDIO_RB_CMD_START` command. When the ringbuffer position reaches the end of the VMO (as indicated by[zx_vmo_get_size(...)](/docs/reference/syscalls/vmo_get_size.md)), the ring buffer positionwraps back to zero. Drivers are not required to consume or produce data inintegral numbers of audio frames. Clients whose notion of stream positiondepends on position notifications should take care to request that a sufficientnumber of notifications per ring be sent (minimum 2) and to process them quicklyenough that aliasing does not occur. 成功执行“ AUDIO_RB_CMD_START”命令后，驱动程序的回放/捕获位置必须（始终）始终从环形缓冲区字节0开始。当环形缓冲区位置到达VMO的末尾时（如[zx_vmo_get_size（...）]（/ docs / reference / syscalls / vmo_get_size.md）所示），环形缓冲区位置将回零。不需要驱动程序消耗或产生整数个音频帧的数据。流位置取决于位置通知的客户端应注意，请求每个环发送足够数量的通知（最少2个），并在不发生混叠的情况下迅速对其进行处理。

 
### Clock recovery  时钟恢复 

> TODO: rewrite this section to include how clock recovery occurs, and how this > is exposed to clients. Also, detail how slewable oscillators are discovered> and controlled. We may need rate-change notifications to clients of slewable> clocks.>> Previous content: TODO: define a way that clock recovery information can be> sent to clients in the case that the audio output oscillator is not derived> from the `ZX_CLOCK_MONOTONIC` oscillator. In addition, if the oscillator is> slew-able in hardware, provide the ability to discover this capability and> control the slew rate. Given the fact that this oscillator is likely to be> shared by multiple streams, it might be best to return some form of system> wide clock identifier and provide the ability to obtain a channel on which> clock recovery notifications can be delivered to clients and HW slewing> command can be sent from clients to the clock. > TODO：重写此部分以包括如何进行时钟恢复，以及如何向客户端公开此时钟。另外，详细说明如何发现和控制可摆振荡器。我们可能需要向客户端发送速率变化通知，其中包括可时钟时钟。>>上一内容：TODO：定义了一种方式，可以在不从音频输出振荡器派生音频的情况下，从ZX_CLOCK_MONOTONIC向客户端发送时钟恢复信息。振荡器。另外，如果振荡器>在硬件上可以转换，则可以发现该功能并>控制转换速率。考虑到该振荡器可能被多个流共享的事实，最好返回某种形式的系统>宽时钟标识符，并提供获得通道的能力，在该通道上可以将时钟恢复通知传递给客户端和HW slewing>命令可以从客户端发送到时钟。

 
### Error notifications  错误通知 

> TODO: define these and what driver behavior should be, if/when they occur.  > TODO：定义这些以及驱动程序的行为（如果/何时发生）。

 
### Unexpected client termination  客户端意外终止 

If the client side of a ring buffer control channel is closed for any reason, drivers **must** immediately close the control channel and shut down the ringbuffer, such that no further audio is emitted nor captured. While drivers areencouraged to do so in a way which produces a graceful transition to silence,they **must** ensure that the audio stream goes silent instead of looping. Oncethe transition to silence is complete, resources associated with playback orcapture **may** be released and reused by the driver. 如果由于某种原因关闭了环形缓冲区控制通道的客户端，则驱动程序必须立即关闭控制通道并关闭环形缓冲区，这样就不会再发出或捕获任何音频。鼓励驱动程序以一种使声音平稳过渡到静音的方式进行操作，但他们必须确保音频流变为静音而不是循环播放。一旦完成向静音的过渡，与播放或捕获相关的资源可能会被驱动程序释放并重新使用。

